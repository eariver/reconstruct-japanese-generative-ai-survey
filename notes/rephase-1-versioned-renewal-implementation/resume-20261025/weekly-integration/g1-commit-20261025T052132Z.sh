#!/bin/bash
# G1 SOURCE commit — BEFORE any renewal authority
set -u
REPO=/home/eariver/git/reconstruct-japanese-generative-ai-survey
STAMP=20261025T052132Z
BASE_OP=$REPO/.rephase-1-editorial-runtime/versioned-renewal-weekly-${STAMP}
FIX=$BASE_OP/renewal-weekly
EVID=$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-integration/setup-${STAMP}
exec >> "$EVID/commands.log" 2>&1
echo "=== G1 commit ==="
run() { desc="$1"; shift; echo "\$ $* # $desc"; "$@" > "$EVID/$desc-stdout.txt" 2> "$EVID/$desc-stderr.txt"; ec=$?; echo $ec > "$EVID/$desc-exit.txt"; echo "-> exit=$ec"; return $ec; }
run head-g1-pre git -C "$FIX" rev-parse HEAD
run log-g1-pre git -C "$FIX" log --oneline -3
run status-g1-pre git -C "$FIX" status --porcelain=v1 --untracked-files=all
# commit SOURCE-only (47 staged, E untracked)
run commit-g1 git -C "$FIX" commit -m "HIGH phase TEST-ONLY: G1 base FIXED 736 INPUT (weekly integration, SOURCE-only before renewal)" --no-verify
run head-g1-post git -C "$FIX" rev-parse HEAD
run log-g1-post git -C "$FIX" log --oneline -5
run tree-g1-post git -C "$FIX" rev-parse HEAD^{tree}
run ancestor-g1 git -C "$FIX" merge-base --is-ancestor 721a04d85532d7855f3e54cc411f5847c787726e HEAD
run status-g1-post git -C "$FIX" status --porcelain=v1 --untracked-files=all
# HIGH blob at G1
python3 -c "
import hashlib, pathlib
p=pathlib.Path('$FIX/scripts/survey_versioned_renewal_v2.py')
h=hashlib.sha256(p.read_bytes()).hexdigest()
print(f'{h}  {len(p.read_bytes())}B')
open('$EVID/high-g1-sha.txt','w').write(h+'\n')
"
run show-g1-stat git -C "$FIX" show --stat --oneline HEAD
echo "G1 DONE"
