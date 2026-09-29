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


def _exclusive_bytes(path: Path, data: bytes, label: str) -> None:
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


def _atomic_replace(path: Path, data: bytes, label: str, run_id: str) -> None:
    if path.is_symlink() or not path.is_file():
        raise MechanicalRefreshError(f"refresh {label} missing or unsafe: {path}")
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
    if core.sha256_bytes(tmp.read_bytes()) != core.sha256_bytes(data):
        tmp.unlink(missing_ok=True)
        raise MechanicalRefreshError(f"refresh {label} temp bytes mismatch")
    os.replace(tmp, path)


def _receipt_paths(root: Path, surface_rel: str) -> Path:
    surface_path = core.repo_local_path(root, surface_rel, "reviewed reader input")
    receipt_path = surface_path.parent / RECEIPT_FILENAME
    if receipt_path.name != RECEIPT_FILENAME:
        raise MechanicalRefreshError("receipt path is not canonical")
    return receipt_path


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
    try:
        state_path = core.repo_local_path(root, _rel(root, state_path), "Production State")
    except (TypeError, ValueError) as exc:
        raise MechanicalRefreshError(str(exc)) from exc
    if state_path.is_symlink() or not state_path.is_file():
        raise MechanicalRefreshError("refresh State missing or unsafe")
    state = core.load_json(state_path)
    head = core.repository_commit_sha(root)
    state_sha_p0 = core.sha256_file(state_path)

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
    checkpoint_path = core.repo_local_path(root, validation_ref["path"], "validation checkpoint")
    if checkpoint_path.is_symlink() or core.sha256_file(checkpoint_path) != validation_ref["sha256"]:
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
    manuscript_path = core.repo_local_path(root, manuscript_rel, "refresh manuscript")

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

    gate_path = core.repo_local_path(root, gate_rel, "refresh Gate")
    if gate_path.is_symlink() or not gate_path.is_file():
        raise MechanicalRefreshError("refresh Gate missing or unsafe")
    old_gate_bytes = gate_path.read_bytes()
    if core.sha256_bytes(old_gate_bytes) != old_gate_sha:
        raise MechanicalRefreshError("live Gate differs from strict checkpoint/active effective row")

    inspected = surface_gate._inspect_gate_record(
        root, gate_path, expected_manuscript_path=manuscript_path
    )
    old_gate = inspected["payload"]
    if old_gate.get("derivation", {}).get("scope") != "WEEKLY_MAIN_BIB_STYLE":
        raise MechanicalRefreshError("refresh supports only WEEKLY_MAIN_BIB_STYLE Gate scope")
    receipt_ref = old_gate.get("derivation", {}).get("receipt")
    if not isinstance(receipt_ref, dict) or set(receipt_ref) != {"path", "sha256"}:
        raise MechanicalRefreshError("old Gate derivation receipt authority fields invalid")
    old_receipt_path = core.repo_local_path(root, receipt_ref["path"], "refresh old receipt")
    if old_receipt_path.is_symlink() or not old_receipt_path.is_file():
        raise MechanicalRefreshError("refresh old receipt missing or unsafe")
    old_receipt_bytes = old_receipt_path.read_bytes()
    if core.sha256_bytes(old_receipt_bytes) != receipt_ref["sha256"]:
        raise MechanicalRefreshError("old receipt differs from bound Gate derivation reference")
    # Receipt must live next to the reviewed surface (Gate derivation §1093).
    envelope = weekly.inspect_receipt_envelope(root, old_receipt_path)
    old_receipt = envelope["receipt"]
    if old_receipt.get("route") != weekly.ROUTE or old_receipt.get("issue_id") != state.get("issue_id"):
        raise MechanicalRefreshError("old receipt route/issue mismatch")
    if old_receipt.get("reviewed_reader_input") != {
        "path": _rel(root, core.repo_local_path(root, old_receipt["reviewed_reader_input"]["path"], "reviewed reader input")),
        "sha256": core.sha256_file(
            core.repo_local_path(root, old_receipt["reviewed_reader_input"]["path"], "reviewed reader input")
        ),
    }:
        raise MechanicalRefreshError("old receipt reviewed input drift")
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

    # Same-edition equality: re-derive from accepted current inputs.
    authored_rel = old_receipt["authored_refs"][0]["path"]
    context = weekly.load_derivation(root, state_path, core.repo_local_path(root, authored_rel, "authored input"))
    if context["accepted_refs"] != old_receipt["accepted_refs"]:
        raise MechanicalRefreshError("accepted authority differs from bound receipt")
    reviewed_path = core.repo_local_path(root, old_receipt["reviewed_reader_input"]["path"], "reviewed reader input")
    reviewed = weekly.validate_reader_input(root, reviewed_path)
    if context["surface"] != reviewed:
        raise MechanicalRefreshError("independently recomputed reader input differs from reviewed bytes")
    # Manuscript / bundle / reviews / PDF unchanged (existing validators).
    reader.validate_manuscript_manifest(root, manuscript_path, issue_id=state["issue_id"])
    profile = context["profile"]
    bundle_rows = [k for k in ck_rows if k[0] == "quality-regression-bundle"]
    if not bundle_rows:
        raise MechanicalRefreshError("checkpoint lacks quality-regression-bundle row")
    bundle_doc = quality.validate_bundle(
        root, core.repo_local_path(root, bundle_rows[0][1], "quality bundle"), issue_id=state["issue_id"]
    )
    for _role, _kind in (("semantic-review", "SEMANTIC_EDITORIAL"), ("visual-review", "VISUAL")):
        rows = [k for k in ck_rows if k[0] == _role]
        if len(rows) != 1:
            raise MechanicalRefreshError(f"checkpoint must carry exactly one {_role} row")
        reader.validate_review_record(
            root, core.repo_local_path(root, rows[0][1], _role), issue_id=state["issue_id"], expected_kind=_kind
        )
    style_source = (root / weekly.STYLE_PATH).read_text(encoding="utf-8")
    main_text = weekly.render_main(reviewed)
    bib_text = weekly.render_bibliography(reviewed)
    weekly.validate_generated_closure(main_text, style_source)
    expected_render = {
        "primary": main_text.encode("utf-8"),
        "bibliography": bib_text.encode("utf-8"),
        "style": (root / weekly.STYLE_PATH).read_bytes(),
    }
    for _name, _data in expected_render.items():
        row = old_receipt["outputs"][_name]
        disk = core.repo_local_path(root, row["path"], f"refresh output {_name}")
        if disk.read_bytes() != _data or core.sha256_bytes(_data) != row["sha256"]:
            raise MechanicalRefreshError(f"rendered {_name} differs from bound receipt")

    # Prospective receipt (pre-retention comparison).
    review_rel = old_receipt["semantic_review"]["path"]
    review_path = core.repo_local_path(root, review_rel, "semantic review")
    receipt_context = dict(context)
    receipt_context["authored_path"] = core.repo_local_path(
        root, old_receipt["authored_refs"][0]["path"], "authored input"
    )
    new_receipt = weekly.build_receipt(
        root,
        receipt_context,
        reviewed_path,
        review_path,
        core.repo_local_path(root, old_receipt["outputs"]["primary"]["path"], "primary output"),
        core.repo_local_path(root, old_receipt["outputs"]["bibliography"]["path"], "bibliography output"),
        core.repo_local_path(root, old_receipt["outputs"]["style"]["path"], "style output"),
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

    # ---- P1 guard + retention ----
    publication_dir = reviewed_path.parent
    if publication_dir.name != "v2" or publication_dir.parent.name != "publication":
        raise MechanicalRefreshError("reviewed surface is not under canonical publication/v2")
    lock_path = publication_dir / LOCK_FILENAME
    if lock_path.is_symlink() or lock_path.exists():
        raise MechanicalRefreshError("cooperative refresh guard occupied")
    try:
        with open(lock_path, "xb") as fh:
            fh.write(core.json_bytes({"run_id": run_id, "head": head, "state_sha256": state_sha_p0}))
    except FileExistsError as exc:
        raise MechanicalRefreshError("cooperative refresh guard occupied") from exc
    owned_lock = True
    try:
        if core.sha256_file(state_path) != state_sha_p0 or core.repository_commit_sha(root) != head:
            raise MechanicalRefreshError("State/HEAD drift after guard acquisition")
        if core.sha256_bytes(gate_path.read_bytes()) != old_gate_sha or core.sha256_bytes(
            old_receipt_path.read_bytes()
        ) != receipt_ref["sha256"]:
            raise MechanicalRefreshError("live receipt/Gate drift after guard acquisition")
        retention_base = publication_dir / RETENTION_DIRNAME
        retention_base.mkdir(parents=True, exist_ok=True)
        run_dir = retention_base / run_id
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

        # ---- P2 receipt installation ----
        if core.sha256_file(state_path) != state_sha_p0 or core.repository_commit_sha(root) != head:
            raise MechanicalRefreshError("snapshot drift before receipt installation")
        _atomic_replace(old_receipt_path, new_receipt_bytes, "receipt", run_id)
        if core.sha256_file(old_receipt_path) != core.sha256_bytes(new_receipt_bytes):
            raise MechanicalRefreshError("installed receipt hash mismatch")
        weekly.validate_receipt(root, old_receipt_path)

        # ---- P3 Gate computation/installation (after new receipt) ----
        if core.sha256_file(state_path) != state_sha_p0 or core.repository_commit_sha(root) != head:
            raise MechanicalRefreshError("snapshot drift before Gate computation")
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
        for _key in ("scanned_surfaces", "rules_checked", "findings", "suppressions", "semantic_authority"):
            if _key == "semantic_authority":
                for _sk in ("status", "decision", "reviewed_by", "surface_sha256", "review_path", "review_sha256"):
                    if new_report["semantic_authority"].get(_sk) != old_gate["semantic_authority"].get(_sk):
                        raise MechanicalRefreshError(f"renewed Gate semantic_authority.{_sk} changed")
                continue
            if new_report.get(_key) != old_gate.get(_key):
                raise MechanicalRefreshError(f"renewed Gate {_key} changed")
        if new_report.get("derivation", {}).get("receipt") != {
            "path": _rel(root, old_receipt_path),
            "sha256": core.sha256_bytes(new_receipt_bytes),
        }:
            raise MechanicalRefreshError("renewed Gate receipt derivation mismatch")
        new_gate_bytes = core.json_bytes(new_report)
        _atomic_replace(gate_path, new_gate_bytes, "gate", run_id)
        if core.sha256_file(gate_path) != core.sha256_bytes(new_gate_bytes):
            raise MechanicalRefreshError("installed Gate hash mismatch")
        surface_gate.validate_reader_surface_gate(
            root, gate_path, expected_manuscript_path=manuscript_path, state_path=state_path
        )

        # ---- P4 revalidation/commit ----
        if core.sha256_file(state_path) != state_sha_p0 or core.repository_commit_sha(root) != head:
            raise MechanicalRefreshError("snapshot drift before revalidation")
        basis = agent.built_checked_pending_publication_basis(root, cfg, state_path)
        if len(basis.replacements) != 1 or basis.replacements[0][0] != "reader-surface-gate":
            raise MechanicalRefreshError("pending basis is not exactly the renewed Gate row")
        record_path = agent.revalidate_publication_surface(
            root, cfg, state_path, REASON_CLASS, reason, executor, recorded_at, head
        )
        final_active, final_errors = agent.resolve_active_publication_revalidation(root, cfg, core.load_json(state_path))
        if final_errors or final_active is None:
            raise MechanicalRefreshError("post-commit active readback invalid: " + "; ".join(final_errors))
    except Exception as exc:
        # Guarded restoration for caught failures before commit only.
        # Non-ValueError failures are wrapped so the CLI maps every failure
        # to exit 2 with its evidence; the original is preserved via chain.
        try:
            cur_state_ok = state_path.is_file() and core.sha256_file(state_path) == state_sha_p0
            cur_head_ok = core.repository_commit_sha(root) == head
            live_receipt = old_receipt_path.read_bytes() if old_receipt_path.is_file() else None
            live_gate = gate_path.read_bytes() if gate_path.is_file() else None
            receipt_known = live_receipt in (old_receipt_bytes, new_receipt_bytes)
            gate_known = live_gate in (old_gate_bytes, new_gate_bytes if "new_gate_bytes" in locals() else None)
            if cur_state_ok and cur_head_ok and receipt_known and gate_known:
                if live_receipt != old_receipt_bytes:
                    old_receipt_path.write_bytes(old_receipt_bytes)
                if live_gate != old_gate_bytes:
                    gate_path.write_bytes(old_gate_bytes)
                if core.sha256_file(old_receipt_path) != receipt_ref["sha256"] or core.sha256_file(
                    gate_path
                ) != old_gate_sha:
                    raise MechanicalRefreshError("restored owned bytes mismatch")
            else:
                raise MechanicalRefreshError(
                    "refresh failed with external drift; live bytes + retention + guard preserved for manual recovery"
                )
        finally:
            if owned_lock:
                try:
                    lock_path.unlink()
                except OSError:
                    pass
        if isinstance(exc, MechanicalRefreshError):
            raise
        raise MechanicalRefreshError(f"refresh failed: {exc}") from exc
    if owned_lock:
        try:
            lock_path.unlink()
        except OSError as exc:
            raise MechanicalRefreshError(f"refresh guard release failed: {exc}") from exc
    return {
        "state": _rel(root, state_path),
        "revalidation_record": _rel(root, record_path),
        "receipt": _rel(root, old_receipt_path),
        "gate": _rel(root, gate_path),
        "retention": _rel(root, run_dir),
        "supersedes": supersedes,
    }
