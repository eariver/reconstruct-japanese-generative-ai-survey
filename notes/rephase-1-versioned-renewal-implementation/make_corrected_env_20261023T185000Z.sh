#!/bin/bash
# Corrected environment provision — actual409+57 workcopy from proof-copy (retry with fixed env-check)
# Saved BEFORE execution via dedicated editor (Write), no apply_patch available.
# First attempt 184000Z failed only on overly strict env-check (sanitization vars mistaken for inherited).
# This retry uses fresh unique id 185000Z, same safe method, corrected inherited-DIR check.
# No old runners, no network, no restore, no reconstruct/input writes (except new WORK+EVIDENCE).
# Fail-closed: set -u only, explicit rc checks, stop before WORK creation on pre-check failure.
set -u
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
PROOF="$REPO/.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60"
SNAP="$REPO/.rephase-1-editorial-runtime/jgas-editorial-r7b-20261023T034500Z/candidate-partial-b40de60"
PATCH="$REPO/notes/rephase-1-editorial-operation-implementation/source-packaging/complete-r3-operation-409.patch"
MANIFEST_COMPLETE="$REPO/notes/rephase-1-editorial-operation-implementation/source-packaging/complete-r3-operation-manifest.json"
MANIFEST_R7B="$REPO/notes/rephase-1-editorial-operation-implementation/correction-r7/source-manifest-r7b.json"
STAMP="20261023T185000Z"
PACKROOT="$REPO/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z"
WORK="$PACKROOT/candidate-work"
REJECTED="$REPO/.rephase-1-editorial-runtime/versioned-renewal-impl-20261023T181352Z/candidate-work"
EVIDENCE="$REPO/notes/rephase-1-versioned-renewal-implementation/environment-correction-evidence-20261023T185000Z"
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

[ -d "$PROOF/.git" ] || fail "proof .git missing"
[ -f "$PATCH" ] || fail "patch missing"
[ -f "$MANIFEST_COMPLETE" ] || fail "complete manifest missing"
[ -f "$MANIFEST_R7B" ] || fail "r7b manifest missing"
[ -d "$REJECTED/.git" ] || fail "rejected M1 missing (must preserve, not modify)"
[ -e "$PACKROOT" ] && fail "PACKROOT already exists, need fresh unique id"
[ -e "$WORK" ] && fail "WORK already exists"

run recon-head git -C "$REPO" --no-optional-locks rev-parse HEAD || fail "recon-head rc"
grep -q "^c5b0d7cff9f978a2823f9a9e00ae1e0f9d5b3e1f$" "$EVIDENCE/recon-head-stdout.txt" || fail "recon HEAD mismatch"
run recon-status git -C "$REPO" --no-optional-locks status --porcelain=v1 --untracked-files=normal || fail "recon-status rc"

run rejected-head git -C "$REJECTED" --no-optional-locks rev-parse HEAD || fail "rejected-head rc"
grep -q "^a8890d4ff612563e71b7dcf5db76287acfe4ea35$" "$EVIDENCE/rejected-head-stdout.txt" || fail "rejected HEAD changed (must stay a8890d4)"
run rejected-log git -C "$REJECTED" --no-optional-locks log --oneline -3 || fail "rejected-log rc"
run rejected-status git -C "$REJECTED" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "rejected-status rc"
[ -s "$EVIDENCE/rejected-status-stdout.txt" ] && fail "rejected M1 status not clean (must preserve untouched)"

run proof-head git -C "$PROOF" --no-optional-locks rev-parse HEAD || fail "proof-head rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/proof-head-stdout.txt" || fail "proof HEAD not 409"
run proof-tree git -C "$PROOF" --no-optional-locks rev-parse 'HEAD^{tree}' || fail "proof-tree rc"
grep -q "^8ce3699861505f32d1d60bdc185d4d4f635aedb2$" "$EVIDENCE/proof-tree-stdout.txt" || fail "proof tree not 8ce"
run proof-status git -C "$PROOF" --no-optional-locks status --porcelain=v1 --untracked-files=normal || fail "proof-status rc"
run proof-diff-names git -C "$PROOF" --no-optional-locks diff HEAD --name-only || fail "proof-diff-names rc"
run proof-diff-cached git -C "$PROOF" --no-optional-locks diff --cached --name-only || fail "proof-diff-cached rc"
[ -s "$EVIDENCE/proof-diff-cached-stdout.txt" ] && fail "proof index not clean (diff --cached must be empty)"

run patch-sha sha256sum "$PATCH" || fail "patch-sha rc"
grep -q "^659063dc27f0926aaf6e8a33f322937076563c4a23f6cf0d80ca970e1b2abd5b" "$EVIDENCE/patch-sha-stdout.txt" || fail "patch SHA mismatch"
run patch-bytes wc -c "$PATCH" || fail "patch-bytes rc"
grep -q "2018112" "$EVIDENCE/patch-bytes-stdout.txt" || fail "patch bytes mismatch"

run snap-head git -C "$SNAP" --no-optional-locks rev-parse HEAD || fail "snap-head rc"
grep -q "^721a04d85532d7855f3e54cc411f5847c787726e$" "$EVIDENCE/snap-head-stdout.txt" || fail "snap HEAD not 721a04"
run snap-tree git -C "$SNAP" --no-optional-locks rev-parse 'HEAD^{tree}' || fail "snap-tree rc"
grep -q "^ac7cb0bd2e977b46e957450816eddd779799e144$" "$EVIDENCE/snap-tree-stdout.txt" || fail "snap tree mismatch"

run proof-manifest-verify python3 - "$PROOF" "$MANIFEST_COMPLETE" "$MANIFEST_R7B" <<'PYEOF'
import json, hashlib, os, sys
proof, mcomp_path, mr7b_path = sys.argv[1], sys.argv[2], sys.argv[3]
mcomp=json.load(open(mcomp_path))
mr7b=json.load(open(mr7b_path))
assert mcomp['delta_count']==57, "delta_count"
assert mcomp['tracked_modified']==25, "tracked_modified"
assert mcomp['untracked_new']==32, "untracked_new"
assert mcomp['head']=="409b292756dd1277b9dfae87679934c0d2ce251c", "head"
assert mcomp['head_tree']=="8ce3699861505f32d1d60bdc185d4d4f635aedb2", "tree"
assert mcomp['patch']['sha256']=="659063dc27f0926aaf6e8a33f322937076563c4a23f6cf0d80ca970e1b2abd5b", "patch sha"
assert mcomp['patch']['bytes']==2018112, "patch bytes"
assert len(mcomp['files'])==57, "files len"
assert mr7b['count']==721 and len(mr7b['files'])==721, "r7b 721"
rel=[]
for root,dirs,files in os.walk(proof):
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
        rel.append(os.path.relpath(full, proof))
assert len(rel)==721, f"proof rel count {len(rel)} !=721"
r7b_paths=set(x['path'] for x in mr7b['files'])
assert set(rel)==r7b_paths, f"proof rel != r7b 721"
r7b_by={x['path']:x for x in mr7b['files']}
for path,meta in mcomp['files'].items():
    full=os.path.join(proof,path)
    data=open(full,'rb').read()
    h=hashlib.sha256(data).hexdigest()
    assert h==meta['sha256'], f"sha {path}"
    assert len(data)==meta['bytes'], f"bytes {path}"
    assert h==r7b_by[path]['sha256'], f"r7b sha {path}"
print("proof-manifest-verify OK 25M32A 721/721 57/57")
PYEOF
[ "$(cat "$EVIDENCE/proof-manifest-verify-exit.txt")" = "0" ] || fail "proof-manifest-verify failed"

mkdir -p "$WORK" || fail "mkdir WORK"
run mkdir-work mkdir -p "$WORK" || fail "mkdir-work rc"
run cp-git cp -a "$PROOF/.git" "$WORK/.git" || fail "cp-git rc"
[ -d "$WORK/.git" ] || fail "WORK .git missing after cp"
run work-git-count bash -c "find \"$WORK/.git\" -type f | wc -l" || fail "work-git-count rc"
grep -q "83" "$EVIDENCE/work-git-count-stdout.txt" || fail "WORK .git file count not 83"
[ -e "$WORK/.git/objects/info/alternates" ] && fail "WORK alternates exists (must be absent)"
[ -e "$WORK/.git/objects/info" ] && fail "WORK objects/info exists (proof has no objects/info, must match absence)"
run work-head git -C "$WORK" --no-optional-locks rev-parse HEAD || fail "work-head rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/work-head-stdout.txt" || fail "WORK HEAD not 409"
run work-tree git -C "$WORK" --no-optional-locks rev-parse 'HEAD^{tree}' || fail "work-tree rc"
grep -q "^8ce3699861505f32d1d60bdc185d4d4f635aedb2$" "$EVIDENCE/work-tree-stdout.txt" || fail "WORK tree not 8ce"
run work-gitdir git -C "$WORK" --no-optional-locks rev-parse --absolute-git-dir || fail "work-gitdir rc"
grep -q "versioned-renewal-env-20261023T185000Z/candidate-work/.git" "$EVIDENCE/work-gitdir-stdout.txt" || fail "WORK gitdir not own"
run work-remote git -C "$WORK" --no-optional-locks remote -v || fail "work-remote rc"
grep -q "example.invalid" "$EVIDENCE/work-remote-stdout.txt" || fail "WORK remote not inert"
grep -q "github.com" "$EVIDENCE/work-remote-stdout.txt" && fail "WORK remote points to real origin"

run populate-worktree python3 - "$PROOF" "$WORK" "$MANIFEST_R7B" <<'PYEOF'
import json, os, shutil, hashlib, sys
src, dst, manifest_path = sys.argv[1], sys.argv[2], sys.argv[3]
m=json.load(open(manifest_path))
assert m['count']==721, "r7b count"
for entry in m['files']:
    p=entry['path']
    s=os.path.join(src,p)
    d=os.path.join(dst,p)
    assert os.path.isfile(s), f"src missing {p}"
    os.makedirs(os.path.dirname(d) or dst, exist_ok=True)
    shutil.copy2(s,d)
    data=open(d,'rb').read()
    assert hashlib.sha256(data).hexdigest()==entry['sha256'], f"copy sha {p}"
    assert len(data)==entry['bytes'], f"copy bytes {p}"
print(f"populate OK {len(m['files'])} files")
PYEOF
[ "$(cat "$EVIDENCE/populate-worktree-exit.txt")" = "0" ] || fail "populate-worktree failed"

run work-count bash -c "find \"$WORK\" -path \"$WORK/.git\" -prune -o -type f -print | wc -l" || fail "work-count rc"
grep -q "721" "$EVIDENCE/work-count-stdout.txt" || fail "WORK file count not 721"
run work-status git -C "$WORK" --no-optional-locks status --porcelain=v1 --untracked-files=normal || fail "work-status rc"
run work-diff-names git -C "$WORK" --no-optional-locks diff HEAD --name-only || fail "work-diff-names rc"
run work-diff-cached git -C "$WORK" --no-optional-locks diff --cached --name-only || fail "work-diff-cached rc"
[ -s "$EVIDENCE/work-diff-cached-stdout.txt" ] && fail "WORK index not clean"

run work-manifest-verify python3 - "$WORK" "$MANIFEST_COMPLETE" "$MANIFEST_R7B" <<'PYEOF'
import json, hashlib, os, sys, subprocess
work, mcomp_path, mr7b_path = sys.argv[1], sys.argv[2], sys.argv[3]
mcomp=json.load(open(mcomp_path))
mr7b=json.load(open(mr7b_path))
env={**os.environ, 'GIT_NO_LAZY_FETCH':'1','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_OPTIONAL_LOCKS':'0'}
for k in ['GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE']:
    env.pop(k,None)
out=subprocess.check_output(['git','--no-optional-locks','status','--porcelain=v1','--untracked-files=normal'], cwd=work, env=env).decode()
lines=[l for l in out.splitlines() if l.strip()]
mods=sorted([l[3:] for l in lines if l.startswith(' M ')])
adds=sorted([l[3:] for l in lines if l.startswith('?? ')])
assert len(mods)==25 and len(adds)==32, f"status {len(mods)}M {len(adds)}A"
m_mods=sorted([p for p,m in mcomp['files'].items() if m['git_status']=='M'])
m_adds=sorted([p for p,m in mcomp['files'].items() if m['git_status']=='A'])
assert mods==m_mods, f"mods mismatch"
assert adds==m_adds, f"adds mismatch"
for entry in mr7b['files']:
    p=entry['path']
    data=open(os.path.join(work,p),'rb').read()
    assert hashlib.sha256(data).hexdigest()==entry['sha256'], f"721 sha {p}"
for path,meta in mcomp['files'].items():
    data=open(os.path.join(work,path),'rb').read()
    assert hashlib.sha256(data).hexdigest()==meta['sha256'], f"57 sha {path}"
print("work-manifest-verify OK 25M32A 721/721")
PYEOF
[ "$(cat "$EVIDENCE/work-manifest-verify-exit.txt")" = "0" ] || fail "work-manifest-verify failed"

run isolation-check python3 - "$PROOF" "$WORK" <<'PYEOF'
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
assert src_inodes.isdisjoint(dst_inodes), f"git inode collision"
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
assert len(src_w)==721 and len(dst_w)==721, f"work counts {len(src_w)} {len(dst_w)}"
src_di=set((d,i) for d,i,n in src_w.values())
dst_di=set((d,i) for d,i,n in dst_w.values())
assert src_di.isdisjoint(dst_di), "worktree inode sharing (hardlink)"
for rel,(d,i,n) in dst_w.items():
    assert n==1, f"hardlink nlink {rel} {n}"
print(f"isolation OK git {len(src_inodes)}/{len(dst_inodes)} work 721/721 no sharing")
PYEOF
[ "$(cat "$EVIDENCE/isolation-check-exit.txt")" = "0" ] || fail "isolation-check failed"
run work-noalternates bash -c "test ! -e \"$WORK/.git/objects/info/alternates\" && test ! -e \"$WORK/.git/objects/info\" && echo no-alternates" || fail "work-noalternates rc"
run work-config-show git -C "$WORK" --no-optional-locks config --list --show-origin || fail "work-config-show rc"
run env-check bash -c "env | grep -E '^GIT_(DIR|WORK_TREE|INDEX_FILE)=' || echo no-inherited-GIT-DIR" || fail "env-check rc"
grep -q "no-inherited-GIT-DIR" "$EVIDENCE/env-check-stdout.txt" || fail "inherited GIT_DIR/WORK_TREE/INDEX_FILE present"

run proof-head-post git -C "$PROOF" --no-optional-locks rev-parse HEAD || fail "proof-head-post rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/proof-head-post-stdout.txt" || fail "proof HEAD changed post"
run proof-status-post git -C "$PROOF" --no-optional-locks status --porcelain=v1 --untracked-files=normal || fail "proof-status-post rc"
run recon-head-post git -C "$REPO" --no-optional-locks rev-parse HEAD || fail "recon-head-post rc"
grep -q "^c5b0d7cff9f978a2823f9a9e00ae1e0f9d5b3e1f$" "$EVIDENCE/recon-head-post-stdout.txt" || fail "recon HEAD changed"
run rejected-head-post git -C "$REJECTED" --no-optional-locks rev-parse HEAD || fail "rejected-head-post rc"
grep -q "^a8890d4ff612563e71b7dcf5db76287acfe4ea35$" "$EVIDENCE/rejected-head-post-stdout.txt" || fail "rejected HEAD changed post"

printf "DONE OK %s WORK %s\n" "$STAMP" "$WORK" >> "$LOG"
echo "DONE OK"
