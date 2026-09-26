from __future__ import annotations
import shutil
import unittest
from pathlib import Path
from unittest import mock

from scripts import survey_production_v2 as core
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
        return chain

    def test_accepted_weekly_chain_probe(self) -> None:
        chain = self._chain()
        self.assertEqual(chain["draft_package"]["issue_id"], ISSUE)

