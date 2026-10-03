#!/bin/bash
# Binary-exact single capture of docs/core-v2-deferred-maintenance-summary.md
# at pinned main d6381568cc897a47d6de992189e20339350342b7.
# Why shell subprocess is necessary: gh API returns JSON with base64-encoded
# blob; only a byte-preserving base64 decode (python3) yields the exact source
# bytes. The decoded file below is written ONLY by this script's decoder, never
# by text editing, to avoid reconstructing claimed original bytes through edits.
# Single fetch only: one `gh api .../contents/...?ref=<SHA>` call. No re-fetch.
set -u
OUTDIR="notes/rephase-1-deferred-intake-20261003"
REF="d6381568cc897a47d6de992189e20339350342b7"
PATH_DOC="docs/core-v2-deferred-maintenance-summary.md"
RAW_JSON="$OUTDIR/raw-contents-api.json"
STDERR_LOG="$OUTDIR/fetch.stderr"
EXIT_FILE="$OUTDIR/fetch.exit"
DECODED="$OUTDIR/deferred-maintenance-summary.md"

echo "REF=$REF"
echo "UTC_START=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
gh api "repos/eariver/japanese-generative-ai-survey/contents/${PATH_DOC}?ref=${REF}" >"$RAW_JSON" 2>"$STDERR_LOG"
echo "$?" >"$EXIT_FILE"
echo "EXIT=$(cat "$EXIT_FILE")"
echo "UTC_END=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
# Decode exactly once from saved raw JSON (no network):
python3 - "$RAW_JSON" "$DECODED" <<'PY'
import base64, json, sys
raw_path, out_path = sys.argv[1], sys.argv[2]
obj = json.load(open(raw_path, encoding="utf-8"))
assert obj.get("encoding") == "base64", obj.get("encoding")
assert obj.get("path") == "docs/core-v2-deferred-maintenance-summary.md", obj.get("path")
b = base64.b64decode(obj["content"])
open(out_path, "wb").write(b)
print(f"decoded_bytes={len(b)} api_name={obj.get('name')} api_sha={obj.get('sha')} api_size={obj.get('size')}")
PY
echo "DECODER_EXIT:$?"
ls -l "$RAW_JSON" "$DECODED" "$STDERR_LOG" "$EXIT_FILE"
sha256sum "$DECODED"
git hash-object "$DECODED"
wc -c "$DECODED"
