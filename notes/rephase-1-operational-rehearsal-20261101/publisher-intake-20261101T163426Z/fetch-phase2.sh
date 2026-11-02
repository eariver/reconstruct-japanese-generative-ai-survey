#!/usr/bin/env bash
# Publisher intake phase2 — version-pinned arXiv PDF primary bodies
# Immutable vN available by 2026-09-21T16:10:00Z per phase1 API/abs verification
set -uo pipefail
INTAKE_DIR="notes/rephase-1-operational-rehearsal-20261101/publisher-intake-20261101T163426Z"
UA="Mozilla/5.0 (compatible; SP-publisher-intake/20261101; bounded-research)"
fetch_http() {
  gid="$1"; label="$2"; url="$3"; outbase="$4"
  echo "=== $gid $label ==="
  echo "curl -L --max-redirs 5 --connect-timeout 20 --max-time 180 -A \"$UA\" -D \"$INTAKE_DIR/${gid}.headers.txt\" -o \"$INTAKE_DIR/${outbase}\" \"$url\"" > "$INTAKE_DIR/${gid}.command.txt"
  echo "$label" > "$INTAKE_DIR/${gid}.label.txt"
  echo "$url" > "$INTAKE_DIR/${gid}.url.txt"
  echo "UA: $UA" > "$INTAKE_DIR/${gid}.argv-extra.txt"
  start=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "start $start" > "$INTAKE_DIR/${gid}.time.txt"
  echo $$ > "$INTAKE_DIR/${gid}.pid.txt"
  curl -L --max-redirs 5 --connect-timeout 20 --max-time 180 -s -v -A "$UA" -D "$INTAKE_DIR/${gid}.headers.txt" -o "$INTAKE_DIR/${outbase}" "$url" 2> "$INTAKE_DIR/${gid}.stderr.txt"
  ec=$?
  echo -n "$ec" > "$INTAKE_DIR/${gid}.exit.txt"
  end=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  echo "end $end" >> "$INTAKE_DIR/${gid}.time.txt"
  if [ -f "$INTAKE_DIR/${outbase}" ]; then
    bytes=$(wc -c < "$INTAKE_DIR/${outbase}" | tr -d ' ')
    sha=$(sha256sum "$INTAKE_DIR/${outbase}" | cut -d' ' -f1)
  else
    bytes="0-missing"; sha="missing"
  fi
  echo "bytes $bytes sha256 $sha exit $ec" >> "$INTAKE_DIR/${gid}.time.txt"
  echo "$bytes" > "$INTAKE_DIR/${gid}.bytes.txt"
  echo "$sha" > "$INTAKE_DIR/${gid}.sha256.txt"
  echo "exit $ec bytes $bytes sha $sha for $gid"
}
# vN chosen: latest immutable version with updated < cutoff 2026-09-21T16:10:00Z, verified phase1 API+abs
fetch_http "sp01-body" "EAGLE 2401.15077v3 PDF primary (updated 2025-03-04 < cutoff)" "https://arxiv.org/pdf/2401.15077v3" "DATA.sp01-eagle-v3.pdf"
fetch_http "sp02-body" "Snell 2408.03314v1 PDF primary (2024-08-06)" "https://arxiv.org/pdf/2408.03314v1" "DATA.sp02-snell-v1.pdf"
fetch_http "sp03-body" "s1 2501.19393v3 PDF primary (updated 2025-03-01 < cutoff)" "https://arxiv.org/pdf/2501.19393v3" "DATA.sp03-s1-v3.pdf"
fetch_http "sp04-body" "ThinkPrune 2504.01296v1 PDF primary (2025-04-02)" "https://arxiv.org/pdf/2504.01296v1" "DATA.sp04-thinkprune-v1.pdf"
fetch_http "sp05-body" "overthinking 2604.10739v1 PDF primary (2026-04-12 < cutoff; P5 claim 2026-08-24 flagged)" "https://arxiv.org/pdf/2604.10739v1" "DATA.sp05-overthinking-v1.pdf"
fetch_http "sp06-body" "FrugalGPT 2305.05176v1 PDF primary (2023-05-09)" "https://arxiv.org/pdf/2305.05176v1" "DATA.sp06-frugalgpt-v1.pdf"
fetch_http "sp07-body" "Kimi 2510.26692v2 PDF primary (updated 2025-11-01 < cutoff; latest before cutoff)" "https://arxiv.org/pdf/2510.26692v2" "DATA.sp07-kimi-v2.pdf"
fetch_http "sp08-body" "Qwen 2608.30320v1 PDF primary (2026-08-31)" "https://arxiv.org/pdf/2608.30320v1" "DATA.sp08-qwen-v1.pdf"
fetch_http "sp09-body" "V4.1 2609.19969v1 PDF primary (2026-09-17 < cutoff)" "https://arxiv.org/pdf/2609.19969v1" "DATA.sp09-v41-v1.pdf"
fetch_http "sp10-body" "V3.2 2512.02556v1 PDF primary (2025-12-02)" "https://arxiv.org/pdf/2512.02556v1" "DATA.sp10-v32-v1.pdf"
echo "Phase2 done."
