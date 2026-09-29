#!/bin/sh
# R1 round2 durable suite runner. Usage: sh run-suite.sh <testmodule> <logfile>
# Appends header (HEAD/tree/parent, source hashes, argv, cwd, python/deps)
# then unittest -v output, then EXIT + counts footer. No tool-only results.
FIX=/tmp/jgas-rephase-mechanical-r1-20260928T000710Z
PY=/tmp/jgas-rephase-application-venv/bin/python3.12
DEPS_SCRIPT=/mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-mechanical-refresh/correction/deps.py
MOD=$1
LOG=$2
cd $FIX
{
echo "=== R1 round2 final suite (committed successor) ==="
echo "HEAD: $(git -C $FIX rev-parse HEAD)"
echo "TREE: $(git -C $FIX show -s --format=%T HEAD)"
echo "PARENT: $(git -C $FIX rev-parse HEAD^)"
echo "DATE-UTC: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "CWD: $(pwd)"
echo "ARGV: $PY -m unittest $MOD -v"
echo "PYTHON: $($PY --version 2>&1)"
echo "DEPS: $($PY $DEPS_SCRIPT 2>&1 | tr '\n' ';')"
echo "SOURCE-SHA256:"
sha256sum scripts/survey_weekly_mechanical_refresh_v2.py scripts/survey_agent_control_v2.py scripts/survey_reader_surface_gate_v2.py scripts/survey_weekly_derivation_v2.py tests/test_survey_weekly_mechanical_refresh_v2.py tests/test_survey_publication_revalidation_v2.py docs/weekly-mechanical-refresh.md
echo "--- unittest start ---"
$PY -m unittest $MOD -v
echo "EXIT:$?"
} > "$LOG" 2>&1
