# Affected verification — Evidence scaling repair (NEW General verification owner)

Packet: `notes/rephase-1-evidence-scaling-repair/affected-verification-20261103T175000Z/`
Status: **All selected affected batches green, fresh CURRENT proof green. No implementation/audit/adoption/semantic PASS. Root + independent reviewer decide.**

## 0. Root addendum 2026-11-04 — old 478 qualified, NEW actual CURRENT supplement

Per Root: `current_proof_harness.py` 478 PASS (`test-runs/batch-09-current-proof/`, fixtures `.../current-proof-fixture-*/`) are **preserved, not erased**, but qualified as **closure/file assertions only** (`current_closure` live-SHA, `verify_closure_at_commit` Git-blob equality, Contract8 recompute, hist no-LIVE guard). They call `current_closure`/`verify_closure_at_commit` but **NEVER `survey_versioned_renewal_source_v2.verify_renewal_source_proof`**; mutated-closure-vs-HEAD is narrower than SAME persisted proof rejecting CURRENT drift. That harness also `git config user.name` (line127) despite process-identity instruction and sets `HOME=/tmp` — disclosed fixture-only deviation (don't erase), no universal rerunner safety. Fresh root `969b…` contains new bytes but no old→new epoch transition; real409 `e84a…` provides genuine code-epoch transition, don't attribute it to fresh root. Historical helper probe DIRECT+None refusal is not COPY/DERIVED proof (actual new19 separate cases cover). Keep useful closure checks labelled correctly, 478 checks not 478 tests.

NEW actual CURRENT supplement (no repeat of green batches 01–08/00/19/W34):
- `current-supplement-20261104T003000Z/README.md` + `data/` + `harness/` + `raw/` — genuine `CURRENT_PROOF_VALID True` via real `verify_renewal_source_proof` (weekly, final139, closure 70), SAME-proof `BASIS_CURRENT_TOOL_DRIFT` refusal on CURRENT LOW byte, restore-positive, all771 pre/post binding to final patch `de0af9…`/manifest `c5a6b230…`.
- Preserved setup failure: `current-supplement-20261104T000000Z-HIGH-toolchain-blocked/` (HIGH finalize `BASIS_ENTRY_INELIGIBLE: ... toolchain executable must be an existing file`, TeX absent, no fake).
- Old harness/raw preserved with qualified claims above. Test19/Raw409 not repeated (already green).

## 1. Authority read + scope

Read in full before execution: `notes/rephase-1-evidence-scaling-repair/astra-implementation-resolution.md` FULL §7, `astra-source-review.md`, `final-implementation-review.md` (bounded source/operation PASS, NOT delivery), `real-w34-retry-20261103T172327Z/README.md` + raw, `notes/rephase-1-evidence-scaling-test-final19-20261103T173758Z/README.md` + `test-runs/batch-01-final19/` (19/19 green, not repeated here).

Task: meaningful regressions/CURRENT proof beyond new19 after actual409 success. NOT source author / NOT independent reviewer. Code quiescent, packager parallel read-only. No edit runtime/tests; failures return Root. No subagents/network/Production/current checkout/HumanCommit readback/ordinary commit. Meaningful fixture commits only new isolated DB/process identity/no empty/no object sharing.

## 2. Fixed NEW snapshot (771, verified full hash)

- Snapshot: `.rephase-1-editorial-runtime/evidence-scaling-affected-verify-20261103T175000Z/snapshot-fixed`
- Method: `mkdir -p` (parents verified), `tar --exclude=.git -cf - -C final19-candidate-work . | tar -xf - -C snapshot-fixed` exit 0, `cp -a final19/.git snapshot-fixed/.git` exit 0. No blind-copy author residue. Preserved original/final19; no old runners, no cleanup/reset/raw overwrites.
- Git: HEAD `e746a5dbb8ad657feb0e2a4c7602a79239c878ba` (final19 synthetic-fixture-only execution snapshot, independent DB, inert origin `https://example.invalid/evidence-scaling-final19-20261103T173758Z.git`, no alternates, no `GIT_*`), `status --short` clean (after narrow `rm -rf` of harness-created `__pycache__`, disclosed below), distinct inodes vs final19 (copy, no hardlinks).
- Count: 771 files excl `.git`/excl `*.pyc`/`__pycache__`, 0 `*.pyc`, 0 `__pycache__` after narrow removal. `tests/__pycache__` + `scripts/__pycache__` recreated by CURRENT harness (in-process imports) despite `PYTHONDONTWRITEBYTECODE=1`; removed narrowly (`rm -rf` exact two dirs) to restore clean binding. No source/test edits.
- Frozen pins re-observed (full SHA256 + bytes, verified actual full hash):
  - `scripts/survey_evidence_v2.py` 158943B `487425385052fa181b0a24954815c6fbb6882a0af1fc7256ef7352b309359c2a`
  - `scripts/run_evidence_v2_interactive.py` 45833B `5e195730d1553b2359eb5729cebaa49e9bd616b4b3f63b65dca413ef33c3e543`
  - `scripts/survey_research_authority_v2.py` 218692B `0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b`
  - `tests/test_evidence_scaling_v2.py` 106616B `7b862305db39afde93c44ca0f1ce2d4b5faf512729e6956a8166b16f09c0e12e` (19)
- Author workcopy `evidence-scaling-implementation-20261103T114312Z/candidate-work` now same 3 runtimes + final test `7b862305` (verified); source author quiescent during execution (no runtime/test edits observed; pins-before==pins-after every batch).

## 3. Selected batches (proportionate, no old-hundreds decoration)

Rationale by actual shared Evidence readback/card body/LOW source-7 changes (Evidence card construction/validation core, runner facade, LOW bulk). No PASS transfer: same test module names as prior Profile packet BUT SOURCE NEW, rerun on new source.

- `batch-01-positive-smoke` (2): `DM016CanonicalTenTests.test_01…` + `SurveyEvidenceV2Tests.test_evidence_authority_supplement_binds_exact_raw_source_and_card` — setup check, not counted as full suite.
- `batch-02-profile-28`: `tests.test_profile_support_upstream_repair_v2` full 28 (DM016/DM017/Parity/History/Prepackage/DERIVED/Guard).
- `batch-03-evidence-runner-agent-sourceclass-26`: `test_survey_evidence_v2` (12) + `test_run_evidence_v2_interactive` (8) + `test_run_evidence_v2_agent_first` (4) + `test_survey_evidence_source_class_regression` (2) =26.
- `batch-04-dm022-c7`: `tests.test_dm022_c_direct_operation_v2` full 7 (weekly/thematic prepare/adopt/readback, DERIVED R!=E, negatives, binding, extra-rows).
- `batch-05-dm022-a2-selected-5`: 5 from `test_dm022_prearchitecture_acceptance_v2` (25 total, only affected 5 run): weekly/thematic actualops + low_typed_loader + low_guard + high_cli_prepare_adopt. Remaining 20 A2 not run (gap).
- `batch-06-family-6`: `tests.test_dm022_c1_family_closure_v2` full 6 (literal membership + actual files + AST + own-epoch + schema fingerprint + reloaded G71→G76 70-dep graph).
- `batch-07-graph-h-8`: `test_dm022_c1_research_graph_v2` (5) + `test_dm022_c1_h_presence_controls_v2` (3) =8 (real-file discriminators, LOW typed loader, own-epoch, G71/G76 control, absent/committed presence).
- `batch-08-consumers-3`: 3 single existing consumers (Selection-stage, 7-slot retain/clear/regenerate, draft synthesis reader) — selected family/current/historical/consumer paths.
- `batch-09-current-proof`: NEW `current_proof_harness.py` (packet-only, not shipping) — fresh CURRENT source proof (see §5), 478 checks.
- `batch-00-loader`: `loader_probe.py` (packet-only) — same-process `__file__` binding + committed-blob equality.

Runner: packet `run_affected_verification.py` (fail-closed Popen wrapper, sequential, no `timeout`-shell, common-positive-setup STOP armed, no failure so all ran). Each batch own exact run, no cross-batch count sums. `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=snapshot-fixed`, cwd snapshot-fixed. Genuine verbose `stderr.txt` holds `Ran … OK` (unittest -v writes to stderr; `stdout.txt` 0B by framework, not loss). Numeric exits saved. No skips/errors/failures in any batch.

Results (all `pins-same YES`, 771 identical pre/post, no source/test edits):

- 01: PID 3586867, 2026-11-03T17:48:24Z→17:48:25Z, exit 0, `Ran 2 tests in 0.283s OK`
- 02: PID 3586885, 17:48:25Z→17:48:34Z, exit 0, `Ran 28 tests in 8.380s OK`
- 03: PID 3587633, 17:48:34Z→17:48:38Z, exit 0, `Ran 26 tests in 3.058s OK`
- 04: PID 3587802, 17:48:38Z→17:48:57Z, exit 0, `Ran 7 tests in 18.704s OK`
- 05: PID 3589690, 17:48:57Z→17:49:05Z, exit 0, `Ran 5 tests in 6.883s OK`
- 06: PID 3590524, 17:49:05Z→17:49:06Z, exit 0, `Ran 6 tests in 1.329s OK`
- 07: PID 3590548, 17:49:07Z→17:49:17Z, exit 0, `Ran 8 tests in 9.881s OK`
- 08: PID 3592139, 17:49:17Z→17:51:23Z, exit 0, `Ran 3 tests in 126.126s OK`
- 09: PID 3623024 (harness process), 17:56:44Z→17:56:46Z, exit 0, 478 PASS `CURRENT_PROOF_HARNESS_OK`, `stdout.txt` 54004B (all PASS lines), `stderr.txt` 0B
- 00: exit 0, `LOADER_BINDING_OK`, 771 pins, HEAD `e746a…`, 3 runtimes + test match working==committed.

Raw paths: `test-runs/batch-*/{stdout,stderr,exit,argv,env,cwd,pid,wall-start,wall-end,meta,pins-before,pins-after,pins-same}.txt` + `batches-summary.json`. No historical runners overwritten/reused.

## 4. Loader binding (strict source hash/binding)

`loader_probe.py` (packet, `-B` to avoid bytecode): same-process `__file__` under snapshot-fixed, SHA256+bytes+mode match frozen pins, `git show HEAD:<rel>` SHA256 == working == SNAP running (before authority), `git status --porcelain` empty, HEAD `e746a…`, inert origin, no alternates. Rejects wrong loader path or missing CURRENT proof (exits 2). See `test-runs/batch-00-loader/stdout.txt` (binding OK).

## 5. CURRENT proof (fresh, not membership-count/sha-alone)

Harness: `current_proof_harness.py` (packet-only, not shipping module). Uses actual public builder/validator APIs + existing C1/renewal fixture tests (inspected, not bypassed). No fake proof/self-report cache; must-not-call LIVE guard is refusal proof (AssertionError on LIVE use, no fake pass), not monkeypatched success. No whole-RELEASED/PDF claim, no Source Gate fake Human review as real.

- New genuine changed runtime epoch: NEW independent DB `current-proof-fixture-20261103T175645Z` (ignored runtime, inert, process identity, no empty, no object sharing, no `git config` writes), copied 771-file worktree (22M), verified 3 runtimes + G76 7-file match SNAP running before authority, committed `969bd4f233127dfb6975fa26c0a1c236bb5979d9` (40-char, meaningful message, NOT ordinary candidate). Earlier 3 fixtures (566e…, ec9d…, ea27…) are superseded harness-dev attempts, preserved in runtime, not authoritative. Manifest (no full DB in packet): `test-runs/current-proof-fixture-manifest.json` + `current-proof-checks.json` (478 checks).
- CURRENT family from disk: `_derive_current_family_from_disk` → `G76` (not hardcoded).
- Closures all mapped, no new family/schema: receipt G71/G76 delta == 7 `DM022_NEW_UNTRACKED_7` (both routes), all files exist; staged 63→70 delta 7, all exist; canon weekly 29→36, longform 34→41, all exist; `_verify_actual_import_closure` weekly+longform pass; known family config maps (`_OLD_PY_30/_NEW_PY_3/_FAMILY_PY_2/_NEW_DM022_MODULES_2`, `_NEW_SCHEMAS_5`, `_ALLOWED_SCHEMA_PATHS/_KNOWN_SCHEMA_SHAS`) compared as actual sets, no new family/schema.
- Contract8 unchanged (typed): `contract_identity(SNAP, cfg, WEEKLY, WEEKLY_MAGAZINE)` recomputed fresh == State `3adfbda2…/b5b955…/666f8a…/99adff…` (pipeline/quality/research/publication, 8 fields). Script-only edits have no Contract8 members, confirmed.
- Live SHAs == `current_closure` rows (weekly 36, longform 41, fresh, not old proof reused). `verify_closure_at_commit(fix, closure, new HEAD)` weekly+longform pass at new epoch (fresh bound Git-blob proof, member-wise `git show <commit>:<name>` byte equality).
- Drift refusal: mutated working copy (one byte in `survey_research_authority_v2.py`), recomputed closure at same HEAD refuses `Weekly historical closure bytes differ…` (exact). Restored, matches SNAP again.
- Historical `_content` with supplement + real R/E/COPY, no LIVE at return: real `ScalingFixture.base(["hist1"])` (independent temp DB, meaningful commits, process identity), real supplement validator + manifest, real `prepare/build/accept` chain, real `resolve_effective_discovery_basis` (true R, not E-as-R), `expectations` with canonical State path, `_validate_evidence_acceptance_content` with `mock.patch(core.verify_state_basis, side_effect=AssertionError)` (must-not-call guard) validates `SP001` (no LIVE read). LOW `derive_ordinary_root_effective_context(None,None)` refuses exact `revision request path must be a Path or non-empty string, got NoneType` (COPY required). R!=E distinct per W34 R369/E439 (read-only, no E-as-R; see real retry packet).
- Fixture blobs at commits matched running modules before authority (3 runtimes + 7 G76 files + sampled closures, `git show HEAD:<rel>` SHA256 == working == SNAP).

Known family config membership maps read: `config/survey-production-v2.json` contract_files pipeline/quality, `weekly-pipeline.json`/`special-pipeline.json` lifecycle/policy (no new family), plus G71/G76 literal maps above. No new schema/family.

## 6. Remaining gaps (no blanket PASS)

- Full19 19 already green final (`7b862305`, 19/19, 8.2s, PID per raw) NOT repeated (no new concern/packaging need for those 19 alone; CURRENT harness re-proves historical no-LIVE + LOW refusals fresh).
- A2 remaining 20/25 not run (only 5 affected selected). Full `prearchitecture_acceptance` 25, `full_lifecycle` beyond 3 consumers, `normal_writer_late_guard`, `b_late_prepublish`, `g71_g76`, `lifecycle`, `prearch_b_ordinary_consumers` 23 beyond selected, `dm022_full_lifecycle` beyond 3, etc. not run, not claimed.
- No real409 re-run here (already `e84a…` exit 0, 409 completion, 45GB logical rchar, 175s wall, full validators/readbacks, strict facades; see real retry packet). CurrentProof fixture is source-proof, not 409 re-execution; no new wall/physical-disk performance claim (currentProof calls no need physical-disk proof).
- No PDF/RELEASED/EVIDENCE_REVIEWED/Gate/Production claim. SP Ledger/Completeness disposal still held (W34 proceeds, SP retry needs guarded decision). No savings/quality/adoption claim.
- Three superseded harness fixtures retained in ignored runtime (566e/ec9d/ea27) + final authoritative 969b; packet holds manifest + checks only (no full DB in packet). Harness-created `__pycache__` removed narrowly (disclosed); no source mutation.

## 7. Pointers

- Runner: `run_affected_verification.py`; batch-09 runner: `run_batch09.py`; harness: `current_proof_harness.py`; loader: `loader_probe.py`
- Snapshot: `.rephase-1-editorial-runtime/evidence-scaling-affected-verify-20261103T175000Z/snapshot-fixed` HEAD `e746a…`
- Fixtures (ignored runtime, manifest in packet): `.../current-proof-fixture-20261103T175645Z` HEAD `969bd4f…` (authoritative); superseded `...-175545Z/175558Z/175613Z`
- Raw: `test-runs/batch-*/`, `test-runs/batches-summary.json`, `test-runs/current-proof-checks.json`, `test-runs/current-proof-fixture-manifest.json`
- Next: Root + independent reviewer decide (delivery/independent implementation review → Human Commit Point). No implementation/audit/adoption/semantic PASS here.
