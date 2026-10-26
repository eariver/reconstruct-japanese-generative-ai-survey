#!/bin/bash
# HIGH U1 finalize (U, REUSE_TARGETS, fresh QA, reuse predecessor reviews) + activate with current FIXED735 in u1-weekly-721.
# Saved via Write before execution. No old runners, no network.
set -u
U1=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-operation-correction-20261025T060000Z/u1-weekly-721
EVID=/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/resume-20261025/operation-correction
export PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0
STATE="sources/2026-W37/production-state.json"
BASIS="sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-u1-test/renewal-basis.json"
# Generate fresh QA checks (at/after basis capture, clearly labelled synthetic fixture type for test; genuine in production).
/usr/bin/python3 /home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/resume-20261025/operation-correction/gen_u1_qa_20261025T084500Z.py "$U1" "$BASIS" "sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-u1-test/qa-checks.json" 2> "$EVID/u1-high-qa-gen-stderr.txt" > "$EVID/u1-high-qa-gen-stdout.txt"
echo $? > "$EVID/u1-high-qa-gen-exit.txt"
CHECKS="sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-u1-test/qa-checks.json"
# Finalize U1 (U reuses predecessor reviews, so semantic/visual None).
/usr/bin/time -v /usr/bin/python3 -c "import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; sys.exit(main(sys.argv[2:]))" "$U1" finalize --root "$U1" --state "$STATE" --basis "$BASIS" --checks "$CHECKS" --executor test > "$EVID/u1-high-finalize-stdout.txt" 2> "$EVID/u1-high-finalize-stderr.txt"
echo $? > "$EVID/u1-high-finalize-exit.txt"
python3 /home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/resume-20261025/operation-correction/extract_set_20261025T084500Z.py "$EVID/u1-high-finalize-stdout.txt" "$EVID/u1-high-set-path.txt" 2> "$EVID/u1-high-set-extract-stderr.txt"
echo $? > "$EVID/u1-high-set-extract-exit.txt"
SET=$(cat "$EVID/u1-high-set-path.txt")
# Activate U1 (truthful Core-change reason for test fixture type only).
/usr/bin/time -v /usr/bin/python3 -c "import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; sys.exit(main(sys.argv[2:]))" "$U1" activate --root "$U1" --state "$STATE" --set "$SET" --reason "test U1 Core renewal (fixture type only, synthetic)" --executor test > "$EVID/u1-high-activate-stdout.txt" 2> "$EVID/u1-high-activate-stderr.txt"
echo $? > "$EVID/u1-high-activate-exit.txt"
echo DONE
