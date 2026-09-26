from __future__ import annotations
import shutil
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import timedelta
from dataclasses import replace
from pathlib import Path
from unittest import mock
from pypdf import PdfReader, PdfWriter

from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent
from scripts import survey_discovery_v2 as discovery
from scripts import survey_drafting_v2 as drafting
from scripts import survey_x_intake_v2 as xintake
from scripts import survey_stage_validation_v2 as stage_validation
from scripts import survey_weekly_semantic_publication_v2 as weekly_publication
from scripts import survey_reader_publication_v2 as reader_publication
from scripts import survey_reader_surface_gate_v2 as reader_gate
from scripts import survey_quality_v2 as quality
from scripts import survey_weekly_derivation_v2 as weekly
from tests import test_survey_evidence_v2 as evidence_tests
from tests import test_survey_architecture_v2 as architecture_tests
from tests import test_survey_drafting_v2 as drafting_tests


ISSUE = "2026-W37"


class _NoopCleanup:
    def cleanup(self) -> None:
        pass


class IncrementBWeeklyDerivationV2Tests(unittest.TestCase):
    def setUp(self) -> None:
        for name in (
            "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR",
        ):
            if os.environ.get(name):
                raise AssertionError(f"unsafe inherited Git root override for isolated fixture: {name}")
        workspace = Path(__file__).resolve().parents[1]
        scratch = tempfile.TemporaryDirectory(prefix="jgas-weekly-b-")
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name).resolve()
        tracked = subprocess.run(
            ["git", "ls-files", "-z", "--", "config", "schemas", "scripts", "templates", "prompts", "docs", "data"],
            cwd=workspace, capture_output=True, check=True,
        ).stdout
        for raw in tracked.split(b"\0"):
            if not raw:
                continue
            relative = Path(raw.decode("utf-8"))
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(workspace / relative, destination)
        for command in (
            ["git", "init", "-q"],
            ["git", "config", "user.name", "Synthetic Weekly B Fixture"],
            ["git", "config", "user.email", "synthetic-weekly-b@example.invalid"],
            ["git", "remote", "add", "origin", "https://example.invalid/weekly-b-fixture.git"],
            ["git", "add", "-A"],
            ["git", "commit", "-q", "-m", "Synthetic isolated Weekly B source basis"],
        ):
            subprocess.run(command, cwd=self.root, check=True, capture_output=True)
        self.cfg = core.load_json(self.root / core.DEFAULT_CONFIG)
        self.head = core.repository_commit_sha(self.root)
        self.source_root = self.root / "sources" / ISSUE
        self.survey_root = self.root / "surveys" / "weekly" / ISSUE

    def _chain(self) -> dict:
        root, cfg, head = self.root, self.cfg, self.head

        def sandbox(_helper):
            return _NoopCleanup(), root, cfg

        def init_profile(_helper, repo_root, active_cfg, research_profile):
            assert research_profile == "WEEKLY"
            profile = core.weekly_profile(
                repo_root, active_cfg, core.parse_instant("2026-09-19T02:00:00+09:00"), ISSUE
            )
            return core.initialize(
                repo_root, active_cfg, profile, head, "ARCHITECTURE_REVIEW",
                core.parse_instant("2026-09-19T02:05:00+09:00"),
            )

        original_architecture = architecture_tests.SurveyArchitectureV2Tests.architecture_for

        def architecture_for(chain, selection_path, *, research_profile):
            plan = original_architecture(chain, selection_path, research_profile=research_profile)
            plan["publication_extensions"]["closing_summary"] = {
                "required": True,
                "heading": "今週の総括",
                "placement": "after_body_before_references",
            }
            plan["profile_extensions"]["weekly_closing_summary"] = {
                "required": True,
                "source": "profile_synthesis.current_interpretation",
            }
            plan["packages"][0]["publication_extensions"]["section_label"] = "Primary source"
            return plan

        worker = drafting_tests.SurveyDraftingV2Tests()
        with mock.patch.object(evidence_tests.SurveyEvidenceV2Tests, "sandbox", sandbox), \
             mock.patch.object(evidence_tests.SurveyEvidenceV2Tests, "init_profile", init_profile), \
             mock.patch.object(architecture_tests, "IMPLEMENTATION_SHA", head), \
             mock.patch.object(drafting_tests, "IMPLEMENTATION_SHA", head), \
             mock.patch.object(evidence_tests, "IMPLEMENTATION_SHA", head), \
             mock.patch.object(architecture_tests.SurveyArchitectureV2Tests, "architecture_for", staticmethod(architecture_for)):
            chain = worker.build_authorized_chain("WEEKLY")
            package = worker.derive_package(chain)
        chain["draft_package"] = package
        chain["worker"] = worker
        return chain

    def _complete_authorities(self, chain: dict) -> dict:
        issue = ISSUE
        package = chain["draft_package"]
        pid = package["package_id"]
        package_path = self.source_root / "draft/v2/packages" / pid / "draft-package.json"
        core.write_json(package_path, package)
        result = chain["worker"].valid_result(package, package_path, self.root / drafting.DRAFT_PROMPT)
        result["profile_extensions"] = copy.deepcopy(package["profile_extensions"])
        result["publication_extensions"] = copy.deepcopy(package["publication_extensions"])
        result_path = package_path.parent / "draft-result.json"
        core.write_json(result_path, result)
        self.assertEqual(drafting.validate_draft_result(result, package_path, self.root / drafting.DRAFT_PROMPT), [])
        synthesis_input = drafting.build_synthesis_input(
            self.root, chain["profile_path"], chain["architecture_path"],
            chain["review_summary_path"], chain["approval_path"], [(package_path, result_path)],
        )
        synthesis_input_path = self.source_root / "draft/v2/profile-synthesis-input.json"
        core.write_json(synthesis_input_path, synthesis_input)
        closing = "The accepted source authors describe the tested method."
        profile_payload = {key: f"fixture {key}" for key in synthesis_input["profile_payload_requirements"]}
        profile_payload["current_interpretation"] = closing
        synthesis_result = {
            "schema_version": "2.0-rc1", "issue_id": issue,
            "research_profile": "WEEKLY", "publication_profile": "WEEKLY_MAGAZINE",
            "synthesis_version": "v0.1", "status": "ESTABLISHED",
            "basis": {
                "synthesis_input_sha256": core.sha256_file(synthesis_input_path),
                "prompt_id": "profile-synthesis-v2",
                "prompt_sha256": core.sha256_file(self.root / drafting.SYNTHESIS_PROMPT),
            },
            "runner": {
                "provider": "fixture", "model": "fixture", "invocation": "unit-test",
                "generated_at": "2026-09-19T03:20:00+09:00", "run_reference": None,
            },
            "profile_payload": profile_payload, "publication_payload": {},
        }
        synthesis_result_path = self.source_root / "draft/v2/profile-synthesis-result.json"
        core.write_json(synthesis_result_path, synthesis_result)
        self.assertEqual(drafting.validate_synthesis_result(
            synthesis_result, synthesis_input_path, self.root / drafting.SYNTHESIS_PROMPT
        ), [])
        archive_path = self.source_root / "draft/v2/interactive-drafting-synthesis-input.json"
        core.write_json(archive_path, {"packages": [{
            "package_id": pid, "headline": result["headline"], "deck": result["deck"],
            "deck_discovery_ids": ["target-source"], "deck_ref_mode": "CLAIMS",
            "blocks": [{
                "block_id": result["blocks"][0]["block_id"], "text": result["blocks"][0]["text"],
                "discovery_ids": ["target-source"], "ref_mode": "CLAIMS",
            }],
        }]})
        authored_path = self.source_root / "semantic-publication-input.json"
        core.write_json(authored_path, {
            "schema_version": "2.0-rc1", "issue_id": issue, "runner": "WEEKLY_MAGAZINE",
            "cover": {"headline": "Weekly tested method", "deck": "Source-based survey",
                      "anchors": ["Target Model"]},
            "frontmatter": {"heading": "This week", "lede": "A bounded technical survey.",
                            "scope_notes": ["One accepted primary source."]},
            "final_summary": {"heading": "今週の総括", "paragraphs": [
                "The edition surveys one source.", "The claims remain attributed.", closing,
            ]},
        })

        raw_source = self.root / "raw/source.json"
        raw_source.parent.mkdir(parents=True, exist_ok=True)
        raw_source.write_text('{"fixture": true}\n', encoding="utf-8")
        x_manifest = xintake.build_manifest(
            self.root, self.cfg, chain["profile_path"],
            {
                "decision": "REQUIRED", "rationale": "A bounded X fixture is profile-required.",
                "series_context": None, "runs": [{
                    "run_id": "weekly-x-b-fixture",
                    "purpose": "Observe material technical signal.",
                    "research_questions": ["Did material X signal emerge?"],
                    "coverage_focus": ["technical signal"],
                    "time_scope": "fixture week",
                    "expected_result_filename": "grok-x-result.md",
                }],
            },
        )
        x_raw = self.source_root / "external/x/weekly-x-b-fixture/raw/grok-x-result.md"
        x_raw.parent.mkdir(parents=True, exist_ok=True)
        x_raw.write_text("No material technical X signal.\n", encoding="utf-8")
        xintake.record_result(
            self.root, self.cfg, x_manifest, "weekly-x-b-fixture", x_raw, "grok-x-result.md",
            "2026-09-19T03:30:00Z", "2026-09-19T03:35:00Z",
            "NO_MATERIAL_SIGNAL", "NO_MATERIAL_DISCOVERY", [],
            "No material discovery in the fixture X pass.",
        )
        discovery_accepted = discovery.build_acceptance(
            self.root, chain["discovery_path"], x_manifest, issue,
            self.source_root / "discovery/discovery-accepted-v2.json",
        )
        chain.update({
            "draft_package_path": package_path, "draft_result_path": result_path,
            "synthesis_input_path": synthesis_input_path, "synthesis_result_path": synthesis_result_path,
            "archive_path": archive_path, "authored_path": authored_path,
            "discovery_accepted": discovery_accepted,
        })
        return chain

    def _advance(self, chain: dict, stage: str, artifacts: dict[str, Path], minute: int) -> None:
        state_path = self.source_root / "production-state.json"
        self.assertEqual(core.load_json(state_path)["lifecycle_state"], stage)
        stamp = core.parse_instant(f"2026-09-19T{4 + minute // 60:02d}:{minute % 60:02d}:00+09:00")
        report = self.source_root / "orchestration/v2/reviews" / f"{stage}-core-contract.json"
        stage_validation.validate_stage(self.root, self.cfg, state_path, artifacts, report, stamp)
        review_path = report.with_name(f"{stage}-reviews.json")
        core.write_json(review_path, {"reviews": [{
            "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
            "executor": "synthetic Weekly fixture using actual stage validator",
            "evidence": "actual stage validator PASS for exact synthetic edition authorities",
            "result_path": str(report.relative_to(self.root)),
        }]})
        checkpoint = agent.build_stage_checkpoint(
            self.root, self.cfg, state_path, artifacts, review_path,
            f"Synthetic Weekly {stage} fixture stage was validated.", stamp,
        )
        updated = agent.advance_with_checkpoint(self.root, self.cfg, state_path, checkpoint)
        self.assertEqual(agent.validate_agent_state(self.root, self.cfg, updated), [])

    def _current_state(self, chain: dict) -> Path:
        for source, target in (
            (chain["architecture_path"], self.source_root / "architecture-v2.json"),
            (chain["review_summary_path"], self.source_root / "architecture-review-summary-v2.json"),
            (chain["review_attention_path"], self.source_root / "architecture-review-attention-v2.json"),
        ):
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        stages = [
            ("ISSUE_INITIALIZED", {"discovery-acceptance": chain["discovery_accepted"]}),
            ("DISCOVERY_COLLECTED", {"screening-acceptance": chain["screening"]}),
            ("CANDIDATES_NORMALIZED", {
                "evidence-acceptance": chain["evidence"], "edition-views-acceptance": chain["views"],
                "materiality-ledger": chain["ledger_path"], "profile-completeness": chain["completeness_path"],
            }),
            ("EVIDENCE_REVIEWED", {
                "candidate-matrix": chain["matrix_path"], "candidate-selection": chain["selection_path"],
            }),
            ("SELECTION_COMPLETE", {
                "issue-architecture": self.source_root / "architecture-v2.json",
                "architecture-review-summary": self.source_root / "architecture-review-summary-v2.json",
                "architecture-review-attention": self.source_root / "architecture-review-attention-v2.json",
            }),
            ("ARCHITECTURE_ESTABLISHED", {
                "draft-package:" + chain["draft_package"]["package_id"]: chain["draft_package_path"],
                "draft-result:" + chain["draft_package"]["package_id"]: chain["draft_result_path"],
                "synthesis-input": chain["synthesis_input_path"],
                "synthesis-result": chain["synthesis_result_path"],
            }),
        ]
        for number, (stage, artifacts) in enumerate(stages):
            self._advance(chain, stage, artifacts, number + 1)
            if stage == "SELECTION_COMPLETE":
                agent.approve_architecture(
                    self.root, self.cfg, self.source_root / "production-state.json",
                    "synthetic human reviewer", core.parse_instant("2026-09-19T04:06:30+09:00"),
                    "synthetic Weekly B fixture architecture review",
                )
                chain["approval_path"] = self.source_root / "gates/architecture-approval.json"
                package = core.load_json(chain["draft_package_path"])
                package["basis"]["architecture_approval_sha256"] = core.sha256_file(chain["approval_path"])
                core.write_json(chain["draft_package_path"], package)
                result = chain["worker"].valid_result(
                    package, chain["draft_package_path"], self.root / drafting.DRAFT_PROMPT
                )
                result["profile_extensions"] = copy.deepcopy(package["profile_extensions"])
                result["publication_extensions"] = copy.deepcopy(package["publication_extensions"])
                core.write_json(chain["draft_result_path"], result)
                synthesis_input = drafting.build_synthesis_input(
                    self.root, chain["profile_path"], chain["architecture_path"],
                    chain["review_summary_path"], chain["approval_path"],
                    [(chain["draft_package_path"], chain["draft_result_path"])],
                )
                core.write_json(chain["synthesis_input_path"], synthesis_input)
                synthesis_result = core.load_json(chain["synthesis_result_path"])
                synthesis_result["basis"]["synthesis_input_sha256"] = core.sha256_file(chain["synthesis_input_path"])
                core.write_json(chain["synthesis_result_path"], synthesis_result)
        return self.source_root / "production-state.json"

    def test_accepted_weekly_chain_probe(self) -> None:
        chain = self._chain()
        self.assertEqual(chain["draft_package"]["issue_id"], ISSUE)
        self._complete_authorities(chain)

    def test_accepted_weekly_current_state_probe(self) -> None:
        chain = self._complete_authorities(self._chain())
        state_path = self._current_state(chain)
        self.assertEqual(core.load_json(state_path)["lifecycle_state"], "DRAFT_COMPLETE")
        context = weekly.load_derivation(self.root, state_path, chain["authored_path"])
        self.assertEqual(context["surface"]["issue_id"], ISSUE)

    def test_accepted_weekly_two_pass_publication(self) -> None:
        chain = self._complete_authorities(self._chain())
        state_path = self._current_state(chain)
        argv = ["survey_weekly_semantic_publication_v2.py", "--repo-root", str(self.root),
                "--state", str(state_path), "--input", str(chain["authored_path"])]
        with mock.patch.object(sys, "argv", argv + ["--materialize-surface-only"]):
            self.assertEqual(weekly_publication.main(), 0)
        with mock.patch.object(sys, "argv", argv):
            with self.assertRaisesRegex(SystemExit, "semantic review artifact missing"):
                weekly_publication.main()
        publication_root = self.source_root / "publication/v2"
        surface_path = publication_root / "reader-surface-input-v2.json"
        self.assertTrue(surface_path.is_file())
        self.assertFalse((self.survey_root / "main.tex").exists())
        self.assertFalse((self.survey_root / "references.bib").exists())
        self.assertFalse((self.survey_root / "jgaisurvey.sty").exists())
        self.assertFalse((publication_root / "validated-source-manifest.json").exists())

        review_path = publication_root / "reader-surface-semantic-review-v2.json"
        review = {
            "schema_version": "2.0-rc1", "issue_id": ISSUE,
            "publication_profile": "WEEKLY_MAGAZINE", "review_kind": "SEMANTIC_EDITORIAL",
            "reviewed_surface": {"path": str(surface_path.relative_to(self.root)),
                                 "sha256": core.sha256_file(surface_path)},
            "checks": [{"check_id": "READER_PIPELINE_INDEPENDENCE", "status": "PASS",
                        "detail": "Synthetic reviewer judged complete fixture prose independently understandable.",
                        "evidence_locations": ["reader-surface-input-v2.json:packages",
                                               "reader-surface-input-v2.json:bibliography"]}],
            "decision": "PASS", "reviewed_by": "synthetic Weekly B reviewer",
            "reviewed_at": "2026-09-19T05:00:00+09:00", "recorded_at": "2026-09-19T05:00:00+09:00",
            "status": "PASSED", "findings": [],
            "summary": "Synthetic PASS after inspection of the complete fixture reader input.",
        }
        review["review_sha256"] = core.sha256_object(review)
        for failure in ("wrong-target", "non-pass"):
            bad_review = copy.deepcopy(review)
            if failure == "wrong-target":
                bad_review["reviewed_surface"]["sha256"] = "0" * 64
            else:
                bad_review["decision"] = "FAIL"
                bad_review["status"] = "FAILED"
            bad_review["review_sha256"] = core.sha256_object({
                key: value for key, value in bad_review.items() if key != "review_sha256"
            })
            core.write_json(review_path, bad_review)
            with self.subTest(failure=failure), mock.patch.object(sys, "argv", argv):
                expected = "Reviewed surface bytes drifted" if failure == "wrong-target" else "did not yield PASS decision"
                with self.assertRaisesRegex(SystemExit, expected):
                    weekly_publication.main()
            for absent in ("main.tex", "references.bib", "jgaisurvey.sty"):
                self.assertFalse((self.survey_root / absent).exists())
            self.assertFalse((publication_root / "validated-source-manifest.json").exists())
        core.write_json(review_path, review)
        self.survey_root.mkdir(parents=True, exist_ok=True)
        extra_local_package = self.survey_root / "hyperref.sty"
        extra_local_package.write_text("% inert local package shadow\n", encoding="utf-8")
        with mock.patch.object(sys, "argv", argv):
            with self.assertRaisesRegex(SystemExit, "Weekly publication build directory invalid.*undeclared entry"):
                weekly_publication.main()
        for absent in ("main.tex", "references.bib", "jgaisurvey.sty"):
            self.assertFalse((self.survey_root / absent).exists())
        self.assertFalse((publication_root / "validated-source-manifest.json").exists())
        extra_local_package.unlink()
        with mock.patch.object(sys, "argv", argv):
            self.assertEqual(weekly_publication.main(), 0)
        receipt_path = publication_root / "validated-source-manifest.json"
        self.assertTrue(receipt_path.is_file())
        weekly.validate_receipt(self.root, receipt_path, state_path)
        receipt_original = receipt_path.read_bytes()
        for role, file_path in (
            ("primary", self.survey_root / "main.tex"),
            ("bibliography", self.survey_root / "references.bib"),
            ("style", self.survey_root / "jgaisurvey.sty"),
        ):
            with self.subTest(rehashed_output=role):
                original = file_path.read_bytes()
                file_path.write_bytes(original + b"\n% synthetic changed output\n")
                changed_receipt = core.load_json(receipt_path)
                changed_receipt["outputs"][role]["sha256"] = core.sha256_file(file_path)
                changed_receipt["receipt_sha256"] = core.sha256_object({
                    key: value for key, value in changed_receipt.items() if key != "receipt_sha256"
                })
                core.write_json(receipt_path, changed_receipt)
                with self.assertRaisesRegex(ValueError, "deterministic .* replay mismatch"):
                    weekly.validate_receipt(self.root, receipt_path, state_path)
                file_path.write_bytes(original)
                receipt_path.write_bytes(receipt_original)
        reviewed_original = surface_path.read_bytes()
        changed_surface = core.load_json(surface_path)
        changed_surface["cover"]["headline"] = "Unreviewed replacement headline"
        core.write_json(surface_path, changed_surface)
        changed_receipt = core.load_json(receipt_path)
        changed_receipt["reviewed_reader_input"]["sha256"] = core.sha256_file(surface_path)
        changed_receipt["receipt_sha256"] = core.sha256_object({
            key: value for key, value in changed_receipt.items() if key != "receipt_sha256"
        })
        core.write_json(receipt_path, changed_receipt)
        with self.assertRaisesRegex(ValueError, "independently recomputed reader input differs"):
            weekly.validate_receipt(self.root, receipt_path, state_path)
        surface_path.write_bytes(reviewed_original)
        receipt_path.write_bytes(receipt_original)
        architecture = core.load_json(self.source_root / "architecture-v2.json")
        coverage = [
            {"package_id": plan["package_id"], "requirement": requirement,
             "status": "FULFILLED", "reader_locations": ["main.tex:package-1"],
             "detail": "Synthetic fixture author maps the accepted package requirement to its source section."}
            for plan in architecture["packages"]
            for requirement in plan["must_cover_requirements"]
        ]
        requirements = [
            {"requirement_id": key, "status": "FULFILLED", "reader_locations": [location],
             "detail": "Synthetic fixture author asserts this visible requirement is present."}
            for key, location in (("FINAL_SYNTHESIS", "main.tex:summary"),
                                  ("WEEKLY_COMMUNITY_MOVEMENT", "main.tex:package-1"))
        ]
        manuscript_path = publication_root / "reader-manuscript-v2.json"
        reader_publication.build_manuscript_manifest(
            self.root, ISSUE, chain["profile_path"], self.source_root / "architecture-v2.json",
            chain["approval_path"], self.survey_root / "main.tex",
            [{"role": "BIBLIOGRAPHY", "path": str((self.survey_root / "references.bib").relative_to(self.root))},
             {"role": "STYLE", "path": str((self.survey_root / "jgaisurvey.sty").relative_to(self.root))}],
            coverage, requirements, "synthetic Weekly B manuscript author",
            core.parse_instant("2026-09-19T05:10:00+09:00"), manuscript_path,
        )
        gate_path = publication_root / "reader-surface-gate-v2.json"
        reader_publication.build_reader_surface_gate(
            self.root, manuscript_path, review_path, output_path=gate_path, state_path=state_path,
        )
        gate = reader_gate.validate_reader_surface_gate(
            self.root, gate_path, issue_id=ISSUE, publication_profile="WEEKLY_MAGAZINE",
            expected_manuscript_path=manuscript_path, state_path=state_path,
        )
        self.assertEqual(gate["status"], "PASSED")
        self.assertEqual(gate["derivation"]["route"], weekly.ROUTE)

        # Synthetic ancillary PDF/review records exercise stage wiring only;
        # this fixture does not claim a TeX build or real editorial/visual QA.
        pdf_path = self.survey_root / "main.pdf"
        pdf = PdfWriter()
        pdf.add_blank_page(width=595, height=842)
        with pdf_path.open("wb") as output:
            pdf.write(output)
        self.assertEqual(len(PdfReader(pdf_path).pages), 1)
        # The fixed Weekly build workflow can leave these three non-input outputs.
        log_path = self.survey_root / "main.log"
        checksum_path = self.survey_root / "main.pdf.sha256"
        log_path.write_text("synthetic build log\n", encoding="utf-8")
        checksum_path.write_text(core.sha256_file(pdf_path) + "  main.pdf\n", encoding="utf-8")
        weekly.validate_receipt(self.root, receipt_path, state_path)
        reader_gate.validate_reader_surface_gate(
            self.root, gate_path, expected_manuscript_path=manuscript_path, state_path=state_path,
        )
        log_path.unlink()
        checksum_path.unlink()

        for extra_name, extra_kind in (
            ("hyperref.sty", "file"), ("jlreq.cls", "file"),
            (".latexmkrc", "file"), ("main.aux", "file"),
            ("main.bbl", "file"), ("nested", "directory"),
            ("main.log", "symlink"), ("dangling.tex", "dangling_symlink"),
        ):
            extra = self.survey_root / extra_name
            with self.subTest(undeclared_build_entry=extra_name):
                if extra_kind == "directory":
                    extra.mkdir()
                elif extra_kind == "symlink":
                    extra.symlink_to(self.survey_root / "main.tex")
                elif extra_kind == "dangling_symlink":
                    extra.symlink_to(self.survey_root / "missing-target.tex")
                else:
                    extra.write_text("inert extra build entry\n", encoding="utf-8")
                try:
                    with self.assertRaisesRegex(ValueError, "Weekly survey build directory.*undeclared entry"):
                        weekly.validate_receipt(self.root, receipt_path, state_path)
                    with self.assertRaisesRegex(ValueError, "Weekly survey build directory.*undeclared entry"):
                        reader_gate.validate_reader_surface_gate(
                            self.root, gate_path, expected_manuscript_path=manuscript_path,
                            state_path=state_path,
                        )
                finally:
                    if extra_kind == "directory":
                        extra.rmdir()
                    else:
                        extra.unlink()
        survey_alias = self.root / "synthetic-survey-alias"
        survey_alias.symlink_to(self.root / "surveys", target_is_directory=True)
        try:
            with self.assertRaisesRegex(ValueError, "Weekly survey build directory.*symlinked component"):
                weekly.validate_survey_build_directory(
                    self.root, f"synthetic-survey-alias/weekly/{ISSUE}"
                )
        finally:
            survey_alias.unlink()

        decoy_root = self.root / "synthetic-decoy-outputs"
        decoy_root.mkdir()
        decoy_receipt = core.load_json(receipt_path)
        for role, name in (("primary", "main.tex"), ("bibliography", "references.bib"),
                           ("style", "jgaisurvey.sty")):
            decoy = decoy_root / name
            decoy.write_bytes((self.survey_root / name).read_bytes())
            decoy_receipt["outputs"][role]["path"] = str(decoy.relative_to(self.root))
        decoy_receipt["receipt_sha256"] = core.sha256_object({
            key: value for key, value in decoy_receipt.items() if key != "receipt_sha256"
        })
        core.write_json(receipt_path, decoy_receipt)
        try:
            with self.assertRaisesRegex(ValueError, "output path is not canonical survey_root"):
                weekly.validate_receipt(self.root, receipt_path, state_path)
            with self.assertRaisesRegex(ValueError, "output path is not canonical survey_root"):
                reader_gate.validate_reader_surface_gate(
                    self.root, gate_path, expected_manuscript_path=manuscript_path,
                    state_path=state_path,
                )
        finally:
            receipt_path.write_bytes(receipt_original)
            for name in ("main.tex", "references.bib", "jgaisurvey.sty"):
                (decoy_root / name).unlink()
            decoy_root.rmdir()
        quality_root = publication_root / "quality"
        subject_path = quality_root / "subject-entity-property-binding.json"
        self.assertEqual(core.load_json(subject_path)["status"], "PASS")
        main_text = (self.survey_root / "main.tex").read_text(encoding="utf-8")
        for token in (ISSUE, "Target Model"):
            self.assertIn(token, main_text)
        identifier_path = quality_root / "identifier-preservation.json"
        core.write_json(identifier_path, {
            "check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
            "source_sha256": core.sha256_file(self.survey_root / "main.tex"),
            "inspected_identifiers": [ISSUE, "Target Model"],
            "scope": "synthetic generated fixture",
        })
        preflight_path = quality_root / "pdf-preflight.json"
        core.write_json(preflight_path, {
            "check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": 1,
            "pdf_sha256": core.sha256_file(pdf_path), "byte_count": pdf_path.stat().st_size,
            "scope": "synthetic parseable one-page PDF; not a TeX rendering",
        })
        result_paths = {
            "SUBJECT_ENTITY_PROPERTY_BINDING": subject_path,
            "IDENTIFIER_PRESERVATION": identifier_path,
            "PDF_PREFLIGHT": preflight_path,
        }
        quality_checks = [
            {"check_id": check_id, "kind": "DETERMINISTIC", "status": "PASS",
             "executor": "synthetic Weekly B fixture with actual file assertions",
             "evidence": "Exact fixture bytes and result file inspected by test.",
             "recorded_at": "2026-09-19T05:20:00+09:00",
             "result": {"path": str(path.relative_to(self.root)), "sha256": core.sha256_file(path)}}
            for check_id, path in result_paths.items()
        ]
        bundle_path = publication_root / "quality-regression-bundle-v2.json"
        quality.build_bundle(
            self.root, ISSUE, self.survey_root / "main.tex", pdf_path, quality_checks,
            bundle_path, production_profile_path=chain["profile_path"],
        )
        review_paths: dict[str, Path] = {}
        profile = core.load_json(chain["profile_path"])
        for kind, name in (("SEMANTIC_EDITORIAL", "semantic-editorial-review-v2.json"),
                           ("VISUAL", "visual-review-v2.json")):
            checks = [
                {"check_id": check_id, "status": "PASS",
                 "detail": "Synthetic fixture review; no real editorial or visual acceptance asserted.",
                 "evidence_locations": ["synthetic-fixture:main.tex"]}
                for check_id in sorted(reader_publication._expected_review_checks(self.root, profile, kind))
            ]
            path = publication_root / name
            reader_publication.build_review_record(
                self.root, manuscript_path, pdf_path, 1, kind, checks,
                f"synthetic Weekly B {kind} reviewer", core.parse_instant("2026-09-19T05:30:00+09:00"),
                path,
            )
            review_paths[kind] = path
        self._advance(chain, "DRAFT_COMPLETE", {
            "reader-manuscript": manuscript_path,
            "validated-source": self.survey_root / "main.tex",
            "publication-pdf": pdf_path,
            "quality-regression-bundle": bundle_path,
            "semantic-review": review_paths["SEMANTIC_EDITORIAL"],
            "visual-review": review_paths["VISUAL"],
            "reader-surface-gate": gate_path,
        }, 130)
        self.assertEqual(core.load_json(state_path)["lifecycle_state"], "VALIDATED_DRAFT")
        weekly.validate_receipt(self.root, receipt_path, state_path)
        reader_gate.validate_reader_surface_gate(
            self.root, gate_path, expected_manuscript_path=manuscript_path, state_path=state_path,
        )
        creation_head = self.head
        closure_before = weekly.current_closure(self.root)
        subprocess.run(["git", "add", "--", str(surface_path.relative_to(self.root))],
                       cwd=self.root, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m", "Synthetic reviewed reader input artifact"],
                       cwd=self.root, check=True, capture_output=True)
        self.assertNotEqual(core.repository_commit_sha(self.root), creation_head)
        self.assertEqual(weekly.current_closure(self.root), closure_before)
        weekly.validate_receipt(self.root, receipt_path, state_path)

        def renew_publication(marker: str, minute: int) -> Path:
            # The synthetic metadata renewal is a real pending publication byte
            # change against the immutable validation checkpoint.
            document = core.load_json(manuscript_path)
            document["authored_by"] = f"synthetic Weekly B manuscript author {marker}"
            document["manifest_sha256"] = core.sha256_object({
                key: value for key, value in document.items() if key != "manifest_sha256"
            })
            core.write_json(manuscript_path, document)
            self.assertNotEqual(agent.validate_agent_state(self.root, self.cfg, core.load_json(state_path)), [])
            pending = agent.built_checked_pending_publication_basis(self.root, self.cfg, state_path)
            self.assertTrue(pending.replacements)
            if marker == "first":
                # Rechecking must reject a copied State and a directory-symlink
                # alias even when their JSON bytes equal the canonical State.
                copied_state = self.source_root / "synthetic-copied-state.json"
                copied_state.write_bytes(state_path.read_bytes())
                copied_basis = replace(pending, state_path=str(copied_state))
                self.assertTrue(any("State path is not canonical" in row for row in agent._validate_agent_state(
                    self.root, self.cfg, core.load_json(state_path), copied_basis
                )))
                copied_state.unlink()
                state_alias = self.root / "synthetic-state-alias"
                state_alias.symlink_to(self.source_root, target_is_directory=True)
                alias_basis = replace(pending, state_path=str(state_alias / state_path.name))
                self.assertTrue(any("State path is not canonical" in row for row in agent._validate_agent_state(
                    self.root, self.cfg, core.load_json(state_path), alias_basis
                )))
                state_alias.unlink()
                pristine_state = state_path.read_bytes()
                for mutation, expected in (("next_action", "next_action drift"), ("history", "history length")):
                    altered = core.load_json(state_path)
                    if mutation == "next_action":
                        altered["next_action"] = "synthetic-invalid-controller-action"
                    else:
                        altered["history"].pop()
                    core.write_json(state_path, altered)
                    with self.subTest(pending_state_mutation=mutation):
                        self.assertTrue(any("State bytes changed" in row for row in agent._validate_agent_state(
                            self.root, self.cfg, altered, pending
                        )))
                        with self.assertRaisesRegex(agent.AgentControlError, expected):
                            agent.built_checked_pending_publication_basis(self.root, self.cfg, state_path)
                    state_path.write_bytes(pristine_state)
                manuscript_before_stale = manuscript_path.read_bytes()
                manuscript_path.write_bytes(manuscript_before_stale + b" ")
                self.assertTrue(any("row snapshot changed" in row for row in agent._validate_agent_state(
                    self.root, self.cfg, core.load_json(state_path), pending
                )))
                manuscript_path.write_bytes(manuscript_before_stale)
                validation_ref = core.load_json(state_path)["checkpoint_provenance"]["validation"]
                checkpoint_path = self.root / validation_ref["path"]
                checkpoint_before = checkpoint_path.read_bytes()
                alias_path = publication_root / "synthetic-wrong-manuscript-path.json"
                alias_path.write_bytes(manuscript_path.read_bytes())
                checkpoint = core.load_json(checkpoint_path)
                wrong_row = next(row for row in checkpoint["artifacts"] if row["name"] == "reader-manuscript")
                wrong_row["path"] = str(alias_path.relative_to(self.root))
                core.write_json(checkpoint_path, checkpoint)
                wrong_state = core.load_json(state_path)
                wrong_state["checkpoint_provenance"]["validation"]["sha256"] = core.sha256_file(checkpoint_path)
                core.write_json(state_path, wrong_state)
                with self.assertRaisesRegex(agent.AgentControlError, "noncanonical or upstream role/path"):
                    agent.built_checked_pending_publication_basis(self.root, self.cfg, state_path)
                state_path.write_bytes(pristine_state)
                checkpoint_path.write_bytes(checkpoint_before)
                alias_path.unlink()
                checkpoint = core.load_json(checkpoint_path)
                wrong_row = next(row for row in checkpoint["artifacts"] if row["name"] == "reader-manuscript")
                wrong_row["name"] = "synthetic-wrong-publication-role"
                core.write_json(checkpoint_path, checkpoint)
                wrong_state = core.load_json(state_path)
                wrong_state["checkpoint_provenance"]["validation"]["sha256"] = core.sha256_file(checkpoint_path)
                core.write_json(state_path, wrong_state)
                with self.assertRaisesRegex(agent.AgentControlError, "noncanonical or upstream role/path"):
                    agent.built_checked_pending_publication_basis(self.root, self.cfg, state_path)
                state_path.write_bytes(pristine_state)
                checkpoint_path.write_bytes(checkpoint_before)
            elif marker == "second":
                state_before_chain = state_path.read_bytes()
                first_ref = core.load_json(state_path)["publication_revalidation_provenance"]
                first_path = self.root / first_ref["path"]
                first_before_chain = first_path.read_bytes()
                broken = core.load_json(first_path)
                broken["supersedes"] = {
                    "path": str((publication_root / "missing-predecessor.json").relative_to(self.root)),
                    "sha256": "0" * 64,
                }
                core.write_json(first_path, broken)
                altered = core.load_json(state_path)
                altered["publication_revalidation_provenance"]["sha256"] = core.sha256_file(first_path)
                core.write_json(state_path, altered)
                with self.assertRaisesRegex(agent.AgentControlError, "predecessor invalid"):
                    agent.built_checked_pending_publication_basis(self.root, self.cfg, state_path)
                state_path.write_bytes(state_before_chain)
                first_path.write_bytes(first_before_chain)
            weekly.validate_receipt(self.root, receipt_path, state_path)
            reader_publication.build_reader_surface_gate(
                self.root, manuscript_path, review_path, output_path=gate_path, state_path=state_path,
            )
            reader_gate.validate_reader_surface_gate(
                self.root, gate_path, expected_manuscript_path=manuscript_path, state_path=state_path,
            )
            for kind, path in review_paths.items():
                old_review = core.load_json(path)
                path.unlink()
                reader_publication.build_review_record(
                    self.root, manuscript_path, pdf_path, 1, kind,
                    old_review["checks"], f"synthetic Weekly B {marker} reviewer",
                    core.parse_instant(f"2026-09-19T{minute:02d}:00:00+09:00"), path,
                )
            if marker == "first":
                state_before = state_path.read_bytes()
                records_before = sorted(publication_root.glob("publication-surface-revalidation-r*.json"))
                architecture_path = self.source_root / "architecture-v2.json"
                architecture_before = architecture_path.read_bytes()
                architecture_path.write_bytes(architecture_before + b" ")
                with self.assertRaisesRegex(agent.AgentControlError, "artifact drift"):
                    agent.built_checked_pending_publication_basis(self.root, self.cfg, state_path)
                architecture_path.write_bytes(architecture_before)
                bundle_before = bundle_path.read_bytes()
                bundle_path.write_bytes(b"{invalid synthetic QA bundle")
                with self.assertRaises((agent.AgentControlError, ValueError)):
                    agent.revalidate_publication_surface(
                        self.root, self.cfg, state_path, "REVIEWED_CORE_CHANGE",
                        "synthetic malformed QA negative", "synthetic fixture",
                        core.parse_instant("2026-09-19T06:05:00+09:00"),
                    )
                bundle_path.write_bytes(bundle_before)
                self.assertEqual(state_path.read_bytes(), state_before)
                self.assertEqual(sorted(publication_root.glob("publication-surface-revalidation-r*.json")), records_before)
                with self.assertRaisesRegex(agent.AgentControlError, "actual current HEAD"):
                    agent.revalidate_publication_surface(
                        self.root, self.cfg, state_path, "REVIEWED_CORE_CHANGE",
                        "synthetic wrong implementation override", "synthetic fixture",
                        core.parse_instant("2026-09-19T06:05:30+09:00"),
                        implementation_sha="0" * 40,
                    )
                self.assertEqual(state_path.read_bytes(), state_before)
                self.assertEqual(sorted(publication_root.glob("publication-surface-revalidation-r*.json")), records_before)
                # Fault injection is confined to the post-write validator; the
                # positive authority path below uses its real implementation.
                with mock.patch.object(agent, "validate_agent_state", return_value=["injected post-write failure"]):
                    with self.assertRaisesRegex(agent.AgentControlError, "resulting revalidation State invalid"):
                        agent.revalidate_publication_surface(
                            self.root, self.cfg, state_path, "REVIEWED_CORE_CHANGE",
                            "synthetic rollback injection", "synthetic fixture",
                            core.parse_instant("2026-09-19T06:06:00+09:00"),
                        )
                self.assertEqual(state_path.read_bytes(), state_before)
                self.assertEqual(sorted(publication_root.glob("publication-surface-revalidation-r*.json")), records_before)
            record = agent.revalidate_publication_surface(
                self.root, self.cfg, state_path, "REVIEWED_CORE_CHANGE",
                f"Synthetic Weekly B {marker} publication renewal", "synthetic fixture",
                core.parse_instant(f"2026-09-19T{minute:02d}:10:00+09:00"),
            )
            self.assertEqual(agent.validate_agent_state(self.root, self.cfg, core.load_json(state_path)), [])
            self.assertEqual(agent.resolve_active_publication_revalidation(
                self.root, self.cfg, core.load_json(state_path)
            )[1], [])
            weekly.validate_receipt(self.root, receipt_path, state_path)
            reader_gate.validate_reader_surface_gate(
                self.root, gate_path, expected_manuscript_path=manuscript_path, state_path=state_path,
            )
            return record

        first_record = renew_publication("first", 6)
        state_before_pointer_negative = state_path.read_bytes()
        bad_state = core.load_json(state_path)
        bad_state["publication_revalidation_provenance"]["sha256"] = "0" * 64
        core.write_json(state_path, bad_state)
        with self.assertRaisesRegex(agent.AgentControlError, "predecessor invalid"):
            agent.built_checked_pending_publication_basis(self.root, self.cfg, state_path)
        state_path.write_bytes(state_before_pointer_negative)
        with self.assertRaisesRegex(agent.AgentControlError, "already validates current bytes"):
            agent.revalidate_publication_surface(
                self.root, self.cfg, state_path, "REVIEWED_CORE_CHANGE", "no-op repeat",
                "synthetic fixture", core.parse_instant("2026-09-19T06:20:00+09:00"),
            )
        second_record = renew_publication("second", 7)
        self.assertEqual(core.load_json(second_record)["supersedes"], {
            "path": str(first_record.relative_to(self.root)), "sha256": core.sha256_file(first_record),
        })
        # Rehash every link and the State pointer so the failure reaches the
        # ancestor's immutable QA-to-artifact agreement, not file SHA checking.
        chain_state_before = state_path.read_bytes()
        first_before = first_record.read_bytes()
        second_before = second_record.read_bytes()
        broken_first = core.load_json(first_record)
        broken_first["validation"]["manuscript"]["sha256"] = "0" * 64
        core.write_json(first_record, broken_first)
        broken_second = core.load_json(second_record)
        broken_second["supersedes"]["sha256"] = core.sha256_file(first_record)
        core.write_json(second_record, broken_second)
        broken_state = core.load_json(state_path)
        broken_state["publication_revalidation_provenance"]["sha256"] = core.sha256_file(second_record)
        core.write_json(state_path, broken_state)
        self.assertTrue(any("predecessor manuscript is not bound" in row for row in agent.validate_agent_state(
            self.root, self.cfg, core.load_json(state_path)
        )))
        state_path.write_bytes(chain_state_before)
        second_record.write_bytes(second_before)
        first_record.write_bytes(first_before)
        with self.assertRaisesRegex(ValueError, "missing or is not a commit"):
            weekly._verify_head_bytes(self.root, "0" * 40, closure_before)
        orphan = subprocess.run(
            ["git", "commit-tree", f"{core.repository_commit_sha(self.root)}^{{tree}}",
             "-m", "Synthetic unrelated commit"], cwd=self.root,
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        with self.assertRaisesRegex(ValueError, "not an ancestor"):
            weekly._verify_head_bytes(self.root, orphan, closure_before)
        control = self.root / "scripts/survey_weekly_derivation_v2.py"
        control.write_text(control.read_text(encoding="utf-8") + "\n# synthetic control change\n", encoding="utf-8")
        subprocess.run(["git", "add", "--", "scripts/survey_weekly_derivation_v2.py"],
                       cwd=self.root, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m", "Synthetic code control change"],
                       cwd=self.root, check=True, capture_output=True)
        with self.assertRaisesRegex(ValueError, "implementation or contract changed"):
            weekly.validate_receipt(self.root, receipt_path, state_path)

    def test_receipt_basis_controls_reject_dirty_and_committed_changes(self) -> None:
        closure = weekly.current_closure(self.root)
        basis = core.repository_commit_sha(self.root)
        weekly._verify_head_bytes(self.root, basis, closure)

        helper = self.root / "scripts/survey_weekly_derivation_v2.py"
        original_helper = helper.read_bytes()
        helper.write_bytes(original_helper + b"\n# dirty fixture control\n")
        with self.assertRaisesRegex(ValueError, "differs from committed HEAD"):
            weekly._verify_head_bytes(self.root, basis, closure)
        helper.write_bytes(original_helper)

        config_path = self.root / core.DEFAULT_CONFIG
        original_config = config_path.read_bytes()
        config = json.loads(original_config)
        # A changed config cannot narrow the set used to inspect itself.
        config["implementation_control_roots"] = []
        config["contract_files"] = {}
        core.write_json(config_path, config)
        with self.assertRaisesRegex(ValueError, "differs from committed HEAD"):
            weekly._verify_head_bytes(self.root, basis, closure)
        subprocess.run(["git", "add", "--", str(core.DEFAULT_CONFIG)],
                       cwd=self.root, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m", "Synthetic narrowed config control"],
                       cwd=self.root, check=True, capture_output=True)
        with self.assertRaisesRegex(ValueError, "changed since renderer commit"):
            weekly._verify_head_bytes(self.root, basis, closure)
    def test_historical_visible_omission_projection_matrix(self) -> None:
        # Each case reprojects changed in-memory source fields. Immutable
        # checkpoint rebinding is tested by the integration/replay paths.
        chain = self._complete_authorities(self._chain())
        state_path = self._current_state(chain)
        context = weekly.load_derivation(self.root, state_path, chain["authored_path"])
        source = {
            "profile": core.load_json(chain["profile_path"]),
            "architecture": core.load_json(chain["architecture_path"]),
            "authored": core.load_json(chain["authored_path"]),
            "synthesis": core.load_json(chain["synthesis_result_path"]),
            "ordered": [{
                "plan": core.load_json(chain["architecture_path"])["packages"][0],
                "spec": core.load_json(chain["archive_path"])["packages"][0],
                "package": core.load_json(chain["draft_package_path"]),
                "result": core.load_json(chain["draft_result_path"]),
            }],
            "records": context["records"],
        }
        source["ordered"][0]["result"]["blocks"].append({
            "block_id": "result-only-claim-boundary", "block_type": "CLAIM_BOUNDARY",
            "text": "The accepted source does not establish broader adoption.",
            "attribution_mode": "INFERENCE", "evidence_refs": [],
        })

        def project(value: dict) -> dict:
            return weekly.build_reader_input(
                ISSUE, value["profile"], value["architecture"], value["authored"],
                value["synthesis"], value["ordered"], value["records"],
            )

        baseline = project(source)
        weekly.validate_reader_input(self.root, baseline)
        baseline_main = weekly.render_main(baseline)
        self.assertNotEqual(core.sha256_object(baseline), core.sha256_object(context["surface"]))
        self.assertIn("result-only-claim-boundary",
                      [block["block_id"] for block in baseline["packages"][0]["blocks"]])

        target_path = self.source_root / "publication/v2/reader-surface-input-v2.json"
        target_path.parent.mkdir(parents=True, exist_ok=True)
        review_path = target_path.parent / "reader-surface-semantic-review-v2.json"
        core.write_json(target_path, baseline)
        review = {
            "schema_version": "2.0-rc1", "issue_id": ISSUE,
            "publication_profile": "WEEKLY_MAGAZINE", "review_kind": "SEMANTIC_EDITORIAL",
            "reviewed_surface": {"path": str(target_path.relative_to(self.root)),
                                 "sha256": core.sha256_file(target_path)},
            "checks": [{"check_id": "READER_PIPELINE_INDEPENDENCE", "status": "PASS",
                        "detail": "Synthetic review of the pure projection fixture.",
                        "evidence_locations": ["reader-surface-input-v2.json:packages"]}],
            "decision": "PASS", "reviewed_by": "synthetic projection reviewer",
            "reviewed_at": "2026-09-19T05:00:00+09:00",
            "recorded_at": "2026-09-19T05:00:00+09:00",
            "status": "PASSED", "findings": [], "summary": "Synthetic review fixture.",
        }
        review["review_sha256"] = core.sha256_object(review)
        core.write_json(review_path, review)

        def validate_review() -> None:
            reader_gate.load_and_validate_semantic_review(
                self.root, review_path, expected_issue_id=ISSUE,
                expected_publication_profile="WEEKLY_MAGAZINE",
                expected_surface_path=target_path,
                expected_surface_sha256=core.sha256_file(target_path),
                require_pass=True,
            )

        validate_review()

        def change(value: dict, name: str) -> None:
            author = value["authored"]
            plan = value["architecture"]["packages"][0]
            ordered = value["ordered"][0]
            temporal = value["profile"]["research_scope"]["temporal_policy"]
            if name == "cover anchors":
                author["cover"]["anchors"][0] = "Different anchor"
            elif name == "front heading":
                author["frontmatter"]["heading"] = "Different front heading"
            elif name == "front lede":
                author["frontmatter"]["lede"] = "Different front lede"
            elif name == "front scope":
                author["frontmatter"]["scope_notes"][0] = "Different scope note"
            elif name == "final heading":
                author["final_summary"]["heading"] = "Different final heading"
                value["architecture"]["publication_extensions"]["closing_summary"]["heading"] = "Different final heading"
            elif name == "section label":
                plan["publication_extensions"]["section_label"] = "Different section label"
                ordered["plan"]["publication_extensions"]["section_label"] = "Different section label"
            elif name == "result claim boundary":
                ordered["result"]["blocks"][-1]["text"] = "Different claim boundary"
            elif name == "display date":
                temporal["window_end"] = "2026-09-20T02:00:00+09:00"
                temporal["cutoff"] = temporal["window_end"]
            elif name == "window boundary":
                temporal["window_start"] = "2026-09-10T02:00:00+09:00"
            elif name == "citation identity":
                old_did, new_did = "target-source", "alternate-source"
                ordered["package"]["candidate_matrix"]["rows"][0]["discovery_ids"].append(new_did)
                ordered["spec"]["deck_discovery_ids"] = [new_did]
                value["records"][new_did] = copy.deepcopy(value["records"][old_did])
            elif name == "cover headline control":
                author["cover"]["headline"] = "Different cover headline"
            elif name == "summary paragraph control":
                author["final_summary"]["paragraphs"][0] = "Different summary paragraph"
            else:
                raise AssertionError(name)

        names = (
            "cover anchors", "front heading", "front lede", "front scope",
            "final heading", "section label", "result claim boundary",
            "display date", "window boundary", "citation identity",
            "cover headline control", "summary paragraph control",
        )
        for name in names:
            with self.subTest(name=name):
                changed_source = copy.deepcopy(source)
                change(changed_source, name)
                changed = project(changed_source)
                weekly.validate_reader_input(self.root, changed)
                self.assertNotEqual(core.sha256_object(changed), core.sha256_object(baseline))
                self.assertNotEqual(weekly.render_main(changed), baseline_main)
                core.write_json(target_path, changed)
                with self.assertRaisesRegex(ValueError, "Reviewed surface bytes drifted"):
                    validate_review()
        core.write_json(target_path, baseline)
        validate_review()

        invalid = copy.deepcopy(source)
        invalid["ordered"][0]["spec"]["deck_discovery_ids"] = ["unaccepted-source"]
        with self.assertRaisesRegex(ValueError, "resolve exactly once"):
            project(invalid)
        none_mode = copy.deepcopy(source)
        none_mode["ordered"][0]["spec"]["deck_ref_mode"] = "NONE"
        with self.assertRaisesRegex(ValueError, "NONE cannot carry discovery_ids"):
            project(none_mode)
    def test_weekly_closing_source_must_be_exact_accepted_profile_value(self) -> None:
        chain = self._complete_authorities(self._chain())
        profile = core.load_json(chain["profile_path"])
        architecture = core.load_json(chain["architecture_path"])
        authored = core.load_json(chain["authored_path"])
        synthesis = core.load_json(chain["synthesis_result_path"])
        self.assertEqual(synthesis["publication_payload"], {})
        synthesis["profile_payload"].pop("current_interpretation")
        with self.assertRaisesRegex(ValueError, "lacks current_interpretation"):
            weekly.build_reader_input(ISSUE, profile, architecture, authored, synthesis, [], {})
        synthesis["profile_payload"]["current_interpretation"] = ""
        with self.assertRaisesRegex(ValueError, "lacks current_interpretation"):
            weekly.build_reader_input(ISSUE, profile, architecture, authored, synthesis, [], {})
        synthesis["profile_payload"]["current_interpretation"] = "Unreviewed replacement."
        with self.assertRaisesRegex(ValueError, "preserve exact approved synthesis paragraph"):
            weekly.build_reader_input(ISSUE, profile, architecture, authored, synthesis, [], {})

    def test_bib_special_text_is_escaped_and_url_is_preserved(self) -> None:
        url = "https://example.invalid/a%20b?q=one&lang=ja#part"
        rendered = weekly.render_bibliography({"bibliography": [{
            "key": "w2026w37special", "title": "A% & B_# $ ^ ~ {C}",
            "author": "R&D_#", "url": url, "urldate": "2026-09-19",
        }]})
        self.assertIn(r"A\% \& B\_\# \$ \textasciicircum{} \textasciitilde{} \{C\}", rendered)
        self.assertIn(r"R\&D\_\#", rendered)
        self.assertIn(url, rendered)
        with self.assertRaisesRegex(ValueError, "unsafe bibliography title"):
            weekly.render_bibliography({"bibliography": [{
                "key": "w2026w37special", "title": "A\\input{secret}",
                "author": "Author", "url": url, "urldate": "2026-09-19",
            }]})

    def test_unbraced_repository_includes_are_rejected(self) -> None:
        base = "\\usepackage{jgaisurvey}\n\\addbibresource{references.bib}\n"
        for command in (r"\input secret", r"\include secret", r"\input{secret}"):
            with self.subTest(command=command), self.assertRaisesRegex(ValueError, "include"):
                weekly.validate_generated_closure(base + command, "")
            with self.subTest(style=command), self.assertRaisesRegex(ValueError, "include"):
                weekly.validate_generated_closure(base, command)
