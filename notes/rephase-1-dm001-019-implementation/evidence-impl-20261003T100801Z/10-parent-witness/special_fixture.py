"""Scratch scaffold: valid Special LONGFORM_SPECIAL State fixture, canonical layout.

Mirrors proven b40 builders (publication-test Special chain + revalidation
Fixture state/checkpoint/surface-gate construction), parameterized by issue
and survey_root so divergent public slugs are built BEFORE downstream
hash-binding. No mocks: real validators, real stage/checkpoint/advance,
real approve_publication_preview. Runs with cwd=repo root.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from scripts import survey_agent_control_v2 as agent
from scripts import survey_production_v2 as core
from scripts import survey_publication_v2 as publication
from scripts import survey_quality_v2 as quality
from scripts import survey_reader_publication_v2 as reader
from scripts import survey_stage_validation_v2 as stage_validation

T0 = datetime(2026, 9, 12, 12, 0, 0, tzinfo=timezone.utc)
EXECUTOR = "dm001019-special-fixture"

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


def candidate_path(fix: SpecialFixture) -> Path:
    return fix.src / "publication" / "v2" / "publication-candidate-v2.json"


def state_path(fix: SpecialFixture) -> Path:
    return fix.src / "production-state.json"


def advance_to_rc(fix: SpecialFixture, at: datetime,
                  visual_name: str | None = None) -> Path:
    pub = fix.src / "publication" / "v2"
    if visual_name is None:
        visual_name = fix.visual_filename
    candidate = pub / "publication-candidate-v2.json"
    publication.build_candidate(
        fix.repo, fix.issue, fix.publication_profile,
        pub / "reader-manuscript-v2.json",
        fix.survey / "main.tex", fix.survey / "main.pdf", 12,
        pub / "quality-regression-bundle-v2.json",
        pub / "semantic-editorial-review-v2.json",
        pub / visual_name, candidate,
    )
    report = fix.src / "execution/validated-draft-stage-report.json"
    stage_validation.validate_stage(
        fix.repo, fix.cfg, state_path(fix), {"publication-candidate": candidate},
        report, at + timedelta(hours=1),
    )
    reviews = fix.src / "execution/validated-draft-reviews.json"
    core.write_json(reviews, {"reviews": [{
        "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
        "executor": "dm001019-special-fixture",
        "evidence": "synthetic connected stage validation",
        "result_path": str(report.relative_to(fix.repo))}]})
    checkpoint = agent.build_stage_checkpoint(
        fix.repo, fix.cfg, state_path(fix), {"publication-candidate": candidate},
        reviews, "SpecialFixture Publication Candidate boundary", at + timedelta(hours=1, minutes=1))
    updated = agent.advance_with_checkpoint(fix.repo, fix.cfg, state_path(fix), checkpoint)
    assert updated["lifecycle_state"] == "RELEASE_CANDIDATE", updated
    assert updated["terminal_reason"] == "HUMAN_GATE_REACHED", updated
    return candidate


def approve(fix: SpecialFixture, at: datetime) -> dict:
    return agent.approve_publication_preview(
        fix.repo, fix.cfg, state_path(fix),
        "synthetic-human-fixture", at + timedelta(hours=2), "synthetic:publication-preview")


def advance_to_frozen(fix: SpecialFixture, artifacts: dict[str, Path], at: datetime,
                      suffix: str = "positive") -> Path:
    from scripts import survey_stage_validation_v2 as stage_mod

    output = fix.src / f"execution/freeze-stage-report-{suffix}.json"
    report = stage_mod.validate_stage(
        fix.repo, fix.cfg, state_path(fix), artifacts, output, at + timedelta(hours=4))
    reviews = fix.src / f"execution/freeze-reviews-{suffix}.json"
    core.write_json(reviews, {"reviews": [{
        "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
        "executor": "dm001019-special-fixture",
        "evidence": "synthetic exact-authority Freeze validation",
        "result_path": str(report.relative_to(fix.repo))}]})
    checkpoint = agent.build_stage_checkpoint(
        fix.repo, fix.cfg, state_path(fix), artifacts, reviews,
        "SpecialFixture exact-authority Freeze boundary", at + timedelta(hours=4, minutes=1))
    updated = agent.advance_with_checkpoint(fix.repo, fix.cfg, state_path(fix), checkpoint)
    assert updated["lifecycle_state"] == "FROZEN", updated
    assert agent.validate_agent_state(fix.repo, fix.cfg, updated) == []
    return report


def extract_workflow_predicate(repo: Path) -> str:
    """Fail-closed extraction of the authority/predicate Python block."""
    text = (repo / ".github/workflows/survey-production-v2-release.yml").read_text(encoding="utf-8")
    step = "Resolve exact frozen release authority"
    assert text.count(step) == 1, "workflow step anchor not unique"
    seg = text.split(step, 1)[1]
    start_marker = "PYTHONPATH=. python - <<'PY' >> \"$GITHUB_OUTPUT\""
    assert seg.count(start_marker) == 1, "python heredoc start not unique"
    body = seg.split(start_marker, 1)[1]
    end_marker = "\n          PY\n"
    # Heredoc end markers repeat across steps; the step's block ends at the
    # FIRST end marker after its unique start (heredocs cannot nest).
    assert end_marker in body, "python heredoc end missing"
    block = body.split(end_marker, 1)[0]
    import textwrap as _tw

    # Raw file lines carry the YAML block indent (stripped by YAML before bash
    # in production); dedent to the executed form for local runs.
    block = _tw.dedent(block).lstrip("\n")
    assert block.lstrip().startswith("import os, pathlib, re"), "unexpected block head"
    assert "Release Manifest public identity mismatch" in block, "identity predicate missing"
    return block.lstrip("\n")


def run_workflow_predicate(repo: Path, issue: str, state_sha: str, manifest_sha: str,
                           outdir: Path) -> tuple[int, str, str]:
    """Execute the extracted block with cwd=repo; synthetic fixture only."""
    block = extract_workflow_predicate(repo)
    outdir.mkdir(parents=True, exist_ok=True)
    gh_out = outdir / "github_output.txt"
    gh_out.write_text("", encoding="utf-8")
    env = {
        "PATH": "/usr/bin:/bin",
        "PYTHONPATH": str(repo),
        "PYTHONDONTWRITEBYTECODE": "1",
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
