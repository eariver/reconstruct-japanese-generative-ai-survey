#!/usr/bin/env python3
"""Factual Evidence, Edition Views, Materiality and Completeness for Core v2.

WU-007 keeps reusable facts separate from edition significance and fail-closes
on two historical defect families:
- #166: every Discovery record must retain an explicit downstream disposition;
- #191: every factual statement/value must bind an explicit entity and role.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Any

from scripts import survey_production_v2 as core
from scripts import survey_schema_v2 as schema_gate
from scripts import survey_screening_v2 as screening

PROMPT_PATH = Path("config/prompts/evidence-verification-v2.md")
PACKAGE_SCHEMA = Path("schemas/evidence-v2-run-package.schema.json")
TASK_SCHEMA = Path("schemas/evidence-v2-task.schema.json")
CARD_SCHEMA = Path("schemas/evidence-v2-card.schema.json")
VIEW_SCHEMA = Path("schemas/edition-evidence-view.schema.json")
SUPPLEMENT_SCHEMA = Path("schemas/evidence-authority-supplement-v2.schema.json")
LEDGER_SCHEMA = Path("schemas/materiality-ledger.schema.json")
COMPLETENESS_SCHEMA = Path("schemas/profile-completeness-result.schema.json")

CARD_KEYS = {
    "schema_version", "issue_id", "evidence_task_id", "basis", "status",
    "entities", "artifact", "temporal", "sources", "claims", "metrics",
    "limitations", "verification",
}
EVIDENCE_CLASSES = {
    "PRIMARY_FACT", "VENDOR_CLAIM", "PROJECT_CLAIM", "AUTHOR_CLAIM",
    "SOCIAL_OBSERVATION", "INFERENCE",
}
SUBJECT_ROLES = {"PRIMARY_SUBJECT", "COMPARATOR", "RELATED"}
VIEW_MATERIALITY = {"MATERIAL", "CONTEXT", "NON_MATERIAL", "HOLD"}
OBLIGATION_STATUS = {"SATISFIED", "LIMITATION", "NEEDS_RESEARCH", "NOT_APPLICABLE"}
SOURCE_CLASS_MAP = {
    "PRIMARY_OFFICIAL": "PRIMARY_OFFICIAL",
    "PRIMARY_PAPER": "PRIMARY_PAPER",
    "PRIMARY_REPOSITORY": "PRIMARY_REPOSITORY",
    "SOCIAL": "SOCIAL",
    "SECONDARY": "SECONDARY",
    "SECONDARY_INVESTOR_ACCOUNT": "SECONDARY",
    "paper": "PRIMARY_PAPER",
    "github-release": "PRIMARY_REPOSITORY",
    "official-feed-item": "PRIMARY_OFFICIAL",
    "official-index": "PRIMARY_OFFICIAL",
    "first_party_release_or_docs": "PRIMARY_OFFICIAL",
    "first_party_official": "PRIMARY_OFFICIAL",
    "government_security_authority": "PRIMARY_OFFICIAL",
    "vendor_technical": "PRIMARY_OFFICIAL",
    "repository_release": "PRIMARY_REPOSITORY",
    "arxiv_primary": "PRIMARY_PAPER",
    "dailyx_x_observation": "SOCIAL",
    "github_release_api_response": "PRIMARY_REPOSITORY",
    "official_project_repo": "PRIMARY_REPOSITORY",
    "official_publisher_page": "PRIMARY_OFFICIAL",
    "sol_working_set_observation": "SECONDARY",
    # These values are part of the existing Weekly fixtures.  They are
    # deliberately classified by their established provenance, rather than
    # by words appearing in the value itself.
    "github-changelog": "PRIMARY_OFFICIAL",
    "github-repository": "PRIMARY_REPOSITORY",
    "official-index-snapshot": "PRIMARY_OFFICIAL",
    "official-page": "PRIMARY_OFFICIAL",
    "prior-week-authority": "SECONDARY",
    "x-community-signal": "SOCIAL",
    # W34's Discovery vocabulary includes these edition-local observations.
    "carryover_recheck": "SECONDARY",
    "grok_x_observation_corrected_r2": "SOCIAL",
    "sol_discovery_working_record": "SECONDARY",
    # W34 fresh gap-fill Discovery collectors (accepted canonical Discovery).
    # Added 2026-09-09 after edition-found fail-closed gap blocked fresh
    # Evidence (see sources/2026-W34/execution/luna/
    # w34-screening-evidence-after-sol-discovery-r2/defects/
    # shared-core-evidence-source-map-gap.md). Classes mirror siblings.
    "arxiv_atom_snapshot": "PRIMARY_PAPER",
    "official_web_fallback_observation": "PRIMARY_OFFICIAL",
    "official_release_notes_snapshot": "PRIMARY_OFFICIAL",
    "official_rss_index_snapshot": "PRIMARY_OFFICIAL",
    "official_research_index_snapshot": "PRIMARY_OFFICIAL",
    # Exact source_type values used by the W34 post-Screening supplement.
    "first_party_product_release": "PRIMARY_OFFICIAL",
    "first_party_product_changelog": "PRIMARY_OFFICIAL",
    "first_party_product_docs": "PRIMARY_OFFICIAL",
    "first_party_repository": "PRIMARY_REPOSITORY",
    "primary_research_record": "PRIMARY_PAPER",
    "primary_research_pdf": "PRIMARY_PAPER",
    "first_party_announcement": "PRIMARY_OFFICIAL",
    "first_party_research_publication": "PRIMARY_PAPER",
    "first_party_vendor_blog": "PRIMARY_OFFICIAL",
    "first_party_product_release_notes": "PRIMARY_OFFICIAL",
    "first_party_product_announcement": "PRIMARY_OFFICIAL",
    "first_party_safety_publication": "PRIMARY_OFFICIAL",
    "first_party_product_safety_publication": "PRIMARY_OFFICIAL",
    "first_party_technical_example": "PRIMARY_OFFICIAL",
    "vendor_technical_blog": "PRIMARY_OFFICIAL",
    "official_conference_paper": "PRIMARY_PAPER",
    "vulnerability_authority_api": "PRIMARY_OFFICIAL",
    "industry_rights_authority": "PRIMARY_OFFICIAL",
    "government_security_mirror": "PRIMARY_OFFICIAL",
}


def _rel(repo_root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(repo_root.resolve()))


def _repo_file(repo_root: Path, relative: str, label: str) -> Path:
    if not isinstance(relative, str) or not relative:
        raise ValueError(f"{label} path missing")
    if Path(relative).is_absolute() or "\\" in relative or ".." in Path(relative).parts:
        raise ValueError(f"{label} must be a repository-relative path without traversal")
    root = repo_root.resolve()
    candidate = root / relative
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository root: {relative}") from exc
    current = root
    for part in Path(relative).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"{label} may not traverse symlinked path: {relative}")
    path = candidate.resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository root") from exc
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"{label} missing or symlinked: {relative}")
    return path


def _repo_output_path(repo_root: Path, relative: str, label: str) -> Path:
    """Validate a repository-local output path without requiring it to exist."""
    if not isinstance(relative, str) or not relative:
        raise ValueError(f"{label} path missing")
    if Path(relative).is_absolute() or "\\" in relative or ".." in Path(relative).parts:
        raise ValueError(f"{label} must be a repository-relative path without traversal")
    root = repo_root.resolve()
    candidate = root / relative
    current = root
    for part in Path(relative).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"{label} may not traverse symlinked path: {relative}")
    path = candidate.resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository root") from exc
    if candidate.exists() and not candidate.is_file():
        raise ValueError(f"{label} is not a regular file: {relative}")
    return path


def _raw_repo_relative(repo_root: Path, path: Path, label: str) -> str:
    """Return a non-resolved repository-relative path for symlink checks."""
    root = repo_root.resolve()
    candidate = path if path.is_absolute() else root / path
    raw = Path(os.path.abspath(str(candidate)))
    try:
        relative = raw.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} must be repository-local: {path}") from exc
    return relative.as_posix()


def _source_class(source_type: Any) -> str:
    value = SOURCE_CLASS_MAP.get(source_type)
    if value is not None:
        return value
    if not isinstance(source_type, str) or not source_type.strip():
        raise ValueError(f"unsupported source_type for Evidence authority: {source_type!r}")
    raise ValueError(f"unsupported source_type for Evidence authority: {source_type!r}")


def _supplement_source_file(repo_root: Path, raw_path: Any, source_root: Path) -> Path:
    if not isinstance(raw_path, str) or not raw_path:
        raise ValueError("Evidence Authority Supplement raw_path is required")
    root = repo_root.resolve()
    if Path(raw_path).is_absolute() or "\\" in raw_path or ".." in Path(raw_path).parts:
        raise ValueError("Evidence Authority Supplement raw_path must be repository-relative without traversal")
    candidate = root / raw_path
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError("Evidence Authority Supplement raw_path escapes repository") from exc
    current = root
    for part in Path(raw_path).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"Evidence Authority Supplement raw_path traverses symlink: {raw_path}")
    path = core.repo_local_path(repo_root, raw_path, "Evidence Authority Supplement raw_path")
    try:
        path.relative_to(source_root.resolve())
    except ValueError as exc:
        raise ValueError("Evidence Authority Supplement raw_path crosses issue source_root") from exc
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Evidence Authority Supplement Raw file missing or unsafe: {raw_path}")
    return path


def validate_evidence_authority_supplement(
    repo_root: Path,
    supplement_path: Path,
    implementation_sha: str | None = None,
    *,
    expected_issue_id: str | None = None,
    expected_source_root: Path | None = None,
    expected_discovery_path: Path | None = None,
    expected_screening_acceptance_path: Path | None = None,
    screening_acceptance: dict[str, Any] | None = None,
    discoveries: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Validate an additive, post-Screening authority manifest and its Raw bytes.

    A supplement is deliberately narrower than Discovery: every row must point
    at an existing non-DROP Discovery task, and every factual source remains
    explicitly task-bound in the Evidence package before a Card can cite it.
    """
    supplement_path = _repo_file(
        repo_root,
        _raw_repo_relative(repo_root, supplement_path, "Evidence Authority Supplement"),
        "Evidence Authority Supplement",
    )
    manifest = schema_gate.load_and_validate_json(
        supplement_path,
        repo_root / SUPPLEMENT_SCHEMA,
        label="Evidence Authority Supplement",
    )
    if expected_issue_id is not None and manifest["issue_id"] != expected_issue_id:
        raise ValueError("Evidence Authority Supplement issue identity mismatch")
    basis = manifest["basis"]
    source_root = core.repo_local_path(repo_root, basis["source_root"], "Evidence supplement source_root")
    if not source_root.is_dir():
        raise ValueError("Evidence supplement source_root is missing")
    if expected_source_root is not None and source_root.resolve() != expected_source_root.resolve():
        raise ValueError("Evidence Authority Supplement source_root mismatch")

    discovery_path = _repo_file(repo_root, basis["discovery_path"], "Evidence supplement Discovery")
    screening_path = _repo_file(repo_root, basis["screening_acceptance_path"], "Evidence supplement Screening acceptance")
    if core.sha256_file(discovery_path) != basis["discovery_sha256"]:
        raise ValueError("Evidence Authority Supplement Discovery SHA drift")
    if core.sha256_file(screening_path) != basis["screening_acceptance_sha256"]:
        raise ValueError("Evidence Authority Supplement Screening acceptance SHA drift")
    if expected_discovery_path is not None and discovery_path.resolve() != expected_discovery_path.resolve():
        raise ValueError("Evidence Authority Supplement Discovery path mismatch")
    if expected_screening_acceptance_path is not None and screening_path.resolve() != expected_screening_acceptance_path.resolve():
        raise ValueError("Evidence Authority Supplement Screening acceptance path mismatch")

    if screening_acceptance is None or discoveries is None:
        if implementation_sha is not None:
            screening_acceptance, _, discoveries = validate_screening_acceptance(
                repo_root,
                screening_path,
                discovery_path,
                manifest["issue_id"],
                implementation_sha,
            )
        else:
            screening_acceptance = core.load_json(screening_path)
            discoveries = screening.read_jsonl(discovery_path)
    if not isinstance(screening_acceptance, dict) or screening_acceptance.get("issue_id") != manifest["issue_id"]:
        raise ValueError("Evidence Authority Supplement Screening issue identity mismatch")
    if not isinstance(discoveries, list) or any(
        not isinstance(row, dict) or row.get("issue_id") != manifest["issue_id"]
        for row in discoveries
    ):
        raise ValueError("Evidence Authority Supplement Discovery issue identity mismatch")
    discovery_ids = {row.get("discovery_id") for row in discoveries if isinstance(row, dict)}
    decisions = {
        row.get("discovery_id"): row.get("decision")
        for row in (screening_acceptance or {}).get("decisions", [])
        if isinstance(row, dict)
    }

    seen_ids: set[str] = set()
    seen_bindings: set[tuple[str, str]] = set()
    for index, entry in enumerate(manifest["sources"]):
        prefix = f"Evidence Authority Supplement sources[{index}]"
        source_id = entry["supplement_source_id"]
        if source_id in seen_ids:
            raise ValueError(f"duplicate Evidence Authority Supplement source ID: {source_id}")
        seen_ids.add(source_id)
        discovery_id = entry["discovery_id"]
        task_id = entry["evidence_task_id"]
        if discovery_id not in discovery_ids:
            raise ValueError(f"{prefix} references unknown Discovery ID: {discovery_id}")
        if discovery_id not in decisions:
            raise ValueError(f"{prefix} references a Discovery without a Screening decision: {discovery_id}")
        if decisions.get(discovery_id) == "DROP":
            raise ValueError(f"{prefix} may not target a DROP Discovery task: {discovery_id}")
        if task_id != stable_task_id(manifest["issue_id"], discovery_id):
            raise ValueError(f"{prefix} Evidence task identity does not match Discovery ID")
        if entry["source_class"] != _source_class(entry["source_type"]):
            raise ValueError(f"{prefix} source_class does not match source_type")
        binding = (task_id, entry["locator"])
        if binding in seen_bindings:
            raise ValueError(f"duplicate/ambiguous Evidence Authority Supplement binding: {binding}")
        seen_bindings.add(binding)
        try:
            core.parse_instant(entry["accessed_at"])
            if entry["published_at"] is not None:
                core.parse_instant(entry["published_at"])
        except (KeyError, ValueError) as exc:
            raise ValueError(f"{prefix} timestamp invalid") from exc
        raw = _supplement_source_file(repo_root, entry["raw_path"], source_root)
        actual_byte_count = raw.stat().st_size
        if actual_byte_count < 1:
            raise ValueError(f"{prefix} Raw body must be non-empty: {entry['raw_path']}")
        if actual_byte_count != entry["byte_count"]:
            raise ValueError(f"{prefix} byte_count drift: {entry['raw_path']}")
        if core.sha256_file(raw) != entry["raw_sha256"]:
            raise ValueError(f"{prefix} Raw SHA drift: {entry['raw_path']}")
    return manifest


def build_evidence_authority_supplement(
    repo_root: Path,
    issue_id: str,
    source_root: Path,
    discovery_path: Path,
    screening_acceptance_path: Path,
    sources: list[dict[str, Any]],
    output_path: Path,
    *,
    supplement_id: str,
    implementation_sha: str | None = None,
) -> Path:
    """Materialize and validate an edition-local authority supplement manifest."""
    output_rel = _raw_repo_relative(repo_root, output_path, "Evidence Authority Supplement output")
    output_path = _repo_output_path(repo_root, output_rel, "Evidence Authority Supplement output")
    if output_path.exists():
        raise ValueError(f"refusing to overwrite Evidence Authority Supplement: {output_path}")
    payload = {
        "schema_version": "2.0-rc1",
        "supplement_id": supplement_id,
        "issue_id": issue_id,
        "basis": {
            "source_root": _rel(repo_root, source_root),
            "discovery_path": _rel(repo_root, discovery_path),
            "discovery_sha256": core.sha256_file(discovery_path),
            "screening_acceptance_path": _rel(repo_root, screening_acceptance_path),
            "screening_acceptance_sha256": core.sha256_file(screening_acceptance_path),
        },
        "sources": sources,
    }
    schema_gate.validate_instance(
        payload,
        repo_root / SUPPLEMENT_SCHEMA,
        label="Evidence Authority Supplement",
    )
    core.write_json(output_path, payload)
    try:
        validate_evidence_authority_supplement(
            repo_root,
            output_path,
            implementation_sha,
            expected_issue_id=issue_id,
            expected_source_root=source_root,
            expected_discovery_path=discovery_path,
            expected_screening_acceptance_path=screening_acceptance_path,
        )
    except Exception:
        output_path.unlink(missing_ok=True)
        raise
    return output_path


def _supplement_entries_for_package(
    repo_root: Path,
    package: dict[str, Any],
    *,
    implementation_sha: str | None = None,
    screening_acceptance: dict[str, Any] | None = None,
    discoveries: list[dict[str, Any]] | None = None,
) -> dict[str, dict[str, Any]]:
    authority = package.get("authority_supplement")
    if authority is None:
        return {}
    if not isinstance(authority, dict) or set(authority) != {"path", "sha256"}:
        raise ValueError("Evidence package authority_supplement fields invalid")
    path = _repo_file(repo_root, authority["path"], "Evidence Authority Supplement manifest")
    if core.sha256_file(path) != authority["sha256"]:
        raise ValueError("Evidence Authority Supplement manifest SHA drift")
    manifest = validate_evidence_authority_supplement(
        repo_root,
        path,
        implementation_sha,
        expected_issue_id=package["issue_id"],
        expected_discovery_path=repo_root / package["basis"]["discovery_path"],
        expected_screening_acceptance_path=repo_root / package["basis"]["screening_acceptance_path"],
        screening_acceptance=screening_acceptance,
        discoveries=discoveries,
    )
    result: dict[str, dict[str, Any]] = {}
    for entry in manifest["sources"]:
        if entry["supplement_source_id"] in result:
            raise ValueError("Evidence Authority Supplement source IDs are ambiguous")
        result[entry["supplement_source_id"]] = entry
    return result


def task_authority_sources(
    repo_root: Path,
    task: dict[str, Any],
    package: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Return only exact Discovery/supplement sources explicitly bound to *task*."""
    result: dict[str, dict[str, Any]] = {}
    for index, source in enumerate(task.get("source_records", []), start=1):
        result[f"src-{index}"] = {
            "url": source.get("locator"),
            "source_class": _source_class(source.get("source_type")),
            "title": source.get("title") or source.get("locator"),
            "published_at": source.get("published_at"),
            "accessed_at": None,
            "role": "Discovery-bounded source used for factual verification",
            "supplement": False,
        }
    supplement_ids = task.get("authority_supplement_source_ids", [])
    if supplement_ids:
        entries = _supplement_entries_for_package(repo_root, package)
        for source_id in supplement_ids:
            entry = entries.get(source_id)
            if entry is None:
                raise ValueError(f"Evidence Task references unbound supplement source: {source_id}")
            result[source_id] = {
                "url": entry["locator"],
                "source_class": entry["source_class"],
                "title": entry["title"],
                "published_at": entry["published_at"],
                "accessed_at": entry["accessed_at"],
                "role": f"Post-Screening exact authority supplement: {entry['relation']}",
                "supplement": True,
            }
    return result


def _exact_regular_files(directory: Path, expected: set[str], label: str) -> dict[str, Path]:
    if not directory.is_dir():
        raise ValueError(f"{label} directory missing: {directory}")
    entries = list(directory.iterdir())
    if any(path.is_symlink() for path in entries):
        raise ValueError(f"{label} may not contain symlinks")
    non_files = sorted(path.name for path in entries if not path.is_file())
    if non_files:
        raise ValueError(f"{label} may contain files only: {non_files}")
    actual = {path.name for path in entries}
    if actual != expected:
        raise ValueError(
            f"{label} must be complete and exact: "
            f"missing={sorted(expected-actual)} extra={sorted(actual-expected)}"
        )
    return {path.name: path for path in entries}


def stable_task_id(issue_id: str, discovery_id: str) -> str:
    digest = hashlib.sha256(discovery_id.encode("utf-8")).hexdigest()[:16]
    return f"evidence:{issue_id}:{digest}"


def task_filename(task_id: str) -> str:
    digest = hashlib.sha256(task_id.encode("utf-8")).hexdigest()[:20]
    return f"task-{digest}.json"


def view_filename(task_id: str) -> str:
    digest = hashlib.sha256(task_id.encode("utf-8")).hexdigest()[:20]
    return f"view-{digest}.json"


def _screening_acceptance_digest(acceptance: dict[str, Any]) -> str:
    return core.sha256_object({
        "package_sha256": acceptance["package_sha256"],
        "batches": acceptance["batches"],
        "decisions": acceptance["decisions"],
    })


def validate_screening_acceptance(
    repo_root: Path,
    screening_acceptance_path: Path,
    discovery_path: Path,
    issue_id: str,
    implementation_sha: str,
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    acceptance = core.load_json(screening_acceptance_path)
    expected_keys = {
        "schema_version", "issue_id", "research_profile", "result_set_sha256",
        "package_sha256", "record_count", "batch_count", "batches", "decisions",
    }
    if set(acceptance) != expected_keys:
        raise ValueError("Screening acceptance fields invalid")
    if acceptance["schema_version"] != "2.0-rc1" or acceptance["issue_id"] != issue_id:
        raise ValueError("Screening acceptance identity mismatch")
    digest = _screening_acceptance_digest(acceptance)
    if acceptance["result_set_sha256"] != digest or screening_acceptance_path.parent.name != digest:
        raise ValueError("Screening acceptance content-addressed identity mismatch")

    package_path = screening_acceptance_path.parent / "package.json"
    if not package_path.is_file() or core.sha256_file(package_path) != acceptance["package_sha256"]:
        raise ValueError("accepted Screening package copy is missing or changed")
    package = core.load_json(package_path)
    screening.validate_package_basis(repo_root, package_path, package, implementation_sha)
    if package["issue_id"] != issue_id or package["research_profile"] != acceptance["research_profile"]:
        raise ValueError("Screening package/acceptance profile identity mismatch")

    effective = screening.resolve_effective_discovery_basis(
        repo_root, package_path, implementation_sha
    )
    expected_discovery = effective["path"].resolve()
    if expected_discovery != discovery_path.resolve():
        raise ValueError("Screening acceptance points at a different Discovery set")
    if core.sha256_file(discovery_path) != effective["sha256"]:
        raise ValueError("Screening acceptance Discovery bytes changed")
    discoveries = effective["records"]
    expected_ids = {row["discovery_id"] for row in discoveries}
    decisions = acceptance["decisions"]
    if not isinstance(decisions, list):
        raise ValueError("Screening acceptance decisions missing")
    actual_ids = [row.get("discovery_id") for row in decisions if isinstance(row, dict)]
    if len(actual_ids) != len(decisions) or len(actual_ids) != len(set(actual_ids)) or set(actual_ids) != expected_ids:
        raise ValueError("Screening acceptance does not cover Discovery set exactly")
    if acceptance["record_count"] != len(discoveries) or acceptance["batch_count"] != len(acceptance["batches"]):
        raise ValueError("Screening acceptance counts are inconsistent")
    return acceptance, package, discoveries


def prepare_evidence_package(
    repo_root: Path,
    state_path: Path,
    discovery_path: Path,
    screening_acceptance_path: Path,
    output_dir: Path,
    implementation_sha: str,
    supplement_manifest_path: Path | None = None,
) -> Path:
    cfg = core.load_json(repo_root / core.DEFAULT_CONFIG)
    state = core.load_json(state_path)
    core.verify_state_basis(repo_root, cfg, state, implementation_sha)
    issue_id = state["issue_id"]
    profile_path = _repo_file(repo_root, state["profile"]["path"], "Production Profile")
    profile = core.load_json(profile_path)
    acceptance, screening_package, discoveries = validate_screening_acceptance(
        repo_root, screening_acceptance_path, discovery_path, issue_id, implementation_sha
    )
    if (repo_root / screening_package["basis"]["state_path"]).resolve() != state_path.resolve():
        raise ValueError("Screening acceptance was produced from a different Production State")
    discovery_map = {row["discovery_id"]: row for row in discoveries}
    decisions = {row["discovery_id"]: row for row in acceptance["decisions"]}
    supplement_entries: dict[str, dict[str, Any]] = {}
    supplement_authority: dict[str, str] | None = None
    if supplement_manifest_path is not None:
        supplement_manifest_path = _repo_file(
            repo_root,
            _raw_repo_relative(repo_root, supplement_manifest_path, "Evidence Authority Supplement manifest"),
            "Evidence Authority Supplement manifest",
        )
        manifest = validate_evidence_authority_supplement(
            repo_root,
            supplement_manifest_path,
            implementation_sha,
            expected_issue_id=issue_id,
            expected_source_root=core.repo_local_path(
                repo_root, profile["paths"]["source_root"], "paths.source_root"
            ),
            expected_discovery_path=discovery_path,
            expected_screening_acceptance_path=screening_acceptance_path,
            screening_acceptance=acceptance,
            discoveries=discoveries,
        )
        supplement_entries = {
            entry["supplement_source_id"]: entry for entry in manifest["sources"]
        }
        supplement_authority = {
            "path": _rel(repo_root, supplement_manifest_path),
            "sha256": core.sha256_file(supplement_manifest_path),
        }

    required_contracts = (PROMPT_PATH, PACKAGE_SCHEMA, TASK_SCHEMA, CARD_SCHEMA)
    if supplement_manifest_path is not None:
        required_contracts = (*required_contracts, SUPPLEMENT_SCHEMA)
    for required in required_contracts:
        _repo_file(repo_root, str(required), f"Evidence v2 contract {required.name}")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError(f"refusing to overwrite non-empty Evidence package directory: {output_dir}")
    task_dir = output_dir / "tasks"
    task_dir.mkdir(parents=True, exist_ok=True)
    tasks_meta: list[dict[str, Any]] = []

    for discovery_id in sorted(discovery_map):
        decision = decisions[discovery_id]
        if decision["decision"] == "DROP":
            continue
        task_id = stable_task_id(issue_id, discovery_id)
        task = {
            "schema_version": "2.0-rc1",
            "issue_id": issue_id,
            "evidence_task_id": task_id,
            "discovery_ids": [discovery_id],
            "source_records": [discovery_map[discovery_id]["source"]],
            "verification_targets": list(decision["verification_targets"]),
            "screening_basis": {
                "screening_acceptance_sha256": core.sha256_file(screening_acceptance_path),
                "decisions": [{
                    "discovery_id": discovery_id,
                    "decision": decision["decision"],
                    "scope_tags": list(decision["scope_tags"]),
                }],
            },
        }
        task_supplement_ids = sorted(
            source_id
            for source_id, entry in supplement_entries.items()
            if entry["evidence_task_id"] == task_id
        )
        if task_supplement_ids:
            task["authority_supplement_source_ids"] = task_supplement_ids
        filename = task_filename(task_id)
        path = task_dir / filename
        core.write_json(path, task)
        tasks_meta.append({
            "evidence_task_id": task_id,
            "path": f"tasks/{filename}",
            "sha256": core.sha256_file(path),
            "discovery_ids": [discovery_id],
            **({"authority_supplement_source_ids": task_supplement_ids} if task_supplement_ids else {}),
        })

    package = {
        "schema_version": "2.0-rc1",
        "issue_id": issue_id,
        "research_profile": profile["research_profile"],
        "basis": {
            "profile_path": _rel(repo_root, profile_path),
            "profile_sha256": core.sha256_file(profile_path),
            "state_path": _rel(repo_root, state_path),
            "state_sha256": core.sha256_file(state_path),
            "discovery_path": _rel(repo_root, discovery_path),
            "discovery_sha256": core.sha256_file(discovery_path),
            "screening_acceptance_path": _rel(repo_root, screening_acceptance_path),
            "screening_acceptance_sha256": core.sha256_file(screening_acceptance_path),
        },
        "prompt": {"path": str(PROMPT_PATH), "sha256": core.sha256_file(repo_root / PROMPT_PATH)},
        "contracts": {
            "run_package": {"path": str(PACKAGE_SCHEMA), "sha256": core.sha256_file(repo_root / PACKAGE_SCHEMA)},
            "task": {"path": str(TASK_SCHEMA), "sha256": core.sha256_file(repo_root / TASK_SCHEMA)},
            "card": {"path": str(CARD_SCHEMA), "sha256": core.sha256_file(repo_root / CARD_SCHEMA)},
        },
        "tasks": tasks_meta,
        "expected_outputs": {"one_result_per_task": True, "filename_rule": "same-basename-as-task"},
        "rules": [
            "Factual Evidence contains no Weekly why_now, Thematic lineage role, or Candidate Selection recommendation.",
            "Every event/claim/metric/limitation binds an explicit subject entity and subject role.",
            "Comparator-owned facts remain bound to comparator entities.",
            "Evidence sources must be represented by the task's Discovery source records or an exact validated Evidence Authority Supplement.",
            "Only a complete exact one-result-per-task set may be accepted.",
        ],
    }
    if supplement_authority is not None:
        package["authority_supplement"] = supplement_authority
        package["contracts"]["supplement"] = {
            "path": str(SUPPLEMENT_SCHEMA),
            "sha256": core.sha256_file(repo_root / SUPPLEMENT_SCHEMA),
        }
        package["rules"].append(
            "Post-Screening authority is eligible only through an exact validated Evidence Authority Supplement source ID bound to this task."
        )
    package_path = output_dir / "package.json"
    core.write_json(package_path, package)
    return package_path


def _validate_task(task: dict[str, Any], meta: dict[str, Any], acceptance_sha: str) -> list[str]:
    errors: list[str] = []
    required_keys = {
        "schema_version", "issue_id", "evidence_task_id", "discovery_ids",
        "source_records", "verification_targets", "screening_basis",
    }
    optional_keys = {"authority_supplement_source_ids"}
    if set(task) - required_keys - optional_keys or not required_keys.issubset(task):
        return ["Evidence Task fields invalid"]
    if task["schema_version"] != "2.0-rc1" or task["evidence_task_id"] != meta["evidence_task_id"]:
        errors.append("Evidence Task identity mismatch")
    if task["discovery_ids"] != meta["discovery_ids"] or len(task["discovery_ids"]) != 1:
        errors.append("WU-007 Evidence Task must bind exactly its declared Discovery ID")
    if not isinstance(task["source_records"], list) or len(task["source_records"]) != len(task["discovery_ids"]):
        errors.append("Evidence Task source_records must match Discovery cardinality")
    supplement_ids = task.get("authority_supplement_source_ids")
    if supplement_ids is not None:
        if (
            not isinstance(supplement_ids, list)
            or len(supplement_ids) != len(set(supplement_ids))
            or any(not isinstance(value, str) or not value for value in supplement_ids)
        ):
            errors.append("Evidence Task authority_supplement_source_ids must be unique strings")
    screening_basis = task.get("screening_basis")
    if not isinstance(screening_basis, dict) or screening_basis.get("screening_acceptance_sha256") != acceptance_sha:
        errors.append("Evidence Task Screening basis mismatch")
    else:
        decisions = screening_basis.get("decisions")
        if not isinstance(decisions, list) or len(decisions) != 1:
            errors.append("Evidence Task must carry exactly one Screening decision")
        elif decisions[0].get("discovery_id") != task["discovery_ids"][0] or decisions[0].get("decision") not in {"KEEP", "MAYBE", "INSPECT"}:
            errors.append("Evidence Task carries invalid Screening decision")
    return errors


def validate_evidence_package_basis(
    repo_root: Path,
    package_path: Path,
    package: dict[str, Any],
    implementation_sha: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    required_keys = {
        "schema_version", "issue_id", "research_profile", "basis", "prompt",
        "contracts", "tasks", "expected_outputs", "rules",
    }
    if set(package) - required_keys - {"authority_supplement"} or not required_keys.issubset(package) or package.get("schema_version") != "2.0-rc1":
        raise ValueError("Evidence package fields/schema_version invalid")
    cfg = core.load_json(repo_root / core.DEFAULT_CONFIG)
    basis = package["basis"]
    for path_key, sha_key in (
        ("profile_path", "profile_sha256"),
        ("state_path", "state_sha256"),
        ("discovery_path", "discovery_sha256"),
        ("screening_acceptance_path", "screening_acceptance_sha256"),
    ):
        path = _repo_file(repo_root, basis[path_key], f"Evidence basis {path_key}")
        if core.sha256_file(path) != basis[sha_key]:
            raise ValueError(f"Evidence package basis drift: {sha_key}")
    if package["expected_outputs"] != {"one_result_per_task": True, "filename_rule": "same-basename-as-task"}:
        raise ValueError("Evidence expected-output contract mismatch")
    for key, expected_path in (("run_package", PACKAGE_SCHEMA), ("task", TASK_SCHEMA), ("card", CARD_SCHEMA)):
        meta = package["contracts"].get(key)
        if not isinstance(meta, dict) or meta.get("path") != str(expected_path):
            raise ValueError(f"Evidence contract metadata missing: {key}")
        path = _repo_file(repo_root, meta["path"], f"Evidence contract {key}")
        if core.sha256_file(path) != meta.get("sha256"):
            raise ValueError(f"Evidence contract drift: {meta['path']}")
    supplement_entries: dict[str, dict[str, Any]] = {}
    if "authority_supplement" in package:
        supplement_meta = package["contracts"].get("supplement")
        if not isinstance(supplement_meta, dict) or supplement_meta.get("path") != str(SUPPLEMENT_SCHEMA):
            raise ValueError("Evidence supplement contract metadata missing")
        supplement_schema_path = _repo_file(repo_root, supplement_meta["path"], "Evidence supplement contract")
        if core.sha256_file(supplement_schema_path) != supplement_meta.get("sha256"):
            raise ValueError("Evidence supplement contract drift")
    prompt = package["prompt"]
    prompt_path = _repo_file(repo_root, prompt["path"], "Evidence prompt")
    if prompt["path"] != str(PROMPT_PATH) or core.sha256_file(prompt_path) != prompt["sha256"]:
        raise ValueError("Evidence prompt contract drift")

    state = core.load_json(repo_root / basis["state_path"])
    core.verify_state_basis(repo_root, cfg, state, implementation_sha)
    if state["issue_id"] != package["issue_id"] or state["research_profile"] != package["research_profile"]:
        raise ValueError("Evidence package/State profile identity divergence")
    profile = core.load_json(repo_root / basis["profile_path"])
    if profile["issue_id"] != package["issue_id"] or profile["research_profile"] != package["research_profile"]:
        raise ValueError("Evidence package/Profile identity divergence")

    acceptance_path = repo_root / basis["screening_acceptance_path"]
    acceptance, _, discoveries = validate_screening_acceptance(
        repo_root,
        acceptance_path,
        repo_root / basis["discovery_path"],
        package["issue_id"],
        implementation_sha,
    )
    if core.sha256_file(acceptance_path) != basis["screening_acceptance_sha256"]:
        raise ValueError("Evidence package Screening acceptance bytes changed")
    non_drop = {
        row["discovery_id"] for row in acceptance["decisions"] if row["decision"] != "DROP"
    }
    task_meta = package["tasks"]
    if not isinstance(task_meta, list):
        raise ValueError("Evidence package tasks missing")
    task_ids: list[str] = []
    task_paths: list[str] = []
    task_discovery: list[str] = []
    tasks: list[dict[str, Any]] = []
    for meta in task_meta:
        meta_required = {"evidence_task_id", "path", "sha256", "discovery_ids"}
        meta_optional = {"authority_supplement_source_ids"}
        if not isinstance(meta, dict) or set(meta) - meta_required - meta_optional or not meta_required.issubset(meta):
            raise ValueError("Evidence task metadata fields invalid")
        task_ids.append(meta["evidence_task_id"])
        task_paths.append(meta["path"])
        task_discovery.extend(meta["discovery_ids"])
        task_path = package_path.parent / meta["path"]
        if task_path.is_symlink() or not task_path.is_file() or core.sha256_file(task_path) != meta["sha256"]:
            raise ValueError(f"Evidence Task bytes changed: {meta['evidence_task_id']}")
        if Path(meta["path"]).name != task_filename(meta["evidence_task_id"]):
            raise ValueError(f"Evidence Task filename is not deterministic: {meta['evidence_task_id']}")
        task = core.load_json(task_path)
        errors = _validate_task(task, meta, basis["screening_acceptance_sha256"])
        if errors:
            raise ValueError(f"Evidence Task {meta['evidence_task_id']} invalid: {'; '.join(errors)}")
        if "authority_supplement_source_ids" in meta and meta["authority_supplement_source_ids"] != task.get("authority_supplement_source_ids"):
            raise ValueError(
                f"Evidence Task metadata supplement bindings differ: {meta['evidence_task_id']}"
            )
        tasks.append(task)
    if len(task_ids) != len(set(task_ids)) or len(task_paths) != len(set(task_paths)):
        raise ValueError("Evidence package contains duplicate task identities/paths")
    if len(task_discovery) != len(set(task_discovery)) or set(task_discovery) != non_drop:
        raise ValueError("Evidence Tasks must cover every non-DROP Discovery exactly once")
    if {row["discovery_id"] for row in discoveries} != {
        row["discovery_id"] for row in acceptance["decisions"]
    }:
        raise ValueError("Evidence package inherited inconsistent Discovery/Screening basis")
    if "authority_supplement" in package:
        supplement_entries = _supplement_entries_for_package(
            repo_root,
            package,
            implementation_sha=implementation_sha,
            screening_acceptance=acceptance,
            discoveries=discoveries,
        )
        bound: dict[str, int] = {}
        task_by_id = {task["evidence_task_id"]: task for task in tasks}
        for task in tasks:
            for source_id in task.get("authority_supplement_source_ids", []):
                entry = supplement_entries.get(source_id)
                if entry is None:
                    raise ValueError(f"Evidence Task references unknown supplement source: {source_id}")
                if entry["evidence_task_id"] != task["evidence_task_id"] or entry["discovery_id"] not in task["discovery_ids"]:
                    raise ValueError(f"Evidence supplement source is bound to the wrong task: {source_id}")
                bound[source_id] = bound.get(source_id, 0) + 1
        if set(bound) != set(supplement_entries) or any(count != 1 for count in bound.values()):
            raise ValueError("every Evidence supplement source must be bound exactly once by its task")
    elif any("authority_supplement_source_ids" in task for task in tasks):
        raise ValueError("Evidence Task supplement sources require an Evidence Authority Supplement manifest")
    elif "supplement" in package["contracts"]:
        raise ValueError("Evidence supplement contract requires an Evidence Authority Supplement manifest")
    return acceptance, tasks


def _check_subject_role(
    errors: list[str], subject_id: Any, subject_role: Any, primary_subject_id: str,
    entity_set: set[str], label: str,
) -> None:
    if subject_id not in entity_set:
        errors.append(f"{label} subject_id is not a registered entity")
        return
    if subject_role not in SUBJECT_ROLES:
        errors.append(f"{label} subject_role invalid")
        return
    if subject_role == "PRIMARY_SUBJECT" and subject_id != primary_subject_id:
        errors.append(f"{label} PRIMARY_SUBJECT must bind artifact.primary_subject_id")
    if subject_role in {"COMPARATOR", "RELATED"} and subject_id == primary_subject_id:
        errors.append(f"{label} {subject_role} cannot bind artifact.primary_subject_id")


def validate_evidence_card(
    card: dict[str, Any],
    task: dict[str, Any],
    task_sha: str,
    package: dict[str, Any],
    *,
    repo_root: Path | None = None,
) -> list[str]:
    errors: list[str] = []
    if set(card) != CARD_KEYS:
        return ["Evidence Card fields must exactly match factual v2 contract; editorial fields are forbidden"]
    if card.get("schema_version") != "2.0-rc1":
        errors.append("Evidence Card schema_version mismatch")
    if card.get("issue_id") != task.get("issue_id") or card.get("evidence_task_id") != task.get("evidence_task_id"):
        errors.append("Evidence Card task identity mismatch")
    expected_basis = {
        "task_sha256": task_sha,
        "screening_acceptance_sha256": task["screening_basis"]["screening_acceptance_sha256"],
        "prompt_sha256": package["prompt"]["sha256"],
        "result_contract_sha256": package["contracts"]["card"]["sha256"],
    }
    if card.get("basis") != expected_basis:
        errors.append("Evidence Card basis hashes do not match exact task/package")
    if card.get("status") not in {"VERIFIED", "PARTIAL", "REJECTED", "NEEDS_MORE"}:
        errors.append("Evidence Card status invalid")

    entities = card.get("entities")
    if not isinstance(entities, list) or not entities:
        return errors + ["Evidence Card requires at least one entity"]
    entity_ids = [row.get("entity_id") for row in entities if isinstance(row, dict)]
    if len(entity_ids) != len(entities) or any(not isinstance(x, str) or not x for x in entity_ids) or len(entity_ids) != len(set(entity_ids)):
        return errors + ["Evidence Card entity_id values must be unique non-empty strings"]
    entity_set = set(entity_ids)
    artifact = card.get("artifact")
    if not isinstance(artifact, dict) or artifact.get("primary_subject_id") not in entity_set:
        return errors + ["artifact.primary_subject_id must reference a registered entity"]
    primary_subject_id = artifact["primary_subject_id"]

    sources = card.get("sources")
    if not isinstance(sources, list) or not sources:
        return errors + ["Evidence Card requires at least one source"]
    source_ids = [row.get("source_id") for row in sources if isinstance(row, dict)]
    if len(source_ids) != len(sources) or any(not isinstance(x, str) or not x for x in source_ids) or len(source_ids) != len(set(source_ids)):
        return errors + ["Evidence Card source_id values must be unique non-empty strings"]
    source_set = set(source_ids)
    allowed_sources: dict[str, dict[str, Any]] = {}
    if package.get("authority_supplement") is not None:
        if repo_root is None:
            errors.append("Evidence Authority Supplement source binding requires repository validation context")
        else:
            try:
                allowed_sources = task_authority_sources(repo_root, task, package)
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                errors.append(str(exc))
    else:
        allowed_sources = {
            f"src-{index}": {
                "url": source.get("locator"),
                "source_class": _source_class(source.get("source_type")),
                "supplement": False,
            }
            for index, source in enumerate(task.get("source_records", []), start=1)
            if isinstance(source, dict)
        }
    allowed_locators = {value.get("url") for value in allowed_sources.values()}
    for source in sources:
        source_id = source.get("source_id")
        authority_source = allowed_sources.get(source_id)
        if authority_source is None:
            # Existing Discovery Cards use their own source-id namespace
            # (for example, ``source-1``) while the Core authority map uses
            # deterministic ``src-N`` keys.  Preserve that legacy contract
            # only for an unambiguous Discovery locator; supplement sources
            # still require their explicit supplement_source_id.
            discovery_matches = [
                value for value in allowed_sources.values()
                if not value.get("supplement") and value.get("url") == source.get("url")
            ]
            if len(discovery_matches) == 1:
                authority_source = discovery_matches[0]
        if package.get("authority_supplement") is None:
            unbound = source.get("url") not in allowed_locators
        else:
            unbound = authority_source is None or source.get("url") not in allowed_locators or source.get("url") != authority_source.get("url")
        if unbound:
            errors.append(
                f"Evidence source {source.get('source_id')} was not explicitly bound to this Evidence task; add it through Discovery/Screening first or use an exact Evidence Authority Supplement"
            )
        elif authority_source is not None and source.get("source_class") != authority_source.get("source_class"):
            errors.append(
                f"Evidence source {source_id} source_class does not match task-bound authority class {authority_source.get('source_class')}"
            )
        elif package.get("authority_supplement") is not None and authority_source is not None and authority_source.get("supplement"):
            for key in ("url", "source_class", "title", "published_at", "accessed_at"):
                if source.get(key) != authority_source.get(key):
                    errors.append(
                        f"Evidence supplement source {source_id} {key} differs from exact authority manifest"
                    )
        try:
            core.parse_instant(str(source.get("accessed_at", "")))
        except ValueError:
            errors.append(f"Evidence source {source.get('source_id')} accessed_at must be offset-aware")

    def check_refs(item: dict[str, Any], label: str) -> None:
        refs = item.get("source_ids")
        if not isinstance(refs, list) or not refs or any(ref not in source_set for ref in refs):
            errors.append(f"{label} source_ids must reference registered sources")
        _check_subject_role(
            errors, item.get("subject_id"), item.get("subject_role"),
            primary_subject_id, entity_set, label,
        )

    temporal = card.get("temporal")
    if not isinstance(temporal, dict):
        errors.append("temporal must be an object")
    else:
        try:
            core.parse_instant(str(temporal.get("observed_at", "")))
        except ValueError:
            errors.append("temporal.observed_at must be offset-aware")
        event_ids: list[str] = []
        for event in temporal.get("events", []):
            if not isinstance(event, dict):
                errors.append("temporal event must be an object")
                continue
            event_ids.append(event.get("event_id"))
            check_refs(event, f"event {event.get('event_id')}")
        if len(event_ids) != len(set(event_ids)):
            errors.append("event_id values must be unique")

    for collection_name in ("claims", "limitations"):
        values = card.get(collection_name)
        if not isinstance(values, list):
            errors.append(f"{collection_name} must be an array")
            continue
        statement_ids: list[str] = []
        for item in values:
            if not isinstance(item, dict):
                errors.append(f"{collection_name} item must be an object")
                continue
            statement_ids.append(item.get("statement_id"))
            if item.get("evidence_class") not in EVIDENCE_CLASSES:
                errors.append(f"{collection_name} evidence_class invalid")
            check_refs(item, f"{collection_name} {item.get('statement_id')}")
        if len(statement_ids) != len(set(statement_ids)):
            errors.append(f"{collection_name} statement_id values must be unique")

    metrics = card.get("metrics")
    if not isinstance(metrics, list):
        errors.append("metrics must be an array")
    else:
        metric_ids: list[str] = []
        for metric in metrics:
            if not isinstance(metric, dict):
                errors.append("metric must be an object")
                continue
            metric_ids.append(metric.get("metric_id"))
            if metric.get("evidence_class") not in EVIDENCE_CLASSES:
                errors.append("metric evidence_class invalid")
            check_refs(metric, f"metric {metric.get('metric_id')}")
            comparators = metric.get("comparison_subject_ids")
            if not isinstance(comparators, list) or len(comparators) != len(set(comparators)) or any(x not in entity_set for x in comparators):
                errors.append(f"metric {metric.get('metric_id')} comparison_subject_ids must be unique registered entities")
            elif metric.get("subject_id") in comparators:
                errors.append(f"metric {metric.get('metric_id')} cannot list its own subject as comparator")
            elif metric.get("subject_role") == "COMPARATOR" and primary_subject_id not in comparators:
                errors.append(f"comparator metric {metric.get('metric_id')} must explicitly compare against the primary subject")
        if len(metric_ids) != len(set(metric_ids)):
            errors.append("metric_id values must be unique")

    verification = card.get("verification")
    if not isinstance(verification, dict):
        errors.append("verification must be an object")
    else:
        for target in verification.get("targets", []):
            if not isinstance(target, dict):
                errors.append("verification target must be an object")
                continue
            subjects = target.get("subject_ids")
            refs = target.get("source_ids")
            if not isinstance(subjects, list) or any(x not in entity_set for x in subjects):
                errors.append("verification subject_ids must reference registered entities")
            if not isinstance(refs, list) or any(x not in source_set for x in refs):
                errors.append("verification source_ids must reference registered sources")
    return errors


def _evidence_result_set_digest(package_sha: str, entries: list[dict[str, Any]]) -> str:
    return core.sha256_object({
        "package_sha256": package_sha,
        "results": sorted(entries, key=lambda row: row["evidence_task_id"]),
    })


def accept_evidence_results(
    repo_root: Path,
    package_path: Path,
    results_dir: Path,
    accepted_root: Path,
    implementation_sha: str,
) -> Path:
    package = core.load_json(package_path)
    validate_evidence_package_basis(repo_root, package_path, package, implementation_sha)
    expected = {Path(meta["path"]).name for meta in package["tasks"]}
    files = _exact_regular_files(results_dir, expected, "Evidence result set")
    entries: list[dict[str, Any]] = []
    for meta in package["tasks"]:
        task_path = package_path.parent / meta["path"]
        task = core.load_json(task_path)
        result_path = files[Path(meta["path"]).name]
        card = core.load_json(result_path)
        errors = validate_evidence_card(card, task, meta["sha256"], package, repo_root=repo_root)
        if errors:
            raise ValueError(f"Evidence Card {meta['evidence_task_id']} invalid: {'; '.join(errors)}")
        entries.append({
            "evidence_task_id": meta["evidence_task_id"],
            "discovery_ids": list(meta["discovery_ids"]),
            "sha256": core.sha256_file(result_path),
            "status": card["status"],
            "filename": result_path.name,
        })
    package_sha = core.sha256_file(package_path)
    result_set_sha = _evidence_result_set_digest(package_sha, entries)
    run_dir = accepted_root / result_set_sha
    acceptance_path = run_dir / "evidence-accepted.json"
    if run_dir.exists():
        if acceptance_path.is_file():
            validate_evidence_acceptance(repo_root, acceptance_path, implementation_sha)
            return acceptance_path
        raise ValueError(f"incomplete pre-existing Evidence acceptance directory: {run_dir}")
    (run_dir / "tasks").mkdir(parents=True)
    (run_dir / "results").mkdir(parents=True)
    shutil.copy2(package_path, run_dir / "package.json")
    for meta in package["tasks"]:
        basename = Path(meta["path"]).name
        shutil.copy2(package_path.parent / meta["path"], run_dir / "tasks" / basename)
        shutil.copy2(files[basename], run_dir / "results" / basename)
    acceptance = {
        "schema_version": "2.0-rc1",
        "issue_id": package["issue_id"],
        "research_profile": package["research_profile"],
        "result_set_sha256": result_set_sha,
        "package_sha256": package_sha,
        "screening_acceptance_sha256": package["basis"]["screening_acceptance_sha256"],
        "result_count": len(entries),
        "results": sorted(entries, key=lambda row: row["evidence_task_id"]),
    }
    core.write_json(acceptance_path, acceptance)
    return acceptance_path


def validate_evidence_acceptance(
    repo_root: Path, evidence_acceptance_path: Path, implementation_sha: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    acceptance = core.load_json(evidence_acceptance_path)
    expected_keys = {
        "schema_version", "issue_id", "research_profile", "result_set_sha256",
        "package_sha256", "screening_acceptance_sha256", "result_count", "results",
    }
    if set(acceptance) != expected_keys or acceptance["schema_version"] != "2.0-rc1":
        raise ValueError("Evidence acceptance fields/schema_version invalid")
    run_dir = evidence_acceptance_path.parent
    package_path = run_dir / "package.json"
    if not package_path.is_file() or core.sha256_file(package_path) != acceptance["package_sha256"]:
        raise ValueError("accepted Evidence package copy missing or changed")
    package = core.load_json(package_path)
    validate_evidence_package_basis(repo_root, package_path, package, implementation_sha)
    if package["issue_id"] != acceptance["issue_id"] or package["research_profile"] != acceptance["research_profile"]:
        raise ValueError("Evidence package/acceptance identity mismatch")
    if package["basis"]["screening_acceptance_sha256"] != acceptance["screening_acceptance_sha256"]:
        raise ValueError("Evidence acceptance Screening basis mismatch")

    expected_names = {Path(meta["path"]).name for meta in package["tasks"]}
    task_files = _exact_regular_files(run_dir / "tasks", expected_names, "accepted Evidence task set")
    result_files = _exact_regular_files(run_dir / "results", expected_names, "accepted Evidence result set")
    meta_by_id = {meta["evidence_task_id"]: meta for meta in package["tasks"]}
    entries = acceptance["results"]
    if not isinstance(entries, list) or acceptance["result_count"] != len(entries):
        raise ValueError("Evidence acceptance result_count mismatch")
    ids = [row.get("evidence_task_id") for row in entries if isinstance(row, dict)]
    if len(ids) != len(entries) or len(ids) != len(set(ids)) or set(ids) != set(meta_by_id):
        raise ValueError("Evidence acceptance result identities do not match package tasks")
    for row in entries:
        meta = meta_by_id[row["evidence_task_id"]]
        name = Path(meta["path"]).name
        if core.sha256_file(task_files[name]) != meta["sha256"]:
            raise ValueError(f"accepted Evidence Task changed: {row['evidence_task_id']}")
        if row.get("filename") != name or core.sha256_file(result_files[name]) != row.get("sha256"):
            raise ValueError(f"accepted Evidence result changed: {row['evidence_task_id']}")
        card = core.load_json(result_files[name])
        errors = validate_evidence_card(
            card,
            core.load_json(task_files[name]),
            meta["sha256"],
            package,
            repo_root=repo_root,
        )
        if errors or card.get("status") != row.get("status") or row.get("discovery_ids") != meta["discovery_ids"]:
            raise ValueError(f"accepted Evidence result metadata/card divergence: {row['evidence_task_id']}")
    digest = _evidence_result_set_digest(acceptance["package_sha256"], entries)
    if acceptance["result_set_sha256"] != digest or run_dir.name != digest:
        raise ValueError("Evidence acceptance content-addressed identity mismatch")
    return acceptance, package


def validate_edition_view(
    view: dict[str, Any], profile: dict[str, Any], evidence_sha: str, evidence_status: str
) -> list[str]:
    errors: list[str] = []
    required = {
        "schema_version", "issue_id", "research_profile", "evidence_task_id",
        "evidence_sha256", "materiality", "scope_dimensions", "profile_annotations",
    }
    if set(view) != required:
        return ["Edition Evidence View fields must exactly match v2 contract"]
    if view.get("schema_version") != "2.0-rc1" or view.get("issue_id") != profile["issue_id"] or view.get("research_profile") != profile["research_profile"]:
        errors.append("Edition Evidence View identity mismatch")
    if view.get("evidence_sha256") != evidence_sha:
        errors.append("Edition Evidence View does not bind exact factual Evidence bytes")
    materiality = view.get("materiality")
    if not isinstance(materiality, dict) or set(materiality) != {"status", "rationale"} or materiality.get("status") not in VIEW_MATERIALITY or not isinstance(materiality.get("rationale"), str) or not materiality["rationale"].strip():
        errors.append("Edition Evidence View materiality invalid")
    else:
        status = materiality["status"]
        if evidence_status == "REJECTED" and status != "NON_MATERIAL":
            errors.append("REJECTED factual Evidence must be NON_MATERIAL in Edition View")
        if evidence_status == "NEEDS_MORE" and status != "HOLD":
            errors.append("NEEDS_MORE factual Evidence must remain HOLD in Edition View")
    dims = view.get("scope_dimensions")
    allowed_dims = set(profile["research_scope"]["scope_dimensions"])
    if not isinstance(dims, list) or len(dims) != len(set(dims)) or any(x not in allowed_dims for x in dims):
        errors.append("Edition Evidence View scope_dimensions must come from Production Profile")
    ann = view.get("profile_annotations")
    if not isinstance(ann, dict):
        return errors + ["profile_annotations must be an object"]
    research_profile = profile["research_profile"]
    if research_profile == "WEEKLY":
        expected = {"why_this_issue", "window_relation", "carry_over"}
        if set(ann) != expected or not isinstance(ann.get("why_this_issue"), str) or not ann.get("why_this_issue", "").strip() or not isinstance(ann.get("carry_over"), bool):
            errors.append("Weekly Edition View annotations invalid")
        if ann.get("window_relation") not in {"MAIN_EVENT", "PRE_WINDOW_RELEVANCE", "POST_CUTOFF", "CARRY_OVER", "OTHER"}:
            errors.append("Weekly window_relation invalid")
    elif research_profile == "THEMATIC":
        expected = {"lineage_role", "branch_ids", "transition_ids", "inheritance_note", "historical_attribution_caveat"}
        if set(ann) != expected:
            errors.append("Thematic Edition View annotations invalid")
        if ann.get("lineage_role") not in {"CORE", "BRIDGE", "CONTEXT", "PARALLEL", "COMPETING", "COUNTEREXAMPLE"}:
            errors.append("Thematic lineage_role invalid")
        for key in ("branch_ids", "transition_ids"):
            vals = ann.get(key)
            if not isinstance(vals, list) or len(vals) != len(set(vals)) or any(not isinstance(x, str) or not x for x in vals):
                errors.append(f"Thematic {key} invalid")
        for key in ("inheritance_note", "historical_attribution_caveat"):
            if ann.get(key) is not None and not isinstance(ann.get(key), str):
                errors.append(f"Thematic {key} must be string or null")
    elif research_profile == "RETROSPECTIVE_PERIOD":
        expected = {"period_role", "chronology_relevance"}
        if set(ann) != expected or not isinstance(ann.get("period_role"), str) or not ann.get("period_role", "").strip() or not isinstance(ann.get("chronology_relevance"), bool):
            errors.append("Period Edition View annotations invalid")
    return errors


def _view_set_digest(rows: list[dict[str, Any]]) -> str:
    return core.sha256_object(sorted(rows, key=lambda row: row["evidence_task_id"]))


def accept_edition_views(
    repo_root: Path,
    profile_path: Path,
    evidence_acceptance_path: Path,
    views_dir: Path,
    accepted_root: Path,
    implementation_sha: str,
) -> Path:
    profile = core.load_json(profile_path)
    evidence_acceptance, _ = validate_evidence_acceptance(repo_root, evidence_acceptance_path, implementation_sha)
    if evidence_acceptance["issue_id"] != profile["issue_id"] or evidence_acceptance["research_profile"] != profile["research_profile"]:
        raise ValueError("Edition View Profile/Evidence acceptance identity mismatch")
    expected = {entry["evidence_task_id"]: entry for entry in evidence_acceptance["results"]}
    expected_names = {view_filename(task_id) for task_id in expected}
    files = _exact_regular_files(views_dir, expected_names, "Edition Evidence View set")
    rows: list[dict[str, Any]] = []
    for task_id, entry in expected.items():
        path = files[view_filename(task_id)]
        view = core.load_json(path)
        if view.get("evidence_task_id") != task_id:
            raise ValueError(f"Edition View filename/task mismatch: {task_id}")
        errors = validate_edition_view(view, profile, entry["sha256"], entry["status"])
        if errors:
            raise ValueError(f"Edition Evidence View {task_id} invalid: {'; '.join(errors)}")
        rows.append({
            "evidence_task_id": task_id,
            "evidence_sha256": entry["sha256"],
            "view_sha256": core.sha256_file(path),
            "materiality": view["materiality"]["status"],
            "scope_dimensions": list(view["scope_dimensions"]),
        })
    view_set_sha = _view_set_digest(rows)
    run_dir = accepted_root / view_set_sha
    acceptance_path = run_dir / "edition-views-accepted.json"
    if run_dir.exists():
        if acceptance_path.is_file():
            validate_edition_views_acceptance(
                repo_root, profile_path, evidence_acceptance_path, acceptance_path, implementation_sha
            )
            return acceptance_path
        raise ValueError(f"incomplete pre-existing Edition View acceptance directory: {run_dir}")
    (run_dir / "views").mkdir(parents=True)
    for path in files.values():
        shutil.copy2(path, run_dir / "views" / path.name)
    acceptance = {
        "schema_version": "2.0-rc1",
        "issue_id": profile["issue_id"],
        "research_profile": profile["research_profile"],
        "view_set_sha256": view_set_sha,
        "profile_sha256": core.sha256_file(profile_path),
        "evidence_acceptance_sha256": core.sha256_file(evidence_acceptance_path),
        "views": sorted(rows, key=lambda row: row["evidence_task_id"]),
    }
    core.write_json(acceptance_path, acceptance)
    return acceptance_path


def validate_edition_views_acceptance(
    repo_root: Path,
    profile_path: Path,
    evidence_acceptance_path: Path,
    views_acceptance_path: Path,
    implementation_sha: str,
) -> dict[str, Any]:
    profile = core.load_json(profile_path)
    evidence_acceptance, _ = validate_evidence_acceptance(repo_root, evidence_acceptance_path, implementation_sha)
    acceptance = core.load_json(views_acceptance_path)
    expected_keys = {
        "schema_version", "issue_id", "research_profile", "view_set_sha256",
        "profile_sha256", "evidence_acceptance_sha256", "views",
    }
    if set(acceptance) != expected_keys or acceptance["schema_version"] != "2.0-rc1":
        raise ValueError("Edition View acceptance fields/schema_version invalid")
    if acceptance["issue_id"] != profile["issue_id"] or acceptance["research_profile"] != profile["research_profile"]:
        raise ValueError("Edition View acceptance Profile identity mismatch")
    if acceptance["profile_sha256"] != core.sha256_file(profile_path) or acceptance["evidence_acceptance_sha256"] != core.sha256_file(evidence_acceptance_path):
        raise ValueError("Edition View acceptance basis bytes changed")
    expected_evidence = {row["evidence_task_id"]: row for row in evidence_acceptance["results"]}
    rows = acceptance["views"]
    ids = [row.get("evidence_task_id") for row in rows if isinstance(row, dict)]
    if len(ids) != len(rows) or len(ids) != len(set(ids)) or set(ids) != set(expected_evidence):
        raise ValueError("Edition View acceptance does not cover Evidence tasks exactly")
    expected_names = {view_filename(task_id) for task_id in expected_evidence}
    files = _exact_regular_files(views_acceptance_path.parent / "views", expected_names, "accepted Edition View set")
    for row in rows:
        task_id = row["evidence_task_id"]
        path = files[view_filename(task_id)]
        if core.sha256_file(path) != row.get("view_sha256"):
            raise ValueError(f"accepted Edition View bytes changed: {task_id}")
        view = core.load_json(path)
        evidence = expected_evidence[task_id]
        errors = validate_edition_view(view, profile, evidence["sha256"], evidence["status"])
        if errors or row.get("evidence_sha256") != evidence["sha256"] or row.get("materiality") != view["materiality"]["status"] or row.get("scope_dimensions") != view["scope_dimensions"]:
            raise ValueError(f"accepted Edition View metadata/content divergence: {task_id}")
    digest = _view_set_digest(rows)
    if acceptance["view_set_sha256"] != digest or views_acceptance_path.parent.name != digest:
        raise ValueError("Edition View acceptance content-addressed identity mismatch")
    return acceptance


def build_materiality_ledger(
    repo_root: Path,
    profile_path: Path,
    discovery_path: Path,
    screening_acceptance_path: Path,
    evidence_acceptance_path: Path,
    views_acceptance_path: Path,
    implementation_sha: str,
) -> dict[str, Any]:
    profile = core.load_json(profile_path)
    screening_acceptance, _, discoveries = validate_screening_acceptance(
        repo_root, screening_acceptance_path, discovery_path, profile["issue_id"], implementation_sha
    )
    evidence_acceptance, _ = validate_evidence_acceptance(repo_root, evidence_acceptance_path, implementation_sha)
    views_acceptance = validate_edition_views_acceptance(
        repo_root, profile_path, evidence_acceptance_path, views_acceptance_path, implementation_sha
    )
    screening_map = {row["discovery_id"]: row for row in screening_acceptance["decisions"]}
    evidence_by_discovery: dict[str, list[str]] = {}
    for row in evidence_acceptance["results"]:
        for discovery_id in row["discovery_ids"]:
            evidence_by_discovery.setdefault(discovery_id, []).append(row["evidence_task_id"])
    view_map = {row["evidence_task_id"]: row["materiality"] for row in views_acceptance["views"]}
    rows: list[dict[str, Any]] = []
    for discovery in discoveries:
        discovery_id = discovery["discovery_id"]
        decision = screening_map.get(discovery_id)
        if decision is None:
            raise ValueError(f"silent drop: Discovery lacks Screening disposition: {discovery_id}")
        tasks = sorted(evidence_by_discovery.get(discovery_id, []))
        if decision["decision"] == "DROP":
            if tasks:
                raise ValueError(f"DROP Discovery unexpectedly has Evidence task: {discovery_id}")
            duplicate_group = decision.get("duplicate_group")
            disposition = "DUPLICATE" if duplicate_group else "EXCLUDED"
            statuses: list[str] = []
            rationale = decision["reason"]
        else:
            if len(tasks) != 1:
                raise ValueError(f"non-DROP Discovery must have exactly one Evidence task in WU-007: {discovery_id}")
            task_id = tasks[0]
            if task_id not in view_map:
                raise ValueError(f"silent drop: Evidence task lacks Edition View: {task_id}")
            statuses = [view_map[task_id]]
            disposition = statuses[0]
            duplicate_group = None
            rationale = f"Screening={decision['decision']}; Edition View={disposition}"
        rows.append({
            "discovery_id": discovery_id,
            "origin": discovery["provenance"]["origin"],
            "screening_decision": decision["decision"],
            "downstream_disposition": disposition,
            "evidence_task_ids": tasks,
            "evidence_view_statuses": statuses,
            "duplicate_group": duplicate_group,
            "rationale": rationale,
        })
    ledger = {
        "schema_version": "2.0-rc1",
        "issue_id": profile["issue_id"],
        "research_profile": profile["research_profile"],
        "basis": {
            "production_profile_sha256": core.sha256_file(profile_path),
            "discovery_sha256": core.sha256_file(discovery_path),
            "screening_acceptance_sha256": core.sha256_file(screening_acceptance_path),
            "evidence_acceptance_sha256": core.sha256_file(evidence_acceptance_path),
            "edition_views_acceptance_sha256": core.sha256_file(views_acceptance_path),
            "evidence_set_sha256": evidence_acceptance["result_set_sha256"],
            "edition_view_set_sha256": views_acceptance["view_set_sha256"],
        },
        "rows": sorted(rows, key=lambda row: row["discovery_id"]),
    }
    validate_materiality_ledger(
        ledger, repo_root, profile_path, discovery_path, screening_acceptance_path,
        evidence_acceptance_path, views_acceptance_path, implementation_sha,
    )
    return ledger


def validate_materiality_ledger(
    ledger: dict[str, Any],
    repo_root: Path,
    profile_path: Path,
    discovery_path: Path,
    screening_acceptance_path: Path,
    evidence_acceptance_path: Path,
    views_acceptance_path: Path,
    implementation_sha: str,
) -> None:
    profile = core.load_json(profile_path)
    screening_acceptance, _, discoveries = validate_screening_acceptance(
        repo_root, screening_acceptance_path, discovery_path, profile["issue_id"], implementation_sha
    )
    evidence_acceptance, _ = validate_evidence_acceptance(repo_root, evidence_acceptance_path, implementation_sha)
    views_acceptance = validate_edition_views_acceptance(
        repo_root, profile_path, evidence_acceptance_path, views_acceptance_path, implementation_sha
    )
    expected_basis = {
        "production_profile_sha256": core.sha256_file(profile_path),
        "discovery_sha256": core.sha256_file(discovery_path),
        "screening_acceptance_sha256": core.sha256_file(screening_acceptance_path),
        "evidence_acceptance_sha256": core.sha256_file(evidence_acceptance_path),
        "edition_views_acceptance_sha256": core.sha256_file(views_acceptance_path),
        "evidence_set_sha256": evidence_acceptance["result_set_sha256"],
        "edition_view_set_sha256": views_acceptance["view_set_sha256"],
    }
    if set(ledger) != {"schema_version", "issue_id", "research_profile", "basis", "rows"} or ledger.get("schema_version") != "2.0-rc1":
        raise ValueError("Materiality Ledger fields/schema_version invalid")
    if ledger.get("issue_id") != profile["issue_id"] or ledger.get("research_profile") != profile["research_profile"]:
        raise ValueError("Materiality Ledger Profile identity mismatch")
    if ledger.get("basis") != expected_basis:
        raise ValueError("Materiality Ledger basis hashes do not match exact upstream artifacts")
    expected_ids = {row["discovery_id"] for row in discoveries}
    rows = ledger.get("rows")
    if not isinstance(rows, list):
        raise ValueError("Materiality Ledger rows missing")
    actual_ids = [row.get("discovery_id") for row in rows if isinstance(row, dict)]
    if len(actual_ids) != len(rows) or len(actual_ids) != len(set(actual_ids)) or set(actual_ids) != expected_ids:
        raise ValueError("Materiality Ledger must contain exactly one row per Discovery; silent drop/extra row detected")
    screening_map = {row["discovery_id"]: row for row in screening_acceptance["decisions"]}
    evidence_tasks = {row["evidence_task_id"] for row in evidence_acceptance["results"]}
    view_map = {row["evidence_task_id"]: row["materiality"] for row in views_acceptance["views"]}
    evidence_by_discovery: dict[str, list[str]] = {}
    for evidence in evidence_acceptance["results"]:
        for discovery_id in evidence["discovery_ids"]:
            evidence_by_discovery.setdefault(discovery_id, []).append(evidence["evidence_task_id"])
    for row in rows:
        discovery_id = row["discovery_id"]
        decision = screening_map[discovery_id]
        if row.get("screening_decision") != decision["decision"]:
            raise ValueError(f"Materiality row Screening decision drift: {discovery_id}")
        expected_tasks = sorted(evidence_by_discovery.get(discovery_id, []))
        if row.get("evidence_task_ids") != expected_tasks:
            raise ValueError(f"Materiality row Evidence refs drift: {discovery_id}")
        statuses = row.get("evidence_view_statuses")
        if decision["decision"] == "DROP":
            expected_disposition = "DUPLICATE" if decision.get("duplicate_group") else "EXCLUDED"
            if expected_tasks or statuses != [] or row.get("downstream_disposition") != expected_disposition or row.get("duplicate_group") != decision.get("duplicate_group"):
                raise ValueError(f"DROP Materiality disposition invalid: {discovery_id}")
        else:
            if len(expected_tasks) != 1 or expected_tasks[0] not in evidence_tasks:
                raise ValueError(f"non-DROP Discovery lacks exact Evidence task: {discovery_id}")
            expected_status = view_map.get(expected_tasks[0])
            if statuses != [expected_status] or row.get("downstream_disposition") != expected_status or row.get("duplicate_group") is not None:
                raise ValueError(f"Materiality disposition/View drift: {discovery_id}")
        if not isinstance(row.get("rationale"), str) or not row["rationale"].strip():
            raise ValueError(f"Materiality row rationale missing: {discovery_id}")


def write_materiality_ledger(path: Path, ledger: dict[str, Any]) -> Path:
    if path.exists():
        raise ValueError(f"refusing to overwrite Materiality Ledger: {path}")
    core.write_json(path, ledger)
    return path


def validate_completeness(
    result: dict[str, Any],
    repo_root: Path,
    profile_path: Path,
    discovery_path: Path,
    screening_acceptance_path: Path,
    evidence_acceptance_path: Path,
    views_acceptance_path: Path,
    ledger_path: Path,
    implementation_sha: str,
) -> list[str]:
    errors: list[str] = []
    profile = core.load_json(profile_path)
    ledger = core.load_json(ledger_path)
    try:
        validate_materiality_ledger(
            ledger, repo_root, profile_path, discovery_path, screening_acceptance_path,
            evidence_acceptance_path, views_acceptance_path, implementation_sha,
        )
    except ValueError as exc:
        return [f"Materiality Ledger invalid: {exc}"]
    required = {
        "schema_version", "issue_id", "research_profile", "basis", "overall_status",
        "obligations", "residual_limitations", "closure",
    }
    if set(result) != required:
        return ["Completeness fields must exactly match v2 contract"]
    if result.get("schema_version") != "2.0-rc1" or result.get("issue_id") != profile["issue_id"] or result.get("research_profile") != profile["research_profile"]:
        errors.append("Completeness identity mismatch")
    expected_basis = {
        "production_profile_sha256": core.sha256_file(profile_path),
        "materiality_ledger_sha256": core.sha256_file(ledger_path),
    }
    if result.get("basis") != expected_basis:
        errors.append("Completeness basis hashes do not match exact Profile/Ledger")
    obligations = result.get("obligations")
    if not isinstance(obligations, list):
        return errors + ["Completeness obligations must be an array"]
    ids: list[str] = []
    ledger_discovery_ids = {row["discovery_id"] for row in ledger["rows"]}
    ledger_task_ids = {task for row in ledger["rows"] for task in row["evidence_task_ids"]}
    for obligation in obligations:
        if not isinstance(obligation, dict):
            errors.append("Completeness obligation must be an object")
            continue
        oid = obligation.get("obligation_id")
        if not isinstance(oid, str) or not oid:
            errors.append("Completeness obligation_id invalid")
        else:
            ids.append(oid)
        if obligation.get("status") not in OBLIGATION_STATUS:
            errors.append(f"Completeness obligation {oid} has invalid status")
        if not isinstance(obligation.get("rationale"), str) or not obligation.get("rationale", "").strip():
            errors.append(f"Completeness obligation {oid} rationale missing")
        if any(x not in ledger_discovery_ids for x in obligation.get("discovery_ids", [])):
            errors.append(f"Completeness obligation {oid} references unknown Discovery")
        if any(x not in ledger_task_ids for x in obligation.get("evidence_task_ids", [])):
            errors.append(f"Completeness obligation {oid} references unknown Evidence task")
    if len(ids) != len(set(ids)):
        errors.append("Completeness obligation_id values must be unique")
    dimensions = set(profile["research_scope"]["scope_dimensions"])
    covered_dimensions = {row.get("dimension") for row in obligations if isinstance(row, dict)}
    if dimensions - covered_dimensions:
        errors.append(f"Completeness lacks obligations for Profile dimensions: {sorted(dimensions-covered_dimensions)}")
    needs_research = sum(1 for row in obligations if isinstance(row, dict) and row.get("status") == "NEEDS_RESEARCH")
    limitations = [row for row in obligations if isinstance(row, dict) and row.get("status") == "LIMITATION"]
    residual = result.get("residual_limitations")
    if not isinstance(residual, list) or any(not isinstance(value, str) or not value for value in residual):
        errors.append("residual_limitations invalid")
        residual = []
    expected_status = "INCOMPLETE" if needs_research else ("LIMITED" if limitations or residual else "READY")
    if result.get("overall_status") != expected_status:
        errors.append(f"overall_status must be {expected_status} for current obligations/limitations")

    closure = result.get("closure")
    if profile["research_profile"] == "THEMATIC":
        if not isinstance(closure, dict):
            errors.append("Thematic Completeness requires closure/saturation evidence")
        else:
            required_closure = {
                "expansion_passes", "final_pass_new_sources", "final_pass_new_material_obligations",
                "final_pass_new_material_obligations_open", "targeted_gap_fill_completed",
                "open_material_obligations", "limitations", "status",
            }
            if set(closure) != required_closure:
                errors.append("Thematic closure fields invalid")
            else:
                for key in (
                    "final_pass_new_sources", "final_pass_new_material_obligations",
                    "final_pass_new_material_obligations_open", "open_material_obligations",
                ):
                    if not isinstance(closure[key], int) or closure[key] < 0:
                        errors.append(f"Thematic closure {key} must be a non-negative integer")
                if not isinstance(closure["expansion_passes"], int) or closure["expansion_passes"] < 1:
                    errors.append("Thematic closure requires at least one expansion pass")
                if not isinstance(closure["targeted_gap_fill_completed"], bool):
                    errors.append("Thematic closure targeted_gap_fill_completed must be boolean")
                if closure["final_pass_new_material_obligations_open"] > closure["final_pass_new_material_obligations"]:
                    errors.append("final-pass open material obligations cannot exceed new material obligations")
                if closure["open_material_obligations"] != needs_research:
                    errors.append("Thematic closure open_material_obligations must equal unresolved material obligations")
                expected_closure = "NEEDS_RESEARCH" if expected_status == "INCOMPLETE" else ("LIMITED" if expected_status == "LIMITED" else "COMPLETE")
                if closure.get("status") != expected_closure:
                    errors.append(f"Thematic closure status must be {expected_closure}")
                if expected_closure in {"COMPLETE", "LIMITED"}:
                    if not closure["targeted_gap_fill_completed"]:
                        errors.append("Thematic closure cannot finish before targeted residual gap-fill")
                    if closure["open_material_obligations"] != 0 or closure["final_pass_new_material_obligations_open"] != 0:
                        errors.append("Thematic closure cannot finish with open material obligations")
                closure_limitations = closure.get("limitations")
                if not isinstance(closure_limitations, list) or any(not isinstance(value, str) or not value for value in closure_limitations):
                    errors.append("Thematic closure limitations invalid")
                elif expected_closure == "COMPLETE" and closure_limitations:
                    errors.append("COMPLETE Thematic closure cannot retain unresolved limitations")
                elif expected_closure == "LIMITED" and not closure_limitations:
                    errors.append("LIMITED Thematic closure must state limitations")
                elif expected_closure == "LIMITED" and not set(residual).issubset(set(closure_limitations)):
                    errors.append("Thematic closure must preserve residual limitations")
    elif closure is not None:
        errors.append(f"{profile['research_profile']} Completeness does not use Thematic closure payload")
    return errors
