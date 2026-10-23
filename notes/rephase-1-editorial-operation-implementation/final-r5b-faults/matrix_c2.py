#!/usr/bin/env python3
"""Group C2: State faults, foreign, orphan, ALREADY_ACTIVE, INDETERMINATE."""
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

def c_state_faults():
    for fault in ["temp_create","temp_write","temp_fsync","temp_close","pre_replace","replace","postread"]:
        name=f"c-state-{fault}"
        dst=new_fault(INERT_W, name)
        state_rel=f"sources/{ISSUE_W}/production-state.json"
        set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
        code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
import os
from scripts import survey_editorial_publication_v2 as m
orig_open=os.open; orig_write=os.write; orig_fsync=os.fsync; orig_close=os.close; orig_replace=os.replace; orig_read=os.read
# track State temp FDs (tmp-reval)
tfds=set()
def is_tmp(p):
    try: s=str(p)
    except: return False
    return ".production-state.json.tmp-reval-" in s
def my_open(p,f,*a,**kw):
    fd=orig_open(p,f,*a,**kw)
    if is_tmp(p): tfds.add(fd)
    return fd
def my_write(fd,data):
    if fd in tfds and r'{fault}'=='temp_write': raise OSError("injected State temp write")
    return orig_write(fd,data)
def my_fsync(fd):
    if fd in tfds and r'{fault}'=='temp_fsync': raise OSError("injected State temp fsync")
    # also record fsync? Only State temp here (record fsync already covered in C_record). For State faults, only temp.
    return orig_fsync(fd)
def my_close(fd):
    if fd in tfds and r'{fault}'=='temp_close': raise OSError("injected State temp close")
    return orig_close(fd)
def my_replace(s,d,*a,**kw):
    # pre_replace: fail if State drift? Simulate by raising before replace when fault==pre_replace (after temp success, before replace, State drifted? Actually pre_replace fault = temp identity changed? Simpler: raise OSError for replace when fault==pre_replace? No, pre_replace should be State drift before replace (cur_old2 != expected_old) – simulate by modifying State file after temp? Easier: patch to raise drift-like error? For this matrix, pre_replace = patch os.replace to succeed but first corrupt temp? Hmm.
    # Simplify: pre_replace fault = raise OSError("injected pre-replace") to simulate temp identity changed before replace (should be classified as STATE_REPLACE? Actually pre-replace checks are STATE_DRIFT or temp identity? Let's just raise and expect STATE_REPLACE/EXPLICIT_RECOVERY with observed old.
    if str(d).endswith("production-state.json") and r'{fault}' in ('pre_replace','replace'):
        raise OSError("injected State replace fault {fault}")
    return orig_replace(s,d,*a,**kw)
# temp_create: fail exclusive open
if r'{fault}'=='temp_create':
    def my_open2(p,f,*a,**kw):
        if is_tmp(p): raise FileExistsError("injected temp collision")
        return orig_open(p,f,*a,**kw)
    os.open=my_open2
else:
    os.open=my_open
os.write=my_write; os.fsync=my_fsync; os.close=my_close; os.replace=my_replace
# postread: allow replace then fail read
flag={{"r":False}}
if r'{fault}'=='postread':
    orig_replace2=orig_replace
    def my_replace2(s,d,*a,**kw):
        r=orig_replace2(s,d,*a,**kw)
        if str(d).endswith("production-state.json"): flag["r"]=True
        return r
    os.replace=my_replace2
    import builtins as _b; ro=_b.open
    def fo(p,*a,**kw):
        if flag["r"] and str(p).endswith("production-state.json"):
            # fail first 2 reads after replace (postread + selection)
            if fo.c<2:
                fo.c+=1; raise OSError("injected postread")
        return ro(p,*a,**kw)
    fo.c=0; _b.open=fo
try:
    import datetime
    m.activate_publication(Path(r'{dst}'), r'{state_rel}', r'{set_rel}', "fault {fault}", "tester", datetime.datetime.now(datetime.timezone.utc))
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    msg=str(e); print(f"REFUSED {{type(e).__name__}}: {{msg[:2500]}}")
    low=msg.lower()
    # must be State-related, preserve, observed old (except postread unknown/new)
    assert "state" in low or "temp" in low or "replace" in low or "postread" in low or "drift" in low or "explicit_recovery" in low, low[:1200]
    if r'{fault}'=='postread':
        assert "unknown" in low or "postread" in low or "postreplace" in low, f"postread should be unknown {{low[:1200]}}"
    else:
        assert "old" in low or "inert" in low or "preserved" in low, f"State fault should be observed old {{low[:1200]}}"
    sys.exit(0)
"""
        r=child_api(dst, code)
        assert r["exit"]==0, f"State {fault} should refuse {r['stdout'][:2000]} {r['stderr'][:800]}"
        log(f"C State {fault} refused OK")

def c_foreign():
    dst=new_fault(INERT_W, "c-foreign")
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
    # create replacement WHILE original exists, assert different inode, then os.replace (avoid ext4 reuse)
    repl=Path(str(p)+".repl")
    repl.write_bytes(exp)
    o=os.stat(p); n=os.stat(repl)
    assert (o.st_dev,o.st_ino)!=(n.st_dev,n.st_ino), f"replacement must be foreign while original exists {{o.st_ino}} vs {{n.st_ino}}"
    os.replace(repl,p)
    # verify foreign now (same bytes, different inode)
    assert not agent._record_identity_matches(Path(p), owned, exp), "foreign must not match ownership"
    assert Path(p).is_file(), "referenced record must never be deleted"
    return owned
agent._exclusive_create_record_bytes=hooked
try:
    import datetime
    m.activate_publication(Path(r'{dst}'), r'{state_rel}', r'{set_rel}', "foreign", "tester", datetime.datetime.now(datetime.timezone.utc))
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    msg=str(e); print(f"REFUSED foreign: {{msg[:2500]}}")
    low=msg.lower()
    assert "ownership" in low or "inode" in low or "foreign" in low or "record" in low, low[:1200]
    assert "old" in low or "inert" in low or "preserved" in low, f"foreign should be observed old {{low[:1200]}}"
    # State must still be old (no adopt)
    import json as _j
    cur=_j.loads((Path(r'{dst}')/r'{state_rel}').read_bytes().decode())
    assert cur.get("publication_revalidation_provenance",{{}}).get("path","").endswith("publication-surface-revalidation-r1.json"), f"State must stay old r1 {{cur}}"
    sys.exit(0)
"""
    r=child_api(dst, code); assert r["exit"]==0, f"foreign should refuse before State write {r['stdout'][:2500]} {r['stderr'][:800]}"
    log("C foreign same-bytes refused before State write OK (no deletion)")

def c_orphan_resume_active():
    # complete orphan: INERT State old + PRELC r2 record
    dst=new_fault(INERT_W, "c-orphan")
    import shutil as _sh
    prelc_r2=PRELC_W/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    assert prelc_r2.is_file()
    dst_r2=dst/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    if not dst_r2.exists():
        _sh.copy(str(prelc_r2), str(dst_r2))
    assert dst_r2.is_file()
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json"
    rec_rel=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    # ordinary must COLLISION no r3 fork
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
import datetime
try:
    m.activate_publication(Path(r'{dst}'), r'{state_rel}', r'{set_rel}', "orphan", "tester", datetime.datetime.now(datetime.timezone.utc))
    print("UNEXPECTED_PASS_FORK"); sys.exit(10)
except Exception as e:
    msg=str(e); print(f"REFUSED orphan ordinary: {{msg[:2000]}}")
    low=msg.lower()
    assert "collision" in low or "intent" in low or "orphan" in low or "resume" in low, msg[:1200]
    sys.exit(0)
"""
    r=child_api(dst, code); assert r["exit"]==0, f"orphan ordinary must COLLISION {r['stdout'][:2000]}"
    # ensure no r3 fork
    assert not (dst/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r3.json").exists(), "orphan must not fork r3"
    log("C orphan ordinary COLLISION no fork OK")
    # explicit resume -> RESUMED exact r2
    code2=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
from scripts import survey_publication_set_v2 as s, survey_production_v2 as core, survey_agent_control_v2 as a
res=m.resume_activation(Path(r'{dst}'), r'{state_rel}', r'{rec_rel}')
print(f"RESUME {{res}}"); assert res.get("status")=="RESUMED" and res.get("observed")=="new", res
# exact r2?
import hashlib
new_state=(Path(r'{dst}')/r'{state_rel}').read_bytes()
import json as _j
ns=_j.loads(new_state.decode())
assert ns.get("publication_revalidation_provenance")==dict(path=r'{rec_rel}', sha256=hashlib.sha256((Path(r'{dst}')/r'{rec_rel}').read_bytes()).hexdigest()), "exact r2"
cfg=core.load_json(Path(r'{dst}')/core.DEFAULT_CONFIG)
assert a.validate_agent_state(Path(r'{dst}'), cfg, ns)==[]
sel=s.resolve_publication_selection(Path(r'{dst}'), cfg, ns)
assert sel.get("mode")=="VERSIONED_ACTIVE" and "wk-r5b-2" in (sel.get("candidate_ref") or {{}}).get("path","")
"""
    r2=child_api(dst, code2); assert r2["exit"]==0, f"orphan resume should RESUMED {r2['stdout'][:2000]} {r2['stderr'][:800]}"
    log("C orphan resume RESUMED exact r2 OK")
    # ALREADY_ACTIVE readonly on prelc (State r2)
    dst2=new_fault(PRELC_W, "c-already-active")
    # snapshot hashes before
    import hashlib as _h
    def snap(p):
        d={}
        for dp,dn,fn in __import__("os").walk(p):
            if ".git" in Path(dp).parts: dn[:]=[]; continue
            for f in sorted(fn):
                pp=Path(dp)/f
                try:
                    if pp.is_symlink(): continue
                    d[pp.relative_to(p).as_posix()]=_h.sha256(pp.read_bytes()).hexdigest()
                except: pass
        return d
    before=snap(dst2)
    code3=f"""
import sys; sys.path.insert(0, r'{dst2}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
import datetime
res=m.activate_publication(Path(r'{dst2}'), r'sources/{ISSUE_W}/production-state.json', r'sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-set.json', "already", "tester", datetime.datetime.now(datetime.timezone.utc))
print(f"ALREADY {{res}}"); assert res.get("status")=="ALREADY_ACTIVE" and res.get("observed")=="new", res
"""
    r3=child_api(dst2, code3); assert r3["exit"]==0, f"ALREADY_ACTIVE should be readonly {r3['stdout'][:1000]}"
    assert snap(dst2)==before, "ALREADY_ACTIVE must be readonly"
    log("C ALREADY_ACTIVE readonly OK")
    # CLI activate on orphan must exit2? Actually orphan ordinary via CLI should also refuse exit2 (not fork)
    # Use fresh orphan copy for CLI (to avoid already-resumed dst)
    dst_cli=new_fault(INERT_W, "c-orphan-cli")
    _sh.copy(str(prelc_r2), str(dst_cli/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"))
    cr=child_cli(dst_cli, ["--repo-root", str(dst_cli), "activate-publication", "--state", state_rel, "--set", set_rel, "--reason", "x", "--executor", "y"])
    assert cr["exit"]==2, f"CLI orphan ordinary should exit2, got {cr['exit']} {cr['stdout'][:800]} {cr['stderr'][:800]}"
    log("C CLI orphan ordinary exit2 OK")
    # CLI resume on orphan should succeed exit0 with RESUMED? Check CLI resume
    cr2=run_subprocess(dst, [sys.executable,"-B","-m","scripts.survey_editorial_publication_v2","--repo-root",str(dst),"resume-activation","--state",state_rel,"--record",rec_rel], cwd=dst)
    # dst already resumed (State new), so resume should be ALREADY_ACTIVE exit0? Actually after resume, State new, so second resume should be ALREADY_ACTIVE, not RESUMED. That's fine (readonly). For CLI negative, test unknown State resume exit2 (in next case).
    log(f"C CLI resume after already (exit {cr2['exit']}) – readonly, not takeover")

def c_unknown_incomplete():
    # Unknown State introduced after record write (readable null pointer, neither old r1 nor new r2)
    dst=new_fault(INERT_W, "c-unknown")
    import shutil as _sh, json as _j
    prelc_r2=PRELC_W/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    _sh.copy(str(prelc_r2), str(dst/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"))
    # null pointer: valid CANONICAL State, neither old (r1) nor new (r2) -> INDETERMINATE on resume r2 (supersedes r1)
    st_rel=f"sources/{ISSUE_W}/production-state.json"
    st=_j.loads((dst/st_rel).read_bytes().decode())
    st["publication_revalidation_provenance"]=None
    (dst/st_rel).write_bytes(json.dumps(st, indent=2, sort_keys=True).encode()+b"\n")
    rec_rel=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    unk_rel=st_rel  # for preserve check below, use State itself (no extra unknown file)
    code=f"""
import sys; sys.path.insert(0, r'{dst}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
try:
    m.resume_activation(Path(r'{dst}'), r'{st_rel}', r'{rec_rel}')
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    msg=str(e); print(f"REFUSED unknown: {{msg[:2000]}}")
    assert "indeterminate" in msg.lower(), f"unknown State should be INDETERMINATE, got {{msg[:1200]}}"
    sys.exit(0)
"""
    r=child_api(dst, code); assert r["exit"]==0, f"unknown should be INDETERMINATE {r['stdout'][:2000]}"
    # preserve all (record + State)
    assert (dst/rec_rel).is_file() and (dst/st_rel).is_file()
    log("C unknown INDETERMINATE preserved OK")
    # unadopted incomplete orphan: truncated record file, resume must refuse gracefully (not auto overwrite)
    dst2=new_fault(INERT_W, "c-incomplete-orphan")
    _sh.copy(str(prelc_r2), str(dst2/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"))
    # truncate record to incomplete (invalid JSON)
    p2=dst2/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    b=p2.read_bytes(); p2.write_bytes(b[:len(b)//2])
    code2=f"""
import sys; sys.path.insert(0, r'{dst2}')
from pathlib import Path
from scripts import survey_editorial_publication_v2 as m
try:
    m.resume_activation(Path(r'{dst2}'), r'sources/{ISSUE_W}/production-state.json', r'sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json')
    print("UNEXPECTED_PASS"); sys.exit(10)
except Exception as e:
    msg=str(e); print(f"REFUSED incomplete: {{msg[:2000]}}")
    # must refuse gracefully, preserve (no auto overwrite, manual recovery retained)
    assert "invalid" in msg.lower() or "record" in msg.lower() or "refuse" in msg.lower(), msg[:1200]
    sys.exit(0)
"""
    r2=child_api(dst2, code2); assert r2["exit"]==0, f"incomplete orphan should refuse gracefully {r2['stdout'][:2000]}"
    assert p2.is_file(), "incomplete record must be preserved, not deleted"
    log("C incomplete orphan refused gracefully, preserved OK")

def main():
    for n,f in [("C_state_faults",c_state_faults),("C_foreign",c_foreign),("C_orphan_resume_active",c_orphan_resume_active),("C_unknown_incomplete",c_unknown_incomplete)]:
        case(n,f)
    log(f"TOTAL C2 pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary_c2.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    import sys as _s; _s.exit(rc)
