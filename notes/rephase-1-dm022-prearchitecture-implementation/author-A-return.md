# Owner-A implementation return — DM022 pre-Architecture research operation

2026-10-28. Owner A (research operation). Human continuation authorized ACTUAL
CODE in independent candidate; docs-only explicitly NOT the task. Binding
order: contract a345bb95 INCLUDING S11, pre-code assessment S5, precode packet
README, mandatory astra-precode-gate-resolution INCLUDING S5
(FULL 0425c530…/13788B), independent readiness SS8-9 FINAL-BINDING, then
R3 (overridden by) R4 + literal 5 schemas, R5 families, R6 roles, then ROOT.
No ordinary candidate/reconstruct Commit/Push; no fixtures in reconstruct;
no git config/global writes; no network/Production/reset/clean/old-log
overwrites. Python 3.14.4 + unittest/jsonschema/pypdf assumed; TinyTeX path
per coordination (availability only, no build executed here).

Working source:
`.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`
(all paths below relative to it). Started from prepared full742+inodes
sourceactual409 + inherited93; no ordinary source commit.

## 1. Exact written paths (Owner A ONLY, disjoint from B/C1/C2)

NEW (created by A, this unit):

- `scripts/survey_research_authority_v2.py` (LOW, detached, PATHS-only)
- `scripts/survey_prearchitecture_acceptance_v2.py` (HIGH, sole mutator)
- `schemas/dm022-revision-request-v2.schema.json` (literal R4 copy)
- `schemas/dm022-revision-manifest-v2.schema.json` (literal R4 copy)
- `schemas/dm022-revision-proof-v2.schema.json` (literal R4 copy)
- `schemas/dm022-preadoption-report-v2.schema.json` (literal R4 copy + ONE
  intentional B2 registry fix: first two `roleSchemaRegistry` entries retarget
  `notes/.../schema-proposals-r4/dm022-revision-proof-v2.schema.json` →
  `schemas/dm022-revision-proof-v2.schema.json`; closed/local registry, no
  dangling proposal path in installed source)
- `schemas/dm022-supersession-checkpoint-v2.schema.json` (literal R4 copy)
- `tests/test_dm022_prearchitecture_acceptance_v2.py` (Owner-A tests)
- `tests/dm022_prearchitecture_fixtures_v2.py` (Owner-A test-only helper;
  NEVER runtime authority, never enters source closures)

EXISTING A-owned (read, verified, NOT edited this unit):

- `scripts/survey_evidence_v2.py`, `scripts/survey_screening_v2.py`,
  `scripts/survey_completeness_v2.py` — all required S1.1 leaf cores already
  present (verified by AST inventory; zero missing); wrappers already preserve
  full old predicates via pure `_content` extraction from final93
  (P1/P2R-era delegation). No fake oldState, no global monkeypatch observed.
  A deliberately made NO edits to avoid breaking the inherited93 overlay or
  cross-owner compilation. If root's integration snapshot finds a wrapper
  predicate gap, A will patch narrowly on request.

NOT touched (other owners, concurrent edits respected):

- B: `survey_agent_control_v2.py`, selection/architecture/drafting/handler/
  stage/bridge/orchestrator/human-gate paths, four-ref/7-slot writers.
- C1: versioned-renewal/derivation/staged-source + `config/survey-production-v2.json`.
- C2: publication/editorial/retention/current-authority/reader/execution/
  release paths. Shared C1/C2 fixture helpers untouched.

## 2. Implementation API contract (stabilized for cross-owner compilation)

All signatures take explicit `repo_root: Path + PATHS`; no generic flags, no
caller-verified dicts, no readiness-bool tokens. Returns are exact shapes
below. R4 dict/planned-map returns apply (R3 `-> Path` superseded for
zero-write oracles); detailed R3 argument lists retained (no invented flags).

### LOW — `scripts/survey_research_authority_v2.py`

Top imports ONLY: `core.{repo_local_path,sha256_file,sha256_object,
sha256_bytes,json_bytes,load_json,parse_instant,iso_utc}` (exact symbols) +
`schema_gate` + stdlib. Every evidence/screening/completeness access is
function-local and calls ONLY R4 S1.1 pure cores. No agent/HIGH/public-State
validation; no canonical/State/guard mutation; guard reads are passive
lstat-only.

- `load_typed_checkpoint_record(repo_root, path) -> {family: LEGACY|PREARCH, record}`
  strict duplicate-key parse; kind absent -> old `stage-checkpoint-v2`
  validate; `PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1` -> new DM022 schema
  + operation/producer/checkpoint/artifact/SELF-digest checks; else refuse.
- `is_prearchitecture_record(record) -> bool` / `is_legacy_candidates_record(record) -> bool`
  pure discriminators (classification read, never adoption).
- `_resolve_research_from_state_bytes(repo_root, state: dict) -> {family, checkpoint_path, checkpoint_sha256, checkpoint_refs}`
  structural-only (path safety, same-record shape, kind dispatch); caller
  facade MUST have already called `agent.validate_agent_state`; no second
  validation, no guard/HEAD.
- `_load_typed_four_refs(repo_root, structural) -> {family, record, artifacts}`
  typed checkpoint FILE sha verify + 4 named artifact live re-hash loads.
- `resolve_research_authority(repo_root, state_path) -> {family, checkpoint, artifacts, lineage}`
  public path-reloading entry; State FILE structural peek + typed + four-ref
  + same-record triplet; zero writes.
- `load_revision_request(repo_root, request_path) -> dict` (installed schema).
- `derive_before_context(repo_root, request_path, before_copy_path, previous_checkpoint_path) -> {request, before_state, before_state_sha256, previous_checkpoint, old_checkpoint_refs, research_profile, issue_id, revision_id}`
  verifies COPY bytes == request.before_state.sha256; basis stays canonical
  LIVE path, never rebound to COPY.
- `build_revision_package_from_paths(repo_root, request_path, before_copy_path, output_dir) -> {package, tasks, planned_files}`
  pure; REJECTED->NON_MATERIAL / NEEDS_MORE->HOLD enforced; no CANDIDATES_NORMALIZED pretense.
- `build_revision_cards_views_from_paths(repo_root, package_path, request_path, results_dir, views_dir) -> {cards, views, planned_files}` pure.
- `accept_revision_evidence_views_from_paths(repo_root, package_path, results_dir, views_dir, profile_path, evidence_accepted_root, views_accepted_root) -> {evidence_acceptance, views_acceptance, planned_files}` pure.
- `build_versioned_ledger_from_paths(repo_root, profile_path, discovery_path, screening_acceptance_path, evidence_acceptance_path, views_acceptance_path) -> {ledger, planned_files}` pure.
- `build_versioned_completeness_from_paths(repo_root, profile_path, discovery_path, screening_acceptance_path, evidence_acceptance_path, views_acceptance_path, ledger_path, request_path, old_completeness_path) -> {completeness, planned_files}`
  Profile-initial UNION Discovery-named union; dimension/description from OLD
  valid completeness where Profile lacks them; no invented defaults.
- `prove_revision_from_paths(repo_root, revision_manifest_path, decision_path, before_copy_path) -> {proof, planned_files}`
  proposed-bytes only; no State recursion; binds M+D+before COPY.
- `check_supersession_record_from_paths(repo_root, checkpoint_path, report_path, before_copy_path) -> list[str]` detached (empty = pass).
- `require_same_triplet(state, structural) -> None` (same-record enforcement).
- `guard_path_for(source_root) -> Path` pure join (`orchestration/v2/acceptance-revision.guard.json`).
- `require_no_active_guard(source_root) -> None` lstat-once; ANY present/
  nonregular/unreadable -> `DM022_TRANSITION_ACTIVE`; no owner/skip params.
- `require_completion_consistent(source_root, checkpoint_ref) -> None`
  repo-root discovered by walking up to `config/survey-production-v2.json`;
  checkpoint FILE sha + completion receipt + seven_plan slot check; no State.
- `require_research_operation_ready(repo_root, state_path) -> None`
  ONE passive entry (entry+prepublish): guard ANY-present refuses; legacy ->
  guard-only; PREARCH triplet -> guard absent + completion exact verify
  (COPY-derived expected_after, seven_plan vs slot lstat with stale-present
  refusal; regenerated new bytes are a HIGH/postread concern, not a passive
  refusal here). No agent.validate, no HIGH, no guard claim.
- `lstat_slot(source_root, rel) -> {slot, present, lstat_kind, ...}` single
  lstat; symlink/nonregular/FIFO/dir never coerced to absent.

Trust boundary unchanged: LOW never writes, never calls agent/HIGH/current-
State validation, never treats guard ownership as permission. Agent validator
detached branch calls LOW proof, NEVER operational guard; no recursion.

### HIGH — `scripts/survey_prearchitecture_acceptance_v2.py`

Top imports ONLY: `core`, `schema_gate`, LOW. agent/evidence/screening/
completeness/discovery are function-local per entry. Sole mutator while bound
guard exists; exclusive `O_CREAT|O_EXCL`/short-write/`fsync`/checked-close/
`replace`/`dirfsync`/postread; never `core.write_json`/`copy2`/`is_file`.

- `prepare_revision(repo_root, state_path, request_path, revision_id) -> {revision_root, manifest_ref, retention, planned_files}`
  inert preparation: LIVE eligibility + guard-absent + HEAD/tree pins, S_before
  + 7-slot COPYs + inventory, LOW pure candidate (in-memory), exclusive R writes
  only (request/candidate/manifest/retention). No guard/State writes.
- `adopt_revision(repo_root, state_path, revision_path, decision_path) -> {status: ADOPTED, revision_id, checkpoint_ref, expected_after_state_sha256, seven_plan, guard_released}`
  full destructive order: reverify retention -> claim+revalidate guard ->
  LOW proof -> pre-adoption report (NO checkpoint/afterState/guard-hash) ->
  planned checkpoint bytes + FILE sha + expected State (in-memory) -> guard
  claim (nonce deterministic from planned bytes) -> write checkpoint as
  byte-identical planned copy (sha verified pre-switch) -> ONE known-byte
  State triplet switch (same new ref, guarded single-writer, inode-pinned) ->
  checked clearing of remaining exact old slots (pre-unlink re-read + COPY
  verify + dir fsync) -> postread/inventory -> completion (owned R, never
  canonical) -> release OWN guard (held-by-self verified, absent verified).
  Unknown LIVE -> INDETERMINATE, preserve records/bytes/guard, no automatic
  restoration/rollback; temp-E never adopted.
- `verify_live_eligibility(repo_root, cfg, state) -> list[str]`
  HIGH-ONLY strict LIVE: public `agent.validate_agent_state` on same bytes +
  S3 window (EVIDENCE_REVIEWED, passed Discovery/Screening/Evidence/
  Materiality/Completeness, no accepted Selection/Architecture/Draft/
  validation/preview/Freeze/Release, no Human approval, no Exception, null
  publication pointer). Returns errors (empty = eligible); never writes.
- `claim_guard(repo_root, state_path, rev, request_ref, retention_ref, planned_checkpoint_bytes, expected_after_sha, executor, work) -> {guard, guard_path}`
- `write_checkpoint_as_planned/clear_remaining_exact_slots/replace_state_triplet/write_cleanup_completion/release_guard(guard) -> dict`
  narrow step oracles; outside adopt context they raise explicit
  "requires HIGH adopt context" (no detached misuse).
- `resume_revision = resume_bound_attempt(repo_root, state_path, revision_path)`
  explicit bound-intent resume: S==B -> RESUME_ADOPT; S==E -> RESUME_CLEAR;
  else INDETERMINATE (preserve, no takeover/delete).
- `readback_revision(repo_root, state_path, revision_path=None) -> {research_acceptance, artifact_producer_boundary}`
  truthful same-State report + SEPARATE producer boundary (Matrix/Selection/
  Architecture regeneration reported distinctly, never merged).

R layout (deterministic, no timestamps in paths):
`R=<source_root>/research/v2/acceptance-revisions/<rev>/` with request,
candidate/{package,cards,views,evidence-acceptance,views-acceptance,ledger,
completeness}, retention/{state-before.json,slots/*,inventory.json},
revision-manifest.json, proof/{proposed-graph-proof.json,
supersession-report.json}, checkpoint.planned.json/.sha256,
checkpoint/record.json, completion/cleanup-completion.json. No R-prefix
wildcard reads; every resolver opens exact relpaths.

## 3. Actual checks performed (static only; NO integration execution)

Per execution discipline (no tests against files other workers edit; tests
run after root freezes the snapshot; no saved-runner invocation):

- AST parse OK: LOW, HIGH, new test, new helper (no imports executed).
- JSON parse OK: all five installed `schemas/dm022-*` (strict duplicate-key
  refusal via `schema_gate` at runtime, not just `json.load` here).
- AST import audit: LOW top imports contain no agent/HIGH/verify/transition/
  publication/renewal/guard-coordinator; HIGH top is core+schema+LOW only
  (agent/evidence/screening/completeness are function-local per entry).
- IO audit via AST: LOW has no `write_json`/`copy2`; former `is_file`/`is_dir`
  probes replaced with single-`os.lstat` (slot probe, repo-root discovery,
  card-dir probe via `iterdir` + per-file lstat). HIGH uses `_lstat_single`
  for absence (ENOENT legitimate; symlink/nonregular/unreadable refuse), safe
  `O_NOFOLLOW` reads, exclusive writes with short-write/fsync/checked-close/
  dir-fsync/replace/postread; no `core.write_json` equivalence.
- Registry check: installed report `roleSchemaRegistry` points at installed
  `schemas/dm022-revision-proof-v2.schema.json` (first two rows), other rows
  unchanged (`materiality-ledger`, `profile-completeness-result`,
  `candidate-matrix-v2`, `candidate-selection-v2`).
- Existing A-owned wrappers: AST inventory confirms zero missing S1.1 leaf
  cores; wrappers already delegate (final93 P1/P2R-era `_content`
  extraction). No edits made; old predicates preserved by non-interference.
- Tests written but NOT executed (discipline: static syntax/data checks only
  in this turn; no imports/bytecode; collection+execution deferred to root's
  frozen snapshot).

## 4. Precise map contradictions / TODO / blockers (HONEST, no broadening)

- NONE that blocks A-scope compilation: no new direct reader/closure/
  contract contradiction discovered in A-owned surface. No missing A reader;
  no omitted import closure in A files; no incompatible predicate introduced
  by A. If root/B/C1/C2 find a genuine omission, A returns to Astra rather
  than broadening (per coordination).
- Open interface-consistency items (NOT contradictions, owned elsewhere):
  C1 owns source-family pins/registry/config (`pipeline71->76`, replay
  70/union73, canon 36/41, schema SHAs at code); A validates via installed
  file SHAs at runtime and does not pin family labels. B owns the 17-site
  loader migration + 8 branches + 40-row guard/readiness wiring; A exposes
  the exact `load_typed_checkpoint_record` / `resolve_research_authority` /
  `_resolve_research_from_state_bytes` / `_load_typed_four_refs` /
  `check_supersession_record_from_paths` / `require_research_operation_ready`
  interfaces B needs. C2 owns downstream role refusal/readiness + P1/P2R
  explicit copy lists. Cross-owner reconciliation happens at root's frozen
  snapshot, not by A changing trust boundaries here.
- `require_completion_consistent(source_root, checkpoint_ref)` (R4 signature,
  no repo_root) is implemented via deterministic repo-root discovery (walk up
  to `config/survey-production-v2.json`). Documented here so B/C callers do
  not misread it as source_root-relative resolution. If root prefers a
  repo_root-explicit variant, A will add it WITHOUT changing the R4 signature.
- Mechanical `result_set_sha256`/`view_set_sha256` in proof `proposed` are
  carried as explicit content digests (R4); full acceptance-run-dir-name ==
  digest binding is enforced at HIGH materialization (prepare writes), not
  inside LOW pure proof. No directory-prefix exclusion; every mechanical
  projection is explicitly mappable via manifest/retention SHAs.
- Tests are new-only + existing A-owned (untouched). No old test-count/PASS
  transferred; no implementation acceptance claimed; no Production semantic
  claim. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN remain
  until independent implementation review + affected regressions + Human
  adoption decide otherwise.

## 5. Files for root freeze / next steps

Root binds one immutable complete integration snapshot, then executes
meaningful both-route positive/negative/later-lifecycle witnesses + affected
regressions (per ROOT S5.2 + decision S10): Weekly+Thematic genuine-type
synthetic fixtures; independent supplied research decisions; complete
four-artifact acceptance; affected/unaffected comparison + full obligations;
7-slot retain/clear + audit no-overwrite + regen; repeat correction;
wrong-role publication refusal; forward Architecture/Draft/publication +
history separation; G71->G76 unchanged-upstream compat control; G76 upstream
correction -> initial publication -> editorial/renewal; old/new/unknown
State + guard/completion loss + stale Raw/HEAD + ownership/close/replace
faults + late-seam explicit resume; synthetic reviews stay nongenuine.
After freeze, run at minimum:
`python -m pytest tests/test_dm022_prearchitecture_acceptance_v2.py -v`
plus affected `test_run_evidence_v2_interactive`,
`test_prepare_evidence_run`, `test_prepare_screening_run`,
`test_accept_evidence_results`, `test_accept_screening_results` (existing
A-owned; A did not modify them).

Author: Owner A. Scope complete; no implementation acceptance claimed.
