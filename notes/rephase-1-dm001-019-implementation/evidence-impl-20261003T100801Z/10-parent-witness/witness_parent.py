"""Parent (b40) defect witnesses W1a/W1b/W2/W4/W3. Runs with cwd=parent repo copy.

Each witness prints a `WITNESS <id> <OUTCOME> <detail>` line and appends to
the JSONL record. Fixture dirs are untracked worktree paths, removed at end.
Parent tracked bytes must be unchanged (verified by caller via git status).
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import traceback
from datetime import timedelta
from pathlib import Path

ROOT = Path(".").resolve()
sys.path.insert(0, "/tmp/opencode/dm001019-scratch-20261003T100801Z")

from scripts import survey_agent_control_v2 as agent
from scripts import survey_production_v2 as core
from scripts import survey_profiled_freeze_v2 as profiled
from scripts import survey_publication_v2 as publication
from scripts import survey_quality_v2 as quality
from scripts import survey_reader_publication_v2 as reader
from scripts import survey_stage_validation_v2 as stage_validation

import special_fixture as sf

EXPECTED_HEAD = "b40de600e9ed1f80cb278213ccf17aa5f3cd9de3"
RESULTS: list[dict] = []
TRACKED_PATHS: list[Path] = []


def record(wid: str, outcome: str, detail: dict) -> None:
    RESULTS.append({"witness": wid, "outcome": outcome, "detail": detail})
    print(f"WITNESS {wid} {outcome} {json.dumps(detail, sort_keys=True)}", flush=True)


def head() -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(ROOT),
                          capture_output=True, text=True).stdout.strip()


def load_revalidation_fixture():
    spec = importlib.util.spec_from_file_location(
        "parent_wit_revalidation_fixture",
        ROOT / "tests/test_survey_publication_revalidation_v2.py")
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def advance_weekly_rc(fix, at, visual_name="visual-review-v2.json"):
    pub = fix.src / "publication" / "v2"
    candidate = pub / "publication-candidate-v2.json"
    publication.build_candidate(
        ROOT, fix.ISSUE if hasattr(fix, "ISSUE") else "2026-W35",
        "WEEKLY_MAGAZINE", pub / "reader-manuscript-v2.json",
        fix.survey / "main.tex", fix.survey / "main.pdf", 1,
        pub / "quality-regression-bundle-v2.json",
        pub / "semantic-editorial-review-v2.json",
        pub / visual_name, candidate)
    cfg = core.load_json(ROOT / core.DEFAULT_CONFIG)
    report = fix.src / "execution/validated-draft-stage-report.json"
    stage_validation.validate_stage(
        ROOT, cfg, fix.src / "production-state.json",
        {"publication-candidate": candidate}, report, at + timedelta(hours=1))
    reviews = fix.src / "execution/validated-draft-reviews.json"
    core.write_json(reviews, {"reviews": [{
        "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
        "executor": "parent-witness", "evidence": "w1",
        "result_path": str(report.relative_to(ROOT))}]})
    checkpoint = agent.build_stage_checkpoint(
        ROOT, cfg, fix.src / "production-state.json",
        {"publication-candidate": candidate}, reviews,
        "Parent witness Weekly boundary", at + timedelta(hours=1, minutes=1))
    updated = agent.advance_with_checkpoint(ROOT, cfg, fix.src / "production-state.json", checkpoint)
    assert updated["lifecycle_state"] == "RELEASE_CANDIDATE", updated
    return candidate


def approve_weekly(fix, at):
    cfg = core.load_json(ROOT / core.DEFAULT_CONFIG)
    return agent.approve_publication_preview(
        ROOT, cfg, fix.src / "production-state.json",
        "synthetic-human-fixture", at + timedelta(hours=2), "synthetic:publication-preview")


def w1a(REV, at) -> None:
    temp = tempfile.TemporaryDirectory(dir=str(ROOT))
    try:
        fix = REV.Fixture(ROOT, Path(temp.name))
        advance_weekly_rc(fix, at)
        approve_weekly(fix, at)
        cfg = core.load_json(ROOT / core.DEFAULT_CONFIG)
        pub = fix.src / "publication" / "v2"
        try:
            profiled.build_profiled_freeze(ROOT, cfg, fix.src / "production-state.json",
                                            at + timedelta(hours=3))
            record("W1a", "UNEXPECTED_SUCCESS",
                   {"note": "parent wrapper accepted canonical-shape visual via legacy validator"})
        except ValueError as exc:
            record("W1a", "PARENT_REFUSAL", {
                "error": str(exc)[:300],
                "freeze_exists": (pub / "freeze-record-v2.json").exists(),
                "manifest_exists": (pub / "release-manifest-v2.json").exists()})
    except Exception:
        record("W1a", "HARNESS_ERROR", {"trace": traceback.format_exc(limit=8)[-2000:]})
    finally:
        temp.cleanup()


def w1b(at) -> None:
    # Canonical VISUAL lives at a non-hardcoded path from fixture start, so
    # validation checkpoints bind it; the wrapper's hardcoded legacy path is
    # checkpoint-free and can hold an additional valid legacy record.
    try:
        fix = sf.SpecialFixture(ROOT, "SP001", "surveys/special/SP001",
                                visual_filename="visual-review-canonical-v2.json")
        try:
            pub = fix.src / "publication" / "v2"
            sf.advance_to_rc(fix, at)
            sf.approve(fix, at)
            cfg = core.load_json(ROOT / core.DEFAULT_CONFIG)
            approval = fix.src / cfg["state_authority"]["publication_preview_approval_path"]
            publication.build_visual_review(
                ROOT, approval,
                [{"check_id": "VISUAL_CONFIRM", "status": "PASS", "detail": "parent witness legacy"}],
                "fixture-tool", at + timedelta(hours=2, minutes=30),
                pub / "visual-review-v2.json")
            try:
                from scripts import survey_profiled_freeze_v2 as profiled_mod
                profiled_mod.build_profiled_freeze(
                    ROOT, cfg, sf.state_path(fix), at + timedelta(hours=3))
                record("W1b", "UNEXPECTED_SUCCESS",
                       {"note": "legacy at hardcoded path froze cleanly"})
            except ValueError as exc:
                record("W1b", "PARENT_LATE_REFUSAL", {
                    "error": str(exc)[:300],
                    "freeze_exists": (pub / "freeze-record-v2.json").exists(),
                    "freeze_sha": core.sha256_file(pub / "freeze-record-v2.json")
                    if (pub / "freeze-record-v2.json").is_file() else None,
                    "manifest_exists": (pub / "release-manifest-v2.json").exists(),
                    "manifest_sha": core.sha256_file(pub / "release-manifest-v2.json")
                    if (pub / "release-manifest-v2.json").is_file() else None})
        finally:
            shutil.rmtree(fix.src, ignore_errors=True)
            shutil.rmtree(fix.survey, ignore_errors=True)
    except Exception:
        record("W1b", "HARNESS_ERROR", {"trace": traceback.format_exc(limit=8)[-2000:]})


def load_publication_tests():
    spec = importlib.util.spec_from_file_location(
        "parent_wit_publication_tests", ROOT / "tests/test_survey_publication_v2.py")
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_second_chain(t, issue="SP001") -> dict:
    """Second valid chain: same issue/profile/source/PDF, distinct bundle/review/candidate bytes+paths.

    The manuscript primary source must be canonical survey_root/main.tex, so
    C2 shares C1's source, PDF and manuscript but carries its own quality
    bundle (different deterministic evidence), reviews (different detail)
    and candidate file. Same issue, byte-identical PDF, distinct Candidate
    path/hash — the contract's mixed-Candidate shape.
    """
    p1dir = t.root / f"sources/{issue}/publication/v2"
    profile = t.root / f"sources/{issue}/production-profile.json"
    survey_root = t.root / quality.core.load_json(profile)["paths"]["survey_root"]
    pdf = survey_root / "main.pdf"
    source = survey_root / "main.tex"
    manifest1 = p1dir / "reader-manuscript-v2.json"
    detdir = p1dir / "quality-results-2"
    detdir.mkdir(parents=True, exist_ok=True)
    cfg = quality.core.load_json(t.root / quality.core.DEFAULT_CONFIG)
    checks = []
    for check_id in sorted(quality.expected_checks_by_kind(
            cfg, "THEMATIC", "LONGFORM_SPECIAL", {"DETERMINISTIC"})):
        result_path = detdir / f"{check_id}.json"
        quality.core.write_json(result_path, {"check_id": check_id, "status": "PASS", "chain": 2})
        checks.append({
            "check_id": check_id, "kind": "DETERMINISTIC", "status": "PASS",
            "executor": "parent-witness-second-chain", "evidence": f"second-chain:{check_id}",
            "recorded_at": "2026-08-23T07:00:00Z",
            "result": {"path": str(result_path.relative_to(t.root)),
                        "sha256": quality.core.sha256_file(result_path)}})
    bundle2 = p1dir / "quality-regression-bundle-2-v2.json"
    quality.build_bundle(t.root, issue, source, pdf, checks, bundle2,
                         production_profile_path=profile)

    def _checks2(kind: str) -> list[dict]:
        rows = t._review_checks(profile, kind)
        for row in rows:
            row["detail"] = "Second-chain ChatGPT review passed " + row["check_id"]
        return rows

    sem2 = p1dir / "semantic-editorial-review-2-v2.json"
    vis2 = p1dir / "visual-review-2-v2.json"
    reader.build_review_record(t.root, manifest1, pdf, 12, "SEMANTIC_EDITORIAL",
                               _checks2("SEMANTIC_EDITORIAL"), "ChatGPT", t.now, sem2)
    reader.build_review_record(t.root, manifest1, pdf, 12, "VISUAL",
                               _checks2("VISUAL"), "ChatGPT", t.now, vis2)
    candidate2 = p1dir / "publication-candidate-2-v2.json"
    publication.build_candidate(
        t.root, issue, "LONGFORM_SPECIAL", manifest1, source, pdf, 12,
        bundle2, sem2, vis2, candidate2)
    return {"candidate2": candidate2, "pdf2": pdf}


def w2(PUBMOD, at) -> None:
    t = PUBMOD.SurveyPublicationV2Tests()
    try:
        t.setUp()
        try:
            p1 = t._candidate()
            c1 = p1["candidate"]
            approval1 = p1["publication_dir"] / "publication-preview-approval-v2.json"
            publication.build_preview_approval(
                t.root, c1, approval1, "human-reviewer", t.now, "review:SP001:preview")
            c2info = build_second_chain(t)
            c2 = c2info["candidate2"]
            sha1 = core.sha256_file(c1)
            sha2 = core.sha256_file(c2)
            pdf_same = (core.sha256_file(p1["pdf"]) == core.sha256_file(c2info["pdf2"]))
            freeze = p1["publication_dir"] / "freeze-mixed-v2.json"
            manifest = p1["publication_dir"] / "release-manifest-mixed-v2.json"
            try:
                publication.build_freeze(t.root, c2, approval1, t.now, freeze, manifest)
                record("W2", "PARENT_MIXED_ACCEPTED", {
                    "candidate1_sha": sha1[:16], "candidate2_sha": sha2[:16],
                    "distinct_paths": str(c1) != str(c2), "pdf_sha_equal": pdf_same,
                    "freeze_exists": freeze.is_file(), "manifest_exists": manifest.is_file()})
            except ValueError as exc:
                record("W2", "PARENT_REFUSED", {"error": str(exc)[:300]})
        except Exception:
            record("W2", "HARNESS_ERROR", {"trace": traceback.format_exc(limit=10)[-2000:]})
    finally:
        try:
            t.doCleanups()
        except Exception:
            pass


def w4(PUBMOD, at) -> None:
    t = PUBMOD.SurveyPublicationV2Tests()
    try:
        t.setUp()
        try:
            p1 = t._candidate()
            c1 = p1["candidate"]
            approval1 = p1["publication_dir"] / "publication-preview-approval-v2.json"
            publication.build_preview_approval(
                t.root, c1, approval1, "human-reviewer", t.now, "review:SP001:preview")
            freeze = p1["publication_dir"] / "freeze-record-v2.json"
            manifest = p1["publication_dir"] / "release-manifest-v2.json"
            foreign = {"schema_version": "2.0-rc1", "foreign": "pre-existing-divergent"}
            core.write_json(manifest, foreign)
            before_manifest = manifest.read_bytes()
            try:
                publication.build_freeze(t.root, c1, approval1, t.now, freeze, manifest)
                record("W4", "UNEXPECTED_SUCCESS", {"note": "divergent manifest overwritten"})
            except ValueError as exc:
                record("W4", "PARENT_CONFLICT", {
                    "error": str(exc)[:300],
                    "freeze_exists": freeze.is_file(),
                    "freeze_sha": core.sha256_file(freeze) if freeze.is_file() else None,
                    "manifest_unchanged": manifest.read_bytes() == before_manifest})
        except Exception:
            record("W4", "HARNESS_ERROR", {"trace": traceback.format_exc(limit=10)[-2000:]})
    finally:
        try:
            t.doCleanups()
        except Exception:
            pass


def w3(at) -> None:
    for issue, survey_rel, expect in (
            ("SP001", "surveys/special/SP001", "PredicatePass"),
            ("SP002", "surveys/special/SP002-DIVERGED", "PredicateReject")):
        try:
            fix = sf.SpecialFixture(ROOT, issue, survey_rel)
            try:
                cand = sf.advance_to_rc(fix, at)
                sf.approve(fix, at)
                pub = fix.src / "publication" / "v2"
                freeze = pub / "freeze-record-v2.json"
                manifest = pub / "release-manifest-v2.json"
                publication.build_freeze(ROOT, cand,
                                         fix.src / fix.cfg["state_authority"]["publication_preview_approval_path"],
                                         at + timedelta(hours=3), freeze, manifest)
                man = core.load_json(manifest)
                cand_payload = publication.validate_candidate(ROOT, cand, issue_id=issue)
                artifacts = {
                    "visual-review-record": ROOT / cand_payload["visual_review"]["path"],
                    "freeze-record": freeze, "release-manifest": manifest}
                sf.advance_to_frozen(fix, artifacts, at, suffix=f"W3-{issue}")
                state_sha = core.sha256_file(sf.state_path(fix))
                man_sha = core.sha256_file(manifest)
                outdir = Path(f"/tmp/opencode/dm001019-scratch-20261003T100801Z/wf-{issue}")
                code, out, err = sf.run_workflow_predicate(ROOT, issue, state_sha, man_sha, outdir)
                record(f"W3-{issue}", "WORKFLOW_EXIT", {
                    "exit": code, "expected": expect,
                    "manifest_tag": man["release_identity"],
                    "stdout_tail": out[-800:], "stderr_tail": err[-800:]})
            finally:
                shutil.rmtree(fix.src, ignore_errors=True)
                shutil.rmtree(fix.survey, ignore_errors=True)
        except Exception:
            record(f"W3-{issue}", "HARNESS_ERROR", {"trace": traceback.format_exc(limit=10)[-2000:]})


def main() -> int:
    assert head() == EXPECTED_HEAD, f"parent HEAD mismatch: {head()}"
    at = sf.T0
    REV = load_revalidation_fixture()
    PUBMOD = load_publication_tests()
    w1a(REV, at)
    w1b(at)
    w2(PUBMOD, at)
    w4(PUBMOD, at)
    w3(at)
    out = Path("/tmp/opencode/dm001019-scratch-20261003T100801Z/parent-witness-results.jsonl")
    with out.open("w", encoding="utf-8") as fh:
        for row in RESULTS:
            fh.write(json.dumps(row, sort_keys=True) + "\n")
    print(f"HEAD_AFTER={head()}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
