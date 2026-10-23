# R7b closeout — DM004 7/7 inherited resolution (internal unit, not Human Commit Point)

R7 runtime fixes accepted pending evidence. This unit resolves the inherited DM004 4/7 with NO runtime code change (runtime AST/functions byte-identical to R7 except the test file) and no blocker waiver. Failed-7 raw preserved (`r7-dm004-stderr.txt`, 3 failures).

## Environment fix (test subprocess only)

Exact extracted workflow line uses bare `python`, which is absent locally (`python: command not found`; local is `python3` 3.14.4, workflow pins 3.12 — qualification gap recorded, not repaired). Created process-scoped owned launcher symlink `.rephase-1-editorial-runtime/bin/python -> /usr/bin/python3` (target SHA256 `52e0a13e...`, launcher reports 3.14.4). Prepended to PATH ONLY inside DM004 test subprocess env (`offline_env`); no system/global install/config, workflow line NOT edited. Pins in `r7b-dm004-env-pins.json`.

## Test-only oracle adaptation (business contract unchanged)

Missing-record case previously expected `Stage Checkpoint artifact drift: release-record`; the strict path guard now fails closed earlier with controlled exit 2 and diagnostic `checkpoint artifact release-record missing: ...` (plus `Production State invalid`, no data write). Updated the single expected string to that EXACT diagnostic — narrow, not a blanket accept (NameError or any other message still fails: exit must be 2 with `Production State invalid`). Precondition (renamed-away canonical `release-record-v2.json`, asserted absent before CLI) and no-write checks unchanged. Old test/source raw archived (`test_survey_dm004_release_validate_state_v2.py.pre-r7b`, R7 manifest pins) before edit; edit via dedicated editor in DST test only.

## Runs: 7/7 in two code-bound isolated clones

Fresh `cp -a` clones of DST (with test update) under workspace-ignored `final-r7-dm004/dm004-clone-{a,b}`: own GitDir verified NOT reconstruct, inert origin, no alternates, no inode sharing (dev:ino distinct across DST/A/B). Full raw + numeric exit saved (`r7b-dm004-clone{A,B}-{stdout,stderr,exit}.txt`): both exit 0, `Ran 7 tests ... OK`, 0 skipped. Pre/post `git status` identical (25M/35??), no residue (fixtures cleaned, escape/sibling dirs removed, closure script removed). No tests executed inside frozen SOURCE images.

## Frozen final source (NEW unique snapshot, not R6/R7 path)

`.rephase-1-editorial-runtime/jgas-editorial-r7b-20261023T034500Z/candidate-partial-b40de60` — `cp -a` of R7 snapshot + test-only file, independent inodes, own GitDir NOT parent, inert origin, no alternates/sharing. Meaningful SOURCE fixture commit allowed (`worker-r7b`): HEAD `721a04d85532d7855f3e54cc411f5847c787726e`, tree `ac7cb0bd2e977b46e957450816eddd779799e144`, 721 files (recomputed actual), status only `?? scripts/__pycache__/` (no caches/tmp/evidence committed). Manifest `source-manifest-r7b.json` valid JSON (HEAD/tree40, 721 entries with path/SHA256/bytes/mode). Full SHA comparison R7 vs R7b: exactly one differing file (the DM004 test); all runtime files byte-identical.

DST working-tree delta actual: 25 modified tracked + 35 untracked = 60 entries vs HEAD 409b292 (prompt float cited 55/56; actual counted 60). Ordinary DST/reconstruct commits NOT done (Human-owned).

Return for packaging + independent review: final root/HEAD/pins above; runtime unchanged from R7 except test; no automatic R6 PASS transfer. No next Human Commit Point until root closes unit.
