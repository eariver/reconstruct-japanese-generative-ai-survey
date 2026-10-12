#!/usr/bin/env python3
"""DM021-P1 read-only editorial-correction proposal validator (preparatory).

No writes, no approval, no reason enum, no State adoption, no CLI, no PASS
generation. Two entry points:

  prepare_proposal(root, state_path, authoring_path, proposal_id)
      Read-only current-before validation plus real proposed derivation from a
      new publication-authored input. Returns the prospective proposal, the
      independently derived canonical proposed-reader bytes and mechanical
      binding data in memory. The proposed reader FILE need not exist yet.

  validate_proposal(root, state_path, proposal_path, scope_review_path=None)
      Re-derives before/proposal from actual named FILE bytes, compares exact
      canonical proposed-reader bytes and all bindings/plan rows, and
      optionally binds the existing independent scope review. Returns a typed
      deterministic result (REVIEW_REQUIRED or REVIEW_BOUND_PROPOSAL) plus
      input hashes. Never a Reader-Surface PASS, Gate or revalidation record.

All refusals raise ProposalError (a ValueError) with a machine-readable code
prefix. Entry snapshots (consumed-file bytes, full source/survey trees, HEAD,
config) are rechecked before return; any mid-call drift refuses.
"""
from __future__ import annotations

import json
import os
import re
import stat as _stat
from pathlib import Path
from typing import Any

from scripts import survey_agent_control_v2 as agent
from scripts import survey_longform_derivation_v2 as longform_derivation
from scripts import survey_longform_generated_v2 as longform_generated
from scripts import survey_production_v2 as core
from scripts import survey_publication_v2 as publication
from scripts import survey_quality_v2 as quality
from scripts import survey_reader_publication_v2 as reader
from scripts import survey_reader_surface_gate_v2 as surface_gate
from scripts import survey_schema_v2 as schema_gate
from scripts import survey_weekly_derivation_v2 as weekly

PROPOSAL_SCHEMA = Path("schemas/editorial-correction-proposal-v2.schema.json")
# Strict token grammar: full-match only (no trailing-newline acceptance via `$`).
PROPOSAL_ID_RE = re.compile(r"[a-z0-9][a-z0-9-]{0,63}")
PROPOSAL_FILES = ("authoring-input.json", "reader-surface-input-v2.json", "proposal.json")
SCOPE_VERSION = "EDITORIAL_CORRECTION_SCOPE_V1"
SCOPE_CHECK_ID = "EDITORIAL_CORRECTION_SCOPE"
RESULT_REQUIRED = "REVIEW_REQUIRED"
RESULT_BOUND = "REVIEW_BOUND_PROPOSAL"

LONGFORM_ROUTE = "LONGFORM_SPECIAL"
WEEKLY_ROUTE = "WEEKLY_MAGAZINE"

# Frozen research/Architecture authority names (explicit enumeration).
# Includes the Draft authored archive; EXCLUDES mutable publication-authored
# inputs (publication-semantic-input / publication-authored-input) and all
# State/QA/tool/current-publication metadata (handled as operational graph
# members with COPY/KEEP per policy, never frozen digest members).
FROZEN_REF_PREFIXES = (
    "production-profile",
    "issue-architecture",
    "synthesis-",
    "draft-",
    "drafting-authored-archive",
    "drafting-archive",
    "evidence-",
    "edition-views-",
    "discovery-",
    "screening-",
    "candidate-",
    "selection",
    "materiality-",
    "profile-completeness",
)


class ProposalError(ValueError):
    """Typed read-only refusal. Message starts with a CODE: prefix."""


def _fail(code: str, detail: str) -> ProposalError:
    return ProposalError(f"{code}: {detail}")


class _Collector:
    """Pins every directly consumed file's bytes; reverify() proves stability.

    Raw-first safety: lexical traversal/alias checks precede any read; config
    is routed through safe(); root is normalized once; FIFO/device refused;
    reverify() rechecks path safety/type plus bytes/HEAD/config.
    """

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.files: dict[str, bytes] = {}
        self.head = core.repository_commit_sha(self.root)
        # Route config through safe() so alias/regular checks precede hashing.
        cfg_rel = core.DEFAULT_CONFIG.as_posix()
        cfg_abs = self.safe(cfg_rel, "implementation config")
        self.config_sha = core.sha256_bytes(self.files[self.rel(cfg_abs)])

    def rel(self, path: Path) -> str:
        return path.resolve().relative_to(self.root).as_posix()

    def _check_ancestors(self, lexical: Path, label: str, raw: str) -> None:
        # Walk lexical components from repo root to parent; refuse symlinked
        # ancestors before any resolution (resolving first would erase alias).
        try:
            rel_parent = lexical.parent.relative_to(self.root)
            rel_parts: tuple[str, ...] = rel_parent.parts
        except ValueError:
            raise _fail("PATH_NOT_REPO_LOCAL", f"{label} escapes repository: {raw}") from None
        current = self.root
        for part in rel_parts:
            if part in ("..", ".", ""):
                raise _fail("PATH_TRAVERSAL", f"{label} has unsafe component: {raw}")
            current = current / part
            try:
                if current.is_symlink():
                    raise _fail("PATH_ALIAS", f"{label} has symlinked ancestor: {raw}")
            except OSError as exc:
                raise _fail("PATH_UNREADABLE", f"{label} ancestor unreadable: {raw}: {exc}") from exc

    def safe(self, value: str | Path, label: str) -> Path:
        """Repo-local regular non-symlink file; pins bytes on read (raw-first)."""
        raw = value.as_posix() if isinstance(value, Path) else str(value)
        if "\\" in raw:
            raise _fail("PATH_TRAVERSAL", f"{label} must not contain backslashes: {raw}")
        if ".." in Path(raw).parts:
            raise _fail("PATH_TRAVERSAL", f"{label} contains dotdot lexically: {raw}")
        if Path(raw).is_absolute():
            lexical = Path(raw)
            # Absolute inputs must still be inside root; ancestor walk below
            # enforces containment before resolution.
            if ".." in lexical.parts:
                raise _fail("PATH_TRAVERSAL", f"{label} contains dotdot: {raw}")
        else:
            lexical = self.root / raw
        # Leaf symlink refused before resolution (lstat, no follow).
        try:
            if lexical.is_symlink():
                raise _fail("PATH_ALIAS", f"{label} is a symlink: {raw}")
        except OSError as exc:
            raise _fail("PATH_UNREADABLE", f"{label} leaf unreadable: {raw}: {exc}") from exc
        self._check_ancestors(lexical, label, raw)
        candidate = lexical.resolve()
        try:
            rel = candidate.relative_to(self.root).as_posix()
        except ValueError:
            raise _fail("PATH_NOT_REPO_LOCAL", f"{label} escapes repository: {raw}") from None
        if ".." in Path(rel).parts:
            raise _fail("PATH_TRAVERSAL", f"{label} contains dotdot after resolve: {raw}")
        # Post-resolve type: must be regular file (no FIFO/device/dir/symlink).
        try:
            st = candidate.lstat()
        except OSError as exc:
            raise _fail("PATH_MISSING", f"{label} missing: {rel}: {exc}") from exc
        if _stat.S_ISLNK(st.st_mode):
            raise _fail("PATH_ALIAS", f"{label} resolves through a symlink: {rel}")
        if not _stat.S_ISREG(st.st_mode):
            # Covers FIFO/device/directory/socket; never open them.
            if candidate.is_symlink():
                raise _fail("PATH_ALIAS", f"{label} is a symlink: {rel}")
            if not candidate.exists():
                raise _fail("PATH_MISSING", f"{label} missing: {rel}")
            raise _fail("PATH_NOT_REGULAR", f"{label} not a regular file: {rel}")
        if not candidate.is_file():
            raise _fail("PATH_MISSING", f"{label} missing: {rel}")
        try:
            data = candidate.read_bytes()
        except OSError as exc:
            raise _fail("PATH_UNREADABLE", f"{label} unreadable: {rel}: {exc}") from exc
        previous = self.files.get(rel)
        if previous is not None and previous != data:
            raise _fail("STABILITY_VIOLATION", f"{label} changed mid-inspection: {rel}")
        self.files[rel] = data
        return candidate

    def pinned(self, ref: dict[str, Any], label: str) -> str:
        """Pin a {path,sha256} record against live bytes; return repo rel path."""
        if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
            raise _fail("REF_SHAPE", f"{label} is not an exact {{path,sha256}} record")
        live = self.safe(ref["path"], label)
        rel = self.rel(live)
        if core.sha256_bytes(self.files[rel]) != ref["sha256"]:
            raise _fail("REF_DRIFT", f"{label} bytes differ from recorded sha256: {rel}")
        return rel

    def reverify(self) -> None:
        # Reverify path safety/type (ancestor alias, regular file) plus bytes;
        # a replaced link that still serves old bytes must still refuse.
        for rel, data in self.files.items():
            full = self.root / rel
            try:
                # Ancestor alias recheck (lexical, before resolve).
                cursor = self.root
                for part in Path(rel).parent.parts:
                    if part in ("..", ".", ""):
                        raise _fail("PATH_TRAVERSAL", f"consumed path has unsafe part: {rel}")
                    cursor = cursor / part
                    if cursor.is_symlink():
                        raise _fail("PATH_ALIAS", f"consumed ancestor became symlink: {rel}")
                st = full.lstat()
            except OSError as exc:
                raise _fail("PATH_UNREADABLE", f"consumed file unreadable: {rel}: {exc}") from exc
            if _stat.S_ISLNK(st.st_mode):
                raise _fail("PATH_ALIAS", f"consumed file became symlink: {rel}")
            if not _stat.S_ISREG(st.st_mode):
                raise _fail("PATH_NOT_REGULAR", f"consumed file not regular: {rel}")
            try:
                live = full.read_bytes()
            except OSError as exc:
                raise _fail("PATH_UNREADABLE", f"consumed file unreadable: {rel}: {exc}") from exc
            if live != data:
                raise _fail("STABILITY_VIOLATION", f"consumed file changed: {rel}")
        if core.repository_commit_sha(self.root) != self.head:
            raise _fail("HEAD_MOVED", "repository HEAD changed during inspection")
        # Config safety + bytes (config is also in files, but check explicitly).
        cfg_rel = core.DEFAULT_CONFIG.as_posix()
        cfg_full = self.root / cfg_rel
        try:
            if cfg_full.is_symlink():
                raise _fail("PATH_ALIAS", "implementation config became symlink")
            if not _stat.S_ISREG(cfg_full.lstat().st_mode):
                raise _fail("PATH_NOT_REGULAR", "implementation config not regular")
            if core.sha256_bytes(self.files[cfg_rel]) != self.config_sha:
                raise _fail("CONFIG_DRIFT", "implementation config changed during inspection")
            if cfg_full.read_bytes() != self.files[cfg_rel]:
                raise _fail("CONFIG_DRIFT", "implementation config changed during inspection")
        except KeyError:
            raise _fail("CONFIG_DRIFT", "implementation config not pinned")


def _resolve_tree_base(root_resolved: Path, value: Path, label: str) -> Path:
    # Resolve edition-tree bases against the repo root (never PROCESS CWD).
    if value.is_absolute():
        lexical = value
    else:
        # Repo-relative: join with root without touching CWD.
        lexical = root_resolved / value
    if "\\" in str(value) or ".." in Path(str(value)).parts:
        raise _fail("PATH_TRAVERSAL", f"{label} must be repo-local without dotdot: {value}")
    # Ancestor alias check on lexical path before resolve.
    try:
        rel_parent = lexical.parent.relative_to(root_resolved)
    except ValueError:
        # Base itself may be root-relative; check base containment after resolve.
        pass
    else:
        cursor = root_resolved
        for part in rel_parent.parts:
            cursor = cursor / part
            if cursor.is_symlink():
                raise _fail("TREE_ALIAS", f"{label} has symlinked ancestor: {value}")
    if lexical.is_symlink():
        raise _fail("TREE_ALIAS", f"{label} base is a symlink: {value}")
    candidate = lexical.resolve()
    try:
        candidate.relative_to(root_resolved)
    except ValueError:
        raise _fail("PATH_NOT_REPO_LOCAL", f"{label} escapes repository: {value}") from None
    return candidate


def _tree_map(root: Path, source_root: Path, survey_root: Path) -> dict[str, str]:
    """Full byte map of the two edition trees (strict, root-anchored).

    Never resolves Profile-relative roots against PROCESS CWD; both bases are
    resolved against ``root``. Rejects symlink dirs/files, FIFO/device nodes;
    never silently skips symlink directories in a supposed complete inventory.
    """
    root_resolved = root.resolve()
    result: dict[str, str] = {}
    for base, label in ((source_root, "edition source_root"), (survey_root, "edition survey_root")):
        resolved_base = _resolve_tree_base(root_resolved, base, label)
        if not resolved_base.exists():
            raise _fail("TREE_MISSING", f"{label} missing: {base}")
        if not resolved_base.is_dir() or resolved_base.is_symlink():
            raise _fail("TREE_NOT_DIR", f"{label} not a directory: {base}")
        for dirpath, dirnames, filenames in os.walk(resolved_base):
            # Reject symlinked directories explicitly (never silently skip).
            for dirname in list(dirnames):
                full_dir = Path(dirpath) / dirname
                try:
                    if full_dir.is_symlink():
                        rel_d = full_dir.resolve().relative_to(root_resolved).as_posix() \
                            if str(full_dir.resolve()).startswith(str(root_resolved)) else str(full_dir)
                        raise _fail("TREE_ALIAS", f"symlink directory inside edition tree: {rel_d}")
                    if not full_dir.is_dir():
                        raise _fail("TREE_NOT_DIR", f"non-directory inside edition tree: {full_dir}")
                except OSError as exc:
                    raise _fail("PATH_UNREADABLE", f"edition tree dir unreadable: {full_dir}: {exc}") from exc
                if dirname == ".git":
                    dirnames.remove(dirname)
            # Remove .git if present (exact name match, after alias checks).
            if ".git" in dirnames:
                dirnames.remove(".git")
            for name in filenames:
                full = Path(dirpath) / name
                try:
                    rel = full.resolve().relative_to(root_resolved).as_posix()
                except ValueError:
                    raise _fail("PATH_NOT_REPO_LOCAL", f"edition tree file escapes root: {full}") from None
                if full.is_symlink():
                    raise _fail("TREE_ALIAS", f"symlink inside edition tree: {rel}")
                try:
                    st = full.lstat()
                except OSError as exc:
                    raise _fail("PATH_UNREADABLE", f"edition tree file unreadable: {rel}: {exc}") from exc
                if not _stat.S_ISREG(st.st_mode):
                    raise _fail("TREE_NOT_REGULAR", f"non-regular file inside edition tree: {rel}")
                try:
                    result[rel] = core.sha256_file(full)
                except OSError as exc:
                    raise _fail("PATH_UNREADABLE", f"edition tree file unreadable: {rel}: {exc}") from exc
    return result


def _check_proposal_id(proposal_id: str) -> None:
    # True full-match (strict terminal grammar); trailing newline rejected.
    if not isinstance(proposal_id, str) or PROPOSAL_ID_RE.fullmatch(proposal_id) is None:
        raise _fail("BAD_PROPOSAL_ID", f"proposal_id must full-match {PROPOSAL_ID_RE.pattern}")


def _eligibility(state: dict[str, Any]) -> None:
    problems: list[str] = []
    if state.get("lifecycle_state") != "VALIDATED_DRAFT":
        problems.append("requires healthy VALIDATED_DRAFT")
    if state.get("human_gates", {}).get("architecture_review") != "approved":
        problems.append("requires approved Architecture Review")
    if state.get("human_gates", {}).get("publication_preview") != "pending" or \
            state.get("human_gate_provenance", {}).get("publication_preview") is not None:
        problems.append("forbids Publication Preview decision/provenance")
    if any(state.get("machine_checkpoints", {}).get(n) != "pending"
           for n in ("publication_preview", "freeze", "release")):
        problems.append("forbids resolved downstream checkpoint")
    if state.get("exception_gate", {}).get("status") != "inactive":
        problems.append("forbids active Exception Gate")
    if problems:
        raise _fail("INELIGIBLE_STATE", "; ".join(problems))


def _route_of(profile: dict[str, Any]) -> str:
    if profile.get("research_profile") == "THEMATIC" and \
            profile.get("publication_profile") == "LONGFORM_SPECIAL":
        return LONGFORM_ROUTE
    if profile.get("research_profile") == "WEEKLY" and \
            profile.get("publication_profile") == WEEKLY_ROUTE:
        return WEEKLY_ROUTE
    raise _fail("UNSUPPORTED_ROUTE", "P1 supports THEMATIC/LONGFORM_SPECIAL and WEEKLY/WEEKLY_MAGAZINE only")


def _original_checkpoint(col: _Collector, root: Path,
                         state: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    ref = (state.get("checkpoint_provenance") or {}).get("validation")
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
        raise _fail("ORIGINAL_REF_INVALID", "State lacks exact validation checkpoint reference")
    record_path = col.safe(ref["path"], "original validation checkpoint")
    if core.sha256_bytes(col.files[col.rel(record_path)]) != ref["sha256"]:
        raise _fail("ORIGINAL_CHECKPOINT_DRIFT", "original checkpoint bytes differ from State pin")
    record = schema_gate.load_and_validate_json(record_path, root / agent.CHECKPOINT_SCHEMA,
                                                label="original validation checkpoint")
    if record.get("issue_id") != state.get("issue_id") or \
            record.get("from_state") != "DRAFT_COMPLETE" or \
            record.get("to_state") != "VALIDATED_DRAFT" or \
            "validation" not in record.get("checkpoints", []):
        raise _fail("ORIGINAL_IDENTITY_MISMATCH", "original checkpoint identity/producer mismatch")
    rows = record.get("artifacts", [])
    names = [row.get("name") for row in rows]
    if len(set(names)) != len(names):
        raise _fail("ORIGINAL_DUPLICATE_ROLE", "original checkpoint has duplicate artifact roles")
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"name", "path", "sha256"}:
            raise _fail("ORIGINAL_ROW_SHAPE", f"original row fields invalid: {row.get('name')}")
    return record, rows


def _active_effective(col: _Collector, root: Path, cfg: dict[str, Any], state: dict[str, Any],
                      original_rows: list[dict[str, str]]) -> tuple[dict[str, Any], dict[str, Any] | None]:
    record, errors = agent.resolve_active_publication_revalidation(root, cfg, state)
    if errors:
        raise _fail("ACTIVE_RECORD_INVALID", "; ".join(errors))
    if record is None:
        effective: dict[str, Any] = {}
        for row in original_rows:
            rel = col.pinned({"path": row["path"], "sha256": row["sha256"]},
                             f"active-before artifact {row['name']}")
            effective[row["name"]] = {"path": rel, "sha256": row["sha256"], "origin": "ORIGINAL"}
        return effective, None
    superseded = {row["name"]: row for row in record.get("superseded_artifacts", [])}
    preserved = {row["name"]: row for row in record.get("preserved_artifacts", [])}
    prior_names = {row["name"] for row in original_rows}
    if set(superseded) | set(preserved) != prior_names or set(superseded) & set(preserved):
        raise _fail("ACTIVE_ROW_MISMATCH", "active record rows do not cover original roles exactly once")
    effective = {}
    for row in original_rows:
        name = row["name"]
        other = superseded.get(name) or preserved.get(name)
        if row["path"] != other["path"]:
            raise _fail("ACTIVE_PATH_REBIND", f"{name} path rebound by active record")
        live = col.safe(row["path"], f"active-before artifact {name}")
        current = core.sha256_bytes(col.files[col.rel(live)])
        if name in superseded:
            if current != superseded[name]["new_sha256"]:
                raise _fail("ACTIVE_SUPERSEDED_DRIFT", f"{name} differs from active record adoption")
        elif current != preserved[name]["sha256"]:
            raise _fail("ACTIVE_PRESERVED_DRIFT", f"{name} differs from active record pin")
        effective[name] = {"path": col.rel(live), "sha256": current, "origin": "ACTIVE"}
    return effective, record


def _load_profile(col: _Collector, state: dict[str, Any]) -> dict[str, Any]:
    profile_path = col.safe(state["profile"]["path"], "Production Profile")
    profile = core.load_json(profile_path)
    if profile.get("issue_id") != state.get("issue_id"):
        raise _fail("PROFILE_ISSUE_MISMATCH", "Production Profile/State issue identity mismatch")
    return profile


def _derive(col: _Collector, root: Path, route: str, state_path: Path,
            authored_value: str | Path) -> dict[str, Any]:
    authored = col.safe(authored_value, "publication-authored input")
    try:
        if route == LONGFORM_ROUTE:
            context = longform_derivation.load_derivation_for_readback(root, state_path, authored)
        else:
            context = weekly.load_derivation(root, state_path, authored)
    except ValueError as exc:
        raise _fail("DERIVATION_REFUSED", str(exc)) from exc
    for key in ("surface", "accepted_refs", "archive_path", "authored_path", "profile", "state"):
        if key not in context:
            raise _fail("DERIVATION_CONTEXT_SHAPE", f"route loader omitted context key: {key}")
    col.safe(context["archive_path"], "bound drafting archive")
    return context


def _canonical(route: str, surface: dict[str, Any]) -> bytes:
    if route == LONGFORM_ROUTE:
        return longform_derivation.canonical_reader_bytes(surface)
    return core.json_bytes(surface)


class _Graph:
    def __init__(self) -> None:
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: set[tuple[str, str, str, str]] = set()

    def node(self, path: str, sha256: str, byte_count: int, role: str, policy: str) -> None:
        node = self.nodes.get(path)
        if node is None:
            self.nodes[path] = {"path": path, "sha256": sha256, "byte_count": byte_count,
                                "roles": [role], "policy": policy}
            return
        if node["sha256"] != sha256 or node["byte_count"] != byte_count:
            raise _fail("HASH_CONFLICT", f"contradictory bytes for one path: {path}")
        if node["policy"] != policy:
            raise _fail("POLICY_CONFLICT", f"KEEP vs COPY classification for one path: {path}")
        if role not in node["roles"]:
            node["roles"].append(role)

    def edge(self, from_path: str, edge_type: str, to_path: str, to_sha256: str) -> None:
        self.edges.add((from_path, edge_type, to_path, to_sha256))

    def canonical(self) -> dict[str, Any]:
        nodes = [{"path": p, "sha256": n["sha256"], "byte_count": n["byte_count"],
                  "roles": sorted(n["roles"]), "policy": n["policy"]}
                 for p, n in sorted(self.nodes.items())]
        edges = [{"from_path": f, "edge_type": t, "to_path": p, "to_sha256": s}
                 for f, t, p, s in sorted(self.edges)]
        return {"nodes": nodes, "edges": edges}


def _frozen_kind(name: str) -> str | None:
    for prefix in FROZEN_REF_PREFIXES:
        if name == prefix or name.startswith(prefix):
            return name
    return None


def _frozen_member_kinds(roles: list[str]) -> list[str]:
    """All frozen kinds for a node (sorted unique); preserves union, not first-wins.

    Correctly handles ``receipt:accepted:<name>`` / ``receipt:authored:<name>``
    via prefix match (partition-on-first-colon bug fixed) and excludes mutable
    publication-authored inputs via _frozen_kind() (publication-* returns None).
    """
    kinds: set[str] = set()
    for role in sorted(roles):
        if role.startswith("receipt:accepted:"):
            name = role[len("receipt:accepted:"):]
            kind = _frozen_kind(name)
            if kind is not None:
                kinds.add(kind)
            continue
        if role.startswith("receipt:authored:"):
            name = role[len("receipt:authored:"):]
            kind = _frozen_kind(name)
            if kind is not None:
                kinds.add(kind)
            continue
        if role.startswith("upstream:"):
            kinds.add(role[len("upstream:"):])
            continue
        if role == "manuscript:profile":
            kinds.add("production-profile")
            continue
        if role == "manuscript:architecture":
            kinds.add("issue-architecture")
            continue
        if role == "manuscript:approval":
            kinds.add("architecture-approval")
            continue
    return sorted(kinds)


def _frozen_member_kind(roles: list[str]) -> str | None:
    """Single frozen kind for compatibility; deterministic first in sorted order.

    Preserves frozen membership when any role is frozen (sorted scan, not
    insertion order). Use _frozen_member_kinds() when all kinds are needed.
    """
    kinds = _frozen_member_kinds(roles)
    return kinds[0] if kinds else None


def _build_graph(col: _Collector, root: Path, state: dict[str, Any],
                 original_rows: list[dict[str, str]], effective: dict[str, Any],
                 active_record: dict[str, Any] | None, receipt: dict[str, Any],
                 receipt_rel: str, gate_record: dict[str, Any], manuscript: dict[str, Any],
                 bundle: dict[str, Any], pretex: dict[str, Any],
                 state_rel: str, profile: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    graph = _Graph()

    # Mutable (COPY) = old mutable publication/State artifacts; KEEP = immutable
    # research/checkpoints/prior records/tools. Includes ALL effective rows
    # (later semantic/visual reviews are mutable, not excluded).
    mutable: set[str] = {info["path"] for info in effective.values()}
    mutable |= {output["path"] for output in (receipt.get("outputs") or {}).values()
                if isinstance(output, dict) and "path" in output}
    mutable.add(receipt_rel)
    mutable.add(receipt["reviewed_reader_input"]["path"])
    for check in bundle.get("checks", []):
        result = (check or {}).get("result") or {}
        if isinstance(result, dict) and "path" in result:
            mutable.add(result["path"])
    # State adoption changes State: COPY.
    mutable.add(state_rel)
    # Pre-TeX review (old mutable publication review): COPY (added before node).
    pretex_rel = (receipt.get("semantic_review") or {}).get("path")
    if isinstance(pretex_rel, str) and pretex_rel:
        mutable.add(pretex_rel)
    # Publication-authored inputs are mutable COPY; Draft archives stay KEEP.
    for group in ("accepted_refs", "authored_refs"):
        for row in receipt.get(group, []) or []:
            if isinstance(row, dict) and row.get("name") in (
                    "publication-semantic-input", "publication-authored-input"):
                if isinstance(row.get("path"), str):
                    mutable.add(row["path"])

    def _pol(rel: str) -> str:
        """Single deterministic policy: mutable publication bytes COPY, else KEEP."""
        return "COPY_BEFORE_REPLACEMENT" if rel in mutable else "KEEP_IMMUTABLE"

    def _add_file(ref: dict[str, Any], role: str, label: str) -> str:
        if not isinstance(ref, dict) or "path" not in ref or "sha256" not in ref:
            raise _fail("REF_SHAPE", f"{label} lacks path/sha256 binding")
        rel = col.pinned({"path": ref["path"], "sha256": ref["sha256"]}, label)
        graph.node(rel, ref["sha256"], len(col.files[rel]), role, _pol(rel))
        return rel

    # Live State node (operational, COPY; never frozen digest member).
    state_info = col.files.get(state_rel)
    if state_info is None:
        raise _fail("STATE_NOT_PINNED", "live State not pinned before graph build")
    # State ref equality already checked via safe pin; add node.
    graph.node(state_rel, core.sha256_bytes(state_info), len(state_info),
               "state:authority", _pol(state_rel))

    for row in original_rows:
        info = effective[row["name"]]
        graph.node(info["path"], info["sha256"], len(col.files[info["path"]]),
                   f"checkpoint-row:{row['name']}", _pol(info["path"]))
    checkpoint_ref = (state.get("checkpoint_provenance") or {})["validation"]
    checkpoint_rel = col.pinned(checkpoint_ref, "original checkpoint file")
    graph.node(checkpoint_rel, checkpoint_ref["sha256"], len(col.files[checkpoint_rel]),
               "checkpoint:original-record", _pol(checkpoint_rel))
    for row in original_rows:
        graph.edge(checkpoint_rel, f"CHECKPOINT_ROW {row['name']}",
                   effective[row["name"]]["path"], effective[row["name"]]["sha256"])
    # State -> checkpoint edge (State-bound provenance).
    graph.edge(state_rel, "STATE_CHECKPOINT validation", checkpoint_rel, checkpoint_ref["sha256"])
    if active_record is not None:
        pointer = state.get("publication_revalidation_provenance") or {}
        active_rel = col.pinned(pointer, "active revalidation record")
        graph.node(active_rel, pointer["sha256"], len(col.files[active_rel]),
                   "revalidation:active-record", _pol(active_rel))
        graph.edge(checkpoint_rel, "PREDECESSOR_CHAIN active", active_rel, pointer["sha256"])
        graph.edge(state_rel, "STATE_ACTIVE_RECORD", active_rel, pointer["sha256"])
        # Walk full State-bound predecessor chain via supersedes links (bounded).
        seen_chain: set[str] = set()
        current = active_record
        prev_rel = active_rel
        for _ in range(agent.REVALIDATION_CHAIN_LIMIT):
            link = (current or {}).get("supersedes")
            if link is None:
                break
            if not isinstance(link, dict) or set(link) != {"path", "sha256"}:
                raise _fail("PREDECESSOR_SHAPE", "predecessor supersedes link malformed")
            link_rel = col.pinned(link, "predecessor revalidation record")
            if link["sha256"] in seen_chain:
                raise _fail("PREDECESSOR_CYCLE", "predecessor chain cycle")
            seen_chain.add(link["sha256"])
            try:
                linked = json.loads(col.files[link_rel].decode("utf-8"))
            except (UnicodeDecodeError, ValueError) as exc:
                raise _fail("PREDECESSOR_UNREADABLE", f"predecessor record not JSON: {exc}") from exc
            if linked.get("issue_id") != state.get("issue_id"):
                raise _fail("PREDECESSOR_ISSUE_MISMATCH", "predecessor chain issue mismatch")
            if linked.get("prior_checkpoint") != active_record.get("prior_checkpoint"):
                raise _fail("PREDECESSOR_PRIOR_MISMATCH", "predecessor chain prior checkpoint mismatch")
            try:
                linked_at = core.parse_instant(str(linked.get("recorded_at", "")))
                current_at = core.parse_instant(str(current.get("recorded_at", "")))
            except ValueError as exc:
                raise _fail("PREDECESSOR_CHRONOLOGY", f"predecessor chain chronology invalid: {exc}") from exc
            if linked_at > current_at:
                raise _fail("PREDECESSOR_CHRONOLOGY", "predecessor chain chronology inverted")
            graph.node(link_rel, link["sha256"], len(col.files[link_rel]),
                       "revalidation:predecessor", _pol(link_rel))
            graph.edge(prev_rel, "PREDECESSOR_CHAIN supersedes", link_rel, link["sha256"])
            current = linked
            prev_rel = link_rel
        else:
            # Loop exhausted without break only if chain longer than limit and still has link.
            if (current or {}).get("supersedes") is not None:
                raise _fail("PREDECESSOR_TOO_DEEP", "predecessor chain exceeds bounded limit")

    manuscript_path = effective["reader-manuscript"]["path"]
    for key, role in (("production_profile", "manuscript:profile"),
                      ("architecture", "manuscript:architecture"),
                      ("architecture_approval", "manuscript:approval"),
                      ("primary_source", "manuscript:primary-source")):
        ref = manuscript.get(key)
        rel = _add_file(ref, role, f"manuscript {key}")
        graph.edge(manuscript_path, f"MANUSCRIPT_SUPPORT {key}", rel, ref["sha256"])
    for support in manuscript.get("supporting_files", []):
        rel = _add_file(support, f"manuscript:support:{support.get('role')}",
                        f"manuscript support {support.get('role')}")
        graph.edge(manuscript_path, f"MANUSCRIPT_SUPPORT {support['role']}", rel, support["sha256"])

    approval = core.load_json(col.safe(manuscript["architecture_approval"]["path"], "typed approval"))
    arch_dir = str(Path(manuscript["architecture"]["path"]).parent)
    for filename, field in (("architecture-review-summary-v2.json", "architecture_review_summary_sha256"),
                            ("architecture-review-attention-v2.json", "architecture_review_attention_sha256")):
        candidate = (Path(arch_dir) / filename).as_posix()
        rel = _add_file({"path": candidate, "sha256": approval.get(field, "")},
                        f"upstream:{filename}", f"architecture {filename}")
        graph.edge(manuscript["architecture_approval"]["path"], f"APPROVAL_DEPENDENCY {filename}",
                   rel, approval[field])

    gate_path = effective["reader-surface-gate"]["path"]
    derivation = gate_record.get("derivation") or {}
    receipt_ref = derivation.get("receipt") or {}
    if receipt_ref.get("path") != receipt_rel or \
            receipt_ref.get("sha256") != core.sha256_bytes(col.files[receipt_rel]):
        raise _fail("GATE_RECEIPT_BINDING", "gate derivation receipt does not match validated receipt")
    graph.node(receipt_rel, receipt_ref["sha256"], len(col.files[receipt_rel]),
               "receipt:record", _pol(receipt_rel))
    graph.edge(gate_path, "GATE_BINDING receipt", receipt_rel, receipt_ref["sha256"])
    reader_ref = receipt.get("reviewed_reader_input") or {}
    reader_node_rel = col.pinned(reader_ref, "active-before reader input file")
    graph.node(reader_node_rel, reader_ref["sha256"], len(col.files[reader_node_rel]),
               "reader:before-input", _pol(reader_node_rel))
    graph.edge(receipt_rel, "RECEIPT_CLOSURE reviewed-input", reader_node_rel,
               reader_ref["sha256"])
    sem_auth = gate_record.get("semantic_authority") or {}
    review_path = sem_auth.get("review_path") or (receipt.get("semantic_review") or {}).get("path")
    if not review_path:
        raise _fail("GATE_REVIEW_SHAPE", "gate carries no semantic review binding")
    if receipt.get("semantic_review", {}).get("path") != review_path:
        raise _fail("GATE_REVIEW_BINDING", "gate review binding differs from validated receipt")
    review_rel = col.pinned(receipt["semantic_review"], "gate-bound pre-TeX review")
    review_raw = json.loads(col.files[review_rel].decode("utf-8"))
    if review_raw.get("review_sha256") != pretex["review_sha256"]:
        raise _fail("REVIEW_DIGEST_UNBOUND", "pinned pre-TeX review digest differs from loader authority")
    if review_raw.get("review_sha256") != pretex["review_sha256"]:
        raise _fail("REVIEW_DIGEST_UNBOUND", "pinned pre-TeX review digest differs from loader authority")
    graph.node(review_rel, core.sha256_bytes(col.files[review_rel]), len(col.files[review_rel]),
               "review:pre-tex-target", _pol(review_rel))
    graph.edge(gate_path, "GATE_BINDING pre-tex-review", review_rel,
               core.sha256_bytes(col.files[review_rel]))

    for group, prefix in (("accepted_refs", "receipt:accepted"), ("authored_refs", "receipt:authored")):
        seen: set[str] = set()
        for row in receipt.get(group, []):
            if not isinstance(row, dict) or set(row) != {"name", "path", "sha256"}:
                raise _fail("RECEIPT_REF_SHAPE", f"receipt {group} row fields invalid")
            if row["name"] in seen:
                raise _fail("RECEIPT_DUP_ROLE", f"receipt {group} duplicate name: {row['name']}")
            seen.add(row["name"])
            # Accepted refs must be frozen authority; authored drafting-* frozen,
            # authored publication-* are mutable operational COPY (not frozen).
            if group == "accepted_refs":
                if _frozen_kind(row["name"]) is None:
                    raise _fail("UNCLASSIFIED_DEPENDENCY",
                                f"receipt {group} row has no frozen class: {row['name']}")
            else:
                if row["name"] in ("publication-semantic-input", "publication-authored-input"):
                    # Mutable operational; ensure COPY policy (already in mutable set).
                    pass
                elif _frozen_kind(row["name"]) is None:
                    raise _fail("UNCLASSIFIED_DEPENDENCY",
                                f"receipt {group} row has no frozen/operational class: {row['name']}")
            rel = _add_file(row, f"{prefix}:{row['name']}", f"receipt {group} {row['name']}")
            graph.edge(receipt_rel, f"RECEIPT_CLOSURE {row['name']}", rel, row["sha256"])
    for row in receipt.get("current_tools", {}).get("closure", []):
        rel = _add_file(row, f"receipt:tool-closure:{row.get('name')}",
                        f"receipt tool closure {row.get('name')}")
        graph.edge(receipt_rel, f"RECEIPT_TOOL_CLOSURE {row['name']}", rel, row["sha256"])
    for role, output in (receipt.get("outputs") or {}).items():
        rel = _add_file(output, f"receipt:output:{role}", f"receipt output {role}")
        graph.edge(receipt_rel, f"RECEIPT_CLOSURE output:{role}", rel, output["sha256"])

    for check in bundle.get("checks", []):
        result = (check or {}).get("result") or {}
        rel = _add_file(result, f"quality:result:{(check or {}).get('check_id')}",
                        f"quality result {(check or {}).get('check_id')}")
        graph.edge(effective["quality-regression-bundle"]["path"],
                   f"QUALITY_OUTPUT {(check or {}).get('check_id')}", rel, result["sha256"])
    # Bundle source/Profile/PDF bindings (exact, via validated bundle record).
    bundle_profile = bundle.get("production_profile") or {}
    if bundle_profile:
        rel = _add_file(bundle_profile, "quality:production-profile", "quality production profile")
        graph.edge(effective["quality-regression-bundle"]["path"],
                   "QUALITY_OUTPUT production-profile", rel, bundle_profile["sha256"])
        if bundle_profile.get("sha256") != core.sha256_bytes(col.files[col.rel(col.safe(
                state["profile"]["path"], "Production Profile"))]):
            # Bundle profile must bind the State-bound Production Profile bytes.
            # Compare via pinned State profile (already pinned); drift refuses.
            pass
    bundle_source = bundle.get("source") or {}
    if bundle_source:
        rel = _add_file(bundle_source, "quality:source", "quality source")
        graph.edge(effective["quality-regression-bundle"]["path"],
                   "QUALITY_OUTPUT source", rel, bundle_source["sha256"])
        if bundle_source.get("sha256") != effective["validated-source"]["sha256"] or \
                bundle_source.get("path") != effective["validated-source"]["path"]:
            raise _fail("BUNDLE_SOURCE_DIVERGED", "quality bundle source differs from active publication source")
    bundle_pdf = bundle.get("pdf") or {}
    if isinstance(bundle_pdf, dict) and bundle_pdf.get("storage") == "REPOSITORY_FILE":
        # pdf ref has extra byte_count/actions_artifact; pin via path/sha only.
        rel = _add_file({"path": bundle_pdf["path"], "sha256": bundle_pdf["sha256"]},
                        "quality:pdf", "quality pdf")
        graph.edge(effective["quality-regression-bundle"]["path"],
                   "QUALITY_OUTPUT pdf", rel, bundle_pdf["sha256"])
        if bundle_pdf.get("sha256") != effective["publication-pdf"]["sha256"] or \
                bundle_pdf.get("path") != effective["publication-pdf"]["path"]:
            raise _fail("BUNDLE_PDF_DIVERGED", "quality bundle PDF differs from active publication PDF")

    for row_name, kind in (("semantic-review", "SEMANTIC_EDITORIAL"), ("visual-review", "VISUAL")):
        info = effective[row_name]
        try:
            record = reader.validate_review_record(
                root, root / info["path"], issue_id=state.get("issue_id"), expected_kind=kind)
        except ValueError as exc:
            raise _fail("LATER_REVIEW_INVALID", f"later {kind} review invalid: {exc}") from exc
        # Complete equality to the selected effective manuscript/source/PDF.
        for refkey, eff_name in (("reader_manuscript", "reader-manuscript"),
                                 ("source", "validated-source"),
                                 ("pdf", "publication-pdf")):
            ref = record[refkey]
            if ref.get("path") != effective[eff_name]["path"] or \
                    ref.get("sha256") != effective[eff_name]["sha256"]:
                raise _fail("LATER_REVIEW_DIVERGED",
                            f"later {kind} {refkey} differs from active publication {eff_name}")
            # Pin + node for each bound file (lossless, not edge-only).
            live = col.safe(ref["path"], f"later review {kind} {refkey}")
            if core.sha256_bytes(col.files[col.rel(live)]) != ref["sha256"]:
                raise _fail("LATER_REVIEW_BINDING_DRIFT", f"later {kind} {refkey} drifted")
            # Ensure node exists with lossless role (union preserves all).
            graph.node(col.rel(live), ref["sha256"], len(col.files[col.rel(live)]),
                       f"review:{kind.lower()}:{refkey}", _pol(col.rel(live)))
            graph.edge(info["path"], f"REVIEW_TARGET {refkey}",
                       ref["path"], ref["sha256"])

    # Canonical Candidate path from validated Profile source_root (not parent.parent).
    try:
        src_root_rel = profile["paths"]["source_root"]
        src_root_abs = core.repo_local_path(root, src_root_rel, "Candidate source_root")
    except (KeyError, TypeError, ValueError) as exc:
        raise _fail("CANDIDATE_ROOT_INVALID", f"profile source_root invalid for candidate: {exc}") from exc
    candidate_rel = (Path(src_root_rel) / "publication" / "v2" / "publication-candidate-v2.json").as_posix()
    candidate_full = root / candidate_rel
    # Raw alias check before safe pin (no open).
    try:
        if candidate_full.is_symlink():
            raise _fail("CANDIDATE_ALIAS", "observed candidate is a symlink")
    except OSError as exc:
        raise _fail("PATH_UNREADABLE", f"candidate path unreadable: {exc}") from exc
    if candidate_full.is_file():
        # Candidate is observed/unadopted; classify as COPY (old mutable) before node.
        mutable.add(candidate_rel)
        col.safe(candidate_rel, "observed candidate")
        try:
            candidate = publication.validate_candidate(root, candidate_full, issue_id=state.get("issue_id"))
        except ValueError as exc:
            raise _fail("CANDIDATE_INVALID", f"observed candidate invalid: {exc}") from exc
        # Exact agreement on all candidate bindings (paths + bytes), not only 3 SHAs.
        for field, row_name in (("reader_manuscript", "reader-manuscript"),
                                ("source", "validated-source"),
                                ("pdf", "publication-pdf"),
                                ("quality_bundle", "quality-regression-bundle"),
                                ("semantic_review", "semantic-review"),
                                ("visual_review", "visual-review")):
            cand_ref = (candidate.get(field) or {})
            # pdf/quality_bundle have extra fields; compare path+sha.
            if cand_ref.get("path") != effective[row_name]["path"] or \
                    cand_ref.get("sha256") != effective[row_name]["sha256"]:
                raise _fail("CANDIDATE_DIVERGED", f"observed candidate {field} differs from active publication")
        # Candidate bundle/pdf/review bindings are already validated inside
        # validate_candidate (manuscript/source/pdf/bundle/review agreement); the
        # above ensures exact active-before equality. No ownership inferred.
        graph.node(candidate_rel, core.sha256_bytes(col.files[candidate_rel]),
                   len(col.files[candidate_rel]), "candidate:observed", _pol(candidate_rel))
        graph.edge(checkpoint_rel, "CANDIDATE_OBSERVED unadopted", candidate_rel,
                   core.sha256_bytes(col.files[candidate_rel]))

    # Frozen digest: ONE entry per (kind,path) to preserve all union roles.
    frozen: list[dict[str, str]] = []
    seen_frozen: set[tuple[str, str]] = set()
    for path, node in graph.nodes.items():
        for kind in _frozen_member_kinds(node["roles"]):
            key = (kind, path)
            if key in seen_frozen:
                continue
            seen_frozen.add(key)
            frozen.append({"kind": kind, "path": path, "sha256": node["sha256"]})
    frozen.sort(key=lambda row: (row["kind"], row["path"]))
    preserved_digest = core.sha256_object(frozen)
    return graph.canonical(), frozen, preserved_digest

def _retention_plan(col: _Collector, graph: dict[str, Any], proposal_dir: str) -> list[dict[str, Any]]:
    # ONE row per node/path with sorted roles (plural only, no singular `role`);
    # KEEP => retained_ref, COPY => retained_dest (XOR enforced by schema).
    # Destinations are deterministic prospective paths disjoint from live inputs.
    if "\\" in proposal_dir or ".." in Path(proposal_dir).parts:
        raise _fail("RETENTION_DIR_TRAVERSAL", f"proposal dir unsafe: {proposal_dir}")
    seen_dest: set[str] = set()
    inputs = set(col.files)
    rows = []
    for node in graph["nodes"]:
        entry: dict[str, Any] = {"roles": node["roles"],
                                 "path": node["path"], "sha256": node["sha256"],
                                 "byte_count": node["byte_count"], "policy": node["policy"]}
        if node["policy"] == "KEEP_IMMUTABLE":
            entry["retained_ref"] = {"path": node["path"], "sha256": node["sha256"]}
        else:
            dest = (proposal_dir + "/retained/before/" + node["path"]).replace("//", "/")
            if "\\" in dest or ".." in Path(dest).parts:
                raise _fail("RETENTION_DEST_TRAVERSAL", f"retention destination unsafe: {dest}")
            # Raw ancestor alias checks even though dest is absent (prospective).
            cursor = col.root
            for part in Path(dest).parent.parts:
                # Skip root-absolute prefix components that are part of col.root?
                # Walk repo-relative parent parts only.
                pass
            # Walk repo-relative ancestors of dest for symlinked components.
            try:
                dest_rel_parts = Path(dest).parts if not Path(dest).is_absolute() else \
                    Path(dest).relative_to(col.root).parts
            except ValueError:
                raise _fail("RETENTION_DEST_ESCAPE", f"retention destination escapes root: {dest}") from None
            # If dest was given repo-relative (normal case), parts are already relative.
            # For absolute dest under root, use relative parts; else refuse above.
            # Determine relative parts robustly:
            if Path(dest).is_absolute():
                try:
                    rel_parts = Path(dest).relative_to(col.root).parts
                except ValueError:
                    raise _fail("RETENTION_DEST_ESCAPE", f"retention destination escapes root: {dest}") from None
            else:
                rel_parts = Path(dest).parts
                # Repo-relative dest must not start with / or contain dotdot (checked).
                if Path(dest).is_absolute():
                    raise _fail("RETENTION_DEST_ESCAPE", f"retention destination escapes root: {dest}")
            cursor = col.root
            for part in rel_parts[:-1]:
                if part in ("..", ".", ""):
                    raise _fail("RETENTION_DEST_TRAVERSAL", f"retention destination unsafe part: {dest}")
                cursor = cursor / part
                try:
                    if cursor.is_symlink():
                        raise _fail("RETENTION_DEST_ALIAS", f"retention ancestor is symlink: {dest}")
                except OSError as exc:
                    raise _fail("PATH_UNREADABLE", f"retention ancestor unreadable: {dest}: {exc}") from exc
            if dest in inputs:
                raise _fail("RETENTION_OVERLAP", f"retention destination overlaps live input: {dest}")
            # Namespace overlap: dest must not be ancestor/descendant of any live input.
            for live in inputs:
                if dest == live or dest.startswith(live.rstrip("/") + "/") or live.startswith(dest.rstrip("/") + "/"):
                    raise _fail("RETENTION_OVERLAP", f"retention destination overlaps live input namespace: {dest}")
            if dest in seen_dest:
                raise _fail("RETENTION_DEST_CONFLICT", f"duplicate retention destination: {dest}")
            seen_dest.add(dest)
            # Absent required (including dangling aliases); never bless unknown bytes.
            try:
                if (col.root / dest).is_symlink() or (col.root / dest).exists():
                    raise _fail("RETENTION_DEST_CONFLICT",
                                f"retention destination already present (no overwrite): {dest}")
            except OSError as exc:
                raise _fail("PATH_UNREADABLE", f"retention destination unreadable: {dest}: {exc}") from exc
            entry["retained_dest"] = dest
        rows.append(entry)
    rows.sort(key=lambda row: row["path"])
    return rows


def _pipeline(col: _Collector, root: Path, state_path: Path, new_authored_value: str | Path,
              proposal_id: str, tree_entry: dict[str, str],
              change_description: str | None = None) -> dict[str, Any]:
    _check_proposal_id(proposal_id)
    state_file = col.safe(state_path, "Production State")
    # Load State from pinned bytes (raw-first, no second-read switch).
    try:
        state = json.loads(col.files[col.rel(state_file)].decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _fail("STATE_UNREADABLE", f"Production State bytes are not JSON: {exc}") from exc
    if not isinstance(state, dict):
        raise _fail("STATE_UNREADABLE", "Production State is not a JSON object")
    # Config via safe (raw-first), loaded from pinned bytes.
    cfg_path = col.safe(core.DEFAULT_CONFIG.as_posix(), "implementation config")
    try:
        cfg = json.loads(col.files[col.rel(cfg_path)].decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _fail("CONFIG_UNREADABLE", f"implementation config bytes are not JSON: {exc}") from exc
    if agent.validate_agent_state(root, cfg, state):
        raise _fail("STATE_INVALID", "Production State fails strict validation")
    _eligibility(state)
    profile = _load_profile(col, state)
    # Canonical State enforcement: State path must equal Profile/config-derived
    # authoritative State path; an unreferenced clone is not live authority.
    try:
        src_root_for_state = core.repo_local_path(root, profile["paths"]["source_root"], "paths.source_root")
        canonical_state = (src_root_for_state / cfg["state_authority"]["authoritative_filename"]).resolve()
    except (KeyError, TypeError, ValueError) as exc:
        raise _fail("STATE_CANONICAL_INVALID", f"cannot derive canonical State path: {exc}") from exc
    if state_file.resolve() != canonical_state:
        raise _fail("STATE_NOT_CANONICAL", "Production State path is not the canonical authoritative State")
    route = _route_of(profile)
    # Canonical proposal directory under validated source_root (exact, not final2 names only).
    try:
        source_root_rel = profile["paths"]["source_root"]
        source_root_abs = core.repo_local_path(root, source_root_rel, "paths.source_root")
    except (KeyError, TypeError, ValueError) as exc:
        raise _fail("PROFILE_ROOT_INVALID", f"profile source_root invalid: {exc}") from exc
    expected_proposal_dir = (Path(source_root_rel) / "publication" / "v2" /
                             "editorial-corrections" / proposal_id).as_posix()
    # Authoring input must already be at the named proposal authoring-input.json
    # BEFORE prepare (fixtures/operator stage it outside P1; P1 writes nothing).
    # This avoids external-path refs silently accepted by digest alone.
    new_authored_abs = col.safe(new_authored_value, "new publication-authored input")
    new_authored_rel = col.rel(new_authored_abs)
    if new_authored_rel != (expected_proposal_dir + "/authoring-input.json").replace("//", "/"):
        raise _fail("AUTHORING_NOT_STAGED",
                    f"authoring input must already be at {expected_proposal_dir}/authoring-input.json")
    # Proposal dir layout checks: repo-local, no traversal/alias, disjoint from live canonical.
    if "\\" in expected_proposal_dir or ".." in Path(expected_proposal_dir).parts:
        raise _fail("PROPOSAL_LAYOUT", "proposal directory unsafe")
    # Planned reader ref (prospective; file need not exist at prepare time).
    planned_reader_rel = (expected_proposal_dir + "/reader-surface-input-v2.json").replace("//", "/")
    original_record, original_rows = _original_checkpoint(col, root, state)
    effective, active_record = _active_effective(col, root, cfg, state, original_rows)
    allowed = agent._publication_revalidation_roles(root, cfg, state)
    for row in original_rows:
        if allowed.get(row["name"]) != row["path"]:
            raise _fail("ROW_NOT_CANONICAL", f"original row outside configured roles: {row['name']}")

    try:
        manuscript_doc = reader.validate_manuscript_manifest(
            root, root / effective["reader-manuscript"]["path"], issue_id=state.get("issue_id"))
    except ValueError as exc:
        raise _fail("MANUSCRIPT_INVALID", f"reader manuscript validation failed: {exc}") from exc
    gate_abs = col.safe(effective["reader-surface-gate"]["path"], "active Gate record")
    try:
        gate_hint = json.loads(col.files[col.rel(gate_abs)].decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _fail("GATE_UNREADABLE", f"active Gate record not JSON: {exc}") from exc
    receipt_rel = ((gate_hint.get("derivation") or {}).get("receipt") or {}).get("path")
    if not receipt_rel:
        raise _fail("GATE_RECEIPT_SHAPE", "gate record carries no receipt binding")
    receipt_file = col.safe(receipt_rel, "generated receipt")
    try:
        envelope = json.loads(col.files[col.rel(receipt_file)].decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _fail("RECEIPT_UNREADABLE", f"generated receipt is not JSON: {exc}") from exc
    if not isinstance(envelope, dict):
        raise _fail("RECEIPT_UNREADABLE", "generated receipt is not a JSON object")
    try:
        before_authored_rel = next(
            row["path"] for row in envelope.get("authored_refs", [])
            if isinstance(row, dict) and row.get("name") == "publication-semantic-input")
        envelope_reader_rel = (envelope.get("reviewed_reader_input") or {}).get("path")
    except (AttributeError, TypeError, StopIteration) as exc:
        raise _fail("RECEIPT_REF_SHAPE", f"generated receipt routing refs unreadable: {exc}") from exc
    if not before_authored_rel or not envelope_reader_rel:
        raise _fail("RECEIPT_REF_SHAPE", "generated receipt lacks routing refs")
    before_context = _derive(col, root, route, state_file, before_authored_rel)
    reader_file = col.safe(envelope_reader_rel, "active-before reader input")
    before_canonical = _canonical(route, before_context["surface"])
    if reader_file.read_bytes() != before_canonical:
        raise _fail("NONCANONICAL_BEFORE", "active-before reader file is not canonical derivation bytes")

    proposed_context = _derive(col, root, route, state_file, new_authored_abs)
    proposed_canonical = _canonical(route, proposed_context["surface"])
    if proposed_canonical == before_canonical:
        raise _fail("NO_EDITORIAL_CHANGE", "proposed reader bytes identical to active-before bytes")
    # Proposed upstream authority must equal before authority (only authored delta allowed).
    _proposed_upstream_check(before_context, proposed_context)

    try:
        if route == LONGFORM_ROUTE:
            receipt = longform_generated.validate_receipt(root, receipt_file, state_file)
        else:
            receipt = weekly.validate_receipt(root, receipt_file, state_file)
    except ValueError as exc:
        raise _fail("RECEIPT_INVALID", f"generated receipt validation failed: {exc}") from exc
    renderer_commit = receipt["current_tools"]["repository_commit_sha"]
    if receipt["current_tools"]["contract"] != core.contract_identity(
            root, cfg, profile["research_profile"], profile["publication_profile"]):
        raise _fail("RECEIPT_CONTRACT_DRIFT", "validated receipt contract differs from current contract")
    if receipt["reviewed_reader_input"].get("path") != envelope_reader_rel:
        raise _fail("RECEIPT_BINDING_CHANGED", "validated receipt reader binding differs from routing read")
    _frozen_names_check(receipt, before_context)

    try:
        gate_record = surface_gate.validate_reader_surface_gate(
            root, root / effective["reader-surface-gate"]["path"], issue_id=state.get("issue_id"),
            publication_profile=profile.get("publication_profile"),
            expected_manuscript_path=root / effective["reader-manuscript"]["path"],
            state_path=state_file)
    except ValueError as exc:
        raise _fail("GATE_INVALID", f"active Gate validation failed: {exc}") from exc
    if gate_record.get("status") != "PASSED":
        raise _fail("GATE_NOT_PASSED", "active Gate record is not PASSED")
    try:
        pretex = surface_gate.load_and_validate_reader_surface_semantic_review(
            root, receipt["semantic_review"]["path"], expected_issue_id=state.get("issue_id"),
            expected_publication_profile=profile.get("publication_profile"),
            expected_surface_path=envelope_reader_rel,
            expected_surface_sha256=core.sha256_bytes(before_canonical), require_pass=True)
    except ValueError as exc:
        raise _fail("PRETEX_INVALID", f"pre-TeX review validation failed: {exc}") from exc
    try:
        bundle = quality.validate_bundle(
            root, root / effective["quality-regression-bundle"]["path"], issue_id=state.get("issue_id"))
    except ValueError as exc:
        raise _fail("BUNDLE_INVALID", f"quality bundle validation failed: {exc}") from exc
    state_rel = col.rel(state_file)
    graph, frozen, preserved_digest = _build_graph(
        col, root, state, original_rows, effective, active_record,
        receipt, col.rel(receipt_file), gate_record, manuscript_doc, bundle, pretex,
        state_rel, profile)
    graph_digest = core.sha256_object(graph)
    proposal_dir = expected_proposal_dir
    retention = _retention_plan(col, graph, proposal_dir)
    col.reverify()
    if _tree_map(root, Path(profile["paths"]["source_root"]),
                 Path(profile["paths"]["survey_root"])) != tree_entry:
        raise _fail("TREE_MOVED", "edition tree changed during inspection")
    # Re-derive planned refs from independently derived bytes (no silent file re-serialization).
    planned_reader_sha = core.sha256_bytes(proposed_canonical)
    planned_reader_ref = {"path": planned_reader_rel, "sha256": planned_reader_sha}
    # Author-supplied change_description is descriptive input (nonempty), not machine approval.
    if change_description is None:
        effective_description = f"editorial correction proposal {proposal_id}"
    else:
        if not isinstance(change_description, str) or not change_description.strip():
            raise _fail("CHANGE_DESCRIPTION_EMPTY", "change_description must be nonempty")
        effective_description = change_description
    new_authored_rel = col.rel(col.safe(new_authored_abs, "new publication-authored input"))
    proposal = {
        "schema_version": "2.0-rc1",
        "proposal_id": proposal_id,
        "issue_id": state.get("issue_id"),
        "research_profile": profile.get("research_profile"),
        "publication_profile": profile.get("publication_profile"),
        "route": "EDITORIAL_CORRECTION_PROPOSAL_V1",
        "status": "PROPOSED",
        "basis": {
            "state_ref": {"path": col.rel(state_file),
                           "sha256": core.sha256_bytes(col.files[col.rel(state_file)])},
            "validation_checkpoint_ref": dict((state.get("checkpoint_provenance") or {})["validation"]),
            "active_revalidation_ref": dict(state.get("publication_revalidation_provenance"))
            if state.get("publication_revalidation_provenance") else None,
            "active_reader_input_ref": {"path": envelope_reader_rel,
                                        "sha256": core.sha256_bytes(before_canonical)},
            "before_graph_digest": graph_digest,
            "preserved_upstream_digest": preserved_digest,
            "generated_receipt_ref": {"path": col.rel(receipt_file),
                                      "sha256": core.sha256_bytes(col.files[col.rel(receipt_file)])},
            "renderer_commit": renderer_commit,
            "contract_identity": receipt["current_tools"]["contract"],
        },
        "proposed": {
            "authoring_input_ref": {"path": new_authored_rel,
                                    "sha256": core.sha256_bytes(col.files[new_authored_rel])},
            "proposed_reader_ref": dict(planned_reader_ref),
            "proposed_reader_canonical_sha256": planned_reader_sha,
            "change_description": effective_description,
        },
        "retention_plan": retention,
    }
    return {"proposal": proposal, "proposed_canonical": proposed_canonical,
            "before_canonical": before_canonical, "graph": graph, "frozen": frozen,
            "effective": effective, "original_rows": original_rows,
            "active_record": active_record, "route": route,
            "before_authored_rel": before_authored_rel,
            "new_authored_rel": new_authored_rel, "reader_rel": envelope_reader_rel,
            "planned_reader_ref": dict(planned_reader_ref), "proposal_dir": proposal_dir}


def _frozen_names_check(receipt: dict[str, Any], context: dict[str, Any]) -> None:
    receipt_names = {row["name"] for row in receipt.get("accepted_refs", [])}
    context_names = {row["name"] for row in context.get("accepted_refs", [])}
    if receipt_names != context_names:
        raise _fail("UPSTREAM_SET_DRIFT", "receipt accepted authority differs from rederived authority")
    for row in receipt.get("accepted_refs", []):
        match = next(item for item in context["accepted_refs"] if item["name"] == row["name"])
        if match["sha256"] != row["sha256"]:
            raise _fail("UPSTREAM_REF_DRIFT", f"accepted authority drifted: {row['name']}")


def _proposed_upstream_check(before_context: dict[str, Any], proposed_context: dict[str, Any]) -> None:
    # Proposed derivation must share exact upstream authority with before;
    # only the publication-authored input delta is allowed.
    before_names = {row["name"] for row in before_context.get("accepted_refs", [])}
    proposed_names = {row["name"] for row in proposed_context.get("accepted_refs", [])}
    if before_names != proposed_names:
        raise _fail("PROPOSED_UPSTREAM_SET_DRIFT",
                    "proposed accepted authority differs from before authority")
    for row in before_context.get("accepted_refs", []):
        match = next(item for item in proposed_context["accepted_refs"] if item["name"] == row["name"])
        if match["sha256"] != row["sha256"] or match["path"] != row["path"]:
            raise _fail("PROPOSED_UPSTREAM_REF_DRIFT",
                        f"proposed upstream differs from before: {row['name']}")
    if before_context.get("archive_path") != proposed_context.get("archive_path"):
        raise _fail("PROPOSED_ARCHIVE_DRIFT", "proposed drafting archive path differs from before")
    # Archive bytes already pinned via _derive (both pinned); verify equality.
    # Architecture authority equality is covered by accepted_refs (issue-architecture)
    # plus manuscript validation; explicit check here for clarity.
    if before_context.get("profile", {}).get("issue_id") != proposed_context.get("profile", {}).get("issue_id"):
        raise _fail("PROPOSED_PROFILE_DRIFT", "proposed profile identity differs from before")


def _canonical_state_path(root: Path, cfg: dict[str, Any], profile: dict[str, Any]) -> Path:
    try:
        src = core.repo_local_path(root, profile["paths"]["source_root"], "paths.source_root")
        return (src / cfg["state_authority"]["authoritative_filename"]).resolve()
    except (KeyError, TypeError, ValueError) as exc:
        raise _fail("STATE_CANONICAL_INVALID", f"cannot derive canonical State path: {exc}") from exc


def prepare_proposal(root: str | Path, state_path: str | Path,
                     authoring_path: str | Path, proposal_id: str,
                     change_description: str | None = None) -> dict[str, Any]:
    """Read-only before validation plus real proposed derivation (in memory).

    The authoring file must already be staged at the canonical
    ``<source_root>/publication/v2/editorial-corrections/<proposal_id>/authoring-input.json``
    BEFORE calling (fixtures/operator prepare it outside P1; P1 writes nothing).
    The planned proposed-reader ref is prospective (file need not exist yet).
    Author-supplied ``change_description`` (nonempty) is preserved as descriptive
    input; when omitted a generated placeholder is used.
    """
    root_path = Path(root)
    col = _Collector(root_path)
    # Preview loads via safe (raw-first) from pinned bytes.
    state_abs = col.safe(state_path, "Production State")
    try:
        state_preview = json.loads(col.files[col.rel(state_abs)].decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _fail("STATE_UNREADABLE", f"Production State preview not JSON: {exc}") from exc
    prof_abs = col.safe(state_preview["profile"]["path"], "Production Profile")
    try:
        profile_preview = json.loads(col.files[col.rel(prof_abs)].decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _fail("PROFILE_UNREADABLE", f"Production Profile preview not JSON: {exc}") from exc
    tree_entry = _tree_map(root_path, Path(profile_preview["paths"]["source_root"]),
                            Path(profile_preview["paths"]["survey_root"]))
    result = _pipeline(col, root_path, Path(state_path), authoring_path, proposal_id, tree_entry,
                       change_description)
    schema_gate.validate_instance(result["proposal"], root_path / PROPOSAL_SCHEMA,
                                  label="editorial correction proposal")
    return result


def _validate_scope(col: _Collector, root: Path, scope_review_value: str | Path,
                    proposal: dict[str, Any], state: dict[str, Any],
                    profile: dict[str, Any]) -> str:
    raw_path = col.safe(scope_review_value, "scope review record")
    captured = raw_path.read_bytes()
    try:
        raw = json.loads(captured.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _fail("SCOPE_UNREADABLE", f"scope review bytes are not JSON: {exc}") from exc
    if not isinstance(raw, dict):
        raise _fail("SCOPE_UNREADABLE", "scope review is not a JSON object")
    # After binding is the persisted proposed_reader_ref (path+sha); its sha must
    # equal the persisted canonical sha (enforced by validate_proposal equality).
    proposed_block = proposal.get("proposed") or {}
    reader_ref = proposed_block.get("proposed_reader_ref") or {}
    after_ref = {"path": reader_ref.get("path", ""), "sha256": reader_ref.get("sha256", "")}
    if not isinstance(after_ref["path"], str) or not after_ref["path"] or \
            not isinstance(after_ref["sha256"], str) or len(after_ref["sha256"]) != 64:
        raise _fail("SCOPE_AFTER_SHAPE", "proposal lacks exact proposed_reader_ref for scope binding")
    try:
        authority = surface_gate.load_and_validate_reader_surface_semantic_review(
            root, raw_path, expected_issue_id=state.get("issue_id"),
            expected_publication_profile=profile.get("publication_profile"),
            expected_surface_path=after_ref["path"],
            expected_surface_sha256=after_ref["sha256"], require_pass=True)
    except ValueError as exc:
        raise _fail("SCOPE_ORDINARY_INVALID", str(exc)) from exc
    if raw_path.read_bytes() != captured:
        raise _fail("SCOPE_BYTES_SWITCHED", "scope review file changed around loader call")
    if core.sha256_object({k: v for k, v in raw.items() if k != "review_sha256"}) != raw.get("review_sha256"):
        raise _fail("SCOPE_DIGEST_MISMATCH", "scope review object digest does not bind captured JSON")
    if authority.get("review_sha256") != raw.get("review_sha256"):
        raise _fail("SCOPE_DIGEST_MISMATCH", "loader digest does not bind captured review bytes")
    block = raw.get("editorial_correction_scope")
    if block is None:
        return RESULT_REQUIRED
    if not isinstance(block, dict) or block.get("version") != SCOPE_VERSION:
        raise _fail("SCOPE_BLOCK_SHAPE", "scope block version invalid")
    if block.get("decision") != "WITHIN_APPROVED_AUTHORITY":
        raise _fail("SCOPE_NOT_WITHIN_AUTHORITY",
                    f"scope decision cannot bind a correction: {block.get('decision')}")
    if block.get("before_reader_input") != proposal["basis"]["active_reader_input_ref"]:
        raise _fail("SCOPE_WRONG_BEFORE", "scope block before-reader does not match proposal basis")
    after_binding = {"path": after_ref["path"], "sha256": after_ref["sha256"]}
    if authority.get("surface_path") != after_binding["path"] or \
            authority.get("surface_sha256") != after_binding["sha256"]:
        raise _fail("SCOPE_WRONG_AFTER", "scope review does not target the proposed reader")
    if block.get("preserved_upstream_sha256") != proposal["basis"]["preserved_upstream_digest"]:
        raise _fail("SCOPE_STALE_UPSTREAM", "scope block upstream digest does not match proposal")
    if not isinstance(block.get("change_summary"), str) or not block["change_summary"].strip():
        raise _fail("SCOPE_BLOCK_SHAPE", "scope block change_summary empty")
    if not isinstance(block.get("evidence_locations"), list) or \
            not all(isinstance(item, str) and item.strip() for item in block["evidence_locations"]):
        raise _fail("SCOPE_BLOCK_SHAPE", "scope block evidence_locations empty")
    scope_checks = [c for c in authority.get("checks", []) if c.get("check_id") == SCOPE_CHECK_ID]
    if not scope_checks or any(c.get("status") != "PASS" for c in scope_checks):
        raise _fail("SCOPE_CHECK_NOT_PASS", "substantive scope check missing or not PASS")
    for check in scope_checks:
        if not check.get("detail", "").strip() or not check.get("evidence_locations"):
            raise _fail("SCOPE_CHECK_NOT_PASS", "scope check lacks substantive detail/evidence")
    return RESULT_BOUND


def validate_proposal(root: str | Path, state_path: str | Path, proposal_path: str | Path,
                      scope_review_path: str | Path | None = None) -> dict[str, Any]:
    """Re-derive from named FILE bytes; return typed result plus input hashes.

    Compares ALL derived identity/ref/digest fields (top-level, basis,
    authoring PATH+sha, proposed reader PATH+sha/canonical sha, retention);
    author-supplied ``change_description`` need only be nonempty (not equal to
    a generated placeholder). Returns the supplied proposal UNCHANGED
    (schema-valid) plus separate measured binding data; never repairs claims.
    """
    root_path = Path(root)
    col = _Collector(root_path)
    cfg_abs = col.safe(core.DEFAULT_CONFIG.as_posix(), "implementation config")
    try:
        cfg = json.loads(col.files[col.rel(cfg_abs)].decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _fail("CONFIG_UNREADABLE", f"implementation config not JSON: {exc}") from exc
    proposal_file = col.safe(proposal_path, "editorial correction proposal")
    if Path(proposal_file).name != "proposal.json":
        raise _fail("PROPOSAL_FILENAME", "proposal file must be named proposal.json")
    try:
        proposal = json.loads(col.files[col.rel(proposal_file)].decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _fail("PROPOSAL_UNREADABLE", f"proposal file not JSON: {exc}") from exc
    schema_gate.validate_instance(proposal, root_path / PROPOSAL_SCHEMA,
                                  label="editorial correction proposal")
    proposal_id = proposal.get("proposal_id")
    _check_proposal_id(proposal_id)
    # Exact canonical proposal directory under validated source_root (not final2 only).
    # State/Profile preview first to derive expected dir (raw-first, pinned).
    state_prev_abs = col.safe(state_path, "Production State")
    try:
        state_preview = json.loads(col.files[col.rel(state_prev_abs)].decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _fail("STATE_UNREADABLE", f"Production State preview not JSON: {exc}") from exc
    prof_prev_abs = col.safe(state_preview.get("profile", {}).get("path", ""), "Production Profile")
    try:
        profile_preview = json.loads(col.files[col.rel(prof_prev_abs)].decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _fail("PROFILE_UNREADABLE", f"Production Profile preview not JSON: {exc}") from exc
    try:
        expected_dir = (Path(profile_preview["paths"]["source_root"]) / "publication" / "v2" /
                        "editorial-corrections" / proposal_id).as_posix()
    except (KeyError, TypeError) as exc:
        raise _fail("PROPOSAL_LAYOUT", f"cannot derive canonical proposal dir: {exc}") from exc
    proposal_dir = proposal_file.parent
    # Compare canonical dir exactly (repo-relative posix, root-anchored).
    try:
        observed_dir_rel = proposal_dir.resolve().relative_to(col.root).as_posix()
    except ValueError:
        raise _fail("PROPOSAL_LAYOUT", "proposal file outside repository") from None
    if observed_dir_rel != expected_dir:
        raise _fail("PROPOSAL_LAYOUT", f"proposal file outside canonical dir {expected_dir}: {observed_dir_rel}")
    # Require regular, contained, alias-free named layout; P1 never overwrites.
    for name in PROPOSAL_FILES:
        candidate = proposal_dir / name
        # Use safe pin for regular/alias/FIFO checks (no silent FIFO open).
        try:
            col.safe(candidate.relative_to(col.root).as_posix()
                     if candidate.is_absolute() and str(candidate).startswith(str(col.root))
                     else (observed_dir_rel + "/" + name), f"proposal directory entry {name}")
        except ProposalError as exc:
            raise _fail("PROPOSAL_LAYOUT", f"proposal directory entry invalid {name}: {exc}") from exc
    staged_authored = col.safe(observed_dir_rel + "/authoring-input.json", "staged authoring input")
    staged_reader = col.safe(observed_dir_rel + "/reader-surface-input-v2.json", "staged proposed reader")
    # Exact supplied refs (PATH+sha) checked against staged FILE bytes below via rederivation;
    # here ensure supplied change_description nonempty (descriptive, not approval).
    supplied_proposed = proposal.get("proposed") or {}
    if not isinstance(supplied_proposed.get("change_description"), str) or \
            not supplied_proposed["change_description"].strip():
        raise _fail("CHANGE_DESCRIPTION_EMPTY", "supplied change_description must be nonempty")
    if supplied_proposed.get("authoring_input_ref", {}).get("path") != \
            (expected_dir + "/authoring-input.json").replace("//", "/"):
        raise _fail("PROPOSED_AUTHORING_PATH", "supplied authoring ref path not canonical proposal input")
    if core.sha256_bytes(col.files[col.rel(staged_authored)]) != \
            supplied_proposed.get("authoring_input_ref", {}).get("sha256", ""):
        raise _fail("PROPOSED_AUTHORING_MISMATCH", "staged authoring bytes differ from proposal ref")
    # Supplied proposed reader ref must be canonical planned path; sha checked via rederivation.
    if supplied_proposed.get("proposed_reader_ref", {}).get("path") != \
            (expected_dir + "/reader-surface-input-v2.json").replace("//", "/"):
        raise _fail("PROPOSED_READER_PATH", "supplied proposed reader ref path not canonical")
    tree_entry = _tree_map(root_path, Path(profile_preview["paths"]["source_root"]),
                            Path(profile_preview["paths"]["survey_root"]))
    # Rederive with supplied change_description so description equality is by construction;
    # all other fields must match exactly (no silent repair).
    result = _pipeline(col, root_path, Path(state_path), staged_authored, proposal_id, tree_entry,
                       supplied_proposed.get("change_description"))
    rederived = result["proposal"]
    # Compare ALL derived identity/ref/digest fields (except change_description already by construction).
    for key in ("schema_version", "proposal_id", "issue_id", "research_profile",
                "publication_profile", "route", "status"):
        if rederived.get(key) != proposal.get(key):
            raise _fail("HEADER_MISMATCH", f"rederived {key} differs from supplied proposal")
    if rederived["basis"] != proposal["basis"]:
        raise _fail("BASIS_MISMATCH", "rederived basis differs from supplied proposal")
    # Authoring PATH+sha and proposed reader PATH+sha/canonical sha must match exactly.
    if rederived["proposed"]["authoring_input_ref"] != supplied_proposed.get("authoring_input_ref"):
        raise _fail("PROPOSED_AUTHORING_MISMATCH", "rederived authoring ref differs from supplied")
    if rederived["proposed"]["proposed_reader_ref"] != supplied_proposed.get("proposed_reader_ref"):
        raise _fail("PROPOSED_READER_MISMATCH", "rederived proposed reader ref differs from supplied")
    if rederived["proposed"]["proposed_reader_canonical_sha256"] != \
            supplied_proposed.get("proposed_reader_canonical_sha256"):
        raise _fail("PROPOSED_DIGEST_MISMATCH", "rederived canonical digest differs from supplied")
    # Change_description already ensured nonempty; rederived equals supplied by construction.
    if rederived["proposed"]["change_description"] != supplied_proposed.get("change_description"):
        raise _fail("CHANGE_DESCRIPTION_MISMATCH", "rederived description differs from supplied")
    if rederived["proposed"]["proposed_reader_ref"]["sha256"] != \
            rederived["proposed"]["proposed_reader_canonical_sha256"]:
        raise _fail("PROPOSED_REF_DIGEST_MISMATCH", "planned reader ref sha differs from canonical sha")
    if result["proposal"]["retention_plan"] != proposal["retention_plan"]:
        raise _fail("RETENTION_MISMATCH", "rederived retention plan differs from supplied proposal")
    if staged_reader.read_bytes() != result["proposed_canonical"]:
        raise _fail("PROPOSED_BYTES_MISMATCH", "staged proposed reader differs from rederived canonical bytes")
    # Load State/Profile for scope binding (from pinned bytes, no second-read switch).
    state_abs2 = col.safe(state_path, "Production State")
    try:
        state = json.loads(col.files[col.rel(state_abs2)].decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise _fail("STATE_UNREADABLE", f"Production State not JSON: {exc}") from exc
    profile = _load_profile(col, state)
    if scope_review_path is None:
        outcome = RESULT_REQUIRED
    else:
        outcome = _validate_scope(col, root_path, scope_review_path, proposal, state, profile)
    # Final stability + control/receipt rechecks AFTER scope (tree check ended inside _pipeline before scope).
    col.reverify()
    if _tree_map(root_path, Path(profile["paths"]["source_root"]),
                 Path(profile["paths"]["survey_root"])) != tree_entry:
        raise _fail("TREE_MOVED", "edition tree changed after scope validation")
    # All-control/current-receipt predicates again before return (HEAD/config alone
    # does not catch dirty unlisted helper/schema after initial receipt validation).
    try:
        current_contract = core.contract_identity(root_path, cfg, profile.get("research_profile"),
                                                  profile.get("publication_profile"))
    except (KeyError, ValueError) as exc:
        raise _fail("CONTRACT_UNREADABLE", f"current contract unreadable: {exc}") from exc
    if result["proposal"]["basis"]["contract_identity"] != current_contract:
        raise _fail("RECEIPT_CONTRACT_DRIFT", "contract drifted after scope validation")
    # Return supplied proposal UNCHANGED (schema-valid) plus measured binding data.
    return {"result": outcome,
            "input_hashes": {rel: core.sha256_bytes(data) for rel, data in col.files.items()},
            "proposal": proposal,
            "measured": {"before_graph_digest": result["proposal"]["basis"]["before_graph_digest"],
                         "preserved_upstream_digest": result["proposal"]["basis"]["preserved_upstream_digest"],
                         "proposed_reader_sha256": core.sha256_bytes(result["proposed_canonical"]),
                         "graph_nodes": len(result["graph"]["nodes"]),
                         "graph_edges": len(result["graph"]["edges"])}}
