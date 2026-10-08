#!/usr/bin/env python3
"""DM-004 saved runner: fail-closed guarded execution with durable in-file guards.

Creates a unique absent per-run directory, writes literal argv/cwd/runtime/env
plus fresh expected-HEAD/tree/source-hash/clean assertions BEFORE the run,
captures raw stdout/stderr/numeric exit to files, then writes the same
assertions AFTER the run. Aborts on drift; never invents transcripts.

Modes: parent-witness | new | affected
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

E170_HEAD = "e1705b7fed01369767ab9d827c0360117d54aa1f"
E170_TREE = "3d21322587b9e4d3d05d7ae9ef66fbd1d74d3557"
SOURCE_RELPATHS = [
    "scripts/survey_agent_control_v2.py",
    ".github/workflows/survey-production-v2-release.yml",
    "scripts/survey_release_checkpoint_v2.py",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def git(repo: Path, env: dict, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, env=env,
    )


def collect_guard(repo: Path, env: dict, argv: list[str], label: str) -> tuple[dict, list[str]]:
    head = git(repo, env, "rev-parse", "HEAD").stdout.strip()
    tree = git(repo, env, "rev-parse", "HEAD^{tree}").stdout.strip()
    parent = git(repo, env, "rev-parse", "HEAD^").stdout.strip()
    branch = git(repo, env, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    status = git(repo, env, "status", "--porcelain").stdout
    remote = git(repo, env, "remote", "-v").stdout.strip()
    alternates = (repo / ".git" / "objects" / "info" / "alternates").exists()
    sources = {}
    for rel in SOURCE_RELPATHS:
        p = repo / rel
        if p.is_file():
            sources[rel] = sha256_file(p)
    problems: list[str] = []
    return ({
        "label": label,
        "argv": argv,
        "cwd": str(repo),
        "runtime": {"python": sys.version.split()[0], "executable": sys.executable},
        "env": {k: env.get(k) for k in sorted(env) if k.startswith(("GIT_", "PYTHON", "PATH"))},
        "head": head, "tree": tree, "parent": parent, "branch": branch,
        "status_porcelain": status, "remote": remote,
        "alternates_present": alternates, "source_sha256": sources,
        "problems": problems,
    }, problems)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out-root", required=True)
    ap.add_argument("--run-name", required=True)
    ap.add_argument("--expect-head", required=True)
    ap.add_argument("--expect-tree", required=True)
    ap.add_argument("--mode", required=True, choices=["parent-witness", "new", "affected"])
    ap.add_argument("--venv", required=True)
    args = ap.parse_args()
    repo = Path(args.repo).resolve()
    out_root = Path(args.out_root).resolve()
    rundir = out_root / args.run_name
    if rundir.exists():
        print(f"refusing to reuse existing run dir: {rundir}", file=sys.stderr)
        return 3
    rundir.mkdir(parents=True)

    path = f"{args.venv}/bin:/usr/bin:/bin"
    env = dict(os.environ)
    env.update({
        "PATH": path,
        "PYTHONPATH": ".",
        "PYTHONDONTWRITEBYTECODE": "1",
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_ALLOW_PROTOCOL": "file",
    })
    py = f"{args.venv}/bin/python"

    if args.mode == "parent-witness":
        argv = [py, "scripts/survey_agent_control_v2.py", "--repo-root", ".",
                "validate-state", "--state", "sources/SP001/production-state.json"]
    elif args.mode == "new":
        argv = [py, "-m", "unittest",
                "tests.test_survey_dm004_release_validate_state_v2", "-v"]
    else:
        argv = [py, "-m", "unittest",
                "tests.test_survey_agent_control_v2",
                "tests.test_survey_release_checkpoint_v2", "-v"]

    pre, _ = collect_guard(repo, env, argv, "pre")
    pre_ok = (pre["head"] == args.expect_head and pre["tree"] == args.expect_tree
              and pre["status_porcelain"] == "")
    pre["expect_head"] = args.expect_head
    pre["expect_tree"] = args.expect_tree
    pre["guard_ok"] = pre_ok
    (rundir / "guard-pre.json").write_text(json.dumps(pre, indent=2), encoding="utf-8")
    if not pre_ok:
        (rundir / "ABORTED-DRIFT").write_text(
            f"pre-run guard mismatch: head={pre['head']} tree={pre['tree']} "
            f"status={pre['status_porcelain']!r}\n", encoding="utf-8")
        return 3

    proc = subprocess.run(argv, cwd=str(repo), env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (rundir / "stdout.log").write_bytes(proc.stdout)
    (rundir / "stderr.log").write_bytes(proc.stderr)
    (rundir / "exit").write_text(f"{proc.returncode}\n", encoding="utf-8")

    post, _ = collect_guard(repo, env, argv, "post")
    post["exit"] = proc.returncode
    post_ok = (post["head"] == args.expect_head and post["tree"] == args.expect_tree
               and post["status_porcelain"] == "")
    post["expect_head"] = args.expect_head
    post["expect_tree"] = args.expect_tree
    post["guard_ok"] = post_ok
    (rundir / "guard-post.json").write_text(json.dumps(post, indent=2), encoding="utf-8")
    if not post_ok:
        (rundir / "ABORTED-DRIFT").write_text(
            f"post-run guard mismatch: head={post['head']} tree={post['tree']} "
            f"status={post['status_porcelain']!r}\n", encoding="utf-8")
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
