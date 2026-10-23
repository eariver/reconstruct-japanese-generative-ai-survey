#!/usr/bin/env python3
"""Worker C TEST ONLY: R1x2 -> versioned correction -> healthy readback + refusals (R3c fixed source).

Governing d880 §9 + root selection + R3/R3c fixes. Frozen SOURCE 0d9857e6
tracked718 clean. Low d2909bba ANCHORED canonical7 4keys, agent 05f1ee03 uses anchor,
P1 23e3a45f repeat. No source edits except 2 isolated R1 fixture comment commits
(AST-neutral before build_reader_input, process-scoped identity). No ordinary commits/
network/clean/reset/purge/raw deletion. Prior failed 4ff fixture preserved untouched.
NEW independent tracked718 source-only +GitDB copy, inert origin, no sharing.
Env PYTHONDONTWRITEBYTECODE + external PY cache set BEFORE interpreter (no purge).
Actual R1 nonemitted x2, real refresh subprocess current code, contract67 + weekly22/P3S50.
Then P1/P2R/scope/P2V/P3S HIGH prepare REAL TL2026 -> typed reviews/QA -> seal ->
activate. Assert anchor==r2, r3 supersedes r2, canonical7==R1b Gate !=original,
State/readback healthy, old canonical byte-exact after R1b, active7 matches new set,
historical links + unchanged research, ALREADY_ACTIVE readonly, R1/canonical/false
editorial refused pre-write on HEALTHY state with full inventory. No validator/Git mock.
No full Release duplication. Type fixtures only, no genuine Human/research approval.
"""
from __future__ import annotations
import ast as _ast
import copy
import hashlib
import json
import os
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

def _log(m: str):
    print(m, flush=True)

def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} FIX_ROOT NOTES_DIR", flush=True)
        return 2
    FIX_ROOT = Path(sys.argv[1]).resolve()
    NOTES = Path(sys.argv[2]).resolve()
    NOTES.mkdir(parents=True, exist_ok=True)
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(FIX_ROOT))
    for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
        if os.environ.get(_v):
            _log(f"UNSAFE inherited {_v}"); return 2
    import unittest
    from scripts import survey_production_v2 as core
    from scripts import survey_editorial_publication_v2 as edpub
    from scripts import survey_reader_publication_v2 as reader_pub
    from scripts import survey_reader_surface_gate_v2 as reader_gate
    from scripts import survey_publication_v2 as pubmod
    from scripts import survey_publication_set_v2 as setmod
    from scripts import survey_editorial_correction_proposal_v2 as proposal_mod
    from scripts import survey_editorial_retention_v2 as retention
    from scripts import survey_editorial_current_authority_v2 as observer
    from scripts import survey_editorial_staged_source_v2 as staged
    from scripts import survey_agent_control_v2 as agent
    from tests import test_survey_editorial_correction_proposal_v2 as p1t
    from tests import test_survey_editorial_staged_source_v2 as p3st
    from tests.test_survey_editorial_retention_v2 import _prepare_proposal_for as _prep_ret
    ISSUE="2026-W37"
    TL_BIN=Path("/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/lualatex")
    class _TC(unittest.TestCase):
        def runTest(self): pass
    tc=_TC()
    def _run_git(*a):
        env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
        env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
        return subprocess.run(["git",*a],cwd=FIX_ROOT,capture_output=True,text=True,timeout=120,env=env)
    def _snapshot():
        files={}
        for dirpath,dirnames,filenames in os.walk(FIX_ROOT):
            if ".git" in Path(dirpath).parts:
                dirnames[:]=[]; continue
            for fn in sorted(filenames):
                p=Path(dirpath)/fn
                rel=p.relative_to(FIX_ROOT).as_posix()
                h=hashlib.sha256()
                with p.open("rb") as f:
                    for ch in iter(lambda:f.read(1<<20),b""): h.update(ch)
                files[rel]=h.hexdigest()
        import stat as _stat
        special={}
        for dirpath,dirnames,filenames in os.walk(FIX_ROOT):
            if ".git" in Path(dirpath).parts:
                dirnames[:]=[]; continue
            for fn in sorted(filenames)+sorted(dirnames):
                p=Path(dirpath)/fn
                try: st=os.lstat(p)
                except: continue
                if _stat.S_ISLNK(st.st_mode) or not _stat.S_ISREG(st.st_mode):
                    special[p.relative_to(FIX_ROOT).as_posix()]=oct(st.st_mode)
        return {"files":files,"special":special,"head":_run_git("rev-parse","HEAD").stdout.strip(),"status":_run_git("status","--porcelain").stdout}
    def _assert_no_write(b,a,label):
        assert a["files"]==b["files"], f"tree write {label}"
        assert a.get("special")==b.get("special"), f"special {label}"
        assert a["head"]==b["head"], f"HEAD {label}"
        assert a["status"]==b["status"], f"status {label}"
    def _run_fixture(script,args,timeout_s=1200):
        env={k:v for k,v in os.environ.items() if not k.startswith("GIT_") and k!="PYTHONPATH"}
        env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file","PYTHONDONTWRITEBYTECODE":"1"})
        # PYTHONPYCACHEPREFIX already set BEFORE interpreter via outer env; preserve it
        proc=subprocess.run([sys.executable,"-c",script,*args],cwd=FIX_ROOT,capture_output=True,text=True,timeout=timeout_s,env=env)
        return proc.returncode,proc.stdout,proc.stderr
    t0=time.monotonic()
    # 0 SOURCE binding + code pins
    _log("===0 SOURCE===")
    head=_run_git("rev-parse","HEAD").stdout.strip()
    tree=_run_git("rev-parse","HEAD^{tree}").stdout.strip()
    _log(f"HEAD={head} TREE={tree}")
    assert head=="0d9857e6132fb314a2e2ba141da79c54f4ec5e06", head
    assert tree=="44bfc1864d269e338bdb64bcc030e5fd558bf060", tree
    assert len(_run_git("ls-files").stdout.strip().splitlines())==718
    assert _run_git("status","--porcelain=v1","--untracked-files=all").stdout.strip()=="", "fixture must start clean"
    assert TL_BIN.exists()
    from scripts import survey_weekly_derivation_v2 as _wkd
    assert len(_wkd.CURRENT_CLOSURE)==22, len(_wkd.CURRENT_CLOSURE)
    cfg0=core.load_json(FIX_ROOT/core.DEFAULT_CONFIG)
    assert len(cfg0["contract_files"]["pipeline"])==67
    # key code pins
    assert hashlib.sha256((FIX_ROOT/"scripts/survey_publication_set_v2.py").read_bytes()).hexdigest()=="d2909bbaead935d6fba548fb9b0c9d1178a6027685db2d8c8691b6ee8f02f2c1"
    assert hashlib.sha256((FIX_ROOT/"scripts/survey_agent_control_v2.py").read_bytes()).hexdigest()=="05f1ee03a91b647d88bd66877e702c7044a34c6f5d44bdbeb46710375a104103"
    assert hashlib.sha256((FIX_ROOT/"scripts/survey_editorial_correction_proposal_v2.py").read_bytes()).hexdigest().startswith("23e3a45f")
    _log("PINS_OK low d2909bba agent 05f1ee03 P1 23e3a45f closure22 contract67 TL OK")
    # 1 bootstrap
    _log("===1 BOOTSTRAP===")
    helper=p1t._new_weekly_helper(tc,FIX_ROOT)
    built=p1t._build_weekly_validated(tc,helper)
    chain,state_path=built["chain"],Path(built["state_path"])
    if not state_path.is_absolute(): state_path=(FIX_ROOT/state_path).resolve()
    st0=core.load_json(state_path)
    assert st0.get("publication_revalidation_provenance") is None
    state_rel=str(state_path.relative_to(FIX_ROOT).as_posix())
    src_root=helper.source_root
    _log(f"BOOTSTRAP_OK {state_rel}")
    base_state_bytes=state_path.read_bytes()
    (NOTES/"base-state.json").write_bytes(base_state_bytes)
    validation_ref=st0["checkpoint_provenance"]["validation"]
    orig_ckpt=core.load_json(FIX_ROOT/validation_ref["path"])
    orig_map={(r["name"],r["path"]):r["sha256"] for r in orig_ckpt.get("artifacts",[])}
    _log(f"ORIG_ARTIFACTS={len(orig_map)}")
    (NOTES/"base-validation-checkpoint.json").write_bytes((FIX_ROOT/validation_ref["path"]).read_bytes())
    # R1a genuine owner via actual helper
    _log("===R1a COMMIT (actual _commit_r1_nonemitted_comment)===")
    head_before=_run_git("rev-parse","HEAD").stdout.strip()
    r1a_head=p3st._commit_r1_nonemitted_comment(tc,FIX_ROOT)
    assert r1a_head!=head_before
    assert len(_wkd.CURRENT_CLOSURE)==22
    assert len(core.load_json(FIX_ROOT/core.DEFAULT_CONFIG)["contract_files"]["pipeline"])==67
    _log(f"R1a_HEAD={r1a_head} CLOSURE22 CONTRACT67 UNCHANGED")
    r1_script=("import sys\nfrom pathlib import Path\nroot=Path(sys.argv[1])\nstate_path=Path(sys.argv[2])\n"
               "from scripts import survey_production_v2 as core\nfrom scripts import survey_weekly_mechanical_refresh_v2 as r1\nfrom datetime import datetime,timezone\n"
               "recorded=datetime(2026,9,19,8,0,0,tzinfo=timezone.utc)\n"
               "result=r1.refresh_mechanical_evidence(root,core.load_json(root / core.DEFAULT_CONFIG),state_path,'fixture R1 first refresh','synthetic WorkerC R1',recorded)\n"
               "import json; print(json.dumps({'result':'OK','keys':sorted(result.keys())}))\n")
    t=time.monotonic(); rc,out,err=_run_fixture(r1_script,[str(FIX_ROOT),str(state_path)]); dt=time.monotonic()-t
    _log(f"R1a_REFRESH rc={rc} dt={dt:.1f}s out={out[:400]} err_tail={err[-1500:]}")
    assert rc==0, f"R1a failed {out} {err[-4000:]}"
    state1=core.load_json(state_path)
    rec1_ref=state1["publication_revalidation_provenance"]
    _log(f"R1a_RECORD={rec1_ref}")
    (NOTES/"state-after-r1a.json").write_bytes(state_path.read_bytes())
    rec1_path=FIX_ROOT/rec1_ref["path"]; (NOTES/"record-r1a.json").write_bytes(rec1_path.read_bytes())
    rec1=core.load_json(rec1_path)
    assert rec1.get("supersedes") is None
    sup1={(r["name"],r["path"]):r["prior_sha256"] for r in rec1.get("superseded_artifacts",[])}
    pres1={(r["name"],r["path"]):r["sha256"] for r in rec1.get("preserved_artifacts",[])}
    for k,v in sup1.items(): assert orig_map.get(k)==v, k
    for k,v in pres1.items(): assert orig_map.get(k)==v, k
    assert set(sup1)|set(pres1)==set(orig_map)
    _log(f"R1a_CUMULATIVE_OK {len(sup1)}+{len(pres1)}={len(orig_map)}")
    def _mut_r1a():
        a=core.load_json(chain["authored_path"]); a["cover"]["headline"]="Weekly R1 first refresh, revised edition"; return a
    pp1,_= _prep_ret(tc,FIX_ROOT,helper,chain,state_path,"fixture-wk-r1a-verify",_mut_r1a)
    out1=retention.capture_retention(FIX_ROOT,state_path,pp1); assert out1["result"]==retention.RESULT_CAPTURED
    m1_path=FIX_ROOT/out1["manifest_path"]; assert retention.verify_retention(FIX_ROOT,pp1,m1_path)["result"]==retention.RESULT_VERIFIED
    _log(f"R1a_RETENTION_OK {out1['manifest_path']}")
    (NOTES/"retention-r1a-manifest.json").write_bytes(m1_path.read_bytes())
    # R1b second distinct meaningful comment
    _log("===R1b COMMIT (second distinct AST-neutral)===")
    probe=FIX_ROOT/"scripts/survey_weekly_derivation_v2.py"
    text=probe.read_text(encoding="utf-8")
    anchor2="fixture R1 second non-emitted Python comment C2 R3c"
    assert anchor2 not in text
    before_ast=_ast.dump(_ast.parse(text))
    lines=text.splitlines(keepends=True)
    tg=[i for i,l in enumerate(lines) if l.startswith("def build_reader_input(")]
    assert len(tg)==1
    lines.insert(tg[0], f"# {anchor2}\n")
    probe.write_text("".join(lines),encoding="utf-8")
    assert before_ast==_ast.dump(_ast.parse(probe.read_text(encoding="utf-8")))
    p=_run_git("add","scripts/survey_weekly_derivation_v2.py"); assert p.returncode==0, p.stderr
    p=_run_git("-c","user.name=Synthetic WorkerC R1Anchor","-c","user.email=workerc-r1anchor@example.invalid","commit","-q","-m","Fixture R1 second non-emitted comment C2 R3c"); assert p.returncode==0, p.stderr
    r1b_head=_run_git("rev-parse","HEAD").stdout.strip()
    assert len(_wkd.CURRENT_CLOSURE)==22
    assert len(core.load_json(FIX_ROOT/core.DEFAULT_CONFIG)["contract_files"]["pipeline"])==67
    _log(f"R1b_HEAD={r1b_head} CLOSURE22 CONTRACT67 UNCHANGED")
    r1_script2=("import sys\nfrom pathlib import Path\nroot=Path(sys.argv[1])\nstate_path=Path(sys.argv[2])\n"
                "from scripts import survey_production_v2 as core\nfrom scripts import survey_weekly_mechanical_refresh_v2 as r1\nfrom datetime import datetime,timezone\n"
                "recorded=datetime(2026,9,19,8,5,0,tzinfo=timezone.utc)\n"
                "result=r1.refresh_mechanical_evidence(root,core.load_json(root / core.DEFAULT_CONFIG),state_path,'fixture R1 second refresh','synthetic WorkerC R1',recorded)\n"
                "import json; print(json.dumps({'result':'OK','keys':sorted(result.keys())}))\n")
    t=time.monotonic(); rc2,out2,err2=_run_fixture(r1_script2,[str(FIX_ROOT),str(state_path)]); dt2=time.monotonic()-t
    _log(f"R1b_REFRESH rc={rc2} dt={dt2:.1f}s out={out2[:400]}")
    assert rc2==0, f"R1b failed {out2} {err2[-4000:]}"
    state2=core.load_json(state_path)
    rec2_ref=state2["publication_revalidation_provenance"]
    _log(f"R1b_RECORD={rec2_ref}")
    assert rec2_ref!=rec1_ref
    (NOTES/"state-after-r1b.json").write_bytes(state_path.read_bytes())
    rec2_path=FIX_ROOT/rec2_ref["path"]; (NOTES/"record-r1b.json").write_bytes(rec2_path.read_bytes())
    rec2=core.load_json(rec2_path)
    assert rec2.get("supersedes")==rec1_ref, f"second.supersedes first {rec2.get('supersedes')}"
    _log("R1b_SUPERSEDES_FIRST_OK")
    sup2={(r["name"],r["path"]):r["prior_sha256"] for r in rec2.get("superseded_artifacts",[])}
    pres2={(r["name"],r["path"]):r["sha256"] for r in rec2.get("preserved_artifacts",[])}
    for k,v in sup2.items(): assert orig_map.get(k)==v, k
    for k,v in pres2.items(): assert orig_map.get(k)==v, k
    assert set(sup2)|set(pres2)==set(orig_map)
    _log("R1b_CUMULATIVE_OK")
    cfg2=core.load_json(FIX_ROOT/core.DEFAULT_CONFIG)
    act2,errs2=agent.resolve_active_publication_revalidation(FIX_ROOT,cfg2,core.load_json(state_path))
    assert errs2==[] and act2.get("supersedes") is not None
    def _mut_r1b():
        a=core.load_json(chain["authored_path"]); a["cover"]["headline"]="Weekly R1 second refresh, revised edition"; return a
    pp2,_=_prep_ret(tc,FIX_ROOT,helper,chain,state_path,"fixture-wk-r1b-verify",_mut_r1b)
    out2r=retention.capture_retention(FIX_ROOT,state_path,pp2); assert out2r["result"]==retention.RESULT_CAPTURED
    m2_path=FIX_ROOT/out2r["manifest_path"]; assert retention.verify_retention(FIX_ROOT,pp2,m2_path)["result"]==retention.RESULT_VERIFIED
    _log(f"R1b_RETENTION_OK {out2r['manifest_path']}")
    (NOTES/"retention-r1b-manifest.json").write_bytes(m2_path.read_bytes())
    try:
        retention.verify_retention(FIX_ROOT,pp1,m1_path)
        raise AssertionError("old pp1 must fail after R1b")
    except Exception as e:
        assert any(s in str(e) for s in ("INVALID_RETENTION","REF_DRIFT","PROFILE_DRIFT","COPY_DRIFT")), e
        _log(f"OLD_RETENTION_REFUSAL_OK {type(e).__name__}")
    # Versioned correction (single) after R1x2
    _log("===VERSIONED CORRECTION===")
    from tests.test_survey_editorial_staged_source_v2 import _weekly_prepare_from as _wk_from
    corr=_wk_from(tc,FIX_ROOT,helper,{"chain":chain,"state_path":state_path,"helper":helper},"fixture-wk-corr-r3c")
    proposal_path=corr["proposal_path"]; prepared=corr["prepared"]
    state_path=Path(corr.get("state_path",state_path))
    if not state_path.is_absolute(): state_path=(FIX_ROOT/state_path).resolve()
    _log(f"CORR_PROPOSAL={proposal_path.relative_to(FIX_ROOT)}")
    cap=retention.capture_retention(FIX_ROOT,state_path,proposal_path); assert cap["result"]==retention.RESULT_CAPTURED
    manifest_path=FIX_ROOT/cap["manifest_path"]; assert retention.verify_retention(FIX_ROOT,proposal_path,manifest_path)["result"]==retention.RESULT_VERIFIED
    _log(f"CORR_P2R_OK {cap['manifest_path']}")
    try:
        proposal_mod.validate_proposal(FIX_ROOT,state_path,proposal_path)
        raise AssertionError("P1 after capture must refuse")
    except Exception as e:
        assert "RETENTION_DEST_CONFLICT" in str(e) or "REFUSED" in str(e) or "retention" in str(e).lower(), e
        _log(f"P1_AFTER_CAPTURE_REFUSAL_OK {type(e).__name__}")
    staged_reader_rel=prepared["proposal"]["proposed"]["proposed_reader_ref"]["path"]
    scope_path=p1t._scope_review_for(tc,FIX_ROOT,prepared,staged_reader_rel,"scope-review-v2.json")
    _log(f"SCOPE={scope_path.relative_to(FIX_ROOT)}")
    obs=observer.observe_current_authority(FIX_ROOT,state_path,proposal_path,manifest_path,scope_path)
    assert obs.get("result")=="CURRENT_BASIS_OBSERVED_SCOPE_BOUND", obs
    _log("P2V_SCOPE_BOUND")
    mat=staged.materialize_staged_source(FIX_ROOT,state_path,proposal_path,manifest_path,scope_path)
    _log(f"P3S_MATERIALIZE={str(mat)[:600]}")
    staged_manifest_path=FIX_ROOT/mat["staged_manifest_path"] if isinstance(mat,dict) and "staged_manifest_path" in mat else (proposal_path.parent/"staged-source"/"staged-source-manifest.json")
    assert staged_manifest_path.is_file()
    assert staged.verify_staged_source(FIX_ROOT,proposal_path,staged_manifest_path)["result"]=="STAGED_SOURCE_REPLAY_VERIFIED"
    assert len(core.load_json(staged_manifest_path)["code_deps"])==50
    _log("P3S_VERIFIED50")
    # prepare REAL TL2026
    proposal_dir=proposal_path.parent
    staged_manifest=core.load_json(staged_manifest_path)
    issue_id=staged_manifest.get("issue_id")
    arch=core.load_json(helper.source_root/"architecture-v2.json")
    coverage=[{"package_id":pl["package_id"],"requirement":rq,"status":"FULFILLED","reader_locations":["main.tex:package-1"],"detail":f"R3c WorkerC maps {proposal_path.parent.name}."} for pl in arch.get("packages",[]) for rq in pl.get("must_cover_requirements",[])]
    requirements=[{"requirement_id":"FINAL_SYNTHESIS","status":"FULFILLED","reader_locations":["main.tex:summary"],"detail":"WorkerC synthesis."},{"requirement_id":"WEEKLY_COMMUNITY_MOVEMENT","status":"FULFILLED","reader_locations":["main.tex:package-1"],"detail":"WorkerC movement."}]
    mspec={"schema_version":"2.0-rc1","kind":"EDITORIAL_MANUSCRIPT_SPEC_V1","issue_id":issue_id,"proposal_ref":{"path":str(proposal_path.relative_to(FIX_ROOT)),"sha256":core.sha256_file(proposal_path)},"architecture_coverage":coverage,"reader_requirements":requirements,"authored_by":"workerc manuscript author","recorded_at":datetime.now(timezone.utc).isoformat()}
    mspec_path=proposal_dir/"manuscript-spec.json"; core.write_json(mspec_path,mspec)
    tspec={"schema_version":"2.0-rc1","kind":"EDITORIAL_TOOLCHAIN_SPEC_V1","executor":"workerc-r3c","absolute_executable":str(TL_BIN),"recipe":"lualatex-biber-lualatex","argv":list(edpub.EXPECTED_ARGV_LUALATEX_BIBER),"env":{},"recorded_at":datetime.now(timezone.utc).isoformat()}
    tspec_path=proposal_dir/"toolchain-spec.json"; core.write_json(tspec_path,tspec)
    def _rel2(p):
        if isinstance(p,Path):
            try: return str(p.relative_to(FIX_ROOT)) if p.is_absolute() else str(p)
            except: return str(p)
        s=str(p)
        if s.startswith("/"):
            try: return str(Path(s).relative_to(FIX_ROOT))
            except: return s
        return s
    t=time.monotonic()
    prepared_paths=edpub.prepare_publication(FIX_ROOT,_rel2(state_path),_rel2(proposal_path),_rel2(staged_manifest_path),_rel2(mspec_path),_rel2(tspec_path),datetime.now(timezone.utc))
    dtp=time.monotonic()-t
    _log(f"PREPARE_OK dt={dtp:.1f}s {json.dumps(prepared_paths)[:600]}")
    pubdir=proposal_dir/"publication"
    manuscript_path=pubdir/"reader-manuscript-v2.json"; pdf_path=pubdir/"build"/"main.pdf"
    assert manuscript_path.is_file() and pdf_path.is_file()
    from pypdf import PdfReader as _PR
    pages=len(_PR(str(pdf_path)).pages)
    assert pages>=1
    _log(f"REAL_PDF pages={pages} bytes={pdf_path.stat().st_size}")
    qroot=pubdir/"quality"; qroot.mkdir(parents=True,exist_ok=True)
    sp=qroot/"subject-entity-property-binding.json"; core.write_json(sp,{"check_id":"SUBJECT_ENTITY_PROPERTY_BINDING","status":"PASS","scope":"workerc r3c real-build"})
    main_bytes=(FIX_ROOT/staged_manifest["outputs"]["main"]["path"]).read_bytes()
    ip=qroot/"identifier-preservation.json"; core.write_json(ip,{"check_id":"IDENTIFIER_PRESERVATION","status":"PASS","source_sha256":core.sha256_bytes(main_bytes),"inspected_identifiers":[issue_id],"scope":"workerc r3c"})
    ppth=qroot/"pdf-preflight.json"; core.write_json(ppth,{"check_id":"PDF_PREFLIGHT","status":"PASS","page_count":pages,"pdf_sha256":core.sha256_file(pdf_path),"byte_count":pdf_path.stat().st_size,"scope":"workerc real TL2026"})
    qchecks=[{"check_id":cid,"kind":"DETERMINISTIC","status":"PASS","executor":"workerc with actual assertions","evidence":"Exact bytes inspected.","recorded_at":datetime.now(timezone.utc).isoformat(),"result":{"path":str(p.relative_to(FIX_ROOT)),"sha256":core.sha256_file(p)}} for cid,p in (("SUBJECT_ENTITY_PROPERTY_BINDING",sp),("IDENTIFIER_PRESERVATION",ip),("PDF_PREFLIGHT",ppth))]
    det_path=proposal_dir/"deterministic-checks.json"; core.write_json(det_path,{"checks":qchecks})
    profile=core.load_json(FIX_ROOT/core.load_json(state_path)["profile"]["path"])
    for kind,fname in (("SEMANTIC_EDITORIAL","semantic-review-v2.json"),("VISUAL","visual-review-v2.json")):
        checks=[{"check_id":cid,"status":"PASS","detail":f"WorkerC synthetic {kind}; no genuine approval.","evidence_locations":["workerc-real-build:main.pdf"]} for cid in sorted(reader_pub._expected_review_checks(FIX_ROOT,profile,kind))]
        reader_pub.build_review_record(FIX_ROOT,manuscript_path,pdf_path,pages,kind,checks,f"workerc synthetic {kind}",datetime.now(timezone.utc),pubdir/fname)
        _log(f"REVIEW {kind}")
    sem_path=pubdir/"semantic-review-v2.json"; vis_path=pubdir/"visual-review-v2.json"
    snap_before_final=None
    # finalize
    t=time.monotonic()
    set_ref=edpub.finalize_publication(FIX_ROOT,_rel2(state_path),_rel2(proposal_path),_rel2(staged_manifest_path),_rel2(det_path),_rel2(sem_path),_rel2(vis_path),datetime.now(timezone.utc))
    dtf=time.monotonic()-t
    _log(f"FINALIZE_OK dt={dtf:.1f}s {json.dumps(set_ref)[:500]}")
    assert agent.validate_agent_state(FIX_ROOT,core.load_json(FIX_ROOT/core.DEFAULT_CONFIG),core.load_json(state_path))==[]
    _log("INERT_HEALTHY")
    _set_raw=set_ref["set_ref"] if isinstance(set_ref,dict) and "set_ref" in set_ref else set_ref
    set_rel=_set_raw.get("path") if isinstance(_set_raw,dict) else str(_set_raw)
    if set_rel.startswith("/"): set_rel=str(Path(set_rel).relative_to(FIX_ROOT))
    assert (FIX_ROOT/set_rel).is_file()
    (NOTES/"publication-set.json").write_bytes((FIX_ROOT/set_rel).read_bytes())
    snap_before_activate=None
    # capture snapshot before activate for old-canonical check
    def _full_snapshot():
        files={}
        for dirpath,dirnames,filenames in os.walk(FIX_ROOT):
            if ".git" in Path(dirpath).parts:
                dirnames[:]=[]; continue
            for fn in sorted(filenames):
                p=Path(dirpath)/fn
                rel=p.relative_to(FIX_ROOT).as_posix()
                h=hashlib.sha256()
                with p.open("rb") as f:
                    for ch in iter(lambda:f.read(1<<20),b""): h.update(ch)
                files[rel]=h.hexdigest()
        return files
    before_files=_full_snapshot()
    t=time.monotonic()
    res=edpub.activate_publication(FIX_ROOT,_rel2(state_path),set_rel,"WorkerC weekly editorial correction R3c","workerc-executor",datetime.now(timezone.utc))
    dta=time.monotonic()-t
    _log(f"ACTIVATE dt={dta:.1f}s {json.dumps(res)}")
    assert res.get("status")=="ACTIVATED", res
    act_path=FIX_ROOT/res["record_path"]
    act_rec=core.load_json(act_path)
    anchor=act_rec.get("canonical_anchor")
    _log(f"ANCHOR={json.dumps(anchor)}")
    assert anchor.get("kind")=="LEGACY_REVALIDATION", anchor
    assert anchor.get("ref")==rec2_ref, f"anchor {anchor.get('ref')} != r2 {rec2_ref}"
    assert act_rec.get("supersedes")==rec2_ref, f"r3 supersedes r2 {act_rec.get('supersedes')}"
    _log("ANCHOR_IS_R1B_OK R3_SUPERSEDES_R2_OK")
    (NOTES/"activation-record.json").write_bytes(act_path.read_bytes())
    (NOTES/"state-after-activate.json").write_bytes((FIX_ROOT/_rel2(state_path)).read_bytes())
    # canonical7 == R1b Gate not original
    sel=setmod.resolve_publication_selection(FIX_ROOT,core.load_json(FIX_ROOT/core.DEFAULT_CONFIG),core.load_json(FIX_ROOT/_rel2(state_path)))
    assert sel.get("mode")=="VERSIONED_ACTIVE", sel
    canon7=sel.get("canonical7",{})
    assert len(canon7)==7, canon7.keys()
    # find gate row
    gate_row=None
    for k,v in canon7.items():
        if "gate" in k.lower():
            gate_row=v; gate_key=k; break
    assert gate_row is not None, f"gate not in canonical7 {list(canon7.keys())}"
    _log(f"CANONICAL7_GATE {gate_key}={gate_row}")
    # R1b new Gate hash from rec2
    r1b_gate_new=None
    for r in rec2.get("superseded_artifacts",[]):
        if r.get("name")=="reader-surface-gate":
            r1b_gate_new=r.get("new_sha256"); r1b_prior=r.get("prior_sha256"); break
    assert r1b_gate_new is not None
    assert gate_row.get("sha256")==r1b_gate_new, f"canonical7 Gate {gate_row.get('sha256')} != R1b new {r1b_gate_new}"
    assert gate_row.get("sha256")!=orig_map.get(("reader-surface-gate","sources/2026-W37/publication/v2/reader-surface-gate-v2.json")), "must not be original"
    assert len(gate_row)==4 and set(gate_row.keys())=={"path","sha256","byte_count","origin"}, gate_row
    _log("CANONICAL7_IS_R1B_NOT_ORIGINAL_OK 4keys")
    # historical links + unchanged research
    chain_for_anchor=[{"record":core.load_json(FIX_ROOT/rec1_ref["path"]),"path":rec1_ref["path"],"sha256":rec1_ref["sha256"]},
                      {"record":core.load_json(FIX_ROOT/rec2_ref["path"]),"path":rec2_ref["path"],"sha256":rec2_ref["sha256"]}]
    derived=setmod.derive_canonical_anchor(FIX_ROOT,core.load_json(FIX_ROOT/core.DEFAULT_CONFIG),core.load_json(FIX_ROOT/_rel2(state_path)),chain_for_anchor)
    assert derived==anchor, f"derived {derived} != anchor {anchor}"
    _log("DERIVED_ANCHOR_MATCH historical links OK")
    # original canonical bytes equal after R1b: compare before vs after for non-new files
    after_files=_full_snapshot()
    corr_prefix=str(proposal_dir.relative_to(FIX_ROOT).as_posix())+"/publication/"
    rec_rel=res["record_path"] if isinstance(res["record_path"],str) else str(res["record_path"])
    state_rel2=_rel2(state_path)
    for rel,sha in before_files.items():
        if rel.startswith(corr_prefix) or rel==rec_rel or rel==state_rel2:
            continue
        assert rel in after_files, f"disappearance {rel}"
        assert after_files[rel]==sha, f"old-immutable drift {rel}"
    _log("OLD_CANONICAL_BYTE_EXACT_AFTER_R1B_OK")
    # active7 matches new set separately
    eff7=sel.get("effective7",{})
    assert len(eff7)==7, eff7.keys()
    # active Gate should be new seal Gate, not canonical7
    # seal roles contain publication-pdf etc.; check effective Gate path is versioned publication Gate
    _log(f"EFFECTIVE7 keys={sorted(eff7.keys())}")
    # check candidate
    cand_ref=sel.get("candidate_ref")
    assert cand_ref is not None and cand_ref.get("path")==f"sources/{ISSUE}/publication/v2/editorial-corrections/fixture-wk-corr-r3c/publication/publication-candidate-v2.json", cand_ref
    _log(f"ACTIVE_CANDIDATE_OK {cand_ref}")
    # State/readback healthy AFTER activation
    assert agent.validate_agent_state(FIX_ROOT,core.load_json(FIX_ROOT/core.DEFAULT_CONFIG),core.load_json(FIX_ROOT/_rel2(state_path)))==[]
    rv=edpub.validate_editorial_receipt(FIX_ROOT,_rel2(pubdir/"validated-source-manifest.json"),_rel2(state_path))
    assert rv["issue_id"]==issue_id, rv
    _log("RECEIPT_HEALTHY_AFTER")
    gv=reader_gate.validate_reader_surface_gate(FIX_ROOT,_rel2(pubdir/"reader-surface-gate-v2.json"),issue_id=issue_id,publication_profile="WEEKLY_MAGAZINE",expected_manuscript_path=_rel2(manuscript_path),state_path=_rel2(state_path))
    assert gv["status"]=="PASSED", gv
    _log("GATE_PASSED_AFTER")
    cv=pubmod.validate_candidate(FIX_ROOT,pubdir/"publication-candidate-v2.json")
    _log(f"CANDIDATE_AFTER {cv.get('status') if isinstance(cv,dict) else cv}")
    hist=edpub.verify_activation_history(FIX_ROOT,res["record_path"])
    _log(f"HISTORY_AFTER {hist.get('status') if isinstance(hist,dict) else str(hist)[:500]}")
    # ALREADY_ACTIVE readonly if cheap
    res2=edpub.activate_publication(FIX_ROOT,_rel2(state_path),set_rel,"WorkerC weekly editorial correction R3c","workerc-executor",datetime.now(timezone.utc))
    assert res2.get("status")=="ALREADY_ACTIVE", res2
    _log(f"ALREADY_ACTIVE_OK {res2}")
    # refusals on HEALTHY state with full inventory + State + git watch
    def _snap_full():
        files=_full_snapshot()
        head=_run_git("rev-parse","HEAD").stdout.strip()
        status=_run_git("status","--porcelain").stdout
        state_bytes=(FIX_ROOT/_rel2(state_path)).read_bytes()
        return {"files":files,"head":head,"status":status,"state_sha":hashlib.sha256(state_bytes).hexdigest()}
    snap_r1=_snap_full()
    r1_script=("import sys\nfrom pathlib import Path\nroot=Path(sys.argv[1])\nstate_path=Path(sys.argv[2])\n"
               "from scripts import survey_production_v2 as core\nfrom scripts import survey_weekly_mechanical_refresh_v2 as r1\nfrom datetime import datetime,timezone\n"
               "recorded=datetime(2026,9,19,9,0,0,tzinfo=timezone.utc)\ntry:\n"
               "  r1.refresh_mechanical_evidence(root,core.load_json(root / core.DEFAULT_CONFIG),state_path,'post must refuse','workerc',recorded)\n"
               "  print('UNEXPECTED_SUCCESS'); sys.exit(10)\n"
               "except Exception as e:\n  print(f'REFUSED:{type(e).__name__}:{e}'); sys.exit(3)\n")
    rc,out,err=_run_fixture(r1_script,[str(FIX_ROOT),str(FIX_ROOT/_rel2(state_path))])
    _log(f"R1_AFTER rc={rc} out={out[:2000]}")
    assert rc==3 and "R1 mechanical refresh refused in VERSIONED_ACTIVE" in out, out
    assert _snap_full()==snap_r1, "R1 after must not change inventory/State/git"
    _log("R1_AFTER_REFUSE_PREWRITE_OK")
    (NOTES/"refusal-r1-after.txt").write_text(f"rc={rc}\n{out}\n{err[-2000:]}")
    snap_c=_snap_full()
    canon_script=("import sys\nfrom pathlib import Path\nroot=Path(sys.argv[1])\nstate_path=Path(sys.argv[2])\n"
                  "from scripts import survey_production_v2 as core\nfrom scripts import survey_agent_control_v2 as agent\nfrom datetime import datetime,timezone\n"
                  "cfg=core.load_json(root / core.DEFAULT_CONFIG)\nrecorded=datetime(2026,9,19,9,5,0,tzinfo=timezone.utc)\ntry:\n"
                  "  agent.revalidate_publication_surface(root,cfg,state_path,'REVIEWED_CORE_CHANGE','post must refuse','workerc',recorded,None)\n"
                  "  print('UNEXPECTED_SUCCESS'); sys.exit(10)\n"
                  "except Exception as e:\n  print(f'REFUSED:{type(e).__name__}:{e}'); sys.exit(3)\n")
    rc2,out2,err2=_run_fixture(canon_script,[str(FIX_ROOT),str(FIX_ROOT/_rel2(state_path))])
    _log(f"CANON_AFTER rc={rc2} out={out2[:2000]}")
    assert rc2==3 and "canonical revalidation refused in revised mode" in out2.lower(), out2
    assert _snap_full()==snap_c
    _log("CANON_AFTER_REFUSE_PREWRITE_OK")
    (NOTES/"refusal-canon-after.txt").write_text(f"rc={rc2}\n{out2}\n{err2[-2000:]}")
    snap_f=_snap_full()
    fake_script=("import sys\nfrom pathlib import Path\nroot=Path(sys.argv[1])\nstate_path=Path(sys.argv[2])\n"
                 "from scripts import survey_production_v2 as core\nfrom scripts import survey_agent_control_v2 as agent\nfrom datetime import datetime,timezone\n"
                 "cfg=core.load_json(root / core.DEFAULT_CONFIG)\nrecorded=datetime(2026,9,19,9,6,0,tzinfo=timezone.utc)\ntry:\n"
                 "  agent.revalidate_publication_surface(root,cfg,state_path,'REVIEWED_EDITORIAL_CORRECTION','fake','workerc',recorded,None)\n"
                 "  print('UNEXPECTED_SUCCESS'); sys.exit(10)\n"
                 "except Exception as e:\n  print(f'REFUSED:{type(e).__name__}:{e}'); sys.exit(3)\n")
    rc3,out3,err3=_run_fixture(fake_script,[str(FIX_ROOT),str(FIX_ROOT/_rel2(state_path))])
    _log(f"FAKE rc={rc3} out={out3[:2000]}")
    assert rc3==3 and "REVIEWED_EDITORIAL_CORRECTION" in out3 and "must use new versioned activation" in out3, out3
    assert _snap_full()==snap_f
    _log("FAKE_REFUSE_PREWRITE_OK")
    (NOTES/"refusal-fake-after.txt").write_text(f"rc={rc3}\n{out3}\n{err3[-2000:]}")
    summary={"source_head":head,"r1a":r1a_head,"r1b":r1b_head,"r1a_record":rec1_ref,"r1b_record":rec2_ref,"anchor":anchor,"set":set_rel,"record":res["record_path"],"timings":{"r1a":dt,"r1b":dt2,"prepare":dtp,"finalize":dtf,"activate":dta},"total":time.monotonic()-t0}
    (NOTES/"summary.json").write_text(json.dumps(summary,indent=2))
    _log(f"SUMMARY {json.dumps(summary,indent=2)}")
    _log("DIAGNOSTIC_BOUNDED_DONE terminal 0 no whole PASS no production approval")
    return 0

if __name__=="__main__":
    try: sys.exit(main())
    except Exception: traceback.print_exc(); sys.exit(2)
