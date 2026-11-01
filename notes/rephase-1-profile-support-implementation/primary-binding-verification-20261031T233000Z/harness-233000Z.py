#!/usr/bin/env python3
"""Narrow evidence-only regression: multi-source + multi-DID ambiguous PRIMARY_SUBJECT refused.

Outside shipping tree. Imports ACTUAL final proof modules (immutable source, no edits).
No mocks/success forcers, no SOURCE aliases/class default (uses real _source_class),
no false many-primaryIDs (2 entities, control vs negative differ by one subject_id).
Distinguishes source ambiguity (sources correct in both) vs entity subject
(PRIMARY_SUBJECT mismatch in negative only).

Contract 6.4 oracle: multi-source and multi-DID with ambiguous primary subject
rejected rather than coerced. Existing runner.test_multiple... (multi-source explicit
bindings, single DID, unambiguous primary) + Evidence test_issue_191 (single task,
COMPARATOR role, not multi-source/multi-DID) + ordinary 10 task/card (single-source
single-DID unambiguous) + DERIVED multiDID (obligations, no entities) do NOT cover
combined multi-source + multi-DID + ambiguous PRIMARY_SUBJECT. This harness does.
"""

from __future__ import annotations

import sys
import unittest

PROOF = "/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/profile-support-packaging-20261031T202327Z/proof-copy/candidate-partial-b40de60"
if PROOF not in sys.path:
    sys.path.insert(0, PROOF)

from scripts import survey_evidence_v2 as evidence  # noqa: E402  actual proof modules


def _task_multi() -> tuple[dict, dict, str, str, str, str]:
    # Multi-source (paper PRIMARY_PAPER + SECONDARY_REFERENCE SECONDARY, distinct
    # locators/classes via real _source_class, no alias/default) + multi-DID
    # (D-1, D-2). Dummy consistent 64-hex SHAs (validator checks equality, not files;
    # no supplement, so no repo I/O). Real shapes, no mocks.
    cls_primary = evidence._source_class("paper")
    cls_secondary = evidence._source_class("SECONDARY_REFERENCE")
    assert cls_primary == "PRIMARY_PAPER", cls_primary
    assert cls_secondary == "SECONDARY", cls_secondary
    task_sha, scr_sha, prompt_sha, card_sha = "a" * 64, "b" * 64, "c" * 64, "d" * 64
    task = {
        "schema_version": "2.0-rc1",
        "issue_id": "SP001",
        "evidence_task_id": "evidence:SP001:test-multi",
        "discovery_ids": ["D-1", "D-2"],
        "source_records": [
            {"source_type": "paper", "locator": "https://example.invalid/primary",
             "title": "Primary", "published_at": "2025-01-01T00:00:00Z"},
            {"source_type": "SECONDARY_REFERENCE", "locator": "https://example.invalid/secondary",
             "title": "Secondary", "published_at": "2025-01-01T00:00:00Z"},
        ],
        "verification_targets": ["subject identity"],
        "screening_basis": {"screening_acceptance_sha256": scr_sha, "decisions": []},
    }
    package = {
        "schema_version": "2.0-rc1",
        "issue_id": "SP001",
        "research_profile": "THEMATIC",
        "prompt": {"path": "config/prompts/evidence-verification-v2.md", "sha256": prompt_sha},
        "contracts": {
            "run_package": {"path": "schemas/evidence-v2-run-package.schema.json", "sha256": "e" * 64},
            "task": {"path": "schemas/evidence-v2-task.schema.json", "sha256": "f" * 64},
            "card": {"path": "schemas/evidence-v2-card.schema.json", "sha256": card_sha},
        },
        "tasks": [],
        "expected_outputs": {"one_result_per_task": True, "filename_rule": "same-basename-as-task"},
        "rules": [],
    }
    return task, package, task_sha, scr_sha, prompt_sha, card_sha


def _card_multi(task: dict, package: dict, task_sha: str, claim_subject: str) -> dict:
    # Two entities (target primary + other). Artifact primary = target (unambiguous).
    # claim_subject "target" (control, correct) vs "other" (negative, PRIMARY_SUBJECT mismatch).
    # Sources correct in both (source ambiguity resolved); only subject differs.
    return {
        "schema_version": "2.0-rc1",
        "issue_id": task["issue_id"],
        "evidence_task_id": task["evidence_task_id"],
        "basis": {
            "task_sha256": task_sha,
            "screening_acceptance_sha256": task["screening_basis"]["screening_acceptance_sha256"],
            "prompt_sha256": package["prompt"]["sha256"],
            "result_contract_sha256": package["contracts"]["card"]["sha256"],
        },
        "status": "VERIFIED",
        "entities": [
            {"entity_id": "target", "canonical_name": "Target",
             "entity_type": "MODEL", "organization": "Example",
             "canonical_url": "https://example.invalid/primary"},
            {"entity_id": "other", "canonical_name": "Other",
             "entity_type": "MODEL", "organization": "Other",
             "canonical_url": "https://example.invalid/secondary"},
        ],
        "artifact": {
            "primary_subject_id": "target",
            "artifact_type": "MODEL",
            "canonical_name": "Target",
            "canonical_url": "https://example.invalid/primary",
        },
        "temporal": {"observed_at": "2026-08-22T02:10:00+09:00", "events": []},
        "sources": [
            {"source_id": "source-1", "url": "https://example.invalid/primary",
             "source_class": "PRIMARY_PAPER", "title": "Primary",
             "published_at": "2025-01-01T00:00:00Z", "accessed_at": "2026-08-22T02:10:00+09:00",
             "role": "verification source"},
            {"source_id": "source-2", "url": "https://example.invalid/secondary",
             "source_class": "SECONDARY", "title": "Secondary",
             "published_at": "2025-01-01T00:00:00Z", "accessed_at": "2026-08-22T02:10:00+09:00",
             "role": "verification source"},
        ],
        "claims": [{
            "statement_id": "claim-1",
            "text": "Target introduces the tested method.",
            "subject_id": claim_subject,
            "subject_role": "PRIMARY_SUBJECT",
            "evidence_class": "AUTHOR_CLAIM",
            "source_ids": ["source-1", "source-2"],
            "context": "source-local claim",
        }],
        "metrics": [],
        "limitations": [],
        "verification": {
            "targets": [{
                "target": "subject identity",
                "status": "VERIFIED",
                "finding": "target and other are distinct",
                "subject_ids": ["target", "other"],
                "source_ids": ["source-1", "source-2"],
            }],
            "unresolved_questions": [],
            "contradictions": [],
        },
    }


class PrimaryBindingTests(unittest.TestCase):
    def test_control_multi_source_multi_did_unambiguous_primary_passes(self) -> None:
        task, package, task_sha, _, _, _ = _task_multi()
        card = _card_multi(task, package, task_sha, claim_subject="target")
        self.assertEqual(evidence.validate_evidence_card(card, task, task_sha, package), [])

    def test_negative_multi_source_multi_did_ambiguous_primary_refused_no_coercion(self) -> None:
        task, package, task_sha, _, _, _ = _task_multi()
        card = _card_multi(task, package, task_sha, claim_subject="other")
        self.assertEqual(
            evidence.validate_evidence_card(card, task, task_sha, package),
            ["claims claim-1 PRIMARY_SUBJECT must bind artifact.primary_subject_id"],
        )


if __name__ == "__main__":
    unittest.main()
