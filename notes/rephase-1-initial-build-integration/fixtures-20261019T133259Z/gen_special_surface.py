#!/usr/bin/env python3
"""Special fixture: accepted THEMATIC chain through DRAFT_COMPLETE + surface-only CLI.

Uses actual LongformDerivationV2Tests helpers _chain/_complete_authorities/_current_state
with the narrow integration-test data adapter (clean Discovery URLs for lexical gate),
without calling historical setUp runners or unrequested source commits.
Custom object init root/cfg/head/source_root/survey_root. Imports ONLY fixture source.
Synthetic content stays synthetic. No TeX/pass2. Stops at surface ready.
"""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

TS = "20261019T133259Z"
FIXTURE = Path("/tmp/opencode/jgas-initial-fixtures-20261019T133259Z/special-fixture")
EVIDENCE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-initial-build-integration/fixtures-20261019T133259Z")
ISSUE = "SP001"
DID1 = "fixture-paper-D001"
URL1 = "https://example.invalid/papers/lineage-note-one"
URL_BY_DID = {DID1: URL1}

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def git(args, cwd):
    env = dict(os.environ)
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
              "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR"):
        env.pop(k, None)
    env["GIT_NO_LAZY_FETCH"] = "1"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    return subprocess.run(["git", "--no-optional-locks", *args], cwd=str(cwd),
                          capture_output=True, env=env, text=True)

def snapshot(root: Path) -> dict:
    files = {}
    for p in sorted(root.rglob("*")):
        if ".git" in p.parts:
            continue
        if "__pycache__" in p.parts:
            continue
        if p.is_file() and not p.is_symlink():
            files[str(p.relative_to(root))] = sha256_file(p)
    return files

def main() -> int:
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
              "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR"):
        if os.environ.get(k):
            print(f"FATAL inherited {k}", file=sys.stderr)
            return 2
    for mod in list(sys.modules):
        if mod == "scripts" or mod.startswith("scripts.") or mod.startswith("tests."):
            del sys.modules[mod]
    sys.path.insert(0, str(FIXTURE))
    os.chdir(str(FIXTURE))
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    before_files = snapshot(FIXTURE)
    before_head = git(["rev-parse", "HEAD"], FIXTURE).stdout.strip()
    before_status = git(["status", "--porcelain=v1", "--untracked-files=all"], FIXTURE).stdout
    (EVIDENCE / "special-before-head.txt").write_text(before_head + "\n")
    (EVIDENCE / "special-before-status.txt").write_text(before_status)
    if before_status.strip() != "":
        print(f"fixture not clean: {before_status[:500]}", file=sys.stderr)
        return 3
    from scripts import survey_production_v2 as core
    assert Path(core.__file__).resolve().as_posix().startswith(FIXTURE.resolve().as_posix()), \
        f"core outside fixture: {core.__file__}"
    from tests import test_survey_longform_derivation_v2 as lf1_tests
    # narrow fixture object, no setUp runner
    worker = lf1_tests.LongformDerivationV2Tests(methodName="test_valid_single_did_projects_every_category")
    worker.root = FIXTURE.resolve()
    worker.cfg = core.load_json(worker.root / core.DEFAULT_CONFIG)
    worker.head = core.repository_commit_sha(worker.root)
    worker.workspace = FIXTURE.resolve()  # independent copy, not original source workspace
    (EVIDENCE / "special-fixture-source-head.txt").write_text(worker.head + "\n")
    if worker.head == "409b292756dd1277b9dfae87679934c0d2ce251c":
        print("fixture head equals 409; mislabelled", file=sys.stderr)
        return 4
    # replicate integration narrow adapter (setUp 169-201): clean Discovery URLs + authored primary_url
    def _bound_authored(chain: dict, review_reference: str = "fixture longform review") -> dict:
        rows = []
        for pid in chain["draft_paths"]:
            row = worker._revision_row(pid, worker._did_for_package(chain, pid))
            for note in row["technical_notes"]:
                note["primary_url"] = URL1
            rows.append(row)
        dids = [did for pid in chain["draft_paths"] for did in worker._did_for_package(chain, pid)]
        return {
            "schema_version": "2.0-rc1", "issue_id": ISSUE, "runner": "LONGFORM_SPECIAL",
            "cover": {"headline": "Fixture lineage cover", "deck": "Source-based lineage survey",
                      "anchors": ["Target Model"]},
            "frontmatter": {"heading": "Fixture frontmatter", "lede": "A bounded lineage survey.",
                            "scope_notes": ["One accepted primary source per package."]},
            "final_summary": {"heading": "この号の総括", "paragraphs": [
                "The edition surveys accepted lineage sources.",
                "The claims remain attributed to their origins.",
                "The synthesis stays inside authorized evidence."]},
            "longform_revision": {
                "review_reference": review_reference, "new_external_evidence": False,
                "packages": rows,
                "cross_family_synthesis": {
                    "heading": "Fixture cross-family synthesis",
                    "paragraphs": [
                        {"text": "Fixture cross paragraph one.", "discovery_ids": list(dids)},
                        {"text": "Fixture cross paragraph two.", "discovery_ids": list(dids)}],
                    "comparison_rows": [
                        {"dimension": f"Fixture aspect {number}", "glm": "Fixture GLM.",
                         "qwen": "Fixture Qwen.", "deepseek": "Fixture DeepSeek.",
                         "kimi": "Fixture Kimi.", "discovery_ids": list(dids)}
                        for number in (1, 2, 3)]}}}

    worker._authored = _bound_authored
    base_helper_factory = worker._evidence_helper
    def _clean_evidence_helper():
        helper = base_helper_factory()
        helper.repo_root = FIXTURE.resolve()
        original_discovery = helper.discovery
        def _clean_discovery(issue_id: str, discovery_id: str, origin: str = "BASE") -> dict:
            record = original_discovery(issue_id, discovery_id, origin)
            record["source"] = helper.source(URL_BY_DID[discovery_id])
            return record
        helper.discovery = _clean_discovery
        return helper
    worker._evidence_helper = _clean_evidence_helper
    # accepted chain via actual producers
    try:
        chain = worker._chain(dids=(DID1,))
    except Exception as e:
        (EVIDENCE / "special-chain-failure.txt").write_text(f"{type(e).__name__}: {e}\n")
        import traceback; (EVIDENCE / "special-chain-traceback.txt").write_text(traceback.format_exc())
        print(f"special _chain failed: {e}", file=sys.stderr)
        return 5
    try:
        chain = worker._complete_authorities(chain)
    except Exception as e:
        (EVIDENCE / "special-complete-failure.txt").write_text(f"{type(e).__name__}: {e}\n")
        import traceback; (EVIDENCE / "special-complete-traceback.txt").write_text(traceback.format_exc())
        print(f"special _complete failed: {e}", file=sys.stderr)
        return 6
    try:
        state_path = worker._current_state(chain)
    except Exception as e:
        (EVIDENCE / "special-state-failure.txt").write_text(f"{type(e).__name__}: {e}\n")
        import traceback; (EVIDENCE / "special-state-traceback.txt").write_text(traceback.format_exc())
        print(f"special _current_state failed: {e}", file=sys.stderr)
        return 7
    state = core.load_json(state_path)
    (EVIDENCE / "special-state.json").write_text(json.dumps(
        {"path": str(state_path.relative_to(worker.root)), "sha256": sha256_file(state_path),
         "bytes": state_path.stat().st_size, "lifecycle_state": state.get("lifecycle_state"),
         "next_action": state.get("next_action")}, indent=2))
    if state.get("lifecycle_state") != "DRAFT_COMPLETE":
        print(f"unexpected lifecycle {state.get('lifecycle_state')}", file=sys.stderr)
        return 8
    authored_path = chain["authored_path"]
    (EVIDENCE / "special-authored.json").write_text(json.dumps(
        {"path": str(authored_path.relative_to(worker.root)), "sha256": sha256_file(authored_path),
         "bytes": authored_path.stat().st_size}, indent=2))
    after_files = snapshot(FIXTURE)
    after_head = git(["rev-parse", "HEAD"], FIXTURE).stdout.strip()
    after_status = git(["status", "--porcelain=v1", "--untracked-files=all"], FIXTURE).stdout
    (EVIDENCE / "special-after-authority-status.txt").write_text(after_status)
    if after_head != before_head:
        print("HEAD moved during authority", file=sys.stderr)
        return 9
    new_or_changed = [k for k in after_files if k not in before_files or after_files[k] != before_files.get(k)]
    removed = [k for k in before_files if k not in after_files]
    allowed_roots = ("architecture-v2.json", "architecture-review-summary-v2.json",
                     "architecture-review-attention-v2.json", "architecture-approval-v2.json",
                     "selection-v2.json", "candidate-matrix-v2.json")
    allowed_prefixes = (f"sources/{ISSUE}/", "raw/", "views-input/", "views-accepted/")
    def _allowed(path: str) -> bool:
        if path in allowed_roots:
            return True
        if path.startswith(allowed_prefixes):
            return True
        if path.startswith("draft-package-") or path.startswith("draft-result-"):
            return True
        return False
    (EVIDENCE / "special-authority-delta.json").write_text(json.dumps(
        {"new_or_changed": sorted(new_or_changed), "removed": sorted(removed)}, indent=2))
    bad = [k for k in new_or_changed if not _allowed(k)]
    control_bad = [k for k in new_or_changed if k.startswith(("scripts/", "schemas/", "config/", "templates/", "tests/", "prompts/", "docs/", "data/", ".latexmkrc"))]
    if bad or control_bad or removed:
        print(f"unexpected delta: bad={bad[:10]} control={control_bad[:10]} removed={removed[:10]}", file=sys.stderr)
        return 10
    if not new_or_changed:
        print("no authority output", file=sys.stderr)
        return 11
    # actual CLI subprocess surface-only
    cli = [sys.executable, "scripts/survey_longform_semantic_publication_v2.py",
           "--repo-root", str(worker.root), "--state", str(state_path),
           "--input", str(authored_path), "--materialize-surface-only"]
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(worker.root)
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(k, None)
    proc = subprocess.run(cli, cwd=str(worker.root), capture_output=True, text=True, env=env)
    (EVIDENCE / "special-surface-stdout.txt").write_bytes(proc.stdout.encode())
    (EVIDENCE / "special-surface-stderr.txt").write_bytes(proc.stderr.encode())
    (EVIDENCE / "special-surface-exit.txt").write_text(str(proc.returncode))
    (EVIDENCE / "special-surface-command.txt").write_text(" ".join(cli) + "\n")
    if proc.returncode != 0:
        print(f"special CLI failed {proc.returncode} {proc.stderr[:2000]}", file=sys.stderr)
        return 12
    publication_root = worker.root / "sources" / ISSUE / "publication" / "v2"
    surface_path = publication_root / "reader-surface-input-v2.json"
    if not surface_path.is_file():
        print("surface missing", file=sys.stderr)
        return 13
    surface = core.load_json(surface_path)
    (EVIDENCE / "special-surface-pin.json").write_text(json.dumps(
        {"path": str(surface_path.relative_to(worker.root)), "sha256": sha256_file(surface_path),
         "bytes": surface_path.stat().st_size, "issue_id": surface.get("issue_id")}, indent=2))
    survey_root = worker.root / "surveys" / "special" / ISSUE
    for absent in ("main.tex", "references.bib", "jgaisurvey.sty"):
        if (survey_root / absent).exists():
            print(f"unexpected TeX output {absent}", file=sys.stderr)
            return 14
    if (publication_root / "validated-source-manifest.json").exists():
        print("unexpected receipt after surface-only", file=sys.stderr)
        return 15
    final_head = git(["rev-parse", "HEAD"], FIXTURE).stdout.strip()
    final_status = git(["status", "--porcelain=v1", "--untracked-files=all"], FIXTURE).stdout
    (EVIDENCE / "special-final-head.txt").write_text(final_head + "\n")
    (EVIDENCE / "special-final-status.txt").write_text(final_status)
    if final_head != before_head:
        print("HEAD moved after CLI", file=sys.stderr)
        return 16
    print("special surface OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
