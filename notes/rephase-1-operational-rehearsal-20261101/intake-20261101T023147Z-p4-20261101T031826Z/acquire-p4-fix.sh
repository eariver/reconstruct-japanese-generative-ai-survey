#!/usr/bin/env bash
# P4 — fix 6 metadata-only rows via exact blob + fetch 2 X-manifests (same fixed refs, no new permission)
set -uo pipefail
INTAKE_DIR="notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p4-20261101T031826Z"
REPO="eariver/japanese-generative-ai-survey"
REF_W34="774dd39a951c9ac3818e83dfffd4c7666efb0a20"
REF_SP="c8d0ecc1c9566a2303ad3b4c42635d4b672650e4"
mkdir -p "$INTAKE_DIR"
declare -a SPECS=(
"p4a02|W34-gh-flashinfer-blob|repos/${REPO}/git/blobs/90462213d9825c9224a0b169d753f023dcf18537"
"p4a03|W34-gh-llamacpp-blob|repos/${REPO}/git/blobs/62edff35562c0eaa4d175546364b1c2838a11a3a"
"p4a04|W34-gh-transformers-blob|repos/${REPO}/git/blobs/daa04d862800fc51c3066a2b3e2f53ff96394992"
"p4a05|W34-gh-tensorrt-blob|repos/${REPO}/git/blobs/6b093886cc5cf29de0c3ebe55bb907de9c64bad3"
"p4a06|W34-gh-sglang-blob|repos/${REPO}/git/blobs/f16c5ec6b2a24a09e7f76dd5fd7ca8e555d30587"
"p4a07|W34-gh-vllm-blob|repos/${REPO}/git/blobs/94aaa50674ab67014d4b0a0030c00af752df7c87"
"p4x01|W34-x-manifest|repos/${REPO}/contents/sources/2026-W34/external/x/x-source-intake-v2.json?ref=${REF_W34}"
"p4x02|SP-x-manifest|repos/${REPO}/contents/sources/SP-efficient-llm-2026/external/x/x-source-intake-v2.json?ref=${REF_SP}"
)
for spec in "${SPECS[@]}"; do
  IFS='|' read -r gid label apipath <<< "$spec"
  echo "=== $gid $label ==="
  echo "gh api -i \"$apipath\"" > "$INTAKE_DIR/${gid}.command.txt"
  echo "$label" > "$INTAKE_DIR/${gid}.label.txt"
  echo "$apipath" > "$INTAKE_DIR/${gid}.url.txt"
  if [[ "$apipath" == *"$REF_W34"* ]]; then echo "$REF_W34" > "$INTAKE_DIR/${gid}.ref.txt"; elif [[ "$apipath" == *"$REF_SP"* ]]; then echo "$REF_SP" > "$INTAKE_DIR/${gid}.ref.txt"; else echo "blob-sha-pinned from fixed P3 path metadata (774 selected Raw, no new ref)" > "$INTAKE_DIR/${gid}.ref.txt"; fi
  date -u +%Y-%m-%dT%H:%M:%SZ > "$INTAKE_DIR/${gid}.time.txt"
  echo $$ > "$INTAKE_DIR/${gid}.pid.txt"
  gh api -i "$apipath" > "$INTAKE_DIR/${gid}.stdout.raw" 2> "$INTAKE_DIR/${gid}.stderr.txt"
  echo -n "$?" > "$INTAKE_DIR/${gid}.exit.txt"
  echo "exit $(cat "$INTAKE_DIR/${gid}.exit.txt") for $gid"
done
echo "P4 fetch done. Splitting/verifying."
python3 - "$INTAKE_DIR" <<'PY'
import os, sys, json, base64, hashlib, glob
d=sys.argv[1]
ids=sorted([os.path.basename(p).split('.')[0] for p in glob.glob(os.path.join(d,"p4*.command.txt"))])
for gid in ids:
  raw=os.path.join(d,gid+".stdout.raw")
  hdr=os.path.join(d,gid+".headers.txt")
  body=os.path.join(d,gid+".body.json")
  data=open(raw,'rb').read()
  idx=data.find(b"\r\n\r\n"); sep=4
  if idx<0:
    idx=data.find(b"\n\n"); sep=2
  if idx>=0:
    open(hdr,'wb').write(data[:idx]); open(body,'wb').write(data[idx+sep:])
  else:
    open(hdr,'wb').write(b""); open(body,'wb').write(data)
  try:
    j=json.loads(open(body,'rb').read().decode('utf-8',errors='replace'))
  except Exception as e:
    print(gid,"not JSON",e); continue
  if isinstance(j,dict) and 'content' in j:
    enc=j.get('encoding')
    if enc=='base64':
      b=base64.b64decode(j.get('content',''))
      print(gid,"decoded",len(b),"reported",j.get('size'),"match",len(b)==j.get('size'))
      rep=j.get('sha',''); calc=hashlib.sha1(b"blob %d\0"%len(b)+b).hexdigest()
      print(gid,"blob",rep,calc,rep==calc)
      # map to P3 repo filename for supersede (no recopy confusion: NEW verified payload in P4)
      # Use original P3 DATA filename for continuity, but NEW file in P4 dir
      # Determine original filename: for blob p4a02-07 use P3 mapping, for manifests use path basename
      orig_map={
        "p4a02": "flashinfer-ai__flashinfer.json",
        "p4a03": "ggml-org__llama.cpp.json",
        "p4a04": "huggingface__transformers.json",
        "p4a05": "nvidia__tensorrt-llm.json",
        "p4a06": "sgl-project__sglang.json",
        "p4a07": "vllm-project__vllm.json",
      }
      if gid in orig_map:
        name=orig_map[gid]
      else:
        name=j.get('path','').split('/')[-1] or gid
      out=os.path.join(d,f"DATA.{gid}.{name}")
      open(out,'wb').write(b)
      print(gid,"wrote",out,hashlib.sha256(b).hexdigest())
    else:
      print(gid,"encoding",enc,"size",j.get('size'),"content_len",len(j.get('content','')))
  elif isinstance(j,list):
    print(gid,"listing",len(j))
  else:
    print(gid,"dict",list(j.keys())[:10], str(j.get('message',''))[:200] if isinstance(j,dict) else "")
PY
echo "P4 split done."
