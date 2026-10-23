#!/usr/bin/env python3
"""Worker A LONGFORM phase2: second prePreview correction + normal lifecycle.

Precondition: 10-smoke succeeded, marker at proposal lf-longform-1, State VALIDATED_DRAFT active first set.
Steps:
  - Record first-set immutable hashes (proposal/publication + staged-source + seal/Candidate) + State bytes.
  - BEFOREPREVIEW_COPY is expected at /tmp/opencode/jgas-editorial-longform-20261021T091000Z/beforePreview (bash cp -a before this script).
  - Second correction lf-longform-2 from active authoring (first authoring + second sentence), full P1/P2R/P2V/P3S/prepare/real build/finalize/activate.
  - Prove prior versioned KEEP_IMMUTABLE (all old files byte unchanged vs pre-second + beforePreview) + live State COPY (only pointer changed) + full accepted_refs new receipt binding.
  - Then normal Candidate->RELEASE_CANDIDATE->Preview->Freeze->FROZEN->Release->RELEASED via actual functions.
  - Save PDFs/text/PNG pins.
"""
from __future__ import annotations
import copy
import json
import os
import sys
import traceback
import hashlib
from datetime import datetime, timezone
from pathlib import Path

FIX_ROOT = Path(os.environ.get("SMOKE_FIX_ROOT", "/tmp/opencode/jgas-editorial-longform-20261021T090000Z/candidate-partial-b40de60"))
BEFORE_DIR = Path(os.environ.get("BEFOREPREVIEW_ROOT", "/tmp/opencode/jgas-editorial-longform-20261021T090000Z/beforePreview"))
sys.path.insert(0, str(FIX_ROOT))
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONPYCACHEPREFIX"] = "/tmp/opencode/lf-pycache-verify2"
os.environ["TMPDIR"] = "/tmp/opencode"

from scripts import survey_production_v2 as core

def _rel(root: Path, p) -> str:
    pp = Path(p)
    if pp.is_absolute():
        return str(pp.relative_to(root))
    s = str(p)
    if s.startswith("/"):
        return str(Path(s).relative_to(root))
    return s

def _hash_tree(root: Path, base: Path) -> dict[str, str]:
    out = {}
    for f in sorted(base.rglob("*")):
        if f.is_file() and ".git" not in f.parts:
            out[str(f.relative_to(root))] = core.sha256_file(f)
    return out

def main() -> int:
    import unittest
    from tests import test_survey_editorial_correction_proposal_v2 as p1t
    from scripts import survey_editorial_correction_proposal_v2 as proposal_mod
    from scripts import survey_editorial_retention_v2 as retention
    from scripts import survey_editorial_current_authority_v2 as observer
    from scripts import survey_editorial_staged_source_v2 as staged
    from scripts import survey_editorial_publication_v2 as edpub
    from scripts import survey_reader_publication_v2 as reader_pub
    from scripts import survey_reader_surface_gate_v2 as reader_gate
    from scripts import survey_quality_v2 as quality
    from scripts import survey_publication_v2 as pubmod

    class _TC(unittest.TestCase):
        def runTest(self):
            pass
    tc = _TC()
    root = FIX_ROOT
    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    print(f"PHASE2 FIX_ROOT={root} HEAD={core.repository_commit_sha(root)}", flush=True)
    # Load marker from phase1
    # Find marker: sources/SP001/publication/v2/editorial-corrections/lf-longform-1/publication/activation-marker.json? Actually marker at proposal_dir/activation-marker.json
    markers = list(root.rglob("activation-marker.json"))
    print(f"MARKERS={markers}", flush=True)
    assert len(markers) == 1, f"expected 1 marker, got {markers}"
    marker_path = markers[0]
    marker = core.load_json(marker_path)
    print(f"MARKER={json.dumps(marker)}", flush=True)
    first_proposal_id = marker["proposal_id"]
    first_proposal_path = root / marker["proposal_path"]
    first_proposal_dir = first_proposal_path.parent
    first_pubdir = first_proposal_dir / "publication"
    first_staged_dir = first_proposal_dir / "staged-source"
    state_rel = marker["state_path"]
    state_path = root / state_rel
    assert state_path.is_file(), f"state missing: {state_path}"
    print(f"STATE={state_rel} lifecycle={core.load_json(state_path)['lifecycle_state']}", flush=True)
    # Record first-set hashes before second correction
    pre_hashes = _hash_tree(root, first_proposal_dir)
    print(f"PRE_FIRSTSET_FILES={len(pre_hashes)}", flush=True)
    for k in sorted(pre_hashes)[:5]:
        print(f"PRE {k} {pre_hashes[k][:16]}", flush=True)
    pre_state_bytes = state_path.read_bytes()
    pre_state = core.load_json(state_path)
    print(f"PRE_STATE_POINTER={pre_state.get('publication_revalidation_provenance')}", flush=True)
    # Verify BEFORE copy exists and matches pre (bash cp -a before this script)
    print(f"BEFORE_DIR={BEFORE_DIR} exists={BEFORE_DIR.exists()}", flush=True)
    assert BEFORE_DIR.exists(), f"beforePreview copy missing: {BEFORE_DIR} (bash must cp -a before phase2)"
    # Compare BEFORE copy's first proposal dir hashes vs pre
    before_first = BEFORE_DIR / first_proposal_dir.relative_to(root)
    # BEFORE_DIR is a copy of FIX_ROOT? Actually bash cp -a DST DST_beforePreview, so BEFORE_DIR contains candidate-partial-b40de60? Adjust:
    # If BEFORE_DIR is /tmp/.../beforePreview (which contains candidate-partial-b40de60 subtree?), handle both.
    if not before_first.exists():
        # Try BEFORE_DIR/candidate-partial-b40de60/...
        alt = BEFORE_DIR / "candidate-partial-b40de60" / first_proposal_dir.relative_to(root)
        print(f"BEFORE_ALT_CHECK {alt} exists={alt.exists()}", flush=True)
        if alt.exists():
            before_first = alt
    assert before_first.exists(), f"before first proposal dir missing: {before_first}"
    before_hashes = _hash_tree(BEFORE_DIR if (BEFORE_DIR / first_proposal_dir.relative_to(root)).exists() else BEFORE_DIR / "candidate-partial-b40de60", before_first)
    # Simpler: compare file-by-file via relative
    mism = []
    for rel, sha in pre_hashes.items():
        bf = BEFORE_DIR / rel if (BEFORE_DIR / rel).exists() else BEFORE_DIR / "candidate-partial-b40de60" / rel
        if not bf.is_file():
            mism.append((rel, "before-missing"))
        elif core.sha256_file(bf) != sha:
            mism.append((rel, "before-drift"))
    print(f"BEFORE_MATCH_MISM={len(mism)}", flush=True)
    assert not mism, f"before copy drift: {mism[:3]}"
    print("BEFORE_COPY_MATCHES_PRE", flush=True)
    # Second correction: new proposal from active authoring (first authoring + second sentence)
    # Do NOT re-init SP001 (fixture already VALIDATED + activated); reuse existing base files.
    # _new_longform_helper only sets paths (no init), minimal chain for section/coverage (chain unused except source_root).
    helper = p1t._new_longform_helper(tc, root, root)
    chain = {"source_root": helper.source_root, "profile_path": helper.source_root / "production-profile.json"}
    print(f"REUSE_BASE source_root={helper.source_root} profile={chain['profile_path'].exists()}", flush=True)
    # Note: for second correction we need active authoring: load first authoring-input
    first_authoring = core.load_json(first_proposal_dir / "authoring-input.json")
    authored2 = copy.deepcopy(first_authoring)
    try:
        pkg0 = authored2["longform_revision"]["packages"][0]
        paras = pkg0["narrative_sections"][0]["paragraphs"]
        paras[0]["text"] += " Second revised fixture sentence within approved evidence."
        print(f"AUTHORED2_CHANGED len={len(paras[0]['text'])}", flush=True)
    except Exception as exc:
        print(f"AUTHORED2_BLOCKER {exc}", flush=True)
        traceback.print_exc()
        return 2
    proposal_id2 = "lf-longform-2"
    staged_authoring2 = p1t._stage_authoring_before_prepare(tc, root, helper.source_root, proposal_id2, authored2)
    print(f"STAGED2 {staged_authoring2.relative_to(root)}", flush=True)
    prepared2 = proposal_mod.prepare_proposal(root, state_path, staged_authoring2, proposal_id2, "Second LF prePreview correction within approved evidence.")
    proposal_path2 = p1t._stage_reader_and_proposal(tc, root, helper.source_root, proposal_id2, prepared2)
    print(f"PROPOSAL2 {proposal_path2.relative_to(root)}", flush=True)
    outcome2 = proposal_mod.validate_proposal(root, state_path, proposal_path2)
    assert outcome2["result"] in ("REVIEW_REQUIRED", "REVIEW_BOUND_PROPOSAL"), outcome2
    print(f"P1_VALIDATE2 {outcome2['result']}", flush=True)
    cap2 = retention.capture_retention(root, state_path, proposal_path2)
    assert cap2["result"] == retention.RESULT_CAPTURED, cap2
    manifest_path2 = root / cap2["manifest_path"]
    print(f"P2R_CAPTURE2 {manifest_path2.relative_to(root)}", flush=True)
    vout2 = retention.verify_retention(root, proposal_path2, manifest_path2)
    assert vout2["result"] == retention.RESULT_VERIFIED, vout2
    print("P2R_VERIFIED2", flush=True)
    staged_reader_rel2 = prepared2["proposal"]["proposed"]["proposed_reader_ref"]["path"]
    scope_path2 = p1t._scope_review_for(tc, root, prepared2, staged_reader_rel2, "scope-review-v2.json")
    print(f"SCOPE2 {scope_path2.relative_to(root)}", flush=True)
    obs2 = observer.observe_current_authority(root, state_path, proposal_path2, manifest_path2, scope_path2)
    assert obs2.get("result") == "CURRENT_BASIS_OBSERVED_SCOPE_BOUND", obs2
    print("P2V_SCOPE_BOUND2", flush=True)
    staged_manifest_path2 = (proposal_path2.parent / "staged-source" / "staged-source-manifest.json")
    mat2 = staged.materialize_staged_source(root, state_path, proposal_path2, manifest_path2, scope_path2)
    print(f"P3S_MATERIALIZE2 {mat2}", flush=True)
    if isinstance(mat2, dict) and "staged_manifest_path" in mat2:
        staged_manifest_path2 = root / mat2["staged_manifest_path"]
    assert staged_manifest_path2.is_file(), f"staged2 missing: {staged_manifest_path2}"
    ver2 = staged.verify_staged_source(root, proposal_path2, staged_manifest_path2)
    assert ver2.get("result") == "STAGED_SOURCE_REPLAY_VERIFIED", ver2
    print("P3S_VERIFIED2", flush=True)
    # Prove prior versioned KEEP: all old files byte unchanged after P1/P2R/P2V/P3S repeat (before prepare2 writes new pubdir)
    post_p3_hashes = _hash_tree(root, first_proposal_dir)
    keep_mism = [(k, pre_hashes[k][:8], post_p3_hashes.get(k, "missing")[:8] if post_p3_hashes.get(k) else "missing") for k in pre_hashes if pre_hashes[k] != post_p3_hashes.get(k)]
    print(f"KEEP_CHECK_AFTER_P3 mism={len(keep_mism)}", flush=True)
    for m in keep_mism[:5]:
        print(f"KEEP_MISM {m}", flush=True)
    assert not keep_mism, f"prior versioned drift after repeat: {keep_mism[:3]}"
    print("PRIOR_KEEP_IMMUTABLE_AFTER_REPEAT", flush=True)
    # State COPY check: State file should still be exact pre bytes? Actually P1/P2R/P2V/P3S are read-only, State must be unchanged until activation
    assert state_path.read_bytes() == pre_state_bytes, "State drifted during repeat (must be COPY, no write until activation)"
    print("STATE_COPY_NO_WRITE_AFTER_REPEAT", flush=True)
    # Prepare second: manuscript-spec/toolchain-spec + REAL build
    proposal_dir2 = proposal_path2.parent
    staged_manifest2 = core.load_json(staged_manifest_path2)
    issue_id2 = staged_manifest2.get("issue_id")
    assert issue_id2 == marker["issue_id"], f"issue2 {issue_id2} != {marker['issue_id']}"
    new_surface2 = core.load_json(proposal_dir2 / "reader-surface-input-v2.json")
    staged_main_rel2 = staged_manifest2["outputs"]["main"]["path"]
    staged_main_text2 = (root / staged_main_rel2).read_text(encoding="utf-8")
    pkg_locs2, final_loc2 = helper._section_locations(chain, new_surface2, staged_main_text2)
    print(f"SECTION2 pkg={pkg_locs2} final={final_loc2}", flush=True)
    arch = core.load_json(helper.source_root / "architecture-v2.json")
    pkgs = arch.get("packages", [])
    coverage2 = [{"package_id": pkg["package_id"], "requirement": req, "status": "FULFILLED", "reader_locations": [loc], "detail": "Second LF editorial author maps requirement."} for pkg, loc in zip(pkgs, pkg_locs2) for req in pkg.get("must_cover_requirements", [])]
    requirements2 = [{"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED", "reader_locations": [final_loc2], "detail": "Second LF editorial asserts synthesis."}]
    manuscript_spec2 = {"schema_version": "2.0-rc1", "kind": "EDITORIAL_MANUSCRIPT_SPEC_V1", "issue_id": issue_id2, "proposal_ref": {"path": str(proposal_path2.relative_to(root)), "sha256": core.sha256_file(proposal_path2)}, "architecture_coverage": coverage2, "reader_requirements": requirements2, "authored_by": "second LF editorial author", "recorded_at": datetime.now(timezone.utc).isoformat()}
    manuscript_spec_path2 = proposal_dir2 / "manuscript-spec.json"
    core.write_json(manuscript_spec_path2, manuscript_spec2)
    from scripts import survey_editorial_publication_v2 as edpub2
    tl_bin = Path("/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/lualatex")
    toolchain_spec2 = {"schema_version": "2.0-rc1", "kind": "EDITORIAL_TOOLCHAIN_SPEC_V1", "executor": "second-lf", "absolute_executable": str(tl_bin), "recipe": "lualatex-biber-lualatex", "argv": list(edpub2.EXPECTED_ARGV_LUALATEX_BIBER), "env": {}, "recorded_at": datetime.now(timezone.utc).isoformat()}
    toolchain_spec_path2 = proposal_dir2 / "toolchain-spec.json"
    core.write_json(toolchain_spec_path2, toolchain_spec2)
    print(f"SPECS2 {manuscript_spec_path2.relative_to(root)} {toolchain_spec_path2.relative_to(root)}", flush=True)
    prepared_paths2 = edpub.prepare_publication(root, _rel(root, state_path), _rel(root, proposal_path2), _rel(root, staged_manifest_path2), _rel(root, manuscript_spec_path2), _rel(root, toolchain_spec_path2), datetime.now(timezone.utc))
    print(f"PREPARE2 {json.dumps(prepared_paths2)}", flush=True)
    pubdir2 = proposal_dir2 / "publication"
    manuscript_path2 = pubdir2 / "reader-manuscript-v2.json"
    pdf_path2 = pubdir2 / "build" / "main.pdf"
    assert manuscript_path2.is_file() and pdf_path2.is_file(), "prepare2 outputs missing"
    from pypdf import PdfReader as _PR2
    page_count2 = len(_PR2(str(pdf_path2)).pages)
    print(f"REAL_PDF2 pages={page_count2} sha={core.sha256_file(pdf_path2)[:16]}", flush=True)
    assert page_count2 >= 2, f"second PDF must be REAL, got {page_count2}"
    # QA + reviews for second
    quality_root2 = pubdir2 / "quality"
    quality_root2.mkdir(parents=True, exist_ok=True)
    staged_main_bytes2 = (root / staged_main_rel2).read_bytes()
    profile = core.load_json(chain["profile_path"])
    kinds = quality.expected_checks_by_kind(cfg, "THEMATIC", "LONGFORM_SPECIAL", {"DETERMINISTIC"})
    payloads2 = {
        "SUBJECT_ENTITY_PROPERTY_BINDING": {"check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "status": "PASS", "issue_id": issue_id2, "cited_discovery_count": 1, "bindings": [{"discovery_id": "d01", "canonical_name": "Target Model", "canonical_url": "https://example.invalid/target", "materiality": "MATERIAL", "status": "VERIFIED", "source_accessed_at": "2026-08-22T02:10:00+09:00"}]},
        "IDENTIFIER_PRESERVATION": {"check_id": "IDENTIFIER_PRESERVATION", "status": "PASS", "source_sha256": core.sha256_bytes(staged_main_bytes2), "inspected_identifiers": [issue_id2, "Target Model"], "scope": "second LF real-build"},
        "PDF_PREFLIGHT": {"check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": page_count2, "pdf_sha256": core.sha256_file(pdf_path2), "byte_count": pdf_path2.stat().st_size, "scope": "second LF real PDF"},
        "EMPTY_WRAPPER_SUPPRESSION": {"check_id": "EMPTY_WRAPPER_SUPPRESSION", "status": "PASS", "scope": "second LF no wrapper", "inspected_paths": [staged_main_rel2]},
    }
    assert set(payloads2) == set(kinds), f"payloads2 mismatch"
    result_paths2 = {}
    for cid, payload in payloads2.items():
        p = quality_root2 / f"{cid.lower()}.json"
        core.write_json(p, payload)
        result_paths2[cid] = p
    quality_checks2 = [{"check_id": cid, "kind": kinds[cid], "status": "PASS", "executor": "second LF with file assertions", "evidence": "Exact bytes inspected.", "recorded_at": datetime.now(timezone.utc).isoformat(), "result": {"path": str(p.relative_to(root)), "sha256": core.sha256_file(p)}} for cid, p in result_paths2.items()]
    det_checks_path2 = proposal_dir2 / "deterministic-checks.json"
    core.write_json(det_checks_path2, {"checks": quality_checks2})
    manuscript2 = core.load_json(manuscript_path2)
    try:
        from scripts.survey_reader_fidelity_v2 import _locations_from_manifest as _lfm2
        cov2, fin2 = _lfm2(manuscript2)
        cov_locs2, fin_locs2 = sorted(cov2), sorted(fin2)
    except Exception:
        cov_locs2 = sorted({r["reader_locations"][0] for r in coverage2})
        fin_locs2 = [final_loc2]
    print(f"MANUSCRIPT2_LOCS cov={cov_locs2} fin={fin_locs2}", flush=True)
    architecture = core.load_json(helper.source_root / "architecture-v2.json")
    package_ids = [r["package_id"] for r in architecture["packages"]]
    final_package = max(architecture["packages"], key=lambda r: r["drafting_order"])["package_id"]
    _pp2 = (architecture.get("page_plan") or {}).get("target_pages", 12)
    try:
        _tgt2 = int(float(_pp2)) if float(_pp2).is_integer() else str(_pp2)
    except Exception:
        _tgt2 = 12
    print(f"PAGE_PLAN2 target={_pp2} marker={_tgt2} actual_pages={page_count2}", flush=True)
    for kind, fname in (("SEMANTIC_EDITORIAL", "semantic-review-v2.json"), ("VISUAL", "visual-review-v2.json")):
        expected = reader_pub._expected_review_checks(root, profile, kind)
        checks = []
        for cid in sorted(expected):
            ev = ["synthetic-fixture:main.tex"]
            if cid in ("ARCHITECTURE_CONTENT_FIDELITY", "LONGFORM_TECHNICAL_DEPTH"):
                ev = sorted({f"package:{pid}" for pid in package_ids} | set(cov_locs2))
                if cid == "LONGFORM_TECHNICAL_DEPTH":
                    ev = sorted(set(ev) | {f"page-plan:{page_count2}/{_tgt2}", "density-review:below-target-substantive"})
            elif cid == "FINAL_SYNTHESIS_QUALITY":
                ev = sorted(set(fin_locs2) | {"reader-role:final-synthesis", f"package:{final_package}"})
            elif cid == "LONGFORM_MIXED_LAYOUT":
                ev = ["reader-layout:wide-surfaces-full-width", "reader-layout:references-one-column", "reader-layout:balanced-two-column-narrative"]
            checks.append({"check_id": cid, "status": "PASS", "detail": "Second synthetic LF review; no genuine approval.", "evidence_locations": ev})
        out_path = pubdir2 / fname
        reader_pub.build_review_record(root, manuscript_path2, pdf_path2, page_count2, kind, checks, f"second synthetic LF {kind} reviewer", datetime.now(timezone.utc), out_path)
        print(f"REVIEW2 {kind} {out_path.relative_to(root)}", flush=True)
    sem_path2 = pubdir2 / "semantic-review-v2.json"
    vis_path2 = pubdir2 / "visual-review-v2.json"
    def _r(p):
        return _rel(root, p)
    # Prior KEEP still before finalize2?
    mid_hashes = _hash_tree(root, first_proposal_dir)
    assert all(mid_hashes[k] == pre_hashes[k] for k in pre_hashes), "prior drift before finalize2"
    print("PRIOR_KEEP_BEFORE_FINALIZE2", flush=True)
    set_ref2 = edpub.finalize_publication(root, _r(state_path), _r(proposal_path2), _r(staged_manifest_path2), _r(det_checks_path2), _r(sem_path2), _r(vis_path2), datetime.now(timezone.utc))
    print(f"FINALIZE2 {json.dumps(set_ref2)}", flush=True)
    from scripts import survey_agent_control_v2 as agent
    cfg2 = core.load_json(root / core.DEFAULT_CONFIG)
    errs = agent.validate_agent_state(root, cfg2, core.load_json(state_path))
    assert not errs, f"State unhealthy after finalize2: {errs}"
    print("INERT_HEALTHY2 (old State still healthy before second activate)", flush=True)
    # Full accepted_refs new receipt binding for second?
    receipt_path2 = pubdir2 / "validated-source-manifest.json"
    rv2 = edpub.validate_editorial_receipt(root, _r(receipt_path2), _r(state_path))
    print(f"RECEIPT2_ACCEPTED n={len(rv2.get('accepted_refs', []))} issue={rv2.get('issue_id')}", flush=True)
    assert len(rv2.get("accepted_refs", [])) >= 1, "second receipt missing accepted_refs"
    # Activate second (supersedes first)
    _set2 = set_ref2["set_ref"] if isinstance(set_ref2, dict) and "set_ref" in set_ref2 else set_ref2
    res2 = edpub.activate_publication(root, _r(state_path), _r(_set2) if isinstance(_set2, Path) else str(_set2), "Second LF editorial correction", "second-lf-executor", datetime.now(timezone.utc))
    print(f"ACTIVATE2 {json.dumps(res2)}", flush=True)
    assert res2.get("status") == "ACTIVATED", res2
    # Prove prior immutable still byte unchanged after second activation + State only pointer changed
    post_hashes = _hash_tree(root, first_proposal_dir)
    keep2_mism = [(k, pre_hashes[k][:8], post_hashes.get(k, "missing")[:8] if post_hashes.get(k) else "missing") for k in pre_hashes if pre_hashes[k] != post_hashes.get(k)]
    print(f"KEEP_AFTER_ACTIVATE2 mism={len(keep2_mism)}", flush=True)
    assert not keep2_mism, f"prior drift after second activate: {keep2_mism[:3]}"
    print("PRIOR_KEEP_IMMUTABLE_AFTER_SECOND_ACTIVATE", flush=True)
    post_state_bytes = state_path.read_bytes()
    print(f"STATE_PRE_SHA={hashlib.sha256(pre_state_bytes).hexdigest()[:16]} POST_SHA={hashlib.sha256(post_state_bytes).hexdigest()[:16]}", flush=True)
    assert post_state_bytes != pre_state_bytes, "State must change pointer on second activate (COPY)"
    # Strict checks on second active
    gv2 = reader_gate.validate_reader_surface_gate(root, _r(pubdir2 / "reader-surface-gate-v2.json"), issue_id=issue_id2, publication_profile="LONGFORM_SPECIAL", expected_manuscript_path=_r(manuscript_path2), state_path=_r(state_path))
    assert gv2["status"] == "PASSED", gv2
    print("GATE_ACTIVE_OK2", flush=True)
    cv2 = pubmod.validate_candidate(root, pubdir2 / "publication-candidate-v2.json")
    print(f"CANDIDATE_ACTIVE_OK2 {cv2.get('status') if isinstance(cv2, dict) else cv2}", flush=True)
    res2r = edpub.activate_publication(root, _r(state_path), _r(_set2) if isinstance(_set2, Path) else str(_set2), "Second LF editorial correction", "second-lf-executor", datetime.now(timezone.utc))
    assert res2r.get("status") == "ALREADY_ACTIVE", res2r
    print("ALREADY_ACTIVE2_OK", flush=True)
    # Normal lifecycle: Candidate->RELEASE_CANDIDATE->Preview->Freeze->FROZEN->Release->RELEASED via actual functions
    # Use second active Candidate (versioned) with existing LF healthy sequence
    from scripts import survey_stage_validation_v2 as stage_validation
    second_cand = pubdir2 / "publication-candidate-v2.json"
    # Need chain for _advance: reuse helper chain (base) but state is active second set; _advance uses chain[source_root]/production-state.json
    # Our helper chain's source_root is sources/SP001, state_path is same file (production-state.json). Good.
    # Advance VALIDATED_DRAFT with versioned candidate
    helper._advance(chain, "VALIDATED_DRAFT", {"publication-candidate": second_cand}, 140)
    print("LIFECYCLE_RELEASE_CANDIDATE_OK", flush=True)
    state_file = helper.source_root / "production-state.json"
    assert core.load_json(state_file)["lifecycle_state"] == "RELEASE_CANDIDATE"
    agent.approve_publication_preview(root, cfg, state_file, "synthetic-human-fixture", core.parse_instant("2026-08-22T07:00:00+09:00"), "synthetic:publication-preview")
    print("LIFECYCLE_PREVIEW_OK", flush=True)
    approval_rel = cfg["state_authority"]["publication_preview_approval_path"]
    approval_path = helper.source_root / approval_rel
    assert approval_path.is_file(), f"approval missing: {approval_path}"
    freeze_path = helper.publication_root / "freeze-record-v2.json"
    manifest_path = helper.publication_root / "release-manifest-v2.json"
    # build_freeze with versioned candidate
    pubmod.build_freeze(root, second_cand, approval_path, core.parse_instant("2026-08-22T08:00:00+09:00"), freeze_path, manifest_path)
    print(f"LIFECYCLE_FREEZE_BUILT {freeze_path.relative_to(root)}", flush=True)
    cand_payload = pubmod.validate_candidate(root, second_cand, issue_id=issue_id2)
    visual_path = root / cand_payload["visual_review"]["path"]
    print(f"LIFECYCLE_VISUAL {visual_path.relative_to(root)}", flush=True)
    helper._advance(chain, "RELEASE_CANDIDATE", {"freeze-record": freeze_path, "release-manifest": manifest_path, "visual-review-record": visual_path}, 141)
    assert core.load_json(state_file)["lifecycle_state"] == "FROZEN"
    print("LIFECYCLE_FROZEN_OK", flush=True)
    # Offline Release/checkpoint -> RELEASED (reuse LF healthy sequence, no network/real Human)
    from scripts import survey_longform_derivation_v2 as derivation
    from scripts import survey_longform_generated_v2 as generated
    from scripts import survey_publication_v2 as pub2
    # Need paths for readback: use initial archive? For editorial active, readback uses? Use second pub? Simpler: use release builders with manifest
    from scripts import survey_release_checkpoint_v2 as release_checkpoint
    merge_path = helper.publication_root / "merge-verification-v2.json"
    record_path = helper.publication_root / "release-record-v2.json"
    pub2.build_merge_verification(root, manifest_path, core.repository_commit_sha(root), core.parse_instant("2026-08-22T09:00:00+09:00"), merge_path)
    pub2.build_release_record(root, manifest_path, merge_path, core.parse_instant("2026-08-22T09:30:00+09:00"), "synthetic-lf2i-release", record_path)
    checkpoint = release_checkpoint.build_release_checkpoint(root, cfg, state_file, merge_path, record_path, core.parse_instant("2026-08-22T10:00:00+09:00"))
    updated = agent.advance_with_checkpoint(root, cfg, state_file, checkpoint)
    assert updated["lifecycle_state"] == "RELEASED"
    assert agent.validate_agent_state(root, cfg, updated) == []
    print("LIFECYCLE_RELEASED_OK", flush=True)
    # Save pins marker
    core.write_json(proposal_dir2 / "phase2-marker.json", {"proposal_id2": proposal_id2, "issue_id": issue_id2, "page_count2": page_count2, "pdf_sha2": core.sha256_file(pdf_path2), "second_cand": str(second_cand.relative_to(root)), "lifecycle": "RELEASED"})
    print("PHASE2_COMPLETE", flush=True)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
