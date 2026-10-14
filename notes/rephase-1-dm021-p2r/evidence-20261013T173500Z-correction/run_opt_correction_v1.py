#!/usr/bin/env python3
"""Cheap -O check v1 (separate from long suite timeout): single weekly positive under -O."""
import os
import subprocess
import sys
from pathlib import Path

CANDIDATE = Path("/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60")
EV = Path(__file__).resolve().parent
TIMEOUT_S = 1800


def main():
    cmd = [sys.executable, "-O", "-m", "unittest",
           "tests.test_survey_editorial_retention_v2.EditorialRetentionV2Tests.test_weekly_capture_verify_positive",
           "-v"]
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    try:
        proc = subprocess.run(cmd, cwd=CANDIDATE, capture_output=True, text=True, env=env, timeout=TIMEOUT_S)
        (EV / "run_opt_correction_v1.stdout.txt").write_bytes(proc.stdout.encode("utf-8", "replace"))
        (EV / "run_opt_correction_v1.stderr.txt").write_bytes(proc.stderr.encode("utf-8", "replace"))
        (EV / "run_opt_correction_v1.exit").write_text(f"{proc.returncode}\n")
        print(f"optimized_rc={proc.returncode}")
        return proc.returncode
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or ""
        err = exc.stderr or ""
        if isinstance(out, bytes):
            out = out.decode("utf-8", "replace")
        if isinstance(err, bytes):
            err = err.decode("utf-8", "replace")
        (EV / "run_opt_correction_v1.stdout.txt").write_bytes((out + "\n[TIMEOUT partial]\n").encode())
        (EV / "run_opt_correction_v1.stderr.txt").write_bytes((err + "\n[TIMEOUT partial]\n").encode())
        (EV / "run_opt_correction_v1.exit").write_text("124\n")
        print("optimized_rc=124 TIMEOUT")
        return 124


if __name__ == "__main__":
    sys.exit(main())
