#!/bin/bash
# P3S remaining-8 run on NEW SOURCE (WITH fix), workspace TMPDIR. Preserves 1200s timeout raw.
# Saved BEFORE execution via Write. Fail-closed: set -u only, explicit rc.
set -u
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
DST="$REPO/.rephase-1-editorial-runtime/versioned-renewal-p3s-runtime-20261025T160000Z/test-source"
TMPBASE="$REPO/.rephase-1-editorial-runtime/versioned-renewal-p3s-runtime-20261025T160000Z/tmp"
EVID="$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/p3s-runtime-correction"
export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C
export TMPDIR="$TMPBASE"
export P3S_DURABLE_OUTDIR="$TMPBASE/p3s-durable"
mkdir -p "$TMPBASE/p3s-durable"

LOG="$EVID/commands-remaining8.log"
printf "stamp 20261025T160000Z-remaining8 on NEW SOURCE WITH fix\n" > "$LOG"

run() {
  tag="$1"; shift
  out="$EVID/${tag}-stdout.txt"
  err="$EVID/${tag}-stderr.txt"
  rcfile="$EVID/${tag}-exit.txt"
  env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0 PYTHONDONTWRITEBYTECODE=1 TMPDIR="$TMPBASE" P3S_DURABLE_OUTDIR="$TMPBASE/p3s-durable" "$@" >"$out" 2>"$err"
  rc=$?
  printf "%s" "$rc" > "$rcfile"
  printf "run %s rc=%s cmd=%s pid_guard=%s\n" "$tag" "$rc" "$*" "$$" >> "$LOG"
  return $rc
}

run pin-before-8 git -C "$DST" --no-optional-locks rev-parse HEAD || exit 1
# Remaining 8 not covered in first 1200s run (o4,o5,o6a,o6b,o7,o8,o9,r1)
run p3s-remaining8 timeout --preserve-status --signal=TERM --kill-after=10 1200 python3 -m unittest -v \
  tests.test_survey_editorial_staged_source_v2.EditorialStagedSourceV2Tests.test_o4_live_state_mutation_replay_ok_materializer_refuses \
  tests.test_survey_editorial_staged_source_v2.EditorialStagedSourceV2Tests.test_o5_artifact_only_head_independence \
  tests.test_survey_editorial_staged_source_v2.EditorialStagedSourceV2Tests.test_o6a_tool_drift_reaches_check \
  tests.test_survey_editorial_staged_source_v2.EditorialStagedSourceV2Tests.test_o6b_keep_drift_preempts_honestly \
  tests.test_survey_editorial_staged_source_v2.EditorialStagedSourceV2Tests.test_o7_scope_refusals \
  tests.test_survey_editorial_staged_source_v2.EditorialStagedSourceV2Tests.test_o8_path_ref_schema_inventory_tamper \
  tests.test_survey_editorial_staged_source_v2.EditorialStagedSourceV2Tests.test_o9_alias_fifo_no_read \
  tests.test_survey_editorial_staged_source_v2.EditorialStagedSourceV2Tests.test_r1_genuine_owner_binds_materialization || true

run pin-after-8 git -C "$DST" --no-optional-locks rev-parse HEAD || exit 1
run status-after-8 git -C "$DST" --no-optional-locks status --porcelain=v1 --untracked-files=all || exit 1

printf "DONE remaining8 rc=%s\n" "$(cat "$EVID/p3s-remaining8-exit.txt")" >> "$LOG"
cat "$LOG"
