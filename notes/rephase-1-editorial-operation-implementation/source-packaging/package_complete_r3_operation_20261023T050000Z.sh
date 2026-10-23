#!/usr/bin/env bash
# COMPLETE-R3-OPERATION packaging — final Worker (not independent reviewer) — 2026-10-23
# Governing: d880 R3 editorial operation contract (immutable versioned set + explicit activation),
#   root implementation selection (astra-implementation-selection.md),
#   correction-r7 README + r7b-closeout-note.md + source-manifest-r7b.json (721 files, HEAD 721a04...).
# Final intended source snapshot (workspace-ignored, untouched, before authority):
#   .rephase-1-editorial-runtime/jgas-editorial-r7b-20261023T034500Z/candidate-partial-b40de60
#   HEAD 721a04d85532d7855f3e54cc411f5847c787726e, tree ac7cb0bd2e977b46e957450816eddd779799e144, 721 tracked files.
#   Snapshot untracked pycache observed ignore-preserve, not clean claim.
# Actual candidate DST (real detached409/tree8ce partialDB with code overlay + owned residue):
#   /tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60
#   HEAD 409b292756dd1277b9dfae87679934c0d2ce251c, tree 8ce3699861505f32d1d60bdc185d4d4f635aedb2.
# Root expects intended delta maybe 25M+32A=57; recompute EXACT vs actual409 here, don't take
#   60 raw status including cache/tmp as code (notes/ 9 files, tests/__pycache__/ 2 pyc, tmpvr07sdme/ many).
# Runtime files byte-equal R7b manifest; original22 protected (inherited22 subset of 57, all new R3 fields included).
# Task: CREATE COMPLETE final overlay patch applies DIRECT clean actual409 (includes inherited22 +
#   all new R3 fields; NO candidate commit/new fake ancestry), independently saved-patch check/apply proof.
# Method (new script saved BEFORE execution, dedicated editor, no old runners, no source edits, no net,
#   no ordinary commits, no clean/reset):
#   GEN external absolute TempIndex under ignored scratch (not notes): read-tree actual409 then add ONLY
#     exact intended changed/new files; git diff cached --binary HEAD => complete-r3-operation-409.patch;
#     capture mode/blob/paths. Never stage original DST index.
#   PROOF prepare clean409 by restoring ONLY known tracked changed files to actual HEAD bytes and
#     excluding ONLY new intended files in disposable proof copy; verify actual HEAD/clean/index/absent
#     new paths and original HEAD blobs (no fakeRoot); apply SAVED patch check and apply separately
#     numeric exit, capture warnings, final content/git modes equality exact all intended files + delta.
#     Don't normalize whitespace inherited warnings. Full physical mode differences from fixture Git
#     checkout 644 vs DST 664 separate from Git mode; don't fake all mode equal.
#     Compare actual code hashes to final SOURCE exact, not old stale R2 manifest.
# GEN/PROOF independent GitDB byte copies of candidate409 DB (cp -a .git only, no hardlinks/alternates/
#   object sharing vs original/reconstruct); populate WORKTREE only explicit 721 intended final files
#   (from SNAP via manifest list, copy2 preserves bytes/mode), exclude DST cache/tmp/evidence
#   (notes/, __pycache__/, tmpvr07sdme/). Before Git writes verify own GitDir != reconstruct and HEAD409 tree8ce.
# Process no-bytecode + source before/after guards; partialDB 26309 limits retained.
# Durable packet under notes/.../source-packaging/: patch + FULL valid JSON manifest (final 57 paths SHA/bytes/
#   Git mode/physical observed mode) + source before/after + GEN/PROOF raw + script + README.
# No embedded .git/index/venv/toolchain under notes, every GitDB outside packet.
# Prior archival compaction maps/raw loss qualifications retained; no continuous no-drift/generic rerunner cert.
# Only needed new source inputs old four parent + complete N patch, no network restore.
# Return patch SHA/bytes/N and proof exact scope/any diagnostic; final code immutable for independent review,
#   if mismatch stop don't change source. No HumanCommitPoint on own, root final synthesis later.

# Do NOT use set -e (would mask which command failed). Use set -u for undefined vars.
set -u
export PYTHONDONTWRITEBYTECODE=1

WORKSPACE="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
CAND_SRC="/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60"
SNAP_SRC="/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/jgas-editorial-r7b-20261023T034500Z/candidate-partial-b40de60"
EXPECT_HEAD="409b292756dd1277b9dfae87679934c0d2ce251c"
EXPECT_TREE="8ce3699861505f32d1d60bdc185d4d4f635aedb2"
SNAP_HEAD="721a04d85532d7855f3e54cc411f5847c787726e"
SNAP_TREE="ac7cb0bd2e977b46e957450816eddd779799e144"
SNAP_MANIFEST="$WORKSPACE/notes/rephase-1-editorial-operation-implementation/correction-r7/source-manifest-r7b.json"

PACKROOT="/home/eariver/git/reconstruct-japanese-generative-ai-survey/.rephase-1-editorial-runtime/final-source-packaging"
GEN_PARENT="$PACKROOT/gen-copy"
PROOF_PARENT="$PACKROOT/proof-copy"
GEN_COPY="$PACKROOT/gen-copy/candidate-partial-b40de60"
PROOF_COPY="$PACKROOT/proof-copy/candidate-partial-b40de60"
GEN_INDEX="$PACKROOT/gen-index"
PACKET_DIR="/home/eariver/git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-editorial-operation-implementation/source-packaging"
PATCH_OUT="$PACKET_DIR/complete-r3-operation-409.patch"
MANIFEST_OUT="$PACKET_DIR/complete-r3-operation-manifest.json"

# Sanitize inherited Git env (fail informational, enforce per-command).
for v in GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_CEILING_DIRECTORIES GIT_COMMON_DIR GIT_PREFIX; do
  unset "$v" 2>/dev/null || true
done
export GIT_NO_LAZY_FETCH=1
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_OPTIONAL_LOCKS=0

# Exact intended delta: 25 tracked modified (M) vs actual409.
TRACKED25=(
  ".github/workflows/build-special-pdf.yml"
  ".github/workflows/build-weekly-survey.yml"
  ".github/workflows/survey-production-v2-export-publication-preview.yml"
  "config/survey-production-v2.json"
  "schemas/publication-surface-revalidation.schema.json"
  "schemas/reader-manuscript-v2.schema.json"
  "schemas/reader-surface-gate-v2.schema.json"
  "schemas/reader-surface-semantic-review-v2.schema.json"
  "scripts/run_semantic_publication_v2_interactive.py"
  "scripts/run_semantic_publication_v2_interactive_base.py"
  "scripts/survey_agent_control_v2.py"
  "scripts/survey_handoff_v2.py"
  "scripts/survey_human_gate_v2.py"
  "scripts/survey_orchestrator_v2.py"
  "scripts/survey_production_v2.py"
  "scripts/survey_profiled_freeze_v2.py"
  "scripts/survey_reader_publication_v2.py"
  "scripts/survey_reader_surface_gate_v2.py"
  "scripts/survey_schema_v2.py"
  "scripts/survey_semantic_quality_v2.py"
  "scripts/survey_stage_validation_v2.py"
  "scripts/survey_weekly_derivation_v2.py"
  "scripts/survey_weekly_mechanical_refresh_v2.py"
  "templates/survey/jgaisurvey.sty"
  "tests/test_survey_dm004_release_validate_state_v2.py"
)

# Exact intended new: 32 untracked (A) = snap721 - DST HEAD 689 (10 schemas + 9 scripts + 13 tests).
UNTRACKED32=(
  "schemas/editorial-correction-proposal-v2.schema.json"
  "schemas/editorial-manuscript-spec-v2.schema.json"
  "schemas/editorial-publication-build-record-v2.schema.json"
  "schemas/editorial-publication-set-v2.schema.json"
  "schemas/editorial-publication-source-manifest-v2.schema.json"
  "schemas/editorial-retention-manifest-v2.schema.json"
  "schemas/editorial-staged-source-manifest-v2.schema.json"
  "schemas/editorial-toolchain-spec-v2.schema.json"
  "schemas/longform-publication-source-manifest-v2.schema.json"
  "schemas/longform-reader-input-v2.schema.json"
  "scripts/survey_editorial_correction_proposal_v2.py"
  "scripts/survey_editorial_current_authority_v2.py"
  "scripts/survey_editorial_publication_v2.py"
  "scripts/survey_editorial_retention_v2.py"
  "scripts/survey_editorial_staged_source_v2.py"
  "scripts/survey_longform_derivation_v2.py"
  "scripts/survey_longform_generated_v2.py"
  "scripts/survey_longform_semantic_publication_v2.py"
  "scripts/survey_publication_set_v2.py"
  "tests/test_group_c_editorial_consumers_v2.py"
  "tests/test_survey_editorial_activation_faults_r4c.py"
  "tests/test_survey_editorial_correction_proposal_v2.py"
  "tests/test_survey_editorial_current_authority_v2.py"
  "tests/test_survey_editorial_r5_gaps_v2.py"
  "tests/test_survey_editorial_r7_boundary_v2.py"
  "tests/test_survey_editorial_retention_v2.py"
  "tests/test_survey_editorial_staged_source_v2.py"
  "tests/test_survey_longform_derivation_v2.py"
  "tests/test_survey_longform_publication_integration_v2.py"
  "tests/test_survey_publication_r3_anchor_shape_v2.py"
  "tests/test_survey_publication_set_v2.py"
  "tests/test_survey_schema_cache_v2.py"
)

# Complete 57 sorted (LC_ALL=C byte order) for GEN add/diff verification.
KNOWN57=(
  ".github/workflows/build-special-pdf.yml"
  ".github/workflows/build-weekly-survey.yml"
  ".github/workflows/survey-production-v2-export-publication-preview.yml"
  "config/survey-production-v2.json"
  "schemas/editorial-correction-proposal-v2.schema.json"
  "schemas/editorial-manuscript-spec-v2.schema.json"
  "schemas/editorial-publication-build-record-v2.schema.json"
  "schemas/editorial-publication-set-v2.schema.json"
  "schemas/editorial-publication-source-manifest-v2.schema.json"
  "schemas/editorial-retention-manifest-v2.schema.json"
  "schemas/editorial-staged-source-manifest-v2.schema.json"
  "schemas/editorial-toolchain-spec-v2.schema.json"
  "schemas/longform-publication-source-manifest-v2.schema.json"
  "schemas/longform-reader-input-v2.schema.json"
  "schemas/publication-surface-revalidation.schema.json"
  "schemas/reader-manuscript-v2.schema.json"
  "schemas/reader-surface-gate-v2.schema.json"
  "schemas/reader-surface-semantic-review-v2.schema.json"
  "scripts/run_semantic_publication_v2_interactive.py"
  "scripts/run_semantic_publication_v2_interactive_base.py"
  "scripts/survey_agent_control_v2.py"
  "scripts/survey_editorial_correction_proposal_v2.py"
  "scripts/survey_editorial_current_authority_v2.py"
  "scripts/survey_editorial_publication_v2.py"
  "scripts/survey_editorial_retention_v2.py"
  "scripts/survey_editorial_staged_source_v2.py"
  "scripts/survey_handoff_v2.py"
  "scripts/survey_human_gate_v2.py"
  "scripts/survey_longform_derivation_v2.py"
  "scripts/survey_longform_generated_v2.py"
  "scripts/survey_longform_semantic_publication_v2.py"
  "scripts/survey_orchestrator_v2.py"
  "scripts/survey_production_v2.py"
  "scripts/survey_profiled_freeze_v2.py"
  "scripts/survey_publication_set_v2.py"
  "scripts/survey_reader_publication_v2.py"
  "scripts/survey_reader_surface_gate_v2.py"
  "scripts/survey_schema_v2.py"
  "scripts/survey_semantic_quality_v2.py"
  "scripts/survey_stage_validation_v2.py"
  "scripts/survey_weekly_derivation_v2.py"
  "scripts/survey_weekly_mechanical_refresh_v2.py"
  "templates/survey/jgaisurvey.sty"
  "tests/test_group_c_editorial_consumers_v2.py"
  "tests/test_survey_dm004_release_validate_state_v2.py"
  "tests/test_survey_editorial_activation_faults_r4c.py"
  "tests/test_survey_editorial_correction_proposal_v2.py"
  "tests/test_survey_editorial_current_authority_v2.py"
  "tests/test_survey_editorial_r5_gaps_v2.py"
  "tests/test_survey_editorial_r7_boundary_v2.py"
  "tests/test_survey_editorial_retention_v2.py"
  "tests/test_survey_editorial_staged_source_v2.py"
  "tests/test_survey_longform_derivation_v2.py"
  "tests/test_survey_longform_publication_integration_v2.py"
  "tests/test_survey_publication_r3_anchor_shape_v2.py"
  "tests/test_survey_publication_set_v2.py"
  "tests/test_survey_schema_cache_v2.py"
)

FAILURES=0
log() { echo "$*"; }
fail() { echo "FAIL_CLOSE: $*"; FAILURES=$((FAILURES+1)); }

# run_cap <stdout_file> <stderr_file> <exit_file> -- <cmd...>
run_cap() {
  out="$1"; err="$2"; exf="$3"; shift 3
  if [ "${1:-}" = "--" ]; then shift; fi
  echo "CMD: $* CWD: $(pwd)" >> "$PACKET_DIR/commands.log"
  "$@" > "$out" 2> "$err"
  rc=$?
  printf "%s" "$rc" > "$exf"
  echo "EXIT: $rc CMD: $*" >> "$PACKET_DIR/commands.log"
  return $rc
}

echo "=== COMPLETE-R3-OPERATION packaging start ==="
echo "workspace=$WORKSPACE"
echo "candidate DST=$CAND_SRC"
echo "snapshot R7b=$SNAP_SRC"
echo "packroot=$PACKROOT"
echo "packet=$PACKET_DIR"
ls -ld "$WORKSPACE" 2>&1 | head -n 2
: > "$PACKET_DIR/commands.log"
echo "commands.log initialized" >> "$PACKET_DIR/commands.log"

# 0. Preconditions: missing targets / already-exists fail-close.
log "--- 0. preconditions ---"
if [ ! -d "$CAND_SRC" ]; then fail "CAND_SRC absent $CAND_SRC"; fi
if [ -L "$CAND_SRC" ]; then fail "CAND_SRC is symlink"; fi
if [ ! -d "$SNAP_SRC" ]; then fail "SNAP_SRC absent $SNAP_SRC"; fi
if [ -L "$SNAP_SRC" ]; then fail "SNAP_SRC is symlink"; fi
if [ ! -f "$SNAP_MANIFEST" ]; then fail "SNAP_MANIFEST absent $SNAP_MANIFEST"; fi
if [ -e "$PACKROOT" ]; then fail "PACKROOT already exists (must be new unique) $PACKROOT"; fi
if [ -e "$GEN_INDEX" ]; then fail "GEN_INDEX already exists $GEN_INDEX"; fi
if [ -e "$PATCH_OUT" ]; then fail "PATCH_OUT already exists (no overwrite) $PATCH_OUT"; fi
if [ -e "$MANIFEST_OUT" ]; then fail "MANIFEST_OUT already exists (no overwrite) $MANIFEST_OUT"; fi
# arrays must be 25 / 32 / 57 with no duplicates.
if [ "${#TRACKED25[@]}" != "25" ]; then fail "TRACKED25 count ${#TRACKED25[@]} != 25"; fi
if [ "${#UNTRACKED32[@]}" != "32" ]; then fail "UNTRACKED32 count ${#UNTRACKED32[@]} != 32"; fi
if [ "${#KNOWN57[@]}" != "57" ]; then fail "KNOWN57 count ${#KNOWN57[@]} != 57"; fi
if [ "$FAILURES" -ne 0 ]; then echo "PRECONDITION FAILURES=$FAILURES"; exit 2; fi

# 1. Source before guards: DST HEAD/tree/detached/diff/status; SNAP HEAD/tree/status; R7b manifest valid.
log "--- 1a. DST before identity ---"
run_cap "$PACKET_DIR/src-before-rev-parse-head-stdout.txt" "$PACKET_DIR/src-before-rev-parse-head-stderr.txt" "$PACKET_DIR/src-before-rev-parse-head-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" rev-parse HEAD || fail "src rev-parse HEAD failed"
run_cap "$PACKET_DIR/src-before-rev-parse-tree-stdout.txt" "$PACKET_DIR/src-before-rev-parse-tree-stderr.txt" "$PACKET_DIR/src-before-rev-parse-tree-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" rev-parse 'HEAD^{tree}' || fail "src rev-parse tree failed"
run_cap "$PACKET_DIR/src-before-symbolic-ref-stdout.txt" "$PACKET_DIR/src-before-symbolic-ref-stderr.txt" "$PACKET_DIR/src-before-symbolic-ref-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" symbolic-ref -q HEAD
symrc=$(cat "$PACKET_DIR/src-before-symbolic-ref-exit.txt")
if [ "$symrc" = "0" ]; then fail "src NOT detached (symbolic-ref succeeded)"; else echo "src detached OK (rc=$symrc)" | tee "$PACKET_DIR/src-before-detached.txt"; fi
headval=$(cat "$PACKET_DIR/src-before-rev-parse-head-stdout.txt" | tr -d '\n')
treeval=$(cat "$PACKET_DIR/src-before-rev-parse-tree-stdout.txt" | tr -d '\n')
if [ "$headval" != "$EXPECT_HEAD" ]; then fail "src HEAD mismatch $headval"; fi
if [ "$treeval" != "$EXPECT_TREE" ]; then fail "src TREE mismatch $treeval"; fi
run_cap "$PACKET_DIR/src-before-diff-head-names-stdout.txt" "$PACKET_DIR/src-before-diff-head-names-stderr.txt" "$PACKET_DIR/src-before-diff-head-names-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" diff HEAD --name-only || fail "src diff HEAD failed"
run_cap "$PACKET_DIR/src-before-diff-cached-names-stdout.txt" "$PACKET_DIR/src-before-diff-cached-names-stderr.txt" "$PACKET_DIR/src-before-diff-cached-names-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" diff --cached --name-only || fail "src diff cached failed"
run_cap "$PACKET_DIR/src-before-status-porcelain-stdout.txt" "$PACKET_DIR/src-before-status-porcelain-stderr.txt" "$PACKET_DIR/src-before-status-porcelain-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" status --porcelain=v1 || fail "src status porcelain failed"
run_cap "$PACKET_DIR/src-before-status-all-stdout.txt" "$PACKET_DIR/src-before-status-all-stderr.txt" "$PACKET_DIR/src-before-status-all-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" status --porcelain=v1 --untracked-files=all || fail "src status all failed"
run_cap "$PACKET_DIR/src-before-ls-others-stdout.txt" "$PACKET_DIR/src-before-ls-others-stderr.txt" "$PACKET_DIR/src-before-ls-others-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" ls-files --others --exclude-standard || fail "src ls-others failed"
# exact 25M check (LC_ALL=C sorted).
diffnames=$(LC_ALL=C sort "$PACKET_DIR/src-before-diff-head-names-stdout.txt")
expdiff=$(printf "%s\n" "${TRACKED25[@]}" | LC_ALL=C sort)
if [ "$diffnames" != "$expdiff" ]; then
  fail "src diff HEAD 25 mismatch (recomputed EXACT, not 60 raw)"
  echo "--- actual 25 ---" > "$PACKET_DIR/src-before-diff-mismatch.txt"
  echo "$diffnames" >> "$PACKET_DIR/src-before-diff-mismatch.txt"
  echo "--- expected 25 ---" >> "$PACKET_DIR/src-before-diff-mismatch.txt"
  echo "$expdiff" >> "$PACKET_DIR/src-before-diff-mismatch.txt"
else
  echo "src diff HEAD exact 25M OK (not 60 raw)" | tee "$PACKET_DIR/src-before-diff-ok.txt"
fi
cachednames=$(cat "$PACKET_DIR/src-before-diff-cached-names-stdout.txt")
if [ -n "$cachednames" ]; then fail "src diff cached not empty"; else echo "src diff cached empty OK" | tee "$PACKET_DIR/src-before-cached-ok.txt"; fi
# residue must exist in raw status but must NOT be in intended 57 (notes/, pycache, tmp).
if ! grep -q "^?? notes/" "$PACKET_DIR/src-before-status-all-stdout.txt"; then fail "expected residue notes/ absent in raw status (EDQUOT layout changed?)"; fi
if ! grep -q "tests/__pycache__/" "$PACKET_DIR/src-before-status-all-stdout.txt"; then fail "expected residue pycache absent in raw status"; fi
if ! grep -q "^?? tmpvr07sdme/" "$PACKET_DIR/src-before-status-porcelain-stdout.txt"; then
  # porcelain without -all shows tmpvr07sdme/ as single dir entry.
  if ! grep -q "tmpvr07sdme" "$PACKET_DIR/src-before-status-porcelain-stdout.txt"; then fail "expected residue tmpvr07sdme absent"; fi
fi
echo "raw 60 includes cache/tmp/evidence; intended EXACT is 25M+32A=57 (residue excluded)" | tee "$PACKET_DIR/src-before-residue-note.txt"

log "--- 1b. SNAP before identity + R7b manifest valid ---"
run_cap "$PACKET_DIR/snap-rev-parse-head-stdout.txt" "$PACKET_DIR/snap-rev-parse-head-stderr.txt" "$PACKET_DIR/snap-rev-parse-head-exit.txt" -- git --no-optional-locks -C "$SNAP_SRC" rev-parse HEAD || fail "snap rev-parse HEAD failed"
run_cap "$PACKET_DIR/snap-rev-parse-tree-stdout.txt" "$PACKET_DIR/snap-rev-parse-tree-stderr.txt" "$PACKET_DIR/snap-rev-parse-tree-exit.txt" -- git --no-optional-locks -C "$SNAP_SRC" rev-parse 'HEAD^{tree}' || fail "snap rev-parse tree failed"
run_cap "$PACKET_DIR/snap-status-stdout.txt" "$PACKET_DIR/snap-status-stderr.txt" "$PACKET_DIR/snap-status-exit.txt" -- git --no-optional-locks -C "$SNAP_SRC" status --porcelain=v1 --untracked-files=all || fail "snap status failed"
snaphead=$(cat "$PACKET_DIR/snap-rev-parse-head-stdout.txt" | tr -d '\n')
snaptree=$(cat "$PACKET_DIR/snap-rev-parse-tree-stdout.txt" | tr -d '\n')
if [ "$snaphead" != "$SNAP_HEAD" ]; then fail "snap HEAD mismatch $snaphead"; fi
if [ "$snaptree" != "$SNAP_TREE" ]; then fail "snap TREE mismatch $snaptree"; fi
# Snapshot untracked pycache observed ignore-preserve, not clean claim.
# With --untracked-files=all, pycache dir expands to individual .pyc files; allow any files ONLY under scripts/__pycache__/.
snapstat_file="$PACKET_DIR/snap-status-stdout.txt"
if [ ! -s "$snapstat_file" ]; then
  fail "snap status empty (expected pycache residue)"
else
  # every non-empty line must start with "?? scripts/__pycache__/".
  if grep -v "^?? scripts/__pycache__/" "$snapstat_file" | grep -q .; then
    fail "snap status not only pycache (got non-pycache lines)"
    cat "$snapstat_file" > "$PACKET_DIR/snap-status-unexpected.txt"
  else
    echo "snap status only pycache OK (ignore-preserve, not clean claim; $(wc -l < "$snapstat_file") files)" | tee "$PACKET_DIR/snap-status-ok.txt"
  fi
fi
export SNAP_MANIFEST PACKET_DIR
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/snap-manifest-valid-stdout.txt" "$PACKET_DIR/snap-manifest-valid-stderr.txt" "$PACKET_DIR/snap-manifest-valid-exit.txt" -- python3 -c "
import json
from pathlib import Path
m = json.loads(Path('$SNAP_MANIFEST').read_text())
assert m['head'] == '$SNAP_HEAD', f\"manifest head {m['head']}\"
assert m['tree'] == '$SNAP_TREE', f\"manifest tree {m['tree']}\"
assert m['count'] == 721, f\"manifest count {m['count']}\"
assert len(m['files']) == 721, f\"files len {len(m['files'])}\"
print(f\"R7b manifest valid: head={m['head']} tree={m['tree']} count={m['count']}\")
" || fail "snap manifest valid failed"
if [ "$(cat "$PACKET_DIR/snap-manifest-valid-exit.txt")" != "0" ]; then fail "snap manifest valid non-zero"; fi

log "--- 1c. DST 57 byte-equal SNAP R7b (final SOURCE exact, not old stale R2) ---"
export CAND_SRC SNAP_SRC SNAP_MANIFEST PACKET_DIR
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/src-snap-57-equal-stdout.txt" "$PACKET_DIR/src-snap-57-equal-stderr.txt" "$PACKET_DIR/src-snap-57-equal-exit.txt" -- python3 -c "
import json, hashlib
from pathlib import Path
snap = Path('$SNAP_SRC')
dst = Path('$CAND_SRC')
manifest = json.loads(Path('$SNAP_MANIFEST').read_text())
snap_by_path = {f['path']: f for f in manifest['files']}
tracked = '''.github/workflows/build-special-pdf.yml
.github/workflows/build-weekly-survey.yml
.github/workflows/survey-production-v2-export-publication-preview.yml
config/survey-production-v2.json
schemas/editorial-correction-proposal-v2.schema.json
schemas/editorial-manuscript-spec-v2.schema.json
schemas/editorial-publication-build-record-v2.schema.json
schemas/editorial-publication-set-v2.schema.json
schemas/editorial-publication-source-manifest-v2.schema.json
schemas/editorial-retention-manifest-v2.schema.json
schemas/editorial-staged-source-manifest-v2.schema.json
schemas/editorial-toolchain-spec-v2.schema.json
schemas/longform-publication-source-manifest-v2.schema.json
schemas/longform-reader-input-v2.schema.json
schemas/publication-surface-revalidation.schema.json
schemas/reader-manuscript-v2.schema.json
schemas/reader-surface-gate-v2.schema.json
schemas/reader-surface-semantic-review-v2.schema.json
scripts/run_semantic_publication_v2_interactive.py
scripts/run_semantic_publication_v2_interactive_base.py
scripts/survey_agent_control_v2.py
scripts/survey_editorial_correction_proposal_v2.py
scripts/survey_editorial_current_authority_v2.py
scripts/survey_editorial_publication_v2.py
scripts/survey_editorial_retention_v2.py
scripts/survey_editorial_staged_source_v2.py
scripts/survey_handoff_v2.py
scripts/survey_human_gate_v2.py
scripts/survey_longform_derivation_v2.py
scripts/survey_longform_generated_v2.py
scripts/survey_longform_semantic_publication_v2.py
scripts/survey_orchestrator_v2.py
scripts/survey_production_v2.py
scripts/survey_profiled_freeze_v2.py
scripts/survey_publication_set_v2.py
scripts/survey_reader_publication_v2.py
scripts/survey_reader_surface_gate_v2.py
scripts/survey_schema_v2.py
scripts/survey_semantic_quality_v2.py
scripts/survey_stage_validation_v2.py
scripts/survey_weekly_derivation_v2.py
scripts/survey_weekly_mechanical_refresh_v2.py
templates/survey/jgaisurvey.sty
tests/test_group_c_editorial_consumers_v2.py
tests/test_survey_dm004_release_validate_state_v2.py
tests/test_survey_editorial_activation_faults_r4c.py
tests/test_survey_editorial_correction_proposal_v2.py
tests/test_survey_editorial_current_authority_v2.py
tests/test_survey_editorial_r5_gaps_v2.py
tests/test_survey_editorial_r7_boundary_v2.py
tests/test_survey_editorial_retention_v2.py
tests/test_survey_editorial_staged_source_v2.py
tests/test_survey_longform_derivation_v2.py
tests/test_survey_longform_publication_integration_v2.py
tests/test_survey_publication_r3_anchor_shape_v2.py
tests/test_survey_publication_set_v2.py
tests/test_survey_schema_cache_v2.py'''.splitlines()
assert len(tracked) == 57, len(tracked)
fails = 0
for rel in tracked:
  d = (dst/rel).read_bytes() if (dst/rel).exists() else None
  s = (snap/rel).read_bytes() if (snap/rel).exists() else None
  exp = snap_by_path.get(rel)
  if d is None or s is None or exp is None:
    print(f'MISSING {rel} dst={d is not None} snap={s is not None} manifest={exp is not None}')
    fails += 1
    continue
  dh = hashlib.sha256(d).hexdigest()
  sh = hashlib.sha256(s).hexdigest()
  if d != s or dh != sh or dh != exp['sha256'] or len(d) != exp['bytes']:
    print(f'MISMATCH {rel} dst={dh[:8]} snap={sh[:8]} manifest={exp[\"sha256\"][:8]}')
    fails += 1
  else:
    print(f'OK {rel} {dh[:8]} {len(d)}B')
print(f'57_EQUAL fails={fails}')
exit(1 if fails else 0)
" || fail "src-snap 57 equal failed"
if [ "$(cat "$PACKET_DIR/src-snap-57-equal-exit.txt")" != "0" ]; then fail "DST 57 not byte-equal SNAP R7b (stop, don't change source)"; exit 2; else echo "DST 57 byte-equal SNAP R7b OK (original22 protected inside 57)" | tee "$PACKET_DIR/src-snap-57-ok.txt"; fi

log "--- 1d. SNAP 721 vs manifest (runtime byte-equal) + HEAD blobs for 25 ---"
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/snap-721-pins-stdout.txt" "$PACKET_DIR/snap-721-pins-stderr.txt" "$PACKET_DIR/snap-721-pins-exit.txt" -- python3 -c "
import json, hashlib, stat
from pathlib import Path
snap = Path('$SNAP_SRC')
m = json.loads(Path('$SNAP_MANIFEST').read_text())
fails = 0
for f in m['files']:
  rel = f['path']
  fp = snap/rel
  if not fp.exists():
    print(f'MISSING {rel}')
    fails += 1
    continue
  d = fp.read_bytes()
  h = hashlib.sha256(d).hexdigest()
  if h != f['sha256'] or len(d) != f['bytes']:
    print(f\"MISMATCH {rel} got {h[:8]}/{len(d)} exp {f['sha256'][:8]}/{f['bytes']}\")
    fails += 1
print(f'SNAP721 fails={fails} total={len(m[\"files\"])}')
exit(1 if fails else 0)
" || fail "snap 721 pins failed"
if [ "$(cat "$PACKET_DIR/snap-721-pins-exit.txt")" != "0" ]; then fail "SNAP 721 not byte-equal manifest"; exit 2; fi
for f in "${TRACKED25[@]}"; do
  safe=$(echo "$f" | tr '/' '_')
  run_cap "$PACKET_DIR/src-before-show-$safe-stdout.bin" "$PACKET_DIR/src-before-show-$safe-stderr.txt" "$PACKET_DIR/src-before-show-$safe-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" show "HEAD:$f" || fail "src show HEAD:$f failed (missing historical blob, no fakeRoot)"
  if [ "$(cat "$PACKET_DIR/src-before-show-$safe-exit.txt")" != "0" ]; then fail "src show HEAD:$f non-zero"; exit 2; fi
done
echo "HEAD blobs for 25 present OK (no fakeRoot)" | tee "$PACKET_DIR/src-before-blobs-ok.txt"
if [ "$FAILURES" -ne 0 ]; then echo "SOURCE BEFORE FAILURES=$FAILURES"; exit 2; fi

# 2. Create PACKROOT + independent DB byte copies + populate worktree 721 only.
log "--- 2. packaging root + independent DB copies ---"
run_cap "$PACKET_DIR/mkdir-packroot-stdout.txt" "$PACKET_DIR/mkdir-packroot-stderr.txt" "$PACKET_DIR/mkdir-packroot-exit.txt" -- mkdir -p "$GEN_PARENT" || fail "mkdir gen-parent failed"
run_cap "$PACKET_DIR/mkdir-proof-stdout.txt" "$PACKET_DIR/mkdir-proof-stderr.txt" "$PACKET_DIR/mkdir-proof-exit.txt" -- mkdir -p "$PROOF_PARENT" || fail "mkdir proof-parent failed"
run_cap "$PACKET_DIR/mkdir-gen-leaf-stdout.txt" "$PACKET_DIR/mkdir-gen-leaf-stderr.txt" "$PACKET_DIR/mkdir-gen-leaf-exit.txt" -- mkdir -p "$GEN_COPY" || fail "mkdir gen leaf failed"
run_cap "$PACKET_DIR/mkdir-proof-leaf-stdout.txt" "$PACKET_DIR/mkdir-proof-leaf-stderr.txt" "$PACKET_DIR/mkdir-proof-leaf-exit.txt" -- mkdir -p "$PROOF_COPY" || fail "mkdir proof leaf failed"
# cp -a .git only (no hardlinks, no worktree residue, no sources/surveys bulk).
run_cap "$PACKET_DIR/cp-gen-git-stdout.txt" "$PACKET_DIR/cp-gen-git-stderr.txt" "$PACKET_DIR/cp-gen-git-exit.txt" -- cp -a "$CAND_SRC/.git" "$GEN_COPY/.git" || fail "cp gen .git failed"
run_cap "$PACKET_DIR/cp-proof-git-stdout.txt" "$PACKET_DIR/cp-proof-git-stderr.txt" "$PACKET_DIR/cp-proof-git-exit.txt" -- cp -a "$CAND_SRC/.git" "$PROOF_COPY/.git" || fail "cp proof .git failed"
if [ "$(cat "$PACKET_DIR/cp-gen-git-exit.txt")" != "0" ]; then fail "cp gen git non-zero"; exit 2; fi
if [ "$(cat "$PACKET_DIR/cp-proof-git-exit.txt")" != "0" ]; then fail "cp proof git non-zero"; exit 2; fi
if [ -L "$GEN_COPY/.git" ]; then fail "gen .git is symlink"; fi
if [ -L "$PROOF_COPY/.git" ]; then fail "proof .git is symlink"; fi
# populate WORKTREE only explicit 721 intended final files from SNAP (copy2 preserves bytes; mode preserved where possible).
export SNAP_SRC GEN_COPY PROOF_COPY SNAP_MANIFEST PACKET_DIR
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/populate-gen-stdout.txt" "$PACKET_DIR/populate-gen-stderr.txt" "$PACKET_DIR/populate-gen-exit.txt" -- python3 -c "
import json, shutil
from pathlib import Path
snap = Path('$SNAP_SRC')
gen = Path('$GEN_COPY')
m = json.loads(Path('$SNAP_MANIFEST').read_text())
fails = 0
for f in m['files']:
  rel = f['path']
  src = snap/rel
  dst = gen/rel
  try:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
  except Exception as e:
    print(f'COPY_FAIL {rel} {e}')
    fails += 1
print(f'POPULATE_GEN copied={len(m[\"files\"])} fails={fails}')
exit(1 if fails else 0)
" || fail "populate gen failed"
if [ "$(cat "$PACKET_DIR/populate-gen-exit.txt")" != "0" ]; then fail "populate gen non-zero"; exit 2; fi
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/populate-proof-stdout.txt" "$PACKET_DIR/populate-proof-stderr.txt" "$PACKET_DIR/populate-proof-exit.txt" -- python3 -c "
import json, shutil
from pathlib import Path
snap = Path('$SNAP_SRC')
proof = Path('$PROOF_COPY')
m = json.loads(Path('$SNAP_MANIFEST').read_text())
fails = 0
for f in m['files']:
  rel = f['path']
  src = snap/rel
  dst = proof/rel
  try:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
  except Exception as e:
    print(f'COPY_FAIL {rel} {e}')
    fails += 1
print(f'POPULATE_PROOF copied={len(m[\"files\"])} fails={fails}')
exit(1 if fails else 0)
" || fail "populate proof failed"
if [ "$(cat "$PACKET_DIR/populate-proof-exit.txt")" != "0" ]; then fail "populate proof non-zero"; exit 2; fi
# verify worktrees have exactly 721 files (excluding .git), no residue.
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/worktree-721-check-stdout.txt" "$PACKET_DIR/worktree-721-check-stderr.txt" "$PACKET_DIR/worktree-721-check-exit.txt" -- python3 -c "
import json
from pathlib import Path
m = json.loads(Path('$SNAP_MANIFEST').read_text())
expected = set(f['path'] for f in m['files'])
for tag, root in [('gen', Path('$GEN_COPY')), ('proof', Path('$PROOF_COPY'))]:
  actual = set()
  for p in root.rglob('*'):
    if '.git' in p.parts:
      continue
    if p.is_file():
      actual.add(str(p.relative_to(root)))
  if actual != expected:
    print(f'{tag} WORKTREE MISMATCH extra={len(actual-expected)} missing={len(expected-actual)}')
    for e in sorted(actual-expected)[:10]:
      print(f'  EXTRA {e}')
    for e in sorted(expected-actual)[:10]:
      print(f'  MISSING {e}')
    exit(1)
  else:
    print(f'{tag} WORKTREE exact 721 OK (no cache/tmp/evidence)')
" || fail "worktree 721 check failed"
if [ "$(cat "$PACKET_DIR/worktree-721-check-exit.txt")" != "0" ]; then fail "worktree not exact 721"; exit 2; fi
if [ "$FAILURES" -ne 0 ]; then echo "COPY FAILURES=$FAILURES"; exit 2; fi

log "--- 2b. separation + own GitDir + HEAD409 tree8ce BEFORE writes ---"
export PACKROOT CAND_SRC GEN_COPY PROOF_COPY WORKSPACE
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/separation-stdout.txt" "$PACKET_DIR/separation-stderr.txt" "$PACKET_DIR/separation-exit.txt" -- python3 -c "
import os
from pathlib import Path
from collections import defaultdict
def collect_git(dot):
  out = {}
  for cur, dirs, files in os.walk(dot, followlinks=False):
    for f in files:
      q = Path(cur) / f
      try:
        if q.is_symlink() or not q.is_file():
          continue
        st = q.stat()
        out[str(q.relative_to(Path(dot).parent))] = f'{st.st_dev}:{st.st_ino}'
      except OSError as e:
        out[str(q.relative_to(Path(dot).parent))] = f'ERR:{e}'
  return out
src = collect_git(Path('$CAND_SRC') / '.git')
gen = collect_git(Path('$GEN_COPY') / '.git')
prf = collect_git(Path('$PROOF_COPY') / '.git')
rec = collect_git(Path('$WORKSPACE') / '.git')
print(f'src .git files={len(src)} gen={len(gen)} proof={len(prf)} recon={len(rec)}')
holders = defaultdict(list)
for rel, di in src.items():
  if not di.startswith('ERR:'): holders[di].append(f'src:{rel}')
for rel, di in gen.items():
  if not di.startswith('ERR:'): holders[di].append(f'gen:{rel}')
for rel, di in prf.items():
  if not di.startswith('ERR:'): holders[di].append(f'proof:{rel}')
for rel, di in rec.items():
  if not di.startswith('ERR:'): holders[di].append(f'recon:{rel}')
shared = {di:h for di,h in holders.items() if len(h)>1}
cross = {}
for di,h in shared.items():
  domains = set(x.split(':')[0] for x in h)
  if len(domains)>1: cross[di]=h
print(f'collisions total={len(shared)} cross-domain={len(cross)} expected 0/0')
for di in sorted(list(cross))[:20]:
  print(f' shared {di} {cross[di][:4]}')
# worktree 57 hardlink check src vs gen vs proof.
known = '''.github/workflows/build-special-pdf.yml
.github/workflows/build-weekly-survey.yml
.github/workflows/survey-production-v2-export-publication-preview.yml
config/survey-production-v2.json
schemas/editorial-correction-proposal-v2.schema.json
schemas/editorial-manuscript-spec-v2.schema.json
schemas/editorial-publication-build-record-v2.schema.json
schemas/editorial-publication-set-v2.schema.json
schemas/editorial-publication-source-manifest-v2.schema.json
schemas/editorial-retention-manifest-v2.schema.json
schemas/editorial-staged-source-manifest-v2.schema.json
schemas/editorial-toolchain-spec-v2.schema.json
schemas/longform-publication-source-manifest-v2.schema.json
schemas/longform-reader-input-v2.schema.json
schemas/publication-surface-revalidation.schema.json
schemas/reader-manuscript-v2.schema.json
schemas/reader-surface-gate-v2.schema.json
schemas/reader-surface-semantic-review-v2.schema.json
scripts/run_semantic_publication_v2_interactive.py
scripts/run_semantic_publication_v2_interactive_base.py
scripts/survey_agent_control_v2.py
scripts/survey_editorial_correction_proposal_v2.py
scripts/survey_editorial_current_authority_v2.py
scripts/survey_editorial_publication_v2.py
scripts/survey_editorial_retention_v2.py
scripts/survey_editorial_staged_source_v2.py
scripts/survey_handoff_v2.py
scripts/survey_human_gate_v2.py
scripts/survey_longform_derivation_v2.py
scripts/survey_longform_generated_v2.py
scripts/survey_longform_semantic_publication_v2.py
scripts/survey_orchestrator_v2.py
scripts/survey_production_v2.py
scripts/survey_profiled_freeze_v2.py
scripts/survey_publication_set_v2.py
scripts/survey_reader_publication_v2.py
scripts/survey_reader_surface_gate_v2.py
scripts/survey_schema_v2.py
scripts/survey_semantic_quality_v2.py
scripts/survey_stage_validation_v2.py
scripts/survey_weekly_derivation_v2.py
scripts/survey_weekly_mechanical_refresh_v2.py
templates/survey/jgaisurvey.sty
tests/test_group_c_editorial_consumers_v2.py
tests/test_survey_dm004_release_validate_state_v2.py
tests/test_survey_editorial_activation_faults_r4c.py
tests/test_survey_editorial_correction_proposal_v2.py
tests/test_survey_editorial_current_authority_v2.py
tests/test_survey_editorial_r5_gaps_v2.py
tests/test_survey_editorial_r7_boundary_v2.py
tests/test_survey_editorial_retention_v2.py
tests/test_survey_editorial_staged_source_v2.py
tests/test_survey_longform_derivation_v2.py
tests/test_survey_longform_publication_integration_v2.py
tests/test_survey_publication_r3_anchor_shape_v2.py
tests/test_survey_publication_set_v2.py
tests/test_survey_schema_cache_v2.py'''.splitlines()
wshare=[]
for rel in known:
  try:
    a = (Path('$CAND_SRC')/rel).stat()
    b = (Path('$GEN_COPY')/rel).stat()
    c = (Path('$PROOF_COPY')/rel).stat()
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
" || fail "separation failed"
if [ "$(cat "$PACKET_DIR/separation-exit.txt")" != "0" ]; then fail "separation non-zero"; exit 2; fi
for tag in gen proof; do
  if [ "$tag" = "gen" ]; then COPY="$GEN_COPY"; else COPY="$PROOF_COPY"; fi
  run_cap "$PACKET_DIR/$tag-remote-stdout.txt" "$PACKET_DIR/$tag-remote-stderr.txt" "$PACKET_DIR/$tag-remote-exit.txt" -- git --no-optional-locks -C "$COPY" remote -v || fail "$tag remote failed"
  if ! grep -q "example.invalid" "$PACKET_DIR/$tag-remote-stdout.txt"; then fail "$tag remote not inert"; fi
  if [ -e "$COPY/.git/objects/info/alternates" ]; then fail "$tag alternates present"; else echo "$tag no-alternates OK" | tee "$PACKET_DIR/$tag-noalternates.txt"; fi
  run_cap "$PACKET_DIR/$tag-gitdir-stdout.txt" "$PACKET_DIR/$tag-gitdir-stderr.txt" "$PACKET_DIR/$tag-gitdir-exit.txt" -- git --no-optional-locks -C "$COPY" rev-parse --absolute-git-dir || fail "$tag gitdir failed"
  run_cap "$PACKET_DIR/$tag-toplevel-stdout.txt" "$PACKET_DIR/$tag-toplevel-stderr.txt" "$PACKET_DIR/$tag-toplevel-exit.txt" -- git --no-optional-locks -C "$COPY" rev-parse --show-toplevel || fail "$tag toplevel failed"
  gd=$(cat "$PACKET_DIR/$tag-gitdir-stdout.txt" | tr -d '\n')
  # own GitDir must NOT be reconstruct.
  if [ "$gd" = "/home/eariver/git/reconstruct-japanese-generative-ai-survey/.git" ]; then fail "$tag GitDir is reconstruct (must be own)"; fi
  run_cap "$PACKET_DIR/$tag-head-stdout.txt" "$PACKET_DIR/$tag-head-stderr.txt" "$PACKET_DIR/$tag-head-exit.txt" -- git --no-optional-locks -C "$COPY" rev-parse HEAD || fail "$tag head failed"
  hv=$(cat "$PACKET_DIR/$tag-head-stdout.txt" | tr -d '\n')
  if [ "$hv" != "$EXPECT_HEAD" ]; then fail "$tag HEAD mismatch $hv"; fi
  run_cap "$PACKET_DIR/$tag-tree-stdout.txt" "$PACKET_DIR/$tag-tree-stderr.txt" "$PACKET_DIR/$tag-tree-exit.txt" -- git --no-optional-locks -C "$COPY" rev-parse 'HEAD^{tree}' || fail "$tag tree failed"
  tv=$(cat "$PACKET_DIR/$tag-tree-stdout.txt" | tr -d '\n')
  if [ "$tv" != "$EXPECT_TREE" ]; then fail "$tag TREE mismatch $tv"; fi
done
echo "own GitDir != reconstruct + HEAD409 tree8ce verified BEFORE writes" | tee "$PACKET_DIR/prewrite-ok.txt"
if [ "$FAILURES" -ne 0 ]; then echo "SEPARATION FAILURES=$FAILURES"; exit 2; fi

# 3. GEN via independent DB + absolute temp index outside packet.
log "--- 3. GEN temp-index patch (57 only, never stage DST index) ---"
if [ -e "$GEN_INDEX" ]; then fail "GEN_INDEX exists"; exit 2; fi
export GIT_INDEX_FILE="$GEN_INDEX"
run_cap "$PACKET_DIR/gen-read-tree-stdout.txt" "$PACKET_DIR/gen-read-tree-stderr.txt" "$PACKET_DIR/gen-read-tree-exit.txt" -- git --no-optional-locks --git-dir="$GEN_COPY/.git" --work-tree="$GEN_COPY" read-tree HEAD || fail "gen read-tree failed (missing tree object?)"
if [ "$(cat "$PACKET_DIR/gen-read-tree-exit.txt")" != "0" ]; then fail "gen read-tree non-zero"; exit 2; fi
run_cap "$PACKET_DIR/gen-add-stdout.txt" "$PACKET_DIR/gen-add-stderr.txt" "$PACKET_DIR/gen-add-exit.txt" -- git --no-optional-locks --git-dir="$GEN_COPY/.git" --work-tree="$GEN_COPY" add -- "${KNOWN57[@]}" || fail "gen add 57 failed"
if [ "$(cat "$PACKET_DIR/gen-add-exit.txt")" != "0" ]; then fail "gen add non-zero"; exit 2; fi
run_cap "$PACKET_DIR/gen-diff-cached-names-stdout.txt" "$PACKET_DIR/gen-diff-cached-names-stderr.txt" "$PACKET_DIR/gen-diff-cached-names-exit.txt" -- git --no-optional-locks --git-dir="$GEN_COPY/.git" --work-tree="$GEN_COPY" diff --cached --name-only || fail "gen diff names failed"
if [ "$(cat "$PACKET_DIR/gen-diff-cached-names-exit.txt")" != "0" ]; then fail "gen diff names non-zero"; exit 2; fi
gennames=$(LC_ALL=C sort "$PACKET_DIR/gen-diff-cached-names-stdout.txt")
expnames=$(printf "%s\n" "${KNOWN57[@]}" | LC_ALL=C sort)
if [ "$gennames" != "$expnames" ]; then
  fail "gen staged 57 mismatch"
  echo "--- gen ---" > "$PACKET_DIR/gen-names-mismatch.txt"
  echo "$gennames" >> "$PACKET_DIR/gen-names-mismatch.txt"
  echo "--- exp 57 ---" >> "$PACKET_DIR/gen-names-mismatch.txt"
  echo "$expnames" >> "$PACKET_DIR/gen-names-mismatch.txt"
  exit 2
else
  echo "gen staged exact 57 OK" | tee "$PACKET_DIR/gen-names-ok.txt"
fi
# capture mode/blob/paths for 57 from temp index (mode blob paths, no whitespace normalization).
run_cap "$PACKET_DIR/gen-ls-files-s-stdout.txt" "$PACKET_DIR/gen-ls-files-s-stderr.txt" "$PACKET_DIR/gen-ls-files-s-exit.txt" -- git --no-optional-locks --git-dir="$GEN_COPY/.git" --work-tree="$GEN_COPY" ls-files -s -- "${KNOWN57[@]}" || fail "gen ls-files -s failed"
run_cap "$PACKET_DIR/gen-diff-cached-stat-stdout.txt" "$PACKET_DIR/gen-diff-cached-stat-stderr.txt" "$PACKET_DIR/gen-diff-cached-stat-exit.txt" -- git --no-optional-locks --git-dir="$GEN_COPY/.git" --work-tree="$GEN_COPY" diff --cached --stat -- "${KNOWN57[@]}" || fail "gen diff stat failed"
run_cap "$PACKET_DIR/gen-diff-cached-numstat-stdout.txt" "$PACKET_DIR/gen-diff-cached-numstat-stderr.txt" "$PACKET_DIR/gen-diff-cached-numstat-exit.txt" -- git --no-optional-locks --git-dir="$GEN_COPY/.git" --work-tree="$GEN_COPY" diff --cached --numstat -- "${KNOWN57[@]}" || fail "gen numstat failed"
# diff cached --binary HEAD => patch (stdout is patch, stderr separate with warnings, no whitespace fix).
echo "CMD: git diff --cached --binary HEAD > PATCH (no whitespace normalization)" >> "$PACKET_DIR/commands.log"
git --no-optional-locks --git-dir="$GEN_COPY/.git" --work-tree="$GEN_COPY" diff --cached --binary HEAD > "$PATCH_OUT" 2> "$PACKET_DIR/gen-diff-stderr.txt"
genrc=$?
printf "%s" "$genrc" > "$PACKET_DIR/gen-diff-exit.txt"
echo "EXIT: $genrc CMD: git diff --cached --binary HEAD" >> "$PACKET_DIR/commands.log"
if [ "$genrc" != "0" ]; then fail "gen diff non-zero (missing historical blob?)"; exit 2; fi
if [ ! -s "$PATCH_OUT" ]; then fail "gen patch empty"; exit 2; fi
patch_bytes=$(stat -c '%s' "$PATCH_OUT")
patch_sha=$(sha256sum "$PATCH_OUT" | awk '{print $1}')
echo "patch bytes=$patch_bytes sha=$patch_sha" | tee "$PACKET_DIR/gen-patch-info.txt"
# warnings preserved (inherited whitespace), not normalized — record stderr size, do not fail on warnings.
gen_warn_bytes=$(stat -c '%s' "$PACKET_DIR/gen-diff-stderr.txt")
echo "gen diff stderr (warnings preserved, no fix) bytes=$gen_warn_bytes" | tee "$PACKET_DIR/gen-warnings-note.txt"
cat "$PACKET_DIR/gen-diff-stderr.txt" >> "$PACKET_DIR/commands.log" || true
# ensure original/source index untouched: source diff cached still empty, DST status unchanged.
unset GIT_INDEX_FILE
run_cap "$PACKET_DIR/src-mid-diff-cached-stdout.txt" "$PACKET_DIR/src-mid-diff-cached-stderr.txt" "$PACKET_DIR/src-mid-diff-cached-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" diff --cached --name-only || fail "src mid cached check failed"
if [ -n "$(cat "$PACKET_DIR/src-mid-diff-cached-stdout.txt")" ]; then fail "source index mutated (never stage DST index violated)"; fi
case "$GEN_INDEX" in
  "$PACKET_DIR"*) fail "GEN_INDEX inside packet (must be ignored scratch)" ;;
  *) echo "GEN_INDEX outside packet OK $GEN_INDEX" | tee "$PACKET_DIR/gen-index-outside-ok.txt" ;;
esac
if [ -e "$PACKET_DIR/index" ] || [ -e "$PACKET_DIR/gen-index" ]; then fail "index leaked into packet"; fi
if [ "$FAILURES" -ne 0 ]; then echo "GEN FAILURES=$FAILURES"; exit 2; fi

# 4. PROOF: clean409 restore in disposable copy (scoped 689 + 32, sources/surveys outside scope).
log "--- 4. PROOF clean restore (ONLY 25 tracked to HEAD, ONLY 32 new removed) ---"
# verify proof copy before pins match SNAP final 721 (already populated final).
export PROOF_COPY SNAP_MANIFEST PACKET_DIR
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/proof-before-721-stdout.txt" "$PACKET_DIR/proof-before-721-stderr.txt" "$PACKET_DIR/proof-before-721-exit.txt" -- python3 -c "
import json, hashlib
from pathlib import Path
proof = Path('$PROOF_COPY')
m = json.loads(Path('$SNAP_MANIFEST').read_text())
fails = 0
for f in m['files']:
  rel = f['path']
  fp = proof/rel
  if not fp.exists():
    print(f'MISSING {rel}')
    fails += 1
    continue
  d = fp.read_bytes()
  if hashlib.sha256(d).hexdigest() != f['sha256'] or len(d) != f['bytes']:
    print(f'MISMATCH {rel}')
    fails += 1
print(f'PROOF_BEFORE_721 fails={fails} total={len(m[\"files\"])}')
exit(1 if fails else 0)
" || fail "proof before 721 failed"
if [ "$(cat "$PACKET_DIR/proof-before-721-exit.txt")" != "0" ]; then fail "proof before not exact 721 final"; exit 2; fi
# restore ONLY 25 tracked exact HEAD bytes (no other mutation). Use git show stdout.bin then cp.
for f in "${TRACKED25[@]}"; do
  safe=$(echo "$f" | tr '/' '_')
  run_cap "$PACKET_DIR/proof-restore-$safe-stdout.bin" "$PACKET_DIR/proof-restore-$safe-stderr.txt" "$PACKET_DIR/proof-restore-$safe-exit.txt" -- git --no-optional-locks --git-dir="$PROOF_COPY/.git" --work-tree="$PROOF_COPY" show "HEAD:$f" || fail "proof show HEAD:$f failed"
  if [ "$(cat "$PACKET_DIR/proof-restore-$safe-exit.txt")" != "0" ]; then fail "proof show $f non-zero"; exit 2; fi
  cp "$PACKET_DIR/proof-restore-$safe-stdout.bin" "$PROOF_COPY/$f"
  cprc=$?
  echo "$cprc" > "$PACKET_DIR/proof-restore-$safe-cp-exit.txt"
  if [ "$cprc" != "0" ]; then fail "proof restore cp $f failed"; exit 2; fi
done
# remove ONLY 32 new intended files after pin verification (pins already verified above as final).
for f in "${UNTRACKED32[@]}"; do
  safe=$(echo "$f" | tr '/' '_')
  rm -f "$PROOF_COPY/$f"
  rrc=$?
  echo "$rrc" > "$PACKET_DIR/proof-rm-$safe-exit.txt"
  if [ "$rrc" != "0" ]; then fail "proof rm $f failed"; exit 2; fi
done
# verify scoped clean409: HEAD still 409, index clean, 689 tracked diff empty, 32 absent, HEAD blobs present.
run_cap "$PACKET_DIR/proof-clean-head-stdout.txt" "$PACKET_DIR/proof-clean-head-stderr.txt" "$PACKET_DIR/proof-clean-head-exit.txt" -- git --no-optional-locks -C "$PROOF_COPY" rev-parse HEAD || fail "proof clean head failed"
if [ "$(cat "$PACKET_DIR/proof-clean-head-stdout.txt" | tr -d '\n')" != "$EXPECT_HEAD" ]; then fail "proof clean HEAD mismatch (must stay 409, no commit)"; fi
run_cap "$PACKET_DIR/proof-clean-diff-cached-stdout.txt" "$PACKET_DIR/proof-clean-diff-cached-stderr.txt" "$PACKET_DIR/proof-clean-diff-cached-exit.txt" -- git --no-optional-locks -C "$PROOF_COPY" diff --cached --name-only || fail "proof clean cached failed"
if [ -n "$(cat "$PACKET_DIR/proof-clean-diff-cached-stdout.txt")" ]; then fail "proof clean index not empty"; fi
# scoped diff for 689 tracked intended files (those in HEAD): must be empty after restore.
# Build 689 list as SNAP 721 minus 32 new (i.e., DST HEAD 689 subset). Use python to list.
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/proof-clean-scoped-list-stdout.txt" "$PACKET_DIR/proof-clean-scoped-list-stderr.txt" "$PACKET_DIR/proof-clean-scoped-list-exit.txt" -- python3 -c "
import json
from pathlib import Path
m = json.loads(Path('$SNAP_MANIFEST').read_text())
new = set('''schemas/editorial-correction-proposal-v2.schema.json
schemas/editorial-manuscript-spec-v2.schema.json
schemas/editorial-publication-build-record-v2.schema.json
schemas/editorial-publication-set-v2.schema.json
schemas/editorial-publication-source-manifest-v2.schema.json
schemas/editorial-retention-manifest-v2.schema.json
schemas/editorial-staged-source-manifest-v2.schema.json
schemas/editorial-toolchain-spec-v2.schema.json
schemas/longform-publication-source-manifest-v2.schema.json
schemas/longform-reader-input-v2.schema.json
scripts/survey_editorial_correction_proposal_v2.py
scripts/survey_editorial_current_authority_v2.py
scripts/survey_editorial_publication_v2.py
scripts/survey_editorial_retention_v2.py
scripts/survey_editorial_staged_source_v2.py
scripts/survey_longform_derivation_v2.py
scripts/survey_longform_generated_v2.py
scripts/survey_longform_semantic_publication_v2.py
scripts/survey_publication_set_v2.py
tests/test_group_c_editorial_consumers_v2.py
tests/test_survey_editorial_activation_faults_r4c.py
tests/test_survey_editorial_correction_proposal_v2.py
tests/test_survey_editorial_current_authority_v2.py
tests/test_survey_editorial_r5_gaps_v2.py
tests/test_survey_editorial_r7_boundary_v2.py
tests/test_survey_editorial_retention_v2.py
tests/test_survey_editorial_staged_source_v2.py
tests/test_survey_longform_derivation_v2.py
tests/test_survey_longform_publication_integration_v2.py
tests/test_survey_publication_r3_anchor_shape_v2.py
tests/test_survey_publication_set_v2.py
tests/test_survey_schema_cache_v2.py'''.splitlines())
tracked689 = sorted([f['path'] for f in m['files'] if f['path'] not in new])
print('\n'.join(tracked689))
print(f'TRACKED689 count={len(tracked689)}', file=__import__('sys').stderr)
" || fail "proof scoped list failed"
# diff HEAD for those 689 must be empty (scoped clean).
run_cap "$PACKET_DIR/proof-clean-scoped-diff-stdout.txt" "$PACKET_DIR/proof-clean-scoped-diff-stderr.txt" "$PACKET_DIR/proof-clean-scoped-diff-exit.txt" -- git --no-optional-locks -C "$PROOF_COPY" diff HEAD --name-only -- $(cat "$PACKET_DIR/proof-clean-scoped-list-stdout.txt" | tr '\n' ' ') || fail "proof scoped diff failed"
# The helper file descriptor: proof-clean-scoped-diff-stdout contains names that differ; must be empty.
if [ -s "$PACKET_DIR/proof-clean-scoped-diff-stdout.txt" ]; then
  fail "proof scoped clean diff not empty (expected 689 at HEAD)"
  cat "$PACKET_DIR/proof-clean-scoped-diff-stdout.txt" > "$PACKET_DIR/proof-clean-scoped-nonempty.txt"
  exit 2
else
  echo "proof scoped clean 689 at HEAD OK (sources/surveys 31466 outside scope, disclosed)" | tee "$PACKET_DIR/proof-clean-scoped-ok.txt"
fi
# absent32 check.
absent_fail=0
for f in "${UNTRACKED32[@]}"; do
  if [ -e "$PROOF_COPY/$f" ]; then echo "STILL_PRESENT $f" >> "$PACKET_DIR/proof-clean-absent-fail.txt"; absent_fail=1; fi
done
if [ "$absent_fail" != "0" ]; then fail "proof clean absent32 failed"; exit 2; else echo "proof clean absent32 OK (32 absent)" | tee "$PACKET_DIR/proof-clean-absent-ok.txt"; fi
# 25 HEAD bytes check (must equal HEAD show blobs, no fakeRoot).
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/proof-clean-headbytes-stdout.txt" "$PACKET_DIR/proof-clean-headbytes-stderr.txt" "$PACKET_DIR/proof-clean-headbytes-exit.txt" -- python3 -c "
import hashlib, subprocess
from pathlib import Path
base = Path('$PROOF_COPY')
fails = 0
for rel in '''.github/workflows/build-special-pdf.yml
.github/workflows/build-weekly-survey.yml
.github/workflows/survey-production-v2-export-publication-preview.yml
config/survey-production-v2.json
schemas/publication-surface-revalidation.schema.json
schemas/reader-manuscript-v2.schema.json
schemas/reader-surface-gate-v2.schema.json
schemas/reader-surface-semantic-review-v2.schema.json
scripts/run_semantic_publication_v2_interactive.py
scripts/run_semantic_publication_v2_interactive_base.py
scripts/survey_agent_control_v2.py
scripts/survey_handoff_v2.py
scripts/survey_human_gate_v2.py
scripts/survey_orchestrator_v2.py
scripts/survey_production_v2.py
scripts/survey_profiled_freeze_v2.py
scripts/survey_reader_publication_v2.py
scripts/survey_reader_surface_gate_v2.py
scripts/survey_schema_v2.py
scripts/survey_semantic_quality_v2.py
scripts/survey_stage_validation_v2.py
scripts/survey_weekly_derivation_v2.py
scripts/survey_weekly_mechanical_refresh_v2.py
templates/survey/jgaisurvey.sty
tests/test_survey_dm004_release_validate_state_v2.py'''.splitlines():
  d = (base/rel).read_bytes()
  blob = subprocess.check_output(['git','--no-optional-locks','--git-dir', str(base/'.git'),'--work-tree', str(base),'show', f'HEAD:{rel}'])
  if d != blob:
    print(f'MISMATCH {rel} worktree != HEAD blob')
    fails += 1
  else:
    print(f'OK {rel} {len(d)}B == HEAD blob')
print(f'HEADBYTES fails={fails}')
exit(1 if fails else 0)
" || fail "proof clean headbytes failed"
if [ "$(cat "$PACKET_DIR/proof-clean-headbytes-exit.txt")" != "0" ]; then fail "proof clean headbytes mismatch"; exit 2; fi
if [ "$FAILURES" -ne 0 ]; then echo "PROOF CLEAN FAILURES=$FAILURES"; exit 2; fi

log "--- 5. PROOF apply SAVED patch check + apply separately (warnings preserved) ---"
run_cap "$PACKET_DIR/proof-apply-check-stdout.txt" "$PACKET_DIR/proof-apply-check-stderr.txt" "$PACKET_DIR/proof-apply-check-exit.txt" -- git --no-optional-locks -C "$PROOF_COPY" apply --check --verbose "$PATCH_OUT" || fail "proof apply --check failed"
checkrc=$(cat "$PACKET_DIR/proof-apply-check-exit.txt")
if [ "$checkrc" != "0" ]; then fail "proof --check non-zero rc=$checkrc"; echo "CHECK_FAILED"; exit 2; else echo "proof --check rc=0 OK" | tee "$PACKET_DIR/proof-check-ok.txt"; fi
run_cap "$PACKET_DIR/proof-apply-stdout.txt" "$PACKET_DIR/proof-apply-stderr.txt" "$PACKET_DIR/proof-apply-exit.txt" -- git --no-optional-locks -C "$PROOF_COPY" apply --verbose "$PATCH_OUT" || fail "proof apply failed"
applyrc=$(cat "$PACKET_DIR/proof-apply-exit.txt")
if [ "$applyrc" != "0" ]; then fail "proof apply non-zero rc=$applyrc"; exit 2; else echo "proof apply rc=0 OK" | tee "$PACKET_DIR/proof-apply-ok.txt"; fi
if [ "$FAILURES" -ne 0 ]; then echo "PROOF APPLY FAILURES=$FAILURES"; exit 2; fi

log "--- 6. PROOF validate exact 721 + delta 57 (content/Git modes, no whitespace fix) ---"
run_cap "$PACKET_DIR/proof-after-head-stdout.txt" "$PACKET_DIR/proof-after-head-stderr.txt" "$PACKET_DIR/proof-after-head-exit.txt" -- git --no-optional-locks -C "$PROOF_COPY" rev-parse HEAD || fail "proof after head failed"
if [ "$(cat "$PACKET_DIR/proof-after-head-stdout.txt" | tr -d '\n')" != "$EXPECT_HEAD" ]; then fail "proof after HEAD changed (must stay 409, no commit/new ancestry)"; fi
run_cap "$PACKET_DIR/proof-after-diff-cached-stdout.txt" "$PACKET_DIR/proof-after-diff-cached-stderr.txt" "$PACKET_DIR/proof-after-diff-cached-exit.txt" -- git --no-optional-locks -C "$PROOF_COPY" diff --cached --name-only || fail "proof after cached failed"
# apply without --index must not stage; index must stay clean.
if [ -n "$(cat "$PACKET_DIR/proof-after-diff-cached-stdout.txt")" ]; then fail "proof after index staged (apply must not stage)"; fi
export PROOF_COPY SNAP_MANIFEST PACKET_DIR GEN_COPY
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/proof-after-721-stdout.txt" "$PACKET_DIR/proof-after-721-stderr.txt" "$PACKET_DIR/proof-after-721-exit.txt" -- python3 -c "
import json, hashlib, stat, subprocess
from pathlib import Path
proof = Path('$PROOF_COPY')
snap = Path('$SNAP_SRC')
m = json.loads(Path('$SNAP_MANIFEST').read_text())
fails = 0
for f in m['files']:
  rel = f['path']
  pd = (proof/rel).read_bytes() if (proof/rel).exists() else None
  if pd is None:
    print(f'MISSING_PROOF {rel}')
    fails += 1
    continue
  ph = hashlib.sha256(pd).hexdigest()
  if ph != f['sha256'] or len(pd) != f['bytes']:
    print(f\"MISMATCH_PROOF {rel} got {ph[:8]}/{len(pd)} exp {f['sha256'][:8]}/{f['bytes']}\")
    fails += 1
print(f'PROOF_AFTER_721 fails={fails} total={len(m[\"files\"])}')
# delta 57 must equal DST final (which equals SNAP, already checked) — re-verify proof 57 vs SNAP 57.
known57 = '''.github/workflows/build-special-pdf.yml
.github/workflows/build-weekly-survey.yml
.github/workflows/survey-production-v2-export-publication-preview.yml
config/survey-production-v2.json
schemas/editorial-correction-proposal-v2.schema.json
schemas/editorial-manuscript-spec-v2.schema.json
schemas/editorial-publication-build-record-v2.schema.json
schemas/editorial-publication-set-v2.schema.json
schemas/editorial-publication-source-manifest-v2.schema.json
schemas/editorial-retention-manifest-v2.schema.json
schemas/editorial-staged-source-manifest-v2.schema.json
schemas/editorial-toolchain-spec-v2.schema.json
schemas/longform-publication-source-manifest-v2.schema.json
schemas/longform-reader-input-v2.schema.json
schemas/publication-surface-revalidation.schema.json
schemas/reader-manuscript-v2.schema.json
schemas/reader-surface-gate-v2.schema.json
schemas/reader-surface-semantic-review-v2.schema.json
scripts/run_semantic_publication_v2_interactive.py
scripts/run_semantic_publication_v2_interactive_base.py
scripts/survey_agent_control_v2.py
scripts/survey_editorial_correction_proposal_v2.py
scripts/survey_editorial_current_authority_v2.py
scripts/survey_editorial_publication_v2.py
scripts/survey_editorial_retention_v2.py
scripts/survey_editorial_staged_source_v2.py
scripts/survey_handoff_v2.py
scripts/survey_human_gate_v2.py
scripts/survey_longform_derivation_v2.py
scripts/survey_longform_generated_v2.py
scripts/survey_longform_semantic_publication_v2.py
scripts/survey_orchestrator_v2.py
scripts/survey_production_v2.py
scripts/survey_profiled_freeze_v2.py
scripts/survey_publication_set_v2.py
scripts/survey_reader_publication_v2.py
scripts/survey_reader_surface_gate_v2.py
scripts/survey_schema_v2.py
scripts/survey_semantic_quality_v2.py
scripts/survey_stage_validation_v2.py
scripts/survey_weekly_derivation_v2.py
scripts/survey_weekly_mechanical_refresh_v2.py
templates/survey/jgaisurvey.sty
tests/test_group_c_editorial_consumers_v2.py
tests/test_survey_dm004_release_validate_state_v2.py
tests/test_survey_editorial_activation_faults_r4c.py
tests/test_survey_editorial_correction_proposal_v2.py
tests/test_survey_editorial_current_authority_v2.py
tests/test_survey_editorial_r5_gaps_v2.py
tests/test_survey_editorial_r7_boundary_v2.py
tests/test_survey_editorial_retention_v2.py
tests/test_survey_editorial_staged_source_v2.py
tests/test_survey_longform_derivation_v2.py
tests/test_survey_longform_publication_integration_v2.py
tests/test_survey_publication_r3_anchor_shape_v2.py
tests/test_survey_publication_set_v2.py
tests/test_survey_schema_cache_v2.py'''.splitlines()
for rel in known57:
  pd = (proof/rel).read_bytes()
  sd = (snap/rel).read_bytes()
  if pd != sd:
    print(f'DELTA_MISMATCH {rel}')
    fails += 1
print(f'DELTA57 vs SNAP fails={fails}')
exit(1 if fails else 0)
" || fail "proof after 721 failed"
if [ "$(cat "$PACKET_DIR/proof-after-721-exit.txt")" != "0" ]; then fail "proof after not exact 721 + delta (stop, don't change source)"; exit 2; else echo "proof after exact 721 + delta 57 OK" | tee "$PACKET_DIR/proof-after-721-ok.txt"; fi
# Git modes (100644) from GEN temp index + physical observed modes (664 vs 644) separate; don't fake all equal.
export GIT_INDEX_FILE="$GEN_INDEX"
run_cap "$PACKET_DIR/proof-gitmodes-gen-stdout.txt" "$PACKET_DIR/proof-gitmodes-gen-stderr.txt" "$PACKET_DIR/proof-gitmodes-gen-exit.txt" -- git --no-optional-locks --git-dir="$GEN_COPY/.git" --work-tree="$GEN_COPY" ls-files -s || fail "gen ls-files -s full failed"
unset GIT_INDEX_FILE
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/proof-modes-compare-stdout.txt" "$PACKET_DIR/proof-modes-compare-stderr.txt" "$PACKET_DIR/proof-modes-compare-exit.txt" -- python3 -c "
import stat, subprocess
from pathlib import Path
proof = Path('$PROOF_COPY')
# Git modes for 57 from GEN temp index file (parse ls-files -s output).
gen_ls = Path('$PACKET_DIR/proof-gitmodes-gen-stdout.txt').read_text().splitlines()
gitmode_by_path = {}
for line in gen_ls:
  # format: <mode> <blob> <stage> <path>
  parts = line.split(None, 3)
  if len(parts) == 4:
    mode, blob, stage, path = parts
    gitmode_by_path[path] = (mode, blob)
fails = 0
for rel in open('$PACKET_DIR/gen-diff-cached-names-stdout.txt').read().splitlines():
  rel = rel.strip()
  if not rel:
    continue
  gm = gitmode_by_path.get(rel)
  if not gm:
    print(f'NO_GITMODE {rel}')
    fails += 1
    continue
  mode, blob = gm
  phys = oct(stat.S_IMODE((proof/rel).stat().st_mode))
  print(f'{rel} git_mode={mode} blob={blob[:8]} physical={phys}')
  if mode != '100644':
    print(f'  UNEXPECTED_GITMODE {rel} {mode}')
    fails += 1
print(f'MODES fails={fails} (physical 664 vs 644 recorded separately, not faked equal)')
# Do not fail on physical 644 vs 664 differences; only fail if Git mode unexpected or missing.
# Physical differences are disclosed in manifest, not normalized.
exit(1 if fails else 0)
" || fail "modes compare failed"
if [ "$(cat "$PACKET_DIR/proof-modes-compare-exit.txt")" != "0" ]; then fail "git modes unexpected"; exit 2; fi
if [ "$FAILURES" -ne 0 ]; then echo "PROOF VALIDATE FAILURES=$FAILURES"; exit 2; fi

# 7. Source after guards: DST unchanged (HEAD/status/pins).
log "--- 7. source after unchanged (DST + SNAP immutable) ---"
run_cap "$PACKET_DIR/src-after-head-stdout.txt" "$PACKET_DIR/src-after-head-stderr.txt" "$PACKET_DIR/src-after-head-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" rev-parse HEAD || fail "src after head failed"
run_cap "$PACKET_DIR/src-after-status-all-stdout.txt" "$PACKET_DIR/src-after-status-all-stderr.txt" "$PACKET_DIR/src-after-status-all-exit.txt" -- git --no-optional-locks -C "$CAND_SRC" status --porcelain=v1 --untracked-files=all || fail "src after status failed"
if ! diff -q "$PACKET_DIR/src-before-status-all-stdout.txt" "$PACKET_DIR/src-after-status-all-stdout.txt" > "$PACKET_DIR/src-after-status-diff-stdout.txt" 2> "$PACKET_DIR/src-after-status-diff-stderr.txt"; then
  echo "1" > "$PACKET_DIR/src-after-status-diff-exit.txt"
  fail "source DST changed during packaging (must be immutable)"
  exit 2
else
  echo "0" > "$PACKET_DIR/src-after-status-diff-exit.txt"
  echo "source DST before/after identical OK (immutable, no source edits)" | tee "$PACKET_DIR/src-after-ok.txt"
fi
run_cap "$PACKET_DIR/snap-after-head-stdout.txt" "$PACKET_DIR/snap-after-head-stderr.txt" "$PACKET_DIR/snap-after-head-exit.txt" -- git --no-optional-locks -C "$SNAP_SRC" rev-parse HEAD || fail "snap after head failed"
if [ "$(cat "$PACKET_DIR/snap-after-head-stdout.txt" | tr -d '\n')" != "$SNAP_HEAD" ]; then fail "snapshot changed (must be immutable)"; fi
run_cap "$PACKET_DIR/snap-after-status-stdout.txt" "$PACKET_DIR/snap-after-status-stderr.txt" "$PACKET_DIR/snap-after-status-exit.txt" -- git --no-optional-locks -C "$SNAP_SRC" status --porcelain=v1 --untracked-files=all || fail "snap after status failed"
if ! diff -q "$PACKET_DIR/snap-status-stdout.txt" "$PACKET_DIR/snap-after-status-stdout.txt" > "$PACKET_DIR/snap-after-diff-stdout.txt" 2> "$PACKET_DIR/snap-after-diff-stderr.txt"; then
  echo "1" > "$PACKET_DIR/snap-after-diff-exit.txt"
  fail "snapshot status changed"
  exit 2
else
  echo "0" > "$PACKET_DIR/snap-after-diff-exit.txt"
  echo "snapshot before/after identical OK" | tee "$PACKET_DIR/snap-after-ok.txt"
fi

# 8. Manifest FULL JSON (57 paths SHA/bytes/Git mode/physical mode + source before/after + GEN/PROOF).
log "--- 8. manifest FULL (57 delta, 721 verified) ---"
patch_sha2=$(sha256sum "$PATCH_OUT" | awk '{print $1}')
patch_bytes2=$(stat -c '%s' "$PATCH_OUT")
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/manifest-gen-stdout.txt" "$PACKET_DIR/manifest-gen-stderr.txt" "$PACKET_DIR/manifest-gen-exit.txt" -- python3 -c "
import json, hashlib, stat, subprocess
from pathlib import Path
proof = Path('$PROOF_COPY')
gen_ls = Path('$PACKET_DIR/proof-gitmodes-gen-stdout.txt').read_text().splitlines()
gitmode_by_path = {}
for line in gen_ls:
  parts = line.split(None, 3)
  if len(parts) == 4:
    mode, blob, stage, path = parts
    # only keep 57 (ls-files -s was scoped to 57, but full file may contain only 57).
    gitmode_by_path[path] = (mode, blob)
files = {}
known57 = [l.strip() for l in Path('$PACKET_DIR/gen-diff-cached-names-stdout.txt').read_text().splitlines() if l.strip()]
assert len(known57) == 57, len(known57)
for rel in sorted(known57):
  fp = proof/rel
  d = fp.read_bytes()
  gm, blob = gitmode_by_path.get(rel, ('MISSING','MISSING'))
  phys = oct(stat.S_IMODE(fp.stat().st_mode))
  # git blob SHA1 via hash-object for cross-check (content blob, not SHA256).
  blob2 = subprocess.check_output(['git','--no-optional-locks','hash-object', str(fp)], text=True).strip()
  files[rel] = {
    'sha256': hashlib.sha256(d).hexdigest(),
    'bytes': len(d),
    'git_mode': gm,
    'git_blob': blob,
    'git_blob_hash_object': blob2,
    'physical_mode': phys,
    'git_status': 'TBD'
  }
# fix git_status: M for 25 tracked, A for 32 new.
tracked25 = set('''.github/workflows/build-special-pdf.yml
.github/workflows/build-weekly-survey.yml
.github/workflows/survey-production-v2-export-publication-preview.yml
config/survey-production-v2.json
schemas/publication-surface-revalidation.schema.json
schemas/reader-manuscript-v2.schema.json
schemas/reader-surface-gate-v2.schema.json
schemas/reader-surface-semantic-review-v2.schema.json
scripts/run_semantic_publication_v2_interactive.py
scripts/run_semantic_publication_v2_interactive_base.py
scripts/survey_agent_control_v2.py
scripts/survey_handoff_v2.py
scripts/survey_human_gate_v2.py
scripts/survey_orchestrator_v2.py
scripts/survey_production_v2.py
scripts/survey_profiled_freeze_v2.py
scripts/survey_reader_publication_v2.py
scripts/survey_reader_surface_gate_v2.py
scripts/survey_schema_v2.py
scripts/survey_semantic_quality_v2.py
scripts/survey_stage_validation_v2.py
scripts/survey_weekly_derivation_v2.py
scripts/survey_weekly_mechanical_refresh_v2.py
templates/survey/jgaisurvey.sty
tests/test_survey_dm004_release_validate_state_v2.py'''.splitlines())
for rel in files:
  files[rel]['git_status'] = 'M' if rel in tracked25 else 'A'
man = {
  'candidate_dst': '$CAND_SRC',
  'head': '$EXPECT_HEAD',
  'head_tree': '$EXPECT_TREE',
  'snapshot_r7b': '$SNAP_SRC',
  'snapshot_head': '$SNAP_HEAD',
  'snapshot_tree': '$SNAP_TREE',
  'snapshot_manifest': 'notes/rephase-1-editorial-operation-implementation/correction-r7/source-manifest-r7b.json',
  'intended_721': 721,
  'intended_721_verified': True,
  'delta_count': 57,
  'tracked_modified': 25,
  'untracked_new': 32,
  'status_summary': '25M+32A=57 (raw 60 incl. notes/pycache/tmp excluded; LC_ALL=C sorted)',
  'patch': {'path': 'complete-r3-operation-409.patch', 'sha256': '$patch_sha2', 'bytes': int('$patch_bytes2')},
  'files': files,
  'proof': {
    'gen_copy': '$GEN_COPY',
    'proof_copy': '$PROOF_COPY',
    'gen_index': '$GEN_INDEX',
    'gen_index_outside_packet': True,
    'check_exit': open('$PACKET_DIR/proof-apply-check-exit.txt').read().strip(),
    'apply_exit': open('$PACKET_DIR/proof-apply-exit.txt').read().strip(),
    'check_stderr_bytes': int(__import__('os').stat('$PACKET_DIR/proof-apply-check-stderr.txt').st_size),
    'apply_stderr_bytes': int(__import__('os').stat('$PACKET_DIR/proof-apply-stderr.txt').st_size),
    'scope': 'scoped 689 tracked at HEAD + 32 absent (sources/surveys 31466 outside scope, unchanged, not in patch); final 721 exact + delta 57; HEAD stays 409, no commit/new ancestry'
  },
  'source_before_after': {
    'dst_before_head': open('$PACKET_DIR/src-before-rev-parse-head-stdout.txt').read().strip(),
    'dst_after_head': open('$PACKET_DIR/src-after-head-stdout.txt').read().strip(),
    'snap_before_head': open('$PACKET_DIR/snap-rev-parse-head-stdout.txt').read().strip(),
    'snap_after_head': open('$PACKET_DIR/snap-after-head-stdout.txt').read().strip(),
    'dst_unchanged': True,
    'snap_unchanged': True
  },
  'notes': 'partialDB 26309 missing blobs retained (not full-history cert); runtime unbundled; current packaging observation only, not continuous no-drift/global cert; no generic rerunner cert; no old runners; no network; no source edits; inherited whitespace warnings preserved, not normalized; physical 644 vs 664 recorded separately from Git 100644, not faked equal; only needed inputs old four parent + complete 57 patch'
}
Path('$MANIFEST_OUT').write_text(json.dumps(man, indent=1, sort_keys=True))
print(f\"manifest wrote delta={len(files)} patch {'$patch_sha2'} {'$patch_bytes2'}B intended721 verified\")
" || fail "manifest gen failed"
if [ "$(cat "$PACKET_DIR/manifest-gen-exit.txt")" != "0" ]; then fail "manifest gen non-zero"; exit 2; fi
# validate manifest FULL JSON (must be valid, delta57 + intended721).
PYTHONDONTWRITEBYTECODE=1 run_cap "$PACKET_DIR/manifest-valid-stdout.txt" "$PACKET_DIR/manifest-valid-stderr.txt" "$PACKET_DIR/manifest-valid-exit.txt" -- python3 -c "
import json
from pathlib import Path
m = json.loads(Path('$MANIFEST_OUT').read_text())
assert m['delta_count'] == 57 and len(m['files']) == 57, f\"delta {m['delta_count']} files {len(m['files'])}\"
assert m['intended_721'] == 721 and m['intended_721_verified'] is True
print(f\"manifest valid FULL: delta57 + intended721 verified, patch {m['patch']['sha256'][:8]} {m['patch']['bytes']}B\")
" || fail "manifest valid failed"
if [ "$(cat "$PACKET_DIR/manifest-valid-exit.txt")" != "0" ]; then fail "manifest invalid"; exit 2; fi
# verify no .git/index in packet.
if [ -d "$PACKET_DIR/.git" ]; then fail ".git leaked into packet"; fi
if [ -e "$PACKET_DIR/index" ] || [ -e "$PACKET_DIR/gen-index" ]; then fail "index leaked into packet"; fi
run_cap "$PACKET_DIR/packet-find-git-stdout.txt" "$PACKET_DIR/packet-find-git-stderr.txt" "$PACKET_DIR/packet-find-git-exit.txt" -- find "$PACKET_DIR" -maxdepth 2 -name .git || fail "find git failed"
if [ -s "$PACKET_DIR/packet-find-git-stdout.txt" ]; then fail ".git found in packet"; fi
ls -1 "$PACKET_DIR" > "$PACKET_DIR/packet-list.txt"
echo "packet files:" >> "$PACKET_DIR/packet-list.txt"

echo "=== COMPLETE-R3-OPERATION packaging done FAILURES=$FAILURES ==="
if [ "$FAILURES" -ne 0 ]; then exit 2; else exit 0; fi
