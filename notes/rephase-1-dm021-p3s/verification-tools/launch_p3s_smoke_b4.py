#!/usr/bin/env python3
"""Durable P3S smoke launcher B4 — same-process wrapper (NOT a test runner).

B4 repairs root-read defects in B3 (B3 preserved); B4 is the only launcher
approved for the scoped smoke. Runner/gen/proof stay B3 (accepted).
- Timeout always returns 124 once the launcher wait expires, even if the
  child later reports 0 (B3 could adopt the post-signal 0).
- Launcher wait allowance is runner timeout + 600 s minimum (separate
  --launcher-timeout, floor-enforced), so the runner always has time to
  finish its own timeout handling + finally-POST + finalization.
- Outer timeout/interrupt signals the RUNNER pgid with SIGINT first, so
  the runner executes its finally-POST and its own test-session cleanup.
  Runner and tests run in SEPARATE sessions (runner uses
  start_new_session=True for the test child): SIGTERM-ing the runner
  alone would orphan the tests. SIGKILL is fallback after a grace wait;
  any nested test session that may have escaped is explicitly recorded —
  never a false reaped-all claim.
- Generic exceptions after spawn also reap the child (B3 left it running).
- Pre-spawn refusal covers ALL outputs incl. launch.record-done.json.
- Per-logdir cache prefix /tmp/opencode/<logdir-name>-launcher-cache-absent
  refused if present, forced into the child env only after the absent
  check (no shared constant).
- Child-pid append failure is recorded and propagates (no silent pass)
  while reap + finalization still run.
- wrapper_rc_final is refreshed after stream handling, before
  record-done, so the persisted record matches the actual exit file.

Usage (root-selected smoke; worker run task uses this file):
  python3 launch_p3s_smoke_b4.py --runner <run_p3s_b3.py> --logdir <packet-dir>
    --manifest <static21.json> --candidate <path> --outdir <new-run-dir>
    [--cache-inventory <path>] [--p2v-expected18 <path>]
    [--timeout <s>] [--launcher-timeout <s>] [-- <test selectors...>]
Outputs in --logdir (all exclusive x/xb, no overwrites):
  launch.cmd, launch.pid, launch.stdout, launch.stderr, launch.exit,
  launch.record.json, launch.record-done.json
Env hygiene: strips all GIT_* + PYTHONPATH/PYTHONHOME for the child;
records allowlisted vars + redaction count only, never full env values.
Timeout default 7200 (smoke O1/O2 operational bound); launcher wait is
timeout+600 minimum; interrupt returns 130. Raw launch.cmd/record are
written BEFORE spawn.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import stat as _stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TIMEOUT_DEFAULT = 7200
TIMEOUT_MAX = 18000
LAUNCHER_GRACE_EXTRA = 600
LAUNCHER_SIGINT_GRACE = 300


def _refuse(msg: str) -> int:
    print("LAUNCH_REFUSAL: " + msg, file=sys.stderr)
    return 40


def _require_pin(path: Path, label: str) -> bytes:
    try:
        st = os.lstat(path)
    except OSError as exc:
        raise RuntimeError(label + " lstat failed: " + str(path) + ": " + str(exc))
    if _stat.S_ISLNK(st.st_mode):
        raise RuntimeError(label + " is symlink (alias refusal): " + str(path))
    if not _stat.S_ISREG(st.st_mode):
        raise RuntimeError(label + " not regular: " + str(path))
    if st.st_nlink != 1:
        raise RuntimeError(label + " nlink!=1: " + str(path))
    return path.read_bytes()


def _escalate_runner(proc: subprocess.Popen, record: dict, tag: str) -> int | None:
    """SIGINT the runner pgid first so the runner executes its finally-POST
    and its own test-session cleanup, then SIGKILL fallback after grace.
    Runner and tests run in SEPARATE sessions (runner spawns tests with
    start_new_session=True, an unknown pgid): signals here reach ONLY the
    runner pgid. A SIGTERM/SIGKILL of the runner alone would orphan the
    tests, so SIGINT-first is mandatory. Any nested test session that may
    have escaped is explicitly recorded — never a false reaped-all claim.
    Returns the runner rc, or None if unreaped."""
    try:
        os.killpg(proc.pid, signal.SIGINT)
        record[tag + "_sigint"] = "sent to pgid " + str(proc.pid)
    except ProcessLookupError:
        record[tag + "_sigint"] = "already-exited"
    except OSError as exc:
        record[tag + "_sigint"] = "failed: " + type(exc).__name__ + ": " + str(exc)
    try:
        rc = proc.wait(timeout=LAUNCHER_SIGINT_GRACE)
        record[tag + "_reap_sigint"] = "rc=" + str(rc)
        return rc
    except subprocess.TimeoutExpired:
        record[tag + "_sigint_grace_expired"] = (
            "runner pgid alive after " + str(LAUNCHER_SIGINT_GRACE) + "s; "
            "nested test session (separate pgid, id unknown to launcher) may "
            "still be running — NOT claimed reaped")
    except Exception as exc:
        record[tag + "_reap_sigint"] = "failed: " + type(exc).__name__ + ": " + str(exc)
    try:
        os.killpg(proc.pid, signal.SIGKILL)
        record[tag + "_sigkill"] = "sent to pgid " + str(proc.pid)
    except ProcessLookupError:
        record[tag + "_sigkill"] = "already-exited"
    except OSError as exc:
        record[tag + "_sigkill"] = "failed: " + type(exc).__name__ + ": " + str(exc)
    try:
        rc = proc.wait(timeout=120)
        record[tag + "_reap_kill"] = "rc=" + str(rc)
        return rc
    except Exception as exc:
        record[tag + "_reap_kill"] = "failed: " + type(exc).__name__ + ": " + str(exc)
        record[tag + "_escaped_note"] = (
            "runner and/or nested test sessions may still be alive; only the "
            "runner pgid was signaled — never a false reaped-all")
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Durable P3S smoke launcher B4 (same-process wrapper)")
    ap.add_argument("--runner", required=True)
    ap.add_argument("--logdir", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--cache-inventory", required=True)
    ap.add_argument("--p2v-expected18", required=True)
    ap.add_argument("--timeout", type=int, default=TIMEOUT_DEFAULT)
    ap.add_argument("--launcher-timeout", type=int, default=None,
                    help="launcher wait allowance; defaults to --timeout + 600 and "
                         "must be at least --timeout + 600 so the runner can finish "
                         "its own timeout handling + finally-POST + finalization")
    ap.add_argument("tests", nargs="*", help="unittest selectors passed to runner")
    args = ap.parse_args()
    try:
        runner = Path(args.runner).resolve()
        logdir = Path(args.logdir).resolve()
        manifest_abs = str(Path(args.manifest).resolve())
        candidate_abs = str(Path(args.candidate).resolve())
        outdir_abs = str(Path(args.outdir).resolve())
        cache_abs = str(Path(args.cache_inventory).resolve())
        p2v_abs = str(Path(args.p2v_expected18).resolve())
    except OSError as exc:
        return _refuse("arg path unresolvable: " + type(exc).__name__ + ": " + str(exc))
    timeout_s = int(args.timeout)
    if timeout_s <= 0 or timeout_s > TIMEOUT_MAX:
        return _refuse("timeout must be 1.." + str(TIMEOUT_MAX))
    if args.launcher_timeout is None:
        launcher_wait_s = timeout_s + LAUNCHER_GRACE_EXTRA
    else:
        launcher_wait_s = int(args.launcher_timeout)
        if launcher_wait_s < timeout_s + LAUNCHER_GRACE_EXTRA:
            return _refuse("launcher-timeout must be at least timeout + " +
                           str(LAUNCHER_GRACE_EXTRA) + " (got " + str(launcher_wait_s) +
                           " for timeout " + str(timeout_s) + ")")
    if not os.path.lexists(runner) or not runner.is_file():
        return _refuse("runner missing/non-regular: " + str(runner))
    try:
        runner_raw = _require_pin(runner, "runner")
        runner_sha = hashlib.sha256(runner_raw).hexdigest()
    except RuntimeError as exc:
        return _refuse(str(exc))
    if not logdir.is_dir():
        return _refuse("logdir missing (packet dir must pre-exist): " + str(logdir))
    cache_prefix = Path("/tmp/opencode") / (logdir.name + "-launcher-cache-absent")
    if os.path.lexists(cache_prefix):
        return _refuse("launcher cache prefix exists (must stay absent, never mkdir'd): " + str(cache_prefix))
    cmd_path = logdir / "launch.cmd"
    pid_path = logdir / "launch.pid"
    out_path = logdir / "launch.stdout"
    err_path = logdir / "launch.stderr"
    exit_path = logdir / "launch.exit"
    record_path = logdir / "launch.record.json"
    record_done_path = logdir / "launch.record-done.json"
    for p in (cmd_path, pid_path, out_path, err_path, exit_path, record_path, record_done_path):
        if os.path.lexists(p):
            return _refuse("launch output exists (not overwriting): " + str(p))
    child_cmd = [sys.executable, "-u", str(runner),
                 "--manifest", manifest_abs,
                 "--candidate", candidate_abs,
                 "--outdir", outdir_abs,
                 "--cache-inventory", cache_abs,
                 "--p2v-expected18", p2v_abs,
                 "--timeout", str(timeout_s),
                 "--", *list(args.tests)]
    started = datetime.now(timezone.utc)
    try:
        launcher_self_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    except OSError:
        launcher_self_sha = "unreadable"
    record: dict = {"launcher": "launch_p3s_smoke_b4.py",
                    "launcher_sha256": launcher_self_sha,
                    "pid": os.getpid(),
                    "started_utc": started.isoformat(),
                    "argv": sys.argv,
                    "cwd": os.getcwd(),
                    "python": sys.version,
                    "sys_executable": sys.executable,
                    "runner": str(runner),
                    "runner_sha256": runner_sha,
                    "runner_bytes": len(runner_raw),
                    "child_cmd": child_cmd,
                    "timeout_s": timeout_s,
                    "launcher_wait_s": launcher_wait_s,
                    "launcher_cache_prefix": str(cache_prefix)}
    child_env = {k: v for k, v in os.environ.items()
                 if not k.startswith("GIT_") and k not in ("PYTHONPATH", "PYTHONHOME")}
    child_env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
                      "GIT_ALLOW_PROTOCOL": "file", "PYTHONDONTWRITEBYTECODE": "1",
                      "PYTHONPYCACHEPREFIX": str(cache_prefix),
                      "TMPDIR": "/tmp/opencode"})
    record["child_env_forced"] = {k: child_env[k] for k in
                                  ("GIT_NO_LAZY_FETCH", "GIT_OPTIONAL_LOCKS",
                                   "GIT_ALLOW_PROTOCOL", "PYTHONDONTWRITEBYTECODE",
                                   "PYTHONPYCACHEPREFIX", "TMPDIR")}
    record["child_env_other_withheld"] = str(len(child_env) - 6) + " inherited keys withheld, no values persisted"
    try:
        with open(cmd_path, "x") as f:
            f.write(" ".join(child_cmd) + "\n")
        with open(pid_path, "x") as f:
            f.write(str(os.getpid()) + "\n")
        with open(record_path, "x") as f:
            json.dump(record, f, indent=1)
    except OSError as exc:
        return _refuse("cannot reserve launch raw (before spawn): " + type(exc).__name__ + ": " + str(exc))
    out_fh = None
    err_fh = None
    try:
        out_fh = open(out_path, "xb")
        err_fh = open(err_path, "xb")
    except OSError as exc:
        return _refuse("cannot reserve launch stdout/stderr: " + type(exc).__name__ + ": " + str(exc))
    proc: subprocess.Popen | None = None
    child_rc: int | None = None
    wrapper_rc = 40
    try:
        proc = subprocess.Popen(child_cmd, stdout=out_fh, stderr=err_fh,
                                env=child_env, start_new_session=True)
        try:
            with open(pid_path, "a") as f:
                f.write("child=" + str(proc.pid) + " pgid=" + str(proc.pid) + "\n")
        except OSError as exc:
            record["child_pid_write_error"] = type(exc).__name__ + ": " + str(exc)
        print("launcher pid=" + str(os.getpid()) + " child pid=" + str(proc.pid), flush=True)
        try:
            child_rc = proc.wait(timeout=launcher_wait_s)
            record["child_rc"] = child_rc
            wrapper_rc = int(child_rc)
        except subprocess.TimeoutExpired:
            record["timed_out"] = True
            record["timed_out_note"] = (
                "launcher wait (" + str(launcher_wait_s) + "s) expired; runner "
                "timeout was " + str(timeout_s) + "s — signaling runner pgid "
                "with SIGINT first so it finalizes")
            child_rc = _escalate_runner(proc, record, "timeout")
            record["child_rc_after_escalation"] = child_rc
            wrapper_rc = 124
            record["wrapper_rc"] = wrapper_rc
    except KeyboardInterrupt as exc:
        record["interrupted"] = type(exc).__name__ + ": " + str(exc)
        if proc is not None:
            child_rc = _escalate_runner(proc, record, "interrupt")
            record["child_rc_after_escalation"] = child_rc
        else:
            record["child_rc_after_escalation"] = None
        record["child_rc"] = child_rc
        wrapper_rc = 130
        record["wrapper_rc"] = wrapper_rc
    except Exception as exc:
        record["fatal"] = type(exc).__name__ + ": " + str(exc)
        if proc is not None and child_rc is None:
            try:
                still_alive = proc.poll() is None
            except Exception:
                still_alive = True
            if still_alive:
                record["fatal_reap"] = "reaping own child after exception"
                reaped = _escalate_runner(proc, record, "fatal")
                if child_rc is None:
                    child_rc = reaped
        wrapper_rc = 1
        record["wrapper_rc"] = wrapper_rc
    flush_errors: list[str] = []
    record["ended_utc"] = datetime.now(timezone.utc).isoformat()
    record["child_rc_final"] = child_rc
    if record.get("child_pid_write_error") and wrapper_rc == 0:
        record["pid_write_propagated"] = "child-pid append failed; forcing 5 (reap+finalize still ran)"
        wrapper_rc = 5
    try:
        if out_fh is not None and not out_fh.closed:
            out_fh.write(("\n[LAUNCHER child_rc=" + str(child_rc) +
                           " wrapper_rc=" + str(wrapper_rc) + "]\n").encode())
            out_fh.flush()
    except (OSError, ValueError) as exc:
        record["trailer_write_error"] = type(exc).__name__ + ": " + str(exc)
        if wrapper_rc == 0:
            wrapper_rc = 5
    for fh, name in ((out_fh, "stdout"), (err_fh, "stderr")):
        if fh is not None and not fh.closed:
            try:
                fh.flush()
            except (OSError, ValueError) as exc:
                flush_errors.append(name + " flush: " + type(exc).__name__)
            try:
                fh.close()
            except (OSError, ValueError) as exc:
                flush_errors.append(name + " close: " + type(exc).__name__)
    if flush_errors:
        record["flush_errors"] = flush_errors
        if wrapper_rc == 0:
            wrapper_rc = 5
    try:
        with open(exit_path, "x") as f:
            f.write(str(wrapper_rc) + "\n")
            f.flush()
    except OSError as exc:
        print("LAUNCH_REFUSAL: cannot record launch.exit: " + str(exc), file=sys.stderr)
        if wrapper_rc == 0:
            wrapper_rc = 6
    record["wrapper_rc_final"] = wrapper_rc
    record["actual_exit_captured"] = str(wrapper_rc)
    try:
        with open(record_done_path, "x") as f:
            json.dump(record, f, indent=1)
            f.flush()
    except OSError as exc:
        print("LAUNCH_LIMIT: cannot record launch.record-done: " + str(exc), file=sys.stderr)
        if wrapper_rc == 0:
            wrapper_rc = 6
    print("launcher child_rc=" + str(child_rc) + " wrapper_rc=" + str(wrapper_rc))
    return wrapper_rc


if __name__ == "__main__":
    sys.exit(main())
