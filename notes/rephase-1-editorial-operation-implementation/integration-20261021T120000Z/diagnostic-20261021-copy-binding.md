# Diagnostic copy binding — independent EXACT failing FIX23

No DST edits. Read-only `cp -a` + `stat`/`git` probes only. No clean/reset/commit/network.

## Commands/exits

- `mkdir -p $(dirname $DIAG); cp -a $FIX23 $DIAG` → exit 0
  - SRC `$FIX23=/tmp/opencode/jgas-editorial-smoke-20261021T180000Z/candidate-partial-b40de60`
  - DST `$DIAG=/tmp/opencode/jgas-editorial-diag-20261021T000000Z/candidate-partial-b40de60`
- `git -C $DIAG rev-parse HEAD` → `feb4d1fcd36566653b2dbe58eefc5311daecc7ee` (exit 0, same as FIX23)
- `git -C $DIAG log -1 --format=%H_%ci_%s` → `feb4d1fc... 2026-10-21 16:23:09 +0900 SOURCE snapshot: integrated editorial operation DST 20261021 runtime fix before authority (attempt23)` (exit 0)
- `git -C $DIAG status --short | wc -l` → `10` (exit 0; only authority outputs, same as FIX23 failing state)
- `git -C $DIAG ls-files -s | wc -l` → `759` (exit 0)
- `stat -c "%d:%i %h %n"`:
  - FIX23 pub file → `45:718801 1 .../jgas-editorial-smoke-.../scripts/survey_editorial_publication_v2.py` (exit 0)
  - DIAG pub file → `45:720964 1 .../jgas-editorial-diag-.../scripts/survey_editorial_publication_v2.py` (exit 0)
  - Link counts `1` (no hardlinks); `dev:ino` differ (`718801` vs `720964`) → `INDEPENDENT_OK`
- `stat -c "%d:%i %n" $FIX23/.git/HEAD $DIAG/.git/HEAD` → `45:719160` vs `45:721293` (different inodes, independent DBs) (exit 0)
- `ls -d $FIX23/.git/objects $DIAG/.git/objects` → both exist, separate dirs (exit 0)

## Interpretation

- Independent full DB/worktree copy, no hardlinks (`cp -a` without `--hard-links` creates new inodes; verified link count 1 and distinct `dev:ino`).
- Source identity same (`feb4d1f...` both, same log message/time).
- Worktree is EXACT failing state (post-activated `r1.json` + `publication/` + `sources/` + `surveys/` untracked, 10 status lines), not fresh positive SOURCE (which would have 0 status lines). Preserved for post-activated repeat diagnosis without entire accepted-chain/build rerun.
- No fixture source-file edits; no authority rebind (no new commit, no `git add`, no DST import).
