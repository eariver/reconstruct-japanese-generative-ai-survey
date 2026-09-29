#!/usr/bin/env python3
"""Bounded mechanical-only Weekly receipt/Gate refresh writer (R1).

Renews the live Weekly source receipt and Reader-Surface Gate after a
reviewed helper-only tool change when this edition's entire reviewed input
and rendered output are byte-identical. Pre-decision VALIDATED_DRAFT only.
Uses existing validators/CLI-equivalent library calls; creates no new review
authority, schema, config role or build workflow.

Owned live writes: receipt, Gate (atomic replace), plus the existing
revalidation API's new record and State pointer. Retention, temp files and
the cooperative guard are inert operating evidence.
"""
from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality
from scripts import survey_reader_publication_v2 as reader
from scripts import survey_reader_surface_gate_v2 as surface_gate
from scripts import survey_schema_v2 as schema_gate
from scripts import survey_weekly_derivation_v2 as weekly

ALLOWED_CHANGED_PATH = Path("scripts/survey_weekly_derivation_v2.py")
RECEIPT_FILENAME = "validated-source-manifest.json"
GATE_FILENAME = "reader-surface-gate-v2.json"
LOCK_FILENAME = ".mechanical-refresh.lock"
RETENTION_DIRNAME = ".mechanical-refresh-retention"
REASON_CLASS = "REVIEWED_CORE_CHANGE"


class MechanicalRefreshError(ValueError):
    pass


def _rel(root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)


def _control_paths(cfg: dict[str, Any]) -> list[str]:
    paths = [core.DEFAULT_CONFIG.as_posix(), *cfg["implementation_control_roots"]]
    paths.append(weekly.STYLE_PATH.as_posix())
    paths.extend(p for rows in cfg["contract_files"].values() for p in rows)
    return sorted(set(paths))


def _reject_symlink_ancestors(root: Path, path: Path, label: str) -> None:
    """Reject symlink ancestors/aliases for retention/guard/temp/live targets.

    Walks lexical components from the resolved repo root to the target's
    parent, refusing any symlink component. The target itself must not be a
    symlink. Resolving first would erase alias information and permit
    out-of-root writes (e.g. retention_base following a symlink out of root).
    No global CAS or power-loss durability is claimed beyond the selected
    exclusive-create/replace file operations.
    """
    root_resolved = root.resolve()
    # Determine lexical absolute parent without resolving symlinks.
    lexical_parent = path.parent if path.is_absolute() else (root_resolved / path.parent)
    try:
        rel_parts = lexical_parent.relative_to(root_resolved).parts
    except ValueError as exc:
        raise MechanicalRefreshError(f"refresh {label} escapes repository root: {path}") from exc
    current = root_resolved
    for part in rel_parts:
        if part in ("..", ".", ""):
            raise MechanicalRefreshError(f"refresh {label} has unsafe path component: {part}")
        current = current / part
        try:
            if current.is_symlink():
                raise MechanicalRefreshError(f"refresh {label} has symlinked ancestor component: {current}")
        except OSError as exc:
            raise MechanicalRefreshError(f"refresh {label} ancestor check failed: {current}: {exc}") from exc
    try:
        if path.is_symlink():
            raise MechanicalRefreshError(f"refresh {label} is a symlink/refusal: {path}")
    except OSError as exc:
        raise MechanicalRefreshError(f"refresh {label} symlink check failed: {path}: {exc}") from exc


def _safe_existing_file(root: Path, rel: str, label: str) -> Path:
    """Resolve a repository-relative file with lexical + ancestor + resolve checks.

    Validates the raw relative path lexically (no traversal/backslash/absolute),
    rejects symlink ancestors before resolution, resolves via core.repo_local_path,
    re-verifies under root, and refuses symlink/missing targets. Used for all
    retention/live/config/State/publication/manuscript/reader-input/receipt/Gate
    targets derived from Profile authority.
    """
    if not isinstance(rel, str) or not rel or "\\" in rel:
        raise MechanicalRefreshError(f"refresh {label} must be a repository-relative path without backslash: {rel!r}")
    raw = Path(rel)
    if raw.is_absolute() or ".." in raw.parts:
        raise MechanicalRefreshError(f"refresh {label} must be repository-local without traversal: {rel}")
    try:
        resolved = core.repo_local_path(root, rel, label)
    except (TypeError, ValueError) as exc:
        raise MechanicalRefreshError(f"refresh {label} invalid: {exc}") from exc
    _reject_symlink_ancestors(root, resolved, label)
    # Re-verify still under root after ancestor checks (no TOCTOU blessing).
    try:
        resolved.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise MechanicalRefreshError(f"refresh {label} escapes repository root: {rel}") from exc
    if resolved.is_symlink() or not resolved.is_file():
        raise MechanicalRefreshError(f"refresh {label} missing or unsafe: {rel} -> {resolved}")
    return resolved


def _exclusive_bytes(path: Path, data: bytes, label: str) -> None:
    # Ancestor rejection is performed by the caller with the operation root
    # for precise error context; this helper enforces exclusive creation only.
    if path.is_symlink() or path.exists():
        raise MechanicalRefreshError(f"refresh {label} collision/refusal: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "xb") as fh:
            fh.write(data)
            fh.flush()
            try:
                os.fsync(fh.fileno())
            except OSError:
                pass
    except FileExistsError as exc:
        raise MechanicalRefreshError(f"refresh {label} collision/refusal: {path}") from exc
    # Verify exclusive bytes equal expected, not whatever raced onto disk.
    try:
        if path.read_bytes() != data:
            raise MechanicalRefreshError(
                f"refresh {label} bytes mismatch after exclusive create: {path}; live bytes preserved"
            )
    except OSError as exc:
        raise MechanicalRefreshError(f"refresh {label} readback failed: {path}: {exc}") from exc


def _atomic_replace(path: Path, data: bytes, label: str, run_id: str, expected_old_sha256: str | None = None) -> None:
    if path.is_symlink() or not path.is_file():
        raise MechanicalRefreshError(f"refresh {label} missing or unsafe: {path}")
    if expected_old_sha256 is not None:
        try:
            current_sha = core.sha256_file(path)
        except OSError as exc:
            raise MechanicalRefreshError(f"refresh {label} read failed before replace: {path}: {exc}") from exc
        if current_sha != expected_old_sha256:
            raise MechanicalRefreshError(
                f"refresh {label} drift before replace at {path} "
                f"(expected {expected_old_sha256[:16]}.., found {current_sha[:16]}..); "
                "live bytes + retention + guard preserved for manual recovery"
            )
    tmp = path.parent / f".{path.name}.tmp-{run_id}"
    if tmp.is_symlink() or tmp.exists():
        raise MechanicalRefreshError(f"refresh {label} temp collision: {tmp}")
    with open(tmp, "xb") as fh:
        fh.write(data)
        fh.flush()
        try:
            os.fsync(fh.fileno())
        except OSError:
            pass
    try:
        if tmp.read_bytes() != data:
            try:
                tmp.unlink(missing_ok=True)
            except OSError:
                pass
            raise MechanicalRefreshError(f"refresh {label} temp bytes mismatch; live bytes untouched")
    except OSError as exc:
        if isinstance(exc, MechanicalRefreshError):
            raise
        raise MechanicalRefreshError(f"refresh {label} temp readback failed: {tmp}: {exc}") from exc
    # Immediate target recheck: destination must still equal expected old bytes.
    if expected_old_sha256 is not None:
        try:
            if core.sha256_file(path) != expected_old_sha256:
                try:
                    tmp.unlink(missing_ok=True)
                except OSError:
                    pass
                raise MechanicalRefreshError(
                    f"refresh {label} destination changed before replace at {path}; "
                    "live bytes + retention + guard preserved for manual recovery"
                )
        except OSError as exc:
            if isinstance(exc, MechanicalRefreshError):
                raise
            try:
                tmp.unlink(missing_ok=True)
            except OSError:
                pass
            raise MechanicalRefreshError(f"refresh {label} pre-replace recheck failed: {exc}") from exc
    os.replace(tmp, path)
    try:
        if core.sha256_file(path) != core.sha256_bytes(data):
            raise MechanicalRefreshError(f"refresh {label} post-replace mismatch at {path}; manual recovery required")
    except OSError as exc:
        raise MechanicalRefreshError(f"refresh {label} post-replace readback failed: {exc}") from exc


def _release_guard_if_owned(lock_path: Path, expected_bytes: bytes, label: str) -> None:
    """Release only an unchanged operation-owned guard.

    Refuses to delete a foreign/replaced/removed guard; preserves lock +
    retention + unknown bytes on conflict for manual recovery. Never steals a
    stale lock automatically.
    """
    try:
        if lock_path.is_symlink():
            raise MechanicalRefreshError(
                f"refresh {label} guard is a symlink at {lock_path}; preserved for manual recovery"
            )
        if not lock_path.is_file():
            raise MechanicalRefreshError(
                f"refresh {label} guard missing at {lock_path}; preserved state requires manual recovery"
            )
        current = lock_path.read_bytes()
    except OSError as exc:
        if isinstance(exc, MechanicalRefreshError):
            raise
        raise MechanicalRefreshError(f"refresh {label} guard read failed at {lock_path}: {exc}") from exc
    if current != expected_bytes:
        raise MechanicalRefreshError(
            f"refresh {label} guard changed (expected run_id hash {core.sha256_bytes(expected_bytes)[:16]}.., "
            f"found {core.sha256_bytes(current)[:16]}..); foreign guard preserved, no deletion performed"
        )
    try:
        lock_path.unlink()
    except OSError as exc:
        raise MechanicalRefreshError(f"refresh {label} guard release failed at {lock_path}: {exc}") from exc


def _capture_bound_snapshot(
    root: Path,
    *,
    state_path: Path,
    state_sha: str,
    gate_path: Path,
    gate_sha: str,
    receipt_path: Path,
    receipt_sha: str,
    old_receipt: dict[str, Any],
    checkpoint_path: Path,
    checkpoint_sha: str,
    checkpoint: dict[str, Any],
    manuscript_path: Path,
    head: str,
    cfg: dict[str, Any],
) -> dict[str, str]:
    """Snapshot all VALIDATED source dependencies vs expected originals.

    Covers receipt input refs (accepted/authored), reviewed input, semantic
    review, outputs, old Gate/manuscript/reviews/PDF/bundle + deterministic
    result refs, checkpoints/prior chain, config + control files, profile/HEAD.
    Keys are repo-relative paths (or __HEAD__/__STATE__ sentinels); values are
    expected sha256. Rechecked after guard, before each live write and
    rollback/commit-sensitive operation. Never blessed by re-hashing after drift.
    """
    snap: dict[str, str] = {}
    snap["__HEAD__"] = head
    snap["__STATE__:" + _rel(root, state_path)] = state_sha
    snap["__GATE__:" + _rel(root, gate_path)] = gate_sha
    snap["__RECEIPT__:" + _rel(root, receipt_path)] = receipt_sha
    snap["__CHECKPOINT__:" + _rel(root, checkpoint_path)] = checkpoint_sha
    # Receipt-bound inputs/outputs (accepted/authored/reviewed/semantic/outputs).
    for group_key in ("accepted_refs", "authored_refs"):
        for row in old_receipt.get(group_key, []):
            snap[_rel(root, _safe_existing_file(root, row["path"], f"snapshot {row.get('name')}"))] = row["sha256"]
    for single_key in ("reviewed_reader_input", "semantic_review"):
        row = old_receipt.get(single_key, {})
        if isinstance(row, dict) and "path" in row:
            snap[_rel(root, _safe_existing_file(root, row["path"], f"snapshot {single_key}"))] = row["sha256"]
    for out_name, row in (old_receipt.get("outputs", {}) or {}).items():
        if isinstance(row, dict) and "path" in row:
            snap[_rel(root, _safe_existing_file(root, row["path"], f"snapshot output {out_name}"))] = row["sha256"]
    # Checkpoint artifacts (manuscript/bundle/reviews/PDF Gate inputs).
    # For repeat refresh, the Gate row in the validation checkpoint still carries
    # the original sha, while live Gate is the previously renewed effective sha
    # (old_gate_sha). The effective Gate is already pinned via __GATE__ above;
    # do not also pin the stale checkpoint Gate row as requiring live match.
    gate_rel_canonical = _rel(root, gate_path)
    for row in checkpoint.get("artifacts", []):
        if isinstance(row, dict) and "path" in row and "sha256" in row:
            if row.get("name") == "reader-surface-gate" and row.get("path") == gate_rel_canonical:
                continue
            try:
                snap[_rel(root, _safe_existing_file(root, row["path"], f"snapshot checkpoint {row.get('name')}"))] = row["sha256"]
            except MechanicalRefreshError:
                # Checkpoint rows that are not files (e.g. synthetic) are still
                # pinned by their recorded sha; recheck will fail closed if drifted.
                snap[row["path"]] = row["sha256"]
    # Manuscript file itself (canonical).
    snap[_rel(root, manuscript_path)] = core.sha256_file(manuscript_path)
    # Config + control files + profile.
    try:
        snap[core.DEFAULT_CONFIG.as_posix()] = core.sha256_file(root / core.DEFAULT_CONFIG)
    except OSError:
        pass
    for rel in _control_paths(cfg):
        # Control roots may include whole directories (implementation roots);
        # snapshot only real files. Directories are covered by the git-diff
        # allowed-change gate, not by single-file hashing. Missing files are
        # fail-closed at recheck.
        candidate = root / rel
        try:
            if candidate.is_symlink():
                raise MechanicalRefreshError(f"snapshot control symlink: {rel}")
            if candidate.is_dir():
                continue
            if not candidate.is_file():
                snap[rel] = "__MISSING__"
                continue
            p = _safe_existing_file(root, rel, f"snapshot control {rel}")
            snap[_rel(root, p)] = core.sha256_file(p)
        except MechanicalRefreshError as merr:
            # Directory skips already handled; other failures are fail-closed.
            if candidate.is_dir() and not candidate.is_symlink():
                continue
            snap[rel] = "__MISSING__"
    return snap


def _recheck_bound_snapshot(root: Path, snap: dict[str, str], label: str) -> None:
    """Recheck complete bound snapshot; reject detected drift without normalizing."""
    # HEAD first (implementation identity).
    expected_head = snap.get("__HEAD__")
    if expected_head is not None:
        actual_head = core.repository_commit_sha(root)
        if actual_head != expected_head:
            raise MechanicalRefreshError(
                f"refresh {label}: HEAD drift (expected {expected_head[:16]}.., found {actual_head[:16]}..); "
                "live bytes + retention + guard preserved for manual recovery"
            )
    for key, expected_sha in snap.items():
        if key == "__HEAD__":
            continue
        if key.startswith("__STATE__:") or key.startswith("__GATE__:") or key.startswith("__RECEIPT__:") or key.startswith("__CHECKPOINT__:"):
            rel = key.split(":", 1)[1]
        else:
            rel = key
        if expected_sha == "__MISSING__":
            # Control path was missing at capture; any appearance is drift.
            candidate = root / rel
            if candidate.exists() or candidate.is_symlink():
                raise MechanicalRefreshError(
                    f"refresh {label}: unexpected control file appeared at {rel}; manual recovery required"
                )
            continue
        try:
            target = root / rel
            # Use safe resolution to avoid alias blessing.
            safe = _safe_existing_file(root, rel, f"recheck {label} {rel}")
            actual = core.sha256_file(safe)
        except (MechanicalRefreshError, OSError) as exc:
            raise MechanicalRefreshError(
                f"refresh {label}: dependency unreadable at {rel}: {exc}; manual recovery required"
            ) from exc
        if actual != expected_sha:
            raise MechanicalRefreshError(
                f"refresh {label}: dependency drift at {rel} "
                f"(expected {expected_sha[:16]}.., found {actual[:16]}..); "
                "live bytes + retention + guard preserved, no overwrite of unknown bytes"
            )


def _compare_gate_reports(
    old: dict[str, Any],
    new: dict[str, Any],
    *,
    old_receipt_rel: str,
    old_receipt_sha: str,
    new_receipt_sha: str,
) -> None:
    """Complete old/new Gate equality except selected machine metadata/digest/receipt.

    Preserves all semantic-authority/report fields except explicitly allowed
    evaluation metadata (evaluated_by/recorded_at + semantic recorded_at/reviewed_at),
    internal digest (gate_sha256) and the exact receipt derivation reference.
    No dropped findings/suppressions/scan scope is permitted.
    """
    # Top-level exact equality except allowed evaluation metadata/digest/receipt
    # and semantic_authority (handled in detail below to allow timestamp advance).
    allowed_top = {"recorded_at", "gate_sha256", "derivation", "semantic_authority"}
    for key in set(old) | set(new):
        if key in allowed_top:
            continue
        if old.get(key) != new.get(key):
            raise MechanicalRefreshError(f"renewed Gate {key} changed; no silent finding/scope drop permitted")
    # evaluated_by must be stable; recorded_at is allowed to advance.
    if old.get("evaluated_by") != new.get("evaluated_by"):
        raise MechanicalRefreshError("renewed Gate evaluated_by changed")
    # Derivation: only receipt reference may change to the new receipt hash.
    old_der = dict(old.get("derivation", {}))
    new_der = dict(new.get("derivation", {}))
    if old_der.get("route") != new_der.get("route") or old_der.get("scope") != new_der.get("scope"):
        raise MechanicalRefreshError("renewed Gate derivation route/scope changed")
    if old_der.get("receipt") != {"path": old_receipt_rel, "sha256": old_receipt_sha}:
        raise MechanicalRefreshError("old Gate receipt derivation does not match retained old receipt")
    if new_der.get("receipt") != {"path": old_receipt_rel, "sha256": new_receipt_sha}:
        raise MechanicalRefreshError("renewed Gate receipt derivation mismatch")
    # Semantic authority: all fields except machine evaluation metadata
    # (recorded_at/reviewed_at timestamps and human-readable summary).
    # The wrapper-built old Gate uses summary "Bound semantic review passed"
    # while direct evaluate derives summary from the review file; both bind the
    # same review file path/digest/decision, so summary is evaluation metadata.
    old_sem = dict(old.get("semantic_authority", {}))
    new_sem = dict(new.get("semantic_authority", {}))
    for ts_key in ("recorded_at", "reviewed_at", "summary"):
        old_sem.pop(ts_key, None)
        new_sem.pop(ts_key, None)
    if old_sem != new_sem:
        # Precise diff for manual recovery.
        for k in set(old_sem) | set(new_sem):
            if old_sem.get(k) != new_sem.get(k):
                raise MechanicalRefreshError(f"renewed Gate semantic_authority.{k} changed")
        raise MechanicalRefreshError("renewed Gate semantic_authority changed")


def refresh_mechanical_evidence(
    repo_root: Path,
    cfg: dict[str, Any],
    state_path: Path,
    reason: str,
    executor: str,
    recorded_at: datetime,
) -> dict[str, Any]:
    """Execute one bounded mechanical receipt/Gate refresh. See §4 protocol."""
    from scripts import survey_agent_control_v2 as agent

    root = repo_root.resolve()
    if not isinstance(reason, str) or not reason.strip():
        raise MechanicalRefreshError("refresh requires a non-empty reason")
    if not isinstance(executor, str) or not executor.strip():
        raise MechanicalRefreshError("refresh requires executor identity")
    try:
        run_id = core.iso_utc(recorded_at).replace(":", "").replace("-", "").replace("Z", "Z")
    except Exception as exc:
        raise MechanicalRefreshError(f"refresh recorded_at invalid: {exc}") from exc

    # ---- P0 preflight (read-only) ----
    # Canonical cfg passed to library too: writer requires exact canonical default config.
    try:
        canonical_cfg = core.load_json(root / core.DEFAULT_CONFIG)
    except (OSError, ValueError) as exc:
        raise MechanicalRefreshError(f"refresh canonical config unreadable: {exc}") from exc
    if cfg != canonical_cfg:
        raise MechanicalRefreshError("refresh requires the canonical default config bytes (no alternate-config authority)")
    _reject_symlink_ancestors(root, root / core.DEFAULT_CONFIG, "canonical config")
    try:
        state_rel_raw = _rel(root, state_path)
    except ValueError as exc:
        raise MechanicalRefreshError(f"refresh Production State must be repository-local: {exc}") from exc
    state_path = _safe_existing_file(root, state_rel_raw, "Production State")
    state = core.load_json(state_path)
    head = core.repository_commit_sha(root)
    state_sha_p0 = core.sha256_file(state_path)
    # Canonical State path must be Profile-derived (source_root + authoritative filename).
    try:
        profile_rel_raw = state.get("profile", {}).get("path", "")
        profile_path_p0 = _safe_existing_file(root, profile_rel_raw, "Production Profile")
        profile_p0 = core.load_json(profile_path_p0)
        source_root_p0 = core.repo_local_path(root, profile_p0["paths"]["source_root"], "Weekly source root")
        _reject_symlink_ancestors(root, source_root_p0, "Weekly source root")
        canonical_state = (source_root_p0 / cfg["state_authority"]["authoritative_filename"]).resolve()
        if state_path.resolve() != canonical_state:
            raise MechanicalRefreshError(
                f"refresh State path is not canonical Profile-derived: {_rel(root, state_path)} != {_rel(root, canonical_state)}"
            )
    except (KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, MechanicalRefreshError):
            raise
        raise MechanicalRefreshError(f"refresh Profile/source_root resolution failed: {exc}") from exc

    conditions = agent._pending_conditions(state)
    # _pending_conditions covers lifecycle/human-gates/checkpoints/exception.
    if conditions:
        raise MechanicalRefreshError("; ".join(conditions))
    if agent.validate_agent_state(root, cfg, state):
        raise MechanicalRefreshError(
            "refresh strict State invalid: " + "; ".join(agent.validate_agent_state(root, cfg, state))
        )
    active, active_errors = agent.resolve_active_publication_revalidation(root, cfg, state)
    if active_errors:
        raise MechanicalRefreshError("refresh active predecessor invalid: " + "; ".join(active_errors))

    validation_ref = state.get("checkpoint_provenance", {}).get("validation")
    if not isinstance(validation_ref, dict) or set(validation_ref) != {"path", "sha256"}:
        raise MechanicalRefreshError("refresh requires exact validation checkpoint reference")
    checkpoint_path = _safe_existing_file(root, validation_ref["path"], "validation checkpoint")
    if core.sha256_file(checkpoint_path) != validation_ref["sha256"]:
        raise MechanicalRefreshError("validation checkpoint provenance drift")
    checkpoint = schema_gate.load_and_validate_json(
        checkpoint_path, root / agent.CHECKPOINT_SCHEMA, label="refresh validation checkpoint"
    )
    if (
        checkpoint.get("issue_id") != state.get("issue_id")
        or checkpoint.get("from_state") != "DRAFT_COMPLETE"
        or checkpoint.get("to_state") != "VALIDATED_DRAFT"
        or "validation" not in checkpoint.get("checkpoints", [])
    ):
        raise MechanicalRefreshError("refresh validation checkpoint identity/producer mismatch")

    roles = agent._publication_revalidation_roles(root, cfg, state)
    gate_rel = roles.get("reader-surface-gate")
    if not gate_rel:
        raise MechanicalRefreshError("refresh Gate role is not canonical")
    ck_rows = {(r.get("name"), r.get("path")): r for r in checkpoint.get("artifacts", []) if isinstance(r, dict)}
    ck_gate = ck_rows.get(("reader-surface-gate", gate_rel))
    if ck_gate is None:
        raise MechanicalRefreshError("checkpoint lacks canonical reader-surface-gate row")
    ms_rows = [k for k in ck_rows if k[0] == "reader-manuscript"]
    if len(ms_rows) != 1:
        raise MechanicalRefreshError("checkpoint must carry exactly one reader-manuscript row")
    manuscript_rel = ms_rows[0][1]
    manuscript_path = _safe_existing_file(root, manuscript_rel, "refresh manuscript")

    if active is None:
        old_gate_sha = ck_gate["sha256"]
        supersedes: dict[str, str] | None = None
    else:
        if active.get("prior_checkpoint") != validation_ref:
            raise MechanicalRefreshError("active revalidation does not bind the active validation checkpoint")
        effective = {
            (r["name"], r["path"]): r["new_sha256"] for r in active.get("superseded_artifacts", [])
        }
        effective.update({(r["name"], r["path"]): r["sha256"] for r in active.get("preserved_artifacts", [])})
        old_gate_sha = effective.get(("reader-surface-gate", gate_rel))
        if not old_gate_sha:
            raise MechanicalRefreshError("active revalidation has no effective reader-surface-gate row")
        ptr = state.get("publication_revalidation_provenance")
        supersedes = {"path": ptr["path"], "sha256": ptr["sha256"]} if ptr else None

    gate_path = _safe_existing_file(root, gate_rel, "refresh Gate")
    old_gate_bytes = gate_path.read_bytes()
    if core.sha256_bytes(old_gate_bytes) != old_gate_sha:
        raise MechanicalRefreshError("live Gate differs from strict checkpoint/active effective row")

    inspected = surface_gate._inspect_gate_record(
        root, gate_path, expected_manuscript_path=manuscript_path
    )
    old_gate = inspected["payload"]
    if old_gate.get("derivation", {}).get("scope") != "WEEKLY_MAIN_BIB_STYLE":
        raise MechanicalRefreshError("refresh supports only WEEKLY_MAIN_BIB_STYLE Gate scope")
    if old_gate.get("issue_id") != state.get("issue_id") or old_gate.get("publication_profile") != "WEEKLY_MAGAZINE":
        raise MechanicalRefreshError("old Gate issue/profile mismatch vs State")
    receipt_ref = old_gate.get("derivation", {}).get("receipt")
    if not isinstance(receipt_ref, dict) or set(receipt_ref) != {"path", "sha256"}:
        raise MechanicalRefreshError("old Gate derivation receipt authority fields invalid")
    old_receipt_path = _safe_existing_file(root, receipt_ref["path"], "refresh old receipt")
    old_receipt_bytes = old_receipt_path.read_bytes()
    if core.sha256_bytes(old_receipt_bytes) != receipt_ref["sha256"]:
        raise MechanicalRefreshError("old receipt differs from bound Gate derivation reference")
    # Private shared receipt inspection only after raw hash anchoring; never proves replay alone.
    envelope = weekly._inspect_receipt_envelope(root, old_receipt_path)
    old_receipt = envelope["receipt"]
    # Full old receipt linkage to inspected old Gate before retention:
    # exact route/issue/profile/scope, unique roles, authored refs by NAME,
    # semantic input/review raw-byte hash and output-manuscript identities.
    if old_receipt.get("route") != weekly.ROUTE:
        raise MechanicalRefreshError("old receipt route mismatch")
    if old_receipt.get("issue_id") != state.get("issue_id") or old_receipt.get("issue_id") != old_gate.get("issue_id"):
        raise MechanicalRefreshError("old receipt/Gate/State issue identity mismatch")
    # Reviewed input must match live bytes and Gate semantic authority surface.
    reviewed_input_row = old_receipt.get("reviewed_reader_input", {})
    reviewed_input_path = _safe_existing_file(root, reviewed_input_row.get("path", ""), "reviewed reader input")
    if core.sha256_file(reviewed_input_path) != reviewed_input_row.get("sha256"):
        raise MechanicalRefreshError("old receipt reviewed input drift")
    sem_auth = old_gate.get("semantic_authority", {})
    if reviewed_input_row.get("sha256") != sem_auth.get("surface_sha256"):
        raise MechanicalRefreshError("old receipt reviewed input does not match Gate semantic_authority.surface_sha256")
    if reviewed_input_row.get("path") != sem_auth.get("surface_path"):
        raise MechanicalRefreshError("old receipt reviewed input path does not match Gate semantic_authority.surface_path")
    # Semantic review must match Gate review reference path and live file bytes.
    # Note: receipt semantic_review.sha256 is the raw file SHA, while Gate
    # semantic_authority.review_sha256 is the internal object digest
    # (sha256_object of the review JSON without its digest field). These are
    # different identities by design and must not be compared directly. Linkage
    # is via identical review file path plus each side's own validation
    # (receipt envelope file-hash check above, Gate inspection object-digest
    # check already performed). Raw file SHA vs object digest are distinct.
    sem_review_row = old_receipt.get("semantic_review", {})
    sem_review_path = _safe_existing_file(root, sem_review_row.get("path", ""), "semantic review")
    if core.sha256_file(sem_review_path) != sem_review_row.get("sha256"):
        raise MechanicalRefreshError("old receipt semantic review drift")
    if sem_review_row.get("path") != sem_auth.get("review_path"):
        raise MechanicalRefreshError("old receipt semantic review path does not match Gate semantic_authority.review_path")
    # Outputs must match manuscript supporting files (primary/bibliography/style).
    manuscript_doc = inspected.get("manuscript", {})
    primary_ref = manuscript_doc.get("primary_source", {})
    supp_by_role = {r.get("role"): r for r in manuscript_doc.get("supporting_files", []) if isinstance(r, dict)}
    for out_role, man_role in (("primary", None), ("bibliography", "BIBLIOGRAPHY"), ("style", "STYLE")):
        out_row = old_receipt.get("outputs", {}).get(out_role, {})
        out_path = _safe_existing_file(root, out_row.get("path", ""), f"refresh output {out_role}")
        if core.sha256_file(out_path) != out_row.get("sha256"):
            raise MechanicalRefreshError(f"old receipt output {out_role} drift")
        if out_role == "primary":
            if out_row.get("path") != primary_ref.get("path") or out_row.get("sha256") != primary_ref.get("sha256"):
                raise MechanicalRefreshError("old receipt primary output does not match manuscript primary_source")
        else:
            man_row = supp_by_role.get(man_role)
            if man_row is None or out_row.get("path") != man_row.get("path") or out_row.get("sha256") != man_row.get("sha256"):
                raise MechanicalRefreshError(f"old receipt {out_role} output does not match manuscript {man_role}")
    # Authored refs by NAME (unique roles), not index.
    authored_by_name = {r.get("name"): r for r in old_receipt.get("authored_refs", []) if isinstance(r, dict)}
    if set(authored_by_name) != {"publication-semantic-input", "drafting-authored-archive"}:
        raise MechanicalRefreshError("old receipt authored refs must carry exactly publication-semantic-input + drafting-authored-archive")
    # Receipt must live next to the reviewed surface and under Profile publication dir (canonical).
    # (Profile-derived publication_dir check is performed after context load; retained here as path sanity.)
    if old_receipt_path.parent != reviewed_input_path.parent:
        raise MechanicalRefreshError("old receipt must live next to the reviewed reader input")
    old_commit = old_receipt.get("current_tools", {}).get("repository_commit_sha")
    if not isinstance(old_commit, str) or len(old_commit) != 40:
        raise MechanicalRefreshError("old receipt generating commit invalid")
    weekly.verify_closure_at_commit(root, old_receipt.get("current_tools", {}).get("closure", []), old_commit)
    ancestor = _git(root, "merge-base", "--is-ancestor", old_commit, head)
    if ancestor.returncode != 0:
        raise MechanicalRefreshError("old receipt generating commit is not an ancestor of current HEAD")

    # Allowed-change gate: only weekly_derivation.py may differ old->HEAD.
    # NOTE: control paths include whole directories (implementation roots),
    # so a pathspec exclusion cannot carve out one file; classify the exact
    # changed names instead.
    controls = _control_paths(cfg)
    status = _git(root, "diff", "--name-status", "-z", old_commit, head, "--", *controls)
    if status.returncode != 0:
        raise MechanicalRefreshError("refresh control diff unreadable")
    tokens = [t for t in status.stdout.split("\x00") if t != ""]
    changed: list[tuple[str, str]] = []
    _i = 0
    while _i < len(tokens):
        code = tokens[_i]
        _i += 1
        if code.startswith("R"):
            _old = tokens[_i]
            _i += 1
            _new = tokens[_i]
            _i += 1
            changed.append((code, _old + " -> " + _new))
        else:
            _path = tokens[_i]
            _i += 1
            changed.append((code, _path))
    allowed = ALLOWED_CHANGED_PATH.as_posix()
    if any(code != "M" or path != allowed for code, path in changed):
        raise MechanicalRefreshError("unsupported control/criteria/schema change outside weekly_derivation.py")
    summary = _git(root, "diff", "--summary", old_commit, head, "--", *controls)
    if "mode change" in summary.stdout:
        raise MechanicalRefreshError("unsupported control mode change")
    current_closure = weekly.current_closure(root)
    old_closure = old_receipt.get("current_tools", {}).get("closure", [])
    # Current-source clean at actual HEAD with the existing helper BEFORE
    # no-op classification, so dirty/untracked controls report their precise
    # cause instead of being misread as "no change".
    try:
        weekly._verify_head_bytes(root, head, current_closure)
    except ValueError as exc:
        raise MechanicalRefreshError(str(exc)) from exc
    if not changed and old_closure == current_closure:
        raise MechanicalRefreshError("MECHANICAL_REFRESH_NO_OP: no supported control/closure change")
    current_contract = core.contract_identity(root, cfg, "WEEKLY", "WEEKLY_MAGAZINE")
    if old_receipt.get("current_tools", {}).get("contract") != current_contract:
        raise MechanicalRefreshError("refresh contract identity differs from current repository")

    # Same-edition equality: re-derive from accepted current inputs (authored by NAME).
    authored_by_name = {r.get("name"): r for r in old_receipt.get("authored_refs", [])}
    authored_rel = authored_by_name.get("publication-semantic-input", {}).get("path")
    if not authored_rel:
        raise MechanicalRefreshError("old receipt lacks publication-semantic-input authored ref")
    context = weekly.load_derivation(root, state_path, _safe_existing_file(root, authored_rel, "authored input"))
    if context["accepted_refs"] != old_receipt["accepted_refs"]:
        raise MechanicalRefreshError("accepted authority differs from bound receipt")
    reviewed_path = _safe_existing_file(root, old_receipt["reviewed_reader_input"]["path"], "reviewed reader input")
    reviewed = weekly.validate_reader_input(root, reviewed_path)
    if context["surface"] != reviewed:
        raise MechanicalRefreshError("independently recomputed reader input differs from reviewed bytes")
    # Manuscript / bundle / reviews / PDF unchanged (existing validators).
    reader.validate_manuscript_manifest(root, manuscript_path, issue_id=state["issue_id"])
    profile = context["profile"]
    # Canonical Profile-derived publication/survey roots (not basename-only).
    try:
        source_root = core.repo_local_path(root, profile["paths"]["source_root"], "Weekly source root")
        survey_root = core.repo_local_path(root, profile["paths"]["survey_root"], "Weekly survey root")
    except (KeyError, TypeError, ValueError) as exc:
        raise MechanicalRefreshError(f"refresh Profile paths invalid: {exc}") from exc
    _reject_symlink_ancestors(root, source_root, "Weekly source root")
    _reject_symlink_ancestors(root, survey_root, "Weekly survey root")
    if profile.get("research_profile") != "WEEKLY" or profile.get("publication_profile") != "WEEKLY_MAGAZINE":
        raise MechanicalRefreshError("refresh Profile requires WEEKLY / WEEKLY_MAGAZINE")
    bundle_rows = [k for k in ck_rows if k[0] == "quality-regression-bundle"]
    if not bundle_rows:
        raise MechanicalRefreshError("checkpoint lacks quality-regression-bundle row")
    bundle_doc = quality.validate_bundle(
        root, _safe_existing_file(root, bundle_rows[0][1], "quality bundle"), issue_id=state["issue_id"]
    )
    for _role, _kind in (("semantic-review", "SEMANTIC_EDITORIAL"), ("visual-review", "VISUAL")):
        rows = [k for k in ck_rows if k[0] == _role]
        if len(rows) != 1:
            raise MechanicalRefreshError(f"checkpoint must carry exactly one {_role} row")
        reader.validate_review_record(
            root, _safe_existing_file(root, rows[0][1], _role), issue_id=state["issue_id"], expected_kind=_kind
        )
    style_path_canonical = _safe_existing_file(root, weekly.STYLE_PATH.as_posix(), "Weekly style")
    style_source = style_path_canonical.read_text(encoding="utf-8")
    main_text = weekly.render_main(reviewed)
    bib_text = weekly.render_bibliography(reviewed)
    weekly.validate_generated_closure(main_text, style_source)
    expected_render = {
        "primary": main_text.encode("utf-8"),
        "bibliography": bib_text.encode("utf-8"),
        "style": style_path_canonical.read_bytes(),
    }
    for _name, _data in expected_render.items():
        row = old_receipt["outputs"][_name]
        disk = _safe_existing_file(root, row["path"], f"refresh output {_name}")
        if disk.read_bytes() != _data or core.sha256_bytes(_data) != row["sha256"]:
            raise MechanicalRefreshError(f"rendered {_name} differs from bound receipt")

    # Prospective receipt (pre-retention comparison).
    review_rel = old_receipt["semantic_review"]["path"]
    review_path = _safe_existing_file(root, review_rel, "semantic review")
    receipt_context = dict(context)
    receipt_context["authored_path"] = _safe_existing_file(
        root, authored_by_name["publication-semantic-input"]["path"], "authored input"
    )
    new_receipt = weekly.build_receipt(
        root,
        receipt_context,
        reviewed_path,
        review_path,
        _safe_existing_file(root, old_receipt["outputs"]["primary"]["path"], "primary output"),
        _safe_existing_file(root, old_receipt["outputs"]["bibliography"]["path"], "bibliography output"),
        _safe_existing_file(root, old_receipt["outputs"]["style"]["path"], "style output"),
    )
    for _key in ("accepted_refs", "authored_refs", "reviewed_reader_input", "semantic_review", "outputs"):
        if new_receipt[_key] != old_receipt[_key]:
            raise MechanicalRefreshError(f"prospective receipt {_key} differs from bound receipt")
    if new_receipt["current_tools"]["repository_commit_sha"] != head:
        raise MechanicalRefreshError("prospective receipt does not bind actual HEAD")
    if new_receipt["production_state_basis"]["lifecycle_state"] != "VALIDATED_DRAFT":
        raise MechanicalRefreshError("prospective receipt must record actual VALIDATED_DRAFT basis")
    if new_receipt["production_state_basis"]["historical_sha256"] != state_sha_p0:
        raise MechanicalRefreshError("prospective receipt State basis drift")
    new_receipt_bytes = core.json_bytes(new_receipt)

    # ---- P1 guard + retention (Profile-derived canonical paths) ----
    # Derive publication dir from Profile source_root, not basename-only.
    publication_dir = (source_root / "publication" / "v2").resolve()
    _reject_symlink_ancestors(root, publication_dir, "publication dir")
    _reject_symlink_ancestors(root, reviewed_path, "reviewed reader input")
    if reviewed_path.resolve().parent != publication_dir:
        raise MechanicalRefreshError(
            f"reviewed surface is not under canonical Profile publication/v2: {_rel(root, reviewed_path)}"
        )
    if old_receipt_path.resolve().parent != publication_dir or gate_path.resolve().parent != publication_dir:
        raise MechanicalRefreshError("receipt/Gate are not under canonical Profile publication/v2")
    # Canonical State already verified Profile-derived above.
    # Capture complete bound snapshot before any live write.
    bound_snapshot = _capture_bound_snapshot(
        root,
        state_path=state_path,
        state_sha=state_sha_p0,
        gate_path=gate_path,
        gate_sha=old_gate_sha,
        receipt_path=old_receipt_path,
        receipt_sha=receipt_ref["sha256"],
        old_receipt=old_receipt,
        checkpoint_path=checkpoint_path,
        checkpoint_sha=validation_ref["sha256"],
        checkpoint=checkpoint,
        manuscript_path=manuscript_path,
        head=head,
        cfg=cfg,
    )
    lock_path = publication_dir / LOCK_FILENAME
    _reject_symlink_ancestors(root, lock_path, "cooperative guard")
    if lock_path.is_symlink() or lock_path.exists():
        raise MechanicalRefreshError(f"cooperative refresh guard occupied: {lock_path}")
    expected_guard_bytes = core.json_bytes({"run_id": run_id, "head": head, "state_sha256": state_sha_p0})
    try:
        with open(lock_path, "xb") as fh:
            fh.write(expected_guard_bytes)
            fh.flush()
            try:
                os.fsync(fh.fileno())
            except OSError:
                pass
    except FileExistsError as exc:
        raise MechanicalRefreshError(f"cooperative refresh guard occupied: {lock_path}") from exc
    # Verify own guard bytes immediately (no blessing of raced bytes).
    try:
        if lock_path.read_bytes() != expected_guard_bytes:
            raise MechanicalRefreshError(f"cooperative guard bytes mismatch after create: {lock_path}")
    except OSError as exc:
        raise MechanicalRefreshError(f"cooperative guard readback failed: {exc}") from exc
    owned_lock = True
    committed = False
    api_attempted = False
    live_stage = 0
    pre_records: set[str] = set()
    try:
        _recheck_bound_snapshot(root, bound_snapshot, "after guard acquisition")
        retention_base = publication_dir / RETENTION_DIRNAME
        _reject_symlink_ancestors(root, retention_base, "retention base")
        # Reject unsafe retention parent before mkdir (never follow symlink out of root).
        if retention_base.is_symlink():
            raise MechanicalRefreshError(f"refresh retention base is a symlink: {retention_base}")
        # Check each parent component for symlink before creating.
        _reject_symlink_ancestors(root, retention_base / "probe", "retention base parent")
        retention_base.mkdir(parents=True, exist_ok=True)
        # Re-verify retention_base is still a real dir under root after mkdir.
        if retention_base.is_symlink() or not retention_base.is_dir():
            raise MechanicalRefreshError(f"refresh retention base unsafe after mkdir: {retention_base}")
        try:
            retention_base.resolve().relative_to(root.resolve())
        except ValueError as exc:
            raise MechanicalRefreshError(f"refresh retention base escapes repository: {retention_base}") from exc
        run_dir = retention_base / run_id
        _reject_symlink_ancestors(root, run_dir, "retention run dir")
        try:
            run_dir.mkdir(parents=False, exist_ok=False)
        except FileExistsError as exc:
            raise MechanicalRefreshError(f"refresh retention collision: {run_dir}") from exc
        for _name, _data in (
            ("receipt-superseded.json", old_receipt_bytes),
            ("gate-superseded.json", old_gate_bytes),
            ("production-state-superseded.json", state_path.read_bytes()),
        ):
            dest = run_dir / _name
            _exclusive_bytes(dest, _data, f"retention {_name}")
            if core.sha256_bytes(dest.read_bytes()) != core.sha256_bytes(_data):
                raise MechanicalRefreshError(f"retention copy mismatch: {_name}")
        retention_meta = {
            "run_id": run_id,
            "old_commit": old_commit,
            "new_head": head,
            "old_receipt": {
                "path": _rel(root, old_receipt_path),
                "sha256": receipt_ref["sha256"],
                "byte_count": len(old_receipt_bytes),
            },
            "old_gate": {"path": _rel(root, gate_path), "sha256": old_gate_sha, "byte_count": len(old_gate_bytes)},
            "state": {"path": _rel(root, state_path), "sha256": state_sha_p0},
            "validation": validation_ref,
            "supersedes": supersedes,
            "reason": reason.strip(),
            "executor": executor.strip(),
            "recorded_at": core.iso_utc(recorded_at),
        }
        _exclusive_bytes(run_dir / "retention.json", core.json_bytes(retention_meta), "retention metadata")

        # ---- P2 receipt installation (recheck complete snapshot + immediate target) ----
        _recheck_bound_snapshot(root, bound_snapshot, "before receipt installation")
        _reject_symlink_ancestors(root, old_receipt_path, "live receipt")
        new_receipt_sha = core.sha256_bytes(new_receipt_bytes)
        _atomic_replace(old_receipt_path, new_receipt_bytes, "receipt", run_id, expected_old_sha256=receipt_ref["sha256"])
        if core.sha256_file(old_receipt_path) != new_receipt_sha:
            raise MechanicalRefreshError(
                f"installed receipt hash mismatch at {old_receipt_path}; manual recovery required"
            )
        weekly.validate_receipt(root, old_receipt_path)
        live_stage = 1
        # Update bound snapshot for intentionally changed owned receipt (avoid false drift).
        receipt_rel = _rel(root, old_receipt_path)
        bound_snapshot["__RECEIPT__:" + receipt_rel] = new_receipt_sha
        if receipt_rel in bound_snapshot:
            bound_snapshot[receipt_rel] = new_receipt_sha

        # ---- P3 Gate computation/installation (after new receipt) ----
        _recheck_bound_snapshot(root, bound_snapshot, "before Gate computation")
        # Gate replace has immediate target old-hash check; never bless changed bytes.
        _reject_symlink_ancestors(root, gate_path, "live Gate")
        try:
            if core.sha256_file(gate_path) != old_gate_sha:
                raise MechanicalRefreshError(
                    f"live Gate drift before computation at {gate_path}; manual recovery required"
                )
        except OSError as exc:
            raise MechanicalRefreshError(f"live Gate read failed before computation: {exc}") from exc
        old_suppressions = old_gate.get("suppressions", [])
        new_report = surface_gate.evaluate_reader_surface_gate(
            root,
            manuscript_path,
            semantic_review_path=review_rel,
            suppressions=old_suppressions,
            output_path=None,
            state_path=state_path,
        )
        if new_report.get("status") != "PASSED":
            raise MechanicalRefreshError("renewed Gate did not PASS")
        if new_report.get("derivation", {}).get("scope") != "WEEKLY_MAIN_BIB_STYLE":
            raise MechanicalRefreshError("renewed Gate scope changed")
        # Complete old/new Gate equality except allowed evaluation metadata/digest/receipt.
        _compare_gate_reports(
            old_gate,
            new_report,
            old_receipt_rel=_rel(root, old_receipt_path),
            old_receipt_sha=receipt_ref["sha256"],
            new_receipt_sha=new_receipt_sha,
        )
        new_gate_bytes = core.json_bytes(new_report)
        new_gate_sha = core.sha256_bytes(new_gate_bytes)
        _recheck_bound_snapshot(root, bound_snapshot, "before Gate installation")
        _atomic_replace(gate_path, new_gate_bytes, "gate", run_id, expected_old_sha256=old_gate_sha)
        if core.sha256_file(gate_path) != new_gate_sha:
            raise MechanicalRefreshError(f"installed Gate hash mismatch at {gate_path}; manual recovery required")
        surface_gate.validate_reader_surface_gate(
            root, gate_path, expected_manuscript_path=manuscript_path, state_path=state_path
        )
        live_stage = 2
        # Update bound snapshot for intentionally changed owned Gate.
        gate_rel = _rel(root, gate_path)
        bound_snapshot["__GATE__:" + gate_rel] = new_gate_sha
        if gate_rel in bound_snapshot:
            bound_snapshot[gate_rel] = new_gate_sha

        # ---- P4 revalidation/commit (explicit commit point) ----
        _recheck_bound_snapshot(root, bound_snapshot, "before revalidation")
        basis = agent.built_checked_pending_publication_basis(root, cfg, state_path)
        if len(basis.replacements) != 1 or basis.replacements[0][0] != "reader-surface-gate":
            raise MechanicalRefreshError("pending basis is not exactly the renewed Gate row")
        # Capture pre-API record inventory for post-failure disposition inspection.
        try:
            pub_dir = publication_dir
            pre_records = {
                p.name for p in pub_dir.iterdir()
                if p.name.startswith("publication-surface-revalidation-r") and p.is_file()
            }
        except OSError as exc:
            raise MechanicalRefreshError(f"pre-revalidation record inventory failed: {exc}") from exc
        pre_state_bytes = state_path.read_bytes()
        if core.sha256_bytes(pre_state_bytes) != state_sha_p0:
            raise MechanicalRefreshError("State drift before revalidation commit; manual recovery required")
        api_attempted = True
        record_path = agent.revalidate_publication_surface(
            root, cfg, state_path, REASON_CLASS, reason, executor, recorded_at, head
        )
        # Successful API return after its strict post-State validation is the commit point.
        # Post-commit reporting/readback must never undo committed authority.
        committed = True
        try:
            final_state = core.load_json(state_path)
        except (OSError, ValueError) as exc:
            raise MechanicalRefreshError(
                f"post-commit State readback failed at {state_path}: {exc}; "
                f"authority is committed at {record_path}, manual reconciliation required"
            ) from exc
        final_active, final_errors = agent.resolve_active_publication_revalidation(root, cfg, final_state)
        if final_errors or final_active is None:
            raise MechanicalRefreshError(
                "post-commit active readback invalid (" + "; ".join(final_errors) + "); "
                f"authority is committed at {_rel(root, record_path)}, no rollback performed"
            )
    except Exception as exc:
        # Explicit commit flag/point: post-commit reporting errors never undo committed authority.
        # Guard ownership: release only an unchanged operation-owned guard; preserve
        # lock+retention+unknown bytes on conflict for manual recovery.
        if committed:
            # Authority is committed at record_path; never roll back live receipt/Gate/State.
            # Release own guard (commit complete) only if still owned; otherwise retain.
            try:
                _release_guard_if_owned(lock_path, expected_guard_bytes, "cooperative guard (post-commit)")
            except MechanicalRefreshError as guard_exc:
                raise MechanicalRefreshError(
                    f"refresh post-commit reporting failed ({exc}); committed at {_rel(root, record_path) if 'record_path' in locals() else 'unknown'}; "
                    f"guard retained for manual reconciliation: {guard_exc}"
                ) from exc
            if isinstance(exc, MechanicalRefreshError):
                raise
            raise MechanicalRefreshError(f"refresh post-commit reporting failed: {exc}") from exc
        # Pre-commit: inspect actual State/record disposition after API error; do not assume rollback.
        if api_attempted:
            try:
                cur_state_bytes = state_path.read_bytes()
            except OSError:
                cur_state_bytes = None
            try:
                post_records = {
                    p.name for p in publication_dir.iterdir()
                    if p.name.startswith("publication-surface-revalidation-r") and p.is_file()
                }
            except OSError:
                post_records = None
            # Leftover tampered/orphan record or changed State => manual guard retained.
            if cur_state_bytes != pre_state_bytes or (post_records is not None and post_records != pre_records):
                raise MechanicalRefreshError(
                    f"refresh revalidation failed with State/record disposition changed "
                    f"(State equal={cur_state_bytes == pre_state_bytes}, "
                    f"records before={sorted(pre_records)}, after={sorted(post_records) if post_records is not None else 'unreadable'}); "
                    f"live bytes + retention + guard preserved for manual recovery: {exc}; "
                    f"paths State={_rel(root, state_path)} Gate={_rel(root, gate_path)} Receipt={_rel(root, old_receipt_path)}"
                ) from exc
            # Disposition clean (State original, no new record): fall through to guarded restoration below.
        # Guarded restoration for caught pre-commit failures only, with ownership checks.
        # Safe pre-live-write aborts (live_stage==0, no owned live changes) may release own guard.
        # Failed restoration with unknown bytes retains guard.
        try:
            # Verify HEAD/State still match captured basis (never bless changed bytes).
            try:
                cur_head = core.repository_commit_sha(root)
            except ValueError as head_exc:
                raise MechanicalRefreshError(
                    f"refresh failed ({exc}); HEAD unreadable, live bytes + retention + guard preserved for manual recovery"
                ) from exc
            if cur_head != head:
                raise MechanicalRefreshError(
                    f"refresh failed ({exc}) with HEAD drift (expected {head[:16]}.., found {cur_head[:16]}..); "
                    "live bytes + retention + guard preserved for manual recovery"
                ) from exc
            try:
                cur_state = state_path.read_bytes()
            except OSError as state_exc:
                raise MechanicalRefreshError(
                    f"refresh failed ({exc}); State unreadable at {_rel(root, state_path)}, guard retained"
                ) from exc
            if core.sha256_bytes(cur_state) != state_sha_p0:
                raise MechanicalRefreshError(
                    f"refresh failed ({exc}) with State drift at {_rel(root, state_path)} "
                    f"(expected {state_sha_p0[:16]}.., found {core.sha256_bytes(cur_state)[:16]}..); "
                    "live bytes + retention + guard preserved"
                ) from exc
            # Live receipt/Gate must be exactly old or new owned bytes; unknown => retain.
            try:
                live_receipt = old_receipt_path.read_bytes() if old_receipt_path.is_file() else None
            except OSError:
                live_receipt = None
            try:
                live_gate = gate_path.read_bytes() if gate_path.is_file() else None
            except OSError:
                live_gate = None
            new_receipt_sha_local = core.sha256_bytes(new_receipt_bytes)
            new_gate_known = new_gate_bytes if "new_gate_bytes" in locals() else None
            receipt_known = live_receipt in (old_receipt_bytes, new_receipt_bytes)
            gate_known = live_gate in (old_gate_bytes, new_gate_known)
            if not receipt_known or not gate_known:
                raise MechanicalRefreshError(
                    f"refresh failed ({exc}) with unknown live bytes "
                    f"(receipt known={receipt_known}, gate known={gate_known}); "
                    f"live Receipt={_rel(root, old_receipt_path)} Gate={_rel(root, gate_path)} + retention + guard preserved"
                ) from exc
            # Verify all other bound dependencies (excluding intentionally changed receipt/gate) still match.
            # Build a recheck snapshot that excludes live receipt/gate/state/head (already checked above).
            try:
                _recheck_bound_snapshot(root, {k: v for k, v in bound_snapshot.items() if not (k.startswith("__RECEIPT__:") or k.startswith("__GATE__:") or k.startswith("__STATE__:") or k == "__HEAD__")}, "pre-restore dependencies")
            except MechanicalRefreshError as dep_exc:
                raise MechanicalRefreshError(
                    f"refresh failed ({exc}) with dependency drift before restore: {dep_exc}; guard retained"
                ) from exc
            # Restore only operation-owned files whose current bytes equal known written bytes.
            if live_receipt != old_receipt_bytes:
                # Current must be exactly new owned bytes before restoring.
                if live_receipt != new_receipt_bytes:
                    raise MechanicalRefreshError("restoration refused unknown receipt bytes") from exc
                _atomic_replace(old_receipt_path, old_receipt_bytes, "receipt-restore", run_id, expected_old_sha256=new_receipt_sha_local)
                if core.sha256_file(old_receipt_path) != receipt_ref["sha256"]:
                    raise MechanicalRefreshError(
                        f"restored receipt mismatch at {_rel(root, old_receipt_path)}; manual recovery required"
                    ) from exc
            if live_gate != old_gate_bytes:
                if new_gate_known is None or live_gate != new_gate_known:
                    raise MechanicalRefreshError("restoration refused unknown Gate bytes") from exc
                _atomic_replace(gate_path, old_gate_bytes, "gate-restore", run_id, expected_old_sha256=core.sha256_bytes(new_gate_known))
                if core.sha256_file(gate_path) != old_gate_sha:
                    raise MechanicalRefreshError(
                        f"restored Gate mismatch at {_rel(root, gate_path)}; manual recovery required"
                    ) from exc
            # Verified safe restore complete: release only own guard.
            _release_guard_if_owned(lock_path, expected_guard_bytes, "cooperative guard (restored)")
        except MechanicalRefreshError as restore_exc:
            # Restoration unsafe or guard changed: preserve live + retention + guard.
            # If restore_exc already chains original exc, re-raise it; otherwise chain.
            if restore_exc.__cause__ is exc or restore_exc.__cause__ is not None:
                raise
            raise restore_exc from exc
        if isinstance(exc, MechanicalRefreshError):
            raise
        raise MechanicalRefreshError(f"refresh failed: {exc}") from exc
    # Success path: commit or pre-live abort both release only own guard after verification.
    if committed:
        _release_guard_if_owned(lock_path, expected_guard_bytes, "cooperative guard (committed)")
    else:
        # Success without commit should not happen (all successes commit), but handle safely.
        _release_guard_if_owned(lock_path, expected_guard_bytes, "cooperative guard (success)")
    return {
        "state": _rel(root, state_path),
        "revalidation_record": _rel(root, record_path),
        "receipt": _rel(root, old_receipt_path),
        "gate": _rel(root, gate_path),
        "retention": _rel(root, run_dir),
        "supersedes": supersedes,
    }
