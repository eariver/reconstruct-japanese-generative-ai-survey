#!/bin/bash
# DM-021 narrow read-only intake — single-document capture.
# Resolves ONE current Production main commit (metadata only), then fetches ONLY
# docs/core-v2-deferred-maintenance-summary.md pinned to that exact SHA via gh API.
# Exclusive/no-overwrite: refuses if any output already exists; never re-fetches
# on success; never touches notes/rephase-1-deferred-intake-20261003/.
# Saved argv/stdout/stderr/returncodes are evidence (see run-*.log files created
# by the outer invocation, plus per-call *.stderr/*.exit inside the packet).
# Why shell subprocess is necessary: gh API Contents returns JSON with a base64
# `content` field; only a byte-preserving base64 decode (python3) yields the
# exact source bytes. The decoded file is written ONLY by this script's decoder.
set -u -o noclobber
PACKET="notes/rephase-1-dm021-intake/evidence-20261009T171707Z"
REPO="eariver/japanese-generative-ai-survey"
PATH_DOC="docs/core-v2-deferred-maintenance-summary.md"
MAIN_JSON="$PACKET/main-commit-api.json"
MAIN_STDERR="$PACKET/main-commit.stderr"
MAIN_EXIT="$PACKET/main-commit.exit"
RAW_JSON="$PACKET/raw-contents-api.json"
CONT_STDERR="$PACKET/contents.stderr"
CONT_EXIT="$PACKET/contents.exit"
DECODED="$PACKET/deferred-maintenance-summary.md"
DECODE_STDERR="$PACKET/decode.stderr"
DECODE_EXIT="$PACKET/decode.exit"

echo "ARGV=$*"
echo "ARGC=$#"
echo "UTC_START=$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Exclusive guards: refuse to overwrite any existing packet output.
for f in "$MAIN_JSON" "$MAIN_STDERR" "$MAIN_EXIT" "$RAW_JSON" "$CONT_STDERR" "$CONT_EXIT" "$DECODED" "$DECODE_STDERR" "$DECODE_EXIT"; do
  if [ -e "$f" ]; then
    echo "REFUSE_OVERWRITE_EXISTS: $f" >&2
    exit 10
  fi
done

# Call 1/2: resolve one current main commit, metadata only. No code/tree fetch.
gh api "repos/${REPO}/commits/main" >"$MAIN_JSON" 2>"$MAIN_STDERR"
echo "$?" >"$MAIN_EXIT"
echo "MAIN_EXIT=$(cat "$MAIN_EXIT")"
echo "MAIN_STDERR_BYTES=$(wc -c <"$MAIN_STDERR")"
if [ "$(cat "$MAIN_EXIT")" != "0" ]; then
  echo "MAIN_RESOLVE_FAILED" >&2
  exit 11
fi

# Extract exact SHA locally from saved JSON (no network).
PIN_SHA=$(python3 - "$MAIN_JSON" <<'PY'
import json, sys
obj = json.load(open(sys.argv[1], encoding="utf-8"))
sha = obj.get("sha")
assert isinstance(sha, str) and len(sha) == 40, repr(sha)[:100]
print(sha)
PY
)
echo "PIN_SHA=$PIN_SHA"

# Call 2/2: single named-document fetch pinned to exact SHA. No ref follow.
gh api "repos/${REPO}/contents/${PATH_DOC}?ref=${PIN_SHA}" >"$RAW_JSON" 2>"$CONT_STDERR"
echo "$?" >"$CONT_EXIT"
echo "CONTENTS_EXIT=$(cat "$CONT_EXIT")"
echo "CONTENTS_STDERR_BYTES=$(wc -c <"$CONT_STDERR")"
if [ "$(cat "$CONT_EXIT")" != "0" ]; then
  echo "CONTENTS_FETCH_FAILED" >&2
  exit 12
fi

# Decode exactly once from saved raw JSON (no network).
python3 - "$RAW_JSON" "$DECODED" >"$PACKET/decode.stdout" 2>"$DECODE_STDERR"
echo "$?" >"$DECODE_EXIT"
echo "DECODE_EXIT=$(cat "$DECODE_EXIT")"
cat "$PACKET/decode.stdout"
if [ "$(cat "$DECODE_EXIT")" != "0" ]; then
  echo "DECODE_FAILED" >&2
  exit 13
fi

echo "UTC_END=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
ls -l "$MAIN_JSON" "$RAW_JSON" "$DECODED" "$MAIN_STDERR" "$CONT_STDERR" "$MAIN_EXIT" "$CONT_EXIT"
sha256sum "$RAW_JSON" "$DECODED"
git hash-object "$DECODED"
wc -c "$DECODED" "$RAW_JSON"
