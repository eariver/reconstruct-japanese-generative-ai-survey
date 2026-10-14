#!/usr/bin/env python3
"""DM021-P2R retention-only capture/readback (one-shot, no promotion).

Two entry points:

  capture_retention(root, state_path, proposal_path) -> result
      Calls unmodified P1 validate_proposal BEFORE writes only, copies old
      bytes into exclusively claimed retained/ root, publishes manifest last.
      Existing retained root refuses (including empty/same-byte foreign).
      No overwrite/retry/adopt/cleanup. Live originals never mutated.

  verify_retention(root, proposal_path, manifest_path) -> result
      Standalone read-only retained-set verification. Never calls P1, never
      calls Git/current HEAD/config authority, never requires mutable live
      COPY originals or current eligibility. Exact proposal -> retained State
      COPY -> State.profile -> matching KEEP Profile -> canonical namespace.

All refusals raise RetentionError (ValueError) with structured
code/phase/disposition/detail/owned/cause. No CLI, no State adoption,
no reason enum, no review production. No assert guards (explicit raises;
safe under python -O).
"""
from __future__ import annotations

import json
import os
import stat as _stat
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


def _norm_rel(value: str | Path, label: str) -> str:
    raw = value.as_posix() if isinstance(value, Path) else str(value)
    if "\\" in raw:
        raise _fail("PATH_TRAVERSAL", "PRE_P1_PIN", "REFUSED_PRE_WRITE", f"{label} must not contain backslashes: {raw}")
    if "//" in raw:
        raise _fail("PATH_TRAVERSAL", "PRE_P1_PIN", "REFUSED_PRE_WRITE", f"{label} has empty segment: {raw}")
    p = Path(raw)
    if p.is_absolute():
        raise _fail("PATH_NOT_REPO_LOCAL", "PRE_P1_PIN", "REFUSED_PRE_WRITE", f"{label} must be repo-relative: {raw}")
    if not raw or raw in (".", "./"):
        raise _fail("PATH_TRAVERSAL", "PRE_P1_PIN", "REFUSED_PRE_WRITE", f"{label} is empty: {raw}")
    parts = p.parts
    for part in parts:
        if part in ("..", ".", ""):
            raise _fail("PATH_TRAVERSAL", "PRE_P1_PIN", "REFUSED_PRE_WRITE", f"{label} has unsafe component: {raw}")
    return raw


def _resolve_to_rel(root_resolved: Path, value: str | Path, label: str, phase: str) -> str:
    raw = value.as_posix() if isinstance(value, Path) else str(value)
    if "\\" in raw:
        raise _fail("PATH_TRAVERSAL", phase, "REFUSED_PRE_WRITE", f"{label} must not contain backslashes: {raw}")
    cand: Path
    if Path(raw).is_absolute():
        cand = Path(raw)
        if ".." in Path(raw).parts:
            raise _fail("PATH_TRAVERSAL", phase, "REFUSED_PRE_WRITE", f"{label} contains dotdot: {raw}")
    else:
        if ".." in Path(raw).parts:
            raise _fail("PATH_TRAVERSAL", phase, "REFUSED_PRE_WRITE", f"{label} contains dotdot: {raw}")
        cand = root_resolved / raw
    try:
        rel = cand.resolve().relative_to(root_resolved).as_posix()
    except ValueError:
        raise _fail("PATH_NOT_REPO_LOCAL", phase, "REFUSED_PRE_WRITE", f"{label} escapes repository: {raw}") from None
    if ".." in Path(rel).parts:
        raise _fail("PATH_TRAVERSAL", phase, "REFUSED_PRE_WRITE", f"{label} escapes after resolve: {raw}")
    return rel


def _loads_strict(data: bytes, label: str, phase: str, disp: str) -> Any:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _fail("MANIFEST_UNREADABLE" if "manifest" in label.lower() else "PROPOSAL_UNREADABLE",
                    phase, disp, f"{label} bytes are not UTF-8: {exc}") from exc

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
        raise _fail("MANIFEST_UNREADABLE" if "manifest" in label.lower() else "PROPOSAL_UNREADABLE",
                    phase, disp, f"{label} is not JSON: {exc}") from exc


def _check_lexical_path(rel: str, label: str, phase: str, disp: str) -> None:
    if "\\" in rel or "//" in rel:
        raise _fail("PATH_TRAVERSAL", phase, disp, f"{label} has unsafe lexical form: {rel}")
    if not rel or Path(rel).is_absolute():
        raise _fail("PATH_NOT_REPO_LOCAL", phase, disp, f"{label} must be repo-relative: {rel}")
    for part in Path(rel).parts:
        if part in ("..", ".", ""):
            raise _fail("PATH_TRAVERSAL", phase, disp, f"{label} has unsafe component: {rel}")


class _Session:
    """Dirfd-relative no-follow safe reader; capture subclass adds writers.

    Holds root dir fd open during invocation; every file/dir accessed
    relative to a pinned parent fd with O_NOFOLLOW|O_NONBLOCK. All fds
    (including directory fds) are closed before successful return; close
    errors fail even when bytes are complete.
    """

    def __init__(self, root: str | Path) -> None:
        self.root_resolved = Path(root).resolve()
        try:
            self.root_fd = os.open(self.root_resolved, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0))
        except OSError as exc:
            raise _fail("PATH_UNREADABLE", "PRE_P1_PIN", "REFUSED_PRE_WRITE", f"cannot open repo root: {exc}") from exc
        try:
            st = os.fstat(self.root_fd)
        except OSError as exc:
            self._close_quiet(self.root_fd)
            raise _fail("PATH_UNREADABLE", "PRE_P1_PIN", "REFUSED_PRE_WRITE", f"cannot fstat repo root: {exc}") from exc
        if not _stat.S_ISDIR(st.st_mode):
            self._close_quiet(self.root_fd)
            raise _fail("PATH_NOT_REGULAR", "PRE_P1_PIN", "REFUSED_PRE_WRITE", "repo root is not a directory")
        self.root_id = (st.st_dev, st.st_ino, _stat.S_IMODE(st.st_mode))
        self.files: dict[str, bytes] = {}
        self.file_ids: dict[str, tuple[int, int, int]] = {}
        self.dir_ids: dict[str, tuple[int, int, int]] = {".": self.root_id}
        self._open_fds: list[int] = [self.root_fd]
        self._closed = False

    @staticmethod
    def _close_quiet(fd: int) -> None:
        try:
            os.close(fd)
        except OSError:
            pass

    def _close_all(self, phase: str, disp: str, prior: BaseException | None = None) -> None:
        # Close every held fd; preserve prior error if cleanup-close also fails.
        first: BaseException | None = prior
        for fd in reversed(self._open_fds):
            try:
                os.close(fd)
            except OSError as exc:
                if first is None:
                    first = _fail("CLOSE_FAILED", phase, disp, f"descriptor close failed: {exc}", cause=exc)
                # else preserve original; secondary recorded by caller via owned
        self._open_fds = []
        self._closed = True
        if first is not None and prior is None:
            raise first

    def _split(self, rel: str) -> tuple[list[str], str]:
        parts = list(Path(rel).parts)
        if len(parts) == 0:
            raise _fail("PATH_TRAVERSAL", "PRE_P1_PIN", "REFUSED_PRE_WRITE", f"empty path: {rel}")
        return parts[:-1], parts[-1]

    def _open_dir_chain(self, dir_parts: list[str], label: str, phase: str, disp: str) -> int:
        # Open each ancestor relative to parent with NOFOLLOW; return deepest fd.
        parent = self.root_fd
        cur_parts: list[str] = []
        for part in dir_parts:
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
                self._close_quiet(fd)
                raise _fail("PATH_UNREADABLE", phase, disp, f"{label} ancestor fstat failed: {'/'.join(cur_parts)}: {exc}") from exc
            if not _stat.S_ISDIR(st.st_mode):
                self._close_quiet(fd)
                raise _fail("PATH_NOT_REGULAR", phase, disp, f"{label} ancestor not a directory: {'/'.join(cur_parts)}")
            self._open_fds.append(fd)
            rel = "/".join(cur_parts)
            self.dir_ids[rel] = (st.st_dev, st.st_ino, _stat.S_IMODE(st.st_mode))
            parent = fd
        return parent

    def _entry_identity(self, parent_fd: int, name: str, label: str, phase: str, disp: str) -> tuple[int, int, int, int]:
        # Current name entry from pinned parent fd (detects pathname replacement
        # even when a held fd's fstat is unchanged). Returns (dev,ino,mode,is_symlink).
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
        rel = _resolve_to_rel(self.root_resolved, value, label, phase)
        _check_lexical_path(rel, label, phase, disp)
        dir_parts, leaf = self._split(rel)
        mark = len(self._open_fds)
        try:
            parent = self._open_dir_chain(dir_parts, label, phase, disp) if dir_parts else self.root_fd
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
            try:
                st = os.fstat(fd)
            except OSError as exc:
                raise _fail("PATH_UNREADABLE", phase, disp, f"{label} fstat failed: {rel}: {exc}") from exc
            if not _stat.S_ISREG(st.st_mode):
                raise _fail("PATH_NOT_REGULAR", phase, disp, f"{label} not regular after open: {rel}")
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
            self._open_fds.remove(fd)
            self.file_ids[rel] = (st.st_dev, st.st_ino, len(data))
            prev = self.files.get(rel)
            if prev is not None and prev != data:
                raise _fail("STABILITY_VIOLATION", phase, disp, f"{label} changed mid-inspection: {rel}")
            self.files[rel] = data
            return rel, data
        finally:
            while len(self._open_fds) > mark:
                extra = self._open_fds.pop()
                if extra != self.root_fd:
                    self._close_quiet(extra)

    def repinned(self, ref: dict[str, Any], label: str, phase: str, disp: str) -> str:
        if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
            raise _fail("REF_SHAPE", phase, disp, f"{label} is not an exact {{path,sha256}} record")
        if not isinstance(ref["path"], str) or not isinstance(ref["sha256"], str) or len(ref["sha256"]) != 64:
            raise _fail("REF_SHAPE", phase, disp, f"{label} has invalid path/sha256")
        rel, data = self.safe_read(ref["path"], label, phase, disp)
        if core.sha256_bytes(data) != ref["sha256"]:
            raise _fail("REF_DRIFT", phase, disp, f"{label} bytes differ from recorded sha256: {rel}")
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
                        self._close_quiet(extra)


def _validate_roles_sorted_unique(roles: Any, label: str, phase: str, disp: str) -> None:
    if not isinstance(roles, list) or len(roles) == 0 or not all(isinstance(r, str) and r for r in roles):
        raise _fail("RETENTION_MISMATCH", phase, disp, f"{label} roles must be nonempty string list")
    if roles != sorted(roles):
        raise _fail("RETENTION_ORDER_MISMATCH", phase, disp, f"{label} roles not sorted-unique")
    if len(set(roles)) != len(roles):
        raise _fail("RETENTION_MISMATCH", phase, disp, f"{label} roles have duplicates")


def _project_manifest_canonical(manifest: dict[str, Any], phase: str, disp: str) -> dict[str, Any]:
    # Deterministic key-order projector for canonical-byte check ONLY.
    # Never accepts omitted/extra data (schema + equality checks run first).
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
            basis[k] = manifest["basis"][k]
        ci = manifest["basis"]["contract_identity"]
        cio: dict[str, Any] = {}
        for k in _CONTRACT_ORDER:
            cio[k] = ci[k]
        basis["contract_identity"] = cio
        out["basis"] = basis
        prop: dict[str, Any] = {}
        for k in _PROPOSED_ORDER:
            prop[k] = manifest["proposed"][k]
        out["proposed"] = prop
        rows: list[dict[str, Any]] = []
        for row in manifest["rows"]:
            order = _ROW_COPY_ORDER if row.get("policy") == "COPY_BEFORE_REPLACEMENT" else _ROW_KEEP_ORDER
            r: dict[str, Any] = {}
            for k in order:
                r[k] = row[k]
            rows.append(r)
        out["rows"] = rows
        out["capture_inputs"] = [{"path": e["path"], "sha256": e["sha256"]} for e in manifest["capture_inputs"]]
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
        paths.add(r)
    if not isinstance(contracts, dict):
        raise _fail("CONFIG_UNREADABLE", phase, disp, "contract_files invalid")
    for rows in contracts.values():
        if not isinstance(rows, list):
            raise _fail("CONFIG_UNREADABLE", phase, disp, "contract_files row invalid")
        for p in rows:
            if not isinstance(p, str):
                raise _fail("CONFIG_UNREADABLE", phase, disp, "contract_files entry invalid")
            paths.add(p)
    return sorted(paths)


def _snapshot_expanded(session: _Session, rels_or_roots: list[str], kind: str,
                       phase: str, disp: str) -> tuple[dict[str, str], dict[str, str]]:
    # Strict snapshot: regular file hashes + directory inventory (incl. empty
    # dirs). Fails on walk/stat errors. Returns (files, dirs).
    files: dict[str, str] = {}
    dirs: dict[str, str] = {}
    for base in rels_or_roots:
        _check_lexical_path(base, f"{kind} base", phase, disp) if "/" not in base and "." not in base else None
        # Resolve base: it may be a dir root or a file path.
        full = session.root_resolved / base
        try:
            st = full.lstat()
        except OSError as exc:
            raise _fail("TREE_MISSING", phase, disp, f"{kind} base missing: {base}: {exc}") from exc
        if _stat.S_ISLNK(st.st_mode):
            raise _fail("TREE_ALIAS", phase, disp, f"{kind} base is symlink: {base}")
        if _stat.S_ISDIR(st.st_mode):
            for dirpath, dirnames, filenames in os.walk(full, topdown=True, followlinks=False):
                try:
                    rel_dir = Path(dirpath).resolve().relative_to(session.root_resolved).as_posix()
                except ValueError:
                    raise _fail("PATH_NOT_REPO_LOCAL", phase, disp, f"{kind} tree escapes root: {dirpath}") from None
                for d in list(dirnames):
                    fp = Path(dirpath) / d
                    try:
                        lst = fp.lstat()
                    except OSError as exc:
                        raise _fail("PATH_UNREADABLE", phase, disp, f"{kind} dir unreadable: {fp}: {exc}") from exc
                    if _stat.S_ISLNK(lst.st_mode):
                        raise _fail("TREE_ALIAS", phase, disp, f"symlink directory inside {kind} tree: {rel_dir}/{d}")
                    if not fp.is_dir():
                        raise _fail("TREE_NOT_DIR", phase, disp, f"non-directory inside {kind} tree: {fp}")
                    if d == ".git":
                        dirnames.remove(d)
                if ".git" in dirnames:
                    dirnames.remove(".git")
                if rel_dir != ".":
                    dirs[rel_dir] = f"DIR:{oct(_stat.S_IMODE(st.st_mode))}"
                for name in filenames:
                    fp = Path(dirpath) / name
                    try:
                        rel = fp.resolve().relative_to(session.root_resolved).as_posix()
                    except ValueError:
                        raise _fail("PATH_NOT_REPO_LOCAL", phase, disp, f"{kind} file escapes root: {fp}") from None
                    if fp.is_symlink():
                        raise _fail("TREE_ALIAS", phase, disp, f"symlink inside {kind} tree: {rel}")
                    try:
                        lst = fp.lstat()
                    except OSError as exc:
                        raise _fail("PATH_UNREADABLE", phase, disp, f"{kind} file unreadable: {rel}: {exc}") from exc
                    if not _stat.S_ISREG(lst.st_mode):
                        raise _fail("TREE_NOT_REGULAR", phase, disp, f"non-regular file inside {kind} tree: {rel}")
                    _rel, data = session.safe_read(rel, f"{kind} file", phase, disp)
                    files[_rel] = core.sha256_bytes(data)
        elif _stat.S_ISREG(st.st_mode):
            _rel, data = session.safe_read(base, f"{kind} file", phase, disp)
            files[_rel] = core.sha256_bytes(data)
        else:
            raise _fail("TREE_NOT_REGULAR", phase, disp, f"{kind} base not regular/dir: {base}")
    return files, dirs


def _retained_inventory(session: _Session, retained_rel: str, phase: str, disp: str) -> tuple[dict[str, str], dict[str, str]]:
    # Full inventory below retained/ (files + dirs incl. empty, no-follow).
    full = session.root_resolved / retained_rel
    try:
        lst = full.lstat()
    except OSError as exc:
        raise _fail("INCOMPLETE_RETENTION", phase, disp, f"retained root missing: {retained_rel}: {exc}") from exc
    if _stat.S_ISLNK(lst.st_mode) or not full.is_dir():
        raise _fail("INVALID_RETENTION", phase, disp, f"retained root not a directory: {retained_rel}")
    files: dict[str, str] = {}
    dirs: dict[str, str] = {}
    for dirpath, dirnames, filenames in os.walk(full, topdown=True, followlinks=False):
        try:
            rel_dir = Path(dirpath).resolve().relative_to(session.root_resolved).as_posix()
        except ValueError:
            raise _fail("PATH_NOT_REPO_LOCAL", phase, disp, "retained tree escapes root") from None
        for d in list(dirnames):
            fp = Path(dirpath) / d
            try:
                lst_d = fp.lstat()
                if _stat.S_ISLNK(lst_d.st_mode):
                    raise _fail("INVALID_RETENTION", phase, disp, f"unexpected alias below retained/: {rel_dir}/{d}")
            except RetentionError:
                raise
            except OSError as exc:
                raise _fail("PATH_UNREADABLE", phase, disp, f"retained dir unreadable: {fp}: {exc}") from exc
        dirs[rel_dir] = "DIR"
        for name in filenames:
            fp = Path(dirpath) / name
            try:
                rel = fp.resolve().relative_to(session.root_resolved).as_posix()
            except ValueError:
                raise _fail("PATH_NOT_REPO_LOCAL", phase, disp, "retained file escapes root") from None
            if fp.is_symlink():
                raise _fail("INVALID_RETENTION", phase, disp, f"unexpected alias below retained/: {rel}")
            try:
                lst2 = fp.lstat()
            except OSError as exc:
                raise _fail("PATH_UNREADABLE", phase, disp, f"retained file unreadable: {rel}: {exc}") from exc
            if not _stat.S_ISREG(lst2.st_mode):
                raise _fail("INVALID_RETENTION", phase, disp, f"unexpected special below retained/: {rel}")
            _rel, data = session.safe_read(rel, "retained file", phase, disp)
            files[_rel] = core.sha256_bytes(data)
    return files, dirs


def _validate_proposal_shape(proposal: Any, phase: str, disp: str) -> None:
    if not isinstance(proposal, dict):
        raise _fail("PROPOSAL_UNREADABLE", phase, disp, "proposal is not a JSON object")


def capture_retention(root: str | Path, state_path: str | Path, proposal_path: str | Path) -> dict[str, Any]:
    """One-shot retention capture. See module docstring."""
    # Lazy P1 import preserves verifier separation (no module-level P1).
    from scripts import survey_editorial_correction_proposal_v2 as p1  # noqa: PLC0415

    session = _Session(root)
    owned: dict[str, Any] = {"retained_root": None, "owned_files": [], "observed_extra": []}
    phase = "PRE_P1_PIN"
    disp = "REFUSED_PRE_WRITE"
    try:
        # 1. Narrow pins before P1 (no broad walk from unvalidated Profile).
        state_rel, state_data = session.safe_read(str(state_path), "Production State", phase, disp)
        try:
            state = json.loads(state_data.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise _fail("STATE_UNREADABLE", phase, disp, f"Production State not JSON: {exc}") from exc
        if not isinstance(state, dict):
            raise _fail("STATE_UNREADABLE", phase, disp, "Production State is not an object")
        cfg_rel, cfg_data = session.safe_read(core.DEFAULT_CONFIG.as_posix(), "implementation config", phase, disp)
        try:
            cfg = json.loads(cfg_data.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise _fail("CONFIG_UNREADABLE", phase, disp, f"config not JSON: {exc}") from exc
        prof_ref = state.get("profile") or {}
        if not isinstance(prof_ref, dict) or set(prof_ref) != {"path", "sha256"}:
            raise _fail("STATE_PROFILE_SHAPE", phase, disp, "State lacks exact Production Profile reference")
        prof_rel, prof_data = session.safe_read(prof_ref["path"], "State-bound Production Profile", phase, disp)
        if core.sha256_bytes(prof_data) != prof_ref.get("sha256"):
            raise _fail("PROFILE_DRIFT", phase, disp, "State-bound Profile bytes drifted")
        try:
            profile = json.loads(prof_data.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise _fail("PROFILE_UNREADABLE", phase, disp, f"Profile not JSON: {exc}") from exc
        prop_rel, prop_data = session.safe_read(str(proposal_path), "editorial correction proposal", phase, disp)
        if Path(prop_rel).name != PROPOSAL_FILENAME:
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
        except (KeyError, TypeError) as exc:
            raise _fail("PROFILE_ROOT_INVALID", phase, disp, f"profile source_root invalid: {exc}") from exc
        expected_dir = (Path(source_root_rel) / "publication" / "v2" / "editorial-corrections" / proposal_id).as_posix()
        retained_rel = (expected_dir + "/retained").replace("//", "/")
        _check_lexical_path(expected_dir, "proposal dir", phase, disp)
        retained_full = session.root_resolved / retained_rel
        try:
            if retained_full.is_symlink() or retained_full.exists():
                raise _fail("RETAINED_ROOT_EXISTS", phase, disp,
                            f"retained root already present (no overwrite/takeover): {retained_rel}")
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

        # 2. P1 call (before writes only).
        phase = "P1_CALL"
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
            # validate_proposal returns supplied UNCHANGED; any repair diverges.
            raise _fail("PROPOSAL_MISMATCH", phase, disp, "P1 measured proposal differs from supplied bytes", owned)
        # Compare every P1 input hash immediately (no replacing mismatches).
        phase = "POST_P1_SNAPSHOT"
        for rel, sha in p1_hashes.items():
            _check_lexical_path(rel, "P1 input", phase, disp)
            _rel, live = session.safe_read(rel, "P1 input recheck", phase, disp)
            if core.sha256_bytes(live) != sha:
                raise _fail("STABILITY_VIOLATION", phase, disp,
                            f"P1 input changed around P1 call: {rel}", owned)

        # 3. Full validated snapshots before any write.
        control_list = _control_paths(cfg, phase, disp)
        control_files: dict[str, str] = {}
        for cp in control_list:
            full = session.root_resolved / cp
            try:
                lst = full.lstat()
            except OSError:
                continue  # Roots may be dirs or absent files; walker below handles dirs; missing files: P1 already validated authority, skip silently? No — fail closed only for required? Control snapshot records what exists; missing contract file would have failed P1 receipt recheck already. Skip absent.
            if _stat.S_ISDIR(lst.st_mode) and not full.is_symlink():
                continue  # Expanded below via walker over roots.
            if _stat.S_ISREG(lst.st_mode):
                _rel, data = session.safe_read(cp, "control file", phase, disp)
                control_files[_rel] = core.sha256_bytes(data)
        # Expand dir roots.
        try:
            impl_roots = cfg["implementation_control_roots"]
        except KeyError as exc:
            raise _fail("CONFIG_UNREADABLE", phase, disp, f"missing implementation_control_roots: {exc}") from exc
        for r in impl_roots:
            fmap, _dmap = _snapshot_expanded(session, [r], "control root", phase, disp)
            control_files.update(fmap)
        try:
            survey_root_rel = profile["paths"]["survey_root"]
        except (KeyError, TypeError) as exc:
            raise _fail("PROFILE_ROOT_INVALID", phase, disp, f"profile survey_root invalid: {exc}") from exc
        edition_files, edition_dirs = _snapshot_expanded(session, [source_root_rel, survey_root_rel],
                                                        "edition tree", phase, disp)

        # 4. Preflight (no writes on failure).
        phase = "PREFLIGHT"
        disp = "REFUSED_PRE_WRITE"
        plan = supplied.get("retention_plan") or []
        if not isinstance(plan, list) or not plan:
            raise _fail("RETENTION_MISMATCH", phase, disp, "P1 retention plan empty")
        seen_dest: set[str] = set()
        copy_rows: list[dict[str, Any]] = []
        keep_rows: list[dict[str, Any]] = []
        for row in plan:
            if not isinstance(row, dict):
                raise _fail("RETENTION_MISMATCH", phase, disp, "retention row not an object")
            for k in ("roles", "path", "sha256", "byte_count", "policy"):
                if k not in row:
                    raise _fail("RETENTION_MISMATCH", phase, disp, f"retention row missing {k}")
            _validate_roles_sorted_unique(row["roles"], f"retention {row.get('path')}", phase, disp)
            _check_lexical_path(row["path"], "retention source", phase, disp)
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
                if dfull.is_symlink() or dfull.exists():
                    raise _fail("RETENTION_DEST_CONFLICT", phase, disp,
                                f"retention destination already present: {dest}")
            except OSError as exc:
                raise _fail("PATH_UNREADABLE", phase, disp, f"retention dest unreadable: {dest}: {exc}") from exc
            _rel, live_bytes = session.safe_read(row["path"], "COPY source", phase, disp)
            if core.sha256_bytes(live_bytes) != row["sha256"] or len(live_bytes) != row["byte_count"]:
                raise _fail("REF_DRIFT", phase, disp, f"COPY source bytes differ from plan: {row['path']}")
        for row in keep_rows:
            session.repinned(row["retained_ref"], f"KEEP ref {row['path']}", phase, disp)

        # 5. Exclusive claim + dirfd-relative writes.
        phase = "CLAIM"
        disp = "OWNED_PARTIAL"
        # Re-check retained absence under parent fd (detects replacement).
        dir_parts, leaf = session._split(retained_rel)
        mark = len(session._open_fds)
        parent_fd = session._open_dir_chain(dir_parts, "proposal parent", phase, disp) if dir_parts else session.root_fd
        ent_exists = True
        try:
            os.stat(leaf, dir_fd=parent_fd, follow_symlinks=False)
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
        root_id = (rst.st_dev, rst.st_ino)
        owned["retained_root"] = {"path": retained_rel, "dev": rst.st_dev, "ino": rst.st_ino,
                                  "mode": oct(_stat.S_IMODE(rst.st_mode))}
        retained_fd = rf
        # Parent chain + retained fd stay held until final close (no pop;
        # popping would close parent_fd and break replacement detection).

        def _check_root_live(op: str) -> None:
            try:
                cur = os.stat(leaf, dir_fd=parent_fd, follow_symlinks=False)
            except OSError as exc:
                raise _fail("ROOT_IDENTITY_CHANGED", "WRITE", "OWNED_PARTIAL",
                            f"retained root entry lost during {op}: {exc}", owned) from exc
            if (cur.st_dev, cur.st_ino) != root_id or not _stat.S_ISDIR(cur.st_mode):
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
        # Build ancestor dirs under retained root (dirfd-relative, one level at a time).
        needed_dirs: set[str] = set()
        for row in copy_rows:
            dest_rel = row["retained_dest"]
            sub = dest_rel[len(retained_rel) + 1:]
            parts = list(Path(sub).parts)[:-1]
            cur = ""
            for part in parts:
                cur = cur + "/" + part if cur else part
                needed_dirs.add(cur)
        # Map sub-rel -> fd (retained_fd is base).
        dirfd_map: dict[str, int] = {"": retained_fd}
        secondary_close_error: BaseException | None = None
        try:
            _check_root_live("ancestor-build")
            for sub in sorted(needed_dirs):
                parent_sub = "/".join(sub.split("/")[:-1])
                name = sub.split("/")[-1]
                pfd = dirfd_map[parent_sub]
                try:
                    try:
                        os.stat(name, dir_fd=pfd, follow_symlinks=False)
                        raise _fail("RETENTION_DEST_CONFLICT", phase, "OWNED_PARTIAL",
                                    f"retained ancestor already present: {sub}", owned)
                    except FileNotFoundError:
                        pass
                    os.mkdir(name, 0o777, dir_fd=pfd)
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
                dirfd_map[sub] = dfd
            # Write each COPY exclusively via its parent fd.
            for row in copy_rows:
                _check_root_live(f"write {row['retained_dest']}")
                dest_rel = row["retained_dest"]
                sub = dest_rel[len(retained_rel) + 1:]
                parts = list(Path(sub).parts)
                parent_sub = "/".join(parts[:-1])
                name = parts[-1]
                pfd = dirfd_map[parent_sub]
                src_rel = row["path"]
                data = session.files.get(src_rel)
                if data is None:
                    _rel, data = session.safe_read(src_rel, "COPY source resnapshot", phase, "OWNED_PARTIAL")
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
                    view = memoryview(data)
                    total = 0
                    while total < len(data):
                        try:
                            n = os.write(wfd, view[total:])
                        except OSError as exc:
                            raise _fail("WRITE_FAILED", phase, "OWNED_PARTIAL",
                                        f"write failed: {dest_rel}: {exc}", owned) from exc
                        if n == 0:
                            raise _fail("WRITE_FAILED", phase, "OWNED_PARTIAL",
                                        f"zero-progress write: {dest_rel}", owned)
                        total += n
                    try:
                        os.fsync(wfd)
                    except OSError as exc:
                        raise _fail("WRITE_FAILED", phase, "OWNED_PARTIAL",
                                    f"fsync failed: {dest_rel}: {exc}", owned) from exc
                finally:
                    try:
                        os.close(wfd)
                    except OSError as exc:
                        if secondary_close_error is None:
                            secondary_close_error = exc
                        raise _fail("CLOSE_FAILED", phase, "OWNED_PARTIAL",
                                    f"close after write failed: {dest_rel}: {exc}", owned) from exc
                    finally:
                        if wfd in session._open_fds:
                            session._open_fds.remove(wfd)
                owned["owned_files"].append({"path": dest_rel, "bytes": len(data)})
                _check_root_live(f"after write {dest_rel}")
                _rel, back = session.safe_read(dest_rel, "COPY readback", phase, "OWNED_PARTIAL")
                if core.sha256_bytes(back) != row["sha256"] or len(back) != row["byte_count"]:
                    raise _fail("READBACK_MISMATCH", phase, "OWNED_PARTIAL",
                                f"COPY readback mismatch: {dest_rel}", owned)
        except RetentionError as exc:
            # Attach secondary close error context without losing original.
            if secondary_close_error is not None and exc.__cause__ is None:
                owned.setdefault("secondary_close_error", str(secondary_close_error))
            raise

        # 6. Late rechecks before manifest (allow only owned delta).
        phase = "FINALIZE"
        for rel, sha in p1_hashes.items():
            _rel, live = session.safe_read(rel, "final input recheck", phase, "OWNED_PARTIAL")
            if core.sha256_bytes(live) != sha:
                raise _fail("FINALIZATION_REFUSED", phase, "OWNED_PARTIAL",
                            f"input drift before finalization: {rel}", owned)
        for row in copy_rows:
            _rel, back = session.safe_read(row["retained_dest"], "final retained recheck", phase, "OWNED_PARTIAL")
            if core.sha256_bytes(back) != row["sha256"]:
                raise _fail("FINALIZATION_REFUSED", phase, "OWNED_PARTIAL",
                            f"retained drift before finalization: {row['retained_dest']}", owned)
        for row in keep_rows:
            session.repinned(row["retained_ref"], "final KEEP recheck", phase, "OWNED_PARTIAL")
        # Edition/control inventories: only owned additions allowed.
        edition_files2, _e2 = _snapshot_expanded(session, [source_root_rel, survey_root_rel],
                                                "edition tree final", phase, "OWNED_PARTIAL")
        owned_set = {r["retained_dest"] for r in copy_rows}
        for rel, sha in edition_files2.items():
            if rel in edition_files:
                if edition_files[rel] != sha:
                    raise _fail("FINALIZATION_REFUSED", phase, "OWNED_PARTIAL",
                                f"edition drift before finalization: {rel}", owned)
            elif rel in owned_set or rel.startswith(retained_rel + "/"):
                pass  # Owned retention delta allowed (COPY + ancestors).
            else:
                # Proposal dir itself (authoring/reader/proposal.json) is expected
                # pre-existing (staged before P1), not an owned addition; it must
                # have been in the pre-write snapshot if still present. New files
                # outside owned retained subtree refuse.
                if rel.startswith(expected_dir + "/") and rel in session.files:
                    pass
                else:
                    raise _fail("FINALIZATION_REFUSED", phase, "OWNED_PARTIAL",
                                f"unexpected edition addition before finalization: {rel}", owned)
        # Do not discard retained/proposal entries: require previously known
        # edition entries still present (except nothing may disappear).
        for rel in edition_files:
            if rel not in edition_files2:
                raise _fail("FINALIZATION_REFUSED", phase, "OWNED_PARTIAL",
                            f"edition disappearance before finalization: {rel}", owned)

        # 7. Manifest-last (exclusive create, fsync, close-checked, readback).
        phase = "MANIFEST_PUBLISH"
        p2r_mod_rel, p2r_mod_data = session.safe_read(P2R_MODULE.as_posix(), "P2R module final", phase, "OWNED_PARTIAL")
        p2r_sch_rel, p2r_sch_data = session.safe_read(MANIFEST_SCHEMA.as_posix(), "P2R schema final", phase, "OWNED_PARTIAL")
        cap_inputs = [{"path": k, "sha256": v} for k, v in sorted(p1_hashes.items())]
        cap_inputs.append({"path": p2r_mod_rel, "sha256": core.sha256_bytes(p2r_mod_data)})
        cap_inputs.append({"path": p2r_sch_rel, "sha256": core.sha256_bytes(p2r_sch_data)})
        # Dedupe by path (P1 already includes config etc.; P2R deps are new paths).
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
                base["retained_ref"] = dict(row["retained_ref"])
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
        manifest_parent_sub = "/".join(list(Path(manifest_rel[len(retained_rel) + 1:]).parts)[:-1])
        mpfd = dirfd_map[manifest_parent_sub] if manifest_parent_sub else retained_fd
        mname = list(Path(manifest_rel[len(retained_rel) + 1:]).parts)[-1] if manifest_parent_sub else MANIFEST_FILENAME
        _check_root_live("manifest publish")
        try:
            mfd = os.open(mname, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0),
                          0o664, dir_fd=mpfd)
        except FileExistsError as exc:
            raise _fail("RETENTION_DEST_CONFLICT", phase, "OWNED_PARTIAL",
                        f"manifest already present: {manifest_rel}: {exc}", owned) from exc
        except OSError as exc:
            raise _fail("WRITE_FAILED", phase, "OWNED_PARTIAL",
                        f"manifest open failed: {manifest_rel}: {exc}", owned) from exc
        session._open_fds.append(mfd)
        try:
            view = memoryview(manifest_bytes)
            total = 0
            while total < len(manifest_bytes):
                try:
                    n = os.write(mfd, view[total:])
                except OSError as exc:
                    raise _fail("MANIFEST_CLOSE_FAILED", phase, "OWNED_PARTIAL",
                                f"manifest write failed: {exc}", owned) from exc
                if n == 0:
                    raise _fail("MANIFEST_CLOSE_FAILED", phase, "OWNED_PARTIAL",
                                "manifest zero-progress write", owned)
                total += n
            try:
                os.fsync(mfd)
            except OSError as exc:
                raise _fail("MANIFEST_CLOSE_FAILED", phase, "OWNED_PARTIAL",
                            f"manifest fsync failed: {exc}", owned) from exc
        finally:
            try:
                os.close(mfd)
            except OSError as exc:
                raise _fail("MANIFEST_CLOSE_FAILED", phase, "OWNED_PARTIAL",
                            f"manifest close failed: {exc}", owned) from exc
            finally:
                if mfd in session._open_fds:
                    session._open_fds.remove(mfd)
        _rel, back = session.safe_read(manifest_rel, "manifest readback", phase, "OWNED_PARTIAL")
        if back != manifest_bytes:
            raise _fail("READBACK_MISMATCH", phase, "OWNED_PARTIAL", "manifest readback mismatch", owned)
        manifest_sha = core.sha256_bytes(back)
        # Standalone verification + final no-drift before reporting success.
        session.reverify(phase, "OWNED_PARTIAL")
        # Close all dir fds before successful return (close errors fail).
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
        return {"result": RESULT_CAPTURED, "manifest_path": manifest_rel, "manifest_sha256": manifest_sha,
                "proposal_sha256": core.sha256_bytes(prop_data),
                "input_hashes": {e["path"]: e["sha256"] for e in cap_inputs},
                "retained": {"copy_files": len(copy_rows), "keep_refs": len(keep_rows),
                             "manifest_bytes": len(manifest_bytes)}}
    except RetentionError:
        # Preserve partials; close held fds (best effort, original error wins).
        try:
            if not session._closed:
                session._close_all("WRITE" if phase in ("CLAIM", "WRITE", "FINALIZE", "MANIFEST_PUBLISH") else phase,
                                   "OWNED_PARTIAL" if phase in ("CLAIM", "WRITE", "FINALIZE", "MANIFEST_PUBLISH") else disp)
        except RetentionError:
            pass
        raise
    except Exception as exc:
        try:
            if not session._closed:
                session._close_all(phase, disp)
        except RetentionError:
            pass
        raise _fail("WRITE_FAILED", phase, disp, f"unexpected capture failure: {exc}", owned, cause=exc) from exc


def verify_retention(root: str | Path, proposal_path: str | Path, manifest_path: str | Path) -> dict[str, Any]:
    """Standalone read-only retained-set verification (no P1/Git/HEAD)."""
    session = _Session(root)
    phase = "VERIFY"
    disp = "INVALID"
    try:
        prop_rel, prop_data = session.safe_read(str(proposal_path), "editorial correction proposal", phase, disp)
        if Path(prop_rel).name != PROPOSAL_FILENAME:
            raise _fail("PROPOSAL_FILENAME", phase, disp, "proposal file must be named proposal.json")
        proposal = _loads_strict(prop_data, "editorial correction proposal", phase, disp)
        _validate_proposal_shape(proposal, phase, disp)
        man_rel, man_data = session.safe_read(str(manifest_path), "retention manifest", phase, disp)
        if Path(man_rel).name != MANIFEST_FILENAME:
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
        for k in ("schema_version", "proposal_id", "issue_id", "research_profile", "publication_profile"):
            if proposal.get(k) != manifest.get("proposal_ref", {}).get(k if k != "schema_version" else "path") and k == "schema_version":
                pass  # proposal schema_version checked separately below
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
        # Duplicate path check.
        paths = [r["path"] for r in rows]
        if len(set(paths)) != len(paths):
            raise _fail("RETENTION_MISMATCH", phase, disp, "duplicate retention paths")
        # I1 chain: state:authority COPY -> retained State -> State.profile -> KEEP Profile.
        basis = proposal.get("basis") or {}
        state_ref = basis.get("state_ref") or {}
        if set(state_ref) != {"path", "sha256"}:
            raise _fail("BASIS_MISMATCH", phase, disp, "basis.state_ref must be exact {path,sha256}")
        state_rows = [r for r in rows if "state:authority" in (r.get("roles") or [])]
        if len(state_rows) != 1:
            raise _fail("INVALID_RETENTION", phase, disp, "unique state:authority row required")
        srow = state_rows[0]
        if srow.get("policy") != "COPY_BEFORE_REPLACEMENT":
            raise _fail("INVALID_RETENTION", phase, disp, "state:authority must be COPY")
        if srow.get("path") != state_ref.get("path") or srow.get("sha256") != state_ref.get("sha256"):
            raise _fail("INVALID_RETENTION", phase, disp, "state:authority row must equal basis.state_ref")
        if "retained_dest" not in srow:
            raise _fail("INVALID_RETENTION", phase, disp, "state:authority lacks retained_dest")
        _srel, sdata = session.safe_read(srow["retained_dest"], "retained State", phase, disp)
        if core.sha256_bytes(sdata) != srow["sha256"] or len(sdata) != srow["byte_count"]:
            raise _fail("INVALID_RETENTION", phase, disp, "retained State bytes differ from row")
        try:
            rstate = json.loads(sdata.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise _fail("INVALID_RETENTION", phase, disp, f"retained State not JSON: {exc}") from exc
        if not isinstance(rstate, dict):
            raise _fail("INVALID_RETENTION", phase, disp, "retained State not an object")
        rprof = rstate.get("profile") or {}
        if not isinstance(rprof, dict) or set(rprof) != {"path", "sha256"}:
            raise _fail("INVALID_RETENTION", phase, disp, "retained State lacks exact profile ref")
        matches = [r for r in rows if r.get("policy") == "KEEP_IMMUTABLE"
                   and r.get("retained_ref", {}).get("path") == rprof.get("path")
                   and r.get("retained_ref", {}).get("sha256") == rprof.get("sha256")]
        if len(matches) != 1:
            raise _fail("INVALID_RETENTION", phase, disp, "unique matching KEEP Profile row required")
        prow_match = matches[0]
        _prel, pdata = session.safe_read(prow_match["retained_ref"]["path"], "required KEEP Profile", phase, disp)
        if core.sha256_bytes(pdata) != rprof.get("sha256") or len(pdata) != prow_match["byte_count"]:
            raise _fail("INVALID_RETENTION", phase, disp, "KEEP Profile bytes drifted")
        try:
            rprofile = json.loads(pdata.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise _fail("INVALID_RETENTION", phase, disp, f"KEEP Profile not JSON: {exc}") from exc
        # Issue/label agreement across proposal, retained State, Profile.
        if rstate.get("issue_id") != proposal.get("issue_id"):
            raise _fail("INVALID_RETENTION", phase, disp, "retained State issue differs from proposal")
        if rprofile.get("issue_id") != proposal.get("issue_id"):
            raise _fail("INVALID_RETENTION", phase, disp, "KEEP Profile issue differs from proposal")
        for k in ("research_profile", "publication_profile"):
            if rprofile.get(k) != proposal.get(k):
                raise _fail("INVALID_RETENTION", phase, disp, f"KEEP Profile {k} differs from proposal")
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
        # Recompute expected inventory + rehash COPY/KEEP + staged refs.
        retained_root_rel = expected_dir + "/retained"
        inv_files, _inv_dirs = _retained_inventory(session, retained_root_rel, phase, disp)
        expected_files: set[str] = set()
        for r in rows:
            if r["policy"] == "COPY_BEFORE_REPLACEMENT":
                expected_files.add(r["retained_dest"])
        expected_files.add(man_rel)
        if set(inv_files) != expected_files:
            raise _fail("INVALID_RETENTION", phase, disp,
                        f"retained inventory mismatch: extra={sorted(set(inv_files) - expected_files)} missing={sorted(expected_files - set(inv_files))}")
        for r in rows:
            if r["policy"] == "COPY_BEFORE_REPLACEMENT":
                _rel, back = session.safe_read(r["retained_dest"], "COPY rehash", phase, disp)
                if core.sha256_bytes(back) != r["sha256"] or len(back) != r["byte_count"]:
                    raise _fail("INVALID_RETENTION", phase, disp, f"COPY drift: {r['retained_dest']}")
                if core.sha256_bytes(back) != r["retained_sha256"] or len(back) != r["retained_byte_count"]:
                    raise _fail("INVALID_RETENTION", phase, disp, f"COPY measurement mismatch: {r['retained_dest']}")
            else:
                session.repinned(r["retained_ref"], f"KEEP recheck {r['path']}", phase, disp)
                # ANY required KEEP drift (including X rows, which are KEEP rows
                # when present) fails: all rows rechecked above cover every KEEP.
        # Staged authoring/reader refs (exact, no semantic re-derivation).
        proposed = proposal.get("proposed") or {}
        for key in ("authoring_input_ref", "proposed_reader_ref"):
            ref = proposed.get(key) or {}
            session.repinned({"path": ref.get("path", ""), "sha256": ref.get("sha256", "")},
                             f"staged {key}", phase, disp)
        # capture_inputs: uniqueness/sorted + required bindings against
        # available bytes; historical extras are observations (not re-proven).
        cap = manifest.get("capture_inputs") or []
        if not isinstance(cap, list) or not cap:
            raise _fail("RETENTION_MISMATCH", phase, disp, "capture_inputs empty")
        seen: set[str] = set()
        for e in cap:
            if not isinstance(e, dict) or set(e) != {"path", "sha256"}:
                raise _fail("RETENTION_MISMATCH", phase, disp, "capture_inputs entry must be exact {path,sha256}")
            _check_lexical_path(e["path"], "capture input", phase, disp)
            if e["path"] in seen:
                raise _fail("RETENTION_MISMATCH", phase, disp, f"capture_inputs duplicate: {e['path']}")
            seen.add(e["path"])
        if [e["path"] for e in cap] != sorted(seen):
            raise _fail("RETENTION_ORDER_MISMATCH", phase, disp, "capture_inputs not sorted-unique by path")
        avail = dict(inv_files)
        # Add staged/proposal/manifest/KEEP-hashed entries for binding check.
        for rel in [prop_rel, man_rel] + [r["retained_ref"]["path"] for r in rows if r["policy"] == "KEEP_IMMUTABLE"] \
                + [(proposed.get("authoring_input_ref") or {}).get("path", ""),
                   (proposed.get("proposed_reader_ref") or {}).get("path", "")]:
            if rel and rel not in avail:
                _rel, data = session.safe_read(rel, "capture input binding", phase, disp)
                avail[rel] = core.sha256_bytes(data)
        cmap = {e["path"]: e["sha256"] for e in cap}
        for rel, sha in avail.items():
            if rel in cmap and cmap[rel] != sha:
                raise _fail("INVALID_RETENTION", phase, disp, f"capture input drift for available path: {rel}")
        # Required bindings: every row path + staged + proposal must be present in capture_inputs.
        required = {r["path"] for r in rows} | {prop_rel,
                                                (proposed.get("authoring_input_ref") or {}).get("path", ""),
                                                (proposed.get("proposed_reader_ref") or {}).get("path", "")}
        required.discard("")
        for rel in required:
            if rel not in cmap:
                raise _fail("RETENTION_MISMATCH", phase, disp, f"capture_inputs missing required path: {rel}")
        # Canonical bytes check (projector only for comparison).
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
