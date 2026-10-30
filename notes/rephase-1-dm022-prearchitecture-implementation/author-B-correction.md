# Owner-B correction return — R1 REJECTED findings closed (B scope only)

2026-10-28. Corrects the first 756-file return preserved in
`snapshot-r1-20261028T121631Z/worktree` (manifest `f67ad9b9…`) per
`astra-r1-source-review.md` §A + cross-owner B findings. Human Commit
readback still none; no ordinary commit/Gitconfig/network/cleanup/Production.
Source + rejected R1 snapshot immutable. Only the 12 B-owned scripts + B test
file below are edited here; A/C1/C2 files untouched. No readiness,
completion, or approval claimed. Runtime integration tests not executed on
shared source while A2/C1/C2 edit; AST static checks on own files only.

Working source: `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`.

## 1. Exact B files corrected

- `scripts/survey_agent_control_v2.py`
- `scripts/run_selection_architecture_v2_interactive.py`
- `scripts/run_evidence_v2_interactive.py`
- `scripts/run_drafting_synthesis_v2_interactive.py`
- `scripts/survey_drafting_v2.py`
- `scripts/survey_drafting_v2_base.py`
- `scripts/survey_handlers_v2.py`
- `scripts/survey_stage_validation_v2.py`
- `scripts/survey_orchestrator_v2.py`
- `scripts/survey_core_execution_bridge_v2.py`
- `scripts/survey_human_gate_v2.py`
- `scripts/survey_architecture_v2_base.py`
- `tests/test_dm022_prearch_b_ordinary_consumers_v2.py` (rewritten, unittest, 12 methods)

## 2. Root deviations fixed (no schema weakening)

1. **Strict `reason` field.** `_is_prearchitecture_record` now checks
   `record.get("reason") == "REVIEWED_ACCEPTED_UPSTREAM_CORRECTION"`, not
   `reason_class`. Legacy/editorial discriminators unchanged.
2. **Exact operation/boundary objects.** `_validate_prearchitecture_record_content`
   now requires `operation == {from_state:EVIDENCE_REVIEWED,to_state:EVIDENCE_REVIEWED}`
   and `producer_boundary == {from_state:CANDIDATES_NORMALIZED,to_state:EVIDENCE_REVIEWED}`.
   All `from`/`to`, list-alias, and `producer_from` variants removed; an
   invalid-dict boundary now refuses (previously passed).
3. **Four-path proof plumbing.** `_validate_prearchitecture_core_proof` signature
   is now `(repo_root, checkpoint_path, record) -> list[str]` and calls the
   selected `low.check_supersession_record_from_paths(repo_root, checkpoint_path,
   report_path, before_copy_path)`. `report_path` derives from the pinned
   record's `report` SizedRef; `before_copy_path` derives from the pinned
   `revision_root + /retention/state-before.json`. No caller proof dict is
   trusted; the record is crossbound (report/revision shapes) before the call.
   The old `checker(record)` single-arg call is deleted.
4. **Required LOW, no scaffolds.** All B files now use static
   `from scripts import survey_research_authority_v2 as low` (G76 required
   dependency). All `_dm022_low()` wrappers, `getattr(low, …)` /
   `hasattr` probes, `LOW_UNAVAILABLE` compatibility branches, and
   `except Exception: pass` fallbacks are deleted. Direct calls:
   `low.require_research_operation_ready`, `low.require_no_active_guard`,
   `low.load_typed_checkpoint_record`, `low.resolve_research_authority`,
   `low.check_supersession_record_from_paths`.
5. **No fallback swallowing.** `_validate_checkpoint_record` and
   `_resolve_checkpoint_artifact` now do generic classification first via the
   required loader: LEGACY → strict old-schema path; PREARCH → full branch
   (content + same-record triplet + issue + 4-path proof); unknown kind →
   refuse. A malformed PREARCH record returns errors, never falls through to
   legacy. The same rule applies to `resolve_active_evidence_views`,
   `advance_with_checkpoint`, `build_stage_checkpoint`, orchestrator/bridge
   refusal, and evidence-runner supersession refusal.
6. **Full legacy validity preserved.** Legacy `_validate_checkpoint_record`
   producer/issue/lifecycle/superseded/artifact/review/core-report/release
   predicates are byte-identical; only the PREARCH dispatch was added above
   them. `validate_agent_state` retains all existing predicates plus the
   precise new-kind branch; `production.verify_state_basis` is never
   substituted.
7. **New CP through full path proof.** `_resolve_prearchitecture_artifact`
   and `resolve_active_research_four_refs` use the required loader + live
   re-hash + View→Evidence binding + same-record triplet + the 4-path checker.
   The return now exposes the A2-compatible shape
   `{family, checkpoint, artifacts(parsed), lineage, artifact_refs(4 NamedRefs),
   evidence/views/ledger/completeness + paths}`; callers consume
   `artifact_refs` paths, never old `evidence_path` fake fields or canonical
   Singletons. A current fake bodies were consulted only for signatures, not
   matched for fake fields (e.g. fabricated digests, `result_set` placeholders,
   `reason_class`).

## 3. Per-file scope vs real calls (all 12 reviewed)

- `agent_control`: real `low.*` calls in dispatch/resolve/proof/ready/advance;
  prepublish READY in build/advance/approve; no canonical fallback.
- `run_selection`: READY entry + before each of 7 writes; 7-slot preflight incl
  audit (lstat, symlink-safe); ledger/completeness + evidence/views via
  `artifact_refs`; caller input vs generated archive provenance kept.
- `run_evidence`: READY entry + prepublish before ledger/completeness writes;
  explicit PREARCH supersession refusal (HIGH R writers only).
- `run_drafting`: READY entry + before each package/result/synthesis/archive;
  R4 via `artifact_refs`; no stale fallback.
- `survey_drafting_v2`: `_historical_raw_authority_hashes` gains optional
  `evidence_ref/matrix_ref` (R4 same-SHA + parsed equality); stale canonical
  refuses; `validate_self_contained` threads them through.
- `survey_drafting_v2_base` / `survey_architecture_v2_base`: pure, guard-free,
  `_content never verify_state_basis`; callers pass R4 paths; entry enforces G.
- `survey_handlers`: `_evidence_basis(cfg)` + `_selection_basis(cfg)` thread cfg;
  `_dm022_verify_handoff_four_refs` binds handoff inputs to `artifact_refs`
  bytes; superseded mode refuses when R4 absent; zero handoff bytes on refuse.
  `validate_drafting_synthesis` keeps cfg and passes R4 `evidence_ref` when PREARCH.
- `survey_stage_validation`: READY at `validate_stage` entry + before report;
  `REQUIRED_CURRENT` names unchanged, `CANDIDATES_NORMALIZED` values verified
  against `artifact_refs` when PREARCH; `_prior_artifacts` same-wrapper note;
  pure historical validation stays guard-free.
- `survey_orchestrator`: READY entry + prepublish; `_dm022_refuse_prearch_transition`
  now loads the pinned record kind (not shape-only) and refuses only PREARCH.
- `survey_core_execution_bridge`: READY entry; bridge advance classifies via
  loader and refuses only PREARCH-kind.
- `survey_human_gate`: `_current_pending_gate` stays guard-free diagnosis;
  all 4 mutating entries add READY; bare `EVIDENCE_REVIEWED` manufacture still
  refused by `_validate_gate_pending`; genuine-Human-only paths unchanged.

No new runtime module was created; no C1/C2/shared-helper file was edited.
Shared fixture/copy-list changes (C1 staged-source/renewal/Weekly/Longform,
C2 editorial/retention/current-authority/P1/P2R) remain requests, not edits here.

## 4. Open API counterparts (owned elsewhere, needed to bind)

- A2 LOW (replacing fake prove/4-ref/completeness): `load_typed_checkpoint_record
  -> {family, record}`, `_resolve_research_from_state_bytes`,
  `_load_typed_four_refs`, `resolve_research_authority -> {family, checkpoint,
  artifacts(parsed), lineage, artifact_refs}`, `check_supersession_record_from_paths
  (repo_root, checkpoint_path, report_path, before_copy_path) -> list[str]`,
  `require_research_operation_ready`, `require_no_active_guard`,
  `require_completion_consistent`, `guard_path_for`, `lstat_slot`, plus 5
  installed `schemas/dm022-*` bytes and full content/ledger/completeness/HEAD-tree
  proofs. B codes to these signatures; current A fake bodies were not matched.
- C1: source-family pins/registry/config (`pipeline71→76`, replay 70/union 73,
  canon 36/41, schema SHAs), staged-source/renewal/derivation wiring.
- C2: downstream role refusal/readiness, retention walks, P1/P2R/P3S explicit
  copy-lists. No B fallback satisfies those paths.
- Root: frozen immutable integration snapshot + meaningful both-route witnesses
  + affected regressions + independent implementation review before any closeout.

## 5. Tests (honest status, no execution here)

- Rewrote `tests/test_dm022_prearch_b_ordinary_consumers_v2.py` as `unittest`
  with 12 methods calling real public B paths with schema-shaped PREARCH
  records and real tmp files: strict reason, exact operation, exact boundary,
  full content pass, wrong-family for validation/freeze/release/selection,
  forward-field/lineage, triplet same/split, 7-slot exact + audit overwrite
  zero-writes, core-proof accept/mixed-refuse, legacy discriminators preserved,
  drafting R4 missing-refuse. No stub-LOW injection, no hand-coded `raise` in
  the test body to simulate errors, no synthetic fake-PASS approvals.
- Not executed in this turn per discipline (no runtime integration on shared
  source while A2/C1/C2 edit). `ast.parse` passes for all 12 B scripts + the
  rewritten test (13/13 OK, no imports). Collection/execution, both-route
  fixtures, late-seam/old/new/unknown State, guard/completion loss, stale
  Raw/HEAD, ownership/close/replace faults, and explicit resume belong to the
  frozen-snapshot phase + independent review. No old test-count/PASS transfer,
  no readiness claim.

Author: Owner B. Correction complete in code; implementation acceptance remains
with root + independent review at the next coherent Commit Point.
