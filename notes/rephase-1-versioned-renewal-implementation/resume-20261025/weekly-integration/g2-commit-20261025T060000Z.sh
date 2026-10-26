#!/bin/bash
# G2 commit — genuine eligible Core + style comment (semantic unchanged)
set -u
REPO=/home/eariver/git/reconstruct-japanese-generative-ai-survey
STAMP=20261025T052132Z
FIX=$REPO/.rephase-1-editorial-runtime/versioned-renewal-weekly-${STAMP}/renewal-weekly
EVID_STEP=$(ls -d $REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-integration/step1-* | head -n 1)
EVID=$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-integration/g2-commit-20261025T060000Z
mkdir -p "$EVID"
exec >> "$EVID/commands.log" 2>&1
echo "=== G2 commit ==="
run() { desc="$1"; shift; echo "\$ $* # $desc"; "$@" > "$EVID/$desc-stdout.txt" 2> "$EVID/$desc-stderr.txt"; ec=$?; echo $ec > "$EVID/$desc-exit.txt"; echo "-> exit=$ec"; return $ec; }
run head-g2-pre git -C "$FIX" rev-parse HEAD
run status-g2-pre git -C "$FIX" status --porcelain=v1 --untracked-files=all
run diff-g2-pre git -C "$FIX" diff --name-only
# verify style bytes changed, contract same (schemas unchanged)
python3 -c "import hashlib, pathlib; p=pathlib.Path('$FIX/templates/survey/jgaisurvey.sty'); print(hashlib.sha256(p.read_bytes()).hexdigest(), len(p.read_bytes()))" > "$EVID/style-g2-sha-stdout.txt" 2> "$EVID/style-g2-sha-stderr.txt"; echo $? > "$EVID/style-g2-sha-exit.txt"
cat "$EVID/style-g2-sha-stdout.txt"
run add-g2 git -C "$FIX" add -- templates/survey/jgaisurvey.sty scripts/survey_weekly_derivation_v2.py
run status-staged-g2 git -C "$FIX" status --porcelain=v1 --untracked-files=all
run commit-g2 git -C "$FIX" commit -m "HIGH phase TEST-ONLY: G2 eligible Core+style comment (semantic unchanged, trio change for C)" --no-verify
run head-g2-post git -C "$FIX" rev-parse HEAD
run log-g2 git -C "$FIX" log --oneline -6
run tree-g2 git -C "$FIX" rev-parse HEAD^{tree}
run ancestor-g2 git -C "$FIX" merge-base --is-ancestor 721a04d85532d7855f3e54cc411f5847c787726e HEAD
# HIGH blob at G2 (should differ from G1 due to Core comment)
python3 -c "import hashlib, pathlib; p=pathlib.Path('$FIX/scripts/survey_versioned_renewal_v2.py'); print(hashlib.sha256(p.read_bytes()).hexdigest())" > "$EVID/high-g2-sha-stdout.txt" 2> "$EVID/high-g2-sha-stderr.txt"; echo $? > "$EVID/high-g2-sha-exit.txt"
cat "$EVID/high-g2-sha-stdout.txt"
# tool file changed sha
python3 -c "import hashlib, pathlib; p=pathlib.Path('$FIX/scripts/survey_weekly_derivation_v2.py'); print(hashlib.sha256(p.read_bytes()).hexdigest())" > "$EVID/tool-g2-sha-stdout.txt" 2> "$EVID/tool-g2-sha-stderr.txt"; echo $? > "$EVID/tool-g2-sha-exit.txt"
echo "G2 DONE"
