#!/usr/bin/env python3
"""Parent witnesses for persisted reader-surface review admission via `scan-manuscript`.

WITNESS ONLY. This does not change runtime source and is not the fix. It reuses the
existing real direct-primary fixture builder from
`tests/test_survey_reader_surface_gate_v2.py` through importlib (no unittest
discovery), writes a schema-valid persisted `reader-surface-semantic-review-v2`
record, and invokes the real CLI as a subprocess.

All review records here are explicitly labelled synthetic and are NOT real Human
review, publication or adoption evidence.

Usage (must be run with cwd == fixture git root):
    python run_parent_witness.py <outdir>
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

from scripts import survey_production_v2 as core  # noqa: E402
from scripts import survey_reader_surface_gate_v2 as surface_gate  # noqa: E402
from scripts import survey_schema_v2 as schema_gate  # noqa: E402

OUTDIR = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (REPO / "gate-cli-witness-out")
OUTDIR.mkdir(parents=True, exist_ok=True)

ISSUE = "2026-W35"
MANUSCRIPT_REL = f"sources/{ISSUE}/publication/v2/reader-manuscript-v2.json"
REVIEW_REL = f"sources/{ISSUE}/publication/v2/reader-surface-semantic-review-v2.json"

SYNTHETIC_REVIEWER = "synthetic-parent-witness (not human)"


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clean_env() -> dict[str, str]:
    env = dict(os.environ)
    for key in (
        "GIT_DIR",
        "GIT_WORK_TREE",
        "GIT_INDEX_FILE",
        "GIT_OBJECT_DIRECTORY",
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        "GIT_COMMON_DIR",
    ):
        env.pop(key, None)
    env["PYTHONPATH"] = str(REPO)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def run_witness(name: str, argv: list[str], cwd: Path) -> dict[str, Any]:
    log_base = OUTDIR / f"parent-witness-{name}"
    proc = subprocess.run(
        argv,
        cwd=str(cwd),
        env=clean_env(),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    (log_base.with_suffix(".cmd.txt")).write_text(
        "cwd: " + str(cwd) + "\nargv: " + json.dumps(argv) + "\n", encoding="utf-8"
    )
    (log_base.with_suffix(".stdout.txt")).write_text(proc.stdout or "", encoding="utf-8")
    (log_base.with_suffix(".stderr.txt")).write_text(proc.stderr or "", encoding="utf-8")
    (log_base.with_suffix(".exit.txt")).write_text(f"{proc.returncode}\n", encoding="utf-8")
    return {
        "name": name,
        "cwd": str(cwd),
        "argv": argv,
        "exit": proc.returncode,
        "stdout": proc.stdout or "",
        "stderr": proc.stderr or "",
    }


def classify(observed: dict[str, Any]) -> dict[str, Any]:
    err = observed["stderr"]
    return {
        "exit_nonzero": observed["exit"] != 0,
        "has_surface_sha256_missing": "semantic_authority missing required field: surface_sha256" in err,
        "has_relative_to_error": "is not in the subpath of" in err,
        "has_file_not_found": "FileNotFoundError" in err or "No such file or directory" in err,
        "has_reviewed_surface_typeerror": "'dict' object has no attribute" in err,
    }


def main() -> int:
    fixture_mod = load_module(
        "gate_cli_parent_witness_fixture",
        REPO / "tests" / "test_survey_reader_surface_gate_v2.py",
    )
    case = fixture_mod.SurveyReaderSurfaceGateV2Tests(
        methodName="test_clean_reader_prose_passes_gate"
    )
    case.setUp()
    summary: dict[str, Any] = {"kind": "parent witness (no fix)", "synthetic_review_only": True}
    try:
        _profile, main_tex, _bib, m_path = case._build_valid_manifest()
        surface_path, rev_path, _sem_auth = case._create_semantic_surface_and_review()
        root = Path(case.root)

        # Relabel accurately-synthetic and recompute the strict review digest so the
        # persisted record is genuine but not misattributed to a human reviewer.
        doc = json.loads(Path(rev_path).read_text(encoding="utf-8"))
        doc["reviewed_by"] = SYNTHETIC_REVIEWER
        base = {k: v for k, v in doc.items() if k != "review_sha256"}
        doc["review_sha256"] = core.sha256_object(base)
        core.write_json(rev_path, doc)

        schema_gate.validate_instance(
            doc,
            root / "schemas/reader-surface-semantic-review-v2.schema.json",
            label="Parent-witness persisted reader-surface review",
        )
        manifest = json.loads(Path(m_path).read_text(encoding="utf-8"))

        summary["fixture"] = {
            "temp_repo_root": str(root),
            "manifest_path": str(m_path),
            "manifest_primary_source": manifest["primary_source"],
            "reviewed_surface": doc["reviewed_surface"],
            "review_path": str(rev_path),
            "review_rel": REVIEW_REL,
            "route_reason": "reviewed_surface.path == primary_source.path -> DIRECT_PRIMARY",
            "review_kind": doc["review_kind"],
            "reviewed_by": doc["reviewed_by"],
            "review_sha256": doc["review_sha256"],
            "schema_valid": True,
        }

        python = sys.executable
        base_cmd = [
            python,
            str(GATE),
            "--repo-root",
            str(root),
            "scan-manuscript",
            "--manuscript",
            MANUSCRIPT_REL,
        ]
        witnesses = [
            (
                "absolute-contained",
                base_cmd + ["--semantic-authority", str(rev_path)],
                root,
            ),
            (
                "repo-relative",
                base_cmd + ["--semantic-authority", REVIEW_REL],
                root,
            ),
            (
                "relative-cwd-differs-supplementary",
                base_cmd + ["--semantic-authority", REVIEW_REL],
                REPO,
            ),
        ]
        results = []
        for name, argv, cwd in witnesses:
            observed = run_witness(name, argv, cwd)
            observed["classification"] = classify(observed)
            results.append(observed)
        summary["witnesses"] = results

        # Positive controls: prove the persisted review and direct-primary fixture are
        # sound, so the CLI failures above are not setup failures masquerading as a defect.
        controls: list[dict[str, Any]] = []
        try:
            strict_report = surface_gate.evaluate_reader_surface_gate(
                root, Path(m_path), semantic_review_path=REVIEW_REL, recorded_at=case.now
            )
            controls.append({"name": "strict-loader semantic_review_path (repo-relative)", "result": "PASSED",
                             "report": {k: strict_report[k] for k in ("status",) if k in strict_report}})
        except Exception as exc:  # noqa: BLE001 - witness records the raw outcome
            controls.append({"name": "strict-loader semantic_review_path (repo-relative)", "result": "FAILED",
                             "error": f"{type(exc).__name__}: {exc}"})
        try:
            validated = surface_gate.load_and_validate_reader_surface_semantic_review(
                root, Path(rev_path),
                expected_issue_id=ISSUE, expected_publication_profile="WEEKLY_MAGAZINE",
                require_pass=True,
            )
            auth_report = surface_gate.evaluate_reader_surface_gate(
                root, Path(m_path), semantic_authority=validated, recorded_at=case.now
            )
            controls.append({"name": "authority-object (correctly built)", "result": "PASSED",
                             "report": {k: auth_report[k] for k in ("status",) if k in auth_report}})
        except Exception as exc:  # noqa: BLE001
            controls.append({"name": "authority-object (correctly built)", "result": "FAILED",
                             "error": f"{type(exc).__name__}: {exc}"})
        summary["positive_controls"] = controls
        (OUTDIR / "parent-witness-controls.json").write_text(
            json.dumps(controls, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

        (OUTDIR / "parent-witness-summary.json").write_text(
            json.dumps({k: v for k, v in summary.items() if k != "witnesses"}, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        (OUTDIR / "parent-witness-summary-full.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(json.dumps({k: v for k, v in summary.items() if k not in ("witnesses", "positive_controls")},
                         indent=2, ensure_ascii=False))
        for observed in results:
            print(
                f"[{observed['name']}] exit={observed['exit']} "
                f"surface_sha256_missing={observed['classification']['has_surface_sha256_missing']} "
                f"relative_to_error={observed['classification']['has_relative_to_error']} "
                f"file_not_found={observed['classification']['has_file_not_found']}"
            )
        for control in controls:
            print(f"[control:{control['name']}] {control['result']} {control.get('error', '')}")
        return 0
    finally:
        case.doCleanups()


if __name__ == "__main__":
    sys.exit(main())
