#!/usr/bin/env python3
"""Verify DST tracked717 bytes vs snapshot-manifest + committed blobs (read-only).

DST: /tmp/opencode/jgas-editorial-longform-20261021T090000Z/candidate-partial-b40de60
MANIFEST: notes/.../verification-source-20261021T084804Z/snapshot-manifest.json (sha text)
Checks:
  1. Every manifest line parses as "<sha256>  <bytes>  <mode>  <path>" (sha text format).
  2. DST file bytes sha256 + size + mode match manifest row.
  3. DST `git ls-files -s` blob hashes equal SNAP blob hashes (no drift).
  4. DST `git cat-file -p HEAD:<path>` bytes sha256 equals working-tree sha256 (committed).
  5. No untracked, no cache, HEAD/TREE pins.
"""
from __future__ import annotations
import hashlib
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SNAP = Path("/tmp/opencode/jgas-editorial-r2v-20261021T084804Z/candidate-partial-b40de60")
DST = Path("/tmp/opencode/jgas-editorial-longform-20261021T090000Z/candidate-partial-b40de60")
MANIFEST = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-editorial-operation-implementation/verification-source-20261021T084804Z/snapshot-manifest.json")
EXPECTED_HEAD = "4ff2d8562502db36223332c45c9cc5d01bb93156"
EXPECTED_TREE = "4a0c5343937151af0c0ad4522177441acd0e8fcc"

def _env():
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != "PYTHONPATH"}
    e.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
              "GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
              "GIT_ALLOW_PROTOCOL": "file", "PYTHONDONTWRITEBYTECODE": "1",
              "PYTHONPYCACHEPREFIX": "/tmp/opencode/lf-pycache-verify", "TMPDIR": "/tmp/opencode"})
    return e

def _git(args, cwd):
    return subprocess.run(["git", "--no-optional-locks", *args], cwd=str(cwd),
                          capture_output=True, text=True, env=_env())

def _git_bytes(args, cwd):
    return subprocess.run(["git", "--no-optional-locks", *args], cwd=str(cwd),
                          capture_output=True, env=_env())

def main() -> int:
    print(f"VERIFY_TRACKED start {datetime.now(timezone.utc).isoformat()}", flush=True)
    assert DST.is_dir(), f"DST missing: {DST}"
    lines = MANIFEST.read_text(encoding="utf-8").splitlines()
    print(f"MANIFEST_LINES={len(lines)}", flush=True)
    assert len(lines) == 717, f"manifest {len(lines)} != 717"
    manifest = {}
    for i, line in enumerate(lines):
        parts = line.split()
        # format: sha bytes mode path (path may contain spaces? none here, but split max 4)
        assert len(parts) >= 4, f"line {i} bad split: {line!r}"
        sha, bstr, mstr = parts[0], parts[1], parts[2]
        path = " ".join(parts[3:]) if len(parts) > 4 else parts[3]
        # sha text inspection
        assert len(sha) == 64 and all(c in "0123456789abcdef" for c in sha), f"line {i} sha bad: {sha}"
        assert bstr.isdigit(), f"line {i} bytes bad: {bstr}"
        assert mstr.isdigit(), f"line {i} mode bad: {mstr}"
        manifest[path] = (sha, int(bstr), mstr)
    print(f"MANIFEST_PARSED={len(manifest)} FORMAT=SHA_TEXT sha/bytes/mode/path", flush=True)
    # HEAD/TREE/status
    for label, args in [("HEAD", ["rev-parse", "HEAD"]), ("TREE", ["rev-parse", "HEAD^{tree}"])]:
        p = _git(args, DST)
        assert p.returncode == 0, p.stderr
        print(f"DST_{label}={p.stdout.strip()}", flush=True)
    assert _git(["rev-parse", "HEAD"], DST).stdout.strip() == EXPECTED_HEAD
    assert _git(["rev-parse", "HEAD^{tree}"], DST).stdout.strip() == EXPECTED_TREE
    p = _git(["status", "--short"], DST)
    assert p.returncode == 0, p.stderr
    print(f"DST_STATUS={p.stdout!r}", flush=True)
    assert p.stdout.strip() == "", "DST not clean"
    # ls-files count
    p = _git(["ls-files"], DST)
    assert p.returncode == 0, p.stderr
    tracked = [l for l in p.stdout.splitlines() if l]
    print(f"DST_TRACKED={len(tracked)}", flush=True)
    assert len(tracked) == 717
    assert set(tracked) == set(manifest.keys()), "tracked set != manifest set"
    # 2. bytes/sha/mode vs manifest
    mism = []
    for rel in tracked:
        f = DST / rel
        data = f.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        exp_sha, exp_bytes, exp_mode = manifest[rel]
        if sha != exp_sha or len(data) != exp_bytes:
            mism.append((rel, sha[:8], exp_sha[:8], len(data), exp_bytes))
        # mode: manifest shows filesystem 664 for all? check actual
        actual_mode = oct(f.stat().st_mode & 0o777).replace("0o", "")
        # manifest mode is like "664" without leading 0; compare
        if actual_mode != exp_mode:
            mism.append((rel + " MODE", actual_mode, exp_mode, 0, 0))
    print(f"MANIFEST_MISMATCHES={len(mism)}", flush=True)
    for m in mism[:10]:
        print(f"MISMATCH {m}", flush=True)
    assert not mism, f"manifest mismatches: {mism[:3]}"
    print("MANIFEST_ALL717_MATCH sha/bytes/mode", flush=True)
    # 3. blob hashes SNAP vs DST equal
    ps = _git(["ls-files", "-s"], SNAP)
    pd = _git(["ls-files", "-s"], DST)
    assert ps.returncode == 0 and pd.returncode == 0, "ls-files -s failed"
    # map path -> blob
    def _parse(s):
        d = {}
        for line in s.splitlines():
            # "100644 <blob> 0\t<path>"
            left, path = line.split("\t")
            mode, blob, stage = left.split()
            d[path] = (mode, blob)
        return d
    ms, md = _parse(ps.stdout), _parse(pd.stdout)
    assert set(ms) == set(md) == set(manifest.keys()), "ls-files set drift"
    blob_mism = [(k, ms[k], md[k]) for k in ms if ms[k] != md[k]]
    print(f"BLOB_MISMATCHES={len(blob_mism)}", flush=True)
    assert not blob_mism, f"blob mismatches: {blob_mism[:3]}"
    print("BLOB_ALL717_EQUAL snap==dst", flush=True)
    # 4. committed bytes == working tree (sample full: all 717 via cat-file)
    # Use git cat-file batch? loop per file with bytes mode to avoid text decode
    bad = []
    for rel in tracked:
        q = _git_bytes(["cat-file", "-p", f"HEAD:{rel}"], DST)
        if q.returncode != 0:
            bad.append((rel, "cat-file rc", q.returncode))
            continue
        committed_sha = hashlib.sha256(q.stdout).hexdigest()
        working_sha = hashlib.sha256((DST / rel).read_bytes()).hexdigest()
        if committed_sha != working_sha:
            bad.append((rel, committed_sha[:8], working_sha[:8]))
        # also vs manifest
        if committed_sha != manifest[rel][0]:
            bad.append((rel + " COMMITvsMANIFEST", committed_sha[:8], manifest[rel][0][:8]))
    print(f"COMMITTED_MISMATCHES={len(bad)}", flush=True)
    for b in bad[:10]:
        print(f"COMMIT_MISMATCH {b}", flush=True)
    assert not bad, f"committed mismatches: {bad[:3]}"
    print("COMMITTED_ALL717_MATCH working==HEAD==manifest", flush=True)
    # 5. no cache/authority
    for pat in ["__pycache__", ".pyc", "tmpvr"]:
        found = [str(x) for x in DST.rglob(f"*{pat}*") if ".git" not in str(x)]
        print(f"RESIDUE_{pat}={len(found)}", flush=True)
        assert not found, f"residue {pat}: {found[:3]}"
    print("VERIFY_TRACKED_OK", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
