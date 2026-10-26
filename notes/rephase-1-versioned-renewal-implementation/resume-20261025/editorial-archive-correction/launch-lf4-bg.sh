#!/bin/bash
# Launch LONGFORM closure background only (short outer, no long poll)
set -u
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
EVID="$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-archive-correction/run-lf4-closure-20261025T120000Z"
mkdir -p "$EVID"
PIDFILE="$EVID/pid.txt"
OUT="$EVID/stdout.txt"
ERR="$EVID/stderr.txt"
EXITF="$EVID/exit.txt"
# Avoid duplicate: if PID alive, refuse
if [ -f "$PIDFILE" ]; then
  OLDPID=$(cat "$PIDFILE" 2>/dev/null || echo "")
  if [ -n "$OLDPID" ] && ps -p "$OLDPID" > /dev/null 2>&1; then
    echo "DUPLICATE_REFUSE alive PID=$OLDPID"
    ps -p "$OLDPID" -o pid,etime,cmd
    exit 2
  fi
fi
rm -f "$OUT" "$ERR" "$EXITF" "$EVID/heartbeat.txt"
export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C
# Launch with timeout 1300 wrapper to bound library 1200 + margin; nohup so outer kill does not lose child
nohup bash -c 'python3 "$0" >"$1" 2>"$2"; RC=$?; echo "$RC" >"$3"' "$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-archive-correction/run-lf4-closure-20261025T120000Z.py" "$OUT" "$ERR" "$EXITF" > /dev/null 2>&1 &
NEWPID=$!
echo "$NEWPID" > "$PIDFILE"
echo "LAUNCHED PID=$NEWPID EVID=$EVID"
ps -p "$NEWPID" -o pid,etime,cmd
