#!/usr/bin/env python3
"""Generate complete 16-path patch WITHOUT touching active index.

Byte-copies active P2R candidate to a disposable dir, does transient
`git add -N` + `git diff HEAD` THERE (disposable index only), saves patch +
sha256 to evidence, verifies active untouched. No add-N/reset in active.
Failures preserved via stdout/exit (direct capture by caller).
"""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

ACTIVE = Path("/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60")
EVID = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey"
            "/notes/rephase-1-dm021-p2r/evidence-20261013T123807Z-impl")
GENROOT = Path("/tmp/opencode/jgas-dm021p2r-gen-20261013T123807Z")
GENREPO = GENROOT / "candidate-partial-b40de60"
OUT = EVID / "complete-p2r-16path.patch"
OUTHASH = EVID / "complete-p2r-16path.sha256"
MODIFIED = [
    "schemas/reader-surface-gate-v2.schema.json",
    "schemas/reader-surface-semantic-review-v2.schema.json",
    "scripts/survey_reader_surface_gate_v2.py",
]
NEW = [
    "schemas/editorial-correction-proposal-v2.schema.json",
    "schemas/editorial-retention-manifest-v2.schema.json",
    "schemas/longform-publication-source-manifest-v2.schema.json",
    "schemas/longform-reader-input-v2.schema.json",
    "scripts/survey_editorial_correction_proposal_v2.py",
    "scripts/survey_editorial_retention_v2.py",
    "scripts/survey_longform_derivation_v2.py",
    "scripts/survey_longform_generated_v2.py",
    "scripts/survey_longform_semantic_publication_v2.py",
    "tests/test_survey_editorial_correction_proposal_v2.py",
    "tests/test_survey_editorial_retention_v2.py",
    "tests/test_survey_longform_derivation_v2.py",
    "tests/test_survey_longform_publication_integration_v2.py",
]


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, env=env)


def main() -> int:
    if OUT.exists() or OUTHASH.exists():
        print("REFUSAL: patch output exists")
        return 40
    if GENROOT.exists():
        print(f"REFUSAL: gen destination exists: {GENROOT}")
        return 40
    head = git(ACTIVE, "rev-parse", "HEAD").stdout.strip()
    tree = git(ACTIVE, "rev-parse", "HEAD^{tree}").stdout.strip()
    if head != "409b292756dd1277b9dfae87679934c0d2ce251c":
        print(f"REFUSAL: active HEAD moved: {head}")
        return 40
    if tree != "8ce3699861505f32d1d60bdc185d4d4f635aedb2":
        print(f"REFUSAL: active tree moved: {tree}")
        return 40
    status = git(ACTIVE, "status", "--porcelain=v1", "-uall").stdout
    for m in MODIFIED:
        if f" M {m}" not in status:
            print(f"REFUSAL: modified missing in status: {m}\n{status[:2000]}")
            return 40
    for n in NEW:
        if f"?? {n}" not in status:
            print(f"REFUSAL: new missing in status: {n}\n{status[:2000]}")
            return 40
    GENROOT.mkdir(parents=True)
    proc = subprocess.run(["cp", "-a", "--reflink=never", str(ACTIVE), str(GENREPO)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"REFUSAL: byte-copy failed: {proc.stderr[:1000]}")
        return 40
    # Disposable add-N + diff (never in active).
    r = git(GENREPO, "add", "-N", "--", *NEW)
    if r.returncode != 0:
        print(f"REFUSAL: disposable add-N failed: {r.stderr[:1000]}")
        return 40
    r = git(GENREPO, "diff", "HEAD", "--")
    if r.returncode != 0:
        print(f"REFUSAL: disposable diff failed: {r.stderr[:1000]}")
        return 40
    OUT.write_bytes(r.stdout.encode("utf-8"))
    OUTHASH.write_text(hashlib.sha256(r.stdout.encode("utf-8")).hexdigest() + "\n")
    print(f"wrote {OUT} {OUT.stat().st_size}B sha256={OUTHASH.read_text().strip()}")
    # Verify active untouched (no add-N there: check index intent entries absent).
    r2 = git(ACTIVE, "diff", "--cached", "--name-only")
    if r2.stdout.strip() != "":
        print(f"REFUSAL: active index mutated: {r2.stdout[:500]}")
        return 40
    return 0


if __name__ == "__main__":
    sys.exit(main())
