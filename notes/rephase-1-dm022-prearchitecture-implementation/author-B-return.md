# DM022 implementation — Author B return (ordinary consumers)

2026-10-28. Owner B (12 assigned files + B tests). Human continued after
precode Commit/Push; no Human commit readback performed here. This unit is
implementation only; no implementation completion, adoption, or approval is
claimed. Whole NOT_READY / DM021+022 OPEN preserved until independent
implementation review + frozen integration snapshot + witnesses.

Working source: `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`
(original final93 proof-copy untouched). Binding map: decision `a345…`
INCLUDING §11, precode ROOT full `0425c530…`/13788B INCLUDING §5, R4 40 rows +
5 literal schemas, R5 families, R6 17-site roles, R3 retained mechanics; R4
overrides R3, R6 narrows R5 publication chain, ROOT is final.

## 1. Files actually changed (B ownership only)

All paths relative to `candidate-work`. No cross-owner file edited.

- `scripts/survey_agent_control_v2.py` — R4 rows 1–4, 20, 39, 40; R6 sites
  1–9; strict LIVE State predicates retained + precise PREARCH branch.
- `scripts/run_selection_architecture_v2_interactive.py` — R4 row 7; entry +
  prepublish READY; 7-slot audit incl audit; R4 ledger/completeness; caller
  input vs generated archive provenance.
- `scripts/run_evidence_v2_interactive.py` — R4 row 8; entry + prepublish
  READY; canonical Ledger/Completeness creation while guard held refuses;
  versioned R outputs HIGH-only.
- `scripts/run_drafting_synthesis_v2_interactive.py` — R4 row 9; entry +
  prepublish READY; ledger/completeness/matrix/selection via R4; 70–73 binds
  vs R4 bytes; refuse if R4 unavailable post-adoption.
- `scripts/survey_drafting_v2.py` — R4 row 10; NEW optional
  `evidence_ref/matrix_ref` signature; versioned R4 refs (same SHA + parsed
  equality); stale-matrix canonical read refuses; frozen validator strict.
- `scripts/survey_drafting_v2_base.py` — R4 row 11; pure loader stays
  guard-free; callers pass R4 paths; `_content` never `verify_state_basis`.
- `scripts/survey_handlers_v2.py` — R4 row 12; `_evidence_basis` gains
  optional `cfg` + R4 handoff binding; `_selection_basis` threads `cfg`;
  `validate_*` pass `cfg`; superseded-mode refuse if R4 absent; zero handoff
  bytes written on refuse.
- `scripts/survey_stage_validation_v2.py` — R4 rows 13–15; READY at
  `validate_stage` entry + prepublish; `_dm022_verify_current_r4` enforces
  CANDIDATES_NORMALIZED current = 4 R refs when PREARCH; `_prior_artifacts`
  same-wrapper note; `REQUIRED_CURRENT` names unchanged; historical retained
  validation stays guard-free (detached proof rule).
- `scripts/survey_orchestrator_v2.py` — R4 row 16; READY entry + prepublish;
  PREARCH via advance/transition always refuses (HIGH single-file switch only).
- `scripts/survey_core_execution_bridge_v2.py` — R4 row 17; READY entry;
  bridge advance refuses PREARCH.
- `scripts/survey_human_gate_v2.py` — R4 rows 18–19; `_current_pending_gate`
  stays diagnosis guard-free; presentation/invalidation add READY; no
  manufactured Gate at bare `EVIDENCE_REVIEWED` (existing pending-Gate
  predicates enforce); genuine-Human-only paths unchanged.
- `scripts/survey_architecture_v2_base.py` — R4 row 32; pure derivation stays
  guard-free; callers pass R4 paths; entry enforces G + R4.
- `tests/test_dm022_prearch_b_ordinary_consumers_v2.py` (NEW, B-owned) —
  12 meaningful cases: discriminator, content branch, triplet, 7-slot exact +
  audit overwrite/symlink, guard entry + late seam zero-writes, LOW-missing
  explicit blocker, core-proof branch accept/mixed-refuse, handlers R4 bind,
  stage CURRENT names, drafting R4 missing-refuse. No shallow mirrors.

Existing B-corresponding tests untouched. C1/C2 files, A files, schemas,
config, shared fixture helpers untouched.

## 2. APIs required (pending A reconcile) vs actually implemented

Required from A (not created here; B allows pending, no concealing fallback):

- LOW `scripts/survey_research_authority_v2.py`:
  `resolve_research_authority(repo_root, state_path)`,
  `load_typed_checkpoint_record(repo_root, path) -> {family, record}`,
  `_resolve_research_from_state_bytes(repo_root, structural)`,
  `_load_typed_four_refs(repo_root, structural)`,
  `require_research_operation_ready(repo_root, state_path)`,
  `require_no_active_guard(source_root)`,
  `require_completion_consistent(source_root, checkpoint_ref)`,
  `guard_path_for(source_root)`, `lstat_slot(source_root, rel)`,
  `check_supersession_record_from_paths(...)`.
- HIGH `scripts/survey_prearchitecture_acceptance_v2.py` (sole mutator):
  `prepare/adopt/resume/readback_revision`, `verify_live_eligibility`,
  `claim_guard/write_checkpoint_as_planned/replace_state_triplet/`
  `clear_remaining_exact_slots/write_cleanup_completion/release_guard`.
- Five `schemas/dm022-*.schema.json` (installed `schemas/` paths).
- Existing `survey_evidence_v2` / `survey_screening_v2` /
  `survey_completeness_v2` pure `_content` cores (A-owned, consumed
  function-locally only; no predicate weakened).

Actually implemented in B (this return):

- `agent._is_prearchitecture_record`, `_validate_prearchitecture_record_content`,
  `_validate_prearchitecture_core_proof`, `_dm022_state_kind`,
  `_require_dm022_ready`, `_require_no_dm022_guard_by_root`,
  `_resolve_prearchitecture_artifact`, `resolve_active_research_four_refs`
  (extends `resolve_active_evidence_views` with 4-ref same-record, View→Evidence
  binding, live re-hash, no old canonical fallback).
- `_validate_checkpoint_record` PREARCH dispatch via LOW typed loader with
  legacy strict path preserved; PREARCH at legacy schema path refuses
  `DM022_WRONG_FAMILY`; triplet same-record + proof enforced.
- `_validate_core_stage_report` new-kind branch: sole
  `DM022_SUPERSESSION_PROOF` + artifact-set check; old `CORE_STAGE_CONTRACT`
  lifecycle match retained for legacy; mixed refuses.
- `_resolve_checkpoint_artifact` role gate: validation/freeze/release/
  selection PREARCH refuses; upstream 3 roles + 4 names dispatch to typed path.
- `build_stage_checkpoint` READY + PREARCH-via-forward refuses (producer NONE).
- `advance_with_checkpoint` READY + PREARCH-via-advance refuses + raw-bytes
  probe when LOW unavailable.
- `approve_architecture` READY (G released before approval; active PREARCH
  additionally needs completion via LOW READY).
- Runners/handlers/validators/orchestrator/bridge/gate READY helpers +
  `_dm022_is_prearch`, `_dm022_preflight_seven` (all-7 incl audit, lstat
  symlink-safe), `_dm022_resolve_ledger_completeness`,
  `_dm022_verify_handoff_four_refs`, `_dm022_verify_current_r4` as above.
- Full HIGH public `agent.validate_agent_state` preserved (no weakening;
  `production.verify_state_basis` never substituted); LOW never does
  current-State recursion; `NoStateArg` writers derive canonical State via
  Profile or refuse; no `skip`/`owner` guard params; new family readback
  survives later LIVE stages, original entry window via retained context only;
  publication `_record_kind`/`supersedes`/`publication_revalidation_provenance`
  untouched (R6: PREARCH as activation refuses `DM022_WRONG_FAMILY`).

No new runtime module beyond the two mapped modules was created (no return to
Astra needed for module invention). Test-only helper is B-owned test file only;
it never enters source closures. Shared fixture helper lists (C1 staged-source/
renewal/Weekly/Longform, C2 editorial/retention/current-authority/P1/P2R/P2V
copy-lists) are NOT edited; any needed copy-list change is requested via
coordination, not made here.

## 3. Precise map contradictions / blockers

None that weakens the map. One honest incomplete-source condition (not a map
contradiction):

- LOW/HIGH/schemas are not yet installed in `candidate-work` (A owns). Every
  B PREARCH path therefore raises explicit `DM022_LOW_UNAVAILABLE` (or
  `DM022_TRANSITION_ACTIVE` via stub in tests) and never falls back to old
  canonical reads. This is the selected fail-closed behavior per coordination
  (“don't add fallback when LOW missing to conceal incomplete source”), not a
  silent pass. Full B PREARCH execution (four-ref live re-hash, completion
  consistency, HIGH switch) requires A landing + frozen integration snapshot.
- `tests/test_dm022_prearchitecture_acceptance_v2.py` (A-owned, already
  present in `candidate-work`) imports LOW/HIGH/fixture helper that are not
  yet installed; it does not collect in this tree state. B did not edit it.
  This is expected parallel-ownership incompleteness, not a B failure.

No R4/R6/ROOT predicate was found unimplementable in B scope; no A1-vs-A2
reopening is requested. If A’s LOW signatures differ literally from
`require_research_operation_ready(repo_root, state_path)` /
`resolve_research_authority(repo_root, state_path)` /
`load_typed_checkpoint_record(repo_root, path)`, B will adapt call sites
before the frozen snapshot (exact mismatch to be returned then, not broadened
here).

## 4. Honest test status (no execution per task discipline)

- `DO NOT RUN tests during concurrent source edits` was obeyed: no
  `pytest`/`unittest`/import execution was run in this turn.
- `ast.parse` (no imports, no cache) passes for all 12 edited B files + the
  new B test file (13/13 OK). This is syntax only, not behavioral proof.
- New B tests are written to be meaningful (real predicates, tmp fixtures,
  stub-LOW late seams, zero-write assertions) but have NOT been collected or
  executed here; they must run AFTER authors return, on the frozen immutable
  integration snapshot with separately source-committed synthetic fixtures in
  an independent DB (no fixture objects in reconstruct, no old-runner reuse,
  no ordinary candidate/reconstruct commit).
- Affected regressions + both-route positive/negative/later-lifecycle witnesses
  (Weekly+Thematic, four-artifact acceptance, affected/unaffected semantics,
  7-slot retain/clear/regenerate without audit overwrite, repeat, wrong-role
  refusal, forward Architecture/Draft/publication readback, G71→G76 control,
  G76 correction→initial publication→editorial/renewal, old/new/unknown
  State + guard/completion recovery, stale Raw/HEAD, ownership/close/replace
  faults, explicit resume) remain for the frozen-snapshot phase + independent
  implementation review. No old test-count/PASS is transferred.

## 5. Ownership / next

- B owns only the 12 files + new B test above. A owns LOW/HIGH/schemas/
  evidence/screening/completeness + A tests; C1 owns histories/derivation/
  config; C2 owns publication/editorial consumers. No cross-owner edit was
  made.
- After A + C1/C2 return, bind one immutable complete integration snapshot,
  then execute meaningful both-route witnesses + affected regressions + late
  seams; preserve all failures + unique raw logs with actual exit codes.
- No author approval is claimed; root review + independent implementation
  review remain required before closeout. Stop at next coherent Commit Point;
  ordinary Commit/Push Human-owned.
