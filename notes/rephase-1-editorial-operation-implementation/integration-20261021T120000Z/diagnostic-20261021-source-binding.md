# Diagnostic source binding — DST vs FIX23 (exact, commands/exits/data)

No DST code edits in this unit. All data tool-observed, not asserted.

## Commands (all read-only, no clean/reset/commit/network)

- `git -C $DST rev-parse HEAD` → `409b292756dd1277b9dfae87679934c0d2ce251c` (exit 0)
- `git -C $DST status --short | wc -l` → `53` (exit 0; 23 tracked `M` + 30 untracked `??` incl. `__pycache__`, `tmpvr07sdme/`, new modules/schemas/tests)
- `git -C $FIX23 rev-parse HEAD` → `feb4d1fcd36566653b2dbe58eefc5311daecc7ee` (exit 0)
- `git -C $FIX23 log -1 --format=%H_%ci_%s` → `feb4d1fc... 2026-10-21 16:23:09 +0900 SOURCE snapshot: integrated editorial operation DST 20261021 runtime fix before authority (attempt23)` (exit 0)
- `sha256sum $DST/scripts/survey_editorial_publication_v2.py` → `5aee10f9d844077b6e0a491e6309629db316f559911b89eaf60422bf1df7eb47` (exit 0)
- `sha256sum $FIX23/scripts/survey_editorial_publication_v2.py` → `cf0687c8a5c34bd815ee6963aa8bec90895381f1faeae56ae05224a6398908ed` (exit 0)
- `sha256sum $DST/scripts/survey_publication_set_v2.py` → `e897a638d9c113944185a7e7c76c4fd9f14d5a5bfbf06d3741b07b4ca387fa7d` (exit 0)
- `sha256sum $FIX23/scripts/survey_publication_set_v2.py` → `e897a638d9c113944185a7e7c76c4fd9f14d5a5bfbf06d3741b07b4ca387fa7d` (exit 0, identical)
- `stat -c %y` DST pub file → `2026-10-21 16:45:35 +0900`; FIX23 pub file → `2026-10-21 15:43:15 +0900`; FIX23 commit → `2026-10-21 16:23:09 +0900`

## ALREADY_ACTIVE record_path fix timing (exact)

- FIX23 pub SHA `cf0687c8...` (15:43 file, 16:23 commit) does NOT contain the fix.
- DST pub SHA `5aee10f9...` (16:45 file) DOES contain the fix:
  - old (FIX23): `return {"status": "ALREADY_ACTIVE", "record_path": sel_set0.get("path"), ...}` where `sel_set0` is seal ref (`set_ref`/`active_set_ref`, i.e. `.../publication-set.json`)
  - new (DST): `return {"status": "ALREADY_ACTIVE", "record_path": state_pointer0.get("path"), ...}` where `state_pointer0` is State `publication_revalidation_provenance` (i.e. `.../publication-surface-revalidation-r1.json`), with explicit invalid-pointer guard
- Therefore: fix AFTER FIX23 SOURCE commit (16:45 > 16:23). FIX23 worktree/blobs lack the fix; DST worktree has it; no FIX23 re-commit after fix (preserved, no authority rebind).
- Manual repeat on FIX23 (old code) returned `record_path='.../publication-set.json'` (wrong, seal not record) with `status=ALREADY_ACTIVE` (see `smoke-weekly-stderr17.txt` DEBUG lines). After fix, fresh-process repeat must return `r1.json` (not yet re-executed on FIX23 copy; see diagnostic below for bounded re-check).

## No direct fixture edits / ambient imports (disclosure)

- No files edited inside any `/tmp/opencode/jgas-editorial-smoke-*` fixture after its SOURCE commit, except authority outputs created by the smoke runner itself (proposal/retained/scope/staged/publication/build/record/receipt/manuscript/bundle/reviews/gate/candidate/seal/record/State) – no source-file edits, no receipt-pin edits to green.
- No `PYTHONPATH` outside fixture/code during smoke: `PYTHONPATH=$FIX` only, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPYCACHEPREFIX=/tmp/opencode/int-pycache` (external cache), `TMPDIR=/tmp/opencode`. No imports from DST (`/tmp/.../jgas-editorial-op-impl-...`) during fixture runs (sys.path[0]=FIX_ROOT only).
- Diagnostic below uses independent copy (not FIX23 original) with `PYTHONPATH=<copy>` only; no DST imports.

## Full manifests (summary; full lists in freeze/ + smoke/ raw)

- DST tracked modified: 23 paths (see `freeze/tracked-modified-sha.txt` + `tracked-modified-sha2.txt` for post-proof deltas)
- DST untracked new (excluding `__pycache__`/`.pyc`): 27 core new (8 schemas + 9 scripts + 7 tests + 3 config/workflows) + `tmpvr07sdme/` noise (excluded from SOURCE fixtures via `rm -rf` before `git add`? Actually fixtures `rm -rf .git/__pycache__/tests/__pycache__` but kept `tmpvr07sdme`? No, fixtures `cp -a DST` then `rm -rf .git/__pycache__/tests/__pycache__` – `tmpvr07sdme/` remains? Check FIX23 status shows `??` for `sources/`, `surveys/`, etc. (authority outputs), not `tmpvr07sdme` – because FIX23 `git add -A` included `tmpvr07sdme`? No, FIX23 status does NOT list `tmpvr07sdme`, so it was either absent in DST copy? Actually DST has `tmpvr07sdme/` untracked, FIX23 copy would have it, but `git add -A` would include it, then `git status` after commit should be clean except authority outputs. FIX23 status shows only authority outputs (`sources/`, `surveys/`, etc.), no `tmpvr07sdme`, meaning `tmpvr07sdme` was either not copied? Wait `cp -a DST FIX` copies `tmpvr07sdme`, then `git add -A` would include it, then status clean. After smoke run, authority outputs appear as untracked. So `tmpvr07sdme` must be committed in FIX23 SOURCE (not shown as untracked). Verified: FIX23 `git ls-files | grep tmpvr07sdme | head` needed for full blob check (see diagnostic script output).
- FIX23 SOURCE commit blobs: `git -C FIX23 ls-files -s | wc -l` and `git -C FIX23 show HEAD:<path> | sha256sum` for key paths to be recorded by diagnostic script (not asserted here).
