#!/usr/bin/env bash
# r5 prepare launcher — unique raw capture, no git readback.
# Captures argv/cwd/env-subset/timestamps + tool stdout/stderr/exit into one
# per-run bundle. The tool itself performs the single selected isolated call
# (git rev-parse inside the e84 repo via core.repository_commit_sha); this
# launcher runs no git.
set -u
PACKET="/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-operational-rehearsal-resume-20261104"
TOOL="$PACKET/sp-operator-prepare-r5-20261104.py"
NEW_ID=""
RETENTION=""
MANIFEST="$PACKET/sp-prepare-expected-manifest-r5-20261104.json"
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work"
while [ $# -gt 0 ]; do
  case "$1" in
    --new-supplement-id) NEW_ID="$2"; shift 2;;
    --retention-dir) RETENTION="$2"; shift 2;;
    --manifest) MANIFEST="$2"; shift 2;;
    --repo-root) REPO="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
if [ -z "$NEW_ID" ] || [ -z "$RETENTION" ]; then
  echo "usage: $0 --new-supplement-id ID --retention-dir DIR [--manifest M] [--repo-root R]" >&2
  exit 2
fi
RUN="$PACKET/r5-prepare-run-$(date -u +%Y%m%dT%H%M%SZ)-$$"
mkdir -p "$RUN/raw"
{
  echo "utc_start=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "argv=$0 --new-supplement-id $NEW_ID --retention-dir $RETENTION --manifest $MANIFEST --repo-root $REPO"
  echo "cwd=$(pwd)"
  echo "python=$(python3 --version 2>&1)"
  echo "PYTHONDONTWRITEBYTECODE=${PYTHONDONTWRITEBYTECODE-unset} PYTHONHASHSEED=${PYTHONHASHSEED-unset}"
} > "$RUN/launcher.json"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0
python3 "$TOOL" --retention-dir "$RETENTION" --new-supplement-id "$NEW_ID" \
  --manifest "$MANIFEST" --repo-root "$REPO" \
  > "$RUN/raw/tool.stdout.txt" 2> "$RUN/raw/tool.stderr.txt"
code=$?
echo "$code" > "$RUN/raw/tool.exit.txt"
{
  echo "utc_end=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "exit=$code"
} >> "$RUN/launcher.json"
echo "run_bundle=$RUN exit=$code"
exit "$code"
