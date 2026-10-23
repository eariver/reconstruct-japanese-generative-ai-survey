#!/usr/bin/env python3
"""Second independent fixture for fixed longform attempt (same SOURCEHEAD, new DST, no cache).

SNAP same, DST2=/tmp/opencode/jgas-editorial-longform-20261021T091000Z/candidate-partial-b40de60
Preserves first fixture+raw (no clean/reset/delete of DST1).
"""
from __future__ import annotations
import hashlib, os, shutil, stat, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
SNAP = Path("/tmp/opencode/jgas-editorial-r2v-20261021T084804Z/candidate-partial-b40de60")
DST = Path("/tmp/opencode/jgas-editorial-longform-20261021T091000Z/candidate-partial-b40de60")
EXPECTED_HEAD="4ff2d8562502db36223332c45c9cc5d01bb93156"
EXPECTED_TREE="4a0c5343937151af0c0ad4522177441acd0e8fcc"
EXPECTED_TRACKED=717
def _env():
    e={k:v for k,v in os.environ.items() if not k.startswith("GIT_") and k!="PYTHONPATH"}
    e.update({"GIT_CONFIG_NOSYSTEM":"1","GIT_CONFIG_GLOBAL":"/dev/null","GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file","PYTHONDONTWRITEBYTECODE":"1","PYTHONPYCACHEPREFIX":"/tmp/opencode/lf-pycache-verify","TMPDIR":"/tmp/opencode"})
    return e
def _run_git(args,cwd):
    return subprocess.run(["git","--no-optional-locks",*args],cwd=str(cwd),capture_output=True,text=True,env=_env())
def main()->int:
    print(f"CREATE_FIXTURE2 start {datetime.now(timezone.utc).isoformat()}",flush=True)
    print(f"SNAP={SNAP} DST={DST}",flush=True)
    assert SNAP.is_dir()
    p=_run_git(["rev-parse","HEAD"],SNAP)
    assert p.returncode==0
    assert p.stdout.strip()==EXPECTED_HEAD, p.stdout
    p=_run_git(["rev-parse","HEAD^{tree}"],SNAP)
    assert p.stdout.strip()==EXPECTED_TREE
    assert DST.parent.is_dir(), f"DST parent missing: {DST.parent}"
    assert not DST.exists(), f"DST2 already exists: {DST}"
    proc=subprocess.run(["git","--no-optional-locks","ls-files","-z"],cwd=str(SNAP),capture_output=True,env=_env())
    assert proc.returncode==0
    rels=[r for r in proc.stdout.split(b"\0") if r]
    assert len(rels)==EXPECTED_TRACKED
    for raw_rel in rels:
        rel=raw_rel.decode("utf-8")
        src=SNAP/rel; dst=DST/rel
        assert src.is_file() and not src.is_symlink()
        dst.parent.mkdir(parents=True,exist_ok=True)
        assert not dst.exists()
        with src.open("rb") as fsrc, dst.open("wb") as fdst:
            shutil.copyfileobj(fsrc,fdst,length=1024*1024)
        st=src.stat(); os.chmod(dst,stat.S_IMODE(st.st_mode))
        assert hashlib.sha256(src.read_bytes()).hexdigest()==hashlib.sha256(dst.read_bytes()).hexdigest()
    print(f"COPIED_TRACKED={len(rels)}",flush=True)
    shutil.copytree(SNAP/".git",DST/".git",symlinks=True,copy_function=shutil.copy2)
    print("GIT_BYTECOPY_DONE",flush=True)
    for rel in [".git/index","scripts/survey_schema_v2.py","scripts/survey_editorial_publication_v2.py"]:
        s=(SNAP/rel).stat(); d=(DST/rel).stat()
        shared=(s.st_dev==d.st_dev and s.st_ino==d.st_ino)
        print(f"INODE_CHECK {rel} shared={shared}",flush=True)
        assert not shared
    p=_run_git(["rev-parse","HEAD"],DST); assert p.stdout.strip()==EXPECTED_HEAD
    p=_run_git(["rev-parse","HEAD^{tree}"],DST); assert p.stdout.strip()==EXPECTED_TREE
    p=_run_git(["ls-files"],DST); assert len([l for l in p.stdout.splitlines() if l])==EXPECTED_TRACKED
    p=_run_git(["status","--short"],DST); print(f"DST_STATUS={p.stdout!r}",flush=True); assert p.stdout.strip()==""
    p=_run_git(["remote","-v"],DST)
    print(f"DST_REMOTE_BEFORE={p.stdout!r}",flush=True)
    if not p.stdout.strip():
        q=_run_git(["remote","add","origin","https://example.invalid/jgas-longform-verify-20261021T091000Z.git"],DST)
        assert q.returncode==0
        print("DST_ORIGIN_SET",flush=True)
    alt=DST/".git/objects/info/alternates"; print(f"ALTERNATES_EXISTS={alt.exists()}",flush=True); assert not alt.exists()
    for pat in ["__pycache__",".pyc","tmpvr"]:
        found=[str(x) for x in DST.rglob(f"*{pat}*") if ".git" not in str(x)]
        print(f"RESIDUE_{pat}={len(found)}",flush=True); assert len(found)==0
    print("CREATE_FIXTURE2_OK",flush=True)
    return 0
if __name__=="__main__":
    sys.exit(main())
