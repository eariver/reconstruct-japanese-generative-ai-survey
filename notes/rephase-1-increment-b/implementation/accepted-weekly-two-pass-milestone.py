from __future__ import annotations
import shutil
import copy
import json
import subprocess
import sys
import unittest
from datetime import timedelta
from pathlib import Path
from unittest import mock

from scripts import survey_production_v2 as core
from scripts import survey_agent_control_v2 as agent
from scripts import survey_discovery_v2 as discovery
from scripts import survey_drafting_v2 as drafting
from scripts import survey_x_intake_v2 as xintake
from scripts import survey_stage_validation_v2 as stage_validation
from scripts import survey_weekly_semantic_publication_v2 as weekly_publication
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
        self.root = Path(".").resolve()
        self.cfg = core.load_json(self.root / core.DEFAULT_CONFIG)
        self.head = core.repository_commit_sha(self.root)
        self.source_root = self.root / "sources" / ISSUE
        self.survey_root = self.root / "surveys" / "weekly" / ISSUE
        if self.source_root.exists() or self.survey_root.exists():
            raise AssertionError("Weekly B test edition already exists; preserve it for inspection")

    def tearDown(self) -> None:
        for name in (
            "architecture-approval-v2.json", "architecture-review-attention-v2.json",
            "architecture-review-summary-v2.json", "architecture-v2.json",
            "selection-v2.json", "views-accepted", "views-input", "raw/source.json",
        ):
            path = (self.root / name).resolve()
            if not path.is_relative_to(self.root):
                raise AssertionError(f"test cleanup escaped fixture: {path}")
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()
        for path in (self.source_root, self.survey_root):
            if path.exists():
                if not path.resolve().is_relative_to(self.root):
                    raise AssertionError(f"test cleanup escaped fixture: {path}")
                shutil.rmtree(path)

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
        stamp = core.parse_instant(f"2026-09-19T04:{minute:02d}:00+09:00")
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
        core.write_json(review_path, review)
        with mock.patch.object(sys, "argv", argv):
            self.assertEqual(weekly_publication.main(), 0)
        receipt_path = publication_root / "validated-source-manifest.json"
        self.assertTrue(receipt_path.is_file())
        weekly.validate_receipt(self.root, receipt_path, state_path)
