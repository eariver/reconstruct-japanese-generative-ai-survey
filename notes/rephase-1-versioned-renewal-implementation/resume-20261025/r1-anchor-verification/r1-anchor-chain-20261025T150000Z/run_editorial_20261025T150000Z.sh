#!/bin/bash
# Run editorial — fresh child old 721, workspace TMPDIR, PID heartbeat, 1200s guard.
set -u
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
FIX="$REPO/.rephase-1-editorial-runtime/versioned-renewal-r1-anchor-20261025T150000Z/anchor-weekly"
TMPLOCAL="$REPO/.rephase-1-editorial-runtime/versioned-renewal-r1-anchor-20261025T150000Z/tmp"
EVIDENCE="$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/r1-anchor-verification/r1-anchor-chain-20261025T150000Z"
export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C
export TMPDIR="$TMPLOCAL"
LOG="$EVIDENCE/commands.log"
printf "run editorial fresh child old721\n" >> "$LOG"
timeout 1500 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0 PYTHONDONTWRITEBYTECODE=1 TMPDIR="$TMPLOCAL" PYTHONPATH="$FIX" P3S_DURABLE_OUTDIR="$TMPLOCAL/p3s-durable" python3 "$EVIDENCE/editorial_20261025T150000Z.py" "$FIX" "$EVIDENCE" >"$EVIDENCE/editorial-stdout.txt" 2>"$EVIDENCE/editorial-stderr.txt"
rc=$?
printf "%s" "$rc" > "$EVIDENCE/editorial-exit.txt"
printf "run editorial rc=%s\n" "$rc" >> "$LOG"
exit $rc
