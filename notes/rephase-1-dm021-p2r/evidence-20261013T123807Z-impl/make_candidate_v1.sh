#!/usr/bin/env bash
# P2R make_candidate_v1.sh — NEW independent byte copy, no P1 mutation.
# Saved BEFORE execution; every executed version survives; failures preserved.
# Sanitizes ALL inherited GIT_* then forces GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file.
set -u
SRC="/tmp/opencode/jgas-dm021p1-phaseA-20261011T160037Z/candidate-partial-b40de60"
DST_BASE="/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z"
DST="$DST_BASE/candidate-partial-b40de60"
echo "SRC=$SRC"
echo "DST=$DST"
echo "--- preflight src ---"
ls -la "$SRC" | head -n 20
test -d "$SRC/.git" || { echo "SRC_MISSING_GIT"; exit 10; }
test ! -L "$SRC" || { echo "SRC_IS_SYMLINK"; exit 11; }
test ! -L "$SRC/.git" || { echo "SRC_GIT_SYMLINK"; exit 12; }
if [ -e "$DST" ]; then echo "DST_ALREADY_EXISTS refused"; exit 13; fi
mkdir -p "$DST_BASE"
echo "--- byte copy (cp -a, no hardlinks, no reflink) ---"
cp -a --reflink=never "$SRC" "$DST"
echo "copy_rc=$?"
echo "--- dst listing ---"
ls -la "$DST" | head -n 20
ls -la "$DST/.git" | head -n 30
echo "--- sanitize ALL GIT_* then force 3 ---"
for k in $(env | cut -d= -f1 | grep '^GIT_' || true); do unset "$k"; done
export GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file
echo "forced: GIT_NO_LAZY_FETCH=$GIT_NO_LAZY_FETCH GIT_OPTIONAL_LOCKS=$GIT_OPTIONAL_LOCKS GIT_ALLOW_PROTOCOL=$GIT_ALLOW_PROTOCOL"
echo "residual_GIT_vars: $(env | cut -d= -f1 | grep '^GIT_' | sort | tr '\n' ' ')"
echo "--- identity (read-only, no mutations) ---"
git -C "$DST" rev-parse HEAD
echo "revparse_rc=$?"
git -C "$DST" rev-parse 'HEAD^{tree}'
echo "tree_rc=$?"
git -C "$DST" status --porcelain=v1 -uall
echo "status_rc=$?"
git -C "$DST" diff --name-only
echo "diff_rc=$?"
echo "--- config/remote (must be inert) ---"
git -C "$DST" config --local --list
echo "config_rc=$?"
git -C "$DST" remote -v
echo "remote_rc=$?"
echo "--- alternates/shallow/index checks ---"
ls -la "$DST/.git/objects/info/" || true
test ! -e "$DST/.git/objects/info/alternates" && echo "no_alternates_OK" || echo "ALTERNATES_PRESENT"
ls -l "$DST/.git/shallow" "$DST/.git/index" || true
test ! -L "$DST/.git" && echo "gitdir_not_symlink_OK" || echo "GITDIR_SYMLINK"
echo "--- no-sharing inode check (src vs dst must differ) ---"
for f in scripts/survey_editorial_correction_proposal_v2.py schemas/editorial-correction-proposal-v2.schema.json tests/test_survey_editorial_correction_proposal_v2.py .git/HEAD; do
  a=$(stat -c '%d:%i' "$SRC/$f"); b=$(stat -c '%d:%i' "$DST/$f"); echo "$f src=$a dst=$b"; test "$a" != "$b" || echo "SHARED_INODE_FAIL:$f";
done
echo "--- P1 13 presence + P2R 3 absence ---"
for f in schemas/reader-surface-gate-v2.schema.json schemas/reader-surface-semantic-review-v2.schema.json scripts/survey_reader_surface_gate_v2.py schemas/editorial-correction-proposal-v2.schema.json schemas/longform-publication-source-manifest-v2.schema.json schemas/longform-reader-input-v2.schema.json scripts/survey_editorial_correction_proposal_v2.py scripts/survey_longform_derivation_v2.py scripts/survey_longform_generated_v2.py scripts/survey_longform_semantic_publication_v2.py tests/test_survey_editorial_correction_proposal_v2.py tests/test_survey_longform_derivation_v2.py tests/test_survey_longform_publication_integration_v2.py; do test -f "$DST/$f" || echo "MISSING:$f"; done; echo "p1_13_check_done"
for f in scripts/survey_editorial_retention_v2.py schemas/editorial-retention-manifest-v2.schema.json tests/test_survey_editorial_retention_v2.py; do test ! -e "$DST/$f" && echo "absent_OK:$f" || echo "UNEXPECTED_PRESENT:$f"; done
echo "--- runtime (probes only, no imports/tests) ---"
/usr/bin/python3 --version; /usr/bin/git --version; echo "sys_exe=/usr/bin/python3"
echo "MAKE_CANDIDATE_V1_DONE"
