#!/bin/bash
# Affected-regressions runner — fresh child per module, workspace TMPDIR, exact SOURCE pin raw before/after
# Saved BEFORE execution via Write. No product runtime changes, no reconstruct/candidate commits, no network/pip.
# TEST SOURCE: versioned-renewal-affected-regress-20261025T143000Z/test-source (HEAD debd16c9, 740 tracked, 32206 total)
# Runs: new H/S/HIGH/Reader/Freeze/dispatch/archive (96 methods) + existing affected (199 methods). Previous 120 green NOT transferred.
set -u
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
TESTSRC="$REPO/.rephase-1-editorial-runtime/versioned-renewal-affected-regress-20261025T143000Z/test-source"
TMPBASE="$REPO/.rephase-1-editorial-runtime/versioned-renewal-affected-regress-20261025T143000Z/tmp"
EVIDENCE="$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/affected-regressions"
export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C
export TMPDIR="$TMPBASE"

LOG="$EVIDENCE/regress-commands.log"
printf "regress stamp 20261025T143000Z\n" > "$LOG"

run() {
  tag="$1"; shift
  out="$EVIDENCE/${tag}-stdout.txt"
  err="$EVIDENCE/${tag}-stderr.txt"
  rcfile="$EVIDENCE/${tag}-exit.txt"
  env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0 PYTHONDONTWRITEBYTECODE=1 TMPDIR="$TMPBASE" "$@" >"$out" 2>"$err"
  rc=$?
  printf "%s" "$rc" > "$rcfile"
  printf "run %s rc=%s cmd=%s\n" "$tag" "$rc" "$*" >> "$LOG"
  return $rc
}

fail() {
  printf "FAIL %s\n" "$1" >> "$LOG"
  echo "FAIL: $1" >&2
  exit 1
}

[ -d "$TESTSRC/.git" ] || fail "TESTSRC .git missing"
[ -d "$TMPBASE" ] || fail "TMPBASE missing"

run regress-testsrc-head git -C "$TESTSRC" --no-optional-locks rev-parse HEAD || fail "testsrc-head rc"
grep -q "^debd16c9da0e8e533968c2926048b336eadb7070$" "$EVIDENCE/regress-testsrc-head-stdout.txt" || fail "TESTSRC HEAD not debd16c9 (must be TEST-ONLY 740 commit)"
run regress-testsrc-status git -C "$TESTSRC" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "testsrc-status rc"
[ -s "$EVIDENCE/regress-testsrc-status-stdout.txt" ] && fail "TESTSRC not clean before regress"

# Fresh child per module: record pin before, run unittest, record pin after. Timeout per module to avoid hang.
# New renewal tests first (fast, complete-source).
MODULES_NEW="test_editorial_renewal_archive_correction_20261025 test_editorial_renewal_p1_dispatch_20261025 test_versioned_renewal_high_phase test_versioned_renewal_history_phase_h test_versioned_renewal_source_phase_s test_versioned_renewal_reader_f4_20261025 test_versioned_renewal_freeze_transitive_correction_20261025 test_versioned_renewal_history_author_h_20261025 test_versioned_renewal_source_author_s_f1f2f3_20261025 test_versioned_renewal_operation_correction_b1b2b3 test_versioned_renewal_history_perf_batched_20261025 test_versioned_renewal_history_traversal_opt_20261025"
MODULES_EXIST="test_survey_dm004_release_validate_state_v2 test_survey_agent_control_v2 test_survey_publication_set_v2 test_survey_reader_surface_gate_v2 test_survey_quality_v2 test_survey_publication_v2 test_group_c_editorial_consumers_v2 test_survey_stage_validation_v2 test_survey_profiled_freeze_v2 test_survey_editorial_correction_proposal_v2 test_survey_editorial_retention_v2 test_survey_editorial_current_authority_v2 test_survey_editorial_staged_source_v2 test_survey_weekly_mechanical_refresh_v2"

run regress-pin-before git -C "$TESTSRC" --no-optional-locks rev-parse HEAD || fail "pin-before rc"

for mod in $MODULES_NEW $MODULES_EXIST; do
  safe=$(echo "$mod" | tr '.' '_' | tr '/' '_')
  # before pin per module
  git -C "$TESTSRC" --no-optional-locks rev-parse HEAD > "$EVIDENCE/pin-${safe}-before-stdout.txt" 2> "$EVIDENCE/pin-${safe}-before-stderr.txt"; printf "%s" "$?" > "$EVIDENCE/pin-${safe}-before-exit.txt"
  git -C "$TESTSRC" --no-optional-locks status --porcelain=v1 --untracked-files=all > "$EVIDENCE/status-${safe}-before-stdout.txt" 2> "$EVIDENCE/status-${safe}-before-stderr.txt"; printf "%s" "$?" > "$EVIDENCE/status-${safe}-before-exit.txt"
  printf "module %s before HEAD %s\n" "$mod" "$(cat "$EVIDENCE/pin-${safe}-before-stdout.txt")" >> "$LOG"
  # run with timeout 1200s (heavy P3S/R1 may need it), fresh child, workspace TMPDIR, no pip/network
  timeout 1200 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0 PYTHONDONTWRITEBYTECODE=1 TMPDIR="$TMPBASE" PYTHONPATH="$TESTSRC" python3 -m unittest "tests.${mod}" -v > "$EVIDENCE/run-${safe}-stdout.txt" 2> "$EVIDENCE/run-${safe}-stderr.txt"
  rc=$?
  printf "%s" "$rc" > "$EVIDENCE/run-${safe}-exit.txt"
  printf "run %s rc=%s\n" "$mod" "$rc" >> "$LOG"
  # after pin per module
  git -C "$TESTSRC" --no-optional-locks rev-parse HEAD > "$EVIDENCE/pin-${safe}-after-stdout.txt" 2> "$EVIDENCE/pin-${safe}-after-stderr.txt"; printf "%s" "$?" > "$EVIDENCE/pin-${safe}-after-exit.txt"
  git -C "$TESTSRC" --no-optional-locks status --porcelain=v1 --untracked-files=all > "$EVIDENCE/status-${safe}-after-stdout.txt" 2> "$EVIDENCE/status-${safe}-after-stderr.txt"; printf "%s" "$?" > "$EVIDENCE/status-${safe}-after-exit.txt"
  printf "module %s after HEAD %s rc %s\n" "$mod" "$(cat "$EVIDENCE/pin-${safe}-after-stdout.txt")" "$rc" >> "$LOG"
done

run regress-pin-after git -C "$TESTSRC" --no-optional-locks rev-parse HEAD || fail "pin-after rc"
run regress-testsrc-status-after git -C "$TESTSRC" --no-optional-locks status --porcelain=v1 --untracked-files=all || fail "testsrc-status-after rc"

printf "DONE regress\n" >> "$LOG"
