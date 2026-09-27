#!/usr/bin/env bash
# Run the parent witness runner against the independent gate-cli DB.
# Writes raw stdout/stderr/exit per witness plus a JSON summary into the packet.
set -euo pipefail

REPO=/tmp/jgas-rephase-gate-cli
PY=/tmp/jgas-rephase-application-venv/bin/python3.12
PACKET=/mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-gate-cli
OUT="$PACKET/logs/parent-witness"
SCRIPT="$PACKET/witness/run_parent_witness.py"

test -x "$PY" || { echo "venv python missing: $PY" >&2; exit 2; }
test -f "$SCRIPT" || { echo "witness script missing: $SCRIPT" >&2; exit 2; }
mkdir -p "$OUT"
cd "$REPO"
set +e
"$PY" "$SCRIPT" "$OUT" 2>&1 | tee "$OUT/run.log"
runner_exit=${PIPESTATUS[0]}
set -e
echo "RUNNER_EXIT=$runner_exit"
exit "$runner_exit"
