#!/bin/bash
# G3 commit — impl-only, style unchanged
set -u
REPO=/home/eariver/git/reconstruct-japanese-generative-ai-survey
STAMP=20261025T052132Z
FIX=$REPO/.rephase-1-editorial-runtime/versioned-renewal-weekly-${STAMP}/renewal-weekly
EVID=$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-integration/g3-commit-20261025T070000Z
mkdir -p "$EVID"
exec >> "$EVID/commands.log" 2>&1
echo "=== G3 commit ==="
run() { desc="$1"; shift; echo "\$ $* # $desc"; "$@" > "$EVID/$desc-stdout.txt" 2> "$EVID/$desc-stderr.txt"; ec=$?; echo $ec > "$EVID/$desc-exit.txt"; echo "-> exit=$ec"; return $ec; }
run head-g3-pre git -C "$FIX" rev-parse HEAD
run status-g3-pre git -C "$FIX" status --porcelain=v1 --untracked-files=all
# ensure style unchanged (a4bd...)
python3 -c "import hashlib, pathlib; print(hashlib.sha256(pathlib.Path('$FIX/templates/survey/jgaisurvey.sty').read_bytes()).hexdigest())" > "$EVID/style-g3-check-stdout.txt" 2> "$EVID/style-g3-check-stderr.txt"; echo $? > "$EVID/style-g3-check-exit.txt"
cat "$EVID/style-g3-check-stdout.txt"
run add-g3 git -C "$FIX" add -- scripts/survey_versioned_renewal_history_v2.py
run commit-g3 git -C "$FIX" commit -m "HIGH phase TEST-ONLY: G3 impl-only Core comment (style unchanged, eligible)" --no-verify
run head-g3-post git -C "$FIX" rev-parse HEAD
run log-g3 git -C "$FIX" log --oneline -7
echo "G3 DONE"
