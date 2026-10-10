"""Focused LF-1 tests: source-only LONGFORM_GENERATED_V1 reader-input derivation.

All research/editorial/visual/Human records here are synthetic TYPE/IDENTITY
test inputs built through the real current producers and stage validators;
they never assert genuine semantic sufficiency. Fixture Git databases are
independent temp dirs; the candidate source and reconstruct databases are
never written. The derivation under test writes nothing itself.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import survey_agent_control_v2 as agent
from scripts import survey_architecture_v2 as architecture
from scripts import survey_completeness_v2 as completeness
from scripts import survey_discovery_v2 as discovery
from scripts import survey_drafting_v2 as drafting
from scripts import survey_evidence_v2 as evidence
from scripts import survey_longform_derivation_v2 as longform
from scripts import survey_production_v2 as core
from scripts import survey_review_attention_v2 as review_attention
from scripts import survey_stage_validation_v2 as stage_validation
from scripts import survey_x_intake_v2 as xintake
from tests import test_survey_architecture_v2 as architecture_tests
from tests import test_survey_drafting_v2 as drafting_tests
from tests import test_survey_evidence_v2 as evidence_tests


ISSUE = "SP001"
DID1 = "fixture-paper-D001"
DID2 = "second-paper-D002"

_GIT_VARS = (
    "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR",
)


def _reversed_keys(value):
    if isinstance(value, dict):
        return {key: _reversed_keys(value[key]) for key in reversed(list(value.keys()))}
    if isinstance(value, list):
        return [_reversed_keys(item) for item in value]
    return value


def _snapshot(root: Path) -> dict:
    # Scoped no-write oracle: owned fixture tree excluding .git object store
    # (excluded .git file walk is scoped here; Git state is observed via
    # plumbing HEAD/status/diff instead). Records regular-file bytes,
    # directory identity, symlink targets, plus Git refs/status.
    files: dict[str, str] = {}
    dirs: list[str] = []
    symlinks: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if ".git" in path.parts:
            continue
        rel = str(path.relative_to(root))
        if path.is_symlink():
            try:
                symlinks[rel] = os.readlink(path)
            except OSError:
                symlinks[rel] = "<unreadable-symlink>"
        elif path.is_dir():
            dirs.append(rel)
        elif path.is_file():
            files[rel] = core.sha256_file(path)
    git: dict[str, str] = {}
    for args, key in (
        (["git", "rev-parse", "HEAD"], "head"),
        (["git", "status", "--porcelain=v1", "--untracked-files=all"], "status"),
        (["git", "diff", "--name-only", "HEAD"], "diff"),
    ):
        proc = subprocess.run(args, cwd=root, capture_output=True, text=True)
        git[key] = proc.stdout
        git[key + ":exit"] = str(proc.returncode)
    return {"files": files, "dirs": sorted(dirs), "symlinks": symlinks, "git": git}


def _inventory(root: Path) -> dict[str, str]:
    # Legacy file-only view retained for compatibility; new oracle is _snapshot.
    return _snapshot(root)["files"]


class LongformDerivationV2Tests(unittest.TestCase):
    def setUp(self) -> None:
        for name in _GIT_VARS:
            if os.environ.get(name):
                raise AssertionError(f"unsafe inherited Git root override for isolated fixture: {name}")
        self.workspace = Path(__file__).resolve().parents[1]
        scratch = tempfile.TemporaryDirectory(prefix="jgas-lf1-")
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name).resolve()
        tracked = subprocess.run(
            ["git", "ls-files", "-z", "--", "config", "schemas", "scripts", "templates", "prompts", "docs", "data"],
            cwd=self.workspace, capture_output=True, check=True,
        ).stdout
        for raw in tracked.split(b"\0"):
            if not raw:
                continue
            relative = Path(raw.decode("utf-8"))
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(self.workspace / relative, destination)
        for rel in ("scripts/survey_longform_derivation_v2.py", "schemas/longform-reader-input-v2.schema.json"):
            destination = self.root / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(self.workspace / rel, destination)
        # Process-scoped synthetic identity only: no persistent git config user.*
        # Identity travels via -c overrides + author/committer env for this repo.
        fixture_env = {
            **os.environ,
            "GIT_AUTHOR_NAME": "Synthetic LF-1 Fixture",
            "GIT_AUTHOR_EMAIL": "synthetic-lf1@example.invalid",
            "GIT_COMMITTER_NAME": "Synthetic LF-1 Fixture",
            "GIT_COMMITTER_EMAIL": "synthetic-lf1@example.invalid",
        }
        for command in (
            ["git", "init", "-q"],
            ["git", "remote", "add", "origin", "https://example.invalid/lf1-fixture.git"],
            ["git", "add", "-A"],
            ["git", "-c", "user.name=Synthetic LF-1 Fixture",
             "-c", "user.email=synthetic-lf1@example.invalid",
             "commit", "-q", "-m", "Synthetic isolated LF-1 source basis"],
        ):
            subprocess.run(command, cwd=self.root, check=True, capture_output=True, env=fixture_env)
        # Prove no persistent user.* was written into this fixture DB (local only;
        # global user.name/email from the operator environment is out of scope).
        listed = subprocess.run(
            ["git", "config", "--local", "--list"], cwd=self.root, capture_output=True, text=True, check=True,
        ).stdout
        self.assertNotIn("user.name=", listed)
        self.assertNotIn("user.email=", listed)
        self.cfg = core.load_json(self.root / core.DEFAULT_CONFIG)
        self.head = core.repository_commit_sha(self.root)

    # ---- fixture construction through real producers/validators ----

    def _evidence_helper(self):
        helper = evidence_tests.SurveyEvidenceV2Tests(
            methodName="test_evidence_package_is_exact_and_preserves_task_bytes"
        )
        helper.repo_root = self.workspace
        return helper

    def _chain(self, dids=(DID1,), card_hook=None, card_status="VERIFIED", npackages=1,
               views_materiality="MATERIAL"):
        helper = self._evidence_helper()
        root, cfg, head = self.root, self.cfg, self.head
        with mock.patch.object(evidence_tests, "IMPLEMENTATION_SHA", head), \
                mock.patch.object(architecture_tests, "IMPLEMENTATION_SHA", head), \
                mock.patch.object(drafting_tests, "IMPLEMENTATION_SHA", head):
            profile_path, state_path = helper.init_profile(root, cfg, "THEMATIC")
            issue = core.load_json(state_path)["issue_id"]
            self.assertEqual(issue, ISSUE)
            records = [helper.discovery(issue, did) for did in dids]
            decisions = {did: "KEEP" for did in dids}
            discovery_path, screening = helper.make_screening(root, state_path, records, decisions)
            return self._chain_screened(
                helper, root, cfg, head, profile_path, state_path, issue,
                discovery_path, screening, dids, card_hook, card_status, npackages, views_materiality,
            )

    def _chain_screened(self, helper, root, cfg, head, profile_path, state_path, issue,
                        discovery_path, screening, dids, card_hook=None, card_status="VERIFIED",
                        npackages=1, views_materiality="MATERIAL"):
        with mock.patch.object(evidence_tests, "IMPLEMENTATION_SHA", head), \
                mock.patch.object(architecture_tests, "IMPLEMENTATION_SHA", head), \
                mock.patch.object(drafting_tests, "IMPLEMENTATION_SHA", head):
            package_path = evidence.prepare_evidence_package(
                root, state_path, discovery_path, screening,
                root / "sources" / issue / "evidence" / "v2" / "package", head,
            )
            package = core.load_json(package_path)
            results_dir = package_path.parent / "results"
            results_dir.mkdir(parents=True)
            for meta in package["tasks"]:
                card = helper.card_for_task(root, package_path, meta, status=card_status)
                if card_hook is not None:
                    card = card_hook(meta, card)
                core.write_json(results_dir / Path(meta["path"]).name, card)
            evidence_acceptance = evidence.accept_evidence_results(
                root, package_path, results_dir, root / "sources" / issue / "evidence" / "v2" / "runs", head,
            )
            # Drafting production consumes the content-addressed canonical accepted
            # Evidence tree, not only the earlier per-run acceptance. Preserve the
            # exact accepted bytes while matching that production authority shape.
            canonical_accepted = (
                root / "sources" / issue / "evidence" / "v2" / "accepted"
                / core.load_json(evidence_acceptance)["result_set_sha256"]
            )
            canonical_accepted.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(evidence_acceptance.parent, canonical_accepted)
            views = helper.make_views(root, profile_path, evidence_acceptance, materiality=views_materiality)
            ledger = evidence.build_materiality_ledger(
                root, profile_path, discovery_path, screening, evidence_acceptance, views, head,
            )
            ledger_path = root / "sources" / issue / "materiality-ledger.json"
            evidence.write_materiality_ledger(ledger_path, ledger)
            profile = core.load_json(profile_path)
            acceptance = core.load_json(evidence_acceptance)
            task_ids = [row["evidence_task_id"] for row in acceptance["results"]]
            obligations = [
                {
                    "obligation_id": initial["obligation_id"],
                    "dimension": initial["dimension"],
                    "description": initial["description"],
                    "status": "SATISFIED",
                    "discovery_ids": list(dids),
                    "evidence_task_ids": list(task_ids),
                    "rationale": "fixture evidence satisfies the Profile initial obligation",
                }
                for initial in profile["research_scope"]["initial_obligations"]
            ]
            completeness_result = {
                "schema_version": "2.0-rc1",
                "issue_id": issue,
                "research_profile": "THEMATIC",
                "basis": {
                    "production_profile_sha256": core.sha256_file(profile_path),
                    "materiality_ledger_sha256": core.sha256_file(ledger_path),
                },
                "overall_status": "READY",
                "obligations": obligations,
                "residual_limitations": [],
                "closure": {
                    "expansion_passes": 1,
                    "final_pass_new_sources": 0,
                    "final_pass_new_material_obligations": 0,
                    "final_pass_new_material_obligations_open": 0,
                    "targeted_gap_fill_completed": True,
                    "open_material_obligations": 0,
                    "limitations": [],
                    "status": "COMPLETE",
                },
            }
            self.assertEqual(completeness.validate_profile_completeness(
                completeness_result, root, profile_path, discovery_path, screening,
                evidence_acceptance, views, ledger_path, head,
            ), [])
            completeness_path = root / "sources" / issue / "profile-completeness.json"
            core.write_json(completeness_path, completeness_result)
            matrix = architecture.derive_candidate_matrix(
                root, profile_path, discovery_path, screening, evidence_acceptance,
                views, ledger_path, completeness_path, head,
            )
            matrix_path = root / "sources" / issue / "candidate-matrix-v2.json"
            architecture.write_candidate_matrix(matrix_path, matrix)
            rows = matrix["rows"]
            if npackages == 1:
                chosen = [rows[0]]
            else:
                self.assertGreaterEqual(len(rows), 2)
                chosen = rows[:2]
            assignments = [
                {
                    "candidate_id": row["candidate_id"],
                    "disposition": "SELECTED",
                    "rationale": "explicit editorial disposition for fixture",
                    "architecture_usage": "PRIMARY",
                    "publication_role": "LONGFORM_SPECIAL:FIXTURE_ROLE",
                    "architecture_role": "THEMATIC:FIXTURE_ROLE",
                    "profile_extensions": {},
                }
                for row in chosen
            ]
            selection = {
                "schema_version": "2.0-rc1",
                "issue_id": issue,
                "research_profile": "THEMATIC",
                "publication_profile": "LONGFORM_SPECIAL",
                "selection_version": "v0.1",
                "status": "ESTABLISHED",
                "basis": {
                    "production_profile_sha256": core.sha256_file(profile_path),
                    "candidate_matrix_sha256": core.sha256_file(matrix_path),
                    "profile_completeness_sha256": core.sha256_file(completeness_path),
                    "materiality_ledger_sha256": core.sha256_file(ledger_path),
                },
                "assignments": assignments,
                "summary": {
                    "candidate_count": len(assignments),
                    "disposition_counts": {"SELECTED": len(assignments)},
                    "selected_count": len(assignments),
                },
            }
            selection_path = root / "selection-v2.json"
            core.write_json(selection_path, selection)
            packages = [
                {
                    "package_id": f"pkg-00{order}",
                    "title": f"Fixture package {order}",
                    "purpose": "Carry the selected primary candidate into drafting.",
                    "primary_candidate_ids": [row["candidate_id"]],
                    "supporting_candidate_ids": [],
                    "must_cover_requirements": ["subject identity"],
                    "boundaries": list(row["remaining_boundaries"]),
                    "drafting_order": order,
                    "profile_extensions": {"lineage_package_role": "CORE"},
                    "publication_extensions": {"longform_chapter_kind": "lineage"},
                }
                for order, row in enumerate(chosen, start=1)
            ]
            plan = {
                "schema_version": "2.0-rc1",
                "issue_id": issue,
                "research_profile": "THEMATIC",
                "publication_profile": "LONGFORM_SPECIAL",
                "status": "PROPOSED",
                "basis": {
                    "production_profile_sha256": core.sha256_file(profile_path),
                    "profile_completeness_sha256": core.sha256_file(completeness_path),
                    "materiality_ledger_sha256": core.sha256_file(ledger_path),
                    "candidate_matrix_sha256": core.sha256_file(matrix_path),
                    "candidate_selection_sha256": core.sha256_file(selection_path),
                },
                "editorial_thesis": "A bounded editorial thesis derived from selected evidence.",
                "architecture_goals": ["preserve evidence boundaries", "make compression auditable"],
                "page_plan": {"target_pages": 12, "max_pages": 24, "notes": "fixture-only planning"},
                "packages": packages,
                "selected_exceptions": [],
                "profile_extensions": {},
                "publication_extensions": {},
                "human_review": {"reviewed_by": None, "reviewed_at": None, "review_reference": None},
            }
            architecture_path = root / "architecture-v2.json"
            core.write_json(architecture_path, plan)
            summary = architecture.build_architecture_review_summary(
                root, profile_path, discovery_path, screening, evidence_acceptance, views,
                ledger_path, completeness_path, matrix_path, selection_path, architecture_path, head,
            )
            self.assertEqual(summary["readiness"]["status"], "READY_FOR_ARCHITECTURE_REVIEW")
            summary_path = root / "architecture-review-summary-v2.json"
            core.write_json(summary_path, summary)
            attention_path = root / "architecture-review-attention-v2.json"
            review_attention.build_attention(root, screening, ledger_path, selection_path, attention_path)
            approval = {
                "schema_version": "2.0-rc1",
                "approval_id": f"approval:{issue}:architecture",
                "issue_id": issue,
                "gate": "ARCHITECTURE_REVIEW",
                "decision": "APPROVED",
                "architecture_sha256": core.sha256_file(architecture_path),
                "architecture_review_summary_sha256": core.sha256_file(summary_path),
                "architecture_review_attention_sha256": core.sha256_file(attention_path),
                "reviewed_by": "human-reviewer",
                "reviewed_at": "2026-08-22T03:00:00+09:00",
                "review_reference": "human-gate-fixture",
            }
            approval_path = root / "architecture-approval-v2.json"
            core.write_json(approval_path, approval)
            worker = drafting_tests.SurveyDraftingV2Tests(
                methodName="test_weekly_and_thematic_share_generic_draft_contract_without_dummy_fields"
            )
            draft_paths: dict[str, tuple[Path, Path]] = {}
            for package_row in packages:
                pid = package_row["package_id"]
                derived = drafting.derive_draft_package(
                    root, profile_path, discovery_path, screening, evidence_acceptance, views,
                    ledger_path, completeness_path, matrix_path, selection_path,
                    architecture_path, summary_path, approval_path, pid, head,
                )
                package_file = root / f"draft-package-{pid}.json"
                core.write_json(package_file, derived)
                result = worker.valid_result(derived, package_file, root / drafting.DRAFT_PROMPT)
                result["profile_extensions"] = copy.deepcopy(derived["profile_extensions"])
                result["publication_extensions"] = copy.deepcopy(derived["publication_extensions"])
                result_file = root / f"draft-result-{pid}.json"
                core.write_json(result_file, result)
                self.assertEqual(drafting.validate_draft_result(result, package_file, root / drafting.DRAFT_PROMPT), [])
                draft_paths[pid] = (package_file, result_file)
        source_root = root / "sources" / issue
        return {
            "root": root, "profile_path": profile_path, "discovery_path": discovery_path,
            "screening": screening, "evidence": evidence_acceptance, "views": views,
            "ledger_path": ledger_path, "completeness_path": completeness_path,
            "matrix_path": matrix_path, "matrix": matrix, "selection_path": selection_path,
            "architecture_path": architecture_path, "review_summary_path": summary_path,
            "review_attention_path": attention_path, "approval_path": approval_path,
            "draft_paths": draft_paths, "source_root": source_root,
            "survey_root": root / "surveys" / "special" / issue,
            "packages": packages, "dids": list(dids),
        }

    def _did_for_package(self, chain: dict, pid: str) -> list[str]:
        row = next(item for item in chain["matrix"]["rows"] if item["candidate_id"] in next(
            plan["primary_candidate_ids"] for plan in chain["packages"] if plan["package_id"] == pid
        ))
        return list(row["discovery_ids"])

    def _complete_authorities(self, chain: dict) -> dict:
        root = chain["root"]
        source_root = chain["source_root"]
        for pid, (package_file, result_file) in chain["draft_paths"].items():
            package = core.load_json(package_file)
            target = source_root / "draft/v2/packages" / pid / "draft-package.json"
            target.parent.mkdir(parents=True, exist_ok=True)
            core.write_json(target, package)
            result = core.load_json(result_file)
            core.write_json(target.parent / "draft-result.json", result)
        pairs = [
            (source_root / "draft/v2/packages" / pid / "draft-package.json",
             source_root / "draft/v2/packages" / pid / "draft-result.json")
            for pid in chain["draft_paths"]
        ]
        synthesis_input = drafting.build_synthesis_input(
            root, chain["profile_path"], chain["architecture_path"],
            chain["review_summary_path"], chain["approval_path"], pairs,
        )
        synthesis_input_path = source_root / "draft/v2/profile-synthesis-input.json"
        core.write_json(synthesis_input_path, synthesis_input)
        profile_payload = {key: f"fixture {key}" for key in synthesis_input["profile_payload_requirements"]}
        synthesis_result = {
            "schema_version": "2.0-rc1",
            "issue_id": ISSUE,
            "research_profile": "THEMATIC",
            "publication_profile": "LONGFORM_SPECIAL",
            "synthesis_version": "v0.1",
            "status": "ESTABLISHED",
            "basis": {
                "synthesis_input_sha256": core.sha256_file(synthesis_input_path),
                "prompt_id": "profile-synthesis-v2",
                "prompt_sha256": core.sha256_file(root / drafting.SYNTHESIS_PROMPT),
            },
            "runner": {
                "provider": "fixture", "model": "fixture-model", "invocation": "unit-test",
                "generated_at": "2026-08-22T03:10:00+09:00", "run_reference": None,
            },
            "profile_payload": profile_payload,
            "publication_payload": {},
        }
        synthesis_result_path = source_root / "draft/v2/profile-synthesis-result.json"
        core.write_json(synthesis_result_path, synthesis_result)
        self.assertEqual(drafting.validate_synthesis_result(
            synthesis_result, synthesis_input_path, root / drafting.SYNTHESIS_PROMPT), [])
        archive_rows = []
        for pid in chain["draft_paths"]:
            result = core.load_json(source_root / "draft/v2/packages" / pid / "draft-result.json")
            dids = self._did_for_package(chain, pid)
            archive_rows.append({
                "package_id": pid, "headline": result["headline"], "deck": result["deck"],
                "deck_discovery_ids": list(dids), "deck_ref_mode": "CLAIMS",
                "blocks": [{
                    "block_id": result["blocks"][0]["block_id"], "text": result["blocks"][0]["text"],
                    "discovery_ids": list(dids), "ref_mode": "CLAIMS",
                }],
            })
        archive_path = source_root / "draft/v2/interactive-drafting-synthesis-input.json"
        core.write_json(archive_path, {"packages": archive_rows})
        authored_path = source_root / "semantic-publication-input.json"
        core.write_json(authored_path, self._authored(chain))
        raw_source = root / "raw/source.json"
        raw_source.parent.mkdir(parents=True, exist_ok=True)
        raw_source.write_text('{"fixture": true}\n', encoding="utf-8")
        x_manifest = xintake.build_manifest(root, self.cfg, chain["profile_path"], {
            "decision": "REQUIRED", "rationale": "A bounded X fixture observes intake.",
            "series_context": None, "runs": [{
                "run_id": "lf1-x-fixture", "purpose": "Observe material technical signal.",
                "research_questions": ["Did material X signal emerge?"],
                "coverage_focus": ["technical signal"], "time_scope": "fixture edition",
                "expected_result_filename": "grok-x-result.md",
            }],
        })
        x_raw = source_root / "external/x/lf1-x-fixture/raw/grok-x-result.md"
        x_raw.parent.mkdir(parents=True, exist_ok=True)
        x_raw.write_text("No material technical X signal.\n", encoding="utf-8")
        xintake.record_result(
            root, self.cfg, x_manifest, "lf1-x-fixture", x_raw, "grok-x-result.md",
            "2026-08-22T03:30:00Z", "2026-08-22T03:35:00Z",
            "NO_MATERIAL_SIGNAL", "NO_MATERIAL_DISCOVERY", [],
            "No material discovery in the fixture X pass.",
        )
        discovery_accepted = discovery.build_acceptance(
            root, chain["discovery_path"], x_manifest, ISSUE,
            source_root / "discovery/discovery-accepted-v2.json",
        )
        chain.update({
            "synthesis_input_path": synthesis_input_path, "synthesis_result_path": synthesis_result_path,
            "archive_path": archive_path, "authored_path": authored_path,
            "discovery_accepted": discovery_accepted,
        })
        return chain

    def _revision_row(self, pid: str, dids: list[str]) -> dict:
        paragraphs = lambda tag: [
            {"text": f"Fixture {tag} paragraph one for {pid}.", "discovery_ids": list(dids)},
            {"text": f"Fixture {tag} paragraph two for {pid}.", "discovery_ids": list(dids)},
        ]
        return {
            "package_id": pid,
            "theme_at_a_glance": [
                {"label": "Focus", "text": f"Fixture glance one for {pid}.", "discovery_ids": list(dids)},
                {"label": "Signal", "text": f"Fixture glance two for {pid}.", "discovery_ids": list(dids)},
            ],
            "narrative_sections": [
                {"heading": f"Fixture narrative one for {pid}", "paragraphs": paragraphs("narrative-one")},
                {"heading": f"Fixture narrative two for {pid}", "paragraphs": paragraphs("narrative-two")},
            ],
            "timeline": [
                {"label": "Early", "text": f"Fixture timeline early for {pid}.", "discovery_ids": list(dids)},
                {"label": "Late", "text": f"Fixture timeline late for {pid}.", "discovery_ids": list(dids)},
            ],
            "synthesis": {"heading": f"Fixture synthesis for {pid}", "paragraphs": paragraphs("synthesis")},
            "reader_claim_boundary": [
                {"text": f"Fixture boundary for {pid}.", "discovery_ids": list(dids)},
            ],
            "technical_notes": [{
                "title": f"Fixture note for {pid}",
                "discovery_id": dids[0],
                "chronology": f"Fixture chronology for {pid}.",
                "technical_points": [
                    f"Fixture point one for {pid}.", f"Fixture point two for {pid}.",
                ],
                "limitation": f"Fixture limitation for {pid}.",
                "primary_url": f"https://example.invalid/{dids[0]}",
            }],
        }

    def _authored(self, chain: dict, review_reference: str = "fixture longform review") -> dict:
        rows = [self._revision_row(pid, self._did_for_package(chain, pid)) for pid in chain["draft_paths"]]
        dids = [did for pid in chain["draft_paths"] for did in self._did_for_package(chain, pid)]
        return {
            "schema_version": "2.0-rc1",
            "issue_id": ISSUE,
            "runner": "LONGFORM_SPECIAL",
            "cover": {"headline": "Fixture lineage cover", "deck": "Source-based lineage survey",
                      "anchors": ["Target Model"]},
            "frontmatter": {"heading": "Fixture frontmatter", "lede": "A bounded lineage survey.",
                            "scope_notes": ["One accepted primary source per package."]},
            "final_summary": {"heading": "この号の総括", "paragraphs": [
                "The edition surveys accepted lineage sources.",
                "The claims remain attributed to their origins.",
                "The synthesis stays inside authorized evidence.",
            ]},
            "longform_revision": {
                "review_reference": review_reference,
                "new_external_evidence": False,
                "packages": rows,
                "cross_family_synthesis": {
                    "heading": "Fixture cross-family synthesis",
                    "paragraphs": [
                        {"text": "Fixture cross paragraph one.", "discovery_ids": list(dids)},
                        {"text": "Fixture cross paragraph two.", "discovery_ids": list(dids)},
                    ],
                    "comparison_rows": [
                        {"dimension": f"Fixture aspect {number}", "glm": "Fixture GLM.",
                         "qwen": "Fixture Qwen.", "deepseek": "Fixture DeepSeek.",
                         "kimi": "Fixture Kimi.", "discovery_ids": list(dids)}
                        for number in (1, 2, 3)
                    ],
                },
            },
        }

    def _advance(self, chain: dict, stage: str, artifacts: dict[str, Path], minute: int) -> None:
        state_path = chain["source_root"] / "production-state.json"
        self.assertEqual(core.load_json(state_path)["lifecycle_state"], stage)
        stamp = core.parse_instant(f"2026-08-22T{4 + minute // 60:02d}:{minute % 60:02d}:00+09:00")
        report = chain["source_root"] / "orchestration/v2/reviews" / f"{stage}-core-contract.json"
        stage_validation.validate_stage(self.root, self.cfg, state_path, artifacts, report, stamp)
        review_path = report.with_name(f"{stage}-reviews.json")
        core.write_json(review_path, {"reviews": [{
            "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
            "executor": "synthetic LF-1 fixture using actual stage validator",
            "evidence": "actual stage validator PASS for exact synthetic edition authorities",
            "result_path": str(review_path.parent.joinpath(report.name).relative_to(self.root)),
        }]})
        checkpoint = agent.build_stage_checkpoint(
            self.root, self.cfg, state_path, artifacts, review_path,
            f"Synthetic LF-1 {stage} fixture stage was validated.", stamp,
        )
        updated = agent.advance_with_checkpoint(self.root, self.cfg, state_path, checkpoint)
        self.assertEqual(agent.validate_agent_state(self.root, self.cfg, updated), [])

    def _current_state(self, chain: dict, stop_after: str | None = None) -> Path:
        for source, target in (
            (chain["architecture_path"], chain["source_root"] / "architecture-v2.json"),
            (chain["review_summary_path"], chain["source_root"] / "architecture-review-summary-v2.json"),
            (chain["review_attention_path"], chain["source_root"] / "architecture-review-attention-v2.json"),
        ):
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        stages = [
            ("ISSUE_INITIALIZED", {"discovery-acceptance": chain["discovery_accepted"]}),
            ("DISCOVERY_COLLECTED", {"screening-acceptance": chain["screening"]}),
            ("CANDIDATES_NORMALIZED", {
                "evidence-acceptance": chain["evidence"], "edition-views-acceptance": chain["views"],
                "materiality-ledger": chain["ledger_path"], "profile-completeness": chain["completeness_path"],
            }),
            ("EVIDENCE_REVIEWED", {
                "candidate-matrix": chain["matrix_path"], "candidate-selection": chain["selection_path"],
            }),
            ("SELECTION_COMPLETE", {
                "issue-architecture": chain["source_root"] / "architecture-v2.json",
                "architecture-review-summary": chain["source_root"] / "architecture-review-summary-v2.json",
                "architecture-review-attention": chain["source_root"] / "architecture-review-attention-v2.json",
            }),
            ("ARCHITECTURE_ESTABLISHED", {
                **{f"draft-package:{pid}": chain["source_root"] / "draft/v2/packages" / pid / "draft-package.json"
                   for pid in chain["draft_paths"]},
                **{f"draft-result:{pid}": chain["source_root"] / "draft/v2/packages" / pid / "draft-result.json"
                   for pid in chain["draft_paths"]},
                "synthesis-input": chain["synthesis_input_path"],
                "synthesis-result": chain["synthesis_result_path"],
            }),
        ]
        for number, (stage, artifacts) in enumerate(stages):
            if stop_after == stage:
                break
            self._advance(chain, stage, artifacts, number + 1)
            if stage == "SELECTION_COMPLETE":
                agent.approve_architecture(
                    self.root, self.cfg, chain["source_root"] / "production-state.json",
                    "synthetic human reviewer", core.parse_instant("2026-08-22T04:06:30+09:00"),
                    "synthetic LF-1 fixture architecture review",
                )
                chain["approval_path"] = chain["source_root"] / "gates/architecture-approval.json"
                for pid in chain["draft_paths"]:
                    package_path = chain["source_root"] / "draft/v2/packages" / pid / "draft-package.json"
                    package = core.load_json(package_path)
                    package["basis"]["architecture_approval_sha256"] = core.sha256_file(chain["approval_path"])
                    core.write_json(package_path, package)
                    result_path = package_path.parent / "draft-result.json"
                    result = drafting_tests.SurveyDraftingV2Tests.valid_result(
                        package, package_path, self.root / drafting.DRAFT_PROMPT
                    )
                    result["profile_extensions"] = copy.deepcopy(package["profile_extensions"])
                    result["publication_extensions"] = copy.deepcopy(package["publication_extensions"])
                    core.write_json(result_path, result)
                    self.assertEqual(drafting.validate_draft_result(
                        result, package_path, self.root / drafting.DRAFT_PROMPT), [])
                synthesis_input = drafting.build_synthesis_input(
                    self.root, chain["profile_path"], chain["source_root"] / "architecture-v2.json",
                    chain["source_root"] / "architecture-review-summary-v2.json",
                    chain["approval_path"], [
                        (chain["source_root"] / "draft/v2/packages" / other / "draft-package.json",
                         chain["source_root"] / "draft/v2/packages" / other / "draft-result.json")
                        for other in chain["draft_paths"]
                    ],
                )
                core.write_json(chain["synthesis_input_path"], synthesis_input)
                synthesis_result = core.load_json(chain["synthesis_result_path"])
                synthesis_result["basis"]["synthesis_input_sha256"] = core.sha256_file(chain["synthesis_input_path"])
                core.write_json(chain["synthesis_result_path"], synthesis_result)
        return chain["source_root"] / "production-state.json"

    def _derive(self, chain: dict, authored_path: Path | None = None) -> dict:
        state_path = chain["source_root"] / "production-state.json"
        return longform.load_derivation(self.root, state_path, authored_path or chain["authored_path"])

    def _derive_checked(self, chain: dict, authored_path: Path | None = None, scope: str = "") -> dict:
        # Scoped full no-write oracle: mutation must already be on disk before
        # before-snapshot; compare immediately around derivation before repair.
        before = _snapshot(self.root)
        try:
            context = self._derive(chain, authored_path)
        finally:
            after = _snapshot(self.root)
            self.assertEqual(after, before, f"derivation wrote fixture tree ({scope})")
        return context

    def _derive_checked_refuses(self, chain: dict, authored_path: Path | None = None, scope: str = "") -> ValueError:
        before = _snapshot(self.root)
        try:
            with self.assertRaises(ValueError) as caught:
                self._derive(chain, authored_path)
        finally:
            after = _snapshot(self.root)
            self.assertEqual(after, before, f"refusing derivation wrote fixture tree ({scope})")
        return caught.exception  # type: ignore[return-value]

    def _write_variant(self, chain: dict, name: str, mutate) -> Path:
        authored = self._authored(chain)
        mutate(authored)
        path = chain["source_root"] / f"{name}.json"
        core.write_json(path, authored)
        return path

    def _pure_context(self, chain: dict) -> dict:
        # Reusable accepted chain for table-driven pure reprojection: derive once
        # via real loaders, then mutate in-memory inputs through the pure
        # projector without rebuilding the chain per field.
        state_path = chain["source_root"] / "production-state.json"
        context = longform.load_derivation(self.root, state_path, chain["authored_path"])
        return context

    # ---- positive proof: every emitted category ----

    def test_valid_single_did_projects_every_category(self) -> None:
        chain = self._complete_authorities(self._chain())
        state_path = self._current_state(chain)
        self.assertEqual(core.load_json(state_path)["lifecycle_state"], "DRAFT_COMPLETE")
        self.assertEqual(core.load_json(state_path)["next_action"], "stage:reader-publication-validation")
        context = self._derive_checked(chain, scope="valid-single-did-positive")
        surface = context["surface"]
        self.assertEqual(surface["route"], "LONGFORM_GENERATED_V1")
        self.assertEqual(surface["format"], "THEMATIC_FOUR_FAMILY_LINEAGE_V1")
        self.assertEqual(surface["issue_metadata"]["title"], "Japanese Generative AI Technical Survey Special")
        self.assertEqual(surface["visible_text"]["toc_title"], "目次")
        self.assertEqual(surface["visible_text"]["edition_descriptor"], "Thematic Longform Special")
        self.assertEqual(surface["visible_text"]["cross_table_header"], ["観点", "GLM", "Qwen", "DeepSeek", "Kimi"])
        self.assertEqual(surface["visible_text"]["note_chronology_label"], "Chronology:")
        self.assertEqual(surface["visible_text"]["note_points_label"], "Technical points:")
        self.assertEqual(surface["visible_text"]["note_limitation_label"], "Limitation / attribution:")
        self.assertEqual(surface["visible_text"]["note_url_label"], "Primary URL:")
        self.assertEqual(surface["final_summary"]["heading"], "この号の総括")
        self.assertEqual(surface["final_summary"]["placement"], "END_OF_PUBLICATION_BEFORE_REFERENCES_OR_END_MATTER")
        self.assertEqual(len(surface["final_summary"]["paragraphs"]), 3)
        package = surface["packages"][0]
        self.assertEqual(package["package_id"], "pkg-001")
        self.assertEqual(package["kicker"], "THEMATIC LINEAGE 1/1 — 001")
        self.assertEqual(len(package["theme_at_a_glance"]), 2)
        self.assertEqual(len(package["narrative_sections"]), 2)
        self.assertEqual(len(package["timeline"]), 2)
        self.assertEqual(len(package["technical_notes"]), 1)
        self.assertEqual(len(surface["cross_family_synthesis"]["comparison_rows"]), 3)
        entry = surface["bibliography"][0]
        self.assertEqual(entry["discovery_id"], DID1)
        self.assertEqual(entry["title"], "Target Model")
        self.assertEqual(entry["author"], "Example")
        self.assertEqual(entry["url"], f"https://example.invalid/{DID1}")
        self.assertEqual(entry["urldate"], "2026-08-22")
        self.assertTrue(entry["key"].startswith("sp001"))
        raw = longform.canonical_reader_bytes(surface)
        self.assertEqual(raw, core.json_bytes(surface))
        self.assertEqual(hashlib.sha256(raw).hexdigest(), hashlib.sha256(core.json_bytes(surface)).hexdigest())
        self.assertNotIn("run_semantic_publication_v2_interactive", sys.modules)
        names = [row["name"] for row in context["accepted_refs"]]
        self.assertTrue(any(name.startswith("evidence-card:") for name in names), names)

    def test_reordered_authoring_dictionaries_normalize_identically(self) -> None:
        chain = self._complete_authorities(self._chain())
        state_path = self._current_state(chain)
        first = self._derive(chain)["surface"]
        reordered_path = chain["source_root"] / "semantic-publication-input-reordered.json"
        core.write_json(reordered_path, _reversed_keys(self._authored(chain)))
        second = longform.load_derivation(self.root, state_path, reordered_path)["surface"]
        self.assertEqual(longform.canonical_reader_bytes(first), longform.canonical_reader_bytes(second))

    def test_two_package_chain_orders_bibliography(self) -> None:
        chain = self._complete_authorities(self._chain(dids=(DID1, DID2), npackages=2))
        state_path = self._current_state(chain)
        surface = self._derive(chain)["surface"]
        self.assertEqual([row["package_id"] for row in surface["packages"]], ["pkg-001", "pkg-002"])
        self.assertEqual(surface["packages"][0]["kicker"], "THEMATIC LINEAGE 1/2 — 001")
        self.assertEqual(surface["packages"][1]["kicker"], "THEMATIC LINEAGE 2/2 — 002")
        self.assertEqual(
            [row["discovery_id"] for row in surface["bibliography"]], [DID1, DID2]
        )

    def test_unknown_organization_falls_back(self) -> None:
        def hook(meta, card):
            card["entities"][0]["organization"] = None
            return card
        chain = self._complete_authorities(self._chain(card_hook=hook))
        state_path = self._current_state(chain)
        surface = self._derive(chain)["surface"]
        self.assertEqual(surface["bibliography"][0]["author"], "Unknown")
        self.assertEqual(surface["bibliography"][0]["title"], "Target Model")

    # ---- refusal proof: real inputs, rederived ----

    def test_unknown_discovery_id_refuses(self) -> None:
        chain = self._complete_authorities(self._chain())
        self._current_state(chain)
        def mutate(authored):
            authored["longform_revision"]["packages"][0]["theme_at_a_glance"][0]["discovery_ids"] = ["ghost-thing-D999"]
        path = self._write_variant(chain, "authored-unknown-did", mutate)
        with self.assertRaisesRegex(ValueError, "outside the approved package"):
            self._derive(chain, path)

    def test_duplicate_technical_note_refuses(self) -> None:
        chain = self._complete_authorities(self._chain())
        self._current_state(chain)
        def mutate(authored):
            row = authored["longform_revision"]["packages"][0]
            row["technical_notes"].append(copy.deepcopy(row["technical_notes"][0]))
        path = self._write_variant(chain, "authored-dup-note", mutate)
        with self.assertRaisesRegex(ValueError, "repeat a Discovery ID"):
            self._derive(chain, path)

    def test_primary_url_mismatch_refuses(self) -> None:
        chain = self._complete_authorities(self._chain())
        self._current_state(chain)
        def mutate(authored):
            authored["longform_revision"]["packages"][0]["technical_notes"][0]["primary_url"] = "https://example.invalid/other"
        path = self._write_variant(chain, "authored-url-mismatch", mutate)
        with self.assertRaisesRegex(ValueError, "primary_url differs"):
            self._derive(chain, path)

    def test_needs_more_evidence_never_reaches_projection(self) -> None:
        # Upstream readiness evidence ONLY, not a direct loader negative and not
        # a projector negative: held-back evidence blocks at real Architecture
        # readiness before any projection input exists. Projector-level refusal
        # of held-back cites is proved separately via pure build with
        # held-back records (see test_held_back_cite_refuses_at_projection).
        with self.assertRaisesRegex(AssertionError, "BLOCKED"):
            self._chain(card_status="NEEDS_MORE", views_materiality="HOLD")

    def test_held_back_cite_refuses_at_projection(self) -> None:
        # PROJECTOR-level pure-build evidence (in-memory mutated records from a
        # real loader context), explicitly NOT a direct loader negative: the
        # loader never sees held-back records because selected-only eligibility
        # skips them. The NEEDS_MORE upstream test below is upstream-readiness
        # evidence only, likewise not a loader negative.
        chain = self._complete_authorities(self._chain())
        self._current_state(chain)
        context = self._pure_context(chain)
        held = copy.deepcopy(context["records"])
        did = next(iter(held))
        held[did] = {**held[did], "status": "NEEDS_MORE", "materiality": "HOLD"}
        with self.assertRaisesRegex(ValueError, "held-back"):
            longform.build_longform_reader_input(
                ISSUE, context["profile"], core.load_json(chain["architecture_path"]),
                core.load_json(chain["authored_path"]), core.load_json(chain["synthesis_result_path"]),
                # Re-derive ordered via real loader context is already validated;
                # reuse in-memory ordered by re-resolving through load_derivation internals:
                # simplest is to call build with original ordered captured via fresh derive.
                self._ordered_for(chain, context), held,
            )

    def _ordered_for(self, chain: dict, context: dict) -> list[dict]:
        # Reconstruct ordered from the last successful derivation by re-running
        # the loader's ordered assembly without rebuilding producers: use the
        # acceptedRefs to reload packages? Instead, re-derive purely: call
        # load_derivation again and capture ordered via monkey-patch.
        captured: dict[str, Any] = {}
        original = longform.build_longform_reader_input

        def spy(*args: Any, **kwargs: Any) -> Any:
            captured["ordered"] = args[5]
            return original(*args, **kwargs)

        with mock.patch.object(longform, "build_longform_reader_input", spy):
            longform.load_derivation(
                self.root, chain["source_root"] / "production-state.json", chain["authored_path"]
            )
        return captured["ordered"]

    def test_tampered_card_hash_refuses(self) -> None:
        chain = self._complete_authorities(self._chain())
        state_path = self._current_state(chain)
        acceptance = core.load_json(chain["evidence"])
        name = acceptance["results"][0]["filename"]
        card_path = Path(chain["evidence"]).parent / "results" / name
        # Mutation belongs BEFORE the before-snapshot for the no-write oracle.
        with card_path.open("a", encoding="utf-8") as handle:
            handle.write("\n")
        before = _snapshot(self.root)
        try:
            with self.assertRaisesRegex(ValueError, "SHA drift|changed"):
                longform.load_derivation(self.root, state_path, chain["authored_path"])
        finally:
            after = _snapshot(self.root)
            self.assertEqual(after, before, "refusing derivation wrote fixture tree (tamper-hash)")

    def test_access_ambiguity_refuses(self) -> None:
        def hook(meta, card):
            locator = card["sources"][0]["url"]
            card["sources"].append({
                "source_id": "source-2",
                "url": locator,
                "source_class": "PRIMARY_PAPER",
                "title": "Second capture",
                "published_at": "2025-01-01T00:00:00Z",
                "accessed_at": "2026-08-23T02:10:00+09:00",
                "role": "verification source",
            })
            return card
        chain = self._complete_authorities(self._chain(card_hook=hook))
        state_path = self._current_state(chain)
        with self.assertRaisesRegex(ValueError, "ambiguous captures"):
            longform.load_derivation(self.root, state_path, chain["authored_path"])

    def test_unsafe_canonical_url_refuses(self) -> None:
        # End-to-end: a task-bound source locator outside the finite URL subset
        # must fail closed in the loader (defense in depth behind task binding).
        helper = self._evidence_helper()
        root, cfg, head = self.root, self.cfg, self.head
        with mock.patch.object(evidence_tests, "IMPLEMENTATION_SHA", head), \
                mock.patch.object(architecture_tests, "IMPLEMENTATION_SHA", head), \
                mock.patch.object(drafting_tests, "IMPLEMENTATION_SHA", head):
            profile_path, state_path = helper.init_profile(root, cfg, "THEMATIC")
            record = helper.discovery(ISSUE, DID1)
            record["source"]["locator"] = "https://example.invalid/odd path"
            discovery_path, screening = helper.make_screening(root, state_path, [record], {DID1: "KEEP"})
            chain = self._chain_screened(
                helper, root, cfg, head, profile_path, state_path, ISSUE,
                discovery_path, screening, (DID1,),
            )
        chain = self._complete_authorities(chain)
        state_path = self._current_state(chain)
        with self.assertRaisesRegex(ValueError, "excluded delimiter|whitespace"):
            longform.load_derivation(self.root, state_path, chain["authored_path"])
        # Exact documented reject set at the policy boundary.
        self.assertEqual(longform._check_url("https://example.invalid/paper", "probe"), "https://example.invalid/paper")
        for bad in ("http://exa mple.invalid/x", "https://example.invalid/a%b", "https://example.invalid/x#frag",
                    "https://例.invalid/x", "notaurl", "https://example.invalid/{x}", "https://example.invalid/x\\y"):
            with self.assertRaises(ValueError, msg=bad):
                longform._check_url(bad, "probe")

    def test_missing_package_row_refuses(self) -> None:
        chain = self._complete_authorities(self._chain(dids=(DID1, DID2), npackages=2))
        self._current_state(chain)
        def mutate(authored):
            authored["longform_revision"]["packages"].pop()
        path = self._write_variant(chain, "authored-missing-row", mutate)
        with self.assertRaisesRegex(ValueError, "exactly one row per approved Architecture package"):
            self._derive(chain, path)

    def test_directive_file_presence_refuses(self) -> None:
        chain = self._complete_authorities(self._chain())
        state_path = self._current_state(chain)
        target = chain["source_root"] / "editorial/post-architecture-directives-v2.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps({"requirements": []}) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unsupported directive authority"):
            longform.load_derivation(self.root, state_path, chain["authored_path"])

    def test_directive_symlink_presence_refuses(self) -> None:
        chain = self._complete_authorities(self._chain())
        state_path = self._current_state(chain)
        target = chain["source_root"] / "editorial/post-architecture-directives-v2.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to("nowhere-directive.json")
        with self.assertRaisesRegex(ValueError, "unsupported directive authority"):
            longform.load_derivation(self.root, state_path, chain["authored_path"])

    def test_earlier_lifecycle_state_refuses(self) -> None:
        chain = self._complete_authorities(self._chain())
        state_path = self._current_state(chain, stop_after="ARCHITECTURE_ESTABLISHED")
        self.assertEqual(core.load_json(state_path)["lifecycle_state"], "ARCHITECTURE_ESTABLISHED")
        with self.assertRaisesRegex(ValueError, "exact DRAFT_COMPLETE"):
            longform.load_derivation(self.root, state_path, chain["authored_path"])

    def test_runner_and_review_reference_are_nonreader(self) -> None:
        # R4: runner metadata must remain nonreader. Profile defines the route;
        # authored runner/review-reference are mechanical envelope only. Any
        # non-empty runner projects identically; empty runner refuses as type
        # policy. Runner-only and review-reference-only changes retain reader
        # bytes while the authored binding hash changes.
        chain = self._complete_authorities(self._chain())
        state_path = self._current_state(chain)
        first = self._derive_checked(chain, scope="runner-baseline")
        first_bytes = longform.canonical_reader_bytes(first["surface"])
        # Runner-only change retains reader bytes.
        runner_path = self._write_variant(chain, "authored-runner-alt", lambda a: a.update({"runner": "CUSTOM_RUNNER"}))
        second = self._derive_checked(chain, runner_path, scope="runner-alt-retains-bytes")
        self.assertEqual(longform.canonical_reader_bytes(second["surface"]), first_bytes)
        self.assertNotEqual(first["authored_refs"], second["authored_refs"])
        # Empty runner refuses as envelope type policy, not authority.
        empty_path = self._write_variant(chain, "authored-runner-empty", lambda a: a.update({"runner": ""}))
        self._derive_checked_refuses(chain, empty_path, scope="runner-empty-refuses")
        # Review-reference-only change retains reader bytes (existing stability).
        reref_path = chain["source_root"] / "semantic-publication-input-reref2.json"
        core.write_json(reref_path, self._authored(chain, review_reference="a different review note"))
        third = self._derive_checked(chain, reref_path, scope="reref-retains-bytes")
        self.assertEqual(longform.canonical_reader_bytes(third["surface"]), first_bytes)
        self.assertNotEqual(first["authored_refs"], third["authored_refs"])
        # Reader schema carries no runner/provenance fields.
        self.assertNotIn("runner", second["surface"])
        self.assertNotIn("review_reference", second["surface"])
        for key in ("runner", "review_reference", "provenance", "recorded_at"):
            self.assertNotIn(key, second["surface"].get("visible_text", {}))

    def test_state_path_escape_refuses(self) -> None:
        chain = self._complete_authorities(self._chain())
        self._current_state(chain)
        with self.assertRaises(ValueError):
            longform.load_derivation(self.root, self.root / ".." / "outside.json", chain["authored_path"])

    def test_symlinked_ancestor_refuses(self) -> None:
        chain = self._complete_authorities(self._chain())
        self._current_state(chain)
        outside = tempfile.TemporaryDirectory(prefix="jgas-lf1-outside-")
        self.addCleanup(outside.cleanup)
        link = self.root / "linked-ancestor"
        link.symlink_to(Path(outside.name))
        with self.assertRaises(ValueError):
            longform.load_derivation(self.root, link / "state.json", chain["authored_path"])

    # ---- stability: mechanical-only change keeps reader bytes ----

    def test_mechanical_only_change_keeps_reader_bytes(self) -> None:
        chain = self._complete_authorities(self._chain())
        state_path = self._current_state(chain)
        first = self._derive_checked(chain, scope="mechanical-baseline")
        second_path = chain["source_root"] / "semantic-publication-input-reref.json"
        core.write_json(second_path, self._authored(chain, review_reference="a different review note"))
        # Mutation was written before the before-snapshot inside _derive_checked.
        second = self._derive_checked(chain, second_path, scope="mechanical-reref")
        self.assertEqual(
            longform.canonical_reader_bytes(first["surface"]),
            longform.canonical_reader_bytes(second["surface"]),
        )
        self.assertNotEqual(
            first["authored_refs"], second["authored_refs"],
            "mechanical authored binding must differ while reader bytes stay identical",
        )

    def test_no_writer_artifacts_or_gate_created(self) -> None:
        chain = self._complete_authorities(self._chain())
        self._current_state(chain)
        # Scoped oracle: compare full snapshots, not absent filenames. Pre-existing
        # source files (e.g. templates in the fixture copy) are preserved; the
        # derivation must not add main/bib/sty/gate/manifest under edition roots.
        before = _snapshot(self.root)
        self._derive(chain)
        after = _snapshot(self.root)
        self.assertEqual(after, before, "derivation wrote fixture tree (no-writer)")
        for name in ("main.tex", "references.bib", "jgaisurvey.sty", "reader-surface-gate-v2.json",
                     "validated-source-manifest.json"):
            found = [path for base in (chain["source_root"], chain["survey_root"]) for path in base.rglob(name)]
            # Edition roots must not gain writer artifacts beyond the before-set.
            before_names = {k for k in before["files"] if k.endswith("/" + name) or k == name}
            after_names = {k for k in after["files"] if k.endswith("/" + name) or k == name}
            self.assertEqual(after_names, before_names, f"derivation materialized {name}")


    def test_pure_policy_boundaries_without_chain(self) -> None:
        # No fixture chain: exact policy unit proof for scanner/URL/primary/
        # constants/token/path boundaries. Real-loader end-to-end for scanner
        # is covered by the table test's scanner row.
        # Scanner obligation: phrase blocked by read-only scanner but absent
        # from the preserved local forbidden list must still refuse.
        with self.assertRaisesRegex(ValueError, "leaks production metadata"):
            longform._reader_text("The approved architecture guides the survey.", "probe")
        # Preserved local checks still refuse (scanner blocks first with the same
        # fail-closed prefix; patterns match the scanner's leaking span).
        for bad, pattern in [
            ("Core v2 Evidence: leak", "production metadata"),
            ("Please Verify this", "leaks production metadata"),
            ("See fixture-paper-D001 here", "leaks production metadata"),
            ("\\input{evil}", "TeX inclusion"),
        ]:
            with self.assertRaisesRegex(ValueError, pattern, msg=bad):
                longform._reader_text(bad, "probe")
        self.assertEqual(longform._reader_text("A bounded lineage survey.", "probe"), "A bounded lineage survey.")
        # Exact untrimmed URL: surrounding whitespace refuses, never normalizes.
        with self.assertRaisesRegex(ValueError, "surrounding whitespace"):
            longform._check_url(" https://example.invalid/x", "probe")
        with self.assertRaisesRegex(ValueError, "surrounding whitespace"):
            longform._check_url("https://example.invalid/x ", "probe")
        # Exact reject set at the policy boundary (untrimmed, no transform).
        self.assertEqual(
            longform._check_url("https://example.invalid/paper", "probe"),
            "https://example.invalid/paper",
        )
        for bad in (
            "http://exa mple.invalid/x",
            "https://example.invalid/a%b",
            "https://example.invalid/x#frag",
            "https://\u4f8b.invalid/x",
            "notaurl",
            "https://example.invalid/{x}",
            "https://example.invalid/x\\y",
            "https://example.invalid/x|y",
            "https://example.invalid/x`y",
        ):
            with self.assertRaises(ValueError, msg=bad):
                longform._check_url(bad, "probe")
        # Primary entity: exact URL validated before trim; missing/ambiguous refuse.
        card_ok = {
            "entities": [{
                "entity_id": "target",
                "canonical_name": "Target Model",
                "organization": "Example",
                "canonical_url": "https://example.invalid/fixture-paper-D001",
            }],
            "artifact": {"primary_subject_id": "target"},
        }
        resolved = longform._resolve_primary_entity(card_ok, "fixture-paper-D001")
        self.assertEqual(resolved["url"], "https://example.invalid/fixture-paper-D001")
        card_space = {
            "entities": [{
                "entity_id": "target",
                "canonical_name": "Target Model",
                "organization": "Example",
                "canonical_url": " https://example.invalid/x ",
            }],
            "artifact": {"primary_subject_id": "target"},
        }
        with self.assertRaisesRegex(ValueError, "surrounding whitespace"):
            longform._resolve_primary_entity(card_space, "fixture-paper-D001")
        with self.assertRaisesRegex(ValueError, "carries no entities"):
            longform._resolve_primary_entity({"entities": [], "artifact": {"primary_subject_id": "target"}}, DID1)
        with self.assertRaisesRegex(ValueError, "lacks an artifact authority"):
            longform._resolve_primary_entity({"entities": [{"entity_id": "target"}]}, DID1)
        dup_card = {
            "entities": [
                {"entity_id": "target", "canonical_name": "A", "organization": "E", "canonical_url": "https://example.invalid/a"},
                {"entity_id": "target", "canonical_name": "B", "organization": "E", "canonical_url": "https://example.invalid/b"},
            ],
            "artifact": {"primary_subject_id": "target"},
        }
        with self.assertRaisesRegex(ValueError, "no unique primary-subject"):
            longform._resolve_primary_entity(dup_card, DID1)
        # Trusted-constants isolation is proved with a REAL returned surface in
        # test_returned_surface_mutation_leaves_trusted_constants (loader plus a
        # second projection); a constant-only deepcopy here would be tautological.
        self.assertEqual(longform.VISIBLE_TEXT["cross_table_header"], ["\u89b3\u70b9", "GLM", "Qwen", "DeepSeek", "Kimi"])
        # Citation-key grammar aligned with DID subset (dots preserved).
        self.assertEqual(longform._bib_key("fixture-paper-D001"), "sp001fixturepaperd001")
        self.assertEqual(longform._bib_key("paper.v1-D001"), "sp001paper.v1d001")
        with self.assertRaisesRegex(ValueError, "supported Discovery ID"):
            longform._did("bad id!", "probe")
        with self.assertRaisesRegex(ValueError, "supported token subset"):
            longform._kicker("bad id!", 1, 1)
        # Pre-read path safety: card filename traversal refuses before any read.
        fake_accept = self.root / "sources" / "SP001" / "evidence" / "v2" / "accepted" / "dummy" / "acceptance.json"
        for bad_name in ("../evil.json", "a/b.json", "", "..", "/abs.json", "a\\b.json"):
            with self.assertRaisesRegex(ValueError, "card filename|escapes", msg=str(bad_name)):
                longform._safe_card_path(self.root, fake_accept, bad_name, "probe")
        # validate_* path overload applies contained-read contract.
        with self.assertRaises(ValueError):
            longform.validate_longform_reader_input(self.root, self.root / ".." / "outside.json")

    def test_table_every_category_mutation_reuses_single_chain(self) -> None:
        # R3: one accepted chain, table-driven authoring mutations for each
        # emitted category. Each row rederives via real loaders (no chain
        # rebuild); mutation file is written BEFORE the before-snapshot.
        chain = self._complete_authorities(self._chain())
        self._current_state(chain)
        baseline = self._derive_checked(chain, scope="table-baseline")
        baseline_bytes = longform.canonical_reader_bytes(baseline["surface"])

        def variant(mutate) -> Path:
            authored = self._authored(chain)
            mutate(authored)
            path = chain["source_root"] / f"authored-table-{variant.counter}.json"
            variant.counter += 1
            core.write_json(path, authored)
            return path
        variant.counter = 0  # type: ignore[attr-defined]

        # (name, mutate, expectation): "changes" means reader bytes must differ;
        # ("refuses", pattern) means load must fail closed with pattern.
        rows: list[tuple[str, Any, Any]] = [
            ("cover-headline", lambda a: a["cover"].update({"headline": "Altered lineage cover"}), "changes"),
            ("cover-deck", lambda a: a["cover"].update({"deck": "Altered deck text"}), "changes"),
            ("frontmatter-lede", lambda a: a["frontmatter"].update({"lede": "Altered bounded lede"}), "changes"),
            ("final-summary-para", lambda a: a["final_summary"]["paragraphs"].__setitem__(0, "Altered edition summary one."), "changes"),
            ("glance-text", lambda a: a["longform_revision"]["packages"][0]["theme_at_a_glance"][0].update({"text": "Altered glance text."}), "changes"),
            ("narrative-heading", lambda a: a["longform_revision"]["packages"][0]["narrative_sections"][0].update({"heading": "Altered narrative heading"}), "changes"),
            ("timeline-label", lambda a: a["longform_revision"]["packages"][0]["timeline"][0].update({"label": "Altered"}), "changes"),
            ("synthesis-heading", lambda a: a["longform_revision"]["packages"][0]["synthesis"].update({"heading": "Altered synthesis heading"}), "changes"),
            ("boundary-text", lambda a: a["longform_revision"]["packages"][0]["reader_claim_boundary"].__setitem__(0, {"text": "Altered boundary.", "discovery_ids": [DID1]}), "changes"),
            ("note-chronology", lambda a: a["longform_revision"]["packages"][0]["technical_notes"][0].update({"chronology": "Altered chronology."}), "changes"),
            ("note-point", lambda a: a["longform_revision"]["packages"][0]["technical_points"] if False else a["longform_revision"]["packages"][0]["technical_notes"][0]["technical_points"].__setitem__(0, "Altered point one."), "changes"),
            ("note-limitation", lambda a: a["longform_revision"]["packages"][0]["technical_notes"][0].update({"limitation": "Altered limitation."}), "changes"),
            ("cross-heading", lambda a: a["longform_revision"]["cross_family_synthesis"].update({"heading": "Altered cross heading"}), "changes"),
            ("cross-dimension", lambda a: a["longform_revision"]["cross_family_synthesis"]["comparison_rows"][0].update({"dimension": "Altered aspect"}), "changes"),
            ("cross-glm", lambda a: a["longform_revision"]["cross_family_synthesis"]["comparison_rows"][0].update({"glm": "Altered GLM."}), "changes"),
            ("cover-anchors", lambda a: a["cover"]["anchors"].__setitem__(0, "Altered Anchor"), "changes"),
            ("frontmatter-heading", lambda a: a["frontmatter"].update({"heading": "Altered frontmatter heading"}), "changes"),
            ("frontmatter-scope-note", lambda a: a["frontmatter"]["scope_notes"].__setitem__(0, "Altered scope note."), "changes"),
            ("narrative-paragraph", lambda a: a["longform_revision"]["packages"][0]["narrative_sections"][0]["paragraphs"][0].update({"text": "Altered narrative paragraph."}), "changes"),
            ("timeline-text", lambda a: a["longform_revision"]["packages"][0]["timeline"][0].update({"text": "Altered timeline text."}), "changes"),
            ("package-synthesis-paragraph", lambda a: a["longform_revision"]["packages"][0]["synthesis"]["paragraphs"][0].update({"text": "Altered package synthesis paragraph."}), "changes"),
            ("note-title", lambda a: a["longform_revision"]["packages"][0]["technical_notes"][0].update({"title": "Altered note title"}), "changes"),
            ("cross-paragraph", lambda a: a["longform_revision"]["cross_family_synthesis"]["paragraphs"][0].update({"text": "Altered cross paragraph."}), "changes"),
            ("cross-qwen", lambda a: a["longform_revision"]["cross_family_synthesis"]["comparison_rows"][0].update({"qwen": "Altered Qwen."}), "changes"),
            ("cross-deepseek", lambda a: a["longform_revision"]["cross_family_synthesis"]["comparison_rows"][0].update({"deepseek": "Altered DeepSeek."}), "changes"),
            ("cross-kimi", lambda a: a["longform_revision"]["cross_family_synthesis"]["comparison_rows"][0].update({"kimi": "Altered Kimi."}), "changes"),
            ("glance-order", lambda a: a["longform_revision"]["packages"][0].__setitem__("theme_at_a_glance", list(reversed(a["longform_revision"]["packages"][0]["theme_at_a_glance"]))), "changes"),
            ("comparison-order", lambda a: a["longform_revision"]["cross_family_synthesis"].__setitem__("comparison_rows", list(reversed(a["longform_revision"]["cross_family_synthesis"]["comparison_rows"]))), "changes"),
            ("scanner-phrase", lambda a: a["cover"].update({"headline": "The approved architecture guides"}), ("refuses", "leaks production metadata")),
            ("forbidden-phrase", lambda a: a["cover"].update({"headline": "Core v2 Evidence: leak"}), ("refuses", "leaks production metadata")),
            ("did-leak", lambda a: a["cover"].update({"headline": f"See {DID1} here"}), ("refuses", "leaks production metadata")),
            ("missing-note", lambda a: a["longform_revision"]["packages"][0]["technical_notes"].pop(), ("refuses", "requires source-backed Technical Notes")),
            ("unknown-did", lambda a: a["longform_revision"]["packages"][0]["theme_at_a_glance"][0].update({"discovery_ids": ["ghost-thing-D999"]}), ("refuses", "outside the approved package")),
            ("bad-final-heading", lambda a: a["final_summary"].update({"heading": "Wrong"}), ("refuses", "required final issue summary heading")),
        ]
        for name, mutate, expect in rows:
            path = variant(mutate)
            before = _snapshot(self.root)
            try:
                if isinstance(expect, tuple):
                    _, pattern = expect
                    with self.assertRaisesRegex(ValueError, pattern, msg=name):
                        self._derive(chain, path)
                else:
                    surface = self._derive(chain, path)["surface"]
                    self.assertNotEqual(
                        longform.canonical_reader_bytes(surface), baseline_bytes, msg=name,
                    )
            finally:
                after = _snapshot(self.root)
                # No-write holds for both changing and refusing derivations;
                # variant file itself was written before before-snapshot.
                self.assertEqual(after, before, f"table row wrote fixture tree ({name})")

    def test_archive_exact_coverage_and_selected_only(self) -> None:
        # R2 + R6-selected-only on ONE reusable two-package chain (no rebuild per
        # field). Archive file mutations are written BEFORE the before-snapshot;
        # snapshots compare immediately around derivation before archive repair.
        chain = self._complete_authorities(self._chain(dids=(DID1, DID2), npackages=2))
        self._current_state(chain)
        healthy = self._derive_checked(chain, scope="archive-healthy-control")
        self.assertEqual([r["package_id"] for r in healthy["surface"]["packages"]], ["pkg-001", "pkg-002"])
        archive_path = chain["archive_path"]
        original_bytes = archive_path.read_bytes()

        def restore() -> None:
            archive_path.write_bytes(original_bytes)

        self.addCleanup(restore)
        cases: list[tuple[str, Any, str]] = []

        def extra_package() -> None:
            data = json.loads(original_bytes.decode("utf-8"))
            dup = copy.deepcopy(data["packages"][0])
            dup["package_id"] = "pkg-999"
            data["packages"].append(dup)
            archive_path.write_bytes(core.json_bytes(data))

        def duplicate_package() -> None:
            data = json.loads(original_bytes.decode("utf-8"))
            data["packages"].append(copy.deepcopy(data["packages"][0]))
            archive_path.write_bytes(core.json_bytes(data))

        def extra_block() -> None:
            data = json.loads(original_bytes.decode("utf-8"))
            row = data["packages"][0]
            extra = copy.deepcopy(row["blocks"][0])
            extra["block_id"] = "extra-block"
            extra["discovery_ids"] = [DID2]
            row["blocks"].append(extra)
            archive_path.write_bytes(core.json_bytes(data))

        def duplicate_block() -> None:
            data = json.loads(original_bytes.decode("utf-8"))
            row = data["packages"][0]
            row["blocks"].append(copy.deepcopy(row["blocks"][0]))
            archive_path.write_bytes(core.json_bytes(data))

        def cross_package_did() -> None:
            # Archive-only DID from the other package's authorized set: pkg-001
            # spec gains DID2 which resolves exactly once only inside pkg-002.
            data = json.loads(original_bytes.decode("utf-8"))
            row = next(r for r in data["packages"] if r["package_id"] == "pkg-001")
            row["blocks"][0]["discovery_ids"] = [DID2]
            archive_path.write_bytes(core.json_bytes(data))

        cases = [
            ("extra-archive-package", extra_package, "coverage differs"),
            ("duplicate-archive-package", duplicate_package, "duplicates package|coverage differs"),
            ("extra-archive-block", extra_block, "block coverage differs|exactly once inside package"),
            ("duplicate-archive-block", duplicate_block, "duplicates block|block coverage differs"),
            ("cross-package-archive-did", cross_package_did, "exactly once inside package|outside the approved|coverage|placement"),
        ]
        for name, mutate, pattern in cases:
            mutate()
            before = _snapshot(self.root)
            try:
                with self.assertRaisesRegex(ValueError, pattern, msg=name):
                    self._derive(chain)
            finally:
                after = _snapshot(self.root)
                self.assertEqual(after, before, f"archive negative wrote fixture tree ({name})")
                restore()
        # Healthy control again after repairs.
        self._derive_checked(chain, scope="archive-healthy-after-repair")
        # Selected-only eligibility: global integrity holds for both DIDs, but
        # records contain only the selected subset; unselected is preserved
        # without promotion (absent, never blocks).
        matrix_path = next(r["path"] for r in healthy["accepted_refs"] if r["name"] == "candidate-matrix")
        ledger_path = next(r["path"] for r in healthy["accepted_refs"] if r["name"] == "materiality-ledger")
        discovery_path = next(r["path"] for r in healthy["accepted_refs"] if r["name"] == "discovery-acceptance")
        evidence_path = next(r["path"] for r in healthy["accepted_refs"] if r["name"] == "evidence-acceptance")
        rec_one, _ = longform._longform_records(
            self.root, self.root / matrix_path, self.root / ledger_path,
            self.root / discovery_path, self.root / evidence_path, self.head, {DID1},
        )
        self.assertEqual(set(rec_one), {DID1})
        rec_both, _ = longform._longform_records(
            self.root, self.root / matrix_path, self.root / ledger_path,
            self.root / discovery_path, self.root / evidence_path, self.head, {DID1, DID2},
        )
        self.assertEqual(set(rec_both), {DID1, DID2})

    def test_citation_collision_refuses_end_to_end(self) -> None:
        # Two distinct DIDs folding to one bibliography key refuse. DIDs differ
        # only by dash/case so lower/dash folding collides.
        colliding = ("fixture-paper-D001", "fixturepaper-D001")
        self.assertEqual(longform._bib_key(colliding[0]), longform._bib_key(colliding[1]))
        chain = self._complete_authorities(self._chain(dids=colliding, npackages=2))
        self._current_state(chain)
        before = _snapshot(self.root)
        try:
            with self.assertRaisesRegex(ValueError, "citation key collision"):
                self._derive(chain)
        finally:
            after = _snapshot(self.root)
            self.assertEqual(after, before, "collision refusal wrote fixture tree")

    def test_dotted_did_full_loader_schema_positive(self) -> None:
        # B1: a dotted Discovery ID through the REAL chain → projector → schema.
        # Helper-only key tests cannot catch a schema/module grammar disagreement;
        # this loader positive proves the fixed dotted citation-key grammar agrees.
        dotted = "paper.v1-D001"
        self.assertEqual(longform._bib_key(dotted), "sp001paper.v1d001")
        chain = self._complete_authorities(self._chain(dids=(dotted,)))
        self._current_state(chain)
        context = self._derive_checked(chain, scope="dotted-did-positive")
        surface = context["surface"]
        entry = surface["bibliography"][0]
        self.assertEqual(entry["discovery_id"], dotted)
        self.assertEqual(entry["key"], "sp001paper.v1d001")
        self.assertEqual(entry["url"], f"https://example.invalid/{dotted}")
        # Schema positive on the projected dotted object (would fail before the
        # citation_key dot fix).
        longform.validate_longform_reader_input(self.root, surface)
        raw = longform.canonical_reader_bytes(surface)
        self.assertEqual(raw, core.json_bytes(surface))

    def test_results_dir_alias_refuses_before_read(self) -> None:
        # Pre-read alias gap: an accepted-tree results directory aliased to an
        # outside malformed sentinel must refuse BEFORE the accepted-Evidence
        # loader reads through it. Observation spies assert the loader never ran
        # and the sentinel was never read; they never replace authority checks.
        from scripts import survey_evidence_v2 as evidence_mod

        chain = self._complete_authorities(self._chain())
        self._current_state(chain)
        run_dir = Path(chain["evidence"]).parent
        real_results = run_dir / "results"
        outside = tempfile.TemporaryDirectory(prefix="jgas-lf1-sentinel-")
        self.addCleanup(outside.cleanup)
        sentinel = Path(outside.name) / "evil.json"
        sentinel.write_text('{"malformed": true}\n', encoding="utf-8")
        sentinel_bytes = sentinel.read_bytes()
        # Swap the real results directory for an outside alias BEFORE the
        # before-snapshot for the no-write oracle.
        staged = run_dir / "results-real"
        real_results.rename(staged)
        real_results.symlink_to(Path(outside.name))

        def restore() -> None:
            if real_results.is_symlink():
                real_results.unlink()
            if staged.exists() and not real_results.exists():
                staged.rename(real_results)

        self.addCleanup(restore)
        validator_calls: list[str] = []
        real_validator = evidence_mod.validate_evidence_acceptance

        def spy_validator(*args: Any, **kwargs: Any) -> Any:
            validator_calls.append("called")
            return real_validator(*args, **kwargs)

        read_paths: list[str] = []
        real_load = core.load_json

        def spy_load(path: Any, *args: Any, **kwargs: Any) -> Any:
            read_paths.append(str(path))
            return real_load(path, *args, **kwargs)

        before = _snapshot(self.root)
        try:
            with mock.patch.object(evidence_mod, "validate_evidence_acceptance", spy_validator), \
                    mock.patch.object(core, "load_json", spy_load):
                with self.assertRaisesRegex(ValueError, "alias/symlink"):
                    self._derive(chain)
        finally:
            after = _snapshot(self.root)
            self.assertEqual(after, before, "alias refusal wrote fixture tree")
            restore()
        # The real authority loader never ran, so no aliased content was parsed.
        self.assertEqual(validator_calls, [])
        # The outside malformed sentinel was never read and is unchanged.
        self.assertFalse(any(str(sentinel) in item or item.startswith(outside.name) for item in read_paths))
        self.assertEqual(sentinel.read_bytes(), sentinel_bytes)
        # Healthy control after repair.
        self._derive_checked(chain, scope="alias-healthy-after-repair")

    def test_equal_timestamp_first_capture_keeps_projection(self) -> None:
        # Resolver control complementing test_access_ambiguity_refuses: two
        # captures of the same URL with the SAME access timestamp follow the
        # resolver's first-capture rule and the projection succeeds.
        # Single-DID-per-card-row shape is producer-guaranteed (per-task cards),
        # so a multi-DID-row loader negative is not constructible through real
        # producers; DID uniqueness loader proof is the duplicate-card shape
        # check plus this same-authority disambiguation pair. Not counted beyond
        # what the resolver contract states.
        def hook(meta, card):
            locator = card["sources"][0]["url"]
            card["sources"].append({
                "source_id": "source-2",
                "url": locator,
                "source_class": "PRIMARY_PAPER",
                "title": "Second capture",
                "published_at": "2025-01-01T00:00:00Z",
                "accessed_at": "2026-08-22T02:10:00+09:00",
                "role": "verification source",
            })
            return card
        chain = self._complete_authorities(self._chain(card_hook=hook))
        self._current_state(chain)
        surface = self._derive_checked(chain, scope="equal-timestamp-control")["surface"]
        self.assertEqual(surface["bibliography"][0]["urldate"], "2026-08-22")

    def test_returned_surface_mutation_leaves_trusted_constants(self) -> None:
        # Isolation with REAL returned objects (not a constant-only deepcopy):
        # mutating one derived surface cannot alter a second projection or the
        # trusted module constants it was projected from.
        chain = self._complete_authorities(self._chain())
        self._current_state(chain)
        first = self._derive_checked(chain, scope="isolation-first")
        first_bytes = longform.canonical_reader_bytes(first["surface"])
        first["surface"]["visible_text"]["cross_table_header"].append("MUT")
        first["surface"]["packages"][0]["headline"] = "MUTATED HEADLINE"
        first["surface"]["bibliography"][0]["title"] = "MUTATED TITLE"
        second = self._derive_checked(chain, scope="isolation-second")
        self.assertEqual(longform.canonical_reader_bytes(second["surface"]), first_bytes)
        self.assertEqual(
            second["surface"]["visible_text"]["cross_table_header"],
            ["観点", "GLM", "Qwen", "DeepSeek", "Kimi"],
        )
        self.assertNotEqual(second["surface"]["packages"][0]["headline"], "MUTATED HEADLINE")
        self.assertEqual(longform.VISIBLE_TEXT["cross_table_header"][0], "観点")
        self.assertEqual(len(longform.VISIBLE_TEXT["cross_table_header"]), 5)

    def test_derived_value_pure_probes_from_loaded_context(self) -> None:
        # Accepted headline/deck/date/bibliography/style/kicker probes. Each probe
        # starts from an ACTUALLY LOADED valid context (real loader, one chain,
        # spy-captured ordered/records) and mutates ONLY in-memory copies through
        # the PURE projector. Labelled PURE evidence throughout: it proves the
        # projector carries accepted values into reader bytes, not a fresh
        # accepted-loader PASS. Schema/refusal checks use the precise validator.
        chain = self._complete_authorities(self._chain())
        self._current_state(chain)
        captured: dict[str, Any] = {}
        original = longform.build_longform_reader_input

        def spy(*args: Any, **kwargs: Any) -> Any:
            captured["ordered"] = copy.deepcopy(args[5])
            captured["records"] = copy.deepcopy(args[6])
            return original(*args, **kwargs)

        with mock.patch.object(longform, "build_longform_reader_input", spy):
            context = self._derive_checked(chain, scope="pure-probes-baseline")
        baseline_bytes = longform.canonical_reader_bytes(context["surface"])
        profile = copy.deepcopy(context["profile"])
        architecture = core.load_json(chain["source_root"] / "architecture-v2.json")
        synthesis = core.load_json(chain["synthesis_result_path"])
        authored = core.load_json(chain["authored_path"])

        def build(ordered: Any, records: Any, prof: Any = None) -> dict[str, Any]:
            return longform.build_longform_reader_input(
                ISSUE, prof or profile, architecture, authored, synthesis, ordered, records,
            )

        # PURE: accepted deck alteration (spec+result kept consistent in the
        # in-memory copy) reaches the reader surface and validates.
        ordered_deck = copy.deepcopy(captured["ordered"])
        ordered_deck[0]["spec"]["deck"] = "Altered accepted deck."
        ordered_deck[0]["result"]["deck"] = "Altered accepted deck."
        surface_deck = build(ordered_deck, captured["records"])
        self.assertEqual(surface_deck["packages"][0]["deck"], "Altered accepted deck.")
        self.assertNotEqual(longform.canonical_reader_bytes(surface_deck), baseline_bytes)
        longform.validate_longform_reader_input(self.root, surface_deck)
        # PURE refusal (precise): accepted headline drift between spec and result.
        ordered_drift = copy.deepcopy(captured["ordered"])
        ordered_drift[0]["result"]["headline"] = "Drifted headline."
        with self.assertRaisesRegex(ValueError, "Draft semantic archive drift"):
            build(ordered_drift, captured["records"])
        # PURE: accepted temporal policy reaches the displayed date and validates.
        profile_date = copy.deepcopy(profile)
        profile_date["research_scope"]["temporal_policy"]["as_of"] = "2026-09-01T00:00:00+09:00"
        surface_date = build(captured["ordered"], captured["records"], prof=profile_date)
        self.assertIn("2026-09-01", surface_date["issue_metadata"]["display_as_of"])
        self.assertNotEqual(longform.canonical_reader_bytes(surface_date), baseline_bytes)
        longform.validate_longform_reader_input(self.root, surface_date)
        # PURE: accepted bibliography record reaches the bibliography and validates.
        records_bib = copy.deepcopy(captured["records"])
        did = next(iter(records_bib))
        records_bib[did] = {**records_bib[did], "title": "Altered accepted title."}
        surface_bib = build(captured["ordered"], records_bib)
        self.assertEqual(surface_bib["bibliography"][0]["title"], "Altered accepted title.")
        self.assertNotEqual(longform.canonical_reader_bytes(surface_bib), baseline_bytes)
        longform.validate_longform_reader_input(self.root, surface_bib)
        # Schema refusal (precise): fixed style labels are const-validated.
        surface_style = copy.deepcopy(context["surface"])
        surface_style["visible_text"]["edition_descriptor"] = "Mutated edition"
        with self.assertRaises(ValueError):
            longform.validate_longform_reader_input(self.root, surface_style)
        # Kicker unit: derived ordinal/total/suffix grammar on the real helper.
        self.assertEqual(longform._kicker("pkg-001", 1, 1), "THEMATIC LINEAGE 1/1 — 001")
        self.assertEqual(longform._kicker("pkg-002", 2, 2), "THEMATIC LINEAGE 2/2 — 002")

    def test_unsupported_inputs_refuse_reusing_single_chain(self) -> None:
        # One healthy chain captured once; pure projector negatives for profile/
        # format/synthesis/accepted-ref alterations without chain rebuilds.
        chain = self._complete_authorities(self._chain())
        self._current_state(chain)
        captured: dict[str, Any] = {}
        original = longform.build_longform_reader_input

        def spy(*args: Any, **kwargs: Any) -> Any:
            captured["ordered"] = args[5]
            captured["records"] = args[6]
            return original(*args, **kwargs)

        with mock.patch.object(longform, "build_longform_reader_input", spy):
            context = self._derive_checked(chain, scope="unsupported-baseline")
        ordered = captured["ordered"]
        records = captured["records"]
        profile = context["profile"]
        architecture = core.load_json(chain["source_root"] / "architecture-v2.json")
        synthesis = core.load_json(chain["synthesis_result_path"])
        authored = core.load_json(chain["authored_path"])
        # Unsupported research profile refuses (route authority is Profile).
        bad_profile = copy.deepcopy(profile)
        bad_profile["research_profile"] = "WEEKLY"
        with self.assertRaisesRegex(ValueError, "THEMATIC / LONGFORM_SPECIAL"):
            longform.build_longform_reader_input(ISSUE, bad_profile, architecture, authored, synthesis, ordered, records)
        # Unsupported publication profile refuses.
        bad_pub = copy.deepcopy(profile)
        bad_pub["publication_profile"] = "WEEKLY_MAGAZINE"
        with self.assertRaisesRegex(ValueError, "THEMATIC / LONGFORM_SPECIAL"):
            longform.build_longform_reader_input(ISSUE, bad_pub, architecture, authored, synthesis, ordered, records)
        # Altered synthesis issue identity refuses.
        bad_syn = copy.deepcopy(synthesis)
        bad_syn["issue_id"] = "SP999"
        with self.assertRaisesRegex(ValueError, "Synthesis issue identity"):
            longform.build_longform_reader_input(ISSUE, profile, architecture, authored, bad_syn, ordered, records)
        # Altered synthesis shape: a synthesis result without issue identity cannot
        # satisfy the projector's identity check (precise refusal, not a broad
        # exception tuple).
        bad_syn2 = copy.deepcopy(synthesis)
        bad_syn2.pop("issue_id", None)
        with self.assertRaisesRegex(ValueError, "Synthesis issue identity"):
            longform.build_longform_reader_input(ISSUE, profile, architecture, authored, bad_syn2, ordered, records)
        # Token refusals without chain rebuilds. Dots are preserved in keys per the
        # aligned grammar, so a dotted DID yields a valid dotted key; genuinely
        # unsupported tokens refuse at DID/kicker stage.
        with self.assertRaisesRegex(ValueError, "supported Discovery ID"):
            longform._did("not a did", "probe")
        with self.assertRaisesRegex(ValueError, "supported token subset"):
            longform._kicker("bad id!", 1, 1)
        self.assertEqual(longform._bib_key("paper.v1-D001"), "sp001paper.v1d001")


if __name__ == "__main__":
    unittest.main()
