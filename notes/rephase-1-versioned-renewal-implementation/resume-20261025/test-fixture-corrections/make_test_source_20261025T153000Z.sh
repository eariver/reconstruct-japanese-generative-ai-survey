#!/bin/bash
# TEST-ONLY complete SOURCE provision for fixture corrections — 740 intended from archive INPUT
# Saved via Write before execution. No old runners, no network. Fail-closed: set -u only, explicit rc.
set -u
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
SRC="$REPO/.rephase-1-editorial-runtime/versioned-renewal-archive-input-20261025T133248Z/snapshot-work"
STAMP="20261025T153000Z"
PACKROOT="$REPO/.rephase-1-editorial-runtime/versioned-renewal-test-fixture-corrections-20261025T153000Z"
DST="$PACKROOT/test-source"
TMPLOCAL="$PACKROOT/tmp"
EVIDENCE="$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/test-fixture-corrections"
export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C

LOG="$EVIDENCE/commands.log"
printf "stamp %s TEST-ONLY fixture corrections base\n" "$STAMP" > "$LOG"

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
[ -e "$PACKROOT" ] && fail "PACKROOT already exists, need fresh unique id"
[ -e "$DST" ] && fail "DST already exists"
mkdir -p "$EVIDENCE" || fail "mkdir EVIDENCE"
mkdir -p "$TMPLOCAL" || fail "mkdir TMPLOCAL"
mkdir -p "$DST" || fail "mkdir DST"

run recon-head git -C "$REPO" --no-optional-locks rev-parse HEAD || fail "recon-head rc"
run recon-status git -C "$REPO" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "recon-status rc"
run recon-diff-cached git -C "$REPO" --no-optional-locks diff --cached --name-only || fail "recon-diff-cached rc"

run src-head git -C "$SRC" --no-optional-locks rev-parse HEAD || fail "src-head rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/src-head-stdout.txt" || fail "SRC HEAD not 409"
run src-tree git -C "$SRC" --no-optional-locks rev-parse 'HEAD^{tree}' || fail "src-tree rc"
run src-count bash -c "find \"$SRC\" -path \"$SRC/.git\" -prune -o -type f -print | wc -l" || fail "src-count rc"

run cp-git cp -a "$SRC/.git" "$DST/.git" || fail "cp-git rc"
[ -d "$DST/.git" ] || fail "DST .git missing after cp"
run dst-head git -C "$DST" --no-optional-locks rev-parse HEAD || fail "dst-head rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/dst-head-stdout.txt" || fail "DST HEAD not 409 pre-populate"

run populate-worktree python3 - "$SRC" "$DST" <<'PYEOF'
import os, shutil, hashlib, sys
src,dst=sys.argv[1],sys.argv[2]
count=0
for root,dirs,fnames in os.walk(src):
    if '.git' in dirs:
        dirs.remove('.git')
    dirs[:]=[d for d in dirs if d!='__pycache__']
    for f in fnames:
        if f.endswith('.pyc'):
            continue
        full=os.path.join(root,f)
        if '/.git/' in full:
            continue
        rel=os.path.relpath(full,src)
        target=os.path.join(dst,rel)
        os.makedirs(os.path.dirname(target) or dst, exist_ok=True)
        shutil.copy2(full,target)
        a=open(full,'rb').read()
        b=open(target,'rb').read()
        assert a==b, f"copy mismatch {rel}"
        assert hashlib.sha256(a).hexdigest()==hashlib.sha256(b).hexdigest()
        count+=1
print(f"populate OK {count}")
PYEOF
[ "$(cat "$EVIDENCE/populate-worktree-exit.txt")" = "0" ] || fail "populate-worktree failed"

run dst-count bash -c "find \"$DST\" -path \"$DST/.git\" -prune -o -type f -print | wc -l" || fail "dst-count rc"
run dst-verify-sha python3 - "$SRC" "$DST" <<'PYEOF'
import os, hashlib, sys
src,dst=sys.argv[1],sys.argv[2]
def collect(base):
    out={}
    for root,dirs,fnames in os.walk(base):
        if '.git' in dirs:
            dirs.remove('.git')
        dirs[:]=[d for d in dirs if d!='__pycache__']
        for f in fnames:
            if f.endswith('.pyc'):
                continue
            full=os.path.join(root,f)
            if '/.git/' in full:
                continue
            rel=os.path.relpath(full,base)
            out[rel]=hashlib.sha256(open(full,'rb').read()).hexdigest()
    return out
a=collect(src); b=collect(dst)
assert set(a)==set(b), f"sets differ {len(a)} vs {len(b)}"
mismatch=[k for k in a if a[k]!=b[k]]
assert not mismatch, f"mismatch {mismatch[:5]}"
print(f"SRC==DST {len(a)}/{len(b)} SHA identical")
PYEOF
[ "$(cat "$EVIDENCE/dst-verify-sha-exit.txt")" = "0" ] || fail "dst-verify-sha failed"

run dst-pin-before python3 - "$DST" <<'PYEOF'
import hashlib, pathlib, sys
dst=pathlib.Path(sys.argv[1])
for rel in ["scripts/survey_versioned_renewal_history_v2.py","scripts/survey_editorial_correction_proposal_v2.py","scripts/survey_publication_v2.py","scripts/survey_versioned_renewal_source_v2.py","scripts/survey_versioned_renewal_v2.py","scripts/survey_reader_publication_v2.py","scripts/survey_editorial_publication_v2.py","tests/test_editorial_renewal_archive_correction_20261025.py",".latexmkrc"]:
    data=(dst/rel).read_bytes()
    print(f"{rel} {len(data)} {hashlib.sha256(data).hexdigest()}")
PYEOF
[ "$(cat "$EVIDENCE/dst-pin-before-exit.txt")" = "0" ] || fail "dst-pin-before failed"

echo "BASE READY DST=$DST"
