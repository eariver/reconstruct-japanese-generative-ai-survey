#!/bin/bash
# Guarded background controller for LONGFORM closure: owned PID/heartbeat/terminal exit files + poll
set -u
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
EVID="$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-archive-correction/run-lf4-closure-20261025T120000Z"
mkdir -p "$EVID"
PIDFILE="$EVID/pid.txt"
OUT="$EVID/stdout.txt"
ERR="$EVID/stderr.txt"
EXITF="$EVID/exit.txt"
HEART="$EVID/heartbeat.txt"
# Avoid duplicate run: if PID alive, do not launch
if [ -f "$PIDFILE" ]; then
  OLDPID=$(cat "$PIDFILE")
  if [ -n "$OLDPID" ] && ps -p "$OLDPID" > /dev/null 2>&1; then
    echo "DUPLICATE: closure child $OLDPID still alive, not launching"
    exit 2
  fi
fi
# Launch NEW child bounded 1200s library timeout (inside script), outer guarded via poll
# Use timeout 1250 to allow 1200 library + margin, but outer bash poll uses short waits
rm -f "$OUT" "$ERR" "$EXITF" "$HEART"
export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C
nohup python3 "$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/editorial-archive-correction/run-lf4-closure-20261025T120000Z.py" >"$OUT" 2>"$ERR" &
NEWPID=$!
echo "$NEWPID" > "$PIDFILE"
echo "LAUNCHED closure PID=$NEWPID at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
# Poll with heartbeat, max 1250s (poll every 10s, 125 polls)
for i in $(seq 1 125); do
  sleep 10
  if [ -f "$HEART" ]; then tail -1 "$HEART"; fi
  if ! ps -p "$NEWPID" > /dev/null 2>&1; then
    echo "CHILD $NEWPID finished, checking exit"
    # Wait to reap exit code if available via jobs? Use kill -0 check + exit file
    # Our child writes exit via wrapper? Actually python script does not write EXITF; we write via wait
    wait "$NEWPID"; RC=$?
    echo "$RC" > "$EXITF"
    echo "TERMINAL rc=$RC PID=$NEWPID"
    exit $RC
  fi
  # Also check if child wrote done marker in heartbeat
  if grep -q "done rc0" "$HEART" 2>/dev/null; then
    echo "HEARTBEAT done rc0 observed"
  fi
done
echo "POLL TIMEOUT 1250s, child $NEWPID still alive, preserving (no kill, no blind dup)"
ps -p "$NEWPID" -o pid,etime,cmd
exit 124
