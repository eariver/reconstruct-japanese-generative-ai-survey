#!/usr/bin/env bash
# Supplement phaseD — vLLM same-file history correct repo (bounded)
set -uo pipefail
SUPP_DIR="notes/rephase-1-operational-rehearsal-20261101/publisher-intake-supplement-20261101T172535Z"
ORIG_DIR="notes/rephase-1-operational-rehearsal-20261101/publisher-intake-20261101T163426Z"
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
# Correct repo vllm-project/vllm, same file path
fetch_gh "s14-commits-file-correct" "vLLM recipe file commits correct repo vllm" "repos/vllm-project/vllm/commits?path=recipes/models/deepseek-ai/DeepSeek-V4.1-Flash.yaml&per_page=100" "DATA.s14-commits-file-correct.json"
echo "Supplement phaseD done (1 request)."
