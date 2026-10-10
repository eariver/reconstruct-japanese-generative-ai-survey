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


def _safe(root: Path, raw: str | Path, label: str) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = root / path
    resolved = path.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository: {raw}") from exc
    if resolved.is_symlink() or not resolved.is_file():
        raise ValueError(f"{label} missing or unsafe: {raw}")
    return resolved


def _resolve_contained(root: Path, raw: str | Path, label: str) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = root / path
    root_resolved = root.resolve()
    current = root_resolved
    try:
        rel_parent = (path if path.is_absolute() else root_resolved / path).parent.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository: {raw}") from exc
    for part in rel_parent.parts:
        if part in ("..", ".", ""):
            raise ValueError(f"{label} has unsafe path component: {part}")
        current = current / part
        if current.is_symlink():
            raise ValueError(f"{label} has symlinked ancestor component: {current}")
    resolved = path.resolve()
    try:
        resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"{label} escapes repository: {raw}") from exc
    return resolved


def _rel(root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")


def _write_bytes_exclusive(path: Path, data: bytes, label: str) -> None:
    if os.path.lexists(path):
        raise ValueError(f"refusing existing Longform publication artifact: {path}")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
    except BaseException:
        try:
            os.unlink(path)
        except OSError:
            pass
        raise


def _write_json_exclusive(path: Path, value: Any) -> None:
    _write_bytes_exclusive(path, core.json_bytes(value), "Longform publication artifact")


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
    if surface_path.exists():
        try:
            existing = derivation.validate_longform_reader_input(root, surface_path)
        except (OSError, ValueError) as exc:
            raise SystemExit(f"existing complete reader input invalid: {exc}") from exc
        if core.sha256_file(surface_path) != core.sha256_bytes(derivation.canonical_reader_bytes(surface)):
            raise SystemExit("existing complete reader input differs from current independent derivation")
        if existing != surface:
            raise SystemExit("existing complete reader input differs from current independent derivation")
    else:
        publication_root.mkdir(parents=True, exist_ok=True)
        try:
            _write_json_exclusive(surface_path, surface)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc

    if args.materialize_surface_only:
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
    if not review_path.is_file() or review_path.is_symlink():
        raise SystemExit(
            f"Pre-TeX semantic review artifact missing on disk: {review_path}; "
            "TeX/BibTeX/style materialization prohibited until semantic review PASS"
        )
    try:
        surface_gate.load_and_validate_reader_surface_semantic_review(
            root, review_path, expected_issue_id=surface["issue_id"],
            expected_publication_profile="LONGFORM_SPECIAL", expected_surface_path=surface_path,
            expected_surface_sha256=core.sha256_file(surface_path), require_pass=True,
        )
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Pre-TeX semantic review validation FAILED: {exc}") from exc

    # Reject a dirty or mismatched current implementation before creating any
    # TeX, bibliography, copied style, archive, or receipt output.
    try:
        generated.verify_tool_basis(root, {
            "repository_commit_sha": core.repository_commit_sha(root),
            "closure": generated.current_closure(root),
        })
    except ValueError as exc:
        raise SystemExit(f"Longform current implementation basis invalid: {exc}") from exc

    try:
        survey_root = generated.validate_survey_build_directory(
            root, context["profile"]["paths"]["survey_root"]
        )
    except ValueError as exc:
        raise SystemExit(f"Longform publication build directory invalid: {exc}") from exc
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
    receipt_path = publication_root / "validated-source-manifest.json"
    archived_input = publication_root / "interactive-semantic-publication-input.json"
    for path in (primary_path, bibliography_path, style_path, receipt_path, archived_input):
        if os.path.lexists(path):
            raise SystemExit(f"refusing existing Longform publication artifact: {path}")

    try:
        main_text = generated.render_main(surface)
        bibliography_text = generated.render_bibliography(surface)
        style_bytes = (root / generated.STYLE_PATH).read_bytes()
        generated.validate_generated_closure(main_text, style_bytes.decode("utf-8"))
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Longform source derivation invalid: {exc}") from exc
    # Exact pre-write snapshot: predictable failure from here must leave the
    # source window untouched, and every installed byte must match it.
    planned = {
        "surface_sha256": core.sha256_bytes(derivation.canonical_reader_bytes(surface)),
        "review_sha256": core.sha256_file(review_path),
        "authored_sha256": core.sha256_file(input_path),
        "archive_planned_sha256": core.sha256_bytes(core.json_bytes(core.load_json(input_path))),
        "main_sha256": core.sha256_bytes(main_text.encode("utf-8")),
        "bibliography_sha256": core.sha256_bytes(bibliography_text.encode("utf-8")),
        "style_sha256": core.sha256_bytes(style_bytes),
    }
    written: list[str] = []
    try:
        _write_bytes_exclusive(primary_path, main_text.encode("utf-8"), "primary source")
        written.append(_rel(root, primary_path))
        _write_bytes_exclusive(bibliography_path, bibliography_text.encode("utf-8"), "bibliography")
        written.append(_rel(root, bibliography_path))
        _write_bytes_exclusive(style_path, style_bytes, "style")
        written.append(_rel(root, style_path))
        _write_json_exclusive(archived_input, core.load_json(input_path))
        written.append(_rel(root, archived_input))
    except (OSError, ValueError) as exc:
        raise SystemExit(
            f"Longform source materialization failed; retained owned partial outputs {written}, "
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
        _write_json_exclusive(receipt_path, receipt)
    except ValueError as exc:
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
