#!/usr/bin/env python3
"""DM021-P1 current-state qualification checks — NEW, authored 2026-10-11T16:15:49Z.

READ-ONLY: no extraction, no worktree mutation, no git writes, no app imports
(stdlib only: hashlib/json/os/tarfile/subprocess), no fixtures/tests/network.
Verifies the CURRENT restored copy + portable archive bytes as current
corroboration — NOT a pre-extraction proof, NOT a general safe restorer.
Any gate failure exits nonzero with a named reason; nothing is repaired.
"""
from __future__ import annotations

import hashlib
import json
import os
import stat
import subprocess
import sys
import tarfile
from pathlib import PurePosixPath

WS = "/home/eariver/git/reconstruct-japanese-generative-ai-survey"
REPO = "/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60"
ARC = WS + "/notes/rephase-1-candidate-recovery/m3-20261003T0445Z/candidate-partial-b40de60.tar.gz"
MANIFEST = WS + "/notes/rephase-1-longform-lf2-implementation/evidence-20261010T120000Z-correction3/hash-manifest.json"
FINAL = "409b292756dd1277b9dfae87679934c0d2ce251c"
FTREE = "8ce3699861505f32d1d60bdc185d4d4f635aedb2"
FPARENT = "34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4"
EXPECTED_STATUS = [
    ("M", "schemas/reader-surface-gate-v2.schema.json"),
    ("M", "scripts/survey_reader_surface_gate_v2.py"),
    ("??", "schemas/longform-publication-source-manifest-v2.schema.json"),
    ("??", "schemas/longform-reader-input-v2.schema.json"),
    ("??", "scripts/survey_longform_derivation_v2.py"),
    ("??", "scripts/survey_longform_generated_v2.py"),
    ("??", "scripts/survey_longform_semantic_publication_v2.py"),
    ("??", "tests/test_survey_longform_derivation_v2.py"),
    ("??", "tests/test_survey_longform_publication_integration_v2.py"),
]

failures: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    print(f"[{'OK' if cond else 'FAIL'}] {name}" + (f" :: {detail}" if detail else ""))
    if not cond:
        failures.append(name)


def git(*args: str) -> subprocess.CompletedProcess[str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH": "1", "GIT_OPTIONAL_LOCKS": "0",
                "GIT_ALLOW_PROTOCOL": "file", "GIT_CEILING_DIRECTORIES": "/tmp/opencode"})
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True, env=env)


print("== Q1 identity/chain/status (read-only git) ==")
check("head-409", git("rev-parse", "HEAD").stdout.strip() == FINAL)
check("tree-8ce", git("rev-parse", "HEAD^{tree}").stdout.strip() == FTREE)
check("parent-34f", git("rev-parse", "HEAD^").stdout.strip() == FPARENT)
for sha, label in (("222a37e9ee2aa96724a491f2c04c2583a86b9650", "C222"),
                   ("e1705b7fed01369767ab9d827c0360117d54aa1f", "CE170"),
                   (FINAL, "FINAL")):
    check(f"cat-file-{label}", git("cat-file", "-e", sha).returncode == 0)
status = git("status", "--porcelain").stdout.splitlines()
rows = sorted((line[:2], line[3:]) for line in status)
check("status-exact-2M7A", rows == sorted(EXPECTED_STATUS),
      f"observed={len(status)} rows")
print("--- observed status ---")
for line in status:
    print("  " + line)

print("== Q2 nine files: type/mode/hash/size (stdlib, no app imports) ==")
manifest = json.load(open(MANIFEST))
for path in sorted(manifest):
    full = os.path.join(REPO, path)
    try:
        st = os.lstat(full)
    except FileNotFoundError:
        check(f"nine-present:{path}", False); continue
    is_reg = stat.S_ISREG(st.st_mode)
    not_link = not os.path.islink(full)
    mode = oct(stat.S_IMODE(st.st_mode))
    data = open(full, "rb").read()
    sha = hashlib.sha256(data).hexdigest()
    check(f"nine:{path}",
          is_reg and not_link and sha == manifest[path]["sha256"]
          and mode == "0o" + manifest[path]["mode"] and len(data) > 0,
          f"reg={is_reg} nolink={not_link} sha_match={sha == manifest[path]['sha256']} "
          f"mode={mode} exp=0o{manifest[path]['mode']} bytes={len(data)}")

print("== Q3 device/inode separation (correct st_dev/st_ino) ==")


def collect_objects(gitdir: str) -> tuple[set[tuple[int, int]], dict[int, int], int]:
    pairs: set[tuple[int, int]] = set()
    nlink_hist: dict[int, int] = {}
    total = 0
    for dirpath, _dirs, files in os.walk(os.path.join(gitdir, "objects")):
        for name in files:
            total += 1
            st = os.lstat(os.path.join(dirpath, name))
            pairs.add((st.st_dev, st.st_ino))
            nlink_hist[st.st_nlink] = nlink_hist.get(st.st_nlink, 0) + 1
    return pairs, nlink_hist, total


rest, rest_links, rest_total = collect_objects(os.path.join(REPO, ".git"))
work, _work_links, work_total = collect_objects(os.path.join(WS, ".git"))
shared = rest & work
rest_devs = {d for d, _i in rest}
print(f"restored objects files={rest_total} distinct(dev,ino)={len(rest)} devs={sorted(rest_devs)} nlink_hist={rest_links}")
print(f"workspace objects files={work_total} distinct(dev,ino)={len(work)}")
print(f"shared(dev,ino)={len(shared)}")
check("zero-shared-devino", len(shared) == 0)
check("restored-nlink-all-one", set(rest_links) == {1}, f"hist={rest_links}")

print("== Q4 archive-member audit (stdlib tarfile, no extraction) ==")
tf = tarfile.open(ARC, "r:gz")
members = tf.getmembers()
names = [m.name for m in members]
topdirs = {PurePosixPath(n).parts[0] for n in names if n}
cats: dict[str, int] = {}
for m in members:
    if m.issym() or m.islnk():
        cats["symlink/hardlink"] = cats.get("symlink/hardlink", 0) + 1
    elif m.isreg():
        cats["regular"] = cats.get("regular", 0) + 1
    elif m.isdir():
        cats["dir"] = cats.get("dir", 0) + 1
    elif m.ischr() or m.isblk() or m.isfifo() or m.isdev():
        cats["device/special"] = cats.get("device/special", 0) + 1
    else:
        cats[f"other:{m.type!r}"] = cats.get(f"other:{m.type!r}", 0) + 1
bad_abs = [n for n in names if PurePosixPath(n).is_absolute()]
bad_dot = [n for n in names if ".." in PurePosixPath(n).parts]
dups = sorted({n for n in names if names.count(n) > 1})
fetchhead = [n for n in names if PurePosixPath(n).parts[-2:] == (".git", "FETCH_HEAD")]
print(f"members={len(members)} topdirs={sorted(topdirs)} types={cats}")
print(f"absolute={len(bad_abs)} dotdot={len(bad_dot)} duplicates={len(dups)} fetchhead={len(fetchhead)}")
check("archive-single-topdir", topdirs == {"candidate-partial-b40de60"}, f"{sorted(topdirs)}")
check("archive-no-abs", bad_abs == [])
check("archive-no-dotdot", bad_dot == [])
check("archive-no-duplicates", dups == [])
check("archive-no-links", cats.get("symlink/hardlink", 0) == 0, str(cats))
check("archive-no-devices", cats.get("device/special", 0) == 0, str(cats))
check("archive-no-fetchhead", fetchhead == [])
check("archive-only-reg-or-dir", set(cats) <= {"regular", "dir"}, str(cats))

print("== Q5 imported config/hooks/remotes/alternates/env ==")
cfg_text = open(os.path.join(REPO, ".git", "config")).read()
print("--- .git/config ---"); print(cfg_text.rstrip())
check("config-no-hookspath", "hooksPath" not in cfg_text)
hookdir = os.path.join(REPO, ".git", "hooks")
active_hooks = []
for name in sorted(os.listdir(hookdir)):
    full = os.path.join(hookdir, name)
    st = os.lstat(full)
    kind = "symlink" if os.path.islink(full) else ("reg" if stat.S_ISREG(st.st_mode) else "other")
    exe = bool(st.st_mode & 0o111)
    print(f"hook {name} kind={kind} mode={oct(stat.S_IMODE(st.st_mode))}")
    if not name.endswith(".sample") and kind == "reg" and exe:
        active_hooks.append(name)
check("hooks-no-active", active_hooks == [], f"active={active_hooks}")
remotes = git("remote", "-v").stdout
print("--- remotes ---"); print(remotes.rstrip())
check("remotes-inert", all("example.invalid" in ln for ln in remotes.splitlines() if ln.strip()))
check("no-alternates", not os.path.exists(os.path.join(REPO, ".git", "objects", "info", "alternates")))
git_env = sorted(f"{k}={v}" for k, v in os.environ.items() if k.startswith("GIT_"))
print(f"inherited-GIT-env={git_env}")
check("no-inherited-git-common", "GIT_COMMON_DIR" not in os.environ)
print("--- available chain ---")
log = git("log", "--oneline", "-14").stdout
print(log.rstrip())
check("chain-has-409-and-b40", "409b292" in log and "b40de60" in log)

print("== RESULT ==")
if failures:
    print(f"QUALIFICATION_FAILS: {failures}")
    sys.exit(10)
print("ALL_CURRENT_CHECKS_PASS")
