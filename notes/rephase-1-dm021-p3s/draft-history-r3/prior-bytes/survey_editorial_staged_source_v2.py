#!/usr/bin/env python3
"""DM021-P3S post-review staged source materialization + standalone replay.

Two entry points (no CLI, no State adoption, no Gate/Candidate/PDF):

  materialize_staged_source(root, state_path, proposal_path,
                            retention_manifest_path, scope_review_path)
      One-shot current-scoped writer. Calls actual fresh P2V
      ``observe_current_authority`` INSIDE its own invocation (lazy import so
      the observer never leaks into the verifier's claimed closure), renders
      the already-derived proposed reader through the existing route
      renderers, exclusively claims ``<proposal_dir>/staged-source/`` with
      exactly main.tex + references.bib + jgaisurvey.sty, publishes the staged
      manifest LAST, then runs standalone replay + a second fresh P2V and
      compares stable facts only.

  verify_staged_source(root, proposal_path, staged_manifest_path)
      Standalone read-only retained/staged consistency + deterministic replay.
      Never calls P2V, never validates current State, never compares current
      HEAD to producer HEAD. Derives the expected retention path from the
      supplied staged manifest and the historical namespace from P2R-verified
      retained bytes.

All refusals raise StagedSourceError (a ValueError) with structured
code/phase/disposition/detail/owned/cause. Pre-write refusals create nothing;
post-claim failures preserve owned partials and never report success; a failed
close/final check that leaves complete valid bytes reports
INDETERMINATE_INVOCATION (not success); later artifact verification may then
attest byte-consistency only.
"""
from __future__ import annotations

import json
import os
import stat as _stat
import subprocess
import sys
from pathlib import Path
from typing import Any

from scripts import survey_editorial_correction_proposal_v2 as p1mod
from scripts import survey_editorial_retention_v2 as retention
from scripts import survey_longform_derivation_v2 as longform_derivation
from scripts import survey_longform_generated_v2 as longform_generated
from scripts import survey_production_v2 as core
from scripts import survey_reader_surface_gate_v2 as surface_gate
from scripts import survey_schema_v2 as schema_gate
from scripts import survey_weekly_derivation_v2 as weekly

RESULT_MATERIALIZED = "STAGED_SOURCE_MATERIALIZED"
RESULT_VERIFIED = "STAGED_SOURCE_REPLAY_VERIFIED"

STAGED_DIRNAME = "staged-source"
MANIFEST_FILENAME = "staged-source-manifest.json"
MAIN_FILENAME = "main.tex"
BIBLIOGRAPHY_FILENAME = "references.bib"
STYLE_FILENAME = "jgaisurvey.sty"

STAGED_SCHEMA = Path("schemas/editorial-staged-source-manifest-v2.schema.json")
STAGED_MODULE = Path("scripts/survey_editorial_staged_source_v2.py")
P2V_MODULE = Path("scripts/survey_editorial_current_authority_v2.py")
STYLE_PATH = Path("templates/survey/jgaisurvey.sty")

LONGFORM_ROUTE = "LONGFORM_GENERATED_V1"
WEEKLY_ROUTE = "WEEKLY_GENERATED_V2"

LONGFORM_READER_SCHEMA = Path("schemas/longform-reader-input-v2.schema.json")
LONGFORM_RECEIPT_SCHEMA = Path("schemas/longform-publication-source-manifest-v2.schema.json")
LONGFORM_SEMANTIC_PUBLICATION = Path("scripts/survey_longform_semantic_publication_v2.py")
WEEKLY_READER_SCHEMA = Path("schemas/reader-surface-input-v2.schema.json")
WEEKLY_RECEIPT_SCHEMA = Path("schemas/weekly-publication-source-manifest-v2.schema.json")
WEEKLY_SEMANTIC_PUBLICATION = Path("scripts/survey_weekly_semantic_publication_v2.py")
PROPOSAL_SCHEMA = p1mod.PROPOSAL_SCHEMA
RETENTION_MANIFEST_SCHEMA = retention.MANIFEST_SCHEMA
REVIEW_SCHEMA = surface_gate.SEMANTIC_REVIEW_SCHEMA
GATE_SCHEMA = surface_gate.SURFACE_GATE_SCHEMA

_UNSAFE_GIT_VARS = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_PREFIX")

# Fixed shared load closure: every repo .py reachable via top-level imports
# from this module's own top-level imports (AST-derived, fixpoint). All are
# loaded at verifier import time, hence all are pinned for runtime binding.
# Nested (function-local) imports on paths the writer/verifier never execute
# (e.g. R1 refresh, screening internals) are NOT pinned; any new call edge to
# them is an exact blocker requiring an S2 extension, never silent execution.
_SHARED_PY = (
    "scripts/render_article_draft_tex.py",
    "scripts/survey_agent_control_v2.py",
    "scripts/survey_agent_tool_v2.py",
    "scripts/survey_architecture_v2.py",
    "scripts/survey_architecture_v2_base.py",
    "scripts/survey_bibliography_access_provenance_v2.py",
    "scripts/survey_completeness_v2.py",
    "scripts/survey_drafting_citation_refs_v2.py",
    "scripts/survey_drafting_v2.py",
    "scripts/survey_drafting_v2_base.py",
    "scripts/survey_editorial_correction_proposal_v2.py",
    "scripts/survey_editorial_retention_v2.py",
    "scripts/survey_evidence_v2.py",
    "scripts/survey_longform_derivation_v2.py",
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_production_v2.py",
    "scripts/survey_publication_v2.py",
    "scripts/survey_quality_v2.py",
    "scripts/survey_reader_fidelity_v2.py",
    "scripts/survey_reader_publication_v2.py",
    "scripts/survey_reader_surface_gate_v2.py",
    "scripts/survey_review_attention_v2.py",
    "scripts/survey_schema_v2.py",
    "scripts/survey_screening_v2.py",
    "scripts/survey_weekly_derivation_v2.py",
    "scripts/validate_article_draft.py",
    "scripts/weekly_pipeline.py",
)

_SHARED_SCHEMAS = (
    "schemas/editorial-correction-proposal-v2.schema.json",
    "schemas/editorial-retention-manifest-v2.schema.json",
    "schemas/editorial-staged-source-manifest-v2.schema.json",
    "schemas/reader-surface-gate-v2.schema.json",
    "schemas/reader-surface-semantic-review-v2.schema.json",
)


def _route_code_deps(route: str) -> tuple[str, ...]:
    """Exact fixed sorted-unique replay dependency set for one route."""
    if route == LONGFORM_ROUTE:
        extra = (LONGFORM_READER_SCHEMA.as_posix(), LONGFORM_RECEIPT_SCHEMA.as_posix(),
                 LONGFORM_SEMANTIC_PUBLICATION.as_posix())
    elif route == WEEKLY_ROUTE:
        extra = (WEEKLY_READER_SCHEMA.as_posix(), WEEKLY_RECEIPT_SCHEMA.as_posix(),
                 WEEKLY_SEMANTIC_PUBLICATION.as_posix())
    else:
        raise StagedSourceError("UNKNOWN_ROUTE", "PIN", "REFUSED_PRE_WRITE",
                                f"unsupported staged route: {route}")
    members = (set(_SHARED_PY) | set(_SHARED_SCHEMAS) | set(extra)
               | {STAGED_MODULE.as_posix(), STYLE_PATH.as_posix()})
    ordered = tuple(sorted(members))
    if len(ordered) != 27 + 5 + 3 + 1 + 1:
        raise StagedSourceError("CODE_DEPS_SHAPE", "PIN", "REFUSED_PRE_WRITE",
                                f"fixed S2 set changed size: {len(ordered)}")
    return ordered


class StagedSourceError(ValueError):
    """Typed staged-source refusal with structured fields."""

    def __init__(self, code: str, phase: str, disposition: str, detail: str,
                 owned: dict[str, Any] | None = None,
                 cause: BaseException | None = None) -> None:
        super().__init__(f"{code}: [{phase}/{disposition}] {detail}")
        self.code = code
        self.phase = phase
        self.disposition = disposition
        self.detail = detail
        self.owned: dict[str, Any] = owned if owned is not None else {}
        if cause is not None:
            self.__cause__ = cause


def _fail(code: str, phase: str, disposition: str, detail: str,
          owned: dict[str, Any] | None = None,
          cause: BaseException | None = None) -> StagedSourceError:
    return StagedSourceError(code, phase, disposition, detail, owned, cause)


class _SessionScopeReader:
    """Narrow safe-reader shim exposing ONLY the surface P1 scope uses.

    P1 ``_validate_scope`` touches exactly one collector method,
    ``col.safe(value, label)``, plus passed proposal/State/Profile data.
    This shim backs ``safe`` with an actual P2R ``_Session`` (dirfd/no-follow
    pins over the retained history) so no live ``_Collector`` (live HEAD +
    config) is ever constructed in the artifact verifier, and no dummy
    HEAD/config values or fabricated former-State dicts are introduced.
    """

    def __init__(self, session: Any) -> None:
        self._session = session
        self._root = session.root_resolved
        self.rels: list[str] = []

    def safe(self, value: str | Path, label: str) -> Path:
        rel, _data = self._session.safe_read(value, label, "VERIFY", "INVALID")
        if rel not in self.rels:
            self.rels.append(rel)
        return self._root / rel


def _canonical_json_bytes(value: Any) -> bytes:
    """Deterministic canonical bytes: recursive dict-key ordering.

    Mapping keys sort ascending at every level; arrays preserve semantic
    order (``code_deps`` is pre-sorted by path at construction and enforced).
    Serialized with the existing ``core.json_bytes`` (indent 2 + newline).
    """

    def _canon(node: Any) -> Any:
        if isinstance(node, dict):
            return {k: _canon(node[k]) for k in sorted(node)}
        if isinstance(node, (list, tuple)):
            return [_canon(item) for item in node]
        return node

    return core.json_bytes(_canon(value))


def _manifest_digest(manifest: dict[str, Any]) -> str:
    """Self-digest excluding the digest field (review_sha256 precedent)."""
    body = {k: v for k, v in manifest.items() if k != "manifest_digest"}
    return core.sha256_object(body)


def _ordered_sized_ref(ref: dict[str, Any], label: str, phase: str, disp: str) -> dict[str, Any]:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256", "byte_count"}:
        raise _fail("REF_SHAPE", phase, disp, f"{label} is not an exact {{path,sha256,byte_count}} record")
    if not isinstance(ref["path"], str) or not ref["path"]:
        raise _fail("REF_SHAPE", phase, disp, f"{label} has invalid path")
    if not isinstance(ref["sha256"], str) or len(ref["sha256"]) != 64:
        raise _fail("REF_SHAPE", phase, disp, f"{label} has invalid sha256")
    if not isinstance(ref["byte_count"], int) or ref["byte_count"] < 1:
        raise _fail("REF_SHAPE", phase, disp, f"{label} has invalid byte_count")
    return {"path": ref["path"], "sha256": ref["sha256"], "byte_count": ref["byte_count"]}


def _ordered_ref(ref: dict[str, Any], label: str, phase: str, disp: str) -> dict[str, Any]:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"}:
        raise _fail("REF_SHAPE", phase, disp, f"{label} is not an exact {{path,sha256}} record")
    return {"path": ref["path"], "sha256": ref["sha256"]}


def _check_contract_identity(ci: Any, phase: str, disp: str) -> dict[str, str]:
    expected = ("pipeline_contract_version", "pipeline_contract_sha256",
                "quality_contract_version", "quality_contract_sha256",
                "research_profile_version", "research_profile_sha256",
                "publication_profile_version", "publication_profile_sha256")
    if not isinstance(ci, dict) or set(ci) != set(expected):
        raise _fail("CONTRACT_IDENTITY_SHAPE", phase, disp,
                    "basis.contract_identity must carry the strict 8 keys")
    return {k: ci[k] for k in expected}


def _attach_close(primary: StagedSourceError, close_exc: BaseException) -> None:
    detail = f"{primary.detail}; secondary closes: {close_exc}"
    primary.detail = detail
    primary.owned.setdefault("secondary_close_errors", []).append(str(close_exc))
    primary.args = (f"{primary.code}: [{primary.phase}/{primary.disposition}] {detail}",)


def _close_session(session: Any, phase: str, disp: str, primary: StagedSourceError | None = None) -> None:
    """Checked close that never drops StagedSourceError diagnostics.

    ``_Session._close_all`` only attaches secondaries to a ``RetentionError``
    prior, so a ``StagedSourceError`` primary is never passed as ``prior``;
    close failures are caught here as ``RetentionError`` and attached
    manually (or raised when no primary is in flight).
    """
    try:
        session._close_all(phase, disp)
    except Exception as exc:
        if primary is not None:
            _attach_close(primary, exc)
        else:
            raise _fail("CLOSE_FAILED", phase, disp,
                        f"descriptor close failed: {exc}", cause=exc) from exc


def _snapshot_originals(session: Any, control_rels: list[str], source_root_rel: str,
                          survey_root_rel: str, ret_rel: str, phase: str, disp: str):
    """Full original inventory snapshot (control + edition + retained).

    Uses the real snapshot helpers (no broad walk from unvalidated roots by
    the caller). Empty dirs are included; aliases/nonregulars refuse inside
    the helpers. Returns deep-copied plain dicts for later comparison.
    """
    try:
        ctrl_files, ctrl_dirs, ctrl_sizes = retention._snapshot_expanded(
            session, control_rels, "control", phase, disp)
        src_files, src_dirs, src_sizes = retention._snapshot_expanded(
            session, [source_root_rel, survey_root_rel], "edition", phase, disp)
        ret_files, ret_dirs, ret_sizes = retention._retained_inventory(
            session, ret_rel, phase, disp)
    except Exception as exc:
        if isinstance(exc, retention.RetentionError):
            raise _fail("SNAPSHOT_FAILED", phase, disp, f"snapshot failed: {exc}",
                        cause=exc) from exc
        raise _fail("SNAPSHOT_FAILED", phase, disp, f"snapshot failed: {exc}",
                    cause=exc) from exc
    return ((dict(ctrl_files), dict(ctrl_dirs), dict(ctrl_sizes)),
            (dict(src_files), dict(src_dirs), dict(src_sizes)),
            (dict(ret_files), dict(ret_dirs), dict(ret_sizes)))


def _compare_original_boundary(init_triple, session: Any, control_rels: list[str],
                               source_root_rel: str, survey_root_rel: str, ret_rel: str,
                               allowed_new_files: set[str], allowed_new_dirs: set[str],
                               phase: str, disp: str, owned: dict[str, Any]) -> None:
    """Re-inventory and compare against ORIGINAL snapshots (never rebaselined).

    Deletions AND additions refuse unless exactly the admitted owned delta;
    changed bytes/sizes/modes refuse. `Session.reverify` alone cannot see
    newly planted files/empty dirs, so full inventories are rewalked here.
    """
    cur = _snapshot_originals(session, control_rels, source_root_rel, survey_root_rel,
                              ret_rel, phase, disp)
    labels = ("control", "edition", "retained")
    for label, init, now in zip(labels, init_triple, cur):
        init_files, init_dirs, init_sizes = init
        cur_files, cur_dirs, cur_sizes = now
        allow_files = allowed_new_files if label == "edition" else set()
        allow_dirs = allowed_new_dirs if label == "edition" else set()
        for rel in init_files:
            if rel not in cur_files:
                raise _fail("ORIGINAL_DELETED", phase, disp,
                            f"{label} original file deleted: {rel}", owned)
        extra_files = set(cur_files) - set(init_files)
        if extra_files != allow_files:
            raise _fail("ORIGINAL_DRIFT", phase, disp,
                        f"{label} unexpected new files: {sorted(extra_files)}", owned)
        for rel, sha in init_files.items():
            if cur_files.get(rel) != sha:
                raise _fail("ORIGINAL_DRIFT", phase, disp,
                            f"{label} original file bytes changed: {rel}", owned)
            if cur_sizes.get(rel) != init_sizes.get(rel):
                raise _fail("ORIGINAL_DRIFT", phase, disp,
                            f"{label} original file size changed: {rel}", owned)
        for rel in init_dirs:
            if rel not in cur_dirs:
                raise _fail("ORIGINAL_DELETED", phase, disp,
                            f"{label} original dir deleted: {rel}", owned)
        extra_dirs = set(cur_dirs) - set(init_dirs)
        if extra_dirs != allow_dirs:
            raise _fail("ORIGINAL_DRIFT", phase, disp,
                        f"{label} unexpected new dirs: {sorted(extra_dirs)}", owned)
        for rel, mode in init_dirs.items():
            if cur_dirs.get(rel) != mode:
                raise _fail("ORIGINAL_DRIFT", phase, disp,
                            f"{label} original dir mode changed: {rel}", owned)


def _recheck_consumed_pins(live: Any, session: Any, orig_live_map: dict[str, bytes],
                           orig_ret_map: dict[str, bytes], head_pinned: str,
                           root_path: Path, phase: str, disp: str,
                           owned: dict[str, Any] | None) -> None:
    """Recheck every original consumed pin + HEAD (no newly captured baseline)."""
    if retention._git_head(root_path, "boundary HEAD", phase, disp or "REFUSED_PRE_WRITE") != head_pinned:
        raise _fail("HEAD_MOVED", phase, disp or "REFUSED_PRE_WRITE",
                    "HEAD changed at boundary", owned)
    if live.head != head_pinned:
        raise _fail("HEAD_MOVED", phase, disp or "REFUSED_PRE_WRITE",
                    "collector HEAD changed at boundary", owned)
    for rel, orig_bytes in orig_ret_map.items():
        cur = session.files.get(rel)
        if cur is None or cur != orig_bytes:
            raise _fail("PIN_DRIFT", phase, disp or "REFUSED_PRE_WRITE",
                        f"retained pin changed at boundary: {rel}", owned)
    for rel, orig_bytes in orig_live_map.items():
        cur = live.files.get(rel)
        if cur is None or cur != orig_bytes:
            raise _fail("PIN_DRIFT", phase, disp or "REFUSED_PRE_WRITE",
                        f"live pin changed at boundary: {rel}", owned)
    try:
        live.reverify()
    except Exception as exc:
        raise _fail("REVERIFY_FAILED", phase, disp or "REFUSED_PRE_WRITE",
                    f"live reverify failed at boundary: {exc}", owned) from exc
    try:
        session.reverify(phase, disp or "REFUSED_PRE_WRITE")
    except Exception as exc:
        raise _fail("REVERIFY_FAILED", phase, disp or "REFUSED_PRE_WRITE",
                    f"session reverify failed at boundary: {exc}", owned) from exc


def _check_runtime_binding(root: Path, pinned: dict[str, str], phase: str, disp: str) -> None:
    """Tripwire (not a hotpatch proof): every loaded S2 .py must resolve to
    the pinned repo-rel path with matching bytes. File-pin-only entries
    (semantic-publication producers, schemas, style) are byte-compared from
    disk, never imported, and are skipped here.

    R2-10: arbitrary same-basename ``.pyc`` acceptance is removed. A loaded
    ``.pyc`` path without a pinned ``.py`` source at the expected location
    refuses (pyc-only provenance is unsupported). Normal source imports under
    an isolated cache prefix remain supported because their ``__file__``
    resolves to the pinned ``.py`` path.
    """
    for rel, sha in sorted(pinned.items()):
        if not rel.endswith(".py"):
            continue
        if rel in (LONGFORM_SEMANTIC_PUBLICATION.as_posix(),
                   WEEKLY_SEMANTIC_PUBLICATION.as_posix()):
            continue
        stem = Path(rel).stem
        mod = sys.modules.get("scripts." + stem)
        if mod is None or not hasattr(mod, "__file__") or mod.__file__ is None:
            raise _fail("RUNTIME_BINDING_MISSING", phase, disp,
                        f"S2 module not loaded for binding: {rel}")
        loaded = Path(str(mod.__file__))
        expected = root / rel
        # R2-10: refuse pyc-only provenance outright; do not tolerate an
        # unrelated __pycache__ entry as if it proved source correspondence.
        if loaded.suffix == ".pyc":
            raise _fail("RUNTIME_BINDING_PYC", phase, disp,
                        f"S2 module loaded from .pyc without pinned .py source: {rel} -> {loaded}")
        try:
            same = loaded.resolve() == expected.resolve()
        except OSError:
            same = False
        if not same:
            raise _fail("RUNTIME_BINDING_PATH", phase, disp,
                        f"S2 module resolves away from pinned path: {rel}")
        try:
            data = loaded.read_bytes()
        except OSError as exc:
            raise _fail("RUNTIME_BINDING_UNREADABLE", phase, disp,
                        f"S2 module unreadable for binding: {rel}: {exc}") from exc
        if core.sha256_bytes(data) != sha:
            raise _fail("TOOL_DRIFT", phase, disp,
                        f"S2 runtime bytes differ from pin: {rel}")


def _route_of(proposal: dict[str, Any], retention_manifest: dict[str, Any],
              phase: str, disp: str) -> str:
    """Renderer route derives from valid publication labels, never a caller enum."""
    try:
        profile = proposal["publication_profile"]
    except (KeyError, TypeError) as exc:
        raise _fail("ROUTE_UNKNOWN", phase, disp, f"proposal lacks publication_profile: {exc}") from exc
    if profile == p1mod.LONGFORM_ROUTE:
        route = LONGFORM_ROUTE
    elif profile == p1mod.WEEKLY_ROUTE:
        route = WEEKLY_ROUTE
    else:
        raise _fail("ROUTE_UNKNOWN", phase, disp, f"unsupported publication_profile: {profile}")
    manifest_profile = ((retention_manifest.get("proposal_ref") or {}).get("publication_profile"))
    if manifest_profile != profile:
        raise _fail("ROUTE_MISMATCH", phase, disp,
                    "retention proposal_ref publication_profile differs from proposal")
    return route


def materialize_staged_source(root: str | Path, state_path: str | Path,
                              proposal_path: str | Path,
                              retention_manifest_path: str | Path,
                              scope_review_path: str | Path) -> dict[str, Any]:
    """One-shot current-scoped staged-source writer (no live writes)."""
    # Lazy P2V import: writer-only dependency, never in verifier closure.
    from scripts import survey_editorial_current_authority_v2 as observer  # noqa: PLC0415

    for name in _UNSAFE_GIT_VARS:
        if os.environ.get(name):
            raise _fail("GIT_ENV_REFUSED", "PIN", "REFUSED_PRE_WRITE",
                        f"inherited {name} refuses isolated materialization")
    session: Any = None
    live: Any = None
    owned: dict[str, Any] = {"staged_dir": None, "owned_files": [], "owned_dirs": [],
                             "observed_extra": [], "secondary_close_errors": []}
    phase = "PIN"
    disp = "REFUSED_PRE_WRITE"
    try:
        # W0: strict current root BEFORE any broad inventory.
        try:
            session = retention._Session(root)
        except Exception as exc:
            raise _fail("ROOT_UNSAFE", phase, disp,
                        f"repo root refused: {exc}", cause=exc) from exc
        root_path = session.root_resolved
        head_pinned = retention._git_head(root_path, "materialize HEAD pin", phase, disp)
        # Narrow pins: State/config/State-bound Profile, proposal, retention
        # manifest, scope review, schemas, style, every S2 file, P2V module.
        st_rel, st_data = session.safe_read(str(state_path), "Production State", phase, disp)
        try:
            state_obj = json.loads(st_data.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise _fail("STATE_UNREADABLE", phase, disp, f"pinned State not JSON: {exc}") from exc
        if not isinstance(state_obj, dict):
            raise _fail("STATE_UNREADABLE", phase, disp, "pinned State is not an object")
        prof_ref = state_obj.get("profile") or {}
        if not isinstance(prof_ref, dict) or set(prof_ref) != {"path", "sha256"}:
            raise _fail("STATE_PROFILE_SHAPE", phase, disp, "pinned State lacks exact profile ref")
        prof_rel, prof_data = session.safe_read(prof_ref["path"], "State-bound Profile", phase, disp)
        if core.sha256_bytes(prof_data) != prof_ref["sha256"]:
            raise _fail("PROFILE_DRIFT", phase, disp, "State-bound Profile bytes drifted")
        prop_rel, prop_data = session.safe_read(str(proposal_path),
                                                "editorial correction proposal", phase, disp)
        if prop_rel.split("/")[-1] != "proposal.json":
            raise _fail("PROPOSAL_FILENAME", phase, disp, "proposal file must be named proposal.json")
        man_rel, man_data = session.safe_read(str(retention_manifest_path),
                                              "retention manifest", phase, disp)
        if man_rel.split("/")[-1] != "retention-manifest.json":
            raise _fail("MANIFEST_FILENAME", phase, disp, "manifest file must be named retention-manifest.json")
        scope_rel, scope_data = session.safe_read(str(scope_review_path),
                                                  "scope review record", phase, disp)
        try:
            proposal_obj = json.loads(prop_data.decode("utf-8"))
            manifest_obj = json.loads(man_data.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise _fail("PIN_UNREADABLE", phase, disp, f"pinned proposal/manifest not JSON: {exc}") from exc
        for schema_rel in (PROPOSAL_SCHEMA.as_posix(), RETENTION_MANIFEST_SCHEMA.as_posix(),
                           STAGED_SCHEMA.as_posix(), REVIEW_SCHEMA.as_posix(), GATE_SCHEMA.as_posix(),
                           STYLE_PATH.as_posix(), STAGED_MODULE.as_posix(), P2V_MODULE.as_posix(),
                           core.DEFAULT_CONFIG.as_posix()):
            session.safe_read(schema_rel, "staged pin " + schema_rel, phase, disp)
        try:
            config_obj = json.loads(session.files[core.DEFAULT_CONFIG.as_posix()].decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise _fail("CONFIG_UNREADABLE", phase, disp,
                        f"pinned implementation config not JSON: {exc}") from exc
        if not isinstance(config_obj, dict):
            raise _fail("CONFIG_UNREADABLE", phase, disp, "pinned implementation config is not an object")
        orig_config_sha = core.sha256_bytes(session.files[core.DEFAULT_CONFIG.as_posix()])
        for schema_rel, payload, label in (
                (PROPOSAL_SCHEMA, proposal_obj, "editorial correction proposal"),
                (RETENTION_MANIFEST_SCHEMA, manifest_obj, "editorial retention manifest")):
            try:
                schema_gate.validate_instance(payload, root_path / schema_rel, label=label + " shape")
            except ValueError as exc:
                raise _fail("SCHEMA_INVALID", phase, disp, f"{label} schema invalid: {exc}") from exc
        try:
            # Staged schema file must itself be a valid JSON Schema (no instance to check yet).
            schema_gate.load_schema(root_path / STAGED_SCHEMA)
        except ValueError as exc:
            raise _fail("SCHEMA_INVALID", phase, disp, f"staged schema file invalid: {exc}") from exc
        session.safe_read(PROPOSAL_SCHEMA.as_posix(), "proposal schema recheck", phase, disp)
        session.safe_read(RETENTION_MANIFEST_SCHEMA.as_posix(), "retention schema recheck", phase, disp)
        route = _route_of(proposal_obj, manifest_obj, phase, disp)
        code_deps = _route_code_deps(route)
        dep_pins: dict[str, str] = {}
        dep_sizes: dict[str, int] = {}
        # Route schemas pinned per route: each file is checked AS a schema
        # (load_schema), never validated as a reader instance against itself.
        # The actual pinned reader is validated later via the canonicalizer.
        route_schemas = (LONGFORM_READER_SCHEMA, LONGFORM_RECEIPT_SCHEMA) \
            if route == LONGFORM_ROUTE else (WEEKLY_READER_SCHEMA, WEEKLY_RECEIPT_SCHEMA)
        for schema_rel in route_schemas:
            session.safe_read(schema_rel.as_posix(), "route schema pin", phase, disp)
        try:
            for schema_rel in route_schemas:
                schema_gate.load_schema(root_path / schema_rel)
        except ValueError as exc:
            raise _fail("SCHEMA_INVALID", phase, disp, f"route schema file invalid: {exc}") from exc
        for dep in code_deps:
            _rel, _data = session.safe_read(dep, "S2 dep pin", phase, disp)
            dep_pins[dep] = core.sha256_bytes(_data)
            dep_sizes[dep] = len(_data)
        _check_runtime_binding(root_path, dep_pins, phase, disp)
        orig_proposal_sha = core.sha256_bytes(prop_data)
        orig_manifest_sha = core.sha256_bytes(man_data)
        orig_state_sha = core.sha256_bytes(st_data)
        orig_scope_sha = core.sha256_bytes(scope_data)
        style_rel = STYLE_PATH.as_posix()
        style_bytes = session.files[style_rel]
        try:
            live = p1mod._Collector(root_path)
        except Exception as exc:
            raise _fail("PIN_FAILED", phase, disp,
                        f"live collector refused: {exc}", cause=exc) from exc
        try:
            sanitized = retention._sanitized_git_env()
            proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root_path,
                                  capture_output=True, text=True, env=sanitized, timeout=30)
        except (OSError, subprocess.SubprocessError) as exc:
            raise _fail("GIT_UNAVAILABLE", phase, disp, f"sanitized HEAD pin failed: {exc}") from exc
        if proc.returncode != 0 or proc.stdout.strip() != live.head or live.head != head_pinned:
            raise _fail("HEAD_MISMATCH", phase, disp, "collector/sanitized/pinned HEAD disagree")
        try:
            layout = p1mod._pin_proposal_layout(live, root_path, state_path, proposal_path)
        except Exception as exc:
            raise _fail("LAYOUT_REFUSED", phase, disp,
                        f"canonical proposal layout refused: {exc}", cause=exc) from exc
        if layout["proposal"] != proposal_obj:
            raise _fail("PROPOSAL_MISMATCH", phase, disp, "layout proposal differs from pinned proposal bytes")
        expected_dir = layout["expected_dir"]
        profile = layout["profile"]
        state = layout["state"]
        staged_authored = layout["staged_authored"]
        staged_reader = layout["staged_reader"]
        tree_entry = layout["tree_entry"]
        # Cross-check live vs retained ORIGINALs (no laundering), including
        # config: the separate live Collector's config never populates this
        # Session, so both sides are compared explicitly here.
        for rel, data in ((prop_rel, prop_data), (st_rel, st_data)):
            if live.files.get(rel) is None or core.sha256_bytes(live.files[rel]) != core.sha256_bytes(data):
                raise _fail("PIN_DRIFT", phase, disp, f"live vs retained bytes differ: {rel}")
        live_cfg_rel = core.DEFAULT_CONFIG.as_posix()
        if live.files.get(live_cfg_rel) is None or \
                core.sha256_bytes(live.files[live_cfg_rel]) != orig_config_sha:
            raise _fail("PIN_DRIFT", phase, disp, "live vs retained config bytes differ")
        try:
            source_root_rel = profile["paths"]["source_root"]
            survey_root_rel = profile["paths"]["survey_root"]
        except (KeyError, TypeError) as exc:
            raise _fail("PROFILE_ROOT_INVALID", phase, disp, f"profile roots invalid: {exc}") from exc
        staged_rel = expected_dir + "/" + STAGED_DIRNAME
        # W1: snapshots only AFTER canonical roots (never before). Config is
        # the PIN-phase pinned bytes (cross-checked vs live above), never a
        # second read that could move the basis.
        try:
            cfg = config_obj
            control_rels = retention._control_paths(cfg, phase, disp)
            ctrl_files, ctrl_dirs, ctrl_sizes = retention._snapshot_expanded(
                session, control_rels, "control", phase, disp)
            src_files, src_dirs, src_sizes = retention._snapshot_expanded(
                session, [source_root_rel, survey_root_rel], "edition", phase, disp)
            ret_rel = expected_dir + "/retained"
            ret_files, ret_dirs, ret_sizes = retention._retained_inventory(
                session, ret_rel, phase, disp)
            man_rows = manifest_obj.get("rows")
            if not isinstance(man_rows, list):
                raise _fail("RETENTION_MISMATCH", phase, disp, "retention manifest rows must be a list")
            exp_files_set, exp_dirs_set = retention._retained_expected_sets(
                man_rows, man_rel, ret_rel)
            if set(ret_files) != exp_files_set or set(ret_dirs) != exp_dirs_set:
                raise _fail("INVALID_RETENTION", phase, disp, "retained inventory != expected sets")
        except StagedSourceError:
            raise
        except Exception as exc:
            if isinstance(exc, retention.RetentionError):
                raise _fail("SNAPSHOT_FAILED", phase, disp,
                            f"snapshot failed: {exc}", cause=exc) from exc
            raise _fail("SNAPSHOT_FAILED", phase, disp, f"snapshot failed: {exc}", cause=exc) from exc
        init_triple = ((dict(ctrl_files), dict(ctrl_dirs), dict(ctrl_sizes)),
                       (dict(src_files), dict(src_dirs), dict(src_sizes)),
                       (dict(ret_files), dict(ret_dirs), dict(ret_sizes)))
        init_ctrl, init_src, init_ret = init_triple
        init_tree = dict(tree_entry)
        orig_live_map = dict(live.files)
        orig_ret_map = dict(session.files)
        # Pre-claim boundary: original pins/HEAD + full inventories with
        # ZERO admitted delta (W2 P2V + W3 render are read-only, so any
        # drift refuses before the root is claimed).
        _recheck_consumed_pins(live, session, orig_live_map, orig_ret_map,
                               head_pinned, root_path, "PRE_WRITE", "REFUSED_PRE_WRITE", None)
        _compare_original_boundary(init_triple, session, control_rels, source_root_rel,
                                   survey_root_rel, ret_rel, set(), set(),
                                   "PRE_WRITE", "REFUSED_PRE_WRITE", None)
        # Staged root must be absent (any entry incl. byte-equal refuses).
        try:
            os.lstat(root_path / staged_rel)
            raise _fail("STAGED_ROOT_EXISTS", phase, disp,
                        f"staged root already present (no overwrite/takeover): {staged_rel}")
        except FileNotFoundError:
            pass
        except StagedSourceError:
            raise
        except OSError as exc:
            raise _fail("PATH_UNREADABLE", phase, disp,
                        f"staged root unreadable: {staged_rel}: {exc}") from exc
        # W2: fresh in-call P2V with scope; SCOPE_BOUND required.
        phase = "OBSERVE"
        with retention._sanitized_git_env_ctx():
            try:
                observed = observer.observe_current_authority(
                    root_path, state_path, proposal_path, retention_manifest_path, scope_review_path)
            except Exception as exc:
                raise _fail("OBSERVER_REFUSED", phase, disp,
                            f"fresh current-authority observation refused: {exc}", cause=exc) from exc
        if not isinstance(observed, dict) or observed.get("result") != observer.RESULT_SCOPE_BOUND:
            raise _fail("OBSERVER_NOT_BOUND", phase, disp, "fresh P2V did not return SCOPE_BOUND")
        for key, orig_rel, orig_sha in (("state_ref", st_rel, orig_state_sha),
                                        ("proposal_ref", prop_rel, orig_proposal_sha),
                                        ("retention_manifest_ref", man_rel, orig_manifest_sha),
                                        ("scope_review_ref", scope_rel, orig_scope_sha)):
            ref = observed.get(key)
            if not isinstance(ref, dict) or ref.get("sha256") != orig_sha or \
                    ref.get("path") != orig_rel:
                raise _fail("OBSERVER_MISMATCH", phase, disp,
                            f"fresh P2V {key} path/SHA differs from original pin")
        # Bind every dynamically discovered P2V pin to the original basis (R2-5):
        # overlaps must be byte-identical AND any newly discovered consumed path
        # (not in either original map) refuses — it is a new consumed input that
        # was not pinned at the original boundary, never silently ignored.
        for rel, sha in (observed.get("input_hashes") or {}).items():
            if rel in orig_ret_map:
                if core.sha256_bytes(orig_ret_map[rel]) != sha:
                    raise _fail("OBSERVER_MISMATCH", phase, disp,
                                f"fresh P2V retained pin differs from original: {rel}")
            elif rel in orig_live_map:
                if core.sha256_bytes(orig_live_map[rel]) != sha:
                    raise _fail("OBSERVER_MISMATCH", phase, disp,
                                f"fresh P2V live pin differs from original: {rel}")
            else:
                raise _fail("OBSERVER_NEW_PIN", phase, disp,
                            f"fresh P2V discovered new consumed path not in original pins: {rel}")
        obs_measured = observed.get("measured") or {}
        if obs_measured.get("before_graph_digest") != (proposal_obj.get("basis") or {}).get("before_graph_digest"):
            raise _fail("OBSERVER_MISMATCH", phase, disp, "fresh P2V before digest differs from proposal basis")
        if obs_measured.get("preserved_upstream_digest") != \
                (proposal_obj.get("basis") or {}).get("preserved_upstream_digest"):
            raise _fail("OBSERVER_MISMATCH", phase, disp, "fresh P2V upstream digest differs from proposal basis")
        # W3 (decided): pinned staged reader + P2V digest + canonicalizer +
        # actual renderers. No redundant private _pipeline_data, no public P1.
        phase = "PRE_WRITE"
        disp = "REFUSED_PRE_WRITE"
        reader_ref = (proposal_obj.get("proposed") or {}).get("proposed_reader_ref") or {}
        canon_sha = (proposal_obj.get("proposed") or {}).get("proposed_reader_canonical_sha256")
        if reader_ref.get("sha256") != canon_sha:
            raise _fail("PROPOSED_DIGEST_MISMATCH", phase, disp, "proposal reader ref != canonical sha")
        # Distinct immutable names: the output directory (staged_rel) and the
        # existing reader FILE (staged_reader_rel) must never share a variable;
        # overwriting the directory with the file path corrupts every later
        # manifest/claim/output path.
        try:
            staged_reader_rel = live.rel(staged_reader)
        except Exception as exc:
            raise _fail("PIN_FAILED", phase, disp, f"staged reader rel failed: {exc}") from exc
        pinned_staged = live.files.get(staged_reader_rel)
        try:
            live_staged_now = staged_reader.read_bytes()
        except OSError as exc:
            raise _fail("PATH_UNREADABLE", phase, disp, f"staged reader unreadable: {exc}") from exc
        if pinned_staged is None or live_staged_now != pinned_staged:
            raise _fail("STABILITY_VIOLATION", phase, disp, "staged reader changed mid-inspection")
        _rr, reader_bytes_ret = session.safe_read(reader_ref.get("path", ""),
                                                  "staged proposed reader", phase, disp)
        if core.sha256_bytes(reader_bytes_ret) != canon_sha or \
                core.sha256_bytes(live_staged_now) != canon_sha:
            raise _fail("PROPOSED_DIGEST_MISMATCH", phase, disp, "staged reader != canonical digest")
        if obs_measured.get("proposed_reader_sha256") != canon_sha:
            raise _fail("OBSERVER_MISMATCH", phase, disp, "fresh P2V proposed digest != canonical digest")
        try:
            reader_text = live_staged_now.decode("utf-8")
            reader_obj = json.loads(reader_text)
        except (UnicodeDecodeError, ValueError) as exc:
            raise _fail("READER_UNREADABLE", phase, disp, f"staged reader not JSON: {exc}") from exc
        try:
            if route == LONGFORM_ROUTE:
                reviewed = longform_derivation.validate_longform_reader_input(root_path, reader_obj)
                if live_staged_now != longform_derivation.canonical_reader_bytes(reviewed):
                    raise _fail("READER_NONCANONICAL", phase, disp,
                                "staged reader FILE bytes != canonical rederived bytes")
                main_text = longform_generated.render_main(reviewed)
                bib_text = longform_generated.render_bibliography(reviewed)
                longform_generated.validate_heading_syntax(reviewed)
                longform_generated.validate_generated_closure(main_text, style_bytes.decode("utf-8"))
            else:
                reviewed = weekly.validate_reader_input(root_path, reader_obj)
                main_text = weekly.render_main(reviewed)
                bib_text = weekly.render_bibliography(reviewed)
                weekly.validate_generated_closure(main_text, style_bytes.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            raise _fail("RENDER_REFUSED", phase, disp, f"renderer/closure refused: {exc}") from exc
        main_bytes = main_text.encode("utf-8")
        bib_bytes = bib_text.encode("utf-8")
        expected_outputs = {"main": (MAIN_FILENAME, main_bytes),
                            "bibliography": (BIBLIOGRAPHY_FILENAME, bib_bytes),
                            "style": (STYLE_FILENAME, style_bytes)}
        # Preflight all 4 prospective outputs + schema bytes + closed inventory.
        manifest_pre: dict[str, Any] = {
            "schema_version": "2.0-rc1",
            "kind": "EDITORIAL_STAGED_SOURCE_V1",
            "status": "STAGED_ONLY",
            "proposal_ref": {"path": prop_rel, "sha256": orig_proposal_sha,
                             "proposal_id": proposal_obj["proposal_id"],
                             "issue_id": proposal_obj["issue_id"],
                             "research_profile": proposal_obj["research_profile"],
                             "publication_profile": proposal_obj["publication_profile"]},
            "retention_manifest_ref": {"path": man_rel, "sha256": orig_manifest_sha},
            "scope_review_ref": {"path": scope_rel, "sha256": orig_scope_sha},
            "issue_id": proposal_obj["issue_id"],
            "research_profile": proposal_obj["research_profile"],
            "publication_profile": proposal_obj["publication_profile"],
            "route": route,
            "basis": proposal_obj["basis"],
            "proposed": proposal_obj["proposed"],
            "outputs": {role: {"path": staged_rel + "/" + name,
                                "sha256": core.sha256_bytes(data),
                                "byte_count": len(data)}
                        for role, (name, data) in expected_outputs.items()},
            "style_input_ref": {"path": style_rel, "sha256": core.sha256_bytes(style_bytes),
                                "byte_count": len(style_bytes)},
            "code_deps": [{"path": dep, "sha256": dep_pins[dep], "byte_count": dep_sizes[dep]}
                          for dep in code_deps],
            "producer_head": head_pinned,
        }
        manifest_pre["manifest_digest"] = _manifest_digest(manifest_pre)
        try:
            schema_gate.validate_instance(manifest_pre, root_path / STAGED_SCHEMA,
                                          label="staged source manifest preflight")
        except ValueError as exc:
            raise _fail("SCHEMA_INVALID", phase, disp, f"projected staged manifest invalid: {exc}") from exc
        if manifest_pre["basis"] != proposal_obj["basis"]:
            raise _fail("BASIS_MISMATCH", phase, disp, "projected basis != proposal basis")
        if manifest_pre["proposed"] != proposal_obj["proposed"]:
            raise _fail("PROPOSED_MISMATCH", phase, disp, "projected proposed != proposal proposed")
        if [d["path"] for d in manifest_pre["code_deps"]] != list(code_deps):
            raise _fail("CODE_DEPS_MISMATCH", phase, disp, "projected code_deps != fixed sorted S2 set")
        _check_contract_identity(manifest_pre["basis"].get("contract_identity"), phase, disp)
        manifest_bytes = _canonical_json_bytes(manifest_pre)
        if not manifest_bytes:
            raise _fail("MANIFEST_EMPTY", phase, disp, "projected manifest bytes empty")
        # R2-5: intended actual preclaim boundary AFTER rendering/preflight,
        # immediately before mkdir. The earlier PRE_WRITE check ran before the
        # first P2V/render; this rechecks every original pin/HEAD plus full
        # inventories with ZERO admitted delta after all later reads (render,
        # preflight, digest). A drift after render/before claim refuses here,
        # not at the earlier boundary. First HEAD comparison before writes is
        # this boundary (plus the earlier one), never after mkdir.
        _recheck_consumed_pins(live, session, orig_live_map, orig_ret_map,
                               head_pinned, root_path, "PRE_CLAIM", "REFUSED_PRE_WRITE", None)
        _compare_original_boundary(init_triple, session, control_rels, source_root_rel,
                                   survey_root_rel, ret_rel, set(), set(),
                                   "PRE_CLAIM", "REFUSED_PRE_WRITE", None)
        # Re-verify the staged root is still absent immediately before claim.
        try:
            os.lstat(root_path / staged_rel)
            raise _fail("STAGED_ROOT_EXISTS", phase, disp,
                        f"staged root appeared before claim: {staged_rel}")
        except FileNotFoundError:
            pass
        except StagedSourceError:
            raise
        except OSError as exc:
            raise _fail("PATH_UNREADABLE", phase, disp,
                        f"staged root unreadable before claim: {exc}") from exc
        # W4 CLAIM: exclusive dirfd mkdir + entry/fd identity; then files.
        phase = "CLAIM"
        disp = "OWNED_PARTIAL"
        owned["staged_dir"] = staged_rel
        parent_fd: int | None = None
        staged_fd: int | None = None
        # Observation-window qualification (R2-6): between exclusive mkdir and
        # the earliest entry stat + open+fstat+entry bind below, a concurrent
        # rename cannot be fully excluded (no global exclusion or race-free
        # mkdir identity acquisition is claimed). The window is narrowed to
        # three syscalls by stating the earliest entry immediately after mkdir
        # and opening immediately; any replacement AFTER the earliest stat is
        # detected by the entry-vs-fd bind before any file write. A replacement
        # strictly between mkdir and the earliest stat remains an explicitly
        # qualified blind window, not a detected case.
        owned["observed_extra"].append({"path": staged_rel, "note": "mkdir attempted"})
        try:
            prop_parts = staged_rel.split("/")[:-1]
            # _open_dir_chain tracks every opened ancestor fd in
            # session._open_fds for checked close; never append twice here.
            parent_fd = session._open_dir_chain(prop_parts, "staged parent", phase, disp) \
                if prop_parts else session.root_fd
            try:
                os.mkdir(STAGED_DIRNAME, dir_fd=parent_fd)
            except FileExistsError as exc:
                raise _fail("STAGED_ROOT_EXISTS", phase, disp,
                            f"staged root raced into existence: {staged_rel}", owned) from exc
            except OSError as exc:
                raise _fail("STAGED_ROOT_CREATE_FAILED", phase, disp,
                            f"staged root mkdir failed: {staged_rel}: {exc}", owned) from exc
            # Earliest entry stat immediately after mkdir (R2-6): the first
            # observable identity of the directory created by mkdir. Compared
            # below against both the opened fd and a re-read entry.
            try:
                earliest = session._entry_identity(parent_fd, STAGED_DIRNAME, "staged root earliest",
                                                   phase, disp)
            except Exception as exc:
                # Identity unknown: preserve the attempt, refuse before writes.
                owned["observed_extra"].append({"path": staged_rel,
                                                "note": f"earliest entry unknown: {exc}"})
                raise _fail("STAGED_ROOT_IDENTITY_FAILED", phase, disp,
                            f"staged root earliest entry identity failed: {exc}", owned) from exc
            try:
                staged_fd = os.open(STAGED_DIRNAME, os.O_RDONLY | os.O_DIRECTORY |
                                    getattr(os, "O_NOFOLLOW", 0), dir_fd=parent_fd)
            except OSError as exc:
                raise _fail("STAGED_ROOT_OPEN_FAILED", phase, disp,
                            f"staged root open failed: {staged_rel}: {exc}", owned) from exc
            session._open_fds.append(staged_fd)
            try:
                st = os.fstat(staged_fd)
            except OSError as exc:
                owned["observed_extra"].append({"path": staged_rel, "note": "fstat failed, identity unknown"})
                raise _fail("STAGED_ROOT_FSTAT_FAILED", phase, disp,
                            f"staged root fstat failed before any write: {staged_rel}: {exc}",
                            owned) from exc
            if not _stat.S_ISDIR(st.st_mode):
                raise _fail("STAGED_ROOT_NOT_DIR", phase, disp,
                            f"claimed staged root is not a directory: {staged_rel}", owned)
            try:
                ent = session._entry_identity(parent_fd, STAGED_DIRNAME, "staged root", phase, disp)
            except Exception as exc:
                raise _fail("STAGED_ROOT_IDENTITY_FAILED", phase, disp,
                            f"staged root entry identity failed: {exc}", owned) from exc
            # All three must agree: earliest post-mkdir entry, opened fd fstat,
            # and current entry. A mkdir->open replacement that swaps the entry
            # after the earliest stat is detected here; a swap strictly between
            # mkdir and the earliest stat is the qualified blind window above.
            if (st.st_dev, st.st_ino) != (ent[0], ent[1]) or \
               (st.st_dev, st.st_ino) != (earliest[0], earliest[1]):
                raise _fail("STAGED_ROOT_REPLACED", phase, disp,
                            f"staged root replaced between mkdir and open: {staged_rel}", owned)
            owned["owned_dirs"].append({"path": staged_rel, "dev": st.st_dev, "ino": st.st_ino})
            owned["staged_identity"] = (st.st_dev, st.st_ino)
            owned["observed_extra"].append({"path": staged_rel,
                                             "note": f"earliest entry dev={earliest[0]} ino={earliest[1]}"})
        except StagedSourceError:
            raise
        except Exception as exc:
            if isinstance(exc, retention.RetentionError):
                raise _fail("CLAIM_FAILED", phase, disp,
                            f"staged root claim failed: {exc}", owned, cause=exc) from exc
            raise _fail("CLAIM_FAILED", phase, disp,
                        f"staged root claim failed: {exc}", owned, cause=exc) from exc
        # W4 files + W5 manifest LAST (all exclusive, fstat-bound, read back).
        try:
            _emit_outputs(session, staged_fd, staged_rel, expected_outputs, owned, phase, disp,
                          manifest_name=None, manifest_bytes=None)
        except StagedSourceError:
            raise
        # Pre-manifest boundary: original pins/HEAD + full inventories with
        # EXACTLY the three admitted source outputs (no manifest yet) as the
        # only allowed edition delta.
        phase = "MANIFEST"
        disp = "INDETERMINATE_INVOCATION"
        _recheck_consumed_pins(live, session, orig_live_map, orig_ret_map,
                               head_pinned, root_path, phase, disp, owned)
        _compare_original_boundary(init_triple, session, control_rels, source_root_rel,
                                   survey_root_rel, ret_rel,
                                   {staged_rel + "/" + name for _role, (name, _data)
                                    in expected_outputs.items()},
                                   {staged_rel}, phase, disp, owned)
        try:
            _emit_outputs(session, staged_fd, staged_rel, {}, owned, phase, disp,
                          manifest_name=MANIFEST_FILENAME, manifest_bytes=manifest_bytes)
        except StagedSourceError:
            raise
        _verify_outputs_and_manifest(session, staged_rel, expected_outputs, manifest_bytes, phase, disp)
        owned_identities = {entry["path"]: (entry["dev"], entry["ino"]) for entry in owned["owned_files"]}
        # W6: standalone replay in this module, then second fresh P2V.
        phase = "REPLAY"
        disp = "INDETERMINATE_INVOCATION"
        try:
            replayed = verify_staged_source(root_path, proposal_path, staged_rel + "/" + MANIFEST_FILENAME)
        except Exception as exc:
            raise _fail("REPLAY_UNVERIFIED", phase, disp,
                        f"standalone staged replay refused: {exc}", owned, cause=exc) from exc
        if not isinstance(replayed, dict) or replayed.get("result") != RESULT_VERIFIED:
            raise _fail("REPLAY_UNVERIFIED", phase, disp, "standalone staged replay did not verify", owned)
        if replayed.get("staged_manifest_ref", {}).get("sha256") != core.sha256_bytes(manifest_bytes):
            raise _fail("REPLAY_MISMATCH", phase, disp, "replay manifest ref != original manifest bytes", owned)
        phase = "OBSERVE"
        with retention._sanitized_git_env_ctx():
            try:
                observed2 = observer.observe_current_authority(
                    root_path, state_path, proposal_path, retention_manifest_path, scope_review_path)
            except Exception as exc:
                raise _fail("OBSERVER2_REFUSED", phase, disp,
                            f"second fresh observation refused: {exc}", owned, cause=exc) from exc
        if not isinstance(observed2, dict) or observed2.get("result") != observer.RESULT_SCOPE_BOUND:
            raise _fail("OBSERVER2_NOT_BOUND", phase, disp, "second P2V did not return SCOPE_BOUND", owned)
        # Explicit normalized ref + stable-fact compare: paths AND SHAs must
        # equal the ORIGINAL pins, and the second observation must agree with
        # the FIRST observation (no whole input-map equality either way).
        for key, orig_rel, orig_sha in (("state_ref", st_rel, orig_state_sha),
                                        ("proposal_ref", prop_rel, orig_proposal_sha),
                                        ("retention_manifest_ref", man_rel, orig_manifest_sha),
                                        ("scope_review_ref", scope_rel, orig_scope_sha)):
            ref = observed2.get(key)
            first = (observed.get(key) or {}) if isinstance(observed, dict) else {}
            if not isinstance(ref, dict) or ref.get("sha256") != orig_sha or \
                    ref.get("path") != orig_rel:
                raise _fail("OBSERVER2_MISMATCH", phase, disp,
                            f"second P2V {key} path/SHA differs from original pin", owned)
            if not isinstance(first, dict) or ref.get("sha256") != first.get("sha256") or \
                    ref.get("path") != first.get("path"):
                raise _fail("OBSERVER2_MISMATCH", phase, disp,
                            f"second P2V {key} differs from first observation", owned)
        obs2_measured = observed2.get("measured") or {}
        obs_measured = (observed.get("measured") or {}) if isinstance(observed, dict) else {}
        if obs2_measured.get("before_graph_digest") != (proposal_obj.get("basis") or {}).get("before_graph_digest"):
            raise _fail("OBSERVER2_MISMATCH", phase, disp,
                        "second P2V before digest differs from original basis", owned)
        if obs2_measured.get("preserved_upstream_digest") != \
                (proposal_obj.get("basis") or {}).get("preserved_upstream_digest"):
            raise _fail("OBSERVER2_MISMATCH", phase, disp,
                        "second P2V upstream digest differs from original basis", owned)
        if obs2_measured.get("proposed_reader_sha256") != canon_sha or \
                obs2_measured.get("proposed_reader_sha256") != obs_measured.get("proposed_reader_sha256"):
            raise _fail("OBSERVER2_MISMATCH", phase, disp,
                        "second P2V proposed digest differs from original/first basis", owned)
        if observed2.get("observed_head") != head_pinned or \
                observed.get("observed_head") != head_pinned:
            raise _fail("HEAD_MOVED", phase, disp, "first/second P2V HEAD != original pin", owned)
        # R2-5: second-observation input-map check. Newly materialized files
        # legitimately appear in the second observation; never demand full-map
        # equality to the first observation and never rebaseline changed output
        # bytes. Exactly the 4 owned staged files may be new; every other new
        # path refuses, and every overlapping pin must stay byte-identical.
        allowed_second_new = {staged_rel + "/" + name for _role, (name, _data)
                              in list(expected_outputs.items()) + [("manifest", (MANIFEST_FILENAME, manifest_bytes))]}
        for rel, sha in (observed2.get("input_hashes") or {}).items():
            if rel in allowed_second_new:
                # Must equal the ORIGINAL expected output bytes, not a
                # rebaselined second-session read.
                want_data = None
                for _role, (name, data) in list(expected_outputs.items()) + \
                        [("manifest", (MANIFEST_FILENAME, manifest_bytes))]:
                    if staged_rel + "/" + name == rel:
                        want_data = data
                        break
                if want_data is None or core.sha256_bytes(want_data) != sha:
                    raise _fail("OBSERVER2_MISMATCH", phase, disp,
                                f"second P2V staged pin != original expected bytes: {rel}", owned)
            elif rel in orig_ret_map:
                if core.sha256_bytes(orig_ret_map[rel]) != sha:
                    raise _fail("OBSERVER2_MISMATCH", phase, disp,
                                f"second P2V retained pin differs from original: {rel}", owned)
            elif rel in orig_live_map:
                if core.sha256_bytes(orig_live_map[rel]) != sha:
                    raise _fail("OBSERVER2_MISMATCH", phase, disp,
                                f"second P2V live pin differs from original: {rel}", owned)
            else:
                raise _fail("OBSERVER2_NEW_PIN", phase, disp,
                            f"second P2V discovered unexpected new path: {rel}", owned)
        # W7 FINAL: original inputs/outputs + exact inventories AFTER later
        # helpers, compared to ORIGINAL expected values (never rebaselined).
        phase = "FINAL"
        disp = "INDETERMINATE_INVOCATION"
        if retention._git_head(root_path, "materialize HEAD final", phase, disp) != head_pinned:
            raise _fail("HEAD_MOVED", phase, disp, "HEAD changed by final boundary", owned)
        if live.head != head_pinned:
            raise _fail("HEAD_MOVED", phase, disp, "collector HEAD changed by final boundary", owned)
        # R2-6: original root/entry check at FINAL. Held root fd fstat must
        # still match the canonical repo-root entry (a rename-away keeps the
        # held fd unchanged but moves the entry). Ancestor alias walk is
        # covered by _open_dir_chain below; this pins the root itself.
        try:
            _root_fd_stat = os.fstat(session.root_fd)
            _root_entry = os.lstat(session.root_resolved)
        except OSError as exc:
            raise _fail("ROOT_UNSAFE", phase, disp,
                        f"final root entry unreadable: {exc}", owned) from exc
        if (_root_fd_stat.st_dev, _root_fd_stat.st_ino) != (_root_entry.st_dev, _root_entry.st_ino):
            raise _fail("STAGED_ROOT_REPLACED", phase, disp,
                        "final repo-root entry != held root fd (root replaced)", owned)
        if _stat.S_ISLNK(_root_entry.st_mode):
            raise _fail("ROOT_UNSAFE", phase, disp, "final repo-root is a symlink", owned)
        try:
            # Full original-boundary compare: control + retained must show ZERO
            # delta; edition must show EXACTLY the owned 4-file staged set.
            # Session.reverify alone cannot see planted files/empty dirs, so
            # full inventories (incl. empty dirs) are rewalked here.
            want_files = {staged_rel + "/" + name for _role, (name, _data)
                          in list(expected_outputs.items()) + [("manifest", (MANIFEST_FILENAME, manifest_bytes))]}
            _compare_original_boundary(init_triple, session, control_rels, source_root_rel,
                                       survey_root_rel, ret_rel, want_files, {staged_rel},
                                       phase, disp, owned)
            # Owned-delta tree comparison (R2-1): the edition file map must equal
            # ORIGINAL tree plus exactly the 4 owned staged outputs. Never
            # whole-map equality against the pre-claim snapshot (which would
            # guarantee rejection of every correct materialization).
            expected_tree = dict(init_tree)
            for _role, (name, data) in list(expected_outputs.items()) + \
                    [("manifest", (MANIFEST_FILENAME, manifest_bytes))]:
                expected_tree[staged_rel + "/" + name] = core.sha256_bytes(data)
            try:
                cur_tree = p1mod._tree_map(root_path, Path(source_root_rel), Path(survey_root_rel))
            except Exception as exc:
                raise _fail("TREE_UNREADABLE", phase, disp,
                            f"edition tree unreadable at final boundary: {exc}", owned) from exc
            if cur_tree != expected_tree:
                extra = sorted(set(cur_tree) - set(expected_tree))
                missing = sorted(set(expected_tree) - set(cur_tree))
                changed = sorted(k for k in set(cur_tree) & set(expected_tree)
                                 if cur_tree[k] != expected_tree[k])
                raise _fail("TREE_MOVED", phase, disp,
                            f"edition tree != original+owned 4-file delta "
                            f"(extra={extra[:8]} missing={missing[:8]} changed={changed[:8]})", owned)
            fin_files, fin_dirs, fin_sizes = retention._snapshot_expanded(
                session, [staged_rel], "staged final", phase, disp)
            if set(fin_files) != want_files or set(fin_dirs) != {staged_rel}:
                raise _fail("STAGED_DRIFT", phase, disp, "final staged inventory != exact 4-file closure", owned)
            for _role, (name, data) in list(expected_outputs.items()) + \
                    [("manifest", (MANIFEST_FILENAME, manifest_bytes))]:
                if fin_files.get(staged_rel + "/" + name) != core.sha256_bytes(data) or \
                        fin_sizes.get(staged_rel + "/" + name) != len(data):
                    raise _fail("OUTPUT_DRIFT", phase, disp, f"final staged bytes moved: {name}", owned)
            # Same-inode in-place edit detection for ALL FOUR owned files
            # (no manifest exemption): entry identity must still be the owned
            # identity AND bytes must equal ORIGINAL expected bytes.
            prop_parts = staged_rel.split("/")[:-1]
            check_parent = session._open_dir_chain(prop_parts, "staged final parent", phase, disp) \
                if prop_parts else session.root_fd
            try:
                check_staged = os.open(STAGED_DIRNAME, os.O_RDONLY | os.O_DIRECTORY |
                                       getattr(os, "O_NOFOLLOW", 0), dir_fd=check_parent)
            except OSError as exc:
                raise _fail("STAGED_ROOT_REOPEN_FAILED", phase, disp,
                            f"final staged reopen failed: {exc}", owned) from exc
            session._open_fds.append(check_staged)
            # R2-7: any primary (StagedSourceError OR RetentionError from
            # _entry_identity) must survive a secondary close failure. Unknown
            # identity/failed-close descriptor state is recorded explicitly;
            # the descriptor is closed exactly once (no blind retry on a
            # possibly reused fd number).
            body_error: BaseException | None = None
            try:
                for _role, (name, data) in list(expected_outputs.items()) + \
                        [("manifest", (MANIFEST_FILENAME, manifest_bytes))]:
                    try:
                        ent = session._entry_identity(check_staged, name, "final " + name, phase, disp)
                    except Exception as exc:
                        # Identity unknown: preserve attempt, refuse (R2-7).
                        raise _fail("FILE_IDENTITY_UNKNOWN", phase, disp,
                                    f"staged file identity unreadable at final: {name}: {exc}",
                                    owned, cause=exc) from exc
                    key = staged_rel + "/" + name
                    if (ent[0], ent[1]) != owned_identities.get(key):
                        raise _fail("FILE_REPLACED", phase, disp,
                                    f"staged file identity changed after self-readback: {name}", owned)
            except BaseException as exc:
                body_error = exc
                raise
            finally:
                try:
                    os.close(check_staged)
                except OSError as exc:
                    owned.setdefault("secondary_close_errors", []).append(
                        f"final-staged-dir-close: {exc}")
                    if body_error is not None:
                        if isinstance(body_error, StagedSourceError):
                            _attach_close(body_error, exc)
                        # Non-StagedSourceError primaries (e.g. RetentionError
                        # wrapped above is already StagedSourceError; any other
                        # unexpected primary propagates with secondary recorded
                        # above, never masked by a fresh CLOSE_FAILED).
                    else:
                        raise _fail("CLOSE_FAILED", phase, disp,
                                    f"final staged dir close failed: {exc}", owned) from exc
                finally:
                    if check_staged in session._open_fds:
                        session._open_fds.remove(check_staged)
            if retention._git_head(root_path, "materialize HEAD final2", phase, disp) != head_pinned:
                raise _fail("HEAD_MOVED", phase, disp, "HEAD changed at final close", owned)
            for rel, orig_bytes in orig_ret_map.items():
                cur = session.files.get(rel)
                if cur is None or cur != orig_bytes:
                    raise _fail("PIN_DRIFT", phase, disp,
                                f"retained pin changed after later reads: {rel}", owned)
            for rel, orig_bytes in orig_live_map.items():
                cur = live.files.get(rel)
                if cur is None or cur != orig_bytes:
                    raise _fail("PIN_DRIFT", phase, disp,
                                f"live pin changed after later reads: {rel}", owned)
            live.reverify()
            session.reverify(phase, disp)
        except StagedSourceError:
            raise
        except Exception as exc:
            if isinstance(exc, retention.RetentionError):
                raise _fail("FINAL_FAILED", phase, disp, f"final boundary failed: {exc}", owned,
                            cause=exc) from exc
            raise _fail("FINAL_FAILED", phase, disp, f"final boundary failed: {exc}", owned,
                        cause=exc) from exc
        # Final close with complete valid bytes: a close failure here is
        # INDETERMINATE (not a labelled success, diagnostics preserved).
        try:
            _close_session(session, "CLOSE", "CLOSED")
        except StagedSourceError as exc:
            raise _fail("INDETERMINATE_INVOCATION", "CLOSE", "INDETERMINATE_INVOCATION",
                        f"final close failed with complete valid bytes: {exc.detail}",
                        owned, cause=exc) from exc
        session = None
        return {
            "result": RESULT_MATERIALIZED,
            "proposal_ref": {"path": prop_rel, "sha256": orig_proposal_sha},
            "retention_manifest_ref": {"path": man_rel, "sha256": orig_manifest_sha},
            "scope_review_ref": {"path": scope_rel, "sha256": orig_scope_sha},
            "staged_manifest_ref": {"path": staged_rel + "/" + MANIFEST_FILENAME,
                                    "sha256": core.sha256_bytes(manifest_bytes)},
            "outputs": {role: {"path": staged_rel + "/" + name,
                                "sha256": core.sha256_bytes(data), "byte_count": len(data)}
                        for role, (name, data) in expected_outputs.items()},
            "style_input_ref": {"path": style_rel, "sha256": core.sha256_bytes(style_bytes),
                                "byte_count": len(style_bytes)},
            "code_deps": [{"path": dep, "sha256": dep_pins[dep], "byte_count": dep_sizes[dep]}
                          for dep in code_deps],
            "observed_head": head_pinned,
            "measured": {
                "before_graph_digest": (proposal_obj.get("basis") or {}).get("before_graph_digest"),
                "preserved_upstream_digest": (proposal_obj.get("basis") or {}).get("preserved_upstream_digest"),
                "proposed_reader_sha256": canon_sha,
                "copy_files": (observed.get("measured") or {}).get("copy_files"),
                "keep_refs": (observed.get("measured") or {}).get("keep_refs"),
                "stable_p2v": {
                    "before": obs2_measured.get("before_graph_digest"),
                    "upstream": obs2_measured.get("preserved_upstream_digest"),
                    "proposed_reader": obs2_measured.get("proposed_reader_sha256"),
                    "head_first": observed.get("observed_head"),
                    "head_second": observed2.get("observed_head"),
                },
            },
            "manifest_digest": manifest_pre["manifest_digest"],
        }
    except StagedSourceError as primary:
        if session is not None:
            _close_session(session, primary.phase, primary.disposition, primary)
            session = None
        raise
    except Exception as exc:
        wrapped = _fail("WRITER_FAILED", phase, disp, f"unexpected writer failure: {exc}",
                        owned, cause=exc)
        if session is not None:
            _close_session(session, phase, disp, wrapped)
            session = None
        raise wrapped from exc


def _write_owned_file(session: Any, staged_fd: int, staged_rel: str, leaf: str,
                      data: bytes, owned: dict[str, Any], phase: str, disp: str,
                      dir_identity: tuple[int, int] | None = None) -> None:
    """Exclusive no-follow create + fstat identity BEFORE any byte is written.

    Attempt is recorded before open; identity once obtained; progress, byte
    counts, fsync/close/readback state after each step. Durability seam:
    ``os.fsync`` before close (no crash-atomicity/power-loss claim — a
    failure reports INDETERMINATE because complete bytes may already exist).
    A close/fsync failure never masks an in-flight write error: the first
    error stays primary and later close failures attach as secondary.
    R2-6: held-fd fstat alone cannot prove entry identity (a renamed dir keeps
    the same fd). Before EACH file creation both the held fd AND the canonical
    entry (lstat of the staged path plus ancestor alias walk) are compared to
    the earliest owned identity.
    R2-7: every secondary close failure is recorded, never silently discarded;
    failed-close descriptor state is explicit and never blindly retried on a
    possibly reused fd number.
    R2-3: ``bytes_written`` advances after every successful chunk so partial
    progress survives a later failure.
    """
    full = staged_rel + "/" + leaf
    entry: dict[str, Any] = {"path": full, "attempted": True, "dev": "unknown", "ino": "unknown",
                             "sha256": core.sha256_bytes(data), "byte_count": len(data),
                             "bytes_written": 0, "fsync": "pending", "close": "pending",
                             "readback": "pending"}
    owned["owned_files"].append(entry)
    if dir_identity is not None:
        # Held-root check before each write (R2-6, part 1).
        try:
            dst = os.fstat(staged_fd)
        except OSError as exc:
            entry["error"] = f"held root fstat failed: {exc}"
            raise _fail("STAGED_ROOT_FSTAT_FAILED", phase, disp,
                        f"held staged root fstat failed before writing {leaf}: {exc}", owned) from exc
        if (dst.st_dev, dst.st_ino) != dir_identity:
            entry["error"] = "held root identity changed"
            raise _fail("STAGED_ROOT_REPLACED", phase, disp,
                        f"held staged root replaced before writing {leaf}", owned)
        # Canonical entry check before each write (R2-6, part 2): reopen the
        # canonical staged path from the repo root and compare to the earliest
        # owned identity. A rename-away keeps the held fd unchanged but moves
        # or replaces the canonical entry, which this detects. Ancestor
        # components are lstat-checked for alias (no follow) before the leaf.
        try:
            root_resolved = session.root_resolved
            # Ancestor alias walk (lexical, no resolve): every component of
            # staged_rel must be a real dir, never a symlink.
            parts = staged_rel.split("/")
            cur = root_resolved
            for i, comp in enumerate(parts):
                if comp in ("", ".", ".."):
                    raise OSError(f"unsafe staged component: {comp}")
                nxt = cur / comp
                try:
                    lst = os.lstat(nxt)
                except OSError as exc:
                    raise OSError(f"canonical ancestor unreadable {nxt}: {exc}") from exc
                if _stat.S_ISLNK(lst.st_mode):
                    raise OSError(f"canonical ancestor is symlink: {nxt}")
                if i < len(parts) - 1 and not _stat.S_ISDIR(lst.st_mode):
                    raise OSError(f"canonical ancestor not a dir: {nxt}")
                cur = nxt
            canon = os.lstat(root_resolved / staged_rel)
        except OSError as exc:
            entry["error"] = f"canonical staged entry unreadable: {exc}"
            raise _fail("STAGED_ROOT_ENTRY_FAILED", phase, disp,
                        f"canonical staged entry unreadable before writing {leaf}: {exc}", owned) from exc
        if _stat.S_ISLNK(canon.st_mode) or not _stat.S_ISDIR(canon.st_mode):
            entry["error"] = "canonical staged entry not a real dir"
            raise _fail("STAGED_ROOT_REPLACED", phase, disp,
                        f"canonical staged entry replaced before writing {leaf}", owned)
        if (canon.st_dev, canon.st_ino) != dir_identity:
            entry["error"] = "canonical entry != earliest owned identity"
            raise _fail("STAGED_ROOT_REPLACED", phase, disp,
                        f"canonical staged entry != earliest mkdir identity before writing {leaf}", owned)
    try:
        fd = os.open(leaf, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
                      0o666, dir_fd=staged_fd)
    except FileExistsError as exc:
        entry["error"] = "raced into existence"
        raise _fail("STAGED_FILE_EXISTS", phase, disp,
                    f"staged file raced into existence: {full}", owned) from exc
    except OSError as exc:
        entry["error"] = f"create failed: {exc}"
        raise _fail("STAGED_FILE_CREATE_FAILED", phase, disp,
                    f"staged file create failed: {full}: {exc}", owned) from exc
    # From here the descriptor is owned exactly once; every failure path below
    # closes exactly once and records secondary close errors (R2-7: no silent
    # discard, no blind retry on a possibly reused number).
    fd_closed = False
    def _close_once_record(tag: str) -> None:
        nonlocal fd_closed
        if fd_closed:
            return
        try:
            os.close(fd)
        except OSError as exc:
            entry.setdefault("secondary_close_errors", []).append(f"{tag}: {exc}")
            owned.setdefault("secondary_close_errors", []).append(f"{full}:{tag}: {exc}")
        finally:
            fd_closed = True
    try:
        st = os.fstat(fd)
    except OSError as exc:
        entry["error"] = f"fstat failed, identity unknown: {exc}"
        entry["dev"], entry["ino"] = "unknown", "unknown"
        _close_once_record("fstat-cleanup")
        raise _fail("STAGED_FILE_FSTAT_FAILED", phase, disp,
                    f"staged file fstat failed before any write: {leaf}: {exc}", owned) from exc
    entry["dev"], entry["ino"] = st.st_dev, st.st_ino
    if not _stat.S_ISREG(st.st_mode):
        entry["error"] = "created file is not regular"
        _close_once_record("not-regular-cleanup")
        raise _fail("STAGED_FILE_NOT_REGULAR", phase, disp,
                    f"created staged file is not regular: {leaf}", owned)
    try:
        ent = session._entry_identity(staged_fd, leaf, "staged " + leaf, phase, disp)
    except Exception as exc:
        entry["error"] = f"entry identity failed: {exc}"
        # RetentionError and StagedSourceError both preserve explicitly; the
        # descriptor state is unknown-identity but closed exactly once.
        _close_once_record("entry-cleanup")
        if isinstance(exc, retention.RetentionError):
            raise _fail("STAGED_FILE_IDENTITY_FAILED", phase, disp,
                        f"staged file entry identity failed: {leaf}: {exc}", owned) from exc
        raise _fail("STAGED_FILE_IDENTITY_FAILED", phase, disp,
                    f"staged file entry identity failed: {leaf}: {exc}", owned) from exc
    if (st.st_dev, st.st_ino) != (ent[0], ent[1]):
        entry["error"] = "replaced between create and fstat"
        _close_once_record("replaced-cleanup")
        raise _fail("STAGED_FILE_REPLACED", phase, disp,
                    f"staged file replaced between create and fstat: {leaf}", owned)
    primary: StagedSourceError | None = None
    try:
        view = memoryview(data)
        while view:
            try:
                written = os.write(fd, view)
            except OSError as exc:
                primary = _fail("STAGED_FILE_WRITE_FAILED", phase, disp,
                                    f"staged file short/failed write: {leaf}: {exc}", owned)
                raise primary from exc
            if written <= 0:
                primary = _fail("STAGED_FILE_WRITE_FAILED", phase, disp,
                                    f"staged file zero write: {leaf}", owned)
                raise primary
            view = view[written:]
            # R2-3: progressive byte progress (not only after ALL writes).
            entry["bytes_written"] = len(data) - len(view)
        # Durability seam (contract S4/S5 fault taxonomy): fsync before close.
        # No atomicity/power-loss claim; failure => INDETERMINATE (complete
        # bytes may already exist). Assigned to primary so a later close
        # failure attaches as secondary instead of masking it (R2-7).
        try:
            os.fsync(fd)
        except OSError as exc:
            entry["fsync"] = f"failed: {exc}"
            entry["error"] = f"fsync failed: {exc}"
            primary = _fail("FSYNC_FAILED", "MANIFEST" if leaf == MANIFEST_FILENAME else phase,
                        "INDETERMINATE_INVOCATION",
                        f"staged file fsync failed (bytes may be complete): {leaf}: {exc}",
                        owned)
            raise primary from exc
        entry["fsync"] = "ok"
    finally:
        # A close failure after fully written + fsynced bytes leaves a
        # potentially complete file: INDETERMINATE, never a success label and
        # never silently INCOMPLETE. It must not mask an in-flight primary
        # (write or fsync) error (R2-7).
        try:
            os.close(fd)
            fd_closed = True
        except OSError as exc:
            entry["close"] = f"failed: {exc}"
            fd_closed = True
            if primary is not None:
                _attach_close(primary, exc)
            else:
                # Per-file close uncertainty with complete bytes: INDETERMINATE
                # (distinguished from a missing-manifest INCOMPLETE set by the
                # caller phases: MANIFEST/CLOSE vs CLAIM/OWNED_PARTIAL).
                raise _fail("CLOSE_FAILED", phase, "INDETERMINATE_INVOCATION",
                            f"staged file close failed (bytes may be complete): {leaf}: {exc}",
                            owned) from exc
        else:
            entry["close"] = "ok"
    if primary is not None:
        raise primary
    try:
        back = session.safe_read(full, "staged readback " + leaf, phase, disp)[1]
    except Exception as exc:
        entry["readback"] = f"failed: {exc}"
        entry["error"] = f"readback failed: {exc}"
        raise _fail("STAGED_FILE_READBACK_FAILED", phase, disp,
                    f"staged file readback failed: {leaf}: {exc}", owned) from exc
    if back != data:
        entry["readback"] = "mismatch"
        entry["error"] = "readback != expected bytes"
        raise _fail("STAGED_FILE_READBACK_MISMATCH", phase, disp,
                    f"staged file readback != expected bytes: {leaf}", owned)
    entry["readback"] = "ok"


def _emit_outputs(session: Any, staged_fd: int, staged_rel: str,
                  expected_outputs: dict[str, tuple[str, bytes]], owned: dict[str, Any],
                  phase: str, disp: str,
                  manifest_name: str | None = None, manifest_bytes: bytes | None = None) -> None:
    dir_identity = owned.get("staged_identity")
    for _role, (name, data) in expected_outputs.items():
        _write_owned_file(session, staged_fd, staged_rel, name, data, owned, phase, disp,
                          dir_identity=dir_identity)
    if manifest_name is not None and manifest_bytes is not None:
        _write_owned_file(session, staged_fd, staged_rel, manifest_name, manifest_bytes,
                          owned, phase, disp, dir_identity=dir_identity)


def _verify_outputs_and_manifest(session: Any, staged_rel: str,
                                 expected_outputs: dict[str, tuple[str, bytes]],
                                 manifest_bytes: bytes, phase: str, disp: str) -> None:
    for _role, (name, data) in list(expected_outputs.items()) + \
            [("manifest", (MANIFEST_FILENAME, manifest_bytes))]:
        _rel, back = session.safe_read(staged_rel + "/" + name,
                                       "staged verify " + name, phase, disp)
        if back != data:
            raise _fail("OUTPUT_MISMATCH", phase, disp,
                        f"staged file != expected bytes: {name}")
    want = {staged_rel + "/" + name for _role, (name, _data)
            in list(expected_outputs.items()) + [("manifest", (MANIFEST_FILENAME, manifest_bytes))]}
    got_files, got_dirs, _got_sizes = retention._snapshot_expanded(
        session, [staged_rel], "staged verify", phase, disp)
    if set(got_files) != want or set(got_dirs) != {staged_rel}:
        raise _fail("STAGED_SET_MISMATCH", phase, disp, "staged set != exact 4-file closure")


def verify_staged_source(root: str | Path, proposal_path: str | Path,
                         staged_manifest_path: str | Path) -> dict[str, Any]:
    """Standalone read-only staged-set verification + deterministic replay.

    No P2V, no current-State validation, no HEAD comparison. Historical
    namespace comes from P2R-verified retained bytes only.
    """
    for name in _UNSAFE_GIT_VARS:
        if os.environ.get(name):
            raise _fail("GIT_ENV_REFUSED", "PIN", "INVALID",
                        f"inherited {name} refuses isolated verification")
    session: Any = None
    phase = "PIN"
    disp = "INVALID"
    try:
        try:
            session = retention._Session(root)
        except Exception as exc:
            raise _fail("ROOT_UNSAFE", phase, disp, f"repo root refused: {exc}",
                        cause=exc) from exc
        root_path = session.root_resolved
        # V1: safe-pin supplied proposal + staged manifest; schema pins first.
        prop_rel, prop_data = session.safe_read(str(proposal_path),
                                                "editorial correction proposal", phase, disp)
        if prop_rel.split("/")[-1] != "proposal.json":
            raise _fail("PROPOSAL_FILENAME", phase, disp, "proposal file must be named proposal.json")
        sm_rel, sm_data = session.safe_read(str(staged_manifest_path),
                                            "staged source manifest", phase, disp)
        if sm_rel.split("/")[-1] != MANIFEST_FILENAME:
            raise _fail("MANIFEST_FILENAME", phase, disp,
                        "staged manifest file must be named " + MANIFEST_FILENAME)
        for schema_rel in (PROPOSAL_SCHEMA.as_posix(), RETENTION_MANIFEST_SCHEMA.as_posix(),
                           STAGED_SCHEMA.as_posix(), REVIEW_SCHEMA.as_posix(), GATE_SCHEMA.as_posix()):
            session.safe_read(schema_rel, "verifier schema pin", phase, disp)
        try:
            proposal = retention._parse_json_strict(prop_data, "editorial correction proposal",
                                                    phase, disp, "PROPOSAL_UNREADABLE")
            staged = retention._parse_json_strict(sm_data, "staged source manifest",
                                                  phase, disp, "MANIFEST_UNREADABLE")
        except retention.RetentionError as exc:
            raise _fail("PIN_UNREADABLE", phase, disp, f"pinned JSON unreadable: {exc}",
                        cause=exc) from exc
        if not isinstance(proposal, dict) or not isinstance(staged, dict):
            raise _fail("PIN_UNREADABLE", phase, disp, "proposal/manifest must be objects")
        if staged.get("proposal_ref", {}).get("path") != prop_rel or \
                staged.get("proposal_ref", {}).get("sha256") != core.sha256_bytes(prop_data):
            raise _fail("PROPOSAL_REF_MISMATCH", phase, disp,
                        "staged proposal_ref != supplied proposal bytes")
        # Proposal-ref identity beyond path/SHA: the six carried IDs must
        # equal the supplied proposal (drift in IDs alone refuses).
        staged_pref = staged.get("proposal_ref") or {}
        for id_key in ("proposal_id", "issue_id", "research_profile", "publication_profile"):
            if staged_pref.get(id_key) != proposal.get(id_key):
                raise _fail("PROPOSAL_REF_MISMATCH", phase, disp,
                            f"staged proposal_ref {id_key} != supplied proposal")
        # Top-level labels + strict contract identity must agree staged vs proposal.
        for label_key in ("issue_id", "research_profile", "publication_profile"):
            if staged.get(label_key) != proposal.get(label_key):
                raise _fail("LABEL_MISMATCH", phase, disp,
                            f"staged top-level {label_key} != proposal")
        if staged.get("basis") != proposal.get("basis"):
            raise _fail("BASIS_MISMATCH", phase, disp, "staged basis != proposal basis")
        if staged.get("proposed") != proposal.get("proposed"):
            raise _fail("PROPOSED_MISMATCH", phase, disp, "staged proposed != proposal proposed")
        _check_contract_identity((staged.get("basis") or {}).get("contract_identity"), phase, disp)
        if _check_contract_identity((proposal.get("basis") or {}).get("contract_identity"),
                                    phase, disp) != \
                _check_contract_identity((staged.get("basis") or {}).get("contract_identity"),
                                         phase, disp):
            raise _fail("CONTRACT_IDENTITY_MISMATCH", phase, disp,
                        "staged contract identity != proposal contract identity")
        try:
            schema_gate.validate_instance(proposal, root_path / PROPOSAL_SCHEMA,
                                          label="editorial correction proposal")
            schema_gate.validate_instance(staged, root_path / STAGED_SCHEMA,
                                          label="editorial staged source manifest")
        except ValueError as exc:
            raise _fail("SCHEMA_INVALID", phase, disp, f"schema invalid: {exc}") from exc
        for schema_rel in (PROPOSAL_SCHEMA.as_posix(), STAGED_SCHEMA.as_posix()):
            session.safe_read(schema_rel, "verifier schema recheck", phase, disp)
        try:
            profile_label = proposal["publication_profile"]
        except (KeyError, TypeError) as exc:
            raise _fail("ROUTE_UNKNOWN", phase, disp, f"proposal lacks publication_profile: {exc}") from exc
        route = _route_of(proposal, {"proposal_ref": staged.get("proposal_ref")}, phase, disp)
        if staged.get("publication_profile") != profile_label or staged.get("route") != route:
            raise _fail("ROUTE_MISMATCH", phase, disp, "staged manifest labels != proposal route")
        code_deps = _route_code_deps(route)
        got_deps = staged.get("code_deps")
        if not isinstance(got_deps, list) or [d.get("path") for d in got_deps] != list(code_deps):
            raise _fail("CODE_DEPS_MISMATCH", phase, disp,
                        "staged code_deps != fixed sorted S2 set for route")
        dep_pins: dict[str, str] = {}
        dep_sizes: dict[str, int] = {}
        for dep in code_deps:
            _rel, _data = session.safe_read(dep, "S2 dep pin", phase, disp)
            dep_pins[dep] = core.sha256_bytes(_data)
            dep_sizes[dep] = len(_data)
        for row in got_deps:
            ordered = _ordered_sized_ref(row, "staged code_dep", phase, disp)
            if dep_pins[ordered["path"]] != ordered["sha256"] or \
                    dep_sizes[ordered["path"]] != ordered["byte_count"]:
                raise _fail("TOOL_DRIFT", phase, disp,
                            f"staged code_dep pin != current bytes: {ordered['path']}")
        route_schemas = (LONGFORM_READER_SCHEMA, LONGFORM_RECEIPT_SCHEMA) \
            if route == LONGFORM_ROUTE else (WEEKLY_READER_SCHEMA, WEEKLY_RECEIPT_SCHEMA)
        for schema_rel in route_schemas:
            session.safe_read(schema_rel.as_posix(), "route schema pin", phase, disp)
        _check_runtime_binding(root_path, dep_pins, phase, disp)
        orig_proposal_sha = core.sha256_bytes(prop_data)
        orig_staged_sha = core.sha256_bytes(sm_data)
        lock_map = dict(session.files)
        # V2: full P2R verification on the manifest-declared retention path.
        phase = "RETAINED"
        man_ref = staged.get("retention_manifest_ref") or {}
        if set(man_ref) != {"path", "sha256"}:
            raise _fail("REF_SHAPE", phase, disp, "staged retention_manifest_ref must be exact {path,sha256}")
        ret_man_rel, ret_man_data = session.safe_read(man_ref["path"], "retention manifest", phase, disp)
        if core.sha256_bytes(ret_man_data) != man_ref["sha256"]:
            raise _fail("RETENTION_REF_DRIFT", phase, disp, "retention manifest bytes != staged ref")
        try:
            ret_manifest = retention._parse_json_strict(ret_man_data, "retention manifest",
                                                        phase, disp, "MANIFEST_UNREADABLE")
        except retention.RetentionError as exc:
            raise _fail("PIN_UNREADABLE", phase, disp, f"retention manifest unreadable: {exc}",
                        cause=exc) from exc
        try:
            schema_gate.validate_instance(ret_manifest, root_path / RETENTION_MANIFEST_SCHEMA,
                                          label="editorial retention manifest")
        except ValueError as exc:
            raise _fail("SCHEMA_INVALID", phase, disp, f"retention manifest schema invalid: {exc}") from exc
        try:
            with retention._sanitized_git_env_ctx():
                verified = retention.verify_retention(root_path, proposal_path, man_ref["path"])
        except Exception as exc:
            raise _fail("P2R_REFUSED", phase, disp, f"P2R verification refused: {exc}",
                        cause=exc) from exc
        if not isinstance(verified, dict) or verified.get("result") != retention.RESULT_VERIFIED:
            raise _fail("RETAINED_NOT_VERIFIED", phase, disp, "P2R did not return VERIFIED")
        if verified.get("proposal_sha256") != orig_proposal_sha or \
                verified.get("manifest_sha256") != core.sha256_bytes(ret_man_data):
            raise _fail("RETAINED_SHA_MISMATCH", phase, disp, "P2R SHAs != original pins")
        checked = verified.get("checked") or {}
        # Independent typed I1 hops from ORIGINAL pinned bytes (P2R returns
        # hashes/counts, not a decoded chain — decode here, compare after).
        if ret_manifest.get("proposal_ref", {}).get("sha256") != orig_proposal_sha:
            raise _fail("HEADER_MISMATCH", phase, disp, "retention proposal_ref != pinned proposal bytes")
        if ret_manifest.get("basis") != proposal.get("basis"):
            raise _fail("BASIS_MISMATCH", phase, disp, "retention basis != pinned proposal basis")
        if ret_manifest.get("proposed") != proposal.get("proposed"):
            raise _fail("PROPOSED_MISMATCH", phase, disp, "retention proposed != pinned proposal proposed")
        rows = ret_manifest.get("rows")
        plan = proposal.get("retention_plan")
        if not isinstance(rows, list) or not isinstance(plan, list) or len(rows) != len(plan):
            raise _fail("RETENTION_MISMATCH", phase, disp, "retention rows/plan shape mismatch")
        try:
            proposal_dir = prop_rel.rsplit("/", 1)[0]
            state_rows = [r for r in rows if "state:authority" in (r.get("roles") or [])]
            if len(state_rows) != 1:
                raise _fail("MISSING_STATE_AUTHORITY", phase, disp, "unique state:authority row required")
            srow = state_rows[0]
            basis = proposal.get("basis") or {}
            if srow.get("policy") != "COPY_BEFORE_REPLACEMENT":
                raise _fail("INVALID_RETENTION", phase, disp, "state:authority must be COPY")
            if srow.get("path") != (basis.get("state_ref") or {}).get("path") or \
                    srow.get("sha256") != (basis.get("state_ref") or {}).get("sha256"):
                raise _fail("STATE_REF_MISMATCH", phase, disp, "state:authority != proposal basis.state_ref")
            provisional = retention._expected_retained_dest(proposal_dir, srow["path"])
            if srow.get("retained_dest") != provisional:
                raise _fail("RETENTION_DEST_MISMATCH", phase, disp, "COPY dest != recomputed provisional dest")
            _srel, sdata = session.safe_read(srow["retained_dest"], "retained State", phase, disp)
            if core.sha256_bytes(sdata) != srow["sha256"] or len(sdata) != srow["byte_count"]:
                raise _fail("INVALID_RETENTION", phase, disp, "retained State bytes differ from row")
            rstate = retention._parse_json_strict(sdata, "retained State", phase, disp, "INVALID_RETENTION")
            rprof = rstate.get("profile") or {}
            if not isinstance(rprof, dict) or set(rprof) != {"path", "sha256"}:
                raise _fail("INVALID_RETENTION", phase, disp, "retained State lacks exact profile ref")
            matches = [r for r in rows if r.get("policy") == "KEEP_IMMUTABLE"
                       and r.get("retained_ref", {}).get("path") == rprof.get("path")
                       and r.get("retained_ref", {}).get("sha256") == rprof.get("sha256")]
            if len(matches) != 1:
                raise _fail("MISSING_PROFILE_MATCH", phase, disp, "unique matching KEEP Profile row required")
            _prel, pdata = session.safe_read(matches[0]["retained_ref"]["path"],
                                             "required KEEP Profile", phase, disp)
            if core.sha256_bytes(pdata) != rprof.get("sha256"):
                raise _fail("PROFILE_DRIFT", phase, disp, "KEEP Profile bytes drifted")
            rprofile = retention._parse_json_strict(pdata, "KEEP Profile", phase, disp, "INVALID_RETENTION")
            if rstate.get("issue_id") != proposal.get("issue_id"):
                raise _fail("LABEL_MISMATCH", phase, disp, "retained State issue != proposal issue")
            for label_key in ("research_profile", "publication_profile"):
                if rstate.get(label_key) != proposal.get(label_key):
                    raise _fail("LABEL_MISMATCH", phase, disp, f"retained State {label_key} != proposal")
            if rprofile.get("issue_id") != proposal.get("issue_id"):
                raise _fail("LABEL_MISMATCH", phase, disp, "KEEP Profile issue != proposal issue")
            source_root_rel = rprofile["paths"]["source_root"]
            survey_root_rel = rprofile["paths"]["survey_root"]
        except StagedSourceError:
            raise
        except Exception as exc:
            if isinstance(exc, retention.RetentionError):
                raise _fail("CHAIN_FAILED", phase, disp, f"historical chain failed: {exc}",
                            cause=exc) from exc
            raise _fail("CHAIN_FAILED", phase, disp, f"historical chain failed: {exc}",
                        cause=exc) from exc
        try:
            expected_dir = (Path(source_root_rel) / "publication" / "v2" /
                            "editorial-corrections" / proposal["proposal_id"]).as_posix()
        except (KeyError, TypeError) as exc:
            raise _fail("PROPOSAL_LAYOUT", phase, disp, f"cannot derive canonical proposal dir: {exc}") from exc
        if proposal_dir != expected_dir:
            raise _fail("PROPOSAL_LAYOUT", phase, disp, "proposal file outside canonical retained dir")
        staged_rel = expected_dir + "/" + STAGED_DIRNAME
        if sm_rel != staged_rel + "/" + MANIFEST_FILENAME:
            raise _fail("STAGED_NAMESPACE", phase, disp, "staged manifest outside canonical staged dir")
        if staged.get("issue_id") != proposal.get("issue_id"):
            raise _fail("LABEL_MISMATCH", phase, disp, "staged issue != proposal issue")
        # V3: scope through the narrow Session adapter + retained State/Profile.
        phase = "SCOPE"
        scope_ref = staged.get("scope_review_ref") or {}
        if set(scope_ref) != {"path", "sha256"}:
            raise _fail("REF_SHAPE", phase, disp, "staged scope_review_ref must be exact {path,sha256}")
        _screl, scdata = session.safe_read(scope_ref["path"], "scope review record", phase, disp)
        if core.sha256_bytes(scdata) != scope_ref["sha256"]:
            raise _fail("SCOPE_DRIFT", phase, disp, "scope review bytes != staged ref")
        if rprofile.get("publication_profile") != profile_label:
            raise _fail("LABEL_MISMATCH", phase, disp, "KEEP Profile publication_profile != proposal")
        shim = _SessionScopeReader(session)
        try:
            outcome = p1mod._validate_scope(shim, root_path, scope_ref["path"], proposal, rstate, rprofile)
        except Exception as exc:
            raise _fail("SCOPE_REFUSED", phase, disp, f"existing scope rules refused: {exc}",
                        cause=exc) from exc
        if outcome != p1mod.RESULT_BOUND:
            raise _fail("SCOPE_NOT_BOUND", phase, disp, f"scope did not bind: {outcome}")
        try:
            session.reverify(phase, disp)
        except Exception as exc:
            raise _fail("SCOPE_REVERIFY_FAILED", phase, disp,
                        f"post-scope reverify failed: {exc}", cause=exc) from exc
        # V4: deterministic replay from pinned staged reader bytes.
        phase = "REPLAY"
        reader_ref = (proposal.get("proposed") or {}).get("proposed_reader_ref") or {}
        canon_sha = (proposal.get("proposed") or {}).get("proposed_reader_canonical_sha256")
        try:
            staged_reader_rel = session.repinned(reader_ref, "staged proposed reader", phase, disp)
        except Exception as exc:
            raise _fail("READER_PIN_FAILED", phase, disp, f"staged reader pin failed: {exc}",
                        cause=exc) from exc
        reader_bytes = session.files[staged_reader_rel]
        if core.sha256_bytes(reader_bytes) != canon_sha:
            raise _fail("PROPOSED_DIGEST_MISMATCH", phase, disp, "staged reader != canonical digest")
        try:
            reader_obj = json.loads(reader_bytes.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise _fail("READER_UNREADABLE", phase, disp, f"staged reader not JSON: {exc}") from exc
        try:
            if route == LONGFORM_ROUTE:
                reviewed = longform_derivation.validate_longform_reader_input(root_path, reader_obj)
                if reader_bytes != longform_derivation.canonical_reader_bytes(reviewed):
                    raise _fail("READER_NONCANONICAL", phase, disp,
                                "staged reader FILE bytes != canonical rederived bytes")
                main_text = longform_generated.render_main(reviewed)
                bib_text = longform_generated.render_bibliography(reviewed)
                style_text = session.files[STYLE_PATH.as_posix()].decode("utf-8")
                longform_generated.validate_heading_syntax(reviewed)
                longform_generated.validate_generated_closure(main_text, style_text)
            else:
                reviewed = weekly.validate_reader_input(root_path, reader_obj)
                main_text = weekly.render_main(reviewed)
                bib_text = weekly.render_bibliography(reviewed)
                style_text = session.files[STYLE_PATH.as_posix()].decode("utf-8")
                weekly.validate_generated_closure(main_text, style_text)
        except (ValueError, UnicodeDecodeError) as exc:
            raise _fail("REPLAY_MISMATCH", phase, disp, f"deterministic replay refused: {exc}") from exc
        expected = {role: (staged.get("outputs") or {}).get(role) or {} for role in ("main", "bibliography", "style")}
        replay_bytes = {"main": main_text.encode("utf-8"), "bibliography": bib_text.encode("utf-8"),
                        "style": session.files[STYLE_PATH.as_posix()]}
        for role, data in replay_bytes.items():
            row = expected[role]
            if row.get("path") != staged_rel + "/" + {"main": MAIN_FILENAME,
                                                      "bibliography": BIBLIOGRAPHY_FILENAME,
                                                      "style": STYLE_FILENAME}[role]:
                raise _fail("OUTPUT_PATH_MISMATCH", phase, disp, f"staged {role} path not canonical")
            _orel, oback = session.safe_read(row.get("path", ""), "staged output " + role, phase, disp)
            if oback != data or core.sha256_bytes(data) != row.get("sha256") or \
                    len(data) != row.get("byte_count"):
                raise _fail("REPLAY_MISMATCH", phase, disp, f"staged {role} != deterministic replay bytes")
        style_pinned = session.files[STYLE_PATH.as_posix()]
        if replay_bytes["style"] != style_pinned:
            raise _fail("STYLE_MISMATCH", phase, disp, "staged style != pinned style input")
        # style_input_ref must be the fixed template path/hash/size (not a
        # self-referential output hash, not a caller-chosen path).
        style_ref = staged.get("style_input_ref") or {}
        if style_ref.get("path") != STYLE_PATH.as_posix() or \
                style_ref.get("sha256") != core.sha256_bytes(style_pinned) or \
                style_ref.get("byte_count") != len(style_pinned):
            raise _fail("STYLE_REF_MISMATCH", phase, disp,
                        "staged style_input_ref != fixed template path/hash/size")
        if expected["style"].get("sha256") != core.sha256_bytes(style_pinned) or \
                expected["style"].get("byte_count") != len(style_pinned):
            raise _fail("STYLE_MISMATCH", phase, disp, "staged style output != pinned style input")
        # V5: exact closed set + manifest self-digest/canonical bytes.
        phase = "VERIFY"
        got_files, got_dirs, _got_sizes = retention._snapshot_expanded(
            session, [staged_rel], "staged verify", phase, disp)
        want = {staged_rel + "/" + name for name in (MAIN_FILENAME, BIBLIOGRAPHY_FILENAME,
                                                     STYLE_FILENAME, MANIFEST_FILENAME)}
        if set(got_files) != want or set(got_dirs) != {staged_rel}:
            raise _fail("STAGED_SET_MISMATCH", phase, disp, "staged set != exact 4-file closure")
        if _manifest_digest(staged) != staged.get("manifest_digest"):
            raise _fail("MANIFEST_DIGEST_MISMATCH", phase, disp, "staged manifest self-digest mismatch")
        if _canonical_json_bytes({k: v for k, v in staged.items()}) != sm_data:
            raise _fail("MANIFEST_NONCANONICAL", phase, disp, "staged manifest bytes != canonical projection")
        # V6 FINAL: full staged AND retained inventories + original pins after
        # later reads (scope/rendering). Retained COPY/KEEP closure is pinned
        # and checked in this verifier's own domain (no current-State/HEAD
        # authority, no blanket historical capture_inputs equality).
        phase = "FINAL"
        try:
            fin_files, fin_dirs, _fin_sizes = retention._snapshot_expanded(
                session, [staged_rel], "staged final", phase, disp)
            if set(fin_files) != want or set(fin_dirs) != {staged_rel}:
                raise _fail("STAGED_DRIFT", phase, disp, "final staged inventory drifted")
            ret_rel = expected_dir + "/retained"
            fin_ret_files, fin_ret_dirs, fin_ret_sizes = retention._retained_inventory(
                session, ret_rel, phase, disp)
            man_rows = ret_manifest.get("rows")
            if not isinstance(man_rows, list):
                raise _fail("RETENTION_MISMATCH", phase, disp, "retention rows must be a list")
            exp_files_set, exp_dirs_set = retention._retained_expected_sets(
                man_rows, ret_man_rel, ret_rel)
            if set(fin_ret_files) != exp_files_set or set(fin_ret_dirs) != exp_dirs_set:
                raise _fail("INVALID_RETENTION", phase, disp, "final retained inventory drifted")
            for r in man_rows:
                if r.get("policy") == "COPY_BEFORE_REPLACEMENT":
                    _rr, back = session.safe_read(r["retained_dest"], "COPY final recheck",
                                                  phase, disp)
                    if core.sha256_bytes(back) != r["sha256"] or len(back) != r["byte_count"]:
                        raise _fail("COPY_DRIFT", phase, disp,
                                    f"final COPY bytes drifted: {r['retained_dest']}")
                else:
                    session.repinned(r["retained_ref"], "KEEP final recheck", phase, disp,
                                     expected_size=r["byte_count"])
            for rel, orig_bytes in lock_map.items():
                cur = session.files.get(rel)
                if cur is None or cur != orig_bytes:
                    raise _fail("PIN_DRIFT", phase, disp,
                                f"consumed pin changed after later reads: {rel}")
            if session.files.get(sm_rel) != sm_data or session.files.get(prop_rel) != prop_data:
                raise _fail("PIN_DRIFT", phase, disp, "supplied bytes changed after later reads")
            session.reverify(phase, disp)
        except StagedSourceError:
            raise
        except Exception as exc:
            if isinstance(exc, retention.RetentionError):
                raise _fail("FINAL_FAILED", phase, disp, f"final boundary failed: {exc}",
                            cause=exc) from exc
            raise _fail("FINAL_FAILED", phase, disp, f"final boundary failed: {exc}",
                        cause=exc) from exc
        _close_session(session, "CLOSE", "VERIFIED")
        session = None
        return {
            "result": RESULT_VERIFIED,
            "proposal_ref": {"path": prop_rel, "sha256": orig_proposal_sha},
            "staged_manifest_ref": {"path": sm_rel, "sha256": orig_staged_sha},
            "observed_refs": {
                "retention_manifest_ref": {"path": ret_man_rel,
                                           "sha256": core.sha256_bytes(ret_man_data)},
                "scope_review_ref": {"path": _screl, "sha256": core.sha256_bytes(scdata)},
                "code_deps": [{"path": dep, "sha256": dep_pins[dep], "byte_count": dep_sizes[dep]}
                               for dep in code_deps],
            },
            "measured": {
                "proposed_reader_sha256": canon_sha,
                "replay_main_sha256": core.sha256_bytes(replay_bytes["main"]),
                "replay_bib_sha256": core.sha256_bytes(replay_bytes["bibliography"]),
                # Any style mismatch already refused above (STYLE_MISMATCH /
                # per-role replay equality); reaching here proves the match.
                "style_match": True,
                "closure_count": len(code_deps),
            },
        }
    except StagedSourceError as primary:
        if session is not None:
            _close_session(session, primary.phase, primary.disposition, primary)
            session = None
        raise
    except Exception as exc:
        if isinstance(exc, retention.RetentionError):
            wrapped = _fail("VERIFIER_FAILED", phase, disp,
                            f"retention layer refused: {exc}", cause=exc)
        else:
            wrapped = _fail("VERIFIER_FAILED", phase, disp,
                            f"unexpected verifier failure: {exc}", cause=exc)
        if session is not None:
            _close_session(session, phase, disp, wrapped)
            session = None
        raise wrapped from exc