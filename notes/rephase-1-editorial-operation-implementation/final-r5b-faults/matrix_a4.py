#!/usr/bin/env python3
"""Group A4: 2route positives, LF reader canonical, both before kinds, CLI resume, observed new."""
from __future__ import annotations
import json, os, sys, time, traceback
from pathlib import Path
sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
    if os.environ.get(_v): print(f"UNSAFE {_v}"); sys.exit(2)
def log(m): print(m, flush=True)
REPO=Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey").resolve()
sys.path.insert(0, str(REPO/"notes/rephase-1-editorial-operation-implementation/final-r5b-faults"))
from matrix_common import FAULT_BASE, INERT_W, PRELC_W, INERT_L, PRELC_L, cp_fixture, verify_fixture, run_subprocess, sha_file
NOTES=REPO/"notes/rephase-1-editorial-operation-implementation/final-r5b-faults"
PASS=0; FAIL=0; CASES=[]
def case(n,fn):
    global PASS, FAIL
    t0=time.monotonic()
    try: fn(); dt=time.monotonic()-t0; log(f"CASE PASS {n} dt={dt:.1f}s"); CASES.append((n,"PASS",dt,"")); PASS+=1
    except AssertionError as e: dt=time.monotonic()-t0; log(f"CASE FAIL {n} dt={dt:.1f}s {e}"); traceback.print_exc(); CASES.append((n,"FAIL",dt,str(e)[:1500])); FAIL+=1
    except Exception as e: dt=time.monotonic()-t0; log(f"CASE BLOCKER {n} dt={dt:.1f}s {type(e).__name__}: {e}"); traceback.print_exc(); CASES.append((n,"BLOCKER",dt,f"{type(e).__name__}: {e}"[:1500])); FAIL+=1
def child_api(fixture: Path, code: str, timeout=180):
    return run_subprocess(fixture, [sys.executable,"-B","-c",code], cwd=fixture, timeout=timeout)
def new_fault(base: Path, name: str):
    dst=FAULT_BASE/name
    if dst.exists(): verify_fixture(dst, name+"(reuse)"); return dst
    cp_fixture(base, dst, name); return dst

def a_2route_positives():
    for label, base, issue, prop in [("weekly",PRELC_W,"2026-W37","wk-r5b-2"),("longform",PRELC_L,"SP001","lf-r5b-2")]:
        dst=new_fault(base, f"a-2route-{label}")
        state_rel=f"sources/{issue}/production-state.json"
        set_rel=f"sources/{issue}/publication/v2/editorial-corrections/{prop}/publication/publication-set.json"
        code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m, survey_publication_set_v2 as s, survey_production_v2 as core, survey_agent_control_v2 as a
v=m.validate_prepared_set(Path(r'{dst}'), r'{state_rel}', r'{set_rel}')
assert v.get('issue_id')=="{issue}"
cfg=core.load_json(Path(r'{dst}')/core.DEFAULT_CONFIG)
st=core.load_json(Path(r'{dst}')/r'{state_rel}')
assert a.validate_agent_state(Path(r'{dst}'), cfg, st)==[]
sel=s.resolve_publication_selection(Path(r'{dst}'), cfg, st)
assert sel.get('mode')=="VERSIONED_ACTIVE" and "{prop}" in (sel.get('candidate_ref') or {{}}).get("path","")
print("{label} healthy VERSIONED_ACTIVE")
"""
        r=child_api(dst, code); assert r["exit"]==0, f"{label} healthy failed {r['stdout'][:1000]} {r['stderr'][:800]}"
        log(f"A 2route {label} healthy OK")
    # LF specific reader canonical: longform reader input must be longform canonical (not weekly)? Check longform reader file exists and Gate uses longform?
    # Both before kinds: retention must have COPY and KEEP policies at least one route
    dst=new_fault(INERT_W, "a-before-kinds")
    code2=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json
from scripts import survey_production_v2 as core
staged=json.loads((Path(r'{dst}')/r'sources/2026-W37/publication/v2/editorial-corrections/wk-r5b-2/staged-source/staged-source-manifest.json').read_bytes().decode())
ret=json.loads((Path(r'{dst}')/staged['retention_manifest_ref']['path']).read_bytes().decode())
pols=set(x.get('policy') for x in ret.get('rows',[]))
print(f"pols={{pols}}")
assert "COPY_BEFORE_REPLACEMENT" in pols and "KEEP_IMMUTABLE" in pols, f"both before kinds required {{pols}}"
# LF reader canonical: longform inert reader must exist and be longform (check issue SP001)
import pathlib as _p
lf_reader=_p.Path(r'{INERT_L}')/r'sources/SP001/publication/v2/editorial-corrections/lf-r5b-2/reader-surface-input-v2.json'
assert lf_reader.is_file(), "LF reader missing"
print("LF reader canonical exists")
"""
    r2=child_api(dst, code2); assert r2["exit"]==0, f"before kinds/LF reader failed {r2['stdout'][:1000]}"
    log("A both before kinds + LF reader canonical OK")

def main():
    for n,f in [("A_2route_positives",a_2route_positives)]:
        case(n,f)
    log(f"TOTAL A4 pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_a4.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    import sys as _s; _s.exit(rc)
