#!/bin/bash
# Weekly integration setup — NEW fixture from old R3 baseline + FIXED 736 INPUT G1
# HumanHEAD f84fcf5. No candidate/INPUT/other-route edits. New DB only.
set -u
REPO=/home/eariver/git/reconstruct-japanese-generative-ai-survey
BOOT=$REPO/.rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly
SNAP=$REPO/.rephase-1-editorial-runtime/versioned-renewal-final-input-20261025T051343Z/snapshot-work
STAMP=20261025T052132Z
BASE_OP=$REPO/.rephase-1-editorial-runtime/versioned-renewal-weekly-${STAMP}
FIX=$BASE_OP/renewal-weekly
EVID=$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-integration/setup-${STAMP}
mkdir -p "$EVID"
exec > "$EVID/commands.log" 2>&1
echo "STAMP $STAMP"
echo "REPO HEAD $(git -C $REPO rev-parse HEAD)"
echo "BOOT HEAD $(git -C $BOOT rev-parse HEAD)"
run() { desc="$1"; shift; echo "\$ $* # $desc"; "$@" > "$EVID/$desc-stdout.txt" 2> "$EVID/$desc-stderr.txt"; ec=$?; echo $ec > "$EVID/$desc-exit.txt"; echo "-> exit=$ec"; return $ec; }
# 1. clone byte-independent, no hardlinks
run clone-0 git clone --no-hardlinks "$BOOT" "$FIX"
run remote-0 git -C "$FIX" remote set-url origin https://example.invalid/versioned-renewal-weekly-integration.git
run cfg-user-name git -C "$FIX" config user.name rephase-fixture
run cfg-user-email git -C "$FIX" config user.email fixture@example.invalid
run cfg-gpgsign git -C "$FIX" config commit.gpgsign false
run head-pre git -C "$FIX" rev-parse HEAD
run log-pre git -C "$FIX" log --oneline -3
run status-pre git -C "$FIX" status --porcelain=v1 --untracked-files=all
run gitdir git -C "$FIX" rev-parse --absolute-git-dir
run noalternates test ! -e "$FIX/.git/objects/info/alternates"
run config-show git -C "$FIX" config --list --show-origin
cat "$EVID/config-show-stdout.txt" | grep -i "GIT_\|alternat" || echo "no GIT leak in config"
echo "GIT_DIR=${GIT_DIR:-unset} GIT_WORK_TREE=${GIT_WORK_TREE:-unset} GIT_INDEX_FILE=${GIT_INDEX_FILE:-unset}"
# E manifest capture from BOOT: untracked + ignored
python3 -c "
import subprocess, pathlib
boot=pathlib.Path('$BOOT')
# untracked
p1=subprocess.run(['git','--no-optional-locks','status','--porcelain=v1','--untracked-files=all'],cwd=str(boot),capture_output=True,text=True)
untracked=[l[3:].strip().strip('\"') for l in p1.stdout.splitlines() if l.startswith('?? ')]
# ignored others
p2=subprocess.run(['git','--no-optional-locks','ls-files','--others','--ignored','--exclude-standard'],cwd=str(boot),capture_output=True,text=True)
ignored=[l.strip() for l in p2.stdout.splitlines() if l.strip()]
print(f'untracked={len(untracked)} ignored={len(ignored)}')
open('$EVID/e-manifest-untracked.txt','w').write('\n'.join(sorted(untracked))+'\n')
open('$EVID/e-manifest-ignored.txt','w').write('\n'.join(sorted(ignored))+'\n')
# hash E bytes in BOOT
import hashlib
def h(p):
  return hashlib.sha256((boot/p).read_bytes()).hexdigest() if (boot/p).is_file() else 'MISSING'
rows=[]
for rel in sorted(set(untracked+ignored)):
  rows.append(f'{h(rel)}  {rel}')
open('$EVID/e-hash-boot.txt','w').write('\n'.join(rows)+'\n')
print('E manifest captured')
"
cat "$EVID/e-manifest-untracked.txt" | head -n 5
cat "$EVID/e-manifest-ignored.txt"
wc -l "$EVID/e-manifest-untracked.txt" "$EVID/e-manifest-ignored.txt" "$EVID/e-hash-boot.txt"
# copy exact E including ignored PDF/log by captured manifest, no arbitrary residue
python3 -c "
import pathlib, shutil
boot=pathlib.Path('$BOOT'); dst=pathlib.Path('$FIX')
for fname in ['$EVID/e-manifest-untracked.txt','$EVID/e-manifest-ignored.txt']:
  for line in open(fname):
    rel=line.strip()
    if not rel: continue
    src=boot/rel; d=dst/rel
    if src.is_file():
      d.parent.mkdir(parents=True,exist_ok=True)
      shutil.copy2(src,d)
    elif src.is_dir():
      d.mkdir(parents=True,exist_ok=True)
print('E copy done')
"
# verify E hash unchanged in FIX
python3 -c "
import hashlib, pathlib
fix=pathlib.Path('$FIX')
rows=open('$EVID/e-hash-boot.txt').read().strip().splitlines()
ok=True
for r in rows:
  exp, rel = r.split('  ',1)
  data=(fix/rel).read_bytes() if (fix/rel).is_file() else b'MISSING'
  got=hashlib.sha256(data).hexdigest() if (fix/rel).is_file() else 'MISSING'
  if got!=exp:
    print(f'MISMATCH {rel} exp {exp} got {got}')
    ok=False
print('E_HASH_UNCHANGED' if ok else 'E_HASH_MISMATCH')
open('$EVID/e-hash-verify.txt','w').write('E_HASH_UNCHANGED\n' if ok else 'E_HASH_MISMATCH\n')
"
run status-postE git -C "$FIX" status --porcelain=v1 --untracked-files=all
# isolation: hardlinks, inode sharing, object sharing
python3 -c "
import pathlib, subprocess, os
fix=pathlib.Path('$FIX'); boot=pathlib.Path('$BOOT')
# nlink check for .git files
bad=[]
for p in (fix/'.git').rglob('*'):
  if p.is_file():
    if p.stat().st_nlink!=1:
      bad.append(str(p))
print(f'nlink_bad={len(bad)}')
open('$EVID/isolation-nlink.txt','w').write(f'nlink_bad={len(bad)}\n' + '\n'.join(bad[:20]))
# dev:ino disjoint
def inos(root):
  s=set()
  for p in pathlib.Path(root).rglob('*'):
    try:
      st=p.stat()
      s.add((st.st_dev, st.st_ino))
    except: pass
  return s
fix_git=inos(str(fix/'.git')); boot_git=inos(str(boot/'.git'))
print(f'git_inode_overlap={len(fix_git & boot_git)}')
open('$EVID/isolation-inode.txt','w').write(f'git_inode_overlap={len(fix_git & boot_git)}\n')
# no alternates
import pathlib as pl
print('alternates_exists='+str((fix/'.git/objects/info/alternates').exists()))
"
run head-postE git -C "$FIX" rev-parse HEAD
# overlay EXACT 736 INPUT filenames/modes
python3 -c "
import pathlib, shutil, hashlib, stat
snap=pathlib.Path('$SNAP'); dst=pathlib.Path('$FIX')
lst=[l.strip() for l in open('$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/final-integration-input-evidence-20261025T051343Z/dst-hash-intended-stdout.txt') if l.strip()]
print(f'INPUT_list={len(lst)}')
for line in lst:
  parts=line.split()
  exp_sha, rel = parts[0], parts[2]
  src=snap/rel; d=dst/rel
  if not src.is_file():
    print(f'MISSING_SRC {rel}')
    raise SystemExit(1)
  d.parent.mkdir(parents=True,exist_ok=True)
  shutil.copy2(src,d)
print('overlay copy done')
# verify SRC==DST bytes for 736
ok=True
for line in lst:
  exp_sha, rel = line.split()[0], line.split()[2]
  got=hashlib.sha256((dst/rel).read_bytes()).hexdigest()
  if got!=exp_sha:
    print(f'MISMATCH {rel}')
    ok=False
print('OVERLAY_BYTES_OK' if ok else 'OVERLAY_MISMATCH')
# physical modes: ensure bridge 775 others 664? copy2 already preserves; enforce per manifest rule
bridge=dst/'scripts/survey_core_execution_bridge_v2.py'
print(f'bridge_mode={oct(bridge.stat().st_mode & 0o777)}')
"
run diff-names git -C "$FIX" diff --name-only
run status-overlay git -C "$FIX" status --porcelain=v1 --untracked-files=all
# SOURCE-only add: exact 736 list via git add of those paths (E remains untracked)
python3 -c "
import subprocess
repo='$FIX'
lst=[l.split()[2] for l in open('$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/final-integration-input-evidence-20261025T051343Z/dst-hash-intended-stdout.txt') if l.strip()]
# git add only those 736 (some may be new)
proc=subprocess.run(['git','--no-optional-locks','add','--']+lst, cwd=repo, capture_output=True, text=True)
print(proc.stdout[:2000]); print(proc.stderr[:2000]); print('add rc',proc.returncode)
open('$EVID/add-736-stdout.txt','w').write(proc.stdout)
open('$EVID/add-736-stderr.txt','w').write(proc.stderr)
open('$EVID/add-736-exit.txt','w').write(str(proc.returncode))
"
run diff-cached-names git -C "$FIX" diff --cached --name-only
run status-staged git -C "$FIX" status --porcelain=v1 --untracked-files=all
# verify E still untracked (not staged)
python3 -c "
import subprocess
p=subprocess.run(['git','--no-optional-locks','diff','--cached','--name-only'],cwd='$FIX',capture_output=True,text=True)
staged=set(p.stdout.splitlines())
e_untracked=set([l.strip() for l in open('$EVID/e-manifest-untracked.txt') if l.strip()])
overlap=staged & e_untracked
print(f'staged={len(staged)} overlap_with_E={len(overlap)}')
print(sorted(list(overlap))[:10])
open('$EVID/staged-vs-E.txt','w').write(f'staged={len(staged)} overlap={len(overlap)}\n'+'\n'.join(sorted(overlap)))
"
echo "READY_FOR_G1_COMMIT"
