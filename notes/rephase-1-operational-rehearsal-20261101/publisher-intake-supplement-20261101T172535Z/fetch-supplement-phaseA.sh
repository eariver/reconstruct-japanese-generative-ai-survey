#!/usr/bin/env bash
# Supplement phaseA — targeted version metadata only, preserve original 40 captures (no overwrite)
# Original: publisher-intake-20261101T163426Z (40 req, 40 DATA preserved)
# Cutoff: 2026-09-21T16:10:00Z
set -uo pipefail
SUPP_DIR="notes/rephase-1-operational-rehearsal-20261101/publisher-intake-supplement-20261101T172535Z"
ORIG_DIR="notes/rephase-1-operational-rehearsal-20261101/publisher-intake-20261101T163426Z"
mkdir -p "$SUPP_DIR"
UA="Mozilla/5.0 (compatible; SP-publisher-supplement/20261101; bounded-research)"

fetch_gh() {
  gid="$1"; label="$2"; apipath="$3"; outbase="$4"
  echo "=== $gid $label ==="
  echo "gh api -i \"$apipath\"" > "$SUPP_DIR/${gid}.command.txt"
  echo "$label" > "$SUPP_DIR/${gid}.label.txt"
  echo "$apipath" > "$SUPP_DIR/${gid}.url.txt"
  echo "gh host github.com (token redacted, not logged)" > "$SUPP_DIR/${gid}.argv-extra.txt"
  echo "supplement of $ORIG_DIR, no overwrite" > "$SUPP_DIR/${gid}.supplement-note.txt"
  start=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "start $start" > "$SUPP_DIR/${gid}.time.txt"
  echo $$ > "$SUPP_DIR/${gid}.pid.txt"
  gh api -i "$apipath" > "$SUPP_DIR/${gid}.stdout.raw" 2> "$SUPP_DIR/${gid}.stderr.txt"
  ec=$?
  echo -n "$ec" > "$SUPP_DIR/${gid}.exit.txt"
  end=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "end $end" >> "$SUPP_DIR/${gid}.time.txt"
  python3 - "$SUPP_DIR" "$gid" "$outbase" <<'PY'
import os, sys, hashlib
d=sys.argv[1]; gid=sys.argv[2]; outbase=sys.argv[3]
raw=os.path.join(d,gid+".stdout.raw")
hdr=os.path.join(d,gid+".headers.txt")
body=os.path.join(d,outbase)
data=open(raw,'rb').read()
idx=data.find(b"\r\n\r\n")
sep=4
if idx<0:
  idx=data.find(b"\n\n"); sep=2
if idx>=0:
  open(hdr,'wb').write(data[:idx])
  open(body,'wb').write(data[idx+sep:])
else:
  open(hdr,'wb').write(b"")
  open(body,'wb').write(data)
b=open(body,'rb').read()
print(gid, "bytes", len(b), "sha256", hashlib.sha256(b).hexdigest())
open(os.path.join(d,gid+".bytes.txt"),'w').write(str(len(b)))
open(os.path.join(d,gid+".sha256.txt"),'w').write(hashlib.sha256(b).hexdigest())
PY
  echo "exit $ec for $gid"
}

fetch_http() {
  gid="$1"; label="$2"; url="$3"; outbase="$4"
  echo "=== $gid $label ==="
  echo "curl -L --max-redirs 5 --connect-timeout 20 --max-time 120 -A \"$UA\" -D \"$SUPP_DIR/${gid}.headers.txt\" -o \"$SUPP_DIR/${outbase}\" \"$url\"" > "$SUPP_DIR/${gid}.command.txt"
  echo "$label" > "$SUPP_DIR/${gid}.label.txt"
  echo "$url" > "$SUPP_DIR/${gid}.url.txt"
  echo "UA: $UA" > "$SUPP_DIR/${gid}.argv-extra.txt"
  echo "supplement of $ORIG_DIR, no overwrite" > "$SUPP_DIR/${gid}.supplement-note.txt"
  start=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "start $start" > "$SUPP_DIR/${gid}.time.txt"
  echo $$ > "$SUPP_DIR/${gid}.pid.txt"
  curl -L --max-redirs 5 --connect-timeout 20 --max-time 120 -s -v -A "$UA" -D "$SUPP_DIR/${gid}.headers.txt" -o "$SUPP_DIR/${outbase}" "$url" 2> "$SUPP_DIR/${gid}.stderr.txt"
  ec=$?
  echo -n "$ec" > "$SUPP_DIR/${gid}.exit.txt"
  end=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "end $end" >> "$SUPP_DIR/${gid}.time.txt"
  if [ -f "$SUPP_DIR/${outbase}" ]; then
    bytes=$(wc -c < "$SUPP_DIR/${outbase}" | tr -d ' ')
    sha=$(sha256sum "$SUPP_DIR/${outbase}" | cut -d' ' -f1)
  else
    bytes="0-missing"; sha="missing"
  fi
  echo "bytes $bytes sha256 $sha exit $ec" >> "$SUPP_DIR/${gid}.time.txt"
  echo "$bytes" > "$SUPP_DIR/${gid}.bytes.txt"
  echo "$sha" > "$SUPP_DIR/${gid}.sha256.txt"
  echo "exit $ec bytes $bytes sha $sha for $gid"
}

# PR27742 remaining — bounded pagination per_page100 within existing PR (immutable merge facts + validation claims)
fetch_gh "s15-commits-all100" "PR27742 commits all per_page100 (supplement 30/65 partial)" "repos/ggml-org/llama.cpp/pulls/27742/commits?per_page=100" "DATA.s15-commits-all100.json"
fetch_gh "s15-comments-p1-100" "PR27742 comments page1 per_page100" "repos/ggml-org/llama.cpp/issues/27742/comments?per_page=100&page=1" "DATA.s15-comments-p1-100.json"
fetch_gh "s15-comments-p2-100" "PR27742 comments page2 per_page100 (remainder 44)" "repos/ggml-org/llama.cpp/issues/27742/comments?per_page=100&page=2" "DATA.s15-comments-p2-100.json"

# vLLM recipe same-file commit history (direct Edit link from current body)
fetch_gh "s14-commits-file" "vLLM recipes file commits history (same file DeepSeek-V4.1-Flash.yaml)" "repos/vllm-project/recipes/commits?path=recipes/models/deepseek-ai/DeepSeek-V4.1-Flash.yaml&per_page=100" "DATA.s14-commits-file.json"

# HF modelcard commit history (same document, NO weights, metadata only)
fetch_http "s16-commits" "HF DeepSeek-V4.1-Flash commit history (same modelcard document)" "https://huggingface.co/api/models/deepseek-ai/DeepSeek-V4.1-Flash/commits" "DATA.s16-commits.json"

echo "Supplement phaseA done (5 requests)."
