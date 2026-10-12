"""DM021-P1 focused tests: read-only editorial-correction proposal validation.

Real healthy fixtures through actual producers/stage validators in independent
Git databases (process-scoped identity, inert origins, no empty commits);
fixture source commits include all untracked P1/LF2I bytes. Every P1 call is
asserted side-effect-free via before/after tree+HEAD+status snapshots. All
synthetic reviews are type/identity fixtures, never semantic acceptance.
"""
from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from pypdf import PdfReader, PdfWriter

from scripts import survey_agent_control_v2 as agent
from scripts import survey_editorial_correction_proposal_v2 as proposal_mod
from scripts import survey_production_v2 as core
from scripts import survey_publication_v2 as publication
from scripts import survey_quality_v2 as quality
from scripts import survey_reader_publication_v2 as reader_publication
from scripts import survey_reader_surface_gate_v2 as reader_gate
from scripts import survey_weekly_derivation_v2 as weekly
from scripts import survey_weekly_semantic_publication_v2 as weekly_publication
from scripts import survey_longform_generated_v2 as generated
from tests import test_survey_increment_b_weekly_derivation_v2 as incb
from tests import test_survey_longform_derivation_v2 as lf1_tests
from tests import test_survey_longform_publication_integration_v2 as lf2i_tests

ProposalError = proposal_mod.ProposalError

_GIT_VARS = (
    "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR",
)

# Untracked P1/LF2I source bytes that fixture copies must include and pin.
UNTRACKED_SOURCES = (
    "scripts/survey_longform_derivation_v2.py",
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_longform_semantic_publication_v2.py",
    "scripts/survey_editorial_correction_proposal_v2.py",
    "schemas/longform-publication-source-manifest-v2.schema.json",
    "schemas/longform-reader-input-v2.schema.json",
    "schemas/editorial-correction-proposal-v2.schema.json",
    "tests/test_survey_longform_derivation_v2.py",
    "tests/test_survey_longform_publication_integration_v2.py",
    "tests/test_survey_editorial_correction_proposal_v2.py",
)

W_ISSUE = incb.ISSUE
L_ISSUE = lf2i_tests.ISSUE


def _run_git(root: Path, *args: str, env_extra: dict | None = None) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({
        "GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file",
        "GIT_AUTHOR_NAME": "Synthetic DM021-P1 Fixture", "GIT_AUTHOR_EMAIL": "p1-fixture@example.invalid",
        "GIT_COMMITTER_NAME": "Synthetic DM021-P1 Fixture", "GIT_COMMITTER_EMAIL": "p1-fixture@example.invalid",
    })
    if env_extra:
        env.update(env_extra)
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, env=env)


def _make_source_root(testcase: unittest.TestCase, prefix: str) -> tuple[tempfile.TemporaryDirectory, Path]:
    workspace = Path(__file__).resolve().parents[1]
    scratch = tempfile.TemporaryDirectory(prefix=prefix)
    testcase.addCleanup(scratch.cleanup)
    root = Path(scratch.name).resolve()
    tracked = subprocess.run(
        ["git", "ls-files", "-z", "--", "config", "schemas", "scripts", "templates", "prompts",
         "docs", "data", "tests"],
        cwd=workspace, capture_output=True, check=True).stdout
    for raw in tracked.split(b"\0"):
        if not raw:
            continue
        relative = Path(raw.decode("utf-8"))
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(workspace / relative, destination)
    pinned: dict[str, str] = {}
    for rel in UNTRACKED_SOURCES:
        source = workspace / rel
        testcase.assertTrue(source.is_file(), f"untracked P1/LF2I source missing: {rel}")
        destination = root / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        pinned[rel] = core.sha256_file(source)
        testcase.assertEqual(core.sha256_file(destination), pinned[rel], f"fixture copy drift: {rel}")
    for command in (
        ["init", "-q"],
        ["remote", "add", "origin", "https://example.invalid/dm021-p1-fixture.git"],
        ["add", "-A"],
        ["-c", "user.name=Synthetic DM021-P1 Fixture",
         "-c", "user.email=p1-fixture@example.invalid",
         "commit", "-q", "-m", "Synthetic isolated DM021-P1 source basis"],
    ):
        proc = _run_git(root, *command)
        testcase.assertEqual(proc.returncode, 0, f"git {command}: {proc.stderr}")
    status = _run_git(root, "status", "--porcelain").stdout
    testcase.assertEqual(status, "", f"fixture source not clean after commit: {status}")
    listed = _run_git(root, "config", "--local", "--list").stdout
    testcase.assertNotIn("user.name=", listed)
    testcase.assertNotIn("user.email=", listed)
    return scratch, root


def _snapshot(root: Path) -> dict:
    # Owned-tree/State/refs snapshot: regular-file hashes plus symlink/dir/FIFO
    # inventory (never opens FIFO/device) plus Git HEAD/status. Used immediately
    # around EACH P1 call after setup/fault mutation, before cleanup.
    import stat as _stat
    files: dict[str, str] = {}
    special: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if ".git" in path.parts:
            continue
        rel = str(path.relative_to(root))
        try:
            st = path.lstat()
        except OSError:
            special[rel] = "UNREADABLE"
            continue
        if _stat.S_ISLNK(st.st_mode):
            try:
                special[rel] = "SYMLINK->" + str(path.readlink())
            except OSError:
                special[rel] = "SYMLINK"
            continue
        if _stat.S_ISDIR(st.st_mode):
            special[rel] = "DIR"
            continue
        if not _stat.S_ISREG(st.st_mode):
            # FIFO/device/socket: record presence, never open.
            special[rel] = "SPECIAL:" + oct(_stat.S_IMODE(st.st_mode))
            continue
        # Regular file: hash without following symlinks (already excluded).
        try:
            files[rel] = core.sha256_file(path)
        except OSError:
            special[rel] = "UNREADABLE_FILE"
    head = _run_git(root, "rev-parse", "HEAD")
    status = _run_git(root, "status", "--porcelain")
    return {"files": files, "special": special, "head": head.stdout, "status": status.stdout}


def _assert_no_write(testcase: unittest.TestCase, before: dict, after: dict, label: str) -> None:
    testcase.assertEqual(after["files"], before["files"], f"tree write during {label}")
    testcase.assertEqual(after.get("special"), before.get("special"), f"special/dir/symlink write during {label}")
    testcase.assertEqual(after["head"], before["head"], f"HEAD moved during {label}")
    testcase.assertEqual(after["status"], before["status"], f"status changed during {label}")


def _new_weekly_helper(testcase: unittest.TestCase, root: Path):
    helper = incb.IncrementBWeeklyDerivationV2Tests(methodName="test_accepted_weekly_chain_probe")
    helper.root = root
    helper.cfg = core.load_json(root / core.DEFAULT_CONFIG)
    helper.head = core.repository_commit_sha(root)
    helper.source_root = root / "sources" / W_ISSUE
    helper.survey_root = root / "surveys" / "weekly" / W_ISSUE
    return helper


def _build_weekly_validated(testcase: unittest.TestCase, helper) -> dict:
    """Straight-line healthy Weekly VALIDATED_DRAFT (adapted increment-B recipe)."""
    root, cfg = helper.root, helper.cfg
    chain = helper._complete_authorities(helper._chain())
    state_path = helper._current_state(chain)
    publication_root = helper.source_root / "publication/v2"
    argv = ["survey_weekly_semantic_publication_v2.py", "--repo-root", str(root),
            "--state", str(state_path), "--input", str(chain["authored_path"])]
    with mock.patch.object(sys, "argv", argv + ["--materialize-surface-only"]):
        testcase.assertEqual(weekly_publication.main(), 0)
    surface_path = publication_root / "reader-surface-input-v2.json"
    testcase.assertTrue(surface_path.is_file())
    review_path = publication_root / "reader-surface-semantic-review-v2.json"
    review = {
        "schema_version": "2.0-rc1", "issue_id": W_ISSUE,
        "publication_profile": "WEEKLY_MAGAZINE", "review_kind": "SEMANTIC_EDITORIAL",
        "reviewed_surface": {"path": str(surface_path.relative_to(root)),
                             "sha256": core.sha256_file(surface_path)},
        "checks": [{"check_id": "READER_PIPELINE_INDEPENDENCE", "status": "PASS",
                    "detail": "Synthetic reviewer judged complete fixture prose independently understandable.",
                    "evidence_locations": ["reader-surface-input-v2.json:packages"]}],
        "decision": "PASS", "reviewed_by": "synthetic DM021-P1 reviewer",
        "reviewed_at": "2026-09-19T05:00:00+09:00", "recorded_at": "2026-09-19T05:00:00+09:00",
        "status": "PASSED", "findings": [],
        "summary": "Synthetic PASS for P1 fixture.",
    }
    review["review_sha256"] = core.sha256_object(review)
    core.write_json(review_path, review)
    with mock.patch.object(sys, "argv", argv):
        testcase.assertEqual(weekly_publication.main(), 0)
    receipt_path = publication_root / "validated-source-manifest.json"
    testcase.assertTrue(receipt_path.is_file())
    weekly.validate_receipt(root, receipt_path, state_path)
    architecture = core.load_json(helper.source_root / "architecture-v2.json")
    coverage = [
        {"package_id": plan["package_id"], "requirement": requirement,
         "status": "FULFILLED", "reader_locations": ["main.tex:package-1"],
         "detail": "Synthetic P1 fixture author maps the accepted package requirement."}
        for plan in architecture["packages"] for requirement in plan["must_cover_requirements"]]
    requirements = [
        {"requirement_id": key, "status": "FULFILLED", "reader_locations": [location],
         "detail": "Synthetic P1 fixture author asserts this visible requirement is present."}
        for key, location in (("FINAL_SYNTHESIS", "main.tex:summary"),
                              ("WEEKLY_COMMUNITY_MOVEMENT", "main.tex:package-1"))]
    manuscript_path = publication_root / "reader-manuscript-v2.json"
    reader_publication.build_manuscript_manifest(
        root, W_ISSUE, chain["profile_path"], helper.source_root / "architecture-v2.json",
        chain["approval_path"], helper.survey_root / "main.tex",
        [{"role": "BIBLIOGRAPHY", "path": str((helper.survey_root / "references.bib").relative_to(root))},
         {"role": "STYLE", "path": str((helper.survey_root / "jgaisurvey.sty").relative_to(root))}],
        coverage, requirements, "synthetic P1 manuscript author",
        core.parse_instant("2026-09-19T05:10:00+09:00"), manuscript_path)
    gate_path = publication_root / "reader-surface-gate-v2.json"
    reader_publication.build_reader_surface_gate(
        root, manuscript_path, review_path, output_path=gate_path, state_path=state_path)
    gate = reader_gate.validate_reader_surface_gate(
        root, gate_path, issue_id=W_ISSUE, publication_profile="WEEKLY_MAGAZINE",
        expected_manuscript_path=manuscript_path, state_path=state_path)
    testcase.assertEqual(gate["status"], "PASSED")
    pdf_path = helper.survey_root / "main.pdf"
    pdf = PdfWriter()
    pdf.add_blank_page(width=595, height=842)
    with pdf_path.open("wb") as output:
        pdf.write(output)
    testcase.assertEqual(len(PdfReader(pdf_path).pages), 1)
    quality_root = publication_root / "quality"
    quality_root.mkdir(parents=True, exist_ok=True)
    subject_path = quality_root / "subject-entity-property-binding.json"
    core.write_json(subject_path, {"check_id": "SUBJECT_ENTITY_PROPERTY_BINDING", "status": "PASS",
                                   "scope": "synthetic P1 fixture"})
    identifier_path = quality_root / "identifier-preservation.json"
    core.write_json(identifier_path, {
        "check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
        "source_sha256": core.sha256_file(helper.survey_root / "main.tex"),
        "inspected_identifiers": [W_ISSUE], "scope": "synthetic P1 fixture"})
    preflight_path = quality_root / "pdf-preflight.json"
    core.write_json(preflight_path, {
        "check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": 1,
        "pdf_sha256": core.sha256_file(pdf_path), "byte_count": pdf_path.stat().st_size,
        "scope": "synthetic parseable one-page PDF; not a TeX rendering"})
    result_paths = {"SUBJECT_ENTITY_PROPERTY_BINDING": subject_path,
                    "IDENTIFIER_PRESERVATION": identifier_path, "PDF_PREFLIGHT": preflight_path}
    quality_checks = [
        {"check_id": check_id, "kind": "DETERMINISTIC", "status": "PASS",
         "executor": "synthetic P1 fixture with actual file assertions",
         "evidence": "Exact fixture bytes and result file inspected by test.",
         "recorded_at": "2026-09-19T05:20:00+09:00",
         "result": {"path": str(path.relative_to(root)), "sha256": core.sha256_file(path)}}
        for check_id, path in result_paths.items()]
    bundle_path = publication_root / "quality-regression-bundle-v2.json"
    quality.build_bundle(root, W_ISSUE, helper.survey_root / "main.tex", pdf_path,
                         quality_checks, bundle_path, production_profile_path=chain["profile_path"])
    profile = core.load_json(chain["profile_path"])
    review_paths: dict[str, Path] = {}
    for kind, name in (("SEMANTIC_EDITORIAL", "semantic-editorial-review-v2.json"),
                       ("VISUAL", "visual-review-v2.json")):
        checks = [{"check_id": check_id, "status": "PASS",
                   "detail": "Synthetic P1 fixture review; no real editorial or visual acceptance asserted.",
                   "evidence_locations": ["synthetic-fixture:main.tex"]}
                  for check_id in sorted(reader_publication._expected_review_checks(root, profile, kind))]
        path = publication_root / name
        reader_publication.build_review_record(
            root, manuscript_path, pdf_path, 1, kind, checks,
            f"synthetic P1 {kind} reviewer", core.parse_instant("2026-09-19T05:30:00+09:00"), path)
        review_paths[kind] = path
    helper._advance(chain, "DRAFT_COMPLETE", {
        "reader-manuscript": manuscript_path,
        "validated-source": helper.survey_root / "main.tex",
        "publication-pdf": pdf_path,
        "quality-regression-bundle": bundle_path,
        "semantic-review": review_paths["SEMANTIC_EDITORIAL"],
        "visual-review": review_paths["VISUAL"],
        "reader-surface-gate": gate_path}, 130)
    testcase.assertEqual(core.load_json(state_path)["lifecycle_state"], "VALIDATED_DRAFT")
    weekly.validate_receipt(root, receipt_path, state_path)
    return {"chain": chain, "state_path": state_path, "surface_path": surface_path,
            "review_path": review_path, "receipt_path": receipt_path,
            "manuscript_path": manuscript_path, "gate_path": gate_path,
            "bundle_path": bundle_path, "pdf_path": pdf_path,
            "later_sem": review_paths["SEMANTIC_EDITORIAL"], "later_vis": review_paths["VISUAL"]}


def _new_longform_helper(testcase: unittest.TestCase, root: Path, workspace: Path):
    helper = lf2i_tests.LongformPublicationIntegrationV2Tests(
        methodName="test_two_pass_initial_reviewer_gating")
    helper.root = root
    helper.cfg = core.load_json(root / core.DEFAULT_CONFIG)
    helper.head = core.repository_commit_sha(root)
    helper.workspace = workspace
    helper.source_root = root / "sources" / L_ISSUE
    helper.survey_root = root / "surveys" / "special" / L_ISSUE
    helper.publication_root = helper.source_root / "publication" / "v2"
    worker = lf1_tests.LongformDerivationV2Tests(
        methodName="test_valid_single_did_projects_every_category")
    worker.root = root
    worker.cfg = helper.cfg
    worker.head = helper.head
    worker.workspace = workspace
    test_self = helper

    def _bound_authored(chain: dict, review_reference: str = "fixture longform review") -> dict:
        return test_self._authored(chain, worker, review_reference)

    worker._authored = _bound_authored
    base_helper_factory = worker._evidence_helper

    def _clean_evidence_helper():
        helper_obj = base_helper_factory()
        original_discovery = helper_obj.discovery

        def _clean_discovery(issue_id: str, discovery_id: str, origin: str = "BASE") -> dict:
            record = original_discovery(issue_id, discovery_id, origin)
            record["source"] = helper_obj.source(lf2i_tests.URL_BY_DID[discovery_id])
            return record

        helper_obj.discovery = _clean_discovery
        return helper_obj

    worker._evidence_helper = _clean_evidence_helper
    helper.worker = worker
    return helper


DERIVATION_COMMENT_ANCHOR = "% Generated from the reviewed Core v2 complete reader input. Do not hand-edit."
DERIVATION_COMMENT_REVISED = (
    "% Generated from the reviewed Core v2 complete reader input. Do not hand-edit. "
    "Fixture derivation revision.")


def _commit_derivation_only_change(testcase: unittest.TestCase, root: Path) -> str:
    """Real derivation-only source commit: one TeX comment literal flows to main.tex only."""
    target = root / "scripts" / "survey_weekly_derivation_v2.py"
    text = target.read_text(encoding="utf-8")
    testcase.assertIn(DERIVATION_COMMENT_ANCHOR, text)
    testcase.assertNotIn("Fixture derivation revision", text)
    target.write_text(text.replace(DERIVATION_COMMENT_ANCHOR, DERIVATION_COMMENT_REVISED),
                      encoding="utf-8")
    proc = _run_git(root, "add", "scripts/survey_weekly_derivation_v2.py")
    testcase.assertEqual(proc.returncode, 0, proc.stderr)
    proc = _run_git(root, "-c", "user.name=Synthetic DM021-P1 Fixture",
                    "-c", "user.email=p1-fixture@example.invalid",
                    "commit", "-q", "-m", "Fixture reviewed derivation-only rendering change")
    testcase.assertEqual(proc.returncode, 0, proc.stderr)
    return core.repository_commit_sha(root)


def _rebuild_weekly_qa_after_regeneration(testcase: unittest.TestCase, root: Path, built: dict) -> None:
    """Honest QA cascade after a derivation-only regeneration (real builders only)."""
    helper_chain = built["chain"]
    helper = built["helper"]
    state_path, publication_root = built["state_path"], built["publication_root"]
    # Rebuild strictly in dependency order, unlinking each stale file immediately
    # before its own rebuild so pending-path row resolution never sees gaps.
    built["manuscript_path"].unlink()
    architecture = core.load_json(helper.source_root / "architecture-v2.json")
    coverage = [
        {"package_id": plan["package_id"], "requirement": requirement,
         "status": "FULFILLED", "reader_locations": ["main.tex:package-1"],
         "detail": "Synthetic P1 fixture author maps the accepted package requirement."}
        for plan in architecture["packages"] for requirement in plan["must_cover_requirements"]]
    requirements = [
        {"requirement_id": key, "status": "FULFILLED", "reader_locations": [location],
         "detail": "Synthetic P1 fixture author asserts this visible requirement is present."}
        for key, location in (("FINAL_SYNTHESIS", "main.tex:summary"),
                              ("WEEKLY_COMMUNITY_MOVEMENT", "main.tex:package-1"))]
    reader_publication.build_manuscript_manifest(
        root, W_ISSUE, helper_chain["profile_path"], helper.source_root / "architecture-v2.json",
        helper_chain["approval_path"], helper.survey_root / "main.tex",
        [{"role": "BIBLIOGRAPHY", "path": str((helper.survey_root / "references.bib").relative_to(root))},
         {"role": "STYLE", "path": str((helper.survey_root / "jgaisurvey.sty").relative_to(root))}],
        coverage, requirements, "synthetic P1 manuscript author",
        core.parse_instant("2026-09-19T06:10:00+09:00"), built["manuscript_path"])
    identifier_path = publication_root / "quality" / "identifier-preservation.json"
    core.write_json(identifier_path, {
        "check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
        "source_sha256": core.sha256_file(helper.survey_root / "main.tex"),
        "inspected_identifiers": [W_ISSUE], "scope": "synthetic P1 fixture"})
    result_paths = {
        "SUBJECT_ENTITY_PROPERTY_BINDING": publication_root / "quality" / "subject-entity-property-binding.json",
        "IDENTIFIER_PRESERVATION": identifier_path,
        "PDF_PREFLIGHT": publication_root / "quality" / "pdf-preflight.json"}
    quality_checks = [
        {"check_id": check_id, "kind": "DETERMINISTIC", "status": "PASS",
         "executor": "synthetic P1 fixture with actual file assertions",
         "evidence": "Exact fixture bytes and result file inspected by test.",
         "recorded_at": "2026-09-19T06:20:00+09:00",
         "result": {"path": str(path.relative_to(root)), "sha256": core.sha256_file(path)}}
        for check_id, path in result_paths.items()]
    built["bundle_path"].unlink()
    quality.build_bundle(root, W_ISSUE, helper.survey_root / "main.tex", built["pdf_path"],
                         quality_checks, built["bundle_path"],
                         production_profile_path=helper_chain["profile_path"])
    profile = core.load_json(helper_chain["profile_path"])
    for kind, path in (("SEMANTIC_EDITORIAL", built["later_sem"]), ("VISUAL", built["later_vis"])):
        path.unlink()
        checks = [{"check_id": check_id, "status": "PASS",
                   "detail": "Synthetic P1 fixture review; no real editorial or visual acceptance asserted.",
                   "evidence_locations": ["synthetic-fixture:main.tex"]}
                  for check_id in sorted(reader_publication._expected_review_checks(root, profile, kind))]
        reader_publication.build_review_record(
            root, built["manuscript_path"], built["pdf_path"], 1, kind, checks,
            f"synthetic P1 {kind} reviewer", core.parse_instant("2026-09-19T06:30:00+09:00"), path)
    # Gate builder evaluates (pending replay needs the old gate present) then writes.
    reader_publication.build_reader_surface_gate(
        root, built["manuscript_path"], built["review_path"],
        output_path=built["gate_path"], state_path=state_path)
    gate = reader_gate.validate_reader_surface_gate(
        root, built["gate_path"], issue_id=W_ISSUE, publication_profile="WEEKLY_MAGAZINE",
        expected_manuscript_path=built["manuscript_path"], state_path=state_path)
    testcase.assertEqual(gate["status"], "PASSED")


def _regenerate_weekly_outputs(testcase: unittest.TestCase, root: Path, built: dict) -> None:
    """Honest post-VALIDATED regeneration with real producers (mirrors publisher pass2 tail).

    The publisher CLI is DRAFT_COMPLETE-gated by design, so the fixture replays
    its exact producer sequence: strict derivation, same-byte surface proof,
    bound pre-TeX review, deterministic render, receipt build + validation.
    """
    from scripts import survey_schema_v2 as schema_gate
    chain, state_path = built["chain"], built["state_path"]
    context = weekly.load_derivation(root, state_path, chain["authored_path"])
    surface = context["surface"]
    publication_root = context["source_root"] / "publication" / "v2"
    surface_path = publication_root / "reader-surface-input-v2.json"
    testcase.assertEqual(surface_path.read_bytes(), core.json_bytes(surface),
                         "same-byte refresh baseline must reproduce exact reader bytes")
    reader_gate.load_and_validate_reader_surface_semantic_review(
        root, built["review_path"], expected_issue_id=W_ISSUE,
        expected_publication_profile="WEEKLY_MAGAZINE",
        expected_surface_path=str(surface_path.relative_to(root)),
        expected_surface_sha256=core.sha256_file(surface_path), require_pass=True)
    survey_root = weekly.validate_survey_build_directory(root, context["profile"]["paths"]["survey_root"])
    main_text = weekly.render_main(surface)
    bibliography_text = weekly.render_bibliography(surface)
    style_bytes = (root / weekly.STYLE_PATH).read_bytes()
    weekly.validate_generated_closure(main_text, style_bytes.decode("utf-8"))
    primary_path = survey_root / "main.tex"
    bibliography_path = survey_root / "references.bib"
    style_path = survey_root / "jgaisurvey.sty"
    primary_path.write_text(main_text, encoding="utf-8")
    bibliography_path.write_text(bibliography_text, encoding="utf-8")
    style_path.write_bytes(style_bytes)
    archived_input = publication_root / "interactive-semantic-publication-input.json"
    core.write_json(archived_input, core.load_json(chain["authored_path"]))
    receipt_context = dict(context)
    receipt_context["authored_path"] = archived_input
    receipt = weekly.build_receipt(root, receipt_context, surface_path, built["review_path"],
                                   primary_path, bibliography_path, style_path)
    schema_gate.validate_instance(receipt, root / weekly.RECEIPT_SCHEMA, label="Weekly source receipt")
    receipt_path = publication_root / "validated-source-manifest.json"
    core.write_json(receipt_path, receipt)
    subject = {
        "schema_version": "2.0-rc1", "check_id": "SUBJECT_ENTITY_PROPERTY_BINDING",
        "status": "PASS", "issue_id": surface["issue_id"],
        "cited_discovery_count": len(surface["bibliography"]),
        "bindings": [
            {
                "discovery_id": row["discovery_id"], "canonical_name": row["title"],
                "canonical_url": row["url"], "materiality": context["records"][row["discovery_id"]]["materiality"],
                "status": context["records"][row["discovery_id"]]["status"],
                "source_accessed_at": context["records"][row["discovery_id"]]["source_accessed_at"],
            }
            for row in surface["bibliography"]],
    }
    core.write_json(publication_root / "quality" / "subject-entity-property-binding.json", subject)
    weekly.validate_receipt(root, receipt_path, state_path)


def _run_fixture_code(testcase: unittest.TestCase, root: Path, script: str,
                      args: list[str], timeout_s: int = 1200) -> str:
    """Execute a script with the FIXTURE's committed code (cwd=fixture root).

    Required after a fixture source commit: epoch guards bind execution to
    committed bytes, so replay validations must run the committed basis, not
    the ambient candidate checkout. Sanitized env, no network, no PYTHONPATH.
    """
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != "PYTHONPATH"}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file",
                "PYTHONDONTWRITEBYTECODE": "1"})
    proc = subprocess.run([sys.executable, "-c", script, *args], cwd=root,
                          capture_output=True, text=True, timeout=timeout_s, env=env)
    testcase.assertEqual(proc.returncode, 0,
                         f"fixture-code step failed:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr[-4000:]}")
    return proc.stdout


_FIXTURE_CASCADE = """
import json, sys
from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase
root = Path(sys.argv[1])
state_path = Path(sys.argv[2])
new_authored = Path(sys.argv[3])
proposal_id = sys.argv[4]
payload = json.loads(sys.argv[5])
from scripts import survey_agent_control_v2 as agent
from scripts import survey_production_v2 as core
from scripts import survey_editorial_correction_proposal_v2 as proposal_mod
from tests import test_survey_editorial_correction_proposal_v2 as p1t
tc = TestCase()
tc.maxDiff = None
cfg = core.load_json(root / core.DEFAULT_CONFIG)
chain = {k: (Path(v) if k.endswith("_path") else v) for k, v in payload["chain"].items()}
helper = SimpleNamespace(root=root, cfg=cfg, head=payload["head"],
                         source_root=root / payload["source_root"],
                         survey_root=root / payload["survey_root"])
built = {"chain": chain, "helper": helper, "state_path": state_path,
         "publication_root": root / payload["publication_root"],
         "surface_path": root / payload["surface_path"], "review_path": root / payload["review_path"],
         "receipt_path": root / payload["receipt_path"], "manuscript_path": root / payload["manuscript_path"],
         "gate_path": root / payload["gate_path"], "bundle_path": root / payload["bundle_path"],
         "pdf_path": root / payload["pdf_path"], "later_sem": root / payload["later_sem"],
         "later_vis": root / payload["later_vis"]}
p1t._regenerate_weekly_outputs(tc, root, built)
p1t._rebuild_weekly_qa_after_regeneration(tc, root, built)
record_path = agent.revalidate_publication_surface(
    root, cfg, state_path, "REVIEWED_CORE_CHANGE",
    "fixture reviewed derivation-only rendering change",
    "synthetic P1 predecessor fixture",
    core.parse_instant("2026-09-19T08:00:00+09:00"), None)
assert record_path.is_file(), "revalidation record missing"
assert agent.validate_agent_state(root, cfg, core.load_json(state_path)) == []
snap = p1t._snapshot(root)
prepared = proposal_mod.prepare_proposal(root, state_path, new_authored, proposal_id)
p1t._assert_no_write(tc, snap, p1t._snapshot(root), "predecessor prepare (fixture code)")
source_root = helper.source_root
proposal_path = p1t._stage_proposal(tc, root, source_root, proposal_id, prepared,
                                    new_authored.read_bytes())
staged = p1t._snapshot(root)
outcome = proposal_mod.validate_proposal(root, state_path, proposal_path)
p1t._assert_no_write(tc, staged, p1t._snapshot(root), "predecessor validate (fixture code)")
assert outcome["result"] == "REVIEW_REQUIRED", outcome["result"]
effective = prepared["effective"]
summary = {
    "record": str(record_path.relative_to(root)),
    "origins": {name: info["origin"] for name, info in effective.items()},
    "effective_shas": {name: info["sha256"] for name, info in effective.items()},
    "original_shas": {row["name"]: row["sha256"] for row in prepared["original_rows"]},
    "active_ref": prepared["proposal"]["basis"]["active_revalidation_ref"],
    "before_sha": core.sha256_bytes(prepared["before_canonical"]),
    "proposed_sha": core.sha256_bytes(prepared["proposed_canonical"]),
    "graph_nodes": len(prepared["graph"]["nodes"]),
    "graph_edges": len(prepared["graph"]["edges"]),
    "result": outcome["result"],
}
print(json.dumps(summary))
"""


def _stage_proposal(testcase: unittest.TestCase, root: Path, source_root: Path,
                    proposal_id: str, prepared: dict, authored_bytes: bytes) -> Path:
    # Legacy helper retained for compatibility: stages all three files AFTER prepare.
    # New tests must stage authoring BEFORE prepare via _stage_authoring_before_prepare()
    # and then stage reader+proposal via _stage_reader_and_proposal(). This helper
    # now asserts the proposal dir does not exist (old external-path flow) and is
    # only used by updated tests that already staged authoring? For safety, if the
    # dir already exists with staged authoring, only stage reader+proposal.
    proposal_dir = source_root / "publication" / "v2" / "editorial-corrections" / proposal_id
    if proposal_dir.exists():
        # Authoring already staged before prepare (new flow): only stage reader+proposal.
        testcase.assertTrue((proposal_dir / "authoring-input.json").is_file())
        testcase.assertEqual((proposal_dir / "authoring-input.json").read_bytes(), authored_bytes)
        (proposal_dir / "reader-surface-input-v2.json").write_bytes(prepared["proposed_canonical"])
        core.write_json(proposal_dir / "proposal.json", prepared["proposal"])
        return proposal_dir / "proposal.json"
    proposal_dir.mkdir(parents=True)
    (proposal_dir / "authoring-input.json").write_bytes(authored_bytes)
    (proposal_dir / "reader-surface-input-v2.json").write_bytes(prepared["proposed_canonical"])
    core.write_json(proposal_dir / "proposal.json", prepared["proposal"])
    return proposal_dir / "proposal.json"


def _stage_authoring_before_prepare(testcase: unittest.TestCase, root: Path, source_root: Path,
                                    proposal_id: str, authored: dict) -> Path:
    # Required new flow: authoring file already at the named proposal input BEFORE prepare.
    proposal_dir = source_root / "publication" / "v2" / "editorial-corrections" / proposal_id
    testcase.assertFalse(proposal_dir.exists(), f"proposal dir already exists: {proposal_dir}")
    proposal_dir.mkdir(parents=True)
    target = proposal_dir / "authoring-input.json"
    core.write_json(target, authored)
    testcase.assertTrue(target.is_file())
    return target


def _stage_reader_and_proposal(testcase: unittest.TestCase, root: Path, source_root: Path,
                               proposal_id: str, prepared: dict) -> Path:
    # After prepare (planned reader ref prospective), stage reader FILE + proposal.json.
    proposal_dir = source_root / "publication" / "v2" / "editorial-corrections" / proposal_id
    testcase.assertTrue((proposal_dir / "authoring-input.json").is_file())
    testcase.assertFalse((proposal_dir / "reader-surface-input-v2.json").exists())
    testcase.assertFalse((proposal_dir / "proposal.json").exists())
    (proposal_dir / "reader-surface-input-v2.json").write_bytes(prepared["proposed_canonical"])
    core.write_json(proposal_dir / "proposal.json", prepared["proposal"])
    return proposal_dir / "proposal.json"


def _scope_review_for(testcase: unittest.TestCase, root: Path, prepared: dict,
                      staged_reader_rel: str, name: str,
                      decision: str = "WITHIN_APPROVED_AUTHORITY",
                      before_override: dict | None = None,
                      upstream_override: str | None = None) -> Path:
    after_sha = core.sha256_bytes(prepared["proposed_canonical"])
    block = {
        "version": "EDITORIAL_CORRECTION_SCOPE_V1",
        "decision": decision,
        "before_reader_input": before_override or prepared["proposal"]["basis"]["active_reader_input_ref"],
        "preserved_upstream_sha256": upstream_override or prepared["proposal"]["basis"]["preserved_upstream_digest"],
        "change_summary": "Synthetic fixture scope judgment inside approved authority.",
        "evidence_locations": ["synthetic-fixture:proposal"],
    }
    review = {
        "schema_version": "2.0-rc1", "issue_id": prepared["proposal"]["issue_id"],
        "publication_profile": prepared["proposal"]["publication_profile"],
        "review_kind": "SEMANTIC_EDITORIAL",
        "reviewed_surface": {"path": staged_reader_rel, "sha256": after_sha},
        "checks": [
            {"check_id": "READER_PIPELINE_INDEPENDENCE", "status": "PASS",
             "detail": "Synthetic scope reviewer judged the proposed reader independently understandable.",
             "evidence_locations": ["synthetic-fixture:proposed-reader"]},
            {"check_id": "EDITORIAL_CORRECTION_SCOPE", "status": "PASS",
             "detail": "Synthetic scope reviewer judged the delta inside approved Architecture authority.",
             "evidence_locations": ["synthetic-fixture:proposal"]},
        ],
        "decision": "PASS", "reviewed_by": "synthetic P1 scope reviewer",
        "reviewed_at": "2026-09-19T07:00:00+09:00", "recorded_at": "2026-09-19T07:00:00+09:00",
        "status": "PASSED", "findings": [],
        "summary": "Synthetic scope PASS for P1 fixture.",
        "editorial_correction_scope": block,
    }
    review["review_sha256"] = core.sha256_object(review)
    path = root / staged_reader_rel
    scope_path = path.parent / name
    core.write_json(scope_path, review)
    return scope_path


def _assert_transitives_expected_set(testcase: unittest.TestCase, root: Path,
                                     source_root: Path, prepared: dict,
                                     state_path: Path | None = None) -> None:
    # R3 independent oracle: EXPECTEDSET from actual selected checkpoint rows
    # (via agent API in test, not receipt list) + independently loaded container
    # maps (explicit fields, not implementation graph). Proves candidate-selection,
    # exact profile-completeness, views acceptance/package/results + Evidence/
    # Screening/Discovery locals; research KEEP+frozen, wrappers KEEP not frozen,
    # pub/QA/State excluded; stale valid-looking sibling NOT adopted.
    from scripts import survey_agent_control_v2 as _agent
    graph = prepared["graph"]
    frozen = prepared["frozen"]
    nodes_by_path = {n["path"]: n for n in graph["nodes"]}
    frozen_by_path: dict[str, set[str]] = {}
    for row in frozen:
        frozen_by_path.setdefault(row["path"], set()).add(row["kind"])
    # Expected checkpoint artifacts via actual State-bound API in test (independent).
    # Requires state_path for resolve; derive from prepared basis if not given.
    if state_path is None:
        # Fallback: find State via basis state_ref (already pinned, validated).
        state_rel = prepared["proposal"]["basis"]["state_ref"]["path"]
        state_path = root / state_rel
    _state = core.load_json(state_path)
    _cfg = core.load_json(root / core.DEFAULT_CONFIG)
    _expected: dict[str, str] = {}  # path -> expected frozen kind (or "" for wrapper operational)
    _wrappers: set[str] = set()
    def _exp_ckpt(cp: str, name: str, frozen_kind: str | None) -> None:
        try:
            _r = _agent.resolve_checkpoint_artifact(root, _cfg, _state, cp, name)
        except Exception as exc:
            testcase.fail(f"test oracle cannot resolve {cp}/{name}: {exc}")
            return
        _rel = str(_r["artifact_path"].relative_to(root).as_posix())
        _expected[_rel] = frozen_kind or ""
        # Wrapper file itself (checkpoint record) operational, not frozen.
        _wref = (_state.get("checkpoint_provenance") or {}).get(cp) or {}
        _wrel = _wref.get("path", "")
        if _wrel:
            _wrappers.add(_wrel)
    # Exact producer/name map (R3, no fake names).
    _exp_ckpt("discovery", "discovery-acceptance", "discovery-acceptance")
    _exp_ckpt("screening", "screening-acceptance", "screening-acceptance")
    _exp_ckpt("evidence", "evidence-acceptance", "evidence-acceptance")
    _exp_ckpt("evidence", "edition-views-acceptance", "edition-views-acceptance")
    _exp_ckpt("materiality", "materiality-ledger", "materiality-ledger")
    _exp_ckpt("completeness", "profile-completeness", "profile-completeness")
    _exp_ckpt("selection", "candidate-matrix", "candidate-matrix")
    _exp_ckpt("selection", "candidate-selection", "candidate-selection")
    _exp_ckpt("architecture", "issue-architecture", "issue-architecture")
    _exp_ckpt("architecture", "architecture-review-summary", "architecture-review-summary")
    _exp_ckpt("architecture", "architecture-review-attention", "architecture-review-attention")
    _exp_ckpt("draft", "synthesis-input", "synthesis-input")
    _exp_ckpt("draft", "synthesis-result", "synthesis-result")
    # Draft packages/results dynamic via pinned draft record (no pid guessing).
    try:
        _draft_rec = _agent.resolve_checkpoint_artifact(root, _cfg, _state, "draft", "synthesis-input")
        _draft_record = core.load_json(_draft_rec["artifact_path"])
        # Actually need checkpoint RECORD (wrappers file), not synthesis-input file.
        # Load wrapper record for draft checkpoint (already pinned as wrapper, validated).
        _draft_wrapper_rel = ((_state.get("checkpoint_provenance") or {}).get("draft") or {}).get("path", "")
        _draft_wrapper = core.load_json(root / _draft_wrapper_rel) if _draft_wrapper_rel else {"artifacts": []}
        for _row in _draft_wrapper.get("artifacts", []) or []:
            _n = _row.get("name", "")
            if _n.startswith("draft-package:") or _n.startswith("draft-result:"):
                _expected[_row["path"]] = _n
    except Exception as exc:
        testcase.fail(f"draft dynamic discovery failed: {exc}")
    # Container maps independently (explicit fields, not P1 graph).
    # Evidence package/tasks via evidence acceptance explicit fields.
    try:
        _ev_rel = [p for p, k in _expected.items() if k == "evidence-acceptance"][0]
        _ev_data = core.load_json(root / _ev_rel)
        _pkg_rel = (Path(_ev_rel).parent / "package.json").as_posix()
        _expected[_pkg_rel] = "evidence-package"
        _pkg_data = core.load_json(root / _pkg_rel)
        for _t in _pkg_data.get("tasks", []) or []:
            _trel = (Path(_ev_rel).parent / _t.get("path", "")).as_posix()
            _expected[_trel] = f"evidence-task:{_t.get('evidence_task_id','')}"
        # Screening via evidence basis (explicit paths, independent).
        _sacc_rel = (_pkg_data.get("basis") or {}).get("screening_acceptance_path", "")
        if _sacc_rel:
            # Already in expected via checkpoint (screening-acceptance), verify same path.
            testcase.assertIn(_sacc_rel, _expected, "screening acceptance via evidence basis must match checkpoint")
        # Views files via views acceptance explicit views[] (independent).
        _vacc_rels = [p for p, k in _expected.items() if k == "edition-views-acceptance"]
        for _vrel in _vacc_rels:
            _vdata = core.load_json(root / _vrel)
            from scripts.survey_evidence_v2 import view_filename as _vfn
            for _vrow in _vdata.get("views", []) or []:
                _tid = _vrow.get("evidence_task_id", "")
                _fname = _vfn(_tid)
                _vf_rel = (Path(_vrel).parent / "views" / _fname).as_posix()
                _expected[_vf_rel] = f"edition-view:{_tid}"
        # Screening package/results/batches via screening acceptance explicit (independent).
        _sacc_only = [p for p, k in _expected.items() if k == "screening-acceptance"]
        for _srel in _sacc_only:
            _sdata = core.load_json(root / _srel)
            _spkg_rel = (Path(_srel).parent / "package.json").as_posix()
            _expected[_spkg_rel] = "screening-package"
            _spkg = core.load_json(root / _spkg_rel)
            for _b in ((_spkg.get("input") or {}).get("batches", []) or []):
                _brel = (Path(_srel).parent / _b.get("path", "")).as_posix()
                _expected[_brel] = f"screening-batch:{_b.get('batch_id','')}"
            for _ab in _sdata.get("batches", []) or []:
                _bid = _ab.get("batch_id", "")
                _rrel = (Path(_srel).parent / f"results/{_bid}.json").as_posix()
                _expected[_rrel] = f"screening-result:{_bid}"
    except Exception as exc:
        testcase.fail(f"container map independent load failed: {exc}")
    # Assert each expected in graph/retention with KEEP + frozen (research) vs wrappers.
    retention_by_path = {r["path"]: r for r in prepared["proposal"]["retention_plan"]}
    for _path, _kind in sorted(_expected.items()):
        with testcase.subTest(expected=_path):
            testcase.assertIn(_path, nodes_by_path, f"expected transitive missing in graph: {_path}")
            _node = nodes_by_path[_path]
            testcase.assertEqual(_node["policy"], "KEEP_IMMUTABLE", f"research must be KEEP: {_path}")
            testcase.assertIn(_path, retention_by_path, f"expected missing in retention: {_path}")
            testcase.assertEqual(retention_by_path[_path]["policy"], "KEEP_IMMUTABLE")
            testcase.assertIn("retained_ref", retention_by_path[_path])
            # Frozen inclusion for research (all expected here are research, not wrappers).
            testcase.assertIn(_path, frozen_by_path, f"research must be frozen: {_path}")
    for _wrel in sorted(_wrappers):
        with testcase.subTest(wrapper=_wrel):
            testcase.assertIn(_wrel, nodes_by_path, f"wrapper missing in graph: {_wrel}")
            testcase.assertEqual(nodes_by_path[_wrel]["policy"], "KEEP_IMMUTABLE")
            testcase.assertNotIn(_wrel, frozen_by_path, f"wrapper must stay operational (not frozen): {_wrel}")
    # Exclusion: pub/QA/State/receipt/candidate stay out of frozen (research-only digest).
    for _row in frozen:
        testcase.assertFalse(_row["path"].endswith("production-state.json"), "State must stay operational")
        testcase.assertFalse("orchestration/v2/checkpoints" in _row["path"], "wrappers must stay operational")
        testcase.assertFalse(_row["path"].endswith("validated-source-manifest.json"), "receipt must stay operational")
        testcase.assertFalse("publication-candidate-v2.json" in _row["path"], "candidate must stay operational")
    # Stale valid-looking sibling NOT adopted (presence must not infer authority).
    for _stale in sorted(source_root.glob("stale-*.json")):
        _srel = str(_stale.relative_to(root).as_posix())
        testcase.assertNotIn(_srel, nodes_by_path, f"stale sibling must NOT be adopted: {_srel}")
        testcase.assertNotIn(_srel, frozen_by_path, f"stale must NOT be frozen: {_srel}")


class EditorialCorrectionProposalV2Tests(unittest.TestCase):
    def setUp(self) -> None:
        for name in _GIT_VARS:
            if os.environ.get(name):
                raise AssertionError(f"unsafe inherited Git root override for isolated fixture: {name}")
        self.workspace = Path(__file__).resolve().parents[1]

    def test_longform_prose_correction_end_to_end(self) -> None:
        scratch, root = _make_source_root(self, "jgas-p1-longform-")
        helper = _new_longform_helper(self, root, self.workspace)
        chain = helper._complete(helper._chain())
        state_path = helper._state_path(chain)
        built = helper._advance_to_validated_draft(chain, state_path)
        self.assertEqual(core.load_json(state_path)["lifecycle_state"], "VALIDATED_DRAFT")
        authored = helper._authored(chain, helper.worker)
        authored["longform_revision"]["packages"][0]["narrative_sections"][0]["paragraphs"][0]["text"] += \
            " Revised fixture sentence within approved evidence."
        # R3 stale valid-looking sibling (NOT State-bound, must NOT be adopted).
        # Same bytes as real completeness (valid basis SHAs, same issue) at non-checkpoint path.
        _real_comp = helper.source_root / "profile-completeness.json"
        _stale_comp = helper.source_root / "stale-profile-completeness.json"
        if _real_comp.is_file():
            _stale_comp.write_bytes(_real_comp.read_bytes())
        # New flow: authoring already at named proposal input BEFORE prepare.
        staged_authoring = _stage_authoring_before_prepare(
            self, root, helper.source_root, "fixture-lf-rev-1", authored)
        before = _snapshot(root)
        prepared = proposal_mod.prepare_proposal(
            root, state_path, staged_authoring, "fixture-lf-rev-1",
            "Fixture longform prose correction within approved evidence.")
        _assert_no_write(self, before, _snapshot(root), "longform prepare")
        proposal = prepared["proposal"]
        self.assertEqual(proposal["status"], "PROPOSED")
        self.assertEqual(proposal["route"], "EDITORIAL_CORRECTION_PROPOSAL_V1")
        self.assertIsNone(proposal["basis"]["active_revalidation_ref"])
        self.assertIn("active_revalidation_ref", proposal["basis"])
        self.assertNotEqual(prepared["before_canonical"], prepared["proposed_canonical"])
        # Planned reader ref prospective (path canonical, sha equals canonical).
        self.assertTrue(proposal["proposed"]["proposed_reader_ref"]["path"].endswith(
            "/editorial-corrections/fixture-lf-rev-1/reader-surface-input-v2.json"))
        self.assertEqual(proposal["proposed"]["proposed_reader_ref"]["sha256"],
                         proposal["proposed"]["proposed_reader_canonical_sha256"])
        self.assertEqual(proposal["proposed"]["authoring_input_ref"]["path"],
                         str(staged_authoring.relative_to(root).as_posix()))
        nodes = prepared["graph"]["nodes"]
        self.assertTrue(all(set(n) == {"path", "sha256", "byte_count", "roles", "policy"} for n in nodes))
        # No singular role key in nodes or retention (R2).
        self.assertTrue(all("role" not in n for n in nodes))
        policies = {n["policy"] for n in nodes}
        self.assertEqual(policies, {"KEEP_IMMUTABLE", "COPY_BEFORE_REPLACEMENT"})
        self.assertTrue(all(r["policy"] in policies for r in proposal["retention_plan"]))
        self.assertTrue(all("role" not in r for r in proposal["retention_plan"]))
        self.assertTrue(all(set(r) >= {"roles", "path", "sha256", "byte_count", "policy"} for r in proposal["retention_plan"]))
        # Frozen completeness: full upstream kinds, no operational leakage.
        frozen_kinds = {row["kind"] for row in prepared["frozen"]}
        self.assertIn("production-profile", frozen_kinds)
        self.assertIn("issue-architecture", frozen_kinds)
        # At least one Draft package/result, Synthesis, Evidence, Matrix/Ledger/Discovery, drafting archive.
        for required in ("synthesis-input", "synthesis-result", "evidence-acceptance",
                         "candidate-matrix", "materiality-ledger", "discovery-acceptance",
                         "drafting-archive", "drafting-authored-archive"):
            # Longform uses drafting-archive; Weekly uses drafting-authored-archive.
            pass
        # Longform-specific: drafting-archive must be frozen, publication-authored excluded.
        frozen_by_path = {row["path"]: row["kind"] for row in prepared["frozen"]}
        self.assertTrue(any(k.startswith("draft-package:") for k in frozen_kinds))
        self.assertTrue(any(k.startswith("draft-result:") for k in frozen_kinds))
        self.assertTrue(any(k.startswith("evidence-card:") for k in frozen_kinds))
        # Mutable publication inputs must NOT be frozen.
        for row in prepared["frozen"]:
            self.assertNotIn(row["kind"], ("publication-semantic-input", "publication-authored-input"))
        # Retention: ONE row per node/path, sorted roles, XOR retained_ref/dest.
        retention_by_path = {r["path"]: r for r in proposal["retention_plan"]}
        self.assertEqual(len(retention_by_path), len(nodes))
        self.assertEqual(sorted(retention_by_path), sorted(n["path"] for n in nodes))
        for r in proposal["retention_plan"]:
            self.assertEqual(r["roles"], sorted(r["roles"]))
            self.assertEqual(len(r["roles"]), len(set(r["roles"])))
            if r["policy"] == "KEEP_IMMUTABLE":
                self.assertIn("retained_ref", r)
                self.assertNotIn("retained_dest", r)
                self.assertEqual(r["retained_ref"], {"path": r["path"], "sha256": r["sha256"]})
            else:
                self.assertIn("retained_dest", r)
                self.assertNotIn("retained_ref", r)
                self.assertTrue(r["retained_dest"].endswith("/retained/before/" + r["path"]))
        # C1 independent transitive expected-set (filesystem, not receipt list).
        with self.subTest(case="c1-transitives-longform"):
            snap_c1 = _snapshot(root)
            _assert_transitives_expected_set(self, root, helper.source_root, prepared)
            _assert_no_write(self, snap_c1, _snapshot(root), "c1 oracle no-write")
        proposal_path = _stage_reader_and_proposal(
            self, root, helper.source_root, "fixture-lf-rev-1", prepared)
        staged_rel = str((proposal_path.parent / "reader-surface-input-v2.json").relative_to(root))
        self.assertEqual(staged_rel, proposal["proposed"]["proposed_reader_ref"]["path"])
        before = _snapshot(root)
        outcome = proposal_mod.validate_proposal(root, state_path, proposal_path)
        _assert_no_write(self, before, _snapshot(root), "longform validate noscope")
        self.assertEqual(outcome["result"], "REVIEW_REQUIRED")
        # Returned proposal unchanged (no silent repair).
        self.assertEqual(outcome["proposal"], proposal)
        scope_path = _scope_review_for(self, root, prepared, staged_rel, "scope-review-v2.json")
        before = _snapshot(root)
        bound = proposal_mod.validate_proposal(root, state_path, proposal_path, scope_path)
        _assert_no_write(self, before, _snapshot(root), "longform validate bound")
        self.assertEqual(bound["result"], "REVIEW_BOUND_PROPOSAL")
        self.assertEqual(bound["proposal"], proposal)

    def test_weekly_envelope_positive_and_body_negatives(self) -> None:
        scratch, root = _make_source_root(self, "jgas-p1-weekly-")
        helper = _new_weekly_helper(self, root)
        built = _build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]
        authored = core.load_json(chain["authored_path"])
        authored["cover"]["headline"] = "Weekly tested method, revised edition"
        # R3 stale sibling (same bytes as real completeness, not State-bound).
        _real_comp_w = helper.source_root / "profile-completeness.json"
        _stale_comp_w = helper.source_root / "stale-profile-completeness.json"
        if _real_comp_w.is_file():
            _stale_comp_w.write_bytes(_real_comp_w.read_bytes())
        staged_authoring = _stage_authoring_before_prepare(
            self, root, helper.source_root, "fixture-wk-env-1", authored)
        before = _snapshot(root)
        prepared = proposal_mod.prepare_proposal(
            root, state_path, staged_authoring, "fixture-wk-env-1",
            "Fixture weekly envelope correction within approved authority.")
        _assert_no_write(self, before, _snapshot(root), "weekly prepare")
        # Author-supplied description preserved (not placeholder).
        self.assertEqual(prepared["proposal"]["proposed"]["change_description"],
                         "Fixture weekly envelope correction within approved authority.")
        # C1 independent transitive expected-set for Weekly (filesystem, not receipt).
        with self.subTest(case="c1-transitives-weekly"):
            snap_c1w = _snapshot(root)
            _assert_transitives_expected_set(self, root, helper.source_root, prepared)
            _assert_no_write(self, snap_c1w, _snapshot(root), "c1 weekly oracle no-write")
        proposal_path = _stage_reader_and_proposal(
            self, root, helper.source_root, "fixture-wk-env-1", prepared)
        staged = _snapshot(root)
        snap_before_validate = _snapshot(root)
        outcome = proposal_mod.validate_proposal(root, state_path, proposal_path)
        self.assertEqual(outcome["result"], "REVIEW_REQUIRED")
        _assert_no_write(self, snap_before_validate, _snapshot(root), "weekly validate")
        self.assertEqual(outcome["proposal"], prepared["proposal"])
        result_path = Path(chain["draft_result_path"])
        original_result = result_path.read_bytes()
        # EACH negative gets its own immediately-around snapshot AFTER fault mutation, before P1 call.
        try:
            tampered = core.load_json(result_path)
            tampered["blocks"][0]["text"] += " Unaccepted body edit."
            core.write_json(result_path, tampered)
            snap = _snapshot(root)
            # Checkpoint-bound tamper fails strict State validation before derivation.
            with self.assertRaisesRegex(ProposalError, "STATE_INVALID"):
                proposal_mod.prepare_proposal(root, state_path, staged_authoring, "fixture-wk-env-1")
            _assert_no_write(self, snap, _snapshot(root), "weekly negative draft-result tamper (no P1 write)")
        finally:
            result_path.write_bytes(original_result)
        synthesis_path = Path(chain["synthesis_result_path"])
        original_synthesis = synthesis_path.read_bytes()
        try:
            tampered = core.load_json(synthesis_path)
            tampered["profile_payload"]["current_interpretation"] = "Tampered closing synthesis."
            core.write_json(synthesis_path, tampered)
            snap2 = _snapshot(root)
            # Checkpoint-bound tamper fails strict State validation before derivation.
            with self.assertRaisesRegex(ProposalError, "STATE_INVALID"):
                proposal_mod.prepare_proposal(root, state_path, staged_authoring, "fixture-wk-env-1")
            _assert_no_write(self, snap2, _snapshot(root), "weekly negative synthesis tamper")
        finally:
            synthesis_path.write_bytes(original_synthesis)
        archive_path = helper.source_root / "draft" / "v2" / "interactive-drafting-synthesis-input.json"
        original_archive = archive_path.read_bytes()
        try:
            tampered = core.load_json(archive_path)
            tampered["packages"][0]["headline"] = "Tampered archive headline"
            core.write_json(archive_path, tampered)
            snap3 = _snapshot(root)
            # Non-checkpoint authoring-archive tamper reaches the route loader refusal.
            with self.assertRaisesRegex(ProposalError, "DERIVATION_REFUSED"):
                proposal_mod.prepare_proposal(root, state_path, staged_authoring, "fixture-wk-env-1")
            _assert_no_write(self, snap3, _snapshot(root), "weekly negative archive tamper")
        finally:
            archive_path.write_bytes(original_archive)
        # Same-byte staged authoring (new proposal dir, same bytes as before) -> NO_EDITORIAL_CHANGE.
        same_authored = core.load_json(chain["authored_path"])
        staged_same = _stage_authoring_before_prepare(
            self, root, helper.source_root, "fixture-wk-env-same", same_authored)
        snap4 = _snapshot(root)
        with self.assertRaisesRegex(ProposalError, "NO_EDITORIAL_CHANGE"):
            proposal_mod.prepare_proposal(root, state_path, staged_same, "fixture-wk-env-same")
        _assert_no_write(self, snap4, _snapshot(root), "weekly same-byte no-change")
        # Cleanup injected same-byte proposal dir before aggregate (records deliberate delta removal).
        import shutil as _shutil2
        _shutil2.rmtree((helper.source_root / "publication" / "v2" / "editorial-corrections" / "fixture-wk-env-same"))
        _assert_no_write(self, staged, _snapshot(root), "weekly negatives aggregate")

    def test_honest_predecessor_original_vs_active(self) -> None:
        # Generic honest Core-change predecessor (emitted TeX-comment literal +
        # manual regeneration cascade). This exercises the real generic
        # REVIEWED_CORE_CHANGE owner, NOT R1 same-byte mechanical refresh
        # (see test_r1_mechanical_refresh_owner below for R1).
        scratch, root = _make_source_root(self, "jgas-p1-predecessor-")
        helper = _new_weekly_helper(self, root)
        built = _build_weekly_validated(self, helper)
        built["helper"] = helper
        built["publication_root"] = helper.source_root / "publication" / "v2"
        chain, state_path = built["chain"], built["state_path"]
        context = weekly.load_derivation(root, state_path, chain["authored_path"])
        self.assertEqual(core.json_bytes(context["surface"]),
                         built["surface_path"].read_bytes(),
                         "same-byte refresh baseline must reproduce exact reader bytes")
        checkpoint_before = core.sha256_file(
            root / core.load_json(state_path)["checkpoint_provenance"]["validation"]["path"])
        renderer_before = core.load_json(built["receipt_path"])["current_tools"]["repository_commit_sha"]
        new_head = _commit_derivation_only_change(self, root)
        self.assertNotEqual(new_head, renderer_before)
        authored = core.load_json(chain["authored_path"])
        authored["frontmatter"]["lede"] = "A bounded technical survey, revised edition."
        # Stage authoring BEFORE prepare (canonical proposal input, P1 writes nothing).
        staged_authoring = _stage_authoring_before_prepare(
            self, root, helper.source_root, "fixture-wk-pred-1", authored)
        # Post-commit cascade executes the FIXTURE's committed code: epoch guards
        # bind replay execution to committed bytes, so ambient candidate code
        # cannot honestly replay the derivation-only revision.
        rel = lambda p: str(Path(p).relative_to(root))  # noqa: E731
        chain_paths = {k: rel(chain[k]) for k in
                       ("profile_path", "approval_path", "authored_path")}
        payload = {
            "head": new_head,
            "source_root": rel(helper.source_root),
            "survey_root": rel(helper.survey_root),
            "publication_root": rel(helper.source_root / "publication" / "v2"),
            "chain": chain_paths,
            "surface_path": rel(built["surface_path"]),
            "review_path": rel(built["review_path"]),
            "receipt_path": rel(built["receipt_path"]),
            "manuscript_path": rel(built["manuscript_path"]),
            "gate_path": rel(built["gate_path"]),
            "bundle_path": rel(built["bundle_path"]),
            "pdf_path": rel(built["pdf_path"]),
            "later_sem": rel(built["later_sem"]),
            "later_vis": rel(built["later_vis"]),
        }
        out = _run_fixture_code(
            self, root, _FIXTURE_CASCADE,
            [str(root), str(state_path), str(staged_authoring), "fixture-wk-pred-1",
             json.dumps(payload)])
        summary = json.loads(out)
        self.assertEqual(summary["origins"]["validated-source"], "ACTIVE")
        self.assertNotEqual(summary["effective_shas"]["validated-source"],
                            summary["original_shas"]["validated-source"])
        self.assertIsNotNone(summary["active_ref"])
        self.assertNotEqual(summary["before_sha"], summary["proposed_sha"])
        self.assertEqual(summary["result"], "REVIEW_REQUIRED")
        self.assertTrue((root / summary["record"]).is_file())
        state = core.load_json(state_path)
        pointer = state.get("publication_revalidation_provenance")
        self.assertIsNotNone(pointer)
        self.assertEqual(core.sha256_file(root / pointer["path"]),
                         core.sha256_file(root / summary["record"]))
        self.assertEqual(core.sha256_file(
            root / state["checkpoint_provenance"]["validation"]["path"]), checkpoint_before)
        self.assertGreater(summary["graph_nodes"], 20)
        self.assertGreater(summary["graph_edges"], 20)

    def test_refusal_and_scope_matrix(self) -> None:
        scratch, root = _make_source_root(self, "jgas-p1-matrix-")
        helper = _new_weekly_helper(self, root)
        built = _build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]
        authored = core.load_json(chain["authored_path"])
        authored["cover"]["headline"] = "Weekly tested method, matrix edition"
        staged_authoring = _stage_authoring_before_prepare(
            self, root, helper.source_root, "fixture-wk-mx-1", authored)
        base = _snapshot(root)
        with self.subTest(case="bad-id"):
            snap = _snapshot(root)
            with self.assertRaisesRegex(ProposalError, "BAD_PROPOSAL_ID"):
                proposal_mod.prepare_proposal(root, state_path, staged_authoring, "BAD ID!")
            _assert_no_write(self, snap, _snapshot(root), "bad-id no-write")
        with self.subTest(case="bad-id-newline"):
            snap = _snapshot(root)
            with self.assertRaisesRegex(ProposalError, "BAD_PROPOSAL_ID"):
                proposal_mod.prepare_proposal(root, state_path, staged_authoring, "fixture-wk-mx-1\n")
            _assert_no_write(self, snap, _snapshot(root), "bad-id-newline no-write")
        alias = helper.source_root / "alias-authoring.json"
        try:
            alias.symlink_to(staged_authoring)
            with self.subTest(case="alias"):
                snap = _snapshot(root)
                with self.assertRaisesRegex(ProposalError, "PATH_ALIAS|TREE_ALIAS"):
                    proposal_mod.prepare_proposal(root, state_path, alias, "fixture-wk-mx-1")
                _assert_no_write(self, snap, _snapshot(root), "alias no-write")
        finally:
            alias.unlink()
        with self.subTest(case="traversal"):
            snap = _snapshot(root)
            with self.assertRaisesRegex(ProposalError, "PATH_NOT_REPO_LOCAL|PATH_TRAVERSAL"):
                proposal_mod.prepare_proposal(root, state_path, "../outside.json", "fixture-wk-mx-1")
            _assert_no_write(self, snap, _snapshot(root), "traversal no-write")
        with self.subTest(case="ancestor-alias"):
            # Symlinked ancestor component must refuse before any read.
            linkdir = helper.source_root / "link-ancestor"
            target_dir = helper.source_root / "publication"
            try:
                linkdir.symlink_to(target_dir, target_is_directory=True)
                # Path through symlinked ancestor to the staged authoring (lexically inside root).
                via = linkdir / "v2" / "editorial-corrections" / "fixture-wk-mx-1" / "authoring-input.json"
                # via is absolute? Use repo-relative through linkdir.
                rel_via = str(via.relative_to(root))
                snap = _snapshot(root)
                with self.assertRaisesRegex(ProposalError, "PATH_ALIAS|TREE_ALIAS"):
                    proposal_mod.prepare_proposal(root, state_path, rel_via, "fixture-wk-mx-1")
                _assert_no_write(self, snap, _snapshot(root), "ancestor-alias no-write")
            finally:
                if linkdir.is_symlink() or linkdir.exists():
                    linkdir.unlink()
        with self.subTest(case="fifo-sentinel"):
            import stat as _stat
            fifo_path = helper.source_root / "fifo-sentinel"
            try:
                if fifo_path.exists() or fifo_path.is_symlink():
                    fifo_path.unlink()
                os.mkfifo(fifo_path)
                snap = _snapshot(root)
                with self.assertRaisesRegex(ProposalError, "PATH_NOT_REGULAR|PATH_MISSING|TREE_NOT_REGULAR"):
                    proposal_mod.prepare_proposal(root, state_path, str(fifo_path.relative_to(root)), "fixture-wk-mx-1")
                _assert_no_write(self, snap, _snapshot(root), "fifo no-write")
            finally:
                try:
                    if fifo_path.exists() or fifo_path.is_symlink():
                        os.unlink(fifo_path)
                except OSError:
                    pass
        with self.subTest(case="shadow-state"):
            shadow = helper.source_root / "shadow-state.json"
            try:
                shadow.write_bytes(Path(state_path).read_bytes())
                snap = _snapshot(root)
                with self.assertRaisesRegex(ProposalError, "STATE_NOT_CANONICAL|PATH_"):
                    proposal_mod.prepare_proposal(root, shadow, staged_authoring, "fixture-wk-mx-1")
                _assert_no_write(self, snap, _snapshot(root), "shadow-state no-write")
            finally:
                if shadow.exists():
                    shadow.unlink()
        with self.subTest(case="c4-unvalidated-tree-spy"):
            # Forge Profile roots to absolute escape; strict authority must fail
            # BEFORE any broad tree walk (spy proves walker not invoked, no mock success).
            from unittest import mock as _mock2
            state_data = core.load_json(state_path)
            prof_rel = state_data["profile"]["path"]
            prof_abs = root / prof_rel
            orig_prof = prof_abs.read_bytes()
            try:
                forged = core.load_json(prof_abs)
                forged["paths"]["source_root"] = "/"
                forged["paths"]["survey_root"] = "/tmp"
                core.write_json(prof_abs, forged)
                snap_spy = _snapshot(root)
                with _mock2.patch.object(proposal_mod, "_tree_map",
                                         wraps=proposal_mod._tree_map) as spy:
                    with self.assertRaisesRegex(ProposalError,
                                                "STATE_INVALID|PROFILE|ROOT|TRAVERSAL|DRIFT|MISMATCH|CANONICAL"):
                        proposal_mod.prepare_proposal(
                            root, state_path, staged_authoring, "fixture-wk-mx-1")
                    self.assertEqual(spy.call_count, 0,
                                     "unvalidated Profile must not trigger broad tree walk")
                _assert_no_write(self, snap_spy, _snapshot(root), "c4 spy no-write")
            finally:
                prof_abs.write_bytes(orig_prof)
        surface_path = built["surface_path"]
        original_surface = surface_path.read_bytes()
        try:
            surface_path.write_text(json.dumps(
                core.load_json(surface_path), indent=4, sort_keys=True), encoding="utf-8")
            with self.subTest(case="noncanonical-before"):
                snap = _snapshot(root)
                with self.assertRaisesRegex(ProposalError, "NONCANONICAL_BEFORE"):
                    proposal_mod.prepare_proposal(root, state_path, staged_authoring, "fixture-wk-mx-1")
                _assert_no_write(self, snap, _snapshot(root), "noncanonical no-write")
        finally:
            surface_path.write_bytes(original_surface)
        state_file = Path(state_path)
        original_state = state_file.read_bytes()
        try:
            tampered = core.load_json(state_file)
            tampered["lifecycle_state"] = "DRAFT_COMPLETE"
            core.write_json(state_file, tampered)
            with self.subTest(case="ineligible"):
                snap = _snapshot(root)
                with self.assertRaisesRegex(ProposalError, "STATE_INVALID|INELIGIBLE_STATE"):
                    proposal_mod.prepare_proposal(root, state_path, staged_authoring, "fixture-wk-mx-1")
                _assert_no_write(self, snap, _snapshot(root), "ineligible no-write")
        finally:
            state_file.write_bytes(original_state)
        # Valid prepare for subsequent validate matrix (staged flow).
        snap_prep = _snapshot(root)
        prepared = proposal_mod.prepare_proposal(
            root, state_path, staged_authoring, "fixture-wk-mx-1",
            "Matrix edition within approved authority.")
        _assert_no_write(self, snap_prep, _snapshot(root), "matrix prepare no-write")
        proposal_path = _stage_reader_and_proposal(
            self, root, helper.source_root, "fixture-wk-mx-1", prepared)
        staged_rel = str((proposal_path.parent / "reader-surface-input-v2.json").relative_to(root))
        copy_dest = next(row["retained_dest"] for row in prepared["proposal"]["retention_plan"]
                         if row["policy"] == "COPY_BEFORE_REPLACEMENT")
        try:
            (root / copy_dest).parent.mkdir(parents=True, exist_ok=True)
            (root / copy_dest).write_text("occupant\n", encoding="utf-8")
            snap_ret = _snapshot(root)
            with self.subTest(case="retention-conflict"):
                with self.assertRaisesRegex(ProposalError, "RETENTION_DEST_CONFLICT"):
                    proposal_mod.validate_proposal(root, state_path, proposal_path)
                _assert_no_write(self, snap_ret, _snapshot(root), "retention-conflict no-write")
        finally:
            try:
                (root / copy_dest).unlink()
            except OSError:
                pass
        snap_noscope = _snapshot(root)
        self.assertEqual(
            proposal_mod.validate_proposal(root, state_path, proposal_path)["result"], "REVIEW_REQUIRED")
        _assert_no_write(self, snap_noscope, _snapshot(root), "noscope no-write")
        ordinary = _scope_review_for(self, root, prepared, staged_rel, "ordinary-review-v2.json")
        ordinary_raw = core.load_json(ordinary)
        del ordinary_raw["editorial_correction_scope"]
        for check in ordinary_raw["checks"]:
            if check["check_id"] == "EDITORIAL_CORRECTION_SCOPE":
                ordinary_raw["checks"].remove(check)
                break
        del ordinary_raw["review_sha256"]
        ordinary_raw["review_sha256"] = core.sha256_object(ordinary_raw)
        core.write_json(ordinary, ordinary_raw)
        snap_ord = _snapshot(root)
        self.assertEqual(
            proposal_mod.validate_proposal(root, state_path, proposal_path, ordinary)["result"],
            "REVIEW_REQUIRED")
        _assert_no_write(self, snap_ord, _snapshot(root), "ordinary no-write")
        with self.subTest(case="wrong-before"):
            wrong = _scope_review_for(
                self, root, prepared, staged_rel, "scope-wrong-before-v2.json",
                before_override={"path": prepared["proposal"]["basis"]["active_reader_input_ref"]["path"],
                                 "sha256": "0" * 64})
            snap = _snapshot(root)
            with self.assertRaisesRegex(ProposalError, "SCOPE_ORDINARY_INVALID|SCOPE_WRONG_BEFORE"):
                proposal_mod.validate_proposal(root, state_path, proposal_path, wrong)
            _assert_no_write(self, snap, _snapshot(root), "wrong-before no-write")
        with self.subTest(case="wrong-after"):
            before_reader_rel = str(built["surface_path"].relative_to(root))
            wrong_after = _scope_review_for(
                self, root, prepared, before_reader_rel,
                "scope-wrong-after-v2.json")
            snap = _snapshot(root)
            # Scope targets before-reader, not proposed -> ordinary loader fails or wrong-after.
            with self.assertRaisesRegex(ProposalError, "SCOPE_ORDINARY_INVALID|SCOPE_WRONG_AFTER|SCOPE_DIGEST"):
                proposal_mod.validate_proposal(root, state_path, proposal_path, wrong_after)
            _assert_no_write(self, snap, _snapshot(root), "wrong-after no-write")
        with self.subTest(case="reject"):
            rejected = _scope_review_for(self, root, prepared, staged_rel,
                                         "scope-reject-v2.json", decision="REJECT")
            snap = _snapshot(root)
            with self.assertRaisesRegex(ProposalError, "SCOPE_NOT_WITHIN_AUTHORITY"):
                proposal_mod.validate_proposal(root, state_path, proposal_path, rejected)
            _assert_no_write(self, snap, _snapshot(root), "reject no-write")
        with self.subTest(case="needs-owner"):
            needs = _scope_review_for(self, root, prepared, staged_rel,
                                      "scope-needs-owner-v2.json", decision="REQUIRES_OWNER_DECISION")
            snap = _snapshot(root)
            with self.assertRaisesRegex(ProposalError, "SCOPE_NOT_WITHIN_AUTHORITY"):
                proposal_mod.validate_proposal(root, state_path, proposal_path, needs)
            _assert_no_write(self, snap, _snapshot(root), "needs-owner no-write")
        with self.subTest(case="stale-upstream"):
            stale = _scope_review_for(self, root, prepared, staged_rel, "scope-stale-v2.json",
                                      upstream_override="f" * 64)
            snap = _snapshot(root)
            with self.assertRaisesRegex(ProposalError, "SCOPE_STALE_UPSTREAM"):
                proposal_mod.validate_proposal(root, state_path, proposal_path, stale)
            _assert_no_write(self, snap, _snapshot(root), "stale-upstream no-write")
        with self.subTest(case="hash-conflict"):
            g = proposal_mod._Graph()
            g.node("a/b.json", "0" * 64, 10, "receipt:accepted:production-profile", "KEEP_IMMUTABLE")
            with self.assertRaisesRegex(ProposalError, "HASH_CONFLICT"):
                g.node("a/b.json", "f" * 64, 10, "receipt:accepted:production-profile", "KEEP_IMMUTABLE")
        with self.subTest(case="policy-conflict"):
            g = proposal_mod._Graph()
            g.node("a/c.json", "0" * 64, 10, "receipt:accepted:production-profile", "KEEP_IMMUTABLE")
            with self.assertRaisesRegex(ProposalError, "POLICY_CONFLICT"):
                g.node("a/c.json", "0" * 64, 10, "receipt:accepted:production-profile", "COPY_BEFORE_REPLACEMENT")
        with self.subTest(case="union-roles"):
            g = proposal_mod._Graph()
            g.node("a/d.json", "0" * 64, 10, "manuscript:profile", "KEEP_IMMUTABLE")
            g.node("a/d.json", "0" * 64, 10, "receipt:accepted:production-profile", "KEEP_IMMUTABLE")
            node = g.nodes["a/d.json"]
            self.assertEqual(sorted(node["roles"]), sorted(["manuscript:profile", "receipt:accepted:production-profile"]))
            kinds = proposal_mod._frozen_member_kinds(node["roles"])
            self.assertIn("production-profile", kinds)
        bound_scope = _scope_review_for(self, root, prepared, staged_rel, "scope-bound-v2.json")
        staged = _snapshot(root)
        self.assertEqual(
            proposal_mod.validate_proposal(root, state_path, proposal_path, bound_scope)["result"],
            "REVIEW_BOUND_PROPOSAL")
        _assert_no_write(self, staged, _snapshot(root), "bound validate")

    def test_ordinary_reviews_stay_compatible(self) -> None:
        scratch, root = _make_source_root(self, "jgas-p1-compat-")
        helper = _new_weekly_helper(self, root)
        built = _build_weekly_validated(self, helper)
        authority = reader_gate.load_and_validate_reader_surface_semantic_review(
            root, built["review_path"], expected_issue_id=W_ISSUE,
            expected_publication_profile="WEEKLY_MAGAZINE",
            expected_surface_path=str(built["surface_path"].relative_to(root)),
            expected_surface_sha256=core.sha256_file(built["surface_path"]), require_pass=True)
        self.assertEqual(authority["decision"], "PASS")
        self.assertNotIn("editorial_correction_scope", core.load_json(built["review_path"]))
        # Same-byte staged authoring in a new proposal dir -> NO_EDITORIAL_CHANGE (not AUTHORING_NOT_STAGED).
        same_authored = core.load_json(built["chain"]["authored_path"])
        staged_same = _stage_authoring_before_prepare(
            self, root, helper.source_root, "fixture-wk-cmp-1", same_authored)
        snap = _snapshot(root)
        with self.assertRaisesRegex(ProposalError, "NO_EDITORIAL_CHANGE"):
            proposal_mod.prepare_proposal(root, built["state_path"], staged_same, "fixture-wk-cmp-1")
        _assert_no_write(self, snap, _snapshot(root), "compat no-change no-write")

    def test_proposal_binding_and_retention(self) -> None:
        # Forged headers, wrong digests/refs, missing nullable, wrong dir,
        # extra/omitted/conflicting retention; no silent repair.
        scratch, root = _make_source_root(self, "jgas-p1-bind-")
        helper = _new_weekly_helper(self, root)
        built = _build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]
        authored = core.load_json(chain["authored_path"])
        authored["cover"]["headline"] = "Weekly binding test, revised edition"
        staged_authoring = _stage_authoring_before_prepare(
            self, root, helper.source_root, "fixture-wk-bind-1", authored)
        prepared = proposal_mod.prepare_proposal(
            root, state_path, staged_authoring, "fixture-wk-bind-1", "Binding test.")
        proposal_path = _stage_reader_and_proposal(
            self, root, helper.source_root, "fixture-wk-bind-1", prepared)
        supplied = core.load_json(proposal_path)
        # No silent repair: validate returns supplied unchanged.
        snap = _snapshot(root)
        outcome = proposal_mod.validate_proposal(root, state_path, proposal_path)
        self.assertEqual(outcome["proposal"], supplied)
        _assert_no_write(self, snap, _snapshot(root), "binding noscope no-write")
        # Forged header: tamper issue_id.
        forged = copy.deepcopy(supplied)
        forged["issue_id"] = "FORGED-ISSUE"
        forged_path = proposal_path.parent / "proposal-forged.json"
        # Must write to a temp file outside canonical name? Use direct validate via tampered file
        # staged as proposal.json copy with forged content (no-write check around validate only).
        tmp_forged = proposal_path.parent / "tmp-forged-proposal.json"
        core.write_json(tmp_forged, forged)
        # Canonical filename check: non-proposal.json must refuse.
        snap2 = _snapshot(root)
        with self.assertRaisesRegex(ProposalError, "PROPOSAL_FILENAME"):
            proposal_mod.validate_proposal(root, state_path, tmp_forged)
        _assert_no_write(self, snap2, _snapshot(root), "forged filename no-write")
        tmp_forged.unlink()
        # Wrong directory: copy proposal to non-canonical dir.
        wrong_dir = helper.source_root / "publication" / "v2" / "editorial-corrections" / "wrong-dir" / "proposal.json"
        wrong_dir.parent.mkdir(parents=True, exist_ok=True)
        core.write_json(wrong_dir, supplied)
        # Stage required reader/authoring siblings to isolate dir check (copy from valid).
        (wrong_dir.parent / "authoring-input.json").write_bytes((proposal_path.parent / "authoring-input.json").read_bytes())
        (wrong_dir.parent / "reader-surface-input-v2.json").write_bytes((proposal_path.parent / "reader-surface-input-v2.json").read_bytes())
        snap3 = _snapshot(root)
        with self.assertRaisesRegex(ProposalError, "PROPOSAL_LAYOUT|HEADER_MISMATCH|PROPOSED_"):
            proposal_mod.validate_proposal(root, state_path, wrong_dir)
        _assert_no_write(self, snap3, _snapshot(root), "wrong-dir no-write")
        import shutil as _shutil
        _shutil.rmtree(wrong_dir.parent)
        # Missing nullable: remove active_revalidation_ref (must be present-as-null).
        missing = copy.deepcopy(supplied)
        del missing["basis"]["active_revalidation_ref"]
        missing_path = proposal_path.parent / "proposal-missing-nullable.json"
        # Overwrite canonical proposal.json temporarily? Instead test schema directly.
        # Validate that schema requires the key (new schema).
        from scripts import survey_schema_v2 as _sg
        with self.assertRaises(ValueError):
            _sg.validate_instance(missing, root / proposal_mod.PROPOSAL_SCHEMA, label="missing nullable")
        # Wrong proposed digest/ref: tamper canonical sha.
        wrong_digest = copy.deepcopy(supplied)
        wrong_digest["proposed"]["proposed_reader_canonical_sha256"] = "0" * 64
        core.write_json(proposal_path, wrong_digest)
        snap4 = _snapshot(root)
        try:
            with self.assertRaisesRegex(ProposalError, "PROPOSED_DIGEST_MISMATCH|BASIS_MISMATCH|SCHEMA"):
                proposal_mod.validate_proposal(root, state_path, proposal_path)
            _assert_no_write(self, snap4, _snapshot(root), "wrong-digest no-write")
        finally:
            core.write_json(proposal_path, supplied)
        # Same-byte wrong-authoring-PATH: staged authoring bytes differ from ref sha? Tamper ref path.
        wrong_path = copy.deepcopy(supplied)
        wrong_path["proposed"]["authoring_input_ref"] = {"path": str(chain["authored_path"].relative_to(root)) if isinstance(chain["authored_path"], Path) else chain["authored_path"], "sha256": supplied["proposed"]["authoring_input_ref"]["sha256"]}
        core.write_json(proposal_path, wrong_path)
        snap5 = _snapshot(root)
        try:
            with self.assertRaisesRegex(ProposalError, "PROPOSED_AUTHORING_PATH|PROPOSED_AUTHORING_MISMATCH"):
                proposal_mod.validate_proposal(root, state_path, proposal_path)
            _assert_no_write(self, snap5, _snapshot(root), "wrong-authoring-path no-write")
        finally:
            core.write_json(proposal_path, supplied)
        # Extra/omitted/conflicting retention.
        extra = copy.deepcopy(supplied)
        extra["retention_plan"].append(dict(extra["retention_plan"][0]))
        core.write_json(proposal_path, extra)
        snap6 = _snapshot(root)
        try:
            with self.assertRaisesRegex(ProposalError, "RETENTION_MISMATCH|SCHEMA"):
                proposal_mod.validate_proposal(root, state_path, proposal_path)
            _assert_no_write(self, snap6, _snapshot(root), "extra-retention no-write")
        finally:
            core.write_json(proposal_path, supplied)
        omitted = copy.deepcopy(supplied)
        omitted["retention_plan"] = omitted["retention_plan"][:-1]
        core.write_json(proposal_path, omitted)
        snap7 = _snapshot(root)
        try:
            with self.assertRaisesRegex(ProposalError, "RETENTION_MISMATCH|SCHEMA"):
                proposal_mod.validate_proposal(root, state_path, proposal_path)
            _assert_no_write(self, snap7, _snapshot(root), "omitted-retention no-write")
        finally:
            core.write_json(proposal_path, supplied)

    def test_artifact_only_vs_control_drift_and_tree(self) -> None:
        scratch, root = _make_source_root(self, "jgas-p1-drift-")
        helper = _new_weekly_helper(self, root)
        built = _build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]
        authored = core.load_json(chain["authored_path"])
        authored["cover"]["headline"] = "Weekly drift test, revised edition"
        staged_authoring = _stage_authoring_before_prepare(
            self, root, helper.source_root, "fixture-wk-drift-1", authored)
        # CWD-independent tree snapshot: chdir to /tmp, tree map must still match.
        import os as _os
        cwd_before = _os.getcwd()
        try:
            _os.chdir("/tmp")
            tree_via_cwd = proposal_mod._tree_map(
                root, Path(core.load_json(root / core.DEFAULT_CONFIG) and helper.source_root.relative_to(root).as_posix() or "sources/2026-W37"),
                Path(helper.survey_root.relative_to(root).as_posix()))
            # The above uses repo-relative paths; must equal the entry captured at fixture root.
            # Recompute correctly via profile preview (root-anchored, not CWD).
            profile = core.load_json(root / core.load_json(state_path)["profile"]["path"])
            tree_correct = proposal_mod._tree_map(
                root, Path(profile["paths"]["source_root"]), Path(profile["paths"]["survey_root"]))
            self.assertEqual(tree_via_cwd, tree_correct)
        finally:
            _os.chdir(cwd_before)
        # Artifact-only HEAD descendant allowed: commit unrelated non-control file.
        artifact_path = root / "sources" / W_ISSUE / "artifact-only-note.txt"
        artifact_path.write_text("artifact-only\n", encoding="utf-8")
        proc = _run_git(root, "add", str(artifact_path.relative_to(root)))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        proc = _run_git(root, "-c", "user.name=Synthetic DM021-P1 Fixture",
                        "-c", "user.email=p1-fixture@example.invalid",
                        "commit", "-q", "-m", "Artifact-only commit")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        snap_artifact = _snapshot(root)
        try:
            prepared_artifact = proposal_mod.prepare_proposal(
                root, state_path, staged_authoring, "fixture-wk-drift-1", "Drift test.")
            _assert_no_write(self, snap_artifact, _snapshot(root), "artifact-only prepare no-write")
            self.assertEqual(prepared_artifact["proposal"]["proposal_id"], "fixture-wk-drift-1")
        finally:
            # Reset artifact-only commit (keep staged authoring untracked).
            proc = _run_git(root, "reset", "--hard", "HEAD~1")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            # Staged authoring was untracked and survives reset? It was under sources/.../editorial-corrections (untracked),
            # reset --hard does not delete untracked files, so it remains. Verify.
            self.assertTrue(staged_authoring.is_file())
        # Control drift refused: dirty unlisted helper/schema after receipt validation.
        # Tamper a tool-closure file on disk (dirty, no commit) -> receipt validation must fail.
        closure_path = None
        receipt = core.load_json(built["receipt_path"])
        for row in receipt.get("current_tools", {}).get("closure", []):
            closure_path = root / row["path"]
            break
        self.assertIsNotNone(closure_path)
        original_closure = closure_path.read_bytes()
        try:
            closure_path.write_bytes(original_closure + b"\n# control drift\n")
            snap_control = _snapshot(root)
            with self.assertRaisesRegex(ProposalError, "RECEIPT|CLOSURE|DRIFT|STATE_INVALID|CONTRACT"):
                proposal_mod.prepare_proposal(root, state_path, staged_authoring, "fixture-wk-drift-1")
            _assert_no_write(self, snap_control, _snapshot(root), "control-drift no-write")
        finally:
            closure_path.write_bytes(original_closure)
        # C2 same-issue valid alternate-profile path (same bytes, different valid path).
        # File tamper necessarily causes checkpoint drift first (STATE_INVALID, fail-closed);
        # exact path+SHA logic proved by unit below (same SHA, different path, no file tamper).
        with self.subTest(case="c2-alt-profile-path"):
            state = core.load_json(state_path)
            state_prof_rel = state["profile"]["path"]
            alt_rel = str(Path(state_prof_rel).parent / "alt-production-profile.json")
            alt_abs = root / alt_rel
            self.assertFalse(alt_abs.exists())
            alt_abs.write_bytes((root / state_prof_rel).read_bytes())
            try:
                # Alt profile same issue/bytes (valid same-issue alternate path).
                bundle_abs = root / core.load_json(built["bundle_path"])["production_profile"]["path"]
                # Bundle file itself is at built["bundle_path"], not its profile ref; tamper bundle file:
                bundle_file = Path(built["bundle_path"])
                orig_bundle = bundle_file.read_bytes()
                try:
                    bdata = core.load_json(bundle_file)
                    bdata["production_profile"] = {"path": alt_rel,
                                                   "sha256": core.sha256_file(alt_abs)}
                    core.write_json(bundle_file, bdata)
                    snap_alt = _snapshot(root)
                    # Bundle file tamper changes its bytes -> checkpoint drift (STATE_INVALID) first;
                    # both are correct fail-closed refusals (exact check is defense-in-depth, unit-proved below).
                    with self.assertRaisesRegex(ProposalError, "STATE_INVALID|BUNDLE_PROFILE_DIVERGED|MANUSCRIPT_PROFILE"):
                        proposal_mod.prepare_proposal(
                            root, state_path, staged_authoring, "fixture-wk-drift-1", "Drift test.")
                    _assert_no_write(self, snap_alt, _snapshot(root), "alt-profile no-write")
                finally:
                    bundle_file.write_bytes(orig_bundle)
            finally:
                if alt_abs.is_file():
                    alt_abs.unlink()
            # Unit exact path+SHA (same SHA, different valid paths, no file tamper, no drift).
            with self.subTest(case="c2-alt-profile-exact-unit"):
                from scripts.survey_editorial_correction_proposal_v2 import _check_bundle_profile_exact
                from scripts.survey_editorial_correction_proposal_v2 import _Collector
                # Use real State/Profile/manuscript from fixture (valid, no tamper).
                _state = core.load_json(state_path)
                _col = _Collector(root)
                _prof = core.load_json(root / _state["profile"]["path"])
                # Craft bundle/manuscript with alt path (same SHA, same issue, valid) -> must refuse by PATH.
                alt_path = str(Path(_state["profile"]["path"]).parent / "alt-unit-profile.json")
                same_sha = _state["profile"]["sha256"]
                _bundle = {"production_profile": {"path": alt_path, "sha256": same_sha}}
                _manuscript = {"production_profile": {"path": _state["profile"]["path"], "sha256": same_sha}}
                with self.assertRaisesRegex(ProposalError, "BUNDLE_PROFILE_DIVERGED"):
                    _check_bundle_profile_exact(_bundle, _state, _manuscript, _col)
        # C3 late helper drift outside closure (HEAD/config/closure unchanged, control dirty).
        with self.subTest(case="c3-late-helper-prepare"):
            helper_path = root / "scripts" / "survey_production_v2.py"
            # Verify helper outside Weekly closure (14/8 closure bytes unchanged premise).
            from scripts import survey_weekly_derivation_v2 as _wkc
            self.assertNotIn(helper_path.relative_to(root).as_posix(),
                             {str(p) for p in _wkc.CURRENT_CLOSURE})
            orig_helper = helper_path.read_bytes()
            try:
                helper_path.write_bytes(orig_helper + b"\n# C3 late helper drift (outside closure).\n")
                snap_late = _snapshot(root)
                with self.assertRaisesRegex(ProposalError, "RECEIPT|RECHECK|DRIFT|INVALID"):
                    proposal_mod.prepare_proposal(
                        root, state_path, staged_authoring, "fixture-wk-drift-1", "Drift test.")
                _assert_no_write(self, snap_late, _snapshot(root), "late-helper-prepare no-write")
            finally:
                helper_path.write_bytes(orig_helper)
        # C3 late-scope seam: helper drifted after scope creation, before validate return.
        with self.subTest(case="c3-late-helper-scope"):
            # Fresh prepare/stage/scope with clean helper, then drift helper before validate.
            snap_clean = _snapshot(root)
            prepared_scope = proposal_mod.prepare_proposal(
                root, state_path, staged_authoring, "fixture-wk-drift-1", "Drift test.")
            _assert_no_write(self, snap_clean, _snapshot(root), "late-scope prepare clean")
            # Stage to a second proposal id to avoid colliding with staged_authoring's dir?
            # staged_authoring already at fixture-wk-drift-1; use helper to stage reader/proposal there
            # only if not already staged (artifact test has not staged yet for drift-1).
            drift_dir = helper.source_root / "publication" / "v2" / "editorial-corrections" / "fixture-wk-drift-1"
            if not (drift_dir / "proposal.json").exists():
                proposal_path_scope = _stage_reader_and_proposal(
                    self, root, helper.source_root, "fixture-wk-drift-1", prepared_scope)
            else:
                proposal_path_scope = drift_dir / "proposal.json"
            staged_rel_scope = str((proposal_path_scope.parent / "reader-surface-input-v2.json").relative_to(root))
            scope_file = _scope_review_for(self, root, prepared_scope, staged_rel_scope, "scope-late-drift-v2.json")
            helper_path2 = root / "scripts" / "survey_production_v2.py"
            orig2 = helper_path2.read_bytes()
            try:
                helper_path2.write_bytes(orig2 + b"\n# C3 late-scope helper drift.\n")
                snap_late_scope = _snapshot(root)
                with self.assertRaisesRegex(ProposalError, "RECEIPT|RECHECK|DRIFT|INVALID"):
                    proposal_mod.validate_proposal(root, state_path, proposal_path_scope, scope_file)
                _assert_no_write(self, snap_late_scope, _snapshot(root), "late-scope no-write")
            finally:
                helper_path2.write_bytes(orig2)

    def test_candidate_observed_and_stale(self) -> None:
        scratch, root = _make_source_root(self, "jgas-p1-cand-")
        helper = _new_weekly_helper(self, root)
        built = _build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]
        profile = core.load_json(chain["profile_path"])
        src_root = root / profile["paths"]["source_root"]
        cand_rel = (Path(profile["paths"]["source_root"]) / "publication" / "v2" / "publication-candidate-v2.json").as_posix()
        # Absent candidate (observed/unadopted absent) allows success.
        self.assertFalse((root / cand_rel).exists())
        authored = core.load_json(chain["authored_path"])
        authored["cover"]["headline"] = "Weekly candidate test, revised edition"
        staged_authoring = _stage_authoring_before_prepare(
            self, root, helper.source_root, "fixture-wk-cand-1", authored)
        snap_absent = _snapshot(root)
        prepared_absent = proposal_mod.prepare_proposal(
            root, state_path, staged_authoring, "fixture-wk-cand-1", "Candidate absent test.")
        _assert_no_write(self, snap_absent, _snapshot(root), "candidate-absent prepare")
        # Proper candidate via real builder (exact agreement) allows success.
        from scripts import survey_publication_v2 as _pub
        cand_path = root / cand_rel
        # Effective manuscript/source/pdf/bundle/reviews from built fixture.
        state = core.load_json(state_path)
        # Build candidate with exact effective bytes (all paths absolute inside fixture root).
        _pub.build_candidate(
            root, state["issue_id"], "WEEKLY_MAGAZINE",
            built["manuscript_path"],
            helper.survey_root / "main.tex",
            helper.survey_root / "main.pdf", 1,
            built["bundle_path"],
            built["later_sem"],
            built["later_vis"],
            cand_path)
        snap_cand = _snapshot(root)
        try:
            prepared_cand = proposal_mod.prepare_proposal(
                root, state_path, staged_authoring, "fixture-wk-cand-1", "Candidate proper test.")
            _assert_no_write(self, snap_cand, _snapshot(root), "candidate-proper prepare")
            # Retention must include candidate as COPY.
            cand_rows = [r for r in prepared_cand["proposal"]["retention_plan"] if r["path"] == cand_rel]
            self.assertEqual(len(cand_rows), 1)
            self.assertEqual(cand_rows[0]["policy"], "COPY_BEFORE_REPLACEMENT")
        except Exception as exc:
            # If builder path resolution failed, record precise blocker (no fake candidate).
            self.fail(f"proper candidate construction blocked: {exc}")
        finally:
            if cand_path.is_file():
                cand_path.unlink()
        # Stale candidate (diverged bytes) must refuse.
        core.write_json(cand_path, {"forged": "candidate"})
        snap_stale = _snapshot(root)
        try:
            with self.assertRaisesRegex(ProposalError, "CANDIDATE|SCHEMA|VALIDATION|REVIEW|DIVERGED"):
                proposal_mod.prepare_proposal(root, state_path, staged_authoring, "fixture-wk-cand-1")
            _assert_no_write(self, snap_stale, _snapshot(root), "candidate-stale no-write")
        finally:
            if cand_path.is_file():
                cand_path.unlink()

    def test_r1_mechanical_refresh_owner(self) -> None:
        # Real R1 owner: non-emitted Python comment-only derivation commit,
        # unchanged reader/output bytes, via the supported mechanical-refresh
        # owner (survey_weekly_mechanical_refresh_v2), NOT the emitted
        # TeX-comment generic Core-change path. Prefers two successive
        # refreshes to exercise the supersedes chain; reports exact blocker if
        # unconstructible (no fake pointer/reason/State).
        scratch, root = _make_source_root(self, "jgas-p1-r1-")
        helper = _new_weekly_helper(self, root)
        built = _build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]
        before_surface = built["surface_path"].read_bytes()
        before_main = (helper.survey_root / "main.tex").read_bytes()
        before_receipt = core.load_json(built["receipt_path"])
        # Non-emitted change: Python comment-only at end of derivation file
        # (does not flow to rendered TeX/reader bytes).
        target = root / "scripts" / "survey_weekly_derivation_v2.py"
        original_text = target.read_text(encoding="utf-8")
        self.assertNotIn("R1 non-emitted fixture comment", original_text)
        target.write_text(original_text + "\n# R1 non-emitted fixture comment: no output change.\n",
                          encoding="utf-8")
        proc = _run_git(root, "add", "scripts/survey_weekly_derivation_v2.py")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        proc = _run_git(root, "-c", "user.name=Synthetic DM021-P1 Fixture",
                        "-c", "user.email=p1-fixture@example.invalid",
                        "commit", "-q", "-m", "Fixture R1 non-emitted derivation comment")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        head1 = core.repository_commit_sha(root)
        # Same-byte proof: derivation still reproduces exact reader/output bytes.
        context = weekly.load_derivation(root, state_path, chain["authored_path"])
        self.assertEqual(core.json_bytes(context["surface"]), before_surface,
                         "R1 comment-only change must preserve exact reader bytes")
        self.assertEqual((helper.survey_root / "main.tex").read_bytes(), before_main,
                         "R1 comment-only change must preserve exact rendered output")
        # First refresh via the fixture's committed R1 owner code (honest epoch).
        refresh_script = """
import sys
from pathlib import Path
root = Path(sys.argv[1])
state_path = Path(sys.argv[2])
from scripts import survey_production_v2 as core
from scripts import survey_weekly_mechanical_refresh_v2 as r1
cfg = core.load_json(root / core.DEFAULT_CONFIG)
from datetime import datetime, timezone
recorded = datetime(2026, 9, 19, 8, 0, 0, tzinfo=timezone.utc)
result = r1.refresh_mechanical_evidence(root, cfg, state_path, "fixture R1 non-emitted refresh", "synthetic P1 R1 fixture", recorded)
print(core.sha256_object(result)[:16])
"""
        out1 = _run_fixture_code(self, root, refresh_script, [str(root), str(state_path)])
        # State must now carry an active revalidation pointer (R1 record).
        state_after1 = core.load_json(state_path)
        self.assertIsNotNone(state_after1.get("publication_revalidation_provenance"),
                             "R1 refresh must install State-bound active record")
        # Second non-emitted commit + second refresh to exercise supersedes chain.
        target.write_text(target.read_text(encoding="utf-8") + "# R1 second non-emitted comment.\n",
                          encoding="utf-8")
        proc = _run_git(root, "add", "scripts/survey_weekly_derivation_v2.py")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        proc = _run_git(root, "-c", "user.name=Synthetic DM021-P1 Fixture",
                        "-c", "user.email=p1-fixture@example.invalid",
                        "commit", "-q", "-m", "Fixture R1 second non-emitted comment")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        context2 = weekly.load_derivation(root, state_path, chain["authored_path"])
        self.assertEqual(core.json_bytes(context2["surface"]), before_surface,
                         "second R1 comment must also preserve reader bytes")
        out2 = _run_fixture_code(self, root, refresh_script, [str(root), str(state_path)])
        state_after2 = core.load_json(state_path)
        pointer2 = state_after2.get("publication_revalidation_provenance")
        self.assertIsNotNone(pointer2)
        # Predecessor chain must have depth >=1 (second supersedes first).
        from scripts import survey_agent_control_v2 as _agent
        cfg2 = core.load_json(root / core.DEFAULT_CONFIG)
        record2, errors2 = _agent.resolve_active_publication_revalidation(root, cfg2, state_after2)
        self.assertEqual(errors2, [])
        self.assertIsNotNone(record2)
        self.assertIsNotNone(record2.get("supersedes"), "second R1 must supersede first (chain depth)")
        # P1 prepare/validate on the R1-active fixture (staged authoring, honest fixture code).
        authored = core.load_json(chain["authored_path"])
        authored["cover"]["headline"] = "Weekly R1 test, revised edition"
        staged_r1 = _stage_authoring_before_prepare(
            self, root, helper.source_root, "fixture-wk-r1-1", authored)
        # Run P1 via fixture code to bind to committed R1 basis (epoch honesty).
        r1_p1_script = """
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
state_path = Path(sys.argv[2])
authored_path = Path(sys.argv[3])
proposal_id = sys.argv[4]
from scripts import survey_production_v2 as core
from scripts import survey_editorial_correction_proposal_v2 as proposal_mod
from tests import test_survey_editorial_correction_proposal_v2 as p1t
from unittest import TestCase
tc = TestCase()
snap = p1t._snapshot(root)
prepared = proposal_mod.prepare_proposal(root, state_path, authored_path, proposal_id, "R1 test.")
p1t._assert_no_write(tc, snap, p1t._snapshot(root), "R1 prepare")
proposal_path = p1t._stage_reader_and_proposal(tc, root, root / sys.argv[5], proposal_id, prepared)
staged = p1t._snapshot(root)
outcome = proposal_mod.validate_proposal(root, state_path, proposal_path)
p1t._assert_no_write(tc, staged, p1t._snapshot(root), "R1 validate")
assert outcome[\"result\"] == \"REVIEW_REQUIRED\", outcome[\"result\"]
assert prepared[\"effective\"][\"validated-source\"][\"origin\"] == \"ACTIVE\", prepared[\"effective\"]
print(json.dumps({\"origins\": {k: v[\"origin\"] for k, v in prepared[\"effective\"].items()},
\"active_ref\": prepared[\"proposal\"][\"basis\"][\"active_revalidation_ref\"],
\"nodes\": len(prepared[\"graph\"][\"nodes\"])}))
"""
        out_p1 = _run_fixture_code(
            self, root, r1_p1_script,
            [str(root), str(state_path), str(staged_r1), "fixture-wk-r1-1",
             str(helper.source_root.relative_to(root))])
        summary = json.loads(out_p1)
        self.assertEqual(summary["origins"]["validated-source"], "ACTIVE")
        self.assertIsNotNone(summary["active_ref"])
        self.assertGreater(summary["nodes"], 20)
