#!/bin/bash
# Source-complete immutable-for-review snapshot — CURRENT candidate freeze for parallel review/test (retry with corrected recon check)
# Prior 174224Z FAILED only on overly strict recon-status clean check (parallel packet untracked files mistaken for dirt).
# This retry uses fresh unique id 174422Z, same safe method, corrected recon check: HEAD unchanged + no staged + no tracked mods, untracked allowed (parallel workers).
# Author-side Co-Worker, NO implementation edits/tests/build/project imports/network/ordinary candidate or reconstruct commit.
# Source FROZEN: root no authors writing during round. Documentation/source inspection only.
# Saved BEFORE execution via dedicated editor (Write). No old runners. Fail-closed: set -u only, explicit rc, no overwrite/deletion.
set -u
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
SRC="$REPO/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
REJECTED="$REPO/.rephase-1-editorial-runtime/versioned-renewal-impl-20261023T181352Z/candidate-work"
MANIFEST_COMPLETE="$REPO/notes/rephase-1-editorial-operation-implementation/source-packaging/complete-r3-operation-manifest.json"
MANIFEST_R7B="$REPO/notes/rephase-1-editorial-operation-implementation/correction-r7/source-manifest-r7b.json"
STAMP="20261024T174422Z"
FREEZE_PARENT="$REPO/.rephase-1-editorial-runtime/versioned-renewal-freeze-20261024T174422Z"
DST="$FREEZE_PARENT/snapshot-work"
PACKET_DIR="$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025"
EVIDENCE="$PACKET_DIR/source-freeze-evidence-20261024T174422Z"
export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C

mkdir -p "$EVIDENCE"
LOG="$EVIDENCE/commands.log"
printf "stamp %s (retry after 174224Z strict-recon FAIL preserved)\n" "$STAMP" > "$LOG"

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
[ -f "$MANIFEST_COMPLETE" ] || fail "complete manifest missing"
[ -f "$MANIFEST_R7B" ] || fail "r7b manifest missing"
[ -d "$REJECTED/.git" ] || fail "rejected M1 missing (must preserve, not modify)"
[ -d "$REPO/.rephase-1-editorial-runtime" ] || fail "ignored runtime parent missing"
[ -e "$FREEZE_PARENT" ] && fail "FREEZE_PARENT already exists, need fresh unique id (no overwrite)"
[ -e "$DST" ] && fail "DST already exists (no overwrite)"

run recon-head git -C "$REPO" --no-optional-locks rev-parse HEAD || fail "recon-head rc"
grep -q "^f84fcf5321be3798c862c0156278afbba01f89f6$" "$EVIDENCE/recon-head-stdout.txt" || fail "recon HEAD not f84fcf5 (HumanHEAD)"
run recon-status git -C "$REPO" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "recon-status rc"
run recon-diff-cached git -C "$REPO" --no-optional-locks diff --cached --name-only || fail "recon-diff-cached rc"
[ -s "$EVIDENCE/recon-diff-cached-stdout.txt" ] && fail "recon index not clean (staged changes forbidden)"
run recon-diff-head git -C "$REPO" --no-optional-locks diff HEAD --name-only || fail "recon-diff-head rc"
[ -s "$EVIDENCE/recon-diff-head-stdout.txt" ] && fail "recon tracked modifications present (must be clean HEAD, untracked only)"
run recon-status-untracked-only python3 - "$EVIDENCE/recon-status-stdout.txt" <<'PYEOF'
import sys
p=sys.argv[1]
lines=[l.rstrip('\n') for l in open(p) if l.strip()!='']
for l in lines:
    assert l.startswith('?? '), f"tracked change forbidden in recon (parallel untracked only): {l}"
print(f"recon untracked-only OK {len(lines)} untracked (parallel packet allowed, no tracked mods)")
PYEOF
[ "$(cat "$EVIDENCE/recon-status-untracked-only-exit.txt")" = "0" ] || fail "recon untracked-only check failed"

run rejected-head git -C "$REJECTED" --no-optional-locks rev-parse HEAD || fail "rejected-head rc"
grep -q "^a8890d4ff612563e71b7dcf5db76287acfe4ea35$" "$EVIDENCE/rejected-head-stdout.txt" || fail "rejected HEAD changed (must stay a8890d4)"
run rejected-log git -C "$REJECTED" --no-optional-locks log --oneline -3 || fail "rejected-log rc"
run rejected-status git -C "$REJECTED" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "rejected-status rc"
[ -s "$EVIDENCE/rejected-status-stdout.txt" ] && fail "rejected M1 status not clean (must preserve untouched)"

run src-head git -C "$SRC" --no-optional-locks rev-parse HEAD || fail "src-head rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/src-head-stdout.txt" || fail "SRC HEAD not actual409"
run src-tree git -C "$SRC" --no-optional-locks rev-parse 'HEAD^{tree}' || fail "src-tree rc"
grep -q "^8ce3699861505f32d1d60bdc185d4d4f635aedb2$" "$EVIDENCE/src-tree-stdout.txt" || fail "SRC tree not 8ce"
run src-log git -C "$SRC" --no-optional-locks log --oneline -3 || fail "src-log rc"
run src-status git -C "$SRC" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "src-status rc"
run src-diff-cached git -C "$SRC" --no-optional-locks diff --cached --name-only || fail "src-diff-cached rc"
[ -s "$EVIDENCE/src-diff-cached-stdout.txt" ] && fail "SRC index not clean (diff --cached must be empty)"
run src-diff-names git -C "$SRC" --no-optional-locks diff HEAD --name-only || fail "src-diff-names rc"
run src-others git -C "$SRC" --no-optional-locks ls-files --others --exclude-standard || fail "src-others rc"
run src-count bash -c "find \"$SRC\" -path \"$SRC/.git\" -prune -o -type f -print | wc -l" || fail "src-count rc"
grep -q "731" "$EVIDENCE/src-count-stdout.txt" || fail "SRC worktree count not 731"
run src-git-count bash -c "find \"$SRC/.git\" -type f | wc -l" || fail "src-git-count rc"
grep -q "83" "$EVIDENCE/src-git-count-stdout.txt" || fail "SRC .git file count not 83"
[ -e "$SRC/.git/objects/info/alternates" ] && fail "SRC alternates exists (must be absent)"
[ -e "$SRC/.git/objects/info" ] && fail "SRC objects/info exists (must match absence)"
run src-remote git -C "$SRC" --no-optional-locks remote -v || fail "src-remote rc"
grep -q "example.invalid" "$EVIDENCE/src-remote-stdout.txt" || fail "SRC remote not inert"
grep -q "github.com" "$EVIDENCE/src-remote-stdout.txt" && fail "SRC remote points to real origin"
run src-shallow cat "$SRC/.git/shallow" || fail "src-shallow rc"
grep -q "^774dd39a951c9ac3818e83dfffd4c7666efb0a20$" "$EVIDENCE/src-shallow-stdout.txt" || fail "SRC shallow not 774"
run src-pycache bash -c "find \"$SRC\" -path \"$SRC/.git\" -prune -o \\( -name __pycache__ -o -name '*.pyc' \\) -print | wc -l" || fail "src-pycache rc"
grep -q "0" "$EVIDENCE/src-pycache-stdout.txt" || fail "SRC has pycache residue (must be 0 in current worktree)"

run src-intended-verify python3 - "$SRC" "$MANIFEST_R7B" "$MANIFEST_COMPLETE" <<'PYEOF'
import json, os, sys, hashlib, ast, subprocess
src, r7b_path, comp_path = sys.argv[1], sys.argv[2], sys.argv[3]
r7b=json.load(open(r7b_path))
comp=json.load(open(comp_path))
assert r7b['count']==721 and len(r7b['files'])==721, "r7b 721"
assert comp['delta_count']==57 and len(comp['files'])==57, "base57 57"
assert comp['tracked_modified']==25 and comp['untracked_new']==32, "base57 partition"
r7b_paths=set(x['path'] for x in r7b['files'])
rel=[]
for root,dirs,files in os.walk(src):
    if '.git' in dirs:
        dirs.remove('.git')
    if '/.git/' in root or root.endswith('/.git'):
        continue
    parts=root.split(os.sep)
    if '.git' in parts:
        continue
    for f in files:
        full=os.path.join(root,f)
        if '/.git/' in full:
            continue
        rel.append(os.path.relpath(full, src))
cur=set(rel)
assert len(cur)==731, f"cur {len(cur)} !=731"
missing=r7b_paths-cur
assert len(missing)==0, f"R7b missing {sorted(missing)[:5]}"
extra=sorted(cur-r7b_paths)
expected_extra=sorted([
 "schemas/versioned-renewal-basis-v2.schema.json",
 "schemas/versioned-renewal-publication-set-v2.schema.json",
 "schemas/versioned-renewal-source-manifest-v2.schema.json",
 "schemas/versioned-renewal-source-proof-v2.schema.json",
 "scripts/survey_versioned_renewal_history_v2.py",
 "scripts/survey_versioned_renewal_source_v2.py",
 "scripts/survey_versioned_renewal_v2.py",
 "tests/test_versioned_renewal_high_phase.py",
 "tests/test_versioned_renewal_history_phase_h.py",
 "tests/test_versioned_renewal_source_phase_s.py",
])
assert extra==expected_extra, f"extra mismatch {extra}"
env={**os.environ, 'GIT_NO_LAZY_FETCH':'1','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_OPTIONAL_LOCKS':'0'}
for k in ['GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE']:
    env.pop(k,None)
out=subprocess.check_output(['git','--no-optional-locks','status','--porcelain=v1','--untracked-files=all'], cwd=src, env=env).decode()
lines=[l for l in out.splitlines() if l.strip()]
mods=sorted([l[3:] for l in lines if l.startswith(' M ')])
adds=sorted([l[3:] for l in lines if l.startswith('?? ')])
assert len(mods)==39 and len(adds)==42, f"status {len(mods)}M {len(adds)}U"
comp_m=sorted([p for p,m in comp['files'].items() if m['git_status']=='M'])
comp_a=sorted([p for p,m in comp['files'].items() if m['git_status']=='A'])
assert set(comp_m).issubset(set(mods)), "baseline25 M not subset of current39 M"
assert set(comp_a).issubset(set(adds)), "baseline32 A not subset of current42 U"
assert set(expected_extra).issubset(set(adds)), "renewal10 not subset of U"
for p in adds:
    assert p.endswith('.py') or p.endswith('.json'), f"untracked non-source {p}"
    assert '__pycache__' not in p and not p.endswith('.pyc'), f"cache in untracked {p}"
for p in adds:
    if p.startswith('schemas/') and p.endswith('.json'):
        json.load(open(os.path.join(src,p)))
    if p.endswith('.py'):
        ast.parse(open(os.path.join(src,p)).read())
for p in expected_extra:
    fp=os.path.join(src,p)
    assert os.path.isfile(fp), f"renewal missing {p}"
print(f"src-intended-verify OK 731=R7b721+10renewal 39M42U baseline25+32 subset no-blind-cache JSON+AST OK")
PYEOF
[ "$(cat "$EVIDENCE/src-intended-verify-exit.txt")" = "0" ] || fail "src-intended-verify failed"

run src-ls-files-s git -C "$SRC" --no-optional-locks ls-files -s || fail "src-ls-files-s rc"
run src-hash-everything python3 - "$SRC" <<'PYEOF'
import os, hashlib, sys
src=sys.argv[1]
for root,dirs,files in os.walk(src):
    if '.git' in dirs:
        dirs.remove('.git')
    if '/.git/' in root or root.endswith('/.git'):
        continue
    if '.git' in root.split(os.sep):
        continue
    for f in sorted(files):
        full=os.path.join(root,f)
        if '/.git/' in full:
            continue
        rel=os.path.relpath(full, src)
        data=open(full,'rb').read()
        print(f"{hashlib.sha256(data).hexdigest()}  {len(data)}  {rel}")
PYEOF
[ "$(cat "$EVIDENCE/src-hash-everything-exit.txt")" = "0" ] || fail "src-hash pre failed"

mkdir -p "$FREEZE_PARENT" || fail "mkdir FREEZE_PARENT"
[ -d "$FREEZE_PARENT" ] || fail "FREEZE_PARENT missing after mkdir"
run mkdir-freeze mkdir -p "$DST" || fail "mkdir DST rc"
run cp-git cp -a "$SRC/.git" "$DST/.git" || fail "cp-git rc"
[ -d "$DST/.git" ] || fail "DST .git missing after cp"
run dst-git-count bash -c "find \"$DST/.git\" -type f | wc -l" || fail "dst-git-count rc"
grep -q "83" "$EVIDENCE/dst-git-count-stdout.txt" || fail "DST .git file count not 83"
[ -e "$DST/.git/objects/info/alternates" ] && fail "DST alternates exists (must be absent)"
[ -e "$DST/.git/objects/info" ] && fail "DST objects/info exists (must match SRC absence)"
run dst-head git -C "$DST" --no-optional-locks rev-parse HEAD || fail "dst-head rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/dst-head-stdout.txt" || fail "DST HEAD not 409"
run dst-tree git -C "$DST" --no-optional-locks rev-parse 'HEAD^{tree}' || fail "dst-tree rc"
grep -q "^8ce3699861505f32d1d60bdc185d4d4f635aedb2$" "$EVIDENCE/dst-tree-stdout.txt" || fail "DST tree not 8ce"
run dst-gitdir git -C "$DST" --no-optional-locks rev-parse --absolute-git-dir || fail "dst-gitdir rc"
grep -q "versioned-renewal-freeze-20261024T174422Z/snapshot-work/.git" "$EVIDENCE/dst-gitdir-stdout.txt" || fail "DST gitdir not own"
run dst-remote git -C "$DST" --no-optional-locks remote -v || fail "dst-remote rc"
grep -q "example.invalid" "$EVIDENCE/dst-remote-stdout.txt" || fail "DST remote not inert"
grep -q "github.com" "$EVIDENCE/dst-remote-stdout.txt" && fail "DST remote points to real origin"
run dst-log git -C "$DST" --no-optional-locks log --oneline -3 || fail "dst-log rc"
grep -q "^409b292" "$EVIDENCE/dst-log-stdout.txt" || fail "DST log not real409 ancestry (no fake-root)"

run populate-snapshot python3 - "$SRC" "$DST" "$MANIFEST_R7B" <<'PYEOF'
import json, os, shutil, hashlib, sys
src, dst, manifest_path = sys.argv[1], sys.argv[2], sys.argv[3]
m=json.load(open(manifest_path))
r7b_paths=[x['path'] for x in m['files']]
extra=[
 "schemas/versioned-renewal-basis-v2.schema.json",
 "schemas/versioned-renewal-publication-set-v2.schema.json",
 "schemas/versioned-renewal-source-manifest-v2.schema.json",
 "schemas/versioned-renewal-source-proof-v2.schema.json",
 "scripts/survey_versioned_renewal_history_v2.py",
 "scripts/survey_versioned_renewal_source_v2.py",
 "scripts/survey_versioned_renewal_v2.py",
 "tests/test_versioned_renewal_high_phase.py",
 "tests/test_versioned_renewal_history_phase_h.py",
 "tests/test_versioned_renewal_source_phase_s.py",
]
intended=r7b_paths+extra
assert len(intended)==731, "intended 731"
for p in intended:
    s=os.path.join(src,p)
    d=os.path.join(dst,p)
    assert os.path.isfile(s), f"src missing {p}"
    parent=os.path.dirname(d)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)
    shutil.copy2(s,d)
    assert open(s,'rb').read()==open(d,'rb').read(), f"copy mismatch {p}"
print(f"populate OK {len(intended)} files via manifest-exact copy2 (no rsync blind)")
PYEOF
[ "$(cat "$EVIDENCE/populate-snapshot-exit.txt")" = "0" ] || fail "populate-snapshot failed"

run dst-count bash -c "find \"$DST\" -path \"$DST/.git\" -prune -o -type f -print | wc -l" || fail "dst-count rc"
grep -q "731" "$EVIDENCE/dst-count-stdout.txt" || fail "DST worktree count not 731"
run dst-status git -C "$DST" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "dst-status rc"
run dst-diff-names git -C "$DST" --no-optional-locks diff HEAD --name-only || fail "dst-diff-names rc"
run dst-diff-cached git -C "$DST" --no-optional-locks diff --cached --name-only || fail "dst-diff-cached rc"
[ -s "$EVIDENCE/dst-diff-cached-stdout.txt" ] && fail "DST index not clean"
run dst-others git -C "$DST" --no-optional-locks ls-files --others --exclude-standard || fail "dst-others rc"

run dst-manifest-verify python3 - "$SRC" "$DST" "$MANIFEST_R7B" "$MANIFEST_COMPLETE" <<'PYEOF'
import json, hashlib, os, sys, subprocess
src, dst, r7b_path, comp_path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
r7b=json.load(open(r7b_path))
comp=json.load(open(comp_path))
env={**os.environ, 'GIT_NO_LAZY_FETCH':'1','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_OPTIONAL_LOCKS':'0'}
for k in ['GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE']:
    env.pop(k,None)
def porcelain(cwd):
    out=subprocess.check_output(['git','--no-optional-locks','status','--porcelain=v1','--untracked-files=all'], cwd=cwd, env=env).decode()
    lines=[l for l in out.splitlines() if l.strip()]
    mods=sorted([l[3:] for l in lines if l.startswith(' M ')])
    adds=sorted([l[3:] for l in lines if l.startswith('?? ')])
    return mods, adds
src_m, src_u=porcelain(src)
dst_m, dst_u=porcelain(dst)
assert src_m==dst_m and src_u==dst_u, f"SRC/DST status mismatch"
assert len(dst_m)==39 and len(dst_u)==42, f"dst {len(dst_m)}M {len(dst_u)}U"
for root,dirs,files in os.walk(src):
    if '.git' in dirs:
        dirs.remove('.git')
    if '/.git/' in root or root.endswith('/.git'):
        continue
    if '.git' in root.split(os.sep):
        continue
    for f in files:
        full=os.path.join(root,f)
        if '/.git/' in full:
            continue
        rel=os.path.relpath(full, src)
        a=open(full,'rb').read()
        b=open(os.path.join(dst,rel),'rb').read()
        assert a==b, f"SRC/DST bytes differ {rel}"
        assert hashlib.sha256(a).hexdigest()==hashlib.sha256(b).hexdigest(), f"sha {rel}"
print(f"dst-manifest-verify OK SRC==DST 39M42U 731/731 bytes identical")
PYEOF
[ "$(cat "$EVIDENCE/dst-manifest-verify-exit.txt")" = "0" ] || fail "dst-manifest-verify failed"

run isolation-check python3 - "$SRC" "$DST" <<'PYEOF'
import os, sys
src, dst = sys.argv[1], sys.argv[2]
def walk_git_inodes(root):
    s=set()
    for r,dirs,files in os.walk(os.path.join(root,'.git')):
        for f in files:
            full=os.path.join(r,f)
            try:
                st=os.stat(full)
                s.add((st.st_dev, st.st_ino))
            except FileNotFoundError:
                pass
    return s
src_inodes=walk_git_inodes(src)
dst_inodes=walk_git_inodes(dst)
assert len(src_inodes)>0 and len(dst_inodes)>0, "empty git inodes"
assert src_inodes.isdisjoint(dst_inodes), "git inode collision (hardlink/share)"
def work_files(root):
    out={}
    for r,dirs,files in os.walk(root):
        if '.git' in dirs:
            dirs.remove('.git')
        if '.git' in r.split(os.sep):
            continue
        for f in files:
            full=os.path.join(r,f)
            if '/.git/' in full:
                continue
            rel=os.path.relpath(full, root)
            try:
                st=os.stat(full)
                out[rel]=(st.st_dev, st.st_ino, st.st_nlink)
            except FileNotFoundError:
                pass
    return out
src_w=work_files(src)
dst_w=work_files(dst)
assert len(src_w)==731 and len(dst_w)==731, f"work counts {len(src_w)} {len(dst_w)}"
src_di=set((d,i) for d,i,n in src_w.values())
dst_di=set((d,i) for d,i,n in dst_w.values())
assert src_di.isdisjoint(dst_di), "worktree inode sharing (hardlink)"
for rel,(d,i,n) in dst_w.items():
    assert n==1, f"hardlink nlink {rel} {n}"
print(f"isolation OK git {len(src_inodes)}/{len(dst_inodes)} work 731/731 no sharing nlink==1")
PYEOF
[ "$(cat "$EVIDENCE/isolation-check-exit.txt")" = "0" ] || fail "isolation-check failed"
run dst-noalternates bash -c "test ! -e \"$DST/.git/objects/info/alternates\" && test ! -e \"$DST/.git/objects/info\" && echo no-alternates" || fail "dst-noalternates rc"
run dst-config-show git -C "$DST" --no-optional-locks config --list --show-origin || fail "dst-config-show rc"
run env-check bash -c "env | grep -E '^GIT_(DIR|WORK_TREE|INDEX_FILE)=' || echo no-inherited-GIT-DIR" || fail "env-check rc"
grep -q "no-inherited-GIT-DIR" "$EVIDENCE/env-check-stdout.txt" || fail "inherited GIT_DIR/WORK_TREE/INDEX_FILE present"
run dst-hash-everything python3 - "$DST" <<'PYEOF'
import os, hashlib, sys
dst=sys.argv[1]
for root,dirs,files in os.walk(dst):
    if '.git' in dirs:
        dirs.remove('.git')
    if '/.git/' in root or root.endswith('/.git'):
        continue
    if '.git' in root.split(os.sep):
        continue
    for f in sorted(files):
        full=os.path.join(root,f)
        if '/.git/' in full:
            continue
        rel=os.path.relpath(full, dst)
        data=open(full,'rb').read()
        print(f"{hashlib.sha256(data).hexdigest()}  {len(data)}  {rel}")
PYEOF
[ "$(cat "$EVIDENCE/dst-hash-everything-exit.txt")" = "0" ] || fail "dst-hash post failed"

run src-head-post git -C "$SRC" --no-optional-locks rev-parse HEAD || fail "src-head-post rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/src-head-post-stdout.txt" || fail "SRC HEAD changed post"
run src-status-post git -C "$SRC" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "src-status-post rc"
run recon-head-post git -C "$REPO" --no-optional-locks rev-parse HEAD || fail "recon-head-post rc"
grep -q "^f84fcf5321be3798c862c0156278afbba01f89f6$" "$EVIDENCE/recon-head-post-stdout.txt" || fail "recon HEAD changed"
run rejected-head-post git -C "$REJECTED" --no-optional-locks rev-parse HEAD || fail "rejected-head-post rc"
grep -q "^a8890d4ff612563e71b7dcf5db76287acfe4ea35$" "$EVIDENCE/rejected-head-post-stdout.txt" || fail "rejected HEAD changed post"

printf "DONE OK %s DST %s\n" "$STAMP" "$DST" >> "$LOG"
echo "DONE OK"
