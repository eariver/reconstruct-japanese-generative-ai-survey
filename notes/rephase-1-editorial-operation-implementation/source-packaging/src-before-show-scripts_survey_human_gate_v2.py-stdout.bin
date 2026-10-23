#!/usr/bin/env python3
"""Canonical Human Gate round-trip protocol for Survey Production Core v2.

Human judgment remains external. This module only records an explicit Human
APPROVED or REQUEST_CHANGES decision against exact reviewed bytes and applies
the deterministic lifecycle consequence.

APPROVED delegates to the existing exact-byte approval recorders. A routine
REQUEST_CHANGES decision records immutable review provenance, selectively
invalidates downstream checkpoint authority, removes only superseded canonical
authority that would block regeneration, and returns Production State to an
allowed regeneration boundary. Publication Preview corrections may explicitly
reopen Architecture Review when the Human-selected boundary is upstream of the
approved Architecture. This module never chooses the decision or boundary.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

from scripts import survey_agent_control_v2 as agent
from scripts import survey_production_v2 as core
from scripts import survey_publication_v2 as publication
from scripts import survey_review_attention_v2 as review_attention
from scripts import survey_schema_v2 as schema_gate

REVIEW_RECORD_SCHEMA = Path("schemas/human-gate-review-record-v2.schema.json")
REVIEW_INDEX_SCHEMA = Path("schemas/human-gate-review-index-v2.schema.json")
OPERATOR_INVALIDATION_SCHEMA = Path("schemas/operator-pending-gate-invalidation-v2.schema.json")
GATE_KEYS = {
    "ARCHITECTURE_REVIEW": "architecture_review",
    "PUBLICATION_PREVIEW": "publication_preview",
}
GATE_STATES = {
    "ARCHITECTURE_REVIEW": "ARCHITECTURE_ESTABLISHED",
    "PUBLICATION_PREVIEW": "RELEASE_CANDIDATE",
}
GATE_SLUGS = {
    "ARCHITECTURE_REVIEW": "architecture",
    "PUBLICATION_PREVIEW": "publication",
}


class HumanGateError(ValueError):
    pass


def _rel(repo_root: Path, path: Path) -> str:
    root = repo_root.resolve()
    resolved = path.resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError as exc:
        raise HumanGateError(f"path escapes repository: {path}") from exc


def _authority(repo_root: Path, path: Path) -> dict[str, str]:
    if path.is_symlink() or not path.is_file():
        raise HumanGateError(f"authority file missing or unsafe: {_rel(repo_root, path)}")
    return {"path": _rel(repo_root, path), "sha256": core.sha256_file(path)}


def _named_authority(repo_root: Path, name: str, path: Path) -> dict[str, str]:
    return {"name": name, **_authority(repo_root, path)}


def _state_context(
    repo_root: Path,
    cfg: dict[str, Any],
    state_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], Path]:
    state = core.load_json(state_path)
    agent.verify_agent_state_basis(repo_root, cfg, state)
    profile_path = core.repo_local_path(repo_root, state["profile"]["path"], "Production Profile")
    profile = core.load_json(profile_path)
    source_root = core.repo_local_path(repo_root, profile["paths"]["source_root"], "paths.source_root")
    expected_state = source_root / cfg["state_authority"]["authoritative_filename"]
    if state_path.resolve() != expected_state.resolve():
        raise HumanGateError("Human Gate protocol requires canonical Production State path")
    return state, profile, source_root


def _review_dir(source_root: Path, cfg: dict[str, Any]) -> Path:
    return source_root / cfg["state_authority"]["human_review_dir"]


def review_index_path(source_root: Path, cfg: dict[str, Any]) -> Path:
    return source_root / cfg["state_authority"]["human_review_index_path"]


def review_record_path(
    source_root: Path,
    cfg: dict[str, Any],
    gate: str,
    revision: int,
) -> Path:
    return _review_dir(source_root, cfg) / f"{GATE_SLUGS[gate]}-r{revision}.json"


def approval_snapshot_path(
    source_root: Path,
    cfg: dict[str, Any],
    gate: str,
    revision: int,
) -> Path:
    return _review_dir(source_root, cfg) / "approvals" / f"{GATE_SLUGS[gate]}-r{revision}.json"


def _reopens_architecture(regeneration_boundary: str | None) -> bool:
    if regeneration_boundary is None:
        return False
    return core.LIFECYCLE.index(regeneration_boundary) < core.LIFECYCLE.index("ARCHITECTURE_ESTABLISHED")


def _validate_review_index_semantics(
    repo_root: Path,
    payload: dict[str, Any],
    expected_issue_id: str,
) -> None:
    if payload.get("issue_id") != expected_issue_id:
        raise HumanGateError("Human Gate review index issue identity mismatch")
    expected_revision = {gate: 1 for gate in GATE_KEYS}
    approved_active = {gate: False for gate in GATE_KEYS}
    for row in payload.get("reviews", []):
        gate = row["gate"]
        revision = row["revision"]
        if approved_active[gate]:
            raise HumanGateError(f"Human Gate review index has review after active APPROVED decision: {gate}")
        if revision != expected_revision[gate]:
            raise HumanGateError(
                f"Human Gate review revisions must be contiguous for {gate}: expected {expected_revision[gate]}, got {revision}"
            )
        expected_revision[gate] += 1
        record_ref = row["record"]
        record_path = core.repo_local_path(repo_root, record_ref["path"], "Human Gate review record")
        if record_path.is_symlink() or not record_path.is_file():
            raise HumanGateError(f"Human Gate review record missing: {record_ref['path']}")
        if core.sha256_file(record_path) != record_ref["sha256"]:
            raise HumanGateError(f"Human Gate review record SHA drift: {record_ref['path']}")
        record = schema_gate.load_and_validate_json(
            record_path,
            repo_root / REVIEW_RECORD_SCHEMA,
            label="Human Gate Review Record",
        )
        if (
            record.get("issue_id") != expected_issue_id
            or record.get("gate") != gate
            or record.get("revision") != revision
            or record.get("decision") != row["decision"]
        ):
            raise HumanGateError("Human Gate review index/record identity mismatch")
        if row["decision"] == "APPROVED":
            approval = record.get("approval")
            if not isinstance(approval, dict):
                raise HumanGateError("APPROVED Human Gate review lacks immutable approval snapshot")
            approval_path = core.repo_local_path(repo_root, approval["path"], "Human Gate approval snapshot")
            if approval_path.is_symlink() or not approval_path.is_file():
                raise HumanGateError(f"Human Gate approval snapshot missing: {approval['path']}")
            if core.sha256_file(approval_path) != approval["sha256"]:
                raise HumanGateError(f"Human Gate approval snapshot SHA drift: {approval['path']}")
            approved_active[gate] = True
        elif (
            gate == "PUBLICATION_PREVIEW"
            and row["decision"] == "REQUEST_CHANGES"
            and _reopens_architecture(record.get("regeneration_boundary"))
        ):
            if not approved_active["ARCHITECTURE_REVIEW"]:
                raise HumanGateError("Publication cross-gate revision has no active approved Architecture to reopen")
            approved_active["ARCHITECTURE_REVIEW"] = False


def _load_review_index(
    repo_root: Path,
    cfg: dict[str, Any],
    source_root: Path,
    issue_id: str,
) -> dict[str, Any]:
    path = review_index_path(source_root, cfg)
    if not path.exists():
        return {"schema_version": "2.0-rc1", "issue_id": issue_id, "reviews": []}
    payload = schema_gate.load_and_validate_json(
        path,
        repo_root / REVIEW_INDEX_SCHEMA,
        label="Human Gate Review Index",
    )
    _validate_review_index_semantics(repo_root, payload, issue_id)
    return payload


def _next_revision(index: dict[str, Any], gate: str, expected_revision: int | None) -> int:
    revision = 1 + sum(1 for row in index["reviews"] if row["gate"] == gate)
    if expected_revision is not None and expected_revision != revision:
        raise HumanGateError(
            f"stale Human Gate request for {gate}: expected revision {expected_revision}, current next revision is {revision}"
        )
    return revision


def _expand_gate_path(template: str, profile: dict[str, Any]) -> str:
    value = template
    for key, replacement in profile["paths"].items():
        value = value.replace("{" + key + "}", replacement)
    if "{" in value or "}" in value:
        raise HumanGateError(f"unsupported Human Gate path template token: {template}")
    return value


def _raw_repo_file(repo_root: Path, relative: str, label: str) -> Path:
    """Resolve a repository-relative file without following symlink components."""
    if not core._safe_relative_repo_path(relative):
        raise HumanGateError(f"{label} must be a safe repository-relative path")
    root = repo_root.resolve()
    raw = root / relative
    current = root
    for part in Path(relative).parts:
        current = current / part
        if current.is_symlink():
            raise HumanGateError(f"{label} may not traverse a symlink: {relative}")
    if not raw.is_file():
        raise HumanGateError(f"{label} missing or unsafe: {relative}")
    return raw


def _reviewed_artifacts(
    repo_root: Path,
    cfg: dict[str, Any],
    state: dict[str, Any],
    profile: dict[str, Any],
    gate: str,
    *,
    require_current_candidate_validity: bool = True,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in cfg["orchestration"]["gate_inputs"][gate]:
        path = core.repo_local_path(
            repo_root,
            _expand_gate_path(item["path"], profile),
            f"Human Gate input {item['name']}",
        )
        rows.append(_named_authority(repo_root, item["name"], path))
    if gate == "PUBLICATION_PREVIEW":
        candidate_path = next(
            core.repo_local_path(repo_root, row["path"], "Publication Candidate")
            for row in rows
            if row["name"] == "publication-candidate"
        )
        if require_current_candidate_validity:
            candidate = publication.validate_candidate(
                repo_root, candidate_path, issue_id=state["issue_id"]
            )
        else:
            # REQUEST_CHANGES records the exact historical review surface. A
            # newer Candidate schema or substantive validator may be the reason
            # the Human is rejecting these bytes, so rejection must not require
            # the historical artifact to satisfy current acceptance contracts.
            candidate = core.load_json(candidate_path)
            if candidate.get("issue_id") != state["issue_id"]:
                raise HumanGateError("Publication Candidate historical review issue identity mismatch")
            if candidate.get("publication_profile") != profile.get("publication_profile"):
                raise HumanGateError("Publication Candidate historical review profile identity mismatch")
        pdf = candidate.get("pdf")
        if not isinstance(pdf, dict) or not isinstance(pdf.get("path"), str):
            raise HumanGateError("Publication Candidate lacks durable PDF authority")
        pdf_path = core.repo_local_path(repo_root, pdf["path"], "Publication Preview PDF")
        pdf_authority = _named_authority(repo_root, "publication-pdf", pdf_path)
        if pdf_authority["sha256"] != pdf.get("sha256"):
            raise HumanGateError("Publication Candidate PDF authority drift")
        rows.append(pdf_authority)
    return rows


def _review_record_payload(
    *,
    issue_id: str,
    gate: str,
    revision: int,
    decision: str,
    reviewed_state: dict[str, str],
    reviewed_artifacts: list[dict[str, str]],
    reviewed_repository_commit_sha: str,
    reviewed_by: str,
    reviewed_at: datetime,
    review_reference: str,
    requested_changes: str | None,
    regeneration_boundary: str | None,
    approval: dict[str, str] | None,
) -> dict[str, Any]:
    seed = {
        "issue_id": issue_id,
        "gate": gate,
        "revision": revision,
        "decision": decision,
        "reviewed_state": reviewed_state,
        "reviewed_artifacts": reviewed_artifacts,
        "reviewed_repository_commit_sha": reviewed_repository_commit_sha,
        "reviewed_at": core.iso_utc(reviewed_at),
        "review_reference": review_reference,
        "regeneration_boundary": regeneration_boundary,
    }
    return {
        "schema_version": "2.0-rc1",
        "review_id": f"review:{issue_id}:{GATE_SLUGS[gate]}:r{revision}:{core.sha256_object(seed)[:16]}",
        "issue_id": issue_id,
        "gate": gate,
        "revision": revision,
        "decision": decision,
        "reviewed_state": reviewed_state,
        "reviewed_artifacts": reviewed_artifacts,
        "reviewed_repository_commit_sha": reviewed_repository_commit_sha,
        "reviewed_by": reviewed_by,
        "reviewed_at": core.iso_utc(reviewed_at),
        "review_reference": review_reference,
        "requested_changes": requested_changes,
        "regeneration_boundary": regeneration_boundary,
        "approval": approval,
    }


def _write_review_record(
    repo_root: Path,
    cfg: dict[str, Any],
    source_root: Path,
    index: dict[str, Any],
    record: dict[str, Any],
) -> tuple[Path, Path]:
    schema_gate.validate_instance(record, repo_root / REVIEW_RECORD_SCHEMA, label="Human Gate Review Record")
    record_path = review_record_path(source_root, cfg, record["gate"], record["revision"])
    if record_path.exists():
        raise HumanGateError(f"refusing Human Gate review record overwrite: {_rel(repo_root, record_path)}")
    core.write_json(record_path, record)
    updated_index = deepcopy(index)
    updated_index["reviews"].append(
        {
            "gate": record["gate"],
            "revision": record["revision"],
            "decision": record["decision"],
            "record": _authority(repo_root, record_path),
        }
    )
    schema_gate.validate_instance(
        updated_index,
        repo_root / REVIEW_INDEX_SCHEMA,
        label="Human Gate Review Index",
    )
    _validate_review_index_semantics(repo_root, updated_index, record["issue_id"])
    index_path = review_index_path(source_root, cfg)
    core.write_json(index_path, updated_index)
    return record_path, index_path


def _validate_gate_pending(state: dict[str, Any], gate: str) -> None:
    key = GATE_KEYS[gate]
    expected_state = GATE_STATES[gate]
    if state.get("lifecycle_state") != expected_state or state.get("human_gates", {}).get(key) != "pending":
        raise HumanGateError(f"{gate} decision requires pending {expected_state} Human Gate")


def _current_pending_gate(
    cfg: dict[str, Any],
    state: dict[str, Any],
    *,
    requested_gate: str | None = None,
) -> str:
    """Derive the currently stopped Human Gate from lifecycle authority.

    target_gate is the eventual run destination, not the identity of the Gate
    currently awaiting presentation. The configured lifecycle mapping, pending
    status, null provenance, and terminal reason together define the only
    operator-invalidatable pending surface.
    """
    lifecycle = state.get("lifecycle_state")
    gate_at_state = cfg.get("orchestration", {}).get("gate_at_state")
    if not isinstance(gate_at_state, dict):
        raise HumanGateError("orchestration.gate_at_state is missing or invalid")
    current_gate = gate_at_state.get(lifecycle)
    if current_gate not in GATE_KEYS:
        if requested_gate in GATE_KEYS and lifecycle != GATE_STATES[requested_gate]:
            raise HumanGateError(
                f"{requested_gate} decision requires pending {GATE_STATES[requested_gate]} Human Gate"
            )
        raise HumanGateError(
            f"current lifecycle {lifecycle!r} has no configured pending Human Gate"
        )
    if GATE_STATES[current_gate] != lifecycle:
        raise HumanGateError(
            f"configured current Human Gate {current_gate} does not match lifecycle {lifecycle}"
        )
    human_gates = state.get("human_gates")
    provenance = state.get("human_gate_provenance")
    gate_key = GATE_KEYS[current_gate]
    if not isinstance(human_gates, dict) or human_gates.get(gate_key) != "pending":
        raise HumanGateError(
            f"current {current_gate} Human Gate is not pending"
        )
    if not isinstance(provenance, dict) or provenance.get(gate_key) is not None:
        raise HumanGateError(
            f"current {current_gate} Human Gate has active provenance"
        )
    if state.get("terminal_reason") != "HUMAN_GATE_REACHED":
        raise HumanGateError(
            "operator pending-Gate invalidation requires HUMAN_GATE_REACHED"
        )
    return current_gate


def _historical_core_config(repo_root: Path, commit_sha: str) -> dict[str, Any]:
    """Load the canonical Core config bytes from an invalidated commit."""
    config_path = core.DEFAULT_CONFIG.as_posix()
    raw = _committed_file_bytes(repo_root, commit_sha, config_path)
    try:
        config = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HumanGateError(
            "invalidated repository commit Core config is not valid UTF-8 JSON"
        ) from exc
    if not isinstance(config, dict):
        raise HumanGateError("invalidated repository commit Core config is not an object")
    gate_at_state = config.get("orchestration", {}).get("gate_at_state")
    if not isinstance(gate_at_state, dict):
        raise HumanGateError(
            "invalidated repository commit Core config lacks orchestration.gate_at_state"
        )
    return config

def _require_review_commit(repo_root: Path, commit_sha: str) -> None:
    try:
        subprocess.run(
            ["git", "cat-file", "-e", f"{commit_sha}^{{commit}}"],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise HumanGateError(
            f"Human Gate reviewed repository commit does not exist: {commit_sha}"
        ) from exc


def _require_review_commit_reachable(repo_root: Path, commit_sha: str, work_branch: str) -> None:
    ref, label = _work_branch_ref(repo_root, work_branch)
    reachable = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit_sha, ref],
        cwd=repo_root,
    )
    if reachable.returncode != 0:
        raise HumanGateError(
            f"Human Gate reviewed repository commit is not reachable from canonical work branch {label}: {commit_sha}"
        )


def _work_branch_ref(repo_root: Path, work_branch: str) -> tuple[str, str]:
    try:
        subprocess.run(
            ["git", "check-ref-format", "--branch", work_branch],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise HumanGateError(f"invalid Human Gate work branch: {work_branch}") from exc

    origin = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"],
        cwd=repo_root,
        capture_output=True,
    )
    if origin.returncode == 0:
        ref = f"refs/remotes/origin/{work_branch}"
        label = f"origin/{work_branch}"
    else:
        ref = f"refs/heads/{work_branch}"
        label = work_branch
    return ref, label


def _require_expected_branch_head(
    repo_root: Path,
    work_branch: str,
    expected_branch_head: str,
) -> None:
    if len(expected_branch_head) != 40 or any(c not in "0123456789abcdef" for c in expected_branch_head):
        raise HumanGateError("expected work branch head must be a lowercase 40-hex SHA")
    ref, label = _work_branch_ref(repo_root, work_branch)
    present = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", ref],
        cwd=repo_root,
    )
    if present.returncode != 0:
        raise HumanGateError(
            f"canonical work branch {label} is unavailable; push/fetch the pending Gate surface first"
        )
    actual = subprocess.run(
        ["git", "rev-parse", "--verify", ref],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    if actual.stdout.strip() != expected_branch_head:
        raise HumanGateError(
            f"stale pending Gate surface: expected {label} head {expected_branch_head}, found {actual.stdout.strip()}"
        )


def _committed_file_bytes(repo_root: Path, commit_sha: str, rel: str) -> bytes:
    try:
        listing = subprocess.run(
            ["git", "ls-tree", "-z", commit_sha, "--", rel],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise HumanGateError(
            f"cannot inspect Human Gate reviewed repository commit path: {commit_sha}:{rel}"
        ) from exc
    entries = [entry for entry in listing.stdout.split(b"\0") if entry]
    if len(entries) != 1:
        raise HumanGateError(
            f"Human Gate reviewed repository commit is missing reviewed path: {rel}"
        )
    try:
        meta, encoded_path = entries[0].split(b"\t", 1)
        mode, object_type, object_sha = meta.decode("ascii").split()
        listed_path = encoded_path.decode("utf-8")
    except (UnicodeDecodeError, ValueError) as exc:
        raise HumanGateError(
            f"Human Gate reviewed repository tree entry invalid for: {rel}"
        ) from exc
    if listed_path != rel or object_type != "blob" or mode not in {"100644", "100755"}:
        raise HumanGateError(
            f"Human Gate reviewed repository path is not a regular file: {rel}"
        )
    try:
        blob = subprocess.run(
            ["git", "cat-file", "blob", object_sha],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise HumanGateError(
            f"cannot read Human Gate reviewed repository blob: {rel}"
        ) from exc
    return blob.stdout


def _review_commit(
    repo_root: Path,
    override: str | None,
    work_branch: str,
    reviewed_state: dict[str, str],
    reviewed_artifacts: list[dict[str, str]],
) -> str:
    commit_sha = core.repository_commit_sha(repo_root, override)
    _require_review_commit(repo_root, commit_sha)
    _require_review_commit_reachable(repo_root, commit_sha, work_branch)
    refs: list[tuple[str, dict[str, str]]] = [("Production State", reviewed_state)]
    refs.extend(
        (f"Human Gate artifact {row['name']}", row)
        for row in reviewed_artifacts
    )
    for label, ref in refs:
        rel = ref["path"]
        current = core.repo_local_path(repo_root, rel, label)
        if current.is_symlink() or not current.is_file():
            raise HumanGateError(f"{label} missing or unsafe while verifying reviewed commit: {rel}")
        committed = _committed_file_bytes(repo_root, commit_sha, rel)
        if core.sha256_bytes(committed) != ref["sha256"]:
            raise HumanGateError(
                f"Human Gate reviewed repository commit bytes differ for {label}: {rel}"
            )
    return commit_sha


def _snapshot_approval(
    repo_root: Path,
    source_root: Path,
    cfg: dict[str, Any],
    gate: str,
    revision: int,
    canonical_approval: Path,
) -> dict[str, str]:
    canonical = _authority(repo_root, canonical_approval)
    snapshot = approval_snapshot_path(source_root, cfg, gate, revision)
    if snapshot.exists():
        existing = _authority(repo_root, snapshot)
        if existing["sha256"] != canonical["sha256"]:
            raise HumanGateError(f"Human Gate approval snapshot collision: {_rel(repo_root, snapshot)}")
        return existing
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    snapshot.write_bytes(canonical_approval.read_bytes())
    snap = _authority(repo_root, snapshot)
    if snap["sha256"] != canonical["sha256"]:
        raise HumanGateError("Human Gate approval snapshot byte mismatch")
    return snap


def record_architecture_approval(
    repo_root: Path,
    cfg: dict[str, Any],
    state_path: Path,
    reviewed_by: str,
    reviewed_at: datetime,
    review_reference: str,
    *,
    expected_revision: int | None = None,
    reviewed_commit_sha: str | None = None,
) -> tuple[dict[str, Any], Path, Path]:
    state, profile, source_root = _state_context(repo_root, cfg, state_path)
    _validate_gate_pending(state, "ARCHITECTURE_REVIEW")
    index = _load_review_index(repo_root, cfg, source_root, state["issue_id"])
    revision = _next_revision(index, "ARCHITECTURE_REVIEW", expected_revision)
    reviewed_state = _authority(repo_root, state_path)
    artifacts = _reviewed_artifacts(repo_root, cfg, state, profile, "ARCHITECTURE_REVIEW")
    commit_sha = _review_commit(
        repo_root,
        reviewed_commit_sha,
        profile["paths"]["work_branch"],
        reviewed_state,
        artifacts,
    )
    updated = agent.approve_architecture(
        repo_root,
        cfg,
        state_path,
        reviewed_by,
        reviewed_at,
        review_reference,
    )
    approval_path = source_root / cfg["state_authority"]["architecture_approval_path"]
    approval_snapshot = _snapshot_approval(
        repo_root, source_root, cfg, "ARCHITECTURE_REVIEW", revision, approval_path
    )
    record = _review_record_payload(
        issue_id=state["issue_id"],
        gate="ARCHITECTURE_REVIEW",
        revision=revision,
        decision="APPROVED",
        reviewed_state=reviewed_state,
        reviewed_artifacts=artifacts,
        reviewed_repository_commit_sha=commit_sha,
        reviewed_by=reviewed_by,
        reviewed_at=reviewed_at,
        review_reference=review_reference,
        requested_changes=None,
        regeneration_boundary=None,
        approval=approval_snapshot,
    )
    record_path, index_path = _write_review_record(repo_root, cfg, source_root, index, record)
    return updated, record_path, index_path


def record_publication_preview_approval(
    repo_root: Path,
    cfg: dict[str, Any],
    state_path: Path,
    reviewed_by: str,
    reviewed_at: datetime,
    review_reference: str,
    *,
    expected_revision: int | None = None,
    reviewed_commit_sha: str | None = None,
) -> tuple[dict[str, Any], Path, Path]:
    state, profile, source_root = _state_context(repo_root, cfg, state_path)
    _validate_gate_pending(state, "PUBLICATION_PREVIEW")
    index = _load_review_index(repo_root, cfg, source_root, state["issue_id"])
    revision = _next_revision(index, "PUBLICATION_PREVIEW", expected_revision)
    reviewed_state = _authority(repo_root, state_path)
    artifacts = _reviewed_artifacts(repo_root, cfg, state, profile, "PUBLICATION_PREVIEW")
    commit_sha = _review_commit(
        repo_root,
        reviewed_commit_sha,
        profile["paths"]["work_branch"],
        reviewed_state,
        artifacts,
    )
    updated = agent.approve_publication_preview(
        repo_root,
        cfg,
        state_path,
        reviewed_by,
        reviewed_at,
        review_reference,
    )
    approval_path = source_root / cfg["state_authority"]["publication_preview_approval_path"]
    approval_snapshot = _snapshot_approval(
        repo_root, source_root, cfg, "PUBLICATION_PREVIEW", revision, approval_path
    )
    record = _review_record_payload(
        issue_id=state["issue_id"],
        gate="PUBLICATION_PREVIEW",
        revision=revision,
        decision="APPROVED",
        reviewed_state=reviewed_state,
        reviewed_artifacts=artifacts,
        reviewed_repository_commit_sha=commit_sha,
        reviewed_by=reviewed_by,
        reviewed_at=reviewed_at,
        review_reference=review_reference,
        requested_changes=None,
        regeneration_boundary=None,
        approval=approval_snapshot,
    )
    record_path, index_path = _write_review_record(repo_root, cfg, source_root, index, record)
    return updated, record_path, index_path


def _completed_checkpoints(cfg: dict[str, Any], lifecycle: str) -> set[str]:
    index = core.LIFECYCLE.index(lifecycle)
    result: set[str] = set()
    for state_name in core.LIFECYCLE[:index]:
        stage = cfg["orchestration"]["stage_plan"].get(state_name)
        if isinstance(stage, dict):
            result.update(stage.get("checkpoints", []))
    return result


def _superseded_checkpoint_paths(
    repo_root: Path,
    cfg: dict[str, Any],
    state: dict[str, Any],
    source_root: Path,
    regeneration_boundary: str,
    gate: str,
) -> list[Path]:
    keep = _completed_checkpoints(cfg, regeneration_boundary)
    paths: dict[str, Path] = {}
    for checkpoint in core.CHECKPOINTS:
        if checkpoint in keep:
            continue
        authority = state.get("checkpoint_provenance", {}).get(checkpoint)
        if isinstance(authority, dict):
            path = _raw_repo_file(
                repo_root,
                authority["path"],
                f"superseded checkpoint {checkpoint}",
            )
            try:
                path.resolve().relative_to(source_root.resolve())
            except ValueError as exc:
                raise HumanGateError(f"superseded checkpoint authority escapes source_root: {authority['path']}") from exc
            paths[_rel(repo_root, path)] = path

    start = core.LIFECYCLE.index(regeneration_boundary)
    end = core.LIFECYCLE.index(GATE_STATES[gate])
    for state_name in core.LIFECYCLE[start:end]:
        path = source_root / cfg["state_authority"]["agent_checkpoint_dir"] / f"{state_name}.json"
        relative = _rel(repo_root, path)
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise HumanGateError(f"superseded checkpoint is missing or unsafe: {relative}")
        if path.exists():
            paths[relative] = path
    return [paths[key] for key in sorted(paths)]


def _superseded_canonical_artifacts(
    repo_root: Path,
    cfg: dict[str, Any],
    profile: dict[str, Any],
    source_root: Path,
    regeneration_boundary: str,
    gate: str,
) -> list[tuple[str, Path]]:
    """Resolve configured mutable singleton artifacts that block regeneration."""
    configured = cfg["orchestration"].get("canonical_regeneration_artifacts")
    if not isinstance(configured, list):
        raise HumanGateError("Core lacks canonical_regeneration_artifacts cleanup authority")
    seen_names: set[str] = set()
    seen_paths: set[str] = set()
    boundary_index = core.LIFECYCLE.index(regeneration_boundary)
    gate_index = core.LIFECYCLE.index(GATE_STATES[gate])
    resolved: list[tuple[str, Path]] = []
    for index, item in enumerate(configured):
        if not isinstance(item, dict) or set(item) != {"name", "path", "owner_state"}:
            raise HumanGateError(f"canonical regeneration cleanup entry {index} is malformed")
        name = item["name"]
        owner_state = item["owner_state"]
        if not isinstance(name, str) or not name or name in seen_names:
            raise HumanGateError("canonical regeneration cleanup names must be unique")
        if owner_state not in core.LIFECYCLE:
            raise HumanGateError(f"canonical regeneration cleanup owner state is invalid: {owner_state}")
        seen_names.add(name)
        if not (boundary_index <= core.LIFECYCLE.index(owner_state) < gate_index):
            continue
        relative = _expand_gate_path(item["path"], profile)
        raw = repo_root / relative
        current = repo_root.resolve()
        for part in Path(relative).parts:
            current = current / part
            if current.is_symlink():
                raise HumanGateError(
                    f"canonical regeneration artifact is missing or unsafe: {relative}"
                )
        if raw.exists() and not raw.is_file():
            raise HumanGateError(
                f"canonical regeneration artifact is missing or unsafe: {relative}"
            )
        path = core.repo_local_path(
            repo_root,
            relative,
            f"canonical regeneration artifact {name}",
        )
        try:
            path.resolve().relative_to(source_root.resolve())
        except ValueError as exc:
            raise HumanGateError(
                f"canonical regeneration artifact escapes source_root: {item['path']}"
            ) from exc
        rel = _rel(repo_root, path)
        if rel in seen_paths:
            raise HumanGateError("canonical regeneration cleanup paths must be unique")
        seen_paths.add(rel)
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise HumanGateError(f"canonical regeneration artifact is missing or unsafe: {rel}")
        resolved.append((name, path))
    return sorted(resolved, key=lambda row: _rel(repo_root, row[1]))


def _superseded_paths_for_regeneration(
    repo_root: Path,
    cfg: dict[str, Any],
    state: dict[str, Any],
    profile: dict[str, Any],
    source_root: Path,
    regeneration_boundary: str,
    gate: str,
) -> tuple[list[Path], list[tuple[str, Path]]]:
    checkpoint_paths = _superseded_checkpoint_paths(
        repo_root, cfg, state, source_root, regeneration_boundary, gate
    )
    canonical = _superseded_canonical_artifacts(
        repo_root, cfg, profile, source_root, regeneration_boundary, gate
    )
    all_paths: dict[str, Path] = {
        _rel(repo_root, path): path for path in checkpoint_paths
    }
    all_paths.update({_rel(repo_root, path): path for _, path in canonical})
    return [all_paths[key] for key in sorted(all_paths)], canonical


def _superseded_gate_authority_paths(
    repo_root: Path,
    cfg: dict[str, Any],
    state: dict[str, Any],
    source_root: Path,
    gate: str,
    regeneration_boundary: str,
) -> list[Path]:
    if gate != "PUBLICATION_PREVIEW" or not _reopens_architecture(regeneration_boundary):
        return []
    if state["human_gates"]["architecture_review"] != "approved":
        raise HumanGateError("Publication cross-gate revision requires active approved Architecture Review")
    path = source_root / cfg["state_authority"]["architecture_approval_path"]
    authority = _authority(repo_root, path)
    provenance = state.get("human_gate_provenance", {}).get("architecture_review")
    if not isinstance(provenance, dict) or provenance.get("path") != authority["path"] or provenance.get("sha256") != authority["sha256"]:
        raise HumanGateError("active Architecture approval provenance does not match canonical approval bytes")
    return [path]


def _revised_state(
    repo_root: Path,
    cfg: dict[str, Any],
    state: dict[str, Any],
    gate: str,
    regeneration_boundary: str,
    *,
    allowed_boundaries: list[str] | None = None,
) -> dict[str, Any]:
    allowed = allowed_boundaries
    if allowed is None:
        allowed = cfg["orchestration"].get("human_gate_revision_boundaries", {}).get(gate, [])
    if regeneration_boundary not in allowed:
        raise HumanGateError(
            f"regeneration boundary {regeneration_boundary!r} is not allowed for {gate}; allowed={allowed}"
        )
    target_index = core.LIFECYCLE.index(regeneration_boundary)
    gate_index = core.LIFECYCLE.index(GATE_STATES[gate])
    if target_index >= gate_index:
        raise HumanGateError("regeneration boundary must precede the reviewed Human Gate state")

    updated = deepcopy(state)
    keep = _completed_checkpoints(cfg, regeneration_boundary)
    for checkpoint in core.CHECKPOINTS:
        if checkpoint in keep:
            continue
        updated["machine_checkpoints"][checkpoint] = "pending"
        updated["checkpoint_provenance"][checkpoint] = None
    if "validation" not in keep:
        # The active revalidation basis is bound to the validation checkpoint.
        # Invalidating that checkpoint orphans the pointer, so revision clears it
        # deterministically. The historical record file itself is never touched
        # here; unreferenced it is inert historical evidence.
        updated["publication_revalidation_provenance"] = None
    updated["lifecycle_state"] = regeneration_boundary
    updated["history"] = updated["history"][: target_index + 1]

    if gate == "ARCHITECTURE_REVIEW":
        updated["human_gates"]["architecture_review"] = "pending"
        updated["human_gate_provenance"]["architecture_review"] = None
        updated["human_gates"]["publication_preview"] = "pending"
        updated["human_gate_provenance"]["publication_preview"] = None
    else:
        if updated["human_gates"]["architecture_review"] != "approved":
            raise HumanGateError("Publication Preview revision requires active approved Architecture Review")
        if _reopens_architecture(regeneration_boundary):
            updated["human_gates"]["architecture_review"] = "pending"
            updated["human_gate_provenance"]["architecture_review"] = None
        updated["human_gates"]["publication_preview"] = "pending"
        updated["human_gate_provenance"]["publication_preview"] = None

    updated = core.refresh_state_control(updated, cfg)
    errors = agent.validate_agent_state(repo_root, cfg, updated)
    if errors:
        raise HumanGateError("refusing inconsistent Human Gate revision State: " + "; ".join(errors))
    return updated


def _validate_pending_gate_surface(
    repo_root: Path,
    cfg: dict[str, Any],
    state: dict[str, Any],
    profile: dict[str, Any],
    gate: str,
) -> list[dict[str, str]]:
    """Validate the exact unpresented Gate surface before operator invalidation."""
    for item in cfg["orchestration"]["gate_inputs"][gate]:
        _raw_repo_file(
            repo_root,
            _expand_gate_path(item["path"], profile),
            f"Human Gate input {item['name']}",
        )
    artifacts = _reviewed_artifacts(repo_root, cfg, state, profile, gate)
    if gate == "ARCHITECTURE_REVIEW":
        architecture_path = next(row["path"] for row in artifacts if row["name"] == "issue-architecture")
        summary_path = next(row["path"] for row in artifacts if row["name"] == "architecture-review-summary")
        attention_path = next(row["path"] for row in artifacts if row["name"] == "architecture-review-attention")
        architecture = schema_gate.load_and_validate_json(
            core.repo_local_path(repo_root, architecture_path, "Architecture Gate input"),
            repo_root / Path("schemas/issue-architecture-v2.schema.json"),
            label="Architecture Gate input",
        )
        summary = schema_gate.load_and_validate_json(
            core.repo_local_path(repo_root, summary_path, "Architecture Review Summary Gate input"),
            repo_root / Path("schemas/architecture-review-summary-v2.schema.json"),
            label="Architecture Review Summary Gate input",
        )
        attention = core.repo_local_path(repo_root, attention_path, "Architecture Review Attention Gate input")
        review_attention.validate_attention(repo_root, attention)
        if architecture.get("issue_id") != state["issue_id"] or architecture.get("status") != "PROPOSED":
            raise HumanGateError("Architecture Gate input is not the current PROPOSED Architecture for this issue")
        if summary.get("issue_id") != state["issue_id"] or summary.get("readiness", {}).get("status") != "READY_FOR_ARCHITECTURE_REVIEW":
            raise HumanGateError("Architecture Review Summary Gate input is not ready for review")
        if summary.get("basis", {}).get("architecture_sha256") != core.sha256_file(
            core.repo_local_path(repo_root, architecture_path, "Architecture Gate input")
        ):
            raise HumanGateError("Architecture Review Summary Gate input does not bind exact Architecture bytes")
    elif gate == "PUBLICATION_PREVIEW":
        candidate = next(row["path"] for row in artifacts if row["name"] == "publication-candidate")
        publication.validate_candidate(
            repo_root,
            core.repo_local_path(repo_root, candidate, "Publication Candidate Gate input"),
            issue_id=state["issue_id"],
        )
    return artifacts


def _operator_record_dir(source_root: Path, cfg: dict[str, Any]) -> Path:
    raw = cfg["state_authority"].get("operator_invalidation_dir")
    if not isinstance(raw, str) or not core._safe_relative_repo_path(raw):
        raise HumanGateError("state_authority.operator_invalidation_dir must be a safe relative path")
    return source_root / raw


def _validate_committed_authority(
    repo_root: Path,
    commit_sha: str,
    ref: dict[str, Any],
    label: str,
) -> bytes:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
        raise HumanGateError(f"{label} authority fields invalid")
    if not core._safe_relative_repo_path(ref.get("path")):
        raise HumanGateError(f"{label} path must be a safe repository-relative path")
    raw = _committed_file_bytes(repo_root, commit_sha, ref["path"])
    if core.sha256_bytes(raw) != ref["sha256"]:
        raise HumanGateError(f"{label} SHA does not match invalidated repository commit")
    return raw


def validate_operator_invalidation_record(
    repo_root: Path,
    record_path: Path,
    *,
    expected_issue_id: str | None = None,
) -> dict[str, Any]:
    """Validate immutable operator provenance against the invalidated commit."""
    record_path = core.repo_local_path(
        repo_root,
        _rel(repo_root, record_path),
        "operator invalidation record",
    )
    payload = schema_gate.load_and_validate_json(
        record_path,
        repo_root / OPERATOR_INVALIDATION_SCHEMA,
        label="Operator Pending Gate Invalidation",
    )
    if expected_issue_id is not None and payload["issue_id"] != expected_issue_id:
        raise HumanGateError("operator invalidation record issue identity mismatch")
    commit_sha = payload["invalidated_repository_commit_sha"]
    _require_review_commit(repo_root, commit_sha)
    state_raw = _validate_committed_authority(
        repo_root, commit_sha, payload["prior_state"], "operator invalidation prior State"
    )
    try:
        prior_state = json.loads(state_raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HumanGateError("operator invalidation prior State is not valid JSON") from exc
    if prior_state.get("issue_id") != payload["issue_id"]:
        raise HumanGateError("operator invalidation prior State issue identity mismatch")
    gate = payload["gate"]
    cfg = _historical_core_config(repo_root, commit_sha)
    try:
        subprocess.run(
            ["git", "check-ref-format", "--branch", payload["work_branch"]],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise HumanGateError("operator invalidation work_branch is invalid") from exc
    _require_review_commit_reachable(repo_root, commit_sha, payload["work_branch"])
    current_gate = _current_pending_gate(cfg, prior_state, requested_gate=gate)
    if current_gate != gate:
        raise HumanGateError(
            f"operator invalidation prior State current Gate mismatch: requested {gate}, current {current_gate}"
        )

    names: set[str] = set()
    for row in payload["prior_gate_inputs"]:
        if row["name"] in names:
            raise HumanGateError("operator invalidation prior Gate inputs are ambiguous")
        names.add(row["name"])
        _validate_committed_authority(
            repo_root,
            commit_sha,
            {"path": row["path"], "sha256": row["sha256"]},
            f"operator invalidation Gate input {row['name']}",
        )
    checkpoints: set[str] = set()
    for row in payload["invalidated_checkpoint_authority"]:
        if row["checkpoint"] in checkpoints:
            raise HumanGateError("operator invalidation checkpoint authority is ambiguous")
        if row["checkpoint"] not in core.CHECKPOINTS:
            raise HumanGateError("operator invalidation checkpoint authority is unknown")
        checkpoints.add(row["checkpoint"])
        _validate_committed_authority(repo_root, commit_sha, {"path": row["path"], "sha256": row["sha256"]}, f"operator invalidation checkpoint {row['checkpoint']}")
    canonical_names: set[str] = set()
    canonical_paths: set[str] = set()
    for row in payload["superseded_canonical_paths"]:
        if row["name"] in canonical_names or row["path"] in canonical_paths:
            raise HumanGateError("operator invalidation canonical cleanup authority is ambiguous")
        canonical_names.add(row["name"])
        canonical_paths.add(row["path"])
        _validate_committed_authority(repo_root, commit_sha, {"path": row["path"], "sha256": row["sha256"]}, f"operator invalidation canonical artifact {row['name']}")
    return payload


def _load_operator_invalidation_records(
    repo_root: Path,
    cfg: dict[str, Any],
    source_root: Path,
    issue_id: str,
) -> list[dict[str, Any]]:
    directory = _operator_record_dir(source_root, cfg)
    if not directory.exists():
        return []
    if directory.is_symlink() or not directory.is_dir():
        raise HumanGateError("operator invalidation record directory is missing or unsafe")
    paths = sorted(directory.glob("*.json"))
    if any(
        path.is_symlink() or not path.is_file() or path.suffix != ".json"
        for path in directory.iterdir()
    ):
        raise HumanGateError("operator invalidation record directory may contain regular JSON files only")
    records = [
        validate_operator_invalidation_record(repo_root, path, expected_issue_id=issue_id)
        for path in paths
    ]
    sequences = sorted(record["sequence"] for record in records)
    if sequences != list(range(1, len(records) + 1)):
        raise HumanGateError("operator invalidation sequences must be contiguous")
    return records


def invalidate_pending_gate(
    repo_root: Path,
    cfg: dict[str, Any],
    state_path: Path,
    gate: str,
    regeneration_boundary: str,
    reason: str,
    operator_reference: str,
    expected_work_branch_head: str,
    *,
    invalidated_commit_sha: str | None = None,
    recorded_at: datetime | None = None,
) -> tuple[dict[str, Any], Path, list[str]]:
    """Invalidate an unpresented pending Human Gate without creating a Human record."""
    if gate not in GATE_KEYS:
        raise HumanGateError(f"unsupported Human Gate: {gate}")
    if not isinstance(reason, str) or not reason.strip():
        raise HumanGateError("operator pending-Gate invalidation requires a non-empty reason")
    if not isinstance(operator_reference, str) or not operator_reference.strip():
        raise HumanGateError("operator pending-Gate invalidation requires operator_reference")
    if not isinstance(expected_work_branch_head, str) or not expected_work_branch_head.strip():
        raise HumanGateError("operator pending-Gate invalidation requires expected_work_branch_head")

    state, profile, source_root = _state_context(repo_root, cfg, state_path)
    current_gate = _current_pending_gate(cfg, state, requested_gate=gate)
    if current_gate != gate:
        raise HumanGateError(
            f"operator pending-Gate invalidation current Gate mismatch: requested {gate}, current {current_gate}"
        )
    if state.get("machine_checkpoints", {}).get("architecture") != "passed" and gate == "ARCHITECTURE_REVIEW":
        raise HumanGateError("Architecture pending-Gate invalidation requires a passed Architecture checkpoint")
    if state.get("human_gates", {}).get("architecture_review") == "approved" and gate == "PUBLICATION_PREVIEW":
        raise HumanGateError("operator invalidation cannot cross an active Human Architecture approval")

    allowed = cfg["orchestration"].get("operator_pending_gate_invalidation_boundaries", {}).get(gate, [])
    if regeneration_boundary not in allowed:
        raise HumanGateError(
            f"operator regeneration boundary {regeneration_boundary!r} is not allowed for {gate}; allowed={allowed}"
        )
    index = _load_review_index(repo_root, cfg, source_root, state["issue_id"])
    if index.get("reviews"):
        raise HumanGateError("operator pending-Gate invalidation requires no Human review records")

    invalidated_commit_sha = invalidated_commit_sha or core.repository_commit_sha(repo_root)
    current_head = core.repository_commit_sha(repo_root)
    if current_head != invalidated_commit_sha:
        raise HumanGateError(
            f"stale pending Gate surface: checkout HEAD {current_head} differs from invalidated commit {invalidated_commit_sha}"
        )
    _require_expected_branch_head(repo_root, profile["paths"]["work_branch"], expected_work_branch_head)
    artifacts = _validate_pending_gate_surface(repo_root, cfg, state, profile, gate)
    reviewed_state = _authority(repo_root, state_path)
    commit_sha = _review_commit(
        repo_root,
        invalidated_commit_sha,
        profile["paths"]["work_branch"],
        reviewed_state,
        artifacts,
    )
    if commit_sha != invalidated_commit_sha:
        raise HumanGateError("invalidated repository commit identity changed during preflight")

    updated = _revised_state(
        repo_root,
        cfg,
        state,
        gate,
        regeneration_boundary,
        allowed_boundaries=list(allowed),
    )
    cleanup_paths, canonical = _superseded_paths_for_regeneration(
        repo_root, cfg, state, profile, source_root, regeneration_boundary, gate
    )
    record_dir = _operator_record_dir(source_root, cfg)
    existing_records = _load_operator_invalidation_records(
        repo_root, cfg, source_root, state["issue_id"]
    )
    sequence = len(existing_records) + 1
    record_path = record_dir / f"{GATE_SLUGS[gate]}-invalidation-{sequence:04d}.json"
    if record_path.exists():
        raise HumanGateError(f"refusing operator invalidation record overwrite: {_rel(repo_root, record_path)}")
    if record_path in cleanup_paths:
        raise HumanGateError("operator invalidation record path is also a cleanup target")

    invalidated_checkpoints: list[dict[str, str]] = []
    keep = _completed_checkpoints(cfg, regeneration_boundary)
    for checkpoint in core.CHECKPOINTS:
        if checkpoint in keep:
            continue
        authority = state.get("checkpoint_provenance", {}).get(checkpoint)
        if isinstance(authority, dict):
            path = core.repo_local_path(repo_root, authority["path"], f"invalidated checkpoint {checkpoint}")
            invalidated_checkpoints.append({
                "checkpoint": checkpoint,
                "path": _rel(repo_root, path),
                "sha256": core.sha256_file(path),
            })
    canonical_rows = [
        {"name": name, "path": _rel(repo_root, path), "sha256": core.sha256_file(path)}
        for name, path in canonical
        if path.exists()
    ]
    seed = {
        "issue_id": state["issue_id"],
        "gate": gate,
        "sequence": sequence,
        "prior_state": reviewed_state,
        "prior_gate_inputs": artifacts,
        "invalidated_repository_commit_sha": commit_sha,
        "regeneration_boundary": regeneration_boundary,
        "operator_reference": operator_reference.strip(),
    }
    record = {
        "schema_version": "2.0-rc1",
        "issue_id": state["issue_id"],
        "gate": gate,
        "invalidation_id": f"operator-invalidation:{state['issue_id']}:{GATE_SLUGS[gate]}:{sequence}:{core.sha256_object(seed)[:16]}",
        "sequence": sequence,
        "human_decision": False,
        "prior_state": reviewed_state,
        "prior_gate_inputs": artifacts,
        "invalidated_repository_commit_sha": commit_sha,
        "work_branch": profile["paths"]["work_branch"],
        "expected_work_branch_head": expected_work_branch_head,
        "regeneration_boundary": regeneration_boundary,
        "reason": reason.strip(),
        "operator_reference": operator_reference.strip(),
        "invalidated_checkpoint_authority": sorted(invalidated_checkpoints, key=lambda row: row["checkpoint"]),
        "superseded_canonical_paths": sorted(canonical_rows, key=lambda row: row["path"]),
        "recorded_at": core.iso_utc(recorded_at or datetime.now().astimezone()),
    }
    schema_gate.validate_instance(
        record,
        repo_root / OPERATOR_INVALIDATION_SCHEMA,
        label="Operator Pending Gate Invalidation",
    )

    state_bytes = state_path.read_bytes()
    snapshots = {path: path.read_bytes() for path in cleanup_paths if path.exists()}
    removed: list[str] = []
    try:
        for path in cleanup_paths:
            if path.exists():
                if path.is_symlink() or not path.is_file():
                    raise HumanGateError(f"operator cleanup target became unsafe: {_rel(repo_root, path)}")
                path.unlink()
                removed.append(_rel(repo_root, path))
        record_dir.mkdir(parents=True, exist_ok=True)
        core.write_json(record_path, record)
        core.write_json(state_path, updated)
        validate_operator_invalidation_record(
            repo_root, record_path, expected_issue_id=state["issue_id"]
        )
        final_errors = agent.validate_agent_state(repo_root, cfg, core.load_json(state_path))
        if final_errors:
            raise HumanGateError(
                "operator invalidation did not produce resumable State: " + "; ".join(final_errors)
            )
    except Exception as exc:
        if record_path.exists():
            record_path.unlink(missing_ok=True)
        state_path.write_bytes(state_bytes)
        for path, raw in snapshots.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        if isinstance(exc, HumanGateError):
            raise
        raise HumanGateError(f"operator pending-Gate invalidation rolled back: {exc}") from exc
    return updated, record_path, sorted(removed)


def request_changes(
    repo_root: Path,
    cfg: dict[str, Any],
    state_path: Path,
    gate: str,
    regeneration_boundary: str,
    requested_changes: str,
    reviewed_by: str,
    reviewed_at: datetime,
    review_reference: str,
    *,
    expected_revision: int | None = None,
    reviewed_commit_sha: str | None = None,
) -> tuple[dict[str, Any], Path, Path, list[str]]:
    if gate not in GATE_KEYS:
        raise HumanGateError(f"unsupported Human Gate: {gate}")
    if not isinstance(requested_changes, str) or not requested_changes.strip():
        raise HumanGateError("REQUEST_CHANGES requires a non-empty requested_changes summary")
    if not reviewed_by.strip() or not review_reference.strip():
        raise HumanGateError("reviewed_by and review_reference are required")

    state, profile, source_root = _state_context(repo_root, cfg, state_path)
    _validate_gate_pending(state, gate)
    index = _load_review_index(repo_root, cfg, source_root, state["issue_id"])
    revision = _next_revision(index, gate, expected_revision)
    reviewed_state = _authority(repo_root, state_path)
    artifacts = _reviewed_artifacts(
        repo_root,
        cfg,
        state,
        profile,
        gate,
        require_current_candidate_validity=False,
    )
    commit_sha = _review_commit(
        repo_root,
        reviewed_commit_sha,
        profile["paths"]["work_branch"],
        reviewed_state,
        artifacts,
    )
    updated = _revised_state(repo_root, cfg, state, gate, regeneration_boundary)
    superseded, _ = _superseded_paths_for_regeneration(
        repo_root, cfg, state, profile, source_root, regeneration_boundary, gate
    )
    superseded.extend(
        _superseded_gate_authority_paths(
            repo_root, cfg, state, source_root, gate, regeneration_boundary
        )
    )
    record = _review_record_payload(
        issue_id=state["issue_id"],
        gate=gate,
        revision=revision,
        decision="REQUEST_CHANGES",
        reviewed_state=reviewed_state,
        reviewed_artifacts=artifacts,
        reviewed_repository_commit_sha=commit_sha,
        reviewed_by=reviewed_by,
        reviewed_at=reviewed_at,
        review_reference=review_reference,
        requested_changes=requested_changes.strip(),
        regeneration_boundary=regeneration_boundary,
        approval=None,
    )
    record_path, index_path = _write_review_record(repo_root, cfg, source_root, index, record)
    removed: list[str] = []
    for path in sorted(set(superseded), key=lambda item: _rel(repo_root, item)):
        if path.exists():
            path.unlink()
            removed.append(_rel(repo_root, path))
    core.write_json(state_path, updated)
    final_errors = agent.validate_agent_state(repo_root, cfg, core.load_json(state_path))
    if final_errors:
        raise HumanGateError("Human Gate revision did not produce resumable State: " + "; ".join(final_errors))
    return updated, record_path, index_path, removed


def request_architecture_revision(
    repo_root: Path,
    cfg: dict[str, Any],
    state_path: Path,
    regeneration_boundary: str,
    requested_changes: str,
    reviewed_by: str,
    reviewed_at: datetime,
    review_reference: str,
    *,
    expected_revision: int | None = None,
    reviewed_commit_sha: str | None = None,
) -> tuple[dict[str, Any], Path, Path, list[str]]:
    return request_changes(
        repo_root,
        cfg,
        state_path,
        "ARCHITECTURE_REVIEW",
        regeneration_boundary,
        requested_changes,
        reviewed_by,
        reviewed_at,
        review_reference,
        expected_revision=expected_revision,
        reviewed_commit_sha=reviewed_commit_sha,
    )


def request_publication_preview_revision(
    repo_root: Path,
    cfg: dict[str, Any],
    state_path: Path,
    regeneration_boundary: str,
    requested_changes: str,
    reviewed_by: str,
    reviewed_at: datetime,
    review_reference: str,
    *,
    expected_revision: int | None = None,
    reviewed_commit_sha: str | None = None,
) -> tuple[dict[str, Any], Path, Path, list[str]]:
    return request_changes(
        repo_root,
        cfg,
        state_path,
        "PUBLICATION_PREVIEW",
        regeneration_boundary,
        requested_changes,
        reviewed_by,
        reviewed_at,
        review_reference,
        expected_revision=expected_revision,
        reviewed_commit_sha=reviewed_commit_sha,
    )


def _path(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--config", default=str(core.DEFAULT_CONFIG))
    sub = parser.add_subparsers(dest="command", required=True)

    for command in ("record-architecture-approval", "record-publication-preview-approval"):
        child = sub.add_parser(command)
        child.add_argument("--state", required=True)
        child.add_argument("--expected-revision", type=int)
        child.add_argument("--reviewed-by", required=True)
        child.add_argument("--reviewed-at", required=True)
        child.add_argument("--review-reference", required=True)
        child.add_argument("--reviewed-commit-sha")

    for command in ("request-architecture-revision", "request-publication-preview-revision"):
        child = sub.add_parser(command)
        child.add_argument("--state", required=True)
        child.add_argument("--expected-revision", type=int)
        child.add_argument("--regeneration-boundary", required=True)
        child.add_argument("--requested-changes", required=True)
        child.add_argument("--reviewed-by", required=True)
        child.add_argument("--reviewed-at", required=True)
        child.add_argument("--review-reference", required=True)
        child.add_argument("--reviewed-commit-sha")

    invalidate = sub.add_parser("invalidate-pending-gate")
    invalidate.add_argument("--state", required=True)
    invalidate.add_argument("--gate", required=True, choices=sorted(GATE_KEYS))
    invalidate.add_argument("--regeneration-boundary", required=True)
    invalidate.add_argument("--reason", required=True)
    invalidate.add_argument("--operator-reference", required=True)
    invalidate.add_argument("--expected-work-branch-head", required=True)
    invalidate.add_argument("--invalidated-commit-sha")
    invalidate.add_argument("--recorded-at")

    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    try:
        cfg = core.load_json(_path(root, args.config))
        state_path = _path(root, args.state)
        if args.command == "invalidate-pending-gate":
            state, record, removed = invalidate_pending_gate(
                root,
                cfg,
                state_path,
                args.gate,
                args.regeneration_boundary,
                args.reason,
                args.operator_reference,
                args.expected_work_branch_head,
                invalidated_commit_sha=args.invalidated_commit_sha,
                recorded_at=core.parse_instant(args.recorded_at) if args.recorded_at else datetime.now().astimezone(),
            )
            print(json.dumps({
                "state": _rel(root, state_path),
                "lifecycle_state": state["lifecycle_state"],
                "next_action": state["next_action"],
                "terminal_reason": state["terminal_reason"],
                "operator_invalidation_record": _rel(root, record),
                "removed_paths": removed,
                "human_decision": False,
            }, ensure_ascii=False, indent=2))
            return 0
        reviewed_at = core.parse_instant(args.reviewed_at)
        common = {
            "expected_revision": args.expected_revision,
            "reviewed_commit_sha": args.reviewed_commit_sha,
        }
        if args.command == "record-architecture-approval":
            state, record, index = record_architecture_approval(
                root, cfg, state_path, args.reviewed_by, reviewed_at, args.review_reference, **common
            )
            removed: list[str] = []
        elif args.command == "record-publication-preview-approval":
            state, record, index = record_publication_preview_approval(
                root, cfg, state_path, args.reviewed_by, reviewed_at, args.review_reference, **common
            )
            removed = []
        elif args.command == "request-architecture-revision":
            state, record, index, removed = request_architecture_revision(
                root,
                cfg,
                state_path,
                args.regeneration_boundary,
                args.requested_changes,
                args.reviewed_by,
                reviewed_at,
                args.review_reference,
                **common,
            )
        elif args.command == "request-publication-preview-revision":
            state, record, index, removed = request_publication_preview_revision(
                root,
                cfg,
                state_path,
                args.regeneration_boundary,
                args.requested_changes,
                args.reviewed_by,
                reviewed_at,
                args.review_reference,
                **common,
            )
        else:
            raise HumanGateError(f"unsupported Human Gate command: {args.command}")
        print(
            json.dumps(
                {
                    "state": _rel(root, state_path),
                    "lifecycle_state": state["lifecycle_state"],
                    "next_action": state["next_action"],
                    "terminal_reason": state["terminal_reason"],
                    "review_record": _rel(root, record),
                    "review_index": _rel(root, index),
                    "removed_paths": removed,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
