#!/bin/bash
# Run NEW VALIDATED builder — fresh child, workspace TMPDIR, PID heartbeat, terminal guard.
set -u
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
FIX="$REPO/.rephase-1-editorial-runtime/versioned-renewal-r1-anchor-20261025T150000Z/anchor-weekly"
TMPLOCAL="$REPO/.rephase-1-editorial-runtime/versioned-renewal-r1-anchor-20261025T150000Z/tmp"
EVIDENCE="$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/r1-anchor-verification/r1-anchor-chain-20261025T150000Z"
export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C
export TMPDIR="$TMPLOCAL"

LOG="$EVIDENCE/commands.log"
printf "run validated-build fresh child cwd FIX\n" >> "$LOG"

run() {
  tag="$1"; shift
  out="$EVIDENCE/${tag}-stdout.txt"
  err="$EVIDENCE/${tag}-stderr.txt"
  rcfile="$EVIDENCE/${tag}-exit.txt"
  env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0 PYTHONDONTWRITEBYTECODE=1 TMPDIR="$TMPLOCAL" "$@" >"$out" 2>"$err"
  rc=$?
  printf "%s" "$rc" > "$rcfile"
  printf "run %s rc=%s cmd=%s\n" "$tag" "$rc" "$*" >> "$LOG"
  return $rc
}

# Fresh Python per code epoch: PYTHONPATH=FIX (old 721), cwd=FIX, no 740 caching.
timeout 1200 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0 PYTHONDONTWRITEBYTECODE=1 TMPDIR="$TMPLOCAL" PYTHONPATH="$FIX" python3 "$EVIDENCE/build_validated_20261025T150000Z.py" "$FIX" "$EVIDENCE" >"$EVIDENCE/validated-build-stdout.txt" 2>"$EVIDENCE/validated-build-stderr.txt"
rc=$?
printf "%s" "$rc" > "$EVIDENCE/validated-build-exit.txt"
printf "run validated-build rc=%s\n" "$rc" >> "$LOG"
exit $rc
