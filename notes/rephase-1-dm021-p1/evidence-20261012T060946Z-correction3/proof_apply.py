#!/usr/bin/env python3
"""Independent 409-copy apply proof (R2): byte-copy active, revert 13 overlays
in COPY to clean409, apply EXACT saved patch, verify 13 bytes/modes/status/base.

Preserves active source/inputs (no writes there), no commits/branches/network.
Also verifies object separation (no shared inodes between active and copy).
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

ACTIVE = Path("/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60")
COPYROOT = Path("/tmp/opencode/jgas-dm021p1-R2-verify-20261012T060946Z")
COPYREPO = COPYROOT / "candidate-partial-b40de60"
EVID = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey"
            "/notes/rephase-1-dm021-p1/evidence-20261012T060946Z-correction3")
PATCH = EVID / "complete-p1-correction-13path.patch"
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


def fail(msg: str) -> int:
    print(f"PROOF_REFUSAL: {msg}")
    return 40


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"})
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, env=env)


def main() -> int:
    for name in ("proof-apply.stdout.txt", "proof-apply.stderr.txt", "proof-apply.exit",
                 "proof-freeze-clean.json", "proof-freeze-applied.json"):
        if (EVID / name).exists():
            return fail(f"proof output exists: {name}")
    if not PATCH.is_file():
        return fail("saved patch missing; run gen first")
    if COPYROOT.exists():
        return fail(f"copy destination exists: {COPYROOT}")
    COPYROOT.mkdir(parents=True)
    proc = subprocess.run(["cp", "-a", str(ACTIVE), str(COPYREPO)], capture_output=True, text=True)
    if proc.returncode != 0:
        return fail(f"byte-copy failed: {proc.stderr[:1000]}")
    # Object separation: no shared inodes for .git objects between active and copy.
    try:
        a_stat = os.stat(ACTIVE / ".git" / "HEAD")
        c_stat = os.stat(COPYREPO / ".git" / "HEAD")
        # HEAD files are distinct copies (different inodes/dev expected after cp -a without --link).
        if (a_stat.st_ino, a_stat.st_dev) == (c_stat.st_ino, c_stat.st_dev):
            return fail("object separation failed: copy shares HEAD inode with active")
    except OSError as exc:
        return fail(f"separation check unreadable: {exc}")
    cfg = git(COPYREPO, "config", "--list", "--show-origin").stdout
    if "example.invalid" not in cfg:
        return fail("copy origin not inert")
    if (COPYREPO / ".git" / "objects" / "info" / "alternates").exists():
        return fail("copy has alternates")
    freeze_pre = json.loads((EVID / "freeze-pre.json").read_text(encoding="utf-8"))
    head = git(COPYREPO, "rev-parse", "HEAD").stdout.strip()
    tree = git(COPYREPO, "rev-parse", "HEAD^{tree}").stdout.strip()
    status = git(COPYREPO, "status", "--porcelain").stdout
    if head != freeze_pre["head"] or tree != freeze_pre["tree"] or status != freeze_pre["status"]:
        return fail("copy identity mismatch before revert")
    for rel, meta in freeze_pre["files"].items():
        data = (COPYREPO / rel).read_bytes()
        if hashlib.sha256(data).hexdigest() != meta["sha256"]:
            return fail(f"copy content mismatch: {rel}")
    proc = git(COPYREPO, "checkout", "HEAD", "--", *MODIFIED)
    if proc.returncode != 0:
        return fail(f"copy checkout failed: {proc.stderr[:1000]}")
    for rel in NEW:
        if ".git" in Path(rel).parts or Path(rel).is_absolute() or ".." in Path(rel).parts:
            return fail(f"unsafe overlay: {rel}")
        target = COPYREPO / rel
        if target.is_symlink() or target.is_file():
            target.unlink()
        elif target.exists():
            return fail(f"overlay not a file: {rel}")
    for cache in ("scripts/__pycache__", "tests/__pycache__", "schemas/__pycache__"):
        full = COPYREPO / cache
        if full.is_dir():
            shutil.rmtree(full)
    clean_status = git(COPYREPO, "status", "--porcelain").stdout
    clean_head = git(COPYREPO, "rev-parse", "HEAD").stdout.strip()
    clean_tree = git(COPYREPO, "rev-parse", "HEAD^{tree}").stdout.strip()
    if clean_status.strip() != "":
        return fail(f"copy not clean: {clean_status[:1000]}")
    if clean_head != "409b292756dd1277b9dfae87679934c0d2ce251c":
        return fail(f"copy HEAD not 409: {clean_head}")
    if clean_tree != "8ce3699861505f32d1d60bdc185d4d4f635aedb2":
        return fail(f"copy tree not 8ce: {clean_tree}")
    (EVID / "proof-freeze-clean.json").write_text(
        json.dumps({"head": clean_head, "tree": clean_tree, "status": clean_status}, indent=1) + "\n")
    print(f"copy reverted to clean409 head={clean_head}")
    check = git(COPYREPO, "apply", "--check", str(PATCH))
    (EVID / "proof-apply.stdout.txt").write_text(check.stdout)
    (EVID / "proof-apply.stderr.txt").write_text(check.stderr)
    if check.returncode != 0:
        (EVID / "proof-apply.exit").write_text(f"exit={check.returncode}\n")
        return fail(f"apply --check failed: {check.stderr[:2000]}")
    apply = git(COPYREPO, "apply", str(PATCH))
    if apply.returncode != 0:
        (EVID / "proof-apply.exit").write_text(f"exit={apply.returncode}\n")
        return fail(f"apply failed: {apply.stderr[:2000]}")
    (EVID / "proof-apply.exit").write_text("exit=0\n")
    print("apply succeeded on clean409 copy")
    applied_files: dict = {}
    for rel in MODIFIED + NEW:
        full = COPYREPO / rel
        data = full.read_bytes()
        applied_files[rel] = {"sha256": hashlib.sha256(data).hexdigest(),
                              "mode": oct(stat.S_IMODE(full.lstat().st_mode)),
                              "bytes": len(data)}
    applied_status = git(COPYREPO, "status", "--porcelain").stdout
    applied_head = git(COPYREPO, "rev-parse", "HEAD").stdout.strip()
    applied_tree = git(COPYREPO, "rev-parse", "HEAD^{tree}").stdout.strip()
    (EVID / "proof-freeze-applied.json").write_text(
        json.dumps({"head": applied_head, "tree": applied_tree, "status": applied_status,
                    "files": applied_files}, indent=1) + "\n")
    if applied_files != freeze_pre["files"]:
        mism = [k for k in applied_files if applied_files[k] != freeze_pre["files"].get(k)]
        return fail(f"applied files differ: {mism}")
    if applied_status != freeze_pre["status"]:
        return fail(f"applied status differs: {applied_status[:1000]}")
    if applied_head != freeze_pre["head"] or applied_tree != freeze_pre["tree"]:
        return fail("applied HEAD/tree differ")
    print("PROOF_COMPLETE: patch applies AS SAVED, all13 bytes/modes/status match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
