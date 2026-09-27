#!/usr/bin/env python3
"""Observational probe: `--semantic-review` transport shape (DEFERRED, not normative).

This probe records the current behavior of the CLI `--semantic-review` argument so
the inherited limitations are documented evidence rather than institutionalized in
the acceptance test module. It is NOT part of the candidate test suite and asserts
no desired behavior.

Findings transport is out of scope for this unit:
  - `core.load_json` is object-only, so a bare findings array cannot be loaded.
  - a JSON object is passed through as `semantic_review_findings` (mapping keys).
The canonical separation property (a review supplied only via `--semantic-review`
cannot substitute for `--semantic-authority`) is asserted in the normative test
module, not here.

Run with cwd == fixture git root:
    python run_findings_transport_probe.py <outdir>
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO = Path.cwd().resolve()
GATE = REPO / "scripts" / "survey_reader_surface_gate_v2.py"
if not GATE.is_file():
    raise SystemExit(f"run from the fixture git root; missing {GATE}")
sys.path.insert(0, str(REPO))

from scripts import survey_reader_surface_gate_v2 as surface_gate  # noqa: E402
from scripts import survey_production_v2 as core  # noqa: E402

OUTDIR = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (REPO / "findings-transport-probe")
OUTDIR.mkdir(parents=True, exist_ok=True)
GATE_SCRIPT = "scripts/survey_reader_surface_gate_v2.py"


def clean_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["PYTHONPATH"] = str(REPO)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def run_cli(root: Path, argv: list[str]) -> dict[str, Any]:
    cmd = [sys.executable, str(REPO / GATE_SCRIPT), "--repo-root", str(root), "scan-manuscript", *argv]
    proc = subprocess.run(
        cmd, cwd=str(root), env=clean_env(), capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    return {"argv": argv, "exit": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}


def main() -> int:
    spec = importlib.util.spec_from_file_location(
        "findings_probe_fixture", REPO / "tests" / "test_survey_reader_surface_gate_v2.py"
    )
    assert spec is not None and spec.loader is not None
    fixture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixture)
    case = fixture.SurveyReaderSurfaceGateV2Tests(methodName="test_clean_reader_prose_passes_gate")
    case.setUp()
    summary: dict[str, Any] = {"kind": "observational findings-transport probe (deferred)", "cases": []}
    try:
        _profile, _main_tex, _bib, manifest = case._build_valid_manifest()
        _surface, review_path, _sem_auth = case._create_semantic_surface_and_review()
        root = Path(case.root)
        doc = core.load_json(review_path)
        doc["reviewed_by"] = "synthetic findings-transport probe (not human)"
        doc["review_sha256"] = core.sha256_object({k: v for k, v in doc.items() if k != "review_sha256"})
        core.write_json(review_path, doc)
        review_rel = str(review_path.relative_to(root)).replace("\\", "/")
        manifest_rel = str(manifest.relative_to(root)).replace("\\", "/")

        validated = surface_gate.load_and_validate_reader_surface_semantic_review(
            root, review_rel, expected_issue_id="2026-W35", expected_publication_profile="WEEKLY_MAGAZINE",
            require_pass=True,
        )
        authority_path = review_path.parent / "probe-authority-object.json"
        core.write_json(authority_path, validated)
        authority_rel = str(authority_path.relative_to(root)).replace("\\", "/")

        array_path = review_path.parent / "probe-findings-array.json"
        array_path.write_text('[{"finding_id": "ARRAY-1", "severity": "BLOCKING"}]', encoding="utf-8")
        object_path = review_path.parent / "probe-findings-object.json"
        core.write_json(object_path, {"note": "inert findings container"})
        array_rel = str(array_path.relative_to(root)).replace("\\", "/")
        object_rel = str(object_path.relative_to(root)).replace("\\", "/")

        cases = {
            "bare-array-with-valid-authority": [
                "--manuscript", manifest_rel, "--semantic-authority", authority_rel,
                "--semantic-review", array_rel,
                "--output", "sources/2026-W35/publication/v2/probe-array.json",
            ],
            "object-with-valid-authority": [
                "--manuscript", manifest_rel, "--semantic-authority", authority_rel,
                "--semantic-review", object_rel,
                "--output", "sources/2026-W35/publication/v2/probe-object.json",
            ],
            "review-only-via-semantic-review": [
                "--manuscript", manifest_rel, "--semantic-review", review_rel,
                "--output", "sources/2026-W35/publication/v2/probe-only.json",
            ],
        }
        for name, argv in cases.items():
            observed = run_cli(root, argv)
            observed["name"] = name
            summary["cases"].append(observed)
        (OUTDIR / "findings-transport-probe.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        for observed in summary["cases"]:
            first_line = (observed["stderr"].strip().splitlines() or [""])[-1]
            print(f"[{observed['name']}] exit={observed['exit']} last_stderr={first_line!r}")
        return 0
    finally:
        case.doCleanups()


if __name__ == "__main__":
    sys.exit(main())
