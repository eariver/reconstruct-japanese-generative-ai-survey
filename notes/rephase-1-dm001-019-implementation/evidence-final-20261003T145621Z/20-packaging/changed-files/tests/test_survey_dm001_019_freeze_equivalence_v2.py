"""DM-001/019 joint Freeze boundary: builder equivalence and writer preflight.

Both builders must freeze the exact Human-approved Candidate through the
Candidate-bound pre-preview VISUAL record, derive public identity from the
validated Profile slug, and refuse predictable authority/identity/output
conflicts before either target write. All research, editorial, visual and
Human decisions here are synthetic fixture records; the tests exercise real
production validators, stage/checkpoint/State transitions and the saved
release-workflow predicate. They are not publication or approval evidence.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from scripts import survey_agent_control_v2 as agent
from scripts import survey_production_v2 as core
from scripts import survey_profiled_freeze_v2 as profiled
from scripts import survey_publication_v2 as publication
from scripts import survey_quality_v2 as quality
from scripts import survey_reader_publication_v2 as reader
from scripts import survey_stage_validation_v2 as stage_validation

ROOT = Path(".").resolve()
T0 = datetime(2026, 9, 12, 12, 0, 0, tzinfo=timezone.utc)
EXECUTOR = "dm001019-freeze-test"
WEEKLY_ISSUE = "2026-W35"

_REV_SPEC = importlib.util.spec_from_file_location(
    "dm001019_revalidation_fixture",
    ROOT / "tests/test_survey_publication_revalidation_v2.py",
)
assert _REV_SPEC is not None and _REV_SPEC.loader is not None
_REV = importlib.util.module_from_spec(_REV_SPEC)
_REV_SPEC.loader.exec_module(_REV)
WeeklyFixture = _REV.Fixture


class WeeklyCanonicalFixture(_REV.Fixture):
    """Weekly edition in canonical layout (State at sources/<issue>/...).

    Reuses every WeeklyFixture builder verbatim (all are src/survey-generic);
    only the directory roots follow the production layout so the saved
    release-workflow predicate resolves the canonical State path and the
    public slug equals the issue id.
    """

    def __init__(self, root: Path) -> None:
        self.repo = root
        self.cfg = core.load_json(root / core.DEFAULT_CONFIG)
        self.base = root / "sources" / WEEKLY_ISSUE
        self.src = self.base
        self.survey = root / "surveys" / "weekly" / WEEKLY_ISSUE
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

    def cleanup(self) -> None:
        shutil.rmtree(self.src, ignore_errors=True)
        shutil.rmtree(self.survey, ignore_errors=True)

_PUB_SPEC = importlib.util.spec_from_file_location(
    "dm001019_publication_tests",
    ROOT / "tests/test_survey_publication_v2.py",
)
assert _PUB_SPEC is not None and _PUB_SPEC.loader is not None
_PUBMOD = importlib.util.module_from_spec(_PUB_SPEC)
_PUB_SPEC.loader.exec_module(_PUBMOD)


def _cfg() -> dict:
    return core.load_json(ROOT / core.DEFAULT_CONFIG)


# ---------------------------------------------------------------------------
# Special LONGFORM_SPECIAL State scaffold (canonical layout, real validators)
# ---------------------------------------------------------------------------

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

STATES = ["ISSUE_INITIALIZED", "DISCOVERY_COLLECTED", "CANDIDATES_NORMALIZED",
          "EVIDENCE_REVIEWED", "SELECTION_COMPLETE", "ARCHITECTURE_ESTABLISHED",
          "DRAFT_COMPLETE", "VALIDATED_DRAFT"]


def _fixture_pdf(page_count: int = 12) -> bytes:
    from io import BytesIO

    from pypdf import PdfWriter

    stream = BytesIO()
    writer = PdfWriter()
    for _ in range(page_count):
        writer.add_blank_page(width=612, height=792)
    writer.write(stream)
    return stream.getvalue()


def _longform_source() -> str:
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


class SpecialFixture:
    """VALIDATED_DRAFT Special edition in canonical layout (repo-owned roots)."""

    def __init__(self, root: Path, issue: str, survey_rel: str,
                 research_profile: str = "THEMATIC",
                 publication_profile: str = "LONGFORM_SPECIAL",
                 visual_filename: str = "visual-review-v2.json") -> None:
        self.visual_filename = visual_filename
        self.repo = root
        self.cfg = core.load_json(root / core.DEFAULT_CONFIG)
        self.issue = issue
        self.research_profile = research_profile
        self.publication_profile = publication_profile
        self.src = root / "sources" / issue
        self.survey = root / survey_rel
        self.src.mkdir(parents=True)
        self.survey.mkdir(parents=True)
        (self.src / "publication" / "v2").mkdir(parents=True)
        (self.src / "draft").mkdir(parents=True)
        (self.src / "evidence").mkdir(parents=True)
        (self.src / "gates").mkdir(parents=True)
        (self.src / "orchestration" / "v2" / "checkpoints").mkdir(parents=True)
        (self.src / "execution").mkdir(parents=True)
        self.profile_path = self.src / "production-profile.json"
        core.write_json(self.profile_path, self._profile())
        self._authority_files()
        self._publication_files()
        self._approval_files()
        self._publication_authority()
        self._write_state(provisional=True)
        self._checkpoint_records()
        self._write_state(provisional=False)

    def cleanup(self) -> None:
        shutil.rmtree(self.src, ignore_errors=True)
        shutil.rmtree(self.survey, ignore_errors=True)

    def _profile(self) -> dict:
        return {
            "schema_version": self.cfg["schema_version"],
            "issue_id": self.issue,
            "research_profile": self.research_profile,
            "publication_profile": self.publication_profile,
            "research_scope": {
                "question": "Fixture Special publication question",
                "inclusion": [],
                "exclusion": [],
                "scope_dimensions": ["fixture"],
                "initial_obligations": [
                    {"obligation_id": "fixture:coverage", "dimension": "fixture",
                     "description": "Fixture coverage"}
                ],
                "temporal_policy": {"mode": "OPEN_HISTORY_AS_OF", "as_of": "2026-08-23T07:00:00Z"},
            },
            "paths": {
                "source_root": str(self.src.relative_to(self.repo)),
                "survey_root": str(self.survey.relative_to(self.repo)),
                "work_branch": f"test/{self.issue}",
            },
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
        }

    def _authority_files(self) -> None:
        arch = self.src / "architecture-v2.json"
        core.write_json(arch, {
            "schema_version": "2.0-rc1",
            "issue_id": self.issue,
            "research_profile": self.research_profile,
            "publication_profile": self.publication_profile,
            "status": "APPROVED",
            "basis": {
                "production_profile_sha256": "0" * 64,
                "profile_completeness_sha256": "0" * 64,
                "materiality_ledger_sha256": "0" * 64,
                "candidate_matrix_sha256": "0" * 64,
                "candidate_selection_sha256": "0" * 64,
            },
            "editorial_thesis": "Fixture thesis",
            "architecture_goals": ["Explain the selected material to readers"],
            "page_plan": {"target_pages": 12, "max_pages": 24, "notes": "planning envelope"},
            "packages": [{
                "package_id": "PKG-1",
                "title": "Fixture package",
                "purpose": "Fixture purpose",
                "primary_candidate_ids": ["C-1"],
                "supporting_candidate_ids": [],
                "must_cover_requirements": ["Explain concrete transition", "Explain remaining boundary"],
                "boundaries": ["Keep claims source-bounded"],
                "drafting_order": 1,
                "profile_extensions": {},
                "publication_extensions": {},
            }],
            "selected_exceptions": [],
            "profile_extensions": {},
            "publication_extensions": {},
            "human_review": {"reviewed_by": None, "reviewed_at": None, "review_reference": None},
        })
        (self.src / "architecture-review-summary-v2.json").write_text("{}", encoding="utf-8")
        (self.src / "architecture-review-attention-v2.json").write_text("{}", encoding="utf-8")

    def _approval_files(self) -> None:
        arch = self.src / "architecture-v2.json"
        summ = self.src / "architecture-review-summary-v2.json"
        attn = self.src / "architecture-review-attention-v2.json"
        core.write_json(self.src / "gates" / "architecture-approval.json", {
            "schema_version": "2.0-rc1",
            "approval_id": "fixture-approval-r1",
            "issue_id": self.issue,
            "gate": "ARCHITECTURE_REVIEW",
            "decision": "APPROVED",
            "architecture_sha256": core.sha256_file(arch),
            "architecture_review_summary_sha256": core.sha256_file(summ),
            "architecture_review_attention_sha256": core.sha256_file(attn),
            "reviewed_by": "fixture-human",
            "reviewed_at": "2026-09-12T11:00:00Z",
            "review_reference": "fixture",
        })

    def _publication_files(self) -> None:
        (self.survey / "main.tex").write_text(_longform_source(), encoding="utf-8")
        (self.survey / "references.bib").write_text(
            "@misc{fixtureA,title={Fixture A}}\n@misc{fixtureB,title={Fixture B}}\n",
            encoding="utf-8",
        )
        (self.survey / "main.pdf").write_bytes(_fixture_pdf(12))

    def _deterministic_checks(self, directory: Path) -> list[dict]:
        expected = quality.expected_checks_by_kind(
            self.cfg, self.research_profile, self.publication_profile, {"DETERMINISTIC"})
        rows: list[dict] = []
        for check_id in sorted(expected):
            result_path = directory / "quality-results" / f"{check_id}.json"
            quality.core.write_json(result_path, {"check_id": check_id, "status": "PASS"})
            rows.append({
                "check_id": check_id, "kind": "DETERMINISTIC", "status": "PASS",
                "executor": EXECUTOR, "evidence": f"fixture:{check_id}",
                "recorded_at": "2026-08-23T07:00:00Z",
                "result": {"path": str(result_path.relative_to(self.repo)),
                            "sha256": quality.core.sha256_file(result_path)},
            })
        return rows

    def _review_checks(self, kind: str) -> list[dict]:
        profile = quality.core.load_json(self.profile_path)
        ids = reader._expected_review_checks(self.repo, profile, kind)
        rows: list[dict] = []
        exact_blocks = {"Subsection 1.1 — Concrete transition", "Subsection 1.2 — Remaining boundary"}
        for check_id in sorted(ids):
            evidence_locations = ["main.tex:fixture"]
            if kind == "SEMANTIC_EDITORIAL" and check_id in {
                    "ARCHITECTURE_CONTENT_FIDELITY", "LONGFORM_TECHNICAL_DEPTH"}:
                evidence_locations.extend(sorted({"package:PKG-1"} | exact_blocks))
            if kind == "SEMANTIC_EDITORIAL" and check_id == "FINAL_SYNTHESIS_QUALITY":
                evidence_locations.extend(
                    ["package:PKG-1", "reader-role:final-synthesis", "Section 1 — Final synthesis"])
            if kind == "VISUAL" and check_id == "LONGFORM_MIXED_LAYOUT":
                evidence_locations.extend([
                    "reader-layout:balanced-two-column-narrative",
                    "reader-layout:wide-surfaces-full-width",
                    "reader-layout:references-one-column",
                ])
            rows.append({"check_id": check_id, "status": "PASS",
                         "detail": f"Explicit ChatGPT review passed {check_id}",
                         "evidence_locations": evidence_locations})
        return rows

    def _publication_authority(self) -> None:
        pub = self.src / "publication" / "v2"
        support = [{"role": "BIBLIOGRAPHY",
                    "path": str((self.survey / "references.bib").relative_to(self.repo))}]
        coverage = [
            {"package_id": "PKG-1", "requirement": "Explain concrete transition",
             "status": "FULFILLED", "reader_locations": ["Subsection 1.1 — Concrete transition"],
             "detail": "Reader prose explains the transition in a distinct substantive block"},
            {"package_id": "PKG-1", "requirement": "Explain remaining boundary",
             "status": "FULFILLED", "reader_locations": ["Subsection 1.2 — Remaining boundary"],
             "detail": "Reader prose explains the remaining boundary in a distinct substantive block"},
        ]
        requirements = [{"requirement_id": "FINAL_SYNTHESIS", "status": "FULFILLED",
                         "reader_locations": ["Section 1 — Final synthesis"],
                         "detail": "Final synthesis remains reader-visible and substantive"}]
        reader.build_manuscript_manifest(
            self.repo, self.issue, self.profile_path,
            self.src / "architecture-v2.json", self.src / "gates" / "architecture-approval.json",
            self.survey / "main.tex", support, coverage, requirements,
            EXECUTOR, T0, pub / "reader-manuscript-v2.json",
        )
        checks = self._deterministic_checks(pub)
        quality.build_bundle(
            self.repo, self.issue, self.survey / "main.tex", self.survey / "main.pdf",
            checks, pub / "quality-regression-bundle-v2.json",
            production_profile_path=self.profile_path,
        )
        reader.build_review_record(
            self.repo, pub / "reader-manuscript-v2.json", self.survey / "main.pdf", 12,
            "SEMANTIC_EDITORIAL", self._review_checks("SEMANTIC_EDITORIAL"),
            "ChatGPT", T0, pub / "semantic-editorial-review-v2.json",
        )
        reader.build_review_record(
            self.repo, pub / "reader-manuscript-v2.json", self.survey / "main.pdf", 12,
            "VISUAL", self._review_checks("VISUAL"),
            "ChatGPT", T0, pub / self.visual_filename,
        )
        sem_surface_path = self.survey / "main.tex"
        sem_rev_path = pub / "reader-surface-semantic-review-v2.json"
        sem_rev_base = {
            "schema_version": "2.0-rc1",
            "issue_id": self.issue,
            "publication_profile": self.publication_profile,
            "review_kind": "SEMANTIC_EDITORIAL",
            "reviewed_surface": {
                "path": str(sem_surface_path.relative_to(self.repo)).replace("\\", "/"),
                "sha256": core.sha256_file(sem_surface_path),
            },
            "checks": [{
                "check_id": "READER_PIPELINE_INDEPENDENCE",
                "status": "PASS",
                "detail": "Prose is independently understandable without internal pipeline knowledge.",
                "evidence_locations": [f"{sem_surface_path.name}:closing_synthesis"],
            }],
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
            self.repo, pub / "reader-manuscript-v2.json", sem_rev_path,
            output_path=pub / "reader-surface-gate-v2.json",
            evaluated_by=EXECUTOR, recorded_at=T0,
        )

    def _contract_report(self, record_path: Path, from_state: str, to_state: str, artifacts: list) -> Path:
        report_path = record_path.parent / (record_path.stem + "-core-contract.json")
        state_path = self.src / "production-state.json"
        core.write_json(report_path, {
            "schema_version": "2.0-rc1",
            "check_id": "CORE_STAGE_CONTRACT",
            "status": "PASS",
            "issue_id": self.issue,
            "from_state": from_state,
            "to_state": to_state,
            "production_state": {
                "path": str((self.src / "production-state.json").relative_to(self.repo)),
                "sha256": core.sha256_file(state_path) if state_path.is_file() else "0" * 64},
            "production_profile": {
                "path": str((self.src / "production-profile.json").relative_to(self.repo)),
                "sha256": core.sha256_file(self.src / "production-profile.json")},
            "implementation_commit_sha": core.repository_commit_sha(self.repo),
            "contract": core.contract_identity(
                self.repo, self.cfg, self.research_profile, self.publication_profile),
            "artifacts": artifacts,
            "recorded_at": "2026-09-12T11:00:00Z",
        })
        return report_path

    def _checkpoint_records(self) -> None:
        (self.src / "evidence" / "evidence-accepted.json").write_text('{"records": []}', encoding="utf-8")
        (self.src / "draft" / "draft-note.json").write_text('{"note": "v1"}', encoding="utf-8")
        for name in ("screening-accepted.json", "edition-views-accepted.json",
                     "materiality-ledger.json", "profile-completeness.json",
                     "candidate-matrix.json", "candidate-selection.json",
                     "synthesis-input.json", "synthesis-result.json"):
            (self.src / name).write_text('{"fixture": "%s"}' % name, encoding="utf-8")
        F = lambda *parts: self.src.joinpath(*parts)
        stage_rows = {
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
        stage_rows["discovery"] = [("discovery-acceptance", self.src / "discovery-accepted.json")]
        stamp = T0
        for name, from_state, to_state in PRODUCERS:
            stamp = stamp + timedelta(minutes=1)
            record_path = self.src / "orchestration" / "v2" / "checkpoints" / f"{from_state}.json"
            artifacts = [
                {"name": n, "path": str(p.relative_to(self.repo)), "sha256": core.sha256_file(p)}
                for n, p in stage_rows.get(name, [])
            ]
            if name == "validation":
                artifacts = artifacts + [
                    {"name": n, "path": str((self.src / "publication" / "v2" / f).relative_to(self.repo)),
                     "sha256": core.sha256_file(self.src / "publication" / "v2" / f)}
                    for n, f in [
                        ("reader-manuscript", "reader-manuscript-v2.json"),
                        ("quality-regression-bundle", "quality-regression-bundle-v2.json"),
                        ("semantic-review", "semantic-editorial-review-v2.json"),
                        ("visual-review", self.visual_filename),
                        ("reader-surface-gate", "reader-surface-gate-v2.json"),
                    ]
                ] + [
                    {"name": "publication-pdf",
                     "path": str((self.survey / "main.pdf").relative_to(self.repo)),
                     "sha256": core.sha256_file(self.survey / "main.pdf")},
                    {"name": "validated-source",
                     "path": str((self.survey / "main.tex").relative_to(self.repo)),
                     "sha256": core.sha256_file(self.survey / "main.tex")},
                    {"name": "evidence-accepted",
                     "path": str((self.src / "evidence" / "evidence-accepted.json").relative_to(self.repo)),
                     "sha256": core.sha256_file(self.src / "evidence" / "evidence-accepted.json")},
                ]
            report_path = self._contract_report(record_path, from_state, to_state, artifacts)
            core.write_json(record_path, {
                "schema_version": "2.0-rc1",
                "issue_id": self.issue,
                "from_state": from_state,
                "to_state": to_state,
                "checkpoints": sorted({n for (n, f, _t) in PRODUCERS if f == from_state}),
                "recorded_at": core.iso_utc(stamp),
                "implementation": {
                    "repository_commit_sha": core.repository_commit_sha(self.repo),
                    "orchestrator_version": self.cfg["orchestrator_version"],
                },
                "contract": core.contract_identity(
                    self.repo, self.cfg, self.research_profile, self.publication_profile),
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

    def _write_state(self, provisional: bool = False) -> None:
        history = [{
            "from": None if i == 0 else STATES[i - 1],
            "to": name,
            "recorded_at": core.iso_utc(T0 + timedelta(minutes=i)),
            "repository_commit_sha": core.repository_commit_sha(self.repo),
        } for i, name in enumerate(STATES)]
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
            "issue_id": self.issue,
            "research_profile": self.research_profile,
            "publication_profile": self.publication_profile,
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


def _state_path(fix: SpecialFixture) -> Path:
    return fix.src / "production-state.json"


def _special_advance_to_rc(fix: SpecialFixture, at: datetime) -> Path:
    pub = fix.src / "publication" / "v2"
    candidate = pub / "publication-candidate-v2.json"
    publication.build_candidate(
        fix.repo, fix.issue, fix.publication_profile,
        pub / "reader-manuscript-v2.json",
        fix.survey / "main.tex", fix.survey / "main.pdf", 12,
        pub / "quality-regression-bundle-v2.json",
        pub / "semantic-editorial-review-v2.json",
        pub / fix.visual_filename, candidate,
    )
    report = fix.src / "execution/validated-draft-stage-report.json"
    stage_validation.validate_stage(
        fix.repo, fix.cfg, _state_path(fix), {"publication-candidate": candidate},
        report, at + timedelta(hours=1),
    )
    reviews = fix.src / "execution/validated-draft-reviews.json"
    core.write_json(reviews, {"reviews": [{
        "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
        "executor": EXECUTOR,
        "evidence": "synthetic connected stage validation",
        "result_path": str(report.relative_to(fix.repo))}]})
    checkpoint = agent.build_stage_checkpoint(
        fix.repo, fix.cfg, _state_path(fix), {"publication-candidate": candidate},
        reviews, "DM001019 SpecialFixture boundary", at + timedelta(hours=1, minutes=1))
    updated = agent.advance_with_checkpoint(fix.repo, fix.cfg, _state_path(fix), checkpoint)
    assert updated["lifecycle_state"] == "RELEASE_CANDIDATE", updated
    assert updated["terminal_reason"] == "HUMAN_GATE_REACHED", updated
    return candidate


def _special_approve(fix: SpecialFixture, at: datetime) -> dict:
    return agent.approve_publication_preview(
        fix.repo, fix.cfg, _state_path(fix),
        "synthetic-human-fixture", at + timedelta(hours=2), "synthetic:publication-preview")


def _special_advance_to_frozen(fix: SpecialFixture, artifacts: dict[str, Path],
                               at: datetime, suffix: str) -> Path:
    output = fix.src / f"execution/freeze-stage-report-{suffix}.json"
    report = stage_validation.validate_stage(
        fix.repo, fix.cfg, _state_path(fix), artifacts, output, at + timedelta(hours=4))
    reviews = fix.src / f"execution/freeze-reviews-{suffix}.json"
    core.write_json(reviews, {"reviews": [{
        "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
        "executor": EXECUTOR,
        "evidence": "synthetic exact-authority Freeze validation",
        "result_path": str(report.relative_to(fix.repo))}]})
    checkpoint = agent.build_stage_checkpoint(
        fix.repo, fix.cfg, _state_path(fix), artifacts, reviews,
        "DM001019 SpecialFixture Freeze boundary", at + timedelta(hours=4, minutes=1))
    updated = agent.advance_with_checkpoint(fix.repo, fix.cfg, _state_path(fix), checkpoint)
    assert updated["lifecycle_state"] == "FROZEN", updated
    assert agent.validate_agent_state(fix.repo, fix.cfg, updated) == []
    return report


def _weekly_advance_to_rc(fix, at: datetime) -> Path:
    pub = fix.src / "publication" / "v2"
    candidate = pub / "publication-candidate-v2.json"
    publication.build_candidate(
        ROOT, WEEKLY_ISSUE, "WEEKLY_MAGAZINE", pub / "reader-manuscript-v2.json",
        fix.survey / "main.tex", fix.survey / "main.pdf", 1,
        pub / "quality-regression-bundle-v2.json",
        pub / "semantic-editorial-review-v2.json",
        pub / "visual-review-v2.json", candidate)
    cfg = _cfg()
    report = fix.src / "execution/validated-draft-stage-report.json"
    stage_validation.validate_stage(
        ROOT, cfg, fix.src / "production-state.json",
        {"publication-candidate": candidate}, report, at + timedelta(hours=1))
    reviews = fix.src / "execution/validated-draft-reviews.json"
    core.write_json(reviews, {"reviews": [{
        "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
        "executor": EXECUTOR, "evidence": "weekly advance",
        "result_path": str(report.relative_to(ROOT))}]})
    checkpoint = agent.build_stage_checkpoint(
        ROOT, cfg, fix.src / "production-state.json",
        {"publication-candidate": candidate}, reviews,
        "DM001019 Weekly boundary", at + timedelta(hours=1, minutes=1))
    updated = agent.advance_with_checkpoint(
        ROOT, cfg, fix.src / "production-state.json", checkpoint)
    assert updated["lifecycle_state"] == "RELEASE_CANDIDATE", updated
    assert updated["terminal_reason"] == "HUMAN_GATE_REACHED", updated
    return candidate


def _weekly_approve(fix, at: datetime) -> dict:
    return agent.approve_publication_preview(
        ROOT, _cfg(), fix.src / "production-state.json",
        "synthetic-human-fixture", at + timedelta(hours=2), "synthetic:publication-preview")


def _weekly_advance_to_frozen(fix, artifacts: dict[str, Path], at: datetime, suffix: str) -> Path:
    cfg = _cfg()
    output = fix.src / f"execution/freeze-stage-report-{suffix}.json"
    report = stage_validation.validate_stage(
        ROOT, cfg, fix.src / "production-state.json", artifacts, output, at + timedelta(hours=4))
    reviews = fix.src / f"execution/freeze-reviews-{suffix}.json"
    core.write_json(reviews, {"reviews": [{
        "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
        "executor": EXECUTOR, "evidence": "weekly freeze validation",
        "result_path": str(report.relative_to(ROOT))}]})
    checkpoint = agent.build_stage_checkpoint(
        ROOT, cfg, fix.src / "production-state.json", artifacts, reviews,
        "DM001019 Weekly Freeze boundary", at + timedelta(hours=4, minutes=1))
    updated = agent.advance_with_checkpoint(
        ROOT, cfg, fix.src / "production-state.json", checkpoint)
    assert updated["lifecycle_state"] == "FROZEN", updated
    assert agent.validate_agent_state(ROOT, cfg, updated) == []
    return report


def _extract_workflow_predicate(repo: Path) -> str:
    """Fail-closed extraction of the authority/predicate Python block."""
    text = (repo / ".github/workflows/survey-production-v2-release.yml").read_text(encoding="utf-8")
    step = "Resolve exact frozen release authority"
    assert text.count(step) == 1, "workflow step anchor not unique"
    seg = text.split(step, 1)[1]
    start_marker = "PYTHONPATH=. python - <<'PY' >> \"$GITHUB_OUTPUT\""
    assert seg.count(start_marker) == 1, "python heredoc start not unique"
    body = seg.split(start_marker, 1)[1]
    end_marker = "\n          PY\n"
    assert end_marker in body, "python heredoc end missing"
    block = textwrap.dedent(body.split(end_marker, 1)[0]).lstrip("\n")
    assert block.startswith("import os, pathlib, re"), "unexpected block head"
    assert "Release Manifest public identity mismatch" in block, "identity predicate missing"
    return block


def _run_workflow_predicate(repo: Path, issue: str, state_sha: str, manifest_sha: str,
                            outdir: Path) -> tuple[int, str, str]:
    """Execute the extracted block with cwd=repo; synthetic fixture only."""
    block = _extract_workflow_predicate(repo)
    outdir.mkdir(parents=True, exist_ok=True)
    gh_out = outdir / "github_output.txt"
    gh_out.write_text("", encoding="utf-8")
    env = {
        "PATH": "/usr/bin:/bin",
        "PYTHONPATH": str(repo),
        "PYTHONDONTWRITEBYTECODE": "1",
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_ALLOW_PROTOCOL": "file",
        "GIT_OPTIONAL_LOCKS": "0",
        "ISSUE_ID": issue,
        "EXPECTED_STATE_SHA": state_sha,
        "EXPECTED_MANIFEST_SHA": manifest_sha,
        "CONFIRMATION": f"release:{issue}",
        "REPOSITORY": "eariver/japanese-generative-ai-survey",
        "GITHUB_OUTPUT": str(gh_out),
    }
    proc = subprocess.run(
        [sys.executable, "-"], input=block, capture_output=True, text=True,
        cwd=str(repo), env=env, timeout=120,
    )
    return proc.returncode, proc.stdout, proc.stderr


def _snap_state_targets(
    state_file: Path, freeze: Path, manifest: Path
) -> tuple[bytes | None, tuple[bool, str | None], tuple[bool, str | None]]:
    """Capture State bytes plus both-target existence/content for no-write proofs."""

    def _target(path: Path) -> tuple[bool, str | None]:
        if not path.is_file() or path.is_symlink():
            return (path.exists(), None)
        return (True, core.sha256_file(path))

    state_bytes = state_file.read_bytes() if state_file.is_file() else None
    return (state_bytes, _target(freeze), _target(manifest))


class _PublicationLevel:
    """Self-contained publication-level fixture root (no State)."""

    def __init__(self, test: unittest.TestCase) -> None:
        self.case = _PUBMOD.SurveyPublicationV2Tests()
        self.case.setUp()
        test.addCleanup(self.case.doCleanups)

    @property
    def root(self) -> Path:
        return self.case.root

    @property
    def now(self) -> datetime:
        return self.case.now


def _build_second_chain(t) -> dict:
    """Second valid chain sharing C1's source/PDF/manuscript with distinct bundle/reviews/candidate."""
    issue = "SP001"
    p1dir = t.root / f"sources/{issue}/publication/v2"
    profile = t.root / f"sources/{issue}/production-profile.json"
    survey_root = t.root / quality.core.load_json(profile)["paths"]["survey_root"]
    pdf = survey_root / "main.pdf"
    source = survey_root / "main.tex"
    manifest1 = p1dir / "reader-manuscript-v2.json"
    detdir = p1dir / "quality-results-2"
    detdir.mkdir(parents=True, exist_ok=True)
    cfg = quality.core.load_json(t.root / quality.core.DEFAULT_CONFIG)
    checks = []
    for check_id in sorted(quality.expected_checks_by_kind(
            cfg, "THEMATIC", "LONGFORM_SPECIAL", {"DETERMINISTIC"})):
        result_path = detdir / f"{check_id}.json"
        quality.core.write_json(result_path, {"check_id": check_id, "status": "PASS", "chain": 2})
        checks.append({
            "check_id": check_id, "kind": "DETERMINISTIC", "status": "PASS",
            "executor": "dm001019-second-chain", "evidence": f"second-chain:{check_id}",
            "recorded_at": "2026-08-23T07:00:00Z",
            "result": {"path": str(result_path.relative_to(t.root)),
                        "sha256": quality.core.sha256_file(result_path)}})
    bundle2 = p1dir / "quality-regression-bundle-2-v2.json"
    quality.build_bundle(t.root, issue, source, pdf, checks, bundle2,
                         production_profile_path=profile)

    def _checks2(kind: str) -> list[dict]:
        rows = t.case._review_checks(profile, kind)
        for row in rows:
            row["detail"] = "Second-chain ChatGPT review passed " + row["check_id"]
        return rows

    sem2 = p1dir / "semantic-editorial-review-2-v2.json"
    vis2 = p1dir / "visual-review-2-v2.json"
    reader.build_review_record(t.root, manifest1, pdf, 12, "SEMANTIC_EDITORIAL",
                               _checks2("SEMANTIC_EDITORIAL"), "ChatGPT", t.now, sem2)
    reader.build_review_record(t.root, manifest1, pdf, 12, "VISUAL",
                               _checks2("VISUAL"), "ChatGPT", t.now, vis2)
    candidate2 = p1dir / "publication-candidate-2-v2.json"
    publication.build_candidate(
        t.root, issue, "LONGFORM_SPECIAL", manifest1, source, pdf, 12,
        bundle2, sem2, vis2, candidate2)
    return {"candidate2": candidate2}


def _build_special_second_chain(fix: SpecialFixture) -> dict:
    """Second valid Special chain sharing source/PDF/manuscript, distinct bundle/reviews/candidate."""
    pub = fix.src / "publication" / "v2"
    checks = fix._deterministic_checks(pub)
    for row in checks:
        row["executor"] = "dm001019-second-chain"
        row["evidence"] = "second-chain:" + row["check_id"]
    bundle2 = pub / "quality-regression-bundle-2-v2.json"
    quality.build_bundle(
        fix.repo, fix.issue, fix.survey / "main.tex", fix.survey / "main.pdf",
        checks, bundle2, production_profile_path=fix.profile_path)

    def _checks2(kind: str) -> list[dict]:
        rows = fix._review_checks(kind)
        for row in rows:
            row["detail"] = "Second-chain ChatGPT review passed " + row["check_id"]
        return rows

    sem2 = pub / "semantic-editorial-review-2-v2.json"
    vis2 = pub / "visual-review-2-v2.json"
    reader.build_review_record(
        fix.repo, pub / "reader-manuscript-v2.json", fix.survey / "main.pdf", 12,
        "SEMANTIC_EDITORIAL", _checks2("SEMANTIC_EDITORIAL"), "ChatGPT", T0, sem2)
    reader.build_review_record(
        fix.repo, pub / "reader-manuscript-v2.json", fix.survey / "main.pdf", 12,
        "VISUAL", _checks2("VISUAL"), "ChatGPT", T0, vis2)
    candidate2 = pub / "publication-candidate-2-v2.json"
    publication.build_candidate(
        fix.repo, fix.issue, fix.publication_profile,
        pub / "reader-manuscript-v2.json",
        fix.survey / "main.tex", fix.survey / "main.pdf", 12,
        bundle2, sem2, vis2, candidate2)
    return {"candidate2": candidate2}


class DM001019CanonicalFreezeTests(unittest.TestCase):
    """Lower-level builder: exact authority, identity and writer preflight."""

    def freeze_targets(self, pub: Path, tag: str) -> tuple[Path, Path]:
        return pub / f"freeze-record-{tag}-v2.json", pub / f"release-manifest-{tag}-v2.json"

    def test_l1_weekly_positive_freeze_validates(self) -> None:
        fix = WeeklyCanonicalFixture(ROOT)
        self.addCleanup(fix.cleanup)
        at = T0 + timedelta(days=30)
        candidate = _weekly_advance_to_rc(fix, at)
        _weekly_approve(fix, at)
        cfg = _cfg()
        approval = fix.src / cfg["state_authority"]["publication_preview_approval_path"]
        pub = fix.src / "publication" / "v2"
        freeze, manifest = self.freeze_targets(pub, "l1")
        out_freeze, out_manifest = publication.build_freeze(
            ROOT, candidate, approval, at + timedelta(hours=3), freeze, manifest)
        self.assertEqual(out_freeze.read_bytes(), freeze.read_bytes())
        payload = publication.validate_release_manifest(ROOT, out_manifest)
        self.assertEqual(payload["release_identity"], "weekly/2026-W35")
        freeze_payload = core.load_json(out_freeze)
        self.assertEqual(freeze_payload["publication_candidate_sha256"], core.sha256_file(candidate))
        self.assertEqual(payload["freeze_record_sha256"], core.sha256_file(out_freeze))

    def test_l2_special_convergent_positive_and_wrapper_byte_equal(self) -> None:
        at = T0 + timedelta(days=31)
        fix = SpecialFixture(ROOT, "SP001", "surveys/special/SP001")
        self.addCleanup(fix.cleanup)
        candidate = _special_advance_to_rc(fix, at)
        _special_approve(fix, at)
        pub = fix.src / "publication" / "v2"
        # Wrapper writes first; outputs reset; canonical writes second.
        w_freeze, w_manifest = profiled.build_profiled_freeze(
            ROOT, fix.cfg, _state_path(fix), at + timedelta(hours=3))
        w_freeze_bytes, w_manifest_bytes = w_freeze.read_bytes(), w_manifest.read_bytes()
        w_freeze.unlink()
        w_manifest.unlink()
        approval = fix.src / fix.cfg["state_authority"]["publication_preview_approval_path"]
        c_freeze, c_manifest = publication.build_freeze(
            ROOT, candidate, approval, at + timedelta(hours=3),
            pub / "freeze-record-v2.json", pub / "release-manifest-v2.json")
        self.assertEqual(c_freeze.read_bytes(), w_freeze_bytes)
        self.assertEqual(c_manifest.read_bytes(), w_manifest_bytes)
        self.assertEqual(core.load_json(c_manifest)["release_identity"], "special/SP001")

    def test_l3_legacy_visual_cannot_enter_candidate(self) -> None:
        t = _PublicationLevel(self)
        p1 = t.case._candidate()
        approval = p1["publication_dir"] / "publication-preview-approval-2-v2.json"
        publication.build_preview_approval(
            t.root, p1["candidate"], approval, "human-reviewer", t.now, "review:SP001:preview")
        legacy = p1["publication_dir"] / "legacy-visual-v2.json"
        shutil.copy2(ROOT / publication.VISUAL_REVIEW_SCHEMA,
                      t.root / publication.VISUAL_REVIEW_SCHEMA)
        publication.build_visual_review(
            t.root, approval,
            [{"check_id": "VISUAL_CONFIRM", "status": "PASS", "detail": "legacy"}],
            "legacy-tool", t.now, legacy)
        with self.assertRaisesRegex(ValueError, "kind mismatch|review_kind|Publication Review"):
            publication.build_candidate(
                t.root, "SP001", "LONGFORM_SPECIAL",
                p1["manifest"], p1["source"], p1["pdf"], 12,
                p1["bundle"], p1["semantic"], legacy,
                p1["publication_dir"] / "candidate-legacy-v2.json")

    def test_l4_mixed_candidate_same_pdf_rejected_before_writes(self) -> None:
        t = _PublicationLevel(self)
        p1 = t.case._candidate()
        c1 = p1["candidate"]
        approval1 = p1["publication_dir"] / "publication-preview-approval-v2.json"
        publication.build_preview_approval(
            t.root, c1, approval1, "human-reviewer", t.now, "review:SP001:preview")
        c2 = _build_second_chain(t)["candidate2"]
        self.assertNotEqual(core.sha256_file(c1), core.sha256_file(c2))
        c1_pdf = publication.validate_candidate(t.root, c1)["pdf"]["sha256"]
        c2_pdf = publication.validate_candidate(t.root, c2)["pdf"]["sha256"]
        self.assertEqual(c1_pdf, c2_pdf)
        freeze = p1["publication_dir"] / "freeze-mixed-v2.json"
        manifest = p1["publication_dir"] / "release-manifest-mixed-v2.json"
        with self.assertRaisesRegex(ValueError, "does not bind the exact Publication Candidate"):
            publication.build_freeze(t.root, c2, approval1, t.now, freeze, manifest)
        self.assertFalse(freeze.exists())
        self.assertFalse(manifest.exists())
        with self.assertRaisesRegex(ValueError, "does not bind the exact Publication Candidate"):
            publication._prepare_freeze_inputs(t.root, c2, approval1)

    def test_l5_divergent_special_profile_identity(self) -> None:
        at = T0 + timedelta(days=32)
        fix = SpecialFixture(ROOT, "SP002", "surveys/special/SP002-DIVERGED")
        self.addCleanup(fix.cleanup)
        candidate = _special_advance_to_rc(fix, at)
        _special_approve(fix, at)
        approval = fix.src / fix.cfg["state_authority"]["publication_preview_approval_path"]
        pub = fix.src / "publication" / "v2"
        freeze = pub / "freeze-record-v2.json"
        manifest = pub / "release-manifest-v2.json"
        c_freeze, c_manifest = publication.build_freeze(
            ROOT, candidate, approval, at + timedelta(hours=3), freeze, manifest)
        payload = core.load_json(c_manifest)
        self.assertEqual(payload["release_identity"], "special/SP002-DIVERGED")
        raw = c_manifest.read_bytes().decode("utf-8")
        self.assertIn("special/SP002-DIVERGED", raw)
        self.assertNotIn('"release_identity": "special/SP002"', raw)

    def test_l6_writer_conflict_matrix(self) -> None:
        t = _PublicationLevel(self)
        p1 = t.case._candidate()
        c1 = p1["candidate"]
        approval1 = p1["publication_dir"] / "publication-preview-approval-v2.json"
        publication.build_preview_approval(
            t.root, c1, approval1, "human-reviewer", t.now, "review:SP001:preview")
        pub = p1["publication_dir"]
        base_freeze = pub / "freeze-ok-v2.json"
        base_manifest = pub / "manifest-ok-v2.json"

        def attempt(freeze: Path, manifest: Path) -> str:
            try:
                publication.build_freeze(t.root, c1, approval1, t.now, freeze, manifest)
            except ValueError as exc:
                return str(exc)
            return "BUILT"

        # Divergent pre-existing Freeze.
        core.write_json(base_freeze, {"schema_version": "2.0-rc1", "foreign": True})
        self.assertIn("refusing to overwrite divergent Freeze record",
                      attempt(base_freeze, base_manifest))
        self.assertFalse(base_manifest.exists())
        base_freeze.unlink()
        # Pre-existing Manifest without Freeze.
        core.write_json(base_manifest, {"schema_version": "2.0-rc1", "foreign": True})
        self.assertIn("refusing to overwrite divergent Release manifest",
                      attempt(base_freeze, base_manifest))
        self.assertFalse(base_freeze.exists())
        # Compatible Manifest without Freeze: conservative refusal.
        candidate = publication.validate_candidate(t.root, c1)
        prep = publication._prepare_freeze_inputs(t.root, c1, approval1)
        freeze_payload = publication._build_freeze_payload(
            repo_root=t.root, candidate_path=c1, candidate=candidate,
            approval_path=approval1, approval=prep["approval"],
            visual_path=prep["visual_path"], frozen_at=t.now)
        freeze_sha = core.sha256_bytes(core.json_bytes(freeze_payload))
        core.write_json(base_manifest, publication._build_manifest_payload(
            repo_root=t.root, freeze_path=base_freeze, freeze_record_sha256=freeze_sha,
            release_identity=publication.profile_release_identity(prep["profile"]),
            source_path=candidate["source"]["path"],
            source_sha256=candidate["source"]["sha256"],
            pdf_path=candidate["pdf"]["path"], pdf_sha256=candidate["pdf"]["sha256"],
            page_count=candidate["pdf"]["page_count"], issue_id=candidate["issue_id"]))
        self.assertIn("exists without its Freeze record", attempt(base_freeze, base_manifest))
        self.assertFalse(base_freeze.exists())
        base_manifest.unlink()
        # Same target for both outputs.
        self.assertIn("must differ", attempt(base_freeze, base_freeze))
        # Manifest target overlapping the Candidate input.
        self.assertIn("overlaps a Freeze authority input", attempt(base_freeze, c1))
        # Symlink target.
        real = pub / "freeze-real-v2.json"
        link = pub / "freeze-link-v2.json"
        real.write_bytes(b"{}")
        os.symlink(real, link)
        self.assertIn("is a symlink", attempt(link, base_manifest))
        self.assertFalse(base_manifest.exists())
        link.unlink()
        real.unlink()
        # Non-regular target (directory).
        direc = pub / "manifest-dir-v2.json"
        direc.mkdir()
        self.assertIn("not a regular file", attempt(base_freeze, direc))
        self.assertFalse(base_freeze.exists())
        direc.rmdir()
        # Symlinked ancestor component.
        outside = pub / "outside-ancestor"
        outside.mkdir()
        linked_parent = pub / "linked-parent"
        os.symlink(outside, linked_parent)
        self.assertIn("ancestor is a symlink",
                      attempt(linked_parent / "freeze-v2.json", linked_parent / "manifest-v2.json"))
        linked_parent.unlink()
        shutil.rmtree(outside)
        # Manifest target overlapping the bound Candidate PDF input.
        pdf = p1["pdf"]
        self.assertIn("overlaps a Freeze authority input",
                      attempt(pub / "freeze-pdf-alias-v2.json", pdf))
        self.assertFalse((pub / "freeze-pdf-alias-v2.json").exists())
        # FIFO target: refused by type check without blocking.
        fifo = pub / "manifest-fifo-v2.json"
        os.mkfifo(fifo)
        self.assertIn("not a regular file", attempt(base_freeze, fifo))
        self.assertFalse(base_freeze.exists())
        fifo.unlink()
        # Malformed existing bytes: divergent refusal, not incidental parse use.
        malformed = pub / "freeze-malformed-v2.json"
        malformed.write_bytes(b"{not json")
        self.assertIn("refusing to overwrite divergent Freeze record",
                      attempt(malformed, base_manifest))
        self.assertFalse(base_manifest.exists())
        self.assertEqual(malformed.read_bytes(), b"{not json")
        malformed.unlink()

    def test_l9_nested_and_dotdot_outputs_rejected_pre_write(self) -> None:
        t = _PublicationLevel(self)
        p1 = t.case._candidate()
        c1 = p1["candidate"]
        approval1 = p1["publication_dir"] / "publication-preview-approval-v2.json"
        publication.build_preview_approval(
            t.root, c1, approval1, "human-reviewer", t.now, "review:SP001:preview")
        pub = p1["publication_dir"]

        def attempt(freeze: Path, manifest: Path) -> str:
            try:
                publication.build_freeze(t.root, c1, approval1, t.now, freeze, manifest)
            except ValueError as exc:
                return str(exc)
            return "BUILT"

        # Manifest nested under the Freeze file, both absent.
        nest_f = pub / "nest-freeze-v2.json"
        nest_m = nest_f / "manifest-v2.json"
        self.assertIn("must not nest", attempt(nest_f, nest_m))
        self.assertFalse(nest_f.exists())
        self.assertFalse(nest_m.exists())
        # Freeze nested under the Manifest file, both absent.
        nest_m2 = pub / "nest-manifest-v2.json"
        nest_f2 = nest_m2 / "freeze-v2.json"
        self.assertIn("must not nest", attempt(nest_f2, nest_m2))
        self.assertFalse(nest_m2.exists())
        self.assertFalse(nest_f2.exists())
        # Lexical `..` rejected before normalization, even resolving inside.
        dotdot = pub / "sub" / ".." / "dotdot-freeze-v2.json"
        self.assertIn("'..'", attempt(dotdot, pub / "dotdot-manifest-v2.json"))
        self.assertFalse((pub / "dotdot-freeze-v2.json").exists())
        self.assertFalse((pub / "dotdot-manifest-v2.json").exists())
        self.assertFalse((pub / "sub").exists())

    def test_l7_same_payload_retry_is_idempotent(self) -> None:
        t = _PublicationLevel(self)
        p1 = t.case._candidate()
        c1 = p1["candidate"]
        approval1 = p1["publication_dir"] / "publication-preview-approval-v2.json"
        publication.build_preview_approval(
            t.root, c1, approval1, "human-reviewer", t.now, "review:SP001:preview")
        pub = p1["publication_dir"]
        freeze = pub / "freeze-record-v2.json"
        manifest = pub / "release-manifest-v2.json"
        f1, m1 = publication.build_freeze(t.root, c1, approval1, t.now, freeze, manifest)
        first = (f1.read_bytes(), m1.read_bytes())
        f2, m2 = publication.build_freeze(t.root, c1, approval1, t.now, freeze, manifest)
        self.assertEqual((f2.read_bytes(), m2.read_bytes()), first)
        publication.validate_release_manifest(t.root, m2)

    def test_l8_install_failures_leave_fail_closed_state(self) -> None:
        t = _PublicationLevel(self)
        p1 = t.case._candidate()
        c1 = p1["candidate"]
        approval1 = p1["publication_dir"] / "publication-preview-approval-v2.json"
        publication.build_preview_approval(
            t.root, c1, approval1, "human-reviewer", t.now, "review:SP001:preview")
        pub = p1["publication_dir"]
        # (a) Pre-open failure via read-only directory.
        ro_freeze = pub / "ro-freeze-v2.json"
        ro_manifest = pub / "ro-manifest-v2.json"
        pub.chmod(0o555)
        try:
            with self.assertRaisesRegex(ValueError, "install failed|unreadable|ancestor"):
                publication.build_freeze(t.root, c1, approval1, t.now, ro_freeze, ro_manifest)
        finally:
            pub.chmod(0o755)
        self.assertFalse(ro_freeze.exists())
        self.assertFalse(ro_manifest.exists())
        # (b) Mid-write failure at the real os.write boundary: partial then raise.
        real_write = os.write
        state = {"failed": False}

        def flaky_write(fd: int, data: bytes) -> int:
            if not state["failed"] and len(data) > 512:
                state["failed"] = True
                real_write(fd, bytes(data[: len(data) // 2]))
                raise OSError("injected mid-write failure")
            return real_write(fd, data)

        mid_freeze = pub / "mid-freeze-v2.json"
        mid_manifest = pub / "mid-manifest-v2.json"
        with mock.patch.object(os, "write", side_effect=flaky_write):
            with self.assertRaisesRegex(ValueError, "owned partial file removed"):
                publication.build_freeze(t.root, c1, approval1, t.now, mid_freeze, mid_manifest)
        self.assertTrue(state["failed"])
        self.assertFalse(mid_freeze.exists())
        self.assertFalse(mid_manifest.exists())
        # (c) Manifest-install failure retains the completed Freeze for retry.
        real_open = os.open

        def fail_manifest(path, *args, **kwargs):
            if str(path).endswith("release-manifest-v2.json"):
                raise OSError("injected manifest install failure")
            return real_open(path, *args, **kwargs)

        keep_freeze = pub / "freeze-record-v2.json"
        keep_manifest = pub / "release-manifest-v2.json"
        with mock.patch.object(os, "open", side_effect=fail_manifest):
            with self.assertRaisesRegex(ValueError, "completed Freeze record retained"):
                publication.build_freeze(t.root, c1, approval1, t.now, keep_freeze, keep_manifest)
        self.assertTrue(keep_freeze.is_file())
        self.assertFalse(keep_manifest.exists())
        f2, m2 = publication.build_freeze(t.root, c1, approval1, t.now, keep_freeze, keep_manifest)
        self.assertEqual(f2.read_bytes(), keep_freeze.read_bytes())
        publication.validate_release_manifest(t.root, m2)


    def test_l10_reformatted_existing_bytes_preserved(self) -> None:
        t = _PublicationLevel(self)
        p1 = t.case._candidate()
        c1 = p1["candidate"]
        approval1 = p1["publication_dir"] / "publication-preview-approval-v2.json"
        publication.build_preview_approval(
            t.root, c1, approval1, "human-reviewer", t.now, "review:SP001:preview")
        pub = p1["publication_dir"]
        freeze = pub / "freeze-record-v2.json"
        manifest = pub / "release-manifest-v2.json"
        publication.build_freeze(t.root, c1, approval1, t.now, freeze, manifest)
        reformatted = (json.dumps(json.loads(freeze.read_bytes()),
                                  indent=4, ensure_ascii=False) + "\n").encode("utf-8")
        self.assertNotEqual(reformatted, freeze.read_bytes())
        freeze.write_bytes(reformatted)
        manifest.unlink()
        f2, m2 = publication.build_freeze(t.root, c1, approval1, t.now, freeze, manifest)
        self.assertEqual(f2.read_bytes(), reformatted)
        self.assertEqual(core.load_json(m2)["freeze_record_sha256"], core.sha256_bytes(reformatted))
        reformatted_manifest = (json.dumps(json.loads(m2.read_bytes()),
                                           indent=4, ensure_ascii=False) + "\n").encode("utf-8")
        m2.write_bytes(reformatted_manifest)
        f3, m3 = publication.build_freeze(t.root, c1, approval1, t.now, freeze, manifest)
        self.assertEqual(f3.read_bytes(), reformatted)
        self.assertEqual(m3.read_bytes(), reformatted_manifest)


class DM001019WriterBoundaryTests(unittest.TestCase):
    """Install-boundary faults: collisions, close errors, residuals, drift."""

    def _valid_chain(self, t):
        p1 = t.case._candidate()
        c1 = p1["candidate"]
        approval1 = p1["publication_dir"] / "publication-preview-approval-v2.json"
        publication.build_preview_approval(
            t.root, c1, approval1, "human-reviewer", t.now, "review:SP001:preview")
        return p1, c1, approval1

    def _plan(self, t, c1, approval1, freeze: Path, manifest: Path):
        prep = publication._prepare_freeze_inputs(t.root, c1, approval1)
        candidate = prep["candidate"]
        freeze_payload = publication._build_freeze_payload(
            repo_root=t.root, candidate_path=c1, candidate=candidate,
            approval_path=approval1, approval=prep["approval"],
            visual_path=prep["visual_path"], frozen_at=t.now)
        source, pdf = candidate["source"], candidate["pdf"]
        tag = publication.profile_release_identity(prep["profile"])
        return publication._preflight_freeze_pair(
            t.root, freeze, manifest, prep, freeze_payload,
            lambda sha, target: publication._build_manifest_payload(
                repo_root=t.root, freeze_path=target, freeze_record_sha256=sha,
                release_identity=tag, source_path=source["path"],
                source_sha256=source["sha256"], pdf_path=pdf["path"],
                pdf_sha256=pdf["sha256"], page_count=pdf["page_count"],
                issue_id=candidate["issue_id"]))

    def test_fileexists_symlink_identical_bytes_refused(self) -> None:
        t = _PublicationLevel(self)
        p1 = t.case._candidate()
        real = p1["publication_dir"] / "collision-real-v2.json"
        data = '{"identical": "bytes"}\n'.encode("utf-8")
        real.write_bytes(data)
        link = p1["publication_dir"] / "collision-link-v2.json"
        os.symlink(real, link)
        with mock.patch.object(os, "open", side_effect=FileExistsError("injected collision")):
            with self.assertRaisesRegex(ValueError, "target is a symlink"):
                publication._install_owned_json(t.root, link, data, "Collision probe")
        self.assertTrue(link.is_symlink())
        self.assertEqual(real.read_bytes(), data)

    def test_fileexists_fifo_refused_without_blocking(self) -> None:
        t = _PublicationLevel(self)
        p1 = t.case._candidate()
        fifo = p1["publication_dir"] / "collision-fifo-v2.json"
        os.mkfifo(fifo)
        with mock.patch.object(os, "open", side_effect=FileExistsError("injected collision")):
            with self.assertRaisesRegex(ValueError, "not a regular file"):
                publication._install_owned_json(t.root, fifo, b"{}", "Collision probe")
        self.assertTrue(os.lstat(fifo) is not None)
        fifo.unlink()

    def test_close_failure_never_reports_success(self) -> None:
        t = _PublicationLevel(self)
        p1, c1, approval1 = self._valid_chain(t)
        freeze = p1["publication_dir"] / "freeze-close-v2.json"
        manifest = p1["publication_dir"] / "manifest-close-v2.json"
        real_close = os.close
        calls = {"n": 0}

        def flaky_close(fd: int):
            calls["n"] += 1
            if calls["n"] == 1:
                real_close(fd)
                raise OSError("injected close failure")
            return real_close(fd)

        with mock.patch.object(os, "close", side_effect=flaky_close):
            with self.assertRaisesRegex(ValueError, "close failed but complete verified bytes retained"):
                publication.build_freeze(t.root, c1, approval1, t.now, freeze, manifest)
        self.assertTrue(calls["n"] >= 1)
        retained = freeze.read_bytes()
        f2, _m2 = publication.build_freeze(t.root, c1, approval1, t.now, freeze, manifest)
        self.assertEqual(f2.read_bytes(), retained)

    def test_manifest_close_failure_retains_freeze(self) -> None:
        t = _PublicationLevel(self)
        p1, c1, approval1 = self._valid_chain(t)
        freeze = p1["publication_dir"] / "freeze-mclose-v2.json"
        manifest = p1["publication_dir"] / "manifest-mclose-v2.json"
        real_close = os.close
        calls = {"n": 0}

        def flaky_close(fd: int):
            calls["n"] += 1
            if calls["n"] == 2:
                real_close(fd)
                raise OSError("injected manifest close failure")
            return real_close(fd)

        with mock.patch.object(os, "close", side_effect=flaky_close):
            with self.assertRaisesRegex(ValueError, "completed Freeze record retained"):
                publication.build_freeze(t.root, c1, approval1, t.now, freeze, manifest)
        self.assertTrue(freeze.is_file())
        retained = freeze.read_bytes()
        f2, m2 = publication.build_freeze(t.root, c1, approval1, t.now, freeze, manifest)
        self.assertEqual(f2.read_bytes(), retained)
        publication.validate_release_manifest(t.root, m2)

    def test_owned_partial_identity_replacement_preserved(self) -> None:
        t = _PublicationLevel(self)
        p1 = t.case._candidate()
        target = p1["publication_dir"] / "owned-replaced-v2.json"
        data = b'{"owned": true}\n'
        publication._install_owned_json(t.root, target, data, "Owned probe")
        st0 = os.lstat(target)
        target.unlink()
        foreign = b'{"foreign": "replacement"}\n'
        target.write_bytes(foreign)
        with self.assertRaisesRegex(ValueError, "identity changed"):
            publication._remove_owned_partial(
                target, st0.st_dev, st0.st_ino, data, "Owned probe", ValueError("x"))
        self.assertEqual(target.read_bytes(), foreign)

    def test_owned_partial_non_prefix_preserved(self) -> None:
        t = _PublicationLevel(self)
        p1 = t.case._candidate()
        target = p1["publication_dir"] / "owned-nonprefix-v2.json"
        foreign = b'{"entirely": "different content, longer than intended"}\n'
        target.write_bytes(foreign)
        st = os.lstat(target)
        with self.assertRaisesRegex(ValueError, "unverifiable residual"):
            publication._remove_owned_partial(
                target, st.st_dev, st.st_ino, b'{"short": 1}\n', "Owned probe", ValueError("x"))
        self.assertEqual(target.read_bytes(), foreign)

    def test_owned_partial_symlink_preserved(self) -> None:
        t = _PublicationLevel(self)
        p1 = t.case._candidate()
        real = p1["publication_dir"] / "owned-real-v2.json"
        real.write_bytes(b'{"real": true}\n')
        link = p1["publication_dir"] / "owned-link-v2.json"
        os.symlink(real, link)
        st = os.lstat(real)
        with self.assertRaisesRegex(ValueError, "residual is a symlink"):
            publication._remove_owned_partial(
                link, st.st_dev, st.st_ino, b"{}", "Owned probe", ValueError("x"))
        self.assertTrue(link.is_symlink())

    def test_close_failure_leaves_unrelated_descriptor_usable(self) -> None:
        # G2: after a failed os.close the numeric fd may already be reused.
        # The installer must not retry-close it. The injection really closes
        # the Freeze fd, immediately opens an unrelated sentinel (which may
        # reuse the same number), then raises; the sentinel must stay usable
        # and only the test closes it.
        t = _PublicationLevel(self)
        p1, c1, approval1 = self._valid_chain(t)
        freeze = p1["publication_dir"] / "freeze-sentinel-v2.json"
        manifest = p1["publication_dir"] / "manifest-sentinel-v2.json"
        sentinel = p1["publication_dir"] / "sentinel.bin"
        real_close = os.close
        real_open = os.open
        state: dict = {}

        def flaky_close(fd: int):
            real_close(fd)
            if "sentinel" not in state:
                state["sentinel"] = real_open(
                    str(sentinel), os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o644)
            raise OSError("injected close failure")

        with mock.patch.object(os, "close", side_effect=flaky_close):
            with self.assertRaisesRegex(ValueError, "close failed but complete verified bytes retained"):
                publication.build_freeze(t.root, c1, approval1, t.now, freeze, manifest)
        sfd = state["sentinel"]
        os.write(sfd, b"sentinel-ok")
        os.fstat(sfd)
        real_close(sfd)
        state.clear()
        self.assertEqual(sentinel.read_bytes(), b"sentinel-ok")
        retained = freeze.read_bytes()
        f2, m2 = publication.build_freeze(t.root, c1, approval1, t.now, freeze, manifest)
        self.assertEqual(f2.read_bytes(), retained)
        publication.validate_release_manifest(t.root, m2)

    def test_freeze_output_drift_before_second_install_no_manifest(self) -> None:
        # G3: inputs intact but the installed Freeze output drifted before
        # the Manifest half. No Manifest may be written; the drifted Freeze
        # is retained as found with no identical-retry promise.
        t = _PublicationLevel(self)
        p1, c1, approval1 = self._valid_chain(t)
        freeze = p1["publication_dir"] / "freeze-outdrift-v2.json"
        manifest = p1["publication_dir"] / "manifest-outdrift-v2.json"
        plan = self._plan(t, c1, approval1, freeze, manifest)
        publication._install_freeze_target(t.root, plan)
        freeze.write_bytes(b'{"drifted": "after freeze install"}\n')
        with self.assertRaisesRegex(ValueError, "drift before second install"):
            publication._install_manifest_target(t.root, plan)
        self.assertFalse(manifest.exists())
        self.assertEqual(freeze.read_bytes(), b'{"drifted": "after freeze install"}\n')
        # A full-pair retry then refuses at Freeze reinstall (divergent
        # existing output), still without writing any Manifest.
        with self.assertRaisesRegex(ValueError, "refusing to overwrite divergent Freeze record"):
            publication._install_freeze_pair(t.root, plan)
        self.assertFalse(manifest.exists())
        self.assertEqual(freeze.read_bytes(), b'{"drifted": "after freeze install"}\n')

    def test_input_drift_before_first_write_leaves_no_outputs(self) -> None:
        t = _PublicationLevel(self)
        p1, c1, approval1 = self._valid_chain(t)
        freeze = p1["publication_dir"] / "freeze-drift1-v2.json"
        manifest = p1["publication_dir"] / "manifest-drift1-v2.json"
        plan = self._plan(t, c1, approval1, freeze, manifest)
        p1["source"].write_text("drifted after preparation\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "changed before first write"):
            publication._install_freeze_target(t.root, plan)
        self.assertFalse(freeze.exists())
        self.assertFalse(manifest.exists())

    def test_input_drift_before_second_install_retains_freeze(self) -> None:
        t = _PublicationLevel(self)
        p1, c1, approval1 = self._valid_chain(t)
        freeze = p1["publication_dir"] / "freeze-drift2-v2.json"
        manifest = p1["publication_dir"] / "manifest-drift2-v2.json"
        plan = self._plan(t, c1, approval1, freeze, manifest)
        installed = publication._install_freeze_target(t.root, plan)
        planned_bytes = installed.read_bytes()
        p1["source"].write_text("drifted after freeze install\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "changed before second install"):
            publication._install_manifest_target(t.root, plan)
        self.assertEqual(freeze.read_bytes(), planned_bytes)
        self.assertFalse(manifest.exists())
        # Through the full pair entry the same drift refuses even earlier
        # (freeze-half input recheck), still with Freeze intact and no Manifest.
        # The pair wrapper's "retained as found" drift text covers truly
        # concurrent inter-half mutation, which no single-threaded test can
        # produce; it is defensive-only and makes no retry promise.
        with self.assertRaisesRegex(ValueError, "changed before first write"):
            publication._install_freeze_pair(t.root, plan)
        self.assertEqual(freeze.read_bytes(), planned_bytes)
        self.assertFalse(manifest.exists())


class DM001019WrapperFreezeTests(unittest.TestCase):
    """Profiled wrapper: real State gates plus shared authority/writer."""

    def test_w1_weekly_wrapper_positive(self) -> None:
        fix = WeeklyCanonicalFixture(ROOT)
        self.addCleanup(fix.cleanup)
        at = T0 + timedelta(days=40)
        _weekly_advance_to_rc(fix, at)
        _weekly_approve(fix, at)
        state_file = fix.src / "production-state.json"
        pub = fix.src / "publication" / "v2"
        before = _snap_state_targets(state_file, pub / "freeze-record-v2.json",
                                     pub / "release-manifest-v2.json")
        freeze, manifest = profiled.build_profiled_freeze(
            ROOT, _cfg(), state_file, at + timedelta(hours=3))
        payload = publication.validate_release_manifest(ROOT, manifest)
        self.assertEqual(payload["release_identity"], "weekly/2026-W35")
        self.assertEqual(payload["freeze_record_sha256"], core.sha256_file(freeze))
        # The wrapper never rewrites State; both targets were absent before.
        self.assertEqual(state_file.read_bytes(), before[0])
        self.assertEqual(before[1], (False, None))
        self.assertEqual(before[2], (False, None))

    def test_w2_special_convergent_wrapper_positive(self) -> None:
        at = T0 + timedelta(days=41)
        fix = SpecialFixture(ROOT, "SP001", "surveys/special/SP001")
        self.addCleanup(fix.cleanup)
        _special_advance_to_rc(fix, at)
        _special_approve(fix, at)
        freeze, manifest = profiled.build_profiled_freeze(
            ROOT, fix.cfg, _state_path(fix), at + timedelta(hours=3))
        payload = publication.validate_release_manifest(ROOT, manifest)
        self.assertEqual(payload["release_identity"], "special/SP001")

    def test_w3_special_divergent_wrapper_positive(self) -> None:
        at = T0 + timedelta(days=42)
        fix = SpecialFixture(ROOT, "SP002", "surveys/special/SP002-DIVERGED")
        self.addCleanup(fix.cleanup)
        _special_advance_to_rc(fix, at)
        _special_approve(fix, at)
        freeze, manifest = profiled.build_profiled_freeze(
            ROOT, fix.cfg, _state_path(fix), at + timedelta(hours=3))
        payload = publication.validate_release_manifest(ROOT, manifest)
        self.assertEqual(payload["release_identity"], "special/SP002-DIVERGED")

    def test_w3b_divergent_builders_agree_byte_equal(self) -> None:
        at = T0 + timedelta(days=43)
        fix = SpecialFixture(ROOT, "SP002", "surveys/special/SP002-DIVERGED")
        self.addCleanup(fix.cleanup)
        candidate = _special_advance_to_rc(fix, at)
        _special_approve(fix, at)
        approval = fix.src / fix.cfg["state_authority"]["publication_preview_approval_path"]
        pub = fix.src / "publication" / "v2"
        # Canonical writes first; outputs reset; wrapper writes second.
        c_freeze, c_manifest = publication.build_freeze(
            ROOT, candidate, approval, at + timedelta(hours=3),
            pub / "freeze-record-v2.json", pub / "release-manifest-v2.json")
        c_bytes = (c_freeze.read_bytes(), c_manifest.read_bytes())
        c_freeze.unlink()
        c_manifest.unlink()
        w_freeze, w_manifest = profiled.build_profiled_freeze(
            ROOT, fix.cfg, _state_path(fix), at + timedelta(hours=3))
        self.assertEqual((w_freeze.read_bytes(), w_manifest.read_bytes()), c_bytes)

    def test_w4_wrapper_negatives_leave_no_outputs(self) -> None:
        at = T0 + timedelta(days=44)
        fix = SpecialFixture(ROOT, "SP001", "surveys/special/SP001")
        self.addCleanup(fix.cleanup)
        _special_advance_to_rc(fix, at)
        _special_approve(fix, at)
        cfg = fix.cfg
        state_file = _state_path(fix)
        pub = fix.src / "publication" / "v2"
        freeze, manifest = pub / "freeze-record-v2.json", pub / "release-manifest-v2.json"

        def attempt() -> str:
            try:
                profiled.build_profiled_freeze(ROOT, cfg, state_file, at + timedelta(hours=3))
            except ValueError as exc:
                return str(exc)
            return "BUILT"

        def assert_unchanged(before) -> None:
            self.assertEqual(state_file.read_bytes(), before[0])
            self.assertFalse(freeze.exists())
            self.assertFalse(manifest.exists())

        # Stale approval provenance in State.
        state = core.load_json(state_file)
        state["human_gate_provenance"]["publication_preview"] = {
            **state["human_gate_provenance"]["publication_preview"], "sha256": "f" * 64}
        core.write_json(state_file, state)
        before = _snap_state_targets(state_file, freeze, manifest)
        self.assertIn("approval authority drift", attempt())
        assert_unchanged(before)
        # Restore valid State by re-approving is impossible post-decision; rebuild.
        fix.cleanup()
        fix = SpecialFixture(ROOT, "SP001", "surveys/special/SP001")
        _special_advance_to_rc(fix, at)
        _special_approve(fix, at)
        state_file = _state_path(fix)
        pub = fix.src / "publication" / "v2"
        freeze, manifest = pub / "freeze-record-v2.json", pub / "release-manifest-v2.json"
        # Profile drift.
        profile = core.load_json(fix.profile_path)
        profile["publication_profile"] = "WEEKLY_MAGAZINE"
        core.write_json(fix.profile_path, profile)
        before = _snap_state_targets(state_file, freeze, manifest)
        self.assertIn("invalid before Freeze", attempt())
        assert_unchanged(before)
        # Restore profile, break lifecycle instead.
        fix.cleanup()
        fix = SpecialFixture(ROOT, "SP001", "surveys/special/SP001")
        _special_advance_to_rc(fix, at)
        _special_approve(fix, at)
        state_file = _state_path(fix)
        pub = fix.src / "publication" / "v2"
        freeze, manifest = pub / "freeze-record-v2.json", pub / "release-manifest-v2.json"
        state = core.load_json(state_file)
        state["lifecycle_state"] = "VALIDATED_DRAFT"
        core.write_json(state_file, state)
        before = _snap_state_targets(state_file, freeze, manifest)
        self.assertIn("RELEASE_CANDIDATE", attempt())
        assert_unchanged(before)
        # Divergent pre-existing Manifest.
        fix.cleanup()
        fix = SpecialFixture(ROOT, "SP001", "surveys/special/SP001")
        _special_advance_to_rc(fix, at)
        _special_approve(fix, at)
        pub = fix.src / "publication" / "v2"
        freeze, manifest = pub / "freeze-record-v2.json", pub / "release-manifest-v2.json"
        core.write_json(manifest, {"schema_version": "2.0-rc1", "foreign": True})
        before = _snap_state_targets(state_file, freeze, manifest)
        self.assertIn("refusing to overwrite divergent Release manifest", attempt())
        self.assertEqual(state_file.read_bytes(), before[0])
        self.assertFalse(freeze.exists())
        self.assertEqual(core.load_json(manifest), {"schema_version": "2.0-rc1", "foreign": True})

    def test_w4b_wrapper_mixed_candidate_fails_closed(self) -> None:
        t = _PublicationLevel(self)
        p1 = t.case._candidate()
        c1 = p1["candidate"]
        approval1 = p1["publication_dir"] / "publication-preview-approval-v2.json"
        publication.build_preview_approval(
            t.root, c1, approval1, "human-reviewer", t.now, "review:SP001:preview")
        c2 = _build_second_chain(t)["candidate2"]
        freeze = p1["publication_dir"] / "freeze-mixed-v2.json"
        manifest = p1["publication_dir"] / "release-manifest-mixed-v2.json"
        # Shared preparation gate (used by both builders) rejects the mix.
        with self.assertRaisesRegex(ValueError, "does not bind the exact Publication Candidate"):
            publication._prepare_freeze_inputs(t.root, c2, approval1)
        self.assertFalse(freeze.exists())
        self.assertFalse(manifest.exists())

    def test_w1c_legacy_record_ignored_by_repaired_builders(self) -> None:
        at = T0 + timedelta(days=47)
        fix = SpecialFixture(ROOT, "SP001", "surveys/special/SP001",
                             visual_filename="visual-review-canonical-v2.json")
        self.addCleanup(fix.cleanup)
        candidate = _special_advance_to_rc(fix, at)
        _special_approve(fix, at)
        pub = fix.src / "publication" / "v2"
        approval = fix.src / fix.cfg["state_authority"]["publication_preview_approval_path"]
        legacy = pub / "visual-review-v2.json"
        publication.build_visual_review(
            ROOT, approval,
            [{"check_id": "VISUAL_CONFIRM", "status": "PASS", "detail": "repaired ignores legacy"}],
            "legacy-tool", at + timedelta(hours=2, minutes=30), legacy)
        legacy_bytes = legacy.read_bytes()
        w_freeze, w_manifest = profiled.build_profiled_freeze(
            ROOT, fix.cfg, _state_path(fix), at + timedelta(hours=3))
        w_bytes = (w_freeze.read_bytes(), w_manifest.read_bytes())
        self.assertEqual(core.load_json(w_manifest)["release_identity"], "special/SP001")
        w_freeze.unlink()
        w_manifest.unlink()
        c_freeze, c_manifest = publication.build_freeze(
            ROOT, candidate, approval, at + timedelta(hours=3),
            pub / "freeze-record-v2.json", pub / "release-manifest-v2.json")
        self.assertEqual((c_freeze.read_bytes(), c_manifest.read_bytes()), w_bytes)
        # The legacy record played no role and is untouched.
        self.assertEqual(legacy.read_bytes(), legacy_bytes)
        frozen = core.load_json(c_freeze)
        self.assertEqual(frozen["visual_review_path"],
                         "sources/SP001/publication/v2/visual-review-canonical-v2.json")

    def test_w2b_weekly_builders_agree_byte_equal(self) -> None:
        at = T0 + timedelta(days=48)
        fix = WeeklyCanonicalFixture(ROOT)
        self.addCleanup(fix.cleanup)
        candidate = _weekly_advance_to_rc(fix, at)
        _weekly_approve(fix, at)
        cfg = _cfg()
        approval = fix.src / cfg["state_authority"]["publication_preview_approval_path"]
        pub = fix.src / "publication" / "v2"
        w_freeze, w_manifest = profiled.build_profiled_freeze(
            ROOT, cfg, fix.src / "production-state.json", at + timedelta(hours=3))
        w_bytes = (w_freeze.read_bytes(), w_manifest.read_bytes())
        self.assertIn(b"weekly/2026-W35", w_bytes[1])
        w_freeze.unlink()
        w_manifest.unlink()
        c_freeze, c_manifest = publication.build_freeze(
            ROOT, candidate, approval, at + timedelta(hours=3),
            pub / "freeze-record-v2.json", pub / "release-manifest-v2.json")
        self.assertEqual((c_freeze.read_bytes(), c_manifest.read_bytes()), w_bytes)

    def test_w4c_wrapper_mixed_candidate_real_call(self) -> None:
        at = T0 + timedelta(days=49)
        fix = SpecialFixture(ROOT, "SP001", "surveys/special/SP001")
        self.addCleanup(fix.cleanup)
        _special_advance_to_rc(fix, at)
        _special_approve(fix, at)
        pub = fix.src / "publication" / "v2"
        fixed = pub / "publication-candidate-v2.json"
        c1_bytes = fixed.read_bytes()
        (pub / "publication-candidate-C1-record-v2.json").write_bytes(c1_bytes)
        c2 = _build_special_second_chain(fix)["candidate2"]
        c2_bytes = c2.read_bytes()
        self.assertNotEqual(core.sha256_bytes(c1_bytes), core.sha256_bytes(c2_bytes))
        self.assertEqual(
            publication.validate_candidate(ROOT, fixed)["pdf"]["sha256"],
            publication.validate_candidate(ROOT, c2)["pdf"]["sha256"])
        fixed.unlink()
        fixed.write_bytes(c2_bytes)
        state_file = _state_path(fix)
        freeze, manifest = pub / "freeze-record-v2.json", pub / "release-manifest-v2.json"
        before = _snap_state_targets(state_file, freeze, manifest)
        with self.assertRaisesRegex(ValueError, "invalid before Freeze"):
            profiled.build_profiled_freeze(ROOT, fix.cfg, state_file, at + timedelta(hours=3))
        # Honest earlier State-provenance refusal: the swapped Candidate is a
        # checkpoint-bound artifact, so valid State cannot survive the swap.
        # Nothing written; State, recorded C1, installed C2 and approval intact.
        self.assertEqual(state_file.read_bytes(), before[0])
        self.assertFalse(freeze.exists())
        self.assertFalse(manifest.exists())
        self.assertEqual(fixed.read_bytes(), c2_bytes)
        self.assertEqual((pub / "publication-candidate-C1-record-v2.json").read_bytes(), c1_bytes)

    def test_w7_wrapper_reformatted_freeze_preserved(self) -> None:
        at = T0 + timedelta(days=53)
        fix = SpecialFixture(ROOT, "SP001", "surveys/special/SP001")
        self.addCleanup(fix.cleanup)
        _special_advance_to_rc(fix, at)
        _special_approve(fix, at)
        pub = fix.src / "publication" / "v2"
        freeze, manifest = pub / "freeze-record-v2.json", pub / "release-manifest-v2.json"
        profiled.build_profiled_freeze(ROOT, fix.cfg, _state_path(fix), at + timedelta(hours=3))
        reformatted = (json.dumps(json.loads(freeze.read_bytes()),
                                  indent=4, ensure_ascii=False) + "\n").encode("utf-8")
        self.assertNotEqual(reformatted, freeze.read_bytes())
        freeze.write_bytes(reformatted)
        manifest.unlink()
        f2, m2 = profiled.build_profiled_freeze(
            ROOT, fix.cfg, _state_path(fix), at + timedelta(hours=3))
        self.assertEqual(f2.read_bytes(), reformatted)
        self.assertEqual(core.load_json(m2)["freeze_record_sha256"], core.sha256_bytes(reformatted))
        self.assertEqual(core.load_json(m2)["release_identity"], "special/SP001")

    def test_w5_pending_preview_cannot_freeze(self) -> None:
        fix = WeeklyCanonicalFixture(ROOT)
        self.addCleanup(fix.cleanup)
        at = T0 + timedelta(days=45)
        _weekly_advance_to_rc(fix, at)
        # Inert approval file without the State decision: State gate refuses.
        pub = fix.src / "publication" / "v2"
        candidate = pub / "publication-candidate-v2.json"
        publication.build_preview_approval(
            ROOT, candidate, pub / "inert-approval-v2.json",
            "synthetic-human-fixture", at + timedelta(hours=2), "synthetic:inert")
        with self.assertRaisesRegex(ValueError, "approved Publication Preview"):
            profiled.build_profiled_freeze(
                ROOT, _cfg(), fix.src / "production-state.json", at + timedelta(hours=3))
        self.assertFalse((pub / "freeze-record-v2.json").exists())
        self.assertFalse((pub / "release-manifest-v2.json").exists())

    def test_w6_wrapper_manifest_failure_retains_freeze(self) -> None:
        at = T0 + timedelta(days=46)
        fix = SpecialFixture(ROOT, "SP001", "surveys/special/SP001")
        self.addCleanup(fix.cleanup)
        _special_advance_to_rc(fix, at)
        _special_approve(fix, at)
        pub = fix.src / "publication" / "v2"
        freeze, manifest = pub / "freeze-record-v2.json", pub / "release-manifest-v2.json"
        real_open = os.open

        def fail_manifest(path, *args, **kwargs):
            if str(path).endswith("release-manifest-v2.json"):
                raise OSError("injected manifest install failure")
            return real_open(path, *args, **kwargs)

        with mock.patch.object(os, "open", side_effect=fail_manifest):
            with self.assertRaisesRegex(ValueError, "completed Freeze record retained"):
                profiled.build_profiled_freeze(
                    ROOT, fix.cfg, _state_path(fix), at + timedelta(hours=3))
        self.assertTrue(freeze.is_file())
        self.assertFalse(manifest.exists())
        freeze_bytes = freeze.read_bytes()
        f2, m2 = profiled.build_profiled_freeze(
            ROOT, fix.cfg, _state_path(fix), at + timedelta(hours=3))
        self.assertEqual(f2.read_bytes(), freeze_bytes)
        publication.validate_release_manifest(ROOT, m2)


class DM001019FreezeConsumerTests(unittest.TestCase):
    """Genuine FROZEN admission and saved release-workflow predicate."""

    def _freeze_artifacts(self, fix: SpecialFixture) -> dict[str, Path]:
        candidate = publication.validate_candidate(
            ROOT, fix.src / "publication" / "v2" / "publication-candidate-v2.json",
            issue_id=fix.issue)
        return {
            "visual-review-record": ROOT / candidate["visual_review"]["path"],
            "freeze-record": fix.src / "publication" / "v2" / "freeze-record-v2.json",
            "release-manifest": fix.src / "publication" / "v2" / "release-manifest-v2.json",
        }

    def test_s1_special_frozen_admission(self) -> None:
        at = T0 + timedelta(days=50)
        fix = SpecialFixture(ROOT, "SP001", "surveys/special/SP001")
        self.addCleanup(fix.cleanup)
        _special_advance_to_rc(fix, at)
        _special_approve(fix, at)
        profiled.build_profiled_freeze(ROOT, fix.cfg, _state_path(fix), at + timedelta(hours=3))
        report = _special_advance_to_frozen(fix, self._freeze_artifacts(fix), at, "s1")
        self.assertEqual(core.load_json(report)["status"], "PASS")

    def test_s1b_weekly_frozen_admission(self) -> None:
        fix = WeeklyCanonicalFixture(ROOT)
        self.addCleanup(fix.cleanup)
        at = T0 + timedelta(days=51)
        _weekly_advance_to_rc(fix, at)
        _weekly_approve(fix, at)
        profiled.build_profiled_freeze(
            ROOT, _cfg(), fix.src / "production-state.json", at + timedelta(hours=3))
        candidate = publication.validate_candidate(
            ROOT, fix.src / "publication" / "v2" / "publication-candidate-v2.json",
            issue_id=WEEKLY_ISSUE)
        artifacts = {
            "visual-review-record": ROOT / candidate["visual_review"]["path"],
            "freeze-record": fix.src / "publication" / "v2" / "freeze-record-v2.json",
            "release-manifest": fix.src / "publication" / "v2" / "release-manifest-v2.json",
        }
        report = _weekly_advance_to_frozen(fix, artifacts, at, "s1b")
        self.assertEqual(core.load_json(report)["status"], "PASS")

    def test_s2_workflow_predicate_accepts_all_pairs(self) -> None:
        at = T0 + timedelta(days=52)
        weekly = WeeklyCanonicalFixture(ROOT)
        self.addCleanup(weekly.cleanup)
        _weekly_advance_to_rc(weekly, at)
        _weekly_approve(weekly, at)
        profiled.build_profiled_freeze(
            ROOT, _cfg(), weekly.src / "production-state.json", at + timedelta(hours=3))
        _weekly_advance_to_frozen(weekly, {
            "visual-review-record": ROOT / publication.validate_candidate(
                ROOT, weekly.src / "publication" / "v2" / "publication-candidate-v2.json",
                issue_id=WEEKLY_ISSUE)["visual_review"]["path"],
            "freeze-record": weekly.src / "publication" / "v2" / "freeze-record-v2.json",
            "release-manifest": weekly.src / "publication" / "v2" / "release-manifest-v2.json",
        }, at, "s2w")
        outdir = Path(tempfile.mkdtemp(prefix="dm001019-wf-"))
        self.addCleanup(shutil.rmtree, outdir, True)
        code, out, err = _run_workflow_predicate(
            ROOT, WEEKLY_ISSUE,
            core.sha256_file(weekly.src / "production-state.json"),
            core.sha256_file(weekly.src / "publication" / "v2" / "release-manifest-v2.json"),
            outdir)
        self.assertEqual(code, 0, f"weekly predicate failed: {out[-500:]} {err[-500:]}")
        self.assertIn("tag=weekly/2026-W35", out)
        for issue, survey_rel, tag in (
                ("SP001", "surveys/special/SP001", "special/SP001"),
                ("SP002", "surveys/special/SP002-DIVERGED", "special/SP002-DIVERGED")):
            fix = SpecialFixture(ROOT, issue, survey_rel)
            self.addCleanup(fix.cleanup)
            _special_advance_to_rc(fix, at)
            _special_approve(fix, at)
            profiled.build_profiled_freeze(ROOT, fix.cfg, _state_path(fix), at + timedelta(hours=3))
            _special_advance_to_frozen(fix, self._freeze_artifacts(fix), at, f"s2-{issue}")
            code, out, err = _run_workflow_predicate(
                ROOT, issue, core.sha256_file(_state_path(fix)),
                core.sha256_file(fix.src / "publication" / "v2" / "release-manifest-v2.json"),
                outdir / issue)
            self.assertEqual(code, 0, f"{issue} predicate failed: {out[-500:]} {err[-500:]}")
            self.assertIn(f"tag={tag}", out)


if __name__ == "__main__":
    unittest.main()
