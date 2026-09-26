from __future__ import annotations

import copy
import unittest
from pathlib import Path

from scripts import survey_production_v2 as core
from scripts import survey_weekly_derivation_v2 as weekly
from tests import test_survey_increment_b_weekly_derivation_v2 as fixture_module


class WeeklyEvidenceAuthorityJoinTests(unittest.TestCase):
    def _fixture(self) -> tuple[fixture_module.IncrementBWeeklyDerivationV2Tests, dict, Path, dict]:
        # The shared helper builds real accepted Core authority and its own
        # independent Git database; none of its TestCase methods are discovered.
        fixture = fixture_module.IncrementBWeeklyDerivationV2Tests(methodName="runTest")
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        chain = fixture._complete_authorities(fixture._chain())
        state_path = fixture._current_state(chain)
        context = weekly.load_derivation(fixture.root, state_path, chain["authored_path"])
        return fixture, chain, state_path, context

    def test_join_uses_only_accepted_core_authorities(self):
        fixture, chain, _state_path, context = self._fixture()
        records, card_refs = weekly._records_from_authorities(
            fixture.root, chain["matrix_path"], chain["ledger_path"],
            chain["discovery_accepted"], chain["evidence"], fixture.head,
        )
        self.assertEqual(records, context["records"])
        did = next(iter(records))
        record = records[did]
        matrix = core.load_json(chain["matrix_path"])
        matrix_row = next(row for row in matrix["rows"] if did in row["discovery_ids"])
        discovery = core.load_json(chain["discovery_accepted"])
        locator = next(row["source_locator"] for row in discovery["records"] if row["discovery_id"] == did)
        acceptance = core.load_json(chain["evidence"])
        accepted_row = next(row for row in acceptance["results"] if did in row["discovery_ids"])
        card_path = chain["evidence"].parent / "results" / accepted_row["filename"]
        card = core.load_json(card_path)
        source = next(row for row in card["sources"] if row["url"] == locator)
        self.assertEqual(record["title"], matrix_row["title"])
        self.assertEqual(record["author"], "Unknown")
        self.assertEqual(record["url"], locator)
        self.assertEqual(record["status"], accepted_row["status"])
        self.assertEqual(record["materiality"], matrix_row["materiality"])
        self.assertEqual(record["source_accessed_at"], source["accessed_at"])
        self.assertEqual(record["urldate"], source["accessed_at"][:10])
        self.assertTrue(any(
            row["name"] == f"evidence-card:{accepted_row['evidence_task_id']}"
            and row["sha256"] == core.sha256_file(card_path)
            for row in card_refs
        ))

    def test_join_fails_closed_on_evidence_status_drift(self):
        fixture, chain, state_path, _context = self._fixture()
        matrix = core.load_json(chain["matrix_path"])
        altered = copy.deepcopy(matrix)
        altered["rows"][0]["evidence_status"] = "PARTIAL" if matrix["rows"][0]["evidence_status"] != "PARTIAL" else "VERIFIED"
        synthetic_matrix = fixture.root / "synthetic-status-drift-matrix.json"
        core.write_json(synthetic_matrix, altered)
        # A separate matrix copy reaches the join after real accepted Evidence
        # validation. This loader-plus-join negative is not State-adopted authority.
        with self.assertRaisesRegex(ValueError, "Evidence status authority mismatch"):
            weekly._records_from_authorities(
                fixture.root, synthetic_matrix, chain["ledger_path"],
                chain["discovery_accepted"], chain["evidence"], fixture.head,
            )

        # Changing the canonical matrix cannot bypass its exact checkpoint.
        matrix_path = chain["matrix_path"]
        original = matrix_path.read_bytes()
        self.addCleanup(matrix_path.write_bytes, original)
        core.write_json(matrix_path, altered)
        with self.assertRaisesRegex(ValueError, "Production State invalid|checkpoint"):
            weekly.load_derivation(fixture.root, state_path, chain["authored_path"])


if __name__ == "__main__":
    unittest.main()
