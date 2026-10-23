#!/usr/bin/env python3
"""Group C3: postread (os.*), foreign v2, orphan v2 fresh, CLI already."""
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
def child_cli(fixture: Path, args: list[str], timeout=120):
    return run_subprocess(fixture, [sys.executable,"-B","-m","scripts.survey_editorial_publication_v2"]+args, cwd=fixture, timeout=timeout)
def new_fault(base: Path, name: str):
    dst=FAULT_BASE/name
    if dst.exists(): verify_fixture(dst, name+"(reuse)"); return dst
    cp_fixture(base, dst, name); return dst

def c_postread_v2():
    dst=new_fault(INERT_W, "c-state-postread-v2")
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import os
from scripts import survey_editorial_publication_v2 as m
orig_open=os.open; orig_read=os.read; orig_close=os.close; orig_replace=os.replace
flag={{"r":False}}
def my_replace(s,d,*a,**kw):
    r=orig_replace(s,d,*a,**kw)
    if str(d).endswith("production-state.json"): flag["r"]=True
    return r
def my_read(fd,n):
    # fail reads of State after replace (postread) – need to identify State FD? Track opens of State path.
    # Simpler: after flag, fail all os.read with OSError? That would also fail other reads (selection, etc.) – but postread is first read after replace, so failing all after flag will cause postread failure (observed unknown), which is intended. Other reads after (selection) will also fail, but primary is postread.
    if flag["r"]:
        # fail only first 2 reads after replace, then delegate (to allow snapshot? No, child exits after, so fail all is fine – will cause POSTREAD_FAIL)
        if my_read.c<3:
            my_read.c+=1; raise OSError("injected postread os.read")
    return orig_read(fd,n)
my_read.c=0
os.replace=my_replace; os.read=my_read
# also need to track State opens? os.read fails for any FD after flag, including record reads? Record reads happen before replace (flag False), so safe. After replace, only State postread + selection + record + set reads happen – failing all will cause postread failure first (observed unknown). Good.
try:
    import datetime
    m.activate_publication(Path(r'{dst}'), r'{state_rel}', r'{set_rel}', "postread", "tester", datetime.datetime.now(datetime.timezone.utc))
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    msg2=str(e); print(f"REFUSED: {{msg2[:2500]}}")
    low2=msg2.lower()
    assert "postread" in low2 or "postreplace" in low2 or "unknown" in low2, f"postread should be unknown {{low2[:1200]}}"
    sys.exit(0)
"""
    r=child_api(dst, code); assert r["exit"]==0, f"postread v2 should refuse unknown {r['stdout'][:2500]} {r['stderr'][:800]}"
    log("C postread v2 (os.read) refused unknown OK")

def c_foreign_v2():
    dst=new_fault(INERT_W, "c-foreign-v2")
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import os
from scripts import survey_agent_control_v2 as agent
from scripts import survey_editorial_publication_v2 as m
orig_excl=agent._exclusive_create_record_bytes
def hooked(p,exp,label):
    owned=orig_excl(p,exp,label)
    repl=Path(str(p)+".repl")
    repl.write_bytes(exp)
    o=os.stat(p); n=os.stat(repl)
    assert (o.st_dev,o.st_ino)!=(n.st_dev,n.st_ino), "foreign must be different inode while original exists"
    os.replace(repl,p)
    assert not agent._record_identity_matches(Path(p), owned, exp), "foreign must not match"
    assert Path(p).is_file()
    return owned
agent._exclusive_create_record_bytes=hooked
try:
    import datetime
    m.activate_publication(Path(r'{dst}'), r'{state_rel}', r'{set_rel}', "foreign", "tester", datetime.datetime.now(datetime.timezone.utc))
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    out=str(e); print(f"REFUSED foreign: {{out[:2500]}}")
    low=out.lower()
    assert "ownership" in low or "inode" in low or "foreign" in low or "record" in low, out[:1200]
    assert "old" in low or "inert" in low or "preserved" in low, f"foreign observed old {{low[:1200]}}"
    import json as _j
    cur=_j.loads((Path(r'{dst}')/r'{state_rel}').read_bytes().decode())
    assert cur.get("publication_revalidation_provenance",{{}}).get("path","").endswith("publication-surface-revalidation-r1.json"), f"State old {{cur}}"
    sys.exit(0)
"""
    r=child_api(dst, code); assert r["exit"]==0, f"foreign v2 should refuse {r['stdout'][:2500]}"
    log("C foreign v2 refused before State write OK")

def c_orphan_v2():
    dst=new_fault(INERT_W, "c-orphan-v2")
    import shutil as _sh
    prelc_r2=PRELC_W/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    dst_r2=dst/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    if not dst_r2.exists(): _sh.copy(str(prelc_r2), str(dst_r2))
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
    rec_rel=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
import datetime
try:
    m.activate_publication(Path(r'{dst}'), r'{state_rel}', r'{set_rel}', "orphan", "tester", datetime.datetime.now(datetime.timezone.utc))
    print("UNEXPECTED_PASS_FORK"); sys.exit(10)
except Exception as e:
    out=str(e); print(f"REFUSED orphan: {{out[:2000]}}")
    low=out.lower()
    assert "collision" in low or "intent" in low or "orphan" in low or "resume" in low, out[:1200]
    sys.exit(0)
"""
    r=child_api(dst, code); assert r["exit"]==0, f"orphan v2 must COLLISION {r['stdout'][:2000]}"
    assert not (dst/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r3.json").exists(), "no r3 fork"
    log("C orphan v2 COLLISION no fork OK")
    code2=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
from scripts import survey_publication_set_v2 as s, survey_production_v2 as core, survey_agent_control_v2 as a
import hashlib
res=m.resume_activation(Path(r'{dst}'), r'{state_rel}', r'{rec_rel}')
print(f"RESUME {{res}}"); assert res.get("status")=="RESUMED" and res.get("observed")=="new", res
ns=json.loads((Path(r'{dst}')/r'{state_rel}').read_bytes().decode()) if False else None
"""
    # fix code2: need json import
    code2=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import json, hashlib
from scripts import survey_editorial_publication_v2 as m
from scripts import survey_publication_set_v2 as s, survey_production_v2 as core, survey_agent_control_v2 as a
res=m.resume_activation(Path(r'{dst}'), r'{state_rel}', r'{rec_rel}')
print(f"RESUME {{res}}"); assert res.get("status")=="RESUMED" and res.get("observed")=="new", res
ns=json.loads((Path(r'{dst}')/r'{state_rel}').read_bytes().decode())
assert ns.get("publication_revalidation_provenance")==dict(path=r'{rec_rel}', sha256=hashlib.sha256((Path(r'{dst}')/r'{rec_rel}').read_bytes()).hexdigest())
cfg=core.load_json(Path(r'{dst}')/core.DEFAULT_CONFIG)
assert a.validate_agent_state(Path(r'{dst}'), cfg, ns)==[]
sel=s.resolve_publication_selection(Path(r'{dst}'), cfg, ns)
assert sel.get("mode")=="VERSIONED_ACTIVE" and "wk-r5b-2" in (sel.get("candidate_ref") or {{}}).get("path","")
"""
    r2=child_api(dst, code2); assert r2["exit"]==0, f"orphan resume v2 should RESUMED {r2['stdout'][:2000]}"
    log("C orphan v2 resume RESUMED exact OK")

def main():
    for n,f in [("C_postread_v2",c_postread_v2),("C_foreign_v2",c_foreign_v2),("C_orphan_v2",c_orphan_v2)]:
        case(n,f)
    log(f"TOTAL C3 pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_c3.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    import sys as _s; _s.exit(rc)
