#!/usr/bin/env python3
"""Finalize a Core v2 semantic-publication Quality Bundle from exact reviewed bytes.

The semantic publication build establishes deterministic source/PDF checks first.
ChatGPT then reviews those exact bytes and supplies only the qualitative review
rows required by the active Research/Publication Profile. This helper validates
both families against config/survey-production-v2.json and creates one immutable
Quality Regression Bundle. It does not advance Production State.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts import survey_production_v2 as core
from scripts import survey_quality_v2 as quality


def _safe(root: Path, raw: str, label: str) -> Path:
    path = core.repo_local_path(root, raw, label)
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"{label} missing or unsafe: {raw}")
    return path


def _validate_authority(root: Path, ref: dict[str, Any], label: str, *, byte_count: bool = False) -> Path:
    expected = {"path", "sha256", "byte_count"} if byte_count else {"path", "sha256"}
    if not isinstance(ref, dict) or set(ref) != expected:
        raise ValueError(f"{label} authority fields invalid")
    path = _safe(root, ref["path"], label)
    if core.sha256_file(path) != ref["sha256"]:
        raise ValueError(f"{label} SHA drift")
    if byte_count and path.stat().st_size != ref["byte_count"]:
        raise ValueError(f"{label} byte_count drift")
    return path


def validate_request(
    root: Path,
    state_path: Path,
    request_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], Path, Path, list[dict[str, Any]]]:
    state = core.load_json(state_path)
    if state.get("lifecycle_state") != "DRAFT_COMPLETE" or state.get("next_action") != "stage:semantic-publication-validation":
        raise ValueError("semantic quality finalization requires DRAFT_COMPLETE State")
    issue_id = state["issue_id"]
    profile_path = _safe(root, state["profile"]["path"], "Production Profile")
    profile = core.load_json(profile_path)

    request = core.load_json(request_path)
    expected = {
        "schema_version", "issue_id", "runner", "source", "pdf", "page_count",
        "deterministic_results", "reviews", "recorded_at",
    }
    if set(request) != expected or request.get("schema_version") != "2.0-rc1":
        raise ValueError("semantic quality request envelope invalid")
    if request.get("issue_id") != issue_id or request.get("runner") != "CORE_V2_SEMANTIC_QUALITY":
        raise ValueError("semantic quality request identity mismatch")
    try:
        core.parse_instant(str(request.get("recorded_at", "")))
    except ValueError as exc:
        raise ValueError("semantic quality request recorded_at invalid") from exc

    source = _validate_authority(root, request["source"], "validated source")
    pdf = _validate_authority(root, request["pdf"], "publication PDF", byte_count=True)
    page_count = request["page_count"]
    if not isinstance(page_count, int) or page_count < 1:
        raise ValueError("semantic quality request page_count must be positive")

    source_root = core.repo_local_path(root, profile["paths"]["source_root"], "paths.source_root")
    expected_source = core.repo_local_path(root, profile["paths"]["survey_root"], "paths.survey_root") / "main.tex"
    expected_pdf = source_root / "publication/v2" / f"{issue_id}-publication-preview.pdf"
    if source.resolve() != expected_source.resolve():
        raise ValueError("semantic quality source path is not canonical")
    if pdf.resolve() != expected_pdf.resolve():
        raise ValueError("semantic quality PDF path is not canonical")

    preflight_path = source_root / "publication/v2/quality/pdf-preflight.json"
    preflight = core.load_json(preflight_path)
    if (
        preflight.get("check_id") != "PDF_PREFLIGHT"
        or preflight.get("status") != "PASS"
        or preflight.get("pdf_sha256") != core.sha256_file(pdf)
        or preflight.get("page_count") != page_count
        or preflight.get("byte_count") != pdf.stat().st_size
    ):
        raise ValueError("PDF preflight does not bind exact reviewed PDF/page count")

    cfg = core.load_json(root / core.DEFAULT_CONFIG)
    expected_checks = quality.expected_checks(
        cfg, profile["research_profile"], profile["publication_profile"]
    )
    expected_deterministic = {
        check_id for check_id, kind in expected_checks.items() if kind == "DETERMINISTIC"
    }
    expected_agent = {
        check_id: kind for check_id, kind in expected_checks.items() if kind != "DETERMINISTIC"
    }

    rows = request["deterministic_results"]
    if not isinstance(rows, list):
        raise ValueError("deterministic_results must be a list")
    deterministic_ids = [row.get("check_id") for row in rows if isinstance(row, dict)]
    if set(deterministic_ids) != expected_deterministic or len(deterministic_ids) != len(set(deterministic_ids)):
        raise ValueError(
            "deterministic quality family incomplete: "
            f"expected={sorted(expected_deterministic)} actual={sorted(str(x) for x in deterministic_ids)}"
        )

    checks: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"check_id", "path", "sha256"}:
            raise ValueError("deterministic result reference fields invalid")
        check_id = row["check_id"]
        result_path = _validate_authority(
            root,
            {"path": row["path"], "sha256": row["sha256"]},
            f"deterministic result {check_id}",
        )
        result_payload = core.load_json(result_path)
        if result_payload.get("check_id") != check_id or result_payload.get("status") != "PASS":
            raise ValueError(f"deterministic result payload did not PASS: {check_id}")
        checks.append(
            {
                "check_id": check_id,
                "kind": "DETERMINISTIC",
                "status": "PASS",
                "executor": "Core v2 deterministic validator",
                "evidence": f"Exact result artifact {row['path']} passed and is SHA-bound to the reviewed publication bytes.",
                "recorded_at": request["recorded_at"],
                "result": {"path": row["path"], "sha256": row["sha256"]},
            }
        )

    reviews = request["reviews"]
    if not isinstance(reviews, list):
        raise ValueError("reviews must be a list")
    review_ids = [row.get("check_id") for row in reviews if isinstance(row, dict)]
    if set(review_ids) != set(expected_agent) or len(review_ids) != len(set(review_ids)):
        raise ValueError(
            "agent quality family incomplete: "
            f"expected={sorted(expected_agent)} actual={sorted(str(x) for x in review_ids)}"
        )
    for row in reviews:
        required = {"check_id", "kind", "status", "executor", "evidence", "recorded_at", "result"}
        if not isinstance(row, dict) or set(row) != required:
            raise ValueError("agent quality review fields invalid")
        check_id = row["check_id"]
        if row["kind"] != expected_agent[check_id]:
            raise ValueError(f"agent quality review kind mismatch: {check_id}")
        if row["status"] != "PASS" or row["result"] is not None:
            raise ValueError(f"agent quality review must be PASS without deterministic result authority: {check_id}")
        if not isinstance(row["executor"], str) or not row["executor"].strip():
            raise ValueError(f"agent quality executor required: {check_id}")
        if not isinstance(row["evidence"], str) or not row["evidence"].strip():
            raise ValueError(f"agent quality evidence required: {check_id}")
        try:
            core.parse_instant(str(row["recorded_at"]))
        except ValueError as exc:
            raise ValueError(f"agent quality recorded_at invalid: {check_id}") from exc
        checks.append(dict(row))

    quality.validate_checks(
        root, cfg, profile["research_profile"], profile["publication_profile"], checks
    )
    return state, profile, source, pdf, checks


def finalize(
    root: Path,
    state_path: Path,
    request_path: Path,
    output_path: Path,
) -> Path:
    state, profile, source, pdf, checks = validate_request(root, state_path, request_path)
    del profile
    if output_path.exists():
        raise ValueError(f"refusing existing Quality Regression Bundle: {output_path}")
    quality.build_bundle(
        root,
        state["issue_id"],
        source,
        pdf,
        checks,
        output_path,
        production_profile_path=root / state["profile"]["path"],
    )
    quality.validate_bundle(root, output_path, issue_id=state["issue_id"])
    return output_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--state", required=True)
    ap.add_argument("--request", required=True)
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    state_path = _safe(root, args.state, "Production State")
    request_path = _safe(root, args.request, "semantic quality request")
    state = core.load_json(state_path)
    profile = core.load_json(root / state["profile"]["path"])
    source_root = core.repo_local_path(root, profile["paths"]["source_root"], "paths.source_root")
    output = source_root / "publication/v2/quality-regression-bundle-v2.json"
    final = finalize(root, state_path, request_path, output)
    print(json.dumps(
        {
            "issue_id": state["issue_id"],
            "quality_bundle": str(final.relative_to(root)),
            "quality_bundle_sha256": core.sha256_file(final),
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
