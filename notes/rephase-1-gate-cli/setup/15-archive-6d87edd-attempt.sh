#!/usr/bin/env bash
# Archive the immutable 6d87edd antecedent (manifest/patch/changed-files/report/raw log)
# under attempts/6d87edd/ BEFORE packaging the corrected test-only successor.
set -euo pipefail
P=/mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-gate-cli
cd "$P"
mkdir -p attempts/6d87edd
mv candidate.json increment-gate-cli.patch changed-files implementation-report.md attempts/6d87edd/
mv logs/candidate-relevant-tests-6d87edd.log attempts/6d87edd/
mv logs/candidate-relevant-tests-6d87edd.exit attempts/6d87edd/

cat > attempts/6d87edd/README.md <<'EOF'
# Antecedent attempt: 6d87edd (superseded tests; runtime unchanged)

- Successor head `6d87edd28a1be8893ca2ab67fed6e32e54b0de6c`, tree `777c65e9e51fa5c31953808520ee00db65514d03`, parent B `c04f32a`.
- Runtime change to `scripts/survey_reader_surface_gate_v2.py` is IDENTICAL in the later
  test-only successor; only `tests/test_survey_gate_cli_persisted_review_v2.py` changed.
- Archived here immutably because root review found test/evidence corrections
  (unrelated-manuscript negative, findings transport, wrong-target assertion, evidence
  counting/oracle breadth, repro hygiene).
- `candidate-relevant-tests-6d87edd.log` / `.exit`: 32 test methods, OK, exit 0 (antecedent).
- `changed-files/` and `increment-gate-cli.patch` are B-to-6d87edd.
EOF
echo "ARCHIVED"
find attempts/6d87edd -type f | sort
