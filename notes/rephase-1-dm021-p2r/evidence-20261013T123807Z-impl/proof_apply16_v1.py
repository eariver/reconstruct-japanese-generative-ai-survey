#!/usr/bin/env python3
"""Independent clean409 saved-patch proof (P2R 16-path).

Byte-copies active (no writes there), reverts 16 overlays in COPY to
clean409, applies EXACT saved patch, verifies all16 bytes/modes/status/base
+ object separation. No commits/branches/network, no active add-N.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ACTIVE = Path("/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60")
COPYROOT = Path("/tmp/opencode/jgas-dm021p2r-verify-20261013T123807Z")
COPYREPO = COPYROOT / "candidate-partial-b40de60"
EVID = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey"
            "/notes/rephase-1-dm021-p2r/evidence-20261013T123807Z-impl")
PATCH = EVID / "complete-p2r-16path.patch"
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


def fail(msg: str) -> int:
    print(f"PROOF_REFUSAL: {msg}")
    return 40


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, env=env)


def freeze(repo: Path) -> dict:
    out: dict = {}
    out["head"] = git(repo, "rev-parse", "HEAD").stdout.strip()
    out["tree"] = git(repo, "rev-parse", "HEAD^{tree}").stdout.strip()
    out["status"] = git(repo, "status", "--porcelain=v1", "-uall").stdout
    files: dict = {}
    for rel in MODIFIED + NEW:
        p = repo / rel
        files[rel] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                      "mode": oct(p.stat().st_mode & 0o777), "bytes": p.stat().st_size}
    out["files"] = files
    return out


def main() -> int:
    for name in ("proof-apply.stdout.txt", "proof-apply.stderr.txt", "proof-apply.exit",
                 "proof-freeze-clean.json", "proof-freeze-applied.json"):
        if (EVID / name).exists():
            return fail(f"proof output exists: {name}")
    if not PATCH.is_file():
        return fail("saved patch missing")
    if COPYROOT.exists():
        return fail(f"copy destination exists: {COPYROOT}")
    COPYROOT.mkdir(parents=True)
    proc = subprocess.run(["cp", "-a", "--reflink=never", str(ACTIVE), str(COPYREPO)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        return fail(f"byte-copy failed: {proc.stderr[:1000]}")
    try:
        a = os.stat(ACTIVE / ".git" / "HEAD")
        c = os.stat(COPYREPO / ".git" / "HEAD")
        if (a.st_ino, a.st_dev) == (c.st_ino, c.st_dev):
            return fail("copy shares HEAD inode with active")
    except OSError as exc:
        return fail(f"separation check unreadable: {exc}")
    cfg = git(COPYREPO, "config", "--list", "--show-origin").stdout
    if "example.invalid" not in cfg:
        return fail("copy origin not inert")
    if (COPYREPO / ".git" / "objects" / "info" / "alternates").exists():
        return fail("copy has alternates")
    # Revert 16 overlays in COPY to clean409 (never in active).
    r = git(COPYREPO, "checkout", "HEAD", "--", *MODIFIED)
    if r.returncode != 0:
        return fail(f"copy checkout failed: {r.stderr[:1000]}")
    for n in NEW:
        try:
            (COPYREPO / n).unlink()
        except FileNotFoundError:
            return fail(f"copy new file already absent: {n}")
    for cache in (COPYREPO / "scripts" / "__pycache__", COPYREPO / "tests" / "__pycache__"):
        shutil.rmtree(cache, ignore_errors=True)
    head = git(COPYREPO, "rev-parse", "HEAD").stdout.strip()
    tree = git(COPYREPO, "rev-parse", "HEAD^{tree}").stdout.strip()
    status = git(COPYREPO, "status", "--porcelain=v1", "-uall").stdout
    if head != "409b292756dd1277b9dfae87679934c0d2ce251c" or status != "":
        return fail(f"copy not clean409: head={head} status={status[:500]!r}")
    (EVID / "proof-freeze-clean.json").write_text(json.dumps(
        {"head": head, "tree": tree, "status": status}, indent=2) + "\n")
    # Apply EXACT saved patch.
    r = git(COPYREPO, "apply", "--check", str(PATCH))
    if r.returncode != 0:
        return fail(f"apply --check failed: {r.stderr[:2000]}")
    r = git(COPYREPO, "apply", str(PATCH))
    if r.returncode != 0:
        return fail(f"apply failed: {r.stderr[:2000]}")
    applied = freeze(COPYREPO)
    (EVID / "proof-freeze-applied.json").write_text(json.dumps(applied, indent=2) + "\n")
    if applied["head"] != "409b292756dd1277b9dfae87679934c0d2ce251c":
        return fail("applied HEAD moved (must stay detached 409, uncommitted)")
    # All16 bytes/modes vs active.
    for rel in MODIFIED + NEW:
        a_data = (ACTIVE / rel).read_bytes()
        c_data = (COPYREPO / rel).read_bytes()
        if a_data != c_data:
            return fail(f"byte mismatch after apply: {rel}")
        if oct((ACTIVE / rel).stat().st_mode & 0o777) != oct((COPYREPO / rel).stat().st_mode & 0o777):
            return fail(f"mode mismatch after apply: {rel}")
    st = applied["status"]
    for m in MODIFIED:
        if f" M {m}" not in st:
            return fail(f"applied status missing M: {m}")
    for n in NEW:
        if f"?? {n}" not in st:
            return fail(f"applied status missing ??: {n}")
    print(f"APPLY_PROOF_OK head={applied['head']} files=16")
    return 0


if __name__ == "__main__":
    sys.exit(main())
