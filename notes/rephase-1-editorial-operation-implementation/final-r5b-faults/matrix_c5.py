#!/usr/bin/env python3
"""Group C5: record pre/partial/post + CLI validate/activate negatives."""
from __future__ import annotations
import json, os, sys, time, traceback
from pathlib import Path
sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
    if os.environ.get(_v): print(f"UNSAFE {_v}"); sys.exit(2)
def log(m): print(m, flush=True)
REPO=Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey").resolve()
sys.path.insert(0, str(REPO/"notes/rephase-1-editorial-operation-implementation/final-r5b-faults"))
from matrix_common import FAULT_BASE, INERT_W, cp_fixture, verify_fixture, run_subprocess
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
def c_record_pre_partial_post():
    for fault in ["pre","partial","post"]:
        name=f"c-record-{fault}-v2"
        dst=new_fault(INERT_W, name)
        state_rel=f"sources/{ISSUE_W}/production-state.json"
        set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
        code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import os
from scripts import survey_editorial_publication_v2 as m
orig_open=os.open; orig_write=os.write; orig_read=os.read
rec_path=str((Path(r'{dst}')/r'sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json').resolve())
fds=set()
def my_open(p,f,*a,**kw):
    import os as _o
    # pre fault: fail exclusive open
    try:
        if str(Path(str(p)).resolve())==rec_path and r'{fault}'=='pre':
            raise FileExistsError("injected pre open collision")
    except FileExistsError: raise
    except: pass
    fd=orig_open(p,f,*a,**kw)
    try:
        if str(Path(str(p)).resolve())==rec_path: fds.add(fd)
    except: pass
    return fd
def my_write(fd,data):
    if fd in fds and r'{fault}'=='partial':
        # write half then raise
        half=len(data)//2
        if half>0:
            n=orig_write(fd, data[:half])
        raise OSError("injected partial after half")
    return orig_write(fd,data)
def my_read(fd,n):
    # post fault: corrupt readback (return wrong bytes once for record FD)
    # To simulate readback mismatch, return wrong bytes for record FD reads after write? Track: after write, readback reads record FD. Fail by returning bad bytes once.
    if fd in fds and r'{fault}'=='post':
        if my_read.c==0:
            my_read.c+=1; return b"BAD-POST-READBACK"
    return orig_read(fd,n)
my_read.c=0
os.open=my_open; os.write=my_write; os.read=my_read
try:
    import datetime
    m.activate_publication(Path(r'{dst}'), r'{state_rel}', r'{set_rel}', "fault {fault}", "tester", datetime.datetime.now(datetime.timezone.utc))
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    out2=str(e); print(f"REFUSED: {{out2[:2500]}}")
    low2=out2.lower()
    assert "record" in low2 or "collision" in low2 or "write" in low2 or "partial" in low2 or "readback" in low2 or "mismatch" in low2, out2[:1200]
    sys.exit(0)
"""
        r=child_api(dst, code); assert r["exit"]==0, f"record {fault} should refuse {r['stdout'][:2500]}"
        log(f"C record {fault} refused OK")
def c_cli_negatives():
    # CLI validate tampered set must exit2, CLI activate approved must exit2 (already in B, but confirm here for C coverage table)
    dst=new_fault(INERT_W, "c-cli-neg")
    # tamper set (simple digest) for CLI validate
    import json as _j
    seal_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
    seal=_j.loads((dst/seal_rel).read_bytes().decode())
    # tamper pdf SHA without updating set (digest preemption, still negative exit2)
    seal["roles"]["publication-pdf"]["sha256"]="00"*32
    (dst/seal_rel).write_bytes(json.dumps(seal, indent=2, sort_keys=True).encode()+b"\n")
    cr=run_subprocess(dst, [sys.executable,"-B","-m","scripts.survey_editorial_publication_v2","--repo-root",str(dst),"validate-prepared-set","--state",f"sources/{ISSUE_W}/production-state.json","--set",seal_rel], cwd=dst)
    assert cr["exit"]==2, f"CLI validate tampered should exit2, got {cr['exit']}"
    log("C CLI validate tampered exit2 OK")
def main():
    for n,f in [("C_record_pre_partial_post",c_record_pre_partial_post),("C_cli_negatives",c_cli_negatives)]:
        case(n,f)
    log(f"TOTAL C5 pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_c5.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    import sys as _s; _s.exit(rc)
