# Owner-C2 implementation return — DM022 pre-Architecture publication/editorial consumers

2026-10-28. Owner C2 (publication/editorial consumers). Human continuation authorized
ACTUAL CODE in independent candidate-work ONLY; docs-only explicitly NOT the task.
Binding order: contract a345bb95 INCLUDING §11, precode assessment §5,
precode ROOT FULL 0425c530…/13788B INCLUDING §5, independent readiness §§8–9
FINAL-BINDING, then R3 (overridden by) R4 + literal 5 schemas, R5 families, R6 roles,
then ROOT. R6 replaces R5 per_function_branches[7] and overbroad publication-chain
wording. No ordinary candidate/reconstruct Commit/Push; no fixtures in reconstruct;
no Git config mutation; no network/Production/reset/clean/old-runner/raw-overwrite.
Used apply_patch-equivalent edits (dedicated Edit tool); no shared-source test runs
while others editing; AST-only now (no import/cache).

Working source:
`.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`
(all C2 paths below relative to it). Started from prepared full742+inodes
source actual409/tree8ce + inherited93; no ordinary source commit.

## 1. Exact owned paths (C2 ONLY, disjoint from A/B/C1)

12 scripts (all scripts, per coordination):

- `scripts/survey_publication_set_v2.py` (R4 row23, R6 sites 10-13 + selectors/discriminators/chain-walkers)
- `scripts/run_semantic_publication_v2_interactive_base.py` (R4 row24)
- `scripts/survey_editorial_correction_proposal_v2.py` (R4 row25, R6 site 14)
- `scripts/survey_editorial_publication_v2.py` (R4 row26)
- `scripts/survey_editorial_retention_v2.py` (R4 row33, P2R)
- `scripts/survey_editorial_current_authority_v2.py` (P2V observer)
- `scripts/survey_publication_v2.py` (R4 row31)
- `scripts/survey_reader_surface_gate_v2.py` (R4 row34)
- `scripts/survey_execution_record_v2.py` (R4 row35)
- `scripts/survey_reader_publication_v2.py` (R4 row36)
- `scripts/survey_weekly_mechanical_refresh_v2.py` (R6 site 17, R4 receipt diagnostic)
- `scripts/survey_release_checkpoint_v2.py` (R6 site 15)

Owned tests / fixture helpers (no other-owner updates):

- `tests/test_survey_editorial_correction_proposal_v2.py` (P1 helper: added DM022_UNTRACKED_SOURCES)
- `tests/test_survey_editorial_retention_v2.py` (P2R helper: added DM022_UNTRACKED_SOURCES + copy-if-present)
- `tests/test_survey_editorial_current_authority_v2.py` (P2V helper: added DM022_UNTRACKED_P2V_SOURCES + copy-if-present)
- `tests/test_survey_dm022_c2_consumers_v2.py` (NEW C2 group tests: wrong-role, no-read/no-write, guard/completion, lineage, independent GitDB)

NOT touched (other owners, concurrent edits respected):

- A: `survey_research_authority_v2.py`, `survey_prearchitecture_acceptance_v2.py`,
  5× `schemas/dm022-*.schema.json`, evidence/screening/completeness cores, A tests/helpers.
- B: agent/stage/handlers/orchestrator/bridge/human-gate, selection/architecture/drafting,
  stage_validation, four-ref/7-slot writers.
- C1: versioned-renewal history/source/renewal, weekly/longform derivation, longform
  generated, staged-source, `config/survey-production-v2.json`, C1 fixture helpers.

New runtime modules beyond the mapped 2 modules / 5 schemas: NONE added. Test-only helper
file above is NOT runtime authority and never enters source closures.

## 2. What was implemented (per R4/R6/ROOT, not count-only)

All paths resolve 4 refs from the new PREARCH record, never stale canonical
Ledger/Completeness. Optional State paths exact State-bind or typed
recognized/refuse (no generic verified dict). Research own lineage distinct from
publication supersedes. Publication activation/schema/_record_kind/revalidation
pointer NEVER accept PREARCH; explicit wrong-family refuse in mode probe BEFORE
CANONICAL fallback, retain strict legacy/known-versioned cases. Checkpoint validation
expected roles concrete 17 sites incl original validation 557, release payload 121,
refresh validation 931 — no PREARCH. LOW generic parse-only classification, not
permission. Detached history no live State validation; normal HIGH writer full LIVE
validation/guard. Later corrected research survives actual initial publication→
editorial/renewal readback without requiring EVIDENCE live window.

- **publication_set**: Added PREARCH_KIND/REASON, DM022_CHECKPOINT_SCHEMA const (old
  CHECKPOINT_SCHEMA byte-identical), `_is_prearch_record` (pure dict-only
  classification), `_refuse_if_prearch_publication` / `_refuse_prearch_checkpoint_record`,
  `_dm022_resolve_research_refs_via_low` (prefers LOW.resolve_research_authority /
  _resolve_research_from_state_bytes; else explicit DM022_MISSING_RESEARCH_AUTHORITY,
  never stale fallback, never caller-verified dict). Mode probe
  `resolve_publication_mode:2253` now explicit PREARCH test BEFORE versioned test;
  PREARCH refuses wrong-family, legacy returns CANONICAL, unknown kind fails-closed
  (strict legacy/known-versioned only). Activation
  `validate_activation_record` + `_validate_versioned_activation` refuse PREARCH before
  any branch. `_load_record_file` refuses PREARCH chain members. Sites 11-13
  (derive_canonical_anchor:1213, before-digest:1627, selection prior:1981) refuse
  PREARCH at Stage Checkpoint sites. `resolve_publication_artifact_path:2151` refuses
  PREARCH roles before any read. `resolve_stage_artifact_path:2181` refuses research
  4-ref names via stage-template (F4b split; stage-template inheritance true only for
  stage paths). Selectors `1992/2215/2267` inherit mode-probe refusal (no CANONICAL
  fallback); `_record_kind` unchanged (LEGACY|EDITORIAL|VERSIONED only).

- **release_checkpoint (R6:121)**: Expected FROZEN→RELEASED only; PREARCH payload
  refused before schema gate (`_dm022_is_prearch_record` + explicit check). Passive
  READY entry after Profile/source_root bound + prepublish re-check before checkpoint
  write. No LIVE State bypass; agent State basis retained.

- **weekly_mechanical_refresh (R6:931)**: Expected refresh validation checkpoint
  DRAFT_COMPLETE→VALIDATED_DRAFT + validation in checkpoints; PREARCH refuses.
  READY entry after canonical State/Profile/source_root bind. Receipt replay uses
  retained lineage (no before-equality); guard only preArch transition.

- **editorial_correction_proposal (R6:557 + R4:25)**: ROOT-corrected row14 expected =
  original validation checkpoint (NOT downstream graph). `_original_checkpoint`
  refuses PREARCH as wrong family. `_ckpt_resolve` pins SAME PREARCH wrapper for
  evidence+materiality+completeness, resolves 4 via agent/LOW R4 same-record path,
  retains old canonical bytes history-only. Split/mixed authority refuses
  (DM022_SPLIT_AUTHORITY). Upstream PREARCH nodes resolved separately via LOW R4.

- **editorial_publication (R4:26)**: MUST NOT treat PREARCH as editorial/versioned
  activation; explicit recognition-or-refuse (`_dm022_refuse_prearch_activation`).
  VERSIONED_ACTIVE branches unchanged. READY entry after scope bound + before any
  canonical writes (prepare path hooked; finalize/activate/resume share same helper
  for integration snapshot).

- **editorial_retention (R4:33, P2R)**: Capture takes explicit R4 + PREARCH wrapper
  refs post-adoption (no canonical fallback); Human approval refs NEVER rebound.
  READY entry after State/Profile bound, before P1 + before any writes.
  `verify_retention` diagnostic MUST NOT require guard absence (read-only, not a write
  permit) — unchanged, documented.

- **editorial_current_authority (P2V)**: Read-only observer; diagnostic MUST NOT
  require guard absence. `_dm022_check_prearch_lineage` recognizes PREARCH lineage
  (same-record triplet, retained COPY/lineage, no live-before equality, no
  window/HEAD re-check on later readback) or refuses superseded mode. Later corrected
  research survives initial publication readback.

- **publication (R4:31)**: Walkers accept PREARCH for evidence/materiality/completeness
  group (same 4-name set, new kind/operation branch); Freeze/Release via State-bound
  selection. `validate_candidate` / `validate_release_record` refuse PREARCH as
  publication authority. Mutating builders expose `_dm022_require_ready` for READY
  entry+prepublish (guard + completion). Stale canonical Freeze/Release refuses;
  State-bound selection resolves.

- **reader_surface_gate (R4:34)**: Optional State paths exact State-bind or typed
  recognized/refuse. No no-State canonical research read post-adoption; receipt replay
  uses retained lineage. `validate_reader_surface_gate` binds State→Profile→source_root
  then passive READY when State present; malformed State binding fails-closed.

- **execution_record (R4:35)**: READY entry after Profile/source_root bound, before any
  canonical output (`initialize` hooked). `validate` diagnostic MUST NOT require guard
  absence (read-only, not a write permit) — unchanged.

- **reader_publication (R4:36)**: MUST recognize PREARCH kind or refuse superseded
  mode. READY entry after Profile/source_root bound, before manuscript/binding output
  (`build_manuscript_manifest` hooked). No unguarded normal writer. Stale-canonical
  read refuses.

- **run_semantic_base (R4:24)**: READY entry (passive guard + completion) after State/
  Profile bind + before main.tex/bib/sty/manifest writes, plus prepublish re-check.
  Ledger/completeness transitively via package basis + R4; Evidence-bind +
  HOLD/NEEDS_MORE refuse retained; `assert_canonical_publication_mode` strict retained.
  Publication activation NEVER accepts PREARCH (via pubset mode probe).

LOW/HIGH integration: C2 files call LOW via function-local imports only
(`HIGH→LOW` passive allowed, no recursion, no top-level LOW→agent/HIGH). When LOW
absent (parallel window), local lstat fail-closed predicate enforces same rule
(guard ANY present refuses; active PREARCH without verifiable completion refuses)
— never weaker, never stub success. Now that owner-A has landed LOW/HIGH + 5 schemas
in the same workcopy (untracked, per §3), delegates resolve to real LOW.

C1-needed closure additions in C2 P1/P2R/P2V files per R4/R5: fixture copy lists now
include the two LOW/HIGH new files + five new schemas explicitly (lists, not counts),
protected actual parent (workspace = candidate-work parents[1]), copy-if-present until
A lands (now present), pinned SHA + drift checks. No count-only claim. No other-owner
test updates.

## 3. Exact API needs from A/C1/B (no broadening without root)

- LOW `resolve_research_authority(repo_root, state_path)` public path interface +
  `_resolve_research_from_state_bytes(repo_root, state)` structural +
  `_load_typed_four_refs(repo_root, structural)` typed loads — used by C2 resolvers.
  If any signature differs from R4 §1.2, return to Astra before broadening.
- HIGH `require_research_operation_ready(repo_root, state_path)` /
  `require_no_active_guard(source_root)` passive IO — C2 delegates when present.
- C1: G76 pipeline76 / replay70 / union73 / canon36+41 memberships are planned
  memberships, not measured source; C2 does not invent them. Publication history/source
  walkers (C1) must recognize PREARCH lineage without forcing old records into G76.
- B: `agent:489/819` PREARCH branches, `advance:1774` REFUSE, `build:1703` UNTOUCHED —
  owned by B/A; C2 does not edit. Any missing direct canonical reader or omitted
  import/closure/contract contradiction returns to Astra (none new found in C2 scope;
  pubset single-resolver split F4a/F4b applied).

Map contradictions found: NONE new in C2 scope. R6 row14 label corrected per ROOT
(original validation, not downstream graph); R4 row25 separate. Mode-probe
`else CANONICAL` overbreadth fixed per R6. No new family/schema introduced.

## 4. Tests: NOT RUN (by design this unit)

- AST-only verification performed (no import/cache): all 12 scripts + 3 owned test
  helpers + 1 new C2 test file parse OK (see §5). No shared-source pytest runs while
  others editing (coordination § execution discipline).
- New tests `tests/test_survey_dm022_c2_consumers_v2.py` (C2-owned, independent temp
  dirs, no reconstruct fixtures, no inherited GIT_* vars, process-scoped identity,
  meaningful fixture commit test, no ordinary commit/config/network/Production) cover:
  public wrong-role + no-read/no-write (mode probe, artifact roles, stage-template
  research names, release payload, original validation 557, refresh 931),
  completion guards/later forward (guard blocks mutator, guard-absent diagnostic,
  research vs publication supersedes separation), independent GitDB discipline.
- Full meaningful runs (both routes Weekly+Thematic, genuine-type synthetic,
  complete 4-artifact acceptance, affected/unaffected semantics, old/new/unknown
  State, guard/completion loss, stale Raw/HEAD, close/replace/ownership faults, late
  seams, explicit resume, normal forward Architecture/Draft/publication + history
  readback, G76 correction→initial publication→editorial/renewal, G71→G76 unchanged-
  upstream compatibility control) require root-fixed integration snapshot + all owners
  bound + independent GitDB fixtures. NOT run here.
- Affected regressions: NOT run here (would touch files others are changing).

## 5. Code status (exact)

AST parse OK (no import/cache), candidate-work relative:

- scripts/survey_publication_set_v2.py — OK, 2463 lines (was 2291; +DM022 block)
- scripts/run_semantic_publication_v2_interactive_base.py — OK, 288 lines
- scripts/survey_editorial_correction_proposal_v2.py — OK, 2682 lines
- scripts/survey_editorial_publication_v2.py — OK, 4132 lines
- scripts/survey_editorial_retention_v2.py — OK, 2142 lines
- scripts/survey_editorial_current_authority_v2.py — OK, 712 lines
- scripts/survey_publication_v2.py — OK, 2132 lines
- scripts/survey_reader_surface_gate_v2.py — OK, 2375 lines
- scripts/survey_execution_record_v2.py — OK, 474 lines
- scripts/survey_reader_publication_v2.py — OK, 1069 lines
- scripts/survey_weekly_mechanical_refresh_v2.py — OK, 1682 lines
- scripts/survey_release_checkpoint_v2.py — OK, 297 lines
- tests/test_survey_editorial_correction_proposal_v2.py — OK, 1878 lines
- tests/test_survey_editorial_retention_v2.py — OK, 1890 lines
- tests/test_survey_editorial_current_authority_v2.py — OK, 1266 lines
- tests/test_survey_dm022_c2_consumers_v2.py — OK, 222 lines (NEW)

No stub/closed-dict/readonly-helper-only completion claims. No synthetic genuine
approvals. No old test-count/PASS transfer. No ordinary commit/Push. Whole
NOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN preserved except implementation
progress; Profile/quality/adoption/savings OPEN. Stop at Commit Point; implementation
review independent of authors/root author-side review still required before closeout.
