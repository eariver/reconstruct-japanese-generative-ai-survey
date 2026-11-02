#!/usr/bin/env bash
# P2 Phase G — SP supplement raw bytes (13, required primary), screening/evidence package details
set -uo pipefail
INTAKE_DIR="notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z"
REPO="eariver/japanese-generative-ai-survey"
REF_SP="c8d0ecc1c9566a2303ad3b4c42635d4b672650e4"
mkdir -p "$INTAKE_DIR"
declare -a SPECS=(
"p2g01|SP-supp-raw-d005|repos/${REPO}/contents/sources/SP-efficient-llm-2026/external/evidence-supplement/raw/supp-d005-fp8-abs.html?ref=${REF_SP}"
"p2g02|SP-supp-raw-d032|repos/${REPO}/contents/sources/SP-efficient-llm-2026/external/evidence-supplement/raw/supp-d032-v32exp-launch.html?ref=${REF_SP}"
"p2g03|SP-supp-raw-d061|repos/${REPO}/contents/sources/SP-efficient-llm-2026/external/evidence-supplement/raw/supp-d061-mooncake-abs.html?ref=${REF_SP}"
"p2g04|SP-supp-raw-d062a|repos/${REPO}/contents/sources/SP-efficient-llm-2026/external/evidence-supplement/raw/supp-d062-sarathi2023-abs.html?ref=${REF_SP}"
"p2g05|SP-supp-raw-d062b|repos/${REPO}/contents/sources/SP-efficient-llm-2026/external/evidence-supplement/raw/supp-d062-sarathiserve2024-abs.html?ref=${REF_SP}"
"p2g06|SP-supp-raw-d093a|repos/${REPO}/contents/sources/SP-efficient-llm-2026/external/evidence-supplement/raw/supp-d093-swepro-abs.html?ref=${REF_SP}"
"p2g07|SP-supp-raw-d093h|repos/${REPO}/contents/sources/SP-efficient-llm-2026/external/evidence-supplement/raw/supp-d093-swepro-html.html?ref=${REF_SP}"
"p2g08|SP-supp-raw-d094|repos/${REPO}/contents/sources/SP-efficient-llm-2026/external/evidence-supplement/raw/supp-d094-tbench2-abs.html?ref=${REF_SP}"
"p2g09|SP-supp-raw-d098|repos/${REPO}/contents/sources/SP-efficient-llm-2026/external/evidence-supplement/raw/supp-d098-ruler-abs.html?ref=${REF_SP}"
"p2g10|SP-supp-raw-d112|repos/${REPO}/contents/sources/SP-efficient-llm-2026/external/evidence-supplement/raw/supp-d112-pyramidkv-abs.html?ref=${REF_SP}"
"p2g11|SP-supp-raw-d117|repos/${REPO}/contents/sources/SP-efficient-llm-2026/external/evidence-supplement/raw/supp-d117-deebert-abs.html?ref=${REF_SP}"
"p2g12|SP-supp-raw-d119|repos/${REPO}/contents/sources/SP-efficient-llm-2026/external/evidence-supplement/raw/supp-d119-genai-perf-docs.html?ref=${REF_SP}"
"p2g13|SP-supp-raw-d139|repos/${REPO}/contents/sources/SP-efficient-llm-2026/external/evidence-supplement/raw/supp-d139-doremi-abs.html?ref=${REF_SP}"
"p2g14|SP-screening-interactive-decisions|repos/${REPO}/contents/sources/SP-efficient-llm-2026/screening/v2/accepted/24bac6aa5c849eb2f6ac46f2162c7333137230cfec2610e908815a0e591b045d/interactive-decisions.json?ref=${REF_SP}"
"p2g15|SP-evidence-package|repos/${REPO}/contents/sources/SP-efficient-llm-2026/evidence/v2/accepted/dba89409c1cdcfb6a8b319ef35e0e1ee1b5ffdc74cad4715dbe44e10345e5603/package.json?ref=${REF_SP}"
"p2g16|SP-evidence-interactive-accepted|repos/${REPO}/contents/sources/SP-efficient-llm-2026/evidence/v2/accepted/dba89409c1cdcfb6a8b319ef35e0e1ee1b5ffdc74cad4715dbe44e10345e5603/interactive-evidence.json?ref=${REF_SP}"
)
for spec in "${SPECS[@]}"; do
  IFS='|' read -r gid label apipath <<< "$spec"
  echo "=== $gid $label ==="
  echo "gh api -i \"$apipath\"" > "$INTAKE_DIR/${gid}.command.txt"
  echo "$label" > "$INTAKE_DIR/${gid}.label.txt"
  echo "$apipath" > "$INTAKE_DIR/${gid}.url.txt"
  echo "$REF_SP" > "$INTAKE_DIR/${gid}.ref.txt"
  date -u +%Y-%m-%dT%H:%M:%SZ > "$INTAKE_DIR/${gid}.time.txt"
  echo $$ > "$INTAKE_DIR/${gid}.pid.txt"
  gh api -i "$apipath" > "$INTAKE_DIR/${gid}.stdout.raw" 2> "$INTAKE_DIR/${gid}.stderr.txt"
  echo -n "$?" > "$INTAKE_DIR/${gid}.exit.txt"
  echo "exit $(cat "$INTAKE_DIR/${gid}.exit.txt") for $gid"
done
echo "Phase G done."
python3 - "$INTAKE_DIR" <<'PY'
import os, sys, json, base64, hashlib, glob
d=sys.argv[1]
ids=sorted([os.path.basename(p).split('.')[0] for p in glob.glob(os.path.join(d,"p2g*.command.txt"))])
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
    b=base64.b64decode(j.get('content',''))
    print(gid,"decoded",len(b),"reported",j.get('size'),"match",len(b)==j.get('size'))
    rep=j.get('sha',''); calc=hashlib.sha1(b"blob %d\0"%len(b)+b).hexdigest()
    print(gid,"blob",rep,calc,rep==calc)
    name=j.get('path','').split('/')[-1] or gid
    out=os.path.join(d,f"DATA.{gid}.{name}")
    open(out,'wb').write(b)
    print(gid,"wrote",out,hashlib.sha256(b).hexdigest())
  elif isinstance(j,list):
    print(gid,"listing",len(j))
  else:
    print(gid,"dict",list(j.keys())[:10])
PY
echo "Phase G split done."
