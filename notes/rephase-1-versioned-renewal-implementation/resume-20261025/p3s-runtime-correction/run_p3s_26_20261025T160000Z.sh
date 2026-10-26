#!/bin/bash
# P3S original-26 run on NEW isolated complete SOURCE db (WITH fix), workspace TMPDIR.
# Saved BEFORE execution via Write. Fail-closed: set -u only, explicit rc.
# Per-module bounded 1200s, guard PID genuine child status, no filtered pass.
# No network/old runners/cleanup. Raw saved as parent controls.
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

LOG="$EVID/commands-26.log"
printf "stamp 20261025T160000Z-26 original-26 on NEW SOURCE WITH fix, TMPDIR workspace\n" > "$LOG"

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

# Source pins before/after (HEAD must stay same, clean)
run pin-before git -C "$DST" --no-optional-locks rev-parse HEAD || exit 1
run status-before git -C "$DST" --no-optional-locks status --porcelain=v1 --untracked-files=all || exit 1

# Original 26: full module, timeout 1200s (bounded, genuine child status)
# Use timeout(1) as guard; timeout exit 124 on timeout (genuine, not filtered PASS)
run p3s-26 timeout --preserve-status --signal=TERM --kill-after=10 1200 python3 -m unittest tests.test_survey_editorial_staged_source_v2 -v || true
# Do NOT fail here on test failures; save raw as parent controls (exit may be 1)

run pin-after git -C "$DST" --no-optional-locks rev-parse HEAD || exit 1
run status-after git -C "$DST" --no-optional-locks status --porcelain=v1 --untracked-files=all || exit 1

printf "DONE 26 rc=%s (see p3s-26-exit.txt; test failures preserved as parent controls)\n" "$(cat "$EVID/p3s-26-exit.txt")" >> "$LOG"
cat "$LOG"
