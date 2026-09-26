#!/usr/bin/env bash
set -u

fixture=/tmp/jgas-rephase-increment-b-sol-implementation
packet=/mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-increment-b
expected=cb96ab97045b0d0767f38806809d33e383bac73d
actual=$(git -C "$fixture" rev-parse HEAD)
if [ "$actual" != "$expected" ]; then
  printf 'Fixture HEAD changed: expected %s, found %s\n' "$expected" "$actual" > "$packet/focused-migration.log"
  printf '91\n' > "$packet/focused-migration.exit"
  exit 91
fi

cd "$fixture" || exit 92
/tmp/jgas-rephase-application-venv/bin/python3.12 -m unittest -v \
  tests.test_survey_bibliography_access_provenance_v2 \
  tests.test_survey_weekly_evidence_authority_v2 \
  > "$packet/focused-migration.log" 2>&1
result=$?
printf '%s\n' "$result" > "$packet/focused-migration.exit"
exit "$result"
