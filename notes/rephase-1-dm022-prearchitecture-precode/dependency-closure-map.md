# DM022 pre-Architecture — dependency / fingerprint closure supplement (AUTHOR, pre-code only)

2026-10-27 AUTHOR-side. No implementation/import/tests/build/fixture/restore/network/Git mutation.
Method was `Read`/`Grep` + `ast` parse as DATA only; no `scripts.*` imports executed.
Other R2 siblings readonly; this unit writes ONLY this map + `dependency-closure-map.json`.
Root integration next; no independent PASS/readiness authority.

Binds: decision `outputs/rephase-1-dm022-prearchitecture-contract-decision.md` incl §11,
SHA256 `a345bb9524b4dfc5b5f32600d0d708687e2b6131d91a43965c97b6418388f223`/31351B;
`astra-review-resolution.md` incl §5 + BOTH FINAL-BINDING addenda (selection only, B2/B4 OPEN).
Source read-only: `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`
= actual `409b292`/tree `8ce36998` +93/742. Human `ab84b4f` assumed; 55 bare Gitlinks preserved.
Availability honest scope: 5/5 stdlib rehash match per `source-and-carryover-observation.md` §8
(renewal HIGH/H/S + agent-delta + evidence-delta); full93/742 NOT recertified;
missing26309/bulk31466/runtimeTeX/5 whitespace diagnostics retained.

## 1. Literal names confirmed + disagreements flagged

Confirmed in `authority-consumer-map-r2.md` §§1–2/15, `schemas-generation-dag-r2.md` §§5/7/13,
`guard-resume-oracles-r2.md` §0:

- LOW `scripts/survey_research_authority_v2.py` — detached research-authority resolver + State-free revalidation.
- HIGH `scripts/survey_prearchitecture_acceptance_v2.py` — coordinated LIVE acceptance (sole State/guard/retention owner).
- Owner-A (existing, no new file) `scripts/survey_agent_control_v2.py` gains new-kind branch inside; calls LOW pure validators function-locally for detached/history checks.
- 5 required schemas: `dm022-revision-request` / `dm022-revision-manifest` / `dm022-revision-proof` /
  `dm022-preadoption-report` / `dm022-supersession-checkpoint` (all `schemas/dm022-*-v2.schema.json`);
  +1 optional POST `dm022-completion-receipt`. Guard path fixed
  `<source_root>/orchestration/v2/acceptance-revision.guard.json` (zero hits in final93);
  revision-id `[a-z0-9][a-z0-9-]{0,63}`; `R=<source_root>/research/v2/acceptance-revisions/<rev>/` + 18 fixed children.

Disagreements (prompt shorthand vs R2 binding):

- D1 — prompt “4 new request/proof/checkpoint/report schemas” omits `revision-manifest` (5th required)
  and optional receipt. R2 §§9.3–9.8 + JSON `schemas_required 5 + optional 1` is binding.
  Manifest FILE SHA is M identity (no embedded self); omitting it recreates the Finding-4 future-ref cycle.
- D2 — prompt “embedded guard/retention/completion defs” contradicts R2 §9.8 + C ownership.
  R2 carries only `SizedRef` + `phase`/path strings; guard/record/write-set/fault oracles + retention
  manifest + completion receipt shape are C-owned (`guard-resume-oracles-r2.md` §§1/7). No duplicated diverging schema.
- D3 — prompt “new2/4” vs actual 2+5+1. No arbitrary 7-file budget is imposed; if a real new component
  needs more, root decides. Manifest + receipt are not omittable without breaking the SHA DAG.
- D4 — `inventory.json` 28 rows (R1) vs `inventory-r2.json` 29 rows (adds `_validate_core_stage_report`
  lifecycle row + screening/prior splits). R2 count is binding; R1 preserved as history.

## 2. Stage Checkpoint loader: standalone NEW + shared kind dispatch (concrete)

Old `schemas/stage-checkpoint-v2.schema.json` requires top-level `from_state`/`to_state`
(`required` 11 incl those two, `additionalProperties:false`) with per-`from_state` const branches,
e.g. `CANDIDATES_NORMALIZED` → 4 names `evidence-acceptance/edition-views-acceptance/materiality-ledger/profile-completeness`
(`evidenceArtifacts`); `EVIDENCE_REVIEWED` → 2 names `candidate-matrix/candidate-selection`;
plus `localStageValidationReview` requiring exactly one `CORE_STAGE_CONTRACT` deterministic PASS row.
Validator `_validate_checkpoint_record:481` enforces `record.from/to == producer(from/to)` via
`_producer_for_checkpoint:348` (stage_plan lookup), and `_validate_core_stage_report:365`
enforces `report.from/to == historical_state.lifecycle/next_state` (`:403-408`).

New PREARCH record uses `operation{EVIDENCE_REVIEWED→EVIDENCE_REVIEWED}` +
`producer_boundary{CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED}` + `kind/reason/checkpoints/artifacts/...`
(R2 §§3/9.7), not top-level `from_state`/`to_state`. Blindly adding `if kind==new` to the old file
fails: without relaxing `required from/to`, the new record is schema-invalid; relaxing weakens all
old authority; forging `from/to=CANDIDATES→EVIDENCE` contradicts truthful same-State operation
(decision §5 forbids forged execution report); asserting `EVIDENCE→EVIDENCE` matches no `stage_plan`
producer (`_producer_for_checkpoint` returns `NONE` → “has no lifecycle producer”) and fails the
`CORE_STAGE_CONTRACT` lifecycle match unless bypassed.

**Concrete choice (ROOT-preferred, condition holds): exact kind-based loader dispatch to standalone
NEW strict CheckpointSchema, old file UNCHANGED.** All 17 direct schema sites have `repo_root+path`
and can call a pure file loader without State; validators call after facade State validation.
No `oneOf` legacy+new with local refs (would duplicate diverging schema and weaken old strictness).
No caller flags / verified dicts; strict `kind` match, unknown refuses, no `.get(kind,legacy)` fallback,
no raw `record["kind"]` mutation.

Shared loader (LOW, pure): `load_typed_checkpoint_record(repo_root, path) → {family, record}` —
strict duplicate-key parse → `kind` absent ⇒ validate old schema; `kind==PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`
⇒ validate new schema; else refuse. Old file byte-identical; new file is additive
`schemas/dm022-supersession-checkpoint-v2.schema.json` (R2 §9.7 literal).

Affected calls that MUST migrate from direct `CHECKPOINT_SCHEMA` loads to the shared loader
(all `file:line` are proof-copy; each needs code change before code gate closes, not “future TBD”):

- `survey_agent_control_v2.py:42` const + `:489` record load + `:819` second load + `:1011` pending
  validation + `:1532` revalidation prior + `:1758` validate_instance + `:1774` load_and_validate +
  `:1971` basis checkpoint + `:2397` prior.
- `survey_publication_set_v2.py:56` const + `:1213` anchor prior + `:1627` before-digest prior + `:1981` selection prior
  (single-resolver change covers all `_l_stage_path` adapters: `production._l_stage:47`,
  `stage_validation._l_stage:99`, `human_gate.resolve_gate_path:255`, `orchestrator.resolve_configured:167`).
- `survey_editorial_correction_proposal_v2.py:557` via `agent.CHECKPOINT_SCHEMA`.
- `survey_release_checkpoint_v2.py:121` validate_instance.
- `survey_stage_validation_v2.py:288` prior load.
- `survey_weekly_mechanical_refresh_v2.py:931` refresh validation checkpoint.

Validator branches (same gate): `:348` must NOT be called for PREARCH (branch before lookup);
`:365` bypass `CORE_STAGE_CONTRACT` match only inside new-kind branch (replace with
`DM022_SUPERSESSION_PROOF` + SELF + artifact re-hash); `:481` add PREARCH branch
(kind/reason/operation/producer_boundary/checkpoints/artifacts/lineage/SELF + new proof review);
`:761` add PREARCH dispatch; `:902` KEEP legacy + ADD `R4=LOW.resolve_research_authority`;
`:1608` exempt canonical path only inside new branch; `:1703` builder UNTOUCHED (new builder separate);
`:1768` + orchestrator/bridge/Gate paths REFUSE PREARCH through forward advance (HIGH single-file switch only).

## 3. Runtime / import sets (top vs function-local; acyclic per-function)

`ast` top-import observations (proof-copy; stdlib/future omitted):

- `survey_evidence_v2` top: `core, schema_gate, screening`.
- `survey_screening_v2` top: `core` ONLY.
- `survey_completeness_v2` top: `evidence, core, screening`.
- `survey_discovery_v2` top: `core, schema_gate, x_intake`.
- `survey_agent_control_v2` top: `drafting, core, publication, pubset, quality, reader_publication, surface_gate, review_attention, schema_gate` (NOT evidence/screening/agent_tool at top).
- `survey_agent_tool_v2` top: `agent_control, evidence, core, screening`.
- `survey_production_v2` top: `weekly_pipeline, pubset`.
- `survey_publication_set_v2` top: `core, schema_gate`.

Function-local (runtime-only) edges: `screening:465` → `agent`, `:480` → `agent_tool`
(`current_stage_basis_override`); `evidence:1366/1743` → `screening_mod`;
`agent:2911` → `weekly_refresh` (inside `main` only). Therefore the true chain is
`Evidence(top)→Screening(top)→Core` with agent imports lazy at runtime; whole-module cycle
claims are false. R2 §10 per-function leaf holds: LOW may import ONLY leaf symbols
(`_check_*_content`, `_validate_*_content`, `validate_evidence_card/validate_edition_view`,
`read_jsonl/validate_discovery_set`, etc.); any transitive reach to `verify_state_basis` /
`repository_commit_sha` / `resolve_*` breaks leaf and is a precise OPEN blocker.

Selected DAG: LOW top `core(shape-only: repo_local_path, sha256_file/object/bytes, json_bytes,
load_json, parse_instant, iso_utc — NEVER verify_state_basis/transition_state/repository_commit_sha)`
+ `schema_gate`; HIGH top `core, schema_gate, LOW`; all `evidence/screening/completeness/discovery/agent`
accesses function-local (LOW pure cores; HIGH `validate_agent_state` / `repository_commit_sha` for
eligibility only). FORBIDDEN: `LOW→agent`, `LOW→HIGH`, `agent→HIGH` (top), `LOW→guard coordinator`
(LOW never reads guard; HIGH checks guard). Direction: `LOW ← OwnerA ← HIGH` + `LOW ← HIGH` direct.

## 4. Exact old closures + precise successor lists (no count+6 without membership)

Old (verified final93 + renewal R3 binding `integrated-precode-r3.json`):

- P3S per-route 63 = `shared_py35 + schema22 + route3 + staged1 + style1 + recipe1`; union 66 = 63 + other route3.
  Full `shared_py35` (35), `schema22` (22), `route3_weekly/longform` (3 each), `staged1`, `style1`, `recipe1`
  are listed verbatim in `dependency-closure-map.json` (copied from R3; 35 route-independent shared,
  route3 disjoint). Do NOT recount without that membership.
- Weekly `CURRENT_CLOSURE` 29 (`survey_weekly_derivation_v2.py:28-58` incl `READER_INPUT_SCHEMA`,
  `RECEIPT_SCHEMA`, `STYLE_PATH` + pubset/editorial/current-authority + 5 editorial schemas + manuscript/Gate/
  revalidation/quality/candidate + `.latexmkrc` + 3 renewal modules + 4 renewal schemas).
- Longform `CURRENT_CLOSURE` 34 (`survey_longform_generated_v2.py:52-87` incl longform reader/receipt +
  semantic-review/Gate + surface_gate + production/schema + same editorial/manuscript/quality/candidate set +
  `.latexmkrc` + same 3+4 renewal files).
- Config `pipeline71` = verified `config/survey-production-v2.json` `contract_files.pipeline` len 71
  (67 base + 4 versioned-renewal new; ordered list ends with stage-checkpoint/review-finding/repair-set +
  4 renewal schemas); `implicit3` = `config/survey-production-v2.json`,
  `schemas/survey-production-profile.schema.json`, `schemas/survey-production-state.schema.json`;
  `quality3` = 3 historical docs; `control_roots` = `[config,schemas,scripts,.github/workflows]`.

Successor (transitive consumer analysis incl guard/complete readback included):

- P3S replay inputs: file membership UNCHANGED 63/66 (DM022 adds no staged replay inputs). Code closure
  ADDS 2 modules + 5 required schemas as recognized historical SOURCE refs for history/retention walkers
  (`verify_versioned_history`, `load_renewal_accepted_authority`, publication groups accept PREARCH for
  evidence/materiality/completeness; Freeze/Release via State-bound selection). No new shared helper file;
  reuse via function-local extraction + wrapper delegation (R2 §4 narrow cores verbatim); LOW header must
  enumerate exact imported SYMBOLS; any duplication returns to root for single-helper decision.
- Weekly29 / LF34: file membership UNCHANGED for rendering; derivation logic ADDS LOW R4 resolver branch
  + guard/completion predicate (code_deps, not closure expansion). Refusing old singleton fallback is part of the branch.
- Pipeline: 71 + 5 required = 76 (77 iff root registers optional receipt); `control_roots` UNCHANGED.
  Registration is root decision. `implicit3`/`quality3` UNCHANGED. Guard file is transient coordination,
  NOT pipeline/control/closure membership; completion receipt is readback predicate, NOT live selector.
- Distinguish: normal `code_deps` (above imports) vs current `controls` (pipeline/quality/roots/
  `contract_identity`/`implementation_sha`/STATE_SCHEMA/stage_plan) vs `schemas/$ref` data
  (local `#/$defs/*` only, no remote fetch, no cross-file cycle) vs historical `SOURCE` roles
  (renewal + new `dm022-*` refs as retained/COPY lineage for P2R/history/publication walkers —
  HIST descriptive, reload-by-path every use, never permission; old canonical Ledger/Completeness stay
  history-only after adoption, never fallback).

## 5. Fingerprints: old format vs new semantic branch

Old: `stage-checkpoint` required `from_state/to_state` + `checkpoints[]` + `artifacts namedAuthority`
per-`from_state` branch + `reviews contains CORE_STAGE_CONTRACT DETERMINISTIC PASS` + `result artifactAuthority`
+ 8-field `contract` + `gitsha` implementation. New branch: `kind=PREARCH…/reason=REVIEWED…` +
`operation EVIDENCE→EVIDENCE` + `producer_boundary CANDIDATES→EVIDENCE` + same 3 checkpoints + same 4 names
at versioned `R/` paths + `reviews` sole `{DM022_SUPERSESSION_PROOF, DETERMINISTIC, PASS, result=SizedRef==proof}`
(no `CORE_STAGE_CONTRACT` row, no `AGENT_RESEARCH` decision row — decision is separate `SizedRef`) +
`before_state/before_checkpoint/parent/anchor/supersedes/revision_id/R/request/retention_plan/proof/decision/report/contract/implementation/profile/executor/recorded_at/SELF-excluded digest`.
Mixed triplet (not same file / kinds differ) refuses; canonical-filename fallback after adoption refuses.
Digests: `revision_proof_sha256/preadoption_report_sha256/supersession_checkpoint_sha256 = sha256_object(body-minus-self)`;
FILE SHA `sha256_file` distinct; every `SizedRef` re-hashed; `mechanical_projections[]` lists exact schema
field paths with old/new SHAs, no directory-prefix exclusion.

## 6. HEAD/tree closure (normalized known inputs; no prospective SelfRef)

Exact commands (read-only, no execution here): `git -C <repo_root> rev-parse HEAD`,
`rev-parse HEAD^{tree}`, `status --porcelain=v1 --untracked-files=no` (tracked dirt only),
`diff --raw HEAD` (mode+sha both sides); `--ignore-submodules` mode MUST be stated
(`none` for eligibility, `all` is scoped carryover only). No `R/**` wildcard, no
`orchestration/v2/**` wildcard, no gitlink eligibility (55 bare links never enter
`contract_identity`/`implementation_sha`). Normalized known inputs: request carries
`expected_head/tree/contract/tool_shas/profile/source pins`; guard `work{head,tree}`; pin sets
`B` + Profile + current 4 artifacts + 7 slot observations at pin time. No prospective
`ToolCommitSelfRef`: checkpoint/report carry observations of already-existing files only;
artifact-only descendant admissible ONLY if `diff-tree --no-commit-id --name-only` subset of finite
declared `R` output+review+retention relpaths + linear descendant of `expected_head` + no merge +
pins/controls identical; otherwise refuse + NEW bounded attempt. Checkpoint NEVER embeds future commit
SHA, NEVER references POST receipt; proof NEVER references checkpoint (one-way SHA DAG
`before→M→D→P→RPT→CP→State→POST-receipt`).

## 7. Plan diff / register matrix + loader adaptations (each required before code)

New files: 2 modules + 5 required + 1 optional (above). Modified: `survey_agent_control_v2.py`
(Owner-A branch). Behaviour-modified: 30 DIRECT-site rows per `inventory-r2.json`
(R4-resolve or explicit refuse + `G` guard + `K` kind per row; 7-path preflight incl audit).
Registers: pipeline 71→76 (77) + roots unchanged + `contract_identity` recomputed on new disk
(old State contract stays historical). Schema-owner binding still OPEN: strict branch text for
`EVIDENCE→EVIDENCE` + `producer_boundary` + same-triplet + new-report; `check_id`
`DM022_SUPERSESSION_PROOF`; `contract_identity`/`repository_commit_sha` pin placement.

Loader adaptations (PATHS-only, no caller dicts/flags): `LOW.load_typed_checkpoint_record`,
`LOW.resolve_research_authority`, `LOW._resolve_research_from_state_bytes` (structural only),
`LOW._load_typed_four_refs`, Owner-A `_validate_checkpoint_record` / `_validate_core_stage_report`
branches (no recursion), `pubset.resolve_stage_artifact_path` single-resolver PREARCH recognition,
HIGH `prepare/adopt/resume/readback` + exclusive writers (never `core.write_json`/`copy2`/`is_file`
for guard/State/slot authority), C `require_no_active_guard(source_root)` at every mutating entry +
before-publish, `require_completion_consistent` after release (expectedAfter is baseline, not LIVE equality).

B2/B4 + audit-slot writer/ownership + HEAD/tree/C IO oracles remain pre-code OPEN.
Next: root integration. Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN.
