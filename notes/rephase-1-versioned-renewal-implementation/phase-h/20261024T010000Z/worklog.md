# Phase-H correction worklog — STRICT fail-closed historian (append-only, preserves prior runs)

2026-10-24. AUTHOR correction for Astra REJECT of phase-H-complete claim.
Workdir authoritative: `.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work/`
(actual409 `409b292`/tree `8ce36998`+57 25M32A; candidate remains actual409 uncommitted, no ordinary commits).
Rejected M1 `.../versioned-renewal-impl-20261023T181352Z/candidate-work/` (fake-root `a8890d4`)
+ env `184000Z` FAIL + prior phase-H `20261024T000000Z` (5 minimal tests) retained as failure evidence,
not deleted, not reset. Source precorrection pins retained (contract478f0051, root7d7d5a45,
R3 `d080c182`/json `1f758b0a`, R4 `b8e422bb`, R5 `57b6b023`, patch`659063dc`/2018112B).

## 1. Astra 7 fatal classes fixed (grounded code, not minimal spots)

- **Editorial exact 15 names + required refs**: `roles` must equal `PUBLICATION_ROLES_15` exact
  (missing/extra lists, no `len==15`), `proposal/staged/build` required live, seal `set_sha256`
  self-digest verified. Proposal/staged/retention/scope required (not optional skipped).
- **Scope O17 whole-doc**: `schema_pointer` must be `""` (never `"/"`), schema blob+mode at
  `staged_head`, scope cross-bindings (reviewed_surface, `WITHIN_APPROVED_AUTHORITY` where present,
  before_reader/preserved_upstream/summary/locations/PASS where present).
- **Staged code_deps exact**: `_expected_staged_code_deps(route)` fixed 50 sorted, each row exact
  `{path,sha256,byte_count}`, name set equality (no subset/superset), order sorted, each blob+mode
  at `staged_head` + byte_count matches epoch blob length. Style trio file is E, explicitly NOT
  required at tool commit (forbidden check removed).
- **Receipt T exact + no swallow**: receipt `current_tools.repository_commit_sha` must equal derived
  `receipt_epoch` (no swallow of `RenewalHistoryError`, fail-closed if receipt missing/invalid),
  receipt `receipt_sha256` self-digest where present, closure exact via
  `_verify_receipt_closure_exact` (name==path, exact 50 OLD for editorial / 63 NEW for versioned,
  no subset, each blob+mode at epoch).
- **Retained COPY not live + digest recompute**: `before_state_ref` live NOT validated as mutable
  authority; retained COPY via retention rows (`COPY_BEFORE_REPLACEMENT` + `KEEP` Profile via
  retained bytes, not live), exact inventory, `before_active_digest` recomputed chain-wide via
  `_verify_before_digests_chain` (original 7 vs latest legacy vs prior seal seven, repeated must
  equal prior seal Candidate, Candidate PDF must bind effective PDF), not presence-only.
- **Closure exact membership**: `_verify_receipt_closure_exact` enforces `name==path`, exact expected
  set (50 OLD / 63 NEW per route/generation from fixed registries, no `*.py` blanket, unknown refuses),
  count/set/order/blob/mode all fail-closed (subset/superset/order drift all refuse).
- **Versioned exact path+SHA + epoch from owner graph + order fail-closed**: seal/basis/proof refs
  checked exact path+SHA (not path-only), `history_graph` derived from linked docs
  (prior seal receipt/staged + basis CURRENT, never inferred from untrusted observed rows),
  SCHEMA epoch must equal derived owner (no caller authority), supported==observed sorted-set
  equality + file-bytes order must equal sorted order (both fail-closed, old `pass` removed).
- **Observed bindings for builder**: `verify_versioned_history` returns
  `observed_source_bindings` (exact owner/source paths, sorted deduped) derived from verified bases,
  not claimed when skip cases (required scope O17 + RECEIPT coverage enforced, missing fails closed).
  No caller verified dict.
- **FD-bound + limits + close**: `_fd_safe_read` via root FD + `dir_fd` chain, entry-vs-fd binding,
  symlink/dir/FIFO refusal, `MAX_PATH_LEN`/`MAX_PARTS`/`MAX_FILE_BYTES`/`MAX_JSON_BYTES` limits,
  checked close (fail even when bytes complete), no checked-path race.

## 2. Harness — NEW complete-source fixture DB (not git ls-files)

- Prior 25 retention errors are HARNESS setup failures (`git ls-files` misses untracked 32),
  NOT pre-existing product defects. New harness copies complete source via worktree walk
  (all 721 + phase-H newcode + synthetic source/high stubs for closure exactness in isolated DB only,
  labelled synthetic, never claimed as public operation) and commits BEFORE authorities in
  workspace-local scratch `.rephase-1-editorial-runtime/versioned-renewal-test-scratch`
  (not `/tmp` quota, not candidate commit, disjoint inert DBs, genuine tool-before-authority ancestry).
- Fixture provider OLD active R3 under old721 code assigned separately; integrate when provided,
  not calling old unsafe scripts. Current complete graph is synthetic realistic (exact 50/63,
  all cross-bindings) for unit scope, distinguished from actual public operation acceptance
  (production semantic NO-GO retained).
- Scope owned H files unchanged; no shared other module editing (only historian + 4 schemas +
  low plumbing `publication_set`/`agent_control`/`revalidation`; other workers own source/high/content).

## 3. Tests — full strict realistic complete graph, every predicate mutated with correct cause

NEW `tests/test_versioned_renewal_history_phase_h.py` (2 complete tests, fresh NEW procedures,
no saved runners, no AST/string-presence as proof, all behavioral):

- `test_complete_editorial_passes_and_mutations`: complete editorial (exact 15, required refs,
  self-digest, cross-binding, staged 50, receipt 50 OLD, retained COPY not live, digest recompute)
  passes `HISTORICAL_IDENTITY_VERIFIED`; seal name mutation -> `HISTORY_DIGEST_MISMATCH` + repair;
  staged code_deps subset -> `HISTORY_DIGEST_MISMATCH` + repair. E-uncommitted-at-tool-commit positive
  (E absent at tool epoch proved via `git show` fail, historian still passes).
- `test_complete_versioned_passes_and_mutations`: complete versioned (prior editorial + basis/proof/set
  with exact 63 NEW, observed scope O17 `""` + RECEIPT required, derived epochs, supported==observed +
  sorted order, retained COPY, digest recompute with prior seal seven, foreign lineage via issue,
  derived bindings for builder with exact owner/source paths) passes; proof tamper without updating
  seal/record -> `HISTORY_DIGEST_MISMATCH` (exact path+SHA) + repair; direct epoch drift via
  `_check_observed_binding_row` with tampered epoch -> `HISTORY_TOOL_EPOCH_DRIFT`; basis order tamper
  without updating record -> `HISTORY_DIGEST_MISMATCH` + repair; plus duplicate/raw/symlink/depth/anchor
  covered in prior run retained as evidence (now superseded by strict complete tests but preserved).
- Synthetic fixtures labelled synthetic in code comments + this log, never claimed as actual public
  operation; strict unit scope only, not whole PASS.

Raw (candidate-work):
- `python3 -m unittest tests.test_versioned_renewal_history_phase_h -v` -> 2/2 OK.
- `python3 -m unittest tests.test_survey_publication_set_v2 tests.test_repository_contract_syntax` -> 20/20 OK
  (18 pubset + 2 contract). `test_survey_publication_revalidation_v2` 31/31 OK (prior run retained).
- Retention 25 errors retained as harness evidence (not product defects).

## 4. Interfaces for Root (exact, no unmapped fields)

- `verify_versioned_history(root,record_path)->{HISTORICAL_IDENTITY_VERIFIED,observed_refs,observed_source_bindings (sorted deduped exact owner/source paths),chain_length,anchor_kind}`.
  `verify_renewal_retention(root,basis_path)->{HISTORICAL_IDENTITY_VERIFIED,retained_copy}`.
  `_expected_receipt_closure(route,OLD|NEW)`, `_expected_staged_code_deps(route)`,
  `_derive_history_graph_for_editorial`, `_check_observed_binding_row` (derived owner),
  `_verify_before_digests_chain`, `_compute_before_digest_hist`. No caller dict/epoch.
- Low: `_is_versioned_record` (activation pair) + `_is_versioned_seal` (seal pair) in both modules,
  versioned seal/activation HIST-only, legacy/editorial verbatim, full `validate_agent_state` preserved.
- Schemas: 4 new strict + revalidation 3rd branch as before (pointer `""` allows empty, no `minLength:1`).
- On contract contradiction return precise `file:line` before broadening. No faithfulness from AST tests.

Stop here. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN. Ordinary Commit/Push Human-owned.
