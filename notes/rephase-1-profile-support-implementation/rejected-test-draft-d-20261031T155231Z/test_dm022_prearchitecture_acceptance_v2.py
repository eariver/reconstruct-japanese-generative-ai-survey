#!/usr/bin/env python3
"""DM022 Owner-A tests: research operation prepare/adopt/resume/readback — A2 correction.

Scope (Owner A only): LOW survey_research_authority_v2 + HIGH
survey_prearchitecture_acceptance_v2 + five schemas/dm022-* + this file's
test-only helper tests/dm022_prearchitecture_fixtures_v2.py (never runtime
authority).

Covers BOTH routes (WEEKLY + THEMATIC) full operation semantics with REAL
chain-helper fixtures (test_survey_evidence_v2.make_chain) + independent Git
DBs + external synthetic decisions, REAL validators/digests, REAL
prepare/adopt/resume/readback (not advice), REAL guard/State/slot/completion
IO, and explicit synthetic provenance. No pytest, no self-raised expected
errors (positive paths assert real success; negative paths use real fixtures
that cause real code refusals). All fixtures are isolated temp trees with
SYNTHETIC provenance; no genuine PASS is generated (supplied decisions are
externally supplied synthetic bundles validated, never minted as approvals).
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

from scripts import survey_production_v2 as core
from scripts import survey_schema_v2 as schema_gate
from scripts import survey_research_authority_v2 as low
from scripts import survey_prearchitecture_acceptance_v2 as high
from tests import dm022_prearchitecture_fixtures_v2 as fix
from tests import test_survey_evidence_v2 as evidence_tests


def _sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _sha_obj(value: object) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _write(path: Path, payload: object) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode())
    return path


class Dm022A2OperationTests(unittest.TestCase):
    """Real prepare/adopt/resume/readback for WEEKLY + THEMATIC (unittest only)."""

    def _fixture_commit(self, root: Path, message: str) -> tuple[str, str]:
        """Real commit in the independent fixture DB (meaningful synthetic change)."""
        env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GIT_CONFIG_NOSYSTEM": "1"}
        subprocess.run(["git", "add", "-A"], cwd=str(root), check=True, capture_output=True, env=env, timeout=120)
        subprocess.run(["git", "commit", "-q", "-m", message], cwd=str(root), check=True, capture_output=True, env=env, timeout=120)
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(root), check=True, capture_output=True, text=True, env=env, timeout=120).stdout.strip()
        tree = subprocess.run(["git", "rev-parse", "HEAD^{tree}"], cwd=str(root), check=True, capture_output=True, text=True, env=env, timeout=120).stdout.strip()
        return head, tree

    def _write_prior_human_review(self, chain: dict, state_abs: Path) -> dict[str, Path]:
        """Record a genuine prior REQUEST_CHANGES Human Gate review on disk.

        Builds a full typed review record + review index exactly per the
        human-gate shapes (same field sets the real writers use), validates
        both against the REAL installed schemas, and writes them with
        no-overwrite semantics. The review carries a real requested-changes
        statement + regeneration boundary and no approval. Returns paths.
        """
        decision = "REQUEST_CHANGES"
        root: Path = chain["root"]
        issue_id: str = chain["issue_id"]
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(root), check=True, capture_output=True, text=True, timeout=120).stdout.strip()
        state_rel = str(state_abs.relative_to(root))
        profile_path: Path = chain["profile_path"]
        profile_doc = core.load_json(profile_path)
        source_root = root / profile_doc["paths"]["source_root"]
        cfg = chain["cfg"]
        reviewed_state = {"path": state_rel, "sha256": _sha_file(state_abs)}
        reviewed_artifacts = [{"name": "production-profile", "path": str(profile_path.relative_to(root)), "sha256": _sha_file(profile_path)}]
        seed = {
            "issue_id": issue_id, "gate": "ARCHITECTURE_REVIEW", "revision": 1, "decision": decision,
            "reviewed_state": reviewed_state, "reviewed_artifacts": reviewed_artifacts,
            "reviewed_repository_commit_sha": head,
        }
        review_id = f"review:{issue_id}:architecture:r1:{core.sha256_object(seed)[:16]}"
        requested_changes: str | None = "Synthetic requested changes: revise selection basis"
        regeneration_boundary: str | None = "EVIDENCE_REVIEWED"
        approval = None
        record = {
            "schema_version": "2.0-rc1",
            "review_id": review_id,
            "issue_id": issue_id,
            "gate": "ARCHITECTURE_REVIEW",
            "revision": 1,
            "decision": decision,
            "reviewed_state": reviewed_state,
            "reviewed_artifacts": reviewed_artifacts,
            "reviewed_repository_commit_sha": head,
            "reviewed_by": "Synthetic Human Reviewer",
            "reviewed_at": "2026-10-28T00:00:00Z",
            "review_reference": "synthetic-human-review-r1",
            "requested_changes": requested_changes,
            "regeneration_boundary": regeneration_boundary,
            "approval": approval,
        }
        schema_gate.validate_instance(record, root / "schemas/human-gate-review-record-v2.schema.json", label="fixture review record")
        # Resolve the real index/record paths via the actual human_gate path
        # helpers over the fixture config (never guessed, never scanned).
        from scripts import survey_human_gate_v2 as human_gate

        record_abs = human_gate.review_record_path(source_root, cfg, "ARCHITECTURE_REVIEW", 1)
        index_abs = human_gate.review_index_path(source_root, cfg)
        self.assertEqual(record_abs, source_root / cfg["state_authority"]["human_review_dir"] / "architecture-r1.json")
        self.assertEqual(index_abs, source_root / cfg["state_authority"]["human_review_index_path"])
        record_abs.parent.mkdir(parents=True, exist_ok=True)
        self.assertFalse(record_abs.exists(), "review record must be a fresh write (no overwrite)")
        _write(record_abs, record)
        index = {
            "schema_version": "2.0-rc1",
            "issue_id": issue_id,
            "reviews": [{
                "gate": "ARCHITECTURE_REVIEW",
                "revision": 1,
                "decision": decision,
                "record": {"path": str(record_abs.relative_to(root)), "sha256": hashlib.sha256(record_abs.read_bytes()).hexdigest()},
            }],
        }
        schema_gate.validate_instance(index, root / "schemas/human-gate-review-index-v2.schema.json", label="fixture review index")
        self.assertFalse(index_abs.exists(), "review index must be a fresh write (no overwrite)")
        index_abs.parent.mkdir(parents=True, exist_ok=True)
        _write(index_abs, index)
        return {"record": record_abs, "index": index_abs}

    def _chain_root(self, research_profile: str, named_obligations=()):
        helper = evidence_tests.SurveyEvidenceV2Tests(methodName="test_evidence_package_is_exact_and_preserves_task_bytes")
        helper.setUp()
        self.addCleanup(helper.tearDown if hasattr(helper, "tearDown") else lambda: None)
        temp, root, cfg = helper.sandbox()
        self.addCleanup(temp.cleanup)
        profile_path, state_path = helper.init_profile(root, cfg, research_profile)
        issue_id = core.load_json(state_path)["issue_id"]
        rec = helper.discovery(issue_id, "target-source")
        if named_obligations:
            rec["provenance"] = dict(rec.get("provenance", {}), obligation_ids=list(named_obligations))
        records = [rec]
        decisions = {"target-source": "KEEP"}
        discovery_path, screening_acceptance = helper.make_screening(root, state_path, records, decisions)
        package_path, evidence_acceptance = helper.make_evidence(root, state_path, discovery_path, screening_acceptance)
        views_acceptance = helper.make_views(root, profile_path, evidence_acceptance)
        # Ledger + completeness via real builders.
        from scripts import survey_evidence_v2 as evidence_mod
        ledger = evidence_mod.build_materiality_ledger(
            root, profile_path, discovery_path, screening_acceptance,
            evidence_acceptance, views_acceptance, "4" * 40,
        )
        issue = core.load_json(state_path)["issue_id"]
        # Ledger canonical path under source_root for DM022 (source_root/materiality-ledger-v2.json).
        profile_doc = core.load_json(profile_path)
        source_root = root / profile_doc["paths"]["source_root"]
        source_root.mkdir(parents=True, exist_ok=True)
        ledger_path = source_root / "materiality-ledger-v2.json"
        evidence_mod.write_materiality_ledger(ledger_path, ledger)
        # Completeness via direct fixture construction (profile-initial union).
        # Test-only fixture building; no runner import (detached A scope).
        discoveries = [helper.discovery(issue_id, "target-source")]
        # Build completeness input from profile initial (SATISFIED).
        initial = profile_doc["research_scope"]["initial_obligations"]
        # Construct via the same union logic as production (profile-initial
        # IDs only for the single-Discovery fixture; discovery_ids and
        # evidence_task_ids re-derived from the real ledger, not invented).
        obligations = []
        for init_row in initial:
            obligations.append({
                "obligation_id": init_row["obligation_id"],
                "dimension": init_row["dimension"],
                "description": init_row["description"],
                "status": "SATISFIED",
                "discovery_ids": ["target-source"],
                "evidence_task_ids": [core.load_json(evidence_acceptance)["results"][0]["evidence_task_id"]],
                "rationale": "fixture evidence satisfies the obligation",
            })
        completeness = {
            "schema_version": "2.0-rc1",
            "issue_id": issue,
            "research_profile": research_profile,
            "basis": {"production_profile_sha256": _sha_file(profile_path), "materiality_ledger_sha256": _sha_file(ledger_path)},
            "overall_status": "READY",
            "obligations": obligations,
            "residual_limitations": [],
            "closure": {"expansion_passes": 1, "final_pass_new_sources": 0, "final_pass_new_material_obligations": 0, "final_pass_new_material_obligations_open": 0, "targeted_gap_fill_completed": True, "open_material_obligations": 0, "limitations": [], "status": "COMPLETE"} if research_profile == "THEMATIC" else None,
        }
        completeness_path = source_root / "profile-completeness-v2.json"
        _write(completeness_path, completeness)
        return {
            "helper": helper, "root": root, "cfg": cfg, "profile_path": profile_path,
            "state_path": state_path, "discovery_path": discovery_path,
            "screening_acceptance": screening_acceptance, "package_path": package_path,
            "evidence_acceptance": evidence_acceptance, "views_acceptance": views_acceptance,
            "ledger_path": ledger_path, "completeness_path": completeness_path,
            "issue_id": issue_id, "research_profile": research_profile,
        }


    def _ensure_dm022_files(self, root: Path) -> None:
        src_root = REPO_ROOT
        for rel in [
            "scripts/survey_research_authority_v2.py",
            "scripts/survey_prearchitecture_acceptance_v2.py",
            "schemas/dm022-revision-request-v2.schema.json",
            "schemas/dm022-revision-manifest-v2.schema.json",
            "schemas/dm022-revision-proof-v2.schema.json",
            "schemas/dm022-preadoption-report-v2.schema.json",
            "schemas/dm022-supersession-checkpoint-v2.schema.json",
        ]:
            src = src_root / rel
            dst = root / rel
            if src.is_file() and not dst.is_file():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)

    def _git_init(self, root: Path) -> tuple[str, str]:
        head, tree = fix.init_independent_git(root, identity=f"dm022-a2-{os.getpid()}")
        return head, tree

    def _materialize_production_discovery_acceptance(self, chain: dict) -> Path:
        """Materialize real Discovery acceptance for the LOW DCP chain (D repair).

        Uses the chain Discovery JSONL bytes plus a real X manifest. WEEKLY
        (REQUIRED_BY_PROFILE) gets a real REQUIRED run + recorded Grok result
        binding the same raw bytes; THEMATIC (CHATGPT_DECIDES) uses
        NOT_REQUIRED. Raw file root/raw/source.json is created with real bytes
        (the chain Discovery source.raw_paths). Never fabricated SHAs. The DCP
        discovery-acceptance artifact must be this acceptance file, never the
        raw JSONL. SCP remains the real Screening acceptance with sibling
        package.json from make_chain.
        """
        from scripts import survey_discovery_v2 as discovery_mod
        from scripts import survey_x_intake_v2 as x_mod
        root: Path = chain["root"]
        cfg: dict = chain["cfg"]
        profile_path: Path = chain["profile_path"]
        profile = core.load_json(profile_path)
        raw_path = root / "raw" / "source.json"
        if not raw_path.is_file():
            raw_path.parent.mkdir(parents=True, exist_ok=True)
            raw_path.write_bytes(b'{"synthetic": "dm022-a2 raw source", "locator": "https://example.invalid/target-source"}\n')
        source_root = root / profile["paths"]["source_root"]
        spec_path = source_root / "external" / "x" / "spec.json"
        spec_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path = source_root / "external" / "x" / "x-source-intake-v2.json"
        if profile["research_profile"] == "WEEKLY":
            if not spec_path.is_file():
                core.write_json(spec_path, {
                    "decision": "REQUIRED",
                    "rationale": "WEEKLY profile requires Grok/X Source Intake (synthetic A2 fixture run)",
                    "series_context": None,
                    "runs": [{
                        "run_id": "run-001",
                        "purpose": "Synthetic A2 fixture X observation for target-source",
                        "research_questions": ["What is the synthetic target finding?"],
                        "coverage_focus": ["synthetic target-source"],
                        "time_scope": "2026-08-22",
                        "expected_result_filename": "result-001.md",
                    }],
                })
            if not manifest_path.is_file():
                x_mod.build_manifest(root, cfg, profile_path, core.load_json(spec_path), manifest_path)
            manifest_doc = core.load_json(manifest_path)
            if manifest_doc.get("status") != "COMPLETE":
                grok_raw = source_root / "external" / "x" / "run-001" / "result-001-raw.json"
                grok_raw.parent.mkdir(parents=True, exist_ok=True)
                if not grok_raw.is_file():
                    grok_raw.write_bytes(raw_path.read_bytes())
                x_mod.record_result(
                    root, cfg, manifest_path, "run-001", raw_path,
                    "result-001.md", "2026-08-22T02:00:00+09:00",
                    "2026-08-22T02:05:00+09:00", "SUCCESS",
                    "DISCOVERY_RECORDED", ["target-source"],
                    "Synthetic A2 fixture Grok observation binds target-source raw bytes")
        else:
            if not spec_path.is_file():
                core.write_json(spec_path, {
                    "decision": "NOT_REQUIRED",
                    "rationale": "A2 fixture does not require X intake",
                    "series_context": None,
                    "runs": [],
                })
            if not manifest_path.is_file():
                x_mod.build_manifest(root, cfg, profile_path, core.load_json(spec_path), manifest_path)
        acceptance_path = source_root / "discovery" / "discovery-accepted-v2.json"
        if not acceptance_path.is_file():
            acceptance_path.parent.mkdir(parents=True, exist_ok=True)
            discovery_mod.build_acceptance(root, chain["discovery_path"], manifest_path, chain["issue_id"], acceptance_path)
        discovery_mod.validate_acceptance(root, acceptance_path)
        return acceptance_path

    def _make_evidence_reviewed_state(self, chain: dict) -> Path:
        """Build minimal valid EVIDENCE_REVIEWED State + 3 checkpoint records.

        Creates legacy discovery/screening/evidence records with REAL SHAs +
        CORE_STAGE_CONTRACT reports, advances State provenance/history to
        EVIDENCE_REVIEWED, and verifies via real agent.validate_agent_state.
        DCP uses the real Discovery acceptance (never raw JSONL); SCP uses the
        real Screening acceptance with sibling package.json.
        """
        from scripts import survey_agent_control_v2 as agent

        root: Path = chain["root"]
        cfg: dict = chain["cfg"]
        issue_id: str = chain["issue_id"]
        profile_path: Path = chain["profile_path"]
        self._ensure_dm022_files(root)
        # Real Discovery acceptance FIRST: DCP must bind acceptance bytes.
        discovery_acceptance_path = self._materialize_production_discovery_acceptance(chain)
        head, _ = self._git_init(root)
        # Recompute contract/implementation after Git init (files unchanged, but
        # HEAD now exists for pins).
        contract = core.contract_identity(root, cfg, chain["research_profile"], "WEEKLY_MAGAZINE" if chain["research_profile"] == "WEEKLY" else "LONGFORM_SPECIAL")
        # Discovery record (ISSUE_INITIALIZED->DISCOVERY_COLLECTED) via real acceptance.
        state_path = root / "sources" / issue_id / "production-state.json"
        # Load initial State (ISSUE_INITIALIZED) to preserve profile/contract/etc.
        init_state = core.load_json(chain["state_path"])
        # Build 3 checkpoint records with real SHAs.
        def _report(state_dict: dict, from_s: str, to_s: str, checkpoints: list[str], artifacts: list[dict]) -> tuple[Path, dict]:
            report = {
                "schema_version": "2.0-rc1", "check_id": "CORE_STAGE_CONTRACT", "status": "PASS",
                "issue_id": issue_id, "from_state": from_s, "to_state": to_s,
                "production_state": {"path": str(state_path.relative_to(root)), "sha256": _sha_file(state_path)},
                "production_profile": {"path": str(profile_path.relative_to(root)), "sha256": _sha_file(profile_path)},
                "implementation_commit_sha": head, "contract": contract,
                "artifacts": artifacts, "recorded_at": "2026-10-28T00:00:00Z",
            }
            return report
        # Discovery artifacts: discovery-acceptance -> real acceptance file (real bytes, never raw JSONL).
        disc_rel = str(discovery_acceptance_path.relative_to(root))
        disc_artifacts = [{"name": "discovery-acceptance", "path": disc_rel, "sha256": _sha_file(discovery_acceptance_path)}]
        disc_report = _report(init_state, "ISSUE_INITIALIZED", "DISCOVERY_COLLECTED", ["discovery"], disc_artifacts)
        disc_report_path = root / "sources" / issue_id / "checkpoint-discovery-report.json"
        _write(disc_report_path, disc_report)
        disc_record = {
            "schema_version": "2.0-rc1", "issue_id": issue_id,
            "from_state": "ISSUE_INITIALIZED", "to_state": "DISCOVERY_COLLECTED",
            "checkpoints": ["discovery"], "recorded_at": "2026-10-28T00:00:00Z",
            "implementation": {"repository_commit_sha": head, "orchestrator_version": cfg["orchestrator_version"]},
            "contract": contract, "artifacts": disc_artifacts,
            "reviews": [{"check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC", "status": "PASS", "executor": "fixture", "evidence": "fixture", "result": {"path": str(disc_report_path.relative_to(root)), "sha256": _sha_file(disc_report_path)}}],
            "summary": "fixture discovery checkpoint",
        }
        disc_record_path = root / "sources" / issue_id / "checkpoint-discovery.json"
        _write(disc_record_path, disc_record)
        # Screening artifacts: screening-acceptance -> screening acceptance file (real).
        scr_rel = str(chain["screening_acceptance"].relative_to(root))
        scr_artifacts = [{"name": "screening-acceptance", "path": scr_rel, "sha256": _sha_file(chain["screening_acceptance"])}]
        scr_report = _report(init_state, "DISCOVERY_COLLECTED", "CANDIDATES_NORMALIZED", ["screening"], scr_artifacts)
        scr_report_path = root / "sources" / issue_id / "checkpoint-screening-report.json"
        _write(scr_report_path, scr_report)
        scr_record = {
            "schema_version": "2.0-rc1", "issue_id": issue_id,
            "from_state": "DISCOVERY_COLLECTED", "to_state": "CANDIDATES_NORMALIZED",
            "checkpoints": ["screening"], "recorded_at": "2026-10-28T00:00:00Z",
            "implementation": {"repository_commit_sha": head, "orchestrator_version": cfg["orchestrator_version"]},
            "contract": contract, "artifacts": scr_artifacts,
            "reviews": [{"check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC", "status": "PASS", "executor": "fixture", "evidence": "fixture", "result": {"path": str(scr_report_path.relative_to(root)), "sha256": _sha_file(scr_report_path)}}],
            "summary": "fixture screening checkpoint",
        }
        scr_record_path = root / "sources" / issue_id / "checkpoint-screening.json"
        _write(scr_record_path, scr_record)
        # Evidence record: 4 research refs (real SHAs from chain).
        ev_rel = str(chain["evidence_acceptance"].relative_to(root))
        vw_rel = str(chain["views_acceptance"].relative_to(root))
        ld_rel = str(chain["ledger_path"].relative_to(root))
        cp_rel = str(chain["completeness_path"].relative_to(root))
        ev_artifacts = [
            {"name": "evidence-acceptance", "path": ev_rel, "sha256": _sha_file(chain["evidence_acceptance"])},
            {"name": "edition-views-acceptance", "path": vw_rel, "sha256": _sha_file(chain["views_acceptance"])},
            {"name": "materiality-ledger", "path": ld_rel, "sha256": _sha_file(chain["ledger_path"])},
            {"name": "profile-completeness", "path": cp_rel, "sha256": _sha_file(chain["completeness_path"])},
        ]
        ev_report = _report(init_state, "CANDIDATES_NORMALIZED", "EVIDENCE_REVIEWED", ["evidence", "materiality", "completeness"], ev_artifacts)
        ev_report_path = root / "sources" / issue_id / "checkpoint-evidence-report.json"
        _write(ev_report_path, ev_report)
        ev_record = {
            "schema_version": "2.0-rc1", "issue_id": issue_id,
            "from_state": "CANDIDATES_NORMALIZED", "to_state": "EVIDENCE_REVIEWED",
            "checkpoints": ["evidence", "materiality", "completeness"], "recorded_at": "2026-10-28T00:00:00Z",
            "implementation": {"repository_commit_sha": head, "orchestrator_version": cfg["orchestrator_version"]},
            "contract": contract, "artifacts": ev_artifacts,
            "reviews": [{"check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC", "status": "PASS", "executor": "fixture", "evidence": "fixture", "result": {"path": str(ev_report_path.relative_to(root)), "sha256": _sha_file(ev_report_path)}}],
            "summary": "fixture evidence checkpoint",
        }
        ev_record_path = root / "sources" / issue_id / "checkpoint-evidence.json"
        _write(ev_record_path, ev_record)
        # State at EVIDENCE_REVIEWED with valid provenance/history.
        profile_doc = core.load_json(profile_path)
        source_root_rel = profile_doc["paths"]["source_root"]
        canonical_state_rel = f"{source_root_rel}/production-state.json"
        new_state = copy.deepcopy(init_state)
        new_state["lifecycle_state"] = "EVIDENCE_REVIEWED"
        new_state["contract"] = contract
        new_state["implementation"] = {"repository_commit_sha": head, "orchestrator_version": cfg["orchestrator_version"]}
        new_state["machine_checkpoints"] = {
            "discovery": "passed", "screening": "passed", "evidence": "passed",
            "materiality": "passed", "completeness": "passed",
            "selection": "pending", "architecture": "pending", "draft": "pending",
            "validation": "pending", "publication_preview": "pending",
            "freeze": "pending", "release": "pending",
        }
        new_state["checkpoint_provenance"] = {
            "discovery": {"path": str(disc_record_path.relative_to(root)), "sha256": _sha_file(disc_record_path)},
            "screening": {"path": str(scr_record_path.relative_to(root)), "sha256": _sha_file(scr_record_path)},
            "evidence": {"path": str(ev_record_path.relative_to(root)), "sha256": _sha_file(ev_record_path)},
            "materiality": {"path": str(ev_record_path.relative_to(root)), "sha256": _sha_file(ev_record_path)},
            "completeness": {"path": str(ev_record_path.relative_to(root)), "sha256": _sha_file(ev_record_path)},
            "selection": None, "architecture": None, "draft": None,
            "validation": None, "publication_preview": None,
            "freeze": None, "release": None,
        }
        new_state["human_gates"] = {"architecture_review": "pending", "publication_preview": "pending"}
        new_state["human_gate_provenance"] = {"architecture_review": None, "publication_preview": None}
        new_state["target_gate"] = "ARCHITECTURE_REVIEW"
        new_state["next_action"] = "stage:selection"
        new_state["terminal_reason"] = None
        new_state["exception_gate"] = {"status": "inactive", "reason": None}
        new_state["publication_revalidation_provenance"] = None
        new_state["history"] = [
            {"from": None, "to": "ISSUE_INITIALIZED", "recorded_at": "2026-10-28T00:00:00Z", "repository_commit_sha": head},
            {"from": "ISSUE_INITIALIZED", "to": "DISCOVERY_COLLECTED", "recorded_at": "2026-10-28T00:00:01Z", "repository_commit_sha": head},
            {"from": "DISCOVERY_COLLECTED", "to": "CANDIDATES_NORMALIZED", "recorded_at": "2026-10-28T00:00:02Z", "repository_commit_sha": head},
            {"from": "CANDIDATES_NORMALIZED", "to": "EVIDENCE_REVIEWED", "recorded_at": "2026-10-28T00:00:03Z", "repository_commit_sha": head},
        ]
        # Write canonical State (source_root/production-state.json) + update profile SHA if needed.
        canonical_state_abs = root / canonical_state_rel
        canonical_state_abs.parent.mkdir(parents=True, exist_ok=True)
        # Profile must match State.profile SHA (init_state profile already matches; keep).
        _write(canonical_state_abs, new_state)
        # Verify via real agent validator (must pass; otherwise fixture is dishonest).
        errs = agent.validate_agent_state(root, cfg, core.load_json(canonical_state_abs))
        self.assertEqual(errs, [], f"fixture EVIDENCE_REVIEWED State must pass real agent validation: {errs}")
        return canonical_state_abs

    def _build_request_and_decision(self, chain: dict, state_abs: Path, revision_id: str, affected: list[str], extra_obligations=()) -> tuple[Path, Path]:
        root: Path = chain["root"]
        cfg: dict = chain["cfg"]
        profile_path: Path = chain["profile_path"]
        # Real SHAs for refs.
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(root), capture_output=True, text=True, check=True).stdout.strip()
        tree = subprocess.run(["git", "rev-parse", "HEAD^{tree}"], cwd=str(root), capture_output=True, text=True, check=True).stdout.strip()
        contract = core.contract_identity(root, cfg, chain["research_profile"], "WEEKLY_MAGAZINE" if chain["research_profile"] == "WEEKLY" else "LONGFORM_SPECIAL")
        tool_paths = [
            "scripts/survey_research_authority_v2.py",
            "scripts/survey_prearchitecture_acceptance_v2.py",
            "schemas/dm022-revision-request-v2.schema.json",
            "schemas/dm022-revision-manifest-v2.schema.json",
            "schemas/dm022-revision-proof-v2.schema.json",
            "schemas/dm022-preadoption-report-v2.schema.json",
            "schemas/dm022-supersession-checkpoint-v2.schema.json",
        ]
        tool_shas = [{"path": p, "sha256": _sha_file(root / p)} for p in tool_paths]
        state_doc = core.load_json(state_abs)
        state_rel = str(state_abs.relative_to(root))
        # Records: exact non-DROP Discovery IDs from real Discovery set.
        from scripts import survey_screening_v2 as screening_mod
        discoveries = screening_mod.read_jsonl(chain["discovery_path"])
        non_drop = []
        screening_doc = core.load_json(chain["screening_acceptance"])
        dec_map = {r["discovery_id"]: r["decision"] for r in screening_doc.get("decisions", [])}
        for disc in discoveries:
            if dec_map.get(disc["discovery_id"]) in ("KEEP", "MAYBE", "INSPECT"):
                non_drop.append(disc["discovery_id"])
        self.assertTrue(non_drop, "fixture must have non-DROP Discovery IDs")
        # For affected: use first non-DROP ID; records carry new claims for affected,
        # old-matching claims for unaffected (to keep unaffected byte-identical).
        # Load OLD cards to copy unaffected semantics.
        from scripts import survey_evidence_v2 as evidence_mod
        old_pkg = core.load_json(chain["package_path"])
        old_cards: dict[str, dict] = {}
        for meta in old_pkg.get("tasks", []):
            task_path = chain["package_path"].parent / meta["path"]
            task = core.load_json(task_path)
            # Card file is in results dir sibling? make_chain results are in
            # package-adjacent results? Actually make_evidence writes results to
            # package_path.parent/results/*.json with same basename as task.
            card_path = chain["package_path"].parent / "results" / Path(meta["path"]).name
            if card_path.is_file():
                old_cards[meta["evidence_task_id"]] = core.load_json(card_path)
        # Build interactive records: for each non-DROP discovery, status VERIFIED,
        # entity/MATERIAL etc. For affected, use new claim text + new rationale;
        # for unaffected, reuse OLD card-derived materiality/claims where possible.
        # To keep it REAL but simple, use status VERIFIED + MATERIAL for all,
        # with affected carrying new claim text.
        profile_doc = core.load_json(profile_path)
        records = []
        for did in sorted(non_drop):
            is_affected = did in affected
            claim_text = f"Synthetic revised claim for {did} ({revision_id})" if is_affected else f"Synthetic preserved claim for {did}"
            rec: dict[str, Any] = {
                "discovery_id": did,
                "status": "VERIFIED",
                "entity": {"entity_id": f"ent-{did}", "canonical_name": f"Entity {did}", "entity_type": "MODEL", "organization": "Synthetic Org", "canonical_url": None},
                "artifact_type": "MODEL",
                "claims": [{"text": claim_text, "evidence_class": "PRIMARY_FACT", "context": None}],
                "limitations": [],
                "verification": [{"target": "subject identity", "status": "VERIFIED", "finding": "synthetic verification"}],
                "materiality": "MATERIAL",
                "materiality_rationale": f"Synthetic revised rationale for {did}" if is_affected else f"Synthetic preserved rationale for {did}",
                "scope_dimensions": list(profile_doc["research_scope"]["scope_dimensions"][:1]),
            }
            if chain["research_profile"] == "WEEKLY":
                rec.update({"window_relation": "MAIN_EVENT", "carry_over": False})
            else:
                rec.update({"lineage_role": "CORE", "branch_ids": ["b1"], "transition_ids": ["t1"], "inheritance_note": None, "historical_attribution_caveat": None})
            records.append(rec)
        # Completeness: full 7-field obligations for Profile-initial union Discovery-named.
        initial = profile_doc["research_scope"]["initial_obligations"]
        obligations = []
        for init_row in initial:
            obligations.append({
                "obligation_id": init_row["obligation_id"],
                "dimension": init_row["dimension"],
                "description": init_row["description"],
                "status": "SATISFIED",
                "discovery_ids": sorted(non_drop)[:1],
                "evidence_task_ids": [],
                "rationale": f"Synthetic fixture satisfies {init_row['obligation_id']}",
            })
        for extra in extra_obligations:
            obligations.append(dict(extra))
        # Raw refs: create real Raw files with provenance (URL/fetched_at/SHA/bytes).
        raw_dir = root / "sources" / chain["issue_id"] / "raw-dm022"
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_refs = []
        for did in affected:
            # Raw bytes MUST carry the new card's claim text: prove binds each
            # affected card claim to its routed Raw file by content, not SHA only.
            raw_payload = (
                f"Synthetic raw bytes for {did} revision {revision_id}\n"
                f"URL: https://example.invalid/{did}\n"
                f"Claim: Synthetic revised claim for {did} ({revision_id})\n"
            ).encode()
            raw_path = raw_dir / f"{did}-{revision_id}.html"
            raw_path.write_bytes(raw_payload)
            rel = str(raw_path.relative_to(root))
            raw_refs.append({"path": rel, "sha256": hashlib.sha256(raw_payload).hexdigest(), "byte_count": len(raw_payload)})
        # before_checkpoint: current State provenance triplet (same record).
        prov = state_doc["checkpoint_provenance"]
        request = {
            "schema_version": "2.0-rc1",
            "issue_id": chain["issue_id"],
            "revision_id": revision_id,
            "research_profile": chain["research_profile"],
            "before_state": {"path": state_rel, "sha256": _sha_file(state_abs), "byte_count": state_abs.stat().st_size},
            "before_checkpoint": {"evidence": prov["evidence"], "materiality": prov["materiality"], "completeness": prov["completeness"]},
            "profile_ref": {"path": str(profile_path.relative_to(root)), "sha256": _sha_file(profile_path), "byte_count": profile_path.stat().st_size},
            "discovery_ref": {"path": str(chain["discovery_path"].relative_to(root)), "sha256": _sha_file(chain["discovery_path"]), "byte_count": chain["discovery_path"].stat().st_size},
            "screening_ref": {"path": str(chain["screening_acceptance"].relative_to(root)), "sha256": _sha_file(chain["screening_acceptance"]), "byte_count": chain["screening_acceptance"].stat().st_size},
            "work": {"expected_head": head, "expected_tree": tree},
            "affected_ids": sorted(affected),
            "supplement_manifest": None,
            "records": records,
            "completeness": {"obligations": obligations, "residual_limitations": [], "closure": {"expansion_passes": 1, "final_pass_new_sources": 0, "final_pass_new_material_obligations": 0, "final_pass_new_material_obligations_open": 0, "targeted_gap_fill_completed": True, "open_material_obligations": 0, "limitations": [], "status": "COMPLETE"} if chain["research_profile"] == "THEMATIC" else None},
            "runner": {"provider": "SYNTHETIC_FIXTURE_PROVIDER", "model": "SYNTHETIC_FIXTURE_MODEL_DM022_A2", "invocation": f"SYNTHETIC_FIXTURE_INVOCATION_{revision_id}", "generated_at": "2026-10-28T00:00:00Z"},
            "tool_pins": {"repository_commit_sha": head, "orchestrator_version": cfg["orchestrator_version"], "contract": contract, "tool_shas": tool_shas},
            "recorded_at": "2026-10-28T00:00:00Z",
            "executor": fix.SYNTHETIC_EXECUTOR,
        }
        request_path = root / "sources" / chain["issue_id"] / f"request-{revision_id}.json"
        _write(request_path, request)
        # Decision (external synthetic, validated at adopt; manifest_ref filled after prepare).
        decision_path = root / "sources" / chain["issue_id"] / f"decision-{revision_id}.json"
        return request_path, decision_path

    def _prepare_and_decide(self, chain: dict, state_abs: Path, revision_id: str, affected: list[str]):
        root: Path = chain["root"]
        request_path, decision_path = self._build_request_and_decision(chain, state_abs, revision_id, affected)
        # Prepare (no decision input).
        out = high.prepare_revision(root, state_abs, request_path, revision_id)
        self.assertIn("manifest_ref", out)
        manifest = core.load_json(root / out["manifest_ref"]["path"])
        # Build external decision binding the immutable manifest.
        state_doc = core.load_json(state_abs)
        decision = {
            "schema_version": "2.0-rc1",
            "issue_id": chain["issue_id"],
            "revision_id": revision_id,
            "manifest_ref": {"path": out["manifest_ref"]["path"], "sha256": out["manifest_ref"]["sha256"], "byte_count": out["manifest_ref"]["byte_count"]},
            "before_state": manifest["before_state"],
            "before_checkpoint": manifest["before_checkpoint"],
            "affected_ids": sorted(affected),
            "raw_refs": [],
            "allowlist": {"allowed_ids": sorted(affected), "basis": "Synthetic external research decision allows exactly the affected non-DROP IDs"},
            "assessment": {"interpretation": "Synthetic revised interpretation", "event_semantics": "Synthetic event semantics with preserved provenance", "provenance_check": "Synthetic raw bytes verified by SHA"},
            "reviewer": dict(fix.SYNTHETIC_REVIEWER),
            "recorded_at": "2026-10-28T00:00:00Z",
        }
        # Raw refs from request (real files).
        request_doc = core.load_json(request_path)
        # Re-derive raw refs: create them now (same as in request builder).
        raw_dir = root / "sources" / chain["issue_id"] / "raw-dm022"
        raw_refs = []
        for did in affected:
            raw_path = raw_dir / f"{did}-{revision_id}.html"
            raw = raw_path.read_bytes()
            raw_refs.append({"path": str(raw_path.relative_to(root)), "sha256": hashlib.sha256(raw).hexdigest(), "byte_count": len(raw)})
        decision["raw_refs"] = raw_refs
        _write(decision_path, decision)
        return out, request_path, decision_path

    def test_weekly_prepare_adopt_resume_readback(self) -> None:
        chain = self._chain_root("WEEKLY")
        state_abs = self._make_evidence_reviewed_state(chain)
        affected = ["target-source"]
        out, request_path, decision_path = self._prepare_and_decide(chain, state_abs, "rev-weekly-a2", affected)
        root: Path = chain["root"]
        rev_rel = out["revision_root"]
        # Adopt (real switch + clear + completion + release).
        adopted = high.adopt_revision(root, state_abs, root / rev_rel, decision_path)
        self.assertEqual(adopted.get("status"), "ADOPTED")
        self.assertTrue(adopted.get("guard_released"))
        # Readback (genuine-typed, no LIVE creation window).
        rb = high.readback_revision(root, state_abs, root / rev_rel)
        self.assertEqual(rb["research_acceptance"]["family"], "PREARCH")
        self.assertTrue(rb["research_acceptance"]["triplet"])
        # Resume after completion + guard release reports ALREADY_ACTIVE (no writes).
        resumed = high.resume_revision(root, state_abs, root / rev_rel)
        self.assertIn(resumed.get("status"), ("ALREADY_ACTIVE", "RESUME_CLEARED", "RESUME_ADOPTED"))
        # Checker (REQUIRED signature) passes on the adopted record.
        manifest = core.load_json(root / out["manifest_ref"]["path"])
        cp_rel = f"{rev_rel}/checkpoint/record.json"
        report_rel = f"{rev_rel}/proof/supersession-report.json"
        copy_rel = f"{rev_rel}/retention/state-before.json"
        errs = low.check_supersession_record_from_paths(root, root / cp_rel, root / report_rel, root / copy_rel)
        self.assertEqual(errs, [], f"checker must pass on adopted record: {errs}")
        # FULL completion verification passes on the adopted record too.
        cp_sha = hashlib.sha256((root / cp_rel).read_bytes()).hexdigest()
        low.require_completion_consistent(self._source_root_of(chain), {"path": cp_rel, "sha256": cp_sha})
        # Resolver returns 4 artifacts + artifact_refs (paths reloadable).
        resolved = low.resolve_research_authority(root, state_abs)
        self.assertEqual(resolved["family"], "PREARCH")
        self.assertEqual(sorted(resolved["artifacts"]), sorted(low.DM022_ARTIFACT_NAMES))
        self.assertEqual(sorted(resolved["artifact_refs"]), sorted(low.DM022_ARTIFACT_NAMES))

    def test_thematic_prepare_adopt_resume_readback(self) -> None:
        chain = self._chain_root("THEMATIC")
        state_abs = self._make_evidence_reviewed_state(chain)
        affected = ["target-source"]
        out, request_path, decision_path = self._prepare_and_decide(chain, state_abs, "rev-thematic-a2", affected)
        root: Path = chain["root"]
        rev_rel = out["revision_root"]
        adopted = high.adopt_revision(root, state_abs, root / rev_rel, decision_path)
        self.assertEqual(adopted.get("status"), "ADOPTED")
        rb = high.readback_revision(root, state_abs, root / rev_rel)
        self.assertEqual(rb["research_acceptance"]["family"], "PREARCH")
        resumed = high.resume_revision(root, state_abs, root / rev_rel)
        self.assertIn(resumed.get("status"), ("ALREADY_ACTIVE", "RESUME_CLEARED", "RESUME_ADOPTED"))
        cp_rel = f"{rev_rel}/checkpoint/record.json"
        report_rel = f"{rev_rel}/proof/supersession-report.json"
        copy_rel = f"{rev_rel}/retention/state-before.json"
        errs = low.check_supersession_record_from_paths(root, root / cp_rel, root / report_rel, root / copy_rel)
        self.assertEqual(errs, [], f"checker must pass: {errs}")

    def test_low_typed_loader_dispatch(self) -> None:
        chain = self._chain_root("WEEKLY")
        root: Path = chain["root"]
        # Legacy record (schema-valid, no kind): use ISSUE_INITIALIZED with
        # discovery-acceptance (satisfies issueInitializedArtifacts).
        leg_path = root / "leg-checkpoint.json"
        _write(leg_path, {
            "schema_version": "2.0-rc1", "issue_id": chain["issue_id"],
            "from_state": "ISSUE_INITIALIZED", "to_state": "DISCOVERY_COLLECTED",
            "checkpoints": ["discovery"], "recorded_at": "2026-10-28T00:00:00Z",
            "implementation": {"repository_commit_sha": "0" * 40, "orchestrator_version": "s"},
            "contract": {"pipeline_contract_version": "v", "pipeline_contract_sha256": "0" * 64, "quality_contract_version": "v", "quality_contract_sha256": "0" * 64, "research_profile_version": "v", "research_profile_sha256": "0" * 64, "publication_profile_version": "v", "publication_profile_sha256": "0" * 64},
            "artifacts": [{"name": "discovery-acceptance", "path": "disc.json", "sha256": "a" * 64}],
            "reviews": [{"check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC", "status": "PASS", "executor": "fixture", "evidence": "fixture", "result": {"path": "rep.json", "sha256": "b" * 64}}],
            "summary": "legacy",
        })
        got = low.load_typed_checkpoint_record(root, leg_path)
        self.assertEqual(got["family"], "LEGACY")
        self.assertTrue(low.is_legacy_candidates_record(got["record"]))
        self.assertFalse(low.is_prearchitecture_record(got["record"]))
        # Unknown kind refuses (real refusal from code, not test-raised).
        bad_path = root / "bad-kind.json"
        _write(bad_path, {"kind": "SOME_OTHER_KIND"})
        with self.assertRaises(low.ResearchAuthorityError):
            low.load_typed_checkpoint_record(root, bad_path)

    def test_loader_accepts_str_path_same_as_path(self) -> None:
        """Public loader normalizes Path|str: same valid CP, identical result."""
        chain = self._chain_root("WEEKLY")
        state_abs = self._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        out, _, decision_path = self._prepare_and_decide(chain, state_abs, "rev-strpath-a4", ["target-source"])
        rev_rel = out["revision_root"]
        self.assertEqual(high.adopt_revision(root, state_abs, root / rev_rel, decision_path).get("status"), "ADOPTED")
        cp_rel = f"{rev_rel}/checkpoint/record.json"
        via_path = low.load_typed_checkpoint_record(root, root / cp_rel)
        via_str = low.load_typed_checkpoint_record(root, cp_rel)
        self.assertEqual(via_str["family"], "PREARCH")
        self.assertEqual(via_str, via_path)
        # Resolver accepts a str state path too and returns the same authority.
        resolved_str = low.resolve_research_authority(root, str(state_abs))
        resolved_path = low.resolve_research_authority(root, state_abs)
        self.assertEqual(resolved_str["family"], "PREARCH")
        self.assertEqual(resolved_str["checkpoint"], resolved_path["checkpoint"])
        self.assertEqual(resolved_str["artifact_refs"], resolved_path["artifact_refs"])
        # Checker accepts all-str paths and passes on the adopted record.
        errs = low.check_supersession_record_from_paths(
            root, cp_rel,
            f"{rev_rel}/proof/supersession-report.json",
            f"{rev_rel}/retention/state-before.json")
        self.assertEqual(errs, [], f"checker must pass with str paths: {errs}")

    def test_loader_wrong_family_str_path(self) -> None:
        """A legacy checkpoint path (str or Path) classifies LEGACY, never PREARCH."""
        chain = self._chain_root("WEEKLY")
        root: Path = chain["root"]
        leg_rel = "leg-checkpoint.json"
        _write(root / leg_rel, {
            "schema_version": "2.0-rc1", "issue_id": chain["issue_id"],
            "from_state": "ISSUE_INITIALIZED", "to_state": "DISCOVERY_COLLECTED",
            "checkpoints": ["discovery"], "recorded_at": "2026-10-28T00:00:00Z",
            "implementation": {"repository_commit_sha": "0" * 40, "orchestrator_version": "s"},
            "contract": {"pipeline_contract_version": "v", "pipeline_contract_sha256": "0" * 64, "quality_contract_version": "v", "quality_contract_sha256": "0" * 64, "research_profile_version": "v", "research_profile_sha256": "0" * 64, "publication_profile_version": "v", "publication_profile_sha256": "0" * 64},
            "artifacts": [{"name": "discovery-acceptance", "path": "disc.json", "sha256": "a" * 64}],
            "reviews": [{"check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC", "status": "PASS", "executor": "fixture", "evidence": "fixture", "result": {"path": "rep.json", "sha256": "b" * 64}}],
            "summary": "legacy",
        })
        for probe in (root / leg_rel, leg_rel):
            got = low.load_typed_checkpoint_record(root, probe)
            self.assertEqual(got["family"], "LEGACY")
            self.assertTrue(low.is_legacy_candidates_record(got["record"]))
            self.assertFalse(low.is_prearchitecture_record(got["record"]))
        # Unknown kind as str still raises the typed refusal, not AttributeError.
        bad_path = root / "bad-kind.json"
        _write(bad_path, {"kind": "SOME_OTHER_KIND"})
        with self.assertRaises(low.ResearchAuthorityError):
            low.load_typed_checkpoint_record(root, "bad-kind.json")

    def test_low_guard_and_slots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src"
            src.mkdir(parents=True)
            low.require_no_active_guard(src)
            guard = low.guard_path_for(src)
            guard.parent.mkdir(parents=True, exist_ok=True)
            guard.write_bytes(b"{}")
            with self.assertRaises(low.ResearchAuthorityError):
                low.require_no_active_guard(src)
            obs = low.lstat_slot(src, "candidate-matrix-v2.json")
            self.assertFalse(obs["present"])

    def test_high_cli_prepare_adopt(self) -> None:
        chain = self._chain_root("WEEKLY")
        state_abs = self._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        request_path, _ = self._build_request_and_decision(chain, state_abs, "rev-cli-a2", ["target-source"])
        # Real CLI prepare (four operations exist; exercise prepare via CLI).
        proc = subprocess.run(
            [sys.executable, "-m", "scripts.survey_prearchitecture_acceptance_v2", "prepare",
             "--repo-root", str(root), "--state-path", str(state_abs),
             "--request-path", str(request_path), "--revision-id", "rev-cli-a2"],
            cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=300,
        )
        self.assertEqual(proc.returncode, 0, f"CLI prepare must succeed: {proc.stderr}")

    # ---------- A3 fault/lifecycle suite (B8: meaningful actual fault tests) ----------

    def _source_root_of(self, chain: dict) -> Path:
        profile_doc = core.load_json(chain["profile_path"])
        return chain["root"] / profile_doc["paths"]["source_root"]

    def test_raw_binding_refuses_unbound_claim(self) -> None:
        """Affected card whose claim text appears in NO routed Raw file refuses."""
        chain = self._chain_root("WEEKLY")
        state_abs = self._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        out, request_path, decision_path = self._prepare_and_decide(chain, state_abs, "rev-rawbind-a3", ["target-source"])
        # Break the content binding only: rewrite the routed Raw file so it no
        # longer carries the NEW card's claim text (SHA changes with it).
        raw_path = root / "sources" / chain["issue_id"] / "raw-dm022" / "target-source-rev-rawbind-a3.html"
        self.assertTrue(raw_path.is_file())
        raw_path.write_bytes(b"unrelated bytes with no claim text\n")
        decision = core.load_json(decision_path)
        for ref in decision.get("raw_refs", []):
            if ref["path"].endswith("target-source-rev-rawbind-a3.html"):
                ref["sha256"] = hashlib.sha256(raw_path.read_bytes()).hexdigest()
                ref["byte_count"] = len(raw_path.read_bytes())
        _write(decision_path, decision)
        with self.assertRaisesRegex(low.ResearchAuthorityError, "bind no supplied Raw bytes"):
            high.adopt_revision(root, state_abs, root / out["revision_root"], decision_path)
        # Refusal is pre-guard: guard absent, LIVE still before (no writes).
        source_root = self._source_root_of(chain)
        low.require_no_active_guard(source_root)
        manifest = core.load_json(root / out["manifest_ref"]["path"])
        self.assertEqual(hashlib.sha256(state_abs.read_bytes()).hexdigest(), manifest["before_state"]["sha256"])

    def test_late_final_plant_blocks_and_resume_recovers(self) -> None:
        """Late-planted checkpoint final refuses atomically; resume adopts."""
        from scripts import survey_agent_control_v2 as agent

        chain = self._chain_root("WEEKLY")
        state_abs = self._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        out, request_path, decision_path = self._prepare_and_decide(chain, state_abs, "rev-lateplant-a3", ["target-source"])
        rev_rel = out["revision_root"]
        cp_path = root / rev_rel / "checkpoint" / "record.json"
        cp_path.parent.mkdir(parents=True, exist_ok=True)
        plant = b'{"foreign": true}\n'
        cp_path.write_bytes(plant)
        with self.assertRaisesRegex(high.AcceptanceError, "already exists with different bytes"):
            high.adopt_revision(root, state_abs, root / rev_rel, decision_path)
        # Guard held by the interrupted attempt; LIVE still before; plant intact.
        source_root = self._source_root_of(chain)
        with self.assertRaises(low.ResearchAuthorityError):
            low.require_no_active_guard(source_root)
        manifest = core.load_json(root / out["manifest_ref"]["path"])
        self.assertEqual(hashlib.sha256(state_abs.read_bytes()).hexdigest(), manifest["before_state"]["sha256"])
        self.assertEqual(cp_path.read_bytes(), plant)
        # Guard-held diagnostics still work: detached readback + agent validation.
        rb = high.readback_revision(root, state_abs, root / rev_rel)
        self.assertEqual(rb["research_acceptance"]["family"], "LEGACY")
        self.assertEqual(agent.validate_agent_state(root, chain["cfg"], core.load_json(state_abs)), [])
        # Operator removes ONLY the foreign plant (retained COPY untouched).
        cp_path.unlink()
        resumed = high.resume_revision(root, state_abs, root / rev_rel)
        self.assertEqual(resumed.get("status"), "RESUME_ADOPTED")
        self.assertEqual(hashlib.sha256(state_abs.read_bytes()).hexdigest(), resumed["expected_after_state_sha256"])
        for slot in low.SEVEN_SLOTS:
            self.assertFalse((source_root / slot).exists(), f"slot not cleared: {slot}")
        cp_sha = hashlib.sha256((root / rev_rel / "checkpoint" / "record.json").read_bytes()).hexdigest()
        low.require_completion_consistent(source_root, {"path": f"{rev_rel}/checkpoint/record.json", "sha256": cp_sha})
        low.require_no_active_guard(source_root)

    def test_completion_tamper_refuses_and_resume_indeterminate(self) -> None:
        """Tampered completion is unverifiable; resume reports INDETERMINATE."""
        for tamper in ("checkpointsha", "disposition", "expectedafter"):
            with self.subTest(tamper=tamper):
                chain = self._chain_root("WEEKLY")
                state_abs = self._make_evidence_reviewed_state(chain)
                root: Path = chain["root"]
                out, request_path, decision_path = self._prepare_and_decide(chain, state_abs, f"rev-tamper-{tamper}-a4", ["target-source"])
                rev_rel = out["revision_root"]
                adopted = high.adopt_revision(root, state_abs, root / rev_rel, decision_path)
                self.assertEqual(adopted.get("status"), "ADOPTED")
                source_root = self._source_root_of(chain)
                cp_path = root / rev_rel / "checkpoint" / "record.json"
                cp_sha = hashlib.sha256(cp_path.read_bytes()).hexdigest()
                completion_abs = root / rev_rel / "completion" / "cleanup-completion.json"
                comp = core.load_json(completion_abs)
                if tamper == "checkpoint_sha":
                    comp["checkpoint"]["sha256"] = "0" * 64
                elif tamper == "disposition":
                    comp["seven_plan"][0]["disposition"] = "absent_legitimate" if comp["seven_plan"][0]["disposition"] == "cleared" else "cleared"
                else:
                    comp["expected_after_state"]["sha256"] = "f" * 64
                completion_abs.write_bytes(core.json_bytes(comp))
                with self.assertRaises(low.ResearchAuthorityError):
                    low.require_completion_consistent(source_root, {"path": f"{rev_rel}/checkpoint/record.json", "sha256": cp_sha})
                resumed = high.resume_revision(root, state_abs, root / rev_rel)
                self.assertEqual(resumed.get("status"), "INDETERMINATE")

    def test_absent_slot_regeneration_ready_and_readback(self) -> None:
        """Legit post-completion regeneration (incl. old-absent slots) passes READY."""
        from scripts import survey_agent_control_v2 as agent

        chain = self._chain_root("WEEKLY")
        state_abs = self._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        out, request_path, decision_path = self._prepare_and_decide(chain, state_abs, "rev-regen-a3", ["target-source"])
        rev_rel = out["revision_root"]
        adopted = high.adopt_revision(root, state_abs, root / rev_rel, decision_path)
        self.assertEqual(adopted.get("status"), "ADOPTED")
        source_root = self._source_root_of(chain)
        for row in adopted.get("seven_plan", []):
            self.assertEqual(row.get("disposition"), "absent_legitimate")
        # Normal runner regenerates outputs, including previously absent slots.
        for rel in ("candidate-matrix-v2.json", "orchestration/v2/interactive/selection-architecture-input.json"):
            p = source_root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((json.dumps({"regenerated": True, "slot": rel}, sort_keys=True) + "\n").encode())
        # READY must NOT reapply the old absence window after valid completion.
        # (Agent validation of the adopted PREARCH state is B-owned; A scope
        # asserts LOW readiness + detached readback here.)
        low.require_research_operation_ready(root, state_abs)
        rb = high.readback_revision(root, state_abs, root / rev_rel)
        self.assertEqual(rb["research_acceptance"]["family"], "PREARCH")
        self.assertTrue(rb["research_acceptance"]["triplet"])

    def test_repeat_correction_preserves_original_anchor_both_routes(self) -> None:
        """Real repeat correction (both routes): anchor carried, supersedes appends."""
        for profile in ("WEEKLY", "THEMATIC"):
            with self.subTest(profile=profile):
                chain = self._chain_root(profile)
                state_abs = self._make_evidence_reviewed_state(chain)
                root: Path = chain["root"]
                rev1_id = f"rev-repeat1-{profile.lower()}-a4"
                out1, _, decision_path1 = self._prepare_and_decide(chain, state_abs, rev1_id, ["target-source"])
                rev1 = out1["revision_root"]
                self.assertEqual(high.adopt_revision(root, state_abs, root / rev1, decision_path1).get("status"), "ADOPTED")
                cp1 = core.load_json(root / rev1 / "checkpoint" / "record.json")
                # Per-file manifest bindings are non-empty and resolve to real bytes.
                manifest1 = core.load_json(root / out1["manifest_ref"]["path"])
                for key in ("tasks", "cards", "views"):
                    refs = manifest1["candidate_outputs"][key]
                    self.assertTrue(isinstance(refs, list) and len(refs) > 0, f"manifest {key} must bind per-file refs")
                    for ref in refs:
                        raw = (root / ref["path"]).read_bytes()
                        self.assertEqual(hashlib.sha256(raw).hexdigest(), ref["sha256"])
                        self.assertEqual(len(raw), ref["byte_count"])
                proof1 = core.load_json(root / rev1 / "proof" / "proposed-graph-proof.json")
                self.assertTrue(any(m.get("field_path") == "evidence-package.sha256" for m in proof1["unaffected_comparison"]["mechanical_projections"]))
                rev2_id = f"rev-repeat2-{profile.lower()}-a4"
                out2, _, decision_path2 = self._prepare_and_decide(chain, state_abs, rev2_id, ["target-source"])
                rev2 = out2["revision_root"]
                adopted2 = high.adopt_revision(root, state_abs, root / rev2, decision_path2)
                self.assertEqual(adopted2.get("status"), "ADOPTED")
                self.assertTrue(adopted2.get("guard_released"))
                cp2 = core.load_json(root / rev2 / "checkpoint" / "record.json")
                # Lineage refs bind checkpoint FILE bytes (ArtifactRef), not the
                # internal self-digest field.
                rev1_file_sha = hashlib.sha256((root / rev1 / "checkpoint" / "record.json").read_bytes()).hexdigest()
                self.assertEqual(cp2["parent_checkpoint"], {"path": f"{rev1}/checkpoint/record.json", "sha256": rev1_file_sha})
                self.assertEqual(cp2["original_anchor"], cp1["original_anchor"])
                self.assertIn({"path": f"{rev1}/checkpoint/record.json", "sha256": rev1_file_sha, "revision_id": rev1_id}, cp2["supersedes"])
                # Resolver + checker accept the second-generation record too.
                resolved = low.resolve_research_authority(root, state_abs)
                self.assertEqual(resolved["family"], "PREARCH")
                self.assertEqual(resolved["checkpoint"]["revision_id"], rev2_id)
                errs = low.check_supersession_record_from_paths(
                    root, root / rev2 / "checkpoint" / "record.json",
                    root / rev2 / "proof" / "supersession-report.json",
                    root / rev2 / "retention" / "state-before.json")
                self.assertEqual(errs, [], f"checker must pass on repeat record: {errs}")

    def test_malformed_review_result_refuses(self) -> None:
        """Genuinely malformed SizedRef review result is refused (SELF binds it)."""
        chain = self._chain_root("WEEKLY")
        state_abs = self._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        out, _, decision_path = self._prepare_and_decide(chain, state_abs, "rev-malformed-a4", ["target-source"])
        rev_rel = out["revision_root"]
        self.assertEqual(high.adopt_revision(root, state_abs, root / rev_rel, decision_path).get("status"), "ADOPTED")
        bad = core.load_json(root / rev_rel / "checkpoint" / "record.json")
        bad["reviews"][0]["result"]["sha256"] = "0" * 64
        bad_path = root / "tampered-checkpoint.json"
        _write(bad_path, bad)
        with self.assertRaises(low.ResearchAuthorityError):
            low.load_typed_checkpoint_record(root, bad_path)

    def test_stale_and_unsupported_inputs_refuse(self) -> None:
        # (a) stale HEAD: commit after prepare, adopt must refuse the stale pin.
        chain = self._chain_root("WEEKLY")
        state_abs = self._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        out, request_path, decision_path = self._prepare_and_decide(chain, state_abs, "rev-stalehead-a3", ["target-source"])
        (root / "stale-note.txt").write_text("stale head\n", encoding="utf-8")
        self._fixture_commit(root, "stale HEAD fixture change")
        with self.assertRaisesRegex(high.AcceptanceError, "HEAD/tree moved"):
            high.adopt_revision(root, state_abs, root / out["revision_root"], decision_path)
        source_root = self._source_root_of(chain)
        low.require_no_active_guard(source_root)
        # (b) tampered decision manifest binding.
        chain_b = self._chain_root("WEEKLY")
        state_b = self._make_evidence_reviewed_state(chain_b)
        root_b: Path = chain_b["root"]
        out_b, req_b, dec_b = self._prepare_and_decide(chain_b, state_b, "rev-staledec-a3", ["target-source"])
        dec_doc = core.load_json(dec_b)
        dec_doc["manifest_ref"]["sha256"] = "1" * 64
        _write(dec_b, dec_doc)
        with self.assertRaisesRegex(high.AcceptanceError, "manifest_ref"):
            high.adopt_revision(root_b, state_b, root_b / out_b["revision_root"], dec_b)
        # (c) unsupported profile: RETROSPECTIVE_PERIOD is not a DM022 route.
        chain_c = self._chain_root("WEEKLY")
        state_c = self._make_evidence_reviewed_state(chain_c)
        root_c: Path = chain_c["root"]
        req_c_path, _ = self._build_request_and_decision(chain_c, state_c, "rev-badprof-a3", ["target-source"])
        req_doc = core.load_json(req_c_path)
        req_doc["research_profile"] = "RETROSPECTIVE_PERIOD"
        _write(req_c_path, req_doc)
        with self.assertRaises(Exception):
            high.prepare_revision(root_c, state_c, req_c_path, "rev-badprof-a3")
        # (d) named Discovery obligation omitted from the request union.
        chain_d = self._chain_root("WEEKLY", named_obligations=("OBL_NAMED_X",))
        state_d = self._make_evidence_reviewed_state(chain_d)
        root_d: Path = chain_d["root"]
        req_d_path, _ = self._build_request_and_decision(chain_d, state_d, "rev-namedgap-a3", ["target-source"])
        with self.assertRaisesRegex(low.ResearchAuthorityError, "union"):
            high.prepare_revision(root_d, state_d, req_d_path, "rev-namedgap-a3")

    def test_named_obligation_complete_row_passes(self) -> None:
        """Explicit full named-obligation row satisfies the Profile+named union."""
        chain = self._chain_root("WEEKLY", named_obligations=("OBL_NAMED_X",))
        state_abs = self._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        profile_doc = core.load_json(chain["profile_path"])
        dims = list(profile_doc["research_scope"]["scope_dimensions"])
        extra = [{
            "obligation_id": "OBL_NAMED_X",
            "dimension": dims[0],
            "description": "Named fixture obligation declared by Discovery provenance",
            "status": "SATISFIED",
            "discovery_ids": ["target-source"],
            "evidence_task_ids": [],
            "rationale": "Synthetic fixture satisfies the named obligation",
        }]
        request_path, _ = self._build_request_and_decision(chain, state_abs, "rev-namedok-a3", ["target-source"], extra_obligations=extra)
        out = high.prepare_revision(root, state_abs, request_path, "rev-namedok-a3")
        self.assertIn("manifest_ref", out)

    def test_interrupted_clear_resume_cleared(self) -> None:
        """E-state + guard-held interrupt at clearing resumes to RESUME_CLEARED."""
        if os.geteuid() == 0:
            self.skipTest("ownership/permission faults need a non-root user")
        from scripts import survey_agent_control_v2 as agent

        chain = self._chain_root("WEEKLY")
        state_abs = self._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        source_root = self._source_root_of(chain)
        slot_rel = "orchestration/v2/interactive/selection-architecture-input.json"
        slot_abs = source_root / slot_rel
        slot_abs.parent.mkdir(parents=True, exist_ok=True)
        slot_abs.write_bytes(b'{"stale": "output"}\n')
        out, request_path, decision_path = self._prepare_and_decide(chain, state_abs, "rev-interrupt-a3", ["target-source"])
        rev_rel = out["revision_root"]
        os.chmod(slot_abs.parent, 0o555)
        try:
            with self.assertRaises(high.AcceptanceError):
                high.adopt_revision(root, state_abs, root / rev_rel, decision_path)
        finally:
            os.chmod(slot_abs.parent, 0o755)
        # Interrupted with state already switched and guard held.
        manifest = core.load_json(root / out["manifest_ref"]["path"])
        self.assertNotEqual(hashlib.sha256(state_abs.read_bytes()).hexdigest(), manifest["before_state"]["sha256"])
        with self.assertRaises(low.ResearchAuthorityError):
            low.require_no_active_guard(source_root)
        self.assertTrue(slot_abs.is_file())
        # Guard-held diagnostics still work while blocked: detached readback
        # does not require READY/guard-absence. (Agent validation of the
        # adopted PREARCH triplet is B-owned; see the result-authority pin.)
        rb = high.readback_revision(root, state_abs, root / rev_rel)
        self.assertEqual(rb["research_acceptance"]["family"], "PREARCH")
        self.assertTrue(rb["research_acceptance"]["triplet"])
        resumed = high.resume_revision(root, state_abs, root / rev_rel)
        self.assertEqual(resumed.get("status"), "RESUME_CLEARED")
        self.assertFalse(slot_abs.exists())
        low.require_no_active_guard(source_root)

    def test_unknown_live_resume_indeterminate(self) -> None:
        """Unrecognized LIVE bytes yield INDETERMINATE with records preserved."""
        chain = self._chain_root("WEEKLY")
        state_abs = self._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        out, request_path, decision_path = self._prepare_and_decide(chain, state_abs, "rev-unknown-a3", ["target-source"])
        rev_rel = out["revision_root"]
        self.assertEqual(high.adopt_revision(root, state_abs, root / rev_rel, decision_path).get("status"), "ADOPTED")
        state_abs.write_bytes(b"not json{{")
        resumed = high.resume_revision(root, state_abs, root / rev_rel)
        self.assertEqual(resumed.get("status"), "INDETERMINATE")
        self.assertIn("live_sha256", resumed)
        # Guard already released; retained records preserved, nothing deleted.
        source_root = self._source_root_of(chain)
        low.require_no_active_guard(source_root)
        self.assertTrue((root / rev_rel / "retention" / "state-before.json").is_file())
        self.assertTrue((root / rev_rel / "revision-manifest.json").is_file())

    def test_slot_ownership_faults(self) -> None:
        """Unreadable slots fail closed; same-byte new-inode plants refuse."""
        if os.geteuid() == 0:
            self.skipTest("ownership/permission faults need a non-root user")
        chain = self._chain_root("WEEKLY")
        state_abs = self._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        source_root = self._source_root_of(chain)
        slot_abs = source_root / "candidate-matrix-v2.json"
        slot_abs.write_bytes(b'{"slot": "output"}\n')
        out, request_path, decision_path = self._prepare_and_decide(chain, state_abs, "rev-owner-a3", ["target-source"])
        rev_rel = out["revision_root"]
        # (a) unreadable retained slot refuses before any guard claim.
        os.chmod(slot_abs, 0o000)
        try:
            with self.assertRaises(high.AcceptanceError):
                high.adopt_revision(root, state_abs, root / rev_rel, decision_path)
        finally:
            os.chmod(slot_abs, 0o644)
        low.require_no_active_guard(source_root)
        # (b) same-byte replacement (new inode) is foreign: refuse, guard held.
        saved = slot_abs.read_bytes()
        slot_abs.unlink()
        slot_abs.write_bytes(saved)
        self.assertNotEqual(os.lstat(slot_abs).st_ino, core.load_json(root / out["manifest_ref"]["path"])["retention_snapshots"][0]["source_ino"])
        with self.assertRaisesRegex(high.AcceptanceError, "inode changed"):
            high.adopt_revision(root, state_abs, root / rev_rel, decision_path)
        with self.assertRaises(low.ResearchAuthorityError):
            low.require_no_active_guard(source_root)
        # Operator removes the foreign plant; explicit resume finishes honestly
        # (state already switched, so the E+guard-held path clears+completes).
        slot_abs.unlink()
        resumed = high.resume_revision(root, state_abs, root / rev_rel)
        self.assertEqual(resumed.get("status"), "RESUME_CLEARED")
        low.require_no_active_guard(source_root)

    def test_replace_tmp_exists_refuses(self) -> None:
        """Pre-created State temp file refuses the switch (no silent replace)."""
        chain = self._chain_root("WEEKLY")
        state_abs = self._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        out, request_path, decision_path = self._prepare_and_decide(chain, state_abs, "rev-tmpplant-a3", ["target-source"])
        rev_rel = out["revision_root"]
        cp_path = root / rev_rel / "checkpoint" / "record.json"
        cp_path.parent.mkdir(parents=True, exist_ok=True)
        cp_path.write_bytes(b'{"foreign": true}\n')
        with self.assertRaisesRegex(high.AcceptanceError, "already exists with different bytes"):
            high.adopt_revision(root, state_abs, root / rev_rel, decision_path)
        # Guard held by the interrupted attempt; clear the checkpoint plant so
        # the resume reaches the State switch, then plant the State temp path
        # derived from the real guard nonce and prove the switch refuses it.
        cp_path.unlink()
        guard_abs = self._source_root_of(chain) / "orchestration/v2/acceptance-revision.guard.json"
        guard_doc = core.load_json(guard_abs)
        tmp_state = state_abs.with_name(state_abs.name + f".tmp.{guard_doc['attempt_nonce']}")
        tmp_state.write_bytes(b"planted temp\n")
        try:
            with self.assertRaisesRegex(high.AcceptanceError, "temp State already exists"):
                high.resume_revision(root, state_abs, root / rev_rel)
        finally:
            tmp_state.unlink(missing_ok=True)
        # Resume to a real adoption once the temp plant is gone.
        resumed = high.resume_revision(root, state_abs, root / rev_rel)
        self.assertEqual(resumed.get("status"), "RESUME_ADOPTED")

    def test_completion_idempotent_reuse(self) -> None:
        """Existing completion with identical intent is reused, never rewritten."""
        chain = self._chain_root("WEEKLY")
        state_abs = self._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        out, request_path, decision_path = self._prepare_and_decide(chain, state_abs, "rev-idem-a3", ["target-source"])
        rev_rel = out["revision_root"]
        self.assertEqual(high.adopt_revision(root, state_abs, root / rev_rel, decision_path).get("status"), "ADOPTED")
        completion_abs = root / rev_rel / "completion" / "cleanup-completion.json"
        before_bytes = completion_abs.read_bytes()
        manifest = core.load_json(root / out["manifest_ref"]["path"])
        source_root = self._source_root_of(chain)
        # Reconstructed narrow-oracle context with the REAL stored pieces; the
        # guard below is synthetic (post-release) and only its nonce is read.
        completion = core.load_json(completion_abs)
        live_sha = hashlib.sha256(state_abs.read_bytes()).hexdigest()
        bound = {
            "repo_root": str(root), "state_path": str(state_abs), "rev_root": str(root / rev_rel),
            "source_root": str(source_root), "planned_bytes": b"", "expected_raw": b"",
            "expected_sha": live_sha,
            "retention": core.load_json(root / rev_rel / "retention" / "inventory.json"),
            "manifest": manifest,
            "guard": {"attempt_nonce": completion["attempt_nonce"]},
            "seven_plan": completion["seven_plan"],
        }
        result = high.write_cleanup_completion(bound)
        self.assertTrue(result.get("idempotent"))
        self.assertEqual(completion_abs.read_bytes(), before_bytes)

    def test_prepare_refuses_prior_request_changes_history(self) -> None:
        """Valid prior REQUEST_CHANGES history refuses entry before any R/COPY write.

        All seven slots absent + pending/null current Gate, yet a genuine
        prior Human Gate review (REQUEST_CHANGES, schema-valid index+record)
        exists: prepare must refuse with the prior-Human-review error BEFORE
        creating the revision directory, copying retained state, or claiming
        the guard. State bytes must be unchanged.
        """
        chain = self._chain_root("WEEKLY")
        state_abs = self._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        history = self._write_prior_human_review(chain, state_abs)
        self.assertTrue(history["record"].is_file() and history["index"].is_file())
        state_before = state_abs.read_bytes()
        request_path, _ = self._build_request_and_decision(chain, state_abs, "rev-humanwin-a4", ["target-source"])
        with self.assertRaisesRegex(high.AcceptanceError, "prior Human"):
            high.prepare_revision(root, state_abs, request_path, "rev-humanwin-a4")
        profile_doc = core.load_json(chain["profile_path"])
        rev_root = root / profile_doc["paths"]["source_root"] / "research" / "v2" / "acceptance-revisions" / "rev-humanwin-a4"
        self.assertFalse(rev_root.exists(), "no revision dir may be created on refused entry")
        self.assertEqual(state_abs.read_bytes(), state_before, "LIVE state bytes must be unchanged")
        low.require_no_active_guard(self._source_root_of(chain))

    def test_adopt_refuses_late_human_review(self) -> None:
        """A review recorded between prepare and adopt refuses adoption pre-guard."""
        chain = self._chain_root("WEEKLY")
        state_abs = self._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        out, request_path, decision_path = self._prepare_and_decide(chain, state_abs, "rev-latehuman-a4", ["target-source"])
        rev_rel = out["revision_root"]
        manifest = core.load_json(root / out["manifest_ref"]["path"])
        # Human review lands after inert preparation, before adoption.
        history = self._write_prior_human_review(chain, state_abs)
        self.assertTrue(history["record"].is_file() and history["index"].is_file())
        with self.assertRaisesRegex(high.AcceptanceError, "prior Human"):
            high.adopt_revision(root, state_abs, root / rev_rel, decision_path)
        # Refused before any guard claim, checkpoint/State mutation, or R proof write.
        low.require_no_active_guard(self._source_root_of(chain))
        self.assertEqual(hashlib.sha256(state_abs.read_bytes()).hexdigest(), manifest["before_state"]["sha256"])
        self.assertFalse((root / rev_rel / "checkpoint" / "record.json").exists())
        self.assertFalse((root / rev_rel / "proof" / "proposed-graph-proof.json").exists())

    def test_explicit_empty_index_allows_prepare(self) -> None:
        """A genuinely empty valid index is eligible (absence is not approval)."""
        chain = self._chain_root("WEEKLY")
        state_abs = self._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        profile_doc = core.load_json(chain["profile_path"])
        source_root = root / profile_doc["paths"]["source_root"]
        cfg = chain["cfg"]
        index_abs = source_root / cfg["state_authority"]["human_review_index_path"]
        index_abs.parent.mkdir(parents=True, exist_ok=True)
        empty_index = {"schema_version": "2.0-rc1", "issue_id": chain["issue_id"], "reviews": []}
        from scripts import survey_schema_v2 as schema_gate

        schema_gate.validate_instance(empty_index, root / "schemas/human-gate-review-index-v2.schema.json", label="fixture empty review index")
        _write(index_abs, empty_index)
        out, _, decision_path = self._prepare_and_decide(chain, state_abs, "rev-emptyidx-a4", ["target-source"])
        rev_rel = out["revision_root"]
        self.assertTrue((root / rev_rel / "revision-manifest.json").is_file())
        adopted = high.adopt_revision(root, state_abs, root / rev_rel, decision_path)
        self.assertEqual(adopted.get("status"), "ADOPTED")

    def test_arch_gate_readback_after_adopt(self) -> None:
        """Adopted record stays readable after a normal Human Gate approval.

        The creation-window predicate must not reapply on readback/READY:
        after recording a genuine APPROVED ARCHITECTURE_REVIEW (index + record
        + approval binding, state gates updated), the adopted PREARCH record
        still resolves with its triplet, and normal-writer readiness still
        passes. No LIVE recreation, no window re-imposition.
        """
        chain = self._chain_root("WEEKLY")
        state_abs = self._make_evidence_reviewed_state(chain)
        root: Path = chain["root"]
        out, _, decision_path = self._prepare_and_decide(chain, state_abs, "rev-archread-a4", ["target-source"])
        rev_rel = out["revision_root"]
        self.assertEqual(high.adopt_revision(root, state_abs, root / rev_rel, decision_path).get("status"), "ADOPTED")
        # Normal forward Human Gate: APPROVED ARCHITECTURE_REVIEW with a real
        # approval file, bound index entry, and updated gate state.
        profile_doc = core.load_json(chain["profile_path"])
        source_root = root / profile_doc["paths"]["source_root"]
        cfg = chain["cfg"]
        approval_abs = source_root / cfg["state_authority"]["architecture_approval_path"]
        approval_abs.parent.mkdir(parents=True, exist_ok=True)
        approval_abs.write_bytes((json.dumps({"approval": "synthetic-human-approval", "issue_id": chain["issue_id"]}, sort_keys=True) + "\n").encode())
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(root), check=True, capture_output=True, text=True, timeout=120).stdout.strip()
        reviewed_state = {"path": str(state_abs.relative_to(root)), "sha256": _sha_file(state_abs)}
        record = {
            "schema_version": "2.0-rc1",
            "review_id": f"review:{chain['issue_id']}:architecture:r1:{core.sha256_object({'issue_id': chain['issue_id'], 'gate': 'ARCHITECTURE_REVIEW', 'revision': 1, 'decision': 'APPROVED'})[:16]}",
            "issue_id": chain["issue_id"],
            "gate": "ARCHITECTURE_REVIEW",
            "revision": 1,
            "decision": "APPROVED",
            "reviewed_state": reviewed_state,
            "reviewed_artifacts": [{"name": "production-profile", "path": str(chain["profile_path"].relative_to(root)), "sha256": _sha_file(chain["profile_path"])}],
            "reviewed_repository_commit_sha": head,
            "reviewed_by": "Synthetic Human Reviewer",
            "reviewed_at": "2026-10-28T00:00:00Z",
            "review_reference": "synthetic-human-approval-r1",
            "requested_changes": None,
            "regeneration_boundary": None,
            "approval": {"path": str(approval_abs.relative_to(root)), "sha256": hashlib.sha256(approval_abs.read_bytes()).hexdigest()},
        }
        from scripts import survey_schema_v2 as schema_gate

        schema_gate.validate_instance(record, root / "schemas/human-gate-review-record-v2.schema.json", label="fixture approval record")
        record_abs = source_root / "gates" / "reviews" / "architecture-r1.json"
        record_abs.parent.mkdir(parents=True, exist_ok=True)
        self.assertFalse(record_abs.exists())
        _write(record_abs, record)
        index_abs = source_root / cfg["state_authority"]["human_review_index_path"]
        index = {
            "schema_version": "2.0-rc1",
            "issue_id": chain["issue_id"],
            "reviews": [{
                "gate": "ARCHITECTURE_REVIEW",
                "revision": 1,
                "decision": "APPROVED",
                "record": {"path": str(record_abs.relative_to(root)), "sha256": hashlib.sha256(record_abs.read_bytes()).hexdigest()},
            }],
        }
        schema_gate.validate_instance(index, root / "schemas/human-gate-review-index-v2.schema.json", label="fixture approval index")
        self.assertFalse(index_abs.exists())
        index_abs.parent.mkdir(parents=True, exist_ok=True)
        _write(index_abs, index)
        state_doc = core.load_json(state_abs)
        state_doc["human_gates"] = {"architecture_review": "approved", "publication_preview": "pending"}
        state_doc["human_gate_provenance"] = {"architecture_review": {"path": str(approval_abs.relative_to(root)), "sha256": hashlib.sha256(approval_abs.read_bytes()).hexdigest()}, "publication_preview": None}
        _write(state_abs, state_doc)
        # Readback still resolves the adopted PREARCH triplet; READY still passes.
        rb = high.readback_revision(root, state_abs, root / rev_rel)
        self.assertEqual(rb["research_acceptance"]["family"], "PREARCH")
        self.assertTrue(rb["research_acceptance"]["triplet"])
        low.require_research_operation_ready(root, state_abs)
        cp_rel = f"{rev_rel}/checkpoint/record.json"
        errs = low.check_supersession_record_from_paths(
            root, root / cp_rel,
            root / rev_rel / "proof" / "supersession-report.json",
            root / rev_rel / "retention" / "state-before.json")
        self.assertEqual(errs, [], f"checker must pass after Human Gate: {errs}")

    def test_unreadable_paths_fail_closed_not_coerced(self) -> None:
        """EACCES paths refuse (never coerced to absent/pass)."""
        if os.geteuid() == 0:
            self.skipTest("ownership/permission faults need a non-root user")
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src"
            src.mkdir(parents=True)
            os.chmod(src, 0o000)
            try:
                obs = low.lstat_slot(src, "candidate-matrix-v2.json")
                self.assertEqual(obs["lstat_kind"], "refused")
                with self.assertRaises(low.ResearchAuthorityError):
                    low.require_no_active_guard(src)
            finally:
                os.chmod(src, 0o755)


if __name__ == "__main__":
    unittest.main()
