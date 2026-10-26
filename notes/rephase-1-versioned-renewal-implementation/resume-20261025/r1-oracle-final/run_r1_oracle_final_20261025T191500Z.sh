#!/bin/bash
# Run ONLY tightened pointer + one healthy R1 control in DST snapshot (no shared candidate execution).
# Workspace TMPDIR, no network/old runners/cleanup/candidate-or-reconstruct commit.
set -u
export LC_ALL=C
export PYTHONDONTWRITEBYTECODE=1
export GIT_NO_LAZY_FETCH=1
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_OPTIONAL_LOCKS=0
RECON="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
DST_BASE="$RECON/.rephase-1-editorial-runtime/versioned-renewal-r1-oracle-final-20261025T191500Z"
DST="$DST_BASE/snapshot-work"
TMPWS="$DST_BASE/tmp"
EVID="$RECON/notes/rephase-1-versioned-renewal-implementation/resume-20261025/r1-oracle-final"
LOG="$EVID/commands.log"
run_test() {
  name="$1"; shift
  # Single unittest method in DST, workspace TMPDIR, PYTHONPATH=DST, cwd=DST.
  TMPDIR="$TMPWS" PYTHONPATH="$DST" /usr/bin/python3 -m unittest -v "$@" >"$EVID/$name-stdout.txt" 2>"$EVID/$name-stderr.txt"
  rc=$?
  echo "$rc" > "$EVID/$name-exit.txt"
  printf "run %s rc=%s cmd=TMPDIR=%s PYTHONPATH=%s /usr/bin/python3 -m unittest -v %s (cwd=%s)\n" "$name" "$rc" "$TMPWS" "$DST" "$*" "$DST" >> "$LOG"
  return $rc
}
# Pin DST source before authorities (post-commit HEAD, test hash, latexmkrc).
git --no-optional-locks -C "$DST" rev-parse HEAD >"$EVID/authority-dst-head-stdout.txt" 2>"$EVID/authority-dst-head-stderr.txt"; echo "$?" > "$EVID/authority-dst-head-exit.txt"
sha256sum "$DST/tests/test_survey_weekly_mechanical_refresh_v2.py" >"$EVID/authority-dst-test-sha-stdout.txt" 2>"$EVID/authority-dst-test-sha-stderr.txt"; echo "$?" > "$EVID/authority-dst-test-sha-exit.txt"
sha256sum "$DST/.latexmkrc" >"$EVID/authority-dst-latexmkrc-stdout.txt" 2>"$EVID/authority-dst-latexmkrc-stderr.txt"; echo "$?" > "$EVID/authority-dst-latexmkrc-exit.txt"
printf "run authority-dst-head rc=%s cmd=git -C DST rev-parse HEAD\n" "$(cat "$EVID/authority-dst-head-exit.txt")" >> "$LOG"
printf "run authority-dst-test-sha rc=%s cmd=sha256sum DST test file\n" "$(cat "$EVID/authority-dst-test-sha-exit.txt")" >> "$LOG"
printf "run authority-dst-latexmkrc rc=%s cmd=sha256sum DST .latexmkrc\n" "$(cat "$EVID/authority-dst-latexmkrc-exit.txt")" >> "$LOG"
# Change to DST for no shared candidate execution (subshell per test).
(cd "$DST" && run_test test-malformed-old-authority-refused tests.test_survey_weekly_mechanical_refresh_v2.WeeklyMechanicalRefreshV2Tests.test_malformed_old_authority_refused)
rc1=$(cat "$EVID/test-malformed-old-authority-refused-exit.txt")
(cd "$DST" && run_test test-first-and-repeat-success tests.test_survey_weekly_mechanical_refresh_v2.WeeklyMechanicalRefreshV2Tests.test_first_and_repeat_success)
rc2=$(cat "$EVID/test-first-and-repeat-success-exit.txt")
echo "DONE 2-METHOD RUN malformed=$rc1 healthy=$rc2"
exit 0
