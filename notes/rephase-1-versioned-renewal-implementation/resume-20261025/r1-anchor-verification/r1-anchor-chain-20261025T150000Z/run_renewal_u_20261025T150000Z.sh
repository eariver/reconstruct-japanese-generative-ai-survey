#!/bin/bash
# Run renewal U — fresh child new 740 epoch, workspace TMPDIR, 1200s guard.
set -u
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
FIX="$REPO/.rephase-1-editorial-runtime/versioned-renewal-r1-anchor-20261025T150000Z/anchor-weekly"
TMPLOCAL="$REPO/.rephase-1-editorial-runtime/versioned-renewal-r1-anchor-20261025T150000Z/tmp"
EVIDENCE="$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/r1-anchor-verification/r1-anchor-chain-20261025T150000Z"
export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C
export TMPDIR="$TMPLOCAL"
LOG="$EVIDENCE/commands.log"
printf "run renewal U fresh child new740\n" >> "$LOG"
timeout 1200 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0 PYTHONDONTWRITEBYTECODE=1 TMPDIR="$TMPLOCAL" PYTHONPATH="$FIX" python3 "$EVIDENCE/renewal_u_20261025T150000Z.py" "$FIX" "$EVIDENCE" >"$EVIDENCE/renewal-u-stdout.txt" 2>"$EVIDENCE/renewal-u-stderr.txt"
rc=$?
printf "%s" "$rc" > "$EVIDENCE/renewal-u-exit.txt"
printf "run renewal U rc=%s\n" "$rc" >> "$LOG"
exit $rc
