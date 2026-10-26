#!/bin/bash
# Reader F4 test execution in NEW isolated snapshot (no shared candidate exec).
# No network/old runners/cleanup/reset. Captures raw exit/stdout/stderr.
set -u
export LC_ALL=C
export PYTHONDONTWRITEBYTECODE=1
export GIT_NO_LAZY_FETCH=1
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_OPTIONAL_LOCKS=0
export PYTHONPATH=""
if [ -n "${GIT_DIR:-}" ] || [ -n "${GIT_WORK_TREE:-}" ] || [ -n "${GIT_INDEX_FILE:-}" ]; then
  echo "FAIL inherited GIT_*"
  exit 2
fi
RECON="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
DST="$RECON/.rephase-1-editorial-runtime/versioned-renewal-readerf4-20261025T060000Z/snapshot-work"
EVID="$RECON/notes/rephase-1-versioned-renewal-implementation/resume-20261025/reader-correction"
WEEKLY="$RECON/.rephase-1-editorial-runtime/versioned-renewal-high24-20261025T040000Z/renewal-weekly"
export READER_F4_WEEKLY_ROOT="$WEEKLY"
cd "$DST"
echo "DST_HEAD=$(git -C "$DST" rev-parse HEAD)"
echo "WEEKLY_HEAD=$(git -C "$WEEKLY" rev-parse HEAD)"
echo "PYTHON=$(which python3) $(python3 --version 2>&1)"
# Record pre-test mutation absence (temp files must not pre-exist).
ls "$WEEKLY/sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-c1-weekly/" | grep -E "f4-.*tmp" || echo "PRE_CLEAN_OK"
# Run ONLY the new dedicated F4 oracles (7 tests) with verbose unittest.
# Timeout 20 minutes (history git walks can be slow; run54 timeouts were 3min probes).
python3 -m unittest tests.test_versioned_renewal_reader_f4_20261025 -v
RC=$?
echo "TEST_RC=$RC"
# Post-test mutation restore check.
ls "$WEEKLY/sources/2026-W37/publication/v2/editorial-corrections/wk-boot-1/renewals/high-c1-weekly/" | grep -E "f4-.*tmp" && echo "POST_DIRTY_FAIL" || echo "POST_CLEAN_OK"
exit $RC
