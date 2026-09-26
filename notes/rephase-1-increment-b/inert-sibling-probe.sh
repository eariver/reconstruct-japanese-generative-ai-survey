#!/usr/bin/env bash
set -u

fixture=/tmp/jgas-rephase-increment-b-sol-implementation
packet=/mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-increment-b
expected=cb96ab97045b0d0767f38806809d33e383bac73d
actual=$(git -C "$fixture" rev-parse HEAD)
if [ "$actual" != "$expected" ]; then
  printf 'Fixture HEAD changed: expected %s, found %s\n' "$expected" "$actual" > "$packet/inert-sibling-probe.log"
  printf '91\n' > "$packet/inert-sibling-probe.exit"
  exit 91
fi

cd "$fixture" || exit 92
/tmp/jgas-rephase-application-venv/bin/python3.12 -m unittest -v \
  tests.test_survey_increment_b_weekly_derivation_v2.IncrementBWeeklyDerivationV2Tests.test_accepted_weekly_two_pass_publication \
  > "$packet/inert-sibling-probe.log" 2>&1
result=$?
printf '%s\n' "$result" > "$packet/inert-sibling-probe.exit"
exit "$result"
