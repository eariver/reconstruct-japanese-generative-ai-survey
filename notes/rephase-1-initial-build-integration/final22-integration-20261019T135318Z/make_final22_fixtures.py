#!/usr/bin/env python3
"""Init NEW independent synthetic source-snapshot Git fixtures from final22 candidate.

Source (READ ONLY): /tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60
  HEAD 409b292..., worktree 4M18A22 (21 inherited + approved coltitle style line).
Destinations (NEW, no .git copy; fresh git init => independent synthetic root history):
  /tmp/opencode/jgas-final22-fixtures-20261019T135318Z/weekly-final22
  /tmp/opencode/jgas-final22-fixtures-20261019T135318Z/special-final22
Meaningful SOURCE commit before any authority (process-scoped identity, inert origin,
no empty commit, no hooks bypass). NOT a candidate commit; ancestry labelled synthetic.
Verifies: 22 worktree pins (21 static + approved style), full .git dev:ino independence
vs candidate/source-copy/reconstruct, no alternates/hardlinks, safe local config,
no inherited GIT_* overrides.
"""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

TS = "20261019T135318Z"
SOURCE = Path("/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60")
DEST_PARENT = Path("/tmp/opencode/jgas-final22-fixtures-20261019T135318Z")
EVIDENCE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-initial-build-integration/final22-integration-20261019T135318Z")
STATIC21 = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm021-p3s/draft-history-r11/static21.json")
RECONSTRUCT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
STYLE_AFTER = "035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec"
STYLE_BYTES = 6569

FIXTURES = {
    "weekly-final22": "Synthetic isolated final22 Weekly fixture source basis (synthetic snapshot of 409+22 with approved coltitle fix; not 409 ancestry, not candidate commit)",
    "special-final22": "Synthetic isolated final22 Special fixture source basis (synthetic snapshot of 409+22 with approved coltitle fix; not 409 ancestry, not candidate commit)",
}
SANITIZE = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR")

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()

def git(args, cwd: Path, env_extra: dict | None = None):
    env = dict(os.environ)
    for k in SANITIZE:
        env.pop(k, None)
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_OPTIONAL_LOCKS": "0"})
    if env_extra:
        env.update(env_extra)
    p = subprocess.run(["git", "--no-optional-locks", *args], cwd=str(cwd),
                       capture_output=True, text=True, env=env)
    with open(EVIDENCE / "commands-fixtures.log", "a") as f:
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
    open(EVIDENCE / "commands-fixtures.log", "w").write("# final22 fixtures init\n")
    for k in SANITIZE:
        if os.environ.get(k):
            print(f"FATAL inherited {k}", file=sys.stderr); return 2
    # source read-only checks
    if git(["rev-parse", "HEAD"], SOURCE).stdout.strip() != "409b292756dd1277b9dfae87679934c0d2ce251c":
        print("source HEAD mismatch", file=sys.stderr); return 3
    src_status = git(["status", "--porcelain=v1", "--untracked-files=all"], SOURCE).stdout
    (EVIDENCE / "source22-status-before.txt").write_text(src_status)
    n_m = sum(1 for l in src_status.splitlines() if l.startswith(" M") or l.startswith("M "))
    n_q = sum(1 for l in src_status.splitlines() if l.startswith("??"))
    if (n_m, n_q) != (4, 18):
        print(f"source status not 4M18A22: M={n_m} ??={n_q}", file=sys.stderr); return 4
    static21 = json.loads(STATIC21.read_text())
    src_git = census_git(SOURCE / ".git")
    rec_git = census_git(RECONSTRUCT / ".git")
    for fname, msg in FIXTURES.items():
        dest = DEST_PARENT / fname
        if dest.exists():
            print(f"dest exists {dest}", file=sys.stderr); return 5
        dest.mkdir(parents=True)
        copied = 0
        for item in SOURCE.rglob("*"):
            if ".git" in item.parts or "__pycache__" in item.parts or ".pytest_cache" in item.parts:
                continue
            if item.is_symlink():
                continue
            if item.is_dir():
                (dest / item.relative_to(SOURCE)).mkdir(parents=True, exist_ok=True)
            elif item.is_file():
                rel = item.relative_to(SOURCE)
                tgt = dest / rel
                tgt.parent.mkdir(parents=True, exist_ok=True)
                tgt.write_bytes(item.read_bytes())
                copied += 1
        with open(EVIDENCE / "commands-fixtures.log", "a") as f:
            f.write(f"COPIED {copied} worktree files into {fname}\n")
        # 22-pin verify (21 static + approved style)
        bad = [rel for rel, pin in static21.items()
               if not (dest / rel).is_file() or sha256_file(dest / rel) != pin["sha256"]]
        st = dest / "templates/survey/jgaisurvey.sty"
        if sha256_file(st) != STYLE_AFTER or st.stat().st_size != STYLE_BYTES:
            bad.append("templates/survey/jgaisurvey.sty")
        (EVIDENCE / f"{fname}-22pin-check.txt").write_text(json.dumps({"mismatches": bad}, indent=2))
        if bad:
            print(f"{fname} pin mismatch {bad}", file=sys.stderr); return 6
        fenv = {"GIT_AUTHOR_NAME": "Synthetic Final22 Fixture",
                "GIT_AUTHOR_EMAIL": "synthetic-final22@example.invalid",
                "GIT_COMMITTER_NAME": "Synthetic Final22 Fixture",
                "GIT_COMMITTER_EMAIL": "synthetic-final22@example.invalid"}
        for args in (["init", "-q"],
                     ["remote", "add", "origin", "https://example.invalid/final22-fixture.git"],
                     ["add", "-A"]):
            p = git(args, dest, fenv)
            if p.returncode != 0:
                print(f"cmd failed {args} {p.stderr[:300]}", file=sys.stderr); return 7
        p = git(["-c", "user.name=Synthetic Final22 Fixture",
                 "-c", "user.email=synthetic-final22@example.invalid",
                 "commit", "-q", "-m", msg], dest, fenv)
        if p.returncode != 0:
            print(f"commit failed {p.stderr[:500]}", file=sys.stderr); return 8
        head = git(["rev-parse", "HEAD"], dest).stdout.strip()
        (EVIDENCE / f"{fname}-source-head.txt").write_text(head + "\n")
        if head == "409b292756dd1277b9dfae87679934c0d2ce251c":
            print(f"{fname} head equals 409; mislabelled", file=sys.stderr); return 9
        tree = git(["rev-parse", "HEAD^{tree}"], dest).stdout.strip()
        (EVIDENCE / f"{fname}-source-tree.txt").write_text(tree + "\n")
        for args, tag in ((["status", "--porcelain=v1", "--untracked-files=all"], "status"),
                          (["config", "--local", "--list"], "config"),
                          (["remote", "-v"], "remote")):
            (EVIDENCE / f"{fname}-{tag}.txt").write_text(git(args, dest).stdout)
        if "user.name=" in (EVIDENCE / f"{fname}-config.txt").read_text():
            print(f"{fname} persistent user.*", file=sys.stderr); return 10
        if (dest / ".git/objects/info/alternates").exists():
            print(f"{fname} alternates", file=sys.stderr); return 11
        dg = census_git(dest / ".git")
        ov = (len(dg & src_git), len(dg & rec_git))
        with open(EVIDENCE / "commands-fixtures.log", "a") as f:
            f.write(f"SEPARATION {fname}: dest_git={len(dg)} overlap_src={ov[0]} overlap_recon={ov[1]}\n")
        if ov != (0, 0):
            print(f"{fname} git sharing", file=sys.stderr); return 12
        linked = [rel for rel in list(static21) + ["templates/survey/jgaisurvey.sty"]
                  if (SOURCE / rel).stat().st_ino == (dest / rel).stat().st_ino
                  and (SOURCE / rel).stat().st_dev == (dest / rel).stat().st_dev]
        if linked:
            print(f"{fname} hardlinks {linked}", file=sys.stderr); return 13
        # all 22 code bytes vs committed basis: clean tree => worktree == HEAD
        st_out = git(["status", "--porcelain=v1", "--untracked-files=all"], dest).stdout.strip()
        if st_out != "":
            print(f"{fname} not clean after SOURCE commit", file=sys.stderr); return 14
    print("final22 fixtures OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
