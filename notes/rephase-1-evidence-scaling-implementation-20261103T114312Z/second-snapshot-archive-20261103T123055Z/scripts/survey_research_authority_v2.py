#!/usr/bin/env python3
"""DM022 pre-Architecture research authority (LOW, detached, PATHS-only) — A2 correction.

Binding: contract a345bb95 INCLUDING S11, pre-code assessment S5, precode packet
README, mandatory astra-precode-gate-resolution INCLUDING S5 (FULL 0425c530/13788B),
independent readiness SS8-9 FINAL-BINDING, then R3 (overridden by) R4 + literal 5
schemas, R5 families, R6 roles, then ROOT.

Role (R4 B1, coordination): detached path-reloading validation + pure content
computation + passive guard/completion verification. NEVER:

- accepts caller State/ledger/completeness/proof dictionaries as authority
  (public entries take repo_root + PATHS only; private state-dict helpers are
  structural-only and run only after the caller's own facade has already called
  public agent.validate_agent_state);
- calls agent.validate_agent_state, production.verify_state_basis, HIGH mutators,
  guard claim/release, or canonical/State/slot mutation;
- writes any file (pure builders return dict payloads + planned file maps;
  HIGH alone performs exclusive writes).

Top-level imports (exact, B1 leaf rule): ONLY core shape-only symbols
(repo_local_path, sha256_file, sha256_object, sha256_bytes, json_bytes,
load_json, parse_instant, iso_utc) and schema_gate plus stdlib. Every
evidence/screening/completeness access is function-local and calls ONLY the
real pure content cores with exact signatures — including the detached
record/card/view builders in survey_evidence_v2
(validate_research_record_content, build_research_card_content,
build_research_view_content). LOW never imports run_evidence_v2_interactive
(its top-level pulls agent/agent_tool/discovery plus a circular LOW import);
the interactive runner (B-owned) keeps its own copies for the normal
CANDIDATES_NORMALIZED path. No agent, survey_agent_control_v2,
survey_agent_tool_v2, survey_production_v2.verify_state_basis,
survey_human_gate_v2, operator/bridge, renewal/editorial/publication_set or
guard-coordinator imports at top level or inside LOW bodies. LOW never
validates State.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat as _stat
from pathlib import Path
from typing import Any

from scripts import survey_production_v2 as core
from scripts import survey_schema_v2 as schema_gate

DM022_KIND = "PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1"
DM022_REASON = "REVIEWED_ACCEPTED_UPSTREAM_CORRECTION"
DM022_OPERATION = ("EVIDENCE_REVIEWED", "EVIDENCE_REVIEWED")
DM022_PRODUCER_BOUNDARY = ("CANDIDATES_NORMALIZED", "EVIDENCE_REVIEWED")
DM022_CHECKPOINTS = ("evidence", "materiality", "completeness")
DM022_ARTIFACT_NAMES = (
    "evidence-acceptance",
    "edition-views-acceptance",
    "materiality-ledger",
    "profile-completeness",
)
DM022_PROOF_CHECK_ID = "DM022_SUPERSESSION_PROOF"
DM022_SCHEMA_VERSION = "2.0-rc1"
DM022_GUARD_REL = "orchestration/v2/acceptance-revision.guard.json"

SEVEN_SLOTS = (
    "candidate-matrix-v2.json",
    "candidate-selection-v2.json",
    "architecture-v2.json",
    "architecture-review-summary-v2.json",
    "architecture-review-attention-v2.json",
    "orchestration/v2/interactive/selection-architecture-input.json",
    "orchestration/v2/interactive/selection-architecture-audit.json",
)

OLD_CHECKPOINT_SCHEMA = Path("schemas/stage-checkpoint-v2.schema.json")
DM022_REQUEST_SCHEMA = Path("schemas/dm022-revision-request-v2.schema.json")
DM022_MANIFEST_SCHEMA = Path("schemas/dm022-revision-manifest-v2.schema.json")
DM022_PROOF_SCHEMA = Path("schemas/dm022-revision-proof-v2.schema.json")
DM022_REPORT_SCHEMA = Path("schemas/dm022-preadoption-report-v2.schema.json")
DM022_CHECKPOINT_SCHEMA = Path("schemas/dm022-supersession-checkpoint-v2.schema.json")
STATE_SCHEMA = Path("schemas/survey-production-state.schema.json")
PROFILE_SCHEMA = Path("schemas/survey-production-profile.schema.json")
CONFIG_REL = Path("config/survey-production-v2.json")

# Profile/support P1-P4 (workstream C): ordinary DCP/SCP legacy expectations.
# DCP carries exactly one `discovery-acceptance` NamedRef; SCP carries exactly
# one `screening-acceptance` NamedRef. Both are LEGACY family only (PREARCH at
# DCP/SCP refuses DM022_WRONG_FAMILY). Producer pairs come from the on-disk
# config stage_plan (read as data, never agent authority).
_LEGACY_DCP_NAME = "discovery"
_LEGACY_SCP_NAME = "screening"
_LEGACY_DCP_ARTIFACT = "discovery-acceptance"
_LEGACY_SCP_ARTIFACT = "screening-acceptance"
_CORE_STAGE_REVIEW_ID = "CORE_STAGE_CONTRACT"
_HISTORICAL_REPORT_KEYS = frozenset({
    "schema_version", "check_id", "status", "issue_id", "from_state", "to_state",
    "production_state", "production_profile", "implementation_commit_sha",
    "contract", "artifacts", "recorded_at",
})

_REVISION_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
_HEX40_RE = re.compile(r"^[0-9a-f]{40}$")
_HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


class ResearchAuthorityError(ValueError):
    """Typed LOW failure (fail-closed, no writes, no permission conferred)."""


def _norm_path(value: Any, label: str) -> Path:
    """Normalize a documented Path-or-string filesystem input (no IO).

    Accepts exactly Path or non-empty str and returns a Path. Anything else
    (None, empty string, bytes, other objects) raises the typed error — never
    a bare AttributeError, and never coerced to a different path. Callers
    still apply repo containment (via _repo_rel) and no-follow reads
    (O_NOFOLLOW) after normalization.
    """
    if isinstance(value, Path):
        return value
    if isinstance(value, str) and value:
        return Path(value)
    raise ResearchAuthorityError(f"{label} must be a Path or non-empty string, got {type(value).__name__}")


def _repo_rel(repo_root: Path, rel: str, label: str) -> Path:
    if not isinstance(rel, str) or not rel or "\\" in rel:
        raise ResearchAuthorityError(f"{label} must be a repository-relative path: {rel!r}")
    if rel.startswith("/") or ".." in Path(rel).parts:
        raise ResearchAuthorityError(f"{label} escapes repository root: {rel!r}")
    try:
        return core.repo_local_path(repo_root, rel, label)
    except ValueError as exc:
        raise ResearchAuthorityError(f"{label} unsafe: {exc}") from exc


def _lstat_one(path: Path, label: str) -> os.stat_result:
    try:
        return os.lstat(path)
    except OSError as exc:
        raise ResearchAuthorityError(
            f"{label} lstat failed: {path}: errno={exc.errno} ({exc.strerror})"
        ) from exc


def _safe_read_bytes(path: Path, label: str) -> bytes:
    """Passive read with FD/inode identity match (no symlink follow, no TOCTOU)."""
    try:
        lst = os.lstat(path)
    except OSError as exc:
        raise ResearchAuthorityError(
            f"{label} lstat failed: {path}: errno={exc.errno}"
        ) from exc
    if not _stat.S_ISREG(lst.st_mode):
        raise ResearchAuthorityError(
            f"{label} is not a regular file: {path} (mode={oct(lst.st_mode)})"
        )
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise ResearchAuthorityError(
            f"{label} open(O_NOFOLLOW) failed: {path}: errno={exc.errno}"
        ) from exc
    try:
        fst = os.fstat(fd)
        if not _stat.S_ISREG(fst.st_mode):
            raise ResearchAuthorityError(f"{label} fstat is not regular: {path}")
        if (fst.st_dev, fst.st_ino) != (lst.st_dev, lst.st_ino):
            raise ResearchAuthorityError(
                f"{label} inode changed between lstat and open (replaced): {path}"
            )
        chunks: list[bytes] = []
        while True:
            try:
                data = os.read(fd, 65536)
            except OSError as exc:
                raise ResearchAuthorityError(f"{label} read failed: {exc}") from exc
            if not data:
                break
            chunks.append(data)
        return b"".join(chunks)
    finally:
        try:
            os.close(fd)
        except OSError as exc:
            raise ResearchAuthorityError(f"{label} checked close failed: {exc}") from exc


def _strict_parse_object(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = schema_gate.parse_json_strict_bytes(raw, label)
    except Exception as exc:
        raise ResearchAuthorityError(f"{label} strict parse failed: {exc}") from exc
    if not isinstance(value, dict):
        raise ResearchAuthorityError(f"{label} must be a JSON object")
    return value


def _load_validated(rel_path: Path, repo_root: Path, schema_rel: Path, label: str) -> dict[str, Any]:
    rel_path = _norm_path(rel_path, label)
    repo_root = _norm_path(repo_root, "repo_root")
    abs_path = _repo_rel(repo_root, str(rel_path), label) if not rel_path.is_absolute() else rel_path
    raw = _safe_read_bytes(abs_path, label)
    doc = _strict_parse_object(raw, label)
    schema_abs = repo_root / str(schema_rel)
    try:
        schema_gate.validate_instance(doc, schema_abs, label=label)
    except Exception as exc:
        raise ResearchAuthorityError(f"{label} schema validation failed: {exc}") from exc
    return doc


def _self_digest_hex(payload_without_self: dict[str, Any]) -> str:
    return core.sha256_object(payload_without_self)


def _check_self_digest(doc: dict[str, Any], field: str, label: str) -> None:
    claimed = doc.get(field)
    if not isinstance(claimed, str) or not _HEX64_RE.fullmatch(claimed):
        raise ResearchAuthorityError(f"{label} self-digest field {field} invalid")
    body = {k: v for k, v in doc.items() if k != field}
    if _self_digest_hex(body) != claimed:
        raise ResearchAuthorityError(f"{label} self-digest mismatch for {field}")


def _validate_against_report_def(repo_root: Path, def_name: str, instance: Any, label: str) -> None:
    """Validate an instance against a report-schema $defs fragment (EXACT registry).

    Loads the installed report schema strictly (no symlink, duplicate-key
    refusal) and validates `instance` against `#/$defs/<def_name>` with the
    full Draft 2020-12 validator including format checks. Used for the
    embedded completionReceipt/retentionManifest/guardIntentCoord shapes, which
    are $defs-only (never top-level files). jsonschema is imported
    function-locally: it is the already-required runtime validation library
    (schema_gate wraps it), not repo code — no source-closure widening, no
    agent/State, no circularity.
    """
    import jsonschema

    repo_root = _norm_path(repo_root, "repo_root")
    schema_abs = repo_root / str(DM022_REPORT_SCHEMA)
    try:
        schema_doc = schema_gate.load_schema(schema_abs)
    except Exception as exc:
        raise ResearchAuthorityError(f"{label} report schema unloadable: {exc}") from exc
    defs = schema_doc.get("$defs")
    if not isinstance(defs, dict) or def_name not in defs:
        raise ResearchAuthorityError(f"{label} report $defs/{def_name} missing from registry")
    combined = {"$defs": defs, "$ref": f"#/$defs/{def_name}"}
    try:
        jsonschema.Draft202012Validator(combined, format_checker=jsonschema.FormatChecker()).validate(instance)
    except jsonschema.ValidationError as exc:
        raise ResearchAuthorityError(
            f"{label} fails report $defs/{def_name}: {list(exc.absolute_path)}: {exc.message}"
        ) from exc
    except ResearchAuthorityError:
        raise
    except Exception as exc:
        raise ResearchAuthorityError(f"{label} def validation error: {exc}") from exc


def _sized_ref_shape(ref: Any, label: str) -> dict[str, Any]:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256", "byte_count"}:
        raise ResearchAuthorityError(f"{label} SizedRef fields invalid")
    if not isinstance(ref["path"], str) or not ref["path"] or "\\" in ref["path"]:
        raise ResearchAuthorityError(f"{label} SizedRef path invalid")
    if not isinstance(ref["sha256"], str) or not _HEX64_RE.fullmatch(ref["sha256"]):
        raise ResearchAuthorityError(f"{label} SizedRef sha256 invalid")
    if not isinstance(ref["byte_count"], int) or ref["byte_count"] < 1:
        raise ResearchAuthorityError(f"{label} SizedRef byte_count invalid")
    return ref


def _artifact_ref_shape(ref: Any, label: str) -> dict[str, Any]:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
        raise ResearchAuthorityError(f"{label} ArtifactRef fields invalid")
    if not isinstance(ref["path"], str) or not ref["path"] or "\\" in ref["path"]:
        raise ResearchAuthorityError(f"{label} ArtifactRef path invalid")
    if not isinstance(ref["sha256"], str) or not _HEX64_RE.fullmatch(ref["sha256"]):
        raise ResearchAuthorityError(f"{label} ArtifactRef sha256 invalid")
    return ref


def _named_ref_shape(ref: Any, label: str) -> dict[str, Any]:
    if not isinstance(ref, dict) or set(ref) != {"name", "path", "sha256"}:
        raise ResearchAuthorityError(f"{label} NamedRef fields invalid")
    if not isinstance(ref["name"], str) or not ref["name"]:
        raise ResearchAuthorityError(f"{label} NamedRef name invalid")
    if not isinstance(ref["path"], str) or not ref["path"] or "\\" in ref["path"]:
        raise ResearchAuthorityError(f"{label} NamedRef path invalid")
    if not isinstance(ref["sha256"], str) or not _HEX64_RE.fullmatch(ref["sha256"]):
        raise ResearchAuthorityError(f"{label} NamedRef sha256 invalid")
    return ref


def _verify_sized_ref_bytes(repo_root: Path, ref: dict[str, Any], label: str) -> bytes:
    repo_root = _norm_path(repo_root, "repo_root")
    abs_path = _repo_rel(repo_root, ref["path"], label)
    raw = _safe_read_bytes(abs_path, label)
    if len(raw) != ref["byte_count"]:
        raise ResearchAuthorityError(
            f"{label} byte_count mismatch: claimed={ref['byte_count']} actual={len(raw)}"
        )
    if hashlib.sha256(raw).hexdigest() != ref["sha256"]:
        raise ResearchAuthorityError(f"{label} SHA drift: {ref['path']}")
    return raw


def is_prearchitecture_record(record: Any) -> bool:
    """Pure PREARCH discriminator (classification read, not adoption)."""
    return (
        isinstance(record, dict)
        and record.get("kind") == DM022_KIND
        and record.get("reason") == DM022_REASON
    )


def is_legacy_candidates_record(record: Any) -> bool:
    """Pure legacy discriminator (no kind key, has from/to)."""
    return (
        isinstance(record, dict)
        and "kind" not in record
        and isinstance(record.get("from_state"), str)
        and isinstance(record.get("to_state"), str)
    )


def load_typed_checkpoint_record(repo_root: Path, path: Path) -> dict[str, Any]:
    """Strict kind dispatch: kind absent -> legacy; PREARCH kind -> DM022.

    Accepts a Path or a repository-relative string (normalized first; release
    and refresh callers pass JSON string refs). Generic parse only: no
    role/producer decision, no State/guard/HEAD read, no caller-flag inference,
    no .get(kind, legacy) fallback. Parsing a valid PREARCH never authorizes
    standing in for validation/freeze/release.
    Returns {"family": "LEGACY"|"PREARCH", "record": dict}.
    """
    repo_root = _norm_path(repo_root, "repo_root")
    path = _norm_path(path, "checkpoint record path")
    target = path if path.is_absolute() else (repo_root / str(path))
    raw = _safe_read_bytes(target, "checkpoint record")
    record = _strict_parse_object(raw, "checkpoint record")
    kind = record.get("kind")
    if kind is None:
        schema_abs = repo_root / str(OLD_CHECKPOINT_SCHEMA)
        try:
            schema_gate.validate_instance(record, schema_abs, label="legacy checkpoint")
        except Exception as exc:
            raise ResearchAuthorityError(f"legacy checkpoint schema invalid: {exc}") from exc
        return {"family": "LEGACY", "record": record}
    if kind == DM022_KIND:
        schema_abs = repo_root / str(DM022_CHECKPOINT_SCHEMA)
        try:
            schema_gate.validate_instance(record, schema_abs, label="PREARCH checkpoint")
        except Exception as exc:
            raise ResearchAuthorityError(f"PREARCH checkpoint schema invalid: {exc}") from exc
        if record.get("reason") != DM022_REASON:
            raise ResearchAuthorityError("PREARCH reason must be REVIEWED_ACCEPTED_UPSTREAM_CORRECTION")
        op = record.get("operation") or {}
        if op.get("from_state") != "EVIDENCE_REVIEWED" or op.get("to_state") != "EVIDENCE_REVIEWED":
            raise ResearchAuthorityError("PREARCH operation must be EVIDENCE_REVIEWED->EVIDENCE_REVIEWED")
        pb = record.get("producer_boundary") or {}
        if pb.get("from_state") != "CANDIDATES_NORMALIZED" or pb.get("to_state") != "EVIDENCE_REVIEWED":
            raise ResearchAuthorityError("PREARCH producer_boundary must be CANDIDATES_NORMALIZED->EVIDENCE_REVIEWED")
        if sorted(record.get("checkpoints", [])) != sorted(DM022_CHECKPOINTS):
            raise ResearchAuthorityError("PREARCH checkpoints must be exactly evidence/materiality/completeness")
        names = sorted(a.get("name") for a in record.get("artifacts", []) if isinstance(a, dict))
        if names != sorted(DM022_ARTIFACT_NAMES):
            raise ResearchAuthorityError("PREARCH artifacts must be exactly the 4 research refs")
        _check_self_digest(record, "supersession_checkpoint_sha256", "PREARCH checkpoint")
        return {"family": "PREARCH", "record": record}
    raise ResearchAuthorityError(f"unknown checkpoint kind refused: {kind!r}")


def _structural_checkpoint_refs(state: dict[str, Any]) -> dict[str, dict[str, str]]:
    prov = state.get("checkpoint_provenance")
    if not isinstance(prov, dict):
        raise ResearchAuthorityError("state.checkpoint_provenance missing")
    refs: dict[str, dict[str, str]] = {}
    for key in DM022_CHECKPOINTS:
        ref = prov.get(key)
        refs[key] = _artifact_ref_shape(ref, f"state.checkpoint_provenance.{key}")
    return refs


def require_same_triplet(state: dict[str, Any], structural: dict[str, Any]) -> None:
    """Enforce the sole-active-selection same-record triplet (pure, no IO)."""
    refs = _structural_checkpoint_refs(state)
    paths = {refs[k]["path"] for k in DM022_CHECKPOINTS}
    shas = {refs[k]["sha256"] for k in DM022_CHECKPOINTS}
    if len(paths) != 1 or len(shas) != 1:
        raise ResearchAuthorityError(
            "DM022 same-record triplet violated: evidence/materiality/completeness "
            "must reference the SAME new checkpoint record"
        )
    if structural.get("checkpoint_sha256") != next(iter(shas)):
        raise ResearchAuthorityError("structural checkpoint sha does not match State triplet")
    if structural.get("checkpoint_path") != next(iter(paths)):
        raise ResearchAuthorityError("structural checkpoint path does not match State triplet")


def _resolve_research_from_state_bytes(repo_root: Path, state: dict[str, Any]) -> dict[str, Any]:
    """Structural-only State-dict helper (no validation, no file content).

    Caller facade MUST have already called public agent.validate_agent_state;
    this helper performs no second validation, no verify_state_basis, no guard
    read. It checks path safety, same-record shape, and kind dispatch only.
    Referenced files are NOT loaded here (see _load_typed_four_refs).
    """
    repo_root = _norm_path(repo_root, "repo_root")
    if not isinstance(state, dict):
        raise ResearchAuthorityError("state must be a dict")
    refs = _structural_checkpoint_refs(state)
    paths = {refs[k]["path"] for k in DM022_CHECKPOINTS}
    shas = {refs[k]["sha256"] for k in DM022_CHECKPOINTS}
    if len(paths) != 1 or len(shas) != 1:
        return {
            "family": "LEGACY",
            "checkpoint_path": None,
            "checkpoint_sha256": None,
            "checkpoint_refs": refs,
        }
    sole_path = next(iter(paths))
    sole_sha = next(iter(shas))
    _repo_rel(repo_root, sole_path, "state checkpoint triplet path")
    if not _HEX64_RE.fullmatch(sole_sha):
        raise ResearchAuthorityError("state checkpoint triplet sha invalid")
    return {
        "family": "UNKNOWN_TRIPLET",
        "checkpoint_path": sole_path,
        "checkpoint_sha256": sole_sha,
        "checkpoint_refs": refs,
    }


def _load_typed_four_refs(repo_root: Path, structural: dict[str, Any]) -> dict[str, Any]:
    """Load the 4 named research artifacts: classification + file/shape checks.

    structural comes from _resolve_research_from_state_bytes (already
    shape-checked). This loader resolves the checkpoint record file, verifies
    FILE sha, dispatches family, and loads each named artifact file with
    lstat+read+hash+schema plus digest-equality, ledger shape/basis-key and
    completeness shape/obligation-shape checks. No agent.validate, no
    verify_state_basis, no guard/HEAD.
    Returns {"family", "record", "artifacts", "artifact_refs"} where
    artifact_refs maps the four role names to NamedRefs (output data only;
    consumers reload bytes themselves via the same path+hash).

    SCOPE CONTRACT (narrow): this is classification + file/shape authority
    only. It does NOT prove ledger row linkage against discoveries, ledger
    basis against live upstream files, completeness closure/provenance, or
    request/manifest lineage — those need request/manifest context and are
    proven by prove_revision_from_paths, check_supersession_record_from_paths,
    write_cleanup_completion postread and require_completion_consistent. No
    acceptance path may treat this loader alone as full acceptance; mutating
    producers and READY entries must go through the FULL paths.
    """
    from scripts import survey_completeness_v2 as completeness_mod
    from scripts import survey_evidence_v2 as evidence_mod

    repo_root = _norm_path(repo_root, "repo_root")
    cp_path = structural.get("checkpoint_path")
    cp_sha = structural.get("checkpoint_sha256")
    if not isinstance(cp_path, str) or not isinstance(cp_sha, str):
        raise ResearchAuthorityError("structural checkpoint ref missing (legacy State?)")
    abs_cp = _repo_rel(repo_root, cp_path, "research checkpoint")
    raw_cp = _safe_read_bytes(abs_cp, "research checkpoint")
    if hashlib.sha256(raw_cp).hexdigest() != cp_sha:
        raise ResearchAuthorityError("research checkpoint FILE sha drift")
    typed = load_typed_checkpoint_record(repo_root, abs_cp)
    record = typed["record"]
    family = typed["family"]
    if family != "PREARCH":
        return {"family": "LEGACY", "record": record, "artifacts": {}, "artifact_refs": {}}
    artifact_rows = record.get("artifacts", [])
    by_name: dict[str, dict[str, Any]] = {}
    for row in artifact_rows:
        _named_ref_shape(row, "PREARCH artifact")
        if row["name"] not in DM022_ARTIFACT_NAMES:
            raise ResearchAuthorityError(f"unexpected artifact name: {row['name']!r}")
        if row["name"] in by_name:
            raise ResearchAuthorityError(f"duplicate artifact name: {row['name']!r}")
        by_name[row["name"]] = {"path": row["path"], "sha256": row["sha256"]}
    if sorted(by_name) != sorted(DM022_ARTIFACT_NAMES):
        raise ResearchAuthorityError("PREARCH artifacts must be exactly the 4 research refs")
    loaded: dict[str, dict[str, Any]] = {}
    for name in DM022_ARTIFACT_NAMES:
        ref = by_name[name]
        abs_art = _repo_rel(repo_root, ref["path"], f"artifact {name}")
        raw_art = _safe_read_bytes(abs_art, f"artifact {name}")
        if hashlib.sha256(raw_art).hexdigest() != ref["sha256"]:
            raise ResearchAuthorityError(f"artifact {name} FILE sha drift")
        loaded[name] = _strict_parse_object(raw_art, f"artifact {name}")
    ev_acc = loaded["evidence-acceptance"]
    vw_acc = loaded["edition-views-acceptance"]
    ledger = loaded["materiality-ledger"]
    comp = loaded["profile-completeness"]
    # File/shape validation via real leaf cores (no State, no guard).
    # Expectations come from the checkpoint record's issue/profile context:
    # issue_id from record, research_profile from the acceptance payloads
    # (must all agree; mismatch refuses).
    issue_id = record.get("issue_id")
    profiles = {ev_acc.get("research_profile"), vw_acc.get("research_profile"), ledger.get("research_profile"), comp.get("research_profile")}
    if len(profiles) != 1 or next(iter(profiles)) not in ("WEEKLY", "THEMATIC", "RETROSPECTIVE_PERIOD"):
        raise ResearchAuthorityError("PREARCH artifact research_profile mismatch")
    research_profile = next(iter(profiles))
    if ev_acc.get("issue_id") != issue_id or vw_acc.get("issue_id") != issue_id:
        raise ResearchAuthorityError("PREARCH artifact issue_id mismatch")
    expectations = {"issue_id": issue_id, "research_profile": research_profile, "canonical_state_path": record.get("before_state", {}).get("path", "")}
    # Resolve the profile file from the checkpoint's profile ref and validate
    # the four artifacts against each other + the profile file (no State
    # recursion, no canonical Discovery/Screening reload here by contract).
    profile_ref = record.get("profile") or {}
    _artifact_ref_shape(profile_ref, "PREARCH profile")
    profile_abs = _repo_rel(repo_root, profile_ref["path"], "PREARCH profile.path")
    profile_raw = _safe_read_bytes(profile_abs, "PREARCH profile")
    if hashlib.sha256(profile_raw).hexdigest() != profile_ref["sha256"]:
        raise ResearchAuthorityError("PREARCH profile FILE sha drift")
    profile_doc = _strict_parse_object(profile_raw, "PREARCH profile")
    # Digest recompute (real algorithms, no constants):
    # evidence result_set digest is over {package_sha256, results sorted}.
    try:
        recomputed_result_set = evidence_mod._evidence_result_set_digest(
            ev_acc["package_sha256"], ev_acc["results"]
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"evidence result_set digest recompute failed: {exc}") from exc
    if recomputed_result_set != ev_acc.get("result_set_sha256"):
        raise ResearchAuthorityError("evidence-acceptance result_set_sha256 mismatch (fabricated digest refused)")
    try:
        recomputed_view_set = evidence_mod._view_set_digest(vw_acc["views"])
    except Exception as exc:
        raise ResearchAuthorityError(f"views view_set digest recompute failed: {exc}") from exc
    if recomputed_view_set != vw_acc.get("view_set_sha256"):
        raise ResearchAuthorityError("views-acceptance view_set_sha256 mismatch (fabricated digest refused)")
    # Ledger shape + basis-key + evidence/view linkage (narrow contract: row
    # linkage vs discoveries and basis vs live upstream files are proven by
    # the FULL paths, not here).
    if set(ledger) != {"schema_version", "issue_id", "research_profile", "basis", "rows"}:
        raise ResearchAuthorityError("materiality-ledger fields invalid (four-ref load)")
    ledger_basis = ledger.get("basis") or {}
    for key in ("production_profile_sha256", "discovery_sha256", "screening_acceptance_sha256", "evidence_acceptance_sha256", "edition_views_acceptance_sha256", "evidence_set_sha256", "edition_view_set_sha256"):
        if key not in ledger_basis:
            raise ResearchAuthorityError(f"materiality-ledger basis missing {key}")
    if ledger_basis.get("evidence_set_sha256") != ev_acc.get("result_set_sha256"):
        raise ResearchAuthorityError("ledger evidence_set_sha256 must equal evidence result_set_sha256")
    if ledger_basis.get("edition_view_set_sha256") != vw_acc.get("view_set_sha256"):
        raise ResearchAuthorityError("ledger edition_view_set_sha256 must equal views view_set_sha256")
    # Completeness via real obligation shape + overall_status logic (no invented COMPLETE).
    if set(comp) != {"schema_version", "issue_id", "research_profile", "basis", "overall_status", "obligations", "residual_limitations", "closure"}:
        raise ResearchAuthorityError("profile-completeness fields invalid (four-ref load)")
    if comp.get("overall_status") not in ("READY", "LIMITED", "INCOMPLETE"):
        raise ResearchAuthorityError("profile-completeness overall_status must be READY/LIMITED/INCOMPLETE (never COMPLETE)")
    for row in comp.get("obligations", []):
        errs = completeness_mod._validate_obligation_shape(
            row,
            set(profile_doc.get("research_scope", {}).get("scope_dimensions", [])),
            {r.get("discovery_id", "") for r in ledger.get("rows", []) if isinstance(r, dict)},
            {t for r in ledger.get("rows", []) for t in r.get("evidence_task_ids", [])},
        )
        if errs:
            raise ResearchAuthorityError(f"completeness obligation invalid: {errs[0]}")
    artifact_refs = {name: {"name": name, "path": by_name[name]["path"], "sha256": by_name[name]["sha256"]} for name in DM022_ARTIFACT_NAMES}
    return {"family": "PREARCH", "record": record, "artifacts": loaded, "artifact_refs": artifact_refs}


def _expected_after_state_bytes(copy_raw: bytes, checkpoint_ref: dict[str, str]) -> bytes:
    """Pure COPY-derived expected-after State bytes (no State read, no authority).

    Takes the retained before-State COPY bytes and returns the same bytes with
    ONLY checkpoint_provenance.{evidence,materiality,completeness} replaced by
    the SAME new checkpoint ref. Used to recompute (never trust) the
    completion's expected_after_state on every verification.
    """
    live = json.loads(copy_raw.decode("utf-8"))
    if not isinstance(live, dict):
        raise ResearchAuthorityError("retained COPY State must be a JSON object")
    live = dict(live)
    prov = dict(live.get("checkpoint_provenance", {}))
    for key in ("evidence", "materiality", "completeness"):
        prov[key] = dict(checkpoint_ref)
    live["checkpoint_provenance"] = prov
    return core.json_bytes(live)


_MAPPED_DM022_CODESET = frozenset({
    # Exact R4 finite-family code delta for DM022 (2 modules + 5 schemas).
    # This is the selected map itself, not an unmapped dependency: manifest
    # tool_pins must equal exactly this set (no caller-arbitrary lists, no
    # silent broadening — a future map change returns to Astra instead).
    "scripts/survey_research_authority_v2.py",
    "scripts/survey_prearchitecture_acceptance_v2.py",
    "schemas/dm022-revision-request-v2.schema.json",
    "schemas/dm022-revision-manifest-v2.schema.json",
    "schemas/dm022-revision-proof-v2.schema.json",
    "schemas/dm022-preadoption-report-v2.schema.json",
    "schemas/dm022-supersession-checkpoint-v2.schema.json",
})

_DM022_SCHEMA_IDS = {
    "schemas/dm022-revision-request-v2.schema.json": "https://example.invalid/schemas/dm022-revision-request-v2.schema.json",
    "schemas/dm022-revision-manifest-v2.schema.json": "https://example.invalid/schemas/dm022-revision-manifest-v2.schema.json",
    "schemas/dm022-revision-proof-v2.schema.json": "https://example.invalid/schemas/dm022-revision-proof-v2.schema.json",
    "schemas/dm022-preadoption-report-v2.schema.json": "https://example.invalid/schemas/dm022-preadoption-report-v2.schema.json",
    "schemas/dm022-supersession-checkpoint-v2.schema.json": "https://example.invalid/schemas/dm022-supersession-checkpoint-v2.schema.json",
}


def _git_read(repo_root: Path, *args: str, raw: bool = False) -> bytes:
    """Read-only git object access (no fetch, no mutation, no HEAD pinning).

    Uses only immutable object reads (cat-file/ls-tree/show) against the
    recorded commit; never the LIVE worktree, never demands HEAD equal the
    recorded epoch, never touches current State. GIT_DIR-style overrides are
    scrubbed so reads always bind the given repo_root.
    """
    import subprocess

    repo_root = _norm_path(repo_root, "repo_root")
    env = {k: v for k, v in os.environ.items() if k not in (
        "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
        "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR",
    )}
    env["GIT_OPTIONAL_LOCKS"] = "0"
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            capture_output=True, env=env, timeout=60,
        )
    except OSError as exc:
        raise ResearchAuthorityError(f"recorded-commit git read failed (no network fetch): {exc}") from exc
    if proc.returncode != 0:
        detail = (proc.stderr.decode("utf-8", "replace") if raw else proc.stderr) if isinstance(proc.stderr, bytes) else proc.stderr
        raise ResearchAuthorityError(f"recorded-commit git read refused (no network fetch): git {' '.join(args)}: {str(detail)[:200]}")
    return proc.stdout


def _verify_own_epoch_commit(repo_root: Path, record: dict[str, Any], manifest: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    """Own-epoch proof against RECORDED commit objects (not stored claims only).

    Verifies, from the repo's git object DB only: the recorded commit exists;
    the manifest tool_pins path set equals EXACTLY the mapped DM022 code set
    (never a caller-arbitrary list); every pinned path is a 100644 blob in
    that commit whose bytes hash to the pinned SHA; schema files carry the
    selected $ids; and Contract8 recomputed from the COMMIT's config/files
    (replicating core.contract_identity byte-for-byte, with profile names
    from the COMMIT's profile bytes resolved via the stored request ref)
    equals both the checkpoint contract and the manifest pins. Historical
    reads never substitute current LIVE tools, never demand HEAD equal the
    recorded epoch, never recurse into current State. No unmapped imports:
    only stdlib subprocess git reads plus already-closed core/schema_gate.
    """
    repo_root = _norm_path(repo_root, "repo_root")
    commit = (record.get("implementation") or {}).get("repository_commit_sha")
    if not isinstance(commit, str) or not _HEX40_RE.fullmatch(commit):
        raise ResearchAuthorityError("adopted checkpoint implementation commit sha invalid")
    pins = (manifest.get("tool_pins") or {})
    if commit != pins.get("repository_commit_sha"):
        raise ResearchAuthorityError("adopted checkpoint implementation != stored manifest tool_pins commit (ownEpoch drift)")
    if not isinstance(pins.get("tool_shas"), list) or not pins["tool_shas"]:
        raise ResearchAuthorityError("stored manifest tool_pins.tool_shas missing")
    pinned = {e.get("path"): e.get("sha256") for e in pins["tool_shas"] if isinstance(e, dict)}
    if set(pinned) != set(_MAPPED_DM022_CODESET):
        raise ResearchAuthorityError(
            f"stored tool pins must equal exactly the mapped DM022 code set (no caller-arbitrary list, no silent broadening): extra={sorted(set(pinned) - set(_MAPPED_DM022_CODESET))} missing={sorted(set(_MAPPED_DM022_CODESET) - set(pinned))}"
        )
    prof_ref = request.get("profile_ref") or {}
    _sized_ref_shape(prof_ref, "request.profile_ref")
    profile_rel = prof_ref["path"]
    _git_read(repo_root, "cat-file", "-e", f"{commit}^{{commit}}")
    config_rel = "config/survey-production-v2.json"
    config_raw = _git_read(repo_root, "show", f"{commit}:{config_rel}")
    try:
        cfg_c = schema_gate.parse_json_strict_bytes(config_raw, "recorded-commit config")
    except Exception as exc:
        raise ResearchAuthorityError(f"recorded-commit config unreadable: {exc}") from exc
    if not isinstance(cfg_c, dict):
        raise ResearchAuthorityError("recorded-commit config must be an object")
    try:
        pipeline_files = list(cfg_c["contract_files"]["pipeline"])
        quality_files = list(cfg_c["contract_files"]["quality"])
    except (KeyError, TypeError) as exc:
        raise ResearchAuthorityError(f"recorded-commit config lacks contract_files: {exc}") from exc
    pipeline_files = pipeline_files + [config_rel, "schemas/survey-production-profile.schema.json", "schemas/survey-production-state.schema.json"]
    # Full needed set: contract inputs (from the COMMIT's own config) + pinned
    # code + the request profile file (names come from commit objects below).
    needed: list[str] = []
    for rel in pipeline_files + quality_files:
        if not isinstance(rel, str) or not rel:
            raise ResearchAuthorityError("recorded-commit contract file list invalid")
        needed.append(rel)
    for rel in sorted(pinned):
        needed.append(rel)
    needed.append(profile_rel)
    out = _git_read(repo_root, "ls-tree", "-r", commit, "--", *needed)
    entries: dict[str, tuple[str, str, str]] = {}
    for line in out.decode("utf-8").splitlines():
        if not line.strip():
            continue
        try:
            meta, path = line.split("\t", 1)
            mode, kind, blob = meta.split(" ", 2)
        except ValueError:
            raise ResearchAuthorityError(f"recorded-commit tree entry unparseable: {line[:120]!r}")
        if path in entries:
            raise ResearchAuthorityError(f"recorded-commit tree lists duplicate path: {path}")
        entries[path] = (mode, kind, blob)
    for rel in needed:
        if rel not in entries:
            raise ResearchAuthorityError(f"recorded-commit tree lacks required path: {rel} (no historical substitution)")
        mode, kind, blob = entries[rel]
        if mode != "100644" or kind != "blob":
            raise ResearchAuthorityError(f"recorded-commit path is not a regular file blob (mode/blob): {rel} ({mode} {kind})")
    # Batch-read all blobs in one subprocess; verify byte SHAs.
    want_blobs = [entries[rel][2] for rel in needed]
    batch_in = "".join(f"{b}\n" for b in want_blobs).encode("utf-8")
    import subprocess as _sp

    env = {k: v for k, v in os.environ.items() if k not in (
        "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
        "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR",
    )}
    env["GIT_OPTIONAL_LOCKS"] = "0"
    try:
        proc = _sp.run(["git", "-C", str(repo_root), "cat-file", "--batch"], input=batch_in, capture_output=True, env=env, timeout=60)
    except OSError as exc:
        raise ResearchAuthorityError(f"recorded-commit batch read failed (no network fetch): {exc}") from exc
    if proc.returncode != 0:
        raise ResearchAuthorityError("recorded-commit batch read refused (no network fetch)")
    blob_bytes: dict[str, bytes] = {}
    stream = proc.stdout
    pos = 0
    for rel, blob in zip(needed, want_blobs):
        nl = stream.find(b"\n", pos)
        if nl < 0:
            raise ResearchAuthorityError(f"recorded-commit batch truncated for: {rel}")
        header = stream[pos:nl].decode("utf-8", "replace").split(" ")
        if len(header) != 3 or header[0] != blob:
            raise ResearchAuthorityError(f"recorded-commit batch header mismatch for: {rel}")
        try:
            size = int(header[2])
        except ValueError:
            raise ResearchAuthorityError(f"recorded-commit batch size invalid for: {rel}")
        start = nl + 1
        data = stream[start:start + size]
        if len(data) != size or stream[start + size:start + size + 1] != b"\n":
            raise ResearchAuthorityError(f"recorded-commit batch body invalid for: {rel}")
        blob_bytes[rel] = data
        pos = start + size + 1
    for rel, pinned_sha in pinned.items():
        if hashlib.sha256(blob_bytes[rel]).hexdigest() != pinned_sha:
            raise ResearchAuthorityError(f"recorded-commit blob bytes do not match pinned SHA (not caller arbitrary list): {rel}")
    # Schema fingerprints: selected $ids on committed schema bytes.
    for rel, expected_id in _DM022_SCHEMA_IDS.items():
        try:
            doc = schema_gate.parse_json_strict_bytes(blob_bytes[rel], f"recorded-commit schema {rel}")
        except Exception as exc:
            raise ResearchAuthorityError(f"recorded-commit schema unreadable: {rel}: {exc}") from exc
        if not isinstance(doc, dict) or doc.get("$id") != expected_id:
            raise ResearchAuthorityError(f"recorded-commit schema fingerprint mismatch ($id): {rel}")
    # Contract8 recomputed byte-for-byte from commit objects (mirrors
    # core.contract_identity + core.aggregate_file_hash exactly). Profile
    # names come from the COMMIT's profile bytes (never LIVE files).
    def _agg(paths: list[str]) -> str:
        digest = hashlib.sha256()
        for r in sorted(paths):
            digest.update(r.encode("utf-8"))
            digest.update(b"\0")
            digest.update(blob_bytes[r])
            digest.update(b"\0")
        return digest.hexdigest()
    try:
        profile_doc = schema_gate.parse_json_strict_bytes(blob_bytes[profile_rel], "recorded-commit profile")
    except Exception as exc:
        raise ResearchAuthorityError(f"recorded-commit profile unreadable: {exc}") from exc
    if not isinstance(profile_doc, dict):
        raise ResearchAuthorityError("recorded-commit profile must be an object")
    research_name = profile_doc.get("research_profile")
    publication_name = profile_doc.get("publication_profile")
    research = (cfg_c.get("research_profiles") or {}).get(research_name) if isinstance(research_name, str) else None
    publication = (cfg_c.get("publication_profiles") or {}).get(publication_name) if isinstance(publication_name, str) else None
    if not isinstance(research, dict) or not isinstance(publication, dict):
        raise ResearchAuthorityError("recorded-commit config lacks the profile named by the recorded profile bytes")
    recomputed = {
        "pipeline_contract_version": cfg_c.get("pipeline_contract_version"),
        "pipeline_contract_sha256": _agg(pipeline_files),
        "quality_contract_version": cfg_c.get("quality_contract_version"),
        "quality_contract_sha256": _agg(quality_files),
        "research_profile_version": research.get("version"),
        "research_profile_sha256": core.sha256_object({"name": research_name, "contract": research}),
        "publication_profile_version": publication.get("version"),
        "publication_profile_sha256": core.sha256_object({"name": publication_name, "contract": publication}),
    }
    if recomputed != record.get("contract"):
        raise ResearchAuthorityError("recomputed own-epoch Contract8 != checkpoint contract (recorded-commit proof, not stored-claim equality)")
    if recomputed != pins.get("contract"):
        raise ResearchAuthorityError("recomputed own-epoch Contract8 != stored manifest tool_pins.contract")
    return {"commit": commit, "blobs": blob_bytes, "config": cfg_c, "contract": recomputed}


def _verify_adopted_graph_full(repo_root: Path, checkpoint_path: str, checkpoint_sha: str) -> dict[str, Any]:
    repo_root = _norm_path(repo_root, "repo_root")
    checkpoint_path = str(_norm_path(checkpoint_path, "checkpoint path"))
    """FULL adopted-graph validation with request/manifest context (no State).

    Loads the PREARCH checkpoint (schema + SELF + family), its four artifacts
    (classification + file/sha + schema + digest + shape checks), then runs
    the COMPLETE content validators with exact signatures on the proposed
    bytes: evidence acceptance, edition-views acceptance, materiality ledger
    (basis + row linkage vs discoveries), profile completeness (obligations +
    closure + named/extra checks), all with the true historical root context
    (root_records/root_path from the DCP acceptance chain) and the bound
    effective Discovery path as the graph discovery argument. Also verifies
    own-epoch pins from stored files only (never current source): the
    checkpoint contract/implementation must equal the stored manifest
    tool_pins (manifest resolved via the checkpoint revision_root). Returns
    the loaded pieces for callers. Raises on any gap — never a partial PASS.
    """
    from scripts import survey_completeness_v2 as completeness_mod
    from scripts import survey_evidence_v2 as evidence_mod

    repo_root = _norm_path(repo_root, "repo_root")
    abs_cp = _repo_rel(repo_root, checkpoint_path, "adopted checkpoint")
    raw_cp = _safe_read_bytes(abs_cp, "adopted checkpoint")
    if hashlib.sha256(raw_cp).hexdigest() != checkpoint_sha:
        raise ResearchAuthorityError("adopted checkpoint FILE sha drift")
    typed = load_typed_checkpoint_record(repo_root, abs_cp)
    if typed["family"] != "PREARCH":
        raise ResearchAuthorityError("adopted checkpoint is not PREARCH family")
    record = typed["record"]
    four = _load_typed_four_refs(
        repo_root,
        {"checkpoint_path": checkpoint_path, "checkpoint_sha256": checkpoint_sha, "checkpoint_refs": {}},
    )
    # Request (own-epoch pins + Discovery/Profile refs come from here, stored).
    req_ref = record.get("request") or {}
    _sized_ref_shape(req_ref, "checkpoint.request")
    req_raw = _verify_sized_ref_bytes(repo_root, req_ref, "checkpoint request")
    request = _strict_parse_object(req_raw, "checkpoint request")
    try:
        schema_gate.validate_instance(request, repo_root / str(DM022_REQUEST_SCHEMA), label="checkpoint request")
    except Exception as exc:
        raise ResearchAuthorityError(f"checkpoint request schema invalid: {exc}") from exc
    if request.get("issue_id") != record.get("issue_id") or request.get("revision_id") != record.get("revision_id"):
        raise ResearchAuthorityError("checkpoint request identity must match record")
    by_name = {r["name"]: r for r in record.get("artifacts", []) if isinstance(r, dict)}
    ev_abs = _repo_rel(repo_root, by_name["evidence-acceptance"]["path"], "adopted evidence acceptance")
    vw_abs = _repo_rel(repo_root, by_name["edition-views-acceptance"]["path"], "adopted views acceptance")
    ledger_abs = _repo_rel(repo_root, by_name["materiality-ledger"]["path"], "adopted ledger")
    comp_abs = _repo_rel(repo_root, by_name["profile-completeness"]["path"], "adopted completeness")
    for key in ("profile_ref", "discovery_ref", "screening_ref"):
        _sized_ref_shape(request.get(key), f"request.{key}")
        _verify_sized_ref_bytes(repo_root, request[key], f"request {key}")
    prof_abs = _repo_rel(repo_root, request["profile_ref"]["path"], "request profile")
    scr_abs = _repo_rel(repo_root, request["screening_ref"]["path"], "request screening")
    # Record-bound bindings BEFORE any historical R/E derivation (R5 §3): the
    # fixed recorded layout revision_root/retention/state-before.json is
    # derived only after the verified checkpoint exact-SHA / request /
    # revision / retention-plan / manifest / before-SHA-size binding below.
    # Never reads request.before_state.path for historical bytes (that logical
    # path is LIVE-owned); never an optional public COPY default.
    rev_root_rel = record.get("revision_root")
    if not isinstance(rev_root_rel, str) or not rev_root_rel:
        raise ResearchAuthorityError("adopted checkpoint revision_root missing")
    if record.get("revision_id") != request.get("revision_id"):
        raise ResearchAuthorityError("adopted checkpoint revision_id must match request revision_id")
    ret_ref = record.get("retention_plan")
    _sized_ref_shape(ret_ref, "checkpoint.retention_plan")
    _verify_sized_ref_bytes(repo_root, ret_ref, "checkpoint retention_plan")
    manifest_abs = _repo_rel(repo_root, f"{rev_root_rel.rstrip('/')}/revision-manifest.json", "stored revision manifest")
    manifest_raw = _safe_read_bytes(manifest_abs, "stored revision manifest")
    manifest = _strict_parse_object(manifest_raw, "stored revision manifest")
    try:
        schema_gate.validate_instance(manifest, repo_root / str(DM022_MANIFEST_SCHEMA), label="stored revision manifest")
    except Exception as exc:
        raise ResearchAuthorityError(f"stored revision manifest schema invalid: {exc}") from exc
    if manifest.get("revision_id") != record.get("revision_id"):
        raise ResearchAuthorityError("stored manifest revision_id must match adopted checkpoint revision_id")
    if manifest.get("revision_root") != rev_root_rel:
        raise ResearchAuthorityError("stored manifest revision_root must match adopted checkpoint revision_root")
    man_req_ref = manifest.get("request")
    _sized_ref_shape(man_req_ref, "stored manifest.request")
    if man_req_ref != req_ref:
        raise ResearchAuthorityError("stored manifest request ref must equal adopted checkpoint request ref")
    before_state_ref = record.get("before_state")
    _sized_ref_shape(before_state_ref, "checkpoint.before_state")
    if (manifest.get("before_state") or {}).get("sha256") != before_state_ref["sha256"]:
        raise ResearchAuthorityError("stored manifest before_state must match adopted checkpoint before_state")
    if manifest.get("before_checkpoint") != request.get("before_checkpoint"):
        raise ResearchAuthorityError(
            "stored manifest before_checkpoint must equal the bound request before_checkpoint "
            "(exact evidence/materiality/completeness ArtifactRef triplet)"
        )
    # Typed retention payload binding (existing full predicates, not a second
    # weaker parser): the retention-plan file must parse as the 7-row
    # inventory and every row must exactly equal the stored manifest
    # retention_snapshots slot row — the same predicate the supersession
    # checker and completion verifier enforce. Only then is the fixed
    # recorded layout revision_root/retention/state-before.json derived.
    ret_abs = _repo_rel(repo_root, ret_ref["path"], "checkpoint retention_plan")
    ret_raw = _safe_read_bytes(ret_abs, "checkpoint retention_plan")
    retention_inventory = _strict_parse_object(ret_raw, "checkpoint retention_plan")
    inv_rows = retention_inventory.get("rows")
    if not isinstance(inv_rows, list) or len(inv_rows) != 7:
        raise ResearchAuthorityError("checkpoint retention_plan inventory must have exactly 7 rows")
    man_snapshots = {r.get("slot"): r for r in manifest.get("retention_snapshots", []) if isinstance(r, dict)}
    if set(man_snapshots) != set(SEVEN_SLOTS):
        raise ResearchAuthorityError("stored manifest retention_snapshots must cover exactly the 7 slots")
    for inv_row in inv_rows:
        if not isinstance(inv_row, dict) or inv_row.get("slot") not in SEVEN_SLOTS:
            raise ResearchAuthorityError(f"checkpoint retention_plan inventory unknown slot: {(inv_row or {}).get('slot')!r}")
        other = man_snapshots.get(inv_row.get("slot"))
        if not isinstance(other, dict) or inv_row != other:
            raise ResearchAuthorityError(
                f"checkpoint retention_plan inventory row != stored manifest snapshot for slot: {inv_row.get('slot')}"
            )
    before_copy_abs = _repo_rel(
        repo_root, f"{rev_root_rel.rstrip('/')}/retention/state-before.json", "retained state-before COPY"
    )
    before_copy_raw = _safe_read_bytes(before_copy_abs, "retained state-before COPY")
    if hashlib.sha256(before_copy_raw).hexdigest() != before_state_ref["sha256"]:
        raise ResearchAuthorityError("retained COPY does not match checkpoint before_state sha")
    if len(before_copy_raw) != before_state_ref["byte_count"]:
        raise ResearchAuthorityError("retained COPY byte_count mismatch vs checkpoint before_state")
    # True historical R/E from the bound COPY + accepted D/S chain (never
    # E-as-R: the request Discovery file alone is E, R comes from the DCP
    # acceptance chain validated inside the loader).
    _adopted_request_abs = _repo_rel(repo_root, req_ref["path"], "checkpoint request path")
    try:
        _adopted_ctx = derive_ordinary_root_effective_context(repo_root, _adopted_request_abs, before_copy_abs)
    except Exception as exc:
        raise ResearchAuthorityError(f"adopted historical root/effective context refused: {exc}") from exc
    discoveries = _adopted_ctx["root_records"]
    disc_abs = _adopted_ctx["root_path"]
    ev_acc = four["artifacts"]["evidence-acceptance"]
    research_profile = ev_acc.get("research_profile")
    expectations = {
        "issue_id": record.get("issue_id"),
        "research_profile": research_profile,
        "canonical_state_path": _adopted_ctx["canonical_state_path"],
    }
    if not expectations["canonical_state_path"]:
        raise ResearchAuthorityError("adopted checkpoint before_state.path missing")
    try:
        evidence_mod._validate_evidence_acceptance_content(repo_root, ev_abs, expectations, discoveries, disc_abs)
    except Exception as exc:
        raise ResearchAuthorityError(f"FULL evidence acceptance invalid: {exc}") from exc
    try:
        evidence_mod._validate_edition_views_acceptance_content(
            repo_root, prof_abs, ev_abs, vw_abs, expectations, discoveries, disc_abs
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"FULL views acceptance invalid: {exc}") from exc
    ledger = four["artifacts"]["materiality-ledger"]
    try:
        evidence_mod._validate_materiality_ledger_content(
            ledger, repo_root, prof_abs, _adopted_ctx["effective_path"], scr_abs, ev_abs, vw_abs,
            expectations, discoveries, disc_abs,
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"FULL materiality ledger invalid: {exc}") from exc
    comp = four["artifacts"]["profile-completeness"]
    try:
        comp_errs = completeness_mod._validate_profile_completeness_content(
            comp, repo_root, prof_abs, _adopted_ctx["effective_path"], scr_abs, ev_abs, vw_abs, ledger_abs,
            expectations, discoveries, disc_abs,
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"FULL profile completeness check failed: {exc}") from exc
    if comp_errs:
        raise ResearchAuthorityError(f"FULL profile completeness invalid: {comp_errs[0]}")
    # Own-epoch pins from STORED files only (never current source): the stored
    # manifest pins (already bound above) are PROVEN against recorded-commit
    # git objects (blob/mode/bytes, schema fingerprints, Contract8 recompute)
    # — not mere stored-claim equality. Historical reads never substitute LIVE
    # tools, never demand HEAD equal the recorded epoch, never recurse into
    # current State.
    _verify_own_epoch_commit(repo_root, record, manifest, request)
    return {
        "record": record,
        "artifacts": four["artifacts"],
        "artifact_refs": four["artifact_refs"],
        "request": request,
        "manifest": manifest,
        "profile_abs": prof_abs,
        "discovery_abs": disc_abs,
        "screening_abs": scr_abs,
        "evidence_abs": ev_abs,
        "views_abs": vw_abs,
        "ledger_abs": ledger_abs,
        "completeness_abs": comp_abs,
    }


def _verify_completion_full(
    repo_root: Path, source_root: Path, checkpoint_ref: dict[str, Any]
) -> dict[str, Any]:
    """FULL completion verification: schema + COPY + triplet + slots (no trust).

    Verifies, from stored files only: checkpoint FILE/sha + PREARCH family;
    completion receipt against the EXACT report $defs/completionReceipt schema;
    checkpoint/issue/revision/nonce cross-bindings; retention inventory (7 rows)
    exactly bound to the stored manifest retention_snapshots; expected_after
    recomputed from the retained COPY + checkpoint ref (byte-compared, never
    trusted); LIVE canonical State reloaded with same-record triplet + FULL
    adopted-graph validation (recomputes triplet_match/artifacts_rehashed
    instead of trusting booleans); seven_plan vs inventory vs current slot
    lstat with legitimate-regeneration tolerance (old-absent slots and
    regenerated new-content/same-byte-new-inode outputs do NOT block; only
    same-inode stale bytes refuse). Returns the verified pieces.
    """
    repo_root = _norm_path(repo_root, "repo_root")
    source_root = _norm_path(source_root, "source_root")
    _artifact_ref_shape(checkpoint_ref, "checkpoint_ref")
    cp_abs = _repo_rel(repo_root, checkpoint_ref["path"], "checkpoint_ref.path")
    cp_rel = str(checkpoint_ref["path"])
    full = _verify_adopted_graph_full(repo_root, cp_rel, checkpoint_ref["sha256"])
    record = full["record"]
    manifest = full["manifest"]
    rev_root_rel = record.get("revision_root", "")
    completion_abs = _repo_rel(repo_root, f"{rev_root_rel.rstrip('/')}/completion/cleanup-completion.json", "cleanup completion")
    completion_raw = _safe_read_bytes(completion_abs, "cleanup completion")
    completion = _strict_parse_object(completion_raw, "cleanup completion")
    _validate_against_report_def(repo_root, "completionReceipt", completion, "cleanup completion")
    if completion.get("checkpoint", {}).get("sha256") != checkpoint_ref["sha256"]:
        raise ResearchAuthorityError("completion checkpoint sha mismatch")
    if completion.get("checkpoint", {}).get("path") != checkpoint_ref["path"]:
        raise ResearchAuthorityError("completion checkpoint path mismatch")
    if completion.get("issue_id") != record.get("issue_id") or completion.get("revision_id") != record.get("revision_id"):
        raise ResearchAuthorityError("completion issue/revision must match adopted checkpoint")
    # Retention inventory: 7 rows, exactly bound to the stored manifest snapshots.
    inv_abs = _repo_rel(repo_root, f"{rev_root_rel.rstrip('/')}/retention/inventory.json", "retention inventory")
    inv_raw = _safe_read_bytes(inv_abs, "retention inventory")
    inventory = _strict_parse_object(inv_raw, "retention inventory")
    inv_rows = inventory.get("rows")
    if not isinstance(inv_rows, list) or len(inv_rows) != 7:
        raise ResearchAuthorityError("retention inventory must have exactly 7 rows")
    man_rows = (manifest.get("retention_snapshots") or [])
    if not isinstance(man_rows, list) or len(man_rows) != 7:
        raise ResearchAuthorityError("stored manifest retention_snapshots must have exactly 7 rows")
    man_by_slot = {r.get("slot"): r for r in man_rows if isinstance(r, dict)}
    seen: set[str] = set()
    for row in inv_rows:
        slot = row.get("slot")
        if slot not in SEVEN_SLOTS:
            raise ResearchAuthorityError(f"retention inventory unknown slot: {slot!r}")
        if slot in seen:
            raise ResearchAuthorityError(f"retention inventory duplicate slot: {slot}")
        seen.add(slot)
        other = man_by_slot.get(slot)
        if not isinstance(other, dict) or row != other:
            raise ResearchAuthorityError(f"retention inventory row != stored manifest snapshot for slot: {slot}")
    # Expected_after recomputed from the retained COPY (never trusted).
    copy_abs = _repo_rel(repo_root, f"{rev_root_rel.rstrip('/')}/retention/state-before.json", "retained state-before COPY")
    copy_raw = _safe_read_bytes(copy_abs, "retained state-before COPY")
    if hashlib.sha256(copy_raw).hexdigest() != (record.get("before_state") or {}).get("sha256"):
        raise ResearchAuthorityError("retained COPY does not match checkpoint before_state")
    expected_raw = _expected_after_state_bytes(copy_raw, {"path": completion["checkpoint"]["path"], "sha256": completion["checkpoint"]["sha256"]})
    if hashlib.sha256(expected_raw).hexdigest() != completion.get("expected_after_state", {}).get("sha256"):
        raise ResearchAuthorityError("completion expected_after_state.sha256 != COPY-derived recomputation")
    if len(expected_raw) != completion.get("expected_after_state", {}).get("byte_count"):
        raise ResearchAuthorityError("completion expected_after_state.byte_count != COPY-derived recomputation")
    # LIVE canonical State: same-record triplet bound to THIS checkpoint, then
    # FULL graph (recomputes postread booleans; forward lifecycle tolerated).
    live_abs = source_root / "production-state.json"
    live_raw = _safe_read_bytes(live_abs, "LIVE canonical state")
    live = _strict_parse_object(live_raw, "LIVE canonical state")
    structural = _resolve_research_from_state_bytes(repo_root, live)
    require_same_triplet(live, structural)
    if structural.get("checkpoint_path") != checkpoint_ref["path"] or structural.get("checkpoint_sha256") != checkpoint_ref["sha256"]:
        raise ResearchAuthorityError("LIVE triplet does not reference this completion checkpoint (stale completion)")
    _verify_adopted_graph_full(repo_root, cp_rel, checkpoint_ref["sha256"])
    # Seven_plan vs inventory vs current slots (B4 regeneration tolerance).
    seven = completion.get("seven_plan", [])
    if not isinstance(seven, list) or len(seven) != 7:
        raise ResearchAuthorityError("completion seven_plan must have exactly 7 rows")
    inv_by_slot = {r.get("slot"): r for r in inv_rows}
    seen_plan: set[str] = set()
    for row in seven:
        slot = row.get("slot")
        if slot not in SEVEN_SLOTS:
            raise ResearchAuthorityError(f"completion seven_plan unknown slot: {slot!r}")
        if slot in seen_plan:
            raise ResearchAuthorityError(f"completion seven_plan duplicate slot: {slot}")
        seen_plan.add(slot)
        if row.get("disposition") not in ("cleared", "absent_legitimate"):
            raise ResearchAuthorityError(f"completion seven_plan disposition invalid for {slot}")
        inv = inv_by_slot.get(slot)
        if inv is None:
            raise ResearchAuthorityError(f"completion seven_plan slot missing from retention inventory: {slot}")
        if inv.get("present"):
            if row.get("disposition") != "cleared":
                raise ResearchAuthorityError(f"seven_plan disposition must be cleared for retained slot: {slot}")
            if row.get("captured_sha") != inv.get("source_sha256") or row.get("copy_sha") != inv.get("copy_sha256"):
                raise ResearchAuthorityError(f"seven_plan captured/copy sha must match retention inventory for slot: {slot}")
        else:
            if row.get("disposition") != "absent_legitimate":
                raise ResearchAuthorityError(f"seven_plan disposition must be absent_legitimate for never-present slot: {slot}")
            if row.get("captured_sha") is not None or row.get("copy_sha") is not None:
                raise ResearchAuthorityError(f"seven_plan shas must be null for never-present slot: {slot}")
        obs = lstat_slot(source_root, slot)
        if not obs["present"]:
            continue
        if not inv.get("present"):
            # Old-absent slot with a present file: legitimate normal
            # regeneration after valid completion (the normal runner recreates
            # all seven outputs, including previously absent ones). Do NOT
            # block READY on this slot; stage validators enforce content.
            continue
        if obs.get("lstat_kind") != "regular":
            raise ResearchAuthorityError(f"DM022_TRANSITION_ACTIVE: nonregular present slot: {slot}")
        try:
            cur_raw = _safe_read_bytes(source_root / slot, f"slot {slot}")
        except ResearchAuthorityError:
            raise ResearchAuthorityError(f"DM022_TRANSITION_ACTIVE: unreadable present slot: {slot}")
        if hashlib.sha256(cur_raw).hexdigest() != inv.get("copy_sha256"):
            # Different bytes: regenerated with new content — allowed.
            continue
        captured_ino = inv.get("source_ino")
        if isinstance(captured_ino, int) and obs.get("ino") != captured_ino:
            # Same bytes but new inode: legitimate same-byte regeneration.
            continue
        raise ResearchAuthorityError(f"DM022_TRANSITION_ACTIVE: stale slot still present: {slot}")
    return {"completion": completion, "inventory": inventory, "record": record, "manifest": manifest}


def resolve_research_authority(repo_root: Path, state_path: Path) -> dict[str, Any]:
    """Public path-reloading research resolver with FULL authority validation.

    Takes the canonical State FILE only (never a caller State dict, never a
    caller "verified" bundle). Performs a structural peek (duplicate-refusing
    parse, no schema/State validation), then validates the FULL adopted graph
    at the SAME selected checkpoint SHA: checkpoint schema/kind/operation/
    boundary/SELF, four artifacts with live re-hash, FULL evidence/views/
    ledger/completeness content validators, own-epoch recorded-commit proof,
    and report/proof/decision/retention actual reloads with cross-bindings
    (report/proof/decision/request/manifest/before vs checkpoint, retained
    COPY vs before_state). Finally re-reads the State file and the checkpoint
    FILE and refuses unless the triplet still references exactly the selected
    checkpoint path+sha (recheck pins before return — never a different
    selection observed after an earlier READY call). Returns {"family",
    "checkpoint", "artifacts", "artifact_refs", "lineage"} (data only;
    consumers reload bytes themselves). Zero writes; calls no
    agent.validate_agent_state, no verify_state_basis, no HIGH mutators, no
    operational guard. Detached diagnosis only — never a write permit.
    """
    repo_root = _norm_path(repo_root, "repo_root")
    state_path = _norm_path(state_path, "state path")
    abs_state = state_path if state_path.is_absolute() else (repo_root / str(state_path))
    raw = _safe_read_bytes(abs_state, "production state")
    state = _strict_parse_object(raw, "production state")
    structural = _resolve_research_from_state_bytes(repo_root, state)
    if structural["family"] == "LEGACY":
        return {
            "family": "LEGACY",
            "checkpoint": None,
            "artifacts": {},
            "artifact_refs": {},
            "lineage": {"checkpoint_path": None, "triplet": False},
        }
    selected_path = structural["checkpoint_path"]
    selected_sha = structural["checkpoint_sha256"]
    selected = _load_typed_four_refs(repo_root, structural)
    if selected["family"] != "PREARCH":
        # Legacy (or unknown-triplet non-PREARCH) keeps the exact historical
        # resolver shape: classification only, checkpoint None. FULL applies
        # to the adopted PREARCH graph below, never retrofitted onto legacy.
        return {
            "family": "LEGACY",
            "checkpoint": None,
            "artifacts": {},
            "artifact_refs": {},
            "lineage": {"checkpoint_path": None, "triplet": False},
        }
    require_same_triplet(state, structural)
    full = _verify_adopted_graph_full(repo_root, selected_path, selected_sha)
    record = full["record"]
    # Report/proof/decision/retention lineage: actual reload + cross-bind at
    # the SAME selected checkpoint SHA (not trusted dicts).
    report_ref = record.get("report") or {}
    _sized_ref_shape(report_ref, "checkpoint.report")
    report_raw = _verify_sized_ref_bytes(repo_root, report_ref, "checkpoint report")
    report = _strict_parse_object(report_raw, "checkpoint report")
    try:
        schema_gate.validate_instance(report, repo_root / str(DM022_REPORT_SCHEMA), label="adopted pre-adoption report")
    except Exception as exc:
        raise ResearchAuthorityError(f"adopted report schema invalid: {exc}") from exc
    for key in ("proof", "decision", "request"):
        if report.get(key, {}).get("sha256") != record.get(key, {}).get("sha256"):
            raise ResearchAuthorityError(f"adopted report/checkpoint {key} sha mismatch")
    if report.get("before_state", {}).get("sha256") != record.get("before_state", {}).get("sha256"):
        raise ResearchAuthorityError("adopted report/checkpoint before_state sha mismatch")
    if report.get("manifest", {}).get("sha256") != hashlib.sha256(
        _safe_read_bytes(_repo_rel(repo_root, full["manifest"].get("revision_root", "") + "/revision-manifest.json", "stored revision manifest"), "stored revision manifest")
    ).hexdigest():
        raise ResearchAuthorityError("adopted report manifest ref does not bind the stored manifest bytes")
    copy_target = f"{record.get('revision_root', '').rstrip('/')}/retention/state-before.json"
    copy_raw = _safe_read_bytes(_repo_rel(repo_root, copy_target, "retained state-before COPY"), "retained state-before COPY")
    if hashlib.sha256(copy_raw).hexdigest() != record.get("before_state", {}).get("sha256"):
        raise ResearchAuthorityError("adopted checkpoint before_state does not match retained COPY")
    # Final pin recheck: re-read State + checkpoint files; refuse unless the
    # triplet still references exactly the selected checkpoint (no drift
    # between selection and return, no other selection substituted).
    re_raw = _safe_read_bytes(abs_state, "production state recheck")
    re_state = _strict_parse_object(re_raw, "production state recheck")
    re_structural = _resolve_research_from_state_bytes(repo_root, re_state)
    require_same_triplet(re_state, re_structural)
    if re_structural.get("checkpoint_path") != selected_path or re_structural.get("checkpoint_sha256") != selected_sha:
        raise ResearchAuthorityError("State triplet moved during resolve (selection changed; refuse stale read)")
    cp_abs = _repo_rel(repo_root, selected_path, "research checkpoint recheck")
    if hashlib.sha256(_safe_read_bytes(cp_abs, "research checkpoint recheck")).hexdigest() != selected_sha:
        raise ResearchAuthorityError("research checkpoint FILE drift during resolve")
    lineage = {
        "checkpoint_path": selected_path,
        "checkpoint_sha256": selected_sha,
        "parent_checkpoint": record.get("parent_checkpoint"),
        "original_anchor": record.get("original_anchor"),
        "supersedes": record.get("supersedes", []),
        "triplet": True,
    }
    return {
        "family": "PREARCH",
        "checkpoint": record,
        "artifacts": full["artifacts"],
        "artifact_refs": full["artifact_refs"],
        "lineage": lineage,
    }


def load_revision_request(repo_root: Path, request_path: Path) -> dict[str, Any]:
    """Load+validate a DM022 revision request (immutable prepare input)."""
    repo_root = _norm_path(repo_root, "repo_root")
    request_path = _norm_path(request_path, "revision request path")
    target = request_path if request_path.is_absolute() else (repo_root / str(request_path))
    raw = _safe_read_bytes(target, "revision request")
    doc = _strict_parse_object(raw, "revision request")
    schema_abs = repo_root / str(DM022_REQUEST_SCHEMA)
    try:
        schema_gate.validate_instance(doc, schema_abs, label="revision request")
    except Exception as exc:
        raise ResearchAuthorityError(f"revision request schema invalid: {exc}") from exc
    _sized_ref_shape(doc["before_state"], "request.before_state")
    return doc


def _load_json_from_sized(repo_root: Path, ref: dict[str, Any], label: str) -> tuple[dict[str, Any], bytes]:
    repo_root = _norm_path(repo_root, "repo_root")
    _sized_ref_shape(ref, label)
    raw = _verify_sized_ref_bytes(repo_root, ref, label)
    return _strict_parse_object(raw, label), raw


# ---------------------------------------------------------------------------
# Profile/support P1-P4 workstream C: detached D/S root/effective context.
#
# Two PATH-only public loaders share one private state-free kernel. The loaders hold
# validated bytes authority (pinned COPY for LOW history, HIGH-eligible LIVE
# bytes for HIGH current); the kernel itself confers no permission. Context
# recovery is D/S-only and acyclic: the loader/kernel never call
# _verify_adopted_graph_full, check_supersession_record_from_paths,
# prove_revision_from_paths, completion verification, agent validation,
# production.verify_state_basis, or any PREARCH-only verifier. Adopted-full and
# completion call the loader (one direction only). ECP lineage (previous
# evidence/materiality/completeness) stays an outer file+SHA check owned by the
# existing callers, never re-entered here.
# ---------------------------------------------------------------------------


def _local_artifact_map(rows: Any, label: str) -> dict[str, dict[str, str]]:
    """Local NamedRef map (unique/non-empty names, exact {name,path,sha256}).

    Local to LOW so historical DCP/SCP/report validation never imports agent
    control (LOW header forbids agent imports at top level or inside bodies).
    Predicates mirror the actual agent validator byte-for-byte.
    """
    if not isinstance(rows, list):
        raise ResearchAuthorityError(f"{label} artifacts must be an array")
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        _named_ref_shape(row, f"{label} artifact")
        name = row["name"]
        if not name or name in result:
            raise ResearchAuthorityError(f"{label} artifact names must be unique/non-empty")
        result[name] = {"name": name, "path": row["path"], "sha256": row["sha256"]}
    return result


def _legacy_producer_check(repo_root: Path, record: dict[str, Any], checkpoint_name: str) -> None:
    """Bind record from/to to the on-disk config stage_plan producer pair.

    Reads config as data (stage_plan only, never authority): the from_state
    whose stage lists `checkpoint_name` in checkpoints and whose next_state
    equals record.to_state must equal record.from_state. DCP resolves to
    (ISSUE_INITIALIZED, DISCOVERY_COLLECTED); SCP to
    (DISCOVERY_COLLECTED, CANDIDATES_NORMALIZED). No agent import.
    """
    repo_root = _norm_path(repo_root, "repo_root")
    cfg_abs = repo_root / str(CONFIG_REL)
    cfg_raw = _safe_read_bytes(cfg_abs, "production config for producer lookup")
    cfg = _strict_parse_object(cfg_raw, "production config for producer lookup")
    try:
        plan = cfg["orchestration"]["stage_plan"]
    except (KeyError, TypeError) as exc:
        raise ResearchAuthorityError(f"production config lacks orchestration.stage_plan: {exc}") from exc
    if not isinstance(plan, dict):
        raise ResearchAuthorityError("production config stage_plan must be an object")
    from_state = record.get("from_state")
    to_state = record.get("to_state")
    matched = False
    for stage_from, stage in plan.items():
        if not isinstance(stage, dict):
            continue
        checkpoints = stage.get("checkpoints", [])
        if checkpoint_name in checkpoints and stage.get("next_state") == to_state and stage_from == from_state:
            matched = True
            break
    if not matched:
        raise ResearchAuthorityError(
            f"legacy {checkpoint_name} checkpoint producer mismatch: "
            f"from_state={from_state!r} to_state={to_state!r} binds no config stage_plan producer"
        )


def _rehash_deterministic_reviews(repo_root: Path, reviews: Any, label: str) -> dict[str, Any]:
    """Exactly-one CORE_STAGE_CONTRACT PASS + all deterministic refs rehashed.

    Requires exactly one matching CORE_STAGE_CONTRACT row (kind DETERMINISTIC,
    status PASS, 2-key {path,sha256} result with file rehash). Additional
    schema-valid review rows are allowed; every deterministic row's result ref
    ({path,sha256} plus optional byte_count) is file-rehashed. Never equates
    FILE SHA with any result-set digest.
    """
    repo_root = _norm_path(repo_root, "repo_root")
    if not isinstance(reviews, list) or not reviews:
        raise ResearchAuthorityError(f"{label} reviews must be a non-empty array")
    for row in reviews:
        if not isinstance(row, dict):
            raise ResearchAuthorityError(f"{label} review row must be an object")
        for key in ("check_id", "kind", "status"):
            if not isinstance(row.get(key), str) or not row[key]:
                raise ResearchAuthorityError(f"{label} review row lacks {key}")
    matches = [row for row in reviews if row.get("check_id") == _CORE_STAGE_REVIEW_ID]
    if len(matches) != 1:
        raise ResearchAuthorityError(
            f"{label} requires exactly one {_CORE_STAGE_REVIEW_ID} review (got {len(matches)})"
        )
    core_row = matches[0]
    if core_row.get("kind") != "DETERMINISTIC" or core_row.get("status") != "PASS":
        raise ResearchAuthorityError(f"{label} {_CORE_STAGE_REVIEW_ID} must be a deterministic PASS review")
    result_ref = core_row.get("result")
    if not isinstance(result_ref, dict) or set(result_ref) != {"path", "sha256"}:
        raise ResearchAuthorityError(f"{label} {_CORE_STAGE_REVIEW_ID} result must be ArtifactRef {{path,sha256}}")
    result_abs = _repo_rel(repo_root, result_ref["path"], f"{label} CORE result path")
    result_raw = _safe_read_bytes(result_abs, f"{label} CORE result")
    if hashlib.sha256(result_raw).hexdigest() != result_ref["sha256"]:
        raise ResearchAuthorityError(f"{label} {_CORE_STAGE_REVIEW_ID} result FILE sha drift")
    for row in reviews:
        if row.get("kind") != "DETERMINISTIC":
            continue
        ref = row.get("result")
        # Non-CORE deterministic rows keep the original predicate: path + sha
        # present with file rehash (extra keys tolerated, as the original only
        # reads path/sha). CORE itself stays exact 2-key above.
        if not isinstance(ref, dict) or not isinstance(ref.get("path"), str) or not ref["path"]:
            raise ResearchAuthorityError(f"{label} deterministic review result path invalid: {row.get('check_id')!r}")
        if not isinstance(ref.get("sha256"), str) or not _HEX64_RE.fullmatch(ref["sha256"]):
            raise ResearchAuthorityError(f"{label} deterministic review result sha invalid: {row.get('check_id')!r}")
        ref_abs = _repo_rel(repo_root, ref["path"], f"{label} deterministic result {row.get('check_id')}")
        ref_raw = _safe_read_bytes(ref_abs, f"{label} deterministic result {row.get('check_id')}")
        if hashlib.sha256(ref_raw).hexdigest() != ref["sha256"]:
            raise ResearchAuthorityError(
                f"{label} deterministic review result FILE sha drift: {row.get('check_id')}"
            )
        if "byte_count" in ref and len(ref_raw) != ref["byte_count"]:
            raise ResearchAuthorityError(
                f"{label} deterministic review result byte_count mismatch: {row.get('check_id')}"
            )
    return core_row


def _validate_legacy_stage_report(
    repo_root: Path,
    record: dict[str, Any],
    historical_issue_id: str,
    profile_ref_path: str,
    profile_sha256: str,
    canonical_state_path: str,
    label: str,
) -> dict[str, Any]:
    """Historical ordinary report: original 12 keys, record-owned equality.

    Mirrors the actual legacy predicates: exact 12-key shape,
    2.0-rc1/CORE_STAGE_CONTRACT/PASS identity, issue/from/to bound to the
    record (record-owned, never a current contract_identity fallback),
    production_profile == {path,sha256} of the bound profile file,
    production_state canonical logical path ONLY (no live SHA comparison),
    contract == record.contract, implementation == record implementation SHA,
    artifact map equality, recorded_at parse. Returns the parsed report.
    """
    repo_root = _norm_path(repo_root, "repo_root")
    reviews = record.get("reviews")
    if not isinstance(reviews, list):
        raise ResearchAuthorityError(f"{label} reviews must be an array")
    core_row = _rehash_deterministic_reviews(repo_root, reviews, label)
    result_ref = core_row["result"]
    report_abs = _repo_rel(repo_root, result_ref["path"], f"{label} CORE report")
    report_raw = _safe_read_bytes(report_abs, f"{label} CORE report")
    report = _strict_parse_object(report_raw, f"{label} CORE report")
    if set(report) != set(_HISTORICAL_REPORT_KEYS):
        raise ResearchAuthorityError(
            f"{label} CORE report must carry exactly the original 12 keys "
            f"(missing={sorted(set(_HISTORICAL_REPORT_KEYS) - set(report))} "
            f"extra={sorted(set(report) - set(_HISTORICAL_REPORT_KEYS))})"
        )
    if report.get("schema_version") != "2.0-rc1":
        raise ResearchAuthorityError(f"{label} CORE report schema_version must be 2.0-rc1")
    if report.get("check_id") != _CORE_STAGE_REVIEW_ID or report.get("status") != "PASS":
        raise ResearchAuthorityError(f"{label} CORE report check_id/status must be CORE_STAGE_CONTRACT/PASS")
    if report.get("issue_id") != historical_issue_id or report.get("issue_id") != record.get("issue_id"):
        raise ResearchAuthorityError(f"{label} CORE report issue_id must equal record and historical issue")
    if report.get("from_state") != record.get("from_state") or report.get("to_state") != record.get("to_state"):
        raise ResearchAuthorityError(f"{label} CORE report from/to must equal record from/to")
    expected_profile = {"path": profile_ref_path, "sha256": profile_sha256}
    if report.get("production_profile") != expected_profile:
        raise ResearchAuthorityError(f"{label} CORE report production_profile must equal the bound profile file ref")
    report_state = report.get("production_state")
    if not isinstance(report_state, dict) or set(report_state) != {"path", "sha256"}:
        raise ResearchAuthorityError(f"{label} CORE report production_state fields invalid")
    if report_state.get("path") != canonical_state_path:
        raise ResearchAuthorityError(
            f"{label} CORE report production_state must be the canonical historical State path only "
            f"(got {report_state.get('path')!r}, want {canonical_state_path!r}; no live SHA comparison)"
        )
    # Record-owned Contract8/implementation equality: never compute a current
    # contract_identity fallback while validating a historical checkpoint.
    expected_contract = record.get("contract")
    if not isinstance(expected_contract, dict):
        raise ResearchAuthorityError(f"{label} record contract missing (record-owned equality required)")
    if report.get("contract") != expected_contract:
        raise ResearchAuthorityError(f"{label} CORE report contract != record-owned contract")
    expected_impl = (record.get("implementation") or {}).get("repository_commit_sha")
    if not isinstance(expected_impl, str) or not _HEX40_RE.fullmatch(expected_impl):
        raise ResearchAuthorityError(f"{label} record implementation commit sha invalid")
    if report.get("implementation_commit_sha") != expected_impl:
        raise ResearchAuthorityError(f"{label} CORE report implementation != record-owned implementation")
    try:
        core.parse_instant(str(report.get("recorded_at", "")))
    except ValueError as exc:
        raise ResearchAuthorityError(f"{label} CORE report recorded_at invalid: {exc}") from exc
    record_artifacts = record.get("artifacts")
    if _local_artifact_map(report.get("artifacts"), f"{label} report") != _local_artifact_map(
        record_artifacts, f"{label} record"
    ):
        raise ResearchAuthorityError(f"{label} CORE report artifacts differ from record artifacts")
    return report


def _validate_legacy_dcp_scp(
    repo_root: Path,
    record: dict[str, Any],
    checkpoint_name: str,
    expected_artifact_name: str,
    historical_issue_id: str,
    profile_ref_path: str,
    profile_sha256: str,
    canonical_state_path: str,
) -> dict[str, str]:
    """Validate one ordinary LEGACY DCP/SCP record with its historical report.

    Family must be LEGACY (PREARCH here refuses DM022_WRONG_FAMILY; unknown
    kinds already refused by the typed loader). Then issue/producer/checkpoint
    membership/single-NamedRef artifact/reviews/report predicates. Returns the
    bound acceptance artifact {path, sha256}. No State validation, no Git
    blobs, no PREARCH seven-file proof, no completion/agent calls.
    """
    label = f"legacy {checkpoint_name} checkpoint"
    if record.get("issue_id") != historical_issue_id:
        raise ResearchAuthorityError(f"{label} issue_id must equal historical issue")
    _legacy_producer_check(repo_root, record, checkpoint_name)
    checkpoints = record.get("checkpoints")
    if not isinstance(checkpoints, list) or checkpoint_name not in checkpoints:
        raise ResearchAuthorityError(f"{label} must list {checkpoint_name} in checkpoints")
    # Original contract (stage-checkpoint schema artifacts minItems 1; agent
    # validator drift-checks every row without a total-count cap; CORE report
    # enforces full artifact-map equality): every row must be a valid NamedRef
    # with a unique non-empty name, and exactly one row must carry the expected
    # role name. Other valid named rows are allowed — never strengthened to
    # one-total. Every row's file is rehashed (original per-row drift).
    artifact_map = _local_artifact_map(record.get("artifacts"), label)
    matches = [name for name in artifact_map if name == expected_artifact_name]
    if len(matches) != 1:
        raise ResearchAuthorityError(
            f"{label} must carry exactly one {expected_artifact_name} artifact "
            f"(got {len(matches)}; other valid named rows allowed: {sorted(artifact_map)})"
        )
    for name, ref in artifact_map.items():
        abs_art = _repo_rel(repo_root, ref["path"], f"{label} artifact {name}")
        raw_art = _safe_read_bytes(abs_art, f"{label} artifact {name}")
        if hashlib.sha256(raw_art).hexdigest() != ref["sha256"]:
            raise ResearchAuthorityError(f"{label} artifact FILE sha drift: {name}")
    _validate_legacy_stage_report(
        repo_root, record, historical_issue_id, profile_ref_path,
        profile_sha256, canonical_state_path, label,
    )
    ref = artifact_map[expected_artifact_name]
    return {"path": ref["path"], "sha256": ref["sha256"]}


def _derive_root_effective_kernel(
    *,
    repo_root: Path,
    before_state: dict[str, Any],
    canonical_state_path: str,
    dcp_record: dict[str, Any],
    scp_record: dict[str, Any],
    request: dict[str, Any],
    profile_doc: dict[str, Any],
    root_records: list[dict[str, Any]],
    root_path: Path,
) -> dict[str, Any]:
    """Shared private kernel: state-free CONTENT validation + request binding.

    State-free path-reloading validation on caller-bound inputs (detached-map
    steps 7b-10): it reads files with no-follow/SHA checks and runs only the
    state-free Discovery validator and Screening _content siblings — never
    LIVE-bound Screening validators, agent validation, State loads, or
    PREARCH-only proof/completion. Both public loaders call this kernel (no
    logic fork). Acceptance never constitutes a caller-granted permission
    token — callers must already hold validated COPY (LOW) or HIGH-eligible
    LIVE authority. Returns the data-only context (consumers reload bytes
    themselves).
    """
    from scripts import survey_discovery_v2 as discovery_mod
    from scripts import survey_screening_v2 as screening_mod

    repo_root = _norm_path(repo_root, "repo_root")
    if not isinstance(before_state, dict):
        raise ResearchAuthorityError("kernel before_state must be an object")
    if not isinstance(canonical_state_path, str) or not canonical_state_path:
        raise ResearchAuthorityError("kernel canonical_state_path invalid")
    if not isinstance(request, dict):
        raise ResearchAuthorityError("kernel request must be an object")
    if not isinstance(profile_doc, dict):
        raise ResearchAuthorityError("kernel profile_doc must be an object")
    if not isinstance(root_records, list) or not root_records:
        raise ResearchAuthorityError("kernel root_records must be a non-empty list")
    root_path = _norm_path(root_path, "kernel root path")
    issue_id = before_state.get("issue_id")
    research_profile = before_state.get("research_profile")
    if not isinstance(issue_id, str) or not issue_id:
        raise ResearchAuthorityError("kernel before_state issue_id invalid")
    if request.get("issue_id") != issue_id:
        raise ResearchAuthorityError("kernel request issue_id must equal before-State issue")
    if profile_doc.get("issue_id") != issue_id or profile_doc.get("research_profile") != research_profile:
        raise ResearchAuthorityError("kernel profile issue/research must equal before-State")
    try:
        source_root_rel = profile_doc["paths"]["source_root"]
    except (KeyError, TypeError) as exc:
        raise ResearchAuthorityError(f"kernel profile source_root invalid: {exc}") from exc
    expectations = {
        "issue_id": issue_id,
        "research_profile": research_profile,
        "canonical_state_path": canonical_state_path,
    }
    # DCP acceptance: path from the validated record artifact, FILE rehash,
    # then the state-free ordinary Discovery validator (never PREARCH proof).
    dcp_artifacts = _local_artifact_map(dcp_record.get("artifacts"), "kernel DCP record")
    d_accept_rel = dcp_artifacts[_LEGACY_DCP_ARTIFACT]["path"]
    d_accept_abs = _repo_rel(repo_root, d_accept_rel, "kernel DCP discovery-acceptance")
    d_accept_raw = _safe_read_bytes(d_accept_abs, "kernel DCP discovery-acceptance")
    if hashlib.sha256(d_accept_raw).hexdigest() != dcp_artifacts[_LEGACY_DCP_ARTIFACT]["sha256"]:
        raise ResearchAuthorityError("kernel DCP discovery-acceptance FILE sha drift")
    try:
        discovery_acceptance = discovery_mod.validate_acceptance(repo_root, d_accept_abs)
    except Exception as exc:
        raise ResearchAuthorityError(f"kernel DCP discovery acceptance invalid: {exc}") from exc
    # Root JSONL consistency: the loader-passed root must be the acceptance's
    # Discovery set (resolve + SHA equality, never a second fetch).
    accepted_disc_rel = discovery_acceptance.get("discovery_path")
    accepted_disc_abs = _repo_rel(repo_root, accepted_disc_rel, "kernel accepted Discovery path")
    try:
        if accepted_disc_abs.resolve() != root_path.resolve():
            raise ResearchAuthorityError(
                "kernel root path does not match DCP acceptance Discovery path"
            )
    except OSError as exc:
        raise ResearchAuthorityError(f"kernel root path resolve failed: {exc}") from exc
    if hashlib.sha256(_safe_read_bytes(accepted_disc_abs, "kernel accepted Discovery")).hexdigest() != discovery_acceptance.get("discovery_sha256"):
        raise ResearchAuthorityError("kernel accepted Discovery FILE sha drift")
    # SCP acceptance: CONTENT sibling only (explicit expectations + true root).
    scp_artifacts = _local_artifact_map(scp_record.get("artifacts"), "kernel SCP record")
    s_accept_rel = scp_artifacts[_LEGACY_SCP_ARTIFACT]["path"]
    s_accept_abs = _repo_rel(repo_root, s_accept_rel, "kernel SCP screening-acceptance")
    s_accept_raw = _safe_read_bytes(s_accept_abs, "kernel SCP screening-acceptance")
    if hashlib.sha256(s_accept_raw).hexdigest() != scp_artifacts[_LEGACY_SCP_ARTIFACT]["sha256"]:
        raise ResearchAuthorityError("kernel SCP screening-acceptance FILE sha drift")
    try:
        screening_acceptance = screening_mod._validate_screening_acceptance_content(
            repo_root, s_accept_abs, expectations, root_records, root_path,
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"kernel SCP screening acceptance invalid: {exc}") from exc
    # FILE SHA (acceptance bytes) stays distinct from the recomputed
    # result-set digest (run-directory identity): never equated here.
    s_package_abs = s_accept_abs.parent / "package.json"
    s_package_raw = _safe_read_bytes(s_package_abs, "kernel SCP package")
    s_package = _strict_parse_object(s_package_raw, "kernel SCP package")
    try:
        effective = screening_mod._resolve_effective_discovery_basis_content(
            repo_root, s_package_abs, s_package, root_records, root_path,
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"kernel effective Discovery basis invalid: {exc}") from exc
    effective_records = effective.get("records")
    effective_path = effective.get("path")
    effective_mode = effective.get("mode")
    if not isinstance(effective_records, list) or not effective_records:
        raise ResearchAuthorityError("kernel effective records must be a non-empty list")
    if effective_mode not in ("DIRECT", "DERIVED_EXPANSION"):
        raise ResearchAuthorityError(f"kernel effective mode invalid: {effective_mode!r}")
    try:
        effective_sha256 = hashlib.sha256(_safe_read_bytes(effective_path, "kernel effective Discovery")).hexdigest()
    except ResearchAuthorityError as exc:
        raise ResearchAuthorityError(f"kernel effective Discovery unreadable: {exc}") from exc
    try:
        root_sha256 = hashlib.sha256(_safe_read_bytes(root_path, "kernel root Discovery")).hexdigest()
    except ResearchAuthorityError as exc:
        raise ResearchAuthorityError(f"kernel root Discovery unreadable: {exc}") from exc
    # Request binding: Discovery binds E (resolve + SHA + SizedRef bytes),
    # Screening binds the SCP artifact (path + SHA + file rehash).
    disc_ref = request.get("discovery_ref")
    _sized_ref_shape(disc_ref, "kernel request.discovery_ref")
    disc_req_abs = _repo_rel(repo_root, disc_ref["path"], "kernel request.discovery_ref.path")
    try:
        if disc_req_abs.resolve() != effective_path.resolve():
            raise ResearchAuthorityError(
                "kernel request.discovery_ref.path does not resolve to the effective Discovery path"
            )
    except OSError as exc:
        raise ResearchAuthorityError(f"kernel request discovery path resolve failed: {exc}") from exc
    _verify_sized_ref_bytes(repo_root, disc_ref, "kernel request.discovery_ref")
    if disc_ref["sha256"] != effective_sha256:
        raise ResearchAuthorityError("kernel request.discovery_ref.sha256 != effective Discovery FILE sha")
    scr_ref = request.get("screening_ref")
    _sized_ref_shape(scr_ref, "kernel request.screening_ref")
    if scr_ref["path"] != s_accept_rel or scr_ref["sha256"] != scp_artifacts[_LEGACY_SCP_ARTIFACT]["sha256"]:
        raise ResearchAuthorityError(
            "kernel request.screening_ref must equal the SCP screening-acceptance artifact (path + sha)"
        )
    _verify_sized_ref_bytes(repo_root, scr_ref, "kernel request.screening_ref")
    try:
        screening_map = {r["discovery_id"]: r for r in screening_acceptance.get("decisions", [])}
    except AttributeError as exc:
        raise ResearchAuthorityError(f"kernel screening decisions unreadable: {exc}") from exc
    return {
        "request": request,
        "before_state": before_state,
        "before_state_sha256": request.get("before_state", {}).get("sha256"),
        "canonical_state_path": canonical_state_path,
        "profile": profile_doc,
        "profile_path": _repo_rel(repo_root, request["profile_ref"]["path"], "kernel request.profile_ref.path"),
        "profile_sha256": request["profile_ref"]["sha256"],
        "dcp_record": dcp_record,
        "scp_record": scp_record,
        "dcp_path": d_accept_rel,
        "scp_path": s_accept_rel,
        "discovery_acceptance": discovery_acceptance,
        "screening_acceptance": screening_acceptance,
        "root_records": root_records,
        "root_path": root_path,
        "root_sha256": root_sha256,
        "effective_records": effective_records,
        "effective_path": effective_path,
        "effective_sha256": effective_sha256,
        "effective_mode": effective_mode,
        "screening_decisions": screening_map,
        "provenance": {
            "dcp_ref": dict(before_state.get("checkpoint_provenance", {}).get("discovery", {})),
            "scp_ref": dict(before_state.get("checkpoint_provenance", {}).get("screening", {})),
            "before_checkpoint": dict(request.get("before_checkpoint", {})),
            "copy_sha": request.get("before_state", {}).get("sha256"),
        },
    }


def _bind_profile_and_canonical(
    repo_root: Path, request: dict[str, Any]
) -> dict[str, Any]:
    """Bind request Profile SizedRef and derive the canonical logical State path.

    Loads the profile file through the request SizedRef (SHA + byte_count
    verified) and shape-validates it, then derives the canonical logical State
    path from the BOUND profile (parent directory of the profile file) and the
    on-disk config `state_authority.authoritative_filename` — the exact
    original predicate. Never the caller request's `before_state.path`
    assertion, never LIVE State bytes, never current Contract8. Returns
    {"profile_doc", "profile_raw", "profile_abs", "profile_sha256",
    "canonical_state_path", "canonical_abs"}.
    """
    repo_root = _norm_path(repo_root, "repo_root")
    profile_ref = request.get("profile_ref")
    profile_doc, profile_raw = _load_json_from_sized(repo_root, profile_ref, "request.profile_ref")
    try:
        schema_gate.validate_instance(profile_doc, repo_root / str(PROFILE_SCHEMA), label="request profile")
    except Exception as exc:
        raise ResearchAuthorityError(f"request profile shape invalid: {exc}") from exc
    profile_abs = _repo_rel(repo_root, profile_ref["path"], "request.profile_ref.path")
    cfg_abs = repo_root / str(CONFIG_REL)
    cfg_raw = _safe_read_bytes(cfg_abs, "production config for canonical State path")
    cfg = _strict_parse_object(cfg_raw, "production config for canonical State path")
    try:
        authoritative = cfg["state_authority"]["authoritative_filename"]
    except (KeyError, TypeError) as exc:
        raise ResearchAuthorityError(
            f"production config lacks state_authority.authoritative_filename: {exc}"
        ) from exc
    if not isinstance(authoritative, str) or not authoritative or "/" in authoritative or "\\" in authoritative or ".." in authoritative:
        raise ResearchAuthorityError("production config authoritative_filename invalid")
    canonical_abs = profile_abs.parent / authoritative
    try:
        canonical_rel = str(canonical_abs.resolve().relative_to(repo_root.resolve()))
    except ValueError as exc:
        raise ResearchAuthorityError(f"canonical State path escapes repository root: {exc}") from exc
    return {
        "profile_doc": profile_doc,
        "profile_raw": profile_raw,
        "profile_abs": profile_abs,
        "profile_sha256": hashlib.sha256(profile_raw).hexdigest(),
        "canonical_state_path": canonical_rel,
        "canonical_abs": canonical_abs,
    }


def _context_from_before_state(
    repo_root: Path, request: dict[str, Any], before_state: dict[str, Any]
) -> dict[str, Any]:
    """Shared tail for both public loaders (detached-map steps 3-10).

    Validates before_checkpoint == COPY/LIVE provenance (all three ArtifactRef
    triplets, ECP evidence included — never Discovery-derived), loads and
    LEGACY-validates DCP/SCP, binds the profile SizedRef, loads the root JSONL
    from the DCP acceptance chain, then calls the shared kernel. No new
    request field/schema presumed; genuinely absent R authority refuses with
    the exact gap (never an invented field or support reduction).
    """
    from scripts import survey_screening_v2 as screening_mod

    repo_root = _norm_path(repo_root, "repo_root")
    old_prov = before_state.get("checkpoint_provenance", {})
    if not isinstance(old_prov, dict):
        raise ResearchAuthorityError("before-State checkpoint_provenance missing")
    before_checkpoint = request.get("before_checkpoint")
    if not isinstance(before_checkpoint, dict):
        raise ResearchAuthorityError("request.before_checkpoint missing")
    for key in DM022_CHECKPOINTS:
        req_ref = before_checkpoint.get(key)
        _artifact_ref_shape(req_ref, f"request.before_checkpoint.{key}")
        st_ref = old_prov.get(key)
        _artifact_ref_shape(st_ref, f"before-State checkpoint_provenance.{key}")
        if req_ref != st_ref:
            raise ResearchAuthorityError(
                f"request.before_checkpoint.{key} must equal before-State provenance (exact ArtifactRef)"
            )
    dcp_ref = old_prov.get("discovery")
    scp_ref = old_prov.get("screening")
    for ref, kind in ((dcp_ref, "discovery"), (scp_ref, "screening")):
        _artifact_ref_shape(ref, f"before-State checkpoint_provenance.{kind}")
    issue_id = before_state.get("issue_id")
    if not isinstance(issue_id, str) or not issue_id:
        raise ResearchAuthorityError("before-State issue_id invalid")
    if request.get("issue_id") != issue_id:
        raise ResearchAuthorityError("request issue_id must equal before-State issue_id")

    def _load_cp(ref: dict[str, str], kind: str) -> dict[str, Any]:
        abs_cp = _repo_rel(repo_root, ref["path"], f"before-State {kind} checkpoint record")
        raw_cp = _safe_read_bytes(abs_cp, f"before-State {kind} checkpoint record")
        if hashlib.sha256(raw_cp).hexdigest() != ref["sha256"]:
            raise ResearchAuthorityError(f"before-State {kind} checkpoint record FILE sha drift")
        typed = load_typed_checkpoint_record(repo_root, abs_cp)
        if typed["family"] != "LEGACY":
            raise ResearchAuthorityError(
                f"DM022_WRONG_FAMILY: before-State {kind} checkpoint must be LEGACY family "
                f"(got {typed['family']}; PREARCH roles are evidence/materiality/completeness only)"
            )
        return typed["record"]

    dcp_record = _load_cp(dcp_ref, "discovery")
    scp_record = _load_cp(scp_ref, "screening")
    # Bound Profile + derived canonical logical State path (never the request
    # assertion). The profile file SHA feeds the LEGACY report checks.
    bound = _bind_profile_and_canonical(repo_root, request)
    profile_doc = bound["profile_doc"]
    profile_raw = bound["profile_raw"]
    profile_ref = request["profile_ref"]
    canonical_state_path = bound["canonical_state_path"]
    # Exact Profile identity vs before-State: path AND hash, not just
    # issue/research. The request Profile must be the before-State Profile.
    state_prof = before_state.get("profile")
    if not isinstance(state_prof, dict) or set(state_prof) != {"path", "sha256"}:
        raise ResearchAuthorityError("before-State profile authority fields invalid")
    if state_prof["path"] != profile_ref["path"] or state_prof["sha256"] != profile_ref["sha256"]:
        raise ResearchAuthorityError(
            "request Profile path/SHA must exactly match before_state.profile "
            "(path and hash, not just issue/research)"
        )
    if profile_doc.get("issue_id") != issue_id:
        raise ResearchAuthorityError("request profile issue_id must equal before-State issue_id")
    if profile_doc.get("research_profile") != before_state.get("research_profile"):
        raise ResearchAuthorityError("request profile research_profile must equal before-State research_profile")
    # The request assertion must equal the derived canonical path; a foreign
    # logical State path is never silently adopted.
    request_state_path = (request.get("before_state") or {}).get("path")
    if request_state_path != canonical_state_path:
        raise ResearchAuthorityError(
            f"request.before_state.path must be the derived canonical logical State path "
            f"(got {request_state_path!r}, want {canonical_state_path!r})"
        )
    profile_sha256 = bound["profile_sha256"]
    _validate_legacy_dcp_scp(
        repo_root, dcp_record, _LEGACY_DCP_NAME, _LEGACY_DCP_ARTIFACT,
        issue_id, profile_ref["path"], profile_sha256, canonical_state_path,
    )
    _validate_legacy_dcp_scp(
        repo_root, scp_record, _LEGACY_SCP_NAME, _LEGACY_SCP_ARTIFACT,
        issue_id, profile_ref["path"], profile_sha256, canonical_state_path,
    )
    # Root JSONL from the DCP acceptance chain (never a second fetch, never
    # the request Discovery file presumed as root: R comes from the accepted
    # Discovery chain, E is bound separately by the kernel).
    from scripts import survey_discovery_v2 as discovery_mod

    dcp_artifacts = _local_artifact_map(dcp_record.get("artifacts"), "context DCP record")
    d_accept_abs = _repo_rel(repo_root, dcp_artifacts[_LEGACY_DCP_ARTIFACT]["path"], "context DCP discovery-acceptance")
    try:
        discovery_acceptance = discovery_mod.validate_acceptance(repo_root, d_accept_abs)
    except Exception as exc:
        raise ResearchAuthorityError(f"context DCP discovery acceptance invalid: {exc}") from exc
    root_abs = _repo_rel(repo_root, discovery_acceptance["discovery_path"], "context accepted Discovery path")
    try:
        root_records = screening_mod.read_jsonl(root_abs)
    except Exception as exc:
        raise ResearchAuthorityError(f"context accepted Discovery JSONL unreadable: {exc}") from exc
    try:
        screening_mod.validate_discovery_set(root_records, issue_id)
    except Exception as exc:
        raise ResearchAuthorityError(f"context accepted Discovery set invalid: {exc}") from exc
    return _derive_root_effective_kernel(
        repo_root=repo_root,
        before_state=before_state,
        canonical_state_path=canonical_state_path,
        dcp_record=dcp_record,
        scp_record=scp_record,
        request=request,
        profile_doc=profile_doc,
        root_records=root_records,
        root_path=root_abs,
    )


def derive_ordinary_root_effective_context(
    repo_root: Path, request_path: Path, before_copy_path: Path
) -> dict[str, Any]:
    """Public LOW history loader (PATHS-only, pinned COPY, no LIVE State).

    Derives the true historical root/effective context from the pinned
    before-State COPY and its accepted Discovery/Screening refs. Request
    Discovery binds E; R comes from the separately bound accepted Discovery
    chain. No writes, no guard, no State mutation, no agent, no PREARCH proof,
    no completion, no future COPY. Genuinely absent R authority refuses with
    the exact gap (no invented field, no DIRECT fallback, no support cut).
    """
    repo_root = _norm_path(repo_root, "repo_root")
    request_path = _norm_path(request_path, "revision request path")
    before_copy_path = _norm_path(before_copy_path, "retained state-before COPY path")
    if request_path is None or before_copy_path is None:  # defensive: Path type already rejects None
        raise ResearchAuthorityError("derive_ordinary_root_effective_context requires request_path and before_copy_path (None refused; never infer a COPY)")
    request = load_revision_request(repo_root, request_path)
    before_ref = _sized_ref_shape(request.get("before_state"), "request.before_state")
    # Bind Profile + derived canonical path BEFORE any COPY read: the request
    # assertion must equal the Profile/config-derived canonical path, and LOW
    # history must never read LIVE State (the supplied COPY must not resolve
    # to the canonical LIVE path).
    pre_bound = _bind_profile_and_canonical(repo_root, request)
    if before_ref["path"] != pre_bound["canonical_state_path"]:
        raise ResearchAuthorityError(
            f"request.before_state.path must be the derived canonical logical State path "
            f"(got {before_ref['path']!r}, want {pre_bound['canonical_state_path']!r})"
        )
    copy_target = before_copy_path if before_copy_path.is_absolute() else (repo_root / str(before_copy_path))
    try:
        if copy_target.resolve() == pre_bound["canonical_abs"].resolve():
            raise ResearchAuthorityError(
                "LOW history loader refuses the canonical LIVE State path as before_copy_path "
                "(retained COPY only; LOW never reads LIVE State)"
            )
    except OSError as exc:
        raise ResearchAuthorityError(f"before COPY path resolve failed: {exc}") from exc
    copy_raw = _safe_read_bytes(copy_target, "retained state-before COPY")
    if hashlib.sha256(copy_raw).hexdigest() != before_ref["sha256"]:
        raise ResearchAuthorityError("retained COPY bytes != request.before_state.sha256")
    if len(copy_raw) != before_ref["byte_count"]:
        raise ResearchAuthorityError("retained COPY byte_count mismatch")
    before_state = _strict_parse_object(copy_raw, "retained state-before COPY")
    try:
        schema_gate.validate_instance(before_state, repo_root / str(STATE_SCHEMA), label="retained state-before COPY")
    except Exception as exc:
        raise ResearchAuthorityError(f"retained state-before COPY State shape invalid: {exc}") from exc
    return _context_from_before_state(repo_root, request, before_state)


def derive_current_root_effective_context(
    repo_root: Path, request_path: Path, live_state_path: Path
) -> dict[str, Any]:
    """Public HIGH-only current loader (after eligibility, before first COPY).

    Reads the LIVE State file (= request.before_state.path, hash/bytes
    checked) as DATA and loads the COPY-equivalent provenance from that LIVE
    dict plus DCP/SCP files, then calls the shared private kernel. LOW history
    never uses this entry; LOW uses the pinned-COPY loader only. Shared kernel
    accepts data; permission comes from HIGH eligibility vs LOW COPY pin.
    """
    repo_root = _norm_path(repo_root, "repo_root")
    request_path = _norm_path(request_path, "revision request path")
    live_state_path = _norm_path(live_state_path, "LIVE State path")
    request = load_revision_request(repo_root, request_path)
    before_ref = _sized_ref_shape(request.get("before_state"), "request.before_state")
    # The supplied LIVE path must equal the canonical request path: bind
    # Profile + derived canonical first, then require resolve-equality with
    # the request assertion (a foreign LIVE file is never loaded as DATA).
    live_bound = _bind_profile_and_canonical(repo_root, request)
    if before_ref["path"] != live_bound["canonical_state_path"]:
        raise ResearchAuthorityError(
            f"request.before_state.path must be the derived canonical logical State path "
            f"(got {before_ref['path']!r}, want {live_bound['canonical_state_path']!r})"
        )
    live_target = live_state_path if live_state_path.is_absolute() else (repo_root / str(live_state_path))
    try:
        if live_target.resolve() != live_bound["canonical_abs"].resolve():
            raise ResearchAuthorityError(
                "HIGH current loader supplied LIVE path must equal the canonical request path "
                f"(got {str(live_state_path)!r}, want {live_bound['canonical_state_path']!r})"
            )
    except OSError as exc:
        raise ResearchAuthorityError(f"LIVE path resolve failed: {exc}") from exc
    live_raw = _safe_read_bytes(live_target, "LIVE State bytes for current context")
    if hashlib.sha256(live_raw).hexdigest() != before_ref["sha256"]:
        raise ResearchAuthorityError("LIVE State bytes != request.before_state.sha256 (current context binds the request)")
    if len(live_raw) != before_ref["byte_count"]:
        raise ResearchAuthorityError("LIVE State byte_count mismatch (current context binds the request)")
    live_state = _strict_parse_object(live_raw, "LIVE State bytes for current context")
    try:
        schema_gate.validate_instance(live_state, repo_root / str(STATE_SCHEMA), label="LIVE State for current context")
    except Exception as exc:
        raise ResearchAuthorityError(f"LIVE State shape invalid: {exc}") from exc
    return _context_from_before_state(repo_root, request, live_state)


def derive_before_context(
    repo_root: Path,
    request_path: Path,
    before_copy_path: Path,
    previous_checkpoint_path: Path,
) -> dict[str, Any]:
    """Derive immutable before-context from retained COPY (detached).

    Loads request + retained State COPY + previous checkpoint + 4 old accepted
    artifacts; verifies COPY bytes == request.before_state.sha256. Uses COPY
    via retention mapping; never rebinds basis to the COPY path. Also validates
    request records via the detached pure record validator and completeness
    obligations via real shape checks (no invented defaults). Pure
    path-reloading; zero writes.
    """
    from scripts import survey_evidence_v2 as evidence_mod

    repo_root = _norm_path(repo_root, "repo_root")
    request_path = _norm_path(request_path, "revision request path")
    before_copy_path = _norm_path(before_copy_path, "retained state-before COPY path")
    previous_checkpoint_path = _norm_path(previous_checkpoint_path, "previous checkpoint path")
    request_path = _norm_path(request_path, "revision request path")
    before_copy_path = _norm_path(before_copy_path, "retained state-before COPY path")
    previous_checkpoint_path = _norm_path(previous_checkpoint_path, "previous checkpoint path")
    request = load_revision_request(repo_root, request_path)
    before_ref = _sized_ref_shape(request["before_state"], "request.before_state")
    copy_target = before_copy_path if Path(before_copy_path).is_absolute() else (repo_root / str(before_copy_path))
    copy_raw = _safe_read_bytes(copy_target, "retained state-before COPY")
    if hashlib.sha256(copy_raw).hexdigest() != before_ref["sha256"]:
        raise ResearchAuthorityError("retained COPY bytes != request.before_state.sha256")
    if len(copy_raw) != before_ref["byte_count"]:
        raise ResearchAuthorityError("retained COPY byte_count mismatch")
    before_state = _strict_parse_object(copy_raw, "retained state-before COPY")
    prev_target = previous_checkpoint_path if Path(previous_checkpoint_path).is_absolute() else (repo_root / str(previous_checkpoint_path))
    prev_typed = load_typed_checkpoint_record(repo_root, prev_target)
    # before_checkpoint (3 refs) must equal the COPY State's provenance triplet.
    old_prov = before_state.get("checkpoint_provenance", {})
    for key in DM022_CHECKPOINTS:
        req_ref = (request.get("before_checkpoint") or {}).get(key)
        _artifact_ref_shape(req_ref, f"request.before_checkpoint.{key}")
        st_ref = old_prov.get(key)
        _artifact_ref_shape(st_ref, f"COPY checkpoint_provenance.{key}")
        if req_ref != st_ref:
            raise ResearchAuthorityError(f"request.before_checkpoint.{key} must equal COPY State provenance")
    # Supplied previous path must equal the ECP from request
    # before_checkpoint.evidence AND COPY checkpoint_provenance.evidence, with
    # its file SHA checked. It is never derived from Discovery provenance and
    # never defaults to a Discovery-side path. For split legacy triplets the
    # ECP is the evidence ref (the record carrying the 4 research artifacts);
    # for same-record triplets the single predecessor file is that same ECP.
    req_ecp = (request.get("before_checkpoint") or {}).get("evidence")
    _artifact_ref_shape(req_ecp, "request.before_checkpoint.evidence")
    copy_ecp = old_prov.get("evidence")
    _artifact_ref_shape(copy_ecp, "COPY checkpoint_provenance.evidence")
    if req_ecp != copy_ecp:
        raise ResearchAuthorityError(
            "request.before_checkpoint.evidence must equal COPY checkpoint_provenance.evidence (ECP binding, never DCP-derived)"
        )
    try:
        prev_resolved = prev_target.resolve()
        ecp_abs = _repo_rel(repo_root, req_ecp["path"], "request.before_checkpoint.evidence.path")
        ecp_resolved = ecp_abs.resolve()
    except OSError as exc:
        raise ResearchAuthorityError(f"previous checkpoint path resolve failed: {exc}") from exc
    if prev_resolved != ecp_resolved:
        raise ResearchAuthorityError(
            f"previous_checkpoint_path must be the ECP file {req_ecp['path']!r} "
            f"(got {str(previous_checkpoint_path)!r}; never a Discovery-side path)"
        )
    prev_raw_check = _safe_read_bytes(prev_target, "previous checkpoint record")
    if hashlib.sha256(prev_raw_check).hexdigest() != req_ecp["sha256"]:
        raise ResearchAuthorityError("previous checkpoint record FILE sha drift vs ECP ref")
    # Load profile/discovery/screening refs with live re-hash (real files).
    profile_doc, _ = _load_json_from_sized(repo_root, request["profile_ref"], "request.profile_ref")
    screening_abs = _repo_rel(repo_root, request["screening_ref"]["path"], "request.screening_ref.path")
    screening_raw = _safe_read_bytes(screening_abs, "screening acceptance")
    if hashlib.sha256(screening_raw).hexdigest() != request["screening_ref"]["sha256"]:
        raise ResearchAuthorityError("screening acceptance FILE sha drift (before-context)")
    discovery_abs = _repo_rel(repo_root, request["discovery_ref"]["path"], "request.discovery_ref.path")
    discovery_raw = _safe_read_bytes(discovery_abs, "discovery set")
    if hashlib.sha256(discovery_raw).hexdigest() != request["discovery_ref"]["sha256"]:
        raise ResearchAuthorityError("discovery FILE sha drift (before-context)")
    # Validate request records via the detached pure record validator (no promotion).
    for idx, rec in enumerate(request.get("records", [])):
        try:
            evidence_mod.validate_research_record_content(rec, profile_doc)
        except Exception as exc:
            raise ResearchAuthorityError(f"request.records[{idx}] invalid: {exc}") from exc
    # Affected allowlist: nonempty unique subset of non-DROP Discovery IDs.
    # Discovery IDs come from the real Discovery set (JSONL), not invented.
    from scripts import survey_screening_v2 as screening_mod

    try:
        discoveries = screening_mod.read_jsonl(discovery_abs)
    except Exception as exc:
        raise ResearchAuthorityError(f"discovery JSONL read failed: {exc}") from exc
    if not isinstance(discoveries, list) or not discoveries:
        raise ResearchAuthorityError("discovery set must be a nonempty list")
    discovery_ids = [d.get("discovery_id") for d in discoveries if isinstance(d, dict)]
    if len(discovery_ids) != len(set(discovery_ids)):
        raise ResearchAuthorityError("discovery set has duplicate IDs")
    try:
        screening_doc = _strict_parse_object(screening_raw, "screening acceptance")
    except ResearchAuthorityError:
        raise
    decisions = {r.get("discovery_id"): r.get("decision") for r in screening_doc.get("decisions", []) if isinstance(r, dict)}
    non_drop = {did for did, dec in decisions.items() if dec in ("KEEP", "MAYBE", "INSPECT")}
    affected = request.get("affected_ids", [])
    if not affected or len(set(affected)) != len(affected):
        raise ResearchAuthorityError("request.affected_ids must be nonempty unique")
    if not set(affected).issubset(non_drop):
        raise ResearchAuthorityError("request.affected_ids must be a subset of non-DROP Discovery IDs")
    if not set(affected).issubset(set(discovery_ids)):
        raise ResearchAuthorityError("request.affected_ids must be known Discovery IDs")
    # Records must cover exact non-DROP Discovery IDs (same-State, no new IDs).
    record_ids = [r.get("discovery_id") for r in request.get("records", [])]
    if set(record_ids) != non_drop:
        raise ResearchAuthorityError("request.records must cover exact non-DROP Discovery IDs (no new/omitted IDs allowed in same-State correction)")
    # Old accepted graph from previous checkpoint record (4 artifacts).
    prev_record = prev_typed["record"]
    if prev_typed["family"] == "PREARCH":
        old_names = sorted(a.get("name") for a in prev_record.get("artifacts", []))
        if old_names != sorted(DM022_ARTIFACT_NAMES):
            raise ResearchAuthorityError("previous PREARCH record must carry exactly the 4 research refs")
    else:
        art_names = sorted(a.get("name") for a in prev_record.get("artifacts", []) if isinstance(a, dict))
        for need in ("evidence-acceptance", "edition-views-acceptance", "materiality-ledger", "profile-completeness"):
            if need not in art_names:
                raise ResearchAuthorityError(f"previous legacy record lacks required artifact: {need}")
    old_prov_map = {k: old_prov.get(k) for k in DM022_CHECKPOINTS}
    # True historical R/E threads through this entry as well: derive the
    # D/S-bound context from the same request + retained COPY (never E-as-R,
    # never LIVE State) and carry it alongside the legacy keys for callers.
    # The new D/S loader does not replace the ECP content/lineage validation
    # above; both bind the same before-State authority.
    ds_context = derive_ordinary_root_effective_context(repo_root, request_path, before_copy_path)
    return {
        "request": request,
        "before_state": before_state,
        "before_state_sha256": before_ref["sha256"],
        "previous_checkpoint": prev_typed,
        "old_checkpoint_refs": old_prov_map,
        "research_profile": request.get("research_profile"),
        "issue_id": request.get("issue_id"),
        "revision_id": request.get("revision_id"),
        "profile": profile_doc,
        "discoveries": discoveries,
        "screening_acceptance": screening_doc,
        "root_records": ds_context["root_records"],
        "root_path": ds_context["root_path"],
        "root_sha256": ds_context["root_sha256"],
        "effective_records": ds_context["effective_records"],
        "effective_path": ds_context["effective_path"],
        "effective_sha256": ds_context["effective_sha256"],
        "effective_mode": ds_context["effective_mode"],
        "canonical_state_path": ds_context["canonical_state_path"],
    }


def _planned_ref(repo_root: Path, rel: str, payload: dict[str, Any]) -> dict[str, Any]:
    raw = core.json_bytes(payload)
    return {
        "path": rel,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "byte_count": len(raw),
        "payload": payload,
    }


def build_revision_package_from_paths(
    repo_root: Path, request_path: Path, before_copy_path: Path, output_dir: Path
) -> dict[str, Any]:
    """Pure package derivation bound to S_before + existing Discovery/Screening.

    Uses REAL Discovery/Screening data (not invented tasks): for each non-DROP
    Discovery, derives a task with stable_task_id, source_records from the real
    Discovery source, verification_targets from the real Screening decision,
    and screening_basis binding the real screening acceptance SHA. Validates
    request records via the detached pure record validator. Returns
    {"package", "tasks", "planned_files"}; writes nothing.
    """
    from scripts import survey_evidence_v2 as evidence_mod
    from scripts import survey_screening_v2 as screening_mod

    repo_root = _norm_path(repo_root, "repo_root")
    request_path = _norm_path(request_path, "revision request path")
    before_copy_path = _norm_path(before_copy_path, "retained state-before COPY path")
    output_dir = _norm_path(output_dir, "output dir")
    request_path = _norm_path(request_path, "revision request path")
    before_copy_path = _norm_path(before_copy_path, "retained state-before COPY path")
    output_dir = _norm_path(output_dir, "output dir")
    request = load_revision_request(repo_root, request_path)
    before_ref = _sized_ref_shape(request["before_state"], "request.before_state")
    copy_target = before_copy_path if Path(before_copy_path).is_absolute() else (repo_root / str(before_copy_path))
    copy_raw = _safe_read_bytes(copy_target, "retained state-before COPY")
    if hashlib.sha256(copy_raw).hexdigest() != before_ref["sha256"]:
        raise ResearchAuthorityError("package derivation COPY drift")
    # Previous record path comes from the request's before_checkpoint evidence
    # ref (the predecessor checkpoint file). Load it to reuse real
    # prompt/contracts (no invented placeholder SHAs).
    prev_ref = (request.get("before_checkpoint") or {}).get("evidence")
    _artifact_ref_shape(prev_ref, "request.before_checkpoint.evidence")
    prev_abs = _repo_rel(repo_root, prev_ref["path"], "previous checkpoint record")
    prev_raw = _safe_read_bytes(prev_abs, "previous checkpoint record")
    if hashlib.sha256(prev_raw).hexdigest() != prev_ref["sha256"]:
        raise ResearchAuthorityError("previous checkpoint record FILE sha drift (package stage)")
    prev_typed_pkg = load_typed_checkpoint_record(repo_root, prev_abs)
    prev_record_pkg = prev_typed_pkg["record"]
    old_art_by_name_pkg = {r.get("name"): r for r in prev_record_pkg.get("artifacts", []) if isinstance(r, dict)}
    old_ev_ref_pkg = old_art_by_name_pkg.get("evidence-acceptance")
    if old_ev_ref_pkg is None:
        raise ResearchAuthorityError("previous record lacks evidence-acceptance artifact")
    old_ev_abs_pkg = _repo_rel(repo_root, old_ev_ref_pkg["path"], "OLD evidence acceptance")
    old_pkg_path_pkg = old_ev_abs_pkg.parent / "package.json"
    try:
        old_pkg_raw_pkg = _safe_read_bytes(old_pkg_path_pkg, "OLD evidence package")
    except ResearchAuthorityError as exc:
        raise ResearchAuthorityError(f"OLD evidence package missing (run_dir layout required): {exc}") from exc
    old_pkg_pkg = _strict_parse_object(old_pkg_raw_pkg, "OLD evidence package")
    profile_doc, _ = _load_json_from_sized(repo_root, request["profile_ref"], "request.profile_ref")
    # True historical R/E from the pinned COPY + accepted D/S chain (never
    # E-as-R, never LIVE State). Tasks derive from the validated effective
    # set; the loader already bound request.discovery_ref == E and
    # request.screening_ref == the SCP artifact.
    ds_context = derive_ordinary_root_effective_context(repo_root, request_path, before_copy_path)
    discoveries = ds_context["effective_records"]
    screening_doc = ds_context["screening_acceptance"]
    screening_abs = _repo_rel(repo_root, request["screening_ref"]["path"], "request.screening_ref.path")
    screening_raw = _safe_read_bytes(screening_abs, "screening acceptance")
    # Real screening digest recompute (no constants).
    try:
        screening_digest = evidence_mod._screening_acceptance_digest(screening_doc)
    except Exception as exc:
        raise ResearchAuthorityError(f"screening digest recompute failed: {exc}") from exc
    if screening_doc.get("result_set_sha256") != screening_digest:
        raise ResearchAuthorityError("screening acceptance result_set digest mismatch")
    discovery_map = {d["discovery_id"]: d for d in discoveries if isinstance(d, dict)}
    decisions = {r["discovery_id"]: r for r in screening_doc.get("decisions", []) if isinstance(r, dict)}
    for idx, rec in enumerate(request.get("records", [])):
        try:
            evidence_mod.validate_research_record_content(rec, profile_doc)
        except Exception as exc:
            raise ResearchAuthorityError(f"request.records[{idx}] invalid: {exc}") from exc
    out_rel = str(output_dir).rstrip("/")
    tasks: list[dict[str, Any]] = []
    for discovery_id in sorted(discovery_map):
        decision = decisions.get(discovery_id)
        if decision is None:
            raise ResearchAuthorityError(f"Discovery lacks Screening disposition: {discovery_id}")
        if decision.get("decision") == "DROP":
            continue
        task_id = evidence_mod.stable_task_id(request["issue_id"], discovery_id)
        task = {
            "schema_version": DM022_SCHEMA_VERSION,
            "issue_id": request["issue_id"],
            "evidence_task_id": task_id,
            "discovery_ids": [discovery_id],
            "source_records": [discovery_map[discovery_id]["source"]],
            "verification_targets": list(decision.get("verification_targets", [])),
            "screening_basis": {
                "screening_acceptance_sha256": hashlib.sha256(screening_raw).hexdigest(),
                "decisions": [{
                    "discovery_id": discovery_id,
                    "decision": decision.get("decision"),
                    "scope_tags": list(decision.get("scope_tags", [])),
                }],
            },
        }
        task_filename = evidence_mod.task_filename(task_id)
        tasks.append({"task": task, "filename": task_filename})
    if not tasks:
        raise ResearchAuthorityError("no non-DROP Discovery tasks (empty package refused)")
    # Validate each task shape via real task validator (needs meta sha; compute
    # task file sha from canonical task bytes first).
    task_metas: list[dict[str, Any]] = []
    for entry in tasks:
        task = entry["task"]
        task_raw = core.json_bytes(task)
        task_sha = hashlib.sha256(task_raw).hexdigest()
        meta = {"evidence_task_id": task["evidence_task_id"], "path": f"tasks/{entry['filename']}", "sha256": task_sha, "discovery_ids": task["discovery_ids"]}
        errs = evidence_mod._validate_task(task, meta, hashlib.sha256(screening_raw).hexdigest())
        if errs:
            raise ResearchAuthorityError(f"derived task invalid: {errs[0]}")
        task_metas.append({**meta, "_task": task, "_raw": task_raw})
    package = {
        "schema_version": DM022_SCHEMA_VERSION,
        "issue_id": request["issue_id"],
        "research_profile": request["research_profile"],
        "basis": {
            "state_path": before_ref["path"],
            "state_sha256": before_ref["sha256"],
            "profile_path": request["profile_ref"]["path"],
            "profile_sha256": request["profile_ref"]["sha256"],
            "discovery_path": request["discovery_ref"]["path"],
            "discovery_sha256": request["discovery_ref"]["sha256"],
            "screening_acceptance_path": request["screening_ref"]["path"],
            "screening_acceptance_sha256": hashlib.sha256(screening_raw).hexdigest(),
        },
        "prompt": old_pkg_pkg.get("prompt"),
        "contracts": old_pkg_pkg.get("contracts"),
        "tasks": [{k: m[k] for k in ("evidence_task_id", "path", "sha256", "discovery_ids")} for m in task_metas],
        "expected_outputs": {"one_result_per_task": True, "filename_rule": "same-basename-as-task"},
        "rules": [
            "DM022 same-State revision: tasks derive from real Discovery/Screening; no CANDIDATES_NORMALIZED pretense.",
            "Every event/claim/metric/limitation binds an explicit subject entity and subject role.",
        ],
    }
    # Real package field/content checks (no State).
    try:
        evidence_mod._check_evidence_package_fields_content(package)
    except Exception as exc:
        raise ResearchAuthorityError(f"derived package fields invalid: {exc}") from exc
    planned = [_planned_ref(repo_root, f"{out_rel}/candidate/package.json", package)]
    for meta in task_metas:
        planned.append(_planned_ref(repo_root, f"{out_rel}/candidate/tasks/{meta['path'].split('/')[-1]}", meta["_task"]))
    return {"package": package, "tasks": task_metas, "planned_files": planned}


def build_revision_cards_views_from_paths(
    repo_root: Path, package_path: Path, request_path: Path, results_dir: Path, views_dir: Path,
    *, before_copy_path: Path,
) -> dict[str, Any]:
    """Pure card/view derivation from package + request records (no writes).

    Uses the detached pure card/view builders with actual task authority
    (source_records, verification_targets, screening_basis) and validates
    every card/view via real validate_evidence_card/validate_edition_view.
    Computes REAL digests via _evidence_result_set_digest/_view_set_digest.
    No fabricated SHAs. before_copy_path is REQUIRED keyword-only (None
    refused; never guessed from LIVE State or a basename): the true
    historical R/E is derived from the same request + retained COPY, and
    request records are bound to effective DIDs.
    """
    from scripts import survey_evidence_v2 as evidence_mod

    repo_root = _norm_path(repo_root, "repo_root")
    package_path = _norm_path(package_path, "revision package path")
    request_path = _norm_path(request_path, "revision request path")
    results_dir = _norm_path(results_dir, "results dir")
    views_dir = _norm_path(views_dir, "views dir")
    if before_copy_path is None:
        raise ResearchAuthorityError(
            "build_revision_cards_views_from_paths requires before_copy_path "
            "(None refused; never infer a COPY from LIVE State or a basename)"
        )
    before_copy_path = _norm_path(before_copy_path, "retained state-before COPY path")
    request = load_revision_request(repo_root, request_path)
    # True historical R/E (chain + request-ref binding validated here).
    ds_context = derive_ordinary_root_effective_context(repo_root, request_path, before_copy_path)
    effective_ids = {d.get("discovery_id") for d in ds_context["effective_records"] if isinstance(d, dict)}
    for idx, rec in enumerate(request.get("records", [])):
        if not isinstance(rec, dict) or rec.get("discovery_id") not in effective_ids:
            raise ResearchAuthorityError(
                f"request.records[{idx}] discovery_id is not a bound effective Discovery ID "
                f"(records bind E DIDs, never invented IDs)"
            )
    pkg_target = package_path if Path(package_path).is_absolute() else (repo_root / str(package_path))
    pkg_raw = _safe_read_bytes(pkg_target, "revision package")
    package = _strict_parse_object(pkg_raw, "revision package")
    try:
        evidence_mod._check_evidence_package_fields_content(package)
    except Exception as exc:
        raise ResearchAuthorityError(f"package fields invalid (cards stage): {exc}") from exc
    # LOW bulk phase: bind package basis to true historical root (COPY-only,
    # no LIVE), then one phase context (package-linear), pure per-task slices.
    _low_expect = {
        "issue_id": request.get("issue_id"),
        "research_profile": request.get("research_profile"),
        "canonical_state_path": ds_context["canonical_state_path"],
    }
    try:
        evidence_mod._validate_evidence_package_basis_content(
            repo_root, pkg_target, package, _low_expect,
            ds_context["root_records"], ds_context["root_path"],
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"revision package basis invalid against true root: {exc}") from exc
    try:
        _low_ctx = evidence_mod._resolve_phase_supplement_context(
            repo_root, package, implementation_sha=None,
            screening_acceptance=None, discoveries=None,
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"revision supplement context invalid: {exc}") from exc
    profile_doc, _ = _load_json_from_sized(repo_root, request["profile_ref"], "request.profile_ref")
    by_discovery = {r["discovery_id"]: r for r in request.get("records", [])}
    # LOW phase pins: COPY/profile/request/package/tasks (no LIVE).
    _low_pin_list: list[tuple[str, Path]] = [
        ("LOW request", request_path if Path(request_path).is_absolute() else (repo_root / str(request_path))),
        ("LOW retained COPY", before_copy_path if Path(before_copy_path).is_absolute() else (repo_root / str(before_copy_path))),
        ("LOW revision package", pkg_target),
    ]
    try:
        _prof_rel = request["profile_ref"]["path"]
        _low_pin_list.append(("LOW profile", _repo_rel(repo_root, _prof_rel, "request.profile_ref")))
    except Exception:
        pass
    for _m in package.get("tasks", []):
        for _cand in (pkg_target.parent / _m.get("path", ""), pkg_target.parent / "tasks" / Path(_m.get("path", "")).name):
            try:
                if _cand.is_file() and not _cand.is_symlink():
                    _low_pin_list.append((f"LOW revision task {_m.get('evidence_task_id')}", _cand))
                    break
            except OSError:
                continue
    _low_pins = evidence_mod._capture_phase_pins(tuple(_low_pin_list))
    cards: list[dict[str, Any]] = []
    for meta in package.get("tasks", []):
        dids = meta.get("discovery_ids", [])
        if len(dids) != 1:
            raise ResearchAuthorityError("DM022 task must bind exactly one Discovery ID")
        rec = by_discovery.get(dids[0])
        if rec is None:
            raise ResearchAuthorityError(f"task {meta.get('evidence_task_id')} has no request record")
        # Load full task dict: prefer in-package tasks (HIGH writes tasks
        # alongside package); fall back to package-adjacent tasks dir.
        task: dict[str, Any] | None = None
        for cand in (pkg_target.parent / meta.get("path", ""), pkg_target.parent / "tasks" / Path(meta.get("path", "")).name):
            try:
                cand_raw = _safe_read_bytes(cand, "package task")
                task = _strict_parse_object(cand_raw, "package task")
                break
            except ResearchAuthorityError:
                continue
        if task is None:
            raise ResearchAuthorityError(f"package task file missing for {meta.get('evidence_task_id')}")
        try:
            _low_base = evidence_mod._discovery_task_sources(task)
            _low_auth = evidence_mod._merge_supplement_task_sources(_low_base, task, _low_ctx["entries"])
            card = evidence_mod._build_card_core(task, meta, package, rec, request.get("runner", {}), _low_auth)
        except Exception as exc:
            raise ResearchAuthorityError(f"card build failed for {meta.get('evidence_task_id')}: {exc}") from exc

        def _low_validate(_task: dict[str, Any] = task) -> dict[str, dict[str, Any]]:
            _b = evidence_mod._discovery_task_sources(_task)
            return evidence_mod._merge_supplement_task_sources(_b, _task, _low_ctx["entries"])

        errs = evidence_mod._validate_card_core(card, task, meta["sha256"], package, _low_validate)
        if errs:
            raise ResearchAuthorityError(f"built card invalid for {meta.get('evidence_task_id')}: {errs[0]}")
        cards.append(card)
    views: list[dict[str, Any]] = []
    for card in cards:
        task_id = card["evidence_task_id"]
        rec = next((r for r in request.get("records", []) if r.get("status") == card.get("status") and r.get("discovery_id") in [d for t in package.get("tasks", []) if t.get("evidence_task_id") == task_id for d in t.get("discovery_ids", [])]), None)
        # Find record by discovery binding (exact).
        rec = None
        for meta in package.get("tasks", []):
            if meta.get("evidence_task_id") == task_id:
                rec = by_discovery.get(meta["discovery_ids"][0])
                break
        if rec is None:
            raise ResearchAuthorityError(f"view record missing for {task_id}")
        card_raw = core.json_bytes(card)
        card_sha = hashlib.sha256(card_raw).hexdigest()
        try:
            view = evidence_mod.build_research_view_content(profile_doc, task_id, card_sha, rec)
        except Exception as exc:
            raise ResearchAuthorityError(f"view build failed for {task_id}: {exc}") from exc
        errs = evidence_mod.validate_edition_view(view, profile_doc, card_sha, card.get("status"))
        if errs:
            raise ResearchAuthorityError(f"built view invalid for {task_id}: {errs[0]}")
        views.append(view)
    # Final checks at logical return (no LIVE): recheck pins+ctx, revalidate
    # basis content (nonrecursive DS/content, true root), recheck again.

    def _revalidate_low_build_owner() -> None:
        evidence_mod._validate_evidence_package_basis_content(
            repo_root, pkg_target, package, _low_expect,
            ds_context["root_records"], ds_context["root_path"],
        )

    evidence_mod._finish_authority_phase(
        repo_root, _low_ctx, _low_pins, revalidate_owner=_revalidate_low_build_owner
    )
    return {
        "cards": cards,
        "views": views,
        "planned_files": [
            {"dir": str(results_dir), "count": len(cards)},
            {"dir": str(views_dir), "count": len(views)},
        ],
    }


def accept_revision_evidence_views_from_paths(
    repo_root: Path,
    package_path: Path,
    results_dir: Path,
    views_dir: Path,
    profile_path: Path,
    evidence_accepted_root: Path,
    views_accepted_root: Path,
    *,
    request_path: Path,
    before_copy_path: Path,
) -> dict[str, Any]:
    """Pure acceptance computation with REAL validators and REAL digests.

    Reads proposed card/view files from exact result/view dirs (no directory
    listing as authority beyond exact task-bound filenames), validates each via
    real validate_evidence_card/validate_edition_view, and builds real
    acceptance payloads with exact required keys and real
    _evidence_result_set_digest/_view_set_digest. No hashed constants, no
    invented MATERIAL/COMPLETE, no placeholder rows. request_path and
    before_copy_path are REQUIRED keyword-only (None refused; never guessed):
    the true historical R/E is derived from the same request + retained COPY,
    the package basis is re-validated through the State-free evidence content
    core with that true root, and package paths are bound to the accepted
    D/S chain.
    """
    from scripts import survey_evidence_v2 as evidence_mod

    repo_root = _norm_path(repo_root, "repo_root")
    package_path = _norm_path(package_path, "revision package path")
    results_dir = _norm_path(results_dir, "results dir")
    views_dir = _norm_path(views_dir, "views dir")
    profile_path = _norm_path(profile_path, "profile path")
    evidence_accepted_root = _norm_path(evidence_accepted_root, "evidence accepted root")
    views_accepted_root = _norm_path(views_accepted_root, "views accepted root")
    if request_path is None or before_copy_path is None:
        raise ResearchAuthorityError(
            "accept_revision_evidence_views_from_paths requires request_path and "
            "before_copy_path (None refused; never infer request/COPY)"
        )
    request_path = _norm_path(request_path, "revision request path")
    before_copy_path = _norm_path(before_copy_path, "retained state-before COPY path")
    request = load_revision_request(repo_root, request_path)
    ds_context = derive_ordinary_root_effective_context(repo_root, request_path, before_copy_path)
    pkg_target = package_path if Path(package_path).is_absolute() else (repo_root / str(package_path))
    pkg_raw = _safe_read_bytes(pkg_target, "revision package")
    package = _strict_parse_object(pkg_raw, "revision package")
    # Package basis re-validated through the State-free evidence content core
    # with the true historical root (never E-as-R, never None,None). Canonical
    # path is the loader-derived value, not the request assertion.
    _accept_expectations = {
        "issue_id": request.get("issue_id"),
        "research_profile": request.get("research_profile"),
        "canonical_state_path": ds_context["canonical_state_path"],
    }
    if not _accept_expectations["canonical_state_path"]:
        raise ResearchAuthorityError("request.before_state.path missing (accept stage)")
    try:
        evidence_mod._validate_evidence_package_basis_content(
            repo_root, pkg_target, package, _accept_expectations,
            ds_context["root_records"], ds_context["root_path"],
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"revision package basis invalid against true root: {exc}") from exc
    try:
        _accept_ctx = evidence_mod._resolve_phase_supplement_context(
            repo_root, package, implementation_sha=None,
            screening_acceptance=None, discoveries=None,
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"revision supplement context invalid: {exc}") from exc
    # LOW accept pins: COPY/profile/request/package/tasks/results/views (no LIVE).
    _accept_pin_list: list[tuple[str, Path]] = [
        ("LOW request", request_path if Path(request_path).is_absolute() else (repo_root / str(request_path))),
        ("LOW retained COPY", before_copy_path if Path(before_copy_path).is_absolute() else (repo_root / str(before_copy_path))),
        ("LOW revision package", pkg_target),
    ]
    try:
        _apro_rel = request["profile_ref"]["path"]
        _accept_pin_list.append(("LOW profile", _repo_rel(repo_root, _apro_rel, "request.profile_ref")))
    except Exception:
        pass
    for _m in package.get("tasks", []):
        for _cand in (pkg_target.parent / _m.get("path", ""), pkg_target.parent / "tasks" / Path(_m.get("path", "")).name):
            try:
                if _cand.is_file() and not _cand.is_symlink():
                    _accept_pin_list.append((f"LOW revision task {_m.get('evidence_task_id')}", _cand))
                    break
            except OSError:
                continue
    _accept_pins = evidence_mod._capture_phase_pins(tuple(_accept_pin_list))
    prof_target = profile_path if Path(profile_path).is_absolute() else (repo_root / str(profile_path))
    prof_raw = _safe_read_bytes(prof_target, "profile")
    profile = _strict_parse_object(prof_raw, "profile")
    results_abs = results_dir if Path(results_dir).is_absolute() else (repo_root / str(results_dir))
    views_abs = views_dir if Path(views_dir).is_absolute() else (repo_root / str(views_dir))
    entries: list[dict[str, Any]] = []
    for meta in package.get("tasks", []):
        name = Path(meta["path"]).name
        card_path = results_abs / name
        card_raw = _safe_read_bytes(card_path, f"proposed result {name}")
        card = _strict_parse_object(card_raw, f"proposed result {name}")
        _accept_task = _strict_parse_object(_safe_read_bytes(pkg_target.parent / meta["path"], "package task"), "package task")

        def _accept_batch(_task: dict[str, Any] = _accept_task) -> dict[str, dict[str, Any]]:
            _b = evidence_mod._discovery_task_sources(_task)
            return evidence_mod._merge_supplement_task_sources(_b, _task, _accept_ctx["entries"])

        errs = evidence_mod._validate_card_core(card, _accept_task, meta["sha256"], package, _accept_batch)
        if errs:
            raise ResearchAuthorityError(f"proposed card {meta.get('evidence_task_id')} invalid: {errs[0]}")
        # Status/materiality mapping is enforced by validate_evidence_card plus
        # the detached record validator upstream (REJECTED/HOLD bindings).
        entries.append({
            "evidence_task_id": meta["evidence_task_id"],
            "discovery_ids": list(meta["discovery_ids"]),
            "sha256": hashlib.sha256(card_raw).hexdigest(),
            "status": card["status"],
            "filename": name,
        })
    entries_sorted = sorted(entries, key=lambda r: r["evidence_task_id"])
    package_sha = hashlib.sha256(pkg_raw).hexdigest()
    try:
        result_set_sha = evidence_mod._evidence_result_set_digest(package_sha, entries_sorted)
    except Exception as exc:
        raise ResearchAuthorityError(f"result_set digest failed: {exc}") from exc
    # Screening acceptance SHA: resolve from package basis (real file SHA, not constant).
    screening_ref_path = package.get("basis", {}).get("screening_acceptance_path")
    if not isinstance(screening_ref_path, str):
        raise ResearchAuthorityError("package basis screening_acceptance_path missing")
    screening_abs2 = _repo_rel(repo_root, screening_ref_path, "package screening_acceptance_path")
    screening_raw2 = _safe_read_bytes(screening_abs2, "package screening acceptance")
    screening_sha = hashlib.sha256(screening_raw2).hexdigest()
    evidence_acceptance = {
        "schema_version": DM022_SCHEMA_VERSION,
        "issue_id": package.get("issue_id"),
        "research_profile": package.get("research_profile"),
        "result_set_sha256": result_set_sha,
        "package_sha256": package_sha,
        "screening_acceptance_sha256": screening_sha,
        "result_count": len(entries_sorted),
        "results": entries_sorted,
    }
    if evidence_acceptance["result_count"] != len(entries_sorted) or not entries_sorted:
        raise ResearchAuthorityError("evidence acceptance result_count mismatch")
    view_rows: list[dict[str, Any]] = []
    for row in entries_sorted:
        view_path = views_abs / evidence_mod.view_filename(row["evidence_task_id"])
        view_raw = _safe_read_bytes(view_path, f"proposed view {row['evidence_task_id']}")
        view = _strict_parse_object(view_raw, f"proposed view {row['evidence_task_id']}")
        errs = evidence_mod.validate_edition_view(view, profile, row["sha256"], row["status"])
        if errs:
            raise ResearchAuthorityError(f"proposed view {row['evidence_task_id']} invalid: {errs[0]}")
        if view.get("evidence_sha256") != row["sha256"]:
            raise ResearchAuthorityError(f"view evidence_sha256 drift for {row['evidence_task_id']}")
        view_rows.append({
            "evidence_task_id": row["evidence_task_id"],
            "evidence_sha256": row["sha256"],
            "view_sha256": hashlib.sha256(view_raw).hexdigest(),
            "materiality": view["materiality"]["status"],
            "scope_dimensions": list(view["scope_dimensions"]),
        })
    view_rows_sorted = sorted(view_rows, key=lambda r: r["evidence_task_id"])
    try:
        view_set_sha = evidence_mod._view_set_digest(view_rows_sorted)
    except Exception as exc:
        raise ResearchAuthorityError(f"view_set digest failed: {exc}") from exc
    views_acceptance = {
        "schema_version": DM022_SCHEMA_VERSION,
        "issue_id": package.get("issue_id"),
        "research_profile": package.get("research_profile"),
        "view_set_sha256": view_set_sha,
        "profile_sha256": hashlib.sha256(prof_raw).hexdigest(),
        "evidence_acceptance_sha256": hashlib.sha256(core.json_bytes(evidence_acceptance)).hexdigest(),
        "views": view_rows_sorted,
    }
    # Final checks at logical publication (no LIVE): recheck pins+ctx,
    # revalidate basis content (nonrecursive DS/content, true root), recheck.

    def _revalidate_accept_owner() -> None:
        evidence_mod._validate_evidence_package_basis_content(
            repo_root, pkg_target, package, _accept_expectations,
            ds_context["root_records"], ds_context["root_path"],
        )

    evidence_mod._finish_authority_phase(
        repo_root, _accept_ctx, _accept_pins, revalidate_owner=_revalidate_accept_owner
    )
    return {
        "evidence_acceptance": evidence_acceptance,
        "views_acceptance": views_acceptance,
        "planned_files": [
            {"root": str(evidence_accepted_root), "kind": "evidence-acceptance"},
            {"root": str(views_accepted_root), "kind": "edition-views-acceptance"},
        ],
    }


def build_versioned_ledger_from_paths(
    repo_root: Path,
    profile_path: Path,
    discovery_path: Path,
    screening_acceptance_path: Path,
    evidence_acceptance_path: Path,
    views_acceptance_path: Path,
    *,
    request_path: Path,
    before_copy_path: Path,
) -> dict[str, Any]:
    """Pure versioned Ledger with REAL basis/rows and REAL row validation.

    Reads real profile/Discovery/screening/evidence/views files, derives one
    row per Discovery with exact Screening decision, Evidence task linkage, and
    View disposition (same logic as production build_materiality_ledger, not
    invented MATERIAL). Validates rows via real _check_ledger_rows_content
    (which checks basis SHAs, exactly-one-row-per-Discovery, decision drift,
    task linkage, DROP vs non-DROP dispositions, rationale) plus the FULL
    State-free materiality content core with the true historical root. No
    fabricated rationale constants beyond truthful same-State binding note.
    request_path and before_copy_path are REQUIRED keyword-only (None refused;
    never guessed): supplied Discovery/Screening paths are bound to the same
    accepted D/S chain before rows are derived.
    """
    from scripts import survey_evidence_v2 as evidence_mod
    from scripts import survey_screening_v2 as screening_mod

    repo_root = _norm_path(repo_root, "repo_root")
    profile_path = _norm_path(profile_path, "profile path")
    discovery_path = _norm_path(discovery_path, "discovery path")
    screening_acceptance_path = _norm_path(screening_acceptance_path, "screening acceptance path")
    evidence_acceptance_path = _norm_path(evidence_acceptance_path, "evidence acceptance path")
    views_acceptance_path = _norm_path(views_acceptance_path, "views acceptance path")
    if request_path is None or before_copy_path is None:
        raise ResearchAuthorityError(
            "build_versioned_ledger_from_paths requires request_path and "
            "before_copy_path (None refused; never infer request/COPY)"
        )
    request_path = _norm_path(request_path, "revision request path")
    before_copy_path = _norm_path(before_copy_path, "retained state-before COPY path")
    request = load_revision_request(repo_root, request_path)
    ds_context = derive_ordinary_root_effective_context(repo_root, request_path, before_copy_path)
    # Supplied paths must bind the same accepted chain (resolve + bytes).
    def _must_match(supplied: Path, bound_abs: Path, label: str) -> Path:
        target = supplied if Path(supplied).is_absolute() else (repo_root / str(supplied))
        try:
            if target.resolve() != bound_abs.resolve():
                raise ResearchAuthorityError(
                    f"ledger {label} does not resolve to the bound accepted chain "
                    f"(got {supplied}, want {bound_abs})"
                )
        except OSError as exc:
            raise ResearchAuthorityError(f"ledger {label} resolve failed: {exc}") from exc
        return target

    _must_match(discovery_path, ds_context["effective_path"], "discovery_path")
    _must_match(screening_acceptance_path, _repo_rel(repo_root, ds_context["scp_path"], "bound SCP acceptance"), "screening_acceptance_path")

    def _load(p: Path, label: str) -> tuple[dict[str, Any], bytes]:
        t = p if Path(p).is_absolute() else (repo_root / str(p))
        raw = _safe_read_bytes(t, label)
        return _strict_parse_object(raw, label), raw

    profile, profile_raw = _load(Path(profile_path), "profile")
    # Rows derive from the validated effective set (the supplied path was
    # bound to the same chain above; no second divergent read).
    discoveries = ds_context["effective_records"]
    discovery_abs = ds_context["effective_path"]
    screening_acc, screening_raw = _load(Path(screening_acceptance_path), "screening acceptance")
    evidence_acc, _ = _load(Path(evidence_acceptance_path), "evidence acceptance")
    views_acc, _ = _load(Path(views_acceptance_path), "views acceptance")
    # Real basis (file SHAs, not invented).
    screening_map = {r["discovery_id"]: r for r in screening_acc.get("decisions", []) if isinstance(r, dict)}
    evidence_by_discovery: dict[str, list[str]] = {}
    for row in evidence_acc.get("results", []):
        for did in row.get("discovery_ids", []):
            evidence_by_discovery.setdefault(did, []).append(row["evidence_task_id"])
    view_map = {r["evidence_task_id"]: r["materiality"] for r in views_acc.get("views", []) if isinstance(r, dict)}
    rows: list[dict[str, Any]] = []
    for disc in discoveries:
        if not isinstance(disc, dict):
            raise ResearchAuthorityError("discovery record must be an object")
        did = disc.get("discovery_id")
        decision = screening_map.get(did)
        if decision is None:
            raise ResearchAuthorityError(f"silent drop: Discovery lacks Screening disposition: {did}")
        tasks = sorted(evidence_by_discovery.get(did, []))
        if decision.get("decision") == "DROP":
            if tasks:
                raise ResearchAuthorityError(f"DROP Discovery unexpectedly has Evidence task: {did}")
            dup = decision.get("duplicate_group")
            disp = "DUPLICATE" if dup else "EXCLUDED"
            statuses: list[str] = []
            rationale = decision.get("reason") or "DROP disposition preserved from Screening"
        else:
            if len(tasks) != 1:
                raise ResearchAuthorityError(f"non-DROP Discovery must have exactly one Evidence task: {did}")
            task_id = tasks[0]
            if task_id not in view_map:
                raise ResearchAuthorityError(f"silent drop: Evidence task lacks Edition View: {task_id}")
            statuses = [view_map[task_id]]
            disp = statuses[0]
            dup = None
            rationale = f"Screening={decision.get('decision')}; Edition View={disp}"
        rows.append({
            "discovery_id": did,
            "origin": (disc.get("provenance") or {}).get("origin", "BASE"),
            "screening_decision": decision.get("decision"),
            "downstream_disposition": disp,
            "evidence_task_ids": tasks,
            "evidence_view_statuses": statuses,
            "duplicate_group": dup,
            "rationale": rationale,
        })
    ledger = {
        "schema_version": DM022_SCHEMA_VERSION,
        "issue_id": profile.get("issue_id"),
        "research_profile": profile.get("research_profile"),
        "basis": {
            "production_profile_sha256": hashlib.sha256(profile_raw).hexdigest(),
            "discovery_sha256": hashlib.sha256(_safe_read_bytes(discovery_abs, "discovery set")).hexdigest(),
            "screening_acceptance_sha256": hashlib.sha256(screening_raw).hexdigest(),
            "evidence_acceptance_sha256": hashlib.sha256(_safe_read_bytes(Path(evidence_acceptance_path) if Path(evidence_acceptance_path).is_absolute() else (repo_root / str(evidence_acceptance_path)), "evidence acceptance file")).hexdigest(),
            "edition_views_acceptance_sha256": hashlib.sha256(_safe_read_bytes(Path(views_acceptance_path) if Path(views_acceptance_path).is_absolute() else (repo_root / str(views_acceptance_path)), "views acceptance file")).hexdigest(),
            "evidence_set_sha256": evidence_acc.get("result_set_sha256"),
            "edition_view_set_sha256": views_acc.get("view_set_sha256"),
        },
        "rows": sorted(rows, key=lambda r: r["discovery_id"]),
    }
    # Real row validation (dict-level + file SHA basis inside helper needs files;
    # call the shared pure checker with real discoveries + acceptances).
    try:
        evidence_mod._check_ledger_rows_content(
            ledger, profile, Path(profile_path) if Path(profile_path).is_absolute() else (repo_root / str(profile_path)),
            discovery_abs, Path(screening_acceptance_path) if Path(screening_acceptance_path).is_absolute() else (repo_root / str(screening_acceptance_path)),
            Path(evidence_acceptance_path) if Path(evidence_acceptance_path).is_absolute() else (repo_root / str(evidence_acceptance_path)),
            Path(views_acceptance_path) if Path(views_acceptance_path).is_absolute() else (repo_root / str(views_acceptance_path)),
            screening_acc, evidence_acc, views_acc, discoveries, repo_root,
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"derived ledger rows invalid: {exc}") from exc
    # FULL State-free materiality content core with the true historical root
    # (basis SHAs + row linkage recomputed, not hash-only, never E-as-R).
    # Canonical path is the loader-derived value, not the request assertion.
    _ledger_expectations = {
        "issue_id": request.get("issue_id"),
        "research_profile": request.get("research_profile"),
        "canonical_state_path": ds_context["canonical_state_path"],
    }
    try:
        evidence_mod._validate_materiality_ledger_content(
            ledger, repo_root,
            Path(profile_path) if Path(profile_path).is_absolute() else (repo_root / str(profile_path)),
            discovery_abs,
            Path(screening_acceptance_path) if Path(screening_acceptance_path).is_absolute() else (repo_root / str(screening_acceptance_path)),
            Path(evidence_acceptance_path) if Path(evidence_acceptance_path).is_absolute() else (repo_root / str(evidence_acceptance_path)),
            Path(views_acceptance_path) if Path(views_acceptance_path).is_absolute() else (repo_root / str(views_acceptance_path)),
            _ledger_expectations,
            ds_context["root_records"], ds_context["root_path"],
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"derived ledger FULL content invalid against true root: {exc}") from exc
    return {"ledger": ledger, "planned_files": [{"kind": "materiality-ledger"}]}


def build_versioned_completeness_from_paths(
    repo_root: Path,
    profile_path: Path,
    discovery_path: Path,
    screening_acceptance_path: Path,
    evidence_acceptance_path: Path,
    views_acceptance_path: Path,
    ledger_path: Path,
    request_path: Path,
    old_completeness_path: Path,
    *,
    before_copy_path: Path,
) -> dict[str, Any]:
    """Pure versioned Completeness with Profile-initial union Discovery-named union.

    Preserves/validates the union of Profile-initial and existing
    Discovery-named obligations with exact provenance; never fabricates
    fulfilment. Dimension/description for Profile-missing obligations derive
    from the OLD valid completeness row; no invented defaults. Status comes
    from the explicitly supplied complete obligation rows in the request (which
    must cover the full union); discovery_ids/task_ids are re-derived from
    ledger/Discovery (not trusted blindly). Validates every row via real
    _validate_obligation_shape and the full result via real
    _check_completeness_result_content (which enforces READY/LIMITED/INCOMPLETE,
    never COMPLETE) plus the FULL State-free profile-completeness content core
    with the true historical root. Propagates Discovery-read failures (no
    empty-list fallback, no placeholder task IDs). before_copy_path is
    REQUIRED keyword-only (None refused; never guessed): the named union
    covers initial + root-named + effective-named obligations from the same
    accepted D/S chain.
    """
    from scripts import survey_completeness_v2 as completeness_mod

    repo_root = _norm_path(repo_root, "repo_root")
    profile_path = _norm_path(profile_path, "profile path")
    discovery_path = _norm_path(discovery_path, "discovery path")
    screening_acceptance_path = _norm_path(screening_acceptance_path, "screening acceptance path")
    evidence_acceptance_path = _norm_path(evidence_acceptance_path, "evidence acceptance path")
    views_acceptance_path = _norm_path(views_acceptance_path, "views acceptance path")
    ledger_path = _norm_path(ledger_path, "ledger path")
    request_path = _norm_path(request_path, "revision request path")
    old_completeness_path = _norm_path(old_completeness_path, "old completeness path")
    if before_copy_path is None:
        raise ResearchAuthorityError(
            "build_versioned_completeness_from_paths requires before_copy_path "
            "(None refused; never infer a COPY)"
        )
    before_copy_path = _norm_path(before_copy_path, "retained state-before COPY path")

    def _load(p: Path, label: str) -> tuple[dict[str, Any], bytes]:
        t = p if Path(p).is_absolute() else (repo_root / str(p))
        raw = _safe_read_bytes(t, label)
        return _strict_parse_object(raw, label), raw

    profile, profile_raw = _load(Path(profile_path), "profile")
    ledger, ledger_raw = _load(Path(ledger_path), "ledger")
    old_comp, _ = _load(Path(old_completeness_path), "old completeness")
    request = load_revision_request(repo_root, request_path)
    ds_context = derive_ordinary_root_effective_context(repo_root, request_path, before_copy_path)
    # Supplied Discovery must bind the same effective chain.
    _supplied_disc = discovery_path if Path(discovery_path).is_absolute() else (repo_root / str(discovery_path))
    try:
        if _supplied_disc.resolve() != ds_context["effective_path"].resolve():
            raise ResearchAuthorityError(
                "completeness discovery_path does not resolve to the bound effective Discovery path"
            )
    except OSError as exc:
        raise ResearchAuthorityError(f"completeness discovery_path resolve failed: {exc}") from exc
    discoveries = ds_context["effective_records"]
    scope = profile.get("research_scope", {})
    if not isinstance(scope, dict):
        raise ResearchAuthorityError("profile research_scope invalid")
    initial = scope.get("initial_obligations", []) if isinstance(scope, dict) else []
    initial_ids = {r.get("obligation_id") for r in initial if isinstance(r, dict)}
    # Discovery-named obligations from real Discovery provenance: effective
    # plus root (U = initial + root-named + effective-named; same-State
    # DERIVED chains name obligations through either side).
    named_ids: set[str] = set()
    declaring: dict[str, list[str]] = {}
    for disc in list(ds_context["root_records"]) + discoveries:
        if not isinstance(disc, dict):
            continue
        for oid in (disc.get("provenance") or {}).get("obligation_ids", []) or []:
            if isinstance(oid, str) and oid:
                named_ids.add(oid)
    for disc in discoveries:
        if not isinstance(disc, dict):
            continue
        for oid in (disc.get("provenance") or {}).get("obligation_ids", []) or []:
            if isinstance(oid, str) and oid:
                declaring.setdefault(oid, []).append(disc.get("discovery_id"))
    union_ids = set(initial_ids) | named_ids
    # Request must supply full 7-field rows for the entire union (explicit
    # obligations, not builder-inferred).
    requested = request.get("completeness", {}).get("obligations", [])
    by_id_request = {r.get("obligation_id"): r for r in requested if isinstance(r, dict)}
    if set(by_id_request) != union_ids:
        raise ResearchAuthorityError(
            f"request completeness must cover exact Profile-initial union Discovery-named union: missing={sorted(union_ids - set(by_id_request))} extra={sorted(set(by_id_request) - union_ids)}"
        )
    old_by_id = {r.get("obligation_id"): r for r in old_comp.get("obligations", []) if isinstance(r, dict)}
    ledger_task_by_discovery = {r["discovery_id"]: list(r.get("evidence_task_ids", [])) for r in ledger.get("rows", []) if isinstance(r, dict)}
    full_rows: list[dict[str, Any]] = []
    for oid in sorted(union_ids):
        req = by_id_request[oid]
        if not isinstance(req, dict):
            raise ResearchAuthorityError(f"obligation {oid} must be an object")
        # Dimension/description: request must carry them; if empty, fall back
        # to OLD valid completeness row (same ID) — never invent.
        dim = req.get("dimension")
        desc = req.get("description")
        if (not dim or not desc) and oid in old_by_id:
            if not dim:
                dim = old_by_id[oid].get("dimension")
            if not desc:
                desc = old_by_id[oid].get("description")
            req = {**req, "dimension": dim, "description": desc}
        if not dim or not desc:
            raise ResearchAuthorityError(f"obligation {oid} missing dimension/description (no invented defaults)")
        # discovery_ids re-derived from real Discovery provenance (not trusted).
        dids = sorted(declaring.get(oid, []))
        if not dids:
            # Profile-initial obligations with no declaring Discovery: empty list
            # is legitimate (profile-level obligation); do not invent.
            dids = list(req.get("discovery_ids", []) or [])
            if dids:
                # If request claims declaring DIDs, they must be real.
                if not set(dids).issubset({d.get("discovery_id") for d in discoveries if isinstance(d, dict)}):
                    raise ResearchAuthorityError(f"obligation {oid} references unknown Discovery")
        task_ids = sorted({t for did in dids for t in ledger_task_by_discovery.get(did, [])})
        # If no declaring Discovery (profile-only), task_ids empty is legitimate.
        row = {
            "obligation_id": oid,
            "dimension": dim,
            "description": desc,
            "status": req.get("status"),
            "discovery_ids": dids,
            "evidence_task_ids": task_ids,
            "rationale": req.get("rationale"),
        }
        errs = completeness_mod._validate_obligation_shape(
            row,
            set(scope.get("scope_dimensions", []) or []),
            {d.get("discovery_id", "") for d in discoveries if isinstance(d, dict)},
            {t for r in ledger.get("rows", []) for t in r.get("evidence_task_ids", [])},
        )
        if errs:
            raise ResearchAuthorityError(f"obligation {oid} invalid: {errs[0]}")
        full_rows.append(row)
    # overall_status via real logic (READY/LIMITED/INCOMPLETE, never COMPLETE).
    needs = sum(r["status"] == "NEEDS_RESEARCH" for r in full_rows)
    lims = [r for r in full_rows if r["status"] == "LIMITATION"]
    residual = request.get("completeness", {}).get("residual_limitations", []) or []
    if needs:
        overall = "INCOMPLETE"
    elif lims or residual:
        overall = "LIMITED"
    else:
        overall = "READY"
    closure_input = request.get("completeness", {}).get("closure")
    closure = None
    if profile.get("research_profile") == "THEMATIC":
        if not isinstance(closure_input, dict):
            raise ResearchAuthorityError("Thematic completeness requires closure/saturation evidence")
        max_pass = max([(d.get("provenance") or {}).get("research_pass", 0) for d in discoveries if isinstance(d, dict)] + [0])
        final_records = [d for d in discoveries if isinstance(d, dict) and (d.get("provenance") or {}).get("research_pass") == max_pass] if max_pass > 0 else []
        by_status = {r["obligation_id"]: r["status"] for r in full_rows}
        final_ids = {oid for d in final_records for oid in ((d.get("provenance") or {}).get("obligation_ids", []) or []) if oid in by_status}
        material_ids = {oid for oid in final_ids if by_status[oid] in ("SATISFIED", "LIMITATION", "NEEDS_RESEARCH")}
        open_ids = {oid for oid in material_ids if by_status[oid] == "NEEDS_RESEARCH"}
        closure = {
            "expansion_passes": max(1, max_pass),
            "final_pass_new_sources": len(final_records),
            "final_pass_new_material_obligations": len(material_ids),
            "final_pass_new_material_obligations_open": len(open_ids),
            "targeted_gap_fill_completed": bool(closure_input.get("targeted_gap_fill_completed")),
            "open_material_obligations": needs,
            "limitations": list(closure_input.get("limitations", []) or []),
            "status": closure_input.get("status"),
        }
        if closure["status"] not in ("COMPLETE", "LIMITED", "NEEDS_RESEARCH"):
            raise ResearchAuthorityError("Thematic closure status must be COMPLETE/LIMITED/NEEDS_RESEARCH")
    elif closure_input is not None:
        raise ResearchAuthorityError("non-Thematic completeness closure must be null")
    result = {
        "schema_version": DM022_SCHEMA_VERSION,
        "issue_id": profile.get("issue_id"),
        "research_profile": profile.get("research_profile"),
        "basis": {
            "production_profile_sha256": hashlib.sha256(profile_raw).hexdigest(),
            "materiality_ledger_sha256": hashlib.sha256(ledger_raw).hexdigest(),
        },
        "overall_status": overall,
        "obligations": sorted(full_rows, key=lambda r: r["obligation_id"]),
        "residual_limitations": list(residual),
        "closure": closure,
    }
    # Real full validation (no swallowed errors, no placeholders).
    ledger_path_abs = ledger_path if Path(ledger_path).is_absolute() else (repo_root / str(ledger_path))
    profile_path_abs = profile_path if Path(profile_path).is_absolute() else (repo_root / str(profile_path))
    discovery_path_abs = ds_context["effective_path"]
    errs: list[str] = []
    try:
        from scripts import survey_evidence_v2 as _ev_mod
        errs = _ev_mod._check_completeness_result_content(
            result, profile, ledger, repo_root, profile_path_abs, ledger_path_abs, []
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"completeness content check failed: {exc}") from exc
    if errs:
        raise ResearchAuthorityError(f"derived completeness invalid: {errs[0]}")
    # Thematic closure counters vs Discovery provenance (real).
    try:
        cerrs = completeness_mod._thematic_closure_errors(
            result, discoveries, {r["obligation_id"]: r for r in full_rows}
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"thematic closure check failed: {exc}") from exc
    if cerrs:
        raise ResearchAuthorityError(f"thematic closure invalid: {cerrs[0]}")
    # FULL State-free profile-completeness content core with the true
    # historical root (obligation/closure recomputed, not hash-only).
    # Canonical path is the loader-derived value, not the request assertion.
    _comp_expectations = {
        "issue_id": request.get("issue_id"),
        "research_profile": request.get("research_profile"),
        "canonical_state_path": ds_context["canonical_state_path"],
    }
    try:
        _comp_errs = completeness_mod._validate_profile_completeness_content(
            result, repo_root, profile_path_abs,
            discovery_path_abs,
            screening_acceptance_path if Path(screening_acceptance_path).is_absolute() else (repo_root / str(screening_acceptance_path)),
            evidence_acceptance_path if Path(evidence_acceptance_path).is_absolute() else (repo_root / str(evidence_acceptance_path)),
            views_acceptance_path if Path(views_acceptance_path).is_absolute() else (repo_root / str(views_acceptance_path)),
            ledger_path_abs,
            _comp_expectations,
            ds_context["root_records"], ds_context["root_path"],
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"completeness FULL content check failed: {exc}") from exc
    if _comp_errs:
        raise ResearchAuthorityError(f"derived completeness FULL content invalid: {_comp_errs[0]}")
    return {"completeness": result, "planned_files": [{"kind": "profile-completeness"}]}


def prove_revision_from_paths(
    repo_root: Path, revision_manifest_path: Path, decision_path: Path, before_copy_path: Path
) -> dict[str, Any]:
    """Deterministic proof over proposed bytes only (no State recursion).

    Binds manifest + supplied independent decision + before COPY; recomputes
    FULL affected/unaffected comparison (every affected ID old/new full content
    + reason + retained Raw + source/event/clock semantics; every unaffected
    row semantic equality except explicit mechanical projections). Validates
    the complete proposed graph with real content validators (evidence/views/
    ledger/completeness + package/tasks), binds tool pins and retention/lineage,
    and returns in-memory proof dict + planned file map. No State recursion;
    LIVE eligibility is checked by HIGH separately. No zero-unaffected PASS, no
    placeholder digests after SELF.
    """
    from scripts import survey_completeness_v2 as completeness_mod
    from scripts import survey_evidence_v2 as evidence_mod
    from scripts import survey_screening_v2 as screening_mod

    repo_root = _norm_path(repo_root, "repo_root")
    revision_manifest_path = _norm_path(revision_manifest_path, "revision manifest path")
    decision_path = _norm_path(decision_path, "decision path")
    before_copy_path = _norm_path(before_copy_path, "retained state-before COPY path")
    revision_manifest_path = _norm_path(revision_manifest_path, "revision manifest path")
    decision_path = _norm_path(decision_path, "decision path")
    before_copy_path = _norm_path(before_copy_path, "retained state-before COPY path")
    man_target = revision_manifest_path if Path(revision_manifest_path).is_absolute() else (repo_root / str(revision_manifest_path))
    dec_target = decision_path if Path(decision_path).is_absolute() else (repo_root / str(decision_path))
    man_raw = _safe_read_bytes(man_target, "revision manifest")
    dec_raw = _safe_read_bytes(dec_target, "supplied decision")
    manifest = _strict_parse_object(man_raw, "revision manifest")
    try:
        schema_gate.validate_instance(manifest, repo_root / str(DM022_MANIFEST_SCHEMA), label="revision manifest")
    except Exception as exc:
        raise ResearchAuthorityError(f"revision manifest schema invalid: {exc}") from exc
    decision = _strict_parse_object(dec_raw, "supplied decision")
    # Decision shape lives in request.$defs.suppliedDecision; validate binding.
    if decision.get("revision_id") != manifest.get("revision_id"):
        raise ResearchAuthorityError("decision revision_id does not match manifest")
    man_sha = hashlib.sha256(man_raw).hexdigest()
    if decision.get("manifest_ref", {}).get("sha256") != man_sha:
        raise ResearchAuthorityError("decision manifest_ref does not bind revision manifest FILE sha")
    if decision.get("before_state", {}).get("sha256") != manifest["before_state"]["sha256"]:
        raise ResearchAuthorityError("decision before_state does not match manifest")
    affected = decision.get("affected_ids", [])
    if not affected or len(set(affected)) != len(affected):
        raise ResearchAuthorityError("decision affected_ids must be nonempty unique")
    allowlist = (decision.get("allowlist") or {}).get("allowed_ids", [])
    if set(affected) != set(allowlist):
        raise ResearchAuthorityError("decision affected_ids must equal allowlist.allowed_ids (exact scope)")
    # Raw refs: every raw file must exist with exact SHA (truthful newly supplied Raw).
    for raw_ref in decision.get("raw_refs", []) or []:
        _sized_ref_shape(raw_ref, "decision.raw_refs[]")
        _verify_sized_ref_bytes(repo_root, raw_ref, "decision raw_ref")
    # Before COPY binding.
    copy_target = before_copy_path if Path(before_copy_path).is_absolute() else (repo_root / str(before_copy_path))
    copy_raw = _safe_read_bytes(copy_target, "retained state-before COPY")
    if hashlib.sha256(copy_raw).hexdigest() != manifest["before_state"]["sha256"]:
        raise ResearchAuthorityError("before COPY does not match manifest before_state")
    # Load OLD vs NEW 4-artifact graphs for full comparison.
    # OLD: from manifest retention? OLD files are the previous checkpoint's 4
    # artifacts (loaded via previous record in derive context). Here we load
    # them via the manifest's before_checkpoint refs? Those are checkpoint
    # records, not acceptances. Instead load OLD acceptances from the retained
    # COPY's provenance? For proof, OLD vs NEW comparison uses:
    #  - OLD evidence/views/ledger/completeness bytes as captured in retention?
    # Retention only holds 7 slots + state-before, not old acceptances. OLD
    # acceptances are canonical files still present (before adoption, old
    # canonical Ledger/Completeness byte-identical). Resolve them via the
    # before-State COPY's provenance? No — before-State points to checkpoint
    # records. Resolve OLD 4 via the previous checkpoint record artifacts.
    # The manifest does not carry previous record path; reconstruct from
    # before_checkpoint evidence ref (first of triplet).
    before_cp_ref = manifest.get("before_checkpoint", {}).get("evidence")
    _artifact_ref_shape(before_cp_ref, "manifest.before_checkpoint.evidence")
    prev_abs = _repo_rel(repo_root, before_cp_ref["path"], "previous checkpoint record")
    prev_raw = _safe_read_bytes(prev_abs, "previous checkpoint record")
    if hashlib.sha256(prev_raw).hexdigest() != before_cp_ref["sha256"]:
        raise ResearchAuthorityError("previous checkpoint record FILE sha drift (proof)")
    prev_typed = load_typed_checkpoint_record(repo_root, prev_abs)
    prev_record = prev_typed["record"]
    if prev_typed["family"] == "PREARCH":
        old_art_rows = prev_record.get("artifacts", [])
    else:
        old_art_rows = prev_record.get("artifacts", [])
    old_by_name = {r["name"]: r for r in old_art_rows if isinstance(r, dict)}
    # Map legacy names to DM022 4 names (legacy evidence record carries same 4 names).
    name_map = {"evidence-acceptance": "evidence-acceptance", "edition-views-acceptance": "edition-views-acceptance", "materiality-ledger": "materiality-ledger", "profile-completeness": "profile-completeness"}
    old_loaded: dict[str, dict[str, Any]] = {}
    for dm_name, legacy_name in name_map.items():
        ref = old_by_name.get(legacy_name)
        if ref is None:
            raise ResearchAuthorityError(f"previous record lacks required artifact: {legacy_name}")
        abs_old = _repo_rel(repo_root, ref["path"], f"OLD {dm_name}")
        raw_old = _safe_read_bytes(abs_old, f"OLD {dm_name}")
        if hashlib.sha256(raw_old).hexdigest() != ref["sha256"]:
            raise ResearchAuthorityError(f"OLD {dm_name} FILE sha drift")
        old_loaded[dm_name] = _strict_parse_object(raw_old, f"OLD {dm_name}")
    # NEW 4 from manifest candidate_outputs (files must exist, HIGH wrote them).
    new_refs = manifest.get("candidate_outputs", {})
    new_loaded: dict[str, dict[str, Any]] = {}
    for key, dm_name in (("evidence_acceptance", "evidence-acceptance"), ("views_acceptance", "edition-views-acceptance"), ("ledger", "materiality-ledger"), ("completeness", "profile-completeness")):
        ref = new_refs.get(key)
        _sized_ref_shape(ref, f"manifest.candidate_outputs.{key}")
        raw_new = _verify_sized_ref_bytes(repo_root, ref, f"NEW {dm_name}")
        new_loaded[dm_name] = _strict_parse_object(raw_new, f"NEW {dm_name}")
    # FULL content validation of the NEW graph via the exact content cores
    # (proposed bytes only, no State). Request provides own-epoch Profile/
    # Discovery/Screening refs; the Discovery file doubles as the DIRECT
    # session root. Per-file manifest refs (tasks/cards/views) are verified
    # here as well, with empty arrays refused outright.
    new_ev = new_loaded["evidence-acceptance"]
    new_vw = new_loaded["edition-views-acceptance"]
    # Request load (own-epoch pins + research_profile authority for expectations).
    req_ref = manifest.get("request") or {}
    _sized_ref_shape(req_ref, "manifest.request")
    req_raw = _verify_sized_ref_bytes(repo_root, req_ref, "manifest request")
    request = _strict_parse_object(req_raw, "manifest request")
    try:
        schema_gate.validate_instance(request, repo_root / str(DM022_REQUEST_SCHEMA), label="manifest request")
    except Exception as exc:
        raise ResearchAuthorityError(f"manifest request schema invalid: {exc}") from exc
    if request.get("revision_id") != manifest.get("revision_id") or request.get("issue_id") != manifest.get("issue_id"):
        raise ResearchAuthorityError("manifest request identity must match manifest")
    for key in ("profile_ref", "discovery_ref", "screening_ref"):
        _sized_ref_shape(request.get(key), f"request.{key}")
        _verify_sized_ref_bytes(repo_root, request[key], f"request {key}")
    prof_abs = _repo_rel(repo_root, request["profile_ref"]["path"], "request profile")
    scr_abs = _repo_rel(repo_root, request["screening_ref"]["path"], "request screening")
    # OLD context (manifest.request + retained COPY) supplies the true
    # historical R/E for the NEW graph FULL content checks (same-State: OLD
    # before-graph R/E == NEW proposed-graph basis). Separate contexts, no
    # new DM016/DM017 policy in either historic pass (classification/loss are
    # HIGH new-admission gates, not retrofitted validators). Never E-as-R.
    _prove_request_abs = _repo_rel(repo_root, req_ref["path"], "manifest request path")
    _old_ctx = derive_ordinary_root_effective_context(repo_root, _prove_request_abs, before_copy_path)
    discoveries = _old_ctx["root_records"]
    disc_abs = _old_ctx["root_path"]
    for art_key, art_label in (("evidence_acceptance", "NEW evidence acceptance"), ("views_acceptance", "NEW views acceptance"), ("ledger", "NEW ledger"), ("completeness", "NEW completeness"), ("package", "NEW package")):
        _sized_ref_shape(new_refs.get(art_key), f"manifest.candidate_outputs.{art_key}")
        _verify_sized_ref_bytes(repo_root, new_refs[art_key], art_label)
    new_ev_abs = _repo_rel(repo_root, new_refs["evidence_acceptance"]["path"], "NEW evidence acceptance")
    new_vw_abs = _repo_rel(repo_root, new_refs["views_acceptance"]["path"], "NEW views acceptance")
    new_ledger_abs = _repo_rel(repo_root, new_refs["ledger"]["path"], "NEW ledger")
    new_comp_abs = _repo_rel(repo_root, new_refs["completeness"]["path"], "NEW completeness")
    new_pkg_abs = _repo_rel(repo_root, new_refs["package"]["path"], "NEW package")
    if not isinstance(new_ev.get("research_profile"), str):
        raise ResearchAuthorityError("NEW evidence acceptance research_profile missing")
    if request.get("research_profile") != new_ev.get("research_profile"):
        raise ResearchAuthorityError("NEW graph research_profile must equal request research_profile")
    expectations = {
        "issue_id": manifest.get("issue_id"),
        "research_profile": request.get("research_profile"),
        "canonical_state_path": _old_ctx["canonical_state_path"],
    }
    if not expectations["canonical_state_path"]:
        raise ResearchAuthorityError("manifest before_state.path missing")
    for arr_key in ("tasks", "cards", "views"):
        arr = new_refs.get(arr_key)
        if not isinstance(arr, list) or not arr:
            raise ResearchAuthorityError(f"manifest candidate_outputs.{arr_key} must be a non-empty per-file binding (no empty arrays)")
        for ref in arr:
            _sized_ref_shape(ref, f"manifest.candidate_outputs.{arr_key}[]")
            _verify_sized_ref_bytes(repo_root, ref, f"NEW {arr_key} file")
    try:
        if evidence_mod._evidence_result_set_digest(new_ev["package_sha256"], new_ev["results"]) != new_ev.get("result_set_sha256"):
            raise ResearchAuthorityError("NEW evidence result_set digest mismatch")
        if evidence_mod._view_set_digest(new_vw["views"]) != new_vw.get("view_set_sha256"):
            raise ResearchAuthorityError("NEW views view_set digest mismatch")
    except ResearchAuthorityError:
        raise
    except Exception as exc:
        raise ResearchAuthorityError(f"NEW acceptance digest recompute failed: {exc}") from exc
    try:
        evidence_mod._validate_evidence_acceptance_content(repo_root, new_ev_abs, expectations, discoveries, disc_abs)
    except Exception as exc:
        raise ResearchAuthorityError(f"FULL NEW evidence acceptance invalid: {exc}") from exc
    try:
        evidence_mod._validate_edition_views_acceptance_content(
            repo_root, prof_abs, new_ev_abs, new_vw_abs, expectations, discoveries, disc_abs
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"FULL NEW views acceptance invalid: {exc}") from exc
    try:
        evidence_mod._validate_materiality_ledger_content(
            new_loaded["materiality-ledger"], repo_root, prof_abs, _old_ctx["effective_path"], scr_abs,
            new_ev_abs, new_vw_abs, expectations, discoveries, disc_abs,
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"FULL NEW materiality ledger invalid: {exc}") from exc
    try:
        comp_errs = completeness_mod._validate_profile_completeness_content(
            new_loaded["profile-completeness"], repo_root, prof_abs, _old_ctx["effective_path"], scr_abs,
            new_ev_abs, new_vw_abs, new_ledger_abs, expectations, discoveries, disc_abs,
        )
    except Exception as exc:
        raise ResearchAuthorityError(f"FULL NEW profile completeness check failed: {exc}") from exc
    if comp_errs:
        raise ResearchAuthorityError(f"FULL NEW profile completeness invalid: {comp_errs[0]}")
    # Decision content (no hash-only admission): exact scope already checked
    # above; assessment/reviewer/recorded_at must be present non-empty shapes.
    for akey in ("interpretation", "event_semantics", "provenance_check"):
        if not isinstance((decision.get("assessment") or {}).get(akey), str) or not (decision.get("assessment") or {})[akey].strip():
            raise ResearchAuthorityError(f"decision assessment.{akey} must be a non-empty string")
    reviewer = decision.get("reviewer")
    if not isinstance(reviewer, dict) or not all(isinstance(reviewer.get(k), str) and reviewer[k].strip() for k in ("provider", "model", "invocation", "recorded_at")):
        raise ResearchAuthorityError("decision reviewer must carry provider/model/invocation/recorded_at")
    raw_list = decision.get("raw_refs", [])
    if not isinstance(raw_list, list) or not raw_list:
        raise ResearchAuthorityError("decision raw_refs must be a non-empty supplied Raw set")
    raw_bytes_by_path: dict[str, bytes] = {}
    for raw_ref in raw_list:
        raw_bytes_by_path[raw_ref["path"]] = _verify_sized_ref_bytes(repo_root, raw_ref, "decision raw_ref")
    # Ledger/completeness full checks via real cores (needs profile/discovery/screening paths from manifest? Use request refs).
    # Affected/unaffected: affected IDs are Discovery IDs with new content.
    # Map Discovery ID -> evidence task -> card/view/ledger-row/obligation.
    old_ev_by_task = {r["evidence_task_id"]: r for r in old_loaded["evidence-acceptance"].get("results", [])}
    new_ev_by_task = {r["evidence_task_id"]: r for r in new_ev.get("results", [])}
    if set(old_ev_by_task) != set(new_ev_by_task):
        raise ResearchAuthorityError("evidence task identity set must be identical OLD vs NEW (same-State, no added/dropped tasks)")
    # Discovery ID -> task mapping from OLD package? Need package files: OLD package
    # is sibling of OLD evidence acceptance (run_dir/package.json); NEW package is
    # manifest candidate package. Load both and compare.
    old_ev_acc_path = _repo_rel(repo_root, old_by_name["evidence-acceptance"]["path"], "OLD evidence acceptance path")
    old_pkg_path = old_ev_acc_path.parent / "package.json"
    try:
        old_pkg_raw = _safe_read_bytes(old_pkg_path, "OLD evidence package")
    except ResearchAuthorityError as exc:
        raise ResearchAuthorityError(f"OLD evidence package missing (run_dir layout required): {exc}") from exc
    old_pkg = _strict_parse_object(old_pkg_raw, "OLD evidence package")
    new_pkg_ref = new_refs.get("package")
    # NEW package ref may be a SizedRef to R/candidate/package.json.
    if isinstance(new_pkg_ref, dict) and "sha256" in new_pkg_ref:
        new_pkg_raw = _verify_sized_ref_bytes(repo_root, new_pkg_ref, "NEW package")
        new_pkg = _strict_parse_object(new_pkg_raw, "NEW package")
    else:
        raise ResearchAuthorityError("manifest candidate_outputs.package must be a SizedRef")
    old_task_by_disc: dict[str, str] = {}
    for meta in old_pkg.get("tasks", []):
        for did in meta.get("discovery_ids", []):
            old_task_by_disc[did] = meta["evidence_task_id"]
    new_task_by_disc: dict[str, str] = {}
    for meta in new_pkg.get("tasks", []):
        for did in meta.get("discovery_ids", []):
            new_task_by_disc[did] = meta["evidence_task_id"]
    if old_task_by_disc != new_task_by_disc:
        raise ResearchAuthorityError("Discovery->task binding must be identical OLD vs NEW")
    # Task IDs for affected Discovery IDs.
    affected_tasks = {old_task_by_disc[did] for did in affected}
    # Unaffected Discovery IDs = non-DROP minus affected.
    all_non_drop = set(old_task_by_disc)
    unaffected_dids = all_non_drop - set(affected)
    # Full affected comparison: old/new card bytes + reason + Raw binding.
    # Cards live in OLD run_dir/results/*.json and NEW R/candidate/results/*.json.
    # For proof (files exist), load and compare full semantics. Raw/event
    # binding: every affected Discovery must route to >=1 supplied Raw file
    # (basename carries the Discovery ID) whose bytes carry the NEW card's
    # first claim text — proving the new card was built from the supplied
    # independent decision's captured sources, not an automatic semantic PASS.
    mechanical: list[dict[str, Any]] = []
    rows_checked = 0
    # Helper to find card file for a task in OLD vs NEW layouts.
    def _old_card_bytes(task_id: str) -> bytes:
        # OLD layout: run_dir/results/<basename> where basename from package meta.
        meta = next(m for m in old_pkg["tasks"] if m["evidence_task_id"] == task_id)
        p = old_ev_acc_path.parent / "results" / Path(meta["path"]).name
        return _safe_read_bytes(p, f"OLD card {task_id}")
    new_cards_dir = None
    # NEW cards dir: sibling of NEW package (R/candidate/results, as HIGH writes).
    try:
        new_pkg_abs = _repo_rel(repo_root, new_pkg_ref["path"], "NEW package path")
        new_cards_dir = new_pkg_abs.parent / "results"
    except Exception as exc:
        raise ResearchAuthorityError(f"NEW cards dir resolve failed: {exc}") from exc
    for did in sorted(all_non_drop):
        task_id = old_task_by_disc[did]
        old_raw = _old_card_bytes(task_id)
        meta = next(m for m in new_pkg["tasks"] if m["evidence_task_id"] == task_id)
        new_raw = _safe_read_bytes(new_cards_dir / Path(meta["path"]).name, f"NEW card {task_id}")
        old_doc = _strict_parse_object(old_raw, f"OLD card {task_id}")
        new_doc = _strict_parse_object(new_raw, f"NEW card {task_id}")
        rows_checked += 1
        if did in set(affected):
            # Affected: must differ in at least one semantic field (not just digest),
            # and new status/materiality must satisfy REJECTED/HOLD mapping (already
            # validated at build).
            if old_raw == new_raw:
                raise ResearchAuthorityError(f"affected Discovery {did} card bytes identical OLD vs NEW (must carry new evidence)")
            new_claims = new_doc.get("claims", [])
            if not isinstance(new_claims, list) or not new_claims or not isinstance(new_claims[0].get("text"), str) or not new_claims[0]["text"]:
                raise ResearchAuthorityError(f"affected Discovery {did} NEW card carries no claim text to bind Raw")
            claim_bytes = new_claims[0]["text"].encode("utf-8")
            routed = [r for r in raw_list if did in Path(r["path"]).name]
            if not routed:
                raise ResearchAuthorityError(f"affected Discovery {did} has no supplied Raw file routed to it (Raw basename must contain the Discovery ID)")
            if not any(claim_bytes in raw_bytes_by_path[r["path"]] for r in routed):
                raise ResearchAuthorityError(f"affected Discovery {did} NEW card claims bind no supplied Raw bytes (must carry the independent decision's captured sources)")
        else:
            # Unaffected: full semantic equality except explicit mechanical digest
            # propagation (task_sha/package_sha/result SHA may change only if package
            # basis SHAs changed due to new files? In same-State with same tasks,
            # package bytes identical, so cards should be byte-identical. Any
            # difference in unaffected card semantic fields refuses.
            if old_doc != new_doc:
                # Allow only mechanical basis SHA propagation? Cards' basis has
                # task_sha256/screening_acceptance_sha256/prompt_sha256/result_contract_sha256.
                # In same-State, all these are identical (same tasks, same screening,
                # same prompt/contracts), so any card difference is semantic drift.
                raise ResearchAuthorityError(f"unaffected Discovery {did} card semantic drift OLD vs NEW")
            # Mechanical digest propagation for acceptances/ledger/completeness
            # basis SHAs is recorded below (field_path level), not per-card.
    # Ledger rows: affected rows may change downstream_disposition/view_statuses/rationale only.
    old_ledger_rows = {r["discovery_id"]: r for r in old_loaded["materiality-ledger"].get("rows", [])}
    new_ledger_rows = {r["discovery_id"]: r for r in new_loaded["materiality-ledger"].get("rows", [])}
    if set(old_ledger_rows) != set(new_ledger_rows):
        raise ResearchAuthorityError("ledger Discovery identity set must be identical OLD vs NEW")
    for did in sorted(old_ledger_rows):
        rows_checked += 1
        old_r = old_ledger_rows[did]
        new_r = new_ledger_rows[did]
        if did in set(affected):
            for key in ("discovery_id", "origin", "screening_decision", "duplicate_group", "evidence_task_ids"):
                if old_r.get(key) != new_r.get(key):
                    raise ResearchAuthorityError(f"affected ledger row {did} immutable field changed: {key}")
        else:
            if old_r != new_r:
                # Ledger basis SHAs are not in rows; rows should be identical for unaffected.
                raise ResearchAuthorityError(f"unaffected ledger row {did} drift OLD vs NEW")
    # Record mechanical projections for ALL propagated digest SHAs (explicit
    # field_path, no directory-prefix exclusion; only actually-differing SHAs
    # are emitted — derived set, never count-only).
    old_pkg_sha = hashlib.sha256(old_pkg_raw).hexdigest()
    new_pkg_sha = new_refs["package"]["sha256"]
    old_comp_basis = (old_loaded["profile-completeness"].get("basis") or {})
    new_comp_basis = (new_loaded["profile-completeness"].get("basis") or {})
    basis_pairs = [
        ("evidence-package.sha256", old_pkg_sha, new_pkg_sha, "same-State revision re-pins package basis.state_sha256 to current LIVE before-State"),
        ("evidence-acceptance.package_sha256", (old_loaded["evidence-acceptance"].get("package_sha256")), new_ev.get("package_sha256"), "new package FILE sha mechanically propagated to evidence acceptance"),
        ("evidence-acceptance.result_set_sha256", old_loaded["evidence-acceptance"].get("result_set_sha256"), new_ev.get("result_set_sha256"), "new card bytes mechanically propagated to result_set digest"),
        ("edition-views-acceptance.view_set_sha256", old_loaded["edition-views-acceptance"].get("view_set_sha256"), new_vw.get("view_set_sha256"), "new view bytes mechanically propagated to view_set digest"),
        ("materiality-ledger.basis.evidence_acceptance_sha256", old_loaded["materiality-ledger"].get("basis", {}).get("evidence_acceptance_sha256"), new_loaded["materiality-ledger"].get("basis", {}).get("evidence_acceptance_sha256"), "new acceptance FILE sha mechanically propagated to ledger basis"),
        ("materiality-ledger.basis.edition_views_acceptance_sha256", old_loaded["materiality-ledger"].get("basis", {}).get("edition_views_acceptance_sha256"), new_loaded["materiality-ledger"].get("basis", {}).get("edition_views_acceptance_sha256"), "new acceptance FILE sha mechanically propagated to ledger basis"),
        ("materiality-ledger.basis.evidence_set_sha256", old_loaded["materiality-ledger"].get("basis", {}).get("evidence_set_sha256"), new_loaded["materiality-ledger"].get("basis", {}).get("evidence_set_sha256"), "new result_set digest mechanically propagated to ledger basis"),
        ("materiality-ledger.basis.edition_view_set_sha256", old_loaded["materiality-ledger"].get("basis", {}).get("edition_view_set_sha256"), new_loaded["materiality-ledger"].get("basis", {}).get("edition_view_set_sha256"), "new view_set digest mechanically propagated to ledger basis"),
        ("profile-completeness.basis.materiality_ledger_sha256", old_comp_basis.get("materiality_ledger_sha256"), new_comp_basis.get("materiality_ledger_sha256"), "new ledger FILE sha mechanically propagated to completeness basis"),
    ]
    for field_path, old_sha, new_sha, reason in basis_pairs:
        if old_sha != new_sha:
            mechanical.append({"field_path": field_path, "old_sha256": old_sha, "new_sha256": new_sha, "reason": reason})
    if rows_checked == 0:
        raise ResearchAuthorityError("comparison rows_checked must be >0 (empty package already refused upstream; zero-row PASS refused)")
    # Tool pins: manifest tool_pins must bind actual current files (no stale pins).
    tool_pins = manifest.get("tool_pins", {})
    for entry in tool_pins.get("tool_shas", []) or []:
        p = entry.get("path")
        if not isinstance(p, str):
            raise ResearchAuthorityError("tool_pins entry path invalid")
        abs_tool = _repo_rel(repo_root, p, "tool pin path")
        raw_tool = _safe_read_bytes(abs_tool, f"tool pin {p}")
        if hashlib.sha256(raw_tool).hexdigest() != entry.get("sha256"):
            raise ResearchAuthorityError(f"tool pin drift for {p} (stale pins refused)")
    proof_body = {
        "schema_version": DM022_SCHEMA_VERSION,
        "issue_id": manifest.get("issue_id"),
        "revision_id": manifest.get("revision_id"),
        "revision_root": manifest.get("revision_root"),
        "manifest": {"path": str(revision_manifest_path if not Path(revision_manifest_path).is_absolute() else Path(revision_manifest_path).relative_to(repo_root.resolve())), "sha256": man_sha, "byte_count": len(man_raw)},
        "decision": {"path": str(decision_path if not Path(decision_path).is_absolute() else Path(decision_path).relative_to(repo_root.resolve())), "sha256": hashlib.sha256(dec_raw).hexdigest(), "byte_count": len(dec_raw)},
        "before_state": manifest.get("before_state"),
        "proposed": {
            "package": new_refs.get("package"),
            "tasks": new_refs.get("tasks", []),
            "cards": new_refs.get("cards", []),
            "views": new_refs.get("views", []),
            "evidence_acceptance": new_refs.get("evidence_acceptance"),
            "views_acceptance": new_refs.get("views_acceptance"),
            "ledger": new_refs.get("ledger"),
            "completeness": new_refs.get("completeness"),
            "result_set_sha256": new_ev.get("result_set_sha256"),
            "view_set_sha256": new_vw.get("view_set_sha256"),
        },
        "affected_ids": sorted(affected),
        "unaffected_comparison": {"rows_checked": rows_checked, "mechanical_projections": mechanical},
        "validations": [{
            "check_id": DM022_PROOF_CHECK_ID,
            "kind": "DETERMINISTIC",
            "status": "PASS",
            "executor": "LOW prove_revision_from_paths",
            "evidence": "proposed-bytes content proof with full affected/unaffected comparison; no State recursion",
            "result": {"path": str(revision_manifest_path if not Path(revision_manifest_path).is_absolute() else Path(revision_manifest_path).relative_to(repo_root.resolve())), "sha256": man_sha, "byte_count": len(man_raw)},
        }],
        "recorded_at": decision.get("recorded_at"),
        "executor": "LOW prove_revision_from_paths",
    }
    digest = _self_digest_hex({k: v for k, v in proof_body.items() if k != "revision_proof_sha256"})
    proof_body["revision_proof_sha256"] = digest
    try:
        schema_gate.validate_instance(proof_body, repo_root / str(DM022_PROOF_SCHEMA), label="revision proof")
    except Exception as exc:
        raise ResearchAuthorityError(f"derived proof schema invalid: {exc}") from exc
    return {"proof": proof_body, "planned_files": [{"kind": "revision-proof"}]}


def check_supersession_record_from_paths(
    repo_root: Path, checkpoint_path: Path, report_path: Path, before_copy_path: Path
) -> list[str]:
    """Detached supersession validation (pure, returns error list, no writes).

    REQUIRED signature: (repo_root, checkpoint_path, report_path,
    before_copy_path) -> list[str]. Empty = pass. Validates the FULL graph:
    checkpoint schema/kind/reason/operation/boundary/checkpoints/artifacts/SELF,
    report schema (NO checkpoint/afterState/guard-hash refs) and cross-bindings
    report.proof/decision/request/manifest/before vs checkpoint proof/decision/
    request/retention, before COPY equality, reviews sole DM022_SUPERSESSION_PROOF,
    own-epoch contract/implementation pins from STORED files (never current
    source, so this stays valid after LIVE advances), retention inventory
    exactly bound to the stored manifest, contract/implementation/profile/
    lineage, and the 4 artifacts via FULL content validators (evidence, views,
    ledger row linkage, completeness obligations/closure — recomputed, not
    hash-only, not trusted booleans).
    """
    repo_root = _norm_path(repo_root, "repo_root")
    checkpoint_path = _norm_path(checkpoint_path, "checkpoint path")
    report_path = _norm_path(report_path, "pre-adoption report path")
    before_copy_path = _norm_path(before_copy_path, "retained state-before COPY path")
    checkpoint_path = _norm_path(checkpoint_path, "checkpoint path")
    report_path = _norm_path(report_path, "pre-adoption report path")
    before_copy_path = _norm_path(before_copy_path, "retained state-before COPY path")
    errors: list[str] = []
    try:
        cp_abs = Path(checkpoint_path) if Path(checkpoint_path).is_absolute() else (repo_root / str(checkpoint_path))
        cp_raw = _safe_read_bytes(cp_abs, "checkpoint FILE")
        cp_sha = hashlib.sha256(cp_raw).hexdigest()
        try:
            cp_rel = str(cp_abs.relative_to(repo_root.resolve()))
        except ValueError:
            cp_rel = str(checkpoint_path)
    except ResearchAuthorityError as exc:
        return [f"checkpoint load failed: {exc}"]
    try:
        full = _verify_adopted_graph_full(repo_root, cp_rel, cp_sha)
    except ResearchAuthorityError as exc:
        return [f"adopted graph FULL validation failed: {exc}"]
    record = full["record"]
    manifest = full["manifest"]
    try:
        report_target = Path(report_path) if Path(report_path).is_absolute() else (repo_root / str(report_path))
        report_raw = _safe_read_bytes(report_target, "pre-adoption report")
        report = _strict_parse_object(report_raw, "pre-adoption report")
    except ResearchAuthorityError as exc:
        return [f"report load failed: {exc}"]
    try:
        schema_gate.validate_instance(report, repo_root / str(DM022_REPORT_SCHEMA), label="pre-adoption report")
    except Exception as exc:
        return [f"report schema invalid: {exc}"]
    # Report must NOT carry checkpoint/afterState/guard-hash refs.
    for forbidden in ("checkpoint", "expected_after_state", "guard_hash", "guard_ref", "after_state_sha256"):
        if forbidden in report:
            errors.append(f"report must not carry {forbidden} (cycle refused)")
    # Cross-bindings: report.proof/decision/request/manifest/before vs checkpoint,
    # plus report.manifest vs the STORED manifest bytes (own-epoch binding).
    for key in ("proof", "decision", "request"):
        if report.get(key, {}).get("sha256") != record.get(key, {}).get("sha256"):
            errors.append(f"report/checkpoint {key} sha mismatch")
    if report.get("before_state", {}).get("sha256") != record.get("before_state", {}).get("sha256"):
        errors.append("report/checkpoint before_state sha mismatch")
    man_ref = report.get("manifest") or {}
    if not isinstance(man_ref, dict) or man_ref.get("sha256") is None:
        errors.append("report manifest ref missing")
    else:
        try:
            man_raw = _verify_sized_ref_bytes(repo_root, man_ref, "report manifest")
            if hashlib.sha256(man_raw).hexdigest() != man_ref.get("sha256"):
                errors.append("report manifest FILE sha drift")
        except ResearchAuthorityError as exc:
            errors.append(f"report manifest check failed: {exc}")
    # Before COPY binding (stored COPY, valid after LIVE advances). The
    # supplied COPY is verified against the checkpoint's bound retention
    # layout AND the before-State SHA/size: bytes must equal before_state
    # sha/byte_count and byte-equal the layout COPY at the fixed recorded
    # path (never a LIVE-path or basename guess).
    try:
        copy_target = Path(before_copy_path) if Path(before_copy_path).is_absolute() else (repo_root / str(before_copy_path))
        copy_raw = _safe_read_bytes(copy_target, "retained state-before COPY")
        before_ref = record.get("before_state", {})
        if hashlib.sha256(copy_raw).hexdigest() != before_ref.get("sha256"):
            errors.append("checkpoint before_state does not match retained COPY")
        if len(copy_raw) != before_ref.get("byte_count"):
            errors.append("retained COPY byte_count mismatch vs checkpoint before_state")
        rev_root = record.get("revision_root", "")
        layout_abs = _repo_rel(repo_root, f"{rev_root.rstrip('/')}/retention/state-before.json", "bound retention layout COPY")
        try:
            layout_raw = _safe_read_bytes(layout_abs, "bound retention layout COPY")
        except ResearchAuthorityError as exc:
            errors.append(f"bound retention layout COPY unreadable: {exc}")
        else:
            if layout_raw != copy_raw:
                errors.append("supplied COPY bytes differ from the checkpoint-bound retention layout COPY")
    except ResearchAuthorityError as exc:
        errors.append(f"before COPY check failed: {exc}")
    if (record.get("reviews", [{}])[0].get("check_id") if record.get("reviews") else None) != DM022_PROOF_CHECK_ID:
        errors.append("checkpoint review must be exactly DM022_SUPERSESSION_PROOF")
    if len(record.get("reviews", [])) != 1:
        errors.append("checkpoint must carry exactly one DM022_SUPERSESSION_PROOF review")
    # Retention plan must exist and bind 7 rows, exactly matching the stored
    # manifest snapshots (same check as the completion helper enforces).
    try:
        ret_ref = record.get("retention_plan") or {}
        _sized_ref_shape(ret_ref, "checkpoint.retention_plan")
        inv_raw = _verify_sized_ref_bytes(repo_root, ret_ref, "checkpoint retention_plan")
        inventory = _strict_parse_object(inv_raw, "checkpoint retention_plan")
        inv_rows = inventory.get("rows", [])
        if not isinstance(inv_rows, list) or len(inv_rows) != 7:
            errors.append("retention inventory must have exactly 7 rows")
        else:
            man_snapshots = {r.get("slot"): r for r in manifest.get("retention_snapshots", []) if isinstance(r, dict)}
            for row in inv_rows:
                other = man_snapshots.get(row.get("slot"))
                if not isinstance(other, dict) or row != other:
                    errors.append(f"retention inventory row != stored manifest snapshot for slot: {row.get('slot')}")
                    break
    except ResearchAuthorityError as exc:
        errors.append(f"retention_plan check failed: {exc}")
    # Lineage: parent/original_anchor/supersedes shapes (no invented lineage).
    try:
        _artifact_ref_shape(record.get("parent_checkpoint"), "checkpoint.parent_checkpoint")
        _artifact_ref_shape(record.get("original_anchor"), "checkpoint.original_anchor")
        if not isinstance(record.get("supersedes"), list):
            errors.append("checkpoint supersedes must be a list")
    except ResearchAuthorityError as exc:
        errors.append(f"lineage check failed: {exc}")
    return errors


def guard_path_for(source_root: Path) -> Path:
    """Pure join for the fixed canonical guard path (no IO)."""
    return _norm_path(source_root, "source_root") / DM022_GUARD_REL


def lstat_slot(source_root: Path, rel: str) -> dict[str, Any]:
    """Single-lstat slot observation (no follow, no read, no write)."""
    if rel not in SEVEN_SLOTS:
        raise ResearchAuthorityError(f"unknown slot: {rel!r}")
    target = _norm_path(source_root, "source_root") / rel
    try:
        st = os.lstat(target)
    except OSError as exc:
        import errno as _errno

        if exc.errno == _errno.ENOENT:
            return {"slot": rel, "present": False, "lstat_kind": "absent", "errno": exc.errno}
        return {
            "slot": rel,
            "present": False,
            "lstat_kind": "refused",
            "errno": exc.errno,
            "error": str(exc),
        }
    if not _stat.S_ISREG(st.st_mode):
        return {
            "slot": rel,
            "present": True,
            "lstat_kind": "nonregular",
            "mode": oct(st.st_mode),
            "dev": st.st_dev,
            "ino": st.st_ino,
            "size": st.st_size,
        }
    return {
        "slot": rel,
        "present": True,
        "lstat_kind": "regular",
        "mode": oct(st.st_mode),
        "dev": st.st_dev,
        "ino": st.st_ino,
        "size": st.st_size,
    }


def require_no_active_guard(source_root: Path) -> None:
    """Passive guard absence check: ANY present/unreadable/nonregular refuses.

    Signature has no owner/allow-held-by-self/skip params. Guard presence never
    grants permission. ONLY HIGH adopt/resume operate while a bound guard
    exists, after verifying nonce/rev/sha + State disposition.
    """
    guard = guard_path_for(_norm_path(source_root, "source_root"))
    try:
        st = os.lstat(guard)
    except OSError as exc:
        import errno as _errno

        if exc.errno == _errno.ENOENT:
            return
        raise ResearchAuthorityError(
            f"DM022_TRANSITION_ACTIVE: guard unreadable: errno={exc.errno}"
        ) from exc
    if not _stat.S_ISREG(st.st_mode):
        raise ResearchAuthorityError("DM022_TRANSITION_ACTIVE: guard present (nonregular)")
    raise ResearchAuthorityError("DM022_TRANSITION_ACTIVE: guard present")


def _discover_repo_root_from_source(source_root: Path) -> Path:
    """Walk up from source_root to the repo root (holds config file)."""
    cur = _norm_path(source_root, "source_root").resolve()
    for _ in range(8):
        probe = cur / "config" / "survey-production-v2.json"
        try:
            st = os.lstat(probe)
            if _stat.S_ISREG(st.st_mode):
                return cur
        except OSError:
            pass
        parent = cur.parent
        if parent == cur:
            break
        cur = parent
    raise ResearchAuthorityError("cannot discover repo root from source_root")


def require_completion_consistent(source_root: Path, checkpoint_ref: dict[str, Any]) -> None:
    """Verify owned completion receipt for an active PREARCH checkpoint.

    R4 signature (no repo_root): repo root is discovered by walking up from
    source_root to the directory holding config/survey-production-v2.json
    (location only, never content authority). Delegates to the FULL verifier:
    EXACT report $defs/completionReceipt schema, issue/revision/checkpoint
    cross-bindings, retention inventory exactly bound to the stored manifest,
    expected_after recomputed from the retained COPY (never trusted), LIVE
    canonical State reloaded with same-record triplet + FULL adopted-graph
    validation (postread booleans recomputed; forward lifecycle tolerated),
    and seven_plan vs inventory vs current slots with legitimate-regeneration
    tolerance. No State validation beyond the read-only LIVE reload; returns
    None or raises.
    """
    source_root = _norm_path(source_root, "source_root")
    _artifact_ref_shape(checkpoint_ref, "checkpoint_ref")
    repo_root = _discover_repo_root_from_source(source_root)
    _verify_completion_full(repo_root, source_root, checkpoint_ref)
    return None


def require_research_operation_ready(repo_root: Path, state_path: Path) -> None:
    """ONE passive entry for all normal mutating entries (entry+prepublish).

    lstat guard ANY present (well-formed/malformed/nonregular/unreadable)
    refuses DM022_TRANSITION_ACTIVE; else structural kind peek of the State
    file (no validation authority): legacy (no kind or split triplet) -> only
    guard absence required; PREARCH same-record triplet -> guard absent + FULL
    completion verification (EXACT receipt schema, COPY-derived expected_after
    recompute, retained-inventory exact bind, LIVE triplet + FULL graph
    revalidation, seven_plan vs inventory vs slots with legitimate-regeneration
    tolerance: old-absent slots and regenerated new-content/same-byte-new-inode
    outputs do NOT block; only same-inode stale bytes refuse). No
    agent.validate, no verify_state_basis, no HIGH, no guard claim.
    """
    repo_root = _norm_path(repo_root, "repo_root")
    state_path = _norm_path(state_path, "state path")
    abs_state = state_path if state_path.is_absolute() else (repo_root / str(state_path))
    raw_state = _safe_read_bytes(abs_state, "production state")
    state = _strict_parse_object(raw_state, "production state")
    profile_ref = state.get("profile")
    if not isinstance(profile_ref, dict) or set(profile_ref) != {"path", "sha256"}:
        raise ResearchAuthorityError("state.profile authority fields invalid (readiness)")
    profile_abs = _repo_rel(repo_root, profile_ref["path"], "state.profile.path")
    profile_raw = _safe_read_bytes(profile_abs, "production profile")
    if hashlib.sha256(profile_raw).hexdigest() != profile_ref["sha256"]:
        raise ResearchAuthorityError("production profile bytes differ (readiness)")
    profile = _strict_parse_object(profile_raw, "production profile")
    try:
        source_rel = profile["paths"]["source_root"]
    except (KeyError, TypeError) as exc:
        raise ResearchAuthorityError(f"profile source_root invalid: {exc}") from exc
    source_root = _repo_rel(repo_root, source_rel, "paths.source_root")
    require_no_active_guard(source_root)
    prov = state.get("checkpoint_provenance", {})
    if not isinstance(prov, dict):
        raise ResearchAuthorityError("state.checkpoint_provenance missing (readiness)")
    triplet_refs = [prov.get(k) for k in DM022_CHECKPOINTS]
    if not all(isinstance(r, dict) and set(r) == {"path", "sha256"} for r in triplet_refs):
        return
    paths = {r["path"] for r in triplet_refs}
    shas = {r["sha256"] for r in triplet_refs}
    if len(paths) != 1 or len(shas) != 1:
        return
    cp_rel = next(iter(paths))
    cp_sha = next(iter(shas))
    cp_abs = _repo_rel(repo_root, cp_rel, "research checkpoint")
    cp_raw = _safe_read_bytes(cp_abs, "research checkpoint")
    if hashlib.sha256(cp_raw).hexdigest() != cp_sha:
        raise ResearchAuthorityError("DM022_TRANSITION_ACTIVE: checkpoint FILE drift (completion unverifiable)")
    cp_doc = _strict_parse_object(cp_raw, "research checkpoint")
    if not is_prearchitecture_record(cp_doc):
        return
    _verify_completion_full(repo_root, source_root, {"path": cp_rel, "sha256": cp_sha})
    return None
