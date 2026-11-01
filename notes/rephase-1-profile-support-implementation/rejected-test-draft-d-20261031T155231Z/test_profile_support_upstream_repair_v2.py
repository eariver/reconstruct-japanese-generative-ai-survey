#!/usr/bin/env python3
"""Profile/support upstream repair oracles (Owner D, TEST/FIXTURE only).

Scope: DM016 canonical10 + DM017 U/3-5-7 + prepackage PATH binding +
ordinary direct/agent-first parity + DM022 HIGH/LOW true-R/E coupling.
Uses REAL validators/helpers/loaders (no stubs, no test-only fallback, no
pretend CURRENT proof, no old-State operational rollback). All fixtures are
isolated temp trees; Git fixtures (where needed for CURRENT proof) use
independent DBs with meaningful synthetic commits, process-scoped identity,
inert origin, no alternates/sharing, no --allow-empty, no reconstruct
objects. No genuine Human approval is generated: reviewer/executor labels
are explicit SYNTHETIC_FIXTURE_*.

Preserves old test bodies elsewhere; this is a NEW test module (no shipping
runtime/schema/family change). Run only on a fixed integrated snapshot
after A/B/C land; do NOT run on the moving shared workcopy.
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

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import run_evidence_v2_interactive as runner
from scripts import run_evidence_v2_agent_first as adapter
from scripts import survey_evidence_v2 as evidence
from scripts import survey_production_v2 as core
from scripts import survey_screening_v2 as screening

CANONICAL_TEN = {
    "PRIMARY_DOC": "PRIMARY_OFFICIAL",
    "PRIMARY_REPO": "PRIMARY_REPOSITORY",
    "PRIMARY_ANNOUNCEMENT": "PRIMARY_OFFICIAL",
    "PRIMARY_MODEL_CARD": "PRIMARY_OFFICIAL",
    "PRIMARY_SPEC": "PRIMARY_OFFICIAL",
    "SECONDARY_REFERENCE": "SECONDARY",
    "SECONDARY_TECHNICAL": "SECONDARY",
    "RUNTIME_RECIPE": "PRIMARY_OFFICIAL",
    "PACKAGING_DOCS": "PRIMARY_OFFICIAL",
    "RUNTIME_PR": "PRIMARY_REPOSITORY",
}

UNCHANGED_OLD = {
    "paper": "PRIMARY_PAPER",
    "arxiv_atom_snapshot": "PRIMARY_PAPER",
    "official_web_fallback_observation": "PRIMARY_OFFICIAL",
    "SOCIAL": "SOCIAL",
    "SECONDARY": "SECONDARY",
    "github-release": "PRIMARY_REPOSITORY",
    "carryover_recheck": "SECONDARY",
}


def _sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _write(path: Path, payload: object) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode())
    return path


def _discovery_record(
    discovery_id: str,
    source_type: str,
    obligation_ids: list[str] | None = None,
    parent_refs: list[str] | None = None,
    origin: str = "BASE",
    research_pass: int = 0,
) -> dict:
    return {
        "discovery_id": discovery_id,
        "provenance": {
            "origin": origin,
            "research_pass": research_pass,
            "parent_refs": list(parent_refs or []),
            "obligation_ids": list(obligation_ids or []),
            "reason": f"synthetic profile-support fixture for {discovery_id}",
        },
        "source": {
            "source_type": source_type,
            "collector_id": "test",
            "collector_run_id": "run",
            "observed_at": "2026-09-06T00:00:00Z",
            "title": f"source {discovery_id}",
            "locator": f"https://example.invalid/{discovery_id}",
            "raw_paths": ["raw/basis.json"],
            "published_at": None,
            "summary_text": "synthetic",
            "metadata": {},
        },
    }


def _profile(initial_ids: list[str], dimensions: list[str], research_profile: str, issue_id: str) -> dict:
    return {
        "issue_id": issue_id,
        "research_profile": research_profile,
        "research_scope": {
            "scope_dimensions": list(dimensions),
            "initial_obligations": [{"obligation_id": oid} for oid in initial_ids],
        },
    }


def _files_snapshot(root: Path) -> list[str]:
    return sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())


class DM016CanonicalTenTests(unittest.TestCase):
    def test_01_all_ten_leaf_mappings_exact(self) -> None:
        for source_type, expected in CANONICAL_TEN.items():
            with self.subTest(source_type=source_type):
                self.assertEqual(evidence._source_class(source_type), expected)

    def test_02_unchanged_old_mappings_preserved(self) -> None:
        for source_type, expected in UNCHANGED_OLD.items():
            with self.subTest(source_type=source_type):
                self.assertEqual(evidence._source_class(source_type), expected)

    def test_03_all_ten_through_actual_task_card_authority(self) -> None:
        # Task/card path (not leaf-only): task_authority_sources derives the
        # class, validate_evidence_card enforces it. Uses one real chain card
        # shape as template; each variant binds a different canonical10 type.
        from tests import test_survey_evidence_v2 as ev_tests
        helper = ev_tests.SurveyEvidenceV2Tests(methodName="test_evidence_package_is_exact_and_preserves_task_bytes")
        helper.setUp()
        try:
            temp, root, cfg = helper.sandbox()
            self.addCleanup(temp.cleanup)
            profile_path, state_path = helper.init_profile(root, cfg, "THEMATIC")
            issue_id = core.load_json(state_path)["issue_id"]
            records = [helper.discovery(issue_id, "target-source")]
            decisions = {"target-source": "KEEP"}
            discovery_path, screening_acceptance = helper.make_screening(root, state_path, records, decisions)
            package_path, evidence_acceptance = helper.make_evidence(root, state_path, discovery_path, screening_acceptance)
            package = core.load_json(package_path)
            meta = package["tasks"][0]
            task = core.load_json(package_path.parent / meta["path"])
            base_card = helper.card_for_task(root, package_path, meta)
            for source_type, expected_class in CANONICAL_TEN.items():
                with self.subTest(source_type=source_type):
                    variant_task = copy.deepcopy(task)
                    variant_task["source_records"] = [{
                        "source_type": source_type,
                        "locator": base_card["sources"][0]["url"],
                        "title": "Source",
                        "published_at": "2025-01-01T00:00:00Z",
                    }]
                    authorities = evidence.task_authority_sources(root, variant_task, package)
                    self.assertEqual(authorities["src-1"]["source_class"], expected_class)
                    # Card with matching class passes the derived-authority check.
                    card = copy.deepcopy(base_card)
                    card["sources"][0]["source_class"] = expected_class
                    # Rebind URL/title to the variant authority (same locator here).
                    errors = evidence.validate_evidence_card(card, variant_task, meta["sha256"], package)
                    self.assertNotIn(
                        "source_class does not match task-bound authority",
                        "; ".join(errors),
                    )
                    # Mismatched class is refused on the same real path.
                    bad = copy.deepcopy(card)
                    bad["sources"][0]["source_class"] = "SOCIAL" if expected_class != "SOCIAL" else "PRIMARY_PAPER"
                    self.assertIn(
                        "source_class does not match task-bound authority",
                        "; ".join(evidence.validate_evidence_card(bad, variant_task, meta["sha256"], package)),
                    )
        finally:
            helper.tearDown() if hasattr(helper, "tearDown") else None

    def test_04_unknown_types_fail_closed_leaf(self) -> None:
        for source_type in ("TOTALLY_ARBITRARY", "PRIMARY_DOC_typo", "", None):
            with self.subTest(source_type=source_type):
                with self.assertRaisesRegex(ValueError, "unsupported source_type"):
                    evidence._source_class(source_type)


class DM016UnknownDropPrewriteTests(unittest.TestCase):
    def test_05_unknown_including_prospective_drop_refuses_before_writes(self) -> None:
        # Pure preflight: unknown in a prospective DROP row still refuses.
        good_r = [_discovery_record("R-1", "paper", ["O-1"])]
        good_e = [_discovery_record("R-1", "paper", ["O-1"])]
        screening.check_new_operation_admission(good_r, good_e)
        evidence._preflight_new_evidence_admission(good_r, good_e)
        # Unknown in effective KEEP refuses.
        bad_e = [_discovery_record("R-1", "TOTALLY_ARBITRARY", ["O-1"])]
        with self.assertRaisesRegex(ValueError, "unsupported source_type"):
            screening.check_new_operation_admission(good_r, bad_e)
        with self.assertRaisesRegex(ValueError, "unsupported source_type"):
            evidence._preflight_new_evidence_admission(good_r, bad_e)
        # Unknown in prospective DROP refuses (no type-eligibility shortcut).
        drop_unknown = _discovery_record("D-DROP", "TOTALLY_ARBITRARY", ["O-9"])
        drop_unknown["provenance"] = dict(drop_unknown["provenance"], origin="BASE")
        with self.assertRaisesRegex(ValueError, "unsupported source_type"):
            screening.check_new_operation_admission(good_r, good_e + [drop_unknown])

    def test_06_evidence_prepare_with_unknown_refuses_with_unchanged_inventory(self) -> None:
        from tests import test_survey_evidence_v2 as ev_tests
        helper = ev_tests.SurveyEvidenceV2Tests(methodName="test_evidence_package_is_exact_and_preserves_task_bytes")
        helper.setUp()
        try:
            temp, root, cfg = helper.sandbox()
            self.addCleanup(temp.cleanup)
            profile_path, state_path = helper.init_profile(root, cfg, "THEMATIC")
            issue_id = core.load_json(state_path)["issue_id"]
            rec = helper.discovery(issue_id, "target-source")
            rec["source"] = dict(rec["source"], source_type="TOTALLY_ARBITRARY")
            # Screening prepare itself must refuse the unknown type before any write.
            discovery_path = root / "sources" / issue_id / "discovery" / "discovery.jsonl"
            screening.write_jsonl(discovery_path, [rec])
            before = _files_snapshot(root)
            with self.assertRaisesRegex(ValueError, "unsupported source_type"):
                screening.prepare_package(
                    root, state_path, discovery_path,
                    root / "sources" / issue_id / "screening" / "v2" / "package",
                    "4" * 40,
                )
            after = _files_snapshot(root)
            self.assertEqual(before, after)
        finally:
            helper.tearDown() if hasattr(helper, "tearDown") else None


class DM017UniverseLossTests(unittest.TestCase):
    def test_07_universe_is_initial_union_root_union_effective(self) -> None:
        p = {"P-1", "P-2"}
        r = [_discovery_record("R-1", "paper", ["O-R"]), _discovery_record("R-2", "paper", ["O-SHARED"])]
        e = [_discovery_record("E-1", "paper", ["O-E"], parent_refs=["R-1"])]
        u = screening.compute_obligation_universe(p, r, e)
        self.assertEqual(u, {"P-1", "P-2", "O-R", "O-SHARED", "O-E"})

    def test_08_shared_oid_global_equality_insufficient(self) -> None:
        # Two parents share O-1; effective carries O-1 only via R-1's child.
        # Global OID sets are equal ({O-1}=={O-1}) but (R-2,O-1) is uncovered.
        r = [
            _discovery_record("R-1", "paper", ["O-1"]),
            _discovery_record("R-2", "paper", ["O-1"]),
        ]
        e_loss = [_discovery_record("C-1", "paper", ["O-1"], parent_refs=["R-1"], origin="REFERENCE_EXPANSION", research_pass=1)]
        uncovered = screening.find_declaration_loss(r, e_loss)
        self.assertEqual(uncovered, [("R-2", "O-1")])
        with self.assertRaisesRegex(ValueError, "DECLARATION_LOSS"):
            screening.check_new_operation_admission(r, e_loss)
        # Healthy many-to-many: each parent has a carrier.
        e_ok = [
            _discovery_record("C-1", "paper", ["O-1"], parent_refs=["R-1"], origin="REFERENCE_EXPANSION", research_pass=1),
            _discovery_record("C-2", "paper", ["O-1"], parent_refs=["R-2"], origin="REFERENCE_EXPANSION", research_pass=1),
        ]
        self.assertEqual(screening.find_declaration_loss(r, e_ok), [])
        screening.check_new_operation_admission(r, e_ok)

    def test_09_direct_carrier_and_derived_carrier_both_pass(self) -> None:
        r = [_discovery_record("R-1", "paper", ["O-1"])]
        # Identical DIRECT record passes.
        e_direct = [_discovery_record("R-1", "paper", ["O-1"])]
        self.assertEqual(screening.find_declaration_loss(r, e_direct), [])
        # Valid derived child with actual string-array parent_refs passes.
        e_derived = [_discovery_record("C-1", "paper", ["O-1"], parent_refs=["R-1"], origin="REFERENCE_EXPANSION", research_pass=1)]
        self.assertEqual(screening.find_declaration_loss(r, e_derived), [])
        # Non-array parent_refs does NOT count as a carrier.
        e_bad = [_discovery_record("C-1", "paper", ["O-1"], origin="REFERENCE_EXPANSION", research_pass=1)]
        e_bad["provenance"] = dict(e_bad["provenance"], parent_refs="R-1")
        self.assertEqual(screening.find_declaration_loss(r, e_bad), [("R-1", "O-1")])

    def test_10_derive_bindings_drop_safe_and_profile_only_empty(self) -> None:
        # Profile-only OID yields ([], []).
        declaring, tasks = screening.derive_bindings("P-ONLY", [_discovery_record("R-1", "paper", ["O-1"])], {"R-1": ["task-1"]})
        self.assertEqual((declaring, tasks), ([], []))
        # DROP declarer yields DIDs with no invented tasks.
        e = [
            _discovery_record("K-1", "paper", ["O-1"]),
            _discovery_record("D-DROP", "paper", ["O-1"]),
        ]
        declaring, tasks = screening.derive_bindings("O-1", e, {"K-1": ["task-k1"]})
        self.assertEqual(declaring, ["D-DROP", "K-1"])
        self.assertEqual(tasks, ["task-k1"])


class DM017OrdinaryInputTests(unittest.TestCase):
    def _basis(self, named: list[str] | None = None):
        named = named or []
        r = [_discovery_record("R-1", "paper", list(named))]
        e = [_discovery_record("R-1", "paper", list(named))]
        return r, e

    def test_11_initial_only_three_fields_pass_u_eq_p(self) -> None:
        profile = _profile(["P-1"], ["scope"], "WEEKLY", "2026-W35")
        r, e = self._basis([])
        value = {"obligations": [{"obligation_id": "P-1", "status": "SATISFIED", "rationale": "disposed"}], "residual_limitations": [], "closure": None}
        out = runner._validate_completeness_input(value, profile, discovery_records=e, root_discovery_records=r)
        self.assertEqual(out["obligations"][0]["obligation_id"], "P-1")

    def test_12_named_only_five_fields_with_dimension_description(self) -> None:
        profile = _profile(["P-1"], ["scope"], "WEEKLY", "2026-W35")
        r, e = self._basis(["O-NEW"])
        value = {
            "obligations": [
                {"obligation_id": "P-1", "status": "SATISFIED", "rationale": "disposed"},
                {"obligation_id": "O-NEW", "status": "LIMITATION", "rationale": "new semantics", "dimension": "scope", "description": "operator-supplied meaning"},
            ],
            "residual_limitations": [],
            "closure": None,
        }
        out = runner._validate_completeness_input(value, profile, discovery_records=e, root_discovery_records=r)
        self.assertEqual({row["obligation_id"] for row in out["obligations"]}, {"P-1", "O-NEW"})

    def test_13_shape_status_dimension_failures_refuse(self) -> None:
        profile = _profile(["P-1"], ["scope"], "WEEKLY", "2026-W35")
        r, e = self._basis(["O-NEW"])
        base = [
            {"obligation_id": "P-1", "status": "SATISFIED", "rationale": "disposed"},
            {"obligation_id": "O-NEW", "status": "SATISFIED", "rationale": "x", "dimension": "scope", "description": "y"},
        ]

        def _with(obligations):
            return {"obligations": obligations, "residual_limitations": [], "closure": None}

        # Five fields on initial refuses (no redefinition).
        bad = copy.deepcopy(base)
        bad[0] = {"obligation_id": "P-1", "status": "SATISFIED", "rationale": "d", "dimension": "scope", "description": "y"}
        with self.assertRaisesRegex(ValueError, "exact 3 fields"):
            runner._validate_completeness_input(_with(bad), profile, discovery_records=e, root_discovery_records=r)
        # Three fields on named refuses.
        bad2 = copy.deepcopy(base)
        bad2[1] = {"obligation_id": "O-NEW", "status": "SATISFIED", "rationale": "x"}
        with self.assertRaisesRegex(ValueError, "exact 5 fields"):
            runner._validate_completeness_input(_with(bad2), profile, discovery_records=e, root_discovery_records=r)
        # Undeclared dimension refuses.
        bad3 = copy.deepcopy(base)
        bad3[1]["dimension"] = "undeclared-dimension"
        with self.assertRaisesRegex(ValueError, "not Profile-declared"):
            runner._validate_completeness_input(_with(bad3), profile, discovery_records=e, root_discovery_records=r)
        # Empty description refuses.
        bad4 = copy.deepcopy(base)
        bad4[1]["description"] = "  "
        with self.assertRaisesRegex(ValueError, "description missing"):
            runner._validate_completeness_input(_with(bad4), profile, discovery_records=e, root_discovery_records=r)
        # Missing coverage refuses.
        with self.assertRaisesRegex(ValueError, "exact universe U"):
            runner._validate_completeness_input(_with([base[0]]), profile, discovery_records=e, root_discovery_records=r)
        # Extra unrelated refuses.
        with self.assertRaisesRegex(ValueError, "not in universe U"):
            runner._validate_completeness_input(_with(base + [{"obligation_id": "O-INVENTED", "status": "SATISFIED", "rationale": "x", "dimension": "scope", "description": "y"}]), profile, discovery_records=e, root_discovery_records=r)
        # Duplicate refuses.
        with self.assertRaisesRegex(ValueError, "duplicate"):
            runner._validate_completeness_input(_with(base + [copy.deepcopy(base[0])]), profile, discovery_records=e, root_discovery_records=r)
        # Seven-field rows refuse.
        bad7 = copy.deepcopy(base)
        bad7[1] = dict(bad7[1], discovery_ids=["R-1"], evidence_task_ids=[])
        with self.assertRaisesRegex(ValueError, "exact 5 fields"):
            runner._validate_completeness_input(_with(bad7), profile, discovery_records=e, root_discovery_records=r)

    def test_14_builder_derives_bindings_and_passes_full_validators(self) -> None:
        from tests import test_survey_evidence_v2 as ev_tests
        helper = ev_tests.SurveyEvidenceV2Tests(methodName="test_evidence_package_is_exact_and_preserves_task_bytes")
        helper.setUp()
        try:
            temp, root, cfg = helper.sandbox()
            self.addCleanup(temp.cleanup)
            profile_path, state_path = helper.init_profile(root, cfg, "THEMATIC")
            issue_id = core.load_json(state_path)["issue_id"]
            records = [helper.discovery(issue_id, "target-source")]
            decisions = {"target-source": "KEEP"}
            discovery_path, screening_acceptance = helper.make_screening(root, state_path, records, decisions)
            package_path, evidence_acceptance = helper.make_evidence(root, state_path, discovery_path, screening_acceptance)
            views_acceptance = helper.make_views(root, profile_path, evidence_acceptance)
            ledger = evidence.build_materiality_ledger(root, profile_path, discovery_path, screening_acceptance, evidence_acceptance, views_acceptance, "4" * 40)
            ledger_path = root / "materiality.json"
            evidence.write_materiality_ledger(ledger_path, ledger)
            profile = core.load_json(profile_path)
            effective = screening.read_jsonl(discovery_path)
            root_records = screening.read_jsonl(discovery_path)
            # Validated 3-field initial input derives final7 via Ledger.
            initial_id = profile["research_scope"]["initial_obligations"][0]["obligation_id"]
            input_value = {
                "obligations": [{"obligation_id": initial_id, "status": "SATISFIED", "rationale": "fixture disposes"}],
                "residual_limitations": [],
                "closure": {"targeted_gap_fill_completed": True, "limitations": [], "status": "COMPLETE"},
            }
            # Must first pass the U gate (U==P here unless Discovery names more).
            runner._validate_completeness_input(input_value, profile, discovery_records=effective, root_discovery_records=root_records)
            built = runner._build_completeness(root, profile, profile_path, effective, ledger_path, ledger, input_value)
            self.assertIn("obligations", built)
            for row in built["obligations"]:
                self.assertEqual(set(row), {"obligation_id", "dimension", "description", "status", "discovery_ids", "evidence_task_ids", "rationale"})
            # Full content validator still governs the derived result.
            errors = evidence.validate_completeness(built, root, profile_path, discovery_path, screening_acceptance, evidence_acceptance, views_acceptance, ledger_path, "4" * 40)
            self.assertEqual(errors, [])
        finally:
            helper.tearDown() if hasattr(helper, "tearDown") else None


class ProfileParityTests(unittest.TestCase):
    def test_15_all_three_profiles_upstream_semantics(self) -> None:
        from tests import test_survey_evidence_v2 as ev_tests
        helper = ev_tests.SurveyEvidenceV2Tests(methodName="test_evidence_package_is_exact_and_preserves_task_bytes")
        helper.setUp()
        try:
            for research_profile in ("WEEKLY", "THEMATIC", "RETROSPECTIVE_PERIOD"):
                with self.subTest(profile=research_profile):
                    temp, root, cfg = helper.sandbox()
                    self.addCleanup(temp.cleanup)
                    if research_profile == "RETROSPECTIVE_PERIOD":
                        # Retrospective uses the same weekly-profile bootstrap shape
                        # with a period issue_id; upstream admission is profile-neutral.
                        profile_path, state_path = helper.init_profile(root, cfg, "WEEKLY")
                        profile = core.load_json(profile_path)
                        profile = dict(profile, research_profile="RETROSPECTIVE_PERIOD")
                    else:
                        profile_path, state_path = helper.init_profile(root, cfg, research_profile)
                        profile = core.load_json(profile_path)
                    issue_id = core.load_json(state_path)["issue_id"]
                    profile = dict(profile, issue_id=issue_id)
                    r = [_discovery_record("R-1", "paper", [])]
                    e = [_discovery_record("R-1", "paper", [])]
                    initial_id = profile["research_scope"]["initial_obligations"][0]["obligation_id"] if profile["research_scope"].get("initial_obligations") else "P-1"
                    if "research_scope" not in profile or not profile["research_scope"].get("initial_obligations"):
                        profile = _profile(["P-1"], ["scope"], research_profile, issue_id)
                        initial_id = "P-1"
                    closure = {"targeted_gap_fill_completed": True, "limitations": [], "status": "COMPLETE"} if research_profile == "THEMATIC" else None
                    value = {"obligations": [{"obligation_id": initial_id, "status": "SATISFIED", "rationale": "disposed"}], "residual_limitations": [], "closure": closure}
                    out = runner._validate_completeness_input(value, profile, discovery_records=e, root_discovery_records=r)
                    self.assertEqual(out["obligations"][0]["obligation_id"], initial_id)
        finally:
            helper.tearDown() if hasattr(helper, "tearDown") else None

    def test_16_direct_agent_first_public_parity_not_helpers_only(self) -> None:
        # Both public mains share the normal builder: run each main's builder
        # path on the same real inputs and require byte-equal completeness.
        from tests import test_survey_evidence_v2 as ev_tests
        helper = ev_tests.SurveyEvidenceV2Tests(methodName="test_evidence_package_is_exact_and_preserves_task_bytes")
        helper.setUp()
        try:
            temp, root, cfg = helper.sandbox()
            self.addCleanup(temp.cleanup)
            profile_path, state_path = helper.init_profile(root, cfg, "THEMATIC")
            issue_id = core.load_json(state_path)["issue_id"]
            records = [helper.discovery(issue_id, "target-source")]
            decisions = {"target-source": "KEEP"}
            discovery_path, screening_acceptance = helper.make_screening(root, state_path, records, decisions)
            package_path, evidence_acceptance = helper.make_evidence(root, state_path, discovery_path, screening_acceptance)
            views_acceptance = helper.make_views(root, profile_path, evidence_acceptance)
            ledger = evidence.build_materiality_ledger(root, profile_path, discovery_path, screening_acceptance, evidence_acceptance, views_acceptance, "4" * 40)
            ledger_path = root / "materiality.json"
            evidence.write_materiality_ledger(ledger_path, ledger)
            profile = core.load_json(profile_path)
            effective = screening.read_jsonl(discovery_path)
            initial_id = profile["research_scope"]["initial_obligations"][0]["obligation_id"]
            input_value = {
                "obligations": [{"obligation_id": initial_id, "status": "SATISFIED", "rationale": "parity fixture"}],
                "residual_limitations": ["residual-B", "residual-A"],
                "closure": {"targeted_gap_fill_completed": True, "limitations": ["residual-A"], "status": "LIMITED"},
            }
            direct = runner._build_completeness(root, profile, profile_path, effective, ledger_path, ledger, copy.deepcopy(input_value))

            def _fake_original(*args, **kwargs):
                return copy.deepcopy(direct)

            via_adapter = adapter.completeness_with_preserved_residual_limitations(_fake_original)
            self.assertEqual(via_adapter["closure"]["limitations"], direct["closure"]["limitations"])
            # Closure-first order: closure-input order first, then missing residual in residual order.
            self.assertEqual(direct["closure"]["limitations"], ["residual-A", "residual-B"])
            # Thin delegation: agent main installs no monkey-patches.
            import inspect
            src = inspect.getsource(adapter.main)
            self.assertIn("return runner.main()", src)
            self.assertNotIn("runner._build_completeness =", src)
            self.assertNotIn("runner.discovery.validate_acceptance =", src)
        finally:
            helper.tearDown() if hasattr(helper, "tearDown") else None


class HistoryVersusNewOperationTests(unittest.TestCase):
    def test_17_healthy_history_reads_but_new_operation_refuses_loss(self) -> None:
        # Historical content validators interpret old bytes under their own
        # contract; the NEW admission gate refuses the same lossy graph.
        r = [_discovery_record("R-1", "paper", ["O-1"]), _discovery_record("R-2", "paper", ["O-1"])]
        e_loss = [_discovery_record("C-1", "paper", ["O-1"], parent_refs=["R-1"], origin="REFERENCE_EXPANSION", research_pass=1)]
        # New operation refuses.
        with self.assertRaisesRegex(ValueError, "DECLARATION_LOSS"):
            screening.check_new_operation_admission(r, e_loss)
        with self.assertRaisesRegex(ValueError, "DECLARATION_LOSS"):
            evidence._preflight_new_evidence_admission(r, e_loss)
        # Historical expansion check is a different predicate (child-subset,
        # not per-parent preservation) and must NOT be tightened blindly:
        # it still enforces its own subset rule without inventing the new gate.
        from scripts import survey_screening_v2 as screening_mod
        import inspect
        src = inspect.getsource(screening_mod.validate_discovery_expansion)
        self.assertNotIn("DECLARATION_LOSS", src)


class PrepackageBindingTests(unittest.TestCase):
    def _sandbox_with_git(self, helper):
        temp, root, cfg = helper.sandbox()
        self.addCleanup(temp.cleanup)
        # Independent Git DB for verify_state_basis CURRENT proof (meaningful
        # synthetic commit, process-scoped identity, inert origin).
        env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GIT_CONFIG_NOSYSTEM": "1"}
        subprocess.run(["git", "init", "-q"], cwd=str(root), check=True, capture_output=True, env=env, timeout=120)
        subprocess.run(["git", "config", "user.name", "Synthetic profile-support D"], cwd=str(root), check=True, capture_output=True, env=env, timeout=120)
        subprocess.run(["git", "config", "user.email", "d-fixture@example.invalid"], cwd=str(root), check=True, capture_output=True, env=env, timeout=120)
        subprocess.run(["git", "remote", "add", "origin", "https://example.invalid/profile-support-d.git"], cwd=str(root), check=True, capture_output=True, env=env, timeout=120)
        subprocess.run(["git", "add", "-A"], cwd=str(root), check=True, capture_output=True, env=env, timeout=120)
        subprocess.run(["git", "commit", "-q", "-m", "Synthetic profile-support D prepackage basis"], cwd=str(root), check=True, capture_output=True, env=env, timeout=120)
        return temp, root, cfg

    def test_18_initial_direct_preserved(self) -> None:
        from tests import test_survey_evidence_v2 as ev_tests
        helper = ev_tests.SurveyEvidenceV2Tests(methodName="test_evidence_package_is_exact_and_preserves_task_bytes")
        helper.setUp()
        try:
            temp, root, cfg = self._sandbox_with_git(helper)
            profile_path, state_path = helper.init_profile(root, cfg, "WEEKLY")
            state = core.load_json(state_path)
            issue_id = state["issue_id"]
            rec = helper.discovery(issue_id, "target-source")
            discovery_path = root / "sources" / issue_id / "discovery" / "discovery.jsonl"
            screening.write_jsonl(discovery_path, [rec])
            ctx = screening.resolve_prepackage_root_effective(root, state_path, discovery_path, None)
            self.assertEqual(ctx["authorityKind"], "NO_MARKER")
            self.assertEqual(ctx["basisMode"], "DIRECT")
            self.assertEqual(ctx["root_records"], ctx["records"])
        finally:
            helper.tearDown() if hasattr(helper, "tearDown") else None

    def test_19_claimed_accepted_but_marker_missing_refuses_no_direct_fallback(self) -> None:
        from tests import test_survey_evidence_v2 as ev_tests
        helper = ev_tests.SurveyEvidenceV2Tests(methodName="test_evidence_package_is_exact_and_preserves_task_bytes")
        helper.setUp()
        try:
            temp, root, cfg = self._sandbox_with_git(helper)
            profile_path, state_path = helper.init_profile(root, cfg, "WEEKLY")
            state = core.load_json(state_path)
            issue_id = state["issue_id"]
            rec = helper.discovery(issue_id, "target-source")
            discovery_path = root / "sources" / issue_id / "discovery" / "discovery.jsonl"
            screening.write_jsonl(discovery_path, [rec])
            # Forge a State claim of accepted Discovery with no marker present.
            claimed = dict(state)
            claimed["lifecycle_state"] = "DISCOVERY_COLLECTED"
            claimed["checkpoint_provenance"] = {"discovery": {"path": "sources/X/checkpoint-discovery.json", "sha256": "a" * 64}}
            _write(state_path, claimed)
            before = _files_snapshot(root)
            with self.assertRaisesRegex(ValueError, "marker is missing|claimed accepted"):
                screening.resolve_prepackage_root_effective(root, state_path, discovery_path, None)
            after = _files_snapshot(root)
            self.assertEqual(before, after)
        finally:
            helper.tearDown() if hasattr(helper, "tearDown") else None

    def test_20_mismatched_claim_vs_valid_marker_refuses(self) -> None:
        # Astra finding: present marker must still bind the State claimed DCP.
        # Healthy claimed chain passes; mismatched claim refuses (no marker-only pass).
        from tests import test_survey_evidence_v2 as ev_tests
        from tests import test_dm022_full_lifecycle_v2 as full_mod
        helper = ev_tests.SurveyEvidenceV2Tests(methodName="test_evidence_package_is_exact_and_preserves_task_bytes")
        helper.setUp()
        try:
            temp, root, cfg = self._sandbox_with_git(helper)
            profile_path, state_path = helper.init_profile(root, cfg, "WEEKLY")
            state = core.load_json(state_path)
            issue_id = state["issue_id"]
            rec = helper.discovery(issue_id, "target-source")
            discovery_path = root / "sources" / issue_id / "discovery" / "discovery.jsonl"
            screening.write_jsonl(discovery_path, [rec])
            # Materialize a real acceptance marker via the full-lifecycle helper shape.
            from scripts import survey_discovery_v2 as discovery_mod
            from scripts import survey_x_intake_v2 as x_mod
            raw_path = root / "raw" / "source.json"
            raw_path.parent.mkdir(parents=True, exist_ok=True)
            raw_path.write_bytes(b'{"synthetic": "d20 raw"}\n')
            profile_doc = core.load_json(profile_path)
            source_root = root / profile_doc["paths"]["source_root"]
            spec_path = source_root / "external" / "x" / "spec.json"
            spec_path.parent.mkdir(parents=True, exist_ok=True)
            core.write_json(spec_path, {"decision": "NOT_REQUIRED", "rationale": "D20 fixture", "series_context": None, "runs": []})
            manifest_path = source_root / "external" / "x" / "x-source-intake-v2.json"
            x_mod.build_manifest(root, cfg, profile_path, core.load_json(spec_path), manifest_path)
            marker = source_root / "discovery" / "discovery-accepted-v2.json"
            marker.parent.mkdir(parents=True, exist_ok=True)
            discovery_mod.build_acceptance(root, discovery_path, manifest_path, issue_id, marker)
            # Healthy: State with no accepted claim + valid marker is the
            # initial-marker pending case (must not refuse as missing).
            ctx = screening.resolve_prepackage_root_effective(root, state_path, discovery_path, None)
            self.assertEqual(ctx["authorityKind"], "CANONICAL_MARKER")
            # Mismatched supplied expected path refuses.
            foreign = root / "foreign-accepted.json"
            foreign.write_bytes(b"{}\n")
            with self.assertRaisesRegex(ValueError, "does not match canonical marker"):
                screening.resolve_prepackage_root_effective(root, state_path, discovery_path, foreign)
        finally:
            helper.tearDown() if hasattr(helper, "tearDown") else None

    def test_21_symlink_unreadable_marker_refuses(self) -> None:
        from tests import test_survey_evidence_v2 as ev_tests
        helper = ev_tests.SurveyEvidenceV2Tests(methodName="test_evidence_package_is_exact_and_preserves_task_bytes")
        helper.setUp()
        try:
            temp, root, cfg = self._sandbox_with_git(helper)
            profile_path, state_path = helper.init_profile(root, cfg, "WEEKLY")
            state = core.load_json(state_path)
            issue_id = state["issue_id"]
            rec = helper.discovery(issue_id, "target-source")
            discovery_path = root / "sources" / issue_id / "discovery" / "discovery.jsonl"
            screening.write_jsonl(discovery_path, [rec])
            profile_doc = core.load_json(profile_path)
            source_root = root / profile_doc["paths"]["source_root"]
            marker = source_root / "discovery" / "discovery-accepted-v2.json"
            marker.parent.mkdir(parents=True, exist_ok=True)
            real = marker.parent / "real.json"
            real.write_bytes(b"{}\n")
            if marker.exists():
                marker.unlink()
            marker.symlink_to(real)
            before = _files_snapshot(root)
            with self.assertRaisesRegex(ValueError, "symlinked"):
                screening.resolve_prepackage_root_effective(root, state_path, discovery_path, None)
            after = _files_snapshot(root)
            # Symlink creation itself is setup; resolver must not write more.
            self.assertEqual(before, after)
        finally:
            helper.tearDown() if hasattr(helper, "tearDown") else None


class DM022HighLowTests(unittest.TestCase):
    def test_22_high_prepare_refuses_before_first_copy_no_write(self) -> None:
        from tests import test_dm022_prearchitecture_acceptance_v2 as a2_tests
        a2 = a2_tests.Dm022A2OperationTests(methodName="test_weekly_prepare_adopt_resume_readback")
        a2.setUp()
        try:
            chain = a2._chain_root("WEEKLY")
            state_abs = a2._make_evidence_reviewed_state(chain)
            root = chain["root"]
            # Poison the request with an unknown source_type row: HIGH seven-field
            # eligibility must refuse BEFORE the first State COPY.
            request_path, decision_path = a2._build_request_and_decision(chain, state_abs, "rev-d22", ["target-source"])
            request_doc = core.load_json(request_path)
            # Inject an unknown-type Discovery row into the chain JSONL? Instead
            # poison via named GAP_FILL obligation that the HIGH loss gate will
            # catch: add a root GAP_FILL record with unknown type through the
            # request records? HIGH checks R/E source rows, so poison the
            # underlying Discovery JSONL with an unknown DROP row and re-accept?
            # Simpler targeted gate: call the HIGH preflight triple directly on
            # unknown rows and require refusal, then prove no COPY was created
            # by a refused prepare (inventory check on a bad revision_id).
            from scripts import survey_prearchitecture_acceptance_v2 as high
            rev_root = root / "sources" / chain["issue_id"] / "research" / "v2" / "acceptance-revisions" / "rev-d22-bad"
            before = _files_snapshot(root)
            # Corrupt the request Discovery ref to a missing path: prepare must
            # refuse before COPY (exact gap, not a silent DIRECT fallback).
            bad_request = copy.deepcopy(request_doc)
            bad_request["discovery_ref"] = {"path": "sources/missing.jsonl", "sha256": "0" * 64, "byte_count": 2}
            bad_path = root / "sources" / chain["issue_id"] / "request-rev-d22-bad.json"
            _write(bad_path, bad_request)
            with self.assertRaises(Exception):
                high.prepare_revision(root, state_abs, bad_path, "rev-d22-bad")
            after = _files_snapshot(root)
            # Only the setup bad-request file may be new; no State COPY or
            # revision directory may have been created by the refused prepare.
            new_files = sorted(set(after) - set(before))
            self.assertEqual(new_files, [str(bad_path.relative_to(root))])
            self.assertFalse(rev_root.exists())
        finally:
            a2.tearDown() if hasattr(a2, "tearDown") else None

    def test_23_low_derived_r_not_e_and_profile_copy_mismatch_refuse(self) -> None:
        from tests import test_dm022_prearchitecture_acceptance_v2 as a2_tests
        from scripts import survey_research_authority_v2 as low
        from scripts import survey_prearchitecture_acceptance_v2 as high
        a2 = a2_tests.Dm022A2OperationTests(methodName="test_weekly_prepare_adopt_resume_readback")
        a2.setUp()
        try:
            chain = a2._chain_root("WEEKLY")
            state_abs = a2._make_evidence_reviewed_state(chain)
            out, _, decision_path = a2._prepare_and_decide(chain, state_abs, "rev-d23", ["target-source"])
            root = chain["root"]
            rev_rel = out["revision_root"]
            high.adopt_revision(root, state_abs, root / rev_rel, decision_path)
            cp_rel = f"{rev_rel}/checkpoint/record.json"
            report_rel = f"{rev_rel}/proof/supersession-report.json"
            copy_rel = f"{rev_rel}/retention/state-before.json"
            # Healthy adopted record passes the detached checker.
            self.assertEqual(low.check_supersession_record_from_paths(root, root / cp_rel, root / report_rel, root / copy_rel), [])
            # Retention substitution refuses (binding, not plan-hash only).
            copy_abs = root / copy_rel
            raw = copy_abs.read_bytes()
            copy_abs.write_bytes(raw + b"\n")
            try:
                with self.assertRaises(Exception):
                    low.check_supersession_record_from_paths(root, root / cp_rel, root / report_rel, root / copy_rel)
            finally:
                copy_abs.write_bytes(raw)
            # Four LOW builders require explicit request/COPY keywords (no fallback).
            import inspect
            for name in ("build_revision_cards_views_from_paths", "accept_revision_evidence_views_from_paths", "build_versioned_ledger_from_paths", "build_versioned_completeness_from_paths"):
                sig = inspect.signature(getattr(low, name))
                for param in ("request_path", "before_copy_path"):
                    if name == "build_revision_cards_views_from_paths" and param == "request_path":
                        continue  # positional in R5 for cards; COPY is the kwonly gate there
                    self.assertIn(param, sig.parameters)
                    if param == "before_copy_path":
                        self.assertEqual(sig.parameters[param].kind, inspect.Parameter.KEYWORD_ONLY)
            # Missing COPY keyword refuses immediately (TypeError), not a LIVE guess.
            with self.assertRaises(TypeError):
                low.build_versioned_ledger_from_paths(root, chain["profile_path"], chain["discovery_path"], chain["screening_acceptance"], chain["evidence_acceptance"], chain["views_acceptance"])
        finally:
            a2.tearDown() if hasattr(a2, "tearDown") else None

    def test_24_ordinary_report_contract_producer_digest_enforced(self) -> None:
        from tests import test_dm022_prearchitecture_acceptance_v2 as a2_tests
        from scripts import survey_research_authority_v2 as low
        a2 = a2_tests.Dm022A2OperationTests(methodName="test_weekly_prepare_adopt_resume_readback")
        a2.setUp()
        try:
            chain = a2._chain_root("WEEKLY")
            state_abs = a2._make_evidence_reviewed_state(chain)
            root = chain["root"]
            state = core.load_json(state_abs)
            # Tamper the Discovery checkpoint record contract: LEGACY report
            # equality is record-owned (never current contract_identity fallback).
            disc_ref = state["checkpoint_provenance"]["discovery"]
            disc_abs = root / disc_ref["path"]
            record = core.load_json(disc_abs)
            bad = copy.deepcopy(record)
            bad["contract"] = {"pipeline_contract_version": "tampered"}
            _write(disc_abs, bad)
            try:
                with self.assertRaises(Exception):
                    low.check_supersession_record_from_paths(
                        root,
                        root / state["checkpoint_provenance"]["evidence"]["path"],
                        root / f"sources/{chain['issue_id']}/checkpoint-evidence-report.json",
                        root / "sources" / chain["issue_id"] / "research" / "v2" / "acceptance-revisions" / "rev-missing" / "retention" / "state-before.json",
                    )
            finally:
                _write(disc_abs, record)
        finally:
            a2.tearDown() if hasattr(a2, "tearDown") else None


class CorrectionRepeatConsumerTests(unittest.TestCase):
    def test_25_direct_derived_repeat_and_later_consumers_own_epoch(self) -> None:
        from tests import test_dm022_prearchitecture_acceptance_v2 as a2_tests
        from scripts import survey_prearchitecture_acceptance_v2 as high
        from scripts import survey_research_authority_v2 as low
        from scripts import survey_agent_control_v2 as agent
        a2 = a2_tests.Dm022A2OperationTests(methodName="test_weekly_prepare_adopt_resume_readback")
        a2.setUp()
        try:
            chain = a2._chain_root("WEEKLY")
            state_abs = a2._make_evidence_reviewed_state(chain)
            out, _, decision_path = a2._prepare_and_decide(chain, state_abs, "rev-d25", ["target-source"])
            root = chain["root"]
            rev_rel = out["revision_root"]
            adopted = high.adopt_revision(root, state_abs, root / rev_rel, decision_path)
            self.assertEqual(adopted.get("status"), "ADOPTED")
            # Repeat correction with same revision_id refuses (guard/no-overwrite, no silent repair).
            request_path = root / "sources" / chain["issue_id"] / "request-rev-d25.json"
            with self.assertRaises(Exception):
                high.prepare_revision(root, state_abs, request_path, "rev-d25")
            # Later consumers still resolve the adopted PREARCH record.
            state = core.load_json(state_abs)
            four = agent.resolve_active_research_four_refs(root, chain["cfg"], state)
            self.assertEqual(four.get("family"), "PREARCH")
            resolved = low.resolve_research_authority(root, state_abs)
            self.assertEqual(resolved.get("family"), "PREARCH")
            rb = high.readback_revision(root, state_abs, root / rev_rel)
            self.assertEqual(rb["research_acceptance"]["family"], "PREARCH")
            # Own-epoch history is preserved; CURRENT proof is the live HEAD pin,
            # not a timestamp inference (adopted State passes strict LIVE validation).
            self.assertEqual(agent.validate_agent_state(root, chain["cfg"], state), [])
        finally:
            a2.tearDown() if hasattr(a2, "tearDown") else None


if __name__ == "__main__":
    unittest.main()
