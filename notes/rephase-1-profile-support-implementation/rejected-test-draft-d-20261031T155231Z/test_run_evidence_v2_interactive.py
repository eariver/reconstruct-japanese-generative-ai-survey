from __future__ import annotations

import unittest

from scripts import run_evidence_v2_interactive as interactive


class InteractiveEvidenceProfileContractTests(unittest.TestCase):
    @staticmethod
    def profile(research_profile: str) -> dict:
        issue_id = {
            "WEEKLY": "2026-W35",
            "THEMATIC": "SP001",
            "RETROSPECTIVE_PERIOD": "SP-2025-H2",
        }[research_profile]
        return {
            "issue_id": issue_id,
            "research_profile": research_profile,
            "research_scope": {
                "scope_dimensions": ["scope"],
                "initial_obligations": [{"obligation_id": "obligation-1"}],
            },
        }

    @staticmethod
    def common_record() -> dict:
        return {
            "discovery_id": "D-1",
            "status": "VERIFIED",
            "entity": {
                "entity_id": "entity-1",
                "canonical_name": "Example Model",
                "entity_type": "MODEL",
                "organization": "Example",
                "canonical_url": "https://example.invalid/model",
            },
            "artifact_type": "MODEL",
            "claims": [{
                "text": "The source identifies the example model.",
                "evidence_class": "PRIMARY_FACT",
                "context": None,
            }],
            "limitations": [],
            "verification": [{
                "target": "subject identity",
                "status": "VERIFIED",
                "finding": "The subject is explicitly identified.",
            }],
            "materiality": "MATERIAL",
            "materiality_rationale": "The bounded event is material to the profile.",
            "scope_dimensions": ["scope"],
        }

    def record(self, research_profile: str) -> dict:
        row = self.common_record()
        if research_profile == "THEMATIC":
            row.update({
                "lineage_role": "CORE",
                "branch_ids": [],
                "transition_ids": [],
                "inheritance_note": None,
                "historical_attribution_caveat": None,
            })
        elif research_profile == "WEEKLY":
            row.update({"window_relation": "MAIN_EVENT", "carry_over": False})
        return row

    def document(self, research_profile: str, row: dict | None = None) -> tuple[dict, dict]:
        profile = self.profile(research_profile)
        value = {
            "schema_version": "2.0-rc1",
            "issue_id": profile["issue_id"],
            "runner": {
                "provider": "test",
                "model": "fixture",
                "invocation": "profile-contract",
                "generated_at": "2026-09-06T00:00:00Z",
            },
            "records": [row or self.record(research_profile)],
            "completeness": {
                "obligations": [{
                    "obligation_id": "obligation-1",
                    "status": "SATISFIED",
                    "rationale": "The fixture obligation is explicitly disposed.",
                }],
                "residual_limitations": [],
                "closure": (
                    {
                        "targeted_gap_fill_completed": True,
                        "limitations": [],
                        "status": "COMPLETE",
                    }
                    if research_profile == "THEMATIC" else None
                ),
            },
        }
        return profile, value

    @staticmethod
    def _discovery_basis() -> tuple[list[dict], list[dict]]:
        # Minimal validated R/E basis for the preserved U==P old tests.
        # Uses canonical "paper" (PRIMARY_PAPER) and empty obligation_ids so
        # U==P=={"obligation-1"}; no DECLARATION_LOSS, no unknown-type refusal.
        # Real JSONL-shaped records; not compact summaries, not supplement DIDs.
        root = [{
            "discovery_id": "D-1",
            "provenance": {"origin": "BASE", "research_pass": 0, "parent_refs": [], "obligation_ids": [], "reason": "profile-support D migration basis"},
            "source": {"source_type": "paper", "collector_id": "test", "collector_run_id": "run", "observed_at": "2026-09-06T00:00:00Z", "title": "basis", "locator": "https://example.invalid/basis", "raw_paths": ["raw/basis.json"], "published_at": None, "summary_text": "basis", "metadata": {}},
        }]
        effective = [{
            "discovery_id": "D-1",
            "provenance": {"origin": "BASE", "research_pass": 0, "parent_refs": [], "obligation_ids": [], "reason": "profile-support D migration basis"},
            "source": {"source_type": "paper", "collector_id": "test", "collector_run_id": "run", "observed_at": "2026-09-06T00:00:00Z", "title": "basis", "locator": "https://example.invalid/basis", "raw_paths": ["raw/basis.json"], "published_at": None, "summary_text": "basis", "metadata": {}},
        }]
        return root, effective

    def validate(self, research_profile: str, row: dict | None = None, task_sources=None):
        profile, document = self.document(research_profile, row)
        root_records, effective_records = self._discovery_basis()
        return interactive.validate_interactive_input(
            document,
            profile,
            {"D-1"},
            task_sources,
            discovery_records=effective_records,
            root_discovery_records=root_records,
        )

    def test_weekly_input_passes_without_thematic_fields(self) -> None:
        by_id, _, _ = self.validate("WEEKLY")
        self.assertEqual(by_id["D-1"]["window_relation"], "MAIN_EVENT")

    def test_weekly_rejects_thematic_only_fields(self) -> None:
        row = self.record("WEEKLY")
        row["lineage_role"] = "CORE"
        with self.assertRaisesRegex(ValueError, "fields invalid"):
            self.validate("WEEKLY", row)

    def test_thematic_input_requires_and_accepts_thematic_fields(self) -> None:
        by_id, _, _ = self.validate("THEMATIC")
        self.assertEqual(by_id["D-1"]["lineage_role"], "CORE")

        row = self.common_record()
        with self.assertRaisesRegex(ValueError, "fields invalid"):
            self.validate("THEMATIC", row)

    def test_retrospective_input_passes_without_thematic_fields(self) -> None:
        by_id, _, _ = self.validate("RETROSPECTIVE_PERIOD")
        self.assertNotIn("lineage_role", by_id["D-1"])

    def test_retrospective_rejects_thematic_only_fields(self) -> None:
        row = self.record("THEMATIC")
        row["discovery_id"] = "D-1"
        with self.assertRaisesRegex(ValueError, "fields invalid"):
            self.validate("RETROSPECTIVE_PERIOD", row)

    def test_retrospective_rejects_weekly_only_fields(self) -> None:
        row = self.record("RETROSPECTIVE_PERIOD")
        row.update({"window_relation": "MAIN_EVENT", "carry_over": False})
        with self.assertRaisesRegex(ValueError, "fields invalid"):
            self.validate("RETROSPECTIVE_PERIOD", row)

    def test_multiple_task_bound_sources_require_explicit_bindings(self) -> None:
        task_sources = {"D-1": {"src-1", "supplement-src-1234567890abcdef"}}
        with self.assertRaisesRegex(ValueError, "source_bindings is required"):
            self.validate("WEEKLY", task_sources=task_sources)

        row = self.record("WEEKLY")
        row["source_bindings"] = ["supplement-src-1234567890abcdef"]
        self.validate("WEEKLY", row, task_sources)

    def test_single_source_legacy_input_remains_backward_compatible(self) -> None:
        task_sources = {"D-1": {"src-1"}}
        by_id, _, _ = self.validate("WEEKLY", task_sources=task_sources)
        self.assertNotIn("source_bindings", by_id["D-1"])


if __name__ == "__main__":
    unittest.main()
