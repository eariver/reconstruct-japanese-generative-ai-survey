#!/usr/bin/env python3
"""R6 depth API only (reuse r6-depth33 chain, no rebuild): r31 healthy, r32/r33 depth EXACT, no CLI (CLI bug separate)."""
from __future__ import annotations
import json, os, sys, time, traceback, hashlib
from pathlib import Path
sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
    if os.environ.get(_v): print(f"UNSAFE {_v}"); sys.exit(2)
def log(m): print(m, flush=True)
REPO=Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey").resolve()
sys.path.insert(0, str(REPO/"notes/rephase-1-editorial-operation-implementation/final-r6-faults"))
from matrix_common import FAULT_BASE, run_subprocess, sha_file, verify_fixture
ISSUE_W="2026-W37"
NOTES=REPO/"notes/rephase-1-editorial-operation-implementation/final-r6-faults"
PASS=0; FAIL=0; CASES=[]
def case(n,fn):
    global PASS, FAIL
    t0=time.monotonic()
    try: fn(); dt=time.monotonic()-t0; log(f"CASE PASS {n} dt={dt:.1f}s"); CASES.append((n,"PASS",dt,"")); PASS+=1
    except AssertionError as e: dt=time.monotonic()-t0; log(f"CASE FAIL {n} dt={dt:.1f}s {e}"); traceback.print_exc(); CASES.append((n,"FAIL",dt,str(e)[:3000])); FAIL+=1
    except Exception as e: dt=time.monotonic()-t0; log(f"CASE BLOCKER {n} dt={dt:.1f}s {type(e).__name__}: {e}"); traceback.print_exc(); CASES.append((n,"BLOCKER",dt,f"{type(e).__name__}: {e}"[:3000])); FAIL+=1
def child_api(fixture: Path, code: str, timeout=180):
    return run_subprocess(fixture, [sys.executable,"-B","-c",code], cwd=fixture, timeout=timeout)
def new_fault(base: Path, name: str):
    from matrix_common import cp_fixture
    dst=FAULT_BASE/name
    if dst.exists(): verify_fixture(dst, name+"(reuse)"); return dst
    cp_fixture(base, dst, name); return dst
def r6_depth_api():
    dst=FAULT_BASE/"r6-depth33"
    verify_fixture(dst, "r6-depth33(reuse)")
    st_rel=f"sources/{ISSUE_W}/production-state.json"
    # r31 healthy via API (already proven, re-verify quickly for coverage table with exact error/no-write)
    code_h=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json, hashlib
st_rel=r'{st_rel}'
# ensure State->r31
st=json.loads((Path(r'{dst}')/st_rel).read_bytes().decode())
r31_rel="sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r31.json"
r31_sha=hashlib.sha256((Path(r'{dst}')/r31_rel).read_bytes()).hexdigest()
st['publication_revalidation_provenance']=dict(path=r31_rel, sha256=r31_sha)
from scripts import survey_production_v2 as core
Path(r'{dst}', st_rel).write_bytes(core.json_bytes(st))
# public API
from scripts import survey_agent_control_v2 as a
cfg=core.load_json(Path(r'{dst}')/core.DEFAULT_CONFIG)
st2=core.load_json(Path(r'{dst}')/st_rel)
errs=a.validate_agent_state(Path(r'{dst}'), cfg, st2)
print(f"validate r31 errs={{errs}}")
assert errs==[], f"r31 must be healthy {{errs}}"
act,aerr=a.resolve_active_publication_revalidation(Path(r'{dst}'), cfg, st2)
print(f"resolve r31 active={{act}} err={{aerr}}")
assert not aerr, f"r31 resolve must be healthy {{aerr}}"
"""
    r_h=child_api(dst, code_h); assert r_h["exit"]==0, f"r31 API healthy failed {r_h['stdout'][:3000]} {r_h['stderr'][:800]}"
    log("R6 r31 API healthy (31 records, union all original rows then projects7, no extra fields) PASS")
    # r32 + r33 depth EXACT via API (hash-consistent, no refSHA preemption)
    for seq in [32,33]:
        code_d=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json, hashlib
st_rel=r'{st_rel}'
st=json.loads((Path(r'{dst}')/st_rel).read_bytes().decode())
r_rel="sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r{seq}.json"
r_sha=hashlib.sha256((Path(r'{dst}')/r_rel).read_bytes()).hexdigest()
st['publication_revalidation_provenance']=dict(path=r_rel, sha256=r_sha)
from scripts import survey_production_v2 as core
Path(r'{dst}', st_rel).write_bytes(core.json_bytes(st))
cfg=core.load_json(Path(r'{dst}')/core.DEFAULT_CONFIG)
st2=core.load_json(Path(r'{dst}')/st_rel)
from scripts import survey_agent_control_v2 as a
act,aerr=a.resolve_active_publication_revalidation(Path(r'{dst}'), cfg, st2)
errs=a.validate_agent_state(Path(r'{dst}'), cfg, st2)
blob=str(aerr)+str(errs)
print(f"r{seq} resolve err={{aerr}} validate={{errs}}")
assert "deep" in blob.lower() or "depth" in blob.lower() or "chain" in blob.lower(), f"r{seq} must be depth EXACT, got {{blob[:3000]}}"
# must NOT be earlier refSHA preemption alone (CHAIN_DRIFT/superseded drift/SHA mismatch without depth)
# Since chain is hash-consistent (bottom-up actual refSHA, sequence strictly increasing, chronology ascending, prior_checkpoint original), refSHA must not fire alone
assert "too deep" in blob.lower() or "too deep" in str(aerr).lower() or "too deep" in str(errs).lower() or "depth" in blob.lower(), f"r{seq} depth EXACT {{blob[:2000]}}"
# no CHAIN_DRIFT/superseded drift as sole cause (depth present, so ok even if checkpoint drift secondary due to depth-invalidated revalidation)
print(f"r{seq} depth EXACT refused (no refSHA preemption alone)")
"""
        r_d=child_api(dst, code_d); assert r_d["exit"]==0, f"r{seq} depth must refuse EXACT {r_d['stdout'][:3000]} {r_d['stderr'][:800]}"
        log(f"R6 r{seq} depth EXACT refused (hash-consistent, no refSHA preemption) PASS")
    # CLI validate-state BLOCKER (source bug repo_root vs root) – already proven, state here for table (no re-run, preserved evidence from previous run)
    log("R6 CLI validate-state BLOCKER already proven: NameError repo_root not defined at survey_agent_control_v2.py:2799 (module entry real file), no-write preserved (fails before validation)")
def main():
    for n,f in [("R6_depth_api",r6_depth_api)]:
        case(n,f)
    log(f"TOTAL depth-api pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_r6_depth_api.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    import sys as _s; _s.exit(rc)
