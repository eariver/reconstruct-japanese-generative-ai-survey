# Evidence scaling repair — TEST-owner preparation (v3: fixed-snapshot runs)

Fixed snapshot `.rephase-1-editorial-runtime/evidence-scaling-fixed-20261103T124755Z/candidate-work/`
(771 files, independent DB HEAD `a7245948…`, inert origin, no alternates).
Runtime pins (before/after every batch, unchanged): Evidence `dfc5e27f…`/156966B,
runner `c9b7c70b…`/45501B, LOW `0974c709…`/218692B. Test module final `1c95f675…`
(synced exact snapshot→author workcopy after green runs).

Scope: TEST-owner rewrite of `tests/test_evidence_scaling_v2.py` (workcopy
`.rephase-1-editorial-runtime/evidence-scaling-implementation-20261103T114312Z/candidate-work/`),
replacing the rejected initial 5-test draft per Root `astra-source-review.md`
INCLUDING the new §22 independent disposition. Source owner is finishing
readback task/result pins + ancestors; **no test/import/run was executed here**
(static `ast.parse` only). Root dispatches the fixed snapshot, then runs.

Special tooling disclosure: `apply_patch` is absent in this harness; used
`default.edit`/`default.write`. No shell binary search for semantics; no
network/current checkout/Production/Git readback/ordinary commit. No
subagents. No runtime/config/schema edits.

## Rejected-draft archive (race-safe)

- Initial test bytes+hash preserved at
  `notes/rephase-1-evidence-scaling-repair/test-rejected-draft-20261103T114312Z/test_evidence_scaling_v2.py`
  + `SHA256.txt`: `8d3bec57…`/33543B (matches the implementation packet
  `initial-snapshot-archive-20261103T121216Z/hashes.txt`). Original packet
  evidence untouched.
- Only `tests/test_evidence_scaling_v2.py` was edited; no runtime/config/schema
  or other test/fixture files touched.

## Prior compile side-effect (recorded, removed narrowly)

- An earlier `python3 -m py_compile` of the new test created exactly one file:
  `tests/__pycache__/test_evidence_scaling_v2.cpython-314.pyc`
  (74116B, sha256 `88880545…`). Removed that file only (`rm` on the exact
  path); no other cache touched, nothing else deleted. Current static check
  uses `ast.parse` (no bytecode written); `tests/__pycache__/` verified empty
  afterwards.

## New test IDs (16 honest names, exact single predicates, no alternation)

All tests use ACTUAL existing fixture APIs
(`tests.test_survey_evidence_v2` helper;
`survey_agent_control_v2.validate_agent_state` CAND facade; real PUBLIC
Evidence/LOW/HIGH APIs). Independent temp Git DBs, process-scoped identity,
inert origin, meaningful commits, no `GIT_*` inheritance, no `--allow-empty`,
no object sharing. Synthetic labels honest; no genuine Human decision
fabricated. No `except Exception`/broad-regex alternation; no source-string
tests; no reset/cleanup beyond fixture temp cleanup + planted-fault restore.

1. `test_golden_full_card_public_builder_matches_reviewed_baseline_and_validates_clean`
   — Stored explicit golden (reviewed old-body normalization, 1-task supp
   fixture) vs new PUBLIC `build_research_card_content`; VALID task (stored
   sha == meta, no dict mutation); FULL PUBLIC `validate_evidence_card`
   `== []` incl. Discovery-only control `== []`.
2. `test_unit_private_slices_match_public_authority_map`
   — Labelled UNIT probe only (pure `_discovery/_merge` vs PUBLIC map,
   supplemented + unbound); full Raw closure asserted
   (`entries` == manifest source IDs, `len(raw_refs)` == manifest rows, from
   currently loaded bytes).
3. `test_public_acceptance_readback_real_io_slope_is_package_linear`
   — Real PUBLIC `accept_evidence_results` + `validate_evidence_acceptance`
   vs preserved PUBLIC per-task reload, 4 tasks / 3 supp + 1 unbound;
   instruments ACTUAL `core.sha256_file` only; asserts new < old,
   new ≤ distinct×4, old ≥ distinct×tasks.
4. `test_repo_root_none_structural_nonsupplement_unbound_cases_are_exact`
   — PUBLIC `repo_root=None`: full field-contract error with zero IO;
   non-supplement valid card `[]` with zero IO; supplement package (bound +
   unbound task) full `…source binding requires repository validation context`.
5. `test_lazy_error_order_invalid_card_triggers_no_supplement_io`
   — CARD_KEYS-invalid card fails before supplement getter (getter would raise
   if called); Raw-IO count on supplemented Raws is zero.
6. `test_standalone_two_public_calls_after_raw_change_second_refuses_exact`
   — Two ACTUAL PUBLIC `task_authority_sources` calls; same-size Raw drift →
   exact `Evidence Authority Supplement sources[0] Raw SHA drift`; restore → equal.
7. `test_standalone_two_public_calls_after_manifest_change_second_refuses_exact`
   — Same with manifest `byte_count` edit → exact
   `Evidence Authority Supplement manifest SHA drift`.
8. `test_two_healthy_operations_with_changed_source_metadata_yield_new_values`
   — Two healthy PUBLIC prepare+build+validate+accept with changed Raw bytes
   (rebuilt supplement) → distinct `result_set_sha256`/dirs; both readbacks
   still validate (no global reuse).
9. `test_late_raw_drift_after_context_before_public_accept_refuses_exact_and_preserves_inventory`
   — Valid PUBLIC control first; ctx + first cached card (real), same-size Raw
   fault, real PUBLIC accept → exact indexed `Raw SHA drift`; full
   SHA/mode/type/dir inventory post-fault BEFORE restore (intentional fault
   accounted); pre-first-copy zero new outputs.
10. `test_late_task_mutation_after_load_before_accept_refuses_exact`
    — Task-file mutation after load → exact
    `Evidence Task bytes changed: <id>`; full inventory; pre-first-copy zero
    accepted outputs.
11. `test_post_validation_package_field_drift_refuses_before_first_write`
    — Reseal regression: positive full-valid-card control first; hook CALLS
    the original `validate_evidence_package_basis` then plants a rules-only
    package drift (task bytes + all basis/contract SHAs intact); fixed code
    (pins precede validation) must refuse with exact
    `Evidence package bytes changed` BEFORE first write; task meta SHA
    asserted unchanged; inventory + zero-new-outputs.
12. `test_post_evidence_accept_views_failure_preserves_earlier_absent_later`
    — Evidence accepted (present), then a field-level view fault (valid JSON,
    REAL validator rejects) → exact `Edition Evidence View materiality
    invalid`; full inventory; earlier present, later absent.
13. `test_historical_readback_never_reads_live_state_and_validates_content`
    — History `_validate_evidence_acceptance_content` with true
    root_records/root_path (current-loaded, DATA) and `verify_state_basis`
    must-not-call (AssertionError on LIVE use, no fake pass); validates.
14. `test_readback_result_mutation_after_check_before_return_refuses_exact`
    — Readback freshness: hook CALLS the original per-result checker then
    plants a same-size result drift; pre-RETURN recheck must refuse with the
    exact `bytes changed` pin predicate; full inventory post-fault BEFORE
    restore; restored bytes read back clean. **Gap: depends on the in-progress
    runtime readback task/result pins (finding5); fails honestly until the
    owner lands the pins.**
15. `test_low_derived_copy_build_accept_readback_with_supplement_raw_succeeds`
    — REAL C-helper 1-child DERIVED chain + REAL A2 state/prepare/decide +
    HIGH prepare/adopt/readback (unsupplemented HIGH flow) + direct LOW
    `derive_ordinary_root_effective_context` (R!=E oracle) + COPY pin +
    `check_supersession_record_from_paths` `[]`, PLUS direct LOW public
    `build_revision_cards_views_from_paths` /
    `accept_revision_evidence_views_from_paths` on an ACTUAL supplemented
    revision-package copy (real HIGH package + real supplement manifest via
    real validator; meta SHAs recomputed; schema-valid `source_bindings` in a
    request copy) with the genuine retained COPY/request/DCP/SCP: bulk cards
    cite the exact supp authority (URL/class/role), FULL PUBLIC card
    validator `== []`, accept payloads bind card/view SHAs.
    Pre-existing HIGH producer limitation recorded (not a runtime change):
    HIGH `build_revision_package_from_paths` never carries
    `authority_supplement` and the HIGH request builder sets
    `supplement_manifest: None` with no `source_bindings`, so HIGH
    prepare/adopt cannot thread supplement cards; the direct LOW package-path
    case above verifies the selected lower API without pretending HIGH
    creates it (per §22 disposition).
16. `test_low_copy_and_none_refusals_are_exact`
    — LOW loader `None` refusal is the exact `ResearchAuthorityError`
    `requires request_path and before_copy_path` (not TypeError).

## Readiness / gaps (bounded, no PASS claimed)

- Static: `ast.parse` OK, 16 test methods. Final hash `1c95f675…`/1420 lines
  (attempt history: `a02a38b8` initial fixes → `d626a85c` fixture repairs →
  `1c95f675` two_healthy Raw separation; runtime files never touched).
- F5 dispatch (fresh snapshot `evidence-scaling-fixed-20261103T170019Z`, HEAD
  `4d13640a…` synthetic-fixture-only, NOT ordinary): F5-only green (PID
  3450059); full 16 green (5.5s, per-Raw exactly 12.0 ≤ 16); DM022 readback
  green (PID 3453513). 771-file manifests MATCH pre/post every batch; tree
  clean; no pycache. Report: `notes/rephase-1-evidence-scaling-test-F5-20261103T170019Z/README.md`.
  Views-RETURN pins have no dedicated test (flagged for Root real409 gate).
  **No whole-suite PASS claimed: 15/16 + 1 returned runtime gap.**
- Gaps: readback-RETURN task/result recheck missing in
  `validate_evidence_acceptance` (fails honestly until runtime owner lands it);
  HIGH carries no supplement (recorded limitation; direct LOW package-path case
  proves the lower API instead).
- Prior packet findings respected: Finding4 left unchanged (LOW
  `evidence_acceptance_sha256` is the planned `core.json_bytes` file hash per
  §22 — test 15 does not assert file-SHA equality for it); Finding5 covered by
  tests 12–14; no dead-code/lookup cleanup smuggled in; HIGH limitation
  reported, not papered over.
- Next: root re-review → fixed-snapshot dispatch → affected suites (new
  scaling + old Evidence positive/negative + runner + Profile/DM022) →
  independent implementation review → Human Commit Point. No automatic R4.

- F5 dispatch (`evidence-scaling-fixed-20261103T170019Z`, HEAD `4d13640a…`
  synthetic-fixture-only, NOT ordinary): F5-only 1/1 (PID 3450059), full16
  16/16 (5.5s), DM022 readback 1/1 (PID 3453513). 771 manifests MATCH pre/post;
  tree otherwise clean; no pycache.
- Views-RETURN dispatch (fresh snapshot `evidence-scaling-fixed-20261103T170831Z`,
  HEAD `a6f73314…` synthetic-fixture-only, NOT ordinary; author workcopy
  `409b292…` untouched; `1c95f675` archived): 2 NEW Views-RETURN tests 2/2
  (LIVE + history, exact `Accepted Edition View <id> bytes changed`,
  must-not-call LIVE, full inventories; PID 3482136). Test file `d486809c…`
  = `1c95f675` + TEST-only additions (diff in packet `TEST-ONLY-DIFF.md` for
  later composite onto the real409 clone, which was not touched). 771
  manifests MATCH pre/post; tree otherwise clean; no pycache. No real409.

## Commit-wording qualification (no blanket "no commits")

Prior notes saying "no commits"/"no ordinary commit" are hereby qualified:
isolated SYNTHETIC fixture commits DO exist and are disclosed, none of them
ordinary candidate/reconstruct commits —
(a) one clearly-labelled `SYNTHETIC FIXTURE-ONLY execution snapshot commit`
per fixed snapshot, in its own independent Git DB (inert origin, no
ancestry/shared objects, never pushed, never merged);
(b) per-fixture temp-DB commits inside test runs (process-scoped identity,
meaningful non-empty content, no `--allow-empty`, no `git config` writes),
owned by the test fixtures and discarded with their temp dirs.
Author workcopy ordinary HEAD, the real409 clone, Production, and old
rehearsal/proof commits were never touched.

- Runner-epoch facade dispatch (fresh snapshot `evidence-scaling-fixed-20261103T172903Z`,
  HEAD `4555c301…` synthetic-fixture-only, NOT ordinary; 5e runner + F5 Evidence +
  LOW + tests `1b48169a…` = `1c95f675` + ONE runner test; author workcopy `1c95f675`
  untouched; real409 clone untouched): new test green 1/1 (2.0s, PID 3535980;
  attempt 1 proved PUBLIC run() completes at epoch B and bare standalone readback
  correctly refuses; attempt 2 with facade-mediated readbacks green). Exact
  predicate coverage: facade-wrapped pre-accept/archive `_finish` owners pass at
  B while State/Profile/old bytes and init SHA A hold; old-c9 expectation recorded
  source-based only (no old run, not faked). 771 manifests MATCH pre/post; tree
  otherwise clean (`M tests/…` only); no pycache. No full16 rerun (additive).

- FINAL19 dispatch (fresh snapshot `evidence-scaling-final19-20261103T173758Z`,
  HEAD `e746a5db…` synthetic-fixture-only, NOT ordinary; author workcopy updated
  YES — actual deliverable `tests/test_evidence_scaling_v2.py` = `7b862305…`
  (16 + Views2 + HEAD1 = 19 distinct methods; old-16 behavior byte-identical
  save one landed-F5 docstring line; both branch deltas merged without
  overwriting either). Full 19 run once on the new snapshot: 19/19 ok;
  bindings bind actual final runtime 5e; pre/post 771 MATCH; tree clean at run
  (deliverable committed before execution, no dirty claim); no pycache.
  `final-test-map.json` carries all 19 IDs + sha. Real409 e84 used d486;
  TEST-only diff recorded for careful later composite (other 770 match).
