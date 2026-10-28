# DM022 pre-Architecture — integrated pre-code readiness R3 (AUTHOR, PRE-CODE ONLY)

2026-10-27 AUTHOR integration worker. PRE-CODE ONLY. Human `ab84b4f` assumed.
No source/runtime/import/tests/build/fixture/restore/network/Git writes.
Actual93 proof-copy READONLY. No candidate/reconstruct Commit/Push.
Preserves ALL R1/R2 (`authority-consumer-map.md`, `inventory.json`,
`schemas-generation-dag.md/json`, `guard-resume-oracles.md/json`,
R2 `*-r2.md/json`) and `independent-readiness-review.md` (NOT_READY) unchanged.
This file + `integrated-readiness-r3.json` + `schema-proposals/*.schema.json`
are the ONLY writes of this unit. No installed runtime. No MAP COMPLETE/PASS claim.

Binds: decision `outputs/rephase-1-dm022-prearchitecture-contract-decision.md`
incl. §11, SHA256 `a345bb9524b4dfc5b5f32600d0d708687e2b6131d91a43965c97b6418388f223`/31351B;
`notes/rephase-1-dm022-prearchitecture-contract/astra-review-resolution.md` incl. §5;
BOTH independent design reviews WITH FINAL-BINDING addenda (selection only,
B2/B4 pre-code OPEN at entry). Source: proof-copy
`.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`
= actual `409b292`/tree `8ce36998` +93/742. All `file:line` below are proof-copy
unless stated `workspace:`. Method: `Read` + `Grep` + `ast` parse as DATA only;
ordinary `json` parse/`ast`/hashing as data readonly source. No `scripts.*` imports executed.

ROOT task choices 1–11 are binding and incorporated verbatim below. Where R2
said “5+1 standalone” or “other owner will close”, this R3 replaces it: FIVE
standalone new schemas only (ROOT 3), per-caller exact signatures (no deferral),
full closure memberships (no count-only), literal branch/schema text (no OPEN file edits).

## 0. ROOT 1–11 incorporation (no handwave)

1. Two functional modules: LOW `scripts/survey_research_authority_v2.py`,
   HIGH `scripts/survey_prearchitecture_acceptance_v2.py`. LOW read-only path
   entries + pure content builders, no agent/currentState validation, no HIGH.
   Family imports function-local as needed per actual AST (Evidence TOP→Screening
   TOP→Core, agent runtime-local; §1). Normal 4-ref resolver is path-based facade;
   agent caller validates separately; inside agent State validator private LOW
   structural from its already-parsed State, no backcall.
2. STANDALONE NEW strict checkpoint schema selected by exact-kind loader
   `LOW.load_typed_checkpoint_record` (shared in LOW), old
   `schemas/stage-checkpoint-v2.schema.json` UNCHANGED. Blind if-kind on old
   schema's required `from/to` is not valid (§2). All 17 direct schema sites + 8
   validator branches enumerated with exact rewiring/refusal; normal
   `agent.advance_with_checkpoint` cannot install new kind via forward stage;
   new HIGH adopt only (§2, §11). New raw record: `operation`
   EVIDENCE/EVIDENCE, `producer_boundary` CANDIDATES/EVIDENCE, 3 checkpoint
   roles + 4 refs exact; State 3 refs SAME record atomic file; lifecycle/history/
   gates unchanged; late readback allowed across stages without entry window.
3. FIVE standalone new schemas: request, candidate-manifest, proof,
   supersession-checkpoint, report (filenames `dm022-*` consistent existing B map;
   datafile paths under `R/`). Decision shape embedded `request.$defs`,
   retention/immutable-guard/cleanup-completion embedded `report.$defs` with fixed
   internal role→schema-pointer registry; no generic SizedRef-only validate or
   untyped objects. Full literal JSON docs under `schema-proposals/` with fixed
   required/conditional/allRefs/digests/enum. No `records.items: object`/ellipsis.
   Request interactive card/view record spec mirrors actual
   `run_evidence_v2_interactive._validate_record:119-214`; nested actual schema
   defs explicit or fixed `$ref` closed registry. Supplied decision is
   actual before/after/allowlist/raw/assessment checked data, not new role/genuine
   PASS generator. FILE refs 2 keys, Sized 3, Named `{name,path,sha}`; self-digest
   named field one omitted only; repeated metadata equality explicit (§3).
4. Immutable before-State + 7-slot COPY and retention manifest captured in prepare
   as immutable INPUT to proposed generation; `request.before.state_path` stays
   canonical LIVE source, not COPY. HIGH binds CURRENT before bytes; LOW detached
   uses COPY via retention mapping. Canonical path never rewritten. Early immutable
   capture is preparation; later adopt REVERIFIES unchanged retention (does not
   rewrite it). No old-authority mutation before guard (§4).
5. Prepare writes complete candidate manifest + outputs before external decision.
   Then adopt validates provided decision and creates proof + pre-adoption report
   (NO checkpoint ref / no afterState hash / no guard hash). Checkpoint references
   completed request/manifest/proof/report/decision/retention; no future
   completion/ref cycle. HIGH computes EXACT checkpoint payload bytes
   deterministically + FILE sha + expectedState (bytes COPY with 3 refs) INMEMORY
   before immutable guard claim; guard binds nonce/request/planned checkpointRef/
   before+expectedAfter/executor+time/current workref; checkpoint NEVER backrefs
   guard. Planned cp bytes may be saved as datafile iff explicit path/digest, not
   authority. Write actual checkpoint after guard. Resume reconstructs exact bytes
   or loads planned bytes, must FILEsha match intent, not infer future SHAs (§5).
6. Guard fixed canonical `<source_root>/orchestration/v2/acceptance-revision.guard.json`;
   NORMAL writer/Gate ANY presence refuses, no self-owned/skip. HIGH bound
   adopt/resume only operate under own intent; readonly State/history never
   authorizes writes. Immutable guard phase derived State+slots/record, no mutable
   phase hash. Exact reopen identity across restart, single writer, no creator-auth
   claim. Completion `R/completion/cleanup-completion.json` after 7 absent verified
   BEFORE guard release; checkpoint never backref. Active typed checkpoint normal
   operational readiness requires valid completion bound checkpoint + COPY-derived
   expectedAfter AND guard absent. Completion expectedAfter does not equal later
   LIVE State once forward advanced. State NEW + guard lost + no Completion must
   block normal writers; resume exact bound intent (no blind takeover), explicit
   algorithm; unknown live never rewritten. LIVE canonical path only determines
   B/E/neither; temp E is not adopted. lstat/safeFD regular files/ancestors/
   hardlink/inodes, exclusive copies/writes/State temp fsync checked close/
   known-byte+inode replace/dirfsync; no `core.write_json` equivalence (§6).
7. All guard-check sites exact signature + Profile/sourceRoot/state source in each
   caller including public no-State CLIs/pure writer wrappers. A30 vs JSON29
   mismatch fixed, no bundled name-list row as closure. Ordinary stage & Gate
   guard checks entry + before publish, audit all-7 no-overwrite. Existing
   canonical upstream originals never overwritten even after adoption (§7).
8. HEAD/tree actual code commit before authority, exact expected HEAD/tree per
   invocation, artifact-only descendant allowed ONLY finite declared file diff-set
   derived request/manifest/retention/review/output artifacts (no R-prefix
   wildcard), require control-roots/code/schema/contract unchanged and all pins
   and readmode/status including untracked selective exact paths; root inherited
   55 gitlinks are workspace carryover NOT production runtime exception.
   Before-record new work HEAD changes plan hash update: must recompute entire
   bound intent and require decision binding consistent; no field defaults (§8).
9. DEPENDENCY: `P3S/Weekly/LF membership UNCHANGED because code branches only`
   REJECTED. NEW modules/schemas invoked MUST be in pinned closures. Enumerate
   full proposed lists actual callgraph; with 2+5 additions likely 63→70 per
   route/union 73, 29→36, 34→41, pipeline 71→76 BUT derive full set and necessary
   file-pin ONLY HIGH, not just add counts. Extra new module/schema if genuine
   need → return ROOT, not silent budget. Normal pub retention/historian must
   recognize PREARCH checkpoint schema/digest and full E graph, current-source
   Dependency Tool epoch maps no unsupported old-format ignorance (§9).
10. DM016 exact supported types per current tables, no canonical-type aliases
    merely pass. DM017 full provided 7-field obligation rows for union existing
    Profile+namedDiscovery, derive ID/DID/task relations and unchanged
    dimension/description from OLD valid completeness where Profile missing, no
    invent defaults. Mechanical card/task/view hash propagation actual schema only,
    no `ledger.self_digest` invented, compare unaffected semantic full projection
    all root keys not implicitly ignored, affected field-set limits precise.
    Include Profile witnesses and negative cases (§10).
11. Point-to-point names for all raw checkpoint/report/active-four-ref/guard/mode/
    digest loaders and after-State stages through publication/R1/editorial/renewal;
    exact public oracles and failure matrix (no readiness-bool tokens / no current
    State calls LOW) internally agree. Source citations exact current files. Build
    schemas proposals literal, no tests/project imports; ordinary json parse/AST/
    hashing as data okay readonly source. No independent PASS/MAP-COMPLETE if
    mandatory gaps remain; list residual and stop internal (§11–§13).

## 1. Modules / import DAG (ROOT 1)

- LOW `scripts/survey_research_authority_v2.py` (NEW, detached): public
  path-reloading entries take `repo_root + PATHS only` (`request_path`,
  `before_copy_path`, `previous_checkpoint_path`, `manifest_path`,
  `decision_path`, `checkpoint_path`, `state_path` for the single State-path
  entry). Never accepts caller State dict / ledger/completeness/proof dicts.
  Top-level imports ONLY `core` (shape-only: `repo_local_path, sha256_file,
  sha256_object, sha256_bytes, json_bytes, load_json, parse_instant, iso_utc` —
  NEVER `verify_state_basis, transition_state, repository_commit_sha`),
  `schema_gate`, stdlib `pathlib/json`. Every
  `evidence/screening/completeness/discovery/agent` access is function-local
  `from scripts import survey_evidence_v2 as evidence` (same for
  screening/completeness/discovery/agent) then calls ONLY §1.1 pure cores.
  LOW never imports `survey_agent_control_v2`, `survey_agent_tool_v2`,
  `survey_production_v2.verify_state_basis`, `survey_human_gate_v2`, operator/
  bridge, renewal/editorial/publication_set, guard coordinator. LOW header MUST
  enumerate exact imported SYMBOLS (not modules); any added import reaching
  State breaks leaf and is a precise OPEN blocker.
  Actual AST (proof-copy): `survey_evidence_v2` top imports `core, schema_gate,
  screening`; `survey_screening_v2` top imports `core` ONLY; function-local
  `screening:465 → agent`, `:480 → agent_tool` (`current_stage_basis_override`);
  `survey_completeness_v2` top `evidence, core, screening`; `survey_discovery_v2`
  top `core, schema_gate, x_intake`; `survey_agent_control_v2` top `drafting,
  core, publication, pubset, quality, reader_publication, surface_gate,
  review_attention, schema_gate` (NOT evidence/screening/agent_tool at top);
  `survey_agent_tool_v2` top `agent_control, evidence, core, screening`;
  `survey_production_v2` top `weekly_pipeline, pubset`;
  `survey_publication_set_v2` top `core, schema_gate`. True chain is
  `Evidence(TOP)→Screening(TOP)→Core` with agent imports lazy at runtime; whole-
  module cycle claims are false. R2 §10 per-function leaf holds; LOW may import
  ONLY leaf symbols (§1.1).
- HIGH `scripts/survey_prearchitecture_acceptance_v2.py` (NEW, sole mutator
  while bound guard exists): top-level ONLY `core, schema_gate, LOW`
  (`from scripts import survey_research_authority_v2 as low`);
  `agent/evidence/screening/completeness/discovery` imports function-local
  inside each entry (`prepare_revision`, `adopt_revision`, `resume_revision`,
  `readback_revision`). No permanent DM-issue runner name. CLI (if any) is thin
  `argparse` wrapper over these four entries; no new caller flags/verified dicts.
- Owner-A (existing, no new file) `scripts/survey_agent_control_v2.py` gains
  new-kind branch INSIDE; calls LOW pure validators function-locally for
  detached/history proof. Import direction: `LOW ← Owner-A ← HIGH` +
  `LOW ← HIGH` direct. FORBIDDEN: `LOW→agent`, `LOW→HIGH`, `agent→HIGH` (top),
  `LOW→guard coordinator` (LOW never reads guard; HIGH checks guard).

### 1.1 LOW leaf cores (exact names, no invention)

From `survey_evidence_v2.py`: `_check_evidence_package_fields_content:719`,
`_check_evidence_package_files_content:731`, `_check_evidence_tasks_content:769`,
`_supplement_entries_for_package:379` (State-free branch `:260-271`),
`task_authority_sources:413`, `_screening_acceptance_digest:482`,
`_evidence_result_set_digest:1152`, `_view_set_digest:1494`,
`_check_evidence_acceptance_results_content:1216`,
`_check_views_acceptance_rows_content:1286`, `_check_ledger_rows_content:1658`,
`_check_completeness_result_content:1804`, `_validate_evidence_package_basis_content:839`,
`_validate_evidence_acceptance_content:1255`,
`_validate_edition_views_acceptance_content:1322`,
`_validate_materiality_ledger_content:1725`, `_validate_completeness_content:1915`,
`validate_evidence_card:965`, `validate_edition_view:1437`.
From `survey_completeness_v2.py`: `_validate_obligation_shape:50`,
`_thematic_closure_errors:81`, `_check_profile_completeness_extra_content:145`,
`_validate_profile_completeness_content:241`.
From `survey_screening_v2.py`: `_resolve_effective_discovery_basis_content`,
`_validate_screening_acceptance_content`, `read_jsonl/validate_discovery_set`.
State-bound wrappers (`validate_evidence_package_basis:898`,
`validate_screening_acceptance:490`, `validate_evidence_acceptance:1412`,
`validate_edition_views_acceptance:1555`, `validate_materiality_ledger:1771`,
`validate_profile_completeness:265`, `prepare_evidence_package:539`,
`build_materiality_ledger:1579`, `accept_evidence_results:1159`,
`accept_edition_views:1498`, `run_evidence_v2_interactive.run:586`,
`write_materiality_ledger:1797`) keep exact old behavior for normal paths
(wrapper-delegation in implementation scope: refactor each to call §1.1 pure core
first, then State-bound suffix; no predicate weakened). New DM022 code calls ONLY
§1.1 cores + new HIGH exclusive writers below.

### 1.2 Exact signatures (path-reloading, no caller dicts)

```python
# LOW — scripts/survey_research_authority_v2.py
def load_typed_checkpoint_record(repo_root: Path, path: Path) -> dict
def resolve_research_authority(repo_root: Path, state_path: Path) -> dict
def _resolve_research_from_state_bytes(repo_root: Path, state: dict) -> dict
def _load_typed_four_refs(repo_root: Path, structural: dict) -> dict
def load_revision_request(repo_root: Path, request_path: Path) -> dict
def derive_before_context(repo_root: Path, request_path: Path, before_copy_path: Path, previous_checkpoint_path: Path) -> dict
def build_revision_package_from_paths(repo_root: Path, request_path: Path, before_copy_path: Path, output_dir: Path) -> Path
def build_revision_cards_views_from_paths(repo_root: Path, package_path: Path, request_path: Path, results_dir: Path, views_dir: Path) -> tuple[Path, Path]
def accept_revision_evidence_views_from_paths(repo_root: Path, package_path: Path, results_dir: Path, views_dir: Path, profile_path: Path, evidence_accepted_root: Path, views_accepted_root: Path) -> tuple[Path, Path]
def build_versioned_ledger_from_paths(repo_root: Path, profile_path: Path, discovery_path: Path, screening_acceptance_path: Path, evidence_acceptance_path: Path, views_acceptance_path: Path) -> dict
def build_versioned_completeness_from_paths(repo_root: Path, profile_path: Path, discovery_path: Path, screening_acceptance_path: Path, evidence_acceptance_path: Path, views_acceptance_path: Path, ledger_path: Path, request_path: Path, old_completeness_path: Path) -> dict
def prove_revision_from_paths(repo_root: Path, revision_manifest_path: Path, decision_path: Path, before_copy_path: Path) -> Path
def check_supersession_record_from_paths(repo_root: Path, checkpoint_path: Path, report_path: Path, before_copy_path: Path) -> list[str]
def is_prearchitecture_record(record: dict) -> bool
def is_legacy_candidates_record(record: dict) -> bool
def require_same_triplet(state: dict, structural: dict) -> None
def guard_path_for(source_root: Path) -> Path
def require_no_active_guard(source_root: Path) -> None
def lstat_slot(source_root: Path, rel: str) -> dict
```

```python
# HIGH — scripts/survey_prearchitecture_acceptance_v2.py
def prepare_revision(repo_root: Path, state_path: Path, request_path: Path, revision_id: str) -> Path
def adopt_revision(repo_root: Path, state_path: Path, revision_path: Path, decision_path: Path) -> dict
def resume_revision(repo_root: Path, state_path: Path, revision_path: Path) -> dict
def readback_revision(repo_root: Path, state_path: Path, revision_path: Path | None = None) -> dict
def verify_live_eligibility(repo_root: Path, cfg: dict, state: dict) -> list[str]
def claim_guard(repo_root: Path, state_path: Path, rev: str, request_ref: dict, retention_ref: dict, planned_checkpoint_bytes: bytes, expected_after_sha: str, executor: dict, work: dict) -> dict
def write_checkpoint_as_planned(guard: dict) -> dict
def replace_state_triplet(guard: dict) -> dict
def clear_remaining_exact_slots(guard: dict) -> dict
def write_cleanup_completion(guard: dict) -> dict
def release_guard(guard: dict) -> dict
def resume_bound_attempt(repo_root: Path, state_path: Path, revision_path: Path) -> dict
```

State-source rule: helpers WITH `state_path: Path` use that canonical file as the
ONLY State source (strict duplicate-key parse; never accept caller State dict
alongside). Helpers WITH `state: dict` (facade: handlers/validators/agent) FIRST
call public `agent.validate_agent_state(repo_root,cfg,state)` in the facade, THEN
call private `_resolve_research_from_state_bytes` (structural, no second
validation). The agent validator LOW branch itself MUST NOT call
`agent.validate_agent_state` again (no recursion). Helpers WITHOUT State (pure
writers/validators) take explicit `Path` args; their State source is the
profile-aware ENTRY that resolved R4 and checked guard absence. No readiness-bool
tokens; oracles return descriptive `{triplet_match, lineage_match, guard_state,
slots_present/absent}` recomputed every check, never bearer permission.

## 2. Checkpoint loader (ROOT 2, F8)

Old `schemas/stage-checkpoint-v2.schema.json` UNCHANGED (byte-identical; required
`from_state/to_state` + per-`from_state` artifact branches + `CORE_STAGE_CONTRACT`
review row retained). New record uses `operation{EVIDENCE_REVIEWED→EVIDENCE_REVIEWED}`
+ `producer_boundary{CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED}` + `kind/reason/
checkpoints/artifacts/...` (literal in
`schema-proposals/dm022-supersession-checkpoint-v2.schema.json`), not top-level
`from_state/to_state`. Blindly adding `if kind==new` to the old file fails:
without relaxing `required from/to`, the new record is schema-invalid; relaxing
weakens all old authority; forging `from/to=CANDIDATES→EVIDENCE` contradicts
truthful same-State operation (decision §5 forbids forged execution report);
asserting `EVIDENCE→EVIDENCE` matches no `stage_plan` producer
(`_producer_for_checkpoint:348` returns NONE for `EVIDENCE→EVIDENCE`,
`stage_plan:276-315` has no such entry) and fails
`_validate_core_stage_report:365` (`:403-408` requires
`report.from==lifecycle && report.to==next_state`). Standalone + shared dispatch
avoids `oneOf` duplication and old-file weakening.

Shared loader (LOW, pure, no State): `load_typed_checkpoint_record(repo_root,
path) → {family: LEGACY|PREARCH, record}` — strict duplicate-key parse → `kind`
absent ⇒ validate old schema; `kind==PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`
⇒ validate new schema; else refuse unknown. No caller flags, no verified dicts,
no `.get(kind,legacy)` fallback, no raw `record["kind"]` mutation.

All 17 direct schema sites MUST migrate from direct `CHECKPOINT_SCHEMA` loads to
the shared loader (each needs code change before code gate closes; §11 table
gives per-caller exact new call):

- `survey_agent_control_v2.py:42` const, `:489` record load, `:819` second load,
  `:1011` pending validation, `:1532` revalidation prior, `:1758`
  validate_instance, `:1774` load_and_validate, `:1971` basis checkpoint,
  `:2397` revalidation prior Stage Checkpoint.
- `survey_publication_set_v2.py:56` const, `:1213` anchor prior, `:1627`
  before-digest prior, `:1981` selection prior (single-resolver change covers all
  `_l_stage_path` adapters `production._l_stage:47`, `stage_validation._l_stage:99`,
  `human_gate.resolve_gate_path:255`, `orchestrator.resolve_configured:167` for
  stage-template paths ONLY; research four-ref per-caller R4-or-refuse is separate,
  F4 split, §11).
- `survey_editorial_correction_proposal_v2.py:557` via `agent.CHECKPOINT_SCHEMA`.
- `survey_release_checkpoint_v2.py:121` validate_instance.
- `survey_stage_validation_v2.py:288` prior Stage Checkpoint load.
- `survey_weekly_mechanical_refresh_v2.py:931` refresh validation checkpoint.

Validator branches (8, same gate): `:348` must NOT be called for PREARCH
(branch before lookup; producer NONE); `:365` bypass `CORE_STAGE_CONTRACT`
match ONLY inside new-kind branch (replace with `DM022_SUPERSESSION_PROOF` +
SELF + artifact re-hash); `:481` ADD PREARCH branch
(kind/reason/operation/producer_boundary/checkpoints/artifacts/lineage/SELF +
new proof review; validation-projection `868-891` untouched; unknown kind refuse);
`:761` ADD PREARCH dispatch (`EVIDENCE→EVIDENCE` + `producer_boundary` + 4-name
set + SELF/proof binding); `:902` KEEP legacy + ADD `R4=LOW.resolve_research_authority`;
`:1608` exempt canonical path ONLY inside new branch; `:1703`
`build_stage_checkpoint` UNTOUCHED (new PREARCH builder separate, F5);
`:1768` `advance_with_checkpoint` REFUSE PREARCH same-State (producer NONE;
adoption is HIGH single-file switch only, F5).

Normal agent strict public State validator `validate_agent_state:597`
(`:602-748` + `core.validate_state_semantics:760-780` fixed forward history)
retains FULL existing predicates with precise new-kind branch; never substituted
by current-pinned `production.verify_state_basis:959`.

## 3. Five standalone schemas (ROOT 3, F1/F2/F8)

`schema-proposals/` contains EXACTLY five standalone files (ROOT selects five;
R2 5+1 optional standalone WITHDRAWN; completion/guard/retention shapes are
embedded `report.$defs`, decision shape embedded `request.$defs`; no sixth file):

- `dm022-revision-request-v2.schema.json` — immutable prepare input.
- `dm022-revision-manifest-v2.schema.json` — immutable prepare inventory
  (FILE SHA is identity, no embedded self-digest).
- `dm022-revision-proof-v2.schema.json` — deterministic proof, proposed bytes only.
- `dm022-preadoption-report-v2.schema.json` — pre-adoption, NO checkpoint/
  afterState/guard-hash refs; embeds `retentionManifest`, `guardIntentCoord`,
  `completionReceipt`, `roleSchemaRegistry` as `$defs` (coordination views, not
  competing schema files).
- `dm022-supersession-checkpoint-v2.schema.json` — typed record (standalone new;
  old file unchanged).

Every file: `{"$schema":"https://json-schema.org/draft/2020-12/schema",
"$id":"https://example.invalid/schemas/dm022-*.schema.json",
"type":"object","additionalProperties":false,"required":[...],
"properties":{...},"$defs":{...}}` with `$defs` repeated literally per file
(`sha256 ^[0-9a-f]{64}$`, `gitsha ^[0-9a-f]{40}$`, `safePath`
`^(?![/\\\\])(?!.*\\.\\.)[^\\\\]+$` = `core.repo_local_path` semantics,
`ArtifactRef={path,sha256}`, `SizedRef={path,sha256,byte_count}`,
`NamedRef={name,path,sha256}`), `additionalProperties:false` throughout,
`if/then/contains` for `checkpoints==[evidence,materiality,completeness]` and
`artifacts` 4 `NamedRef` with `contains` each name, `reviews` sole
`DM022_SUPERSESSION_PROOF`, `contract` literal 8-field, `implementation` literal
2-field, digests `*_sha256==sha256_object(body-minus-self)` (FILE `sha256_file`
distinct), `enum` fixed, no `object`/ellipsis, no `...`.

F1 repair: `request.records` is NOT `{"type":"array","items":{"type":"object"}}`.
`request.$defs` defines `entity`, `claim`, `verificationItem`,
`interactiveRecord` (COMMON + all optional profile fields + REJECTED→NON_MATERIAL
/ NEEDS_MORE→HOLD `allOf`), `weeklyRecord` (COMMON + `window_relation` enum
`WEEKLY_WINDOW_RELATIONS` + `carry_over` bool, required), `thematicRecord`
(COMMON + `lineage_role` enum `LINEAGE_ROLES` + `branch_ids`/`transition_ids`
unique string arrays + `inheritance_note`/`historical_attribution_caveat`
string/null, required). Top-level `allOf` selects `weeklyRecord` iff
`research_profile==WEEKLY`, `thematicRecord` iff `THEMATIC`, mirroring actual
`run_evidence_v2_interactive._validate_record:119-214`
(`COMMON_RECORD_FIELDS:66-70`, `THEMATIC_RECORD_FIELDS:71-74`,
`WEEKLY_RECORD_FIELDS:75`, `RETROSPECTIVE_RECORD_FIELDS:79` empty — RETROSPECTIVE
not admitted here; `ENTITY_TYPES:47-50`, `ARTIFACT_TYPES:51-55`,
`EVIDENCE_CLASSES:56-59`, `CARD_STATUS`, `VERIFY_STATUS`, `MATERIALITY`,
`WEEKLY_WINDOW_RELATIONS:65`, `LINEAGE_ROLES:63`). `source_bindings` optional
unique nonempty string array (iff multi-source; presence checked semantically,
not schema-mandated). Nested actual schema defs explicit; no unknown `$ref`.

F2 repair: all five files are literal JSON (not prose required-lists); each
`SizedRef` re-hashed on load, each `byte_count==stat().st_size`, each digest
recompute-excluding-self verified.

Refs: `ArtifactRef` 2 keys, `SizedRef` 3 keys, `NamedRef` 3 keys with
`name∈{evidence-acceptance,edition-views-acceptance,materiality-ledger,
profile-completeness}` (checkpoint) — no generic `kind` on refs, no bare
`{path,sha,byte_count,kind}`. Self-digest named field one omitted only:
`revision_proof_sha256`, `preadoption_report_sha256`,
`supersession_checkpoint_sha256` each `==sha256_object(all other top-level
fields, sort_keys, separators=(",",":"))`; request/manifest have NO self-digest
(FILE SHA is identity, avoids cycle). Repeated metadata equality explicit: every
duplicate SHA states equality in R3 §4–§5 predicates and is carried in both
sides (e.g. `ledger.basis.evidence_acceptance_sha256 == sha256_file(R
evidence-accepted.json) == proof.proposed.evidence_acceptance.sha256 ==
report.proposed_artifacts.ledger basis`; `mechanical_projections[]` lists each
`{field_path (actual schema path, e.g.
materiality-ledger.basis.evidence_acceptance_sha256), old_sha256|null,
new_sha256, reason}` — directory-prefix exclusion forbidden).

Decision (supplied, author-independent research/authority-consumption): shape
embedded `request.$defs.suppliedDecision` (closed registry, not a standalone
schema file). Required: `schema_version, issue_id, revision_id, manifest_ref
(SizedRef == M FILE SHA), before_state, before_checkpoint, affected_ids,
raw_refs[] (SizedRef, actual preserved bytes/provenance), allowlist
{allowed_ids nonempty unique subset non-DROP + basis string},
assessment {interpretation, event_semantics, provenance_check strings},
reviewer {provider, model, invocation, recorded_at}, recorded_at`. No
`status:PASS`, no `kind:AGENT_RESEARCH`, no writer-generated genuine PASS; authority
comes from file binding + LOW revalidation (`affected_ids ⊆ non-DROP`,
Raw re-hash + before/after SHA binding). Checkpoint `reviews[]` carries ONLY
`{check_id:DM022_SUPERSESSION_PROOF, kind:DETERMINISTIC, status:PASS,
executor, evidence, result:SizedRef(==proof)}` (local content-proof binding,
not approval); `decision` is separate `SizedRef` field.

Retention/guard/completion embedded `report.$defs` (fixed internal
role→schema-pointer registry; no generic SizedRef-only validate):
`roleSchemaRegistry` (6 fixed `name→const $id` entries for the 4 research
artifacts + matrix/selection), `retentionManifest` (7 rows, present/absent +
SHAs + bound flags), `guardIntentCoord` (`guard_path` const
`orchestration/v2/acceptance-revision.guard.json`, `issue_id`, `revision_id`,
`attempt_nonce ^[0-9a-f]{16,}$`, `planned_checkpoint_ref SizedRef`,
`before_state_sha256`, `expected_after_state_sha256`, `work{head,tree}` — NO
phase field, NO hash authority, coordination view only), `completionReceipt`
(`schema_version 1.0`, `checkpoint SizedRef`, `expected_after_state SizedRef`,
`seven_plan[7] {slot, disposition:cleared|absent_legitimate, captured_sha,
copy_sha}`, `postread{state_sha, triplet_match:true, artifacts_rehashed:true}`).
Actual data files `R/retention/inventory.json` and
`R/completion/cleanup-completion.json` validate against these embedded shapes;
no sixth standalone schema file is installed.

Digest/mode note: `guardIntentCoord` and `completionReceipt` carry NO digest
that the checkpoint or report hashes over (report has NO `guard hash`;
checkpoint has NO `guardRef`/`afterStateSHA`; proof has NO checkpoint ref).
SHA DAG is one-way `before→M→D→P→RPT→CP→State→POST-receipt` (§5).

## 4. Before-State + 7 slots + retention (ROOT 4)

`package.basis.state_path` is ALWAYS the canonical LIVE source path
(repo-relative, e.g. `<source_root>/production-state.json` as recorded by
`prepare_evidence_package:539-681` at `:644-652` via `_rel(repo_root,state_path)`),
`package.basis.state_sha256` = exact BEFORE bytes (`sha256_file(state_path)` at
pin time). Verified State-free by
`_validate_evidence_package_basis_content:839-895`
(`basis.state_path == canonical_state_path` at `:860-864`, file/contract drift
at `:867`, screening via State-free content at `:874-886`, no
`verify_state_basis`/`repository_commit_sha`). Retained COPY (e.g.
`R/retention/state-before.json`) is a SEPARATE manifest entry
`{source_rel: canonical LIVE path, copy_rel: R retention path, source_sha256,
copy_sha256, byte_count, st_dev/ino both sides}` with
`copy_sha256 == source_sha256 == basis.state_sha256` (re-hashed on capture +
resealed in adopt). Rebinding basis to the COPY path is refused. `request.before_state`
is `SizedRef` to the canonical LIVE source (not COPY); LOW detached uses COPY
via retention mapping (`derive_before_context` loads COPY + previous checkpoint +
4 artifacts, verifies `COPY bytes == request.before_state.sha256`).

Immutable before-State + 7-slot COPY and retention manifest are captured in
prepare as immutable INPUT to proposed generation (inert preparation: no canonical
writes, no State writes, no guard claim; present/absent inventory). Preparation
records exact present/absent + source refs for the seven Profile-`source_root`-
relative slots (decision §11.1): `candidate-matrix-v2.json`,
`candidate-selection-v2.json`, `architecture-v2.json`,
`architecture-review-summary-v2.json`, `architecture-review-attention-v2.json`,
`orchestration/v2/interactive/selection-architecture-input.json`,
`orchestration/v2/interactive/selection-architecture-audit.json` (audit
`:330-343` unguarded-today, successor 7-path preflight required). Old reviewed
targets are not rebound by copying equal bytes; partial failed-run outputs are
inventoried as partial, never fabricated into a complete reviewed result; caller
`input_path` (outside `source_root`, argv `--input`) vs generated `archive_path`
(inside `source_root`, `run:328-329`) provenance kept distinct.

Canonical path never rewritten. HIGH binds CURRENT before bytes at pin
(`lstat`+read+hash LIVE `production-state.json` + `validate_agent_state==[]` +
window + HEAD/tree/contract/live pins). LOW detached uses COPY via retention
mapping only. Early immutable capture is preparation; later adopt REVERIFIES
unchanged retention (present bytes still equal captured old bytes, still
unaccepted/unbound, guard not yet held) BEFORE claiming guard; it does not
rewrite retention. No old-authority mutation before guard. Existing content-
addressed old-package State-SHA evolution follows ONLY
`agent_tool._historical_state_basis_wrapper:53-118` (historical drift allowed
iff `sha256_file(package_path)==acceptance.package_sha256` + full same-source
binding); new package `state_sha` is the new before, never rewritten to the
other's path. Old canonical Ledger/Completeness stay byte-identical and become
inactive ONLY after State adoption; no canonical overwrite/rebind-by-hash.
Existing canonical upstream originals are never overwritten even after adoption.

## 5. Prepare / adopt split + determinism (ROOT 5)

```text
prepare phase (no decision input, no guard claim, no canonical/State mutation):
  pin current basis (S_before bytes + HEAD/tree/contract + live pins, HIGH-side)
  → capture immutable before snapshots within NEW owned R (S_before COPY + every
    present 7-slot COPY + present/absent inventory; inert preparation, old authority untouched)
  → generate truthful candidate under R via LOW PATHS-only builders (§1.2) bound to
    S_before + existing Discovery/Screening (same-State, no CANDIDATES_NORMALIZED pretense)
  → emit immutable revision manifest M (R/revision-manifest.json, literal §3; FILE SHA is identity)
external decision (binds already-existing immutable M outputs; no future ref):
  supplied independent bundle D (FILE SHAs == M + before + Raw SHAs + allowlist; immutable file,
  shape = request.$defs.suppliedDecision, validated at adopt)
adopt/finalize phase (validates D + seals + guards + records + switches + clears + verifies):
  seal/reverify final retention inventory (present bytes still equal captured old bytes,
  still unaccepted/unbound) → claim + revalidate G → complete deterministic proof P
  (LOW PATHS-only, refs M + D + before) → complete pre-adoption report RPT
  (refs M + P + D + before + all-4-artifacts + operation/boundary + tools/workref;
  NO checkpoint/afterState/guard refs) → complete typed checkpoint CP (refs completed
  RPT + P + D + before + retention plan; SELF-excluded digest + FILE SHA)
  → prevalidate S_expected (S_before with ONLY provenance.{evidence,materiality,
    completeness} → SAME new CP ref) → ONE known-byte State switch → checked
  clearing of remaining exact old slots → postread/inventory verification →
  release OWN G → normal regen
```

Destructive order unchanged from decision (`guard → record → State triplet
switch → checked clearing → postread → completion → release guard → regen`).
M vs P/RPT vs CP vs optional POST receipt are distinct types/stages; every SHA
edge points backward only (`M←D←P←RPT←CP←State←POST-receipt`). No self/future SHA.

HIGH computes EXACT checkpoint payload bytes deterministically
(`core.json_bytes`-equivalent sorted-keys canonical form) + FILE sha +
expectedState (bytes COPY with 3 refs: `S_expected = S_before` with ONLY
`checkpoint_provenance.{evidence,materiality,completeness}` replaced TOGETHER by
SAME new CP `{path,sha256}`) INMEMORY before immutable guard claim. Guard binds
`nonce/request/planned_checkpointRef/before+expectedAfter/executor+time/current
workref` (`guardIntentCoord` shape, §3; guard bytes FIXED after claim; no phase
field; checkpoint NEVER backrefs guard). Planned cp bytes may be saved as datafile
`R/checkpoint.planned.json` + `R/checkpoint.planned.sha256` iff explicit
path/digest recorded in guard `planned_checkpoint_ref`; saved bytes are NOT
authority (authority is guard-bound planned SHA + FILE sha after write). Write
actual checkpoint (`R/checkpoint/record.json` + canonical checkpoint location per
new schema branch) as byte-identical copy of planned bytes AFTER guard claim;
verify FILE sha `== planned_sha == guard.planned_checkpoint_ref.sha256` BEFORE
any State replace; mismatch → abort to INDETERMINATE, preserve guard+temp, no
State write. Resume reconstructs EXACT bytes deterministically from guard's
immutable refs (`request_ref` + `retention_ref` + `executor/time` + review/proof/
report bytes under `R/proof/` + `R/candidate/`) or loads planned bytes; must
FILEsha match intent (`recompute sha == guard.planned_checkpoint_ref.sha256`),
not infer future SHAs; if reconstruction is not bit-identical (e.g. proof bytes
missing, `recorded_at` drift via `now()` instead of guard `executor.recorded_at`)
→ fail-closed NEW attempt + manual resolution, preserve guard+retention.

## 6. Guard / completion / State dispositions / IO (ROOT 6)

Guard fixed canonical `<source_root>/orchestration/v2/acceptance-revision.guard.json`
where `<source_root>` = validated Profile `source_root` via
`core.repo_local_path(repo_root, profile["paths"]["source_root"], …)`
(`survey_production_v2:282`) + `agent._profile_and_source:307`. Collision
verified: zero hits for `acceptance-revision.guard` / `acceptance-revisions` in
final93 tree; guard distinct from `config:271`
`orchestration/v2/interactive/selection-architecture-input.json`,
`config:403-404` `orchestration/v2/attestations` / `orchestration/v2/checkpoints`,
`agent.canonical_checkpoint_path:1608`. R deterministic, no timestamps in paths:
`R=<source_root>/research/v2/acceptance-revisions/<rev>/` (`[a-z0-9][a-z0-9-]{0,63}`,
single segment, no `/`, no `.`, no uppercase, no traversal; two attempts MUST NOT
share an id) with 18 fixed children (request, prepare/early-copy (optional),
candidate/{package,tasks,results,evidence-acceptance,edition-views-acceptance,
ledger,completeness}, proof/{proposed-graph-proof,supersession-report},
retention/{state-before,slots/<7 basenames>,inventory}, checkpoint.planned.json/
.planned.sha256, checkpoint/record.json, completion/cleanup-completion.json).
No wildcard R-prefix reads: every resolver opens EXACT files by exact relpath,
never `R/**/*.json` or directory listing as authority.

FIXED NORMAL API (LOW): `require_no_active_guard(source_root: Path) -> None`.
Signature has NO `owner`, NO `allow_held_by_self`, NO `skip` param. Behavior:
guard `lstat` absent → pass; guard present well-formed/foreign/self/malformed/
nonregular/symlink/unreadable → raise `DM022_TRANSITION_ACTIVE`. Guard presence
NEVER grants permission — normal generator still needs its own preconditions.
ONLY HIGH adopt/resume operates while bound guard exists, and ONLY after verifying
`guard.nonce/rev/sha == retained intent` + `S` disposition per §11 failure table.
Readonly State/history diagnosis never checks guard as eligibility; mutation/
publication/presentation MUST NOT proceed while guard held. Strict read-only
`core.load_json:136` / `agent.validate_agent_state:597` / `core.validate_state_semantics:718`
MUST NOT call guard as eligibility.

Immutable guard phase DERIVED (`S==B vs S==E` + `record present?` + `slots
present/absent` + `completion present?`), never by rewriting guard hash:
`claimed (guard present, S==B, record unwritten?)` / `recorded (guard present,
record FILE sha==planned, S==B)` / `switched (guard present, S==E)` /
`clearing (guard present, S==E, some slots cleared)` / `completed (guard present,
completion receipt verified)` / `released (guard absent + completion verified)`.
No mutable `phase` field inside guard hash; no `SELF` cycle. Checkpoint contains
NO `guardRef`, NO `afterStateSHA`.

Exact reopen identity across restart (single writer, no creator-auth claim):
process FDs do NOT persist across restart; HIGH holds NO cross-restart lease.
Resume reopens guard by `lstat`+read+hash vs retained intent (`R/request.json` +
`R/retention/inventory.json` + `R/checkpoint.planned.sha256` + pin sets). Checks:
`guard bytes == retained guard copy?`, `nonce/rev/issue/planned_sha/before_sha/
expected_after_sha` match retained intent; `dev/ino` recorded for diagnostics
only (reboot may recycle inodes — identity is `nonce+hashes`, NOT inode
persistence). No stale lease, no foreign takeover, no creator-auth claim
(executor/time are audit fields, not permission).

Completion `R/completion/cleanup-completion.json` (owned R, NOT canonical, no State
provenance pointer, no lifecycle advance) written AFTER all seven planned slots
verified cleared/absent-legitimate + full postread (`S==E` + triplet same-record +
four live hashes + inventory match) and BEFORE guard release. Single HIGH writer,
exclusive-temp+fsync+postread primitive. Content (literal `report.$defs.completionReceipt`):
`{schema_version 1.0, issue_id, revision_id, attempt_nonce,
checkpoint:{path,sha256}, before_state_sha256, expected_after_state_sha256
(NEVER live-after; operation baseline derived from before-COPY + planned
checkpoint), retention_ref, seven_plan[7 × {slot, disposition:cleared|
absent_legitimate, captured_sha, copy_sha, observed_at_postread}],
postread:{state_sha, triplet_match:true, artifacts_rehashed:true}, recorded_at,
executor}` (+ `self_digest` excluded from checkpoint hash; checkpoint NEVER
references completion). Consumer predicate (no generic flag): normal writers with
active typed checkpoint (`checkpoint_kind==PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`)
MUST require BOTH (a) `require_no_active_guard(source_root)` passes (guard ABSENT)
AND (b) completion receipt exists + verifies (`checkpoint_ref.sha == active
checkpoint sha`, `expected_after_sha == receipt.expected_after`, `seven_plan`
matches current absent/legitimate dispositions for slots NOT yet regenerated).
Late State-forward is OK: `receipt.expected_after` is the OPERATION BASELINE, not
a demand that LIVE State still equal `E` (after forward `SELECTION_COMPLETE→…`,
LIVE differs; receipt still validates the adoption it attests). This supports
`ALREADY_ACTIVE` after forward regen: do NOT demand current seven slots still
absent after normal regen has recreated Matrix/Selection/Architecture (those are
NEW bytes under NEW authority, not old stale bytes).

State NEW + guard lost + no Completion MUST block normal writers (refuse seven-
slot writes until HIGH re-establishes completion or manual resolution; do NOT
silently proceed). Resume exact bound intent (no blind takeover), explicit
algorithm per §11 failure table (F8/F9/F10/F11/F13). Unknown live never rewritten:
R1 F4 (rewrite unknown LIVE to B/E) WITHDRAWN. If LIVE unknown at any step,
preserve LIVE + temp as-is, posture INDETERMINATE (F11), no second write
fabricating B/E. LIVE canonical path ONLY (`production-state.json` via
`lstat`+hash+validation) determines `B/E/neither`; temp E present does NOT mean
live adopted (ONLY canonical LIVE disposition counts). Never rewrite unknown
LIVE to B/E.

IO discipline (no `core.write_json` equivalence): NO `Path.is_file` / `exists()`
for absence (use `os.lstat` once per path per phase; `ENOENT`=absent legitimate;
`EACCES/EPERM/ELOOP`/symlink incl. dangling/FIFO/socket/device/dir/nonregular/
other `lstat` error = refuse + record `lstat_kind/errno`, never coerce to absent;
dangling symlink MUST NOT be followed; FIFO MUST NOT be opened). NO
`shutil.copy2` (no exclusive guarantee). COPY primitive (HIGH): open source
`O_RDONLY|O_NOFOLLOW`, `fstat` verify regular + `dev/ino/size/sha` match capture,
stream copy to `R/retention/slots/<basename>.tmp.<nonce>` with
`O_CREAT|O_EXCL|O_WRONLY 0600`, short-write loop (retry `write()` until all bytes
or error), `fsync(file)`, checked `close()` (close error = FAILURE, never
swallowed in logger), `fsync(dir)`, re-hash COPY + `lstat` COPY `dev/ino` (MUST
differ path identity from source; no inode-sharing claim beyond this pair), then
re-read source bytes+sha (MUST still equal capture). Rename tmp→final via atomic
`os.replace` + `fsync(dir)`. State replace = NEW exclusive temp sequence (§11
F-table): serialize `S_expected` in memory → `expected_after_sha`; `lstat`+read+
hash LIVE → classify `S==B/E/unknown`; if not `S==B` at adopt → do NOT write;
write temp sibling `production-state.json.tmp.<nonce>` with `O_CREAT|O_EXCL`,
short-write loop, `fsync(file)`, checked `close()`, verify temp bytes+sha ==
`S_expected`, `lstat` temp `dev/ino` (new inode, not LIVE inode); knownbyte+inode
compare: re-`lstat`+re-hash LIVE path, MUST still be `B` with SAME `dev/ino`,
else abort (no replace), preserve temp; `os.replace(temp,live)` +
`fsync(containing dir)` + immediate postread (`lstat`+read+hash LIVE == `E` +
`validate_agent_state==[]` + triplet same-record check). Any `write/fsync/close/
replace/dirfsync/read` error retained as `P/Q` with observed bytes/inode/hash.
Short-write TEMP is NOT LIVE: LIVE `B` preserved (temp sibling only). Postclear
slot absent CAN be legitimate (already-cleared or never-present with SAME dir
identity); `absent but dir dev/ino changed` OR `present with unexpected dev/ino
even if bytes/sha equal captured old` → refuse (new inode = new file, even on
equal bytes). COPY backup verified BEFORE unlink; unlink verifies pre-unlink
re-read `sha==captured_old_sha` + still unaccepted/unbound + guard held by HIGH
self. Guard-release errors: held-by-self verified → unlink guard + dir fsync +
verify absent → regen unblocked (completion already verified); absent (`ENOENT`)
→ record `guard_absent_at_release`, posture INDETERMINATE (lost-guard window:
normal writers MUST still require completion; do NOT silently proceed); foreign/
mismatched → refuse, no takeover/delete.

## 7. Guard-check sites (ROOT 7, F6/F7)

A30 vs JSON29 fixed: R2 `authority-consumer-map-r2.md` has 30 numbered rows
(1–30) with row 3 bundling `_validate_checkpoint_record:481` +
`_validate_core_stage_report:365` under one `line:481` entry and missing row 5
`resolve_effective_discovery_basis:353 / _content:809`; `inventory-r2.json` has
29 rows. This R3 unbundles to exact per-function rows (no bundled name-list row
as closure): 36 rows in `integrated-readiness-r3.json` (`rows[]` each with
`file`, `fn`, `line`, `state_source`, `guard_check`, `kind_branch`, `oracle`).
Bundling noted only as history; machine inventory matches prose exactly.

Every row CLOSED with exact signature + Profile/sourceRoot/state source +
guard check + oracle (pattern alone is not closure). `G` =
`LOW.require_no_active_guard(source_root: Path)` (absence required, no
owner/skip). `C` = `require_completion_consistent(source_root,
checkpoint_ref)` (active new-kind writers after release). `K` = kind dispatch
(§2). `R4` = `LOW.resolve_research_authority(repo_root, state_path)` (public,
path-reloading) or private `_resolve_research_from_state_bytes(repo_root, state)`
after facade `agent.validate_agent_state` (State-dict callers). Status CLOSED
means exact call + guard location + oracle given; no row left as “caller G”
without Profile path derivation.

No-State-arg caller derivation per caller (F7): resolve `repo_root` → load
`cfg` → resolve Profile (`state.profile.path` if State arg exists; else
canonical `production-profile.json` location via `repo_local_path` + `sha` vs
State or vs `contract_identity`) → `source_root` → `guard_path_for(source_root)`
→ `require_no_active_guard`. If Profile cannot be validated or `source_root`
cannot be bound (e.g. handoff dict without `profile.path`, artifact-map without
State), REFUSE before any canonical write. Exact per-caller derivation in
`integrated-readiness-r3.json` `guard_derivation` per row; e.g.:

- `survey_handlers_v2._evidence_basis:204` (State-dict facade): facade validates
  `agent.validate_agent_state(repo_root,cfg,state)==[]` → `source_root =
  _profile_and_source(repo_root,cfg,state).source_root` → `G(source_root)` at
  entry + before each handoff bind; handoff rows bind to `R4` refs when State
  carries PREARCH (`{path,sha256}` + live re-hash, `_same_authority` kept);
  refuse superseded mode if R4 absent. Oracle: handoff with old SHAs refuses,
  zero handoff bytes written.
- `survey_stage_validation_v2._evidence_basis:402` + `_selection_basis:468` +
  `_validate_stage_semantics:501` + `validate_stage:778` (`artifacts` map +
  `REQUIRED_CURRENT:150-177`): same facade derivation; `REQUIRED_CURRENT` names
  unchanged, VALUES become R4 refs post-adoption; `REQUIRED_CURRENT` for
  `CANDIDATES_NORMALIZED` = 4 R refs; pre-adoption proof uses LOW `_content`
  (never wrapper). Pure historical validation of retained record MUST NOT require
  guard-absent (detached proof rule); MUTATING validation path requires `G`
  at entry + before publish.
- Pure writers (`survey_evidence_v2.build_materiality_ledger:1579`,
  `write_materiality_ledger(path,ledger):1797` arbitrary path,
  `accept_evidence_results/accept_edition_views` arbitrary `accepted_root`,
  `survey_architecture_v2_base.*`, `survey_drafting_v2_base.*`,
  `survey_completeness_v2` builders/validators with explicit paths): STAY pure
  (no `state_path`/`profile` args, no guard read inside); the CHECK lives in
  their profile-aware ENTRY (`run_selection_architecture:158`,
  `run_drafting_synthesis.main:150`, `run_evidence.run:586`,
  `run_semantic_publication.main:118`, orchestrator/bridge/Gate). No-State-arg
  pure function never gains a State param; caller supplies R4 paths + `G`.
- Public no-State CLIs / wrappers without `state_path` (e.g.
  `survey_reader_surface_gate_v2:1152/1414/1972` optional-`state_path`,
  `survey_execution_record_v2._load_state:82`, `survey_reader_publication_v2`
  manuscript binding, Weekly/Longform receipt validators): MUST require State
  post-adoption when resolving research authority (no no-State canonical read);
  receipt replay uses retained lineage (no before-equality). Derivation:
  `repo_root → cfg → Profile (canonical profile path + sha vs contract_identity)
  → source_root → G`; if Profile unvalidatable → refuse before any canonical
  output. Names-only listing is NOT closure.

Ordinary stage & Gate guard checks entry + before publish (each `core.write_json/
copy2/unlink/transition` and each of the 7 writes): `run_selection_architecture:158`
(entry after `source_root:172`, before `ledger_path:176` use: `G(source_root)`;
before EACH of 7 writes `209/252/314/324/325/329/331`: re-`G` + 7-path preflight
(6 at `199-201` PLUS audit `330-343`); `agent.advance_with_checkpoint:1768`
(after state/cfg load, before canonical `1771`: `G(source_root via
_profile_and_source:307)` + explicit refuse PREARCH kind);
`survey_human_gate_v2` Gate presentation (before loading Gate inputs
`config:227-232` dossier: `G` + `C` if new kind active; read-only
`_current_pending_gate:440` / `invalidate:1179` diagnosis paths MUST NOT call
`G`); `run_drafting_synthesis._upstream:43` (after `source_root:55`, before
`matrix:65`: `G` + matrix↔Evidence binding `70-73` via LOW R4);
`run_evidence` canonical Ledger `715-717` + Completeness `730-732` (before either
`exists()` check: `G`; versioned R writes via HIGH only); `agent.approve_architecture:1829`
(after `source_root:1845`, before `1846-1848`: `G` + `C`); `survey_drafting_v2:130`
(every function opening that path: `G` + LOW four-ref); handlers/stage-validation/
orchestrator/editorial/publication/renewal/walker rows per §11 table (each with
call-site + oracle for 7-slot audit). Audit all-7 no-overwrite: successor runner
MUST include audit in 7-path preflight + `G` at entry/before-publish; divergent
audit overwrite never occurs because audit now in preflight.

Existing canonical upstream originals never overwritten even after adoption:
versioned R writers (HIGH exclusive, R roots only) never open canonical
`source_root/materiality-ledger-v2.json` / `profile-completeness-v2.json` for
write; `write_materiality_ledger(canonical)` / canonical `core.write_json` remain
refused paths in supersession mode.

## 8. HEAD/tree (ROOT 8, F9)

Bound current predicates (exact commands, read-only observation, no execution
here): `git -C <repo_root> rev-parse HEAD` (40-hex, cf `core.repository_commit_sha:189`),
`git -C <repo_root> rev-parse HEAD^{tree}`, `git -C <repo_root> status
--porcelain=v1 --untracked-files=no` (tracked dirt only; untracked bulk excluded
from eligibility), `git -C <repo_root> diff --raw HEAD` (mode+sha both sides).
`--ignore-submodules` mode MUST be stated per check (`none` for project
eligibility; `all` is SCOPED carryover check only, never eligibility). 55 bare
gitlinks mode `160000` WITHOUT `.gitmodules` are WORKSPACE carryover, NEVER
project runtime eligibility: HIGH/LOW MUST NOT `rev-parse` child gitlinks, MUST
NOT include child HEADs/trees/dirt in `contract_identity`/`implementation_sha`,
MUST NOT glob `resume-20261025/*/fork-*` or any `R/` prefix directory as authority.
Project eligibility = repo-root HEAD/tree + `implementation_control_roots
[config,schemas,scripts,.github/workflows]` + Profile/source/proof pins (§6 pin
sets) ONLY.

Expected maps (no execution): pre-code/implementation fixtures MUST pre-declare
`expected_head`, `expected_tree`, `expected_contract (contract_identity)`,
`expected_tool_shas (exact tool/schema/contract files)`, `expected_profile_sha`,
`expected_source_pins` in `R/request.json` + guard `work{head,tree}`. At pin +
at adopt + at resume, HIGH re-observes LIVE `HEAD/tree` + recomputes
contract/tool SHAs and requires equality (no standing main-follow, no dirty
allowance for control roots, no self-reference future SHA). F9 predicate: eligibility
requires `expected_head == LIVE HEAD` AND `expected_tree == LIVE tree` AND
`contract_identity` + `tool_shas` + Profile/source/proof pins equal, with
`status --porcelain` clean for control roots; docs/template drift = refuse (not
allow), because control roots are the trust boundary; non-control drift (e.g.
`notes/` prose) does not block DM022 eligibility but MUST be recorded as
`untracked selective exact paths` (readmode/status including untracked selective
exact paths) and MUST NOT enter `contract_identity`.

Allowed artifact-only descendant diff-set (bound, no wildcards, no gitlink
metadata): during review, an artifact-only descendant commit is admissible ONLY
if (a) `git diff-tree --no-commit-id --name-only -r <expected_head>..<observed_head>`
⊆ EXACT finite set = `{declared R output relpaths from R/request.json output
inventory} ∪ {declared review/proof relpaths} ∪ {retention manifest relpaths}`
(explicit finite list per attempt, no `R/**`, no directory prefix, no
`orchestration/v2/**` wildcard); (b) ancestry is linear descendant of
`expected_head` with NO merge; (c) every prior pin (Profile/source/proof/contract/
tool SHAs) unchanged; (d) current controls/contract identical. Otherwise refuse +
NEW bounded attempt. CodeEpoch (`implementation_sha` at generation) vs Authorities
(E at adoption) separation holds: `E` (observed work HEAD/tree at run time) ≠ `C`
(code-commit SHA reviewers bind); demanding a future self-containing commit SHA
is refused. Identity `old/new/codeEpoch` stored TRUE in guard+request
(`before_state_sha`, `expected_after_state_sha`, `work.head/tree` +
`contract_identity`), with NO self-SHA cycle (checkpoint/report carry observations
of already-existing files only; checkpoint NEVER embeds future commit SHA, NEVER
references POST receipt; proof NEVER references checkpoint).

Before-record new work HEAD changes plan hash update: if LIVE HEAD/tree advances
between `request` pin and `adopt` (new commit on top of `expected_head`), MUST
recompute ENTIRE bound intent (new `expected_head/tree`, new `contract/tool_shas`,
new `before_state` re-pin if State bytes changed, new `planned_checkpoint_bytes`
+ `planned_sha` + `expected_after_sha`, new `attempt_nonce`, new guard) and
require decision binding consistent (`D.manifest_ref == new M FILE SHA` +
`D.before_state == new before` + allowlist still subset non-DROP); no field
defaults, no silent `expected_head` overwrite, no standing main-follow. If
decision was bound to old `M`, new `M` requires NEW external decision (or
explicit re-binding with same `affected_ids`/Raw SHAs re-verified).

## 9. Dependency closures (ROOT 9)

R2 `P3S/Weekly/LF membership UNCHANGED because code branches only` REJECTED.
NEW modules/schemas invoked MUST be in pinned closures. Full proposed lists
(actual callgraph; file-pin ONLY HIGH, not just add counts):

- P3S per-route 63 = `shared_py35 + schema22 + route3 + staged1 + style1 + recipe1`;
  union 66 = 63 + other route3. Full `shared_py35` (35), `schema22` (22),
  `route3_weekly/longform` (3 each), `staged1`, `style1`, `recipe1` listed verbatim
  in `integrated-readiness-r3.json` `closures_old_exact` (copied from renewal R3;
  35 route-independent shared, route3 disjoint). Do NOT recount without that
  membership.
- Weekly `CURRENT_CLOSURE` 29 (`survey_weekly_derivation_v2.py:28-58` incl
  `READER_INPUT_SCHEMA`, `RECEIPT_SCHEMA`, `STYLE_PATH` + pubset/editorial/
  current-authority + 5 editorial schemas + manuscript/Gate/revalidation/quality/
  candidate + `.latexmkrc` + 3 renewal modules + 4 renewal schemas).
- Longform `CURRENT_CLOSURE` 34 (`survey_longform_generated_v2.py:52-87` incl
  longform reader/receipt + semantic-review/Gate + surface_gate + production/
  schema + same editorial/manuscript/quality/candidate set + `.latexmkrc` + same
  3+4 renewal files).
- Config `pipeline71` = verified `config/survey-production-v2.json`
  `contract_files.pipeline` len 71 (67 base + 4 versioned-renewal new; ordered
  list ends with stage-checkpoint/review-finding/repair-set + 4 renewal schemas);
  `implicit3` = `config/survey-production-v2.json`,
  `schemas/survey-production-profile.schema.json`,
  `schemas/survey-production-state.schema.json`; `quality3` = 3 historical docs;
  `control_roots` = `[config,schemas,scripts,.github/workflows]`.

Successor (transitive consumer analysis incl guard/complete readback included):

- P3S replay inputs: file membership UNCHANGED 63/66 for replay (DM022 adds no
  staged replay inputs). Code closure ADDS 2 modules + 5 required schemas as
  recognized historical SOURCE refs for history/retention walkers
  (`verify_versioned_history`, `load_renewal_accepted_authority`, publication
  groups accept PREARCH for evidence/materiality/completeness; Freeze/Release
  via State-bound selection). No new shared helper file; reuse via function-local
  extraction + wrapper delegation (§1.1 narrow cores verbatim); LOW header must
  enumerate exact imported SYMBOLS; any duplication returns to root for
  single-helper decision. Numeric: per-route 63→70 (+2 modules +5 schemas),
  union 66→73, Weekly 29→36, Longform 34→41, pipeline 71→76 (77 iff root
  registers optional receipt — NOT selected; receipt shape is embedded, not a
  77th pipeline file). These counts are DERIVED from full membership lists in
  `integrated-readiness-r3.json` `closures_successor_proposed` (file-pin ONLY
  HIGH), not just added counts. Extra new module/schema if genuine need →
  return ROOT, not silent budget.
- Weekly29 / LF34: file membership UNCHANGED for rendering; derivation logic
  ADDS LOW R4 resolver branch + guard/completion predicate (code_deps, not
  closure expansion). Refusing old singleton fallback is part of the branch.
- Pipeline: 71 + 5 required = 76; `control_roots` UNCHANGED; registration is
  root decision. `implicit3`/`quality3` UNCHANGED. Guard file is transient
  coordination, NOT pipeline/control/closure membership; completion receipt is
  readback predicate, NOT live selector.
- Distinguish: normal `code_deps` (top + function-local imports, §1) vs current
  `controls` (pipeline/quality/roots/`contract_identity`/`implementation_sha`/
  STATE_SCHEMA/stage_plan) vs `schemas/$ref` data (local `#/$defs/*` only, no
  remote fetch, no cross-file cycle, `$defs` repeated literally per new schema)
  vs historical `SOURCE` roles (renewal + new `dm022-*` refs as retained/COPY
  lineage for P2R/history/publication walkers — HIST descriptive, reload-by-path
  every use, never permission; old canonical Ledger/Completeness stay
  history-only after adoption, never fallback). Current-source Dependency Tool
  epoch maps (P2R/history `retention:427/history:488`, `load_renewal_accepted_authority:933`
  `before_state_ref.path` identity `974-976` + `state_sha` + retained COPY
  `504-513/540-561`) recognize PREARCH kind with full E graph (research 4 refs
  from same PREARCH record + `supersedes`/parent/anchor lineage + SELF/digest);
  no unsupported old-format ignorance: walkers MUST NOT treat PREARCH as
  unknown-producer reject after adoption, MUST NOT fall back to old singleton.

## 10. DM016 / DM017 (ROOT 10)

DM016 (fail-closed, no alias relabelling): `run_evidence_v2_interactive.SOURCE_CLASS_MAP:38-45`
(6 entries: `PRIMARY_OFFICIAL, PRIMARY_PAPER, PRIMARY_REPOSITORY, SOCIAL,
SECONDARY_INVESTOR_ACCOUNT→SECONDARY, SECONDARY`) vs
`survey_evidence_v2.SOURCE_CLASS_MAP:44-109` (Weekly-extended, ~40 values
including `paper→PRIMARY_PAPER`, `github-release→PRIMARY_REPOSITORY`,
`official-feed-item→PRIMARY_OFFICIAL`, `dailyx_x_observation→SOCIAL`,
`arxiv_atom_snapshot→PRIMARY_PAPER`, `official_web_fallback_observation→PRIMARY_OFFICIAL`,
etc.) are inconsistent; neither contains the 10 captured canonical Thematic
types (decision §8). Witnesses use ONLY genuinely supported source types under
the CURRENT validators; no canonical-type aliases merely pass. Exact supported-
type allowlists per witness are per-invocation `request.records[].entity` +
`supplement.sources[].source_class` values (must each be in the CURRENT
`survey_evidence_v2.SOURCE_CLASS_MAP` values
`{PRIMARY_OFFICIAL, PRIMARY_PAPER, PRIMARY_REPOSITORY, SOCIAL, SECONDARY}` via
`_source_class:177-184` + `validate_evidence_card:965` + `validate_edition_view:1437`
+ supplement `validate_evidence_authority_supplement:212-324`); 10 absent
Thematic types stay OPEN with explicit non-closure report. Broader taxonomy
unification is a separate prerequisite. Negative N6 (unsupported type) must
refuse.

DM017 (union, no invention): `survey_completeness_v2.py:25-35`
`OBLIGATION_KEYS` 7 fields (`obligation_id, dimension, description, status,
discovery_ids, evidence_task_ids, rationale`); `:213-236` requires
Profile-initial + every Discovery-named `obligation_ids` with traceability;
`run_evidence_v2_interactive._build_completeness:471-507` iterates initial-only
(MUST NOT be called alone). This R3 consumes FULL provided 7-field obligation
rows for union existing Profile + namedDiscovery (request `completeness.obligations[]`
each with all 7 keys, literal `fullObligation`); derives ID set = Profile-initial
IDs ∪ Discovery-named `provenance.obligation_ids` (same enumeration as
`_check_profile_completeness_extra_content:213-236`), references
`discovery_ids` = declaring DIDs (sorted, per `named:213-220`),
`evidence_task_ids` = via ledger rows (same mapping as runner but over union,
not initial-only); verifies unchanged `dimension/description` for every existing
ID against the OLD valid completeness (loaded via `before_checkpoint.completeness`
→ old `profile-completeness-v2.json`, State-free validated); refuses invention
from Profile for named-only IDs and refuses silent drops (`silently dropped:209/223`
preserved); validates built result with UNCHANGED
`survey_completeness_v2.validate_profile_completeness:265-290` +
`schema_gate.validate_instance(..., profile-completeness-result.schema.json)`
(never incomplete `_build_completeness:471-507` / `_validate_completeness_input:217-258`
initial-only path). No new obligation IDs (Discovery frozen); any unknown ID in
request vs old-union → refuse. Mechanical card/task/view hash propagation actual
schema only (`evidence-v2-run-package`, `evidence-v2-card`,
`edition-evidence-view`, `materiality-ledger` basis fields §§3–4; package has NO
`self_digest`; `card.basis.task_sha256` change ⇒ task bytes changed ⇒ card bytes
changed ⇒ card SHA changes; unchanged `cardSHA` held ONLY if `task_sha256` +
all other basis + semantic fields equal (FILE SHA equality is the check);
`view.evidence_sha256 == sha256_file(card file)`; ledger/completeness basis
exclusions limited to recomputed evidence/view/digest SHAs listed per-field in
`mechanical_projections[]`); compare unaffected semantic full projection all
root keys not implicitly ignored (`mechanical_projections[]` + `proof.unaffected_comparison.rows_checked`
cover every unaffected DID/task/card/view/ledger-row/obligation field; directory-
prefix exclusion forbidden; affected field-set limits precise per R1 §7.3 retained:
cards `status/entities/artifact/temporal.events/sources/claims/metrics/limitations/
verification` may change for affected only; views `evidence_sha256/materiality/
scope_dimensions/annotations` for affected only; ledger rows only
`downstream_disposition/evidence_view_statuses/rationale` for affected
(`evidence_task_ids` same stable IDs, `discovery_id/origin/screening_decision/
duplicate_group` immutable); completeness obligations referencing affected only
`status/rationale` (+ derived `evidence_task_ids` linkage, same IDs) may change
(`obligation_id/dimension/description/discovery_ids` immutable, verified vs old)).

Profile witnesses: Weekly (`ROLLING_WINDOW` + X/Grok transport, genuinely
supported types e.g. `official-feed-item→PRIMARY_OFFICIAL`,
`dailyx_x_observation→SOCIAL`, `arxiv_atom_snapshot→PRIMARY_PAPER`) + Thematic
(`OPEN_HISTORY_AS_OF`/`CURRENT_STATE_AS_OF` + lineage, genuinely supported types
only; 10 absent canonical Thematic types reported as non-closure, not relabelled).
Each witness carries exact allowlist (nonempty unique subset non-DROP from
Screening decisions + ledger rows), exact named-obligation rows with provenance
(declaring DIDs + old-completeness `dimension/description` equality), archived-
HTML/retrieval provenance (`supplement.sources[].raw_path/raw_sha256/byte_count/
locator/source_type/source_class/title/published_at/accessed_at/relation` +
`URL/fetched_at/SHA/bytes` + `datePublished`-as-event, never Summary quotation),
timestamp/event-meaning fields, INSPECT binding (retained ONLY where non-DROP +
valid task association + evidence status + event/clock/Profile scope + materiality
pass; never promote to KEEP/MATERIAL; HOLD→MATERIAL/SELECTED auto-promotion
refused per `survey_architecture_v2_base:526-527`), unaffected comparison, and
N1–N12 negative matrix (§11). Synthetic reviews remain nongenuine; Production
semantic NO-GO unchanged.

## 11. Loaders, after-State stages, oracles, failure matrix (ROOT 11, F3/F4/F5)

Point-to-point loader names (no readiness-bool tokens; no current-State calls in
LOW): `LOW.load_typed_checkpoint_record`, `LOW.resolve_research_authority`,
`LOW._resolve_research_from_state_bytes` (structural only),
`LOW._load_typed_four_refs`, `LOW.load_revision_request`,
`LOW.derive_before_context`, `LOW.build_revision_package_from_paths`,
`LOW.build_revision_cards_views_from_paths`,
`LOW.accept_revision_evidence_views_from_paths`,
`LOW.build_versioned_ledger_from_paths`,
`LOW.build_versioned_completeness_from_paths`, `LOW.prove_revision_from_paths`,
`LOW.check_supersession_record_from_paths`, `LOW.is_prearchitecture_record`,
`LOW.is_legacy_candidates_record`, `LOW.require_same_triplet`,
`LOW.guard_path_for`, `LOW.require_no_active_guard`, `LOW.lstat_slot`,
`LOW.require_completion_consistent` (read-only, guard-independent check of
completion receipt vs active checkpoint); Owner-A
`agent._validate_checkpoint_record` PREARCH branch,
`agent._validate_core_stage_report` new-proof branch (no recursion),
`agent._resolve_checkpoint_artifact` PREARCH dispatch,
`agent.resolve_active_evidence_views` KEEP + R4,
`pubset.resolve_stage_artifact_path` PREARCH recognition (research 4 refs via
same record; stage-template adapters inherit; research per-caller R4-or-refuse
is separate, F4 split); HIGH `prepare_revision`, `adopt_revision`,
`resume_revision`, `readback_revision`, `verify_live_eligibility`,
`_prevalidate_expected_state`, `_adopt_triplet`, `_adopt_triplet`/`_clear_seven`/
`_postread`, `claim_guard`, `write_checkpoint_as_planned`,
`replace_state_triplet`, `clear_remaining_exact_slots`,
`write_cleanup_completion`, `release_guard`, `resume_bound_attempt`.

F3 repair (hardcoded canonical reader): `survey_drafting_v2._historical_raw_authority_hashes:102`
(`matrix_path:130` + accepted root `131-134`, SHA+parsed equality `143-211`)
MUST accept versioned R4 Evidence/Matrix refs. Exact new signature (no “scoped
here” handwave):

```python
def _historical_raw_authority_hashes(repo_root: Path, evidence_ref: dict, matrix_ref: dict) -> dict
# evidence_ref, matrix_ref: NamedRef-equivalent {name,path,sha256} from LOW R4
# (same SHA+parsed-equality discipline as before, against R4 bytes, not old singletons).
# Pure; G in caller. Entry `run_drafting_synthesis_v2_interactive.main:150` via
# `_upstream:43` supplies R4 (LOW.resolve_research_authority) + `selection`
# checkpoint refs; refuses if R4 unavailable post-adoption.
```

F4 repair (single-resolver overclaim split): (a) stage-template adapter
inheritance TRUE and kept: `survey_publication_set_v2.resolve_stage_artifact_path:2181`
(`:2218-2230` resolves stage templates via profile expansion; special-case
`publication-candidate`) covers all `_l_stage_path` adapters
(`production._l_stage:47`, `stage_validation._l_stage:99`,
`human_gate.resolve_gate_path:255`, `orchestrator.resolve_configured:167`) for
stage-template paths; (b) research four-ref per-caller R4-or-refuse NOT inherited
(`_l_stage_path` never resolves Ledger/Matrix/Selection research refs; research
resolves via `agent.resolve_*`, handlers, derivation): each research caller in
§7/§11 table carries its own R4-or-refuse row (cannot inherit). Closure text
“all adapters inherit, no per-adapter fork” corrected to this split.

F5 repair (forward builders): restore two explicit rows (dropped in R2):
`agent.build_stage_checkpoint:1703-1765` UNTOUCHED (new PREARCH builder separate;
never `advance_with_checkpoint` with fabricated State) and
`agent.advance_with_checkpoint:1768-1826` REFUSE PREARCH kind (producer NONE for
`EVIDENCE→EVIDENCE`; adoption is HIGH single-file switch only) with guard check
location (`G(source_root via _profile_and_source:307)` at entry) + oracle
(DM022 record via this path always refuses). Both are public entry points
callable directly, not only via orchestrator/bridge (`orchestrator.execute_action:635`
→ `transition:694`, `bridge._advance_stage:365` → `advance:401` refusals are
caller-side only, not substitutes).

After-State stages through publication/R1/editorial/renewal (each with exact
disposition; no unchanged-consumer claim):

- Selection/Architecture/Draft/validation/publication-preview/Freeze/Release
  forward advancement: normal `advance_with_checkpoint:1768` / `transition_state:998`
  + `plan_action` + `_validate_architecture_attestation:723` /
  `apply_architecture_approval:744` refuse PREARCH kind through forward path;
  adopted-checkpoint readback through `SELECTION_COMPLETE→ARCHITECTURE_ESTABLISHED→
  DRAFT_COMPLETE→VALIDATED_DRAFT→RELEASE_CANDIDATE→FROZEN→RELEASED` validates
  ADOPTED record via retained COPY/lineage (no live-before equality, no window
  re-check, no `repository_commit_sha` equality with revision HEAD).
- Draft/Synthesis/Reader derivation (`survey_weekly_derivation_v2.load_derivation:585`,
  `survey_longform_derivation_v2._derive_authority_context:1020` +
  `load_derivation:1157` + `load_derivation_for_readback:1198`,
  `survey_drafting_v2_base`, `run_drafting_synthesis.main:150`,
  `run_semantic_publication.main:118`): rewire `ledger/matrix/completeness` via
  R4 + State-bound selection; `load_derivation_for_readback` MUST accept adopted
  PREARCH through `READBACK_LIFECYCLES` (no `EVIDENCE_REVIEWED` demand at readback).
- Publication proposal/retention (`survey_publication_v2` groups `644-680` + M1-M6
  `757-799` + Freeze/Manifest `760-772`, `survey_profiled_freeze_v2:29`,
  `survey_release_checkpoint_v2:22`, `survey_editorial_retention_v2:857/1737`,
  `survey_editorial_staged_source_v2:656`, `survey_stage_validation_v2:226/263/352`,
  `survey_publication_set_v2:1213/1627/1981/1956/2135/2181/2267`): walkers MUST
  accept PREARCH record for `evidence/materiality/completeness` group (same 4-name
  set, new kind/operation branch, `artifact set mismatch:754-756` updated to allow
  PREARCH `from/to`); Freeze/Release resolve via State-bound selection (no stale
  canonical); retention/staged/current-authority validators take explicit R4 +
  PREARCH wrapper refs post-adoption (no canonical fallback); Human approval refs
  NEVER rebound.
- R1/editorial/renewal accepted-source/retention walkers
  (`survey_editorial_correction_proposal_v2:1454/1490/1502`,
  `survey_editorial_publication_v2:749/1631/3260/3748`,
  `survey_versioned_renewal_source_v2:407/933`, `survey_versioned_renewal_history_v2:3864/4200`,
  `survey_versioned_renewal_v2:619/1068/1578/3247/3575/3500`,
  `survey_weekly_mechanical_refresh_v2:931`,
  `survey_reader_surface_gate_v2:1152`, `survey_execution_record_v2:82/284`,
  `survey_reader_publication_v2:171`, Weekly/Longform receipt validators):
  MUST recognize PREARCH kind/digest and full E graph (research 4 refs same record
  + lineage; `before_state_ref.path` == canonical Source Path identity `974-976`
  + `state_sha` actual before + retained COPY separate); renewal entry window
  (`_observe_renewal_entry:619`, `_require_renewal_entry_window:560`
  VALIDATED_DRAFT+approved) INELIGIBLE for DM022 creation (refuse); later renewal
  walkers accept PREARCH-adopted lineage as valid research history (no window,
  no before-equality). Current-source Dependency Tool epoch maps (retention/history
  `SOURCE` roles) no unsupported old-format ignorance.

Exact public oracles (Weekly + Thematic, both sides, negatives as refusals; no
readiness-bool tokens; LOW never calls current State): O-W1 (Weekly
`ROLLING_WINDOW`+X/Grok) / O-T1 (Thematic `OPEN/CURRENT_STATE_AS_OF`+lineage,
supported types only, union obligations, article bytes + `URL/fetched_at/SHA/bytes`
+ `datePublished`-as-event) happy paths (`entry` pinned `EVIDENCE_REVIEWED` +
preserved Discovery/Screening/Profile + old accepts immutable + newly captured
input proof; `seam` §5 order; `observed` new 4 under R + same-record triplet +
7 retained-then-cleared + completion + guard release + fresh Matrix/Selection/
Architecture + Gate later); O-W2/O-T2 forward Draft/Reader closure via LOW
resolver + completion (no old fallback); O-R1 repeated revision with NEW rev+nonce;
O-G1/G2/G3 guard interruptions before/after switch + release failure per F8/F9/F13;
N1–N12 negatives (stale-canonical reuse, fake Gate/REQUEST_CHANGES, malformed/split
refs `resolve_active_evidence_views:920-932`, wrong stage/prior review, missing
obligations `survey_completeness_v2:208-223`, unknown types, INSPECT misuse,
clock/quotation misuse, stale HEAD/controls/Raw, metadata-only promotion,
ownership/close/replace faults, ordinary collision) each as REFUSAL with
`entry + seam none + writes none (except allowed owned inert prep)`. Earlier
refusal ≠ later seam proof. Synthetic reviews nongenuine; Production NO-GO
unchanged. Cost unknown, no numeric claim.

Failure matrix (exact old/new/unknown per failure; retains `P+Q`, `S∈{B,E,unknown}`,
partial preservation, no delete of referenced/possibly-referenced records,
retained COPYs, or unknown guard; no CAS/crash claim; `core.write_json`
equivalence REVOKED for guard/State/checkpoint/completion/slot writes):

| # | Boundary | Behavior |
|---|---|---|
| F1 | Invalid basis / changed ID/Raw/Profile / failed review/content proof / unsupported stage/mode (before adoption) | REFUSE before guard claim/cleanup. Preserve `R/` + early copy. No State write, no slot unlink. Resume = NEW `rev`+`nonce` (collision → `DM022_TRANSITION_ACTIVE`, no fork). Normal callers: `G` absent so proceed normally; 7-slot audit oracle: zero of seven changed. |
| F2 | Incomplete candidate/retention/proof/planned-checkpoint (before guard) | PRESERVE; no takeover. NEW rev+nonce unless immutable completed phase has explicit validated continuation (exact phase+bytes+sha in manifest). |
| F3 | `write` fault (exclusive-temp create/write raises) | Retain `P(errno)` + `S` re-observation. `S==B`→F8. Unknown→F11. NEVER overwrite possibly-referenced file; NEVER delete `R`/retention. Explicit resume reloads bound intent, MAY proceed only if `S==B` + guard held + planned sha matches. |
| F4 | `short-write` (temp bytes < expected; temp sha != planned/`E`) | Temp NOT LIVE: LIVE `B` preserved (temp sibling only). Retain `expected vs actual` + LIVE `B` proof. NEVER rewrite unknown LIVE to `B/E`. Resume = rewrite temp under held guard (same nonce/planned bytes) or F11. |
| F5 | `fsync/close/dirfsync` fault (raises; close error never swallowed) | `P` write-ok + `Q` sync/close error, both retained. Re-`lstat`+re-hash → `B`→F8, `E`→F7/F9/F10, else F11. Logger text NOT proof. |
| F6 | `replace` fault (`os.replace` raises; temp lands wrong; COPY lands wrong path) | Record BOTH old/new dispositions. Temp-E present ≠ live adopted: ONLY canonical LIVE disposition counts. Old LIVE still `B` + temp absent/partial → F8. Either path shows `E` at canonical LIVE → F9/F10 family. Preserve both, delete neither. |
| F7 | `after-read` fault (post-replace `lstat`+hash+`validate_agent_state`+triplet fail, or read raises) | Adoption gate. `S==E`+PASS→clearing (F9). `S==E`+FAIL→preserve `S==E` bytes+record+guard, posture cleanup-pending WITH reported defect; explicit resume must re-prove readback before clearing. `S==B`→F8. Neither/unreadable→F11. NEVER restore `B` over new/unknown. |
| F8 | Complete record, `S==B` exactly, cleanup not started | Ordinary adoption REFUSES same intent. EXPLICIT HIGH resume ONLY: reload guard+request+retention+planned bytes (`sha==guard.planned_sha`), revalidate LIVE eligibility + guard holder + HEAD/tree, then MAY switch. Same-rev collision cannot fork. Normal callers during window: `G` present → ALL refuse. |
| F9 | `S==E` exactly, cleanup incomplete | EXPLICIT HIGH resume: verify triplet same-record + 4 live hashes, clear ONLY remaining EXACT old planned slots with pre-unlink reverify (`lstat` regular + `sha==captured_old` + COPY verified + still unaccepted/unbound + guard held). `missing+already-cleared` allowed (record). `changed-foreign` (present but `sha/dev/ino != captured`, EVEN IF bytes equal) → preserve+refuse. `new file at cleared path` → preserve+refuse (may be early regen — operator decision, never delete). |
| F10 | `S==E` + cleanup complete + completion verified | Full readback + readonly `ALREADY_ACTIVE`/complete. NO new acceptance/approval. Normal regen proceeds ONLY after guard release + completion verified (§6 predicate). |
| F11 | `S∉{B,E}` or unreadable/ownership unverifiable; guard unknown/malformed/unreadable; pin mismatch | INDETERMINATE. Preserve records/bytes/guard+retention. NO State restore/delete/adopt. Read-only diagnosis allowed (no `G`). Return exact blocker; if A1 map cannot preserve invariants → A1-vs-A2 revisit (decision §9), never partially guarded A1. |
| F12 | `unlink` fault per slot (pre-unlink reverify fails or `unlink` raises) | Retain `P` + per-slot `observed` (`old-captured`/`changed-foreign`/`missing-cleared`/`new-foreign`). `changed/new-foreign`→preserve+refuse (stay F9). `missing-cleared`→record+continue. Guard stays held; NO release until postread+completion pass. 7-slot audit oracle: each slot's `observed` recorded in completion `seven_plan`. |
| F13 | `guard-release` fault (raises; `dev/ino/sha` mismatch; guard absent at release) | Classify by observed existence/identity, do NOT claim always-held. Held-by-self verified → release (unlink + dir fsync + verify absent) → regen unblocked (completion already verified). Absent (`ENOENT`) → record `guard_absent_at_release`, posture INDETERMINATE (lost-guard window: writers MUST still require completion; do NOT silently proceed). Foreign/mismatched → refuse, no takeover/delete. Writers while guard (any) present → refuse; after release + completion → proceed per §6 predicate (late-State-forward OK, no demand seven still absent post-regen). |

Normal-caller 7-slot audit code oracle (applies to every §7 row): with `S==E` +
completion verified + guard ABSENT, successor `run` MUST include audit in 7-path
preflight and MUST write all 7 fresh (no divergent audit overwrite); with guard
PRESENT (any) MUST raise `DM022_TRANSITION_ACTIVE` before first of 7 writes;
with active new-kind checkpoint but NO completion (lost-guard window) MUST refuse
7-slot writes until HIGH re-establishes completion or manual resolution. Each
refusal records `entry + intended seam (none taken) + observed writes (none)`.

## 12. F1–F9 closure (independent review blockers)

- F1 HIGH bare `records` schema (`schemas-generation-dag-r2.md:236`
  `"items":{"type":"object"}`): CLOSED by `schema-proposals/dm022-revision-request-v2.schema.json`
  `$defs.weeklyRecord/thematicRecord/interactiveRecord` literal COMMON/WEEKLY/
  THEMATIC shapes from `run_evidence_v2_interactive._validate_record:119-214`
  (+ `entity/claim/verificationItem` nested defs); no generic object.
- F2 HIGH only request has literal JSON: CLOSED by five literal files under
  `schema-proposals/` (request/manifest/proof/preadoption-report/checkpoint,
  each `additionalProperties:false`, `required`, `properties`, `$defs` repeated
  literally, `if/then/contains` for checkpoints/artifacts, `reviews` sole
  `DM022_SUPERSESSION_PROOF`, `contract` 8-field, `implementation` 2-field,
  digests `*_sha256==sha256_object(body-minus-self)`, FILE SHA distinct).
  Report has NO `checkpoint`/`expectedAfterState`/`guard` hash fields
  (`additionalProperties:false` enforces; `guard_claimed` bool + `guard_path`
  string descriptive only). Checkpoint has NO backref to completion.
- F3 HIGH hardcoded canonical reader DSS pure vs caller R4: CLOSED by exact new
  signature `survey_drafting_v2._historical_raw_authority_hashes(repo_root,
  evidence_ref, matrix_ref)` (§11) + entry `run_drafting_synthesis.main:150` via
  `_upstream:43` supplies R4 + `selection` refs; pure function stays pure, caller
  passes R4 paths (no “UNCHANGED pure, callers pass R4” without signature).
- F4 HIGH single-resolver overclaim: CLOSED by split (a) stage-template inheritance
  TRUE via `pubset.resolve_stage_artifact_path:2181` for `_l_stage_path` adapters
  + (b) research four-ref per-caller R4-or-refuse rows (cannot inherit); closure
  text corrected in `integrated-readiness-r3.json` `research_vs_stage_split`.
- F5 HIGH forward builders have no dedicated rows: CLOSED by two restored rows
  (`build_stage_checkpoint:1703` UNTOUCHED + new PREARCH builder separate;
  `advance_with_checkpoint:1768` REFUSE PREARCH kind + `G` location + oracle) in
  R3 inventory rows 31–32; no caller-only refuse.
- F6 MEDIUM count/bundling: CLOSED by R3 36-row unbundled inventory
  (`integrated-readiness-r3.json` `rows[]` 36 exact per-function rows; R2 30-md vs
  29-json bundling preserved as history with explicit mapping in §7; D4 + `:201`
  count corrected: 30 md numbered = 29 json (row 5 missing, row 3 bundled); R3 36
  = 30 R2 numbered unbundled (rows 3,5,16,24,26 split) + 2 F5 restored + 4
  screening/prior/handler splits).
- F7 HIGH no-State-arg guard derivation per caller missing: CLOSED by per-caller
  `guard_derivation` (`repo_root→cfg→Profile→source_root→guard_path_for→
  require_no_active_guard`, or explicit `refuse in superseded mode` with
  kind-check location) for every no-`state_path` mutating path in R3 json
  (§7 examples; pattern alone not closure).
- F8 HIGH schema-owner branch text still OPEN: CLOSED by literal branch JSON
  (standalone new `dm022-supersession-checkpoint-v2.schema.json` + shared
  `LOW.load_typed_checkpoint_record` dispatch; all 17 direct schema sites +
  8 validator branches enumerated §2; old file UNCHANGED; registration decision:
  pipeline 71→76, `control_roots` unchanged, `contract_identity` recomputed on
  new disk, staged/P3S/Weekly/LF file memberships unchanged for replay per §9).
- F9 MEDIUM HEAD/tree complete-set scope ambiguous: CLOSED by exact predicate
  (`expected_head == LIVE HEAD` AND `expected_tree == LIVE tree` AND
  `contract_identity` + `tool_shas` + Profile/source/proof pins equal, `status
  --porcelain` clean for control roots; docs drift = refuse; non-control drift
  recorded as untracked selective exact paths, not eligibility) + finite
  artifact-only descendant diff-set (no `R/` wildcard) + no gitlink eligibility
  + before-record HEAD-change recompute rule (§8).

Non-blocking notes (no repair required, recorded): 30 vs 29 is bundling once
clarified (F6); dropped R1 Profile rows (`SOURCE_CLASS_MAP:38/44`,
`_build_completeness:471`, `completeness_extra:145`, `build_ledger:1579`) are
Profile predicates (§10 DM016/017) not B2 rows, traced explicitly; `reader_publication`
+ `weekly_mechanical_refresh` canonical refs are stage/publication-surface, not
research four-ref (covered via C row12 walker recognition-or-refuse + publication_set
single-resolver for stage paths, research cutover per F4 split); new 2+5+1 budget
justified (merging manifest↔proof forces future ref; proof↔report forces self-digest
cycle; report↔checkpoint recreates cycle; embedded guard/retention/completion defs
refuse duplication); if implementation needs more, return to root (closure D3).

## 13. Residual + stop (honest, no PASS)

This R3 closes the MAP gaps (literal schemas, per-caller exact signatures, loader,
guard derivation, HEAD/tree predicate, closure memberships, F1–F9 repairs). It does
NOT claim MAP-COMPLETE/GO, independent PASS, or implementation authorization:

- Astra + author-independent readiness review MUST confirm this R3 (schemas +
  map + inventory) before any code. Implementation remains BLOCKED until that
  confirmation. Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN
  preserved. DM016 10 absent Thematic types, DM017 builder alignment, necessary
  Profile/representative-quality/fixed-candidate/audit/Human-adoption/savings remain OPEN.
- Per-invocation values are NOT pre-pinned here (no invented IDs/Raw/SHAs):
  `expected_head/tree`, `contract_identity`/`tool_shas` recomputed values,
  `profile/discovery/screening` SHAs, `before_state` bytes, 7-slot observations,
  `affected_ids` allowlist, named-obligation rows, archived-HTML/retrieval
  provenance, `mechanical_projections[]` recomputed SHAs, `executor/recorded_at`
  must be bound at invocation and re-verified at pin/adopt/resume; stale values
  refuse + NEW bounded attempt (§8).
- No `implementation-later-will-close-map` handwave: every listed caller has an
  exact disposition + guard location + oracle in `integrated-readiness-r3.json`;
  any reviewer-found extra DIRECT reader not listed here is a precise OPEN blocker
  (pre-code stays NO-GO until it gains a file:function:line row with R4-or-refuse).
- Stop internal. No code, no fixture, no runtime, no Commit Point claim.
  Ordinary Commit/Push Human-owned.

### Preservation + source citations

R1/R2 preserved untouched (see §13 header). Source-grounded citations:
`survey_agent_control_v2.py:42/348/365/481/489/761/819/902/1011/1532/1608/1703/1758/1774/1782/1829/1971/2397/2911`,
`survey_evidence_v2.py:44-109/177-184/212-324/379-410/413-446/449-464/467-474/482/539-681/640-652/719-766/769-836/839-895/898-946/965/1152-1156/1159-1213/1216-1253/1255-1283/1286-1319/1322-1349/1366/1412-1434/1437-1491/1494-1495/1498-1552/1555-1577/1579-1655/1658-1723/1725-1794/1797-1801/1804-1941/1944`,
`run_evidence_v2_interactive.py:38-45/119-214/471-507/586-774`,
`survey_completeness_v2.py:25-35/50-78/81-142/145-262/265-290/208-223`,
`survey_screening_v2.py:353/402/442/465/480/809`,
`run_selection_architecture_v2_interactive.py:158-353`,
`survey_publication_set_v2.py:56/1213/1627/1956/1981/2135/2181/2267`,
`config/survey-production-v2.json:266-275/298-306/pipeline71`,
`schemas/stage-checkpoint-v2.schema.json:74/111-134/200-208`,
`schemas/evidence-v2-run-package.schema.json`, `schemas/evidence-v2-card.schema.json`,
`schemas/edition-evidence-view.schema.json`, `schemas/materiality-ledger.schema.json`,
`schemas/profile-completeness-result.schema.json`,
`schemas/survey-production-state.schema.json`. Availability: final93 proof-copy
available; full93/742/file-inode/guard recertification NOT performed here (carryover
§8 scope retained); 55 bare Gitlinks + child dirt preserved, NOT cleaned/relocated
(`source-and-carryover-observation.md`).

(End of file)
