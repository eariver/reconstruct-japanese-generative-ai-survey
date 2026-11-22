# Real Selection validation — prior-reader fix (report-only, SP PASS / W34 timeout)

Root: `../astra-repair-resolution.md` §3. Source commit + bounded real validation authorized.

## Source commit (author DB, no reconstruct write)

Author: `.rephase-1-editorial-runtime/prior-artifact-reader-implementation-20261122T062101Z/candidate-work`
- Before: `d591` parent `ae0` tree `ff01`, 774 intended vs frozen manifest `0dc3…` 0 mismatch (other773 unchanged).
- Staged exact 2: `scripts/survey_stage_validation_v2.py` `51927B 1e4c818b…` + `tests/test_prior_artifact_reader_repair_v2.py` `30019B 1fb83167…`, both `0o664`, normal hooks, `Prior artifact reader repair <prior-artifact-reader@example.invalid>`, no empty/amend/bypass/config/HOME.
- New child: `e59fa9bc5f323a640fd922412de7757e60eb5944`, parent `d591`, tree `e5e888cbb285dc32c60b422a41b24acc044378e6`, body 390B, SHA1(`commit 390\0`+body) recompute match True.
- 775 committed blobs/modes vs worktree: 773 unchanged 0 mismatch + changed/new match True. No `f591` copy (history preserved only). Full `rev-parse/log10/scoped diff` inspected isolated-only; full `diff --stat` unusable due to partial DB missing blob (STOP rule respected, scoped diff used).

## Real copy (independent, no shared objects)

`.rephase-1-editorial-runtime/prior-artifact-reader-real-20261122T065145Z/candidate-work` (`cp -a` author, no hardlinks — inodes differ, no alternates/commondir, inert origin unchanged, no set-url, caches excluded, old author/source/real/proof/shadow preserved).
- HEAD `e59…`, parent `d591`, tree `e5e8…`. 775 spot OK, States `EVIDENCE_REVIEWED` init `48082356` (`W34 a858…`, `SP 38a634…`), research own `cc1c/ae0` lineage preserved, 14 outputs match R2 (spot-checked 7 + States), guards absent, report targets absent pre-run, no writer/regeneration/adopt/State edit.

## Launcher (operation evidence, not shipping source)

`launcher-prior-reader-validation.py` stdlib-only (`faulthandler/runpy/sys/pathlib`): `dump_traceback_later(300,repeat)` to separate `raw/<ED>/stack-trace.txt`, then `runpy.run_module(scripts.survey_stage_validation_v2)` with exact normal CLI argv. v1 failed import (`scripts` not on path, preserved in `raw/SP-harness-import-failure-20261122T065315Z/` exit 1); v2 adds repo-root to `sys.path` (mirrors `python -m`, no project mock/wrap/fake proof/checked context/source patch). Recorded as launcher v2 used for both editions.

Common argv: `--repo-root <abs-R> --config config/survey-production-v2.json --state sources/<issue>/production-state.json --artifact candidate-matrix=… --artifact candidate-selection=… --output sources/<issue>/orchestration/v2/stage-validation/prior-reader-selection-r1.json --recorded-at <UTC>`. `PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1…`, scrubbed `GIT_*`, explicit cwd `R`, unique PIDs reaped via `wait`, no `timeout` command (tool bound 1250s).

## SP — PASS (report-only, no advance)

- `06:53:45Z–07:07:45Z` UTC, wall ~840s, child PID 1528119, exit 0, stdout report path, stderr empty, `stack-trace.txt` 10822B (dumps, run >300s), State pre/post `38a…` unchanged.
- Report `prior-reader-selection-r1.json` 1704B `e4245513…`: 12 keys (`schema_version/check_id/status/issue_id/from_state/to_state/production_state/production_profile/implementation_commit_sha/contract/artifacts/recorded_at`), `CORE_STAGE_CONTRACT PASS`, `EVIDENCE_REVIEWED→SELECTION_COMPLETE`, `issue SP-efficient-llm-2026`, `impl e59…` (current HEAD, no fake old impl), `production_state 38a…`, `production_profile aff0…`, contract 8 keys, artifacts matrix `2f62…`/selection `4e68…` pins. No reviews/checkpoint/advance.

## W34 — timeout (>1200s bound, STOP, no retry)

- `07:08:03Z–07:28:53Z` UTC (tool 1250s kill), child PID 1529795 reaped, exit 124, stdout/stderr 0B, `stack-trace.txt` 11463B, report absent, State `a858…` unchanged.
- Stack phase (faulthandler, 5-min repeats): `_prior_artifacts` refusal GONE (no `from_state` error); stuck in full semantics `_evidence_basis→_selection_basis→_validate_stage_semantics`: `_verify_adopted_graph_full→check_supersession…→_validate_prearchitecture_core_proof→_validate_checkpoint_record` + `_recheck_phase_pins/_recheck_supplement_context/_supplement_source_file` (supplement Raw per task, 409 W34 transitive reloads). Precise cost question preserved, not bypassed. SP reaped and W34 pre unchanged, so W34 run was lawful single attempt. No repair/retry/extend, no State/artifact mutation except intentional guard none.

## Result

Fix verified on real SP normal path; W34 full-semantics cost exceeds 1200s bound (UNKNOWN remains, now bounded below by >1200s for W34 Selection). No real writer/regeneration/adopt/State edit/HumanGate/R4/PDF/Production, no ordinary Commit/Push. Stop, no auto next. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN.
