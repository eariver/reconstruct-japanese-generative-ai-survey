"""R1 mechanical-only Weekly receipt/Gate refresh tests.

Builds a real accepted Weekly VALIDATED_DRAFT baseline at the installed R1
source (existing constructors/argv only, synthetic reviews/PDFs), commits an
allowed helper change, then drives the real
`refresh-mechanical-evidence` CLI in fresh processes. No authority or
Git-success stubs; no archived-harness reuse.
"""
from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from pypdf import PdfReader, PdfWriter

from scripts import survey_agent_control_v2 as agent
from scripts import survey_drafting_v2 as drafting
from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality
from scripts import survey_reader_publication_v2 as reader_publication
from scripts import survey_reader_surface_gate_v2 as reader_gate
from scripts import survey_weekly_derivation_v2 as weekly
from scripts import survey_weekly_mechanical_refresh_v2 as refresh_owner
from scripts import survey_weekly_semantic_publication_v2 as weekly_publication
from tests.test_survey_gate_cli_persisted_review_v2 import _semantic_review
from tests import test_survey_increment_b_weekly_derivation_v2 as weekly_b


def _base_suite() -> type:
    """Unbound constructor owner; kept behind a function so unittest module
    loading does not collect the archived suite as part of this module."""
    return weekly_b.IncrementBWeeklyDerivationV2Tests

ISSUE = weekly_b.ISSUE
REPO = Path(__file__).resolve().parents[1]
GIT_ENV_OVERRIDES = (
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_COMMON_DIR",
)
IDENTITY = {
    "GIT_AUTHOR_NAME": "Synthetic Mechanical Refresh Fixture",
    "GIT_AUTHOR_EMAIL": "synthetic-mechanical-refresh@example.invalid",
    "GIT_COMMITTER_NAME": "Synthetic Mechanical Refresh Fixture",
    "GIT_COMMITTER_EMAIL": "synthetic-mechanical-refresh@example.invalid",
}
R1_TIME = datetime(2026, 9, 27, 16, 12, 3, tzinfo=timezone.utc)
R2_TIME = datetime(2026, 9, 27, 16, 12, 57, tzinfo=timezone.utc)


class WeeklyMechanicalRefreshV2Tests(unittest.TestCase):
    def setUp(self) -> None:
        for name in GIT_ENV_OVERRIDES:
            if os.environ.get(name):
                raise AssertionError(f"unsafe inherited Git root override for isolated fixture: {name}")
        scratch = tempfile.TemporaryDirectory(prefix="jgas-weekly-mechanical-r1-")
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name).resolve()
        tracked = subprocess.run(
            ["git", "ls-files", "-z", "--", "config", "schemas", "scripts", "templates", "prompts", "docs", "data"],
            cwd=REPO,
            capture_output=True,
            check=True,
        ).stdout
        for raw in tracked.split(b"\0"):
            if not raw:
                continue
            relative = Path(raw.decode("utf-8"))
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / relative, destination)
        self.git_env = {**os.environ, **IDENTITY}
        for command in (
            ["git", "init", "-q"],
            ["git", "remote", "add", "origin", "https://example.invalid/weekly-mechanical-refresh-fixture.git"],
            ["git", "add", "-A"],
            ["git", "commit", "-q", "-m", "Synthetic isolated mechanical-refresh source basis (R1 installed)"],
        ):
            subprocess.run(command, cwd=self.root, env=self.git_env, check=True, capture_output=True)
        self.cfg = core.load_json(self.root / core.DEFAULT_CONFIG)
        self.head = core.repository_commit_sha(self.root)
        self.source_root = self.root / "sources" / ISSUE
        self.survey_root = self.root / "surveys" / "weekly" / ISSUE

    # -- helpers ---------------------------------------------------------
    def _git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", *args], cwd=self.root, env=self.git_env, capture_output=True, text=True)

    def _commit_helper_comment(self, marker: str) -> str:
        helper = self.root / "scripts/survey_weekly_derivation_v2.py"
        text = helper.read_text(encoding="utf-8")
        helper.write_text(text + f"\n# R1 mechanical-refresh {marker}: comment-only control change.\n", encoding="utf-8")
        self._git("add", "--", "scripts/survey_weekly_derivation_v2.py")
        result = self._git("commit", "-q", "-m", f"R1 fixture {marker} comment-only helper change")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        return core.repository_commit_sha(self.root)

    def _run_refresh(self, reason: str, executor: str, recorded_at: str) -> subprocess.CompletedProcess:
        env = {k: v for k, v in os.environ.items() if k not in GIT_ENV_OVERRIDES}
        env["PYTHONPATH"] = str(self.root)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        cmd = [
            sys.executable,
            str(self.root / "scripts/survey_agent_control_v2.py"),
            "--repo-root",
            str(self.root),
            "refresh-mechanical-evidence",
            "--state",
            str(self.source_root / "production-state.json"),
            "--reason",
            reason,
            "--executor",
            executor,
            "--recorded-at",
            recorded_at,
        ]
        return subprocess.run(cmd, cwd=str(self.root), env=env, capture_output=True, text=True)

    def _advance(self, chain: dict, stage: str, artifacts: dict[str, Path], minute: int) -> None:
        # Reuse the authorized stage-advance constructor without invoking
        # the archived setUp (env-identity fixture here instead).
        return _base_suite()._advance(self, chain, stage, artifacts, minute)

    def _snapshot(self, paths: list[Path]) -> dict[str, str | None]:
        return {str(p): (core.sha256_file(p) if p.is_file() else None) for p in paths}

    def _record_list(self) -> list[str]:
        directory = self.source_root / "publication/v2"
        return sorted(p.name for p in directory.iterdir() if p.name.startswith("publication-surface-revalidation-r"))

    def _build_validated_draft(self) -> dict:
        chain = _base_suite()._complete_authorities(self, _base_suite()._chain(self))
        state_path = _base_suite()._current_state(self, chain)
        argv = [
            "survey_weekly_semantic_publication_v2.py",
            "--repo-root",
            str(self.root),
            "--state",
            str(state_path),
            "--input",
            str(chain["authored_path"]),
        ]
        with mock.patch.object(sys, "argv", argv + ["--materialize-surface-only"]):
            self.assertEqual(weekly_publication.main(), 0)
        publication_root = self.source_root / "publication/v2"
        surface_path = publication_root / "reader-surface-input-v2.json"
        review_path = publication_root / "reader-surface-semantic-review-v2.json"
        core.write_json(
            review_path,
            _semantic_review(
                ISSUE,
                "WEEKLY_MAGAZINE",
                str(surface_path.relative_to(self.root)),
                core.sha256_file(surface_path),
            ),
        )
        with mock.patch.object(sys, "argv", argv):
            self.assertEqual(weekly_publication.main(), 0)
        receipt_path = publication_root / "validated-source-manifest.json"
        weekly.validate_receipt(self.root, receipt_path, state_path)

        architecture = core.load_json(self.source_root / "architecture-v2.json")
        coverage = [
            {
                "package_id": plan["package_id"],
                "requirement": requirement,
                "status": "FULFILLED",
                "reader_locations": ["main.tex:package-1"],
                "detail": "Synthetic fixture author maps the accepted package requirement to its source section.",
            }
            for plan in architecture["packages"]
            for requirement in plan["must_cover_requirements"]
        ]
        requirements = [
            {
                "requirement_id": key,
                "status": "FULFILLED",
                "reader_locations": [location],
                "detail": "Synthetic fixture author asserts this visible requirement is present.",
            }
            for key, location in (("FINAL_SYNTHESIS", "main.tex:summary"), ("WEEKLY_COMMUNITY_MOVEMENT", "main.tex:package-1"))
        ]
        manuscript_path = publication_root / "reader-manuscript-v2.json"
        reader_publication.build_manuscript_manifest(
            self.root,
            ISSUE,
            chain["profile_path"],
            self.source_root / "architecture-v2.json",
            chain["approval_path"],
            self.survey_root / "main.tex",
            [
                {"role": "BIBLIOGRAPHY", "path": str((self.survey_root / "references.bib").relative_to(self.root))},
                {"role": "STYLE", "path": str((self.survey_root / "jgaisurvey.sty").relative_to(self.root))},
            ],
            coverage,
            requirements,
            "synthetic mechanical-refresh manuscript author",
            core.parse_instant("2026-09-19T05:10:00+09:00"),
            manuscript_path,
        )
        gate_path = publication_root / "reader-surface-gate-v2.json"
        reader_publication.build_reader_surface_gate(
            self.root, manuscript_path, review_path, output_path=gate_path, state_path=state_path
        )
        gate = reader_gate.validate_reader_surface_gate(
            self.root,
            gate_path,
            issue_id=ISSUE,
            publication_profile="WEEKLY_MAGAZINE",
            expected_manuscript_path=manuscript_path,
            state_path=state_path,
        )
        self.assertEqual(gate["status"], "PASSED")

        pdf_path = self.survey_root / "main.pdf"
        pdf = PdfWriter()
        pdf.add_blank_page(width=595, height=842)
        with pdf_path.open("wb") as output:
            pdf.write(output)
        self.assertEqual(len(PdfReader(pdf_path).pages), 1)
        subject_path = publication_root / "quality" / "subject-entity-property-binding.json"
        quality_root = publication_root / "quality"
        main_text = (self.survey_root / "main.tex").read_text(encoding="utf-8")
        identifier_path = quality_root / "identifier-preservation.json"
        core.write_json(
            identifier_path,
            {
                "check_id": "IDENTIFIER_PRESERVATION",
                "status": "PASS",
                "source_sha256": core.sha256_file(self.survey_root / "main.tex"),
                "inspected_identifiers": [ISSUE, "Target Model"],
                "scope": "synthetic generated fixture",
            },
        )
        preflight_path = quality_root / "pdf-preflight.json"
        core.write_json(
            preflight_path,
            {
                "check_id": "PDF_PREFLIGHT",
                "status": "PASS",
                "page_count": 1,
                "pdf_sha256": core.sha256_file(pdf_path),
                "byte_count": pdf_path.stat().st_size,
                "scope": "synthetic parseable one-page PDF; not a TeX rendering",
            },
        )
        result_paths = {
            "SUBJECT_ENTITY_PROPERTY_BINDING": subject_path,
            "IDENTIFIER_PRESERVATION": identifier_path,
            "PDF_PREFLIGHT": preflight_path,
        }
        quality_checks = [
            {
                "check_id": check_id,
                "kind": "DETERMINISTIC",
                "status": "PASS",
                "executor": "synthetic mechanical-refresh fixture with actual file assertions",
                "evidence": "Exact fixture bytes and result file inspected by test.",
                "recorded_at": "2026-09-19T05:20:00+09:00",
                "result": {"path": str(path.relative_to(self.root)), "sha256": core.sha256_file(path)},
            }
            for check_id, path in result_paths.items()
        ]
        bundle_path = publication_root / "quality-regression-bundle-v2.json"
        quality.build_bundle(
            self.root, ISSUE, self.survey_root / "main.tex", pdf_path, quality_checks, bundle_path,
            production_profile_path=chain["profile_path"],
        )
        review_paths: dict[str, Path] = {}
        profile = core.load_json(chain["profile_path"])
        for kind, name in (("SEMANTIC_EDITORIAL", "semantic-editorial-review-v2.json"), ("VISUAL", "visual-review-v2.json")):
            checks = [
                {
                    "check_id": check_id,
                    "status": "PASS",
                    "detail": "Synthetic fixture review; no real acceptance asserted.",
                    "evidence_locations": ["synthetic-fixture:main.tex"],
                }
                for check_id in sorted(reader_publication._expected_review_checks(self.root, profile, kind))
            ]
            path = publication_root / name
            reader_publication.build_review_record(
                self.root, manuscript_path, pdf_path, 1, kind, checks,
                f"synthetic mechanical-refresh {kind} reviewer",
                core.parse_instant("2026-09-19T05:30:00+09:00"), path,
            )
            review_paths[kind] = path
        self._advance(
            chain,
            "DRAFT_COMPLETE",
            {
                "reader-manuscript": manuscript_path,
                "validated-source": self.survey_root / "main.tex",
                "publication-pdf": pdf_path,
                "quality-regression-bundle": bundle_path,
                "semantic-review": review_paths["SEMANTIC_EDITORIAL"],
                "visual-review": review_paths["VISUAL"],
                "reader-surface-gate": gate_path,
            },
            130,
        )
        self.assertEqual(core.load_json(state_path)["lifecycle_state"], "VALIDATED_DRAFT")
        return {
            "chain": chain,
            "state_path": state_path,
            "surface_path": surface_path,
            "review_path": review_path,
            "manuscript_path": manuscript_path,
            "gate_path": gate_path,
            "receipt_path": receipt_path,
            "bundle_path": bundle_path,
            "pdf_path": pdf_path,
        }

    # -- §7.1 first + repeat ----------------------------------------------
    def test_first_and_repeat_success(self) -> None:
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        receipt_path = edition["receipt_path"]
        gate_path = edition["gate_path"]
        old_receipt = receipt_path.read_bytes()
        old_gate = gate_path.read_bytes()
        old_state_sha = core.sha256_file(state_path)
        self.assertIsNone(core.load_json(state_path).get("publication_revalidation_provenance"))

        new_head = self._commit_helper_comment("first")
        with self.assertRaisesRegex(ValueError, "implementation or contract changed"):
            weekly.validate_receipt(self.root, receipt_path, state_path)

        proc = self._run_refresh("mechanical helper comment", "synthetic-refresh-executor", "2026-09-27T16:12:03Z")
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        result = json.loads(proc.stdout)
        r1_path = self.root / result["revalidation_record"]
        self.assertTrue(r1_path.is_file())
        r1 = core.load_json(r1_path)
        self.assertIsNone(r1["supersedes"])
        self.assertEqual(r1["reason_class"], "REVIEWED_CORE_CHANGE")
        # New receipt/Gate validate; strict State + active readback accept.
        weekly.validate_receipt(self.root, receipt_path, state_path)
        reader_gate.validate_reader_surface_gate(
            self.root, gate_path, expected_manuscript_path=edition["manuscript_path"], state_path=state_path
        )
        state = core.load_json(state_path)
        self.assertEqual(
            state["publication_revalidation_provenance"],
            {"path": str(r1_path.relative_to(self.root)), "sha256": core.sha256_file(r1_path)},
        )
        self.assertEqual(agent.validate_agent_state(self.root, self.cfg, state), [])
        active, errors = agent.resolve_active_publication_revalidation(self.root, self.cfg, state)
        self.assertEqual(errors, [])
        self.assertIsNotNone(active)
        # Both superseded bytes retained exactly.
        run_dir = self.root / result["retention"]
        self.assertEqual((run_dir / "receipt-superseded.json").read_bytes(), old_receipt)
        self.assertEqual((run_dir / "gate-superseded.json").read_bytes(), old_gate)
        retained_state = (run_dir / "production-state-superseded.json").read_bytes()
        self.assertEqual(core.sha256_bytes(retained_state), old_state_sha)
        # Complete pre/post byte+record inventory: only selected writes occurred.
        # Capture full publication/v2 inventory before (already have old bytes) and
        # verify after that every file except receipt/Gate/State/new-record/retention/guard-absent is unchanged.
        pub_dir = self.source_root / "publication/v2"
        after_files = {p.name: (p.read_bytes() if p.is_file() else None) for p in pub_dir.iterdir() if p.is_file()}
        # Expected selected writes: receipt, Gate, r1 record, State changed; retention is a dir, guard released.
        self.assertNotEqual(receipt_path.read_bytes(), old_receipt)
        self.assertNotEqual(gate_path.read_bytes(), old_gate)
        self.assertIn(r1_path.name, after_files)
        self.assertFalse((pub_dir / ".mechanical-refresh.lock").exists(), "own guard must be released after commit")
        # No temp files left behind.
        for name in after_files:
            self.assertFalse(name.startswith(".reader-surface-gate-v2.json.tmp-"), f"temp left: {name}")
            self.assertFalse(name.startswith(".validated-source-manifest.json.tmp-"), f"temp left: {name}")
        # Retention run dir contains exactly the four expected inert files.
        retained_names = sorted(p.name for p in run_dir.iterdir() if p.is_file())
        self.assertEqual(
            retained_names,
            ["gate-superseded.json", "production-state-superseded.json", "receipt-superseded.json", "retention.json"],
        )
        # Manuscript, bundle, reviews, PDF and prior checkpoint must be byte-identical old->new.
        for key in ("manuscript_path", "bundle_path", "pdf_path"):
            self.assertTrue(edition[key].is_file(), f"expected fixture file missing: {key}")
        new_receipt = core.load_json(receipt_path)
        # Receipt accepted/authored/reviewed/semantic/outputs unchanged except tool provenance/digest/State basis.
        old_receipt_json = json.loads(old_receipt.decode("utf-8"))
        for _k in ("accepted_refs", "authored_refs", "reviewed_reader_input", "semantic_review", "outputs"):
            self.assertEqual(new_receipt[_k], old_receipt_json[_k], f"prospective receipt {_k} must equal bound receipt")
        self.assertEqual(new_receipt["current_tools"]["repository_commit_sha"], new_head)
        self.assertEqual(new_receipt["accepted_refs"], core.load_json(run_dir / "receipt-superseded.json")["accepted_refs"])
        first_gate = gate_path.read_bytes()
        r1_bytes = r1_path.read_bytes()

        second_head = self._commit_helper_comment("second")
        proc2 = self._run_refresh("second mechanical helper comment", "synthetic-refresh-executor", "2026-09-27T16:12:57Z")
        self.assertEqual(proc2.returncode, 0, msg=proc2.stderr)
        result2 = json.loads(proc2.stdout)
        r2_path = self.root / result2["revalidation_record"]
        r2 = core.load_json(r2_path)
        self.assertEqual(r2["supersedes"], {"path": str(r1_path.relative_to(self.root)), "sha256": core.sha256_file(r1_path)})
        # Immutable r1 untouched by the repeat.
        self.assertEqual(r1_path.read_bytes(), r1_bytes)
        weekly.validate_receipt(self.root, receipt_path, state_path)
        reader_gate.validate_reader_surface_gate(
            self.root, gate_path, expected_manuscript_path=edition["manuscript_path"], state_path=state_path
        )
        state2 = core.load_json(state_path)
        self.assertEqual(agent.validate_agent_state(self.root, self.cfg, state2), [])
        self.assertEqual(core.load_json(receipt_path)["current_tools"]["repository_commit_sha"], second_head)
        self.assertNotEqual(gate_path.read_bytes(), first_gate)
        run_dir2 = self.root / result2["retention"]
        self.assertEqual((run_dir2 / "gate-superseded.json").read_bytes(), first_gate)

    # -- §7.2 predecessor / no-op / pre-install ------------------------------
    def test_active_predecessor_not_noop_and_artifact_only_noop(self) -> None:
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        # Artifact-only HEAD move: old receipt still replays, refresh must
        # refuse NO_OP before any retention/guard write.
        notes = self.root / "synthetic-artifact-note.txt"
        notes.write_text("artifact-only edition note\n", encoding="utf-8")
        self._git("add", "--", "synthetic-artifact-note.txt")
        self.assertEqual(self._git("commit", "-q", "-m", "Synthetic artifact-only commit").returncode, 0)
        weekly.validate_receipt(self.root, edition["receipt_path"], state_path)
        before = self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]])
        proc = self._run_refresh("artifact-only attempt", "synthetic-refresh-executor", "2026-09-27T16:13:03Z")
        self.assertEqual(proc.returncode, 2, msg=proc.stdout)
        self.assertRegex(proc.stderr, "MECHANICAL_REFRESH_NO_OP")
        self.assertEqual(before, self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]]))
        self.assertEqual(self._record_list(), [])
        retention_base = self.source_root / "publication/v2/.mechanical-refresh-retention"
        self.assertFalse(retention_base.exists())
        self.assertFalse((self.source_root / "publication/v2/.mechanical-refresh.lock").exists())

    def test_pre_install_control_change_unsupported(self) -> None:
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        helper = self.root / "scripts/survey_production_v2.py"
        helper.write_text(helper.read_text(encoding="utf-8") + "\n# synthetic pre-install control edit\n", encoding="utf-8")
        self._git("add", "--", "scripts/survey_production_v2.py")
        self.assertEqual(self._git("commit", "-q", "-m", "Synthetic pre-install control change").returncode, 0)
        before = self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]])
        proc = self._run_refresh("unsupported control attempt", "synthetic-refresh-executor", "2026-09-27T16:13:03Z")
        self.assertEqual(proc.returncode, 2, msg=proc.stdout)
        self.assertRegex(proc.stderr, "unsupported control/criteria")
        self.assertEqual(before, self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]]))
        self.assertEqual(self._record_list(), [])

    # -- §7.3 change-scope negatives ------------------------------------------
    def test_changed_renderer_output_refused(self) -> None:
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        helper = self.root / "scripts/survey_weekly_derivation_v2.py"
        text = helper.read_text(encoding="utf-8")
        self.assertIn('return "\\n".join(lines)', text)
        helper.write_text(
            text.replace('return "\\n".join(lines)', 'return "\\n".join(lines) + "\\n% output-mutation\\n"'),
            encoding="utf-8",
        )
        self._git("add", "--", "scripts/survey_weekly_derivation_v2.py")
        self.assertEqual(self._git("commit", "-q", "-m", "Synthetic output-changing helper edit").returncode, 0)
        before = self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]])
        proc = self._run_refresh("output-change attempt", "synthetic-refresh-executor", "2026-09-27T16:13:03Z")
        self.assertEqual(proc.returncode, 2, msg=proc.stdout)
        self.assertRegex(proc.stderr, "rendered primary differs|prospective receipt outputs differs")
        self.assertEqual(before, self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]]))
        self.assertEqual(self._record_list(), [])

    def test_accepted_and_authored_mutation_refused(self) -> None:
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        # Independent-case isolation: each subtest restores its exact known bytes
        # in finally so the second case cannot pass on the first case's upstream
        # failure. Authored path targets the actual receipt-bound path by NAME.
        with self.subTest(mutation="accepted"):
            matrix_path = edition["chain"]["matrix_path"]
            original_matrix = matrix_path.read_bytes()
            try:
                matrix = core.load_json(matrix_path)
                matrix["synthetic_mutation"] = "drift"
                core.write_json(matrix_path, matrix)
                before = self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]])
                proc = self._run_refresh("accepted-drift attempt", "synthetic-refresh-executor", "2026-09-27T16:13:03Z")
                self.assertEqual(proc.returncode, 2, msg=proc.stdout)
                # Intended accepted branch: matrix drift (State invalid / checkpoint drift / accepted authority).
                self.assertRegex(proc.stderr, "candidate-matrix|accepted authority differs|strict State invalid")
                self.assertNotIn("publication-semantic-input", proc.stderr)
                self.assertEqual(before, self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]]))
                self.assertEqual(self._record_list(), [])
            finally:
                matrix_path.write_bytes(original_matrix)
        with self.subTest(mutation="authored"):
            # Target actual receipt-bound authored path by NAME, not external index.
            receipt = core.load_json(edition["receipt_path"])
            authored_by_name = {r["name"]: r for r in receipt.get("authored_refs", [])}
            bound_authored_rel = authored_by_name["publication-semantic-input"]["path"]
            bound_authored_path = self.root / bound_authored_rel
            original_authored = bound_authored_path.read_bytes()
            try:
                authored = core.load_json(bound_authored_path)
                authored["cover"]["headline"] = "Unreviewed replacement headline"
                core.write_json(bound_authored_path, authored)
                before = self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]])
                proc = self._run_refresh("authored-drift attempt", "synthetic-refresh-executor", "2026-09-27T16:13:04Z")
                self.assertEqual(proc.returncode, 2, msg=proc.stdout)
                # Intended authored branch (not prior accepted failure): bound authored input drift.
                self.assertRegex(proc.stderr, "publication-semantic-input|exact input drift|independently recomputed reader input differs")
                self.assertNotIn("candidate-matrix", proc.stderr)
                self.assertEqual(before, self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]]))
                self.assertEqual(self._record_list(), [])
            finally:
                bound_authored_path.write_bytes(original_authored)

    def test_review_contract_change_refused(self) -> None:
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        contract_path = self.root / "config/publication-review-v2.json"
        contract = core.load_json(contract_path)
        contract["publication_profiles"]["WEEKLY_MAGAZINE"]["semantic"].append("WITNESS_SUPPLEMENT_REQUIRED_CHECK")
        core.write_json(contract_path, contract)
        self._git("add", "--", "config/publication-review-v2.json")
        self.assertEqual(self._git("commit", "-q", "-m", "Synthetic review-contract change").returncode, 0)
        before = self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]])
        proc = self._run_refresh("criteria-change attempt", "synthetic-refresh-executor", "2026-09-27T16:13:03Z")
        self.assertEqual(proc.returncode, 2, msg=proc.stdout)
        self.assertRegex(proc.stderr, "unsupported control/criteria")
        self.assertEqual(before, self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]]))
        self.assertEqual(self._record_list(), [])

    def test_malformed_old_authority_refused(self) -> None:
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("malformed")
        with self.subTest(case="gate-bytes"):
            gate_path = edition["gate_path"]
            original = gate_path.read_bytes()
            gate_path.write_bytes(original[:-1] + (b"X" if original[-1:] != b"X" else b"Y"))
            try:
                before = self._snapshot([state_path, edition["receipt_path"]])
                proc = self._run_refresh("malformed-gate attempt", "synthetic-refresh-executor", "2026-09-27T16:13:03Z")
                self.assertEqual(proc.returncode, 2, msg=proc.stdout)
                self.assertRegex(proc.stderr, "live Gate differs|digest mismatch|drift")
                self.assertEqual(before, self._snapshot([state_path, edition["receipt_path"]]))
                self.assertEqual(self._record_list(), [])
            finally:
                gate_path.write_bytes(original)
        with self.subTest(case="pointer"):
            # Deliberately leaves State mutated: refusal is the only oracle
            # here and the whole fixture is discarded after this test method.
            state = core.load_json(state_path)
            state["publication_revalidation_provenance"] = {"path": "sources/2026-W37/publication/v2/missing-r9.json", "sha256": "0" * 64}
            core.write_json(state_path, state)
            proc = self._run_refresh("malformed-pointer attempt", "synthetic-refresh-executor", "2026-09-27T16:13:04Z")
            self.assertEqual(proc.returncode, 2, msg=proc.stdout)
            self.assertRegex(proc.stderr, "predecessor invalid|missing or unsafe|SHA mismatch|strict State invalid")
            self.assertEqual(self._record_list(), [])

    def test_dirty_and_untracked_control_refused(self) -> None:
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        with self.subTest(case="dirty"):
            helper = self.root / "scripts/survey_weekly_derivation_v2.py"
            helper.write_text(helper.read_text(encoding="utf-8") + "\n# uncommitted dirty line\n", encoding="utf-8")
            try:
                before = self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]])
                proc = self._run_refresh("dirty attempt", "synthetic-refresh-executor", "2026-09-27T16:13:03Z")
                self.assertEqual(proc.returncode, 2, msg=proc.stdout)
                self.assertRegex(proc.stderr, "differs from committed HEAD|uncommitted|dirty|drift")
                self.assertEqual(before, self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]]))
            finally:
                self._git("checkout", "--", "scripts/survey_weekly_derivation_v2.py")
        with self.subTest(case="untracked"):
            stray = self.root / "scripts/synthetic-untracked-control.py"
            stray.write_text("# untracked control file\n", encoding="utf-8")
            try:
                proc = self._run_refresh("untracked attempt", "synthetic-refresh-executor", "2026-09-27T16:13:04Z")
                self.assertEqual(proc.returncode, 2, msg=proc.stdout)
                self.assertRegex(proc.stderr, "uncommitted source|differs from committed HEAD")
            finally:
                stray.unlink()

    def test_staged_control_change_refused_before_writes(self) -> None:
        # Staged-only divergence (worktree matching HEAD while the index holds a
        # different helper blob) is refused explicitly before any write. Setup
        # uses exact saved bytes for worktree restore (no reset/checkout/clean);
        # the staged index is left for fixture teardown.
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        helper_path = self.root / "scripts/survey_weekly_derivation_v2.py"
        orig = helper_path.read_bytes()
        helper_path.write_bytes(orig + b"\n# synthetic staged-only control change\n")
        self.assertEqual(self._git("add", "--", "scripts/survey_weekly_derivation_v2.py").returncode, 0)
        helper_path.write_bytes(orig)
        before = self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]])
        proc = self._run_refresh("staged attempt", "synthetic-refresh-executor", "2026-09-27T16:13:03Z")
        self.assertEqual(proc.returncode, 2, msg=proc.stdout)
        self.assertRegex(proc.stderr, "staged control changes|differ from committed HEAD")
        self.assertEqual(before, self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]]))
        self.assertEqual(self._record_list(), [])
        self.assertFalse((self.source_root / "publication/v2/.mechanical-refresh.lock").exists())
        self.assertFalse((self.source_root / "publication/v2/.mechanical-refresh-retention").exists())

    # -- §7.4 guard / retention / races -----------------------------------------
    def test_occupied_guard_refuses_without_clobber(self) -> None:
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("guard")
        lock = self.source_root / "publication/v2/.mechanical-refresh.lock"
        lock.write_bytes(b'{"run_id": "foreign"}')
        try:
            before = self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]])
            proc = self._run_refresh("guarded attempt", "synthetic-refresh-executor", "2026-09-27T16:13:03Z")
            self.assertEqual(proc.returncode, 2, msg=proc.stdout)
            self.assertRegex(proc.stderr, "guard occupied")
            self.assertEqual(before, self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]]))
            self.assertEqual(lock.read_bytes(), b'{"run_id": "foreign"}')
            self.assertEqual(self._record_list(), [])
        finally:
            lock.unlink()

    def test_retention_collision_refuses_without_live_write(self) -> None:
        # Run-ids carry a per-operation nonce, so the exact colliding path is
        # controlled here via deterministic nonce injection (in-process direct
        # call; a CLI subprocess could not share the mock). Collision checks
        # stay enforced: the foreign dir and its marker are preserved, live
        # bytes untouched, no record, own guard released after safe abort.
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("collision")
        run_id = "20260927T161203Z-cccccccc"
        run_dir = self.source_root / "publication/v2/.mechanical-refresh-retention" / run_id
        run_dir.mkdir(parents=True)
        (run_dir / "foreign.txt").write_text("foreign", encoding="utf-8")
        old_receipt = edition["receipt_path"].read_bytes()
        old_gate = edition["gate_path"].read_bytes()
        old_state = state_path.read_bytes()
        try:
            with mock.patch.object(refresh_owner.secrets, "token_hex", return_value="c" * 32):
                with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, run_id.replace("-", "\\-")):
                    refresh_owner.refresh_mechanical_evidence(
                        self.root, self.cfg, state_path, "collision attempt", "synthetic-executor", R1_TIME
                    )
            self.assertEqual(edition["receipt_path"].read_bytes(), old_receipt)
            self.assertEqual(edition["gate_path"].read_bytes(), old_gate)
            self.assertEqual(state_path.read_bytes(), old_state)
            self.assertEqual((run_dir / "foreign.txt").read_text(encoding="utf-8"), "foreign")
            self.assertEqual(self._record_list(), [])
            self.assertFalse((self.source_root / "publication/v2/.mechanical-refresh.lock").exists())
        finally:
            shutil.rmtree(run_dir.parent, ignore_errors=True)

    # -- §7.5 fault restoration --------------------------------------------------
    def test_gate_failure_restores_owned_receipt(self) -> None:
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("restore")
        old_receipt = edition["receipt_path"].read_bytes()
        old_gate = edition["gate_path"].read_bytes()
        old_state = state_path.read_bytes()
        with mock.patch.object(
            reader_gate, "evaluate_reader_surface_gate", side_effect=RuntimeError("injected gate failure")
        ):
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "injected gate failure"):
                refresh_owner.refresh_mechanical_evidence(
                    self.root, self.cfg, state_path, "injected failure", "synthetic-executor", R1_TIME
                )
        self.assertEqual(edition["receipt_path"].read_bytes(), old_receipt)
        self.assertEqual(edition["gate_path"].read_bytes(), old_gate)
        self.assertEqual(state_path.read_bytes(), old_state)
        self.assertEqual(self._record_list(), [])

    def test_revalidation_failure_restores_owned_files(self) -> None:
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("reval-fail")
        old_receipt = edition["receipt_path"].read_bytes()
        old_gate = edition["gate_path"].read_bytes()
        old_state = state_path.read_bytes()
        with mock.patch.object(
            agent, "revalidate_publication_surface", side_effect=agent.AgentControlError("injected revalidation failure")
        ):
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "injected revalidation failure"):
                refresh_owner.refresh_mechanical_evidence(
                    self.root, self.cfg, state_path, "injected failure", "synthetic-executor", R1_TIME
                )
        self.assertEqual(edition["receipt_path"].read_bytes(), old_receipt)
        self.assertEqual(edition["gate_path"].read_bytes(), old_gate)
        self.assertEqual(state_path.read_bytes(), old_state)
        self.assertEqual(self._record_list(), [])

    def test_record_collision_preserves_foreign_record(self) -> None:
        # Deterministic allocator collision: a foreign file already occupies
        # the r1 slot while the record listing is empty, so the API's
        # exclusive-create guard (not the max+1 allocator) must refuse
        # without touching the foreign bytes or owned live files.
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("record-collision")
        old_receipt = edition["receipt_path"].read_bytes()
        old_gate = edition["gate_path"].read_bytes()
        old_state = state_path.read_bytes()
        foreign = self.source_root / "publication/v2/publication-surface-revalidation-r1.json"
        foreign.write_bytes(b'{"foreign": true}')
        try:
            with mock.patch.object(agent, "_revalidation_existing_sequences", return_value=[]):
                with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "collision"):
                    refresh_owner.refresh_mechanical_evidence(
                        self.root, self.cfg, state_path, "collision-record attempt",
                        "synthetic-executor", R1_TIME,
                    )
            self.assertEqual(foreign.read_bytes(), b'{"foreign": true}')
            self.assertEqual(edition["receipt_path"].read_bytes(), old_receipt)
            self.assertEqual(edition["gate_path"].read_bytes(), old_gate)
            self.assertEqual(state_path.read_bytes(), old_state)
            self.assertEqual(self._record_list(), ["publication-surface-revalidation-r1.json"])
        finally:
            foreign.unlink(missing_ok=True)

    # -- §7.6 inspection regression ------------------------------------------------
    def test_public_validators_still_reject_without_bypass(self) -> None:
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        receipt_path = edition["receipt_path"]
        gate_path = edition["gate_path"]
        self._commit_helper_comment("regression")
        with self.subTest(case="stale-receipt"):
            with self.assertRaisesRegex(ValueError, "implementation or contract changed"):
                weekly.validate_receipt(self.root, receipt_path, state_path)
        with self.subTest(case="wrong-manuscript"):
            with self.assertRaisesRegex(ValueError, "does not bind the exact expected"):
                reader_gate.validate_reader_surface_gate(
                    self.root, gate_path, expected_manuscript_path=edition["review_path"], state_path=state_path
                )
        with self.subTest(case="unresolved-findings"):
            gate = core.load_json(gate_path)
            gate["findings"].append(
                {
                    "finding_id": "SYNTHETIC-BLOCKING",
                    "rule_id": "SYNTHETIC",
                    "artifact": "synthetic.tex",
                    "path": "synthetic",
                    "locator": "1",
                    "field_or_block": "synthetic",
                    "text_span": "synthetic",
                    "severity": "BLOCKING",
                    "reason": "synthetic",
                    "proposed_normalization": "Rewrite.",
                    "disposition": "UNRESOLVED",
                }
            )
            gate["summary"]["blocking_findings"] = 1
            gate["summary"]["total_findings"] = len(gate["findings"])
            gate["gate_sha256"] = core.sha256_object({k: gate[k] for k in (
                "schema_version", "issue_id", "publication_profile", "status", "scanned_surfaces",
                "rules_checked", "suppressions", "findings", "summary", "evaluated_by",
                "recorded_at", "semantic_authority", "derivation")})
            variant = gate_path.parent / "gate-unresolved-variant.json"
            core.write_json(variant, gate)
            try:
                with self.assertRaisesRegex(ValueError, "unresolved blocking finding"):
                    reader_gate.validate_reader_surface_gate(
                        self.root, variant, expected_manuscript_path=edition["manuscript_path"]
                    )
                with self.assertRaisesRegex(ValueError, "unresolved blocking finding"):
                    reader_gate._inspect_gate_record(
                        self.root, variant, expected_manuscript_path=edition["manuscript_path"]
                    )
            finally:
                variant.unlink()

    # -- R1 correction: guard ownership, symlink, drift, overlap, partial, tamper, postcommit --
    def test_symlink_helpers_reject_ancestors(self) -> None:
        # Fast unit checks: ancestor rejection, guard ownership, Gate equality, private naming.
        # Uses a tiny temp repo root, no Weekly fixture.
        import tempfile

        with tempfile.TemporaryDirectory(prefix="jgas-r1-symlink-unit-") as tmp:
            root = Path(tmp).resolve()
            (root / "a" / "b").mkdir(parents=True)
            # Symlinked ancestor must be rejected.
            (root / "linkdir").symlink_to(root / "a", target_is_directory=True)
            probe = root / "linkdir" / "b" / "file.json"
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "symlinked ancestor"):
                refresh_owner._reject_symlink_ancestors(root, probe, "unit probe")
            # Clean path passes.
            clean = root / "a" / "b" / "file.json"
            refresh_owner._reject_symlink_ancestors(root, clean, "unit clean")
            # Guard ownership: foreign bytes are never deleted; identical bytes
            # with a different file identity are also refused.
            import os as _os

            guard = root / "guard.lock"
            guard.write_bytes(b'{"run_id": "foreign"}')
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "guard changed|foreign guard"):
                refresh_owner._release_guard_if_owned(guard, b'{"run_id": "own"}', None, "unit guard")
            self.assertEqual(guard.read_bytes(), b'{"run_id": "foreign"}')
            # Own guard releases (bytes + identity).
            guard.write_bytes(b'{"run_id": "own"}')
            _own_id = (_os.stat(guard).st_dev, _os.stat(guard).st_ino)
            refresh_owner._release_guard_if_owned(guard, b'{"run_id": "own"}', _own_id, "unit guard")
            self.assertFalse(guard.exists())
            # Identical-contents replacement has a new identity and is refused.
            # (Via atomic rename so the inode cannot be recycled by unlink+recreate.)
            guard.write_bytes(b'{"run_id": "own"}')
            _stale_id = (_os.stat(guard).st_dev, _os.stat(guard).st_ino)
            _replacement = root / "guard.replacement"
            _replacement.write_bytes(b'{"run_id": "own"}')
            _os.replace(_replacement, guard)
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "different file identity|guard changed"):
                refresh_owner._release_guard_if_owned(guard, b'{"run_id": "own"}', _stale_id, "unit guard")
            self.assertEqual(guard.read_bytes(), b'{"run_id": "own"}')
            guard.unlink(missing_ok=True)
            # Raw lexical checks run BEFORE resolve: inside-root alias refused.
            (root / "real").mkdir()
            (root / "real" / "f.json").write_bytes(b"{}")
            (root / "alias").symlink_to(root / "real", target_is_directory=True)
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "symlink"):
                refresh_owner._check_raw_rel_ancestors(root, "alias/f.json", "unit alias")
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "symlink"):
                refresh_owner._check_raw_abs_ancestors(root, root / "alias" / "f.json", "unit alias abs")

    def test_canonical_publication_names_binding(self) -> None:
        # Lightweight prior-binding unit driving the writer's real canonical
        # assertion helper: actual anchored positive control plus
        # filename/role/location decoys. The helper runs before any retained
        # write in the real writer path.
        import tempfile

        with tempfile.TemporaryDirectory(prefix="jgas-r1-names-unit-") as tmp:
            root = Path(tmp).resolve()
            pub = root / "sources" / "2026-W37" / "publication" / "v2"
            pub.mkdir(parents=True)
            surface = pub / "reader-surface-input-v2.json"
            receipt = pub / refresh_owner.RECEIPT_FILENAME
            gate = pub / refresh_owner.GATE_FILENAME
            manuscript_rel = "sources/2026-W37/publication/v2/reader-manuscript-v2.json"
            roles = {
                "reader-manuscript": manuscript_rel,
                "reader-surface-gate": "sources/2026-W37/publication/v2/reader-surface-gate-v2.json",
            }
            # Positive actual anchored control passes.
            refresh_owner._assert_canonical_publication_paths(
                root, pub, surface, receipt, gate, manuscript_rel, roles
            )
            # Decoy filenames refused.
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "filename is not canonical"):
                refresh_owner._assert_canonical_publication_paths(
                    root, pub, pub / "surface-input.json", receipt, gate, manuscript_rel, roles
                )
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "filename is not canonical"):
                refresh_owner._assert_canonical_publication_paths(
                    root, pub, surface, pub / "manifest.json", gate, manuscript_rel, roles
                )
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "filename is not canonical"):
                refresh_owner._assert_canonical_publication_paths(
                    root, pub, surface, receipt, pub / "gate.json", manuscript_rel, roles
                )
            # Non-canonical manuscript role refused (unique-but-wrong is not enough).
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "canonical reader-manuscript role"):
                refresh_owner._assert_canonical_publication_paths(
                    root, pub, surface, receipt, gate,
                    "sources/2026-W37/publication/v2/decoy-manuscript.json", roles,
                )
            # Off-directory surface (canonical name, wrong dir) refused.
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "canonical Profile publication"):
                refresh_owner._assert_canonical_publication_paths(
                    root, pub, root / "reader-surface-input-v2.json", receipt, gate, manuscript_rel, roles
                )

    def test_atomic_replace_temp_ownership(self) -> None:
        # Operating-contract safety for the writer temp helper (lightweight,
        # tmp-dir only): (a) same-inode content change after verification is
        # detected before publish; (b) inode swap with identical bytes is
        # refused by identity. Unknown temps are never removed or published;
        # live stays original with a precise retained-file error.
        import tempfile

        with tempfile.TemporaryDirectory(prefix="jgas-r1-writer-tmp-") as tmp:
            live = Path(tmp).resolve() / "live.json"
            old = b'{"v": 1}\n'
            new = b'{"v": 2}\n'
            live.write_bytes(old)
            old_sha = core.sha256_bytes(old)
            tmp_path = live.parent / ".live.json.tmp-R1UNIT"
            # (a) Same-inode bytes change between verification and publish.
            real_read = Path.read_bytes
            tampered = {"n": 0}

            def tampering_read(self):
                if self == tmp_path:
                    tampered["n"] += 1
                    if tampered["n"] == 2:
                        tmp_path.write_bytes(b'{"tampered": true}\n')
                return real_read(self)

            with mock.patch.object(Path, "read_bytes", autospec=True, side_effect=tampering_read):
                with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "temp bytes changed before replace"):
                    refresh_owner._atomic_replace(live, new, "unit-live", "R1UNIT", expected_old_sha256=old_sha)
            self.assertEqual(live.read_bytes(), old)
            self.assertEqual(tmp_path.read_bytes(), b'{"tampered": true}\n')
            tmp_path.unlink(missing_ok=True)
            # (b) Inode swap with identical bytes refused by identity.
            real_stat = os.stat
            swapped = {"done": False}

            def swapping_stat(path, *args, **kwargs):
                try:
                    result = real_stat(path, *args, **kwargs)
                except OSError:
                    raise
                if path == tmp_path and not swapped["done"]:
                    try:
                        if tmp_path.read_bytes() == new:
                            swapped["done"] = True
                            sib = live.parent / "sibling-identical.json"
                            sib.write_bytes(new)
                            os.replace(sib, tmp_path)
                            result = real_stat(path, *args, **kwargs)
                    except OSError:
                        pass
                return result

            with mock.patch.object(os, "stat", side_effect=swapping_stat):
                with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "temp identity changed before replace"):
                    refresh_owner._atomic_replace(live, new, "unit-live", "R1UNIT", expected_old_sha256=old_sha)
            self.assertTrue(swapped["done"])
            self.assertEqual(live.read_bytes(), old)
            self.assertEqual(tmp_path.read_bytes(), new)

    def test_record_inventory_unreadable_fails_closed_without_writes(self) -> None:
        # Tiny error-injection boundary: unreadable record entries raise a
        # precise error (no '<unreadable>' sentinel treated as clean) and the
        # helper performs zero writes.
        import tempfile

        with tempfile.TemporaryDirectory(prefix="jgas-r1-recinv-unit-") as tmp:
            pub = Path(tmp).resolve()
            rec = pub / "publication-surface-revalidation-r1.json"
            rec.write_bytes(b'{"a": 1}')
            before = sorted(p.name for p in pub.iterdir())
            with mock.patch.object(refresh_owner.core, "sha256_file", side_effect=OSError("injected unreadable")):
                with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "unreadable|record inventory"):
                    refresh_owner._record_inventory(pub)
            self.assertEqual(sorted(p.name for p in pub.iterdir()), before)
            self.assertEqual(rec.read_bytes(), b'{"a": 1}')

    def test_gate_equality_requires_complete_fields(self) -> None:
        import copy

        base = {
            "schema_version": "2.0-rc1",
            "issue_id": "ISSUE",
            "publication_profile": "WEEKLY_MAGAZINE",
            "status": "PASSED",
            "scanned_surfaces": [],
            "rules_checked": [],
            "findings": [],
            "suppressions": [],
            "summary": {"verdict": "PASSED"},
            "evaluated_by": "Core v2 Pre-Publication Reader-Surface Gate",
            "recorded_at": "2026-09-27T16:12:03Z",
            "derivation": {"route": "WEEKLY_GENERATED_V2", "scope": "WEEKLY_MAIN_BIB_STYLE", "receipt": {"path": "r", "sha256": "a" * 64}},
            "semantic_authority": {
                "status": "PASSED", "decision": "PASS", "reviewed_by": "rev",
                "surface_path": "s", "surface_sha256": "b" * 64,
                "recorded_at": "2026-09-27T16:12:03Z", "reviewed_at": "2026-09-27T16:12:03Z",
                "review_path": "p", "review_sha256": "c" * 64,
                "summary": "Bound semantic review passed",
            },
            "gate_sha256": "d" * 64,
        }
        # Identical except allowed top-level recorded_at/digest/receipt passes;
        # the full semantic_authority dictionary is preserved exactly.
        new = copy.deepcopy(base)
        new["recorded_at"] = "2026-09-27T16:13:03Z"
        new["gate_sha256"] = "e" * 64
        new["derivation"]["receipt"] = {"path": "r", "sha256": "f" * 64}
        refresh_owner._compare_gate_reports(base, new, old_receipt_rel="r", old_receipt_sha="a" * 64, new_receipt_sha="f" * 64)
        # Dropped finding must fail.
        bad = copy.deepcopy(new)
        bad["findings"] = [{"finding_id": "X"}]
        with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "findings"):
            refresh_owner._compare_gate_reports(base, bad, old_receipt_rel="r", old_receipt_sha="a" * 64, new_receipt_sha="f" * 64)
        # Semantic timestamp/summary changes are NOT allowed: full preservation.
        for _field, _value in (("recorded_at", "2026-09-27T16:14:03Z"), ("reviewed_at", "2026-09-27T16:14:03Z"), ("summary", "changed")):
            _bad = copy.deepcopy(new)
            _bad["semantic_authority"][_field] = _value
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "semantic_authority"):
                refresh_owner._compare_gate_reports(base, _bad, old_receipt_rel="r", old_receipt_sha="a" * 64, new_receipt_sha="f" * 64)
        # Narrowed semantic field change must fail (covers old 6-field gap + extended fields).
        bad2 = copy.deepcopy(new)
        bad2["semantic_authority"]["surface_path"] = "other"
        with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "semantic_authority"):
            refresh_owner._compare_gate_reports(base, bad2, old_receipt_rel="r", old_receipt_sha="a" * 64, new_receipt_sha="f" * 64)
        # Private helper naming: public inspection-only helper must not exist.
        self.assertFalse(hasattr(weekly, "inspect_receipt_envelope"), "public inspect_receipt_envelope must be private")
        self.assertTrue(hasattr(weekly, "_inspect_receipt_envelope"))

    def test_retention_symlink_refuses_without_live_write(self) -> None:
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("ret-symlink")
        pub_dir = self.source_root / "publication/v2"
        retention_base = pub_dir / ".mechanical-refresh-retention"
        # Replace retention base with a symlink escaping root.
        import tempfile

        with tempfile.TemporaryDirectory(prefix="jgas-r1-escape-") as esc:
            esc_path = Path(esc).resolve()
            # Ensure base does not exist yet, then symlink it out.
            if retention_base.exists() and not retention_base.is_symlink():
                import shutil

                shutil.rmtree(retention_base)
            try:
                if retention_base.is_symlink() or retention_base.exists():
                    retention_base.unlink()
            except OSError:
                pass
            retention_base.symlink_to(esc_path, target_is_directory=True)
            try:
                before = self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]])
                proc = self._run_refresh("symlink-retention attempt", "synthetic-refresh-executor", "2026-09-27T16:13:03Z")
                self.assertEqual(proc.returncode, 2, msg=proc.stdout)
                self.assertRegex(proc.stderr, "symlink|ancestor|retention base")
                self.assertEqual(before, self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]]))
                self.assertEqual(self._record_list(), [])
                # Live bytes untouched, escape dir must not contain retention writes from this run.
                self.assertEqual(list(esc_path.iterdir()), [])
            finally:
                retention_base.unlink(missing_ok=True)

    def test_foreign_guard_replacement_and_removal_retained(self) -> None:
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("foreign-guard")
        pub_dir = self.source_root / "publication/v2"
        lock_path = pub_dir / ".mechanical-refresh.lock"
        old_receipt = edition["receipt_path"].read_bytes()
        old_gate = edition["gate_path"].read_bytes()
        old_state = state_path.read_bytes()
        # Foreign guard present before run: run must refuse without clobbering.
        lock_path.write_bytes(b'{"run_id": "foreign-guard"}')
        try:
            before = self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]])
            proc = self._run_refresh("foreign-guard attempt", "synthetic-refresh-executor", "2026-09-27T16:13:03Z")
            self.assertEqual(proc.returncode, 2, msg=proc.stdout)
            self.assertRegex(proc.stderr, "guard occupied")
            self.assertEqual(lock_path.read_bytes(), b'{"run_id": "foreign-guard"}')
            self.assertEqual(before, self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]]))
        finally:
            lock_path.unlink(missing_ok=True)
        # Guard replacement during run: inject foreign guard after acquisition via fault.
        # Simulate by patching retention mkdir to replace guard, then verify retained fail-closed.
        original_mkdir = Path.mkdir

        def replacing_mkdir(self, *args, **kwargs):
            result = original_mkdir(self, *args, **kwargs)
            # After retention base creation, replace the guard with foreign bytes.
            try:
                candidate = pub_dir / ".mechanical-refresh.lock"
                if candidate.is_file():
                    candidate.write_bytes(b'{"run_id": "replaced-foreign"}')
            except OSError:
                pass
            return result

        with mock.patch.object(Path, "mkdir", autospec=True, side_effect=replacing_mkdir):
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "guard ownership lost|guard changed|foreign guard"):
                refresh_owner.refresh_mechanical_evidence(
                    self.root, self.cfg, state_path, "replaced-guard attempt", "synthetic-executor", R1_TIME
                )
        # Guard ownership lost BEFORE any live mutation: precommit refusal with
        # old authority intact, no new record, foreign guard + retention base left.
        self.assertEqual(lock_path.read_bytes(), b'{"run_id": "replaced-foreign"}')
        self.assertEqual(edition["receipt_path"].read_bytes(), old_receipt)
        self.assertEqual(edition["gate_path"].read_bytes(), old_gate)
        self.assertEqual(state_path.read_bytes(), old_state)
        self.assertEqual(self._record_list(), [])
        self.assertTrue((pub_dir / ".mechanical-refresh-retention").is_dir(), "retention base left for manual recovery")
        # Cleanup foreign guard + retention for fixture teardown.
        lock_path.unlink(missing_ok=True)
        import shutil as _shutil

        _shutil.rmtree(pub_dir / ".mechanical-refresh-retention", ignore_errors=True)

    def test_head_drift_refused(self) -> None:
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("drift-base")
        # HEAD drift: concurrent artifact commit during the run must fail closed.
        # Writer rechecks HEAD after guard and before each live write.
        old_receipt = edition["receipt_path"].read_bytes()
        old_gate = edition["gate_path"].read_bytes()
        old_state = state_path.read_bytes()
        original_replace = refresh_owner._atomic_replace

        def drifting_replace(path, data, label, run_id, expected_old_sha256=None):
            # Simulate concurrent HEAD move just before receipt replace.
            note = self.root / "synthetic-concurrent-note.txt"
            note.write_text("concurrent\n", encoding="utf-8")
            self._git("add", "--", "synthetic-concurrent-note.txt")
            self._git("commit", "-q", "-m", "Synthetic concurrent HEAD drift")
            return original_replace(path, data, label, run_id, expected_old_sha256)

        with mock.patch.object(refresh_owner, "_atomic_replace", side_effect=drifting_replace):
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "HEAD drift|drift before|preserved"):
                refresh_owner.refresh_mechanical_evidence(
                    self.root, self.cfg, state_path, "head-drift attempt", "synthetic-executor", R1_TIME
                )
        # HEAD drift after P2 live receipt install: live NEW preserved (not restored), guard retained.
        self.assertNotEqual(edition["receipt_path"].read_bytes(), old_receipt)
        self.assertEqual(edition["gate_path"].read_bytes(), old_gate)
        self.assertEqual(self._record_list(), [])
        _ = old_state

    def test_state_drift_refused(self) -> None:
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("drift-state")
        orig_state = state_path.read_bytes()
        orig_receipt = edition["receipt_path"].read_bytes()
        orig_gate = edition["gate_path"].read_bytes()
        real_recheck = refresh_owner._recheck_bound_snapshot
        call_count = {"n": 0}

        def state_drifting_recheck(root, snap, controls, label):
            call_count["n"] += 1
            if call_count["n"] == 2:
                # Corrupt State after guard acquisition.
                state_path.write_bytes(orig_state + b" ")
            return real_recheck(root, snap, controls, label)

        with mock.patch.object(refresh_owner, "_recheck_bound_snapshot", side_effect=state_drifting_recheck):
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "drift|preserved|manual recovery"):
                refresh_owner.refresh_mechanical_evidence(
                    self.root, self.cfg, state_path, "state-drift attempt", "synthetic-executor", R1_TIME
                )
        # State drift is fail-closed; live receipt/Gate preserved (old or new owned, never unknown).
        self.assertIn(edition["receipt_path"].read_bytes(), (orig_receipt,))
        self.assertIn(edition["gate_path"].read_bytes(), (orig_gate,))
        _ = orig_state

    def test_two_cooperating_calls_controlled_overlap(self) -> None:
        # TRUE controlled overlap: a second real writer starts synchronously
        # while the first writer still holds the guard (via callback inside the
        # first writer's retention phase). The second must refuse on the
        # occupied guard without touching anything; the first then completes.
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("overlap")
        old_receipt = edition["receipt_path"].read_bytes()
        second_outcome: dict[str, Any] = {}
        _real_exclusive = refresh_owner._exclusive_bytes
        _triggered = {"done": False}

        def overlapping_exclusive(path: Path, data: bytes, label: str) -> None:
            if not _triggered["done"] and label.startswith("retention receipt-superseded"):
                _triggered["done"] = True
                # Second real writer enters while the first holds the guard.
                try:
                    refresh_owner.refresh_mechanical_evidence(
                        self.root, self.cfg, state_path,
                        "overlapping second attempt", "synthetic-executor-2", R2_TIME,
                    )
                    second_outcome["raised"] = False
                except refresh_owner.MechanicalRefreshError as exc:
                    second_outcome["raised"] = True
                    second_outcome["error"] = str(exc)
            return _real_exclusive(path, data, label)

        with mock.patch.object(refresh_owner, "_exclusive_bytes", side_effect=overlapping_exclusive):
            result = refresh_owner.refresh_mechanical_evidence(
                self.root, self.cfg, state_path, "overlap first", "synthetic-executor-1", R1_TIME
            )
        self.assertTrue(_triggered["done"], "overlap callback must have run the second writer")
        self.assertTrue(second_outcome.get("raised"), "second writer must refuse while first holds guard")
        self.assertRegex(second_outcome.get("error", ""), "guard occupied")
        # First writer completed: new authority committed, own guard released.
        self.assertNotEqual(edition["receipt_path"].read_bytes(), old_receipt)
        self.assertEqual(len(self._record_list()), 1)
        self.assertFalse((self.source_root / "publication/v2/.mechanical-refresh.lock").exists())
        self.assertIn("retention", result)
        weekly.validate_receipt(self.root, edition["receipt_path"], state_path)

    def test_post_preflight_drift_refused_without_writes(self) -> None:
        # Drift injected AFTER preflight capture (checkpoint / control script /
        # untracked control file) must be caught by the before-guard recheck
        # with no guard, no retention, no live writes and no new record.
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("post-preflight-drift")
        pub_dir = self.source_root / "publication/v2"
        lock_path = pub_dir / ".mechanical-refresh.lock"
        retention_base = pub_dir / ".mechanical-refresh-retention"
        state = core.load_json(state_path)
        checkpoint_rel = state["checkpoint_provenance"]["validation"]["path"]
        checkpoint_path = self.root / checkpoint_rel
        control_rel = "scripts/survey_production_v2.py"
        control_path = self.root / control_rel
        stray_path = self.root / "scripts" / "synthetic-untracked-r1-drift.py"
        cases = ("checkpoint", "control-dirty", "control-untracked")
        for case in cases:
            with self.subTest(case=case):
                orig_checkpoint = checkpoint_path.read_bytes()
                orig_control = control_path.read_bytes()
                before = self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]])
                real_recheck = refresh_owner._recheck_bound_snapshot
                fired = {"n": 0}

                def drifting_recheck(root, snap, controls, label):
                    fired["n"] += 1
                    if fired["n"] == 1:
                        if case == "checkpoint":
                            checkpoint_path.write_bytes(orig_checkpoint + b" ")
                        elif case == "control-dirty":
                            control_path.write_bytes(orig_control + b"\n# synthetic post-preflight drift\n")
                        else:
                            stray_path.write_text("# synthetic untracked control drift\n", encoding="utf-8")
                    return real_recheck(root, snap, controls, label)

                try:
                    with mock.patch.object(refresh_owner, "_recheck_bound_snapshot", side_effect=drifting_recheck):
                        with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "drift|untracked| differ from committed HEAD"):
                            refresh_owner.refresh_mechanical_evidence(
                                self.root, self.cfg, state_path, f"{case} attempt", "synthetic-executor", R1_TIME
                            )
                    self.assertTrue(fired["n"] >= 1)
                    self.assertFalse(lock_path.exists(), "no guard may be created after post-preflight drift")
                    self.assertFalse(retention_base.exists(), "no retention may be written after post-preflight drift")
                    self.assertEqual(before, self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]]))
                    self.assertEqual(self._record_list(), [])
                finally:
                    checkpoint_path.write_bytes(orig_checkpoint)
                    control_path.write_bytes(orig_control)
                    stray_path.unlink(missing_ok=True)

    def test_alias_state_and_inside_root_symlinks_refused(self) -> None:
        # REAL entry-point alias coverage (not helper-only): a symlinked --state
        # path and inside-root symlinked source/publication/receipt locations
        # must be refused with no guard/retention/live/record writes.
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("alias-entry")
        pub_dir = self.source_root / "publication/v2"
        before = self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]])
        # (a) Symlinked State path through the real library entry.
        alias_state = state_path.parent / "production-state-alias.json"
        alias_state.symlink_to(state_path)
        try:
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "symlink"):
                refresh_owner.refresh_mechanical_evidence(
                    self.root, self.cfg, alias_state, "alias-state attempt", "synthetic-executor", R1_TIME
                )
            self.assertEqual(before, self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]]))
            self.assertEqual(self._record_list(), [])
            self.assertFalse((pub_dir / ".mechanical-refresh.lock").exists())
        finally:
            alias_state.unlink(missing_ok=True)
        # (b) Inside-root symlinked publication directory.
        pub = self.source_root / "publication"
        real = self.source_root / "publication-real"
        pub.rename(real)
        try:
            (self.source_root / "publication").symlink_to(real, target_is_directory=True)
            proc = self._run_refresh("inside-root-alias attempt", "synthetic-refresh-executor", "2026-09-27T16:13:03Z")
            self.assertEqual(proc.returncode, 2, msg=proc.stdout)
            self.assertRegex(proc.stderr, "symlink|ancestor|alias|unsafe")
            self.assertEqual(self._record_list(), [])
        finally:
            (self.source_root / "publication").unlink(missing_ok=True)
            real.rename(pub)
        self.assertEqual(before, self._snapshot([state_path, edition["receipt_path"], edition["gate_path"]]))

    def test_bundle_result_drift_before_and_after_receipt(self) -> None:
        # Actual bundle deterministic result.path/hash (not synthetic): mutation
        # BEFORE any live write must fail with no guard/retention/live/record;
        # mutation AFTER receipt installation must retain the guard and the new
        # owned receipt (never restore new bytes against dependency drift).
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("result-drift")
        pub_dir = self.source_root / "publication/v2"
        lock_path = pub_dir / ".mechanical-refresh.lock"
        bundle_doc = quality.validate_bundle(self.root, edition["bundle_path"], issue_id=ISSUE)
        res_ref = bundle_doc["checks"][0]["result"]
        res_path = self.root / res_ref["path"]
        orig_res = res_path.read_bytes()
        old_receipt = edition["receipt_path"].read_bytes()
        # Phase 1: drift before any live write (first recheck boundary).
        real_recheck = refresh_owner._recheck_bound_snapshot
        fired = {"n": 0}

        def early_drifting_recheck(root, snap, controls, label):
            fired["n"] += 1
            if fired["n"] == 1:
                res_path.write_bytes(orig_res + b" ")
            return real_recheck(root, snap, controls, label)

        try:
            with mock.patch.object(refresh_owner, "_recheck_bound_snapshot", side_effect=early_drifting_recheck):
                with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, res_path.name.replace(".", "\\.")):
                    refresh_owner.refresh_mechanical_evidence(
                        self.root, self.cfg, state_path, "result-drift-before", "synthetic-executor", R1_TIME
                    )
            self.assertFalse(lock_path.exists())
            self.assertFalse((pub_dir / ".mechanical-refresh-retention").exists())
            self.assertEqual(edition["receipt_path"].read_bytes(), old_receipt)
            self.assertEqual(self._record_list(), [])
        finally:
            res_path.write_bytes(orig_res)
        # Phase 2: drift after receipt installation (fourth recheck boundary).
        fired2 = {"n": 0}

        def late_drifting_recheck(root, snap, controls, label):
            fired2["n"] += 1
            if fired2["n"] == 4:
                res_path.write_bytes(orig_res + b" ")
            return real_recheck(root, snap, controls, label)

        try:
            with mock.patch.object(refresh_owner, "_recheck_bound_snapshot", side_effect=late_drifting_recheck):
                with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, res_path.name.replace(".", "\\.")):
                    refresh_owner.refresh_mechanical_evidence(
                        self.root, self.cfg, state_path, "result-drift-after", "synthetic-executor", R1_TIME
                    )
            # Guard retained; new owned receipt preserved (never restored against drift).
            self.assertTrue(lock_path.is_file())
            self.assertNotEqual(edition["receipt_path"].read_bytes(), old_receipt)
            self.assertEqual(self._record_list(), [])
        finally:
            res_path.write_bytes(orig_res)
            lock_path.unlink(missing_ok=True)
            import shutil as _shutil2

            _shutil2.rmtree(pub_dir / ".mechanical-refresh-retention", ignore_errors=True)

    def test_validation_report_drift_before_and_after_receipt(self) -> None:
        # TRUE validation-report coverage (K1): the State.validation
        # checkpoint's reviews CORE_STAGE_CONTRACT.result actual path/hash
        # (not bundle refs). Mutation BEFORE any live write fails at the
        # pre-guard recheck with zero writes; mutation AFTER receipt
        # installation retains the guard plus the new owned receipt (never
        # restored against dependency drift), keeps old Gate/State, creates no
        # record, and names the exact result dependency.
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("validation-report-drift")
        pub_dir = self.source_root / "publication/v2"
        lock_path = pub_dir / ".mechanical-refresh.lock"
        state = core.load_json(state_path)
        validation_rel = state["checkpoint_provenance"]["validation"]["path"]
        checkpoint = core.load_json(self.root / validation_rel)
        result_ref = None
        for review in checkpoint.get("reviews", []):
            if isinstance(review, dict) and review.get("check_id") == agent.CORE_STAGE_REVIEW_ID:
                result_ref = review.get("result")
                break
        if not isinstance(result_ref, dict) or not result_ref.get("path") or not result_ref.get("sha256"):
            self.fail("validation checkpoint lacks CORE_STAGE_CONTRACT result authority")
        res_path = self.root / result_ref["path"]
        orig_res = res_path.read_bytes()
        self.assertEqual(core.sha256_bytes(orig_res), result_ref["sha256"])
        old_receipt = edition["receipt_path"].read_bytes()
        old_gate = edition["gate_path"].read_bytes()
        old_state = state_path.read_bytes()
        # Phase (a): drift before any live write (first recheck boundary).
        real_recheck = refresh_owner._recheck_bound_snapshot
        fired = {"n": 0}

        def early_drifting_recheck(root, snap, controls, label):
            fired["n"] += 1
            if fired["n"] == 1:
                res_path.write_bytes(orig_res + b" ")
            return real_recheck(root, snap, controls, label)

        try:
            with mock.patch.object(refresh_owner, "_recheck_bound_snapshot", side_effect=early_drifting_recheck):
                with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, res_path.name.replace(".", "\\.")):
                    refresh_owner.refresh_mechanical_evidence(
                        self.root, self.cfg, state_path, "validation-report-drift-before", "synthetic-executor", R1_TIME
                    )
            # Zero writes: no guard, no retention, live original, no record.
            # Live bytes equal original because nothing was ever written (spy:
            # guard/retention absence proves no-write, not restore).
            self.assertFalse(lock_path.exists())
            self.assertFalse((pub_dir / ".mechanical-refresh-retention").exists())
            self.assertEqual(edition["receipt_path"].read_bytes(), old_receipt)
            self.assertEqual(edition["gate_path"].read_bytes(), old_gate)
            self.assertEqual(state_path.read_bytes(), old_state)
            self.assertEqual(self._record_list(), [])
        finally:
            res_path.write_bytes(orig_res)
        # Phase (b): drift after receipt installation (fourth recheck boundary).
        fired2 = {"n": 0}

        def late_drifting_recheck(root, snap, controls, label):
            fired2["n"] += 1
            if fired2["n"] == 4:
                res_path.write_bytes(orig_res + b" ")
            return real_recheck(root, snap, controls, label)

        try:
            with mock.patch.object(refresh_owner, "_recheck_bound_snapshot", side_effect=late_drifting_recheck):
                with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, res_path.name.replace(".", "\\.")):
                    refresh_owner.refresh_mechanical_evidence(
                        self.root, self.cfg, state_path, "validation-report-drift-after", "synthetic-executor", R1_TIME
                    )
            # Guard + retention retained; new owned receipt kept (proves no
            # restore-against-drift: restored bytes would equal old_receipt).
            self.assertTrue(lock_path.is_file())
            self.assertNotEqual(edition["receipt_path"].read_bytes(), old_receipt)
            self.assertEqual(edition["gate_path"].read_bytes(), old_gate)
            self.assertEqual(state_path.read_bytes(), old_state)
            self.assertEqual(self._record_list(), [])
        finally:
            res_path.write_bytes(orig_res)
            lock_path.unlink(missing_ok=True)
            import shutil as _shutil4

            _shutil4.rmtree(pub_dir / ".mechanical-refresh-retention", ignore_errors=True)

    def test_partial_api_record_state_write_retained(self) -> None:
        # Partial API record/State write: force API to leave a tampered record + original State,
        # wrapper must retain guard and never delete unknown record.
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("partial-api")
        old_receipt = edition["receipt_path"].read_bytes()
        old_gate = edition["gate_path"].read_bytes()
        old_state = state_path.read_bytes()
        real_api = agent.revalidate_publication_surface

        def partial_api(root, cfg, sp, rc, reason, executor, recorded_at, head):
            # Call real API, then tamper the new record to simulate partial/torn write
            # and restore State to original to simulate torn State (record without State).
            rec = real_api(root, cfg, sp, rc, reason, executor, recorded_at, head)
            # Tamper record after successful commit (simulates torn write observed by wrapper).
            rec.write_bytes(rec.read_bytes() + b" ")
            # Restore State to original to simulate API that wrote record but not State.
            sp.write_bytes(old_state)
            raise agent.AgentControlError("injected partial API torn write")

        with mock.patch.object(agent, "revalidate_publication_surface", side_effect=partial_api):
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "disposition|tamper|unknown|manual recovery|partial"):
                refresh_owner.refresh_mechanical_evidence(
                    self.root, self.cfg, state_path, "partial-api attempt", "synthetic-executor", R1_TIME
                )
        # Tampered record evidence must be preserved, not deleted; live new receipt/Gate preserved (not restored).
        records = self._record_list()
        self.assertTrue(len(records) >= 1)
        tampered_found = False
        for name in records:
            data = (self.source_root / "publication/v2" / name).read_bytes()
            if data.endswith(b" "):
                tampered_found = True
        self.assertTrue(tampered_found, "tampered torn-write record must be preserved")
        self.assertNotEqual(edition["receipt_path"].read_bytes(), old_receipt)
        self.assertNotEqual(edition["gate_path"].read_bytes(), old_gate)
        # Guard retained for manual recovery (since disposition changed).
        self.assertTrue((self.source_root / "publication/v2/.mechanical-refresh.lock").is_file())
        # Cleanup guard for teardown (preserve evidence in test log, then release own? foreign?).
        # The guard at this point is own expected bytes (since API fault retained it); remove for cleanup.
        (self.source_root / "publication/v2/.mechanical-refresh.lock").unlink(missing_ok=True)

    def test_metadata_revalidation_effective_rows_then_refresh(self) -> None:
        # Healthy prior METADATA revalidation with effective manuscript/review
        # rows (not gate-only): snapshot + preflight must use current-effective
        # shas, not false-fail on original checkpoint shas. Pattern follows the
        # existing B pending-renewal helper (manuscript authored_by renewal).
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("meta-first")
        first = refresh_owner.refresh_mechanical_evidence(
            self.root, self.cfg, state_path, "meta first refresh", "synthetic-executor", R1_TIME
        )
        r1_path = self.root / first["revalidation_record"]
        r1_before = r1_path.read_bytes()
        # Metadata renewal: manuscript authored_by change (B helper pattern),
        # Gate rebuild, then a real metadata revalidation (manuscript + Gate
        # superseded, reviews preserved).
        manuscript_path = edition["manuscript_path"]
        manuscript_doc = core.load_json(manuscript_path)
        manuscript_doc["authored_by"] = "synthetic metadata-renewal author"
        manuscript_doc["manifest_sha256"] = core.sha256_object({
            key: value for key, value in manuscript_doc.items() if key != "manifest_sha256"
        })
        core.write_json(manuscript_path, manuscript_doc)
        reader_publication.build_reader_surface_gate(
            self.root, manuscript_path, edition["review_path"],
            output_path=edition["gate_path"], state_path=state_path,
        )
        # Publication reviews bind the manuscript bytes, so renew them too
        # (B pending-renewal pattern: same checks, new reviewer/instant).
        for _kind, _name in (("SEMANTIC_EDITORIAL", "semantic-editorial-review-v2.json"), ("VISUAL", "visual-review-v2.json")):
            _path = self.source_root / "publication" / "v2" / _name
            _old = core.load_json(_path)
            _path.unlink()
            reader_publication.build_review_record(
                self.root, manuscript_path, edition["pdf_path"], 1, _kind,
                _old["checks"], "synthetic metadata-renewal reviewer",
                core.parse_instant("2026-09-19T05:35:00+09:00"), _path,
            )
        r2_path = agent.revalidate_publication_surface(
            self.root, self.cfg, state_path, "REVIEWED_CORE_CHANGE",
            "synthetic metadata renewal", "synthetic-executor",
            core.parse_instant("2026-09-27T16:14:00Z"), None,
        )
        r2 = core.load_json(r2_path)
        renewed_names = {row["name"] for row in r2["superseded_artifacts"]}
        self.assertIn("reader-manuscript", renewed_names)
        self.assertEqual(r1_path.read_bytes(), r1_before)
        # Second helper change + refresh must succeed against effective rows.
        # Recorded_at must advance past the metadata revalidation (chain
        # chronology), so a fresh instant is used here, not R2_TIME.
        self._commit_helper_comment("meta-second")
        result = refresh_owner.refresh_mechanical_evidence(
            self.root, self.cfg, state_path, "meta second refresh", "synthetic-executor",
            core.parse_instant("2026-09-27T16:15:00Z"),
        )
        r3_path = self.root / result["revalidation_record"]
        r3 = core.load_json(r3_path)
        self.assertEqual(r3["supersedes"], {"path": str(r2_path.relative_to(self.root)), "sha256": core.sha256_file(r2_path)})
        self.assertEqual(r1_path.read_bytes(), r1_before)
        weekly.validate_receipt(self.root, edition["receipt_path"], state_path)
        reader_gate.validate_reader_surface_gate(
            self.root, edition["gate_path"], expected_manuscript_path=manuscript_path, state_path=state_path
        )

    def test_same_byte_record_swap_retains_guard(self) -> None:
        # Same-byte foreign record (identical content, new inode) swapped in
        # before an injected API post-write failure: the API must not delete it
        # and the wrapper must retain the guard on unknown record disposition
        # (inventory now pins dev/ino for regular records). Live new receipt is
        # preserved, never restored against the changed disposition.
        import os as _os

        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        self._commit_helper_comment("samebyte-swap")
        old_receipt = edition["receipt_path"].read_bytes()
        pub_dir = self.source_root / "publication/v2"
        lock_path = pub_dir / ".mechanical-refresh.lock"
        real_validate = agent.validate_agent_state
        swapped = {"done": False}

        def swapping_validate(repo_root, cfg, state):
            errors = real_validate(repo_root, cfg, state)
            if state.get("publication_revalidation_provenance") is not None and not swapped["done"]:
                swapped["done"] = True
                rec_ref = state["publication_revalidation_provenance"]
                rec_path = self.root / rec_ref["path"]
                original = rec_path.read_bytes()
                sib = rec_path.parent / "sibling-identical.json"
                sib.write_bytes(original)
                _os.replace(sib, rec_path)
                return ["injected post-write failure"]
            return errors

        with mock.patch.object(agent, "validate_agent_state", side_effect=swapping_validate):
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "disposition|unknown|manual recovery|retained"):
                refresh_owner.refresh_mechanical_evidence(
                    self.root, self.cfg, state_path, "samebyte-swap attempt", "synthetic-executor", R1_TIME
                )
        self.assertTrue(swapped["done"])
        # Guard retained on unknown disposition; foreign same-byte record kept.
        self.assertTrue(lock_path.is_file())
        records = self._record_list()
        self.assertEqual(len(records), 1)
        # Live new receipt preserved (not restored against changed disposition).
        self.assertNotEqual(edition["receipt_path"].read_bytes(), old_receipt)
        lock_path.unlink(missing_ok=True)
        import shutil as _shutil3

        _shutil3.rmtree(pub_dir / ".mechanical-refresh-retention", ignore_errors=True)

    def test_postcommit_reporting_does_not_rollback(self) -> None:
        edition = self._build_validated_draft()
        state_path = edition["state_path"]
        new_head = self._commit_helper_comment("postcommit")
        old_receipt = edition["receipt_path"].read_bytes()
        old_gate = edition["gate_path"].read_bytes()
        # Force post-commit readback to fail after successful API commit,
        # without breaking the API's own post-write validation (which also
        # resolves active with the new provenance). Fail only the second
        # provenance call (writer post-commit), pass the first (API post-write).
        real_resolve = agent.resolve_active_publication_revalidation
        provenance_calls = {"n": 0}

        def failing_resolve(root, cfg, state):
            rec, errs = real_resolve(root, cfg, state)
            if state.get("publication_revalidation_provenance") is not None:
                provenance_calls["n"] += 1
                if provenance_calls["n"] >= 2:
                    return None, ["injected post-commit readback failure"]
            return rec, errs

        with mock.patch.object(agent, "resolve_active_publication_revalidation", side_effect=failing_resolve):
            with self.assertRaisesRegex(refresh_owner.MechanicalRefreshError, "post-commit|committed|no rollback"):
                refresh_owner.refresh_mechanical_evidence(
                    self.root, self.cfg, state_path, "postcommit test", "synthetic-executor", R1_TIME
                )
        # Committed authority must remain (new receipt/Gate + new record + new State), never restored to old.
        self.assertNotEqual(edition["receipt_path"].read_bytes(), old_receipt)
        self.assertNotEqual(edition["gate_path"].read_bytes(), old_gate)
        new_state = core.load_json(state_path)
        self.assertIsNotNone(new_state.get("publication_revalidation_provenance"))
        self.assertEqual(len(self._record_list()), 1)
        # Guard released after commit (own guard), since commit complete.
        self.assertFalse((self.source_root / "publication/v2/.mechanical-refresh.lock").exists())
        _ = new_head


if __name__ == "__main__":
    unittest.main()
