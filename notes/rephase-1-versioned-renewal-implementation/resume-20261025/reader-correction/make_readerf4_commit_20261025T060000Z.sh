#!/bin/bash
# Reader F4 SOURCE commit (isolated DB only) + test execution.
# No ordinary candidate/reconstruct commit; no network/old runners/cleanup/reset.
set -u
export LC_ALL=C
export PYTHONDONTWRITEBYTECODE=1
export GIT_NO_LAZY_FETCH=1
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_OPTIONAL_LOCKS=0
if [ -n "${GIT_DIR:-}" ] || [ -n "${GIT_WORK_TREE:-}" ] || [ -n "${GIT_INDEX_FILE:-}" ]; then
  echo "FAIL inherited GIT_*"
  exit 2
fi
RECON="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
DST="$RECON/.rephase-1-editorial-runtime/versioned-renewal-readerf4-20261025T060000Z/snapshot-work"
EVID="$RECON/notes/rephase-1-versioned-renewal-implementation/resume-20261025/reader-correction"
WEEKLY="$RECON/.rephase-1-editorial-runtime/versioned-renewal-high24-20261025T040000Z/renewal-weekly"
echo "DST=$DST"
git -C "$DST" rev-parse HEAD
git -C "$DST" status --porcelain=v1 --untracked-files=all | wc -l
# Process-scoped identity for synthetic fixture SOURCE commit (isolated DB only).
export GIT_AUTHOR_NAME="Reader F4 Fix"
export GIT_AUTHOR_EMAIL="reader-f4-test@example.invalid"
export GIT_COMMITTER_NAME="Reader F4 Fix"
export GIT_COMMITTER_EMAIL="reader-f4-test@example.invalid"
# Stage complete 732 (frozen 731 + F4 fix + F4 test) as isolated TEST-ONLY SOURCE.
git -C "$DST" add -A
git -C "$DST" status --porcelain=v1 --untracked-files=all | wc -l
git -C "$DST" --no-optional-locks commit -m "Reader F4 fix TEST-ONLY: refuse neither-with-proof (C requires serialized renewal_source)

Isolated test SOURCE only (independent DB, HEAD was 409b292). Frozen
snapshot 731 (39M42U at 20261024T174422Z) + OWN files only:
- scripts/survey_reader_publication_v2.py (F4: neither+proof REVIEW_TARGET_MISMATCH)
- tests/test_versioned_renewal_reader_f4_20261025.py (new dedicated oracles)
Other H/S/HIGH/consumer files are frozen inputs preserved unchanged here,
not authored in this fix. No candidate/reconstruct authority."
git -C "$DST" rev-parse HEAD
git -C "$DST" log --oneline -3
git -C "$DST" status --porcelain=v1 --untracked-files=all
echo "COMMIT_DONE"
# Pin weekly fixture SHAs (source pins for evidence).
sha256sum "$WEEKLY/sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-c1-weekly/reader-manuscript-v2.json"
sha256sum "$WEEKLY/sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-c1-weekly/renewal-source-proof.json"
sha256sum "$WEEKLY/sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-u1-weekly/renewal-source-proof.json"
sha256sum "$WEEKLY/sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-u2-weekly/renewal-source-proof.json"
sha256sum "$WEEKLY/sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/publication/reader-manuscript-v2.json"
sha256sum "$WEEKLY/sources/2026-W37/publication/v2/reader-manuscript-v2.json"
# Record weekly HEADs (tool epochs).
git -C "$WEEKLY" rev-parse HEAD
echo "PINS_DONE"
