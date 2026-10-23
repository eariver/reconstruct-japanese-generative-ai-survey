#!/usr/bin/env python3
"""Worker D v3: reuse v1 complete before-record fixtures (no new full copies, quota-blocked).

Uses existing /tmp/opencode/jgas-faults-r3c-20261021T151500Z/fault-* (16M each, exact source 718,
independent inodes, inert origin) which are still clean before-record (v1 failed at P2V due to
FROZEN-import harness bug, before any fault injection). v3 loads modules per-fixture root
(correct runtime binding) and runs fault injection with real validators, no fake stubs.
Preserves all mutated copies, snapshots before/after, no cleanup before snapshot.
"""
from __future__ import annotations
import hashlib, json, os, subprocess, sys, time, traceback
from datetime import datetime, timezone
from pathlib import Path
sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
os.environ.setdefault("PYTHONPYCACHEPREFIX","/tmp/opencode/pycache-faults-v3")
for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
    if os.environ.get(_v): print(f"UNSAFE {_v}"); sys.exit(2)
def _log(m): print(m, flush=True)
V1BASE=Path("/tmp/opencode/jgas-faults-r3c-20261021T151500Z")
ISSUE_W="2026-W37"
def _run_git(cwd,*a):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
    return subprocess.run(["git",*a],cwd=str(cwd),capture_output=True,text=True,timeout=60,env=env)
def _load(root: Path):
    root=str(Path(root).resolve())
    sys.path=[p for p in sys.path if "jgas-faults" not in p and "jgas-editorial-r3c" not in p and "jgas-weekly" not in p]
    sys.path.insert(0,root)
    for m in list(sys.modules.keys()):
        if m=="scripts" or m.startswith("scripts."): del sys.modules[m]
    import importlib
    core=importlib.import_module("scripts.survey_production_v2")
    edpub=importlib.import_module("scripts.survey_editorial_publication_v2")
    setmod=importlib.import_module("scripts.survey_publication_set_v2")
    observer=importlib.import_module("scripts.survey_editorial_current_authority_v2")
    agent=importlib.import_module("scripts.survey_agent_control_v2")
    return core,edpub,setmod,observer,agent
def _snap(dst,label):
    sr=f"sources/{ISSUE_W}/production-state.json"; rr=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    try: b=(dst/sr).read_bytes(); sha=hashlib.sha256(b).hexdigest()[:16]; ptr=json.loads(b.decode()).get("publication_revalidation_provenance")
    except Exception as e: sha=f"UNREAD:{e}"; ptr=f"UNREAD:{e}"
    _log(f"SNAPSHOT {label} sha16={sha} ptr={ptr} rec2={(dst/rr).exists()}")
    return sha
PASS=0; FAIL=0; CASES=[]
def _case(n,fn):
    global PASS,FAIL
    t0=time.monotonic()
    try: fn(); dt=time.monotonic()-t0; _log(f"CASE PASS {n} dt={dt:.1f}s"); CASES.append((n,"PASS",dt,"")); PASS+=1
    except AssertionError as e: dt=time.monotonic()-t0; _log(f"CASE FAIL {n} dt={dt:.1f}s {e}"); traceback.print_exc(); CASES.append((n,"FAIL",dt,str(e))); FAIL+=1
    except Exception as e: dt=time.monotonic()-t0; _log(f"CASE BLOCKER {n} dt={dt:.1f}s {type(e).__name__}: {e}"); traceback.print_exc(); CASES.append((n,"BLOCKER",dt,f"{type(e).__name__}: {e}")); FAIL+=1
def _pre(dst):
    core,edpub,setmod,observer,agent=_load(dst)
    sr=f"sources/{ISSUE_W}/production-state.json"; srel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/publication/publication-set.json"
    pr=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/proposal.json"; str_=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/staged-source/staged-source-manifest.json"
    obs=observer.observe_current_authority(dst,dst/sr,dst/pr,dst/core.load_json(dst/str_)["retention_manifest_ref"]["path"],dst/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/scope-review-v2.json")
    assert obs.get("result")=="CURRENT_BASIS_OBSERVED_SCOPE_BOUND", obs
    assert edpub.validate_prepared_set(dst,sr,srel).get("issue_id")==ISSUE_W
    return core,edpub,setmod,observer,agent,sr,srel
def c_B7():
    dst=V1BASE/"fault-orphan-r2"
    assert dst.exists()
    core,edpub,setmod,observer,agent,sr,srel=_pre(dst)
    rec_rel=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    try:
        res=edpub.activate_publication(dst,sr,srel,"orphan","fault-exec",datetime.now(timezone.utc))
        # success means fork (r3) not collision -> BLOCKER
        import json as _j
        st=_j.loads((dst/sr).read_bytes().decode())
        ptr=st.get("publication_revalidation_provenance",{})
        _log(f"ORPHAN activate succeeded status={res.get('status')} ptr={ptr} -> fork, not collision")
        # check r3 exists?
        r3=dst/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r3.json"
        _log(f"r3 exists={r3.exists()} (fork evidence, preserved)")
        raise AssertionError(f"BLOCKER: ordinary activate on orphan (State old r1, record r2 exists) did NOT refuse RECORD_COLLISION; instead created {ptr.get('path')} (fork r3 with same set2, supersedes r1). Expected: refuse collision, require resume. Fired STATE_REPLACE (adopt) vs expected RECORD_COLLISION. Precise: survey_editorial_publication_v2.py:2836 _next_record_seq max+1 + os.lstat collision check only on next (r3), not orphan (r2). Earlier P2V/validate/retained/supersedes all passed.")
    except AssertionError as ae:
        if "BLOCKER" in str(ae): raise ae
        raise
    except Exception as e:
        assert "RECORD_COLLISION" in str(e) or "collision" in str(e).lower(), f"wrong seam {type(e).__name__}: {str(e)[:800]}"
        _log(f"ORPHAN refused collision as expected: {str(e)[:400]}")
def c_B1():
    dst=V1BASE/"fault-before-record-write"
    core,edpub,setmod,observer,agent,sr,srel=_pre(dst)
    import builtins; ro=builtins.open
    rec_abs=(dst/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json").resolve()
    def f(p,*a,**kw):
        try: q=Path(str(p)).resolve()
        except: q=None
        if q==rec_abs and ("x" in (a[0] if a else kw.get("mode","")) or "x" in str(a)+str(kw)): raise OSError("injected record-write")
        return ro(p,*a,**kw)
    builtins.open=f
    try:
        try: edpub.activate_publication(dst,sr,srel,"fault","fault-exec",datetime.now(timezone.utc)); raise AssertionError("should fail")
        except Exception as e: assert "RECORD_COLLISION" in str(e) or "injected record-write" in str(e), f"wrong {str(e)[:800]}"; _log(f"RECORD-WRITE classified: {str(e)[:500]}")
    finally: builtins.open=ro
    _snap(dst,"record-write")
def c_B2():
    dst=V1BASE/"fault-state-temp-write"
    core,edpub,setmod,observer,agent,sr,srel=_pre(dst)
    import builtins; ro=builtins.open
    def f2(p,*a,**kw):
        if ".production-state.json.tmp-reval-" in str(p) and "x" in str(a[0] if a else kw.get("mode","")): raise OSError("injected temp")
        return ro(p,*a,**kw)
    builtins.open=f2
    try:
        try: edpub.activate_publication(dst,sr,srel,"fault","fault-exec",datetime.now(timezone.utc)); raise AssertionError("should fail")
        except Exception as e: assert "STATE_REPLACE" in str(e) or "injected temp" in str(e) or "EXPLICIT_RECOVERY" in str(e), f"wrong {str(e)[:800]}"; _log(f"TEMP classified: {str(e)[:600]}")
    finally: builtins.open=ro
    _snap(dst,"temp")
def c_B3():
    dst=V1BASE/"fault-state-replace"
    core,edpub,setmod,observer,agent,sr,srel=_pre(dst)
    rr=os.replace
    def fr(s,d,*a,**kw):
        if str(d).endswith("production-state.json"): raise OSError("injected replace")
        return rr(s,d,*a,**kw)
    os.replace=fr
    try:
        try: edpub.activate_publication(dst,sr,srel,"fault","fault-exec",datetime.now(timezone.utc)); raise AssertionError("should fail")
        except Exception as e: assert "STATE_REPLACE" in str(e), f"wrong {str(e)[:800]}"; _log(f"REPLACE classified: {str(e)[:600]}")
    finally: os.replace=rr
    _snap(dst,"replace")
def c_B4():
    dst=V1BASE/"fault-postread"
    core,edpub,setmod,observer,agent,sr,srel=_pre(dst)
    rr=os.replace; fl={"r":False}
    def fr2(s,d,*a,**kw):
        r=rr(s,d,*a,**kw)
        if str(d).endswith("production-state.json"): fl["r"]=True
        return r
    import builtins; ro=builtins.open
    def fo(p,*a,**kw):
        if fl["r"] and str(p).endswith("production-state.json") and fo.c<3: fo.c+=1; raise OSError("injected postread")
        return ro(p,*a,**kw)
    fo.c=0; os.replace=fr2; builtins.open=fo
    try:
        try: edpub.activate_publication(dst,sr,srel,"fault","fault-exec",datetime.now(timezone.utc)); raise AssertionError("should fail")
        except Exception as e: assert "POSTREAD" in str(e) or "POSTREPLACE" in str(e) or "observed unknown" in str(e).lower(), f"wrong {str(e)[:1000]}"; _log(f"POSTREAD classified: {str(e)[:700]}")
    finally: os.replace=rr; builtins.open=ro
    _snap(dst,"postread")
def c_B5():
    dst=V1BASE/"fault-fsync"
    # fault-fsync v1 dir? Check exists, else use before-record-write? Actually v1 has fault-fsync? List shows fault-fsync exists (16M). Use it.
    assert (V1BASE/"fault-fsync").exists(), "fault-fsync missing"
    dst=V1BASE/"fault-fsync"
    core,edpub,setmod,observer,agent,sr,srel=_pre(dst)
    rf=os.fsync; os.fsync=lambda fd: (_ for _ in ()).throw(OSError("injected fsync"))
    try:
        try:
            res=edpub.activate_publication(dst,sr,srel,"fsync","fault-exec",datetime.now(timezone.utc))
            _log(f"FSYNC swallowed succeeded {res}")
            raise AssertionError("BLOCKER: os.fsync failure swallowed (pass) in _exclusive_create_record_bytes:1941 and _atomic_replace_state_bytes:2008; no primary/secondary/observed. Need root disposition explicit non-guarantee or classification.")
        except AssertionError as ae:
            if "BLOCKER" in str(ae): raise ae
            raise
        except Exception as e: raise AssertionError(f"fsync unexpectedly classified {str(e)[:500]}")
    finally: os.fsync=rf
def c_B8():
    # use fault-foreign-inode v1 (clean before-record)
    dst=V1BASE/"fault-foreign-inode"
    core,edpub,setmod,observer,agent,sr,srel=_pre(dst)
    rex=agent._exclusive_create_record_bytes
    def hooked(p,exp,label):
        o=rex(p,exp,label); cur=Path(p).read_bytes(); assert cur==exp; old=os.stat(p); Path(p).unlink(); Path(p).write_bytes(exp); new=os.stat(p); _log(f"FOREIGN swap {old.st_ino}->{new.st_ino}"); return o
    agent._exclusive_create_record_bytes=hooked
    try:
        try:
            res=edpub.activate_publication(dst,sr,srel,"foreign","fault-exec",datetime.now(timezone.utc))
            _log(f"FOREIGN succeeded {res}")
            raise AssertionError("BLOCKER: _exclusive_create returns owned (dev,ino) but record_owned_id never checked via _record_identity_matches before _atomic_replace_state_bytes; same-bytes foreign inode adopts State (should refuse ownership). Fired STATE_REPLACE vs expected OWNERSHIP. File survey_editorial_publication_v2.py:2990-2992, agent_control_v2.py:1963.")
        except AssertionError as ae:
            if "BLOCKER" in str(ae): raise ae
            raise
        except Exception as e:
            if "ownership" in str(e).lower() or "identity" in str(e).lower(): _log(f"FOREIGN correctly refused: {str(e)[:600]}")
            else: raise AssertionError(f"foreign refused unclear seam: {type(e).__name__}: {str(e)[:800]}")
    finally: agent._exclusive_create_record_bytes=rex
    _snap(dst,"foreign")
def main():
    import sys
    _log(f"CMD={' '.join(sys.argv)} CWD={Path.cwd()} V1BASE={V1BASE}")
    for n,f in [("B7_orphan_fork_BLOCKER",c_B7),("B1_record_write",c_B1),("B2_temp",c_B2),("B3_replace",c_B3),("B4_postread",c_B4),("B5_fsync_BLOCKER",c_B5),("B8_foreign_BLOCKER",c_B8)]:
        _case(n,f)
    _log(f"TOTAL pass={PASS} fail={FAIL}")
    for n,s,d,det in CASES: _log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    Path("notes/rephase-1-editorial-operation-implementation/verify-faults-r3c-20261021T151500Z/summary-v3.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s} for n,s,_,_ in CASES]}, indent=2))
    print(f"EXIT:{0 if FAIL==0 else 2}"); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    sys.exit(rc)
