#!/bin/bash
# Archive-compatible INPUT for final affected verification (all SOURCE authors done; editorial worker only OWN fixture child continues, no code writes)
# Previous 731/735/736/739 inputs immutable preserved, no overwrites. Same independent partial GitDB / raw source hash before-after / safe intent copy / no hardlinks / no alternates / no Git root env / no ordinary commits / no cleanup / no project imports/tests/build/network.
# Source unchanged readonly during freeze. Documentation/source inspection only.
# Saved BEFORE execution via dedicated editor (Write). No old runners. Read-only AST/json as data (no project imports).
# Fail-closed: set -u only, explicit rc, no overwrite/deletion.
set -u
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
SRC="$REPO/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
PREV731="$REPO/.rephase-1-editorial-runtime/versioned-renewal-freeze-20261024T174422Z/snapshot-work"
PREV735="$REPO/.rephase-1-editorial-runtime/versioned-renewal-combined-freeze-20261025T041436Z/snapshot-work"
PREV736="$REPO/.rephase-1-editorial-runtime/versioned-renewal-final-input-20261025T051343Z/snapshot-work"
PREV739="$REPO/.rephase-1-editorial-runtime/versioned-renewal-repair-input-20261025T082826Z/snapshot-work"
MANIFEST_COMPLETE="$REPO/notes/rephase-1-editorial-operation-implementation/source-packaging/complete-r3-operation-manifest.json"
MANIFEST_R7B="$REPO/notes/rephase-1-editorial-operation-implementation/correction-r7/source-manifest-r7b.json"
MANIFEST_PREV739="$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/integration-repair-input.json"
STAMP="20261025T133248Z"
FREEZE_PARENT="$REPO/.rephase-1-editorial-runtime/versioned-renewal-archive-input-20261025T133248Z"
DST="$FREEZE_PARENT/snapshot-work"
PACKET_DIR="$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025"
EVIDENCE="$PACKET_DIR/archive-compatible-input-evidence-20261025T133248Z"
export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C

mkdir -p "$EVIDENCE"
LOG="$EVIDENCE/commands.log"
printf "stamp %s ARCHIVE-INPUT (prev731/735/736/739 KEEP READONLY, no cleanup)\n" "$STAMP" > "$LOG"

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
[ -d "$PREV731/.git" ] || fail "PREV731 missing"
[ -d "$PREV735/.git" ] || fail "PREV735 missing"
[ -d "$PREV736/.git" ] || fail "PREV736 missing"
[ -d "$PREV739/.git" ] || fail "PREV739 missing"
[ -f "$MANIFEST_COMPLETE" ] || fail "complete manifest missing"
[ -f "$MANIFEST_R7B" ] || fail "r7b manifest missing"
[ -f "$MANIFEST_PREV739" ] || fail "prev739 manifest missing (do NOT overwrite)"
[ -d "$REPO/.rephase-1-editorial-runtime" ] || fail "ignored parent missing"
[ -e "$FREEZE_PARENT" ] && fail "FREEZE_PARENT exists (fresh unique required)"
[ -e "$DST" ] && fail "DST exists"

run recon-head git -C "$REPO" --no-optional-locks rev-parse HEAD || fail "recon-head rc"
grep -q "^f84fcf5321be3798c862c0156278afbba01f89f6$" "$EVIDENCE/recon-head-stdout.txt" || fail "recon HEAD not f84fcf5"
run recon-status git -C "$REPO" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "recon-status rc"
run recon-diff-cached git -C "$REPO" --no-optional-locks diff --cached --name-only || fail "recon-diff-cached rc"
[ -s "$EVIDENCE/recon-diff-cached-stdout.txt" ] && fail "recon index not clean"
run recon-diff-head git -C "$REPO" --no-optional-locks diff HEAD --name-only || fail "recon-diff-head rc"
[ -s "$EVIDENCE/recon-diff-head-stdout.txt" ] && fail "recon tracked mods"
run recon-untracked-only python3 - "$EVIDENCE/recon-status-stdout.txt" <<'PYEOF'
import sys
p=sys.argv[1]
lines=[l.rstrip('\n') for l in open(p) if l.strip()!='']
for l in lines:
    assert l.startswith('?? '), f"tracked: {l}"
print(f"recon untracked-only OK {len(lines)}")
PYEOF
[ "$(cat "$EVIDENCE/recon-untracked-only-exit.txt")" = "0" ] || fail "recon untracked-only failed"

run prev731-head git -C "$PREV731" --no-optional-locks rev-parse HEAD || fail "prev731-head rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/prev731-head-stdout.txt" || fail "PREV731 HEAD not 409"
run prev736-head git -C "$PREV736" --no-optional-locks rev-parse HEAD || fail "prev736-head rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/prev736-head-stdout.txt" || fail "PREV736 HEAD not 409"
run prev739-head git -C "$PREV739" --no-optional-locks rev-parse HEAD || fail "prev739-head rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/prev739-head-stdout.txt" || fail "PREV739 HEAD not 409"
run prev735-head git -C "$PREV735" --no-optional-locks rev-parse HEAD || fail "prev735-head rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/prev735-head-stdout.txt" || fail "PREV735 HEAD not 409"
run prev731-count bash -c "find \"$PREV731\" -path \"$PREV731/.git\" -prune -o -type f -print | wc -l" || fail "prev731-count rc"
grep -q "731" "$EVIDENCE/prev731-count-stdout.txt" || fail "PREV731 not 731"
run prev736-count bash -c "find \"$PREV736\" -path \"$PREV736/.git\" -prune -o -type f -print | wc -l" || fail "prev736-count rc"
grep -q "736" "$EVIDENCE/prev736-count-stdout.txt" || fail "PREV736 not 736"
run prev739-count bash -c "find \"$PREV739\" -path \"$PREV739/.git\" -prune -o -type f -print | wc -l" || fail "prev739-count rc"
grep -q "739" "$EVIDENCE/prev739-count-stdout.txt" || fail "PREV739 not 739"
run prev735-count bash -c "find \"$PREV735\" -path \"$PREV735/.git\" -prune -o -type f -print | wc -l" || fail "prev735-count rc"
cat "$EVIDENCE/prev735-count-stdout.txt"

run src-head git -C "$SRC" --no-optional-locks rev-parse HEAD || fail "src-head rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/src-head-stdout.txt" || fail "SRC HEAD not 409"
run src-tree git -C "$SRC" --no-optional-locks rev-parse 'HEAD^{tree}' || fail "src-tree rc"
grep -q "^8ce3699861505f32d1d60bdc185d4d4f635aedb2$" "$EVIDENCE/src-tree-stdout.txt" || fail "SRC tree not 8ce"
run src-log git -C "$SRC" --no-optional-locks log --oneline -3 || fail "src-log rc"
run src-status git -C "$SRC" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "src-status rc"
run src-diff-cached git -C "$SRC" --no-optional-locks diff --cached --name-only || fail "src-diff-cached rc"
[ -s "$EVIDENCE/src-diff-cached-stdout.txt" ] && fail "SRC index not clean (verify root index unchanged)"
run src-diff-names git -C "$SRC" --no-optional-locks diff HEAD --name-only || fail "src-diff-names rc"
run src-others git -C "$SRC" --no-optional-locks ls-files --others --exclude-standard || fail "src-others rc"
run src-deleted git -C "$SRC" --no-optional-locks ls-files --deleted || fail "src-deleted rc"
[ -s "$EVIDENCE/src-deleted-stdout.txt" ] && fail "SRC tracked deletions present (existing D history no actual D)"
run src-count-all bash -c "find \"$SRC\" -path \"$SRC/.git\" -prune -o -type f -print | wc -l" || fail "src-count-all rc"
grep -q "775" "$EVIDENCE/src-count-all-stdout.txt" || fail "SRC total not 775 (740+35pyc)"
run src-cache-dirs bash -c "find \"$SRC\" -type d -name __pycache__ -print" || fail "src-cache-dirs rc"
grep -q "scripts/__pycache__" "$EVIDENCE/src-cache-dirs-stdout.txt" || fail "scripts cache missing"
grep -q "tests/__pycache__" "$EVIDENCE/src-cache-dirs-stdout.txt" || fail "tests cache missing"
run src-pyc-count bash -c "find \"$SRC\" -name '*.pyc' | wc -l" || fail "src-pyc-count rc"
grep -q "35" "$EVIDENCE/src-pyc-count-stdout.txt" || fail "SRC pyc not 35"
run src-git-count bash -c "find \"$SRC/.git\" -type f | wc -l" || fail "src-git-count rc"
grep -q "83" "$EVIDENCE/src-git-count-stdout.txt" || fail "SRC .git not 83"
[ -e "$SRC/.git/objects/info/alternates" ] && fail "SRC alternates exists"
[ -e "$SRC/.git/objects/info" ] && fail "SRC objects/info exists"
run src-remote git -C "$SRC" --no-optional-locks remote -v || fail "src-remote rc"
grep -q "example.invalid" "$EVIDENCE/src-remote-stdout.txt" || fail "SRC remote not inert"
grep -q "github.com" "$EVIDENCE/src-remote-stdout.txt" && fail "SRC remote real"
run src-shallow cat "$SRC/.git/shallow" || fail "src-shallow rc"
grep -q "^774dd39a951c9ac3818e83dfffd4c7666efb0a20$" "$EVIDENCE/src-shallow-stdout.txt" || fail "SRC shallow not 774"

run src-archive-verify python3 - "$SRC" "$MANIFEST_R7B" "$MANIFEST_COMPLETE" "$MANIFEST_PREV739" <<'PYEOF'
import json, os, sys, hashlib, ast, subprocess
src, r7b_path, comp_path, prev739_path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
r7b=json.load(open(r7b_path))
comp=json.load(open(comp_path))
prev739=json.load(open(prev739_path))
assert r7b['count']==721
assert comp['delta_count']==57
assert prev739['full_source_identity']['worktree_intended_files']==739
r7b_paths=set(x['path'] for x in r7b['files'])
rel_all=[]
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
        rel_all.append(os.path.relpath(full, src))
cur_all=set(rel_all)
assert len(cur_all)==775, f"total {len(cur_all)} !=775"
cache=[p for p in cur_all if p.endswith('.pyc') or '__pycache__' in p]
assert len(cache)==35, f"cache {len(cache)}"
# H/S active cache count metadata exclude only declared bytecode keep SRC (do NOT delete SRC cache)
hs_cache=[p for p in cache if 'history' in p or 'source' in p.lower() or 'schema' in p]
assert len(hs_cache)>=2, "H/S active cache expected"
cur=set(p for p in cur_all if p not in cache)
assert len(cur)==740, f"intended {len(cur)} !=740 (739+1)"
assert r7b_paths.issubset(cur), "R7b missing"
extra10=[
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
prev4=[
 "tests/test_versioned_renewal_history_author_h_20261025.py",
 "tests/test_versioned_renewal_source_author_s_f1f2f3_20261025.py",
 "tests/test_versioned_renewal_operation_correction_b1b2b3.py",
 "tests/test_versioned_renewal_reader_f4_20261025.py",
]
prev1=["tests/test_versioned_renewal_history_perf_batched_20261025.py"]
prev3=[
 "tests/test_editorial_renewal_p1_dispatch_20261025.py",
 "tests/test_versioned_renewal_freeze_transitive_correction_20261025.py",
 "tests/test_versioned_renewal_history_traversal_opt_20261025.py",
]
new1=["tests/test_editorial_renewal_archive_correction_20261025.py"]
expected_extra=sorted(extra10+prev4+prev1+prev3+new1)
extra=sorted(cur-r7b_paths)
assert extra==expected_extra, f"extra mismatch {extra}"
env={**os.environ, 'GIT_NO_LAZY_FETCH':'1','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_OPTIONAL_LOCKS':'0'}
for k in ['GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE']:
    env.pop(k,None)
out=subprocess.check_output(['git','--no-optional-locks','status','--porcelain=v1','--untracked-files=all'], cwd=src, env=env).decode()
lines=[l for l in out.splitlines() if l.strip()]
mods=sorted([l[3:] for l in lines if l.startswith(' M ')])
adds_raw=sorted([l[3:] for l in lines if l.startswith('?? ')])
assert len(mods)==39, f"M {len(mods)} !=39"
assert len(adds_raw)==86, f"raw U {len(adds_raw)} !=86 (51+35pyc)"
adds=[p for p in adds_raw if p not in cache]
assert len(adds)==51, f"intended U {len(adds)} !=51"
assert not any(l.startswith(' D ') or l.startswith('D ') for l in lines), "tracked deletions (existing D history no actual D)"
comp_m=set(p for p,m in comp['files'].items() if m['git_status']=='M')
comp_a=set(p for p,m in comp['files'].items() if m['git_status']=='A')
assert comp_m.issubset(set(mods))
assert comp_a.issubset(set(adds))
assert set(extra10).issubset(set(adds))
assert set(prev4).issubset(set(adds))
assert set(prev1).issubset(set(adds))
assert set(prev3).issubset(set(adds))
assert set(new1).issubset(set(adds))
for p in [x for x in adds if x.endswith('.json')]:
    json.load(open(os.path.join(src,p)))
for p in [x for x in adds if x.endswith('.py')]:
    ast.parse(open(os.path.join(src,p)).read())
def sha(p):
    return hashlib.sha256(open(os.path.join(src,p),'rb').read()).hexdigest()
actual={
 "H": sha("scripts/survey_versioned_renewal_history_v2.py"),
 "P1": sha("scripts/survey_editorial_correction_proposal_v2.py"),
 "PUB": sha("scripts/survey_publication_v2.py"),
 "S": sha("scripts/survey_versioned_renewal_source_v2.py"),
 "HIGH": sha("scripts/survey_versioned_renewal_v2.py"),
 "Reader": sha("scripts/survey_reader_publication_v2.py"),
 "EDHIGH": sha("scripts/survey_editorial_publication_v2.py"),
 "ARCH": sha("tests/test_editorial_renewal_archive_correction_20261025.py"),
 "STYLE": sha("templates/survey/jgaisurvey.sty"),
}
assert actual["H"]=="6fe86e78a12e2159d6ff50dfd7f70fda7b2e0d34d48db26402743edda2eca5ad", f"H {actual['H']}"
assert actual["P1"]=="825dba1dedaed0850134b3a54a249a427b2e77709861818e8eb7cb63e1a33a2b", f"P1"
assert actual["PUB"]=="3f4039fd7699baa212020dddfb02b3918bd63e02c475d638d99cbb2a1150d8d6", f"PUB"
assert actual["S"]=="20f63eafc96923dc7be25f3f495b94dd9add0e398d6cdc2fe47c2c9bff46c306", "S"
assert actual["HIGH"]=="9a0469ef5a6bc2b2e37fc9efb1376cfccbd0333ffaa08a59d23634345d382152", "HIGH"
assert actual["Reader"]=="098a2c8222f15f693c524139f2678be008a7ec9fafca275fc831ede9aa13bf1c", "Reader"
assert actual["EDHIGH"]=="85814124278c3112562c84c4685ef555689d551b494dcbd23526fb27dc1d9a2a", f"EDHIGH {actual['EDHIGH']}"
assert actual["ARCH"]=="5e5a0bdc9d950c7ef0d409be8fd6245ad8830cf8bcaf001bca429c309f5d57d7", f"ARCH {actual['ARCH']}"
assert actual["STYLE"]=="035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec", "STYLE baseline 035"
print(f"archive-verify OK 740=R7b721+10+4+1+3+1new 39M51U(+35pyc) H6fe/P1825/PUB3f stable EDHIGH8581 ARCH5e5a STYLE035 no-D index-clean")
print(actual)
PYEOF
[ "$(cat "$EVIDENCE/src-archive-verify-exit.txt")" = "0" ] || fail "src-archive-verify failed"

run src-ls-files-s git -C "$SRC" --no-optional-locks ls-files -s || fail "src-ls-files-s rc"
run src-hash-intended python3 - "$SRC" <<'PYEOF'
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
        if '__pycache__' in full or full.endswith('.pyc'):
            continue
        rel=os.path.relpath(full, src)
        data=open(full,'rb').read()
        print(f"{hashlib.sha256(data).hexdigest()}  {len(data)}  {rel}")
PYEOF
[ "$(cat "$EVIDENCE/src-hash-intended-exit.txt")" = "0" ] || fail "src-hash pre failed"

mkdir -p "$FREEZE_PARENT" || fail "mkdir FREEZE_PARENT"
run mkdir-archive mkdir -p "$DST" || fail "mkdir DST rc"
run cp-git cp -a "$SRC/.git" "$DST/.git" || fail "cp-git rc"
[ -d "$DST/.git" ] || fail "DST .git missing"
run dst-git-count bash -c "find \"$DST/.git\" -type f | wc -l" || fail "dst-git-count rc"
grep -q "83" "$EVIDENCE/dst-git-count-stdout.txt" || fail "DST .git not 83"
[ -e "$DST/.git/objects/info/alternates" ] && fail "DST alternates exists"
[ -e "$DST/.git/objects/info" ] && fail "DST objects/info exists"
run dst-head git -C "$DST" --no-optional-locks rev-parse HEAD || fail "dst-head rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/dst-head-stdout.txt" || fail "DST HEAD not 409"
run dst-tree git -C "$DST" --no-optional-locks rev-parse 'HEAD^{tree}' || fail "dst-tree rc"
grep -q "^8ce3699861505f32d1d60bdc185d4d4f635aedb2$" "$EVIDENCE/dst-tree-stdout.txt" || fail "DST tree not 8ce"
run dst-gitdir git -C "$DST" --no-optional-locks rev-parse --absolute-git-dir || fail "dst-gitdir rc"
grep -q "versioned-renewal-archive-input-20261025T133248Z/snapshot-work/.git" "$EVIDENCE/dst-gitdir-stdout.txt" || fail "DST gitdir not own"
run dst-remote git -C "$DST" --no-optional-locks remote -v || fail "dst-remote rc"
grep -q "example.invalid" "$EVIDENCE/dst-remote-stdout.txt" || fail "DST remote not inert"
grep -q "github.com" "$EVIDENCE/dst-remote-stdout.txt" && fail "DST remote real"
run dst-log git -C "$DST" --no-optional-locks log --oneline -3 || fail "dst-log rc"
grep -q "^409b292" "$EVIDENCE/dst-log-stdout.txt" || fail "DST log not real409"

run populate-archive python3 - "$SRC" "$DST" "$MANIFEST_R7B" <<'PYEOF'
import json, os, shutil, sys
src, dst, manifest_path = sys.argv[1], sys.argv[2], sys.argv[3]
m=json.load(open(manifest_path))
r7b_paths=[x['path'] for x in m['files']]
extra10=[
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
prev4=[
 "tests/test_versioned_renewal_history_author_h_20261025.py",
 "tests/test_versioned_renewal_source_author_s_f1f2f3_20261025.py",
 "tests/test_versioned_renewal_operation_correction_b1b2b3.py",
 "tests/test_versioned_renewal_reader_f4_20261025.py",
]
prev1=["tests/test_versioned_renewal_history_perf_batched_20261025.py"]
prev3=[
 "tests/test_editorial_renewal_p1_dispatch_20261025.py",
 "tests/test_versioned_renewal_freeze_transitive_correction_20261025.py",
 "tests/test_versioned_renewal_history_traversal_opt_20261025.py",
]
new1=["tests/test_editorial_renewal_archive_correction_20261025.py"]
intended=r7b_paths+extra10+prev4+prev1+prev3+new1
assert len(intended)==740
for p in intended:
    s=os.path.join(src,p)
    d=os.path.join(dst,p)
    assert os.path.isfile(s), f"src missing {p}"
    parent=os.path.dirname(d)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)
    shutil.copy2(s,d)
    assert open(s,'rb').read()==open(d,'rb').read(), f"copy mismatch {p}"
print(f"populate OK {len(intended)} manifest-exact copy2 (no rsync blind, no cache)")
PYEOF
[ "$(cat "$EVIDENCE/populate-archive-exit.txt")" = "0" ] || fail "populate-archive failed"

run dst-count bash -c "find \"$DST\" -path \"$DST/.git\" -prune -o -type f -print | wc -l" || fail "dst-count rc"
grep -q "740" "$EVIDENCE/dst-count-stdout.txt" || fail "DST not 740"
run dst-status git -C "$DST" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "dst-status rc"
run dst-diff-names git -C "$DST" --no-optional-locks diff HEAD --name-only || fail "dst-diff-names rc"
run dst-diff-cached git -C "$DST" --no-optional-locks diff --cached --name-only || fail "dst-diff-cached rc"
[ -s "$EVIDENCE/dst-diff-cached-stdout.txt" ] && fail "DST index not clean"
run dst-others git -C "$DST" --no-optional-locks ls-files --others --exclude-standard || fail "dst-others rc"
run dst-pyc-check bash -c "find \"$DST\" -name '__pycache__' -o -name '*.pyc' | wc -l" || fail "dst-pyc-check rc"
grep -q "0" "$EVIDENCE/dst-pyc-check-stdout.txt" || fail "DST has cache"

run dst-manifest-verify python3 - "$SRC" "$DST" <<'PYEOF'
import hashlib, os, sys, subprocess
src, dst = sys.argv[1], sys.argv[2]
env={**os.environ, 'GIT_NO_LAZY_FETCH':'1','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_OPTIONAL_LOCKS':'0'}
for k in ['GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE']:
    env.pop(k,None)
def intended(cwd):
    out=subprocess.check_output(['git','--no-optional-locks','status','--porcelain=v1','--untracked-files=all'], cwd=cwd, env=env).decode()
    lines=[l for l in out.splitlines() if l.strip()]
    mods=sorted([l[3:] for l in lines if l.startswith(' M ')])
    adds_raw=sorted([l[3:] for l in lines if l.startswith('?? ')])
    adds=[p for p in adds_raw if '__pycache__' not in p and not p.endswith('.pyc')]
    return mods, adds, adds_raw
src_m, src_u, src_raw=intended(src)
dst_m, dst_u, dst_raw=intended(dst)
assert src_m==dst_m and src_u==dst_u, "SRC/DST mismatch"
assert len(dst_m)==39 and len(dst_u)==51, f"dst {len(dst_m)}M {len(dst_u)}U"
assert len(dst_raw)==51, "dst raw (no cache)"
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
        if '__pycache__' in full or full.endswith('.pyc'):
            continue
        rel=os.path.relpath(full, src)
        a=open(full,'rb').read()
        b=open(os.path.join(dst,rel),'rb').read()
        assert a==b, f"bytes {rel}"
print(f"dst-manifest-verify OK SRC==DST 39M51U intended 740/740")
PYEOF
[ "$(cat "$EVIDENCE/dst-manifest-verify-exit.txt")" = "0" ] || fail "dst-manifest-verify failed"

run isolation-check python3 - "$SRC" "$DST" <<'PYEOF'
import os, sys
src, dst = sys.argv[1], sys.argv[2]
def walk_git(root):
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
src_g=walk_git(src)
dst_g=walk_git(dst)
assert len(src_g)>0 and len(dst_g)>0
assert src_g.isdisjoint(dst_g), "git inode collision"
def work(root):
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
            if '__pycache__' in full or full.endswith('.pyc'):
                continue
            rel=os.path.relpath(full, root)
            st=os.stat(full)
            out[rel]=(st.st_dev, st.st_ino, st.st_nlink)
    return out
src_w=work(src)
dst_w=work(dst)
assert len(src_w)==740 and len(dst_w)==740, f"work {len(src_w)} {len(dst_w)}"
assert set((d,i) for d,i,n in src_w.values()).isdisjoint(set((d,i) for d,i,n in dst_w.values())), "worktree sharing"
for rel,(d,i,n) in dst_w.items():
    assert n==1, f"nlink {rel} {n}"
print(f"isolation OK git {len(src_g)}/{len(dst_g)} work 740/740 no sharing nlink==1")
PYEOF
[ "$(cat "$EVIDENCE/isolation-check-exit.txt")" = "0" ] || fail "isolation-check failed"
run dst-noalternates bash -c "test ! -e \"$DST/.git/objects/info/alternates\" && test ! -e \"$DST/.git/objects/info\" && echo no-alternates" || fail "dst-noalternates rc"
run dst-config-show git -C "$DST" --no-optional-locks config --list --show-origin || fail "dst-config-show rc"
run env-check bash -c "env | grep -E '^GIT_(DIR|WORK_TREE|INDEX_FILE)=' || echo no-inherited-GIT-DIR" || fail "env-check rc"
grep -q "no-inherited-GIT-DIR" "$EVIDENCE/env-check-stdout.txt" || fail "inherited GIT env"
run dst-hash-intended python3 - "$DST" <<'PYEOF'
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
[ "$(cat "$EVIDENCE/dst-hash-intended-exit.txt")" = "0" ] || fail "dst-hash post failed"

run src-head-post git -C "$SRC" --no-optional-locks rev-parse HEAD || fail "src-head-post rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/src-head-post-stdout.txt" || fail "SRC HEAD changed"
run src-status-post git -C "$SRC" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "src-status-post rc"
run prev731-head-post git -C "$PREV731" --no-optional-locks rev-parse HEAD || fail "prev731-head-post rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/prev731-head-post-stdout.txt" || fail "PREV731 HEAD changed"
run prev735-head-post git -C "$PREV735" --no-optional-locks rev-parse HEAD || fail "prev735-head-post rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/prev735-head-post-stdout.txt" || fail "PREV735 HEAD changed"
run prev736-head-post git -C "$PREV736" --no-optional-locks rev-parse HEAD || fail "prev736-head-post rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/prev736-head-post-stdout.txt" || fail "PREV736 HEAD changed"
run prev739-head-post git -C "$PREV739" --no-optional-locks rev-parse HEAD || fail "prev739-head-post rc"
grep -q "^409b292756dd1277b9dfae87679934c0d2ce251c$" "$EVIDENCE/prev739-head-post-stdout.txt" || fail "PREV739 HEAD changed"
run recon-head-post git -C "$REPO" --no-optional-locks rev-parse HEAD || fail "recon-head-post rc"
grep -q "^f84fcf5321be3798c862c0156278afbba01f89f6$" "$EVIDENCE/recon-head-post-stdout.txt" || fail "recon HEAD changed"

printf "DONE OK %s DST %s\n" "$STAMP" "$DST" >> "$LOG"
echo "DONE OK"
