#!/usr/bin/env python3
"""Bounded NONPUBLISHING diagnosis: profile low.require_research_operation_ready.

Read-only. No writer/prepare/adopt, no canonical artifacts, no monkeypatch.
All artifacts go to --out packet dir only. Source guard before shadow import.
Same-process /proc/self/io rchar/read_bytes + resource cpu + wall before/after.
On SIGTERM/SIGALRM flushes cProfile stats + partial raw (no source edits).
"""
import argparse
import hashlib
import json
import os
import resource
import signal
import sys
import time
from pathlib import Path

EXPECTED_HEAD = "ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56"
EXPECTED_LOW_SHA = "7f5fc9e0d79729d98345f0b0352d5070c76e93f92f2c14148e22c9f38a8f4c0f"
EXPECTED_LOW_BYTES = 240969

profiler = None
out_dir = None
label = None
start_wall = None
start_mono = None
start_rusage = None
start_io = None
flushed = False


def read_proc_self_io():
    try:
        txt = Path("/proc/self/io").read_text()
    except OSError as exc:
        return {"error": str(exc)}
    d = {}
    for line in txt.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip()
            try:
                d[k] = int(v)
            except ValueError:
                d[k] = v
    return {"rchar": d.get("rchar"), "read_bytes": d.get("read_bytes"), "raw": d}


def snapshot_cpu():
    ru = resource.getrusage(resource.RUSAGE_SELF)
    return {"utime": ru.ru_utime, "stime": ru.ru_stime,
            "maxrss_kb": ru.ru_maxrss, "minflt": ru.ru_minflt, "majflt": ru.ru_majflt,
            "inblock": ru.ru_inblock, "oublock": ru.ru_oublock}


def flush_stats(reason):
    global flushed
    if flushed:
        return
    flushed = True
    try:
        if profiler is not None and out_dir is not None and label is not None:
            import pstats
            p = out_dir / f"{label}.pstats.txt"
            try:
                ps = pstats.Stats(profiler, stream=open(os.devnull, "w"))
                # write sorted by cumulative to file
                with open(p, "w") as f:
                    st = pstats.Stats(profiler, stream=f)
                    st.strip_dirs().sort_stats("cumulative").print_stats(80)
            except Exception as exc:
                (out_dir / f"{label}.flush-error.txt").write_text(f"pstats flush failed {reason}: {exc}\n")
            try:
                profiler.dump_stats(str(out_dir / f"{label}.pstats.bin"))
            except Exception as exc:
                (out_dir / f"{label}.dump-error.txt").write_text(f"dump_stats failed: {exc}\n")
            try:
                import faulthandler
                with open(out_dir / f"{label}.traceback-{reason}.txt", "w") as f:
                    faulthandler.dump_traceback(file=f)
            except Exception:
                pass
    except Exception:
        pass


def on_term(signum, frame):
    flush_stats(f"signal-{signum}")
    # record partial raw then exit 124-like (timeout)
    try:
        end_wall = time.time()
        end_mono = time.monotonic()
        partial = {
            "label": label,
            "outcome": f"timeout-signal-{signum}",
            "pid": os.getpid(),
            "start_wall": start_wall,
            "end_wall": end_wall,
            "wall_delta_s": end_mono - start_mono if start_mono else None,
            "start_io": start_io,
            "end_io": read_proc_self_io(),
            "start_cpu": {"utime": start_rusage.ru_utime, "stime": start_rusage.ru_stime} if start_rusage else None,
            "end_cpu": snapshot_cpu(),
        }
        (out_dir / f"{label}.partial-signal.json").write_text(json.dumps(partial, indent=2))
    except Exception:
        pass
    sys.stderr.write(f"diagnostic {label} received signal {signum}, flushed stats\n")
    sys.stderr.flush()
    os._exit(124)


def main():
    global profiler, out_dir, label, start_wall, start_mono, start_rusage, start_io
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--state", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--label", required=True)
    args = ap.parse_args()
    repo_root = Path(args.repo_root).resolve()
    state_path = Path(args.state)
    if not state_path.is_absolute():
        state_path = (repo_root / str(state_path)).resolve()
    else:
        state_path = state_path.resolve()
    out_dir = Path(args.out).resolve()
    label = args.label
    out_dir.mkdir(parents=True, exist_ok=True)

    argv_rec = sys.argv
    pid = os.getpid()
    # ---- source guard BEFORE shadow import ----
    guard = {"repo_root": str(repo_root), "state": str(state_path), "pid": pid, "argv": argv_rec}
    try:
        gitdir = repo_root / ".git"
        assert gitdir.is_dir() and not gitdir.is_symlink(), "shadow .git must be dir"
        assert not (repo_root / ".git" / "commondir").exists(), "commondir must be absent"
        assert not (repo_root / ".git" / "objects" / "info" / "alternates").exists(), "alternates must be absent"
        head = (repo_root / ".git" / "HEAD").read_text().strip()
        # resolve ref
        if head.startswith("ref:"):
            ref = head.split(":", 1)[1].strip()
            actual_head = (repo_root / ".git" / ref).read_text().strip()
        else:
            actual_head = head
        guard["head"] = actual_head
        assert actual_head == EXPECTED_HEAD, f"HEAD mismatch {actual_head}"
        low_path = repo_root / "scripts" / "survey_research_authority_v2.py"
        raw = low_path.read_bytes()
        guard["low_sha256"] = hashlib.sha256(raw).hexdigest()
        guard["low_bytes"] = len(raw)
        assert guard["low_sha256"] == EXPECTED_LOW_SHA, "LOW bytes differ"
        assert guard["low_bytes"] == EXPECTED_LOW_BYTES, "LOW size differ"
        assert state_path.is_file(), "state file missing"
        guard["guard"] = "PASS"
    except Exception as exc:
        guard["guard"] = f"FAIL: {exc}"
        (out_dir / f"{label}.guard.json").write_text(json.dumps(guard, indent=2))
        sys.stderr.write(f"source guard failed: {exc}\n")
        return 2
    (out_dir / f"{label}.guard.json").write_text(json.dumps(guard, indent=2))

    # ---- shadow import AFTER guard ----
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    # ensure no bytecode writes (env already sets, double-check)
    sys.dont_write_bytecode = True
    from scripts import survey_research_authority_v2 as low  # noqa: E402

    signal.signal(signal.SIGTERM, on_term)
    signal.signal(signal.SIGALRM, on_term)
    try:
        signal.alarm(85)
    except Exception:
        pass

    import cProfile
    profiler = cProfile.Profile()
    start_wall = time.time()
    start_mono = time.monotonic()
    start_rusage = resource.getrusage(resource.RUSAGE_SELF)
    start_io = read_proc_self_io()
    (out_dir / f"{label}.start.json").write_text(json.dumps({
        "pid": pid, "argv": argv_rec,
        "env": {"PYTHONPATH": os.environ.get("PYTHONPATH"), "PYTHONDONTWRITEBYTECODE": os.environ.get("PYTHONDONTWRITEBYTECODE"),
                "GIT_NO_LAZY_FETCH": os.environ.get("GIT_NO_LAZY_FETCH"), "HOME": os.environ.get("HOME"), "PWD": os.environ.get("PWD")},
        "start_wall": start_wall, "start_io": start_io, "start_cpu": snapshot_cpu(),
        "repo_root": str(repo_root), "state": str(state_path),
    }, indent=2))

    exc_text = None
    result = None
    try:
        profiler.enable()
        result = low.require_research_operation_ready(repo_root, state_path)
        profiler.disable()
        outcome = "returned"
        code = 0
    except Exception as exc:
        try:
            profiler.disable()
        except Exception:
            pass
        import traceback
        exc_text = f"{type(exc).__name__}: {exc}\n" + traceback.format_exc()
        outcome = "raised"
        code = 3
    finally:
        try:
            signal.alarm(0)
        except Exception:
            pass
    end_wall = time.time()
    end_mono = time.monotonic()
    end_io = read_proc_self_io()
    end_cpu = snapshot_cpu()
    flush_stats("normal-finish")
    raw_rec = {
        "label": label,
        "pid": pid,
        "argv": argv_rec,
        "outcome": outcome,
        "result_keys": sorted(result.keys()) if isinstance(result, dict) else None,
        "exception": exc_text,
        "exit": code,
        "start_wall": start_wall,
        "end_wall": end_wall,
        "wall_delta_s": end_mono - start_mono,
        "start_io": start_io,
        "end_io": end_io,
        "start_cpu_utime": start_rusage.ru_utime,
        "start_cpu_stime": start_rusage.ru_stime,
        "end_cpu": end_cpu,
    }
    (out_dir / f"{label}.raw.json").write_text(json.dumps(raw_rec, indent=2))
    if exc_text:
        (out_dir / f"{label}.stderr.txt").write_text(exc_text)
    else:
        (out_dir / f"{label}.stdout.txt").write_text(f"READY returned keys={raw_rec['result_keys']}\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
