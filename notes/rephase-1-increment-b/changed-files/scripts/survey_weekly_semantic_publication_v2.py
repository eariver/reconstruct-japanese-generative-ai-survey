#!/usr/bin/env python3
"""Materialize a reviewed complete Weekly reader input into exact publication source."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts import survey_production_v2 as core
from scripts import survey_reader_surface_gate_v2 as surface_gate
from scripts import survey_schema_v2 as schema_gate
from scripts import survey_weekly_derivation_v2 as weekly


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


def _rel(root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")


def _write_json(path: Path, value: Any) -> None:
    if path.exists():
        raise ValueError(f"refusing to overwrite publication artifact: {path}")
    core.write_json(path, value)


def _identifier_tokens(surface: dict[str, Any], records: dict[str, dict[str, Any]]) -> list[str]:
    tokens = [surface["issue_id"]]
    for row in surface["bibliography"]:
        record = records[row["discovery_id"]]
        if record.get("materiality") != "MATERIAL":
            continue
        title = row["title"].strip()
        if title and title not in tokens:
            tokens.append(title)
        if len(tokens) >= 8:
            break
    return tokens


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--state", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--semantic-review", default=None)
    parser.add_argument("--materialize-surface-only", action="store_true")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    state_path = _safe(root, args.state, "Production State")
    input_path = _safe(root, args.input, "semantic publication input")
    state = core.load_json(state_path)
    if state.get("lifecycle_state") != "DRAFT_COMPLETE":
        raise SystemExit("semantic publication requires DRAFT_COMPLETE State")
    try:
        context = weekly.load_derivation(root, state_path, input_path)
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Weekly derivation invalid: {exc}") from exc
    surface = context["surface"]
    publication_root = context["source_root"] / "publication/v2"
    publication_root.mkdir(parents=True, exist_ok=True)
    surface_path = publication_root / "reader-surface-input-v2.json"
    if surface_path.exists():
        existing = weekly.validate_reader_input(root, surface_path)
        if existing != surface:
            raise SystemExit("existing complete reader input differs from current independent derivation")
    else:
        core.write_json(surface_path, surface)

    findings = surface_gate.scan_structured_reader_surface(surface, _rel(root, surface_path))
    blocking = [row for row in findings if row.severity == "BLOCKING" and row.disposition == "UNRESOLVED"]
    if blocking:
        first = blocking[0]
        raise SystemExit(
            f"Pre-TeX reader-facing validation FAILED: {first.artifact} leaks production metadata: "
            f"{first.text_span!r} ({first.reason})"
        )
    if args.materialize_surface_only:
        print(json.dumps({
            "issue_id": surface["issue_id"], "structured_surface": _rel(root, surface_path),
            "surface_sha256": core.sha256_file(surface_path), "status": "SURFACE_MATERIALIZED",
        }, ensure_ascii=False, indent=2))
        return 0

    review_path = Path(args.semantic_review) if args.semantic_review else publication_root / "reader-surface-semantic-review-v2.json"
    if not review_path.is_absolute():
        review_path = root / review_path
    if not review_path.is_file() or review_path.is_symlink():
        raise SystemExit(
            f"Pre-TeX semantic review artifact missing on disk: {review_path}; "
            "TeX/BibTeX/style materialization prohibited until semantic review PASS"
        )
    try:
        surface_gate.load_and_validate_semantic_review(
            root, review_path, expected_issue_id=surface["issue_id"],
            expected_publication_profile="WEEKLY_MAGAZINE", expected_surface_path=surface_path,
            expected_surface_sha256=core.sha256_file(surface_path), require_pass=True,
        )
    except Exception as exc:
        raise SystemExit(f"Pre-TeX semantic review validation FAILED: {exc}") from exc

    # Reject a dirty or mismatched current implementation before creating any
    # TeX, bibliography, copied style, or receipt output.
    weekly._verify_head_bytes(root, core.repository_commit_sha(root), weekly.current_closure(root))

    try:
        survey_root = weekly.validate_survey_build_directory(
            root, context["profile"]["paths"]["survey_root"]
        )
    except ValueError as exc:
        raise SystemExit(f"Weekly publication build directory invalid: {exc}") from exc
    quality_root = publication_root / "quality"
    survey_root.mkdir(parents=True, exist_ok=True)
    quality_root.mkdir(parents=True, exist_ok=True)
    primary_path = survey_root / "main.tex"
    bibliography_path = survey_root / "references.bib"
    style_path = survey_root / "jgaisurvey.sty"
    receipt_path = publication_root / "validated-source-manifest.json"
    archived_input = publication_root / "interactive-semantic-publication-input.json"
    subject_path = quality_root / "subject-entity-property-binding.json"
    for path in (primary_path, bibliography_path, style_path, receipt_path, archived_input, subject_path):
        if path.exists():
            raise SystemExit(f"refusing existing semantic publication artifact: {path}")

    main_text = weekly.render_main(surface)
    bibliography_text = weekly.render_bibliography(surface)
    style_bytes = (root / weekly.STYLE_PATH).read_bytes()
    weekly.validate_generated_closure(main_text, style_bytes.decode("utf-8"))
    primary_path.write_text(main_text, encoding="utf-8")
    bibliography_path.write_text(bibliography_text, encoding="utf-8")
    style_path.write_bytes(style_bytes)
    core.write_json(archived_input, core.load_json(input_path))
    receipt_context = dict(context)
    receipt_context["authored_path"] = archived_input
    receipt = weekly.build_receipt(
        root, receipt_context, surface_path, review_path, primary_path, bibliography_path, style_path
    )
    schema_gate.validate_instance(receipt, root / weekly.RECEIPT_SCHEMA, label="Weekly source receipt")
    core.write_json(receipt_path, receipt)

    subject = {
        "schema_version": "2.0-rc1", "check_id": "SUBJECT_ENTITY_PROPERTY_BINDING",
        "status": "PASS", "issue_id": surface["issue_id"],
        "cited_discovery_count": len(surface["bibliography"]),
        "bindings": [
            {
                "discovery_id": row["discovery_id"], "canonical_name": row["title"],
                "canonical_url": row["url"], "materiality": context["records"][row["discovery_id"]]["materiality"],
                "status": context["records"][row["discovery_id"]]["status"],
                "source_accessed_at": context["records"][row["discovery_id"]]["source_accessed_at"],
            }
            for row in surface["bibliography"]
        ],
    }
    core.write_json(subject_path, subject)
    print(json.dumps({
        "issue_id": surface["issue_id"], "source_root": _rel(root, context["source_root"]),
        "survey_root": _rel(root, survey_root), "source_manifest": _rel(root, receipt_path),
        "main_tex": _rel(root, primary_path), "bibliography": _rel(root, bibliography_path),
        "style": _rel(root, style_path), "subject_result": _rel(root, subject_path),
        "identifier_tokens": _identifier_tokens(surface, context["records"]),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
