#!/bin/bash
# Continuation setup — NEW independent copy of valid prePreview r5 (6141dad) + overlay 739 G5 (preserve a4bd style)
set -u
REPO=/home/eariver/git/reconstruct-japanese-generative-ai-survey
OLD=$REPO/.rephase-1-editorial-runtime/versioned-renewal-weekly-20261025T052132Z/renewal-weekly
SNAP=$REPO/.rephase-1-editorial-runtime/versioned-renewal-repair-input-20261025T082826Z/snapshot-work
STAMP=20261025T083000Z
BASE_OP=$REPO/.rephase-1-editorial-runtime/versioned-renewal-weekly-continuation-${STAMP}
FIX=$BASE_OP/renewal-weekly
EVID=$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-integration/continuation-setup-${STAMP}
mkdir -p "$EVID"
exec > "$EVID/commands.log" 2>&1
echo "STAMP $STAMP OLD_HEAD $(git -C $OLD rev-parse HEAD)"
run() { desc="$1"; shift; echo "\$ $* # $desc"; "$@" > "$EVID/$desc-stdout.txt" 2> "$EVID/$desc-stderr.txt"; ec=$?; echo $ec > "$EVID/$desc-exit.txt"; echo "-> exit=$ec"; return $ec; }
# 1. clone tracked history byte-independent, no hardlinks
run clone-0 git clone --no-hardlinks "$OLD" "$FIX"
run remote-0 git -C "$FIX" remote set-url origin https://example.invalid/versioned-renewal-weekly-continuation.git
run cfg-user-name git -C "$FIX" config user.name rephase-fixture
run cfg-user-email git -C "$FIX" config user.email fixture@example.invalid
run cfg-gpgsign git -C "$FIX" config commit.gpgsign false
run head-pre git -C "$FIX" rev-parse HEAD
run log-pre git -C "$FIX" log --oneline -12
run gitdir git -C "$FIX" rev-parse --absolute-git-dir
run noalternates test ! -e "$FIX/.git/objects/info/alternates"
run config-show git -C "$FIX" config --list --show-origin
echo "GIT_DIR=${GIT_DIR:-unset} GIT_WORK_TREE=${GIT_WORK_TREE:-unset} GIT_INDEX_FILE=${GIT_INDEX_FILE:-unset}"
# E + renewals manifest from OLD (untracked + ignored)
python3 -c "
import subprocess, pathlib
old=pathlib.Path('$OLD')
p1=subprocess.run(['git','--no-optional-locks','status','--porcelain=v1','--untracked-files=all'],cwd=str(old),capture_output=True,text=True)
untracked=[l[3:].strip().strip('\"') for l in p1.stdout.splitlines() if l.startswith('?? ')]
p2=subprocess.run(['git','--no-optional-locks','ls-files','--others','--ignored','--exclude-standard'],cwd=str(old),capture_output=True,text=True)
ignored=[l.strip() for l in p2.stdout.splitlines() if l.strip()]
print(f'untracked={len(untracked)} ignored={len(ignored)}')
open('$EVID/e-manifest-untracked.txt','w').write('\n'.join(sorted(untracked))+'\n')
open('$EVID/e-manifest-ignored.txt','w').write('\n'.join(sorted(ignored))+'\n')
import hashlib
def h(p):
  return hashlib.sha256((old/p).read_bytes()).hexdigest() if (old/p).is_file() else 'MISSING'
rows=[]
for rel in sorted(set(untracked+ignored)):
  rows.append(f'{h(rel)}  {rel}')
open('$EVID/e-hash-old.txt','w').write('\n'.join(rows)+'\n')
print('E manifest captured')
"
cat "$EVID/e-manifest-ignored.txt"
wc -l "$EVID/e-manifest-untracked.txt" "$EVID/e-manifest-ignored.txt"
# copy exact E including ignored + renewals by manifest
python3 -c "
import pathlib, shutil
old=pathlib.Path('$OLD'); dst=pathlib.Path('$FIX')
for fname in ['$EVID/e-manifest-untracked.txt','$EVID/e-manifest-ignored.txt']:
  for line in open(fname):
    rel=line.strip()
    if not rel: continue
    src=old/rel; d=dst/rel
    if src.is_file():
      d.parent.mkdir(parents=True,exist_ok=True)
      shutil.copy2(src,d)
    elif src.is_dir():
      d.mkdir(parents=True,exist_ok=True)
print('E copy done')
"
python3 -c "
import hashlib, pathlib
old=pathlib.Path('$OLD'); fix=pathlib.Path('$FIX')
rows=open('$EVID/e-hash-old.txt').read().strip().splitlines()
ok=True
for r in rows:
  exp, rel = r.split('  ',1)
  got=hashlib.sha256((fix/rel).read_bytes()).hexdigest() if (fix/rel).is_file() else 'MISSING'
  if got!=exp:
    print(f'MISMATCH {rel}')
    ok=False
print('E_HASH_UNCHANGED' if ok else 'E_MISMATCH')
open('$EVID/e-hash-verify.txt','w').write('E_HASH_UNCHANGED\n' if ok else 'E_MISMATCH\n')
"
run status-postE git -C "$FIX" status --porcelain=v1 --untracked-files=all
python3 -c "
import pathlib
fix=pathlib.Path('$FIX'); old=pathlib.Path('$OLD')
bad=[str(p) for p in (fix/'.git').rglob('*') if p.is_file() and p.stat().st_nlink!=1]
print(f'nlink_bad={len(bad)}')
open('$EVID/isolation-nlink.txt','w').write(f'nlink_bad={len(bad)}\n')
def inos(root):
  s=set()
  for p in pathlib.Path(root).rglob('*'):
    try: st=p.stat(); s.add((st.st_dev,st.st_ino))
    except: pass
  return s
print(f'git_inode_overlap={len(inos(str(fix/\".git\")) & inos(str(old/\".git\")))}')
open('$EVID/isolation-inode.txt','w').write(f'git_inode_overlap={len(inos(str(fix/\".git\")) & inos(str(old/\".git\")))}\n')
print('alternates_exists='+str((fix/'.git/objects/info/alternates').exists()))
"
run head-postE git -C "$FIX" rev-parse HEAD
# overlay 739 except style variant (preserve a4bd...)
python3 -c "
import pathlib, shutil, hashlib
snap=pathlib.Path('$SNAP'); dst=pathlib.Path('$FIX')
lst=[l.strip() for l in open('$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/integration-repair-input-evidence-20261025T082826Z/dst-hash-intended-stdout.txt') if l.strip()]
print(f'INPUT_list={len(lst)}')
style_rel='templates/survey/jgaisurvey.sty'
old_style=hashlib.sha256((dst/style_rel).read_bytes()).hexdigest()
print(f'preserve_style_before={old_style}')
assert old_style=='a4bd135aa2876079923ba925f16cc2963c73647e49a3f1460806483d9c092827', 'must be G2 variant a4bd'
for line in lst:
  parts=line.split()
  exp_sha, rel = parts[0], parts[2]
  if rel==style_rel:
    print(f'SKIP style {rel} (preserve a4bd variant)')
    continue
  src=snap/rel; d=dst/rel
  if not src.is_file():
    print(f'MISSING_SRC {rel}'); raise SystemExit(1)
  d.parent.mkdir(parents=True,exist_ok=True)
  shutil.copy2(src,d)
print('overlay copy done (except style)')
# verify 738 bytes (excluding style) + style preserved
ok=True
for line in lst:
  exp_sha, rel = line.split()[0], line.split()[2]
  if rel==style_rel: continue
  got=hashlib.sha256((dst/rel).read_bytes()).hexdigest()
  if got!=exp_sha:
    print(f'MISMATCH {rel}'); ok=False
print('OVERLAY_738_OK' if ok else 'OVERLAY_MISMATCH')
print(f'style_after={hashlib.sha256((dst/style_rel).read_bytes()).hexdigest()}')
"
run diff-names git -C "$FIX" diff --name-only
run status-overlay git -C "$FIX" status --porcelain=v1 --untracked-files=all
# SOURCE-only add: 739 list minus style (plus style already tracked? style unchanged, so not staged)
python3 -c "
import subprocess
lst=[l.split()[2] for l in open('$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/integration-repair-input-evidence-20261025T082826Z/dst-hash-intended-stdout.txt') if l.strip()]
lst=[p for p in lst if p!='templates/survey/jgaisurvey.sty']
proc=subprocess.run(['git','--no-optional-locks','add','--']+lst, cwd='$FIX', capture_output=True, text=True)
print(proc.stdout[:1000]); print(proc.stderr[:1000]); print('add rc',proc.returncode)
open('$EVID/add-739-stdout.txt','w').write(proc.stdout)
open('$EVID/add-739-stderr.txt','w').write(proc.stderr)
open('$EVID/add-739-exit.txt','w').write(str(proc.returncode))
"
run diff-cached-names git -C "$FIX" diff --cached --name-only
run status-staged git -C "$FIX" status --porcelain=v1 --untracked-files=all
python3 -c "
import subprocess
p=subprocess.run(['git','--no-optional-locks','diff','--cached','--name-only'],cwd='$FIX',capture_output=True,text=True)
staged=set(p.stdout.splitlines())
e_untracked=set([l.strip() for l in open('$EVID/e-manifest-untracked.txt') if l.strip()])
print(f'staged={len(staged)} overlap_E={len(staged & e_untracked)}')
open('$EVID/staged-vs-E.txt','w').write(f'staged={len(staged)} overlap={len(staged & e_untracked)}\n')
"
echo "READY_FOR_G5_COMMIT"
