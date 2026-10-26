#!/usr/bin/env python3
"""Weekly State lifecycle clone — byte-independent DB + exact E copy.
Input read-only OLD fixture HEAD afab176. No modifications to OLD.
Excludes: none (no owned alias/neg-temp with explicit annotation at capture time).
All untracked + ignored copied by manifest; pycache preserved as observed (annotated, not blind-cleaned).
"""
import os, sys, subprocess, hashlib, shutil, json
from pathlib import Path
from datetime import datetime, timezone

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
OLD = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-continuation-20261025T083000Z/renewal-weekly"
STAMP = "20261025T101500Z"
BASE = REPO / f".rephase-1-editorial-runtime/versioned-renewal-weekly-state-lifecycle-{STAMP}"
FIX = BASE / "renewal-weekly"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-state-lifecycle" / f"setup-{STAMP}"
EVID.mkdir(parents=True, exist_ok=True)
LOG = EVID / "commands.log"

def log(msg):
    print(msg, flush=True)
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(msg + "\n")

def run(cmd, cwd, tag, timeout=1200, env=None):
    if env is None:
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["LC_ALL"] = "C"
        # sanitized GIT root vars
        for k in ["GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"]:
            env.pop(k, None)
        tmpdir = BASE / "tmp-tex"
        tmpdir.mkdir(parents=True, exist_ok=True)
        env["TMPDIR"] = str(tmpdir); env["TMP"] = str(tmpdir); env["TEMP"] = str(tmpdir)
    log(f"$ {' '.join(cmd[:6])}... # {tag}")
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)
    (EVID / f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID / f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID / f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    log(f"-> {tag} exit={proc.returncode} pid-like")
    return proc

LOG.write_text("", encoding="utf-8")
log(f"STAMP {STAMP} OLD_HEAD {(subprocess.run(['git','-C',str(OLD),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip())}")

# 1. clone tracked history byte-independent, no hardlinks
if BASE.exists():
    log(f"BASE exists {BASE} — refusing overwrite")
    sys.exit(2)
p = run(["git","clone","--no-hardlinks",str(OLD),str(FIX)], REPO, "clone-0")
if p.returncode != 0:
    sys.exit(1)
run(["git","-C",str(FIX),"remote","set-url","origin","https://example.invalid/versioned-renewal-weekly-state-lifecycle.git"], REPO, "remote-0")
run(["git","-C",str(FIX),"config","user.name","rephase-fixture"], REPO, "cfg-user-name")
run(["git","-C",str(FIX),"config","user.email","fixture@example.invalid"], REPO, "cfg-user-email")
run(["git","-C",str(FIX),"config","commit.gpgsign","false"], REPO, "cfg-gpgsign")
run(["git","-C",str(FIX),"rev-parse","HEAD"], REPO, "head-pre")
run(["git","-C",str(FIX),"log","--oneline","-8"], REPO, "log-pre")
run(["git","-C",str(FIX),"rev-parse","--absolute-git-dir"], REPO, "gitdir")
run(["test","!","-e",str(FIX/".git/objects/info/alternates")], REPO, "noalternates")
run(["git","-C",str(FIX),"config","--list","--show-origin"], REPO, "config-show")

# E manifest from OLD (untracked + ignored)
def capture_manifest():
    p1 = subprocess.run(["git","--no-optional-locks","status","--porcelain=v1","--untracked-files=all"], cwd=str(OLD), capture_output=True, text=True)
    untracked = [l[3:].strip().strip('"') for l in p1.stdout.splitlines() if l.startswith("?? ")]
    p2 = subprocess.run(["git","--no-optional-locks","ls-files","--others","--ignored","--exclude-standard"], cwd=str(OLD), capture_output=True, text=True)
    ignored = [l.strip() for l in p2.stdout.splitlines() if l.strip()]
    (EVID/"e-manifest-untracked.txt").write_text("\n".join(sorted(untracked))+"\n", encoding="utf-8")
    (EVID/"e-manifest-ignored.txt").write_text("\n".join(sorted(ignored))+"\n", encoding="utf-8")
    log(f"untracked={len(untracked)} ignored={len(ignored)}")
    def h(p):
        fp = OLD/p
        return hashlib.sha256(fp.read_bytes()).hexdigest() if fp.is_file() else "MISSING_DIR" if fp.is_dir() else "MISSING"
    rows = []
    for rel in sorted(set(untracked+ignored)):
        rows.append(f"{h(rel)}  {rel}")
    (EVID/"e-hash-old.txt").write_text("\n".join(rows)+"\n", encoding="utf-8")
    log("E manifest captured")
    return untracked, ignored

untracked, ignored = capture_manifest()

# Copy exact E including ignored + untracked
for fname in ["e-manifest-untracked.txt","e-manifest-ignored.txt"]:
    for line in open(EVID/fname, encoding="utf-8"):
        rel = line.strip()
        if not rel:
            continue
        src = OLD/rel; d = FIX/rel
        if src.is_file():
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, d)
        elif src.is_dir():
            d.mkdir(parents=True, exist_ok=True)
log("E copy done")

# Verify
ok = True
for r in open(EVID/"e-hash-old.txt", encoding="utf-8"):
    r = r.strip()
    if not r:
        continue
    exp, rel = r.split("  ",1)
    fp = FIX/rel
    if exp == "MISSING_DIR":
        if not fp.is_dir():
            log(f"MISMATCH DIR {rel}")
            ok = False
        continue
    got = hashlib.sha256(fp.read_bytes()).hexdigest() if fp.is_file() else "MISSING"
    if got != exp:
        log(f"MISMATCH {rel} exp={exp[:12]} got={got[:12]}")
        ok = False
(EVID/"e-hash-verify.txt").write_text("E_HASH_UNCHANGED\n" if ok else "E_MISMATCH\n", encoding="utf-8")
log("E_HASH_UNCHANGED" if ok else "E_MISMATCH")
if not ok:
    sys.exit(1)

run(["git","-C",str(FIX),"status","--porcelain=v1","--untracked-files=all"], REPO, "status-postE")

# Isolation: nlink + inode overlap + no alternates
fix_git = FIX/".git"; old_git = OLD/".git"
bad = [str(p) for p in fix_git.rglob("*") if p.is_file() and p.stat().st_nlink != 1]
(EVID/"isolation-nlink.txt").write_text(f"nlink_bad={len(bad)}\n", encoding="utf-8")
log(f"nlink_bad={len(bad)}")
if bad:
    log("\n".join(bad[:10]))
    sys.exit(1)
def inos(root):
    s=set()
    for p in Path(root).rglob("*"):
        try:
            st=p.stat(); s.add((st.st_dev, st.st_ino))
        except: pass
    return s
overlap = len(inos(str(fix_git)) & inos(str(old_git)))
(EVID/"isolation-inode.txt").write_text(f"git_inode_overlap={overlap}\n", encoding="utf-8")
log(f"git_inode_overlap={overlap}")
if overlap != 0:
    sys.exit(1)
log(f"alternates_exists={(fix_git/'objects/info/alternates').exists()}")
if (fix_git/"objects/info/alternates").exists():
    sys.exit(1)
run(["git","-C",str(FIX),"rev-parse","HEAD"], REPO, "head-postE")
# Code pre-guard (H6fe P1825d PUB3f S20f HIGH9a Reader098 style a4bd, G5 6e82e97)
import hashlib as hl
codes = {
    "templates/survey/jgaisurvey.sty": "a4bd135aa2876079923ba925f16cc2963c73647e49a3f1460806483d9c092827",
    "scripts/survey_versioned_renewal_history_v2.py": "6fe86e78",
    "scripts/survey_editorial_correction_proposal_v2.py": "825dba1d",
    "scripts/survey_publication_v2.py": "3f4039fd",
    "scripts/survey_versioned_renewal_v2.py": None,
    "scripts/survey_reader_publication_v2.py": "098a2c82",
}
for rel, prefix in codes.items():
    sha = hl.sha256((FIX/rel).read_bytes()).hexdigest()
    log(f"{rel} {sha[:16]}")
    if prefix and not sha.startswith(prefix):
        log(f"CODE DRIFT {rel}")
        sys.exit(1)
head = subprocess.run(["git","-C",str(FIX),"rev-parse","HEAD"], capture_output=True, text=True).stdout.strip()
log(f"FIX HEAD {head}")
if head != "afab1762a90ca568b333abae7f1641ea64bdb5df":
    log("HEAD mismatch expected afab176")
    sys.exit(1)
# Explicit annotation: no exclusions; pycache preserved
(EVID/"exclusion-annotation.txt").write_text("No exclusions: all 225 untracked + 3 ignored copied exactly including scripts/__pycache__/*.pyc (cache residue preserved, not blind-cleaned; no owned alias/neg-temp with explicit annotation to exclude).\n", encoding="utf-8")
log("CLONE DONE")
