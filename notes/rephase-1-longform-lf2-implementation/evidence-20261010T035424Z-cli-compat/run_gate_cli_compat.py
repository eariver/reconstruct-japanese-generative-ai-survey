#!/usr/bin/env python3
"""Gate CLI compat check: 2 affected methods at exact final 9 hashes.

Closeout-only gap fill. No candidate edits, no 43-suite rerun, no old whole
runner (no proof suite, no apply proof, no empty commits). Runs only:
- tests.test_survey_gate_cli_persisted_review_v2.GateCliPersistedReviewV2Tests.test_generated_weekly_cli_admission_and_readback
- tests.test_survey_gate_cli_persisted_review_v2.GateCliPersistedReviewV2Tests.test_direct_primary_cli_admission_absolute_relative_and_cwd
Test bodies/oracles unchanged. Target module already uses process-local Git
identity env (no persistent user config in its own fixture path); inherited
weekly-B setUp with persistent config is NOT invoked by these two methods.
Real git and real validators; no success mocks.

Writes manifest.json / run.stdout.log / run.stderr.log / run.log exclusively.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DESIGN = Path("/tmp/opencode/jgas-lf2-design-20261009T113013Z")
EVIDENCE = Path(__file__).resolve().parent
BASE_HEAD = "409b292756dd1277b9dfae87679934c0d2ce251c"
BASE_TREE = "8ce3699861505f32d1d60bdc185d4d4f635aedb2"
BASE_PARENT = "34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4"
EXPECTED = {
    "scripts/survey_reader_surface_gate_v2.py": {"sha256": "e73058841cfa1a841030b96d5cd2fb756c6ba99d1b99522ddbf0131d1f06bbe4", "mode": "664"},
    "schemas/reader-surface-gate-v2.schema.json": {"sha256": "fe4a96f4aa87f2a527096c4d3040f92e0217ef972ddae1d7140498184a13322c", "mode": "664"},
    "schemas/longform-publication-source-manifest-v2.schema.json": {"sha256": "4dadf873096f31cf564a7db4fee42a1fc8cdd8fc039dd14a7ee01cf26043e8ca", "mode": "664"},
    "schemas/longform-reader-input-v2.schema.json": {"sha256": "7bae9d2ac753c83521165c76c9e461ce40ac4e704d9b44d3518ae7b88fbd0643", "mode": "664"},
    "scripts/survey_longform_derivation_v2.py": {"sha256": "c09c5558f9668906b7d2ed34c55281d5f6d9ed279d3237a8ffc18ac84ea41149", "mode": "664"},
    "scripts/survey_longform_generated_v2.py": {"sha256": "d480e11d1c398f79f3e894e2e1e1f56ceec507dfde376a163a58b0ebed97d3c2", "mode": "664"},
    "scripts/survey_longform_semantic_publication_v2.py": {"sha256": "4d235a388955dcedd34d6a7dc5ac7761f9fc91de8bc723eb11f68cec6a229195", "mode": "664"},
    "tests/test_survey_longform_derivation_v2.py": {"sha256": "ce687447539a99eb92532bc34246a271fb489b259e63b31ed6699fcc12fbf913", "mode": "664"},
    "tests/test_survey_longform_publication_integration_v2.py": {"sha256": "4a03b564f8fa4dd39f2b48766ddb7612cf2d8d4dacdcc42ac39f637d2bca11a4", "mode": "664"},
}
M_FILES = ("scripts/survey_reader_surface_gate_v2.py", "schemas/reader-surface-gate-v2.schema.json")
A_FILES = (
    "scripts/survey_longform_derivation_v2.py",
    "schemas/longform-reader-input-v2.schema.json",
    "tests/test_survey_longform_derivation_v2.py",
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_longform_semantic_publication_v2.py",
    "schemas/longform-publication-source-manifest-v2.schema.json",
    "tests/test_survey_longform_publication_integration_v2.py",
)
TARGET_TESTS = (
    "tests.test_survey_gate_cli_persisted_review_v2.GateCliPersistedReviewV2Tests.test_generated_weekly_cli_admission_and_readback",
    "tests.test_survey_gate_cli_persisted_review_v2.GateCliPersistedReviewV2Tests.test_direct_primary_cli_admission_absolute_relative_and_cwd",
)
GIT_OVERRIDE_VARS = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR")
PYTHON_OVERRIDE_VARS = ("PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "PYTHONOPTIMIZE")
FORCED_GIT_ENV = {"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mode_of(path: Path) -> str:
    return oct(stat.S_IMODE(path.stat().st_mode))[2:]


def check_clean_env(phase: str, record: dict) -> None:
    present_git = sorted(v for v in GIT_OVERRIDE_VARS if os.environ.get(v))
    present_py = sorted(v for v in PYTHON_OVERRIDE_VARS if os.environ.get(v))
    record.setdefault("env_checks", {})[phase] = {
        "git_present": present_git,
        "python_present": present_py,
        "optimize_flag": sys.flags.optimize,
    }
    if present_git:
        raise RuntimeError(phase + ": refusing Git routing override: " + repr(present_git))
    if present_py:
        raise RuntimeError(phase + ": refusing Python routing override: " + repr(present_py))
    if sys.flags.optimize != 0:
        raise RuntimeError(phase + ": refusing optimized interpreter mode")


def git_env() -> dict[str, str]:
    env = dict(os.environ)
    env.update(FORCED_GIT_ENV)
    return env


def child_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k not in (*GIT_OVERRIDE_VARS, *PYTHON_OVERRIDE_VARS)}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["TMPDIR"] = "/tmp/opencode"
    env.update(FORCED_GIT_ENV)
    return env


def git_checked(repo: Path, args: list[str], phase: str, record: dict) -> subprocess.CompletedProcess:
    check_clean_env(phase, record)
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, env=git_env())


def exclusive_write(path: Path, data: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
    except BaseException:
        try:
            os.close(fd)
        except OSError:
            pass
        raise


def identity_for(root: Path, phase: str, record: dict) -> dict:
    head_p = git_checked(root, ["rev-parse", "HEAD"], phase, record)
    tree_p = git_checked(root, ["rev-parse", "HEAD^{tree}"], phase, record)
    parent_p = git_checked(root, ["rev-parse", "HEAD~1"], phase, record)
    status_p = git_checked(root, ["status", "--porcelain=v1", "--untracked-files=all"], phase, record)
    overlay: dict[str, dict[str, str]] = {}
    for rel in (*M_FILES, *A_FILES):
        p = root / rel
        if not p.is_file():
            raise RuntimeError(phase + ": missing overlay file " + rel)
        overlay[rel] = {"sha256": sha256_file(p), "mode": mode_of(p)}
    return {
        "head": head_p.stdout.strip(), "head_exit": head_p.returncode,
        "tree": tree_p.stdout.strip(), "tree_exit": tree_p.returncode,
        "parent": parent_p.stdout.strip(), "parent_exit": parent_p.returncode,
        "status": status_p.stdout, "status_exit": status_p.returncode,
        "overlay": overlay,
    }


def guard_overlay(root: Path, tag: str, record: dict) -> tuple[int, dict]:
    try:
        ident = identity_for(root, "guard-" + tag, record)
    except (RuntimeError, OSError) as exc:
        return 1, {"error": tag + ": identity collection failed: " + str(exc)}
    for key, want, label in (("head_exit", 0, "rev-parse HEAD"), ("tree_exit", 0, "rev-parse tree"), ("parent_exit", 0, "rev-parse parent"), ("status_exit", 0, "status")):
        if ident[key] != want:
            return 1, {"error": tag + ": git " + label + " exit " + repr(ident[key]), "ident": ident}
    if ident["head"] != BASE_HEAD:
        return 1, {"error": tag + ": HEAD drift " + ident["head"], "ident": ident}
    if ident["tree"] != BASE_TREE:
        return 1, {"error": tag + ": tree drift " + ident["tree"], "ident": ident}
    if ident["parent"] != BASE_PARENT:
        return 1, {"error": tag + ": parent drift " + ident["parent"], "ident": ident}
    for rel, pin in EXPECTED.items():
        got = ident["overlay"][rel]
        if got["sha256"] != pin["sha256"]:
            return 1, {"error": tag + ": source hash drift " + rel + " " + got["sha256"], "ident": ident}
        if got["mode"] != pin["mode"]:
            return 1, {"error": tag + ": source mode drift " + rel + " " + got["mode"], "ident": ident}
    rows = [r for r in ident["status"].splitlines() if r.strip()]
    cache_rows = [r for r in rows if "__pycache__" in r or r.strip().endswith(".pyc")]
    src_rows = [r for r in rows if r not in cache_rows]
    allowed = {("?? " + rel) for rel in A_FILES} | {(" M " + rel) for rel in M_FILES}
    unexpected = [r for r in src_rows if r not in allowed]
    if unexpected:
        return 1, {"error": tag + ": unexpected working-tree delta: " + repr(unexpected), "ident": ident}
    if len(src_rows) != len(allowed):
        return 1, {"error": tag + ": overlay set changed: " + repr(src_rows), "ident": ident}
    ident["cache_side_effects"] = cache_rows
    return 0, ident


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()
    for name in ("manifest.json", "run.stdout.log", "run.stderr.log", "run.log"):
        if (EVIDENCE / name).exists():
            print("refusing to overwrite prior evidence: " + name, file=sys.stderr)
            return 2
    git_version = subprocess.run(["git", "--version"], capture_output=True, text=True, env=git_env())
    manifest: dict = {
        "runner": Path(__file__).name,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "runtime": sys.version,
        "sys_flags_optimize": sys.flags.optimize,
        "git_version": git_version.stdout.strip(),
        "forced_git_env": FORCED_GIT_ENV,
        "argv": sys.argv,
        "tests": list(TARGET_TESTS),
        "distinct_methods": len(TARGET_TESTS),
        "fixture_binding": "tests/test_survey_gate_cli_persisted_review_v2.py:GateCliPersistedReviewV2Tests:test_direct_primary_cli_admission_absolute_relative_and_cwd(335)/test_generated_weekly_cli_admission_and_readback(637)",
        "timeout_sec": args.timeout,
        "cwd": os.getcwd(),
        "tmpdir": os.environ.get("TMPDIR", ""),
        "design": str(DESIGN),
        "env": {k: os.environ.get(k, "") for k in ("PATH", "LANG", "LC_ALL", "TZ")},
        "base": {"head": BASE_HEAD, "tree": BASE_TREE, "parent": BASE_PARENT},
        "expected_overlay": EXPECTED,
    }
    try:
        rc_pre, detail_pre = guard_overlay(DESIGN, "pre", manifest)
    except RuntimeError as exc:
        manifest["precheck"] = "REFUSED: " + str(exc)
        exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
        print("PRE-CHECK REFUSED: " + str(exc), file=sys.stderr)
        return 2
    manifest["identity_pre"] = detail_pre.get("ident", detail_pre)
    if rc_pre != 0:
        manifest["precheck"] = "REFUSED: " + str(detail_pre.get("error", "guard failed"))
        exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
        print("PRE-CHECK REFUSED: " + str(detail_pre.get("error")), file=sys.stderr)
        return 2
    manifest["precheck"] = "PASS"
    child_argv = [sys.executable, "-m", "unittest", "-v", *TARGET_TESTS]
    manifest["child_argv"] = child_argv
    out_fd = os.open(EVIDENCE / "run.stdout.log", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    err_fd = os.open(EVIDENCE / "run.stderr.log", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    child = subprocess.Popen(child_argv, cwd=str(DESIGN), stdout=out_fd, stderr=err_fd, env=child_env())
    os.close(out_fd)
    os.close(err_fd)
    try:
        exit_code = child.wait(timeout=args.timeout)
        timed_out = False
    except subprocess.TimeoutExpired:
        child.kill()
        child.wait()
        exit_code = None
        timed_out = True
    manifest["child"] = {"exit": exit_code, "timeout": timed_out}
    if timed_out:
        try:
            rc_post, detail_post = guard_overlay(DESIGN, "post-timeout", manifest)
            manifest["identity_post"] = detail_post.get("ident", detail_post)
            manifest["postcheck"] = "PASS" if rc_post == 0 else "FAIL: " + str(detail_post.get("error"))
        except RuntimeError as exc:
            manifest["postcheck"] = "FAIL: " + str(exc)
        exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
        exclusive_write(EVIDENCE / "run.log", ("CHILD TIMEOUT after " + str(args.timeout) + "s; partial stdout/stderr preserved\n").encode())
        print("CHILD TIMEOUT after " + str(args.timeout) + "s; partial output preserved", file=sys.stderr)
        return 3
    try:
        rc_post, detail_post = guard_overlay(DESIGN, "post", manifest)
    except RuntimeError as exc:
        manifest["postcheck"] = "FAIL: " + str(exc)
        exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
        print("POST-CHECK FAIL (child exit " + repr(exit_code) + "): " + str(exc), file=sys.stderr)
        return 4
    manifest["identity_post"] = detail_post.get("ident", detail_post)
    if rc_post != 0:
        manifest["postcheck"] = "FAIL: " + str(detail_post.get("error"))
        exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
        print("POST-CHECK FAIL (child exit " + repr(exit_code) + "): " + str(detail_post.get("error")), file=sys.stderr)
        return 4
    manifest["postcheck"] = "PASS"
    exclusive_write(EVIDENCE / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())
    exclusive_write(EVIDENCE / "run.log", ("child exit " + repr(exit_code) + " pre PASS post PASS\n").encode())
    if exit_code != 0:
        print("CHILD EXIT " + repr(exit_code) + "; see run.stdout.log/run.stderr.log", file=sys.stderr)
        return 6
    print("GATE CLI COMPAT PASS: 2 methods at exact final 9 hashes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
