#!/bin/bash
# New firstU (U1) fixture with current FIXED735 + NEW PUB comprehensive fix, for public Freeze.
# Saved via Write before execution. No old runners, no network.
# Steps: clone REAL old bootstrap 721a04d+oldE, overlay COMBINED 735 + writable PUB fix, SOURCE commit ONLY code before NEW authority (preserve old tool ancestry).
set -u
BASE_OP=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-operation-correction-20261025T060000Z
BOOT=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/bootstrap-weekly
COMBINED=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-combined-freeze-20261025T041436Z/snapshot-work
CAND=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work
EVID=/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/resume-20261025/operation-correction
U1=$BASE_OP/u1-weekly
mkdir -p "$U1" "$EVID"
echo "u1 fixture start" > "$EVID/u1-fixture-stdout.txt"
# 1. Byte-independent .git copy (no -l, no hardlinks) from REAL old bootstrap (721a04d, inert origin).
cp -a "$BOOT/.git" "$U1/.git" 2> "$EVID/u1-fixture-stderr.txt"
echo $? > "$EVID/u1-fixture-git-exit.txt"
# 2. Populate worktree: COMBINED 735 (FIXED, read-only) + oldE from BOOT (untracked live/COPY, NOT committed) + writable PUB comprehensive fix (owned only).
cp -a "$COMBINED/." "$U1/" 2>> "$EVID/u1-fixture-stderr.txt"
echo $? >> "$EVID/u1-fixture-git-exit.txt"
# Overlay oldE untracked (live/COPY, preserve, NOT required at tool commit) – copy untracked files from BOOT (excluding .git).
python3 -c "
import subprocess, pathlib
boot=pathlib.Path('$BOOT')
u1=pathlib.Path('$U1')
# List untracked files in BOOT (oldE) via git status (read-only, no mutation).
proc=subprocess.run(['git','--no-optional-locks','status','--porcelain=v1','--untracked-files=all'], cwd=str(boot), capture_output=True, text=True)
for line in proc.stdout.splitlines():
    if line.startswith('?? '):
        rel=line[3:].strip().strip('\"')
        src=boot/rel
        dst=u1/rel
        if src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            import shutil
            shutil.copy2(src, dst)
print('oldE copy done')
" 2>> "$EVID/u1-fixture-stderr.txt"
# Overlay writable PUB comprehensive fix (owned only, HIGH unchanged) + new test (for fixture-local run? Actually fixture needs code to run HIGH – use writable candidate scripts).
cp "$CAND/scripts/survey_publication_v2.py" "$U1/scripts/survey_publication_v2.py" 2>> "$EVID/u1-fixture-stderr.txt"
cp "$CAND/scripts/survey_versioned_renewal_v2.py" "$U1/scripts/survey_versioned_renewal_v2.py" 2>> "$EVID/u1-fixture-stderr.txt"
cp "$CAND/tests/test_versioned_renewal_operation_correction_b1b2b3.py" "$U1/tests/test_versioned_renewal_operation_correction_b1b2b3.py" 2>> "$EVID/u1-fixture-stderr.txt"
# 3. Verify isolation (own .git, no alternates, inert origin, no hardlinks) + counts.
git -C "$U1" rev-parse HEAD > "$EVID/u1-fixture-head-stdout.txt" 2> "$EVID/u1-fixture-head-stderr.txt"
echo $? > "$EVID/u1-fixture-head-exit.txt"
git -C "$U1" status --porcelain=v1 --untracked-files=all | head -n 30 > "$EVID/u1-fixture-status-stdout.txt" 2> "$EVID/u1-fixture-status-stderr.txt"
echo DONE
