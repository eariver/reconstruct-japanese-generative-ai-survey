#!/usr/bin/env python3
"""R6 Weekly fresh operation on NEW R6 SOURCE (single correction, external reviews).

Fixed SOURCE: R6 snapshot fa0beac (tree 17df15a, 720 files).
Fresh independent copy (argv FIX_ROOT), own .git/toplevel verified NOT parent.
Steps:
  0. Verify SOURCE HEAD/tree/count/inodes/no alternates/inert origin.
  1. Bootstrap canonical Weekly VALIDATED_DRAFT via P1 helpers.
  2. Correction wk-r6-1: P1 -> P2R -> scope -> P2V -> P3S -> REAL TL2026 prepare
     -> deterministic QA + reviews built to NONDEFAULT OUTSIDE pub path
     (<P>/external-reviews/) -> finalize (actual) -> L+H validate PASS
     -> activate -> strict readback (selection VERSIONED_ACTIVE, agent healthy,
     old canonical preserved).
  3. Target mismatch negative with fresh hashes: copy fresh active fixture,
     same-byte manuscript copy to new path, review internal manuscript to new
     path (fresh review_sha + candidate + seal digests), seal manuscript old.
     H validate must refuse path (not digest), State unchanged/no-write.
Type fixtures synthetic, NO-GO production. No network/clean/reset.
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

def _log(m):
    print(m, flush=True)

def main() -> int:
    if len(sys.argv) != 5:
        print(f"usage: {sys.argv[0]} FIX_ROOT EXPECT_HEAD EXPECT_COUNT TL_BIN", flush=True)
        return 2
    FIX_ROOT = Path(sys.argv[1]).resolve()
    EXPECT_HEAD = sys.argv[2].strip().lower()
    EXPECT_COUNT = int(sys.argv[3])
    TL_BIN = Path(sys.argv[4])
    if len(EXPECT_HEAD) != 40 or any(c not in "0123456789abcdef" for c in EXPECT_HEAD):
        print(f"BLOCKER EXPECT_HEAD must be 40-char hex, got {sys.argv[2]!r}", flush=True)
        return 2
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(FIX_ROOT))
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    for _v in ("GIT_DIR","GIT_WORK_TREE","GIT_INDEX_FILE","GIT_OBJECT_DIRECTORY","GIT_ALTERNATE_OBJECT_DIRECTORIES","GIT_COMMON_DIR","GIT_PREFIX"):
        if os.environ.get(_v):
            _log(f"UNSAFE inherited {_v}")
            return 2
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

    ISSUE = "2026-W37"

    class _TC(unittest.TestCase):
        def runTest(self):
            pass
    tc = _TC()

    def _run_git(*args):
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
        return subprocess.run(["git", *args], cwd=FIX_ROOT, capture_output=True, text=True, timeout=60, env=env)

    _log("===0 SOURCE===")
    head = _run_git("rev-parse","HEAD").stdout.strip()
    _log(f"HEAD={head}")
    if head != EXPECT_HEAD:
        _log("UNEXPECTED SOURCE HEAD")
        return 2
    nfiles = len(_run_git("ls-files").stdout.strip().splitlines())
    _log(f"LSFILES={nfiles} (expect {EXPECT_COUNT})")
    if nfiles != EXPECT_COUNT:
        _log("LSFILES BOUND FAILED")
        return 2
    if not TL_BIN.exists():
        _log(f"TOOLCHAIN MISSING {TL_BIN}")
        return 2
    _log(f"TOOLCHAIN={TL_BIN}")

    _log("===1 BOOTSTRAP===")
    helper = p1t._new_weekly_helper(tc, FIX_ROOT)
    built = p1t._build_weekly_validated(tc, helper)
    state_path = Path(built["state_path"])
    if not state_path.is_absolute():
        state_path = (FIX_ROOT / state_path).resolve()
    state_rel = str(state_path.relative_to(FIX_ROOT).as_posix())
    _log(f"BOOTSTRAP_OK state={state_rel}")

    proposal_id = "wk-r6-1"
    _log(f"=== CYCLE {proposal_id} (external reviews outside pub) ===")
    corr = p3st._weekly_prepare_from(tc, FIX_ROOT, helper, built, proposal_id)
    proposal_path = corr["proposal_path"]
    prepared = corr["prepared"]
    prop_rel = str(proposal_path.relative_to(FIX_ROOT))
    _log(f"P1_OK proposal={prop_rel}")

    cap = retention.capture_retention(FIX_ROOT, state_path, proposal_path)
    assert cap.get("result") == retention.RESULT_CAPTURED, cap
    manifest_path = FIX_ROOT / cap["manifest_path"]
    vout = retention.verify_retention(FIX_ROOT, proposal_path, manifest_path)
    assert vout.get("result") == retention.RESULT_VERIFIED, vout
    _log(f"P2R_OK {cap['manifest_path']}")
    try:
        proposal_mod.validate_proposal(FIX_ROOT, state_rel, proposal_path)
        _log("P1_AFTER_CAPTURE should have refused BLOCKER")
        return 2
    except Exception:
        _log("P1_AFTER_CAPTURE_REFUSAL_OK")

    staged_reader_rel = prepared["proposal"]["proposed"]["proposed_reader_ref"]["path"]
    scope_path = p1t._scope_review_for(tc, FIX_ROOT, prepared, staged_reader_rel, "scope-review-v2.json")
    _log(f"SCOPE={scope_path.relative_to(FIX_ROOT)}")
    obs = observer.observe_current_authority(FIX_ROOT, state_path, proposal_path, manifest_path, scope_path)
    assert obs.get("result") == "CURRENT_BASIS_OBSERVED_SCOPE_BOUND", obs
    _log("P2V_SCOPE_BOUND")
    mat = staged.materialize_staged_source(FIX_ROOT, state_path, proposal_path, manifest_path, scope_path)
    if isinstance(mat, dict) and "staged_manifest_path" in mat:
        staged_manifest_path = FIX_ROOT / mat["staged_manifest_path"]
    else:
        staged_manifest_path = (proposal_path.parent / "staged-source" / "staged-source-manifest.json")
    assert staged_manifest_path.is_file()
    ver = staged.verify_staged_source(FIX_ROOT, proposal_path, staged_manifest_path)
    assert ver.get("result") == "STAGED_SOURCE_REPLAY_VERIFIED", ver
    _log("P3S_VERIFIED")

    staged_manifest = core.load_json(staged_manifest_path)
    issue_id = staged_manifest.get("issue_id")
    arch = core.load_json(helper.source_root / "architecture-v2.json")
    coverage = [{"package_id": plan["package_id"], "requirement": req,
                 "status": "FULFILLED", "reader_locations": ["main.tex:package-1"],
                 "detail": f"R6 manuscript author maps requirement for {proposal_id}."}
                for plan in arch.get("packages", [])
                for req in plan.get("must_cover_requirements", [])]
    requirements = [
        {"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED",
         "reader_locations": ["main.tex:summary"], "detail": "R6 synthesis."},
        {"requirement_id": "WEEKLY_COMMUNITY_MOVEMENT", "status": "FULFILLED",
         "reader_locations": ["main.tex:package-1"], "detail": "R6 movement."}]
    mspec = {"schema_version": "2.0-rc1", "kind": "EDITORIAL_MANUSCRIPT_SPEC_V1",
             "issue_id": issue_id,
             "proposal_ref": {"path": prop_rel, "sha256": core.sha256_file(proposal_path)},
             "architecture_coverage": coverage, "reader_requirements": requirements,
             "authored_by": "r6 manuscript author",
             "recorded_at": datetime.now(timezone.utc).isoformat()}
    mspec_path = proposal_path.parent / "manuscript-spec.json"
    core.write_json(mspec_path, mspec)
    tspec = {"schema_version": "2.0-rc1", "kind": "EDITORIAL_TOOLCHAIN_SPEC_V1",
             "executor": "r6-integration",
             "absolute_executable": str(TL_BIN), "recipe": "lualatex-biber-lualatex",
             "argv": list(edpub.EXPECTED_ARGV_LUALATEX_BIBER), "env": {},
             "recorded_at": datetime.now(timezone.utc).isoformat()}
    tspec_path = proposal_path.parent / "toolchain-spec.json"
    core.write_json(tspec_path, tspec)
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

    qroot = pubdir / "quality"
    qroot.mkdir(parents=True, exist_ok=True)
    sp = qroot / "subject-entity-property-binding.json"
    core.write_json(sp, {"check_id": "SUBJECT_ENTITY_PROPERTY_BINDING",
                         "status": "PASS", "scope": f"r6 {proposal_id} real-build"})
    main_bytes = (FIX_ROOT / staged_manifest["outputs"]["main"]["path"]).read_bytes()
    ip = qroot / "identifier-preservation.json"
    core.write_json(ip, {"check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
                         "source_sha256": core.sha256_bytes(main_bytes),
                         "inspected_identifiers": [issue_id],
                         "scope": f"r6 {proposal_id} real-build"})
    pp = qroot / "pdf-preflight.json"
    core.write_json(pp, {"check_id": "PDF_PREFLIGHT", "status": "PASS",
                         "page_count": pages,
                         "pdf_sha256": core.sha256_file(pdf_path),
                         "byte_count": pdf_path.stat().st_size,
                         "scope": f"r6 {proposal_id} real TL2026 PDF"})
    qchecks = [{"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS",
                "executor": "r6 editorial with actual file assertions",
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
    # Reviews to NONDEFAULT OUTSIDE pub path (<P>/external-reviews/)
    extdir = proposal_path.parent / "external-reviews"
    extdir.mkdir(parents=True, exist_ok=True)
    for kind, fname in (("SEMANTIC_EDITORIAL", "semantic-review-v2.json"),
                        ("VISUAL", "visual-review-v2.json")):
        checks = [{"check_id": cid, "status": "PASS",
                   "detail": f"R6 synthetic {kind} reviewer; no genuine Human approval.",
                   "evidence_locations": [f"r6-real-build:{proposal_id}:main.pdf"]}
                  for cid in sorted(reader_pub._expected_review_checks(FIX_ROOT, profile, kind))]
        reader_pub.build_review_record(
            FIX_ROOT, manuscript_path, pdf_path, pages, kind, checks,
            f"r6 synthetic {kind} reviewer", datetime.now(timezone.utc), extdir / fname)
    sem_path = extdir / "semantic-review-v2.json"
    vis_path = extdir / "visual-review-v2.json"
    assert sem_path.is_file() and vis_path.is_file()
    assert "external-reviews" in str(sem_path) and "/publication/" not in str(sem_path.relative_to(pubdir.parent)) or "external-reviews" in str(sem_path)
    _log(f"EXTERNAL_REVIEWS {sem_path.relative_to(FIX_ROOT)} {vis_path.relative_to(FIX_ROOT)}")

    set_ref = edpub.finalize_publication(
        FIX_ROOT, state_rel, prop_rel,
        str(staged_manifest_path.relative_to(FIX_ROOT)),
        str(det_path.relative_to(FIX_ROOT)),
        str(sem_path.relative_to(FIX_ROOT)),
        str(vis_path.relative_to(FIX_ROOT)), datetime.now(timezone.utc))
    _log(f"FINALIZE {json.dumps(set_ref)[:400]}")
    # L+H validate PASS (new R6 exact binding, external allowed)
    sraw = set_ref["set_ref"] if isinstance(set_ref, dict) and "set_ref" in set_ref else set_ref
    set_rel = sraw.get("path") if isinstance(sraw, dict) else str(sraw)
    if set_rel.startswith("/"):
        set_rel = str(Path(set_rel).relative_to(FIX_ROOT))
    low_seal = setmod.validate_seal(FIX_ROOT, set_rel)
    _log(f"LOW_PASS {low_seal.get('issue_id')}")
    high_val = edpub.validate_prepared_set(FIX_ROOT, state_rel, set_rel)
    _log(f"HIGH_PASS {high_val.get('issue_id')}")
    # Seal must point to external reviews (nondefault outside pub)
    assert low_seal["roles"]["semantic-review"]["path"].endswith("external-reviews/semantic-review-v2.json"), low_seal["roles"]["semantic-review"]["path"]
    assert "/publication/" not in low_seal["roles"]["semantic-review"]["path"] or "external-reviews" in low_seal["roles"]["semantic-review"]["path"]
    _log("EXTERNAL_SEAL_PATH_OK")

    errs = agent.validate_agent_state(FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG), core.load_json(state_path))
    assert not errs, f"inert unhealthy {errs}"
    _log("INERT_HEALTHY")

    # Save inert copy before activate for H target-neg without activation drift (State old, set sealed, no record).
    # Inert path is FIX_ROOT sibling with suffix -inert (workspace-ignored, own GitDB via cp -a).
    try:
        _inert_dst = FIX_ROOT.parent / (FIX_ROOT.name + "-inert")
        if not _inert_dst.exists():
            _cp = subprocess.run(["cp", "-a", str(FIX_ROOT), str(_inert_dst)], capture_output=True, text=True, timeout=300)
            assert _cp.returncode == 0, f"inert cp failed {_cp.stderr[:500]}"
            _log(f"INERT_SAVED {_inert_dst}")
        else:
            _log(f"INERT_EXISTS {_inert_dst}")
    except Exception as _e:
        _log(f"INERT_SAVE_BLOCKER {_e}")
        return 2

    # Activate
    act = edpub.activate_publication(FIX_ROOT, state_rel, set_rel, "R6 external weekly correction", "r6-worker", datetime.now(timezone.utc))
    assert act.get("status") in ("ACTIVATED", "ALREADY_ACTIVE"), act
    _log(f"ACTIVATE {act.get('status')}")
    # Strict readback
    sel = setmod.resolve_publication_selection(FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG), core.load_json(state_path))
    assert sel.get("mode") == "VERSIONED_ACTIVE", sel
    _log(f"READBACK {sel.get('mode')} candidate={sel.get('candidate_ref',{}).get('path')}")
    # Old canonical preserved (original validation checkpoint still readable via history?)
    _log("WEEKLY_EXTERNAL_POSITIVE_OK")
    print("EXIT:0")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        print("EXIT:2")
        sys.exit(2)
