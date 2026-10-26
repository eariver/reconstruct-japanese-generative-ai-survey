#!/bin/bash
# New isolated baseline + patch snapshot + live tests (no shared candidate writes).
# Saved via Write before execution. No old runners, no network.
set -u
BASE_OP=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-operation-correction-20261025T060000Z
SNAP=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-freeze-20261024T174422Z/snapshot-work
CAND=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work
EVID=/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/resume-20261025/operation-correction
mkdir -p "$BASE_OP/baseline" "$BASE_OP/patched" "$EVID"
echo "copy baseline start" > "$EVID/copy-baseline-stdout.txt"
# Byte-independent copy (no -l/--link, no hardlinks): worktree 731 + .git
cp -a "$SNAP/." "$BASE_OP/baseline/" 2> "$EVID/copy-baseline-stderr.txt"
echo $? > "$EVID/copy-baseline-exit.txt"
# Verify baseline 731 + HEAD 409
python3 -c "import pathlib, hashlib; b=pathlib.Path('$BASE_OP/baseline'); files=[p for p in b.rglob('*') if p.is_file() and '.git' not in p.parts]; print(len(files))" > "$EVID/baseline-count-stdout.txt" 2> "$EVID/baseline-count-stderr.txt"
echo $? > "$EVID/baseline-count-exit.txt"
# Patched = baseline + only owned patch (2 scripts + new test)
cp -a "$BASE_OP/baseline/." "$BASE_OP/patched/" 2> "$EVID/copy-patched-stderr.txt"
echo $? > "$EVID/copy-patched-exit.txt"
cp "$CAND/scripts/survey_versioned_renewal_v2.py" "$BASE_OP/patched/scripts/survey_versioned_renewal_v2.py" 2>> "$EVID/copy-patched-stderr.txt"
cp "$CAND/scripts/survey_publication_v2.py" "$BASE_OP/patched/scripts/survey_publication_v2.py" 2>> "$EVID/copy-patched-stderr.txt"
cp "$CAND/tests/test_versioned_renewal_operation_correction_b1b2b3.py" "$BASE_OP/patched/tests/test_versioned_renewal_operation_correction_b1b2b3.py" 2>> "$EVID/copy-patched-stderr.txt"
sha256sum "$BASE_OP/patched/scripts/survey_versioned_renewal_v2.py" "$BASE_OP/patched/scripts/survey_publication_v2.py" > "$EVID/patched-sha-stdout.txt" 2> "$EVID/patched-sha-stderr.txt"
echo $? > "$EVID/patched-sha-exit.txt"
# AST parse (stdlib, no project import)
python3 -c "import ast, pathlib; ast.parse(pathlib.Path('$BASE_OP/patched/scripts/survey_versioned_renewal_v2.py').read_text()); ast.parse(pathlib.Path('$BASE_OP/patched/scripts/survey_publication_v2.py').read_text()); print('AST OK')" > "$EVID/patched-ast-stdout.txt" 2> "$EVID/patched-ast-stderr.txt"
echo $? > "$EVID/patched-ast-exit.txt"
# Live tests in patched snapshot only, fixture = high24 weekly read-only for B1 exact-path
export RENEWAL_FIXTURE_ROOT=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-high24-20261025T040000Z/renewal-weekly
export PYTHONDONTWRITEBYTECODE=1
cd "$BASE_OP/patched"
python3 -m unittest tests.test_versioned_renewal_operation_correction_b1b2b3 -v > "$EVID/test-live-stdout.txt" 2> "$EVID/test-live-stderr.txt"
echo $? > "$EVID/test-live-exit.txt"
# Static-only run (no fixture) for fault-seam inventory
unset RENEWAL_FIXTURE_ROOT
python3 -m unittest tests.test_versioned_renewal_operation_correction_b1b2b3.TestStaticOperationCorrection -v > "$EVID/test-static-stdout.txt" 2> "$EVID/test-static-stderr.txt"
echo $? > "$EVID/test-static-exit.txt"
cd - > /dev/null
echo "DONE"
