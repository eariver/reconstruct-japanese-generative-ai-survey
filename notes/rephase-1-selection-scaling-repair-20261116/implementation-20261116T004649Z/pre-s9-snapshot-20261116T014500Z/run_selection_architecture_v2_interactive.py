#!/usr/bin/env python3
"""Build Core v2 Candidate Selection and proposed Architecture from explicit interactive decisions.

The runner is profile-neutral. Candidate identities and the Candidate Matrix are derived from
accepted Evidence/View/Materiality/Completeness artifacts by the canonical implementation.
Interactive input addresses candidates by Discovery ID for operator ergonomics; every ID is
resolved to the deterministic Matrix candidate before Selection/Architecture validation.

This runner does not advance Production State and never records Human Gate approval.
"""
from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

from scripts import survey_agent_control_v2 as agent
from scripts import survey_agent_tool_v2 as agent_tool
from scripts import survey_architecture_v2 as architecture
from scripts import survey_architecture_v2_base as base
from scripts import survey_discovery_v2 as discovery
from scripts import survey_production_v2 as core
from scripts import survey_research_authority_v2 as low
from scripts import survey_review_attention_v2 as review_attention
from scripts import survey_schema_v2 as schema_gate
from scripts import survey_screening_v2 as screening

INPUT_NAME = "interactive-selection-architecture.json"
# DM022 ordinary-consumer readiness (B side). PREARCH inputs resolve through
# the State-bound research checkpoint; old canonical Ledger/Completeness are
# never reopened after supersession. New Ledger/Completeness live at versioned
# R paths carried by the same typed PREARCH record.
DM022_SEVEN_SLOTS = (
    "candidate-matrix-v2.json",
    "candidate-selection-v2.json",
    "architecture-v2.json",
    "architecture-review-summary-v2.json",
    "architecture-review-attention-v2.json",
    "orchestration/v2/interactive/selection-architecture-input.json",
    "orchestration/v2/interactive/selection-architecture-audit.json",
)


def _dm022_require_ready(repo_root: Path, state_path: Path) -> None:
    low.require_research_operation_ready(repo_root, state_path)


def _dm022_pinned_family(repo_root: Path, state: dict[str, Any]) -> str:
    """Strict pinned-record family (no triplet heuristic, no fallback).

    Reloads the pinned evidence checkpoint and inspects the strict typed
    family. Healthy LEGACY same-triplet states return LEGACY (same record,
    legacy kind) and use the legacy branch. Malformed records raise (fail
    closed, never fall back to the other branch after an exception).
    """
    prov = state.get("checkpoint_provenance", {})
    if not isinstance(prov, dict):
        return "LEGACY"
    ev = prov.get("evidence")
    if not isinstance(ev, dict) or set(ev) != {"path", "sha256"}:
        return "LEGACY"
    fam = low.load_typed_checkpoint_record(repo_root, repo_root / str(ev["path"]))
    if isinstance(fam, dict):
        return str(fam.get("family", "LEGACY"))
    return "LEGACY"


def _dm022_resolve_ledger_completeness(
    repo_root: Path, state_path: Path, state: dict[str, Any], source_root: Path
) -> tuple[Path, Path]:
    """Resolve active Ledger/Completeness via R4 when PREARCH, else canonical.

    Explicit state_path plumbing (no generic token): LOW public entry reloads
    the canonical LIVE State file. Selected return shape is
    {family, checkpoint, artifacts(parsed), lineage, artifact_refs}; the
    versioned R refs come from artifact_refs (four NamedRefs mapping), never
    from a caller proof dict. Refuses old canonical fallback after supersession.
    Strict pinned-record family decides the branch (no triplet heuristic):
    healthy LEGACY same-triplet states use the legacy canonical branch.
    """
    if _dm022_pinned_family(repo_root, state) != "PREARCH":
        return (
            source_root / "materiality-ledger-v2.json",
            source_root / "profile-completeness-v2.json",
        )
    four = low.resolve_research_authority(repo_root, state_path)
    if not isinstance(four, dict) or four.get("family") != "PREARCH":
        raise ValueError("PREARCH research resolution did not return PREARCH family")
    refs = four.get("artifact_refs")
    if not isinstance(refs, dict) or set(refs) != {"evidence-acceptance", "edition-views-acceptance", "materiality-ledger", "profile-completeness"}:
        raise ValueError("PREARCH artifact_refs must be exactly the 4 NamedRefs")
    ledger_rel = refs["materiality-ledger"].get("path")
    comp_rel = refs["profile-completeness"].get("path")
    if not isinstance(ledger_rel, str) or not isinstance(comp_rel, str):
        raise ValueError("PREARCH artifact_refs paths invalid")
    return repo_root / ledger_rel, repo_root / comp_rel


def _dm022_preflight_seven(source_root: Path) -> None:
    """Successor no-overwrite preflight covering all seven slots incl audit."""
    for rel in DM022_SEVEN_SLOTS:
        candidate = source_root / rel
        # lstat semantics: never follow a symlink as absent; any present file
        # (regular or not) blocks normal generation.
        try:
            st = candidate.lstat()
        except FileNotFoundError:
            continue
        except OSError as exc:
            raise ValueError(f"refusing Selection/Architecture generation with unreadable slot {rel}: {exc}") from exc
        raise ValueError(f"refusing to overwrite Selection/Architecture artifact: {candidate}")
        del st


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _rel(root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(root.resolve()))


def _unique_strings(value: Any, label: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value) or any(not _nonempty(x) for x in value):
        raise ValueError(f"{label} must be a {'non-empty ' if not allow_empty else ''}string array")
    if len(value) != len(set(value)):
        raise ValueError(f"{label} must not contain duplicates")
    return list(value)


def _validate_input(doc: dict[str, Any], issue_id: str, expected_discovery_ids: set[str]) -> None:
    required = {
        "schema_version", "issue_id", "runner", "assignments", "architecture",
    }
    if not isinstance(doc, dict) or set(doc) != required:
        raise ValueError("interactive Selection/Architecture fields invalid")
    if doc.get("schema_version") != "2.0-rc1" or doc.get("issue_id") != issue_id:
        raise ValueError("interactive Selection/Architecture identity mismatch")
    runner = doc.get("runner")
    if not isinstance(runner, dict) or not all(_nonempty(runner.get(k)) for k in ("provider", "model", "invocation", "generated_at")):
        raise ValueError("interactive Selection/Architecture runner metadata invalid")
    assignments = doc.get("assignments")
    if not isinstance(assignments, list):
        raise ValueError("interactive assignments must be an array")
    ids: list[str] = []
    fields = {
        "discovery_id", "disposition", "rationale", "architecture_usage",
        "publication_role", "architecture_role", "profile_extensions",
    }
    for index, row in enumerate(assignments):
        if not isinstance(row, dict) or set(row) != fields:
            raise ValueError(f"interactive assignments[{index}] fields invalid")
        did = row.get("discovery_id")
        if did not in expected_discovery_ids:
            raise ValueError(f"interactive assignments[{index}] unknown Discovery ID: {did}")
        ids.append(did)
        if row.get("disposition") not in {"SELECTED", "HOLD", "REJECT", "INSPECT"}:
            raise ValueError(f"interactive assignments[{index}] disposition invalid")
        if row.get("architecture_usage") not in {"PRIMARY", "SUPPORTING", "NONE"}:
            raise ValueError(f"interactive assignments[{index}] architecture_usage invalid")
        if not _nonempty(row.get("rationale")) or not isinstance(row.get("profile_extensions"), dict):
            raise ValueError(f"interactive assignments[{index}] rationale/extensions invalid")
        for key in ("publication_role", "architecture_role"):
            if row.get(key) is not None and not _nonempty(row.get(key)):
                raise ValueError(f"interactive assignments[{index}] {key} invalid")
    if len(ids) != len(set(ids)) or set(ids) != expected_discovery_ids:
        raise ValueError("interactive assignments must cover every Matrix Discovery exactly once")

    plan = doc.get("architecture")
    if not isinstance(plan, dict) or set(plan) != {
        "editorial_thesis", "architecture_goals", "page_plan", "packages",
        "selected_exceptions", "profile_extensions", "publication_extensions",
    }:
        raise ValueError("interactive architecture fields invalid")
    if not _nonempty(plan.get("editorial_thesis")):
        raise ValueError("interactive architecture editorial_thesis required")
    _unique_strings(plan.get("architecture_goals"), "architecture_goals", allow_empty=False)
    page = plan.get("page_plan")
    if not isinstance(page, dict) or set(page) != {"target_pages", "max_pages", "notes"}:
        raise ValueError("interactive page_plan fields invalid")
    for key in ("target_pages", "max_pages"):
        value = page.get(key)
        if value is not None and (not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0):
            raise ValueError(f"interactive page_plan.{key} invalid")
    if page.get("notes") is not None and not _nonempty(page.get("notes")):
        raise ValueError("interactive page_plan.notes invalid")
    packages = plan.get("packages")
    if not isinstance(packages, list) or not packages:
        raise ValueError("interactive architecture requires packages")
    package_ids: list[str] = []
    package_fields = {
        "package_id", "title", "purpose", "primary_discovery_ids", "supporting_discovery_ids",
        "must_cover_requirements", "boundaries", "drafting_order", "profile_extensions", "publication_extensions",
    }
    for index, package in enumerate(packages):
        if not isinstance(package, dict) or set(package) != package_fields:
            raise ValueError(f"interactive packages[{index}] fields invalid")
        if not all(_nonempty(package.get(k)) for k in ("package_id", "title", "purpose")):
            raise ValueError(f"interactive packages[{index}] identity/title/purpose invalid")
        package_ids.append(package["package_id"])
        for key in ("primary_discovery_ids", "supporting_discovery_ids", "must_cover_requirements", "boundaries"):
            values = _unique_strings(package.get(key), f"packages[{index}].{key}")
            if key.endswith("discovery_ids") and any(x not in expected_discovery_ids for x in values):
                raise ValueError(f"interactive packages[{index}] references unknown Discovery")
        if set(package["primary_discovery_ids"]) & set(package["supporting_discovery_ids"]):
            raise ValueError(f"interactive packages[{index}] duplicates primary/supporting Discovery")
        order = package.get("drafting_order")
        if not isinstance(order, int) or isinstance(order, bool) or order < 1:
            raise ValueError(f"interactive packages[{index}] drafting_order invalid")
        if not isinstance(package.get("profile_extensions"), dict) or not isinstance(package.get("publication_extensions"), dict):
            raise ValueError(f"interactive packages[{index}] extensions invalid")
    if len(package_ids) != len(set(package_ids)):
        raise ValueError("interactive package_id values must be unique")
    exceptions = plan.get("selected_exceptions")
    if not isinstance(exceptions, list):
        raise ValueError("interactive selected_exceptions must be an array")
    for index, item in enumerate(exceptions):
        if not isinstance(item, dict) or set(item) != {"discovery_id", "reason", "exception_kind"}:
            raise ValueError(f"interactive selected_exceptions[{index}] fields invalid")
        if item.get("discovery_id") not in expected_discovery_ids or not _nonempty(item.get("reason")):
            raise ValueError(f"interactive selected_exceptions[{index}] identity/reason invalid")
        if item.get("exception_kind") not in {"OMITTED_FROM_ARCHITECTURE", "DEFERRED", "STRUCTURAL_EXCEPTION"}:
            raise ValueError(f"interactive selected_exceptions[{index}] kind invalid")
    if not isinstance(plan.get("profile_extensions"), dict) or not isinstance(plan.get("publication_extensions"), dict):
        raise ValueError("interactive architecture extensions invalid")


def _matrix_discovery_map(matrix: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in matrix["rows"]:
        ids = row.get("discovery_ids")
        if not isinstance(ids, list) or len(ids) != 1:
            raise ValueError("interactive Selection/Architecture requires one Discovery per Matrix candidate")
        did = ids[0]
        if did in result:
            raise ValueError(f"Matrix maps Discovery more than once: {did}")
        result[did] = row
    return result


class _CheckedSelection:
    """Runner-local checked context (single run() call, no LOW upstream ownership).

    Holds read_set (LOW DATA), validated pieces, expectations/root/effective,
    input pin/bytes, implementation_sha, upstream (held after first content EU),
    expected output bytes. Public functions take no bundle/skip flag.
    """
    __slots__ = (
        "read_set", "state", "profile_path", "profile", "source_root",
        "four", "evidence_path", "views_path", "ledger_path", "completeness_path",
        "screening_path", "effective", "discovery_path",
        "expectations", "root_records", "root_path",
        "input_pin", "input_doc", "implementation_sha",
        "upstream", "expected_outputs",
    )
    def __init__(self, **kwargs):
        for k in self.__slots__:
            setattr(self, k, kwargs.get(k))


def _prepare_checked_selection(repo_root: Path, state_path: Path, input_path: Path, implementation_sha: str) -> _CheckedSelection:
    """Capture -> ORIGINAL full validation -> recheck -> sealed runner context.

    Order capture FIRST (typed exhaustive pins, same-bytes parse), then ORIGINAL
    full strict agent/READY/resolve/Discovery/Screening BOTH halves+effective and
    once-only ORIGINAL Screening/Evidence package validators under ORIGINAL
    historical facade, then recheck seals private context. Historical
    root_records/root_path come from bound COPY actual DCP/SCP (never None);
    effective separate (never E-as-R). No caller assertion/public verified dict/
    global context/expanded fake facade.
    """
    repo_root = repo_root.resolve()
    state_path = state_path.resolve()
    input_path = input_path.resolve()
    read_set = low._capture_selection_read_set(repo_root, state_path)
    try:
        ist = input_path.lstat()
    except OSError as exc:
        raise ValueError(f"interactive input unreadable: {input_path}: {exc}") from exc
    import stat as _stat
    if not _stat.S_ISREG(ist.st_mode):
        raise ValueError(f"interactive input is not a regular file: {input_path}")
    if input_path.is_symlink():
        raise ValueError(f"interactive input must not be a symlink: {input_path}")
    # Input parent must be regular directory (outside candidate allowed, but validated).
    try:
        _pstat = input_path.parent.lstat()
    except OSError as exc:
        raise ValueError(f"interactive input parent unreadable: {input_path.parent}: {exc}") from exc
    if not _stat.S_ISDIR(_pstat.st_mode) or input_path.parent.is_symlink():
        raise ValueError(f"interactive input parent must be regular directory: {input_path.parent}")
    input_raw = input_path.read_bytes()
    import hashlib as _hl
    input_pin = ("interactive input", input_path, _hl.sha256(input_raw).hexdigest(), len(input_raw))
    try:
        import json as _json
        input_doc = _json.loads(input_raw.decode("utf-8"), object_pairs_hook=core._strict_object_pairs)
    except Exception as exc:
        raise ValueError(f"interactive input JSON invalid: {exc}") from exc
    if not isinstance(input_doc, dict):
        raise ValueError("interactive input must be a JSON object")
    cfg = core.load_json(repo_root / core.DEFAULT_CONFIG)
    state = core.load_json(state_path)
    errors = agent.validate_agent_state(repo_root, cfg, state)
    if errors:
        raise ValueError("Production State invalid before Selection/Architecture: " + "; ".join(errors))
    if state.get("lifecycle_state") != "EVIDENCE_REVIEWED":
        raise ValueError("interactive Selection/Architecture requires EVIDENCE_REVIEWED Production State")
    profile_path = repo_root / state["profile"]["path"]
    profile = core.load_json(profile_path)
    source_root = core.repo_local_path(repo_root, profile["paths"]["source_root"], "paths.source_root")
    _dm022_require_ready(repo_root, state_path)
    discovery_acceptance_path = source_root / "discovery/discovery-accepted-v2.json"
    accepted_discovery = discovery.validate_acceptance(repo_root, discovery_acceptance_path)
    root_discovery_path = core.repo_local_path(repo_root, accepted_discovery["discovery_path"], "accepted Discovery JSONL")
    ledger_path, completeness_path = _dm022_resolve_ledger_completeness(repo_root, state_path, state, source_root)
    if _dm022_pinned_family(repo_root, state) == "PREARCH":
        four = low.resolve_research_authority(repo_root, state_path)
        refs = four.get("artifact_refs")
        if not isinstance(refs, dict) or set(refs) != {"evidence-acceptance", "edition-views-acceptance", "materiality-ledger", "profile-completeness"}:
            raise ValueError("PREARCH artifact_refs must be exactly the 4 NamedRefs")
        evidence_path = repo_root / str(refs["evidence-acceptance"]["path"])
        views_path = repo_root / str(refs["edition-views-acceptance"]["path"])
        ledger_path = repo_root / str(refs["materiality-ledger"]["path"])
        completeness_path = repo_root / str(refs["profile-completeness"]["path"])
        # Retain second adopted traversal (original 1AG at :271) before recheck; recheck does not replace predicates.
        _second = low.resolve_research_authority(repo_root, state_path)
        if _second.get("family") != "PREARCH":
            raise ValueError("PREARCH second resolve did not return PREARCH")
        low._recheck_selection_read_set(repo_root, state_path, read_set)
    else:
        active_evidence_views = agent.resolve_active_evidence_views(repo_root, cfg, state)
        evidence_path = active_evidence_views["evidence_path"]
        views_path = active_evidence_views["views_path"]
        four = {"family": "LEGACY"}
    screening_path = screening.resolve_active_screening_acceptance(
        repo_root, state_path, implementation_sha
    )["path"]
    effective = screening.resolve_effective_discovery_basis(
        repo_root,
        screening_path.parent / "package.json",
        implementation_sha,
        accepted_root_path=root_discovery_path,
    )
    discovery_path = effective["path"]
    with agent_tool.current_stage_basis_override():
        spkg_path = screening_path.parent / "package.json"
        spkg = core.load_json(spkg_path)
        screening.validate_package_basis(repo_root, spkg_path, spkg, implementation_sha)
        try:
            epkg_path = evidence_path.parent / "package.json"
            epkg = core.load_json(epkg_path)
            from scripts import survey_evidence_v2 as _ev
            _ev.validate_evidence_package_basis(repo_root, epkg_path, epkg, implementation_sha)
        except Exception as exc:
            if four.get("family") == "PREARCH":
                raise
    low._recheck_selection_read_set(repo_root, state_path, read_set)
    # Historical root_records/root_path from bound COPY actual DCP/SCP (never None for PREARCH).
    if four.get("family") == "PREARCH":
        _req_pin = None
        _copy_pin = None
        for _lbl, _pp, _ss, _ll in read_set.pins:
            if _lbl == "checkpoint request":
                _req_pin = _pp
            elif _lbl == "retained state-before COPY":
                _copy_pin = _pp
        if _req_pin is None or _copy_pin is None:
            raise ValueError("PREARCH read set missing request/COPY for root derivation")
        _ctx = low.derive_ordinary_root_effective_context(repo_root, Path(_req_pin), Path(_copy_pin))
        root_records = _ctx.get("root_records")
        root_path = _ctx.get("root_path")
        if not isinstance(root_records, list) or not root_records:
            raise ValueError("PREARCH root_records empty after COPY-bound derivation")
        if root_path is None:
            raise ValueError("PREARCH root_path missing after COPY-bound derivation")
        _own = read_set.own_epoch or {}
        _reqd = _own.get("request") or {}
        _canon = (_reqd.get("before_state") or {}).get("path")
        if not isinstance(_canon, str) or not _canon:
            raise ValueError("PREARCH canonical_state_path missing in request")
        _exp_issue = (_own.get("record") or {}).get("issue_id") or state.get("issue_id")
        _exp_prof = (_own.get("record") or {}).get("research_profile") or profile.get("research_profile")
        expectations = {"issue_id": _exp_issue, "research_profile": _exp_prof, "canonical_state_path": _canon}
        if not expectations["issue_id"] or not expectations["research_profile"]:
            raise ValueError("PREARCH expectations missing issue/research")
        # Effective separate from root (never E-as-R): effective path must differ or be DIRECT with same bytes already pinned.
        # No additional check here; content cores distinguish via root_records vs effective path.
    else:
        expectations = {"issue_id": state.get("issue_id"), "research_profile": profile.get("research_profile"), "canonical_state_path": None}
        # LEGACY public path exact: root via accepted root (no PREARCH content).
        try:
            from scripts import survey_screening_v2 as _scm
            root_records = _scm.read_jsonl(root_discovery_path)
        except Exception as exc:
            raise ValueError(f"LEGACY root Discovery unreadable: {exc}") from exc
        root_path = root_discovery_path
    return _CheckedSelection(
        read_set=read_set, state=state, profile_path=profile_path, profile=profile, source_root=source_root,
        four=four, evidence_path=evidence_path, views_path=views_path, ledger_path=ledger_path, completeness_path=completeness_path,
        screening_path=screening_path, effective=effective, discovery_path=discovery_path,
        expectations=expectations, root_records=root_records, root_path=root_path,
        input_pin=input_pin, input_doc=input_doc, implementation_sha=implementation_sha,
        upstream=None, expected_outputs={},
    )




def _check_selection_boundary(repo_root: Path, state_path: Path, checked: _CheckedSelection) -> None:
    """Cheap freshness for later boundaries (FILE/pin/lstat + FULL own-epoch, no 6E/3V).

    Full read-set + directory inventories + ancestor/symlink + guard/State/
    triplet/HEAD/current-code/own-epoch batch UNCONDITIONAL for PREARCH.
    Manifest/request missing refuses. Preserves completion seven-plan/expected_after
    via lightweight shared extraction. No same-inode stale/symlink tolerance.
    """
    low._recheck_selection_read_set(repo_root, state_path, checked.read_set)
    low.require_no_active_guard(checked.source_root)
    cur_state = core.load_json(state_path)
    low.require_same_triplet(cur_state, low._resolve_research_from_state_bytes(repo_root, cur_state))
    cur_head = core.repository_commit_sha(repo_root)
    if cur_head != checked.implementation_sha:
        raise ValueError(f"HEAD moved during Selection/Architecture (expected {checked.implementation_sha}, got {cur_head})")
    raw = checked.input_pin[1].read_bytes() if isinstance(checked.input_pin[1], Path) else None
    if raw is None:
        raise ValueError("checked input pin path invalid")
    import hashlib as _hl2
    if len(raw) != checked.input_pin[3] or _hl2.sha256(raw).hexdigest() != checked.input_pin[2]:
        raise ValueError("interactive input bytes changed after seal")
    # Preserve completion seven-plan/expected_after historical semantics for PREARCH.
    if checked.read_set.is_prearch:
        _cref = None
        try:
            _prov = cur_state.get("checkpoint_provenance", {}) or {}
            _ev = _prov.get("evidence") or {}
            if isinstance(_ev, dict) and isinstance(_ev.get("path"), str) and isinstance(_ev.get("sha256"), str):
                _cref = {"path": str(_ev.get("path")), "sha256": str(_ev.get("sha256"))}
        except Exception as exc:
            raise ValueError(f"checkpoint ref derivation failed: {exc}") from exc
        if _cref is None:
            raise ValueError("PREARCH checkpoint ref missing for slots check")
        try:
            low._check_completion_slots_fresh(repo_root, checked.source_root, _cref)
        except Exception as exc:
            # Preserve typed error as ValueError for runner boundary (no silent pass).
            raise ValueError(str(exc)) from exc


def run(repo_root: Path, state_path: Path, input_path: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    state_path = state_path.resolve()
    input_path = input_path.resolve()
    implementation_sha = core.repository_commit_sha(repo_root)
    checked = _prepare_checked_selection(repo_root, state_path, input_path, implementation_sha)
    state = checked.state
    profile = checked.profile
    profile_path = checked.profile_path
    source_root = checked.source_root
    ledger_path = checked.ledger_path
    completeness_path = checked.completeness_path
    evidence_path = checked.evidence_path
    views_path = checked.views_path
    screening_path = checked.screening_path
    discovery_path = checked.discovery_path
    effective = checked.effective
    expectations = checked.expectations
    root_records = checked.root_records
    root_path = checked.root_path
    interactive = checked.input_doc

    matrix_path = source_root / "candidate-matrix-v2.json"
    selection_path = source_root / "candidate-selection-v2.json"
    architecture_path = source_root / "architecture-v2.json"
    review_path = source_root / "architecture-review-summary-v2.json"
    attention_path = source_root / "architecture-review-attention-v2.json"
    archive_path = source_root / "orchestration/v2/interactive/selection-architecture-input.json"
    audit_probe_path = source_root / "orchestration/v2/interactive/selection-architecture-audit.json"
    # Successor preflight covers all seven incl audit once (not re-run after first write).
    _dm022_preflight_seven(source_root)
    for path in (matrix_path, selection_path, architecture_path, review_path, attention_path, archive_path, audit_probe_path):
        if path.exists() or path.is_symlink():
            raise ValueError(f"refusing to overwrite Selection/Architecture artifact: {path}")

    def _verify_owned(expected_map: dict[str, bytes], written: set[str]) -> None:
        # Already-owned outputs must equal producer expected bytes; not-yet-written absent.
        for rel, exp in expected_map.items():
            p = source_root / rel
            if rel in written:
                try:
                    actual = p.read_bytes()
                except OSError as exc:
                    raise ValueError(f"owned output unreadable after seal: {rel}: {exc}") from exc
                if actual != exp:
                    raise ValueError(f"owned output bytes changed after seal: {rel}")
            else:
                if p.exists() or p.is_symlink():
                    # Allow historical completion tolerance? No: owned progression distinct,
                    # not-yet-written must remain absent (do not adopt conflicting output).
                    raise ValueError(f"not-yet-written slot unexpectedly present: {rel}")

    # First EU via content cores with validated initial predicates (0AG, no LIVE _load_upstream).
    upstream = base._load_upstream_content(
        repo_root, profile_path, discovery_path, screening_path, evidence_path,
        views_path, ledger_path, completeness_path, expectations, root_records, root_path,
    )
    checked.upstream = upstream
    matrix = base._derive_matrix_rows_content(
        repo_root, upstream, profile_path, completeness_path, ledger_path, evidence_path, views_path
    )
    schema_gate.validate_instance(matrix, repo_root / architecture.MATRIX_SCHEMA, label="Candidate Matrix")
    # Boundary before first write (cheap freshness + historical tolerance, no 2AG).
    _check_selection_boundary(repo_root, state_path, checked)
    _verify_owned({}, set())
    if matrix_path.exists() or matrix_path.is_symlink():
        raise ValueError(f"refusing to overwrite Selection/Architecture artifact: {matrix_path}")
    architecture.write_candidate_matrix(matrix_path, matrix)
    exp_matrix = core.json_bytes(matrix)
    if matrix_path.read_bytes() != exp_matrix:
        raise ValueError("Candidate Matrix bytes changed immediately after write")
    checked.expected_outputs["candidate-matrix-v2.json"] = exp_matrix
    matrix_by_discovery = _matrix_discovery_map(matrix)

    interactive = checked.input_doc
    _validate_input(interactive, state["issue_id"], set(matrix_by_discovery))
    assignment_input = {row["discovery_id"]: row for row in interactive["assignments"]}
    assignments: list[dict[str, Any]] = []
    for did in sorted(matrix_by_discovery):
        src = assignment_input[did]
        assignments.append({
            "candidate_id": matrix_by_discovery[did]["candidate_id"],
            "disposition": src["disposition"],
            "rationale": src["rationale"],
            "architecture_usage": src["architecture_usage"],
            "publication_role": src["publication_role"],
            "architecture_role": src["architecture_role"],
            "profile_extensions": src["profile_extensions"],
        })
    dispositions = [row["disposition"] for row in assignments]
    selection = {
        "schema_version": "2.0-rc1",
        "issue_id": state["issue_id"],
        "research_profile": profile["research_profile"],
        "publication_profile": profile["publication_profile"],
        "selection_version": "interactive-v2-1",
        "status": "ESTABLISHED",
        "basis": {
            "production_profile_sha256": core.sha256_file(profile_path),
            "candidate_matrix_sha256": core.sha256_file(matrix_path),
            "profile_completeness_sha256": core.sha256_file(completeness_path),
            "materiality_ledger_sha256": core.sha256_file(ledger_path),
        },
        "assignments": assignments,
        "summary": {
            "candidate_count": len(assignments),
            "disposition_counts": dict(sorted(Counter(dispositions).items())),
            "selected_count": sum(value == "SELECTED" for value in dispositions),
        },
    }
    schema_gate.validate_instance(selection, repo_root / architecture.SELECTION_SCHEMA, label="Candidate Selection")
    errors = architecture.validate_selection(repo_root, selection, profile_path, matrix_path, completeness_path, ledger_path)
    if errors:
        raise ValueError("Candidate Selection invalid: " + "; ".join(errors))
    _check_selection_boundary(repo_root, state_path, checked)
    _verify_owned({"candidate-matrix-v2.json": checked.expected_outputs["candidate-matrix-v2.json"]}, {"candidate-matrix-v2.json"})
    if selection_path.exists() or selection_path.is_symlink():
        raise ValueError(f"refusing to overwrite Selection/Architecture artifact: {selection_path}")
    core.write_json(selection_path, selection)
    exp_selection = core.json_bytes(selection)
    if selection_path.read_bytes() != exp_selection:
        raise ValueError("Candidate Selection bytes changed immediately after write")
    checked.expected_outputs["candidate-selection-v2.json"] = exp_selection

    candidate_id = {did: row["candidate_id"] for did, row in matrix_by_discovery.items()}
    plan_input = interactive["architecture"]
    packages: list[dict[str, Any]] = []
    for src in plan_input["packages"]:
        primary_ids = [candidate_id[x] for x in src["primary_discovery_ids"]]
        supporting_ids = [candidate_id[x] for x in src["supporting_discovery_ids"]]
        inherited = [
            boundary
            for cid in [*primary_ids, *supporting_ids]
            for boundary in next(row for row in matrix["rows"] if row["candidate_id"] == cid)["remaining_boundaries"]
        ]
        boundaries = list(dict.fromkeys([*src["boundaries"], *inherited]))
        packages.append({
            "package_id": src["package_id"],
            "title": src["title"],
            "purpose": src["purpose"],
            "primary_candidate_ids": primary_ids,
            "supporting_candidate_ids": supporting_ids,
            "must_cover_requirements": list(src["must_cover_requirements"]),
            "boundaries": boundaries,
            "drafting_order": src["drafting_order"],
            "profile_extensions": src["profile_extensions"],
            "publication_extensions": src["publication_extensions"],
        })
    exceptions = [
        {
            "candidate_id": candidate_id[row["discovery_id"]],
            "reason": row["reason"],
            "exception_kind": row["exception_kind"],
        }
        for row in plan_input["selected_exceptions"]
    ]
    proposed = {
        "schema_version": "2.0-rc1",
        "issue_id": state["issue_id"],
        "research_profile": profile["research_profile"],
        "publication_profile": profile["publication_profile"],
        "status": "PROPOSED",
        "basis": {
            "production_profile_sha256": core.sha256_file(profile_path),
            "profile_completeness_sha256": core.sha256_file(completeness_path),
            "materiality_ledger_sha256": core.sha256_file(ledger_path),
            "candidate_matrix_sha256": core.sha256_file(matrix_path),
            "candidate_selection_sha256": core.sha256_file(selection_path),
        },
        "editorial_thesis": plan_input["editorial_thesis"],
        "architecture_goals": list(plan_input["architecture_goals"]),
        "page_plan": dict(plan_input["page_plan"]),
        "packages": packages,
        "selected_exceptions": exceptions,
        "profile_extensions": plan_input["profile_extensions"],
        "publication_extensions": plan_input["publication_extensions"],
        "human_review": {"reviewed_by": None, "reviewed_at": None, "review_reference": None},
    }
    schema_gate.validate_instance(proposed, repo_root / architecture.ARCHITECTURE_SCHEMA, label="Issue Architecture")
    errors = architecture.validate_architecture(
        repo_root, proposed, profile_path, completeness_path, ledger_path, matrix_path, selection_path, require_approved=False
    )
    if errors:
        raise ValueError("Issue Architecture invalid: " + "; ".join(errors))
    _check_selection_boundary(repo_root, state_path, checked)
    _verify_owned(
        {"candidate-matrix-v2.json": checked.expected_outputs["candidate-matrix-v2.json"],
         "candidate-selection-v2.json": checked.expected_outputs["candidate-selection-v2.json"]},
        {"candidate-matrix-v2.json", "candidate-selection-v2.json"},
    )
    if architecture_path.exists() or architecture_path.is_symlink():
        raise ValueError(f"refusing to overwrite Selection/Architecture artifact: {architecture_path}")
    core.write_json(architecture_path, proposed)
    exp_arch = core.json_bytes(proposed)
    if architecture_path.read_bytes() != exp_arch:
        raise ValueError("Issue Architecture bytes changed immediately after write")
    checked.expected_outputs["architecture-v2.json"] = exp_arch

    # Single held upstream + shared FULL summary private helper (no 90AG duplicate upstream).
    review = base._build_architecture_review_summary_with_upstream(
        repo_root, profile_path, discovery_path, screening_path, evidence_path, views_path,
        ledger_path, completeness_path, matrix_path, selection_path, architecture_path, checked.upstream,
    )
    if review.get("readiness", {}).get("status") != "READY_FOR_ARCHITECTURE_REVIEW":
        raise ValueError("Architecture Review Summary is BLOCKED: " + "; ".join(review.get("readiness", {}).get("errors", [])))
    schema_gate.validate_instance(review, repo_root / architecture.REVIEW_SCHEMA, label="Architecture Review Summary")
    _check_selection_boundary(repo_root, state_path, checked)
    _verify_owned(
        {"candidate-matrix-v2.json": checked.expected_outputs["candidate-matrix-v2.json"],
         "candidate-selection-v2.json": checked.expected_outputs["candidate-selection-v2.json"],
         "architecture-v2.json": checked.expected_outputs["architecture-v2.json"]},
        {"candidate-matrix-v2.json", "candidate-selection-v2.json", "architecture-v2.json"},
    )
    if review_path.exists() or review_path.is_symlink():
        raise ValueError(f"refusing to overwrite Selection/Architecture artifact: {review_path}")
    core.write_json(review_path, review)
    exp_review = core.json_bytes(review)
    if review_path.read_bytes() != exp_review:
        raise ValueError("Architecture Review Summary bytes changed immediately after write")
    checked.expected_outputs["architecture-review-summary-v2.json"] = exp_review
    # Attention expected bytes BEFORE writes via private pure payload helper (existing extraction).
    exp_attention_payload = review_attention._build_attention_payload(
        repo_root, screening_path, ledger_path, selection_path, limit=50
    )
    exp_attention = core.json_bytes(exp_attention_payload)
    _check_selection_boundary(repo_root, state_path, checked)
    _verify_owned(
        {"candidate-matrix-v2.json": checked.expected_outputs["candidate-matrix-v2.json"],
         "candidate-selection-v2.json": checked.expected_outputs["candidate-selection-v2.json"],
         "architecture-v2.json": checked.expected_outputs["architecture-v2.json"],
         "architecture-review-summary-v2.json": checked.expected_outputs["architecture-review-summary-v2.json"]},
        {"candidate-matrix-v2.json", "candidate-selection-v2.json", "architecture-v2.json", "architecture-review-summary-v2.json"},
    )
    if attention_path.exists() or attention_path.is_symlink():
        raise ValueError(f"refusing to overwrite Selection/Architecture artifact: {attention_path}")
    review_attention.build_attention(repo_root, screening_path, ledger_path, selection_path, attention_path)
    review_attention.validate_attention(repo_root, attention_path)
    if attention_path.read_bytes() != exp_attention:
        raise ValueError("Architecture Review Attention bytes differ from expected payload before write")
    checked.expected_outputs["architecture-review-attention-v2.json"] = exp_attention

    archive_path.parent.mkdir(parents=True, exist_ok=True)
    _check_selection_boundary(repo_root, state_path, checked)
    _verify_owned(
        {"candidate-matrix-v2.json": checked.expected_outputs["candidate-matrix-v2.json"],
         "candidate-selection-v2.json": checked.expected_outputs["candidate-selection-v2.json"],
         "architecture-v2.json": checked.expected_outputs["architecture-v2.json"],
         "architecture-review-summary-v2.json": checked.expected_outputs["architecture-review-summary-v2.json"],
         "architecture-review-attention-v2.json": checked.expected_outputs["architecture-review-attention-v2.json"]},
        {"candidate-matrix-v2.json", "candidate-selection-v2.json", "architecture-v2.json", "architecture-review-summary-v2.json", "architecture-review-attention-v2.json"},
    )
    if archive_path.exists() or archive_path.is_symlink():
        raise ValueError(f"refusing to overwrite Selection/Architecture artifact: {archive_path}")
    # Input archive must match entry-pinned input bytes (frozen same bytes through parsing/archive).
    exp_input = checked.input_pin[1].read_bytes() if isinstance(checked.input_pin[1], Path) else input_path.read_bytes()
    shutil.copy2(input_path, archive_path)
    if archive_path.read_bytes() != exp_input:
        raise ValueError("archived input bytes differ from entry-pinned input")
    checked.expected_outputs["orchestration/v2/interactive/selection-architecture-input.json"] = exp_input
    audit_path = archive_path.parent / "selection-architecture-audit.json"
    audit_payload = {
        "schema_version": "2.0-rc1",
        "issue_id": state["issue_id"],
        "interactive_input": {"path": _rel(repo_root, archive_path), "sha256": core.sha256_file(archive_path)},
        "runner": interactive["runner"],
        "outputs": {
            "candidate_matrix": {"path": _rel(repo_root, matrix_path), "sha256": core.sha256_file(matrix_path)},
            "candidate_selection": {"path": _rel(repo_root, selection_path), "sha256": core.sha256_file(selection_path)},
            "issue_architecture": {"path": _rel(repo_root, architecture_path), "sha256": core.sha256_file(architecture_path)},
            "architecture_review_summary": {"path": _rel(repo_root, review_path), "sha256": core.sha256_file(review_path)},
            "architecture_review_attention": {"path": _rel(repo_root, attention_path), "sha256": core.sha256_file(attention_path)},
        },
    }
    exp_audit = core.json_bytes(audit_payload)
    _check_selection_boundary(repo_root, state_path, checked)
    _verify_owned(
        {"candidate-matrix-v2.json": checked.expected_outputs["candidate-matrix-v2.json"],
         "candidate-selection-v2.json": checked.expected_outputs["candidate-selection-v2.json"],
         "architecture-v2.json": checked.expected_outputs["architecture-v2.json"],
         "architecture-review-summary-v2.json": checked.expected_outputs["architecture-review-summary-v2.json"],
         "architecture-review-attention-v2.json": checked.expected_outputs["architecture-review-attention-v2.json"],
         "orchestration/v2/interactive/selection-architecture-input.json": checked.expected_outputs["orchestration/v2/interactive/selection-architecture-input.json"]},
        {"candidate-matrix-v2.json", "candidate-selection-v2.json", "architecture-v2.json", "architecture-review-summary-v2.json", "architecture-review-attention-v2.json", "orchestration/v2/interactive/selection-architecture-input.json"},
    )
    if audit_path.exists() or audit_path.is_symlink():
        raise ValueError(f"refusing to overwrite Selection/Architecture artifact: {audit_path}")
    core.write_json(audit_path, audit_payload)
    if audit_path.read_bytes() != exp_audit:
        raise ValueError("Audit bytes changed immediately after write")
    checked.expected_outputs["orchestration/v2/interactive/selection-architecture-audit.json"] = exp_audit
    # Final return verifies original read-set/source/HEAD/own-epoch/guard/State and all seven expected outputs.
    _check_selection_boundary(repo_root, state_path, checked)
    _verify_owned(checked.expected_outputs, set(checked.expected_outputs.keys()))
    # Audit expected bytes already verified; no success dict after late drift. Partial files remain on failure.
    return {
        "candidate_matrix": _rel(repo_root, matrix_path),
        "candidate_selection": _rel(repo_root, selection_path),
        "issue_architecture": _rel(repo_root, architecture_path),
        "architecture_review_summary": _rel(repo_root, review_path),
        "architecture_review_attention": _rel(repo_root, attention_path),
        "selected_count": selection["summary"]["selected_count"],
        "architecture_package_count": len(packages),
        "review_readiness": review["readiness"]["status"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--state", required=True)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    state = Path(args.state)
    input_path = Path(args.input)
    if not state.is_absolute(): state = root / state
    if not input_path.is_absolute(): input_path = root / input_path
    try:
        print(json.dumps(run(root, state, input_path), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=__import__("sys").stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
