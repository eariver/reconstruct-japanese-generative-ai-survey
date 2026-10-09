#!/usr/bin/env python3
"""LF-1 correction evidence runner with asserting pre/post guards (R1 strict).

Usage:
  python3 run_evidence.py LOG [--dst D] [--expect-head H] [--expect-tree T]
      [--expect-mod M] [--expect-schema S] [--expect-test U]
      [--proof-postdrift-file F] -- [unittest-args...]

Real runs pass only LOG and unittest args; every expected value then comes from
the pinned constants below. Proof runs pass explicit --expect-*/--dst flags
(the proof argv is recorded in the log, so overrides are disclosed, never
silent). Exit codes: 0 child PASS + postguard PASS; 1 child FAILED + postguard
PASS; 2 pre-guard REFUSE (child never spawned, no CHILD_SPAWN line); 3
post-guard FAILED (child exit reported alongside, never masked).

The single shared guard() runs BEFORE the child AND in a finally AFTER it;
postguard failure yields nonzero even when the child exits 0. The log file is
created exclusively (open(...,'x')). The child runs from the pinned copy with
file-protocol-only Git runtime. Post-source-drift proofs must use a disposable
independent copy via --dst and never the actual candidate.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import os
import platform
import subprocess
import sys
from pathlib import Path

PIN_DST = "/tmp/opencode/jgas-lf1-design-20261009T001653Z"
PIN_HEAD = "409b292756dd1277b9dfae87679934c0d2ce251c"
PIN_TREE = "8ce3699861505f32d1d60bdc185d4d4f635aedb2"
PIN_MOD = "233e86557f1627203a4f1e4129c953bf34e1319bd8949b1d58b7d417b0744cf7"
PIN_SCHEMA = "7bae9d2ac753c83521165c76c9e461ce40ac4e704d9b44d3518ae7b88fbd0643"
PIN_TEST = "ce687447539a99eb92532bc34246a271fb489b259e63b31ed6699fcc12fbf913"
PIN_STATUS = (
    "?? schemas/longform-reader-input-v2.schema.json\n"
    "?? scripts/survey_longform_derivation_v2.py\n"
    "?? tests/test_survey_longform_derivation_v2.py"
)
PIN_FILES = (
    "scripts/survey_longform_derivation_v2.py",
    "schemas/longform-reader-input-v2.schema.json",
    "tests/test_survey_longform_derivation_v2.py",
)
GIT_OVERRIDE_VARS = (
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_COMMON_DIR",
)
PYTHON_ROUTING_VARS = ("PYTHONPATH", "PYTHONHOME")


class GuardFailure(Exception):
    """Raised when a pinned guard comparison fails."""


def _run_git(dst: str, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", dst, *args],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if proc.returncode != 0:
        raise GuardFailure(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def guard(dst: str, exp: dict[str, str]) -> dict[str, str]:
    """Compare every pinned source identity value; raise GuardFailure on drift."""
    actual: dict[str, str] = {}
    actual["head"] = _run_git(dst, "rev-parse", "HEAD").strip()
    if actual["head"] != exp["head"]:
        raise GuardFailure(
            f"HEAD mismatch: actual={actual['head']} expected={exp['head']}"
        )
    actual["tree"] = _run_git(dst, "rev-parse", "HEAD^{tree}").strip()
    if actual["tree"] != exp["tree"]:
        raise GuardFailure(
            f"tree mismatch: actual={actual['tree']} expected={exp['tree']}"
        )
    actual["status"] = _run_git(
        dst, "status", "--porcelain=v1", "--untracked-files=all"
    ).rstrip("\n")
    if actual["status"] != exp["status"]:
        raise GuardFailure(
            f"status predicate failed:\nactual:\n{actual['status']}\n"
            f"expected:\n{exp['status']}"
        )
    tracked = _run_git(dst, "diff", "--name-only", "HEAD").strip()
    actual["tracked"] = tracked
    if tracked:
        raise GuardFailure(f"tracked modifications present: {tracked}")
    for key, rel in (("mod", PIN_FILES[0]), ("schema", PIN_FILES[1]), ("test", PIN_FILES[2])):
        got = _sha256_file(Path(dst) / rel)
        actual[key] = got
        if got != exp[key]:
            raise GuardFailure(
                f"overlay hash mismatch for {rel}: actual={got} expected={exp[key]}"
            )
    remotes = _run_git(dst, "remote", "-v").strip()
    actual["remotes"] = remotes
    for line in remotes.splitlines():
        if "example.invalid" not in line:
            raise GuardFailure(f"non-inert remote: {line}")
    alternates = Path(dst) / ".git" / "objects" / "info" / "alternates"
    if alternates.exists():
        raise GuardFailure("git alternates file present (object sharing)")
    multilink = subprocess.run(
        ["find", os.path.join(dst, ".git", "objects"),
         "-type", "f", "-links", "+1"],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if multilink.stdout.strip():
        raise GuardFailure("hardlinked git objects present (object sharing)")
    actual["multilink"] = ""
    return actual


def parse_args(argv: list[str]) -> argparse.Namespace:
    # Deterministic split: runner flags come before a mandatory `--`, unittest
    # args after it. (argparse REMAINDER swallows interspersed optionals, so a
    # manual split keeps proof-override flags from ever leaking into the child.)
    if "--" not in argv:
        raise _UsageError("missing mandatory `--` separator before unittest args")
    cut = argv.index("--")
    runner_argv, child_args = argv[:cut], argv[cut + 1:]
    if not child_args:
        raise _UsageError("no unittest args after `--`")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dst", default=PIN_DST)
    parser.add_argument("--expect-head", default=PIN_HEAD)
    parser.add_argument("--expect-tree", default=PIN_TREE)
    parser.add_argument("--expect-mod", default=PIN_MOD)
    parser.add_argument("--expect-schema", default=PIN_SCHEMA)
    parser.add_argument("--expect-test", default=PIN_TEST)
    parser.add_argument(
        "--proof-postdrift-file", default=None,
        help="PROOF ONLY (disposable --dst): create this untracked file in "
             "dst after a passing child and before the postguard, proving a "
             "post-source drift yields nonzero even when the child exits 0.",
    )
    parsed = parser.parse_args(runner_argv)
    parsed.child_args = child_args
    return parsed


class _UsageError(Exception):
    """Raised for CLI usage errors (logged, then exit 2)."""


def main(argv: list[str]) -> int:
    if not argv:
        print("REFUSE: missing log path", file=sys.stderr)
        return 2
    log_path = argv[0]
    try:
        log_handle = open(log_path, "x", encoding="utf-8")  # noqa: PTH123
    except FileExistsError:
        print(f"REFUSE: log path already exists (exclusive): {log_path}", file=sys.stderr)
        return 2

    def emit(line: str = "") -> None:
        log_handle.write(line + "\n")
        log_handle.flush()

    emit(f"runner_argv={argv}")
    try:
        args = parse_args(argv[1:])
    except _UsageError as exc:
        emit(f"REFUSE (usage): {exc}")
        emit("DONE")
        log_handle.close()
        print(f"REFUSE (usage): {exc} (child not executed)", file=sys.stderr)
        return 2

    exp = {
        "head": args.expect_head,
        "tree": args.expect_tree,
        "status": PIN_STATUS,
        "mod": args.expect_mod,
        "schema": args.expect_schema,
        "test": args.expect_test,
    }
    for var in (*GIT_OVERRIDE_VARS, *PYTHON_ROUTING_VARS):
        if os.environ.get(var):
            emit(f"REFUSE: unsafe inherited routing override: {var}={os.environ[var]}")
            emit("DONE")
            log_handle.close()
            print(f"REFUSE: unsafe inherited routing override: {var} (child not executed)",
                  file=sys.stderr)
            return 2
    try:
        actual = guard(args.dst, exp)
    except GuardFailure as exc:
        emit("=== PRE guard REFUSE (child not executed) ===")
        emit(f"REFUSE: {exc}")
        emit(f"dst={args.dst}")
        emit("DONE")
        log_handle.close()
        print(f"REFUSE: {exc} (child not executed)", file=sys.stderr)
        return 2

    emit("=== PRE identity (pinned, asserted) ===")
    emit(f"dst={args.dst}")
    emit(f"expected_head={exp['head']} actual_head={actual['head']}")
    emit(f"expected_tree={exp['tree']} actual_tree={actual['tree']}")
    emit(f"expected_mod={exp['mod']} actual_mod={actual['mod']}")
    emit(f"expected_schema={exp['schema']} actual_schema={actual['schema']}")
    emit(f"expected_test={exp['test']} actual_test={actual['test']}")
    emit("--- status (exact) ---")
    emit(actual["status"])
    emit("--- tracked diff (empty) ---")
    emit(f"[{actual['tracked']}]")
    emit("=== runtime ===")
    emit(f"interpreter={sys.executable}")
    emit(f"version={platform.python_version()}")
    emit(f"caller_cwd={os.getcwd()}")
    emit(f"child_cwd={args.dst} (child runs from pinned copy)")
    emit(f"argv={sys.argv}")
    emit("--- env (filtered) ---")
    for key in sorted(os.environ):
        if key.startswith("GIT_") or key.startswith("PYTHON") or key in (
            "PATH", "PWD", "LANG", "LC_ALL", "LC_CTYPE",
        ):
            emit(f"{key}={os.environ[key]}")
    emit(f"git_remotes={actual['remotes'].replace(chr(10), ' | ')}")
    emit("git_allow_protocol=file git_no_lazy_fetch=1 (child env)")
    emit(f"date_utc={datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}")
    emit("=== RUN (child from pinned copy) ===")
    emit("CHILD_SPAWN")
    child_env = dict(os.environ)
    child_env["GIT_NO_LAZY_FETCH"] = "1"
    child_env["GIT_OPTIONAL_LOCKS"] = "0"
    child_env["GIT_ALLOW_PROTOCOL"] = "file"
    child_env["PYTHONDONTWRITEBYTECODE"] = "1"
    child_exit: int | None = None
    post_failure: str | None = None
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", *args.child_args],
            cwd=args.dst,
            env=child_env,
            capture_output=True,
            text=True,
            timeout=3600,
        )
        emit(proc.stdout.rstrip("\n"))
        emit(proc.stderr.rstrip("\n"))
        child_exit = proc.returncode
    except subprocess.TimeoutExpired:
        emit("CHILD_TIMEOUT after 3600s")
        child_exit = 124
    finally:
        if args.proof_postdrift_file and child_exit == 0:
            drift_path = Path(args.dst) / args.proof_postdrift_file
            drift_path.write_text("proof post-source drift canary\n", encoding="utf-8")
            emit(f"PROOF_POSTDRIFT planted: {args.proof_postdrift_file} "
                 f"(disposable dst only, disclosed)")
        emit(f"unittest_exit:{child_exit}")
        emit("=== POST guard (finally, asserted) ===")
        try:
            post = guard(args.dst, exp)
        except GuardFailure as exc:
            post_failure = str(exc)
            emit(f"POSTGUARD_FAILED: {exc}")
            emit(f"child_exit_was={child_exit} (propagated alongside, never masked)")
    if post_failure is not None:
        emit("OUTCOME=POSTGUARD_FAILED")
        emit("DONE")
        log_handle.close()
        print(f"RUNNER_DONE log={log_path} child_exit={child_exit} postguard=FAILED",
              file=sys.stderr)
        return 3
    emit(f"post_head={post['head']}")
    emit(f"post_tree={post['tree']}")
    emit("--- post status (exact) ---")
    emit(post["status"])
    emit("--- post tracked diff (empty) ---")
    emit(f"[{post['tracked']}]")
    emit("--- post overlay hashes ---")
    emit(f"mod={post['mod']} schema={post['schema']} test={post['test']}")
    if child_exit != 0:
        emit(f"CHILD_FAILED exit={child_exit} (propagated, not masked)")
    else:
        emit("CHILD_PASSED exit=0")
    emit("OUTCOME=" + ("PASS" if child_exit == 0 else "CHILD_FAILED"))
    emit("DONE")
    log_handle.close()
    print(f"RUNNER_DONE log={log_path} child_exit={child_exit} postguard=PASS",
          file=sys.stderr)
    return child_exit if child_exit is not None else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
