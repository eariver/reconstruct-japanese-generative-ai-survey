#!/usr/bin/env bash
# dispose+run launcher — unique EXCLUSIVE raw dir (no mkdir -p), no git readback.
# Captures argv/cwd/env-subset/timestamps + tool stdout/stderr/exit into one
# per-run bundle. The tool itself performs the single selected isolated call
# (git rev-parse inside the e84 repo via core.repository_commit_sha); this
# launcher runs no git. DO NOT RUN until root authorizes after independent review.
set -u
PACKET="/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-operational-rehearsal-resume-20261104"
TOOL="$PACKET/sp-operator-dispose-run-20261104.py"
NEW_RET=""
READY=""
MANIFEST="$PACKET/sp-prepare-expected-manifest-r6-20261104.json"
EXP_TOOL=""
EXP_READY=""
EXP_MANIFEST=""
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work"
while [ $# -gt 0 ]; do
  case "$1" in
    --retention-dir) NEW_RET="$2"; shift 2;;
    --ready-path) READY="$2"; shift 2;;
    --manifest) MANIFEST="$2"; shift 2;;
    --expected-tool-sha) EXP_TOOL="$2"; shift 2;;
    --expected-ready-sha) EXP_READY="$2"; shift 2;;
    --expected-manifest-sha) EXP_MANIFEST="$2"; shift 2;;
    --repo-root) REPO="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
if [ -z "$NEW_RET" ] || [ -z "$READY" ] || [ -z "$EXP_TOOL" ] || [ -z "$EXP_READY" ] || [ -z "$EXP_MANIFEST" ]; then
  echo "usage: $0 --retention-dir DIR --ready-path READY --expected-tool-sha H --expected-ready-sha H --expected-manifest-sha H [--manifest M] [--repo-root R]" >&2
  exit 2
fi
for v in "$EXP_TOOL" "$EXP_READY" "$EXP_MANIFEST"; do
  case "$v" in
    *[!0-9a-f]*|"") echo "expected hashes must be 64-hex" >&2; exit 2;;
  esac
  if [ "${#v}" -ne 64 ]; then echo "expected hashes must be 64-hex" >&2; exit 2; fi
done
RUN="$PACKET/dispose-run-$(date -u +%Y%m%dT%H%M%SZ)-$$"
mkdir "$RUN" || { echo "run bundle exists (refuse): $RUN" >&2; exit 2; }
mkdir "$RUN/raw" || { echo "raw dir exists (refuse): $RUN/raw" >&2; exit 2; }
{
  echo "utc_start=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "argv=$0 --retention-dir $NEW_RET --ready-path $READY --expected-tool-sha $EXP_TOOL --expected-ready-sha $EXP_READY --expected-manifest-sha $EXP_MANIFEST --manifest $MANIFEST --repo-root $REPO"
  echo "cwd=$(pwd)"
  echo "python=$(python3 --version 2>&1)"
  echo "PYTHONDONTWRITEBYTECODE=${PYTHONDONTWRITEBYTECODE-unset} PYTHONHASHSEED=${PYTHONHASHSEED-unset}"
} > "$RUN/launcher.json"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0
python3 "$TOOL" --retention-dir "$NEW_RET" --ready-path "$READY" \
  --manifest "$MANIFEST" --expected-tool-sha "$EXP_TOOL" --expected-ready-sha "$EXP_READY" \
  --expected-manifest-sha "$EXP_MANIFEST" --repo-root "$REPO" \
  > "$RUN/raw/tool.stdout.txt" 2> "$RUN/raw/tool.stderr.txt"
code=$?
echo "$code" > "$RUN/raw/tool.exit.txt"
{
  echo "utc_end=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "exit=$code"
} >> "$RUN/launcher.json"
echo "run_bundle=$RUN exit=$code"
exit "$code"
