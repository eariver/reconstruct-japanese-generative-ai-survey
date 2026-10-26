#!/bin/bash
# Affected-regressions TEST-ONLY complete SOURCE provision — 740 intended from archive INPUT
# Saved BEFORE execution via Write, no heredoc edits for procedures. No old runners, no network.
# Fail-closed: set -u only, explicit rc, stop before DST creation on pre-check failure.
# Purpose: guard complete exact SOURCE copy to NEW independent fixture DB with meaningful
# source commit BEFORE authority; never run partial candidate Git ls-files missing untracked.
set -u
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
SRC="$REPO/.rephase-1-editorial-runtime/versioned-renewal-archive-input-20261025T133248Z/snapshot-work"
CAND="$REPO/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
STAMP="20261025T140000Z"
PACKROOT="$REPO/.rephase-1-editorial-runtime/versioned-renewal-affected-regress-20261025T140000Z"
DST="$PACKROOT/test-source"
TMPLOCAL="$PACKROOT/tmp"
EVIDENCE="$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/affected-regressions"
export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C

mkdir -p "$EVIDENCE"
LOG="$EVIDENCE/commands.log"
printf "stamp %s\n" "$STAMP" > "$LOG"

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
[ -d "$CAND/.git" ] || fail "CAND .git missing"
[ -e "$PACKROOT" ] && fail "PACKROOT already exists, need fresh unique id"
[ -e "$DST" ] && fail "DST already exists"
mkdir -p "$TMPLOCAL" || fail "mkdir TMPLOCAL"
mkdir -p "$DST" || fail "mkdir DST early (for .git copy parent)"

run recon-head git -C "$REPO" --no-optional-locks rev-parse HEAD || fail "recon-head rc"
grep -q "^f84fcf5321be3798c862c0156278afbba01f89f6$" "$EVIDENCE/recon-head-stdout.txt" || fail "recon HEAD not f84fcf5"
run recon-status git -C "$REPO" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "recon-status rc"
run recon-diff-cached git -C "$REPO" --no-optional-locks diff --cached --name-only || fail "recon-diff-cached rc"
[ -s "$EVIDENCE/recon-diff-cached-stdout.txt" ] && fail "recon index not clean"

run src-head git -C "$SRC" --no-optional-locks rev-parse HEAD || fail "src-head rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/src-head-stdout.txt" || fail "SRC HEAD not 409"
run src-tree git -C "$SRC" --no-optional-locks rev-parse 'HEAD^{tree}' || fail "src-tree rc"
grep -q "^8ce3699861505f32d1d60bdc185d4d4f635aedb2$" "$EVIDENCE/src-tree-stdout.txt" || fail "SRC tree not 8ce"
run src-status git -C "$SRC" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "src-status rc"
run src-diff-cached git -C "$SRC" --no-optional-locks diff --cached --name-only || fail "src-diff-cached rc"
[ -s "$EVIDENCE/src-diff-cached-stdout.txt" ] && fail "SRC index not clean"
run src-count bash -c "find \"$SRC\" -path \"$SRC/.git\" -prune -o -type f -print | wc -l" || fail "src-count rc"
grep -q "740" "$EVIDENCE/src-count-stdout.txt" || fail "SRC worktree not 740"

run cand-head git -C "$CAND" --no-optional-locks rev-parse HEAD || fail "cand-head rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/cand-head-stdout.txt" || fail "CAND HEAD not 409"

run src-hash-intended python3 - "$SRC" <<'PYEOF'
import os, hashlib, sys
src=sys.argv[1]
files=[]
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
        data=open(full,'rb').read()
        files.append((rel,hashlib.sha256(data).hexdigest(),len(data)))
files.sort()
assert len(files)==740, f"intended {len(files)} !=740"
for rel,h,n in files:
    print(f"{h} {n} {rel}")
PYEOF
[ "$(cat "$EVIDENCE/src-hash-intended-exit.txt")" = "0" ] || fail "src-hash-intended failed"
run src-hash-sha sha256sum "$EVIDENCE/src-hash-intended-stdout.txt" || fail "src-hash-sha rc"
grep -q "^4e2783fb81514c2259192d1fde17dc36ebdc8332bf35123cabdeff494d7c910d" "$EVIDENCE/src-hash-sha-stdout.txt" || fail "SRC dst-hash-intended mismatch 4e27"

mkdir -p "$DST" || fail "mkdir DST"
mkdir -p "$TMPLOCAL" || fail "mkdir TMPLOCAL"
run cp-git cp -a "$SRC/.git" "$DST/.git" || fail "cp-git rc"
[ -d "$DST/.git" ] || fail "DST .git missing after cp"
run dst-git-count bash -c "find \"$DST/.git\" -type f | wc -l" || fail "dst-git-count rc"
grep -q "83" "$EVIDENCE/dst-git-count-stdout.txt" || fail "DST .git count not 83"
[ -e "$DST/.git/objects/info/alternates" ] && fail "DST alternates exists"
[ -e "$DST/.git/objects/info" ] && fail "DST objects/info exists"
run dst-head git -C "$DST" --no-optional-locks rev-parse HEAD || fail "dst-head rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/dst-head-stdout.txt" || fail "DST HEAD not 409 pre-populate"
run dst-gitdir git -C "$DST" --no-optional-locks rev-parse --absolute-git-dir || fail "dst-gitdir rc"
grep -q "versioned-renewal-affected-regress-20261025T140000Z/test-source/.git" "$EVIDENCE/dst-gitdir-stdout.txt" || fail "DST gitdir not own"
run dst-remote git -C "$DST" --no-optional-locks remote -v || fail "dst-remote rc"
grep -q "example.invalid" "$EVIDENCE/dst-remote-stdout.txt" || fail "DST remote not inert"
grep -q "github.com" "$EVIDENCE/dst-remote-stdout.txt" && fail "DST remote points to real origin"

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
        # verify bytes equal
        a=open(full,'rb').read()
        b=open(target,'rb').read()
        assert a==b, f"copy mismatch {rel}"
        assert hashlib.sha256(a).hexdigest()==hashlib.sha256(b).hexdigest()
        count+=1
assert count==740, f"populated {count} !=740"
print(f"populate OK {count}")
PYEOF
[ "$(cat "$EVIDENCE/populate-worktree-exit.txt")" = "0" ] || fail "populate-worktree failed"

run dst-count bash -c "find \"$DST\" -path \"$DST/.git\" -prune -o -type f -print | wc -l" || fail "dst-count rc"
grep -q "740" "$EVIDENCE/dst-count-stdout.txt" || fail "DST worktree not 740"
run dst-status git -C "$DST" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "dst-status rc"
run dst-diff-cached git -C "$DST" --no-optional-locks diff --cached --name-only || fail "dst-diff-cached rc"
[ -s "$EVIDENCE/dst-diff-cached-stdout.txt" ] && fail "DST index not clean pre-commit"

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
print(f"SRC==DST 740/740 SHA identical")
PYEOF
[ "$(cat "$EVIDENCE/dst-verify-sha-exit.txt")" = "0" ] || fail "dst-verify-sha failed"

run dst-pin-hashes python3 - "$DST" <<'PYEOF'
import hashlib, pathlib, sys
dst=pathlib.Path(sys.argv[1])
for rel in ["scripts/survey_versioned_renewal_history_v2.py","scripts/survey_editorial_correction_proposal_v2.py","scripts/survey_publication_v2.py","scripts/survey_versioned_renewal_source_v2.py","scripts/survey_versioned_renewal_v2.py","scripts/survey_reader_publication_v2.py","scripts/survey_editorial_publication_v2.py","tests/test_editorial_renewal_archive_correction_20261025.py"]:
    data=(dst/rel).read_bytes()
    print(f"{rel} {len(data)} {hashlib.sha256(data).hexdigest()}")
PYEOF
[ "$(cat "$EVIDENCE/dst-pin-hashes-exit.txt")" = "0" ] || fail "dst-pin-hashes failed"

run dst-isolation python3 - "$SRC" "$DST" <<'PYEOF'
import os, sys
src,dst=sys.argv[1],sys.argv[2]
def inodes(base, sub):
    out=set()
    target=os.path.join(base,sub)
    for root,dirs,files in os.walk(target):
        for n in dirs+files:
            try:
                st=os.stat(os.path.join(root,n))
                out.add((st.st_dev,st.st_ino))
            except FileNotFoundError:
                pass
    return out
src_git=inodes(src,".git"); dst_git=inodes(dst,".git")
assert not (src_git & dst_git), "git inode sharing"
src_w=set()
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
        st=os.stat(full)
        src_w.add((st.st_dev,st.st_ino))
dst_w=set()
for root,dirs,fnames in os.walk(dst):
    if '.git' in dirs:
        dirs.remove('.git')
    dirs[:]=[d for d in dirs if d!='__pycache__']
    for f in fnames:
        if f.endswith('.pyc'):
            continue
        full=os.path.join(root,f)
        if '/.git/' in full:
            continue
        st=os.stat(full)
        assert st.st_nlink==1, f"hardlink {full} nlink {st.st_nlink}"
        dst_w.add((st.st_dev,st.st_ino))
assert not (src_w & dst_w), "worktree inode sharing"
print(f"isolation OK git {len(src_git)}/{len(dst_git)} work {len(src_w)}/{len(dst_w)} nlink==1")
PYEOF
[ "$(cat "$EVIDENCE/dst-isolation-exit.txt")" = "0" ] || fail "dst-isolation failed"

run dst-noalternates bash -c "test ! -e \"$DST/.git/objects/info/alternates && test ! -e \"$DST/.git/objects/info\" && echo NOALTERNATES" || fail "dst-noalternates rc"
run dst-config git -C "$DST" --no-optional-locks config --list --show-origin || fail "dst-config rc"
run dst-env-check bash -c "env | grep -E '^GIT_(DIR|WORK_TREE|INDEX_FILE)=' && exit 1 || echo NO_INHERITED_GIT_DIR" || fail "dst-env-check rc"

# Meaningful SOURCE-only commit BEFORE authority (code SOURCE only, no E, no authority)
run dst-add git -C "$DST" --no-optional-locks add -A || fail "dst-add rc"
run dst-commit git -C "$DST" --no-optional-locks -c user.name=rephase-fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false commit -m "TEST-ONLY: complete 740 SOURCE (archive 740 + .latexmkrc + root recipe) before authority" || fail "dst-commit rc"
run dst-head-post git -C "$DST" --no-optional-locks rev-parse HEAD || fail "dst-head-post rc"
run dst-log-post git -C "$DST" --no-optional-locks log --oneline -3 || fail "dst-log-post rc"
run dst-status-post git -C "$DST" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "dst-status-post rc"
[ -s "$EVIDENCE/dst-status-post-stdout.txt" ] && fail "DST status not clean post-commit"
run dst-lsfiles git -C "$DST" --no-optional-locks ls-files || fail "dst-lsfiles rc"
run dst-lsfiles-count bash -c "git -C \"$DST\" --no-optional-locks ls-files | wc -l" || fail "dst-lsfiles-count rc"
grep -q "740" "$EVIDENCE/dst-lsfiles-count-stdout.txt" || fail "DST ls-files not 740 (must see all tracked for helpers)"

run src-head-post git -C "$SRC" --no-optional-locks rev-parse HEAD || fail "src-head-post rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/src-head-post-stdout.txt" || fail "SRC HEAD changed (must stay 409)"
run recon-head-post git -C "$REPO" --no-optional-locks rev-parse HEAD || fail "recon-head-post rc"
grep -q "^f84fcf5321be3798c862c0156278afbba01f89f6$" "$EVIDENCE/recon-head-post-stdout.txt" || fail "recon HEAD changed"

printf "DONE OK %s\n" "$STAMP" >> "$LOG"
