#!/bin/bash
# G4 commit — impl-only, style unchanged
set -u
REPO=/home/eariver/git/reconstruct-japanese-generative-ai-survey
FIX=$REPO/.rephase-1-editorial-runtime/versioned-renewal-weekly-20261025T052132Z/renewal-weekly
EVID=$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-integration/g4-commit-20261025T073000Z
mkdir -p "$EVID"
exec >> "$EVID/commands.log" 2>&1
echo "=== G4 commit ==="
run() { desc="$1"; shift; echo "\$ $* # $desc"; "$@" > "$EVID/$desc-stdout.txt" 2> "$EVID/$desc-stderr.txt"; ec=$?; echo $ec > "$EVID/$desc-exit.txt"; echo "-> exit=$ec"; return $ec; }
run head-g4-pre git -C "$FIX" rev-parse HEAD
python3 -c "import hashlib, pathlib; print(hashlib.sha256(pathlib.Path('$FIX/templates/survey/jgaisurvey.sty').read_bytes()).hexdigest())" > "$EVID/style-g4-check-stdout.txt" 2> "$EVID/style-g4-check-stderr.txt"; echo $? > "$EVID/style-g4-check-exit.txt"
cat "$EVID/style-g4-check-stdout.txt"
run add-g4 git -C "$FIX" add -- scripts/survey_versioned_renewal_source_v2.py
run commit-g4 git -C "$FIX" commit -m "HIGH phase TEST-ONLY: G4 impl-only Core comment (style unchanged, eligible)" --no-verify
run head-g4-post git -C "$FIX" rev-parse HEAD
run log-g4 git -C "$FIX" log --oneline -9
echo "G4 DONE"
