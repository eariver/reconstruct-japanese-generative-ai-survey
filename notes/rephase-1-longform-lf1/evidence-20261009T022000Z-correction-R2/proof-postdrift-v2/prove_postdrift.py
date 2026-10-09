#!/usr/bin/env python3
"""Narrow post-drift guard proof v2 (closeout only, no suite rerun).

Single executable capture for the numeric guard claim: every external command
runs via subprocess.run and its .returncode is recorded directly — no shell
pipeline anywhere in the capture path (the v1 shell log masked the runner's
exit behind `tee`, see evidence-qualification.md). Proves the final
run_evidence.py (pinned hashes) returns nonzero when the child exits 0 but the
postguard observes source drift — inside a NEW disposable independent copy,
never the candidate. Child = one fast pure unit test only; the 31-method suite
is NOT rerun (accepted, untouched).

Exits 0 iff runner returncode == 3 AND candidate pre/post status identical
AND no canary in candidate. No source/candidate/refs writes; no network.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys

CAND = "/tmp/opencode/jgas-lf1-design-20261009T001653Z"
DISP = "/tmp/opencode/jgas-lf1-proof-disposable-v2-20261009T025927Z"
PACKET = (
    "/home/eariver/git/reconstruct-japanese-generative-ai-survey"
    "/notes/rephase-1-longform-lf1/evidence-20261009T022000Z-correction-R2"
)
RUNNER = PACKET + "/run_evidence.py"
SUBDIR = PACKET + "/proof-postdrift-v2"
CAPTURE = SUBDIR + "/capture.log"
RUNNER_LOG = SUBDIR + "/runner-postdrift-v2.log"
CANARY = "drift-canary-proof-v2.json"
PURE_TEST = (
    "tests.test_survey_longform_derivation_v2"
    ".LongformDerivationV2Tests.test_pure_policy_boundaries_without_chain"
)
PIN_STATUS = (
    "?? schemas/longform-reader-input-v2.schema.json\n"
    "?? scripts/survey_longform_derivation_v2.py\n"
    "?? tests/test_survey_longform_derivation_v2.py"
)

GIT_ENV = {
    "GIT_NO_LAZY_FETCH": "1",
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_ALLOW_PROTOCOL": "file",
}
FAILURES: list[str] = []


def main() -> int:
    try:
        handle = open(CAPTURE, "x", encoding="utf-8")  # noqa: PTH123
    except FileExistsError:
        print(f"REFUSE: capture log already exists: {CAPTURE}", file=sys.stderr)
        return 2

    def emit(line: str = "") -> None:
        handle.write(line + "\n")
        handle.flush()

    def sh(args: list[str], label: str, cwd: str | None = None) -> subprocess.CompletedProcess[str]:
        emit(f"$ {' '.join(args)}" + (f"  [cwd={cwd}]" if cwd else ""))
        try:
            proc = subprocess.run(
                args, capture_output=True, text=True, timeout=600, cwd=cwd,
            )
        except subprocess.TimeoutExpired:
            emit("TIMEOUT after 600s")
            FAILURES.append(f"{label}: timeout")
            raise
        emit(f"returncode={proc.returncode}")
        if proc.stdout:
            emit("--- stdout ---")
            emit(proc.stdout.rstrip("\n"))
        if proc.stderr:
            emit("--- stderr ---")
            emit(proc.stderr.rstrip("\n"))
        return proc

    def check(label: str, condition: bool, detail: str = "") -> None:
        emit(f"CHECK {label}: {'PASS' if condition else 'FAIL'}" + (f" ({detail})" if detail else ""))
        if not condition:
            FAILURES.append(label)

    os.environ.update(GIT_ENV)
    emit("=== proof-postdrift v2: direct returncode capture (no shell pipe) ===")
    emit(f"candidate={CAND}")
    emit(f"disposable(NEW)={DISP}")
    emit(f"runner={RUNNER} (unmodified final pins)")
    for var in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR",
                "PYTHONPATH", "PYTHONHOME"):
        check(f"env-absent:{var}", not os.environ.get(var), os.environ.get(var, ""))

    emit("=== candidate pre-proof (must be clean 3-path overlay) ===")
    pre_status = sh(["git", "-C", CAND, "status", "--porcelain=v1", "--untracked-files=all"], "cand-pre-status")
    pre_diff = sh(["git", "-C", CAND, "diff", "--name-only", "HEAD"], "cand-pre-diff")
    check("cand-pre-status-exit", pre_status.returncode == 0)
    check("cand-pre-status-exact", pre_status.stdout.rstrip("\n") == PIN_STATUS)
    check("cand-pre-diff-empty", pre_diff.stdout.strip() == "")

    emit("=== fresh disposable byte-copy (never the old one, which was removed) ===")
    check("disp-absent-before", not os.path.exists(DISP), DISP)
    cp = sh(["cp", "-a", CAND, DISP], "cp-a")
    check("cp-exit", cp.returncode == 0)
    head = sh(["git", "-C", DISP, "rev-parse", "HEAD"], "disp-head")
    tree = sh(["git", "-C", DISP, "rev-parse", "HEAD^{tree}"], "disp-tree")
    st = sh(["git", "-C", DISP, "status", "--porcelain=v1", "--untracked-files=all"], "disp-status")
    check("disp-head", head.stdout.strip() == "409b292756dd1277b9dfae87679934c0d2ce251c", head.stdout.strip())
    check("disp-tree", tree.stdout.strip() == "8ce3699861505f32d1d60bdc185d4d4f635aedb2", tree.stdout.strip())
    check("disp-status-exact", st.stdout.rstrip("\n") == PIN_STATUS)
    rem = sh(["git", "-C", DISP, "remote", "-v"], "disp-remote")
    check("disp-remote-inert",
          all("example.invalid" in ln for ln in rem.stdout.splitlines() if ln.strip()))
    check("disp-no-alternates",
          not os.path.exists(os.path.join(DISP, ".git", "objects", "info", "alternates")))
    multilink = sh(["find", os.path.join(DISP, ".git", "objects"),
                    "-type", "f", "-links", "+1"], "disp-multilink")
    check("disp-no-multilink", multilink.stdout.strip() == "")

    def object_inodes(top: str) -> set[int]:
        found: set[int] = set()
        for dirpath, _dirnames, filenames in os.walk(os.path.join(top, ".git", "objects")):
            for name in filenames:
                try:
                    found.add(os.lstat(os.path.join(dirpath, name)).st_ino)
                except OSError:
                    pass
        return found

    shared = object_inodes(CAND) & object_inodes(DISP)
    check("inode-separation", len(shared) == 0, f"shared={len(shared)}")

    emit("=== runner on disposable with postdrift hook (fast pure test child) ===")
    runner_argv = [sys.executable, RUNNER, RUNNER_LOG,
                   "--dst", DISP, "--proof-postdrift-file", CANARY,
                   "--", PURE_TEST]
    check("runner-log-absent-before", not os.path.exists(RUNNER_LOG), RUNNER_LOG)
    runner = sh(runner_argv, "runner")
    check("runner-returncode-is-3", runner.returncode == 3, f"got={runner.returncode}")
    with open(RUNNER_LOG, encoding="utf-8") as fh:
        runner_log_text = fh.read()
    check("runner-log-child-0", "unittest_exit:0" in runner_log_text)
    check("runner-log-postguard-failed", "OUTCOME=POSTGUARD_FAILED" in runner_log_text)
    check("canary-in-disposable", os.path.isfile(os.path.join(DISP, CANARY)))

    emit("=== candidate post-proof (must be identical, canary-free) ===")
    post_status = sh(["git", "-C", CAND, "status", "--porcelain=v1", "--untracked-files=all"], "cand-post-status")
    post_diff = sh(["git", "-C", CAND, "diff", "--name-only", "HEAD"], "cand-post-diff")
    check("cand-post-status-identical",
          post_status.stdout.rstrip("\n") == pre_status.stdout.rstrip("\n"))
    check("cand-post-diff-empty", post_diff.stdout.strip() == "")
    check("canary-absent-in-candidate", not os.path.exists(os.path.join(CAND, CANARY)))

    emit("=== cleanup disposable ===")
    shutil.rmtree(DISP, ignore_errors=False)
    check("disp-removed", not os.path.exists(DISP), DISP)

    emit("=== verdict ===")
    if not FAILURES and runner.returncode == 3:
        emit("VERDICT=PASS (child 0 + postdrift -> runner exit 3, direct capture)")
        emit("DONE")
        handle.close()
        print("VERDICT=PASS runner_exit=3 candidate_unchanged", file=sys.stderr)
        return 0
    emit(f"VERDICT=FAIL failures={FAILURES}")
    emit("DONE")
    handle.close()
    print(f"VERDICT=FAIL failures={FAILURES}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
