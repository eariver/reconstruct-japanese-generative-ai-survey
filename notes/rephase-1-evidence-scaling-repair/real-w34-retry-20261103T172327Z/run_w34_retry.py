#!/usr/bin/env python3
"""Fresh fail-closed W34 409 retry harness (REAL normal run, facade fix).

Bound to NEW retry epoch e84a82a (parent 48082356). Fail-closed: verifies
expected runtime/input SHAs before normal run; refuses on mismatch.
Calls normal scripts.run_evidence_v2_interactive.run only. No bypass,
no monkeypatch, no preloaded context, no subset, no projection.
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

EXPECTED_RUNTIME = {
    "scripts/survey_evidence_v2.py": ("487425385052fa181b0a24954815c6fbb6882a0af1fc7256ef7352b309359c2a", 158943),
    "scripts/run_evidence_v2_interactive.py": ("5e195730d1553b2359eb5729cebaa49e9bd616b4b3f63b65dca413ef33c3e543", 45833),
    "scripts/survey_research_authority_v2.py": ("0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b", 218692),
    "tests/test_evidence_scaling_v2.py": ("d486809c4ae88c0e78784ade8e456cd9227b25a29c12cde9700664a1eec3edad", 91561),
}
EXPECTED_INPUTS = {
    "sources/2026-W34/production-state.json": ("7e6a50c2b84cdc7e526f1560f02efd95184685770edb95ab35bb9a40c633ea58", 3386),
    "sources/2026-W34/production-profile.json": ("2a8c3089cec29eb64e121cdf0429eed38670df704ebe955079751198557cfeb1", 2371),
    "sources/2026-W34/discovery/discovery-v2.jsonl": ("e176326f853ed42b69bad8a1998513d8dba8d3838af7cdea0ca9bc8261df46b0", 963155),
    "sources/2026-W34/screening/input/event-discovery-v2.jsonl": ("0a23be47dad8ddaf4f0a9c3261d97cc0006ac942bfd2321be2487289a34da31e", 1335444),
    "sources/2026-W34/screening/v2/accepted/e193ad0507895568e369437833b87d2610d68ef50f0c6419b092f5711e26bbea/screening-accepted.json": ("b9d963d83b712ba3fb7e93358f051c4e902f31d0e262c44eea6f76dcdf155841", 543880),
    "sources/2026-W34/evidence/proposed-input/interactive-evidence.json": ("3ffc6e310e389bf03275b7ac7df0b029e43acec5f6140cc3a5bd56f8a4794f27", 1573186),
    "sources/2026-W34/external/evidence-supplement/evidence-authority-supplement-r2-fresh-basis.json": ("ce6f977a3e690e779c380b7b035d9247207e262b5c50a5b14b6b6b8f0fbc704e", 389414),
}
EXPECTED_HEAD = "e84a82aca000c990597ea8cf60f548e2ff187bd1"
EXPECTED_PARENT = "480823560c0c26ed2e5baa18e0e79a22b2839a27"


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

    def pin_file(p: Path):
        try:
            h, n = sha_file(p)
            st = p.stat()
            return {"path": str(p), "sha256": h, "bytes": n,
                    "mode": oct(st.st_mode & 0o777), "exists": True}
        except FileNotFoundError:
            return {"path": str(p), "exists": False}

    # Fail-closed guards bound to NEW IDs/source
    guard_errors = []
    for rel, (exp_sha, exp_bytes) in {**EXPECTED_RUNTIME, **EXPECTED_INPUTS}.items():
        q = repo_root / rel
        try:
            h, n = sha_file(q)
            if h != exp_sha or n != exp_bytes:
                guard_errors.append(f"{rel} mismatch: got {h}/{n} exp {exp_sha}/{exp_bytes}")
        except FileNotFoundError:
            guard_errors.append(f"{rel} missing")
    import subprocess
    try:
        head = subprocess.run(["git", "-C", str(repo_root), "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
        parent = subprocess.run(["git", "-C", str(repo_root), "rev-parse", "HEAD^"],
                                capture_output=True, text=True, check=True).stdout.strip()
        if head != EXPECTED_HEAD:
            guard_errors.append(f"HEAD mismatch: got {head} exp {EXPECTED_HEAD}")
        if parent != EXPECTED_PARENT:
            guard_errors.append(f"parent mismatch: got {parent} exp {EXPECTED_PARENT}")
    except Exception as e:
        guard_errors.append(f"git guard failed: {e}")
    # Canonical must be absent at entry
    if (repo_root / "sources/2026-W34/evidence/v2").exists():
        guard_errors.append("canonical evidence/v2 already exists at entry (must be absent)")
    if (repo_root / "sources/2026-W34/materiality-ledger-v2.json").exists():
        guard_errors.append("ledger already exists at entry")
    if (repo_root / "sources/2026-W34/profile-completeness-v2.json").exists():
        guard_errors.append("completeness already exists at entry")

    runtime_rels = list(EXPECTED_RUNTIME.keys())
    state_rels = [
        "sources/2026-W34/production-state.json",
        "sources/2026-W34/production-profile.json",
        "sources/2026-W34/orchestration/v2/checkpoints/DISCOVERY_COLLECTED.json",
        "sources/2026-W34/orchestration/v2/checkpoints/ISSUE_INITIALIZED.json",
        "sources/SP-efficient-llm-2026/production-state.json",
        "sources/SP-efficient-llm-2026/production-profile.json",
    ]
    input_rels = list(EXPECTED_INPUTS.keys())[2:]
    before_runtime = [pin_file(repo_root / r) for r in runtime_rels]
    before_state = [pin_file(repo_root / r) for r in state_rels]
    before_inputs = [pin_file(repo_root / r) for r in EXPECTED_INPUTS.keys()]
    before_full = {}
    try:
        manifest_path = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-profile-support-implementation/source-packaging/final-20261031T202327Z/complete-profile-support-manifest.json")
        manifest = json.loads(manifest_path.read_bytes())
        for rel in manifest.get("files", {}).keys():
            q = repo_root / rel
            if q.is_file():
                h, n = sha_file(q)
                before_full[rel] = {"sha256": h, "bytes": n, "mode": oct(q.stat().st_mode & 0o777)}
            else:
                before_full[rel] = {"exists": False}
        q = repo_root / "tests/test_evidence_scaling_v2.py"
        h, n = sha_file(q)
        before_full["tests/test_evidence_scaling_v2.py"] = {"sha256": h, "bytes": n, "mode": oct(q.stat().st_mode & 0o777)}
    except Exception as e:
        before_full = {"error": str(e)}

    sys.path.insert(0, str(repo_root))
    import scripts.survey_evidence_v2 as ev_mod
    import scripts.run_evidence_v2_interactive as run_mod
    import scripts.survey_research_authority_v2 as low_mod
    modules = {}
    for name, mod in [("survey_evidence_v2", ev_mod), ("run_evidence_v2_interactive", run_mod), ("survey_research_authority_v2", low_mod)]:
        f = Path(mod.__file__).resolve()
        h, n = sha_file(f)
        modules[name] = {"file": str(f), "sha256": h, "bytes": n}
    committed = {}
    try:
        r = subprocess.run(["git", "-C", str(repo_root), "ls-tree", "HEAD",
                            "scripts/survey_evidence_v2.py",
                            "scripts/run_evidence_v2_interactive.py",
                            "scripts/survey_research_authority_v2.py",
                            "tests/test_evidence_scaling_v2.py"],
                           capture_output=True, text=True, check=True)
        committed["ls_tree"] = r.stdout
        committed["head"] = head
        committed["parent"] = parent
    except Exception as e:
        committed["error"] = str(e)

    result = None
    error = None
    tb = None
    exit_code = 0
    if guard_errors:
        exit_code = 3
        error = "FAIL-CLOSED guard refused: " + "; ".join(guard_errors)
    else:
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
    after_inputs = [pin_file(repo_root / r) for r in EXPECTED_INPUTS.keys()]
    after_full = {}
    try:
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
        "argv": argv, "env": env, "cwd": cwd, "pid": pid,
        "start_utc": start_utc, "end_utc": end_utc,
        "start_wall": start_wall, "end_wall": end_wall,
        "elapsed_wall": end_wall - start_wall,
        "elapsed_mono": end_mono - start_mono,
        "exit": exit_code,
        "guard_errors": guard_errors,
        "repo_root": str(repo_root),
        "state_path": str(state_path),
        "input_path": str(input_path),
        "supplement_path": str(supp_path),
        "before_runtime": before_runtime, "after_runtime": after_runtime,
        "before_state": before_state, "after_state": after_state,
        "before_inputs": before_inputs, "after_inputs": after_inputs,
        "before_full_count": len(before_full), "after_full_count": len(after_full),
        "source_mutated_during_run": (before_full != after_full),
        "modules": modules, "committed": committed,
        "rusage_before": ru_to_dict(rusage_before),
        "rusage_after": ru_to_dict(rusage_after),
        "io_before": io_before, "io_after": io_after,
        "result": result, "error": error, "traceback": tb,
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(record, indent=2, ensure_ascii=False))
    print(json.dumps({"exit": exit_code, "result": result, "error": error}, indent=2))
    if tb:
        print(tb, file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
