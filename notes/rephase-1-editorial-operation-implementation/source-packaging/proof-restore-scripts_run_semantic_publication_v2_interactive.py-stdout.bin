#!/usr/bin/env python3
"""Revision-safe entrypoint for the Core v2 semantic publication renderer.

Initial publication remains fail-closed.  A pending, unapproved Publication
Preview revision may replace only artifacts owned by this renderer before the
immutable base entrypoint recreates and revalidates them.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from scripts import survey_production_v2 as core
from scripts import run_semantic_publication_v2_interactive_base as _base


def _safe_owned(path: Path, root: Path) -> Path:
    resolved = path.resolve()
    resolved.relative_to(root.resolve())
    return resolved


def _prepare_revision() -> None:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--state", required=True)
    parser.add_argument("--input", required=True)
    args, _ = parser.parse_known_args()
    root = Path(args.repo_root).resolve()
    state_path = _safe_owned(root / args.state, root)
    state = core.load_json(state_path)
    revision = (
        state.get("lifecycle_state") == "RELEASE_CANDIDATE"
        and state.get("next_action") == "PUBLICATION_PREVIEW"
        and state.get("human_gates", {}).get("publication_preview") == "pending"
        and state.get("human_gate_provenance", {}).get("publication_preview") is None
    )
    if not revision:
        return
    profile_path = _safe_owned(root / state["profile"]["path"], root)
    profile = core.load_json(profile_path)
    source_root = _safe_owned(root / profile["paths"]["source_root"], root)
    survey_root = _safe_owned(root / profile["paths"]["survey_root"], root)
    publication_root = source_root / "publication/v2"
    quality_root = publication_root / "quality"
    owned = (
        survey_root / "main.tex",
        survey_root / "references.bib",
        survey_root / "jgaisurvey.sty",
        publication_root / "validated-source-manifest.json",
        publication_root / "interactive-semantic-publication-input.json",
        quality_root / "longform-special-preflight.json",
        quality_root / "subject-entity-property-binding.json",
        quality_root / "empty-wrapper-suppression.json",
    )
    for path in owned:
        checked = _safe_owned(path, root)
        if checked.is_symlink():
            raise SystemExit(f"refusing to replace symlinked publication artifact: {checked.relative_to(root)}")
        if checked.exists():
            if not checked.is_file():
                raise SystemExit(f"renderer-owned publication path is not a file: {checked.relative_to(root)}")
            checked.unlink()


if __name__ == "__main__":
    _prepare_revision()
    raise SystemExit(_base.main())
