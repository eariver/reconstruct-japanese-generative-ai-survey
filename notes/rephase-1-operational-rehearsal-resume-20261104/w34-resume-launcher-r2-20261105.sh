#!/usr/bin/env bash
# W34 resume one-use launcher — review only, DO NOT EXECUTE YET.
# Captures argv/cwd/env/timestamps/PID + tool stdout/stderr/exit exclusively.
# No git, no network. Single invocation only; never duplicate. Preserves v1; r2 tool.
set -u
PACKET="notes/rephase-1-operational-rehearsal-resume-20261104"
TOOL="$PACKET/w34-operator-resume-r2-20261105.py"
if [ "${PYTHONDONTWRITEBYTECODE:-unset}" != "1" ]; then
  echo "REFUSE: PYTHONDONTWRITEBYTECODE=1 required" >&2
  exit 2
fi
if env | grep -Eq '^(GIT_DIR|GIT_WORK_TREE|GIT_INDEX_FILE|GIT_OBJECT_DIRECTORY)='; then
  echo "REFUSE: inherited GIT_* overrides present" >&2
  exit 2
fi
echo "argv: $0 $*"
echo "cwd: $(pwd)"
echo "HOME=$HOME"
echo "utc_start=$(date -u +%Y-%m-%dT%H:%M:%SZ) pid=$$"
# Caller must pass: --retention-dir <packet retention> --ready-path <READY.json>
#   --manifest <manifest> --expected-tool-sha <64> --expected-ready-sha <64>
#   --expected-manifest-sha <64> [--repo-root <e84>]
PYTHONDONTWRITEBYTECODE=1 python3 "$TOOL" "$@"
code=$?
echo "utc_end=$(date -u +%Y-%m-%dT%H:%M:%SZ) exit=$code"
exit $code
