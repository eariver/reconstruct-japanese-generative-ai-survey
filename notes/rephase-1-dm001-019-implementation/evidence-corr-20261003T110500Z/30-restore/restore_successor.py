#!/usr/bin/env python3
"""Fail-closed offline restore of the enumerated successor pack.

Creates a NEW absent DB only (refuses existing destinations), unpacks the
exact object set, points a new branch at the successor commit and verifies
exact HEAD/tree/parent-linkage/3-path bytes with no remotes, no alternates
and no shared object store. No network, no test suite, no old scripts.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

DST = Path(sys.argv[1])
PACK = Path(sys.argv[2])
MANIFEST = Path(sys.argv[3])
CHANGED = Path(sys.argv[4])

BASE_ENV = {"PATH": "/usr/bin:/bin", "GIT_NO_LAZY_FETCH": "1",
            "GIT_OPTIONAL_LOCKS": "0", "GIT_ALLOW_PROTOCOL": "file"}


def run(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True,
                          cwd=str(DST), env=dict(BASE_ENV), **kwargs)


def fail(msg: str) -> int:
    print(f"RESTORE_REFUSED: {msg}", flush=True)
    return 1


def main() -> int:
    if DST.exists():
        return fail(f"destination exists: {DST}")
    if not PACK.is_file():
        return fail(f"pack missing: {PACK}")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    head, tree = manifest["head"], manifest["tree"]
    parent = manifest["direct_parent"]
    for label, value in (("HEAD", head), ("tree", tree), ("parent", parent)):
        if len(value) != 40 or any(c not in "0123456789abcdef" for c in value):
            return fail(f"bad {label} sha in manifest")
    expected_blobs = {row["path"]: row["blob"] for row in manifest["files"]}
    if set(expected_blobs) != {
            "scripts/survey_publication_v2.py",
            "scripts/survey_profiled_freeze_v2.py",
            "tests/test_survey_dm001_019_freeze_equivalence_v2.py"}:
        return fail("unexpected file set in manifest")
    DST.mkdir(parents=False)
    r = run(["git", "init", "-q", "."])
    if r.returncode != 0:
        return fail(f"git init failed: {r.stderr[-500:]}")
    r = subprocess.run(
        # NOTE: no --strict: this is a successor DELTA pack whose parent
        # commit and unchanged subtrees intentionally live in the stated
        # parent-archive prerequisite, not in this pack. --strict refuses
        # objects with such dangling links (observed first-attempt
        # failure, preserved in restore-run.log). Exactness is enforced
        # below by HEAD/tree/parent-linkage/blob/byte gates instead.
        ["git", "unpack-objects"], input=PACK.read_bytes(),
        capture_output=True, cwd=str(DST), env=dict(BASE_ENV))
    if r.returncode != 0:
        return fail(f"unpack-objects failed: {r.stderr.decode()[-500:]}")
    branch = "refs/heads/dm001019-restored"
    if run(["git", "show-ref", "--verify", "--quiet", branch]).returncode == 0:
        return fail("ref already exists")
    if run(["git", "update-ref", branch, head]).returncode != 0:
        return fail("update-ref failed")
    if run(["git", "symbolic-ref", "HEAD", branch]).returncode != 0:
        return fail("symbolic-ref failed")
    checks: list[str] = []

    def check(label: str, ok: bool, detail: str = "") -> bool:
        checks.append(f"{label}={'PASS' if ok else 'FAIL'} {detail}")
        return ok

    ok = True
    r = run(["git", "rev-parse", "HEAD"])
    ok &= check("head", r.stdout.strip() == head, r.stdout.strip())
    r = run(["git", "rev-parse", "HEAD^{tree}"])
    ok &= check("tree", r.stdout.strip() == tree, r.stdout.strip())
    r = run(["git", "cat-file", "commit", "HEAD"])
    ok &= check("parent-linkage", f"\nparent {parent}\n" in f"\n{r.stdout}\n", "")
    for rel, blob in expected_blobs.items():
        r = run(["git", "ls-tree", "HEAD", "--", rel])
        parts = r.stdout.strip().split()
        ok &= check(f"blob:{rel}", len(parts) == 4 and parts[2] == blob, r.stdout.strip())
        show = subprocess.run(
            ["git", "show", f"HEAD:{rel}"], capture_output=True,
            cwd=str(DST), env=dict(BASE_ENV))
        disk = (CHANGED / rel).read_bytes()
        ok &= check(f"bytes:{rel}",
                    show.returncode == 0 and show.stdout == disk
                    and hashlib.sha256(show.stdout).hexdigest()
                    == manifest["files"][[f["path"] for f in manifest["files"]].index(rel)][
                        "worktree_sha256"],
                    f"{len(show.stdout)}B")
    for obj in manifest["new_objects"]:
        r = run(["git", "cat-file", "-e", obj["sha"]])
        ok &= check(f"object:{obj['sha'][:12]}", r.returncode == 0, "")
    r = run(["git", "remote", "-v"])
    ok &= check("no-remotes", r.stdout.strip() == "", "")
    ok &= check("no-alternates", not (DST / ".git/objects/info/alternates").exists(), "")
    inode = DST.stat()
    print(f"RESTORE_DB={DST} gitdir_inode={inode.st_ino} dev={inode.st_dev}", flush=True)
    for line in checks:
        print(line, flush=True)
    if not ok:
        print("RESTORE_RESULT=FAIL", flush=True)
        return 1
    print(f"RESTORE_RESULT=OK HEAD={head} TREE={tree} PARENT_LINK={parent}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
