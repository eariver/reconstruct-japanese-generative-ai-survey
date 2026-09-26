#!/usr/bin/env bash
set -u
cd /tmp/jgas-rephase-increment-b-sol-implementation || exit 99
for name in GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_COMMON_DIR; do
  if [[ -n "${!name:-}" ]]; then printf 'Unsafe Git override: %s\n' "$name"; exit 98; fi
done
printf 'HEAD=%s\n' "$(git rev-parse HEAD)"
printf 'TREE=%s\n' "$(git rev-parse HEAD^{tree})"
/tmp/jgas-rephase-application-venv/bin/python3.12 --version
sha256sum scripts/survey_weekly_derivation_v2.py scripts/survey_weekly_semantic_publication_v2.py tests/test_survey_increment_b_weekly_derivation_v2.py
printf 'STATUS_BEGIN\n'
git status --short
printf 'STATUS_END\n'
/tmp/jgas-rephase-application-venv/bin/python3.12 -m unittest -v tests.test_survey_increment_b_weekly_derivation_v2.IncrementBWeeklyDerivationV2Tests.test_accepted_weekly_two_pass_publication