#!/usr/bin/env python3
"""Narrow evidence-only regression, SECOND harness (valid-task subject negative).

Outside shipping tree. Imports ACTUAL final proof modules + actual existing fixture
APIs (no mocks, no state-basis stub, no fake class default). Uses genuine valid
task/meta/package/card from real Screening/Evidence builders on FINAL proof
(single-DID single-source per task; package holds >=2 separately valid single-DID
tasks for multi-DID at package level, NOT one invented 2DID task). Then primary
mismatch negative changes ONLY claim PRIMARY_SUBJECT ID against artifact primary;
asserts exact one error and no coercion.

Scope (honest, no combined-invalid claim): complements existing multi-source explicit
bindings (runner.test_multiple...) + real multiDID operation (DERIVED test_23/24);
covers ambiguity on a VALID task (single-source, single-DID) without claiming
every combination (multi-source + multi-DID + ambiguous primary in one invalid task
is NOT claimed — first harness 233000Z is preserved as leaf card-gate probe with
explicit task-schema limitation, not valid accepted task).

Valid control must pass task/package checks AND card validator (not only card partial gate).
"""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

PROOF = "/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/profile-support-packaging-20261031T202327Z/proof-copy/candidate-partial-b40de60"
if PROOF not in sys.path:
    sys.path.insert(0, PROOF)

from scripts import survey_evidence_v2 as evidence  # noqa: E402  actual proof modules
from scripts import survey_production_v2 as core  # noqa: E402
from tests import test_survey_evidence_v2 as evidence_tests  # noqa: E402  actual fixture APIs


class ValidTaskSubjectTests(unittest.TestCase):
    def test_control_two_valid_single_did_tasks_pass_task_package_and_card(self) -> None:
        helper = evidence_tests.SurveyEvidenceV2Tests(methodName="test_evidence_package_is_exact_and_preserves_task_bytes")
        helper.setUp()
        try:
            # Fixture APIs resolve base files via helper.repo_root; point at FINAL proof (real source, no mock).
            helper.repo_root = Path(PROOF)
            temp, root, cfg = helper.sandbox()
            self.addCleanup(temp.cleanup)
            profile_path, state_path = helper.init_profile(root, cfg, "THEMATIC")
            head = core.repository_commit_sha(root)
            issue_id = core.load_json(state_path)["issue_id"]
            rec1 = helper.discovery(issue_id, "target-source")
            rec2 = helper.discovery(issue_id, "second-source")
            discovery_path, screening_acceptance = helper.make_screening(
                root, state_path, [rec1, rec2], {"target-source": "KEEP", "second-source": "KEEP"})
            package_path, evidence_acceptance = helper.make_evidence(
                root, state_path, discovery_path, screening_acceptance)
            package = core.load_json(package_path)
            # Multi-DID at package level: >=2 separately valid single-DID tasks (no invented 2DID task).
            self.assertEqual(len(package["tasks"]), 2)
            acceptance_sha = package["basis"]["screening_acceptance_sha256"]
            for meta in package["tasks"]:
                task = core.load_json(package_path.parent / meta["path"])
                # Genuine valid single-DID single-source per task.
                self.assertEqual(len(task["discovery_ids"]), 1)
                self.assertEqual(len(task["source_records"]), len(task["discovery_ids"]))
                # Task/package checks (not only card partial gate).
                self.assertEqual(evidence._validate_task(task, meta, acceptance_sha), [])
            # Card validator on genuine valid cards (errors == [], no coercion needed).
            for meta in package["tasks"]:
                task = core.load_json(package_path.parent / meta["path"])
                card = helper.card_for_task(root, package_path, meta)
                self.assertEqual(
                    evidence.validate_evidence_card(card, task, meta["sha256"], package, repo_root=root), [])
        finally:
            helper.tearDown() if hasattr(helper, "tearDown") else None

    def test_negative_valid_task_primary_mismatch_refused_no_coercion(self) -> None:
        helper = evidence_tests.SurveyEvidenceV2Tests(methodName="test_evidence_package_is_exact_and_preserves_task_bytes")
        helper.setUp()
        try:
            # Fixture APIs resolve base files via helper.repo_root; point at FINAL proof (real source, no mock).
            helper.repo_root = Path(PROOF)
            temp, root, cfg = helper.sandbox()
            self.addCleanup(temp.cleanup)
            profile_path, state_path = helper.init_profile(root, cfg, "THEMATIC")
            issue_id = core.load_json(state_path)["issue_id"]
            rec1 = helper.discovery(issue_id, "target-source")
            rec2 = helper.discovery(issue_id, "second-source")
            discovery_path, screening_acceptance = helper.make_screening(
                root, state_path, [rec1, rec2], {"target-source": "KEEP", "second-source": "KEEP"})
            package_path, evidence_acceptance = helper.make_evidence(
                root, state_path, discovery_path, screening_acceptance)
            package = core.load_json(package_path)
            meta = package["tasks"][0]
            task = core.load_json(package_path.parent / meta["path"])
            card = helper.card_for_task(root, package_path, meta)
            # Sanity: genuine valid card passes (control for this task).
            self.assertEqual(
                evidence.validate_evidence_card(card, task, meta["sha256"], package, repo_root=root), [])
            # Negative changes ONLY claim PRIMARY_SUBJECT ID (target -> comparator,
            # both registered entities so not "not a registered entity").
            bad = copy.deepcopy(card)
            # claims[0] is the factual claim (see card_for_task); metrics empty.
            bad["claims"][0]["subject_id"] = "comparator"
            bad["claims"][0]["subject_role"] = "PRIMARY_SUBJECT"
            self.assertEqual(
                evidence.validate_evidence_card(bad, task, meta["sha256"], package, repo_root=root),
                ["claims claim-1 PRIMARY_SUBJECT must bind artifact.primary_subject_id"],
            )
        finally:
            helper.tearDown() if hasattr(helper, "tearDown") else None


if __name__ == "__main__":
    unittest.main()
