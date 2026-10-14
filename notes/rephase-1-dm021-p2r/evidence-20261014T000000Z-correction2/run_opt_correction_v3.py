#!/usr/bin/env python3
"""Optimized single-positive v3 — one weekly positive under `python -O`.

NEW versioned script (not an old-smoke rerun): same cache isolation as
v9 (`PYTHONPYCACHEPREFIX` proven-absent path + `PYTHONDONTWRITEBYTECODE=1`),
new exclusive outputs, pre/post pin guards (correction2c), forced-keys-only
env record. Separately bound from the long suite (own 1800 s timeout).
"""

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CANDIDATE = Path("/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60").resolve()
EV = Path(__file__).resolve().parent
EXPECTED = json.load(open(EV / "expected16-correction2c.json"))
FIXED_HEAD = "409b292756dd1277b9dfae87679934c0d2ce251c"
CACHE_PREFIX = Path("/tmp/opencode/jgas-p2r-nocache-20261014T000000Z")
TIMEOUT_S = 1800
FORCED_ENV_KEYS = ("GIT_NO_LAZY_FETCH", "GIT_OPTIONAL_LOCKS", "GIT_ALLOW_PROTOCOL",
                   "PYTHONDONTWRITEBYTECODE", "PYTHONPYCACHEPREFIX")
METHOD = ("tests.test_survey_editorial_retention_v2.EditorialRetentionV2Tests."
          "test_weekly_capture_verify_positive")

STDOUT_P = EV / "run_opt_correction_v3.stdout.txt"
STDERR_P = EV / "run_opt_correction_v3.stderr.txt"
EXIT_P = EV / "run_opt_correction_v3.exit"
META_P = EV / "run_opt_correction_v3.meta.json"


def _git(args: list[str]) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    return subprocess.run(["git", "-c", f"safe.directory={CANDIDATE}", *args],
                          cwd=CANDIDATE, capture_output=True, text=True, env=env, timeout=60)


def _pins() -> dict[str, dict]:
    out = {}
    for rel, exp in EXPECTED.items():
        f = CANDIDATE / rel
        try:
            data = f.read_bytes()
        except OSError as e:
            out[rel] = {"error": str(e)}
            continue
        out[rel] = {"sha256": hashlib.sha256(data).hexdigest(),
                    "bytes": len(data), "mode": oct(f.stat().st_mode & 0o777)}
    return out


def _guard(pins: dict, where: str) -> list[str]:
    errors = []
    for rel, exp in EXPECTED.items():
        got = pins.get(rel, {})
        if got.get("sha256") != exp["sha256"] or got.get("mode") != exp["mode"] \
                or got.get("bytes") != exp["bytes"]:
            errors.append(f"{where} pin mismatch: {rel}")
    return errors


def main() -> int:
    for p in (STDOUT_P, STDERR_P, EXIT_P, META_P):
        if p.exists():
            print(f"OPT_REFUSAL: output exists: {p.name}", file=sys.stderr)
            return 40
    if CACHE_PREFIX.exists():
        print(f"OPT_REFUSAL: prefix exists: {CACHE_PREFIX}", file=sys.stderr)
        return 40
    head = _git(["rev-parse", "HEAD"])
    if head.returncode != 0 or head.stdout.strip() != FIXED_HEAD:
        print(f"OPT_REFUSAL: HEAD not pinned 409", file=sys.stderr)
        return 40
    meta: dict = {"started_utc": datetime.now(timezone.utc).isoformat(), "argv": sys.argv,
                  "cwd": os.getcwd(), "python": sys.version, "candidate": str(CANDIDATE),
                  "method": METHOD, "timeout_s": TIMEOUT_S,
                  "env_git": {k: v for k, v in os.environ.items() if k.startswith("GIT")}}
    pre = _pins()
    errors = _guard(pre, "pre")
    if errors:
        print(f"OPT_REFUSAL: pre-guard: {errors}", file=sys.stderr)
        return 40
    cmd = [sys.executable, "-O", "-m", "unittest", METHOD, "-v"]
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
                "GIT_ALLOW_PROTOCOL": "file", "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONPYCACHEPREFIX": str(CACHE_PREFIX)})
    meta["child_cmd"] = cmd
    meta["child_cwd"] = str(CANDIDATE)
    meta["sys_executable"] = sys.executable
    meta["child_env_forced"] = {k: env.get(k) for k in FORCED_ENV_KEYS}
    meta["child_env_other"] = f"redacted ({len(env) - len(FORCED_ENV_KEYS)} additional inherited keys withheld)"
    with open(META_P, "x") as f:
        json.dump(meta, f, indent=1)
    try:
        proc = subprocess.run(cmd, cwd=CANDIDATE, capture_output=True, text=True,
                              env=env, timeout=TIMEOUT_S)
        with open(STDOUT_P, "xb") as f:
            f.write(proc.stdout.encode("utf-8", "replace"))
        with open(STDERR_P, "xb") as f:
            f.write(proc.stderr.encode("utf-8", "replace"))
        with open(EXIT_P, "x") as f:
            f.write(f"{proc.returncode}\n")
        rc = proc.returncode
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or ""
        err = exc.stderr or ""
        if isinstance(out, bytes):
            out = out.decode("utf-8", "replace")
        if isinstance(err, bytes):
            err = err.decode("utf-8", "replace")
        with open(STDOUT_P, "xb") as f:
            f.write((out + "\n[TIMEOUT partial]\n").encode())
        with open(STDERR_P, "xb") as f:
            f.write((err + "\n[TIMEOUT partial]\n").encode())
        with open(EXIT_P, "x") as f:
            f.write("124\n")
        print("optimized_rc=124 TIMEOUT")
        return 124
    post = _pins()
    post_errors = _guard(post, "post")
    if post_errors:
        print(f"OPT_FAILED post-guard: {post_errors}", file=sys.stderr)
        return 3
    print(f"optimized_rc={rc}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
