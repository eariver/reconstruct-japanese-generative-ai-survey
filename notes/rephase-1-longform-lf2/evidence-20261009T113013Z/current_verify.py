#!/usr/bin/env python3
"""LF-2 current read-only verification (observation only, not copy-time proof).

Asserts NOW (no copy, no candidate imports, no tests/fixtures/ref writes):
seven routing-override vars absent, SRC+DST HEAD/tree/parent, exact 3-status,
exact 3 overlay hashes, fetch+push origins inert, no alternates/partialClone,
zero shared object (dev,ino), DST regular-object nlink==1, sparse lists equal.
Log created exclusively ('x'). Read-only git commands only.
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
LOG = EVID / "current-verification.log"

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
OVERRIDE_VARS = ("GIT_DIR", "GIT_WORK_TREE", "GIT_CEILING_DIRECTORIES",
                 "GIT_COMMON_DIR", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                 "GIT_ALTERNATE_OBJECT_DIRECTORIES")

ENV = dict(os.environ)
ENV["GIT_NO_LAZY_FETCH"] = "1"
ENV["GIT_OPTIONAL_LOCKS"] = "0"
ENV["GIT_ALLOW_PROTOCOL"] = "file"
for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_CEILING_DIRECTORIES", "GIT_COMMON_DIR"):
    ENV.pop(k, None)

lines: list[str] = []

def log(s: str = "") -> None:
    print(s, flush=True)
    lines.append(s)

def run(argv: list[str], cwd: str | None = None) -> tuple[int, str, str]:
    p = subprocess.run(argv, cwd=cwd, env=ENV, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, text=True)
    log(f"$ {' '.join(argv)}")
    log(f"  exit={p.returncode}")
    for ln in p.stdout.strip().splitlines()[:8]:
        log(f"  out: {ln}")
    for ln in p.stderr.strip().splitlines()[:8]:
        log(f"  err: {ln}")
    return p.returncode, p.stdout, p.stderr

def check(cond: bool, msg: str) -> None:
    log(("CHECK PASS: " if cond else "CHECK FAIL: ") + msg)
    if not cond:
        raise AssertionError(msg)

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def main() -> int:
    log(f"cwd={os.getcwd()}")
    log(f"python={sys.version.replace(chr(10), ' ')}")
    log(f"time_utc={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    for k in OVERRIDE_VARS:
        v = os.environ.get(k)
        log(f"parent-env {k}={'<unset>' if v is None else repr(v)}")
        check(v in (None, ""), f"override absent: {k}")
    for label, repo in (("SRC", SRC), ("DST", DST)):
        check(repo.is_dir(), f"{label} exists {repo}")
        rc, out, _ = run(["git", "-C", str(repo), "rev-parse", "HEAD"])
        check(rc == 0 and out.strip() == EXP_HEAD, f"{label} HEAD=={EXP_HEAD}")
        rc, out, _ = run(["git", "-C", str(repo), "rev-parse", "HEAD^{tree}"])
        check(rc == 0 and out.strip() == EXP_TREE, f"{label} tree=={EXP_TREE}")
        rc, out, _ = run(["git", "-C", str(repo), "rev-parse", "HEAD^"])
        check(rc == 0 and out.strip() == EXP_PARENT, f"{label} parent=={EXP_PARENT}")
        rc, out, _ = run(["git", "-C", str(repo), "status",
                          "--porcelain=v1", "--untracked-files=all"])
        check(rc == 0 and sorted(l for l in out.splitlines() if l.strip()) == EXP_STATUS,
              f"{label} status exactly 3 untracked")
        rc, out, _ = run(["git", "-C", str(repo), "remote", "get-url", "origin"])
        check(rc == 0 and out.strip() == EXP_ORIGIN, f"{label} fetch origin inert")
        rc, out, _ = run(["git", "-C", str(repo), "remote", "get-url", "--push", "origin"])
        check(rc == 0 and out.strip() == EXP_ORIGIN, f"{label} push origin inert")
        rc, out, _ = run(["git", "-C", str(repo), "rev-parse", "--is-shallow-repository"])
        check(rc == 0 and out.strip() == "true", f"{label} shallow true")
        check(not (repo / ".git" / "objects" / "info" / "alternates").exists(),
              f"{label} no alternates")
        rc, _, _ = run(["git", "-C", str(repo), "config", "--get", "extensions.partialClone"])
        check(rc == 1, f"{label} no partialClone (exit 1)")
        for rel, exp in EXP_HASHES.items():
            check(sha256(repo / rel) == exp, f"{label} hash {rel}")
        rc, out, _ = run(["git", "-C", str(repo), "sparse-checkout", "list"])
        if rc == 0:
            log(f"{label} sparse: {sorted(out.strip().splitlines())}")

    def objs(root: Path) -> set[tuple[int, int]]:
        import stat as _s
        keys: set[tuple[int, int]] = set()
        for dp, _, fns in os.walk(root / ".git" / "objects"):
            for fn in fns:
                p = Path(dp) / fn
                try:
                    st = p.stat()
                except FileNotFoundError:
                    continue
                if _s.S_ISREG(st.st_mode):
                    keys.add((st.st_dev, st.st_ino))
        return keys

    s_objs, d_objs = objs(SRC), objs(DST)
    log(f"SRC objects={len(s_objs)} DST objects={len(d_objs)}")
    check(len(s_objs) > 0 and len(d_objs) > 0, "both object sets nonempty")
    check(len(s_objs & d_objs) == 0, "zero shared object (dev,ino)")
    import stat as _s
    multi = 0
    for dp, _, fns in os.walk(DST / ".git" / "objects"):
        for fn in fns:
            p = Path(dp) / fn
            try:
                st = p.lstat()
            except FileNotFoundError:
                continue
            if _s.S_ISREG(st.st_mode) and st.st_nlink != 1:
                multi += 1
    check(multi == 0, "DST no multilink regular object files")
    for rel in EXP_HASHES:
        a, b = (SRC / rel).stat(), (DST / rel).stat()
        check((a.st_dev, a.st_ino) != (b.st_dev, b.st_ino), f"overlay distinct inode: {rel}")
    log("ALL CURRENT CHECKS PASSED (observation only, not copy-time proof)")
    return 0

if __name__ == "__main__":
    try:
        fh = open(LOG, "x", encoding="utf-8")
    except FileExistsError:
        print(f"refusing to overwrite {LOG}", file=sys.stderr)
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
        finally:
            sys.stdout = old
    sys.exit(code)
