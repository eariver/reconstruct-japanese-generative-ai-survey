#!/usr/bin/env python3
"""Create two independent synthetic fixture Git DBs from complete source worktree.

READ ONLY source: /tmp/opencode/jgas-initial-build-20261019T132209Z/candidate-partial-b40de60
Destinations (NEW, outside notes, no embedded .git in notes):
  /tmp/opencode/jgas-initial-fixtures-20261019T133259Z/weekly-fixture
  /tmp/opencode/jgas-initial-fixtures-20261019T133259Z/special-fixture

Copies complete materialized code/control dependencies including all21 overlay
working-tree bytes + needed tests/config/schemas/scripts/templates/prompts/docs/data/.latexmkrc.
Does NOT use setUp's incomplete untracked overlay (copies full worktree, not git ls-files).
Commits source BEFORE any authority generation. Process-scoped synthetic identity only,
no allow-empty, no hooks bypass, no ordinary candidate commits. Inert origin, no alternates.
"""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

TS = "20261019T133259Z"
SOURCE = Path("/tmp/opencode/jgas-initial-build-20261019T132209Z/candidate-partial-b40de60")
DEST_PARENT = Path("/tmp/opencode/jgas-initial-fixtures-20261019T133259Z")
EVIDENCE = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-initial-build-integration/fixtures-20261019T133259Z")
STATIC21 = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-dm021-p3s/draft-history-r11/static21.json")
RECONSTRUCT = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")

FIXTURES = {
    "weekly-fixture": "Synthetic isolated Weekly initial-build fixture source basis (synthetic snapshot, not 409 ancestry)",
    "special-fixture": "Synthetic isolated Special initial-build fixture source basis (synthetic snapshot, not 409 ancestry)",
}

SANITIZED_ENV_KEYS = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                      "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR")

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def run(cmd, cwd, env_extra=None, out_path=None, err_path=None, exit_path=None):
    env = dict(os.environ)
    for k in SANITIZED_ENV_KEYS:
        env.pop(k, None)
    env["GIT_NO_LAZY_FETCH"] = "1"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    if env_extra:
        env.update(env_extra)
    # process-scoped synthetic identity via env (no persistent config writes)
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, env=env)
    if out_path:
        out_path.write_bytes(proc.stdout)
    if err_path:
        err_path.write_bytes(proc.stderr)
    if exit_path:
        exit_path.write_text(str(proc.returncode))
    return proc, env

def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    log = EVIDENCE / "make_fixture_dbs-commands.log"
    with log.open("w") as lf:
        lf.write(f"# make_fixture_dbs {TS} cwd-explicit command log\n")
        # 0. inherited GIT check (must be absent before sanitized runs)
        inherited = {k: v for k, v in os.environ.items() if k in SANITIZED_ENV_KEYS and v}
        lf.write(f"INHERITED_GIT_ENV={json.dumps(inherited)}\n")
        if inherited:
            print(f"FATAL inherited GIT_* set: {inherited}", file=sys.stderr)
            return 2
        # 1. verify source identity read-only
        for args, key in ((["git", "rev-parse", "HEAD"], "src_head"),
                          (["git", "rev-parse", "HEAD^{tree}"], "src_tree"),
                          (["git", "status", "--porcelain=v1", "--untracked-files=all"], "src_status")):
            p, _ = run(["git", "--no-optional-locks", *args[1:]], SOURCE)
            lf.write(f"CMD git {' '.join(args[1:])} cwd=SOURCE exit={p.returncode}\n")
            lf.write(p.stdout.decode(errors="replace"))
            if p.returncode != 0:
                print(f"source check failed: {args}", file=sys.stderr)
                return 3
        src_head = subprocess.run(["git", "--no-optional-locks", "rev-parse", "HEAD"], cwd=SOURCE,
                                  capture_output=True, env={**os.environ, "GIT_NO_LAZY_FETCH": "1",
                                  "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
                                  "GIT_OPTIONAL_LOCKS": "0"}).stdout.decode().strip()
        if src_head != "409b292756dd1277b9dfae87679934c0d2ce251c":
            print(f"source HEAD mismatch: {src_head}", file=sys.stderr)
            return 4
        # static21 input equality (source working-tree bytes)
        static21 = json.loads(STATIC21.read_text())
        mism = []
        for rel, pin in static21.items():
            sp = SOURCE / rel
            if not sp.is_file():
                mism.append(f"missing {rel}")
                continue
            if sha256_file(sp) != pin["sha256"]:
                mism.append(f"sha mismatch {rel}")
            if sp.stat().st_size != pin["bytes"]:
                mism.append(f"bytes mismatch {rel}")
        lf.write(f"STATIC21 source check mismatches={json.dumps(mism)}\n")
        if mism:
            print(f"static21 mismatch: {mism}", file=sys.stderr)
            return 5
        # record source .git census (for later separation)
        def census_git(gitdir: Path):
            files = []
            for q in gitdir.rglob("*"):
                if q.is_file() or q.is_symlink():
                    try:
                        st = q.stat()
                        files.append(f"{st.st_dev}:{st.st_ino}")
                    except OSError:
                        files.append("unstatable")
            return files
        src_git_files = census_git(SOURCE / ".git")
        recon_git_files = census_git(RECONSTRUCT / ".git")
        # 2. create each fixture
        for fname, msg in FIXTURES.items():
            dest = DEST_PARENT / fname
            lf.write(f"--- fixture {fname} ---\n")
            if dest.exists():
                print(f"dest exists, refusing overwrite: {dest}", file=sys.stderr)
                return 6
            dest.mkdir(parents=True)
            lf.write(f"CMD mkdir {dest} exit=0\n")
            # copy full worktree excluding .git / __pycache__ / caches
            copied = 0
            for item in SOURCE.rglob("*"):
                if ".git" in item.parts:
                    continue
                if "__pycache__" in item.parts or item.name == "__pycache__":
                    continue
                if item.name in (".pytest_cache",) or ".pytest_cache" in item.parts:
                    continue
                if item.is_symlink():
                    # do not copy symlinks from source worktree (none expected); record
                    lf.write(f"SKIP symlink {item.relative_to(SOURCE)}\n")
                    continue
                if item.is_dir():
                    (dest / item.relative_to(SOURCE)).mkdir(parents=True, exist_ok=True)
                elif item.is_file():
                    rel = item.relative_to(SOURCE)
                    tgt = dest / rel
                    tgt.parent.mkdir(parents=True, exist_ok=True)
                    tgt.write_bytes(item.read_bytes())
                    copied += 1
            lf.write(f"COPIED {copied} files into {fname}\n")
            # verify all21 content equality into fixture
            mism2 = []
            for rel, pin in static21.items():
                fp = dest / rel
                if not fp.is_file():
                    mism2.append(f"missing {rel}")
                elif sha256_file(fp) != pin["sha256"]:
                    mism2.append(f"sha mismatch {rel}")
            lf.write(f"STATIC21 fixture {fname} mismatches={json.dumps(mism2)}\n")
            if mism2:
                print(f"fixture static21 mismatch {fname}: {mism2}", file=sys.stderr)
                return 7
            # verify .latexmkrc + key control dirs present
            for req in [".latexmkrc", "config/survey-production-v2.json",
                        "schemas/longform-reader-input-v2.schema.json",
                        "templates/survey/jgaisurvey.sty"]:
                if not (dest / req).is_file():
                    print(f"missing required {req} in {fname}", file=sys.stderr)
                    return 8
            # git init + inert origin + source commit (process-scoped identity)
            fenv = {"GIT_AUTHOR_NAME": "Synthetic Initial-Build Fixture",
                    "GIT_AUTHOR_EMAIL": "synthetic-initial-build@example.invalid",
                    "GIT_COMMITTER_NAME": "Synthetic Initial-Build Fixture",
                    "GIT_COMMITTER_EMAIL": "synthetic-initial-build@example.invalid"}
            ev_prefix = EVIDENCE / f"fixture-{fname}"
            for cmd in (["init", "-q"],
                        ["remote", "add", "origin", "https://example.invalid/initial-build-fixture.git"],
                        ["add", "-A"]):
                p, _ = run(["git", "--no-optional-locks", *cmd],
                            dest, env_extra=fenv)
                lf.write(f"CMD git {' '.join(cmd)} cwd={fname} exit={p.returncode} stderr={p.stderr.decode(errors='replace')[:500]}\n")
                if p.returncode != 0:
                    print(f"cmd failed {cmd} in {fname}: {p.stderr.decode()[:1000]}", file=sys.stderr)
                    return 9
            # commit with -c identity overrides (no persistent user.*)
            p, _ = run(["git", "-c", "user.name=Synthetic Initial-Build Fixture",
                        "-c", "user.email=synthetic-initial-build@example.invalid",
                        "commit", "-q", "-m", msg], dest, env_extra=fenv)
            lf.write(f"CMD git commit cwd={fname} exit={p.returncode} stdout={p.stdout.decode(errors='replace')[:500]} stderr={p.stderr.decode(errors='replace')[:500]}\n")
            if p.returncode != 0:
                print(f"commit failed {fname}", file=sys.stderr)
                return 10
            # record HEAD/tree/status/config/origin/alternates
            for args, tag in ((["rev-parse", "HEAD"], "head"),
                              (["rev-parse", "HEAD^{tree}"], "tree"),
                              (["status", "--porcelain=v1", "--untracked-files=all"], "status"),
                              (["config", "--local", "--list"], "config"),
                              (["remote", "-v"], "remote")):
                p, _ = run(["git", "--no-optional-locks", *args], dest, env_extra=fenv)
                outp = EVIDENCE / f"fixture-{fname}-{tag}.txt"
                outp.write_text(p.stdout.decode(errors="replace") + f"\n[exit={p.returncode}]\n")
                lf.write(f"CMD git {' '.join(args)} cwd={fname} exit={p.returncode}\n")
            # prove no persistent user.* in local config
            cfg_text = (EVIDENCE / f"fixture-{fname}-config.txt").read_text()
            if "user.name=" in cfg_text or "user.email=" in cfg_text:
                print(f"persistent user.* leaked in {fname}", file=sys.stderr)
                return 11
            # alternates absent?
            if (dest / ".git/objects/info/alternates").exists():
                print(f"alternates present in {fname}", file=sys.stderr)
                return 12
            # full .git dev:ino separation vs source/reconstruct/dest-sibling
            dest_git_files = census_git(dest / ".git")
            overlap_src = set(dest_git_files) & set(src_git_files)
            overlap_recon = set(dest_git_files) & set(recon_git_files)
            lf.write(f"SEPARATION {fname}: dest_git={len(dest_git_files)} src_git={len(src_git_files)} recon_git={len(recon_git_files)} overlap_src={len(overlap_src)} overlap_recon={len(overlap_recon)}\n")
            if overlap_src or overlap_recon:
                print(f"git object sharing detected in {fname}", file=sys.stderr)
                return 13
            # worktree hardlink check for 21 files vs source (dev:ino equality means hardlink)
            linked = []
            for rel in static21:
                try:
                    if (SOURCE / rel).stat().st_ino == (dest / rel).stat().st_ino and \
                       (SOURCE / rel).stat().st_dev == (dest / rel).stat().st_dev:
                        linked.append(rel)
                except OSError:
                    pass
            lf.write(f"HARDLINK21 {fname} shared={json.dumps(linked)}\n")
            if linked:
                print(f"hardlinked worktree files in {fname}: {linked}", file=sys.stderr)
                return 14
            # record HEAD/tree manifest
            head = (EVIDENCE / f"fixture-{fname}-head.txt").read_text().split()[0]
            tree_txt = (EVIDENCE / f"fixture-{fname}-tree.txt").read_text().split()[0]
            lf.write(f"MANIFEST {fname} head={head} tree={tree_txt}\n")
    print("make_fixture_dbs OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
