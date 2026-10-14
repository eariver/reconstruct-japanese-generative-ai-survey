#!/usr/bin/env bash
# P2R run_p2r_v5.sh — re-run after R1 expectation + manifest-filename + schema-wrap fixes (v1-v4 preserved).
set -u
echo "=== argv: $0 $* ==="
for k in $(env | cut -d= -f1 | grep '^GIT_' || true); do unset "$k"; done
export GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file
echo "forced3: $GIT_NO_LAZY_FETCH $GIT_OPTIONAL_LOCKS $GIT_ALLOW_PROTOCOL"
/usr/bin/python3 --version
/usr/bin/git --version
/usr/bin/python3 -c "import sys; print('exe=' + sys.executable)"
echo "=== pre ==="
/usr/bin/git rev-parse HEAD
/usr/bin/git rev-parse 'HEAD^{tree}'
/usr/bin/git status --porcelain=v1 -uall | grep -v __pycache__
/usr/bin/git diff --name-only
echo "=== unittest ==="
/usr/bin/python3 -m unittest tests.test_survey_editorial_retention_v2 -v
echo "unittest_rc=$?"
echo "=== -O smoke ==="
/usr/bin/python3 -O -m unittest tests.test_survey_editorial_retention_v2.EditorialRetentionV2Tests.test_weekly_capture_verify_positive -v
echo "optimized_rc=$?"
echo "=== post ==="
/usr/bin/git status --porcelain=v1 -uall | grep -v __pycache__
/usr/bin/git diff --name-only
echo "RUN_P2R_V5_DONE"
