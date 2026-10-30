# Owner-B lifecycle correction — 2 blockers (strict family + accepted-authority drafting)

2026-10-28. Implements `astra-lifecycle-blocker-resolution.md` §§1–2 on B-owned
paths only. Whole-lifecycle Attempt3 (`whole-lifecycle-witness-progress.md`
§Attempt3 + dual repro `dm022-dual-repro-20261028T163326Z.txt` SHA
`4c9c3ec5…` + probe `dm022-dual-repro-probe.py` SHA `67efd4e6…`) is the
failure authority; no whole PASS claimed. No ordinary commits, no Human
readback, no Gitconfig/network/cleanup. A Screening wrapper unchanged; no
foreign source patched (C1/C2 read-only). Unit ongoing — root must review; no
fake milestone.

Working source: `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`.
Private verification copy (B-safe only, no longitudinal foreign-source test):
`/tmp/dm022-b-lifecycle-private-20261028T180000Z` (758 files, 0 pycache,
`tar --exclude=.git --exclude=__pycache__` from current source after own edit;
B file SHAs below). Runtime pins: `Python 3.14.4`, `PYTHONDONTWRITEBYTECODE=1`,
no `GIT_*` overrides, process-scoped fixture identity, inert example.invalid
origin, no alternates. Raw unique:
`/tmp/dm022-b-lifecycle-raw-20261028T180000Z.txt` (51 lines, SHA256
`bd17c5dd53a9e98d3b5c8c35bb7bb092dbd6bcbb269753831d2d55e264e6ee3f`,
`Ran 19 tests OK`, exit 0). B test file SHA256
`c634fa32c90d0dd2fc55949d814a0a4a8c3783db7dc273903011a3030de9052d`.

## 1. Blocker1 — same-triplet heuristic replaced by strict pinned-record family

Root cause (dual repro Part A): LEGACY same-triplet EVIDENCE_REVIEWED (all
three refs to `checkpoint-evidence.json` sha `8e8a0acb…`) made
`_dm022_is_prearch_state` True, while `low.resolve_research_authority`
correctly returned LEGACY (legacy kind). Runner trusted the heuristic and
refused the LEGACY answer instead of using the healthy legacy branch
(`agent.resolve_active_evidence_views` + canonical Ledger/Completeness
`28f53106…`/`7778410e…` all present/valid).

Fix (B-owned only, no heuristic, no fallback after exception): each B consumer
reloads the pinned evidence checkpoint and inspects the strict typed family
via required `low.load_typed_checkpoint_record(repo_root, repo_root /
ev["path"])`. `PREARCH` → PREARCH branch (artifact_refs, no canonical
fallback); `LEGACY` (including healthy LEGACY same-triplet) → legacy branch;
loader raise (malformed/missing/drift/unknown kind) propagates fail-closed,
never falls back to the other branch.

Exact paths/lines (candidate-work):
- `scripts/run_selection_architecture_v2_interactive.py:50`
  `def _dm022_pinned_family(repo_root, state) -> str` (replaces
  `_dm022_is_prearch_state`); call sites `:81` (`_dm022_resolve_ledger_completeness`)
  and `:269` (`run` four-ref branch).
- `scripts/run_drafting_synthesis_v2_interactive.py:48`
  `def _dm022_pinned_family(repo_root, state) -> str`; call site `:85`
  (`_upstream` R4 branch).
- `scripts/survey_handlers_v2.py:40`
  `def _dm022_pinned_family(repo_root, state) -> str`; call sites `:80`
  (`_dm022_verify_handoff_four_refs`) and `:421`
  (`validate_drafting_synthesis` R4 evidence binding).
- `scripts/survey_stage_validation_v2.py:194`
  `def _dm022_pinned_family(repo_root, state) -> str`; call sites `:220`
  (`_dm022_verify_current_r4`) and `:332` (`_prior_artifacts` wrapper check).
- `scripts/survey_agent_control_v2.py:110`
  `def _dm022_pinned_family(repo_root, state) -> str` (strict); old
  `def _dm022_state_kind(state)` kept with deprecation note (unused for
  routing, must not be used). `run_evidence_v2_interactive.py:624-631`
  already used the strict pattern (kept).
- Deleted: all `_dm022_is_prearch(state)` / `_dm022_is_prearch_state(state)`
  triplet-equality heuristics in B scope (verified zero remaining via grep).

No B diagnostic now infers PREARCH from shape; classification always precedes
expected role, full artifact proof follows via the A3 4-path checker (not
downgraded).

## 2. Blocker2 — accepted-authority drafting facade (no Screening relax)

Root cause (dual repro Part B, zero DM022): `prepare_package` pins
`basis.state_sha256` = live State SHA at ISSUE_INITIALIZED;
`validate_package_basis` (`survey_screening_v2.py:704-707`) requires current
live SHA to still equal that pin, so any faithful forward advance (real
`build_stage_checkpoint`+`advance_with_checkpoint`, Part B transcript) makes
`survey_drafting_v2_base._load_drafting_basis:389` →
`_resolve_effective_screening_discovery:244` fail with
`Screening package basis drift: state_sha256`. Merely documenting the loader
as “pure” did not wire the existing content path (`_load_drafting_basis_content`,
`_resolve_effective_screening_discovery_content`, arch content Matrix
rederivation). A creation wrapper stays strict and unchanged.

Fix (B-owned mapped modules only; new public path-based wrapper, not a new
runtime module/authority):
- `scripts/survey_drafting_v2_base.py:540`
  `def derive_draft_package_from_accepted_state(repo_root, state_path,
  profile_path, discovery_path, screening_path, evidence_path, views_path,
  ledger_path, completeness_path, matrix_path, selection_path,
  architecture_path, review_summary_path, approval_path, package_id)`.
  Reloads full canonical State/Profile via `state_path` (+ `core.DEFAULT_CONFIG`,
  `agent.validate_agent_state` must be `[]`); requires `ARCHITECTURE_ESTABLISHED`
  + approved Architecture gate + passed research/Selection/Architecture
  checkpoints; binds `profile_path` to State profile path/sha and
  `approval_path` to `human_gate_provenance.architecture_review` path/sha;
  resolves active four-ref via `agent.resolve_active_research_four_refs`
  and enforces supplied evidence/views/ledger/completeness path+sha equal
  `artifact_refs`; enforces matrix/selection/architecture/review are the
  canonical `source_root` fixed names; derives private
  `expectations={issue_id,research_profile,canonical_state_path=rel(state_path)}`
  + `root_records=screening.read_jsonl(discovery_path)` + `root_path`
  (never caller-verified); calls full `_load_drafting_basis_content` +
  effective Screening content + arch content Matrix rederivation (historical
  Screening + active four-ref graph, DIRECT/DERIVED_EXPANSION, raw/JSON
  binding, source paths, Profile, Matrix rederivation, approval all mandatory);
  then normal package generation (same row/identity/card/basis as the
  preparation path, no State SHA, no skip flag, no old-State fake, no re-pin).
  Direct package-creation callers stay on `derive_draft_package` (preparation
  checks, StateSHA wrapper intact).
- `scripts/survey_drafting_v2.py:370`
  `def derive_draft_package_from_accepted_state(...)` (same signature +
  `state_path`): forwards direct packages to the base facade; handles the
  bounded cross-package synthesis package via the same content authorities
  (reference IDs from other placed packages, SUPPORTING inputs, same
  row/identity/card/basis checks).
- `scripts/run_drafting_synthesis_v2_interactive.py:214`
  runner now calls
  `drafting.derive_draft_package_from_accepted_state(root, state_path, ...)`
  (State-path threading; `implementation_sha` no longer threaded to drafting).
  `_upstream` R4 + matrix Evidence binding + READY entry/prepublish unchanged.

Screening: `survey_screening_v2.py` untouched (creation wrapper still pins +
checks live SHA for preparation callers; content helpers already existed and
are now actually called). No global relaxation, no `skip_current` flag, no
caller dict, no re-pin.

## 3. Real regressions added (B test file, private-copy run)

File: `candidate-work/tests/test_dm022_prearch_b_ordinary_consumers_v2.py`
(SHA `c634fa32…`, 19 tests). `test_01-15` retained (SizedRef correction +
full PREARCH + guard split intact). New B-safe tests use real chain helpers
(`test_survey_evidence_v2.make_chain/sandbox/init_profile`,
A2 `_make_evidence_reviewed_state/_prepare_and_decide` + real HIGH adopt),
never minimal invalid CP, mock LOW proof, or self-raised errors:
- `test_16_healthy_legacy_same_triplet_uses_legacy_canonical`: A2
  EVIDENCE_REVIEWED LEGACY same-triplet → pinned family LEGACY in runner/
  handlers/stage; R4 resolver returns canonical paths; legacy two-ref resolve
  succeeds; no PREARCH error, no writes.
- `test_17_prearch_pinned_family_routes_r_refs_no_canonical_fallback`: full
  PREARCH via HIGH adopt → pinned family PREARCH; ledger/completeness are
  versioned R paths (!= canonical, files exist); four-ref returns
  `artifact_refs` 4 NamedRefs; no canonical fallback.
- `test_18_stage_advance_then_drafting_accepted_authority`: real screening
  package + stale copy (same canonical path, different valid SHA simulates
  post-advance drift): old `validate_package_basis` refuses `state_sha256`
  (preparation strictness preserved); new content
  `_validate_screening_package_basis_content` + `_resolve_effective_..._content`
  with expectations/root records still validates; no writes either path.
  Full public advance→Drafting longitudinal is covered by the longitudinal
  author (awaiting ROOT foreign-source fix); this is the B-safe helper-level
  proof that the accepted-authority path bypasses State SHA without weakening
  the creation gate.
- `test_19_stale_refs_fail_no_write`: stale/missing Discovery/Matrix/Selection/
  Architecture/Review/Approval bindings via `_load_drafting_basis_content`
  refuse (any error) with file set identical before/after (no writes). Split
  State refs are covered by the same-record triplet refusal in B resolvers
  (existing `test_07` + full-State tests); package/archive staleness is
  covered by `_historical_raw_authority_hashes` R4 tests (`test_12`).

Private run (B-safe only): 19/19 OK in 9.1s (ResourceWarnings only from
tempdir cleanup). Longitudinal full-lifecycle (Draft→REAL PDF→receipt/Gate/QA/
Candidate→editorial/renewal→G71→G76, C1/C2 foreign scope) is NOT run here;
awaiting ROOT disposition of C1/C2 + independent review. No whole PASS claimed.

## 4. Exact new API / pin boundaries + caller changes needed

- New API (B): `derive_draft_package_from_accepted_state(repo_root, state_path,
  profile_path, discovery_path, screening_path, evidence_path, views_path,
  ledger_path, completeness_path, matrix_path, selection_path,
  architecture_path, review_summary_path, approval_path, package_id) -> dict`
  in `survey_drafting_v2_base.py:540` + same-shape forwarder in
  `survey_drafting_v2.py:370`. Pins: State/Profile reload + `validate_agent_state==[]`,
  `ARCHITECTURE_ESTABLISHED` + approved gate + passed checkpoints, approval
  provenance path+sha equality, four-ref `artifact_refs` path+sha equality,
  canonical Matrix/Selection/Architecture/Review fixed rels,
  `expectations.canonical_state_path == rel(state_path)`,
  `root_records = read_jsonl(discovery_path)` + `root_path = discovery_path`.
- Callers: `run_drafting_synthesis_v2_interactive.py:214` threads `state_path`
  (already has it from `_upstream`); no other B caller needs changes (handlers/
  stage_validation already pass R4 paths; orchestrator/bridge/human_gate
  unchanged). C1 (`survey_versioned_renewal_source_v2.py:1207` already calls
  `_load_drafting_basis_content` with session expectations/roots) needs no
  change; if C1 ever calls the old StateSHA drafting basis after forward
  progress it must migrate to this accepted-state facade (return to Astra
  first; B does not patch C1). C2: no changes required by this fix.
- Cross-owner recursion request (B does not edit foreign scope): C2
  `survey_reader_surface_gate_v2.validate_reader_surface_gate(..., state_path)`
  calls writer READY inside a diagnostic validator that B `stage_validation`
  invokes with `state_path` (DRAFT_COMPLETE/VALIDATED_DRAFT). Split it as
  `evaluate_*` already does: diagnostic replay (retained lineage, no guard,
  no READY) vs mutating producer entry (READY entry + prepublish with
  explicit canonical State). Until then B keeps passing `state_path` (required
  by current C2 signature) with READY already enforced at `validate_stage`
  entry; no B recursion (B diagnostics never call READY; LOW detached proof
  never calls operational READY; writers refuse while held).

## 5. Status (honest, no milestone)

B blockers closed in code as far as B-owned files reach; 19/19 B-safe tests
green in the private copy. Remaining whole-lifecycle proof (present-old-7slot
retain/clear/regenerate, Draft/reader, REAL PDF, receipt/Gate/QA/Candidate,
editorial/renewal, Preview/Freeze/Release, G71→G76, affected regressions +
independent review) stays with General + C1/C2 + ROOT; whole NOT_READY/step4B3
OPEN preserved except pre-code gate. No Production/W40/adoption claim. Stop at
Human Commit Point; ordinary Commit/Push Human-owned.

Author: Owner B.
