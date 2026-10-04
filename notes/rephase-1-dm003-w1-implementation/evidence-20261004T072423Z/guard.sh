#!/usr/bin/env bash
# Per-run source/candidate guard for DM003-W1 runs. Asserts exact HEAD/tree/
# parent, tracked-clean (allowing only expected untracked paths pre-commit),
# and pinned source hashes. Aborts (exit 1) on any drift.
# Usage: guard.sh <label> <mode:pre-commit|post-commit> <expected_control_sha>
set -u
LABEL="$1"
MODE="$2"
EXPECTED_CONTROL="$3"
cd /tmp/opencode/jgas-dm003w1-impl-20261004T072423Z || exit 1
export GIT_NO_LAZY_FETCH=1 GIT_ALLOW_PROTOCOL=file GIT_OPTIONAL_LOCKS=0
HEAD="$(git rev-parse HEAD)"
TREE="$(git rev-parse HEAD^{tree})"
PARENT="$(git log --format='%P' -1 HEAD)"
STATUS="$(git status --porcelain=v1 --untracked-files=all)"
CONTROL_SHA="$(sha256sum scripts/survey_agent_control_v2.py | cut -d' ' -f1)"
PROFILED_SHA="$(sha256sum scripts/survey_profiled_freeze_v2.py | cut -d' ' -f1)"
STAGE_SHA="$(sha256sum scripts/survey_stage_validation_v2.py | cut -d' ' -f1)"
FAIL=0
[ "$HEAD" = "222a37e9ee2aa96724a491f2c04c2583a86b9650" ] || { echo "GUARD $LABEL: HEAD drift: $HEAD"; FAIL=1; }
[ "$TREE" = "dbabeed5e70d79b51abb09b64666ca9e1d0fd5dd" ] || { echo "GUARD $LABEL: tree drift: $TREE"; FAIL=1; }
[ "$PARENT" = "ff6c67f68e12b3093901248219f2de2872e54d73" ] || { echo "GUARD $LABEL: parent drift: $PARENT"; FAIL=1; }
[ "$CONTROL_SHA" = "$EXPECTED_CONTROL" ] || { echo "GUARD $LABEL: control sha drift: $CONTROL_SHA"; FAIL=1; }
[ "$PROFILED_SHA" = "092f1a2db8a728684cd2c5bcee80d8ef01e5353091cc03e732e5fc5b10a07c05" ] || { echo "GUARD $LABEL: profiled sha drift"; FAIL=1; }
[ "$STAGE_SHA" = "0f2393dadab72cecba5672b945d2be35e41089e4face5f0e2753b84a6a4b5806" ] || { echo "GUARD $LABEL: stage sha drift"; FAIL=1; }
if [ "$MODE" = "post-commit" ]; then
  [ -z "$STATUS" ] || { echo "GUARD $LABEL: expected fully clean, got:"; echo "$STATUS"; FAIL=1; }
else
  # Pre-commit: allow exactly the intended W1 paths, nothing else.
  # Stage 1 (before DM001 oracle update): two paths; stage 2: three paths.
  EXPECTED_STATUS=" M scripts/survey_agent_control_v2.py
?? tests/test_survey_dm003_w1_preview_agreement_v2.py"
  EXPECTED_STATUS2=" M scripts/survey_agent_control_v2.py
 M tests/test_survey_dm001_019_freeze_equivalence_v2.py
?? tests/test_survey_dm003_w1_preview_agreement_v2.py"
  if [ "$STATUS" != "$EXPECTED_STATUS" ] && [ "$STATUS" != "$EXPECTED_STATUS2" ]; then
    echo "GUARD $LABEL: unexpected status:"; echo "$STATUS"; FAIL=1;
  fi
fi
if [ "$FAIL" = "0" ]; then
  echo "GUARD $LABEL: OK head=$HEAD control=$CONTROL_SHA mode=$MODE"
else
  echo "GUARD $LABEL: FAIL"; echo "$STATUS"
  exit 1
fi
