#!/usr/bin/env python3
"""R5b Weekly TWO-REVISION fixture build on FINAL R5b source epoch (no old fixtures).

Fixed SOURCE: FINAL R5b snapshot 10e8662e21fd0aa3c2d71c0bb8d6bf6ae3271ae9
(tree e434978d0d2034f1a6ec51813be92434234bd3b7, 720 files, read-only SOURCE image;
this script runs only in a FRESH independent copy argv FIX_ROOT).

Public CLI coverage: FIRST correction wk-r5b-1 uses direct APIs; SECOND
correction wk-r5b-2 uses the public CLI (prepare-publication /
finalize-publication / activate-publication via subprocess) to prove the
shipped command path on the final epoch; idempotency probe stays on API.

This script (created BEFORE execution, NEW file -- never the saved fixed-path
runners) performs in a FRESH independent copy (argv FIX_ROOT):
  0. Copy verification (HEAD/tree/count/inodes/no alternates, inert origin;
     EXPECT_HEAD + EXPECT_COUNT come from argv, never typed stale hashes).
  1. Bootstrap canonical Weekly VALIDATED_DRAFT via P1 test helpers (no R1:
     first anchor is the original validation checkpoint).
  2. FIRST correction wk-r5b-1: P1 -> P2R -> scope -> P2V -> P3S(50) ->
     REAL TL2026 prepare -> typed reviews + bounded QA -> finalize ->
     activate (expect ACTIVATED, anchor VALIDATION_CHECKPOINT, supersedes null;
     no canonical candidate on disk, so before_candidate_ref is null).
     Strict State/readback + old-immutable checks. NO Preview/lifecycle
     (first active preserved before Preview for later lifecycle owner).
  3. SECOND correction wk-r5b-2 (new headline): prepare/finalize, then capture
     an actual sealed INERT set checkpoint copy (State after first, second
     Candidate/seal complete, NO second record) to INERT_ROOT + manifest, then
     activate (expect ACTIVATED, supersedes == first activation, SAME anchor).
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
    if len(sys.argv) != 7:
        print(f"usage: {sys.argv[0]} FIX_ROOT NOTES_DIR EXPECT_HEAD EXPECT_TREE EXPECT_COUNT INERT_ROOT", flush=True)
        return 2
    FIX_ROOT = Path(sys.argv[1]).resolve()
    NOTES = Path(sys.argv[2]).resolve()
    NOTES.mkdir(parents=True, exist_ok=True)
    EXPECT_HEAD = sys.argv[3].strip().lower()
    EXPECT_TREE = sys.argv[4].strip().lower()
    EXPECT_COUNT = int(sys.argv[5])
    INERT_ROOT = Path(sys.argv[6]).resolve() if sys.argv[6].strip() else None
    for _label, _val in (("EXPECT_HEAD", EXPECT_HEAD), ("EXPECT_TREE", EXPECT_TREE)):
        if len(_val) != 40 or any(c not in "0123456789abcdef" for c in _val):
            print(f"BLOCKER {_label} must be 40-char hex, got {_val!r}", flush=True)
            return 2
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

    def _cli_edpub(*cli_args):
        """Run the PUBLIC CLI (prepare/finalize/activate) in a fresh subprocess
        bound to this fixture. Proves the shipped command path, not just APIs."""
        cmd = [sys.executable, "-m", "scripts.survey_editorial_publication_v2",
               "--repo-root", str(FIX_ROOT)] + list(cli_args)
        env = {k: v for k, v in os.environ.items()
               if not k.startswith("GIT_") and k != "PYTHONPATH"}
        env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
                    "GIT_ALLOW_PROTOCOL": "file",
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "PYTHONPYCACHEPREFIX": os.environ.get("PYTHONPYCACHEPREFIX", ""),
                    "TMPDIR": os.environ.get("TMPDIR", "")})
        proc = subprocess.run(cmd, cwd=FIX_ROOT, capture_output=True,
                              text=True, timeout=1800, env=env)
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
    fr = os.environ.get("FINAL_R5B_ROOT", "")
    if not fr or not Path(fr).is_dir():
        _log(f"BLOCKER FINAL_R5B_ROOT missing/not-a-dir: {fr!r}")
        return 2
    if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
        _log("BLOCKER PYTHONDONTWRITEBYTECODE!=1 (must be set BEFORE python startup)")
        return 2
    for _k in ("PYTHONPYCACHEPREFIX", "TMPDIR"):
        _v = os.environ.get(_k, "")
        if not _v.startswith(fr + "/"):
            _log(f"BLOCKER {_k} must be under FINAL_R5B_ROOT ({fr}), got {_v!r}")
            return 2
    _log(f"ENV_OK FINAL_R5B_ROOT={fr} pycache={os.environ.get('PYTHONPYCACHEPREFIX')} tmp={os.environ.get('TMPDIR')}")
    # Own-Git ownership BEFORE any Git write: toplevel+gitdir must equal this
    # fixture (never parent reconstruct), no alternates, inert origin.
    top = _run_git("rev-parse", "--show-toplevel").stdout.strip()
    gdir = _run_git("rev-parse", "--absolute-git-dir").stdout.strip()
    if Path(top) != FIX_ROOT or Path(gdir) != FIX_ROOT / ".git":
        _log(f"BLOCKER fixture .git not owned: top={top} gitdir={gdir} fix={FIX_ROOT}")
        return 2
    for _alt in (FIX_ROOT / ".git/objects/info/alternates", FIX_ROOT / ".git/info/alternates"):
        if _alt.exists():
            _log(f"BLOCKER alternates present: {_alt}")
            return 2
    origin = _run_git("remote", "-v").stdout
    if "example.invalid" not in origin:
        _log(f"BLOCKER origin not inert: {origin[:200]}")
        return 2
    _log(f"OWN_GIT_OK top={top}")
    head = _run_git("rev-parse", "HEAD").stdout.strip()
    _log(f"HEAD={head}")
    if head != EXPECT_HEAD:
        _log("UNEXPECTED SOURCE HEAD")
        return 2
    _log(f"LSFILES={len(_run_git('ls-files').stdout.strip().splitlines())} (expect {EXPECT_COUNT})")
    if len(_run_git("ls-files").stdout.strip().splitlines()) != EXPECT_COUNT:
        _log("LSFILES BOUND FAILED")
        return 2
    actual_tree = _run_git("rev-parse", "HEAD^{tree}").stdout.strip()
    _log(f"TREE={actual_tree} (expect {EXPECT_TREE})")
    if len(actual_tree) != 40 or actual_tree != EXPECT_TREE:
        _log("TREE BOUND FAILED (must be actual 40-char tree from git, not typed)")
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
            first_auth = FIX_ROOT / f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-r5b-1/authoring-input.json"
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
                "R5b weekly second envelope correction.")
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
                     "detail": f"R5b manuscript author maps requirement for {proposal_id}."}
                    for plan in arch.get("packages", [])
                    for req in plan.get("must_cover_requirements", [])]
        requirements = [
            {"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED",
             "reader_locations": ["main.tex:summary"], "detail": "R5b synthesis."},
            {"requirement_id": "WEEKLY_COMMUNITY_MOVEMENT", "status": "FULFILLED",
             "reader_locations": ["main.tex:package-1"], "detail": "R5b movement."}]
        prop_rel = str(proposal_path.relative_to(FIX_ROOT))
        mspec = {"schema_version": "2.0-rc1", "kind": "EDITORIAL_MANUSCRIPT_SPEC_V1",
                 "issue_id": issue_id,
                 "proposal_ref": {"path": prop_rel, "sha256": core.sha256_file(proposal_path)},
                 "architecture_coverage": coverage, "reader_requirements": requirements,
                 "authored_by": "r5b manuscript author",
                 "recorded_at": datetime.now(timezone.utc).isoformat()}
        mspec_path = proposal_path.parent / "manuscript-spec.json"
        core.write_json(mspec_path, mspec)
        tspec = {"schema_version": "2.0-rc1", "kind": "EDITORIAL_TOOLCHAIN_SPEC_V1",
                 "executor": "r5b-integration",
                 "absolute_executable": str(TL_BIN), "recipe": "lualatex-biber-lualatex",
                 "argv": list(edpub.EXPECTED_ARGV_LUALATEX_BIBER), "env": {},
                 "recorded_at": datetime.now(timezone.utc).isoformat()}
        tspec_path = proposal_path.parent / "toolchain-spec.json"
        core.write_json(tspec_path, tspec)
        # prepare REAL TL2026 (first correction via API, second via PUBLIC CLI)
        t0 = time.monotonic()
        staged_rel = str(staged_manifest_path.relative_to(FIX_ROOT))
        mspec_rel = str(mspec_path.relative_to(FIX_ROOT))
        tspec_rel = str(tspec_path.relative_to(FIX_ROOT))
        now_iso = datetime.now(timezone.utc).isoformat()
        if first:
            prepared_paths = edpub.prepare_publication(
                FIX_ROOT, state_rel, prop_rel, staged_rel, mspec_rel, tspec_rel,
                datetime.now(timezone.utc))
            _log(f"API_PREPARE dt={time.monotonic()-t0:.1f}s")
        else:
            _log("CLI prepare-publication ...")
            p = _cli_edpub("prepare-publication", "--state", state_rel, "--proposal", prop_rel,
                           "--staged-manifest", staged_rel, "--manuscript-spec", mspec_rel,
                           "--toolchain-spec", tspec_rel, "--recorded-at", now_iso)
            if p.returncode != 0:
                _log(f"CLI_PREPARE BLOCKER rc={p.returncode} stderr={p.stderr[-2000:]}")
                return None
            try:
                prepared_paths = json.loads(p.stdout)
            except ValueError as exc:
                _log(f"CLI_PREPARE_NONJSON BLOCKER {exc} stdout={p.stdout[-500:]}")
                return None
            _log(f"CLI_PREPARE dt={time.monotonic()-t0:.1f}s keys={sorted(prepared_paths)}")
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
                             "status": "PASS", "scope": f"r5b {proposal_id} real-build"})
        main_bytes = (FIX_ROOT / staged_manifest["outputs"]["main"]["path"]).read_bytes()
        ip = qroot / "identifier-preservation.json"
        core.write_json(ip, {"check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
                             "source_sha256": core.sha256_bytes(main_bytes),
                             "inspected_identifiers": [issue_id],
                             "scope": f"r5b {proposal_id} real-build"})
        pp = qroot / "pdf-preflight.json"
        core.write_json(pp, {"check_id": "PDF_PREFLIGHT", "status": "PASS",
                             "page_count": pages,
                             "pdf_sha256": core.sha256_file(pdf_path),
                             "byte_count": pdf_path.stat().st_size,
                             "scope": f"r5b {proposal_id} real TL2026 PDF"})
        qchecks = [{"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS",
                    "executor": "r5b editorial with actual file assertions",
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
                       "detail": f"R5b synthetic {kind} reviewer; no genuine Human approval.",
                       "evidence_locations": [f"r5b-real-build:{proposal_id}:main.pdf"]}
                      for cid in sorted(reader_pub._expected_review_checks(FIX_ROOT, profile, kind))]
            reader_pub.build_review_record(
                FIX_ROOT, manuscript_path, pdf_path, pages, kind, checks,
                f"r5b synthetic {kind} reviewer", datetime.now(timezone.utc), pubdir / fname)
        sem_path = pubdir / "semantic-review-v2.json"
        vis_path = pubdir / "visual-review-v2.json"
        # finalize (inert healthy; second correction via PUBLIC CLI)
        det_rel = str(det_path.relative_to(FIX_ROOT))
        sem_rel = str(sem_path.relative_to(FIX_ROOT))
        vis_rel = str(vis_path.relative_to(FIX_ROOT))
        if first:
            set_ref = edpub.finalize_publication(
                FIX_ROOT, state_rel, prop_rel, staged_rel, det_rel, sem_rel, vis_rel,
                datetime.now(timezone.utc))
            _log(f"API_FINALIZE {json.dumps(set_ref)[:400]}")
        else:
            _log("CLI finalize-publication ...")
            p = _cli_edpub("finalize-publication", "--state", state_rel, "--proposal", prop_rel,
                           "--staged-manifest", staged_rel, "--deterministic-checks", det_rel,
                           "--semantic-review", sem_rel, "--visual-review", vis_rel,
                           "--recorded-at", now_iso)
            if p.returncode != 0:
                _log(f"CLI_FINALIZE BLOCKER rc={p.returncode} stderr={p.stderr[-2000:]}")
                return None
            try:
                set_ref = json.loads(p.stdout)
            except ValueError as exc:
                _log(f"CLI_FINALIZE_NONJSON BLOCKER {exc} stdout={p.stdout[-500:]}")
                return None
            _log(f"CLI_FINALIZE {json.dumps(set_ref)[:400]}")
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
            core.write_json(NOTES / "inert-manifest-weekly.json", iman)
            _log(f"INERT_CHECKPOINT {INERT_ROOT} head={ihead}")
        # activate (second correction via PUBLIC CLI)
        if first:
            res = edpub.activate_publication(
                FIX_ROOT, state_rel, set_rel, f"R5b weekly editorial correction {proposal_id}",
                f"r5b-executor-{proposal_id}", datetime.now(timezone.utc))
            _log(f"API_ACTIVATE {json.dumps(res)[:800]}")
        else:
            _log("CLI activate-publication ...")
            p = _cli_edpub("activate-publication", "--state", state_rel, "--set", set_rel,
                           "--reason", f"R5b weekly editorial correction {proposal_id}",
                           "--executor", f"r5b-executor-{proposal_id}",
                           "--recorded-at", now_iso)
            if p.returncode != 0:
                _log(f"CLI_ACTIVATE BLOCKER rc={p.returncode} stderr={p.stderr[-2000:]}")
                return None
            try:
                res = json.loads(p.stdout)
            except ValueError as exc:
                _log(f"CLI_ACTIVATE_NONJSON BLOCKER {exc} stdout={p.stdout[-500:]}")
                return None
            _log(f"CLI_ACTIVATE {json.dumps(res)[:800]}")
        assert res.get("status") == "ACTIVATED", res
        return {"proposal_path": proposal_path, "prepared": prepared,
                "set_rel": set_rel, "record": core.load_json(FIX_ROOT / res["record_path"]),
                "record_rel": res["record_path"] if isinstance(res["record_path"], str)
                else str(res["record_path"]),
                "pubdir": pubdir, "snap_before": snap_before}

    first = _cycle("wk-r5b-1", "Weekly tested method, revised edition", True)
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

    second = _cycle("wk-r5b-2", "Weekly tested method \u2014 Second Editorial Correction", False)
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
    assert cand2 == f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-candidate-v2.json", cand2
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
    pub_prefix = f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-r5b-2/publication/"
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
        FIX_ROOT, f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-r5b-2/publication/validated-source-manifest.json",
        state_rel)
    _log(f"SECOND_RECEIPT issue={rv.get('issue_id')}")
    gv = reader_gate.validate_reader_surface_gate(
        FIX_ROOT, f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-r5b-2/publication/reader-surface-gate-v2.json",
        issue_id=ISSUE, publication_profile="WEEKLY_MAGAZINE",
        expected_manuscript_path=FIX_ROOT / f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-r5b-2/publication/reader-manuscript-v2.json",
        state_path=state_rel)
    assert gv.get("status") == "PASSED", gv
    _log("SECOND_GATE_PASSED")
    cv = pubmod.validate_candidate(
        FIX_ROOT, FIX_ROOT / f"sources/{ISSUE}/publication/v2/editorial-corrections/wk-r5b-2/publication/publication-candidate-v2.json")
    _log(f"SECOND_CANDIDATE status={cv.get('status') if isinstance(cv, dict) else cv}")
    # Idempotent re-activation of the same sealed set must be read-only.
    again = edpub.activate_publication(
        FIX_ROOT, state_rel, second["set_rel"], "R5b weekly idempotency probe",
        "r5b-idempotency-probe", datetime.now(timezone.utc))
    assert again.get("status") == "ALREADY_ACTIVE", again
    _log(f"ALREADY_ACTIVE_OK record={again.get('record_path')}")
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
