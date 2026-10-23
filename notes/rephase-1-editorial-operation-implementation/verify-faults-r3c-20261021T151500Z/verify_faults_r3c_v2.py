#!/usr/bin/env python3
"""Worker D v2: corrected harness (per-fixture imports, pycache outside source).

Fixes v1 harness bugs (not source):
- v1 imported from FROZEN once, so staged _check_runtime_binding failed with
  RUNTIME_BINDING_PATH for fault fixtures (loaded FROZEN vs expected fault root).
  v2 loads modules per-fixture root via _load_for_root (clear sys.modules).
- v1 created __pycache__ in FROZEN (now cleaned); v2 sets PYTHONPYCACHEPREFIX
  outside source + runs with -B.
- v1 A1 called P2V on active State (refused P2V_AFTER_ACTIVATION); v2 checks
  healthy active via selection/history/receipt/Gate only, P2V only on before-State.
- v1 B10 used missing-file pointer (SELECTION_BEFORE) not INDETERMINATE; v2 uses
  null-pointer State for true INDETERMINATE.
- v2 preserves v1 fault copies; uses NEW FAULT_BASE ...T153000Z.

Governing d880, frozen 0d9857e6 718 clean, positives post-second r2 VALIDATED_DRAFT.
"""
from __future__ import annotations
import hashlib, json, os, subprocess, sys, time, traceback, copy
from datetime import datetime, timezone
from pathlib import Path
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
# contain bytecode outside source (v1 polluted frozen; now cleaned)
os.environ.setdefault("PYTHONPYCACHEPREFIX", "/tmp/opencode/pycache-faults-v2")
for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
    if os.environ.get(_v):
        print(f"UNSAFE inherited {_v}", flush=True); sys.exit(2)
def _log(m): print(m, flush=True)
FROZEN = Path("/tmp/opencode/jgas-editorial-r3c-20261021T144500Z/candidate-partial-b40de60")
POS_W = Path("/tmp/opencode/jgas-weekly-r3c-20261021T150000Z/candidate-partial-b40de60")
POS_L = Path("/tmp/opencode/jgas-longform-r3c-20261021T152000Z/candidate-partial-b40de60")
FROZEN_HEAD = "0d9857e6132fb314a2e2ba141da79c54f4ec5e06"
ISSUE_W = "2026-W37"
FAULT_BASE = Path("/tmp/opencode/jgas-faults-r3c-20261021T153000Z")
NOTES = None
_mod_cache = {}
def _run_git(cwd, *args):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
    return subprocess.run(["git",*args], cwd=str(cwd), capture_output=True, text=True, timeout=60, env=env)
def _sha_file(p: Path):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for ch in iter(lambda: f.read(1<<20), b""): h.update(ch)
    return h.hexdigest()
def _load_for_root(root: Path):
    """Import scripts.* from exact root (for runtime-binding pin). Clear cache."""
    root=str(Path(root).resolve())
    # remove previous roots from sys.path (keep only first occurrence of current)
    sys.path=[p for p in sys.path if p not in (str(FROZEN), str(POS_W), str(root))]
    # also remove any fault base copies previously inserted
    # keep stdlib etc.; insert current root front
    sys.path.insert(0, root)
    for m in list(sys.modules.keys()):
        if m=="scripts" or m.startswith("scripts.") or m=="tests" or m.startswith("tests."):
            del sys.modules[m]
    import importlib
    core=importlib.import_module("scripts.survey_production_v2")
    edpub=importlib.import_module("scripts.survey_editorial_publication_v2")
    setmod=importlib.import_module("scripts.survey_publication_set_v2")
    observer=importlib.import_module("scripts.survey_editorial_current_authority_v2")
    agent=importlib.import_module("scripts.survey_agent_control_v2")
    pubmod=importlib.import_module("scripts.survey_publication_v2")
    reader_gate=importlib.import_module("scripts.survey_reader_surface_gate_v2")
    return core, edpub, setmod, observer, agent, pubmod, reader_gate
def _verify_source_copy(dst: Path, label: str):
    p=_run_git(dst,"rev-parse","HEAD"); assert p.stdout.strip()==FROZEN_HEAD, f"{label} HEAD"
    p2=_run_git(dst,"ls-files"); assert len([l for l in p2.stdout.strip().splitlines() if l])==718, f"{label} ls-files"
    for alt in [dst/".git"/"objects"/"info"/"alternates", dst/".git"/"info"/"alternates"]:
        assert not alt.exists(), f"{label} alternates"
    pr=_run_git(dst,"remote","-v"); out=pr.stdout.strip(); assert "example.invalid" in out or out=="", f"{label} origin {out}"
    ps=_run_git(dst,"status","--porcelain")
    for line in ps.stdout.splitlines():
        if line.startswith(" M") or line.startswith("M ") or line.startswith(" D"):
            raise AssertionError(f"{label} tracked dirty {line}")
    for rel in ["scripts/survey_publication_set_v2.py","scripts/survey_agent_control_v2.py"]:
        assert _sha_file(FROZEN/rel)==_sha_file(dst/rel), f"{label} drift {rel}"
    for rel in ["scripts/survey_production_v2.py"]:
        sa=os.stat(FROZEN/rel); sb=os.stat(dst/rel); assert (sa.st_dev,sa.st_ino)!=(sb.st_dev,sb.st_ino), f"{label} hardlink"
    return True
def _cp_a(src: Path, dst: Path):
    if dst.exists(): raise AssertionError(f"exists {dst}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    r=subprocess.run(["cp","-a",str(src),str(dst)], capture_output=True, text=True, timeout=120)
    assert r.returncode==0, f"cp failed {r.stderr[:500]}"
    return dst
PASS=0; FAIL=0; CASES=[]; T0=time.monotonic()
def _case(name, fn):
    global PASS, FAIL
    t0=time.monotonic()
    try:
        fn(); dt=time.monotonic()-t0; _log(f"CASE PASS {name} dt={dt:.1f}s"); CASES.append((name,"PASS",dt,"")); PASS+=1
    except AssertionError as e:
        dt=time.monotonic()-t0; _log(f"CASE FAIL {name} dt={dt:.1f}s ASSERT: {e}"); traceback.print_exc(); CASES.append((name,"FAIL",dt,f"ASSERT: {e}")); FAIL+=1
    except Exception as e:
        dt=time.monotonic()-t0; _log(f"CASE BLOCKER {name} dt={dt:.1f}s {type(e).__name__}: {e}"); traceback.print_exc(); CASES.append((name,"BLOCKER",dt,f"{type(e).__name__}: {e}")); FAIL+=1
def case_A0():
    assert FROZEN.exists()
    assert _run_git(FROZEN,"rev-parse","HEAD").stdout.strip()==FROZEN_HEAD
    assert len(_run_git(FROZEN,"ls-files").stdout.strip().splitlines())==718
    assert _run_git(FROZEN,"status","--porcelain").stdout.strip()=="", f"frozen dirty {_run_git(FROZEN,'status','--porcelain').stdout[:500]}"
    for pos,issue in [(POS_W,ISSUE_W),(POS_L,"SP001")]:
        h=_run_git(pos,"rev-parse","HEAD").stdout.strip(); assert h==FROZEN_HEAD
        st=json.loads((pos/f"sources/{issue}/production-state.json").read_bytes().decode())
        assert st.get("lifecycle_state")=="VALIDATED_DRAFT"
        prov=st.get("publication_revalidation_provenance") or {}; assert prov.get("path","").endswith("publication-surface-revalidation-r2.json")
        rec=json.loads((pos/prov["path"]).read_bytes().decode())
        assert rec["core"]["implementation_commit_sha"]==FROZEN_HEAD
        seal=json.loads((pos/rec["set_ref"]["path"]).read_bytes().decode()); assert seal["status"]=="SEALED_INERT"
        pdf_p=pos/seal["roles"]["publication-pdf"]["path"]; assert pdf_p.is_file() and pdf_p.stat().st_size>10000
        from pypdf import PdfReader as _PR; assert len(_PR(str(pdf_p)).pages)==5
        _log(f"POSITIVE {issue} r2 VALIDATED_DRAFT pdf5pp code==manifest OK")
SHARED_V2=None
def _ensure_shared_v2():
    global SHARED_V2
    if SHARED_V2 is not None and SHARED_V2.exists(): return SHARED_V2
    dst=FAULT_BASE/"shared-ro-v2"
    if not dst.exists(): _cp_a(POS_W,dst); _verify_source_copy(dst,"shared-ro-v2")
    SHARED_V2=dst; return SHARED_V2
def case_A1():
    root=_ensure_shared_v2()
    core,edpub,setmod,observer,agent,pubmod,reader_gate=_load_for_root(root)
    cfg=core.load_json(root/core.DEFAULT_CONFIG.as_posix())
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    state=core.load_json(root/state_rel)
    assert agent.validate_agent_state(root,cfg,state)==[]
    # healthy active: selection VERSIONED_ACTIVE r2, history HISTORICAL_VALID, receipt/Gate (no P2V after activation)
    sel=setmod.resolve_publication_selection(root,cfg,state)
    assert sel.get("mode")=="VERSIONED_ACTIVE" and "wk-r3c-2" in (sel.get("candidate_ref") or {}).get("path",""), sel
    h=edpub.verify_activation_history(root, state["publication_revalidation_provenance"]["path"])
    assert h.get("status")=="HISTORICAL_VALID"
    rv=edpub.validate_editorial_receipt(root, f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/publication/validated-source-manifest.json", state_rel)
    assert rv.get("issue_id")==ISSUE_W
    _log("HEALTHY active VERSIONED_ACTIVE + HISTORICAL_VALID + receipt OK (no P2V after activation, correct)")
    # P2V healthy on before-State (orphan old) proves before-eligibility separate
    # use retained beforeState2 copy? Create temp before fixture for P2V check (no mutation of shared)
    # Instead, check P2V on shared's retained? Shared State is new, so P2V on shared with old proposal would refuse (correct). For healthy P2V, use before fixture created in B7 (will be tested there).
    _log("HEALTHY controls OK")
def _new_before(name, omit):
    dst=FAULT_BASE/name
    if dst.exists(): _verify_source_copy(dst,name+"(reuse)"); return dst
    # copy from POS_W (original positive, never mutated) to keep exact source
    _cp_a(POS_W,dst); _verify_source_copy(dst,name)
    retained_before=dst/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/retained/before/sources/{ISSUE_W}/production-state.json"
    assert retained_before.is_file()
    before_bytes=retained_before.read_bytes()
    state_p=dst/f"sources/{ISSUE_W}/production-state.json"
    assert state_p.read_bytes()!=before_bytes
    state_p.write_bytes(before_bytes)
    rec2_rel=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    rec2_p=dst/rec2_rel
    assert rec2_p.is_file()
    if omit: rec2_p.unlink(); assert not rec2_p.exists()
    (dst/"FAULT_FIXTURE_README.txt").write_text(f"SYNTHETIC REACHABLE FAULT FIXTURE (not normal transition/rewind)\nname={name} omit={omit}\nretained_before sha={hashlib.sha256(before_bytes).hexdigest()[:16]}\nset2 wk-r3c-2 record2 present={ (dst/rec2_rel).exists()}\noriginal positive never modified; preserved, never cleaned before snapshot.\n", encoding="utf-8")
    return dst
def _snap(dst,label):
    state_rel=f"sources/{ISSUE_W}/production-state.json"
    rec2_rel=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    try:
        b=(dst/state_rel).read_bytes(); sha=hashlib.sha256(b).hexdigest()[:16]; ptr=json.loads(b.decode()).get("publication_revalidation_provenance")
    except Exception as e: sha=f"UNREADABLE:{e}"; ptr=f"UNREADABLE:{e}"
    rec_exists=(dst/rec2_rel).exists()
    temps=[]
    for pp in (dst/f"sources/{ISSUE_W}").rglob(".*tmp*"):
        try:
            if pp.is_file() and not pp.is_symlink(): temps.append(pp.relative_to(dst).as_posix())
        except OSError: pass
    _log(f"SNAPSHOT {label} sha16={sha} ptr={ptr} rec2={rec_exists} temps={temps}")
    return {"sha16":sha,"ptr":ptr,"rec":rec_exists,"temps":temps}
def case_B7():
    dst=_new_before("fault-v2-orphan",False)
    core,edpub,setmod,observer,agent,pubmod,reader_gate=_load_for_root(dst)
    cfg=core.load_json(dst/core.DEFAULT_CONFIG.as_posix())
    state_rel=f"sources/{ISSUE_W}/production-state.json"; set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/publication/publication-set.json"; rec_rel=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    prop_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/proposal.json"; staged_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/staged-source/staged-source-manifest.json"
    obs=observer.observe_current_authority(dst,dst/state_rel,dst/prop_rel,dst/core.load_json(dst/staged_rel)["retention_manifest_ref"]["path"],dst/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/scope-review-v2.json")
    assert obs.get("result")=="CURRENT_BASIS_OBSERVED_SCOPE_BOUND", obs
    assert edpub.validate_prepared_set(dst,state_rel,set_rel).get("issue_id")==ISSUE_W
    try:
        edpub.activate_publication(dst,state_rel,set_rel,"orphan","fault-exec",datetime.now(timezone.utc)); raise AssertionError("orphan ordinary should refuse")
    except Exception as e:
        assert "RECORD_COLLISION" in str(e) or "collision" in str(e).lower(), f"orphan wrong seam {type(e).__name__}: {str(e)[:800]}"
        _log(f"ORPHAN ordinary refused collision as expected: {str(e)[:400]}")
    _snap(dst,"orphan-collision")
    assert (dst/rec_rel).is_file()
    assert (dst/state_rel).read_bytes()==(dst/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/retained/before/sources/{ISSUE_W}/production-state.json").read_bytes()
    res=edpub.resume_activation(dst,state_rel,rec_rel); assert res.get("status")=="RESUMED" and res.get("observed")=="new", res
    new_st=json.loads((dst/state_rel).read_bytes().decode()); assert new_st.get("publication_revalidation_provenance")=={"path":rec_rel,"sha256":_sha_file(dst/rec_rel)}
    assert agent.validate_agent_state(dst,cfg,new_st)==[]
    assert "wk-r3c-2" in setmod.resolve_publication_selection(dst,cfg,new_st).get("candidate_ref",{}).get("path","")
    _snap(dst,"orphan-resumed"); _log("ORPHAN resume RESUMED exact new + strict readback OK (separate revalidation, not takeover)")
def _with_before_checks(dst, state_rel, set_rel):
    core,edpub,setmod,observer,agent,pubmod,reader_gate=_load_for_root(dst)
    prop_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/proposal.json"; staged_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/staged-source/staged-source-manifest.json"
    obs=observer.observe_current_authority(dst,dst/state_rel,dst/prop_rel,dst/core.load_json(dst/staged_rel)["retention_manifest_ref"]["path"],dst/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/scope-review-v2.json")
    assert obs.get("result")=="CURRENT_BASIS_OBSERVED_SCOPE_BOUND", obs
    assert edpub.validate_prepared_set(dst,state_rel,set_rel).get("issue_id")==ISSUE_W
    return core,edpub,setmod,observer,agent
def case_B1():
    dst=_new_before("fault-v2-before-record-write",True)
    state_rel=f"sources/{ISSUE_W}/production-state.json"; set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/publication/publication-set.json"
    core,edpub,setmod,observer,agent=_with_before_checks(dst,state_rel,set_rel)
    import builtins; real_open=builtins.open
    rec_abs=(dst/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json").resolve()
    def faulty(path,*a,**kw):
        try: p=Path(str(path)).resolve()
        except Exception: p=None
        if p==rec_abs and ("x" in (a[0] if a else kw.get("mode","")) or "x" in str(a)+str(kw)): raise OSError("injected record-write fault")
        return real_open(path,*a,**kw)
    builtins.open=faulty
    try:
        try: edpub.activate_publication(dst,state_rel,set_rel,"fault record-write","fault-exec",datetime.now(timezone.utc)); raise AssertionError("should fail")
        except Exception as e: assert "RECORD_COLLISION" in str(e) or "injected record-write" in str(e), f"wrong seam {type(e).__name__}: {str(e)[:800]}"; _log(f"RECORD-WRITE classified: {str(e)[:500]}")
    finally: builtins.open=real_open
    _snap(dst,"record-write"); assert (dst/state_rel).read_bytes()==(dst/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/retained/before/sources/{ISSUE_W}/production-state.json").read_bytes()
    _log("RECORD-WRITE preserved old OK")
def case_B2():
    dst=_new_before("fault-v2-state-temp",True)
    state_rel=f"sources/{ISSUE_W}/production-state.json"; set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/publication/publication-set.json"
    core,edpub,setmod,observer,agent=_with_before_checks(dst,state_rel,set_rel)
    import builtins; real_open=builtins.open
    def faulty2(path,*a,**kw):
        if ".production-state.json.tmp-reval-" in str(path) and "x" in str(a[0] if a else kw.get("mode","")): raise OSError("injected State-temp fault")
        return real_open(path,*a,**kw)
    builtins.open=faulty2
    try:
        try: edpub.activate_publication(dst,state_rel,set_rel,"fault temp","fault-exec",datetime.now(timezone.utc)); raise AssertionError("should fail")
        except Exception as e: assert "STATE_REPLACE" in str(e) or "injected State-temp" in str(e) or "EXPLICIT_RECOVERY" in str(e), f"wrong {str(e)[:800]}"; _log(f"STATE-TEMP classified: {str(e)[:600]}")
    finally: builtins.open=real_open
    _snap(dst,"state-temp"); assert (dst/f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json").is_file(); _log("STATE-TEMP record inert + State old OK")
def case_B3():
    dst=_new_before("fault-v2-replace",True)
    state_rel=f"sources/{ISSUE_W}/production-state.json"; set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/publication/publication-set.json"
    core,edpub,setmod,observer,agent=_with_before_checks(dst,state_rel,set_rel)
    real_replace=os.replace
    def faulty_r(s,d,*a,**kw):
        if str(d).endswith("production-state.json"): raise OSError("injected replace fault")
        return real_replace(s,d,*a,**kw)
    os.replace=faulty_r
    try:
        try: edpub.activate_publication(dst,state_rel,set_rel,"fault replace","fault-exec",datetime.now(timezone.utc)); raise AssertionError("should fail")
        except Exception as e: assert "STATE_REPLACE" in str(e) or "replace failed" in str(e).lower(), f"wrong {str(e)[:800]}"; _log(f"REPLACE classified: {str(e)[:600]}")
    finally: os.replace=real_replace
    _snap(dst,"replace"); _log("REPLACE observed old + inert OK")
def case_B4():
    dst=_new_before("fault-v2-postread",True)
    state_rel=f"sources/{ISSUE_W}/production-state.json"; set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/publication/publication-set.json"
    core,edpub,setmod,observer,agent=_with_before_checks(dst,state_rel,set_rel)
    real_replace=os.replace; flag={"r":False}
    def fr2(s,d,*a,**kw):
        r=real_replace(s,d,*a,**kw)
        if str(d).endswith("production-state.json"): flag["r"]=True
        return r
    import builtins; real_open=builtins.open
    def fo3(path,*a,**kw):
        if flag["r"] and str(path).endswith("production-state.json") and fo3.c<3:
            fo3.c+=1; raise OSError("injected postread fault")
        return real_open(path,*a,**kw)
    fo3.c=0
    os.replace=fr2; builtins.open=fo3
    try:
        try: edpub.activate_publication(dst,state_rel,set_rel,"fault postread","fault-exec",datetime.now(timezone.utc)); raise AssertionError("should fail")
        except Exception as e: assert "POSTREAD" in str(e) or "POSTREPLACE" in str(e) or "observed unknown" in str(e).lower(), f"wrong {str(e)[:1000]}"; _log(f"POSTREAD classified: {str(e)[:700]}")
    finally: os.replace=real_replace; builtins.open=real_open
    _snap(dst,"postread"); assert (dst/state_rel).read_bytes()!=(dst/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/retained/before/sources/{ISSUE_W}/production-state.json").read_bytes()
    _log("POSTREAD replace then read fail observed unknown OK")
def case_B5():
    dst=_new_before("fault-v2-fsync",True)
    state_rel=f"sources/{ISSUE_W}/production-state.json"; set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/publication/publication-set.json"
    core,edpub,setmod,observer,agent=_with_before_checks(dst,state_rel,set_rel)
    real_fsync=os.fsync; os.fsync=lambda fd: (_ for _ in ()).throw(OSError("injected fsync"))
    try:
        try:
            res=edpub.activate_publication(dst,state_rel,set_rel,"fsync","fault-exec",datetime.now(timezone.utc))
            _log(f"FSYNC swallowed activate succeeded {res} -> BLOCKER fsync not classified (code ignores OSError on fsync)")
            raise AssertionError("BLOCKER: os.fsync failure swallowed (pass) in _exclusive_create_record_bytes and _atomic_replace_state_bytes; no primary/secondary/observed. Need root disposition explicit non-guarantee or classification.")
        except AssertionError as ae:
            if "BLOCKER" in str(ae): raise ae
            raise
        except Exception as e: _log(f"FSYNC unexpectedly classified {type(e).__name__}: {str(e)[:500]}"); raise AssertionError(f"fsync classified unexpectedly {str(e)[:500]}")
    finally: os.fsync=real_fsync
def case_B8():
    dst=_new_before("fault-v2-foreign-inode",True)
    state_rel=f"sources/{ISSUE_W}/production-state.json"; set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/publication/publication-set.json"
    core,edpub,setmod,observer,agent=_with_before_checks(dst,state_rel,set_rel)
    real_excl=agent._exclusive_create_record_bytes
    def hooked(p,exp,label):
        owned=real_excl(p,exp,label)
        cur=Path(p).read_bytes(); assert cur==exp
        old=os.stat(p); Path(p).unlink(); Path(p).write_bytes(exp); new=os.stat(p)
        _log(f"FOREIGN swap old_ino={old.st_ino} new_ino={new.st_ino}")
        return owned
    agent._exclusive_create_record_bytes=hooked
    try:
        try:
            res=edpub.activate_publication(dst,state_rel,set_rel,"foreign","fault-exec",datetime.now(timezone.utc))
            _log(f"FOREIGN succeeded {res} -> BLOCKER missing ownership check")
            raise AssertionError("BLOCKER: activate_publication _exclusive_create returns owned (dev,ino) but record_owned_id never verified via _record_identity_matches before _atomic_replace_state_bytes; same-bytes foreign inode adopts State (should refuse ownership before State adopt). Fired STATE_REPLACE vs expected OWNERSHIP.")
        except AssertionError as ae:
            if "BLOCKER" in str(ae): raise ae
            raise
        except Exception as e:
            if "ownership" in str(e).lower() or "identity" in str(e).lower(): _log(f"FOREIGN correctly refused ownership: {str(e)[:600]}")
            else:
                st=(dst/state_rel).read_bytes(); oldb=(dst/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/retained/before/sources/{ISSUE_W}/production-state.json").read_bytes()
                if st==oldb: raise AssertionError(f"foreign refused but seam unclear (need ownership check): {type(e).__name__}: {str(e)[:800]}")
                else: raise AssertionError(f"foreign State adopted despite replacement: {type(e).__name__}: {str(e)[:800]}")
    finally: agent._exclusive_create_record_bytes=real_excl
    _snap(dst,"foreign")
def case_B9():
    root=_ensure_shared_v2()
    core,edpub,setmod,observer,agent,pubmod,reader_gate=_load_for_root(root)
    # snapshot hashes
    def snap_files(r):
        d={}
        for dp,dn,fn in os.walk(r):
            if ".git" in Path(dp).parts: dn[:]=[]; continue
            for f in sorted(fn):
                pp=Path(dp)/f
                try:
                    if pp.is_symlink(): continue
                    d[pp.relative_to(r).as_posix()]=hashlib.sha256(pp.read_bytes()).hexdigest()
                except OSError: pass
        return d
    before=snap_files(root)
    res=edpub.activate_publication(root,f"sources/{ISSUE_W}/production-state.json",f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/publication/publication-set.json","already","fault-exec",datetime.now(timezone.utc))
    assert res.get("status")=="ALREADY_ACTIVE" and res.get("observed")=="new", res
    assert snap_files(root)==before, "ALREADY_ACTIVE must be readonly"
    _log("ALREADY_ACTIVE readonly OK")
def case_B10():
    dst=FAULT_BASE/"fault-v2-indeterminate"
    if not dst.exists():
        _cp_a(POS_W,dst); _verify_source_copy(dst,"indeterminate-v2")
        st_p=dst/f"sources/{ISSUE_W}/production-state.json"
        st=json.loads(st_p.read_bytes().decode()); st["publication_revalidation_provenance"]=None
        st_p.write_bytes(__import__("scripts.survey_production_v2", fromlist=["x"]).__dict__.get("json_bytes",None)(st) if False else json.dumps(st, indent=2, sort_keys=True).encode()+b"\n")
        # use core from frozen? Need core.json_bytes from dst after load? Simplify: use json canonical via core of dst
        # reload to get correct canonical bytes
        core2,_,_,_,_,_,_= _load_for_root(dst)
        st2=json.loads((dst/f"sources/{ISSUE_W}/production-state.json").read_bytes().decode())
        # rewrite with core canonical to avoid formatting drift? Keep as is (json load will still work, but sha not pinned? State sha not pinned except before_state? For indeterminate test, State null is valid (no activation yet) -> selection CANONICAL, should succeed.
        (dst/"FAULT_FIXTURE_README.txt").write_text("SYNTHETIC indeterminate null pointer (neither old supersedes r1 nor new r2)\n", encoding="utf-8")
    core,edpub,setmod,observer,agent,pubmod,reader_gate=_load_for_root(dst)
    # ensure State null (if previous run left different, reset to null using core canonical)
    st_p=dst/f"sources/{ISSUE_W}/production-state.json"
    st=json.loads(st_p.read_bytes().decode())
    if st.get("publication_revalidation_provenance") is not None:
        st["publication_revalidation_provenance"]=None
        st_p.write_bytes(core.json_bytes(st))
    state_rel=f"sources/{ISSUE_W}/production-state.json"; rec_rel=f"sources/{ISSUE_W}/publication/v2/publication-surface-revalidation-r2.json"
    # resume r2 when State null (supersedes r1 != null, != r2) -> INDETERMINATE
    try: edpub.resume_activation(dst,state_rel,rec_rel); raise AssertionError("should refuse")
    except Exception as e: assert "INDETERMINATE" in str(e), f"resume indeterminate wrong {type(e).__name__}: {str(e)[:800]}"; _log(f"INDETERMINATE resume refused: {str(e)[:400]}")
    snap_state=(dst/state_rel).read_bytes()
    try: edpub.activate_publication(dst,state_rel,f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/publication/publication-set.json","indet","fault-exec",datetime.now(timezone.utc)); raise AssertionError("activate should refuse (before-state mismatch, preserves)")
    except Exception as e: _log(f"INDETERMINATE activate refused (before-state, preserves): {type(e).__name__}: {str(e)[:400]}")
    assert (dst/state_rel).read_bytes()==snap_state
    _snap(dst,"indeterminate"); _log("INDETERMINATE preserves OK")
def case_B11():
    root=_ensure_shared_v2()
    core,edpub,setmod,observer,agent,pubmod,reader_gate=_load_for_root(root)
    try: edpub.activate_publication(root,f"sources/{ISSUE_W}/production-state.json",f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-1/publication/publication-set.json","conflict","fault-exec",datetime.now(timezone.utc)); raise AssertionError("should refuse")
    except Exception as e: assert "BEFORE_STATE" in str(e) or "REFUSED_PRE_WRITE" in str(e), f"wrong {str(e)[:800]}"; _log(f"CONFLICT refused: {str(e)[:400]}")
def case_C_state_drift():
    dst=FAULT_BASE/"fault-v2-state-drift"
    if not dst.exists(): _cp_a(POS_W,dst); _verify_source_copy(dst,"state-drift-v2")
    core,edpub,setmod,observer,agent,pubmod,reader_gate=_load_for_root(dst)
    st_rel=f"sources/{ISSUE_W}/production-state.json"; st_p=dst/st_rel
    orig=(POS_W/st_rel).read_bytes()
    if st_p.read_bytes()==orig:
        st=json.loads(orig.decode()); st["contract"]["pipeline_contract_sha256"]="00"+st["contract"]["pipeline_contract_sha256"][2:]; st_p.write_bytes(core.json_bytes(st))
    set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/publication/publication-set.json"
    prop_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/proposal.json"; staged_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/staged-source/staged-source-manifest.json"
    try:
        observer.observe_current_authority(dst,dst/st_rel,dst/prop_rel,dst/core.load_json(dst/staged_rel)["retention_manifest_ref"]["path"],dst/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/scope-review-v2.json")
        _log("STATE drift P2V passed (check activate)")
    except Exception as e: _log(f"STATE drift P2V refused: {type(e).__name__}: {str(e)[:500]}"); _snap(dst,"state-drift-p2v"); return
    try: edpub.activate_publication(dst,st_rel,set_rel,"drift","fault-exec",datetime.now(timezone.utc)); raise AssertionError("should refuse")
    except Exception as e: _log(f"STATE drift activate refused: {type(e).__name__}: {str(e)[:600]}")
    _snap(dst,"state-drift")
def case_C_approved_foreign():
    dst=FAULT_BASE/"fault-v2-approved"
    if not dst.exists(): _cp_a(POS_W,dst); _verify_source_copy(dst,"approved-v2")
    core,edpub,setmod,observer,agent,pubmod,reader_gate=_load_for_root(dst)
    st_rel=f"sources/{ISSUE_W}/production-state.json"; st_p=dst/st_rel
    st=json.loads((POS_W/st_rel).read_bytes().decode()); st["human_gates"]["publication_preview"]="approved"; st_p.write_bytes(core.json_bytes(st))
    set_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/publication/publication-set.json"
    try: edpub.activate_publication(dst,st_rel,set_rel,"approved","fault-exec",datetime.now(timezone.utc)); raise AssertionError("should refuse")
    except Exception as e: assert "PREDECISION" in str(e) or "Publication Preview" in str(e), f"wrong {str(e)[:800]}"; _log(f"APPROVED refused: {str(e)[:500]}")
    dst2=FAULT_BASE/"fault-v2-foreign"
    if not dst2.exists(): _cp_a(POS_W,dst2); _verify_source_copy(dst2,"foreign-v2")
    core2,edpub2,setmod2,observer2,agent2,pubmod2,rg2=_load_for_root(dst2)
    lf_set_src=POS_L/f"sources/SP001/publication/v2/editorial-corrections/lf-r3c-2/publication/publication-set.json"
    foreign_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/publication/foreign-lf-set.json"
    if not (dst2/foreign_rel).exists(): (dst2/foreign_rel).write_bytes(lf_set_src.read_bytes())
    try: edpub2.activate_publication(dst2,f"sources/{ISSUE_W}/production-state.json",foreign_rel,"foreign","fault-exec",datetime.now(timezone.utc)); raise AssertionError("should refuse")
    except Exception as e: _log(f"FOREIGN refused: {type(e).__name__}: {str(e)[:600]}")
def case_C_build():
    dst=FAULT_BASE/"fault-v2-build"
    if not dst.exists(): _cp_a(POS_W,dst); _verify_source_copy(dst,"build-v2")
    core,edpub,setmod,observer,agent,pubmod,reader_gate=_load_for_root(dst)
    import shutil as _sh
    pubdir=dst/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/publication"
    bak=dst/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/publication-bak-v2"
    if pubdir.exists() and not bak.exists(): _sh.move(str(pubdir),str(bak))
    assert not pubdir.exists()
    valid_tspec=dst/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/toolchain-spec.json"
    ts=json.loads(valid_tspec.read_bytes().decode()); ts["absolute_executable"]="/nonexistent/lualatex-fault"
    bad_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/toolchain-spec-fault-v2.json"
    (dst/bad_rel).write_bytes(core.json_bytes(ts))
    prop_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/proposal.json"; staged_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/staged-source/staged-source-manifest.json"; mspec_rel=f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/manuscript-spec.json"; state_rel=f"sources/{ISSUE_W}/production-state.json"
    (dst/state_rel).write_bytes((dst/f"sources/{ISSUE_W}/publication/v2/editorial-corrections/wk-r3c-2/retained/before/sources/{ISSUE_W}/production-state.json").read_bytes())
    try: edpub.prepare_publication(dst,state_rel,prop_rel,staged_rel,mspec_rel,bad_rel,datetime.now(timezone.utc)); raise AssertionError("should fail")
    except Exception as e: assert "toolchain" in str(e).lower() or "executable" in str(e).lower() or "build" in str(e).lower(), f"wrong seam {str(e)[:1000]}"; _log(f"BUILD failure refused: {str(e)[:700]}")
    assert bak.exists(); _log("BUILD failure no forged PDF, real controls preserved OK")
    if not pubdir.exists(): _sh.move(str(bak),str(pubdir))
    try: edpub.prepare_publication(dst,state_rel,prop_rel,staged_rel,mspec_rel,bad_rel,datetime.now(timezone.utc)); raise AssertionError("should refuse exists")
    except Exception as e2: assert "PUBLICATION_EXISTS" in str(e2) or "already claimed" in str(e2).lower(), f"wrong {str(e2)[:800]}"; _log(f"EXISTING refused no duplicate build: {str(e2)[:400]}")
def main():
    global NOTES
    if len(sys.argv)!=3: print(f"usage: {sys.argv[0]} FAULT_BASE NOTES_DIR", flush=True); return 2
    base=Path(sys.argv[1]).resolve(); NOTES=Path(sys.argv[2]).resolve(); NOTES.mkdir(parents=True, exist_ok=True); FAULT_BASE.mkdir(parents=True, exist_ok=True)
    _log(f"CMD={' '.join(sys.argv)}"); _log(f"CWD={Path.cwd()}"); _log(f"FROZEN={FROZEN} HEAD={FROZEN_HEAD}"); _log(f"FAULT_BASE={FAULT_BASE}")
    _case("A0_source_and_positives",case_A0); _case("A1_healthy_controls",case_A1)
    _case("B7_orphan_collision_then_resume",case_B7); _case("B1_record_write",case_B1); _case("B2_state_temp",case_B2); _case("B3_replace",case_B3); _case("B4_postread",case_B4)
    _case("B5_fsync_BLOCKER",case_B5); _case("B8_foreign_BLOCKER",case_B8); _case("B9_already_active",case_B9); _case("B10_indeterminate",case_B10); _case("B11_conflict",case_B11)
    _case("C_state_drift",case_C_state_drift); _case("C_approved_foreign",case_C_approved_foreign); _case("C_build",case_C_build)
    dt=time.monotonic()-T0; _log(f"TOTAL pass={PASS} fail={FAIL} dt={dt:.1f}s")
    for n,s,d,det in CASES: _log(f"SUMMARY {s} {n} dt={d:.1f}s {det[:200]}")
    (NOTES/"summary-v2.json").write_text(json.dumps({"pass":PASS,"fail":FAIL,"cases":[{"name":n,"status":s,"dt":d,"detail":det} for n,s,d,det in CASES]}, indent=2), encoding="utf-8")
    print(f"EXIT:{0 if FAIL==0 else 2}", flush=True); return 0 if FAIL==0 else 2
if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2", flush=True); rc=2
    sys.exit(rc)
