#!/usr/bin/env bash
# P2 Phase E — supplement, compat ledger (comparison only), acceptance dir counts, carryover, gate refs
set -uo pipefail
INTAKE_DIR="notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z"
REPO="eariver/japanese-generative-ai-survey"
REF_W34="774dd39a951c9ac3818e83dfffd4c7666efb0a20"
REF_SP="c8d0ecc1c9566a2303ad3b4c42635d4b672650e4"
mkdir -p "$INTAKE_DIR"
declare -a SPECS=(
"p2e01|SP-supplement-list|repos/${REPO}/contents/sources/SP-efficient-llm-2026/external/evidence-supplement?ref=${REF_SP}"
"p2e02|SP-compat-ledger|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/compat/evidence-source-class-projection/projection-ledger.json?ref=${REF_SP}"
"p2e03|SP-compat-readme|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/compat/evidence-source-class-projection/README.md?ref=${REF_SP}"
"p2e04|SP-screening-accepted-dir|repos/${REPO}/contents/sources/SP-efficient-llm-2026/screening/v2/accepted/24bac6aa5c849eb2f6ac46f2162c7333137230cfec2610e908815a0e591b045d?ref=${REF_SP}"
"p2e05|SP-evidence-accepted-dir|repos/${REPO}/contents/sources/SP-efficient-llm-2026/evidence/v2/accepted/dba89409c1cdcfb6a8b319ef35e0e1ee1b5ffdc74cad4715dbe44e10345e5603?ref=${REF_SP}"
"p2e06|SP-views-accepted-hashdir|repos/${REPO}/contents/sources/SP-efficient-llm-2026/evidence/v2/views/accepted/2bf475f518d80c8088dff7a67a0bc5cae5e2fa5c9a309d56695e66b1d54d7762?ref=${REF_SP}"
"p2e07|W34-carryover-ledger|repos/${REPO}/contents/sources/2026-W34/carryover/carryover-ledger-v0.1.json?ref=${REF_W34}"
"p2e08|W34-collectors-arxiv-list|repos/${REPO}/contents/sources/2026-W34/collectors/arxiv?ref=${REF_W34}"
"p2e09|W34-collectors-gh-list|repos/${REPO}/contents/sources/2026-W34/collectors/github-releases?ref=${REF_W34}"
"p2e10|SP-gate-arch-r1|repos/${REPO}/contents/sources/SP-efficient-llm-2026/gates/reviews/architecture-r1.json?ref=${REF_SP}"
"p2e11|SP-gate-pub-r1|repos/${REPO}/contents/sources/SP-efficient-llm-2026/gates/reviews/publication-r1.json?ref=${REF_SP}"
"p2e12|SP-gate-pub-r2|repos/${REPO}/contents/sources/SP-efficient-llm-2026/gates/reviews/publication-r2.json?ref=${REF_SP}"
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
echo "Phase E done. Splitting/verifying."
python3 - "$INTAKE_DIR" <<'PY'
import os, sys, json, base64, hashlib, glob
d=sys.argv[1]
ids=sorted([os.path.basename(p).split('.')[0] for p in glob.glob(os.path.join(d,"p2e*.command.txt"))])
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
echo "Phase E split/verify done."
