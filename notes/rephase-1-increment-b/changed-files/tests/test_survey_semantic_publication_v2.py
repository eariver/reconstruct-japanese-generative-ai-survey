from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import survey_production_v2 as core
from scripts import survey_semantic_quality_v2 as semantic_quality
from scripts import survey_weekly_derivation_v2 as weekly


class WeeklySemanticPublicationTests(unittest.TestCase):
    def test_weekly_window_uses_rolling_window_wall_time(self):
        profile = {
            "research_scope": {
                "temporal_policy": {
                    "mode": "ROLLING_WINDOW",
                    "window_start": "2026-08-07T18:00:00-04:00",
                    "window_end": "2026-08-14T18:00:00-04:00",
                    "cutoff": "2026-08-14T18:00:00-04:00",
                    "timezone": "America/New_York",
                }
            }
        }
        display, boundary = weekly._window(profile)
        self.assertEqual(display, "2026-08-14")
        self.assertEqual(
            boundary,
            "Window: 2026-08-07 18:00 - 2026-08-14 18:00 America/New_York",
        )

    def test_closing_summary_requires_architecture_source(self):
        architecture = {
            "publication_extensions": {
                "closing_summary": {
                    "required": True,
                    "heading": "今週の総括",
                    "placement": "after_body_before_references",
                }
            },
            "profile_extensions": {
                "weekly_closing_summary": {
                    "required": True,
                    "source": "profile_synthesis.current_interpretation",
                }
            },
        }
        self.assertEqual(
            weekly._closing_summary(architecture),
            ("今週の総括", "after_body_before_references"),
        )
        architecture["profile_extensions"]["weekly_closing_summary"]["source"] = "free_text"
        with self.assertRaisesRegex(ValueError, "profile_synthesis.current_interpretation"):
            weekly._closing_summary(architecture)

    def test_bib_text_omits_internal_evidence_materiality(self):
        surface = {"bibliography": [{
            "discovery_id": "example001", "key": "w2026w34example001",
            "title": "Example Source Title", "author": "Unknown",
            "url": "https://example.com/source", "urldate": "2026-08-21",
        }]}
        text = weekly.render_bibliography(surface)
        self.assertIn("w2026w34example001", text)
        self.assertIn("Example Source Title", text)
        self.assertIn("https://example.com/source", text)
        self.assertIn("2026-08-21", text)
        self.assertIn("@online{w2026w34example001,", text)
        self.assertNotIn("Core v2", text)
        self.assertNotIn("Evidence:", text)
        self.assertNotIn("VERIFIED", text)
        self.assertNotIn("materiality", text)
        self.assertNotIn("MATERIAL", text)

    def test_input_heading_is_architecture_bound(self):
        data = {
            "schema_version": "2.0-rc1",
            "issue_id": "2026-W33",
            "runner": "WEEKLY_MAGAZINE",
            "cover": {"headline": "H", "deck": "D", "anchors": ["A"]},
            "frontmatter": {"heading": "F", "lede": "L", "scope_notes": ["S"]},
            "final_summary": {
                "heading": "今週の総括",
                "paragraphs": ["p1", "p2", "p3"],
            },
        }
        weekly._validate_authored_input(data, "2026-W33", "今週の総括")
        data["final_summary"]["heading"] = "この号の総括"
        with self.assertRaisesRegex(ValueError, "approved Architecture"):
            weekly._validate_authored_input(data, "2026-W33", "今週の総括")


class SemanticQualityFinalizerTests(unittest.TestCase):
    def test_missing_deterministic_quality_family_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config").mkdir(parents=True)
            shutil.copyfile(Path(core.DEFAULT_CONFIG), root / core.DEFAULT_CONFIG)
            source_root = root / "sources/2026-W33"
            survey_root = root / "surveys/weekly/2026-W33"
            (source_root / "publication/v2/quality").mkdir(parents=True)
            survey_root.mkdir(parents=True)
            source = survey_root / "main.tex"
            source.write_text("weekly source\n", encoding="utf-8")
            pdf = source_root / "publication/v2/2026-W33-publication-preview.pdf"
            pdf.write_bytes(b"%PDF-1.4\nweekly\n")
            profile = {
                "issue_id": "2026-W33",
                "research_profile": "WEEKLY",
                "publication_profile": "WEEKLY_MAGAZINE",
                "paths": {
                    "source_root": "sources/2026-W33",
                    "survey_root": "surveys/weekly/2026-W33",
                    "work_branch": "weekly/2026-W33-v2-work",
                },
            }
            profile_path = source_root / "production-profile.json"
            core.write_json(profile_path, profile)
            state = {
                "issue_id": "2026-W33",
                "lifecycle_state": "DRAFT_COMPLETE",
                "next_action": "stage:semantic-publication-validation",
                "profile": {"path": "sources/2026-W33/production-profile.json"},
            }
            state_path = source_root / "production-state.json"
            core.write_json(state_path, state)
            preflight = {
                "check_id": "PDF_PREFLIGHT",
                "status": "PASS",
                "pdf_sha256": core.sha256_file(pdf),
                "page_count": 8,
                "byte_count": pdf.stat().st_size,
            }
            core.write_json(source_root / "publication/v2/quality/pdf-preflight.json", preflight)
            request = {
                "schema_version": "2.0-rc1",
                "issue_id": "2026-W33",
                "runner": "CORE_V2_SEMANTIC_QUALITY",
                "source": {"path": str(source.relative_to(root)), "sha256": core.sha256_file(source)},
                "pdf": {
                    "path": str(pdf.relative_to(root)),
                    "sha256": core.sha256_file(pdf),
                    "byte_count": pdf.stat().st_size,
                },
                "page_count": 8,
                "deterministic_results": [],
                "reviews": [],
                "recorded_at": "2026-08-23T01:00:00Z",
            }
            request_path = source_root / "quality-request.json"
            core.write_json(request_path, request)
            with self.assertRaisesRegex(ValueError, "deterministic quality family incomplete"):
                semantic_quality.validate_request(root, state_path, request_path)


if __name__ == "__main__":
    unittest.main()
