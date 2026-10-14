#!/usr/bin/env python3
"""Guarded correction runner v1 (R6): focused P2R suite only, no cleanup.

Preselected expected16 manifest (expected16-pinned.json) verified pre-run.
Records actual HEAD/tree/full raw status+index+cache pre and finally-post,
captures exact runtime/deps/argv/env/stdout/stderr/child+wrapper rc directly
and exclusively, propagates any failure, preserves timeout partial output,
no cleanup, no filtered status, no trailing -O inside long timeout.
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CANDIDATE = Path("/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60")
EV = Path(__file__).resolve().parent
EXPECTED = json.load(open(EV / "expected16-pinned.json"))
FIXED_HEAD = "409b292756dd1277b9dfae87679934c0d2ce251c"
TIMEOUT_S = 7200

STDOUT_P = EV / "run_p2r_correction_v1.stdout.txt"
STDERR_P = EV / "run_p2r_correction_v1.stderr.txt"
EXIT_P = EV / "run_p2r_correction_v1.exit"
PRE_P = EV / "run_p2r_correction_v1.pre.json"
POST_P = EV / "run_p2r_correction_v1.post.json"
META_P = EV / "run_p2r_correction_v1.meta.json"


def _git(args, cwd):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    p = subprocess.run(["git", "-c", "safe.directory=*", *args], cwd=cwd,
                       capture_output=True, text=True, env=env, timeout=60)
    return p


def _observe(label):
    head = _git(["rev-parse", "HEAD"], CANDIDATE)
    tree = _git(["rev-parse", "HEAD^{tree}"], CANDIDATE)
    status = _git(["status", "--porcelain=v1", "--untracked-files=all"], CANDIDATE)
    index = _git(["diff", "--cached", "--name-only"], CANDIDATE)
    diff_wt = _git(["diff", "--name-only"], CANDIDATE)
    caches = []
    for base in ("scripts", "tests", "schemas"):
        d = CANDIDATE / base
        for p in sorted(d.glob("__pycache__/*")):
            caches.append(str(p.relative_to(CANDIDATE)))
        for p in sorted(d.glob("*.pyc")):
            caches.append(str(p.relative_to(CANDIDATE)))
    files = {}
    for rel in sorted(EXPECTED):
        f = CANDIDATE / rel
        try:
            data = f.read_bytes()
        except OSError as e:
            files[rel] = {"error": str(e)}
            continue
        import hashlib
        files[rel] = {"sha256": hashlib.sha256(data).hexdigest(),
                      "bytes": len(data), "mode": oct(f.stat().st_mode & 0o777)}
    return {"label": label, "head": head.stdout.strip(), "head_rc": head.returncode,
            "tree": tree.stdout.strip(), "tree_rc": tree.returncode,
            "status": status.stdout, "status_rc": status.returncode,
            "index": index.stdout, "index_rc": index.returncode,
            "diff_wt": diff_wt.stdout, "diff_wt_rc": diff_wt.returncode,
            "caches": caches, "files": files}


def main():
    meta = {"started_utc": datetime.now(timezone.utc).isoformat(),
            "argv": sys.argv, "python": sys.version,
            "candidate": str(CANDIDATE), "timeout_s": TIMEOUT_S,
            "env_git": {k: v for k, v in os.environ.items() if k.startswith("GIT")}}
    try:
        import unittest  # noqa
        meta["unittest"] = "available"
    except Exception as e:
        meta["unittest"] = str(e)
    try:
        pip = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True, timeout=60)
        meta["pip_freeze_rc"] = pip.returncode
        meta["pip_freeze"] = pip.stdout[:6000]
    except Exception as e:
        meta["pip_freeze_error"] = str(e)
    json.dump(meta, open(META_P, "w"), indent=1)
    pre = _observe("pre")
    json.dump(pre, open(PRE_P, "w"), indent=1)
    errors = []
    if pre["head"] != FIXED_HEAD or pre["head_rc"] != 0:
        errors.append(f"HEAD mismatch: {pre['head']!r} rc={pre['head_rc']}")
    for rel, exp in EXPECTED.items():
        got = pre["files"].get(rel, {})
        if got.get("sha256") != exp["sha256"] or got.get("mode") != exp["mode"] or got.get("bytes") != exp["bytes"]:
            errors.append(f"expected16 mismatch pre: {rel}: got={got} exp={exp}")
    if errors:
        msg = "PRE-GUARD FAILED:\n" + "\n".join(errors) + "\n"
        STDOUT_P.write_bytes(msg.encode())
        STDERR_P.write_bytes(msg.encode())
        EXIT_P.write_text("2\n")
        print(msg, file=sys.stderr)
        return 2
    # Run focused suite only (no old27Gate), direct capture, no cleanup.
    cmd = [sys.executable, "-m", "unittest", "tests.test_survey_editorial_retention_v2", "-v"]
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file",
                "PYTHONDONTWRITEBYTECODE": "0"})
    child_rc = None
    timed_out = False
    try:
        proc = subprocess.run(cmd, cwd=CANDIDATE, capture_output=True, text=True, env=env, timeout=TIMEOUT_S)
        STDOUT_P.write_bytes(proc.stdout.encode("utf-8", "replace"))
        STDERR_P.write_bytes(proc.stderr.encode("utf-8", "replace"))
        child_rc = proc.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        out = (exc.stdout or b"").decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        err = (exc.stderr or b"").decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        STDOUT_P.write_bytes((out + f"\n[TIMEOUT after {TIMEOUT_S}s, partial preserved]\n").encode())
        STDERR_P.write_bytes((err + f"\n[TIMEOUT after {TIMEOUT_S}s, partial preserved]\n").encode())
        child_rc = 124
    post = _observe("finally-post")
    json.dump(post, open(POST_P, "w"), indent=1)
    # Post guards: HEAD must be unchanged, expected16 hashes must still match.
    # Status/caches recorded (no cleanup); deltas reported, not asserted away.
    post_errors = []
    if post["head"] != FIXED_HEAD:
        post_errors.append(f"HEAD moved during run: {post['head']!r}")
    for rel, exp in EXPECTED.items():
        got = post["files"].get(rel, {})
        if got.get("sha256") != exp["sha256"]:
            post_errors.append(f"expected16 changed during run: {rel}")
    wrapper_rc = 0
    summary = (f"child_rc={child_rc} timed_out={timed_out} "
               f"post_errors={post_errors}\n")
    if timed_out:
        wrapper_rc = 124
    elif child_rc != 0:
        wrapper_rc = child_rc if child_rc is not None else 1
    elif post_errors:
        wrapper_rc = 3
    EXIT_P.write_text(f"{wrapper_rc}\n")
    with open(STDOUT_P, "ab") as f:
        f.write(f"\n[WRAPPER child_rc={child_rc} wrapper_rc={wrapper_rc} timed_out={timed_out}]\n".encode())
        if post_errors:
            f.write(("POST-GUARD: " + "; ".join(post_errors) + "\n").encode())
    print(summary)
    print(f"wrapper_rc={wrapper_rc}")
    return wrapper_rc


if __name__ == "__main__":
    sys.exit(main())
