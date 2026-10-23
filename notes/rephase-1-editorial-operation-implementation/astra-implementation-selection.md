# Astra implementation authorization and interface resolution

Human continuation at clean reconstruct `df635550c4683a43da731f33c90f88703e303034`; contract d880f53e unchanged. Approve implementation in `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60` ONLY. Original22 and R2 fixtures stay read-only. No candidate/reconstruct commit, Production action, reset/clean/raw deletion. Meaningful independent fixture SOURCE commits are allowed before authority generation.

The initial map and map-resolution are retained as proposals. This note resolves ownership and one material error: **old8/14/37 closure sets cannot be declared unchanged using the old source's AST while new call edges are being added.** No code acceptance follows from map headings. Both initial and revised routes must use the new source epoch; old receipts do not automatically migrate.

## 1. Disjoint authorship (shared implementation copy)

- **L:** new `scripts/survey_publication_set_v2.py`; existing revalidation schema; new publication-set schema; `scripts/survey_agent_control_v2.py`. Owns low-level identity/chain/anchor, agent integration, path-template resolution hooks, agent Preview and legacy-revalidation refusal. May add only its own low-level tests.
- **H / lead:** new `scripts/survey_editorial_publication_v2.py`; four new receipt/build-record/manuscript-spec/toolchain-spec schemas; Reader/Gate schemas and runtime; Weekly derivation/Longform derivation+generated and initial publishers if required. Owns both CURRENT_CLOSURE declarations, high-level operations/public CLI/build/receipt/Gate/Reader. `quality` generic implementation stays unless concrete need returned. Lead later integrates and owns whole-operation tests.
- **C:** core Production/stage/profiled Freeze/config/orchestrator/handoff/human Gate/export and canonical build workflows; P1/P2V/P2R/P3S; R1 mechanical refresh; interactive revision wrapper/semantic-quality canonical writer; operation documentation. Owns P3S closure/config schema registration and public role-consumer wiring. Does not edit L/H files; interface needs go to lead/root.

Workers must not edit each other's paths or commit the shared implementation. No concurrent whole-fixture executions until the combined source is frozen. Each returns exact diff/status and failures; lead integrates after all drafts arrive. Existing tests may be adapted only where the changed API legitimately requires it, preserving original failure evidence (no prohibition on justified existing-test edits merely to keep an old count).

## 2. Frozen low-level interface (L provides; H/C consume)

`resolve_publication_selection(root,cfg,state)` returns an ordinary derived value, not a bearer:
`{mode,record_ref,set_ref,canonical_anchor,canonical7,effective7,candidate_ref,candidate_path,roles}`.
Modes `CANONICAL` / `VERSIONED_ACTIVE`. `record_ref,set_ref,candidate_ref` nullable refs; anchor exact `{kind,ref}` or null before validation. `canonical7/effective7` are name→file_ref maps (empty before a validation checkpoint exists); `roles` is versioned15 or null. `candidate_path` is Path: canonical expected output when initial/no Candidate, active exact path when revised. A default output path confers no authority. All actual reads validate shape/hash/path/branch/anchor; invalid pointer never falls back.

Additional shared APIs:
`resolve_publication_artifact_path(root,cfg,state,role)->Path`,
`validate_seal(root,set_path)->dict`,
`validate_activation_record(root,record_path)->dict`,
`derive_canonical_anchor(root,cfg,state,chain)->dict`,
`before_active_digest(effective7,candidate_ref)->str`,
`assert_canonical_publication_mode(root,cfg,state)->None` (raises on revised/invalid, before writes).

L supplies a single State-aware template resolver `resolve_stage_artifact_path(root,cfg,state,profile,name,template)->Path`: names other than publication-candidate retain exact existing template behavior; candidate resolves through selection. Existing DRAFT templates remain historical/canonical. C calls this low-level API, not another independently maintained replacement table. Agent and external path readers recompute/compare.

Use actual filenames/schema refs, not source-map's mistaken counts/line guesses. Preserve legacy schema's **actual required list verbatim**, with local `$defs` references preserved under branch refactor.

## 3. Exact selected dependency extension

Retain original listed sets, with fixed sorted-unique unions (no filesystem discovery). These are deliberate finite additions; implementation import/proof review must detect any further edge and return for expansion, not silently omit it.

Common additions to both initial receipt CURRENT_CLOSUREs:

1. `scripts/survey_publication_set_v2.py`
2. `scripts/survey_editorial_publication_v2.py`
3. `scripts/survey_editorial_current_authority_v2.py`
4. `schemas/editorial-publication-source-manifest-v2.schema.json`
5. `schemas/editorial-publication-set-v2.schema.json`
6. `schemas/editorial-publication-build-record-v2.schema.json`
7. `schemas/editorial-manuscript-spec-v2.schema.json`
8. `schemas/editorial-toolchain-spec-v2.schema.json`
9. `schemas/reader-manuscript-v2.schema.json`
10. `schemas/reader-surface-gate-v2.schema.json`
11. `schemas/publication-surface-revalidation.schema.json`
12. `schemas/quality-regression-bundle-v2.schema.json` (verify actual existing QUALITY_SCHEMA name before fixing tuple; if different, report exact correction)
13. `schemas/publication-candidate-v2.schema.json`
14. `.latexmkrc`

Weekly old8 ∪ common14 → expected22; Longform old14 already includes Gate schema → expected27. Reuse existing control-roots/committed-tool verification for other existing shared consumer code; do not imply the narrow tuple is the entire source authority. New editorial receipt closure is the union of the updated P3S route closure and corresponding initial receipt tuple, with its exact count/list checked, not a claimed independent12file closure.

P3S: original27 shared Python + the3 named scripts above →30; original5 shared schemas + new5 schemas + Reader/revalidation/QA/Candidate4 →14 (Gate already present); existing route3 + staged module1 + style1 + recipe1 → expected**50**. Update exact set assertion and actual runtime binding together. Current-authority module inclusion is deliberate because the new publication path invokes it; actual transitive code proof must include dynamic paths, not only old top-level AST.

Register the5 new semantic schemas in config contract-files; do **not** add implementation scripts or config itself to contract_files indiscriminately. Implementation files stay covered by control roots/tool closure. R1 comment-only allowed Weekly source changes must leave contract identity unchanged; test that actual predicate, not a config bypass. Build recipe hash is covered explicitly.

## 4. Inputs/build and ownership clarifications

- manuscript/toolchain input specs live outside the absent writer-owned `P/publication/` root, e.g. `P/manuscript-spec.json`, `P/toolchain-spec.json`.
- Toolchain argv must match the fixed recipe allowlist; no arbitrary latexmk `-e`, shell command, output-root override or injected Git/Python root environment. Allow only required declared TeX environment keys and validate values; recipe `.latexmkrc` exact ref/hash in build record.
- `build_sha256` hashes the complete record **including input/output refs** but excluding only `build_sha256` itself. Map-resolution's “excluding outputs” is rejected; output binding is essential.
- Empty `publication/` root adoption/same-byte takeover is refused. Prepare/finalize separate phases own only their declared new outputs and tolerate only validated prescribed pre-existing inputs from prepare/external-review phases.
- Runtime never generates semantic/visual approvals. Supplied check records remain subject to exact existing schema/ref/family checks and actual independent operational review.

## 5. Implementation/proof sequence

L/H/C code drafts in parallel, then lead integrates and returns source/diff/import-closure diagnostics for root review before long fixture runs. Pure/schema meaningful checks may run locally with bytecode external/no source pollution; no broad old suites. Then fresh complete SOURCE-committed independent fixtures, initial and revised2route real build, repeated prePreview correction, R1×2 anchor/refuseafter, exact public consumer/lifecycle, fault/resume/negative matrix and required regression. Preserve every attempt, exit and assertion scope. Root retains scope decisions and final review; independent author-separated implementation review follows source fixation.
