#!/usr/bin/env bash
# P2R run_opt_v1.sh — single -O smoke on FINAL code (weekly positive).
set -u
for k in $(env | cut -d= -f1 | grep '^GIT_' || true); do unset "$k"; done
export GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file
/usr/bin/python3 --version
/usr/bin/git --version
/usr/bin/git rev-parse HEAD
/usr/bin/python3 -O -m unittest tests.test_survey_editorial_retention_v2.EditorialRetentionV2Tests.test_weekly_capture_verify_positive -v
echo "optimized_rc=$?"
