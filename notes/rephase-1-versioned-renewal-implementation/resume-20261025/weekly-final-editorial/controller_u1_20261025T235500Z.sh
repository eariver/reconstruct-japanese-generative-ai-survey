#!/bin/bash
# Guarded background controller for weekly-final U1 (NEW, no duplicate writers)
# Usage: controller_u1.sh (starts driver if not already running, writes PID/heartbeat/result/exit)
set -u
REPO=/home/eariver/git/reconstruct-japanese-generative-ai-survey
EVID=$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/u1-20261025T235500Z
DRIVER=$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/driver_u1_20261025T235500Z.py
PIDF=$EVID/controller-pid.txt
HBF=$EVID/controller-heartbeat.txt
RESF=$EVID/controller-result.txt
EXITF=$EVID/controller-exit.txt
mkdir -p "$EVID"
# No duplicate: if PID file exists and process alive, refuse
if [ -f "$PIDF" ]; then
  oldpid=$(cat "$PIDF" 2>/dev/null || echo "")
  if [ -n "$oldpid" ] && kill -0 "$oldpid" 2>/dev/null; then
    echo "DUPLICATE_REFUSED pid $oldpid still alive, not starting second writer"
    exit 1
  fi
  echo "stale pid $oldpid not alive, continuing"
fi
# Also refuse if EXIT already 0 (already complete, use resume check not rerun)
if [ -f "$EXITF" ]; then
  ec=$(cat "$EXITF" 2>/dev/null || echo "")
  if [ "$ec" = "0" ]; then
    echo "ALREADY_COMPLETE exit 0, not restarting (use readback, not rerun)"
    exit 0
  fi
fi
echo $$ > "$PIDF"
echo "$(date -u +%FT%TZ) controller start pid $$ driver $DRIVER" > "$HBF"
echo "STARTED pid $$" > "$RESF"
echo "running" > "$EXITF"
# Launch driver in background with nohup, capture driver pid
nohup /usr/bin/python3 "$DRIVER" > "$EVID/driver-stdout.log" 2> "$EVID/driver-stderr.log" &
drvpid=$!
echo "$drvpid" > "$EVID/driver-pid.txt"
echo "$(date -u +%FT%TZ) driver pid $drvpid" >> "$HBF"
echo "DRIVER_PID $drvpid" >> "$RESF"
# This controller returns immediately (background), poller checks EXITF
echo "CONTROLLER_STARTED driver $drvpid"
