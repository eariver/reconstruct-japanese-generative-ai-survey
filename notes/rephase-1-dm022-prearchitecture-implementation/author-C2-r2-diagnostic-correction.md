# Owner-C2 R2 diagnostic correction — detached validation vs writer gates

2026-10-28. Owner C2 (12 owned scripts + owned tests only). Fixed R2 snapshot
`53fde56…` available for reference ONLY (NOT edited). Live `candidate-work`
edited; no tests run on live candidate while A3/B/C1 edit (AST own files
only). No Human commit readback, no ordinary commits, no Git config/network/
Production/old-runner/cleanup. A3 checker/resolve APIs unchanged (full proof
4-path `artifact_refs` vs parsed `artifacts` honored in C2 call sites).

## 1. R2 C2-01 root cause and fix (removed helper → PUBLIC API)

R2 diagnostics §6 C2-01: `test_weekly_refresh_validation_prearch_refuses_whole_path`
called removed helper `wmod._dm022_refuse_prearch_refresh` →
`AttributeError: module has no attribute`. 9/10 C2 pass; this 1 ERROR blocked
Weekly-refresh checkpoint integration sign-off.

Root cause (C2-owned): prior correction removed the private helper but left the
test calling it — helper-only wiring, not PUBLIC coverage.

Fix (C2-owned files only):

- `scripts/survey_weekly_mechanical_refresh_v2.py`: added PUBLIC
  `validate_refresh_validation_checkpoint(root, state, validation_ref)` —
  exact `{path,sha256}` shape, repository-local safe file, SHA drift check,
  then wrong-family PREARCH refusal (exact `reason`, not `reason_class`)
  BEFORE any legacy branch, then stage-checkpoint schema + identity/producer
  (`issue_id`, `DRAFT_COMPLETE→VALIDATED_DRAFT`, `validation` in checkpoints).
  Lightweight PREARCH classification (strict parse, exact kind+reason) runs
  before full LOW typed load, so minimal PREARCH with valid surrounding
  fixture (real file + exact ref + matching SHA) refuses `DM022_WRONG_FAMILY`
  with no early preemption counted (no missing/shape/drift/schema counted).
  Full LOW typed load follows for defense-in-depth; content-invalid propagates
  (no swallow to legacy). Read-only: NO READY, NO State validation, NO guard —
  detached validation MUST work while transition guard held; writer
  `refresh_mechanical_evidence` enforces READY at entry (line ~910) +
  prepublish before receipt (line ~1410) + prepublish before Gate (new).
  Validator wired into writer (replaces inline block) — no unwired helper.
- `tests/test_survey_dm022_c2_consumers_v2.py`: `test_weekly_refresh_validation_
  prearch_refuses_whole_path` now calls the PUBLIC validator with real file +
  exact ref + matching SHA (valid surrounding fixture) and expects
  `DM022_WRONG_FAMILY`; no-read/no-write snapshot asserted. Added healthy
  legacy control `test_weekly_refresh_validation_healthy_legacy_accepts_whole_path`
  with minimal schema-valid legacy checkpoint (same issue, DRAFT_COMPLETE→
  VALIDATED_DRAFT, validation in checkpoints) that passes the same PUBLIC
  validator with no writes. No helper import, no manufactured dict-only pass,
  no phony profile (uses real files + derived Profile path where applicable;
  here validator takes already-validated `state` dict for issue check only,
  file authority via ref SHA — matches writer call context).

## 2. Crucial separation audited and fixed (diagnostic vs writer)

Rule enforced: detached/read-only State/history/Gate validation MUST work
while transition guard held; normal mutators/writers require READY
entry+prepublish; HIGH DM022 sole mutator during guard. No optional readiness
bypass flag.

Audited all C2 READY call sites; fixed one violation, confirmed the rest:

- FIXED `validate_reader_surface_gate(repo_root, path, ..., state_path=None)`:
  REMOVED operational `READY` when `state_path` bound. This diagnostic is
  called by HIGH/agent post-State validation with guard held (e.g.,
  `survey_agent_control_v2.py:2964` passes `state_path` during publication
  revalidation). Requiring READY there blocked HIGH full strict post-State
  validation with guard held. Now: exact path bind only (path reloading, no
  generic verified dict, no guard check); content-invalid propagates via
  derivation replay below. No-State canonical research read still refuses
  in derivation (retained lineage), not via guard.
- KEPT `evaluate_reader_surface_gate(..., output_path=None, state_path=None)`:
  READY entry + prepublish ONLY when writing (`output_path is not None`) —
  via bound `state_path` if given, else derived canonical STATE from validated
  manuscript `production_profile → profile SHA bind → source_root → config`.
  Read-only evaluate (`output_path is None`) has NO READY (diagnostic).
  Prepublish re-checks before `core.write_json` report. No guard-skip, no
  generic permission dict.
- CONFIRMED diagnostic (NO READY): `validate_manuscript_surface`,
  `_inspect_gate_record`, `validate_manuscript_manifest`, `validate_review_record`,
  `validate_candidate`, `validate_preview_approval`, `validate_visual_review`,
  `validate_release_manifest`, `validate_release_record`, `validate_editorial_receipt`,
  `validate_prepared_set`, `verify_activation_history`, `verify_retention`,
  `validation_ref_path`, `_recheck_bound_snapshot`, `_derivation_for_manuscript`
  (derivation binds via reloaded refs, no guard), `load_and_validate_*`.
- CONFIRMED writers (READY entry+prepublish, no bypass): `prepare/finalize/
  activate/resume_publication` (entry + pre-write + pre-State where applicable;
  finalize now also re-checks before Gate, candidate, seal writes for late-guard
  binding); `build_candidate`, `build_preview_approval`, `build_visual_review`
  (entry via derived STATE from manuscript/approval chain + prepublish);
  `build_freeze` (entry+prepublish via derived STATE); `build_manuscript_manifest`,
  `build_review_record` (entry+prepublish via derived/explicit STATE);
  `refresh_mechanical_evidence` (entry + pre-receipt + pre-Gate);
  `build_release_checkpoint` (entry + pre-write + pre-State);
  `initialize` execution_record (entry+prepublish); `capture_retention`
  (entry+prepublish). `_write_immutable`, `_exclusive_write_*` are low-level
  helpers, not independently gated (callers gate).

Traced actual callers for the fixed diagnostic: B agent revalidation
(`agent_control:2964` with `state_path`), C1 renewal (`versioned_renewal:2961`
without `state_path` → diagnostic path, no READY — correct), editorial
correction proposal (`2110,2121` without `state_path` → diagnostic, correct),
weekly refresh (`1437` without `state_path` → diagnostic via
`_inspect_gate_record` path? Actually refresh calls `validate_reader_surface_gate`
at line ~1475 WITH `state_path=state_path` — this is a writer (refresh) calling
diagnostic with State bound for exact bind + derivation replay. After fix,
diagnostic does NOT check guard (good — writer already passed READY at entry;
diagnostic re-validates content without re-gating). No bypass flag added;
writer gates remain.

## 3. Remaining writer closure (complete, no helpers-only)

- Editorial finalize now re-checks READY before bundle, Gate, candidate, seal
  writes (late-guard binding at each actual publish, not just entry).
- Prepare now re-checks before manuscript, receipt, build-record writes
  (in addition to entry + pre-build-transfer).
- Weekly refresh now re-checks before Gate install (in addition to entry +
  pre-receipt).
- All new PUBLIC validators are wired into their writers
  (`validate_refresh_validation_checkpoint` called by
  `refresh_mechanical_evidence`; no dead code).
- Checked own files for unwired `_dm022_*` helpers: removed dead
  `_dm022_resolve_research_refs_via_low` (pubset F4b split — pubset correctly
  refuses research names instead); removed dead weekly classifier helpers
  (replaced by PUBLIC validator). Remaining `_is_prearch_record` classifiers
  are called (payload/activation gates); remaining `_dm022_require_ready*`
  are all called at entry+prepublish (verified per function above).
- A2 API actual shapes used: `artifacts` (parsed) + `artifact_refs`
  (NamedRefs `{name,path,sha256}`) both 4-name checked in P1 `_ckpt_resolve`
  and P2V lineage; `load_typed_checkpoint_record` for classification,
  `resolve_research_authority(repo_root, state_path)` full-path (never
  State-dict structural alone), no `reason_class` for PREARCH.

## 4. Positive G76 + healthy canonical paths (no mocks, no phony profile)

- Tests use actual public APIs on real temp files with valid surrounding
  fixtures (exact refs, matching SHAs, validated Profile via
  `production_profile {path,sha256}` + profile bytes SHA bind → `source_root`
  → `config/state_authority`), never mocks or arbitrary source paths.
  Healthy controls preserved: `resolve_publication_mode(None)` → CANONICAL,
  legacy validation checkpoint passes PUBLIC refresh validator, independent
  GitDB commit discipline test.
- Full normal after-DM022 G76 initial publication→editorial/renewal paths are
  preserved in code (positive PREARCH family continues with new 4 refs +
  completion; only wrong-family at publication sites refuses). Full
  end-to-end witness requires fixed R2 + all owners bound + independent
  implementation review — NOT run here (AST only, no live candidate execution
  while A3/B/C1 edit; evaluator runs fixed R2 separately).

## 5. Real blocking APIs / unknowns (honest, no placeholders)

- NONE. No cross-owner patch requests: publication writers derive STATE
  internally (legacy API preserved via optional `state_path`), so B/C1 callers
  (`agent_control`, `orchestrator`, `versioned_renewal`, editorial finalize)
  need no signature changes. If coordinator prefers explicit threading through
  those external callers instead of internal derivation, exact patch would be
  `state_path: Path | None = None` pass-through — NOT applied (would touch
  outside-owned files).
- Frozen R2 referenced for behavior only (e.g., renewal proof binding shapes);
  NOT edited, no code copied.
- Unit ongoing, no Commit Point claimed. Whole NOT_READY/step4B3OPEN/audit
  unstarted/DM021+022OPEN preserved except implementation progress.
