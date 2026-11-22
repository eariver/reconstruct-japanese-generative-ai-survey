# Independent scoped SOURCE/TEST review — prior-artifact reader implementation

Role: fresh independent scoped reviewer, not author/root. Read-only, no Git/imports/runtime/tests/network/source-State writes/subagents. stdlib hash/line-count only + source reads. Old saved source readonly comparison only.

## Bound inputs

- Root: `../astra-repair-resolution.md` FULL §§1–2.
- Map GO: `../integration-map.md` + machine, `../independent-map-review.md` + machine `GO_SCOPED`.
- Implementation: `README.md`, `machine.json`, `raw/source-diff.patch` 47 lines, `raw/stderr.txt` 1455B, `raw/exit.txt 0`, `raw/stdout.txt` 0B, `raw/git-status.txt`, `raw/rev-parse.txt`, `raw/env-whitelist.txt`.
- Actual new copy: `.rephase-1-editorial-runtime/prior-artifact-reader-implementation-20261122T062101Z/candidate-work`
  - `scripts/survey_stage_validation_v2.py` 51927B `1e4c818b144ebeed7a4365cb00b5e43ed93e9bff4d1396691432ba77a515787e` `0o100664`
  - `tests/test_prior_artifact_reader_repair_v2.py` 22782B `926af092519f641c060dc3d3aa380a2f3fae7e85eccec4896283075b06671030` `0o100664` 408 lines
- Old saved source readonly: `.rephase-1-editorial-runtime/selection-scaling-real-20261116T021943Z/candidate-work/scripts/survey_stage_validation_v2.py` 49688B `ec15f5ba6b0a15162cb42543b15de63ca6ca8581ff63c8ec339229b437867d9c`.
- Diff hash: `raw/source-diff.patch` SHA256 `cf946e74d18e4305c6b5792350e4f410dbc7b327560d0f66d31d07152a3246af` 47 lines.
- Identity: HEAD `3231a0c280287411513bba359f4d3d2b6703d591`, parent `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56`, tree `ff01b73e6012fd4519fdfb3807186753ff330367`, `f591` missing as expected. 774 before +775 after (1 new test). Runtime scope only, not whole-history claim.

## Verdict: GO_SCOPED_AFTER_TEST_SUPPLEMENT

Code matches selected map. No load-bearing source bug. Tests are genuine public-path evidence (8/8 PASS transcribed, not re-executed here) but two TEST-only oracles are still pending per root. No full PASS, no real-material permission, no source commit yet.

Do not require full proof/decision byte-checks beyond contract historic SHA fields. Do not demand whole expensive R3; active PUB7 unchanged supports bounded regression only if needed.

## Source verified (new copy vs old saved + diff)

- Scope exactly one function `_prior_artifacts` 328–423 old → 328–459 new, +36 added lines shown as 47-line unified diff, no deletions. Imports unchanged (22,30,36,39 already `agent,low,_setmod,core,schema_gate`). No new module/schema/family/flag/cache/verified-dict/public flag/third validator.
- Per-row `low.load_typed_checkpoint_record` before dedup; `ResearchAuthorityError` → `StageValidationError` fail-closed via `except Exception`. Correct.
- PREARCH: `name not in DM022_PREARCH_CHECKPOINTS → DM022_WRONG_FAMILY` even if `rel` seen (role-before-seen). Distinct `rel` → `agent._validate_checkpoint_record(...,revalidation=None,pending_basis=None)` keywords equal defaults, PREARCH branch returns at 805 before legacy/superseded logic (770–805). `errs` joined on raise. Correct, no LIVE `validate_agent_state`/guard/HIGH recursion in reader or PREARCH branch.
- Merge from `fam["record"]["artifacts"]` standalone, never old `record` legacy projection. Live `core.repo_local_path` + `sha256_file==row["sha256"]` drift check + `existing.resolve()!=artifact.resolve()` disagree check, NO `superseded` override. `seen.add` + `continue`. Correct.
- `family != LEGACY → unknown family refused`. LEGACY 362–375 byte-for-byte preserved with `bound_prior/superseded` allowance. `_authority_ref_path` provenance path+sha vs file unchanged. Active7 Group C + `_merge_artifacts` + `_require_active_candidate_binding` + entry/prepublish READY + report unchanged.
- Split-ref: same path AND sha triplet (795–800) + `issue_id` (801–802) inside reused helper; per-row authority drift + live rehash + collision cover path/sha/artifact drift. No publication override for PREARCH. `precord` unreadable / row non-dict fail-closed.
- Race note: `fam` loaded before `_validate...`; `_validate...` re-checks provenance SHA + full `low.check_supersession_record_from_paths` reload (report/before/retention/4 FULL validators, own-epoch Contract8, View→Evidence). Mutation between loads fails `_validate` provenance/proof before merge, so stale merge unreachable single-threaded. No new cache/API beyond existing `seen` set. `DM022_PREARCH_CHECKPOINTS` identical in stage/agent/handlers.
- Non-blocking: merge `row["path"]` KeyError would escape as KeyError not `StageValidationError`, but unreachable because loader + `_validate_prearchitecture_record_content` shape checks (exact 4 NamedRefs, `{"name","path","sha256"}`, SELF digest) already refuse before merge. Same pattern as legacy. Not a change request.

## Tests verified (read-only, no re-execution)

- File 408 lines, no `unittest.mock`/`patch.object` (only docstring “no mocks”). Real imports: `survey_production_v2`, `survey_research_authority_v2`, `survey_stage_validation_v2`, `survey_agent_control_v2`, `test_dm022_full_lifecycle_v2` helpers, `survey_prearchitecture_acceptance_v2.high.adopt_revision`, `survey_screening_v2`, `run_selection_architecture_v2_interactive.run`.
- Genuine HIGH-adopted PREARCH via `_chain_root/_materialize_production_discovery_acceptance/_make_evidence_reviewed_state/_prepare_and_decide/high.adopt_revision` + 7 writer outputs asserted, own epoch (no 480 literal), process-scoped Git, inert origin. Public `validate_stage EVIDENCE→SELECTION` exact `CORE_STAGE_CONTRACT` keys + `implementation_commit_sha==HEAD` + no-overwrite rerun → `build_stage_checkpoint/advance` to SELECTION_COMPLETE → public `validate_stage` architecture → advance to ARCHITECTURE_ESTABLISHED pending Human. Both Weekly + Thematic full routes. Synthetic reviews JSON (`synthetic-priorfix-fixture`, DETERMINISTIC) only for checkpoint build, not claimed as real Human approval. LEGACY same-record stays LEGACY PASS.
- Negatives fail-closed no report: wrong-family alias after seen (direct helper `DM022_WRONG_FAMILY` + public alternative), unknown kind, malformed SELF (`00*32` with updated provenance), split SHA (`11*32` → triplet), drift one-byte/missing, `_merge_artifacts` replace-refusal collision, guard history-vs-mutator entry.
- Raw: `stderr.txt` 8/8 `ok`, `Ran 8 tests in 228.541s OK`, `exit 0`, `stdout` empty, `wall 229s`, `2026-11-22T06:29:38Z–06:33:27Z`, `PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=0`-scoped env, `git-status` shows only `M scripts/survey_stage_validation_v2.py` + `?? tests/...` as this unit; other `M/?? sources/*` are inherited worktree-vs-HEAD real-material deltas per README, not test mutation. Scope is current runtime binding only.

## Required TEST-only supplements (pending, no code change)

Per root, record as oracles, not full PASS until read:

1. Actual PREARCH post-semantics (late) guard: wrap original `_validate_stage_semantics` to inject guard between entry and prepublish, prove `validate_stage` refuses `DM022_TRANSITION_ACTIVE` with no report, then release passes. Current `test_guard_history_vs_mutator_and_late_ready` proves only ENTRY guard (`_dm022_require_ready` at entry) + history-detached `_prior_artifacts` allows guard. Name is misleading; late coverage missing.
2. Direct prior-artifact collision in `_prior_artifacts` merge branch (`existing.resolve()!=artifact.resolve()` for distinct priors sharing artifact name). Current collision proves only `_merge_artifacts` replace-refusal via temp file. Need two distinct prior records disagreeing on same name through `_prior_artifacts` (LEGACY distinct priors or equivalent), expecting `prior Stage Checkpoints disagree on artifact name`.

Additional bounded existing tests allowed given PUB7 unchanged, but no whole R3 demand.

## Conditions (original, preserved)

- Code commit not yet allowed at original review. No real W34/SP validation/writer/regeneration, no CURRENT pack, no State/Profile repin, no manual CORE report, no network/Production/Human approval/Draft/PDF/R4/ordinary Commit-Push.
- Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Commit Point; ordinary Commit/Push Human-owned.

## Supplement resolution — Final technical binding (supplement-20261122T064124Z, TEST-ONLY, no code change)

Bound: `supplement-20261122T064124Z/README.md`, `machine.json`, `raw/` (combined + `per-late/` + `per-collision/`), `raw/test-diff.patch` 131 lines, `raw/final-test-hash.txt`, `raw/ast-old8.txt`, `raw/code-frozen.txt`, `raw/stderr.txt`, `raw/exit.txt`, `raw/stdout.txt`, `raw/start.txt`, `raw/end.txt`.

- Code frozen unchanged verified (stdlib hash): `scripts/survey_stage_validation_v2.py` 51927B `1e4c818b144ebeed7a4365cb00b5e43ed93e9bff4d1396691432ba77a515787e` `0o100664` 989 lines. `raw/code-frozen.txt` claim matches actual. No production change.
- Final test verified (stdlib hash): `tests/test_prior_artifact_reader_repair_v2.py` 30019B `1fb831673b8291813ab0480720f84467e334374619a87fe072ff00c63438d4db` `0o100664`, actual `wc -l`/splitlines 522 (packet claims 520 — 2-line doc-count deviation, non-blocking, hash authority controls). Before 22782B `926af092519f641c060dc3d3aa380a2f3fae7e85eccec4896283075b06671030` 408 lines preserved by reconstruction.
- Old-8 preserved: `raw/test-diff.patch` shows doc-qualifier only (`no mocks` → `no fake validators` + probe note) + 2 new classes, no old body edits. AST list in final: old 8 + `TestPriorArtifactLateGuardPrepublish.test_prearch_late_guard_refuses_prepublish_no_report` + `TestPriorArtifactDirectCollisionPrearchMerge.test_direct_prior_collision_hits_prearch_merge_disagree` = 10 total. `raw/ast-old8.txt` lists old 8 stable. Fixture helpers (`_adopted_prearch_with_outputs`, `_legacy_with_outputs`, `_public_validate_*`, `_advance_selection`) unchanged; only new test classes added, not mod assertions in old bodies.
- Supplement 1 late guard verified by read: wraps ORIGINAL `stage_validation._validate_stage_semantics` via `orig_semantics` + `_inject_then_return` calling original then creating owned guard (`low.guard_path_for`) before return, `mock.patch.object(...,side_effect=...)` never replacing validators with PASS. Targeted normal `validate_stage` EVIDENCE refuses `DM022_TRANSITION_ACTIVE|guard` (prepublish `_dm022_require_ready`), fresh `EVIDENCE-late-bad.json` absent, immediate `state_abs`/matrix/selection bytes unchanged except intentional guard (`is_file`), then own-fault restore + separate recovery `EVIDENCE-late-restore.json` PASS (not claimed as immediate proof). Genuine tiny HIGH adopt WEEKLY `late`, PREARCH family, EVIDENCE_REVIEWED triplet, `implementation_commit_sha==HEAD`. Covers pending late oracle.
- Supplement 2 direct collision verified by read: fault State-copy only, no shipping config. Base genuine adopted PREARCH `collide` with `agent._validate_checkpoint_record(evidence)==[]`. Reuses actual LEGACY screening record+report to disposable `disposable-screening-collision*.json` inside independent DB, adds contradictory `evidence-acceptance` row (screening-acceptance path/sha, different resolve from PREARCH evidence) to BOTH record and report, repoints review result to disposable report. `bad_state` repoints only `screening` provenance (new SHA); `evidence/materiality/completeness` keep PREARCH triplet. Proves LEGACY disposable `screening==[]` and PREARCH `evidence==[]` alone, then `_prior_artifacts` hits `prior Stage Checkpoints disagree on artifact name: evidence-acceptance` (screening LEGACY merges first dict order, PREARCH merge second hits `existing.resolve()!=artifact.resolve()`). Specific new PREARCH-merge error, not old `_merge_artifacts` temp-file probe nor early schema/provenance preemptor. Covers pending collision oracle.
- Runs transcribed (not re-executed): combined `2026-11-22T06:42:23Z–06:43:10Z` ~47s wall, `Ran 2 tests in 46.406s OK`, `exit 0`, `stdout` empty; per-late `Ran 1 test in 40.703s OK` `real 41.06s` `exit 0`; per-collision `Ran 1 test in 6.366s OK` `real 6.70s` `exit 0`. Same cwd/env `PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0` scrubbed `GIT_*`. New-only 2 unique methods; per-test runs are duplicates, do not sum to 4. Old-8 raw preserved in `../raw/`.
- Source before/after: 775 = old frozen 774 + 1 modified `scripts/survey_stage_validation_v2.py` + 1 new test. No other source change claimed.
- Scope/limitations: public synthetic both-routes evidence only (Weekly/Thematic synth DBs, genuine HIGH adopt + public validate/advance), not real W34/SP validation, not whole R3, not audit, not Human approval. Read-helper TOCTOU bounded single-threaded (provenance + full proof reload before merge), not global CAS/crash-atomicity. Proof/decision SHA-field byte checks unchanged per contract. Doc line-count 520 vs actual 522 noted, hash controls.

Final binding: no blockers. Prior `GO_SCOPED_AFTER_TEST_SUPPLEMENT` conditions satisfied.

Verdict: `GO_TO_SOURCE_COMMIT_AND_BOUNDED_REAL_VALIDATION` for code (51927B `1e4c818b…`) + focused test (30019B `1fb83167…`). Root dispatch for actual source commit and bounded real-material validation separate; no standing real-run permission claimed here. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN preserved.
