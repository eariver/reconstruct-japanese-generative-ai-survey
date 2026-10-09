#!/usr/bin/env python3
"""LF-2 independent byte-copy preparation (exact-run evidence, not rerun tool).

Copies actual /tmp/opencode/jgas-lf1-design-20261009T001653Z
(HEAD409 + exact 3 untracked LF-1 files) to a unique DST under /tmp/opencode/.
Asserts expected pins, verifies full object device/inode separation,
no hardlinks/alternates, inert origin, no Git overrides, no lazy fetch.
Writes NOTHING to SRC. Log file created exclusively ('x').
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import time
from pathlib import Path

SRC = Path("/tmp/opencode/jgas-lf1-design-20261009T001653Z")
DST = Path("/tmp/opencode/jgas-lf2-design-20261009T113013Z")
EVID = Path("notes/rephase-1-longform-lf2/evidence-20261009T113013Z")
LOG = EVID / "prepare.log"

EXP_HEAD = "409b292756dd1277b9dfae87679934c0d2ce251c"
EXP_TREE = "8ce3699861505f32d1d60bdc185d4d4f635aedb2"
EXP_PARENT = "34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4"
EXP_STATUS = sorted([
    "?? schemas/longform-reader-input-v2.schema.json",
    "?? scripts/survey_longform_derivation_v2.py",
    "?? tests/test_survey_longform_derivation_v2.py",
])
EXP_HASHES = {
    "scripts/survey_longform_derivation_v2.py": "233e86557f1627203a4f1e4129c953bf34e1319bd8949b1d58b7d417b0744cf7",
    "schemas/longform-reader-input-v2.schema.json": "7bae9d2ac753c83521165c76c9e461ce40ac4e704d9b44d3518ae7b88fbd0643",
    "tests/test_survey_longform_derivation_v2.py": "ce687447539a99eb92532bc34246a271fb489b259e63b31ed6699fcc12fbf913",
}
EXP_ORIGIN = "https://example.invalid/rephase-candidate-recovery.git"

CHILD_ENV = dict(os.environ)
CHILD_ENV["GIT_NO_LAZY_FETCH"] = "1"
CHILD_ENV["GIT_OPTIONAL_LOCKS"] = "0"
CHILD_ENV["GIT_ALLOW_PROTOCOL"] = "file"
for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_CEILING_DIRECTORIES", "GIT_COMMON_DIR"):
    CHILD_ENV.pop(k, None)

lines: list[str] = []

def log(s: str = "") -> None:
    print(s, flush=True)
    lines.append(s)

def run(argv: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    p = subprocess.run(argv, cwd=str(cwd) if cwd else None, env=CHILD_ENV,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    log(f"$ {' '.join(argv)} (cwd={cwd})")
    log(f"  exit={p.returncode}")
    if p.stdout.strip():
        for ln in p.stdout.strip().splitlines():
            log(f"  out: {ln}")
    if p.stderr.strip():
        for ln in p.stderr.strip().splitlines():
            log(f"  err: {ln}")
    return p.returncode, p.stdout, p.stderr

def check(cond: bool, msg: str) -> None:
    log(("CHECK PASS: " if cond else "CHECK FAIL: ") + msg)
    if not cond:
        raise AssertionError(msg)

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def git_identity(repo: Path, label: str) -> dict[str, str]:
    rc, out, _ = run(["git", "-C", str(repo), "rev-parse", "HEAD"], None)
    check(rc == 0, f"{label} rev-parse HEAD exit 0")
    head = out.strip()
    rc, out, _ = run(["git", "-C", str(repo), "rev-parse", "HEAD^{tree}"], None)
    check(rc == 0, f"{label} rev-parse tree exit 0")
    tree = out.strip()
    rc, out, _ = run(["git", "-C", str(repo), "rev-parse", "HEAD^"], None)
    check(rc == 0, f"{label} rev-parse parent exit 0")
    parent = out.strip()
    rc, out, _ = run(["git", "-C", str(repo), "status", "--porcelain=v1", "--untracked-files=all"], None)
    check(rc == 0, f"{label} status exit 0")
    status = sorted([l for l in out.splitlines() if l.strip()])
    rc, out, _ = run(["git", "-C", str(repo), "remote", "get-url", "origin"], None)
    check(rc == 0, f"{label} remote get-url exit 0")
    origin = out.strip()
    rc, out, _ = run(["git", "-C", str(repo), "rev-parse", "--is-shallow-repository"], None)
    check(rc == 0, f"{label} is-shallow exit 0")
    shallow = out.strip()
    return {"head": head, "tree": tree, "parent": parent, "status": status,
            "origin": origin, "shallow": shallow}

def main() -> int:
    log(f"argv={sys.argv}")
    log(f"cwd={os.getcwd()}")
    log(f"python={sys.version.replace(chr(10), ' ')}")
    log(f"time_utc={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_CEILING_DIRECTORIES", "GIT_COMMON_DIR",
              "GIT_NO_LAZY_FETCH", "GIT_OPTIONAL_LOCKS", "GIT_ALLOW_PROTOCOL"):
        log(f"env {k}={os.environ.get(k, '<unset>')}")
    check(SRC.is_dir(), f"SRC exists {SRC}")
    check(not DST.exists(), f"DST absent before copy {DST}")
    check(EVID.is_dir(), f"EVID dir exists {EVID}")

    # Source identity asserts
    ident = git_identity(SRC, "SRC")
    check(ident["head"] == EXP_HEAD, f"SRC HEAD=={EXP_HEAD} got {ident['head']}")
    check(ident["tree"] == EXP_TREE, f"SRC tree=={EXP_TREE} got {ident['tree']}")
    check(ident["parent"] == EXP_PARENT, f"SRC parent=={EXP_PARENT} got {ident['parent']}")
    check(ident["status"] == EXP_STATUS, f"SRC status exactly 3 untracked got {ident['status']}")
    check(ident["origin"] == EXP_ORIGIN, f"SRC origin inert got {ident['origin']}")
    check(ident["shallow"] == "true", f"SRC shallow true got {ident['shallow']}")
    alt = SRC / ".git" / "objects" / "info" / "alternates"
    check(not alt.exists(), "SRC no objects/info/alternates")
    rc, out, _ = run(["git", "-C", str(SRC), "config", "--get", "extensions.partialClone"], None)
    check(rc != 0, "SRC no extensions.partialClone")
    for rel, exp in EXP_HASHES.items():
        got = sha256(SRC / rel)
        check(got == exp, f"SRC hash {rel}=={exp} got {got}")

    # Byte-copy (no hardlinks, preserve symlinks, no shell)
    rc, out, err = run(["cp", "-a", "--no-preserve=links", str(SRC), str(DST)], None)
    # cp on this coreutils may not accept --no-preserve=links with -a; fallback:
    if rc != 0 and "unrecognized" in err or "invalid" in err:
        log("retry without --no-preserve flag (default cp -a creates new inodes)")
        rc, out, err = run(["cp", "-a", str(SRC), str(DST)], None)
    check(rc == 0, f"cp -a exit 0 (stderr: {err.strip()})")
    check(DST.is_dir(), f"DST exists after copy {DST}")

    # DST identity asserts
    dident = git_identity(DST, "DST")
    check(dident["head"] == EXP_HEAD, f"DST HEAD=={EXP_HEAD} got {dident['head']}")
    check(dident["tree"] == EXP_TREE, f"DST tree=={EXP_TREE} got {dident['tree']}")
    check(dident["parent"] == EXP_PARENT, f"DST parent=={EXP_PARENT} got {dident['parent']}")
    check(dident["status"] == EXP_STATUS, f"DST status exactly 3 untracked got {dident['status']}")
    check(dident["origin"] == EXP_ORIGIN, f"DST origin inert got {dident['origin']}")
    check(dident["shallow"] == "true", f"DST shallow true got {dident['shallow']}")
    check(not (DST / ".git" / "objects" / "info" / "alternates").exists(), "DST no alternates")
    rc, _, _ = run(["git", "-C", str(DST), "config", "--get", "extensions.partialClone"], None)
    check(rc != 0, "DST no extensions.partialClone")
    for rel, exp in EXP_HASHES.items():
        got = sha256(DST / rel)
        check(got == exp, f"DST hash {rel}=={exp} got {got}")

    # Tracked-bytes equality via ls-files content hashes.
    # SRC/DST are sparse checkouts (only .github/config/docs/schemas/scripts/
    # specials/templates/tests materialized); many ls-files entries are
    # intentionally absent from the worktree. Compare presence + bytes for
    # materialized regular files only; assert identical absent sets.
    rc, out, _ = run(["git", "-C", str(SRC), "ls-files", "-z"], None)
    check(rc == 0, "SRC ls-files exit 0")
    tracked = [t for t in out.split("\0") if t]
    check(len(tracked) > 500, f"SRC tracked count>500 got {len(tracked)}")
    mism = 0
    compared = 0
    absent_src: list[str] = []
    absent_dst: list[str] = []
    for t in tracked:
        ps, pd = SRC / t, DST / t
        es, ed = ps.is_file() and not ps.is_symlink(), pd.is_file() and not pd.is_symlink()
        # symlinks: compare link targets
        if ps.is_symlink() or pd.is_symlink():
            ls = os.readlink(ps) if ps.is_symlink() else "<absent>"
            ld = os.readlink(pd) if pd.is_symlink() else "<absent>"
            if ls != ld:
                log(f"  SYMLINK MISMATCH: {t} src->{ls} dst->{ld}")
                mism += 1
            else:
                compared += 1
            continue
        if not es and not ed:
            absent_src.append(t)
            continue
        if es != ed:
            log(f"  PRESENCE MISMATCH: {t} src_file={es} dst_file={ed}")
            mism += 1
            continue
        hs, hd = sha256(ps), sha256(pd)
        if hs != hd:
            log(f"  TRACKED MISMATCH: {t} src={hs} dst={hd}")
            mism += 1
        else:
            compared += 1
    log(f"tracked materialized compared={compared} both-absent={len(absent_src)} mism={mism}")
    check(mism == 0, f"all materialized tracked bytes identical (compared={compared} mism={mism})")
    # Sparse scope record
    rc, out, _ = run(["git", "-C", str(SRC), "sparse-checkout", "list"], None)
    if rc == 0:
        log(f"SRC sparse list: {out.strip().splitlines()}")
    rc, out, _ = run(["git", "-C", str(DST), "sparse-checkout", "list"], None)
    if rc == 0:
        log(f"DST sparse list: {out.strip().splitlines()}")

    # Object device/inode separation (regular files only)
    def obj_files(root: Path) -> dict[tuple[int, int], str]:
        m: dict[tuple[int, int], str] = {}
        base = root / ".git" / "objects"
        for dirpath, _, filenames in os.walk(base):
            for fn in filenames:
                p = Path(dirpath) / fn
                try:
                    st = p.stat()
                except FileNotFoundError:
                    continue
                import stat as _stat
                if not _stat.S_ISREG(st.st_mode):
                    continue
                key = (st.st_dev, st.st_ino)
                if key in m:
                    log(f"  NOTE duplicate key within same repo (hardlink?): {p} already {m[key]}")
                m[key] = str(p)
        return m
    s_objs = obj_files(SRC)
    d_objs = obj_files(DST)
    log(f"SRC objects regular files: {len(s_objs)}")
    log(f"DST objects regular files: {len(d_objs)}")
    shared = set(s_objs.keys()) & set(d_objs.keys())
    check(len(shared) == 0, f"zero shared object (dev,ino) got {len(shared)}")
    # DST hardlink check: all regular object files nlink==1
    import stat as _stat
    multilink = 0
    base = DST / ".git" / "objects"
    for dirpath, _, filenames in os.walk(base):
        for fn in filenames:
            p = Path(dirpath) / fn
            try:
                st = p.lstat()
            except FileNotFoundError:
                continue
            if _stat.S_ISREG(st.st_mode) and st.st_nlink != 1:
                multilink += 1
                log(f"  MULTILINK: {p} nlink={st.st_nlink}")
    check(multilink == 0, f"DST no multilink regular object files (multilink={multilink})")
    # Overlay files also nlink==1 and distinct inodes across SRC/DST
    for rel in EXP_HASHES:
        ss = (SRC / rel).stat()
        ds = (DST / rel).stat()
        check((ss.st_dev, ss.st_ino) != (ds.st_dev, ds.st_ino), f"overlay {rel} distinct inode")
        check(ds.st_nlink == 1, f"overlay {rel} dst nlink==1 got {ds.st_nlink}")

    # Source post state unchanged
    post = git_identity(SRC, "SRC-POST")
    check(post["head"] == EXP_HEAD, "SRC-POST HEAD unchanged")
    check(post["status"] == EXP_STATUS, "SRC-POST status unchanged")
    for rel, exp in EXP_HASHES.items():
        check(sha256(SRC / rel) == exp, f"SRC-POST hash {rel} unchanged")

    log("ALL CHECKS PASSED")
    return 0

if __name__ == "__main__":
    # Exclusive log creation
    try:
        fh = open(LOG, "x", encoding="utf-8")
    except FileExistsError:
        print(f"refusing to overwrite existing {LOG}", file=sys.stderr)
        sys.exit(2)
    with fh:
        old = sys.stdout
        class Tee:
            def write(self, s):
                old.write(s)
                fh.write(s)
            def flush(self):
                old.flush()
                fh.flush()
        sys.stdout = Tee()
        try:
            code = main()
        except AssertionError as e:
            log(f"FAILED: {e}")
            code = 1
        except Exception as e:
            log(f"ERROR: {type(e).__name__}: {e}")
            code = 1
        finally:
            sys.stdout = old
            fh.write("\n".join(lines[-0:]) if False else "")
    sys.exit(code)
