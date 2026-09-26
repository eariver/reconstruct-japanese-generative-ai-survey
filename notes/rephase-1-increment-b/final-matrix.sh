#!/usr/bin/env bash
set -u

fixture=/tmp/jgas-rephase-increment-b-sol-implementation
packet=/mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-increment-b
expected=cb96ab97045b0d0767f38806809d33e383bac73d
actual=$(git -C "$fixture" rev-parse HEAD)
if [ "$actual" != "$expected" ]; then
  printf 'Fixture HEAD changed: expected %s, found %s\n' "$expected" "$actual" > "$packet/final-matrix.log"
  printf '91\n' > "$packet/final-matrix.exit"
  exit 91
fi

cd "$fixture" || exit 92
/tmp/jgas-rephase-application-venv/bin/python3.12 -m unittest -v \
  tests.test_survey_increment_b_weekly_derivation_v2 \
  tests.test_survey_increment_b_boundary_matrix_v2 \
  tests.test_survey_reader_surface_gate_v2 \
  tests.test_survey_semantic_publication_v2 \
  tests.test_survey_exact_manuscript_admission_v2 \
  tests.test_survey_publication_revalidation_v2 \
  tests.test_survey_human_gate_revalidation_revision_v2 \
  tests.test_survey_agent_tool_v2 \
  tests.test_survey_agent_control_v2 \
  tests.test_survey_stage_validation_v2 \
  tests.test_survey_freeze_stage_boundary_v2 \
  tests.test_survey_interactive_drafting_cross_package_refs_v2 \
  tests.test_survey_bibliography_access_provenance_v2 \
  tests.test_survey_weekly_evidence_authority_v2 \
  > "$packet/final-matrix.log" 2>&1
result=$?
printf '%s\n' "$result" > "$packet/final-matrix.exit"
exit "$result"
