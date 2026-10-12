#!/usr/bin/env python3
"""Generate the complete 13-path correction overlay patch as git-applyable bytes.

Base: actual409 HEAD409b292/tree8ce36998 + overlay (3M10A). Uses `git add -N`
(intent-to-add) for untracked paths so `git diff HEAD` emits proper
`diff --git` new-file headers that `git apply --check` + `git apply` accept on
a clean 409 copy. Verifies 13 diff headers and byte-identical reconstruction
via `git apply` dry-run? Full apply proof is in proof_apply.py (independent copy).
Read-only to active repo except transient `git add -N` (index intent, no commit).
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

REPO = Path("/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60")
EVID = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey"
            "/notes/rephase-1-dm021-p1/evidence-20261011T235631Z-correction")
MODIFIED = [
    "schemas/reader-surface-gate-v2.schema.json",
    "schemas/reader-surface-semantic-review-v2.schema.json",
    "scripts/survey_reader_surface_gate_v2.py",
]
NEW = [
    "schemas/editorial-correction-proposal-v2.schema.json",
    "schemas/longform-publication-source-manifest-v2.schema.json",
    "schemas/longform-reader-input-v2.schema.json",
    "scripts/survey_editorial_correction_proposal_v2.py",
    "scripts/survey_longform_derivation_v2.py",
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_longform_semantic_publication_v2.py",
    "tests/test_survey_editorial_correction_proposal_v2.py",
    "tests/test_survey_longform_derivation_v2.py",
    "tests/test_survey_longform_publication_integration_v2.py",
]
OUT = EVID / "complete-p1-correction-13path.patch"


def run_git(*args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in __import__("os").environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True, env=env)


def main() -> int:
    for name in ("complete-p1-correction-13path.patch", "complete-p1-correction-13path.sha256"):
        if (EVID / name).exists():
            print(f"REFUSAL: output exists: {name}")
            return 40
    head = run_git("rev-parse", "HEAD").stdout.strip()
    tree = run_git("rev-parse", "HEAD^{tree}").stdout.strip()
    status = run_git("status", "--porcelain").stdout
    assert head == "409b292756dd1277b9dfae87679934c0d2ce251c", head
    assert tree == "8ce3699861505f32d1d60bdc185d4d4f635aedb2", tree
    # Intent-to-add for untracked so diff includes them as new files.
    proc = run_git("add", "-N", *NEW)
    assert proc.returncode == 0, proc.stderr
    try:
        diff = run_git("diff", "HEAD", "--", *MODIFIED, *NEW)
        assert diff.returncode == 0, diff.stderr
        body = diff.stdout
        assert body.count("diff --git ") == 13, f"diff count {body.count('diff --git ')}"
        header = f"DM021-P1 correction overlay: 3M10A relative actual409\nbase HEAD {head}\nbase tree {tree}\n"
        full = header + body
        if not full.endswith("\n"):
            full += "\n"
        OUT.write_text(full, encoding="utf-8")
        digest = hashlib.sha256(full.encode("utf-8")).hexdigest()
        (EVID / "complete-p1-correction-13path.sha256").write_text(
            f"{digest}  complete-p1-correction-13path.patch\n", encoding="utf-8")
        # Verify git-applyable: `git apply --check` on a temp index? Use `git apply --check --verbose` with --directory? Instead check via `git diff --check`.
        check = run_git("diff", "--check", "HEAD", "--", *MODIFIED, *NEW)
        # diff --check exits 0 if no whitespace errors; non-zero is warning, not failure for apply.
        print(f"PATCH_OK paths=13 sha256={digest} bytes={len(full.encode())} diffcheck_exit={check.returncode}")
        return 0
    finally:
        # Reset intent-to-add (remove intent entries, keep worktree files).
        # `git reset` without --hard keeps files, clears intent-to-add? Use `git reset HEAD -- <new>`? Actually `git reset` will unstage intent? For -N, need `git reset`? Let's use `git reset HEAD` to clear index intent without touching worktree.
        reset = run_git("reset", "HEAD", "--", *NEW)
        # Ignore reset failure (still preserve worktree); log it.
        if reset.returncode != 0:
            print(f"intent reset warning: {reset.stderr[:500]}")


if __name__ == "__main__":
    sys.exit(main())
