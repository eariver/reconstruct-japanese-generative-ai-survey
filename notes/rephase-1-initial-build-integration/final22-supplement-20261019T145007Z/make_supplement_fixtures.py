#!/usr/bin/env python3
"""Supplement source-only fixtures: tracked707 + full .git, no generated authority.

Source fixtures (READ ONLY): /tmp/opencode/jgas-final22-fixtures-20261019T135318Z/{weekly,special}-final22
  (committed SOURCE states 51b0e42b… / 9917a6ff…).
Destinations (NEW): /tmp/opencode/jgas-supplement-fixtures-20261019T145007Z/{weekly,special}-supp
Method per route: `git archive HEAD` (exactly the committed tracked707 tree) piped to
`tar -x`, then byte-copy `.git`. No generated authority exists in the archive.
No new commit (same SOURCE HEAD expected); worktree must be clean.
Verifies: HEAD equality, clean tree, 22 pins (21 static + approved style),
full .git dev:ino independence vs source-positive/reconstruct DBs, no alternates,
no hardlinked worktree files, safe local config, no inherited GIT_* overrides.
"""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
import sys
import tarfile
from pathlib import Path

TS = "20261019T145007Z"
SRCROOT = Path("/tmp/opencode/jgas-final22-fixtures-20261019T135318Z")
DESTROOT = Path("/tmp/opencode/jgas-supplement-fixtures-20261019T145007Z")
EVIDENCE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-initial-build-integration/final22-supplement-20261019T145007Z")
STATIC21 = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm021-p3s/draft-history-r11/static21.json")
RECONSTRUCT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
STYLE_AFTER = "035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec"
STYLE_BYTES = 6569
EXPECT_HEAD = {"weekly": "51b0e42b4540e963c317fc273d0c9639a0b53b6a",
               "special": "9917a6ff0e53229fe4f20702c58876cc904a8dab"}
SANITIZE = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR")

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

def git(args, cwd):
    env = dict(os.environ)
    for k in SANITIZE:
        env.pop(k, None)
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_OPTIONAL_LOCKS": "0"})
    p = subprocess.run(["git", "--no-optional-locks", *args], cwd=str(cwd),
                       capture_output=True, text=True, env=env)
    with open(EVIDENCE / "commands-supplement-fixtures.log", "a") as f:
        f.write(f"CMD git {' '.join(args)} | cwd={cwd} | exit={p.returncode}\n")
    return p

def census_git(gitdir: Path) -> set:
    out = set()
    for q in gitdir.rglob("*"):
        if q.is_file() or q.is_symlink():
            try:
                st = q.stat()
                out.add((st.st_dev, st.st_ino))
            except OSError:
                pass
    return out

def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    open(EVIDENCE / "commands-supplement-fixtures.log", "w").write("# supplement fixtures\n")
    for k in SANITIZE:
        if os.environ.get(k):
            print(f"FATAL inherited {k}", file=sys.stderr); return 2
    static21 = json.loads(STATIC21.read_text())
    rec_git = census_git(RECONSTRUCT / ".git")
    for route in ("weekly", "special"):
        src = SRCROOT / f"{route}-final22"
        if git(["rev-parse", "HEAD"], src).stdout.strip() != EXPECT_HEAD[route]:
            print(f"{route} source fixture HEAD moved", file=sys.stderr); return 3
        dest = DESTROOT / f"{route}-supp"
        if dest.exists():
            print(f"dest exists {dest}", file=sys.stderr); return 4
        dest.mkdir(parents=True)
        # tracked707 via git archive (no generated authority can be present)
        ap = subprocess.run(["git", "--no-optional-locks", "archive", "HEAD"], cwd=str(src),
                            capture_output=True, env={**os.environ, "GIT_NO_LAZY_FETCH": "1",
                            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
                            "GIT_OPTIONAL_LOCKS": "0"})
        with open(EVIDENCE / "commands-supplement-fixtures.log", "a") as f:
            f.write(f"CMD git archive HEAD | cwd={src} | exit={ap.returncode} bytes={len(ap.stdout)}\n")
        if ap.returncode != 0:
            print(f"archive failed {route}", file=sys.stderr); return 5
        import io
        with tarfile.open(fileobj=io.BytesIO(ap.stdout), mode="r:") as tf:
            tf.extractall(path=str(dest))
        n_files = sum(1 for q in dest.rglob("*") if q.is_file() and ".git" not in q.parts)
        with open(EVIDENCE / "commands-supplement-fixtures.log", "a") as f:
            f.write(f"ARCHIVE {route}: {n_files} tracked files materialized (expect 707)\n")
        if n_files != 707:
            print(f"{route} tracked count {n_files} != 707", file=sys.stderr); return 6
        # independent copied Git DB
        import shutil
        shutil.copytree(src / ".git", dest / ".git", symlinks=False)
        with open(EVIDENCE / "commands-supplement-fixtures.log", "a") as f:
            f.write(f"COPYGIT {route}: .git byte-copied (no hardlinks)\n")
        if git(["rev-parse", "HEAD"], dest).stdout.strip() != EXPECT_HEAD[route]:
            print(f"{route} dest HEAD mismatch", file=sys.stderr); return 7
        st = git(["status", "--porcelain=v1", "--untracked-files=all"], dest).stdout.strip()
        (EVIDENCE / f"{route}-supp-status.txt").write_text(st + "\n")
        if st != "":
            print(f"{route} dest not clean", file=sys.stderr); return 8
        bad = [rel for rel, pin in static21.items()
               if not (dest / rel).is_file() or sha256_file(dest / rel) != pin["sha256"]]
        stf = dest / "templates/survey/jgaisurvey.sty"
        if sha256_file(stf) != STYLE_AFTER or stf.stat().st_size != STYLE_BYTES:
            bad.append("templates/survey/jgaisurvey.sty")
        (EVIDENCE / f"{route}-supp-22pin.txt").write_text(json.dumps({"mismatches": bad}, indent=2))
        if bad:
            print(f"{route} pin mismatch {bad}", file=sys.stderr); return 9
        if (dest / ".git/objects/info/alternates").exists():
            print(f"{route} alternates", file=sys.stderr); return 10
        cfg = git(["config", "--local", "--list"], dest).stdout
        (EVIDENCE / f"{route}-supp-config.txt").write_text(cfg)
        if "user.name=" in cfg or "user.email=" in cfg:
            print(f"{route} persistent user.*", file=sys.stderr); return 11
        dg = census_git(dest / ".git")
        sg = census_git(src / ".git")
        ov = (len(dg & sg), len(dg & rec_git))
        with open(EVIDENCE / "commands-supplement-fixtures.log", "a") as f:
            f.write(f"SEPARATION {route}: dest_git={len(dg)} overlap_src={ov[0]} overlap_recon={ov[1]}\n")
        if ov != (0, 0):
            print(f"{route} git sharing", file=sys.stderr); return 12
        linked = [rel for rel in list(static21) + ["templates/survey/jgaisurvey.sty"]
                  if (src / rel).stat().st_ino == (dest / rel).stat().st_ino
                  and (src / rel).stat().st_dev == (dest / rel).stat().st_dev]
        if linked:
            print(f"{route} hardlinks {linked}", file=sys.stderr); return 13
        (EVIDENCE / f"{route}-supp-head.txt").write_text(EXPECT_HEAD[route] + "\n")
    print("supplement fixtures OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
