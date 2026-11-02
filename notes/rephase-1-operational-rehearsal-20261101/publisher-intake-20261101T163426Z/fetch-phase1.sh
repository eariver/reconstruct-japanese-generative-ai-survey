#!/usr/bin/env bash
# Publisher intake phase1 — metadata + living-doc current observations + PR via gh
# 17 DID targets, version-aware, cutoff 2026-09-21T16:10:00Z
# No old scripts rerun. No code execution. No weights.
set -uo pipefail
INTAKE_DIR="notes/rephase-1-operational-rehearsal-20261101/publisher-intake-20261101T163426Z"
mkdir -p "$INTAKE_DIR"
UA="Mozilla/5.0 (compatible; SP-publisher-intake/20261101; bounded-research)"

fetch_http() {
  gid="$1"; label="$2"; url="$3"; outbase="$4"
  echo "=== $gid $label ==="
  echo "curl -L --max-redirs 5 --connect-timeout 20 --max-time 120 -A \"$UA\" -D \"$INTAKE_DIR/${gid}.headers.txt\" -o \"$INTAKE_DIR/${outbase}\" \"$url\"" > "$INTAKE_DIR/${gid}.command.txt"
  echo "$label" > "$INTAKE_DIR/${gid}.label.txt"
  echo "$url" > "$INTAKE_DIR/${gid}.url.txt"
  echo "UA: $UA" > "$INTAKE_DIR/${gid}.argv-extra.txt"
  start=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "start $start" > "$INTAKE_DIR/${gid}.time.txt"
  echo $$ > "$INTAKE_DIR/${gid}.pid.txt"
  # -v for redirect chain to stderr, -s silent, -L follow, -D headers, -o body
  curl -L --max-redirs 5 --connect-timeout 20 --max-time 120 -s -v -A "$UA" -D "$INTAKE_DIR/${gid}.headers.txt" -o "$INTAKE_DIR/${outbase}" "$url" 2> "$INTAKE_DIR/${gid}.stderr.txt"
  ec=$?
  echo -n "$ec" > "$INTAKE_DIR/${gid}.exit.txt"
  end=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "end $end" >> "$INTAKE_DIR/${gid}.time.txt"
  # effective URL + code + size + time via second w-only call? No second network. Use headers + body stats.
  # Record bytes + sha
  if [ -f "$INTAKE_DIR/${outbase}" ]; then
    bytes=$(wc -c < "$INTAKE_DIR/${outbase}" | tr -d ' ')
    sha=$(sha256sum "$INTAKE_DIR/${outbase}" | cut -d' ' -f1)
  else
    bytes="0-missing"
    sha="missing"
  fi
  echo "bytes $bytes sha256 $sha exit $ec" >> "$INTAKE_DIR/${gid}.time.txt"
  echo "$bytes" > "$INTAKE_DIR/${gid}.bytes.txt"
  echo "$sha" > "$INTAKE_DIR/${gid}.sha256.txt"
  echo "exit $ec bytes $bytes sha $sha for $gid"
}

fetch_gh() {
  gid="$1"; label="$2"; apipath="$3"; outbase="$4"
  echo "=== $gid $label ==="
  echo "gh api -i \"$apipath\"" > "$INTAKE_DIR/${gid}.command.txt"
  echo "$label" > "$INTAKE_DIR/${gid}.label.txt"
  echo "$apipath" > "$INTAKE_DIR/${gid}.url.txt"
  echo "gh host github.com (token redacted, not logged)" > "$INTAKE_DIR/${gid}.argv-extra.txt"
  start=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "start $start" > "$INTAKE_DIR/${gid}.time.txt"
  echo $$ > "$INTAKE_DIR/${gid}.pid.txt"
  gh api -i "$apipath" > "$INTAKE_DIR/${gid}.stdout.raw" 2> "$INTAKE_DIR/${gid}.stderr.txt"
  ec=$?
  echo -n "$ec" > "$INTAKE_DIR/${gid}.exit.txt"
  end=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "end $end" >> "$INTAKE_DIR/${gid}.time.txt"
  # split headers/body like P5
  python3 - "$INTAKE_DIR" "$gid" "$outbase" <<'PY'
import os, sys
d=sys.argv[1]; gid=sys.argv[2]; outbase=sys.argv[3]
raw=os.path.join(d,gid+".stdout.raw")
hdr=os.path.join(d,gid+".headers.txt")
body=os.path.join(d,outbase)
data=open(raw,'rb').read()
idx=data.find(b"\r\n\r\n")
sep=4
if idx<0:
  idx=data.find(b"\n\n"); sep=2
if idx>=0:
  open(hdr,'wb').write(data[:idx])
  open(body,'wb').write(data[idx+sep:])
else:
  open(hdr,'wb').write(b"")
  open(body,'wb').write(data)
import hashlib
b=open(body,'rb').read()
print(gid, "bytes", len(b), "sha256", hashlib.sha256(b).hexdigest())
open(os.path.join(d,gid+".bytes.txt"),'w').write(str(len(b)))
open(os.path.join(d,gid+".sha256.txt"),'w').write(hashlib.sha256(b).hexdigest())
PY
  echo "exit $ec for $gid"
}

# --- arXiv metadata: API + abs (version history) ---
fetch_http "sp01-api" "EAGLE 2401.15077 arXiv API metadata" "https://export.arxiv.org/api/query?id_list=2401.15077" "DATA.sp01-api.xml"
fetch_http "sp01-abs" "EAGLE 2401.15077 abs version history" "https://arxiv.org/abs/2401.15077" "DATA.sp01-abs.html"

fetch_http "sp02-api" "Snell 2408.03314 arXiv API metadata" "https://export.arxiv.org/api/query?id_list=2408.03314" "DATA.sp02-api.xml"
fetch_http "sp02-abs" "Snell 2408.03314 abs version history" "https://arxiv.org/abs/2408.03314" "DATA.sp02-abs.html"

fetch_http "sp03-api" "s1 2501.19393 arXiv API metadata" "https://export.arxiv.org/api/query?id_list=2501.19393" "DATA.sp03-api.xml"
fetch_http "sp03-abs" "s1 2501.19393 abs version history" "https://arxiv.org/abs/2501.19393" "DATA.sp03-abs.html"

fetch_http "sp04-api" "ThinkPrune 2504.01296 arXiv API metadata" "https://export.arxiv.org/api/query?id_list=2504.01296" "DATA.sp04-api.xml"
fetch_http "sp04-abs" "ThinkPrune 2504.01296 abs version history" "https://arxiv.org/abs/2504.01296" "DATA.sp04-abs.html"

fetch_http "sp05-api" "overthinking 2604.10739 arXiv API metadata" "https://export.arxiv.org/api/query?id_list=2604.10739" "DATA.sp05-api.xml"
fetch_http "sp05-abs" "overthinking 2604.10739 abs version history" "https://arxiv.org/abs/2604.10739" "DATA.sp05-abs.html"

fetch_http "sp06-api" "FrugalGPT 2305.05176 arXiv API metadata" "https://export.arxiv.org/api/query?id_list=2305.05176" "DATA.sp06-api.xml"
fetch_http "sp06-abs" "FrugalGPT 2305.05176 abs version history" "https://arxiv.org/abs/2305.05176" "DATA.sp06-abs.html"

fetch_http "sp07-api" "Kimi 2510.26692 arXiv API metadata" "https://export.arxiv.org/api/query?id_list=2510.26692" "DATA.sp07-api.xml"
fetch_http "sp07-abs" "Kimi 2510.26692 abs version history" "https://arxiv.org/abs/2510.26692" "DATA.sp07-abs.html"

fetch_http "sp08-api" "Qwen 2608.30320 arXiv API metadata" "https://export.arxiv.org/api/query?id_list=2608.30320" "DATA.sp08-api.xml"
fetch_http "sp08-abs" "Qwen 2608.30320 abs version history" "https://arxiv.org/abs/2608.30320" "DATA.sp08-abs.html"

fetch_http "sp09-api" "V4.1 2609.19969 arXiv API metadata" "https://export.arxiv.org/api/query?id_list=2609.19969" "DATA.sp09-api.xml"
fetch_http "sp09-abs" "V4.1 2609.19969 abs version history" "https://arxiv.org/abs/2609.19969" "DATA.sp09-abs.html"

fetch_http "sp10-api" "V3.2 2512.02556 arXiv API metadata" "https://export.arxiv.org/api/query?id_list=2512.02556" "DATA.sp10-api.xml"
fetch_http "sp10-abs" "V3.2 2512.02556 abs version history" "https://arxiv.org/abs/2512.02556" "DATA.sp10-abs.html"

# --- living docs (current observation) ---
fetch_http "sp11-body" "Jev launch page current observation" "https://typesafe.ai/blog/introducing-system-one-models-and-jev" "DATA.sp11-launch.html"
fetch_http "sp12-body" "Jev concepts page current observation" "https://docs.typesafe.ai/concepts/system-one" "DATA.sp12-concepts.html"
fetch_http "sp13-body" "Jev models page current observation" "https://docs.typesafe.ai/models" "DATA.sp13-models.html"
fetch_http "sp14-body" "vLLM DeepSeek-V4.1-Flash recipe current observation" "https://recipes.vllm.ai/deepseek-ai/DeepSeek-V4.1-Flash" "DATA.sp14-vllm-recipe.html"
fetch_http "sp16-api" "HF DeepSeek-V4.1-Flash model API metadata" "https://huggingface.co/api/models/deepseek-ai/DeepSeek-V4.1-Flash" "DATA.sp16-hf-api.json"
fetch_http "sp16-body" "HF DeepSeek-V4.1-Flash modelcard ONLY current observation" "https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash" "DATA.sp16-modelcard.html"
fetch_http "sp17-body" "Dynamo DeepSeek-V4.1-Flash recipe current observation" "https://docs.nvidia.com/dynamo/dev/recipes/deepseek-v4-1-flash.md" "DATA.sp17-dynamo.md"

# --- GitHub PR via gh only ---
fetch_gh "sp15-pr" "llama.cpp PR27742 metadata" "repos/ggml-org/llama.cpp/pulls/27742" "DATA.sp15-pr.json"
fetch_gh "sp15-commits" "llama.cpp PR27742 commits" "repos/ggml-org/llama.cpp/pulls/27742/commits" "DATA.sp15-commits.json"
fetch_gh "sp15-comments" "llama.cpp PR27742 issue comments" "repos/ggml-org/llama.cpp/issues/27742/comments" "DATA.sp15-comments.json"

echo "Phase1 done."
