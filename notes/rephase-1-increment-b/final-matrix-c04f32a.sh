#!/usr/bin/env bash
set -u
fixture=/tmp/jgas-rephase-increment-b-sol-implementation
packet=/mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-increment-b
expected=c04f32ad46109403e8a63faaa8394a90ee6b869c
log="$packet/final-matrix-c04f32a.log"
exitfile="$packet/final-matrix-c04f32a.exit"
exec > "$log" 2>&1
for name in GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_COMMON_DIR; do
  if printenv "$name" >/dev/null 2>&1; then
    printf 'Unsafe inherited Git override: %s\n' "$name"
    printf '98\n' > "$exitfile"
    exit 98
  fi
done
cd "$fixture" || { printf '92\n' > "$exitfile"; exit 92; }
actual=$(git rev-parse HEAD)
printf 'HEAD=%s\nTREE=%s\nPARENT=%s\n' "$actual" "$(git rev-parse HEAD^{tree})" "$(git rev-parse HEAD^)"
if [ "$actual" != "$expected" ]; then
  printf 'Fixture HEAD changed; expected %s\n' "$expected"
  printf '91\n' > "$exitfile"
  exit 91
fi
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
  printf 'Tracked fixture changes before fixed-head matrix\n'
  git status --short
  printf '90\n' > "$exitfile"
  exit 90
fi
/tmp/jgas-rephase-application-venv/bin/python3.12 --version
/tmp/jgas-rephase-application-venv/bin/python3.12 -m pip show jsonschema pypdf | grep -E '^(Name|Version):'
sha256sum scripts/survey_weekly_derivation_v2.py scripts/survey_weekly_semantic_publication_v2.py tests/test_survey_increment_b_weekly_derivation_v2.py tests/test_survey_increment_b_boundary_matrix_v2.py tests/test_survey_bibliography_access_provenance_v2.py tests/test_survey_weekly_evidence_authority_v2.py
printf 'TEST_COMMAND=/tmp/jgas-rephase-application-venv/bin/python3.12 -m unittest -v [14 explicit modules]\n'
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
  tests.test_survey_weekly_evidence_authority_v2
result=$?
printf '%s\n' "$result" > "$exitfile"
printf 'MATRIX_EXIT=%s\n' "$result"
exit "$result"