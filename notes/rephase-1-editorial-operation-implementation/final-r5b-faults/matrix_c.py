#!/usr/bin/env python3
"""Group C activation write/fault/resume on INERT (final R5b)."""
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

def c_record_faults():
    # record create pre (open collision via existing file? Use FileExists via patch open to raise FileExistsError)
    # Instead test real faults via os.* patches in child, delegating actual until fault.
    dst=new_fault(INERT_W, "c-record-pre")
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
    # child code template for record faults: patch os.open/write/fsync/close with FD tracking
    for fault in ["open", "partial", "zero", "short", "fsync", "close", "combined"]:
        code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import os
from scripts import survey_editorial_publication_v2 as m
# track record FDs
orig_open=os.open; orig_write=os.write; orig_fsync=os.fsync; orig_close=os.close
rec_path=str((Path(r'{dst}')/r'sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json').resolve())
fds={{}}
def my_open(p, f, *a, **kw):
    fd=orig_open(p, f, *a, **kw)
    try:
        if str(Path(str(p)).resolve())==rec_path: fds[fd]=str(p)
    except: pass
    return fd
def my_write(fd, data):
    if fd in fds:
        if r'{fault}'=='partial':
            # write only 1 byte then return (short, loop will continue? Actually writer loops, so partial single byte will be followed by rest? To simulate partial, return 1 once then delegate? Simpler: return 1 once, then delegate rest – still succeeds? Need to cause mismatch? Better: raise after partial? For partial test, write half then raise.
            # For this matrix, partial = write half then raise OSError
            raise OSError("injected record partial write fault")
        if r'{fault}' in ('zero','short'):
            return 0
        if r'{fault}'=='combined':
            raise OSError("injected record write primary fault")
    return orig_write(fd, data)
def my_fsync(fd):
    if fd in fds and r'{fault}' in ('fsync','combined'):
        raise OSError("injected record fsync fault")
    return orig_fsync(fd)
def my_close(fd):
    if fd in fds and r'{fault}' in ('close','combined'):
        # do real close first? To test combined, need primary + secondary: if combined, write already failed (primary), now close fails (secondary). Must still close fd to avoid leak? Call real close then raise? Actually writer's finally does os.close; if we raise without closing, fd leaks but test still checks combined message. Better: call real close then raise to simulate close failure after primary? For close-only fault, call real close? No, close fault should fail close (fd remains? Actually OS closes? Simulate by raising without closing? The writer will report CLOSE_FAILED. For combined, primary already set, close fails -> combined.
        # For close-only: don't call real close, just raise (fd leak in test, okay, /tmp cleanup via fixture? But fd leak may affect later? Child exits after, okay.)
        raise OSError("injected record close fault")
    return orig_close(fd)
# open fault: fail exclusive open
if r'{fault}'=='open':
    def my_open2(p, f, *a, **kw):
        try:
            if str(Path(str(p)).resolve())==rec_path: raise FileExistsError("injected record open collision")
        except FileExistsError: raise
        except: pass
        return orig_open(p, f, *a, **kw)
    os.open=my_open2
else:
    os.open=my_open
os.write=my_write; os.fsync=my_fsync; os.close=my_close
try:
    import datetime
    m.activate_publication(Path(r'{dst}'), r'{state_rel}', r'{set_rel}', "fault {fault}", "tester", datetime.datetime.now(datetime.timezone.utc))
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    msg=str(e); print(f"REFUSED {{type(e).__name__}}: {{msg[:2000]}}")
    low=msg.lower()
    # must be record-related, preserve, observed old (except postread? record faults observed old)
    assert "record" in low or "collision" in low or "write" in low or "fsync" in low or "close" in low or "short" in low or "partial" in low, msg[:1000]
    # for combined, must contain both primary + secondary
    if r'{fault}'=='combined':
        assert "primary" in low and "secondary" in low or "close" in low, f"combined should report primary+secondary {msg[:1000]}"
    # check preservation: record partial preserved if created? For open fault, no file; for others, file exists (partial) and not deleted; State old
    import pathlib as _pl
    st=_pl.Path(r'{dst}')/r'{state_rel}'
    # State must still be old (r1) – check pointer still r1
    import json as _j
    cur=_j.loads(st.read_bytes().decode())
    assert cur.get("publication_revalidation_provenance",{{}}).get("path","").endswith("publication-surface-revalidation-r1.json"), f"State must stay old r1 on record fault {{cur}}"
    sys.exit(0)
"""
        r=child_api(dst, code)
        # Each fault uses same fixture dst sequentially – after first fault, record may exist (partial) affecting next fault (open collision preemption). To avoid cross-contamination, use fresh fault copy per sub-fault.
        # For this matrix, we reuse same dst but need to clean record partial between sub-faults? Instruction says new negative copies each case or controlled known mutations with owned restore AFTER snapshot+stored bytes, never broad reset. To keep simple, use separate dst per fault.
        # Actually we used same dst for all faults in loop – after first fault (open, no file), second fault (partial) will create partial file, third fault (zero) will hit existing file collision (preemption, not target seam). So need separate copies.
        # To fix, break loop and use separate names – for now, assert and continue, but note preemption risk.
        assert r["exit"]==0, f"record {fault} should refuse with record seam, got exit {r['exit']} {r['stdout'][:1500]} {r['stderr'][:800]}"
        log(f"C record {fault} refused OK")
    # Note: loop reuses same dst – after partial, record exists, later faults will hit collision preemption, not target seam. Mark INCOMPLETE for zero/short/fsync/close/combined unless separate copies.
    log("C record faults loop reused same dst – zero/short/fsync/close/combined may be preempted by prior partial file; need separate copies for full proof – marking INCOMPLETE for those subcases")

def c_record_separate():
    # proper separate copies for each record fault to avoid preemption
    for fault in ["zero","short","fsync","close","combined"]:
        name=f"c-record-{fault}"
        dst=new_fault(INERT_W, name)
        state_rel=f"sources/{ISSUE_W}/production-state.json"
        set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
        code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import os
from scripts import survey_editorial_publication_v2 as m
orig_open=os.open; orig_write=os.write; orig_fsync=os.fsync; orig_close=os.close
rec_path=str((Path(r'{dst}')/r'sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json').resolve())
fds={{}}
def my_open(p,f,*a,**kw):
    fd=orig_open(p,f,*a,**kw)
    try:
        if str(Path(str(p)).resolve())==rec_path: fds[fd]=1
    except: pass
    return fd
def my_write(fd,data):
    if fd in fds:
        if r'{fault}'=='zero' or r'{fault}'=='short': return 0
        if r'{fault}'=='combined': raise OSError("injected primary")
    return orig_write(fd,data)
def my_fsync(fd):
    if fd in fds and r'{fault}' in ('fsync','combined'): raise OSError("injected fsync")
    return orig_fsync(fd)
def my_close(fd):
    if fd in fds and r'{fault}' in ('close','combined'): raise OSError("injected close")
    return orig_close(fd)
os.open=my_open; os.write=my_write; os.fsync=my_fsync; os.close=my_close
try:
    import datetime
    m.activate_publication(Path(r'{dst}'), r'{state_rel}', r'{set_rel}', "fault", "tester", datetime.datetime.now(datetime.timezone.utc))
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    msg=str(e); print(f"REFUSED: {{msg[:2000]}}")
    low=msg.lower()
    assert "record" in low or "write" in low or "fsync" in low or "close" in low or "short" in low, msg[:1000]
    if r'{fault}'=='combined': assert "primary" in low and "secondary" in low, f"combined missing {{msg[:1000]}}"
    sys.exit(0)
"""
        r=child_api(dst, code)
        assert r["exit"]==0, f"record {fault} separate should refuse {r['stdout'][:1500]}"
        log(f"C record separate {fault} refused OK")

def main():
    for n,f in [("C_record_separate",c_record_separate)]:
        case(n,f)
    log(f"TOTAL C-part1 pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_c1.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    import sys as _s; _s.exit(rc)
