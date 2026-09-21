"""Connected regression for the approved Publication Preview-to-Freeze boundary.

All research, editorial, visual, and Human decisions in this module are
synthetic fixture records.  The tests exercise real production validators and
checkpoint/state transitions; they are not publication or approval evidence.
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

from scripts import survey_agent_control_v2 as agent
from scripts import survey_production_v2 as core
from scripts import survey_publication_v2 as publication
from scripts import survey_stage_validation_v2 as stage_validation


ROOT = Path(".").resolve()
_REVALIDATION_SPEC = importlib.util.spec_from_file_location(
    "freeze_boundary_revalidation_fixture",
    ROOT / "tests/test_survey_publication_revalidation_v2.py",
)
assert _REVALIDATION_SPEC is not None and _REVALIDATION_SPEC.loader is not None
_REVALIDATION = importlib.util.module_from_spec(_REVALIDATION_SPEC)
_REVALIDATION_SPEC.loader.exec_module(_REVALIDATION)
Fixture = _REVALIDATION.Fixture
ISSUE = _REVALIDATION.ISSUE
T0 = _REVALIDATION.T0


class FreezeStageBoundaryV2Tests(unittest.TestCase):
    """Real-loader boundary tests over synthetic Weekly publication authority."""

    def setUp(self) -> None:
        self.root = ROOT
        self.cfg = core.load_json(self.root / core.DEFAULT_CONFIG)

    def make_fixture(self) -> Fixture:
        temp = tempfile.TemporaryDirectory(dir=str(self.root))
        self.addCleanup(temp.cleanup)
        return Fixture(self.root, Path(temp.name))

    def build_candidate_and_advance(self, fix: Fixture) -> Path:
        pub = fix.src / "publication/v2"
        candidate = pub / "publication-candidate-v2.json"
        publication.build_candidate(
            self.root,
            ISSUE,
            "WEEKLY_MAGAZINE",
            pub / "reader-manuscript-v2.json",
            fix.survey / "main.tex",
            fix.survey / "main.pdf",
            1,
            pub / "quality-regression-bundle-v2.json",
            pub / "semantic-editorial-review-v2.json",
            pub / "visual-review-v2.json",
            candidate,
        )
        report = fix.src / "execution/validated-draft-stage-report.json"
        stage_validation.validate_stage(
            self.root,
            self.cfg,
            fix.src / "production-state.json",
            {"publication-candidate": candidate},
            report,
            T0 + timedelta(hours=1),
        )
        reviews = fix.src / "execution/validated-draft-reviews.json"
        core.write_json(
            reviews,
            {
                "reviews": [
                    {
                        "check_id": "CORE_STAGE_CONTRACT",
                        "kind": "DETERMINISTIC",
                        "executor": "synthetic-freeze-boundary-fixture",
                        "evidence": "synthetic connected stage validation",
                        "result_path": str(report.relative_to(self.root)),
                    }
                ]
            },
        )
        checkpoint = agent.build_stage_checkpoint(
            self.root,
            self.cfg,
            fix.src / "production-state.json",
            {"publication-candidate": candidate},
            reviews,
            "Synthetic Publication Candidate boundary",
            T0 + timedelta(hours=1, minutes=1),
        )
        updated = agent.advance_with_checkpoint(
            self.root, self.cfg, fix.src / "production-state.json", checkpoint
        )
        self.assertEqual(updated["lifecycle_state"], "RELEASE_CANDIDATE")
        self.assertEqual(updated["terminal_reason"], "HUMAN_GATE_REACHED")
        return candidate

    def approve_and_build_freeze(self, fix: Fixture, candidate: Path) -> dict[str, Path]:
        agent.approve_publication_preview(
            self.root,
            self.cfg,
            fix.src / "production-state.json",
            "synthetic-human-fixture",
            T0 + timedelta(hours=2),
            "synthetic:publication-preview",
        )
        pub = fix.src / "publication/v2"
        approval = fix.src / self.cfg["state_authority"]["publication_preview_approval_path"]
        freeze, manifest = publication.build_freeze(
            self.root,
            candidate,
            approval,
            T0 + timedelta(hours=3),
            pub / "freeze-record-v2.json",
            pub / "release-manifest-v2.json",
        )
        candidate_payload = publication.validate_candidate(self.root, candidate, issue_id=ISSUE)
        visual = self.root / candidate_payload["visual_review"]["path"]
        return {
            "visual-review-record": visual,
            "freeze-record": freeze,
            "release-manifest": manifest,
        }

    def validate_freeze_stage(self, fix: Fixture, artifacts: dict[str, Path], suffix: str) -> Path:
        output = fix.src / f"execution/freeze-stage-report-{suffix}.json"
        return stage_validation.validate_stage(
            self.root,
            self.cfg,
            fix.src / "production-state.json",
            artifacts,
            output,
            T0 + timedelta(hours=4),
        )

    def test_approved_preview_resolves_as_typed_authority(self) -> None:
        fix = self.make_fixture()
        candidate = self.build_candidate_and_advance(fix)
        self.approve_and_build_freeze(fix, candidate)
        state = core.load_json(fix.src / "production-state.json")
        artifacts = stage_validation._prior_artifacts(self.root, self.cfg, state)
        self.assertEqual(artifacts["publication-candidate"], candidate)

    def test_weekly_approved_preview_advances_through_real_freeze_boundary(self) -> None:
        fix = self.make_fixture()
        candidate = self.build_candidate_and_advance(fix)
        artifacts = self.approve_and_build_freeze(fix, candidate)
        report = self.validate_freeze_stage(fix, artifacts, "positive")
        report_payload = core.load_json(report)
        self.assertEqual(
            {row["name"] for row in report_payload["artifacts"]},
            {"visual-review-record", "freeze-record", "release-manifest"},
        )
        reviews = fix.src / "execution/freeze-reviews.json"
        core.write_json(
            reviews,
            {
                "reviews": [
                    {
                        "check_id": "CORE_STAGE_CONTRACT",
                        "kind": "DETERMINISTIC",
                        "executor": "synthetic-freeze-boundary-fixture",
                        "evidence": "synthetic exact-authority Freeze validation",
                        "result_path": str(report.relative_to(self.root)),
                    }
                ]
            },
        )
        checkpoint = agent.build_stage_checkpoint(
            self.root,
            self.cfg,
            fix.src / "production-state.json",
            artifacts,
            reviews,
            "Synthetic exact-authority Freeze boundary",
            T0 + timedelta(hours=4, minutes=1),
        )
        updated = agent.advance_with_checkpoint(
            self.root, self.cfg, fix.src / "production-state.json", checkpoint
        )
        self.assertEqual(updated["lifecycle_state"], "FROZEN")
        self.assertEqual(updated["machine_checkpoints"]["freeze"], "passed")
        self.assertEqual(agent.validate_agent_state(self.root, self.cfg, updated), [])

    def test_freeze_artifact_set_rejects_missing_extra_and_wrong_visual(self) -> None:
        for case in ("missing", "extra", "wrong"):
            with self.subTest(case=case):
                fix = self.make_fixture()
                candidate = self.build_candidate_and_advance(fix)
                artifacts = self.approve_and_build_freeze(fix, candidate)
                expected = ""
                if case == "missing":
                    artifacts.pop("visual-review-record")
                    expected = "current stage artifacts missing: visual-review-record"
                elif case == "extra":
                    artifacts["legacy-postapproval-visual"] = artifacts["visual-review-record"]
                    expected = "unexpected current stage artifacts: legacy-postapproval-visual"
                else:
                    alternate = fix.src / "publication/v2/copied-visual-review-v2.json"
                    alternate.write_bytes(artifacts["visual-review-record"].read_bytes())
                    artifacts["visual-review-record"] = alternate
                    expected = "must be the Candidate pre-preview Visual Review"
                with self.assertRaisesRegex(stage_validation.StageValidationError, expected):
                    self.validate_freeze_stage(fix, artifacts, case)

    def test_pending_preview_cannot_enter_freeze_even_if_approval_file_is_inert(self) -> None:
        fix = self.make_fixture()
        candidate = self.build_candidate_and_advance(fix)
        approval = fix.src / self.cfg["state_authority"]["publication_preview_approval_path"]
        publication.build_preview_approval(
            self.root,
            candidate,
            approval,
            "synthetic-human-fixture",
            T0 + timedelta(hours=2),
            "synthetic:inert-preview-file",
        )
        pub = fix.src / "publication/v2"
        freeze, manifest = publication.build_freeze(
            self.root,
            candidate,
            approval,
            T0 + timedelta(hours=3),
            pub / "freeze-record-v2.json",
            pub / "release-manifest-v2.json",
        )
        visual = self.root / publication.validate_candidate(self.root, candidate)["visual_review"]["path"]
        with self.assertRaisesRegex(stage_validation.StageValidationError, "waiting at a Human Gate"):
            self.validate_freeze_stage(
                fix,
                {
                    "visual-review-record": visual,
                    "freeze-record": freeze,
                    "release-manifest": manifest,
                },
                "pending",
            )

    def test_missing_and_divergent_approval_authority_fail_closed(self) -> None:
        for case in ("missing", "divergent"):
            with self.subTest(case=case):
                fix = self.make_fixture()
                candidate = self.build_candidate_and_advance(fix)
                artifacts = self.approve_and_build_freeze(fix, candidate)
                state_path = fix.src / "production-state.json"
                approval = fix.src / self.cfg["state_authority"]["publication_preview_approval_path"]
                if case == "missing":
                    approval.unlink()
                    expected = "approval provenance drift"
                else:
                    state = core.load_json(state_path)
                    state["human_gate_provenance"]["publication_preview"] = {
                        **state["human_gate_provenance"]["publication_preview"],
                        "sha256": "f" * 64,
                    }
                    core.write_json(state_path, state)
                    expected = "Human Preview and checkpoint approval authorities disagree"
                with self.assertRaisesRegex(stage_validation.StageValidationError, expected):
                    self.validate_freeze_stage(fix, artifacts, case)

    def test_candidate_byte_drift_and_approval_hash_refresh_forgery_fail_closed(self) -> None:
        for case in ("candidate-byte-drift", "approval-hash-refresh"):
            with self.subTest(case=case):
                fix = self.make_fixture()
                candidate = self.build_candidate_and_advance(fix)
                artifacts = self.approve_and_build_freeze(fix, candidate)
                state_path = fix.src / "production-state.json"
                approval = fix.src / self.cfg["state_authority"]["publication_preview_approval_path"]
                if case == "candidate-byte-drift":
                    candidate.write_bytes(candidate.read_bytes() + b"\n")
                    expected = "approved candidate bytes drifted"
                else:
                    forged = core.load_json(approval)
                    forged["publication_candidate_sha256"] = "e" * 64
                    approval.write_text(json.dumps(forged), encoding="utf-8")
                    refreshed = {"path": str(approval.relative_to(self.root)), "sha256": core.sha256_file(approval)}
                    state = core.load_json(state_path)
                    state["human_gate_provenance"]["publication_preview"] = dict(refreshed)
                    state["checkpoint_provenance"]["publication_preview"] = dict(refreshed)
                    core.write_json(state_path, state)
                    expected = "approved candidate bytes drifted"
                with self.assertRaisesRegex(stage_validation.StageValidationError, expected):
                    self.validate_freeze_stage(fix, artifacts, case)

    def test_non_publication_checkpoint_typed_record_is_not_silently_skipped(self) -> None:
        fix = self.make_fixture()
        candidate = self.build_candidate_and_advance(fix)
        artifacts = self.approve_and_build_freeze(fix, candidate)
        state_path = fix.src / "production-state.json"
        state = core.load_json(state_path)
        state["checkpoint_provenance"]["architecture"] = dict(
            state["checkpoint_provenance"]["publication_preview"]
        )
        core.write_json(state_path, state)
        with self.assertRaisesRegex(stage_validation.StageValidationError, "Stage Checkpoint"):
            self.validate_freeze_stage(fix, artifacts, "typed-non-stage")

    def test_active_publication_revalidation_survives_freeze_boundary(self) -> None:
        fix = self.make_fixture()
        pub = fix.src / "publication/v2"
        for name in (
            "reader-manuscript-v2.json",
            "quality-regression-bundle-v2.json",
            "semantic-editorial-review-v2.json",
            "visual-review-v2.json",
            "reader-surface-gate-v2.json",
        ):
            (pub / name).unlink()
        fix._publication_files(version=2)
        fix._publication_authority()
        revalidation = agent.revalidate_publication_surface(
            self.root,
            self.cfg,
            fix.src / "production-state.json",
            "REVIEWED_CORE_CHANGE",
            "synthetic reviewed rendering change",
            "synthetic-revalidation-fixture",
            T0 + timedelta(minutes=30),
            None,
        )
        self.assertTrue(revalidation.is_file())
        candidate = self.build_candidate_and_advance(fix)
        artifacts = self.approve_and_build_freeze(fix, candidate)
        report = self.validate_freeze_stage(fix, artifacts, "revalidated")
        self.assertEqual(core.load_json(report)["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
