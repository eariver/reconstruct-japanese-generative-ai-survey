"""Bounded read-only-upstream witnesses; writes only ignored local fixtures/results.

Run from reconstruct: python notes/phase-5-upstream-reconciliation/probe.py
Requires captured inputs.json bytes and the prior verified support snapshot.
No network, Git commands, production mutations, mocks, or full workflow execution.
Synthetic review PASS below is fixture data, never actual review authority.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
DEST = Path(__file__).resolve().parent
REF = "774dd39a951c9ac3818e83dfffd4c7666efb0a20"
CACHE = ROOT / ".phase-5-inputs" / REF
LAB = ROOT / ".phase-5-inputs" / "upstream-reconciliation"


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def prepare():
    # Copy only verified support files and overlay captured current source.
    # No Git-aware tests are called; this probe never invokes Git.
    support = load(ROOT / "notes/phase-5-runtime-repair/support-inputs.json")
    copied = []
    for row in support["files"]:
        if Path(row["path"]).parts[0] not in {"scripts", "schemas", "config"}:
            continue
        src = ROOT / ".phase-5-inputs/runtime-repair-baseline" / row["path"]
        assert sha(src) == row["sha256"], row["path"]
        dst = LAB / row["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        copied.append(row["path"])
    inputs = load(DEST / "inputs.json")
    for row in inputs:
        assert row["ref"] == REF
        src = CACHE / row["path"]
        assert sha(src) == row["sha256"], row["path"]
        dst = LAB / row["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    # Full eight-commit compare: all changed runtime scripts/schemas are captured.
    changed = load(DEST / "observation.json")["files"]
    captured = {r["path"] for r in inputs}
    assert all(r["filename"] in captured for r in changed
               if r["filename"].startswith(("scripts/", "schemas/")))
    return len(copied)


def rejection(fn):
    try:
        fn()
    except (ValueError, RuntimeError) as e:
        return {"rejected": True, "error": str(e)}
    return {"rejected": False}


def main():
    support_count = prepare()
    os.chdir(LAB)
    sys.path.insert(0, str(LAB))
    from scripts import survey_production_v2 as core
    from scripts import survey_schema_v2 as schema
    from scripts import survey_reader_surface_gate_v2 as gate
    from scripts import survey_stage_validation_v2 as stage
    from scripts import survey_weekly_semantic_publication_v2 as weekly

    spec = importlib.util.spec_from_file_location(
        "upstream_reader_test", LAB / "tests/test_survey_reader_surface_gate_v2.py")
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    t = helper.SurveyReaderSurfaceGateV2Tests()
    t.setUp()
    out = {"production_ref": REF, "support_files_verified": support_count,
           "scope": "FUNCTION_AND_SCHEMA_WITNESSES_NOT_FULL_WORKFLOW_OR_INDEPENDENT_REVIEW"}
    try:
        _, tex, bib, manifest = t._build_valid_manifest()
        # Existing upstream fixture constructs a persisted synthetic semantic review.
        surface, review, sem_authority = t._create_semantic_surface_and_review()
        report_path = t.root / "gate.json"
        report = gate.evaluate_reader_surface_gate(
            t.root, manifest, semantic_authority=sem_authority,
            recorded_at=t.now, output_path=report_path)
        gate.validate_reader_surface_gate(t.root, report_path,
            issue_id="2026-W35", publication_profile="WEEKLY_MAGAZINE")
        assert report["status"] == "PASSED"
        # Genuine reviewed-file drift remains rejected (positive safety control).
        prior_surface = surface.read_bytes()
        surface.write_bytes(prior_surface + b"\n")
        drift = rejection(lambda: gate.validate_reader_surface_gate(t.root, report_path))
        assert drift["rejected"]
        surface.write_bytes(prior_surface)

        # Independently change manifest-bound reader prose; leave reviewed input intact.
        old_tex_sha = sha(tex)
        tex.write_text("\\section{Storage}\nDisk persistence uses durable pages and transaction logs.\n",
                       encoding="utf-8")
        doc = load(manifest)
        doc["primary_source"]["sha256"] = sha(tex)
        base = {k: v for k, v in doc.items() if k != "manuscript_sha256"}
        if "manuscript_sha256" in doc:
            doc["manuscript_sha256"] = core.sha256_object(base)
        core.write_json(manifest, doc)
        changed = gate.evaluate_reader_surface_gate(
            t.root, manifest, semantic_authority=sem_authority,
            recorded_at=t.now, output_path=report_path)
        gate.validate_reader_surface_gate(t.root, report_path,
            issue_id="2026-W35", publication_profile="WEEKLY_MAGAZINE")
        assert changed["status"] == "PASSED"
        out["reader_binding"] = {
            "baseline_gate": report["status"], "reviewed_file_drift_control": drift,
            "primary_before_sha256": old_tex_sha, "primary_after_sha256": sha(tex),
            "unchanged_reviewed_surface_sha256": sha(surface),
            "changed_manuscript_gate": changed["status"],
            "changed_manuscript_gate_revalidation": "ACCEPTED",
            "boundary": "Persisted same-issue review and all hashes valid, but reviewed JSON and current TeX have different prose. No full stage advance attempted."}

        # Mirror the publisher's actual structured input call, then render only.
        publication = {"cover": {"headline": "Systems", "deck": "Weekly developments",
                                  "anchors": ["Tools"]},
                       "frontmatter": {"heading": "Overview", "lede": "Reader introduction.",
                                       "scope_notes": ["Public evidence only."]},
                       "final_summary": {"heading": "Summary", "paragraphs": ["Weekly conclusion."]}}
        def projection(p):
            pth = gate.build_weekly_reader_surface_input(t.root, "2026-W35", "WEEKLY_MAGAZINE",
                "Weekly conclusion.", p["final_summary"]["paragraphs"], [],
                headline=p["cover"]["headline"], deck=p["cover"]["deck"],
                output_path=t.root / "projection.json")
            return sha(pth)
        original_projection = projection(publication)
        original_tex = weekly._render_tex("2026-W35", "2026-09-14", "Weekly", publication, [], {})
        publication["frontmatter"]["lede"] = "Discovery observation is the basis of this introduction."
        changed_projection = projection(publication)
        changed_tex = weekly._render_tex("2026-W35", "2026-09-14", "Weekly", publication, [], {})
        assert original_projection == changed_projection and original_tex != changed_tex
        lexical = gate.scan_reader_text_lines([publication["frontmatter"]["lede"]],
                                              "frontmatter", "publication-input.json")
        assert any(f.severity == "BLOCKING" for f in lexical)
        out["pre_tex_coverage"] = {
            "changed_field": "frontmatter.lede", "surface_sha256_unchanged": original_projection,
            "rendered_tex_changed": True, "omitted_text_would_be_lexically_blocking": True,
            "boundary": "Actual projection/render functions only; empty packages are not a full edition or CLI trial."}

        # Internal manifest rationale is distinct from the unchanged TeX/bibliography.
        clean_surface = gate.validate_manuscript_surface(t.root, doc)
        doc["architecture_coverage"][0]["detail"] = "Discovery observation supports this coverage mapping."
        audit = rejection(lambda: gate.validate_manuscript_surface(t.root, doc))
        assert audit["rejected"]
        out["audit_field_scope"] = {"reader_bytes_unchanged": True,
            "changed_field": "architecture_coverage[0].detail", "result": audit}

        # Current Freeze runtime still rejects the existing schema-required third artifact.
        names = {n: t.root / n for n in ("freeze-record", "release-manifest", "visual-review-record")}
        freeze = rejection(lambda: stage._current_artifacts(t.root,
            {"lifecycle_state": "RELEASE_CANDIDATE"}, names))
        assert freeze["rejected"] and "unexpected current stage artifacts" in freeze["error"]
        out["freeze_artifact_set"] = freeze

        state = load(LAB / "sources/2026-W34/production-state.json")
        approval = LAB / state["checkpoint_provenance"]["publication_preview"]["path"]
        assert sha(approval) == state["checkpoint_provenance"]["publication_preview"]["sha256"]
        # Validate actual approved Human record using the Stage schema used by _prior_artifacts.
        approval_as_stage = rejection(lambda: schema.load_and_validate_json(
            approval, LAB / "schemas/stage-checkpoint-v2.schema.json", label="prior Stage Checkpoint"))
        assert approval_as_stage["rejected"]
        out["approval_type"] = {"actual_w34_pointer_sha_verified": True,
            "stage_schema_rejects_approval": approval_as_stage}
        frozen = LAB / state["checkpoint_provenance"]["release"]["path"]
        assert sha(frozen) == state["checkpoint_provenance"]["release"]["sha256"]
        schema.load_and_validate_json(frozen, LAB / "schemas/stage-checkpoint-v2.schema.json")
        out["historical_w34"] = {"lifecycle_state": state["lifecycle_state"],
            "next_action": state["next_action"], "actual_release_checkpoint_current_schema": "ACCEPTED",
            "scope": "Schema and State pointer raw SHA only; no full State/report dependency validation or PDF review."}
    finally:
        t.doCleanups()
    (DEST / "probe-results.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
