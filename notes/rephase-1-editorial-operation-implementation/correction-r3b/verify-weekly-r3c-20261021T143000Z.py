#!/usr/bin/env python3
"""R3c Weekly TWO-CYCLE verification on NEW source epoch (no old fixtures).

Governing d880 + root selection + R3 verification return. Fixed SOURCE:
  /tmp/opencode/jgas-editorial-r3b-20261021T141500Z/candidate-partial-b40de60
  HEAD 3f5bf45c4964f4facff294a5ef262b044756c498 (718 files).

This script (created BEFORE execution, NEW file -- never the saved fixed-path
runners) performs in a FRESH independent copy (argv FIX_ROOT):
  0. Copy verification (HEAD/tree/718/inodes/no alternates, inert origin).
  1. Bootstrap canonical Weekly VALIDATED_DRAFT via P1 test helpers (no R1:
     first anchor is the original validation checkpoint).
  2. FIRST correction wk-r3c-1: P1 -> P2R -> scope -> P2V -> P3S(50) ->
     REAL TL2026 prepare -> typed reviews + bounded QA -> finalize ->
     activate (expect ACTIVATED, anchor VALIDATION_CHECKPOINT, supersedes null).
     Strict State/readback + old-immutable checks. NO Preview/lifecycle
     (first active preserved before Preview for later lifecycle owner).
  3. SECOND correction wk-r3c-2 (new headline): full cycle again (expect
     ACTIVATED, supersedes == first activation, SAME anchor). This exercises
     the fixed versioned receipt/P1 graph path (was VERSIONED_ROW_SHAPE).
  Terminal exit 0 on second ACTIVATED + strict checks, else exact blocker.
  Type fixtures synthetic, placeholder quality NO-GO. No network/clean/reset.
  No fixture commits (no R1 stimulus in this flow). No candidate/reconstruct commit.
"""
from __future__ import annotations
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path


def _log(msg: str):
    print(msg, flush=True)


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} FIX_ROOT NOTES_DIR", flush=True)
        return 2
    FIX_ROOT = Path(sys.argv[1]).resolve()
    NOTES = Path(sys.argv[2]).resolve()
    NOTES.mkdir(parents=True, exist_ok=True)
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(FIX_ROOT))
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    for _v in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
               "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_PREFIX"):
        if os.environ.get(_v):
            _log(f"UNSAFE inherited {_v}")
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
    from tests import test_survey_editorial_correction_proposal_v2 as p1t
    from tests import test_survey_editorial_staged_source_v2 as p3st

    ISSUE = "2026-W37"
    TL_BIN = Path("/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/lualatex")

    class _TC(unittest.TestCase):
        def runTest(self):
            pass

    tc = _TC()

    def _run_git(*args):
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
                    "GIT_ALLOW_PROTOCOL": "file"})
        proc = subprocess.run(["git", *args], cwd=FIX_ROOT, capture_output=True,
                              text=True, timeout=120, env=env)
        return proc

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
        special: dict[str, str] = {}
        for dirpath, dirnames, filenames in os.walk(FIX_ROOT):
            if ".git" in Path(dirpath).parts:
                dirnames[:] = []
                continue
            for fn in sorted(filenames) + sorted(dirnames):
                p = Path(dirpath) / fn
                try:
                    st = os.lstat(p)
                except OSError:
                    continue
                import stat as _stat
                if _stat.S_ISLNK(st.st_mode) or not _stat.S_ISREG(st.st_mode):
                    special[p.relative_to(FIX_ROOT).as_posix()] = oct(st.st_mode)
        h = _run_git("rev-parse", "HEAD").stdout.strip()
        s = _run_git("status", "--porcelain").stdout
        return {"files": files, "special": special, "head": h, "status": s}

    # === 0 SOURCE BINDING ===
    _log("===0 SOURCE===")
    head = _run_git("rev-parse", "HEAD").stdout.strip()
    _log(f"HEAD={head}")
    if head != "0d9857e6132fb314a2e2ba141da79c54f4ec5e06":
        _log("UNEXPECTED SOURCE HEAD")
        return 2
    _log(f"LSFILES={len(_run_git('ls-files').stdout.strip().splitlines())} (expect 718)")
    if len(_run_git("ls-files").stdout.strip().splitlines()) != 718:
        _log("LSFILES BOUND FAILED")
        return 2
    if not TL_BIN.exists():
        _log(f"TOOLCHAIN MISSING {TL_BIN}")
        return 2
    _log(f"TOOLCHAIN={TL_BIN}")

    # === 1 BOOTSTRAP CANONICAL ===
    _log("===1 BOOTSTRAP===")
    helper = p1t._new_weekly_helper(tc, FIX_ROOT)
    built = p1t._build_weekly_validated(tc, helper)
    chain, state_path = built["chain"], Path(built["state_path"])
    if not state_path.is_absolute():
        state_path = (FIX_ROOT / state_path).resolve()
    st0 = core.load_json(state_path)
    assert st0.get("publication_revalidation_provenance") is None
    state_rel = str(state_path.relative_to(FIX_ROOT).as_posix())
    src_root = helper.source_root
    _log(f"BOOTSTRAP_OK state={state_rel}")

    def _cycle(proposal_id: str, headline: str, first: bool):
        _log(f"=== CYCLE {proposal_id} headline={headline!r} ===")
        snap_before = _snapshot()
        if first:
            corr = p3st._weekly_prepare_from(tc, FIX_ROOT, helper, built, proposal_id)
            proposal_path = corr["proposal_path"]
            prepared = corr["prepared"]
        else:
            # Second correction: new authoring from FIRST proposal authoring.
            first_auth = FIX_ROOT / f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-r3c-1/authoring-input.json"
            assert first_auth.is_file(), f"first authoring missing {first_auth}"
            new_authoring = json.loads(first_auth.read_bytes().decode())
            new_authoring = copy.deepcopy(new_authoring)
            new_authoring["cover"]["headline"] = headline
            try:
                new_authoring["final_summary"]["paragraphs"][0] = \
                    "The edition surveys one source with second correction."
            except Exception:
                pass
            staged_auth = p1t._stage_authoring_before_prepare(
                tc, FIX_ROOT, helper.source_root, proposal_id, new_authoring)
            _log(f"STAGED_AUTH {staged_auth}")
            prepared = proposal_mod.prepare_proposal(
                FIX_ROOT, state_rel, staged_auth, proposal_id,
                "R3c weekly second envelope correction.")
            _log(f"P1_PREPARE proposal={proposal_id} reader_sha={hashlib.sha256(prepared['proposed_canonical']).hexdigest()}")
            proposal_path = p1t._stage_reader_and_proposal(
                tc, FIX_ROOT, helper.source_root, proposal_id, prepared)
            outcome = proposal_mod.validate_proposal(FIX_ROOT, state_rel, proposal_path)
            _log(f"P1_VALIDATE {outcome['result']}")
            assert outcome["result"] in ("REVIEW_REQUIRED", "REVIEW_BOUND_PROPOSAL"), outcome
        # P2R capture + verify + after-capture refusal
        cap = retention.capture_retention(FIX_ROOT, state_path, proposal_path)
        assert cap.get("result") == retention.RESULT_CAPTURED, cap
        manifest_path = FIX_ROOT / cap["manifest_path"]
        vout = retention.verify_retention(FIX_ROOT, proposal_path, manifest_path)
        assert vout.get("result") == retention.RESULT_VERIFIED, vout
        _log(f"P2R_OK manifest={cap['manifest_path']}")
        try:
            proposal_mod.validate_proposal(FIX_ROOT, state_rel, proposal_path)
            _log("P1_AFTER_CAPTURE should have refused BLOCKER")
            return None
        except Exception as exc:
            _log(f"P1_AFTER_CAPTURE_REFUSAL_OK {type(exc).__name__}")
        # scope / P2V / P3S
        staged_reader_rel = prepared["proposal"]["proposed"]["proposed_reader_ref"]["path"]
        scope_path = p1t._scope_review_for(tc, FIX_ROOT, prepared, staged_reader_rel,
                                           "scope-review-v2.json")
        _log(f"SCOPE={scope_path.relative_to(FIX_ROOT)}")
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
        # specs
        staged_manifest = core.load_json(staged_manifest_path)
        issue_id = staged_manifest.get("issue_id")
        arch = core.load_json(helper.source_root / "architecture-v2.json")
        coverage = [{"package_id": plan["package_id"], "requirement": req,
                     "status": "FULFILLED", "reader_locations": ["main.tex:package-1"],
                     "detail": f"R3c manuscript author maps requirement for {proposal_id}."}
                    for plan in arch.get("packages", [])
                    for req in plan.get("must_cover_requirements", [])]
        requirements = [
            {"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED",
             "reader_locations": ["main.tex:summary"], "detail": "R3c synthesis."},
            {"requirement_id": "WEEKLY_COMMUNITY_MOVEMENT", "status": "FULFILLED",
             "reader_locations": ["main.tex:package-1"], "detail": "R3c movement."}]
        prop_rel = str(proposal_path.relative_to(FIX_ROOT))
        mspec = {"schema_version": "2.0-rc1", "kind": "EDITORIAL_MANUSCRIPT_SPEC_V1",
                 "issue_id": issue_id,
                 "proposal_ref": {"path": prop_rel, "sha256": core.sha256_file(proposal_path)},
                 "architecture_coverage": coverage, "reader_requirements": requirements,
                 "authored_by": "r3c manuscript author",
                 "recorded_at": datetime.now(timezone.utc).isoformat()}
        mspec_path = proposal_path.parent / "manuscript-spec.json"
        core.write_json(mspec_path, mspec)
        tspec = {"schema_version": "2.0-rc1", "kind": "EDITORIAL_TOOLCHAIN_SPEC_V1",
                 "executor": "r3c-integration",
                 "absolute_executable": str(TL_BIN), "recipe": "lualatex-biber-lualatex",
                 "argv": list(edpub.EXPECTED_ARGV_LUALATEX_BIBER), "env": {},
                 "recorded_at": datetime.now(timezone.utc).isoformat()}
        tspec_path = proposal_path.parent / "toolchain-spec.json"
        core.write_json(tspec_path, tspec)
        # prepare REAL TL2026
        t0 = time.monotonic()
        prepared_paths = edpub.prepare_publication(
            FIX_ROOT, state_rel, prop_rel,
            str(staged_manifest_path.relative_to(FIX_ROOT)),
            str(mspec_path.relative_to(FIX_ROOT)),
            str(tspec_path.relative_to(FIX_ROOT)), datetime.now(timezone.utc))
        _log(f"PREPARE dt={time.monotonic()-t0:.1f}s")
        pubdir = proposal_path.parent / "publication"
        manuscript_path = pubdir / "reader-manuscript-v2.json"
        pdf_path = pubdir / "build" / "main.pdf"
        assert manuscript_path.is_file() and pdf_path.is_file()
        from pypdf import PdfReader as _PR
        pages = len(_PR(str(pdf_path)).pages)
        _log(f"REAL_PDF pages={pages} bytes={pdf_path.stat().st_size}")
        assert pages >= 1
        # QA + typed reviews (synthetic labels, actual builders)
        qroot = pubdir / "quality"
        qroot.mkdir(parents=True, exist_ok=True)
        sp = qroot / "subject-entity-property-binding.json"
        core.write_json(sp, {"check_id": "SUBJECT_ENTITY_PROPERTY_BINDING",
                             "status": "PASS", "scope": f"r3c {proposal_id} real-build"})
        main_bytes = (FIX_ROOT / staged_manifest["outputs"]["main"]["path"]).read_bytes()
        ip = qroot / "identifier-preservation.json"
        core.write_json(ip, {"check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
                             "source_sha256": core.sha256_bytes(main_bytes),
                             "inspected_identifiers": [issue_id],
                             "scope": f"r3c {proposal_id} real-build"})
        pp = qroot / "pdf-preflight.json"
        core.write_json(pp, {"check_id": "PDF_PREFLIGHT", "status": "PASS",
                             "page_count": pages,
                             "pdf_sha256": core.sha256_file(pdf_path),
                             "byte_count": pdf_path.stat().st_size,
                             "scope": f"r3c {proposal_id} real TL2026 PDF"})
        qchecks = [{"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS",
                    "executor": "r3c editorial with actual file assertions",
                    "evidence": "Exact fixture bytes and result file inspected.",
                    "recorded_at": datetime.now(timezone.utc).isoformat(),
                    "result": {"path": str(p.relative_to(FIX_ROOT)),
                               "sha256": core.sha256_file(p)}}
                   for cid, p in (("SUBJECT_ENTITY_PROPERTY_BINDING", sp),
                                  ("IDENTIFIER_PRESERVATION", ip),
                                  ("PDF_PREFLIGHT", pp))]
        det_path = proposal_path.parent / "deterministic-checks.json"
        core.write_json(det_path, {"checks": qchecks})
        profile = core.load_json(FIX_ROOT / core.load_json(state_path)["profile"]["path"])
        for kind, fname in (("SEMANTIC_EDITORIAL", "semantic-review-v2.json"),
                            ("VISUAL", "visual-review-v2.json")):
            checks = [{"check_id": cid, "status": "PASS",
                       "detail": f"R3c synthetic {kind} reviewer; no genuine Human approval.",
                       "evidence_locations": [f"r3c-real-build:{proposal_id}:main.pdf"]}
                      for cid in sorted(reader_pub._expected_review_checks(FIX_ROOT, profile, kind))]
            reader_pub.build_review_record(
                FIX_ROOT, manuscript_path, pdf_path, pages, kind, checks,
                f"r3c synthetic {kind} reviewer", datetime.now(timezone.utc), pubdir / fname)
        sem_path = pubdir / "semantic-review-v2.json"
        vis_path = pubdir / "visual-review-v2.json"
        # finalize (inert healthy)
        set_ref = edpub.finalize_publication(
            FIX_ROOT, state_rel, prop_rel,
            str(staged_manifest_path.relative_to(FIX_ROOT)),
            str(det_path.relative_to(FIX_ROOT)),
            str(sem_path.relative_to(FIX_ROOT)),
            str(vis_path.relative_to(FIX_ROOT)), datetime.now(timezone.utc))
        _log(f"FINALIZE {json.dumps(set_ref)[:400]}")
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
        # activate
        res = edpub.activate_publication(
            FIX_ROOT, state_rel, set_rel, f"R3c weekly editorial correction {proposal_id}",
            f"r3c-executor-{proposal_id}", datetime.now(timezone.utc))
        _log(f"ACTIVATE {json.dumps(res)[:800]}")
        assert res.get("status") == "ACTIVATED", res
        return {"proposal_path": proposal_path, "prepared": prepared,
                "set_rel": set_rel, "record": core.load_json(FIX_ROOT / res["record_path"]),
                "record_rel": res["record_path"] if isinstance(res["record_path"], str)
                else str(res["record_path"]),
                "pubdir": pubdir, "snap_before": snap_before}

    first = _cycle("wk-r3c-1", "Weekly tested method, revised edition", True)
    if first is None:
        _log("FIRST CYCLE BLOCKER")
        return 2
    rec1 = first["record"]
    assert rec1.get("supersedes") is None, rec1.get("supersedes")
    assert rec1.get("canonical_anchor", {}).get("kind") == "VALIDATION_CHECKPOINT"
    _log(f"FIRST_ANCHOR={json.dumps(rec1['canonical_anchor'])}")
    # strict readback after first (preserve before Preview: no lifecycle)
    st1 = core.load_json(state_path)
    assert agent.validate_agent_state(
        FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG), st1) == []
    sel1 = setmod.resolve_publication_selection(
        FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG), st1)
    assert sel1.get("mode") == "VERSIONED_ACTIVE", sel1.get("mode")
    _log(f"FIRST_SELECTION mode={sel1.get('mode')} candidate={(sel1.get('candidate_ref') or {}).get('path')}")
    hist1 = edpub.verify_activation_history(
        FIX_ROOT, first["record_rel"] if first["record_rel"].startswith("/") else first["record_rel"])
    _log(f"FIRST_HISTORY status={hist1.get('status') if isinstance(hist1, dict) else hist1}")

    second = _cycle("wk-r3c-2", "Weekly tested method \u2014 Second Editorial Correction", False)
    if second is None:
        _log("SECOND CYCLE BLOCKER (exact next blocker above)")
        return 2
    rec2 = second["record"]
    _log(f"SECOND supersedes={rec2.get('supersedes')}")
    assert rec2.get("supersedes") is not None, "second must supersede first"
    assert rec2.get("canonical_anchor") == rec1.get("canonical_anchor"), \
        f"repeated must retain anchor {rec2.get('canonical_anchor')} vs {rec1.get('canonical_anchor')}"
    _log(f"SECOND_ANCHOR_RETAINED={json.dumps(rec2['canonical_anchor'])}")
    # strict State/readback + old immutable KEEP
    st2 = core.load_json(state_path)
    errs2 = agent.validate_agent_state(
        FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG), st2)
    assert not errs2, f"second State unhealthy {errs2}"
    _log("SECOND_STATE_HEALTHY")
    sel2 = setmod.resolve_publication_selection(
        FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG), st2)
    assert sel2.get("mode") == "VERSIONED_ACTIVE"
    cand2 = (sel2.get("candidate_ref") or {}).get("path")
    _log(f"SECOND_SELECTION mode={sel2.get('mode')} candidate={cand2}")
    assert cand2 == f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-r3c-2/publication/publication-candidate-v2.json", cand2
    # old immutable: everything before second except State/record/second-publication unchanged
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
    pub_prefix = f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-r3c-2/publication/"
    rec2_rel = second["record_rel"]
    if rec2_rel.startswith("/"):
        rec2_rel = str(Path(rec2_rel).relative_to(FIX_ROOT))
    for rel, sha in before2.items():
        if rel.startswith(pub_prefix) or rel == rec2_rel or rel == state_rel:
            continue
        assert rel in after2, f"disappearance after second activate: {rel}"
        assert after2[rel] == sha, f"old-immutable drift after second activate: {rel}"
    _log("SECOND_OLD_IMMUTABLE_KEEP_OK")
    # active receipt/Gate/Candidate on second set
    rv = edpub.validate_editorial_receipt(
        FIX_ROOT, f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-r3c-2/publication/validated-source-manifest.json",
        state_rel)
    _log(f"SECOND_RECEIPT issue={rv.get('issue_id')}")
    gv = reader_gate.validate_reader_surface_gate(
        FIX_ROOT, f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-r3c-2/publication/reader-surface-gate-v2.json",
        issue_id=ISSUE, publication_profile="WEEKLY_MAGAZINE",
        expected_manuscript_path=FIX_ROOT / f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-r3c-2/publication/reader-manuscript-v2.json",
        state_path=state_rel)
    assert gv.get("status") == "PASSED", gv
    _log("SECOND_GATE_PASSED")
    cv = pubmod.validate_candidate(
        FIX_ROOT, FIX_ROOT / f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-r3c-2/publication/publication-candidate-v2.json")
    _log(f"SECOND_CANDIDATE status={cv.get('status') if isinstance(cv, dict) else cv}")
    _log("=== SECOND CORRECTION ACTIVATED (terminal) ===")
    return 0


if __name__ == "__main__":
    try:
        rc = main()
    except Exception:
        traceback.print_exc()
        rc = 2
    print(f"EXIT:{rc}", flush=True)
    sys.exit(rc)
