#!/bin/bash
# R1 oracle final TEST-ONLY snapshot + 2-method run (no whole PASS, no CommitPoint).
# Bounded: test-only edit already applied in SRC candidate-work; no runtime edits here.
# NEW independent complete-source snapshot (all 741 intended, not git ls-files-only),
# source-only meaningful fixture commit before authorities, workspace TMPDIR,
# no network/old runners/cleanup/candidate-or-reconstruct commit, no shared execution.
set -u
export LC_ALL=C
export PYTHONDONTWRITEBYTECODE=1
export GIT_NO_LAZY_FETCH=1
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL=/dev/null
export GIT_OPTIONAL_LOCKS=0
RECON="/home/eariver/git/reconstruct-japanese-generative-ai-survey"
SRC="$RECON/.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work"
DST_BASE="$RECON/.rephase-1-editorial-runtime/versioned-renewal-r1-oracle-final-20261025T191500Z"
DST="$DST_BASE/snapshot-work"
TMPWS="$DST_BASE/tmp"
EVID="$RECON/notes/rephase-1-versioned-renewal-implementation/resume-20261025/r1-oracle-final"
LOG="$EVID/commands.log"
: > "$LOG"
run() {
  name="$1"; shift
  printf "run %s rc=" "$name" >> "$LOG"
  "$@" >"$EVID/$name-stdout.txt" 2>"$EVID/$name-stderr.txt"
  rc=$?
  printf "%s cmd=" "$rc" >> "$LOG"
  printf "%s " "$@" >> "$LOG"
  printf "\n" >> "$LOG"
  echo "$rc" > "$EVID/$name-exit.txt"
  return $rc
}
run recon-head git --no-optional-locks -C "$RECON" rev-parse HEAD
run recon-status git --no-optional-locks -C "$RECON" status --porcelain=v1 --untracked-files=all
run recon-diff-cached git --no-optional-locks -C "$RECON" diff --cached --name-only
run src-head git --no-optional-locks -C "$SRC" rev-parse HEAD
run src-tree git --no-optional-locks -C "$SRC" rev-parse 'HEAD^{tree}'
run src-test-sha sha256sum "$SRC/tests/test_survey_weekly_mechanical_refresh_v2.py"
run src-latexmkrc-sha sha256sum "$SRC/.latexmkrc"
run src-count bash -c "find \"$SRC\" -path \"$SRC/.git\" -prune -o -type f -print | grep -v '__pycache__' | grep -v '\.pyc$' | wc -l"
run src-status git --no-optional-locks -C "$SRC" status --porcelain=v1 --untracked-files=all
run src-diff-names git --no-optional-locks -C "$SRC" diff HEAD --name-only
run src-remote git --no-optional-locks -C "$SRC" remote -v
run mkdir-dst mkdir -p "$DST" "$TMPWS"
run cp-git cp -a "$SRC/.git" "$DST/.git"
run dst-head git --no-optional-locks -C "$DST" rev-parse HEAD
run dst-gitdir git --no-optional-locks -C "$DST" rev-parse --absolute-git-dir
run dst-remote git --no-optional-locks -C "$DST" remote -v
run dst-noalternates bash -c "test ! -e \"$DST/.git/objects/info/alternates\" && test ! -e \"$DST/.git/objects/info\" && echo NO_ALTERNATES_OK"
run env-check bash -c "env | grep -E '^GIT_(DIR|WORK_TREE|INDEX_FILE)=' && exit 1 || echo NO_GIT_OVERRIDE_OK"
run populate-worktree /usr/bin/python3 "$EVID/populate_snapshot_20261025T191500Z.py" "$SRC" "$DST"
run dst-count bash -c "find \"$DST\" -path \"$DST/.git\" -prune -o -type f -print | grep -v '__pycache__' | grep -v '\.pyc$' | wc -l"
run dst-test-sha sha256sum "$DST/tests/test_survey_weekly_mechanical_refresh_v2.py"
run dst-latexmkrc-sha sha256sum "$DST/.latexmkrc"
run dst-latexmkrc-cmp cmp "$SRC/.latexmkrc" "$DST/.latexmkrc"
run dst-test-cmp cmp "$SRC/tests/test_survey_weekly_mechanical_refresh_v2.py" "$DST/tests/test_survey_weekly_mechanical_refresh_v2.py"
run dst-status git --no-optional-locks -C "$DST" status --porcelain=v1 --untracked-files=all
run dst-diff-names git --no-optional-locks -C "$DST" diff HEAD --name-only
run dst-isolation /usr/bin/python3 -c "import pathlib,os; dst=pathlib.Path('$DST'); src=pathlib.Path('$SRC'); d_git=list((dst/'.git').rglob('*')); s_git=list((src/'.git').rglob('*')); print('DST_GIT_FILES', len([p for p in d_git if p.is_file()])); print('SRC_GIT_FILES', len([p for p in s_git if p.is_file()])); bad=[str(p) for p in dst.rglob('*') if p.is_file() and os.lstat(p).st_nlink!=1 and '.git/' not in str(p)]; print('NLink_BAD', len(bad)); assert not bad, bad[:3]"
# Source-only meaningful fixture commit BEFORE authorities (test-only file, real bytes, not --allow-empty).
run dst-add git --no-optional-locks -C "$DST" add -- tests/test_survey_weekly_mechanical_refresh_v2.py
run dst-commit env GIT_AUTHOR_NAME=Synthetic-R1-Oracle-Final GIT_AUTHOR_EMAIL=synthetic-r1-oracle-final@example.invalid GIT_COMMITTER_NAME=Synthetic-R1-Oracle-Final GIT_COMMITTER_EMAIL=synthetic-r1-oracle-final@example.invalid git --no-optional-locks -C "$DST" commit -q -m "R1 oracle final TEST-ONLY tightened pointer (missing-r9.json cause, 741 intended preserved)"
run dst-head-post git --no-optional-locks -C "$DST" rev-parse HEAD
run dst-log-post git --no-optional-locks -C "$DST" log --oneline -3
run dst-status-post git --no-optional-locks -C "$DST" status --porcelain=v1 --untracked-files=all
run dst-show-stat git --no-optional-locks -C "$DST" show --stat --oneline HEAD
echo "DONE SNAPSHOT+COMMIT rc=0"
