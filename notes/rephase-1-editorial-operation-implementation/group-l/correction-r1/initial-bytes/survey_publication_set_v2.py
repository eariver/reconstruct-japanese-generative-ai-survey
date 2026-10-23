#!/usr/bin/env python3
"""Low-level strict branch/chain/anchor/seal/current-selection identity layer.

Group L owned. May use ONLY core safe path/hash/schema primitives and stdlib.
Must NOT call (import or runtime): agent control, Stage validation, Reader,
Gate, receipt validators, P1/P2R/P3S, QA/Gate/Candidate builders. Agent calls
low, never reverse. Core State calls it via local import; no top-level cycle.

Provides frozen APIs (see astra-implementation-selection §2 + map-resolution §2):
  resolve_publication_selection, resolve_publication_artifact_path,
  validate_seal, validate_activation_record, derive_canonical_anchor,
  before_active_digest, assert_canonical_publication_mode,
  active_candidate_ref, require_active_or_canonical.

Identity only: validates actual reference path/hash/bytes/schema/declared
layout + current source refs, staged/proposal/retention identity and retained
before-State bytes using schema/low-level primitives only. No semantic replay,
no bogus skip-proof. Legacy rows cumulative against original checkpoint.
Canonical anchor is latest legacy immediately before first activation. Chain
bounded 32, sequence chronology, expected original checkpoint; later legacy
after editorial is rejected fail-closed. Historical branch never requires old
State hash at live path; validates via retained exact COPY. Before digest is
recomputed from before-effective7 + candidate (not caller acceptance).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from scripts import survey_production_v2 as core
from scripts import survey_schema_v2 as schema_gate


class PublicationSetError(ValueError):
    pass


SEAL_SCHEMA = Path("schemas/editorial-publication-set-v2.schema.json")
REVALIDATION_SCHEMA = Path("schemas/publication-surface-revalidation.schema.json")
CHECKPOINT_SCHEMA = Path("schemas/stage-checkpoint-v2.schema.json")
BUNDLE_SCHEMA = Path("schemas/quality-regression-bundle-v2.schema.json")
CANDIDATE_SCHEMA = Path("schemas/publication-candidate-v2.schema.json")
RETENTION_SCHEMA = Path("schemas/editorial-retention-manifest-v2.schema.json")
PROPOSAL_SCHEMA = Path("schemas/editorial-correction-proposal-v2.schema.json")
STAGED_SCHEMA = Path("schemas/editorial-staged-source-manifest-v2.schema.json")

LEGACY_REASON = "REVIEWED_CORE_CHANGE"
EDITORIAL_REASON = "REVIEWED_EDITORIAL_CORRECTION"
EDITORIAL_KIND = "EDITORIAL_PUBLICATION_ACTIVATION_V1"
SEAL_KIND = "EDITORIAL_PUBLICATION_SET_V1"
SEAL_STATUS = "SEALED_INERT"

PUBLICATION_ROLES_15 = (
    "reader-input",
    "authoring-input",
    "source-receipt",
    "reader-manuscript",
    "validated-source",
    "bibliography",
    "style",
    "publication-pdf",
    "build-log",
    "pdf-digest",
    "quality-regression-bundle",
    "semantic-review",
    "visual-review",
    "reader-surface-gate",
    "publication-candidate",
)

# Exactly the seven publication roles of the validation checkpoint that may
# project to active seal roles. No research/Architecture/Draft rebinding.
PUBLICATION_ROLES_7 = (
    "reader-manuscript",
    "validated-source",
    "publication-pdf",
    "quality-regression-bundle",
    "semantic-review",
    "visual-review",
    "reader-surface-gate",
)

CHAIN_LIMIT = 32


def _repo_file(repo_root: Path, rel: str, label: str) -> Path:
    try:
        resolved = core.repo_local_path(repo_root, rel, label)
    except (TypeError, ValueError) as exc:
        raise PublicationSetError(f"{label} escapes repository: {rel}: {exc}") from exc
    if resolved.is_symlink() or not resolved.is_file():
        raise PublicationSetError(f"{label} missing or unsafe: {rel}")
    return resolved


def _check_file_ref(repo_root: Path, ref: Any, label: str) -> Path:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256", "byte_count"}:
        raise PublicationSetError(f"{label} file_ref fields invalid")
    path_value = ref.get("path")
    sha_value = ref.get("sha256")
    size_value = ref.get("byte_count")
    if not isinstance(path_value, str) or not path_value:
        raise PublicationSetError(f"{label} file_ref path invalid")
    if not isinstance(sha_value, str) or len(sha_value) != 64 or any(c not in "0123456789abcdef" for c in sha_value):
        raise PublicationSetError(f"{label} file_ref sha256 invalid")
    if not isinstance(size_value, int) or isinstance(size_value, bool) or size_value < 1:
        raise PublicationSetError(f"{label} file_ref byte_count invalid")
    resolved = _repo_file(repo_root, path_value, label)
    actual_sha = core.sha256_file(resolved)
    if actual_sha != sha_value:
        raise PublicationSetError(f"{label} SHA drift: {path_value}")
    try:
        actual_size = resolved.stat().st_size
    except OSError as exc:
        raise PublicationSetError(f"{label} stat failed: {path_value}: {exc}") from exc
    if actual_size != size_value:
        raise PublicationSetError(f"{label} byte count drift: {path_value}")
    return resolved


def _check_authority_ref(repo_root: Path, ref: Any, label: str) -> Path:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
        raise PublicationSetError(f"{label} authority fields invalid")
    path_value = ref.get("path")
    sha_value = ref.get("sha256")
    if not isinstance(path_value, str) or not path_value:
        raise PublicationSetError(f"{label} authority path invalid")
    if not isinstance(sha_value, str) or len(sha_value) != 64 or any(c not in "0123456789abcdef" for c in sha_value):
        raise PublicationSetError(f"{label} authority sha256 invalid")
    resolved = _repo_file(repo_root, path_value, label)
    if core.sha256_file(resolved) != sha_value:
        raise PublicationSetError(f"{label} SHA drift: {path_value}")
    return resolved


def _parse_sequence(path_value: str) -> int | None:
    name = Path(path_value).name
    prefix = "publication-surface-revalidation-r"
    suffix = ".json"
    if not name.startswith(prefix) or not name.endswith(suffix):
        return None
    middle = name[len(prefix):-len(suffix)]
    if not middle.isdigit() or (len(middle) > 1 and middle.startswith("0")):
        return None
    try:
        return int(middle)
    except ValueError:
        return None


def _is_editorial_record(record: dict[str, Any]) -> bool:
    return (
        record.get("reason_class") == EDITORIAL_REASON
        and record.get("kind") == EDITORIAL_KIND
    )


def _is_legacy_record(record: dict[str, Any]) -> bool:
    return record.get("reason_class") == LEGACY_REASON and "kind" not in record


def before_active_digest(effective7: dict[str, Any], candidate_ref: dict[str, Any] | None) -> str:
    """Canonical SHA of sorted effective seven rows + exact observed Candidate ref/null.

    Recomputed from before-State/proposal/retention-derived effective7 plus
    candidate nullable (file-verified by caller), never just caller value
    acceptance. Deterministic via core.sha256_object with sorted keys.
    """
    if not isinstance(effective7, dict):
        raise PublicationSetError("before_active_digest requires effective7 mapping")
    rows: list[dict[str, str]] = []
    for name in sorted(effective7):
        row = effective7[name]
        if not isinstance(row, dict) or "path" not in row or "sha256" not in row:
            raise PublicationSetError(f"before_active_digest effective row invalid: {name}")
        path_value = row["path"]
        sha_value = row["sha256"]
        if not isinstance(path_value, str) or not path_value:
            raise PublicationSetError(f"before_active_digest effective path invalid: {name}")
        if not isinstance(sha_value, str) or len(sha_value) != 64 or any(c not in "0123456789abcdef" for c in sha_value):
            raise PublicationSetError(f"before_active_digest effective sha invalid: {name}")
        rows.append({"name": name, "path": path_value, "sha256": sha_value})
    if candidate_ref is not None:
        if not isinstance(candidate_ref, dict) or set(candidate_ref) != {"path", "sha256"}:
            raise PublicationSetError("before_active_digest candidate_ref fields invalid")
        cpath = candidate_ref.get("path")
        csha = candidate_ref.get("sha256")
        if not isinstance(cpath, str) or not cpath:
            raise PublicationSetError("before_active_digest candidate path invalid")
        if not isinstance(csha, str) or len(csha) != 64 or any(c not in "0123456789abcdef" for c in csha):
            raise PublicationSetError("before_active_digest candidate sha invalid")
        candidate_payload: dict[str, Any] | None = {"path": cpath, "sha256": csha}
    else:
        candidate_payload = None
    return core.sha256_object({"effective": rows, "candidate": candidate_payload})


def validate_seal(repo_root: Path, set_path: Path | str) -> dict[str, Any]:
    """Validate immutable publication set seal: schema, 15 files, cross-bindings.

    Checks actual reference path/hash/bytes, seal self-hash, declared layout,
    bundle external result refs and seal chains. No semantic replay (no QA
    re-execution, no review reasoning). Returns loaded seal dict.
    """
    root = repo_root.resolve()
    rel: str
    if isinstance(set_path, Path):
        try:
            rel = str(set_path.resolve().relative_to(root))
        except ValueError:
            # Absolute outside or relative: require repo-local via core helper.
            rel = str(set_path)
            if Path(rel).is_absolute():
                raise PublicationSetError(f"seal path escapes repository: {set_path}")
    else:
        rel = str(set_path)
    seal_file = _repo_file(root, rel, "publication set seal")
    try:
        seal = schema_gate.load_and_validate_json(seal_file, root / SEAL_SCHEMA, label="Editorial Publication Set")
    except (OSError, ValueError) as exc:
        raise PublicationSetError(f"publication set seal invalid: {exc}") from exc
    if seal.get("kind") != SEAL_KIND or seal.get("status") != SEAL_STATUS:
        raise PublicationSetError("publication set seal kind/status invalid")
    # Self-hash excluding set_sha256 (same pattern as receipt/bundle self-hash).
    claimed = seal.get("set_sha256")
    if not isinstance(claimed, str) or len(claimed) != 64 or any(c not in "0123456789abcdef" for c in claimed):
        raise PublicationSetError("publication set set_sha256 invalid")
    payload = {k: v for k, v in seal.items() if k != "set_sha256"}
    if core.sha256_object(payload) != claimed:
        raise PublicationSetError("publication set set_sha256 mismatch (not canonical excluding itself)")
    for key in ("proposal_ref", "staged_manifest_ref", "build_record_ref"):
        ref = seal.get(key)
        _check_authority_ref(root, ref, f"publication set {key}")
    roles = seal.get("roles")
    if not isinstance(roles, dict) or set(roles) != set(PUBLICATION_ROLES_15):
        missing = sorted(set(PUBLICATION_ROLES_15) - set(roles) if isinstance(roles, dict) else set(PUBLICATION_ROLES_15))
        extra = sorted(set(roles) - set(PUBLICATION_ROLES_15) if isinstance(roles, dict) else set())
        raise PublicationSetError(f"publication set roles must be exactly 15: missing={missing} extra={extra}")
    seen_paths: set[str] = set()
    for name in PUBLICATION_ROLES_15:
        ref = roles[name]
        resolved = _check_file_ref(root, ref, f"publication set role {name}")
        if ref["path"] in seen_paths:
            raise PublicationSetError(f"publication set duplicated role path: {ref['path']}")
        seen_paths.add(ref["path"])
        _ = resolved
    # Cross-binding: all JSON roles carrying issue_id must agree; seal refs agree.
    seal_issue = seal.get("issue_id")
    for name in PUBLICATION_ROLES_15:
        ref = roles[name]
        # Only JSON roles can carry issue_id; PDFs/logs/digests/bib/style are bytes-only.
        # Attempt JSON load; non-JSON is not an error here (bytes already verified).
        try:
            doc = core.load_json(root / ref["path"])
        except (OSError, ValueError):
            continue
        if isinstance(doc, dict) and "issue_id" in doc and doc.get("issue_id") != seal_issue:
            raise PublicationSetError(f"publication set role {name} issue_id mismatch")
    # Bundle external result refs: deterministic check results must exist/hash-match.
    try:
        bundle_ref = roles["quality-regression-bundle"]
        bundle_path = root / bundle_ref["path"]
        bundle = schema_gate.load_and_validate_json(bundle_path, root / BUNDLE_SCHEMA, label="Editorial QA bundle")
    except (OSError, ValueError) as exc:
        raise PublicationSetError(f"publication set QA bundle invalid: {exc}") from exc
    if bundle.get("issue_id") != seal_issue:
        raise PublicationSetError("publication set QA bundle issue_id mismatch")
    bundle_pdf = bundle.get("pdf", {}) if isinstance(bundle.get("pdf"), dict) else {}
    seal_pdf = roles["publication-pdf"]
    if bundle_pdf.get("sha256") != seal_pdf.get("sha256"):
        raise PublicationSetError("publication set QA bundle PDF does not bind seal publication-pdf")
    for check in bundle.get("checks", []):
        if not isinstance(check, dict):
            raise PublicationSetError("publication set QA bundle check malformed")
        if check.get("status") != "PASS":
            raise PublicationSetError(f"publication set QA bundle check not PASS: {check.get('check_id')}")
        result = check.get("result")
        # DETERMINISTIC checks carry {path,sha256}; semantic/visual carry null.
        if isinstance(result, dict):
            _check_authority_ref(root, result, f"publication set QA check {check.get('check_id')}")
    # Candidate binding: schema + issue + PDF agreement (identity, not approval).
    try:
        candidate_ref = roles["publication-candidate"]
        candidate = schema_gate.load_and_validate_json(
            root / candidate_ref["path"], root / CANDIDATE_SCHEMA, label="Editorial publication candidate"
        )
    except (OSError, ValueError) as exc:
        raise PublicationSetError(f"publication set candidate invalid: {exc}") from exc
    if candidate.get("issue_id") != seal_issue:
        raise PublicationSetError("publication set candidate issue_id mismatch")
    cand_pdf = candidate.get("pdf", {}) if isinstance(candidate.get("pdf"), dict) else {}
    if cand_pdf.get("sha256") != seal_pdf.get("sha256"):
        raise PublicationSetError("publication set candidate PDF does not bind seal publication-pdf")
    return seal


def _load_record_file(repo_root: Path, ref: dict[str, Any], label: str) -> dict[str, Any]:
    _check_authority_ref(repo_root, ref, label)
    path = repo_root.resolve() / ref["path"]
    try:
        record = schema_gate.load_and_validate_json(path, repo_root.resolve() / REVALIDATION_SCHEMA, label="Publication Surface Revalidation")
    except (OSError, ValueError) as exc:
        raise PublicationSetError(f"{label} invalid: {exc}") from exc
    return record


def _walk_chain_backwards(
    repo_root: Path, start_ref: dict[str, Any] | None
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """Walk supersedes links newest->oldest. Returns [(record, ref)] newest first.

    Fail-closed on missing/unknown branch, cycles, depth. Does not validate
    semantics beyond structural load + schema.
    """
    root = repo_root.resolve()
    chain: list[tuple[dict[str, Any], dict[str, Any]]] = []
    seen: set[str] = set()
    current_ref = start_ref
    for _ in range(CHAIN_LIMIT):
        if current_ref is None:
            return chain
        if not isinstance(current_ref, dict) or set(current_ref) != {"path", "sha256"}:
            raise PublicationSetError("supersession link authority fields invalid")
        key = f"{current_ref.get('path')}\0{current_ref.get('sha256')}"
        if key in seen:
            raise PublicationSetError("publication revalidation supersession chain cycle")
        seen.add(key)
        record = _load_record_file(root, current_ref, "superseded revalidation record")
        chain.append((record, {"path": current_ref["path"], "sha256": current_ref["sha256"]}))
        nxt = record.get("supersedes")
        if nxt is None:
            return chain
        current_ref = nxt
    raise PublicationSetError("publication revalidation supersession chain too deep")


def _normalize_chain_input(
    chain: list[dict[str, Any]] | None,
) -> list[tuple[dict[str, Any], dict[str, Any] | None]]:
    """Normalize explicit chain param to [(record, ref|None)] in given order.

    Expected order: oldest->newest (chronological). Each item is either a bare
    record dict (with optional _path/_sha256 metadata) or a wrapper
    {"record":..., "path":..., "sha256":...}. Strict: non-empty chain items
    must carry a parseable sequence path; missing/unknown refuses.
    """
    if not chain:
        return []
    normalized: list[tuple[dict[str, Any], dict[str, Any] | None]] = []
    for index, item in enumerate(chain):
        if not isinstance(item, dict):
            raise PublicationSetError(f"canonical anchor chain[{index}] must be an object")
        if "record" in item and isinstance(item["record"], dict) and "path" in item:
            record = item["record"]
            path_value = item.get("path")
            sha_value = item.get("sha256")
            if not isinstance(path_value, str) or not path_value:
                raise PublicationSetError(f"canonical anchor chain[{index}] path invalid (unknown branch refuses)")
            if _parse_sequence(path_value) is None:
                raise PublicationSetError(f"canonical anchor chain[{index}] sequence unknown (unknown branch refuses)")
            ref: dict[str, Any] | None = {"path": path_value, "sha256": sha_value} if isinstance(sha_value, str) else {"path": path_value, "sha256": ""}
            # sha presence checked later against disk when root available; here require shape.
            if not isinstance(sha_value, str) or len(sha_value) != 64:
                raise PublicationSetError(f"canonical anchor chain[{index}] sha256 invalid")
            normalized.append((record, ref))
        elif "prior_checkpoint" in item or "reason_class" in item:
            record = item
            path_value = item.get("_path", item.get("__source_path"))
            sha_value = item.get("_sha256", item.get("__source_sha256"))
            if not isinstance(path_value, str) or not path_value:
                raise PublicationSetError(f"canonical anchor chain[{index}] missing source path (unknown branch refuses)")
            if _parse_sequence(path_value) is None:
                raise PublicationSetError(f"canonical anchor chain[{index}] sequence unknown (unknown branch refuses)")
            if not isinstance(sha_value, str) or len(sha_value) != 64:
                raise PublicationSetError(f"canonical anchor chain[{index}] missing source sha256")
            normalized.append((record, {"path": path_value, "sha256": sha_value}))
        else:
            raise PublicationSetError(f"canonical anchor chain[{index}] unrecognized shape (unknown branch refuses)")
    return normalized


def derive_canonical_anchor(
    repo_root: Path, cfg: dict[str, Any], state: dict[str, Any], chain: list[dict[str, Any]]
) -> dict[str, Any]:
    """Derive canonical anchor from validation checkpoint + legacy prefix.

    Rules: no legacy before first activation -> original validation checkpoint.
    Otherwise latest legacy immediately preceding first activation. Repeated
    activations retain same anchor. Legacy after editorial refuses. Each legacy
    link validated cumulative against original checkpoint under legacy
    semantics (prior_sha must equal original, not incremental rollforward).
    """
    root = repo_root.resolve()
    if not isinstance(state, dict):
        raise PublicationSetError("derive_canonical_anchor requires State mapping")
    validation_ref = (state.get("checkpoint_provenance") or {}).get("validation")
    if not isinstance(validation_ref, dict) or set(validation_ref) != {"path", "sha256"}:
        raise PublicationSetError("derive_canonical_anchor requires exact validation checkpoint reference")
    # Verify validation checkpoint file still present/hash (historical, immutable).
    _check_authority_ref(root, validation_ref, "derive canonical anchor validation checkpoint")
    try:
        prior_record = schema_gate.load_and_validate_json(
            root / validation_ref["path"], root / CHECKPOINT_SCHEMA, label="derive anchor prior Stage Checkpoint"
        )
    except (OSError, ValueError) as exc:
        raise PublicationSetError(f"derive canonical anchor prior checkpoint unreadable: {exc}") from exc
    original_map: dict[tuple[str, str], str] = {}
    for row in prior_record.get("artifacts", []):
        if not isinstance(row, dict):
            raise PublicationSetError("derive canonical anchor prior artifacts malformed")
        key = (row.get("name"), row.get("path"))
        if key in original_map:
            raise PublicationSetError("derive canonical anchor prior checkpoint duplicate artifact")
        original_map[key] = row.get("sha256")

    normalized = _normalize_chain_input(chain)
    if not normalized:
        return {"kind": "VALIDATION_CHECKPOINT", "ref": {"path": validation_ref["path"], "sha256": validation_ref["sha256"]}}

    # Verify files + basic identities in given (oldest->newest) order.
    issue_id = state.get("issue_id")
    previous_instant = None
    sequences: list[int] = []
    kinds: list[str] = []
    for index, (record, ref) in enumerate(normalized):
        if not isinstance(record, dict):
            raise PublicationSetError(f"canonical anchor chain[{index}] record must be an object")
        if record.get("issue_id") != issue_id:
            raise PublicationSetError("canonical anchor chain issue identity mismatch")
        if record.get("prior_checkpoint") != validation_ref:
            raise PublicationSetError("canonical anchor chain prior checkpoint mismatch (must bind original validation)")
        try:
            instant = core.parse_instant(str(record.get("recorded_at", "")))
        except ValueError as exc:
            raise PublicationSetError(f"canonical anchor chain[{index}] recorded_at invalid: {exc}") from exc
        if previous_instant is not None and instant < previous_instant:
            raise PublicationSetError("canonical anchor chain chronology invalid (must be nondecreasing)")
        previous_instant = instant
        assert ref is not None
        seq = _parse_sequence(ref["path"])
        assert seq is not None
        sequences.append(seq)
        # Verify file bytes identical.
        resolved = _repo_file(root, ref["path"], f"canonical anchor chain[{index}]")
        if core.sha256_file(resolved) != ref.get("sha256"):
            raise PublicationSetError(f"canonical anchor chain[{index}] SHA drift")
        # Re-load via schema to ensure branch validity (no trust of passed dict bytes).
        try:
            on_disk = schema_gate.load_and_validate_json(resolved, root / REVALIDATION_SCHEMA, label="canonical anchor chain record")
        except (OSError, ValueError) as exc:
            raise PublicationSetError(f"canonical anchor chain[{index}] on-disk invalid: {exc}") from exc
        if on_disk != record:
            raise PublicationSetError(f"canonical anchor chain[{index}] passed bytes differ from disk (must be byte-identical)")
        reason = record.get("reason_class")
        if reason == LEGACY_REASON:
            kinds.append("legacy")
        elif reason == EDITORIAL_REASON:
            if record.get("kind") != EDITORIAL_KIND:
                raise PublicationSetError(f"canonical anchor chain[{index}] editorial kind invalid (unknown branch refuses)")
            kinds.append("editorial")
        else:
            raise PublicationSetError(f"canonical anchor chain[{index}] reason class unrecognized (unknown branch refuses)")

    for i in range(1, len(sequences)):
        if sequences[i] <= sequences[i - 1]:
            raise PublicationSetError("canonical anchor chain sequence must be strictly increasing")
    if len(normalized) > CHAIN_LIMIT:
        raise PublicationSetError("canonical anchor chain too deep")
    # No duplicate links.
    seen_refs = set()
    for _, ref in normalized:
        assert ref is not None
        key = (ref["path"], ref["sha256"])
        if key in seen_refs:
            raise PublicationSetError("canonical anchor chain duplicate link")
        seen_refs.add(key)

    first_editorial = next((i for i, k in enumerate(kinds) if k == "editorial"), None)
    if first_editorial is not None and any(k == "legacy" for k in kinds[first_editorial + 1:]):
        raise PublicationSetError("mixed chain with later legacy successor unsupported (fail-closed, not canonical fallback)")

    legacy_prefix = normalized[:first_editorial] if first_editorial is not None else normalized
    # Cumulative legacy validation: each legacy record's union must equal original.
    for index, (record, _ref) in enumerate(legacy_prefix):
        superseded = record.get("superseded_artifacts", [])
        preserved = record.get("preserved_artifacts", [])
        if not isinstance(superseded, list) or not isinstance(preserved, list):
            raise PublicationSetError(f"canonical anchor legacy[{index}] rows malformed")
        effective: dict[tuple[str, str], str] = {}
        seen: set[tuple[str, str]] = set()
        for row in superseded:
            if not isinstance(row, dict):
                raise PublicationSetError(f"canonical anchor legacy[{index}] superseded row malformed")
            key = (row.get("name"), row.get("path"))
            if key in seen:
                raise PublicationSetError(f"canonical anchor legacy[{index}] duplicates artifact")
            seen.add(key)
            original_sha = original_map.get(key)
            if original_sha is None:
                raise PublicationSetError(f"canonical anchor legacy[{index}] supersedes unknown prior artifact")
            if row.get("prior_sha256") != original_sha:
                raise PublicationSetError(
                    f"canonical anchor legacy[{index}] prior SHA mismatch (must be cumulative against original, not incremental)"
                )
            effective[key] = row.get("new_sha256")
        for row in preserved:
            if not isinstance(row, dict):
                raise PublicationSetError(f"canonical anchor legacy[{index}] preserved row malformed")
            key = (row.get("name"), row.get("path"))
            if key in seen:
                raise PublicationSetError(f"canonical anchor legacy[{index}] duplicates artifact")
            seen.add(key)
            original_sha = original_map.get(key)
            if original_sha is None or row.get("sha256") != original_sha:
                raise PublicationSetError(f"canonical anchor legacy[{index}] preserved artifact mismatch (must equal original)")
            effective[key] = row.get("sha256")
        if set(effective) != set(original_map):
            raise PublicationSetError(f"canonical anchor legacy[{index}] row union differs from original checkpoint")

    if not legacy_prefix:
        return {"kind": "VALIDATION_CHECKPOINT", "ref": {"path": validation_ref["path"], "sha256": validation_ref["sha256"]}}
    _last_record, last_ref = legacy_prefix[-1]
    assert last_ref is not None
    return {"kind": "LEGACY_REVALIDATION", "ref": {"path": last_ref["path"], "sha256": last_ref["sha256"]}}


def validate_activation_record(repo_root: Path, record_path: Path | str) -> dict[str, Any]:
    """Validate editorial activation record: schema, seal, proposal/retention, digest.

    Historical branch never requires old State hash at live path; validates via
    retained exact COPY. Before digest recomputed from before-effective7 +
    candidate (not caller acceptance). Returns loaded record.
    """
    root = repo_root.resolve()
    rel = str(record_path.resolve().relative_to(root)) if isinstance(record_path, Path) and record_path.is_absolute() else str(record_path)
    # Allow absolute under root or repo-relative string.
    if isinstance(record_path, Path) and record_path.is_absolute():
        try:
            rel = str(record_path.resolve().relative_to(root))
        except ValueError as exc:
            raise PublicationSetError(f"activation record escapes repository: {record_path}") from exc
    record_file = _repo_file(root, rel, "activation record")
    try:
        record = schema_gate.load_and_validate_json(record_file, root / REVALIDATION_SCHEMA, label="Editorial Publication Activation")
    except (OSError, ValueError) as exc:
        raise PublicationSetError(f"activation record invalid: {exc}") from exc
    if not _is_editorial_record(record):
        raise PublicationSetError("activation record is not editorial branch (legacy handled separately; no fake legacy rows)")
    # prior_checkpoint + set_ref + anchor + supersedes shape checks via file existence.
    _check_authority_ref(root, record.get("prior_checkpoint"), "activation prior checkpoint")
    set_ref = record.get("set_ref")
    _check_authority_ref(root, set_ref, "activation set_ref")
    # Seal must validate (15 files, bundle refs, chains).
    try:
        seal = validate_seal(root, root / set_ref["path"])
    except PublicationSetError as exc:
        raise PublicationSetError(f"activation set seal invalid: {exc}") from exc
    # Verify seal path matches set_ref path (exact binding, no alternate).
    if seal.get("issue_id") != record.get("issue_id"):
        raise PublicationSetError("activation/set issue_id mismatch")
    # Canonical anchor shape + file binding.
    anchor = record.get("canonical_anchor")
    if not isinstance(anchor, dict) or set(anchor) != {"kind", "ref"}:
        raise PublicationSetError("activation canonical_anchor fields invalid")
    if anchor.get("kind") not in ("VALIDATION_CHECKPOINT", "LEGACY_REVALIDATION"):
        raise PublicationSetError("activation canonical_anchor kind invalid")
    _check_authority_ref(root, anchor.get("ref"), "activation canonical_anchor ref")
    # before_state_ref: shape only here (no live-hash equality after activation).
    before_state = record.get("before_state_ref")
    if not isinstance(before_state, dict) or set(before_state) != {"path", "sha256"}:
        raise PublicationSetError("activation before_state_ref fields invalid")
    for key in ("path", "sha256"):
        if not isinstance(before_state.get(key), str) or not before_state.get(key):
            raise PublicationSetError("activation before_state_ref invalid")
    if len(before_state["sha256"]) != 64 or any(c not in "0123456789abcdef" for c in before_state["sha256"]):
        raise PublicationSetError("activation before_state_ref sha256 invalid")
    # before_candidate_ref: nullable; if present, historical file must still exist/hash-match
    # (old canonical Candidate stays byte-identical, pinned historical input).
    before_cand = record.get("before_candidate_ref")
    if before_cand is not None:
        _check_authority_ref(root, before_cand, "activation before_candidate_ref")
    digest_value = record.get("before_active_digest")
    if not isinstance(digest_value, str) or len(digest_value) != 64 or any(c not in "0123456789abcdef" for c in digest_value):
        raise PublicationSetError("activation before_active_digest invalid")
    # supersedes: nullable; if present, file must exist/hash-match (immutable history).
    supersedes = record.get("supersedes")
    if supersedes is not None:
        _check_authority_ref(root, supersedes, "activation supersedes")
    # Establishment + core + recorded_at strictness (schema already enforces shape;
    # re-check pre-decision sanctions explicitly for clear errors).
    establishment = record.get("establishment", {})
    for key, expected in (
        ("lifecycle", "VALIDATED_DRAFT"),
        ("architecture_review", "approved"),
        ("publication_preview", "pending"),
        ("freeze", "pending"),
        ("release", "pending"),
    ):
        if establishment.get(key) != expected:
            raise PublicationSetError(f"activation establishment not pre-decision sanctioned: {key}")
    try:
        core.parse_instant(str(record.get("recorded_at", "")))
        core.parse_instant(str(establishment.get("recorded_at", "")))
    except ValueError as exc:
        raise PublicationSetError(f"activation recorded_at invalid: {exc}") from exc

    # Proposal / staged / retention identity via seal refs (low-level only, no P1/P2R calls).
    _validate_proposal_retention_identity(root, record, seal)

    # Digest recomputation: derive before-effective7 from prior checkpoint +
    # supersedes-backwards legacy prefix (first-activation path) or prior seal
    # (repeated-activation path), then compare. No caller-value acceptance.
    recomputed = _recompute_before_digest(root, record)
    if recomputed != digest_value:
        raise PublicationSetError("activation before_active_digest mismatch (recomputed from before-effective7 + candidate)")
    return record


def _validate_proposal_retention_identity(root: Path, record: dict[str, Any], seal: dict[str, Any]) -> None:
    before_state = record["before_state_ref"]
    # Seal proposal/staged refs already hash-verified in validate_seal; load as JSON.
    proposal_ref = seal.get("proposal_ref")
    staged_ref = seal.get("staged_manifest_ref")
    try:
        proposal = core.load_json(root / proposal_ref["path"])
    except (OSError, ValueError) as exc:
        raise PublicationSetError(f"activation proposal unreadable: {exc}") from exc
    try:
        staged = core.load_json(root / staged_ref["path"])
    except (OSError, ValueError) as exc:
        raise PublicationSetError(f"activation staged manifest unreadable: {exc}") from exc
    if not isinstance(proposal, dict) or not isinstance(staged, dict):
        raise PublicationSetError("activation proposal/staged must be JSON objects")
    if proposal.get("issue_id") != record.get("issue_id") or staged.get("issue_id") != record.get("issue_id"):
        raise PublicationSetError("activation proposal/staged issue identity mismatch")
    # Proposal basis.state_ref must equal activation before_state_ref.
    proposal_basis = proposal.get("basis", {}) if isinstance(proposal.get("basis"), dict) else {}
    if proposal_basis.get("state_ref") != before_state:
        raise PublicationSetError("activation before_state_ref must equal bound proposal basis State ref")
    # Staged must reference same proposal (path+sha) and carry scope_review_ref file.
    staged_proposal = staged.get("proposal_ref")
    if isinstance(staged_proposal, dict) and "path" in staged_proposal and "sha256" in staged_proposal:
        if staged_proposal.get("path") != proposal_ref.get("path") or staged_proposal.get("sha256") != proposal_ref.get("sha256"):
            raise PublicationSetError("activation staged proposal_ref must equal seal proposal_ref")
    scope_ref = staged.get("scope_review_ref")
    if not isinstance(scope_ref, dict) or set(scope_ref) != {"path", "sha256"}:
        raise PublicationSetError("activation staged scope_review_ref fields invalid")
    _check_authority_ref(root, scope_ref, "activation staged scope_review_ref")
    # Retention via staged retention_manifest_ref.
    retention_ref = staged.get("retention_manifest_ref")
    if not isinstance(retention_ref, dict) or set(retention_ref) != {"path", "sha256"}:
        raise PublicationSetError("activation staged retention_manifest_ref fields invalid")
    _check_authority_ref(root, retention_ref, "activation retention manifest")
    try:
        retention = core.load_json(root / retention_ref["path"])
    except (OSError, ValueError) as exc:
        raise PublicationSetError(f"activation retention unreadable: {exc}") from exc
    if not isinstance(retention, dict):
        raise PublicationSetError("activation retention must be a JSON object")
    retention_basis = retention.get("basis", {}) if isinstance(retention.get("basis"), dict) else {}
    if retention_basis.get("state_ref") != before_state:
        raise PublicationSetError("activation before_state_ref must equal P2R retained basis State ref")
    # Retained exact COPY bytes: find COPY row for before-State path.
    rows = retention.get("rows", [])
    if not isinstance(rows, list):
        raise PublicationSetError("activation retention rows must be an array")
    state_row = None
    for row in rows:
        if not isinstance(row, dict):
            continue
        if row.get("path") == before_state.get("path"):
            state_row = row
            break
    if state_row is None:
        raise PublicationSetError("activation retention missing before-State row (retained COPY required)")
    if state_row.get("sha256") != before_state.get("sha256"):
        raise PublicationSetError("activation retention before-State sha mismatch")
    if state_row.get("policy") == "COPY_BEFORE_REPLACEMENT":
        for key in ("retained_dest", "retained_sha256", "retained_byte_count"):
            if key not in state_row:
                raise PublicationSetError("activation retention COPY row missing retained copy fields")
        retained_dest = state_row["retained_dest"]
        retained_sha = state_row["retained_sha256"]
        retained_size = state_row["retained_byte_count"]
        resolved = _repo_file(root, retained_dest, "activation retained State COPY")
        if core.sha256_file(resolved) != retained_sha:
            raise PublicationSetError("activation retained State COPY SHA drift")
        try:
            actual_size = resolved.stat().st_size
        except OSError as exc:
            raise PublicationSetError(f"activation retained State COPY stat failed: {exc}") from exc
        if actual_size != retained_size:
            raise PublicationSetError("activation retained State COPY byte count drift")
        # Retained COPY bytes must equal before_state sha (exact COPY of those bytes).
        if retained_sha != before_state.get("sha256"):
            raise PublicationSetError("activation retained State COPY must equal before_state bytes")
    elif state_row.get("policy") == "KEEP_IMMUTABLE":
        retained_ref = state_row.get("retained_ref")
        if not isinstance(retained_ref, dict):
            raise PublicationSetError("activation retention KEEP row missing retained_ref")
        _check_authority_ref(root, retained_ref, "activation retention KEEP State ref")
        if retained_ref.get("sha256") != before_state.get("sha256"):
            raise PublicationSetError("activation retention KEEP State must equal before_state bytes")
    else:
        raise PublicationSetError("activation retention State row policy invalid")


def _recompute_before_digest(root: Path, record: dict[str, Any]) -> str:
    """Recompute before_active_digest from retained-before derivation.

    First activation (supersedes null/legacy): before-effective7 is cumulative
    legacy effective (or original validation 7 when no legacy), derived from
    prior checkpoint + backwards legacy walk. Repeated activation (supersedes
    editorial): before-effective7 is prior seal's 7 subset. Before candidate is
    record's before_candidate_ref (already file-verified). No caller digest
    acceptance.
    """
    prior_ref = record["prior_checkpoint"]
    try:
        prior_record = schema_gate.load_and_validate_json(
            root / prior_ref["path"], root / CHECKPOINT_SCHEMA, label="before-digest prior Stage Checkpoint"
        )
    except (OSError, ValueError) as exc:
        raise PublicationSetError(f"before-digest prior checkpoint unreadable: {exc}") from exc
    original_7: dict[str, Any] = {}
    for row in prior_record.get("artifacts", []):
        if not isinstance(row, dict):
            continue
        name = row.get("name")
        if name in PUBLICATION_ROLES_7 and name not in original_7:
            original_7[name] = {"path": row.get("path"), "sha256": row.get("sha256")}
    if set(original_7) != set(PUBLICATION_ROLES_7):
        raise PublicationSetError("before-digest prior checkpoint missing seven publication roles")

    supersedes = record.get("supersedes")
    before_cand = record.get("before_candidate_ref")
    if supersedes is None:
        # First record: before-effective is original 7.
        return before_active_digest(original_7, before_cand)
    # Walk backwards to classify predecessor.
    try:
        prev_record = _load_record_file(root, supersedes, "before-digest predecessor")
    except PublicationSetError as exc:
        raise PublicationSetError(f"before-digest predecessor invalid: {exc}") from exc
    if _is_legacy_record(prev_record):
        # Before-effective is cumulative legacy effective: latest legacy in full
        # backwards chain (walk to oldest, then take latest legacy before first editorial).
        full_backwards = _walk_chain_backwards(root, record.get("supersedes"))
        # full_backwards is newest->oldest starting at predecessor.
        # Collect legacy prefix from oldest side: reverse to oldest->newest.
        chronological = list(reversed(full_backwards))
        # Append current record? Current is editorial, so legacy prefix is all legacy in chronological.
        legacy_records = [(rec, ref) for rec, ref in chronological if _is_legacy_record(rec)]
        if not legacy_records:
            return before_active_digest(original_7, before_cand)
        latest_legacy, _ = legacy_records[-1]
        effective: dict[str, Any] = {}
        for row in list(latest_legacy.get("superseded_artifacts", [])):
            key = row.get("name")
            if key in PUBLICATION_ROLES_7:
                effective[key] = {"path": row.get("path"), "sha256": row.get("new_sha256")}
        for row in list(latest_legacy.get("preserved_artifacts", [])):
            key = row.get("name")
            if key in PUBLICATION_ROLES_7 and key not in effective:
                effective[key] = {"path": row.get("path"), "sha256": row.get("sha256")}
        # Fill any missing 7 from original (should not happen if cumulative valid).
        for name in PUBLICATION_ROLES_7:
            if name not in effective:
                effective[name] = original_7[name]
        return before_active_digest(effective, before_cand)
    if _is_editorial_record(prev_record):
        # Repeated activation: before-effective is prior seal's 7.
        prev_set_ref = prev_record.get("set_ref")
        _check_authority_ref(root, prev_set_ref, "before-digest prior set_ref")
        prev_seal = validate_seal(root, root / prev_set_ref["path"])
        prev_roles = prev_seal.get("roles", {})
        effective2: dict[str, Any] = {}
        for name in PUBLICATION_ROLES_7:
            ref = prev_roles.get(name)
            if not isinstance(ref, dict):
                raise PublicationSetError(f"before-digest prior seal missing {name}")
            effective2[name] = {"path": ref.get("path"), "sha256": ref.get("sha256")}
        return before_active_digest(effective2, before_cand)
    raise PublicationSetError("before-digest predecessor branch unknown (missing/unknown refuses)")


def _default_candidate_path(root: Path, cfg: dict[str, Any], state: dict[str, Any]) -> Path:
    try:
        profile_path = core.repo_local_path(root, state["profile"]["path"], "state.profile.path")
        profile = core.load_json(profile_path)
        source_root = core.repo_local_path(root, profile["paths"]["source_root"], "paths.source_root")
    except (KeyError, TypeError, ValueError, OSError) as exc:
        raise PublicationSetError(f"selection profile/source unresolvable: {exc}") from exc
    return (source_root.resolve() / "publication" / "v2" / "publication-candidate-v2.json")


def _canonical7_from_validation(root: Path, validation_record: dict[str, Any]) -> dict[str, Any]:
    canonical7: dict[str, Any] = {}
    for row in validation_record.get("artifacts", []):
        if not isinstance(row, dict):
            continue
        name = row.get("name")
        if name in PUBLICATION_ROLES_7 and name not in canonical7:
            rel = row.get("path")
            sha = row.get("sha256")
            try:
                resolved = _repo_file(root, rel, f"selection canonical row {name}")
            except PublicationSetError as exc:
                raise PublicationSetError(f"selection canonical row missing: {name}: {exc}") from exc
            if core.sha256_file(resolved) != sha:
                raise PublicationSetError(f"selection canonical row drift: {name}")
            try:
                size = resolved.stat().st_size
            except OSError as exc:
                raise PublicationSetError(f"selection canonical row stat failed: {name}: {exc}") from exc
            canonical7[name] = {"path": rel, "sha256": sha, "byte_count": size, "origin": "ORIGINAL"}
    if set(canonical7) != set(PUBLICATION_ROLES_7):
        missing = sorted(set(PUBLICATION_ROLES_7) - set(canonical7))
        raise PublicationSetError(f"selection validation checkpoint missing seven publication roles: {missing}")
    return canonical7


def resolve_publication_selection(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    """Return identity_selection (derived value, never a bearer/permission).

    Modes CANONICAL | VERSIONED_ACTIVE. Returns all frozen keys:
    mode, record_ref, set_ref, active_set_ref, activation_record_ref,
    canonical_anchor, canonical7, effective7, candidate_ref, candidate_path,
    roles. candidate_path is Path: versioned active path when VERSIONED_ACTIVE,
    else default canonical path (default confers no authority). Empty maps
    before a validation checkpoint exists. All actual reads validate
    shape/hash/path/branch/anchor; invalid pointer never falls back.
    """
    root = repo_root.resolve()
    if not isinstance(state, dict) or not isinstance(cfg, dict):
        raise PublicationSetError("selection requires cfg/state mappings")
    validation_ref = (state.get("checkpoint_provenance") or {}).get("validation")
    default_path: Path
    try:
        default_path = _default_candidate_path(root, cfg, state)
    except PublicationSetError:
        # Profile unresolvable pre-initialization: return canonical empty with
        # best-effort default (no authority). Use root-relative fallback.
        default_path = root / "sources" / str(state.get("issue_id", "unknown")) / "publication" / "v2" / "publication-candidate-v2.json"
        return {
            "mode": "CANONICAL",
            "record_ref": None,
            "set_ref": None,
            "active_set_ref": None,
            "activation_record_ref": None,
            "canonical_anchor": None,
            "canonical7": {},
            "effective7": {},
            "candidate_ref": None,
            "candidate_path": default_path,
            "roles": None,
        }
    if not isinstance(validation_ref, dict) or set(validation_ref) != {"path", "sha256"}:
        return {
            "mode": "CANONICAL",
            "record_ref": None,
            "set_ref": None,
            "active_set_ref": None,
            "activation_record_ref": None,
            "canonical_anchor": None,
            "canonical7": {},
            "effective7": {},
            "candidate_ref": None,
            "candidate_path": default_path,
            "roles": None,
        }
    # Load + verify validation checkpoint (historical, immutable).
    _check_authority_ref(root, validation_ref, "selection validation checkpoint")
    try:
        validation_record = schema_gate.load_and_validate_json(
            root / validation_ref["path"], root / CHECKPOINT_SCHEMA, label="selection prior Stage Checkpoint"
        )
    except (OSError, ValueError) as exc:
        raise PublicationSetError(f"selection validation checkpoint unreadable: {exc}") from exc
    canonical7 = _canonical7_from_validation(root, validation_record)

    pointer = state.get("publication_revalidation_provenance")
    if pointer is None:
        anchor = {"kind": "VALIDATION_CHECKPOINT", "ref": {"path": validation_ref["path"], "sha256": validation_ref["sha256"]}}
        effective7 = dict(canonical7)
        return {
            "mode": "CANONICAL",
            "record_ref": None,
            "set_ref": None,
            "active_set_ref": None,
            "activation_record_ref": None,
            "canonical_anchor": anchor,
            "canonical7": dict(canonical7),
            "effective7": effective7,
            "candidate_ref": None,
            "candidate_path": default_path,
            "roles": None,
        }
    if not isinstance(pointer, dict) or set(pointer) != {"path", "sha256"}:
        raise PublicationSetError("selection State pointer authority fields invalid (no fallback)")
    # Load active record (schema-dispatched, no fallback).
    try:
        record = schema_gate.load_and_validate_json(
            _check_authority_ref(root, pointer, "selection active revalidation authority"),
            root / REVALIDATION_SCHEMA,
            label="selection active revalidation",
        )
    except (OSError, ValueError) as exc:
        raise PublicationSetError(f"selection active record invalid: {exc}") from exc
    if record.get("issue_id") != state.get("issue_id"):
        raise PublicationSetError("selection active record issue identity mismatch")
    if record.get("prior_checkpoint") != validation_ref:
        raise PublicationSetError("selection active record does not bind active validation checkpoint")

    # Walk full chain newest->oldest for anchor/sequence/cycle validation.
    backwards = _walk_chain_backwards(root, pointer)
    chronological_wrapped: list[dict[str, Any]] = []
    for rec, ref in reversed(backwards):
        chronological_wrapped.append({"record": rec, "path": ref["path"], "sha256": ref["sha256"]})
    anchor = derive_canonical_anchor(root, cfg, state, chronological_wrapped)

    if _is_legacy_record(record):
        # CANONICAL with legacy prefix: effective is latest legacy cumulative 7.
        latest = backwards[0][0] if backwards else None
        assert latest is not None
        effective7_legacy: dict[str, Any] = {}
        for row in list(latest.get("superseded_artifacts", [])):
            name = row.get("name")
            if name in PUBLICATION_ROLES_7:
                effective7_legacy[name] = {
                    "path": row.get("path"),
                    "sha256": row.get("new_sha256"),
                    "byte_count": row.get("byte_count"),
                    "origin": "ORIGINAL",
                }
        for row in list(latest.get("preserved_artifacts", [])):
            name = row.get("name")
            if name in PUBLICATION_ROLES_7 and name not in effective7_legacy:
                # preserved rows lack byte_count in legacy schema; stat live (canonical bytes still present).
                rel = row.get("path")
                resolved = _repo_file(root, rel, f"selection legacy preserved {name}")
                try:
                    size = resolved.stat().st_size
                except OSError as exc:
                    raise PublicationSetError(f"selection legacy preserved stat failed: {name}: {exc}") from exc
                effective7_legacy[name] = {"path": rel, "sha256": row.get("sha256"), "byte_count": size, "origin": "ORIGINAL"}
        for name in PUBLICATION_ROLES_7:
            if name not in effective7_legacy:
                effective7_legacy[name] = dict(canonical7[name])
        # Verify anchor matches derived (record has no anchor field; chain-derived is authority).
        return {
            "mode": "CANONICAL",
            "record_ref": {"path": pointer["path"], "sha256": pointer["sha256"]},
            "set_ref": None,
            "active_set_ref": None,
            "activation_record_ref": None,
            "canonical_anchor": anchor,
            "canonical7": dict(canonical7),
            "effective7": effective7_legacy,
            "candidate_ref": None,
            "candidate_path": default_path,
            "roles": None,
        }

    if _is_editorial_record(record):
        # Full editorial validation (seal, proposal/retention, digest, anchor).
        validated = validate_activation_record(root, root / pointer["path"])
        if validated.get("canonical_anchor") != anchor:
            raise PublicationSetError("selection recorded anchor must equal chain-derived identity")
        set_ref = validated.get("set_ref")
        seal = validate_seal(root, root / set_ref["path"])
        # set_ref binding: path+sha must match seal file (already hash-verified).
        if set_ref != {"path": set_ref["path"], "sha256": core.sha256_file(root / set_ref["path"])}:
            raise PublicationSetError("selection set_ref drift")
        active7: dict[str, Any] = {}
        for name in PUBLICATION_ROLES_7:
            ref = seal["roles"][name]
            active7[name] = {"path": ref["path"], "sha256": ref["sha256"], "byte_count": ref["byte_count"], "origin": "ACTIVE"}
        candidate_ref = {"path": seal["roles"]["publication-candidate"]["path"], "sha256": seal["roles"]["publication-candidate"]["sha256"]}
        candidate_path = _repo_file(root, candidate_ref["path"], "selection active candidate")
        return {
            "mode": "VERSIONED_ACTIVE",
            "record_ref": {"path": pointer["path"], "sha256": pointer["sha256"]},
            "set_ref": {"path": set_ref["path"], "sha256": set_ref["sha256"]},
            "active_set_ref": {"path": set_ref["path"], "sha256": set_ref["sha256"]},
            "activation_record_ref": {"path": pointer["path"], "sha256": pointer["sha256"]},
            "canonical_anchor": anchor,
            "canonical7": dict(canonical7),
            "effective7": active7,
            "candidate_ref": candidate_ref,
            "candidate_path": candidate_path,
            "roles": dict(seal["roles"]),
        }

    raise PublicationSetError("selection active record branch unknown (missing/unknown refuses)")


def resolve_publication_artifact_path(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any], role: str) -> Path:
    """Single State-aware role path resolver. Role in 7 + publication-candidate.

    Recomputes from resolve_publication_selection; compares resolved bytes to
    selection pins; refuses unknown/ambiguous/mismatched input, symlink/alias
    escape. Loaders recompute+compare, not only producers. Fixed DRAFT
    templates unchanged (only publication roles resolved here).
    """
    allowed = set(PUBLICATION_ROLES_7) | {"publication-candidate"}
    if role not in allowed:
        raise PublicationSetError(f"unknown publication role: {role}")
    selection = resolve_publication_selection(repo_root, cfg, state)
    root = repo_root.resolve()
    if selection["mode"] == "VERSIONED_ACTIVE":
        if role == "publication-candidate":
            ref = selection["candidate_ref"]
        else:
            ref = {k: v for k, v in selection["effective7"][role].items() if k in ("path", "sha256")}
            # effective7 carries origin/byte_count; strip to authority for path resolution.
            ref = {"path": selection["effective7"][role]["path"], "sha256": selection["effective7"][role]["sha256"]}
        if not isinstance(ref, dict) or "path" not in ref or "sha256" not in ref:
            raise PublicationSetError(f"selection missing active role: {role}")
        resolved = _repo_file(root, ref["path"], f"publication artifact {role}")
        if core.sha256_file(resolved) != ref["sha256"]:
            raise PublicationSetError(f"active publication artifact drift: {role}")
        return resolved
    # CANONICAL: candidate derives default path (no authority); 7 derive canonical7.
    if role == "publication-candidate":
        return _default_candidate_path(root, cfg, state)
    row = selection["effective7"].get(role) if selection.get("effective7") else None
    if row is None:
        # Before validation checkpoint exists, no canonical row; fall back to
        # canonical7 if available else refuse (no bearer).
        raise PublicationSetError(f"canonical publication role not yet established: {role}")
    resolved_c = _repo_file(root, row["path"], f"canonical publication artifact {role}")
    if core.sha256_file(resolved_c) != row["sha256"]:
        raise PublicationSetError(f"canonical publication artifact drift: {role}")
    return resolved_c


def active_candidate_ref(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any]) -> dict[str, Any] | None:
    """Return versioned Candidate ref when VERSIONED_ACTIVE, else None."""
    selection = resolve_publication_selection(repo_root, cfg, state)
    if selection["mode"] != "VERSIONED_ACTIVE":
        return None
    ref = selection.get("candidate_ref")
    if not isinstance(ref, dict):
        return None
    return {"path": ref["path"], "sha256": ref["sha256"]}


def require_active_or_canonical(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any], want_versioned: bool) -> dict[str, Any]:
    """Fail-closed branch guard for revised-mode refusal (R1/wrapper/build).

    want_versioned True requires VERSIONED_ACTIVE, False requires CANONICAL.
    Returns selection on success; raises otherwise (call before destructive action).
    """
    selection = resolve_publication_selection(repo_root, cfg, state)
    is_versioned = selection["mode"] == "VERSIONED_ACTIVE"
    if want_versioned and not is_versioned:
        raise PublicationSetError("operation requires versioned active publication selection (canonical present)")
    if not want_versioned and is_versioned:
        raise PublicationSetError("canonical operation refused in revised mode (use versioned editorial operation)")
    return selection


def assert_canonical_publication_mode(repo_root: Path, cfg: dict[str, Any], state: dict[str, Any]) -> None:
    """Raise on revised/invalid (before writes). Canonical writers call first."""
    require_active_or_canonical(repo_root, cfg, state, want_versioned=False)
