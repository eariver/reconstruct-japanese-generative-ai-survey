# DM022 pre-Architecture — integrated pre-code readiness R4 (AUTHOR, PRE-CODE ONLY)

2026-10-28 AUTHOR integration worker. PRE-CODE ONLY. Human `ab84b4f` assumed.
No source/runtime/import/tests/build/fixture/restore/network/Git writes.
Actual93 proof-copy READONLY. No candidate/reconstruct Commit/Push.
Preserves EXACT: R3 `integrated-readiness-r3.md/json` + `schema-proposals/dm022-*.schema.json`
(5 files, reviewed B1–B5 history), all R1/R2, `independent-readiness-review.md` §§0–5
(NOT_READY). This file + `integrated-readiness-r4.json` + `schema-proposals-r4/*.schema.json`
are the ONLY writes of this unit. No installed runtime. No MAP-COMPLETE/PASS claim.

Binds: decision `outputs/rephase-1-dm022-prearchitecture-contract-decision.md`
incl. §11, SHA256 `a345bb9524b4dfc5b5f32600d0d708687e2b6131d91a43965c97b6418388f223`/31351B
(unmodified); `notes/rephase-1-dm022-prearchitecture-contract/astra-review-resolution.md` incl. §5;
BOTH independent design reviews WITH FINAL-BINDING addenda (selection only).
Source: proof-copy `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`
= actual `409b292`/tree `8ce36998` +93/742. All `file:line` below are proof-copy
unless stated `workspace:`. Method: `Read` + `Grep` + `ast` parse as DATA only;
ordinary `json` parse/`ast`/hashing as data readonly source. No `scripts.*` imports.

R4 supersedes R3 as authoritative pre-code map for B1–B5 + root compatibility
clarifications. R3 preserved exact for history; R4 is concise complete (deltas
fully specified, unchanged R3 mechanics incorporated by reference with exact
locations, no verbatim instruction copy).

## 0. What R4 fixes (B1–B5)

- B1 ownership: LOW passive guard absence + completion check allowed (pure/file-path
  IO, no State authority); NO LOW agent/HIGH/public State validation; HIGH alone
  writes + clears; LOW builders return dict/bytes/planned map; per-entry zero-write oracles.
- B2 registry: proof adds explicit `evidenceAcceptance`/`viewsAcceptance` (exact real
  fields/digests); report registry retargeted to fixed filenames + local pointers +
  function validators (no dangling, no $id mismatch, closed/local).
- B3 readiness: ONE passive `require_research_operation_ready(repo_root,state_path)`;
  READY entry+prepublish on every mutating row; 5 split rows for execution_record/
  reader_publication/receipts; readonly vs write-permit distinction; COPY-derived
  expectedAfter; 40-row count match; 7-slot audit all-no-overwrite.
- B4/B5 families: THREE FINITE families G67/G71/G76 with full literal path lists
  in JSON; owned-epoch derivation; narrow G71→G76 mechanical compat; witnesses;
  no general migration.

## 1. Modules / ownership (B1)

- LOW `scripts/survey_research_authority_v2.py` (NEW, detached, PATHS-only):
  top-level ONLY `core` (shape-only: `repo_local_path, sha256_file/object/bytes,
  json_bytes, load_json, parse_instant, iso_utc` — NEVER `verify_state_basis,
  transition_state, repository_commit_sha`), `schema_gate`, stdlib.
  Every `evidence/screening/completeness/discovery/agent` access function-local,
  then ONLY §1.1 pure cores. NO `agent`, NO `HIGH`, NO public State validation,
  NO canonical/State/guard mutation. Prepare inert writes to NEW R only via HIGH
  exclusive writer (LOW never claims/releases guard, never writes State/slots).
  Passive IO allowed: `guard_path_for` (pure join), `require_no_active_guard`
  (lstat absent-pass else `DM022_TRANSITION_ACTIVE`; no State, no agent.validate,
  no FD/lease), `require_completion_consistent` + `require_research_operation_ready`
  (file/path inputs fully reload + exact verify; no State authority).
  Guard absence read + completion check is distinct from detached checkpoint proof
  (agent State validator calls detached proof, NEVER operational guard; LOW never
  calls State guard from agent validator; no recursion).
- HIGH `scripts/survey_prearchitecture_acceptance_v2.py` (NEW, SOLE mutator while
  bound guard exists): top-level ONLY `core, schema_gate, LOW`. Writes new
  R/package/task/card/view/acceptance/ledger/comp/COPY/manifests/proof/report/
  checkpoint/guard/completion/State + clears 7 via exclusive
  `O_CREAT|O_EXCL`/short-write/`fsync`/checked-close/`replace`/`dirfsync`/postread
  (never `core.write_json`/`copy2`/`is_file`). Function-local agent/evidence/
  screening for eligibility only.
- Owner-A `scripts/survey_agent_control_v2.py` (existing): new-kind branch inside;
  calls LOW detached proof function-locally for history/detached checks.

### 1.1 LOW leaf cores (exact, no invention)

`survey_evidence_v2.py`: `_check_evidence_package_fields_content:719`,
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
`survey_completeness_v2.py`: `_validate_obligation_shape:50`,
`_thematic_closure_errors:81`, `_check_profile_completeness_extra_content:145`,
`_validate_profile_completeness_content:241`.
`survey_screening_v2.py`: `_resolve_effective_discovery_basis_content`,
`_validate_screening_acceptance_content`, `read_jsonl/validate_discovery_set`.
State-bound wrappers keep exact old behavior (wrapper-delegation in implementation).

### 1.2 Signatures (R4 corrected, no Path-implies-write)

```python
# LOW (passive + pure; zero-write oracles in JSON)
def load_typed_checkpoint_record(repo_root: Path, path: Path) -> dict
def resolve_research_authority(repo_root: Path, state_path: Path) -> dict
def _resolve_research_from_state_bytes(repo_root: Path, state: dict) -> dict
def _load_typed_four_refs(repo_root: Path, structural: dict) -> dict
def load_revision_request(repo_root, request_path) -> dict
def derive_before_context(repo_root, request_path, before_copy_path, previous_checkpoint_path) -> dict
def build_revision_package_from_paths(...) -> dict  # + planned file map, NOT Path
def build_revision_cards_views_from_paths(...) -> dict
def accept_revision_evidence_views_from_paths(...) -> dict
def build_versioned_ledger_from_paths(...) -> dict
def build_versioned_completeness_from_paths(...) -> dict
def prove_revision_from_paths(...) -> dict
def check_supersession_record_from_paths(...) -> list[str]
def guard_path_for(source_root: Path) -> Path
def require_no_active_guard(source_root: Path) -> None
def require_completion_consistent(source_root: Path, checkpoint_ref: dict) -> None
def require_research_operation_ready(repo_root: Path, state_path: Path) -> None
def lstat_slot(source_root: Path, rel: str) -> dict
```

```python
# HIGH (sole mutator)
def prepare_revision(repo_root, state_path, request_path, revision_id) -> dict
def adopt_revision(repo_root, state_path, revision_path, decision_path) -> dict
def resume_revision(repo_root, state_path, revision_path) -> dict
def readback_revision(repo_root, state_path, revision_path=None) -> dict
def verify_live_eligibility(repo_root, cfg, state) -> list[str]
def claim_guard(...) -> dict
def write_checkpoint_as_planned(guard) -> dict
def replace_state_triplet(guard) -> dict
def clear_remaining_exact_slots(guard) -> dict
def write_cleanup_completion(guard) -> dict
def release_guard(guard) -> dict
```

Public LOW validation input paths fully reload (lstat+read+hash+schema+content);
private pure in-memory compute takes already-loaded dicts, creates no files,
issues no guard/State calls. Zero-write oracle per API in JSON.

## 2. Checkpoint + schemas (B2)

Old `schemas/stage-checkpoint-v2.schema.json` UNCHANGED. New record:
`kind=PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`,
`reason=REVIEWED_ACCEPTED_UPSTREAM_CORRECTION`,
`operation` EVIDENCE→EVIDENCE, `producer_boundary` CANDIDATES→EVIDENCE,
3 roles + 4 refs, State 3 refs SAME record atomic file, lifecycle/history/gates
unchanged, late readback allowed. Loader `LOW.load_typed_checkpoint_record`
strict kind dispatch, no `.get` fallback. 17 direct sites + 8 branches per R3
§2 / R4 JSON (unchanged, incorporated).

R4 `schema-proposals-r4/` FIVE standalone (ROOT): request/manifest/proof/report/
checkpoint (`dm022-*`, `$defs` repeated literally, `additionalProperties:false`
throughout, `if/then/contains` for checkpoints/artifacts, `reviews` sole
`DM022_SUPERSESSION_PROOF`, contract 8-field, implementation 2-field,
digests `*_sha256==sha256_object(body-minus-self)`, no bare object/ellipsis).
Request records mirror `run_evidence_v2_interactive._validate_record:119-214`
(COMMON/WEEKLY/THEMATIC + REJECTED→NON_MATERIAL / NEEDS_MORE→HOLD).
Decision embedded `request.$defs.suppliedDecision` (actual before/after/allowlist/
raw/assessment, no PASS generation). Retention/guard/completion embedded
`report.$defs` (coordination views, checkpoint never backrefs).

B2 fix: proof `$defs` adds `evidenceAcceptance` (exact keys
`schema_version,issue_id,research_profile,result_set_sha256,package_sha256,
screening_acceptance_sha256,result_count,results[]`; results rows
`evidence_task_id,discovery_ids,sha256,status,filename^task-[0-9a-f]{20}\.json$`;
digest `result_set_sha256=sha256_object({package_sha256,results sorted})`,
run_dir name == digest) per `_validate_evidence_acceptance_content` +
`_check_evidence_acceptance_results_content:1216` + `accept_evidence_results:1159`;
and `viewsAcceptance` (keys `schema_version,issue_id,research_profile,
view_set_sha256,profile_sha256,evidence_acceptance_sha256,views[]`; rows
`evidence_task_id,evidence_sha256,view_sha256,materiality,scope_dimensions`;
digest `view_set_sha256`, run_dir name == digest) per
`_validate_edition_views_acceptance_content:1322` +
`_check_views_acceptance_rows_content:1286`. Report `roleSchemaRegistry`
retargeted to fixed filenames + local pointers + function validators (no URLs):
evidence-acceptance → `schema-proposals-r4/dm022-revision-proof-v2.schema.json`
`#/$defs/evidenceAcceptance` via `_validate_evidence_acceptance_content`;
edition-views-acceptance → `#/$defs/viewsAcceptance` via
`_validate_edition_views_acceptance_content`; materiality-ledger →
`schemas/materiality-ledger.schema.json` `#` via
`_validate_materiality_ledger_content`; profile-completeness →
`schemas/profile-completeness-result.schema.json` `#` via
`_validate_profile_completeness_content`; candidate-matrix →
`schemas/candidate-matrix-v2.schema.json` `#` (actual `$id`
`example.invalid`, corrected from github) via `validate_selection`;
candidate-selection → `schemas/candidate-selection-v2.schema.json` `#`
(actual `example.invalid`) via `validate_architecture`. All `$ref` local
`#/$defs/*` only, data-only traversal, no remote fetch, no cross-file cycle.

## 3. Guard + completion readiness (B3)

ONE passive LOW `require_research_operation_ready(repo_root: Path, state_path: Path)
-> None`: lstat guard ANY present (well-formed/malformed/nonregular/unreadable)
refuses `DM022_TRANSITION_ACTIVE`; else structural kind peek of State file
(no validation): legacy (no kind) → only guard absence required; PREARCH →
guard absent + `require_completion_consistent` exact verify (checkpoint SHA +
COPY-derived `expected_after` + `seven_plan` vs slot lstat). No
`agent.validate_agent_state`, no `verify_state_basis`, no HIGH, no guard claim.
HIGH normal writers import as passive IO (`HIGH→LOW` allowed, no recursion).

Normal no-State-arg Profile-aware entries derive canonical STATE via Profile
source_root/config then call ready (e.g. handlers `_evidence_basis:204`,
stage_validation `_evidence_basis:402`, pure writers via entry, execution_record,
reader_publication, receipt validators). Pure/private builders receive validated
4-refs from entry, no source selection themselves. Public writer with Profile/
state context that can write canonical root but lacks bindable Profile/state:
introduce explicit State/Profile path param at public entry or fail-closed if
cannot bind — no guard-skip/foreignRoot.

EVERY mutating entry invokes READY BOTH entry + prepublish (R4 JSON 40 rows;
only row 20 had `+C` in R3). Added dedicated rows: execution_record
`_load_state:82`/`validate:284`, reader_publication
`_validate_renewal_manuscript_binding:171`, weekly `validate_receipt:836`,
longform reader input `validate_longform_reader_input:983` (receipt validators
are diagnostic replay, not write permits). READONLY diagnostic/data validators
don't require guard absence but are NOT write permits; caller producer readiness
separate. Completion after forward compares COPY-derived operation expectedAfter
only, not LIVE equality/slots now absent. Publication readback source proof
while guard? Guard only preArch transition; after later stage none; LOW never
recurses State guard from agent validator (agent validator calls detached proof,
NEVER operational guard). Completion lost/guard missing still normal block;
explicit resume RECOVERY bound known intent, no automatic takeover. 7-slot audit
all-no-overwrite (successor preflight covers all 7 incl audit `:330-343`).

40-row count matches JSON (`counts.rows==40`); any extra DIRECT reader not listed
is precise OPEN blocker.

## 4. Families + compatibility (B4/B5)

THREE FINITE families, owned epoch from EXACT config registered path sets +
contract8 recompute + schema fingerprints + expected module/mode/membership
(never 7-file presence/hard count). Full literal path lists in R4 JSON
(`families.G67/G71/G76`; actual derive elements, not counts):

- G67 (pre-renewal, historical only): pipeline OLD67 (67, literal
  `_OLD_PIPELINE_67:99-167`), staged OLD50 per-route (50 =
  OLD_PY_30 + OLD_SCHEMAS_14 + route3 + staged1 + style1 + recipe1),
  implicit3, quality3, control_roots. No renewal modules, no PREARCH kind.
- G71 (renewal, current before DM022): pipeline NEW71 (71 = OLD67 + 4 renewal
  schemas `_NEW_SCHEMAS_4`), staged NEW63 per-route (63 = OLD50 + FAMILY_PY_2 +
  NEW_PY_3 + NEW_SCHEMAS_4 + FAMILY_SCHEMAS_4), canon Weekly29
  (`survey_weekly_derivation_v2.py:28-58`) + Longform34
  (`survey_longform_generated_v2.py:52-87`), implicit3/quality3/roots.
  Supports versioned renewal publication; no PREARCH kind.
- G76 (DM022, current after): pipeline NEW-DM76 (76 = NEW71 + 5 DM022 schemas
  `schemas/dm022-*.schema.json`), replay per-route 70 (= NEW63 + 2 modules +
  5 schemas), union 73 (= 70 + other route3), canon Weekly36 (= 29+7) +
  Longform41 (= 34+7), implicit3/quality3/roots. New 2 modules pinned; HIGH
  file-pin ONLY but runtime-loaded root/bytes verified; P3S normal caller import
  avoids test preload (lazy bindings per current93 precedent); any additional
  module => return root. Counts proposed, not measured source.

Owned-epoch verification stays OWN epoch (no old tool LIVE): historical G67/G71
via retained COPY/lineage + `supersedes`/parent/anchor + SELF/digest, no
live-before equality; current G76 supports new PREARCH CP in accepted graph
through initial publication/editorial/renewal + normal lifecycle
(§11.2 readback, no entry-window recheck).

Narrow G71→G76 mechanical compat ONLY: +2 modules +5 schemas + old-shape-preserving
modified callers (17 loader sites + 8 branches, exact rewiring/refusal per rows)
+ config pipeline registration 71→76, SAME accepted research/Profile/Architecture/
Draft/reader authority. Old G67 adapter can compose known G71→G76 with same strict
conditions. MECHANICAL source-family compat ONLY; NEVER authorizes upstream changes
after Architecture/VALIDATED. Anything outside known semantic contract
(Profile/review requirements/recipe/new accepted inputs) refused separately.
Explicit allowed change/predicate/path/hash tables in rows + guard + head_tree;
no general migration/bypass. New PREARCH checkpoint only admitted G76 creation
window; older histories no such kind. Existing publication HIST generation,
source-proof current closure/supported epochs/schema-owner registry + P1/P2R/P2V/
P3S + R1 canonical current tools all recognize families without forcing old record
into G76 (old before-E accepted graph path+hash same where unchanged; active new
G76 CP novel-kind authoritative proof-chained, not hash-only). Current source
family + bootstrap adapter semantics, not unselected arbitrary Core migration;
don't invent structural P1 context from dictionary.

Required witnesses (precode oracles only, no execution): G71 current versioned
publication → G76 mechanical renewal with UNMODIFIED upstream as bootstrap compat
negative counterexample (no actual upstream adoption there); G76 DM022 accepted CP
→ initial publication → later editorial/renewal under G76 + history readback
G67/G71.

## 5. Retained R3 mechanics (incorporated, not repeated)

Prepare/adopt split (`M←D←P←RPT←CP→State→POST`, no self/future SHA; proof NO
checkpoint, report NO afterState/guard-hash, checkpoint NO guardRef/backref;
planned bytes deterministic in-memory + FILE sha + expectedState before guard;
resume reconstruct-or-fail-closed); before-State COPY + 7-slot retention in
prepare as immutable INPUT (`request.before.state_path` canonical LIVE, COPY
separate, HIGH binds CURRENT, LOW detached uses COPY mapping, no canonical
rewrite, adopt reverifies); guard fixed canonical path, transient coordination,
phase derived, reopen via nonce+hashes, completion `R/completion/cleanup-completion.json`
before release, operational readiness guard-absent + completion; IO lstat/safeFD/
exclusive/`fsync`/checked-close/replace/dirfsync, no `write_json` equivalence,
temp-E not adopted, unknown never rewritten; HEAD/tree exact predicate + finite
diff-set + no gitlinks + head-change recompute; DM016 exact types (no aliases,
10 absent Thematic OPEN) + DM017 7-field union (dimension/description from OLD
valid completeness) + witnesses + N1–N12; oracles O-W1/T1/W2/T2/R1/G1-3 + failure
F1–F13 (COPY-derived expectedAfter rule per §3). Full predicates/tables in R3
§§4–11 + R4 JSON rows/guard/head_tree/failure_table (authoritative deltas above
override where conflict).

## 6. Residual + stop (honest, no PASS)

B1–B5 concrete blockers closed per §§1–4 + R4 JSON/schemas. No MAP-COMPLETE/GO,
no independent PASS, no implementation authorization. Root + independent review
before code. Per-invocation values open (expected_head/tree, contract/tool SHAs,
Profile/source pins, before bytes, 7-slot observations, affected_ids,
obligations, Raw/HTML provenance, mechanical SHAs, executor/recorded_at).
Any extra DIRECT reader not in 40 rows = precise OPEN blocker.
Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN preserved.
Stop internal; ordinary Commit/Push Human-owned. Selected decision hash `a345`
unmodified; prior reports/source unmodified.

### Preservation + citations

R3 + schema-proposals preserved exact (reviewed B1–B5 history); R1/R2 preserved;
review §§0–5 preserved. Source-grounded: `survey_versioned_renewal_history_v2.py:
81-260/290-365/1275-1420` (OLD67/NEW71/OLD50/NEW63/adapter semantics),
`survey_weekly_derivation_v2.py:28-58/585/836`,
`survey_longform_generated_v2.py:52-87/1020/1157/1198/983`,
`survey_evidence_v2.py:719/839/965/1152/1216/1255/1286/1322/1437/1494/1658/1725`,
`survey_completeness_v2.py:25-35/213-236/265-290`,
`run_evidence_v2_interactive.py:38-45/119-214/471-507`,
`survey_agent_control_v2.py:42/348/365/481/761/902/1608/1703/1768`,
`survey_publication_set_v2.py:56/2181`, `config/survey-production-v2.json`
pipeline71, `schemas/{materiality-ledger,profile-completeness-result,
candidate-matrix-v2,candidate-selection-v2,stage-checkpoint-v2}.schema.json`
`$id`s, `survey_execution_record_v2.py:82/284`,
`survey_reader_publication_v2.py:171`.

(End of file)
