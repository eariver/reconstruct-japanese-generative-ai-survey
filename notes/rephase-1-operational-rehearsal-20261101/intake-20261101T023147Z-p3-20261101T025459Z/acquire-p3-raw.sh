#!/usr/bin/env bash
# P3 — REQUIRED primary Raw bytes referenced in selected records (fixed refs only)
set -uo pipefail
INTAKE_DIR="notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p3-20261101T025459Z"
REPO="eariver/japanese-generative-ai-survey"
REF_W34="774dd39a951c9ac3818e83dfffd4c7666efb0a20"
REF_SP="c8d0ecc1c9566a2303ad3b4c42635d4b672650e4"
mkdir -p "$INTAKE_DIR"
declare -a SPECS=(
"p3a01|W34-gh-comfy|repos/${REPO}/contents/sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/comfy-org__comfyui.json?ref=${REF_W34}"
"p3a02|W34-gh-flashinfer|repos/${REPO}/contents/sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/flashinfer-ai__flashinfer.json?ref=${REF_W34}"
"p3a03|W34-gh-llamacpp|repos/${REPO}/contents/sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/ggml-org__llama.cpp.json?ref=${REF_W34}"
"p3a04|W34-gh-transformers|repos/${REPO}/contents/sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/huggingface__transformers.json?ref=${REF_W34}"
"p3a05|W34-gh-tensorrt|repos/${REPO}/contents/sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/nvidia__tensorrt-llm.json?ref=${REF_W34}"
"p3a06|W34-gh-sglang|repos/${REPO}/contents/sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/sgl-project__sglang.json?ref=${REF_W34}"
"p3a07|W34-gh-vllm|repos/${REPO}/contents/sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/vllm-project__vllm.json?ref=${REF_W34}"
"p3a08|W34-gap-agent-inherit|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/arxiv-agent-inheritance.json?ref=${REF_W34}"
"p3a09|W34-gap-corun|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/arxiv-corun.json?ref=${REF_W34}"
"p3a10|W34-gap-egogazelite|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/arxiv-egogazelite.json?ref=${REF_W34}"
"p3a11|W34-gap-embodied|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/arxiv-embodied-security.json?ref=${REF_W34}"
"p3a12|W34-gap-lapf|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/arxiv-lapf.json?ref=${REF_W34}"
"p3a13|W34-gap-scienceflow|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/arxiv-scienceflow.json?ref=${REF_W34}"
"p3a14|W34-gap-aws|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/aws-vector-solutions.json?ref=${REF_W34}"
"p3a15|W34-gap-deepseek-vision|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/deepseek-v4-flash-vision-exp.json?ref=${REF_W34}"
"p3a16|W34-gap-gemini37|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/google-gemini-3-7-flash.json?ref=${REF_W34}"
"p3a17|W34-gap-omni|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/google-omni-1-1-flash.json?ref=${REF_W34}"
"p3a18|W34-gap-transcribe|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/google-transcribe.json?ref=${REF_W34}"
"p3a19|W34-gap-minimax-h3|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/minimax-h3.json?ref=${REF_W34}"
"p3a20|W34-gap-minimax-music|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/minimax-music-3.json?ref=${REF_W34}"
"p3a21|W34-gap-mistral|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/mistral-agentic-search.json?ref=${REF_W34}"
"p3a22|W34-gap-nvidia-eco|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/nvidia-ai-ecosystem.json?ref=${REF_W34}"
"p3a23|W34-gap-openai-regional|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/openai-api-regional-processing.json?ref=${REF_W34}"
"p3a24|W34-gap-chatgpt-notes|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/openai-chatgpt-release-notes.json?ref=${REF_W34}"
"p3a25|W34-gap-qwen|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/qwen3-8-27b.json?ref=${REF_W34}"
"p3a26|W34-gap-runway|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/runway-changelog.json?ref=${REF_W34}"
"p3a27|W34-gap-sol-baseline|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/sol-baseline-locator-observations.json?ref=${REF_W34}"
"p3a28|W34-gap-stable-audio|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/stability-stable-audio.json?ref=${REF_W34}"
"p3a29|W34-gap-xai|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/xai-api-changelog.json?ref=${REF_W34}"
"p3a30|W34-gap-zai|repos/${REPO}/contents/sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/zai-glm-5-3.json?ref=${REF_W34}"
"p3a31|W34-arxiv-csai|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/arxiv/runs/20260907T161121Z/raw/cs-ai.atom?ref=${REF_W34}"
"p3a32|W34-arxiv-cscl|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/arxiv/runs/20260907T161121Z/raw/cs-cl.atom?ref=${REF_W34}"
"p3a33|W34-arxiv-cscr|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/arxiv/runs/20260907T161121Z/raw/cs-cr.atom?ref=${REF_W34}"
"p3a34|W34-arxiv-cscv|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/arxiv/runs/20260907T161121Z/raw/cs-cv.atom?ref=${REF_W34}"
"p3a35|W34-arxiv-csdc|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/arxiv/runs/20260907T161121Z/raw/cs-dc.atom?ref=${REF_W34}"
"p3a36|W34-arxiv-cslg|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/arxiv/runs/20260907T161121Z/raw/cs-lg.atom?ref=${REF_W34}"
"p3a37|W34-off-apple|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/official-pages/runs/20260907T161655Z/raw/apple-ml-research.html?ref=${REF_W34}"
"p3a38|W34-off-cohere|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/official-pages/runs/20260907T161655Z/raw/cohere-blog.html?ref=${REF_W34}"
"p3a39|W34-off-kimi|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/official-pages/runs/20260907T161655Z/raw/kimi-code-whats-new.html?ref=${REF_W34}"
"p3a40|W34-off-openai-rss|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/official-pages/runs/20260907T161655Z/raw/openai-news-rss.html?ref=${REF_W34}"
"p3a41|W34-obs-alibaba|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-discovery-gapfill-after-sol-review-r1/source-observations/alibaba-model-lifecycle-official-web.md?ref=${REF_W34}"
"p3a42|W34-obs-fallback|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-discovery-gapfill-after-sol-review-r1/source-observations/official-fallback-web-observations.md?ref=${REF_W34}"
"p3a43|W34-dailyx-0816|repos/${REPO}/contents/sources/2026-W34/external/x/dailyx/raw/2026-08-16_0700.md?ref=${REF_W34}"
"p3a44|W34-dailyx-0817|repos/${REPO}/contents/sources/2026-W34/external/x/dailyx/raw/2026-08-17_0700.md?ref=${REF_W34}"
"p3a45|W34-dailyx-0818|repos/${REPO}/contents/sources/2026-W34/external/x/dailyx/raw/2026-08-18_0700.md?ref=${REF_W34}"
"p3a46|W34-dailyx-0819|repos/${REPO}/contents/sources/2026-W34/external/x/dailyx/raw/2026-08-19_0700.md?ref=${REF_W34}"
"p3a47|W34-dailyx-0820|repos/${REPO}/contents/sources/2026-W34/external/x/dailyx/raw/2026-08-20_0700.md?ref=${REF_W34}"
"p3a48|W34-dailyx-0821|repos/${REPO}/contents/sources/2026-W34/external/x/dailyx/raw/2026-08-21_0700.md?ref=${REF_W34}"
"p3a49|W34-dailyx-0822|repos/${REPO}/contents/sources/2026-W34/external/x/dailyx/raw/2026-08-22_0700.md?ref=${REF_W34}"
"p3a50|W34-grok-correction|repos/${REPO}/contents/sources/2026-W34/external/x/weekly-x-2026-W34-r2/raw/correction-report.md?ref=${REF_W34}"
"p3a51|W34-grok-result|repos/${REPO}/contents/sources/2026-W34/external/x/weekly-x-2026-W34-r2/raw/grok-x-result.corrected.md?ref=${REF_W34}"
"p3a52|W34-grok-accounting|repos/${REPO}/contents/sources/2026-W34/external/x/weekly-x-2026-W34-r2/raw/search-accounting.corrected.md?ref=${REF_W34}"
"p3a53|W34-grok-ledger|repos/${REPO}/contents/sources/2026-W34/external/x/weekly-x-2026-W34-r2/raw/x-url-ledger.corrected.tsv?ref=${REF_W34}"
"p3a54|W34-workingset-inventory|repos/${REPO}/contents/sources/2026-W34/intake/working-set/sol-discovery-event-inventory-v0.2.md?ref=${REF_W34}"
"p3a55|W34-bib-audit|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-human-preview-r2-issue491-repair/bibliography-provenance-audit-r2.md?ref=${REF_W34}"
"p3a56|W34-official-prov|repos/${REPO}/contents/sources/2026-W34/execution/luna/w34-screening-evidence-after-sol-discovery-r2/evidence-bodies/official-provenance.jsonl?ref=${REF_W34}"
"p3a57|W34-sol-decision|repos/${REPO}/contents/sources/2026-W34/execution/decisions/sol-discovery-completeness-20260903-r1.md?ref=${REF_W34}"
"p3a58|W34-sty|repos/${REPO}/contents/surveys/weekly/2026-W34/jgaisurvey.sty?ref=${REF_W34}"
"p3a59|SP-x-reception-r3|repos/${REPO}/contents/sources/SP-efficient-llm-2026/external/x/efficient-llm-reception-pass-01/raw/x-reception-result-r3.md?ref=${REF_SP}"
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
echo "P3 Raw fetch done. Splitting/verifying."
python3 - "$INTAKE_DIR" <<'PY'
import os, sys, json, base64, hashlib, glob
d=sys.argv[1]
ids=sorted([os.path.basename(p).split('.')[0] for p in glob.glob(os.path.join(d,"p3a*.command.txt"))])
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
    dkeys=list(j.keys())[:8] if isinstance(j,dict) else type(j)
    print(gid,"dict",dkeys, "message:", str(j.get('message',''))[:200] if isinstance(j,dict) else "")
PY
echo "P3 split done."
