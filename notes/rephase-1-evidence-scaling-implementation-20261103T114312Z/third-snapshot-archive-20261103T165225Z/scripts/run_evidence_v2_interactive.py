#!/usr/bin/env python3
"""Run Core v2 Evidence, Edition Views, Materiality, and Completeness from explicit interactive records.

The runner is profile-neutral and preserves the Core v2 factual/editorial split:
- one explicit interactive record is required for every non-DROP Evidence task;
- factual Evidence Cards cite only a Discovery-bounded source or an exact
  task-bound Evidence Authority Supplement source;
- interactive records require common factual fields plus only the fields
  belonging to the active Research Profile;
- Edition Views carry Profile-specific materiality/lineage annotations;
- Materiality Ledger is derived by the canonical implementation; and
- Completeness retains every Profile/named obligation and is validated by the
  authoritative profile-completeness guard.

It does not advance Production State and cannot resolve a Human Gate.
"""
from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

from scripts import survey_agent_control_v2 as agent
from scripts import survey_agent_tool_v2 as agent_tool
from scripts import survey_completeness_v2 as completeness
from scripts import survey_discovery_v2 as discovery
from scripts import survey_evidence_v2 as evidence
from scripts import survey_production_v2 as core
from scripts import survey_research_authority_v2 as low
from scripts import survey_schema_v2 as schema_gate
from scripts import survey_screening_v2 as screening

INPUT_NAME = "interactive-evidence.json"
AUDIT_NAME = "interactive-audit.json"
# DM022 ordinary-consumer readiness (B side). Normal CANDIDATES_NORMALIZED
# generation requires guard absence; supersession-mode versioned outputs are
# written only by HIGH R writers. Canonical Ledger/Completeness creation while
# the transition guard is held refuses (no old-runner bypass with fabricated
# State, no synthetic CANDIDATES_NORMALIZED pretense).



def _dm022_require_ready(repo_root: Path, state_path: Path) -> None:
    low.require_research_operation_ready(repo_root, state_path)

# DM016 canonical classification lives in survey_evidence_v2._source_class
# (Owner A adds the selected 10 rows there). This runner's former local
# six-key SOURCE_CLASS_MAP was removed after caller census proved zero
# in-file/test callers; live card/task paths already use the canonical leaf.
# Do not reintroduce a second maintained table here.

ENTITY_TYPES = {
    "MODEL", "MODEL_FAMILY", "VARIANT", "API", "PRODUCT", "AGENT",
    "FRAMEWORK", "PAPER", "BENCHMARK", "DATASET", "ORGANIZATION", "OTHER",
}
ARTIFACT_TYPES = {
    "MODEL", "MODEL_UPDATE", "OPEN_WEIGHT", "API", "PRODUCT", "AGENT",
    "FRAMEWORK", "PAPER", "BENCHMARK", "DATASET", "SAFETY_EVENT",
    "SECURITY_EVENT", "INTEGRATION", "OTHER",
}
EVIDENCE_CLASSES = {
    "PRIMARY_FACT", "VENDOR_CLAIM", "PROJECT_CLAIM", "AUTHOR_CLAIM",
    "SOCIAL_OBSERVATION", "INFERENCE",
}
CARD_STATUS = {"VERIFIED", "PARTIAL", "REJECTED", "NEEDS_MORE"}
VERIFY_STATUS = {"VERIFIED", "UNRESOLVED", "CONTRADICTED", "NOT_APPLICABLE"}
MATERIALITY = {"MATERIAL", "CONTEXT", "NON_MATERIAL", "HOLD"}
LINEAGE_ROLES = {"CORE", "BRIDGE", "CONTEXT", "PARALLEL", "COMPETING", "COUNTEREXAMPLE"}
OBLIGATION_STATUS = {"SATISFIED", "LIMITATION", "NEEDS_RESEARCH", "NOT_APPLICABLE"}
WEEKLY_WINDOW_RELATIONS = {"MAIN_EVENT", "PRE_WINDOW_RELEVANCE", "POST_CUTOFF", "CARRY_OVER", "OTHER"}
COMMON_RECORD_FIELDS = {
    "discovery_id", "status", "entity", "artifact_type", "claims",
    "limitations", "verification", "materiality", "materiality_rationale",
    "scope_dimensions",
}
THEMATIC_RECORD_FIELDS = {
    "lineage_role", "branch_ids", "transition_ids", "inheritance_note",
    "historical_attribution_caveat",
}
WEEKLY_RECORD_FIELDS = {"window_relation", "carry_over"}
# Retrospective period semantics are materialized in the Edition View from the
# common materiality/chronology inputs; no Thematic or Weekly-only record
# fields are part of this interactive input contract.
RETROSPECTIVE_RECORD_FIELDS: set[str] = set()


def _rel(repo_root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(repo_root.resolve()))


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any, *, allow_empty: bool = True) -> bool:
    return (
        isinstance(value, list)
        and (allow_empty or bool(value))
        and len(value) == len(set(value))
        and all(_nonempty(item) for item in value)
    )


def _validate_runner(value: Any) -> dict[str, str]:
    if not isinstance(value, dict) or set(value) != {"provider", "model", "invocation", "generated_at"}:
        raise ValueError("interactive Evidence runner fields invalid")
    result: dict[str, str] = {}
    for key in ("provider", "model", "invocation", "generated_at"):
        item = value.get(key)
        if not _nonempty(item):
            raise ValueError(f"interactive Evidence runner.{key} required")
        result[key] = item
    core.parse_instant(result["generated_at"])
    return result


def _validate_record(row: Any, profile: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(row, dict):
        raise ValueError("interactive Evidence record must be an object")
    research_profile = profile.get("research_profile")
    if research_profile == "THEMATIC":
        profile_fields = THEMATIC_RECORD_FIELDS
    elif research_profile == "WEEKLY":
        profile_fields = WEEKLY_RECORD_FIELDS
    elif research_profile == "RETROSPECTIVE_PERIOD":
        profile_fields = RETROSPECTIVE_RECORD_FIELDS
    else:
        raise ValueError(f"unsupported research profile for interactive Evidence: {research_profile!r}")
    required = COMMON_RECORD_FIELDS | profile_fields
    allowed = required | {"source_bindings"}
    if set(row) - allowed or not required.issubset(row):
        raise ValueError(f"interactive Evidence record fields invalid: {row.get('discovery_id')}")
    discovery_id = row.get("discovery_id")
    if not _nonempty(discovery_id):
        raise ValueError("interactive Evidence discovery_id required")
    if row.get("status") not in CARD_STATUS:
        raise ValueError(f"{discovery_id}: invalid Evidence status")

    entity = row.get("entity")
    if not isinstance(entity, dict) or set(entity) != {
        "entity_id", "canonical_name", "entity_type", "organization", "canonical_url"
    }:
        raise ValueError(f"{discovery_id}: entity fields invalid")
    if not _nonempty(entity.get("entity_id")) or not _nonempty(entity.get("canonical_name")):
        raise ValueError(f"{discovery_id}: entity identity required")
    if entity.get("entity_type") not in ENTITY_TYPES:
        raise ValueError(f"{discovery_id}: invalid entity_type")
    if entity.get("organization") is not None and not isinstance(entity.get("organization"), str):
        raise ValueError(f"{discovery_id}: entity.organization must be string/null")
    if entity.get("canonical_url") is not None and not isinstance(entity.get("canonical_url"), str):
        raise ValueError(f"{discovery_id}: entity.canonical_url must be string/null")
    if row.get("artifact_type") not in ARTIFACT_TYPES:
        raise ValueError(f"{discovery_id}: invalid artifact_type")

    claims = row.get("claims")
    if not isinstance(claims, list):
        raise ValueError(f"{discovery_id}: claims must be an array")
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict) or set(claim) != {"text", "evidence_class", "context"}:
            raise ValueError(f"{discovery_id}: claims[{index}] fields invalid")
        if not _nonempty(claim.get("text")) or claim.get("evidence_class") not in EVIDENCE_CLASSES:
            raise ValueError(f"{discovery_id}: claims[{index}] invalid")
        if claim.get("context") is not None and not isinstance(claim.get("context"), str):
            raise ValueError(f"{discovery_id}: claims[{index}].context must be string/null")

    limitations = row.get("limitations")
    if not _string_list(limitations):
        raise ValueError(f"{discovery_id}: limitations must be a unique string array")

    verification = row.get("verification")
    if not isinstance(verification, list):
        raise ValueError(f"{discovery_id}: verification must be an array")
    targets: set[str] = set()
    for index, item in enumerate(verification):
        if not isinstance(item, dict) or set(item) != {"target", "status", "finding"}:
            raise ValueError(f"{discovery_id}: verification[{index}] fields invalid")
        if not _nonempty(item.get("target")) or item["target"] in targets:
            raise ValueError(f"{discovery_id}: invalid/duplicate verification target")
        targets.add(item["target"])
        if item.get("status") not in VERIFY_STATUS or not _nonempty(item.get("finding")):
            raise ValueError(f"{discovery_id}: verification[{index}] invalid")

    if row.get("materiality") not in MATERIALITY or not _nonempty(row.get("materiality_rationale")):
        raise ValueError(f"{discovery_id}: materiality invalid")
    if row["status"] == "REJECTED" and row["materiality"] != "NON_MATERIAL":
        raise ValueError(f"{discovery_id}: REJECTED Evidence must be NON_MATERIAL")
    if row["status"] == "NEEDS_MORE" and row["materiality"] != "HOLD":
        raise ValueError(f"{discovery_id}: NEEDS_MORE Evidence must be HOLD")
    if "source_bindings" in row and not _string_list(row["source_bindings"], allow_empty=False):
        raise ValueError(f"{discovery_id}: source_bindings must be a unique non-empty string array")
    if research_profile == "WEEKLY":
        if not _nonempty(row["window_relation"]):
            raise ValueError(f"{discovery_id}: window_relation must be a non-empty string")
        if row["window_relation"] not in WEEKLY_WINDOW_RELATIONS:
            raise ValueError(f"{discovery_id}: window_relation is not a valid Weekly relation")
        if not isinstance(row["carry_over"], bool):
            raise ValueError(f"{discovery_id}: carry_over must be boolean")

    allowed_dims = set(profile["research_scope"]["scope_dimensions"])
    dims = row.get("scope_dimensions")
    if not _string_list(dims) or any(item not in allowed_dims for item in dims):
        raise ValueError(f"{discovery_id}: scope_dimensions invalid")
    if research_profile == "THEMATIC":
        if row.get("lineage_role") not in LINEAGE_ROLES:
            raise ValueError(f"{discovery_id}: invalid lineage_role")
        for key in ("branch_ids", "transition_ids"):
            if not _string_list(row.get(key)):
                raise ValueError(f"{discovery_id}: {key} invalid")
        for key in ("inheritance_note", "historical_attribution_caveat"):
            if row.get(key) is not None and not isinstance(row.get(key), str):
                raise ValueError(f"{discovery_id}: {key} must be string/null")
    return row


def _validate_completeness_input(
    value: Any,
    profile: dict[str, Any],
    *,
    discovery_records: list[dict[str, Any]],
    root_discovery_records: list[dict[str, Any]],
) -> dict[str, Any]:
    # Required keyword-only validated R/E inputs inside the checked operation.
    # They are validation inputs, not public authority tokens. None refuses.
    if discovery_records is None or root_discovery_records is None:
        raise ValueError("interactive Completeness requires validated discovery_records and root_discovery_records")
    if not isinstance(discovery_records, list) or not isinstance(root_discovery_records, list):
        raise ValueError("interactive Completeness discovery_records/root_discovery_records must be validated record lists")
    if not isinstance(value, dict) or set(value) != {"obligations", "residual_limitations", "closure"}:
        raise ValueError("interactive Completeness fields invalid")
    # DM016 early admission: canonical classification on every validated
    # root/effective record including prospective DROP rows. No
    # type-eligibility shortcut. Canonical table is owned by A in
    # survey_evidence_v2; this runner only consumes the leaf.
    for _rec in list(root_discovery_records) + list(discovery_records):
        if not isinstance(_rec, dict):
            raise ValueError("interactive Completeness Discovery record invalid")
        _source = _rec.get("source")
        if not isinstance(_source, dict):
            raise ValueError("interactive Completeness Discovery source invalid")
        evidence._source_class(_source.get("source_type"))
    # DM017 declaration preservation: every (parent,OID) carrier check.
    # Helper is owned by A in survey_screening_v2; exact precode names only.
    _uncovered = screening.find_declaration_loss(root_discovery_records, discovery_records)
    if _uncovered:
        raise ValueError(f"DECLARATION_LOSS uncovered={_uncovered}")
    try:
        _initial_rows = profile["research_scope"]["initial_obligations"]
    except (KeyError, TypeError) as exc:
        raise ValueError("Production Profile initial_obligations missing") from exc
    _profile_initial_ids = {row["obligation_id"] for row in _initial_rows if isinstance(row, dict)}
    _universe: set[str] = screening.compute_obligation_universe(
        _profile_initial_ids, root_discovery_records, discovery_records
    )
    try:
        _allowed_dimensions = set(profile["research_scope"]["scope_dimensions"])
    except (KeyError, TypeError) as exc:
        raise ValueError("Production Profile scope_dimensions missing") from exc
    obligations = value.get("obligations")
    if not isinstance(obligations, list):
        raise ValueError("interactive Completeness obligations must be an array")
    by_id: dict[str, dict[str, Any]] = {}
    for row in obligations:
        if not isinstance(row, dict):
            raise ValueError("interactive Completeness obligation fields invalid")
        oid = row.get("obligation_id")
        if not _nonempty(oid) or oid in by_id:
            raise ValueError(f"invalid/duplicate Completeness obligation: {oid!r}")
        if oid in _profile_initial_ids:
            # Initial IDs: exactly 3 fields from Profile semantics.
            # Five fields on a Profile-initial ID refuses (no redefinition).
            if set(row) != {"obligation_id", "status", "rationale"}:
                raise ValueError(f"Profile-initial obligation must use exact 3 fields, no redefinition: {oid}")
        elif oid in _universe:
            # Named-only U-P: exactly 5 fields with operator-supplied semantics.
            if set(row) != {"obligation_id", "status", "rationale", "dimension", "description"}:
                raise ValueError(f"named-only obligation must use exact 5 fields: {oid}")
            if row.get("dimension") not in _allowed_dimensions:
                raise ValueError(f"Completeness obligation {oid} dimension is not Profile-declared")
            if not _nonempty(row.get("description")):
                raise ValueError(f"Completeness obligation {oid} description missing")
        else:
            raise ValueError(f"interactive Completeness obligation not in universe U: {oid!r}")
        if row.get("status") not in OBLIGATION_STATUS or not _nonempty(row.get("rationale")):
            raise ValueError(f"Completeness obligation invalid: {oid}")
        by_id[oid] = row
    if set(by_id) != set(_universe):
        raise ValueError(
            f"interactive Completeness must cover exact universe U: missing={sorted(set(_universe)-set(by_id))} extra={sorted(set(by_id)-set(_universe))}"
        )
    residual = value.get("residual_limitations")
    if not _string_list(residual):
        raise ValueError("interactive Completeness residual_limitations invalid")
    closure = value.get("closure")
    required_closure = {
        "targeted_gap_fill_completed", "limitations", "status"
    }
    if profile["research_profile"] == "THEMATIC":
        if not isinstance(closure, dict) or set(closure) != required_closure:
            raise ValueError("interactive Thematic closure fields invalid")
        if not isinstance(closure.get("targeted_gap_fill_completed"), bool):
            raise ValueError("interactive Thematic targeted_gap_fill_completed must be boolean")
        if not _string_list(closure.get("limitations")):
            raise ValueError("interactive Thematic closure limitations invalid")
        if closure.get("status") not in {"COMPLETE", "LIMITED", "NEEDS_RESEARCH"}:
            raise ValueError("interactive Thematic closure status invalid")
    elif closure is not None:
        raise ValueError("non-Thematic interactive Completeness closure must be null")
    return value


def validate_interactive_input(
    value: dict[str, Any],
    profile: dict[str, Any],
    expected_ids: set[str],
    task_source_ids: dict[str, set[str]] | None = None,
    *,
    discovery_records: list[dict[str, Any]],
    root_discovery_records: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, str], dict[str, Any]]:
    if discovery_records is None or root_discovery_records is None:
        raise ValueError("interactive Evidence requires validated discovery_records and root_discovery_records")
    if not isinstance(discovery_records, list) or not isinstance(root_discovery_records, list):
        raise ValueError("interactive Evidence discovery_records/root_discovery_records must be validated record lists")
    if set(value) != {"schema_version", "issue_id", "runner", "records", "completeness"}:
        raise ValueError("interactive Evidence input fields invalid")
    if value.get("schema_version") != "2.0-rc1" or value.get("issue_id") != profile["issue_id"]:
        raise ValueError("interactive Evidence input identity mismatch")
    runner = _validate_runner(value.get("runner"))
    rows = value.get("records")
    if not isinstance(rows, list):
        raise ValueError("interactive Evidence records must be an array")
    by_id: dict[str, dict[str, Any]] = {}
    for raw in rows:
        row = _validate_record(raw, profile)
        did = row["discovery_id"]
        if did in by_id:
            raise ValueError(f"duplicate interactive Evidence discovery_id: {did}")
        if task_source_ids is not None:
            allowed = task_source_ids.get(did)
            if allowed is None:
                raise ValueError(f"{did}: interactive Evidence task source authority is missing")
            bindings = row.get("source_bindings")
            if bindings is None:
                if len(allowed) > 1:
                    raise ValueError(
                        f"{did}: source_bindings is required when multiple task-bound sources exist"
                    )
            elif not set(bindings).issubset(allowed):
                raise ValueError(f"{did}: source_bindings contains an unbound task source")
        by_id[did] = row
    if set(by_id) != expected_ids:
        raise ValueError(
            f"interactive Evidence records must cover exact non-DROP Discovery IDs: missing={sorted(expected_ids-set(by_id))} extra={sorted(set(by_id)-expected_ids)}"
        )
    completeness_input = _validate_completeness_input(
        value.get("completeness"),
        profile,
        discovery_records=discovery_records,
        root_discovery_records=root_discovery_records,
    )
    return by_id, runner, completeness_input


def _build_card(
    repo_root: Path,
    task: dict[str, Any],
    meta: dict[str, Any],
    package: dict[str, Any],
    record: dict[str, Any],
    runner: dict[str, str],
) -> dict[str, Any]:
    """Public reload wrapper delegating to ONE canonical core (no third copy)."""
    source_authorities = evidence.task_authority_sources(repo_root, task, package)
    return evidence._build_card_core(task, meta, package, record, runner, source_authorities)


def _build_view(profile: dict[str, Any], task_id: str, evidence_sha: str, record: dict[str, Any]) -> dict[str, Any]:
    annotations: dict[str, Any]
    if profile["research_profile"] == "THEMATIC":
        annotations = {
            "lineage_role": record["lineage_role"],
            "branch_ids": list(record["branch_ids"]),
            "transition_ids": list(record["transition_ids"]),
            "inheritance_note": record["inheritance_note"],
            "historical_attribution_caveat": record["historical_attribution_caveat"],
        }
    elif profile["research_profile"] == "WEEKLY":
        annotations = {
            "why_this_issue": record["materiality_rationale"],
            "window_relation": record.get("window_relation", "MAIN_EVENT"),
            "carry_over": bool(record.get("carry_over", False)),
        }
    elif profile["research_profile"] == "RETROSPECTIVE_PERIOD":
        annotations = {
            "period_role": record["materiality_rationale"],
            "chronology_relevance": record["materiality"] != "NON_MATERIAL",
        }
    else:
        raise ValueError("unsupported research profile for interactive Edition View")
    return {
        "schema_version": "2.0-rc1",
        "issue_id": profile["issue_id"],
        "research_profile": profile["research_profile"],
        "evidence_task_id": task_id,
        "evidence_sha256": evidence_sha,
        "materiality": {
            "status": record["materiality"],
            "rationale": record["materiality_rationale"],
        },
        "scope_dimensions": list(record["scope_dimensions"]),
        "profile_annotations": annotations,
    }


def _build_completeness(
    repo_root: Path,
    profile: dict[str, Any],
    profile_path: Path,
    discovery_records: list[dict[str, Any]],
    ledger_path: Path,
    ledger: dict[str, Any],
    input_value: dict[str, Any],
) -> dict[str, Any]:
    # Tuple kept per precode map. Final 7 fields are internally derived from
    # effective declarations and exact Ledger rows. No OLD completeness, no
    # child rewrite/autofill/status promotion. DROP produces no invented tasks
    # because the Ledger has no rows for DROP DIDs.
    by_input = {row["obligation_id"]: row for row in input_value["obligations"]}
    ledger_task_by_discovery = {
        row["discovery_id"]: list(row["evidence_task_ids"])
        for row in ledger["rows"]
    }
    _initial_rows = profile["research_scope"]["initial_obligations"]
    _initial_by_id = {row["obligation_id"]: row for row in _initial_rows if isinstance(row, dict)}
    _initial_order = [row["obligation_id"] for row in _initial_rows if isinstance(row, dict) and row.get("obligation_id") in by_input]
    _extra = sorted(oid for oid in by_input if oid not in _initial_by_id)
    _ordered = [oid for oid in _initial_order if oid in by_input] + _extra
    if set(_ordered) != set(by_input):
        raise ValueError("Completeness builder input must cover exact validated obligations")
    obligations: list[dict[str, Any]] = []
    for oid in _ordered:
        # Single-home derivation owned by A in Screening; no duplicate policy
        # here. Includes DROP declarers in discovery_ids with no invented tasks.
        declaring, task_ids = screening.derive_bindings(
            oid, discovery_records, ledger_task_by_discovery
        )
        decision = by_input[oid]
        if oid in _initial_by_id:
            _initial = _initial_by_id[oid]
            obligations.append({
                "obligation_id": oid,
                "dimension": _initial["dimension"],
                "description": _initial["description"],
                "status": decision["status"],
                "discovery_ids": declaring,
                "evidence_task_ids": task_ids,
                "rationale": decision["rationale"],
            })
        else:
            obligations.append({
                "obligation_id": oid,
                "dimension": decision["dimension"],
                "description": decision["description"],
                "status": decision["status"],
                "discovery_ids": declaring,
                "evidence_task_ids": task_ids,
                "rationale": decision["rationale"],
            })

    needs_research = sum(row["status"] == "NEEDS_RESEARCH" for row in obligations)
    residual = list(input_value["residual_limitations"])
    limitations = [row for row in obligations if row["status"] == "LIMITATION"]
    overall = "INCOMPLETE" if needs_research else ("LIMITED" if limitations or residual else "READY")

    closure_input = input_value["closure"]
    closure = None
    if profile["research_profile"] == "THEMATIC":
        max_pass = max(
            (row.get("provenance", {}).get("research_pass", 0) for row in discovery_records),
            default=0,
        )
        final_records = [
            row for row in discovery_records
            if max_pass > 0 and row.get("provenance", {}).get("research_pass") == max_pass
        ]
        obligation_status = {row["obligation_id"]: row["status"] for row in obligations}
        final_ids = {
            oid for row in final_records
            for oid in row.get("provenance", {}).get("obligation_ids", [])
            if oid in obligation_status
        }
        material_ids = {
            oid for oid in final_ids
            if obligation_status[oid] in {"SATISFIED", "LIMITATION", "NEEDS_RESEARCH"}
        }
        open_ids = {oid for oid in material_ids if obligation_status[oid] == "NEEDS_RESEARCH"}
        # Closure-first stable union of residual limitations (normal builder
        # owns parity; byte-exactly as agent-first adapter). 4 provenance/
        # status-derived counters + 1 row-status count + 3 operator-fed fields.
        # No judgment automation: status/targeted_gap_fill_completed are copied
        # from validated operator input; downstream validators enforce cross-
        # checks including residual-subset preservation.
        _normalized = list(closure_input["limitations"])
        for _limitation in residual:
            if _limitation not in _normalized:
                _normalized.append(_limitation)
        closure = {
            "expansion_passes": max(1, max_pass),
            "final_pass_new_sources": len(final_records),
            "final_pass_new_material_obligations": len(material_ids),
            "final_pass_new_material_obligations_open": len(open_ids),
            "targeted_gap_fill_completed": closure_input["targeted_gap_fill_completed"],
            "open_material_obligations": needs_research,
            "limitations": _normalized,
            "status": closure_input["status"],
        }

    return {
        "schema_version": "2.0-rc1",
        "issue_id": profile["issue_id"],
        "research_profile": profile["research_profile"],
        "basis": {
            "production_profile_sha256": core.sha256_file(profile_path),
            "materiality_ledger_sha256": core.sha256_file(ledger_path),
        },
        "overall_status": overall,
        "obligations": obligations,
        "residual_limitations": residual,
        "closure": closure,
    }


def _archive_input(repo_root: Path, evidence_acceptance_path: Path, input_path: Path, runner: dict[str, str], outputs: dict[str, str]) -> dict[str, Any]:
    run_dir = evidence_acceptance_path.parent
    archived = run_dir / INPUT_NAME
    if archived.exists():
        if core.sha256_file(archived) != core.sha256_file(input_path):
            raise ValueError("accepted Evidence run has conflicting interactive input bytes")
    else:
        shutil.copy2(input_path, archived)
    audit = {
        "schema_version": "2.0-rc1",
        "issue_id": core.load_json(evidence_acceptance_path)["issue_id"],
        "interactive_input": {"path": _rel(repo_root, archived), "sha256": core.sha256_file(archived)},
        "runner": runner,
        "outputs": outputs,
    }
    audit_path = run_dir / AUDIT_NAME
    if audit_path.exists():
        if core.load_json(audit_path) != audit:
            raise ValueError("accepted Evidence run has conflicting interactive audit bytes")
    else:
        core.write_json(audit_path, audit)
    return audit


def run(
    repo_root: Path,
    state_path: Path,
    input_path: Path,
    supplement_manifest_path: Path | None = None,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    state_path = state_path.resolve()
    input_path = input_path.resolve()
    if supplement_manifest_path is not None:
        supplement_manifest_path = supplement_manifest_path.resolve()
    cfg = core.load_json(repo_root / core.DEFAULT_CONFIG)
    state = core.load_json(state_path)
    errors = agent.validate_agent_state(repo_root, cfg, state)
    if errors:
        raise ValueError("Production State invalid before interactive Evidence: " + "; ".join(errors))
    if state.get("lifecycle_state") != "CANDIDATES_NORMALIZED":
        raise ValueError("interactive Evidence requires CANDIDATES_NORMALIZED Production State")

    profile_path = repo_root / state["profile"]["path"]
    profile = core.load_json(profile_path)
    source_root = core.repo_local_path(repo_root, profile["paths"]["source_root"], "paths.source_root")
    # DM022 READY entry + supersession refusal: normal CANDIDATES path requires
    # guard absence; when the State triplet classifies as PREARCH, this normal
    # runner refuses (versioned R outputs are HIGH-only, no fabricated
    # CANDIDATES_NORMALIZED pretense, no synthetic State).
    _dm022_require_ready(repo_root, state_path)
    _prov = state.get("checkpoint_provenance", {})
    _refs = [_prov.get(n) for n in ("evidence", "materiality", "completeness")]
    if all(isinstance(r, dict) and set(r) == {"path", "sha256"} for r in _refs):
        if len({(r["path"], r["sha256"]) for r in _refs}) == 1:
            _ev = _prov.get("evidence")
            _fam = low.load_typed_checkpoint_record(repo_root, repo_root / str(_ev["path"]))
            if isinstance(_fam, dict) and _fam.get("family") == "PREARCH":
                raise ValueError("DM022_WRONG_FAMILY: normal Evidence runner refuses in supersession mode (HIGH R writers only)")
    discovery_acceptance_path = source_root / "discovery/discovery-accepted-v2.json"
    accepted_discovery = discovery.validate_acceptance(repo_root, discovery_acceptance_path)
    root_discovery_path = core.repo_local_path(repo_root, accepted_discovery["discovery_path"], "accepted Discovery JSONL")

    implementation_sha = core.repository_commit_sha(repo_root)
    active_screening = screening.resolve_active_screening_acceptance(
        repo_root, state_path, implementation_sha
    )
    screening_acceptance_path = active_screening["path"]
    effective = screening.resolve_effective_discovery_basis(
        repo_root,
        screening_acceptance_path.parent / "package.json",
        implementation_sha,
        accepted_root_path=root_discovery_path,
    )
    discovery_path = effective["path"]
    discovery_records = effective["records"]
    # Resolver contract always carries validated root_records; require the
    # actual field and reject an invalid resolver result. No E-as-R fallback.
    # Legitimate DIRECT already carries explicit identical root bytes.
    if "root_records" not in effective:
        raise ValueError("effective Discovery basis missing validated root_records")
    root_records = effective["root_records"]
    if not isinstance(root_records, list) or not root_records:
        raise ValueError("effective Discovery basis root_records invalid")
    if not isinstance(discovery_records, list) or not discovery_records:
        raise ValueError("effective Discovery basis records invalid")
    # N1 ordinary preflight AFTER validated actual R/E resolution but BEFORE
    # ordinary temp/owned package writes. Uses in-memory input doc and actual
    # canonical/hash-bound JSONL records, not compact summaries or caller sets.
    # Later task-dependent record validation stays after package creation with
    # the real generated task universe; no dummy task universe workaround.
    interactive_doc = core.load_json(input_path)
    _validate_completeness_input(
        interactive_doc.get("completeness"),
        profile,
        discovery_records=discovery_records,
        root_discovery_records=root_records,
    )
    with tempfile.TemporaryDirectory() as temp:
        temp_root = Path(temp)
        package_root = temp_root / "evidence-package"
        with agent_tool.current_stage_basis_override():
            package_path = evidence.prepare_evidence_package(
                repo_root,
                state_path,
                discovery_path,
                screening_acceptance_path,
                package_root,
                implementation_sha,
                supplement_manifest_path,
            )
        package = core.load_json(package_path)
        task_meta = {meta["discovery_ids"][0]: meta for meta in package["tasks"]}
        expected_ids = set(task_meta)
        # Pre-accept phase context: one full supplement validation
        # (package-linear), then pure per-task slices. No per-task reload.
        # Screening validation requires the strict facade (real CAND).
        with agent_tool.current_stage_basis_override():
            _run_screening, _, _run_discoveries = evidence.validate_screening_acceptance(
                repo_root,
                screening_acceptance_path,
                discovery_path,
                profile["issue_id"],
                implementation_sha,
            )
            _run_ctx = evidence._resolve_phase_supplement_context(
                repo_root,
                package,
                implementation_sha=implementation_sha,
                screening_acceptance=_run_screening,
                discoveries=_run_discoveries,
            )
        # Phase pins for owned temp package/tasks (temp allowed).
        _run_pin_paths: list[tuple[str, Path]] = [("Evidence package", package_path)]
        for _meta in package["tasks"]:
            _run_pin_paths.append((f"Evidence Task {_meta['evidence_task_id']}", package_path.parent / _meta["path"]))
        _run_pins = evidence._capture_phase_pins(tuple(_run_pin_paths))
        task_source_ids = {}
        for did, meta in task_meta.items():
            _task_obj = core.load_json(package_path.parent / meta["path"])
            # Pure helpers: Discovery-first, then supplement slice (no IO).
            _base = evidence._discovery_task_sources(_task_obj)
            _merged = evidence._merge_supplement_task_sources(_base, _task_obj, _run_ctx["entries"])
            task_source_ids[did] = set(_merged)
        records_by_id, runner, completeness_input = validate_interactive_input(
            interactive_doc,
            profile,
            expected_ids,
            task_source_ids,
            discovery_records=discovery_records,
            root_discovery_records=root_records,
        )

        results_dir = temp_root / "evidence-results"
        results_dir.mkdir()
        for did in sorted(task_meta):
            meta = task_meta[did]
            task = core.load_json(package_path.parent / meta["path"])
            _batch_auth = evidence._merge_supplement_task_sources(
                evidence._discovery_task_sources(task), task, _run_ctx["entries"]
            )
            card = evidence._build_card_core(task, meta, package, records_by_id[did], runner, _batch_auth)

            def _batch_validate(_task: dict[str, Any] = task) -> dict[str, dict[str, Any]]:
                _b = evidence._discovery_task_sources(_task)
                return evidence._merge_supplement_task_sources(_b, _task, _run_ctx["entries"])

            errors = evidence._validate_card_core(card, task, meta["sha256"], package, _batch_validate)
            if errors:
                raise ValueError(f"interactive Evidence Card {did} invalid: {'; '.join(errors)}")
            core.write_json(results_dir / Path(meta["path"]).name, card)
        # Finish pre-accept phase with role-correct owner (package-basis/current,
        # non-recursive) before discard; no cross-phase reuse.
        def _revalidate_run_owner() -> None:
            evidence.validate_evidence_package_basis(repo_root, package_path, package, implementation_sha)

        evidence._finish_authority_phase(repo_root, _run_ctx, _run_pins, revalidate_owner=_revalidate_run_owner)
        # Discard pre-accept context before canonical accept (no cross-phase reuse).
        _run_ctx = None  # type: ignore[assignment]

        evidence_root = source_root / "evidence/v2/accepted"
        # DM022 prepublish: full readiness immediately before the canonical
        # Evidence acceptance write (late guard after entry must refuse here).
        _dm022_require_ready(repo_root, state_path)
        with agent_tool.current_stage_basis_override():
            evidence_acceptance_path = evidence.accept_evidence_results(
                repo_root,
                package_path,
                results_dir,
                evidence_root,
                implementation_sha,
            )
            evidence_acceptance, _ = evidence.validate_evidence_acceptance(
                repo_root, evidence_acceptance_path, implementation_sha
            )

        evidence_by_task = {
            row["evidence_task_id"]: row for row in evidence_acceptance["results"]
        }
        views_dir = temp_root / "views"
        views_dir.mkdir()
        for did in sorted(task_meta):
            meta = task_meta[did]
            task_id = meta["evidence_task_id"]
            entry = evidence_by_task[task_id]
            view = _build_view(profile, task_id, entry["sha256"], records_by_id[did])
            errors = evidence.validate_edition_view(
                view, profile, entry["sha256"], entry["status"]
            )
            if errors:
                raise ValueError(f"interactive Edition View {did} invalid: {'; '.join(errors)}")
            core.write_json(views_dir / evidence.view_filename(task_id), view)

        views_root = source_root / "evidence/v2/views/accepted"
        # DM022 prepublish: full readiness immediately before the canonical
        # Edition Views acceptance write.
        _dm022_require_ready(repo_root, state_path)
        with agent_tool.current_stage_basis_override():
            views_acceptance_path = evidence.accept_edition_views(
                repo_root,
                profile_path,
                evidence_acceptance_path,
                views_dir,
                views_root,
                implementation_sha,
            )
            evidence.validate_edition_views_acceptance(
                repo_root,
                profile_path,
                evidence_acceptance_path,
                views_acceptance_path,
                implementation_sha,
            )

        ledger_path = source_root / "materiality-ledger-v2.json"
        # DM022 prepublish: canonical Ledger creation while the guard is held
        # refuses; versioned R outputs are HIGH-only.
        _dm022_require_ready(repo_root, state_path)
        if ledger_path.exists() or ledger_path.is_symlink():
            raise ValueError(f"refusing to overwrite Materiality Ledger: {ledger_path}")
        _ledger_pins = evidence._capture_phase_pins(
            (
                ("Materiality profile", profile_path),
                ("Materiality discovery", discovery_path),
                ("Materiality screening acceptance", screening_acceptance_path),
                ("Materiality evidence acceptance", evidence_acceptance_path),
                ("Materiality views acceptance", views_acceptance_path),
                ("Materiality current State", state_path),
            )
        )
        with agent_tool.current_stage_basis_override():
            ledger = evidence.build_materiality_ledger(
                repo_root,
                profile_path,
                discovery_path,
                screening_acceptance_path,
                evidence_acceptance_path,
                views_acceptance_path,
                implementation_sha,
            )
        for _pin in _ledger_pins:
            evidence._assert_pin_repo_ancestors(repo_root, _pin)
        evidence._recheck_phase_pins(_ledger_pins)
        evidence.write_materiality_ledger(ledger_path, ledger)

        completeness_path = source_root / "profile-completeness-v2.json"
        _dm022_require_ready(repo_root, state_path)
        if completeness_path.exists() or completeness_path.is_symlink():
            raise ValueError(f"refusing to overwrite Profile Completeness: {completeness_path}")
        _comp_pins = evidence._capture_phase_pins(
            (
                ("Completeness profile", profile_path),
                ("Completeness discovery", discovery_path),
                ("Completeness screening acceptance", screening_acceptance_path),
                ("Completeness evidence acceptance", evidence_acceptance_path),
                ("Completeness views acceptance", views_acceptance_path),
                ("Completeness ledger", ledger_path),
                ("Completeness current State", state_path),
            )
        )
        result = _build_completeness(
            repo_root,
            profile,
            profile_path,
            discovery_records,
            ledger_path,
            ledger,
            completeness_input,
        )
        schema_gate.validate_instance(
            result,
            repo_root / "schemas/profile-completeness-result.schema.json",
            label="Profile Completeness",
        )
        with agent_tool.current_stage_basis_override():
            errors = completeness.validate_profile_completeness(
                result,
                repo_root,
                profile_path,
                discovery_path,
                screening_acceptance_path,
                evidence_acceptance_path,
                views_acceptance_path,
                ledger_path,
                implementation_sha,
            )
        if errors:
            raise ValueError("Profile Completeness invalid: " + "; ".join(errors))
        for _pin in _comp_pins:
            evidence._assert_pin_repo_ancestors(repo_root, _pin)
        evidence._recheck_phase_pins(_comp_pins)
        core.write_json(completeness_path, result)

    outputs = {
        "evidence_acceptance": _rel(repo_root, evidence_acceptance_path),
        "edition_views_acceptance": _rel(repo_root, views_acceptance_path),
        "materiality_ledger": _rel(repo_root, ledger_path),
        "profile_completeness": _rel(repo_root, completeness_path),
    }
    # DM022 prepublish: full readiness immediately before the canonical
    # archive/audit writes.
    _dm022_require_ready(repo_root, state_path)
    # Archive phase: NEW phase bound to actual accepted package copy (temp
    # lifetime already closed). Full Raw/owner validation, not pins only.
    _accepted_pkg_copy = evidence_acceptance_path.parent / "package.json"
    with agent_tool.current_stage_basis_override():
        _arch_acc, _arch_pkg = evidence.validate_evidence_acceptance(
            repo_root, evidence_acceptance_path, implementation_sha
        )
        _arch_screening, _, _arch_discs = evidence.validate_screening_acceptance(
            repo_root,
            repo_root / _arch_pkg["basis"]["screening_acceptance_path"],
            repo_root / _arch_pkg["basis"]["discovery_path"],
            _arch_pkg["issue_id"],
            implementation_sha,
        )
        _arch_ctx = evidence._resolve_phase_supplement_context(
            repo_root, _arch_pkg, implementation_sha=implementation_sha,
            screening_acceptance=_arch_screening, discoveries=_arch_discs,
        )
    _archive_pins = evidence._capture_phase_pins(
        (
            ("Evidence acceptance", evidence_acceptance_path),
            ("Accepted Evidence package copy", _accepted_pkg_copy),
            ("Interactive input", input_path),
        )
    )

    def _revalidate_archive_owner() -> None:
        evidence.validate_evidence_acceptance(repo_root, evidence_acceptance_path, implementation_sha)

    evidence._finish_authority_phase(
        repo_root, _arch_ctx, _archive_pins, revalidate_owner=_revalidate_archive_owner
    )
    _archive_input(repo_root, evidence_acceptance_path, input_path, runner, outputs)
    evidence._finish_authority_phase(
        repo_root, _arch_ctx, _archive_pins, revalidate_owner=_revalidate_archive_owner
    )
    return {
        **outputs,
        "evidence_result_count": core.load_json(evidence_acceptance_path)["result_count"],
        "completeness_status": core.load_json(completeness_path)["overall_status"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--state", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--supplement")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    state = Path(args.state)
    input_path = Path(args.input)
    if not state.is_absolute():
        state = root / state
    if not input_path.is_absolute():
        input_path = root / input_path
    supplement_path = Path(args.supplement) if args.supplement else None
    if supplement_path is not None and not supplement_path.is_absolute():
        supplement_path = root / supplement_path
    try:
        print(json.dumps(run(root, state, input_path, supplement_path), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=__import__("sys").stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
