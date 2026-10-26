#!/bin/bash
# Weekly-final SOURCE snapshot — explicit complete SOURCE from current candidate (741 intended)
# No product source edits, no tests/build/imports/network/ordinary commits. Read-only guards + byte-independent copy.
# HumanHEAD f84fcf5 expected. SRC candidate-work HEAD 409b292 expected.
set -u
REPO=/home/eariver/git/reconstruct-japanese-generative-ai-survey
SRC=$REPO/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work
STAMP=20261025T235500Z
DSTROOT=$REPO/.rephase-1-editorial-runtime/versioned-renewal-weekly-final-${STAMP}
DST=$DSTROOT/snapshot-work
EVID=$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/source-snapshot-${STAMP}
mkdir -p "$EVID"
exec > "$EVID/commands.log" 2>&1
echo "STAMP $STAMP"
echo "REPO $REPO"
run() { desc="$1"; shift; echo "\$ $* # $desc"; "$@" > "$EVID/$desc-stdout.txt" 2> "$EVID/$desc-stderr.txt"; ec=$?; echo $ec > "$EVID/$desc-exit.txt"; echo "-> exit=$ec"; return $ec; }
# Guards before: reconstruct HEAD, diff-cached, diff HEAD
run recon-head git -C "$REPO" rev-parse HEAD
run recon-status git -C "$REPO" status --porcelain=v1 --untracked-files=no
run recon-diff-cached git -C "$REPO" diff --cached --name-only
run recon-diff-head git -C "$REPO" diff HEAD --name-only
run src-head git --no-optional-locks -C "$SRC" rev-parse HEAD
run src-tree git --no-optional-locks -C "$SRC" rev-parse HEAD^{tree}
run src-status git --no-optional-locks -C "$SRC" status --porcelain=v1 --untracked-files=all
run src-diff-cached git --no-optional-locks -C "$SRC" diff --cached --name-only
run src-diff-head git --no-optional-locks -C "$SRC" diff HEAD --name-only
run src-log git --no-optional-locks -C "$SRC" log --oneline -3
run src-git-count find "$SRC/.git" -type f -print
# Verify parent DSTROOT absent (no overwrite)
if [ -e "$DSTROOT" ]; then echo "DSTROOT exists, refuse overwrite $DSTROOT"; exit 1; fi
echo "parent DSTROOT absent OK"
mkdir -p "$DST"
echo "mkdir DST $DST"
# Copy .git byte-independent (no -l)
run cp-git cp -a "$SRC/.git" "$DST/.git"
run dst-git-count find "$DST/.git" -type f -print
run dst-head git --no-optional-locks -C "$DST" rev-parse HEAD
run dst-tree git --no-optional-locks -C "$DST" rev-parse HEAD^{tree}
run dst-remote git --no-optional-locks -C "$DST" remote -v
run dst-log git --no-optional-locks -C "$DST" log --oneline -3
# Populate worktree manifest-exact via python (no rsync blind, no cache)
python3 - <<'PY'
import pathlib, shutil, hashlib, os, json
repo=pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey")
src=pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work")
dst=pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-weekly-final-20261025T235500Z/snapshot-work")
evid=pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/source-snapshot-20261025T235500Z")
# Enumerate intended: all files excluding .git, __pycache__, *.pyc
intended=[]
for root, dirs, files in os.walk(src):
  if ".git" in pathlib.Path(root).parts:
    continue
  # prune .git, __pycache__
  dirs[:] = [d for d in dirs if d not in (".git","__pycache__")]
  for f in files:
    if f.endswith(".pyc"):
      continue
    p=pathlib.Path(root)/f
    rel=p.relative_to(src)
    # skip __pycache__ residue in path
    if "__pycache__" in rel.parts:
      continue
    intended.append(rel.as_posix())
intended_sorted=sorted(intended)
print(f"intended={len(intended_sorted)}")
open(evid/"intended-list.txt","w").write("\n".join(intended_sorted)+"\n")
# copy
for rel in intended_sorted:
  s=src/rel
  d=dst/rel
  d.parent.mkdir(parents=True, exist_ok=True)
  shutil.copy2(s,d)
print("copy done")
# verify SHA identical SRC==DST
ok=True
rows=[]
for rel in intended_sorted:
  import hashlib as hl
  sb=(src/rel).read_bytes()
  db=(dst/rel).read_bytes()
  hs=hl.sha256(sb).hexdigest()
  hd=hl.sha256(db).hexdigest()
  if hs!=hd:
    print(f"MISMATCH {rel}")
    ok=False
  rows.append(f"{hs}  {len(sb)}  {rel}")
open(evid/"dst-hash-intended.txt","w").write("\n".join(rows)+"\n")
import hashlib as hl2
blob="\n".join(rows)+"\n"
print(f"hash-list-sha={hl2.sha256(blob.encode()).hexdigest()}")
print("SRC_DST_IDENTICAL" if ok else "MISMATCH")
PY
run dst-count find "$DST" -path "$DST/.git" -prune -o -type f -print
run dst-status git --no-optional-locks -C "$DST" status --porcelain=v1 --untracked-files=all
run dst-diff-head git --no-optional-locks -C "$DST" diff HEAD --name-only
run dst-diff-cached git --no-optional-locks -C "$DST" diff --cached --name-only
# Isolation: no alternates, own gitdir, nlink, dev:ino disjoint, no GIT_* leak
run noalternates test '!' -e "$DST/.git/objects/info/alternates"
run gitdir git --no-optional-locks -C "$DST" rev-parse --absolute-git-dir
run config-show git --no-optional-locks -C "$DST" config --list --show-origin
python3 - <<'PY'
import pathlib, os
src=pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work")
dst=pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-weekly-final-20261025T235500Z/snapshot-work")
evid=pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/source-snapshot-20261025T235500Z")
# nlink
bad=[]
for p in (dst/".git").rglob("*"):
  if p.is_file():
    if p.stat().st_nlink!=1:
      bad.append(str(p))
open(evid/"isolation-nlink.txt","w").write(f"nlink_bad={len(bad)}\n"+"\n".join(bad[:20]))
print(f"nlink_bad={len(bad)}")
# dev:ino disjoint
def inos(root):
  s=set()
  for pp in pathlib.Path(root).rglob("*"):
    try:
      st=pp.stat()
      s.add((st.st_dev, st.st_ino))
    except: pass
  return s
sg=inos(str(src/".git")); dg=inos(str(dst/".git"))
print(f"git_inode_overlap={len(sg & dg)}")
open(evid/"isolation-inode.txt","w").write(f"git_inode_overlap={len(sg & dg)}\n")
# worktree disjoint check (sample)
sw=set()
for pp in src.rglob("*"):
  if ".git" in pp.parts: continue
  if "__pycache__" in str(pp): continue
  if pp.suffix==".pyc": continue
  if pp.is_file():
    try: sw.add((pp.stat().st_dev, pp.stat().st_ino))
    except: pass
dw=set()
for pp in dst.rglob("*"):
  if ".git" in pp.parts: continue
  if pp.is_file():
    try: dw.add((pp.stat().st_dev, pp.stat().st_ino))
    except: pass
print(f"worktree_overlap={len(sw & dw)}")
open(evid/"isolation-worktree.txt","w").write(f"worktree_overlap={len(sw & dw)}\n")
print(f"alternates_exists={(dst/'.git/objects/info/alternates').exists()}")
PY
run env-check env
# Pins: exact file hashes for H/S/HIGH/P1/PUB/Reader/edpub/P3S/style
python3 - <<'PY'
import hashlib, pathlib
src=pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work")
evid=pathlib.Path("/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/source-snapshot-20261025T235500Z")
files=["scripts/survey_versioned_renewal_history_v2.py","scripts/survey_versioned_renewal_source_v2.py","scripts/survey_versioned_renewal_v2.py","scripts/survey_editorial_correction_proposal_v2.py","scripts/survey_publication_v2.py","scripts/survey_reader_publication_v2.py","scripts/survey_editorial_publication_v2.py","scripts/survey_editorial_staged_source_v2.py","templates/survey/jgaisurvey.sty"]
rows=[]
for rel in files:
  b=(src/rel).read_bytes()
  h=hashlib.sha256(b).hexdigest()
  rows.append(f"{rel} {len(b)} {h}")
  print(f"{rel} {len(b)} {h}")
open(evid/"source-pins.txt","w").write("\n".join(rows)+"\n")
PY
# Post guards: HEAD same
run src-head-post git --no-optional-locks -C "$SRC" rev-parse HEAD
run recon-head-post git -C "$REPO" rev-parse HEAD
echo "DONE OK $STAMP"
