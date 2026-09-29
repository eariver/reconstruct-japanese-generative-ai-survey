#!/usr/bin/env python3
"""Agent-first production control for Survey Production Core v2.

ChatGPT is the research/editorial operator. This module provides the minimum
repository control needed to make that work resumable and provenance-aware:

- one compact Stage Checkpoint per local/model-assisted lifecycle transition;
- per-stage implementation/contract provenance, allowing reviewed tool upgrades;
- direct exact-byte Architecture Review and Publication Preview approvals;
- no Action Spec / Handoff / Action Result ceremony on the normal local path.

Every local Stage Checkpoint also carries one deterministic CORE_STAGE_CONTRACT
result produced by the compact stage validator.  The controller independently
checks that result against the exact State/Profile/contract/tool/artifact basis;
a same-named or fabricated PASS file is not sufficient to advance lifecycle.

Richer workflow/reconciliation authority remains appropriate at external and
irreversible boundaries such as public Release.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from copy import deepcopy
from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts import survey_drafting_v2 as drafting
from scripts import survey_production_v2 as core
from scripts import survey_publication_v2 as publication
from scripts import survey_quality_v2 as quality
from scripts import survey_reader_publication_v2 as reader
from scripts import survey_reader_surface_gate_v2 as surface_gate
from scripts import survey_review_attention_v2 as review_attention
from scripts import survey_schema_v2 as schema_gate

CHECKPOINT_SCHEMA = Path("schemas/stage-checkpoint-v2.schema.json")
STATE_SCHEMA = Path("schemas/survey-production-state.schema.json")
REVALIDATION_SCHEMA = Path("schemas/publication-surface-revalidation.schema.json")
REVALIDATION_BASENAME = "publication-surface-revalidation"
REVALIDATION_REASON_CLASSES = {"REVIEWED_CORE_CHANGE"}
REVALIDATION_CHAIN_LIMIT = 32
REVIEW_KINDS = {"DETERMINISTIC", "AGENT_RESEARCH", "AGENT_EDITORIAL", "AGENT_VISUAL"}
CORE_STAGE_REVIEW_ID = "CORE_STAGE_CONTRACT"
RELEASE_RECONCILIATION_REVIEW_ID = "RELEASE_EXACT_BYTE_RECONCILIATION"


class AgentControlError(ValueError):
    pass


@dataclass(frozen=True)
class _PendingPublicationBasis:
    """Checked, disk-bound read context; never an active authority."""

    root: str
    state_path: str
    state_sha256: str
    config_sha256: str
    head: str
    validation_ref_sha256: str
    replacements: tuple[tuple[str, str, str, str, int], ...]
    preserved: tuple[tuple[str, str, str], ...]
    predecessor_path: str | None
    predecessor_sha256: str | None


def _pending_replacements(basis: _PendingPublicationBasis | None) -> dict[tuple[str, str], str]:
    if basis is None:
        return {}
    return {(name, path): new for name, path, _old, new, _size in basis.replacements}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _rel(repo_root: Path, path: Path, label: str) -> str:
    root = repo_root.resolve()
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(root))
    except ValueError as exc:
        raise AgentControlError(f"{label} must be repository-local: {path}") from exc


def _authority(repo_root: Path, path: Path, label: str) -> dict[str, str]:
    rel = _rel(repo_root, path, label)
    resolved = core.repo_local_path(repo_root, rel, label)
    if resolved.is_symlink() or not resolved.is_file():
        raise AgentControlError(f"{label} missing or unsafe: {rel}")
    return {"path": rel, "sha256": core.sha256_file(resolved)}


def _named_authority(repo_root: Path, name: str, path: Path) -> dict[str, str]:
    if not isinstance(name, str) or not name.strip():
        raise AgentControlError("artifact name must be non-empty")
    return {"name": name, **_authority(repo_root, path, f"stage artifact {name}")}


def _profile_and_source(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any]) -> tuple[Path, dict[str, Any], Path]:
    profile_path = core.repo_local_path(repo_root, state["profile"]["path"], "state.profile.path")
    if not profile_path.is_file() or core.sha256_file(profile_path) != state["profile"]["sha256"]:
        raise AgentControlError("Production Profile bytes differ from initialized State authority")
    profile = core.load_json(profile_path)
    errors = core.validate_profile(profile, cfg)
    if errors:
        raise AgentControlError("Production Profile invalid under current tool: " + "; ".join(errors))
    if profile.get("issue_id") != state.get("issue_id"):
        raise AgentControlError("Production Profile/State issue identity mismatch")
    if profile.get("research_profile") != state.get("research_profile") or profile.get("publication_profile") != state.get("publication_profile"):
        raise AgentControlError("Production Profile/State Profile identity mismatch")
    if profile.get("contract") != state.get("contract"):
        raise AgentControlError("Production State no longer binds its initialization Profile contract")
    source_root = core.repo_local_path(repo_root, profile["paths"]["source_root"], "paths.source_root")
    return profile_path, profile, source_root


def _expected_completed_checkpoints(cfg: dict[str, Any], lifecycle: str) -> set[str]:
    index = core.LIFECYCLE.index(lifecycle)
    result: set[str] = set()
    for state_name in core.LIFECYCLE[:index]:
        stage = cfg["orchestration"]["stage_plan"].get(state_name)
        if isinstance(stage, dict):
            result.update(stage.get("checkpoints", []))
    return result


def _producer_for_checkpoint(cfg: dict[str, Any], checkpoint: str) -> tuple[str, str] | None:
    for from_state, stage in cfg["orchestration"]["stage_plan"].items():
        if checkpoint in stage.get("checkpoints", []):
            return from_state, stage["next_state"]
    return None


def _artifact_map(rows: list[dict[str, Any]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        name = row.get("name")
        if not isinstance(name, str) or not name or name in result:
            raise AgentControlError("Stage Checkpoint artifact names must be unique/non-empty")
        result[name] = {"name": name, "path": row.get("path"), "sha256": row.get("sha256")}
    return result


def _validate_core_stage_report(
    repo_root: Path,
    cfg: dict[str, Any],
    state: dict[str, Any],
    artifact_rows: list[dict[str, str]],
    reviews: list[dict[str, Any]],
    *,
    state_path: Path | None = None,
    expected_contract: dict[str, Any] | None = None,
    expected_implementation_sha: str | None = None,
) -> None:
    matches = [row for row in reviews if row.get("check_id") == CORE_STAGE_REVIEW_ID]
    if len(matches) != 1:
        raise AgentControlError("local Stage Checkpoint requires exactly one CORE_STAGE_CONTRACT review")
    review = matches[0]
    if review.get("kind") != "DETERMINISTIC" or review.get("status") != "PASS":
        raise AgentControlError("CORE_STAGE_CONTRACT must be a deterministic PASS review")
    result_ref = review.get("result")
    if not isinstance(result_ref, dict) or set(result_ref) != {"path", "sha256"}:
        raise AgentControlError("CORE_STAGE_CONTRACT requires deterministic result authority")
    result_path = core.repo_local_path(repo_root, result_ref["path"], "CORE_STAGE_CONTRACT result")
    if result_path.is_symlink() or not result_path.is_file() or core.sha256_file(result_path) != result_ref["sha256"]:
        raise AgentControlError("CORE_STAGE_CONTRACT result authority drift")
    report = core.load_json(result_path)
    required = {
        "schema_version", "check_id", "status", "issue_id", "from_state", "to_state",
        "production_state", "production_profile", "implementation_commit_sha", "contract",
        "artifacts", "recorded_at",
    }
    if not isinstance(report, dict) or set(report) != required:
        raise AgentControlError("CORE_STAGE_CONTRACT result fields invalid")
    if report.get("schema_version") != "2.0-rc1" or report.get("check_id") != CORE_STAGE_REVIEW_ID or report.get("status") != "PASS":
        raise AgentControlError("CORE_STAGE_CONTRACT result identity/status invalid")
    stage = cfg["orchestration"]["stage_plan"].get(state["lifecycle_state"])
    if not isinstance(stage, dict):
        raise AgentControlError(f"no stage configured for {state['lifecycle_state']}")
    if (
        report.get("issue_id") != state.get("issue_id")
        or report.get("from_state") != state.get("lifecycle_state")
        or report.get("to_state") != stage.get("next_state")
    ):
        raise AgentControlError("CORE_STAGE_CONTRACT lifecycle/issue basis mismatch")
    profile_path, _, _ = _profile_and_source(repo_root, cfg, state)
    expected_profile = {"path": _rel(repo_root, profile_path, "Production Profile"), "sha256": core.sha256_file(profile_path)}
    if report.get("production_profile") != expected_profile:
        raise AgentControlError("CORE_STAGE_CONTRACT Production Profile authority mismatch")
    report_state = report.get("production_state")
    if not isinstance(report_state, dict) or set(report_state) != {"path", "sha256"}:
        raise AgentControlError("CORE_STAGE_CONTRACT Production State authority fields invalid")
    if state_path is not None:
        expected_state = {"path": _rel(repo_root, state_path, "Production State"), "sha256": core.sha256_file(state_path)}
        if report_state != expected_state:
            raise AgentControlError("CORE_STAGE_CONTRACT Production State authority mismatch")
    else:
        path = core.repo_local_path(repo_root, report_state["path"], "historical CORE_STAGE_CONTRACT State")
        if path.resolve() != core.repo_local_path(repo_root, expected_profile["path"], "Production Profile").parent.joinpath(cfg["state_authority"]["authoritative_filename"]).resolve():
            raise AgentControlError("historical CORE_STAGE_CONTRACT State path is not canonical")
    contract = expected_contract or core.contract_identity(
        repo_root, cfg, state["research_profile"], state["publication_profile"]
    )
    if report.get("contract") != contract:
        raise AgentControlError("CORE_STAGE_CONTRACT contract identity mismatch")
    implementation = expected_implementation_sha
    if implementation is None:
        implementation = report.get("implementation_commit_sha")
    if report.get("implementation_commit_sha") != implementation:
        raise AgentControlError("CORE_STAGE_CONTRACT implementation identity mismatch")
    try:
        core.parse_instant(str(report.get("recorded_at", "")))
    except ValueError as exc:
        raise AgentControlError("CORE_STAGE_CONTRACT recorded_at invalid") from exc
    report_artifacts = report.get("artifacts")
    if not isinstance(report_artifacts, list):
        raise AgentControlError("CORE_STAGE_CONTRACT artifacts must be an array")
    if _artifact_map(report_artifacts) != _artifact_map(artifact_rows):
        raise AgentControlError("CORE_STAGE_CONTRACT artifacts differ from Stage Checkpoint artifacts")


def _validate_release_reconciliation_review(
    repo_root: Path,
    cfg: dict[str, Any],
    state: dict[str, Any],
    artifacts: list[dict[str, Any]],
    reviews: list[dict[str, Any]],
) -> None:
    matches = [row for row in reviews if row.get("check_id") == RELEASE_RECONCILIATION_REVIEW_ID]
    if len(matches) != 1:
        raise AgentControlError(f"Release Stage Checkpoint requires exactly one {RELEASE_RECONCILIATION_REVIEW_ID} review")
    review = matches[0]
    if review.get("kind") != "DETERMINISTIC" or review.get("status") != "PASS":
        raise AgentControlError(f"{RELEASE_RECONCILIATION_REVIEW_ID} must be a deterministic PASS review")
    result_ref = review.get("result")
    if not isinstance(result_ref, dict) or set(result_ref) != {"path", "sha256"}:
        raise AgentControlError(f"{RELEASE_RECONCILIATION_REVIEW_ID} requires deterministic result authority")
    record_path = core.repo_local_path(repo_root, result_ref["path"], f"{RELEASE_RECONCILIATION_REVIEW_ID} result")
    if record_path.is_symlink() or not record_path.is_file() or core.sha256_file(record_path) != result_ref["sha256"]:
        raise AgentControlError(f"{RELEASE_RECONCILIATION_REVIEW_ID} result authority drift")
    try:
        release = publication.validate_release_record(repo_root, record_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise AgentControlError(f"invalid Release Record authority: {exc}") from exc
    if release.get("issue_id") != state.get("issue_id"):
        raise AgentControlError("Release Record issue_id mismatch")
    artifact_map = _artifact_map(artifacts)
    release_art = artifact_map.get("release-record")
    if not release_art or release_art.get("path") != result_ref["path"] or release_art.get("sha256") != result_ref["sha256"]:
        raise AgentControlError("release-record artifact does not match RELEASE_EXACT_BYTE_RECONCILIATION result")
    merge_art = artifact_map.get("merge-verification")
    if not merge_art:
        raise AgentControlError("Release Stage Checkpoint missing merge-verification artifact")
    if release.get("merge_verification_path") != merge_art.get("path") or release.get("merge_verification_sha256") != merge_art.get("sha256"):
        raise AgentControlError("Release Record does not bind Stage Checkpoint merge-verification authority")


def _validate_checkpoint_record(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any], checkpoint: str, authority: dict[str, Any], revalidation: dict[str, Any] | None = None, pending_basis: _PendingPublicationBasis | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(authority, dict) or set(authority) != {"path", "sha256"}:
        return [f"checkpoint {checkpoint} provenance fields invalid"]
    try:
        path = core.repo_local_path(repo_root, authority["path"], f"checkpoint {checkpoint}")
    except (TypeError, ValueError) as exc:
        return [str(exc)]
    if not path.is_file():
        return [f"checkpoint {checkpoint} provenance file missing"]
    if core.sha256_file(path) != authority.get("sha256"):
        return [f"checkpoint {checkpoint} provenance SHA drift"]
    try:
        record = schema_gate.load_and_validate_json(path, repo_root / CHECKPOINT_SCHEMA, label=f"Stage Checkpoint {checkpoint}")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)]
    producer = _producer_for_checkpoint(cfg, checkpoint)
    if producer is None:
        return [f"checkpoint {checkpoint} has no lifecycle producer"]
    from_state, to_state = producer
    if record.get("issue_id") != state.get("issue_id"):
        errors.append(f"checkpoint {checkpoint} issue identity mismatch")
    if record.get("from_state") != from_state or record.get("to_state") != to_state:
        errors.append(f"checkpoint {checkpoint} lifecycle producer mismatch")
    if checkpoint not in record.get("checkpoints", []):
        errors.append(f"checkpoint {checkpoint} missing from Stage Checkpoint record")
    superseded: dict[tuple[str, str], str] = {}
    if revalidation is not None and authority.get("path") == revalidation.get("prior_checkpoint", {}).get("path"):
        superseded = {
            (row.get("name"), row.get("path")): row.get("new_sha256")
            for row in revalidation.get("superseded_artifacts", [])
        }
    if pending_basis is not None and checkpoint == "validation":
        superseded = _pending_replacements(pending_basis)
    for artifact in record.get("artifacts", []):
        try:
            resolved = core.repo_local_path(repo_root, artifact["path"], f"checkpoint artifact {artifact['name']}")
        except (TypeError, ValueError) as exc:
            errors.append(str(exc))
            continue
        expected = superseded.get((artifact.get("name"), artifact.get("path")), artifact.get("sha256"))
        if not resolved.is_file() or core.sha256_file(resolved) != expected:
            errors.append(f"Stage Checkpoint artifact drift: {artifact.get('name')}")
    for row in record.get("reviews", []):
        if row.get("kind") == "DETERMINISTIC":
            result = row.get("result")
            if not isinstance(result, dict):
                errors.append(f"deterministic review lacks result authority: {row.get('check_id')}")
                continue
            try:
                result_path = core.repo_local_path(repo_root, result["path"], f"review result {row.get('check_id')}")
            except (TypeError, ValueError) as exc:
                errors.append(str(exc))
                continue
            if not result_path.is_file() or core.sha256_file(result_path) != result.get("sha256"):
                errors.append(f"deterministic review result drift: {row.get('check_id')}")
    historical_state = dict(state)
    historical_state["lifecycle_state"] = from_state
    try:
        _validate_core_stage_report(
            repo_root,
            cfg,
            historical_state,
            record.get("artifacts", []),
            record.get("reviews", []),
            expected_contract=record.get("contract"),
            expected_implementation_sha=record.get("implementation", {}).get("repository_commit_sha"),
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(str(exc))
    if from_state == "FROZEN":
        try:
            _validate_release_reconciliation_review(
                repo_root,
                cfg,
                historical_state,
                record.get("artifacts", []),
                record.get("reviews", []),
            )
        except (AgentControlError, OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(str(exc))
    return errors


def validate_agent_state(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any]) -> list[str]:
    """Strict public State validation; pending publication is never active State."""
    return _validate_agent_state(repo_root, cfg, state)


def _validate_agent_state(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any], pending_basis: _PendingPublicationBasis | None = None) -> list[str]:
    """Validate resumable State without globally pinning the edition tool commit.

    State.contract and State.implementation preserve initialization provenance.
    Each completed stage separately pins the implementation and current contract
    used at that boundary through its Stage Checkpoint record.
    """
    errors: list[str] = []
    if pending_basis is not None:
        errors.extend(_verify_pending_binding(repo_root, cfg, state, pending_basis))
        if errors:
            return errors
    try:
        schema_gate.validate_instance(state, repo_root / STATE_SCHEMA, label="Production State")
    except ValueError as exc:
        return [str(exc)]
    if state.get("lifecycle_state") not in core.LIFECYCLE:
        return ["Production State lifecycle_state invalid"]
    try:
        _, profile, source_root = _profile_and_source(repo_root, cfg, state)
    except (OSError, ValueError, KeyError) as exc:
        return [str(exc)]

    legacy = state.get("legacy_compatibility", {})
    try:
        legacy_path = core.repo_local_path(repo_root, legacy["legacy_state_path"], "legacy_state_path")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    else:
        present = legacy_path.is_file()
        digest = core.sha256_file(legacy_path) if present else None
        if present != legacy.get("legacy_state_present") or digest != legacy.get("legacy_state_sha256"):
            errors.append("legacy compatibility artifact changed after v2 initialization")

    expected = _expected_completed_checkpoints(cfg, state["lifecycle_state"])
    if state.get("human_gates", {}).get("publication_preview") == "approved":
        expected.add("publication_preview")
    if pending_basis is None:
        revalidation, revalidation_errors = resolve_active_publication_revalidation(repo_root, cfg, state)
    else:
        revalidation = None
        _predecessor, revalidation_errors = _resolve_publication_revalidation(repo_root, cfg, state, live=False)
    errors.extend(revalidation_errors)
    checkpoints = state.get("machine_checkpoints", {})
    provenance = state.get("checkpoint_provenance", {})
    for name in core.CHECKPOINTS:
        wanted = "passed" if name in expected else "pending"
        if checkpoints.get(name) != wanted:
            errors.append(f"Production State checkpoint {name}={checkpoints.get(name)!r}; expected {wanted!r}")
        authority = provenance.get(name)
        if name == "publication_preview" and wanted == "passed":
            if not isinstance(authority, dict):
                errors.append("Publication Preview checkpoint lacks approval provenance")
            else:
                approval_path = source_root / cfg["state_authority"]["publication_preview_approval_path"]
                if authority.get("path") != _rel(repo_root, approval_path, "Publication Preview approval"):
                    errors.append("Publication Preview checkpoint provenance path is not canonical")
                elif not approval_path.is_file() or core.sha256_file(approval_path) != authority.get("sha256"):
                    errors.append("Publication Preview checkpoint approval provenance drift")
                else:
                    try:
                        publication.validate_preview_approval(repo_root, approval_path, issue_id=state["issue_id"])
                    except ValueError as exc:
                        errors.append(str(exc))
        elif wanted == "passed":
            if authority is None:
                errors.append(f"passed checkpoint lacks Stage Checkpoint provenance: {name}")
            else:
                errors.extend(_validate_checkpoint_record(repo_root, cfg, state, name, authority, revalidation, pending_basis))
        elif authority is not None:
            errors.append(f"pending checkpoint must not carry provenance: {name}")

    index = core.LIFECYCLE.index(state["lifecycle_state"])
    history = state.get("history")
    if not isinstance(history, list) or len(history) != index + 1:
        errors.append("Production State history length must exactly match lifecycle position")
    else:
        previous: datetime | None = None
        for row_index, row in enumerate(history):
            expected_to = core.LIFECYCLE[row_index]
            expected_from = None if row_index == 0 else core.LIFECYCLE[row_index - 1]
            if not isinstance(row, dict) or row.get("from") != expected_from or row.get("to") != expected_to:
                errors.append(f"Production State history[{row_index}] lifecycle path invalid")
                continue
            sha = row.get("repository_commit_sha")
            if not isinstance(sha, str) or len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha):
                errors.append(f"Production State history[{row_index}] implementation SHA invalid")
            try:
                instant = core.parse_instant(str(row.get("recorded_at", "")))
                if previous is not None and instant < previous:
                    errors.append("Production State history timestamps must be monotonic")
                previous = instant
            except ValueError:
                errors.append(f"Production State history[{row_index}].recorded_at invalid")

    gate_provenance = state.get("human_gate_provenance", {})
    current_index = core.LIFECYCLE.index(state["lifecycle_state"])
    arch_index = core.LIFECYCLE.index("ARCHITECTURE_ESTABLISHED")
    arch_status = state.get("human_gates", {}).get("architecture_review")
    arch_auth = gate_provenance.get("architecture_review")
    if current_index < arch_index and arch_status != "pending":
        errors.append("Architecture Review cannot resolve before ARCHITECTURE_ESTABLISHED")
    if current_index > arch_index and arch_status != "approved":
        errors.append("post-Architecture lifecycle requires approved Architecture Review")
    if arch_status == "pending":
        if arch_auth is not None:
            errors.append("pending Architecture Review must not carry provenance")
    else:
        approval_path = source_root / cfg["state_authority"]["architecture_approval_path"]
        if not isinstance(arch_auth, dict) or arch_auth.get("path") != _rel(repo_root, approval_path, "Architecture approval"):
            errors.append("resolved Architecture Review lacks canonical approval provenance")
        elif not approval_path.is_file() or core.sha256_file(approval_path) != arch_auth.get("sha256"):
            errors.append("Architecture approval provenance drift")
        elif arch_status == "approved":
            architecture = source_root / "architecture-v2.json"
            summary = source_root / "architecture-review-summary-v2.json"
            if not architecture.is_file() or not summary.is_file():
                errors.append("approved Architecture Review lacks canonical review bytes")
            else:
                try:
                    approval = core.load_json(approval_path)
                    approval_errors = drafting.validate_architecture_approval(approval, architecture, summary, state["issue_id"])
                    errors.extend(approval_errors)
                except (OSError, ValueError, json.JSONDecodeError) as exc:
                    errors.append(str(exc))

    pub_index = core.LIFECYCLE.index("RELEASE_CANDIDATE")
    pub_status = state.get("human_gates", {}).get("publication_preview")
    if current_index < pub_index and pub_status != "pending":
        errors.append("Publication Preview cannot resolve before RELEASE_CANDIDATE")
    if current_index > pub_index and pub_status != "approved":
        errors.append("post-Publication Preview lifecycle requires approved Publication Preview")

    try:
        expected_action, expected_terminal = core.derive_control_fields(state, cfg)
    except (KeyError, ValueError) as exc:
        errors.append(f"Production State controller fields cannot be derived: {exc}")
    else:
        if state.get("next_action") != expected_action:
            errors.append(f"Production State next_action drift: {state.get('next_action')!r} != {expected_action!r}")
        if state.get("terminal_reason") != expected_terminal:
            errors.append(f"Production State terminal_reason drift: {state.get('terminal_reason')!r} != {expected_terminal!r}")
    return errors


def resolve_checkpoint_artifact(
    repo_root: Path,
    cfg: dict[str, Any],
    state: dict[str, Any],
    checkpoint: str,
    artifact_name: str,
) -> dict[str, Any]:
    return _resolve_checkpoint_artifact(repo_root, cfg, state, checkpoint, artifact_name)


def _resolve_checkpoint_artifact(
    repo_root: Path,
    cfg: dict[str, Any],
    state: dict[str, Any],
    checkpoint: str,
    artifact_name: str,
    pending_basis: _PendingPublicationBasis | None = None,
) -> dict[str, Any]:
    """Resolve one exact artifact adopted by a passed Stage Checkpoint.

    A content-addressed artifact directory is historical storage, not active
    authority.  Active authority is the artifact explicitly carried by the
    State-bound Stage Checkpoint.  This resolver centralizes that rule for
    downstream helpers and fails closed on every ambiguous or drifted link.
    """
    if checkpoint not in core.CHECKPOINTS:
        raise AgentControlError(f"unsupported checkpoint: {checkpoint}")
    if not isinstance(artifact_name, str) or not artifact_name.strip():
        raise AgentControlError("checkpoint artifact name must be non-empty")
    if pending_basis is not None and checkpoint == "validation":
        raise AgentControlError("pending publication cannot resolve validation output as upstream authority")

    state_errors = _validate_agent_state(repo_root, cfg, state, pending_basis)
    if state_errors:
        raise AgentControlError(
            "Production State invalid before checkpoint artifact resolution: "
            + "; ".join(state_errors)
        )

    if state.get("machine_checkpoints", {}).get(checkpoint) != "passed":
        raise AgentControlError(f"checkpoint {checkpoint} is not passed")
    provenance = state.get("checkpoint_provenance", {})
    authority = provenance.get(checkpoint)
    if not isinstance(authority, dict):
        raise AgentControlError(f"checkpoint {checkpoint} requires exactly one provenance authority")

    checkpoint_errors = _validate_checkpoint_record(
        repo_root, cfg, state, checkpoint, authority, pending_basis=pending_basis
    )
    if checkpoint_errors:
        raise AgentControlError(
            f"checkpoint {checkpoint} authority invalid: " + "; ".join(checkpoint_errors)
        )
    checkpoint_path = core.repo_local_path(
        repo_root, authority["path"], f"checkpoint {checkpoint}"
    )
    checkpoint_raw_path = repo_root / authority["path"]
    if checkpoint_raw_path.is_symlink() or not checkpoint_raw_path.is_file():
        raise AgentControlError(f"checkpoint {checkpoint} path is missing or unsafe")
    checkpoint_record = schema_gate.load_and_validate_json(
        checkpoint_path,
        repo_root / CHECKPOINT_SCHEMA,
        label=f"Stage Checkpoint {checkpoint}",
    )
    producer = _producer_for_checkpoint(cfg, checkpoint)
    if producer is None:
        raise AgentControlError(f"checkpoint {checkpoint} has no lifecycle producer")
    producer_stage = cfg["orchestration"]["stage_plan"].get(producer[0])
    if not isinstance(producer_stage, dict) or set(checkpoint_record["checkpoints"]) != set(
        producer_stage.get("checkpoints", [])
    ):
        raise AgentControlError(
            f"checkpoint {checkpoint} checkpoint set does not match its lifecycle stage"
        )
    try:
        _artifact_map(checkpoint_record["artifacts"])
    except (KeyError, TypeError) as exc:
        raise AgentControlError(
            f"checkpoint {checkpoint} artifact authority is malformed"
        ) from exc
    matches = [
        row for row in checkpoint_record["artifacts"]
        if row.get("name") == artifact_name
    ]
    if len(matches) != 1:
        raise AgentControlError(
            f"checkpoint {checkpoint} must contain exactly one {artifact_name} artifact; "
            f"found {len(matches)}"
        )
    artifact = matches[0]
    artifact_path = core.repo_local_path(
        repo_root, artifact.get("path"), f"checkpoint artifact {artifact_name}"
    )
    artifact_raw_path = repo_root / artifact["path"]
    if artifact_raw_path.is_symlink() or artifact_path.is_symlink() or not artifact_path.is_file():
        raise AgentControlError(
            f"checkpoint artifact {artifact_name} missing or unsafe: {artifact.get('path')}"
        )
    actual_sha = core.sha256_file(artifact_path)
    if actual_sha != artifact.get("sha256"):
        raise AgentControlError(
            f"checkpoint artifact {artifact_name} SHA drift: {artifact.get('path')}"
        )
    return {
        "checkpoint": checkpoint,
        "checkpoint_path": checkpoint_path,
        "checkpoint_authority": deepcopy(authority),
        "checkpoint_record": checkpoint_record,
        "artifact": deepcopy(artifact),
        "artifact_path": artifact_path,
    }


def resolve_active_evidence_views(
    repo_root: Path,
    cfg: dict[str, Any],
    state: dict[str, Any],
) -> dict[str, Any]:
    """Resolve the active Evidence and Edition View pair from one checkpoint.

    Historical accepted directories may contain any number of immutable runs;
    only the exact artifacts named by the State-bound CANDIDATES_NORMALIZED
    checkpoint are eligible. The View acceptance must also bind that exact
    Evidence acceptance, preventing a cross-run join.
    """
    evidence = resolve_checkpoint_artifact(
        repo_root, cfg, state, "evidence", "evidence-acceptance"
    )
    views = resolve_checkpoint_artifact(
        repo_root, cfg, state, "evidence", "edition-views-acceptance"
    )
    if evidence["checkpoint_authority"] != views["checkpoint_authority"]:
        raise AgentControlError(
            "active Evidence and Edition View authorities must come from the same Stage Checkpoint"
        )
    view_acceptance = core.load_json(views["artifact_path"])
    expected_evidence_sha = core.sha256_file(evidence["artifact_path"])
    if view_acceptance.get("evidence_acceptance_sha256") != expected_evidence_sha:
        raise AgentControlError(
            "active Edition View acceptance does not bind the checkpoint-bound Evidence acceptance"
        )
    return {
        "evidence": evidence,
        "views": views,
        "evidence_path": evidence["artifact_path"],
        "views_path": views["artifact_path"],
    }


def verify_agent_state_basis(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any]) -> None:
    errors = validate_agent_state(repo_root, cfg, state)
    if errors:
        raise AgentControlError("Production State is not safely resumable: " + "; ".join(errors))


def _revalidation_record_path(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any], sequence: int) -> Path:
    _, _, source_root = _profile_and_source(repo_root, cfg, state)
    return source_root / "publication" / "v2" / f"{REVALIDATION_BASENAME}-r{sequence}.json"


def _revalidation_existing_sequences(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any]) -> list[int]:
    _, _, source_root = _profile_and_source(repo_root, cfg, state)
    directory = source_root / "publication" / "v2"
    sequences: list[int] = []
    if not directory.is_dir():
        return sequences
    for child in sorted(directory.iterdir()):
        if child.is_symlink() or not child.is_file():
            continue
        name = child.name
        if name.startswith(REVALIDATION_BASENAME + "-r") and name.endswith(".json"):
            middle = name[len(REVALIDATION_BASENAME) + 2:-len(".json")]
            if middle.isdigit() and not middle.startswith("0") and not child.is_symlink():
                sequences.append(int(middle))
    return sorted(sequences)


def _revalidation_surface_roots(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any]) -> tuple[Path, Path]:
    _, profile, source_root = _profile_and_source(repo_root, cfg, state)
    survey_root = core.repo_local_path(repo_root, profile["paths"]["survey_root"], "paths.survey_root")
    return source_root.resolve(), survey_root.resolve()


def _publication_revalidation_roles(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any]) -> dict[str, str]:
    """Exact configured validation artifacts, plus its canonical Reader Gate."""
    _, profile, source_root = _profile_and_source(repo_root, cfg, state)
    stage = cfg["orchestration"]["stage_plan"]["DRAFT_COMPLETE"]
    roles: dict[str, str] = {}
    for row in stage["artifacts"]:
        roles[row["name"]] = _expand_stage_path(row["path"], profile)
    roles["reader-surface-gate"] = _rel(repo_root, source_root / "publication/v2/reader-surface-gate-v2.json", "Reader Gate")
    return roles


def _pending_conditions(state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if state.get("lifecycle_state") != "VALIDATED_DRAFT":
        errors.append("pending publication requires VALIDATED_DRAFT")
    if state.get("human_gates", {}).get("architecture_review") != "approved":
        errors.append("pending publication requires approved Architecture Review")
    if state.get("human_gates", {}).get("publication_preview") != "pending" or state.get("human_gate_provenance", {}).get("publication_preview") is not None:
        errors.append("pending publication forbids Publication Preview decision")
    if any(state.get("machine_checkpoints", {}).get(name) != "pending" for name in ("publication_preview", "freeze", "release")):
        errors.append("pending publication forbids downstream checkpoint")
    if state.get("exception_gate", {}).get("status") != "inactive":
        errors.append("pending publication forbids active Exception Gate")
    return errors


def _collect_pending_rows(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any], *, require_change: bool = True) -> tuple[tuple[tuple[str, str, str, str, int], ...], tuple[tuple[str, str, str], ...]]:
    ref = state.get("checkpoint_provenance", {}).get("validation")
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
        raise AgentControlError("pending publication requires exact validation checkpoint reference")
    checkpoint_path = _revalidation_row_path(repo_root, ref["path"], "pending validation checkpoint")
    if core.sha256_file(checkpoint_path) != ref["sha256"]:
        raise AgentControlError("pending validation checkpoint SHA drift")
    record = schema_gate.load_and_validate_json(checkpoint_path, repo_root / CHECKPOINT_SCHEMA, label="pending validation checkpoint")
    if record.get("issue_id") != state.get("issue_id") or record.get("from_state") != "DRAFT_COMPLETE" or record.get("to_state") != "VALIDATED_DRAFT" or "validation" not in record.get("checkpoints", []):
        raise AgentControlError("pending validation checkpoint identity/producer mismatch")
    allowed = _publication_revalidation_roles(repo_root, cfg, state)
    changed: list[tuple[str, str, str, str, int]] = []
    kept: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()
    seen_names: set[str] = set()
    for row in record["artifacts"]:
        name, raw, old = row["name"], row["path"], row["sha256"]
        key = (name, raw)
        if key in seen or name in seen_names:
            raise AgentControlError(f"pending validation checkpoint duplicate artifact: {name}")
        seen.add(key)
        seen_names.add(name)
        path = _revalidation_row_path(repo_root, raw, f"pending artifact {name}")
        current = core.sha256_file(path)
        if current == old:
            kept.append((name, raw, old))
        elif allowed.get(name) == raw:
            changed.append((name, raw, old, current, path.stat().st_size))
        else:
            raise AgentControlError(f"pending publication changed noncanonical or upstream role/path: {name}")
    if require_change and not changed:
        raise AgentControlError("pending publication requires changed publication bytes")
    return tuple(changed), tuple(kept)


def _verify_pending_binding(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any], basis: _PendingPublicationBasis) -> list[str]:
    errors = _pending_conditions(state)
    try:
        state_path = Path(basis.state_path)
        config_path = repo_root / core.DEFAULT_CONFIG
        _, _, source_root = _profile_and_source(repo_root, cfg, state)
        canonical_state = (source_root / cfg["state_authority"]["authoritative_filename"]).resolve()
        try:
            state_relative = state_path.relative_to(repo_root.resolve())
            safe_state = core.repo_local_path(repo_root, state_relative.as_posix(), "pending Production State")
        except ValueError:
            errors.append("pending publication State path is not repository-local")
        else:
            if state_path != safe_state or state_path.is_symlink() or safe_state != canonical_state:
                errors.append("pending publication State path is not canonical")
        if basis.root != str(repo_root.resolve()) or not state_path.is_file() or core.sha256_file(state_path) != basis.state_sha256 or core.load_json(state_path) != state:
            errors.append("pending publication State bytes changed")
        if core.sha256_file(config_path) != basis.config_sha256 or core.load_json(config_path) != cfg:
            errors.append("pending publication config bytes changed")
        if core.repository_commit_sha(repo_root) != basis.head:
            errors.append("pending publication implementation HEAD changed")
        ref = state.get("checkpoint_provenance", {}).get("validation")
        if not isinstance(ref, dict) or ref.get("sha256") != basis.validation_ref_sha256:
            errors.append("pending publication validation reference changed")
        changed, kept = _collect_pending_rows(repo_root, cfg, state)
        if changed != basis.replacements or kept != basis.preserved:
            errors.append("pending publication row snapshot changed")
        pointer = state.get("publication_revalidation_provenance")
        if pointer is None:
            if basis.predecessor_path is not None or basis.predecessor_sha256 is not None:
                errors.append("pending publication predecessor changed")
        elif pointer != {"path": basis.predecessor_path, "sha256": basis.predecessor_sha256}:
            errors.append("pending publication predecessor changed")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"pending publication basis cannot be rechecked: {exc}")
    return errors


def built_checked_pending_publication_basis(repo_root: Path, cfg: dict[str, Any], state_path: Path) -> _PendingPublicationBasis:
    """Build a fresh context from actual State, checkpoint and current publication files."""
    state_path = _revalidation_row_path(repo_root, _rel(repo_root, state_path, "Production State"), "Production State")
    state = core.load_json(state_path)
    _, _, source_root = _profile_and_source(repo_root, cfg, state)
    if state_path != (source_root / cfg["state_authority"]["authoritative_filename"]).resolve():
        raise AgentControlError("pending publication State path is not canonical")
    conditions = _pending_conditions(state)
    if conditions:
        raise AgentControlError("; ".join(conditions))
    changed, kept = _collect_pending_rows(repo_root, cfg, state)
    predecessor, predecessor_errors = _resolve_publication_revalidation(repo_root, cfg, state, live=False)
    if predecessor_errors:
        raise AgentControlError("pending publication predecessor invalid: " + "; ".join(predecessor_errors))
    pointer = state.get("publication_revalidation_provenance")
    basis = _PendingPublicationBasis(
        str(repo_root.resolve()), str(state_path), core.sha256_file(state_path),
        core.sha256_file(repo_root / core.DEFAULT_CONFIG), core.repository_commit_sha(repo_root),
        state["checkpoint_provenance"]["validation"]["sha256"], changed, kept,
        pointer["path"] if pointer else None, pointer["sha256"] if pointer else None,
    )
    errors = _validate_agent_state(repo_root, cfg, state, basis)
    if errors:
        raise AgentControlError("pending publication State invalid: " + "; ".join(errors))
    return basis


def _revalidation_row_path(repo_root: Path, raw: str, label: str) -> Path:
    try:
        path = core.repo_local_path(repo_root, raw, label)
    except (TypeError, ValueError) as exc:
        raise AgentControlError(f"{label} escapes repository: {raw}") from exc
    if path.is_symlink() or not path.is_file():
        raise AgentControlError(f"{label} missing or unsafe: {raw}")
    return path


def _load_revalidation_record(
    repo_root: Path, ref: dict[str, Any], label: str
) -> tuple[dict[str, Any] | None, str | None]:
    """Load one revalidation record file with structural validation.

    Returns (record, error). Error is a single string; None means success.
    """
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
        return None, f"{label} authority fields invalid"
    try:
        path = core.repo_local_path(repo_root, ref["path"], label)
    except (TypeError, ValueError) as exc:
        return None, str(exc)
    if path.is_symlink() or not path.is_file():
        return None, f"{label} missing or unsafe"
    if core.sha256_file(path) != ref.get("sha256"):
        return None, f"{label} SHA mismatch"
    try:
        record = schema_gate.load_and_validate_json(
            path, repo_root / REVALIDATION_SCHEMA, label="Publication Surface Revalidation"
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return None, f"{label} invalid: {exc}"
    return record, None


def _check_immutable_revalidation_rows(
    repo_root: Path, cfg: dict[str, Any], state: dict[str, Any],
    record: dict[str, Any], prior_record: dict[str, Any],
    publication_dir: Path, survey_root: Path, *, live: bool,
) -> list[str]:
    """Check exact prior rows and QA references for active or historical records."""
    errors: list[str] = []
    prior_list = prior_record.get("artifacts", [])
    prior_rows = {(row.get("name"), row.get("path")): row for row in prior_list if isinstance(row, dict)}
    if len(prior_rows) != len(prior_list) or len({row.get("name") for row in prior_list if isinstance(row, dict)}) != len(prior_list):
        errors.append("publication revalidation prior checkpoint duplicates artifact identities")
    allowed_rows = _publication_revalidation_roles(repo_root, cfg, state)
    seen: set[tuple[str, str]] = set()
    for row in record.get("superseded_artifacts", []):
        key = (row.get("name"), row.get("path"))
        if key in seen:
            errors.append(f"publication revalidation duplicates superseded artifact: {key[0]}")
            continue
        seen.add(key)
        prior = prior_rows.get(key)
        if prior is None:
            errors.append(f"publication revalidation supersedes unknown prior artifact: {key[0]}")
            continue
        if row.get("prior_sha256") != prior.get("sha256"):
            errors.append(f"publication revalidation prior SHA mismatch: {key[0]}")
            continue
        if row.get("new_sha256") == prior.get("sha256"):
            errors.append(f"publication revalidation supersedes unchanged bytes: {key[0]}")
            continue
        if allowed_rows.get(key[0]) != key[1]:
            errors.append(f"publication revalidation role/path is not canonical: {key[0]}")
            continue
        try:
            resolved = _revalidation_row_path(repo_root, row["path"], f"revalidated artifact {key[0]}")
        except AgentControlError as exc:
            errors.append(str(exc))
            continue
        allowed = False
        for root_dir in (publication_dir, survey_root):
            try:
                resolved.resolve().relative_to(root_dir)
                allowed = True
            except ValueError:
                continue
        if not allowed:
            errors.append(f"publication revalidation escapes publication surface: {key[0]}")
            continue
        if live and core.sha256_file(resolved) != row.get("new_sha256"):
            errors.append(f"revalidated publication artifact drift: {key[0]}")
            continue
        if live and resolved.stat().st_size != row.get("byte_count"):
            errors.append(f"revalidated publication artifact byte count drift: {key[0]}")
    for row in record.get("preserved_artifacts", []):
        key = (row.get("name"), row.get("path"))
        if key in seen:
            errors.append(f"publication revalidation duplicates artifact: {key[0]}")
            continue
        seen.add(key)
        prior = prior_rows.get(key)
        if prior is None or row.get("sha256") != prior.get("sha256"):
            errors.append(f"publication revalidation preserved artifact mismatch: {key[0]}")
            continue
        try:
            resolved = _revalidation_row_path(repo_root, row["path"], f"preserved artifact {key[0]}")
        except AgentControlError as exc:
            errors.append(str(exc))
            continue
        if live and core.sha256_file(resolved) != row.get("sha256"):
            errors.append(f"preserved upstream artifact drift: {key[0]}")
    if seen != set(prior_rows):
        errors.append("publication revalidation artifact row union differs from prior checkpoint")
    effective = {
        (row["name"], row["path"]): row["new_sha256"]
        for row in record.get("superseded_artifacts", [])
    }
    effective.update({
        (row["name"], row["path"]): row["sha256"]
        for row in record.get("preserved_artifacts", [])
    })
    for label, role in (
        ("manuscript", "reader-manuscript"),
        ("quality_bundle", "quality-regression-bundle"),
        ("semantic_review", "semantic-review"),
        ("visual_review", "visual-review"),
        ("pdf", "publication-pdf"),
    ):
        ref = record.get("validation", {}).get(label)
        canonical = allowed_rows.get(role)
        if not isinstance(ref, dict) or ref.get("path") != canonical or ref.get("sha256") != effective.get((role, canonical)):
            errors.append(f"publication revalidation predecessor {label} is not bound to its artifact row")
        if label == "pdf" and isinstance(ref, dict):
            superseded_pdf = next((row for row in record.get("superseded_artifacts", []) if (row.get("name"), row.get("path")) == (role, canonical)), None)
            if superseded_pdf is not None and ref.get("byte_count") != superseded_pdf.get("byte_count"):
                errors.append("publication revalidation predecessor PDF byte count mismatch")
            if superseded_pdf is None and canonical is not None:
                try:
                    unchanged_pdf = _revalidation_row_path(repo_root, canonical, "preserved predecessor PDF")
                except AgentControlError as exc:
                    errors.append(str(exc))
                else:
                    if core.sha256_file(unchanged_pdf) == ref.get("sha256") and unchanged_pdf.stat().st_size != ref.get("byte_count"):
                        errors.append("publication revalidation predecessor preserved PDF byte count mismatch")
    return errors


def _check_revalidation_chain(
    repo_root: Path, cfg: dict[str, Any], state: dict[str, Any],
    record: dict[str, Any], prior_record: dict[str, Any],
    publication_dir: Path, survey_root: Path,
) -> list[str]:
    """Walk the immutable supersession chain; every link must exist byte-identical."""
    errors: list[str] = []
    seen: set[str] = set()
    current: dict[str, Any] | None = record
    for _ in range(REVALIDATION_CHAIN_LIMIT):
        if current is None:
            return errors
        link = current.get("supersedes")
        if link is None:
            return errors
        linked, error = _load_revalidation_record(repo_root, link, "superseded revalidation record")
        if error is not None:
            errors.append(error)
            return errors
        assert linked is not None
        digest = core.sha256_file(
            core.repo_local_path(repo_root, link["path"], "superseded revalidation record")
        )
        if digest in seen:
            errors.append("publication revalidation supersession chain cycle")
            return errors
        seen.add(digest)
        if linked.get("issue_id") != record.get("issue_id"):
            errors.append("publication revalidation chain issue identity mismatch")
            return errors
        if linked.get("prior_checkpoint") != record.get("prior_checkpoint"):
            errors.append("publication revalidation chain prior checkpoint mismatch")
            return errors
        try:
            linked_at = core.parse_instant(str(linked.get("recorded_at", "")))
            current_at = core.parse_instant(str(current.get("recorded_at", "")))
        except ValueError:
            errors.append("publication revalidation chain chronology invalid")
            return errors
        if linked_at > current_at:
            errors.append("publication revalidation chain chronology invalid")
            return errors
        if linked.get("reason_class") not in REVALIDATION_REASON_CLASSES:
            errors.append("publication revalidation chain reason class unrecognized")
        establishment = linked.get("establishment", {})
        for key, expected in (
            ("lifecycle", "VALIDATED_DRAFT"),
            ("architecture_review", "approved"),
            ("publication_preview", "pending"),
            ("freeze", "pending"),
            ("release", "pending"),
        ):
            if establishment.get(key) != expected:
                errors.append(f"publication revalidation chain establishment invalid: {key}")
        try:
            core.parse_instant(str(establishment.get("recorded_at", "")))
        except ValueError:
            errors.append("publication revalidation chain establishment recorded_at invalid")
        errors.extend(_check_immutable_revalidation_rows(
            repo_root, cfg, state, linked, prior_record, publication_dir, survey_root, live=False,
        ))
        if errors:
            return errors
        current = linked
    errors.append("publication revalidation supersession chain too deep")
    return errors


def _check_revalidation_agreement(
    repo_root: Path, cfg: dict[str, Any], state: dict[str, Any], record: dict[str, Any]
) -> list[str]:
    """Require post-decision states to agree with Human-approved bytes.

    A revalidation record established pre-decision stays usable afterwards only
    while it binds exactly the PDF bytes the Human decisions approved. Any
    divergence (e.g. swapped live bytes with a forged consistent record) fails.
    """
    errors: list[str] = []
    record_pdf = ((record.get("validation") or {}).get("pdf") or {}).get("sha256")
    gates = state.get("human_gates", {})
    provenance = state.get("human_gate_provenance", {})
    checkpoints = state.get("machine_checkpoints", {})
    _, _, source_root = _profile_and_source(repo_root, cfg, state)
    if gates.get("publication_preview") != "pending" or provenance.get("publication_preview") is not None:
        approval_ref = provenance.get("publication_preview")
        if not isinstance(approval_ref, dict) or set(approval_ref) != {"path", "sha256"}:
            errors.append("decided Publication Preview lacks gate provenance for revalidation agreement")
        else:
            try:
                approval_path = core.repo_local_path(repo_root, approval_ref["path"], "Publication Preview approval")
            except (TypeError, ValueError) as exc:
                errors.append(str(exc))
            else:
                if approval_path.is_symlink() or not approval_path.is_file():
                    errors.append("Publication Preview approval missing for revalidation agreement")
                elif core.sha256_file(approval_path) != approval_ref.get("sha256"):
                    errors.append("Publication Preview approval provenance drift for revalidation agreement")
                else:
                    try:
                        approval = core.load_json(approval_path)
                    except (OSError, ValueError, json.JSONDecodeError) as exc:
                        errors.append(f"Publication Preview approval unreadable for revalidation agreement: {exc}")
                    else:
                        if (
                            approval.get("decision") != "APPROVED"
                            or approval.get("gate") != "PUBLICATION_PREVIEW"
                            or approval.get("issue_id") != state.get("issue_id")
                        ):
                            errors.append("Publication Preview approval identity invalid for revalidation agreement")
                        elif approval.get("pdf_sha256") != record_pdf:
                            errors.append("active revalidation PDF diverges from Human-approved Publication Preview bytes")
    if checkpoints.get("freeze") == "passed":
        freeze_path = source_root / "publication" / "v2" / "freeze-record-v2.json"
        try:
            freeze = core.load_json(freeze_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"freeze record unreadable for revalidation agreement: {exc}")
        else:
            if freeze.get("pdf_sha256") != record_pdf:
                errors.append("active revalidation PDF diverges from Freeze record bytes")
    if checkpoints.get("release") == "passed":
        manifest_path = source_root / "publication" / "v2" / "release-manifest-v2.json"
        try:
            manifest = core.load_json(manifest_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"release manifest unreadable for revalidation agreement: {exc}")
        else:
            if manifest.get("pdf_sha256") != record_pdf:
                errors.append("active revalidation PDF diverges from Release Manifest bytes")
    return errors


def resolve_active_publication_revalidation(
    repo_root: Path, cfg: dict[str, Any], state: dict[str, Any]
) -> tuple[dict[str, Any] | None, list[str]]:
    return _resolve_publication_revalidation(repo_root, cfg, state, live=True)


def _resolve_publication_revalidation(
    repo_root: Path, cfg: dict[str, Any], state: dict[str, Any], *, live: bool
) -> tuple[dict[str, Any] | None, list[str]]:
    """Resolve the State-bound active publication-surface revalidation basis.

    The record is authoritative only through the exact {path, sha256} reference
    in production-state.json. A schema-valid file at a canonical location with
    no State reference is inert and never consulted. Returns (record, errors);
    (None, []) when the State carries no reference. A referenced-but-invalid
    record is a fail-closed error, never a fallback to old behavior.
    """
    try:
        publication_dir, survey_root = _revalidation_surface_roots(repo_root, cfg, state)
    except (OSError, ValueError, KeyError) as exc:
        return None, [f"publication revalidation basis unresolvable: {exc}"]
    pointer = state.get("publication_revalidation_provenance")
    if pointer is None:
        return None, []
    record, error = _load_revalidation_record(repo_root, pointer, "active publication revalidation authority")
    if error is not None:
        return None, [error]
    assert record is not None
    errors: list[str] = []
    if record.get("issue_id") != state.get("issue_id"):
        errors.append("publication revalidation issue identity mismatch")
    if record.get("reason_class") not in REVALIDATION_REASON_CLASSES:
        errors.append("publication revalidation reason class unrecognized")
    establishment = record.get("establishment", {})
    for key, expected in (
        ("lifecycle", "VALIDATED_DRAFT"),
        ("architecture_review", "approved"),
        ("publication_preview", "pending"),
        ("freeze", "pending"),
        ("release", "pending"),
    ):
        if establishment.get(key) != expected:
            errors.append(f"publication revalidation establishment not pre-decision sanctioned: {key}")
    try:
        core.parse_instant(str(establishment.get("recorded_at", "")))
    except ValueError:
        errors.append("publication revalidation establishment recorded_at invalid")
    prior_ref = record.get("prior_checkpoint")
    if not isinstance(prior_ref, dict) or set(prior_ref) != {"path", "sha256"}:
        errors.append("publication revalidation prior checkpoint authority fields invalid")
        return None, errors
    validation_ref = (state.get("checkpoint_provenance") or {}).get("validation")
    if validation_ref != prior_ref:
        errors.append("publication revalidation does not bind the active validation checkpoint")
    try:
        prior_path = core.repo_local_path(repo_root, prior_ref["path"], "revalidation prior checkpoint")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
        return None, errors
    if not prior_path.is_file() or core.sha256_file(prior_path) != prior_ref.get("sha256"):
        errors.append("publication revalidation prior checkpoint drift")
        return None, errors
    try:
        prior_record = schema_gate.load_and_validate_json(
            prior_path, repo_root / CHECKPOINT_SCHEMA, label="revalidation prior Stage Checkpoint"
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"publication revalidation prior checkpoint unreadable: {exc}")
        return None, errors
    errors.extend(_check_immutable_revalidation_rows(
        repo_root, cfg, state, record, prior_record, publication_dir, survey_root, live=live,
    ))
    if not live:
        errors.extend(_check_revalidation_chain(repo_root, cfg, state, record, prior_record, publication_dir, survey_root))
        return (None, errors) if errors else (record, [])
    for label, ref in (
        ("revalidation manuscript", record.get("validation", {}).get("manuscript")),
        ("revalidation quality bundle", record.get("validation", {}).get("quality_bundle")),
        ("revalidation semantic review", record.get("validation", {}).get("semantic_review")),
        ("revalidation visual review", record.get("validation", {}).get("visual_review")),
    ):
        if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
            errors.append(f"{label} authority fields invalid")
            continue
        try:
            resolved = _revalidation_row_path(repo_root, ref["path"], label)
        except AgentControlError as exc:
            errors.append(str(exc))
            continue
        if core.sha256_file(resolved) != ref.get("sha256"):
            errors.append(f"{label} drift")
    pdf_ref = record.get("validation", {}).get("pdf", {})
    try:
        pdf_path = _revalidation_row_path(repo_root, pdf_ref.get("path", ""), "revalidation PDF")
    except AgentControlError as exc:
        errors.append(str(exc))
    else:
        if core.sha256_file(pdf_path) != pdf_ref.get("sha256") or pdf_path.stat().st_size != pdf_ref.get("byte_count"):
            errors.append("revalidation PDF drift")
    errors.extend(_check_revalidation_chain(repo_root, cfg, state, record, prior_record, publication_dir, survey_root))
    errors.extend(_check_revalidation_agreement(repo_root, cfg, state, record))
    if errors:
        return None, errors
    return record, []


def canonical_checkpoint_path(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any]) -> Path:
    _, _, source_root = _profile_and_source(repo_root, cfg, state)
    return source_root / cfg["state_authority"]["agent_checkpoint_dir"] / f"{state['lifecycle_state']}.json"


def _expand_stage_path(template: str, profile: dict[str, Any]) -> str:
    value = template
    for key, replacement in profile["paths"].items():
        value = value.replace("{" + key + "}", replacement)
    if "{" in value or "}" in value:
        raise AgentControlError(f"unsupported stage path template: {template}")
    return value


def _validate_stage_artifacts(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any], profile: dict[str, Any], artifacts: list[dict[str, str]]) -> None:
    names = [row["name"] for row in artifacts]
    if len(names) != len(set(names)):
        raise AgentControlError("Stage Checkpoint artifact names must be unique")
    stage = cfg["orchestration"]["stage_plan"].get(state["lifecycle_state"])
    if not isinstance(stage, dict):
        raise AgentControlError(f"no lifecycle stage configured for {state['lifecycle_state']}")
    by_name = {row["name"]: row for row in artifacts}
    for configured in stage.get("artifacts", []):
        name = configured["name"]
        row = by_name.get(name)
        if row is None:
            raise AgentControlError(f"Stage Checkpoint missing configured canonical artifact: {name}")
        expected_path = _expand_stage_path(configured["path"], profile)
        if row["path"] != expected_path:
            raise AgentControlError(f"Stage Checkpoint artifact path is not canonical for {name}: {expected_path}")


def _load_reviews(repo_root: Path, path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        return []
    payload = core.load_json(path)
    rows = payload.get("reviews")
    if not isinstance(rows, list):
        raise AgentControlError("review file must contain a reviews array")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise AgentControlError(f"reviews[{index}] must be an object")
        allowed = {"check_id", "kind", "executor", "evidence", "result_path"}
        if set(row) - allowed:
            raise AgentControlError(f"reviews[{index}] has unsupported fields")
        check_id = row.get("check_id")
        kind = row.get("kind")
        executor = row.get("executor")
        evidence_text = row.get("evidence")
        if not isinstance(check_id, str) or not check_id.strip() or check_id in seen:
            raise AgentControlError(f"reviews[{index}].check_id must be unique and non-empty")
        seen.add(check_id)
        if kind not in REVIEW_KINDS:
            raise AgentControlError(f"reviews[{index}].kind invalid")
        if not isinstance(executor, str) or not executor.strip() or not isinstance(evidence_text, str) or not evidence_text.strip():
            raise AgentControlError(f"reviews[{index}] executor/evidence required")
        result_path_value = row.get("result_path")
        result_ref = None
        if kind == "DETERMINISTIC":
            if not isinstance(result_path_value, str) or not result_path_value:
                raise AgentControlError(f"deterministic review {check_id} requires result_path")
            result_ref = _authority(repo_root, core.repo_local_path(repo_root, result_path_value, f"review result {check_id}"), f"review result {check_id}")
        elif result_path_value is not None:
            raise AgentControlError(f"agent review {check_id} must not claim deterministic result_path")
        result.append({
            "check_id": check_id,
            "kind": kind,
            "status": "PASS",
            "executor": executor,
            "evidence": evidence_text,
            "result": result_ref,
        })
    return result


def build_stage_checkpoint(
    repo_root: Path,
    cfg: dict[str, Any],
    state_path: Path,
    artifacts: dict[str, Path],
    reviews_path: Path | None,
    summary: str,
    recorded_at: datetime,
    implementation_sha: str | None = None,
) -> Path:
    state = core.load_json(state_path)
    verify_agent_state_basis(repo_root, cfg, state)
    if state.get("terminal_reason") is not None:
        raise AgentControlError(f"cannot advance while State is terminal: {state['terminal_reason']}")
    stage = cfg["orchestration"]["stage_plan"].get(state["lifecycle_state"])
    if not isinstance(stage, dict):
        raise AgentControlError(f"no stage configured for {state['lifecycle_state']}")
    if stage.get("action_kind") == "WORKFLOW_DISPATCH":
        raise AgentControlError("external WORKFLOW_DISPATCH stage must use its dedicated workflow")
    if not isinstance(summary, str) or not summary.strip():
        raise AgentControlError("Stage Checkpoint summary required")
    _, profile, _ = _profile_and_source(repo_root, cfg, state)
    artifact_rows = [_named_authority(repo_root, name, path) for name, path in sorted(artifacts.items())]
    _validate_stage_artifacts(repo_root, cfg, state, profile, artifact_rows)
    reviews = _load_reviews(repo_root, reviews_path)
    if not reviews:
        raise AgentControlError("Stage Checkpoint requires at least one deterministic or ChatGPT review row")
    impl = core.repository_commit_sha(repo_root, implementation_sha)
    current_contract = core.contract_identity(repo_root, cfg, state["research_profile"], state["publication_profile"])
    _validate_core_stage_report(
        repo_root,
        cfg,
        state,
        artifact_rows,
        reviews,
        state_path=state_path,
        expected_contract=current_contract,
        expected_implementation_sha=impl,
    )
    payload = {
        "schema_version": "2.0-rc1",
        "issue_id": state["issue_id"],
        "from_state": state["lifecycle_state"],
        "to_state": stage["next_state"],
        "checkpoints": list(stage.get("checkpoints", [])),
        "recorded_at": core.iso_utc(recorded_at),
        "implementation": {
            "repository_commit_sha": impl,
            "orchestrator_version": cfg["orchestrator_version"],
        },
        "contract": current_contract,
        "artifacts": artifact_rows,
        "reviews": reviews,
        "summary": summary,
    }
    schema_gate.validate_instance(payload, repo_root / CHECKPOINT_SCHEMA, label="Agent Stage Checkpoint")
    path = canonical_checkpoint_path(repo_root, cfg, state)
    if path.exists():
        if core.load_json(path) != payload:
            raise AgentControlError(f"refusing divergent Stage Checkpoint overwrite: {path}")
    else:
        core.write_json(path, payload)
    return path


def advance_with_checkpoint(repo_root: Path, cfg: dict[str, Any], state_path: Path, checkpoint_path: Path) -> dict[str, Any]:
    state = core.load_json(state_path)
    verify_agent_state_basis(repo_root, cfg, state)
    canonical = canonical_checkpoint_path(repo_root, cfg, state)
    if checkpoint_path.resolve() != canonical.resolve():
        raise AgentControlError(f"Stage Checkpoint must use canonical path: {_rel(repo_root, canonical, 'Stage Checkpoint')}")
    record = schema_gate.load_and_validate_json(checkpoint_path, repo_root / CHECKPOINT_SCHEMA, label="Agent Stage Checkpoint")
    stage = cfg["orchestration"]["stage_plan"].get(state["lifecycle_state"])
    if not isinstance(stage, dict):
        raise AgentControlError(f"no stage configured for {state['lifecycle_state']}")
    if record["issue_id"] != state["issue_id"] or record["from_state"] != state["lifecycle_state"] or record["to_state"] != stage["next_state"]:
        raise AgentControlError("Stage Checkpoint does not match current lifecycle")
    if set(record["checkpoints"]) != set(stage.get("checkpoints", [])):
        raise AgentControlError("Stage Checkpoint checkpoint set does not match lifecycle contract")
    current_contract = core.contract_identity(repo_root, cfg, state["research_profile"], state["publication_profile"])
    if record["contract"] != current_contract:
        raise AgentControlError("Stage Checkpoint was not reviewed under the current repository contract")
    current_impl = core.repository_commit_sha(repo_root)
    if record["implementation"]["repository_commit_sha"] != current_impl or record["implementation"]["orchestrator_version"] != cfg["orchestrator_version"]:
        raise AgentControlError("Stage Checkpoint implementation identity differs from current executing tool")
    _, profile, _ = _profile_and_source(repo_root, cfg, state)
    _validate_stage_artifacts(repo_root, cfg, state, profile, record["artifacts"])
    _validate_core_stage_report(
        repo_root,
        cfg,
        state,
        record["artifacts"],
        record["reviews"],
        state_path=state_path,
        expected_contract=current_contract,
        expected_implementation_sha=current_impl,
    )
    if state["lifecycle_state"] == "FROZEN":
        _validate_release_reconciliation_review(
            repo_root,
            cfg,
            state,
            record["artifacts"],
            record["reviews"],
        )
    authority = _authority(repo_root, checkpoint_path, "Stage Checkpoint")
    updated = deepcopy(state)
    for checkpoint in stage.get("checkpoints", []):
        updated["machine_checkpoints"][checkpoint] = "passed"
        updated["checkpoint_provenance"][checkpoint] = deepcopy(authority)
    current = state["lifecycle_state"]
    updated["lifecycle_state"] = stage["next_state"]
    updated["history"].append({
        "from": current,
        "to": stage["next_state"],
        "recorded_at": record["recorded_at"],
        "repository_commit_sha": current_impl,
    })
    updated = core.refresh_state_control(updated, cfg)
    errors = validate_agent_state(repo_root, cfg, updated)
    if errors:
        raise AgentControlError("refusing inconsistent agent-first transition: " + "; ".join(errors))
    core.write_json(state_path, updated)
    return updated


def approve_architecture(
    repo_root: Path,
    cfg: dict[str, Any],
    state_path: Path,
    reviewed_by: str,
    reviewed_at: datetime,
    review_reference: str,
) -> dict[str, Any]:
    state = core.load_json(state_path)
    verify_agent_state_basis(repo_root, cfg, state)
    if state["lifecycle_state"] != "ARCHITECTURE_ESTABLISHED" or state["human_gates"]["architecture_review"] != "pending":
        raise AgentControlError("Architecture approval requires pending ARCHITECTURE_ESTABLISHED Human Gate")
    if state["machine_checkpoints"].get("architecture") != "passed":
        raise AgentControlError("Architecture approval requires completed Architecture checkpoint")
    if not reviewed_by.strip() or not review_reference.strip():
        raise AgentControlError("reviewed_by and review_reference are required")
    _, _, source_root = _profile_and_source(repo_root, cfg, state)
    architecture = source_root / "architecture-v2.json"
    review = source_root / "architecture-review-summary-v2.json"
    attention = source_root / "architecture-review-attention-v2.json"
    for path, label in ((architecture, "Architecture"), (review, "Architecture Review Summary"), (attention, "Architecture Review Attention")):
        if not path.is_file():
            raise AgentControlError(f"{label} missing: {path}")
    review_attention.validate_attention(repo_root, attention)
    plan = core.load_json(architecture)
    summary = core.load_json(review)
    if plan.get("issue_id") != state["issue_id"] or plan.get("status") != "PROPOSED":
        raise AgentControlError("Architecture Human Gate requires immutable PROPOSED Architecture for this issue")
    if summary.get("issue_id") != state["issue_id"] or summary.get("readiness", {}).get("status") != "READY_FOR_ARCHITECTURE_REVIEW":
        raise AgentControlError("Architecture Review Summary is not ready for this issue")
    if summary.get("basis", {}).get("architecture_sha256") != core.sha256_file(architecture):
        raise AgentControlError("Architecture Review Summary does not bind exact Architecture bytes")
    approval_path = source_root / cfg["state_authority"]["architecture_approval_path"]
    seed = {
        "issue_id": state["issue_id"],
        "architecture_sha256": core.sha256_file(architecture),
        "review_summary_sha256": core.sha256_file(review),
        "review_attention_sha256": core.sha256_file(attention),
        "reviewed_at": core.iso_utc(reviewed_at),
        "review_reference": review_reference,
    }
    approval = {
        "schema_version": "2.0-rc1",
        "approval_id": f"approval:{state['issue_id']}:{core.sha256_object(seed)[:20]}",
        "issue_id": state["issue_id"],
        "gate": "ARCHITECTURE_REVIEW",
        "decision": "APPROVED",
        "architecture_sha256": core.sha256_file(architecture),
        "architecture_review_summary_sha256": core.sha256_file(review),
        "architecture_review_attention_sha256": core.sha256_file(attention),
        "reviewed_by": reviewed_by,
        "reviewed_at": core.iso_utc(reviewed_at),
        "review_reference": review_reference,
    }
    approval_errors = drafting.validate_architecture_approval(approval, architecture, review, state["issue_id"])
    if approval_errors:
        raise AgentControlError("Architecture Approval Record invalid: " + "; ".join(approval_errors))
    if approval_path.exists() and core.load_json(approval_path) != approval:
        raise AgentControlError("refusing divergent Architecture Approval overwrite")
    if not approval_path.exists():
        core.write_json(approval_path, approval)
    updated = deepcopy(state)
    updated["human_gates"]["architecture_review"] = "approved"
    updated["human_gate_provenance"]["architecture_review"] = _authority(repo_root, approval_path, "Architecture approval")
    updated = core.refresh_state_control(updated, cfg)
    errors = validate_agent_state(repo_root, cfg, updated)
    if errors:
        raise AgentControlError("refusing inconsistent Architecture approval State: " + "; ".join(errors))
    core.write_json(state_path, updated)
    return updated


def approve_publication_preview(
    repo_root: Path,
    cfg: dict[str, Any],
    state_path: Path,
    reviewed_by: str,
    reviewed_at: datetime,
    review_reference: str,
) -> dict[str, Any]:
    state = core.load_json(state_path)
    verify_agent_state_basis(repo_root, cfg, state)
    if state["lifecycle_state"] != "RELEASE_CANDIDATE" or state["human_gates"]["publication_preview"] != "pending":
        raise AgentControlError("Publication Preview approval requires pending RELEASE_CANDIDATE Human Gate")
    if not reviewed_by.strip() or not review_reference.strip():
        raise AgentControlError("reviewed_by and review_reference are required")
    _, _, source_root = _profile_and_source(repo_root, cfg, state)
    candidate = source_root / "publication/v2/publication-candidate-v2.json"
    if not candidate.is_file():
        raise AgentControlError("canonical Publication Candidate missing")
    publication.validate_candidate(repo_root, candidate, issue_id=state["issue_id"])
    approval_path = source_root / cfg["state_authority"]["publication_preview_approval_path"]
    publication.build_preview_approval(repo_root, candidate, approval_path, reviewed_by, reviewed_at, review_reference)
    updated = deepcopy(state)
    updated["human_gates"]["publication_preview"] = "approved"
    approval_authority = _authority(repo_root, approval_path, "Publication Preview approval")
    updated["human_gate_provenance"]["publication_preview"] = approval_authority
    updated["machine_checkpoints"]["publication_preview"] = "passed"
    updated["checkpoint_provenance"]["publication_preview"] = deepcopy(approval_authority)
    updated = core.refresh_state_control(updated, cfg)
    errors = validate_agent_state(repo_root, cfg, updated)
    if errors:
        raise AgentControlError("refusing inconsistent Publication Preview approval State: " + "; ".join(errors))
    core.write_json(state_path, updated)
    return updated


def _verify_preserved_provenance(
    repo_root: Path,
    cfg: dict[str, Any],
    state: dict[str, Any],
    validation_ref: dict[str, str],
    superseded: list[dict[str, Any]],
) -> None:
    """Verify every checkpoint-bound byte except explicitly superseded publication rows.

    Mirrors the artifact and deterministic-review-result checks of ordinary basis
    validation across the whole checkpoint provenance, so no upstream mutation can
    be smuggled into a publication revalidation. Raises AgentControlError.
    """
    sup = {(row["name"], row["path"]): row["new_sha256"] for row in superseded}
    seen: set[str] = set()
    for name, authority in state.get("checkpoint_provenance", {}).items():
        if authority is None:
            continue
        try:
            path = core.repo_local_path(repo_root, authority["path"], f"checkpoint {name}")
        except (TypeError, ValueError) as exc:
            raise AgentControlError(str(exc)) from exc
        if not path.is_file() or core.sha256_file(path) != authority.get("sha256"):
            raise AgentControlError(f"checkpoint {name} provenance drift during revalidation")
        try:
            record = schema_gate.load_and_validate_json(
                path, repo_root / CHECKPOINT_SCHEMA, label=f"revalidation basis checkpoint {name}"
            )
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            raise AgentControlError(f"basis checkpoint unreadable: {exc}") from exc
        if record.get("issue_id") != state.get("issue_id"):
            raise AgentControlError(f"basis checkpoint issue identity mismatch: {name}")
        is_bound = authority.get("path") == validation_ref.get("path")
        for row in record.get("artifacts", []):
            key = (row.get("name"), row.get("path"))
            try:
                resolved = core.repo_local_path(repo_root, row["path"], f"basis artifact {row.get('name')}")
            except (TypeError, ValueError) as exc:
                raise AgentControlError(str(exc)) from exc
            expected = sup.get(key, row.get("sha256")) if is_bound else row.get("sha256")
            if not resolved.is_file() or core.sha256_file(resolved) != expected:
                if is_bound and key in sup:
                    raise AgentControlError(f"revalidated publication artifact drift during revalidation: {key[0]}")
                raise AgentControlError(f"upstream artifact drift outside publication surface: {key[0]}")
        for review in record.get("reviews", []):
            if review.get("kind") != "DETERMINISTIC":
                continue
            result = review.get("result")
            if not isinstance(result, dict):
                raise AgentControlError(f"deterministic review lacks result authority: {review.get('check_id')}")
            try:
                result_path = core.repo_local_path(repo_root, result["path"], f"review result {review.get('check_id')}")
            except (TypeError, ValueError) as exc:
                raise AgentControlError(str(exc)) from exc
            if not result_path.is_file() or core.sha256_file(result_path) != result.get("sha256"):
                raise AgentControlError(f"deterministic review result drift: {review.get('check_id')}")
        seen.add(name)


def _reject_symlink_ancestors_reval(repo_root: Path, path: Path, label: str) -> None:
    """Reject symlink ancestors/aliases for owned revalidation writes.

    Walks lexical components from the resolved repo root to the target's
    parent, refusing any symlink component. The target itself must not be a
    symlink either. This prevents retention/guard/temp/live writes escaping
    the repository via an aliased directory. Does not claim global CAS or
    power-loss durability beyond the selected exclusive-create/replace ops.
    """
    root = repo_root.resolve()
    # Lexical safety before resolve: no absolute escape via .. is handled by
    # core.repo_local_path for derived paths, but double-check ancestors here.
    current = root
    try:
        rel = path.parent.relative_to(root) if path.is_absolute() else path.parent
        # If path is already absolute under root, walk its components.
        if path.is_absolute():
            try:
                rel_parts = path.parent.relative_to(root).parts
            except ValueError as exc:
                raise AgentControlError(f"{label} escapes repository root: {path}") from exc
            for part in rel_parts:
                if part in ("..", "."):
                    raise AgentControlError(f"{label} has unsafe path component: {part}")
                current = current / part
                if current.is_symlink():
                    raise AgentControlError(f"{label} has symlinked ancestor component: {current}")
        else:
            # Relative path: walk from root.
            for part in path.parent.parts:
                if part in ("..", "."):
                    raise AgentControlError(f"{label} has unsafe path component: {part}")
                if Path(part).is_absolute():
                    continue
                current = current / part
                if current.is_symlink():
                    raise AgentControlError(f"{label} has symlinked ancestor component: {current}")
    except AgentControlError:
        raise
    except Exception as exc:
        raise AgentControlError(f"{label} ancestor check failed: {exc}") from exc
    if path.is_symlink():
        raise AgentControlError(f"{label} is a symlink/refusal: {path}")


def _exclusive_create_record_bytes(record_path: Path, expected: bytes, label: str) -> None:
    """Create a new revalidation record exclusively from known expected bytes.

    Uses atomic exclusive ``xb`` creation only; no prior exists-check is
    trusted. On FileExistsError raises collision without touching foreign
    bytes. Verifies written bytes equal expected before returning; a partial
    write that does not match expected is retained fail-closed by the caller.
    """
    record_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(record_path, "xb") as fh:
            fh.write(expected)
            fh.flush()
            try:
                os.fsync(fh.fileno())
            except OSError:
                pass
    except FileExistsError as exc:
        raise AgentControlError(f"publication revalidation sequence collision: {record_path}") from exc
    # Verify exclusive bytes are exactly the expected serialization, not
    # whatever happened to be on disk after a race.
    try:
        actual = record_path.read_bytes()
    except OSError as exc:
        raise AgentControlError(f"revalidation record readback failed: {exc}") from exc
    if actual != expected:
        raise AgentControlError(
            f"revalidation record bytes mismatch after exclusive create: {record_path}; "
            "live bytes preserved for manual recovery"
        )


def _atomic_replace_state_bytes(state_path: Path, expected_old: bytes, new_bytes: bytes, label: str) -> None:
    """Replace State atomically from known serialized bytes via temp+replace.

    Rechecks current live bytes equal expected_old immediately before
    replacement; refuses on drift without blessing changed bytes. Temp file is
    created exclusively in the same directory, fsynced, verified, then
    atomically replaced. No truncating write_json is used for live State.
    """
    try:
        current = state_path.read_bytes()
    except OSError as exc:
        raise AgentControlError(f"{label} read failed before replace: {exc}") from exc
    if current != expected_old:
        raise AgentControlError(
            f"{label} drift before replace; live bytes preserved for manual recovery"
        )
    tmp = state_path.parent / f".{state_path.name}.tmp-reval-{core.sha256_bytes(new_bytes)[:16]}"
    if tmp.is_symlink() or tmp.exists():
        raise AgentControlError(f"{label} temp collision: {tmp}")
    try:
        with open(tmp, "xb") as fh:
            fh.write(new_bytes)
            fh.flush()
            try:
                os.fsync(fh.fileno())
            except OSError:
                pass
            try:
                _tmp_fst = os.fstat(fh.fileno())
                tmp_id: tuple[int, int] | None = (_tmp_fst.st_dev, _tmp_fst.st_ino)
            except OSError as exc:
                raise AgentControlError(f"{label} temp identity capture failed: {exc}") from exc
    except FileExistsError as exc:
        raise AgentControlError(f"{label} temp collision: {tmp}") from exc

    def _drop_own_temp() -> None:
        """Remove the temp file only if it is still our exclusive creation.

        Unknown temp bytes (identity mismatch or unreadable) are retained,
        never unlinked as potentially foreign.
        """
        try:
            if tmp.is_symlink():
                return
            cur = os.stat(tmp)
            if tmp_id is not None and (cur.st_dev, cur.st_ino) != tmp_id:
                return
            tmp.unlink(missing_ok=True)
        except OSError:
            pass

    try:
        if tmp.read_bytes() != new_bytes:
            _drop_own_temp()
            raise AgentControlError(f"{label} temp bytes mismatch; live bytes untouched")
    except OSError as exc:
        if isinstance(exc, AgentControlError):
            raise
        raise AgentControlError(f"{label} temp readback failed: {exc}") from exc
    # Re-verify live still equals expected_old immediately before replace
    # (detected interleave between temp write and replace).
    try:
        if state_path.read_bytes() != expected_old:
            _drop_own_temp()
            raise AgentControlError(
                f"{label} drift before replace; live bytes preserved for manual recovery"
            )
    except OSError as exc:
        if isinstance(exc, AgentControlError):
            raise
        _drop_own_temp()
        raise AgentControlError(f"{label} pre-replace recheck failed: {exc}") from exc
    try:
        os.replace(tmp, state_path)
    except OSError as exc:
        raise AgentControlError(f"{label} replace failed; live bytes preserved for manual recovery: {exc}") from exc
    try:
        if state_path.read_bytes() != new_bytes:
            raise AgentControlError(f"{label} post-replace mismatch; manual recovery required")
    except OSError as exc:
        if isinstance(exc, AgentControlError):
            raise
        raise AgentControlError(f"{label} post-replace readback failed: {exc}") from exc


def revalidate_publication_surface(
    repo_root: Path,
    cfg: dict[str, Any],
    state_path: Path,
    reason_class: str,
    reason: str,
    executor: str,
    recorded_at: datetime,
    implementation_sha: str | None = None,
) -> Path:
    """Establish new immutable authority for legitimately regenerated publication bytes.

    Historical checkpoints are never rewritten. The new record explicitly
    supersedes the prior validation checkpoint for bounded publication-surface
    roles only; every other checkpoint-bound byte must match exactly.
    """
    if reason_class not in REVALIDATION_REASON_CLASSES:
        raise AgentControlError(f"publication revalidation reason class unrecognized: {reason_class}")
    if not isinstance(reason, str) or not reason.strip():
        raise AgentControlError("publication revalidation requires a non-empty reason")
    if not isinstance(executor, str) or not executor.strip():
        raise AgentControlError("publication revalidation requires executor identity")
    state = core.load_json(state_path)
    active, active_errors = resolve_active_publication_revalidation(repo_root, cfg, state)
    if active is not None and not active_errors:
        raise AgentControlError("active publication revalidation already validates current bytes; nothing to supersede")
    if state.get("lifecycle_state") != "VALIDATED_DRAFT":
        raise AgentControlError("publication revalidation requires VALIDATED_DRAFT lifecycle")
    if state.get("human_gates", {}).get("architecture_review") != "approved":
        raise AgentControlError("publication revalidation requires approved Architecture Review")
    if state.get("human_gates", {}).get("publication_preview") != "pending":
        raise AgentControlError("publication revalidation requires pending Publication Preview")
    if state.get("human_gate_provenance", {}).get("publication_preview") is not None:
        raise AgentControlError("publication revalidation forbids existing Publication Preview provenance")
    for gate in ("publication_preview", "freeze", "release"):
        if state.get("machine_checkpoints", {}).get(gate) != "pending":
            raise AgentControlError(f"publication revalidation forbids resolved {gate} checkpoint")
    exception = state.get("exception_gate", {})
    if exception.get("status") != "inactive":
        raise AgentControlError("publication revalidation forbids active Exception Gate")
    _, profile, source_root = _profile_and_source(repo_root, cfg, state)
    approval_path = source_root / cfg["state_authority"]["architecture_approval_path"]
    arch_auth = state.get("human_gate_provenance", {}).get("architecture_review")
    if (
        not isinstance(arch_auth, dict)
        or arch_auth.get("path") != _rel(repo_root, approval_path, "Architecture approval")
        or not approval_path.is_file()
        or core.sha256_file(approval_path) != arch_auth.get("sha256")
    ):
        raise AgentControlError("publication revalidation requires intact Architecture approval provenance")
    validation_ref = state.get("checkpoint_provenance", {}).get("validation")
    if not isinstance(validation_ref, dict) or set(validation_ref) != {"path", "sha256"}:
        raise AgentControlError("publication revalidation requires validation checkpoint provenance")
    try:
        prior_path = core.repo_local_path(repo_root, validation_ref["path"], "validation checkpoint")
    except (TypeError, ValueError) as exc:
        raise AgentControlError(str(exc)) from exc
    if not prior_path.is_file() or core.sha256_file(prior_path) != validation_ref.get("sha256"):
        raise AgentControlError("validation checkpoint provenance drift")
    try:
        prior_record = schema_gate.load_and_validate_json(
            prior_path, repo_root / CHECKPOINT_SCHEMA, label="revalidation prior Stage Checkpoint"
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise AgentControlError(f"validation checkpoint unreadable: {exc}") from exc
    pending_basis = built_checked_pending_publication_basis(repo_root, cfg, state_path)
    if implementation_sha is not None and implementation_sha != pending_basis.head:
        raise AgentControlError("publication revalidation implementation must be actual current HEAD")
    publication_dir, survey_root = _revalidation_surface_roots(repo_root, cfg, state)
    superseded: list[dict[str, Any]] = []
    preserved: list[dict[str, Any]] = []
    for row in prior_record.get("artifacts", []):
        name, raw = row.get("name"), row.get("path")
        try:
            resolved = core.repo_local_path(repo_root, raw, f"prior artifact {name}")
        except (TypeError, ValueError) as exc:
            raise AgentControlError(str(exc)) from exc
        if not resolved.is_file():
            raise AgentControlError(f"prior publication artifact missing: {name}")
        current_sha = core.sha256_file(resolved)
        under_surface = False
        for root_dir in (publication_dir, survey_root):
            try:
                resolved.resolve().relative_to(root_dir)
                under_surface = True
            except ValueError:
                continue
        if under_surface:
            if current_sha == row.get("sha256"):
                preserved.append({"name": name, "path": raw, "sha256": current_sha})
            else:
                superseded.append({
                    "name": name,
                    "path": raw,
                    "prior_sha256": row.get("sha256"),
                    "new_sha256": current_sha,
                    "byte_count": resolved.stat().st_size,
                })
        elif current_sha != row.get("sha256"):
            raise AgentControlError(f"upstream artifact drift outside publication surface: {name}")
        else:
            preserved.append({"name": name, "path": raw, "sha256": current_sha})
    if not superseded:
        raise AgentControlError("publication revalidation requires at least one regenerated publication artifact")
    expected_superseded = [
        {"name": name, "path": path, "prior_sha256": old, "new_sha256": new, "byte_count": size}
        for name, path, old, new, size in pending_basis.replacements
    ]
    expected_preserved = [
        {"name": name, "path": path, "sha256": sha}
        for name, path, sha in pending_basis.preserved
    ]
    if superseded != expected_superseded or preserved != expected_preserved:
        raise AgentControlError("publication revalidation rows differ from checked pending context")
    _verify_preserved_provenance(repo_root, cfg, state, validation_ref, superseded)
    publication_rows = superseded + preserved

    def unique_publication_path(name: str) -> Path:
        matches = [row for row in publication_rows if row.get("name") == name]
        if len(matches) != 1:
            raise AgentControlError(
                f"publication revalidation requires exactly one {name} artifact; found {len(matches)}"
            )
        return _revalidation_row_path(repo_root, matches[0]["path"], f"revalidation {name}")

    manuscript_path = unique_publication_path("reader-manuscript")
    gate_path = unique_publication_path("reader-surface-gate")
    manuscript_doc = bundle_doc = semantic_doc = visual_doc = None
    bundle_checks: list[dict[str, str]] = []
    bound_paths: dict[str, Path] = {}
    try:
        manuscript_doc = reader.validate_manuscript_manifest(
            repo_root, manuscript_path, issue_id=state["issue_id"]
        )
        bound_paths["manuscript"] = manuscript_path
        for row in publication_rows:
            path = core.repo_local_path(repo_root, row["path"], row["name"])
            if row["name"] == "quality-regression-bundle":
                bundle_doc = quality.validate_bundle(repo_root, path, issue_id=state["issue_id"])
                bound_paths["quality_bundle"] = path
    except ValueError as exc:
        raise AgentControlError(f"publication revalidation QA failed: {exc}") from exc
    if manuscript_doc is None or bundle_doc is None:
        raise AgentControlError("publication revalidation requires bound reader manuscript and quality bundle")
    try:
        for row in publication_rows:
            path = core.repo_local_path(repo_root, row["path"], row["name"])
            if row["name"] == "semantic-review":
                semantic_doc = reader.validate_review_record(repo_root, path, issue_id=state["issue_id"], expected_kind="SEMANTIC_EDITORIAL")
                bound_paths["semantic_review"] = path
            elif row["name"] == "visual-review":
                visual_doc = reader.validate_review_record(repo_root, path, issue_id=state["issue_id"], expected_kind="VISUAL")
                bound_paths["visual_review"] = path
    except ValueError as exc:
        raise AgentControlError(f"publication revalidation QA failed: {exc}") from exc
    if semantic_doc is None or visual_doc is None:
        raise AgentControlError("publication revalidation requires complete semantic and visual reviews")
    try:
        surface_gate.validate_reader_surface_gate(
            repo_root,
            gate_path,
            issue_id=state["issue_id"],
            publication_profile=profile["publication_profile"],
            expected_manuscript_path=manuscript_path,
            state_path=state_path,
        )
    except ValueError as exc:
        raise AgentControlError(f"publication revalidation Reader-Surface Gate failed: {exc}") from exc
    for check in bundle_doc.get("checks", []):
        if check.get("status") != "PASS":
            raise AgentControlError(f"publication revalidation quality check not PASS: {check.get('check_id')}")
        bundle_checks.append({"check_id": check.get("check_id"), "status": "PASS"})
    pdf_ref = bundle_doc.get("pdf", {})
    sequences = _revalidation_existing_sequences(repo_root, cfg, state)
    supersedes: dict[str, str] | None = None
    pointer = state.get("publication_revalidation_provenance")
    if pointer is not None:
        predecessor, predecessor_errors = _resolve_publication_revalidation(repo_root, cfg, state, live=False)
        if predecessor is None or predecessor_errors:
            raise AgentControlError("publication revalidation predecessor invalid: " + "; ".join(predecessor_errors))
        supersedes = {"path": pending_basis.predecessor_path, "sha256": pending_basis.predecessor_sha256}
    sequence = (max(sequences) + 1) if sequences else 1
    record_path = _revalidation_record_path(repo_root, cfg, state, sequence)
    if record_path.exists() or record_path.is_symlink():
        raise AgentControlError("publication revalidation sequence collision")
    establishment_state_sha = core.sha256_file(state_path)
    payload = {
        "schema_version": "2.0-rc1",
        "issue_id": state["issue_id"],
        "reason_class": reason_class,
        "reason": reason.strip(),
        "lifecycle": "VALIDATED_DRAFT",
        "prior_checkpoint": {"path": validation_ref["path"], "sha256": validation_ref["sha256"]},
        "superseded_artifacts": superseded,
        "preserved_artifacts": preserved,
        "validation": {
            "manuscript": _authority(repo_root, bound_paths["manuscript"], "revalidation manuscript"),
            "quality_bundle": _authority(repo_root, bound_paths["quality_bundle"], "revalidation quality bundle"),
            "semantic_review": _authority(repo_root, bound_paths["semantic_review"], "revalidation semantic review"),
            "visual_review": _authority(repo_root, bound_paths["visual_review"], "revalidation visual review"),
            "pdf": {"path": pdf_ref.get("path"), "sha256": pdf_ref.get("sha256"), "byte_count": pdf_ref.get("byte_count"), "page_count": semantic_doc.get("page_count")},
            "deterministic_checks": bundle_checks,
            "summary": f"post-VALIDATED_DRAFT publication-surface revalidation ({reason_class}): {len(superseded)} artifact(s) rebound with complete fresh QA; upstream authority preserved byte-identical",
        },
        "core": {
            "contract": core.contract_identity(repo_root, cfg, state["research_profile"], state["publication_profile"]),
            "implementation_commit_sha": pending_basis.head,
        },
        "executor": executor.strip(),
        "recorded_at": core.iso_utc(recorded_at),
        "supersedes": supersedes,
        "establishment": {
            "state_sha256": establishment_state_sha,
            "lifecycle": "VALIDATED_DRAFT",
            "architecture_review": "approved",
            "publication_preview": "pending",
            "freeze": "pending",
            "release": "pending",
            "implementation_commit_sha": pending_basis.head,
            "recorded_at": core.iso_utc(recorded_at),
        },
    }
    schema_gate.validate_instance(payload, repo_root / REVALIDATION_SCHEMA, label="Publication Surface Revalidation")
    final_errors = _validate_agent_state(repo_root, cfg, state, pending_basis)
    if final_errors:
        raise AgentControlError("pending publication basis changed before write: " + "; ".join(final_errors))
    original_state_bytes = state_path.read_bytes()
    if core.sha256_bytes(original_state_bytes) != pending_basis.state_sha256:
        raise AgentControlError("pending publication State bytes changed before write")
    # Known expected serializations (hashes are of expected bytes, never read-after-write blessing).
    record_bytes = core.json_bytes(payload)
    expected_record_sha = core.sha256_bytes(record_bytes)
    updated = deepcopy(state)
    updated["publication_revalidation_provenance"] = {
        "path": str(record_path.resolve().relative_to(repo_root.resolve())),
        "sha256": expected_record_sha,
    }
    state_bytes = core.json_bytes(updated)
    expected_state_sha = core.sha256_bytes(state_bytes)
    # Pre-mutation snapshot/basis recheck + ancestor safety (immediately before mutation).
    _reject_symlink_ancestors_reval(repo_root, record_path, "revalidation record")
    _reject_symlink_ancestors_reval(repo_root, state_path, "revalidation State")
    basis_recheck = _validate_agent_state(repo_root, cfg, core.load_json(state_path), pending_basis)
    if basis_recheck:
        raise AgentControlError("pending publication basis changed before write: " + "; ".join(basis_recheck))
    if core.sha256_bytes(state_path.read_bytes()) != pending_basis.state_sha256:
        raise AgentControlError("pending publication State bytes changed before write")
    if core.repository_commit_sha(repo_root) != pending_basis.head:
        raise AgentControlError("pending publication HEAD changed before write")
    if record_path.is_symlink() or record_path.exists():
        raise AgentControlError(f"publication revalidation sequence collision: {record_path}")
    created = False
    wrote_state = False
    try:
        _reject_symlink_ancestors_reval(repo_root, record_path, "revalidation record")
        _reject_symlink_ancestors_reval(repo_root, state_path, "revalidation State")
        # Exclusive record creation from known bytes (no exists-then-write TOCTOU).
        _exclusive_create_record_bytes(record_path, record_bytes, "revalidation record")
        created = True
        # Bounded temp+replace State from known bytes (no truncating write_json).
        _atomic_replace_state_bytes(state_path, original_state_bytes, state_bytes, "revalidation State")
        wrote_state = True
        post_errors = validate_agent_state(repo_root, cfg, core.load_json(state_path))
        if post_errors:
            raise AgentControlError("resulting revalidation State invalid: " + "; ".join(post_errors))
    except Exception as exc:
        # Owner-aware cleanup/restore; never delete unknown bytes; preserve cause.
        # Symlink ancestors are rechecked immediately here (not only at API
        # start): rollback must not traverse a swapped alias.
        try:
            _reject_symlink_ancestors_reval(repo_root, record_path, "revalidation record rollback")
            _reject_symlink_ancestors_reval(repo_root, state_path, "revalidation State rollback")
        except AgentControlError as alias_exc:
            raise AgentControlError(
                f"revalidation rollback refused unsafe path at rollback time; "
                f"live bytes preserved for manual recovery: {alias_exc}"
            ) from exc
        # Classify the ACTUAL State disposition regardless of the helper return
        # flag: os.replace may have succeeded before a post-rename readback
        # raised, leaving wrote_state=False while live State already references
        # the new record. The record must be preserved whenever State might
        # still reference it (exact known new, unknown, or unreadable).
        try:
            _cur_state: bytes | None = state_path.read_bytes()
        except OSError:
            _cur_state = None
        _state_is_original = _cur_state == original_state_bytes
        _state_is_new = _cur_state == state_bytes
        if _cur_state is None or (not _state_is_original and not _state_is_new):
            # Unknown/unreadable/foreign State: it might reference the record.
            # Preserve everything, delete nothing.
            if created:
                raise AgentControlError(
                    f"revalidation State disposition unknown after failure at {state_path}; "
                    "owned record preserved because State might still reference it, manual recovery required"
                ) from exc
            try:
                _exists_now = record_path.is_file() or record_path.is_symlink()
            except OSError:
                _exists_now = False
            if _exists_now:
                msg = str(exc)
                if "collision" in msg.lower() or "sequence collision" in msg:
                    raise
                raise AgentControlError(
                    f"revalidation left unknown record bytes at {record_path} with unknown State disposition; "
                    "no deletion performed, manual recovery required"
                ) from exc
            raise
        if _state_is_new:
            # Replacement succeeded (even if the helper raised on post-rename
            # readback): roll State back to original first, then handle record.
            try:
                _atomic_replace_state_bytes(state_path, state_bytes, original_state_bytes, "revalidation State rollback")
            except AgentControlError as rollback_exc:
                raise AgentControlError(
                    f"revalidation State rollback failed at {state_path}; owned record preserved because "
                    f"State might still reference it, manual recovery required: {rollback_exc}"
                ) from exc
            # State is original again: the record is now orphaned. Delete only
            # if it still holds exactly our known bytes.
            if created:
                if record_path.is_symlink():
                    raise AgentControlError(
                        f"revalidation rollback refused symlink record at {record_path}; manual recovery required"
                    ) from exc
                if not record_path.is_file():
                    raise AgentControlError(
                        f"revalidation record missing after failure at {record_path}; manual recovery required"
                    ) from exc
                try:
                    cur_record = record_path.read_bytes()
                except OSError as read_exc:
                    raise AgentControlError(
                        f"revalidation rollback refused unreadable record at {record_path}; manual recovery required"
                    ) from exc
                if cur_record != record_bytes:
                    raise AgentControlError(
                        f"revalidation rollback refused changed record bytes at {record_path} "
                        f"(expected {expected_record_sha[:16]}..); tampered evidence preserved, manual recovery required"
                    ) from exc
                try:
                    record_path.unlink()
                except OSError as unlink_exc:
                    raise AgentControlError(
                        f"revalidation record cleanup failed at {record_path}; manual recovery required: {unlink_exc}"
                    ) from exc
            else:
                try:
                    _exists_now2 = record_path.is_file() or record_path.is_symlink()
                except OSError:
                    _exists_now2 = False
                if _exists_now2:
                    msg2 = str(exc)
                    if "collision" in msg2.lower() or "sequence collision" in msg2:
                        raise
                    raise AgentControlError(
                        f"revalidation left unknown record bytes at {record_path}; "
                        "no deletion performed, manual recovery required"
                    ) from exc
            raise
        # State is original (replacement never happened): record handling only.
        if created:
            if record_path.is_symlink():
                raise AgentControlError(
                    f"revalidation rollback refused symlink record at {record_path}; manual recovery required"
                ) from exc
            if not record_path.is_file():
                raise AgentControlError(
                    f"revalidation record missing after failure at {record_path}; manual recovery required"
                ) from exc
            try:
                cur_record = record_path.read_bytes()
            except OSError as read_exc:
                raise AgentControlError(
                    f"revalidation rollback refused unreadable record at {record_path}; manual recovery required"
                ) from exc
            if cur_record != record_bytes:
                raise AgentControlError(
                    f"revalidation rollback refused changed record bytes at {record_path} "
                    f"(expected {expected_record_sha[:16]}..); tampered evidence preserved, manual recovery required"
                ) from exc
            try:
                record_path.unlink()
            except OSError as unlink_exc:
                raise AgentControlError(
                    f"revalidation record cleanup failed at {record_path}; manual recovery required: {unlink_exc}"
                ) from exc
        else:
            # No owned record: a file that appeared during the attempt (partial write
            # mismatch or competitor between precheck and exclusive create) must be
            # preserved, never deleted as unknown.
            try:
                exists_now = record_path.is_file() or record_path.is_symlink()
            except OSError:
                exists_now = False
            if exists_now:
                msg = str(exc)
                if "collision" in msg.lower() or "sequence collision" in msg:
                    raise
                raise AgentControlError(
                    f"revalidation left unknown record bytes at {record_path}; "
                    "no deletion performed, manual recovery required"
                ) from exc
        raise
    return record_path


def _path(root: Path, value: str | None) -> Path | None:
    if value is None:
        return None
    path = Path(value)
    return path if path.is_absolute() else root / path


def _parse_artifacts(root: Path, values: list[str]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise AgentControlError("--artifact must use NAME=PATH")
        name, raw = value.split("=", 1)
        if not name or not raw or name in result:
            raise AgentControlError("--artifact names/paths must be unique and non-empty")
        result[name] = _path(root, raw)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--config", default=str(core.DEFAULT_CONFIG))
    sub = parser.add_subparsers(dest="command", required=True)

    advance = sub.add_parser("advance-stage")
    advance.add_argument("--state", required=True)
    advance.add_argument("--artifact", action="append", default=[])
    advance.add_argument("--reviews")
    advance.add_argument("--summary", required=True)
    advance.add_argument("--recorded-at")
    advance.add_argument("--implementation-sha")

    arch = sub.add_parser("approve-architecture")
    arch.add_argument("--state", required=True)
    arch.add_argument("--reviewed-by", required=True)
    arch.add_argument("--reviewed-at", required=True)
    arch.add_argument("--review-reference", required=True)

    preview = sub.add_parser("approve-publication-preview")
    preview.add_argument("--state", required=True)
    preview.add_argument("--reviewed-by", required=True)
    preview.add_argument("--reviewed-at", required=True)
    preview.add_argument("--review-reference", required=True)

    revalidate = sub.add_parser("revalidate-publication-surface")
    revalidate.add_argument("--state", required=True)
    revalidate.add_argument("--reason-class", required=True)
    revalidate.add_argument("--reason", required=True)
    revalidate.add_argument("--executor", required=True)
    revalidate.add_argument("--recorded-at")
    revalidate.add_argument("--implementation-sha")

    refresh = sub.add_parser("refresh-mechanical-evidence")
    refresh.add_argument("--state", required=True)
    refresh.add_argument("--reason", required=True)
    refresh.add_argument("--executor", required=True)
    refresh.add_argument("--recorded-at")

    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    config_path = _path(root, args.config)
    try:
        cfg = core.load_json(config_path)
        if args.command == "advance-stage":
            state_path = _path(root, args.state)
            checkpoint = build_stage_checkpoint(
                root,
                cfg,
                state_path,
                _parse_artifacts(root, args.artifact),
                _path(root, args.reviews),
                args.summary,
                core.parse_instant(args.recorded_at) if args.recorded_at else _now(),
                args.implementation_sha,
            )
            state = advance_with_checkpoint(root, cfg, state_path, checkpoint)
            print(json.dumps({
                "state": str(state_path.relative_to(root)),
                "checkpoint": str(checkpoint.relative_to(root)),
                "lifecycle_state": state["lifecycle_state"],
                "next_action": state["next_action"],
                "terminal_reason": state["terminal_reason"],
            }, indent=2))
            return 0
        if args.command == "approve-architecture":
            state_path = _path(root, args.state)
            state = approve_architecture(
                root,
                cfg,
                state_path,
                args.reviewed_by,
                core.parse_instant(args.reviewed_at),
                args.review_reference,
            )
            print(json.dumps({"state": str(state_path.relative_to(root)), "next_action": state["next_action"], "terminal_reason": state["terminal_reason"]}, indent=2))
            return 0
        if args.command == "approve-publication-preview":
            state_path = _path(root, args.state)
            state = approve_publication_preview(
                root,
                cfg,
                state_path,
                args.reviewed_by,
                core.parse_instant(args.reviewed_at),
                args.review_reference,
            )
            print(json.dumps({"state": str(state_path.relative_to(root)), "next_action": state["next_action"], "terminal_reason": state["terminal_reason"]}, indent=2))
            return 0
        if args.command == "revalidate-publication-surface":
            state_path = _path(root, args.state)
            record_path = revalidate_publication_surface(
                root,
                cfg,
                state_path,
                args.reason_class,
                args.reason,
                args.executor,
                core.parse_instant(args.recorded_at) if args.recorded_at else _now(),
                args.implementation_sha,
            )
            print(json.dumps({"state": str(state_path.relative_to(root)), "revalidation_record": str(record_path.relative_to(root))}, indent=2))
            return 0
        if args.command == "refresh-mechanical-evidence":
            # Scoped refresh-only hardening (no global core path-policy change):
            # refuse symlinked config ancestors BEFORE resolving the alias away.
            _config_raw_abs = config_path if config_path.is_absolute() else (root.resolve() / config_path)
            _cfg_cur = root.resolve()
            try:
                _cfg_parts = _config_raw_abs.parent.relative_to(_cfg_cur).parts
            except ValueError as exc:
                raise AgentControlError(f"refresh config escapes repository root: {config_path}") from exc
            for _part in _cfg_parts:
                _cfg_cur = _cfg_cur / _part
                if _cfg_cur.is_symlink():
                    raise AgentControlError(f"refresh config has symlinked ancestor component: {_cfg_cur}")
            if config_path.is_symlink():
                raise AgentControlError(f"refresh config is a symlink/refusal: {config_path}")
            canonical_config = (root / core.DEFAULT_CONFIG).resolve()
            if config_path.resolve() != canonical_config:
                raise AgentControlError("refresh-mechanical-evidence requires the canonical default config")
            # Lazy import: survey_weekly_derivation_v2 imports this controller at
            # top level, so a top-level refresh import would be circular.
            from scripts import survey_weekly_mechanical_refresh_v2 as refresh_owner
            state_path = _path(root, args.state)
            result = refresh_owner.refresh_mechanical_evidence(
                root,
                cfg,
                state_path,
                args.reason,
                args.executor,
                core.parse_instant(args.recorded_at) if args.recorded_at else _now(),
            )
            print(json.dumps(result, indent=2))
            return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
