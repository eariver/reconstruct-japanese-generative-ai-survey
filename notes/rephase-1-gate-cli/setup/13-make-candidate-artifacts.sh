#!/usr/bin/env bash
# Generate B-to-successor patch and changed-file byte copies for the packet.
# Shell copy is used for exact byte fidelity; every copied byte is verified
# against the committed Git blob and recorded by sha256.
set -euo pipefail

DB=/tmp/jgas-rephase-gate-cli
PACKET=/mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-gate-cli
BASE=c04f32ad46109403e8a63faaa8394a90ee6b869c
SUCC=6d87edd28a1be8893ca2ab67fed6e32e54b0de6c
RUNTIME=scripts/survey_reader_surface_gate_v2.py
NEWTEST=tests/test_survey_gate_cli_persisted_review_v2.py

cd "$DB"
test "$(git rev-parse HEAD)" = "$SUCC"

mkdir -p "$PACKET/changed-files/scripts" "$PACKET/changed-files/tests"

git diff --no-color "$BASE" "$SUCC" -- "$RUNTIME" "$NEWTEST" > "$PACKET/increment-gate-cli.patch"
cp "$DB/$RUNTIME" "$PACKET/changed-files/scripts/survey_reader_surface_gate_v2.py"
cp "$DB/$NEWTEST" "$PACKET/changed-files/tests/test_survey_gate_cli_persisted_review_v2.py"

echo "== patch =="
sha256sum "$PACKET/increment-gate-cli.patch"
wc -c < "$PACKET/increment-gate-cli.patch"

echo "== changed file byte verification (disk copy vs committed blob) =="
for path in "$RUNTIME" "$NEWTEST"; do
  blob=$(git rev-parse "$SUCC:$path")
  disk_hash=$(git hash-object "$PACKET/changed-files/$path")
  echo "$path blob=$blob disk_object=$disk_hash"
  test "$blob" = "$disk_hash"
  sha256sum "$PACKET/changed-files/$path"
done
echo "ARTIFACTS_OK"
