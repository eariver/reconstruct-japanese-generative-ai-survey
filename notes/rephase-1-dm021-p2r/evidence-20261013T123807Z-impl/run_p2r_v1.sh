#!/usr/bin/env bash
# P2R run_p2r_v1.sh — focused actual accepted-chain suite, direct capture.
# Saved BEFORE execution; every executed version/failed output survives.
# Strips ALL inherited GIT_* then forces 3. No add-N, no commits, no cleanup
# before comparisons, no filtered-status. Explicit -O handling.
set -u
echo "=== argv: $0 $* ==="
echo "=== forced GIT routing ==="
for k in $(env | cut -d= -f1 | grep '^GIT_' || true); do unset "$k"; done
export GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file
echo "GIT_NO_LAZY_FETCH=$GIT_NO_LAZY_FETCH GIT_OPTIONAL_LOCKS=$GIT_OPTIONAL_LOCKS GIT_ALLOW_PROTOCOL=$GIT_ALLOW_PROTOCOL"
echo "residual: $(env | cut -d= -f1 | grep '^GIT_' | sort | tr '\n' ' ')"
echo "=== runtime ==="
/usr/bin/python3 --version
/usr/bin/git --version
/usr/bin/python3 -c "import sys; print('exe=' + sys.executable)"
echo "=== pre: identity/status/pins ==="
/usr/bin/git rev-parse HEAD
/usr/bin/git rev-parse 'HEAD^{tree}'
/usr/bin/git status --porcelain=v1 -uall
/usr/bin/git diff --name-only
/usr/bin/python3 -c "import hashlib,pathlib,os; rels=['schemas/reader-surface-gate-v2.schema.json','schemas/reader-surface-semantic-review-v2.schema.json','scripts/survey_reader_surface_gate_v2.py','schemas/editorial-correction-proposal-v2.schema.json','schemas/longform-publication-source-manifest-v2.schema.json','schemas/longform-reader-input-v2.schema.json','scripts/survey_editorial_correction_proposal_v2.py','scripts/survey_longform_derivation_v2.py','scripts/survey_longform_generated_v2.py','scripts/survey_longform_semantic_publication_v2.py','tests/test_survey_editorial_correction_proposal_v2.py','tests/test_survey_longform_derivation_v2.py','tests/test_survey_longform_publication_integration_v2.py','scripts/survey_editorial_retention_v2.py','schemas/editorial-retention-manifest-v2.schema.json','tests/test_survey_editorial_retention_v2.py']; [print(r, hashlib.sha256(pathlib.Path(r).read_bytes()).hexdigest(), oct(pathlib.Path(r).stat().st_mode & 0o777), pathlib.Path(r).stat().st_size) for r in rels]"
echo "=== unittest (full P2R focused suite) ==="
/usr/bin/python3 -m unittest tests.test_survey_editorial_retention_v2 -v
echo "unittest_rc=$?"
echo "=== -O smoke (weekly positive under optimized mode) ==="
/usr/bin/python3 -O -m unittest tests.test_survey_editorial_retention_v2.EditorialRetentionV2Tests.test_weekly_capture_verify_positive -v
echo "optimized_rc=$?"
echo "=== post: status/pins/caches (no cleanup before comparison) ==="
/usr/bin/git status --porcelain=v1 -uall
/usr/bin/git diff --name-only
/usr/bin/python3 -c "import hashlib,pathlib; rels=['scripts/survey_editorial_retention_v2.py','schemas/editorial-retention-manifest-v2.schema.json','tests/test_survey_editorial_retention_v2.py']; [print(r, hashlib.sha256(pathlib.Path(r).read_bytes()).hexdigest()) for r in rels]"
echo "--- caches ---"
find . -name "__pycache__" -not -path "./.git/*" | head -n 20
echo "RUN_P2R_V1_DONE"
