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
import secrets
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


def _check_raw_rel_ancestors(root_resolved: Path, rel: str, label: str) -> None:
    """Reject lexical root/path/parent symlinks BEFORE any .resolve().

    Walks ``root_resolved / rel`` parent components with lstat only (no
    resolution), so inside-root aliases are caught instead of being resolved
    away. Must run before ``core.repo_local_path`` / ``Path.resolve``.
    """
    if not isinstance(rel, str) or not rel or "\\" in rel:
        raise MechanicalRefreshError(f"refresh {label} must be a repository-relative path without backslash: {rel!r}")
    raw = Path(rel)
    if raw.is_absolute() or ".." in raw.parts or "." in raw.parts:
        raise MechanicalRefreshError(f"refresh {label} must be repository-local without traversal: {rel}")
    current = root_resolved
    for part in raw.parent.parts:
        if part in ("..", ".", ""):
            raise MechanicalRefreshError(f"refresh {label} has unsafe path component: {part}")
        current = current / part
        try:
            if current.is_symlink():
                raise MechanicalRefreshError(f"refresh {label} has symlinked ancestor component: {current}")
        except OSError as exc:
            raise MechanicalRefreshError(f"refresh {label} ancestor check failed: {current}: {exc}") from exc
    # The leaf itself must not be a symlink either (lstat, no resolve).
    try:
        if (root_resolved / raw).is_symlink():
            raise MechanicalRefreshError(f"refresh {label} is a symlink/refusal: {rel}")
    except OSError as exc:
        raise MechanicalRefreshError(f"refresh {label} symlink check failed: {rel}: {exc}") from exc


def _check_raw_abs_ancestors(root_resolved: Path, abs_path: Path, label: str) -> None:
    """Reject symlinks on a raw absolute path BEFORE any .resolve().

    ``abs_path`` must be absolute and lexical (unresolved, e.g. a user-supplied
    ``--state`` argument or a ``root / raw`` join). Walks from the resolved
    root to the path parent with lstat only.
    """
    if not abs_path.is_absolute():
        raise MechanicalRefreshError(f"refresh {label} must be absolute for raw check: {abs_path}")
    try:
        rel_parts = abs_path.parent.relative_to(root_resolved).parts
    except ValueError as exc:
        raise MechanicalRefreshError(f"refresh {label} escapes repository root: {abs_path}") from exc
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
        if abs_path.is_symlink():
            raise MechanicalRefreshError(f"refresh {label} is a symlink/refusal: {abs_path}")
    except OSError as exc:
        raise MechanicalRefreshError(f"refresh {label} symlink check failed: {abs_path}: {exc}") from exc


def _safe_existing_file(root: Path, rel: str, label: str) -> Path:
    """Resolve a repository-relative file with lexical checks BEFORE resolve.

    Order is load-bearing: raw lexical validation + lstat ancestor walk first
    (catches inside-root aliases), then ``core.repo_local_path`` resolution +
    containment, then final symlink/file refusal. Used for all
    retention/live/config/State/publication/manuscript/reader-input/receipt/Gate
    targets derived from Profile authority.
    """
    root_resolved = root.resolve()
    _check_raw_rel_ancestors(root_resolved, rel, label)
    try:
        resolved = core.repo_local_path(root, rel, label)
    except (TypeError, ValueError) as exc:
        raise MechanicalRefreshError(f"refresh {label} invalid: {exc}") from exc
    try:
        resolved.resolve().relative_to(root_resolved)
    except ValueError as exc:
        raise MechanicalRefreshError(f"refresh {label} escapes repository root: {rel}") from exc
    _reject_symlink_ancestors(root, resolved, label)
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
    try:
        with open(tmp, "xb") as fh:
            fh.write(data)
            fh.flush()
            try:
                os.fsync(fh.fileno())
            except OSError:
                pass
            try:
                _tmp_fst = os.fstat(fh.fileno())
                tmp_id: tuple[int, int] | None = (_tmp_fst.st_dev, _tmp_fst.st_ino)
            except OSError as exc:
                raise MechanicalRefreshError(f"refresh {label} temp identity capture failed: {exc}") from exc
    except FileExistsError as exc:
        raise MechanicalRefreshError(f"refresh {label} temp collision: {tmp}") from exc

    def _drop_own_temp() -> None:
        """Remove the temp file only if it is still our exclusive creation.

        Requires the SAME fd-captured file identity AND bytes equal to the
        expected temporary serialization. Changed content on the same inode,
        swapped inodes (even with identical bytes), aliases, or unreadability
        all retain the temp: unknown bytes are never unlinked as foreign.
        """
        try:
            if tmp.is_symlink():
                return
            cur = os.stat(tmp)
            if tmp_id is not None and (cur.st_dev, cur.st_ino) != tmp_id:
                return
            try:
                if tmp.read_bytes() != data:
                    return
            except OSError:
                return
            tmp.unlink(missing_ok=True)
        except OSError:
            pass

    try:
        if tmp.read_bytes() != data:
            _drop_own_temp()
            raise MechanicalRefreshError(f"refresh {label} temp bytes mismatch; live bytes untouched")
    except OSError as exc:
        if isinstance(exc, MechanicalRefreshError):
            raise
        raise MechanicalRefreshError(f"refresh {label} temp readback failed: {tmp}: {exc}") from exc
    # Immediate target recheck: destination must still equal expected old bytes.
    if expected_old_sha256 is not None:
        try:
            if core.sha256_file(path) != expected_old_sha256:
                _drop_own_temp()
                raise MechanicalRefreshError(
                    f"refresh {label} destination changed before replace at {path}; "
                    "live bytes + retention + guard preserved for manual recovery"
                )
        except OSError as exc:
            if isinstance(exc, MechanicalRefreshError):
                raise
            _drop_own_temp()
            raise MechanicalRefreshError(f"refresh {label} pre-replace recheck failed: {exc}") from exc
    # Re-verify the temp is still our known identity+bytes immediately before
    # publishing: a temp modified after verification must never be published.
    try:
        if tmp.is_symlink():
            raise MechanicalRefreshError(f"refresh {label} temp is a symlink before replace; manual recovery required")
        _tmp_cur = os.stat(tmp)
        if tmp_id is not None and (_tmp_cur.st_dev, _tmp_cur.st_ino) != tmp_id:
            raise MechanicalRefreshError(f"refresh {label} temp identity changed before replace; manual recovery required")
        if tmp.read_bytes() != data:
            raise MechanicalRefreshError(f"refresh {label} temp bytes changed before replace; manual recovery required")
    except OSError as exc:
        if isinstance(exc, MechanicalRefreshError):
            raise
        raise MechanicalRefreshError(f"refresh {label} temp pre-publish recheck failed: {exc}") from exc
    try:
        os.replace(tmp, path)
    except OSError as exc:
        raise MechanicalRefreshError(f"refresh {label} replace failed; live bytes preserved for manual recovery: {exc}") from exc
    try:
        if core.sha256_file(path) != core.sha256_bytes(data):
            raise MechanicalRefreshError(f"refresh {label} post-replace mismatch at {path}; manual recovery required")
    except OSError as exc:
        if isinstance(exc, MechanicalRefreshError):
            raise
        raise MechanicalRefreshError(f"refresh {label} post-replace readback failed: {exc}") from exc


def _guard_id_of(lock_path: Path) -> tuple[int, int]:
    """Return (st_dev, st_ino) for an existing guard path (follows symlinks).

    Callers check ``is_symlink`` first; this helper stats the target for
    identity comparison against the fd-captured creation identity.
    """
    st = os.stat(lock_path)
    return (st.st_dev, st.st_ino)


def _verify_guard_owned(
    lock_path: Path, expected_bytes: bytes, expected_id: tuple[int, int] | None, label: str
) -> None:
    """Verify the guard is still this operation's exclusive file before mutating.

    Checks symlink absence, regular-file presence, exact expected bytes (which
    carry a per-operation unique nonce, so even identical timestamp/head/state
    tuples cannot collide), and file identity (dev/ino captured from the
    exclusive-create fd). A replaced guard with identical contents still has a
    different identity and is refused. On failure the caller must STOP
    immediately: preserve live/foreign bytes, perform no restore through a
    foreign guard, and never delete the foreign guard.
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
            f"refresh {label} guard changed (expected nonce hash {core.sha256_bytes(expected_bytes)[:16]}.., "
            f"found {core.sha256_bytes(current)[:16]}..); foreign guard preserved, no deletion performed"
        )
    if expected_id is not None:
        try:
            actual_id = _guard_id_of(lock_path)
        except OSError as exc:
            raise MechanicalRefreshError(f"refresh {label} guard stat failed at {lock_path}: {exc}") from exc
        if actual_id != expected_id:
            raise MechanicalRefreshError(
                f"refresh {label} guard replaced (same bytes, different file identity); "
                "foreign guard preserved, no deletion performed"
            )


def _release_guard_if_owned(
    lock_path: Path, expected_bytes: bytes, expected_id: tuple[int, int] | None, label: str
) -> None:
    """Release only an unchanged operation-owned guard (bytes + identity).

    Refuses to delete a foreign/replaced/removed guard; preserves lock +
    retention + unknown bytes on conflict for manual recovery. Never steals a
    stale lock automatically.
    """
    _verify_guard_owned(lock_path, expected_bytes, expected_id, label)
    try:
        lock_path.unlink()
    except OSError as exc:
        raise MechanicalRefreshError(f"refresh {label} guard release failed at {lock_path}: {exc}") from exc


def _add_expected(snap: dict[str, str], rel: str, sha: str, context: str) -> None:
    """Pin one expected file hash, rejecting conflicting expectations.

    The same path pinned twice with different hashes means two authorities
    disagree (e.g. a stale checkpoint row vs the current-effective row, or a
    freshly re-hashed drifted file vs its recorded authority). Overwriting
    would bless intervening drift, so conflicts fail closed instead.
    """
    if not isinstance(rel, str) or not rel or not isinstance(sha, str) or not sha:
        raise MechanicalRefreshError(f"refresh snapshot invalid expectation for {context}: {rel!r}")
    if rel in snap:
        if snap[rel] != sha:
            raise MechanicalRefreshError(
                f"refresh snapshot conflicting expectation at {rel} ({context}): "
                f"recorded {snap[rel][:16]}.. vs {sha[:16]}..; refusing to bless drift"
            )
        return
    snap[rel] = sha


def _expect_file(snap: dict[str, str], root: Path, rel: str, sha: str, label: str) -> None:
    """Pin an authoritative (path, sha256) ref and verify live bytes match NOW.

    Nonexistent required dependencies fail here (before any guard/retention/
    live write) instead of a sentinel that would accept absence. Live drift
    already present at capture time is refused without blessing new hashes.
    """
    if not isinstance(rel, str) or not rel or not isinstance(sha, str) or len(sha) != 64:
        raise MechanicalRefreshError(f"refresh snapshot invalid authority ref for {label}: {rel!r}")
    live = _safe_existing_file(root, rel, f"snapshot {label}")
    try:
        actual = core.sha256_file(live)
    except OSError as exc:
        raise MechanicalRefreshError(f"refresh snapshot unreadable at {rel} ({label}): {exc}") from exc
    if actual != sha:
        raise MechanicalRefreshError(
            f"refresh snapshot drift at {rel} ({label}): expected {sha[:16]}.., found {actual[:16]}..; "
            "refusing before any guard/retention/live write"
        )
    _add_expected(snap, _rel(root, live), sha, label)


def _control_tracked_files(root: Path, controls: list[str]) -> list[str]:
    """List tracked files under control roots (null-separated, no shell)."""
    proc = _git(root, "ls-files", "-z", "--", *controls)
    if proc.returncode != 0:
        raise MechanicalRefreshError(f"refresh control file inventory unreadable: {proc.stderr.strip()}")
    return sorted(p for p in proc.stdout.split("\x00") if p != "")


def _control_untracked_files(root: Path, controls: list[str]) -> list[str]:
    """List untracked files under control roots (pycache/pyc ignored)."""
    proc = _git(root, "ls-files", "--others", "--exclude-standard", "-z", "--", *controls)
    if proc.returncode != 0:
        raise MechanicalRefreshError(f"refresh untracked control inventory unreadable: {proc.stderr.strip()}")
    return sorted(
        p for p in proc.stdout.split("\x00")
        if p != "" and "__pycache__" not in Path(p).parts and not p.endswith(".pyc")
    )


def _capture_bound_snapshot(
    root: Path,
    *,
    state_path: Path,
    state: dict[str, Any],
    state_sha: str,
    gate_path: Path,
    gate_sha: str,
    old_gate: dict[str, Any],
    receipt_path: Path,
    receipt_sha: str,
    old_receipt: dict[str, Any],
    checkpoint_path: Path,
    checkpoint_sha: str,
    checkpoint: dict[str, Any],
    manuscript_path: Path,
    bundle_doc: dict[str, Any],
    active: dict[str, Any] | None,
    head: str,
    cfg: dict[str, Any],
) -> dict[str, str]:
    """Snapshot all VALIDATED source dependencies vs authoritative recorded refs.

    Covers, from recorded authority (never freshly re-hashed drift):
    receipt input refs (accepted/authored), reviewed input, semantic review,
    outputs; old Gate scanned surfaces; bundle deterministic-result refs + pdf;
    current validated manuscript/profile/approval refs; every State-bound
    checkpoint file with its artifacts + deterministic review results (using
    current-effective validation rows for ALL roles, so a healthy prior
    metadata revalidation with changed manuscript/reviews vs the original
    checkpoint does not false-fail); the full predecessor record chain via
    supersedes; current control/contract tracked files + membership (dirty/
    untracked rechecked at every boundary); profile/HEAD.
    """
    snap: dict[str, str] = {}
    snap["__HEAD__"] = head
    snap["__STATE__:" + _rel(root, state_path)] = state_sha
    snap["__GATE__:" + _rel(root, gate_path)] = gate_sha
    snap["__RECEIPT__:" + _rel(root, receipt_path)] = receipt_sha
    snap["__CHECKPOINT__:" + _rel(root, checkpoint_path)] = checkpoint_sha
    # Current-effective validation rows for ALL roles (repeat-safe): a healthy
    # prior revalidation may have renewed manuscript/reviews/bundle rows vs the
    # original checkpoint; expecting the stale original sha would false-fail.
    effective: dict[tuple[str, str], str] = {}
    if active is not None:
        for row in active.get("superseded_artifacts", []):
            if isinstance(row, dict) and row.get("name") and row.get("path") and row.get("new_sha256"):
                effective[(row["name"], row["path"])] = row["new_sha256"]
        for row in active.get("preserved_artifacts", []):
            if isinstance(row, dict) and row.get("name") and row.get("path") and row.get("sha256"):
                effective.setdefault((row["name"], row["path"]), row["sha256"])
    # Validation checkpoint artifacts with effective rows.
    for row in checkpoint.get("artifacts", []):
        if not isinstance(row, dict) or not row.get("path") or not row.get("sha256"):
            raise MechanicalRefreshError(f"refresh snapshot malformed checkpoint artifact: {row!r}")
        expected = effective.get((row.get("name"), row.get("path")), row["sha256"])
        _expect_file(snap, root, row["path"], expected, f"checkpoint {row.get('name')}")
    # Receipt-bound inputs/outputs.
    for group_key in ("accepted_refs", "authored_refs"):
        for row in old_receipt.get(group_key, []):
            if not isinstance(row, dict) or not row.get("path") or not row.get("sha256"):
                raise MechanicalRefreshError(f"refresh snapshot malformed receipt {group_key} row: {row!r}")
            _expect_file(snap, root, row["path"], row["sha256"], f"receipt {row.get('name')}")
    for single_key in ("reviewed_reader_input", "semantic_review"):
        row = old_receipt.get(single_key, {})
        if not isinstance(row, dict) or not row.get("path") or not row.get("sha256"):
            raise MechanicalRefreshError(f"refresh snapshot malformed receipt {single_key}: {row!r}")
        _expect_file(snap, root, row["path"], row["sha256"], f"receipt {single_key}")
    for out_name, row in (old_receipt.get("outputs", {}) or {}).items():
        if not isinstance(row, dict) or not row.get("path") or not row.get("sha256"):
            raise MechanicalRefreshError(f"refresh snapshot malformed receipt output {out_name}: {row!r}")
        _expect_file(snap, root, row["path"], row["sha256"], f"receipt output {out_name}")
    # Old Gate scanned surfaces (every scanned file, not just manuscript).
    for surface in old_gate.get("scanned_surfaces", []):
        if not isinstance(surface, dict) or not surface.get("path") or not surface.get("sha256"):
            raise MechanicalRefreshError(f"refresh snapshot malformed Gate scanned surface: {surface!r}")
        _expect_file(snap, root, surface["path"], surface["sha256"], "gate scanned surface")
    # Bundle deterministic-result refs + pdf (REPOSITORY_FILE only).
    for check in bundle_doc.get("checks", []):
        result = (check or {}).get("result", {})
        if isinstance(result, dict) and result.get("path") and result.get("sha256"):
            _expect_file(snap, root, result["path"], result["sha256"], f"bundle result {check.get('check_id')}")
    pdf_ref = bundle_doc.get("pdf", {})
    if isinstance(pdf_ref, dict) and pdf_ref.get("storage", "REPOSITORY_FILE") == "REPOSITORY_FILE":
        if not pdf_ref.get("path") or not pdf_ref.get("sha256"):
            raise MechanicalRefreshError(f"refresh snapshot malformed bundle pdf ref: {pdf_ref!r}")
        _expect_file(snap, root, pdf_ref["path"], pdf_ref["sha256"], "bundle pdf")
    # Current validated manuscript/profile/approval refs.
    manuscript_rel = _rel(root, manuscript_path)
    _expect_file(snap, root, manuscript_rel, core.sha256_file(manuscript_path), "manuscript")
    profile_ref = state.get("profile", {})
    if not isinstance(profile_ref, dict) or not profile_ref.get("path") or not profile_ref.get("sha256"):
        raise MechanicalRefreshError("refresh snapshot malformed State profile ref")
    _expect_file(snap, root, profile_ref["path"], profile_ref["sha256"], "profile")
    arch_ref = (state.get("human_gate_provenance", {}) or {}).get("architecture_review")
    if not isinstance(arch_ref, dict) or not arch_ref.get("path") or not arch_ref.get("sha256"):
        raise MechanicalRefreshError("refresh snapshot malformed architecture approval ref")
    _expect_file(snap, root, arch_ref["path"], arch_ref["sha256"], "architecture approval")
    # Every State-bound checkpoint: file + artifacts + deterministic results.
    # The validation checkpoint itself is covered above with effective rows.
    validation_path = validation_ref_path(state)
    for cp_name, cp_ref in (state.get("checkpoint_provenance", {}) or {}).items():
        if cp_ref is None:
            continue
        if not isinstance(cp_ref, dict) or not cp_ref.get("path") or not cp_ref.get("sha256"):
            raise MechanicalRefreshError(f"refresh snapshot malformed checkpoint provenance: {cp_name}")
        _expect_file(snap, root, cp_ref["path"], cp_ref["sha256"], f"checkpoint {cp_name}")
        try:
            record = core.load_json(root / cp_ref["path"])
        except (OSError, ValueError) as exc:
            raise MechanicalRefreshError(f"refresh snapshot unreadable checkpoint {cp_name}: {exc}") from exc
        if cp_ref["path"] == validation_path:
            # Validation artifacts use current-effective rows (pinned above);
            # its deterministic review results (e.g. the CORE_STAGE_CONTRACT
            # report) are still pinned here from recorded refs.
            pass
        else:
            for art in record.get("artifacts", []):
                if isinstance(art, dict) and art.get("path") and art.get("sha256"):
                    _expect_file(snap, root, art["path"], art["sha256"], f"checkpoint {cp_name} artifact {art.get('name')}")
        for review in record.get("reviews", []):
            if not isinstance(review, dict):
                raise MechanicalRefreshError(f"refresh snapshot malformed checkpoint review in {cp_name}")
            result = review.get("result", {})
            if not isinstance(result, dict) or not result.get("path") or not result.get("sha256"):
                raise MechanicalRefreshError(
                    f"refresh snapshot malformed deterministic result in {cp_name} review {review.get('check_id')}: "
                    "strict checkpoint schema requires {path, sha256}"
                )
            _expect_file(snap, root, result["path"], result["sha256"], f"checkpoint {cp_name} result {review.get('check_id')}")
    # Full predecessor record chain via supersedes (not just the State pointer).
    # Bounded by the existing agent REVALIDATION_CHAIN_LIMIT with the same
    # semantics as _check_revalidation_chain (at most that many links followed).
    from scripts import survey_agent_control_v2 as _agent_for_limit

    ptr: dict[str, Any] | None = state.get("publication_revalidation_provenance")
    _chain_depth = 0
    while isinstance(ptr, dict) and ptr.get("path") and ptr.get("sha256"):
        _chain_depth += 1
        if _chain_depth > _agent_for_limit.REVALIDATION_CHAIN_LIMIT:
            raise MechanicalRefreshError("refresh snapshot predecessor chain exceeds limit 32")
        _expect_file(snap, root, ptr["path"], ptr["sha256"], "predecessor record")
        try:
            predecessor = core.load_json(root / ptr["path"])
        except (OSError, ValueError) as exc:
            raise MechanicalRefreshError(f"refresh snapshot unreadable predecessor record: {exc}") from exc
        ptr = predecessor.get("supersedes")
    # Current control/contract tracked files + membership (dirty/untracked are
    # rechecked at every boundary in _recheck_bound_snapshot).
    controls = _control_paths(cfg)
    tracked = _control_tracked_files(root, controls)
    if not tracked:
        raise MechanicalRefreshError("refresh snapshot empty control file inventory")
    snap["__CONTROL_MEMBERS__"] = json.dumps(tracked)
    for rel in tracked:
        live = _safe_existing_file(root, rel, f"snapshot control {rel}")
        try:
            actual = core.sha256_file(live)
        except OSError as exc:
            raise MechanicalRefreshError(f"refresh snapshot unreadable control file {rel}: {exc}") from exc
        _add_expected(snap, _rel(root, live), actual, f"control {rel}")
    if _control_untracked_files(root, controls):
        raise MechanicalRefreshError(
            f"refresh snapshot untracked control files present: {_control_untracked_files(root, controls)[:5]}"
        )
    return snap


def validation_ref_path(state: dict[str, Any]) -> str:
    """Return the validation checkpoint path recorded in State."""
    ref = (state.get("checkpoint_provenance", {}) or {}).get("validation", {})
    return ref.get("path", "") if isinstance(ref, dict) else ""


def _recheck_bound_snapshot(root: Path, snap: dict[str, str], controls: list[str], label: str) -> None:
    """Recheck complete bound snapshot; reject detected drift without normalizing.

    Verifies HEAD, every pinned file hash, control membership + untracked
    absence, and a clean ``git diff HEAD`` for control roots (catches staged
    index changes that worktree hashing alone cannot see). Never re-hashes
    drifted bytes into new expectations.
    """
    expected_head = snap.get("__HEAD__")
    if expected_head is not None:
        actual_head = core.repository_commit_sha(root)
        if actual_head != expected_head:
            raise MechanicalRefreshError(
                f"refresh {label}: HEAD drift (expected {expected_head[:16]}.., found {actual_head[:16]}..); "
                "live bytes + retention + guard preserved for manual recovery"
            )
    for key, expected_sha in snap.items():
        if key in ("__HEAD__", "__CONTROL_MEMBERS__"):
            continue
        if key.startswith("__STATE__:") or key.startswith("__GATE__:") or key.startswith("__RECEIPT__:") or key.startswith("__CHECKPOINT__:"):
            rel = key.split(":", 1)[1]
        else:
            rel = key
        try:
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
    # Control membership + untracked + staged-index checks run every boundary.
    # Membership is JSON-list encoded (filenames may contain newlines).
    expected_members = snap.get("__CONTROL_MEMBERS__")
    if expected_members is not None:
        try:
            expected_list = json.loads(expected_members)
        except ValueError as exc:
            raise MechanicalRefreshError(f"refresh {label}: control membership encoding invalid: {exc}") from exc
        current_members = _control_tracked_files(root, controls)
        if current_members != expected_list:
            raise MechanicalRefreshError(
                f"refresh {label}: control file membership changed; manual recovery required"
            )
        untracked = _control_untracked_files(root, controls)
        if untracked:
            raise MechanicalRefreshError(
                f"refresh {label}: untracked control files appeared ({len(untracked)}); manual recovery required"
            )
        dirty = _git(root, "diff", "--quiet", "HEAD", "--", *controls)
        if dirty.returncode != 0:
            raise MechanicalRefreshError(
                f"refresh {label}: control files differ from committed HEAD; manual recovery required"
            )
        staged = _git(root, "diff", "--cached", "--quiet", "HEAD", "--", *controls)
        if staged.returncode != 0:
            raise MechanicalRefreshError(
                f"refresh {label}: staged control changes differ from committed HEAD; manual recovery required"
            )


def _assert_canonical_publication_paths(
    root: Path,
    publication_dir: Path,
    reviewed_path: Path,
    receipt_path: Path,
    gate_path: Path,
    manuscript_rel: str,
    roles: dict[str, str],
) -> None:
    """Assert full Profile-derived surface/receipt/Gate/manuscript paths.

    Requires exact default filenames (not just the parent directory), receipt
    next to the reviewed surface, all three under the canonical publication
    dir, and the manuscript row equal to the canonical ``reader-manuscript``
    role (unique is not enough). Runs before any retained write.
    """
    if reviewed_path.name != "reader-surface-input-v2.json":
        raise MechanicalRefreshError(
            f"refresh reviewed surface filename is not canonical: {reviewed_path.name}"
        )
    if receipt_path.name != RECEIPT_FILENAME:
        raise MechanicalRefreshError(f"refresh receipt filename is not canonical: {receipt_path.name}")
    if gate_path.name != GATE_FILENAME:
        raise MechanicalRefreshError(f"refresh Gate filename is not canonical: {gate_path.name}")
    if reviewed_path.parent != publication_dir or receipt_path.parent != publication_dir:
        raise MechanicalRefreshError("refresh reviewed surface/receipt are not under canonical Profile publication/v2")
    if gate_path.parent != publication_dir:
        raise MechanicalRefreshError("refresh Gate is not under canonical Profile publication/v2")
    if receipt_path.parent != reviewed_path.parent:
        raise MechanicalRefreshError("refresh receipt must live next to the reviewed reader input")
    if manuscript_rel != roles.get("reader-manuscript"):
        raise MechanicalRefreshError(
            f"refresh manuscript row is not the canonical reader-manuscript role: {manuscript_rel!r}"
        )


def _record_inventory(publication_dir: Path) -> dict[str, str]:
    """Inventory revalidation records by name+hash/identity (not names only).

    Includes regular files (sha256 of bytes), symlinks (link target, never
    followed), and any other entry type by kind label, so symlink/partial
    plants are detected instead of being filtered out by ``is_file``. Any
    unreadable entry raises a precise error: unknown state is never encoded
    as a sentinel value that could compare equal before/after and be treated
    as clean. Performs zero writes.
    """
    try:
        entries = list(publication_dir.iterdir())
    except OSError as exc:
        raise MechanicalRefreshError(f"refresh record inventory unreadable at {publication_dir}: {exc}") from exc
    inventory: dict[str, str] = {}
    for child in entries:
        if not child.name.startswith("publication-surface-revalidation-r"):
            continue
        try:
            is_link = child.is_symlink()
        except OSError as exc:
            raise MechanicalRefreshError(f"refresh record entry unreadable: {child.name}: {exc}") from exc
        if is_link:
            try:
                target = os.readlink(child)
            except OSError as exc:
                raise MechanicalRefreshError(f"refresh record symlink unreadable: {child.name}: {exc}") from exc
            inventory[child.name] = "symlink:" + target
            continue
        try:
            is_file = child.is_file()
        except OSError as exc:
            raise MechanicalRefreshError(f"refresh record entry unreadable: {child.name}: {exc}") from exc
        if is_file:
            # Regular records pin bytes AND file identity: a same-byte
            # replacement (identical content, different inode) changes the
            # inventory and is treated as disposition change (retained, never
            # adopted or deleted). Prior historical records keep stable
            # identity in the absence of concurrent writers.
            try:
                _st = os.stat(child)
                _digest = core.sha256_file(child)
            except OSError as exc:
                raise MechanicalRefreshError(f"refresh record file unreadable: {child.name}: {exc}") from exc
            inventory[child.name] = f"sha256:{_digest}:ino:{_st.st_dev}:{_st.st_ino}"
        else:
            inventory[child.name] = "<other>"
    return inventory


def _compare_gate_reports(
    old: dict[str, Any],
    new: dict[str, Any],
    *,
    old_receipt_rel: str,
    old_receipt_sha: str,
    new_receipt_sha: str,
) -> None:
    """Complete old/new Gate equality except top-level evaluation metadata/digest/receipt.

    R1 permits only top-level evaluation timestamp/evaluator metadata
    (``recorded_at``; ``evaluated_by`` must still be stable), the internal
    digest (``gate_sha256``) and the exact derivation receipt replacement to
    change. The full validated ``semantic_authority`` dictionary is preserved
    exactly (the writer forwards the old bound dict through the existing
    ``evaluate_reader_surface_gate(semantic_authority=...)`` API, whose strict
    loader still reopens and revalidates the persisted review file, so no
    synthetic PASS is possible). No dropped findings/suppressions/scan scope
    is permitted.
    """
    allowed_top = {"recorded_at", "gate_sha256", "derivation"}
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
    # Semantic authority: preserved fully. The writer forwards the old validated
    # bound dictionary through evaluate(semantic_authority=...), so every
    # persisted reviewer-metadata field (status/decision/reviewed_by/surface /
    # recorded_at/reviewed_at/review_path/review_sha256/summary) must match.
    old_sem = old.get("semantic_authority", {})
    new_sem = new.get("semantic_authority", {})
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
        _run_ts = core.iso_utc(recorded_at).replace(":", "").replace("-", "").replace("Z", "Z")
    except Exception as exc:
        raise MechanicalRefreshError(f"refresh recorded_at invalid: {exc}") from exc
    # --recorded-at is temporal provenance, not an operation ID: same-instant
    # sequential refreshes must not share retention/temp names. The per-operation
    # nonce below (reused as the guard nonce) keeps same-instant overlapping
    # cooperating calls failing on the occupied guard while sequential
    # same-instant runs use distinct retention/temp names.
    _op_nonce = secrets.token_hex(16)
    run_id = f"{_run_ts}-{_op_nonce[:8]}"

    # ---- P0 preflight (read-only) ----
    # Canonical cfg passed to library too: writer requires exact canonical default config.
    try:
        canonical_cfg = core.load_json(root / core.DEFAULT_CONFIG)
    except (OSError, ValueError) as exc:
        raise MechanicalRefreshError(f"refresh canonical config unreadable: {exc}") from exc
    if cfg != canonical_cfg:
        raise MechanicalRefreshError("refresh requires the canonical default config bytes (no alternate-config authority)")
    _reject_symlink_ancestors(root, root / core.DEFAULT_CONFIG, "canonical config")
    # Raw user-supplied --state path: lstat ancestors BEFORE any .resolve(),
    # so a CLI alias (symlinked State path or symlinked parent) is refused
    # instead of being resolved away by _rel().
    _raw_state_abs = state_path if state_path.is_absolute() else (root.resolve() / state_path)
    _check_raw_abs_ancestors(root.resolve(), _raw_state_abs, "Production State")
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
        _check_raw_rel_ancestors(root.resolve(), profile_p0["paths"]["source_root"], "Weekly source root")
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
    # Alias cross-check: the resolved role path must equal the lexically
    # derived Profile path. An inside-root symlink (e.g. publication ->
    # publication-real) resolves away in the owner helper, yielding a rel that
    # no checkpoint row carries; refuse explicitly as an alias instead of a
    # confusing row-mismatch later.
    try:
        _raw_src = profile_p0["paths"]["source_root"]
        _lex_gate_rel = _raw_src.rstrip("/") + "/publication/v2/" + GATE_FILENAME
    except (KeyError, TypeError, AttributeError) as exc:
        raise MechanicalRefreshError(f"refresh Profile source_root invalid: {exc}") from exc
    if gate_rel != _lex_gate_rel:
        raise MechanicalRefreshError(
            f"refresh Gate role path is not the canonical Profile path (possible alias): "
            f"resolved {gate_rel} != lexical {_lex_gate_rel}"
        )
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
    # cause instead of being misread as "no change". Staged-only divergence
    # (worktree matching HEAD while the index differs) is rejected explicitly
    # first with its own message; _verify_head_bytes also covers it.
    _staged_preflight = _git(root, "diff", "--cached", "--quiet", "HEAD", "--", *controls)
    if _staged_preflight.returncode != 0:
        raise MechanicalRefreshError(
            "refresh staged control changes differ from committed HEAD; refusing before any write"
        )
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
        _check_raw_rel_ancestors(root.resolve(), profile["paths"]["source_root"], "Weekly source root")
        _check_raw_rel_ancestors(root.resolve(), profile["paths"]["survey_root"], "Weekly survey root")
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
    # Derive publication dir lexically from the raw Profile source_root string
    # (not from the already-resolved source_root), so an aliased source_root
    # cannot resolve away before the ancestor walk.
    _pub_rel = profile["paths"]["source_root"].rstrip("/") + "/publication/v2"
    _check_raw_rel_ancestors(root.resolve(), _pub_rel, "publication dir")
    publication_dir = core.repo_local_path(root, _pub_rel, "publication dir")
    _reject_symlink_ancestors(root, publication_dir, "publication dir")
    _reject_symlink_ancestors(root, reviewed_path, "reviewed reader input")
    _assert_canonical_publication_paths(
        root, publication_dir, reviewed_path.resolve(), old_receipt_path.resolve(),
        gate_path.resolve(), manuscript_rel, roles,
    )
    # Canonical State already verified Profile-derived above.
    # Capture complete bound snapshot before any live write.
    bound_snapshot = _capture_bound_snapshot(
        root,
        state_path=state_path,
        state=state,
        state_sha=state_sha_p0,
        gate_path=gate_path,
        gate_sha=old_gate_sha,
        old_gate=old_gate,
        receipt_path=old_receipt_path,
        receipt_sha=receipt_ref["sha256"],
        old_receipt=old_receipt,
        checkpoint_path=checkpoint_path,
        checkpoint_sha=validation_ref["sha256"],
        checkpoint=checkpoint,
        manuscript_path=manuscript_path,
        bundle_doc=bundle_doc,
        active=active,
        head=head,
        cfg=cfg,
    )
    lock_path = publication_dir / LOCK_FILENAME
    _reject_symlink_ancestors(root, lock_path, "cooperative guard")
    if lock_path.is_symlink() or lock_path.exists():
        raise MechanicalRefreshError(f"cooperative refresh guard occupied: {lock_path}")
    # Per-operation unique nonce: two operations with identical run_id/head/state
    # still have distinct guard bytes AND distinct file identity, so replacing a
    # guard with identical timestamp/head/state contents cannot pass ownership.
    expected_guard_bytes = core.json_bytes(
        {"run_id": run_id, "head": head, "state_sha256": state_sha_p0,
         "nonce": _op_nonce, "pid": os.getpid()}
    )
    # Recheck the freshly captured snapshot BEFORE creating the guard: drift
    # injected after preflight (checkpoint/result/criteria/script) must refuse
    # here with no guard/retention/live writes at all.
    _recheck_bound_snapshot(root, bound_snapshot, controls, "before guard creation")
    try:
        with open(lock_path, "xb") as fh:
            fh.write(expected_guard_bytes)
            fh.flush()
            try:
                os.fsync(fh.fileno())
            except OSError:
                pass
            try:
                _fst = os.fstat(fh.fileno())
                expected_guard_id: tuple[int, int] | None = (_fst.st_dev, _fst.st_ino)
            except OSError as exc:
                raise MechanicalRefreshError(f"cooperative guard identity capture failed: {exc}") from exc
    except FileExistsError as exc:
        raise MechanicalRefreshError(f"cooperative refresh guard occupied: {lock_path}") from exc
    # Verify own guard bytes + identity immediately (no blessing of raced bytes).
    try:
        if lock_path.read_bytes() != expected_guard_bytes:
            raise MechanicalRefreshError(f"cooperative guard bytes mismatch after create: {lock_path}")
        if _guard_id_of(lock_path) != expected_guard_id:
            raise MechanicalRefreshError(f"cooperative guard identity mismatch after create: {lock_path}")
    except OSError as exc:
        if isinstance(exc, MechanicalRefreshError):
            raise
        raise MechanicalRefreshError(f"cooperative guard readback failed: {exc}") from exc
    owned_lock = True
    committed = False
    api_attempted = False
    live_stage = 0
    pre_records: dict[str, str] = {}
    try:
        _verify_guard_owned(lock_path, expected_guard_bytes, expected_guard_id, "cooperative guard (after acquisition)")
        _recheck_bound_snapshot(root, bound_snapshot, controls, "after guard acquisition")
        _verify_guard_owned(lock_path, expected_guard_bytes, expected_guard_id, "cooperative guard (before retention)")
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
        _verify_guard_owned(lock_path, expected_guard_bytes, expected_guard_id, "cooperative guard (after retention mkdir)")
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
        _recheck_bound_snapshot(root, bound_snapshot, controls, "before receipt installation")
        _verify_guard_owned(lock_path, expected_guard_bytes, expected_guard_id, "cooperative guard (before receipt installation)")
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
        _recheck_bound_snapshot(root, bound_snapshot, controls, "before Gate computation")
        _verify_guard_owned(lock_path, expected_guard_bytes, expected_guard_id, "cooperative guard (before Gate computation)")
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
        # Forward the old VALIDATED semantic_authority bound dictionary through
        # the existing supported API. Its strict loader still reopens and
        # revalidates the persisted review file (review_sha256 + PASS/blocking
        # consistency), so inspection-only bypass is impossible and the full
        # persisted reviewer metadata (including summary/recorded_at/reviewed_at)
        # is preserved exactly in the renewed report.
        new_report = surface_gate.evaluate_reader_surface_gate(
            root,
            manuscript_path,
            semantic_authority=dict(old_gate.get("semantic_authority", {})),
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
        _recheck_bound_snapshot(root, bound_snapshot, controls, "before Gate installation")
        _verify_guard_owned(lock_path, expected_guard_bytes, expected_guard_id, "cooperative guard (before Gate installation)")
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
        _recheck_bound_snapshot(root, bound_snapshot, controls, "before revalidation")
        _verify_guard_owned(lock_path, expected_guard_bytes, expected_guard_id, "cooperative guard (before revalidation)")
        basis = agent.built_checked_pending_publication_basis(root, cfg, state_path)
        # The just-renewed Gate must be the only NEW change relative to the
        # active starting authority. Rows already renewed by a healthy prior
        # metadata revalidation (manuscript/reviews with current-effective
        # shas) are accepted only if they match the active record's superseded
        # rows exactly (same name/path/prior/new); anything else is an
        # unrelated mutation and refuses. Note: this contract delta (Gate-new
        # plus already-active rows) is a clarification of the renewal boundary,
        # not an automatic expansion of revalidation authority: row unions stay
        # strict and every active file remains snapshot-pinned.
        _gate_reps = [r for r in basis.replacements if r[0] == "reader-surface-gate"]
        if len(_gate_reps) != 1 or _gate_reps[0][1] != gate_rel:
            raise MechanicalRefreshError("pending basis is not exactly the renewed Gate row")
        if active is None:
            if len(basis.replacements) != 1:
                raise MechanicalRefreshError("pending basis is not exactly the renewed Gate row")
        else:
            _active_sup = {
                (row.get("name"), row.get("path")): (row.get("prior_sha256"), row.get("new_sha256"))
                for row in active.get("superseded_artifacts", []) if isinstance(row, dict)
            }
            for _rep in basis.replacements:
                if _rep[0] == "reader-surface-gate":
                    continue
                if _active_sup.get((_rep[0], _rep[1])) != (_rep[2], _rep[3]):
                    raise MechanicalRefreshError(
                        f"pending basis has unrelated change outside the renewed Gate and active authority: {_rep[0]}"
                    )
        # Capture pre-API record inventory (names+hashes/identity) for
        # post-failure disposition inspection. Unreadable here fails closed.
        pre_records = _record_inventory(publication_dir)
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
                _release_guard_if_owned(lock_path, expected_guard_bytes, expected_guard_id, "cooperative guard (post-commit)")
            except MechanicalRefreshError as guard_exc:
                raise MechanicalRefreshError(
                    f"refresh post-commit reporting failed ({exc}); committed at {_rel(root, record_path) if 'record_path' in locals() else 'unknown'}; "
                    f"guard retained for manual reconciliation: {guard_exc}"
                ) from exc
            if isinstance(exc, MechanicalRefreshError):
                raise
            raise MechanicalRefreshError(f"refresh post-commit reporting failed: {exc}") from exc
        # Pre-commit: guard ownership FIRST. If the guard was lost/replaced,
        # STOP immediately: preserve live/foreign bytes, perform no restore
        # through a foreign guard and delete nothing.
        try:
            _verify_guard_owned(lock_path, expected_guard_bytes, expected_guard_id, "cooperative guard (failure path)")
        except MechanicalRefreshError as guard_exc:
            raise MechanicalRefreshError(
                f"refresh failed ({exc}); guard ownership lost, no restoration attempted; "
                f"live bytes + retention + foreign guard preserved for manual recovery: {guard_exc}"
            ) from exc
        # Pre-commit: inspect actual State/record disposition after API error; do not assume rollback.
        # Record inventory compares names+hashes/identity (symlink/partial included);
        # an unreadable post inventory is UNKNOWN and fails closed (never clean).
        if api_attempted:
            try:
                cur_state_bytes = state_path.read_bytes()
            except OSError:
                cur_state_bytes = None
            try:
                post_records = _record_inventory(publication_dir)
            except MechanicalRefreshError as inv_exc:
                raise MechanicalRefreshError(
                    f"refresh revalidation failed ({exc}); post-failure record inventory unreadable, "
                    f"disposition unknown, live bytes + retention + guard preserved for manual recovery: {inv_exc}; "
                    f"paths State={_rel(root, state_path)} Gate={_rel(root, gate_path)} Receipt={_rel(root, old_receipt_path)}"
                ) from exc
            # Leftover tampered/orphan record or changed State => manual guard retained.
            if cur_state_bytes != pre_state_bytes or post_records != pre_records:
                raise MechanicalRefreshError(
                    f"refresh revalidation failed with State/record disposition changed "
                    f"(State equal={cur_state_bytes == pre_state_bytes}, "
                    f"records before={sorted(pre_records)}, after={sorted(post_records)}); "
                    f"live bytes + retention + guard preserved for manual recovery: {exc}; "
                    f"paths State={_rel(root, state_path)} Gate={_rel(root, gate_path)} Receipt={_rel(root, old_receipt_path)}"
                ) from exc
            # Disposition clean (State original, record inventory identical): fall through to guarded restoration below.
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
                _recheck_bound_snapshot(root, {k: v for k, v in bound_snapshot.items() if not (k.startswith("__RECEIPT__:") or k.startswith("__GATE__:") or k.startswith("__STATE__:") or k == "__HEAD__")}, controls, "pre-restore dependencies")
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
            _release_guard_if_owned(lock_path, expected_guard_bytes, expected_guard_id, "cooperative guard (restored)")
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
        _release_guard_if_owned(lock_path, expected_guard_bytes, expected_guard_id, "cooperative guard (committed)")
    else:
        # Success without commit should not happen (all successes commit), but handle safely.
        _release_guard_if_owned(lock_path, expected_guard_bytes, expected_guard_id, "cooperative guard (success)")
    return {
        "state": _rel(root, state_path),
        "revalidation_record": _rel(root, record_path),
        "receipt": _rel(root, old_receipt_path),
        "gate": _rel(root, gate_path),
        "retention": _rel(root, run_dir),
        "supersedes": supersedes,
    }
