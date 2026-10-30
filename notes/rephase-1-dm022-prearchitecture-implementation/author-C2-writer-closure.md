# Owner-C2 writer closure — DM022 remaining prepublish coverage complete

2026-10-28. Owner C2 (publication/editorial consumers, 12 scripts + owned tests
only). Working source:
`.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`
(all paths below relative to it). Frozen R2
`snapshot-r2-20261028T124706Z` available for reference ONLY (NOT edited).
No Human commit readback, no ordinary commits, no Git config/network/Production/
old-runner/cleanup. No tests executed on live candidate-work (AST-only);
new tests target independent temp fixtures for evaluator on fixed R2.

Binding order: contract a345bb95 INCLUDING §11, precode §5, ROOT FULL 0425c530
INCLUDING §5, independent §§8–9 FINAL-BINDING, then R3 overridden by R4 + 5
literal schemas + R5 families + R6 roles, then ROOT. A2 LOW
(`survey_research_authority_v2.py`, current but review-pending) is REQUIRED
installed G76 dependency. Used actual shapes: `artifacts` (parsed dicts) vs
`artifact_refs` (4 NamedRefs `{name,path,sha256}`); both checked where
applicable. No `reason_class` for PREARCH (exact `reason ==
REVIEWED_ACCEPTED_UPSTREAM_CORRECTION`). No generic permission dicts, no
guard-skip, no noState fallback for writers. Detached diagnostics/history: no
State validation/mutation guard. Writers: READY entry+prepublish. HIGH DM022
sole mutator during guard (C2 never writes guard/State directly except via
existing agent writers in editorial_publication activate/resume, H-owned).

## 1. Completed call matrix (actual calls, not helpers-only)

Legend: ENTRY = READY at function entry (after safe/lexical binds, before any
canonical writes); PRE = READY immediately before each canonical write batch /
State replace. Derivation = canonical STATE derived from validated
Profile/reloaded manifest retained scope/request paths where writer lacks
explicit state_path; threaded = exact state_path param used. All READY calls are
direct `LOW.require_research_operation_ready(repo_root, state_path)` (full
guard + completion exact verify), no getattr/hasattr fallback, no swallowed
content-invalid.

### editorial_publication (has explicit state_path — threaded)

- `prepare_publication(root, state_path, ...)`: ENTRY (after `_require_scope_bound`,
  `repo / state_rel_init`) + PRE (before build-transfer writes). Done (prior unit,
  retained).
- `finalize_publication(root, state_path, ...)`: ENTRY (after `_require_scope_bound`,
  `repo / state_rel_f`) + PRE (before bundle `quality` write). Wired this unit.
  Positive path: after READY passes, continues with receipt/manuscript/QA/Gate/
  Candidate/seal (normal after-DM022 path preserved, not blanket refuse).
- `activate_publication(root, state_path, set_path, ...)`: ENTRY (after safe binds,
  `repo / state_rel`) + PRE-RECORD (before `_exclusive_create_record_bytes`) +
  PRE-STATE (before `_atomic_replace_state_bytes`). Wired this unit. ALREADY_ACTIVE
  short-circuit does full strict State + full set read-only (no takeover).
- `resume_activation(root, state_path, record_path)`: ENTRY (after safe binds) +
  PRE-INSTALL (before guarded State replace; rechecks State still exact old).
  Wired this unit. INDETERMINATE preserves all bytes (no overwrite/rollback).
- `validate_editorial_receipt / validate_prepared_set / verify_activation_history`:
  diagnostic validators, NO guard (read-only, NOT write permits). Correct per
  detached-diagnostics rule.

### publication writers (no explicit state_path — derived, legacy API preserved)

- `build_candidate(..., state_path=None)`: ENTRY (derived STATE via manuscript
  `production_profile -> profile bytes SHA bind -> source_root -> config
  authoritative_filename`, `repo / src / production-state.json`) + PRE (same
  derivation before `_write_immutable`). Optional `state_path` threaded when
  caller has it (e.g., renewal C1 path); otherwise derived. Legacy callers
  without state_path still work via derivation (no new required param).
- `build_preview_approval(..., state_path=None)`: ENTRY + PRE via candidate
  `reader_manuscript.path -> manuscript -> profile -> STATE` derivation.
- `build_visual_review(..., state_path=None)`: ENTRY + PRE via approval
  `publication_candidate_path -> candidate -> manuscript -> profile -> STATE`.
  Legacy retained; new production uses pre-preview VISUAL (not this function).
- `build_freeze(...)`: ENTRY + PRE via `prep["profile"] -> source_root -> STATE`
  (already wired prior unit, retained). Freeze/Release via State-bound selection;
  stale canonical refuses.
- `validate_candidate / validate_preview_approval / validate_visual_review /
  validate_release_manifest / validate_release_record`: diagnostic validators,
  NO guard (read-only). Publication Candidate/Release NEVER carry PREARCH
  (`_dm022_refuse_prearch_as_publication`, exact `reason`).

### reader_publication (manuscript writers — derived STATE)

- `build_manuscript_manifest(...)`: ENTRY (after `_profile`, derived STATE via
  `profile.paths.source_root -> config`) + PRE (before `core.write_json`,
  recomputed from already-validated `profile`). Fail-closed if cannot bind.
- `build_review_record(..., state_path=None)`: ENTRY (threaded if given, else
  derived via manuscript `production_profile -> profile SHA bind -> source_root
  -> STATE`) + PRE (via already-validated `profile` in scope, no reload).
  Legacy API preserved (optional param only).

### reader_gate (optional state_path — exact bind, no generic dict)

- `evaluate_reader_surface_gate(..., state_path=None, output_path=None)`:
  ENTRY — if `state_path` bound, exact path bind + full READY; elif writing
  (`output_path is not None`) without `state_path`, derive STATE from validated
  manuscript `production_profile -> profile SHA bind -> source_root -> config`
  + full READY (no guard-skip). If read-only (`output_path is None`) without
  `state_path`, detached diagnostic, NO guard. PRE (before `core.write_json`
  report) — same bind/derive + full READY. Preserves normal after-DM022
  positive path (G76 research resolves via LOW, Gate evaluates) + legacy
  business API (optional params only, no new required args).
- `validate_reader_surface_gate(..., state_path=None)`: admission validator —
  if `state_path` bound, exact path bind + full READY (admission context);
  if unbound, detached diagnostic, NO guard (receipt replay uses retained
  lineage). `validate_manuscript_surface`, `_inspect_gate_record`,
  `load_and_validate_*`, `build_weekly_reader_surface_input` (obsolete raises):
  read-only, NO guard.

## 2. Derivation / threading rules applied (no guard-skip)

- Threaded where caller has exact State: all editorial_publication writers
  (`prepare/finalize/activate/resume`) use passed `state_path` (`repo /
  state_rel`) — no derivation, no dict.
- Derived where writer lacks State param (legacy API preserved via optional
  `state_path=None` only): manuscript path -> `production_profile {path,sha256}`
  -> profile bytes SHA verify -> `paths.source_root` -> `config/state_authority/
  authoritative_filename` -> `repo / src / production-state.json`. Each link
  reloaded + SHA/bound checked; any failure raises (fail-closed, never
  guard-skip, never legacy/canonical fallback). Content-invalid propagates.
- No generic permission dicts: every reference reloaded via file/path +
  lstat+read+hash+schema/content; caller dicts never trusted. No
  `require_no_active_guard` alone (guard-only permission removed everywhere);
  only full READY.

## 3. A2 API actual shapes used (review-pending, no placeholders)

- `load_typed_checkpoint_record(repo_root, path) -> {family, record}` for
  classification only (R6:557 original validation, R6:931 refresh validation,
  R6:121 release payload gate, mode probe). PREARCH refused as wrong family
  even if parses, before CANONICAL fallback.
- `resolve_research_authority(repo_root, state_path) -> {family, checkpoint,
  artifacts, artifact_refs, lineage}`: full-path (State FILE only, never caller
  State dict), typed + 4-artifact live re-hash + FULL content checks via real
  S1.1 leaf cores. Used in `_ckpt_resolve` (P1), current-authority lineage,
  and positive-path continuation. Both `artifacts` (parsed, for content) and
  `artifact_refs` (NamedRefs `{name,path,sha256}`, for refs) 4-name checked;
  `lineage.triplet` enforced; `supersession_checkpoint_sha256` bound; research
  supersession lineage kept distinct from publication `supersedes`.
- Structural `_resolve_research_from_state_bytes` alone NEVER used as typed
  full validation (removed from C2 paths).

## 4. Real blocking API requests (exact signatures, no unwired silently)

NONE. All required callers are inside C2-owned files (signatures above) or
already-threaded State paths. No cross-owner patch requests:

- C1-owned `survey_versioned_renewal_v2.build_candidate` call site (line 2712)
  and B-owned `survey_orchestrator/agent_control.build_preview_approval` sites
  do NOT need changes: C2 writers derive STATE internally, preserving their
  legacy call signatures (no new required params). If coordinator prefers
  explicit threading through those external callers instead of internal
  derivation, exact patch would be: add `state_path: Path | None = None`
  pass-through at those call sites — NOT applied (would touch outside-owned
  files); internal derivation satisfies without cross-owner edits.
- No HIGH DM022 sole-mutator violation: C2 never claims/releases guard, never
  writes State except via existing agent writers in activate/resume (H-owned
  path, already reviewed). No new runtime modules beyond mapped 2 modules.
- Frozen R2 referenced for behavior only (e.g., renewal proof binding shapes);
  NOT edited, no code copied from it.

## 5. Tests (not run on live candidate; evaluator runs on fixed R2)

Extended `tests/test_survey_dm022_c2_consumers_v2.py` (independent temp dirs,
no reconstruct fixtures, no inherited GIT_* vars, process-scoped identity,
meaningful fixture commit; AST-only here):

- `TestC2WriterReadyBindingAtActualCalls`: finalize/activate/resume entry refuses
  with guard (`DM022_TRANSITION_ACTIVE|NO_PREPARE|...`, no canonical writes via
  before/after snapshots); build_candidate derived-STATE entry refuses;
  evaluate gate with bound State enforces READY (no helper-only, actual writer
  calls). Late guard/completion binding: prepublish READY calls share the same
  helper as entry (code-identical path); late-guard (guard created between
  entry and prepublish) is refused at prepublish because prepublish re-invokes
  full READY (verified by code path, exercised by evaluator with staged guard
  fixture on fixed R2).
- Prior selector/wrong-family/healthy-control/GitDB tests retained.

Full scope actually done (all §4 writers wired entry+prepublish); no
helpers-only completion claimed. Whole NOT_READY/step4B3OPEN/audit unstarted/
DM021+022OPEN preserved except implementation progress; independent
implementation review still required before closeout.
