#!/usr/bin/env python3
"""NEW isolated weekly fixture: 721 ancestry + fixed OWN 741 SOURCE-only commit.

Clones READONLY bootstrap-weekly (721a04d) to new DB, copies untracked old E,
overlays full fixed 741 OWN source (HIGH b124 + new test + P3S 9e2a preserved),
commits source-only (never git add -A, old E stays uncommitted).

Usage: python3 make_fixture_20261025.py BOOT_WEEKLY OWN_SRC DST_PARENT STAMP
"""
from __future__ import annotations
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

def _run(cmd, cwd, env):
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=120, env=env)

def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def main() -> int:
    if len(sys.argv) != 5:
        print(f"usage: {sys.argv[0]} BOOT_WEEKLY OWN_SRC DST_PARENT STAMP", flush=True)
        return 2
    BOOT = Path(sys.argv[1]).resolve()
    OWN = Path(sys.argv[2]).resolve()
    PARENT = Path(sys.argv[3]).resolve()
    STAMP = sys.argv[4].strip()
    for v in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES"):
        if os.environ.get(v):
            print(f"UNSAFE inherited {v}", flush=True)
            return 2
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "1", "GIT_ALLOW_PROTOCOL": "file",
                "PYTHONDONTWRITEBYTECODE": "1", "LC_ALL": "C"})
    PARENT.mkdir(parents=True, exist_ok=True)
    DST = PARENT / f"versioned-renewal-orphanfix-{STAMP}" / "renewal-weekly"
    if DST.exists():
        print(f"FATAL dst exists (no overwrite): {DST}", flush=True)
        return 2
    h = _run(["git", "rev-parse", "HEAD"], BOOT, env)
    print(f"BOOT HEAD={h.stdout.strip()} rc={h.returncode}", flush=True)
    if h.stdout.strip() != "721a04d85532d7855f3e54cc411f5847c787726e":
        print("FATAL BOOT HEAD !=721a04d", flush=True)
        return 2
    h2 = _run(["git", "rev-parse", "HEAD"], OWN, env)
    print(f"OWN HEAD={h2.stdout.strip()} rc={h2.returncode}", flush=True)
    if h2.stdout.strip() != "409b292756dd1277b9dfae87679934c0d2ce251c":
        print("FATAL OWN HEAD !=409", flush=True)
        return 2
    cp = _run(["git", "clone", "--no-hardlinks", str(BOOT), str(DST)], PARENT, env)
    print(f"CLONE rc={cp.returncode}", flush=True)
    if cp.returncode != 0:
        print(cp.stderr[:1000], flush=True)
        return 2
    _run(["git", "remote", "set-url", "origin", "https://example.invalid/versioned-renewal-orphanfix-weekly.git"], DST, env)
    _run(["git", "config", "user.name", "rephase-fixture"], DST, env)
    _run(["git", "config", "user.email", "fixture@example.invalid"], DST, env)
    _run(["git", "config", "commit.gpgsign", "false"], DST, env)
    src_stat = _run(["git", "status", "--porcelain=v1", "--untracked-files=normal"], BOOT, env).stdout
    e_paths: list[str] = []
    for line in src_stat.splitlines():
        if not line.startswith("??"):
            continue
        rel = line[3:].strip().strip('"')
        if ".git" in Path(rel).parts:
            continue
        if (BOOT / rel).exists():
            e_paths.append(rel)
    print(f"E_PATHS={len(e_paths)}", flush=True)
    for rel in sorted(e_paths):
        s, d = BOOT / rel, DST / rel
        if d.exists():
            print(f"FATAL E target exists: {rel}", flush=True)
            return 2
        if s.is_dir() and not s.is_symlink():
            shutil.copytree(str(s), str(d), symlinks=True, copy_function=shutil.copy2)
        else:
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(s), str(d))
    for rel in sorted(e_paths)[:20]:
        s, d = BOOT / rel, DST / rel
        if s.is_file():
            if _sha(s) != _sha(d):
                print(f"FATAL E sha mismatch: {rel}", flush=True)
                return 2
            if (s.stat().st_dev, s.stat().st_ino) == (d.stat().st_dev, d.stat().st_ino):
                print(f"FATAL E inode sharing: {rel}", flush=True)
                return 2
    print("E_COPY_OK", flush=True)
    own_files: list[str] = []
    for root, dirs, files in os.walk(OWN):
        if ".git" in dirs:
            dirs.remove(".git")
        if "/.git/" in root or root.endswith("/.git"):
            continue
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in sorted(files):
            full = os.path.join(root, f)
            if "/.git/" in full:
                continue
            if "__pycache__" in full or full.endswith(".pyc"):
                continue
            rel = os.path.relpath(full, OWN)
            own_files.append(rel)
    print(f"OWN_FILES={len(own_files)}", flush=True)
    if len(own_files) != 741:
        print(f"FATAL OWN !=741 got {len(own_files)}", flush=True)
        return 2
    for rel in own_files:
        s, d = OWN / rel, DST / rel
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(s), str(d))
    print("OVERLAY_OK", flush=True)
    add = _run(["git", "add", "--"] + own_files, DST, env)
    print(f"ADD rc={add.returncode}", flush=True)
    if add.returncode != 0:
        print(add.stderr[:1000], flush=True)
        return 2
    status = _run(["git", "status", "--porcelain=v1", "--untracked-files=all"], DST, env).stdout
    for line in status.splitlines():
        code, path = line[:2], line[3:].strip().strip('"')
        if code[0] in ("A", "M") and path not in own_files:
            print(f"FATAL staged non-source: {line}", flush=True)
            return 2
    untracked = [l for l in status.splitlines() if l.startswith("??")]
    print(f"UNTRACKED_AFTER_ADD={len(untracked)} (E preserved)", flush=True)
    if len(untracked) == 0:
        print("FATAL E missing (should be untracked)", flush=True)
        return 2
    commit = _run(["git", "commit", "-m", "TEST-ONLY: orphanfix 741 source (HIGH b124 intent-collision fix + new test, trio untouched, before authority)", "--no-verify"], DST, env)
    print(f"COMMIT rc={commit.returncode}", flush=True)
    if commit.returncode != 0:
        print(commit.stdout[:1000] + commit.stderr[:1000], flush=True)
        return 2
    head = _run(["git", "rev-parse", "HEAD"], DST, env).stdout.strip()
    print(f"DST HEAD={head}", flush=True)
    # Verify HIGH + TEST pins in DST (fixed code, no metadata fakes).
    for rel, expect in (
        ("scripts/survey_versioned_renewal_v2.py", "b12439d5057003e703992b91f9590c5eb498f48c21977fa7ab51167e48909413"),
        ("scripts/survey_editorial_staged_source_v2.py", "9e2a0ad6b42cb2444f03f2f9db138c6c1e1db7f41434f5fb1878d87f99ca7ab1"),
    ):
        got = _sha(DST / rel)
        print(f"PIN {rel} {got[:12]} expect {expect[:12]} {'OK' if got == expect else 'MISMATCH'}", flush=True)
        if got != expect:
            return 2
    print("FIXTURE_OK", flush=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
