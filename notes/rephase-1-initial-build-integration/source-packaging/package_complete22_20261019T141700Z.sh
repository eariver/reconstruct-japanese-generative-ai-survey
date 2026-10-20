#!/usr/bin/env bash
# COMPLETE22 packaging — GEN + PROOF (bounded Worker, no independent review).
# Source frozen: /tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60
#   actual detached409/tree8ce +22paths 4M18A (inherited21 R11 pins + style 035645ca/6569B).
# This script is saved BEFORE execution. No source edits/tests/imports/network/
# production/candidate commit, no historical runners.
# GEN: independent DB + absolute temp index outside packet (notes/): read-tree HEAD,
#   add ONLY known22, diff cached --binary HEAD => full22patch (single direct clean409).
# PROOF: independent copy restores tracked4 HEAD bytes, removes known new18 after pin
#   verification, verifies clean409, applies saved full22 via --check then apply
#   (separate raw stdout/stderr/numeric exits), validates 22 SHA/bytes/modes+status.
# All git via --no-optional-locks with sanitized env; every invocation captured to
# unique files with numeric exit (no shell masked exits, no overwrites).
# No .git/index/toolchain written into notes/ packet.
# Usage: bash package_complete22_20261019T141700Z.sh (v3 fix: GEN_COPY/PROOF_COPY are parents; leaf appended at use sites)
# v1 141500Z faulty cp nesting + v2 141600Z faulty leaf-double preserved in attempt1/attempt2; this v3 saved BEFORE third execution.
# Exit 0 only if all fail-close checks pass; nonzero preserves partial logs for diagnosis.

# Do NOT use set -e (would mask which command failed). Use set -u for undefined vars.
set -u
export PYTHONDONTWRITEBYTECODE=1

WORKSPACE="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
CAND_SRC="/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60"
EXPECT_HEAD="409b292756dd1277b9dfae87679934c0d2ce251c"
EXPECT_TREE="8ce3699861505f32d1d60bdc185d4d4f635aedb2"
STATIC21="$WORKSPACE/notes/rephase-1-dm021-p3s/draft-history-r11/static21.json"
EXPECT_STATIC21_SHA="1c0e339ceb31ddb8d565580f4e0d0b2140085cc414bb766b46872fdc8a2ef1a5"
STYLE_PATH="templates/survey/jgaisurvey.sty"
STYLE_SHA="035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec"
STYLE_BYTES="6569"
STYLE_BEFORE_SHA="3b6d15627439b35a352d692c8c5f9c2ac25dd02968e75beb30a69b8c8f53e5cc"
STYLE_BEFORE_BYTES="6547"

PACKROOT="/tmp/opencode/jgas-style22-packaging-20261019T141700Z"
GEN_COPY="$PACKROOT/gen-copy"
PROOF_COPY="$PACKROOT/proof-copy"
GEN_INDEX="$PACKROOT/gen-index"
PACKET_DIR="$WORKSPACE/notes/rephase-1-initial-build-integration/source-packaging"
PATCH_OUT="$PACKET_DIR/complete22-409-clean.patch"
MANIFEST_OUT="$PACKET_DIR/complete22-manifest.json"

# Sanitize inherited Git env (fail informational, enforce per-command).
for v in GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_CEILING_DIRECTORIES GIT_COMMON_DIR GIT_PREFIX; do
  unset "$v" 2>/dev/null || true
done
export GIT_NO_LAZY_FETCH=1
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_OPTIONAL_LOCKS=0

# Known path sets (exact, sorted).
TRACKED4=(
  "schemas/reader-surface-gate-v2.schema.json"
  "schemas/reader-surface-semantic-review-v2.schema.json"
  "scripts/survey_reader_surface_gate_v2.py"
  "templates/survey/jgaisurvey.sty"
)
UNTRACKED18=(
  "schemas/editorial-correction-proposal-v2.schema.json"
  "schemas/editorial-retention-manifest-v2.schema.json"
  "schemas/editorial-staged-source-manifest-v2.schema.json"
  "schemas/longform-publication-source-manifest-v2.schema.json"
  "schemas/longform-reader-input-v2.schema.json"
  "scripts/survey_editorial_correction_proposal_v2.py"
  "scripts/survey_editorial_current_authority_v2.py"
  "scripts/survey_editorial_retention_v2.py"
  "scripts/survey_editorial_staged_source_v2.py"
  "scripts/survey_longform_derivation_v2.py"
  "scripts/survey_longform_generated_v2.py"
  "scripts/survey_longform_semantic_publication_v2.py"
  "tests/test_survey_editorial_correction_proposal_v2.py"
  "tests/test_survey_editorial_current_authority_v2.py"
  "tests/test_survey_editorial_retention_v2.py"
  "tests/test_survey_editorial_staged_source_v2.py"
  "tests/test_survey_longform_derivation_v2.py"
  "tests/test_survey_longform_publication_integration_v2.py"
)
KNOWN22=(
  "schemas/editorial-correction-proposal-v2.schema.json"
  "schemas/editorial-retention-manifest-v2.schema.json"
  "schemas/editorial-staged-source-manifest-v2.schema.json"
  "schemas/longform-publication-source-manifest-v2.schema.json"
  "schemas/longform-reader-input-v2.schema.json"
  "schemas/reader-surface-gate-v2.schema.json"
  "schemas/reader-surface-semantic-review-v2.schema.json"
  "scripts/survey_editorial_correction_proposal_v2.py"
  "scripts/survey_editorial_current_authority_v2.py"
  "scripts/survey_editorial_retention_v2.py"
  "scripts/survey_editorial_staged_source_v2.py"
  "scripts/survey_longform_derivation_v2.py"
  "scripts/survey_longform_generated_v2.py"
  "scripts/survey_longform_semantic_publication_v2.py"
  "scripts/survey_reader_surface_gate_v2.py"
  "templates/survey/jgaisurvey.sty"
  "tests/test_survey_editorial_correction_proposal_v2.py"
  "tests/test_survey_editorial_current_authority_v2.py"
  "tests/test_survey_editorial_retention_v2.py"
  "tests/test_survey_editorial_staged_source_v2.py"
  "tests/test_survey_longform_derivation_v2.py"
  "tests/test_survey_longform_publication_integration_v2.py"
)

FAILURES=0
log() { echo "$*"; }
fail() { echo "FAIL_CLOSE: $*"; FAILURES=$((FAILURES+1)); }

# run_cap <stdout_file> <stderr_file> <exit_file> -- <cmd...>
# Captures raw stdout/stderr/numeric exit to unique files; appends to commands.log.
run_cap() {
  out="$1"; err="$2"; exf="$3"; shift 3
  # consume --
  if [ "${1:-}" = "--" ]; then shift; fi
  # record command
  echo "CMD: $* CWD: $(pwd)" >> "$PACKET_DIR/commands.log"
  "$@" > "$out" 2> "$err"
  rc=$?
  printf "%s" "$rc" > "$exf"
  echo "EXIT: $rc CMD: $*" >> "$PACKET_DIR/commands.log"
  return $rc
}

echo "=== COMPLETE22 packaging start ==="
echo "workspace=$WORKSPACE"
echo "candidate=$CAND_SRC"
echo "packroot=$PACKROOT"
echo "packet=$PACKET_DIR"
ls -ld "$WORKSPACE" 2>&1 | head -n 2
: > "$PACKET_DIR/commands.log"
echo "commands.log initialized" >> "$PACKET_DIR/commands.log"

# 0. Preconditions: missing target / known static pins fail-close.
log "--- 0. preconditions ---"
if [ ! -d "$CAND_SRC" ]; then fail "CAND_SRC absent $CAND_SRC"; fi
if [ -L "$CAND_SRC" ]; then fail "CAND_SRC is symlink"; fi
if [ ! -f "$STATIC21" ]; then fail "STATIC21 absent $STATIC21"; fi
if [ -e "$PACKROOT" ]; then fail "PACKROOT already exists (must be new unique) $PACKROOT"; fi
if [ -e "$GEN_INDEX" ]; then fail "GEN_INDEX already exists $GEN_INDEX"; fi
# static21 hash-before-trust
if [ -f "$STATIC21" ]; then
  ssha=$(sha256sum "$STATIC21" | awk '{print $1}')
  echo "static21 sha=$ssha expected=$EXPECT_STATIC21_SHA" | tee "$PACKET_DIR/pre-static21-sha.txt"
  if [ "$ssha" != "$EXPECT_STATIC21_SHA" ]; then fail "STATIC21 hash mismatch"; fi
else
  echo "STATIC21 missing" > "$PACKET_DIR/pre-static21-sha.txt"
fi
# style-correction manifest exists (reference only; typo disclosed, not trusted for pins)
if [ ! -f "$WORKSPACE/notes/rephase-1-initial-build-integration/style-correction/final22-manifest.json" ]; then
  fail "style-correction final22-manifest absent"
fi
if [ "$FAILURES" -ne 0 ]; then echo "PRECONDITION FAILURES=$FAILURES"; exit 2; fi

# 1. Source before guards: HEAD/tree/detached/status/diff.
log "--- 1. source before identity ---"
run_cap "$PACKET_DIR/src-before-rev-parse-head-stdout.txt" "$PACKET_DIR/src-before-rev-parse-head-stderr.txt" "$PACKET_DIR/src-before-rev-parse-head-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" rev-parse HEAD || fail "src rev-parse HEAD failed"
run_cap "$PACKET_DIR/src-before-rev-parse-tree-stdout.txt" "$PACKET_DIR/src-before-rev-parse-tree-stderr.txt" "$PACKET_DIR/src-before-rev-parse-tree-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" rev-parse 'HEAD^{tree}' || fail "src rev-parse tree failed"
run_cap "$PACKET_DIR/src-before-symbolic-ref-stdout.txt" "$PACKET_DIR/src-before-symbolic-ref-stderr.txt" "$PACKET_DIR/src-before-symbolic-ref-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" symbolic-ref -q HEAD
symrc=$(cat "$PACKET_DIR/src-before-symbolic-ref-exit.txt")
if [ "$symrc" = "0" ]; then fail "src NOT detached (symbolic-ref succeeded)"; else echo "src detached OK (rc=$symrc)" | tee "$PACKET_DIR/src-before-detached.txt"; fi
headval=$(cat "$PACKET_DIR/src-before-rev-parse-head-stdout.txt" | tr -d '\n')
treeval=$(cat "$PACKET_DIR/src-before-rev-parse-tree-stdout.txt" | tr -d '\n')
if [ "$headval" != "$EXPECT_HEAD" ]; then fail "src HEAD mismatch $headval"; fi
if [ "$treeval" != "$EXPECT_TREE" ]; then fail "src TREE mismatch $treeval"; fi
run_cap "$PACKET_DIR/src-before-status-stdout.txt" "$PACKET_DIR/src-before-status-stderr.txt" "$PACKET_DIR/src-before-status-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" status --porcelain=v1 --untracked-files=all || fail "src status failed"
run_cap "$PACKET_DIR/src-before-diff-head-names-stdout.txt" "$PACKET_DIR/src-before-diff-head-names-stderr.txt" "$PACKET_DIR/src-before-diff-head-names-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" diff HEAD --name-only || fail "src diff HEAD failed"
run_cap "$PACKET_DIR/src-before-diff-cached-names-stdout.txt" "$PACKET_DIR/src-before-diff-cached-names-stderr.txt" "$PACKET_DIR/src-before-diff-cached-names-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" diff --cached --name-only || fail "src diff cached failed"
run_cap "$PACKET_DIR/src-before-ls-others-stdout.txt" "$PACKET_DIR/src-before-ls-others-stderr.txt" "$PACKET_DIR/src-before-ls-others-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" ls-files --others --exclude-standard || fail "src ls-others failed"
# exact status check: 4M + 18?? = 22 lines, exact sets
status_lines=$(cat "$PACKET_DIR/src-before-status-stdout.txt" | sort)
expected_status=$(printf " M schemas/reader-surface-gate-v2.schema.json\n M schemas/reader-surface-semantic-review-v2.schema.json\n M scripts/survey_reader_surface_gate_v2.py\n M templates/survey/jgaisurvey.sty\n?? schemas/editorial-correction-proposal-v2.schema.json\n?? schemas/editorial-retention-manifest-v2.schema.json\n?? schemas/editorial-staged-source-manifest-v2.schema.json\n?? schemas/longform-publication-source-manifest-v2.schema.json\n?? schemas/longform-reader-input-v2.schema.json\n?? scripts/survey_editorial_correction_proposal_v2.py\n?? scripts/survey_editorial_current_authority_v2.py\n?? scripts/survey_editorial_retention_v2.py\n?? scripts/survey_editorial_staged_source_v2.py\n?? scripts/survey_longform_derivation_v2.py\n?? scripts/survey_longform_generated_v2.py\n?? scripts/survey_longform_semantic_publication_v2.py\n?? tests/test_survey_editorial_correction_proposal_v2.py\n?? tests/test_survey_editorial_current_authority_v2.py\n?? tests/test_survey_editorial_retention_v2.py\n?? tests/test_survey_editorial_staged_source_v2.py\n?? tests/test_survey_longform_derivation_v2.py\n?? tests/test_survey_longform_publication_integration_v2.py\n")
actual_sorted=$(printf "%s" "$status_lines" | sort)
expected_sorted=$(printf "%s" "$expected_status" | sort)
if [ "$actual_sorted" != "$expected_sorted" ]; then
  fail "src status exact mismatch"
  echo "--- actual ---" > "$PACKET_DIR/src-before-status-mismatch.txt"
  echo "$actual_sorted" >> "$PACKET_DIR/src-before-status-mismatch.txt"
else
  echo "src status 4M18A22 exact OK" | tee "$PACKET_DIR/src-before-status-ok.txt"
fi
diffnames=$(cat "$PACKET_DIR/src-before-diff-head-names-stdout.txt" | sort)
expdiff=$(printf "schemas/reader-surface-gate-v2.schema.json\nschemas/reader-surface-semantic-review-v2.schema.json\nscripts/survey_reader_surface_gate_v2.py\ntemplates/survey/jgaisurvey.sty\n")
if [ "$diffnames" != "$(printf "%s" "$expdiff" | sort)" ]; then fail "src diff HEAD names mismatch"; else echo "src diff HEAD 4 OK" | tee "$PACKET_DIR/src-before-diff-ok.txt"; fi
cachednames=$(cat "$PACKET_DIR/src-before-diff-cached-names-stdout.txt")
if [ -n "$cachednames" ]; then fail "src diff cached not empty"; else echo "src diff cached empty OK" | tee "$PACKET_DIR/src-before-cached-ok.txt"; fi

# 1b. Verify expected22 pins: 21 vs static21 + style vs hardcoded. Fail-close on mismatch/missing.
log "--- 1b. pin verification (21 static + style) ---"
export CAND_SRC STATIC21 PACKET_DIR
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/src-before-pins-stdout.txt" "$PACKET_DIR/src-before-pins-stderr.txt" "$PACKET_DIR/src-before-pins-exit.txt" -- python3 -c "
import json, hashlib, stat
from pathlib import Path
import os
ws = Path('$WORKSPACE')
src = Path('$CAND_SRC')
static21 = Path('$STATIC21')
pins = json.loads(static21.read_text())
style_path = '$STYLE_PATH'
style_sha = '$STYLE_SHA'
style_bytes = int('$STYLE_BYTES')
fails = 0
# check 21
for rel in sorted(pins):
    exp = pins[rel]
    fp = src / rel
    if not fp.exists():
        print(f'MISSING {rel}')
        fails += 1
        continue
    data = fp.read_bytes()
    h = hashlib.sha256(data).hexdigest()
    ln = len(data)
    mode = oct(stat.S_IMODE(fp.stat().st_mode))
    ok = (h == exp.get('sha256') and ln == exp.get('bytes') and mode == exp.get('mode'))
    print(f\"{'OK' if ok else 'MISMATCH'} {rel} sha={h} bytes={ln} mode={mode} exp={exp.get('sha256')}/{exp.get('bytes')}/{exp.get('mode')}\")
    if not ok:
        fails += 1
# style
fp = src / style_path
if not fp.exists():
    print(f'MISSING {style_path}')
    fails += 1
else:
    data = fp.read_bytes()
    h = hashlib.sha256(data).hexdigest()
    ln = len(data)
    mode = oct(stat.S_IMODE(fp.stat().st_mode))
    ok = (h == style_sha and ln == style_bytes and mode == '0o664')
    print(f\"{'OK' if ok else 'MISMATCH'} {style_path} sha={h} bytes={ln} mode={mode} exp={style_sha}/{style_bytes}/0o664\")
    if not ok:
        fails += 1
    # before-sha sanity: HEAD version must equal before
    print(f'STYLE_AFTER pin check done fails={fails}')
print(f'PIN_SUMMARY fails={fails}')
exit(1 if fails else 0)
"
pinrc=$(cat "$PACKET_DIR/src-before-pins-exit.txt")
if [ "$pinrc" != "0" ]; then fail "src pin verification failed rc=$pinrc (see src-before-pins-stdout.txt)"; else echo "src pins 22 OK" | tee "$PACKET_DIR/src-before-pins-ok.txt"; fi
# HEAD blob check for tracked4 (missing historical blob diagnostics)
log "--- 1c. HEAD blob availability for tracked4 ---"
for f in "${TRACKED4[@]}"; do
  safe=$(echo "$f" | tr '/' '_')
  run_cap "$PACKET_DIR/src-before-show-$safe-stdout.bin" "$PACKET_DIR/src-before-show-$safe-stderr.txt" "$PACKET_DIR/src-before-show-$safe-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" show "HEAD:$f" || fail "src show HEAD:$f failed (missing blob?)"
  if [ "$(cat "$PACKET_DIR/src-before-show-$safe-exit.txt")" != "0" ]; then fail "src show HEAD:$f non-zero"; fi
done
# style HEAD must equal before pin
head_style_sha=$(sha256sum "$PACKET_DIR/src-before-show-templates_survey_jgaisurvey.sty-stdout.bin" | awk '{print $1}')
head_style_bytes=$(stat -c '%s' "$PACKET_DIR/src-before-show-templates_survey_jgaisurvey.sty-stdout.bin")
echo "head_style sha=$head_style_sha bytes=$head_style_bytes expected_before=$STYLE_BEFORE_SHA/$STYLE_BEFORE_BYTES" | tee "$PACKET_DIR/src-before-head-style-check.txt"
if [ "$head_style_sha" != "$STYLE_BEFORE_SHA" ] || [ "$head_style_bytes" != "$STYLE_BEFORE_BYTES" ]; then fail "style HEAD bytes mismatch (expected before)"; fi
if [ "$FAILURES" -ne 0 ]; then echo "SOURCE BEFORE FAILURES=$FAILURES"; exit 2; fi

# 2. Create packaging root + independent byte copies (no hardlinks).
log "--- 2. packaging root + copies ---"
if [ -e "$PACKROOT" ]; then fail "PACKROOT exists"; exit 2; fi
run_cap "$PACKET_DIR/mkdir-packroot-stdout.txt" "$PACKET_DIR/mkdir-packroot-stderr.txt" "$PACKET_DIR/mkdir-packroot-exit.txt" -- mkdir -p "$PACKROOT/gen-copy" || fail "mkdir gen-copy failed"
run_cap "$PACKET_DIR/mkdir-proof-stdout.txt" "$PACKET_DIR/mkdir-proof-stderr.txt" "$PACKET_DIR/mkdir-proof-exit.txt" -- mkdir -p "$PACKROOT/proof-copy" || fail "mkdir proof-copy failed"
# cp -a (no hardlinks); capture raw (v3: GEN_COPY/PROOF_COPY are parents, leaf appended => correct single leaf)
run_cap "$PACKET_DIR/cp-gen-stdout.txt" "$PACKET_DIR/cp-gen-stderr.txt" "$PACKET_DIR/cp-gen-exit.txt" -- cp -a "$CAND_SRC" "$GEN_COPY/candidate-partial-b40de60" || fail "cp gen failed"
run_cap "$PACKET_DIR/cp-proof-stdout.txt" "$PACKET_DIR/cp-proof-stderr.txt" "$PACKET_DIR/cp-proof-exit.txt" -- cp -a "$CAND_SRC" "$PROOF_COPY/candidate-partial-b40de60" || fail "cp proof failed"
if [ "$(cat "$PACKET_DIR/cp-gen-exit.txt")" != "0" ]; then fail "cp gen non-zero"; fi
if [ "$(cat "$PACKET_DIR/cp-proof-exit.txt")" != "0" ]; then fail "cp proof non-zero"; fi
# symlink check for copies
if [ -L "$GEN_COPY/candidate-partial-b40de60" ]; then fail "gen copy is symlink"; fi
if [ -L "$PROOF_COPY/candidate-partial-b40de60" ]; then fail "proof copy is symlink"; fi
if [ "$FAILURES" -ne 0 ]; then echo "COPY FAILURES=$FAILURES"; exit 2; fi

# 2b. Full .git separation (all entries, not pack-only) + inert/no-alternates.
log "--- 2b. separation ---"
export PACKROOT CAND_SRC GEN_COPY PROOF_COPY WORKSPACE
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/separation-stdout.txt" "$PACKET_DIR/separation-stderr.txt" "$PACKET_DIR/separation-exit.txt" -- python3 -c "
import os
from pathlib import Path
from collections import defaultdict
def collect(root):
    dot = Path(root) / '.git'
    out = {}
    for cur, dirs, files in os.walk(dot, followlinks=False):
        for f in files:
            q = Path(cur) / f
            try:
                if q.is_symlink() or not q.is_file():
                    continue
                st = q.stat()
                out[str(q.relative_to(Path(root)))] = f'{st.st_dev}:{st.st_ino}'
            except OSError as e:
                out[str(q.relative_to(Path(root)))] = f'ERR:{e}'
    return out
src = collect('$CAND_SRC')
gen = collect('$GEN_COPY/candidate-partial-b40de60')
prf = collect('$PROOF_COPY/candidate-partial-b40de60')
rec = collect('$WORKSPACE')
print(f'src .git files={len(src)} gen={len(gen)} proof={len(prf)} recon={len(rec)}')
holders = defaultdict(list)
for rel, di in src.items():
    if not di.startswith('ERR:'):
        holders[di].append(f'src:{rel}')
for rel, di in gen.items():
    if not di.startswith('ERR:'):
        holders[di].append(f'gen:{rel}')
for rel, di in prf.items():
    if not di.startswith('ERR:'):
        holders[di].append(f'proof:{rel}')
for rel, di in rec.items():
    if not di.startswith('ERR:'):
        holders[di].append(f'recon:{rel}')
shared = {di:h for di,h in holders.items() if len(h)>1}
cross = {}
for di,h in shared.items():
    domains = set(x.split(':')[0] for x in h)
    if len(domains)>1:
        cross[di]=h
print(f'collisions total={len(shared)} cross-domain={len(cross)} expected 0/0')
for di in sorted(list(cross))[:20]:
    print(f' shared {di} {cross[di][:4]}')
# worktree 22 hardlink check src vs gen vs proof
import pathlib
known = '''schemas/editorial-correction-proposal-v2.schema.json
schemas/editorial-retention-manifest-v2.schema.json
schemas/editorial-staged-source-manifest-v2.schema.json
schemas/longform-publication-source-manifest-v2.schema.json
schemas/longform-reader-input-v2.schema.json
schemas/reader-surface-gate-v2.schema.json
schemas/reader-surface-semantic-review-v2.schema.json
scripts/survey_editorial_correction_proposal_v2.py
scripts/survey_editorial_current_authority_v2.py
scripts/survey_editorial_retention_v2.py
scripts/survey_editorial_staged_source_v2.py
scripts/survey_longform_derivation_v2.py
scripts/survey_longform_generated_v2.py
scripts/survey_longform_semantic_publication_v2.py
scripts/survey_reader_surface_gate_v2.py
templates/survey/jgaisurvey.sty
tests/test_survey_editorial_correction_proposal_v2.py
tests/test_survey_editorial_current_authority_v2.py
tests/test_survey_editorial_retention_v2.py
tests/test_survey_editorial_staged_source_v2.py
tests/test_survey_longform_derivation_v2.py
tests/test_survey_longform_publication_integration_v2.py'''.splitlines()
wshare=[]
for rel in known:
    try:
        a = (Path('$CAND_SRC')/rel).stat()
        b = (Path('$GEN_COPY/candidate-partial-b40de60')/rel).stat()
        c = (Path('$PROOF_COPY/candidate-partial-b40de60')/rel).stat()
        if (a.st_dev,a.st_ino)==(b.st_dev,b.st_ino): wshare.append(f'src-gen:{rel}')
        if (a.st_dev,a.st_ino)==(c.st_dev,c.st_ino): wshare.append(f'src-proof:{rel}')
        if (b.st_dev,b.st_ino)==(c.st_dev,c.st_ino): wshare.append(f'gen-proof:{rel}')
    except OSError as e:
        print(f'STAT_FAIL {rel} {e}')
print(f'worktree hardlink-shared count={len(wshare)} expected=0')
for w in wshare: print(f' shared {w}')
fails = 0
if cross: fails+=1
if wshare: fails+=1
print(f'SEPARATION fails={fails}')
exit(1 if fails else 0)
"
if [ "$(cat "$PACKET_DIR/separation-exit.txt")" != "0" ]; then fail "separation failed"; fi
# inert origin + no alternates for gen/proof (separate raw)
for tag in gen proof; do
  if [ "$tag" = "gen" ]; then COPY="$GEN_COPY/candidate-partial-b40de60"; else COPY="$PROOF_COPY/candidate-partial-b40de60"; fi
  safe="$tag"
  run_cap "$PACKET_DIR/$safe-remote-stdout.txt" "$PACKET_DIR/$safe-remote-stderr.txt" "$PACKET_DIR/$safe-remote-exit.txt" -- git --no-optional-locks -C "$COPY" remote -v || fail "$tag remote failed"
  if ! grep -q "example.invalid" "$PACKET_DIR/$safe-remote-stdout.txt"; then fail "$tag remote not inert"; fi
  run_cap "$PACKET_DIR/$safe-config-stdout.txt" "$PACKET_DIR/$safe-config-stderr.txt" "$PACKET_DIR/$safe-config-exit.txt" -- git --no-optional-locks -C "$COPY" config --show-origin --list || fail "$tag config failed"
  if [ -e "$COPY/.git/objects/info/alternates" ]; then fail "$tag alternates present"; else echo "$tag no-alternates OK" | tee "$PACKET_DIR/$safe-noalternates.txt"; fi
  run_cap "$PACKET_DIR/$safe-head-stdout.txt" "$PACKET_DIR/$safe-head-stderr.txt" "$PACKET_DIR/$safe-head-exit.txt" -- git --no-optional-locks -C "$COPY" rev-parse HEAD || fail "$tag rev-parse failed"
  hv=$(cat "$PACKET_DIR/$safe-head-stdout.txt" | tr -d '\n')
  if [ "$hv" != "$EXPECT_HEAD" ]; then fail "$tag HEAD mismatch $hv"; fi
done
if [ "$FAILURES" -ne 0 ]; then echo "SEPARATION FAILURES=$FAILURES"; exit 2; fi

# 3. GEN via independent DB + absolute temp index outside packet.
log "--- 3. GEN temp-index patch ---"
if [ -e "$GEN_INDEX" ]; then fail "GEN_INDEX exists"; exit 2; fi
if [ -e "$PATCH_OUT" ]; then fail "PATCH_OUT already exists (no overwrite)"; exit 2; fi
export GIT_INDEX_FILE="$GEN_INDEX"
# read-tree HEAD into temp index
run_cap "$PACKET_DIR/gen-read-tree-stdout.txt" "$PACKET_DIR/gen-read-tree-stderr.txt" "$PACKET_DIR/gen-read-tree-exit.txt" -- git --no-optional-locks --git-dir="$GEN_COPY/candidate-partial-b40de60/.git" --work-tree="$GEN_COPY/candidate-partial-b40de60" read-tree HEAD || fail "gen read-tree failed (missing blob?)"
if [ "$(cat "$PACKET_DIR/gen-read-tree-exit.txt")" != "0" ]; then fail "gen read-tree non-zero"; exit 2; fi
# add ONLY known22
run_cap "$PACKET_DIR/gen-add-stdout.txt" "$PACKET_DIR/gen-add-stderr.txt" "$PACKET_DIR/gen-add-exit.txt" -- git --no-optional-locks --git-dir="$GEN_COPY/candidate-partial-b40de60/.git" --work-tree="$GEN_COPY/candidate-partial-b40de60" add -- "${KNOWN22[@]}" || fail "gen add failed"
if [ "$(cat "$PACKET_DIR/gen-add-exit.txt")" != "0" ]; then fail "gen add non-zero"; exit 2; fi
# verify staged names are exactly known22 (sorted)
run_cap "$PACKET_DIR/gen-diff-cached-names-stdout.txt" "$PACKET_DIR/gen-diff-cached-names-stderr.txt" "$PACKET_DIR/gen-diff-cached-names-exit.txt" -- git --no-optional-locks --git-dir="$GEN_COPY/candidate-partial-b40de60/.git" --work-tree="$GEN_COPY/candidate-partial-b40de60" diff --cached --name-only || fail "gen diff names failed"
if [ "$(cat "$PACKET_DIR/gen-diff-cached-names-exit.txt")" != "0" ]; then fail "gen diff names non-zero"; exit 2; fi
gennames=$(cat "$PACKET_DIR/gen-diff-cached-names-stdout.txt" | sort)
expnames=$(printf "%s\n" "${KNOWN22[@]}" | sort)
if [ "$gennames" != "$expnames" ]; then
  fail "gen staged names mismatch"
  echo "--- gen ---" > "$PACKET_DIR/gen-names-mismatch.txt"
  echo "$gennames" >> "$PACKET_DIR/gen-names-mismatch.txt"
  echo "--- exp ---" >> "$PACKET_DIR/gen-names-mismatch.txt"
  echo "$expnames" >> "$PACKET_DIR/gen-names-mismatch.txt"
  exit 2
else
  echo "gen staged 22 exact OK" | tee "$PACKET_DIR/gen-names-ok.txt"
fi
# diff cached --binary HEAD => patch (stdout is patch, stderr separate, exit separate)
echo "CMD: git diff --cached --binary HEAD > PATCH" >> "$PACKET_DIR/commands.log"
git --no-optional-locks --git-dir="$GEN_COPY/candidate-partial-b40de60/.git" --work-tree="$GEN_COPY/candidate-partial-b40de60" diff --cached --binary HEAD > "$PATCH_OUT" 2> "$PACKET_DIR/gen-diff-stderr.txt"
genrc=$?
printf "%s" "$genrc" > "$PACKET_DIR/gen-diff-exit.txt"
echo "EXIT: $genrc CMD: git diff --cached --binary HEAD" >> "$PACKET_DIR/commands.log"
if [ "$genrc" != "0" ]; then fail "gen diff non-zero (missing historical blob?)"; exit 2; fi
if [ ! -s "$PATCH_OUT" ]; then fail "gen patch empty"; exit 2; fi
patch_bytes=$(stat -c '%s' "$PATCH_OUT")
patch_sha=$(sha256sum "$PATCH_OUT" | awk '{print $1}')
echo "patch bytes=$patch_bytes sha=$patch_sha" | tee "$PACKET_DIR/gen-patch-info.txt"
# ensure original/source index untouched: source diff cached still empty, status unchanged
# NOTE: unset temp index BEFORE touching source so source uses its own index.
unset GIT_INDEX_FILE
run_cap "$PACKET_DIR/src-mid-diff-cached-stdout.txt" "$PACKET_DIR/src-mid-diff-cached-stderr.txt" "$PACKET_DIR/src-mid-diff-cached-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" diff --cached --name-only || fail "src mid cached check failed"
if [ -n "$(cat "$PACKET_DIR/src-mid-diff-cached-stdout.txt")" ]; then fail "source index mutated"; fi
# ensure temp index is outside packet (absolute /tmp) and no index in packet
case "$GEN_INDEX" in
  "$PACKET_DIR"*) fail "GEN_INDEX inside packet" ;;
  *) echo "GEN_INDEX outside packet OK $GEN_INDEX" | tee "$PACKET_DIR/gen-index-outside-ok.txt" ;;
esac
if [ -e "$PACKET_DIR/index" ] || [ -e "$PACKET_DIR/gen-index" ]; then fail "index leaked into packet"; fi
if [ "$FAILURES" -ne 0 ]; then echo "GEN FAILURES=$FAILURES"; exit 2; fi

# 4. PROOF: clean409 restore in disposable copy, then single direct apply.
log "--- 4. PROOF clean restore ---"
# verify proof copy pins before mutation (same as source)
export CAND_SRC PROOF_COPY
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/proof-before-pins-stdout.txt" "$PACKET_DIR/proof-before-pins-stderr.txt" "$PACKET_DIR/proof-before-pins-exit.txt" -- python3 -c "
import json, hashlib, stat
from pathlib import Path
src = Path('$PROOF_COPY/candidate-partial-b40de60')
pins = json.loads(Path('$STATIC21').read_text())
fails=0
for rel in sorted(pins):
    exp=pins[rel]
    fp=src/rel
    if not fp.exists():
        print(f'MISSING {rel}'); fails+=1; continue
    d=fp.read_bytes(); h=hashlib.sha256(d).hexdigest()
    ok=(h==exp.get('sha256') and len(d)==exp.get('bytes') and oct(stat.S_IMODE(fp.stat().st_mode))==exp.get('mode'))
    print(f\"{'OK' if ok else 'MISMATCH'} {rel}\")
    if not ok: fails+=1
fp=src/'$STYLE_PATH'
d=fp.read_bytes(); h=hashlib.sha256(d).hexdigest()
ok=(h=='$STYLE_SHA' and len(d)==int('$STYLE_BYTES'))
print(f\"{'OK' if ok else 'MISMATCH'} $STYLE_PATH {h} {len(d)}\")
if not ok: fails+=1
print(f'PROOF_BEFORE fails={fails}')
exit(1 if fails else 0)
"
if [ "$(cat "$PACKET_DIR/proof-before-pins-exit.txt")" != "0" ]; then fail "proof before pins failed"; exit 2; fi
# restore tracked4 exact HEAD bytes (only those 4, no other mutation)
for f in "${TRACKED4[@]}"; do
  safe=$(echo "$f" | tr '/' '_')
  run_cap "$PACKET_DIR/proof-restore-$safe-stdout.txt" "$PACKET_DIR/proof-restore-$safe-stderr.txt" "$PACKET_DIR/proof-restore-$safe-exit.txt" -- git --no-optional-locks --git-dir="$PROOF_COPY/candidate-partial-b40de60/.git" --work-tree="$PROOF_COPY/candidate-partial-b40de60" show "HEAD:$f" || fail "proof show HEAD:$f failed"
  if [ "$(cat "$PACKET_DIR/proof-restore-$safe-exit.txt")" != "0" ]; then fail "proof show $f non-zero"; exit 2; fi
  # write stdout.bin to worktree file (stdout file is exact bytes)
  cp "$PACKET_DIR/proof-restore-$safe-stdout.txt" "$PROOF_COPY/candidate-partial-b40de60/$f"
  cprc=$?
  echo "$cprc" > "$PACKET_DIR/proof-restore-$safe-cp-exit.txt"
  if [ "$cprc" != "0" ]; then fail "proof restore cp $f failed"; exit 2; fi
done
# remove only known new18 after pin verification (pins already verified above)
for f in "${UNTRACKED18[@]}"; do
  # pin already OK; remove copy only
  rm -f "$PROOF_COPY/candidate-partial-b40de60/$f"
  rrc=$?
  echo "$rrc" > "$PACKET_DIR/proof-rm-$(echo "$f" | tr '/' '_')-exit.txt"
  if [ "$rrc" != "0" ]; then fail "proof rm $f failed"; exit 2; fi
done
# verify clean409: HEAD same, tree still 8ce? (worktree clean => status empty), absent18, diff empty
run_cap "$PACKET_DIR/proof-clean-head-stdout.txt" "$PACKET_DIR/proof-clean-head-stderr.txt" "$PACKET_DIR/proof-clean-head-exit.txt" -- git --no-optional-locks -C "$PROOF_COPY/candidate-partial-b40de60" rev-parse HEAD || fail "proof clean head failed"
if [ "$(cat "$PACKET_DIR/proof-clean-head-stdout.txt" | tr -d '\n')" != "$EXPECT_HEAD" ]; then fail "proof clean HEAD mismatch"; fi
run_cap "$PACKET_DIR/proof-clean-status-stdout.txt" "$PACKET_DIR/proof-clean-status-stderr.txt" "$PACKET_DIR/proof-clean-status-exit.txt" -- git --no-optional-locks -C "$PROOF_COPY/candidate-partial-b40de60" status --porcelain=v1 --untracked-files=all || fail "proof clean status failed"
if [ -s "$PACKET_DIR/proof-clean-status-stdout.txt" ]; then fail "proof clean status not empty (expected clean409)"; cat "$PACKET_DIR/proof-clean-status-stdout.txt" > "$PACKET_DIR/proof-clean-status-nonempty.txt"; exit 2; else echo "proof clean status empty OK" | tee "$PACKET_DIR/proof-clean-ok.txt"; fi
run_cap "$PACKET_DIR/proof-clean-diff-stdout.txt" "$PACKET_DIR/proof-clean-diff-stderr.txt" "$PACKET_DIR/proof-clean-diff-exit.txt" -- git --no-optional-locks -C "$PROOF_COPY/candidate-partial-b40de60" diff HEAD --name-only || fail "proof clean diff failed"
if [ -n "$(cat "$PACKET_DIR/proof-clean-diff-stdout.txt")" ]; then fail "proof clean diff not empty"; fi
# absent18 check
absent_fail=0
for f in "${UNTRACKED18[@]}"; do
  if [ -e "$PROOF_COPY/candidate-partial-b40de60/$f" ]; then echo "STILL_PRESENT $f" >> "$PACKET_DIR/proof-clean-absent-fail.txt"; absent_fail=1; fi
done
if [ "$absent_fail" != "0" ]; then fail "proof clean absent18 failed"; exit 2; else echo "proof clean absent18 OK (18 absent)" | tee "$PACKET_DIR/proof-clean-absent-ok.txt"; fi
# tracked4 HEAD bytes check (must equal HEAD show)
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/proof-clean-headbytes-stdout.txt" "$PACKET_DIR/proof-clean-headbytes-stderr.txt" "$PACKET_DIR/proof-clean-headbytes-exit.txt" -- python3 -c "
import hashlib
from pathlib import Path
base = Path('$PROOF_COPY/candidate-partial-b40de60')
expect = {
 'schemas/reader-surface-gate-v2.schema.json': ('264fdd6427d2ac4a24f602aa7ec063baf90fc98ecd16f42da563d3671fd7bc9a', 6300),
 'schemas/reader-surface-semantic-review-v2.schema.json': ('1594933fca838afc9315a6bd4b0c0b1f707808cc983b0941ae8c8e6709fe73e6', 3160),
 'scripts/survey_reader_surface_gate_v2.py': ('818b173544b7f048300ba610d7cf7942693f22938305600312f3f54ac6318f4f', 86029),
 'templates/survey/jgaisurvey.sty': ('$STYLE_BEFORE_SHA', int('$STYLE_BEFORE_BYTES')),
}
fails=0
for rel,(eh,eb) in expect.items():
    d=(base/rel).read_bytes(); h=hashlib.sha256(d).hexdigest()
    ok=(h==eh and len(d)==eb)
    print(f\"{'OK' if ok else 'MISMATCH'} {rel} {h} {len(d)} exp {eh}/{eb}\")
    if not ok: fails+=1
print(f'HEADBYTES fails={fails}')
exit(1 if fails else 0)
"
if [ "$(cat "$PACKET_DIR/proof-clean-headbytes-exit.txt")" != "0" ]; then fail "proof clean headbytes mismatch"; exit 2; fi
if [ "$FAILURES" -ne 0 ]; then echo "PROOF CLEAN FAILURES=$FAILURES"; exit 2; fi

log "--- 5. PROOF apply single direct clean409 ---"
# --check then apply, separate raw stdout/stderr/numeric exits
run_cap "$PACKET_DIR/proof-apply-check-stdout.txt" "$PACKET_DIR/proof-apply-check-stderr.txt" "$PACKET_DIR/proof-apply-check-exit.txt" -- git --no-optional-locks -C "$PROOF_COPY/candidate-partial-b40de60" apply --check --verbose "$PATCH_OUT" || fail "proof apply --check failed"
checkrc=$(cat "$PACKET_DIR/proof-apply-check-exit.txt")
if [ "$checkrc" != "0" ]; then fail "proof --check non-zero rc=$checkrc"; echo "CHECK_FAILED"; exit 2; else echo "proof --check rc=0 OK" | tee "$PACKET_DIR/proof-check-ok.txt"; fi
run_cap "$PACKET_DIR/proof-apply-stdout.txt" "$PACKET_DIR/proof-apply-stderr.txt" "$PACKET_DIR/proof-apply-exit.txt" -- git --no-optional-locks -C "$PROOF_COPY/candidate-partial-b40de60" apply --verbose "$PATCH_OUT" || fail "proof apply failed"
applyrc=$(cat "$PACKET_DIR/proof-apply-exit.txt")
if [ "$applyrc" != "0" ]; then fail "proof apply non-zero rc=$applyrc"; exit 2; else echo "proof apply rc=0 OK" | tee "$PACKET_DIR/proof-apply-ok.txt"; fi
if [ "$FAILURES" -ne 0 ]; then echo "PROOF APPLY FAILURES=$FAILURES"; exit 2; fi

log "--- 6. PROOF validate 22 ---"
run_cap "$PACKET_DIR/proof-after-status-stdout.txt" "$PACKET_DIR/proof-after-status-stderr.txt" "$PACKET_DIR/proof-after-status-exit.txt" -- git --no-optional-locks -C "$PROOF_COPY/candidate-partial-b40de60" status --porcelain=v1 --untracked-files=all || fail "proof after status failed"
run_cap "$PACKET_DIR/proof-after-diff-names-stdout.txt" "$PACKET_DIR/proof-after-diff-names-stderr.txt" "$PACKET_DIR/proof-after-diff-names-exit.txt" -- git --no-optional-locks -C "$PROOF_COPY/candidate-partial-b40de60" diff HEAD --name-only || fail "proof after diff failed"
run_cap "$PACKET_DIR/proof-after-head-stdout.txt" "$PACKET_DIR/proof-after-head-stderr.txt" "$PACKET_DIR/proof-after-head-exit.txt" -- git --no-optional-locks -C "$PROOF_COPY/candidate-partial-b40de60" rev-parse HEAD || fail "proof after head failed"
if [ "$(cat "$PACKET_DIR/proof-after-head-stdout.txt" | tr -d '\n')" != "$EXPECT_HEAD" ]; then fail "proof after HEAD changed (must stay 409, no commit)"; fi
# status must equal source before exact 4M18A22
if ! diff -q <(sort "$PACKET_DIR/src-before-status-stdout.txt") <(sort "$PACKET_DIR/proof-after-status-stdout.txt") > "$PACKET_DIR/proof-status-diff-stdout.txt" 2> "$PACKET_DIR/proof-status-diff-stderr.txt"; then
  echo "1" > "$PACKET_DIR/proof-status-diff-exit.txt"
  fail "proof after status differs from source before"
  cat "$PACKET_DIR/proof-status-diff-stdout.txt" >> "$PACKET_DIR/commands.log"
else
  echo "0" > "$PACKET_DIR/proof-status-diff-exit.txt"
  echo "proof after status matches source 4M18A22 OK" | tee "$PACKET_DIR/proof-status-ok.txt"
fi
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/proof-after-pins-stdout.txt" "$PACKET_DIR/proof-after-pins-stderr.txt" "$PACKET_DIR/proof-after-pins-exit.txt" -- python3 -c "
import json, hashlib, stat
from pathlib import Path
proof = Path('$PROOF_COPY/candidate-partial-b40de60')
pins = json.loads(Path('$STATIC21').read_text())
fails=0
for rel in sorted(pins):
    exp=pins[rel]
    fp=proof/rel
    if not fp.exists():
        print(f'MISSING {rel}'); fails+=1; continue
    d=fp.read_bytes(); h=hashlib.sha256(d).hexdigest()
    ok=(h==exp.get('sha256') and len(d)==exp.get('bytes') and oct(stat.S_IMODE(fp.stat().st_mode))==exp.get('mode'))
    print(f\"{'OK' if ok else 'MISMATCH'} {rel} {h} {len(d)}\")
    if not ok: fails+=1
fp=proof/'$STYLE_PATH'
d=fp.read_bytes(); h=hashlib.sha256(d).hexdigest()
ok=(h=='$STYLE_SHA' and len(d)==int('$STYLE_BYTES') and oct(stat.S_IMODE(fp.stat().st_mode))=='0o664')
print(f\"{'OK' if ok else 'MISMATCH'} $STYLE_PATH {h} {len(d)}\")
if not ok: fails+=1
print(f'PROOF_AFTER fails={fails}')
exit(1 if fails else 0)
"
if [ "$(cat "$PACKET_DIR/proof-after-pins-exit.txt")" != "0" ]; then fail "proof after pins failed"; exit 2; fi
if [ "$FAILURES" -ne 0 ]; then echo "PROOF VALIDATE FAILURES=$FAILURES"; exit 2; fi

# 7. Source after guards: unchanged.
log "--- 7. source after unchanged ---"
run_cap "$PACKET_DIR/src-after-head-stdout.txt" "$PACKET_DIR/src-after-head-stderr.txt" "$PACKET_DIR/src-after-head-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" rev-parse HEAD || fail "src after head failed"
run_cap "$PACKET_DIR/src-after-status-stdout.txt" "$PACKET_DIR/src-after-status-stderr.txt" "$PACKET_DIR/src-after-status-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" status --porcelain=v1 --untracked-files=all || fail "src after status failed"
if ! diff -q <(sort "$PACKET_DIR/src-before-status-stdout.txt") <(sort "$PACKET_DIR/src-after-status-stdout.txt") > "$PACKET_DIR/src-after-status-diff-stdout.txt" 2> "$PACKET_DIR/src-after-status-diff-stderr.txt"; then
  echo "1" > "$PACKET_DIR/src-after-status-diff-exit.txt"
  fail "source changed during packaging"
  exit 2
else
  echo "0" > "$PACKET_DIR/src-after-status-diff-exit.txt"
  echo "source before/after identical OK" | tee "$PACKET_DIR/src-after-ok.txt"
fi
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/src-after-pins-stdout.txt" "$PACKET_DIR/src-after-pins-stderr.txt" "$PACKET_DIR/src-after-pins-exit.txt" -- python3 -c "
import json, hashlib, stat
from pathlib import Path
src = Path('$CAND_SRC')
pins = json.loads(Path('$STATIC21').read_text())
fails=0
for rel in sorted(pins):
    exp=pins[rel]
    d=(src/rel).read_bytes(); h=hashlib.sha256(d).hexdigest()
    if not (h==exp.get('sha256') and len(d)==exp.get('bytes')):
        print(f'MISMATCH {rel}'); fails+=1
    else:
        print(f'OK {rel}')
d=(src/'$STYLE_PATH').read_bytes(); h=hashlib.sha256(d).hexdigest()
print(f\"{'OK' if h=='$STYLE_SHA' else 'MISMATCH'} $STYLE_PATH\")
if h!='$STYLE_SHA': fails+=1
print(f'SRC_AFTER fails={fails}')
exit(1 if fails else 0)
"
if [ "$(cat "$PACKET_DIR/src-after-pins-exit.txt")" != "0" ]; then fail "src after pins failed"; exit 2; fi

# 8. Manifest (patch SHA/bytes/path list + source identity). No Git DB in packet.
log "--- 8. manifest ---"
patch_sha2=$(sha256sum "$PATCH_OUT" | awk '{print $1}')
patch_bytes2=$(stat -c '%s' "$PATCH_OUT")
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/manifest-gen-stdout.txt" "$PACKET_DIR/manifest-gen-stderr.txt" "$PACKET_DIR/manifest-gen-exit.txt" -- python3 -c "
import json, hashlib, stat
from pathlib import Path
proof = Path('$PROOF_COPY/candidate-partial-b40de60')
pins = json.loads(Path('$STATIC21').read_text())
files = {}
for rel in sorted(pins):
    fp = proof/rel
    d = fp.read_bytes()
    files[rel] = {'sha256': hashlib.sha256(d).hexdigest(), 'bytes': len(d), 'mode': oct(stat.S_IMODE(fp.stat().st_mode)), 'git_status': 'M' if rel in ['schemas/reader-surface-gate-v2.schema.json','schemas/reader-surface-semantic-review-v2.schema.json','scripts/survey_reader_surface_gate_v2.py'] else '??'}
fp = proof/'$STYLE_PATH'
d = fp.read_bytes()
files['$STYLE_PATH'] = {'sha256': hashlib.sha256(d).hexdigest(), 'bytes': len(d), 'mode': oct(stat.S_IMODE(fp.stat().st_mode)), 'git_status': 'M', 'before_sha256': '$STYLE_BEFORE_SHA', 'before_bytes': int('$STYLE_BEFORE_BYTES')}
man = {
 'candidate': '$CAND_SRC',
 'head': '$EXPECT_HEAD',
 'head_tree': '$EXPECT_TREE',
 'status_summary': '4M18A22',
 'patch': {'path': 'complete22-409-clean.patch', 'sha256': '$patch_sha2', 'bytes': int('$patch_bytes2')},
 'static21_file_sha': '$EXPECT_STATIC21_SHA',
 'style_expected': {'sha256': '$STYLE_SHA', 'bytes': int('$STYLE_BYTES')},
 'files': files,
 'proof': {'copy': '$PROOF_COPY/candidate-partial-b40de60', 'gen_copy': '$GEN_COPY/candidate-partial-b40de60', 'gen_index': '$GEN_INDEX', 'check_exit': open('$PACKET_DIR/proof-apply-check-exit.txt').read().strip(), 'apply_exit': open('$PACKET_DIR/proof-apply-exit.txt').read().strip()},
 'notes': 'partialDB26309/runtime-unbundled retained; current check is packaging observation only, not global certification; no rerun of old tests'
}
Path('$MANIFEST_OUT').write_text(json.dumps(man, indent=1, sort_keys=True))
print(f\"manifest wrote {len(files)} files patch { '$patch_sha2' } { '$patch_bytes2' }B\")
"
if [ "$(cat "$PACKET_DIR/manifest-gen-exit.txt")" != "0" ]; then fail "manifest gen failed"; exit 2; fi
# verify no .git/index in packet
if [ -d "$PACKET_DIR/.git" ]; then fail ".git leaked into packet"; fi
if ls "$PACKET_DIR" | grep -q "^\.git"; then fail "hidden git in packet"; fi
# list packet
ls -1 "$PACKET_DIR" > "$PACKET_DIR/packet-list.txt"
echo "packet files:" | tee -a "$PACKET_DIR/packet-list.txt"

echo "=== COMPLETE22 packaging done FAILURES=$FAILURES ==="
if [ "$FAILURES" -ne 0 ]; then exit 2; else exit 0; fi
