#!/usr/bin/env python3
"""Materialize a reviewed complete Longform reader input into exact publication source.

Initial LONGFORM_GENERATED_V1 two-pass entry (LF-2I). Pass 1 writes only the
canonical reader input; pass 2 requires an already materialized exact reader
input plus an independently validated persisted PASS semantic review, then
materializes same-input main.tex / references.bib / copied style / authoring
archive / source receipt. No default call into the legacy writer, no legacy
dispatcher, no pending-regeneration or changed-output renewal.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from scripts import survey_longform_derivation_v2 as derivation
from scripts import survey_longform_generated_v2 as generated
from scripts import survey_production_v2 as core
from scripts import survey_reader_surface_gate_v2 as surface_gate
from scripts import survey_schema_v2 as schema_gate


def _lexical_join(root_resolved: Path, raw: str | Path) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    return root_resolved / path


def _check_ancestors(root_resolved: Path, lexical: Path, label: str, raw: object) -> None:
    try:
        rel_parent = lexical.parent.relative_to(root_resolved)
    except ValueError:
        raise ValueError(f"{label} escapes repository: {raw}")
    current = root_resolved
    for part in rel_parent.parts:
        if part in ("..", ".", ""):
            raise ValueError(f"{label} has unsafe path component: {part}")
        current = current / part
        if current.is_symlink():
            raise ValueError(f"{label} has symlinked ancestor component: {current}")


def _safe(root: Path, raw: str | Path, label: str) -> Path:
    # Raw-first leaf/ancestor checks retained until complete: explicit
    # State/input/review leaf aliases (including dangling) refuse before any
    # resolve; ancestors refuse before resolve; resolved containment follows.
    import os as _os

    root_resolved = root.resolve()
    lexical = Path(raw) if Path(raw).is_absolute() else (root_resolved / Path(raw))
    try:
        lexical.relative_to(root_resolved)
    except ValueError:
        raise ValueError(f"{label} escapes repository: {raw}")
    for part in lexical.relative_to(root_resolved).parts:
        if part in ("..", ".", ""):
            raise ValueError(f"{label} has unsafe path component: {part}")
    _check_ancestors(root_resolved, lexical, label, raw)
    if _os.path.islink(lexical):
        raise ValueError(f"{label} leaf alias is unsafe: {raw}")
    resolved = lexical.resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository: {raw}") from exc
    if resolved.is_symlink() or not resolved.is_file():
        raise ValueError(f"{label} missing or unsafe: {raw}")
    return resolved


def _resolve_contained(root: Path, raw: str | Path, label: str) -> Path:
    # Narrow shared-in-module contained-path check: raw lexical leaf alias
    # (including dangling) refuses before resolve; ancestors refuse before
    # resolve; resolved containment follows. Callers still check
    # is_file/is_symlink on the returned physical path without re-resolving
    # away alias information (the leaf check already ran on the lexical path).
    import os as _os

    root_resolved = root.resolve()
    lexical = Path(raw) if Path(raw).is_absolute() else (root_resolved / Path(raw))
    try:
        lexical.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository: {raw}") from exc
    for part in lexical.relative_to(root_resolved).parts:
        if part in ("..", ".", ""):
            raise ValueError(f"{label} has unsafe path component: {part}")
    _check_ancestors(root_resolved, lexical, label, raw)
    if _os.path.islink(lexical):
        raise ValueError(f"{label} leaf alias is unsafe: {raw}")
    resolved = lexical.resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository: {raw}") from exc
    return resolved


def _strict_dir_preflight(root: Path, raw: str | Path, label: str) -> Path:
    # Directory preflight BEFORE any mkdir: leaf alias (including dangling),
    # symlinked ancestors, traversal and escapes refuse. Returns lexical dir.
    import os as _os

    root_resolved = root.resolve()
    lexical = Path(raw) if Path(raw).is_absolute() else (root_resolved / Path(raw))
    try:
        lexical.relative_to(root_resolved)
    except ValueError:
        raise ValueError(f"{label} escapes repository: {raw}")
    for part in lexical.relative_to(root_resolved).parts:
        if part in ("..", ".", ""):
            raise ValueError(f"{label} has unsafe path component: {part}")
    _check_ancestors(root_resolved, lexical, label, raw)
    if _os.path.islink(lexical):
        raise ValueError(f"{label} leaf alias is unsafe: {raw}")
    resolved = lexical.resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository: {raw}") from exc
    return lexical


def _rel(root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")


def _write_bytes_exclusive(path: Path, data: bytes, label: str) -> None:
    # Retained-partial policy: no silent deletion/repair. On write/close
    # failure the owned partial file (including the currently failing path) is
    # retained and reported by the caller; this helper never unlinks.
    if os.path.lexists(path):
        raise ValueError(f"refusing existing Longform publication artifact: {path}")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
    except BaseException:
        # Intentionally retain the partial file for inspection; the caller
        # records the failing path in its retained list and refuses receipt
        # success. No unlink, no repair, no crash-atomicity claim.
        raise


def _write_json_exclusive(path: Path, value: Any) -> None:
    _write_bytes_exclusive(path, core.json_bytes(value), "Longform publication artifact")


def _snapshot_inputs(root: Path, context: dict[str, Any], input_raw: bytes,
                     surface: dict[str, Any], review_path: Path | None) -> dict[str, Any]:
    snap: dict[str, Any] = {
        "state_sha256": core.sha256_file(context["state_path"]),
        "accepted_refs": [dict(row) for row in context["accepted_refs"]],
        "authored_sha256": core.sha256_bytes(input_raw),
        "surface_canonical_sha256": core.sha256_bytes(derivation.canonical_reader_bytes(surface)),
        "closure": generated.current_closure(root),
        "commit": core.repository_commit_sha(root),
    }
    if review_path is not None:
        snap["review_sha256"] = core.sha256_file(review_path)
    return snap


def _recheck_snapshot(root: Path, context: dict[str, Any], input_raw: bytes,
                      surface: dict[str, Any], review_path: Path | None,
                      snap: dict[str, Any], stage: str) -> None:
    if core.sha256_file(context["state_path"]) != snap["state_sha256"]:
        raise ValueError(f"Longform pre-write State drift detected {stage}")
    for row in snap["accepted_refs"]:
        path = _safe(root, row["path"], row["name"])
        if core.sha256_file(path) != row["sha256"]:
            raise ValueError(f"Longform accepted authority drift {stage}: {row['name']}")
    if core.sha256_bytes(input_raw) != snap["authored_sha256"]:
        raise ValueError(f"Longform authored input drift {stage}")
    if core.sha256_bytes(derivation.canonical_reader_bytes(surface)) != snap["surface_canonical_sha256"]:
        raise ValueError(f"Longform reader derivation drift {stage}")
    if review_path is not None:
        if core.sha256_file(review_path) != snap.get("review_sha256"):
            raise ValueError(f"Longform semantic review drift {stage}")
    current_closure = generated.current_closure(root)
    if current_closure != snap["closure"]:
        raise ValueError(f"Longform current-tool closure drift {stage}")
    if core.repository_commit_sha(root) != snap["commit"]:
        raise ValueError(f"Longform implementation commit drift {stage}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--state", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--semantic-review", default=None)
    parser.add_argument("--materialize-surface-only", action="store_true")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    try:
        state_path = _safe(root, args.state, "Production State")
        input_path = _safe(root, args.input, "semantic publication input")
    except ValueError as exc:
        raise SystemExit(f"Longform publication input containment invalid: {exc}") from exc
    try:
        context = derivation.load_derivation(root, state_path, input_path)
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Longform derivation invalid: {exc}") from exc
    surface = context["surface"]
    # Exact raw input-byte snapshot from the validated file (not re-canonicalized).
    try:
        input_raw_bytes = input_path.read_bytes()
        if core.sha256_bytes(input_raw_bytes) != core.sha256_file(input_path):
            raise ValueError("authored input byte snapshot inconsistent")
    except OSError as exc:
        raise SystemExit(f"Longform authored input snapshot invalid: {exc}") from exc
    publication_root = context["source_root"] / "publication" / "v2"
    surface_path = publication_root / "reader-surface-input-v2.json"
    try:
        findings = surface_gate.scan_structured_reader_surface(surface, _rel(root, surface_path))
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Pre-TeX Longform reader-surface scan invalid: {exc}") from exc
    blocking = [row for row in findings if row.severity == "BLOCKING" and row.disposition == "UNRESOLVED"]
    if blocking:
        first = blocking[0]
        raise SystemExit(
            f"Pre-TeX reader-facing validation FAILED: {first.artifact} leaks production metadata: "
            f"{first.text_span!r} ({first.reason})"
        )
    # Finite heading/optional-arg delimiter safety BEFORE any mkdir/write.
    try:
        generated.validate_heading_syntax(surface)
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Longform heading syntax invalid: {exc}") from exc
    # Derive all output bytes in memory + closure/tool/build-dir preflight
    # BEFORE any mkdir/output write (R1: mkdir must not precede predictable errors).
    try:
        main_text_pre = generated.render_main(surface)
        bibliography_text_pre = generated.render_bibliography(surface)
        style_bytes_pre = (root / generated.STYLE_PATH).read_bytes()
        generated.validate_generated_closure(main_text_pre, style_bytes_pre.decode("utf-8"))
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Longform source derivation invalid: {exc}") from exc
    try:
        generated.verify_tool_basis(root, {
            "repository_commit_sha": core.repository_commit_sha(root),
            "closure": generated.current_closure(root),
        })
    except ValueError as exc:
        raise SystemExit(f"Longform current implementation basis invalid: {exc}") from exc
    try:
        survey_root_pre = generated.validate_survey_build_directory(
            root, context["profile"]["paths"]["survey_root"]
        )
    except ValueError as exc:
        raise SystemExit(f"Longform publication build directory invalid: {exc}") from exc
    # Publication output directory alias preflight BEFORE any mkdir/write.
    try:
        _strict_dir_preflight(root, _rel(root, publication_root), "Longform publication output directory")
    except ValueError as exc:
        raise SystemExit(f"Longform publication output directory invalid: {exc}") from exc
    # Prospective receipt schema preflight inputs (pass2 only validated after
    # review; pass1 still preflights output refs for eligibility).
    survey_root = survey_root_pre
    primary_path = survey_root / "main.tex"
    bibliography_path = survey_root / "references.bib"
    style_path = survey_root / "jgaisurvey.sty"
    receipt_path = publication_root / "validated-source-manifest.json"
    archived_input = publication_root / "interactive-semantic-publication-input.json"

    is_pass1 = bool(args.materialize_surface_only)
    surface_exists = os.path.lexists(surface_path)
    if not is_pass1:
        # R1: pass2 requires an already materialized exact reader input; absence
        # refuses without silently doing pass1, with no writes.
        if not surface_exists or surface_path.is_symlink() or not surface_path.is_file():
            raise SystemExit(
                "Longform pass2 requires an already materialized exact reader input; "
                f"missing surface {surface_path}; refusing without silently doing pass1"
            )
        try:
            existing = derivation.validate_longform_reader_input(root, surface_path)
        except (OSError, ValueError) as exc:
            raise SystemExit(f"existing complete reader input invalid: {exc}") from exc
        if core.sha256_file(surface_path) != core.sha256_bytes(derivation.canonical_reader_bytes(surface)):
            raise SystemExit("existing complete reader input differs from current independent derivation")
        if existing != surface:
            raise SystemExit("existing complete reader input differs from current independent derivation")
        # Exact raw surface bytes must equal canonical derivation (no noncanonical reuse).
        if surface_path.read_bytes() != derivation.canonical_reader_bytes(surface):
            raise SystemExit("existing complete reader input bytes differ from canonical derivation")
    else:
        # Pass1: preflight survey eligibility BEFORE surface mkdir/write.
        # Undeclared survey entries refuse before any surface write; pre-existing
        # partial/full source outputs refuse a fresh surface write (same-byte
        # reuse with existing surface remains permitted below).
        if surface_exists:
            if surface_path.is_symlink() or not surface_path.is_file():
                raise SystemExit(f"existing complete reader input missing or unsafe: {surface_path}")
            try:
                existing = derivation.validate_longform_reader_input(root, surface_path)
            except (OSError, ValueError) as exc:
                raise SystemExit(f"existing complete reader input invalid: {exc}") from exc
            if core.sha256_file(surface_path) != core.sha256_bytes(derivation.canonical_reader_bytes(surface)):
                raise SystemExit("existing complete reader input differs from current independent derivation")
            if existing != surface:
                raise SystemExit("existing complete reader input differs from current independent derivation")
            if surface_path.read_bytes() != derivation.canonical_reader_bytes(surface):
                raise SystemExit("existing complete reader input bytes differ from canonical derivation")
        else:
            for path in (primary_path, bibliography_path, style_path, receipt_path, archived_input):
                if os.path.lexists(path):
                    raise SystemExit(
                        f"refusing fresh Longform surface write with pre-existing partial output: {path}"
                    )

    if is_pass1:
        if not surface_exists:
            try:
                _strict_dir_preflight(root, _rel(root, publication_root), "Longform publication output directory")
            except ValueError as exc:
                raise SystemExit(f"Longform publication output directory invalid: {exc}") from exc
            publication_root.mkdir(parents=True, exist_ok=True)
            try:
                _write_bytes_exclusive(surface_path, derivation.canonical_reader_bytes(surface), "reader surface")
            except (OSError, ValueError) as exc:
                raise SystemExit(
                    f"Longform surface materialization failed; retained owned partial outputs [], "
                    f"no silent deletion or repair was performed: {exc}"
                ) from exc
            if surface_path.read_bytes() != derivation.canonical_reader_bytes(surface):
                raise SystemExit(
                    "Longform installed surface inconsistent with pre-write snapshot; "
                    "retained owned partial output for inspection, no repair performed"
                )
        print(json.dumps({
            "issue_id": surface["issue_id"], "structured_surface": _rel(root, surface_path),
            "surface_sha256": core.sha256_file(surface_path), "status": "SURFACE_MATERIALIZED",
        }, ensure_ascii=False, indent=2))
        return 0

    if args.semantic_review:
        try:
            review_path = _resolve_contained(root, args.semantic_review, "semantic review record")
        except ValueError as exc:
            raise SystemExit(f"Pre-TeX semantic review path invalid: {exc}") from exc
    else:
        review_path = publication_root / "reader-surface-semantic-review-v2.json"
    # Raw leaf alias refusal for review BEFORE any write (resolved path retains
    # no alias info, so lexical check already ran in _resolve_contained for the
    # explicit case; default sibling still needs explicit leaf check).
    if os.path.islink(review_path):
        raise SystemExit(f"Pre-TeX semantic review leaf alias is unsafe: {review_path}")
    if not review_path.is_file() or review_path.is_symlink():
        raise SystemExit(
            f"Pre-TeX semantic review artifact missing on disk: {review_path}; "
            "TeX/BibTeX/style materialization prohibited until semantic review PASS"
        )
    try:
        validated = surface_gate.load_and_validate_reader_surface_semantic_review(
            root, review_path, expected_issue_id=surface["issue_id"],
            expected_publication_profile="LONGFORM_SPECIAL", expected_surface_path=surface_path,
            expected_surface_sha256=core.sha256_file(surface_path), require_pass=True,
        )
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Pre-TeX semantic review validation FAILED: {exc}") from exc
    # Prospective receipt/schema/preflight BEFORE any source mkdir/write.
    try:
        snap_pre = _snapshot_inputs(root, context, input_raw_bytes, surface, review_path)
        _recheck_snapshot(root, context, input_raw_bytes, surface, review_path, snap_pre, "pre-write")
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Longform pre-write snapshot invalid: {exc}") from exc
    try:
        prospective = {
            "schema_version": "2.0-rc1", "issue_id": context["state"]["issue_id"],
            "route": generated.ROUTE, "status": "ESTABLISHED",
            "production_state_basis": {
                "path": _rel(root, context["state_path"]),
                "historical_sha256": core.sha256_file(context["state_path"]),
                "lifecycle_state": context["state"]["lifecycle_state"],
            },
            "accepted_refs": context["accepted_refs"],
            "authored_refs": [
                {"name": "publication-semantic-input",
                 "path": _rel(root, archived_input),
                 "sha256": core.sha256_bytes(input_raw_bytes)},
                {"name": "drafting-authored-archive",
                 "path": _rel(root, context["archive_path"]),
                 "sha256": core.sha256_file(context["archive_path"])},
            ],
            "reviewed_reader_input": {"path": _rel(root, surface_path),
                                      "sha256": core.sha256_file(surface_path)},
            "semantic_review": {"path": _rel(root, review_path),
                                "sha256": core.sha256_file(review_path)},
            "current_tools": {
                "repository_commit_sha": core.repository_commit_sha(root),
                "contract": core.contract_identity(root, core.load_json(root / core.DEFAULT_CONFIG),
                                                   "THEMATIC", "LONGFORM_SPECIAL"),
                "closure": generated.current_closure(root),
            },
            "outputs": {
                "primary": {"path": _rel(root, primary_path),
                            "sha256": core.sha256_bytes(main_text_pre.encode("utf-8"))},
                "bibliography": {"path": _rel(root, bibliography_path),
                                 "sha256": core.sha256_bytes(bibliography_text_pre.encode("utf-8"))},
                "style": {"path": _rel(root, style_path),
                          "sha256": core.sha256_bytes(style_bytes_pre)},
            },
        }
        prospective["receipt_sha256"] = core.sha256_object(
            {k: v for k, v in prospective.items() if k != "receipt_sha256"})
        schema_gate.validate_instance(prospective, root / generated.RECEIPT_SCHEMA,
                                      label="Longform prospective source receipt")
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Longform prospective receipt invalid; no source writes performed: {exc}") from exc
    # All preflight passed: now create directories (validated lexical paths).
    publication_root.mkdir(parents=True, exist_ok=True)
    survey_root.mkdir(parents=True, exist_ok=True)
    try:
        survey_root = generated.validate_survey_build_directory(
            root, context["profile"]["paths"]["survey_root"]
        )
    except ValueError as exc:
        raise SystemExit(f"Longform publication build directory invalid: {exc}") from exc
    primary_path = survey_root / "main.tex"
    bibliography_path = survey_root / "references.bib"
    style_path = survey_root / "jgaisurvey.sty"
    for path in (primary_path, bibliography_path, style_path, receipt_path, archived_input):
        if os.path.lexists(path):
            raise SystemExit(f"refusing existing Longform publication artifact: {path}")

    main_text = main_text_pre
    bibliography_text = bibliography_text_pre
    style_bytes = style_bytes_pre
    planned = {
        "surface_sha256": core.sha256_bytes(derivation.canonical_reader_bytes(surface)),
        "review_sha256": core.sha256_file(review_path),
        "authored_sha256": core.sha256_bytes(input_raw_bytes),
        "archive_planned_sha256": core.sha256_bytes(input_raw_bytes),
        "main_sha256": core.sha256_bytes(main_text.encode("utf-8")),
        "bibliography_sha256": core.sha256_bytes(bibliography_text.encode("utf-8")),
        "style_sha256": core.sha256_bytes(style_bytes),
    }
    # Recheck all named snapshots immediately before writes.
    try:
        _recheck_snapshot(root, context, input_raw_bytes, surface, review_path, snap_pre, "before-writes")
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Longform snapshot recheck failed before writes; no writes performed: {exc}") from exc
    written: list[str] = []
    failing: str | None = None
    try:
        try:
            _write_bytes_exclusive(primary_path, main_text.encode("utf-8"), "primary source")
        except (OSError, ValueError) as exc:
            failing = _rel(root, primary_path)
            raise
        written.append(_rel(root, primary_path))
        try:
            _write_bytes_exclusive(bibliography_path, bibliography_text.encode("utf-8"), "bibliography")
        except (OSError, ValueError) as exc:
            failing = _rel(root, bibliography_path)
            raise
        written.append(_rel(root, bibliography_path))
        try:
            _write_bytes_exclusive(style_path, style_bytes, "style")
        except (OSError, ValueError) as exc:
            failing = _rel(root, style_path)
            raise
        written.append(_rel(root, style_path))
        try:
            _write_bytes_exclusive(archived_input, input_raw_bytes, "authored archive")
        except (OSError, ValueError) as exc:
            failing = _rel(root, archived_input)
            raise
        written.append(_rel(root, archived_input))
    except (OSError, ValueError) as exc:
        retained = written + ([failing] if failing and failing not in written else [])
        raise SystemExit(
            f"Longform source materialization failed; retained owned partial outputs {retained}, "
            f"no silent deletion or repair was performed: {exc}"
        ) from exc
    if (
        core.sha256_file(primary_path) != planned["main_sha256"]
        or core.sha256_file(bibliography_path) != planned["bibliography_sha256"]
        or core.sha256_file(style_path) != planned["style_sha256"]
        or core.sha256_file(archived_input) != planned["archive_planned_sha256"]
    ):
        raise SystemExit(
            f"Longform installed source inconsistent with pre-write snapshot; "
            f"retained owned partial outputs {written} for inspection, no repair performed"
        )
    # Recheck snapshots immediately before final receipt install; no receipt
    # success on post-write drift.
    try:
        _recheck_snapshot(root, context, input_raw_bytes, surface, review_path, snap_pre, "before-receipt")
    except (OSError, ValueError) as exc:
        raise SystemExit(
            f"Longform snapshot recheck failed before receipt; retained owned partial outputs {written}, "
            f"receipt was not installed: {exc}"
        ) from exc
    receipt_context = dict(context)
    receipt_context["authored_path"] = archived_input
    try:
        receipt = generated.build_receipt(
            root, receipt_context, surface_path, review_path, primary_path, bibliography_path, style_path
        )
        schema_gate.validate_instance(receipt, root / generated.RECEIPT_SCHEMA, label="Longform source receipt")
    except (OSError, ValueError) as exc:
        raise SystemExit(
            f"Longform source receipt invalid; retained owned partial outputs {written}, "
            f"receipt was not installed: {exc}"
        ) from exc
    try:
        _write_bytes_exclusive(receipt_path, core.json_bytes(receipt), "source receipt")
    except (OSError, ValueError) as exc:
        raise SystemExit(
            f"Longform source receipt installation failed; retained owned partial outputs {written}: {exc}"
        ) from exc
    print(json.dumps({
        "issue_id": surface["issue_id"], "source_root": _rel(root, context["source_root"]),
        "survey_root": _rel(root, survey_root), "source_manifest": _rel(root, receipt_path),
        "main_tex": _rel(root, primary_path), "bibliography": _rel(root, bibliography_path),
        "style": _rel(root, style_path),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
