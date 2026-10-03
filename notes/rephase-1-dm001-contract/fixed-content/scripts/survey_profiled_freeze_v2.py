#!/usr/bin/env python3
"""Build Freeze/Release Manifest from the exact Production Profile public slug.

Internal source issue IDs and reader-facing Special slugs are intentionally not
always identical.  Retrospective Period uses e.g. ``SP-2025-H2`` internally but
publishes as ``special/2025-H2``.  This helper derives public identity from the
exact Profile ``paths.survey_root`` authority rather than guessing from issue ID.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts import survey_agent_control_v2 as agent
from scripts import survey_production_v2 as core
from scripts import survey_publication_v2 as publication
from scripts import survey_quality_v2 as quality
from scripts import survey_schema_v2 as schema_gate


def public_issue_slug(profile: dict[str, Any]) -> str:
    survey_root = profile.get("paths", {}).get("survey_root")
    if not isinstance(survey_root, str) or not survey_root.strip():
        raise ValueError("Production Profile survey_root required for public issue identity")
    slug = Path(survey_root).name
    if not slug or slug in {".", ".."} or "/" in slug or "\\" in slug:
        raise ValueError("Production Profile survey_root has invalid public issue slug")
    return slug


def release_identity(profile: dict[str, Any]) -> str:
    slug = public_issue_slug(profile)
    publication_profile = profile.get("publication_profile")
    if publication_profile == "WEEKLY_MAGAZINE":
        return f"weekly/{slug}"
    if publication_profile == "LONGFORM_SPECIAL":
        return f"special/{slug}"
    raise ValueError(f"unsupported publication profile: {publication_profile}")


def _safe_state_profile(repo_root: Path, cfg: dict[str, Any], state_path: Path) -> tuple[dict[str, Any], Path, dict[str, Any], Path]:
    state = core.load_json(state_path)
    errors = agent.validate_agent_state(repo_root, cfg, state)
    if errors:
        raise ValueError("Production State invalid before Freeze: " + "; ".join(errors))
    if state.get("lifecycle_state") != "RELEASE_CANDIDATE":
        raise ValueError("Profile-aware Freeze requires RELEASE_CANDIDATE lifecycle")
    if state.get("human_gates", {}).get("publication_preview") != "approved":
        raise ValueError("Profile-aware Freeze requires approved Publication Preview")
    profile_path = core.repo_local_path(repo_root, state["profile"]["path"], "Production Profile")
    if not profile_path.is_file() or core.sha256_file(profile_path) != state["profile"]["sha256"]:
        raise ValueError("Production Profile authority drift before Freeze")
    profile = core.load_json(profile_path)
    source_root = core.repo_local_path(repo_root, profile["paths"]["source_root"], "source_root")
    return state, profile_path, profile, source_root


def _write_immutable(path: Path, payload: dict[str, Any], label: str) -> None:
    if path.exists():
        if core.load_json(path) != payload:
            raise ValueError(f"refusing to overwrite divergent {label}: {path}")
        return
    core.write_json(path, payload)


def build_profiled_freeze(
    repo_root: Path,
    cfg: dict[str, Any],
    state_path: Path,
    frozen_at: datetime,
) -> tuple[Path, Path]:
    state, profile_path, profile, source_root = _safe_state_profile(repo_root, cfg, state_path)
    publication_root = source_root / "publication/v2"
    candidate_path = publication_root / "publication-candidate-v2.json"
    visual_path = publication_root / "visual-review-v2.json"
    approval_ref = state["human_gate_provenance"]["publication_preview"]
    approval_path = core.repo_local_path(repo_root, approval_ref["path"], "Publication Preview Approval")
    if not approval_path.is_file() or core.sha256_file(approval_path) != approval_ref["sha256"]:
        raise ValueError("Publication Preview approval authority drift before Freeze")

    candidate = publication.validate_candidate(repo_root, candidate_path, issue_id=state["issue_id"])
    approval = publication.validate_preview_approval(repo_root, approval_path, issue_id=state["issue_id"])
    visual = publication.validate_visual_review(repo_root, visual_path, approval_path)
    bundle_path = core.repo_local_path(repo_root, candidate["quality_bundle"]["path"], "Quality Bundle")
    bundle = quality.validate_bundle(repo_root, bundle_path, issue_id=state["issue_id"])
    expected_profile = {"path": str(profile_path.relative_to(repo_root)), "sha256": core.sha256_file(profile_path)}
    if bundle["production_profile"] != expected_profile:
        raise ValueError("Quality Bundle is not bound to the current Production Profile")
    if candidate["publication_profile"] != profile["publication_profile"] or bundle["publication_profile"] != profile["publication_profile"]:
        raise ValueError("Publication Candidate/Profile publication identity mismatch")
    if candidate["pdf"]["sha256"] != approval["pdf_sha256"] or visual["pdf_sha256"] != approval["pdf_sha256"]:
        raise ValueError("Freeze exact-PDF authority chain diverged")

    freeze_path = publication_root / "freeze-record-v2.json"
    manifest_path = publication_root / "release-manifest-v2.json"
    freeze = {
        "schema_version": "2.0-rc1",
        "issue_id": candidate["issue_id"],
        "status": "FROZEN",
        "publication_candidate_path": str(candidate_path.relative_to(repo_root)),
        "publication_candidate_sha256": core.sha256_file(candidate_path),
        "publication_preview_approval_path": str(approval_path.relative_to(repo_root)),
        "publication_preview_approval_sha256": core.sha256_file(approval_path),
        "visual_review_path": str(visual_path.relative_to(repo_root)),
        "visual_review_sha256": core.sha256_file(visual_path),
        "source_path": candidate["source"]["path"],
        "source_sha256": candidate["source"]["sha256"],
        "pdf_path": candidate["pdf"]["path"],
        "pdf_sha256": candidate["pdf"]["sha256"],
        "page_count": candidate["pdf"]["page_count"],
        "frozen_at": core.iso_utc(frozen_at),
    }
    schema_gate.validate_instance(freeze, repo_root / publication.FREEZE_SCHEMA, label="Freeze record")
    _write_immutable(freeze_path, freeze, "Freeze record")

    manifest = {
        "schema_version": "2.0-rc1",
        "issue_id": candidate["issue_id"],
        "release_identity": release_identity(profile),
        "status": "AUTHORIZED",
        "freeze_record_path": str(freeze_path.relative_to(repo_root)),
        "freeze_record_sha256": core.sha256_file(freeze_path),
        "source_path": freeze["source_path"],
        "source_sha256": freeze["source_sha256"],
        "pdf_path": freeze["pdf_path"],
        "pdf_sha256": freeze["pdf_sha256"],
        "page_count": freeze["page_count"],
    }
    schema_gate.validate_instance(manifest, repo_root / publication.RELEASE_MANIFEST_SCHEMA, label="Release manifest")
    _write_immutable(manifest_path, manifest, "Release manifest")
    publication.validate_release_manifest(repo_root, manifest_path)
    return freeze_path, manifest_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--state", required=True)
    parser.add_argument("--frozen-at")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    state_path = Path(args.state)
    if not state_path.is_absolute():
        state_path = root / state_path
    now = core.parse_instant(args.frozen_at) if args.frozen_at else datetime.now(timezone.utc)
    try:
        freeze, manifest = build_profiled_freeze(
            root, core.load_json(root / core.DEFAULT_CONFIG), state_path, now
        )
        print(json.dumps({"freeze": str(freeze.relative_to(root)), "manifest": str(manifest.relative_to(root))}, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
