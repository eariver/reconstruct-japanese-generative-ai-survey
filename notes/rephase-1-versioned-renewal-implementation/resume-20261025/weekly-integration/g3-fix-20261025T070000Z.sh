#!/bin/bash
# G3 fix — correct docstring (previous G3 broke syntax, preserved as failure)
set -u
REPO=/home/eariver/git/reconstruct-japanese-generative-ai-survey
FIX=$REPO/.rephase-1-editorial-runtime/versioned-renewal-weekly-20261025T052132Z/renewal-weekly
EVID=$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-integration/g3-fix-20261025T070000Z
mkdir -p "$EVID"
exec >> "$EVID/commands.log" 2>&1
echo "=== G3 fix ==="
run() { desc="$1"; shift; echo "\$ $* # $desc"; "$@" > "$EVID/$desc-stdout.txt" 2> "$EVID/$desc-stderr.txt"; ec=$?; echo $ec > "$EVID/$desc-exit.txt"; echo "-> exit=$ec"; return $ec; }
run head-pre git -C "$FIX" rev-parse HEAD
python3 -c "import ast; ast.parse(open('$FIX/scripts/survey_versioned_renewal_history_v2.py').read()); print('parse ok')" > "$EVID/parse-fix-stdout.txt" 2> "$EVID/parse-fix-stderr.txt"; echo $? > "$EVID/parse-fix-exit.txt"
cat "$EVID/parse-fix-stdout.txt"
run add-fix git -C "$FIX" add -- scripts/survey_versioned_renewal_history_v2.py
run commit-fix git -C "$FIX" commit -m "HIGH phase TEST-ONLY: G3 fix docstring (previous G3 syntax fail preserved, this corrects)" --no-verify
run head-post git -C "$FIX" rev-parse HEAD
run log-fix git -C "$FIX" log --oneline -8
echo "G3 FIX DONE"
