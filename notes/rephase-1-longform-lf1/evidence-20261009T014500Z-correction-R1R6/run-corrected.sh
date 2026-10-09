#!/bin/bash
# LF-1 correction fail-closed runner (R1). Does NOT reuse old run-focused.sh.
# Usage: bash run-corrected.sh <raw-log-path> [unittest-args...]
# Fail-closed: absent-log-only, pinned HEAD/tree/overlay hashes/paths, exact
# three-path predicate, all Git overrides checked, interpreter/version/cwd/argv/
# env recorded, file-protocol-only runtime, pre+finally-post guards with child
# exit propagation (no masking), exclusive log.
set -u
DST="/tmp/opencode/jgas-lf1-design-20261009T001653Z"
EXPECTED_HEAD="409b292756dd1277b9dfae87679934c0d2ce251c"
EXPECTED_TREE="8ce3699861505f32d1d60bdc185d4d4f635aedb2"
EXPECTED_MOD="abd50864e5065d7d69a6c3ccc13d01915be4654aee4aedeac1eb60f9aa33987f"
EXPECTED_SCHEMA="71156a53b776a82928519b0a3f821cf40bd4279550e0bc4973c7ed27394e588b"
EXPECTED_TEST="d4ab5361c7741d10dbe5986bf1f62b85a21646a8e220641469e6395389ba2ca6"
# Allow proof-only DST override (proof logs disclose this); real runs use pinned DST.
if [ -n "${DST_OVERRIDE:-}" ]; then
  DST="$DST_OVERRIDE"
fi
LOG="${1:-}"
if [ -z "$LOG" ]; then
  echo "REFUSE: missing log path" >&2
  exit 2
fi
shift || true
if [ -e "$LOG" ]; then
  echo "REFUSE: log path already exists (absent-log-only): $LOG" >&2
  exit 2
fi
# Proof-only expected-head override (disclosed; real runs never set it).
if [ -n "${PIN_OVERRIDE_FOR_PROOF:-}" ]; then
  EXPECTED_HEAD="$PIN_OVERRIDE_FOR_PROOF"
fi
export GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file
export PYTHONDONTWRITEBYTECODE=1
# Pre-guard: all Git root overrides must be absent (module's 6 vars).
for v in GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_COMMON_DIR; do
  if [ -n "${!v:-}" ]; then
    echo "REFUSE: unsafe inherited Git root override: $v=${!v}" >&2
    exit 2
  fi
done
# Pre-guard: pinned source identity before child execution.
ACT_HEAD="$(git -C "$DST" rev-parse HEAD 2>&1)" || { echo "REFUSE: cannot rev-parse HEAD: $ACT_HEAD" >&2; exit 2; }
if [ "$ACT_HEAD" != "$EXPECTED_HEAD" ]; then
  echo "REFUSE: HEAD mismatch: actual=$ACT_HEAD expected=$EXPECTED_HEAD (child not executed)" >&2
  exit 2
fi
ACT_TREE="$(git -C "$DST" rev-parse 'HEAD^{tree}' 2>&1)" || { echo "REFUSE: cannot rev-parse tree: $ACT_TREE" >&2; exit 2; }
if [ "$ACT_TREE" != "$EXPECTED_TREE" ]; then
  echo "REFUSE: tree mismatch: actual=$ACT_TREE expected=$EXPECTED_TREE (child not executed)" >&2
  exit 2
fi
# Exact three-path predicate: only the intended new files, zero tracked mods.
STATUS="$(git -C "$DST" status --porcelain=v1 --untracked-files=all 2>&1)" || { echo "REFUSE: status failed: $STATUS" >&2; exit 2; }
EXPECTED_STATUS="?? schemas/longform-reader-input-v2.schema.json
?? scripts/survey_longform_derivation_v2.py
?? tests/test_survey_longform_derivation_v2.py"
if [ "$STATUS" != "$EXPECTED_STATUS" ]; then
  echo "REFUSE: status predicate failed (child not executed). Actual:" >&2
  echo "$STATUS" >&2
  exit 2
fi
TRACKED="$(git -C "$DST" diff --name-only HEAD 2>&1)" || { echo "REFUSE: diff failed: $TRACKED" >&2; exit 2; }
if [ -n "$TRACKED" ]; then
  echo "REFUSE: tracked modifications present (child not executed): $TRACKED" >&2
  exit 2
fi
ACT_MOD="$(sha256sum "$DST/scripts/survey_longform_derivation_v2.py" | awk '{print $1}')"
ACT_SCHEMA="$(sha256sum "$DST/schemas/longform-reader-input-v2.schema.json" | awk '{print $1}')"
ACT_TEST="$(sha256sum "$DST/tests/test_survey_longform_derivation_v2.py" | awk '{print $1}')"
if [ "$ACT_MOD" != "$EXPECTED_MOD" ] || [ "$ACT_SCHEMA" != "$EXPECTED_SCHEMA" ] || [ "$ACT_TEST" != "$EXPECTED_TEST" ]; then
  echo "REFUSE: overlay hash mismatch (child not executed): mod=$ACT_MOD schema=$ACT_SCHEMA test=$ACT_TEST" >&2
  exit 2
fi
# Record actual interpreter/version/env/cwd/argv + runtime protocol.
# Resolve LOG to absolute before cd to the pinned copy (exclusive log stays
# outside the candidate source).
CALLER_CWD="$(pwd)"
case "$LOG" in
  /*) ABS_LOG="$LOG" ;;
  *) ABS_LOG="$CALLER_CWD/$LOG" ;;
esac
{
  echo "=== PRE identity (pinned) ==="
  echo "dst=$DST"
  echo "expected_head=$EXPECTED_HEAD actual_head=$ACT_HEAD"
  echo "expected_tree=$EXPECTED_TREE actual_tree=$ACT_TREE"
  echo "expected_mod=$EXPECTED_MOD actual_mod=$ACT_MOD"
  echo "expected_schema=$EXPECTED_SCHEMA actual_schema=$ACT_SCHEMA"
  echo "expected_test=$EXPECTED_TEST actual_test=$ACT_TEST"
  echo "--- status ---"
  echo "$STATUS"
  echo "--- tracked diff (must be empty) ---"
  echo "[$TRACKED]"
  echo "=== runtime ==="
  echo "interpreter=$(command -v python3)"
  python3 --version
  echo "caller_cwd=$CALLER_CWD"
  echo "child_cwd=$DST (child runs from pinned copy)"
  echo "argv: python3 -m unittest $*"
  echo "--- env (filtered) ---"
  env | grep -E '^(GIT_|PYTHON|PATH|PWD|LANG|LC_)' | sort || true
  echo "git_remote_inert=$(git -C "$DST" remote -v 2>&1 | head -n 5)"
  echo "git_allow_protocol=$GIT_ALLOW_PROTOCOL git_no_lazy_fetch=$GIT_NO_LAZY_FETCH"
  echo "date_utc=$(date -u +%Y%m%dT%H%M%SZ)"
  echo "=== RUN (child from pinned copy) ==="
} > "$ABS_LOG" 2>&1
# Run child from pinned copy, retain numeric exit, finally postguard without masking.
set +e
cd "$DST"
python3 -m unittest "$@" >> "$ABS_LOG" 2>&1
CHILD_EXIT=$?
set -e
{
  echo "unittest_exit:$CHILD_EXIT"
  echo "=== POST guard (finally, child exit preserved) ==="
  echo "post_head=$(git -C "$DST" rev-parse HEAD 2>&1)"
  echo "post_tree=$(git -C "$DST" rev-parse 'HEAD^{tree}' 2>&1)"
  echo "--- post status ---"
  git -C "$DST" status --porcelain=v1 --untracked-files=all 2>&1
  echo "--- post tracked diff (must be empty) ---"
  git -C "$DST" diff --name-only HEAD 2>&1
  echo "post_diff_exit:$?"
  echo "--- post overlay hashes ---"
  sha256sum "$DST/scripts/survey_longform_derivation_v2.py" "$DST/schemas/longform-reader-input-v2.schema.json" "$DST/tests/test_survey_longform_derivation_v2.py" 2>&1
  echo "sha_exit:$?"
  if [ "$CHILD_EXIT" -ne 0 ]; then
    echo "CHILD_FAILED exit=$CHILD_EXIT (propagated, not masked)"
  else
    echo "CHILD_PASSED exit=0"
  fi
  echo "DONE"
} >> "$ABS_LOG" 2>&1
echo "RUNNER_DONE log=$ABS_LOG child_exit=$CHILD_EXIT"
exit $CHILD_EXIT
