#!/usr/bin/env bash
# R2 verification SOURCE snapshot — explicit intended 717 files, no residue/caches/evidence.
# Creates independent Git repo under /tmp/opencode unique root, explicit file list only.
# No DST edits, no clean/reset, no network. Inert origin example.invalid, no alternates/hardlinks.
# Usage: copy-check-source.sh <dst_root> <snapshot_root>
# Records: every intended path SHA bytes mode, total count, Git commit/tree, separation checks.
set -eu
DST="${1:-/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60}"
SNAP="${2:-/tmp/opencode/jgas-editorial-r2v-20261021T084804Z/candidate-partial-b40de60}"
echo "CMD: $0 $DST $SNAP"
echo "CWD: $(pwd)"
echo "DST_HEAD: $(git -C "$DST" rev-parse HEAD)"
echo "DST_STATUS_LINES: $(git -C "$DST" status --short | wc -l)"
mkdir -p "$SNAP"
# Explicit intended materialized tracked (689, exist as files) — no whole-dir cp.
git -C "$DST" ls-files | while read -r f; do
  if [ -f "$DST/$f" ]; then
    mkdir -p "$SNAP/$(dirname "$f")"
    cp -a "$DST/$f" "$SNAP/$f"
  fi
done
# Explicit selected new (28: 10 schemas + 9 scripts + 9 tests incl. cache test) — no tmpvr/cache.
for f in \
  schemas/editorial-correction-proposal-v2.schema.json \
  schemas/editorial-manuscript-spec-v2.schema.json \
  schemas/editorial-publication-build-record-v2.schema.json \
  schemas/editorial-publication-set-v2.schema.json \
  schemas/editorial-publication-source-manifest-v2.schema.json \
  schemas/editorial-retention-manifest-v2.schema.json \
  schemas/editorial-staged-source-manifest-v2.schema.json \
  schemas/editorial-toolchain-spec-v2.schema.json \
  schemas/longform-publication-source-manifest-v2.schema.json \
  schemas/longform-reader-input-v2.schema.json \
  scripts/survey_editorial_correction_proposal_v2.py \
  scripts/survey_editorial_current_authority_v2.py \
  scripts/survey_editorial_publication_v2.py \
  scripts/survey_editorial_retention_v2.py \
  scripts/survey_editorial_staged_source_v2.py \
  scripts/survey_longform_derivation_v2.py \
  scripts/survey_longform_generated_v2.py \
  scripts/survey_longform_semantic_publication_v2.py \
  scripts/survey_publication_set_v2.py \
  tests/test_group_c_editorial_consumers_v2.py \
  tests/test_survey_editorial_correction_proposal_v2.py \
  tests/test_survey_editorial_current_authority_v2.py \
  tests/test_survey_editorial_retention_v2.py \
  tests/test_survey_editorial_staged_source_v2.py \
  tests/test_survey_longform_derivation_v2.py \
  tests/test_survey_longform_publication_integration_v2.py \
  tests/test_survey_publication_set_v2.py \
  tests/test_survey_schema_cache_v2.py \
; do
  mkdir -p "$SNAP/$(dirname "$f")"
  cp -a "$DST/$f" "$SNAP/$f"
done
echo "COPIED_FILES: $(find "$SNAP" -type f | wc -l) (expect 717)"
echo "RESIDUE_CHECK_TMPVR: $(find "$SNAP" -path "*tmpvr07sdme*" | wc -l) (expect 0)"
echo "RESIDUE_CHECK_PYCACHE: $(find "$SNAP" -path "*__pycache__*" | wc -l) (expect 0)"
echo "RESIDUE_CHECK_PYC: $(find "$SNAP" -name "*.pyc" | wc -l) (expect 0)"
echo "GIT_DB_CHECK: $(ls -d "$SNAP/.git" 2>&1 || echo "no .git yet (pre-init, good)")"
git -C "$SNAP" init -q
git -C "$SNAP" config user.name "integration-r2-verify"
git -C "$SNAP" config user.email "r2-verify@example.invalid"
git -C "$SNAP" config commit.gpgsign false
git -C "$SNAP" add -A
echo "TRACKED: $(git -C "$SNAP" ls-files -s | wc -l) (expect 717)"
echo "UNTRACKED_AFTER_ADD: $(git -C "$SNAP" ls-files --others --exclude-standard | wc -l) (expect 0)"
echo "TMPVR_TRACKED: $(git -C "$SNAP" ls-files | grep -c "^tmpvr07sdme/" || echo 0) (expect 0)"
echo "PYCACHE_TRACKED: $(git -C "$SNAP" ls-files | grep -c "__pycache__" || echo 0) (expect 0)"
echo "ALTERNATES: $(ls "$SNAP/.git/objects/info/alternates" 2>&1)"
echo "REMOTE: $(git -C "$SNAP" remote -v 2>&1 || echo "none")"
echo "INODE_SAMPLE_DST: $(stat -c "%d:%i %h" "$DST/scripts/survey_schema_v2.py")"
echo "INODE_SAMPLE_SNAP: $(stat -c "%d:%i %h" "$SNAP/scripts/survey_schema_v2.py")"
GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null git -C "$SNAP" -c commit.gpgsign=false commit -qm "SOURCE snapshot: R2 verified intended 717 (Fix1 FULL + Fix2 cache + Fix3 P2V + revalidation type + P3S helper 50 + cache test) before authority" --no-verify
echo "SOURCE_HEAD: $(git -C "$SNAP" rev-parse HEAD)"
echo "SOURCE_TREE: $(git -C "$SNAP" rev-parse HEAD^{tree})"
echo "SOURCE_LOG: $(git -C "$SNAP" log -1 --format=%H_%ci_%s | cut -c1-120)"
echo "SOURCE_STATUS: $(git -C "$SNAP" status --short | wc -l) (expect 0 clean)"
echo "PRE_POST_PINS_UNCHANGED: DST not modified by this script (only reads DST, writes SNAP); verify DST HEAD still $(git -C "$DST" rev-parse HEAD)"
