#!/usr/bin/env bash
# Fixed-ref limited intake — W34 @774 + SP-efficient-llm @c8
# Read-only gh API GETs only. No git config/auth changes, no push/Issue/Actions.
# No execution of acquired Python. Local python use is for base64/hash verify only.
set -uo pipefail
INTAKE_DIR="notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z"
REPO="eariver/japanese-generative-ai-survey"
REF_W34="774dd39a951c9ac3818e83dfffd4c7666efb0a20"
REF_SP="c8d0ecc1c9566a2303ad3b4c42635d4b672650e4"
mkdir -p "$INTAKE_DIR"
# Fixed GET list: ID|label|api-path (no token in logs)
# W34 publication metadata (small JSON, needed for expected PDF SHA without PDF fetch)
# SP profile/state + directory listings (allowed roots only)
declare -a SPECS=(
"get01|W34-publication-candidate|repos/${REPO}/contents/sources/2026-W34/publication/v2/publication-candidate-v2.json?ref=${REF_W34}"
"get02|W34-release-record|repos/${REPO}/contents/sources/2026-W34/publication/v2/release-record-v2.json?ref=${REF_W34}"
"get03|SP-listing-sources|repos/${REPO}/contents/sources/SP-efficient-llm-2026?ref=${REF_SP}"
"get04|SP-production-profile|repos/${REPO}/contents/sources/SP-efficient-llm-2026/production-profile.json?ref=${REF_SP}"
"get05|SP-production-state|repos/${REPO}/contents/sources/SP-efficient-llm-2026/production-state.json?ref=${REF_SP}"
"get06|SP-listing-surveys|repos/${REPO}/contents/surveys/special/efficient-llm-2026?ref=${REF_SP}"
)
for spec in "${SPECS[@]}"; do
  IFS='|' read -r gid label apipath <<< "$spec"
  echo "=== $gid $label ==="
  echo "gh api -i \"$apipath\"" > "$INTAKE_DIR/${gid}.command.txt"
  echo "$label" > "$INTAKE_DIR/${gid}.label.txt"
  echo "$apipath" > "$INTAKE_DIR/${gid}.url.txt"
  # ref recorded separately (no token)
  if [[ "$apipath" == *"$REF_W34"* ]]; then echo "$REF_W34" > "$INTAKE_DIR/${gid}.ref.txt"; else echo "$REF_SP" > "$INTAKE_DIR/${gid}.ref.txt"; fi
  date -u +%Y-%m-%dT%H:%M:%SZ > "$INTAKE_DIR/${gid}.time.txt"
  # Execute read-only GET; capture stdout (headers+body) and stderr, numeric exit
  gh api -i "$apipath" > "$INTAKE_DIR/${gid}.stdout.raw" 2> "$INTAKE_DIR/${gid}.stderr.txt"
  echo -n "$?" > "$INTAKE_DIR/${gid}.exit.txt"
  echo "exit $(cat "$INTAKE_DIR/${gid}.exit.txt") for $gid"
done
echo "All fixed GETs attempted. Splitting headers/body and verifying where applicable."
python3 - "$INTAKE_DIR" <<'PY'
import os, sys, json, base64, hashlib
d = sys.argv[1]
for i in range(1,7):
  gid = f"get{i:02d}"
  raw = os.path.join(d, gid+".stdout.raw")
  hdr = os.path.join(d, gid+".headers.txt")
  body = os.path.join(d, gid+".body.json")
  if not os.path.exists(raw):
    continue
  data = open(raw,'rb').read()
  # gh -i separates headers and body by blank line (CRLF or LF)
  # Find first double newline
  idx = data.find(b"\r\n\r\n")
  sep = 4
  if idx < 0:
    idx = data.find(b"\n\n")
    sep = 2
  if idx >= 0:
    open(hdr,'wb').write(data[:idx])
    open(body,'wb').write(data[idx+sep:])
  else:
    # No headers (e.g. failure); keep whole as body for inspection, empty headers
    open(hdr,'wb').write(b"")
    open(body,'wb').write(data)
  # Try to decode file bodies to DATA where content is base64 file
  try:
    j = json.loads(open(body,'rb').read().decode('utf-8', errors='replace'))
  except Exception as e:
    print(f"{gid}: body not JSON ({e})")
    continue
  if isinstance(j, dict) and 'content' in j and 'encoding' in j:
    enc = j.get('encoding')
    if enc == 'base64':
      b = base64.b64decode(j.get('content',''))
      # verify size
      rep_size = j.get('size')
      print(f"{gid}: decoded {len(b)} bytes, reported size {rep_size}, match={len(b)==rep_size}")
      # verify git blob sha
      rep_sha = j.get('sha','')
      calc = hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()
      print(f"{gid}: reported blob {rep_sha}, calc {calc}, match={rep_sha==calc}")
      # write DATA file named by original path basename
      name = os.path.basename(j.get('path','') or gid)
      if not name:
        name = gid
      out = os.path.join(d, f"DATA.{name}")
      open(out,'wb').write(b)
      print(f"{gid}: wrote {out} sha256 {hashlib.sha256(b).hexdigest()}")
    else:
      print(f"{gid}: dict without base64 (encoding={enc})")
  elif isinstance(j, list):
    print(f"{gid}: directory listing with {len(j)} entries")
    for e in j[:50]:
      print(f"  - {e.get('type')} {e.get('path')} size={e.get('size')} sha={e.get('sha')}")
  else:
    print(f"{gid}: JSON dict keys {list(j.keys())[:10]}")
PY
echo "Split/verify done."
