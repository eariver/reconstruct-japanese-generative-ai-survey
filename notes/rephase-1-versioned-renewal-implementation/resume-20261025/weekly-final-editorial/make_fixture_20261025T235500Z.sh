#!/bin/bash
# Weekly-final SHORT fixture — NEW independent clone DB + exact E incl ignored PDF/log + overlay 741 current + G1 SOURCE commit
# No rewind of old failed wk-ed5, no cleanup, no network/old runners, no reconstruct/candidate commits.
set -u
REPO=/home/eariver/git/reconstruct-japanese-generative-ai-survey
BOOT=$REPO/.rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly
SNAP=$REPO/.rephase-1-editorial-runtime/versioned-renewal-weekly-final-20261025T235500Z/snapshot-work
STAMP=20261025T235500Z
BASE_OP=$REPO/.rephase-1-editorial-runtime/versioned-renewal-weekly-final-${STAMP}
FIX=$BASE_OP/renewal-weekly-final
EVID=$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/fixture-${STAMP}
mkdir -p "$EVID"
exec > "$EVID/commands.log" 2>&1
echo "STAMP $STAMP"
echo "REPO HEAD $(git -C $REPO rev-parse HEAD)"
echo "BOOT HEAD $(git --no-optional-locks -C $BOOT rev-parse HEAD)"
echo "SNAP HEAD $(git --no-optional-locks -C $SNAP rev-parse HEAD)"
run() { desc="$1"; shift; echo "\$ $* # $desc"; "$@" > "$EVID/$desc-stdout.txt" 2> "$EVID/$desc-stderr.txt"; ec=$?; echo $ec > "$EVID/$desc-exit.txt"; echo "-> exit=$ec"; return $ec; }
# Verify no overwrite (FIX absent, snapshot-work preserved)
if [ -e "$FIX" ]; then echo "FIX exists, refuse $FIX"; exit 1; fi
echo "parent FIX absent OK, snapshot-work preserved"
# 1. clone byte-independent, no hardlinks
run clone-0 git clone --no-hardlinks "$BOOT" "$FIX"
run remote-0 git -C "$FIX" remote set-url origin https://example.invalid/versioned-renewal-weekly-final.git
run cfg-user-name git -C "$FIX" config user.name rephase-fixture
run cfg-user-email git -C "$FIX" config user.email fixture@example.invalid
run cfg-gpgsign git -C "$FIX" config commit.gpgsign false
run head-pre git -C "$FIX" rev-parse HEAD
run log-pre git -C "$FIX" log --oneline -5
run status-pre git -C "$FIX" status --porcelain=v1 --untracked-files=all
run gitdir git -C "$FIX" rev-parse --absolute-git-dir
run noalternates test '!' -e "$FIX/.git/objects/info/alternates"
run config-show git -C "$FIX" config --list --show-origin
echo "GIT_DIR=${GIT_DIR:-unset} GIT_WORK_TREE=${GIT_WORK_TREE:-unset} GIT_INDEX_FILE=${GIT_INDEX_FILE:-unset}"
# E manifest from BOOT: untracked + ignored
python3 -c "
import subprocess, pathlib
boot=pathlib.Path('$BOOT')
p1=subprocess.run(['git','--no-optional-locks','status','--porcelain=v1','--untracked-files=all'],cwd=str(boot),capture_output=True,text=True)
untracked=[l[3:].strip().strip('\"') for l in p1.stdout.splitlines() if l.startswith('?? ')]
p2=subprocess.run(['git','--no-optional-locks','ls-files','--others','--ignored','--exclude-standard'],cwd=str(boot),capture_output=True,text=True)
ignored=[l.strip() for l in p2.stdout.splitlines() if l.strip()]
print(f'untracked={len(untracked)} ignored={len(ignored)}')
open('$EVID/e-manifest-untracked.txt','w').write('\n'.join(sorted(untracked))+'\n')
open('$EVID/e-manifest-ignored.txt','w').write('\n'.join(sorted(ignored))+'\n')
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
# copy exact E incl ignored PDF/log
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
# isolation checks
python3 -c "
import pathlib
fix=pathlib.Path('$FIX'); boot=pathlib.Path('$BOOT')
bad=[]
for p in (fix/'.git').rglob('*'):
  if p.is_file():
    if p.stat().st_nlink!=1:
      bad.append(str(p))
print(f'nlink_bad={len(bad)}')
open('$EVID/isolation-nlink.txt','w').write(f'nlink_bad={len(bad)}\n' + '\n'.join(bad[:20]))
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
print('alternates_exists='+str((fix/'.git/objects/info/alternates').exists()))
"
run head-postE git -C "$FIX" rev-parse HEAD
# overlay EXACT 741 SNAP filenames/modes
python3 -c "
import pathlib, shutil, hashlib
snap=pathlib.Path('$SNAP'); dst=pathlib.Path('$FIX')
lst=[l.strip() for l in open('$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/source-snapshot-20261025T235500Z/intended-list.txt') if l.strip()]
print(f'INPUT_list={len(lst)}')
for rel in lst:
  src=snap/rel; d=dst/rel
  if not src.is_file():
    print(f'MISSING_SRC {rel}')
    raise SystemExit(1)
  d.parent.mkdir(parents=True,exist_ok=True)
  shutil.copy2(src,d)
print('overlay copy done')
ok=True
for rel in lst:
  exp=open('$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/source-snapshot-20261025T235500Z/dst-hash-intended.txt').read()
  # parse expected from snapshot hash file (format: sha bytes rel)
  pass
# verify SRC==DST via snapshot pins
import hashlib as hl
exp_map={}
for line in open('$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/source-snapshot-20261025T235500Z/dst-hash-intended.txt'):
  parts=line.strip().split()
  if len(parts)>=3:
    exp_map[parts[2]]=parts[0]
for rel in lst:
  got=hl.sha256((dst/rel).read_bytes()).hexdigest()
  if got!=exp_map.get(rel):
    print(f'MISMATCH {rel}')
    ok=False
print('OVERLAY_BYTES_OK' if ok else 'OVERLAY_MISMATCH')
bridge=dst/'scripts/survey_core_execution_bridge_v2.py'
print(f'bridge_mode={oct(bridge.stat().st_mode & 0o777)}')
"
run diff-names git -C "$FIX" diff --name-only
run status-overlay git -C "$FIX" status --porcelain=v1 --untracked-files=all
# SOURCE-only add: exact 741 list (E remains untracked)
python3 -c "
import subprocess
repo='$FIX'
lst=[l.strip() for l in open('$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/source-snapshot-20261025T235500Z/intended-list.txt') if l.strip()]
proc=subprocess.run(['git','--no-optional-locks','add','--']+lst, cwd=repo, capture_output=True, text=True)
print(proc.stdout[:2000]); print(proc.stderr[:2000]); print('add rc',proc.returncode)
open('$EVID/add-741-stdout.txt','w').write(proc.stdout)
open('$EVID/add-741-stderr.txt','w').write(proc.stderr)
open('$EVID/add-741-exit.txt','w').write(str(proc.returncode))
"
run diff-cached-names git -C "$FIX" diff --cached --name-only
run status-staged git -C "$FIX" status --porcelain=v1 --untracked-files=all
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
# style baseline check: 035 unchanged matches old trio
python3 -c "
import hashlib, pathlib
fix=pathlib.Path('$FIX')
cur=(fix/'templates/survey/jgaisurvey.sty').read_bytes()
print(f'cur_style {len(cur)} {hashlib.sha256(cur).hexdigest()}')
old=(fix/'surveys/weekly/2026-W37/jgaisurvey.sty').read_bytes() if (fix/'surveys/weekly/2026-W37/jgaisurvey.sty').is_file() else b''
# old trio style is retained before? Check wk-boot-1 retained before
import pathlib as pl
ret=fix/'sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/retained/before/surveys/weekly/2026-W37/jgaisurvey.sty'
if ret.is_file():
  rb=ret.read_bytes()
  print(f'retained_style {len(rb)} {hashlib.sha256(rb).hexdigest()}')
  print('STYLE_MATCH' if cur==rb else 'STYLE_MISMATCH')
else:
  print('retained missing')
"
# G1 SOURCE commit (E untracked, no deletion) — message meaningful, before authority
run add-check git -C "$FIX" diff --cached --stat
run commit-g1 git -C "$FIX" commit -m TEST-ONLY-complete-741-SOURCE-weekly-final-style035
run head-g1 git -C "$FIX" rev-parse HEAD
run log-g1 git -C "$FIX" log --oneline -5
run ancestor-check git -C "$FIX" merge-base --is-ancestor 721a04d85532d7855f3e54cc411f5847c787726e HEAD
run tree-g1 git -C "$FIX" rev-parse HEAD^{tree}
run status-g1 git -C "$FIX" status --porcelain=v1 --untracked-files=all
echo "READY_FOR_RENEWAL"
