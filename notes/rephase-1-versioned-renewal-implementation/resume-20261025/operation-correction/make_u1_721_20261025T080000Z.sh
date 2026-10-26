# U1 fixture fix — correct ancestry 721a04d (preserve wrong 409b292 attempt as failure).
# Previous u1-weekly has HEAD 409b292 (COMBINED .git overwrote bootstrap .git) – WRONG, preserved as failure (do NOT delete).
# Correct: bootstrap .git (721a04d, inert) + COMBINED worktree EXCLUDING .git + oldE (untracked live/COPY) + writable PUB comprehensive fix, then SOURCE commit ONLY code before NEW authority.
set -u
BASE_OP=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-operation-correction-20261025T060000Z
BOOT=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly
COMBINED=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-combined-freeze-20261025T041436Z/snapshot-work
CAND=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work
EVID=/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/resume-20261025/operation-correction
U1F=$BASE_OP/u1-weekly-721
mkdir -p "$U1F"
# .git from BOOT only (721a04d, inert, no alternates).
cp -a "$BOOT/.git" "$U1F/.git" 2> "$EVID/u1-721-git-stderr.txt"
echo $? > "$EVID/u1-721-git-exit.txt"
# Worktree: COMBINED files EXCLUDING .git (use python to exclude .git, no rsync blind, no hardlinks).
python3 -c "
import pathlib, shutil
src=pathlib.Path('$COMBINED')
dst=pathlib.Path('$U1F')
for p in src.rglob('*'):
    if '.git' in p.parts:
        continue
    rel=p.relative_to(src)
    d=dst/rel
    if p.is_dir():
        d.mkdir(parents=True, exist_ok=True)
    elif p.is_file():
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, d)
print('combined worktree copy done (excl .git)')
" 2>> "$EVID/u1-721-git-stderr.txt"
# OldE untracked live/COPY from BOOT (preserve, NOT committed) – same as before, exclude .git.
python3 -c "
import subprocess, pathlib, shutil
boot=pathlib.Path('$BOOT')
u1=pathlib.Path('$U1F')
proc=subprocess.run(['git','--no-optional-locks','status','--porcelain=v1','--untracked-files=all'], cwd=str(boot), capture_output=True, text=True)
for line in proc.stdout.splitlines():
    if line.startswith('?? '):
        rel=line[3:].strip().strip('\"')
        src=boot/rel
        dst=u1/rel
        if src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
print('oldE copy done')
" 2>> "$EVID/u1-721-git-stderr.txt"
# Owned PUB comprehensive fix (HIGH unchanged) + new test (for fixture-local run).
cp "$CAND/scripts/survey_publication_v2.py" "$U1F/scripts/survey_publication_v2.py" 2>> "$EVID/u1-721-git-stderr.txt"
cp "$CAND/scripts/survey_versioned_renewal_v2.py" "$U1F/scripts/survey_versioned_renewal_v2.py" 2>> "$EVID/u1-721-git-stderr.txt"
cp "$CAND/tests/test_versioned_renewal_operation_correction_b1b2b3.py" "$U1F/tests/test_versioned_renewal_operation_correction_b1b2b3.py" 2>> "$EVID/u1-721-git-stderr.txt"
git -C "$U1F" rev-parse HEAD > "$EVID/u1-721-head-stdout.txt" 2> "$EVID/u1-721-head-stderr.txt"
echo $? > "$EVID/u1-721-head-exit.txt"
git -C "$U1F" remote -v > "$EVID/u1-721-remote-stdout.txt" 2> "$EVID/u1-721-remote-stderr.txt"
echo DONE
