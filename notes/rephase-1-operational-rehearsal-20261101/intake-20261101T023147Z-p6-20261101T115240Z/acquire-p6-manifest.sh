#!/usr/bin/env bash
# P6 phase1 — fetch latest supplement manifest (389KB, contents API)
set -uo pipefail
INTAKE_DIR="notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p6-20261101T115240Z"
REPO="eariver/japanese-generative-ai-survey"
REF_W34="774dd39a951c9ac3818e83dfffd4c7666efb0a20"
mkdir -p "$INTAKE_DIR"
gid="p6a01"; label="W34-supplement-manifest-r2"; apipath="repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-screening-evidence-after-sol-discovery-r2/evidence-authority-supplement.json?ref=${REF_W34}"
echo "=== $gid $label ==="
echo "gh api -i \"$apipath\"" > "$INTAKE_DIR/${gid}.command.txt"
echo "$label" > "$INTAKE_DIR/${gid}.label.txt"
echo "$apipath" > "$INTAKE_DIR/${gid}.url.txt"
echo "$REF_W34" > "$INTAKE_DIR/${gid}.ref.txt"
date -u +%Y-%m-%dT%H:%M:%SZ > "$INTAKE_DIR/${gid}.time.txt"
echo $$ > "$INTAKE_DIR/${gid}.pid.txt"
gh api -i "$apipath" > "$INTAKE_DIR/${gid}.stdout.raw" 2> "$INTAKE_DIR/${gid}.stderr.txt"
echo -n "$?" > "$INTAKE_DIR/${gid}.exit.txt"
echo "exit $(cat "$INTAKE_DIR/${gid}.exit.txt") for $gid"
python3 - "$INTAKE_DIR" <<'PY'
import os, sys, json, base64, hashlib
d=sys.argv[1]
gid="p6a01"
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
j=json.loads(open(body,'rb').read().decode())
enc=j.get('encoding')
print(gid,"encoding",enc,"size",j.get('size'),"sha",j.get('sha'))
if enc=='base64':
  b=base64.b64decode(j.get('content',''))
  print(gid,"decoded",len(b),"match",len(b)==j.get('size'))
  calc=hashlib.sha1(b"blob %d\0"%len(b)+b).hexdigest()
  print(gid,"blob",j.get('sha'),calc,calc==j.get('sha'))
  out=os.path.join(d,f"DATA.{gid}.evidence-authority-supplement.json")
  open(out,'wb').write(b)
  print(gid,"wrote",out,hashlib.sha256(b).hexdigest())
else:
  print(gid,"NEEDS BLOB API fallback, content len",len(j.get('content','')))
PY
