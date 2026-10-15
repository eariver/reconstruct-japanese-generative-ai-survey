#!/usr/bin/env python3
"""DM021-P2V read-only retained-aware current-basis observer.

Read-only observation combining fresh current-basis checks with exact
retained-set verification. No writes, no approval, no reason enum, no State
adoption, no CLI, no PASS generation, no bearer permission.

Entry point:

  observe_current_authority(root, state_path, proposal_path, manifest_path,
                            scope_review_path=None) -> observation

Three comparisons stay distinct: current basis vs supplied proposal (exact P1
header/basis/proposed/plan + staged reader bytes), retained-set consistency
(full P2R validation + exact row bytes/sizes/inventory), invocation-entry to
final stability (ORIGINAL pins + full control/edition/retained inventories +
HEAD, no resnapshot laundering).

All refusals raise CurrentAuthorityError (ValueError) with machine-readable
``CODE: [phase] detail`` prefix and chained original cause. No owned files,
no new writer disposition.
"""
from __future__ import annotations

import json
import os
import stat as _stat
import subprocess
from pathlib import Path
from typing import Any

from scripts import survey_editorial_correction_proposal_v2 as p1mod
from scripts import survey_editorial_retention_v2 as retention
from scripts import survey_production_v2 as core

RESULT_NEEDS_SCOPE = "CURRENT_BASIS_OBSERVED_NEEDS_SCOPE"
RESULT_SCOPE_BOUND = "CURRENT_BASIS_OBSERVED_SCOPE_BOUND"

PROPOSAL_SCHEMA = Path("schemas/editorial-correction-proposal-v2.schema.json")
MANIFEST_SCHEMA = Path("schemas/editorial-retention-manifest-v2.schema.json")


class CurrentAuthorityError(ValueError):
    """Typed read-only refusal. Message starts with ``CODE: [phase]`` prefix."""

    def __init__(self, code: str, phase: str | None = None, detail: str = "",
                 cause: BaseException | None = None) -> None:
        # Allow single-string form CurrentAuthorityError("CODE: [phase] detail")
        # for compatibility, plus structured (code, phase, detail, cause).
        if phase is None and detail == "":
            super().__init__(code)
            text = str(code)
            if ":" in text:
                self.code = text.split(":", 1)[0].strip()
            else:
                self.code = "OBSERVER_FAILED"
            self.phase = "FINAL"
            self.detail = text
        else:
            super().__init__(f"{code}: [{phase}] {detail}")
            self.code = code
            self.phase = phase if phase is not None else "FINAL"
            self.detail = detail
        if cause is not None:
            self.__cause__ = cause


def _fail(code: str, phase: str, detail: str, cause: BaseException | None = None) -> CurrentAuthorityError:
    return CurrentAuthorityError(code, phase, detail, cause=cause)


def _sanitized_head(root: Path, phase: str) -> str:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    try:
        proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                              capture_output=True, text=True, env=env, timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        raise _fail("GIT_UNAVAILABLE", phase, f"git rev-parse failed: {exc}", cause=exc) from exc
    if proc.returncode != 0:
        raise _fail("GIT_UNAVAILABLE", phase, f"git rev-parse rc={proc.returncode}: {proc.stderr.strip()}")
    value = proc.stdout.strip()
    if len(value) != 40 or any(c not in "0123456789abcdef" for c in value):
        raise _fail("GIT_UNAVAILABLE", phase, f"HEAD not 40-hex: {value!r}")
    return value


def _wrap_p1(exc: BaseException, phase: str) -> CurrentAuthorityError:
    text = str(exc)
    code = text.split(":", 1)[0].strip() if ":" in text else "P1_REFUSED"
    if not code or " " in code or len(code) > 64:
        code = "P1_REFUSED"
    return _fail(code, phase, f"P1: {text}", cause=exc)


def _wrap_p2r(exc: BaseException, phase: str) -> CurrentAuthorityError:
    text = str(exc)
    code = text.split(":", 1)[0].strip() if ":" in text else "P2R_REFUSED"
    if not code or " " in code or len(code) > 64:
        code = "P2R_REFUSED"
    return _fail(code, phase, f"P2R: {text}", cause=exc)


def observe_current_authority(root: str | Path, state_path: str | Path,
                              proposal_path: str | Path, manifest_path: str | Path,
                              scope_review_path: str | Path | None = None) -> dict[str, Any]:
    """Read-only current-basis + retained-set observation (no bearer permission)."""
    root_path = Path(root).resolve()
    live: Any = None
    session: Any = None
    try:
        # 1. Raw-safe narrow pins before validators that reopen same files.
        try:
            live = p1mod._Collector(root_path)
        except Exception as exc:
            raise _wrap_p1(exc, "PIN") from exc
        orig_head = live.head
        try:
            sanitized = _sanitized_head(root_path, "PIN")
        except CurrentAuthorityError:
            raise
        except Exception as exc:
            raise _fail("GIT_UNAVAILABLE", "PIN", f"sanitized HEAD pin failed: {exc}", cause=exc) from exc
        if sanitized != orig_head:
            raise _fail("HEAD_MISMATCH", "PIN", "collector HEAD differs from sanitized git HEAD")
        try:
            session = retention._Session(root_path)
        except Exception as exc:
            raise _wrap_p2r(exc, "PIN") from exc
        # Narrow pins in retained session (proposal/manifest/schemas/State).
        # Live proposal/State pins happen inside layout helper (stability-checked).
        try:
            prop_rel, prop_data = session.safe_read(str(proposal_path),
                                                    "editorial correction proposal", "VERIFY", "INVALID")
            man_rel, man_data = session.safe_read(str(manifest_path),
                                                  "retention manifest", "VERIFY", "INVALID")
            session.safe_read(PROPOSAL_SCHEMA.as_posix(), "proposal schema", "VERIFY", "INVALID")
            session.safe_read(MANIFEST_SCHEMA.as_posix(), "retention manifest schema", "VERIFY", "INVALID")
            session.safe_read(str(state_path), "Production State", "VERIFY", "INVALID")
        except Exception as exc:
            if isinstance(exc, retention.RetentionError):
                raise _wrap_p2r(exc, "PIN") from exc
            raise _fail("PIN_FAILED", "PIN", f"narrow pin failed: {exc}", cause=exc) from exc
        orig_proposal_sha = core.sha256_bytes(prop_data)
        orig_manifest_sha = core.sha256_bytes(man_data)

        # 2. Strict live authority BEFORE broad walks (inside layout helper).
        # 3. Validated snapshots: full controls + edition (retained session only;
        #    never populates live col.files with retained destinations).
        try:
            cfg_for_controls = json.loads(live.files[core.DEFAULT_CONFIG.as_posix()].decode("utf-8"))
        except Exception as exc:
            raise _fail("CONFIG_UNREADABLE", "SNAPSHOT", f"config not JSON: {exc}", cause=exc) from exc
        try:
            control_rels = retention._control_paths(cfg_for_controls, "VERIFY", "INVALID")
        except Exception as exc:
            raise _wrap_p2r(exc, "SNAPSHOT") from exc
        # Derive expected source/survey roots from live-validated profile AFTER
        # layout guard (avoid untrusted pre-guard walk). For initial snapshot we
        # need roots; use layout helper first, then snapshot controls+edition.
        try:
            layout = p1mod._pin_proposal_layout(live, root_path, state_path, proposal_path)
        except Exception as exc:
            if isinstance(exc, p1mod.ProposalError):
                raise _wrap_p1(exc, "AUTHORITY") from exc
            raise _fail("AUTHORITY_FAILED", "AUTHORITY", f"layout/authority failed: {exc}", cause=exc) from exc
        profile = layout["profile"]
        state = layout["state"]
        proposal = layout["proposal"]
        proposal_id = layout["proposal_id"]
        staged_authored = layout["staged_authored"]
        staged_reader = layout["staged_reader"]
        tree_entry = layout["tree_entry"]
        try:
            source_root_rel = profile["paths"]["source_root"]
            survey_root_rel = profile["paths"]["survey_root"]
        except (KeyError, TypeError) as exc:
            raise _fail("PROFILE_ROOT_INVALID", "SNAPSHOT", f"profile roots invalid: {exc}", cause=exc) from exc
        try:
            ctrl_files, ctrl_dirs, ctrl_sizes = retention._snapshot_expanded(
                session, control_rels, "control", "VERIFY", "INVALID")
            src_files, src_dirs, src_sizes = retention._snapshot_expanded(
                session, [source_root_rel, survey_root_rel], "edition", "VERIFY", "INVALID")
        except Exception as exc:
            raise _wrap_p2r(exc, "SNAPSHOT") from exc
        init_ctrl = (dict(ctrl_files), dict(ctrl_dirs), dict(ctrl_sizes))
        init_src = (dict(src_files), dict(src_dirs), dict(src_sizes))
        init_tree = dict(tree_entry)

        # 4. Same-invocation retained validation (actual P2R, no trust).
        try:
            verified = retention.verify_retention(root_path, proposal_path, manifest_path)
        except Exception as exc:
            raise _wrap_p2r(exc, "RETAINED") from exc
        # verify_retention returns 2 SHAs + counts, NOT row hashes.
        if not isinstance(verified, dict) or verified.get("result") != retention.RESULT_VERIFIED:
            raise _fail("RETAINED_NOT_VERIFIED", "RETAINED", "P2R did not return VERIFIED")
        if verified.get("proposal_sha256") != orig_proposal_sha:
            raise _fail("PROPOSAL_SHA_MISMATCH", "RETAINED",
                        "P2R proposal SHA differs from originally pinned proposal bytes")
        if verified.get("manifest_sha256") != orig_manifest_sha:
            raise _fail("MANIFEST_SHA_MISMATCH", "RETAINED",
                        "P2R manifest SHA differs from originally pinned manifest bytes")
        checked = verified.get("checked") or {}
        # Pin rows/ref bytes in observer's separate retained session using
        # original explicit manifest/proposal expectations (never invented hashes).
        try:
            manifest_obj = json.loads(man_data.decode("utf-8"))
            proposal_obj = json.loads(prop_data.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise _fail("MANIFEST_UNREADABLE", "RETAINED", f"pinned JSON unreadable: {exc}", cause=exc) from exc
        if manifest_obj.get("proposal_ref", {}).get("sha256") != orig_proposal_sha:
            raise _fail("HEADER_MISMATCH", "RETAINED", "manifest proposal_ref.sha256 != pinned proposal bytes")
        if manifest_obj.get("basis") != proposal_obj.get("basis"):
            raise _fail("BASIS_MISMATCH", "RETAINED", "manifest basis != pinned proposal basis")
        if manifest_obj.get("proposed") != proposal_obj.get("proposed"):
            raise _fail("PROPOSED_MISMATCH", "RETAINED", "manifest proposed != pinned proposal proposed")
        rows = manifest_obj.get("rows") or []
        plan = proposal_obj.get("retention_plan") or []
        if len(rows) != len(plan):
            raise _fail("RETENTION_MISMATCH", "RETAINED", "manifest row count != proposal plan count")
        # P1 plan COPY has dest only; manifest COPY has extra measured fields.
        for prow in plan:
            if prow.get("policy") == "COPY_BEFORE_REPLACEMENT":
                if "retained_sha256" in prow or "retained_byte_count" in prow:
                    raise _fail("PLAN_SHAPE", "RETAINED", "P1 plan COPY carries manifest-only measured fields")
                if "retained_dest" not in prow:
                    raise _fail("PLAN_SHAPE", "RETAINED", "P1 plan COPY lacks retained_dest")
        for mrow in rows:
            if mrow.get("policy") == "COPY_BEFORE_REPLACEMENT":
                for k in ("retained_dest", "retained_sha256", "retained_byte_count"):
                    if k not in mrow:
                        raise _fail("RETENTION_MISMATCH", "RETAINED", f"manifest COPY missing {k}")
                if mrow["retained_sha256"] != mrow["sha256"] or \
                        mrow["retained_byte_count"] != mrow["byte_count"]:
                    raise _fail("RETENTION_MISMATCH", "RETAINED", "manifest COPY measurement != source row")
            else:
                if mrow.get("retained_ref") != {"path": mrow["path"], "sha256": mrow["sha256"]}:
                    raise _fail("RETENTION_MISMATCH", "RETAINED", "manifest KEEP ref != source")
        # Re-pin every COPY/KEEP + staged bytes in observer session (cross-binding).
        try:
            for r in rows:
                if r.get("policy") == "COPY_BEFORE_REPLACEMENT":
                    _rel, back = session.safe_read(r["retained_dest"], "COPY rehash", "VERIFY", "INVALID")
                    if core.sha256_bytes(back) != r["sha256"] or len(back) != r["byte_count"]:
                        raise _fail("COPY_DRIFT", "RETAINED", f"COPY drift: {r['retained_dest']}")
                else:
                    session.repinned(r["retained_ref"], f"KEEP recheck {r['path']}",
                                     "VERIFY", "INVALID", expected_size=r["byte_count"])
            # Staged refs at exact canonical names.
            proposed_blk = proposal_obj.get("proposed") or {}
            authoring_ref = proposed_blk.get("authoring_input_ref") or {}
            reader_ref = proposed_blk.get("proposed_reader_ref") or {}
            session.repinned({"path": authoring_ref.get("path", ""),
                              "sha256": authoring_ref.get("sha256", "")},
                             "staged authoring_input_ref", "VERIFY", "INVALID")
            session.repinned({"path": reader_ref.get("path", ""),
                              "sha256": reader_ref.get("sha256", "")},
                             "staged proposed_reader_ref", "VERIFY", "INVALID")
            if reader_ref.get("sha256") != proposed_blk.get("proposed_reader_canonical_sha256"):
                raise _fail("PROPOSED_DIGEST_MISMATCH", "RETAINED", "reader ref != canonical sha")
            _rr, reader_bytes_ret = session.safe_read(reader_ref.get("path", ""),
                                                      "staged proposed reader", "VERIFY", "INVALID")
            if core.sha256_bytes(reader_bytes_ret) != proposed_blk.get("proposed_reader_canonical_sha256"):
                raise _fail("PROPOSED_DIGEST_MISMATCH", "RETAINED", "staged reader != canonical digest")
        except CurrentAuthorityError:
            raise
        except Exception as exc:
            if isinstance(exc, retention.RetentionError):
                raise _wrap_p2r(exc, "RETAINED") from exc
            raise _fail("RETAINED_PIN_FAILED", "RETAINED", f"retained re-pin failed: {exc}", cause=exc) from exc
        try:
            expected_dir = layout["expected_dir"]
            retained_rel = expected_dir + "/retained"
            inv_files, inv_dirs, inv_sizes = retention._retained_inventory(
                session, retained_rel, "VERIFY", "INVALID")
            exp_files_set, exp_dirs_set = retention._retained_expected_sets(
                rows, man_rel, retained_rel)
            if set(inv_files) != exp_files_set or set(inv_dirs) != exp_dirs_set:
                raise _fail("INVALID_RETENTION", "RETAINED", "retained inventory != expected sets")
        except CurrentAuthorityError:
            raise
        except Exception as exc:
            raise _wrap_p2r(exc, "RETAINED") from exc

        # 5. Common current derivation + supplied comparisons (live store only).
        try:
            change_desc = (proposal.get("proposed") or {}).get("change_description")
            data = p1mod._pipeline_data(live, root_path, Path(state_path),
                                        staged_authored, proposal_id, change_desc)
        except Exception as exc:
            if isinstance(exc, p1mod.ProposalError):
                raise _wrap_p1(exc, "DERIVE") from exc
            raise _fail("DERIVE_FAILED", "DERIVE", f"current derivation failed: {exc}", cause=exc) from exc
        # Exact live State byte equality (strict, no metadata exception).
        try:
            live_state_rel = live.rel(live.safe(str(state_path), "Production State"))
            live_state_sha = core.sha256_bytes(live.files[live_state_rel])
            basis_state = (data["proposal"].get("basis") or {}).get("state_ref") or {}
            if basis_state.get("path") != live_state_rel or basis_state.get("sha256") != live_state_sha:
                raise _fail("STATE_REF_MISMATCH", "COMPARE", "live State != rederived basis.state_ref")
            supplied_basis_state = (proposal.get("basis") or {}).get("state_ref") or {}
            if supplied_basis_state != basis_state:
                raise _fail("BASIS_MISMATCH", "COMPARE", "supplied basis.state_ref != rederived live State")
            # Staged bytes vs pinned (detect switch before comparison).
            staged_rel = live.rel(staged_reader)
            pinned_staged = live.files.get(staged_rel)
            live_staged_now = staged_reader.read_bytes()
            if pinned_staged is None or live_staged_now != pinned_staged:
                raise _fail("STABILITY_VIOLATION", "COMPARE", "staged reader changed mid-inspection")
            p1mod._compare_supplied_to_rederived(proposal, data["proposal"],
                                                 live_staged_now, data["proposed_canonical"])
        except CurrentAuthorityError:
            raise
        except Exception as exc:
            if isinstance(exc, p1mod.ProposalError):
                raise _wrap_p1(exc, "COMPARE") from exc
            raise _fail("COMPARE_FAILED", "COMPARE", f"supplied comparison failed: {exc}", cause=exc) from exc
        # Cross-binding: live rederived plan == retained manifest rows (modulo
        # manifest-only measured fields already checked above).
        try:
            live_plan = data["proposal"].get("retention_plan") or []
            if len(live_plan) != len(rows):
                raise _fail("RETENTION_MISMATCH", "COMPARE", "live plan count != retained manifest count")
            for lp, mr in zip(sorted(live_plan, key=lambda r: r["path"]),
                              sorted(rows, key=lambda r: r["path"])):
                for k in ("roles", "path", "sha256", "byte_count", "policy"):
                    if lp.get(k) != mr.get(k):
                        raise _fail("RETENTION_MISMATCH", "COMPARE", f"live vs retained row {k} differs: {lp.get('path')}")
                if lp.get("policy") == "KEEP_IMMUTABLE":
                    if lp.get("retained_ref") != mr.get("retained_ref"):
                        raise _fail("RETENTION_MISMATCH", "COMPARE", "live vs retained KEEP ref differs")
                else:
                    if lp.get("retained_dest") != mr.get("retained_dest"):
                        raise _fail("RETENTION_MISMATCH", "COMPARE", "live vs retained COPY dest differs")
        except CurrentAuthorityError:
            raise
        except Exception as exc:
            raise _fail("COMPARE_FAILED", "COMPARE", f"live/retained cross-binding failed: {exc}", cause=exc) from exc

        # 6. Optional scope BEFORE final FULL receipt.
        try:
            state2_abs = live.safe(str(state_path), "Production State")
            state2 = json.loads(live.files[live.rel(state2_abs)].decode("utf-8"))
            profile2 = p1mod._load_profile(live, state2)
        except Exception as exc:
            if isinstance(exc, p1mod.ProposalError):
                raise _wrap_p1(exc, "SCOPE") from exc
            raise _fail("SCOPE_FAILED", "SCOPE", f"scope State/Profile reload failed: {exc}", cause=exc) from exc
        scope_ref = None
        try:
            if scope_review_path is None:
                outcome = RESULT_NEEDS_SCOPE
            else:
                # Pin scope bytes in retained session as well for final union.
                try:
                    s_rel, s_data = session.safe_read(str(scope_review_path),
                                                      "scope review record", "VERIFY", "INVALID")
                    scope_ref = {"path": s_rel, "sha256": core.sha256_bytes(s_data)}
                except Exception as exc:
                    raise _wrap_p2r(exc, "SCOPE") from exc
                res = p1mod._validate_scope(live, root_path, scope_review_path,
                                            proposal, state2, profile2)
                if res == p1mod.RESULT_BOUND:
                    outcome = RESULT_SCOPE_BOUND
                elif res == p1mod.RESULT_REQUIRED:
                    outcome = RESULT_NEEDS_SCOPE
                else:
                    raise _fail("SCOPE_INVALID", "SCOPE", f"unknown scope result: {res}")
                # scope_review_ref present when supplied ordinary valid review
                # read, even if NEEDS_SCOPE (contract §2).
        except CurrentAuthorityError:
            raise
        except Exception as exc:
            if isinstance(exc, p1mod.ProposalError):
                raise _wrap_p1(exc, "SCOPE") from exc
            raise _fail("SCOPE_FAILED", "SCOPE", f"scope binding failed: {exc}", cause=exc) from exc
        # Actual full receipt/current-tool recheck AFTER scope.
        try:
            p1mod._final_full_receipt_recheck(live, root_path, data, "observe")
        except Exception as exc:
            if isinstance(exc, p1mod.ProposalError):
                raise _wrap_p1(exc, "RECEIPT") from exc
            raise _fail("RECEIPT_FAILED", "RECEIPT", f"final receipt recheck failed: {exc}", cause=exc) from exc
        # Fresh retained revalidation after shared-data equality (bounded second
        # check; later helpers could have affected checked view).
        try:
            verified2 = retention.verify_retention(root_path, proposal_path, manifest_path)
        except Exception as exc:
            raise _wrap_p2r(exc, "RETAINED") from exc
        if verified2.get("proposal_sha256") != orig_proposal_sha or \
                verified2.get("manifest_sha256") != orig_manifest_sha:
            raise _fail("RETAINED_STABILITY", "RETAINED", "second retained verification SHA differs")

        # 7. Final boundary: ORIGINAL pins + ALL inputs/schemas/module/HEAD +
        #    full control/edition/retained dirs+files zero-delta, then closes.
        try:
            live.reverify()
        except Exception as exc:
            raise _wrap_p1(exc, "FINAL") from exc
        try:
            session.reverify("VERIFY", "INVALID")
        except Exception as exc:
            raise _wrap_p2r(exc, "FINAL") from exc
        try:
            ctrl_files2, ctrl_dirs2, ctrl_sizes2 = retention._snapshot_expanded(
                session, control_rels, "control", "VERIFY", "INVALID")
            src_files2, src_dirs2, src_sizes2 = retention._snapshot_expanded(
                session, [source_root_rel, survey_root_rel], "edition", "VERIFY", "INVALID")
            if (ctrl_files2, ctrl_dirs2, ctrl_sizes2) != (init_ctrl[0], init_ctrl[1], init_ctrl[2]):
                raise _fail("CONTROL_DRIFT", "FINAL", "control snapshot changed during call")
            if (src_files2, src_dirs2, src_sizes2) != (init_src[0], init_src[1], init_src[2]):
                raise _fail("EDITION_DRIFT", "FINAL", "edition snapshot changed during call")
            if p1mod._tree_map(root_path, Path(source_root_rel), Path(survey_root_rel)) != init_tree:
                raise _fail("TREE_MOVED", "FINAL", "edition tree changed during call")
            inv_files2, inv_dirs2, _ = retention._retained_inventory(
                session, retained_rel, "VERIFY", "INVALID")
            if set(inv_files2) != exp_files_set or set(inv_dirs2) != exp_dirs_set:
                raise _fail("INVALID_RETENTION", "FINAL", "final retained inventory drifted")
            # Schemas + P1/P2V source deps pinned (no resnapshot laundering).
            for dep in (PROPOSAL_SCHEMA.as_posix(), MANIFEST_SCHEMA.as_posix(),
                        Path("scripts/survey_editorial_correction_proposal_v2.py").as_posix(),
                        Path("scripts/survey_editorial_current_authority_v2.py").as_posix()):
                session.safe_read(dep, "source dep", "VERIFY", "INVALID")
            if _sanitized_head(root_path, "FINAL") != orig_head:
                raise _fail("HEAD_MOVED", "FINAL", "HEAD changed during inspection")
            if live.head != orig_head:
                raise _fail("HEAD_MOVED", "FINAL", "collector HEAD changed during inspection")
        except CurrentAuthorityError:
            raise
        except Exception as exc:
            if isinstance(exc, retention.RetentionError):
                raise _wrap_p2r(exc, "FINAL") from exc
            raise _fail("FINAL_FAILED", "FINAL", f"final boundary failed: {exc}", cause=exc) from exc
        # Checked closes before success (primary-preserving).
        try:
            session._close_all("VERIFY", "VERIFIED")
        except Exception as exc:
            raise _fail("CLOSE_FAILED", "CLOSE", f"descriptor close failed: {exc}", cause=exc) from exc

        # Build observation (measured, not copied into agreement).
        graph = data.get("graph") or {}
        copy_n = int(checked.get("copy_files", 0))
        keep_n = int(checked.get("keep_refs", 0))
        plan_copy = sum(1 for r in (data["proposal"].get("retention_plan") or [])
                        if r.get("policy") == "COPY_BEFORE_REPLACEMENT")
        plan_keep = sum(1 for r in (data["proposal"].get("retention_plan") or [])
                        if r.get("policy") == "KEEP_IMMUTABLE")
        if copy_n != plan_copy or keep_n != plan_keep:
            raise _fail("MEASURED_MISMATCH", "FINAL", "P2R counts != live plan counts")
        live_hashes = {rel: core.sha256_bytes(b) for rel, b in live.files.items()}
        ret_hashes = {rel: core.sha256_bytes(b) for rel, b in session.files.items()}
        merged: dict[str, str] = dict(live_hashes)
        for rel, sha in ret_hashes.items():
            if rel in merged and merged[rel] != sha:
                raise _fail("INPUT_HASH_CONFLICT", "FINAL", f"live/retained hash conflict: {rel}")
            merged[rel] = sha
        # Repo-rel refs from ORIGINAL pins (no resnapshot).
        def _rel_of(p: str | Path) -> str:
            return Path(p).resolve().relative_to(root_path).as_posix() \
                if Path(p).is_absolute() else str(p)
        try:
            state_rel_final = _rel_of(state_path)
            prop_rel_final = _rel_of(proposal_path)
            man_rel_final = _rel_of(manifest_path)
        except ValueError as exc:
            raise _fail("PATH_NOT_REPO_LOCAL", "FINAL", f"ref outside repo: {exc}", cause=exc) from exc
        # No producer-extras blanket check: capture_inputs historical extras are
        # NOT re-proven as current authority (contract §4.7).
        return {
            "result": outcome,
            "state_ref": {"path": state_rel_final,
                          "sha256": core.sha256_bytes(live.files[state_rel_final])},
            "proposal_ref": {"path": prop_rel_final, "sha256": orig_proposal_sha},
            "retention_manifest_ref": {"path": man_rel_final, "sha256": orig_manifest_sha},
            "scope_review_ref": scope_ref,
            "observed_head": orig_head,
            "measured": {
                "before_graph_digest": data["proposal"]["basis"]["before_graph_digest"],
                "preserved_upstream_digest": data["proposal"]["basis"]["preserved_upstream_digest"],
                "proposed_reader_sha256": core.sha256_bytes(data["proposed_canonical"]),
                "graph_nodes": len(graph.get("nodes", [])),
                "graph_edges": len(graph.get("edges", [])),
                "copy_files": copy_n,
                "keep_refs": keep_n,
            },
            "input_hashes": merged,
        }
    except CurrentAuthorityError:
        try:
            if session is not None and not getattr(session, "_closed", True):
                try:
                    session._close_all("VERIFY", "INVALID")
                except Exception:
                    pass
        except Exception:
            pass
        raise
    except Exception as exc:
        try:
            if session is not None and not getattr(session, "_closed", True):
                try:
                    session._close_all("VERIFY", "INVALID")
                except Exception:
                    pass
        except Exception:
            pass
        if isinstance(exc, (p1mod.ProposalError,)):
            raise _wrap_p1(exc, "FINAL") from exc
        if isinstance(exc, (retention.RetentionError,)):
            raise _wrap_p2r(exc, "FINAL") from exc
        raise _fail("OBSERVER_FAILED", "FINAL", f"unexpected observer failure: {exc}", cause=exc) from exc
