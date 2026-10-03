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


def public_issue_slug(profile: dict[str, Any]) -> str:
    """Compatibility shim: slug authority lives in ``survey_publication_v2``."""
    return publication.public_issue_slug_from_profile(profile)


def release_identity(profile: dict[str, Any]) -> str:
    """Compatibility shim: profile release identity lives in ``survey_publication_v2``."""
    return publication.profile_release_identity(profile)


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


def build_profiled_freeze(
    repo_root: Path,
    cfg: dict[str, Any],
    state_path: Path,
    frozen_at: datetime,
) -> tuple[Path, Path]:
    state, profile_path, profile, source_root = _safe_state_profile(repo_root, cfg, state_path)
    publication_root = source_root / "publication/v2"
    candidate_path = publication_root / "publication-candidate-v2.json"
    approval_ref = state["human_gate_provenance"]["publication_preview"]
    approval_path = core.repo_local_path(repo_root, approval_ref["path"], "Publication Preview Approval")
    if not approval_path.is_file() or core.sha256_file(approval_path) != approval_ref["sha256"]:
        raise ValueError("Publication Preview approval authority drift before Freeze")

    prep = publication._prepare_freeze_inputs(repo_root, candidate_path, approval_path)
    candidate = prep["candidate"]
    if candidate["issue_id"] != state["issue_id"]:
        raise ValueError("Publication Candidate issue identity diverges from Production State")
    if prep["approval"]["issue_id"] != state["issue_id"]:
        raise ValueError("Publication Preview approval issue identity diverges from Production State")
    expected_profile = {"path": str(profile_path.relative_to(repo_root)), "sha256": core.sha256_file(profile_path)}
    if prep["profile_ref"] != expected_profile:
        raise ValueError("Quality Bundle is not bound to the current Production Profile")

    release_tag = publication.profile_release_identity(prep["profile"])
    freeze_path = publication_root / "freeze-record-v2.json"
    manifest_path = publication_root / "release-manifest-v2.json"
    # The wrapper's State file is a fixed-path install-boundary input: its
    # outputs must never overlap it, and its bytes join the install snapshot.
    norm_state = publication._lexical_repo_path(repo_root, state_path, "Production State")
    state_rel = publication._rel(repo_root, norm_state)
    for label, target in (("Freeze record", freeze_path), ("Release manifest", manifest_path)):
        if publication._lexical_repo_path(repo_root, target, label) == norm_state:
            raise ValueError(f"{label} target overlaps the Production State input: {target}")
    freeze_payload = publication._build_freeze_payload(
        repo_root=repo_root,
        candidate_path=prep["candidate_path"],
        candidate=candidate,
        approval_path=prep["approval_path"],
        approval=prep["approval"],
        visual_path=prep["visual_path"],
        frozen_at=frozen_at,
    )
    source = candidate["source"]
    pdf = candidate["pdf"]
    plan = publication._preflight_freeze_pair(
        repo_root,
        freeze_path,
        manifest_path,
        prep,
        freeze_payload,
        lambda freeze_sha, freeze_target: publication._build_manifest_payload(
            repo_root=repo_root,
            freeze_path=freeze_target,
            freeze_record_sha256=freeze_sha,
            release_identity=release_tag,
            source_path=source["path"],
            source_sha256=source["sha256"],
            pdf_path=pdf["path"],
            pdf_sha256=pdf["sha256"],
            page_count=pdf["page_count"],
            issue_id=candidate["issue_id"],
        ),
        extra_snapshot={state_rel: core.sha256_file(norm_state)},
    )
    installed_freeze, installed_manifest = publication._install_freeze_pair(repo_root, plan)
    publication.validate_release_manifest(repo_root, installed_manifest)
    return installed_freeze, installed_manifest


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
