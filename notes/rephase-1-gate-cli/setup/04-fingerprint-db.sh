#!/usr/bin/env bash
# Fingerprint the independent gate-cli DB and confirm key B bytes match the manifest.
set -uo pipefail
DST=/tmp/jgas-rephase-gate-cli
cd "$DST"
echo "HEAD=$(git rev-parse HEAD)"
echo "TREE=$(git rev-parse 'HEAD^{tree}')"
echo "PARENT=$(git rev-parse 'HEAD^')"
echo "BRANCH=$(git branch --show-current)"
echo "REMOTE=$(git remote get-url origin)"
echo "SHALLOW_BOUNDARY=$(cat .git/shallow)"
echo "== pack sha256 =="
sha256sum .git/objects/pack/*.pack
echo "== key file sha256 (expect matches notes/rephase-1-increment-b/candidate.json) =="
sha256sum scripts/survey_reader_surface_gate_v2.py scripts/survey_reader_publication_v2.py scripts/survey_weekly_semantic_publication_v2.py scripts/survey_weekly_derivation_v2.py schemas/reader-surface-semantic-review-v2.schema.json
echo "== gate test method count =="
grep -c "    def test_" tests/test_survey_reader_surface_gate_v2.py
echo "== python =="
/tmp/jgas-rephase-application-venv/bin/python3.12 --version
