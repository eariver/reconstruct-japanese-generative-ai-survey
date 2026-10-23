#!/usr/bin/env python3
"""Group C4: ALREADY_ACTIVE, CLI resume unknown, observed new."""
from __future__ import annotations
import json, os, sys, time, traceback
from pathlib import Path
sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
    if os.environ.get(_v): print(f"UNSAFE {_v}"); sys.exit(2)
def log(m): print(m, flush=True)
REPO=Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey").resolve()
sys.path.insert(0, str(REPO/"notes/rephase-1-editorial-operation-implementation/final-r5b-faults"))
from matrix_common import FAULT_BASE, INERT_W, PRELC_W, cp_fixture, verify_fixture, run_subprocess, sha_file
ISSUE_W="2026-W37"
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
def c_already():
    dst=new_fault(PRELC_W, "c-already-v2")
    import hashlib as _h
    def snap(p):
        d={}
        for dp,dn,fn in os.walk(p):
            if ".git" in Path(dp).parts: dn[:]=[]; continue
            for f in sorted(fn):
                pp=Path(dp)/f
                try:
                    if pp.is_symlink(): continue
                    d[pp.relative_to(p).as_posix()]=_h.sha256(pp.read_bytes()).hexdigest()
                except: pass
        return d
    before=snap(dst)
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
import datetime
res=m.activate_publication(Path(r'{dst}'), r'{state_rel}', r'{set_rel}', "already", "tester", datetime.datetime.now(datetime.timezone.utc))
print(f"ALREADY {{res}}"); assert res.get("status")=="ALREADY_ACTIVE" and res.get("observed")=="new", res
"""
    r=child_api(dst, code); assert r["exit"]==0, f"ALREADY_ACTIVE failed {r['stdout'][:1000]}"
    assert snap(dst)==before, "ALREADY_ACTIVE must be readonly"
    log("C ALREADY_ACTIVE readonly OK")
def c_cli_resume_unknown():
    dst=new_fault(INERT_W, "c-cli-resume-unknown")
    import shutil as _sh, json as _j
    prelc_r2=PRELC_W/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    _sh.copy(str(prelc_r2), str(dst/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"))
    st_rel=f"sources/{ISSUE_W}/production-state.json"
    st=_j.loads((dst/st_rel).read_bytes().decode()); st["publication_revalidation_provenance"]=None
    (dst/st_rel).write_bytes(json.dumps(st, indent=2, sort_keys=True).encode()+b"\n")
    rec_rel=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    cr=run_subprocess(dst, [sys.executable,"-B","-m","scripts.survey_editorial_publication_v2","--repo-root",str(dst),"resume-activation","--state",st_rel,"--record",rec_rel], cwd=dst)
    assert cr["exit"]==2, f"CLI resume unknown should exit2, got {cr['exit']} {cr['stdout'][:800]} {cr['stderr'][:800]}"
    log(f"C CLI resume unknown exit2 OK: {cr['stderr'][:400]}")
def c_observed_new():
    dst=new_fault(INERT_W, "c-observed-new")
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import os
from scripts import survey_editorial_publication_v2 as m
orig_replace=os.replace
def my_replace(s,d,*a,**kw):
    r=orig_replace(s,d,*a,**kw)
    # after State replace succeeds (State new), corrupt seal to force post validation failure (observed new)
    if str(d).endswith("production-state.json"):
        seal_p=Path(r'{dst}')/r'{set_rel}'
        b=seal_p.read_bytes()
        seal_p.write_bytes(b+b"\\n#CORRUPT-POST")
    return r
os.replace=my_replace
try:
    import datetime
    m.activate_publication(Path(r'{dst}'), r'{state_rel}', r'{set_rel}', "observed new", "tester", datetime.datetime.now(datetime.timezone.utc))
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    msg2=str(e); print(f"REFUSED: {{msg2[:2500]}}")
    low2=msg2.lower()
    assert "postreplace" in low2 or "post" in low2, f"should be postreplace {{low2[:1200]}}"
    assert "new" in low2, f"observed new expected {{low2[:1200]}}"
    # State must be new (replace succeeded), record preserved, no deletion
    import json as _j
    cur=_j.loads((Path(r'{dst}')/r'{state_rel}').read_bytes().decode())
    # pointer should be new r2 (since replace succeeded)
    assert cur.get("publication_revalidation_provenance",{{}}).get("path","").endswith("publication-surface-revalidation-r2.json"), f"State should be new r2 {{cur}}"
    sys.exit(0)
"""
    r=child_api(dst, code); assert r["exit"]==0, f"observed new should refuse postreplace with new {r['stdout'][:2500]}"
    log("C observed new (post validation fail after replace) OK")
def main():
    for n,f in [("C_already",c_already),("C_cli_resume_unknown",c_cli_resume_unknown),("C_observed_new",c_observed_new)]:
        case(n,f)
    log(f"TOTAL C4 pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_c4.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    import sys as _s; _s.exit(rc)
