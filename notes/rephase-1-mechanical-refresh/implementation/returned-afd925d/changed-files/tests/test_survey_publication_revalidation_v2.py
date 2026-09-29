"""Regression tests for post-VALIDATED_DRAFT publication-surface revalidation.

Covers instruction T1-T12 plus the T13 W34-defect-shape chain on generic
fixtures (the full-fidelity W34 disposable proof runs separately and is
recorded in the repair worklog). No edition-specific conditionals exist in
the implementation; T12 proves profile/path genericity functionally.
"""
from __future__ import annotations

import shutil
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from pypdf import PdfWriter

from scripts import survey_agent_control_v2 as agent
from scripts import survey_drafting_v2_base as drafting_base
from scripts import survey_production_v2 as core
from scripts import survey_publication_v2 as publication
from scripts import survey_quality_v2 as quality
from scripts import survey_stage_validation_v2 as stage_validation

ISSUE = "2026-W35"
EXECUTOR = "revalidation-regression-fixture"
T0 = datetime(2026, 9, 12, 12, 0, 0, tzinfo=timezone.utc)

PRODUCERS = [
    ("discovery", "ISSUE_INITIALIZED", "DISCOVERY_COLLECTED"),
    ("screening", "DISCOVERY_COLLECTED", "CANDIDATES_NORMALIZED"),
    ("evidence", "CANDIDATES_NORMALIZED", "EVIDENCE_REVIEWED"),
    ("materiality", "CANDIDATES_NORMALIZED", "EVIDENCE_REVIEWED"),
    ("completeness", "CANDIDATES_NORMALIZED", "EVIDENCE_REVIEWED"),
    ("selection", "EVIDENCE_REVIEWED", "SELECTION_COMPLETE"),
    ("architecture", "SELECTION_COMPLETE", "ARCHITECTURE_ESTABLISHED"),
    ("draft", "ARCHITECTURE_ESTABLISHED", "DRAFT_COMPLETE"),
    ("validation", "DRAFT_COMPLETE", "VALIDATED_DRAFT"),
]


def _hex(n: int) -> str:
    return f"{n:040x}"


class Fixture:
    """Minimal synthetic VALIDATED_DRAFT edition with real validators passing."""

    def __init__(self, root: Path, base: Path, survey_dirname: str = "survey"):
        self.repo = root
        self.cfg = core.load_json(root / core.DEFAULT_CONFIG)
        self.base = base
        self.src = self.base / "src"
        self.survey = self.base / survey_dirname
        self.src.mkdir(parents=True)
        self.survey.mkdir(parents=True)
        (self.src / "publication" / "v2").mkdir(parents=True)
        (self.src / "draft").mkdir(parents=True)
        (self.src / "evidence").mkdir(parents=True)
        (self.src / "gates").mkdir(parents=True)
        (self.src / "orchestration" / "v2" / "checkpoints").mkdir(parents=True)
        (self.src / "execution").mkdir(parents=True)
        self.profile = self._profile()
        core.write_json(self.src / "production-profile.json", self.profile)
        self._authority_files()
        self._publication_files(version=1)
        self._approval_files()
        self._publication_authority()
        self._write_state(provisional=True)
        self._checkpoint_records()
        self._write_state(provisional=False)

    def _profile(self) -> dict:
        return {
            "schema_version": self.cfg["schema_version"],
            "issue_id": ISSUE,
            "research_profile": "WEEKLY",
            "publication_profile": "WEEKLY_MAGAZINE",
            "research_scope": {
                "question": "Can publication bytes be rebound after validation?",
                "inclusion": ["weekly publication"],
                "exclusion": ["upstream research"],
                "scope_dimensions": ["revalidation"],
                "initial_obligations": [
                    {"obligation_id": "ob-1", "dimension": "revalidation", "description": "rebind safely"}
                ],
                "temporal_policy": {
                    "mode": "ROLLING_WINDOW",
                    "window_start": "2026-08-21T18:00:00-04:00",
                    "window_end": "2026-08-28T18:00:00-04:00",
                    "cutoff": "2026-08-28T18:00:00-04:00",
                    "timezone": "America/New_York",
                },
            },
            "paths": {
                "source_root": str(self.src.relative_to(self.repo)),
                "survey_root": str(self.survey.relative_to(self.repo)),
                "work_branch": "test/revalidation",
            },
            "contract": {
                "pipeline_contract_version": "2.0-rc1",
                "quality_contract_version": "2.0-rc1",
                "research_profile_version": "2.0-rc1",
                "publication_profile_version": "2.0-rc1",
                "pipeline_contract_sha256": "0" * 64,
                "quality_contract_sha256": "0" * 64,
                "research_profile_sha256": "0" * 64,
                "publication_profile_sha256": "0" * 64,
            },
        }

    def _authority_files(self) -> None:
        (self.src / "architecture-v2.json").write_text(
            __import__("json").dumps({
                "schema_version": "2.0-rc1",
                "issue_id": ISSUE,
                "research_profile": "WEEKLY",
                "publication_profile": "WEEKLY_MAGAZINE",
                "status": "APPROVED",
                "basis": {
                    "production_profile_sha256": "0" * 64,
                    "profile_completeness_sha256": "0" * 64,
                    "materiality_ledger_sha256": "0" * 64,
                    "candidate_matrix_sha256": "0" * 64,
                    "candidate_selection_sha256": "0" * 64,
                },
                "editorial_thesis": "Fixture thesis.",
                "architecture_goals": ["rebind safely"],
                "page_plan": {"target_pages": 2, "max_pages": 4, "notes": "fixture"},
                "packages": [{
                    "package_id": "pkg-001",
                    "title": "Fixture package",
                    "purpose": "Carry fixture content.",
                    "primary_candidate_ids": [],
                    "supporting_candidate_ids": [],
                    "must_cover_requirements": ["subject identity"],
                    "boundaries": [],
                    "drafting_order": 1,
                    "profile_extensions": {"weekly_package_role": "LATE_BREAKING"},
                    "publication_extensions": {"magazine_package_kind": "late-breaking"},
                }],
                "selected_exceptions": [],
                "profile_extensions": {},
                "publication_extensions": {},
                "human_review": {"reviewed_by": None, "reviewed_at": None, "review_reference": None},
            }),
            encoding="utf-8",
        )
        (self.src / "architecture-review-summary-v2.json").write_text("{}", encoding="utf-8")
        (self.src / "architecture-review-attention-v2.json").write_text("{}", encoding="utf-8")

    def _approval_files(self) -> None:
        import json as _json

        arch = self.src / "architecture-v2.json"
        summ = self.src / "architecture-review-summary-v2.json"
        attn = self.src / "architecture-review-attention-v2.json"
        core.write_json(self.src / "gates" / "architecture-approval.json", {
            "schema_version": "2.0-rc1",
            "approval_id": "fixture-approval-r1",
            "issue_id": ISSUE,
            "gate": "ARCHITECTURE_REVIEW",
            "decision": "APPROVED",
            "architecture_sha256": core.sha256_file(arch),
            "architecture_review_summary_sha256": core.sha256_file(summ),
            "architecture_review_attention_sha256": core.sha256_file(attn),
            "reviewed_by": "fixture-human",
            "reviewed_at": "2026-09-12T11:00:00Z",
            "review_reference": "fixture",
        })
        approval = core.load_json(self.src / "gates" / "architecture-approval.json")
        assert not drafting_base.validate_architecture_approval(approval, arch, summ, ISSUE)

    def _write_pdf(self, version: int = 1) -> None:
        writer = PdfWriter()
        writer.add_blank_page(width=595, height=842)
        writer.add_metadata({"/Title": "fixture-publication-v%d" % version})
        with (self.survey / "main.pdf").open("wb") as handle:
            writer.write(handle)

    def _publication_files(self, version: int) -> None:
        (self.survey / "main.tex").write_text(
            "%% fixture source v%d\n\\documentclass{article}\\begin{document}hi\\end{document}\n" % version,
            encoding="utf-8",
        )
        (self.survey / "references.bib").write_text(
            "@online{fixturekey%02d,\n  title = {{T%d}},\n  author = {{A}},\n"
            "  url = {https://example.invalid/%d},\n  urldate = {2026-08-28}\n}\n" % (version, version, version),
            encoding="utf-8",
        )
        self._write_pdf(version)

    def _contract_report(self, record_path: Path, from_state: str, to_state: str, artifacts: list) -> Path:
        report_path = record_path.parent / (record_path.stem + "-core-contract.json")
        state_path = self.src / "production-state.json"
        core.write_json(report_path, {
            "schema_version": "2.0-rc1",
            "check_id": "CORE_STAGE_CONTRACT",
            "status": "PASS",
            "issue_id": ISSUE,
            "from_state": from_state,
            "to_state": to_state,
            "production_state": {"path": str((self.src / "production-state.json").relative_to(self.repo)),
                                   "sha256": core.sha256_file(state_path) if state_path.is_file() else "0" * 64},
            "production_profile": {
                "path": str((self.src / "production-profile.json").relative_to(self.repo)),
                "sha256": core.sha256_file(self.src / "production-profile.json"),
            },
            "implementation_commit_sha": core.repository_commit_sha(self.repo),
            "contract": core.contract_identity(self.repo, self.cfg, "WEEKLY", "WEEKLY_MAGAZINE"),
            "artifacts": artifacts,
            "recorded_at": "2026-09-12T11:00:00Z",
        })
        return report_path

    def _checkpoint_records(self) -> None:
        import json as _json

        (self.src / "evidence" / "evidence-accepted.json").write_text('{"records": []}', encoding="utf-8")
        (self.src / "draft" / "draft-note.json").write_text('{"note": "v1"}', encoding="utf-8")
        for name in ("screening-accepted.json", "edition-views-accepted.json",
                     "materiality-ledger.json", "profile-completeness.json",
                     "candidate-matrix.json", "candidate-selection.json",
                     "synthesis-input.json", "synthesis-result.json"):
            (self.src / name).write_text('{"fixture": "%s"}' % name, encoding="utf-8")
        F = lambda *parts: self.src.joinpath(*parts)
        self._stage_rows = {
            "discovery": [("discovery-acceptance", F("discovery-accepted.json"))],
            "screening": [("screening-acceptance", F("screening-accepted.json"))],
            "evidence": [("evidence-acceptance", F("evidence", "evidence-accepted.json")),
                         ("edition-views-acceptance", F("edition-views-accepted.json")),
                         ("materiality-ledger", F("materiality-ledger.json")),
                         ("profile-completeness", F("profile-completeness.json"))],
            "materiality": [("evidence-acceptance", F("evidence", "evidence-accepted.json")),
                            ("edition-views-acceptance", F("edition-views-accepted.json")),
                            ("materiality-ledger", F("materiality-ledger.json")),
                            ("profile-completeness", F("profile-completeness.json"))],
            "completeness": [("evidence-acceptance", F("evidence", "evidence-accepted.json")),
                             ("edition-views-acceptance", F("edition-views-accepted.json")),
                             ("materiality-ledger", F("materiality-ledger.json")),
                             ("profile-completeness", F("profile-completeness.json"))],
            "selection": [("candidate-matrix", F("candidate-matrix.json")),
                          ("candidate-selection", F("candidate-selection.json")),
                          ("draft-note", F("draft", "draft-note.json"))],
            "architecture": [("issue-architecture", F("architecture-v2.json")),
                             ("architecture-review-summary", F("architecture-review-summary-v2.json")),
                             ("architecture-review-attention", F("architecture-review-attention-v2.json"))],
            "draft": [("synthesis-input", F("synthesis-input.json")),
                      ("synthesis-result", F("synthesis-result.json"))],
        }
        (self.src / "discovery-accepted.json").write_text('{"accepted": true}', encoding="utf-8")
        self._stage_rows["discovery"] = [("discovery-acceptance", self.src / "discovery-accepted.json")]
        stamp = T0
        for name, from_state, to_state in PRODUCERS:
            stamp = stamp + timedelta(minutes=1)
            record_path = self.src / "orchestration" / "v2" / "checkpoints" / f"{from_state}.json"
            artifacts = [
                {"name": n, "path": str(p.relative_to(self.repo)), "sha256": core.sha256_file(p)}
                for n, p in self._stage_rows.get(name, [])
            ]
            if name == "validation":
                artifacts = artifacts + [
                    {"name": n, "path": str((self.src / "publication" / "v2" / f).relative_to(self.repo)),
                     "sha256": core.sha256_file(self.src / "publication" / "v2" / f)}
                    for n, f in [
                        ("reader-manuscript", "reader-manuscript-v2.json"),
                        ("quality-regression-bundle", "quality-regression-bundle-v2.json"),
                        ("semantic-review", "semantic-editorial-review-v2.json"),
                        ("visual-review", "visual-review-v2.json"),
                        ("reader-surface-gate", "reader-surface-gate-v2.json"),
                    ]
                ] + [
                    {"name": "publication-pdf", "path": str((self.survey / "main.pdf").relative_to(self.repo)),
                     "sha256": core.sha256_file(self.survey / "main.pdf")},
                    {"name": "validated-source", "path": str((self.survey / "main.tex").relative_to(self.repo)),
                     "sha256": core.sha256_file(self.survey / "main.tex")},
                    {"name": "evidence-accepted", "path": str((self.src / "evidence" / "evidence-accepted.json").relative_to(self.repo)),
                     "sha256": core.sha256_file(self.src / "evidence" / "evidence-accepted.json")},
                ]
            report_path = self._contract_report(record_path, from_state, to_state, artifacts)
            core.write_json(record_path, {
                "schema_version": "2.0-rc1",
                "issue_id": ISSUE,
                "from_state": from_state,
                "to_state": to_state,
                "checkpoints": sorted({n for (n, f, _t) in PRODUCERS if f == from_state}),
                "recorded_at": core.iso_utc(stamp),
                "implementation": {
                    "repository_commit_sha": core.repository_commit_sha(self.repo),
                    "orchestrator_version": self.cfg["orchestrator_version"],
                },
                "contract": core.contract_identity(self.repo, self.cfg, "WEEKLY", "WEEKLY_MAGAZINE"),
                "artifacts": artifacts,
                "reviews": [{
                    "check_id": "CORE_STAGE_CONTRACT",
                    "kind": "DETERMINISTIC",
                    "status": "PASS",
                    "executor": "fixture",
                    "evidence": "fixture stage contract",
                    "result": {"path": str(report_path.relative_to(self.repo)),
                               "sha256": core.sha256_file(report_path)},
                }],
                "summary": f"fixture {name}",
            })

    def _publication_authority(self) -> None:
        from scripts import survey_reader_publication_v2 as reader

        pub = self.src / "publication" / "v2"
        support = [{"role": "SUPPORTING_SOURCE",
                    "path": str((self.survey / "references.bib").relative_to(self.repo))}]
        coverage = [{"package_id": "pkg-001", "requirement": "subject identity",
                     "status": "FULFILLED", "reader_locations": ["main.tex"],
                     "detail": "fixture coverage"}]
        requirements = [
            {"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED",
             "reader_locations": ["main.tex"], "detail": "fixture requirement"},
            {"requirement_id": "WEEKLY_COMMUNITY_MOVEMENT", "status": "FULFILLED",
             "reader_locations": ["main.tex"], "detail": "fixture requirement"},
        ]
        reader.build_manuscript_manifest(
            self.repo, ISSUE,
            self.src / "production-profile.json",
            self.src / "architecture-v2.json",
            self.src / "gates" / "architecture-approval.json",
            self.survey / "main.tex",
            support, coverage, requirements,
            EXECUTOR, T0, pub / "reader-manuscript-v2.json",
        )
        det = pub / "deterministic"
        det.mkdir(exist_ok=True)
        results = {}
        for check_id in ("IDENTIFIER_PRESERVATION", "PDF_PREFLIGHT", "SUBJECT_ENTITY_PROPERTY_BINDING"):
            p = det / f"{check_id.lower()}.json"
            core.write_json(p, {"check_id": check_id, "status": "PASS"})
            results[check_id] = {"path": str(p.relative_to(self.repo)), "sha256": core.sha256_file(p)}
        checks = [{
            "check_id": cid, "kind": "DETERMINISTIC", "status": "PASS",
            "executor": EXECUTOR, "evidence": f"fixture {cid}",
            "recorded_at": core.iso_utc(T0), "result": results[cid],
        } for cid in ("IDENTIFIER_PRESERVATION", "PDF_PREFLIGHT", "SUBJECT_ENTITY_PROPERTY_BINDING")]
        quality.build_bundle(
            self.repo, ISSUE, self.survey / "main.tex", self.survey / "main.pdf",
            checks, pub / "quality-regression-bundle-v2.json",
            production_profile_path=self.src / "production-profile.json",
        )
        expected_sem = sorted(
            [c for c, k in quality.expected_checks(self.cfg, "WEEKLY", "WEEKLY_MAGAZINE").items() if k == "AGENT_SEMANTIC"]
            + ["PUBLICATION_BOUNDARY", "ARCHITECTURE_CONTENT_FIDELITY", "FINAL_SYNTHESIS_QUALITY", "WEEKLY_COMMUNITY_MOVEMENT"]
        )
        expected_vis = sorted(
            [c for c, k in quality.expected_checks(self.cfg, "WEEKLY", "WEEKLY_MAGAZINE").items() if k == "AGENT_VISUAL"]
            + ["EXACT_PDF_VISUAL_REVIEW"]
        )
        sem_checks = [{"check_id": cid, "status": "PASS", "detail": f"fixture {cid}",
                       "evidence_locations": ["main.tex"]} for cid in expected_sem]
        vis_checks = [{"check_id": cid, "status": "PASS", "detail": f"fixture {cid}",
                       "evidence_locations": ["main.pdf"]} for cid in expected_vis]
        reader.build_review_record(
            self.repo, pub / "reader-manuscript-v2.json", self.survey / "main.pdf", 1,
            "SEMANTIC_EDITORIAL", sem_checks, EXECUTOR, T0, pub / "semantic-editorial-review-v2.json",
        )
        reader.build_review_record(
            self.repo, pub / "reader-manuscript-v2.json", self.survey / "main.pdf", 1,
            "VISUAL", vis_checks, EXECUTOR, T0, pub / "visual-review-v2.json",
        )
        # This bounded revalidation fixture reviews the exact primary only.
        sem_surface_path = self.survey / "main.tex"
        sem_rev_path = pub / "reader-surface-semantic-review-v2.json"
        sem_rev_base = {
            "schema_version": "2.0-rc1",
            "issue_id": ISSUE,
            "publication_profile": "WEEKLY_MAGAZINE",
            "review_kind": "SEMANTIC_EDITORIAL",
            "reviewed_surface": {
                "path": str(sem_surface_path.relative_to(self.repo)).replace("\\", "/"),
                "sha256": core.sha256_file(sem_surface_path),
            },
            "checks": [
                {
                    "check_id": "READER_PIPELINE_INDEPENDENCE",
                    "status": "PASS",
                    "detail": "Prose is independently understandable without internal pipeline knowledge.",
                    "evidence_locations": [f"{sem_surface_path.name}:closing_synthesis"],
                }
            ],
            "decision": "PASS",
            "reviewed_by": EXECUTOR,
            "reviewed_at": core.iso_utc(T0),
            "status": "PASSED",
            "findings": [],
            "summary": "Pre-TeX semantic editorial review passed",
        }
        sem_rev_base["review_sha256"] = core.sha256_object(sem_rev_base)
        core.write_json(sem_rev_path, sem_rev_base)
        reader.build_reader_surface_gate(
            self.repo,
            pub / "reader-manuscript-v2.json",
            sem_rev_path,
            output_path=pub / "reader-surface-gate-v2.json",
            evaluated_by=EXECUTOR,
            recorded_at=T0,
        )

    def _write_state(self, provisional: bool = False) -> None:
        states = ["ISSUE_INITIALIZED", "DISCOVERY_COLLECTED", "CANDIDATES_NORMALIZED",
                  "EVIDENCE_REVIEWED", "SELECTION_COMPLETE", "ARCHITECTURE_ESTABLISHED",
                  "DRAFT_COMPLETE", "VALIDATED_DRAFT"]
        history = [{
            "from": None if i == 0 else states[i - 1],
            "to": name,
            "recorded_at": core.iso_utc(T0 + timedelta(minutes=i)),
            "repository_commit_sha": core.repository_commit_sha(self.repo),
        } for i, name in enumerate(states)]
        provenance = {}
        for name, from_state, _ in PRODUCERS:
            p = self.src / "orchestration" / "v2" / "checkpoints" / f"{from_state}.json"
            if provisional or not p.is_file():
                provenance[name] = {"path": str(p.relative_to(self.repo)), "sha256": "0" * 64}
            else:
                provenance[name] = {"path": str(p.relative_to(self.repo)), "sha256": core.sha256_file(p)}
        approval = self.src / "gates" / "architecture-approval.json"
        core.write_json(self.src / "production-state.json", {
            "schema_version": "2.0-rc1",
            "issue_id": ISSUE,
            "research_profile": "WEEKLY",
            "publication_profile": "WEEKLY_MAGAZINE",
            "lifecycle_state": "VALIDATED_DRAFT",
            "profile": {"path": str((self.src / "production-profile.json").relative_to(self.repo)),
                        "sha256": core.sha256_file(self.src / "production-profile.json")},
            "contract": {
                "pipeline_contract_version": "2.0-rc1",
                "pipeline_contract_sha256": "0" * 64,
                "quality_contract_version": "2.0-rc1",
                "quality_contract_sha256": "0" * 64,
                "research_profile_version": "2.0-rc1",
                "research_profile_sha256": "0" * 64,
                "publication_profile_version": "2.0-rc1",
                "publication_profile_sha256": "0" * 64,
            },
            "implementation": {"repository_commit_sha": core.repository_commit_sha(self.repo),
                               "orchestrator_version": self.cfg["orchestrator_version"]},
            "human_gates": {"architecture_review": "approved", "publication_preview": "pending"},
            "human_gate_provenance": {
                "architecture_review": {"path": str(approval.relative_to(self.repo)),
                                        "sha256": core.sha256_file(approval)},
                "publication_preview": None,
            },
            "target_gate": "ARCHITECTURE_REVIEW",
            "next_action": "stage:publication-candidate",
            "terminal_reason": None,
            "exception_gate": {"status": "inactive", "reason": None},
            "machine_checkpoints": {n: ("passed" if n in [p[0] for p in PRODUCERS] else "pending")
                                    for n in core.CHECKPOINTS},
            "checkpoint_provenance": {n: provenance.get(n) for n in core.CHECKPOINTS},
            "legacy_compatibility": {"mode": "NON_AUTHORITATIVE_READ_ONLY",
                                     "legacy_state_path": str((self.src / "legacy.json").relative_to(self.repo)),
                                     "legacy_state_present": False, "legacy_state_sha256": None},
            "history": history,
        })


class PublicationRevalidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(".").resolve()
        self.cfg = core.load_json(self.root / core.DEFAULT_CONFIG)

    def make_fixture(self, survey_dirname: str = "survey") -> tuple[tempfile.TemporaryDirectory[str], Fixture]:
        temp = tempfile.TemporaryDirectory(dir=str(self.root))
        fix = Fixture(self.root, Path(temp.name), survey_dirname)
        return temp, fix

    def regenerate(self, fix: Fixture, version: int = 2) -> None:
        for name in ("reader-manuscript-v2.json", "quality-regression-bundle-v2.json",
                     "semantic-editorial-review-v2.json", "visual-review-v2.json",
                     "reader-surface-gate-v2.json"):
            (fix.src / "publication" / "v2" / name).unlink()
        fix._publication_files(version=version)
        fix._publication_authority()

    def test_t1_legitimate_regeneration_revalidates(self) -> None:
        temp, fix = self.make_fixture()
        try:
            state_path = fix.src / "production-state.json"
            self.assertEqual(agent.validate_agent_state(self.root, self.cfg, core.load_json(state_path)), [])
            self.regenerate(fix)
            pre_errors = agent.validate_agent_state(self.root, self.cfg, core.load_json(state_path))
            self.assertTrue(any("drift" in e for e in pre_errors), pre_errors)
            record_path = agent.revalidate_publication_surface(
                self.root, self.cfg, state_path, "REVIEWED_CORE_CHANGE",
                "fixture reviewed rendering change", EXECUTOR, T0 + timedelta(hours=1), None,
            )
            self.assertTrue(record_path.is_file())
            post_errors = agent.validate_agent_state(self.root, self.cfg, core.load_json(state_path))
            self.assertEqual(post_errors, [], post_errors)
        finally:
            temp.cleanup()

    def test_t2_old_checkpoint_immutable(self) -> None:
        temp, fix = self.make_fixture()
        try:
            record = fix.src / "orchestration" / "v2" / "checkpoints" / "DRAFT_COMPLETE.json"
            before = core.sha256_file(record)
            self.regenerate(fix)
            agent.revalidate_publication_surface(
                self.root, self.cfg, fix.src / "production-state.json", "REVIEWED_CORE_CHANGE",
                "fixture change", EXECUTOR, T0 + timedelta(hours=1), None,
            )
            self.assertEqual(core.sha256_file(record), before)
        finally:
            temp.cleanup()

    def test_t3_upstream_mutation_rejected(self) -> None:
        temp, fix = self.make_fixture()
        try:
            self.regenerate(fix)
            (fix.src / "evidence" / "evidence-accepted.json").write_text('{"records": ["tampered"]}', encoding="utf-8")
            with self.assertRaisesRegex(agent.AgentControlError, "noncanonical or upstream role/path: evidence-accepted"):
                agent.revalidate_publication_surface(
                    self.root, self.cfg, fix.src / "production-state.json", "REVIEWED_CORE_CHANGE",
                    "fixture change", EXECUTOR, T0 + timedelta(hours=1), None,
                )
        finally:
            temp.cleanup()

    def test_t4_architecture_approval_mismatch_rejected(self) -> None:
        temp, fix = self.make_fixture()
        try:
            self.regenerate(fix)
            (fix.src / "architecture-v2.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(agent.AgentControlError, "drift|approval|Architecture"):
                agent.revalidate_publication_surface(
                    self.root, self.cfg, fix.src / "production-state.json", "REVIEWED_CORE_CHANGE",
                    "fixture change", EXECUTOR, T0 + timedelta(hours=1), None,
                )
        finally:
            temp.cleanup()

    def test_t5_draft_mutation_rejected(self) -> None:
        temp, fix = self.make_fixture()
        try:
            self.regenerate(fix)
            (fix.src / "draft" / "draft-note.json").write_text('{"note": "tampered"}', encoding="utf-8")
            with self.assertRaisesRegex(agent.AgentControlError, "Stage Checkpoint artifact drift: draft-note"):
                agent.revalidate_publication_surface(
                    self.root, self.cfg, fix.src / "production-state.json", "REVIEWED_CORE_CHANGE",
                    "fixture change", EXECUTOR, T0 + timedelta(hours=1), None,
                )
        finally:
            temp.cleanup()

    def test_t6_incomplete_qa_rejected(self) -> None:
        temp, fix = self.make_fixture()
        try:
            self.regenerate(fix)
            import json as _json

            bundle_path = fix.src / "publication" / "v2" / "quality-regression-bundle-v2.json"
            bundle = _json.loads(bundle_path.read_text(encoding="utf-8"))
            bundle["checks"][0]["status"] = "FAIL"
            basis = {k: bundle[k] for k in (
                "schema_version", "issue_id", "production_profile", "research_profile",
                "publication_profile", "source", "pdf", "checks", "status")}
            bundle["bundle_sha256"] = core.sha256_object(basis)
            bundle_path.write_text(_json.dumps(bundle), encoding="utf-8")
            with self.assertRaisesRegex(agent.AgentControlError, "not PASS|QA failed"):
                agent.revalidate_publication_surface(
                    self.root, self.cfg, fix.src / "production-state.json", "REVIEWED_CORE_CHANGE",
                    "fixture change", EXECUTOR, T0 + timedelta(hours=1), None,
                )
        finally:
            temp.cleanup()

    def test_t7_stale_candidate_no_longer_validates(self) -> None:
        temp, fix = self.make_fixture()
        try:
            cand_path = fix.src / "publication" / "v2" / "publication-candidate-v2.json"
            publication.build_candidate(
                self.root, ISSUE, "WEEKLY_MAGAZINE",
                fix.src / "publication" / "v2" / "reader-manuscript-v2.json",
                fix.survey / "main.tex", fix.survey / "main.pdf", 1,
                fix.src / "publication" / "v2" / "quality-regression-bundle-v2.json",
                fix.src / "publication" / "v2" / "semantic-editorial-review-v2.json",
                fix.src / "publication" / "v2" / "visual-review-v2.json",
                cand_path,
            )
            publication.validate_candidate(self.root, cand_path, issue_id=ISSUE)
            writer = PdfWriter()
            writer.add_blank_page(width=100, height=100)
            with (fix.survey / "main.pdf").open("wb") as handle:
                writer.write(handle)
            with self.assertRaises(ValueError):
                publication.validate_candidate(self.root, cand_path, issue_id=ISSUE)
        finally:
            temp.cleanup()

    def test_t8_exact_new_byte_binding(self) -> None:
        temp, fix = self.make_fixture()
        try:
            prior = {r["name"]: r["sha256"] for r in core.load_json(
                fix.src / "orchestration" / "v2" / "checkpoints" / "DRAFT_COMPLETE.json")["artifacts"]}
            self.regenerate(fix)
            record_path = agent.revalidate_publication_surface(
                self.root, self.cfg, fix.src / "production-state.json", "REVIEWED_CORE_CHANGE",
                "fixture change", EXECUTOR, T0 + timedelta(hours=1), None,
            )
            record = core.load_json(record_path)
            self.assertTrue(len(record["superseded_artifacts"]) >= 5)
            for row in record["superseded_artifacts"]:
                live = core.sha256_file(self.root / row["path"])
                self.assertEqual(row["new_sha256"], live)
                self.assertEqual(row["prior_sha256"], prior[row["name"]])
                self.assertNotEqual(row["new_sha256"], row["prior_sha256"])
        finally:
            temp.cleanup()

    def test_t9_after_preview_decision_forbidden(self) -> None:
        temp, fix = self.make_fixture()
        try:
            import json as _json

            self.regenerate(fix)
            state_path = fix.src / "production-state.json"
            state = _json.loads(state_path.read_text(encoding="utf-8"))
            state["human_gates"]["publication_preview"] = "approved"
            state_path.write_text(_json.dumps(state), encoding="utf-8")
            with self.assertRaisesRegex(agent.AgentControlError, "pending Publication Preview"):
                agent.revalidate_publication_surface(
                    self.root, self.cfg, state_path, "REVIEWED_CORE_CHANGE",
                    "fixture change", EXECUTOR, T0 + timedelta(hours=1), None,
                )
        finally:
            temp.cleanup()

    def test_t10_after_freeze_forbidden(self) -> None:
        temp, fix = self.make_fixture()
        try:
            import json as _json

            self.regenerate(fix)
            state_path = fix.src / "production-state.json"
            state = _json.loads(state_path.read_text(encoding="utf-8"))
            state["machine_checkpoints"]["freeze"] = "passed"
            state_path.write_text(_json.dumps(state), encoding="utf-8")
            with self.assertRaisesRegex(agent.AgentControlError, "resolved freeze"):
                agent.revalidate_publication_surface(
                    self.root, self.cfg, state_path, "REVIEWED_CORE_CHANGE",
                    "fixture change", EXECUTOR, T0 + timedelta(hours=1), None,
                )
        finally:
            temp.cleanup()

    def test_t11_weekly_viability_and_t13_chain(self) -> None:
        temp, fix = self.make_fixture()
        try:
            self.assertEqual(fix.profile["research_profile"], "WEEKLY")
            state_path = fix.src / "production-state.json"
            self.regenerate(fix)
            pre = agent.validate_agent_state(self.root, self.cfg, core.load_json(state_path))
            self.assertEqual(len([e for e in pre if "drift" in e]), 7, pre)
            agent.revalidate_publication_surface(
                self.root, self.cfg, state_path, "REVIEWED_CORE_CHANGE",
                "W34-defect-shape reproduction", EXECUTOR, T0 + timedelta(hours=1), None,
            )
            self.assertEqual(agent.validate_agent_state(self.root, self.cfg, core.load_json(state_path)), [])
            cand_path = fix.src / "publication" / "v2" / "publication-candidate-v2.json"
            publication.build_candidate(
                self.root, ISSUE, "WEEKLY_MAGAZINE",
                fix.src / "publication" / "v2" / "reader-manuscript-v2.json",
                fix.survey / "main.tex", fix.survey / "main.pdf", 1,
                fix.src / "publication" / "v2" / "quality-regression-bundle-v2.json",
                fix.src / "publication" / "v2" / "semantic-editorial-review-v2.json",
                fix.src / "publication" / "v2" / "visual-review-v2.json",
                cand_path,
            )
            report_path = fix.src / "execution" / "stage-report.json"
            stage_validation.validate_stage(
                self.root, self.cfg, state_path,
                {"publication-candidate": cand_path},
                report_path, T0 + timedelta(hours=2),
            )
            report = core.load_json(report_path)
            self.assertEqual((report["from_state"], report["to_state"], report["status"]),
                             ("VALIDATED_DRAFT", "RELEASE_CANDIDATE", "PASS"))
            reviews_path = fix.src / "execution" / "reviews.json"
            core.write_json(reviews_path, {"reviews": [{
                "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
                "executor": "fixture", "evidence": "fixture stage contract",
                "result_path": str(report_path.relative_to(self.root)),
            }]})
            checkpoint = agent.build_stage_checkpoint(
                self.root, self.cfg, state_path,
                {"publication-candidate": cand_path},
                reviews_path, "fixture advance to RELEASE_CANDIDATE",
                T0 + timedelta(hours=3), None,
            )
            updated = agent.advance_with_checkpoint(self.root, self.cfg, state_path, checkpoint)
            self.assertEqual(updated["lifecycle_state"], "RELEASE_CANDIDATE")
            self.assertEqual(updated["human_gates"]["publication_preview"], "pending")
            self.assertEqual(agent.validate_agent_state(self.root, self.cfg, updated), [])
        finally:
            temp.cleanup()

    def test_t12_special_layout_genericity(self) -> None:
        temp, fix = self.make_fixture(survey_dirname="survey-special")
        try:
            self.regenerate(fix)
            record_path = agent.revalidate_publication_surface(
                self.root, self.cfg, fix.src / "production-state.json", "REVIEWED_CORE_CHANGE",
                "special-layout genericity", EXECUTOR, T0 + timedelta(hours=1), None,
            )
            record = core.load_json(record_path)
            self.assertTrue(any("survey-special" in r["path"] for r in record["superseded_artifacts"]))
            self.assertEqual(agent.validate_agent_state(self.root, self.cfg, core.load_json(fix.src / "production-state.json")), [])
        finally:
            temp.cleanup()

    def _pointer(self, fix: Fixture) -> dict | None:
        import json as _json

        return _json.loads((fix.src / "production-state.json").read_text(encoding="utf-8")).get(
            "publication_revalidation_provenance"
        )

    def _write_state_pointer(self, fix: Fixture, pointer: dict | None) -> None:
        import json as _json

        state_path = fix.src / "production-state.json"
        state = _json.loads(state_path.read_text(encoding="utf-8"))
        if pointer is None:
            state.pop("publication_revalidation_provenance", None)
        else:
            state["publication_revalidation_provenance"] = pointer
        state_path.write_text(_json.dumps(state), encoding="utf-8")

    def _operate(self, fix: Fixture, reason: str = "fixture reviewed core change"):
        return agent.revalidate_publication_surface(
            self.root, self.cfg, fix.src / "production-state.json", "REVIEWED_CORE_CHANGE",
            reason, EXECUTOR, T0 + timedelta(hours=1), None,
        )

    def test_n1_unreferenced_forged_record_inert(self) -> None:
        import json as _json
        import shutil as _shutil

        temp, fix = self.make_fixture()
        try:
            self.regenerate(fix)
            record_path = self._operate(fix)
            saved = _json.loads(record_path.read_text(encoding="utf-8"))
            self._write_state_pointer(fix, None)
            forged = fix.src / "publication" / "v2" / "publication-surface-revalidation-r9.json"
            _shutil.copyfile(record_path, forged)
            record, errors = agent.resolve_active_publication_revalidation(
                self.root, self.cfg, core.load_json(fix.src / "production-state.json"))
            self.assertIsNone(record)
            self.assertEqual(errors, [])
            drift = agent.validate_agent_state(self.root, self.cfg, core.load_json(fix.src / "production-state.json"))
            self.assertTrue(any("drift" in e for e in drift), drift)
            self.assertEqual(saved["issue_id"], ISSUE)
        finally:
            temp.cleanup()

    def test_n2_state_authority_sha_mismatch(self) -> None:
        temp, fix = self.make_fixture()
        try:
            self.regenerate(fix)
            self._operate(fix)
            pointer = self._pointer(fix)
            assert pointer is not None
            pointer = dict(pointer)
            pointer["sha256"] = "0" * 64
            self._write_state_pointer(fix, pointer)
            _, errors = agent.resolve_active_publication_revalidation(
                self.root, self.cfg, core.load_json(fix.src / "production-state.json"))
            self.assertTrue(any("SHA mismatch" in e for e in errors), errors)
        finally:
            temp.cleanup()

    def test_n3_referenced_record_tamper(self) -> None:
        temp, fix = self.make_fixture()
        try:
            self.regenerate(fix)
            record_path = self._operate(fix)
            text = record_path.read_text(encoding="utf-8")
            record_path.write_text(text + " ", encoding="utf-8")
            _, errors = agent.resolve_active_publication_revalidation(
                self.root, self.cfg, core.load_json(fix.src / "production-state.json"))
            self.assertTrue(errors, "tampered record must fail closed")
        finally:
            temp.cleanup()

    def _approve_preview(self, fix: Fixture):
        cand_path = fix.src / "publication" / "v2" / "publication-candidate-v2.json"
        publication.build_candidate(
            self.root, ISSUE, "WEEKLY_MAGAZINE",
            fix.src / "publication" / "v2" / "reader-manuscript-v2.json",
            fix.survey / "main.tex", fix.survey / "main.pdf", 1,
            fix.src / "publication" / "v2" / "quality-regression-bundle-v2.json",
            fix.src / "publication" / "v2" / "semantic-editorial-review-v2.json",
            fix.src / "publication" / "v2" / "visual-review-v2.json",
            cand_path,
        )
        report_path = fix.src / "execution" / "stage-report.json"
        stage_validation.validate_stage(
            self.root, self.cfg, fix.src / "production-state.json",
            {"publication-candidate": cand_path}, report_path, T0 + timedelta(hours=2),
        )
        reviews_path = fix.src / "execution" / "reviews.json"
        core.write_json(reviews_path, {"reviews": [{
            "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
            "executor": "fixture", "evidence": "n4 advance",
            "result_path": str(report_path.relative_to(self.root)),
        }]})
        agent.advance_with_checkpoint(
            self.root, self.cfg, fix.src / "production-state.json",
            agent.build_stage_checkpoint(
                self.root, self.cfg, fix.src / "production-state.json",
                {"publication-candidate": cand_path}, reviews_path,
                "n4 advance", T0 + timedelta(hours=3), None),
        )
        agent.approve_publication_preview(
            self.root, self.cfg, fix.src / "production-state.json",
            "fixture-human", T0 + timedelta(hours=4), "fixture-preview-r1",
        )

    def _swap_live_pdf(self, fix: Fixture) -> tuple[str, int]:
        from pypdf import PdfWriter as _Writer

        writer = _Writer()
        writer.add_blank_page(width=100, height=100)
        writer.add_blank_page(width=100, height=100)
        with (fix.survey / "main.pdf").open("wb") as handle:
            writer.write(handle)
        return core.sha256_file(fix.survey / "main.pdf"), (fix.survey / "main.pdf").stat().st_size

    def test_n4_post_preview_forged_activation_fails(self) -> None:
        import json as _json

        temp, fix = self.make_fixture()
        try:
            self.regenerate(fix)
            record_path = self._operate(fix)
            self._approve_preview(fix)
            state = core.load_json(fix.src / "production-state.json")
            self.assertEqual(state["human_gates"]["publication_preview"], "approved")
            record, errors = agent.resolve_active_publication_revalidation(self.root, self.cfg, state)
            self.assertIsNotNone(record)
            self.assertEqual(errors, [])
            p2_sha, p2_bytes = self._swap_live_pdf(fix)
            forged = _json.loads(record_path.read_text(encoding="utf-8"))
            forged["validation"]["pdf"] = {"path": forged["validation"]["pdf"]["path"],
                                           "sha256": p2_sha, "byte_count": p2_bytes, "page_count": 2}
            for row in forged["superseded_artifacts"]:
                if row["name"] == "publication-pdf":
                    row["new_sha256"] = p2_sha
                    row["byte_count"] = p2_bytes
            forged_path = fix.src / "publication" / "v2" / "publication-surface-revalidation-r2.json"
            forged_path.write_text(_json.dumps(forged), encoding="utf-8")
            self._write_state_pointer(
                fix, {"path": str(forged_path.relative_to(self.root)),
                      "sha256": core.sha256_file(forged_path)})
            _, errors = agent.resolve_active_publication_revalidation(
                self.root, self.cfg, core.load_json(fix.src / "production-state.json"))
            self.assertTrue(any("diverges from Human-approved" in e for e in errors), errors)
        finally:
            temp.cleanup()

    def test_n5_post_freeze_forged_activation_fails(self) -> None:
        import json as _json

        temp, fix = self.make_fixture()
        try:
            self.regenerate(fix)
            record_path = self._operate(fix)
            state_path = fix.src / "production-state.json"
            state = _json.loads(state_path.read_text(encoding="utf-8"))
            state["machine_checkpoints"]["freeze"] = "passed"
            state_path.write_text(_json.dumps(state), encoding="utf-8")
            freeze_path = fix.src / "publication" / "v2" / "freeze-record-v2.json"
            live_pdf_sha = core.sha256_file(fix.survey / "main.pdf")
            freeze_path.write_text(_json.dumps({
                "schema_version": "2.0-rc1", "issue_id": ISSUE, "status": "FROZEN",
                "publication_candidate_path": "x", "publication_candidate_sha256": "0" * 64,
                "publication_preview_approval_path": "x", "publication_preview_approval_sha256": "0" * 64,
                "visual_review_path": "x", "visual_review_sha256": "0" * 64,
                "source_path": "x", "source_sha256": "0" * 64,
                "pdf_path": str((fix.survey / "main.pdf").relative_to(self.root)),
                "pdf_sha256": live_pdf_sha, "page_count": 1, "frozen_at": core.iso_utc(T0),
            }), encoding="utf-8")
            p2_sha, p2_bytes = self._swap_live_pdf(fix)
            forged = _json.loads(record_path.read_text(encoding="utf-8"))
            forged["validation"]["pdf"] = {"path": forged["validation"]["pdf"]["path"],
                                           "sha256": p2_sha, "byte_count": p2_bytes, "page_count": 2}
            for row in forged["superseded_artifacts"]:
                if row["name"] == "publication-pdf":
                    row["new_sha256"] = p2_sha
                    row["byte_count"] = p2_bytes
            forged_path = fix.src / "publication" / "v2" / "publication-surface-revalidation-r2.json"
            forged_path.write_text(_json.dumps(forged), encoding="utf-8")
            self._write_state_pointer(
                fix, {"path": str(forged_path.relative_to(self.root)),
                      "sha256": core.sha256_file(forged_path)})
            _, errors = agent.resolve_active_publication_revalidation(
                self.root, self.cfg, core.load_json(state_path))
            self.assertTrue(any("Freeze record bytes" in e for e in errors), errors)
        finally:
            temp.cleanup()

    def test_n6_immutable_multi_round_chain(self) -> None:
        import json as _json

        temp, fix = self.make_fixture()
        try:
            self.regenerate(fix, version=2)
            r1_path = self._operate(fix, "round one")
            r1_sha = core.sha256_file(r1_path)
            self.regenerate(fix, version=3)
            r2_path = self._operate(fix, "round two")
            self.assertTrue(r1_path.is_file())
            self.assertEqual(core.sha256_file(r1_path), r1_sha)
            r2 = _json.loads(r2_path.read_text(encoding="utf-8"))
            self.assertEqual(r2["supersedes"], {"path": str(r1_path.relative_to(self.root)), "sha256": r1_sha})
            pointer = self._pointer(fix)
            assert pointer is not None
            self.assertEqual(pointer["path"], str(r2_path.relative_to(self.root)))
            self.assertEqual(pointer["sha256"], core.sha256_file(r2_path))
            record, errors = agent.resolve_active_publication_revalidation(
                self.root, self.cfg, core.load_json(fix.src / "production-state.json"))
            self.assertIsNotNone(record)
            self.assertEqual(errors, [])
            self.assertEqual(agent.validate_agent_state(self.root, self.cfg, core.load_json(fix.src / "production-state.json")), [])
        finally:
            temp.cleanup()

    def test_n7_historical_chain_tamper_fails(self) -> None:
        temp, fix = self.make_fixture()
        try:
            self.regenerate(fix, version=2)
            r1_path = self._operate(fix, "round one")
            self.regenerate(fix, version=3)
            self._operate(fix, "round two")
            text = r1_path.read_text(encoding="utf-8")
            r1_path.write_text(text.replace("round one", "round ONE"), encoding="utf-8")
            _, errors = agent.resolve_active_publication_revalidation(
                self.root, self.cfg, core.load_json(fix.src / "production-state.json"))
            self.assertTrue(errors, "tampered chain history must fail closed")
        finally:
            temp.cleanup()

    def test_n8_unrelated_historical_record_inert(self) -> None:
        import json as _json
        import shutil as _shutil

        temp, fix = self.make_fixture()
        try:
            self.regenerate(fix)
            record_path = self._operate(fix)
            stray = fix.src / "publication" / "v2" / "publication-surface-revalidation-r9.json"
            _shutil.copyfile(record_path, stray)
            record, errors = agent.resolve_active_publication_revalidation(
                self.root, self.cfg, core.load_json(fix.src / "production-state.json"))
            self.assertIsNotNone(record)
            self.assertEqual(errors, [])
            active_path = self._pointer(fix)
            assert active_path is not None
            self.assertEqual(active_path["path"], str(record_path.relative_to(self.root)))
            self.assertNotEqual(active_path["path"], str(stray.relative_to(self.root)))
            self.assertEqual(_json.loads(record_path.read_text(encoding="utf-8"))["issue_id"], ISSUE)
        finally:
            temp.cleanup()

    def test_n9_gate_separation(self) -> None:
        import json as _json

        temp, fix = self.make_fixture()
        try:
            before_gates = _json.loads((fix.src / "production-state.json").read_text(encoding="utf-8"))["human_gates"]
            before_prov = _json.loads((fix.src / "production-state.json").read_text(encoding="utf-8"))["human_gate_provenance"]
            self.regenerate(fix)
            self._operate(fix)
            after = _json.loads((fix.src / "production-state.json").read_text(encoding="utf-8"))
            self.assertEqual(after["human_gates"], before_gates)
            self.assertEqual(after["human_gate_provenance"]["architecture_review"], before_prov["architecture_review"])
            self.assertIsNone(after["human_gate_provenance"]["publication_preview"])
            self.assertEqual(after["human_gates"]["publication_preview"], "pending")
            self.assertFalse((fix.src / "gates" / "publication-preview-approval.json").exists())
            self.assertEqual(after["lifecycle_state"], "VALIDATED_DRAFT")
        finally:
            temp.cleanup()

    def test_n10_full_weekly_chain_no_human_decision(self) -> None:
        import json as _json

        temp, fix = self.make_fixture()
        try:
            self.regenerate(fix)
            self._operate(fix)
            cand_path = fix.src / "publication" / "v2" / "publication-candidate-v2.json"
            publication.build_candidate(
                self.root, ISSUE, "WEEKLY_MAGAZINE",
                fix.src / "publication" / "v2" / "reader-manuscript-v2.json",
                fix.survey / "main.tex", fix.survey / "main.pdf", 1,
                fix.src / "publication" / "v2" / "quality-regression-bundle-v2.json",
                fix.src / "publication" / "v2" / "semantic-editorial-review-v2.json",
                fix.src / "publication" / "v2" / "visual-review-v2.json",
                cand_path,
            )
            report_path = fix.src / "execution" / "stage-report.json"
            stage_validation.validate_stage(
                self.root, self.cfg, fix.src / "production-state.json",
                {"publication-candidate": cand_path}, report_path, T0 + timedelta(hours=2),
            )
            reviews_path = fix.src / "execution" / "reviews.json"
            core.write_json(reviews_path, {"reviews": [{
                "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
                "executor": "fixture", "evidence": "n10 chain",
                "result_path": str(report_path.relative_to(self.root)),
            }]})
            updated = agent.advance_with_checkpoint(
                self.root, self.cfg, fix.src / "production-state.json",
                agent.build_stage_checkpoint(
                    self.root, self.cfg, fix.src / "production-state.json",
                    {"publication-candidate": cand_path}, reviews_path,
                    "n10 advance", T0 + timedelta(hours=3), None),
            )
            self.assertEqual(updated["lifecycle_state"], "RELEASE_CANDIDATE")
            self.assertEqual(updated["human_gates"]["publication_preview"], "pending")
            self.assertIsNone(updated["human_gate_provenance"]["publication_preview"])
            self.assertFalse((fix.src / "gates" / "publication-preview-approval.json").exists())
            self.assertEqual(agent.validate_agent_state(self.root, self.cfg, updated), [])
            self.assertEqual(_json.loads((fix.src / "gates" / "architecture-approval.json").read_text(encoding="utf-8"))["decision"], "APPROVED")
        finally:
            temp.cleanup()

    def test_r1_record_collision_no_clobber(self) -> None:
        """R1 narrow correction: exclusive record creation refuses a collision.

        The allocator is pinned to an empty listing while a foreign file
        occupies the r1 slot, so the in-try collision guard (not max+1
        allocation) must refuse without touching foreign bytes or State.
        """
        temp, fix = self.make_fixture()
        try:
            state_path = fix.src / "production-state.json"
            self.regenerate(fix)
            state_before = state_path.read_bytes()
            record_path = agent._revalidation_record_path(
                self.root, self.cfg, core.load_json(state_path), 1
            )
            record_path.write_bytes(b'{"foreign": true}')
            with mock.patch.object(agent, "_revalidation_existing_sequences", return_value=[]):
                with self.assertRaisesRegex(agent.AgentControlError, "sequence collision"):
                    agent.revalidate_publication_surface(
                        self.root, self.cfg, state_path, "REVIEWED_CORE_CHANGE",
                        "fixture change", EXECUTOR, T0 + timedelta(hours=1), None,
                    )
            self.assertEqual(record_path.read_bytes(), b'{"foreign": true}')
            self.assertEqual(state_path.read_bytes(), state_before)
        finally:
            temp.cleanup()

    def test_r1_record_tamper_rollback_refuses_removal(self) -> None:
        """R1 narrow correction: rollback never deletes unknown record bytes.

        The post-write strict check is forced to fail after the record file
        is tampered; rollback must restore State yet refuse record removal
        with a precise error, preserving the tampered evidence.
        """
        temp, fix = self.make_fixture()
        try:
            state_path = fix.src / "production-state.json"
            self.regenerate(fix)
            state_before = state_path.read_bytes()
            expected_record = agent._revalidation_record_path(
                self.root, self.cfg, core.load_json(state_path), 1
            )
            real_validate = agent.validate_agent_state

            def tampering_validate(repo_root, cfg, state):
                errors = real_validate(repo_root, cfg, state)
                self.assertEqual(errors, [])
                with expected_record.open("ab") as handle:
                    handle.write(b" ")
                return ["injected post-write failure"]

            with mock.patch.object(agent, "validate_agent_state", side_effect=tampering_validate):
                with self.assertRaisesRegex(agent.AgentControlError, "refused changed record bytes"):
                    agent.revalidate_publication_surface(
                        self.root, self.cfg, state_path, "REVIEWED_CORE_CHANGE",
                        "fixture change", EXECUTOR, T0 + timedelta(hours=1), None,
                    )
            tampered = expected_record.read_bytes()
            self.assertTrue(tampered.endswith(b" "), "tampered record evidence must be preserved, not deleted")
            self.assertEqual(state_path.read_bytes(), state_before)
        finally:
            temp.cleanup()

    def test_no_edition_conditionals_in_new_paths(self) -> None:
        source = (self.root / "scripts" / "survey_agent_control_v2.py").read_text(encoding="utf-8")
        start = source.index("def resolve_active_publication_revalidation")
        end = source.index("def _path(")
        block = source[start:end]
        for token in ("2026-W34", "WEEKLY", "LONGFORM", "Special", "special", "retrospective", "thematic", "weekly/"):
            self.assertNotIn(token, block, token)


if __name__ == "__main__":
    unittest.main()
