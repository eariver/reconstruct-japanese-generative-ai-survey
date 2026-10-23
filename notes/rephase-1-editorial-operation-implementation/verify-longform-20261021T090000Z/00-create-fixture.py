#!/usr/bin/env python3
"""Worker A LONGFORM: independent fixture creation (tracked717 only + .git bytecopy).

SOURCE snapshot: /tmp/opencode/jgas-editorial-r2v-20261021T084804Z/candidate-partial-b40de60
  SOURCE_HEAD 4ff2d8562502db36223332c45c9cc5d01bb93156
  SOURCE_TREE 4a0c5343937151af0c0ad4522177441acd0e8fcc (717 tracked)
DST fixture: /tmp/opencode/jgas-editorial-longform-20261021T090000Z/candidate-partial-b40de60
Rules: exact `git ls-files -z` tracked bytes only (no untracked authority/cache/tmp),
  independent .git bytecopy (no hardlinks/alternates/shared objects), same SOURCEHEAD,
  inert origin if absent (own fixture only), sanitized Git env, no cache inside source.
No source edits, no network, no clean/reset/rawdelete, no old runners.
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SNAP = Path("/tmp/opencode/jgas-editorial-r2v-20261021T084804Z/candidate-partial-b40de60")
DST = Path("/tmp/opencode/jgas-editorial-longform-20261021T090000Z/candidate-partial-b40de60")
MANIFEST = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-editorial-operation-implementation/verification-source-20261021T084804Z/snapshot-manifest.json")
EXPECTED_HEAD = "4ff2d8562502db36223332c45c9cc5d01bb93156"
EXPECTED_TREE = "4a0c5343937151af0c0ad4522177441acd0e8fcc"
EXPECTED_TRACKED = 717

def _env():
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != "PYTHONPATH"}
    e.update({
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_ALLOW_PROTOCOL": "file",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPYCACHEPREFIX": "/tmp/opencode/lf-pycache-verify",
        "TMPDIR": "/tmp/opencode",
    })
    return e

def _run_git(args, cwd):
    return subprocess.run(["git", "--no-optional-locks", *args], cwd=str(cwd),
                          capture_output=True, text=True, env=_env())

def main() -> int:
    print(f"CREATE_FIXTURE start {datetime.now(timezone.utc).isoformat()}", flush=True)
    print(f"SNAP={SNAP}", flush=True)
    print(f"DST={DST}", flush=True)
    print(f"EXPECTED_HEAD={EXPECTED_HEAD} EXPECTED_TREE={EXPECTED_TREE} EXPECTED_TRACKED={EXPECTED_TRACKED}", flush=True)
    # Preconditions: snapshot exists, HEAD/TREE match, manifest lines 717, snapshot has untracked authorities (must NOT copy)
    assert SNAP.is_dir(), f"SNAP missing: {SNAP}"
    assert MANIFEST.is_file(), f"MANIFEST missing: {MANIFEST}"
    p = _run_git(["rev-parse", "HEAD"], SNAP)
    assert p.returncode == 0, p.stderr
    snap_head = p.stdout.strip()
    print(f"SNAP_HEAD={snap_head}", flush=True)
    assert snap_head == EXPECTED_HEAD, f"SNAP HEAD mismatch: {snap_head}"
    p = _run_git(["rev-parse", "HEAD^{tree}"], SNAP)
    assert p.returncode == 0, p.stderr
    snap_tree = p.stdout.strip()
    print(f"SNAP_TREE={snap_tree}", flush=True)
    assert snap_tree == EXPECTED_TREE, f"SNAP TREE mismatch: {snap_tree}"
    p = _run_git(["ls-files"], SNAP)
    assert p.returncode == 0, p.stderr
    snap_tracked = [l for l in p.stdout.splitlines() if l]
    print(f"SNAP_TRACKED={len(snap_tracked)}", flush=True)
    assert len(snap_tracked) == EXPECTED_TRACKED, f"SNAP tracked {len(snap_tracked)} != {EXPECTED_TRACKED}"
    # Snapshot must have untracked weekly authorities (prove we exclude them)
    p = _run_git(["status", "--short"], SNAP)
    assert p.returncode == 0, p.stderr
    print(f"SNAP_STATUS_LINES={len([l for l in p.stdout.splitlines() if l])}", flush=True)
    print(f"SNAP_STATUS:\n{p.stdout}", flush=True)
    assert "??" in p.stdout, "SNAP expected to have untracked authorities (weekly smoke residue)"
    # Manifest format inspection: file named .json is actually sha text, not JSON
    raw = MANIFEST.read_bytes()
    print(f"MANIFEST_BYTES={len(raw)} MANIFEST_LINES={len(raw.splitlines())}", flush=True)
    try:
        json.loads(raw.decode("utf-8"))
        print("MANIFEST_FORMAT=JSON (unexpected)", flush=True)
        assert False, "manifest named .json but should be sha text, not JSON"
    except Exception as exc:
        print(f"MANIFEST_FORMAT=SHA_TEXT (expected, json parse fails: {type(exc).__name__})", flush=True)
    lines = MANIFEST.read_text(encoding="utf-8").splitlines()
    assert len(lines) == EXPECTED_TRACKED, f"manifest lines {len(lines)} != {EXPECTED_TRACKED}"
    print(f"MANIFEST_SAMPLE0={lines[0]}", flush=True)
    print(f"MANIFEST_SAMPLE_LAST={lines[-1]}", flush=True)
    # DST parent must exist, DST must NOT exist (fail-closed, no overwrite/clean)
    assert DST.parent.is_dir(), f"DST parent missing: {DST.parent}"
    assert not DST.exists(), f"DST already exists (refuse overwrite/clean): {DST}"
    # Enumerate exact tracked via NUL-separated ls-files -z
    proc = subprocess.run(["git", "--no-optional-locks", "ls-files", "-z"],
                          cwd=str(SNAP), capture_output=True, env=_env())
    assert proc.returncode == 0, f"ls-files -z failed: {proc.stderr!r}"
    rels = [r for r in proc.stdout.split(b"\0") if r]
    print(f"LSFILES_Z_COUNT={len(rels)}", flush=True)
    assert len(rels) == EXPECTED_TRACKED, f"ls-files -z {len(rels)} != {EXPECTED_TRACKED}"
    # Copy each tracked byte-exactly with mode preservation, no hardlinks
    for raw_rel in rels:
        rel = raw_rel.decode("utf-8")
        src = SNAP / rel
        dst = DST / rel
        assert src.is_file() and not src.is_symlink(), f"tracked not regular: {rel}"
        dst.parent.mkdir(parents=True, exist_ok=True)
        assert not dst.exists(), f"DST collision: {rel}"
        # byte copy (no hardlink) + mode preserve
        with src.open("rb") as fsrc, dst.open("wb") as fdst:
            shutil.copyfileobj(fsrc, fdst, length=1024*1024)
        st = src.stat()
        os.chmod(dst, stat.S_IMODE(st.st_mode))
        # verify bytes immediately
        assert hashlib.sha256(src.read_bytes()).hexdigest() == hashlib.sha256(dst.read_bytes()).hexdigest(), f"copy drift: {rel}"
    print(f"COPIED_TRACKED={len(rels)}", flush=True)
    # Independent .git bytecopy (no hardlinks/alternates/shared objects)
    src_git = SNAP / ".git"
    dst_git = DST / ".git"
    assert src_git.is_dir(), "SNAP .git missing"
    assert not dst_git.exists(), "DST .git collision"
    shutil.copytree(src_git, dst_git, symlinks=True, copy_function=shutil.copy2)
    print("GIT_BYTECOPY_DONE", flush=True)
    # Verify no hardlink sharing on sample: .git/index + two source files
    for rel in [".git/index", "scripts/survey_schema_v2.py", "scripts/survey_editorial_publication_v2.py"]:
        s = (SNAP / rel).stat() if (SNAP / rel).exists() else None
        d = (DST / rel).stat() if (DST / rel).exists() else None
        if s and d:
            shared = (s.st_dev == d.st_dev and s.st_ino == d.st_ino)
            print(f"INODE_CHECK {rel} src={s.st_dev}:{s.st_ino} dst={d.st_dev}:{d.st_ino} shared={shared}", flush=True)
            assert not shared, f"hardlink sharing detected: {rel}"
    # Verify DST HEAD/TREE same as SNAP (same SOURCEHEAD via bytecopied .git)
    p = _run_git(["rev-parse", "HEAD"], DST)
    assert p.returncode == 0, p.stderr
    dst_head = p.stdout.strip()
    print(f"DST_HEAD={dst_head}", flush=True)
    assert dst_head == EXPECTED_HEAD, f"DST HEAD {dst_head} != {EXPECTED_HEAD}"
    p = _run_git(["rev-parse", "HEAD^{tree}"], DST)
    assert p.returncode == 0, p.stderr
    dst_tree = p.stdout.strip()
    print(f"DST_TREE={dst_tree}", flush=True)
    assert dst_tree == EXPECTED_TREE, f"DST TREE {dst_tree} != {EXPECTED_TREE}"
    p = _run_git(["ls-files"], DST)
    assert p.returncode == 0, p.stderr
    dst_tracked = [l for l in p.stdout.splitlines() if l]
    print(f"DST_TRACKED={len(dst_tracked)}", flush=True)
    assert len(dst_tracked) == EXPECTED_TRACKED, f"DST tracked {len(dst_tracked)}"
    # DST must be clean with NO untracked (proves no authority/cache/tmp copied)
    p = _run_git(["status", "--short"], DST)
    assert p.returncode == 0, p.stderr
    print(f"DST_STATUS={p.stdout!r}", flush=True)
    assert p.stdout.strip() == "", f"DST not clean (untracked/copies?): {p.stdout!r}"
    # Inert origin if absent (own fixture only)
    p = _run_git(["remote", "-v"], DST)
    assert p.returncode == 0, p.stderr
    print(f"DST_REMOTE_BEFORE={p.stdout!r}", flush=True)
    if not p.stdout.strip():
        q = _run_git(["remote", "add", "origin", "https://example.invalid/jgas-longform-verify-20261021T090000Z.git"], DST)
        assert q.returncode == 0, q.stderr
        print("DST_ORIGIN_SET example.invalid (own fixture only)", flush=True)
    else:
        print("DST_REMOTE_PRESENT (kept, no change)", flush=True)
    # No alternates / no common dir / no lazy fetch / no cache inside source
    alt = DST / ".git/objects/info/alternates"
    print(f"ALTERNATES_EXISTS={alt.exists()}", flush=True)
    assert not alt.exists(), "alternates must not exist"
    hooks = sorted((DST / ".git/hooks").iterdir())
    print(f"HOOKS={[h.name for h in hooks]}", flush=True)
    assert all(h.suffix == ".sample" or h.name.endswith(".sample") for h in hooks), "active hooks present"
    for pat, label in [("__pycache__", "PYCACHE"), (".pyc", "PYC"), ("tmpvr", "TMPVR")]:
        found = [str(x) for x in DST.rglob(f"*{pat}*") if ".git" not in str(x)]
        print(f"RESIDUE_{label}={len(found)}", flush=True)
        assert len(found) == 0, f"residue {label}: {found[:5]}"
    # Git config safe checks
    p = _run_git(["config", "--list"], DST)
    assert p.returncode == 0, p.stderr
    print(f"DST_CONFIG:\n{p.stdout}", flush=True)
    assert "promisor" not in p.stdout.lower() and "partial" not in p.stdout.lower(), "lazyfetch promisor present"
    print("CREATE_FIXTURE_OK", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
