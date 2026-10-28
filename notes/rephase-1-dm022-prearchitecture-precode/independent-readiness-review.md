# DM022 pre-Architecture — independent pre-code readiness review (NOT author)

2026-10-27. Fresh independent reviewer, not author. Read-only source/map inspection only.
No runtime/import/tests/build/fixture/restore/network/Git mutation/source edits.
No candidate/reconstruct Commit/Push. Internal review endpoint, not Human Commit Point.

## 0. Inputs and method

Read:

- Selected contract `outputs/rephase-1-dm022-prearchitecture-contract-decision.md` including §11,
  SHA256 `a345bb9524b4dfc5b5f32600d0d708687e2b6131d91a43965c97b6418388f223` / 31351B.
- Mandatory `notes/rephase-1-dm022-prearchitecture-contract/astra-review-resolution.md` including §5,
  plus BOTH independent design reviews WITH FINAL-BINDING addenda (selection only, B2/B4 pre-code OPEN).
- Packet `notes/rephase-1-dm022-prearchitecture-contract/README.md`.
- R2 maps (author-side, binding for review, not approval):
  `notes/rephase-1-dm022-prearchitecture-precode/authority-consumer-map-r2.md` (A, 30-row table),
  `inventory-r2.json` (29 rows), `schemas-generation-dag-r2.md` + `.json` (B, 5 required +1 optional),
  `guard-resume-oracles-r2.md` + `.json` (C, guard/IO/HEAD-tree/oracles),
  `dependency-closure-map.md` + `.json` (closure supplement, author-side).
- R1 preserved as history/rejected where overridden:
  `authority-consumer-map.md`, `inventory.json` (28 rows),
  `schemas-generation-dag.md`/`.json`, `guard-resume-oracles.md`/`.json`.
- Actual source read-only: `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`
  = actual `409b292`/tree `8ce36998` +93/742. All `file:line` below are proof-copy unless stated `workspace:`.
  Spot re-reads only; full93/742 not recertified here (carryover §8 scope retained).

Method: `Read` + `Grep` (via python stdlib, no `scripts.*` imports) + `ast` parse as DATA.
Verified cited `file:line` bytes exist and match claimed semantics; did not execute producers,
did not infer constructibility from selection.

## 1. Verdict

**NOT_READY. Pre-code map not closed. Implementation blocked. No GO, no conditional
deferral of required map to implementation.**

Contract selection (including §11) remains bounded and coherent per FINAL-BINDING reviews;
selection does not prove constructibility. This review covers readiness only.
Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN preserved.

Required map per decision §10 + root §5 is not yet closed. Exact blockers in §3.
R2 repairs 10 root findings on substance (basis path, State-bound reuse, PATHS-only LOW,
report/checkpoint cycle, split prepare/adopt, typed refs, literal digests, changed-package
mechanics, DM017 union, no new role) but leaves literal schema text, per-caller exact
signatures for hardcoded readers, single-resolver scope, forward-builder rows, guard
derivation for no-State callers, schema-owner branch text, and HEAD/tree complete-set
scope open. R2's own §15 + closure §7 admit B2/B4/audit/HEAD-tree/C-IO remain OPEN;
this review confirms they are not waivable as “review later”.

## 2. What was verified CLOSED (source-grounded, no approval)

- **Four-ref same-record triplet while lifecycle/history unchanged, later readback.**
  Decision §5 + §11.2 + root R3. Source: `survey_agent_control_v2.py:902-938`
  same-authority + View→Evidence SHA, `_resolve_checkpoint_artifact:761-899`
  exact-one + live re-hash, `advance_with_checkpoint:1778-1781` same-authority-to-all-stages,
  `validate_agent_state:678-700` + `core.validate_state_semantics:760-780` fixed forward history.
  R2 A §§3/6 kind dispatch (legacy no-kind vs PREARCH kind/reason/operation/producer_boundary,
  mixed-triplet refuse, no `.get` fallback, no canonical fallback after adoption) matches source
  necessity (`_producer_for_checkpoint:348` returns NONE for `EVIDENCE→EVIDENCE`,
  `stage-checkpoint-v2.schema.json:200-208` only `CANDIDATES_NORMALIZED` covers 4 names).
  Later readback rule (creation restricted to `EVIDENCE_REVIEWED`, adopted readback valid
  through forward lifecycles via retained COPY/lineage, no live-before equality) is stated
  correctly; detached proof State-nonrecursive + eligibility HIGH-side preserved.

- **Report/checkpoint SHA acyclicity, proposed-before-decision, package basis.**
  R2 B §§2-3/6/9/13 + C §§6-8: prepare (no decision) → external D binds M → adopt validates
  D + seals + proof P + report RPT (NO checkpoint/afterState/guard-hash) → checkpoint CP binds
  completed RPT → State triplet → optional POST receipt (CP never backrefs). No self/future SHA.
  `package.basis.state_path` ALWAYS canonical LIVE path (`survey_evidence_v2.py:640-652`
  `_rel(repo_root,state_path)`), `state_sha256` = exact before bytes; retained COPY separate
  same-bytes map entry; `_validate_evidence_package_basis_content:839-895` enforces
  `basis.state_path == canonical_state_path` with no live SHA equality. R1 COPY-rebinding
  and “unchanged callsite-only” reuse correctly withdrawn; narrow `_content` cores verified
  State-free via `ast` (e.g. `_validate_materiality_ledger_content` only calls
  `_check_*_content` + screening content, no `verify_state_basis`/`repository_commit_sha`).

- **LOW path-based predicates, no State/current-helper recursion.**
  R2 A §10 + B §4 + closure §3: LOW top only `core(shape-only)` + `schema_gate`,
  all `evidence/screening/completeness/discovery/agent` function-local; leaf funcs verified
  pure (`validate_evidence_card`, `validate_edition_view`, `task_authority_sources`,
  `_validate_obligation_shape` call only pure helpers; top imports
  `evidence→screening→core` only, `screening→agent` function-local `:465,480`).
  HIGH-only LIVE `agent.validate_agent_state:597` + canonical Profile/source/issue/
  initialization (`_profile_and_source:307`) + window predicates correctly separated;
  `production.verify_state_basis:959` never substituted (globally current-pinned vs
  resumable agent path).

- **HIGH full LIVE validity, canonical window.**
  `validate_agent_state:602-748` already checks Profile/source/issue/initialization,
  lifecycle, checkpoints/provenance, history, gates, exception, publication revalidation.
  R2 A §2 HIGH `verify_live_eligibility` adds §3 window (passed Evidence/Materiality/
  Completeness, pending Selection/Architecture/Draft/validation/preview/Freeze/Release,
  null Human provenance, no review-index/presentation, inactive Exception, null
  revalidation pointer, same issue/Profile/Discovery/Screening, allowlist nonempty/unique/
  subset non-DROP, no new Discovery/changed Screening). Window list matches decision §3;
  exact allowlist source (Screening decisions + ledger rows) is stated in B §11 but needs
  per-witness values (see F8).

- **Shared cores exact, mechanical projections actual.**
  R2 B §4.1 narrow cores all exist with cited lines; §10 ledger basis exactly 7 SHAs
  (`materiality-ledger.schema.json` basis required 7, no `self_digest`),
  package/card/view bases match `evidence-v2-run-package/card` + `edition-evidence-view`
  required fields. Card `basis.task_sha256` change ⇒ card bytes change; unchanged cardSHA
  held only if all basis + semantic fields equal (FILE SHA check). Ledger/completeness
  basis exclusions limited to recomputed evidence/view/digest SHAs. No directory-prefix
  exclusion. Source-grounded.

- **Named-obligation completeness safe.**
  `survey_completeness_v2.py:25-35` `OBLIGATION_KEYS` 7 fields, `:213-236` requires
  Profile-initial + every Discovery-named `obligation_ids` with traceability;
  `run_evidence_v2_interactive._build_completeness:471-507` iterates initial-only.
  R2 B §11 union builder (ID set = initial ∪ Discovery-named, `discovery_ids` = declaring
  DIDs, `evidence_task_ids` via ledger, `dimension/description` verified vs old valid
  completeness, unchanged full validator) matches decision §8. No invention from Profile.

- **Guard filesystem invariants.**
  R2 C §§2/5: `lstat` once per slot (`ENOENT`=absent, symlink/FIFO/socket/dir/nonregular/
  `EACCES`=refuse, never `is_file`/`exists` for absence), `O_RDONLY|O_NOFOLLOW` +
  `fstat` verify, `O_CREAT|O_EXCL|0600` tmp + short-write loop + `fsync(file)` + checked
  `close()` + `fsync(dir)` + `replace` + `fsync(dir)` + postread; `core.write_json:150`
  (`mkdir+write_bytes`, no fsync/atomic/existence) correctly revoked for guard/State/slot
  authority; `shutil.copy2` correctly revoked (no exclusive guarantee). Temp-E ≠ adopted
  (ONLY canonical LIVE `production-state.json` disposition counts), never rewrite unknown
  LIVE to B/E, held-FD not persisted across restart (reopen via `lstat`+hash+nonce vs
  retained intent), COPY backup verified before unlink, new inode even on equal bytes
  refuses (F9). Planned-CP-bytes deterministic before guard claim (guard binds
  `planned_checkpoint_ref.sha` + `expected_after_sha` computed in-memory; checkpoint has
  NO `guardRef`/`afterStateSHA`). No mutable `phase` in guard hash, no `SELF` cycle.

## 3. Blocking findings (exact location, root clause, smallest repair)

Severity HIGH = code blocked until repaired. MEDIUM = must be clarified + Astra-confirmed
before code; do not waive.

- **F1 HIGH — bare `records` schema.** `schemas-generation-dag-r2.md:236`
  `"records": {"type": "array", "minItems": 1, "items": {"type": "object"}}`.
  Violates decision §10 (exact interface/schema) + root §5 (exact schema branch fields).
  Task bar: no bare `object`/ellipses. Repair: expand to literal COMMON/WEEKLY/THEMATIC
  shapes from `run_evidence_v2_interactive._validate_record:119-214`
  (`source_bindings` iff multi-source, per-Profile fields) or `$ref` existing schemas;
  no generic object.

- **F2 HIGH — only request has literal JSON; 4 required +1 optional lack it.**
  `schemas-generation-dag-r2.md:§§9.4-9.8` give prose required lists for
  manifest/proof/pre-adoption-report/checkpoint/completion-receipt, not literal
  `{"$schema","$id","type":"object","additionalProperties":false,"required":[...],
  "properties":{...},"$defs":{...}}` as done for request §9.3. Decision §§5/10 +
  §11.3 + root §5 require actual checkpoint-schema branch field names/digest exprs.
  Repair: provide literal JSON for each of 5+1 files (repeat `$defs` literally,
  `additionalProperties:false` throughout, `if/then/contains` for
  `checkpoints==[evidence,materiality,completeness]`, `artifacts` 4 `NamedRef`,
  `reviews` sole `DM022_SUPERSESSION_PROOF`, `contract` literal 8-field,
  `implementation` literal 2-field, digests `*_sha256==sha256_object(body-minus-self)`).

- **F3 HIGH — hardcoded canonical reader has no exact new signature.**
  Proof-copy `survey_drafting_v2.py:102-211` `_historical_raw_authority_hashes`
  hardcodes `source_root/"candidate-matrix-v2.json"` (`:130`) +
  `source_root/"evidence/v2/accepted"` (`:131-134`), `is_file`/`is_dir` compat,
  raw SHA + parsed equality. R2 A row9 (`authority-consumer-map-r2.md:123`)
  says “MUST accept versioned R4 Evidence/Matrix refs” but gives no new params
  (“Exact helper change scoped here”). Decision §11.2 requires each affected caller
  resolve new refs or explicitly refuse. Repair: give exact new signature
  (e.g. add `evidence_ref: NamedRef, matrix_ref: NamedRef` or State-bound R4 resolver
  call + `require_no_active_guard` location) and state which entry
  (`run_drafting_synthesis_v2_interactive.main:150` via `_upstream:43`) supplies R4;
  pure function cannot stay “UNCHANGED pure, callers pass R4 paths” when paths are
  hardcoded.

- **F4 HIGH — single-resolver overclaim for research refs.**
  `authority-consumer-map-r2.md:140` row20 + `dependency-closure-map.md:83-84,195,211`
  claim `survey_publication_set_v2.resolve_stage_artifact_path:2181` single-resolver
  change covers all `_l_stage_path` adapters (`production._l_stage:47`,
  `stage_validation._l_stage:99`, `human_gate.resolve_gate_path:255`,
  `orchestrator.resolve_configured:167`) for PREARCH research 4 refs.
  Source: `:2181-2230` resolves stage templates via profile expansion only (special-case
  `publication-candidate`); research Ledger/Matrix/Selection resolve via
  `agent.resolve_*`, handlers, derivation, not via this function. Decision §11.2
  requires new active research resolver + per-caller rewiring. Repair: split into
  (a) stage-template adapter inheritance (true, keep) and (b) research four-ref
  per-caller R4-or-refuse rows (cannot inherit); correct closure text that says
  “all adapters inherit, no per-adapter fork”.

- **F5 HIGH — forward builders have no dedicated rows.**
  R1 `inventory.json` rows `agent.build_stage_checkpoint:1703`,
  `agent.advance_with_checkpoint:1768` dropped in `inventory-r2.json` (no 1703/1768 keys).
  R2 A only references them via orchestrator/bridge refusal
  (`authority-consumer-map-r2.md:98,100`). Decision §5 (new builder separate, never
  `advance_with_checkpoint` with fabricated State) + §6 completeness bar (every
  guard-requiring writer enumerated) require explicit dispositions.
  Proof-copy `agent.build_stage_checkpoint:1703-1765` + `advance:1768-1826`
  are public entry points callable directly, not only via orchestrator/bridge.
  Repair: restore two rows: `build_stage_checkpoint:1703` UNTOUCHED + new PREARCH
  builder separate (no synthetic `from/to`); `advance_with_checkpoint:1768`
  REFUSE PREARCH kind (producer NONE for `EVIDENCE→EVIDENCE`) with guard check
  location + oracle, not caller-only refuse.

- **F6 MEDIUM — count/bundling misstatements.**
  A says 30 rows (`authority-consumer-map-r2.md:114-147`) but `inventory-r2.json`
  has 29 rows (verified via stdlib json: 29). Row3 bundles
  `_validate_checkpoint_record:481` + `_validate_core_stage_report:365` under single
  `line:481` entry; row5 `resolve_effective_discovery_basis/_content:353/809`
  has no json row. `dependency-closure-map.md:41-42,201` D4 + `:201` “30 rows per
  `inventory-r2.json`” misstates json content (json has 29, no separate 365 row).
  Decision §10 requires complete caller inventory proof. Repair: align json to md
  (add missing screening-effective pure-helper row or document exclusion as
  non-four-ref helper; split 481/365 or note bundling explicitly) and correct D4 +
  `:201` count to 29 json vs 30 md with bundling note. Not a semantic gap if
  clarified, but machine inventory must match prose.

- **F7 HIGH — no-State-arg guard derivation per caller missing.**
  `guard-resume-oracles-r2.md:§4` FIXED `require_no_active_guard(source_root: Path)`
  (no owner/skip, any present/malformed/unknown → `DM022_TRANSITION_ACTIVE`) is correct,
  but §4.2 pattern “derive via validated Profile or ref-graph before any canonical
  output, else refuse” gives no per-caller exact derivation for handoff-dict/
  artifact-map callers without `state_path` (e.g. `survey_handlers_v2._evidence_basis:204`,
  `survey_stage_validation_v2._evidence_basis:402`, pure writers §7).
  R2 A rows say “facade validates State first then private structural” for State-dict
  callers (good) and “caller G” for pure callers, but do not state Profile path source
  per handoff (handoff dicts carry no `profile.path`). Decision §§6/10 + §11.1
  (every producer/advance/Gate checked at entry + before-publish, no unguarded normal
  writer). Repair: for each no-`state_path` mutating path give exact
  `repo_root→cfg→Profile→source_root→guard_path` derivation with `file:line` +
  oracle, or explicit `refuse in superseded mode` with kind-check location;
  pattern alone is not closure.

- **F8 HIGH — schema-owner branch text still OPEN (admitted).**
  R2 B §15 + `dependency-closure-map.md:204-206,216` + `.json:plan_diff_register_matrix`
  admit OPEN: strict `stage-checkpoint-v2.schema.json` branch for
  `EVIDENCE→EVIDENCE` + `producer_boundary` + same-triplet + new-report
  (no `CORE_STAGE_CONTRACT` forgery), `check_id DM022_SUPERSESSION_PROOF`,
  `contract_identity`/`repository_commit_sha` pin placement; pipeline 71→76(77)
  registration is root decision. Decision §§5/10 + §11.2-11.3 + root §5 make this
  required pre-code, not implementation scope. Repair: provide literal branch JSON
  (old file UNCHANGED per closure choice §2: standalone new
  `dm022-supersession-checkpoint-v2.schema.json` + shared
  `LOW.load_typed_checkpoint_record` dispatch; list all 17 direct schema sites
  `agent:42,489,819,1011,1532,1758,1774,1971,2397`, `pubset:56,1213,1627,1981`,
  `editorial_correction:557`, `release:121`, `stage_validation:288`,
  `weekly_refresh:931` migration to shared loader) + registration decision.
  Closure loader choice itself is coherent (old `required from_state/to_state` +
  `additionalProperties:false` cannot host new `operation/producer_boundary` without
  weakening; standalone + dispatch avoids `oneOf` duplication).

- **F9 MEDIUM — HEAD/tree complete-set scope ambiguous.**
  `guard-resume-oracles-r2.md:§9` pins commands (`rev-parse HEAD`, `HEAD^{tree}`,
  `status --porcelain=v1 --untracked-files=no`, `diff --raw HEAD`,
  `--ignore-submodules` `none` for eligibility vs `all` scoped carryover only),
  `control_roots [config,schemas,scripts,.github/workflows]`, no `R/**` wildcard,
  no gitlink eligibility, artifact-only descendant `diff-tree --name-only` ⊆ finite
  declared R output/review/retention relpaths + linear descendant + pins/controls
  identical. Decision §7 requires phase HEAD/tree predicate + complete path set +
  artifact-only descendant admissibility. Open: does eligibility require full HEAD
  equality or only control-roots + contract/tool SHAs? Full HEAD would make
  docs/template drift block DM022; roots-only leaves non-root drift unaddressed.
  Repair: state exact predicate (e.g. `expected_head == LIVE HEAD` AND
  `expected_tree == LIVE tree` AND `contract_identity` + `tool_shas` + Profile/source/
  proof pins equal, with `status --porcelain` clean for control roots; docs drift =
  refuse vs allow) + finite complete path set list per witness (request
  `expected_head/tree/contract/tool_shas/profile/source_pins`, guard `work{head,tree}`,
  pin sets B + 4 artifacts + 7 slots) with no broad `R/` prefix exception.

Additional non-blocking notes (no repair required before readiness, record only):

- 30 vs 29 is bundling (F6), not missing four-ref coverage, once clarified.
- Dropped R1 Profile rows (`SOURCE_CLASS_MAP:38/44`, `_build_completeness:471`,
  `completeness_extra:145`, `build_ledger:1579`) are covered as Profile predicates
  (B §§10-11, DM016/017) not B2 rows; trace explicitly in readiness return.
- `reader_publication` + `weekly_mechanical_refresh` canonical refs are stage/
  publication-surface, not research four-ref; covered via C §4 row12 walker
  recognition-or-refuse + publication_set single-resolver for stage paths, but
  research cutover for those walkers must still be listed per F4 split.
- New 2-module +5+1-schema budget is justified (merging manifest↔proof forces future
  ref; proof↔report forces self-digest cycle; report↔checkpoint recreates Finding-4
  cycle; R2 B §9.8 + closure D2 correctly refuse embedded guard defs). No arbitrary
  budget imposed; if implementation needs more, return to root (closure D3).

## 4. Scope limits

Independent readiness only. No full audit, no adoption claims, no Production acceptance.
No re-verification of final93 patch beyond cited spot reads; prior renewal/contract
evidence bounds retained. Current contract selection (including §11) does not prove
constructibility; this NOT_READY does not contradict DESIGN_BOUNDED_PASS for selection.
Task endpoint is internal review; not Human Commit Point; ordinary Commit/Push Human-owned.

---

## 5. R3 re-review (2026-10-27, fresh independent, preserves §§0–4 NOT_READY)

Read actual R3 beyond ROOT paraphrase (§§1–13, not only §§0/27 header):

- `notes/rephase-1-dm022-prearchitecture-precode/integrated-readiness-r3.md` 1225 lines,
  SHA256 `412b8918c9a9c698a772e24af2171a0fe42221c76f3f691b8aee9c32727d397e` / 88341B.
- `integrated-readiness-r3.json` SHA256 `f6a73d6f2e314c0e277fa4709dcf191653d02f4de11a164d0ceb2cefe9009df5` / 32067B,
  36 rows, 5 schemas, 17 sites + 8 branches, closures, F1–F9 closure claims.
- `schema-proposals/` 5 literal JSON: request `a99f0dc1f6e10ae5` / 18648B,
  manifest `e7534d019ec1b5` / 8773B, proof `4130dfb07cd05b3` / 4558B,
  report `6a436d0d828fcb3` / 12292B, checkpoint `fd39c246617293e` / 7259B.
- Proof-copy final93 readonly, no runtime/import/tests/build/Git/network.
  R1/R2 preserved as NOT_READY history; this §5 appends only, edits no root/author files.

Method: stdlib `json` parse as DATA (no `scripts.*` imports), `ast` leaf checks,
`file:line` byte re-reads. Verified R3 literal text, not paraphrase.

### 5.1 Verdict (R3)

**NOT_READY. Implementation blocked. No GO, no conditional defer to code.**

R3 closes substance of F1 (records literal), F3–F6 (exact hardcoded-reader signature,
stage/research split, forward-builder rows, 36-row unbundling), loader 17+8 enumeration,
HEAD/tree predicate and snapshot/planned-SHA ordering. It does NOT close:
ownership consistency, literal registry validity, per-entry guard+completion,
historian/pipeline/closure compatibility (BIG), successor full memberships.
R3 §13 itself claims no MAP-COMPLETE/GO and lists Astra + independent confirmation
as blockers; this review confirms additional precise blockers below.
Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN preserved.

### 5.2 What R3 verifiably repairs (source-grounded, no approval)

- F1: `dm022-revision-request-v2.schema.json` `$defs.weeklyRecord/thematicRecord/
  interactiveRecord` + `entity/claim/verificationItem` literal, enums match
  `run_evidence_v2_interactive.py:47-65` (`ENTITY_TYPES`, `ARTIFACT_TYPES`,
  `EVIDENCE_CLASSES`, `CARD_STATUS`, `VERIFY_STATUS`, `MATERIALITY`,
  `LINEAGE_ROLES`, `WEEKLY_WINDOW_RELATIONS`), `COMMON:66-70` + `THEMATIC:71-74` +
  `WEEKLY:75` + `RETROSPECTIVE:79` empty (RETROSPECTIVE correctly not admitted),
  `allOf` REJECTED→NON_MATERIAL / NEEDS_MORE→HOLD mirrors `_validate_record:119-214`.
  No bare `object`.
- F3/F4/F5: exact `_historical_raw_authority_hashes(repo_root, evidence_ref,
  matrix_ref)` (§11) + entry `main:150` via `_upstream:43`; stage-template vs
  research split (`pubset.resolve_stage_artifact_path:2181:2218-2230` only stage
  templates, research via `agent.resolve_*`/handlers/derivation); restored
  `build_stage_checkpoint:1703` UNTOUCHED + `advance_with_checkpoint:1768` REFUSE.
- Loader: all 17 direct `CHECKPOINT_SCHEMA` sites re-read present
  (`agent:42,489,819,1011,1532,1758,1774,1971,2397`, `pubset:56,1213,1627,1981`,
  `editorial_correction:557`, `release:121`, `stage_validation:288`,
  `weekly_refresh:931`); 8 branches (`:348,365,481,761,902,1608,1703,1768`) exist.
  Standalone new checkpoint + shared `LOW.load_typed_checkpoint_record`
  (strict kind dispatch, no `.get(kind,legacy)` fallback, no raw mutation) avoids
  old-file weakening (old requires `from_state/to_state` + `additionalProperties:false`).
  `producer_boundary` separate, no `CANDIDATES→EVIDENCE` forgery.
- Snapshot/prepare ordering: immutable before-State + 7-slot COPY captured in prepare
  as inert INPUT (no canonical/State/guard mutation, new owned R only), later adopt
  REVERIFIES unchanged retention before guard claim, never rewrites retention.
  Consistent with decision §6 + R2 staging clarification; no prior-authority mutation.
- Planned-SHA determinism: `M←D←P←RPT←CP→State→POST` one-way; proof NO checkpoint,
  report NO `checkpoint`/`expectedAfterState`/guard-hash
  (`additionalProperties:false` enforces; `guard_claimed` bool + `guard_path` string
  descriptive only), checkpoint NO `guardRef`/`afterStateSHA`/completion backref,
  `*_sha256==sha256_object(body-minus-self)` + `sha256_file` distinct. Planned bytes
  deterministic in-memory before guard, saved `R/checkpoint.planned.json/.sha256`
  iff explicit `planned_checkpoint_ref`, verified `FILE sha==planned==guard.sha`
  before State replace, reconstruct-or-fail-closed on drift. No future/self cycle.
- HEAD/tree: exact commands (`rev-parse HEAD`, `HEAD^{tree}`,
  `status --porcelain=v1 --untracked-files=no`, `diff --raw HEAD`),
  `--ignore-submodules none` for eligibility vs `all` scoped carryover only,
  no child gitlink eligibility, no `R/**` wildcard, finite declared
  `diff-tree --name-only` subset + linear descendant + no merge + pins/controls
  identical, head-change recompute rule. Scope now explicit (docs drift = refuse,
  non-control drift recorded as untracked selective paths).

### 5.3 Remaining blockers (exact location, root clause, smallest repair)

Severity HIGH = code blocked. Preserve R1/R2 F1–F9 history; these are R3-new or
R3-incomplete.

- **R3-B1 HIGH — LOW ownership inconsistent (header vs signatures).**
  `integrated-readiness-r3.md:130-146` header: LOW read-only, never imports agent,
  never reads guard, `FORBIDDEN LOW→guard` (`:171`); signatures `:223-225` place
  `guard_path_for`, `require_no_active_guard`, `lstat_slot` in LOW and `:213-219`
  builders return `Path` + write (`build_..._from_paths→Path`,
  `accept_...→tuple[Path,Path]`, `prove_...→Path`) despite “read-only path entries +
  pure content builders”. Decision §10 + §6 (sole HIGH mutator while bound guard
  exists, LOW detached/history proof State-nonrecursive). Repair: restate ownership
  explicitly — LOW owns passive `lstat`-only absence check (`guard_path_for` pure join
  + `require_no_active_guard` lstat/absent-pass else `DM022_TRANSITION_ACTIVE`, no State,
  no `agent.validate`, no FD/lease) which HIGH normal writers import as passive IO
  (`HIGH→LOW` allowed, no recursion because LOW guard never calls agent/State);
  LOW prepare-phase writes to NEW owned R are inert preparation (no canonical/State/
  guard mutation, no old-authority), HIGH owns all guarded mutation
  (`claim_guard`/`write_checkpoint_as_planned`/`replace_state_triplet`/
  `clear_remaining_exact_slots`/`write_cleanup_completion`/`release_guard` exclusive
  `O_CREAT|O_EXCL`/short-write/`fsync`/checked-close/`replace`/`dirfsync`/postread,
  never `core.write_json`/`copy2`/`is_file`). Change header “never reads guard” to
  “never claims/releases guard, only passive absence check”; change “read-only” to
  “no canonical/State/guard mutation; prepare inert writes to NEW R only”.

- **R3-B2 HIGH — literal registry dangles + $id mismatches.**
  `schema-proposals/dm022-preadoption-report-v2.schema.json:$defs.roleSchemaRegistry`
  consts `evidence-acceptance → .../dm022-revision-proof-v2.schema.json#/$defs/
  proposedEvidence` and `edition-views-acceptance → ...#/$defs/proposedViews`, but
  `dm022-revision-proof-v2.schema.json:$defs` has only
  `sha256/gitsha/safePath/ArtifactRef/SizedRef/NamedRef/mechanicalProjection` —
  no `proposedEvidence`/`proposedViews` (verified via stdlib json). Dangling `$ref`.
  `materiality-ledger → github/.../materiality-ledger.schema.json` matches actual
  `$id` (github), but `candidate-matrix → github/.../candidate-matrix-v2.schema.json`
  mismatches actual `$id` `https://example.invalid/schemas/candidate-matrix-v2.schema.json`
  (proof-copy `schemas/candidate-matrix-v2.schema.json:$id`), same for
  `candidate-selection` (github vs actual `example.invalid`). Decision §5/§10 +
  root §5 (exact schema branch, no untyped objects). Repair: add missing
  `proposedEvidence`/`proposedViews` defs to proof schema or retarget registry consts
  to existing defs/actual files; correct `candidate-matrix`/`candidate-selection`
  consts to actual `$id`s (`example.invalid/...`) or actual github `$id`s if
  intended; re-validate all `$ref`s resolve locally, no remote fetch, no cross-file cycle.

- **R3-B3 HIGH — guard+completion not per mutating entry (incl no-State CLIs).**
  Decision §6 + §11.2 + root 6: normal writers with active PREARCH kind MUST require
  BOTH `require_no_active_guard` passes (guard ABSENT) AND `require_completion_consistent`
  verifies (checkpoint SHA + `expected_after` + `seven_plan`). R3 §6 states predicate,
  but `integrated-readiness-r3.json` 36 rows: only row 20 (`approve_architecture:1829`)
  lists `+ C`; rows 7 (`run_selection:158`), 9 (`_upstream:43`), 24
  (`semantic_publication:118`), 26 (`editorial_publication:749`), etc. list `G` only.
  No-State CLIs: row 34 covers `reader_surface_gate:1152` only as `G where mutating`;
  `execution_record:82/284`, `reader_publication:171`, Weekly/Longform receipt
  validators mentioned in §7 text (`:707-711` “MUST require State post-adoption”)
  have no dedicated rows in 36-row json. Later forward `no before-State equality`
  is stated in §11 but not bound per walker row. Repair: add `+ C` with
  `require_completion_consistent(source_root, checkpoint_ref)` location (entry +
  before-publish) to every mutating row that can run with active kind after release
  (7,8,9,12,13,15,16,17,19,20,24,26,27,30,31,33,34), and add missing rows for
  `execution_record`, `reader_publication`, receipt validators (or explicit
  refuse-in-superseded-mode with kind-check location); each oracle must state
  `entry + seam none + writes none` on refuse and `guard ABSENT + completion verified`
  on proceed, with late-State-forward `expected_after` baseline (not LIVE equality).

- **R3-B4 HIGH (BIG) — pipeline/closure historian bricking: OLD67/NEW71 vs NEW-DM76
  + OLD50/NEW63 vs 70/73 + CURRENT 29/34/63 vs 36/41 undefined.**
  Proof-copy `survey_versioned_renewal_history_v2.py:81-260` pins exact
  `OLD67` (67 paths) vs `NEW71 = OLD67 + 4 new schemas` (`_NEW_SCHEMAS_4`,
  `:350-360`); `_recompute_contract8_at_epoch:169-260` refuses unknown pipeline
  (`UNSUPPORTED_MIGRATION` unless exactly OLD67 or NEW71); `_derive_tool_generation:
  1304-1411` derives OLD vs NEW only on those sets (partial/new-files-with-OLD67
  → REJECT/UNKNOWN); `_expected_staged_code_deps:1277-1303` enforces exact
  `OLD50` vs `NEW63` (`_OLD_PY_30` + `_OLD_SCHEMAS_14` + family/new sets); CURRENT
  closures exact (`survey_weekly_derivation_v2:CURRENT_CLOSURE` 29 lines `:28-58`,
  `survey_longform_generated_v2:CURRENT_CLOSURE` 34 lines `:52-87`,
  `survey_versioned_renewal_source_v2:1414-1540` recomputes CURRENT 63/66 member-wise
  vs proof). R3 §9 proposes pipeline `71→76` (+5 schemas), P3S per-route `63→70`,
  union `66→73`, Weekly `29→36`, Longform `34→41` as counts + “old list +7” rule
  (`integrated-readiness-r3.json:closures_successor_proposed`), but gives no literal
  NEW76 pipeline list, no updated `_OLD_PIPELINE_67`/`_NEW_SCHEMAS_4`/`_derive_tool_
  generation` branches, no `OLD67/NEW71 vs NEW-DM76` current/historical support rule,
  no `OLD50/NEW63 vs 70` staged rule, no CURRENT 36/41 member lists. A DM22 epoch with
  76-pipeline/70-closure files will hit `UNSUPPORTED_MIGRATION`/`HISTORY_DIGEST_MISMATCH`
  in later editorial/renewal walkers that Decision §11.2 REQUIRES to recognize PREARCH.
  Row “MUST recognize PREARCH kind/digest and full E graph” (`integrated-readiness-r3.md:
  1042-1064`, rows 27–31) is insufficient without generation/pipeline/closure
  compatibility. Using post-VALIDATED renewal to authorize upstream changes or
  automatic `old71→76` Core migration is not selected (decision §2/§9). Repair:
  define exact families — e.g. `OLD67` (pre-renewal), `NEW71` (renewal, 67+4),
  `NEW-DM76` (DM22, 71+5) — with literal pipeline/closure memberships (not counts),
  state current-source support (DM76 CURRENT requires 76-pipeline + 2 modules +5 schemas
  + PREARCH kind/digest + full E graph) vs historical support (OLD67 historical,
  NEW71 historical, NEW-DM76 historical via retained COPY/lineage + `supersedes`/
  parent/anchor + SELF/digest, no live-before equality), distinguish
  (a) initial-after-DM22 `current76` readback + future76 same-contract forward
  (pins/controls identical, no migration) vs (b) old71 historical records (detached
  validation via retained bytes, `historical_state`, never live equality) and state
  that `old71→76` automatic migration is NOT selected (new bounded attempt if pins/
  controls drift). Update or explicitly scope `_derive_tool_generation`,
  `_recompute_contract8_at_epoch`, `_expected_staged_code_deps`,
  `verify_renewal_source` CURRENT checks and `CURRENT_CLOSURE` tuples (or prove
  walkers bypass them via retained SOURCE lineage with exact code paths); list full
  successor memberships verbatim in json (not “old +7”). If map cannot preserve
  invariants without weakening, return exact blocker and revisit A1 vs A2
  (decision §9/§11.4), never partially guarded A1.

- **R3-B5 MEDIUM — successor full memberships not verbatim.**
  `integrated-readiness-r3.json:closures_successor_proposed` gives counts
  (`p3s_per_route_70`, `weekly_36`, `longform_41`, `pipeline_76`) + rule “old list +7”,
  referencing `dependency-closure-map.json` old verbatim lists, but no literal NEW76
  pipeline list (71 paths), no literal NEW70/73/36/41 lists. Task ROOT 9 requires full
  proposed lists actual callgraph + file-pin ONLY HIGH, not just add counts.
  Repair: append literal successor lists (sorted relpaths) for pipeline76, P3S 70/73,
  Weekly36, Longform41, staged 50/63 vs 70 (or state staged unchanged with reason),
  with `control_roots` unchanged justification and `contract_identity` recompute note.

### 5.4 Scope

Independent readiness only. Preserves §§0–4 NOT_READY and R3 as author map (no approval).
No runtime/import/tests/build/Git/network, no root/author edits, no full audit/adoption.
Current selection (incl §11) does not prove constructibility. Internal endpoint, not
Human Commit Point; ordinary Commit/Push Human-owned. Bound R3 hashes in §5 header.

---

## 6. R4 re-review (2026-10-28, fresh independent, preserves §§0–5 NOT_READY)

Read actual R4 (not ROOT choice paraphrase):

- `integrated-readiness-r4.md` 323 lines,
  SHA256 `7b6131327355ecb6f3ab5c85ea4d5e2b501af2a3c86b97c2f288568f2161d578` / 20102B.
- `integrated-readiness-r4.json` SHA256 `9ae6a8ce153287b26de637053df77d9e2aab264e3d3b28ea2597cd9db2213625` / 96518B,
  40 rows, 17 sites + 8 branches, 5 schemas, families G67/G71/G76 literal.
- `schema-proposals-r4/` 5 literal JSON: request `a99f0dc1f6e10ae5` / 18648B (unchanged
  from R3), manifest `e7534d019ec1b5` / 8773B (unchanged), proof `a79c09209c145d48` /
  7403B (R3 4558B + `evidenceAcceptance`/`viewsAcceptance`), report `213696081794d98` /
  14745B (R3 12292B + registry retarget), checkpoint `fd39c246617293e` / 7259B (unchanged).
- Proof-copy actual `409b292`/tree `8ce36998` +93/742 readonly; Human `ab84b4f`,
  source unchanged, 55 bare Gitlinks preserved, no runtime/import/tests/build/Git/network.
  R3 preserved exact; selected contract `a345bb95…` unmodified; root will write final
  resolution after this check.

Method: stdlib `json` parse as DATA (no `scripts.*` imports), `ast` leaf checks,
`file:line` byte re-reads. Verified R4 literal schemas/json/rows, not paraphrase.

### 6.1 Verdict (R4)

**NOT_READY. Implementation blocked. No GO, no conditional defer to code.**

R4 verifiably closes R3-B1 (LOW passive ownership + dict builders + zero-write oracles),
R3-B2 (registry dangling + `$id` mismatch), R3-B3 (ONE passive READY + 40 rows + 5 split
rows + readonly vs write-permit + COPY-derived expectedAfter). It does NOT close
R3-B4/B5 historian/closure compatibility (BIG). One precise blocker below (R4-C1);
no other mandatory predicate gaps. Whole NOT_READY / step4B3 OPEN / audit unstarted /
DM021+022 OPEN preserved.

### 6.2 What R4 verifiably closes in actual files (source-grounded)

- **R3-B1 LOW ownership — CLOSED in actual R4 text/json.**
  R4 §1 + json `modules`/`signatures`/`low_zero_write_oracles` (6 oracles): LOW top
  ONLY `core(shape-only)` + `schema_gate`; `agent/HIGH/public State validation`
  forbidden; `require_no_active_guard` lstat-only absent-pass else
  `DM022_TRANSITION_ACTIVE` (no State, no `agent.validate`, no FD);
  `require_completion_consistent` + `require_research_operation_ready` file/path
  reloads only (no State authority, no `verify_state_basis`, no HIGH, no claim);
  detached checkpoint proof vs operational guard separated (agent validator calls
  detached proof, NEVER operational guard; LOW never calls State guard from agent
  validator — no recursion). Builders return `dict/bytes/planned map`, NOT `Path`
  (`build_..._from_paths→dict`, `prove_...→dict+planned map`, HIGH writes);
  HIGH sole mutator while bound guard exists (exclusive `O_CREAT|O_EXCL`/short-write/
  `fsync`/checked-close/`replace`/`dirfsync`/postread). `HIGH→LOW` passive import
  valid, no deadlock (pure builders never require `G+C`). R3 header “never reads
  guard / read-only” corrected to passive-read + inert-NEW-R-only.

- **R3-B2 registry — CLOSED in actual R4 schemas.**
  All `$ref` resolve locally (`#/$defs/*` only, verified via stdlib json: 50+40+34+46+30
  refs, zero dangling, zero non-local, `additionalProperties:false` root throughout).
  `proof.$defs` adds `evidenceAcceptance` (8 keys `schema_version,issue_id,
  research_profile,result_set_sha256,package_sha256,screening_acceptance_sha256,
  result_count,results[]`; rows `evidence_task_id,discovery_ids,sha256,status,
  filename^task-[0-9a-f]{20}\.json$`; digest `result_set_sha256=sha256_object(
  {package_sha256,results sorted})`, run_dir == digest) per
  `survey_evidence_v2.accept_evidence_results:1159` + `_validate_evidence_acceptance_
  content:1255` + `_check_evidence_acceptance_results_content:1216` (byte re-read
  matches); `viewsAcceptance` (7 keys `schema_version,issue_id,research_profile,
  view_set_sha256,profile_sha256,evidence_acceptance_sha256,views[]`; rows
  `evidence_task_id,evidence_sha256,view_sha256,materiality,scope_dimensions`;
  digest `view_set_sha256`, run_dir == digest) per `accept_edition_views:1498` +
  `_validate_edition_views_acceptance_content:1322` + `_check_views_acceptance_rows_
  content:1286` (matches; root 8/7 spot-check holds, `RETROSPECTIVE_PERIOD` in
  `research_profile` enum mirrors `COMMON` + profile union, not admitted as witness).
  `report.$defs.roleSchemaRegistry` retargeted to fixed filenames + local pointers +
  function validators (no URLs, no `$id` mismatch, closed/local):
  `evidence-acceptance → schema-proposals-r4/dm022-revision-proof-v2.schema.json#/
  $defs/evidenceAcceptance` via `_validate_evidence_acceptance_content`,
  `edition-views-acceptance → #/$defs/viewsAcceptance` via `_validate_edition_views_
  acceptance_content`, `materiality-ledger → schemas/materiality-ledger.schema.json#`
  via `_validate_materiality_ledger_content`, `profile-completeness → schemas/
  profile-completeness-result.schema.json#` via `_validate_profile_completeness_content`,
  `candidate-matrix → schemas/candidate-matrix-v2.schema.json#` via
  `validate_selection`, `candidate-selection → schemas/candidate-selection-v2.
  schema.json#` via `validate_architecture` (actual `$id`s `example.invalid` for
  matrix/selection/completeness vs `github` for ledger/supplement verified; registry
  now uses filenames, not `$id` consts — mismatch gone). No remote fetch, no cross-file
  cycle, `$defs` repeated literally. Decision/supplied shape has no `status:PASS`/
  `kind:AGENT_RESEARCH`/writer PASS; retention/guard/completion embedded shapes carry
  NO trusted bools (bools are `present`, `accepted_bound`, `triplet_match:true` const
  recomputed observations, not permission) and NO future SHA (`proof` NO checkpoint,
  `report` NO `checkpoint`/`expectedAfterState`/guard-hash, `checkpoint` NO
  `guardRef`/`afterStateSHA`/completion backref; `*_sha256==sha256_object(body-minus-self)`
  + `sha256_file` distinct).

- **R3-B3 guard+completion — CLOSED in actual R4 rows/json.**
  ONE passive `require_research_operation_ready(repo_root,state_path)` (lstat guard ANY
  present refuses + legacy only-absence vs PREARCH guard-absent + completion exact verify
  via file/path reloads; no `agent.validate`, no HIGH, no claim) imported by HIGH as
  passive IO. 40 rows in json (`counts.rows==40`) match md §3 (36 + 4 splits; R3 36
  preserved as history): added `execution_record:_load_state:82/validate:284`,
  `reader_publication:_validate_renewal_manuscript_binding:171`,
  `weekly:validate_receipt:836`, `longform:validate_longform_reader_input:983` (+
  `longform _derive/load` existing) as dedicated rows 35–38 + existing 34
  (`reader_surface_gate:1152`). Every mutating row lists `READY ... entry + prepublish`
  + `guard ANY present refuses` + `active PREARCH requires completion exact verify
  (COPY-derived expectedAfter, not LIVE equality)` + `completion_check:
  require_completion_consistent ... entry + before-publish`; readonly/diagnostic rows
  (1–6,10–11,14,18,21–23,25,28–29,32,37–38) explicitly `MUST NOT require guard absence`
  + `NOT a write permit; caller producer readiness separate` (no deadlock: pure HIGH-used
  APIs never require ordinary `G+C`). Later forward `no before-State equality`,
  `no window re-check`, `no repository_commit_sha equality` bound per walker
  (§§3–4, rows 27–31 historian/source groups). 7-slot audit all-no-overwrite with
  `audit:330-343` in preflight. Per-invocation pins (expected_head/tree, contract/tool
  SHAs, Profile/source pins, before bytes, 7-slot observations, allowlist, obligations,
  Raw/HTML, mechanical SHAs, executor/recorded_at) correctly remain invocation-bound
  verification (predicate + complete path set + recompute rule in R3 §8 / R4 §3),
  not pre-pinnable map values — residual OPEN is implementation verification, not
  weasel GO (stale refuses + NEW attempt, no field defaults).

- **Snapshot/prepare + planned-SHA + HEAD/tree + DM016/017 + oracles — retained CLOSED.**
  R4 §5 incorporates R3 §§4–11 by reference (no verbatim copy): `request.before.state_path`
  canonical LIVE, COPY separate, HIGH binds CURRENT, LOW detached uses COPY mapping,
  adopt reverifies; `M←D←P←RPT←CP→State→POST` one-way, planned bytes deterministic
  in-memory + FILE sha + expectedState before guard, reconstruct-or-fail-closed;
  guard fixed `<source_root>/orchestration/v2/acceptance-revision.guard.json`,
  transient, phase derived, reopen via nonce+hashes, completion before release,
  `lstat`/safeFD/exclusive/`fsync`/no-`write_json` equivalence, temp-E not adopted,
  unknown never rewritten; HEAD/tree exact + finite diff-set + no gitlinks + head-change
  recompute; DM016 exact types (no aliases, 10 absent OPEN) + DM017 7-field union
  (dimension/description from OLD valid completeness) + witnesses + N1–N12; O-W1/T1/W2/
  T2/R1/G1-3 + F1–F13 with COPY-derived expectedAfter. Spot re-reads match R3 citations.

### 6.3 Remaining blocker (exact, source-grounded, minimal repair)

- **R4-C1 HIGH (BIG) — G71→G76 mechanical compat not concretized in owned-epoch
  code branches; 76/70/73/36/41 literal lists alone do not update actual93 historian
  exact checks.**
  Proof-copy historian currently enforces exact sets with `UNSUPPORTED_MIGRATION`/
  `HISTORY_DIGEST_MISMATCH` unless exactly OLD67 or NEW71:
  `survey_versioned_renewal_history_v2.py:81-260` (`_OLD_PIPELINE_67:99-167`,
  `_NEW_SCHEMAS_4:350-360`, `_recompute_contract8_at_epoch:169-260` pipeline exactly
  OLD67 or NEW71, 71=OLD67+4new, unknown → `UNSUPPORTED`), `_derive_tool_generation:
  1304-1411` (OLD vs NEW only on those sets; partial/new-files-with-OLD67 → REJECT/
  UNKNOWN; OLD R3→OLD, renewal→editorial→NEW), `_expected_staged_code_deps:1277-1303`
  (`OLD50` vs `NEW63` exact; `_OLD_PY_30` + `_OLD_SCHEMAS_14` + family/new sets),
  plus `survey_versioned_renewal_source_v2.py:1414-1540` CURRENT 63/66 member-wise vs
  proof and `survey_weekly_derivation_v2:CURRENT_CLOSURE:28-58` (29) +
  `survey_longform_generated_v2:CURRENT_CLOSURE:52-87` (34) exact names/cardinality.
  R4 `families` gives full literal lists (verified: `pipeline_old67` 67,
  `pipeline_new71` 71 = OLD67+4 renewal schemas, `pipeline_new_dm76` 76 = NEW71+5 DM022
  schemas; `staged_weekly_old50` 50, `staged_weekly_new63` 63, `replay_weekly70` 70 =
  NEW63+2 modules+5 schemas, `replay_union73` 73, `canon_weekly29` 29,
  `canon_weekly36` 36 = 29+7, `canon_longform34` 34, `canon_longform41` 41 = 34+7;
  `p76⊃p71`, `p76-p71` exactly 5 DM022 schemas — source-grounded) and states
  `allowed_change: G71→G76 mechanical ONLY (+2+5 + 17 sites + 8 branches + pipeline
  71→76, SAME authority; no general migration; old G67 adapter composes G71→G76)`.
  But neither `integrated-readiness-r4.md §4` nor `integrated-readiness-r4.json`
  maps the required owned-epoch code branches: which historian functions gain G76
  (e.g. `_recompute_contract8_at_epoch` accept `pipeline_new_dm76` exact + recompute
  Contract8 with 76 aggregate + versions/quality/profiles checks; `_derive_tool_generation`
  derive `G67 vs G71 vs G76` from owned-epoch config + contract8 + schema fingerprints +
  module/mode/membership, never 7-file presence; `_expected_staged_code_deps`/
  `_verify_staged_code_deps` accept `replay70/union73` + `canon36/41` as current G76
  while retaining `OLD50/NEW63` + `29/34` as historical OWN-epoch checks; CURRENT
  closure verifiers accept 76/70/73/36/41 as current while historical G67/G71 stay
  OWN-epoch via retained COPY/lineage + `supersedes`/parent/anchor + SELF/digest).
  Without these branches a DM22 epoch (76-pipeline/70-closure/36-CURRENT) hits
  `UNSUPPORTED_MIGRATION`/`HISTORY_DIGEST_MISMATCH`/closure-name mismatch in later
  editorial/renewal walkers that decision §11.2 REQUIRES to recognize PREARCH,
  bricking §11.2 normal publication/etc. Using post-VALIDATED renewal to authorize
  upstream changes or automatic `old71→76` Core migration is not selected (decision
  §§2/9); R4 correctly says “no general migration” but does not define the required
  distinction: (a) initial-after-DM22 `current76` readback (76-pipeline + PREARCH kind
  present + same contract) vs (b) future76 same-contract (76-pipeline, same contract8/
  versions/quality/profiles, no new PREARCH, pins/controls identical) vs (c) old71
  historical (71-pipeline, no PREARCH, detached validation via retained bytes,
  `historical_state`, never live-before equality). Repair (pre-code, no code):
  append exact owned-epoch predicate + per-function branch table: for each of
  `_recompute_contract8_at_epoch`, `_derive_tool_generation`,
  `_expected_staged_code_deps`/`_verify_staged_code_deps_exact`,
  `verify_renewal_source` CURRENT 63/66 checks, `CURRENT_CLOSURE` 29/34 checks,
  state (i) exact accepted sets (`G67` 67/`G71` 71/`G76` 76 pipelines literal;
  `OLD50`/`NEW63`/`replay70`/`union73`; `29/34` vs `36/41` literal), (ii) derivation
  inputs (owned-epoch config blob mode `100644` + pipeline exact + versions `2.0-rc1` +
  quality3 + research/publication profiles + Contract8 recompute NUL-framed aggregate +
  schema fingerprints + module/mode/membership, never file-presence count), (iii) G76
  admission (only `NEW-DM76` delta + 17 sites + 8 branches + SAME research/Profile/
  Architecture/Draft/reader authority; `old71→76` automatic migration refused; G67
  adapter composes G71→G76 only with same strict conditions), (iv) historical vs
  current handling (`G67/G71` historical via OWN-epoch retained COPY/lineage + SELF,
  no live equality; `current76` initial readback + `future76` same-contract forward
  with pins/controls identical, no entry-window re-check), (v) failure mapping
  (`UNKNOWN cfg` → `UNSUPPORTED_MIGRATION`, mode/blob missing → `FAIL`, partial/new-
  files-with-old-cfg → REJECT/UNKNOWN per current93 precedent extended to G76).
  If any required predicate/walker cannot be included without weakening, return exact
  blocker and revisit A1 vs A2 (decision §9/§11.4), never partially guarded A1.

No other mandatory predicate gaps. Per-invocation values, witnesses, oracles, IO,
HEAD/tree, DM016/017 remain as R4 residual (implementation verification, not map gaps).
40-row `G+C`/State-derivation vs readonly distinction holds; no deadlock (LOW passive
never requires operational `G+C` for HIGH-used pure APIs).

### 6.4 Scope

Independent readiness only. Preserves §§0–5 NOT_READY, R3/R4 as author maps (no approval).
No runtime/import/tests/build/Git/network, no root/author/contract edits
(`a345bb95…` unmodified), no full audit/adoption. Selection does not prove
constructibility. Internal endpoint, not Human Commit Point; ordinary Commit/Push
Human-owned. Bound R4 hashes in §6 header; Human `ab84b4f`, source93, 55 Gitlinks
unchanged.

---

## 7. Final-binding R5 + ROOT review (2026-10-28, fresh independent, preserves §§0–6 NOT_READY)

Read actual R5 + ROOT (not paraphrase):

- `integrated-readiness-r5-family-map.md` 259 lines,
  SHA256 `cc326da994c799794356d7f5fd9956e6278aed6644523d0cd7fb6a03e58c0f92` / 17524B.
- `integrated-readiness-r5-family-map.json` SHA256 `1a4d0eec5a77e91ad490d8947ca1eae83ad87c1df8aaa3dd55f8f0b867d6209f` / 67073B,
  12 `per_function_branches`, G67/G71/G76 literal kept from R4.
- `astra-precode-gate-resolution.md` 37 lines,
  SHA256 `56b668805fded4ac49bf3a2ec8e3cd71c81ad5523fcbd7346be9eca6924a47b9` / 6969B
  (mandatory; §3 is binding correction).
- R4 literal schemas/map preserved: request `a99f0dc1…`, manifest `e7534d01…`,
  proof `a79c0920…`, report `21369608…`, checkpoint `fd39c246…`; R4 json `9ae6a8ce…`.
- Decision `outputs/rephase-1-dm022-prearchitecture-contract-decision.md` incl §11
  SHA256 `a345bb9524b4dfc5b5f32600d0d708687e2b6131d91a43965c97b6418388f223` / 31351B
  unmodified; prior root §5 + FINAL-BINDING design reviews (selection only).
- Proof-copy `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`
  = actual `409b292`/tree `8ce36998` +93/742 readonly. Human `ab84b4f`,
  55 bare Gitlinks untouched. No runtime/import/tests/build/fixture/restore/network/
  Git mutation/source edits/ordinary commit/push. Tools for source data only
  (stdlib `Read`/`Grep`/`ast`/hash as DATA, no `scripts.*` imports).

Method: re-read R4 literal `$ref`s/required/`additionalProperties`/digests/cycles,
R4 40-row `G+C`/State-derivation vs readonly split, R5 literal family lists +
per-function origins/current93/R5_branch, ROOT §§1–4 precedence/boundary/admission,
plus spot `file:line` byte re-reads in final93 for publication boundary
(`renewal_history:1162-1245/2372-2434/2549/2794-2829/3892-4043`,
`pubset:362-393/1120-1141/1308-1351/1437-1441/1583-1646/1874-1877/1992/2151-2253`,
`agent:85-115/1066-1091/1168-1291/1483/2336/2508-2567`).

### 7.1 Verdict

**NOT_READY. Implementation blocked. No GO, no required detail deferred to code.**

R5 + ROOT verifiably close R4-C1 families/owned-epoch narrow compat (three finite
literal families, per-function G67/G71/G76 branches, no auto-migration) and preserve
all R4 closures (acyclic literal schemas, LOW/HIGH passive/zero-write, READY +
completion + 7-slot audit, later readback/history distinction). One precise
publication-boundary overbreadth remains: R5 §2 as written admits PREARCH into the
publication revalidation kind dispatch/supersedes path; ROOT §3 correctly narrows it
to typed upstream research graph nodes only. Until the per-site role table below is
added, the map would allow a valid PREARCH record to stand in for `validation`/
`freeze`/`release` via parsing. Exact blocker R5-PUB-1; no other mandatory gaps.
Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN preserved.

### 7.2 What is verified CLOSED in actual files (source-grounded, no approval)

- **Acyclic literal schemas (R4 preserved, R5 no schema change).**
  All `$ref` resolve locally `#/$defs/*` only (report 50, manifest 40, proof 34,
  request 46, checkpoint 30 refs; zero dangling/non-local via stdlib json),
  `additionalProperties:false` root throughout, `required` ⊆ `properties`,
  `*_sha256==sha256_object(body-minus-self)` + `sha256_file` distinct,
  proof NO checkpoint, report NO `checkpoint`/`expectedAfterState`/guard-hash
  (`guard_claimed` bool + `guard_path` string descriptive only),
  checkpoint NO `guardRef`/`afterStateSHA`/completion backref. Request records mirror
  `run_evidence_v2_interactive._validate_record:119-214` (COMMON 66-70 + THEMATIC
  71-74 + WEEKLY 75 + RETROSPECTIVE 79 empty correctly not admitted;
  REJECTED→NON_MATERIAL / NEEDS_MORE→HOLD `allOf`; entity/claim/verificationItem +
  `ENTITY_TYPES:47-50`/`ARTIFACT_TYPES:51-55`/`EVIDENCE_CLASSES:56-59`/`CARD_STATUS`/
  `VERIFY_STATUS`/`MATERIALITY`/`LINEAGE_ROLES:63`/`WEEKLY_WINDOW_RELATIONS:65`
  match actual). Decision/supplied shape has no `status:PASS`/`kind:AGENT_RESEARCH`/
  writer PASS; retention/guard/completion embedded `$defs` carry no trusted bools
  (bools are `present`/`accepted_bound`/`triplet_match:true` recomputed observations)
  and no future SHA (`M←D←P←RPT←CP→State→POST` one-way). R5 correctly makes no
  schema edits.

- **LOW/HIGH imports/role dispatch (R4 closed, R5 preserved + ROOT §2).**
  LOW top ONLY `core(shape-only)` + `schema_gate`; all `evidence/screening/
  completeness/discovery/agent` function-local; NO `agent`/`HIGH`/public State
  validation; passive `lstat`-only guard absence + file/path completion allowed;
  private pure in-memory after trusted load; builders return `dict/bytes/planned map`
  NOT `Path` (R4 `low_zero_write_oracles` 6 entries: reloads/writes/calls_not_made +
  zero-write oracle per API). HIGH sole mutator while bound guard exists
  (exclusive `O_CREAT|O_EXCL`/short-write/`fsync`/checked-close/`replace`/`dirfsync`/
  postread, never `core.write_json`/`copy2`/`is_file`). Owner-A calls LOW detached
  proof function-locally for history/detached checks. Agent validator calls detached
  proof NEVER operational guard; LOW never calls State guard from agent validator;
  `HIGH→LOW` passive allowed, no recursion. Early COPY in prepare is inert NEW-R
  input (no canonical/State/guard mutation); adopt reverifies. Planned-CP bytes
  deterministic in-memory + FILE sha + expectedState before guard; checkpoint never
  backrefs guard. No `write_json`-as-atomic, temp-E ≠ adopted, unknown never rewritten.

- **Operational readiness + 7-slot audit (R4 40 rows preserved).**
  ONE passive `require_research_operation_ready(repo_root,state_path)` (lstat guard
  ANY present refuses + active PREARCH completion exact verify via file/path reloads;
  no `agent.validate`, no HIGH, no claim) at entry + prepublish on every mutating row;
  readonly/diagnostic rows explicitly `MUST NOT require guard absence` + `NOT a write
  permit`. Guard ANY absent + (active PREARCH ⇒ completion verifies checkpoint SHA +
  COPY-derived expectedAfter + `seven_plan` vs slot lstat) for active NEW kind across
  later stages; expectedAfter ≠ later LIVE once forward advanced; completion-lost/guard-
  missing still blocks; explicit resume RECOVERY bound intent, no takeover. Pure HIGH-used
  APIs never require ordinary `G+C` (no deadlock). 40-row `counts.rows==40` matches md;
  5 split rows added (`execution_record:82/284`, `reader_publication:171`,
  `weekly:validate_receipt:836`, `longform:validate_longform_reader_input:983`);
  7-slot audit all-no-overwrite with `audit:330-343` in preflight. Later forward
  `no live-before equality`, `no window re-check`, `no HEAD equality with revision HEAD`;
  historical OWN-epoch via retained bytes/git-show, current validates NOW with fresh
  tools (no stale-proof waiver for future G76→G76 renewal).

- **Families literal + narrow G71→G76 mechanical compat (R5 closes R4-C1 membership).**
  R5 json gives full literal path lists (verified counts: `pipeline_old67` 67,
  `pipeline_new71` 71 = OLD67+4 `_NEW_SCHEMAS_4:350-360`, `pipeline_new_dm76` 76 =
  NEW71+5 `dm022-*.schema.json`, `p76⊃p71`, `p76-p71` exactly 5; `staged_weekly_old50`
  50, `staged_weekly_new63` 63, `replay_weekly70` 70 = NEW63+2+5, `replay_union73` 73,
  `canon_weekly29` 29, `canon_weekly36` 36 = 29+7, `canon_longform34` 34,
  `canon_longform41` 41 = 34+7; `implicit3`/`quality3`/`control_roots` unchanged;
  `new_modules` 2 + `new_schemas` 5). Per-function branches name actual fn + signature +
  argument origin + callsite branch condition (12 branches: `_recompute_contract8_
  at_epoch:169-260`, `_derive_tool_generation:1304-1411`, `_expected_receipt_closure:
  1263-1277`/`_expected_staged_code_deps:1280-1301`, `_verify_receipt_closure_exact:
  1414-1450`/`_verify_staged_code_deps_exact:1453-...`, `_require_known_schema_sha:
  432-438` + `_KNOWN_SCHEMA_SHAS:410-429` + `OWNER_REGISTRY:380-400` +
  `_ALLOWED_SCHEMA_PATHS:402` + `_resolve_json_pointer:441-468` (`''`=whole doc,
  `'/'` forbidden), `verify_versioned_history:3864`/`verify_renewal_retention:4200` +
  kind helpers `_is_legacy:1165`/`_is_editorial:1169`/`_is_renewal:1177`/`_record_kind:
  1197` + `_walk_chain_backwards:1222` + `_verify_editorial_ancestor:1966` +
  `_verify_versioned_ancestor:2808`, source `_expected_closure_names:1403-1405`/
  `verify_renewal_source_proof:1408-...`/`_verify_current_tools_committed:246-...`/
  `_control_paths_for_current:227-243`, HIGH `_current_commit:460-465`/
  `_observe_renewal_entry:619-...`/`_recheck_entry_pins:808-819`/`_derive_old_tool_epoch:
  2066-...`/`_require_renewal_entry_window:560-...`, canonical Weekly/LF
  `current_closure:683/535` + verifiers/receipts, LOW 17 sites + 8 branches).
  Owned epoch from EXACT config registered sets + Contract8 NUL aggregate + schema
  fingerprints + module/mode/membership (never presence/count); historical G67/G71 stay
  OWN-epoch (no old tool LIVE); current G76 supports new PREARCH CP through initial
  publication/editorial/renewal + normal lifecycle; `G71→G76` ONLY +2+5 + old-shape-
  preserving 17+8 + pipeline 71→76 registration, SAME research/Profile/Architecture/
  Draft/reader authority; no general migration, no post-Architecture upstream revision,
  no review/Profile/rebind/recipe change; unknown refuses. Admission still recomputes
  ALL current proofs (U) or checks (C) with truthful Core reason + prePreview window;
  classification alone confers NO permission; `old71→76` auto-migration NOT selected
  (distinguishes initial-after-DM22 `current76` readback + future76 same-contract forward
  vs old71 historical). Required witnesses (G71→G76 mechanical renewal UNMODIFIED
  upstream as bootstrap negative counterexample; G76 DM022 CP → initial publication →
  later editorial/renewal + G67/G71 history readback) are precode oracles, no execution.

### 7.3 Remaining blocker (exact, minimal repair, no deferral)

- **R5-PUB-1 HIGH — R5 §2 “ADD PREARCH branch” overbroad as written; ROOT §3
  correction needs concrete per-site role table.**
  ROOT §3 (binding): R5 “ADD PREARCH branch” valid ONLY for typed upstream research
  graph nodes reached from accepted-research/retention graph. Must NOT add PREARCH to
  publication activation discriminators, publication `_record_kind`, State
  `publication_revalidation_provenance` selector, or publication `supersedes` chain.
  A PREARCH record supplied as activation/validation checkpoint must refuse as wrong
  family. `LOW.load_typed_checkpoint_record` dispatches ordinary vs PREARCH research
  checkpoint; callers additionally enforce expected role/producer boundary; parsing
  valid PREARCH never allows standing in for `validation`/`freeze`/`release`.
  Research vs publication `supersedes` remain separate predecessor/anchor chains.

  R5 as written violates this at: `integrated-readiness-r5-family-map.md:120-128`
  + json `per_function_branches[7]` (`verify_versioned_history … + _is_legacy_record/
  _is_editorial_record/_is_renewal_record/_record_kind + _walk_chain_backwards +
  _verify_editorial_ancestor + _verify_versioned_ancestor`): “ADD PREARCH kind branch …
  admitted ONLY at G76” without restricting to upstream research nodes. Actual93:
  `_record_kind:1197` dispatches ONLY `LEGACY` (`reason_class==LEGACY_REASON` + no `kind`,
  `:1165`), `EDITORIAL` (`:1169`), `VERSIONED` (`:1177`) — publication revalidation
  kinds; `_walk_chain_backwards:1222` walks publication revalidation `supersedes`
  chain (`HISTORY_ANCESTOR … cycle/too deep`); `_verify_editorial_ancestor:1966` /
  `_verify_versioned_ancestor:2808` verify editorial/renewal ancestors (Contract8,
  closure/code_deps exact, schema fingerprints, SELF digests, retained COPY/lineage).
  PREARCH (`kind=PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1` +
  `reason=REVIEWED_ACCEPTED_UPSTREAM_CORRECTION` + `EVIDENCE→EVIDENCE` +
  `producer_boundary` + 3 roles + 4 `NamedRef` + SELF + sole `DM022_SUPERSESSION_PROOF`)
  is a Stage Checkpoint kind for upstream research, not a revalidation kind. Adding it
  to `_record_kind`/revalidation chain would let a research record stand in for
  publication activation/validation and conflate research `supersedes`/parent/anchor
  with publication `supersedes` (pubset `1120/1141/1308/1437/1583/1646/1874`;
  agent `1168/1174/1291/2336/2508-2567`; `publication_revalidation_provenance`
  selectors pubset `1992/2151/2215/2253`, agent `1066/1091/1274/1483/2509`;
  discriminators pubset `362/377/393`, agent `85/99/115`).

  Repair (pre-code, no code): narrow R5 §2 + json branch to upstream-only and add
  per-site expected-role table for all 17 loader sites. Keep `LOW.load_typed_checkpoint_
  record` dispatch (kind absent→old `stage-checkpoint-v2.schema.json`, kind PREARCH→new
  DM022 schema, else refuse; no `.get(kind,legacy)` fallback, no raw mutation).
  Then state for each site the expected checkpoint role(s)/producer boundary + PREARCH
  admit/refuse: e.g. upstream research loads (agent `489/819` generic via `checkpoint`/
  `checkpoint+artifact_name` params; `load_renewal_accepted_authority:933` evidence/
  ledger/completeness nodes; `verify_renewal_retention` retention graph; P1/P2R/P2V/P3S/
  source/H/Freeze retained upstream refs) ADMIT PREARCH ONLY when expected role ∈
  `{evidence,materiality,completeness}` + `producer_boundary=CANDIDATES→EVIDENCE` at G76;
  publication/selection/validation/freeze/release loads MUST refuse PREARCH even if
  parses — `pubset:56/1213/1627/1981` (anchor/before-digest/selection priors),
  `editorial_correction:557` downstream selection/architecture/draft nodes,
  `release:121` (“Release Stage Checkpoint”), `stage_validation:288` prior where
  expected ≠ upstream research, `weekly_refresh:931` (“refresh validation checkpoint”),
  agent `1011` pending validation, `1532/1971/2397` revalidation priors/basis,
  `1758/1774` forward builder/advance (forward `from→next` only), pubset/agent
  activation discriminators + `publication_revalidation_provenance` selectors +
  both `supersedes` chains. `verify_versioned_history`/`verify_renewal_retention`/
  `_record_kind`/`_is_*`/`_walk_chain_backwards` (revalidation chain) MUST NOT gain
  PREARCH; unknown kind there → `HISTORY_DIGEST_MISMATCH` (no auto-upgrade); PREARCH
  supplied as activation/validation → refuse wrong family. Detached research-history
  validator path for upstream PREARCH nodes (retained refs + OWN-epoch graph, no live
  State, no `agent.validate`, no HIGH) stays separate from revalidation chain; each
  chain keeps own predecessor/anchor checks with no cross-chain inheritance.
  State the 17-row table (`file:line` + expected `checkpoint(s)`/`from→to`/
  `producer_boundary` + admit/refuse + oracle `entry + seam none + writes none` on
  refuse) in R5 json/md; correct json `per_function_branches[7]` R5_branch accordingly.
  If any required walker cannot include without weakening, return exact blocker and
  revisit A1 vs A2 (decision §9/§11.4), never partially guarded A1.

No other mandatory gaps. Per-invocation pins, witnesses, oracles, IO, HEAD/tree,
DM016/017 remain implementation verification (predicate + complete sets + recompute
rule closed), not map gaps. 40-row `G+C`/State-derivation vs readonly holds; no deadlock.

### 7.4 Scope

Independent readiness only. Preserves §§0–6 NOT_READY. No runtime/import/tests/build/
fixtures/restore/network/Git mutation/source edits/ordinary commit/push, no root/author/
contract edits (`a345…` unmodified), no full audit/adoption. Selection does not prove
constructibility. Internal endpoint, not Human Commit Point. Bound R5 + ROOT hashes in
§7 header; Human `ab84b4f`, source93, 55 Gitlinks unchanged.

Preserved verbatim for history (do not edit §§0–7 below).

---

## 8. Final-binding R6 review (2026-10-28, fresh independent, preserves §§0–7 NOT_READY history)

Read actual R6 (not paraphrase) + ROOT §3 + R4 literals/map + final93:

- `integrated-readiness-r6-role-map.md` 197 lines,
  SHA256 `865c938eb8bf8f9ff09084f184f6092c25c5f10eb6e35f964477228c59a8dd26` / 15693B.
- `integrated-readiness-r6-role-map.json` SHA256 `4b5758c7fe9106e2687bf4b073716210823c9ab446237746ff47b702798a09c2` / 19028B,
  `sites_17` + `discriminators` 9 + `chain_walkers` 9 + `selectors` 9.
- ROOT `astra-precode-gate-resolution.md` 37 lines,
  SHA256 `56b668805fded4ac49bf3a2ec8e3cd71c81ad5523fcbd7346be9eca6924a47b9` (mandatory;
  §3 research-vs-publication correction is binding).
- R4 `schema-proposals-r4/` 5 literal JSON preserved (request `a99f0dc1…`,
  manifest `e7534d01…`, proof `a79c0920…`, report `21369608…`, checkpoint `fd39c246…`;
  all `$ref` local `#/$defs/*` only, zero dangling/non-local via stdlib json),
  R4 40-row `G+C`/State-derivation map + R5 G67/G71/G76 literal families preserved.
- Decision `outputs/rephase-1-dm022-prearchitecture-contract-decision.md` incl §11
  SHA256 `a345bb9524b4dfc5b5f32600d0d708687e2b6131d91a43965c97b6418388f223` / 31351B
  unmodified; prior root §5 + FINAL-BINDING design reviews (selection only).
- Proof-copy `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`
  = actual `409b292`/tree `8ce36998` +93/742 readonly. Human `ab84b4f`,
  55 bare Gitlinks untouched. No runtime/import/tests/build/fixture/restore/network/
  Git mutation/source edits/ordinary commit/push. Tools for source data only
  (stdlib `Read`/`Grep`/`ast`/hash as DATA, no `scripts.*` imports).

Method: verified R6 literal table/JSON (not ROOT paraphrase), ROOT §3 boundary,
R4 schemas/rows, plus spot `file:line` byte re-reads for publication boundary
(`renewal_history:1162-1245/2372-2434/2549/2794-2829/3892-4043`,
`pubset:56/362-393/1120-1141/1308-1351/1437-1441/1583-1646/1874-1877/1992/2151-2253/2267`,
`agent:42/85-115/489/819/1011/1066/1091/1274/1483/1532/1758/1774/1971/2397/2509`,
`editorial:557`, `release:121`, `stage_validation:288`, `weekly_refresh:931`,
`resolve_publication_mode:2253` current93 `else CANONICAL` default,
`stage-checkpoint-v2.schema.json` required + `additionalProperties:false`).

### 8.1 Verdict

**PRE_CODE_READY (bounded pre-code map complete). No implementation authorization,
no code/runtime proof, no Production acceptance.**

R6 + ROOT §3 verifiably close R5-PUB-1 without widening publication authority, and
preserve all R4 closures (acyclic literal schemas, LOW/HIGH imports/role dispatch,
operational READY + completion + 7-slot audit, later readback/history distinction,
full G67/G71/G76 family compat). Remaining items in §8.3 are exact binding limits
(wording qualifications with source grounding), not map blockers; root may append the
matching exact qualification before final confirmation. No required detail deferred to
implementation. Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN
preserved (pre-code gate closed; implementation + tests + independent implementation
review + audit + adoption still open). Ordinary Commit/Push Human-owned.

### 8.2 What is verified CLOSED in actual files (source-grounded, no approval)

- **17-site concrete role map (not 17 runtime reads).**
  R6 `sites_17` correctly distinguishes kind: 2 constant declarations
  (`agent:42`, `pubset:56` `CHECKPOINT_SCHEMA = Path(...)` — Path consts only, no data
  path; migration adds LOW DM022 schema const, old const byte-identical),
  12 runtime loaders (`489/819/1011/1532/1971/2397/1213/1627/1981/557/288/931`
  with `repo_root + {path,sha256} / checkpoint / prior_ref / validation_ref` origins
  from State provenance key / retained history graph / `REQUIRED_CURRENT`/prior map),
  3 runtime loader/writers with payload (not file reads: `agent:1758` builder
  `validate_instance(payload)` forward `from==current && to==next`,
  `agent:1774` advance `load_and_validate(checkpoint_path)` forward
  `from==current && to==next && set==stage.checkpoints`,
  `release:121` `validate_instance(payload)` `FROZEN→RELEASED`). Each row states
  `args_origin` (actual signature/origin), `expected` (caller checkpoint/artifact/
  `from→to`/role), `producer` (legacy `stage_plan` lookup or PREARCH
  `EVIDENCE→EVIDENCE` + boundary), `prearch` admit/refuse + oracle
  (`entry + seam none + writes none`, `DM022_WRONG_FAMILY` / `HISTORY_DIGEST_MISMATCH`).
  Admit ONLY upstream `{evidence,materiality,completeness}` + boundary at G76
  (rows 2–3 generic via caller `checkpoint`/`checkpoint+artifact_name`; row 16 generic
  via caller-expected role); all validation/freeze/release/selection priors refuse
  even if parses (rows 4–5,8–9,11–15,17: `1011` pending validation, `1532/1971/2397`
  revalidation prior/basis, `1213` anchor prior, `1627` before-digest 7 roles,
  `1981` selection prior + canonical7, `557` validation/downstream, `121` release,
  `288` non-upstream prior, `931` refresh validation, `1758/1774` forward builder/advance).
  Spot re-reads match labels (`557` “original validation checkpoint”
  `DRAFT_COMPLETE→VALIDATED_DRAFT`, `931` “refresh validation checkpoint”,
  `121` “Release Stage Checkpoint”, `288` “prior Stage Checkpoint”, `1213/1627/1981`
  anchor/before-digest/selection priors). Late-forward `no live-before / no window /
  no HEAD equality` applies ONLY to admitted upstream readback, never refused rows.

- **No publication supersedes decoder change; correct later upstream reads.**
  Discriminators pure dict-only, no file IO: `pubset:362/377/393` +
  `agent:85/99/115` (`_is_renewal/_is_versioned/_is_versioned_seal` exact pairs) +
  `history:1165/1169/1177` (`_is_legacy/_is_editorial/_is_renewal`) all
  `PREARCH=>False` (has `kind` vs legacy no-`kind`; wrong pair vs editorial/renewal);
  callers requiring versioned/legacy must then refuse (no auto-upgrade, no fallback).
  Chain walkers publication-`supersedes` ONLY (`history:1222` structural load + schema +
  cycle/depth, `_verify_editorial_ancestor:1966`/`_verify_versioned_ancestor:2808`,
  `pubset:1120/1141/1308/1437/1583/1646/1874`): MUST NOT walk research
  `supersedes[]`/parent/anchor, MUST NOT call new LOW research decoder for chain
  membership, unknown (incl PREARCH) ⇒ refuse. Existing `_load_record_file`
  validates against `REVALIDATION_SCHEMA` (not Stage Checkpoint), so PREARCH Stage
  Checkpoint bytes already fail chain schema even before kind check — no decoder change,
  existing validation refuses. Detached upstream PREARCH reads stay SEPARATE
  (`load_renewal_accepted_authority:933` evidence/ledger/completeness nodes,
  `verify_renewal_retention` retention graph, P1/P2R/P2V/P3S/source/H/Freeze retained
  upstream refs via LOW + retained COPY + OWN-epoch graph, no live State, no
  `agent.validate`, no HIGH); each chain keeps own predecessor/anchor checks, no
  cross-chain inheritance. `record_kind:1197` dispatches ONLY LEGACY|EDITORIAL|VERSIONED;
  PREARCH/unknown ⇒ `HISTORY_DIGEST_MISMATCH` (no PREARCH arm — R5 overbreadth removed).

- **Selectors reject malicious PREARCH pointer, never CANONICAL fallback.**
  9 selectors with `publication_revalidation_provenance {path,sha256}|None` (exact None
  only = no-pointer; malformed even `{}` fail-closed): `pubset:1992` (None⇒CANONICAL
  anchor else load + LEGACY|EDITORIAL|VERSIONED), `:2151` (role ∈ `PUBLICATION_ROLES_7`
  + `publication-candidate`; PREARCH roles not allowed ⇒ refuse before any read),
  `:2215` (exact None⇒canonical token WITHOUT record; invalid dict fail-closed),
  `:2253/:2267` + `agent:1066/1091/1274/1483/2509` (pending predecessor equality/bind,
  head dispatch `editorial|versioned|legacy else unknown`, `_resolve_publication_
  revalidation` load + three-way else refuse, Gate predecessor bind). All state
  `PREARCH=>REFUSE wrong family`. R6 FIX verified necessary: current93
  `resolve_publication_mode:2253` does `_is_versioned_record=>VERSIONED_ACTIVE else
  CANONICAL`, silently mapping valid PREARCH to CANONICAL; R6 requires explicit PREARCH
  test BEFORE versioned test (refuse, never default). Other selectors already fail-closed
  on unknown (explicit that PREARCH must hit else-branch, no new arm).

- **Families + owned-epoch + admission scope preserved (R5 closed, R6 narrows only).**
  G67/G71/G76 literal lists kept (67/71/76, 50/63/70/73, 29/34/36/41 in R5/R6 JSON),
  owned-epoch from EXACT config sets + Contract8 NUL aggregate + fingerprints +
  module/mode/membership; historical G67/G71 OWN-epoch; current G76 supports new PREARCH
  through initial publication/editorial/renewal + lifecycle; `G71→G76` ONLY +2+5 +
  old-shape-preserving 17+8 + 71→76 registration, SAME authority; no general migration,
  no post-Architecture revision; admission recomputes ALL current proofs (U) or checks (C).
  R6 adds no schemas, changes no families, widens no authority.

### 8.3 Exact binding limits (wording qualifications, not map blockers)

Root may append these verbatim before final confirmation; implementation must enforce them;
they do not reopen the map.

- **B-L1 — illustrative prior/lineage notes vs strict forward schema.**
  R6 §1 lines 46–57 (“`prior_checkpoint` or lineage notes”) is illustrative ONLY.
  Binding: forward `stage-checkpoint-v2.schema.json` unchanged byte-identical
  (required `schema_version,issue_id,from_state,to_state,checkpoints,recorded_at,
  implementation,contract,artifacts,reviews,summary`, `additionalProperties:false`,
  per-`from_state` artifact branches; no `prior_checkpoint`/`lineage_notes`/`parent_
  anchor`/`supersedes[]` fields — verified in final93). “Containing a reference to
  accepted PREARCH” means ONLY existing basis SHAs recomputed from R4 bytes
  (e.g. `candidate-matrix basis.*_sha256`, `candidate-selection`/`architecture` basis,
  review `basis.*_sha256`) plus retained-COPY/`supersedes`/parent/anchor lineage in the
  PREARCH record + `R/` manifest/proof/report/retention (never in forward checkpoint).
  A forward record whose OWN `kind/from→to/producer` claims PREARCH at a
  selection/validation/freeze/release path (even with correct hash pointers) is
  pretending ⇒ refuse. No new forward-schema fields authorized.

- **B-L2 — pointer-record read BEFORE gate (classification only), downstream reads AFTER.**
  R6 §4 line 177 (“file reads AFTER family gate, never before”) is overbroad as written.
  Binding: untrusted pointer-record file read (`lstat` + read + hash + strict duplicate-key
  parse + kind dispatch via shared LOW decoder, no authority consumption, no `resolve_raw_
  path`/`sha256_repo_file` of referenced artifacts, no live re-hash of 4 refs, no State/
  guard/HEAD) happens BEFORE the role/family gate FOR CLASSIFICATION ONLY. All downstream
  authority consumption (artifact `resolve_raw_path`/`sha256_repo_file`, live re-hash +
  same-record + lineage + SELF/proof/digest verification, `REQUIRED_CURRENT`/contract/
  gate checks) happens ONLY AFTER the caller-expected role + producer boundary + G76
  window gate passes. No downstream bytes are trusted for classification; classification
  confers no permission (parse-valid ≠ authorized). This matches R6 decoder
  (`load_typed_checkpoint_record` parse only) vs authoritative checks (caller expected
  role / shared semantic validator) split.

- **B-L3 — row 14 expected-role label (disposition correct, label needs narrowing).**
  R6 JSON `sites_17` row 14 (`editorial_correction:557`) states expected “downstream
  selection/architecture/draft”. Actual93 `557` loads the original validation checkpoint
  (`ref=(checkpoint_provenance).validation`, label “original validation checkpoint”,
  identity `DRAFT_COMPLETE→VALIDATED_DRAFT` + `validation ∈ checkpoints`, verified
  `557` bytes above). Binding: row 14 expected = original validation checkpoint
  (`DRAFT_COMPLETE→VALIDATED_DRAFT`); PREARCH ⇒ refuse (wrong family). Downstream
  selection/architecture/draft nodes (`1502-1542` graph, `_ckpt_resolve:1454` row 25 in
  R4 40-row map) are covered separately (upstream PREARCH nodes via LOW R4 + same wrapper;
  downstream nodes refuse PREARCH). Admit/refuse outcome unchanged (both refuse); label
  corrected to actual callsite so implementer enforces the right expected role.

If root appends B-L1–B-L3 verbatim (or equivalent exact qualification), no map change is
needed; R6 + ROOT §3 then fully close R5-PUB-1. If any walker cannot include without
weakening, return exact blocker and revisit A1 vs A2 (decision §9/§11.4), never partially
guarded A1.

### 8.4 Scope

Independent readiness only. Preserves §§0–7 NOT_READY history. No runtime/import/tests/
build/fixtures/restore/network/Git mutation/source edits/ordinary commit/push, no root/
author/contract edits (`a345…` unmodified), no full audit/adoption. Selection + map do not
prove constructibility or runtime correctness. Internal endpoint, not Human Commit Point.
Bound R6 + ROOT + R4 hashes in §8 header; Human `ab84b4f`, source93, 55 Gitlinks unchanged.

Preserved verbatim for history (do not edit §§0–8 below).

---

## 9. FINAL-BINDING ROOT confirmation (2026-10-28, independent final readback, preserves §§0–8)

Read FULL ROOT `astra-precode-gate-resolution.md` (63 lines, not 37-line snapshot):

- FULL file SHA256 `0425c5300c9c7211e4468d3b842c4e3af1acb9f5bf1eba00e90f7ba72ef44a5a` / 13788B.
  Prior §8-bound `56b668805fded4ac49bf3a2ec8e3cd71c81ad5523fcbd7346be9eca6924a47b9` is the
  §§1–4 37-line snapshot only, superseded as gate status by §5.
- §5 `PRE_CODE_READY — bounded design/interface map only` supersedes pending gate in §§1–4.
  Selected map: R3 retained mechanics overridden by R4 md/json + five literal
  `schema-proposals-r4/` files, R5 family md/json, R6 role md/json, and ROOT incl §5.
  R6 replaces R5 `per_function_branches[7]` and overbroad publication-chain wording.
  Contract `a345bb9524b4dfc5b5f32600d0d708687e2b6131d91a43965c97b6418388f223` / 31351B unchanged.
  B2/B4 map gates closed for pre-code purposes, not proven by execution.
- §5.1 adoptions verified against actual R6 + final93 (read-only, no runtime):
  1. Forward schema byte-identical — adopts §8 B-L1. No new fields in
  `stage-checkpoint-v2.schema.json`; basis SHAs bind R4 bytes; lineage in PREARCH/
  manifest/proof/report/retention only. Source-grounded, no widening.
  2. Classification read precedes admission; referenced consumption follows —
  adopts §8 B-L2. Untrusted pointer `lstat`+read+hash+strict parse (no authority
  consumption) BEFORE gate for classification; `resolve_raw_path`/`sha256_repo_file`
  + live re-hash + same-record/lineage/digest/content AFTER caller-expected role/
  producer + G76 window admission. LOW Stage/PREARCH decoder for research sites only;
  publication revalidation parsing/schema for chain sites; no publication activation
  through LOW decoder. Creation window from retained operation context, never reimposed
  on later LIVE readback. Matches ROOT §3 separate-chain rule.
  3. R6 row14 = original validation checkpoint — adopts §8 B-L3. Actual
  `survey_editorial_correction_proposal_v2.py:549–563` reads
  `checkpoint_provenance.validation`, requires `DRAFT_COMPLETE→VALIDATED_DRAFT` +
  `validation` in checkpoints. PREARCH refuses. Downstream graph nodes are separate
  R4 row25. Labels must not replace predicate.
  4. 17 sites = 2 constants + 2 payload + 13 file loaders — corrects §8 grouping
  (advance `1774` takes `checkpoint_path` file, so file-loader not payload).
  `agent:42` / `pubset:56` consts unchanged (declaration only); new LOW DM022 const is
  not a new authority reader; payload `validate_instance` stays pure validation.
  R6 `sites_17` kind field already distinguishes this; count proof not affected.
  5. Publication mode fail-closed — ROOT directly read `pubset:2241–2264`
  (current `else CANONICAL` default) and `history:1165–1241` (`_record_kind` only
  LEGACY|EDITORIAL|VERSIONED, `_load_record_file` uses REVALIDATION_SCHEMA).
  R6 explicit PREARCH-before-versioned refusal required; neither gains PREARCH arm;
  LOW handles upstream research nodes only. No publication decoder change.
- §5.2 next-unit scope + §5.1 “no new family/schema” introduce no new predicates:
  whole-operation isolated final93-derived source, mapped 2 modules/5 schemas + all
  named caller/config/closure changes, new-reader return-to-Astra, invocation values
  from actual fixture/source, §10 + oracle witness scope, interruption/recovery/negative
  matrices, independent-GitDB fixtures, Human-owned commits, no old PASS transfer;
  DM016/017/quality/audit/adoption/savings remain open; no Production/W40 authority.
  No widened acceptance permission (classification ≠ adoption; narrow G71→G76
  mechanical compat subject to full ordinary renewal current proof).

No unclosed predicate. R5-PUB-1 closed by R6 per-site roles + discriminators +
chain-walker + selector tables as narrowed by ROOT §3/§5 and §8 B-L1–B-L3 binding limits.
No essential detail deferred to implementation beyond per-invocation values derived from
actual fixture/source at implementation time (predicate + complete sets + recompute rule
closed here).

### 9.1 Verdict

**PRE_CODE_READY — bounded design/interface map only (final-binding).**
Preserves §§0–7 NOT_READY history. Implementation still requires Human continuation,
whole-operation build/tests, affected regressions, and independent implementation review
before closeout; no code/runtime proof, no Production acceptance, no adoption.
Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN preserved except
pre-code gate closed. Ordinary Commit/Push Human-owned.

### 9.2 Scope and binding

Independent readiness only. Reviewed R6 role md `865c938e…` / json `4b5758c7…`,
R4 md/json + 5 literal schemas (`a99f0dc1…`, `e7534d01…`, `a79c0920…`, `21369608…`,
`fd39c246…`), R5 family md `cc326da9…` / json `1a4d0eec…`, ROOT FULL `0425c530…` / 13788B
(same binding as family map), decision `a345…` / 31351B, final93 `409b292`/tree `8ce36998`
+93/742 readonly. No runtime/import/tests/build/fixtures/network/Git mutation/source
edits. Existing 55 Gitlinks untouched. Root docs may link this report hash but must not
modify it. Internal endpoint, not Human Commit Point.
