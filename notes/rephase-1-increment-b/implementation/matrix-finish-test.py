"""Focused Increment B authority-boundary controls in an isolated Git fixture.

The existing Weekly fixture supplies accepted Core records and an independent
temporary Git database. These tests do not execute its inherited test methods.
All review and research content here is synthetic, not publication approval.
"""
from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

from scripts import survey_drafting_v2 as drafting
from scripts import survey_evidence_v2 as evidence
from scripts import survey_production_v2 as core
from scripts import survey_reader_surface_gate_v2 as gate
from scripts import survey_agent_tool_v2 as runtime_tool
from scripts import survey_weekly_derivation_v2 as weekly
from scripts import survey_weekly_semantic_publication_v2 as publisher
from tests import test_survey_increment_b_weekly_derivation_v2 as fixture_module

ISSUE = fixture_module.ISSUE


class IncrementBBoundaryMatrixV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # setUp guards inherited Git overrides, copies current source into a
        # temporary directory, and initializes its own inert-origin database.
        cls.fixture = fixture_module.IncrementBWeeklyDerivationV2Tests(methodName="runTest")
        cls.fixture.setUp()
        try:
            fixture_git = cls.fixture.root / ".git"
            workspace = Path(fixture_module.__file__).resolve().parents[1]
            assert fixture_git.is_dir() and not (fixture_git / "objects/info/alternates").exists()
            assert fixture_git.resolve() != (workspace / ".git").resolve()
            fixture_source_stat = (cls.fixture.root / "scripts/survey_weekly_derivation_v2.py").stat()
            workspace_source_stat = (workspace / "scripts/survey_weekly_derivation_v2.py").stat()
            assert (fixture_source_stat.st_dev, fixture_source_stat.st_ino) != (
                workspace_source_stat.st_dev, workspace_source_stat.st_ino,
            )
            origin = subprocess.run(
                ["git", "remote", "get-url", "origin"], cwd=cls.fixture.root,
                check=True, capture_output=True, text=True,
            ).stdout.strip()
            assert origin == "https://example.invalid/weekly-b-fixture.git"
            cls.chain = cls.fixture._complete_authorities(cls.fixture._chain())
            cls.state_path = cls.fixture._current_state(cls.chain)
            cls.context = weekly.load_derivation(
                cls.fixture.root, cls.state_path, cls.chain["authored_path"]
            )
        except BaseException:
            cls.fixture.doCleanups()
            raise

    @classmethod
    def tearDownClass(cls) -> None:
        cls.fixture.doCleanups()

    def _projection_sources(self) -> dict:
        chain = self.chain
        return {
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
            "records": copy.deepcopy(self.context["records"]),
        }

    @staticmethod
    def _project(source: dict) -> dict:
        return weekly.build_reader_input(
            ISSUE, source["profile"], source["architecture"], source["authored"],
            source["synthesis"], source["ordered"], source["records"],
        )

    def test_nonreader_runner_annotation_keeps_pure_projection_but_live_checkpoint_rejects_mutation(self) -> None:
        source = self._projection_sources()
        baseline = self._project(source)
        result = source["ordered"][0]["result"]
        self.assertIsNone(result["runner"]["run_reference"])
        result["runner"]["run_reference"] = "synthetic internal runner annotation revised"
        self.assertEqual(drafting.validate_draft_result(
            result, self.chain["draft_package_path"], self.fixture.root / drafting.DRAFT_PROMPT
        ), [])
        self.assertEqual(self._project(source), baseline)  # Pure projection control only.

        result_path = self.chain["draft_result_path"]
        original = result_path.read_bytes()
        self.addCleanup(result_path.write_bytes, original)
        core.write_json(result_path, result)
        self.assertNotEqual(core.sha256_file(result_path), next(
            row["sha256"] for row in self.context["accepted_refs"]
            if row["name"].startswith("draft-result:")
        ))
        with self.assertRaisesRegex(ValueError, "Production State invalid|checkpoint|Draft"):
            weekly.load_derivation(self.fixture.root, self.state_path, self.chain["authored_path"])

    def test_authorized_alternate_citation_with_distinct_refs_rejects_stale_result(self) -> None:
        source = self._projection_sources()
        ordered = source["ordered"][0]
        package = ordered["package"]
        old_ref = ordered["result"]["deck_evidence_refs"]
        new_did = "different-authorized-source"
        new_candidate = "candidate:alternate-authorized"
        new_input = copy.deepcopy(package["evidence_inputs"][0])
        new_input["candidate_id"] = new_candidate
        new_input["evidence_task_id"] = "different-authorized-task"
        new_input["evidence_card"]["claims"][0]["statement_id"] = "different-authorized-claim"
        package["evidence_inputs"].append(new_input)
        package["candidate_matrix"]["rows"].append({
            "candidate_id": new_candidate, "discovery_ids": [new_did],
        })
        ordered["spec"]["deck_discovery_ids"] = [new_did]
        from scripts import survey_drafting_citation_refs_v2 as citation_refs
        resolved = citation_refs.refs(package, [new_did], ordered["spec"]["deck_ref_mode"])
        self.assertNotEqual(resolved, old_ref)
        with self.assertRaisesRegex(ValueError, "authored deck Discovery placement differs"):
            self._project(source)

    def test_accepted_card_bibliography_identity_and_ambiguous_capture_stop(self) -> None:
        root = self.fixture.root
        records = self.context["records"]
        did = self.context["surface"]["bibliography"][0]["discovery_id"]
        record = records[did]
        cited = self.context["surface"]["bibliography"][0]
        matrix = core.load_json(self.chain["matrix_path"])
        discovery = core.load_json(self.chain["discovery_accepted"])
        row = next(row for row in matrix["rows"] if did in row["discovery_ids"])
        locator = next(row["source_locator"] for row in discovery["records"] if row["discovery_id"] == did)
        self.assertEqual(cited["title"], row["title"])
        self.assertEqual(cited["url"], locator)
        self.assertEqual(cited["author"], "Unknown")
        self.assertEqual(cited["urldate"], record["source_accessed_at"][:10])
        bib = weekly.render_bibliography(self.context["surface"])
        fields = (
            "@online{" + cited["key"], "title = {{" + cited["title"],
            "author = {{" + cited["author"], "url = {" + cited["url"],
            "urldate = {" + cited["urldate"],
        )
        positions = [bib.index(token) for token in fields]
        self.assertEqual(positions, sorted(positions))
        self.assertTrue(cited["url"].startswith("https://"))

        accepted_dir = self.chain["evidence"].parent
        staging = root / "synthetic-ambiguous-staging"
        shutil.copytree(accepted_dir, staging)
        acceptance = core.load_json(staging / "evidence-accepted.json")
        source_row = next(row for row in acceptance["results"] if did in row["discovery_ids"])
        card_path = staging / "results" / source_row["filename"]
        card = core.load_json(card_path)
        first = next(item for item in card["sources"] if item["url"] == locator)
        duplicate = copy.deepcopy(first)
        duplicate["source_id"] = first["source_id"] + "-capture-2"
        duplicate["accessed_at"] = "2026-09-20T03:00:00+09:00"
        card["sources"].append(duplicate)
        core.write_json(card_path, card)
        source_row["sha256"] = core.sha256_file(card_path)
        digest = evidence._evidence_result_set_digest(
            acceptance["package_sha256"], acceptance["results"]
        )
        acceptance["result_set_sha256"] = digest
        accepted_dir_variant = root / "synthetic-ambiguous-accepted" / digest
        shutil.copytree(staging, accepted_dir_variant)
        accepted = accepted_dir_variant / "evidence-accepted.json"
        core.write_json(accepted, acceptance)
        # The real loader validates package, tasks, all cards, and the
        # content-addressed acceptance. The wrapper only permits the known
        # historical package State-SHA drift at the current stage.
        with runtime_tool.current_stage_basis_override():
            evidence.validate_evidence_acceptance(root, accepted, self.fixture.head)
        # A sidecar selector exists but is not accepted Evidence authority.
        core.write_json(accepted.parent / "interactive-evidence.json", {
            "records": [{"discovery_id": did, "source_bindings": [duplicate["source_id"]]}],
        })
        changed_matrix = copy.deepcopy(matrix)
        changed_matrix["basis"]["evidence_acceptance_sha256"] = core.sha256_file(accepted)
        matrix_path = root / "synthetic-ambiguous-matrix.json"
        core.write_json(matrix_path, changed_matrix)
        with self.assertRaisesRegex(ValueError, "ambiguous captures.*no unique authoritative capture"):
            weekly._records_from_authorities(
                root, matrix_path, self.chain["ledger_path"], self.chain["discovery_accepted"],
                accepted, self.fixture.head,
            )
        # A changed card with a stale accepted SHA is a separate earlier
        # authority failure, not evidence of the ambiguity boundary.
        card_path = accepted_dir_variant / "results" / source_row["filename"]
        card = core.load_json(card_path)
        card["sources"][0]["title"] += " tampered"
        core.write_json(card_path, card)
        with self.assertRaisesRegex(ValueError, "accepted Evidence result changed"):
            weekly._records_from_authorities(
                root, matrix_path, self.chain["ledger_path"], self.chain["discovery_accepted"],
                accepted, self.fixture.head,
            )

    def test_generated_schema_route_profile_and_explicit_review_target_fail_before_outputs(self) -> None:
        root = self.fixture.root
        surface = self.context["surface"]
        weekly.validate_reader_input(root, surface)
        invalids = (
            ("missing paragraphs", lambda value: value["final_summary"].pop("paragraphs")),
            ("old final_summary shape", lambda value: value.update(final_summary="obsolete")),
            ("unknown route", lambda value: value.update(route="UNKNOWN_ROUTE")),
            ("wrong research Profile", lambda value: value.update(research_profile="THEMATIC")),
            ("wrong publication Profile", lambda value: value.update(publication_profile="LONGFORM_SPECIAL")),
        )
        for name, mutate in invalids:
            with self.subTest(name=name):
                changed = copy.deepcopy(surface)
                mutate(changed)
                with self.assertRaises(ValueError):
                    weekly.validate_reader_input(root, changed)

        publication_root = self.context["source_root"] / "publication/v2"
        publication_root.mkdir(parents=True, exist_ok=True)
        canonical = publication_root / "reader-surface-input-v2.json"
        alternate = publication_root / "reviewed-other-surface.json"
        core.write_json(canonical, surface)
        core.write_json(alternate, surface)
        review_path = publication_root / "synthetic-wrong-target-review.json"
        review = {
            "schema_version": "2.0-rc1", "issue_id": ISSUE,
            "publication_profile": "WEEKLY_MAGAZINE", "review_kind": "SEMANTIC_EDITORIAL",
            "reviewed_surface": {
                "path": alternate.relative_to(root).as_posix(), "sha256": core.sha256_file(alternate),
            },
            "checks": [{
                "check_id": "READER_PIPELINE_INDEPENDENCE", "status": "PASS",
                "detail": "Synthetic review bound to a different valid reader input file.",
                "evidence_locations": ["reviewed-other-surface.json:packages"],
            }],
            "decision": "PASS", "reviewed_by": "synthetic alternate-target reviewer",
            "reviewed_at": "2026-09-19T05:00:00+09:00",
            "recorded_at": "2026-09-19T05:00:00+09:00",
            "status": "PASSED", "findings": [], "summary": "Synthetic target fixture.",
        }
        review["review_sha256"] = core.sha256_object(review)
        core.write_json(review_path, review)
        gate.load_and_validate_semantic_review(
            root, review_path, expected_issue_id=ISSUE,
            expected_publication_profile="WEEKLY_MAGAZINE",
            expected_surface_path=alternate, expected_surface_sha256=core.sha256_file(alternate),
        )
        argv = [
            "survey_weekly_semantic_publication_v2.py", "--repo-root", str(root),
            "--state", str(self.state_path), "--input", str(self.chain["authored_path"]),
            "--semantic-review", str(review_path),
        ]
        with mock.patch.object(sys, "argv", argv):
            with self.assertRaisesRegex(SystemExit, "Reviewed surface path mismatch"):
                publisher.main()
        for absent in (
            self.context["survey_root"] / "main.tex",
            self.context["survey_root"] / "references.bib",
            self.context["survey_root"] / "jgaisurvey.sty",
            publication_root / "validated-source-manifest.json",
        ):
            self.assertFalse(absent.exists(), str(absent))

    def test_direct_primary_requires_exact_reviewed_primary_bytes(self) -> None:
        root = self.fixture.root
        primary = root / "synthetic-direct-main.tex"
        other = root / "synthetic-direct-other.tex"
        primary.write_text(weekly.render_main(self.context["surface"]), encoding="utf-8")
        other.write_text(primary.read_text(encoding="utf-8") + "\n% other file\n", encoding="utf-8")
        manifest = {
            "issue_id": ISSUE, "research_profile": "WEEKLY",
            "publication_profile": "WEEKLY_MAGAZINE",
            "primary_source": {
                "path": primary.relative_to(root).as_posix(),
                "sha256": core.sha256_file(primary), "byte_count": primary.stat().st_size,
            },
        }
        selected = gate._derivation_for_manuscript(
            root, manifest, manifest["primary_source"]["path"],
            "synthetic-direct-review.json", "0" * 64,
        )
        self.assertEqual(selected, {"route": "DIRECT_PRIMARY", "scope": "PRIMARY_ONLY"})
        with self.assertRaisesRegex(ValueError, "canonical reader input"):
            gate._derivation_for_manuscript(
                root, manifest, other.relative_to(root).as_posix(),
                "synthetic-other-file-review.json", core.sha256_file(other),
            )
        primary.write_text(primary.read_text(encoding="utf-8") + "\n% changed\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "DIRECT_PRIMARY reviewed primary drift"):
            gate._derivation_for_manuscript(
                root, manifest, manifest["primary_source"]["path"],
                "synthetic-direct-review.json", "0" * 64,
            )


if __name__ == "__main__":
    unittest.main()
