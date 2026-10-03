from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import survey_profiled_freeze_v2 as profiled
from scripts import survey_quality_v2 as quality


class SurveyProfiledFreezeV2Tests(unittest.TestCase):
    def profile(self, issue_id: str, research_profile: str, publication_profile: str, survey_root: str) -> dict:
        return {
            "issue_id": issue_id,
            "research_profile": research_profile,
            "publication_profile": publication_profile,
            "paths": {"survey_root": survey_root},
        }

    def test_retrospective_internal_id_preserves_existing_public_special_slug(self) -> None:
        profile = self.profile(
            "SP-2025-H2", "RETROSPECTIVE_PERIOD", "LONGFORM_SPECIAL", "surveys/special/2025-H2"
        )
        self.assertEqual(profiled.public_issue_slug(profile), "2025-H2")
        self.assertEqual(profiled.release_identity(profile), "special/2025-H2")

    def test_thematic_and_weekly_public_identity_remain_natural(self) -> None:
        thematic = self.profile("SP001", "THEMATIC", "LONGFORM_SPECIAL", "surveys/special/SP001")
        weekly = self.profile("2026-W35", "WEEKLY", "WEEKLY_MAGAZINE", "surveys/weekly/2026-W35")
        self.assertEqual(profiled.release_identity(thematic), "special/SP001")
        self.assertEqual(profiled.release_identity(weekly), "weekly/2026-W35")

    def test_release_workflow_rederives_tag_title_and_asset_from_profile_slug(self) -> None:
        text = Path(".github/workflows/survey-production-v2-release.yml").read_text(encoding="utf-8")
        self.assertIn("from scripts import survey_profiled_freeze_v2 as profiled", text)
        self.assertIn("public_slug=profiled.public_issue_slug(profile)", text)
        self.assertIn("expected_tag=profiled.release_identity(profile)", text)
        self.assertIn("if tag != expected_tag", text)
        self.assertIn("Technical Survey Special — {public_slug}", text)
        self.assertIn("Technical_Survey_Special_{public_slug}.pdf", text)
        self.assertNotIn("if tag not in {f'weekly/{issue}',f'special/{issue}'}", text)

    def test_quality_authority_remains_bound_to_profile_publication_identity(self) -> None:
        """The redesigned Quality Bundle owns deterministic QA only, but still cannot drift Profile identity."""
        source_root = Path(".").resolve()
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            for rel in (quality.QUALITY_SCHEMA, quality.core.DEFAULT_CONFIG):
                dst = root / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_root / rel, dst)

            profile_path = root / "sources/SP001/production-profile.json"
            dummy_sha = "a" * 64
            quality.core.write_json(
                profile_path,
                {
                    "schema_version": "2.0-rc1",
                    "issue_id": "SP001",
                    "research_profile": "THEMATIC",
                    "publication_profile": "LONGFORM_SPECIAL",
                    "research_scope": {
                        "question": "Fixture",
                        "inclusion": [],
                        "exclusion": [],
                        "scope_dimensions": ["fixture"],
                        "initial_obligations": [
                            {
                                "obligation_id": "fixture:1",
                                "dimension": "fixture",
                                "description": "Bind deterministic QA to the Production Profile.",
                            }
                        ],
                        "temporal_policy": {
                            "mode": "OPEN_HISTORY_AS_OF",
                            "as_of": "2026-08-22T09:00:00Z",
                        },
                    },
                    "paths": {
                        "source_root": "sources/SP001",
                        "survey_root": "surveys/special/SP001",
                        "work_branch": "test/SP001",
                    },
                    "contract": {
                        "pipeline_contract_version": "fixture",
                        "pipeline_contract_sha256": dummy_sha,
                        "quality_contract_version": "fixture",
                        "quality_contract_sha256": dummy_sha,
                        "research_profile_version": "fixture",
                        "research_profile_sha256": dummy_sha,
                        "publication_profile_version": "fixture",
                        "publication_profile_sha256": dummy_sha,
                    },
                },
            )

            source = root / "surveys/special/SP001/main.tex"
            pdf = root / "surveys/special/SP001/main.pdf"
            source.parent.mkdir(parents=True)
            source.write_text("reader-facing source\n", encoding="utf-8")
            pdf.write_bytes(b"%PDF-1.7\nfixture\n")

            cfg = quality.core.load_json(root / quality.core.DEFAULT_CONFIG)
            checks = []
            for check_id in sorted(
                quality.expected_checks_by_kind(cfg, "THEMATIC", "LONGFORM_SPECIAL", {"DETERMINISTIC"})
            ):
                result_path = root / "quality/results" / f"{check_id}.json"
                quality.core.write_json(result_path, {"check_id": check_id, "status": "PASS"})
                checks.append(
                    {
                        "check_id": check_id,
                        "kind": "DETERMINISTIC",
                        "status": "PASS",
                        "executor": "fixture-tool",
                        "evidence": "fixture deterministic evidence",
                        "recorded_at": "2026-08-22T09:00:00Z",
                        "result": {
                            "path": str(result_path.relative_to(root)),
                            "sha256": quality.core.sha256_file(result_path),
                        },
                    }
                )

            bundle = root / "quality/bundle.json"
            quality.build_bundle(
                root,
                "SP001",
                source,
                pdf,
                checks,
                bundle,
                production_profile_path=profile_path,
            )
            payload = quality.validate_bundle(root, bundle, issue_id="SP001")
            self.assertEqual(payload["publication_profile"], "LONGFORM_SPECIAL")
            self.assertTrue(all(row["kind"] == "DETERMINISTIC" for row in payload["checks"]))

            mutated_profile = quality.core.load_json(profile_path)
            mutated_profile["publication_profile"] = "WEEKLY_MAGAZINE"
            quality.core.write_json(profile_path, mutated_profile)
            with self.assertRaisesRegex(ValueError, "Profile authority drift"):
                quality.validate_bundle(root, bundle, issue_id="SP001")


if __name__ == "__main__":
    unittest.main()
