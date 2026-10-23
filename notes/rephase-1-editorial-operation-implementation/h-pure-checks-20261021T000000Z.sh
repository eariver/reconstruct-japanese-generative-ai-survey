#!/usr/bin/env bash
# H pure checks: syntax + schema JSON + closure counts + H-scope diff, no fixtures/builds.
# Inspect-only except py_compile with BYTECODE disabled (no pollution). No imports of source.
set -u
export PYTHONDONTWRITEBYTECODE=1
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_OPTIONAL_LOCKS=0
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_COMMON_DIR GIT_PREFIX || true

DST="/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60"
SRC="/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60"
echo "=== H pure checks (no fixtures, no builds) ==="
date -u; echo "exit_date=$?"
echo "dst=${DST}"
echo "--- H-owned py_compile (no bytecode) ---"
for f in scripts/survey_editorial_publication_v2.py scripts/survey_reader_publication_v2.py scripts/survey_reader_surface_gate_v2.py scripts/survey_weekly_derivation_v2.py scripts/survey_longform_generated_v2.py; do
  python3 -m py_compile "$DST/$f" && echo "OK $f" || echo "FAIL $f"
done
echo "exit_py=$?"
echo "--- H-owned schema JSON ---"
python3 -c "
import json,pathlib
repo=pathlib.Path('$DST')
files=['schemas/editorial-publication-source-manifest-v2.schema.json','schemas/editorial-publication-build-record-v2.schema.json','schemas/editorial-manuscript-spec-v2.schema.json','schemas/editorial-toolchain-spec-v2.schema.json','schemas/reader-manuscript-v2.schema.json','schemas/reader-surface-gate-v2.schema.json']
for s in files:
  json.load(open(repo/s)); print('OK',s)
"; echo "exit_schema=$?"
echo "--- closure counts (H-owned declarations) ---"
PYTHONDONTWRITEBYTECODE=1 python3 -c "
import ast,pathlib
repo=pathlib.Path('$DST')
def clen(fn):
  t=ast.parse((repo/fn).read_text())
  for n in ast.walk(t):
    if isinstance(n,ast.Assign) and any(getattr(x,'id','')=='CURRENT_CLOSURE' for x in n.targets):
      return len(n.value.elts)
print('weekly',clen('scripts/survey_weekly_derivation_v2.py'),'expected 22')
print('longform',clen('scripts/survey_longform_generated_v2.py'),'expected 27')
"; echo "exit_closure=$?"
echo "--- H-owned status/diff (disjoint, no L/C edits by H) ---"
git --no-optional-locks -C "$DST" status --porcelain=v1 --untracked-files=all | sort; echo "exit_status=$?"
echo "--- H-owned diff stat ---"
git --no-optional-locks -C "$DST" diff HEAD --stat -- scripts/survey_reader_publication_v2.py scripts/survey_reader_surface_gate_v2.py scripts/survey_weekly_derivation_v2.py schemas/reader-manuscript-v2.schema.json schemas/reader-surface-gate-v2.schema.json; echo "exit_diffstat=$?"
echo "--- H new files exist ---"
ls -l "$DST/scripts/survey_editorial_publication_v2.py" "$DST/schemas/editorial-publication-source-manifest-v2.schema.json" "$DST/schemas/editorial-publication-build-record-v2.schema.json" "$DST/schemas/editorial-manuscript-spec-v2.schema.json" "$DST/schemas/editorial-toolchain-spec-v2.schema.json"; echo "exit_new=$?"
echo "--- SRC untouched (original22) ---"
python3 -c "
import json,hashlib,os,pathlib,stat as st
m=json.load(open('notes/rephase-1-initial-build-integration/source-packaging/complete22-manifest.json'))
root=pathlib.Path('$SRC'); ok=0
for rel,exp in sorted(m['files'].items()):
  p=root/rel; d=p.read_bytes(); h=hashlib.sha256(d).hexdigest(); mode=oct(st.S_IMODE(os.stat(p).st_mode))
  if h==exp['sha256'] and len(d)==exp['bytes'] and mode==exp['mode']: ok+=1
print(f'src_pin OK={ok} TOTAL={len(m[\"files\"])}')
"; echo "exit_src=$?"
echo "=== DONE ==="
