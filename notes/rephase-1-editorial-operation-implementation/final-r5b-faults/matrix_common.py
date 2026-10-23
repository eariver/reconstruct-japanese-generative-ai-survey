#!/usr/bin/env python3
"""Matrix common: fixture copy/verify + per-case subprocess bound to fixture code path.

All NEW scratch ONLY .rephase-1-editorial-runtime/final-r5b-faults/ (ROOT approved).
Original source/positives/inert readonly; never tests inside SOURCE.
ENV no-bytecode BEFORE Python, TMPDIR/cache under approved scratch.
"""
from __future__ import annotations
import hashlib, json, os, subprocess, sys, time
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey").resolve()
SRC = REPO/".rephase-1-editorial-runtime/jgas-editorial-r5b-20261022T140000Z/candidate-partial-b40de60"
FAULT_BASE = REPO/".rephase-1-editorial-runtime/final-r5b-faults"
INERT_W = REPO/".rephase-1-editorial-runtime/final-r5b/weekly-inert"
PRELC_W = REPO/".rephase-1-editorial-runtime/final-r5b/weekly-prelc"
INERT_L = REPO/".rephase-1-editorial-runtime/final-r5b/longform-inert"
PRELC_L = REPO/".rephase-1-editorial-runtime/final-r5b/longform-prelc"
SRC_HEAD = "10e8662e21fd0aa3c2d71c0bb8d6bf6ae3271ae9"
SRC_TREE = "e434978d0d2034f1a6ec51813be92434234bd3b7"
def log(m): print(m, flush=True)
def run_git(cwd, *args):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
    return subprocess.run(["git",*args], cwd=str(cwd), capture_output=True, text=True, timeout=60, env=env)
def sha_file(p: Path) -> str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for ch in iter(lambda: f.read(1<<20), b""): h.update(ch)
    return h.hexdigest()
def verify_fixture(dst: Path, label: str):
    # own .git/toplevel NOT reconstruct, HEAD, 720 files, no hardlinks/alternates/inert origin
    toplevel=run_git(dst,"rev-parse","--show-toplevel").stdout.strip()
    assert Path(toplevel).resolve()==dst.resolve(), f"{label} toplevel {toplevel} != {dst}"
    gitdir=run_git(dst,"rev-parse","--absolute-git-dir").stdout.strip()
    assert Path(gitdir).resolve()==(dst/".git").resolve(), f"{label} gitdir {gitdir}"
    # ensure NOT parent reconstruct db
    assert ".rephase-1-editorial-runtime/final-r5b-faults" in str(dst) or ".rephase-1-editorial-runtime/final-r5b/" in str(dst), f"{label} not approved scratch {dst}"
    head=run_git(dst,"rev-parse","HEAD").stdout.strip()
    assert head==SRC_HEAD, f"{label} HEAD {head} != {SRC_HEAD}"
    n=len([l for l in run_git(dst,"ls-files").stdout.strip().splitlines() if l])
    assert n==720, f"{label} ls-files {n} != 720"
    for alt in [dst/".git"/"objects"/"info"/"alternates", dst/".git"/"info"/"alternates"]:
        assert not alt.exists(), f"{label} alternates {alt}"
    rem=run_git(dst,"remote","-v").stdout.strip()
    assert "example.invalid" in rem, f"{label} origin not inert: {rem}"
    # no hardlinks sample
    for rel in ["scripts/survey_production_v2.py","schemas/publication-surface-revalidation.schema.json"]:
        a=os.stat(SRC/rel); b=os.stat(dst/rel)
        assert (a.st_dev,a.st_ino)!=(b.st_dev,b.st_ino), f"{label} hardlink {rel}"
        assert sha_file(SRC/rel)==sha_file(dst/rel), f"{label} drift {rel}"
    # no tracked dirty
    st=run_git(dst,"status","--porcelain").stdout
    for line in st.splitlines():
        if line.startswith(" M") or line.startswith("M ") or line.startswith(" D"):
            raise AssertionError(f"{label} tracked dirty {line}")
    return True
def cp_fixture(src: Path, dst: Path, label: str):
    if dst.exists(): raise AssertionError(f"exists {dst}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    r=subprocess.run(["cp","-a",str(src),str(dst)], capture_output=True, text=True, timeout=180)
    assert r.returncode==0, f"cp {label} failed {r.stderr[:800]}"
    verify_fixture(dst,label)
    return dst
def base_env(fixture: Path):
    env={k:v for k,v in os.environ.items() if not k.startswith("GIT_") and k not in ("PYTHONPATH","PYTHONPYCACHEPREFIX","TMPDIR","TEMP","TMP")}
    env["PYTHONDONTWRITEBYTECODE"]="1"
    env["PYTHONPYCACHEPREFIX"]=str(FAULT_BASE/"tmp"/"pycache")
    env["TMPDIR"]=str(FAULT_BASE/"tmp")
    env["GIT_NO_LAZY_FETCH"]="1"; env["GIT_OPTIONAL_LOCKS"]="0"; env["GIT_ALLOW_PROTOCOL"]="file"
    env["PYTHONPATH"]=str(fixture)
    Path(env["PYTHONPYCACHEPREFIX"]).mkdir(parents=True, exist_ok=True)
    Path(env["TMPDIR"]).mkdir(parents=True, exist_ok=True)
    return env
def run_subprocess(fixture: Path, argv: list[str], cwd: Path | None = None, timeout: int = 120):
    """Run child bound to fixture code path, capture raw cmd/cwd/exit/timing/stdout/stderr."""
    if cwd is None: cwd=fixture
    env=base_env(fixture)
    # verify toplevel before Git write (child will do Git reads/writes only in fixture)
    t0=time.monotonic()
    p=subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)
    dt=time.monotonic()-t0
    return {"cmd":argv,"cwd":str(cwd),"exit":p.returncode,"dt":dt,"stdout":p.stdout,"stderr":p.stderr,"env_tmp":env["TMPDIR"]}
