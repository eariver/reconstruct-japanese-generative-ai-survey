#!/usr/bin/env bash
# P5 phase 1 — execution subtree recursive metadata (exact execution tree SHA only) + minimal binding worklogs
set -uo pipefail
INTAKE_DIR="notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p5-20261101T114236Z"
REPO="eariver/japanese-generative-ai-survey"
REF_SP="c8d0ecc1c9566a2303ad3b4c42635d4b672650e4"
EXEC_SHA="12de971e46661fc86dfd2ea84580187bab562e06"
mkdir -p "$INTAKE_DIR"
declare -a SPECS=(
"p5e01|SP-exec-recursive-tree|repos/${REPO}/git/trees/${EXEC_SHA}?recursive=1"
"p5m01|SP-evidence-consumption-r2|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/reviews/evidence-authority-consumption-package-r2.md?ref=${REF_SP}"
"p5m02|SP-evidence-consumption-r1|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/reviews/evidence-authority-consumption-package-r1.md?ref=${REF_SP}"
)
for spec in "${SPECS[@]}"; do
  IFS='|' read -r gid label apipath <<< "$spec"
  echo "=== $gid $label ==="
  echo "gh api -i \"$apipath\"" > "$INTAKE_DIR/${gid}.command.txt"
  echo "$label" > "$INTAKE_DIR/${gid}.label.txt"
  echo "$apipath" > "$INTAKE_DIR/${gid}.url.txt"
  if [[ "$apipath" == *"$REF_SP"* ]]; then echo "$REF_SP" > "$INTAKE_DIR/${gid}.ref.txt"; else echo "exact execution tree SHA ${EXEC_SHA} from captured c8 sources listing (no whole-repo tree, no current main)" > "$INTAKE_DIR/${gid}.ref.txt"; fi
  date -u +%Y-%m-%dT%H:%M:%SZ > "$INTAKE_DIR/${gid}.time.txt"
  echo $$ > "$INTAKE_DIR/${gid}.pid.txt"
  gh api -i "$apipath" > "$INTAKE_DIR/${gid}.stdout.raw" 2> "$INTAKE_DIR/${gid}.stderr.txt"
  echo -n "$?" > "$INTAKE_DIR/${gid}.exit.txt"
  echo "exit $(cat "$INTAKE_DIR/${gid}.exit.txt") for $gid"
done
echo "P5 phase1 done. Splitting/verifying."
python3 - "$INTAKE_DIR" <<'PY'
import os, sys, json, base64, hashlib, glob
d=sys.argv[1]
ids=sorted([os.path.basename(p).split('.')[0] for p in glob.glob(os.path.join(d,"p5*.command.txt"))])
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
  if isinstance(j,dict) and j.get('truncated'):
    print(gid,"WARNING truncated tree")
  if isinstance(j,dict) and 'tree' in j:
    print(gid,"tree entries",len(j['tree']))
    # count evidence-bodies etc
    from collections import Counter
    c=Counter()
    for e in j['tree']:
      p=e.get('path','')
      if 'evidence-bodies' in p: c['evidence-bodies']+=1
      elif 'source-intake' in p: c['source-intake']+=1
      elif 'fulltext' in p.lower(): c['fulltext']+=1
      elif 'source-inspection' in p: c['source-inspection']+=1
      elif 'claim-extract' in p: c['claim-extract']+=1
      elif 'evidence-interactive' in p: c['evidence-interactive']+=1
    print(gid,"relevant",dict(c))
    # list evidence-bodies paths
    for e in j['tree']:
      if 'evidence-bodies' in e.get('path','') or 'fulltext' in e.get('path','').lower():
        print(" -",e.get('path'),e.get('sha'),e.get('size'))
  elif isinstance(j,dict) and 'content' in j:
    enc=j.get('encoding')
    if enc=='base64':
      b=base64.b64decode(j.get('content',''))
      print(gid,"decoded",len(b),"reported",j.get('size'),"match",len(b)==j.get('size'))
      rep=j.get('sha',''); calc=hashlib.sha1(b"blob %d\0"%len(b)+b).hexdigest()
      print(gid,"blob",rep,calc,rep==calc)
      name=j.get('path','').split('/')[-1] or gid
      out=os.path.join(d,f"DATA.{gid}.{name}")
      open(out,'wb').write(b)
      print(gid,"wrote",out,hashlib.sha256(b).hexdigest())
    else:
      print(gid,"encoding",enc,"size",j.get('size'),"content_len",len(j.get('content','')))
  elif isinstance(j,list):
    print(gid,"listing",len(j))
  else:
    print(gid,"keys",list(j.keys())[:10] if isinstance(j,dict) else type(j))
PY
echo "P5 phase1 split done."
