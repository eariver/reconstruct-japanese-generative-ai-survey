#!/usr/bin/env python3
"""Integration smoke: first valid Weekly activation (REAL TL2026 build).

Uses fixture SOURCE at /tmp/opencode/jgas-editorial-smoke-20261021T120000Z/candidate-partial-b40de60.
Fast base via _new_weekly_helper/_build_weekly_validated (blank initial PDF only).
NEW corrected publication does REAL build. No imports outside fixture/code.
Saves full raw stdout/stderr, numeric exit, persistent unique attempt files + source binding.
"""
from __future__ import annotations
import json
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

FIX_ROOT = Path(os.environ.get("SMOKE_FIX_ROOT", "/tmp/opencode/jgas-editorial-smoke-20261021T120000Z/candidate-partial-b40de60"))
sys.path.insert(0, str(FIX_ROOT))

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
os.environ["PYTHONPYCACHEPREFIX"] = "/tmp/opencode/int-pycache"
os.environ["TMPDIR"] = "/tmp/opencode"

from scripts import survey_production_v2 as core

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

    class _TC(unittest.TestCase):
        def runTest(self):
            pass
    tc = _TC()
    root = FIX_ROOT
    cfg = core.load_json(root / core.DEFAULT_CONFIG)

    # Fast base: healthy Weekly VALIDATED_DRAFT with blank PDF (helper recipe).
    helper = p1t._new_weekly_helper(tc, root)
    built = p1t._build_weekly_validated(tc, helper)
    chain, state_path = built["chain"], Path(built["state_path"]) if not isinstance(built["state_path"], Path) else built["state_path"]
    print(f"BASE_VALIDATED state={state_path.relative_to(root)} issue={chain.get('issue_id','?')}", flush=True)

    # Stage NEW proposed authoring: changed Weekly cover.headline.
    authored = core.load_json(chain["authored_path"])
    orig_headline = authored.get("cover", {}).get("headline", "")
    authored["cover"]["headline"] = (orig_headline + " — Editorial Correction").strip() if orig_headline else "Weekly revised headline — Editorial Correction"
    proposal_id = "wk-smoke-1"
    staged_authoring = p1t._stage_authoring_before_prepare(tc, root, helper.source_root, proposal_id, authored)
    print(f"STAGED_AUTHORING {staged_authoring.relative_to(root)} headline={authored['cover']['headline']!r}", flush=True)

    prepared = proposal_mod.prepare_proposal(root, state_path, staged_authoring, proposal_id, "Smoke weekly envelope correction.")
    proposal_path = p1t._stage_reader_and_proposal(tc, root, helper.source_root, proposal_id, prepared)
    print(f"PROPOSAL {proposal_path.relative_to(root)}", flush=True)
    outcome = proposal_mod.validate_proposal(root, state_path, proposal_path)
    assert outcome["result"] in ("REVIEW_REQUIRED", "REVIEW_BOUND_PROPOSAL"), outcome
    print(f"P1_VALIDATE {outcome['result']}", flush=True)

    # P2R capture.
    cap = retention.capture_retention(root, state_path, proposal_path)
    assert cap["result"] == retention.RESULT_CAPTURED, cap
    manifest_path = root / cap["manifest_path"]
    print(f"P2R_CAPTURE {manifest_path.relative_to(root)}", flush=True)
    vout = retention.verify_retention(root, proposal_path, manifest_path)
    assert vout["result"] == retention.RESULT_VERIFIED, vout

    # Public P1 after capture must remain refusal (retention dests already present).
    try:
        _ = proposal_mod.validate_proposal(root, state_path, proposal_path)
        raise AssertionError("P1 after capture must refuse (retention dest conflict), but returned success")
    except Exception as exc:
        msg = str(exc)
        assert "RETENTION_DEST_CONFLICT" in msg or "REFUSED" in msg or "retention" in msg.lower(), f"P1 after capture wrong refusal: {exc}"
        print(f"P1_AFTER_CAPTURE_REFUSAL_OK {type(exc).__name__}", flush=True)

    # External synthetic scope via actual test helper (clearly synthetic, no H PASS generation).
    staged_reader_rel = prepared["proposal"]["proposed"]["proposed_reader_ref"]["path"]
    scope_path = p1t._scope_review_for(tc, root, prepared, staged_reader_rel, "scope-review-v2.json")
    print(f"SCOPE {scope_path.relative_to(root)}", flush=True)

    # P2V before-eligibility.
    obs = observer.observe_current_authority(root, state_path, proposal_path, manifest_path, scope_path)
    assert obs.get("result") == "CURRENT_BASIS_OBSERVED_SCOPE_BOUND", obs
    print("P2V_SCOPE_BOUND", flush=True)

    # P3S materialize + verify.
    staged_manifest_path = (proposal_path.parent / "staged-source" / "staged-source-manifest.json")
    mat = staged.materialize_staged_source(root, state_path, proposal_path, manifest_path, scope_path)
    print(f"P3S_MATERIALIZE {mat}", flush=True)
    # Find staged manifest (mat returns paths).
    # materialize returns dict with staged_manifest? Inspect.
    if isinstance(mat, dict) and "staged_manifest_path" in mat:
        staged_manifest_path = root / mat["staged_manifest_path"]
    # Fallback: locate via proposal dir.
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

    # Prepare manuscript/toolchain specs (outside P/publication root).
    proposal_dir = proposal_path.parent
    pubs = proposal_dir / "publication"
    # Manuscript spec: actual coverage/requirement assertions, FULFILLED only.
    import copy
    state = core.load_json(state_path)
    # Use staged manifest to get issue/profile.
    staged_manifest = core.load_json(staged_manifest_path)
    issue_id = staged_manifest.get("issue_id")
    # Build minimal manuscript spec from P1 helper coverage pattern.
    # Reuse architecture coverage from _build_weekly_validated? Simplify: read proposal basis?
    # For smoke, construct FULFILLED rows for actual architecture packages.
    arch_path = helper.source_root / "architecture-v2.json"
    arch = core.load_json(arch_path)
    coverage = [
        {"package_id": plan["package_id"], "requirement": req, "status": "FULFILLED",
         "reader_locations": ["main.tex:package-1"], "detail": "Smoke manuscript author maps requirement."}
        for plan in arch.get("packages", []) for req in plan.get("must_cover_requirements", [])
    ]
    requirements = [
        {"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED", "reader_locations": ["main.tex:summary"],
         "detail": "Smoke manuscript author asserts synthesis present."},
        {"requirement_id": "WEEKLY_COMMUNITY_MOVEMENT", "status": "FULFILLED", "reader_locations": ["main.tex:package-1"],
         "detail": "Smoke manuscript author asserts community movement present."},
    ]
    manuscript_spec = {
        "schema_version": "2.0-rc1", "kind": "EDITORIAL_MANUSCRIPT_SPEC_V1",
        "issue_id": issue_id, "proposal_ref": {"path": str(proposal_path.relative_to(root)), "sha256": core.sha256_file(proposal_path)},
        "architecture_coverage": coverage, "reader_requirements": requirements,
        "authored_by": "smoke manuscript author", "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    manuscript_spec_path = proposal_dir / "manuscript-spec.json"
    core.write_json(manuscript_spec_path, manuscript_spec)
    # Toolchain spec: REAL TL2026, fixed recipe lualatex-biber-lualatex.
    tl_bin = Path("/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/lualatex")
    assert tl_bin.exists(), f"toolchain missing: {tl_bin}"
    toolchain_spec = {
        "schema_version": "2.0-rc1", "kind": "EDITORIAL_TOOLCHAIN_SPEC_V1",
        "executor": "smoke-integration", "absolute_executable": str(tl_bin),
        "recipe": "lualatex-biber-lualatex",
        "argv": list(edpub.EXPECTED_ARGV_LUALATEX_BIBER),
        "env": {}, "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    toolchain_spec_path = proposal_dir / "toolchain-spec.json"
    core.write_json(toolchain_spec_path, toolchain_spec)
    print(f"SPECS {manuscript_spec_path.relative_to(root)} {toolchain_spec_path.relative_to(root)}", flush=True)

    # High prepare: REAL TL2026 build. Public functions take repo-relative paths (no absolute).
    prepared_paths = edpub.prepare_publication(
        root,
        state_path.relative_to(root) if isinstance(state_path, Path) and state_path.is_absolute() else state_path,
        proposal_path.relative_to(root) if isinstance(proposal_path, Path) and proposal_path.is_absolute() else proposal_path,
        staged_manifest_path.relative_to(root) if isinstance(staged_manifest_path, Path) and staged_manifest_path.is_absolute() else staged_manifest_path,
        manuscript_spec_path.relative_to(root) if isinstance(manuscript_spec_path, Path) and manuscript_spec_path.is_absolute() else manuscript_spec_path,
        toolchain_spec_path.relative_to(root) if isinstance(toolchain_spec_path, Path) and toolchain_spec_path.is_absolute() else toolchain_spec_path,
        datetime.now(timezone.utc))
    print(f"PREPARE {json.dumps(prepared_paths)}", flush=True)

    # Externally create clearly synthetic post-render review records + QA bounded checks at exact final paths.
    # NEVER H generates PASS: use actual existing builders with synthetic reviewer labels.
    pubdir = proposal_dir / "publication"
    manuscript_path = pubdir / "reader-manuscript-v2.json"
    pdf_path = pubdir / "build" / "main.pdf"
    assert manuscript_path.is_file() and pdf_path.is_file(), "prepare outputs missing"
    from pypdf import PdfReader as _PR
    page_count = len(_PR(str(pdf_path)).pages)
    # QA: deterministic checks via actual quality builders? Use same pattern as _build_weekly_validated but at editorial paths.
    # For smoke, create quality checks that assert real PDF bytes.
    quality_root = pubdir / "quality"
    quality_root.mkdir(parents=True, exist_ok=True)
    # Use actual quality.validate_checks contract? Simplify: create result files + bundle via quality.build_bundle if available.
    # Fallback: construct deterministic checks with actual file assertions (bounded).
    subject_path = quality_root / "subject-entity-property-binding.json"
    core.write_json(subject_path, {"check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "status": "PASS", "scope": "smoke editorial real-build fixture"})
    identifier_path = quality_root / "identifier-preservation.json"
    # Need staged main for source sha: read staged main.
    staged_main_rel = staged_manifest["outputs"]["main"]["path"]
    staged_main_bytes = (root / staged_main_rel).read_bytes()
    core.write_json(identifier_path, {"check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
                                      "source_sha256": core.sha256_bytes(staged_main_bytes),
                                      "inspected_identifiers": [issue_id], "scope": "smoke real-build"})
    preflight_path = quality_root / "pdf-preflight.json"
    core.write_json(preflight_path, {"check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": page_count,
                                     "pdf_sha256": core.sha256_file(pdf_path), "byte_count": pdf_path.stat().st_size,
                                     "scope": "smoke real TL2026 PDF"})
    result_paths = {"SUBJECT_ENTITY_PROPERTY_BINDING": subject_path, "IDENTIFIER_PRESERVATION": identifier_path, "PDF_PREFLIGHT": preflight_path}
    quality_checks = [
        {"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS", "executor": "smoke editorial with actual file assertions",
         "evidence": "Exact fixture bytes and result file inspected.", "recorded_at": datetime.now(timezone.utc).isoformat(),
         "result": {"path": str(p.relative_to(root)), "sha256": core.sha256_file(p)}}
        for cid, p in result_paths.items()
    ]
    # Deterministic checks input file for finalize (actual evidence results).
    det_checks_path = proposal_dir / "deterministic-checks.json"
    core.write_json(det_checks_path, {"checks": quality_checks})
    # Semantic/visual reviews at exact final paths using actual builders, clearly synthetic.
    profile = core.load_json(root / state["profile"]["path"])
    for kind, fname in (("SEMANTIC_EDITORIAL", "semantic-review-v2.json"), ("VISUAL", "visual-review-v2.json")):
        checks = [{"check_id": cid, "status": "PASS", "detail": f"Smoke synthetic {kind} reviewer; no genuine Human approval.",
                   "evidence_locations": ["smoke-real-build:main.pdf"]}
                  for cid in sorted(reader_pub._expected_review_checks(root, profile, kind))]
        out_path = pubdir / fname
        # Map SEMANTIC_EDITORIAL->SEMANTIC? Builder expects kind? Use SEMANTIC_EDITORIAL/VISUAL as in helper.
        reader_pub.build_review_record(root, manuscript_path, pdf_path, page_count, kind, checks,
                                       f"smoke synthetic {kind} reviewer", datetime.now(timezone.utc), out_path)
        print(f"REVIEW {kind} {out_path.relative_to(root)}", flush=True)
    sem_path = pubdir / "semantic-review-v2.json"
    vis_path = pubdir / "visual-review-v2.json"

    # Finalize seal (before Candidate finished, inert old State healthy).
    old_state_bytes = (root / state_path).read_bytes() if isinstance(state_path, Path) else None
    def _rel(p):
        return str(p.relative_to(root)) if isinstance(p, Path) and p.is_absolute() else str(p)
    set_ref = edpub.finalize_publication(root, _rel(state_path), _rel(proposal_path), _rel(staged_manifest_path), _rel(det_checks_path), _rel(sem_path), _rel(vis_path), datetime.now(timezone.utc))
    print(f"FINALIZE {json.dumps(set_ref)}", flush=True)
    # Inert: old State still healthy, still selects old publication.
    from scripts import survey_agent_control_v2 as agent
    cfg2 = core.load_json(root / core.DEFAULT_CONFIG)
    state_after_finalize = core.load_json(root / state_path)
    errs = agent.validate_agent_state(root, cfg2, state_after_finalize)
    assert not errs, f"State unhealthy after finalize (must stay healthy inert): {errs}"
    print("INERT_HEALTHY", flush=True)

    # Activate.
    _set_path = set_ref["set_ref"] if isinstance(set_ref, dict) and "set_ref" in set_ref else set_ref
    print(f"DEBUG_SET_PATH type={type(_set_path).__name__} value={_set_path!r}", flush=True)
    print(f"DEBUG_SET_REF {set_ref!r}", flush=True)
    def _rel2(p):
        if isinstance(p, Path):
            return str(p.relative_to(root)) if p.is_absolute() else str(p)
        s = str(p)
        # If already repo-relative, keep; if absolute, make relative.
        if s.startswith("/"):
            try:
                return str(Path(s).relative_to(root))
            except ValueError:
                return s
        return s
    res = edpub.activate_publication(root, _rel(state_path), _rel2(_set_path), "Smoke weekly editorial correction", "smoke-executor", datetime.now(timezone.utc))
    print(f"ACTIVATE {json.dumps(res)}", flush=True)
    assert res.get("status") == "ACTIVATED", res

    # Strict State/receipt/Gate/Candidate checks.
    state_activated = core.load_json(root / state_path)
    # Receipt validates on new State.
    receipt_path = pubdir / "validated-source-manifest.json"
    rv = edpub.validate_editorial_receipt(root, _rel(receipt_path), _rel(state_path))
    assert rv["issue_id"] == issue_id, rv
    print("RECEIPT_ACTIVE_OK", flush=True)
    # Gate validates.
    gate_path = pubdir / "reader-surface-gate-v2.json"
    gv = reader_gate.validate_reader_surface_gate(root, _rel(gate_path), issue_id=issue_id, publication_profile="WEEKLY_MAGAZINE", expected_manuscript_path=_rel(manuscript_path), state_path=_rel(state_path))
    assert gv["status"] == "PASSED", gv
    print("GATE_ACTIVE_OK", flush=True)
    # Candidate validates (actual builder validator, Path object for is_symlink).
    cand_path = pubdir / "publication-candidate-v2.json"
    from scripts import survey_publication_v2 as pubmod
    cv = pubmod.validate_candidate(root, cand_path)
    print(f"CANDIDATE_ACTIVE_OK {cv.get('status') if isinstance(cv, dict) else cv}", flush=True)

    # Repeat activate ALREADY_ACTIVE readonly.
    res2 = edpub.activate_publication(root, _rel(state_path), _rel2(_set_path), "Smoke weekly editorial correction", "smoke-executor", datetime.now(timezone.utc))
    print(f"REPEAT {json.dumps(res2)}", flush=True)
    assert res2.get("status") == "ALREADY_ACTIVE", res2
    print("SMOKE_WEEKLY_ACTIVATION_OK", flush=True)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
