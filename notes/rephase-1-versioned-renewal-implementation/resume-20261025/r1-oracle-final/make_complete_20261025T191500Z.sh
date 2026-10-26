#!/bin/bash
# Second SOURCE-ONLY commit (complete 741 now tracked) BEFORE successful authorities.
# Preserves prior failed 2-method runs as failure disclosure (no cleanup).
# No runtime edits beyond existing 39M (already in SRC); only tracking untracked intended.
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
EVID="$RECON/notes/rephase-1-versioned-renewal-implementation/resume-20261025/r1-oracle-final"
LOG="$EVID/commands.log"
run() {
  name="$1"; shift
  "$@" >"$EVID/$name-stdout.txt" 2>"$EVID/$name-stderr.txt"
  rc=$?
  echo "$rc" > "$EVID/$name-exit.txt"
  printf "run %s rc=%s cmd=" "$name" "$rc" >> "$LOG"
  printf "%s " "$@" >> "$LOG"
  printf "\n" >> "$LOG"
  return $rc
}
run dst-status-pre-complete git --no-optional-locks -C "$DST" status --porcelain=v1 --untracked-files=all
run dst-pycache-pre bash -c "find \"$DST\" -path \"$DST/.git\" -prune -o -name '__pycache__' -print -o -name '*.pyc' -print | wc -l"
run dst-add-complete git --no-optional-locks -C "$DST" add -A
run dst-status-staged git --no-optional-locks -C "$DST" status --porcelain=v1 --untracked-files=all
run dst-diff-cached-stat git --no-optional-locks -C "$DST" diff --cached --stat
run dst-commit-complete env GIT_AUTHOR_NAME=Synthetic-R1-Oracle-Final GIT_AUTHOR_EMAIL=synthetic-r1-oracle-final@example.invalid GIT_COMMITTER_NAME=Synthetic-R1-Oracle-Final GIT_COMMITTER_EMAIL=synthetic-r1-oracle-final@example.invalid git --no-optional-locks -C "$DST" commit -q -m "R1 oracle final complete 741 SOURCE (all untracked intended now tracked) before authorities"
run dst-head-complete git --no-optional-locks -C "$DST" rev-parse HEAD
run dst-log-complete git --no-optional-locks -C "$DST" log --oneline -4
run dst-status-post-complete git --no-optional-locks -C "$DST" status --porcelain=v1 --untracked-files=all
run dst-ls-files-count git --no-optional-locks -C "$DST" ls-files --stage
run dst-test-sha-post sha256sum "$DST/tests/test_survey_weekly_mechanical_refresh_v2.py"
run dst-latexmkrc-sha-post sha256sum "$DST/.latexmkrc"
echo "DONE COMPLETE COMMIT rc=0"
