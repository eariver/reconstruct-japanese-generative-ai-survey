#!/usr/bin/env bash
# Run the observational findings-transport probe against the fixture DB.
# Append-only: writes a new uniquely-named probe output under logs/.
set -euo pipefail

REPO=/tmp/jgas-rephase-gate-cli
PY=/tmp/jgas-rephase-application-venv/bin/python3.12
PACKET=/mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-gate-cli
OUT="$PACKET/logs/findings-transport-probe-20260927T1"
SCRIPT="$PACKET/witness/run_findings_transport_probe.py"

test -x "$PY" || { echo "venv python missing: $PY" >&2; exit 2; }
test -f "$SCRIPT" || { echo "probe script missing: $SCRIPT" >&2; exit 2; }
mkdir -p "$OUT"
cd "$REPO"
"$PY" "$SCRIPT" "$OUT" 2>&1 | tee "$OUT/run.log"
echo "PROBE_EXIT=${PIPESTATUS[0]}"
