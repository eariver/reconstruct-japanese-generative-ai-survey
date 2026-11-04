#!/usr/bin/env python3
"""Fresh safe W34 409 verification harness (REAL normal run, no bypass).

Calls normal scripts.run_evidence_v2_interactive.run via existing strict
facades only. No monkeypatch, no preloaded operator context, no subset,
no source projection. Same-process module load path/hash, /proc/self/io
before/after, rusage/time, before/after source+State pins.
"""
import argparse
import datetime
import hashlib
import json
import os
import resource
import sys
import time
import traceback
from pathlib import Path


def sha_file(p: Path):
    d = p.read_bytes()
    return hashlib.sha256(d).hexdigest(), len(d)


def read_proc_self_io():
    try:
        return Path("/proc/self/io").read_text()
    except Exception as e:
        return f"UNAVAILABLE: {e}"


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--state", required=True)
    ap.add_argument("--input", required=True)
    ap.add_argument("--supplement", required=True)
    ap.add_argument("--out-json", required=True)
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    state_path = Path(args.state)
    input_path = Path(args.input)
    supp_path = Path(args.supplement)
    out_json = Path(args.out_json)
    if not state_path.is_absolute():
        state_path = repo_root / state_path
    if not input_path.is_absolute():
        input_path = repo_root / input_path
    if not supp_path.is_absolute():
        supp_path = repo_root / supp_path
    state_path = state_path.resolve()
    input_path = input_path.resolve()
    supp_path = supp_path.resolve()

    pid = os.getpid()
    argv = sys.argv
    cwd = os.getcwd()
    env = dict(os.environ)
    start_utc = utc_now()
    start_wall = time.time()
    start_mono = time.monotonic()
    rusage_before = resource.getrusage(resource.RUSAGE_SELF)
    io_before = read_proc_self_io()

    # Before pins: 4 runtime + W34 inputs + State/Profile/checkpoints
    def pin_file(p: Path):
        try:
            h, n = sha_file(p)
            st = p.stat()
            return {"path": str(p), "sha256": h, "bytes": n,
                    "mode": oct(st.st_mode & 0o777), "exists": True}
        except FileNotFoundError:
            return {"path": str(p), "exists": False}

    runtime_rels = [
        "scripts/survey_evidence_v2.py",
        "scripts/run_evidence_v2_interactive.py",
        "scripts/survey_research_authority_v2.py",
        "tests/test_evidence_scaling_v2.py",
    ]
    state_rels = [
        "sources/2026-W34/production-state.json",
        "sources/2026-W34/production-profile.json",
        "sources/2026-W34/orchestration/v2/checkpoints/DISCOVERY_COLLECTED.json",
        "sources/2026-W34/orchestration/v2/checkpoints/ISSUE_INITIALIZED.json",
        "sources/SP-efficient-llm-2026/production-state.json",
        "sources/SP-efficient-llm-2026/production-profile.json",
    ]
    input_rels = [
        "sources/2026-W34/discovery/discovery-v2.jsonl",
        "sources/2026-W34/screening/input/event-discovery-v2.jsonl",
        "sources/2026-W34/screening/v2/accepted/e193ad0507895568e369437833b87d2610d68ef50f0c6419b092f5711e26bbea/screening-accepted.json",
        "sources/2026-W34/evidence/proposed-input/interactive-evidence.json",
        "sources/2026-W34/external/evidence-supplement/evidence-authority-supplement-r2-fresh-basis.json",
    ]
    before_runtime = [pin_file(repo_root / r) for r in runtime_rels]
    before_state = [pin_file(repo_root / r) for r in state_rels]
    before_inputs = [pin_file(repo_root / r) for r in input_rels]
    # Full intended inventory: baseline manifest 770 + newtest (derive, no guess)
    # Load baseline manifest for reference (old pins for 767, new for 3)
    before_full = {}
    try:
        manifest_path = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-profile-support-implementation/source-packaging/final-20261031T202327Z/complete-profile-support-manifest.json")
        manifest = json.loads(manifest_path.read_bytes())
        files = manifest.get("files", {})
        for rel in files.keys():
            q = repo_root / rel
            if q.is_file():
                h, n = sha_file(q)
                before_full[rel] = {"sha256": h, "bytes": n, "mode": oct(q.stat().st_mode & 0o777)}
            else:
                before_full[rel] = {"exists": False}
        # new test (not in baseline)
        q = repo_root / "tests/test_evidence_scaling_v2.py"
        h, n = sha_file(q)
        before_full["tests/test_evidence_scaling_v2.py"] = {"sha256": h, "bytes": n, "mode": oct(q.stat().st_mode & 0o777)}
    except Exception as e:
        before_full = {"error": str(e)}

    # Same-process module load path/hash matching committed source
    # Ensure NEW clone is first on sys.path
    sys.path.insert(0, str(repo_root))
    import scripts.survey_evidence_v2 as ev_mod
    import scripts.run_evidence_v2_interactive as run_mod
    import scripts.survey_research_authority_v2 as low_mod
    modules = {}
    for name, mod in [("survey_evidence_v2", ev_mod), ("run_evidence_v2_interactive", run_mod), ("survey_research_authority_v2", low_mod)]:
        f = Path(mod.__file__).resolve()
        h, n = sha_file(f)
        modules[name] = {"file": str(f), "sha256": h, "bytes": n}
    # Committed blobs for comparison (git)
    import subprocess
    committed = {}
    try:
        r = subprocess.run(["git", "-C", str(repo_root), "ls-tree", "HEAD",
                            "scripts/survey_evidence_v2.py",
                            "scripts/run_evidence_v2_interactive.py",
                            "scripts/survey_research_authority_v2.py",
                            "tests/test_evidence_scaling_v2.py"],
                           capture_output=True, text=True, check=True)
        committed["ls_tree"] = r.stdout
        r2 = subprocess.run(["git", "-C", str(repo_root), "rev-parse", "HEAD"],
                            capture_output=True, text=True, check=True)
        committed["head"] = r2.stdout.strip()
        r3 = subprocess.run(["git", "-C", str(repo_root), "rev-parse", "HEAD^"],
                            capture_output=True, text=True, check=True)
        committed["parent"] = r3.stdout.strip()
    except Exception as e:
        committed["error"] = str(e)

    # Actual normal run via existing strict facade (no bypass)
    result = None
    error = None
    tb = None
    exit_code = 0
    try:
        result = run_mod.run(repo_root, state_path, input_path, supp_path)
    except Exception as e:
        error = str(e)
        tb = traceback.format_exc()
        exit_code = 2

    end_utc = utc_now()
    end_wall = time.time()
    end_mono = time.monotonic()
    rusage_after = resource.getrusage(resource.RUSAGE_SELF)
    io_after = read_proc_self_io()

    after_runtime = [pin_file(repo_root / r) for r in runtime_rels]
    after_state = [pin_file(repo_root / r) for r in state_rels]
    after_inputs = [pin_file(repo_root / r) for r in input_rels]
    after_full = {}
    try:
        # Re-hash full intended (same set as before_full keys, excluding error)
        for rel in before_full.keys():
            if rel == "error":
                continue
            q = repo_root / rel
            if q.is_file():
                h, n = sha_file(q)
                after_full[rel] = {"sha256": h, "bytes": n, "mode": oct(q.stat().st_mode & 0o777)}
            else:
                after_full[rel] = {"exists": False}
    except Exception as e:
        after_full = {"error": str(e)}

    def ru_to_dict(ru):
        return {k: getattr(ru, k) for k in dir(ru) if k.startswith("ru_")}

    record = {
        "argv": argv,
        "env": env,
        "cwd": cwd,
        "pid": pid,
        "start_utc": start_utc,
        "end_utc": end_utc,
        "start_wall": start_wall,
        "end_wall": end_wall,
        "elapsed_wall": end_wall - start_wall,
        "elapsed_mono": end_mono - start_mono,
        "exit": exit_code,
        "repo_root": str(repo_root),
        "state_path": str(state_path),
        "input_path": str(input_path),
        "supplement_path": str(supp_path),
        "before_runtime": before_runtime,
        "after_runtime": after_runtime,
        "before_state": before_state,
        "after_state": after_state,
        "before_inputs": before_inputs,
        "after_inputs": after_inputs,
        "before_full_count": len(before_full),
        "after_full_count": len(after_full),
        "source_mutated_during_run": (before_full != after_full),
        "modules": modules,
        "committed": committed,
        "rusage_before": ru_to_dict(rusage_before),
        "rusage_after": ru_to_dict(rusage_after),
        "io_before": io_before,
        "io_after": io_after,
        "result": result,
        "error": error,
        "traceback": tb,
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(record, indent=2, ensure_ascii=False))
    # stdout carries result summary (exclusive raw captured by caller)
    print(json.dumps({"exit": exit_code, "result": result, "error": error}, indent=2))
    if tb:
        print(tb, file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
