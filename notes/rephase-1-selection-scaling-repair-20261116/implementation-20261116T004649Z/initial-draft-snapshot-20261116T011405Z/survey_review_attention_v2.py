#!/usr/bin/env python3
"""Bounded Human-review attention surface for Architecture Review."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from scripts import survey_production_v2 as core
from scripts import survey_schema_v2 as schema_gate

ATTENTION_SCHEMA = Path("schemas/architecture-review-attention-v2.schema.json")


def _safe_file(repo_root: Path, path: Path) -> Path:
    root = repo_root.resolve()
    resolved = path.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"review-attention input escapes repository: {path}") from exc
    if resolved.is_symlink() or not resolved.is_file():
        raise ValueError(f"review-attention input missing or unsafe: {path}")
    return resolved


def _rel(repo_root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(repo_root.resolve()))


def _build_attention_payload(
    repo_root: Path,
    screening_acceptance_path: Path,
    materiality_ledger_path: Path,
    candidate_selection_path: Path,
    *,
    limit: int = 50,
) -> dict[str, Any]:
    """Private pure payload builder (existing construction+validation, no write).

    Extracted from build_attention for checked-writer expected-bytes binding.
    No second algorithm/new module; public builder and runner writer share it.
    Preserves limit/count/truncation/overflow semantics and basis binds.
    """
    if limit < 1 or limit > 500:
        raise ValueError("review-attention limit must be between 1 and 500")
    screening_path = _safe_file(repo_root, screening_acceptance_path)
    materiality_path = _safe_file(repo_root, materiality_ledger_path)
    selection_path = _safe_file(repo_root, candidate_selection_path)
    screening = core.load_json(screening_path)
    materiality = core.load_json(materiality_path)
    selection = core.load_json(selection_path)
    issue_ids = {screening.get("issue_id"), materiality.get("issue_id"), selection.get("issue_id")}
    if len(issue_ids) != 1 or None in issue_ids:
        raise ValueError("review-attention inputs disagree on issue_id")
    issue_id = next(iter(issue_ids))

    items: list[dict[str, Any]] = []
    for row in screening.get("decisions", []):
        decision = row.get("decision")
        if decision not in {"DROP", "MAYBE", "INSPECT"}:
            continue
        subject_id = row.get("discovery_id")
        rationale = row.get("reason")
        if not isinstance(subject_id, str) or not subject_id or not isinstance(rationale, str) or not rationale.strip():
            raise ValueError("screening review-attention row lacks stable id/rationale")
        items.append(
            {
                "item_id": f"SCREENING:{subject_id}:{decision}",
                "stage": "SCREENING",
                "subject_id": subject_id,
                "decision": decision,
                "rationale": rationale,
            }
        )

    for row in materiality.get("rows", []):
        decision = row.get("downstream_disposition")
        if decision not in {"HOLD", "NON_MATERIAL", "EXCLUDED", "DUPLICATE"}:
            continue
        subject_id = row.get("discovery_id")
        rationale = row.get("rationale")
        if not isinstance(subject_id, str) or not subject_id or not isinstance(rationale, str) or not rationale.strip():
            raise ValueError("materiality review-attention row lacks stable id/rationale")
        items.append(
            {
                "item_id": f"MATERIALITY:{subject_id}:{decision}",
                "stage": "MATERIALITY",
                "subject_id": subject_id,
                "decision": decision,
                "rationale": rationale,
            }
        )

    for row in selection.get("assignments", []):
        disposition = row.get("disposition")
        if disposition not in {"HOLD", "REJECT", "INSPECT"}:
            continue
        subject_id = row.get("candidate_id")
        rationale = row.get("rationale")
        if not isinstance(subject_id, str) or not subject_id or not isinstance(rationale, str) or not rationale.strip():
            raise ValueError("selection review-attention row lacks stable id/rationale")
        decision = "REJECT" if disposition == "REJECT" else disposition
        items.append(
            {
                "item_id": f"SELECTION:{subject_id}:{decision}",
                "stage": "SELECTION",
                "subject_id": subject_id,
                "decision": decision,
                "rationale": rationale,
            }
        )

    items = sorted(items, key=lambda row: (row["stage"], row["decision"], row["subject_id"], row["item_id"]))
    if len({row["item_id"] for row in items}) != len(items):
        raise ValueError("review-attention item_id collision")
    total = len(items)
    shown = items[:limit]
    counts = Counter(f"{row['stage']}:{row['decision']}" for row in items)
    payload = {
        "schema_version": "2.0-rc1",
        "issue_id": issue_id,
        "basis": {
            "screening_acceptance_path": _rel(repo_root, screening_path),
            "screening_acceptance_sha256": core.sha256_file(screening_path),
            "materiality_ledger_path": _rel(repo_root, materiality_path),
            "materiality_ledger_sha256": core.sha256_file(materiality_path),
            "candidate_selection_path": _rel(repo_root, selection_path),
            "candidate_selection_sha256": core.sha256_file(selection_path),
        },
        "limit": limit,
        "total_count": total,
        "shown_count": len(shown),
        "overflow_count": max(0, total - len(shown)),
        "truncated": total > len(shown),
        "counts": dict(sorted(counts.items())),
        "items": shown,
    }
    schema_gate.validate_instance(payload, repo_root / ATTENTION_SCHEMA, label="Architecture Review attention")
    if payload["shown_count"] + payload["overflow_count"] != payload["total_count"]:
        raise ValueError("review-attention bounded count invariant failed")
    if payload["truncated"] != (payload["overflow_count"] > 0):
        raise ValueError("review-attention truncation invariant failed")
    return payload


def build_attention(
    repo_root: Path,
    screening_acceptance_path: Path,
    materiality_ledger_path: Path,
    candidate_selection_path: Path,
    output_path: Path,
    *,
    limit: int = 50,
) -> Path:
    payload = _build_attention_payload(
        repo_root,
        screening_acceptance_path,
        materiality_ledger_path,
        candidate_selection_path,
        limit=limit,
    )
    if output_path.exists():
        raise ValueError(f"refusing to overwrite Architecture Review attention: {output_path}")
    core.write_json(output_path, payload)
    return output_path


def validate_attention(repo_root: Path, path: Path) -> dict[str, Any]:
    payload = schema_gate.load_and_validate_json(path, repo_root / ATTENTION_SCHEMA, label="Architecture Review attention")
    basis = payload["basis"]
    for key in ("screening_acceptance", "materiality_ledger", "candidate_selection"):
        artifact_path = _safe_file(repo_root, repo_root / basis[f"{key}_path"])
        if core.sha256_file(artifact_path) != basis[f"{key}_sha256"]:
            raise ValueError(f"Architecture Review attention basis drift: {key}")
    if payload["shown_count"] != len(payload["items"]):
        raise ValueError("Architecture Review attention shown_count mismatch")
    if payload["shown_count"] + payload["overflow_count"] != payload["total_count"]:
        raise ValueError("Architecture Review attention total/overflow mismatch")
    if payload["truncated"] != (payload["overflow_count"] > 0):
        raise ValueError("Architecture Review attention truncated flag mismatch")
    return payload
