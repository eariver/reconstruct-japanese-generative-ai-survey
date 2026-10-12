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
    files: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if ".git" in path.parts:
            continue
        if path.is_symlink() or not path.is_file():
            continue
        files[str(path.relative_to(root))] = core.sha256_file(path)
    head = _run_git(root, "rev-parse", "HEAD")
    status = _run_git(root, "status", "--porcelain")
    return {"files": files, "head": head.stdout, "status": status.stdout}


def _assert_no_write(testcase: unittest.TestCase, before: dict, after: dict, label: str) -> None:
    testcase.assertEqual(after["files"], before["files"], f"tree write during {label}")
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
    proposal_dir = source_root / "publication" / "v2" / "editorial-corrections" / proposal_id
    testcase.assertFalse(proposal_dir.exists())
    proposal_dir.mkdir(parents=True)
    (proposal_dir / "authoring-input.json").write_bytes(authored_bytes)
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
        new_authored_path = helper.source_root / "proposed-longform-authoring.json"
        core.write_json(new_authored_path, authored)
        before = _snapshot(root)
        prepared = proposal_mod.prepare_proposal(root, state_path, new_authored_path, "fixture-lf-rev-1")
        _assert_no_write(self, before, _snapshot(root), "longform prepare")
        proposal = prepared["proposal"]
        self.assertEqual(proposal["status"], "PROPOSED")
        self.assertEqual(proposal["route"], "EDITORIAL_CORRECTION_PROPOSAL_V1")
        self.assertIsNone(proposal["basis"]["active_revalidation_ref"])
        self.assertNotEqual(prepared["before_canonical"], prepared["proposed_canonical"])
        nodes = prepared["graph"]["nodes"]
        self.assertTrue(all(set(n) == {"path", "sha256", "byte_count", "roles", "policy"} for n in nodes))
        policies = {n["policy"] for n in nodes}
        self.assertEqual(policies, {"KEEP_IMMUTABLE", "COPY_BEFORE_REPLACEMENT"})
        self.assertTrue(all(r["policy"] in policies for r in proposal["retention_plan"]))
        frozen_kinds = {row["kind"] for row in prepared["frozen"]}
        self.assertIn("production-profile", frozen_kinds)
        self.assertIn("issue-architecture", frozen_kinds)
        proposal_path = _stage_proposal(self, root, helper.source_root, "fixture-lf-rev-1",
                                        prepared, new_authored_path.read_bytes())
        staged_rel = str((proposal_path.parent / "reader-surface-input-v2.json").relative_to(root))
        before = _snapshot(root)
        outcome = proposal_mod.validate_proposal(root, state_path, proposal_path)
        _assert_no_write(self, before, _snapshot(root), "longform validate noscope")
        self.assertEqual(outcome["result"], "REVIEW_REQUIRED")
        scope_path = _scope_review_for(self, root, prepared, staged_rel, "scope-review-v2.json")
        before = _snapshot(root)
        bound = proposal_mod.validate_proposal(root, state_path, proposal_path, scope_path)
        _assert_no_write(self, before, _snapshot(root), "longform validate bound")
        self.assertEqual(bound["result"], "REVIEW_BOUND_PROPOSAL")

    def test_weekly_envelope_positive_and_body_negatives(self) -> None:
        scratch, root = _make_source_root(self, "jgas-p1-weekly-")
        helper = _new_weekly_helper(self, root)
        built = _build_weekly_validated(self, helper)
        chain, state_path = built["chain"], built["state_path"]
        authored = core.load_json(chain["authored_path"])
        authored["cover"]["headline"] = "Weekly tested method, revised edition"
        new_authored_path = helper.source_root / "proposed-weekly-authoring.json"
        core.write_json(new_authored_path, authored)
        before = _snapshot(root)
        prepared = proposal_mod.prepare_proposal(root, state_path, new_authored_path, "fixture-wk-env-1")
        _assert_no_write(self, before, _snapshot(root), "weekly prepare")
        proposal_path = _stage_proposal(self, root, helper.source_root, "fixture-wk-env-1",
                                        prepared, new_authored_path.read_bytes())
        staged = _snapshot(root)
        outcome = proposal_mod.validate_proposal(root, state_path, proposal_path)
        self.assertEqual(outcome["result"], "REVIEW_REQUIRED")
        _assert_no_write(self, staged, _snapshot(root), "weekly validate")
        result_path = Path(chain["draft_result_path"])
        original_result = result_path.read_bytes()
        try:
            tampered = core.load_json(result_path)
            tampered["blocks"][0]["text"] += " Unaccepted body edit."
            core.write_json(result_path, tampered)
            # Checkpoint-bound tamper fails strict State validation before derivation.
            with self.assertRaisesRegex(ProposalError, "STATE_INVALID"):
                proposal_mod.prepare_proposal(root, state_path, new_authored_path, "fixture-wk-env-1")
        finally:
            result_path.write_bytes(original_result)
        synthesis_path = Path(chain["synthesis_result_path"])
        original_synthesis = synthesis_path.read_bytes()
        try:
            tampered = core.load_json(synthesis_path)
            tampered["profile_payload"]["current_interpretation"] = "Tampered closing synthesis."
            core.write_json(synthesis_path, tampered)
            # Checkpoint-bound tamper fails strict State validation before derivation.
            with self.assertRaisesRegex(ProposalError, "STATE_INVALID"):
                proposal_mod.prepare_proposal(root, state_path, new_authored_path, "fixture-wk-env-1")
        finally:
            synthesis_path.write_bytes(original_synthesis)
        archive_path = helper.source_root / "draft" / "v2" / "interactive-drafting-synthesis-input.json"
        original_archive = archive_path.read_bytes()
        try:
            tampered = core.load_json(archive_path)
            tampered["packages"][0]["headline"] = "Tampered archive headline"
            core.write_json(archive_path, tampered)
            # Non-checkpoint authoring-archive tamper reaches the route loader refusal.
            with self.assertRaisesRegex(ProposalError, "DERIVATION_REFUSED"):
                proposal_mod.prepare_proposal(root, state_path, new_authored_path, "fixture-wk-env-1")
        finally:
            archive_path.write_bytes(original_archive)
        with self.assertRaisesRegex(ProposalError, "NO_EDITORIAL_CHANGE"):
            proposal_mod.prepare_proposal(root, state_path, chain["authored_path"], "fixture-wk-env-1")
        _assert_no_write(self, staged, _snapshot(root), "weekly negatives")

    def test_honest_predecessor_original_vs_active(self) -> None:
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
        new_authored_path = helper.source_root / "proposed-weekly-authoring.json"
        core.write_json(new_authored_path, authored)
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
            [str(root), str(state_path), str(new_authored_path), "fixture-wk-pred-1",
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
        new_authored_path = helper.source_root / "proposed-weekly-authoring.json"
        core.write_json(new_authored_path, authored)
        base = _snapshot(root)
        with self.subTest(case="bad-id"):
            with self.assertRaisesRegex(ProposalError, "BAD_PROPOSAL_ID"):
                proposal_mod.prepare_proposal(root, state_path, new_authored_path, "BAD ID!")
        alias = helper.source_root / "alias-authoring.json"
        try:
            alias.symlink_to(new_authored_path)
            with self.subTest(case="alias"):
                with self.assertRaisesRegex(ProposalError, "PATH_ALIAS"):
                    proposal_mod.prepare_proposal(root, state_path, alias, "fixture-wk-mx-1")
        finally:
            alias.unlink()
        with self.subTest(case="traversal"):
            with self.assertRaisesRegex(ProposalError, "PATH_NOT_REPO_LOCAL|PATH_TRAVERSAL"):
                proposal_mod.prepare_proposal(root, state_path, "../outside.json", "fixture-wk-mx-1")
        surface_path = built["surface_path"]
        original_surface = surface_path.read_bytes()
        try:
            surface_path.write_text(json.dumps(
                core.load_json(surface_path), indent=4, sort_keys=True), encoding="utf-8")
            with self.subTest(case="noncanonical-before"):
                with self.assertRaisesRegex(ProposalError, "NONCANONICAL_BEFORE"):
                    proposal_mod.prepare_proposal(root, state_path, new_authored_path, "fixture-wk-mx-1")
        finally:
            surface_path.write_bytes(original_surface)
        state_file = Path(state_path)
        original_state = state_file.read_bytes()
        try:
            tampered = core.load_json(state_file)
            tampered["lifecycle_state"] = "DRAFT_COMPLETE"
            core.write_json(state_file, tampered)
            with self.subTest(case="ineligible"):
                with self.assertRaisesRegex(ProposalError, "STATE_INVALID|INELIGIBLE_STATE"):
                    proposal_mod.prepare_proposal(root, state_path, new_authored_path, "fixture-wk-mx-1")
        finally:
            state_file.write_bytes(original_state)
        prepared = proposal_mod.prepare_proposal(root, state_path, new_authored_path, "fixture-wk-mx-1")
        proposal_path = _stage_proposal(self, root, helper.source_root, "fixture-wk-mx-1",
                                        prepared, new_authored_path.read_bytes())
        staged_rel = str((proposal_path.parent / "reader-surface-input-v2.json").relative_to(root))
        copy_dest = next(row["retained_dest"] for row in prepared["proposal"]["retention_plan"]
                         if row["policy"] == "COPY_BEFORE_REPLACEMENT")
        try:
            (root / copy_dest).parent.mkdir(parents=True, exist_ok=True)
            (root / copy_dest).write_text("occupant\n", encoding="utf-8")
            with self.subTest(case="retention-conflict"):
                with self.assertRaisesRegex(ProposalError, "RETENTION_DEST_CONFLICT"):
                    proposal_mod.validate_proposal(root, state_path, proposal_path)
        finally:
            (root / copy_dest).unlink()
        self.assertEqual(
            proposal_mod.validate_proposal(root, state_path, proposal_path)["result"], "REVIEW_REQUIRED")
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
        self.assertEqual(
            proposal_mod.validate_proposal(root, state_path, proposal_path, ordinary)["result"],
            "REVIEW_REQUIRED")
        with self.subTest(case="wrong-before"):
            wrong = _scope_review_for(
                self, root, prepared, staged_rel, "scope-wrong-before-v2.json",
                before_override={"path": prepared["proposal"]["basis"]["active_reader_input_ref"]["path"],
                                 "sha256": "0" * 64})
            with self.assertRaisesRegex(ProposalError, "SCOPE_ORDINARY_INVALID|SCOPE_WRONG_BEFORE"):
                proposal_mod.validate_proposal(root, state_path, proposal_path, wrong)
        with self.subTest(case="reject"):
            rejected = _scope_review_for(self, root, prepared, staged_rel,
                                         "scope-reject-v2.json", decision="REJECT")
            with self.assertRaisesRegex(ProposalError, "SCOPE_NOT_WITHIN_AUTHORITY"):
                proposal_mod.validate_proposal(root, state_path, proposal_path, rejected)
        with self.subTest(case="stale-upstream"):
            stale = _scope_review_for(self, root, prepared, staged_rel, "scope-stale-v2.json",
                                      upstream_override="f" * 64)
            with self.assertRaisesRegex(ProposalError, "SCOPE_STALE_UPSTREAM"):
                proposal_mod.validate_proposal(root, state_path, proposal_path, stale)
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
        with self.assertRaisesRegex(ProposalError, "NO_EDITORIAL_CHANGE"):
            proposal_mod.prepare_proposal(
                root, built["state_path"], built["chain"]["authored_path"], "fixture-wk-cmp-1")
