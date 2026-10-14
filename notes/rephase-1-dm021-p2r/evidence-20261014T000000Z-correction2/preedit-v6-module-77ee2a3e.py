#!/usr/bin/env python3
"""DM021-P2R retention-only capture/readback (one-shot, no promotion).

Correction v2 (R1-R6 + B1-B3): exact dirfd/no-follow raw path protocol,
full finite snapshots, strict historical verifier, typed structured errors,
mandatory one-shot refusal/no cleanup/overwrite.

Two entry points:

  capture_retention(root, state_path, proposal_path) -> result
      Calls unmodified P1 validate_proposal BEFORE writes only (sanitized Git
      env so P1 cannot inherit a conflicting GIT_* route), pins actual HEAD,
      copies old bytes into exclusively claimed retained/ root, publishes
      manifest last. Existing retained root refuses (including empty/same-byte
      foreign). No overwrite/retry/adopt/cleanup. Live originals never mutated.

  verify_retention(root, proposal_path, manifest_path) -> result
      Standalone read-only retained-set verification. Never calls P1, never
      calls Git/current HEAD/config authority, never requires mutable live
      COPY originals or current eligibility. Exact proposal -> retained State
      COPY -> State.profile -> matching KEEP Profile -> canonical namespace.

All refusals raise RetentionError (ValueError) with structured
code/phase/disposition/detail/owned/cause. No CLI, no State adoption,
no reason enum, no review production. No assert guards (explicit raises;
safe under python -O).

Note on edits: no `apply_patch` binary in this environment; module/test
fixes applied via exact file-write/exact-string replacement with identical
semantics (disclosed in correction report).
"""
from __future__ import annotations

import contextlib
import json
import os
import stat as _stat
import subprocess
from pathlib import Path
from typing import Any

from scripts import survey_production_v2 as core
from scripts import survey_schema_v2 as schema_gate

PROPOSAL_SCHEMA = Path("schemas/editorial-correction-proposal-v2.schema.json")
MANIFEST_SCHEMA = Path("schemas/editorial-retention-manifest-v2.schema.json")
P2R_MODULE = Path("scripts/survey_editorial_retention_v2.py")
RESULT_CAPTURED = "RETAINED_SET_CAPTURED"
RESULT_VERIFIED = "RETAINED_SET_VERIFIED"
MANIFEST_FILENAME = "retention-manifest.json"
PROPOSAL_FILENAME = "proposal.json"

_TOP_ORDER = ["schema_version", "kind", "status", "proposal_ref", "basis", "proposed", "rows", "capture_inputs"]
_REF_ORDER = ["path", "sha256"]
_PROPOSAL_REF_ORDER = ["path", "sha256", "proposal_id", "issue_id", "research_profile", "publication_profile"]
_BASIS_ORDER = ["state_ref", "validation_checkpoint_ref", "active_revalidation_ref", "active_reader_input_ref",
                "before_graph_digest", "preserved_upstream_digest", "generated_receipt_ref",
                "renderer_commit", "contract_identity"]
_CONTRACT_ORDER = ["pipeline_contract_version", "pipeline_contract_sha256", "quality_contract_version",
                   "quality_contract_sha256", "research_profile_version", "research_profile_sha256",
                   "publication_profile_version", "publication_profile_sha256"]
_PROPOSED_ORDER = ["authoring_input_ref", "proposed_reader_ref", "proposed_reader_canonical_sha256", "change_description"]
_ROW_COPY_ORDER = ["roles", "path", "sha256", "byte_count", "policy", "retained_dest", "retained_sha256", "retained_byte_count"]
_ROW_KEEP_ORDER = ["roles", "path", "sha256", "byte_count", "policy", "retained_ref"]

_GIT_UNSAFE_VARS = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_PREFIX")


class RetentionError(ValueError):
    """Typed retention refusal with structured fields."""

    def __init__(self, code: str, phase: str, disposition: str, detail: str,
                 owned: dict[str, Any] | None = None, cause: BaseException | None = None) -> None:
        super().__init__(f"{code}: [{phase}/{disposition}] {detail}")
        self.code = code
        self.phase = phase
        self.disposition = disposition
        self.detail = detail
        self.owned: dict[str, Any] = owned if owned is not None else {}
        if cause is not None:
            self.__cause__ = cause


def _fail(code: str, phase: str, disposition: str, detail: str,
          owned: dict[str, Any] | None = None, cause: BaseException | None = None) -> RetentionError:
    return RetentionError(code, phase, disposition, detail, owned, cause)


def _raw_segments(raw: str) -> list[str]:
    # Raw split on "/" only. Never use Path.parts here: Path normalizes away
    # single-dot segments ("a/./b" -> ("a","b")) and would hide them.
    return raw.split("/")


def _lexical_rel(value: str | Path, label: str, phase: str, disp: str) -> str:
    """Validate a repo-relative path lexically WITHOUT resolving aliases.

    Rejects backslashes, absolute paths, empty paths, "//" empty segments,
    trailing slashes, and any "", ".", ".." segment. Returns the raw string
    unchanged when valid. No filesystem access, no symlink resolution, so a
    contained alias can never be erased before NOFOLLOW checks.
    """
    raw = value.as_posix() if isinstance(value, Path) else str(value)
    if "\x00" in raw:
        raise _fail("PATH_TRAVERSAL", phase, disp, f"{label} contains NUL: {raw!r}")
    if "\\" in raw:
        raise _fail("PATH_TRAVERSAL", phase, disp, f"{label} must not contain backslashes: {raw}")
    if not raw or raw in (".", "./"):
        raise _fail("PATH_TRAVERSAL", phase, disp, f"{label} is empty: {raw}")
    if raw.startswith("/"):
        raise _fail("PATH_NOT_REPO_LOCAL", phase, disp, f"{label} must be repo-relative: {raw}")
    if "//" in raw:
        raise _fail("PATH_TRAVERSAL", phase, disp, f"{label} has empty segment: {raw}")
    if raw.endswith("/"):
        raise _fail("PATH_TRAVERSAL", phase, disp, f"{label} has trailing separator: {raw}")
    for part in _raw_segments(raw):
        if part in ("", ".", ".."):
            raise _fail("PATH_TRAVERSAL", phase, disp, f"{label} has unsafe component: {raw}")
    return raw


def _check_lexical_path(rel: str, label: str, phase: str, disp: str) -> None:
    _lexical_rel(rel, label, phase, disp)


def _to_rel(root_resolved: Path, value: str | Path, label: str, phase: str, disp: str) -> str:
    """Accept repo-relative or absolute-inside-root paths; return repo rel.

    Absolute inputs must still be inside the held root (lexical prefix check
    before any resolution); containment is re-enforced by dirfd traversal.
    Raw segments are validated without resolving aliases away.
    """
    raw = value.as_posix() if isinstance(value, Path) else str(value)
    if "\x00" in raw:
        raise _fail("PATH_TRAVERSAL", phase, disp, f"{label} contains NUL: {raw!r}")
    if Path(raw).is_absolute():
        rroot = root_resolved.as_posix()
        if raw != rroot and not raw.startswith(rroot + "/"):
            raise _fail("PATH_NOT_REPO_LOCAL", phase, disp, f"{label} escapes repository: {raw}")
        if raw == rroot:
            raise _fail("PATH_TRAVERSAL", phase, disp, f"{label} is the repository root: {raw}")
        rel = raw[len(rroot) + 1:]
        return _lexical_rel(rel, label, phase, disp)
    return _lexical_rel(raw, label, phase, disp)


def _parse_json_strict(data: bytes, label: str, phase: str, disp: str, unreadable_code: str) -> Any:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _fail(unreadable_code, phase, disp, f"{label} bytes are not UTF-8: {exc}") from exc

    def _hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        seen: set[str] = set()
        out: dict[str, Any] = {}
        for k, v in pairs:
            if k in seen:
                raise _fail("DUPLICATE_KEY", phase, disp, f"{label} has duplicate key: {k}")
            seen.add(k)
            out[k] = v
        return out

    try:
        return json.loads(text, object_pairs_hook=_hook)
    except RetentionError:
        raise
    except ValueError as exc:
        raise _fail(unreadable_code, phase, disp, f"{label} is not JSON: {exc}") from exc


def _loads_strict(data: bytes, label: str, phase: str, disp: str) -> Any:
    code = "MANIFEST_UNREADABLE" if "manifest" in label.lower() else "PROPOSAL_UNREADABLE"
    return _parse_json_strict(data, label, phase, disp, code)


class _Session:
    """Dirfd-relative no-follow safe reader; capture subclass adds writers.

    Holds root dir fd open during invocation; every file/dir accessed
    relative to a pinned parent fd with O_NOFOLLOW|O_NONBLOCK. All fds
    (including directory fds) are closed before successful return; close
    errors fail even when bytes are complete. Entry identities (dev/ino via
    lstat from pinned parent) are compared against fd identities so a
    same-byte pathname replacement cannot evade byte-only readback.
    Root itself must be a real directory (symlink root refuses).
    """

    def __init__(self, root: str | Path) -> None:
        raw = str(root)
        # Explicit root handling: refuse symlink root before open.
        try:
            lst = os.lstat(raw)
        except OSError as exc:
            raise _fail("PATH_UNREADABLE", "PRE_P1_PIN", "REFUSED_PRE_WRITE",
                        f"cannot lstat repo root: {exc}") from exc
        if _stat.S_ISLNK(lst.st_mode):
            raise _fail("PATH_ALIAS", "PRE_P1_PIN", "REFUSED_PRE_WRITE", "repo root is a symlink")
        if not _stat.S_ISDIR(lst.st_mode):
            raise _fail("PATH_NOT_REGULAR", "PRE_P1_PIN", "REFUSED_PRE_WRITE", "repo root is not a directory")
        self.root_resolved = Path(raw).resolve()
        try:
            self.root_fd = os.open(self.root_resolved, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0))
        except OSError as exc:
            raise _fail("PATH_UNREADABLE", "PRE_P1_PIN", "REFUSED_PRE_WRITE", f"cannot open repo root: {exc}") from exc
        try:
            st = os.fstat(self.root_fd)
        except OSError as exc:
            try:
                os.close(self.root_fd)
            except OSError:
                pass
            raise _fail("PATH_UNREADABLE", "PRE_P1_PIN", "REFUSED_PRE_WRITE", f"cannot fstat repo root: {exc}") from exc
        if not _stat.S_ISDIR(st.st_mode):
            try:
                os.close(self.root_fd)
            except OSError:
                pass
            raise _fail("PATH_NOT_REGULAR", "PRE_P1_PIN", "REFUSED_PRE_WRITE", "repo root is not a directory")
        # Entry-vs-fd binding for root: lstat entry must match opened fd.
        if (lst.st_dev, lst.st_ino) != (st.st_dev, st.st_ino):
            try:
                os.close(self.root_fd)
            except OSError:
                pass
            raise _fail("ROOT_IDENTITY_CHANGED", "PRE_P1_PIN", "REFUSED_PRE_WRITE",
                        "repo root replaced between lstat and open")
        self.root_id = (st.st_dev, st.st_ino, _stat.S_IMODE(st.st_mode))
        self.files: dict[str, bytes] = {}
        self.file_ids: dict[str, tuple[int, int, int]] = {}
        self.dir_ids: dict[str, tuple[int, int, int]] = {".": self.root_id}
        self._open_fds: list[int] = [self.root_fd]
        self._closed = False

    def _close_checked(self, fd: int, label: str, phase: str, disp: str) -> None:
        # Intermediate close that FAILS on error (never quiet success).
        try:
            os.close(fd)
        except OSError as exc:
            raise _fail("CLOSE_FAILED", phase, disp, f"{label} close failed: {exc}") from exc
        finally:
            if fd in self._open_fds:
                self._open_fds.remove(fd)

    def _close_all(self, phase: str, disp: str, prior: BaseException | None = None) -> None:
        # Close every held fd; preserve prior error, attach ALL secondary
        # close failures (no silent leak/success).
        first: BaseException | None = prior
        secondaries: list[str] = []
        for fd in reversed(list(self._open_fds)):
            try:
                os.close(fd)
            except OSError as exc:
                if first is None:
                    first = _fail("CLOSE_FAILED", phase, disp, f"descriptor close failed: {exc}", cause=exc)
                else:
                    secondaries.append(str(exc))
            finally:
                if fd in self._open_fds:
                    try:
                        self._open_fds.remove(fd)
                    except ValueError:
                        pass
        self._open_fds = []
        self._closed = True
        if first is not None and prior is None:
            if secondaries and isinstance(first, RetentionError):
                first.detail = first.detail + f"; secondary closes: {secondaries}"
                first.args = (f"{first.code}: [{first.phase}/{first.disposition}] {first.detail}",)
            raise first
        if first is not None and prior is not None and secondaries and isinstance(prior, RetentionError):
            # Attach secondary close context to the primary owned report via cause chain note.
            # Caller copies these into owned["secondary_close_errors"].
            pass

    def _split(self, rel: str) -> tuple[list[str], str]:
        parts = _raw_segments(rel)
        if len(parts) == 0 or any(p in ("", ".", "..") for p in parts):
            raise _fail("PATH_TRAVERSAL", "PRE_P1_PIN", "REFUSED_PRE_WRITE", f"empty/unsafe path: {rel}")
        return parts[:-1], parts[-1]

    def _open_dir_chain(self, dir_parts: list[str], label: str, phase: str, disp: str) -> int:
        # Open each ancestor relative to parent with NOFOLLOW; return deepest fd.
        # Pins (dev,ino,mode) per ancestor; re-entry compares and refuses on
        # replacement. Entry identity (lstat from parent) must match fd fstat
        # so a swapped directory cannot hide behind a held fd.
        parent = self.root_fd
        cur_parts: list[str] = []
        for part in dir_parts:
            if part in ("", ".", ".."):
                raise _fail("PATH_TRAVERSAL", phase, disp, f"{label} has unsafe ancestor: {part}")
            cur_parts.append(part)
            try:
                fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
                             | getattr(os, "O_NONBLOCK", 0), dir_fd=parent)
            except FileNotFoundError as exc:
                raise _fail("PATH_MISSING", phase, disp, f"{label} ancestor missing: {'/'.join(cur_parts)}: {exc}") from exc
            except OSError as exc:
                raise _fail("PATH_ALIAS", phase, disp, f"{label} ancestor not openable as dir (symlink?): {'/'.join(cur_parts)}: {exc}") from exc
            try:
                st = os.fstat(fd)
            except OSError as exc:
                try:
                    os.close(fd)
                except OSError:
                    pass
                raise _fail("PATH_UNREADABLE", phase, disp, f"{label} ancestor fstat failed: {'/'.join(cur_parts)}: {exc}") from exc
            if not _stat.S_ISDIR(st.st_mode):
                try:
                    os.close(fd)
                except OSError:
                    pass
                raise _fail("PATH_NOT_REGULAR", phase, disp, f"{label} ancestor not a directory: {'/'.join(cur_parts)}")
            # Entry identity from pinned parent must match the opened fd.
            try:
                est = os.stat(part, dir_fd=parent, follow_symlinks=False)
            except OSError as exc:
                try:
                    os.close(fd)
                except OSError:
                    pass
                raise _fail("PATH_UNREADABLE", phase, disp, f"{label} ancestor entry unreadable: {'/'.join(cur_parts)}: {exc}") from exc
            if (est.st_dev, est.st_ino) != (st.st_dev, st.st_ino):
                try:
                    os.close(fd)
                except OSError:
                    pass
                raise _fail("ANCESTOR_REPLACED", phase, disp,
                            f"{label} ancestor replaced during open: {'/'.join(cur_parts)}")
            if _stat.S_ISLNK(est.st_mode):
                try:
                    os.close(fd)
                except OSError:
                    pass
                raise _fail("PATH_ALIAS", phase, disp, f"{label} ancestor is symlink: {'/'.join(cur_parts)}")
            rel = "/".join(cur_parts)
            pinned = self.dir_ids.get(rel)
            cur_id = (st.st_dev, st.st_ino, _stat.S_IMODE(st.st_mode))
            if pinned is not None and pinned != cur_id:
                try:
                    os.close(fd)
                except OSError:
                    pass
                raise _fail("ANCESTOR_REPLACED", phase, disp,
                            f"{label} ancestor identity changed: {rel}")
            self._open_fds.append(fd)
            if pinned is None:
                self.dir_ids[rel] = cur_id
            parent = fd
        return parent

    def _entry_identity(self, parent_fd: int, name: str, label: str, phase: str, disp: str) -> tuple[int, int, int, int]:
        # Current name entry from pinned parent fd (detects pathname replacement
        # even when a held fd's fstat is unchanged). Returns (dev,ino,mode,is_symlink).
        if name in ("", ".", ".."):
            raise _fail("PATH_TRAVERSAL", phase, disp, f"{label} has unsafe leaf: {name}")
        try:
            st = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError as exc:
            raise _fail("PATH_MISSING", phase, disp, f"{label} entry missing: {name}: {exc}") from exc
        except OSError as exc:
            raise _fail("PATH_UNREADABLE", phase, disp, f"{label} entry unreadable: {name}: {exc}") from exc
        is_link = 1 if _stat.S_ISLNK(st.st_mode) else 0
        return (st.st_dev, st.st_ino, st.st_mode, is_link)

    def safe_read(self, value: str | Path, label: str, phase: str = "PRE_P1_PIN",
                  disp: str = "REFUSED_PRE_WRITE") -> tuple[str, bytes]:
        rel = _to_rel(self.root_resolved, value, label, phase, disp)
        dir_parts, leaf = self._split(rel)
        mark = len(self._open_fds)
        added: list[int] = []
        try:
            parent = self._open_dir_chain(dir_parts, label, phase, disp) if dir_parts else self.root_fd
            # Track newly opened ancestor fds for checked close below.
            added = self._open_fds[mark:]
            # Refuse symlinked leaf before open (no-follow open also refuses).
            ent = self._entry_identity(parent, leaf, label, phase, disp)
            if ent[3] == 1:
                raise _fail("PATH_ALIAS", phase, disp, f"{label} is a symlink: {rel}")
            if not _stat.S_ISREG(ent[2]):
                raise _fail("PATH_NOT_REGULAR", phase, disp, f"{label} not a regular file: {rel}")
            try:
                fd = os.open(leaf, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0),
                             dir_fd=parent)
            except OSError as exc:
                raise _fail("PATH_ALIAS", phase, disp, f"{label} cannot be opened no-follow (symlink?): {rel}: {exc}") from exc
            self._open_fds.append(fd)
            added = self._open_fds[mark:]
            try:
                st = os.fstat(fd)
            except OSError as exc:
                raise _fail("PATH_UNREADABLE", phase, disp, f"{label} fstat failed: {rel}: {exc}") from exc
            if not _stat.S_ISREG(st.st_mode):
                raise _fail("PATH_NOT_REGULAR", phase, disp, f"{label} not regular after open: {rel}")
            # Entry-vs-fd binding: pathname replacement with same bytes must not pass.
            if (st.st_dev, st.st_ino) != (ent[0], ent[1]):
                raise _fail("FILE_REPLACED", phase, disp, f"{label} replaced between entry check and open: {rel}")
            # Pinned-identity recheck: a re-read that finds a different file
            # (even with equal bytes) is a replacement, not stability.
            pinned = self.file_ids.get(rel)
            if pinned is not None and (pinned[0], pinned[1]) != (st.st_dev, st.st_ino):
                raise _fail("FILE_REPLACED", phase, disp, f"{label} file identity changed: {rel}")
            chunks: list[bytes] = []
            while True:
                try:
                    blk = os.read(fd, 65536)
                except OSError as exc:
                    raise _fail("PATH_UNREADABLE", phase, disp, f"{label} read failed: {rel}: {exc}") from exc
                if not blk:
                    break
                chunks.append(blk)
            data = b"".join(chunks)
            try:
                os.close(fd)
            except OSError as exc:
                raise _fail("CLOSE_FAILED", phase, disp, f"{label} close after read failed: {rel}: {exc}") from exc
            finally:
                if fd in self._open_fds:
                    self._open_fds.remove(fd)
                added = self._open_fds[mark:]
            self.file_ids[rel] = (st.st_dev, st.st_ino, len(data))
            prev = self.files.get(rel)
            if prev is not None and prev != data:
                raise _fail("STABILITY_VIOLATION", phase, disp, f"{label} changed mid-inspection: {rel}")
            self.files[rel] = data
            return rel, data
        finally:
            # Checked close of intermediate ancestor fds: failures FAIL.
            while len(self._open_fds) > mark:
                extra = self._open_fds.pop()
                if extra != self.root_fd:
                    try:
                        os.close(extra)
                    except OSError as exc:
                        raise _fail("CLOSE_FAILED", phase, disp,
                                    f"{label} intermediate dir close failed: {rel}: {exc}") from exc

    def repinned(self, ref: dict[str, Any], label: str, phase: str, disp: str,
                 expected_size: int | None = None) -> str:
        if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
            raise _fail("REF_SHAPE", phase, disp, f"{label} is not an exact {{path,sha256}} record")
        if not isinstance(ref["path"], str) or not isinstance(ref["sha256"], str) or len(ref["sha256"]) != 64:
            raise _fail("REF_SHAPE", phase, disp, f"{label} has invalid path/sha256")
        rel, data = self.safe_read(ref["path"], label, phase, disp)
        if core.sha256_bytes(data) != ref["sha256"]:
            raise _fail("REF_DRIFT", phase, disp, f"{label} bytes differ from recorded sha256: {rel}")
        if expected_size is not None and len(data) != expected_size:
            raise _fail("REF_SIZE_MISMATCH", phase, disp,
                        f"{label} size {len(data)} != recorded {expected_size}: {rel}")
        return rel

    def reverify(self, phase: str, disp: str) -> None:
        for rel, data in list(self.files.items()):
            _check_lexical_path(rel, "consumed file", phase, disp)
            dir_parts, leaf = self._split(rel)
            mark = len(self._open_fds)
            try:
                parent = self._open_dir_chain(dir_parts, label="consumed ancestor", phase=phase, disp=disp) if dir_parts else self.root_fd
                ent = self._entry_identity(parent, leaf, "consumed file", phase, disp)
                if ent[3] == 1:
                    raise _fail("PATH_ALIAS", phase, disp, f"consumed file became symlink: {rel}")
                if not _stat.S_ISREG(ent[2]):
                    raise _fail("PATH_NOT_REGULAR", phase, disp, f"consumed file not regular: {rel}")
                rel2, live = self.safe_read(rel, "consumed file recheck", phase, disp)
                if live != data:
                    raise _fail("STABILITY_VIOLATION", phase, disp, f"consumed file changed: {rel}")
            finally:
                while len(self._open_fds) > mark:
                    extra = self._open_fds.pop()
                    if extra != self.root_fd:
                        try:
                            os.close(extra)
                        except OSError as exc:
                            raise _fail("CLOSE_FAILED", phase, disp,
                                        f"consumed reverify close failed: {rel}: {exc}") from exc


def _validate_roles_sorted_unique(roles: Any, label: str, phase: str, disp: str) -> None:
    if not isinstance(roles, list) or len(roles) == 0 or not all(isinstance(r, str) and r for r in roles):
        raise _fail("RETENTION_MISMATCH", phase, disp, f"{label} roles must be nonempty string list")
    if roles != sorted(roles):
        raise _fail("RETENTION_ORDER_MISMATCH", phase, disp, f"{label} roles not sorted-unique")
    if len(set(roles)) != len(roles):
        raise _fail("RETENTION_MISMATCH", phase, disp, f"{label} roles have duplicates")


def _ordered_ref(ref: dict[str, Any], phase: str, disp: str) -> dict[str, Any]:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
        raise _fail("RETENTION_MISMATCH", phase, disp, "ref is not exact {path,sha256}")
    return {"path": ref["path"], "sha256": ref["sha256"]}


def _project_manifest_canonical(manifest: dict[str, Any], phase: str, disp: str) -> dict[str, Any]:
    # Deterministic key-order projector for canonical-byte check ONLY.
    # Never accepts omitted/extra data (schema + equality checks run first).
    # Every nested ref is rebuilt in fixed order (no silent normalization of
    # claims: equality checks precede this projector).
    try:
        out: dict[str, Any] = {}
        for k in _TOP_ORDER:
            out[k] = manifest[k]
        pr: dict[str, Any] = {}
        for k in _PROPOSAL_REF_ORDER:
            pr[k] = manifest["proposal_ref"][k]
        out["proposal_ref"] = pr
        basis: dict[str, Any] = {}
        for k in _BASIS_ORDER:
            if k == "contract_identity":
                continue
            v = manifest["basis"][k]
            if k in ("state_ref", "validation_checkpoint_ref", "active_reader_input_ref",
                     "generated_receipt_ref") or (k == "active_revalidation_ref" and isinstance(v, dict)):
                basis[k] = _ordered_ref(v, phase, disp)
            else:
                basis[k] = v
        ci = manifest["basis"]["contract_identity"]
        cio: dict[str, Any] = {}
        for k in _CONTRACT_ORDER:
            cio[k] = ci[k]
        basis["contract_identity"] = cio
        out["basis"] = basis
        prop: dict[str, Any] = {}
        for k in _PROPOSED_ORDER:
            v = manifest["proposed"][k]
            if k in ("authoring_input_ref", "proposed_reader_ref"):
                prop[k] = _ordered_ref(v, phase, disp)
            else:
                prop[k] = v
        out["proposed"] = prop
        rows: list[dict[str, Any]] = []
        for row in manifest["rows"]:
            order = _ROW_COPY_ORDER if row.get("policy") == "COPY_BEFORE_REPLACEMENT" else _ROW_KEEP_ORDER
            r: dict[str, Any] = {}
            for k in order:
                v = row[k]
                if k == "retained_ref":
                    r[k] = _ordered_ref(v, phase, disp)
                else:
                    r[k] = v
            rows.append(r)
        out["rows"] = rows
        out["capture_inputs"] = [_ordered_ref(e, phase, disp) for e in manifest["capture_inputs"]]
        return out
    except KeyError as exc:
        raise _fail("RETENTION_MISMATCH", phase, disp, f"manifest missing canonical key: {exc}") from exc


def _check_canonical_bytes(manifest: dict[str, Any], raw: bytes, phase: str, disp: str) -> None:
    projected = _project_manifest_canonical(manifest, phase, disp)
    canonical = core.json_bytes(projected)
    if canonical != raw:
        raise _fail("MANIFEST_NONCANONICAL", phase, disp, "manifest bytes are not canonical key-order/whitespace (json_bytes)")


def _control_paths(cfg: dict[str, Any], phase: str, disp: str) -> list[str]:
    try:
        roots = cfg["implementation_control_roots"]
        contracts = cfg["contract_files"]
    except (KeyError, TypeError) as exc:
        raise _fail("CONFIG_UNREADABLE", phase, disp, f"config lacks control roots/contract files: {exc}") from exc
    if not isinstance(roots, list) or not all(isinstance(r, str) for r in roots):
        raise _fail("CONFIG_UNREADABLE", phase, disp, "implementation_control_roots invalid")
    style = "templates/survey/jgaisurvey.sty"
    paths: set[str] = {core.DEFAULT_CONFIG.as_posix(), style}
    for r in roots:
        _check_lexical_path(r, "control root", phase, disp)
        paths.add(r)
    if not isinstance(contracts, dict):
        raise _fail("CONFIG_UNREADABLE", phase, disp, "contract_files invalid")
    for rows in contracts.values():
        if not isinstance(rows, list):
            raise _fail("CONFIG_UNREADABLE", phase, disp, "contract_files row invalid")
        for p in rows:
            if not isinstance(p, str):
                raise _fail("CONFIG_UNREADABLE", phase, disp, "contract_files entry invalid")
            _check_lexical_path(p, "contract file", phase, disp)
            paths.add(p)
    return sorted(paths)


def _sanitized_git_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    return env


@contextlib.contextmanager
def _sanitized_git_env_ctx():
    saved = dict(os.environ)
    try:
        for k in list(os.environ):
            if k.startswith("GIT_"):
                del os.environ[k]
        os.environ["GIT_NO_LAZY_FETCH"] = "1"
        os.environ["GIT_OPTIONAL_LOCKS"] = "0"
        os.environ["GIT_ALLOW_PROTOCOL"] = "file"
        yield
    finally:
        os.environ.clear()
        os.environ.update(saved)


def _git_head(root: Path, label: str, phase: str, disp: str) -> str:
    # Checked sanitized Git HEAD pin (no inherited GIT_* route). Verifier never calls this.
    try:
        proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True,
                              env=_sanitized_git_env(), timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        raise _fail("GIT_UNAVAILABLE", phase, disp, f"{label} git rev-parse failed: {exc}") from exc
    if proc.returncode != 0:
        raise _fail("GIT_UNAVAILABLE", phase, disp,
                    f"{label} git rev-parse rc={proc.returncode}: {proc.stderr.strip()}")
    value = proc.stdout.strip()
    if len(value) != 40 or any(c not in "0123456789abcdef" for c in value):
        raise _fail("GIT_UNAVAILABLE", phase, disp, f"{label} HEAD not 40-hex: {value!r}")
    return value


def _walk_onerror(exc: OSError, kind: str, phase: str, disp: str) -> None:
    raise _fail("PATH_UNREADABLE", phase, disp, f"{kind} walk failed: {exc}") from exc


def _snapshot_expanded(session: _Session, rels_or_roots: list[str], kind: str,
                       phase: str, disp: str) -> tuple[dict[str, str], dict[str, str], dict[str, int]]:
    # Strict snapshot: regular file hashes + directory inventory (incl. empty
    # dirs) + file sizes. Fails on every walk/stat error. No resolve() anywhere:
    # lexical paths + lstat only, so aliases are never erased.
    # Returns (files: rel->sha, dirs: rel->mode-octal, sizes: rel->bytes).
    files: dict[str, str] = {}
    dirs: dict[str, str] = {}
    sizes: dict[str, int] = {}
    for base in rels_or_roots:
        _check_lexical_path(base, f"{kind} base", phase, disp)
        full = session.root_resolved / base
        try:
            st = os.lstat(full)
        except OSError as exc:
            raise _fail("TREE_MISSING", phase, disp, f"{kind} base missing: {base}: {exc}") from exc
        if _stat.S_ISLNK(st.st_mode):
            raise _fail("TREE_ALIAS", phase, disp, f"{kind} base is symlink: {base}")
        if _stat.S_ISDIR(st.st_mode):
            def _onerror(exc: OSError) -> None:
                _walk_onerror(exc, kind, phase, disp)
            for dirpath, dirnames, filenames in os.walk(full, topdown=True, followlinks=False, onerror=_onerror):
                # Lexical rel (walk yields lexical paths; never resolve).
                try:
                    rel_dir = Path(dirpath).relative_to(session.root_resolved).as_posix()
                except ValueError:
                    raise _fail("PATH_NOT_REPO_LOCAL", phase, disp, f"{kind} tree escapes root: {dirpath}") from None
                if rel_dir == ".":
                    rel_dir = base if base != "." else "."
                    # Record base dir itself with its actual lstat mode.
                    dirs[base] = f"DIR:{oct(_stat.S_IMODE(st.st_mode))}"
                # Per-entry dir checks with actual lstat modes (not base mode).
                for d in sorted(list(dirnames)):
                    fp = Path(dirpath) / d
                    try:
                        lst = os.lstat(fp)
                    except OSError as exc:
                        raise _fail("PATH_UNREADABLE", phase, disp, f"{kind} dir unreadable: {fp}: {exc}") from exc
                    if _stat.S_ISLNK(lst.st_mode):
                        raise _fail("TREE_ALIAS", phase, disp, f"symlink directory inside {kind} tree: {rel_dir}/{d}")
                    if not _stat.S_ISDIR(lst.st_mode):
                        raise _fail("TREE_NOT_DIR", phase, disp, f"non-directory inside {kind} tree: {fp}")
                    if d == ".git":
                        dirnames.remove(d)
                        continue
                    child_rel = (rel_dir + "/" + d).replace("//", "/") if rel_dir != "." else d
                    # Normalize base-relative: dirpath is under base, so child_rel
                    # computed from rel_dir is already repo-relative.
                    dirs[child_rel] = f"DIR:{oct(_stat.S_IMODE(lst.st_mode))}"
                if ".git" in dirnames:
                    dirnames.remove(".git")
                if rel_dir != "." and rel_dir not in dirs:
                    # Intermediate dir itself (from walk): lstat for actual mode.
                    try:
                        dlst = os.lstat(Path(dirpath))
                    except OSError as exc:
                        raise _fail("PATH_UNREADABLE", phase, disp, f"{kind} dir unreadable: {dirpath}: {exc}") from exc
                    dirs[rel_dir] = f"DIR:{oct(_stat.S_IMODE(dlst.st_mode))}"
                for name in filenames:
                    fp = Path(dirpath) / name
                    try:
                        lst = os.lstat(fp)
                    except OSError as exc:
                        raise _fail("PATH_UNREADABLE", phase, disp, f"{kind} file unreadable: {fp}: {exc}") from exc
                    if _stat.S_ISLNK(lst.st_mode):
                        try:
                            rel = Path(fp).relative_to(session.root_resolved).as_posix()
                        except ValueError:
                            rel = str(fp)
                        raise _fail("TREE_ALIAS", phase, disp, f"symlink inside {kind} tree: {rel}")
                    if not _stat.S_ISREG(lst.st_mode):
                        try:
                            rel = Path(fp).relative_to(session.root_resolved).as_posix()
                        except ValueError:
                            rel = str(fp)
                        raise _fail("TREE_NOT_REGULAR", phase, disp, f"non-regular file inside {kind} tree: {rel}")
                    try:
                        rel = Path(fp).relative_to(session.root_resolved).as_posix()
                    except ValueError:
                        raise _fail("PATH_NOT_REPO_LOCAL", phase, disp, f"{kind} file escapes root: {fp}") from None
                    _rel, data = session.safe_read(rel, f"{kind} file", phase, disp)
                    files[_rel] = core.sha256_bytes(data)
                    sizes[_rel] = len(data)
        elif _stat.S_ISREG(st.st_mode):
            _rel, data = session.safe_read(base, f"{kind} file", phase, disp)
            files[_rel] = core.sha256_bytes(data)
            sizes[_rel] = len(data)
        else:
            raise _fail("TREE_NOT_REGULAR", phase, disp, f"{kind} base not regular/dir: {base}")
    return files, dirs, sizes


def _retained_inventory(session: _Session, retained_rel: str, phase: str, disp: str) -> tuple[dict[str, str], dict[str, str], dict[str, int]]:
    # Full inventory below retained/ (files + dirs incl. empty, no-follow, no resolve).
    _check_lexical_path(retained_rel, "retained root", phase, disp)
    full = session.root_resolved / retained_rel
    try:
        lst = os.lstat(full)
    except OSError as exc:
        raise _fail("INCOMPLETE_RETENTION", phase, disp, f"retained root missing: {retained_rel}: {exc}") from exc
    if _stat.S_ISLNK(lst.st_mode) or not _stat.S_ISDIR(lst.st_mode):
        raise _fail("INVALID_RETENTION", phase, disp, f"retained root not a directory: {retained_rel}")
    files: dict[str, str] = {}
    dirs: dict[str, str] = {}
    sizes: dict[str, int] = {}
    dirs[retained_rel] = f"DIR:{oct(_stat.S_IMODE(lst.st_mode))}"

    def _onerror(exc: OSError) -> None:
        raise _fail("PATH_UNREADABLE", phase, disp, f"retained walk failed: {exc}") from exc

    for dirpath, dirnames, filenames in os.walk(full, topdown=True, followlinks=False, onerror=_onerror):
        try:
            rel_dir = Path(dirpath).relative_to(session.root_resolved).as_posix()
        except ValueError:
            raise _fail("PATH_NOT_REPO_LOCAL", phase, disp, "retained tree escapes root") from None
        for d in sorted(list(dirnames)):
            fp = Path(dirpath) / d
            try:
                lst_d = os.lstat(fp)
            except OSError as exc:
                raise _fail("PATH_UNREADABLE", phase, disp, f"retained dir unreadable: {fp}: {exc}") from exc
            if _stat.S_ISLNK(lst_d.st_mode):
                raise _fail("INVALID_RETENTION", phase, disp, f"unexpected alias below retained/: {rel_dir}/{d}")
            if not _stat.S_ISDIR(lst_d.st_mode):
                raise _fail("INVALID_RETENTION", phase, disp, f"unexpected non-dir below retained/: {rel_dir}/{d}")
            child = (rel_dir + "/" + d).replace("//", "/")
            dirs[child] = f"DIR:{oct(_stat.S_IMODE(lst_d.st_mode))}"
        if rel_dir not in dirs:
            try:
                dlst = os.lstat(Path(dirpath))
            except OSError as exc:
                raise _fail("PATH_UNREADABLE", phase, disp, f"retained dir unreadable: {dirpath}: {exc}") from exc
            dirs[rel_dir] = f"DIR:{oct(_stat.S_IMODE(dlst.st_mode))}"
        for name in filenames:
            fp = Path(dirpath) / name
            try:
                rel = Path(fp).relative_to(session.root_resolved).as_posix()
            except ValueError:
                raise _fail("PATH_NOT_REPO_LOCAL", phase, disp, "retained file escapes root") from None
            try:
                lst2 = os.lstat(fp)
            except OSError as exc:
                raise _fail("PATH_UNREADABLE", phase, disp, f"retained file unreadable: {rel}: {exc}") from exc
            if _stat.S_ISLNK(lst2.st_mode):
                raise _fail("INVALID_RETENTION", phase, disp, f"unexpected alias below retained/: {rel}")
            if not _stat.S_ISREG(lst2.st_mode):
                raise _fail("INVALID_RETENTION", phase, disp, f"unexpected special below retained/: {rel}")
            _rel, data = session.safe_read(rel, "retained file", phase, disp)
            files[_rel] = core.sha256_bytes(data)
            sizes[_rel] = len(data)
    return files, dirs, sizes


def _validate_proposal_shape(proposal: Any, phase: str, disp: str) -> None:
    if not isinstance(proposal, dict):
        raise _fail("PROPOSAL_UNREADABLE", phase, disp, "proposal is not a JSON object")


def _expected_retained_dest(proposal_dir: str, original_path: str) -> str:
    return (proposal_dir + "/retained/before/" + original_path).replace("//", "/")


def capture_retention(root: str | Path, state_path: str | Path, proposal_path: str | Path) -> dict[str, Any]:
    """One-shot retention capture. See module docstring."""
    from scripts import survey_editorial_correction_proposal_v2 as p1  # noqa: PLC0415

    session = _Session(root)
    owned: dict[str, Any] = {"retained_root": None, "owned_files": [], "owned_dirs": [],
                             "observed_extra": [], "secondary_close_errors": []}
    phase = "PRE_P1_PIN"
    disp = "REFUSED_PRE_WRITE"
    # Hoist mutable capture state for post-verify recheck.
    p1_hashes: dict[str, str] = {}
    control_files: dict[str, str] = {}
    control_dirs: dict[str, str] = {}
    edition_files: dict[str, str] = {}
    edition_dirs: dict[str, str] = {}
    edition_sizes: dict[str, int] = {}
    head_pinned = ""
    source_root_rel = ""
    survey_root_rel = ""
    expected_dir = ""
    retained_rel = ""
    prop_rel = ""
    prop_data = b""
    supplied: dict[str, Any] = {}
    copy_rows: list[dict[str, Any]] = []
    keep_rows: list[dict[str, Any]] = []
    plan: list[dict[str, Any]] = []
    try:
        # 0. HEAD pin before anything (sanitized Git; verifier never does this).
        head_pinned = _git_head(session.root_resolved, "capture HEAD pin", phase, disp)
        # 1. Narrow pins before P1 (no broad walk from unvalidated Profile).
        state_rel, state_data = session.safe_read(state_path,
                                                  "Production State", phase, disp)
        try:
            state = _parse_json_strict(state_data, "Production State", phase, disp, "STATE_UNREADABLE")
        except RetentionError:
            raise
        if not isinstance(state, dict):
            raise _fail("STATE_UNREADABLE", phase, disp, "Production State is not an object")
        cfg_rel, cfg_data = session.safe_read(core.DEFAULT_CONFIG.as_posix(), "implementation config", phase, disp)
        try:
            cfg = _parse_json_strict(cfg_data, "implementation config", phase, disp, "CONFIG_UNREADABLE")
        except RetentionError:
            raise
        if not isinstance(cfg, dict):
            raise _fail("CONFIG_UNREADABLE", phase, disp, "implementation config is not an object")
        prof_ref = state.get("profile") or {}
        if not isinstance(prof_ref, dict) or set(prof_ref) != {"path", "sha256"}:
            raise _fail("STATE_PROFILE_SHAPE", phase, disp, "State lacks exact Production Profile reference")
        prof_rel, prof_data = session.safe_read(prof_ref["path"], "State-bound Production Profile", phase, disp)
        if core.sha256_bytes(prof_data) != prof_ref.get("sha256"):
            raise _fail("PROFILE_DRIFT", phase, disp, "State-bound Profile bytes drifted")
        try:
            profile = _parse_json_strict(prof_data, "State-bound Production Profile", phase, disp, "PROFILE_UNREADABLE")
        except RetentionError:
            raise
        if not isinstance(profile, dict):
            raise _fail("PROFILE_UNREADABLE", phase, disp, "Profile is not an object")
        prop_rel, prop_data = session.safe_read(proposal_path,
                                                "editorial correction proposal", phase, disp)
        if _raw_segments(prop_rel)[-1] != PROPOSAL_FILENAME:
            raise _fail("PROPOSAL_FILENAME", phase, disp, "proposal file must be named proposal.json")
        proposal = _loads_strict(prop_data, "editorial correction proposal", phase, disp)
        _validate_proposal_shape(proposal, phase, disp)
        # Pin schema + P2R dep bytes (observations, no authority inferred).
        session.safe_read(PROPOSAL_SCHEMA.as_posix(), "proposal schema", phase, disp)
        session.safe_read(MANIFEST_SCHEMA.as_posix(), "retention manifest schema", phase, disp)
        session.safe_read(P2R_MODULE.as_posix(), "P2R module", phase, disp)
        # Retained-root existence refuses before P1 (incl. empty/same-byte/dangling).
        proposal_id = proposal.get("proposal_id")
        if not isinstance(proposal_id, str):
            raise _fail("PROPOSAL_UNREADABLE", phase, disp, "proposal lacks proposal_id")
        try:
            source_root_rel = profile["paths"]["source_root"]
            survey_root_rel = profile["paths"]["survey_root"]
        except (KeyError, TypeError) as exc:
            raise _fail("PROFILE_ROOT_INVALID", phase, disp, f"profile source/survey root invalid: {exc}") from exc
        _check_lexical_path(source_root_rel, "profile source_root", phase, disp)
        _check_lexical_path(survey_root_rel, "profile survey_root", phase, disp)
        expected_dir = (Path(source_root_rel) / "publication" / "v2" / "editorial-corrections" / proposal_id).as_posix()
        retained_rel = (expected_dir + "/retained").replace("//", "/")
        _check_lexical_path(expected_dir, "proposal dir", phase, disp)
        _check_lexical_path(retained_rel, "retained root", phase, disp)
        retained_full = session.root_resolved / retained_rel
        try:
            lst_r = os.lstat(retained_full)
            # Any existing entry (dir/file/symlink/FIFO) refuses.
            raise _fail("RETAINED_ROOT_EXISTS", phase, disp,
                        f"retained root already present (no overwrite/takeover): {retained_rel}")
        except FileNotFoundError:
            pass
        except RetentionError:
            raise
        except OSError as exc:
            raise _fail("PATH_UNREADABLE", phase, disp, f"retained root unreadable: {retained_rel}: {exc}") from exc
        # Schema-validate supplied proposal against pinned bytes (recheck after).
        try:
            schema_gate.validate_instance(proposal, session.root_resolved / PROPOSAL_SCHEMA,
                                          label="editorial correction proposal")
        except ValueError as exc:
            raise _fail("SCHEMA_INVALID", phase, disp, f"proposal schema invalid: {exc}") from exc
        _rel, schema_after = session.safe_read(PROPOSAL_SCHEMA.as_posix(), "proposal schema recheck", phase, disp)
        if schema_after != session.files[PROPOSAL_SCHEMA.as_posix()]:
            raise _fail("STABILITY_VIOLATION", phase, disp, "proposal schema changed mid-inspection")
        # HEAD recheck before P1 (no drift between pin and call).
        if _git_head(session.root_resolved, "capture HEAD pre-P1", phase, disp) != head_pinned:
            raise _fail("HEAD_MOVED", phase, disp, "HEAD changed before P1 call")

        # 2. P1 call (before writes only) under sanitized Git env.
        phase = "P1_CALL"
        with _sanitized_git_env_ctx():
            try:
                outcome = p1.validate_proposal(str(session.root_resolved), str(state_path), str(proposal_path))
            except Exception as exc:
                code = "P1_REFUSED"
                detail = str(exc)
                raise _fail(code, phase, disp, f"P1 refused: {detail}", owned, cause=exc) from exc
        if outcome.get("result") not in ("REVIEW_REQUIRED", "REVIEW_BOUND_PROPOSAL"):
            raise _fail("P1_REFUSED", phase, disp, f"P1 unexpected result: {outcome.get('result')}", owned)
        p1_hashes = outcome.get("input_hashes") or {}
        if not isinstance(p1_hashes, dict) or not p1_hashes:
            raise _fail("P1_REFUSED", phase, disp, "P1 returned no input_hashes", owned)
        supplied = outcome.get("proposal") or {}
        if supplied != proposal:
            raise _fail("PROPOSAL_MISMATCH", phase, disp, "P1 measured proposal differs from supplied bytes", owned)
        # Compare every P1 input hash immediately (no replacing mismatches).
        phase = "POST_P1_SNAPSHOT"
        for rel, sha in p1_hashes.items():
            _check_lexical_path(rel, "P1 input", phase, disp)
            _rel, live = session.safe_read(rel, "P1 input recheck", phase, disp)
            if core.sha256_bytes(live) != sha:
                raise _fail("STABILITY_VIOLATION", phase, disp,
                            f"P1 input changed around P1 call: {rel}", owned)
        if _git_head(session.root_resolved, "capture HEAD post-P1", phase, "OWNED_PARTIAL") != head_pinned:
            raise _fail("HEAD_MOVED", phase, "OWNED_PARTIAL", "HEAD changed around P1 call", owned)

        # 3. Full validated snapshots before any write (exact, fail-closed).
        control_list = _control_paths(cfg, phase, disp)
        control_files = {}
        control_dirs = {}
        for cp in control_list:
            full = session.root_resolved / cp
            try:
                lst = os.lstat(full)
            except OSError as exc:
                raise _fail("CONTROL_MISSING", phase, disp,
                            f"control path missing: {cp}: {exc}", owned) from exc
            if _stat.S_ISLNK(lst.st_mode):
                raise _fail("CONTROL_ALIAS", phase, disp, f"control path is symlink: {cp}", owned)
            if _stat.S_ISDIR(lst.st_mode):
                fmap, dmap, _s = _snapshot_expanded(session, [cp], "control root", phase, disp)
                control_files.update(fmap)
                control_dirs.update(dmap)
            elif _stat.S_ISREG(lst.st_mode):
                _rel, data = session.safe_read(cp, "control file", phase, disp)
                control_files[_rel] = core.sha256_bytes(data)
            else:
                raise _fail("CONTROL_NOT_REGULAR", phase, disp, f"control path not regular/dir: {cp}", owned)
        edition_files, edition_dirs, edition_sizes = _snapshot_expanded(
            session, [source_root_rel, survey_root_rel], "edition tree", phase, disp)

        # 4. Preflight (no writes on failure).
        phase = "PREFLIGHT"
        disp = "REFUSED_PRE_WRITE"
        plan = supplied.get("retention_plan") or []
        if not isinstance(plan, list) or not plan:
            raise _fail("RETENTION_MISMATCH", phase, disp, "P1 retention plan empty")
        # Sorted-unique original plan paths required (no silent repair).
        plan_paths = [r.get("path") for r in plan if isinstance(r, dict)]
        if len(set(plan_paths)) != len(plan_paths):
            raise _fail("RETENTION_MISMATCH", phase, disp, "retention plan has duplicate paths")
        if plan_paths != sorted(plan_paths):
            raise _fail("RETENTION_ORDER_MISMATCH", phase, disp, "retention plan paths not sorted")
        seen_dest: set[str] = set()
        copy_rows = []
        keep_rows = []
        for row in plan:
            if not isinstance(row, dict):
                raise _fail("RETENTION_MISMATCH", phase, disp, "retention row not an object")
            for k in ("roles", "path", "sha256", "byte_count", "policy"):
                if k not in row:
                    raise _fail("RETENTION_MISMATCH", phase, disp, f"retention row missing {k}")
            _validate_roles_sorted_unique(row["roles"], f"retention {row.get('path')}", phase, disp)
            _check_lexical_path(row["path"], "retention source", phase, disp)
            if not isinstance(row["sha256"], str) or len(row["sha256"]) != 64:
                raise _fail("RETENTION_MISMATCH", phase, disp, f"retention row sha invalid: {row['path']}")
            if not isinstance(row["byte_count"], int) or row["byte_count"] < 1:
                raise _fail("RETENTION_MISMATCH", phase, disp, f"retention row size invalid: {row['path']}")
            if row["policy"] == "KEEP_IMMUTABLE":
                if "retained_dest" in row or "retained_sha256" in row or "retained_byte_count" in row:
                    raise _fail("RETENTION_MISMATCH", phase, disp,
                                f"KEEP row must not carry COPY-only fields: {row['path']}")
                if set(row.get("retained_ref", {})) != {"path", "sha256"}:
                    raise _fail("RETENTION_MISMATCH", phase, disp, f"KEEP row lacks exact retained_ref: {row['path']}")
                if row["retained_ref"] != {"path": row["path"], "sha256": row["sha256"]}:
                    raise _fail("RETENTION_MISMATCH", phase, disp, f"KEEP retained_ref must equal source: {row['path']}")
                keep_rows.append(row)
            elif row["policy"] == "COPY_BEFORE_REPLACEMENT":
                if "retained_ref" in row:
                    raise _fail("RETENTION_MISMATCH", phase, disp, f"COPY row must not carry retained_ref: {row['path']}")
                dest = row.get("retained_dest", "")
                if not isinstance(dest, str) or not dest:
                    raise _fail("RETENTION_MISMATCH", phase, disp, f"COPY row lacks retained_dest: {row['path']}")
                _check_lexical_path(dest, "retained dest", phase, disp)
                # Recompute exact dest independently (no blind trust).
                recomputed = _expected_retained_dest(expected_dir, row["path"])
                if dest != recomputed:
                    raise _fail("RETENTION_DEST_MISMATCH", phase, disp,
                                f"COPY dest {dest} != recomputed {recomputed}: {row['path']}")
                if not dest.startswith(retained_rel + "/"):
                    raise _fail("RETENTION_MISMATCH", phase, disp, f"COPY dest outside retained root: {dest}")
                if dest in seen_dest:
                    raise _fail("RETENTION_DEST_CONFLICT", phase, disp, f"duplicate retention destination: {dest}")
                seen_dest.add(dest)
                copy_rows.append(row)
            else:
                raise _fail("RETENTION_MISMATCH", phase, disp, f"unknown policy: {row.get('policy')}")
        # Overlap vs live inputs + absent-required + byte equality.
        live_set = set(session.files)
        for row in copy_rows:
            dest = row["retained_dest"]
            for live in live_set:
                if dest == live or dest.startswith(live.rstrip("/") + "/") or live.startswith(dest.rstrip("/") + "/"):
                    raise _fail("RETENTION_OVERLAP", phase, disp,
                                f"retention destination overlaps live input namespace: {dest}")
            dfull = session.root_resolved / dest
            try:
                os.lstat(dfull)
                raise _fail("RETENTION_DEST_CONFLICT", phase, disp,
                            f"retention destination already present: {dest}")
            except FileNotFoundError:
                pass
            except RetentionError:
                raise
            except OSError as exc:
                raise _fail("PATH_UNREADABLE", phase, disp, f"retention dest unreadable: {dest}: {exc}") from exc
            _rel, live_bytes = session.safe_read(row["path"], "COPY source", phase, disp)
            if core.sha256_bytes(live_bytes) != row["sha256"] or len(live_bytes) != row["byte_count"]:
                raise _fail("REF_DRIFT", phase, disp, f"COPY source bytes differ from plan: {row['path']}")
        for row in keep_rows:
            session.repinned(row["retained_ref"], f"KEEP ref {row['path']}", phase, disp,
                             expected_size=row["byte_count"])

        # 5. Exclusive claim + dirfd-relative writes with full ancestor pinning.
        phase = "CLAIM"
        disp = "OWNED_PARTIAL"
        dir_parts, leaf = session._split(retained_rel)
        # Pin full ancestor chain identities from repo root to retained parent.
        ancestor_pins: dict[str, tuple[int, int, int]] = {}
        cursor = session.root_resolved
        cur_rel_parts: list[str] = []
        for part in dir_parts:
            cur_rel_parts.append(part)
            cur_rel = "/".join(cur_rel_parts)
            try:
                lst = os.lstat(cursor / part if cursor != session.root_resolved else session.root_resolved / cur_rel)
            except OSError as exc:
                raise _fail("PATH_MISSING", phase, disp, f"proposal ancestor missing: {cur_rel}: {exc}", owned) from exc
            if _stat.S_ISLNK(lst.st_mode) or not _stat.S_ISDIR(lst.st_mode):
                raise _fail("PATH_ALIAS", phase, disp, f"proposal ancestor not a real dir: {cur_rel}", owned)
            ancestor_pins[cur_rel] = (lst.st_dev, lst.st_ino, _stat.S_IMODE(lst.st_mode))

        def _verify_ancestors(op: str) -> None:
            for arel, pinned in ancestor_pins.items():
                try:
                    lst = os.lstat(session.root_resolved / arel)
                except OSError as exc:
                    raise _fail("ANCESTOR_REPLACED", "WRITE", "OWNED_PARTIAL",
                                f"ancestor lost during {op}: {arel}: {exc}", owned) from exc
                cur = (lst.st_dev, lst.st_ino, _stat.S_IMODE(lst.st_mode))
                if cur != pinned or _stat.S_ISLNK(lst.st_mode):
                    raise _fail("ANCESTOR_REPLACED", "WRITE", "OWNED_PARTIAL",
                                f"ancestor replaced during {op}: {arel}", owned)

        parent_fd = session._open_dir_chain(dir_parts, "proposal parent", phase, disp) if dir_parts else session.root_fd
        try:
            os.stat(leaf, dir_fd=parent_fd, follow_symlinks=False)
            ent_exists = True
        except FileNotFoundError:
            ent_exists = False
        if ent_exists:
            raise _fail("RETAINED_ROOT_EXISTS", phase, disp,
                        f"retained root appeared before claim: {retained_rel}", owned)
        try:
            os.mkdir(leaf, 0o777, dir_fd=parent_fd)
        except FileExistsError as exc:
            raise _fail("RETAINED_ROOT_EXISTS", phase, disp,
                        f"retained root claim lost (exists): {retained_rel}: {exc}", owned) from exc
        except OSError as exc:
            raise _fail("WRITE_FAILED", phase, disp,
                        f"retained root mkdir failed: {retained_rel}: {exc}", owned) from exc
        try:
            rf = os.open(leaf, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
                         | getattr(os, "O_NONBLOCK", 0), dir_fd=parent_fd)
        except OSError as exc:
            raise _fail("WRITE_FAILED", phase, disp, f"cannot open claimed root: {exc}", owned) from exc
        session._open_fds.append(rf)
        try:
            rst = os.fstat(rf)
        except OSError as exc:
            raise _fail("WRITE_FAILED", phase, disp, f"claimed root fstat failed: {exc}", owned) from exc
        if not _stat.S_ISDIR(rst.st_mode):
            raise _fail("WRITE_FAILED", phase, disp, "claimed root not a directory", owned)
        # Entry-vs-fd binding for claimed root.
        try:
            est = os.stat(leaf, dir_fd=parent_fd, follow_symlinks=False)
        except OSError as exc:
            raise _fail("ROOT_IDENTITY_CHANGED", phase, disp, f"claimed root entry lost: {exc}", owned) from exc
        if (est.st_dev, est.st_ino) != (rst.st_dev, rst.st_ino):
            raise _fail("ROOT_IDENTITY_CHANGED", phase, disp, "claimed root entry/fd mismatch", owned)
        root_id = (rst.st_dev, rst.st_ino)
        owned["retained_root"] = {"path": retained_rel, "dev": rst.st_dev, "ino": rst.st_ino,
                                  "mode": oct(_stat.S_IMODE(rst.st_mode))}
        retained_fd = rf

        def _check_root_live(op: str) -> None:
            _verify_ancestors(op)
            try:
                cur = os.stat(leaf, dir_fd=parent_fd, follow_symlinks=False)
            except OSError as exc:
                raise _fail("ROOT_IDENTITY_CHANGED", "WRITE", "OWNED_PARTIAL",
                            f"retained root entry lost during {op}: {exc}", owned) from exc
            if (cur.st_dev, cur.st_ino) != root_id or not _stat.S_ISDIR(cur.st_mode) or _stat.S_ISLNK(cur.st_mode):
                raise _fail("ROOT_IDENTITY_CHANGED", "WRITE", "OWNED_PARTIAL",
                            f"retained root replaced during {op}: {retained_rel}", owned)
            try:
                live = os.fstat(retained_fd)
            except OSError as exc:
                raise _fail("ROOT_IDENTITY_CHANGED", "WRITE", "OWNED_PARTIAL",
                            f"retained fd fstat failed during {op}: {exc}", owned) from exc
            if (live.st_dev, live.st_ino) != root_id:
                raise _fail("ROOT_IDENTITY_CHANGED", "WRITE", "OWNED_PARTIAL",
                            f"retained fd identity changed during {op}", owned)

        phase = "WRITE"
        needed_dirs: set[str] = set()
        for row in copy_rows:
            dest_rel = row["retained_dest"]
            sub = dest_rel[len(retained_rel) + 1:]
            parts = _raw_segments(sub)[:-1]
            cur = ""
            for part in parts:
                if part in ("", ".", ".."):
                    raise _fail("PATH_TRAVERSAL", phase, "OWNED_PARTIAL", f"bad dest segment: {dest_rel}", owned)
                cur = cur + "/" + part if cur else part
                needed_dirs.add(cur)
        dirfd_map: dict[str, int] = {"": retained_fd}
        owned_dir_ids: dict[str, tuple[int, int]] = {}
        secondary_close_errors: list[str] = []
        primary_error: RetentionError | None = None
        try:
            _check_root_live("ancestor-build")
            for sub in sorted(needed_dirs):
                parent_sub = "/".join(_raw_segments(sub)[:-1])
                name = _raw_segments(sub)[-1]
                pfd = dirfd_map[parent_sub]
                try:
                    try:
                        os.stat(name, dir_fd=pfd, follow_symlinks=False)
                        raise _fail("RETENTION_DEST_CONFLICT", phase, "OWNED_PARTIAL",
                                    f"retained ancestor already present: {sub}", owned)
                    except FileNotFoundError:
                        pass
                    os.mkdir(name, 0o777, dir_fd=pfd)
                    owned["owned_dirs"].append({"path": retained_rel + "/" + sub, "status": "created"})
                except RetentionError:
                    raise
                except OSError as exc:
                    raise _fail("WRITE_FAILED", phase, "OWNED_PARTIAL",
                                f"ancestor mkdir failed: {sub}: {exc}", owned) from exc
                try:
                    dfd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
                                  | getattr(os, "O_NONBLOCK", 0), dir_fd=pfd)
                except OSError as exc:
                    raise _fail("WRITE_FAILED", phase, "OWNED_PARTIAL",
                                f"ancestor open failed: {sub}: {exc}", owned) from exc
                session._open_fds.append(dfd)
                try:
                    dst = os.fstat(dfd)
                    est2 = os.stat(name, dir_fd=pfd, follow_symlinks=False)
                except OSError as exc:
                    raise _fail("WRITE_FAILED", phase, "OWNED_PARTIAL",
                                f"ancestor identity check failed: {sub}: {exc}", owned) from exc
                if (dst.st_dev, dst.st_ino) != (est2.st_dev, est2.st_ino):
                    raise _fail("ANCESTOR_REPLACED", phase, "OWNED_PARTIAL",
                                f"ancestor entry/fd mismatch: {sub}", owned)
                dirfd_map[sub] = dfd
                owned_dir_ids[sub] = (dst.st_dev, dst.st_ino)
            for row in copy_rows:
                _check_root_live(f"write {row['retained_dest']}")
                dest_rel = row["retained_dest"]
                sub = dest_rel[len(retained_rel) + 1:]
                parts = _raw_segments(sub)
                parent_sub = "/".join(parts[:-1])
                name = parts[-1]
                pfd = dirfd_map[parent_sub]
                src_rel = row["path"]
                data = session.files.get(src_rel)
                if data is None:
                    _rel, data = session.safe_read(src_rel, "COPY source resnapshot", phase, "OWNED_PARTIAL")
                # Structured ownership at creation (before close).
                try:
                    wfd = os.open(name, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0),
                                  0o664, dir_fd=pfd)
                except FileExistsError as exc:
                    raise _fail("RETENTION_DEST_CONFLICT", phase, "OWNED_PARTIAL",
                                f"retained dest appeared: {dest_rel}: {exc}", owned) from exc
                except OSError as exc:
                    raise _fail("WRITE_FAILED", phase, "OWNED_PARTIAL",
                                f"retained dest open failed: {dest_rel}: {exc}", owned) from exc
                session._open_fds.append(wfd)
                try:
                    wst = os.fstat(wfd)
                    owned_entry: dict[str, Any] = {"path": dest_rel, "dev": wst.st_dev, "ino": wst.st_ino,
                                                   "bytes": 0, "status": "open"}
                    owned["owned_files"].append(owned_entry)
                except OSError:
                    pass
                write_primary: RetentionError | None = None
                try:
                    view = memoryview(data)
                    total = 0
                    while total < len(data):
                        try:
                            n = os.write(wfd, view[total:])
                        except OSError as exc:
                            raise _fail("WRITE_FAILED", phase, "OWNED_PARTIAL",
                                        f"write failed: {dest_rel}: {exc}", owned) from exc
                        if n == 0:
                            raise _fail("WRITE_ZERO_PROGRESS", phase, "OWNED_PARTIAL",
                                        f"zero-progress write: {dest_rel}", owned)
                        total += n
                    try:
                        os.fsync(wfd)
                    except OSError as exc:
                        raise _fail("FSYNC_FAILED", phase, "OWNED_PARTIAL",
                                    f"fsync failed: {dest_rel}: {exc}", owned) from exc
                except RetentionError as exc:
                    write_primary = exc
                    raise
                finally:
                    try:
                        os.close(wfd)
                    except OSError as exc:
                        close_err = _fail("CLOSE_FAILED", phase, "OWNED_PARTIAL",
                                          f"close after write failed: {dest_rel}: {exc}", owned, cause=exc)
                        if write_primary is not None:
                            # Preserve primary, attach secondary.
                            owned.setdefault("secondary_close_errors", []).append(str(exc))
                            raise write_primary from exc
                        raise close_err from exc
                    finally:
                        if wfd in session._open_fds:
                            session._open_fds.remove(wfd)
                    if write_primary is None:
                        for e in owned["owned_files"]:
                            if e.get("path") == dest_rel and e.get("status") == "open":
                                e["bytes"] = len(data)
                                e["status"] = "closed"
                _check_root_live(f"after write {dest_rel}")
                # Entry identity for owned COPY file (dev/ino must be the created one).
                try:
                    eest = os.stat(name, dir_fd=pfd, follow_symlinks=False)
                except OSError as exc:
                    raise _fail("FILE_REPLACED", phase, "OWNED_PARTIAL",
                                f"owned file entry lost: {dest_rel}: {exc}", owned) from exc
                if owned_entry.get("dev") is not None and (eest.st_dev, eest.st_ino) != (
                        owned_entry["dev"], owned_entry["ino"]):
                    raise _fail("FILE_REPLACED", phase, "OWNED_PARTIAL",
                                f"owned file replaced after write (same bytes do not pass): {dest_rel}", owned)
                # Readback bytes + size.
                _rel, back = session.safe_read(dest_rel, "COPY readback", phase, "OWNED_PARTIAL")
                if core.sha256_bytes(back) != row["sha256"] or len(back) != row["byte_count"]:
                    raise _fail("READBACK_MISMATCH", phase, "OWNED_PARTIAL",
                                f"COPY readback mismatch: {dest_rel}", owned)
        except RetentionError as exc:
            primary_error = exc
            if secondary_close_errors and exc.__cause__ is None:
                owned.setdefault("secondary_close_errors", []).extend(secondary_close_errors)
            raise

        # 6. Late rechecks before manifest (exact owned delta only, no broad exemption).
        phase = "FINALIZE"
        for rel, sha in p1_hashes.items():
            _rel, live = session.safe_read(rel, "final input recheck", phase, "OWNED_PARTIAL")
            if core.sha256_bytes(live) != sha:
                raise _fail("FINALIZATION_REFUSED", phase, "OWNED_PARTIAL",
                            f"input drift before finalization: {rel}", owned)
        if _git_head(session.root_resolved, "capture HEAD final", phase, "OWNED_PARTIAL") != head_pinned:
            raise _fail("HEAD_MOVED", phase, "OWNED_PARTIAL", "HEAD changed before finalization", owned)
        for row in copy_rows:
            _rel, back = session.safe_read(row["retained_dest"], "final retained recheck", phase, "OWNED_PARTIAL")
            if core.sha256_bytes(back) != row["sha256"] or len(back) != row["byte_count"]:
                raise _fail("FINALIZATION_REFUSED", phase, "OWNED_PARTIAL",
                            f"retained drift before finalization: {row['retained_dest']}", owned)
        for row in keep_rows:
            session.repinned(row["retained_ref"], "final KEEP recheck", phase, "OWNED_PARTIAL",
                             expected_size=row["byte_count"])
        # Control inventory recomputation: exact equality (no new control file/dir allowed).
        control_files2: dict[str, str] = {}
        control_dirs2: dict[str, str] = {}
        for cp in control_list:
            full = session.root_resolved / cp
            try:
                lst = os.lstat(full)
            except OSError as exc:
                raise _fail("FINALIZATION_REFUSED", phase, "OWNED_PARTIAL",
                            f"control disappearance before finalization: {cp}: {exc}", owned) from exc
            if _stat.S_ISDIR(lst.st_mode) and not _stat.S_ISLNK(lst.st_mode):
                fmap, dmap, _s = _snapshot_expanded(session, [cp], "control root final", phase, "OWNED_PARTIAL")
                control_files2.update(fmap)
                control_dirs2.update(dmap)
            elif _stat.S_ISREG(lst.st_mode):
                _rel, data = session.safe_read(cp, "control file final", phase, "OWNED_PARTIAL")
                control_files2[_rel] = core.sha256_bytes(data)
            else:
                raise _fail("FINALIZATION_REFUSED", phase, "OWNED_PARTIAL",
                            f"control type change before finalization: {cp}", owned)
        if control_files2 != control_files or control_dirs2 != control_dirs:
            raise _fail("FINALIZATION_REFUSED", phase, "OWNED_PARTIAL",
                        f"control inventory drift before finalization: files-extra={sorted(set(control_files2) - set(control_files))} "
                        f"missing={sorted(set(control_files) - set(control_files2))} "
                        f"dirs-extra={sorted(set(control_dirs2) - set(control_dirs))} "
                        f"dirs-missing={sorted(set(control_dirs) - set(control_dirs2))}", owned)
        # Edition/control inventories: only exact owned additions allowed.
        edition_files2, edition_dirs2, edition_sizes2 = _snapshot_expanded(
            session, [source_root_rel, survey_root_rel], "edition tree final", phase, "OWNED_PARTIAL")
        owned_file_set = {r["retained_dest"] for r in copy_rows}
        owned_dir_set = {retained_rel + "/" + s for s in needed_dirs} | {retained_rel}
        expected_files = set(edition_files) | owned_file_set
        # Manifest not yet written, so not in expected.
        for rel, sha in edition_files2.items():
            if rel in edition_files:
                if edition_files[rel] != sha:
                    raise _fail("FINALIZATION_REFUSED", phase, "OWNED_PARTIAL",
                                f"edition drift before finalization: {rel}", owned)
                if edition_sizes.get(rel) != edition_sizes2.get(rel):
                    raise _fail("FINALIZATION_REFUSED", phase, "OWNED_PARTIAL",
                                f"edition size drift before finalization: {rel}", owned)
            elif rel in owned_file_set:
                pass
            else:
                raise _fail("FINALIZATION_REFUSED", phase, "OWNED_PARTIAL",
                            f"unexpected edition addition before finalization: {rel}", owned)
        for rel in edition_files:
            if rel not in edition_files2:
                raise _fail("FINALIZATION_REFUSED", phase, "OWNED_PARTIAL",
                            f"edition disappearance before finalization: {rel}", owned)
        expected_dirs = set(edition_dirs) | owned_dir_set
        for rel in edition_dirs2:
            if rel not in expected_dirs:
                raise _fail("FINALIZATION_REFUSED", phase, "OWNED_PARTIAL",
                            f"unexpected edition dir before finalization: {rel}", owned)
        for rel in expected_dirs:
            if rel not in edition_dirs2:
                raise _fail("FINALIZATION_REFUSED", phase, "OWNED_PARTIAL",
                            f"edition dir disappearance before finalization: {rel}", owned)

        # 7. Manifest-last (exclusive create, fsync, close-checked, readback).
        # Manifest failures are INDETERMINATE (bytes may be partial/complete).
        phase = "MANIFEST_PUBLISH"
        p2r_mod_rel, p2r_mod_data = session.safe_read(P2R_MODULE.as_posix(), "P2R module final", phase, "OWNED_PARTIAL")
        p2r_sch_rel, p2r_sch_data = session.safe_read(MANIFEST_SCHEMA.as_posix(), "P2R schema final", phase, "OWNED_PARTIAL")
        cap_inputs = [{"path": k, "sha256": v} for k, v in sorted(p1_hashes.items())]
        cap_inputs.append({"path": p2r_mod_rel, "sha256": core.sha256_bytes(p2r_mod_data)})
        cap_inputs.append({"path": p2r_sch_rel, "sha256": core.sha256_bytes(p2r_sch_data)})
        dedup: dict[str, str] = {}
        for e in cap_inputs:
            if e["path"] in dedup and dedup[e["path"]] != e["sha256"]:
                raise _fail("FINALIZATION_REFUSED", phase, "OWNED_PARTIAL",
                            f"capture input conflict: {e['path']}", owned)
            dedup[e["path"]] = e["sha256"]
        cap_inputs = [{"path": k, "sha256": dedup[k]} for k in sorted(dedup)]
        rows: list[dict[str, Any]] = []
        for row in plan:
            base = {"roles": sorted(row["roles"]), "path": row["path"], "sha256": row["sha256"],
                    "byte_count": row["byte_count"], "policy": row["policy"]}
            if row["policy"] == "KEEP_IMMUTABLE":
                base["retained_ref"] = {"path": row["retained_ref"]["path"], "sha256": row["retained_ref"]["sha256"]}
            else:
                base["retained_dest"] = row["retained_dest"]
                base["retained_sha256"] = row["sha256"]
                base["retained_byte_count"] = row["byte_count"]
            rows.append(base)
        manifest = {
            "schema_version": "2.0-rc1",
            "kind": "EDITORIAL_RETENTION_V1",
            "status": "CAPTURED",
            "proposal_ref": {"path": prop_rel, "sha256": core.sha256_bytes(prop_data),
                             "proposal_id": supplied.get("proposal_id"), "issue_id": supplied.get("issue_id"),
                             "research_profile": supplied.get("research_profile"),
                             "publication_profile": supplied.get("publication_profile")},
            "basis": dict(supplied.get("basis") or {}),
            "proposed": dict(supplied.get("proposed") or {}),
            "rows": rows,
            "capture_inputs": cap_inputs,
        }
        try:
            schema_gate.validate_instance(manifest, session.root_resolved / MANIFEST_SCHEMA,
                                          label="editorial retention manifest")
        except ValueError as exc:
            raise _fail("SCHEMA_INVALID", phase, "OWNED_PARTIAL", f"manifest schema invalid: {exc}", owned) from exc
        manifest_bytes = core.json_bytes(_project_manifest_canonical(manifest, phase, "OWNED_PARTIAL"))
        manifest_rel = (retained_rel + "/" + MANIFEST_FILENAME).replace("//", "/")
        manifest_sub = manifest_rel[len(retained_rel) + 1:]
        manifest_parts = _raw_segments(manifest_sub)
        manifest_parent_sub = "/".join(manifest_parts[:-1])
        mpfd = dirfd_map[manifest_parent_sub] if manifest_parent_sub else retained_fd
        mname = manifest_parts[-1]
        _check_root_live("manifest publish")
        if _git_head(session.root_resolved, "capture HEAD pre-manifest", phase, "OWNED_PARTIAL") != head_pinned:
            raise _fail("HEAD_MOVED", phase, "OWNED_PARTIAL", "HEAD changed before manifest publish", owned)
        try:
            mfd = os.open(mname, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0),
                          0o664, dir_fd=mpfd)
        except FileExistsError as exc:
            raise _fail("RETENTION_DEST_CONFLICT", phase, "OWNED_PARTIAL",
                        f"manifest already present: {manifest_rel}: {exc}", owned) from exc
        except OSError as exc:
            raise _fail("MANIFEST_WRITE_FAILED", phase, "INDETERMINATE_INVOCATION",
                        f"manifest open failed: {manifest_rel}: {exc}", owned) from exc
        session._open_fds.append(mfd)
        try:
            owned.setdefault("manifest_attempt", {"path": manifest_rel, "status": "open"})
        except Exception:
            pass
        manifest_primary: RetentionError | None = None
        try:
            view = memoryview(manifest_bytes)
            total = 0
            while total < len(manifest_bytes):
                try:
                    n = os.write(mfd, view[total:])
                except OSError as exc:
                    raise _fail("MANIFEST_WRITE_FAILED", phase, "INDETERMINATE_INVOCATION",
                                f"manifest write failed: {exc}", owned) from exc
                if n == 0:
                    raise _fail("MANIFEST_ZERO_PROGRESS", phase, "INDETERMINATE_INVOCATION",
                                "manifest zero-progress write", owned)
                total += n
            try:
                os.fsync(mfd)
            except OSError as exc:
                raise _fail("MANIFEST_FSYNC_FAILED", phase, "INDETERMINATE_INVOCATION",
                            f"manifest fsync failed: {exc}", owned) from exc
        except RetentionError as exc:
            manifest_primary = exc
            raise
        finally:
            try:
                os.close(mfd)
            except OSError as exc:
                close_err = _fail("MANIFEST_CLOSE_FAILED", phase, "INDETERMINATE_INVOCATION",
                                  f"manifest close failed: {exc}", owned, cause=exc)
                if manifest_primary is not None:
                    owned.setdefault("secondary_close_errors", []).append(str(exc))
                    raise manifest_primary from exc
                raise close_err from exc
            finally:
                if mfd in session._open_fds:
                    session._open_fds.remove(mfd)
        # Record manifest as owned (closed) for post-verify accounting.
        owned["owned_files"].append({"path": manifest_rel, "bytes": len(manifest_bytes), "status": "closed"})
        _rel, back = session.safe_read(manifest_rel, "manifest readback", phase, "OWNED_PARTIAL")
        if back != manifest_bytes:
            raise _fail("READBACK_MISMATCH", phase, "INDETERMINATE_INVOCATION", "manifest readback mismatch", owned)
        manifest_sha = core.sha256_bytes(back)
        # Pre-close reverify, then close all dir fds (close errors fail).
        session.reverify(phase, "OWNED_PARTIAL")
        try:
            session._close_all(phase, "OWNED_PARTIAL")
        except RetentionError as exc:
            raise _fail("CLOSE_FAILED", phase, "INDETERMINATE_INVOCATION",
                        f"directory close failed before success: {exc}", owned, cause=exc) from exc
        # Post-close standalone check opens a fresh read-only session (no fds held).
        verify_out = verify_retention(str(session.root_resolved), str(proposal_path), manifest_rel)
        if verify_out.get("result") != RESULT_VERIFIED:
            raise _fail("FINALIZATION_REFUSED", "MANIFEST_PUBLISH", "INDETERMINATE_INVOCATION",
                        "standalone verification after publish did not verify", owned)
        # Final post-readback boundary: verifier intentionally does not read
        # live P1 inputs/HEAD; recheck them here before reporting success.
        # A mutable live State/input change during verifier execution must not escape.
        post = _Session(str(session.root_resolved))
        try:
            for rel, sha in p1_hashes.items():
                _r, live = post.safe_read(rel, "post-verify input recheck", "MANIFEST_PUBLISH",
                                          "INDETERMINATE_INVOCATION")
                if core.sha256_bytes(live) != sha:
                    raise _fail("FINALIZATION_REFUSED", "MANIFEST_PUBLISH", "INDETERMINATE_INVOCATION",
                                f"input drift during verifier execution: {rel}", owned)
            if _git_head(post.root_resolved, "capture HEAD post-verify", "MANIFEST_PUBLISH",
                         "INDETERMINATE_INVOCATION") != head_pinned:
                raise _fail("HEAD_MOVED", "MANIFEST_PUBLISH", "INDETERMINATE_INVOCATION",
                            "HEAD changed during verifier execution", owned)
            post.reverify("MANIFEST_PUBLISH", "INDETERMINATE_INVOCATION")
            try:
                post._close_all("MANIFEST_PUBLISH", "INDETERMINATE_INVOCATION")
            except RetentionError as exc:
                raise _fail("CLOSE_FAILED", "MANIFEST_PUBLISH", "INDETERMINATE_INVOCATION",
                            f"post-verify close failed: {exc}", owned, cause=exc) from exc
        except RetentionError:
            try:
                if not post._closed:
                    post._close_all("MANIFEST_PUBLISH", "INDETERMINATE_INVOCATION")
            except RetentionError:
                pass
            raise
        return {"result": RESULT_CAPTURED, "manifest_path": manifest_rel, "manifest_sha256": manifest_sha,
                "proposal_sha256": core.sha256_bytes(prop_data),
                "input_hashes": {e["path"]: e["sha256"] for e in cap_inputs},
                "retained": {"copy_files": len(copy_rows), "keep_refs": len(keep_rows),
                             "manifest_bytes": len(manifest_bytes)}}
    except RetentionError as exc:
        # Preserve partials; close held fds (best effort, original error wins).
        # Attach structured ownership to post-claim errors lacking it.
        if phase in ("CLAIM", "WRITE", "FINALIZE", "MANIFEST_PUBLISH") and not exc.owned:
            exc.owned = owned
            exc.args = (f"{exc.code}: [{exc.phase}/{exc.disposition}] {exc.detail}",)
        try:
            if not session._closed:
                try:
                    session._close_all("WRITE" if phase in ("CLAIM", "WRITE", "FINALIZE", "MANIFEST_PUBLISH") else phase,
                                       "OWNED_PARTIAL" if phase in ("CLAIM", "WRITE", "FINALIZE", "MANIFEST_PUBLISH") else disp,
                                       prior=exc)
                except RetentionError as close_exc:
                    # Original error wins; record secondary closes in owned.
                    if isinstance(close_exc, RetentionError) and "secondary closes" in close_exc.detail:
                        owned.setdefault("secondary_close_errors", []).append(close_exc.detail)
                    pass
        except Exception:
            pass
        raise
    except Exception as exc:
        try:
            if not session._closed:
                session._close_all(phase, disp, prior=None)
        except RetentionError:
            pass
        except Exception:
            pass
        raise _fail("WRITE_FAILED", phase, disp, f"unexpected capture failure: {exc}", owned, cause=exc) from exc


def verify_retention(root: str | Path, proposal_path: str | Path, manifest_path: str | Path) -> dict[str, Any]:
    """Standalone read-only retained-set verification (no P1/Git/HEAD)."""
    session = _Session(root)
    phase = "VERIFY"
    disp = "INVALID"
    try:
        prop_rel, prop_data = session.safe_read(proposal_path,
                                                "editorial correction proposal", phase, disp)
        if _raw_segments(prop_rel)[-1] != PROPOSAL_FILENAME:
            raise _fail("PROPOSAL_FILENAME", phase, disp, "proposal file must be named proposal.json")
        proposal = _loads_strict(prop_data, "editorial correction proposal", phase, disp)
        _validate_proposal_shape(proposal, phase, disp)
        man_rel, man_data = session.safe_read(manifest_path,
                                              "retention manifest", phase, disp)
        if _raw_segments(man_rel)[-1] != MANIFEST_FILENAME:
            raise _fail("MANIFEST_FILENAME", phase, disp, "manifest file must be named retention-manifest.json")
        manifest = _loads_strict(man_data, "retention manifest", phase, disp)
        if not isinstance(manifest, dict):
            raise _fail("MANIFEST_UNREADABLE", phase, disp, "manifest is not an object")
        # Pin schemas before validators that reread them.
        session.safe_read(PROPOSAL_SCHEMA.as_posix(), "proposal schema", phase, disp)
        session.safe_read(MANIFEST_SCHEMA.as_posix(), "retention manifest schema", phase, disp)
        try:
            schema_gate.validate_instance(proposal, session.root_resolved / PROPOSAL_SCHEMA,
                                          label="editorial correction proposal")
        except ValueError as exc:
            raise _fail("SCHEMA_INVALID", phase, disp, f"proposal schema invalid: {exc}") from exc
        try:
            schema_gate.validate_instance(manifest, session.root_resolved / MANIFEST_SCHEMA,
                                          label="editorial retention manifest")
        except ValueError as exc:
            raise _fail("SCHEMA_INVALID", phase, disp, f"manifest schema invalid: {exc}") from exc
        session.reverify(phase, disp)
        # Header/basis/proposed equalities + path binding (no rebind by equal SHA).
        if proposal.get("proposal_id") != manifest.get("proposal_ref", {}).get("proposal_id"):
            raise _fail("HEADER_MISMATCH", phase, disp, "proposal_id differs between proposal and manifest")
        for k in ("issue_id", "research_profile", "publication_profile"):
            if proposal.get(k) != manifest.get("proposal_ref", {}).get(k):
                raise _fail("HEADER_MISMATCH", phase, disp, f"{k} differs between proposal and manifest")
        if manifest.get("proposal_ref", {}).get("path") != prop_rel:
            raise _fail("HEADER_MISMATCH", phase, disp, "manifest proposal_ref.path is not the supplied proposal path")
        if manifest.get("proposal_ref", {}).get("sha256") != core.sha256_bytes(prop_data):
            raise _fail("HEADER_MISMATCH", phase, disp, "manifest proposal_ref.sha256 differs from supplied proposal bytes")
        if manifest.get("basis") != proposal.get("basis"):
            raise _fail("BASIS_MISMATCH", phase, disp, "manifest basis differs from supplied proposal basis")
        if manifest.get("proposed") != proposal.get("proposed"):
            raise _fail("PROPOSED_MISMATCH", phase, disp, "manifest proposed differs from supplied proposal")
        # Exact ordered plan projection (no sorting to accept).
        plan = proposal.get("retention_plan") or []
        rows = manifest.get("rows") or []
        if not isinstance(plan, list) or not isinstance(rows, list) or len(plan) != len(rows):
            raise _fail("RETENTION_MISMATCH", phase, disp, "row count differs between proposal plan and manifest")
        # Sorted-unique original plan paths required.
        plan_paths = [r.get("path") if isinstance(r, dict) else None for r in plan]
        if len(set(plan_paths)) != len(plan_paths):
            raise _fail("RETENTION_MISMATCH", phase, disp, "proposal plan has duplicate paths")
        if plan_paths != sorted(plan_paths):
            raise _fail("RETENTION_ORDER_MISMATCH", phase, disp, "proposal plan paths not sorted")
        for i, (prow, mrow) in enumerate(zip(plan, rows)):
            if not isinstance(prow, dict) or not isinstance(mrow, dict):
                raise _fail("RETENTION_MISMATCH", phase, disp, f"row {i} not an object")
            if mrow.get("path") != prow.get("path"):
                raise _fail("RETENTION_ORDER_MISMATCH", phase, disp,
                            f"row {i} path order differs (no reordering accepted)")
            for k in ("roles", "path", "sha256", "byte_count", "policy"):
                if mrow.get(k) != prow.get(k):
                    raise _fail("RETENTION_MISMATCH", phase, disp, f"row {i} field {k} differs from plan")
            _validate_roles_sorted_unique(mrow.get("roles"), f"manifest row {mrow.get('path')}", phase, disp)
            _check_lexical_path(mrow["path"], "manifest row path", phase, disp)
            if not isinstance(mrow.get("byte_count"), int) or mrow["byte_count"] < 1:
                raise _fail("RETENTION_MISMATCH", phase, disp, f"row {i} byte_count invalid")
            if mrow["policy"] == "KEEP_IMMUTABLE":
                if "retained_dest" in mrow or "retained_sha256" in mrow or "retained_byte_count" in mrow:
                    raise _fail("RETENTION_MISMATCH", phase, disp,
                                f"KEEP row carries COPY-only fields: {mrow['path']}")
                if mrow.get("retained_ref") != {"path": mrow["path"], "sha256": mrow["sha256"]}:
                    raise _fail("RETENTION_MISMATCH", phase, disp, f"KEEP retained_ref must equal source: {mrow['path']}")
            elif mrow["policy"] == "COPY_BEFORE_REPLACEMENT":
                if "retained_ref" in mrow:
                    raise _fail("RETENTION_MISMATCH", phase, disp, f"COPY row carries retained_ref: {mrow['path']}")
                for k in ("retained_dest", "retained_sha256", "retained_byte_count"):
                    if k not in mrow:
                        raise _fail("RETENTION_MISMATCH", phase, disp, f"COPY row missing {k}: {mrow['path']}")
                _check_lexical_path(mrow["retained_dest"], "COPY dest", phase, disp)
                if mrow["retained_sha256"] != mrow["sha256"] or mrow["retained_byte_count"] != mrow["byte_count"]:
                    raise _fail("RETENTION_MISMATCH", phase, disp,
                                f"COPY retained measurement must equal source row: {mrow['path']}")
            else:
                raise _fail("RETENTION_MISMATCH", phase, disp, "unknown policy")
        # Duplicate path / dest checks.
        paths = [r["path"] for r in rows]
        if len(set(paths)) != len(paths):
            raise _fail("RETENTION_MISMATCH", phase, disp, "duplicate retention paths")
        dests = [r["retained_dest"] for r in rows if r.get("policy") == "COPY_BEFORE_REPLACEMENT"]
        if len(set(dests)) != len(dests):
            raise _fail("RETENTION_MISMATCH", phase, disp, "duplicate retention destinations")
        # I1 chain: state:authority COPY -> retained State -> State.profile -> KEEP Profile.
        basis = proposal.get("basis") or {}
        state_ref = basis.get("state_ref") or {}
        if set(state_ref) != {"path", "sha256"}:
            raise _fail("BASIS_MISMATCH", phase, disp, "basis.state_ref must be exact {path,sha256}")
        state_rows = [r for r in rows if "state:authority" in (r.get("roles") or [])]
        if len(state_rows) != 1:
            raise _fail("MISSING_STATE_AUTHORITY" if len(state_rows) == 0 else "AMBIGUOUS_STATE_AUTHORITY",
                        phase, disp,
                        "unique state:authority row required" if len(state_rows) != 1 else "state authority ambiguous")
        srow = state_rows[0]
        if srow.get("policy") != "COPY_BEFORE_REPLACEMENT":
            raise _fail("INVALID_RETENTION", phase, disp, "state:authority must be COPY")
        if srow.get("path") != state_ref.get("path") or srow.get("sha256") != state_ref.get("sha256"):
            raise _fail("STATE_REF_MISMATCH", phase, disp, "state:authority row must equal basis.state_ref")
        if "retained_dest" not in srow:
            raise _fail("INVALID_RETENTION", phase, disp, "state:authority lacks retained_dest")
        _srel, sdata = session.safe_read(srow["retained_dest"], "retained State", phase, disp)
        if core.sha256_bytes(sdata) != srow["sha256"] or len(sdata) != srow["byte_count"]:
            raise _fail("INVALID_RETENTION", phase, disp, "retained State bytes differ from row")
        try:
            rstate = _parse_json_strict(sdata, "retained State", phase, disp, "INVALID_RETENTION")
        except RetentionError:
            raise
        if not isinstance(rstate, dict):
            raise _fail("INVALID_RETENTION", phase, disp, "retained State not an object")
        rprof = rstate.get("profile") or {}
        if not isinstance(rprof, dict) or set(rprof) != {"path", "sha256"}:
            raise _fail("INVALID_RETENTION", phase, disp, "retained State lacks exact profile ref")
        matches = [r for r in rows if r.get("policy") == "KEEP_IMMUTABLE"
                   and r.get("retained_ref", {}).get("path") == rprof.get("path")
                   and r.get("retained_ref", {}).get("sha256") == rprof.get("sha256")]
        if len(matches) != 1:
            raise _fail("MISSING_PROFILE_MATCH" if len(matches) == 0 else "AMBIGUOUS_PROFILE_MATCH",
                        phase, disp, "unique matching KEEP Profile row required")
        prow_match = matches[0]
        _prel, pdata = session.safe_read(prow_match["retained_ref"]["path"], "required KEEP Profile", phase, disp)
        if core.sha256_bytes(pdata) != rprof.get("sha256") or len(pdata) != prow_match["byte_count"]:
            raise _fail("PROFILE_DRIFT", phase, disp, "KEEP Profile bytes/size drifted")
        try:
            rprofile = _parse_json_strict(pdata, "KEEP Profile", phase, disp, "INVALID_RETENTION")
        except RetentionError:
            raise
        if not isinstance(rprofile, dict):
            raise _fail("INVALID_RETENTION", phase, disp, "KEEP Profile not an object")
        # Issue/label agreement across proposal, retained State, Profile.
        if rstate.get("issue_id") != proposal.get("issue_id"):
            raise _fail("LABEL_MISMATCH", phase, disp, "retained State issue differs from proposal")
        for k in ("research_profile", "publication_profile"):
            if k in rstate and rstate.get(k) != proposal.get(k):
                raise _fail("LABEL_MISMATCH", phase, disp, f"retained State {k} differs from proposal")
        if rprofile.get("issue_id") != proposal.get("issue_id"):
            raise _fail("LABEL_MISMATCH", phase, disp, "KEEP Profile issue differs from proposal")
        for k in ("research_profile", "publication_profile"):
            if rprofile.get(k) != proposal.get(k):
                raise _fail("LABEL_MISMATCH", phase, disp, f"KEEP Profile {k} differs from proposal")
        try:
            source_root_rel = rprofile["paths"]["source_root"]
        except (KeyError, TypeError) as exc:
            raise _fail("INVALID_RETENTION", phase, disp, f"KEEP Profile source_root invalid: {exc}") from exc
        _check_lexical_path(source_root_rel, "retained source_root", phase, disp)
        expected_dir = (Path(source_root_rel) / "publication" / "v2" / "editorial-corrections" / proposal["proposal_id"]).as_posix()
        try:
            observed_dir = Path(prop_rel).parent.as_posix()
        except ValueError:
            raise _fail("PROPOSAL_LAYOUT", phase, disp, "proposal outside repository") from None
        if observed_dir != expected_dir:
            raise _fail("PROPOSAL_LAYOUT", phase, disp, f"proposal dir {observed_dir} != canonical {expected_dir}")
        expected_man = (expected_dir + "/retained/" + MANIFEST_FILENAME).replace("//", "/")
        if man_rel != expected_man:
            raise _fail("HEADER_MISMATCH", phase, disp, f"manifest path {man_rel} != canonical {expected_man}")
        # COPY dest recomputation: every COPY dest must equal
        # <proposal_dir>/retained/before/<original_path> (no moved dest).
        for r in rows:
            if r["policy"] == "COPY_BEFORE_REPLACEMENT":
                recomputed = _expected_retained_dest(expected_dir, r["path"])
                if r["retained_dest"] != recomputed:
                    raise _fail("RETENTION_DEST_MISMATCH", phase, disp,
                                f"COPY dest {r['retained_dest']} != recomputed {recomputed}: {r['path']}")
                if not r["retained_dest"].startswith(expected_dir + "/retained/"):
                    raise _fail("RETENTION_MISMATCH", phase, disp, f"COPY dest outside retained: {r['path']}")
        # Recompute expected inventory + rehash COPY/KEEP + staged refs.
        retained_root_rel = expected_dir + "/retained"
        inv_files, inv_dirs, inv_sizes = _retained_inventory(session, retained_root_rel, phase, disp)
        expected_files: set[str] = set()
        for r in rows:
            if r["policy"] == "COPY_BEFORE_REPLACEMENT":
                expected_files.add(r["retained_dest"])
        expected_files.add(man_rel)
        if set(inv_files) != expected_files:
            raise _fail("INVALID_RETENTION", phase, disp,
                        f"retained inventory mismatch: extra={sorted(set(inv_files) - expected_files)} missing={sorted(expected_files - set(inv_files))}")
        # Exact directory closure: ancestors of expected files + retained root.
        expected_dirs: set[str] = {retained_root_rel}
        for f in expected_files:
            parts = _raw_segments(f)
            for i in range(1, len(parts)):
                # Only dirs below retained root matter; prefix must start with retained root.
                cand = "/".join(parts[:i])
                if cand == retained_root_rel or cand.startswith(retained_root_rel + "/"):
                    expected_dirs.add(cand)
                elif retained_root_rel.startswith(cand):
                    # Ancestor above retained root (proposal dir etc.) not part of retained inventory.
                    pass
        # inv_dirs includes retained_root_rel and all subdirs; require exact.
        if set(inv_dirs) != expected_dirs:
            raise _fail("INVALID_RETENTION", phase, disp,
                        f"retained dir mismatch: extra={sorted(set(inv_dirs) - expected_dirs)} missing={sorted(expected_dirs - set(inv_dirs))}")
        for r in rows:
            if r["policy"] == "COPY_BEFORE_REPLACEMENT":
                _rel, back = session.safe_read(r["retained_dest"], "COPY rehash", phase, disp)
                if core.sha256_bytes(back) != r["sha256"] or len(back) != r["byte_count"]:
                    raise _fail("COPY_DRIFT", phase, disp, f"COPY drift: {r['retained_dest']}")
                if core.sha256_bytes(back) != r["retained_sha256"] or len(back) != r["retained_byte_count"]:
                    raise _fail("COPY_MEASUREMENT_MISMATCH", phase, disp, f"COPY measurement mismatch: {r['retained_dest']}")
            else:
                # EVERY KEEP row: rehash + size (not only Profile).
                session.repinned(r["retained_ref"], f"KEEP recheck {r['path']}", phase, disp,
                                 expected_size=r["byte_count"])
        # Staged authoring/reader refs at exact canonical staged names (no path substitution).
        proposed = proposal.get("proposed") or {}
        authoring_ref = proposed.get("authoring_input_ref") or {}
        reader_ref = proposed.get("proposed_reader_ref") or {}
        expected_authoring = (expected_dir + "/authoring-input.json").replace("//", "/")
        expected_reader = (expected_dir + "/reader-surface-input-v2.json").replace("//", "/")
        if authoring_ref.get("path") != expected_authoring:
            raise _fail("STAGED_PATH_MISMATCH", phase, disp,
                        f"authoring ref path {authoring_ref.get('path')} != canonical {expected_authoring}")
        if reader_ref.get("path") != expected_reader:
            raise _fail("STAGED_PATH_MISMATCH", phase, disp,
                        f"reader ref path {reader_ref.get('path')} != canonical {expected_reader}")
        session.repinned({"path": authoring_ref.get("path", ""), "sha256": authoring_ref.get("sha256", "")},
                         "staged authoring_input_ref", phase, disp)
        session.repinned({"path": reader_ref.get("path", ""), "sha256": reader_ref.get("sha256", "")},
                         "staged proposed_reader_ref", phase, disp)
        # Proposed canonical digest consistency: staged reader bytes must equal
        # the recorded canonical digest, and ref sha must equal canonical sha.
        if reader_ref.get("sha256") != proposed.get("proposed_reader_canonical_sha256"):
            raise _fail("PROPOSED_DIGEST_MISMATCH", phase, disp,
                        "proposed reader ref sha differs from canonical sha")
        _rr, reader_bytes = session.safe_read(expected_reader, "staged proposed reader", phase, disp)
        if core.sha256_bytes(reader_bytes) != proposed.get("proposed_reader_canonical_sha256"):
            raise _fail("PROPOSED_DIGEST_MISMATCH", phase, disp,
                        "staged proposed reader bytes differ from canonical digest")
        # capture_inputs: uniqueness/sorted + required bindings.
        # Required: every original plan path with correct row hash/size, staged
        # refs, proposal, and mandatory P2R deps. Historical extras are
        # observations (not re-proven live); wrong hashes for required paths fail.
        cap = manifest.get("capture_inputs") or []
        if not isinstance(cap, list) or not cap:
            raise _fail("RETENTION_MISMATCH", phase, disp, "capture_inputs empty")
        seen: set[str] = set()
        for e in cap:
            if not isinstance(e, dict) or set(e) != {"path", "sha256"}:
                raise _fail("RETENTION_MISMATCH", phase, disp, "capture_inputs entry must be exact {path,sha256}")
            _check_lexical_path(e["path"], "capture input", phase, disp)
            if not isinstance(e["sha256"], str) or len(e["sha256"]) != 64:
                raise _fail("RETENTION_MISMATCH", phase, disp, "capture_inputs sha invalid")
            if e["path"] in seen:
                raise _fail("RETENTION_MISMATCH", phase, disp, f"capture_inputs duplicate: {e['path']}")
            seen.add(e["path"])
        if [e["path"] for e in cap] != sorted(seen):
            raise _fail("RETENTION_ORDER_MISMATCH", phase, disp, "capture_inputs not sorted-unique by path")
        cmap = {e["path"]: e["sha256"] for e in cap}
        # Mandatory P2R deps must be present with correct current bytes.
        for dep in (P2R_MODULE.as_posix(), MANIFEST_SCHEMA.as_posix()):
            if dep not in cmap:
                raise _fail("MISSING_P2R_DEP", phase, disp, f"capture_inputs missing P2R dep: {dep}")
            _r, live = session.safe_read(dep, "P2R dep binding", phase, disp)
            if core.sha256_bytes(live) != cmap[dep]:
                raise _fail("P2R_DEP_DRIFT", phase, disp, f"P2R dep bytes differ: {dep}")
        # Every original plan path must be in capture_inputs with row hash.
        for r in rows:
            if r["path"] not in cmap:
                raise _fail("CAPTURE_INPUT_MISSING", phase, disp,
                            f"capture_inputs missing required plan path: {r['path']}")
            if cmap[r["path"]] != r["sha256"]:
                raise _fail("CAPTURE_INPUT_MISMATCH", phase, disp,
                            f"capture_inputs wrong hash for plan path: {r['path']}")
        # Staged + proposal must be present with correct hashes.
        for need_path, need_sha in (
            (prop_rel, core.sha256_bytes(prop_data)),
            (expected_authoring, core.sha256_bytes(session.files.get(expected_authoring, b"")) if expected_authoring in session.files else None),
            (expected_reader, core.sha256_bytes(reader_bytes)),
        ):
            if need_path not in cmap:
                raise _fail("CAPTURE_INPUT_MISSING", phase, disp,
                            f"capture_inputs missing required path: {need_path}")
            if need_sha is not None and cmap[need_path] != need_sha:
                raise _fail("CAPTURE_INPUT_MISMATCH", phase, disp,
                            f"capture_inputs wrong hash for required path: {need_path}")
        # KEEP sizes already checked via repinned; COPY sizes via rehash above.
        # Canonical bytes check (projector only for comparison; equality first).
        _check_canonical_bytes(manifest, man_data, phase, disp)
        session.reverify(phase, disp)
        try:
            session._close_all(phase, "VERIFIED")
        except RetentionError as exc:
            raise _fail("CLOSE_FAILED", phase, "INVALID",
                        f"directory close failed before verify success: {exc}", cause=exc) from exc
        return {"result": RESULT_VERIFIED, "manifest_sha256": core.sha256_bytes(man_data),
                "proposal_sha256": core.sha256_bytes(prop_data),
                "checked": {"copy_files": sum(1 for r in rows if r["policy"] == "COPY_BEFORE_REPLACEMENT"),
                            "keep_refs": sum(1 for r in rows if r["policy"] == "KEEP_IMMUTABLE"),
                            "staged_refs": 2}}
    except RetentionError:
        try:
            if not session._closed:
                session._close_all("VERIFY", "INVALID")
        except RetentionError:
            pass
        raise
    except Exception as exc:
        try:
            if not session._closed:
                session._close_all("VERIFY", "INVALID")
        except RetentionError:
            pass
        raise _fail("INVALID_RETENTION", phase, disp, f"unexpected verifier failure: {exc}", cause=exc) from exc
