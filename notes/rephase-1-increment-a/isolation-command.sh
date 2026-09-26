set -eu
cd /tmp/jgas-rephase-increment-a-sol-copy
echo CANDIDATE_IDENTITY
git rev-parse HEAD^{commit} HEAD^{tree} HEAD^
git show -s --format=%H%n%T%n%P%n%an%n%ae%n%s HEAD
echo STATUS
git status --short
echo REMOTE
git remote -v
echo ALTERNATES
if test -f .git/objects/info/alternates; then cat .git/objects/info/alternates; else echo NO_ALTERNATES; fi
echo INHERITED_GIT_ENV
env | grep -E '^(GIT_DIR|GIT_WORK_TREE|GIT_OBJECT_DIRECTORY|GIT_ALTERNATE_OBJECT_DIRECTORIES|GIT_INDEX_FILE|GIT_COMMON_DIR)=' || echo NONE
echo LINKCOUNT_GT_1
find .git/objects -type f -links +1 -printf '%h %i %p\n' | head -20
echo ORIGIN_CONFIG
git config --get remote.origin.url
git config --get remote.origin.promisor || true
git config --get extensions.partialclone || true
echo RUNTIME
/tmp/jgas-rephase-application-venv/bin/python --version
/tmp/jgas-rephase-application-venv/bin/python - <<'PY'
import jsonschema,pypdf,sys
print('executable='+sys.executable)
print('jsonschema='+jsonschema.__version__)
print('pypdf='+pypdf.__version__)
PY
echo CANDIDATE_HASHES
sha256sum scripts/survey_agent_control_v2.py scripts/survey_reader_surface_gate_v2.py scripts/survey_stage_validation_v2.py tests/test_survey_exact_manuscript_admission_v2.py
echo PARENT_IDENTITY
cd /tmp/jgas-rephase-increment-a-parent-witness
git rev-parse HEAD^{commit} HEAD^{tree} HEAD^
git status --short
git remote -v
if test -f .git/objects/info/alternates; then cat .git/objects/info/alternates; else echo NO_ALTERNATES; fi
echo PARENT_LINKCOUNT_GT_1
find .git/objects -type f -links +1 -printf '%h %i %p\n' | head -20
echo ORIGINAL_F1_IDENTITY_AND_HASHES
cd /tmp/jgas-rephase-freeze-b1b2
git rev-parse HEAD^{commit} HEAD^{tree} HEAD^
sha256sum docs/survey-production-core-v2-authority.md docs/survey-production-core-v2-execution-record-policy.md docs/survey-production-core-v2-redesign-authority.md docs/survey-production-core-v2-session-bootstrap.md scripts/survey_execution_record_v2.py scripts/survey_stage_validation_v2.py tests/test_survey_findings_v2.py tests/test_survey_freeze_stage_boundary_v2.py
git status --short
