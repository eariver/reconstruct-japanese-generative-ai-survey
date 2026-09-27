#!/usr/bin/env python3
"""Bounded mechanical-refresh witness harness (fixture-only, disposable).

Author-side General Co-Worker execution of outputs/rephase-1-weekly-regeneration-decision.md
W0-W6. Ships NO candidate/runtime/test changes. Only writes documentary evidence under
notes/rephase-1-weekly-regeneration/ (harness lives there; logs/identities sidecars there)
and mutates ONLY the disposable edition repo passed via --edition.

Each phase is invoked as a separate OS process (fresh interpreter/imports):
    witness_harness.py w0|w1|w2|w3|w4|w5|w6 --edition <dir> --logs <dir> [--run-id <id>]

Tooling note: Astra asked for apply_patch authoring; this execution environment exposes
only read/write/edit + shell, so this file was authored with the write tool. Bulk source
copying (318+ files) uses `git ls-files` + shutil.copyfile (no hardlinks, no archives,
no shell binary handling); shell git is used only for rev-parse/status/diff/log/commit
metadata with parent verification. Reason recorded here and in the witness report.

Harness preconditions (W2/W5 equality + criteria checks) are HARNESS POLICY enforced by
this script. They are NOT shipping-code guards; the report labels them as such. A wrapper
refusal below never stands in for a production API rejection; every runtime boundary is
additionally exercised through the real loader/validator/CLI call and its raw error.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

E4C_REPO = Path("/tmp/jgas-rephase-gate-cli")
E4C_HEAD = "e4c82692abee6acedbba07815b0d74ccefb80a7e"
E4C_TREE = "bc377b6b7eb1e47dacd719e0f76b5a86703f3f3e"
B_REPO = Path("/tmp/jgas-rephase-increment-b-sol-implementation")
B_HEAD = "c04f32ad46109403e8a63faaa8394a90ee6b869c"
COPY_TOPS = ["config", "docs", "schemas", "scripts", "templates", "tests"]
# Content-boundary rationale (report §): B/gate-proven subset (config/docs/schemas/scripts/
# templates) + tests/ so post-commit fresh processes import constructors AND runtime from the
# single edition root. tests/ is outside _verify_head_bytes control paths, CURRENT_CLOSURE
# names, closed build inventory and stage rows, hence cannot affect witness oracles.
VENV_PYTHON = Path("/tmp/jgas-rephase-application-venv/bin/python")
GIT_ENV_OVERRIDES = (
    "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR",
)
WITNESS_IDENTITY = {
    "GIT_AUTHOR_NAME": "Synthetic Witness Fixture",
    "GIT_AUTHOR_EMAIL": "synthetic-witness@example.invalid",
    "GIT_COMMITTER_NAME": "Synthetic Witness Fixture",
    "GIT_COMMITTER_EMAIL": "synthetic-witness@example.invalid",
}
SYNTHETIC_REVIEWER = "synthetic witness reviewer (not human)"
SYNTHETIC_REASON_FIRST = (
    "Synthetic witness first mechanical refresh after comment-only control change; "
    "not a human judgment"
)
SYNTHETIC_REASON_SECOND = (
    "Synthetic witness second mechanical refresh after comment-only control change; "
    "not a human judgment"
)
CRITERIA_FILES = [
    "config/publication-review-v2.json",
    "config/survey-production-v2.json",
    "schemas/reader-surface-semantic-review-v2.schema.json",
    "schemas/reader-surface-gate-v2.schema.json",
    "schemas/reader-manuscript-v2.schema.json",
    "schemas/publication-review-record-v2.schema.json",
    "schemas/quality-regression-bundle-v2.schema.json",
    "schemas/weekly-publication-source-manifest-v2.schema.json",
    "schemas/reader-surface-input-v2.schema.json",
]


def utc_now_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_object(value) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def git_env(extra: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if k not in GIT_ENV_OVERRIDES}
    env.update(WITNESS_IDENTITY)
    if extra:
        env.update(extra)
    return env


def run_git(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=str(cwd), env=git_env(),
        capture_output=True, text=True, encoding="utf-8", errors="replace", check=check,
    )


def tree_snapshot(root: Path) -> dict[str, str]:
    snap: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if rel.parts and rel.parts[0] == ".git":
            continue
        snap[str(rel).replace("\\", "/")] = sha_file(path)
    return snap


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def check_e4c_intact(log: list[str]) -> None:
    head = subprocess.run(
        ["git", "-C", str(E4C_REPO), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    assert head == E4C_HEAD, f"e4c8269 fixture moved: {head}"
    tree = subprocess.run(
        ["git", "-C", str(E4C_REPO), "show", "-s", "--format=%T", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    assert tree == E4C_TREE, f"e4c8269 tree moved: {tree}"
    bhead = subprocess.run(
        ["git", "-C", str(B_REPO), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    assert bhead == B_HEAD, f"B fixture moved: {bhead}"
    log.append(f"preserved e4c8269 HEAD/tree {head}/{tree}; B HEAD {bhead}")


def check_no_inherited_git_overrides() -> None:
    bad = [n for n in GIT_ENV_OVERRIDES if os.environ.get(n)]
    assert not bad, f"unsafe inherited Git overrides: {bad}"


def check_edition(edition: Path, expect_head: str | None = None) -> dict:
    assert edition.is_dir(), f"edition missing: {edition}"
    assert edition.resolve() != E4C_REPO.resolve(), "refusing to mutate e4c8269 fixture"
    assert edition.resolve() != B_REPO.resolve(), "refusing to mutate B fixture"
    marker = edition / ".witness-edition-marker.json"
    assert marker.is_file(), f"edition marker missing: {marker}"
    meta = json.loads(marker.read_text())
    assert meta.get("e4c_source") == E4C_HEAD, "edition marker source mismatch"
    if expect_head is not None:
        head = run_git(["rev-parse", "HEAD"], edition).stdout.strip()
        assert head == expect_head, f"edition HEAD {head} != expected {expect_head}"
    return meta


def tracked_clean(edition: Path) -> tuple[str, str]:
    status_all = run_git(["status", "--porcelain=v1"], edition, check=False).stdout
    status_tracked = run_git(
        ["status", "--porcelain=v1", "--untracked-files=no"], edition, check=False
    ).stdout
    return status_all, status_tracked


def clear_pycache(edition: Path, log: list[str]) -> None:
    removed = 0
    for cache in (edition / "scripts" / "__pycache__", edition / "tests" / "__pycache__"):
        if cache.is_dir():
            shutil.rmtree(cache)
            removed += 1
    log.append(f"cleared __pycache__ dirs: {removed}")


def fresh_import_check(edition: Path, log: list[str]) -> None:
    env = {k: v for k, v in os.environ.items() if k not in GIT_ENV_OVERRIDES}
    env["PYTHONPATH"] = str(edition)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [str(VENV_PYTHON), "-c",
         "import scripts.survey_weekly_derivation_v2 as m; print(m.__file__)"],
        cwd=str(edition), env=env, capture_output=True, text=True,
    )
    assert proc.returncode == 0, f"fresh import failed: {proc.stderr[-2000:]}"
    src = proc.stdout.strip()
    assert src.startswith(str(edition.resolve())), f"stale module source: {src}"
    log.append(f"fresh interpreter imports weekly derivation from edition: {src}")


def setup_base(edition: Path):
    from scripts import survey_production_v2 as core
    from tests import test_survey_increment_b_weekly_derivation_v2 as weekly_b
    base = weekly_b.IncrementBWeeklyDerivationV2Tests(
        methodName="test_accepted_weekly_two_pass_publication")
    base.root = edition.resolve()
    base.cfg = core.load_json(base.root / core.DEFAULT_CONFIG)
    base.head = core.repository_commit_sha(base.root)
    base.source_root = base.root / "sources" / weekly_b.ISSUE
    base.survey_root = base.root / "surveys" / "weekly" / weekly_b.ISSUE
    return base, weekly_b


def advance_like_b(base, chain: dict, stage: str, artifacts: dict, minute: int) -> None:
    from scripts import survey_production_v2 as core
    from scripts import survey_agent_control_v2 as agent
    from scripts import survey_stage_validation_v2 as stage_validation
    state_path = base.source_root / "production-state.json"
    assert core.load_json(state_path)["lifecycle_state"] == stage
    stamp = core.parse_instant(f"2026-09-19T{4 + minute // 60:02d}:{minute % 60:02d}:00+09:00")
    report = base.source_root / "orchestration/v2/reviews" / f"{stage}-core-contract.json"
    stage_validation.validate_stage(base.root, base.cfg, state_path, artifacts, report, stamp)
    review_path = report.with_name(f"{stage}-reviews.json")
    core.write_json(review_path, {"reviews": [{
        "check_id": "CORE_STAGE_CONTRACT", "kind": "DETERMINISTIC",
        "executor": "synthetic witness fixture using actual stage validator",
        "evidence": "actual stage validator PASS for exact synthetic edition authorities",
        "result_path": str(report.relative_to(base.root)),
    }]})
    checkpoint = agent.build_stage_checkpoint(
        base.root, base.cfg, state_path, artifacts, review_path,
        f"Synthetic witness {stage} fixture stage was validated.", stamp)
    updated = agent.advance_with_checkpoint(base.root, base.cfg, state_path, checkpoint)
    assert agent.validate_agent_state(base.root, base.cfg, updated) == []


def synthetic_pretex_review(issue: str, surface_rel: str, surface_sha: str) -> dict:
    from scripts import survey_production_v2 as core
    doc = {
        "schema_version": "2.0-rc1", "issue_id": issue,
        "publication_profile": "WEEKLY_MAGAZINE", "review_kind": "SEMANTIC_EDITORIAL",
        "reviewed_surface": {"path": surface_rel, "sha256": surface_sha},
        "checks": [{
            "check_id": "READER_PIPELINE_INDEPENDENCE", "status": "PASS",
            "detail": "Synthetic witness reviewer judged complete fixture prose independently understandable.",
            "evidence_locations": ["reader-surface-input-v2.json:packages",
                                   "reader-surface-input-v2.json:bibliography"],
        }],
        "decision": "PASS", "reviewed_by": SYNTHETIC_REVIEWER,
        "reviewed_at": "2026-09-19T05:00:00+09:00", "recorded_at": "2026-09-19T05:00:00+09:00",
        "status": "PASSED", "findings": [],
        "summary": "Synthetic witness PASS; not a human judgment.",
    }
    doc["review_sha256"] = core.sha256_object(doc)
    return doc


def run_gate_cli(edition: Path, manuscript_rel: str, review_rel: str,
                 state: Path, out_rel: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if k not in GIT_ENV_OVERRIDES}
    env["PYTHONPATH"] = str(edition)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    cmd = [str(VENV_PYTHON), str(edition / "scripts/survey_reader_surface_gate_v2.py"),
           "--repo-root", str(edition), "scan-manuscript",
           "--manuscript", manuscript_rel, "--semantic-authority", review_rel,
           "--state", str(state), "--output", out_rel]
    return subprocess.run(cmd, cwd=str(edition), env=env,
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def run_revalidate_cli(edition: Path, state: Path, reason: str, executor: str,
                       recorded_at_iso: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if k not in GIT_ENV_OVERRIDES}
    env["PYTHONPATH"] = str(edition)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    cmd = [str(VENV_PYTHON), str(edition / "scripts/survey_agent_control_v2.py"),
           "--repo-root", str(edition), "revalidate-publication-surface",
           "--state", str(state), "--reason-class", "REVIEWED_CORE_CHANGE",
           "--reason", reason, "--executor", executor, "--recorded-at", recorded_at_iso]
    return subprocess.run(cmd, cwd=str(edition), env=env,
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def log_runtime_source(log: list[str], tag: str) -> None:
    import scripts.survey_production_v2 as core_probe
    log.append(f"{tag} runtime scripts imported from: {core_probe.__file__}")


def key_hashes(base, chain: dict, state_path: Path, extra: dict) -> dict:
    from scripts import survey_production_v2 as core
    pub = base.source_root / "publication/v2"
    paths = {
        "state": state_path,
        "profile": chain["profile_path"],
        "architecture": base.source_root / "architecture-v2.json",
        "synthesis_input": chain["synthesis_input_path"],
        "synthesis_result": chain["synthesis_result_path"],
        "archive": chain["archive_path"],
        "authored": chain["authored_path"],
        "surface": pub / "reader-surface-input-v2.json",
        "pretex_review": pub / "reader-surface-semantic-review-v2.json",
        "receipt": pub / "validated-source-manifest.json",
        "manuscript": pub / "reader-manuscript-v2.json",
        "gate": pub / "reader-surface-gate-v2.json",
        "main_tex": base.survey_root / "main.tex",
        "references_bib": base.survey_root / "references.bib",
        "style": base.survey_root / "jgaisurvey.sty",
        "pdf": base.survey_root / "main.pdf",
        "bundle": pub / "quality-regression-bundle-v2.json",
        "semantic_review": pub / "semantic-editorial-review-v2.json",
        "visual_review": pub / "visual-review-v2.json",
    }
    out = {}
    for name, path in paths.items():
        out[name] = {"rel": str(path.relative_to(base.root)).replace("\\", "/")
                     if path.exists() else None,
                     "sha256": sha_file(path) if path.is_file() else None}
    out["criteria"] = {rel: sha_file(base.root / rel) for rel in CRITERIA_FILES}
    out.update(extra)
    return out


# -------------------------------------------------------------------------- phases

def phase_w0a(args) -> int:
    """Create the disposable edition repo and commit the H0 source basis (stdlib only).

    No scripts/tests imports here: the edition does not exist yet, so runtime imports
    resolve after H0 in phase_w0b from the edition root (single provenance).
    """
    logs = Path(args.logs)
    logs.mkdir(parents=True, exist_ok=True)
    log: list[str] = []
    run_id = args.run_id or utc_now_compact()
    check_no_inherited_git_overrides()
    check_e4c_intact(log)
    edition = Path(args.edition).resolve()
    assert edition != E4C_REPO.resolve() and edition != B_REPO.resolve()
    parent = edition.parent
    assert parent.is_dir(), f"edition parent missing: {parent}"
    assert not edition.exists(), f"edition already exists: {edition}"
    edition.mkdir(parents=True)
    # Bulk copy: read-only git ls-files on e4c + copyfile (no hardlinks/archives).
    listed = subprocess.run(
        ["git", "-C", str(E4C_REPO), "ls-files", "-z", "--", *COPY_TOPS],
        capture_output=True, check=True).stdout
    copied = []
    for raw in listed.split(b"\0"):
        if not raw:
            continue
        rel = Path(raw.decode("utf-8"))
        dst = edition / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(E4C_REPO / rel, dst)
        copied.append(rel.as_posix())
    boundary_hash = sha_object(sorted(copied))
    log.append(f"copied {len(copied)} files under {COPY_TOPS}; boundary hash {boundary_hash}")
    write_json(edition / ".witness-edition-marker.json", {
        "edition": edition.name, "e4c_source": E4C_HEAD, "e4c_tree": E4C_TREE,
        "content_boundary_tops": COPY_TOPS, "content_files": len(copied),
        "content_boundary_hash": boundary_hash,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "bounded mechanical-refresh witness (disposable)",
    })
    for cmd in (["init", "-q"],
                ["remote", "add", "origin", "https://example.invalid/witness-edition.git"],
                ["add", "-A"],
                ["commit", "-q", "-m", "Synthetic isolated witness source basis"]):
        run_git(cmd, edition)
    h0 = run_git(["rev-parse", "HEAD"], edition).stdout.strip()
    h0_tree = run_git(["show", "-s", "--format=%T", "HEAD"], edition).stdout.strip()
    h0_log = run_git(["log", "--oneline", "-3"], edition).stdout.strip()
    status_all, status_tracked = tracked_clean(edition)
    assert status_tracked.strip() == "", f"H0 worktree not clean: {status_tracked[:500]}"
    log.append(f"H0 {h0} tree {h0_tree}\n{h0_log}\nstatus bytes={len(status_all)}")
    write_json(logs / "w0a-sidecar.json", {
        "phase": "w0a", "run_id": run_id, "edition": edition.name,
        "e4c_source": E4C_HEAD, "e4c_tree": E4C_TREE, "h0": h0, "h0_tree": h0_tree,
        "content_files": len(copied), "content_boundary_hash": boundary_hash})
    (logs / "w0a.log").write_text("\n".join(log) + "\n")
    print(f"W0a OK h0={h0} files={len(copied)}")
    return 0


def phase_w0b(args) -> int:
    """Construct the VALIDATED_DRAFT baseline in the H0 edition (fresh process).

    scripts/tests resolve from the edition root (exists since w0a); H0 boundary bytes
    are identical to the e4c source boundary, so this is the same code under test.
    """
    from scripts import survey_production_v2 as core
    from scripts import survey_agent_control_v2 as agent
    from scripts import survey_reader_publication_v2 as reader_publication
    from scripts import survey_reader_surface_gate_v2 as reader_gate
    from scripts import survey_quality_v2 as quality
    from scripts import survey_weekly_derivation_v2 as weekly
    from pypdf import PdfReader, PdfWriter
    logs = Path(args.logs)
    log: list[str] = []
    run_id = args.run_id or utc_now_compact()
    check_no_inherited_git_overrides()
    check_e4c_intact(log)
    edition = Path(args.edition).resolve()
    meta = check_edition(edition)
    w0a = json.loads((logs / "w0a-sidecar.json").read_text())
    h0 = w0a["h0"]
    assert run_git(["rev-parse", "HEAD"], edition).stdout.strip() == h0, "W0b must start at H0"
    log.append(f"W0b starting at H0 {h0} (content files={meta.get('content_files')})")
    log_runtime_source(log, "W0b")
    # W0 construction with edition-root imports (H0 bytes == e4c boundary bytes).
    base, weekly_b = setup_base(edition)
    assert base.head == h0
    from scripts import survey_weekly_semantic_publication_v2 as weekly_publication
    chain = base._complete_authorities(base._chain())
    state_path = base._current_state(chain)
    assert core.load_json(state_path)["lifecycle_state"] == "DRAFT_COMPLETE"
    argv = ["survey_weekly_semantic_publication_v2.py", "--repo-root", str(base.root),
            "--state", str(state_path), "--input", str(chain["authored_path"])]
    with mock.patch.object(sys, "argv", argv + ["--materialize-surface-only"]):
        assert weekly_publication.main() == 0
    publication_root = base.source_root / "publication/v2"
    surface_path = publication_root / "reader-surface-input-v2.json"
    assert surface_path.is_file()
    try:
        with mock.patch.object(sys, "argv", argv):
            weekly_publication.main()
        raise AssertionError("publisher unexpectedly materialized without review")
    except SystemExit as exc:
        assert "semantic review artifact missing" in str(exc), str(exc)[:300]
        log.append("W0 publisher correctly refuses TeX materialization without review")
    review_path = publication_root / "reader-surface-semantic-review-v2.json"
    core.write_json(review_path, synthetic_pretex_review(
        weekly_b.ISSUE, str(surface_path.relative_to(base.root)).replace("\\", "/"),
        core.sha256_file(surface_path)))
    with mock.patch.object(sys, "argv", argv):
        assert weekly_publication.main() == 0
    receipt_path = publication_root / "validated-source-manifest.json"
    assert receipt_path.is_file()
    weekly.validate_receipt(base.root, receipt_path, state_path)
    log.append("W0 publisher two-pass + receipt replay OK")
    architecture = core.load_json(base.source_root / "architecture-v2.json")
    coverage = [{"package_id": p["package_id"], "requirement": r, "status": "FULFILLED",
                 "reader_locations": ["main.tex:package-1"],
                 "detail": "Synthetic witness author maps accepted requirement to source section."}
                for p in architecture["packages"] for r in p["must_cover_requirements"]]
    requirements = [{"requirement_id": k, "status": "FULFILLED", "reader_locations": [loc],
                     "detail": "Synthetic witness author asserts visible requirement present."}
                    for k, loc in (("FINAL_SYNTHESIS", "main.tex:summary"),
                                    ("WEEKLY_COMMUNITY_MOVEMENT", "main.tex:package-1"))]
    manuscript_path = publication_root / "reader-manuscript-v2.json"
    reader_publication.build_manuscript_manifest(
        base.root, weekly_b.ISSUE, chain["profile_path"],
        base.source_root / "architecture-v2.json", chain["approval_path"],
        base.survey_root / "main.tex",
        [{"role": "BIBLIOGRAPHY",
          "path": str((base.survey_root / "references.bib").relative_to(base.root))},
         {"role": "STYLE",
          "path": str((base.survey_root / "jgaisurvey.sty").relative_to(base.root))}],
        coverage, requirements, "synthetic witness manuscript author",
        core.parse_instant("2026-09-19T05:10:00+09:00"), manuscript_path)
    gate_rel = str((publication_root / "reader-surface-gate-v2.json").relative_to(base.root))
    proc = run_gate_cli(
        edition, str(manuscript_path.relative_to(base.root)).replace("\\", "/"),
        str(review_path.relative_to(base.root)).replace("\\", "/"), state_path, gate_rel)
    (logs / "w0-gate-cli.out.txt").write_text(proc.stdout)
    (logs / "w0-gate-cli.err.txt").write_text(proc.stderr)
    (logs / "w0-gate-cli.exit").write_text(str(proc.returncode))
    assert proc.returncode == 0, proc.stderr[-2000:]
    gate_path = publication_root / "reader-surface-gate-v2.json"
    gate = reader_gate.validate_reader_surface_gate(
        base.root, gate_path, issue_id=weekly_b.ISSUE,
        publication_profile="WEEKLY_MAGAZINE",
        expected_manuscript_path=manuscript_path, state_path=state_path)
    assert gate["status"] == "PASSED" and gate["derivation"]["route"] == weekly.ROUTE
    log.append("W0 Gate via fixed CLI PASSED (WEEKLY_GENERATED_V2)")
    pdf_path = base.survey_root / "main.pdf"
    pdf = PdfWriter()
    pdf.add_blank_page(width=595, height=842)
    with pdf_path.open("wb") as fh:
        pdf.write(fh)
    assert len(PdfReader(str(pdf_path)).pages) == 1
    log_path = base.survey_root / "main.log"
    checksum_path = base.survey_root / "main.pdf.sha256"
    log_path.write_text("synthetic build log\n", encoding="utf-8")
    checksum_path.write_text(core.sha256_file(pdf_path) + "  main.pdf\n", encoding="utf-8")
    weekly.validate_receipt(base.root, receipt_path, state_path)
    reader_gate.validate_reader_surface_gate(
        base.root, gate_path, expected_manuscript_path=manuscript_path, state_path=state_path)
    log_path.unlink()
    checksum_path.unlink()
    log.append("W0 synthetic PDF accepted with log/digest present; log+digest removed (canonical root keeps 3 inputs + PDF)")
    quality_root = publication_root / "quality"
    subject_path = quality_root / "subject-entity-property-binding.json"
    assert core.load_json(subject_path)["status"] == "PASS"
    main_text = (base.survey_root / "main.tex").read_text(encoding="utf-8")
    assert weekly_b.ISSUE in main_text
    for check_id, fname, payload in (
        ("IDENTIFIER_PRESERVATION", "identifier-preservation.json", {
            "check_id": "IDENTIFIER_PRESERVATION", "status": "PASS",
            "source_sha256": core.sha256_file(base.survey_root / "main.tex"),
            "inspected_identifiers": [weekly_b.ISSUE], "scope": "synthetic witness fixture"}),
        ("PDF_PREFLIGHT", "pdf-preflight.json", {
            "check_id": "PDF_PREFLIGHT", "status": "PASS", "page_count": 1,
            "pdf_sha256": core.sha256_file(pdf_path), "byte_count": pdf_path.stat().st_size,
            "scope": "synthetic parseable one-page PDF; not a TeX rendering"}),
    ):
        core.write_json(quality_root / fname, payload)
    result_paths = {"SUBJECT_ENTITY_PROPERTY_BINDING": subject_path,
                    "IDENTIFIER_PRESERVATION": quality_root / "identifier-preservation.json",
                    "PDF_PREFLIGHT": quality_root / "pdf-preflight.json"}
    quality_checks = [{"check_id": cid, "kind": "DETERMINISTIC", "status": "PASS",
                       "executor": "synthetic witness fixture with actual file assertions",
                       "evidence": "Exact fixture bytes and result file inspected by harness.",
                       "recorded_at": "2026-09-19T05:20:00+09:00",
                       "result": {"path": str(p.relative_to(base.root)).replace("\\", "/"),
                                  "sha256": core.sha256_file(p)}}
                      for cid, p in result_paths.items()]
    bundle_path = publication_root / "quality-regression-bundle-v2.json"
    quality.build_bundle(base.root, weekly_b.ISSUE, base.survey_root / "main.tex", pdf_path,
                         quality_checks, bundle_path,
                         production_profile_path=chain["profile_path"])
    review_paths = {}
    profile = core.load_json(chain["profile_path"])
    for kind, name in (("SEMANTIC_EDITORIAL", "semantic-editorial-review-v2.json"),
                       ("VISUAL", "visual-review-v2.json")):
        checks = [{"check_id": cid, "status": "PASS",
                   "detail": "Synthetic witness review; no real editorial or visual acceptance asserted.",
                   "evidence_locations": ["synthetic-fixture:main.tex"]}
                  for cid in sorted(reader_publication._expected_review_checks(base.root, profile, kind))]
        path = publication_root / name
        reader_publication.build_review_record(
            base.root, manuscript_path, pdf_path, 1, kind, checks,
            f"synthetic witness {kind} reviewer",
            core.parse_instant("2026-09-19T05:30:00+09:00"), path)
        review_paths[kind] = path
    advance_like_b(base, chain, "DRAFT_COMPLETE", {
        "reader-manuscript": manuscript_path,
        "validated-source": base.survey_root / "main.tex",
        "publication-pdf": pdf_path,
        "quality-regression-bundle": bundle_path,
        "semantic-review": review_paths["SEMANTIC_EDITORIAL"],
        "visual-review": review_paths["VISUAL"],
        "reader-surface-gate": gate_path}, 130)
    assert core.load_json(state_path)["lifecycle_state"] == "VALIDATED_DRAFT"
    assert core.load_json(state_path).get("publication_revalidation_provenance") is None
    assert agent.validate_agent_state(base.root, base.cfg, core.load_json(state_path)) == []
    weekly.validate_receipt(base.root, receipt_path, state_path)
    reader_gate.validate_reader_surface_gate(
        base.root, gate_path, expected_manuscript_path=manuscript_path, state_path=state_path)
    log.append("W0 VALIDATED_DRAFT reached; null pointer; strict State/receipt/Gate readback OK")
    validation_ref = core.load_json(state_path)["checkpoint_provenance"]["validation"]
    h0_tree = run_git(["show", "-s", "--format=%T", "HEAD"], edition).stdout.strip()
    sidecar = {
        "run_id": run_id, "phase": "w0", "edition": edition.name,
        "e4c_source": E4C_HEAD, "h0": h0, "h0_tree": h0_tree,
        "issue": weekly_b.ISSUE, "state_rel": str(state_path.relative_to(base.root)),
        "validation_checkpoint": validation_ref,
        "validation_checkpoint_sha256": sha_file(base.root / validation_ref["path"]),
        "hashes": key_hashes(base, chain, state_path, {}),
        "surface_sha256": core.sha256_file(surface_path),
        "render_main_sha256": hashlib.sha256(
            weekly.render_main(core.load_json(surface_path)).encode()).hexdigest(),
        "render_bib_sha256": hashlib.sha256(
            weekly.render_bibliography(core.load_json(surface_path)).encode()).hexdigest(),
        "tree": tree_snapshot(edition),
    }
    write_json(logs / "w0-sidecar.json", sidecar)
    (logs / "w0.log").write_text("\n".join(log) + "\n")
    print(f"W0 OK h0={h0} state=VALIDATED_DRAFT pointer=null")
    return 0


def commit_control_comment(edition: Path, marker: str, log: list[str]) -> tuple[str, str]:
    helper = edition / "scripts/survey_weekly_derivation_v2.py"
    before = helper.read_bytes()
    status_all, status_tracked = tracked_clean(edition)
    assert status_tracked.strip() == "", f"tracked dirty before {marker}: {status_tracked[:500]}"
    diff_preview = run_git(["diff", "--", "scripts/survey_weekly_derivation_v2.py"], edition)
    assert diff_preview.stdout.strip() == "", "helper unexpectedly dirty"
    helper.write_bytes(before + f"\n# witness-{marker}: mechanical identity comment only; no semantic change.\n".encode())
    diff = run_git(["diff", "--", "scripts/survey_weekly_derivation_v2.py"], edition).stdout
    assert marker in diff and diff.count("\n+") <= 3, diff[:1000]
    run_git(["add", "--", "scripts/survey_weekly_derivation_v2.py"], edition)
    run_git(["commit", "-q", "-m", f"Synthetic witness {marker} comment-only control change"], edition)
    head = run_git(["rev-parse", "HEAD"], edition).stdout.strip()
    parent = run_git(["log", "--format=%P", "-n", "1", "HEAD"], edition).stdout.strip()
    tree = run_git(["show", "-s", "--format=%T", "HEAD"], edition).stdout.strip()
    log.append(f"{marker} head={head} parent={parent} tree={tree}\n--- diff ---\n{diff}")
    clear_pycache(edition, log)
    return head, diff


def phase_w1(args) -> int:
    from scripts import survey_production_v2 as core
    from scripts import survey_agent_control_v2 as agent
    from scripts import survey_weekly_derivation_v2 as weekly
    from scripts import survey_reader_surface_gate_v2 as reader_gate
    logs = Path(args.logs)
    log: list[str] = []
    check_no_inherited_git_overrides()
    check_e4c_intact(log)
    edition = Path(args.edition).resolve()
    meta = check_edition(edition)
    w0 = json.loads((logs / "w0-sidecar.json").read_text())
    assert w0["h0"] == run_git(["rev-parse", "HEAD"], edition).stdout.strip(), "W1 must start at H0"
    h1, diff = commit_control_comment(edition, "H1", log)
    (logs / "w1-comment.patch").write_text(diff)
    fresh_import_check(edition, log)
    base, weekly_b = setup_base(edition)
    assert base.head == h1
    state_path = base.root / w0["state_rel"]
    assert core.load_json(state_path)["lifecycle_state"] == "VALIDATED_DRAFT"
    assert agent.validate_agent_state(base.root, base.cfg, core.load_json(state_path)) == []
    log.append("W1 strict State passes at H1 (HEAD not pinned by State validation)")
    chain_authored = base.root / w0["hashes"]["authored"]["rel"]
    context = weekly.load_derivation(base.root, state_path, chain_authored)
    assert core.sha256_file(base.root / w0["hashes"]["surface"]["rel"]) == w0["surface_sha256"]
    assert context["surface"] == core.load_json(base.root / w0["hashes"]["surface"]["rel"])
    log.append("W1 strict load_derivation passes at H1; recomputed surface identical")
    receipt_path = base.root / w0["hashes"]["receipt"]["rel"]
    try:
        weekly.validate_receipt(base.root, receipt_path, state_path)
        raise AssertionError("old receipt unexpectedly replayed at H1")
    except ValueError as exc:
        msg = str(exc)
        (logs / "w1-old-receipt.err.txt").write_text(msg)
        assert ("implementation or contract changed" in msg or "current-tool" in msg
                or "differ from exact committed basis" in msg), msg[:500]
        log.append(f"W1 old receipt rejects at old-tool boundary: {msg[:220]}")
    gate_path = base.root / w0["hashes"]["gate"]["rel"]
    manuscript_path = base.root / w0["hashes"]["manuscript"]["rel"]
    try:
        reader_gate.validate_reader_surface_gate(
            base.root, gate_path, issue_id=w0["issue"], publication_profile="WEEKLY_MAGAZINE",
            expected_manuscript_path=manuscript_path, state_path=state_path)
        raise AssertionError("old Gate unexpectedly validated at H1")
    except ValueError as exc:
        msg = str(exc)
        (logs / "w1-old-gate.err.txt").write_text(msg)
        log.append(f"W1 old Gate rejects (receipt derivation mismatch): {msg[:220]}")
    write_json(logs / "w1-sidecar.json", {"phase": "w1", "h1": h1, "h1_parent": w0["h0"],
                                          "tree": tree_snapshot(edition)})
    (logs / "w1.log").write_text("\n".join(log) + "\n")
    print(f"W1 OK h1={h1} strict-pass old-receipt-reject old-gate-reject")
    return 0


def harness_preconditions(base, w0: dict, log: list[str], tag: str) -> None:
    # HARNESS POLICY (not shipping code): byte-identity of the mechanical scope.
    # "state" is deliberately NOT hash-compared: State legitimately evolves through the
    # revalidation pointer (W4/W5). State integrity is enforced by the runtime validators
    # (strict validate_agent_state, pending-basis binding, pointer/chain checks), which are
    # strictly stronger than a byte comparison and are asserted separately at every step.
    from scripts import survey_production_v2 as core
    from scripts import survey_weekly_derivation_v2 as weekly
    keep = ["profile", "architecture", "synthesis_input", "synthesis_result",
            "archive", "authored", "surface", "pretex_review", "manuscript",
            "main_tex", "references_bib", "style", "pdf", "bundle",
            "semantic_review", "visual_review"]
    for name in keep:
        rel = w0["hashes"][name]["rel"]
        actual = sha_file(base.root / rel)
        assert actual == w0["hashes"][name]["sha256"], f"{tag} scope drift: {name}"
    for rel, digest in w0["hashes"]["criteria"].items():
        assert sha_file(base.root / rel) == digest, f"{tag} criteria drift: {rel}"
    surface = core.load_json(base.root / w0["hashes"]["surface"]["rel"])
    assert hashlib.sha256(weekly.render_main(surface).encode()).hexdigest() == w0["render_main_sha256"]
    assert hashlib.sha256(weekly.render_bibliography(surface).encode()).hexdigest() == w0["render_bib_sha256"]
    log.append(f"{tag} harness preconditions pass: accepted/authored/surface/render/PDF/manuscript/reviews/criteria identical (receipt/Gate excluded as refresh targets)")


def phase_w2(args) -> int:
    from scripts import survey_production_v2 as core
    from scripts import survey_schema_v2 as schema_gate
    from scripts import survey_weekly_derivation_v2 as weekly
    logs = Path(args.logs)
    log: list[str] = []
    check_no_inherited_git_overrides()
    check_e4c_intact(log)
    edition = Path(args.edition).resolve()
    check_edition(edition)
    w0 = json.loads((logs / "w0-sidecar.json").read_text())
    w1 = json.loads((logs / "w1-sidecar.json").read_text())
    assert run_git(["rev-parse", "HEAD"], edition).stdout.strip() == w1["h1"]
    base, weekly_b = setup_base(edition)
    state_path = base.root / w0["state_rel"]
    harness_preconditions(base, w0, log, "W2")
    fresh_import_check(edition, log)
    receipt_path = base.root / w0["hashes"]["receipt"]["rel"]
    evidence_dir = edition / ".witness-evidence"
    evidence_dir.mkdir(exist_ok=True)
    old_bytes = receipt_path.read_bytes()
    (evidence_dir / "receipt-superseded-H0.json").write_bytes(old_bytes)
    log.append(f"W2 preserved old receipt ({len(old_bytes)} B, sha {sha_file(receipt_path)}) outside canonical dirs")
    context = weekly.load_derivation(base.root, state_path, base.root / w0["hashes"]["authored"]["rel"])
    pub = base.source_root / "publication/v2"
    archived = pub / "interactive-semantic-publication-input.json"
    assert archived.is_file(), "publisher archived input missing"
    assert sha_file(archived) == sha_file(base.root / w0["hashes"]["authored"]["rel"]), \
        "archived input drifted from --input bytes"
    receipt_context = dict(context)
    receipt_context["authored_path"] = archived
    receipt = weekly.build_receipt(
        base.root, receipt_context, base.root / w0["hashes"]["surface"]["rel"],
        base.root / w0["hashes"]["pretex_review"]["rel"],
        base.root / w0["hashes"]["main_tex"]["rel"],
        base.root / w0["hashes"]["references_bib"]["rel"],
        base.root / w0["hashes"]["style"]["rel"])
    assert receipt["current_tools"]["repository_commit_sha"] == w1["h1"]
    assert receipt["production_state_basis"]["lifecycle_state"] == "VALIDATED_DRAFT"
    assert receipt["production_state_basis"]["historical_sha256"] == core.sha256_file(state_path)
    schema_gate.validate_instance(receipt, base.root / weekly.RECEIPT_SCHEMA, label="Weekly source receipt")
    core.write_json(receipt_path, receipt)
    log.append(f"W2 new receipt built at H1 by real build_receipt (VALIDATED_DRAFT provenance, current closure/contract)")
    validated = weekly.validate_receipt(base.root, receipt_path, state_path)
    assert validated["current_tools"]["repository_commit_sha"] == w1["h1"]
    log.append("W2 new receipt replays (real loader/replay)")
    write_json(logs / "w2-sidecar.json", {
        "phase": "w2", "h1": w1["h1"],
        "receipt_new_sha256": core.sha256_file(receipt_path),
        "receipt_old_sha256": sha_object(json.loads(old_bytes.decode())),
        "tree": tree_snapshot(edition)})
    (logs / "w2.log").write_text("\n".join(log) + "\n")
    print(f"W2 OK receipt renewed at {w1['h1'][:12]}")
    return 0


def phase_w3(args) -> int:
    from scripts import survey_production_v2 as core
    from scripts import survey_agent_control_v2 as agent
    from scripts import survey_reader_surface_gate_v2 as reader_gate
    logs = Path(args.logs)
    log: list[str] = []
    check_no_inherited_git_overrides()
    check_e4c_intact(log)
    edition = Path(args.edition).resolve()
    check_edition(edition)
    w0 = json.loads((logs / "w0-sidecar.json").read_text())
    w1 = json.loads((logs / "w1-sidecar.json").read_text())
    assert run_git(["rev-parse", "HEAD"], edition).stdout.strip() == w1["h1"]
    base, weekly_b = setup_base(edition)
    log_runtime_source(log, "W3")
    state_path = base.root / w0["state_rel"]
    gate_path = base.root / w0["hashes"]["gate"]["rel"]
    evidence_dir = edition / ".witness-evidence"
    evidence_dir.mkdir(exist_ok=True)
    (evidence_dir / "gate-superseded-H0.json").write_bytes(gate_path.read_bytes())
    log.append("W3 preserved old Gate outside canonical input dir")
    manuscript_rel = w0["hashes"]["manuscript"]["rel"]
    review_rel = w0["hashes"]["pretex_review"]["rel"]
    gate_rel = w0["hashes"]["gate"]["rel"]
    proc = run_gate_cli(edition, manuscript_rel, review_rel, state_path, gate_rel)
    (logs / "w3-gate-cli.out.txt").write_text(proc.stdout)
    (logs / "w3-gate-cli.err.txt").write_text(proc.stderr)
    (logs / "w3-gate-cli.exit").write_text(str(proc.returncode))
    assert proc.returncode == 0, proc.stderr[-2000:]
    validated = reader_gate.validate_reader_surface_gate(
        base.root, gate_path, issue_id=w0["issue"], publication_profile="WEEKLY_MAGAZINE",
        expected_manuscript_path=base.root / manuscript_rel, state_path=state_path)
    assert validated["status"] == "PASSED"
    receipt_path = base.root / w0["hashes"]["receipt"]["rel"]
    receipt_sha = core.sha256_file(receipt_path)
    assert validated["derivation"]["receipt"] == {
        "path": w0["hashes"]["receipt"]["rel"], "sha256": receipt_sha}, \
        "Gate derivation does not bind the new receipt"
    log.append("W3 Gate renewed via fixed CLI; derivation binds new receipt (not a timestamp oracle)")
    errors = agent.validate_agent_state(base.root, base.cfg, core.load_json(state_path))
    assert errors, "strict State unexpectedly passes after Gate renewal"
    joined = "; ".join(errors)
    (logs / "w3-strict-drift.err.txt").write_text(joined)
    assert "reader-surface-gate" in joined or "artifact drift" in joined, joined[:600]
    log.append(f"W3 strict State reports changed validation row: {joined[:220]}")
    pending = agent.built_checked_pending_publication_basis(base.root, base.cfg, state_path)
    repl = [(n, p) for (n, p, _o, _nw, _s) in pending.replacements]
    assert repl == [(n, p) for (n, p) in repl if n == "reader-surface-gate"], repl
    assert len(pending.replacements) == 1, [r[:2] for r in pending.replacements]
    log.append(f"W3 fresh pending basis: replacements={[(r[0], r[1]) for r in pending.replacements]} "
               f"preserved={len(pending.preserved)} (basis NOT retained across later writes)")
    write_json(logs / "w3-sidecar.json", {
        "phase": "w3", "h1": w1["h1"],
        "gate_new_sha256": core.sha256_file(gate_path),
        "pending_replacements": [[r[0], r[1], r[2], r[3], r[4]] for r in pending.replacements],
        "pending_preserved": [list(r) for r in pending.preserved],
        "tree": tree_snapshot(edition)})
    (logs / "w3.log").write_text("\n".join(log) + "\n")
    print("W3 OK gate renewed; pending basis gate-only")
    return 0


def phase_w4(args) -> int:
    from scripts import survey_production_v2 as core
    from scripts import survey_agent_control_v2 as agent
    from scripts import survey_weekly_derivation_v2 as weekly
    from scripts import survey_reader_surface_gate_v2 as reader_gate
    logs = Path(args.logs)
    log: list[str] = []
    check_no_inherited_git_overrides()
    check_e4c_intact(log)
    edition = Path(args.edition).resolve()
    check_edition(edition)
    w0 = json.loads((logs / "w0-sidecar.json").read_text())
    w1 = json.loads((logs / "w1-sidecar.json").read_text())
    assert run_git(["rev-parse", "HEAD"], edition).stdout.strip() == w1["h1"]
    base, weekly_b = setup_base(edition)
    log_runtime_source(log, "W4")
    state_path = base.root / w0["state_rel"]
    recorded_at = core.iso_utc(datetime.now(timezone.utc))
    log.append(f"W4 actual clock recorded_at={recorded_at} (live clock; system date not assumed)")
    proc = run_revalidate_cli(edition, state_path, SYNTHETIC_REASON_FIRST,
                              "synthetic-witness-harness", recorded_at)
    (logs / "w4-revalidate-cli.out.txt").write_text(proc.stdout)
    (logs / "w4-revalidate-cli.err.txt").write_text(proc.stderr)
    (logs / "w4-revalidate-cli.exit").write_text(str(proc.returncode))
    assert proc.returncode == 0, proc.stderr[-2000:]
    record_rel = json.loads(proc.stdout)["revalidation_record"]
    record_path = base.root / record_rel
    record = core.load_json(record_path)
    assert record["reason_class"] == "REVIEWED_CORE_CHANGE"
    assert record["supersedes"] is None, "first record must supersede nothing"
    assert [r["name"] for r in record["superseded_artifacts"]] == ["reader-surface-gate"]
    state = core.load_json(state_path)
    assert state["publication_revalidation_provenance"] == {
        "path": record_rel, "sha256": core.sha256_file(record_path)}
    assert agent.validate_agent_state(base.root, base.cfg, state) == []
    active, errors = agent.resolve_active_publication_revalidation(base.root, base.cfg, state)
    assert not errors and active is not None
    log.append(f"W4 r1 established: {record_rel}; pointer set; strict State + active readback OK")
    weekly.validate_receipt(base.root, base.root / w0["hashes"]["receipt"]["rel"], state_path)
    reader_gate.validate_reader_surface_gate(
        base.root, base.root / w0["hashes"]["gate"]["rel"], issue_id=w0["issue"],
        publication_profile="WEEKLY_MAGAZINE",
        expected_manuscript_path=base.root / w0["hashes"]["manuscript"]["rel"],
        state_path=state_path)
    manuscript = core.load_json(base.root / w0["hashes"]["manuscript"]["rel"])
    assert manuscript["issue_id"] == w0["issue"]
    log.append("W4 explicit Gate/receipt readback + expected manuscript OK (State alone does not replay derivation)")
    try:
        proc2 = run_revalidate_cli(edition, state_path, "no-op repeat", "synthetic-witness-harness",
                                   core.iso_utc(datetime.now(timezone.utc)))
        assert proc2.returncode != 0 and "already validates current bytes" in proc2.stderr
        log.append("W4 no-op repeat correctly refused (already validates current bytes)")
    except AssertionError:
        (logs / "w4-noop-repeat.out.txt").write_text(proc2.stdout)
        (logs / "w4-noop-repeat.err.txt").write_text(proc2.stderr)
        raise
    write_json(logs / "w4-sidecar.json", {
        "phase": "w4", "h1": w1["h1"], "recorded_at": recorded_at,
        "r1_rel": record_rel, "r1_sha256": core.sha256_file(record_path),
        "tree": tree_snapshot(edition)})
    (logs / "w4.log").write_text("\n".join(log) + "\n")
    print(f"W4 OK r1={record_rel}")
    return 0


def phase_w5(args) -> int:
    from scripts import survey_production_v2 as core
    from scripts import survey_agent_control_v2 as agent
    from scripts import survey_weekly_derivation_v2 as weekly
    from scripts import survey_reader_surface_gate_v2 as reader_gate
    from scripts import survey_schema_v2 as schema_gate
    logs = Path(args.logs)
    log: list[str] = []
    check_no_inherited_git_overrides()
    check_e4c_intact(log)
    edition = Path(args.edition).resolve()
    check_edition(edition)
    w0 = json.loads((logs / "w0-sidecar.json").read_text())
    w1 = json.loads((logs / "w1-sidecar.json").read_text())
    w4 = json.loads((logs / "w4-sidecar.json").read_text())
    assert run_git(["rev-parse", "HEAD"], edition).stdout.strip() == w1["h1"]
    base, weekly_b = setup_base(edition)
    state_path = base.root / w0["state_rel"]
    r1_path = base.root / w4["r1_rel"]
    r1_bytes = r1_path.read_bytes()
    h2, diff = commit_control_comment(edition, "H2", log)
    (logs / "w5-comment.patch").write_text(diff)
    fresh_import_check(edition, log)
    base2, _ = setup_base(edition)
    assert base2.head == h2
    harness_preconditions(base2, w0, log, "W5")
    assert agent.validate_agent_state(base2.root, base2.cfg, core.load_json(state_path)) == []
    log.append("W5 strict State passes at H2 with intact r1 predecessor (live checks tolerate HEAD move)")
    context = weekly.load_derivation(base2.root, state_path, base2.root / w0["hashes"]["authored"]["rel"])
    assert context["surface"] == core.load_json(base2.root / w0["hashes"]["surface"]["rel"])
    log.append("W5 load_derivation passes at H2; surface identical")
    receipt_path = base2.root / w0["hashes"]["receipt"]["rel"]
    try:
        weekly.validate_receipt(base2.root, receipt_path, state_path)
        raise AssertionError("H1 receipt unexpectedly replayed at H2")
    except ValueError as exc:
        (logs / "w5-old-receipt.err.txt").write_text(str(exc))
        log.append(f"W5 H1-era receipt rejects at H2: {str(exc)[:200]}")
    (edition / ".witness-evidence" / "receipt-superseded-H1.json").write_bytes(receipt_path.read_bytes())
    archived = base2.source_root / "publication/v2/interactive-semantic-publication-input.json"
    receipt_context = dict(context)
    receipt_context["authored_path"] = archived
    receipt = weekly.build_receipt(
        base2.root, receipt_context, base2.root / w0["hashes"]["surface"]["rel"],
        base2.root / w0["hashes"]["pretex_review"]["rel"],
        base2.root / w0["hashes"]["main_tex"]["rel"],
        base2.root / w0["hashes"]["references_bib"]["rel"],
        base2.root / w0["hashes"]["style"]["rel"])
    assert receipt["current_tools"]["repository_commit_sha"] == h2
    schema_gate.validate_instance(receipt, base2.root / weekly.RECEIPT_SCHEMA, label="Weekly source receipt")
    core.write_json(receipt_path, receipt)
    weekly.validate_receipt(base2.root, receipt_path, state_path)
    log.append("W5 new receipt at H2 replays")
    gate_path = base2.root / w0["hashes"]["gate"]["rel"]
    (edition / ".witness-evidence" / "gate-superseded-H1.json").write_bytes(gate_path.read_bytes())
    proc = run_gate_cli(edition, w0["hashes"]["manuscript"]["rel"], w0["hashes"]["pretex_review"]["rel"],
                        state_path, w0["hashes"]["gate"]["rel"])
    (logs / "w5-gate-cli.out.txt").write_text(proc.stdout)
    (logs / "w5-gate-cli.err.txt").write_text(proc.stderr)
    (logs / "w5-gate-cli.exit").write_text(str(proc.returncode))
    assert proc.returncode == 0, proc.stderr[-2000:]
    reader_gate.validate_reader_surface_gate(
        base2.root, gate_path, issue_id=w0["issue"], publication_profile="WEEKLY_MAGAZINE",
        expected_manuscript_path=base2.root / w0["hashes"]["manuscript"]["rel"], state_path=state_path)
    pending = agent.built_checked_pending_publication_basis(base2.root, base2.cfg, state_path)
    assert len(pending.replacements) == 1 and pending.replacements[0][0] == "reader-surface-gate"
    recorded_at = core.iso_utc(datetime.now(timezone.utc))
    proc2 = run_revalidate_cli(edition, state_path, SYNTHETIC_REASON_SECOND,
                               "synthetic-witness-harness", recorded_at)
    (logs / "w5-revalidate-cli.out.txt").write_text(proc2.stdout)
    (logs / "w5-revalidate-cli.err.txt").write_text(proc2.stderr)
    (logs / "w5-revalidate-cli.exit").write_text(str(proc2.returncode))
    assert proc2.returncode == 0, proc2.stderr[-2000:]
    r2_rel = json.loads(proc2.stdout)["revalidation_record"]
    r2_path = base2.root / r2_rel
    r2 = core.load_json(r2_path)
    assert r2["supersedes"] == {"path": w4["r1_rel"], "sha256": core.sha256_file(r1_path)}
    assert r1_path.read_bytes() == r1_bytes, "r1 mutated by r2 establishment"
    assert agent.validate_agent_state(base2.root, base2.cfg, core.load_json(state_path)) == []
    weekly.validate_receipt(base2.root, receipt_path, state_path)
    reader_gate.validate_reader_surface_gate(
        base2.root, gate_path, issue_id=w0["issue"], publication_profile="WEEKLY_MAGAZINE",
        expected_manuscript_path=base2.root / w0["hashes"]["manuscript"]["rel"], state_path=state_path)
    log.append(f"W5 r2={r2_rel} supersedes intact r1; chain bound; current Gate/receipt replay OK")
    write_json(logs / "w5-sidecar.json", {
        "phase": "w5", "h2": h2, "h2_parent": w1["h1"], "recorded_at": recorded_at,
        "r2_rel": r2_rel, "r2_sha256": core.sha256_file(r2_path),
        "r1_unchanged": True, "tree": tree_snapshot(edition)})
    (logs / "w5.log").write_text("\n".join(log) + "\n")
    print(f"W5 OK h2={h2[:12]} r2={r2_rel}")
    return 0


def phase_w6(args) -> int:
    from scripts import survey_production_v2 as core
    from scripts import survey_agent_control_v2 as agent
    from scripts import survey_weekly_derivation_v2 as weekly
    from scripts import survey_reader_surface_gate_v2 as reader_gate
    logs = Path(args.logs)
    log: list[str] = []
    check_no_inherited_git_overrides()
    check_e4c_intact(log)
    edition = Path(args.edition).resolve()
    check_edition(edition)
    w0 = json.loads((logs / "w0-sidecar.json").read_text())
    base, weekly_b = setup_base(edition)
    log_runtime_source(log, "W6")
    state_path = base.root / w0["state_rel"]
    head_now = run_git(["rev-parse", "HEAD"], edition).stdout.strip()

    def restore(path: Path, data: bytes, label: str) -> None:
        path.write_bytes(data)
        log.append(f"W6 restored {label}")

    # N1: nonmechanical reader/output mutation. Single outer try/finally owns the
    # restore so EVERY failure path (runtime or oracle assert) restores exact bytes.
    surface_path = base.root / w0["hashes"]["surface"]["rel"]
    surface_before = surface_path.read_bytes()
    mutated = core.load_json(surface_path)
    mutated["cover"]["headline"] = "Unreviewed replacement headline"
    core.write_json(surface_path, mutated)
    try:
        try:
            weekly.validate_receipt(base.root, base.root / w0["hashes"]["receipt"]["rel"], state_path)
            raise AssertionError("N1 mutated surface unexpectedly replayed")
        except ValueError as exc:
            (logs / "w6-n1-surface-mutation.err.txt").write_text(str(exc))
            # Surface-only mutation trips the earlier recorded-bytes guard ("reviewed reader
            # input drift"); the deeper "independently recomputed" oracle fires only when the
            # receipt's recorded sha is also re-pointed at mutated bytes (B's pattern). Either
            # is a fail-closed runtime rejection; accept both, record the actual one.
            assert ("independently recomputed reader input differs" in str(exc)
                    or "Weekly reviewed reader input drift" in str(exc)), str(exc)[:400]
            log.append(f"W6-N1 runtime rejects mutated reader input ({str(exc)[:120]})")
        try:
            harness_preconditions(base, w0, log, "W6-N1")
            raise AssertionError("N1 harness precondition unexpectedly passed on mutated surface")
        except AssertionError as exc:
            assert "scope drift: surface" in str(exc), str(exc)[:300]
            log.append("W6-N1 harness precondition refuses BEFORE any refresh write (policy, not shipping guard)")
    finally:
        restore(surface_path, surface_before, "surface")
    weekly.validate_receipt(base.root, base.root / w0["hashes"]["receipt"]["rel"], state_path)
    log.append("W6-N1 restored; replay passes again")

    # N2: upstream accepted-byte mutation.
    arch_path = base.root / w0["hashes"]["architecture"]["rel"]
    arch_before = arch_path.read_bytes()
    arch_path.write_bytes(arch_before + b" ")
    try:
        agent.built_checked_pending_publication_basis(base.root, base.cfg, state_path)
        raise AssertionError("N2 upstream mutation unexpectedly admitted")
    except agent.AgentControlError as exc:
        (logs / "w6-n2-upstream-mutation.err.txt").write_text(str(exc))
        log.append(f"W6-N2 upstream mutation refused: {str(exc)[:220]}")
    finally:
        restore(arch_path, arch_before, "architecture")
    assert agent.validate_agent_state(base.root, base.cfg, core.load_json(state_path)) == []
    log.append("W6-N2 restored; strict State passes again")

    # N3: review-criteria change (persisted review no longer PASS-worthy).
    review_path = base.root / w0["hashes"]["pretex_review"]["rel"]
    review_before = review_path.read_bytes()
    bad = core.load_json(review_path)
    bad["decision"] = "FAIL"
    bad["status"] = "FAILED"
    bad["review_sha256"] = core.sha256_object({k: v for k, v in bad.items() if k != "review_sha256"})
    core.write_json(review_path, bad)
    try:
        reader_gate.load_and_validate_reader_surface_semantic_review(
            base.root, w0["hashes"]["pretex_review"]["rel"],
            expected_issue_id=w0["issue"], expected_publication_profile="WEEKLY_MAGAZINE",
            expected_surface_path=base.root / w0["hashes"]["surface"]["rel"],
            expected_surface_sha256=w0["surface_sha256"], require_pass=True)
        raise AssertionError("N3 FAIL review unexpectedly validated")
    except ValueError as exc:
        (logs / "w6-n3-criteria.err.txt").write_text(str(exc))
        log.append(f"W6-N3 criteria/review change refused: {str(exc)[:220]}")
    finally:
        restore(review_path, review_before, "pretex review")
    reader_gate.load_and_validate_reader_surface_semantic_review(
        base.root, w0["hashes"]["pretex_review"]["rel"],
        expected_issue_id=w0["issue"], expected_publication_profile="WEEKLY_MAGAZINE",
        require_pass=True)
    log.append("W6-N3 restored; review validates again")

    # N4: malformed predecessor pointer.
    state_before = state_path.read_bytes()
    corrupted = core.load_json(state_path)
    ptr = corrupted.get("publication_revalidation_provenance")
    assert isinstance(ptr, dict), "N4 needs an established pointer; run after W4/W5"
    ptr_path = base.root / ptr["path"]
    ptr_bytes = ptr_path.read_bytes()
    corrupted["publication_revalidation_provenance"]["sha256"] = "0" * 64
    core.write_json(state_path, corrupted)
    try:
        agent.built_checked_pending_publication_basis(base.root, base.cfg, state_path)
        raise AssertionError("N4 malformed predecessor unexpectedly admitted")
    except agent.AgentControlError as exc:
        (logs / "w6-n4-predecessor.err.txt").write_text(str(exc))
        assert "predecessor invalid" in str(exc), str(exc)[:400]
        log.append(f"W6-N4 malformed predecessor refused: {str(exc)[:220]}")
    finally:
        restore(state_path, state_before, "State")
    assert agent.validate_agent_state(base.root, base.cfg, core.load_json(state_path)) == []
    assert (base.root / ptr["path"]).read_bytes() == ptr_bytes
    log.append("W6-N4 restored; pointer intact, strict State passes")
    assert run_git(["rev-parse", "HEAD"], edition).stdout.strip() == head_now
    log.append(f"W6 HEAD unchanged {head_now[:12]}; no new State/record authority created by negatives")
    write_json(logs / "w6-sidecar.json", {"phase": "w6", "head": head_now,
                                          "negatives": ["n1-surface", "n2-upstream", "n3-criteria", "n4-predecessor"],
                                          "tree": tree_snapshot(edition)})
    (logs / "w6.log").write_text("\n".join(log) + "\n")
    print("W6 OK 4 negatives refused, all restored")
    return 0


def phase_w6fix(args) -> int:
    """One-off fixture-only repair of W6-attempt-2 residue (documented, no runtime change).

    Cause: N1's first try/except had no finally in attempts 1-2, so the "Unreviewed
    replacement headline" mutation was never restored. Fixed structurally above; this phase
    rewrites the single known leaf value via the same core.write_json byte path and proves
    byte-identity against the W0-recorded surface sha. Refuses anything else.
    """
    from scripts import survey_production_v2 as core
    logs = Path(args.logs)
    log: list[str] = []
    check_no_inherited_git_overrides()
    check_e4c_intact(log)
    edition = Path(args.edition).resolve()
    check_edition(edition)
    w0 = json.loads((logs / "w0-sidecar.json").read_text())
    base, _ = setup_base(edition)
    log_runtime_source(log, "W6fix")
    surface_path = base.root / w0["hashes"]["surface"]["rel"]
    authored = core.load_json(base.root / w0["hashes"]["authored"]["rel"])
    doc = core.load_json(surface_path)
    assert doc["cover"]["headline"] == "Unreviewed replacement headline", \
        "residue marker absent; refusing to touch surface"
    doc["cover"]["headline"] = authored["cover"]["headline"]
    core.write_json(surface_path, doc)
    actual = sha_file(surface_path)
    assert actual == w0["surface_sha256"], f"repair did not restore exact bytes: {actual}"
    log.append(f"W6fix restored exact W0 surface bytes (sha {actual}) from residue marker")
    (logs / "w6fix.log").write_text("\n".join(log) + "\n")
    print("W6fix OK surface byte-identical to W0")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["w0a", "w0b", "w1", "w2", "w3", "w4", "w5", "w6", "w6fix"])
    parser.add_argument("--edition", required=True)
    parser.add_argument("--logs", required=True)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--exit-file", default=None)
    args = parser.parse_args()
    # Edition first so post-copy phases import edition code; e4c fallback covers only
    # the pre-copy w0a path (stdlib-only, never imports scripts) and is otherwise shadowed.
    sys.path.insert(0, str(E4C_REPO))
    sys.path.insert(0, str(Path(args.edition).resolve()))
    table = {"w0a": phase_w0a, "w0b": phase_w0b, "w1": phase_w1, "w2": phase_w2,
             "w3": phase_w3, "w4": phase_w4, "w5": phase_w5, "w6": phase_w6,
             "w6fix": phase_w6fix}
    try:
        code = table[args.phase](args)
    except Exception:
        code = 3
        raise
    finally:
        if args.exit_file:
            Path(args.exit_file).write_text(str(code if "code" in dir() else 3))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
