#!/usr/bin/env python3
"""Durable P3S smoke launcher B3 — same-process wrapper (NOT a test runner).

Replaces nohup-shell launching (which lost the runner rc across the tool
shell boundary: `wait: not a child of this shell`, rc 127 for wait itself).
This wrapper spawns the runner as a direct child, holds exclusive
stdout/stderr handles, waits/reaps in the SAME parent process, and writes
the actual wrapper exit from that same process — so even an early runner
traceback (e.g. smoke-r5 os.lexists AttributeError, exit 1) is captured as
a real recorded rc, never fabricated.

Usage (root-selected smoke; worker run task uses this file):
  python3 launch_p3s_smoke_b3.py --runner <run_p3s_b3.py> --logdir <packet-dir>
    --manifest <static21.json> --candidate <path> --outdir <new-run-dir>
    [--cache-inventory <path>] [--p2v-expected18 <path>]
    [--timeout <s>] [-- <test selectors...>]
Outputs in --logdir (all exclusive x/xb, no overwrites):
  launch.cmd, launch.pid, launch.stdout, launch.stderr, launch.exit,
  launch.record.json
Env hygiene: strips all GIT_* + PYTHONPATH/PYTHONHOME for the child;
records allowlisted vars + redaction count only, never full env values.
Timeout default 7200 (smoke O1/O2 operational bound); interrupt reaps own
pgid and returns 130. Raw launch.cmd/record are written BEFORE spawn.
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


def main() -> int:
    ap = argparse.ArgumentParser(description="Durable P3S smoke launcher B3 (same-process wrapper)")
    ap.add_argument("--runner", required=True)
    ap.add_argument("--logdir", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--cache-inventory", required=True)
    ap.add_argument("--p2v-expected18", required=True)
    ap.add_argument("--timeout", type=int, default=TIMEOUT_DEFAULT)
    ap.add_argument("tests", nargs="*", help="unittest selectors passed to runner")
    args = ap.parse_args()
    runner = Path(args.runner)
    logdir = Path(args.logdir)
    timeout_s = int(args.timeout)
    if timeout_s <= 0 or timeout_s > TIMEOUT_MAX:
        return _refuse("timeout must be 1.." + str(TIMEOUT_MAX))
    if not os.path.lexists(runner) or not runner.is_file():
        return _refuse("runner missing/non-regular: " + str(runner))
    try:
        runner_raw = _require_pin(runner, "runner")
        runner_sha = hashlib.sha256(runner_raw).hexdigest()
    except RuntimeError as exc:
        return _refuse(str(exc))
    if not logdir.is_dir():
        return _refuse("logdir missing (packet dir must pre-exist): " + str(logdir))
    cmd_path = logdir / "launch.cmd"
    pid_path = logdir / "launch.pid"
    out_path = logdir / "launch.stdout"
    err_path = logdir / "launch.stderr"
    exit_path = logdir / "launch.exit"
    record_path = logdir / "launch.record.json"
    for p in (cmd_path, pid_path, out_path, err_path, exit_path, record_path):
        if os.path.lexists(p):
            return _refuse("launch output exists (not overwriting): " + str(p))
    child_cmd = [sys.executable, "-u", str(runner),
                 "--manifest", args.manifest,
                 "--candidate", args.candidate,
                 "--outdir", args.outdir,
                 "--cache-inventory", args.cache_inventory,
                 "--p2v-expected18", args.p2v_expected18,
                 "--timeout", str(timeout_s),
                 "--", *list(args.tests)]
    started = datetime.now(timezone.utc)
    record: dict = {"launcher": "launch_p3s_smoke_b3.py",
                    "launcher_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
                    if Path(__file__).is_file() else "unreadable",
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
                    "timeout_s": timeout_s}
    child_env = {k: v for k, v in os.environ.items()
                 if not k.startswith("GIT_") and k not in ("PYTHONPATH", "PYTHONHOME")}
    child_env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
                      "GIT_ALLOW_PROTOCOL": "file", "PYTHONDONTWRITEBYTECODE": "1",
                      "PYTHONPYCACHEPREFIX": "/tmp/opencode/launch-nocache-absent",
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
        except OSError:
            pass
        print("launcher pid=" + str(os.getpid()) + " child pid=" + str(proc.pid), flush=True)
        try:
            child_rc = proc.wait(timeout=timeout_s)
            record["child_rc"] = child_rc
            wrapper_rc = int(child_rc)
        except subprocess.TimeoutExpired:
            record["timed_out"] = True
            try:
                os.killpg(proc.pid, signal.SIGTERM)
                record["timeout_sigterm"] = "sent to pgid " + str(proc.pid)
            except (ProcessLookupError, OSError) as exc:
                record["timeout_sigterm"] = "failed: " + type(exc).__name__
            try:
                child_rc = proc.wait(timeout=120)
                record["child_rc_after_term"] = child_rc
                wrapper_rc = int(child_rc)
            except subprocess.SubprocessError:
                pass
            except Exception as exc:
                record["timeout_reap_term"] = "failed: " + type(exc).__name__
            if child_rc is None:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                    record["timeout_sigkill"] = "sent to pgid " + str(proc.pid)
                except (ProcessLookupError, OSError) as exc:
                    record["timeout_sigkill"] = "failed: " + type(exc).__name__
                try:
                    child_rc = proc.wait(timeout=120)
                    record["child_rc_after_kill"] = child_rc
                    wrapper_rc = int(child_rc) if child_rc is not None else 124
                except Exception as exc:
                    record["timeout_reap_kill"] = "failed: " + type(exc).__name__
                    wrapper_rc = 124
            if wrapper_rc == 40:
                wrapper_rc = 124
            record["wrapper_rc"] = wrapper_rc
    except KeyboardInterrupt as exc:
        record["interrupted"] = type(exc).__name__ + ": " + str(exc)
        if proc is not None:
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except (ProcessLookupError, OSError):
                pass
            try:
                child_rc = proc.wait(timeout=120)
            except Exception:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except (ProcessLookupError, OSError):
                    pass
                try:
                    child_rc = proc.wait(timeout=120)
                except Exception:
                    child_rc = None
        record["child_rc"] = child_rc
        wrapper_rc = 130
        record["wrapper_rc"] = wrapper_rc
    except Exception as exc:
        record["fatal"] = type(exc).__name__ + ": " + str(exc)
        wrapper_rc = 1
        record["wrapper_rc"] = wrapper_rc
    flush_errors: list[str] = []
    record["ended_utc"] = datetime.now(timezone.utc).isoformat()
    record["child_rc_final"] = child_rc
    record["wrapper_rc_final"] = wrapper_rc
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
    except OSError as exc:
        print("LAUNCH_REFUSAL: cannot record launch.exit: " + str(exc), file=sys.stderr)
        if wrapper_rc == 0:
            wrapper_rc = 6
    try:
        with open(logdir / "launch.record-done.json", "x") as f:
            json.dump(record, f, indent=1)
    except OSError as exc:
        print("LAUNCH_LIMIT: cannot record launch.record-done: " + str(exc), file=sys.stderr)
        if wrapper_rc == 0:
            wrapper_rc = 6
    print("launcher child_rc=" + str(child_rc) + " wrapper_rc=" + str(wrapper_rc))
    return wrapper_rc


if __name__ == "__main__":
    sys.exit(main())
