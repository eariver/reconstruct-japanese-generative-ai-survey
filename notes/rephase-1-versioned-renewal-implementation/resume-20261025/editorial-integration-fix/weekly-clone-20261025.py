#!/usr/bin/env python3
"""Editorial-integration-fix: weekly clone + P1-fix SOURCE commit + fresh U + P1 prepare.
Own clones from read-only weekly/longform fixtures. Fresh Python per tool commit.
No ordinary candidate/reconstruct commits, no network, no old runners, no cleanup.
"""
import os, sys, json, subprocess, shutil, hashlib, time
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
CAND = REPO / ".rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
WEEKLY_SRC = REPO / ".rephase-1-editorial-runtime/versioned-renewal-weekly-20261025T052132Z/renewal-weekly"
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
BASE = REPO / f".rephase-1-editorial-runtime/versioned-renewal-editorial-fix-{STAMP}"
FIX = BASE / "renewal-weekly-fix"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-integration-fix" / f"weekly-{STAMP}"
EVID.mkdir(parents=True, exist_ok=True)
LOG = EVID / "commands.log"
LOG.write_text("", encoding="utf-8")

def log(msg):
    print(msg, flush=True)
    with open(LOG, "a") as fh:
        fh.write(msg + "\n")

def run(cmd, cwd, tag, timeout=120, env=None):
    if env is None:
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["LC_ALL"] = "C"
        env["GIT_NO_LAZY_FETCH"] = "1"
        env["GIT_CONFIG_NOSYSTEM"] = "1"
        env["GIT_CONFIG_GLOBAL"] = "/dev/null"
        env["GIT_OPTIONAL_LOCKS"] = "0"
        tmpdir = BASE / "tmp-tex"
        tmpdir.mkdir(parents=True, exist_ok=True)
        env["TMPDIR"] = str(tmpdir); env["TMP"] = str(tmpdir); env["TEMP"] = str(tmpdir)
    log(f"$ {' '.join(cmd[:6])}... # {tag} timeout={timeout}s")
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired as exc:
        (EVID / f"{tag}-stdout.txt").write_text(exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or ""), encoding="utf-8")
        (EVID / f"{tag}-stderr.txt").write_text(f"Timeout ({timeout}s)! PID-parent={os.getpid()}\n", encoding="utf-8")
        (EVID / f"{tag}-exit.txt").write_text("TIMEOUT", encoding="utf-8")
        log(f"DONE {tag} TIMEOUT")
        return None
    (EVID / f"{tag}-stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (EVID / f"{tag}-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    (EVID / f"{tag}-exit.txt").write_text(str(proc.returncode), encoding="utf-8")
    log(f"DONE {tag} exit={proc.returncode}")
    return proc

log(f"STAMP {STAMP} REPO-HEAD {subprocess.run(['git','rev-parse','HEAD'],cwd=str(REPO),capture_output=True,text=True).stdout.strip()}")
log(f"CAND P1 {hashlib.sha256((CAND/'scripts/survey_editorial_correction_proposal_v2.py').read_bytes()).hexdigest()}")
log(f"WEEKLY_SRC HEAD {subprocess.run(['git','rev-parse','HEAD'],cwd=str(WEEKLY_SRC),capture_output=True,text=True).stdout.strip()}")

# 1. Clone tracked via git clone --no-hardlinks (read-only originals preserved)
BASE.mkdir(parents=True, exist_ok=True)
p = run(["git","clone","--no-hardlinks",str(WEEKLY_SRC),str(FIX)], REPO, "clone-0", timeout=120)
if p is None or p.returncode != 0:
    log("FATAL clone"); sys.exit(1)
run(["git","-C",str(FIX),"remote","set-url","origin","https://example.invalid/versioned-renewal-editorial-fix-weekly.git"], REPO, "remote-0")
run(["git","-C",str(FIX),"config","user.name","rephase-fixture"], REPO, "cfg-name")
run(["git","-C",str(FIX),"config","user.email","fixture@example.invalid"], REPO, "cfg-email")
run(["git","-C",str(FIX),"config","commit.gpgsign","false"], REPO, "cfg-gpg")
run(["git","-C",str(FIX),"rev-parse","HEAD"], REPO, "head-pre")
run(["git","-C",str(FIX),"log","--oneline","-8"], REPO, "log-pre")
run(["git","-C",str(FIX),"status","--porcelain=v1","--untracked-files=all"], REPO, "status-pre")
run(["git","-C",str(FIX),"rev-parse","--absolute-git-dir"], REPO, "gitdir")
run(["test","!","-e",str(FIX/".git/objects/info/alternates")], REPO, "noalternates")

# 2. Copy untracked (E + renewals + partials) from WEEKLY_SRC via manifest (no blind cache)
# Capture untracked + ignored from source
def _git_lines(cwd, args):
    pr = subprocess.run(["git","--no-optional-locks"]+args, cwd=str(cwd), capture_output=True, text=True)
    return pr.stdout.splitlines()
untracked = [l[3:].strip().strip('"') for l in _git_lines(WEEKLY_SRC, ["status","--porcelain=v1","--untracked-files=all"]) if l.startswith("?? ")]
# ignored (PDF/log etc.)
pr2 = subprocess.run(["git","--no-optional-locks","ls-files","--others","--ignored","--exclude-standard"], cwd=str(WEEKLY_SRC), capture_output=True, text=True)
ignored = [l.strip() for l in pr2.stdout.splitlines() if l.strip()]
(EVID/"e-manifest-untracked.txt").write_text("\n".join(sorted(untracked))+"\n", encoding="utf-8")
(EVID/"e-manifest-ignored.txt").write_text("\n".join(sorted(ignored))+"\n", encoding="utf-8")
log(f"untracked={len(untracked)} ignored={len(ignored)}")
# hash source bytes
def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "MISSING"
rows=[]
for rel in sorted(set(untracked+ignored)):
    if "__pycache__" in Path(rel).parts or rel.endswith(".pyc"):
        continue
    rows.append(f"{_sha(WEEKLY_SRC/rel)}  {rel}")
(EVID/"e-hash-src.txt").write_text("\n".join(rows)+"\n", encoding="utf-8")
# copy (excluding pycache/pyc)
copied=0
for rel in sorted(set(untracked+ignored)):
    if "__pycache__" in Path(rel).parts or rel.endswith(".pyc"):
        continue
    src=WEEKLY_SRC/rel; dst=FIX/rel
    if src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src,dst)
        copied+=1
    elif src.is_dir():
        dst.mkdir(parents=True, exist_ok=True)
log(f"E+renewals copy done copied={copied}")
# verify
ok=True
for r in rows:
    exp, rel = r.split("  ",1)
    got=_sha(FIX/rel)
    if got!=exp:
        log(f"MISMATCH {rel} exp {exp[:8]} got {got[:8]}")
        ok=False
(EVID/"e-hash-verify.txt").write_text("E_HASH_UNCHANGED\n" if ok else "E_HASH_MISMATCH\n", encoding="utf-8")
log(f"E_HASH_{'UNCHANGED' if ok else 'MISMATCH'}")
if not ok:
    log("FATAL E copy mismatch"); sys.exit(1)
run(["git","-C",str(FIX),"status","--porcelain=v1","--untracked-files=all"], REPO, "status-postE")

# 3. Overlay P1 fix + new test (SOURCE-only, exact bytes from CAND)
for rel in ["scripts/survey_editorial_correction_proposal_v2.py","tests/test_editorial_renewal_p1_dispatch_20261025.py"]:
    src=CAND/rel; dst=FIX/rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src,dst)
    log(f"overlay {rel} sha {hashlib.sha256(dst.read_bytes()).hexdigest()[:8]}")
run(["git","-C",str(FIX),"diff","--name-only"], REPO, "diff-pre")
run(["git","-C",str(FIX),"status","--porcelain=v1","--untracked-files=all"], REPO, "status-overlay")
# SOURCE-only add (only those 2, E remains untracked)
padd = run(["git","-C",str(FIX),"add","--","scripts/survey_editorial_correction_proposal_v2.py","tests/test_editorial_renewal_p1_dispatch_20261025.py"], REPO, "add-fix")
run(["git","-C",str(FIX),"diff","--cached","--name-only"], REPO, "diff-cached")
run(["git","-C",str(FIX),"status","--porcelain=v1","--untracked-files=all"], REPO, "status-staged")
# Verify E still untracked (not staged)
pstaged = subprocess.run(["git","--no-optional-locks","diff","--cached","--name-only"], cwd=str(FIX), capture_output=True, text=True)
staged=set(pstaged.stdout.splitlines())
overlap=staged & set(untracked)
log(f"staged={len(staged)} overlap_with_E={len(overlap)}")
if overlap:
    log(f"FATAL staged overlaps E {sorted(overlap)[:5]}"); sys.exit(1)
# Commit G5-fix
pcom = run(["git","-C",str(FIX),"commit","-m","TEST-ONLY: P1 renewal dispatch fix + dispatch unit (SOURCE-only, no E, no authority)"], REPO, "commit-fix")
if pcom is None or pcom.returncode!=0:
    log("FATAL commit"); sys.exit(1)
run(["git","-C",str(FIX),"rev-parse","HEAD"], REPO, "head-post")
run(["git","-C",str(FIX),"log","--oneline","-9"], REPO, "log-post")
run(["git","-C",str(FIX),"rev-parse","HEAD^{tree}"], REPO, "tree-post")
# Verify ancestry: old HEAD must be ancestor
old_head=subprocess.run(["git","-C",str(WEEKLY_SRC),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
new_head=subprocess.run(["git","-C",str(FIX),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
pa=run(["git","-C",str(FIX),"merge-base","--is-ancestor",old_head,new_head], REPO, "ancestor-check")
log(f"old {old_head[:7]} new {new_head[:7]} ancestor rc={pa.returncode if pa else 'TIMEOUT'}")
# Tool SHAs
for rel in ["scripts/survey_editorial_correction_proposal_v2.py","scripts/survey_versioned_renewal_v2.py"]:
    log(f"tool {rel} {hashlib.sha256((FIX/rel).read_bytes()).hexdigest()}")
log("READY FOR U RENEWAL")
print(f"FIX={FIX}")
print(f"EVID={EVID}")
print(f"NEW_HEAD={new_head}")
