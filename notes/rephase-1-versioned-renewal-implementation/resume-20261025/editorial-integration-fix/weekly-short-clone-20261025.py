#!/usr/bin/env python3
"""Short-chain weekly: clone bootstrap R3, overlay 736+P1 fix as G1, U1, P1 positive.
Fast chain2 (EDITORIAL r1 -> U1 r2) to prove renewal->editorial routing fix within 1200s.
Preserves invalid orphans, fresh Python per tool, new IDs time>=prior, no bypass.
"""
import os, sys, json, subprocess, shutil, hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
REPO = Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
CAND = REPO / ".rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
BOOT = REPO / ".rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly"
SNAP = REPO / ".rephase-1-editorial-runtime/versioned-renewal-final-input-20261025T051343Z/snapshot-work"
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
BASE = REPO / f".rephase-1-editorial-runtime/versioned-renewal-editorial-fix-short-{STAMP}"
FIX = BASE / "renewal-weekly-short"
EVID = REPO / "notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-integration-fix" / f"weekly-short-{STAMP}"
EVID.mkdir(parents=True, exist_ok=True)
LOG=EVID/"commands.log"; LOG.write_text("",encoding="utf-8")
def log(m):
    print(m,flush=True); open(LOG,"a").write(m+"\n")
def run(cmd,cwd,tag,timeout=120,env=None):
    if env is None:
        env=dict(os.environ); env["PYTHONDONTWRITEBYTECODE"]="1"; env["LC_ALL"]="C"
        env["GIT_NO_LAZY_FETCH"]="1"; env["GIT_CONFIG_NOSYSTEM"]="1"; env["GIT_CONFIG_GLOBAL"]="/dev/null"; env["GIT_OPTIONAL_LOCKS"]="0"
        tmpdir=BASE/"tmp-tex"; tmpdir.mkdir(parents=True,exist_ok=True)
        env["TMPDIR"]=str(tmpdir); env["TMP"]=str(tmpdir); env["TEMP"]=str(tmpdir)
    log(f"$ {' '.join(cmd[:6])}... # {tag}")
    try:
        proc=subprocess.run(cmd,cwd=str(cwd),capture_output=True,text=True,timeout=timeout,env=env)
    except subprocess.TimeoutExpired:
        (EVID/f"{tag}-stdout.txt").write_text("",encoding="utf-8"); (EVID/f"{tag}-stderr.txt").write_text(f"Timeout {timeout}s PID={os.getpid()}\n",encoding="utf-8"); (EVID/f"{tag}-exit.txt").write_text("TIMEOUT",encoding="utf-8")
        log(f"DONE {tag} TIMEOUT"); return None
    (EVID/f"{tag}-stdout.txt").write_text(proc.stdout or "",encoding="utf-8"); (EVID/f"{tag}-stderr.txt").write_text(proc.stderr or "",encoding="utf-8"); (EVID/f"{tag}-exit.txt").write_text(str(proc.returncode),encoding="utf-8")
    log(f"DONE {tag} exit={proc.returncode}"); return proc
PY=sys.executable
log(f"STAMP {STAMP} BOOT-HEAD {subprocess.run(['git','rev-parse','HEAD'],cwd=str(BOOT),capture_output=True,text=True).stdout.strip()}")
log(f"CAND P1 {hashlib.sha256((CAND/'scripts/survey_editorial_correction_proposal_v2.py').read_bytes()).hexdigest()[:8]}")
BASE.mkdir(parents=True,exist_ok=True)
p=run(["git","clone","--no-hardlinks",str(BOOT),str(FIX)],REPO,"clone-0",timeout=120)
if p is None or p.returncode!=0: log("FATAL clone"); sys.exit(1)
run(["git","-C",str(FIX),"remote","set-url","origin","https://example.invalid/versioned-renewal-editorial-fix-short-weekly.git"],REPO,"remote-0")
run(["git","-C",str(FIX),"config","user.name","rephase-fixture"],REPO,"cfg-name")
run(["git","-C",str(FIX),"config","user.email","fixture@example.invalid"],REPO,"cfg-email")
run(["git","-C",str(FIX),"config","commit.gpgsign","false"],REPO,"cfg-gpg")
run(["git","-C",str(FIX),"rev-parse","HEAD"],REPO,"head-pre")
# E copy from BOOT (untracked+ignored, excluding pycache)
def _lines(cwd,args):
    return subprocess.run(["git","--no-optional-locks"]+args,cwd=str(cwd),capture_output=True,text=True).stdout.splitlines()
untracked=[l[3:].strip().strip('"') for l in _lines(BOOT,["status","--porcelain=v1","--untracked-files=all"]) if l.startswith("?? ")]
ignored=[l.strip() for l in subprocess.run(["git","--no-optional-locks","ls-files","--others","--ignored","--exclude-standard"],cwd=str(BOOT),capture_output=True,text=True).stdout.splitlines() if l.strip()]
(EVID/"e-manifest-untracked.txt").write_text("\n".join(sorted(untracked))+"\n",encoding="utf-8")
(EVID/"e-manifest-ignored.txt").write_text("\n".join(sorted(ignored))+"\n",encoding="utf-8")
log(f"untracked={len(untracked)} ignored={len(ignored)}")
def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "MISSING"
rows=[]
for rel in sorted(set(untracked+ignored)):
    if "__pycache__" in Path(rel).parts or rel.endswith(".pyc"): continue
    rows.append(f"{_sha(BOOT/rel)}  {rel}")
(EVID/"e-hash-boot.txt").write_text("\n".join(rows)+"\n",encoding="utf-8")
copied=0
for rel in sorted(set(untracked+ignored)):
    if "__pycache__" in Path(rel).parts or rel.endswith(".pyc"): continue
    src=BOOT/rel; dst=FIX/rel
    if src.is_file():
        dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst); copied+=1
    elif src.is_dir():
        dst.mkdir(parents=True,exist_ok=True)
log(f"E copy copied={copied}")
ok=all(_sha(FIX/rel.split('  ',1)[1])==rel.split('  ',1)[0] for rel in rows)
# verify via loop (explicit)
ok=True
for r in rows:
    exp, rel = r.split("  ",1)
    if _sha(FIX/rel)!=exp:
        log(f"MISMATCH {rel}"); ok=False
(EVID/"e-hash-verify.txt").write_text("E_HASH_UNCHANGED\n" if ok else "E_HASH_MISMATCH\n",encoding="utf-8")
log(f"E_HASH_{'UNCHANGED' if ok else 'MISMATCH'}")
if not ok: log("FATAL E"); sys.exit(1)
# Overlay 736 INPUT exact
lst=[l.strip() for l in open(REPO/"notes/rephase-1-versioned-renewal-implementation/resume-20261025/final-integration-input-evidence-20261025T051343Z/dst-hash-intended-stdout.txt") if l.strip()]
log(f"INPUT {len(lst)}")
for line in lst:
    exp_sha, rel = line.split()[0], line.split()[2]
    src=SNAP/rel; dst=FIX/rel
    dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
# verify overlay
ok2=True
for line in lst:
    exp_sha, rel = line.split()[0], line.split()[2]
    if _sha(FIX/rel)!=exp_sha:
        log(f"OVERLAY MISMATCH {rel}"); ok2=False
log(f"OVERLAY_{'OK' if ok2 else 'MISMATCH'}")
if not ok2: sys.exit(1)
# Overlay P1 fix + new test (combined latest code, overwrites 736 P1)
for rel in ["scripts/survey_editorial_correction_proposal_v2.py","tests/test_editorial_renewal_p1_dispatch_20261025.py"]:
    shutil.copy2(CAND/rel, FIX/rel)
    log(f"fix overlay {rel} {_sha(FIX/rel)[:8]}")
run(["git","-C",str(FIX),"add","--"]+[l.split()[2] for l in lst]+["tests/test_editorial_renewal_p1_dispatch_20261025.py"],REPO,"add-736-fix",timeout=120)
run(["git","-C",str(FIX),"diff","--cached","--name-only"],REPO,"diff-cached",timeout=60)
run(["git","-C",str(FIX),"status","--porcelain=v1","--untracked-files=all"],REPO,"status-staged",timeout=60)
# Verify E still untracked (staged should be 736+1? Actually 736 list includes P1 (modified) + 15 new? Plus new test = 737? Let's just check overlap)
pstaged=subprocess.run(["git","--no-optional-locks","diff","--cached","--name-only"],cwd=str(FIX),capture_output=True,text=True).stdout.splitlines()
overlap=set(pstaged) & set([l[3:].strip().strip('"') for l in _lines(BOOT,["status","--porcelain=v1","--untracked-files=all"]) if l.startswith("?? ")])
log(f"staged={len(pstaged)} overlap_E={len(overlap)}")
if overlap: log(f"FATAL overlap {sorted(overlap)[:5]}"); sys.exit(1)
pcom=run(["git","-C",str(FIX),"commit","-m","TEST-ONLY: G1 base FIXED 736 + P1 renewal dispatch fix + dispatch unit (SOURCE-only, short-chain)"],REPO,"commit-g1",timeout=120)
if pcom is None or pcom.returncode!=0: log("FATAL commit"); sys.exit(1)
run(["git","-C",str(FIX),"rev-parse","HEAD"],REPO,"head-post",timeout=60)
run(["git","-C",str(FIX),"log","--oneline","-4"],REPO,"log-post",timeout=60)
new_head=subprocess.run(["git","-C",str(FIX),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
log(f"NEW_HEAD {new_head} FIX={FIX} EVID={EVID}")
print(f"FIX={FIX}")
print(f"EVID={EVID}")
print(f"NEW_HEAD={new_head}")
