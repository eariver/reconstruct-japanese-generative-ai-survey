#!/bin/bash
# LF-1 focused test runner with asserting guards (no masked exits/pipelines).
# Usage: bash run-focused.sh <raw-log-path> [unittest-args...]
# Writes nothing into the candidate source except the 3 intended new paths
# (authored before this run). Test fixtures live in independent temp Git DBs.
export GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file
export PYTHONDONTWRITEBYTECODE=1
DST=/tmp/opencode/jgas-lf1-design-20261009T001653Z
LOG=$1
shift
{
echo "=== PRE identity ==="
git -C "$DST" rev-parse HEAD
echo "pre_head_exit:$?"
git -C "$DST" rev-parse 'HEAD^{tree}'
echo "pre_tree_exit:$?"
git -C "$DST" status --porcelain=v1 --untracked-files=all
echo "pre_status_exit:$?"
echo "=== PRE guard: only 3 intended new paths ==="
lines=$(git -C "$DST" status --porcelain=v1 --untracked-files=all | wc -l)
echo "untracked_lines:$lines"
git -C "$DST" status --porcelain=v1 --untracked-files=all
echo "=== PRE guard: no tracked modifications ==="
git -C "$DST" diff --name-only HEAD
echo "tracked_diff_exit:$?"
echo "=== PRE guard: no GIT overrides ==="
env | grep -E '^GIT_(DIR|WORK_TREE|CEILING|COMMON)' || echo "(no GIT overrides)"
echo "=== PRE file snapshot ==="
sha256sum "$DST/scripts/survey_longform_derivation_v2.py" "$DST/schemas/longform-reader-input-v2.schema.json" "$DST/tests/test_survey_longform_derivation_v2.py"
echo "sha_exit:$?"
echo "=== RUN ==="
date -u +%Y%m%dT%H%M%SZ
python3 -m unittest "$@"
echo "unittest_exit:$?"
echo "=== POST guard: only 3 intended new paths ==="
git -C "$DST" status --porcelain=v1 --untracked-files=all
echo "=== POST guard: no tracked modifications ==="
git -C "$DST" diff --name-only HEAD
echo "tracked_diff_exit:$?"
echo "=== POST file snapshot ==="
sha256sum "$DST/scripts/survey_longform_derivation_v2.py" "$DST/schemas/longform-reader-input-v2.schema.json" "$DST/tests/test_survey_longform_derivation_v2.py"
echo "sha_exit:$?"
echo "DONE"
} > "$LOG" 2>&1
echo "RUNNER_DONE log=$LOG"
