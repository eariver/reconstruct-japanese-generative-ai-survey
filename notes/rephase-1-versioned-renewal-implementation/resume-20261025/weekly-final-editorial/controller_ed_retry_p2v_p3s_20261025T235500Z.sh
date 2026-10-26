#!/bin/bash
set -u
REPO=/home/eariver/git/reconstruct-japanese-generative-ai-survey
EVID=$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/ed-retry-p2v-p3s-20261025T235500Z
DRIVER=$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/weekly-final-editorial/driver_ed_retry_p2v_p3s_20261025T235500Z.py
PIDF=$EVID/controller-pid.txt
EXITF=$EVID/controller-exit.txt
mkdir -p "$EVID"
if [ -f "$PIDF" ]; then
  oldpid=$(cat "$PIDF" 2>/dev/null || echo "")
  if [ -n "$oldpid" ] && kill -0 "$oldpid" 2>/dev/null; then echo "DUPLICATE $oldpid"; exit 1; fi
fi
if [ -f "$EXITF" ]; then ec=$(cat "$EXITF" 2>/dev/null || echo ""); if [ "$ec" = "0" ]; then echo "ALREADY_COMPLETE"; exit 0; fi; fi
echo $$ > "$PIDF"
echo "$(date -u +%FT%TZ) start $$" > "$EVID/controller-heartbeat.txt"
echo "RUNNING" > "$EVID/controller-result.txt"
echo "running" > "$EXITF"
nohup /usr/bin/python3 "$DRIVER" > "$EVID/driver-stdout.log" 2> "$EVID/driver-stderr.log" &
drvpid=$!
echo "$drvpid" > "$EVID/driver-pid.txt"
echo "$(date -u +%FT%TZ) driver $drvpid" >> "$EVID/controller-heartbeat.txt"
echo "CONTROLLER_STARTED $drvpid"
