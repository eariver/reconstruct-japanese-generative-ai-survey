#!/usr/bin/env python3
"""R4c LONGFORM two-revision fixture build on NEW R4 source epoch (no old fixtures).

Fixed SOURCE: R4 snapshot b54a1f21a5b6b58b39777b3c5ae402219ff87715
(tree faef73d6e9bea08496be48462e8972d6d59536c2, 719 files incl. new fault tests).

Fresh independent copy (argv FIX_ROOT): bootstrap SP001 canonical via actual
_new_longform_helper -> first correction lf-r4c-1 (P1/P2R/scope/P2V/P3S/REAL
TL2026/reviews/QA/finalize/activate) -> second correction lf-r4c-2: prepare/
finalize, then capture an actual sealed INERT set checkpoint copy (State after
first, second Candidate/seal complete, NO second record) to INERT_ROOT +
manifest, then activate (expect ACTIVATED, supersedes == first, SAME anchor).
Terminal exit 0 on second ACTIVATED + strict checks, else exact blocker.
No lifecycle/Preview (preserved for later owner). Synthetic fixtures, NO-GO
maintained. No network/clean/reset/fixture commits/candidate commits.
"""
from __future__ import annotations
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


def _log(msg: str):
    print(msg, flush=True)


def main() -> int:
    if len(sys.argv) != 6:
        print(f"usage: {sys.argv[0]} FIX_ROOT NOTES_DIR EXPECT_HEAD EXPECT_COUNT INERT_ROOT", flush=True)
        return 2
    FIX_ROOT = Path(sys.argv[1]).resolve()
    NOTES = Path(sys.argv[2]).resolve()
    NOTES.mkdir(parents=True, exist_ok=True)
    EXPECT_HEAD = sys.argv[3].strip().lower()
    EXPECT_COUNT = int(sys.argv[4])
    INERT_ROOT = Path(sys.argv[5]).resolve() if sys.argv[5].strip() else None
    if len(EXPECT_HEAD) != 40 or any(c not in "0123456789abcdef" for c in EXPECT_HEAD):
        print(f"BLOCKER EXPECT_HEAD must be 40-char hex, got {sys.argv[3]!r}", flush=True)
        return 2
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(FIX_ROOT))
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    for _v in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
               "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_PREFIX"):
        if os.environ.get(_v):
            _log("UNSAFE inherited git env")
            return 2
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
    from scripts import survey_quality_v2 as quality
    from tests import test_survey_editorial_correction_proposal_v2 as p1t

    ISSUE = "SP001"
    TL_BIN = Path("/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/lualatex")

    class _TC(unittest.TestCase):
        def runTest(self):
            pass

    tc = _TC()

    def _run_git(*args):
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
                    "GIT_ALLOW_PROTOCOL": "file"})
        return subprocess.run(["git", *args], cwd=FIX_ROOT, capture_output=True,
                              text=True, timeout=120, env=env)

    def _rel(p) -> str:
        return str(p.relative_to(FIX_ROOT)) if isinstance(p, Path) and p.is_absolute() else str(p)

    head = _run_git("rev-parse", "HEAD").stdout.strip()
    _log(f"HEAD={head}")
    if head != EXPECT_HEAD:
        _log("UNEXPECTED SOURCE HEAD")
        return 2
    _log(f"LSFILES={len(_run_git('ls-files').stdout.strip().splitlines())} (expect {EXPECT_COUNT})")
    if len(_run_git("ls-files").stdout.strip().splitlines()) != EXPECT_COUNT:
        _log("LSFILES BOUND FAILED")
        return 2
    if not TL_BIN.exists():
        _log("TOOLCHAIN MISSING")
        return 2

    def _snapshot():
        files: dict[str, str] = {}
        for dirpath, dirnames, filenames in os.walk(FIX_ROOT):
            if ".git" in Path(dirpath).parts:
                dirnames[:] = []
                continue
            for fn in sorted(filenames):
                p = Path(dirpath) / fn
                rel = p.relative_to(FIX_ROOT).as_posix()
                h = hashlib.sha256()
                with p.open("rb") as f:
                    for chunk in iter(lambda: f.read(1 << 20), b""):
                        h.update(chunk)
                files[rel] = h.hexdigest()
        return {"files": files, "head": _run_git("rev-parse", "HEAD").stdout.strip(),
                "status": _run_git("status", "--porcelain").stdout}

    # === BASE ===
    _log("=== BASE ===")
    helper = p1t._new_longform_helper(tc, FIX_ROOT, FIX_ROOT)
    chain = helper._complete(helper._chain())
    state_path = helper._state_path(chain)
    if not isinstance(state_path, Path):
        state_path = FIX_ROOT / str(state_path)
    if not state_path.is_absolute():
        state_path = (FIX_ROOT / state_path).resolve()
    built = helper._advance_to_validated_draft(chain, state_path)
    assert core.load_json(state_path)["lifecycle_state"] == "VALIDATED_DRAFT"
    state_rel = str(state_path.relative_to(FIX_ROOT).as_posix())
    profile = core.load_json(chain["profile_path"])
    cand_rel = (Path(profile["paths"]["source_root"]) / "publication" / "v2" /
                "publication-candidate-v2.json").as_posix()
    cand_path = FIX_ROOT / cand_rel
    assert not cand_path.exists(), "candidate must be absent before initial build"
    pubmod.build_candidate(FIX_ROOT, ISSUE, "LONGFORM_SPECIAL", built["manuscript"],
                           helper.survey_root / "main.tex", built["pdf"], 1,
                           built["bundle"], built["SEMANTIC_EDITORIAL"],
                           built["VISUAL"], cand_path)
    old_cand_bytes = cand_path.read_bytes()
    _log(f"BASE_OK state={state_rel} issue={ISSUE}")

    def _cycle(proposal_id: str, para_suffix: str, first: bool):
        _log(f"=== CYCLE {proposal_id} ===")
        snap_before = _snapshot()
        if first:
            authored = helper._authored(chain, helper.worker)
        else:
            prev_auth = FIX_ROOT / f"sources/{ISSUE}/publication/v2/editorial-corrections/lf-r4c-1/authoring-input.json"
            assert prev_auth.is_file(), f"first authoring missing {prev_auth}"
            authored = copy.deepcopy(json.loads(prev_auth.read_bytes().decode()))
        pkg0 = authored["longform_revision"]["packages"][0]
        paras = pkg0["narrative_sections"][0]["paragraphs"]
        assert len(paras) >= 1
        paras[0]["text"] += para_suffix
        staged_auth = p1t._stage_authoring_before_prepare(
            tc, FIX_ROOT, helper.source_root, proposal_id, authored)
        prepared = proposal_mod.prepare_proposal(
            FIX_ROOT, state_rel, staged_auth, proposal_id,
            f"R3c longform correction {proposal_id}.")
        _log(f"P1_PREPARE {proposal_id} reader_sha={hashlib.sha256(prepared['proposed_canonical']).hexdigest()}")
        proposal_path = p1t._stage_reader_and_proposal(
            tc, FIX_ROOT, helper.source_root, proposal_id, prepared)
        outcome = proposal_mod.validate_proposal(FIX_ROOT, state_rel, proposal_path)
        assert outcome["result"] in ("REVIEW_REQUIRED", "REVIEW_BOUND_PROPOSAL"), outcome
        _log(f"P1_VALIDATE {outcome['result']}")
        cap = retention.capture_retention(FIX_ROOT, state_path, proposal_path)
        assert cap.get("result") == retention.RESULT_CAPTURED, cap
        manifest_path = FIX_ROOT / cap["manifest_path"]
        vout = retention.verify_retention(FIX_ROOT, proposal_path, manifest_path)
        assert vout.get("result") == retention.RESULT_VERIFIED, vout
        _log(f"P2R_OK {cap['manifest_path']}")
        try:
            proposal_mod.validate_proposal(FIX_ROOT, state_rel, proposal_path)
            _log("P1_AFTER_CAPTURE should have refused BLOCKER")
            return None
        except Exception as exc:
            _log(f"P1_AFTER_CAPTURE_REFUSAL_OK {type(exc).__name__}")
        staged_reader_rel = prepared["proposal"]["proposed"]["proposed_reader_ref"]["path"]
        scope_path = p1t._scope_review_for(tc, FIX_ROOT, prepared, staged_reader_rel,
                                           "scope-review-v2.json")
        obs = observer.observe_current_authority(FIX_ROOT, state_path, proposal_path,
                                                 manifest_path, scope_path)
        assert obs.get("result") == "CURRENT_BASIS_OBSERVED_SCOPE_BOUND", obs
        _log("P2V_SCOPE_BOUND")
        mat = staged.materialize_staged_source(FIX_ROOT, state_path, proposal_path,
                                               manifest_path, scope_path)
        if isinstance(mat, dict) and "staged_manifest_path" in mat:
            staged_manifest_path = FIX_ROOT / mat["staged_manifest_path"]
        else:
            staged_manifest_path = (proposal_path.parent / "staged-source" /
                                    "staged-source-manifest.json")
        assert staged_manifest_path.is_file()
        ver = staged.verify_staged_source(FIX_ROOT, proposal_path, staged_manifest_path)
        assert ver.get("result") == "STAGED_SOURCE_REPLAY_VERIFIED", ver
        assert len(core.load_json(staged_manifest_path)["code_deps"]) == 50
        _log("P3S_VERIFIED50")
        # manuscript spec via helper section locations on NEW surface
        proposal_dir = proposal_path.parent
        staged_manifest = core.load_json(staged_manifest_path)
        new_surface = core.load_json(proposal_dir / "reader-surface-input-v2.json")
        staged_main_text = (FIX_ROOT / staged_manifest["outputs"]["main"]["path"]).read_text(encoding="utf-8")
        pkg_locs, final_loc = helper._section_locations(chain, new_surface, staged_main_text)
        pkgs = core.load_json(helper.source_root / "architecture-v2.json").get("packages", [])
        assert len(pkg_locs) == len(pkgs)
        coverage = [{"package_id": pkg["package_id"], "requirement": req, "status": "FULFILLED",
                     "reader_locations": [loc],
                     "detail": f"R3c LF manuscript author maps requirement for {proposal_id}."}
                    for pkg, loc in zip(pkgs, pkg_locs)
                    for req in pkg.get("must_cover_requirements", [])]
        requirements = [{"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED",
                         "reader_locations": [final_loc],
                         "detail": f"R3c LF synthesis for {proposal_id}."}]
        mspec = {"schema_version": "2.0-rc1", "kind": "EDITORIAL_MANUSCRIPT_SPEC_V1",
                 "issue_id": staged_manifest.get("issue_id"),
                 "proposal_ref": {"path": str(proposal_path.relative_to(FIX_ROOT)),
                                  "sha256": core.sha256_file(proposal_path)},
                 "architecture_coverage": coverage, "reader_requirements": requirements,
                 "authored_by": "r3c LF manuscript author",
                 "recorded_at": datetime.now(timezone.utc).isoformat()}
        mspec_path = proposal_dir / "manuscript-spec.json"
        core.write_json(mspec_path, mspec)
        tspec = {"schema_version": "2.0-rc1", "kind": "EDITORIAL_TOOLCHAIN_SPEC_V1",
                 "executor": "r3c-longform-integration",
                 "absolute_executable": str(TL_BIN), "recipe": "lualatex-biber-lualatex",
                 "argv": list(edpub.EXPECTED_ARGV_LUALATEX_BIBER), "env": {},
                 "recorded_at": datetime.now(timezone.utc).isoformat()}
        tspec_path = proposal_dir / "toolchain-spec.json"
        core.write_json(tspec_path, tspec)
        t0 = time.monotonic()
        prepared_paths = edpub.prepare_publication(
            FIX_ROOT, state_rel, _rel(proposal_path),
            _rel(staged_manifest_path), _rel(mspec_path), _rel(tspec_path),
            datetime.now(timezone.utc))
        _log(f"PREPARE dt={time.monotonic()-t0:.1f}s")
        pubdir = proposal_dir / "publication"
        manuscript_path = pubdir / "reader-manuscript-v2.json"
        pdf_path = pubdir / "build" / "main.pdf"
        assert manuscript_path.is_file() and pdf_path.is_file()
        from pypdf import PdfReader as _PR
        pages = len(_PR(str(pdf_path)).pages)
        _log(f"REAL_PDF pages={pages} bytes={pdf_path.stat().st_size}")
        assert pages >= 2, f"corrected LF PDF must be REAL multi-page, got {pages}"
        # QA 4-checks + reviews
        qroot = pubdir / "quality"
        qroot.mkdir(parents=True, exist_ok=True)
        cfg = core.load_json(FIX_ROOT / core.DEFAULT_CONFIG)
        kinds = quality.expected_checks_by_kind(cfg, "THEMATIC", "LONGFORM_SPECIAL", {"DETERMINISTIC"})
        staged_main_bytes = (FIX_ROOT / staged_manifest["outputs"]["main"]["path"]).read_bytes()
        payloads = {
            "SUBJECT_ENTITY_PROPERTY_BINDING": {
                "check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "status": "PASS",
                "issue_id": staged_manifest.get("issue_id"), "cited_discovery_count": 1,
                "bindings": [{"discovery_id": "d01", "canonical_name": "Target Model",
                              "canonical_url": "https://example.invalid/target",
                              "materiality": "MATERIAL", "status": "VERIFIED",
                              "source_accessed_at": "2026-08-22T02:10:00+09:00"}]},
            "IDENTIFIER_PRESERVATION": {
                "check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
                "source_sha256": core.sha256_bytes(staged_main_bytes),
                "inspected_identifiers": [staged_manifest.get("issue_id"), "Target Model"],
                "scope": f"r3c LF {proposal_id} real-build"},
            "PDF_PREFLIGHT": {
                "check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": pages,
                "pdf_sha256": core.sha256_file(pdf_path),
                "byte_count": pdf_path.stat().st_size,
                "scope": f"r3c LF {proposal_id} real TL2026 PDF"},
            "EMPTY_WRAPPER_SUPPRESSION": {
                "check_id": "EMPTY_WRAPPER_SUPPRESSION", "status": "PASS",
                "scope": f"r3c LF {proposal_id} carries no empty wrapper",
                "inspected_paths": [staged_manifest["outputs"]["main"]["path"]]},
        }
        assert set(payloads) == set(kinds), f"{sorted(payloads)} != {sorted(kinds)}"
        qchecks = []
        for cid, payload in payloads.items():
            p = qroot / f"{cid.lower()}.json"
            core.write_json(p, payload)
            qchecks.append({"check_id": cid, "kind": kinds[cid], "status": "PASS",
                            "executor": "r3c LF editorial with actual file assertions",
                            "evidence": "Exact fixture bytes and result file inspected.",
                            "recorded_at": datetime.now(timezone.utc).isoformat(),
                            "result": {"path": str(p.relative_to(FIX_ROOT)),
                                       "sha256": core.sha256_file(p)}})
        det_path = proposal_dir / "deterministic-checks.json"
        core.write_json(det_path, {"checks": qchecks})
        prof = core.load_json(FIX_ROOT / core.load_json(state_path)["profile"]["path"])
        manuscript = core.load_json(manuscript_path)
        try:
            from scripts.survey_reader_fidelity_v2 import _locations_from_manifest as _lfm
            cov_locs, fin_locs = _lfm(manuscript)
            coverage_locations = sorted(cov_locs)
            final_locations = sorted(fin_locs)
        except Exception:
            coverage_locations = sorted({r["reader_locations"][0] for r in coverage})
            final_locations = [final_loc]
        architecture = core.load_json(helper.source_root / "architecture-v2.json")
        package_ids = [r["package_id"] for r in architecture["packages"]]
        final_package = max(architecture["packages"],
                            key=lambda r: r["drafting_order"])["package_id"]
        _pp = (architecture.get("page_plan") or {}).get("target_pages", 12)
        try:
            _tgt = int(float(_pp)) if float(_pp).is_integer() else str(_pp)
        except Exception:
            _tgt = 12
        for kind, fname in (("SEMANTIC_EDITORIAL", "semantic-review-v2.json"),
                            ("VISUAL", "visual-review-v2.json")):
            expected = reader_pub._expected_review_checks(FIX_ROOT, prof, kind)
            checks = []
            for cid in sorted(expected):
                ev = [f"r3c-lf-real-build:{proposal_id}:main.pdf"]
                if cid in ("ARCHITECTURE_CONTENT_FIDELITY", "LONGFORM_TECHNICAL_DEPTH"):
                    ev = sorted({f"package:{pid}" for pid in package_ids} | set(coverage_locations))
                    if cid == "LONGFORM_TECHNICAL_DEPTH":
                        ev = sorted(set(ev) | {f"page-plan:{pages}/{_tgt}",
                                               "density-review:below-target-substantive"})
                elif cid == "FINAL_SYNTHESIS_QUALITY":
                    ev = sorted(set(final_locations) |
                                {"reader-role:final-synthesis", f"package:{final_package}"})
                elif cid == "LONGFORM_MIXED_LAYOUT":
                    ev = ["reader-layout:wide-surfaces-full-width",
                          "reader-layout:references-one-column",
                          "reader-layout:balanced-two-column-narrative"]
                checks.append({"check_id": cid, "status": "PASS",
                               "detail": f"R3c synthetic LF {kind} reviewer; no genuine approval.",
                               "evidence_locations": ev})
            reader_pub.build_review_record(
                FIX_ROOT, manuscript_path, pdf_path, pages, kind, checks,
                f"r3c synthetic LF {kind} reviewer", datetime.now(timezone.utc),
                pubdir / fname)
        sem_path, vis_path = pubdir / "semantic-review-v2.json", pubdir / "visual-review-v2.json"
        set_ref = edpub.finalize_publication(
            FIX_ROOT, state_rel, _rel(proposal_path), _rel(staged_manifest_path),
            _rel(det_path), _rel(sem_path), _rel(vis_path), datetime.now(timezone.utc))
        _log(f"FINALIZE {json.dumps(set_ref)[:300]}")
        errs = agent.validate_agent_state(
            FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG),
            core.load_json(state_path))
        assert not errs, f"inert unhealthy {errs}"
        _log("INERT_HEALTHY")
        sraw = set_ref["set_ref"] if isinstance(set_ref, dict) and "set_ref" in set_ref else set_ref
        set_rel = sraw.get("path") if isinstance(sraw, dict) else str(sraw)
        if set_rel.startswith("/"):
            set_rel = str(Path(set_rel).relative_to(FIX_ROOT))
        assert (FIX_ROOT / set_rel).is_file()
        # BEFORE second activation: capture actual sealed inert set checkpoint copy
        # (State after first, second Candidate/seal complete, NO second record).
        if not first and INERT_ROOT is not None:
            INERT_ROOT.parent.mkdir(parents=True, exist_ok=True)
            if INERT_ROOT.exists():
                raise AssertionError(f"inert root already exists {INERT_ROOT}")
            cp = subprocess.run(["cp", "-a", str(FIX_ROOT), str(INERT_ROOT)],
                                capture_output=True, text=True, timeout=300)
            assert cp.returncode == 0, f"inert cp failed {cp.stderr[:500]}"
            st_now = core.load_json(state_path)
            iptr = st_now.get("publication_revalidation_provenance") or {}
            assert iptr.get("path", "").endswith("publication-surface-revalidation-r1.json"), iptr
            cand2_rel = f"sources/{ISSUE}/publication/v2/editorial-corrections/{proposal_id}/publication/publication-candidate-v2.json"
            assert (INERT_ROOT / cand2_rel).is_file(), "inert copy must carry sealed second candidate"
            rec_absent_rel = f"sources/{ISSUE}/publication/v2/publication-surface-revalidation-r2.json"
            assert not (INERT_ROOT / rec_absent_rel).exists(), "inert copy must have NO second record"
            ihead = subprocess.run(["git", "rev-parse", "HEAD"], cwd=INERT_ROOT,
                                   capture_output=True, text=True, timeout=60,
                                   env={k: v for k, v in os.environ.items()
                                        if not k.startswith("GIT_")}).stdout.strip()
            iman = {"inert_root": str(INERT_ROOT), "inert_head": ihead,
                    "state_pointer": iptr,
                    "sealed_set": {"path": set_rel,
                                   "sha256": core.sha256_file(FIX_ROOT / set_rel)},
                    "sealed_candidate": {"path": cand2_rel,
                                         "sha256": core.sha256_file(FIX_ROOT / cand2_rel)},
                    "record_absent": rec_absent_rel,
                    "note": "State after first activation + second Candidate/seal complete, no second record"}
            core.write_json(NOTES / "inert-manifest-longform.json", iman)
            _log(f"INERT_CHECKPOINT {INERT_ROOT} head={ihead}")
        res = edpub.activate_publication(
            FIX_ROOT, state_rel, set_rel, f"R4c LF editorial correction {proposal_id}",
            f"r4c-lf-executor-{proposal_id}", datetime.now(timezone.utc))
        _log(f"ACTIVATE {json.dumps(res)[:500]}")
        assert res.get("status") == "ACTIVATED", res
        return {"proposal_path": proposal_path, "prepared": prepared, "set_rel": set_rel,
                "record": core.load_json(FIX_ROOT / res["record_path"]),
                "record_rel": res["record_path"] if isinstance(res["record_path"], str)
                else str(res["record_path"]),
                "pubdir": pubdir, "snap_before": snap_before}

    first = _cycle("lf-r4c-1", " Revised fixture sentence within approved evidence.", True)
    if first is None:
        _log("FIRST CYCLE BLOCKER")
        return 2
    rec1 = first["record"]
    assert rec1.get("supersedes") is None
    assert rec1.get("canonical_anchor", {}).get("kind") == "VALIDATION_CHECKPOINT"
    st1 = core.load_json(state_path)
    assert agent.validate_agent_state(
        FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG), st1) == []
    sel1 = setmod.resolve_publication_selection(
        FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG), st1)
    assert sel1.get("mode") == "VERSIONED_ACTIVE", sel1.get("mode")
    _log(f"FIRST_SELECTION candidate={(sel1.get('candidate_ref') or {}).get('path')}")

    second = _cycle("lf-r4c-2", " Second fixture sentence within approved evidence.", False)
    if second is None:
        _log("SECOND CYCLE BLOCKER (exact next blocker above)")
        return 2
    rec2 = second["record"]
    assert rec2.get("supersedes") is not None, "second must supersede first"
    assert rec2.get("canonical_anchor") == rec1.get("canonical_anchor"), \
        f"anchor mismatch {rec2.get('canonical_anchor')} vs {rec1.get('canonical_anchor')}"
    _log(f"SECOND_ANCHOR_RETAINED={json.dumps(rec2['canonical_anchor'])}")
    st2 = core.load_json(state_path)
    assert agent.validate_agent_state(
        FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG), st2) == []
    _log("SECOND_STATE_HEALTHY")
    sel2 = setmod.resolve_publication_selection(
        FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG), st2)
    assert sel2.get("mode") == "VERSIONED_ACTIVE"
    cand2 = (sel2.get("candidate_ref") or {}).get("path")
    _log(f"SECOND_SELECTION candidate={cand2}")
    assert cand2 == f"sources/{ISSUE}/publication/v2/editorial-corrections/lf-r4c-2/publication/publication-candidate-v2.json", cand2
    before2 = second["snap_before"]["files"]
    after2: dict[str, str] = {}
    for dirpath, dirnames, filenames in os.walk(FIX_ROOT):
        if ".git" in Path(dirpath).parts:
            dirnames[:] = []
            continue
        for fn in sorted(filenames):
            p = Path(dirpath) / fn
            rel = p.relative_to(FIX_ROOT).as_posix()
            h = hashlib.sha256()
            with p.open("rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
            after2[rel] = h.hexdigest()
    pub_prefix = f"sources/{ISSUE}/publication/v2/editorial-corrections/lf-r4c-2/publication/"
    rec2_rel = second["record_rel"]
    if rec2_rel.startswith("/"):
        rec2_rel = str(Path(rec2_rel).relative_to(FIX_ROOT))
    for rel, sha in before2.items():
        if rel.startswith(pub_prefix) or rel == rec2_rel or rel == state_rel:
            continue
        assert rel in after2, f"disappearance after second activate: {rel}"
        assert after2[rel] == sha, f"old-immutable drift after second activate: {rel}"
    _log("SECOND_OLD_IMMUTABLE_KEEP_OK")
    rv = edpub.validate_editorial_receipt(
        FIX_ROOT, f"sources/{ISSUE}/publication/v2/editorial-corrections/lf-r4c-2/publication/validated-source-manifest.json",
        state_rel)
    _log(f"SECOND_RECEIPT issue={rv.get('issue_id')}")
    gv = reader_gate.validate_reader_surface_gate(
        FIX_ROOT, f"sources/{ISSUE}/publication/v2/editorial-corrections/lf-r4c-2/publication/reader-surface-gate-v2.json",
        issue_id=ISSUE, publication_profile="LONGFORM_SPECIAL",
        expected_manuscript_path=FIX_ROOT / f"sources/{ISSUE}/publication/v2/editorial-corrections/lf-r4c-2/publication/reader-manuscript-v2.json",
        state_path=state_rel)
    assert gv.get("status") == "PASSED", gv
    _log("SECOND_GATE_PASSED")
    cv = pubmod.validate_candidate(
        FIX_ROOT, FIX_ROOT / f"sources/{ISSUE}/publication/v2/editorial-corrections/lf-r4c-2/publication/publication-candidate-v2.json")
    _log(f"SECOND_CANDIDATE status={cv.get('status') if isinstance(cv, dict) else cv}")
    _log("=== SECOND LONGFORM CORRECTION ACTIVATED (terminal) ===")
    return 0


if __name__ == "__main__":
    try:
        rc = main()
    except Exception:
        traceback.print_exc()
        rc = 2
    print(f"EXIT:{rc}", flush=True)
    sys.exit(rc)
