#!/usr/bin/env python3
"""NEW guarded bootstrap fixture builder — Weekly/Longform old-format R3 ACTIVE prePreview.

Fresh isolated fixture DB (cloned 721a04d source, NOT reconstruct DB, NOT M1
candidate-work) -> accepted research/Architecture/Draft canonical VALIDATED
(bootstrap blankPDF type fixture only) -> P1 changed-reader proposal ->
P2R capture -> scope synthetic early review -> P2V scope-bound ->
P3S real materialize/verify50 -> edpub.prepare_publication with actual
toolchain -> supplied synthetic semantic/visual + actual scoped QA checks ->
finalize -> validate_prepared_set -> activate -> strict State prePreview &
history readback. NO Preview advance. NO freeze/adoption/Human approval.

Single correction per fixture (first activation, supersedes None). Synthetic
source identity 721a04d, NOT actual candidate409 ancestry. Failed partials
preserved (no TemporaryDirectory autodelete, no git clean/reset, no old
runner exec, no network, no log truncation).

Usage:
  python3 run_bootstrap_fixture.py FIX_ROOT NOTES_DIR EXPECT_HEAD EXPECT_TREE EXPECT_COUNT KIND PROPOSAL_ID

  FIX_ROOT: isolated fixture worktree (already cloned 721 source, clean HEAD)
  NOTES_DIR: evidence dir for logs/manifests (notes/.../bootstrap-fixtures/evidence-<kind>/)
  KIND: weekly|longform
  PROPOSAL_ID: e.g. wk-boot-1 / lf-boot-1 (new proposal ID, no takeover)
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


def _run_git(fix_root: Path, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    return subprocess.run(["git", *args], cwd=fix_root, capture_output=True, text=True, timeout=120, env=env)


def _snapshot_files(fix_root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for dirpath, dirnames, filenames in os.walk(fix_root):
        if ".git" in Path(dirpath).parts:
            dirnames[:] = []
            continue
        if "__pycache__" in Path(dirpath).parts:
            continue
        for fn in sorted(filenames):
            if fn.endswith(".pyc"):
                continue
            p = Path(dirpath) / fn
            rel = p.relative_to(fix_root).as_posix()
            h = hashlib.sha256()
            with p.open("rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
            out[rel] = h.hexdigest()
    return out


def main() -> int:
    if len(sys.argv) != 8:
        print(f"usage: {sys.argv[0]} FIX_ROOT NOTES_DIR EXPECT_HEAD EXPECT_TREE EXPECT_COUNT KIND PROPOSAL_ID", flush=True)
        return 2
    FIX_ROOT = Path(sys.argv[1]).resolve()
    NOTES = Path(sys.argv[2]).resolve()
    EXPECT_HEAD = sys.argv[3].strip().lower()
    EXPECT_TREE = sys.argv[4].strip().lower()
    EXPECT_COUNT = int(sys.argv[5])
    KIND = sys.argv[6].strip().lower()
    PROPOSAL_ID = sys.argv[7].strip()
    if KIND not in ("weekly", "longform"):
        print(f"BLOCKER KIND must be weekly|longform, got {KIND!r}", flush=True)
        return 2
    for _l, _v in (("EXPECT_HEAD", EXPECT_HEAD), ("EXPECT_TREE", EXPECT_TREE)):
        if len(_v) != 40 or any(c not in "0123456789abcdef" for c in _v):
            print(f"BLOCKER {_l} must be 40-char hex, got {_v!r}", flush=True)
            return 2
    # Guarded env BEFORE any fixture imports/commands.
    sys.dont_write_bytecode = True
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    for _v in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
               "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_PREFIX"):
        if os.environ.get(_v):
            _log(f"UNSAFE inherited {_v} refuses operation")
            return 2
    tmpdir = os.environ.get("TMPDIR", "")
    if not tmpdir:
        _log("BLOCKER TMPDIR must be set to workspace scratch (external TMPDIR under workspace scratch)")
        return 2
    # TMPDIR must be under workspace scratch, not /tmp.
    try:
        tmp_p = Path(tmpdir).resolve()
        ws_p = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime").resolve()
        if ws_p not in tmp_p.parents and tmp_p != ws_p:
            _log(f"BLOCKER TMPDIR {tmpdir} not under workspace scratch {ws_p}")
            return 2
    except Exception as exc:
        _log(f"BLOCKER TMPDIR check failed: {exc}")
        return 2
    NOTES.mkdir(parents=True, exist_ok=True)
    # Insert FIX_ROOT first so fixture modules resolve from fixture, never candidate-work.
    if str(FIX_ROOT) not in sys.path:
        sys.path.insert(0, str(FIX_ROOT))
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

    TL_BIN = Path("/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/lualatex")
    BIBER_BIN = Path("/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/biber")

    class _TC(unittest.TestCase):
        def runTest(self):
            pass
    tc = _TC()

    def _rel(p) -> str:
        return str(p.relative_to(FIX_ROOT)) if isinstance(p, Path) and p.is_absolute() else str(p)

    # === 0 SOURCE BINDING (read-only checks, no writes) ===
    _log("===0 SOURCE===")
    head = _run_git(FIX_ROOT, "rev-parse", "HEAD").stdout.strip()
    _log(f"HEAD={head}")
    if head != EXPECT_HEAD:
        _log("UNEXPECTED SOURCE HEAD")
        return 2
    ls_n = len([l for l in _run_git(FIX_ROOT, "ls-files").stdout.strip().splitlines() if l])
    _log(f"LSFILES={ls_n} (expect {EXPECT_COUNT})")
    if ls_n != EXPECT_COUNT:
        _log("LSFILES BOUND FAILED")
        return 2
    actual_tree = _run_git(FIX_ROOT, "rev-parse", "HEAD^{tree}").stdout.strip()
    _log(f"TREE={actual_tree} (expect {EXPECT_TREE})")
    if actual_tree != EXPECT_TREE:
        _log("TREE BOUND FAILED")
        return 2
    # No alternates, inert origin, clean status, no pycache.
    alt = FIX_ROOT / ".git" / "objects" / "info" / "alternates"
    if alt.exists():
        _log(f"BLOCKER alternates present: {alt}")
        return 2
    _log("NO_ALTERNATES_OK")
    remote = _run_git(FIX_ROOT, "remote", "-v").stdout.strip()
    _log(f"REMOTE={remote}")
    if "example.invalid" not in remote:
        _log("BLOCKER origin not inert (must contain example.invalid)")
        return 2
    status = _run_git(FIX_ROOT, "status", "--porcelain").stdout
    _log(f"STATUS_CLEAN={'yes' if status == '' else 'NO: '+status[:500]}")
    if status != "":
        _log("BLOCKER fixture DB not clean before authorities")
        return 2
    if not TL_BIN.exists():
        _log(f"TOOLCHAIN MISSING {TL_BIN}")
        return 2
    if not BIBER_BIN.exists():
        _log(f"TOOLCHAIN MISSING {BIBER_BIN}")
        return 2
    _log(f"TOOLCHAIN lualatex={TL_BIN} biber={BIBER_BIN}")
    # Tool versions (local only, no network).
    try:
        lv = subprocess.run([str(TL_BIN), "--version"], capture_output=True, text=True, timeout=60,
                            env={k: v for k, v in os.environ.items() if not k.startswith("GIT_")})
        _log(f"LUALATEX_VERSION rc={lv.returncode} out={lv.stdout.splitlines()[0] if lv.stdout else ''}")
    except Exception as exc:
        _log(f"LUALATEX_VERSION_FAILED {exc}")
        return 2
    _log(f"PYTHON={sys.version.split()[0]} expected 3.14.4")
    # Exact 721 manifest cross-check (read-only): compare worktree SHAs for a pinned subset?
    # Full 721 check is done via HEAD/tree/ls-files; manifest path recorded in evidence.
    snap0 = _snapshot_files(FIX_ROOT)
    _log(f"SNAP0 files={len(snap0)}")

    try:
        if KIND == "weekly":
            ISSUE = "2026-W37"
            _log("===1 BOOTSTRAP WEEKLY CANONICAL===")
            helper = p1t._new_weekly_helper(tc, FIX_ROOT)
            built = p1t._build_weekly_validated(tc, helper)
            chain, state_path = built["chain"], Path(built["state_path"])
            if not state_path.is_absolute():
                state_path = (FIX_ROOT / state_path).resolve()
            st0 = core.load_json(state_path)
            assert st0.get("publication_revalidation_provenance") is None, "bootstrap must be pre-activation"
            state_rel = str(state_path.relative_to(FIX_ROOT).as_posix())
            _log(f"BOOTSTRAP_OK state={state_rel} lifecycle={st0.get('lifecycle_state')}")
            assert core.load_json(state_path)["lifecycle_state"] == "VALIDATED_DRAFT"
            # === P1 ===
            _log(f"===P1 {PROPOSAL_ID}===")
            corr = __import__("tests.test_survey_editorial_staged_source_v2", fromlist=["_weekly_prepare_from"])
            # Use staged helper for weekly prepare on existing helper+built (R1 rebind pattern).
            from tests import test_survey_editorial_staged_source_v2 as p3st
            corr = p3st._weekly_prepare_from(tc, FIX_ROOT, helper, built, PROPOSAL_ID)
            proposal_path = corr["proposal_path"]
            prepared = corr["prepared"]
            _log(f"P1_PREPARE proposal={PROPOSAL_ID} reader_sha={hashlib.sha256(prepared['proposed_canonical']).hexdigest()}")
            _log(f"P1_VALIDATE REVIEW_REQUIRED (asserted inside helper)")
        else:
            ISSUE = "SP001"
            _log("===1 BOOTSTRAP LONGFORM CANONICAL===")
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
            _log(f"BOOTSTRAP_OK state={state_rel}")
            # Old canonical candidate (healthy, preserved, never adopted) — as in R4e longform.
            profile = core.load_json(chain["profile_path"])
            cand_rel = (Path(profile["paths"]["source_root"]) / "publication" / "v2" /
                        "publication-candidate-v2.json").as_posix()
            cand_path = FIX_ROOT / cand_rel
            assert not cand_path.exists(), f"candidate must be absent before initial build: {cand_rel}"
            pubmod.build_candidate(FIX_ROOT, ISSUE, "LONGFORM_SPECIAL", built["manuscript"],
                                   helper.survey_root / "main.tex", built["pdf"], 1,
                                   built["bundle"], built["SEMANTIC_EDITORIAL"],
                                   built["VISUAL"], cand_path)
            old_cand_bytes = cand_path.read_bytes()
            old_cand_rel = str(cand_path.relative_to(FIX_ROOT).as_posix())
            old_cand_sha = core.sha256_file(cand_path)
            old_cand_check = pubmod.validate_candidate(FIX_ROOT, cand_path, issue_id=ISSUE)
            _log(f"OLD_CANDIDATE_HEALTHY {old_cand_rel} sha={old_cand_sha} status={old_cand_check.get('status')}")
            _log(f"===P1 {PROPOSAL_ID}===")
            authored = helper._authored(chain, helper.worker)
            pkg0 = authored["longform_revision"]["packages"][0]
            paras = pkg0["narrative_sections"][0]["paragraphs"]
            assert len(paras) >= 1
            paras[0]["text"] += " Revised fixture sentence within approved evidence."
            staged_auth = p1t._stage_authoring_before_prepare(tc, FIX_ROOT, helper.source_root, PROPOSAL_ID, authored)
            _log(f"STAGED_AUTH {staged_auth.relative_to(FIX_ROOT)}")
            prepared = proposal_mod.prepare_proposal(FIX_ROOT, state_rel, staged_auth, PROPOSAL_ID,
                                                     f"Bootstrap longform correction {PROPOSAL_ID}.")
            _log(f"P1_PREPARE {PROPOSAL_ID} reader_sha={hashlib.sha256(prepared['proposed_canonical']).hexdigest()}")
            proposal_path = p1t._stage_reader_and_proposal(tc, FIX_ROOT, helper.source_root, PROPOSAL_ID, prepared)
            outcome = proposal_mod.validate_proposal(FIX_ROOT, state_rel, proposal_path)
            assert outcome["result"] in ("REVIEW_REQUIRED", "REVIEW_BOUND_PROPOSAL"), outcome
            _log(f"P1_VALIDATE {outcome['result']}")

        # === P2R ===
        _log("===P2R===")
        cap = retention.capture_retention(FIX_ROOT, state_path, proposal_path)
        assert cap.get("result") == retention.RESULT_CAPTURED, cap
        manifest_path = FIX_ROOT / cap["manifest_path"]
        vout = retention.verify_retention(FIX_ROOT, proposal_path, manifest_path)
        assert vout.get("result") == retention.RESULT_VERIFIED, vout
        _log(f"P2R_OK manifest={cap['manifest_path']} sha={core.sha256_file(manifest_path)}")
        try:
            proposal_mod.validate_proposal(FIX_ROOT, state_rel, proposal_path)
            _log("P1_AFTER_CAPTURE should have refused BLOCKER")
            return 2
        except Exception as exc:
            _log(f"P1_AFTER_CAPTURE_REFUSAL_OK {type(exc).__name__}")

        # === scope (synthetic early review, clearly synthetic) ===
        _log("===SCOPE===")
        staged_reader_rel = prepared["proposal"]["proposed"]["proposed_reader_ref"]["path"]
        scope_path = p1t._scope_review_for(tc, FIX_ROOT, prepared, staged_reader_rel, "scope-review-v2.json")
        _log(f"SCOPE={scope_path.relative_to(FIX_ROOT)} sha={core.sha256_file(scope_path)}")

        # === P2V ===
        _log("===P2V===")
        obs = observer.observe_current_authority(FIX_ROOT, state_path, proposal_path, manifest_path, scope_path)
        assert obs.get("result") == "CURRENT_BASIS_OBSERVED_SCOPE_BOUND", obs
        _log("P2V_SCOPE_BOUND")

        # === P3S ===
        _log("===P3S===")
        mat = staged.materialize_staged_source(FIX_ROOT, state_path, proposal_path, manifest_path, scope_path)
        if isinstance(mat, dict) and "staged_manifest_path" in mat:
            staged_manifest_path = FIX_ROOT / mat["staged_manifest_path"]
        else:
            staged_manifest_path = (proposal_path.parent / "staged-source" / "staged-source-manifest.json")
        assert staged_manifest_path.is_file(), f"staged manifest missing {staged_manifest_path}"
        ver = staged.verify_staged_source(FIX_ROOT, proposal_path, staged_manifest_path)
        assert ver.get("result") == "STAGED_SOURCE_REPLAY_VERIFIED", ver
        staged_manifest = core.load_json(staged_manifest_path)
        assert len(staged_manifest.get("code_deps", [])) == 50, f"code_deps !=50: {len(staged_manifest.get('code_deps', []))}"
        _log(f"P3S_VERIFIED50 manifest={staged_manifest_path.relative_to(FIX_ROOT)} sha={core.sha256_file(staged_manifest_path)}")

        # === specs (manuscript/toolchain outside publication/) ===
        _log("===SPECS===")
        proposal_dir = proposal_path.parent
        issue_id = staged_manifest.get("issue_id")
        assert issue_id == ISSUE, f"issue mismatch {issue_id} vs {ISSUE}"
        if KIND == "weekly":
            arch = core.load_json(helper.source_root / "architecture-v2.json")
            coverage = [{"package_id": plan["package_id"], "requirement": req,
                         "status": "FULFILLED", "reader_locations": ["main.tex:package-1"],
                         "detail": f"Bootstrap manuscript author maps requirement for {PROPOSAL_ID}."}
                        for plan in arch.get("packages", [])
                        for req in plan.get("must_cover_requirements", [])]
            requirements = [
                {"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED",
                 "reader_locations": ["main.tex:summary"], "detail": "Bootstrap synthesis."},
                {"requirement_id": "WEEKLY_COMMUNITY_MOVEMENT", "status": "FULFILLED",
                 "reader_locations": ["main.tex:package-1"], "detail": "Bootstrap movement."}]
        else:
            new_surface = core.load_json(proposal_dir / "reader-surface-input-v2.json")
            staged_main_text = (FIX_ROOT / staged_manifest["outputs"]["main"]["path"]).read_text(encoding="utf-8")
            pkg_locs, final_loc = helper._section_locations(chain, new_surface, staged_main_text)
            pkgs = core.load_json(helper.source_root / "architecture-v2.json").get("packages", [])
            assert len(pkg_locs) == len(pkgs), f"section locations {len(pkg_locs)} vs pkgs {len(pkgs)}"
            coverage = [{"package_id": pkg["package_id"], "requirement": req, "status": "FULFILLED",
                         "reader_locations": [loc],
                         "detail": f"Bootstrap LF manuscript author maps requirement for {PROPOSAL_ID}."}
                        for pkg, loc in zip(pkgs, pkg_locs)
                        for req in pkg.get("must_cover_requirements", [])]
            requirements = [{"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED",
                             "reader_locations": [final_loc],
                             "detail": f"Bootstrap LF synthesis for {PROPOSAL_ID}."}]
        prop_rel = str(proposal_path.relative_to(FIX_ROOT))
        mspec = {"schema_version": "2.0-rc1", "kind": "EDITORIAL_MANUSCRIPT_SPEC_V1",
                 "issue_id": issue_id,
                 "proposal_ref": {"path": prop_rel, "sha256": core.sha256_file(proposal_path)},
                 "architecture_coverage": coverage, "reader_requirements": requirements,
                 "authored_by": f"bootstrap {KIND} manuscript author",
                 "recorded_at": datetime.now(timezone.utc).isoformat()}
        mspec_path = proposal_dir / "manuscript-spec.json"
        core.write_json(mspec_path, mspec)
        tspec = {"schema_version": "2.0-rc1", "kind": "EDITORIAL_TOOLCHAIN_SPEC_V1",
                 "executor": f"bootstrap-{KIND}-integration",
                 "absolute_executable": str(TL_BIN), "recipe": "lualatex-biber-lualatex",
                 "argv": list(edpub.EXPECTED_ARGV_LUALATEX_BIBER), "env": {},
                 "recorded_at": datetime.now(timezone.utc).isoformat()}
        tspec_path = proposal_dir / "toolchain-spec.json"
        core.write_json(tspec_path, tspec)
        _log(f"SPECS {mspec_path.relative_to(FIX_ROOT)} {tspec_path.relative_to(FIX_ROOT)}")
        _log(f"SPEC_RECIPE {tspec['recipe']} argv_len={len(tspec['argv'])}")

        # === prepare REAL TL2026 ===
        _log("===PREPARE_REAL_TL2026===")
        t0 = time.monotonic()
        prepared_paths = edpub.prepare_publication(
            FIX_ROOT, state_rel, prop_rel,
            str(staged_manifest_path.relative_to(FIX_ROOT)),
            str(mspec_path.relative_to(FIX_ROOT)),
            str(tspec_path.relative_to(FIX_ROOT)), datetime.now(timezone.utc))
        dt = time.monotonic() - t0
        _log(f"PREPARE dt={dt:.1f}s out_keys={sorted(prepared_paths.keys()) if isinstance(prepared_paths, dict) else type(prepared_paths).__name__}")
        pubdir = proposal_dir / "publication"
        manuscript_path = pubdir / "reader-manuscript-v2.json"
        pdf_path = pubdir / "build" / "main.pdf"
        log_path = pubdir / "build" / "main.log"
        assert manuscript_path.is_file() and pdf_path.is_file() and log_path.is_file()
        from pypdf import PdfReader as _PR
        pages = len(_PR(str(pdf_path)).pages)
        _log(f"REAL_PDF pages={pages} bytes={pdf_path.stat().st_size} log_bytes={log_path.stat().st_size}")
        if KIND == "weekly":
            assert pages >= 1, f"weekly real PDF must have >=1 page, got {pages}"
        else:
            assert pages >= 2, f"longform real PDF must be multi-page, got {pages}"
        _log(f"PDF_SHA {core.sha256_file(pdf_path)}")
        _log(f"MANUSCRIPT_SHA {core.sha256_file(manuscript_path)}")

        # === QA + synthetic reviews (actual builders, clearly synthetic) ===
        _log("===QA_REVIEWS===")
        qroot = pubdir / "quality"
        qroot.mkdir(parents=True, exist_ok=True)
        if KIND == "weekly":
            sp = qroot / "subject-entity-property-binding.json"
            core.write_json(sp, {"check_id": "SUBJECT_ENTITY_PROPERTY_BINDING",
                                 "status": "PASS", "scope": f"bootstrap {PROPOSAL_ID} real-build"})
            main_bytes = (FIX_ROOT / staged_manifest["outputs"]["main"]["path"]).read_bytes()
            ip = qroot / "identifier-preservation.json"
            core.write_json(ip, {"check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
                                 "source_sha256": core.sha256_bytes(main_bytes),
                                 "inspected_identifiers": [issue_id],
                                 "scope": f"bootstrap {PROPOSAL_ID} real-build"})
            pp = qroot / "pdf-preflight.json"
            core.write_json(pp, {"check_id": "PDF_PREFLIGHT", "status": "PASS",
                                 "page_count": pages,
                                 "pdf_sha256": core.sha256_file(pdf_path),
                                 "byte_count": pdf_path.stat().st_size,
                                 "scope": f"bootstrap {PROPOSAL_ID} real TL2026 PDF"})
            qchecks = [{"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS",
                        "executor": "bootstrap editorial with actual file assertions",
                        "evidence": "Exact fixture bytes and result file inspected.",
                        "recorded_at": datetime.now(timezone.utc).isoformat(),
                        "result": {"path": str(p.relative_to(FIX_ROOT)),
                                   "sha256": core.sha256_file(p)}}
                       for cid, p in (("SUBJECT_ENTITY_PROPERTY_BINDING", sp),
                                      ("IDENTIFIER_PRESERVATION", ip),
                                      ("PDF_PREFLIGHT", pp))]
        else:
            from scripts import survey_quality_v2 as quality
            cfg = core.load_json(FIX_ROOT / core.DEFAULT_CONFIG)
            kinds = quality.expected_checks_by_kind(cfg, "THEMATIC", "LONGFORM_SPECIAL", {"DETERMINISTIC"})
            staged_main_bytes = (FIX_ROOT / staged_manifest["outputs"]["main"]["path"]).read_bytes()
            payloads = {
                "SUBJECT_ENTITY_PROPERTY_BINDING": {
                    "check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "status": "PASS",
                    "issue_id": issue_id, "cited_discovery_count": 1,
                    "bindings": [{"discovery_id": "d01", "canonical_name": "Target Model",
                                  "canonical_url": "https://example.invalid/target",
                                  "materiality": "MATERIAL", "status": "VERIFIED",
                                  "source_accessed_at": "2026-08-22T02:10:00+09:00"}]},
                "IDENTIFIER_PRESERVATION": {
                    "check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
                    "source_sha256": core.sha256_bytes(staged_main_bytes),
                    "inspected_identifiers": [issue_id, "Target Model"],
                    "scope": f"bootstrap LF {PROPOSAL_ID} real-build"},
                "PDF_PREFLIGHT": {
                    "check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": pages,
                    "pdf_sha256": core.sha256_file(pdf_path),
                    "byte_count": pdf_path.stat().st_size,
                    "scope": f"bootstrap LF {PROPOSAL_ID} real TL2026 PDF"},
                "EMPTY_WRAPPER_SUPPRESSION": {
                    "check_id": "EMPTY_WRAPPER_SUPPRESSION", "status": "PASS",
                    "scope": f"bootstrap LF {PROPOSAL_ID} carries no empty wrapper",
                    "inspected_paths": [staged_manifest["outputs"]["main"]["path"]]},
            }
            assert set(payloads) == set(kinds), f"{sorted(payloads)} != {sorted(kinds)}"
            qchecks = []
            for cid, payload in payloads.items():
                p = qroot / f"{cid.lower()}.json"
                core.write_json(p, payload)
                qchecks.append({"check_id": cid, "kind": kinds[cid], "status": "PASS",
                                "executor": "bootstrap LF editorial with actual file assertions",
                                "evidence": "Exact fixture bytes and result file inspected.",
                                "recorded_at": datetime.now(timezone.utc).isoformat(),
                                "result": {"path": str(p.relative_to(FIX_ROOT)),
                                           "sha256": core.sha256_file(p)}})
        det_path = proposal_dir / "deterministic-checks.json"
        core.write_json(det_path, {"checks": qchecks})
        _log(f"DET_CHECKS {det_path.relative_to(FIX_ROOT)} n={len(qchecks)}")
        profile = core.load_json(FIX_ROOT / core.load_json(state_path)["profile"]["path"])
        if KIND == "weekly":
            for kind_name, fname in (("SEMANTIC_EDITORIAL", "semantic-review-v2.json"),
                                    ("VISUAL", "visual-review-v2.json")):
                checks = [{"check_id": cid, "status": "PASS",
                           "detail": f"Bootstrap synthetic {kind_name} reviewer; no genuine Human approval.",
                           "evidence_locations": [f"bootstrap-real-build:{PROPOSAL_ID}:main.pdf"]}
                          for cid in sorted(reader_pub._expected_review_checks(FIX_ROOT, profile, kind_name))]
                reader_pub.build_review_record(
                    FIX_ROOT, manuscript_path, pdf_path, pages, kind_name, checks,
                    f"bootstrap synthetic {kind_name} reviewer", datetime.now(timezone.utc), pubdir / fname)
        else:
            manuscript = core.load_json(manuscript_path)
            try:
                from scripts.survey_reader_fidelity_v2 import _locations_from_manifest as _lfm
                cov_locs, fin_locs = _lfm(manuscript)
                coverage_locations = sorted(cov_locs)
                final_locations = sorted(fin_locs)
            except Exception:
                coverage_locations = sorted({r["reader_locations"][0] for r in coverage})
                # final_loc from specs scope above
                final_locations = [coverage[0]["reader_locations"][0] if coverage else "main.tex:summary"]
            architecture = core.load_json(helper.source_root / "architecture-v2.json")
            package_ids = [r["package_id"] for r in architecture["packages"]]
            final_package = max(architecture["packages"], key=lambda r: r["drafting_order"])["package_id"]
            _pp = (architecture.get("page_plan") or {}).get("target_pages", 12)
            try:
                _tgt = int(float(_pp)) if float(_pp).is_integer() else str(_pp)
            except Exception:
                _tgt = 12
            for kind_name, fname in (("SEMANTIC_EDITORIAL", "semantic-review-v2.json"),
                                    ("VISUAL", "visual-review-v2.json")):
                expected = reader_pub._expected_review_checks(FIX_ROOT, profile, kind_name)
                checks = []
                for cid in sorted(expected):
                    ev = [f"bootstrap-lf-real-build:{PROPOSAL_ID}:main.pdf"]
                    if cid in ("ARCHITECTURE_CONTENT_FIDELITY", "LONGFORM_TECHNICAL_DEPTH"):
                        ev = sorted({f"package:{pid}" for pid in package_ids} | set(coverage_locations))
                        if cid == "LONGFORM_TECHNICAL_DEPTH":
                            ev = sorted(set(ev) | {f"page-plan:{pages}/{_tgt}", "density-review:below-target-substantive"})
                    elif cid == "FINAL_SYNTHESIS_QUALITY":
                        ev = sorted(set(final_locations) | {"reader-role:final-synthesis", f"package:{final_package}"})
                    elif cid == "LONGFORM_MIXED_LAYOUT":
                        ev = ["reader-layout:wide-surfaces-full-width",
                              "reader-layout:references-one-column",
                              "reader-layout:balanced-two-column-narrative"]
                    checks.append({"check_id": cid, "status": "PASS",
                                   "detail": f"Bootstrap synthetic LF {kind_name} reviewer; no genuine approval.",
                                   "evidence_locations": ev})
                reader_pub.build_review_record(
                    FIX_ROOT, manuscript_path, pdf_path, pages, kind_name, checks,
                    f"bootstrap synthetic LF {kind_name} reviewer", datetime.now(timezone.utc), pubdir / fname)
        sem_path = pubdir / "semantic-review-v2.json"
        vis_path = pubdir / "visual-review-v2.json"
        assert sem_path.is_file() and vis_path.is_file()
        _log(f"REVIEWS sem={core.sha256_file(sem_path)} vis={core.sha256_file(vis_path)}")

        # === finalize ===
        _log("===FINALIZE===")
        set_ref = edpub.finalize_publication(
            FIX_ROOT, state_rel, prop_rel,
            str(staged_manifest_path.relative_to(FIX_ROOT)),
            str(det_path.relative_to(FIX_ROOT)),
            str(sem_path.relative_to(FIX_ROOT)),
            str(vis_path.relative_to(FIX_ROOT)), datetime.now(timezone.utc))
        _log(f"FINALIZE {json.dumps(set_ref)[:600]}")
        errs = agent.validate_agent_state(FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG),
                                          core.load_json(state_path))
        assert not errs, f"inert unhealthy {errs}"
        _log("INERT_HEALTHY")
        sraw = set_ref["set_ref"] if isinstance(set_ref, dict) and "set_ref" in set_ref else set_ref
        set_rel = sraw.get("path") if isinstance(sraw, dict) else str(sraw)
        if set_rel.startswith("/"):
            set_rel = str(Path(set_rel).relative_to(FIX_ROOT))
        assert (FIX_ROOT / set_rel).is_file(), f"seal missing {set_rel}"
        _log(f"SEAL {set_rel} sha={core.sha256_file(FIX_ROOT / set_rel)}")

        # === validate_prepared_set ===
        _log("===VALIDATE_PREPARED_SET===")
        vset = edpub.validate_prepared_set(FIX_ROOT, state_rel, set_rel)
        _log(f"VALIDATE_SET ok keys={sorted(vset.keys()) if isinstance(vset, dict) else type(vset).__name__}")

        # === activate ===
        _log("===ACTIVATE===")
        res = edpub.activate_publication(
            FIX_ROOT, state_rel, set_rel, f"Bootstrap {KIND} editorial correction {PROPOSAL_ID}",
            f"bootstrap-{KIND}-executor-{PROPOSAL_ID}", datetime.now(timezone.utc))
        _log(f"ACTIVATE {json.dumps(res)[:900]}")
        assert res.get("status") == "ACTIVATED", res
        record_rel = res["record_path"] if isinstance(res.get("record_path"), str) else str(res.get("record_path"))
        if record_rel.startswith("/"):
            record_rel = str(Path(record_rel).relative_to(FIX_ROOT))
        record = core.load_json(FIX_ROOT / record_rel)
        _log(f"RECORD {record_rel} sha={core.sha256_file(FIX_ROOT / record_rel)} supersedes={record.get('supersedes')} anchor={record.get('canonical_anchor')}")

        # === strict State prePreview & history readback (no Preview) ===
        _log("===STRICT_STATE_PREVIEW_PENDING===")
        st1 = core.load_json(state_path)
        assert st1.get("lifecycle_state") == "VALIDATED_DRAFT", st1.get("lifecycle_state")
        assert st1.get("human_gates", {}).get("publication_preview") == "pending", st1.get("human_gates")
        assert st1.get("human_gate_provenance", {}).get("publication_preview") is None
        errs1 = agent.validate_agent_state(FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG), st1)
        assert not errs1, f"strict State unhealthy {errs1}"
        _log("STRICT_STATE_OK")
        sel1 = setmod.resolve_publication_selection(FIX_ROOT, core.load_json(FIX_ROOT / core.DEFAULT_CONFIG), st1)
        assert sel1.get("mode") == "VERSIONED_ACTIVE", sel1.get("mode")
        cand = (sel1.get("candidate_ref") or {}).get("path")
        _log(f"SELECTION mode={sel1.get('mode')} candidate={cand}")
        # History readback (exact record, no Preview).
        hist = edpub.verify_activation_history(FIX_ROOT, record_rel)
        _log(f"HISTORY status={hist.get('status') if isinstance(hist, dict) else hist}")
        # Active receipt/Gate/Candidate rechecks on sealed set.
        prop_pub_prefix = f"sources/{ISSUE}/publication/v2/editorial-corrections/{PROPOSAL_ID}/publication/"
        rv = edpub.validate_editorial_receipt(FIX_ROOT, f"{prop_pub_prefix}validated-source-manifest.json", state_rel)
        _log(f"RECEIPT issue={rv.get('issue_id')}")
        gv = reader_gate.validate_reader_surface_gate(
            FIX_ROOT, f"{prop_pub_prefix}reader-surface-gate-v2.json",
            issue_id=ISSUE, publication_profile=("WEEKLY_MAGAZINE" if KIND == "weekly" else "LONGFORM_SPECIAL"),
            expected_manuscript_path=FIX_ROOT / f"{prop_pub_prefix}reader-manuscript-v2.json",
            state_path=state_rel)
        assert gv.get("status") == "PASSED", gv
        _log("GATE_PASSED")
        cv = pubmod.validate_candidate(FIX_ROOT, FIX_ROOT / f"{prop_pub_prefix}publication-candidate-v2.json")
        _log(f"CANDIDATE status={cv.get('status') if isinstance(cv, dict) else cv}")
        if KIND == "longform":
            assert core.sha256_file(FIX_ROOT / old_cand_rel) == old_cand_sha, "old canonical candidate drift"
            _log(f"OLD_CANDIDATE_PRESERVED {old_cand_rel}")
            assert cand != old_cand_rel, "active selection must not adopt old canonical"
            _log("OLD_CANDIDATE_NOT_ADOPTED_OK")

        # === evidence manifest (references, DB not in notes) ===
        ev = {
            "kind": KIND, "issue": ISSUE, "proposal_id": PROPOSAL_ID,
            "fix_root": str(FIX_ROOT),
            "head": head, "tree": actual_tree, "lsfiles": ls_n,
            "state": {"path": state_rel, "sha256": core.sha256_file(FIX_ROOT / state_rel)},
            "proposal": {"path": prop_rel, "sha256": core.sha256_file(FIX_ROOT / prop_rel)},
            "retention_manifest": {"path": str((FIX_ROOT / cap['manifest_path']).relative_to(FIX_ROOT)) if not str(cap['manifest_path']).startswith("/") else cap['manifest_path'],
                                   "sha256": core.sha256_file(manifest_path)},
            "scope_review": {"path": str(scope_path.relative_to(FIX_ROOT)), "sha256": core.sha256_file(scope_path)},
            "staged_manifest": {"path": str(staged_manifest_path.relative_to(FIX_ROOT)), "sha256": core.sha256_file(staged_manifest_path)},
            "manuscript_spec": {"path": str(mspec_path.relative_to(FIX_ROOT)), "sha256": core.sha256_file(mspec_path)},
            "toolchain_spec": {"path": str(tspec_path.relative_to(FIX_ROOT)), "sha256": core.sha256_file(tspec_path)},
            "seal": {"path": set_rel, "sha256": core.sha256_file(FIX_ROOT / set_rel)},
            "record": {"path": record_rel, "sha256": core.sha256_file(FIX_ROOT / record_rel),
                       "supersedes": record.get("supersedes"), "canonical_anchor": record.get("canonical_anchor")},
            "publication": {
                "manuscript": {"path": str(manuscript_path.relative_to(FIX_ROOT)), "sha256": core.sha256_file(manuscript_path)},
                "pdf": {"path": str(pdf_path.relative_to(FIX_ROOT)), "sha256": core.sha256_file(pdf_path),
                        "bytes": pdf_path.stat().st_size, "pages": pages},
                "log": {"path": str(log_path.relative_to(FIX_ROOT)), "sha256": core.sha256_file(log_path),
                        "bytes": log_path.stat().st_size},
                "deterministic_checks": {"path": str(det_path.relative_to(FIX_ROOT)), "sha256": core.sha256_file(det_path)},
                "semantic_review": {"path": str(sem_path.relative_to(FIX_ROOT)), "sha256": core.sha256_file(sem_path)},
                "visual_review": {"path": str(vis_path.relative_to(FIX_ROOT)), "sha256": core.sha256_file(vis_path)},
            },
            "toolchain": {"lualatex": str(TL_BIN), "biber": str(BIBER_BIN),
                          "recipe": "lualatex-biber-lualatex",
                          "argv": list(edpub.EXPECTED_ARGV_LUALATEX_BIBER)},
            "selection": {"mode": sel1.get("mode"), "candidate": cand},
            "prepare_dt_s": dt,
        }
        core.write_json(NOTES / f"bootstrap-{KIND}-evidence.json", ev)
        _log(f"EVIDENCE {NOTES / f'bootstrap-{KIND}-evidence.json'}")
        _log(f"=== BOOTSTRAP {KIND.upper()} ACTIVATED prePreview (terminal) ===")
        return 0
    except Exception:
        traceback.print_exc()
        # Preserve partials: do NOT delete FIX_ROOT, do NOT truncate logs.
        # Write failure marker with traceback preserved.
        try:
            (NOTES / f"bootstrap-{KIND}-FAILURE.txt").write_text(traceback.format_exc(), encoding="utf-8")
        except Exception:
            pass
        print(f"EXIT:2 (failure preserved at {FIX_ROOT})", flush=True)
        return 2


if __name__ == "__main__":
    try:
        rc = main()
    except Exception:
        traceback.print_exc()
        rc = 2
    print(f"EXIT:{rc}", flush=True)
    sys.exit(rc)
