#!/usr/bin/env python3
"""Weekly fixture: accepted chain through DRAFT_COMPLETE + surface-only CLI.

Uses actual IncrementBWeeklyDerivationV2Tests helpers _chain/_complete_authorities/_current_state
without calling setUp (custom object init root/cfg/head/source_root/survey_root).
Imports ONLY fixture source. No validator/Git stubs. Synthetic content stays synthetic.
Invokes actual CLI in subprocess with --materialize-surface-only.
Stops at surface ready for author-independent pre-TeX inspection. No semantic PASS/Human approval.
"""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

TS = "20261019T133259Z"
FIXTURE = Path("/tmp/opencode/jgas-initial-fixtures-20261019T133259Z/weekly-fixture")
EVIDENCE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-initial-build-integration/fixtures-20261019T133259Z")
ISSUE = "2026-W37"

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
    # enforce fixture-only imports
    for mod in list(sys.modules):
        if mod == "scripts" or mod.startswith("scripts.") or mod.startswith("tests."):
            del sys.modules[mod]
    sys.path.insert(0, str(FIXTURE))
    os.chdir(str(FIXTURE))
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    # before guards
    before_files = snapshot(FIXTURE)
    before_head = git(["rev-parse", "HEAD"], FIXTURE).stdout.strip()
    before_status = git(["status", "--porcelain=v1", "--untracked-files=all"], FIXTURE).stdout
    before_diff = git(["diff", "--name-only", "HEAD"], FIXTURE).stdout
    (EVIDENCE / "weekly-before-head.txt").write_text(before_head + "\n")
    (EVIDENCE / "weekly-before-status.txt").write_text(before_status)
    (EVIDENCE / "weekly-before-diff.txt").write_text(before_diff)
    if before_status.strip() != "":
        print(f"fixture not clean before authority: {before_status[:500]}", file=sys.stderr)
        return 3
    from scripts import survey_production_v2 as core
    assert Path(core.__file__).resolve().as_posix().startswith(FIXTURE.resolve().as_posix()), \
        f"core imported outside fixture: {core.__file__}"
    from tests.test_survey_increment_b_weekly_derivation_v2 import IncrementBWeeklyDerivationV2Tests
    obj = IncrementBWeeklyDerivationV2Tests(methodName="test_accepted_weekly_chain_probe")
    obj.root = FIXTURE.resolve()
    obj.cfg = core.load_json(obj.root / core.DEFAULT_CONFIG)
    obj.head = core.repository_commit_sha(obj.root)
    obj.source_root = obj.root / "sources" / ISSUE
    obj.survey_root = obj.root / "surveys" / "weekly" / ISSUE
    # source-commit head must be synthetic snapshot (not 409); record it
    (EVIDENCE / "weekly-fixture-source-head.txt").write_text(obj.head + "\n")
    if obj.head == "409b292756dd1277b9dfae87679934c0d2ce251c":
        print("fixture head unexpectedly equals 409; ancestry mislabelled", file=sys.stderr)
        return 4
    try:
        chain = obj._chain()
    except Exception as e:
        (EVIDENCE / "weekly-chain-failure.txt").write_text(f"{type(e).__name__}: {e}\n")
        print(f"weekly _chain failed: {e}", file=sys.stderr)
        return 5
    try:
        obj._complete_authorities(chain)
    except Exception as e:
        (EVIDENCE / "weekly-complete-failure.txt").write_text(f"{type(e).__name__}: {e}\n")
        print(f"weekly _complete failed: {e}", file=sys.stderr)
        return 6
    try:
        state_path = obj._current_state(chain)
    except Exception as e:
        (EVIDENCE / "weekly-state-failure.txt").write_text(f"{type(e).__name__}: {e}\n")
        print(f"weekly _current_state failed: {e}", file=sys.stderr)
        return 7
    state = core.load_json(state_path)
    (EVIDENCE / "weekly-state.json").write_text(json.dumps(
        {"path": str(state_path.relative_to(obj.root)), "sha256": sha256_file(state_path),
         "bytes": state_path.stat().st_size, "lifecycle_state": state.get("lifecycle_state"),
         "next_action": state.get("next_action")}, indent=2))
    if state.get("lifecycle_state") != "DRAFT_COMPLETE":
        print(f"unexpected lifecycle: {state.get('lifecycle_state')}", file=sys.stderr)
        return 8
    authored_path = chain["authored_path"]
    (EVIDENCE / "weekly-authored.json").write_text(json.dumps(
        {"path": str(authored_path.relative_to(obj.root)), "sha256": sha256_file(authored_path),
         "bytes": authored_path.stat().st_size}, indent=2))
    # after-authority guards (before CLI): only sources/ new paths, no control drift
    after_files = snapshot(FIXTURE)
    after_head = git(["rev-parse", "HEAD"], FIXTURE).stdout.strip()
    after_diff_names = git(["diff", "--name-only", "HEAD"], FIXTURE).stdout
    after_status = git(["status", "--porcelain=v1", "--untracked-files=all"], FIXTURE).stdout
    (EVIDENCE / "weekly-after-authority-status.txt").write_text(after_status)
    (EVIDENCE / "weekly-after-authority-diff-names.txt").write_text(after_diff_names)
    if after_head != before_head:
        print("HEAD moved during authority generation (unrequested commit)", file=sys.stderr)
        return 9
    # meaningful delta: every new/modified file must be under sources/2026-W37/ (fixture research output)
    new_or_changed = [k for k in after_files if k not in before_files or after_files[k] != before_files.get(k)]
    removed = [k for k in before_files if k not in after_files]
    (EVIDENCE / "weekly-authority-delta.json").write_text(json.dumps(
        {"new_or_changed": sorted(new_or_changed), "removed": sorted(removed)}, indent=2))
    bad = [k for k in new_or_changed if not k.startswith(f"sources/{ISSUE}/")]
    bad += [k for k in removed if not k.startswith(f"sources/{ISSUE}/")]
    # control files must be byte-identical
    control_bad = [k for k in new_or_changed if k.startswith(("scripts/", "schemas/", "config/", "templates/"))]
    if bad or control_bad or removed:
        print(f"unexpected delta outside sources/{ISSUE}: bad={bad[:10]} control={control_bad[:10]} removed={removed[:10]}", file=sys.stderr)
        return 10
    if not new_or_changed:
        print("no authority output produced", file=sys.stderr)
        return 11
    # invoke actual CLI in subprocess --materialize-surface-only
    cli = [sys.executable, "scripts/survey_weekly_semantic_publication_v2.py",
           "--repo-root", str(obj.root), "--state", str(state_path),
           "--input", str(authored_path), "--materialize-surface-only"]
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(obj.root)
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(k, None)
    proc = subprocess.run(cli, cwd=str(obj.root), capture_output=True, text=True, env=env)
    (EVIDENCE / "weekly-surface-stdout.txt").write_bytes(proc.stdout.encode())
    (EVIDENCE / "weekly-surface-stderr.txt").write_bytes(proc.stderr.encode())
    (EVIDENCE / "weekly-surface-exit.txt").write_text(str(proc.returncode))
    (EVIDENCE / "weekly-surface-command.txt").write_text(" ".join(cli) + "\n")
    if proc.returncode != 0:
        print(f"weekly CLI failed exit={proc.returncode} stderr={proc.stderr[:2000]}", file=sys.stderr)
        return 12
    surface_path = obj.source_root / "publication/v2/reader-surface-input-v2.json"
    if not surface_path.is_file():
        print("surface file missing after CLI", file=sys.stderr)
        return 13
    surface = core.load_json(surface_path)
    (EVIDENCE / "weekly-surface-pin.json").write_text(json.dumps(
        {"path": str(surface_path.relative_to(obj.root)), "sha256": sha256_file(surface_path),
         "bytes": surface_path.stat().st_size, "issue_id": surface.get("issue_id"),
         "cli_status": json.loads(proc.stdout).get("status") if proc.stdout.strip() else None}, indent=2))
    # negative guards: no TeX outputs yet
    for absent in ("main.tex", "references.bib", "jgaisurvey.sty"):
        if (obj.survey_root / absent).exists():
            print(f"unexpected TeX output present: {absent}", file=sys.stderr)
            return 14
    if (obj.source_root / "publication/v2/validated-source-manifest.json").exists():
        print("unexpected receipt present after surface-only", file=sys.stderr)
        return 15
    # final status must show only expected untracked sources + surface, HEAD unchanged
    final_head = git(["rev-parse", "HEAD"], FIXTURE).stdout.strip()
    final_status = git(["status", "--porcelain=v1", "--untracked-files=all"], FIXTURE).stdout
    (EVIDENCE / "weekly-final-head.txt").write_text(final_head + "\n")
    (EVIDENCE / "weekly-final-status.txt").write_text(final_status)
    if final_head != before_head:
        print("HEAD moved after CLI", file=sys.stderr)
        return 16
    print("weekly surface OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
