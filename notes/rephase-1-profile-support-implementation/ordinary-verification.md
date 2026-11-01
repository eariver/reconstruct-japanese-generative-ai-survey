# Ordinary Profile/support verification — General test owner

2026-10-31. New General author/test owner for ordinary scope ONLY (no DM022
HIGH/LOW; DM022 in separate snapshots). Workcopy
`.rephase-1-editorial-runtime/profile-support-implementation-20261031T153148Z/candidate-work`.
Prior A/B source owners finished; D rejected draft archived, not run unreviewed.
No subagents. No apply_patch binary; used specialized edit, disclosed.

Authority (read in full): contract `outputs/rephase-1-profile-support-contract-decision.md`
INCLUDING §7 (FULL `62b14add5e50d7e5f7996c4b7536f95b5d74cdbc9b205b1eec54bde260527e2d`),
contract ROOT §5, precode assessment + packet README, mandatory precode ROOT FULL
`bfb72bf2a82691d26149fd970069d0b43e1f57aad380feeb484774f3011352fa` INCLUDING §7,
R3 mechanics overridden R4→R5, R5 REQUIRED-path hardening, scope reassessment §8,
workstream A/B/C reports with corrections, `astra-implementation-review.md`
INCLUDING rejected D findings + latest 'Initial execution / independent...' disposition
and `independent-early-source-review.md` (B0/B1/B2/B3). No new precode cycle, no generic reader.

## 7. Continued work — B0/B1/B3 + facade + shared helper + real parity (2026-10-31)

Per latest root disposition. Preserves initial 21/24 + 14/14 scopes below as history;
corrects raw failures and static/test claims. No stop/closeout yet.

### 7.1 Repairs in owned scope (no LOW B2 touch)

- **B0 (Screening, critical):** deleted stray `profile,` arg at `resolve_prepackage_root_effective:846`
  so the call binds 9 params (`profile_path`, `profile_sha256`, `marker`,
  `marker_sha256`), not 10. Healthy STAGE_CLAIMED now reachable; mismatched claim
  refuses with the mapped `... does not bind the canonical marker` (not TypeError).
- **B3 (Screening, availability):** `must carry exactly one discovery-acceptance`
  total → exactly-one-role + allow other valid NamedRows + rehash every row's FILE
  SHA (mirror LOW), report-map equality kept. Proves no legitimate old-path skip.
  Extra-row positive in test_20b passes.
- **B1 (Evidence, consistency, no bypass claim):** `prepare_evidence_package:607`
  preflight E `discoveries` → `_screening_basis["records"]` (one coherent resolver
  pair). Qualification preserved: B1 bypass NOT proved — `validate_screening_acceptance:556-564`
  already validates caller path/SHA and returns resolver E, so both sources are
  resolver-derived; the change is consistency, not a bypass proof. No new fetch,
  no caller flag, no historical gate change.
- **Symlink no-follow (Screening, owned):** `_resolve_repo_local_input` per-part
  `os.lstat` + `stat.S_ISLNK` refusal before any resolving call (+ `import stat`).
  Leaf/ancestor symlinks now fail closed; test_21 passes. Preserves B3 all-row rehash.
- LOW B2 (ordinary-vs-DM022 scope) untouched per root (no ordinary 3/5 imposition on DM0227).

### 7.2 Shared helper migration (owned, DM022 depends — root ready hash)

`tests/test_survey_evidence_v2.py` migrated to real committed fixture source /
per-fixture actual HEAD before initialize (no repin of old accepted authority):
`sandbox()` Git init + inert remote + `add -A` + process-scoped `git -c user.*`
commit (never `--allow-empty`, never `git config`); `init_profile()` +
`make_screening/make_evidence/make_views/make_chain` use `core.repository_commit_sha(root)`
per-root identity instead of global `IMPLEMENTATION_SHA="4"*40` (constant retained
for unrelated fixtures still passing fake4; no global monkeypatch). All old real
assertions preserved; no validity-window change. Other fixtures may still use fake4
where passed to core; focused callers migrated, no broad runtime fakeSHA permission.

**Root ready hash for DM022 owner:** `tests/test_survey_evidence_v2.py` 43662B
`ed0155cdf97c1baa8381113e775f232c4641c2f52a3c1f815970f5dbf4c03adc`
(pinned in snapshot 173500Z; workcopy delivery same).

My ordinary fixtures likewise use Git-before-initialize HEAD (no `_repin`);
`_repin_state_to_head` retained as legacy no-op helper only. `_advance_*` helpers
use real agent validation; no fabricated attestation as Stage, no validator stub,
no schema weakening/new authority flag.

### 7.3 Operational facade (strict Stage vs bare DIRECT)

`survey_agent_tool_v2.current_stage_basis_override` (lines 42-50,121-143) installs
strict `agent.validate_agent_state` for actual agent-first Stage Checkpoint States;
`core.verify_state_basis` bare expects legacy machine attestations. Distinct contracts.

- Bare DIRECT preserved for initial cases (test_18 NO_MARKER, test_20 healthy pending
  CANONICAL_MARKER, test_21 symlink/nonregular/unreadable with ISSUE_INITIALIZED):
  no override, bare verification, no Direct fallback on claimed/marker faults.
- Strict Stage facade for DISCOVERY_COLLECTED claimed branches (test_19 marker-missing,
  test_20 mismatched, test_20b healthy + B3 + report): `with agent_tool.current_stage_basis_override():`
  around resolver calls, with real source-committed fixture State/CP/accepted bytes
  (Git HEAD = State implementation, DCP/SCP Stage Checkpoint records + reports +
  marker/acceptance files all real, validated via real agent before resolver).
  Healthy strict control passes before targeted mismatches; early State preemptions
  are not counted as DCP gates (B0 reached when facade works).
- If an actual shipping caller cannot use the correct facade, return its exact
  route/predicate (not done here — ordinary callers use the facade above; no
  inferred blocker from fabricated State).

### 7.4 Real public parity + named5→7/Selection + all3 profiles (test_16 probe kept honest)

- `test_16` docstring corrected to “Delegation unit probe (NOT real public parity)”;
  mock `runner.main` return0 kept only as delegation probe, not parity proof.
- New `test_16c` real public parity (THEMATIC, named O-NEW): two independent dirs
  cloned via copytree including .git (same HEAD, same bytes); direct public
  `runner.run` vs agent-first real public `adapter.main` CLI (mocked sys.argv only
  for CLI harness, no runtime/authority mock); equivalent accepted canonical inputs;
  exact outputs compare (evidence/view/ledger/completeness relative paths, counts,
  statuses) + exact limitations `["residual-A","residual-B"]` (closure-first) +
  7-field `discovery_ids`/`evidence_task_ids` (named5→7) + Selection refs
  (ledger + completeness exist, `validate_completeness` == [], issue_id binds).
  No mocked main return, no fake builder.
- `test_14` (THEMATIC KEEP+DROP, DROP-safe, full validators) + new `test_14b`
  (WEEKLY + RETROSPECTIVE_PERIOD KEEP, profile-specific record shapes/annotations,
  closure None, same builders/validators/Selection refs) together cover normal
  named5→accepted7 + Selection consumption for all3 real upstream Profiles via
  operation (not only factory+validator loops in test_11/12/15).

### 7.5 Fixed snapshot + runs (unique command/env/PID/exit, no overwrite)

- Delivery workcopy pins (current, ordinary ownership):
  Screening 82277B `f0f289540302753b2e7cad5f4fded1df0387ca1403309aa032a42d5a1`,
  Evidence 130152B `36b7b5832845ea8a984c69a3097f9846976805c556679ed980b0148fdf454736`,
  shared helper 43662B `ed0155cdf97c1baa8381113e775f232c4641c2f52a3c1f815970f5dbf4c03adc`,
  ordinary tests 77890B+ (with 14b/16c; hash in snapshot 173500Z `d9b590bce9a3…` pre-16c? final hash to be repinned on closeout — behavior bound by snapshot runs below).
- Execution snapshot: `.rephase-1-editorial-runtime/profile-support-ordinary-20261031T173500Z/snapshot-work`
  (769 files, HEAD `409b292…`, shallow `774dd39…`, inert origin, no alternates, no GIT_* env,
  distinct inodes, no pyc; runtime pins same as workcopy at snapshot time).
- Focused first (3 failures + control + public pair, PID 2434170, EXIT 0, 6/6):
  test_19 + test_20 + test_20b (STAGE with strict facade, B0/B3 fixed) + test_18
  (bare DIRECT control) + test_16 (probe) + test_16c (real parity) — all pass.
- Full ordinary: PID 2434619, EXIT 0, **26/26 pass** (24 prior + test_14b + test_16c;
  preserves initial 21/24 scope as history, now 26/26 with B0/B1/B3 + facade + new tests).
- Affected existing: PID 2435750, EXIT 0, **26/26 pass**
  (`test_survey_evidence_v2` 12 + `test_run_evidence_v2_interactive` 8 +
  `test_run_evidence_v2_agent_first` 4 + `test_survey_evidence_source_class_regression` 2;
  preserves initial 14/14 scope as history for the 14 non-shared-helper tests; shared-helper
  migration keeps all 12 old assertions green with real HEADs).
- Raw logs: `notes/rephase-1-profile-support-implementation/ordinary-verification-20261031T173500Z/logs/`
  (new per-run stdout/stderr/command/env/PID/exit; no overwrites; no saved-runner execution;
  no git clean/reset/cache/raw deletion; fixture cleanup via addCleanup only).
  Tool deviation retained: no apply_patch binary; specialized edits, disclosed.

### 7.6 Remaining gaps (no whole PASS, no independent approval)

- Producer-mismatch DCP negative inherently preempted by strict State validation
  (from/to change breaks Stage Checkpoint schema/producer for both State and DCP);
  not counted as DCP gate per root (don't count preemptions). Covered instead by
  B3 extra-row positive + report-contract mismatch with State kept valid
  (record review SHA + State SHA rebinding so failure is contract, not SHA drift).
- Full `runner.run` parity proven for THEMATIC (representative, closure-first);
  WEEKLY/RETRO full-run parity not repeated (same thin-delegation path, profile-agnostic;
  all3 covered via operation builders + validators in test_14/14b/15). No suite-count decoration.
- DM022 HIGH/LOW in separate snapshots (untouched here; shared-helper ready hash above
  for integrator). Independent implementation review, quality/adoption/savings OPEN.
  Running children: none.

## 8. DERIVED R!=E genuine operation + raw-evidence closeout (2026-10-31, frozen)

No source edits unless necessary actual defect (B0/B1/B3/symlink already landed in §7;
no LOW B2 touch; C untouched). Preserve root/independent errors as history (§6, §7.6,
independent §§1-8). Existing no-Git-readback/network/ordinary-commit/source-proof boundaries.

### 8.1 Raw-insufficiency qualification (append, originals preserved)

`ordinary-verification-20261031T173500Z/logs/{focused,full-ordinary,affected}-173500Z-stdout-stderr-exit.txt`
are 7–8-line summaries (command/workdir/env/PID/EXIT + one-line scope), NOT captured
verbose `unittest -v` streams. Do NOT reconstruct stdout or claim raw 26/26 preserved
there. Originals preserved; see `.../173500Z/logs/QUALIFICATION-raw-insufficiency.md`
(append-only). Final binding requires verbose raw (this §8 provides it ONLY for the new
focused DERIVED positives/negatives; full-suite verbose re-run is for the separate
final-evidence worker after freeze — no broad 26/26 re-decoration here).

### 8.2 ONE genuine DERIVED R!=E operation (THEMATIC, shared OID, many-to-many)

New `DerivedOperationTests` in `tests/test_profile_support_upstream_repair_v2.py`
(frozen pin §8.5):

- Root BASE multiDID/sharedOID: R-1/R-2, both `["O-SHARED"]`, BASE, same
  sourceidentity (`paper/test-collector/run-001/https://example.invalid/shared`),
  same Rawunion (`raw/source.json` exists), same headers (`schema_version 2.0-rc1`,
  issue SP001). Root file `discovery-root.jsonl` ONLY for acceptance (never reaccept
  E as root; vocabulary differs Screening derived rawIDs — rootDiscovery normalized local).
- Effective distinct children: C-1 parent R-1 O-SHARED, C-2 parent R-2 O-SHARED
  (healthy) vs C-2 EMPTY (lossy, `(R-2,O-SHARED)` uncovered), REFERENCE_EXPANSION,
  research_pass 1, same sourceidentity/Rawunion/headers as roots (so old expansion
  passes for both; new gate distinguishes).
- Root acceptance (Discovery acceptance via real `build_acceptance` + X NOT_REQUIRED
  + `validate_acceptance` on root JSONL) + E screening package/acceptance (real
  `prepare_package` (prepackage true R/E + `check_new_operation_admission` before
  first write) + `accept_results` (idempotent re-read then loss gate before copy2)).
  True context from real resolver: `resolve_prepackage_root_effective` (marker +
  supplied derived → `CANONICAL_MARKER`/`DERIVED_EXPANSION`) + `resolve_effective_discovery_basis`
  (package → same R/E), R!=E asserted (`{R-1,R-2}` vs `{C-1,C-2}`), U via
  `compute_obligation_universe`, bindings via `derive_bindings` (healthy DIDs
  `[C-1,C-2]` + Ledger tasks; profile-only `([],[])` in unit probes).
- Ordinary named5→derived7: initial 3-field (scope:01/02) + O-SHARED 5-field
  (Profile-declared `lineage`, non-empty description) → `_build_completeness`
  derives 7-field `discovery_ids`/`evidence_task_ids` from effective + exact Ledger
  rows (DROP yields none in test_14; DERIVED KEEP×2 yields 2 tasks here), full
  validators (`validate_discovery_set`, `validate_discovery_expansion`,
  `validate_screening_acceptance`, `validate_evidence_package_basis`,
  `validate_evidence_card == []`, `validate_completeness == []`,
  `validate_materiality_ledger` via completeness).
- Actual Selection consumption (not path.exists): exact existing API
  `survey_architecture_v2.derive_candidate_matrix(root, profile_path, eff_jsonl,
  screening_acceptance, evidence_acceptance, views_acceptance, ledger_path,
  completeness_path, head)` + `write_candidate_matrix` + minimal selection binding
  all matrix rows + `validate_selection(...) == []` (uses existing consumer test
  support pattern from `test_survey_architecture_v2.py`, no new engine).
- Healthy (`test_23`) many-to-many passes with internally derived bindings;
  lossy (`test_24`) with valid old expansion (`validate_discovery_expansion` passes:
  empty subset, accounted R-1/R-2, same Raw file, same headers) refuses NEW
  `prepare_package` with `DECLARATION_LOSS` before first write + full byte/mode/dir +
  hash inventory (no post-repair equality). Never reaccepts E as root.

Contract: canonical10 preserved, unknown incl DROP still pre-write refused (test_05/06),
U = P∪named(R)∪named(E), every (parent,OID) via real parent_refs, no autofill/drop/child
rewrite, HIGH never ordinary 3/5, closure-first residual union, G76 memberships unchanged.
Independent §9.5(2) controls satisfied: healthy DERIVED green + lossy NEW-prewrite refusal
with inventory, resolver R!=E (not E-as-root), no E reacceptance.

### 8.3 Caller census closeout (final source, exact keys/API/affected modules)

Final workcopy (frozen pins §8.5, C present but untouched):

- Required keyword-only R/E (`run_evidence_v2_interactive.py:218/314`):
  `_validate_completeness_input(value, profile, *, discovery_records, root_discovery_records)`,
  `validate_interactive_input(value, profile, expected_ids, task_source_ids=None, *, discovery_records, root_discovery_records)`;
  both REQUIRED (no default, TypeError on omission, no E-as-R). Callers:
  `run():746/776` (early `_validate` + late `validate` with true `root_records` from
  `resolve_effective_discovery_basis:722-739`, explicit `root_records` presence + non-empty
  checks, no `.get(...,fallback)`); tests forward keywords (`test_run_evidence_v2_interactive:120-127`,
  new-module all `_validate` calls with keywords). Weekly/Special wrappers do NOT call
  these validators (legacy v1 compact paths, untouched). No other prod callers.
- Universe/loss/bindings/admission (Screening single home, Evidence consumes):
  `compute_obligation_universe(P,R,E)`, `find_declaration_loss(R,E)->sorted[(parent,OID)]`,
  `derive_bindings(oid,E,ledger_map)->(DIDs,task_ids)`, `check_new_operation_admission(R,E)`,
  `_preflight_new_evidence_admission(R,E)` (Evidence, consistent pair per B1 fix),
  `resolve_prepackage_root_effective(repo_root,state_path,discovery_path,accepted_discovery_path)`
  PATH-only (R4/R5, `None` = no extra expectation, never suppresses marker). NEW-branch sites:
  Screening `prepare:1136-1137` + `accept:1590-1591`, Evidence `prepare:612` + `accept:1257` +
  `views:1942` (all consistent R/E pairs, after idempotent re-reads, before first writes);
  HIGH `prepare:544-568` + `adopt:1172-1197` (seven-field only, before first COPY / before proof).
  Runner `run:246/254/565` consumes `compute/loss/derive`; `_build_completeness` tuple kept.
  Agent-first `main:79-85` thin `return runner.main()`, pure helpers retained, no monkey-patch.
  No top-level Screening↔Evidence cycle (Evidence/Screening/Discovery/schema leaves function-local).
- Stage facade (operational, not permission token):
  `agent_tool.current_stage_basis_override()` in shipping `run_evidence_v2_interactive:755/802/835/858/888`,
  `run_screening_v2_interactive:163/199`, `run_selection_architecture_v2_interactive:309/432`;
  tests mirror split (bare DIRECT for 18/healthy-pending/symlink/dir/unreadable/control; strict
  override for 19/20/20b + 16c + DERIVED healthy (bare ISSUE_INITIALIZED, no claim needed for
  DERIVED CANONICAL_MARKER — strict only where State is DISCOVERY_COLLECTED/CANDIDATES_NORMALIZED)).
- Selection/Architecture downstream (exact API, ordinary scope):
  `survey_architecture_v2.derive_candidate_matrix(...)` + `write_candidate_matrix` +
  `validate_selection(...)` (via `survey_architecture_v2_base.validate_selection`);
  consumed in new test_23 (THEMATIC DERIVED, 2 tasks, 2 DIDs, closure-first). No new engine.
- Affected modules: owned A/B (`survey_evidence_v2`, `survey_screening_v2`,
  `run_evidence_v2_interactive`, `run_evidence_v2_agent_first`) + owned tests
  (`test_profile_support_upstream_repair_v2`, `test_survey_evidence_v2` shared helper,
  `test_run_evidence_v2_interactive` migrated). No C (LOW/HIGH/dm022 fixtures) edits.
  Schemas/config/old source untouched. Full `grep` transcripts are in the frozen
  snapshot shell history, not re-pasted here to avoid transcription drift; the exact
  keys/APIs above are the census result on the frozen pins below.

### 8.4 Focused raw (ONLY new DERIVED, direct capture, no hand summaries)

Snapshot: `.rephase-1-editorial-runtime/profile-support-ordinary-20261031T175500Z/snapshot-work`
(769 files, HEAD `409b292…`, shallow `774dd39…`, inert origin, no alternates, no GIT_* env,
distinct inodes, no pyc; pins §8.5). No source/test edits during runs; fixtures isolated
temp dirs, `addCleanup` only; no git clean/reset/cache/raw deletion; no network/Production/
ordinary commit/source-proof mutation.

- Command: `bash -c 'echo RUN_PID:$$; echo CMD: env PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -m unittest tests.test_profile_support_upstream_repair_v2.DerivedOperationTests -v 2>&1; exec env PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -m unittest tests.test_profile_support_upstream_repair_v2.DerivedOperationTests -v 2>&1'` + `echo EXIT:$?`
  Workdir: above snapshot-work. Env: `PYTHONDONTWRITEBYTECODE=1`, `/usr/bin/python3` 3.14.4,
  existing jsonschema/pypdf, no installs. PID 2519086 (echoed RUN_PID, exec preserves python PID). EXIT 0.
- BEFORE/AFTER pins (snapshot-work, owned files): Screening 82277 `f0f28954…`, Evidence 130152 `36b7b583d…`,
  shared helper 43662 `ed0155cd…`, ordinary tests 115763 `926e2e0a…` — unchanged (fixtures temp only).
- STDOUT/STDERR (exact tool-output archival, combined `2>&1`, per-test verbose, no summary):
  ```
  RUN_PID:2519086
  CMD: env PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -m unittest tests.test_profile_support_upstream_repair_v2.DerivedOperationTests -v
  test_23_healthy_derived_many_to_many_named5_to_7_with_selection (tests.test_profile_support_upstream_repair_v2.DerivedOperationTests.test_23_healthy_derived_many_to_many_named5_to_7_with_selection)
  Genuine DERIVED R!=E public operation (THEMATIC, shared OID, many-to-many). ... ok
  test_24_lossy_derived_shared_oid_refuses_new_prewrite_with_full_inventory (tests.test_profile_support_upstream_repair_v2.DerivedOperationTests.test_24_lossy_derived_shared_oid_refuses_new_prewrite_with_full_inventory)
  Lossy DERIVED (R-2,O-SHARED) with valid old expansion refuses NEW prewrite. ... ok

  ----------------------------------------------------------------------
  Ran 2 tests in 0.676s

  OK
  EXIT:0
  ```
  Saved verbatim (no hand-summarized “raw”) to
  `notes/.../ordinary-verification-20261031T175500Z/logs/derived-175500Z-{stdout-stderr,command,env,pid,exit,pins-before,pins-after}.txt`
  (7 exclusive files). If no actual streams existed we would disclose; here they do —
  no manufacture, no reconstruction of 173500Z summaries.
- Test IDs for final-evidence owner:
  `tests.test_profile_support_upstream_repair_v2.DerivedOperationTests.test_23_healthy_derived_many_to_many_named5_to_7_with_selection`,
  `...test_24_lossy_derived_shared_oid_refuses_new_prewrite_with_full_inventory`;
  path `tests/test_profile_support_upstream_repair_v2.py` 115763B `926e2e0a0ee2f7104ed5c92d7bbdd50ef3610b2d7f6fd542c51a5bcb597632d6`;
  output paths above (genuine run, EXIT 0, 2/2). Frozen — no further ordinary edits pending final-evidence run.

### 8.5 Frozen pins + no whole PASS

Workcopy delivery (frozen, ordinary ownership):
Screening 82277 `f0f289540302753b2e7cad5f4fded1df0387ca1403309aa032a42d5a1`,
Evidence 130152 `36b7b5832845ea8a984c69a3097f9846976805c556679ed980b0148fdf454736`,
runner 45084 `5a6280ac19986a05e363a673dd57294ed6d4257355fdb888d9cdd9466fe5d812`,
agent-first 3684 `f73f2ab91fc88a794d4f734d0952e80edff438259d3ad2315001df60b8d61910`,
shared helper 43662 `ed0155cdf97c1baa8381113e775f232c4641c2f52a3c1f815970f5dbf4c03adc`
(ready hash for DM022 owner, §7.2),
ordinary tests 115763 `926e2e0a0ee2f7104ed5c92d7bbdd50ef3610b2d7f6fd542c51a5bcb597632d6`.
No C/schema/config edits. New tests: test_14b (WEEKLY/RETRO named5→7), test_16c (real parity),
test_23/24 (DERIVED R!=E + Selection). Preserved: initial 21/24 + 14/14 scopes (§4-6 as history),
intermediate 26/26 + 26/26 (§7 as history with raw-summary qualification §8.1).
Remaining: full-suite verbose re-run by separate final-evidence worker; DM022 HIGH/LOW,
independent final review, quality/adoption/savings OPEN. Running children: none.
No whole PASS, no independent approval.

## 1. Delivery pins (workcopy, ordinary ownership — initial 2026-10-31, preserved as history)

Workcopy is the delivery; snapshots are execution only. No ordinary
candidate/reconstruct commits; fixture commits only in isolated temp DBs.

- `scripts/survey_evidence_v2.py` 129758B `174c04cf37ca77f4394c9c7e2bcca9bc05c4c68aeccf0788df964249187fdc88` (unchanged from A correction)
- `scripts/survey_screening_v2.py` 81888B `7cc1fe4d229bab6cf6be646636e49470ca2427008f28fe433a4500ba87893d3b` (A correction `45e93e…` + my `import stat` + symlink no-follow hardening, see §5)
- `scripts/run_evidence_v2_interactive.py` 45084B `5a6280ac19986a05e363a673dd57294ed6d4257355fdb888d9cdd9466fe5d812` (B correction, unchanged)
- `scripts/run_evidence_v2_agent_first.py` 3684B `f73f2ab91fc88a794d4f734d0952e80edff438259d3ad2315001df60b8d61910` (B, unchanged)
- `tests/test_profile_support_upstream_repair_v2.py` 75238B `78c6d102e0b5d1b541d0754118cc11903e61559fc73571f2ce4a51faebfbc598` (REPLACED rejected draft `c4838e…`/46647B, archived already)
- `tests/test_run_evidence_v2_interactive.py` 7721B `9d668bae9aca7437dc05a21c17724f50407b8e2c338bbc5fdf123909f50eb0e3` (D migration, unchanged by me, still passes)

DM022 files untouched (another integrator handles). No schema/config/old-source/proof edits. New testfile allowed; no new shipping module/schema/family.

Tool deviation: `apply_patch` CLI/binary absent (`which apply_patch` not found, consistent with A/B/D). All edits via specialized exact-string edit, one hunk at a time, disclosed here, not recast as apply_patch execution.

## 2. Fixed execution snapshots (ignored, independent DBs)

- Intended workcopy: `.rephase-1-editorial-runtime/profile-support-implementation-20261031T153148Z/candidate-work` (769 files excl .git after D +1 test; 768 manifest +1 new test; no pyc; HEAD `409b292…`, shallow `774dd39…`, origin inert `example.invalid`, no alternates, no GIT_* env, distinct inodes, nlink 1/1).
- Ordinary snapshot for final runs: `.rephase-1-editorial-runtime/profile-support-ordinary-20261031T170000Z/snapshot-work` (769 files, same pins as workcopy above, HEAD/shallow/origin verified, no pyc, distinct inodes). Earlier snapshots `…162500Z` (pre-replacement), `…163500Z` (first corrected tests), `…164500Z` (repin/raw fixes), `…165000Z` (canonical-path + stat-missing failure) preserved as history; only `170000Z` is the fixed CURRENT evidence snapshot.
- Raw logs: `notes/rephase-1-profile-support-implementation/ordinary-verification-20261031T170000Z/logs/` (new per-run stdout/stderr/command/env/PID/exit; no overwrites; no old saved runners executed; no git clean/reset/cache/raw deletion). Bash tool captures PID via `echo RUN_PID:$$; exec …` so the echoed PID is the Python PID (exec replaces shell). `PYTHONDONTWRITEBYTECODE=1`, `/usr/bin/python3` 3.14.4, existing jsonschema/pypdf, no installs/network. No builds (no affected need). Fixture cleanup via `addCleanup(temp.cleanup)` only; critical acceptance/manifests/raw compared before cleanup via byte/mode inventory, not archived wholesale.

## 3. True tests vs helper probes (honest labels)

New module `tests/test_profile_support_upstream_repair_v2.py` (24 tests, ordinary only, no DM022):

- Unit probes (pure helpers, no fixtures, honestly labelled “Unit probe” in docstrings, NOT operation/authority proof):
  `test_01` canonical10 leaf, `test_02` old-sample leaf, `test_04` unknown leaf,
  `test_05` pure preflight unknown/DROP, `test_07` U, `test_08` shared-OID loss,
  `test_09` carriers, `test_10` derive_bindings, `test_11/12/13` validator shapes with REAL profile factories, `test_16b` keyword-only census.
- Operations (real fixtures, real validators/loaders/builders, exact error regex + byte/mode/directory no-write inventory, valid controls):
  `test_03` 10-type task/card (see §4), `test_06` Screening prepare unknown (with known-type control that prepares cleanly),
  `test_14` builder via real chain/Ledger + full `validate_completeness` == [],
  `test_15` all three REAL factories (weekly/thematic/period, no relabel),
  `test_16` real builder through public adapter helper (not fake) + behavioral thin-delegation mock (no source grep),
  `test_17` healthy historical `validate_discovery_expansion` passes while new admission refuses same lossy graph (behavioral separation, no source-text check),
  `test_18` initial DIRECT (NO_MARKER/DIRECT, root==records, no-write),
  `test_19/20/20b` STAGE_CLAIMED family — BLOCKED (see §6),
  `test_21` symlink/nonregular/unreadable (controlled PermissionError mock only, no authority bypass, no-write),
  `test_22` prepare guard + accept idempotence (second prepare refuses, second accept returns same path with no-write).

Rejected flaws corrected: zero-error card assertions (== []), genuine tasks (file SHA == meta SHA, no mutated hash), real Retro factory (`period_profile`, not relabelled Weekly), real builder (not `_fake_original`), no source-text checks (`inspect.getsource` removed; delegation via mock, history separation via behavior), State-claim mismatch via State DCP (not foreign expected path), byte/mode/directory inventories (not filename-only), verified helper names (AST + runtime), process-scoped Git (`git -c user.*` + env, never `git config`), no DM022 tests in this file.

## 4. Oracle scopes (what passed)

Final fixed snapshot `170000Z`, `PYTHONDONTWRITEBYTECODE=1`:

- `tests.test_profile_support_upstream_repair_v2` (ordinary only): 21/24 pass (PIDs 2374829/2375972 runs; EXIT 1 due to 3 STAGE_CLAIMED blocks, see §6). Passing oracles:
  canonical10 task/card zero-error + mismatch refusal (10 genuine tasks, file SHA == meta SHA), old-sample preservation, unknown/DROP pure + write-boundary no-write (with control), U/3-5/dimension/status/coverage with real profiles, builder Ledger/DROP + full validators, three real Profiles, direct/agent-first real parity (closure-first `["residual-A","residual-B"]`, byte-equal, mock delegation), history-vs-new behavioral separation, initial DIRECT, symlink/nonregular/unreadable no-write, guard/idempotence.
- Affected existing: `tests.test_run_evidence_v2_interactive` (8/8) + `tests.test_run_evidence_v2_agent_first` (4/4) + `tests.test_survey_evidence_source_class_regression` (2/2) = 14/14 pass (PID 2375972, EXIT 0). No unbounded old-suite repetition.
- Known affected regression (not run as PASS): `tests.test_survey_evidence_v2` and other Screening/Evidence suites that use `"4"*40` without Git now correctly fail at `resolve_prepackage_root_effective` (`cannot resolve implementation commit`) after A’s CURRENT-proof gate. This is expected test-migration debt (fixtures need Git + HEAD repin, as my new tests do), not a source defect to weaken. Returned to integrator/root; no weakening, no old-PASS transfer.

Caller census (behavioral + grep, documented here, not as test PASS):
`compute_obligation_universe`/`find_declaration_loss`/`derive_bindings`/`check_new_operation_admission`/`_preflight_new_evidence_admission`/`resolve_prepackage_root_effective` present with exact precode names; runner requires keyword-only `discovery_records`/`root_discovery_records` (no default, TypeError on omission, no E-as-R); runner dead mapper removed; Evidence canonical10 present; DM022 files reference `find_declaration_loss` via true R/E (C ownership, not edited here). No missing dependency for ordinary scope.

## 5. Source repair within owned scope (defect found by meaningful test)

`test_21` symlink initially did NOT refuse (ValueError not raised). Root cause: `survey_screening_v2._resolve_repo_local_input` claimed per-part no-follow hardening but called `_repo_file` via `core.repo_local_path(...).resolve()`, which follows leaf symlinks, so a symlinked marker resolved to its target and passed as CANONICAL_MARKER. This weakens the contract’s symlink/nonregular/unreadable gate.

Fix (Screening only, no new policy, matches documented map): add `import stat` + per-part `os.lstat` walk in `_resolve_repo_local_input` that refuses `S_ISLNK` before any resolving call. Ancestor + leaf symlinks now fail closed with `must not traverse symlinked path`; nonregular still refused via `_repo_file`; unreadable still refused via no-follow open probe. After fix, `test_21` passes (symlink/nonregular/unreadable all refuse with no-write). Pins: Screening `81888B 7cc1fe4d…` (was `45e93e…` +33 lines). No other runtime files changed. Independent implementation review still open; no whole PASS claimed.

## 6. Exact real contract gap — STAGE_CLAIMED family BLOCKED (stop, no broadening)

`test_19` (marker-missing refusal), `test_20` (mismatched State DCP vs VALID marker), `test_20b` (healthy STAGE_CLAIMED + producer/report roles) fail at `verify_state_basis` with `checkpoint attestation fields invalid: discovery` (PIDs 2374829/2373083 runs; saved failures, new snapshots retested, still blocked).

Cause: production State validation (`validate_state_semantics` via `_validate_checkpoint_attestation`) requires `checkpoint_provenance.discovery` to be an ATTESTATION (`{checkpoint,action_id,…}` at canonical `orchestration/v2/attestations/discovery.json`), while prepackage STAGE_CLAIMED (`_validate_prepackage_dcp_claim`) requires the SAME field to be a LEGACY DCP stage-checkpoint (`{from_state,to_state,checkpoints,artifacts,reviews,…}`). A State that satisfies one schema cannot satisfy the other. My fixtures put a valid LEGACY DCP record at the canonical attestation path (so the path is canonical), but the content still fails attestation-field validation before the resolver’s DCP logic runs. Using `transition_state` or manual DISCOVERY_COLLECTED construction cannot satisfy both; DM022 helpers pass only `validate_agent_state` (different predicate), not production `verify_state_basis` used by the prepackage resolver.

This is a cross-file contract/dependency contradiction (Screening prepackage DCP authority vs Production State attestation authority), not a test-setup fault (raw files, HEAD repin, history, checkpoints, next_action all made production-valid; only the attestation-vs-stage-checkpoint content clash remains). Per dispatch, I stop and return this exact gap to integrator/root before broadening: either the DCP claim must live in a separate State field (new contract — separate investment, not selected), or State validation must accept LEGACY DCP provenance for DISCOVERY_COLLECTED (weakening — not done), or STAGE_CLAIMED must be re-scoped. No new policy added, no weakening, no fake pass. The three tests remain as failing evidence of the gap; all other ordinary oracles above pass.

Other limits: TeX absent (no real-build verification needed here); partialDB/missing26309/bulk31466/runtimeTeX inherited; 55 Gitlinks/child dirt preserved; no full133/768/inode recertification; no Human approval synthesized; no reconstruct status/HEAD/log/readback, Production/extra intake/rebaseline; baseline774 unchanged. Running children: none (all fixture temp dirs cleaned via addCleanup; no long processes left).

Return: 21/24 ordinary pass, 3 blocked by the attestation-vs-DCP gap; 14/14 affected existing pass; one owned source repair (symlink no-follow + stat import); no whole PASS or independent approval.
