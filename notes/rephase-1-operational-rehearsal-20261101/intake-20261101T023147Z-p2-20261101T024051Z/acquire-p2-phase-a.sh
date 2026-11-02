#!/usr/bin/env bash
# P2 Phase A — checkpoints + navigation listings + SP reader (fixed refs only)
set -uo pipefail
INTAKE_DIR="notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z"
REPO="eariver/japanese-generative-ai-survey"
REF_W34="774dd39a951c9ac3818e83dfffd4c7666efb0a20"
REF_SP="c8d0ecc1c9566a2303ad3b4c42635d4b672650e4"
mkdir -p "$INTAKE_DIR"
# ID|label|api-path  (no tokens)
declare -a SPECS=(
"p2a01|W34-check-ISSUE_INITIALIZED|repos/${REPO}/contents/sources/2026-W34/orchestration/v2/checkpoints/ISSUE_INITIALIZED.json?ref=${REF_W34}"
"p2a02|W34-check-DISCOVERY_COLLECTED|repos/${REPO}/contents/sources/2026-W34/orchestration/v2/checkpoints/DISCOVERY_COLLECTED.json?ref=${REF_W34}"
"p2a03|W34-check-CANDIDATES_NORMALIZED|repos/${REPO}/contents/sources/2026-W34/orchestration/v2/checkpoints/CANDIDATES_NORMALIZED.json?ref=${REF_W34}"
"p2a04|W34-check-EVIDENCE_REVIEWED|repos/${REPO}/contents/sources/2026-W34/orchestration/v2/checkpoints/EVIDENCE_REVIEWED.json?ref=${REF_W34}"
"p2a05|W34-check-SELECTION_COMPLETE|repos/${REPO}/contents/sources/2026-W34/orchestration/v2/checkpoints/SELECTION_COMPLETE.json?ref=${REF_W34}"
"p2a06|W34-check-ARCHITECTURE_ESTABLISHED|repos/${REPO}/contents/sources/2026-W34/orchestration/v2/checkpoints/ARCHITECTURE_ESTABLISHED.json?ref=${REF_W34}"
"p2a07|W34-check-DRAFT_COMPLETE|repos/${REPO}/contents/sources/2026-W34/orchestration/v2/checkpoints/DRAFT_COMPLETE.json?ref=${REF_W34}"
"p2a08|W34-check-RELEASE_CANDIDATE|repos/${REPO}/contents/sources/2026-W34/orchestration/v2/checkpoints/RELEASE_CANDIDATE.json?ref=${REF_W34}"
"p2a09|W34-check-FROZEN|repos/${REPO}/contents/sources/2026-W34/orchestration/v2/checkpoints/FROZEN.json?ref=${REF_W34}"
"p2a10|W34-check-VALIDATED_DRAFT|repos/${REPO}/contents/sources/2026-W34/orchestration/v2/checkpoints/VALIDATED_DRAFT.json?ref=${REF_W34}"
"p2a11|SP-check-ISSUE_INITIALIZED|repos/${REPO}/contents/sources/SP-efficient-llm-2026/orchestration/v2/checkpoints/ISSUE_INITIALIZED.json?ref=${REF_SP}"
"p2a12|SP-check-DISCOVERY_COLLECTED|repos/${REPO}/contents/sources/SP-efficient-llm-2026/orchestration/v2/checkpoints/DISCOVERY_COLLECTED.json?ref=${REF_SP}"
"p2a13|SP-check-CANDIDATES_NORMALIZED|repos/${REPO}/contents/sources/SP-efficient-llm-2026/orchestration/v2/checkpoints/CANDIDATES_NORMALIZED.json?ref=${REF_SP}"
"p2a14|SP-check-EVIDENCE_REVIEWED|repos/${REPO}/contents/sources/SP-efficient-llm-2026/orchestration/v2/checkpoints/EVIDENCE_REVIEWED.json?ref=${REF_SP}"
"p2a15|SP-check-SELECTION_COMPLETE|repos/${REPO}/contents/sources/SP-efficient-llm-2026/orchestration/v2/checkpoints/SELECTION_COMPLETE.json?ref=${REF_SP}"
"p2a16|SP-check-ARCHITECTURE_ESTABLISHED|repos/${REPO}/contents/sources/SP-efficient-llm-2026/orchestration/v2/checkpoints/ARCHITECTURE_ESTABLISHED.json?ref=${REF_SP}"
"p2a17|SP-check-DRAFT_COMPLETE|repos/${REPO}/contents/sources/SP-efficient-llm-2026/orchestration/v2/checkpoints/DRAFT_COMPLETE.json?ref=${REF_SP}"
"p2a18|SP-check-RELEASE_CANDIDATE|repos/${REPO}/contents/sources/SP-efficient-llm-2026/orchestration/v2/checkpoints/RELEASE_CANDIDATE.json?ref=${REF_SP}"
"p2a19|SP-check-FROZEN|repos/${REPO}/contents/sources/SP-efficient-llm-2026/orchestration/v2/checkpoints/FROZEN.json?ref=${REF_SP}"
"p2a20|SP-list-discovery|repos/${REPO}/contents/sources/SP-efficient-llm-2026/discovery?ref=${REF_SP}"
"p2a21|SP-list-screening|repos/${REPO}/contents/sources/SP-efficient-llm-2026/screening?ref=${REF_SP}"
"p2a22|SP-list-evidence|repos/${REPO}/contents/sources/SP-efficient-llm-2026/evidence?ref=${REF_SP}"
"p2a23|SP-list-execution|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution?ref=${REF_SP}"
"p2a24|SP-list-raw|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw?ref=${REF_SP}"
"p2a25|SP-list-gates|repos/${REPO}/contents/sources/SP-efficient-llm-2026/gates?ref=${REF_SP}"
"p2a26|SP-list-orchestration|repos/${REPO}/contents/sources/SP-efficient-llm-2026/orchestration?ref=${REF_SP}"
"p2a27|SP-list-publication|repos/${REPO}/contents/sources/SP-efficient-llm-2026/publication?ref=${REF_SP}"
"p2a28|SP-reader-tex|repos/${REPO}/contents/surveys/special/efficient-llm-2026/main.tex?ref=${REF_SP}"
"p2a29|SP-reader-bib|repos/${REPO}/contents/surveys/special/efficient-llm-2026/references.bib?ref=${REF_SP}"
"p2a30|SP-reader-pdf-blob|repos/${REPO}/git/blobs/a59747015c68361d0022637dee9d58b1c09eaef5"
)
for spec in "${SPECS[@]}"; do
  IFS='|' read -r gid label apipath <<< "$spec"
  echo "=== $gid $label ==="
  echo "gh api -i \"$apipath\"" > "$INTAKE_DIR/${gid}.command.txt"
  echo "$label" > "$INTAKE_DIR/${gid}.label.txt"
  echo "$apipath" > "$INTAKE_DIR/${gid}.url.txt"
  if [[ "$apipath" == *"$REF_W34"* ]]; then echo "$REF_W34" > "$INTAKE_DIR/${gid}.ref.txt"; elif [[ "$apipath" == *"$REF_SP"* ]]; then echo "$REF_SP" > "$INTAKE_DIR/${gid}.ref.txt"; else echo "blob-sha-pinned (no ref, exact blob)" > "$INTAKE_DIR/${gid}.ref.txt"; fi
  date -u +%Y-%m-%dT%H:%M:%SZ > "$INTAKE_DIR/${gid}.time.txt"
  echo $$ > "$INTAKE_DIR/${gid}.pid.txt"
  gh api -i "$apipath" > "$INTAKE_DIR/${gid}.stdout.raw" 2> "$INTAKE_DIR/${gid}.stderr.txt"
  echo -n "$?" > "$INTAKE_DIR/${gid}.exit.txt"
  echo "exit $(cat "$INTAKE_DIR/${gid}.exit.txt") for $gid"
done
echo "Phase A GETs done. Splitting/verifying."
python3 - "$INTAKE_DIR" <<'PY'
import os, sys, json, base64, hashlib
d=sys.argv[1]
import glob
ids=sorted([os.path.basename(p).split('.')[0] for p in glob.glob(os.path.join(d,"p2a*.command.txt"))])
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
      # blob api returns sha1 of blob; contents api also blob sha1
      calc=hashlib.sha1(b"blob %d\0"%len(b)+b).hexdigest()
      print(f"{gid}: reported blob {rep_sha}, calc {calc}, match={rep_sha==calc}")
      name=os.path.basename(j.get('path','') or gid)
      if not name or name=='':
        # blob api has no path; use label
        label=open(os.path.join(d,gid+".label.txt")).read().strip()
        name=label+".bin"
      out=os.path.join(d,f"DATA.{gid}.{name}")
      open(out,'wb').write(b)
      print(f"{gid}: wrote {out} sha256 {hashlib.sha256(b).hexdigest()}")
    else:
      print(f"{gid}: dict encoding {enc}")
  elif isinstance(j,list):
    print(f"{gid}: listing {len(j)} entries")
    for e in j[:60]:
      print(f"  - {e.get('type')} {e.get('path')} size={e.get('size')} sha={e.get('sha')}")
  else:
    print(f"{gid}: dict keys {list(j.keys())[:12]}")
PY
echo "Phase A split/verify done."
