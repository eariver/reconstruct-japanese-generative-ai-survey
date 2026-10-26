#!/bin/bash
# R1-anchor NEW 721 DB clone — complete 721 + .latexmkrc, no E, meaningful HEAD 721a04d
# Saved BEFORE execution via Write. No old runners, no network. Fail-closed set -u.
set -u
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
SRC="$REPO/.rephase-1-editorial-runtime/jgas-editorial-r7b-20261023T034500Z/candidate-partial-b40de60"
R7BMANIFEST="$REPO/notes/rephase-1-editorial-operation-implementation/correction-r7/source-manifest-r7b.json"
STAMP="20261025T150000Z"
PACKROOT="$REPO/.rephase-1-editorial-runtime/versioned-renewal-r1-anchor-20261025T150000Z"
DST="$PACKROOT/anchor-weekly"
TMPLOCAL="$PACKROOT/tmp"
EVIDENCE="$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/r1-anchor-verification/r1-anchor-chain-20261025T150000Z"
export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C

mkdir -p "$EVIDENCE"
LOG="$EVIDENCE/commands.log"
printf "stamp %s R1-anchor 721 clone\n" "$STAMP" > "$LOG"

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

fail() {
  printf "FAIL %s\n" "$1" >> "$LOG"
  echo "FAIL: $1" >&2
  exit 1
}

[ -d "$SRC/.git" ] || fail "SRC .git missing"
[ -f "$R7BMANIFEST" ] || fail "R7B manifest missing"
[ -e "$PACKROOT" ] && fail "PACKROOT exists, need fresh id"
[ -e "$DST" ] && fail "DST exists"
mkdir -p "$TMPLOCAL" || fail "mkdir TMPLOCAL"
mkdir -p "$DST" || fail "mkdir DST"

run recon-head git -C "$REPO" --no-optional-locks rev-parse HEAD || fail "recon-head"
grep -q "^f84fcf5321be3798c862c0156278afbba01f89f6$" "$EVIDENCE/recon-head-stdout.txt" || fail "recon HEAD not f84fcf5"
run src-head git -C "$SRC" --no-optional-locks rev-parse HEAD || fail "src-head"
grep -q "^721a04d85532d7855f3e54cc411f5847c787726e$" "$EVIDENCE/src-head-stdout.txt" || fail "SRC not 721a04d"
run src-tree git -C "$SRC" --no-optional-locks rev-parse 'HEAD^{tree}' || fail "src-tree"
grep -q "^ac7cb0bd2e977b46e957450816eddd779799e144$" "$EVIDENCE/src-tree-stdout.txt" || fail "SRC tree not ac7cb0bd"

run cp-git cp -a "$SRC/.git" "$DST/.git" || fail "cp-git"
run dst-git-count bash -c "find \"$DST/.git\" -type f | wc -l" || fail "dst-git-count"
run dst-head git -C "$DST" --no-optional-locks rev-parse HEAD || fail "dst-head"
grep -q "^721a04d85532d7855f3e54cc411f5847c787726e$" "$EVIDENCE/dst-head-stdout.txt" || fail "DST HEAD not 721a04d"
run dst-gitdir git -C "$DST" --no-optional-locks rev-parse --absolute-git-dir || fail "dst-gitdir"
grep -q "versioned-renewal-r1-anchor-20261025T150000Z/anchor-weekly/.git" "$EVIDENCE/dst-gitdir-stdout.txt" || fail "DST gitdir not own"
run dst-remote git -C "$DST" --no-optional-locks remote -v || fail "dst-remote"
grep -q "example.invalid" "$EVIDENCE/dst-remote-stdout.txt" || fail "DST remote not inert"

run populate-721 python3 - "$SRC" "$DST" "$R7BMANIFEST" <<'PYEOF'
import json, os, shutil, hashlib, sys
src,dst,man=sys.argv[1],sys.argv[2],sys.argv[3]
m=json.load(open(man))
assert m['count']==721
for e in m['files']:
    p=e['path']
    s=os.path.join(src,p)
    assert os.path.isfile(s), f"missing {p} in SRC"
    t=os.path.join(dst,p)
    os.makedirs(os.path.dirname(t) or dst, exist_ok=True)
    shutil.copy2(s,t)
    assert hashlib.sha256(open(s,'rb').read()).hexdigest()==e['sha256']
    assert hashlib.sha256(open(t,'rb').read()).hexdigest()==e['sha256']
print("populate 721 OK")
# verify .latexmkrc present
assert os.path.isfile(os.path.join(dst,".latexmkrc"))
print(".latexmkrc present")
PYEOF
[ "$(cat "$EVIDENCE/populate-721-exit.txt")" = "0" ] || fail "populate-721"

run dst-count bash -c "find \"$DST\" -path \"$DST/.git\" -prune -o -type f -print | wc -l" || fail "dst-count"
grep -q "721" "$EVIDENCE/dst-count-stdout.txt" || fail "DST not 721 files"
run dst-status git -C "$DST" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "dst-status"
# Allow only pycache untracked (4 pyc from SRC?) — we excluded pyc via manifest, so status should be clean (no pyc copied). Check.
cat "$EVIDENCE/dst-status-stdout.txt"
run dst-isolation python3 - "$SRC" "$DST" <<'PYEOF'
import os, sys
src,dst=sys.argv[1],sys.argv[2]
def inodes(base):
    out=set()
    for r,d,f in os.walk(os.path.join(base,".git")):
        for n in d+f:
            try: out.add(os.stat(os.path.join(r,n)).st_ino)
            except: pass
    return out
assert not (inodes(src) & inodes(dst)), "git inode sharing"
print("isolation git OK")
# worktree nlink==1
for r,d,fs in os.walk(dst):
    if '.git' in r: continue
    for fn in fs:
        fp=os.path.join(r,fn)
        if '/.git/' in fp: continue
        assert os.stat(fp).st_nlink==1
print("nlink OK")
PYEOF
[ "$(cat "$EVIDENCE/dst-isolation-exit.txt")" = "0" ] || fail "isolation"

run dst-noalternates bash -c "test ! -e \"$DST/.git/objects/info/alternates\" && echo NOALT" || fail "noalternates"
# Note: R7b .git has no shallow, no objects/info? Check.
run dst-config git -C "$DST" --no-optional-locks config --list --show-origin || fail "config"
run dst-env-check bash -c "env | grep -E '^GIT_(DIR|WORK_TREE|INDEX_FILE)=' && exit 1 || echo NO_INHERIT" || fail "env-check"

printf "DONE OK %s 721 clone\n" "$STAMP" >> "$LOG"
