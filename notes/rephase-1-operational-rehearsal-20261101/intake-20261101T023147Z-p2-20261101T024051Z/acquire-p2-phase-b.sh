#!/usr/bin/env bash
# P2 Phase B — State-selected accepted graph (aggregated, no per-task dump) + Raw + worklogs + publication
set -uo pipefail
INTAKE_DIR="notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z"
REPO="eariver/japanese-generative-ai-survey"
REF_W34="774dd39a951c9ac3818e83dfffd4c7666efb0a20"
REF_SP="c8d0ecc1c9566a2303ad3b4c42635d4b672650e4"
mkdir -p "$INTAKE_DIR"
declare -a SPECS=(
"p2b01|W34-discovery-jsonl|repos/${REPO}/contents/sources/2026-W34/discovery/discovery-v2.jsonl?ref=${REF_W34}"
"p2b02|W34-discovery-accepted|repos/${REPO}/contents/sources/2026-W34/discovery/discovery-accepted-v2.json?ref=${REF_W34}"
"p2b03|W34-screening-sol-authority|repos/${REPO}/contents/sources/2026-W34/screening/decisions/sol-screening-decision-authority-20260904-r1.json?ref=${REF_W34}"
"p2b04|W34-screening-coverage-supplement|repos/${REPO}/contents/sources/2026-W34/screening/decisions/sol-screening-coverage-supplement-20260905-r1.json?ref=${REF_W34}"
"p2b05|W34-screening-accepted-415|repos/${REPO}/contents/sources/2026-W34/screening/v2/accepted/41503363e1aef269ead56ac056b7f58e53eb1934d5de926f2cc49ee3bd84ccc3/screening-accepted.json?ref=${REF_W34}"
"p2b06|W34-evidence-accepted-647|repos/${REPO}/contents/sources/2026-W34/evidence/v2/accepted/647cde464d92935c1ca633ade62bcbf7ebe88c458cc8b3848bae8d2fc4794831/evidence-accepted.json?ref=${REF_W34}"
"p2b07|W34-evidence-package-647|repos/${REPO}/contents/sources/2026-W34/evidence/v2/accepted/647cde464d92935c1ca633ade62bcbf7ebe88c458cc8b3848bae8d2fc4794831/package.json?ref=${REF_W34}"
"p2b08|W34-views-accepted-e2e6|repos/${REPO}/contents/sources/2026-W34/evidence/v2/views/accepted/e2e644bcc97ac664949b272fca919923385af6192c65b5a3566e30382b0ca7ba/edition-views-accepted.json?ref=${REF_W34}"
"p2b09|W34-ledger|repos/${REPO}/contents/sources/2026-W34/materiality-ledger-v2.json?ref=${REF_W34}"
"p2b10|W34-completeness|repos/${REPO}/contents/sources/2026-W34/profile-completeness-v2.json?ref=${REF_W34}"
"p2b11|W34-matrix|repos/${REPO}/contents/sources/2026-W34/candidate-matrix-v2.json?ref=${REF_W34}"
"p2b12|W34-selection|repos/${REPO}/contents/sources/2026-W34/candidate-selection-v2.json?ref=${REF_W34}"
"p2b13|W34-architecture|repos/${REPO}/contents/sources/2026-W34/architecture-v2.json?ref=${REF_W34}"
"p2b14|W34-arch-summary|repos/${REPO}/contents/sources/2026-W34/architecture-review-summary-v2.json?ref=${REF_W34}"
"p2b15|W34-arch-attention|repos/${REPO}/contents/sources/2026-W34/architecture-review-attention-v2.json?ref=${REF_W34}"
"p2b16|W34-event-crosswalk-v1|repos/${REPO}/contents/sources/2026-W34/screening/input/event-discovery-crosswalk-v0.1.json?ref=${REF_W34}"
"p2b17|W34-event-crosswalk-v2|repos/${REPO}/contents/sources/2026-W34/screening/input/event-discovery-crosswalk-v0.2.json?ref=${REF_W34}"
"p2b18|W34-interactive-evidence-blob|repos/${REPO}/git/blobs/697bfc5c5c9c317795d010aca353592802fe4f74"
"p2b19|W34-event-discovery-blob|repos/${REPO}/git/blobs/06eb26bbaafd08782a5158102e9a67885809b434"
"p2b20|SP-discovery-jsonl|repos/${REPO}/contents/sources/SP-efficient-llm-2026/discovery/discovery-v2.jsonl?ref=${REF_SP}"
"p2b21|SP-discovery-accepted|repos/${REPO}/contents/sources/SP-efficient-llm-2026/discovery/discovery-accepted-v2.json?ref=${REF_SP}"
"p2b22|SP-screening-accepted|repos/${REPO}/contents/sources/SP-efficient-llm-2026/screening/v2/accepted/24bac6aa5c849eb2f6ac46f2162c7333137230cfec2610e908815a0e591b045d/screening-accepted.json?ref=${REF_SP}"
"p2b23|SP-evidence-accepted|repos/${REPO}/contents/sources/SP-efficient-llm-2026/evidence/v2/accepted/dba89409c1cdcfb6a8b319ef35e0e1ee1b5ffdc74cad4715dbe44e10345e5603/evidence-accepted.json?ref=${REF_SP}"
"p2b24|SP-views-accepted|repos/${REPO}/contents/sources/SP-efficient-llm-2026/evidence/v2/views/accepted/2bf475f518d80c8088dff7a67a0bc5cae5e2fa5c9a309d56695e66b1d54d7762/edition-views-accepted.json?ref=${REF_SP}"
"p2b25|SP-ledger|repos/${REPO}/contents/sources/SP-efficient-llm-2026/materiality-ledger-v2.json?ref=${REF_SP}"
"p2b26|SP-completeness|repos/${REPO}/contents/sources/SP-efficient-llm-2026/profile-completeness-v2.json?ref=${REF_SP}"
"p2b27|SP-matrix|repos/${REPO}/contents/sources/SP-efficient-llm-2026/candidate-matrix-v2.json?ref=${REF_SP}"
"p2b28|SP-selection|repos/${REPO}/contents/sources/SP-efficient-llm-2026/candidate-selection-v2.json?ref=${REF_SP}"
"p2b29|SP-architecture|repos/${REPO}/contents/sources/SP-efficient-llm-2026/architecture-v2.json?ref=${REF_SP}"
"p2b30|SP-arch-summary|repos/${REPO}/contents/sources/SP-efficient-llm-2026/architecture-review-summary-v2.json?ref=${REF_SP}"
"p2b31|SP-arch-attention|repos/${REPO}/contents/sources/SP-efficient-llm-2026/architecture-review-attention-v2.json?ref=${REF_SP}"
"p2b32|SP-research-scope|repos/${REPO}/contents/sources/SP-efficient-llm-2026/research-scope-v2.json?ref=${REF_SP}"
"p2b33|SP-pub-reader-manuscript|repos/${REPO}/contents/sources/SP-efficient-llm-2026/publication/v2/reader-manuscript-v2.json?ref=${REF_SP}"
"p2b34|SP-pub-list|repos/${REPO}/contents/sources/SP-efficient-llm-2026/publication/v2?ref=${REF_SP}"
"p2b35|SP-exec-index|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/index.md?ref=${REF_SP}"
"p2b36|SP-exec-evidence-input-list|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/evidence-interactive-input?ref=${REF_SP}"
"p2b37|SP-exec-evidence-input-r2-list|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/evidence-interactive-input-r2?ref=${REF_SP}"
"p2b38|SP-exec-reviews-list|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/reviews?ref=${REF_SP}"
"p2b39|SP-exec-sessions-list|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/sessions?ref=${REF_SP}"
"p2b40|SP-screening-v2-list|repos/${REPO}/contents/sources/SP-efficient-llm-2026/screening/v2?ref=${REF_SP}"
"p2b41|SP-evidence-v2-list|repos/${REPO}/contents/sources/SP-efficient-llm-2026/evidence/v2?ref=${REF_SP}"
"p2b42|SP-gates-reviews-list|repos/${REPO}/contents/sources/SP-efficient-llm-2026/gates/reviews?ref=${REF_SP}"
"p2b43|W34-exec-freeze-worklog|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-freeze/session-worklog.md?ref=${REF_W34}"
"p2b44|W34-exec-preview-r2-worklog|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-human-preview-r2-issue491-repair/session-worklog.md?ref=${REF_W34}"
"p2b45|W34-gates-arch-r3|repos/${REPO}/contents/sources/2026-W34/gates/reviews/architecture-r3.json?ref=${REF_W34}"
"p2b46|W34-gates-pub-r2|repos/${REPO}/contents/sources/2026-W34/gates/reviews/publication-r2.json?ref=${REF_W34}"
"p2b47|W34-gates-pub-r3|repos/${REPO}/contents/sources/2026-W34/gates/reviews/publication-r3.json?ref=${REF_W34}"
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
echo "Phase B GETs done. Splitting/verifying."
python3 - "$INTAKE_DIR" <<'PY'
import os, sys, json, base64, hashlib, glob
d=sys.argv[1]
ids=sorted([os.path.basename(p).split('.')[0] for p in glob.glob(os.path.join(d,"p2b*.command.txt"))])
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
    for e in j[:80]:
      print(f"  - {e.get('type')} {e.get('path')} size={e.get('size')} sha={e.get('sha')}")
  else:
    print(f"{gid}: dict keys {list(j.keys())[:12]}")
PY
echo "Phase B split/verify done."
