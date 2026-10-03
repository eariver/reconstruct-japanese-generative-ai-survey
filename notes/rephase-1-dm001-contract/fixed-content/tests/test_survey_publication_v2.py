from __future__ import annotations

import shutil
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from scripts import survey_publication_v2 as publication
from scripts import survey_quality_v2 as quality
from scripts import survey_reader_publication_v2 as reader


class SurveyPublicationV2Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.source_root = Path(".").resolve()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for rel in [
            quality.QUALITY_SCHEMA,
            quality.core.DEFAULT_CONFIG,
            reader.MANUSCRIPT_SCHEMA,
            reader.REVIEW_SCHEMA,
            reader.ARCHITECTURE_SCHEMA,
            reader.ARCHITECTURE_APPROVAL_SCHEMA,
            reader.REVIEW_CONTRACT,
            publication.CANDIDATE_SCHEMA,
            publication.PREVIEW_APPROVAL_SCHEMA,
            publication.FREEZE_SCHEMA,
            publication.RELEASE_MANIFEST_SCHEMA,
            publication.MERGE_VERIFICATION_SCHEMA,
            publication.RELEASE_RECORD_SCHEMA,
        ]:
            dst = self.root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(self.source_root / rel, dst)
        self.now = datetime(2026, 8, 23, 7, 0, tzinfo=timezone.utc)
        self.dummy_sha = "a" * 64

    @staticmethod
    def _fixture_pdf(page_count: int = 12) -> bytes:
        from io import BytesIO

        from pypdf import PdfWriter

        stream = BytesIO()
        writer = PdfWriter()
        for _ in range(page_count):
            writer.add_blank_page(width=612, height=792)
        writer.write(stream)
        return stream.getvalue()

    def _profile(self, issue_id: str, research_profile: str, publication_profile: str) -> Path:
        if research_profile == "WEEKLY":
            temporal = {
                "mode": "ROLLING_WINDOW",
                "window_start": "2026-08-14T22:00:00Z",
                "window_end": "2026-08-21T22:00:00Z",
                "cutoff": "2026-08-21T22:00:00Z",
                "timezone": "America/New_York",
            }
        elif research_profile == "RETROSPECTIVE_PERIOD":
            temporal = {
                "mode": "BOUNDED_PERIOD",
                "start": "2025-01-01T00:00:00+09:00",
                "end": "2025-12-31T23:59:59+09:00",
                "as_of": "2026-08-23T07:00:00Z",
                "timezone": "Asia/Tokyo",
            }
        else:
            temporal = {"mode": "OPEN_HISTORY_AS_OF", "as_of": "2026-08-23T07:00:00Z"}
        survey_root = f"surveys/{'weekly' if publication_profile == 'WEEKLY_MAGAZINE' else 'special'}/{issue_id}"
        path = self.root / f"sources/{issue_id}/production-profile.json"
        quality.core.write_json(
            path,
            {
                "schema_version": "2.0-rc1",
                "issue_id": issue_id,
                "research_profile": research_profile,
                "publication_profile": publication_profile,
                "research_scope": {
                    "question": "Fixture publication question",
                    "inclusion": [],
                    "exclusion": [],
                    "scope_dimensions": ["fixture"],
                    "initial_obligations": [
                        {"obligation_id": "fixture:coverage", "dimension": "fixture", "description": "Fixture coverage"}
                    ],
                    "temporal_policy": temporal,
                },
                "paths": {
                    "source_root": f"sources/{issue_id}",
                    "survey_root": survey_root,
                    "work_branch": f"test/{issue_id}",
                },
                "contract": {
                    "pipeline_contract_version": "fixture",
                    "pipeline_contract_sha256": self.dummy_sha,
                    "quality_contract_version": "fixture",
                    "quality_contract_sha256": self.dummy_sha,
                    "research_profile_version": "fixture",
                    "research_profile_sha256": self.dummy_sha,
                    "publication_profile_version": "fixture",
                    "publication_profile_sha256": self.dummy_sha,
                },
            },
        )
        return path

    def _architecture(self, issue_id: str, research_profile: str, publication_profile: str, requirements: list[str]) -> tuple[Path, Path]:
        root = self.root / f"sources/{issue_id}"
        architecture = root / "architecture-v2.json"
        quality.core.write_json(
            architecture,
            {
                "schema_version": "2.0-rc1",
                "issue_id": issue_id,
                "research_profile": research_profile,
                "publication_profile": publication_profile,
                "status": "APPROVED",
                "basis": {
                    "production_profile_sha256": self.dummy_sha,
                    "profile_completeness_sha256": self.dummy_sha,
                    "materiality_ledger_sha256": self.dummy_sha,
                    "candidate_matrix_sha256": self.dummy_sha,
                    "candidate_selection_sha256": self.dummy_sha,
                },
                "editorial_thesis": "Fixture thesis",
                "architecture_goals": ["Explain the selected material to readers"],
                "page_plan": {"target_pages": 12, "max_pages": 24, "notes": "planning envelope"},
                "packages": [
                    {
                        "package_id": "PKG-1",
                        "title": "Fixture package",
                        "purpose": "Fixture purpose",
                        "primary_candidate_ids": ["C-1"],
                        "supporting_candidate_ids": [],
                        "must_cover_requirements": requirements,
                        "boundaries": ["Keep claims source-bounded"],
                        "drafting_order": 1,
                        "profile_extensions": {},
                        "publication_extensions": {},
                    }
                ],
                "selected_exceptions": [],
                "profile_extensions": {},
                "publication_extensions": {},
                "human_review": {
                    "reviewed_by": "human-reviewer",
                    "reviewed_at": "2026-08-23T07:00:00Z",
                    "review_reference": "fixture:architecture",
                },
            },
        )
        approval = root / "gates/architecture-approval.json"
        quality.core.write_json(
            approval,
            {
                "schema_version": "2.0-rc1",
                "approval_id": f"architecture:{issue_id}:fixture",
                "issue_id": issue_id,
                "gate": "ARCHITECTURE_REVIEW",
                "decision": "APPROVED",
                "architecture_sha256": quality.core.sha256_file(architecture),
                "architecture_review_summary_sha256": self.dummy_sha,
                "architecture_review_attention_sha256": self.dummy_sha,
                "reviewed_by": "human-reviewer",
                "reviewed_at": "2026-08-23T07:00:00Z",
                "review_reference": "fixture:architecture",
            },
        )
        return architecture, approval

    def _deterministic_checks(self, research_profile: str, publication_profile: str, directory: Path) -> list[dict[str, object]]:
        cfg = quality.core.load_json(self.root / quality.core.DEFAULT_CONFIG)
        expected = quality.expected_checks_by_kind(cfg, research_profile, publication_profile, {"DETERMINISTIC"})
        rows: list[dict[str, object]] = []
        for check_id in sorted(expected):
            result_path = directory / "quality-results" / f"{check_id}.json"
            quality.core.write_json(result_path, {"check_id": check_id, "status": "PASS"})
            rows.append({
                "check_id": check_id,
                "kind": "DETERMINISTIC",
                "status": "PASS",
                "executor": "fixture-tool",
                "evidence": f"fixture:{check_id}",
                "recorded_at": "2026-08-23T07:00:00Z",
                "result": {
                    "path": str(result_path.relative_to(self.root)),
                    "sha256": quality.core.sha256_file(result_path),
                },
            })
        return rows

    def _review_checks(self, profile_path: Path, kind: str) -> list[dict[str, object]]:
        profile = quality.core.load_json(profile_path)
        ids = reader._expected_review_checks(self.root, profile, kind)
        rows: list[dict[str, object]] = []
        exact_blocks = {
            "Subsection 1.1 — Concrete transition",
            "Subsection 1.2 — Remaining boundary",
        }
        for check_id in sorted(ids):
            evidence_locations = ["main.tex:fixture"]
            if profile["publication_profile"] == "LONGFORM_SPECIAL" and kind == "SEMANTIC_EDITORIAL":
                if check_id in {"ARCHITECTURE_CONTENT_FIDELITY", "LONGFORM_TECHNICAL_DEPTH"}:
                    evidence_locations.extend(sorted({"package:PKG-1"} | exact_blocks))
                if check_id == "FINAL_SYNTHESIS_QUALITY":
                    evidence_locations.extend(
                        ["package:PKG-1", "reader-role:final-synthesis", "Section 1 — Final synthesis"]
                    )
            if (
                profile["publication_profile"] == "LONGFORM_SPECIAL"
                and kind == "VISUAL"
                and check_id == "LONGFORM_MIXED_LAYOUT"
            ):
                evidence_locations.extend(
                    [
                        "reader-layout:balanced-two-column-narrative",
                        "reader-layout:wide-surfaces-full-width",
                        "reader-layout:references-one-column",
                    ]
                )
            rows.append(
                {
                    "check_id": check_id,
                    "status": "PASS",
                    "detail": f"Explicit ChatGPT review passed {check_id}",
                    "evidence_locations": evidence_locations,
                }
            )
        return rows

    @staticmethod
    def _longform_fixture_source() -> str:
        transition = (
            "This reader-facing block explains a concrete technical transition, its source-bounded significance, "
            "deployment implications, and the distinction between measured facts and interpretation. " * 12
        )
        boundary = (
            "This reader-facing block explains the remaining claim boundary, source-specific limitations, "
            "distribution conditions, and why unlike measurements are not collapsed into a ranking. " * 12
        )
        return (
            "\\section{Final synthesis}\n"
            "\\subsection{Concrete transition}\n"
            + transition
            + "\\autocite{fixtureA}\n"
            "\\subsection{Remaining boundary}\n"
            + boundary
            + "\\autocite{fixtureB}\n"
        )

    def _candidate(self, issue_id: str = "SP001", research_profile: str = "THEMATIC", publication_profile: str = "LONGFORM_SPECIAL") -> dict[str, Path]:
        profile = self._profile(issue_id, research_profile, publication_profile)
        architecture, architecture_approval = self._architecture(
            issue_id, research_profile, publication_profile, ["Explain concrete transition", "Explain remaining boundary"]
        )
        survey_root = self.root / quality.core.load_json(profile)["paths"]["survey_root"]
        survey_root.mkdir(parents=True, exist_ok=True)
        source = survey_root / "main.tex"
        bibliography = survey_root / "references.bib"
        pdf = survey_root / "main.pdf"
        if publication_profile == "LONGFORM_SPECIAL":
            source.write_text(self._longform_fixture_source(), encoding="utf-8")
            bibliography.write_text(
                "@misc{fixtureA,title={Fixture A}}\n@misc{fixtureB,title={Fixture B}}\n",
                encoding="utf-8",
            )
            architecture_coverage = [
                {
                    "package_id": "PKG-1",
                    "requirement": "Explain concrete transition",
                    "status": "FULFILLED",
                    "reader_locations": ["Subsection 1.1 — Concrete transition"],
                    "detail": "Reader prose explains the transition in a distinct substantive block",
                },
                {
                    "package_id": "PKG-1",
                    "requirement": "Explain remaining boundary",
                    "status": "FULFILLED",
                    "reader_locations": ["Subsection 1.2 — Remaining boundary"],
                    "detail": "Reader prose explains the remaining boundary in a distinct substantive block",
                },
            ]
            requirements = [
                {
                    "requirement_id": "FINAL_SYNTHESIS",
                    "status": "FULFILLED",
                    "reader_locations": ["Section 1 — Final synthesis"],
                    "detail": "Final synthesis remains reader-visible and substantive",
                }
            ]
        else:
            source.write_text("reader-facing source with final synthesis\n", encoding="utf-8")
            bibliography.write_text("@misc{fixture,title={Fixture}}\n", encoding="utf-8")
            architecture_coverage = [
                {"package_id": "PKG-1", "requirement": "Explain concrete transition", "status": "FULFILLED", "reader_locations": ["main.tex:transition"], "detail": "Reader prose explains transition"},
                {"package_id": "PKG-1", "requirement": "Explain remaining boundary", "status": "FULFILLED", "reader_locations": ["main.tex:boundary"], "detail": "Reader prose explains boundary"},
            ]
            requirements = [
                {"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED", "reader_locations": ["main.tex:summary"], "detail": "Final synthesis authored"}
            ]
        pdf.write_bytes(self._fixture_pdf(12))
        publication_dir = self.root / f"sources/{issue_id}/publication/v2"
        publication_dir.mkdir(parents=True, exist_ok=True)
        manifest = publication_dir / "reader-manuscript-v2.json"
        if research_profile == "WEEKLY":
            requirements.append({"requirement_id": "WEEKLY_COMMUNITY_MOVEMENT", "status": "FULFILLED", "reader_locations": ["main.tex:community"], "detail": "Weekly community movement authored"})
        reader.build_manuscript_manifest(
            self.root,
            issue_id,
            profile,
            architecture,
            architecture_approval,
            source,
            [{"role": "BIBLIOGRAPHY", "path": bibliography}],
            architecture_coverage,
            requirements,
            "ChatGPT",
            self.now,
            manifest,
        )
        bundle = publication_dir / "quality-regression-bundle-v2.json"
        quality.build_bundle(
            self.root,
            issue_id,
            source,
            pdf,
            self._deterministic_checks(research_profile, publication_profile, publication_dir),
            bundle,
            production_profile_path=profile,
        )
        semantic = publication_dir / "semantic-editorial-review-v2.json"
        visual = publication_dir / "visual-review-v2.json"
        reader.build_review_record(
            self.root, manifest, pdf, 12, "SEMANTIC_EDITORIAL", self._review_checks(profile, "SEMANTIC_EDITORIAL"), "ChatGPT", self.now, semantic
        )
        reader.build_review_record(
            self.root, manifest, pdf, 12, "VISUAL", self._review_checks(profile, "VISUAL"), "ChatGPT", self.now, visual
        )
        candidate = publication_dir / "publication-candidate-v2.json"
        publication.build_candidate(
            self.root,
            issue_id,
            publication_profile,
            manifest,
            source,
            pdf,
            12,
            bundle,
            semantic,
            visual,
            candidate,
        )
        return {
            "profile": profile,
            "architecture": architecture,
            "approval": architecture_approval,
            "source": source,
            "pdf": pdf,
            "manifest": manifest,
            "bundle": bundle,
            "semantic": semantic,
            "visual": visual,
            "candidate": candidate,
            "publication_dir": publication_dir,
        }

    def test_exact_reviewed_pdf_chain_reaches_release_without_postapproval_quality_gate(self) -> None:
        paths = self._candidate()
        approval = paths["publication_dir"] / "publication-preview-approval-v2.json"
        publication.build_preview_approval(self.root, paths["candidate"], approval, "human-reviewer", self.now, "review:SP001:preview")
        freeze = paths["publication_dir"] / "freeze-record-v2.json"
        release_manifest = paths["publication_dir"] / "release-manifest-v2.json"
        publication.build_freeze(self.root, paths["candidate"], approval, self.now, freeze, release_manifest)
        verification = paths["publication_dir"] / "merge-verification-v2.json"
        publication.build_merge_verification(self.root, release_manifest, "a" * 40, self.now, verification)
        release = paths["publication_dir"] / "release-record-v2.json"
        publication.build_release_record(self.root, release_manifest, verification, self.now, "release:SP001", release)
        record = publication.validate_release_record(self.root, release)
        self.assertEqual(record["status"], "RELEASED")
        self.assertEqual(record["release_identity"], "special/SP001")
        freeze_data = quality.core.load_json(freeze)
        candidate_data = publication.validate_candidate(self.root, paths["candidate"])
        self.assertEqual(freeze_data["visual_review_path"], candidate_data["visual_review"]["path"])

    def test_review_page_count_must_match_exact_pdf_bytes(self) -> None:
        paths = self._candidate()
        with self.assertRaisesRegex(ValueError, "asserted=18 actual=12"):
            reader.build_review_record(
                self.root,
                paths["manifest"],
                paths["pdf"],
                18,
                "SEMANTIC_EDITORIAL",
                self._review_checks(paths["profile"], "SEMANTIC_EDITORIAL"),
                "ChatGPT",
                self.now,
                paths["publication_dir"] / "mismatched-page-count-review.json",
            )

    def test_candidate_rejects_actions_only_pdf_authority_because_exact_reviewed_bytes_must_be_repository_resident(self) -> None:
        paths = self._candidate()
        bundle_path = paths["publication_dir"] / "actions-quality.json"
        authority = {
            "storage": "GITHUB_ACTIONS_ARTIFACT",
            "path": "main.pdf",
            "sha256": quality.core.sha256_file(paths["pdf"]),
            "byte_count": paths["pdf"].stat().st_size,
            "actions_artifact": {
                "repository": "eariver/japanese-generative-ai-survey",
                "workflow_run_id": 1,
                "artifact_id": 2,
                "artifact_name": "fixture",
                "artifact_digest": "sha256:" + "b" * 64,
            },
        }
        profile = paths["profile"]
        quality.build_bundle(
            self.root,
            "SP001",
            paths["source"],
            paths["pdf"],
            self._deterministic_checks("THEMATIC", "LONGFORM_SPECIAL", paths["publication_dir"] / "actions"),
            bundle_path,
            authority,
            production_profile_path=profile,
        )
        with self.assertRaisesRegex(ValueError, "requires exact reviewed PDF bytes in repository storage"):
            publication.build_candidate(
                self.root,
                "SP001",
                "LONGFORM_SPECIAL",
                paths["manifest"],
                paths["source"],
                paths["pdf"],
                12,
                bundle_path,
                paths["semantic"],
                paths["visual"],
                paths["publication_dir"] / "actions-candidate.json",
            )

    def test_pdf_change_after_human_preview_invalidates_downstream_chain(self) -> None:
        paths = self._candidate()
        approval = paths["publication_dir"] / "publication-preview-approval-v2.json"
        publication.build_preview_approval(self.root, paths["candidate"], approval, "human-reviewer", self.now, "review:SP001:preview")
        paths["pdf"].write_bytes(b"%PDF-1.7\nchanged-after-review\n")
        with self.assertRaises(ValueError):
            publication.validate_preview_approval(self.root, approval)

    def test_missing_architecture_coverage_blocks_reader_manifest(self) -> None:
        profile = self._profile("SP002", "THEMATIC", "LONGFORM_SPECIAL")
        architecture, approval = self._architecture("SP002", "THEMATIC", "LONGFORM_SPECIAL", ["A", "B"])
        source = self.root / "surveys/special/SP002/main.tex"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("reader source\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "coverage mismatch"):
            reader.build_manuscript_manifest(
                self.root,
                "SP002",
                profile,
                architecture,
                approval,
                source,
                [],
                [{"package_id": "PKG-1", "requirement": "A", "status": "FULFILLED", "reader_locations": ["main.tex:A"], "detail": "A covered"}],
                [{"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED", "reader_locations": ["main.tex:summary"], "detail": "summary"}],
                "ChatGPT",
                self.now,
                self.root / "sources/SP002/publication/v2/reader-manuscript-v2.json",
            )

    def test_weekly_requires_community_movement_before_candidate_work(self) -> None:
        profile = self._profile("2026-W34", "WEEKLY", "WEEKLY_MAGAZINE")
        architecture, approval = self._architecture("2026-W34", "WEEKLY", "WEEKLY_MAGAZINE", ["Explain week"])
        source = self.root / "surveys/weekly/2026-W34/main.tex"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("weekly source\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Reader requirement set differs"):
            reader.build_manuscript_manifest(
                self.root,
                "2026-W34",
                profile,
                architecture,
                approval,
                source,
                [],
                [{"package_id": "PKG-1", "requirement": "Explain week", "status": "FULFILLED", "reader_locations": ["main.tex:week"], "detail": "week explained"}],
                [{"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED", "reader_locations": ["main.tex:summary"], "detail": "summary"}],
                "ChatGPT",
                self.now,
                self.root / "sources/2026-W34/publication/v2/reader-manuscript-v2.json",
            )

    def test_review_contract_preserves_thematic_longform_and_retrospective_semantics(self) -> None:
        thematic = self._profile("SP003", "THEMATIC", "LONGFORM_SPECIAL")
        thematic_ids = {row["check_id"] for row in self._review_checks(thematic, "SEMANTIC_EDITORIAL")}
        self.assertIn("PUBLICATION_BOUNDARY", thematic_ids)
        self.assertIn("ARCHITECTURE_CONTENT_FIDELITY", thematic_ids)
        self.assertIn("FINAL_SYNTHESIS_QUALITY", thematic_ids)
        self.assertIn("LONGFORM_TECHNICAL_DEPTH", thematic_ids)
        self.assertIn("THEMATIC_RESEARCH_CLOSURE", thematic_ids)
        self.assertIn("THEMATIC_HISTORICAL_ATTRIBUTION", thematic_ids)

        retrospective = self._profile("SP-2025-Y", "RETROSPECTIVE_PERIOD", "LONGFORM_SPECIAL")
        retrospective_ids = {row["check_id"] for row in self._review_checks(retrospective, "SEMANTIC_EDITORIAL")}
        self.assertIn("REQUIRED_SYNTHESIS_SURVIVAL", retrospective_ids)
        self.assertIn("LONGFORM_TECHNICAL_DEPTH", retrospective_ids)
        self.assertNotIn("WEEKLY_COMMUNITY_MOVEMENT", retrospective_ids)

    def test_release_manifest_fails_if_frozen_source_changes(self) -> None:
        paths = self._candidate()
        approval = paths["publication_dir"] / "publication-preview-approval-v2.json"
        publication.build_preview_approval(self.root, paths["candidate"], approval, "human-reviewer", self.now, "review:SP001:preview")
        freeze = paths["publication_dir"] / "freeze-record-v2.json"
        manifest = paths["publication_dir"] / "release-manifest-v2.json"
        publication.build_freeze(self.root, paths["candidate"], approval, self.now, freeze, manifest)
        paths["source"].write_text("changed after freeze\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "frozen artifact bytes drift"):
            publication.validate_release_manifest(self.root, manifest)


if __name__ == "__main__":
    unittest.main()
