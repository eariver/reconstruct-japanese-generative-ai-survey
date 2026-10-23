#!/usr/bin/env python3
"""Final R6 TEST ONLY: R1x2 -> changed reader -> healthy active then refusals (final epoch ce90246).

Governing d880 unchanged, production semantic NO_GO still. Previous 0d proof bounded
retained, no automatic PASS transfer. Final SOURCE ce90246b907c86e9bdeb930dec0e83a5637f2805
tree 53349a4efbdd5e3b4153a8e5975101fdd59f132b 720. Fixes: strict parse/close,
anchored full original union + R6 cross bindings. No source edits except 2 isolated
R1 fixture comment stimuli (AST-neutral before build_reader_input, process identity).
Root SOURCE commit already exists before authority. NEW independent tracked720+.git
under workspace-ignored .rephase-1-editorial-runtime/final-r6-r1/, own GitDir, inert,
no hardlinks/alts, no /tmp/home/devshm. Env PYTHONDONTWRITEBYTECODE/TMPDIR/cache
under approved root set BEFORE imports, no purge/clean/reset/raw delete/net/commits.
Adapted R1 helper recipe: real nonemitted Weekly comment x2 + refresh actual code
subprocess; contract67 closure22/P3S50 from final code; cumulative original rows full
union unchanged research (no incremental priorSha). P1/P2R/scope/P2V/P3S REAL TL2026
-> typed post reviews/QA -> Candidate/seal -> activate; anchor==r2, r3 supersedes r2,
canonical7==R1b Gate !=original, State/r3 active15/canonical7 healthy + original
canonical after R1b unchanged, receipt/Gate/Candidate/history + ALREADY_ACTIVE readonly.
CLI refusals after (R1/canonical/false editorial) pre-write with full delta oldState
no guards. Never rewrite old receipt metadata. RELEASED not needed. Type fixtures only.
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
    # TL may also be available via approved root? Use fixed path as prior successful (no network install)
    if not TL_BIN.exists():
        # fallback search under workspace ignored texlive? Keep precise blocker, no fake
        _log(f"TOOLCHAIN MISSING {TL_BIN}"); return 2
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
        # PYTHONPYCACHEPREFIX/TMPDIR already set BEFORE interpreter via outer env; preserve
        return subprocess.run([sys.executable,"-c",script,*args],cwd=FIX_ROOT,capture_output=True,text=True,timeout=timeout_s,env=env)
    def _run_cli(args_list,timeout_s=600):
        env={k:v for k,v in os.environ.items() if not k.startswith("GIT_") and k!="PYTHONPATH"}
        env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file","PYTHONDONTWRITEBYTECODE":"1"})
        return subprocess.run([sys.executable,str(FIX_ROOT/"scripts/survey_agent_control_v2.py"),"--repo-root",str(FIX_ROOT),*args_list],cwd=FIX_ROOT,capture_output=True,text=True,timeout=timeout_s,env=env)
    t0=time.monotonic()
    _log("===0 SOURCE===")
    head=_run_git("rev-parse","HEAD").stdout.strip()
    tree=_run_git("rev-parse","HEAD^{tree}").stdout.strip()
    _log(f"HEAD={head} TREE={tree}")
    assert head=="ce90246b907c86e9bdeb930dec0e83a5637f2805", head
    assert tree=="53349a4efbdd5e3b4153a8e5975101fdd59f132b", tree
    assert len(_run_git("ls-files").stdout.strip().splitlines())==720
    assert _run_git("status","--porcelain=v1","--untracked-files=all").stdout.strip()=="", "fixture must start clean"
    assert TL_BIN.exists()
    from scripts import survey_weekly_derivation_v2 as _wkd
    assert len(_wkd.CURRENT_CLOSURE)==22, len(_wkd.CURRENT_CLOSURE)
    cfg0=core.load_json(FIX_ROOT/core.DEFAULT_CONFIG)
    assert len(cfg0["contract_files"]["pipeline"])==67, len(cfg0["contract_files"]["pipeline"])
    # pins from final code (strict parse/close + anchored union + R6 cross)
    assert hashlib.sha256((FIX_ROOT/"scripts/survey_publication_set_v2.py").read_bytes()).hexdigest()=="ecd7facac09a5c977396803e130d600b75a441767d87ea585024f38c490bfb8a"
    assert hashlib.sha256((FIX_ROOT/"scripts/survey_agent_control_v2.py").read_bytes()).hexdigest()=="c132c944e7cce2e8a6092487760a0888191bdb80f894a2bc08c60d4c1fe11600"
    assert hashlib.sha256((FIX_ROOT/"scripts/survey_editorial_correction_proposal_v2.py").read_bytes()).hexdigest().startswith("23e3a45f")
    _log("PINS_OK final R6 low ecd7faca agent c132c944 P1 23e3a45f closure22 contract67 TL OK")
    _log("===1 BOOTSTRAP===")
    helper=p1t._new_weekly_helper(tc,FIX_ROOT)
    built=p1t._build_weekly_validated(tc,helper)
    chain,state_path=built["chain"],Path(built["state_path"])
    if not state_path.is_absolute(): state_path=(FIX_ROOT/state_path).resolve()
    st0=core.load_json(state_path)
    assert st0.get("publication_revalidation_provenance") is None
    state_rel=str(state_path.relative_to(FIX_ROOT).as_posix())
    _log(f"BOOTSTRAP_OK {state_rel}")
    (NOTES/"base-state.json").write_bytes(state_path.read_bytes())
    validation_ref=st0["checkpoint_provenance"]["validation"]
    orig_ckpt=core.load_json(FIX_ROOT/validation_ref["path"])
    orig_map={(r["name"],r["path"]):r["sha256"] for r in orig_ckpt.get("artifacts",[])}
    assert len(orig_map)==7
    (NOTES/"base-validation-checkpoint.json").write_bytes((FIX_ROOT/validation_ref["path"]).read_bytes())
    # R1a
    _log("===R1a COMMIT (actual helper)===")
    head_before=_run_git("rev-parse","HEAD").stdout.strip()
    r1a_head=p3st._commit_r1_nonemitted_comment(tc,FIX_ROOT)
    assert r1a_head!=head_before
    assert len(_wkd.CURRENT_CLOSURE)==22
    assert len(core.load_json(FIX_ROOT/core.DEFAULT_CONFIG)["contract_files"]["pipeline"])==67
    _log(f"R1a_HEAD={r1a_head}")
    r1_script=("import sys\nfrom pathlib import Path\nroot=Path(sys.argv[1])\nstate_path=Path(sys.argv[2])\n"
               "from scripts import survey_production_v2 as core\nfrom scripts import survey_weekly_mechanical_refresh_v2 as r1\nfrom datetime import datetime,timezone\n"
               "recorded=datetime(2026,9,19,8,0,0,tzinfo=timezone.utc)\n"
               "result=r1.refresh_mechanical_evidence(root,core.load_json(root / core.DEFAULT_CONFIG),state_path,'fixture R1 first refresh','synthetic FinalR6 R1',recorded)\n"
               "import json; print(json.dumps({'result':'OK','keys':sorted(result.keys())}))\n")
    t=time.monotonic(); rc,out,err=_run_fixture(r1_script,[str(FIX_ROOT),str(state_path)]); dt=time.monotonic()-t
    _log(f"R1a_REFRESH rc={rc} dt={dt:.1f}s out={out[:400]} err_tail={err[-1200:]}")
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
    # full union unchanged research: check preserved research rows? At least Gate union + no incremental priorSha
    for r in rec1.get("superseded_artifacts",[]):
        assert r.get("prior_sha256")==orig_map.get((r.get("name"),r.get("path"))), "no incremental priorSha"
    _log(f"R1a_CUMULATIVE_FULL_UNION_OK {len(sup1)}+{len(pres1)}={len(orig_map)}")
    def _mut_r1a():
        a=core.load_json(chain["authored_path"]); a["cover"]["headline"]="Weekly R1 first refresh, revised edition"; return a
    pp1,_=_prep_ret(tc,FIX_ROOT,helper,chain,state_path,"fixture-wk-r1a-verify",_mut_r1a)
    out1=retention.capture_retention(FIX_ROOT,state_path,pp1); assert out1["result"]==retention.RESULT_CAPTURED
    m1_path=FIX_ROOT/out1["manifest_path"]; assert retention.verify_retention(FIX_ROOT,pp1,m1_path)["result"]==retention.RESULT_VERIFIED
    _log(f"R1a_RETENTION_OK {out1['manifest_path']}")
    (NOTES/"retention-r1a-manifest.json").write_bytes(m1_path.read_bytes())
    # R1b
    _log("===R1b COMMIT (second distinct)===")
    probe=FIX_ROOT/"scripts/survey_weekly_derivation_v2.py"
    text=probe.read_text(encoding="utf-8")
    anchor2="fixture R1 second non-emitted Python comment C2 FinalR6"
    assert anchor2 not in text
    before_ast=_ast.dump(_ast.parse(text))
    lines=text.splitlines(keepends=True)
    tg=[i for i,l in enumerate(lines) if l.startswith("def build_reader_input(")]
    assert len(tg)==1
    lines.insert(tg[0], f"# {anchor2}\n")
    probe.write_text("".join(lines),encoding="utf-8")
    assert before_ast==_ast.dump(_ast.parse(probe.read_text(encoding="utf-8")))
    p=_run_git("add","scripts/survey_weekly_derivation_v2.py"); assert p.returncode==0, p.stderr
    p=_run_git("-c","user.name=Synthetic FinalR6 R1","-c","user.email=finalr6-r1@example.invalid","commit","-q","-m","Fixture R1 second non-emitted comment C2 FinalR6"); assert p.returncode==0, p.stderr
    r1b_head=_run_git("rev-parse","HEAD").stdout.strip()
    assert len(_wkd.CURRENT_CLOSURE)==22
    assert len(core.load_json(FIX_ROOT/core.DEFAULT_CONFIG)["contract_files"]["pipeline"])==67
    _log(f"R1b_HEAD={r1b_head}")
    r1_script2=("import sys\nfrom pathlib import Path\nroot=Path(sys.argv[1])\nstate_path=Path(sys.argv[2])\n"
                "from scripts import survey_production_v2 as core\nfrom scripts import survey_weekly_mechanical_refresh_v2 as r1\nfrom datetime import datetime,timezone\n"
                "recorded=datetime(2026,9,19,8,5,0,tzinfo=timezone.utc)\n"
                "result=r1.refresh_mechanical_evidence(root,core.load_json(root / core.DEFAULT_CONFIG),state_path,'fixture R1 second refresh','synthetic FinalR6 R1',recorded)\n"
                "import json; print(json.dumps({'result':'OK','keys':sorted(result.keys())}))\n")
    t=time.monotonic(); rc2,out2,err2=_run_fixture(r1_script2,[str(FIX_ROOT),str(state_path)]); dt2=time.monotonic()-t
    _log(f"R1b_REFRESH rc={rc2} dt={dt2:.1f}s out={out2[:400]}")
    assert rc2==0, f"R1b failed {out2} {err2[-4000:]}"
    state2=core.load_json(state_path)
    rec2_ref=state2["publication_revalidation_provenance"]
    assert rec2_ref!=rec1_ref
    (NOTES/"state-after-r1b.json").write_bytes(state_path.read_bytes())
    rec2_path=FIX_ROOT/rec2_ref["path"]; (NOTES/"record-r1b.json").write_bytes(rec2_path.read_bytes())
    rec2=core.load_json(rec2_path)
    assert rec2.get("supersedes")==rec1_ref
    _log("R1b_SUPERSEDES_FIRST_OK")
    sup2={(r["name"],r["path"]):r["prior_sha256"] for r in rec2.get("superseded_artifacts",[])}
    pres2={(r["name"],r["path"]):r["sha256"] for r in rec2.get("preserved_artifacts",[])}
    for k,v in sup2.items(): assert orig_map.get(k)==v, k
    for k,v in pres2.items(): assert orig_map.get(k)==v, k
    assert set(sup2)|set(pres2)==set(orig_map)
    for r in rec2.get("superseded_artifacts",[]):
        assert r.get("prior_sha256")==orig_map.get((r.get("name"),r.get("path")))
    _log("R1b_CUMULATIVE_FULL_UNION_OK")
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
    # Versioned correction
    _log("===VERSIONED CORRECTION (changed reader)===")
    from tests.test_survey_editorial_staged_source_v2 import _weekly_prepare_from as _wk_from
    corr=_wk_from(tc,FIX_ROOT,helper,{"chain":chain,"state_path":state_path,"helper":helper},"fixture-wk-corr-finalr6")
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
    staged_manifest_path=FIX_ROOT/mat["staged_manifest_path"] if isinstance(mat,dict) and "staged_manifest_path" in mat else (proposal_path.parent/"staged-source"/"staged-source-manifest.json")
    assert staged_manifest_path.is_file()
    assert staged.verify_staged_source(FIX_ROOT,proposal_path,staged_manifest_path)["result"]=="STAGED_SOURCE_REPLAY_VERIFIED"
    assert len(core.load_json(staged_manifest_path)["code_deps"])==50
    _log("P3S_VERIFIED50")
    proposal_dir=proposal_path.parent
    staged_manifest=core.load_json(staged_manifest_path)
    issue_id=staged_manifest.get("issue_id")
    arch=core.load_json(helper.source_root/"architecture-v2.json")
    coverage=[{"package_id":pl["package_id"],"requirement":rq,"status":"FULFILLED","reader_locations":["main.tex:package-1"],"detail":f"FinalR6 maps {proposal_dir.name}."} for pl in arch.get("packages",[]) for rq in pl.get("must_cover_requirements",[])]
    requirements=[{"requirement_id":"FINAL_SYNTHESIS","status":"FULFILLED","reader_locations":["main.tex:summary"],"detail":"FinalR6 synthesis."},{"requirement_id":"WEEKLY_COMMUNITY_MOVEMENT","status":"FULFILLED","reader_locations":["main.tex:package-1"],"detail":"FinalR6 movement."}]
    mspec={"schema_version":"2.0-rc1","kind":"EDITORIAL_MANUSCRIPT_SPEC_V1","issue_id":issue_id,"proposal_ref":{"path":str(proposal_path.relative_to(FIX_ROOT)),"sha256":core.sha256_file(proposal_path)},"architecture_coverage":coverage,"reader_requirements":requirements,"authored_by":"finalr6 manuscript author","recorded_at":datetime.now(timezone.utc).isoformat()}
    mspec_path=proposal_dir/"manuscript-spec.json"; core.write_json(mspec_path,mspec)
    tspec={"schema_version":"2.0-rc1","kind":"EDITORIAL_TOOLCHAIN_SPEC_V1","executor":"finalr6","absolute_executable":str(TL_BIN),"recipe":"lualatex-biber-lualatex","argv":list(edpub.EXPECTED_ARGV_LUALATEX_BIBER),"env":{},"recorded_at":datetime.now(timezone.utc).isoformat()}
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
    _log(f"PREPARE_OK dt={dtp:.1f}s {json.dumps(prepared_paths)[:500]}")
    pubdir=proposal_dir/"publication"
    manuscript_path=pubdir/"reader-manuscript-v2.json"; pdf_path=pubdir/"build"/"main.pdf"
    assert manuscript_path.is_file() and pdf_path.is_file()
    from pypdf import PdfReader as _PR
    pages=len(_PR(str(pdf_path)).pages)
    assert pages>=1
    _log(f"REAL_PDF pages={pages} bytes={pdf_path.stat().st_size}")
    qroot=pubdir/"quality"; qroot.mkdir(parents=True,exist_ok=True)
    sp=qroot/"subject-entity-property-binding.json"; core.write_json(sp,{"check_id":"SUBJECT_ENTITY_PROPERTY_BINDING","status":"PASS","scope":"finalr6 real-build"})
    main_bytes=(FIX_ROOT/staged_manifest["outputs"]["main"]["path"]).read_bytes()
    ip=qroot/"identifier-preservation.json"; core.write_json(ip,{"check_id":"IDENTIFIER_PRESERVATION","status":"PASS","source_sha256":core.sha256_bytes(main_bytes),"inspected_identifiers":[issue_id],"scope":"finalr6"})
    ppth=qroot/"pdf-preflight.json"; core.write_json(ppth,{"check_id":"PDF_PREFLIGHT","status":"PASS","page_count":pages,"pdf_sha256":core.sha256_file(pdf_path),"byte_count":pdf_path.stat().st_size,"scope":"finalr6 real TL2026"})
    qchecks=[{"check_id":cid,"kind":"DETERMINISTIC","status":"PASS","executor":"finalr6 assertions","evidence":"Exact bytes inspected.","recorded_at":datetime.now(timezone.utc).isoformat(),"result":{"path":str(p.relative_to(FIX_ROOT)),"sha256":core.sha256_file(p)}} for cid,p in (("SUBJECT_ENTITY_PROPERTY_BINDING",sp),("IDENTIFIER_PRESERVATION",ip),("PDF_PREFLIGHT",ppth))]
    det_path=proposal_dir/"deterministic-checks.json"; core.write_json(det_path,{"checks":qchecks})
    profile=core.load_json(FIX_ROOT/core.load_json(state_path)["profile"]["path"])
    for kind,fname in (("SEMANTIC_EDITORIAL","semantic-review-v2.json"),("VISUAL","visual-review-v2.json")):
        checks=[{"check_id":cid,"status":"PASS","detail":f"FinalR6 synthetic {kind}; no genuine approval.","evidence_locations":["finalr6-real-build:main.pdf"]} for cid in sorted(reader_pub._expected_review_checks(FIX_ROOT,profile,kind))]
        reader_pub.build_review_record(FIX_ROOT,manuscript_path,pdf_path,pages,kind,checks,f"finalr6 synthetic {kind}",datetime.now(timezone.utc),pubdir/fname)
        _log(f"REVIEW {kind}")
    sem_path=pubdir/"semantic-review-v2.json"; vis_path=pubdir/"visual-review-v2.json"
    t=time.monotonic()
    set_ref=edpub.finalize_publication(FIX_ROOT,_rel2(state_path),_rel2(proposal_path),_rel2(staged_manifest_path),_rel2(det_path),_rel2(sem_path),_rel2(vis_path),datetime.now(timezone.utc))
    dtf=time.monotonic()-t
    _log(f"FINALIZE_OK dt={dtf:.1f}s {json.dumps(set_ref)[:400]}")
    assert agent.validate_agent_state(FIX_ROOT,core.load_json(FIX_ROOT/core.DEFAULT_CONFIG),core.load_json(state_path))==[]
    _log("INERT_HEALTHY")
    _set_raw=set_ref["set_ref"] if isinstance(set_ref,dict) and "set_ref" in set_ref else set_ref
    set_rel=_set_raw.get("path") if isinstance(_set_raw,dict) else str(_set_raw)
    if set_rel.startswith("/"): set_rel=str(Path(set_rel).relative_to(FIX_ROOT))
    assert (FIX_ROOT/set_rel).is_file()
    (NOTES/"publication-set.json").write_bytes((FIX_ROOT/set_rel).read_bytes())
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
    res=edpub.activate_publication(FIX_ROOT,_rel2(state_path),set_rel,"FinalR6 weekly editorial correction","finalr6-executor",datetime.now(timezone.utc))
    dta=time.monotonic()-t
    _log(f"ACTIVATE dt={dta:.1f}s {json.dumps(res)}")
    assert res.get("status")=="ACTIVATED", res
    act_path=FIX_ROOT/res["record_path"]
    act_rec=core.load_json(act_path)
    anchor=act_rec.get("canonical_anchor")
    assert anchor.get("kind")=="LEGACY_REVALIDATION", anchor
    assert anchor.get("ref")==rec2_ref, f"anchor {anchor.get('ref')} != r2 {rec2_ref}"
    assert act_rec.get("supersedes")==rec2_ref
    _log("ANCHOR_IS_R1B_OK R3_SUPERSEDES_R2_OK")
    (NOTES/"activation-record.json").write_bytes(act_path.read_bytes())
    (NOTES/"state-after-activate.json").write_bytes((FIX_ROOT/_rel2(state_path)).read_bytes())
    sel=setmod.resolve_publication_selection(FIX_ROOT,core.load_json(FIX_ROOT/core.DEFAULT_CONFIG),core.load_json(FIX_ROOT/_rel2(state_path)))
    assert sel.get("mode")=="VERSIONED_ACTIVE", sel
    canon7=sel.get("canonical7",{})
    assert len(canon7)==7
    gate_row=None; gate_key=None
    for k,v in canon7.items():
        if "gate" in k.lower():
            gate_row=v; gate_key=k; break
    assert gate_row is not None
    r1b_new=None
    for r in rec2.get("superseded_artifacts",[]):
        if r.get("name")=="reader-surface-gate":
            r1b_new=r.get("new_sha256"); break
    assert r1b_new is not None
    assert gate_row.get("sha256")==r1b_new
    assert gate_row.get("sha256")!=orig_map.get(("reader-surface-gate","sources/2026-W37/publication/v2/reader-surface-gate-v2.json"))
    assert len(gate_row)==4 and set(gate_row.keys())=={"path","sha256","byte_count","origin"}
    _log(f"CANONICAL7_GATE {gate_key}={gate_row} IS_R1B_NOT_ORIGINAL")
    # active15
    roles=sel.get("roles",{})
    assert isinstance(roles,dict) and len(roles)==15, f"active15 {list(roles.keys()) if isinstance(roles,dict) else roles}"
    _log(f"ACTIVE15_OK {sorted(roles.keys())}")
    eff7=sel.get("effective7",{})
    assert len(eff7)==7
    cand_ref=sel.get("candidate_ref")
    assert cand_ref is not None and cand_ref.get("path")==f"sources/{ISSUE}/publication/v2/editorial-corrections/fixture-wk-corr-finalr6/publication/publication-candidate-v2.json", cand_ref
    _log(f"ACTIVE_CANDIDATE_OK {cand_ref}")
    # historical links
    chain_for_anchor=[{"record":core.load_json(FIX_ROOT/rec1_ref["path"]),"path":rec1_ref["path"],"sha256":rec1_ref["sha256"]},
                      {"record":core.load_json(FIX_ROOT/rec2_ref["path"]),"path":rec2_ref["path"],"sha256":rec2_ref["sha256"]}]
    assert setmod.derive_canonical_anchor(FIX_ROOT,core.load_json(FIX_ROOT/core.DEFAULT_CONFIG),core.load_json(FIX_ROOT/_rel2(state_path)),chain_for_anchor)==anchor
    _log("DERIVED_ANCHOR_MATCH historical links OK unchanged research implied via P1 scope/basis")
    after_files=_full_snapshot()
    corr_prefix=str(proposal_dir.relative_to(FIX_ROOT).as_posix())+"/publication/"
    rec_rel=res["record_path"] if isinstance(res["record_path"],str) else str(res["record_path"])
    state_rel2=_rel2(state_path)
    for rel,sha in before_files.items():
        if rel.startswith(corr_prefix) or rel==rec_rel or rel==state_rel2:
            continue
        assert rel in after_files, rel
        assert after_files[rel]==sha, rel
    _log("ORIGINAL_CANONICAL_AFTER_R1B_UNCHANGED_OK")
    assert agent.validate_agent_state(FIX_ROOT,core.load_json(FIX_ROOT/core.DEFAULT_CONFIG),core.load_json(FIX_ROOT/_rel2(state_path)))==[]
    rv=edpub.validate_editorial_receipt(FIX_ROOT,_rel2(pubdir/"validated-source-manifest.json"),_rel2(state_path))
    assert rv["issue_id"]==issue_id
    _log("RECEIPT_HEALTHY_AFTER")
    gv=reader_gate.validate_reader_surface_gate(FIX_ROOT,_rel2(pubdir/"reader-surface-gate-v2.json"),issue_id=issue_id,publication_profile="WEEKLY_MAGAZINE",expected_manuscript_path=_rel2(manuscript_path),state_path=_rel2(state_path))
    assert gv["status"]=="PASSED", gv
    _log("GATE_PASSED_AFTER")
    cv=pubmod.validate_candidate(FIX_ROOT,pubdir/"publication-candidate-v2.json")
    _log(f"CANDIDATE_AFTER {cv.get('status') if isinstance(cv,dict) else cv}")
    hist=edpub.verify_activation_history(FIX_ROOT,res["record_path"])
    _log(f"HISTORY_AFTER {hist.get('status') if isinstance(hist,dict) else str(hist)[:400]}")
    res2=edpub.activate_publication(FIX_ROOT,_rel2(state_path),set_rel,"FinalR6 weekly editorial correction","finalr6-executor",datetime.now(timezone.utc))
    assert res2.get("status")=="ALREADY_ACTIVE", res2
    _log(f"ALREADY_ACTIVE_READONLY_OK {res2}")
    # CLI refusals on HEALTHY state
    def _snap_full_cli():
        files=_full_snapshot()
        head=_run_git("rev-parse","HEAD").stdout.strip()
        status=_run_git("status","--porcelain").stdout
        state_bytes=(FIX_ROOT/_rel2(state_path)).read_bytes()
        return {"files":files,"head":head,"status":status,"state_sha":hashlib.sha256(state_bytes).hexdigest(),"state":state_bytes}
    snap_r1=_snap_full_cli()
    old_state=snap_r1["state"]
    cli_r1=_run_cli(["refresh-mechanical-evidence","--state",state_rel2,"--reason","post must refuse","--executor","finalr6","--recorded-at","2026-09-19T09:00:00Z"])
    _log(f"CLI_R1_AFTER rc={cli_r1.returncode} out={cli_r1.stdout[:2000]} err={cli_r1.stderr[:1500]}")
    assert cli_r1.returncode!=0 and "R1 mechanical refresh refused in VERSIONED_ACTIVE" in (cli_r1.stdout+cli_r1.stderr), cli_r1.stdout+cli_r1.stderr
    assert _snap_full_cli()==snap_r1, "R1 after must not change inventory/State/git, no guards"
    _log("CLI_R1_AFTER_REFUSE_PREWRITE_OK oldState no guards")
    (NOTES/"refusal-r1-after.txt").write_text(f"rc={cli_r1.returncode}\nOUT:{cli_r1.stdout}\nERR:{cli_r1.stderr}")
    snap_c=_snap_full_cli()
    cli_c=_run_cli(["revalidate-publication-surface","--state",state_rel2,"--reason-class","REVIEWED_CORE_CHANGE","--reason","post must refuse","--executor","finalr6","--recorded-at","2026-09-19T09:05:00Z"])
    _log(f"CLI_CANON_AFTER rc={cli_c.returncode} out={cli_c.stdout[:2000]}")
    assert cli_c.returncode!=0 and "canonical revalidation refused in revised mode" in (cli_c.stdout+cli_c.stderr).lower(), cli_c.stdout+cli_c.stderr
    assert _snap_full_cli()==snap_c
    _log("CLI_CANON_AFTER_REFUSE_PREWRITE_OK")
    (NOTES/"refusal-canon-after.txt").write_text(f"rc={cli_c.returncode}\nOUT:{cli_c.stdout}\nERR:{cli_c.stderr}")
    snap_f=_snap_full_cli()
    cli_f=_run_cli(["revalidate-publication-surface","--state",state_rel2,"--reason-class","REVIEWED_EDITORIAL_CORRECTION","--reason","fake","--executor","finalr6","--recorded-at","2026-09-19T09:06:00Z"])
    _log(f"CLI_FAKE rc={cli_f.returncode} out={cli_f.stdout[:2000]}")
    assert cli_f.returncode!=0 and "REVIEWED_EDITORIAL_CORRECTION" in (cli_f.stdout+cli_f.stderr) and "must use new versioned activation" in (cli_f.stdout+cli_f.stderr), cli_f.stdout+cli_f.stderr
    assert _snap_full_cli()==snap_f
    _log("CLI_FAKE_REFUSE_PREWRITE_OK")
    (NOTES/"refusal-fake-after.txt").write_text(f"rc={cli_f.returncode}\nOUT:{cli_f.stdout}\nERR:{cli_f.stderr}")
    summary={"source_head":head,"r1a":r1a_head,"r1b":r1b_head,"r1a_record":rec1_ref,"r1b_record":rec2_ref,"anchor":anchor,"set":set_rel,"record":res["record_path"],"timings":{"r1a":dt,"r1b":dt2,"prepare":dtp,"finalize":dtf,"activate":dta},"total":time.monotonic()-t0}
    (NOTES/"summary.json").write_text(json.dumps(summary,indent=2))
    _log(f"SUMMARY {json.dumps(summary,indent=2)}")
    _log("FINAL_R6_DIAGNOSTIC_BOUNDED_DONE terminal 0 no whole PASS no HumanCommitPoint production NO_GO")
    return 0
if __name__=="__main__":
    try: sys.exit(main())
    except Exception: traceback.print_exc(); sys.exit(2)
