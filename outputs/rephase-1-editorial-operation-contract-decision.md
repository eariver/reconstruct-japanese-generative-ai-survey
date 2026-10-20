# R3 editorial operation contract — immutable publication set / explicit activation

2026-10-20. Astra author-side architecture decision, subject to the fresh independent design review linked from the packet. Scope is **contract and implementation selection**, not executed correction/adoption. Actual source: detached409/tree8ce +22 at `/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60`. Human reconstruct HEAD1442468; no source edits/tests/builds in this unit.

**Select V: prepare a complete immutable publication set, receive external reviews, then activate it through the existing `publication_revalidation_provenance` State pointer.** Profile, original checkpoints, original canonical publication, and old unadopted Candidate remain intact. Candidate is finalized **before** activation and remains at its versioned path. This document overrides contradictory proposals in [Worker analyses](../notes/rephase-1-editorial-operation-contract/README.md); their prose is not a parallel implementation specification.

## 1. Objective, supported operation and exclusions

Support a meaningful **post-VALIDATED_DRAFT / pre-Preview reader correction** on initial generated Weekly and THEMATIC/LONGFORM_SPECIAL, including a second correction while Preview is still pending. Preserve accepted research/Architecture/Draft, exact original/proposed reader identities, existing independent review and two Human Gates. The operator finishes at a healthy active Candidate ready for the normal Preview→Freeze→Release sequence. No invalid-live interval while the reviewer works.

V is selected over canonical live replacement because both require consumer/receipt changes, while canonical replacement additionally needs multi-file replacement, retained mutable publication bytes and recovery across an asynchronous review interval. V adds active-path resolution and retained-set storage; those costs are real. This is qualitative prioritization, not measured optimality. Old P1/P2R/P2V/P3S investment alone is not a reason to retain unnecessary work.

Limits of this selected increment:

- Same **current contract/tool epoch** only. Existing old-epoch P3S manifests are not automatically migrated/reblessed. New implementation fixtures must commit actual implementation/contract source **before** producing authorities.
- Longform authored revision and Weekly envelope-only semantics remain governed by P1. Accepted Draft-body edits and accepted-upstream changes are refused. DM022 pre-Architecture supersession remains separate and OPEN.
- Existing R1 mechanical refresh **before** a correction is supported (including two refresh records). Existing canonical mechanical refresh/revalidation **after** versioned activation must refuse before writes. Versioned mechanical renewal is not selected here; the usability loss and necessary readiness disposition are explicit in §10. No all-R3/whole completion claim.
- Preview approved/request-changed, Freeze/Release decided, exception active, invalid/foreign authority: refuse this operation. No State rewind, Profile rebind, canonical-copy fallback, new Human Gate or generic supersession engine.

## 2. Paths and immutable inputs — no duplicate reviewed targets

Let `P` be the actual existing P1 proposal directory, verified from retained/current Profile as appropriate:
`<source_root>/publication/v2/editorial-corrections/<proposal_id>`.

Keep exact existing `P/proposal.json`, `P/authoring-input.json`, `P/reader-surface-input-v2.json`; keep P2R retained files at their **recorded refs** (do not assume a newly invented retention-manifest location); keep P3S closed4 `P/staged-source/{main.tex,references.bib,jgaisurvey.sty,staged-source-manifest.json}`. Read the exact early scope-review path from the staged manifest's `scope_review_ref`; no forced rename/copy.

Add **one** sibling `P/publication/`:

| Artifact | Exact output |
|---|---|
| real transferred outputs | `build/main.pdf`, `build/main.log`, `build/main.pdf.sha256` |
| build provenance | `build-record.json` (declared source trio/recipe/toolchain/argv/environment/results/output refs; excludes itself from digest inputs) |
| manuscript | `reader-manuscript-v2.json` |
| new receipt | `validated-source-manifest.json` |
| QA bundle / Gate | `quality-regression-bundle-v2.json`, `reader-surface-gate-v2.json` |
| Candidate | `publication-candidate-v2.json` |
| final immutable seal | `publication-set.json` |

Primary source/Bib/style remain the **existing P3S staged trio**, not copies in `publication/outputs/`. Early review remains bound to the **original proposed reader**. New semantic/visual records are supplied at their final repo-contained immutable paths; recommended `P/publication/reviews/`, but their exact supplied refs are retained without relocation. Their result dependencies are explicitly enumerated from validated schemas, not found by a generic path scan. No symlinks/latest/mtime authority.

Writers claim new output paths exclusively, refuse any pre-existing conflicting or same-byte target, preserve incomplete outputs, and never delete foreign/unknown files. The staged4 and build3 inventories stay separate. The publication inventory consists of the named outputs plus schema-declared external review/QA result refs actually inside that namespace. Build auxiliaries remain outside it. External files outside the publication namespace are pinned dependencies, not writer-owned files.

## 3. Three review responsibilities and a constructible order

1. Existing P1 proposed-reader derivation → P2R retention → externally supplied early semantic/correction-scope review → P2V `SCOPE_BOUND` → P3S source. Neither P1 public validation after capture nor P2V after activation is used as a bypass.
2. **Prepare publication:** reverify staged proof/current-before; build the exact trio in a disposable build root using an explicitly selected executable/toolchain and the fixed recipe (no caller shell string). Record real exit/log and tool versions/digests where available. Verify inputs unchanged; exclusively transfer PDF/log/digest to build3; emit build record, new receipt and exact manuscript with supplied coverage/requirement author assertions. No semantic/visual PASS is authored by this operation.
3. **External review interval:** manuscript and PDF already exist at final paths. Existing independent semantic/editorial and visual roles inspect those exact bytes and supply persisted records; deterministic QA inputs/results also arrive explicitly. No runtime can infer genuine reasoning from schema-valid PASS. Reviewer provenance/independence and Human authority remain operational evidence, with synthetic tests visibly separate. No new signature or automatic synthetic-detection scheme is introduced.
4. **Finalize set:** validate external records and exact cross-bindings, assemble QA, build/validate Gate using **early proposed-reader scope review** (not postrender semantic record), build/validate the versioned Candidate, then write `publication-set.json` last. The set is still inert.
5. **Activate:** full current-before and complete-set checks, create immutable activation record, then guarded State pointer replacement only. Normal current validators and normal Candidate→Preview→Freeze/Release consumers resolve this set.

The recipe does not require bitwise reproducible PDFs. It binds the actual successful build input/output bytes, tool/recipe evidence, required deterministic predicates and exact postrender review. A failed build never produces an admissible set. Placeholder real-build fixtures remain insufficient for production quality.

## 4. Exact authority shapes and DAG

All new records use strict objects (`additionalProperties:false`), duplicate-key refusal and exact lowercase SHA256/commit formats. `ref={path,sha256}`, `file_ref={path,sha256,byte_count}`. Dates are validated instants. Any repeated identity field must agree, never establish a competing authority.

### 4.1 Manifest and editorial receipt

Add optional `editorial_source={proposal_ref,staged_manifest_ref}` to the Reader Manuscript schema/builder. Absence retains the canonical primary-root rule unchanged. Presence requires a verified P3S source proof: same issue/Profile/Architecture/approval, exact original proposal namespace, actual staged manifest and exact staged primary/Bib/style refs. Reader `:218` therefore **changes**; existence/hash of an arbitrary staged manifest is insufficient. Full staged verification calls the existing `verify_staged_source(root,proposal_path,staged_manifest_path)` (historical P2R/scope/replay), not P2V or a future seal. Existing coverage/fidelity/leakage rules remain.

Select a new strict receipt kind `EDITORIAL_PUBLICATION_SOURCE_V1` (schema `editorial-publication-source-manifest-v2.schema.json`), rather than relaxing old canonical receipt namespaces. Exact keys: `schema_version,kind,issue_id,research_profile,publication_profile,generator_route,proposal_ref,retention_manifest_ref,staged_manifest_ref,scope_review_ref,reviewed_reader_input,authored_refs,accepted_refs,current_tools,outputs,receipt_sha256`. Generator route is the existing Weekly or Longform route; authored refs retain distinct proposed publication-authoring and accepted Draft archive roles. Outputs are exactly the three staged refs. `receipt_sha256` hashes the canonical object without itself.

Receipt validation independently reloads the exact early scope review; verifies P2R/P3S historical replay; rederives the proposed reader from the **new proposed authoring plus unchanged accepted Draft**; compares canonical reader FILE bytes and all rendered output bytes; verifies current contract/tool closure and actual current accepted research via strict current State plus ordinary route loaders. It never requires current State to remain equal to the old before-State hash. For an inert set, current State still selects old publication and is healthy; after activation it selects the new set and is healthy. A private historical proof path does not claim current eligibility. No `seal_path` is required to validate a receipt or a manuscript.

Gate gains a strict editorial derivation branch bound to this receipt, original proposed-reader ref, exact scope review and exact staged trio/manuscript. Gate schema/loader/CLI are changed together. Existing old receipt branches remain strict. No generic `active_set`/verified-dict/pending boolean from a caller grants permission.

### 4.2 Publication set seal

Schema `editorial-publication-set-v2.schema.json`. Exact top-level keys: `schema_version,kind,status,issue_id,research_profile,publication_profile,proposal_ref,staged_manifest_ref,build_record_ref,roles,set_sha256`. Kind `EDITORIAL_PUBLICATION_SET_V1`; status `SEALED_INERT`. `set_sha256` hashes the canonical object excluding itself.

The **one selection table** `roles` has exactly these15 keys (file_ref values):
`reader-input, authoring-input, source-receipt, reader-manuscript, validated-source, bibliography, style, publication-pdf, build-log, pdf-digest, quality-regression-bundle, semantic-review, visual-review, reader-surface-gate, publication-candidate`.

Each path is checked against §2, the exact proposal/staged refs or the supplied immutable review ref. Source, manuscript, bundle, reviews, Gate, Candidate and build record must agree on all shared paths/SHA/bytes/page-counts. Existing leaf records necessarily contain their own dependency refs; those are checked against the selection table, not alternate active maps. QA result refs are also validated/pinned through the bundle. Seal stores no activation-record hash, before-State copy, arbitrary root or duplicated `external_reviews` map.

### 4.3 Activation record and legacy branch

Refactor `publication-surface-revalidation.schema.json` into **two fully strict branches**. Preserve the complete existing legacy object/required-fields/additionalProperties semantics verbatim in branch1 (`reason_class=REVIEWED_CORE_CHANGE`), not a top-level required-list that accidentally applies to branch2. Branch2 exact keys:
`schema_version,kind,issue_id,reason_class,reason,lifecycle,prior_checkpoint,supersedes,canonical_anchor,before_state_ref,before_active_digest,before_candidate_ref,set_ref,core,executor,recorded_at,establishment`.

`kind=EDITORIAL_PUBLICATION_ACTIVATION_V1`, reason class `REVIEWED_EDITORIAL_CORRECTION`, lifecycle `VALIDATED_DRAFT`; `prior_checkpoint` original validation ref; `supersedes` exact previous revalidation/activation ref or null; `canonical_anchor={kind,ref}` where kind is `VALIDATION_CHECKPOINT` or `LEGACY_REVALIDATION`; `before_candidate_ref` nullable ref; `set_ref` exact seal ref. `before_state_ref` records expected prior State path/hash as establishment provenance, not live-hash equality after activation. `core` and `establishment` retain existing exact contract/implementation and predecision sanctions. `before_active_digest` is canonical SHA of sorted **effective seven publication checkpoint rows plus exact observed Candidate ref/null** at activation entry. No fake legacy superseded/preserved rows, no second active-role table.

Record path keeps existing sequence naming under canonical publication/v2. `supersedes` is the common chain edge for both branches. Same issue/original checkpoint, strictly increasing numeric sequence, nondecreasing valid timestamps, no cycles/duplicate links, bounded depth32; missing or unknown branch refuses. New activation requires canonical record path; preserve existing legacy validation policy for old records. No “reason-only” admission through the existing revalidation writer.

Activation's `before_state_ref` must equal the bound proposal's basis State ref and the P2R retained COPY of those exact bytes; `supersedes`/before-Candidate/digest must agree with both retained-before derivation and freshly observed current-before. Historical validation reads the retained State copy, never expects the old hash at the now-updated live State path. The equality remains mandatory on explicit orphan-record resume.

DAG: proposal/retention/early scope → staged proof → receipt/manuscript + build → external reviews/QA → Gate → Candidate → seal → activation record → State. No leaf depends on seal/activation; Gate requires receipt **before** itself. Public proof APIs distinguish inert validity, historical validity and current active selection.

## 5. Canonical anchor, historical proof and active projection

Actual legacy rows are **cumulative against the original validation checkpoint**, not incremental old→new edits. Do not roll forward `prior_sha256` as if each legacy record were based on its predecessor's live SHA.

- With no legacy revalidation before first activation, canonical anchor is original validation checkpoint.
- Otherwise it is the **latest legacy record immediately preceding the first activation**. Validate each legacy link's original-checkpoint union under its own legacy semantics. Its cumulative effective rows define the preserved canonical bytes. Recorded anchor must equal this chain-derived identity.
- Repeated activations retain that same anchor. Legacy writer after an activation is refused in this increment; a mixed chain containing a later legacy successor is unsupported and fails closed, not canonical fallback.
- Historical checkpoint/report identities/implementation/contract and unchanged research are still verified. For the original validation checkpoint, materialized canonical publication files are checked against the anchor's effective rows. New active set refs are checked **separately**. Older superseded legacy hashes remain historical provenance/retained evidence as under the original contract; do not claim every original SHA is still present canonically.
- Exactly the seven publication roles of that validation checkpoint may project to active seal roles. No research/Architecture/Draft role can be rebound. `resolve_checkpoint_artifact(validation,role)` and stage `_prior_artifacts` return the active projection only after historical and active identity checks; raw historical inspection remains available separately. Other checkpoint roles retain their own semantics. Both old-byte drift and new-set drift refuse.
- The versioned Candidate is a seal role outside the original seven-row union. Normal VALIDATED_DRAFT checkpoint accepts only that selected Candidate path/hash. Later Preview approval and checkpoint provenance still agree exactly. Freeze/Manifest/merge/release/approval output paths remain canonical stable control artifacts; their source/PDF/Candidate refs point to the active set.

Repeated-correction retention changes P1 classification explicitly: prior immutable versioned publication/staged/proposal/seal/Candidate bytes are `KEEP_IMMUTABLE`; mutable live State remains COPY, and mutable non-versioned control inputs retain their actual policy. First canonical before-graph keeps existing conservative P1/P2R capture. This is required new behavior, not a claim about current P1. All KEEP refs remain byte-checked; immutability is an operating rule plus detection, not filesystem magic.

## 6. Dependency layers and public operation interfaces

Select a small **integrated** implementation, not a detached verifier:

- `survey_publication_set_v2.py`: low-level branch/chain/anchor/seal identity and active-role selection. May use core safe path/hash/schema primitives, but **must not call** agent/Stage/Gate/receipt/Reader/P1/P2R/P3S validators. Core State calls it via local import; no top-level import cycle. It validates all selected file refs, allowed role/path structure, seal/record binding and historical anchor. It does not claim semantic replay.
- `survey_editorial_publication_v2.py`: prepare/build/finalize/full set verification/activation and CLI. Calls the existing P2R/P3S proof, Reader/QA/Gate/Candidate APIs and P2V before-eligibility. Source-proof entry used by Reader/receipt must not call seal or current activation. Keep explicit call graph boundaries despite shared file; no import-time execution.

`validate_agent_state` uses low-level identity plus existing checkpoint/report/Human agreement. Full receipt validation may call strict State and route research loaders; those terminate through identity resolution and do not recurse into full receipt/Gate. P3S historical scope uses the existing narrow Session adapter/review loader, not full current P1/P2V. Actual import graph is a mandatory pre-code return and reviewed test boundary.

Public signatures (path arguments repo-contained unless stated build tooling), no caller-verified objects:

```
prepare_publication(root, state_path, proposal_path, staged_manifest_path,
                    manuscript_spec_path, toolchain_spec_path, recorded_at) -> prepared_paths
finalize_publication(root, state_path, proposal_path, staged_manifest_path,
                     deterministic_checks_path, semantic_review_path,
                     visual_review_path, recorded_at) -> set_ref
validate_editorial_receipt(root, receipt_path, state_path) -> receipt
validate_prepared_set(root, state_path, set_path) -> validated_set
activate_publication(root, state_path, set_path, reason, executor, recorded_at) -> result
resume_activation(root, state_path, record_path) -> result
verify_activation_history(root, record_path) -> historical_result
resolve_publication_selection(root, cfg, state) -> identity_selection
```

Prepare consumes an existing valid P3S set and its referenced scope/retention. It derives final paths, invokes real build and public source-proof/manuscript construction; it does not regenerate P1 after retention or invent review. `manuscript_spec` contains only existing coverage/requirement assertions/author/time inputs, not caller source/profile overrides. `toolchain_spec` is executor configuration (absolute executable, declared fixed recipe/options/env), **not approval**; required argv, versions and actual outputs are recorded. Review APIs remain the existing reviewer-owned record creation workflow; this operation accepts persisted files only. Deterministic-check inputs use existing `quality.validate_checks` contract with actual evidence results; no automatic family PASS by schema.

Finalize rechecks current-before scope and all input pins before writes, constructs deterministic wrapper artifacts and Candidate from validated inputs, writes seal last. `validate_prepared_set` needs no active record for that set but verifies current research/tool requirements and full leaf bindings; returns no permission token. Activation rederives everything from supplied paths.

## 7. Activation / failure / resume contract

Activation requires fresh in-invocation P2V SCOPE_BOUND of the original proposal, complete full set validation, exact current State bytes, same predecessor/current contract/tool scope, valid original/active-before Candidate, and current predecision eligibility. Repeat relevant stable pin checks immediately before the first record write and immediately before State replace. Original proposed scope cannot be reused after before-State or accepted research changed.

Healthy old Candidate (if present) must validate and exactly bind active-before artifacts with pending Preview and no decision/provenance; P1 retention includes it. Invalid/missing referenced/foreign/unknown approval is an error, not absence. After activation old canonical Candidate is deliberately inactive and remains pinned historical input; repeated P1 observation selects active versioned Candidate, not stale canonical bytes.

Only write: new exclusive activation record, then known-byte State temp+replace updating **only** `publication_revalidation_provenance`. No canonical Candidate/source/QA rewrite. New State validates selected set and normal stage/Preview path before success. Old canonical readers are no longer permitted as active consumers; UI/export/orchestration use §8 resolution.

| Failure point | Preserved authority / permitted next action |
|---|---|
| prepare/build/review/finalize incomplete | old State healthy; incomplete publication dir inert and preserved. Use new proposal ID for a new attempt; no same-byte takeover or automatic cleanup |
| seal complete, before activation | explicit activation can be retried; recheck full current-before and all inputs. Seal is not permission |
| record created, State still exact old | record inert. `resume_activation` explicitly revalidates full current-before/set/record intent and may install that exact record; ordinary activate refuses collision |
| State already exact new pointer | validate strict active State and full set; return `ALREADY_ACTIVE` read-only, not ownership takeover or a fresh approval |
| State neither known old nor expected new, unreadable or unsafe | preserve all bytes, `INDETERMINATE`; no automated overwrite/rollback/adoption |
| close/postreplace validation failure | report primary plus secondary errors and observed old/new/unknown disposition. Never delete referenced/possibly referenced record. Recovery is explicit, not success inferred from file presence |

No multi-file atomicity/globalCAS/power-loss guarantee. Existing single-writer/operator assumption must be explicit; boundary guards are not atomic CAS. Writers use held/no-follow ownership where implemented; any remaining window is disclosed and fault-tested. Resume proves current consistency/eligibility, not original creator identity. It does not authorize post-Preview correction or manual State rollback.

## 8. Concrete consumer/closure changes required in the same implementation unit

Root reviewed principal source constraints; read-only Explore audited scripts/config/workflows. The finite implementation surface below is a requirement, not a file-count ceiling. No release-ready assertion until every listed consumer is active-aware or explicitly refuses revised mode.

| Source surface | Required change |
|---|---|
| revalidation schema + agent `_resolve_*`, `_check_immutable_revalidation_rows`, `_check_revalidation_chain`, `_validate_checkpoint_record`, `_resolve_checkpoint_artifact`, `_validate_agent_state` | strict branch/anchor/active projection from §§4–6; legacy writer cannot emit editorial authority |
| Reader schema + `_validate_manifest_semantics:207–219`, `build_manuscript_manifest` | editorial_source proof branch; existing fidelity/coverage/lint retained |
| new receipt schema/validator + existing Weekly/Longform receipt dispatch and Gate schema/`_derivation_for_manuscript`/builder/CLI | editor-specific proof/current research/tool replay; early review binding; old canonical receipt constraints retained |
| `survey_stage_validation_v2._prior_artifacts`, VALIDATED/RELEASE_CANDIDATE semantic checks; agent `_validate_stage_artifacts` | active publication roles/Candidate; canonical original checkpoint templates are historical, not rewritten |
| `survey_production_v2.validate_state_semantics:784–809`, agent `approve_publication_preview:1479`, `survey_profiled_freeze_v2.build_profiled_freeze:58` | remove canonical Candidate assumption in revised mode; exact active Candidate; preserve canonical approval/Freeze/Manifest outputs |
| config gate input/publication-candidate template (`:225,:356`), orchestrator `_configured_expected_artifacts/_configured_gate_inputs`, handoff `expected_output_contract`, human_gate `_expand_gate_path/_reviewed_artifacts` | introduce **one role-aware path resolver** with State argument. Fixed DRAFT templates unchanged; publication-candidate token derives active candidate or canonical default. Recompute and compare in loaders, not only producers |
| preview export workflow trigger/discovery/manual input | watch State activation and versioned Candidate paths; choose exact State-bound Candidate, fail on ambiguous/mismatched input. Do not export an inert set merely because its file changed |
| release workflow/checkpoint/generic Candidate/QA/Freeze builders | explicit refs largely already work; verify via actual integration. Stable canonical Manifest path and Freeze's Candidate ref stay; no automatic edit of generic code |
| P1 `_active_effective`, full pipeline/receipt recheck, before graph/retention plan/Candidate observation; P2V caller | support canonical and active-set before graphs, repeat correction; no current-before call after activation |
| P2R/P3S | keep historical namespace/source-proof semantics and public P1 destination conflict. Update exact actual import/schema closure for new dependencies, not a silent unchanged37 claim |
| canonical revalidation/R1 refresh, interactive revision wrapper, semantic-quality canonical writer, canonical Weekly/Special build workflows | revised-mode refusal **before destructive action/output/guard creation** unless explicitly routed through new operation. Initial publishers already DRAFT_COMPLETE-only: preserve that guard and verify revised refusal |
| config contract-files, receipt CURRENT_CLOSUREs, P3S fixed deps, CLI command registration/docs | register every new authority-bearing module/schema and affected transitive consumer. Commit complete implementation source before authority fixtures; no implicit old-epoch acceptance |

New schemas selected: editorial receipt, publication set, build-record, manuscript-spec and toolchain-spec as needed for the public prepare boundary; reuse typed existing structures instead of opaque arbitrary dictionaries. Exact schema-file names for the latter three and dependency enumeration are a mechanical interface return before code, not open authority-policy choices. A publicly exposed command must not depend on a fixture-only driver. No new generalized resolver for non-publication domains.

## 9. Implementation task and decisive verification

After this contract's independent review and the next Human continuation, General returns a concrete module/import/schema/CLI/write-set map satisfying this decision, then implements **the whole selected two-route prepare→review-input→finalize→activate→normal consumer operation**, with root review before execution. No detached helper-only completion. A path-count limit is not imposed; unexpected unrelated defects return for scope choice.

Fixture order: fresh independent Git with actual complete new source/contract (meaningful source commit) → actual accepted research/Architecture/Draft and initial publication authority → P1 proposal/retention/early scope/P3S → new preparation/build → separately labelled supplied review fixtures → seal/activation. No F0 receipt that contains F0's yet-unknown SHA. “Current epoch” means tool/contract/receipt/basis consistency, not calendar recency. Genuine author-independent inspection is separate from synthetic type fixtures; production semantic NO-GO is not laundered.

Required success oracles: both initial routes unchanged; changed-reader correction reaches healthy active Candidate and normal synthetic Preview/Freeze/Release using real PDF; old canonical files and old Candidate stay byte-identical; exact proposed early-review path retained; second pre-Preview correction works; legacy R1×2→correction uses correct cumulative canonical anchor; active vs historical readback remain distinct; artifact-only commits only under actual closure predicates. New meaningful source build when source/tool inputs change; no decorative full old-suite reruns.

Required negatives: same-issue wrong seal/manuscript/Candidate; old canonical Candidate supplied after activation; inert valid set not adopted; unconsumed or unknown record branch; research ref change; old authored/new reader inconsistency; equal-SHA different reviewed path; stale/failed/missing external reviews; build failure/extra input/output/hash drift; seal missing role/unknown ref/duplicated role; legacy-anchor error/cycle/depth/sequence; State/predecessor drift; approved/foreign Candidate; canonical writer after activation; every record/State write/close/late-readback failure classified with immediate observed delta and explicit resume/healthy control. Test public callers, not merely standalone validation or earlier unintended refusal.

Closure/regressions: exact staged/receipt/current contract dependency changes, Reader/Gate/State/stage/Preview/Freeze/export path handlers, affected R1 initial-mode guard, P1/P2R/P2V/P3S repeat behavior. Correct failures and rebind exact source. Independent implementation review and eventual whole-candidate audit remain separate.

## 10. Remaining capability/quality and cost obligations

Same-reader Core-change renewal **after a revised set** remains unsupported by selected R1; it requires a distinct reviewed versioned mechanical-renewal operation or another explicitly accepted operational disposition before whole readiness. This restriction is a lost capability for revised editions, not “compatibility preserved.” Scope does not block ordinary initial R1→correction order. Do not transform a Core change into false editorial reason to bypass it.

DM022 accepted-upstream correction, DM016/017 necessary Profile readiness, representative-data semantic/visual/layout/bibliography acceptance, Retrospective/manual/direct-primary applicability, fixed candidate/audit, Human migration/adoption and net-work measurement remain on the overall roadmap. This contract does not close allR3 or DM021 by design alone.

Expected work removed: in-place publication overwrite/rollback across review wait, stale canonical Candidate replacement, duplicate copies of proposed-reader/staged trio. Added cost: typed selection/resolver consumer changes, strict new branch/closure maintenance, persistent versioned files, preflight/full replay, operator-facing explicit activation/resume, separate future mechanical-renewal cost. No numeric savings/finish-date or “smaller number of files wins” assertion. Actual code/verification time and operator attempts must be measured during implementation and later operation.

**Stop at the design work-unit Commit Point after independent review and handoff.** Source22 unchanged; code execution/implementation acceptance is not claimed. Ordinary Commit/Push and Production adoption remain Human-owned.
