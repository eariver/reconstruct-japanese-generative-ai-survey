#!/usr/bin/env bash
# preflight r8 launcher — unique EXCLUSIVE bundle, no git. DO NOT RUN until root authorizes.
set -u
PACKET="/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-operational-rehearsal-resume-20261104"
TOOL="$PACKET/sp-operator-preflight-r8-D165fix-20261105.py"
NEW_RET=""; NEW_ID=""; MANIFEST="$PACKET/sp-prepare-expected-manifest-r7-D165fix-20261105.json"
EXP_TOOL=""; EXP_MANIFEST=""
REPO="/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work"
while [ $# -gt 0 ]; do
  case "$1" in
    --retention-dir) NEW_RET="$2"; shift 2;;
    --new-input-id) NEW_ID="$2"; shift 2;;
    --manifest) MANIFEST="$2"; shift 2;;
    --expected-tool-sha) EXP_TOOL="$2"; shift 2;;
    --expected-manifest-sha) EXP_MANIFEST="$2"; shift 2;;
    --repo-root) REPO="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done
if [ -z "$NEW_RET" ] || [ -z "$NEW_ID" ] || [ -z "$EXP_TOOL" ] || [ -z "$EXP_MANIFEST" ]; then
  echo "usage: $0 --retention-dir DIR --new-input-id ID --expected-tool-sha H --expected-manifest-sha H [--manifest M] [--repo-root R]" >&2
  exit 2
fi
for v in "$EXP_TOOL" "$EXP_MANIFEST"; do
  case "$v" in *[!0-9a-f]*|"") echo "hashes must be 64-hex" >&2; exit 2;; esac
  if [ "${#v}" -ne 64 ]; then echo "hashes must be 64-hex" >&2; exit 2; fi
done
RUN="$PACKET/preflight-r8-$(date -u +%Y%m%dT%H%M%SZ)-$$"
mkdir "$RUN" || exit 2
mkdir "$RUN/raw" || exit 2
{ echo "utc_start=$(date -u +%Y-%m-%dT%H:%M:%SZ)"; echo "argv=$0 --retention-dir $NEW_RET --new-input-id $NEW_ID"; echo "cwd=$(pwd)"; echo "python=$(python3 --version 2>&1)"; } > "$RUN/launcher.json"
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
python3 "$TOOL" --retention-dir "$NEW_RET" --new-input-id "$NEW_ID" --manifest "$MANIFEST" --expected-manifest-sha "$EXP_MANIFEST" --expected-tool-sha "$EXP_TOOL" --repo-root "$REPO" > "$RUN/raw/tool.stdout.txt" 2> "$RUN/raw/tool.stderr.txt"
code=$?; echo "$code" > "$RUN/raw/tool.exit.txt"; { echo "utc_end=$(date -u +%Y-%m-%dT%H:%M:%SZ)"; echo "exit=$code"; } >> "$RUN/launcher.json"
echo "run_bundle=$RUN exit=$code"; exit "$code"
