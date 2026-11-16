#!/usr/bin/env python3
"""Profile-neutral Candidate Matrix, Selection, Architecture, and Review Summary."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from scripts import survey_completeness_v2 as completeness
from scripts import survey_evidence_v2 as evidence
from scripts import survey_production_v2 as core

MATRIX_SCHEMA = Path("schemas/candidate-matrix-v2.schema.json")
SELECTION_SCHEMA = Path("schemas/candidate-selection-v2.schema.json")
ARCHITECTURE_SCHEMA = Path("schemas/issue-architecture-v2.schema.json")
REVIEW_SCHEMA = Path("schemas/architecture-review-summary-v2.schema.json")
DISPOSITIONS = {"SELECTED", "HOLD", "REJECT", "INSPECT"}
USAGES = {"PRIMARY", "SUPPORTING", "NONE"}
MATERIAL_REVIEW = {"MATERIAL", "CONTEXT"}


def candidate_id(issue_id: str, task_id: str) -> str:
    digest = hashlib.sha256(task_id.encode("utf-8")).hexdigest()[:16]
    return f"candidate:{issue_id}:{digest}"


def _counter(values: list[str]) -> dict[str, int]:
    counts = Counter(values)
    return {key: counts[key] for key in sorted(counts)}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _aware_datetime(value: Any) -> bool:
    if not _nonempty(value):
        return False
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _research_expansion_summary(discoveries: list[dict[str, Any]]) -> dict[str, Any]:
    passes = [row["provenance"]["research_pass"] for row in discoveries]
    parent_links = sum(len(row["provenance"]["parent_refs"]) for row in discoveries)
    obligation_links = sum(len(row["provenance"]["obligation_ids"]) for row in discoveries)
    unique_obligations = {
        obligation_id
        for row in discoveries
        for obligation_id in row["provenance"]["obligation_ids"]
    }
    roots = sum(1 for row in discoveries if not row["provenance"]["parent_refs"])
    expanded = sum(
        1
        for row in discoveries
        if row["provenance"]["origin"] not in {"BASE", "CARRY_OVER"}
    )
    return {
        "max_research_pass": max(passes, default=0),
        "pass_counts": _counter([str(value) for value in passes]),
        "parent_link_count": parent_links,
        "obligation_link_count": obligation_links,
        "unique_obligation_count": len(unique_obligations),
        "root_discovery_count": roots,
        "expanded_discovery_count": expanded,
    }


def _require_contracts(repo_root: Path) -> None:
    for rel in (MATRIX_SCHEMA, SELECTION_SCHEMA, ARCHITECTURE_SCHEMA, REVIEW_SCHEMA):
        if not (repo_root / rel).is_file():
            raise ValueError(f"WU-008 contract file missing: {rel}")


def _load_upstream_content(
    repo_root: Path,
    profile_path: Path,
    discovery_path: Path,
    screening_path: Path,
    evidence_path: Path,
    views_path: Path,
    ledger_path: Path,
    completeness_path: Path,
    expectations: dict[str, Any],
    root_records: list[dict[str, Any]] | None = None,
    root_path: Path | None = None,
) -> dict[str, Any]:
    """State-free renewal content core for WU-008 upstream (Layer-A).

    Mirrors _load_upstream but via State-free content validators (session
    expectations + root, §11.3, no verify_state_basis / implementation_sha /
    checkpoint / pending). Shares pure row/identity checks via same downstream
    content validators (no code copy drift for those); upstream loading itself
    is the narrow extraction (State block removed).
    """
    _require_contracts(repo_root)
    profile = core.load_json(profile_path)
    if profile.get("issue_id") != expectations.get("issue_id") or profile.get("research_profile") != expectations.get("research_profile"):
        raise ValueError("WU-008 Profile/renewal expectations identity mismatch")
    screening_acceptance, _, discoveries = evidence._validate_screening_acceptance_content(
        repo_root, screening_path, discovery_path, expectations, root_records, root_path,
    )
    evidence_acceptance, _ = evidence._validate_evidence_acceptance_content(
        repo_root, evidence_path, expectations, root_records, root_path,
    )
    views_acceptance = evidence._validate_edition_views_acceptance_content(
        repo_root, profile_path, evidence_path, views_path, expectations, root_records, root_path,
    )
    ledger = core.load_json(ledger_path)
    evidence._validate_materiality_ledger_content(
        ledger, repo_root, profile_path, discovery_path, screening_path,
        evidence_path, views_path, expectations, root_records, root_path,
    )
    completeness_result = core.load_json(completeness_path)
    # Completeness content via completeness module (State-free, no implementation_sha).
    comp_errors = completeness._validate_profile_completeness_content(
        completeness_result, repo_root, profile_path, discovery_path,
        screening_path, evidence_path, views_path, ledger_path,
        expectations, root_records, root_path,
    )
    if comp_errors:
        raise ValueError(f"Profile Completeness invalid: {'; '.join(comp_errors)}")
    for payload, label in (
        (screening_acceptance, "Screening"),
        (evidence_acceptance, "Evidence"),
        (views_acceptance, "Edition View"),
        (ledger, "Materiality"),
        (completeness_result, "Completeness"),
    ):
        if payload.get("issue_id") != profile["issue_id"]:
            raise ValueError(f"WU-008 {label}/Profile issue identity divergence")
        if payload.get("research_profile") != profile["research_profile"]:
            raise ValueError(f"WU-008 {label}/Profile research identity divergence")
    return {
        "profile": profile,
        "discoveries": discoveries,
        "screening": screening_acceptance,
        "evidence": evidence_acceptance,
        "views": views_acceptance,
        "ledger": ledger,
        "completeness": completeness_result,
    }


def derive_candidate_matrix_content(
    repo_root: Path,
    profile_path: Path,
    discovery_path: Path,
    screening_path: Path,
    evidence_path: Path,
    views_path: Path,
    ledger_path: Path,
    completeness_path: Path,
    expectations: dict[str, Any],
    root_records: list[dict[str, Any]] | None = None,
    root_path: Path | None = None,
) -> dict[str, Any]:
    """State-free renewal content core for Candidate Matrix derivation.

    Shares pure matrix row derivation with derive_candidate_matrix (same row
    construction below, no drift); upstream loading via _load_upstream_content.
    """
    upstream = _load_upstream_content(
        repo_root, profile_path, discovery_path, screening_path, evidence_path,
        views_path, ledger_path, completeness_path, expectations, root_records, root_path,
    )
    # Pure matrix row derivation below mirrors derive_candidate_matrix rows
    # exactly (same candidate_id, basis, rows, summary); extracted as shared
    # helper to prevent drift.
    return _derive_matrix_rows_content(repo_root, upstream, profile_path, completeness_path, ledger_path, evidence_path, views_path)


def _derive_matrix_rows_content(
    repo_root: Path,
    upstream: dict[str, Any],
    profile_path: Path,
    completeness_path: Path,
    ledger_path: Path,
    evidence_path: Path,
    views_path: Path,
) -> dict[str, Any]:
    """Shared pure Candidate Matrix row derivation (no State)."""
    profile = upstream["profile"]
    evidence_acceptance = upstream["evidence"]
    views_acceptance = upstream["views"]
    ledger = upstream["ledger"]
    ledger_by_task: dict[str, dict[str, Any]] = {}
    for row in ledger["rows"]:
        for task_id in row["evidence_task_ids"]:
            if task_id in ledger_by_task:
                raise ValueError(f"Materiality maps task more than once: {task_id}")
            ledger_by_task[task_id] = row
    views_by_task = {row["evidence_task_id"]: row for row in views_acceptance["views"]}
    rows: list[dict[str, Any]] = []
    for evidence_row in sorted(
        evidence_acceptance["results"], key=lambda value: value["evidence_task_id"]
    ):
        task_id = evidence_row["evidence_task_id"]
        if task_id not in ledger_by_task or task_id not in views_by_task:
            raise ValueError(f"silent drop before Matrix: {task_id}")
        card_path = evidence_path.parent / "results" / evidence_row["filename"]
        view_path = views_path.parent / "views" / evidence.view_filename(task_id)
        if core.sha256_file(card_path) != evidence_row["sha256"]:
            raise ValueError(f"Matrix Evidence bytes changed: {task_id}")
        if core.sha256_file(view_path) != views_by_task[task_id]["view_sha256"]:
            raise ValueError(f"Matrix Edition View bytes changed: {task_id}")
        card = core.load_json(card_path)
        view = core.load_json(view_path)
        boundaries = list(
            dict.fromkeys(
                [
                    *[item["text"] for item in card["limitations"]],
                    *card["verification"]["unresolved_questions"],
                    *card["verification"]["contradictions"],
                ]
            )
        )
        rows.append(
            {
                "candidate_id": candidate_id(profile["issue_id"], task_id),
                "evidence_task_id": task_id,
                "discovery_ids": list(evidence_row["discovery_ids"]),
                "evidence_sha256": evidence_row["sha256"],
                "edition_view_sha256": views_by_task[task_id]["view_sha256"],
                "title": card["artifact"]["canonical_name"],
                "artifact_type": card["artifact"]["artifact_type"],
                "evidence_status": evidence_row["status"],
                "materiality": views_by_task[task_id]["materiality"],
                "scope_dimensions": list(views_by_task[task_id]["scope_dimensions"]),
                "comparison": {
                    "source_count": len(card["sources"]),
                    "claim_count": len(card["claims"]),
                    "metric_count": len(card["metrics"]),
                    "limitation_count": len(card["limitations"]),
                    "unresolved_question_count": len(
                        card["verification"]["unresolved_questions"]
                    ),
                    "contradiction_count": len(card["verification"]["contradictions"]),
                    "entity_count": len(card["entities"]),
                },
                "remaining_boundaries": boundaries,
                "profile_extensions": view["profile_annotations"],
            }
        )
    if set(ledger_by_task) != {row["evidence_task_id"] for row in rows}:
        raise ValueError("Matrix/Evidence/Materiality task set divergence")
    return {
        "schema_version": "2.0-rc1",
        "issue_id": profile["issue_id"],
        "research_profile": profile["research_profile"],
        "basis": {
            "production_profile_sha256": core.sha256_file(profile_path),
            "profile_completeness_sha256": core.sha256_file(completeness_path),
            "materiality_ledger_sha256": core.sha256_file(ledger_path),
            "evidence_acceptance_sha256": core.sha256_file(evidence_path),
            "edition_views_acceptance_sha256": core.sha256_file(views_path),
        },
        "rows": rows,
        "summary": {
            "candidate_count": len(rows),
            "materiality_counts": _counter([row["materiality"] for row in rows]),
            "evidence_status_counts": _counter(
                [row["evidence_status"] for row in rows]
            ),
        },
    }


def _load_upstream(
    repo_root: Path,
    profile_path: Path,
    discovery_path: Path,
    screening_path: Path,
    evidence_path: Path,
    views_path: Path,
    ledger_path: Path,
    completeness_path: Path,
    implementation_sha: str,
) -> dict[str, Any]:
    _require_contracts(repo_root)
    profile = core.load_json(profile_path)
    screening_acceptance, _, discoveries = evidence.validate_screening_acceptance(
        repo_root,
        screening_path,
        discovery_path,
        profile["issue_id"],
        implementation_sha,
    )
    evidence_acceptance, _ = evidence.validate_evidence_acceptance(
        repo_root, evidence_path, implementation_sha
    )
    views_acceptance = evidence.validate_edition_views_acceptance(
        repo_root,
        profile_path,
        evidence_path,
        views_path,
        implementation_sha,
    )
    ledger = core.load_json(ledger_path)
    evidence.validate_materiality_ledger(
        ledger,
        repo_root,
        profile_path,
        discovery_path,
        screening_path,
        evidence_path,
        views_path,
        implementation_sha,
    )
    completeness_result = core.load_json(completeness_path)
    completeness_errors = completeness.validate_profile_completeness(
        completeness_result,
        repo_root,
        profile_path,
        discovery_path,
        screening_path,
        evidence_path,
        views_path,
        ledger_path,
        implementation_sha,
    )
    if completeness_errors:
        raise ValueError(f"Profile Completeness invalid: {'; '.join(completeness_errors)}")
    for payload, label in (
        (screening_acceptance, "Screening"),
        (evidence_acceptance, "Evidence"),
        (views_acceptance, "Edition View"),
        (ledger, "Materiality"),
        (completeness_result, "Completeness"),
    ):
        if payload.get("issue_id") != profile["issue_id"]:
            raise ValueError(f"WU-008 {label}/Profile issue identity divergence")
        if payload.get("research_profile") != profile["research_profile"]:
            raise ValueError(f"WU-008 {label}/Profile research identity divergence")
    return {
        "profile": profile,
        "discoveries": discoveries,
        "screening": screening_acceptance,
        "evidence": evidence_acceptance,
        "views": views_acceptance,
        "ledger": ledger,
        "completeness": completeness_result,
    }


def derive_candidate_matrix(
    repo_root: Path,
    profile_path: Path,
    discovery_path: Path,
    screening_path: Path,
    evidence_path: Path,
    views_path: Path,
    ledger_path: Path,
    completeness_path: Path,
    implementation_sha: str,
) -> dict[str, Any]:
    """DM022 B-side: pure derivation stays guard-free; callers pass R4 paths.

    The profile-aware entry (run_selection_architecture) enforces G + R4 and
    never lets this pure function select State itself. Content/validate/selection/
    review paths remain pure (_content never verify_state_basis).
    """
    upstream = _load_upstream(
        repo_root,
        profile_path,
        discovery_path,
        screening_path,
        evidence_path,
        views_path,
        ledger_path,
        completeness_path,
        implementation_sha,
    )
    # Shared pure row derivation (no drift vs renewal content).
    return _derive_matrix_rows_content(repo_root, upstream, profile_path, completeness_path, ledger_path, evidence_path, views_path)


def validate_candidate_matrix(matrix: dict[str, Any], *args: Any) -> list[str]:
    try:
        expected = derive_candidate_matrix(*args)
    except ValueError as exc:
        return [str(exc)]
    if matrix != expected:
        return [
            "Candidate Matrix does not exactly match validated upstream Evidence/View/Materiality derivation"
        ]
    return []


def _validate_candidate_matrix_against_upstream(
    repo_root: Path,
    matrix: dict[str, Any],
    upstream: dict[str, Any],
    profile_path: Path,
    completeness_path: Path,
    ledger_path: Path,
    evidence_path: Path,
    views_path: Path,
) -> list[str]:
    """Private matrix equality against held upstream (no second _load_upstream).

    Re-derives rows via shared pure P only; 45AG removed. repo_root FIRST per ROOT §6.2.
    """
    try:
        expected = _derive_matrix_rows_content(
            repo_root, upstream, profile_path, completeness_path, ledger_path, evidence_path, views_path
        )
    except ValueError as exc:
        return [str(exc)]
    if matrix != expected:
        return [
            "Candidate Matrix does not exactly match validated upstream Evidence/View/Materiality derivation"
        ]
    return []


def write_candidate_matrix(path: Path, payload: dict[str, Any]) -> Path:
    if path.exists():
        raise ValueError(f"refusing to overwrite Candidate Matrix: {path}")
    core.write_json(path, payload)
    return path


def validate_selection(
    repo_root: Path,
    selection: dict[str, Any],
    profile_path: Path,
    matrix_path: Path,
    completeness_path: Path,
    ledger_path: Path,
) -> list[str]:
    errors: list[str] = []
    cfg = core.load_json(repo_root / core.DEFAULT_CONFIG)
    profile = core.load_json(profile_path)
    matrix = core.load_json(matrix_path)
    completeness_result = core.load_json(completeness_path)
    ledger = core.load_json(ledger_path)
    required = {
        "schema_version",
        "issue_id",
        "research_profile",
        "publication_profile",
        "selection_version",
        "status",
        "basis",
        "assignments",
        "summary",
    }
    if set(selection) != required:
        return [
            "Candidate Selection fields must exactly match v2 contract; Human approval fields are forbidden"
        ]
    if selection.get("schema_version") != "2.0-rc1" or selection.get("status") != "ESTABLISHED":
        errors.append("Candidate Selection schema/status invalid")
    if selection.get("issue_id") != profile.get("issue_id") or selection.get("issue_id") != matrix.get("issue_id"):
        errors.append("Candidate Selection issue identity mismatch")
    if selection.get("research_profile") != profile.get("research_profile") or selection.get("research_profile") != matrix.get("research_profile"):
        errors.append("Candidate Selection research Profile identity mismatch")
    if selection.get("publication_profile") != profile.get("publication_profile"):
        errors.append("Candidate Selection Publication Profile identity mismatch")
    expected_basis = {
        "production_profile_sha256": core.sha256_file(profile_path),
        "candidate_matrix_sha256": core.sha256_file(matrix_path),
        "profile_completeness_sha256": core.sha256_file(completeness_path),
        "materiality_ledger_sha256": core.sha256_file(ledger_path),
    }
    if selection.get("basis") != expected_basis:
        errors.append(
            "Candidate Selection basis does not bind exact Profile/Matrix/Completeness/Materiality bytes"
        )
    if not _nonempty(selection.get("selection_version")):
        errors.append("selection_version must be non-empty")

    research_contract = cfg["research_profiles"].get(profile.get("research_profile"), {})
    publication_contract = cfg["publication_profiles"].get(
        profile.get("publication_profile"), {}
    )
    research_namespace = research_contract.get("role_namespace")
    publication_namespace = publication_contract.get("role_namespace")
    if not _nonempty(research_namespace) or not research_namespace.endswith(":"):
        errors.append("Research Profile role_namespace contract is missing or invalid")
    if not _nonempty(publication_namespace) or not publication_namespace.endswith(":"):
        errors.append("Publication Profile role_namespace contract is missing or invalid")

    rows = matrix.get("rows")
    assignments = selection.get("assignments")
    if not isinstance(rows, list) or not isinstance(assignments, list):
        return errors + ["Matrix rows and Selection assignments must be arrays"]
    matrix_by_id = {
        row.get("candidate_id"): row for row in rows if isinstance(row, dict)
    }
    assignment_ids: list[str] = []
    dispositions: list[str] = []
    assignment_fields = {
        "candidate_id",
        "disposition",
        "rationale",
        "architecture_usage",
        "publication_role",
        "architecture_role",
        "profile_extensions",
    }
    for index, assignment in enumerate(assignments):
        prefix = f"assignments[{index}]"
        if not isinstance(assignment, dict) or set(assignment) != assignment_fields:
            errors.append(f"{prefix} fields invalid")
            continue
        cid = assignment.get("candidate_id")
        if cid not in matrix_by_id:
            errors.append(f"{prefix} references unknown Matrix candidate: {cid}")
            continue
        assignment_ids.append(cid)
        disposition = assignment.get("disposition")
        dispositions.append(disposition)
        if disposition not in DISPOSITIONS:
            errors.append(f"{prefix} disposition invalid")
            continue
        if not _nonempty(assignment.get("rationale")):
            errors.append(f"{prefix} rationale required")
        usage = assignment.get("architecture_usage")
        if usage not in USAGES:
            errors.append(f"{prefix} architecture_usage invalid")
        publication_role = assignment.get("publication_role")
        architecture_role = assignment.get("architecture_role")
        if publication_role is not None and not _nonempty(publication_role):
            errors.append(f"{prefix} publication_role invalid")
        if architecture_role is not None and not _nonempty(architecture_role):
            errors.append(f"{prefix} architecture_role invalid")
        if not isinstance(assignment.get("profile_extensions"), dict):
            errors.append(f"{prefix} profile_extensions must be an object")
        row = matrix_by_id[cid]
        if disposition == "SELECTED":
            if usage not in {"PRIMARY", "SUPPORTING"}:
                errors.append(
                    f"{cid}: SELECTED candidate requires PRIMARY or SUPPORTING architecture_usage"
                )
            if publication_role is None and architecture_role is None:
                errors.append(
                    f"{cid}: SELECTED candidate requires a Profile/Publication-owned proposed role"
                )
            if publication_role is not None and _nonempty(publication_namespace) and not publication_role.startswith(publication_namespace):
                errors.append(
                    f"{cid}: publication_role is outside Publication Profile namespace {publication_namespace}"
                )
            if architecture_role is not None and _nonempty(research_namespace) and not architecture_role.startswith(research_namespace):
                errors.append(
                    f"{cid}: architecture_role is outside Research Profile namespace {research_namespace}"
                )
            if row["materiality"] in {"NON_MATERIAL", "HOLD"}:
                errors.append(f"{cid}: {row['materiality']} candidate cannot be SELECTED")
            if row["evidence_status"] in {"REJECTED", "NEEDS_MORE"}:
                errors.append(
                    f"{cid}: unresolved/rejected Evidence cannot be SELECTED"
                )
        else:
            if usage != "NONE" or publication_role is not None or architecture_role is not None:
                errors.append(
                    f"{cid}: non-selected candidate must not carry publication/architecture assignment"
                )
    if len(assignment_ids) != len(set(assignment_ids)):
        errors.append("Candidate Selection contains duplicate candidate assignments")
    if set(assignment_ids) != set(matrix_by_id) or len(assignment_ids) != len(
        matrix_by_id
    ):
        errors.append("Candidate Selection must assign every Matrix candidate exactly once")
    expected_summary = {
        "candidate_count": len(rows),
        "disposition_counts": _counter(dispositions),
        "selected_count": sum(value == "SELECTED" for value in dispositions),
    }
    if selection.get("summary") != expected_summary:
        errors.append("Candidate Selection summary does not match assignments")
    for payload, label in (
        (completeness_result, "Completeness"),
        (ledger, "Materiality"),
    ):
        if payload.get("issue_id") != selection.get("issue_id") or payload.get(
            "research_profile"
        ) != selection.get("research_profile"):
            errors.append(f"Candidate Selection {label} identity divergence")
    return errors


def validate_architecture(
    repo_root: Path,
    architecture: dict[str, Any],
    profile_path: Path,
    completeness_path: Path,
    ledger_path: Path,
    matrix_path: Path,
    selection_path: Path,
    require_approved: bool = False,
) -> list[str]:
    selection = core.load_json(selection_path)
    selection_errors = validate_selection(
        repo_root,
        selection,
        profile_path,
        matrix_path,
        completeness_path,
        ledger_path,
    )
    if selection_errors:
        return [f"Candidate Selection invalid: {'; '.join(selection_errors)}"]
    profile = core.load_json(profile_path)
    matrix = core.load_json(matrix_path)
    errors: list[str] = []
    required = {
        "schema_version",
        "issue_id",
        "research_profile",
        "publication_profile",
        "status",
        "basis",
        "editorial_thesis",
        "architecture_goals",
        "page_plan",
        "packages",
        "selected_exceptions",
        "profile_extensions",
        "publication_extensions",
        "human_review",
    }
    if set(architecture) != required:
        return ["Issue Architecture fields must exactly match generic v2 envelope"]
    if architecture.get("schema_version") != "2.0-rc1":
        errors.append("Issue Architecture schema_version mismatch")
    if architecture.get("issue_id") != profile["issue_id"] or architecture.get(
        "research_profile"
    ) != profile["research_profile"]:
        errors.append("Issue Architecture Profile identity mismatch")
    if architecture.get("publication_profile") != profile["publication_profile"]:
        errors.append("Issue Architecture Publication Profile mismatch")
    expected_basis = {
        "production_profile_sha256": core.sha256_file(profile_path),
        "profile_completeness_sha256": core.sha256_file(completeness_path),
        "materiality_ledger_sha256": core.sha256_file(ledger_path),
        "candidate_matrix_sha256": core.sha256_file(matrix_path),
        "candidate_selection_sha256": core.sha256_file(selection_path),
    }
    if architecture.get("basis") != expected_basis:
        errors.append("Issue Architecture basis does not bind exact upstream artifacts")
    if not _nonempty(architecture.get("editorial_thesis")):
        errors.append("Issue Architecture editorial_thesis required")
    goals = architecture.get("architecture_goals")
    if not isinstance(goals, list) or not goals or len(goals) != len(
        set(goals)
    ) or any(not _nonempty(value) for value in goals):
        errors.append("Issue Architecture architecture_goals invalid")
    if not isinstance(architecture.get("profile_extensions"), dict) or not isinstance(
        architecture.get("publication_extensions"), dict
    ):
        errors.append("Issue Architecture extensions must be objects")

    page_plan = architecture.get("page_plan")
    if not isinstance(page_plan, dict) or set(page_plan) != {
        "target_pages",
        "max_pages",
        "notes",
    }:
        errors.append("Issue Architecture page_plan fields invalid")
    else:
        target = page_plan.get("target_pages")
        maximum = page_plan.get("max_pages")
        for key, value in (("target_pages", target), ("max_pages", maximum)):
            if value is not None and (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
                or value <= 0
            ):
                errors.append(f"page_plan.{key} must be positive or null")
        if isinstance(target, (int, float)) and isinstance(
            maximum, (int, float)
        ) and maximum < target:
            errors.append("page_plan.max_pages cannot be less than target_pages")
        if page_plan.get("notes") is not None and not _nonempty(
            page_plan.get("notes")
        ):
            errors.append("page_plan.notes must be non-empty or null")

    matrix_by_id = {row["candidate_id"]: row for row in matrix["rows"]}
    selected = {
        row["candidate_id"]: row
        for row in selection["assignments"]
        if row["disposition"] == "SELECTED"
    }
    nonselected = set(matrix_by_id) - set(selected)
    primary: dict[str, list[str]] = defaultdict(list)
    supporting: dict[str, list[str]] = defaultdict(list)
    package_ids: list[str] = []
    drafting_orders: list[int] = []
    packages = architecture.get("packages")
    if not isinstance(packages, list) or not packages:
        errors.append("Issue Architecture requires at least one package")
        packages = []
    package_fields = {
        "package_id",
        "title",
        "purpose",
        "primary_candidate_ids",
        "supporting_candidate_ids",
        "must_cover_requirements",
        "boundaries",
        "drafting_order",
        "profile_extensions",
        "publication_extensions",
    }
    for index, package in enumerate(packages):
        prefix = f"packages[{index}]"
        if not isinstance(package, dict) or set(package) != package_fields:
            errors.append(f"{prefix} fields invalid")
            continue
        package_id = package.get("package_id")
        if _nonempty(package_id):
            package_ids.append(package_id)
        else:
            errors.append(f"{prefix}.package_id required")
        if not _nonempty(package.get("title")) or not _nonempty(
            package.get("purpose")
        ):
            errors.append(f"{prefix} title/purpose required")
        order = package.get("drafting_order")
        if isinstance(order, int) and not isinstance(order, bool) and order > 0:
            drafting_orders.append(order)
        else:
            errors.append(f"{prefix}.drafting_order invalid")
        for key in (
            "primary_candidate_ids",
            "supporting_candidate_ids",
            "must_cover_requirements",
            "boundaries",
        ):
            values = package.get(key)
            if not isinstance(values, list) or len(values) != len(
                set(values)
            ) or any(not _nonempty(value) for value in values):
                errors.append(f"{prefix}.{key} must be a unique string array")
        if not isinstance(package.get("profile_extensions"), dict) or not isinstance(
            package.get("publication_extensions"), dict
        ):
            errors.append(f"{prefix} extensions must be objects")
        primaries = (
            package.get("primary_candidate_ids")
            if isinstance(package.get("primary_candidate_ids"), list)
            else []
        )
        supports = (
            package.get("supporting_candidate_ids")
            if isinstance(package.get("supporting_candidate_ids"), list)
            else []
        )
        if set(primaries) & set(supports):
            errors.append(f"{prefix}: same candidate cannot be primary and supporting")
        placements = [(cid, "PRIMARY") for cid in primaries] + [
            (cid, "SUPPORTING") for cid in supports
        ]
        for cid, kind in placements:
            if cid in nonselected:
                errors.append(f"{prefix}: non-selected candidate used: {cid}")
                continue
            if cid not in selected:
                errors.append(f"{prefix}: unknown selected candidate: {cid}")
                continue
            if selected[cid]["architecture_usage"] != kind:
                errors.append(
                    f"{prefix}: {kind} placement conflicts with Selection usage for {cid}"
                )
                continue
            if kind == "PRIMARY":
                primary[cid].append(package_id or prefix)
            else:
                supporting[cid].append(package_id or prefix)
            boundary_set = set(package.get("boundaries") or [])
            missing = [
                value
                for value in matrix_by_id[cid]["remaining_boundaries"]
                if value not in boundary_set
            ]
            if missing:
                errors.append(
                    f"{prefix}: missing Evidence boundaries for {cid}: {missing}"
                )
    if len(package_ids) != len(set(package_ids)):
        errors.append("Issue Architecture package_id values must be unique")
    if len(drafting_orders) != len(set(drafting_orders)):
        errors.append("Issue Architecture drafting_order values must be unique")

    exception_by_id: dict[str, dict[str, Any]] = {}
    exceptions = architecture.get("selected_exceptions")
    if not isinstance(exceptions, list):
        errors.append("selected_exceptions must be an array")
        exceptions = []
    for item in exceptions:
        if not isinstance(item, dict) or set(item) != {
            "candidate_id",
            "reason",
            "exception_kind",
        }:
            errors.append("selected exception fields invalid")
            continue
        cid = item.get("candidate_id")
        if cid not in selected:
            errors.append(f"selected exception references non-selected candidate: {cid}")
            continue
        if cid in exception_by_id:
            errors.append(f"duplicate selected exception: {cid}")
        exception_by_id[cid] = item
        if not _nonempty(item.get("reason")):
            errors.append(f"selected exception requires reason: {cid}")
        if item.get("exception_kind") not in {
            "OMITTED_FROM_ARCHITECTURE",
            "DEFERRED",
            "STRUCTURAL_EXCEPTION",
        }:
            errors.append(f"selected exception kind invalid: {cid}")
        if primary.get(cid) or supporting.get(cid):
            errors.append(
                f"selected candidate cannot have placement and exception: {cid}"
            )
    for cid, assignment in selected.items():
        if cid in exception_by_id:
            continue
        if assignment["architecture_usage"] == "PRIMARY" and len(
            primary.get(cid, [])
        ) != 1:
            errors.append(
                f"selected PRIMARY candidate requires exactly one Architecture destination: {cid} count={len(primary.get(cid, []))}"
            )
        if assignment["architecture_usage"] == "SUPPORTING" and not supporting.get(
            cid
        ):
            errors.append(
                f"selected SUPPORTING candidate requires at least one Architecture destination: {cid}"
            )

    status = architecture.get("status")
    review = architecture.get("human_review")
    if status not in {"PROPOSED", "APPROVED"}:
        errors.append("Issue Architecture status invalid")
    if not isinstance(review, dict) or set(review) != {
        "reviewed_by",
        "reviewed_at",
        "review_reference",
    }:
        errors.append("Issue Architecture human_review fields invalid")
        review = {}
    if status == "APPROVED":
        for key in ("reviewed_by", "reviewed_at", "review_reference"):
            if not _nonempty(review.get(key)):
                errors.append(f"APPROVED Architecture requires human_review.{key}")
        if _nonempty(review.get("reviewed_at")) and not _aware_datetime(
            review["reviewed_at"]
        ):
            errors.append(
                "human_review.reviewed_at must be timezone-aware ISO-8601"
            )
    elif any(
        review.get(key) is not None
        for key in ("reviewed_by", "reviewed_at", "review_reference")
    ):
        errors.append(
            "PROPOSED Architecture must not contain completed Human Review metadata"
        )
    if require_approved and status != "APPROVED":
        errors.append("Issue Architecture must be APPROVED after Architecture Review")
    return errors


def _summarize_review_contents(
    repo_root: Path,
    upstream: dict[str, Any],
    matrix: dict[str, Any],
    selection: dict[str, Any],
    architecture: dict[str, Any],
    profile_path: Path,
    completeness_path: Path,
    ledger_path: Path,
    matrix_path: Path,
    selection_path: Path,
    architecture_path: Path,
    errors: list[str],
) -> dict[str, Any]:
    """Shared FULL review payload construction (existing algorithm, no duplication).

    Called by both ordinary public and checked-upstream paths. Receives actual
    required paths/basis and accumulated errors (ROOT §6.2 literal). Adds
    completeness INCOMPLETE check, preserves matrix equality, wrapper-specific
    architecture/empty-placement semantics and all normal schema/readiness
    checks via caller-passed errors. No second summary algorithm.
    """
    errs = list(errors)
    if upstream["completeness"]["overall_status"] == "INCOMPLETE":
        errs.append(
            "Profile Completeness is INCOMPLETE; Architecture Review is not ready"
        )
    matrix_by_id = {row["candidate_id"]: row for row in matrix.get("rows", [])}
    selection_by_id = {
        row["candidate_id"]: row
        for row in selection.get("assignments", [])
        if isinstance(row, dict) and row.get("candidate_id")
    }
    primary: dict[str, list[str]] = defaultdict(list)
    supporting: dict[str, list[str]] = defaultdict(list)
    for package in architecture.get("packages", []):
        if not isinstance(package, dict):
            continue
        package_id = package.get("package_id")
        for cid in package.get("primary_candidate_ids", []):
            primary[cid].append(package_id)
        for cid in package.get("supporting_candidate_ids", []):
            supporting[cid].append(package_id)
    exceptions = {
        row["candidate_id"]: row
        for row in architecture.get("selected_exceptions", [])
        if isinstance(row, dict) and row.get("candidate_id")
    }
    major: list[dict[str, Any]] = []
    for cid, row in sorted(matrix_by_id.items()):
        if row["materiality"] not in MATERIAL_REVIEW:
            continue
        assignment = selection_by_id.get(cid)
        disposition = assignment.get("disposition") if assignment else "INSPECT"
        if primary.get(cid):
            destination_kind = "PRIMARY"
            destinations = sorted(primary[cid])
            exception_reason = None
        elif supporting.get(cid):
            destination_kind = "SUPPORTING"
            destinations = sorted(supporting[cid])
            exception_reason = None
        elif cid in exceptions:
            destination_kind = "EXCEPTION"
            destinations = []
            exception_reason = exceptions[cid].get("reason")
        else:
            destination_kind = "NOT_SELECTED"
            destinations = []
            exception_reason = (
                assignment.get("rationale")
                if assignment
                else "Selection assignment missing"
            )
        major.append(
            {
                "candidate_id": cid,
                "title": row["title"],
                "materiality": row["materiality"],
                "selection_disposition": disposition,
                "destination_kind": destination_kind,
                "destinations": destinations,
                "exception_reason": exception_reason,
            }
        )
    obligations = upstream["completeness"]["obligations"]
    return {
        "schema_version": "2.0-rc1",
        "issue_id": upstream["profile"]["issue_id"],
        "research_profile": upstream["profile"]["research_profile"],
        "basis": {
            "architecture_sha256": core.sha256_file(architecture_path),
            "production_profile_sha256": core.sha256_file(profile_path),
            "profile_completeness_sha256": core.sha256_file(completeness_path),
            "materiality_ledger_sha256": core.sha256_file(ledger_path),
            "candidate_matrix_sha256": core.sha256_file(matrix_path),
            "candidate_selection_sha256": core.sha256_file(selection_path),
        },
        "readiness": {
            "status": "READY_FOR_ARCHITECTURE_REVIEW" if not errs else "BLOCKED",
            "errors": errs,
        },
        "discovery": {
            "total": len(upstream["discoveries"]),
            "counts": _counter(
                [row["provenance"]["origin"] for row in upstream["discoveries"]]
            ),
        },
        "research_expansion": _research_expansion_summary(upstream["discoveries"]),
        "screening": {
            "total": len(upstream["screening"]["decisions"]),
            "counts": _counter(
                [row["decision"] for row in upstream["screening"]["decisions"]]
            ),
        },
        "evidence": {
            "total": len(upstream["evidence"]["results"]),
            "counts": _counter(
                [row["status"] for row in upstream["evidence"]["results"]]
            ),
        },
        "materiality": {
            "total": len(upstream["ledger"]["rows"]),
            "counts": _counter(
                [row["downstream_disposition"] for row in upstream["ledger"]["rows"]]
            ),
        },
        "selection": {
            "total": len(selection.get("assignments", [])),
            "counts": _counter(
                [
                    row["disposition"]
                    for row in selection.get("assignments", [])
                    if isinstance(row, dict)
                    and row.get("disposition") in DISPOSITIONS
                ]
            ),
        },
        "completeness": {
            "overall_status": upstream["completeness"]["overall_status"],
            "obligation_counts": _counter([row["status"] for row in obligations]),
        },
        "major_material_destinations": major,
        "residual_limitations": list(
            upstream["completeness"]["residual_limitations"]
        ),
        "architecture": {
            "status": architecture.get("status"),
            "editorial_thesis": architecture.get("editorial_thesis"),
            "package_count": len(architecture.get("packages", [])),
            "packages": [
                row.get("title")
                for row in architecture.get("packages", [])
                if isinstance(row, dict) and _nonempty(row.get("title"))
            ],
            "page_plan": architecture.get("page_plan"),
        },
    }


def _build_architecture_review_summary_with_upstream(
    repo_root: Path,
    profile_path: Path,
    discovery_path: Path,
    screening_path: Path,
    evidence_path: Path,
    views_path: Path,
    ledger_path: Path,
    completeness_path: Path,
    matrix_path: Path,
    selection_path: Path,
    architecture_path: Path,
    upstream: dict[str, Any],
) -> dict[str, Any]:
    """Private checked-upstream summary (held upstream+paths only, no LIVE re-entry).

    Uses held upstream, loads matrix/selection/architecture JSONs, calls
    _validate_candidate_matrix_against_upstream (P-only, no second _load_upstream)
    + validate_selection + validate_architecture (wrapper-patched), then shared
    _summarize_review_contents. No implementation_sha, no _load_upstream.
    """
    matrix = core.load_json(matrix_path)
    selection = core.load_json(selection_path)
    architecture = core.load_json(architecture_path)
    errors = _validate_candidate_matrix_against_upstream(
        repo_root, matrix, upstream, profile_path, completeness_path, ledger_path, evidence_path, views_path
    )
    errors += validate_selection(
        repo_root,
        selection,
        profile_path,
        matrix_path,
        completeness_path,
        ledger_path,
    )
    errors += validate_architecture(
        repo_root,
        architecture,
        profile_path,
        completeness_path,
        ledger_path,
        matrix_path,
        selection_path,
    )
    return _summarize_review_contents(
        repo_root, upstream, matrix, selection, architecture,
        profile_path, completeness_path, ledger_path,
        matrix_path, selection_path, architecture_path, errors,
    )


def build_architecture_review_summary(
    repo_root: Path,
    profile_path: Path,
    discovery_path: Path,
    screening_path: Path,
    evidence_path: Path,
    views_path: Path,
    ledger_path: Path,
    completeness_path: Path,
    matrix_path: Path,
    selection_path: Path,
    architecture_path: Path,
    implementation_sha: str,
) -> dict[str, Any]:
    upstream = _load_upstream(
        repo_root,
        profile_path,
        discovery_path,
        screening_path,
        evidence_path,
        views_path,
        ledger_path,
        completeness_path,
        implementation_sha,
    )
    matrix = core.load_json(matrix_path)
    selection = core.load_json(selection_path)
    architecture = core.load_json(architecture_path)
    errors = validate_candidate_matrix(
        matrix,
        repo_root,
        profile_path,
        discovery_path,
        screening_path,
        evidence_path,
        views_path,
        ledger_path,
        completeness_path,
        implementation_sha,
    )
    errors += validate_selection(
        repo_root,
        selection,
        profile_path,
        matrix_path,
        completeness_path,
        ledger_path,
    )
    errors += validate_architecture(
        repo_root,
        architecture,
        profile_path,
        completeness_path,
        ledger_path,
        matrix_path,
        selection_path,
    )
    return _summarize_review_contents(
        repo_root, upstream, matrix, selection, architecture,
        profile_path, completeness_path, ledger_path,
        matrix_path, selection_path, architecture_path, errors,
    )


def _path(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--implementation-sha")
    subparsers = parser.add_subparsers(dest="command", required=True)

    matrix = subparsers.add_parser("matrix")
    for key in (
        "profile",
        "discovery",
        "screening",
        "evidence",
        "views",
        "ledger",
        "completeness",
        "output",
    ):
        matrix.add_argument(f"--{key}", required=True)

    selection = subparsers.add_parser("selection-check")
    for key in ("selection", "profile", "matrix", "completeness", "ledger"):
        selection.add_argument(f"--{key}", required=True)

    architecture = subparsers.add_parser("architecture-check")
    for key in (
        "architecture",
        "profile",
        "completeness",
        "ledger",
        "matrix",
        "selection",
    ):
        architecture.add_argument(f"--{key}", required=True)
    architecture.add_argument("--require-approved", action="store_true")

    review = subparsers.add_parser("review-summary")
    for key in (
        "profile",
        "discovery",
        "screening",
        "evidence",
        "views",
        "ledger",
        "completeness",
        "matrix",
        "selection",
        "architecture",
        "output",
    ):
        review.add_argument(f"--{key}", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = Path(args.repo_root).resolve()
    implementation_sha = core.repository_commit_sha(
        repo_root, args.implementation_sha
    )
    try:
        if args.command == "matrix":
            payload = derive_candidate_matrix(
                repo_root,
                _path(repo_root, args.profile),
                _path(repo_root, args.discovery),
                _path(repo_root, args.screening),
                _path(repo_root, args.evidence),
                _path(repo_root, args.views),
                _path(repo_root, args.ledger),
                _path(repo_root, args.completeness),
                implementation_sha,
            )
            output = _path(repo_root, args.output)
            write_candidate_matrix(output, payload)
            print(output)
            return 0
        if args.command == "selection-check":
            errors = validate_selection(
                repo_root,
                core.load_json(_path(repo_root, args.selection)),
                _path(repo_root, args.profile),
                _path(repo_root, args.matrix),
                _path(repo_root, args.completeness),
                _path(repo_root, args.ledger),
            )
            print(
                json.dumps(
                    {"passed": not errors, "errors": errors},
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0 if not errors else 1
        if args.command == "architecture-check":
            errors = validate_architecture(
                repo_root,
                core.load_json(_path(repo_root, args.architecture)),
                _path(repo_root, args.profile),
                _path(repo_root, args.completeness),
                _path(repo_root, args.ledger),
                _path(repo_root, args.matrix),
                _path(repo_root, args.selection),
                args.require_approved,
            )
            print(
                json.dumps(
                    {"passed": not errors, "errors": errors},
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0 if not errors else 1
        if args.command == "review-summary":
            payload = build_architecture_review_summary(
                repo_root,
                _path(repo_root, args.profile),
                _path(repo_root, args.discovery),
                _path(repo_root, args.screening),
                _path(repo_root, args.evidence),
                _path(repo_root, args.views),
                _path(repo_root, args.ledger),
                _path(repo_root, args.completeness),
                _path(repo_root, args.matrix),
                _path(repo_root, args.selection),
                _path(repo_root, args.architecture),
                implementation_sha,
            )
            output = _path(repo_root, args.output)
            if output.exists():
                raise ValueError(
                    f"refusing to overwrite Architecture Review Summary: {output}"
                )
            core.write_json(output, payload)
            print(output)
            return (
                0
                if payload["readiness"]["status"]
                == "READY_FOR_ARCHITECTURE_REVIEW"
                else 1
            )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
