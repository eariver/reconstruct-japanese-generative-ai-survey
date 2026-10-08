#!/usr/bin/env python3
"""DM-004 v2 runner (correction): fail-closed guarded execution, tight env.

Differences from run_dm004.py (preserved unchanged): every Git read return
code is checked; the child env is built from a tight allowlist (no inherited
GIT_DIR/WORK_TREE/INDEX/OBJECT overrides); both shipping files' worktree
bytes are compared against committed expected-HEAD blobs pre AND post;
failing child exits propagate. Modes: new | affected only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

SHIPPING = [
    "scripts/survey_agent_control_v2.py",
    "tests/test_survey_dm004_release_validate_state_v2.py",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def tight_env(venv: str, extra: dict[str, str]) -> dict[str, str]:
    import os

    env = {
        "PATH": f"{venv}/bin:/usr/bin:/bin",
        "PYTHONPATH": ".",
        "PYTHONDONTWRITEBYTECODE": "1",
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_ALLOW_PROTOCOL": "file",
    }
    if "HOME" in os.environ:
        env["HOME"] = os.environ["HOME"]
    env.update(extra)
    for banned in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE",
                   "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES"):
        assert banned not in env, f"root override leaked: {banned}"
    return env


def git(repo: Path, env: dict, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, env=env)
    assert proc.returncode == 0, f"git {' '.join(args)} rc={proc.returncode}: {proc.stderr}"
    return proc.stdout.strip()


def blob_sha(repo: Path, env: dict, rev_path: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), "show", rev_path],
        capture_output=True, env=env)
    assert proc.returncode == 0, f"git show {rev_path} rc={proc.returncode}"
    return hashlib.sha256(proc.stdout).hexdigest()


def collect_guard(repo: Path, env: dict, argv: list[str], label: str,
                  expect: dict) -> dict:
    head = git(repo, env, "rev-parse", "HEAD")
    tree = git(repo, env, "rev-parse", "HEAD^{tree}")
    parent = git(repo, env, "rev-parse", "HEAD^")
    branch = git(repo, env, "rev-parse", "--abbrev-ref", "HEAD")
    status = git(repo, env, "status", "--porcelain")
    remote = git(repo, env, "remote", "-v")
    alternates = (repo / ".git" / "objects" / "info" / "alternates").exists()
    pins = {}
    for rel, expected_blob in zip(SHIPPING, (expect["controller_blob"],
                                             expect["test_blob"])):
        worktree = sha256_file(repo / rel)
        committed = blob_sha(repo, env, f"HEAD:{rel}")
        pins[rel] = {"worktree_sha256": worktree,
                     "head_blob_sha256": committed,
                     "expected_blob_sha256": expected_blob,
                     "match": worktree == committed == expected_blob}
    guard = {"label": label, "argv": argv, "cwd": str(repo),
             "runtime": {"python": sys.version.split()[0],
                         "executable": sys.executable},
             "env": dict(sorted(env.items())),
             "head": head, "tree": tree, "parent": parent, "branch": branch,
             "status_porcelain": status, "remote": remote,
             "alternates_present": alternates, "source_pins": pins,
             "expect_head": expect["head"], "expect_tree": expect["tree"]}
    guard["guard_ok"] = (
        head == expect["head"] and tree == expect["tree"] and status == ""
        and not alternates and all(v["match"] for v in pins.values()))
    return guard


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out-root", required=True)
    ap.add_argument("--run-name", required=True)
    ap.add_argument("--expect-head", required=True)
    ap.add_argument("--expect-tree", required=True)
    ap.add_argument("--expect-controller-blob", required=True)
    ap.add_argument("--expect-test-blob", required=True)
    ap.add_argument("--mode", required=True, choices=["new", "affected"])
    ap.add_argument("--venv", required=True)
    args = ap.parse_args()
    repo = Path(args.repo).resolve()
    out_root = Path(args.out_root).resolve()
    rundir = out_root / args.run_name
    if rundir.exists():
        print(f"refusing to reuse existing run dir: {rundir}", file=sys.stderr)
        return 3
    rundir.mkdir(parents=True)
    env = tight_env(args.venv, {})
    py = f"{args.venv}/bin/python"
    expect = {"head": args.expect_head, "tree": args.expect_tree,
              "controller_blob": args.expect_controller_blob,
              "test_blob": args.expect_test_blob}
    if args.mode == "new":
        argv = [py, "-m", "unittest",
                "tests.test_survey_dm004_release_validate_state_v2", "-v"]
    else:
        argv = [py, "-m", "unittest",
                "tests.test_survey_agent_control_v2",
                "tests.test_survey_release_checkpoint_v2", "-v"]
    pre = collect_guard(repo, env, argv, "pre", expect)
    (rundir / "guard-pre.json").write_text(json.dumps(pre, indent=2),
                                           encoding="utf-8")
    if not pre["guard_ok"]:
        (rundir / "ABORTED-DRIFT").write_text("pre-run guard mismatch\n",
                                              encoding="utf-8")
        return 3
    proc = subprocess.run(argv, cwd=str(repo), env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (rundir / "stdout.log").write_bytes(proc.stdout)
    (rundir / "stderr.log").write_bytes(proc.stderr)
    (rundir / "exit").write_text(f"{proc.returncode}\n", encoding="utf-8")
    post = collect_guard(repo, env, argv, "post", expect)
    post["exit"] = proc.returncode
    (rundir / "guard-post.json").write_text(json.dumps(post, indent=2),
                                            encoding="utf-8")
    if not post["guard_ok"]:
        (rundir / "ABORTED-DRIFT").write_text("post-run guard mismatch\n",
                                              encoding="utf-8")
        return 3
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
