#!/usr/bin/env bash
# Fingerprint the committed successor and candidate-test log for candidate.json.
set -uo pipefail
DB=/tmp/jgas-rephase-gate-cli
P=/mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-gate-cli
SUCC=6d87edd28a1be8893ca2ab67fed6e32e54b0de6c
RUNTIME=scripts/survey_reader_surface_gate_v2.py
NEWTEST=tests/test_survey_gate_cli_persisted_review_v2.py

cd "$DB" || exit 2
echo "HEAD=$(git rev-parse "$SUCC")"
echo "TREE=$(git rev-parse "$SUCC^{tree}")"
echo "PARENT=$(git rev-parse "$SUCC^")"
echo "BLOB_RUNTIME=$(git rev-parse "$SUCC:$RUNTIME")"
echo "BLOB_NEWTEST=$(git rev-parse "$SUCC:$NEWTEST")"
echo "RUNTIME_BYTES=$(wc -c < "$RUNTIME")"
echo "NEWTEST_BYTES=$(wc -c < "$NEWTEST")"
echo "RUNTIME_SHA256=$(sha256sum "$RUNTIME" | cut -d' ' -f1)"
echo "NEWTEST_SHA256=$(sha256sum "$NEWTEST" | cut -d' ' -f1)"
echo "PATCH_SHA256=$(sha256sum "$P/increment-gate-cli.patch" | cut -d' ' -f1)"
echo "PATCH_BYTES=$(wc -c < "$P/increment-gate-cli.patch")"
echo "CANDLOG_SHA256=$(sha256sum "$P/logs/candidate-relevant-tests-6d87edd.log" | cut -d' ' -f1)"
echo "CANDEXIT=$(cat "$P/logs/candidate-relevant-tests-6d87edd.exit")"
echo "OK_LINES=$(grep -c '\.\.\. ok' "$P/logs/candidate-relevant-tests-6d87edd.log")"
grep -E '^Ran |^OK|^FAILED' "$P/logs/candidate-relevant-tests-6d87edd.log"
