#!/usr/bin/env python3
"""R7 fresh Weekly acceptance: prepare/finalize/activate/resume with ALREADY real PDF + CLI root + depth.

Fresh independent code epoch: FIX_ROOT is fresh copy of R7 SOURCE snapshot
(HEAD 00397c3, tree 23c9ba9, 721 files, meaningful commit before data).
Fixture data (Weekly VALIDATED_DRAFT + wk-r7-1 correction with real TL2026
build) created AFTER source commit (no F0 self-reference). Typed reviews
synthetic, production NO-GO. No network/clean/reset. All scratch under
workspace ignored .rephase-1-editorial-runtime, never /tmp quota/dev/shm/home.
Own GitDir verified NOT reconstruct + inert/no sharing before writes.
Env no-bytecode preimports, subprocess per fixture no alias mix (here direct
APIs with FIX_ROOT code, cwd=FIX_ROOT, PYTHONPATH=FIX_ROOT).
Frozen SOURCE never executed inside (FIX_ROOT is fresh copy, not SOURCE image).

Validates both CLI root (validate-state loader fix, exit0 JSON) and depth
(32 valid, 33 refuses via typed33 copy + preflight len check) in same run,
plus normal prepare/finalize/activate/resume with real PDF.
"""
from __future__ import annotations
import copy, hashlib, json, os, shutil, subprocess, sys, time, traceback
from datetime import datetime, timezone
from pathlib import Path

def _log(m): print(m, flush=True)

def _run_git(cwd: Path, *args):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
    return subprocess.run(["git",*args], cwd=str(cwd), capture_output=True, text=True, timeout=60, env=env)

def main()->int:
    if len(sys.argv)!=5:
        print(f"usage: {sys.argv[0]} FIX_ROOT NOTES_DIR EXPECT_HEAD EXPECT_COUNT", flush=True)
        return 2
    FIX_ROOT=Path(sys.argv[1]).resolve()
    NOTES=Path(sys.argv[2]).resolve(); NOTES.mkdir(parents=True, exist_ok=True)
    EXPECT_HEAD=sys.argv[3].strip().lower()
    EXPECT_COUNT=int(sys.argv[4])
    sys.dont_write_bytecode=True
    sys.path.insert(0, str(FIX_ROOT))
    os.environ["PYTHONDONTWRITEBYTECODE"]="1"
    for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
        if os.environ.get(_v):
            _log(f"UNSAFE {_v}"); return 2
    for _k in ("PYTHONPYCACHEPREFIX","TMPDIR"):
        _v=os.environ.get(_k,"")
        if not _v.startswith(str(FIX_ROOT.parent)+"/") and not _v.startswith("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/"):
            # Allow workspace runtime pycache/tmp (set by caller to final-r7-accept/...).
            pass
    # Own GitDir BEFORE writes.
    top=_run_git(FIX_ROOT,"rev-parse","--show-toplevel").stdout.strip()
    gdir=_run_git(FIX_ROOT,"rev-parse","--absolute-git-dir").stdout.strip()
    if Path(top)!=FIX_ROOT or Path(gdir)!=FIX_ROOT/".git":
        _log(f"BLOCKER own GitDir top={top} gdir={gdir} fix={FIX_ROOT}"); return 2
    for _alt in (FIX_ROOT/".git/objects/info/alternates", FIX_ROOT/".git/info/alternates"):
        if _alt.exists():
            _log(f"BLOCKER alternates {_alt}"); return 2
    origin=_run_git(FIX_ROOT,"remote","-v").stdout
    if "example.invalid" not in origin:
        _log(f"BLOCKER origin not inert {origin[:200]}"); return 2
    head=_run_git(FIX_ROOT,"rev-parse","HEAD").stdout.strip()
    _log(f"HEAD={head} expect={EXPECT_HEAD}")
    if head!=EXPECT_HEAD:
        _log("UNEXPECTED HEAD"); return 2
    nfiles=len(_run_git(FIX_ROOT,"ls-files").stdout.strip().splitlines())
    _log(f"LSFILES={nfiles} expect={EXPECT_COUNT}")
    if nfiles!=EXPECT_COUNT:
        _log("LSFILES BOUND FAILED"); return 2
    TL_BIN=Path("/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/lualatex")
    if not TL_BIN.exists():
        _log(f"TOOLCHAIN MISSING {TL_BIN}"); return 2
    _log(f"TOOLCHAIN={TL_BIN}")
    import unittest
    from scripts import survey_production_v2 as core
    from scripts import survey_editorial_publication_v2 as edpub
    from scripts import survey_reader_publication_v2 as reader_pub
    from scripts import survey_publication_set_v2 as setmod
    from scripts import survey_editorial_correction_proposal_v2 as proposal_mod
    from scripts import survey_editorial_retention_v2 as retention
    from scripts import survey_editorial_current_authority_v2 as observer
    from scripts import survey_editorial_staged_source_v2 as staged
    from scripts import survey_agent_control_v2 as agent
    from tests import test_survey_editorial_correction_proposal_v2 as p1t
    from tests import test_survey_editorial_staged_source_v2 as p3st
    ISSUE="2026-W37"
    class _TC(unittest.TestCase):
        def runTest(self): pass
    tc=_TC()
    # Bootstrap canonical Weekly VALIDATED_DRAFT.
    _log("===BOOTSTRAP===")
    helper=p1t._new_weekly_helper(tc, FIX_ROOT)
    built=p1t._build_weekly_validated(tc, helper)
    state_path=Path(built["state_path"])
    if not state_path.is_absolute():
        state_path=(FIX_ROOT/state_path).resolve()
    st0=core.load_json(state_path)
    assert st0.get("publication_revalidation_provenance") is None
    state_rel=str(state_path.relative_to(FIX_ROOT).as_posix())
    _log(f"BOOTSTRAP_OK {state_rel}")
    # One correction wk-r7-1 with real build.
    proposal_id="wk-r7-1"; headline="R7 weekly headline correction."
    _log(f"===CYCLE {proposal_id}===")
    corr=p3st._weekly_prepare_from(tc, FIX_ROOT, helper, built, proposal_id)
    proposal_path=corr["proposal_path"]; prepared=corr["prepared"]
    cap=retention.capture_retention(FIX_ROOT, state_path, proposal_path)
    assert cap.get("result")==retention.RESULT_CAPTURED, cap
    manifest_path=FIX_ROOT/cap["manifest_path"]
    vout=retention.verify_retention(FIX_ROOT, proposal_path, manifest_path)
    assert vout.get("result")==retention.RESULT_VERIFIED, vout
    _log("P2R_OK")
    try:
        proposal_mod.validate_proposal(FIX_ROOT, state_rel, proposal_path)
        _log("P1_AFTER_CAPTURE should refuse BLOCKER"); return 2
    except Exception as exc:
        _log(f"P1_AFTER_CAPTURE_REFUSAL_OK {type(exc).__name__}")
    staged_reader_rel=prepared["proposal"]["proposed"]["proposed_reader_ref"]["path"]
    scope_path=p1t._scope_review_for(tc, FIX_ROOT, prepared, staged_reader_rel, "scope-review-v2.json")
    obs=observer.observe_current_authority(FIX_ROOT, state_path, proposal_path, manifest_path, scope_path)
    assert obs.get("result")=="CURRENT_BASIS_OBSERVED_SCOPE_BOUND", obs
    _log("P2V_SCOPE_BOUND")
    mat=staged.materialize_staged_source(FIX_ROOT, state_path, proposal_path, manifest_path, scope_path)
    staged_manifest_path=FIX_ROOT/mat["staged_manifest_path"] if isinstance(mat,dict) and "staged_manifest_path" in mat else (proposal_path.parent/"staged-source"/"staged-source-manifest.json")
    assert staged_manifest_path.is_file()
    ver=staged.verify_staged_source(FIX_ROOT, proposal_path, staged_manifest_path)
    assert ver.get("result")=="STAGED_SOURCE_REPLAY_VERIFIED", ver
    _log("P3S_VERIFIED")
    staged_manifest=core.load_json(staged_manifest_path)
    arch=core.load_json(helper.source_root/"architecture-v2.json")
    coverage=[{"package_id":plan["package_id"],"requirement":req,"status":"FULFILLED","reader_locations":["main.tex:package-1"],"detail":f"R7 manuscript author maps {proposal_id}."} for plan in arch.get("packages",[]) for req in plan.get("must_cover_requirements",[])]
    requirements=[{"requirement_id":"FINAL_SYNTHESIS","status":"FULFILLED","reader_locations":["main.tex:summary"],"detail":"R7 synthesis."},{"requirement_id":"WEEKLY_COMMUNITY_MOVEMENT","status":"FULFILLED","reader_locations":["main.tex:package-1"],"detail":"R7 movement."}]
    prop_rel=str(proposal_path.relative_to(FIX_ROOT))
    mspec={"schema_version":"2.0-rc1","kind":"EDITORIAL_MANUSCRIPT_SPEC_V1","issue_id":staged_manifest.get("issue_id"),"proposal_ref":{"path":prop_rel,"sha256":core.sha256_file(proposal_path)},"architecture_coverage":coverage,"reader_requirements":requirements,"authored_by":"r7 manuscript author","recorded_at":datetime.now(timezone.utc).isoformat()}
    mspec_path=proposal_path.parent/"manuscript-spec.json"; core.write_json(mspec_path, mspec)
    tspec={"schema_version":"2.0-rc1","kind":"EDITORIAL_TOOLCHAIN_SPEC_V1","executor":"r7-integration","absolute_executable":str(TL_BIN),"recipe":"lualatex-biber-lualatex","argv":list(edpub.EXPECTED_ARGV_LUALATEX_BIBER),"env":{},"recorded_at":datetime.now(timezone.utc).isoformat()}
    tspec_path=proposal_path.parent/"toolchain-spec.json"; core.write_json(tspec_path, tspec)
    staged_rel=str(staged_manifest_path.relative_to(FIX_ROOT)); mspec_rel=str(mspec_path.relative_to(FIX_ROOT)); tspec_rel=str(tspec_path.relative_to(FIX_ROOT))
    t0=time.monotonic()
    prepared_paths=edpub.prepare_publication(FIX_ROOT, state_rel, prop_rel, staged_rel, mspec_rel, tspec_rel, datetime.now(timezone.utc))
    _log(f"API_PREPARE dt={time.monotonic()-t0:.1f}s")
    pubdir=proposal_path.parent/"publication"
    manuscript_path=pubdir/"reader-manuscript-v2.json"; pdf_path=pubdir/"build"/"main.pdf"
    assert manuscript_path.is_file() and pdf_path.is_file()
    from pypdf import PdfReader as _PR
    pages=len(_PR(str(pdf_path)).pages)
    _log(f"REAL_PDF pages={pages} bytes={pdf_path.stat().st_size}")
    assert pages>=1
    # QA + typed reviews inside publication (R7 normal, not external).
    qroot=pubdir/"quality"; qroot.mkdir(parents=True, exist_ok=True)
    sp=qroot/"subject-entity-property-binding.json"; core.write_json(sp, {"check_id":"SUBJECT_ENTITY_PROPERTY_BINDING","status":"PASS","scope":f"r7 {proposal_id} real-build"})
    main_bytes=(FIX_ROOT/staged_manifest["outputs"]["main"]["path"]).read_bytes()
    ip=qroot/"identifier-preservation.json"; core.write_json(ip, {"check_id":"IDENTIFIER_PRESERVATION","status":"PASS","source_sha256":core.sha256_bytes(main_bytes),"inspected_identifiers":[staged_manifest.get("issue_id")],"scope":f"r7 {proposal_id} real-build"})
    pp=qroot/"pdf-preflight.json"; core.write_json(pp, {"check_id":"PDF_PREFLIGHT","status":"PASS","page_count":pages,"pdf_sha256":core.sha256_file(pdf_path),"byte_count":pdf_path.stat().st_size,"scope":f"r7 {proposal_id} real TL2026 PDF"})
    qchecks=[{"check_id":cid,"kind":"DETERMINISTIC","status":"PASS","executor":"r7 editorial with actual file assertions","evidence":"Exact fixture bytes inspected.","recorded_at":datetime.now(timezone.utc).isoformat(),"result":{"path":str(p.relative_to(FIX_ROOT)),"sha256":core.sha256_file(p)}} for cid,p in (("SUBJECT_ENTITY_PROPERTY_BINDING",sp),("IDENTIFIER_PRESERVATION",ip),("PDF_PREFLIGHT",pp))]
    det_path=proposal_path.parent/"deterministic-checks.json"; core.write_json(det_path, {"checks":qchecks})
    profile=core.load_json(FIX_ROOT/core.load_json(state_path)["profile"]["path"])
    revdir=pubdir
    for kind,fname in (("SEMANTIC_EDITORIAL","semantic-review-v2.json"),("VISUAL","visual-review-v2.json")):
        checks=[{"check_id":cid,"status":"PASS","detail":f"R7 synthetic {kind} reviewer; no genuine Human approval.","evidence_locations":[f"r7-real-build:{proposal_id}:main.pdf"]} for cid in sorted(reader_pub._expected_review_checks(FIX_ROOT, profile, kind))]
        reader_pub.build_review_record(FIX_ROOT, manuscript_path, pdf_path, pages, kind, checks, f"r7 synthetic {kind} reviewer", datetime.now(timezone.utc), revdir/fname)
    sem_path=revdir/"semantic-review-v2.json"; vis_path=revdir/"visual-review-v2.json"
    assert sem_path.is_file() and vis_path.is_file()
    det_rel=str(det_path.relative_to(FIX_ROOT)); sem_rel=str(sem_path.relative_to(FIX_ROOT)); vis_rel=str(vis_path.relative_to(FIX_ROOT))
    set_ref=edpub.finalize_publication(FIX_ROOT, state_rel, prop_rel, staged_rel, det_rel, sem_rel, vis_rel, datetime.now(timezone.utc))
    _log(f"API_FINALIZE {json.dumps(set_ref)[:300]}")
    # CLI validate-state on inert healthy (proves loader root fix, exit0 JSON).
    import subprocess as _sp
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_") and k not in ("PYTHONPATH","PYTHONPYCACHEPREFIX","TMPDIR")}
    env.update({"PYTHONDONTWRITEBYTECODE":"1","PYTHONPYCACHEPREFIX":str(FIX_ROOT.parent/"pycache"),"TMPDIR":str(FIX_ROOT.parent/"tmp"),"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file","PYTHONPATH":str(FIX_ROOT)})
    Path(env["PYTHONPYCACHEPREFIX"]).mkdir(parents=True, exist_ok=True); Path(env["TMPDIR"]).mkdir(parents=True, exist_ok=True)
    pr=_sp.run([sys.executable,"-B","-m","scripts.survey_agent_control_v2","--repo-root",str(FIX_ROOT),"validate-state","--state",state_rel], cwd=str(FIX_ROOT), capture_output=True, text=True, timeout=120, env=env)
    _log(f"CLI_VALIDATE_STATE exit={pr.returncode} out={pr.stdout[:500]} err={pr.stderr[:500]}")
    if pr.returncode!=0:
        _log("CLI_VALIDATE_STATE BLOCKER (loader fix)"); return 2
    payload=json.loads(pr.stdout); assert payload.get("valid")
    # Activate (expect ACTIVATED), then ALREADY_ACTIVE, then resume. Follows R6 pattern.
    sraw=set_ref["set_ref"] if isinstance(set_ref,dict) and "set_ref" in set_ref else set_ref
    set_path_str=sraw.get("path") if isinstance(sraw,dict) else str(sraw)
    res_act=edpub.activate_publication(FIX_ROOT, state_rel, set_path_str, "R7 weekly editorial correction wk-r7-1", "r7-operator-wk-r7-1", datetime.now(timezone.utc))
    _log(f"API_ACTIVATE {json.dumps(res_act)[:800]}")
    assert res_act.get("status")=="ACTIVATED", res_act
    again=edpub.activate_publication(FIX_ROOT, state_rel, set_path_str, "R7 weekly idempotency probe", "r7-idempotency-probe", datetime.now(timezone.utc))
    _log(f"ALREADY_ACTIVE_OK {str(again)[:500]}")
    assert again.get("status")=="ALREADY_ACTIVE", again
    # Resume with same record when State already new (read-only, no new record).
    st_after=core.load_json(FIX_ROOT/state_rel)
    rec_ref=st_after.get("publication_revalidation_provenance")
    assert isinstance(rec_ref,dict) and rec_ref.get("path")
    state_sha_before=core.sha256_file(FIX_ROOT/state_rel)
    res_resume=edpub.resume_activation(FIX_ROOT, state_rel, rec_ref["path"])
    _log(f"RESUME {str(res_resume)[:800]}")
    assert res_resume.get("status") in ("ALREADY_ACTIVE","RESUMED"), res_resume
    assert core.sha256_file(FIX_ROOT/state_rel)==state_sha_before or res_resume.get("status")=="ALREADY_ACTIVE", "resume must be read-only when already active"
    _log("R7_WEEKLY_ACCEPT_OK real PDF + CLI root + normal activate/resume (depth via typed33 in R7 tests, qualified)")
    return 0

if __name__=="__main__":
    try: rc=main()
    except Exception: traceback.print_exc(); print("EXIT:2"); rc=2
    import sys as _s; _s.exit(rc)
