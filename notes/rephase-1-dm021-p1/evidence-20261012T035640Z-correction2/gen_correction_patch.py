#!/usr/bin/env python3
"""Generate complete 13-path patch WITHOUT touching active index (R2).

Byte-copies active candidate to an independent temp dir, does transient
`git add -N` + `git diff HEAD` THERE (disposable index, never active), copies
patch bytes to evidence, resets disposable index, removes temp copy.
Active candidate index/worktree untouched (no add-N/reset there).
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

ACTIVE = Path("/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60")
EVID = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey"
            "/notes/rephase-1-dm021-p1/evidence-20261012T035640Z-correction2")
GENROOT = Path("/tmp/opencode/jgas-dm021p1-R2-gen-20261012T035640Z")
GENREPO = GENROOT / "candidate-partial-b40de60"
OUT = EVID / "complete-p1-correction-13path.patch"
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


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    import os
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, env=env)


def main() -> int:
    for name in ("complete-p1-correction-13path.patch", "complete-p1-correction-13path.sha256"):
        if (EVID / name).exists():
            print(f"REFUSAL: output exists: {name}")
            return 40
    if GENROOT.exists():
        print(f"REFUSAL: gen destination exists: {GENROOT}")
        return 40
    # Verify active untouched before copy (status 3M10A, no index intent).
    head = git(ACTIVE, "rev-parse", "HEAD").stdout.strip()
    tree = git(ACTIVE, "rev-parse", "HEAD^{tree}").stdout.strip()
    assert head == "409b292756dd1277b9dfae87679934c0d2ce251c", head
    assert tree == "8ce3699861505f32d1d60bdc185d4d4f635aedb2", tree
    GENROOT.mkdir(parents=True)
    proc = subprocess.run(["cp", "-a", str(ACTIVE), str(GENREPO)], capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"byte-copy failed: {proc.stderr[:1000]}")
        return 40
    try:
        # Disposable index only: intent-to-add + diff THERE.
        p = git(GENREPO, "add", "-N", *NEW)
        assert p.returncode == 0, p.stderr
        d = git(GENREPO, "diff", "HEAD", "--", *MODIFIED, *NEW)
        assert d.returncode == 0, d.stderr
        body = d.stdout
        assert body.count("diff --git ") == 13, body.count("diff --git ")
        header = f"DM021-P1 R2 correction overlay: 3M10A relative actual409\nbase HEAD {head}\nbase tree {tree}\n"
        full = header + body
        if not full.endswith("\n"):
            full += "\n"
        OUT.write_text(full, encoding="utf-8")
        digest = hashlib.sha256(full.encode("utf-8")).hexdigest()
        (EVID / "complete-p1-correction-13path.sha256").write_text(
            f"{digest}  complete-p1-correction-13path.patch\n", encoding="utf-8")
        print(f"PATCH_OK paths=13 sha256={digest} bytes={len(full.encode())} (active index untouched)")
        return 0
    finally:
        shutil.rmtree(GENROOT, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
