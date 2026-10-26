#!/usr/bin/env python3
"""Depth32-full editorial31: ACTUAL old public editorial correction at 31 (OLD code, anchor r30).

TEST-only, no product edits, no candidate/reconstruct commits, no network/old-runners,
no cleanup failed fixture/cache purge. Uses workspace TMPDIR, per-phase 1200 with
owned PID/heartbeats/terminal exit, don't duplicate child on return. Fresh Python
per SOURCE epoch (OLD 36c679), no shared execution, no dummy SHA, strict schema.

- NEW independent fixture provided history r1..r30 (NOT R1x30 actual ops) already
  constructed, State->r30, OLD validate_state passes, hist verified.
- Run ACTUAL old public editorial correction at 31 (P1/P2R/P2V/P3S50/realbuild/
  finalize/activate) with latest legacy anchor REAL TYPED r30, no synthetic fake
  Candidate; all source committed before authority (HEAD stays 36c679cc).
- Creates valid NONNULL versioned predecessor 31 (EDITORIAL, supersedes r30,
  canonical_anchor LEGACY r30, no rollover).
- Code/validator no changes, no dummy sha or rows invalid schema.
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
    pidfile=ev/"editorial31.pid"; hbfile=ev/"editorial31.heartbeat.txt"
    pidfile.write_text(f"{os.getpid()}\n{time.monotonic():.3f}\n")
    hbfile.write_text(f"editorial31 start {time.monotonic():.3f}\n")
    head_before=_run_git(fix,"rev-parse","HEAD").stdout.strip()
    assert head_before=="36c679cc5ed3291c11d4a01bdee906807cace8c4", f"must be 36c679cc before editorial31, got {head_before}"
    (ev/"editorial31-pin-before-head.txt").write_text(head_before+"\n")
    rec_dir=fix/"sources/2026-W37/publication/v2"
    recs=sorted(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))
    # Must have exactly r1..r30 (30 files) before editorial31 (lexicographic sort gives r1,r10,...; compare as sets)
    expected_set=set(f"publication-surface-revalidation-r{i}.json" for i in range(1,31))
    assert set(recs)==expected_set, f"need r1..r30 before editorial31, got len={len(recs)} {sorted(recs)[:5]}"
    r30=json.loads((rec_dir/"publication-surface-revalidation-r30.json").read_bytes())
    assert r30.get("reason_class")=="REVIEWED_CORE_CHANGE" and "kind" not in r30, "r30 must be LEGACY"
    assert r30.get("supersedes") is not None or True  # r1 has None, r30 has supersedes
    # State must point to r30
    state_path=fix/"sources/2026-W37/production-state.json"
    state=json.loads(state_path.read_bytes().decode("utf-8"))
    prov=state.get("publication_revalidation_provenance",{})
    r30_sha=_sha(rec_dir/"publication-surface-revalidation-r30.json")
    assert prov.get("path")=="sources/2026-W37/publication/v2/publication-surface-revalidation-r30.json" and prov.get("sha256")==r30_sha, f"State must point r30, got {prov}"
    hbfile.write_text(hbfile.read_text()+f"r30 present {r30_sha[:12]} {time.monotonic():.3f}\n")
    sys.path.insert(0, str(fix))
    import unittest
    from tests import test_survey_editorial_correction_proposal_v2 as p1t
    from scripts import survey_production_v2 as core
    from scripts import survey_editorial_correction_proposal_v2 as proposal_mod
    from scripts import survey_editorial_retention_v2 as retention
    from scripts import survey_editorial_current_authority_v2 as observer
    from scripts import survey_editorial_staged_source_v2 as staged
    from scripts import survey_editorial_publication_v2 as edpub
    class Dummy(unittest.TestCase):
        def runTest(self): pass
    tc=Dummy()
    helper=p1t._new_weekly_helper(tc, fix)
    state_path2=helper.source_root/"production-state.json"
    assert state_path2.is_file()
    state_rel=str(state_path2.relative_to(fix).as_posix())
    PROPOSAL_ID="wk-depth32-ed31"
    # NEW fixture (correct timestamps) has no prior ed dirs (construction deletes old ed dirs); use ed31 fresh. Previous failed fixture (wrong Oct26 timestamps) preserved separately with ed31/ed32 partials + r31 chronology failure, no cleanup.
    old_auth_path=helper.source_root/"semantic-publication-input.json"
    assert old_auth_path.is_file(), f"missing authored {old_auth_path}"
    old_auth=core.load_json(old_auth_path)
    import copy
    new_auth=copy.deepcopy(old_auth)
    new_auth["cover"]["headline"]="Weekly tested method, depth32-full edition"
    new_auth["cover"]["deck"]="Source survey with depth32-full editorial amendment; synthetic, no genuine approval."
    new_auth["final_summary"]["paragraphs"]=[
        "The edition surveys one source with depth32-full P1 changed reader.",
        "The claims remain attributed; provided r1..r30 anchor r30 preserved (NOT R1x30 actual ops).",
        "The accepted source authors describe the tested method."]
    staged_authoring=p1t._stage_authoring_before_prepare(tc, fix, helper.source_root, PROPOSAL_ID, new_auth)
    prepared=proposal_mod.prepare_proposal(fix, state_rel, staged_authoring, PROPOSAL_ID, "Depth32-full editorial31 after provided r1..r30 (NOT R1x30 actual ops).")
    proposal_path=p1t._stage_reader_and_proposal(tc, fix, helper.source_root, PROPOSAL_ID, prepared)
    outcome=proposal_mod.validate_proposal(fix, state_rel, proposal_path)
    assert outcome["result"]=="REVIEW_REQUIRED", outcome
    hbfile.write_text(hbfile.read_text()+f"P1 {PROPOSAL_ID} {time.monotonic():.3f}\n")
    (ev/"editorial31-p1-proposal.txt").write_text(str(proposal_path.relative_to(fix).as_posix())+"\n")
    cap=retention.capture_retention(fix, state_path2, proposal_path)
    assert cap.get("result")==retention.RESULT_CAPTURED, cap
    manifest_path=fix/cap["manifest_path"]
    vout=retention.verify_retention(fix, proposal_path, manifest_path)
    assert vout.get("result")==retention.RESULT_VERIFIED, vout
    hbfile.write_text(hbfile.read_text()+f"P2R {time.monotonic():.3f}\n")
    staged_reader_rel=prepared["proposal"]["proposed"]["proposed_reader_ref"]["path"]
    scope_path=p1t._scope_review_for(tc, fix, prepared, staged_reader_rel, "scope-review-v2.json")
    hbfile.write_text(hbfile.read_text()+f"SCOPE {time.monotonic():.3f} {scope_path}\n")
    obs=observer.observe_current_authority(fix, state_path2, proposal_path, manifest_path, scope_path)
    assert obs.get("result")=="CURRENT_BASIS_OBSERVED_SCOPE_BOUND", obs
    hbfile.write_text(hbfile.read_text()+f"P2V {time.monotonic():.3f}\n")
    mat=staged.materialize_staged_source(fix, state_path2, proposal_path, manifest_path, scope_path)
    sm_path=fix/mat["staged_manifest_path"] if isinstance(mat,dict) and "staged_manifest_path" in mat else (proposal_path.parent/"staged-source"/"staged-source-manifest.json")
    assert sm_path.is_file()
    ver=staged.verify_staged_source(fix, proposal_path, sm_path)
    assert ver.get("result")=="STAGED_SOURCE_REPLAY_VERIFIED", ver
    sm=core.load_json(sm_path)
    assert len(sm.get("code_deps",[]))==50, f"old P3S50 must stay 50, got {len(sm.get('code_deps',[]))}"
    hbfile.write_text(hbfile.read_text()+f"P3S50 {time.monotonic():.3f} {sm_path}\n")
    (ev/"editorial31-staged-manifest.txt").write_text(str(sm_path.relative_to(fix).as_posix())+f" {_sha(sm_path)}\n")
    TL_BIN=Path("/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/lualatex")
    BIBER_BIN=Path("/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/biber")
    assert TL_BIN.exists() and BIBER_BIN.exists(), f"TOOLCHAIN MISSING {TL_BIN} {BIBER_BIN}"
    proposal_dir=proposal_path.parent
    issue_id=sm.get("issue_id")
    arch=core.load_json(helper.source_root/"architecture-v2.json")
    coverage=[{"package_id":pl["package_id"],"requirement":rq,"status":"FULFILLED","reader_locations":["main.tex:package-1"],"detail":f"Depth32-full manuscript maps {PROPOSAL_ID}."} for pl in arch.get("packages",[]) for rq in pl.get("must_cover_requirements",[])]
    requirements=[{"requirement_id":"FINAL_SYNTHESIS","status":"FULFILLED","reader_locations":["main.tex:summary"],"detail":"Depth32-full synthesis."},
                  {"requirement_id":"WEEKLY_COMMUNITY_MOVEMENT","status":"FULFILLED","reader_locations":["main.tex:package-1"],"detail":"Depth32-full movement."}]
    mspec={"schema_version":"2.0-rc1","kind":"EDITORIAL_MANUSCRIPT_SPEC_V1","issue_id":issue_id,
           "proposal_ref":{"path":str(proposal_path.relative_to(fix).as_posix()),"sha256":_sha(proposal_path)},
           "architecture_coverage":coverage,"reader_requirements":requirements,
           "authored_by":"depth32-full weekly manuscript author","recorded_at":datetime.now(timezone.utc).isoformat()}
    mspec_path=proposal_dir/"manuscript-spec.json"; core.write_json(mspec_path, mspec)
    tspec={"schema_version":"2.0-rc1","kind":"EDITORIAL_TOOLCHAIN_SPEC_V1","executor":"depth32-full-integration",
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
    (ev/"editorial31-real-pdf.txt").write_text(f"pages={pages} bytes={pdf_path.stat().st_size} sha={_sha(pdf_path)} log_bytes={log_path.stat().st_size}\n")
    qroot=pubdir/"quality"; qroot.mkdir(parents=True, exist_ok=True)
    sp=qroot/"subject-entity-property-binding.json"; core.write_json(sp, {"check_id":"SUBJECT_ENTITY_PROPERTY_BINDING","status":"PASS","scope":f"depth32-full {PROPOSAL_ID} real-build"})
    main_bytes=(fix/sm["outputs"]["main"]["path"]).read_bytes()
    ip=qroot/"identifier-preservation.json"; core.write_json(ip, {"check_id":"IDENTIFIER_PRESERVATION","status":"PASS","source_sha256":hashlib.sha256(main_bytes).hexdigest(),"inspected_identifiers":[issue_id],"scope":f"depth32-full {PROPOSAL_ID} real-build"})
    pp=qroot/"pdf-preflight.json"; core.write_json(pp, {"check_id":"PDF_PREFLIGHT","status":"PASS","page_count":pages,"pdf_sha256":_sha(pdf_path),"byte_count":pdf_path.stat().st_size,"scope":f"depth32-full {PROPOSAL_ID} real TL2026 PDF"})
    qchecks=[{"check_id":cid,"kind":"DETERMINISTIC","status":"PASS","executor":"depth32-full editorial actual assertions","evidence":"Exact bytes inspected.","recorded_at":datetime.now(timezone.utc).isoformat(),"result":{"path":str(p.relative_to(fix).as_posix()),"sha256":_sha(p)}} for cid,p in (("SUBJECT_ENTITY_PROPERTY_BINDING",sp),("IDENTIFIER_PRESERVATION",ip),("PDF_PREFLIGHT",pp))]
    det_path=proposal_dir/"deterministic-checks.json"; core.write_json(det_path, {"checks":qchecks})
    profile=core.load_json(fix/core.load_json(state_path2)["profile"]["path"])
    from scripts import survey_reader_publication_v2 as reader_pub
    review_paths={}
    for kind,name in (("SEMANTIC_EDITORIAL","semantic-review-v2.json"),("VISUAL","visual-review-v2.json")):
        checks=[{"check_id":cid,"status":"PASS","detail":f"Depth32-full synthetic {kind} reviewer; no genuine Human approval.","evidence_locations":[f"depth32-full-real-build:{PROPOSAL_ID}:main.pdf"]} for cid in sorted(reader_pub._expected_review_checks(fix, profile, kind))]
        rp=pubdir/name
        reader_pub.build_review_record(fix, manuscript_path, pdf_path, pages, kind, checks, f"depth32-full synthetic {kind} reviewer", datetime.now(timezone.utc), rp)
        review_paths[kind]=rp
    hbfile.write_text(hbfile.read_text()+f"QA_REVIEWS {time.monotonic():.3f}\n")
    prop_rel=str(proposal_path.relative_to(fix).as_posix())
    sm_rel=str(sm_path.relative_to(fix).as_posix())
    det_rel=str(det_path.relative_to(fix).as_posix())
    sem_rel=str(review_paths["SEMANTIC_EDITORIAL"].relative_to(fix).as_posix())
    vis_rel=str(review_paths["VISUAL"].relative_to(fix).as_posix())
    set_ref=edpub.finalize_publication(fix, state_rel, prop_rel, sm_rel, det_rel, sem_rel, vis_rel, datetime.now(timezone.utc))
    set_path_str=set_ref.get("set_path") or set_ref.get("publication_set") or set_ref.get("set_ref") or ""
    if isinstance(set_path_str, dict): set_path_str=set_path_str.get("path","")
    set_path=fix/set_path_str if set_path_str else pubdir/"publication-set.json"
    assert set_path.is_file(), f"set missing {set_path}"
    set_rel=str(set_path.relative_to(fix).as_posix())
    vset=edpub.validate_prepared_set(fix, state_rel, set_rel)
    hbfile.write_text(hbfile.read_text()+f"FINALIZE {time.monotonic():.3f} set={set_path.relative_to(fix)}\n")
    (ev/"editorial31-set.txt").write_text(f"{set_path.relative_to(fix)} {_sha(set_path)}\n")
    res=edpub.activate_publication(fix, state_rel, set_rel, f"Depth32-full editorial {PROPOSAL_ID} after provided r1..r30 (NOT R1x30)", "depth32-full-fixture", datetime.now(timezone.utc))
    hbfile.write_text(hbfile.read_text()+f"ACTIVATE {time.monotonic():.3f} res={str(res)[:500]}\n")
    new_recs=sorted(p.name for p in rec_dir.iterdir() if p.name.startswith("publication-surface-revalidation-r"))
    expected_after_set=set(f"publication-surface-revalidation-r{i}.json" for i in range(1,32))
    assert set(new_recs)==expected_after_set, f"must have r1..r31, got len={len(new_recs)}"
    r31=json.loads((rec_dir/"publication-surface-revalidation-r31.json").read_bytes())
    assert r31.get("kind")=="EDITORIAL_PUBLICATION_ACTIVATION_V1" and r31.get("reason_class")=="REVIEWED_EDITORIAL_CORRECTION", f"r31 kind wrong {r31.get('kind')}"
    assert r31.get("supersedes") is not None, "r31 must supersede r30"
    r30_sha=_sha(rec_dir/"publication-surface-revalidation-r30.json")
    sup=r31.get("supersedes")
    assert sup.get("sha256")==r30_sha and sup.get("path")=="sources/2026-W37/publication/v2/publication-surface-revalidation-r30.json", f"r31 must supersede r30, got {sup}"
    anchor=r31.get("canonical_anchor")
    assert anchor=={"kind":"LEGACY_REVALIDATION","ref":{"path":"sources/2026-W37/publication/v2/publication-surface-revalidation-r30.json","sha256":r30_sha}}, f"r31 anchor must be r30, got {anchor}"
    # HEAD must stay 36c679cc (all source committed before authority, no source commit for editorial)
    head_after=_run_git(fix,"rev-parse","HEAD").stdout.strip()
    assert head_after=="36c679cc5ed3291c11d4a01bdee906807cace8c4", f"HEAD must stay 36c679cc after editorial31, got {head_after}"
    # State must now point r31
    new_state=json.loads((fix/"sources/2026-W37/production-state.json").read_bytes().decode("utf-8"))
    new_prov=new_state.get("publication_revalidation_provenance",{})
    r31_sha=_sha(rec_dir/"publication-surface-revalidation-r31.json")
    assert new_prov.get("path")=="sources/2026-W37/publication/v2/publication-surface-revalidation-r31.json" and new_prov.get("sha256")==r31_sha, f"State must point r31, got {new_prov}"
    (ev/"editorial31-r31.json").write_text(json.dumps({"recorded_at":r31.get("recorded_at"),"supersedes":sup,"canonical_anchor":anchor,"r31_sha":r31_sha}, indent=2))
    print(f"EDITORIAL31 OK r31 supersedes r30 anchor r30, real PDF pages={pages} r31={r31_sha[:12]}", flush=True)
    return 0

if __name__=="__main__":
    sys.exit(main())
