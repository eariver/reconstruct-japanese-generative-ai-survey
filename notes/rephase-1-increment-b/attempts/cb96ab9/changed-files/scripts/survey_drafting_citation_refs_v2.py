#!/usr/bin/env python3
"""Exact Draft Package citation-reference resolution shared by drafting and replay."""
from __future__ import annotations

from typing import Any


def ref_rows(card: dict[str, Any], task_id: str, mode: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if mode in {"CLAIMS", "CLAIMS_AND_LIMITATIONS"}:
        for row in card.get("claims", []):
            rows.append({
                "evidence_task_id": task_id,
                "kind": "CLAIM",
                "evidence_id": row["statement_id"],
                "subject_id": row["subject_id"],
                "subject_role": row["subject_role"],
            })
        if not rows:
            for row in card.get("temporal", {}).get("events", []):
                rows.append({
                    "evidence_task_id": task_id,
                    "kind": "EVENT",
                    "evidence_id": row["event_id"],
                    "subject_id": row["subject_id"],
                    "subject_role": row["subject_role"],
                })
    if mode in {"LIMITATIONS", "CLAIMS_AND_LIMITATIONS"}:
        for row in card.get("limitations", []):
            rows.append({
                "evidence_task_id": task_id,
                "kind": "LIMITATION",
                "evidence_id": row["statement_id"],
                "subject_id": row["subject_id"],
                "subject_role": row["subject_role"],
            })
    return rows


def refs(package: dict[str, Any], discovery_ids: list[str], mode: str) -> list[dict[str, Any]]:
    """Preserve drafting's exact-one resolution and first-seen ordered de-duplication."""
    if mode == "NONE":
        if discovery_ids:
            raise ValueError("ref_mode NONE cannot carry discovery_ids")
        return []
    evidence_inputs = package.get("evidence_inputs")
    if not isinstance(evidence_inputs, list) or not evidence_inputs:
        raise ValueError(f'Draft Package has no authorized Evidence inputs: {package.get("package_id")}')
    input_by_candidate: dict[str, dict[str, Any]] = {}
    for offset, row in enumerate(evidence_inputs):
        if not isinstance(row, dict):
            raise ValueError(f"Draft Package Evidence input must be an object: index={offset}")
        candidate_id = row.get("candidate_id")
        if not isinstance(candidate_id, str) or not candidate_id:
            raise ValueError(f"Draft Package Evidence input candidate_id invalid: index={offset}")
        if candidate_id in input_by_candidate:
            raise ValueError(f"Draft Package Evidence inputs duplicate candidate_id: {candidate_id}")
        input_by_candidate[candidate_id] = row
    authorized = set(input_by_candidate)
    matrix_rows = package["candidate_matrix"]["rows"]
    resolved: list[dict[str, Any]] = []
    for did in discovery_ids:
        hits = [
            row for row in matrix_rows
            if row["candidate_id"] in authorized and did in row.get("discovery_ids", [])
        ]
        if len(hits) != 1:
            raise ValueError(
                f'Discovery ID must resolve exactly once inside package {package["package_id"]}: {did}'
            )
        item = input_by_candidate[hits[0]["candidate_id"]]
        resolved.extend(ref_rows(item["evidence_card"], item["evidence_task_id"], mode))
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for ref in resolved:
        key = tuple(
            ref[name]
            for name in ("evidence_task_id", "kind", "evidence_id", "subject_id", "subject_role")
        )
        if key not in seen:
            seen.add(key)
            deduped.append(ref)
    if not deduped:
        raise ValueError(
            f'No Evidence refs resolved for {package["package_id"]} {discovery_ids} mode={mode}'
        )
    return deduped
