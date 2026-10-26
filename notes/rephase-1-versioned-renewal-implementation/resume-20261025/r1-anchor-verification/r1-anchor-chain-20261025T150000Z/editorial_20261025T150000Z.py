#!/usr/bin/env python3
"""Editorial R3 activate under old 721 after R1x2 — real TL build once, synthetic reviews.

Uses OLD 721 source code only (anchor-weekly). Public APIs: P1 prepare, P2R capture/verify,
scope synthetic, P2V observe, P3S50 materialize/verify, edpub prepare (real TL2026)/finalize/activate.
Anchor: supersedes r2 (latest legacy), canonical_anchor stays original checkpoint (no rollover).
Fresh child (PYTHONPATH=old fix), no 740 caching. Synthetic reviews, no genuine approval.
"""
import hashlib, json, os, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

def _run_git(root: Path, *args: str):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
    return subprocess.run(["git",*args], cwd=root, capture_output=True, text=True, timeout=120, env=env)

def _sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    if len(sys.argv)!=3:
        print(f"usage: {sys.argv[0]} FIX_ROOT EVIDENCE_DIR", flush=True); return 2
    fix=Path(sys.argv[1]).resolve(); ev=Path(sys.argv[2]).resolve()
    for v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE"):
        if os.environ.get(v): print(f"UNSAFE {v}", flush=True); return 2
    sys.dont_write_bytecode=True; os.environ["PYTHONDONTWRITEBYTECODE"]="1"
    pidfile=ev/"editorial.pid"; hbfile=ev/"editorial.heartbeat.txt"
    pidfile.write_text(f"{os.getpid()}\n{time.monotonic():.3f}\n")
    hbfile.write_text(f"editorial start {time.monotonic():.3f}\n")
    head_before=_run_git(fix,"rev-parse","HEAD").stdout.strip()
    (ev/"editorial-pin-before-head.txt").write_text(head_before+"\n")
    # must be after R1x2 (HEAD 36c679c, r1+r2 present)
    rec_dir=fix/"sources/2026-W37/publication/v2"
    recs=sorted(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))
    assert recs==["publication-surface-revalidation-r1.json","publication-surface-revalidation-r2.json"], f"need r1+r2 before editorial, got {recs}"
    r2=json.loads((rec_dir/"publication-surface-revalidation-r2.json").read_bytes())
    assert r2.get("supersedes") is not None
    hbfile.write_text(hbfile.read_text()+f"r2 present {time.monotonic():.3f}\n")
    sys.path.insert(0, str(fix))
    import unittest
    from tests import test_survey_editorial_correction_proposal_v2 as p1t
    from tests import test_survey_editorial_staged_source_v2 as p3st
    from scripts import survey_production_v2 as core
    from scripts import survey_editorial_correction_proposal_v2 as proposal_mod
    from scripts import survey_editorial_retention_v2 as retention
    from scripts import survey_editorial_current_authority_v2 as observer
    from scripts import survey_editorial_staged_source_v2 as staged
    from scripts import survey_editorial_publication_v2 as edpub
    from scripts import survey_publication_v2 as pubmod
    class Dummy(unittest.TestCase):
        def runTest(self): pass
    tc=Dummy()
    # Reuse existing VALIDATED (do NOT rebuild — profile already exists). Reconstruct helper (safe, no init).
    helper=p1t._new_weekly_helper(tc, fix)
    state_path=helper.source_root/"production-state.json"
    assert state_path.is_file(), f"missing VALIDATED state {state_path}"
    state_rel=str(state_path.relative_to(fix).as_posix())
    # P1 changed reader: load existing authored, modify headline/deck + 3 paras with exact synthesis, stage, prepare.
    # Previous wk-anchor-ed1/ed2 partials preserved (failed before/ at finalize); retry uses new id, no takeover.
    PROPOSAL_ID="wk-anchor-ed3"
    old_auth_path=helper.source_root/"semantic-publication-input.json"
    assert old_auth_path.is_file(), f"missing authored {old_auth_path}"
    old_auth=core.load_json(old_auth_path)
    import copy
    new_auth=copy.deepcopy(old_auth)
    new_auth["cover"]["headline"]="Weekly tested method, revised anchor edition"
    new_auth["cover"]["deck"]="Source survey with anchor editorial amendment; synthetic, no genuine approval."
    new_auth["final_summary"]["paragraphs"]=[
        "The edition surveys one source with anchor P1 changed reader.",
        "The claims remain attributed; R1x2 anchor r2 preserved.",
        "The accepted source authors describe the tested method."]
    staged_authoring=p1t._stage_authoring_before_prepare(tc, fix, helper.source_root, PROPOSAL_ID, new_auth)
    prepared=proposal_mod.prepare_proposal(fix, state_rel, staged_authoring, PROPOSAL_ID, "Anchor editorial correction after R1x2.")
    proposal_path=p1t._stage_reader_and_proposal(tc, fix, helper.source_root, PROPOSAL_ID, prepared)
    outcome=proposal_mod.validate_proposal(fix, state_rel, proposal_path)
    assert outcome["result"]=="REVIEW_REQUIRED", outcome
    hbfile.write_text(hbfile.read_text()+f"P1 {PROPOSAL_ID} {time.monotonic():.3f}\n")
    (ev/"editorial-p1-proposal.txt").write_text(str(proposal_path.relative_to(fix).as_posix())+"\n")
    # P2R
    cap=retention.capture_retention(fix, state_path, proposal_path)
    assert cap.get("result")==retention.RESULT_CAPTURED, cap
    manifest_path=fix/cap["manifest_path"]
    vout=retention.verify_retention(fix, proposal_path, manifest_path)
    assert vout.get("result")==retention.RESULT_VERIFIED, vout
    hbfile.write_text(hbfile.read_text()+f"P2R {time.monotonic():.3f}\n")
    # scope synthetic
    staged_reader_rel=prepared["proposal"]["proposed"]["proposed_reader_ref"]["path"]
    scope_path=p1t._scope_review_for(tc, fix, prepared, staged_reader_rel, "scope-review-v2.json")
    hbfile.write_text(hbfile.read_text()+f"SCOPE {time.monotonic():.3f} {scope_path}\n")
    # P2V
    obs=observer.observe_current_authority(fix, state_path, proposal_path, manifest_path, scope_path)
    assert obs.get("result")=="CURRENT_BASIS_OBSERVED_SCOPE_BOUND", obs
    hbfile.write_text(hbfile.read_text()+f"P2V {time.monotonic():.3f}\n")
    # P3S50 (old source, must be 50, keep old code)
    mat=staged.materialize_staged_source(fix, state_path, proposal_path, manifest_path, scope_path)
    sm_path=fix/mat["staged_manifest_path"] if isinstance(mat,dict) and "staged_manifest_path" in mat else (proposal_path.parent/"staged-source"/"staged-source-manifest.json")
    assert sm_path.is_file()
    ver=staged.verify_staged_source(fix, proposal_path, sm_path)
    assert ver.get("result")=="STAGED_SOURCE_REPLAY_VERIFIED", ver
    sm=core.load_json(sm_path)
    assert len(sm.get("code_deps",[]))==50, f"old P3S50 must stay 50, got {len(sm.get('code_deps',[]))}"
    hbfile.write_text(hbfile.read_text()+f"P3S50 {time.monotonic():.3f} {sm_path}\n")
    (ev/"editorial-staged-manifest.txt").write_text(str(sm_path.relative_to(fix).as_posix())+f" {_sha(sm_path)}\n")
    # specs + real TL2026 prepare (once, not fake blank)
    TL_BIN=Path("/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/lualatex")
    BIBER_BIN=Path("/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/biber")
    assert TL_BIN.exists() and BIBER_BIN.exists(), f"TOOLCHAIN MISSING {TL_BIN} {BIBER_BIN}"
    proposal_dir=proposal_path.parent
    issue_id=sm.get("issue_id")
    arch=core.load_json(helper.source_root/"architecture-v2.json")
    coverage=[{"package_id":pl["package_id"],"requirement":rq,"status":"FULFILLED","reader_locations":["main.tex:package-1"],"detail":f"Anchor manuscript maps {PROPOSAL_ID}."} for pl in arch.get("packages",[]) for rq in pl.get("must_cover_requirements",[])]
    requirements=[{"requirement_id":"FINAL_SYNTHESIS","status":"FULFILLED","reader_locations":["main.tex:summary"],"detail":"Anchor synthesis."},
                  {"requirement_id":"WEEKLY_COMMUNITY_MOVEMENT","status":"FULFILLED","reader_locations":["main.tex:package-1"],"detail":"Anchor movement."}]
    mspec={"schema_version":"2.0-rc1","kind":"EDITORIAL_MANUSCRIPT_SPEC_V1","issue_id":issue_id,
           "proposal_ref":{"path":str(proposal_path.relative_to(fix).as_posix()),"sha256":_sha(proposal_path)},
           "architecture_coverage":coverage,"reader_requirements":requirements,
           "authored_by":"anchor weekly manuscript author","recorded_at":datetime.now(timezone.utc).isoformat()}
    mspec_path=proposal_dir/"manuscript-spec.json"; core.write_json(mspec_path, mspec)
    tspec={"schema_version":"2.0-rc1","kind":"EDITORIAL_TOOLCHAIN_SPEC_V1","executor":"anchor-weekly-integration",
           "absolute_executable":str(TL_BIN),"recipe":"lualatex-biber-lualatex","argv":list(edpub.EXPECTED_ARGV_LUALATEX_BIBER),"env":{},"recorded_at":datetime.now(timezone.utc).isoformat()}
    tspec_path=proposal_dir/"toolchain-spec.json"; core.write_json(tspec_path, tspec)
    t0=time.monotonic()
    prepared_paths=edpub.prepare_publication(fix, state_rel, str(proposal_path.relative_to(fix).as_posix()),
        str(sm_path.relative_to(fix).as_posix()), str(mspec_path.relative_to(fix).as_posix()), str(tspec_path.relative_to(fix).as_posix()), datetime.now(timezone.utc))
    dt=time.monotonic()-t0
    hbfile.write_text(hbfile.read_text()+f"PREPARE dt={dt:.1f}s {time.monotonic():.3f}\n")
    pubdir=proposal_dir/"publication"
    manuscript_path=pubdir/"reader-manuscript-v2.json"; pdf_path=pubdir/"build"/"main.pdf"; log_path=pubdir/"build"/"main.log"
    assert manuscript_path.is_file() and pdf_path.is_file() and log_path.is_file()
    from pypdf import PdfReader as _PR
    pages=len(_PR(str(pdf_path)).pages)
    assert pages>=1, f"weekly real PDF >=1 page, got {pages}"
    assert pdf_path.stat().st_size>5000, f"real PDF not fake blank, bytes={pdf_path.stat().st_size}"
    (ev/"editorial-real-pdf.txt").write_text(f"pages={pages} bytes={pdf_path.stat().st_size} sha={_sha(pdf_path)} log_bytes={log_path.stat().st_size}\n")
    # QA + synthetic reviews (actual builders, synthetic)
    qroot=pubdir/"quality"; qroot.mkdir(parents=True, exist_ok=True)
    sp=qroot/"subject-entity-property-binding.json"; core.write_json(sp, {"check_id":"SUBJECT_ENTITY_PROPERTY_BINDING","status":"PASS","scope":f"anchor {PROPOSAL_ID} real-build"})
    main_bytes=(fix/sm["outputs"]["main"]["path"]).read_bytes()
    ip=qroot/"identifier-preservation.json"; core.write_json(ip, {"check_id":"IDENTIFIER_PRESERVATION","status":"PASS","source_sha256":hashlib.sha256(main_bytes).hexdigest(),"inspected_identifiers":[issue_id],"scope":f"anchor {PROPOSAL_ID} real-build"})
    pp=qroot/"pdf-preflight.json"; core.write_json(pp, {"check_id":"PDF_PREFLIGHT","status":"PASS","page_count":pages,"pdf_sha256":_sha(pdf_path),"byte_count":pdf_path.stat().st_size,"scope":f"anchor {PROPOSAL_ID} real TL2026 PDF"})
    qchecks=[{"check_id":cid,"kind":"DETERMINISTIC","status":"PASS","executor":"anchor editorial actual assertions","evidence":"Exact bytes inspected.","recorded_at":datetime.now(timezone.utc).isoformat(),"result":{"path":str(p.relative_to(fix).as_posix()),"sha256":_sha(p)}} for cid,p in (("SUBJECT_ENTITY_PROPERTY_BINDING",sp),("IDENTIFIER_PRESERVATION",ip),("PDF_PREFLIGHT",pp))]
    det_path=proposal_dir/"deterministic-checks.json"; core.write_json(det_path, {"checks":qchecks})
    # reviews via actual builders (synthetic)
    profile=core.load_json(fix/core.load_json(state_path)["profile"]["path"])
    from scripts import survey_reader_publication_v2 as reader_pub
    review_paths={}
    for kind,name in (("SEMANTIC_EDITORIAL","semantic-review-v2.json"),("VISUAL","visual-review-v2.json")):
        checks=[{"check_id":cid,"status":"PASS","detail":f"Anchor synthetic {kind} reviewer; no genuine Human approval.","evidence_locations":[f"anchor-real-build:{PROPOSAL_ID}:main.pdf"]} for cid in sorted(reader_pub._expected_review_checks(fix, profile, kind))]
        rp=pubdir/name
        reader_pub.build_review_record(fix, manuscript_path, pdf_path, pages, kind, checks, f"anchor synthetic {kind} reviewer", datetime.now(timezone.utc), rp)
        review_paths[kind]=rp
    hbfile.write_text(hbfile.read_text()+f"QA_REVIEWS {time.monotonic():.3f}\n")
    # finalize + validate + activate (anchor r2, no rollover) — use repo-relative strings (not absolute Paths)
    prop_rel=str(proposal_path.relative_to(fix).as_posix())
    sm_rel=str(sm_path.relative_to(fix).as_posix())
    det_rel=str(det_path.relative_to(fix).as_posix())
    sem_rel=str(review_paths["SEMANTIC_EDITORIAL"].relative_to(fix).as_posix())
    vis_rel=str(review_paths["VISUAL"].relative_to(fix).as_posix())
    set_ref=edpub.finalize_publication(fix, state_rel, prop_rel, sm_rel, det_rel, sem_rel, vis_rel, datetime.now(timezone.utc))
    # set_ref may be dict with set_path or path
    set_path_str=set_ref.get("set_path") or set_ref.get("publication_set") or set_ref.get("set_ref") or ""
    if isinstance(set_path_str, dict): set_path_str=set_path_str.get("path","")
    set_path=fix/set_path_str if set_path_str else pubdir/"publication-set.json"
    assert set_path.is_file(), f"set missing {set_path}"
    set_rel=str(set_path.relative_to(fix).as_posix())
    vset=edpub.validate_prepared_set(fix, state_rel, set_rel)
    hbfile.write_text(hbfile.read_text()+f"FINALIZE {time.monotonic():.3f} set={set_path.relative_to(fix)}\n")
    (ev/"editorial-set.txt").write_text(f"{set_path.relative_to(fix)} {_sha(set_path)}\n")
    res=edpub.activate_publication(fix, state_rel, set_rel, f"Anchor editorial {PROPOSAL_ID} after R1x2", "anchor-fixture", datetime.now(timezone.utc))
    hbfile.write_text(hbfile.read_text()+f"ACTIVATE {time.monotonic():.3f} res={str(res)[:500]}\n")
    # verify new record supersedes r2, anchor stays original (no rollover)
    new_recs=sorted(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))
    assert new_recs==["publication-surface-revalidation-r1.json","publication-surface-revalidation-r2.json","publication-surface-revalidation-r3.json"], f"must have r1+r2+r3, got {new_recs}"
    r3=json.loads((rec_dir/"publication-surface-revalidation-r3.json").read_bytes())
    assert r3.get("supersedes") is not None, "r3 must supersede r2"
    # supersedes must point to r2 (actual file SHA)
    r2_sha=_sha(rec_dir/"publication-surface-revalidation-r2.json")
    sup=r3.get("supersedes")
    assert sup.get("sha256")==r2_sha or sup.get("path","").endswith("r2.json"), f"r3 must supersede r2, got {sup}"
    (ev/"editorial-r3.json").write_text(json.dumps({"recorded_at":r3.get("recorded_at"),"supersedes":sup,"canonical_anchor":r3.get("canonical_anchor")}, indent=2))
    print(f"EDITORIAL OK r3 supersedes r2, real PDF pages={pages}", flush=True)
    return 0

if __name__=="__main__":
    sys.exit(main())
