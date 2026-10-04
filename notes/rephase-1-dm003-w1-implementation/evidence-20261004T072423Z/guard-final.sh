#!/usr/bin/env bash
# Post-commit guard for DM003-W1 final runs. Expects committed successor
# e1705b7 (parent 222a37e), fully clean tree, pinned source hashes.
set -u
LABEL="$1"
cd /tmp/opencode/jgas-dm003w1-impl-20261004T072423Z || exit 1
export GIT_NO_LAZY_FETCH=1 GIT_ALLOW_PROTOCOL=file GIT_OPTIONAL_LOCKS=0
HEAD="$(git rev-parse HEAD)"
TREE="$(git rev-parse HEAD^{tree})"
PARENT="$(git log --format='%P' -1 HEAD)"
STATUS="$(git status --porcelain=v1 --untracked-files=all)"
FAIL=0
[ "$HEAD" = "e1705b7fed01369767ab9d827c0360117d54aa1f" ] || { echo "GUARD $LABEL: HEAD drift: $HEAD"; FAIL=1; }
[ "$TREE" = "3d21322587b9e4d3d05d7ae9ef66fbd1d74d3557" ] || { echo "GUARD $LABEL: tree drift: $TREE"; FAIL=1; }
[ "$PARENT" = "222a37e9ee2aa96724a491f2c04c2583a86b9650" ] || { echo "GUARD $LABEL: parent drift: $PARENT"; FAIL=1; }
[ -z "$STATUS" ] || { echo "GUARD $LABEL: expected fully clean, got:"; echo "$STATUS"; FAIL=1; }
[ "$(sha256sum scripts/survey_agent_control_v2.py | cut -d' ' -f1)" = "7974551f870eb78ca38be815bdca8d97bca7e7445b81cc9e2f2d1e8b03e1f416" ] || { echo "GUARD $LABEL: control sha drift"; FAIL=1; }
[ "$(sha256sum scripts/survey_profiled_freeze_v2.py | cut -d' ' -f1)" = "092f1a2db8a728684cd2c5bcee80d8ef01e5353091cc03e732e5fc5b10a07c05" ] || { echo "GUARD $LABEL: profiled sha drift"; FAIL=1; }
[ "$(sha256sum scripts/survey_stage_validation_v2.py | cut -d' ' -f1)" = "0f2393dadab72cecba5672b945d2be35e41089e4face5f0e2753b84a6a4b5806" ] || { echo "GUARD $LABEL: stage sha drift"; FAIL=1; }
[ "$(sha256sum tests/test_survey_dm003_w1_preview_agreement_v2.py | cut -d' ' -f1)" = "ae42b94a3bad1407207d87a0a2472d109c6cdcd02e2773609699ddf8ce3d366a" ] || { echo "GUARD $LABEL: newtest sha drift"; FAIL=1; }
[ "$(sha256sum tests/test_survey_dm001_019_freeze_equivalence_v2.py | cut -d' ' -f1)" = "7d4d0004aab8e190dcc79bb3916e4ff4c4abc5d500799c4c564098924ec574b9" ] || { echo "GUARD $LABEL: dm001 sha drift"; FAIL=1; }
if [ "$FAIL" = "0" ]; then echo "GUARD $LABEL: OK head=$HEAD"; else echo "GUARD $LABEL: FAIL"; exit 1; fi
