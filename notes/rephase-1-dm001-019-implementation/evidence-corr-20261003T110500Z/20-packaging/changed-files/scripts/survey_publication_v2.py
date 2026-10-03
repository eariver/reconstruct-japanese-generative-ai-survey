#!/usr/bin/env python3
"""Exact-byte publication authority for Survey Production Core v2.

Publication Preview is the second and final normal Human Gate. The redesigned
candidate is finalized only after ChatGPT has authored an explicit reader-facing
source and completed semantic/editorial plus exact-PDF visual review. Human
approval then binds that already-reviewed candidate; Freeze/Release re-use the
same exact authority instead of introducing a second post-approval quality pass.
"""

from __future__ import annotations

import json
import os
import stat
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality
from scripts import survey_reader_publication_v2 as reader
from scripts import survey_schema_v2 as schema_gate

CANDIDATE_SCHEMA = Path("schemas/publication-candidate-v2.schema.json")
PREVIEW_APPROVAL_SCHEMA = Path("schemas/publication-preview-approval-v2.schema.json")
VISUAL_REVIEW_SCHEMA = Path("schemas/visual-review-record-v2.schema.json")  # legacy post-approval record
FREEZE_SCHEMA = Path("schemas/freeze-record-v2.schema.json")
RELEASE_MANIFEST_SCHEMA = Path("schemas/release-manifest-v2.schema.json")
MERGE_VERIFICATION_SCHEMA = Path("schemas/merge-verification-v2.schema.json")
RELEASE_RECORD_SCHEMA = Path("schemas/release-record-v2.schema.json")


def _rel(repo_root: Path, path: Path) -> str:
    root = repo_root.resolve()
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(root)).replace("\\", "/")
    except ValueError as exc:
        raise ValueError(f"publication artifact must be repository-local: {path}") from exc


def _safe_file(repo_root: Path, path: Path, label: str) -> Path:
    _rel(repo_root, path)
    resolved = path.resolve()
    if resolved.is_symlink() or not resolved.is_file():
        raise ValueError(f"{label} missing or unsafe: {path}")
    return resolved


def _authority(repo_root: Path, path: Path) -> dict[str, Any]:
    value = _safe_file(repo_root, path, "publication authority input")
    return {"path": _rel(repo_root, value), "sha256": core.sha256_file(value), "byte_count": value.stat().st_size}


def _validate_authority(repo_root: Path, ref: dict[str, Any], label: str) -> Path:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256", "byte_count"}:
        raise ValueError(f"{label} authority fields invalid")
    artifact = _safe_file(repo_root, repo_root / ref["path"], label)
    if core.sha256_file(artifact) != ref["sha256"] or artifact.stat().st_size != ref["byte_count"]:
        raise ValueError(f"{label} bytes drifted")
    return artifact


def _write_immutable(path: Path, payload: dict[str, Any], label: str) -> Path:
    if path.exists():
        if core.load_json(path) != payload:
            raise ValueError(f"refusing to overwrite divergent {label}: {path}")
        return path
    core.write_json(path, payload)
    return path


def public_issue_slug_from_profile(profile: dict[str, Any]) -> str:
    """Derive the public issue slug from the exact Profile survey_root authority.

    Internal issue IDs and reader-facing slugs are intentionally not always
    identical; the basename of ``paths.survey_root`` is the public identity.
    """
    survey_root = profile.get("paths", {}).get("survey_root")
    if not isinstance(survey_root, str) or not survey_root.strip():
        raise ValueError("Production Profile survey_root required for public issue identity")
    slug = Path(survey_root).name
    if not slug or slug in {".", ".."} or "/" in slug or "\\" in slug:
        raise ValueError("Production Profile survey_root has invalid public issue slug")
    return slug


def profile_release_identity(profile: dict[str, Any]) -> str:
    """Derive release identity from the validated Profile slug and publication profile."""
    slug = public_issue_slug_from_profile(profile)
    publication_profile = profile.get("publication_profile")
    if publication_profile == "WEEKLY_MAGAZINE":
        return f"weekly/{slug}"
    if publication_profile == "LONGFORM_SPECIAL":
        return f"special/{slug}"
    raise ValueError(f"unsupported publication profile: {publication_profile}")


def _lexical_repo_path(repo_root: Path, path: Path, label: str) -> Path:
    """Lexically normalize a repo-local path without resolving symlinks.

    Accepts repo-relative paths and absolute paths inside ``repo_root``.
    Backslashes and any lexical ``..`` segment are rejected before
    normalization: ``normpath`` would otherwise erase a ``..`` component
    whose resolution through a symlinked ancestor differs from the
    normalized spelling. Repository escapes are rejected as well, so later
    symlink checks observe the true ancestry.
    """
    raw = str(path)
    if "\\" in raw:
        raise ValueError(f"{label} must not contain backslashes: {path}")
    if ".." in Path(raw).parts:
        raise ValueError(f"{label} must not contain '..' segments: {path}")
    root = repo_root.resolve()
    candidate = path if path.is_absolute() else (root / path)
    normalized = Path(os.path.normpath(str(candidate)))
    try:
        normalized.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository root: {path}") from exc
    return normalized


def _check_output_ancestors(root: Path, target: Path, label: str) -> None:
    """Refuse symlinked or non-directory existing ancestor components via lstat."""
    rel = target.relative_to(root)
    cursor = root
    for part in rel.parts[:-1]:
        cursor = cursor / part
        try:
            st = os.lstat(cursor)
        except FileNotFoundError:
            # Nothing below a missing component can exist; it is created at install.
            return
        except OSError as exc:
            raise ValueError(f"{label} ancestor unreadable: {cursor}") from exc
        if stat.S_ISLNK(st.st_mode):
            raise ValueError(f"{label} ancestor is a symlink: {cursor}")
        if not stat.S_ISDIR(st.st_mode):
            raise ValueError(f"{label} ancestor is not a directory: {cursor}")


def _existing_compatible_bytes(target: Path, payload: dict[str, Any], label: str) -> bytes | None:
    """Return preserved existing bytes when the file holds exactly payload, else None.

    Existing symlinks, non-regular files and divergent bytes are refused.
    Equal-payload files keep their exact bytes (including formatting); the
    caller hashes the returned bytes rather than reserializing.
    """
    try:
        st = os.lstat(target)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise ValueError(f"{label} target unreadable: {target}") from exc
    if stat.S_ISLNK(st.st_mode):
        raise ValueError(f"{label} target is a symlink: {target}")
    if not stat.S_ISREG(st.st_mode):
        raise ValueError(f"{label} target is not a regular file: {target}")
    try:
        data = target.read_bytes()
        existing = json.loads(data.decode("utf-8"))
    except (OSError, ValueError, UnicodeDecodeError) as exc:
        raise ValueError(f"refusing to overwrite divergent {label}: {target}") from exc
    if not isinstance(existing, dict) or existing != payload:
        raise ValueError(f"refusing to overwrite divergent {label}: {target}")
    return data


def _prepare_freeze_inputs(repo_root: Path, candidate_path: Path, approval_path: Path) -> dict[str, Any]:
    """Validate and resolve the joint Freeze authority shared by both builders.

    Resolves the actual Candidate, its typed Preview approval, the exact
    approval→Candidate path/hash binding, the Candidate-bound pre-preview
    VISUAL record, exact source/PDF/page relationships and the Candidate-bound
    Production Profile (via the validated quality bundle). Captures a
    bounded byte snapshot of every authority input for install-boundary
    rechecks. No writes.
    """
    candidate = validate_candidate(repo_root, candidate_path)
    approval = validate_preview_approval(repo_root, approval_path, issue_id=candidate["issue_id"])
    candidate_rel = _rel(repo_root, candidate_path)
    candidate_file = _safe_file(repo_root, candidate_path, "Publication Candidate")
    if (
        approval["publication_candidate_path"] != candidate_rel
        or approval["publication_candidate_sha256"] != core.sha256_file(candidate_file)
    ):
        raise ValueError("Publication Preview approval does not bind the exact Publication Candidate being frozen")
    visual_path = _safe_file(
        repo_root, repo_root / candidate["visual_review"]["path"], "Candidate pre-preview visual review"
    )
    visual = reader.validate_review_record(
        repo_root, visual_path, issue_id=candidate["issue_id"], expected_kind="VISUAL"
    )
    if candidate["pdf"]["sha256"] != approval["pdf_sha256"] or visual["pdf"]["sha256"] != approval["pdf_sha256"]:
        raise ValueError("Freeze exact-PDF authority chain diverged")
    bundle_path = core.repo_local_path(repo_root, candidate["quality_bundle"]["path"], "Quality Bundle")
    bundle = quality.validate_bundle(repo_root, bundle_path, issue_id=candidate["issue_id"])
    profile_ref = bundle["production_profile"]
    profile_path = core.repo_local_path(repo_root, profile_ref["path"], "Quality Production Profile")
    if not profile_path.is_file() or core.sha256_file(profile_path) != profile_ref["sha256"]:
        raise ValueError("Quality Bundle Production Profile authority drift")
    profile = core.load_json(profile_path)
    if profile.get("issue_id") != candidate["issue_id"]:
        raise ValueError("Production Profile issue identity diverges from Publication Candidate")
    if profile.get("publication_profile") != candidate["publication_profile"]:
        raise ValueError("Production Profile publication identity diverges from Publication Candidate")
    try:
        source_root = core.repo_local_path(repo_root, profile["paths"]["source_root"], "source_root")
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"Production Profile source_root invalid: {exc}") from exc
    snapshot_files = [
        candidate_file,
        _safe_file(repo_root, approval_path, "Publication Preview approval"),
        visual_path,
        bundle_path,
        profile_path,
        _safe_file(repo_root, repo_root / candidate["reader_manuscript"]["path"], "Candidate Reader Manuscript"),
        _safe_file(repo_root, repo_root / candidate["source"]["path"], "Candidate source"),
        _safe_file(repo_root, repo_root / candidate["pdf"]["path"], "Candidate PDF"),
        _safe_file(
            repo_root, repo_root / candidate["semantic_review"]["path"], "Candidate semantic review"
        ),
    ]
    snapshot: dict[str, str] = {}
    for item in snapshot_files:
        rel = _rel(repo_root, item)
        snapshot[rel] = core.sha256_file(item)
    return {
        "candidate": candidate,
        "candidate_path": candidate_path,
        "candidate_rel": candidate_rel,
        "approval": approval,
        "approval_path": approval_path,
        "visual": visual,
        "visual_path": visual_path,
        "bundle": bundle,
        "bundle_path": bundle_path,
        "profile": profile,
        "profile_path": profile_path,
        "profile_ref": profile_ref,
        "source_root": source_root,
        "snapshot": snapshot,
    }


def _recheck_snapshot(repo_root: Path, snapshot: dict[str, str], stage: str) -> None:
    """Fail when any snapshotted authority byte changed since preparation."""
    for rel, expected in snapshot.items():
        try:
            actual = core.sha256_file(repo_root.resolve() / rel)
        except OSError as exc:
            raise ValueError(f"Freeze authority input unreadable {stage}: {rel}") from exc
        if actual != expected:
            raise ValueError(f"Freeze authority input changed {stage}: {rel}")


def _build_freeze_payload(
    *,
    repo_root: Path,
    candidate_path: Path,
    candidate: dict[str, Any],
    approval_path: Path,
    approval: dict[str, Any],
    visual_path: Path,
    frozen_at: datetime,
) -> dict[str, Any]:
    """Construct the exact Freeze record payload (pure; no writes)."""
    _ = approval
    return {
        "schema_version": "2.0-rc1",
        "issue_id": candidate["issue_id"],
        "status": "FROZEN",
        "publication_candidate_path": _rel(repo_root, candidate_path),
        "publication_candidate_sha256": core.sha256_file(
            _safe_file(repo_root, candidate_path, "Publication Candidate")
        ),
        "publication_preview_approval_path": _rel(repo_root, approval_path),
        "publication_preview_approval_sha256": core.sha256_file(
            _safe_file(repo_root, approval_path, "Publication Preview approval")
        ),
        "visual_review_path": _rel(repo_root, visual_path),
        "visual_review_sha256": core.sha256_file(visual_path),
        "source_path": candidate["source"]["path"],
        "source_sha256": candidate["source"]["sha256"],
        "pdf_path": candidate["pdf"]["path"],
        "pdf_sha256": candidate["pdf"]["sha256"],
        "page_count": candidate["pdf"]["page_count"],
        "frozen_at": core.iso_utc(frozen_at),
    }


def _build_manifest_payload(
    *,
    repo_root: Path,
    freeze_path: Path,
    freeze_record_sha256: str,
    release_identity: str,
    source_path: str,
    source_sha256: str,
    pdf_path: str,
    pdf_sha256: str,
    page_count: int,
    issue_id: str,
) -> dict[str, Any]:
    """Construct the exact Release manifest payload (pure; no writes)."""
    return {
        "schema_version": "2.0-rc1",
        "issue_id": issue_id,
        "release_identity": release_identity,
        "status": "AUTHORIZED",
        "freeze_record_path": _rel(repo_root, freeze_path),
        "freeze_record_sha256": freeze_record_sha256,
        "source_path": source_path,
        "source_sha256": source_sha256,
        "pdf_path": pdf_path,
        "pdf_sha256": pdf_sha256,
        "page_count": page_count,
    }


def _preflight_freeze_pair(
    repo_root: Path,
    freeze_path: Path,
    manifest_path: Path,
    prep: dict[str, Any],
    freeze_payload: dict[str, Any],
    make_manifest_payload: Callable[[str, Path], dict[str, Any]],
    extra_snapshot: dict[str, str] | None = None,
) -> tuple[Path, Path, bytes, bytes, str, dict[str, str]]:
    """Complete pre-install gate for the Freeze/Manifest pair. Performs no writes.

    Validates both full schemas and both target/parent conflicts (including
    nested outputs and target/input aliasing) before any target or
    parent-directory write. Equal-payload existing files keep their exact
    bytes; the returned Freeze SHA is always computed over the bytes that
    will be ensured on disk, so the Manifest is fully known here. The
    manifest builder receives the Freeze SHA and the normalized Freeze
    target so payload refs and install paths are one consistent target.
    Returns ``(freeze_target, manifest_target, freeze_bytes, manifest_bytes,
    freeze_sha256, snapshot)``.
    """
    root = repo_root.resolve()
    norm_freeze = _lexical_repo_path(repo_root, freeze_path, "Freeze record")
    norm_manifest = _lexical_repo_path(repo_root, manifest_path, "Release manifest")
    if norm_freeze == norm_manifest:
        raise ValueError("Freeze record and Release manifest targets must differ")
    if norm_freeze in norm_manifest.parents or norm_manifest in norm_freeze.parents:
        raise ValueError(
            "Freeze record and Release manifest targets must not nest: "
            f"{norm_freeze} vs {norm_manifest}"
        )
    schema_gate.validate_instance(freeze_payload, repo_root / FREEZE_SCHEMA, label="Freeze record")
    _check_output_ancestors(root, norm_freeze, "Freeze record")
    _check_output_ancestors(root, norm_manifest, "Release manifest")

    candidate = prep["candidate"]
    authority_raw: list[Path] = [
        repo_root / candidate[key]["path"]
        for key in (
            "reader_manuscript",
            "source",
            "pdf",
            "quality_bundle",
            "semantic_review",
            "visual_review",
        )
    ]
    authority_raw += [
        prep["candidate_path"],
        prep["approval_path"],
        prep["visual_path"],
        prep["bundle_path"],
        prep["profile_path"],
    ]
    identities: set[tuple[int, int]] = set()
    spellings: set[Path] = set()
    for raw in authority_raw:
        norm = _lexical_repo_path(repo_root, raw, "Freeze authority input")
        spellings.add(norm)
        try:
            st = os.stat(norm)
        except OSError as exc:
            raise ValueError(f"Freeze authority input unreadable: {raw}") from exc
        identities.add((st.st_dev, st.st_ino))
    for label, norm in (("Freeze record", norm_freeze), ("Release manifest", norm_manifest)):
        if norm in spellings:
            raise ValueError(f"{label} target overlaps a Freeze authority input: {norm}")
        try:
            st = os.stat(norm)
        except FileNotFoundError:
            continue
        except OSError as exc:
            raise ValueError(f"{label} target unreadable: {norm}") from exc
        if (st.st_dev, st.st_ino) in identities:
            raise ValueError(f"{label} target is hardlinked to a Freeze authority input: {norm}")

    freeze_bytes = _existing_compatible_bytes(norm_freeze, freeze_payload, "Freeze record")
    freeze_is_new = freeze_bytes is None
    if freeze_is_new:
        freeze_bytes = core.json_bytes(freeze_payload)
    assert freeze_bytes is not None
    freeze_sha = core.sha256_bytes(freeze_bytes)
    try:
        os.lstat(norm_manifest)
        manifest_present = True
    except FileNotFoundError:
        manifest_present = False
    except OSError as exc:
        raise ValueError(f"Release manifest target unreadable: {norm_manifest}") from exc
    manifest_payload = make_manifest_payload(freeze_sha, norm_freeze)
    schema_gate.validate_instance(manifest_payload, repo_root / RELEASE_MANIFEST_SCHEMA, label="Release manifest")
    manifest_bytes = _existing_compatible_bytes(norm_manifest, manifest_payload, "Release manifest")
    if freeze_is_new and manifest_present:
        raise ValueError(
            "Release manifest target exists without its Freeze record: "
            f"refusing to install a Freeze pair under pre-existing Manifest bytes: {norm_manifest}"
        )
    if manifest_bytes is None:
        manifest_bytes = core.json_bytes(manifest_payload)
    assert manifest_bytes is not None
    snapshot = dict(prep["snapshot"])
    if extra_snapshot:
        for rel, sha in extra_snapshot.items():
            if rel in snapshot and snapshot[rel] != sha:
                raise ValueError(f"Freeze snapshot conflicts for {rel}")
            snapshot[rel] = sha
    _recheck_snapshot(repo_root, snapshot, "before install")
    return (norm_freeze, norm_manifest, freeze_bytes, manifest_bytes, freeze_sha, snapshot)


def _ensure_parent_dir(root: Path, target: Path, label: str) -> None:
    _check_output_ancestors(root, target, label)
    target.parent.mkdir(parents=True, exist_ok=True)
    # Cheap post-mkdir narrowing (no cross-process claim): refuse a parent
    # chain that changed under us before any file is created.
    _check_output_ancestors(root, target, label)


def _remove_owned_partial(
    path: Path, created_dev: int, created_ino: int, intended: bytes, label: str, cause: BaseException
) -> None:
    """Remove an incomplete file only when this call created it and bytes are a known partial prefix.

    Identity is established with ``lstat`` (never following a replaced
    symlink); any symlink, identity change, or non-prefix content leaves the
    foreign/unverifiable residual intact with an explicit failure.
    """
    try:
        st = os.lstat(path)
    except OSError:
        raise ValueError(
            f"{label} install failed and residual cannot be verified; left intact: {path} ({cause})"
        ) from cause
    if stat.S_ISLNK(st.st_mode):
        raise ValueError(
            f"{label} install failed and residual is a symlink; left intact: {path} ({cause})"
        ) from cause
    if (st.st_dev, st.st_ino) != (created_dev, created_ino):
        raise ValueError(
            f"{label} install failed and target identity changed; left intact: {path} ({cause})"
        ) from cause
    try:
        current = path.read_bytes()
    except OSError:
        raise ValueError(
            f"{label} install failed and residual unreadable; left intact: {path} ({cause})"
        ) from cause
    if len(current) >= len(intended) or intended[: len(current)] != current:
        raise ValueError(
            f"{label} install failed with unverifiable residual; left intact: {path} ({cause})"
        ) from cause
    try:
        os.unlink(path)
    except OSError:
        raise ValueError(
            f"{label} install failed; owned partial residual could not be removed: {path} ({cause})"
        ) from cause
    raise ValueError(f"{label} install failed; owned partial file removed: {path} ({cause})") from cause


def _close_quietly(fd: int) -> None:
    try:
        os.close(fd)
    except OSError:
        pass


def _install_owned_json(root: Path, path: Path, data: bytes, label: str) -> None:
    """Exclusively create a file holding exactly ``data``.

    A colliding existing target is revalidated (lstat type/symlink/ancestor
    checks plus exact content) before any read: identical bytes resume,
    anything else is refused without overwrite and without blocking on
    special files. Partial writes attributable to this call are removed
    only after owned-identity/known-prefix verification. Close failures
    always propagate as explicit errors, never silent success.
    """
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW)
    except FileExistsError:
        try:
            st = os.lstat(path)
        except OSError as exc:
            raise ValueError(f"{label} target exists but is unreadable: {path}") from exc
        if stat.S_ISLNK(st.st_mode):
            raise ValueError(f"{label} target is a symlink: {path}")
        if not stat.S_ISREG(st.st_mode):
            raise ValueError(f"{label} target is not a regular file: {path}")
        _check_output_ancestors(root, path, label)
        try:
            existing = path.read_bytes()
        except OSError as exc:
            raise ValueError(f"{label} target exists but is unreadable: {path}") from exc
        if existing == data:
            return
        raise ValueError(f"refusing to overwrite divergent {label}: {path}")
    except OSError as exc:
        raise ValueError(f"{label} install failed before creation: {path} ({exc})") from exc
    try:
        created = os.fstat(fd)
    except OSError as exc:
        _close_quietly(fd)
        raise ValueError(f"{label} install failed immediately after creation: {path} ({exc})") from exc
    sent = 0
    try:
        while sent < len(data):
            chunk = os.write(fd, data[sent:])
            if chunk <= 0:
                raise OSError("short write with no progress")
            sent += chunk
    except OSError as exc:
        _close_quietly(fd)
        _remove_owned_partial(path, created.st_dev, created.st_ino, data, label, exc)
        raise AssertionError("unreachable") from exc
    try:
        os.close(fd)
    except OSError as exc:
        # A close error can signal writeback failure: never report success.
        # The descriptor state is unspecified after a failed close, so make
        # one best-effort release attempt before verification.
        _close_quietly(fd)
        # Verified complete bytes are retained with an explicit failure so an
        # identical retry resumes; anything else follows the owned-partial rule.
        try:
            st = os.lstat(path)
            landed = path.read_bytes() if stat.S_ISREG(st.st_mode) else None
            owned = (st.st_dev, st.st_ino) == (created.st_dev, created.st_ino)
        except OSError:
            landed, owned = None, False
        if owned and landed == data:
            raise ValueError(
                f"{label} install close failed but complete verified bytes retained "
                f"for identical retry: {path} ({exc})"
            ) from exc
        _remove_owned_partial(path, created.st_dev, created.st_ino, data, label, exc)
        raise AssertionError("unreachable") from exc


def _install_freeze_target(
    repo_root: Path, plan: tuple[Path, Path, bytes, bytes, str, dict[str, str]]
) -> Path:
    """Install the Freeze half of a preflighted plan, rechecking inputs first."""
    root = repo_root.resolve()
    norm_freeze, _norm_manifest, freeze_bytes, _manifest_bytes, _freeze_sha, snapshot = plan
    _recheck_snapshot(repo_root, snapshot, "before first write")
    _ensure_parent_dir(root, norm_freeze, "Freeze record")
    _install_owned_json(root, norm_freeze, freeze_bytes, "Freeze record")
    if norm_freeze.read_bytes() != freeze_bytes:
        raise ValueError(f"Freeze record bytes changed during install; left intact: {norm_freeze}")
    return norm_freeze


def _install_manifest_target(
    repo_root: Path, plan: tuple[Path, Path, bytes, bytes, str, dict[str, str]]
) -> Path:
    """Install the Manifest half of a preflighted plan, rechecking inputs first."""
    root = repo_root.resolve()
    norm_freeze, norm_manifest, _freeze_bytes, manifest_bytes, _freeze_sha, snapshot = plan
    _recheck_snapshot(repo_root, snapshot, "before second install")
    _ensure_parent_dir(root, norm_manifest, "Release manifest")
    _install_owned_json(root, norm_manifest, manifest_bytes, "Release manifest")
    if norm_manifest.read_bytes() != manifest_bytes:
        raise ValueError(
            "Release manifest bytes changed during install; "
            f"completed Freeze record retained: {norm_freeze}"
        )
    return norm_manifest


def _install_freeze_pair(
    repo_root: Path, plan: tuple[Path, Path, bytes, bytes, str, dict[str, str]]
) -> tuple[Path, Path]:
    """Install a preflighted Freeze/Manifest pair. Freeze is installed first.

    A completed valid Freeze is retained when Manifest installation fails so
    an identical retry resumes. Post-install bytes are rechecked; any drift
    is reported explicitly without deleting pre-existing authority.
    """
    norm_freeze = _install_freeze_target(repo_root, plan)
    _norm_freeze, norm_manifest, _fb, _mb, _fs, _snap = plan
    try:
        _install_manifest_target(repo_root, plan)
    except (OSError, ValueError) as exc:
        raise ValueError(
            "Release manifest install failed; completed Freeze record retained "
            f"for identical retry: {norm_freeze} ({exc})"
        ) from exc
    return norm_freeze, norm_manifest


def release_identity(publication_profile: str, issue_id: str) -> str:
    if publication_profile == "WEEKLY_MAGAZINE":
        return f"weekly/{issue_id}"
    if publication_profile == "LONGFORM_SPECIAL":
        return f"special/{issue_id}"
    raise ValueError(f"unsupported publication profile: {publication_profile}")


def build_candidate(
    repo_root: Path,
    issue_id: str,
    publication_profile: str,
    reader_manuscript_path: Path,
    source_path: Path,
    pdf_path: Path,
    page_count: int,
    quality_bundle_path: Path,
    semantic_review_path: Path,
    visual_review_path: Path,
    output_path: Path,
) -> Path:
    """Finalize one immutable Human Preview candidate from already-reviewed bytes."""
    if not isinstance(page_count, int) or page_count < 1:
        raise ValueError("Publication Candidate page_count must be positive")
    source = _safe_file(repo_root, source_path, "validated publication source")
    pdf = _safe_file(repo_root, pdf_path, "publication PDF")
    manuscript_file = _safe_file(repo_root, reader_manuscript_path, "Reader Manuscript Manifest")
    manuscript = reader.validate_manuscript_manifest(repo_root, manuscript_file, issue_id=issue_id)
    if manuscript["publication_profile"] != publication_profile:
        raise ValueError("Publication Candidate publication_profile differs from Reader Manuscript")
    if (
        manuscript["primary_source"]["path"] != _rel(repo_root, source)
        or manuscript["primary_source"]["sha256"] != core.sha256_file(source)
        or manuscript["primary_source"]["byte_count"] != source.stat().st_size
    ):
        raise ValueError("Reader Manuscript does not bind exact Publication Candidate source bytes")

    bundle = quality.validate_bundle(repo_root, quality_bundle_path, issue_id=issue_id)
    if bundle["publication_profile"] != publication_profile:
        raise ValueError("Publication Candidate publication_profile differs from bound Quality Production Profile")
    if bundle["source"]["path"] != _rel(repo_root, source) or bundle["source"]["sha256"] != core.sha256_file(source):
        raise ValueError("quality bundle does not bind exact Publication Candidate source bytes")
    pdf_authority = dict(bundle["pdf"])
    if pdf_authority["storage"] != "REPOSITORY_FILE":
        raise ValueError("Publication Candidate requires exact reviewed PDF bytes in repository storage")
    if (
        pdf_authority["path"] != _rel(repo_root, pdf)
        or pdf_authority["sha256"] != core.sha256_file(pdf)
        or pdf_authority["byte_count"] != pdf.stat().st_size
    ):
        raise ValueError("quality bundle does not bind exact Publication Candidate PDF bytes")

    semantic_file = _safe_file(repo_root, semantic_review_path, "Semantic/editorial review")
    visual_file = _safe_file(repo_root, visual_review_path, "Visual review")
    semantic = reader.validate_review_record(
        repo_root, semantic_file, issue_id=issue_id, expected_kind="SEMANTIC_EDITORIAL"
    )
    visual = reader.validate_review_record(repo_root, visual_file, issue_id=issue_id, expected_kind="VISUAL")
    for label, review in (("semantic", semantic), ("visual", visual)):
        if review["publication_profile"] != publication_profile:
            raise ValueError(f"{label} review publication_profile mismatch")
        if review["reader_manuscript"]["path"] != _rel(repo_root, manuscript_file) or review["reader_manuscript"]["sha256"] != core.sha256_file(manuscript_file):
            raise ValueError(f"{label} review does not bind exact Reader Manuscript")
        if review["source"]["path"] != _rel(repo_root, source) or review["source"]["sha256"] != core.sha256_file(source):
            raise ValueError(f"{label} review does not bind exact candidate source")
        if review["pdf"]["path"] != _rel(repo_root, pdf) or review["pdf"]["sha256"] != core.sha256_file(pdf):
            raise ValueError(f"{label} review does not bind exact candidate PDF")
        if review["pdf"]["byte_count"] != pdf.stat().st_size or review["page_count"] != page_count:
            raise ValueError(f"{label} review PDF size/page_count mismatch")

    base = {
        "schema_version": "2.0-rc1",
        "issue_id": issue_id,
        "publication_profile": publication_profile,
        "status": "READY_FOR_PUBLICATION_PREVIEW",
        "reader_manuscript": _authority(repo_root, manuscript_file),
        "source": _authority(repo_root, source),
        "pdf": {**pdf_authority, "page_count": page_count},
        "quality_bundle": _authority(repo_root, quality_bundle_path),
        "semantic_review": _authority(repo_root, semantic_file),
        "visual_review": _authority(repo_root, visual_file),
    }
    payload = dict(base)
    payload["candidate_sha256"] = core.sha256_object(base)
    schema_gate.validate_instance(payload, repo_root / CANDIDATE_SCHEMA, label="Publication Candidate")
    _write_immutable(output_path, payload, "Publication Candidate")
    return output_path


def validate_candidate(repo_root: Path, path: Path, *, issue_id: str | None = None) -> dict[str, Any]:
    payload = schema_gate.load_and_validate_json(path, repo_root / CANDIDATE_SCHEMA, label="Publication Candidate")
    if issue_id is not None and payload["issue_id"] != issue_id:
        raise ValueError("Publication Candidate issue_id mismatch")
    digest_fields = (
        "schema_version",
        "issue_id",
        "publication_profile",
        "status",
        "reader_manuscript",
        "source",
        "pdf",
        "quality_bundle",
        "semantic_review",
        "visual_review",
    )
    base = {key: payload[key] for key in digest_fields}
    if payload["candidate_sha256"] != core.sha256_object(base):
        raise ValueError("Publication Candidate content digest mismatch")

    manuscript_path = _validate_authority(repo_root, payload["reader_manuscript"], "Publication Candidate reader manuscript")
    source_path = _validate_authority(repo_root, payload["source"], "Publication Candidate source")
    bundle_path = _validate_authority(repo_root, payload["quality_bundle"], "Publication Candidate quality bundle")
    semantic_path = _validate_authority(repo_root, payload["semantic_review"], "Publication Candidate semantic review")
    visual_path = _validate_authority(repo_root, payload["visual_review"], "Publication Candidate visual review")

    manuscript = reader.validate_manuscript_manifest(repo_root, manuscript_path, issue_id=payload["issue_id"])
    if manuscript["publication_profile"] != payload["publication_profile"]:
        raise ValueError("Publication Candidate publication_profile diverges from Reader Manuscript")
    if manuscript["primary_source"] != payload["source"]:
        raise ValueError("Publication Candidate source diverges from Reader Manuscript primary source")

    bundle = quality.validate_bundle(repo_root, bundle_path, issue_id=payload["issue_id"])
    if bundle["publication_profile"] != payload["publication_profile"]:
        raise ValueError("Publication Candidate publication_profile diverges from coupled Quality Production Profile")
    if bundle["source"]["path"] != payload["source"]["path"] or bundle["source"]["sha256"] != payload["source"]["sha256"]:
        raise ValueError("Publication Candidate source diverges from coupled quality bundle")
    candidate_pdf = {key: payload["pdf"][key] for key in ("storage", "path", "sha256", "byte_count", "actions_artifact")}
    if candidate_pdf != bundle["pdf"]:
        raise ValueError("Publication Candidate PDF authority diverges from coupled quality bundle")
    if payload["pdf"]["storage"] != "REPOSITORY_FILE":
        raise ValueError("Publication Candidate PDF must be repository-resident for exact Human/ChatGPT review")
    pdf_path = _safe_file(repo_root, repo_root / payload["pdf"]["path"], "Publication Candidate PDF")
    if core.sha256_file(pdf_path) != payload["pdf"]["sha256"] or pdf_path.stat().st_size != payload["pdf"]["byte_count"]:
        raise ValueError("Publication Candidate PDF bytes drifted")

    semantic = reader.validate_review_record(
        repo_root, semantic_path, issue_id=payload["issue_id"], expected_kind="SEMANTIC_EDITORIAL"
    )
    visual = reader.validate_review_record(
        repo_root, visual_path, issue_id=payload["issue_id"], expected_kind="VISUAL"
    )
    for label, review in (("semantic", semantic), ("visual", visual)):
        if review["publication_profile"] != payload["publication_profile"]:
            raise ValueError(f"Publication Candidate {label} review Profile drift")
        if review["reader_manuscript"]["path"] != payload["reader_manuscript"]["path"] or review["reader_manuscript"]["sha256"] != payload["reader_manuscript"]["sha256"]:
            raise ValueError(f"Publication Candidate {label} review manuscript drift")
        if review["source"]["path"] != payload["source"]["path"] or review["source"]["sha256"] != payload["source"]["sha256"]:
            raise ValueError(f"Publication Candidate {label} review source drift")
        if review["pdf"]["path"] != payload["pdf"]["path"] or review["pdf"]["sha256"] != payload["pdf"]["sha256"]:
            raise ValueError(f"Publication Candidate {label} review PDF drift")
        if review["pdf"]["byte_count"] != payload["pdf"]["byte_count"] or review["page_count"] != payload["pdf"]["page_count"]:
            raise ValueError(f"Publication Candidate {label} review PDF size/page drift")
    if source_path.resolve() != (repo_root / payload["source"]["path"]).resolve():
        raise ValueError("Publication Candidate source authority resolution mismatch")
    return payload


def build_preview_approval(
    repo_root: Path,
    candidate_path: Path,
    output_path: Path,
    reviewed_by: str,
    reviewed_at: datetime,
    review_reference: str,
) -> Path:
    candidate = validate_candidate(repo_root, candidate_path)
    if not reviewed_by.strip() or not review_reference.strip():
        raise ValueError("Publication Preview reviewed_by/review_reference required")
    seed = {
        "issue_id": candidate["issue_id"],
        "candidate_sha256": core.sha256_file(candidate_path),
        "pdf_sha256": candidate["pdf"]["sha256"],
        "reviewed_at": core.iso_utc(reviewed_at),
        "review_reference": review_reference,
    }
    payload = {
        "schema_version": "2.0-rc1",
        "approval_id": f"publication-preview:{candidate['issue_id']}:{core.sha256_object(seed)[:20]}",
        "issue_id": candidate["issue_id"],
        "gate": "PUBLICATION_PREVIEW",
        "decision": "APPROVED",
        "publication_candidate_path": _rel(repo_root, candidate_path),
        "publication_candidate_sha256": core.sha256_file(candidate_path),
        "pdf_path": candidate["pdf"]["path"],
        "pdf_sha256": candidate["pdf"]["sha256"],
        "page_count": candidate["pdf"]["page_count"],
        "reviewed_by": reviewed_by,
        "reviewed_at": core.iso_utc(reviewed_at),
        "review_reference": review_reference,
    }
    schema_gate.validate_instance(payload, repo_root / PREVIEW_APPROVAL_SCHEMA, label="Publication Preview approval")
    _write_immutable(output_path, payload, "Publication Preview approval")
    return output_path


def validate_preview_approval(repo_root: Path, path: Path, *, issue_id: str | None = None) -> dict[str, Any]:
    approval = schema_gate.load_and_validate_json(path, repo_root / PREVIEW_APPROVAL_SCHEMA, label="Publication Preview approval")
    if issue_id is not None and approval["issue_id"] != issue_id:
        raise ValueError("Publication Preview approval issue_id mismatch")
    candidate_path = _safe_file(repo_root, repo_root / approval["publication_candidate_path"], "Publication Candidate")
    if core.sha256_file(candidate_path) != approval["publication_candidate_sha256"]:
        raise ValueError("Publication Preview approved candidate bytes drifted")
    candidate = validate_candidate(repo_root, candidate_path, issue_id=approval["issue_id"])
    if (
        candidate["pdf"]["path"] != approval["pdf_path"]
        or candidate["pdf"]["sha256"] != approval["pdf_sha256"]
        or candidate["pdf"]["page_count"] != approval["page_count"]
    ):
        raise ValueError("Publication Preview approval does not bind exact candidate PDF")
    return approval


def build_visual_review(
    repo_root: Path,
    approval_path: Path,
    checks: list[dict[str, str]],
    review_tool: str,
    recorded_at: datetime,
    output_path: Path,
) -> Path:
    """Legacy post-approval visual record; retained only for historical compatibility.

    New candidates already bind a pre-preview `publication-review-record-v2` VISUAL
    record. New production must not require this function before Freeze.
    """
    approval = validate_preview_approval(repo_root, approval_path)
    if not checks or any(set(row) != {"check_id", "status", "detail"} or row.get("status") != "PASS" for row in checks):
        raise ValueError("Visual Review requires one or more all-PASS checks")
    if not review_tool.strip():
        raise ValueError("Visual Review review_tool required")
    payload = {
        "schema_version": "2.0-rc1",
        "issue_id": approval["issue_id"],
        "status": "PASSED",
        "publication_preview_approval_path": _rel(repo_root, approval_path),
        "publication_preview_approval_sha256": core.sha256_file(approval_path),
        "pdf_path": approval["pdf_path"],
        "pdf_sha256": approval["pdf_sha256"],
        "page_count": approval["page_count"],
        "checks": checks,
        "review_tool": review_tool,
        "recorded_at": core.iso_utc(recorded_at),
    }
    schema_gate.validate_instance(payload, repo_root / VISUAL_REVIEW_SCHEMA, label="Visual Review record")
    _write_immutable(output_path, payload, "Visual Review record")
    return output_path


def validate_visual_review(repo_root: Path, path: Path, approval_path: Path) -> dict[str, Any]:
    """Validate the legacy post-approval visual record."""
    review = schema_gate.load_and_validate_json(path, repo_root / VISUAL_REVIEW_SCHEMA, label="Visual Review record")
    approval = validate_preview_approval(repo_root, approval_path, issue_id=review["issue_id"])
    if review["publication_preview_approval_path"] != _rel(repo_root, approval_path) or review["publication_preview_approval_sha256"] != core.sha256_file(approval_path):
        raise ValueError("Visual Review does not bind exact Publication Preview approval")
    if review["pdf_path"] != approval["pdf_path"] or review["pdf_sha256"] != approval["pdf_sha256"] or review["page_count"] != approval["page_count"]:
        raise ValueError("Visual Review does not bind exact approved PDF")
    return review


def build_freeze(
    repo_root: Path,
    candidate_path: Path,
    approval_path: Path,
    frozen_at: datetime,
    freeze_path: Path,
    release_manifest_path: Path,
) -> tuple[Path, Path]:
    """Freeze the exact Human-approved candidate and its already-bound visual QA."""
    prep = _prepare_freeze_inputs(repo_root, candidate_path, approval_path)
    candidate = prep["candidate"]
    release_tag = profile_release_identity(prep["profile"])
    freeze_payload = _build_freeze_payload(
        repo_root=repo_root,
        candidate_path=prep["candidate_path"],
        candidate=candidate,
        approval_path=prep["approval_path"],
        approval=prep["approval"],
        visual_path=prep["visual_path"],
        frozen_at=frozen_at,
    )
    source = candidate["source"]
    pdf = candidate["pdf"]
    plan = _preflight_freeze_pair(
        repo_root,
        freeze_path,
        release_manifest_path,
        prep,
        freeze_payload,
        lambda freeze_sha, freeze_target: _build_manifest_payload(
            repo_root=repo_root,
            freeze_path=freeze_target,
            freeze_record_sha256=freeze_sha,
            release_identity=release_tag,
            source_path=source["path"],
            source_sha256=source["sha256"],
            pdf_path=pdf["path"],
            pdf_sha256=pdf["sha256"],
            page_count=pdf["page_count"],
            issue_id=candidate["issue_id"],
        ),
    )
    installed_freeze, installed_manifest = _install_freeze_pair(repo_root, plan)
    validate_release_manifest(repo_root, installed_manifest)
    return installed_freeze, installed_manifest


def validate_release_manifest(repo_root: Path, path: Path) -> dict[str, Any]:
    manifest = schema_gate.load_and_validate_json(path, repo_root / RELEASE_MANIFEST_SCHEMA, label="Release manifest")
    freeze_path = _safe_file(repo_root, repo_root / manifest["freeze_record_path"], "Freeze record")
    if core.sha256_file(freeze_path) != manifest["freeze_record_sha256"]:
        raise ValueError("Release manifest Freeze record SHA drift")
    freeze = schema_gate.load_and_validate_json(freeze_path, repo_root / FREEZE_SCHEMA, label="Freeze record")
    for field in ("source_path", "source_sha256", "pdf_path", "pdf_sha256", "page_count"):
        if manifest[field] != freeze[field]:
            raise ValueError(f"Release manifest diverges from Freeze record: {field}")
    source = _safe_file(repo_root, repo_root / manifest["source_path"], "source_path")
    if core.sha256_file(source) != manifest["source_sha256"]:
        raise ValueError("frozen artifact bytes drift before release: source_path")
    candidate_path = _safe_file(repo_root, repo_root / freeze["publication_candidate_path"], "Publication Candidate")
    if core.sha256_file(candidate_path) != freeze["publication_candidate_sha256"]:
        raise ValueError("Freeze record Publication Candidate SHA drift")
    candidate = validate_candidate(repo_root, candidate_path, issue_id=manifest["issue_id"])
    if (
        candidate["pdf"]["path"] != manifest["pdf_path"]
        or candidate["pdf"]["sha256"] != manifest["pdf_sha256"]
        or candidate["pdf"]["page_count"] != manifest["page_count"]
    ):
        raise ValueError("Release manifest diverges from durable Publication Candidate PDF authority")
    if freeze["visual_review_path"] != candidate["visual_review"]["path"] or freeze["visual_review_sha256"] != candidate["visual_review"]["sha256"]:
        raise ValueError("Freeze record visual review diverges from Publication Candidate authority")
    return manifest


def build_merge_verification(
    repo_root: Path,
    manifest_path: Path,
    merged_commit_sha: str,
    verified_at: datetime,
    output_path: Path,
) -> Path:
    if len(merged_commit_sha) != 40 or any(c not in "0123456789abcdef" for c in merged_commit_sha):
        raise ValueError("merged_commit_sha must be lowercase 40-hex")
    manifest = validate_release_manifest(repo_root, manifest_path)
    payload = {
        "schema_version": "2.0-rc1",
        "issue_id": manifest["issue_id"],
        "status": "VERIFIED",
        "release_manifest_path": _rel(repo_root, manifest_path),
        "release_manifest_sha256": core.sha256_file(manifest_path),
        "merged_commit_sha": merged_commit_sha,
        "source_sha256": manifest["source_sha256"],
        "pdf_sha256": manifest["pdf_sha256"],
        "verified_at": core.iso_utc(verified_at),
    }
    schema_gate.validate_instance(payload, repo_root / MERGE_VERIFICATION_SCHEMA, label="Merge verification")
    _write_immutable(output_path, payload, "Merge verification")
    return output_path


def build_release_record(
    repo_root: Path,
    manifest_path: Path,
    merge_verification_path: Path,
    released_at: datetime,
    release_reference: str,
    output_path: Path,
) -> Path:
    manifest = validate_release_manifest(repo_root, manifest_path)
    verification = schema_gate.load_and_validate_json(
        merge_verification_path, repo_root / MERGE_VERIFICATION_SCHEMA, label="Merge verification"
    )
    if verification["issue_id"] != manifest["issue_id"]:
        raise ValueError("Merge verification issue_id mismatch")
    if verification["release_manifest_path"] != _rel(repo_root, manifest_path) or verification["release_manifest_sha256"] != core.sha256_file(manifest_path):
        raise ValueError("Merge verification does not bind exact Release manifest")
    if verification["source_sha256"] != manifest["source_sha256"] or verification["pdf_sha256"] != manifest["pdf_sha256"]:
        raise ValueError("Merge verification does not bind frozen source/PDF bytes")
    if not release_reference.strip():
        raise ValueError("release_reference required")
    payload = {
        "schema_version": "2.0-rc1",
        "issue_id": manifest["issue_id"],
        "release_identity": manifest["release_identity"],
        "status": "RELEASED",
        "release_manifest_path": _rel(repo_root, manifest_path),
        "release_manifest_sha256": core.sha256_file(manifest_path),
        "merge_verification_path": _rel(repo_root, merge_verification_path),
        "merge_verification_sha256": core.sha256_file(merge_verification_path),
        "pdf_sha256": manifest["pdf_sha256"],
        "released_at": core.iso_utc(released_at),
        "release_reference": release_reference,
    }
    schema_gate.validate_instance(payload, repo_root / RELEASE_RECORD_SCHEMA, label="Release record")
    _write_immutable(output_path, payload, "Release record")
    return output_path


def validate_release_record(repo_root: Path, path: Path) -> dict[str, Any]:
    record = schema_gate.load_and_validate_json(path, repo_root / RELEASE_RECORD_SCHEMA, label="Release record")
    manifest_path = _safe_file(repo_root, repo_root / record["release_manifest_path"], "Release manifest")
    verification_path = _safe_file(repo_root, repo_root / record["merge_verification_path"], "Merge verification")
    if core.sha256_file(manifest_path) != record["release_manifest_sha256"] or core.sha256_file(verification_path) != record["merge_verification_sha256"]:
        raise ValueError("Release record authority bytes drift")
    manifest = validate_release_manifest(repo_root, manifest_path)
    verification = schema_gate.load_and_validate_json(verification_path, repo_root / MERGE_VERIFICATION_SCHEMA, label="Merge verification")
    if record["release_identity"] != manifest["release_identity"] or record["pdf_sha256"] != manifest["pdf_sha256"] or verification["pdf_sha256"] != manifest["pdf_sha256"]:
        raise ValueError("Release record does not bind exact frozen PDF")
    return record
