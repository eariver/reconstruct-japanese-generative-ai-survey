# DM022 C1 author return (implementation, NOT run, NO acceptance)

2026-10-28. C1 owner (generations/derivation). Human continuation authorized
actual CODE in ONLY
`.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`.
No Human commit/push readback. No ordinary commits. Tests NOT run; no
acceptance manufactured. Saved unique raw runs required later with fixed
snapshot + independent implementation review.

## 1. Authority read (binding)

- Assessment `outputs/rephase-1-dm022-prearchitecture-precode-assessment.md` §5.
- ROOT `notes/rephase-1-dm022-prearchitecture-precode/astra-precode-gate-resolution.md`
  INCLUDING §5, full SHA256 `0425c5300c9c7211e4468d3b842c4e3af1acb9f5bf1eba00e90f7ba72ef44a5a`/13788B.
- Selected contract `outputs/rephase-1-dm022-prearchitecture-contract-decision.md`
  INCLUDING §11, SHA256 `a345bb9524b4dfc5b5f32600d0d708687e2b6131d91a43965c97b6418388f223`/31351B.
- R4 `integrated-readiness-r4.md/json` + 5 literal `schema-proposals-r4/*.schema.json`
  (request `a99f0dc1…`, manifest `e7534d01…`, proof `a79c0920…`, report `21369608…`,
  checkpoint `fd39c246…`), 40 rows, 17 sites + 8 branches.
- R5 `integrated-readiness-r5-family-map.md/json` (12 `per_function_branches`,
  G67 67 / G71 71 / G76 76, 50/63/70/73, 29/34/36/41 literal).
- R6 `integrated-readiness-r6-role-map.md/json` (17 sites + 9 discriminators +
  9 chain walkers + 9 selectors; replaces R5 `per_function_branches[7]`).
- Independent `independent-readiness-review.md` §§8–9 FINAL-BINDING (PRE_CODE_READY,
  map only; B-L1/B-L2/B-L3 adopted by ROOT §5.1).
- Coordination `notes/rephase-1-dm022-prearchitecture-implementation/astra-implementation-coordination.md`
  (disjoint ownership; C1 scope below).

Precedence: R3 retained mechanics OVERRIDDEN BY R4 + 5 schemas + R5 families +
R6 roles, then ROOT. R6 replaces R5 overbroad publication-chain wording.

## 2. Ownership respected (EXACT, no cross-edit)

C1 edited ONLY (relative to candidate-work):

- `scripts/survey_versioned_renewal_history_v2.py`
- `scripts/survey_versioned_renewal_source_v2.py`
- `scripts/survey_versioned_renewal_v2.py`
- `scripts/survey_weekly_derivation_v2.py`
- `scripts/survey_longform_derivation_v2.py`
- `scripts/survey_longform_generated_v2.py`
- `scripts/survey_editorial_staged_source_v2.py`
- `config/survey-production-v2.json`
- NEW C1 tests/helpers (below)

Did NOT touch: A `survey_research_authority_v2.py`,
`survey_prearchitecture_acceptance_v2.py`, 5 `schemas/dm022-*.schema.json`,
`survey_evidence_v2.py`, `survey_screening_v2.py`, `survey_completeness_v2.py`;
B agent/normal consumers; C2 P1/P2R/P2V/publication. No config writes outside
owned config file. No Git fixture objects in reconstruct DB.

Method: `Read` + `Edit`/`Write` only. AST parse as DATA for syntax check
(no `scripts.*` imports, no cache, no test execution) during shared edits.
No old runner execution, no restore/network.

## 3. What C1 implemented (concrete R5 branches as narrowed by R6/ROOT)

### 3.1 History historian (`survey_versioned_renewal_history_v2.py`)

- Added `_NEW_DM022_SCHEMAS_5` (5 DM022 schemas) + `_NEW_DM022_MODULES_2`
  (HIGH + LOW). Counts planning membership only; exact membership verified
  member-wise vs actual imports/contract.
- `_recompute_contract8_at_epoch`: accepts EXACT G67 OLD67 (67) / G71 NEW71
  (71=OLD67+4new) / G76 NEWDM76 (76=NEW71+5dm022); delta ONLY 5 DM022 for G76.
  Unknown set → `UNSUPPORTED_MIGRATION`; mode/blob missing → FAIL. Same
  NUL-framed aggregate + versions/quality(3)/profiles(3+2) checks unchanged.
  Narrow G71→G76 mechanical compat ONLY, SAME authority.
- Added `_normalize_generation` (OLD==G67, NEW==G71, G76 canonical; unknown
  → UNSUPPORTED). `_expected_receipt_closure` / `_expected_staged_code_deps`:
  G67→50, G71→63, G76→70 (63+2+5); union73 via set union elsewhere. Exact
  set equality, name==path, no alias, sorted-unique. Counts not authority.
- `_derive_tool_generation`: probes 7 renewal + 7 DM022 paths via
  `_git_tree_mode` at OWN epoch (mode 100644), owned-epoch config pipeline
  exact 67/71/76 + versions/quality/profiles + Contract8 + schema fingerprints
  + module/mode/membership (never presence/count). Returns G67|G71|G76
  (not OLD/NEW): 14+NEWDM76→G76; 7+NEW71→G71; 0+OLD67→G67; 7+OLD67→REJECT;
  partial→UNKNOWN; 0+NEWDM76→BLOB_MISSING FAIL. Callers handle three values;
  explicit generation must equal derived after alias normalization
  (OLD==G67, NEW==G71) else `HISTORY_TOOL_EPOCH_DRIFT`. No caller flag.
- `_verify_staged_code_deps_exact`: alias-normalized comparison, `_want`
  50/63/70. Epoch OWN, never live HEAD.
- `OWNER_REGISTRY`: added 5 DM022 rows (request/manifest/proof/report/
  checkpoint, `""` pointer, fixed file + validator). Publication revalidation
  chain MUST NOT gain PREARCH (R5 overbroad revoked); these rows are for typed
  upstream history via LOW detached path only.
- `_KNOWN_SCHEMA_SHAS`: added 5 DM022 paths with R4 proposal SHAs as known
  history (`a99f0dc1…`, `e7534d01…`, `a79c0920…`, `21369608…`, `fd39c246…`);
  old known sets preserved; unknown foreign SHA still `UNSUPPORTED_MIGRATION`.
  Implementation SHAs to be pinned after A installs `schemas/` files (requires
  A coordination; documented here, not silently auto-allowed). Current proof
  checks CURRENT every readback.
- Publication chain hardening (R6): added `PREARCH_KIND` /
  `PREARCH_REASON` + `_is_prearch_record` (exact kind+reason). `_is_legacy` /
  `_is_editorial` / `_is_renewal` already return False for PREARCH (exact
  pairs). `_record_kind`: PREARCH → `HISTORY_DIGEST_MISMATCH`
  `DM022_WRONG_FAMILY` (never CANONICAL fallback, no auto-upgrade); LEGACY|
  EDITORIAL|VERSIONED unchanged; unknown → refuse. `_walk_chain_backwards` /
  `_verify_editorial_ancestor` / `_verify_versioned_ancestor` unchanged
  (publication `supersedes` only, never research lineage, never
  `agent.validate_agent_state`). Detached upstream PREARCH reads stay via LOW,
  never this chain. Each chain keeps own predecessor/anchor checks.
- Historical G67/G71 verification stays OWN-epoch (retained COPY/lineage +
  `supersedes`/parent/anchor + SELF/digest, no live-before equality). Current
  G76 supports new PREARCH through initial publication/editorial/renewal +
  normal lifecycle (§11.2 readback, no entry-window re-check, no
  HEAD==historical equality).

### 3.2 Source leaf (`survey_versioned_renewal_source_v2.py`)

- `_expected_closure_names(route, family="G76")`: G71→63, G76→70 (63+2+5),
  G67→50 historical. Family derived OWN epoch, never caller flag. Added
  `_expected_closure_names_for_family` explicit variant.
- `verify_renewal_source_proof`: CURRENT G76 70 per-route / 73 union,
  member-wise vs actual imports/contract + current committed source (not
  length); contract_identity vs supported; schemas vs current disk;
  supported==observed + sorted order; HIST verdict owner-epoch-bound.
  Never calls agent/State/Reader/Gate/Candidate/seal/P1/P2R/P3S. Family label
  alone confers no permission; ordinary U/C recompute ALL current proofs.
- `_control_paths_for_current`: lexical only (unchanged); G76 5 schemas via
  config-registered `contract_files` (not hardcoded). Epoch=G76 commit, HEAD
  descendant, control diff quiet per R4 head rule, rows live==committed at
  BOTH epoch+HEAD, dirty/staged/untracked control refusals unchanged.
  Artifact-only descendant strict conditions preserved.

### 3.3 HIGH renewal (`survey_versioned_renewal_v2.py`)

- Two CURRENT closure call sites (`OBSERVE`, `PREPARE`) now request G76 (70)
  as CURRENT; historical stays OWN-epoch via hist verifiers. No window change:
  renewal entry ineligible at EVIDENCE_REVIEWED (DM022 uses HIGH
  prearchitecture_acceptance, not renewal prepare) – R5 HIGH branch preserved.
  Existing full strict LIVE State validation retained; no current State in
  source leaf.

### 3.4 Weekly/Longform canonical (`survey_weekly_derivation_v2.py`, `survey_longform_generated_v2.py`)

- Weekly: `_CANON_WEEKLY_G71` (29 literal) + `_DM022_7` (2+5) →
  `_CANON_WEEKLY_G76` (36, sorted). `CURRENT_CLOSURE` = G76 (36) CURRENT;
  historical G71 (29) stays valid OWN-epoch. `verify_closure_at_commit`
  accepts G71 29 OR G76 36 exact (branch on length, exact membership); CURRENT
  `_verify_head_bytes` requires G76 (artifact-only descendant + control diff
  quiet + dirty/staged/untracked refusals + live==committed at BOTH).
- Longform: `_CANON_LONGFORM_G71` (34) + `_DM022_7` → `_CANON_LONGFORM_G76`
  (41). Same CURRENT/historical split. Counts not authority.
- No old report epoch forced to current publication HEAD: historical receipts
  verify OWN epoch via retained bytes/git-show, never live equality; current
  validates NOW with fresh tools; no `old acceptance-report commit == new
  publicationToolHEAD` requirement (otherwise future G76→G76 renewal would
  brick). Full current publication proof still fresh current tools.

### 3.5 Longform derivation (`survey_longform_derivation_v2.py`)

- Docstring DM022 compliance note only (no behavior change): G76 lineage valid
  through initial publication/later renewal; historical OWN-epoch; no PREARCH
  publication activation; LOW detached only upstream; HIGH LIVE validation
  retained; U/C recompute ALL; SAME authority; preserves chain limits + R1
  canonical after versioned refusal. No current State in leaf; no HEAD forcing.

### 3.6 P3S staged (`survey_editorial_staged_source_v2.py`)

- Added `_DM022_PY_2` + `_DM022_SCHEMAS_5`; `_SHARED_PY_G71` (35) /
  `_SHARED_SCHEMAS_G71` (22) historical; `_SHARED_PY_G76` (37) /
  `_SHARED_SCHEMAS_G76` (27) CURRENT. `_SHARED_PY`/`_SHARED_SCHEMAS` default
  to G71 for backward compat; `_route_code_deps(route, family="G76")`:
  G71→63, G76→70 (37+27+3+1+1+1). Family derived, never caller flag.
- Materialize CURRENT uses G76 (70). Verify accepts G71 (63) historical
  OWN-epoch OR G76 (70) current (tries G76 then G71, exact path match).
- Edge audit: actual top-level imports must be subset of G76 shared set;
  extra → `CODE_DEPS_EXPANSION_REQUIRED` (return to Astra, never silent omit).
  Lazy P2V import stays function-local in materialize (never in verifier
  closure); DM022 modules file-pin-only here (HIGH owns writes). Runtime root
  proof (`_check_runtime_binding`) without test preloads; full new transitive
  closures (discovery/X + 3 renewal + lazy P2V) preserved. No reload/rebind.

### 3.7 Config (`config/survey-production-v2.json`)

- Pipeline 71→76: appended 5 DM022 schemas (request/manifest/proof/report/
  checkpoint). Versions/quality/profiles unchanged. Contract8 recompute now
  covers 76. Control roots unchanged (lexical). No other config change.

## 4. New C1 tests/helpers (NOT run)

- `tests/dm022_c1_fixture_helpers_v2.py` (C1 owned shared helper):
  `DM022_NEW_MODULES_2`, `DM022_NEW_SCHEMAS_5`, `DM022_NEW_UNTRACKED_7`,
  explicit G67/G71/G76 pipeline (67/71/76), staged (35/22 vs 37/27),
  receipt (63 vs 70, union 73), canon (29/36, 34/41) counts; `init_independent_repo`
  (inert `example.invalid` origin, process-scoped `dm022-c1-fixture` identity,
  no `alternates`), `commit_all` (40-hex epoch), `write_file`, `make_prearch_record`,
  `make_legacy_record`. Explicit copy lists include new untracked 2+5.
- `tests/test_dm022_c1_family_closure_v2.py`: normalize aliases; receipt
  G71 63 / G76 70 + delta ONLY 2+5; unchanged-upstream control (G71<G76, staged
  mirrors); pipeline 67/71/76 constants; weekly 29/36 + longform 34/41 + delta
  2+5; staged 63/70; source G76 70; allowlist has DM022 + foreign SHA refuses.
- `tests/test_dm022_c1_research_graph_v2.py`: PREARCH identified upstream-only;
  `_record_kind` refuses PREARCH `DM022_WRONG_FAMILY` (never CANONICAL); legacy/
  editorial/renewal still accepted; unknown refuses (no auto-upgrade); G71/G76
  control no rewrite; independent fixture actual epochs (two meaningful commits,
  ancestor reachable, inert origin, no alternates, 2+5 explicit).

All tests use independent temp Git DBs only (no reconstruct objects, no ordinary
commits, meaningful synthetic contents, process identity). Source-committed
synthetic fixture DB later separately permitted (not done here).

## 5. Scope status (honest, no PASS)

- Implemented: concrete R5 helper branches for C1 files + R6 narrowing
  (publication chain refuses PREARCH; LOW detached only upstream). Historical
  fingerprints preserved; CURRENT checks CURRENT every readback; artifact-only
  commit strict conditions preserved (ancestor + control quiet + BOTH-epoch
  live==committed + dirty/staged/untracked refusals). Narrow G71→G76 mechanical
  compat SAME authority; U/C recompute ALL; no label auto-acceptance. G76
  lineage through initial publication/later renewal; no old-report→HEAD forcing.
  P3S lazy bindings + full closures. Chain/orphan/resume + R1 refusal preserved.
- OPEN (not in this return): A 2 modules + 5 schemas file install + final SHA
  pin update in `_KNOWN_SCHEMA_SHAS` (R4 SHAs pinned as history; implementation
  SHAs need A coordination); B/C2 rewiring; whole-operation witnesses
  (Weekly+Thematic, 7-slot, repeat, wrong-role, lifecycle/readback, G71→G76
  control, G76→initial→editorial/renewal, old/new/unknown State, guard/completion,
  close/replace/ownership, unsupported types, stale pins, late seams); affected
  regressions; fixed snapshot raw runs; independent implementation review;
  DM016/017, quality, audit, adoption, savings. Whole NOT_READY/step4B3 OPEN/
  audit unstarted/DM021+022 OPEN preserved except pre-code gate closed.
- Map contradiction: none new. R5 `per_function_branches[7]` overbreadth
  already revoked by R6/ROOT; C1 implements R6 narrowing (publication chain
  has NO PREARCH arm). If any required reader/closure/contract contradiction
  found later, return to Astra before broadening (per coordination).

## 6. Verification (explicit: NOT run)

- Syntax: `ast.parse` as DATA on all 7 owned scripts + 3 new test/helper files:
  OK (no imports, no cache). Config JSON valid, pipeline 76.
- Tests: NOT executed (shared-source parallel discipline; no isolated env with
  pytest/TeX in this unit; no fixed snapshot yet). No PASS claimed, no
  test-count transfer, no fake pending/hash-only/schema-auto-allow.
- No `git status/diff/log` in workspace root (Human commit point preserved);
  no ordinary commit/push; no fixture objects in reconstruct; no network/restore.

## 7. Written paths (apply_patch via Edit/Write)

Source (candidate-work):

- `scripts/survey_versioned_renewal_history_v2.py` (APIs: `_NEW_DM022_SCHEMAS_5`,
  `_NEW_DM022_MODULES_2`, `_normalize_generation`, `_expected_receipt_closure`
  G67/G71/G76, `_expected_staged_code_deps` G67/G71/G76, `_derive_tool_generation`
  G67/G71/G76, `_verify_staged_code_deps_exact` alias-normalized,
  `OWNER_REGISTRY`+5 DM022, `_KNOWN_SCHEMA_SHAS`+5 DM022 (R4 SHAs),
  `PREARCH_KIND`/`PREARCH_REASON`, `_is_prearch_record`, `_record_kind`
  wrong-family refusal)
- `scripts/survey_versioned_renewal_source_v2.py` (APIs:
  `_expected_closure_names(route, family="G76")`,
  `_expected_closure_names_for_family`, CURRENT G76 70 in
  `verify_renewal_source_proof`, `_control_paths_for_current` G76 note)
- `scripts/survey_versioned_renewal_v2.py` (2 CURRENT sites → G76)
- `scripts/survey_weekly_derivation_v2.py` (APIs: `_CANON_WEEKLY_G71`,
  `_DM022_7`, `_CANON_WEEKLY_G76`, `CURRENT_CLOSURE`=G76, historical
  `verify_closure_at_commit` G71/G76)
- `scripts/survey_longform_derivation_v2.py` (DM022 compliance note)
- `scripts/survey_longform_generated_v2.py` (APIs: `_CANON_LONGFORM_G71`,
  `_DM022_7`, `_CANON_LONGFORM_G76`, `CURRENT_CLOSURE`=G76, historical
  `verify_closure_at_commit` G71/G76)
- `scripts/survey_editorial_staged_source_v2.py` (APIs: `_DM022_PY_2`,
  `_DM022_SCHEMAS_5`, `_SHARED_PY_G71/_G76` (35/37),
  `_SHARED_SCHEMAS_G71/_G76` (22/27), `_route_code_deps(route, family="G76")`
  63/70, verify accepts G71/G76, edge audit allows G76)
- `config/survey-production-v2.json` (pipeline 76)

Tests (candidate-work/tests, C1 owned):

- `tests/dm022_c1_fixture_helpers_v2.py`
- `tests/test_dm022_c1_family_closure_v2.py`
- `tests/test_dm022_c1_research_graph_v2.py`

Packet:

- `notes/rephase-1-dm022-prearchitecture-implementation/author-C1-return.md` (this file)

Full scope honest: C1 family/closure/typed-history consumption done per map;
no runtime proof, no adoption. Stop at coherent implementation Commit Point;
await fixed snapshot + independent review. Ordinary Commit/Push Human-owned.
