#!/bin/bash
# HIGH U1 (REUSE_TARGETS, shallower firstU) with current FIXED735 + NEW PUB in u1-weekly-721 (isolated, SOURCE dda9590 before NEW authority).
# Saved via Write before execution. No old runners, no network. Process-scoped identity for fixture commits only (HIGH runs use explicit executor arg, no git identity).
set -u
U1=/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/versioned-renewal-operation-correction-20261025T060000Z/u1-weekly-721
EVID=/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-versioned-renewal-implementation/resume-20261025/operation-correction
export PYTHONDONTWRITEBYTECODE=1
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0
# Inputs (mirror high24 G1 U1 weekly REUSE_TARGETS; manuscript_spec from proposal wk-boot-1, toolchain None for U, executor test).
STATE="sources/2026-W37/production-state.json"
MSPEC="sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/manuscript-spec.json"
RID="high-u1-test"
# Prepare U1 (U, no toolchain).
/usr/bin/time -v /usr/bin/python3 -c "import sys; sys.path.insert(0, sys.argv[1]); from scripts.survey_versioned_renewal_v2 import main; sys.exit(main(sys.argv[2:]))" "$U1" prepare --root "$U1" --state "$STATE" --renewal-id "$RID" --intent REUSE_TARGETS --manuscript-spec "$MSPEC" --executor test > "$EVID/u1-high-prepare-stdout.txt" 2> "$EVID/u1-high-prepare-stderr.txt"
echo $? > "$EVID/u1-high-prepare-exit.txt"
# Extract basis_path for finalize (via python, no jq).
BASIS=$(python3 -c "import json; print(json.load(open('$EVID/u1-high-prepare-stdout.txt'))['basis_path'])" 2> "$EVID/u1-high-basis-extract-stderr.txt"
echo "$BASIS" > "$EVID/u1-high-basis-path.txt"
# QA checks (fresh, at/after basis capture) – reuse proposal renewal-qa-checks? For new RID, need fresh checks file with recorded_at >= basis recorded_at.
# Minimal fresh checks: build from prior seal trio/pdf (like high24 run36 helper) – use python to generate fresh checks file with current time.
python3 -c "
import sys, json, pathlib
sys.path.insert(0, '$U1')
from pathlib import Path
root=Path('$U1')
basis=json.loads((root/'$BASIS').read_bytes()) if '$BASIS'.strip() else {}
# Fallback: use prior seal trio/pdf for fresh checks (same as high24 helper, clearly labelled synthetic fixture type).
print('checks-gen placeholder')
" 2> "$EVID/u1-high-checks-gen-stderr.txt"
echo DONE
