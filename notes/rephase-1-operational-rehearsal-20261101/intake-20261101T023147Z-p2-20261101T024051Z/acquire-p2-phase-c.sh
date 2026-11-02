#!/usr/bin/env bash
# P2 Phase C — original unprojected inputs, Raw closure, publication baseline, repair worklogs
set -uo pipefail
INTAKE_DIR="notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z"
REPO="eariver/japanese-generative-ai-survey"
REF_W34="774dd39a951c9ac3818e83dfffd4c7666efb0a20"
REF_SP="c8d0ecc1c9566a2303ad3b4c42635d4b672650e4"
mkdir -p "$INTAKE_DIR"
declare -a SPECS=(
"p2c01|SP-interactive-evidence-orig|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/evidence-interactive-input/interactive-evidence.json?ref=${REF_SP}"
"p2c02|SP-task-targets-orig|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/evidence-interactive-input/task-targets.json?ref=${REF_SP}"
"p2c03|SP-interactive-evidence-r2|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/evidence-interactive-input-r2/interactive-evidence-r2.json?ref=${REF_SP}"
"p2c04|SP-pub-candidate|repos/${REPO}/contents/sources/SP-efficient-llm-2026/publication/v2/publication-candidate-v2.json?ref=${REF_SP}"
"p2c05|SP-pub-surface-gate|repos/${REPO}/contents/sources/SP-efficient-llm-2026/publication/v2/reader-surface-gate-v2.json?ref=${REF_SP}"
"p2c06|SP-pub-semantic|repos/${REPO}/contents/sources/SP-efficient-llm-2026/publication/v2/semantic-editorial-review-v2.json?ref=${REF_SP}"
"p2c07|SP-pub-visual|repos/${REPO}/contents/sources/SP-efficient-llm-2026/publication/v2/visual-review-v2.json?ref=${REF_SP}"
"p2c08|SP-pub-quality|repos/${REPO}/contents/sources/SP-efficient-llm-2026/publication/v2/quality-regression-bundle-v2.json?ref=${REF_SP}"
"p2c09|SP-pub-freeze-record|repos/${REPO}/contents/sources/SP-efficient-llm-2026/publication/v2/freeze-record-v2.json?ref=${REF_SP}"
"p2c10|SP-pub-manifest|repos/${REPO}/contents/sources/SP-efficient-llm-2026/publication/v2/release-manifest-v2.json?ref=${REF_SP}"
"p2c11|SP-pub-merge|repos/${REPO}/contents/sources/SP-efficient-llm-2026/publication/v2/merge-verification-v2.json?ref=${REF_SP}"
"p2c12|SP-pub-release|repos/${REPO}/contents/sources/SP-efficient-llm-2026/publication/v2/release-record-v2.json?ref=${REF_SP}"
"p2c13|SP-pub-revalidation|repos/${REPO}/contents/sources/SP-efficient-llm-2026/publication/v2/publication-surface-revalidation-r1.json?ref=${REF_SP}"
"p2c14|SP-raw-obs-negative|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-negative-space-2026-09-21.md?ref=${REF_SP}"
"p2c15|SP-raw-obs-method|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-benchmarks-methodology.md?ref=${REF_SP}"
"p2c16|SP-raw-obs-capstone|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-capstones-2026.md?ref=${REF_SP}"
"p2c17|SP-raw-obs-d01|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-d01-fundamentals.md?ref=${REF_SP}"
"p2c18|SP-raw-obs-d02|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-d02-scaling-training.md?ref=${REF_SP}"
"p2c19|SP-raw-obs-d03|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-d03-moe.md?ref=${REF_SP}"
"p2c20|SP-raw-obs-d04|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-d04-attention-kvcache.md?ref=${REF_SP}"
"p2c21|SP-raw-obs-d05|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-d05-decoding.md?ref=${REF_SP}"
"p2c22|SP-raw-obs-d06|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-d06-precision.md?ref=${REF_SP}"
"p2c23|SP-raw-obs-d07|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-d07-representation-local.md?ref=${REF_SP}"
"p2c24|SP-raw-obs-d08|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-d08-serving.md?ref=${REF_SP}"
"p2c25|SP-raw-obs-d09|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-d09-distillation.md?ref=${REF_SP}"
"p2c26|SP-raw-obs-d10|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-d10-specialization-jev.md?ref=${REF_SP}"
"p2c27|SP-raw-obs-r2-g12|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g12-distributed-training.md?ref=${REF_SP}"
"p2c28|SP-raw-obs-r2-g13|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g13-kv-management.md?ref=${REF_SP}"
"p2c29|SP-raw-obs-r2-g14|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g14-conditional-depth.md?ref=${REF_SP}"
"p2c30|SP-raw-obs-r2-g15|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g15-harness.md?ref=${REF_SP}"
"p2c31|SP-raw-obs-r2-g16|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g16-capstone-firstparty.md?ref=${REF_SP}"
"p2c32|SP-raw-obs-r2-g17|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g17-g18-routing-lowbit.md?ref=${REF_SP}"
"p2c33|SP-raw-obs-r2-g19|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g19-g20-data-jev.md?ref=${REF_SP}"
"p2c34|SP-raw-obs-r3-d09|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-r3-d09-depth-check.md?ref=${REF_SP}"
"p2c35|SP-raw-obs-r3-g21|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-r3-g21-conditional-memory.md?ref=${REF_SP}"
"p2c36|SP-raw-obs-r3-g22|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-r3-g22-test-time-compute.md?ref=${REF_SP}"
"p2c37|SP-raw-obs-r3-g23|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-r3-g23-model-routing.md?ref=${REF_SP}"
"p2c38|SP-raw-obs-r4-x|repos/${REPO}/contents/sources/SP-efficient-llm-2026/raw/discovery-observations-r4-x-followup.md?ref=${REF_SP}"
"p2c39|W34-reader-main-tex|repos/${REPO}/contents/surveys/weekly/2026-W34/main.tex?ref=${REF_W34}"
"p2c40|W34-reader-bib|repos/${REPO}/contents/surveys/weekly/2026-W34/references.bib?ref=${REF_W34}"
"p2c41|W34-reader-sec00|repos/${REPO}/contents/surveys/weekly/2026-W34/sections/00-frontmatter.tex?ref=${REF_W34}"
"p2c42|W34-reader-sec10|repos/${REPO}/contents/surveys/weekly/2026-W34/sections/10-agent-control-plane.tex?ref=${REF_W34}"
"p2c43|W34-reader-sec20|repos/${REPO}/contents/surveys/weekly/2026-W34/sections/20-agent-workflows.tex?ref=${REF_W34}"
"p2c44|W34-reader-sec30|repos/${REPO}/contents/surveys/weekly/2026-W34/sections/30-safety-security.tex?ref=${REF_W34}"
"p2c45|W34-reader-sec40|repos/${REPO}/contents/surveys/weekly/2026-W34/sections/40-model-economics.tex?ref=${REF_W34}"
"p2c46|W34-reader-sec50|repos/${REPO}/contents/surveys/weekly/2026-W34/sections/50-creative-multimodal.tex?ref=${REF_W34}"
"p2c47|W34-reader-sec60|repos/${REPO}/contents/surveys/weekly/2026-W34/sections/60-ecosystem-infrastructure.tex?ref=${REF_W34}"
"p2c48|W34-reader-sec70|repos/${REPO}/contents/surveys/weekly/2026-W34/sections/70-week-in-review.tex?ref=${REF_W34}"
"p2c49|W34-reader-sec99|repos/${REPO}/contents/surveys/weekly/2026-W34/sections/99-source-notes.tex?ref=${REF_W34}"
"p2c50|W34-screen-valid-r3|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-screening-evidence-after-sol-discovery-r2/validation/screening-stage-validation-r3.json?ref=${REF_W34}"
"p2c51|W34-evidence-valid-r1|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-screening-evidence-after-sol-discovery-r2/validation/evidence-stage-validation-r1.json?ref=${REF_W34}"
"p2c52|W34-selection-valid-r2|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-selection-c045-cluster-correction-r2/validation/selection-stage-validation-r2.json?ref=${REF_W34}"
"p2c53|W34-arch-valid-r1|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-architecture-after-sol-selection-r2/validation/architecture-stage-validation-r1.json?ref=${REF_W34}"
"p2c54|SP-evidence-valid-r1|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/evidence-stage-advance/validation/evidence-stage-validation-r1.json?ref=${REF_SP}"
"p2c55|SP-selection-valid-r1|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/selection-stage-advance/validation/selection-stage-validation-r1.json?ref=${REF_SP}"
"p2c56|SP-arch-valid-r1|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/architecture-stage-advance/validation/architecture-stage-validation-r1.json?ref=${REF_SP}"
"p2c57|SP-session-compat|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/sessions/ts001-reissue-evidence-compat-20260922.md?ref=${REF_SP}"
"p2c58|SP-session-select-arch|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/sessions/ts001-reissue-selection-architecture-20260922.md?ref=${REF_SP}"
"p2c59|SP-review-sol-evidence-pass|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/reviews/sol-evidence-review-pass-20260922.md?ref=${REF_SP}"
"p2c60|SP-compat-list|repos/${REPO}/contents/sources/SP-efficient-llm-2026/execution/compat?ref=${REF_SP}"
)
for spec in "${SPECS[@]}"; do
  IFS='|' read -r gid label apipath <<< "$spec"
  echo "=== $gid $label ==="
  echo "gh api -i \"$apipath\"" > "$INTAKE_DIR/${gid}.command.txt"
  echo "$label" > "$INTAKE_DIR/${gid}.label.txt"
  echo "$apipath" > "$INTAKE_DIR/${gid}.url.txt"
  if [[ "$apipath" == *"$REF_W34"* ]]; then echo "$REF_W34" > "$INTAKE_DIR/${gid}.ref.txt"; elif [[ "$apipath" == *"$REF_SP"* ]]; then echo "$REF_SP" > "$INTAKE_DIR/${gid}.ref.txt"; else echo "blob-sha-pinned" > "$INTAKE_DIR/${gid}.ref.txt"; fi
  date -u +%Y-%m-%dT%H:%M:%SZ > "$INTAKE_DIR/${gid}.time.txt"
  echo $$ > "$INTAKE_DIR/${gid}.pid.txt"
  gh api -i "$apipath" > "$INTAKE_DIR/${gid}.stdout.raw" 2> "$INTAKE_DIR/${gid}.stderr.txt"
  echo -n "$?" > "$INTAKE_DIR/${gid}.exit.txt"
  echo "exit $(cat "$INTAKE_DIR/${gid}.exit.txt") for $gid"
done
echo "Phase C GETs done. Splitting/verifying."
python3 - "$INTAKE_DIR" <<'PY'
import os, sys, json, base64, hashlib, glob
d=sys.argv[1]
ids=sorted([os.path.basename(p).split('.')[0] for p in glob.glob(os.path.join(d,"p2c*.command.txt"))])
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
echo "Phase C split/verify done."
