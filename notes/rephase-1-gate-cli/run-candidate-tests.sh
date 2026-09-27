#!/usr/bin/env bash
# Committed-candidate relevant-test run for the Gate CLI unit.
# Scope: 27 existing Gate methods + 5 dedicated CLI methods (generated connection included).
# Do NOT run the full historical matrix.
#
# WARNING: this script OVERWRITES its fixed-named log/exit. It is NOT a safe
# re-run stability check. For any new attempt, change LOG/EXITFILE to a new
# unique attempt name first, or copy this script under attempts/.
#
# Correct invocation (absolute WSL path; do not rely on a relative current cwd):
#   wsl -d Ubuntu -- bash /mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-gate-cli/run-candidate-tests.sh
set -u

DB=/tmp/jgas-rephase-gate-cli
PACKET=/mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-gate-cli
PY=/tmp/jgas-rephase-application-venv/bin/python3.12
EXPECTED=e4c82692abee6acedbba07815b0d74ccefb80a7e
LOG="$PACKET/logs/candidate-relevant-tests-e4c8269.log"
EXITFILE="$PACKET/logs/candidate-relevant-tests-e4c8269.exit"

for name in GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_COMMON_DIR; do
  if printenv "$name" >/dev/null 2>&1; then
    echo "unsafe inherited Git override: $name"
    echo 98 > "$EXITFILE"
    exit 98
  fi
done

cd "$DB" || { echo 92 > "$EXITFILE"; exit 92; }

{
  echo "COMMAND=$PY -m unittest -v tests.test_survey_reader_surface_gate_v2 tests.test_survey_gate_cli_persisted_review_v2"
  echo "CWD=$DB"
  echo "HEAD=$(git rev-parse HEAD)"
  echo "TREE=$(git rev-parse HEAD^{tree})"
  echo "PARENT=$(git rev-parse HEAD^)"
  actual=$(git rev-parse HEAD)
  if [ "$actual" != "$EXPECTED" ]; then
    echo "FIXTURE HEAD CHANGED: expected $EXPECTED"
  fi
  if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    echo "TRACKED WORKTREE DIRTY"
    git status --short
  fi
  "$PY" - <<'PYEOF'
import importlib.metadata as md
import os
import sys

print(f"python={sys.version.split()[0]} executable={sys.executable}")
print(f"process_cwd={os.getcwd()}")
for name in (
    "jsonschema",
    "pypdf",
    "attrs",
    "rpds-py",
    "referencing",
    "jsonschema-specifications",
    "typing-extensions",
):
    try:
        print(f"dep {name}={md.version(name)}")
    except Exception as exc:  # noqa: BLE001 - record unavailability explicitly
        print(f"dep {name}=UNAVAILABLE ({exc})")
PYEOF
  "$PY" -m unittest -v \
    tests.test_survey_reader_surface_gate_v2 \
    tests.test_survey_gate_cli_persisted_review_v2
} > "$LOG" 2>&1
result=$?
cat "$LOG"
echo "$result" > "$EXITFILE"
echo "CANDIDATE_TEST_EXIT=$result"
exit "$result"
