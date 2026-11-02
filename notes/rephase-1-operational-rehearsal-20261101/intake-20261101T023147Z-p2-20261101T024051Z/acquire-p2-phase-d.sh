#!/usr/bin/env bash
# P2 Phase D — Raw closure inventory, supplement, compat comparison listing, acceptance dir counts
set -uo pipefail
INTAKE_DIR="notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z"
REPO="eariver/japanese-generative-ai-survey"
REF_W34="774dd39a951c9ac3818e83dfffd4c7666efb0a20"
REF_SP="c8d0ecc1c9566a2303ad3b4c42635d4b672650e4"
mkdir -p "$INTAKE_DIR"
declare -a SPECS=(
"p2d01|W34-supplement|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-core-repair-r1/evidence-authority-supplement.json?ref=${REF_W34}"
"p2d02|W34-collectors-list|repos/${REPO}/contents/sources/2026-W34/collectors?ref=${REF_W34}"
"p2d03|W34-carryover-list|repos/${REPO}/contents/sources/2026-W34/carryover?ref=${REF_W34}"
"p2d04|SP-external-list|repos/${REPO}/contents/sources/SP-efficient-llm-2026/external?ref=${REF_SP}"
"p2d05|SP-compat-proj-list|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/compat/evidence-source-class-projection?ref=${REF_SP}"
"p2d06|SP-screening-accepted-list|repos/${REPO}/contents/sources/SP-efficient-llm-2026/screening/v2/accepted?ref=${REF_SP}"
"p2d07|SP-evidence-accepted-list|repos/${REPO}/contents/sources/SP-efficient-llm-2026/evidence/v2/accepted?ref=${REF_SP}"
"p2d08|SP-evidence-views-list|repos/${REPO}/contents/sources/SP-efficient-llm-2026/evidence/v2/views?ref=${REF_SP}"
"p2d09|SP-exec-compat-sessions-list|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/compat?ref=${REF_SP}"
"p2d10|SP-discovery-r2-jsonl|repos/${REPO}/contents/sources/SP-efficient-llm-2026/discovery/discovery-v2-r2.jsonl?ref=${REF_SP}"
"p2d11|W34-discovery-crosswalk-list|repos/${REPO}/contents/sources/2026-W34/discovery?ref=${REF_W34}"
"p2d12|W34-screening-input-list|repos/${REPO}/contents/sources/2026-W34/screening/input?ref=${REF_W34}"
)
for spec in "${SPECS[@]}"; do
  IFS='|' read -r gid label apipath <<< "$spec"
  echo "=== $gid $label ==="
  echo "gh api -i \"$apipath\"" > "$INTAKE_DIR/${gid}.command.txt"
  echo "$label" > "$INTAKE_DIR/${gid}.label.txt"
  echo "$apipath" > "$INTAKE_DIR/${gid}.url.txt"
  if [[ "$apipath" == *"$REF_W34"* ]]; then echo "$REF_W34" > "$INTAKE_DIR/${gid}.ref.txt"; else echo "$REF_SP" > "$INTAKE_DIR/${gid}.ref.txt"; fi
  date -u +%Y-%m-%dT%H:%M:%SZ > "$INTAKE_DIR/${gid}.time.txt"
  echo $$ > "$INTAKE_DIR/${gid}.pid.txt"
  gh api -i "$apipath" > "$INTAKE_DIR/${gid}.stdout.raw" 2> "$INTAKE_DIR/${gid}.stderr.txt"
  echo -n "$?" > "$INTAKE_DIR/${gid}.exit.txt"
  echo "exit $(cat "$INTAKE_DIR/${gid}.exit.txt") for $gid"
done
echo "Phase D done. Splitting/verifying."
python3 - "$INTAKE_DIR" <<'PY'
import os, sys, json, base64, hashlib, glob
d=sys.argv[1]
ids=sorted([os.path.basename(p).split('.')[0] for p in glob.glob(os.path.join(d,"p2d*.command.txt"))])
for gid in ids:
  raw=os.path.join(d,gid+".stdout.raw")
  hdr=os.path.join(d,gid+".headers.txt")
  body=os.path.join(d,gid+".body.json")
  if not os.path.exists(raw):
    continue
  data=open(raw,'rb').read()
  idx=data.find(b"\r\n\r\n")
  sep=4
  if idx<0:
    idx=data.find(b"\n\n")
    sep=2
  if idx>=0:
    open(hdr,'wb').write(data[:idx])
    open(body,'wb').write(data[idx+sep:])
  else:
    open(hdr,'wb').write(b"")
    open(body,'wb').write(data)
  try:
    j=json.loads(open(body,'rb').read().decode('utf-8',errors='replace'))
  except Exception as e:
    print(f"{gid}: body not JSON ({e})")
    continue
  if isinstance(j,dict) and 'content' in j:
    enc=j.get('encoding')
    if enc=='base64':
      b=base64.b64decode(j.get('content',''))
      rep_size=j.get('size')
      print(f"{gid}: decoded {len(b)} bytes, reported size {rep_size}, match={len(b)==rep_size}")
      rep_sha=j.get('sha','')
      calc=hashlib.sha1(b"blob %d\0"%len(b)+b).hexdigest()
      print(f"{gid}: reported blob {rep_sha}, calc {calc}, match={rep_sha==calc}")
      name=os.path.basename(j.get('path','') or gid)
      if not name:
        label=open(os.path.join(d,gid+".label.txt")).read().strip()
        name=label+".bin"
      out=os.path.join(d,f"DATA.{gid}.{name}")
      open(out,'wb').write(b)
      print(f"{gid}: wrote {out} sha256 {hashlib.sha256(b).hexdigest()}")
    else:
      print(f"{gid}: dict encoding {enc}")
  elif isinstance(j,list):
    print(f"{gid}: listing {len(j)} entries")
    for e in j[:100]:
      print(f"  - {e.get('type')} {e.get('path')} size={e.get('size')} sha={e.get('sha')}")
  else:
    print(f"{gid}: dict keys {list(j.keys())[:12]}")
PY
echo "Phase D split/verify done."
