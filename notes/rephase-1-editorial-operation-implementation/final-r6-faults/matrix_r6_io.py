#!/usr/bin/env python3
"""R6 IO regression: adapt R5b matrix to R6 INERT (representative Weekly + LF healthy). No code IO bodies changed, final epoch new set must be proven."""
from __future__ import annotations
import json, os, sys, time, traceback, shutil, hashlib
from pathlib import Path
sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
    if os.environ.get(_v): print(f"UNSAFE {_v}"); sys.exit(2)
def log(m): print(m, flush=True)
REPO=Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey").resolve()
sys.path.insert(0, str(REPO/"notes/rephase-1-editorial-operation-implementation/final-r6-faults"))
from matrix_common import FAULT_BASE, INERT_W, PRELC_W, INERT_L, PRELC_L, cp_fixture, verify_fixture, run_subprocess, sha_file
ISSUE_W="2026-W37"; ISSUE_L="SP001"
NOTES=REPO/"notes/rephase-1-editorial-operation-implementation/final-r6-faults"
PASS=0; FAIL=0; CASES=[]
def case(n,fn):
    global PASS, FAIL
    t0=time.monotonic()
    try: fn(); dt=time.monotonic()-t0; log(f"CASE PASS {n} dt={dt:.1f}s"); CASES.append((n,"PASS",dt,"")); PASS+=1
    except AssertionError as e: dt=time.monotonic()-t0; log(f"CASE FAIL {n} dt={dt:.1f}s {e}"); traceback.print_exc(); CASES.append((n,"FAIL",dt,str(e)[:2500])); FAIL+=1
    except Exception as e: dt=time.monotonic()-t0; log(f"CASE BLOCKER {n} dt={dt:.1f}s {type(e).__name__}: {e}"); traceback.print_exc(); CASES.append((n,"BLOCKER",dt,f"{type(e).__name__}: {e}"[:2500])); FAIL+=1
def child_api(fixture: Path, code: str, timeout=300):
    return run_subprocess(fixture, [sys.executable,"-B","-c",code], cwd=fixture, timeout=timeout)
def new_fault(base: Path, name: str):
    dst=FAULT_BASE/name
    if dst.exists(): verify_fixture(dst, name+"(reuse)"); return dst
    cp_fixture(base, dst, name); return dst

def r6_record_rep():
    for fault in ["fsync","close","combined"]:
        name=f"r6-record-{fault}"
        dst=new_fault(INERT_W, name)
        state_rel=f"sources/{ISSUE_W}/production-state.json"
        set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/publication-set.json"
        code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import os
from scripts import survey_editorial_publication_v2 as m
orig_open=os.open; orig_write=os.write; orig_fsync=os.fsync; orig_close=os.close
rec_path=str((Path(r'{dst}')/r'sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json').resolve())
fds=set()
def my_open(p,f,*a,**kw):
    fd=orig_open(p,f,*a,**kw)
    try:
        if str(Path(str(p)).resolve())==rec_path: fds.add(fd)
    except: pass
    return fd
def my_write(fd,data): return orig_write(fd,data)
def my_fsync(fd):
    if fd in fds and r'{fault}' in ('fsync','combined'): raise OSError("injected record fsync R6")
    return orig_fsync(fd)
def my_close(fd):
    if fd in fds and r'{fault}' in ('close','combined'): raise OSError("injected record close R6")
    return orig_close(fd)
os.open=my_open; os.write=my_write; os.fsync=my_fsync; os.close=my_close
try:
    import datetime
    m.activate_publication(Path(r'{dst}'), r'{state_rel}', r'{set_rel}', "fault {fault} R6", "tester", datetime.datetime.now(datetime.timezone.utc))
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    out2=str(e); print(f"REFUSED {{out2[:2500]}}")
    low2=out2.lower()
    assert "record" in low2, out2[:1200]
    if r'{fault}'=='combined': assert "primary" in low2 and "secondary" in low2, f"combined {{low2[:1200]}}"
    # State must stay old r1, record partial preserved, no deletion
    import json as _j
    cur=_j.loads((Path(r'{dst}')/r'{state_rel}').read_bytes().decode())
    assert cur.get("publication_revalidation_provenance",{{}}).get("path","").endswith("publication-surface-revalidation-r1.json"), f"old {{cur}}"
    sys.exit(0)
"""
        r=child_api(dst, code); assert r["exit"]==0, f"R6 record {fault} must refuse {r['stdout'][:2500]} {r['stderr'][:800]}"
        log(f"R6 record {fault} REFUSED observed old preserved (fired seam record, primary+secondary) OK")

def r6_state_rep():
    for fault in ["temp_write","replace","postread"]:
        name=f"r6-state-{fault}"
        dst=new_fault(INERT_W, name)
        state_rel=f"sources/{ISSUE_W}/production-state.json"
        set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/publication-set.json"
        code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import os
from scripts import survey_editorial_publication_v2 as m
orig_open=os.open; orig_write=os.write; orig_fsync=os.fsync; orig_close=os.close; orig_replace=os.replace; orig_read=os.read
tfds=set()
def is_tmp(p):
    try: return ".production-state.json.tmp-reval-" in str(p)
    except: return False
def my_open(p,f,*a,**kw):
    fd=orig_open(p,f,*a,**kw)
    if is_tmp(p): tfds.add(fd)
    return fd
def my_write(fd,data):
    if fd in tfds and r'{fault}'=='temp_write': raise OSError("injected State temp write R6")
    return orig_write(fd,data)
def my_fsync(fd): return orig_fsync(fd)
def my_close(fd): return orig_close(fd)
def my_replace(s,d,*a,**kw):
    if str(d).endswith("production-state.json") and r'{fault}'=='replace': raise OSError("injected State replace R6")
    return orig_replace(s,d,*a,**kw)
os.open=my_open; os.write=my_write; os.fsync=my_fsync; os.close=my_close; os.replace=my_replace
flag={{"r":False}}
if r'{fault}'=='postread':
    orig_rep=orig_replace
    def my_replace2(s,d,*a,**kw):
        r=orig_rep(s,d,*a,**kw)
        if str(d).endswith("production-state.json"): flag["r"]=True
        return r
    os.replace=my_replace2
    def my_read(fd,n):
        if flag["r"]:
            if my_read.c<3: my_read.c+=1; raise OSError("injected postread R6")
        return orig_read(fd,n)
    my_read.c=0; os.read=my_read
try:
    import datetime
    m.activate_publication(Path(r'{dst}'), r'{state_rel}', r'{set_rel}', "fault {fault} R6", "tester", datetime.datetime.now(datetime.timezone.utc))
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    out2=str(e); print(f"REFUSED {{out2[:2500]}}")
    low2=out2.lower()
    if r'{fault}'=='postread':
        assert "unknown" in low2 or "postread" in low2 or "postreplace" in low2, f"postread unknown {{low2[:1200]}}"
    else:
        assert "state" in low2 and ("old" in low2 or "inert" in low2 or "preserved" in low2), f"State old {{low2[:1200]}}"
    sys.exit(0)
"""
        r=child_api(dst, code); assert r["exit"]==0, f"R6 State {fault} must refuse {r['stdout'][:2500]}"
        log(f"R6 State {fault} REFUSED OK")

def r6_foreign_orphan_active():
    # foreign
    dst=new_fault(INERT_W, "r6-foreign")
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r6-2/publication/publication-set.json"
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import os
from scripts import survey_agent_control_v2 as agent
from scripts import survey_editorial_publication_v2 as m
orig=agent._exclusive_create_record_bytes
def hooked(p,exp,label):
    owned=orig(p,exp,label)
    repl=Path(str(p)+".repl"); repl.write_bytes(exp)
    o=os.stat(p); n=os.stat(repl)
    assert (o.st_dev,o.st_ino)!=(n.st_dev,n.st_ino), "foreign while exists"
    os.replace(repl,p)
    assert not agent._record_identity_matches(Path(p), owned, exp)
    return owned
agent._exclusive_create_record_bytes=hooked
try:
    import datetime
    m.activate_publication(Path(r'{dst}'), r'{state_rel}', r'{set_rel}', "foreign R6", "tester", datetime.datetime.now(datetime.timezone.utc))
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    out2=str(e); print(f"REFUSED foreign {{out2[:2000]}}")
    assert "ownership" in out2.lower() or "inode" in out2.lower() or "foreign" in out2.lower(), out2[:1200]
    sys.exit(0)
"""
    r=child_api(dst, code); assert r["exit"]==0, f"R6 foreign must refuse {r['stdout'][:2500]}"
    log("R6 foreign REFUSED before State write OK")
    # orphan + resume + ALREADY_ACTIVE weekly
    dst2=new_fault(INERT_W, "r6-orphan")
    import shutil as _sh
    prelc_r2=PRELC_W/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    _sh.copy(str(prelc_r2), str(dst2/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"))
    rec_rel=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    code2=f"""
import sys; sys.path.insert(0, r'{dst2}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
import datetime
try:
    m.activate_publication(Path(r'{dst2}'), r'{state_rel}', r'{set_rel}', "orphan R6", "tester", datetime.datetime.now(datetime.timezone.utc))
    print("UNEXPECTED_FORK"); sys.exit(10)
except Exception as e:
    assert "collision" in str(e).lower() or "intent" in str(e).lower(), str(e)[:1200]
    print("orphan COLLISION no fork")
    res=m.resume_activation(Path(r'{dst2}'), r'{state_rel}', r'{rec_rel}')
    assert res.get("status")=="RESUMED" and res.get("observed")=="new", res
    print(f"RESUMED {{res}}")
"""
    r2=child_api(dst2, code2); assert r2["exit"]==0, f"R6 orphan must COLLISION then RESUMED {r2['stdout'][:2500]}"
    assert not (dst2/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r3.json").exists(), "no r3 fork R6"
    log("R6 orphan COLLISION no fork + RESUMED exact OK")
    # ALREADY_ACTIVE weekly + LF healthy resume control (representative both routes, no double R1)
    for label, base, issue, prop in [("weekly",PRELC_W,"2026-W37","wk-r6-2"),("longform",PRELC_L,"SP001","lf-r6-2")]:
        d=new_fault(base, f"r6-already-{label}")
        srel=f"sources/{issue}/production-state.json"
        srel_set=f"sources/{issue}/publication/v2/editorial-corrections/{prop}/publication/publication-set.json"
        code3=f"""
import sys; sys.path.insert(0, r'{d}')
from pathlib import Path
import datetime
from scripts import survey_editorial_publication_v2 as m
res=m.activate_publication(Path(r'{d}'), r'{srel}', r'{srel_set}', "already R6", "tester", datetime.datetime.now(datetime.timezone.utc))
assert res.get("status")=="ALREADY_ACTIVE", res
print(f"{{res}}")
"""
        r3=child_api(d, code3); assert r3["exit"]==0, f"R6 ALREADY_ACTIVE {label} failed {r3['stdout'][:1000]}"
        log(f"R6 ALREADY_ACTIVE {label} readonly OK (positive controls both routes)")

def main():
    for n,f in [("R6_record_rep",r6_record_rep),("R6_state_rep",r6_state_rep),("R6_foreign_orphan_active",r6_foreign_orphan_active)]:
        case(n,f)
    log(f"TOTAL IO pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_r6_io.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    import sys as _s; _s.exit(rc)
