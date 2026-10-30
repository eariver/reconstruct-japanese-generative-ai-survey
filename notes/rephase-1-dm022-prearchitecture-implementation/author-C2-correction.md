# Owner-C2 correction return — DM022 R1 source review findings

2026-10-28. Owner C2 correction (publication/editorial consumers, 12 scripts +
owned tests only). First integrated 756 return preserved (snapshot
`snapshot-r1-20261028T121631Z`, manifest `f67ad9b6…`); root REJECTED author
completion in `astra-r1-source-review.md` (no test suite run, no completion label
accepted). This correction addresses root §Cross-owner C2 finding and user
correction instruction; it does NOT claim whole-operation completion. No Human
commit readback, no ordinary commits, no Git config/network/Production/old-runner/
cleanup. AST-only now (no shared candidate test execution while others edit).

Working source:
`.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`
(all C2 paths below relative to it).

Binding order: contract a345bb95 INCLUDING §11, precode §5, ROOT FULL 0425c530
INCLUDING §5, independent §§8–9 FINAL-BINDING, then R3 overridden by R4 + 5
literal schemas + R5 families + R6 roles, then ROOT. A2 LOW exact API is required
installed G76 dependency (not optional).

## 1. Root C2 finding addressed (no optional LOW, full READY, exact API)

Root: “C2 adds multiple import/attribute/guard fallbacks and catch-all paths.
LOW is a required installed dependency of G76, not optional. Required normal
publication/editorial/renewal paths after a valid upstream correction must work;
a blanket superseded-mode refusal cannot satisfy the required positive witness.”

Fixed in all 12 C2 scripts (see §3):

- Removed all `try: from LOW … except: pass`, `getattr(_low, …)` optional
  dispatch, `require_no_active_guard` guard-only fallback, local `os.lstat`
  fallback, and `except Exception: continue/pass` content-invalid swallowing.
  Replaced with direct required `from scripts import survey_research_authority_v2
  as _low` + direct `_low.require_research_operation_ready(repo_root, state_path)`
  (full guard + completion exact verify: checkpoint SHA + COPY-derived
  expected_after + seven_plan). No `hasattr`, no `callable` check, no fallback
  to legacy/canonical. Content-invalid propagates (fail-closed).
- All mutating entries call full READY at entry AND before each publish
  (prepublish). Added prepublish in: release_checkpoint (before checkpoint write),
  weekly_refresh (before receipt install), execution_record init (before index/
  session writes), reader_publication manuscript (before manifest write),
  retention capture (before manifest publish), editorial_publication prepare
  (entry + before build-transfer writes), publication Freeze (before install).
  Diagnostic `validate`/`verify_retention`/`observe` paths intentionally do NOT
  require guard absence (read-only, NOT write permits) — documented, not permission.
- Exact A2 LOW API used (no placeholder shapes):
  `load_typed_checkpoint_record(repo_root, path) -> {family, record}`,
  `resolve_research_authority(repo_root, state_path) -> {family, checkpoint,
  artifacts, lineage}` (artifacts = 4 parsed NamedRefs, lineage = checkpoint_path/
  sha + parent/original/supersedes + triplet),
  `check_supersession_record_from_paths(repo_root, checkpoint_path, report_path,
  before_copy_path) -> list[str]` (available for revision validation; C2 P1/P2R
  observers use resolve path, HIGH owns revision adoption).
  Structural `_resolve_research_from_state_bytes` alone is NEVER used as typed
  full content validation; retained graph trace calls full-path LOW with safe
  COPY binding (retained COPY bytes == request.before_state.sha, basis stays
  canonical LIVE path, never rebound to COPY) and preserves P1/P2R/P2V full
  predicates (agent validators + `validate_proposal`/`verify_retention`/scope
  still run; no verified flags or fabricated defaults).
- Positive G76 paths work (not blanket refuse): when LOW returns PREARCH family
  with valid 4 refs + completion, C2 readers/writers continue with new refs
  (e.g., editorial_correction `_ckpt_resolve` validates 4-name set + lineage via
  full LOW, then agent resolver still runs P1 predicates; manuscript/Freeze/
  retention proceed after READY passes). Only wrong-family at publication sites
  refuses (see §2). Old canonical Ledger/Completeness are history-only after
  adoption, never fallback.
- Wrong-family checks use EXACT `reason == REVIEWED_ACCEPTED_UPSTREAM_CORRECTION`
  (not `reason_class`), fail BEFORE CANONICAL fallback. Original validation 557
  expected `DRAFT_COMPLETE→VALIDATED_DRAFT` + `validation` in checkpoints (ROOT-
  corrected, not downstream graph). Release payload 121 expected `FROZEN→RELEASED`;
  refresh 931 expected refresh validation; all refuse PREARCH even if parses.
- All 9 pubset selectors/chainwalkers have actual codes (not comment-only):
  1992 selection pointer (PREARCH → WRONG_FAMILY, never CANONICAL), 2151 artifact
  roles (PREARCH roles not in allowed → refuse before read), 2215 candidate fast
  path (PREARCH pointer → central selection → refused), 2253 mode probe (explicit
  PREARCH test BEFORE versioned test; legacy → CANONICAL, unknown → fail-closed),
  2267 branch guard (inherits mode), 1120 walk (via `_load_record_file` refuse),
  1308 legacy rows (research roles never rebind + explicit PREARCH refuse before
  reason dispatch), 1437 activation supersedes (publication predecessor only),
  1583 KEEP/profile (proposal-dir check), 1646 before-digest (legacy vs versioned
  branches; PREARCH hits neither → refuse), 1874 selection-anchor (same
  non-publication-role + cumulative prior_sha). Existing legacy/control paths
  preserved (strict legacy/known-versioned cases retained).
- Test fixture copy lists include 2+5 explicitly (lists, not counts, protected
  actual parent, pinned SHA + drift checks, copy-if-present until A lands — now
  present): `scripts/survey_research_authority_v2.py`,
  `scripts/survey_prearchitecture_acceptance_v2.py` + 5×
  `schemas/dm022-*.schema.json` in P1/P2R/P2V helpers + new C2 test file.
- Tests rewritten to whole public paths + healthy controls (no helper-only
  manufactured exceptions, no writer mocks): `resolve_publication_mode` None →
  CANONICAL + PREARCH → WRONG_FAMILY (real files, no-read/no-write snapshots),
  artifact/stage research names refuse before read, activation PREARCH refuses,
  LOW typed classification boundary, READY full-completion fail-closed, independent
  GitDB commit discipline. See `tests/test_survey_dm022_c2_consumers_v2.py`.

C1 owns history/renewal/deriv/P3S/config — not edited; B owns agent, A owns A2
LOW — not edited. API needs reported in §4.

## 2. Exact C2 paths changed (disjoint, no cross-owner edits)

- `scripts/survey_publication_set_v2.py` — removed unwired resolver helper; added
  explicit PREARCH refuse in 1308 chain dispatch + kept mode/activation/prior/
  artifact/stage guards. No research 4-ref resolution here (F4b split correct).
- `scripts/survey_release_checkpoint_v2.py` — required READY entry+prepublish;
  R6:121 typed-loader classification (LOW, exact `reason`) before legacy branch.
- `scripts/survey_weekly_mechanical_refresh_v2.py` — required READY entry+
  prepublish (before receipt install); R6:931 via LOW typed (removed local
  classifier dead code).
- `scripts/survey_execution_record_v2.py` — required READY entry+prepublish.
- `scripts/survey_reader_publication_v2.py` — required READY with derived
  canonical STATE (`source_root/production-state.json` via config); entry+
  prepublish.
- `scripts/survey_reader_surface_gate_v2.py` — required READY with passed
  `state_path` (exact State bind, no generic dict); no-State path refuses.
- `scripts/run_semantic_publication_v2_interactive_base.py` — required READY
  entry+prepublish.
- `scripts/survey_editorial_publication_v2.py` — required READY entry (after scope)
  + prepublish (before build transfer); explicit PREARCH recognition-or-refuse.
- `scripts/survey_editorial_retention_v2.py` — required READY entry (after
  State/Profile) + prepublish (before manifest publish).
- `scripts/survey_editorial_current_authority_v2.py` — full-path LOW lineage
  (`resolve_research_authority`) instead of structural dicts; content-invalid
  propagates.
- `scripts/survey_publication_v2.py` — required READY entry+prepublish in Freeze
  (derived STATE); explicit PREARCH refuse in Candidate/Release.
- `scripts/survey_editorial_correction_proposal_v2.py` — `_build_graph` threads
  `state_path`; `_ckpt_resolve` calls full-path LOW + 4-name + lineage checks
  while preserving P1 predicates; removed structural-only wrapper helper.
- Tests: `test_survey_editorial_correction_proposal_v2.py`,
  `test_survey_editorial_retention_v2.py`,
  `test_survey_editorial_current_authority_v2.py` (2+5 copy lists) +
  rewritten `test_survey_dm022_c2_consumers_v2.py` (whole paths + controls).

AST parse OK (no import/cache) for all 12 scripts + 4 test files.

## 3. Map contradictions (return to Astra before broadening: NONE new)

No new predicate/closure contradiction found in C2 scope. R6 row14 label, mode
`else CANONICAL` overbreadth, F4a/F4b split, `reason` vs `reason_class` already
match ROOT. If any required predicate/walker cannot be included without
weakening, return exact blocker and revisit A1 vs A2 (decision §9/§11.4) — none
triggered here; partial-guard A1 not implemented.

## 4. Exact remaining counterparts / API / open issues (honest, NOT complete)

- **C1 (history/renewal/deriv/P3S/config)**: C2 relies on C1 for G76 pipeline76/
  replay70/union73/canon36+41 as planned memberships (not measured source),
  `verify_renewal_source_proof` CURRENT 70/73/36/41 member-wise checks, and
  `config/survey-production-v2.json` pipeline71→76 registration. Need: C1 exact
  branch table for `_recompute_contract8_at_epoch`, `_derive_tool_generation`,
  `_expected_staged_code_deps`, CURRENT closures at G76 + historical OWN-epoch
  handling. C2 does NOT edit these; integration snapshot must bind C1 + C2.
- **B (agent)**: C2 calls `agent.resolve_checkpoint_artifact`,
  `resolve_active_evidence_views`, `validate_agent_state`,
  `require_active_or_canonical`/`assert_canonical_publication_mode`. Need: B
  PREARCH branches at 489/819 (upstream 3 roles + 4-name + SELF/proof) + 348/365/
  761/902/1608/1703/1768 dispositions per R4. C2 does NOT edit agent.
- **A/A2 (LOW/HIGH)**: C2 calls exact A2 LOW API above. Need: A2 corrected HIGH
  IO/resume/proof/contract pinning (root §§A1–A7) + 5 installed schemas byte-
  identical to proposals except intentional registry retarget. C2 does NOT edit
  LOW/HIGH/schemas.
- **C2 prepublish coverage**: entry+prepublish wired for release/weekly/execution/
  manuscript/retention/prepare-build/Freeze paths above. Remaining mutating
  entries (editorial_publication finalize/activate/resume, publication candidate/
  approval/visual/bundle writers, reader Gate manuscript builders without State)
  share the same `_dm022_require_ready` helper but their call sites are NOT yet
  wired to pass `state_path` (they lack State param today). Per R4 they require
  explicit State/Profile path param or fail-closed if cannot bind — that param
  threading + per-site prepublish is OPEN (helpers exist, not yet wired). Hence
  NO completion claim: helpers alone are not witness.
- **Positive G76 end-to-end**: C2 positive paths (resolve + READY pass → continue)
  are implemented, but whole-operation witness (Weekly+Thematic full 4-artifact
  acceptance, affected/unaffected semantics, old/new/unknown State, guard/
  completion loss, stale Raw/HEAD, close/replace/ownership faults, late seams,
  explicit resume, normal forward Architecture/Draft/publication + history
  readback, G76 correction → initial publication → editorial/renewal, G71→G76
  unchanged-upstream control) requires fixed complete snapshot + all owners
  bound + independent GitDB fixtures + independent implementation review. NOT run
  here (AST-only by instruction; no shared candidate execution while others edit).
- **Tests**: rewritten C2 tests cover whole public selectors + healthy controls +
  no-read/no-write + GitDB discipline (AST OK, NOT executed here). Affected
  regressions NOT run (would touch files others are changing).

No stub/closed-dict/readonly-helper-only completion claims. No synthetic genuine
approvals. No old test-count/PASS transfer. Whole NOT_READY/step4B3OPEN/
audit unstarted/DM021+022OPEN preserved except implementation progress.
Stop at Commit Point; independent implementation review required before closeout.
