#!/usr/bin/env bash
# Generate final B-to-successor patch + changed-file byte copies and print the
# exact values needed for candidate.json / implementation-report.md.
# Shell copy is used for exact byte fidelity; every copied byte is verified
# against the committed Git blob.
set -euo pipefail

DB=/tmp/jgas-rephase-gate-cli
PACKET=/mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-gate-cli
BASE=c04f32ad46109403e8a63faaa8394a90ee6b869c
SUCC=e4c82692abee6acedbba07815b0d74ccefb80a7e
RUNTIME=scripts/survey_reader_surface_gate_v2.py
NEWTEST=tests/test_survey_gate_cli_persisted_review_v2.py
LOG="$PACKET/logs/candidate-relevant-tests-e4c8269.log"

cd "$DB"
test "$(git rev-parse HEAD)" = "$SUCC"

rm -rf "$PACKET/changed-files"
mkdir -p "$PACKET/changed-files/scripts" "$PACKET/changed-files/tests"
git diff --no-color "$BASE" "$SUCC" -- "$RUNTIME" "$NEWTEST" > "$PACKET/increment-gate-cli.patch"
cp "$DB/$RUNTIME" "$PACKET/changed-files/scripts/survey_reader_surface_gate_v2.py"
cp "$DB/$NEWTEST" "$PACKET/changed-files/tests/test_survey_gate_cli_persisted_review_v2.py"

echo "HEAD=$(git rev-parse "$SUCC")"
echo "TREE=$(git rev-parse "$SUCC^{tree}")"
echo "PARENT=$(git rev-parse "$SUCC^")"
echo "PATCH_SHA256=$(sha256sum "$PACKET/increment-gate-cli.patch" | cut -d' ' -f1)"
echo "PATCH_BYTES=$(wc -c < "$PACKET/increment-gate-cli.patch")"
for path in "$RUNTIME" "$NEWTEST"; do
  blob=$(git rev-parse "$SUCC:$path")
  disk_hash=$(git hash-object "$PACKET/changed-files/$path")
  test "$blob" = "$disk_hash"
  echo "FILE $path blob=$blob sha256=$(sha256sum "$PACKET/changed-files/$path" | cut -d' ' -f1) bytes=$(wc -c < "$PACKET/changed-files/$path")"
done
echo "RUNTIME_UNCHANGED_VS_6d87edd=$( [ "$(git rev-parse "$SUCC:$RUNTIME")" = "$(git rev-parse 6d87edd:$RUNTIME)" ] && echo yes || echo no )"
echo "SUBTEST_BLOCKS=$(grep -c 'with self.subTest(' "$NEWTEST")"
echo "LOG_SHA256=$(sha256sum "$LOG" | cut -d' ' -f1)"
echo "LOG_EXIT=$(cat "$PACKET/logs/candidate-relevant-tests-e4c8269.exit")"
grep -E '^Ran |^OK|^FAILED' "$LOG"
echo "FINAL_ARTIFACTS_OK"
