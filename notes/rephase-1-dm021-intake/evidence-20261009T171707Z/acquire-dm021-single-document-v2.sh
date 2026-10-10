#!/bin/bash
# DM-021 narrow intake — decode correction v2 (no network).
# Corrects acquire-dm021-single-document.sh v1 whose python decode step lacked
# the heredoc decoder body (no-op, decoded file absent; v1 run exit 1 preserved).
# This v2 performs NO gh API calls: it decodes EXACTLY ONCE from the already
# saved v1 raw response raw-contents-api.json (87440 bytes, contents.exit 0)
# into deferred-maintenance-summary.md via byte-preserving base64 decode.
# Exclusive/no-overwrite: refuses if the decoded output or v2 logs exist.
set -u -o noclobber
PACKET="notes/rephase-1-dm021-intake/evidence-20261009T171707Z"
RAW_JSON="$PACKET/raw-contents-api.json"
DECODED="$PACKET/deferred-maintenance-summary.md"
DECODE2_STDOUT="$PACKET/decode-v2.stdout"
DECODE2_STDERR="$PACKET/decode-v2.stderr"
DECODE2_EXIT="$PACKET/decode-v2.exit"

echo "ARGV=$*"
echo "ARGC=$#"
echo "UTC_START=$(date -u +%Y-%m-%dT%H:%M:%SZ)"

for f in "$DECODED" "$DECODE2_STDOUT" "$DECODE2_STDERR" "$DECODE2_EXIT"; do
  if [ -e "$f" ]; then
    echo "REFUSE_OVERWRITE_EXISTS: $f" >&2
    exit 20
  fi
done
if [ ! -f "$RAW_JSON" ]; then
  echo "MISSING_SAVED_RAW: $RAW_JSON" >&2
  exit 21
fi

python3 - "$RAW_JSON" "$DECODED" >"$DECODE2_STDOUT" 2>"$DECODE2_STDERR" <<'PY'
import base64, json, sys
raw_path, out_path = sys.argv[1], sys.argv[2]
obj = json.load(open(raw_path, encoding="utf-8"))
assert obj.get("encoding") == "base64", obj.get("encoding")
assert obj.get("path") == "docs/core-v2-deferred-maintenance-summary.md", obj.get("path")
b = base64.b64decode(obj["content"])
open(out_path, "wb").write(b)
print(f"decoded_bytes={len(b)} api_name={obj.get('name')} api_sha={obj.get('sha')} api_size={obj.get('size')}")
PY
echo "$?" >"$DECODE2_EXIT"
echo "DECODE_V2_EXIT=$(cat "$DECODE2_EXIT")"
cat "$DECODE2_STDOUT"
if [ "$(cat "$DECODE2_EXIT")" != "0" ]; then
  echo "DECODE_V2_FAILED" >&2
  exit 22
fi

echo "UTC_END=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
ls -l "$RAW_JSON" "$DECODED"
sha256sum "$DECODED"
git hash-object "$DECODED"
wc -c "$DECODED"
