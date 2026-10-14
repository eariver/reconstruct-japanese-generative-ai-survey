#!/usr/bin/env bash
# P2R run_p2r_v3.sh — re-run after fixture .github fix (v1/v2 failures preserved).
# Saved BEFORE execution; prior outputs never overwritten.
set -u
echo "=== argv: $0 $* ==="
for k in $(env | cut -d= -f1 | grep '^GIT_' || true); do unset "$k"; done
export GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file
echo "GIT_NO_LAZY_FETCH=$GIT_NO_LAZY_FETCH GIT_OPTIONAL_LOCKS=$GIT_OPTIONAL_LOCKS GIT_ALLOW_PROTOCOL=$GIT_ALLOW_PROTOCOL"
echo "residual: $(env | cut -d= -f1 | grep '^GIT_' | sort | tr '\n' ' ')"
/usr/bin/python3 --version
/usr/bin/git --version
/usr/bin/python3 -c "import sys; print('exe=' + sys.executable)"
echo "=== pre ==="
/usr/bin/git rev-parse HEAD
/usr/bin/git rev-parse 'HEAD^{tree}'
/usr/bin/git status --porcelain=v1 -uall
/usr/bin/git diff --name-only
echo "=== unittest ==="
/usr/bin/python3 -m unittest tests.test_survey_editorial_retention_v2 -v
echo "unittest_rc=$?"
echo "=== -O smoke ==="
/usr/bin/python3 -O -m unittest tests.test_survey_editorial_retention_v2.EditorialRetentionV2Tests.test_weekly_capture_verify_positive -v
echo "optimized_rc=$?"
echo "=== post ==="
/usr/bin/git status --porcelain=v1 -uall
/usr/bin/git diff --name-only
echo "RUN_P2R_V3_DONE"
