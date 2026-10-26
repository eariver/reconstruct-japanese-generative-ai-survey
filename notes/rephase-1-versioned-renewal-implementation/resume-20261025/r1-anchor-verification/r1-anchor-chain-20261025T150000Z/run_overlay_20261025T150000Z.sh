#!/bin/bash
# Overlay 740 archive INPUT onto anchor-weekly (OWN source commit, preserve E)
set -u
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
FIX="$REPO/.rephase-1-editorial-runtime/versioned-renewal-r1-anchor-20261025T150000Z/anchor-weekly"
SRC740="$REPO/.rephase-1-editorial-runtime/versioned-renewal-archive-input-20261025T133248Z/snapshot-work"
EVIDENCE="$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/r1-anchor-verification/r1-anchor-chain-20261025T150000Z"
export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C
LOG="$EVIDENCE/commands.log"
printf "run overlay 740 OWN source commit preserve E\n" >> "$LOG"

run() {
  tag="$1"; shift
  out="$EVIDENCE/${tag}-stdout.txt"
  err="$EVIDENCE/${tag}-stderr.txt"
  rcfile="$EVIDENCE/${tag}-exit.txt"
  env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0 PYTHONDONTWRITEBYTECODE=1 "$@" >"$out" 2>"$err"
  rc=$?
  printf "%s" "$rc" > "$rcfile"
  printf "run %s rc=%s cmd=%s\n" "$tag" "$rc" "$*" >> "$LOG"
  return $rc
}
fail() { printf "FAIL %s\n" "$1" >> "$LOG"; echo "FAIL: $1" >&2; exit 1; }

run overlay-pin-before git -C "$FIX" --no-optional-locks rev-parse HEAD || fail "pin-before"
run overlay-status-before git -C "$FIX" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "status-before"
run overlay-src-head git -C "$SRC740" --no-optional-locks rev-parse HEAD || fail "src-head"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/overlay-src-head-stdout.txt" || fail "SRC740 not 409"

# Copy 740 files (archive-exact, per-dir sorted double-space list ensures 740) via python (no rsync blind), preserve E (do NOT delete untracked edition).
run overlay-copy python3 - "$SRC740" "$FIX" <<'PYEOF'
import os, shutil, hashlib, sys
src,dst=sys.argv[1],sys.argv[2]
count=0
for root,dirs,files in os.walk(src):
    if '.git' in dirs: dirs.remove('.git')
    if '/.git/' in root or root.endswith('/.git'): continue
    if '.git' in root.split(os.sep): continue
    for f in sorted(files):
        full=os.path.join(root,f)
        if '/.git/' in full: continue
        rel=os.path.relpath(full,src)
        target=os.path.join(dst,rel)
        os.makedirs(os.path.dirname(target) or dst, exist_ok=True)
        shutil.copy2(full,target)
        assert hashlib.sha256(open(full,'rb').read()).hexdigest()==hashlib.sha256(open(target,'rb').read()).hexdigest()
        count+=1
assert count==740, f"overlay {count} !=740"
print(f"overlay OK {count}")
PYEOF
[ "$(cat "$EVIDENCE/overlay-copy-exit.txt")" = "0" ] || fail "overlay-copy"

run overlay-verify-740 python3 - "$SRC740" "$FIX" <<'PYEOF'
import os, hashlib, sys
src,dst=sys.argv[1],sys.argv[2]
def collect(base):
    out={}
    for r,d,fs in os.walk(base):
        if '.git' in d: d.remove('.git')
        if '/.git/' in r or r.endswith('/.git'): continue
        for f in sorted(fs):
            full=os.path.join(r,f)
            if '/.git/' in full: continue
            # only intended 740? For dst, E also present (93 untracked). Only check 740 subset via src list.
            rel=os.path.relpath(full, base)
            out[rel]=hashlib.sha256(open(full,'rb').read()).hexdigest()
    return out
# src 740
slist=[]
for r,d,fs in os.walk(src):
    if '.git' in d: d.remove('.git')
    for f in sorted(fs):
        full=os.path.join(r,f)
        if '/.git/' in full: continue
        slist.append(os.path.relpath(full,src))
assert len(slist)==740
for rel in slist:
    a=open(os.path.join(src,rel),'rb').read()
    b=open(os.path.join(dst,rel),'rb').read()
    assert a==b, f"mismatch {rel}"
print("SRC==DST 740 subset identical, E preserved (not checked)")
PYEOF
[ "$(cat "$EVIDENCE/overlay-verify-740-exit.txt")" = "0" ] || fail "overlay-verify"

# SOURCE-only commit (source paths only, E stays untracked). Build 740 list from SRC, git add -- those only.
run overlay-add python3 - "$SRC740" "$FIX" <<'PYEOF'
import os, subprocess, sys
src,dst=sys.argv[1],sys.argv[2]
rels=[]
for r,d,fs in os.walk(src):
    if '.git' in d: d.remove('.git')
    for f in sorted(fs):
        full=os.path.join(r,f)
        if '/.git/' in full: continue
        rels.append(os.path.relpath(full,src))
assert len(rels)==740
# git add -- 740 paths only (preserve E untracked)
env={k:v for k,v in os.environ.items() if not k.startswith("GIT_")}
env.update({"GIT_NO_LAZY_FETCH":"1","GIT_OPTIONAL_LOCKS":"0","GIT_ALLOW_PROTOCOL":"file"})
proc=subprocess.run(["git","--no-optional-locks","add","--",*rels], cwd=dst, capture_output=True, text=True, timeout=120, env=env)
print(proc.stdout); print(proc.stderr, file=sys.stderr)
assert proc.returncode==0, f"git add failed {proc.stderr[:2000]}"
print(f"add OK 740 paths")
PYEOF
[ "$(cat "$EVIDENCE/overlay-add-exit.txt")" = "0" ] || fail "overlay-add"

run overlay-status-staged git -C "$FIX" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "status-staged"
run overlay-diff-cached git -C "$FIX" --no-optional-locks diff --cached --name-only || fail "diff-cached"
run overlay-commit git -C "$FIX" --no-optional-locks -c user.name=rephase-r1-anchor -c user.email=r1-anchor@example.invalid -c commit.gpgsign=false commit -m "TEST-ONLY: overlay 740 SOURCE (archive 740 + P3S fix if needed) before renewal U, E preserved" || fail "commit"
run overlay-head-post git -C "$FIX" --no-optional-locks rev-parse HEAD || fail "head-post"
run overlay-status-post git -C "$FIX" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "status-post"
# E must still be untracked (93+? includes r1/r2/r3 + editorial files), tracked clean for source
run overlay-lsfiles-subset python3 - "$SRC740" "$FIX" <<'PYEOF'
import os, subprocess, sys
src,dst=sys.argv[1],sys.argv[2]
rels=[]
for r,d,fs in os.walk(src):
    if '.git' in d: d.remove('.git')
    for f in sorted(fs):
        full=os.path.join(r,f)
        if '/.git/' in full: continue
        rels.append(os.path.relpath(full,src))
import subprocess as sp
ls=sp.run(["git","-C",dst,"--no-optional-locks","ls-files"], capture_output=True, text=True).stdout.splitlines()
s=set(ls)
missing=[p for p in rels if p not in s]
assert not missing, f"missing {len(missing)} {missing[:5]}"
print(f"SUBSET OK 740 tracked, total ls-files {len(ls)}")
# E preserved untracked?
st=sp.run(["git","-C",dst,"--no-optional-locks","status","--porcelain=v1","--untracked-files=all"], capture_output=True, text=True).stdout
assert "??" in st, "E must remain untracked"
print(f"E preserved, status lines {len(st.splitlines())}")
PYEOF
[ "$(cat "$EVIDENCE/overlay-lsfiles-subset-exit.txt")" = "0" ] || fail "lsfiles-subset"
printf "DONE overlay 740 OWN commit E preserved\n" >> "$LOG"
