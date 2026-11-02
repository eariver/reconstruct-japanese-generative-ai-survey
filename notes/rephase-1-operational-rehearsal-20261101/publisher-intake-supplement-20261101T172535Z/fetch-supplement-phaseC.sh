#!/usr/bin/env bash
# Supplement phaseC — exact historical file versions (bounded, same-document only, NO weights)
# Corrects phaseA repo error: vLLM Edit/blob links point to vllm-project/vllm (not recipes)
set -uo pipefail
SUPP_DIR="notes/rephase-1-operational-rehearsal-20261101/publisher-intake-supplement-20261101T172535Z"
ORIG_DIR="notes/rephase-1-operational-rehearsal-20261101/publisher-intake-20261101T163426Z"
UA="Mozilla/5.0 (compatible; SP-publisher-supplement/20261101; bounded-research)"
fetch_gh() {
  gid="$1"; label="$2"; apipath="$3"; outbase="$4"
  echo "=== $gid $label ==="
  echo "gh api -i \"$apipath\"" > "$SUPP_DIR/${gid}.command.txt"
  echo "$label" > "$SUPP_DIR/${gid}.label.txt"
  echo "$apipath" > "$SUPP_DIR/${gid}.url.txt"
  echo "gh host github.com (token redacted)" > "$SUPP_DIR/${gid}.argv-extra.txt"
  echo "supplement of $ORIG_DIR, no overwrite" > "$SUPP_DIR/${gid}.supplement-note.txt"
  start=$(date -u +%Y-%m-%dT%H:%M:%SZ); echo "start $start" > "$SUPP_DIR/${gid}.time.txt"; echo $$ > "$SUPP_DIR/${gid}.pid.txt"
  gh api -i "$apipath" > "$SUPP_DIR/${gid}.stdout.raw" 2> "$SUPP_DIR/${gid}.stderr.txt"
  ec=$?; echo -n "$ec" > "$SUPP_DIR/${gid}.exit.txt"; end=$(date -u +%Y-%m-%dT%H:%M:%SZ); echo "end $end" >> "$SUPP_DIR/${gid}.time.txt"
  python3 - "$SUPP_DIR" "$gid" "$outbase" <<'PY'
import os, sys, hashlib
d=sys.argv[1]; gid=sys.argv[2]; outbase=sys.argv[3]
raw=os.path.join(d,gid+".stdout.raw"); hdr=os.path.join(d,gid+".headers.txt"); body=os.path.join(d,outbase)
data=open(raw,'rb').read()
idx=data.find(b"\r\n\r\n"); sep=4
if idx<0: idx=data.find(b"\n\n"); sep=2
if idx>=0: open(hdr,'wb').write(data[:idx]); open(body,'wb').write(data[idx+sep:])
else: open(hdr,'wb').write(b""); open(body,'wb').write(data)
b=open(body,'rb').read()
print(gid,"bytes",len(b),"sha256",hashlib.sha256(b).hexdigest())
open(os.path.join(d,gid+".bytes.txt"),'w').write(str(len(b)))
open(os.path.join(d,gid+".sha256.txt"),'w').write(hashlib.sha256(b).hexdigest())
PY
  echo "exit $ec for $gid"
}
fetch_http() {
  gid="$1"; label="$2"; url="$3"; outbase="$4"
  echo "=== $gid $label ==="
  echo "curl -L --max-redirs 5 --connect-timeout 20 --max-time 120 -A \"$UA\" -D \"$SUPP_DIR/${gid}.headers.txt\" -o \"$SUPP_DIR/${outbase}\" \"$url\"" > "$SUPP_DIR/${gid}.command.txt"
  echo "$label" > "$SUPP_DIR/${gid}.label.txt"; echo "$url" > "$SUPP_DIR/${gid}.url.txt"; echo "UA: $UA" > "$SUPP_DIR/${gid}.argv-extra.txt"
  echo "supplement of $ORIG_DIR, no overwrite" > "$SUPP_DIR/${gid}.supplement-note.txt"
  start=$(date -u +%Y-%m-%dT%H:%M:%SZ); echo "start $start" > "$SUPP_DIR/${gid}.time.txt"; echo $$ > "$SUPP_DIR/${gid}.pid.txt"
  curl -L --max-redirs 5 --connect-timeout 20 --max-time 120 -s -v -A "$UA" -D "$SUPP_DIR/${gid}.headers.txt" -o "$SUPP_DIR/${outbase}" "$url" 2> "$SUPP_DIR/${gid}.stderr.txt"
  ec=$?; echo -n "$ec" > "$SUPP_DIR/${gid}.exit.txt"; end=$(date -u +%Y-%m-%dT%H:%M:%SZ); echo "end $end" >> "$SUPP_DIR/${gid}.time.txt"
  if [ -f "$SUPP_DIR/${outbase}" ]; then bytes=$(wc -c < "$SUPP_DIR/${outbase}" | tr -d ' '); sha=$(sha256sum "$SUPP_DIR/${outbase}" | cut -d' ' -f1); else bytes="0-missing"; sha="missing"; fi
  echo "bytes $bytes sha256 $sha exit $ec" >> "$SUPP_DIR/${gid}.time.txt"
  echo "$bytes" > "$SUPP_DIR/${gid}.bytes.txt"; echo "$sha" > "$SUPP_DIR/${gid}.sha256.txt"
  echo "exit $ec bytes $bytes sha $sha for $gid"
}
# vLLM correct repo (Edit/blob hrefs prove vllm-project/vllm, not recipes)
fetch_gh "s14-file-main-correct" "vLLM recipe file contents @main correct repo vllm" "repos/vllm-project/vllm/contents/recipes/models/deepseek-ai/DeepSeek-V4.1-Flash.yaml?ref=main" "DATA.s14-file-main-correct.json"
fetch_gh "s14-commit-e0d-correct" "vLLM recipe blob commit e0d correct repo vllm" "repos/vllm-project/vllm/commits/e0d00e4b8eb0c89ec30921d0695cfdd409e9c211" "DATA.s14-commit-e0d-correct.json"
# HF exact README at latest commit <= cutoff (dba1be0 2026-09-10T08:18:10Z), NO weights
fetch_http "s16-readme-dba1be0" "HF modelcard README @dba1be0 2026-09-10 (NO weights)" "https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/raw/dba1be0a40aa45a94ad051997016db3960a90277/README.md" "DATA.s16-README-dba1be0.md"
echo "Supplement phaseC done (3 requests)."
