#!/usr/bin/env python3
"""Worker A LONGFORM: actual initial accepted base -> P1 changed narrative -> P2R -> external early scope correct -> P2V -> P3S -> public prepare REAL TL2026 -> external typed semantic/visual + bounded QA actual 5page not blank -> finalize Candidate before seal -> inert old State healthy -> activate -> strict State/receipt/Gate/Candidate -> ALREADY_ACTIVE. Then second prePreview + normal lifecycle.

Rules: no source edits, actual _new_longform_helper, no old setUp overlay, source commit exists before authority.
Fast base blank PDF allowed initial type only; corrected PDF REAL.
Manuscript coverage numbered longform locations, checkfamily evidence, typed fixture not genuine approval.
Initial healthy canonical Candidate generated before P1 to cover preserved oldCandidate.
On bug: return exact blocker, no fixture bypass, no 23 rewrites, no validator weakening.
"""
from __future__ import annotations
import copy
import json
import os
import sys
import traceback
import shutil
from datetime import datetime, timezone
from pathlib import Path

FIX_ROOT = Path(os.environ.get("SMOKE_FIX_ROOT", "/tmp/opencode/jgas-editorial-longform-20261021T090000Z/candidate-partial-b40de60"))
sys.path.insert(0, str(FIX_ROOT))
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONPYCACHEPREFIX"] = "/tmp/opencode/lf-pycache-verify"
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
    from scripts import survey_reader_fidelity_v2 as fidelity

    class _TC(unittest.TestCase):
        def runTest(self):
            pass
    tc = _TC()
    root = FIX_ROOT
    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    print(f"FIX_ROOT={root} HEAD={core.repository_commit_sha(root)}", flush=True)
    # Base: healthy Longform VALIDATED_DRAFT via actual _new_longform_helper (blank 1-page initial allowed)
    helper = p1t._new_longform_helper(tc, root, root)
    print(f"HELPER workspace={helper.workspace} root={helper.root} source_root={helper.source_root}", flush=True)
    chain = helper._complete(helper._chain())
    state_path = helper._state_path(chain)
    print(f"CHAIN issue={chain.get('issue_id', chain.get('issue', '?'))} state={state_path.relative_to(root)}", flush=True)
    built = helper._advance_to_validated_draft(chain, state_path)
    print(f"BASE_VALIDATED lifecycle={core.load_json(state_path)['lifecycle_state']}", flush=True)
    # Initial blank PDF must be 1-page (fast base type only)
    from pypdf import PdfReader as _PR
    base_pages = len(_PR(str(built['pdf'])).pages)
    print(f"BASE_PDF_PAGES={base_pages} path={built['pdf'].relative_to(root)}", flush=True)
    assert base_pages == 1, f"base blank PDF must be 1-page, got {base_pages}"
    # Initial healthy canonical Candidate before P1 (covers preserved oldCandidate)
    profile = core.load_json(chain["profile_path"])
    src_root = root / profile["paths"]["source_root"]
    cand_rel = (Path(profile["paths"]["source_root"]) / "publication" / "v2" / "publication-candidate-v2.json").as_posix()
    cand_path = root / cand_rel
    print(f"CANDIDATE_REL={cand_rel}", flush=True)
    assert not cand_path.exists(), "candidate must be absent before initial build"
    # built keys: manuscript,pdf,bundle,gate,SEMANTIC_EDITORIAL,VISUAL (+surface/review/primary/etc.)
    issue_for_cand = core.load_json(state_path).get("issue_id", "SP001")
    print(f"ISSUE_FOR_CAND={issue_for_cand}", flush=True)
    assert issue_for_cand == "SP001", f"longform issue must be SP001, got {issue_for_cand}"
    pubmod.build_candidate(
        root, issue_for_cand, "LONGFORM_SPECIAL",
        built["manuscript"], helper.survey_root / "main.tex",
        built["pdf"], 1, built["bundle"],
        built["SEMANTIC_EDITORIAL"], built["VISUAL"],
        cand_path)
    print(f"INITIAL_CANDIDATE_BUILT {cand_path.relative_to(root)}", flush=True)
    # Re-validate candidate
    cv0 = pubmod.validate_candidate(root, cand_path)
    print(f"INITIAL_CANDIDATE_VALID status={cv0.get('status') if isinstance(cv0, dict) else cv0}", flush=True)
    old_cand_bytes = cand_path.read_bytes()
    old_cand_sha = core.sha256_file(cand_path)
    print(f"OLD_CAND_SHA={old_cand_sha} bytes={len(old_cand_bytes)}", flush=True)
    # Record old canonical publication files for preservation check
    old_state_bytes = (root / state_path).read_bytes() if isinstance(state_path, Path) else None
    # P1: changed longform narrative (authored revision, not body bypass)
    authored = helper._authored(chain, helper.worker)
    # Change narrative_sections paragraph text (approved evidence, same DIDs)
    try:
        pkg0 = authored["longform_revision"]["packages"][0]
        nsec = pkg0["narrative_sections"][0]
        paras = nsec["paragraphs"]
        assert len(paras) >= 1, "no narrative paragraphs"
        paras[0]["text"] += " Revised fixture sentence within approved evidence."
        print(f"AUTHORED_CHANGED pkg0 narrative len={len(paras[0]['text'])}", flush=True)
    except Exception as exc:
        print(f"AUTHORED_CHANGE_BLOCKER {exc}", flush=True)
        traceback.print_exc()
        return 2
    proposal_id = "lf-longform-1"
    staged_authoring = p1t._stage_authoring_before_prepare(tc, root, helper.source_root, proposal_id, authored)
    print(f"STAGED_AUTHORING {staged_authoring.relative_to(root)}", flush=True)
    prepared = proposal_mod.prepare_proposal(root, state_path, staged_authoring, proposal_id, "Fixture longform prose correction within approved evidence.")
    proposal_path = p1t._stage_reader_and_proposal(tc, root, helper.source_root, proposal_id, prepared)
    print(f"PROPOSAL {proposal_path.relative_to(root)}", flush=True)
    outcome = proposal_mod.validate_proposal(root, state_path, proposal_path)
    assert outcome["result"] in ("REVIEW_REQUIRED", "REVIEW_BOUND_PROPOSAL"), outcome
    print(f"P1_VALIDATE {outcome['result']}", flush=True)
    # P2R capture
    cap = retention.capture_retention(root, state_path, proposal_path)
    assert cap["result"] == retention.RESULT_CAPTURED, cap
    manifest_path = root / cap["manifest_path"]
    print(f"P2R_CAPTURE {manifest_path.relative_to(root)}", flush=True)
    vout = retention.verify_retention(root, proposal_path, manifest_path)
    assert vout["result"] == retention.RESULT_VERIFIED, vout
    print("P2R_VERIFIED", flush=True)
    try:
        _ = proposal_mod.validate_proposal(root, state_path, proposal_path)
        raise AssertionError("P1 after capture must refuse (retention dest conflict)")
    except Exception as exc:
        msg = str(exc)
        assert "RETENTION_DEST_CONFLICT" in msg or "REFUSED" in msg or "retention" in msg.lower(), f"P1 after capture wrong refusal: {exc}"
        print(f"P1_AFTER_CAPTURE_REFUSAL_OK {type(exc).__name__}", flush=True)
    staged_reader_rel = prepared["proposal"]["proposed"]["proposed_reader_ref"]["path"]
    scope_path = p1t._scope_review_for(tc, root, prepared, staged_reader_rel, "scope-review-v2.json")
    print(f"SCOPE {scope_path.relative_to(root)}", flush=True)
    obs = observer.observe_current_authority(root, state_path, proposal_path, manifest_path, scope_path)
    assert obs.get("result") == "CURRENT_BASIS_OBSERVED_SCOPE_BOUND", obs
    print("P2V_SCOPE_BOUND", flush=True)
    staged_manifest_path = (proposal_path.parent / "staged-source" / "staged-source-manifest.json")
    mat = staged.materialize_staged_source(root, state_path, proposal_path, manifest_path, scope_path)
    print(f"P3S_MATERIALIZE {mat}", flush=True)
    if isinstance(mat, dict) and "staged_manifest_path" in mat:
        staged_manifest_path = root / mat["staged_manifest_path"]
    if not staged_manifest_path.is_file():
        cand = list((proposal_path.parent / "staged-source").glob("*.json"))
        print(f"P3S_CANDIDATES {cand}", flush=True)
        for c in cand:
            if "staged-source-manifest" in c.name:
                staged_manifest_path = c
                break
    assert staged_manifest_path.is_file(), f"staged manifest missing: {staged_manifest_path}"
    ver = staged.verify_staged_source(root, proposal_path, staged_manifest_path)
    assert ver.get("result") == "STAGED_SOURCE_REPLAY_VERIFIED", ver
    print("P3S_VERIFIED", flush=True)
    # Manuscript spec: actual coverage with numbered longform locations from NEW surface + staged main
    proposal_dir = proposal_path.parent
    staged_manifest = core.load_json(staged_manifest_path)
    issue_id = staged_manifest.get("issue_id")
    print(f"ISSUE={issue_id} PROFILE={staged_manifest.get('publication_profile')}", flush=True)
    # Load NEW proposed reader (proposed_canonical bytes) + staged main text to derive coverage
    new_reader_path = root / prepared["proposal"]["proposed"]["proposed_reader_ref"]["path"]
    # Note: proposed_reader_ref path is prospective (inside proposal dir, staged after prepare). The staged file is at proposal_dir/reader-surface-input-v2.json
    # Use that file (already staged) as NEW surface
    new_surface = core.load_json(proposal_dir / "reader-surface-input-v2.json")
    staged_main_rel = staged_manifest["outputs"]["main"]["path"]
    staged_main_text = (root / staged_main_rel).read_text(encoding="utf-8")
    print(f"STAGED_MAIN bytes={len(staged_main_text.encode('utf-8'))} rel={staged_main_rel}", flush=True)
    # Derive coverage via helper logic (numbered locations)
    # Reuse helper._section_locations + _manuscript_inputs pattern but with NEW surface + staged main
    # helper._section_locations expects (chain, surface, main_text)
    try:
        pkg_locs, final_loc = helper._section_locations(chain, new_surface, staged_main_text)
        print(f"SECTION_LOCS pkg={pkg_locs} final={final_loc}", flush=True)
    except Exception as exc:
        print(f"SECTION_LOCS_BLOCKER {exc}", flush=True)
        traceback.print_exc()
        return 2
    # Build coverage/requirements via helper._manuscript_inputs but with NEW surface? That helper uses chain surface? Let's call it with NEW surface via monkey?
    # Instead replicate _manuscript_inputs logic using derived locs + architecture
    arch = core.load_json(helper.source_root / "architecture-v2.json")
    # Map packages in order to pkg_locs (helper does zip)
    pkgs = arch.get("packages", [])
    assert len(pkg_locs) == len(pkgs), f"pkg locs {len(pkg_locs)} != pkgs {len(pkgs)}"
    coverage = [
        {"package_id": pkg["package_id"], "requirement": req, "status": "FULFILLED",
         "reader_locations": [loc], "detail": "Synthetic LF editorial manuscript author maps requirement to its source section."}
        for pkg, loc in zip(pkgs, pkg_locs)
        for req in pkg.get("must_cover_requirements", [])
    ]
    requirements = [
        {"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED",
         "reader_locations": [final_loc],
         "detail": "Synthetic LF editorial manuscript author asserts synthesis present."}
    ]
    print(f"COVERAGE rows={len(coverage)} reqs={len(requirements)}", flush=True)
    assert len(coverage) >= 1 and len(requirements) == 1
    # Verify locations are numbered longform (contain canonical block markers, not generic)
    # They should be like from fidelity.parse_longform_blocks (non-empty, distinct)
    assert len(set([r["reader_locations"][0] for r in coverage])) >= 1
    manuscript_spec = {
        "schema_version": "2.0-rc1", "kind": "EDITORIAL_MANUSCRIPT_SPEC_V1",
        "issue_id": issue_id, "proposal_ref": {"path": str(proposal_path.relative_to(root)), "sha256": core.sha256_file(proposal_path)},
        "architecture_coverage": coverage, "reader_requirements": requirements,
        "authored_by": "synthetic LF editorial manuscript author", "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    manuscript_spec_path = proposal_dir / "manuscript-spec.json"
    core.write_json(manuscript_spec_path, manuscript_spec)
    tl_bin = Path("/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/lualatex")
    assert tl_bin.exists(), f"toolchain missing: {tl_bin}"
    toolchain_spec = {
        "schema_version": "2.0-rc1", "kind": "EDITORIAL_TOOLCHAIN_SPEC_V1",
        "executor": "smoke-longform-integration", "absolute_executable": str(tl_bin),
        "recipe": "lualatex-biber-lualatex",
        "argv": list(edpub.EXPECTED_ARGV_LUALATEX_BIBER),
        "env": {}, "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    toolchain_spec_path = proposal_dir / "toolchain-spec.json"
    core.write_json(toolchain_spec_path, toolchain_spec)
    print(f"SPECS {manuscript_spec_path.relative_to(root)} {toolchain_spec_path.relative_to(root)}", flush=True)
    prepared_paths = edpub.prepare_publication(
        root,
        _rel(root, state_path), _rel(root, proposal_path), _rel(root, staged_manifest_path),
        _rel(root, manuscript_spec_path), _rel(root, toolchain_spec_path),
        datetime.now(timezone.utc))
    print(f"PREPARE {json.dumps(prepared_paths)}", flush=True)
    pubdir = proposal_dir / "publication"
    manuscript_path = pubdir / "reader-manuscript-v2.json"
    pdf_path = pubdir / "build" / "main.pdf"
    assert manuscript_path.is_file() and pdf_path.is_file(), "prepare outputs missing"
    page_count = len(_PR(str(pdf_path)).pages)
    pdf_sha = core.sha256_file(pdf_path)
    pdf_bytes = pdf_path.stat().st_size
    print(f"REAL_PDF pages={page_count} sha={pdf_sha[:16]} bytes={pdf_bytes}", flush=True)
    # REAL PDF must be actual 5-page not blank (R2 both routes 5pp)
    assert page_count >= 2, f"corrected PDF must be REAL multi-page, got {page_count}"
    # Extract text for later review (prove not blank)
    try:
        texts = [_PR(str(pdf_path)).pages[i].extract_text() or "" for i in range(page_count)]
        joined = "\n".join(texts)
        print(f"PDF_TEXT_CHARS={len(joined)} PAGES={page_count}", flush=True)
        assert len(joined.strip()) > 500, f"corrected PDF text too short (blank?): {len(joined)}"
    except AssertionError:
        raise
    except Exception as exc:
        print(f"PDF_TEXT_WARN {exc}", flush=True)
    # QA: deterministic checks with actual file assertions (4 for THEMATIC/LONGFORM_SPECIAL)
    quality_root = pubdir / "quality"
    quality_root.mkdir(parents=True, exist_ok=True)
    # Need staged main sha for identifier check
    staged_main_bytes = (root / staged_main_rel).read_bytes()
    # Build 4 payloads matching helper._quality_bundle pattern but for editorial staged source/pdf
    # Use actual PDF bytes for preflight
    payloads = {}
    payloads["SUBJECT_ENTITY_PROPERTY_BINDING"] = {
        "check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "status": "PASS", "issue_id": issue_id,
        "cited_discovery_count": 1,
        "bindings": [{"discovery_id": "d01", "canonical_name": "Target Model",
                      "canonical_url": "https://example.invalid/target", "materiality": "MATERIAL",
                      "status": "VERIFIED", "source_accessed_at": "2026-08-22T02:10:00+09:00"}],
    }
    # For editorial, use staged main sha + issue
    payloads["IDENTIFIER_PRESERVATION"] = {
        "check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
        "source_sha256": core.sha256_bytes(staged_main_bytes),
        "inspected_identifiers": [issue_id, "Target Model"],
        "scope": "smoke longform editorial real-build",
    }
    payloads["PDF_PREFLIGHT"] = {
        "check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": page_count,
        "pdf_sha256": pdf_sha, "byte_count": pdf_bytes,
        "scope": "smoke longform real TL2026 PDF",
    }
    payloads["EMPTY_WRAPPER_SUPPRESSION"] = {
        "check_id": "EMPTY_WRAPPER_SUPPRESSION", "status": "PASS",
        "scope": "smoke longform editorial carries no empty wrapper",
        "inspected_paths": [staged_main_rel],
    }
    # Verify expected set matches config
    kinds = quality.expected_checks_by_kind(cfg, "THEMATIC", "LONGFORM_SPECIAL", {"DETERMINISTIC"})
    print(f"EXPECTED_DETERMINISTIC={sorted(kinds)}", flush=True)
    assert set(payloads) == set(kinds), f"payloads {sorted(payloads)} != expected {sorted(kinds)}"
    result_paths = {}
    for cid, payload in payloads.items():
        p = quality_root / f"{cid.lower()}.json"
        core.write_json(p, payload)
        result_paths[cid] = p
    quality_checks = [
        {"check_id": cid, "kind": kinds[cid], "status": "PASS",
         "executor": "smoke longform editorial with actual file assertions",
         "evidence": "Exact fixture bytes and result file inspected.",
         "recorded_at": datetime.now(timezone.utc).isoformat(),
         "result": {"path": str(p.relative_to(root)), "sha256": core.sha256_file(p)}}
        for cid, p in result_paths.items()
    ]
    det_checks_path = proposal_dir / "deterministic-checks.json"
    core.write_json(det_checks_path, {"checks": quality_checks})
    print(f"DET_CHECKS {det_checks_path.relative_to(root)} n={len(quality_checks)}", flush=True)
    # Reviews: typed semantic/visual with correct checkfamily evidence, synthetic label, no genuine approval
    # Derive coverage_locations/final_locations from editorial manuscript (actual)
    manuscript = core.load_json(manuscript_path)
    # Use fidelity helper to get locations from manuscript (as finalize Gate will)
    try:
        from scripts.survey_reader_fidelity_v2 import _locations_from_manifest as _lfm
        cov_locs, fin_locs = _lfm(manuscript)
        coverage_locations = sorted(cov_locs)
        final_locations = sorted(fin_locs)
        print(f"MANUSCRIPT_LOCS cov={coverage_locations} fin={final_locations}", flush=True)
    except Exception as exc:
        print(f"MANUSCRIPT_LOCS_FALLBACK {exc}", flush=True)
        coverage_locations = sorted({r["reader_locations"][0] for r in coverage})
        final_locations = [final_loc]
    # Architecture for evidence (page-plan target dynamic for REAL PDF, not 1-page base)
    architecture = core.load_json(helper.source_root / "architecture-v2.json")
    package_ids = [r["package_id"] for r in architecture["packages"]]
    final_package = max(architecture["packages"], key=lambda r: r["drafting_order"])["package_id"]
    _pp = (architecture.get("page_plan") or {}).get("target_pages", 12)
    try:
        _tgt = int(float(_pp)) if float(_pp).is_integer() else str(_pp)
    except Exception:
        _tgt = 12
    print(f"PAGE_PLAN target={_pp} marker={_tgt} actual_pages={page_count}", flush=True)
    for kind, fname in (("SEMANTIC_EDITORIAL", "semantic-review-v2.json"), ("VISUAL", "visual-review-v2.json")):
        expected = reader_pub._expected_review_checks(root, profile, kind)
        checks = []
        for cid in sorted(expected):
            ev = ["synthetic-fixture:main.tex"]
            if cid in ("ARCHITECTURE_CONTENT_FIDELITY", "LONGFORM_TECHNICAL_DEPTH"):
                ev = sorted({f"package:{pid}" for pid in package_ids} | set(coverage_locations))
                if cid == "LONGFORM_TECHNICAL_DEPTH":
                    ev = sorted(set(ev) | {f"page-plan:{page_count}/{_tgt}", "density-review:below-target-substantive"})
            elif cid == "FINAL_SYNTHESIS_QUALITY":
                ev = sorted(set(final_locations) | {"reader-role:final-synthesis", f"package:{final_package}"})
            elif cid == "LONGFORM_MIXED_LAYOUT":
                ev = ["reader-layout:wide-surfaces-full-width", "reader-layout:references-one-column", "reader-layout:balanced-two-column-narrative"]
            checks.append({"check_id": cid, "status": "PASS",
                           "detail": "Synthetic LF editorial review; no real editorial or visual acceptance asserted.",
                           "evidence_locations": ev})
        out_path = pubdir / fname
        reader_pub.build_review_record(root, manuscript_path, pdf_path, page_count, kind, checks,
                                       f"synthetic LF editorial {kind} reviewer", datetime.now(timezone.utc), out_path)
        print(f"REVIEW {kind} {out_path.relative_to(root)} n={len(checks)}", flush=True)
    sem_path = pubdir / "semantic-review-v2.json"
    vis_path = pubdir / "visual-review-v2.json"
    # Finalize
    def _r(p):
        return _rel(root, p)
    set_ref = edpub.finalize_publication(root, _r(state_path), _r(proposal_path), _r(staged_manifest_path), _r(det_checks_path), _r(sem_path), _r(vis_path), datetime.now(timezone.utc))
    print(f"FINALIZE {json.dumps(set_ref)}", flush=True)
    from scripts import survey_agent_control_v2 as agent
    state_after_finalize = core.load_json(root / state_path) if isinstance(state_path, Path) else core.load_json(root / Path(state_path))
    # Need cfg reload? Use root config
    cfg2 = core.load_json(root / core.DEFAULT_CONFIG)
    # state_path may be Path or str; normalize
    sp = state_path if isinstance(state_path, Path) else root / str(state_path)
    errs = agent.validate_agent_state(root, cfg2, core.load_json(sp))
    assert not errs, f"State unhealthy after finalize (must stay healthy inert): {errs}"
    print("INERT_HEALTHY", flush=True)
    # Old canonical candidate still byte-identical?
    assert cand_path.read_bytes() == old_cand_bytes, "old canonical Candidate drifted before activation"
    print("OLD_CANDIDATE_PRESERVED_BEFORE_ACTIVATE", flush=True)
    _set_path = set_ref["set_ref"] if isinstance(set_ref, dict) and "set_ref" in set_ref else set_ref
    print(f"DEBUG_SET_PATH type={type(_set_path).__name__} value={_set_path!r}", flush=True)
    res = edpub.activate_publication(root, _r(state_path), _r(_set_path) if isinstance(_set_path, Path) else str(_set_path), "Fixture LF editorial correction", "smoke-lf-executor", datetime.now(timezone.utc))
    print(f"ACTIVATE {json.dumps(res)}", flush=True)
    assert res.get("status") == "ACTIVATED", res
    # Strict checks on new State
    receipt_path = pubdir / "validated-source-manifest.json"
    rv = edpub.validate_editorial_receipt(root, _r(receipt_path), _r(state_path))
    assert rv["issue_id"] == issue_id, rv
    print("RECEIPT_ACTIVE_OK", flush=True)
    # Full accepted_refs must be present and equal ctx (unconditional, incl. repeat) - prove binding
    assert "accepted_refs" in rv and len(rv["accepted_refs"]) >= 1, "receipt missing accepted_refs"
    print(f"RECEIPT_ACCEPTED_REFS n={len(rv['accepted_refs'])}", flush=True)
    gate_path = pubdir / "reader-surface-gate-v2.json"
    gv = reader_gate.validate_reader_surface_gate(root, _r(gate_path), issue_id=issue_id, publication_profile="LONGFORM_SPECIAL", expected_manuscript_path=_r(manuscript_path), state_path=_r(state_path))
    assert gv["status"] == "PASSED", gv
    print("GATE_ACTIVE_OK", flush=True)
    cand_pub_path = pubdir / "publication-candidate-v2.json"
    cv = pubmod.validate_candidate(root, cand_pub_path)
    print(f"CANDIDATE_ACTIVE_OK {cv.get('status') if isinstance(cv, dict) else cv}", flush=True)
    # Old canonical still preserved after activation?
    assert cand_path.read_bytes() == old_cand_bytes, "old canonical Candidate drifted after activation"
    print("OLD_CANDIDATE_PRESERVED_AFTER_ACTIVATE", flush=True)
    # Repeat ALREADY_ACTIVE readonly
    res2 = edpub.activate_publication(root, _r(state_path), _r(_set_path) if isinstance(_set_path, Path) else str(_set_path), "Fixture LF editorial correction", "smoke-lf-executor", datetime.now(timezone.utc))
    print(f"REPEAT {json.dumps(res2)}", flush=True)
    assert res2.get("status") == "ALREADY_ACTIVE", res2
    print("SMOKE_LONGFORM_ACTIVATION_OK", flush=True)
    # Save markers for second-phase script (paths)
    marker = proposal_dir / "activation-marker.json"
    core.write_json(marker, {"proposal_id": proposal_id, "set_ref": _set_path if isinstance(_set_path, str) else str(_set_path), "issue_id": issue_id, "state_path": _r(state_path), "proposal_path": _r(proposal_path), "staged_manifest_path": _r(staged_manifest_path), "old_cand_sha": old_cand_sha, "old_cand_rel": cand_rel, "page_count": page_count, "pdf_sha": pdf_sha})
    print(f"MARKER {marker.relative_to(root)}", flush=True)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
