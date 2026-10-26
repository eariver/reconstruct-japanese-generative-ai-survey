#!/bin/bash
# Unit transitive tests — behavioral, FD-safe, 1200s bound, PID logs
set -u
REPO=/home/eariver/git/reconstruct-japanese-generative-ai-survey
FIX=$REPO/.rephase-1-editorial-runtime/versioned-renewal-freeze-transitive-20261025T120000Z/renewal-weekly
EVID=$REPO/notes/rephase-1-versioned-renewal-implementation/resume-20261025/freeze-transitive-correction/unit-20261025T124500Z
mkdir -p "$EVID"
exec > "$EVID/commands.log" 2>&1
echo "FIX $FIX HEAD $(git -C $FIX rev-parse HEAD)"
echo "PUB $(sha256sum $FIX/scripts/survey_publication_v2.py | cut -d' ' -f1)"
run() { desc="$1"; shift; echo "\$ $* # $desc"; "$@" > "$EVID/$desc-stdout.txt" 2> "$EVID/$desc-stderr.txt"; ec=$?; echo $ec > "$EVID/$desc-exit.txt"; echo "-> exit=$ec"; return $ec; }
export RENEWAL_TEST_REPO=$FIX
export PYTHONDONTWRITEBYTECODE=1
run unit-transitive /usr/bin/python3 -c "import sys; sys.path.insert(0, '$FIX/tests'); import test_versioned_renewal_freeze_transitive_correction_20261025 as t; t.test_shared_wrapper_grouping_real_files(); print('PASS shared')"
run unit-task-conv /usr/bin/python3 -c "import sys; sys.path.insert(0, '$FIX/tests'); import test_versioned_renewal_freeze_transitive_correction_20261025 as t; t.test_evidence_task_path_convention(); t.test_screening_batch_path_convention(); print('PASS conventions')"
run unit-preflight /usr/bin/python3 -c "import sys, os; os.environ['RENEWAL_TEST_REPO']='$FIX'; sys.path.insert(0, '$FIX/tests'); import test_versioned_renewal_freeze_transitive_correction_20261025 as t; t.test_preflight_overlap_with_typed_refs(); t.test_fd_safe_read_refuses_symlink_ancestor(); print('PASS fd')"
run unit-nowalker /usr/bin/python3 -c "import sys, os; os.environ['RENEWAL_TEST_REPO']='$FIX'; sys.path.insert(0, '$FIX/tests'); import test_versioned_renewal_freeze_transitive_correction_20261025 as t; t.test_no_generic_walker_in_pub(); print('PASS nowalker')"
echo "UNIT_DONE"
