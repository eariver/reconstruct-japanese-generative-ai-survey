# Versioned same-reader mechanical-renewal operator cases — Worker B design (DESIGN ONLY)

2026-10-23 JST. Author-side architecture Worker B. **DESIGN ONLY, no code/test/import/build/fixture/Git/network/old-runner.** Next task per `outputs/rephase-1-editorial-operation-implementation-assessment.md §5`, on selected contract `d880f53e` (`outputs/rephase-1-editorial-operation-contract-decision.md`) with R3 closeout (`notes/rephase-1-editorial-operation-implementation/astra-closeout-resolution.md` + independent final operation/packaging/authority/reader-visual resolutions).

Human reconstruct HEAD `8f77571` clean observed at root. Actual57 source read-only at `.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`; complete patch `659063dc…/2018112B` scoped 721 actual409. **This file does not read that source.** Worker A owns historical/current code bridge; Explore owns consumer inventory. Assumptions on Worker A are explicit in §9, not an unconsumed helper.

Scope: constructible OPERATOR flow for **same reader renewed versioned publication after genuine Core/tool change**, with two separately derived cases:

- **Case U**: same exact reader AND exact same source trio / manuscript / PDF reviewed targets.
- **Case C**: same exact reader but source / PDF / manuscript / output changes.

Root chooses contract + fresh review after return; no code yet.

## 0. Non-negotiable constraints (not relaxed by this design)

1. **Reader identity is entire canonical complete IR + exact existing reviewed path**, not headline/prose only. `reader-input` role = exact `P/reader-surface-input-v2.json` bytes at its recorded path; Gate/Candidate/seal bind `path+SHA+byte_count` (+ `page_count` where PDF-bound). Same-SHA different-path is refused (R6 cross-binding fix, preserved).
2. **Current P1 rejects identical reader; R1 refuses revised mode.** Do not fake an editorial reason, do not relax old public `P1 NO_EDITORIAL_CHANGE` / no-change predicate, do not rebind an unchanged receipt, do not run existing R1 against revised activation. R6 proves `refusal-r1-after.txt` / `refusal-canon-after.txt` / `refusal-fake-after.txt` rc=2 `refused in VERSIONED_ACTIVE (versioned renewal unselected §10; no editorial-reason bypass)`. This design truthfully records a **reviewed Core/tool change** under a new strict branch, it does not transform a Core change into editorial reason.
3. **No generic automated Human approval.** External semantic/visual/QA are supplied persisted records, validated strictly; runtime never infers genuine reasoning from schema-valid PASS. Production semantic NO-GO, synthetic placeholder, DM022 / all-profile / representative-quality / audit remain OPEN.
4. **Code commit before authority.** Any implementation must commit complete actual implementation/contract source (meaningful source commit) before producing authorities. No `F0` receipt containing `F0`'s yet-unknown SHA; "current epoch" = tool/contract/receipt/basis consistency, not calendar recency.
5. **No unmeasured saving/date claim.** Operator cost removed/added is qualitative (§10); no numeric savings/finish-date.

## 1. Namespace and paths — renewal root vs P, old sibling

Reference (d880 §2, unchanged): let `P = <source_root>/publication/v2/editorial-corrections/<proposal_id>`.

- Keep exact `P/proposal.json`, `P/authoring-input.json`, `P/reader-surface-input-v2.json`.
- Keep P2R retained files at **recorded refs** (no invented retention-manifest location).
- Keep P3S closed4 `P/staged-source/{main.tex,references.bib,jgaisurvey.sty,staged-source-manifest.json}` + exact `scope_review_ref` from staged manifest; no forced rename/copy.
- Old selected set lives at sibling `P/publication/` (`build/main.pdf`, `build/main.log`, `build/main.pdf.sha256`, `build-record.json`, `reader-manuscript-v2.json`, `validated-source-manifest.json`, `quality-regression-bundle-v2.json`, `reader-surface-gate-v2.json`, `publication-candidate-v2.json`, `publication-set.json` = seal LAST). Staged4 and build3 inventories stay separate; publication inventory = named outputs + schema-declared external/QA refs actually inside namespace.

### 1.1 Options compared on actual P1/P2R/P3S path constraints

| Option | Shape | Verdict |
|---|---|---|
| N0 mutate old `P/publication/` in place | Rewrites closed inventory, breaks KEEP_IMMUTABLE, breaks seal `set_ref` pins, breaks before/after readback distinction | **Refused.** Violates d880 §2 writer exclusivity + §5 retained-set storage. |
| N1 new renewal root `P/renewals/<renewal_id>/` as sibling to `P/publication/` | `P`, P2R refs, P3S closed4, old `P/publication/` all untouched; renewal has own `build/`, `reader-manuscript-renewal-v2.json`, `renewal-source-manifest-v2.json`, `quality-regression-bundle-renewal-v2.json`, `reader-surface-gate-renewal-v2.json`, `publication-candidate-renewal-v2.json`, `publication-set-renewal-v2.json`; early reader path not relocated | **Selected.** Preserves P1 `_active_effective` / before-graph / retention plan (which keys off `P` + retained COPY vs KEEP), preserves P2R historical namespace, preserves P3S `verify_staged_source(root,proposal_path,staged_manifest_path)` historical-only entry. |
| N2 version `P/publication-v2/`, `P/publication-v3/` | Same preservation as N1 but renames the active-namespace convention; requires every §8 consumer to learn a versioned directory glob | Not selected now. Adds resolver complexity for no authority gain; N1 keeps one stable `publication/` name for the first generation and isolates renewals explicitly. |
| N3 new proposal ID for same reader | Creates a second `P'` with identical reader bytes; P1 would refuse identical-reader as NO_EDITORIAL_CHANGE unless faked; breaks "same reader" chain and canonical-anchor continuity | **Refused.** This is exactly the fake-editorial bypass forbidden in §5 item 3. |

Selected: **N1**. Stable identifiers across renewal: same `issue_id`, same `research_profile` / `publication_profile`, same `source_root` / `survey_root` / public slug, same `proposal_ref` (= `P`), same `staged_manifest_ref` (U) or new staged derivation (C, §6), same `scope_review_ref` path. Only `renewal_id` (e.g. `r1-core-<yyyymmdd>-<seq>`) and its directory are new. Do not mutate old closed P3S4 / old publication inventory; do not relocate early reader.

Activation record path keeps existing sequence naming under canonical `publication/v2` (d880 §4.3): `supersedes` is the common chain edge for all branches; renewal records extend the same strictly increasing numeric sequence / nondecreasing timestamps / no-cycle / depth≤32 chain. The renewal seal lives under `P/renewals/<renewal_id>/`; the renewal activation record lives on the canonical chain and points at that seal via exact `set_ref {path,sha256}`.

### 1.2 What "same reader" means operationally

- Byte-identical canonical reader FILE (`reader-surface-input-v2.json` bytes) at the **same recorded path** `P/reader-surface-input-v2.json`.
- Same `proposal_ref` + same `reviewed_reader_input` ref (path+SHA) in any new receipt/Gate.
- Early scope review = **the exact file at the exact `scope_review_ref` path+SHA** recorded in the (U: old, C: revalidated — §6) staged manifest. Its RESULT location (review RECORD file) is distinct from its REVIEWED TARGET identity (the reader path+SHA it approves); see §5.1.
- Headline/prose equality alone is insufficient. Any IR byte difference (including ordering/duplicates/whitespace that changes canonical bytes) = not same reader → refuse renewal, route to editorial correction (no silent stuck state, §4.5).

## 2. Unified operator flow (U and C share this skeleton)

States: `INERT_PARTIAL` (prepare incomplete, old State healthy) → `SEALED_INERT` (seal complete, not active) → `ACTIVATED` (State pointer moved) / `ALREADY_ACTIVE` (readonly) / `INDETERMINATE` (State neither old nor expected new — preserve all bytes).

### 2.1 Public API order (new module, strict objects, no caller-verified objects)

```
prepare_renewal(root, state_path, proposal_path, staged_manifest_ref, renewal_spec_path, toolchain_spec_path, recorded_at) -> renewal_paths
  # U: staged_manifest_ref = old closed manifest path+SHA. C: new staged derivation manifest path+SHA (§6).
  # Never regenerates P1 after retention; never invents review; toolchain_spec is executor config only.
finalize_renewal(root, state_path, renewal_paths, deterministic_checks_path, semantic_review_path|NULL_U, visual_review_path|NULL_U, recorded_at) -> set_ref
  # Rechecks current-before scope + all input pins before any write; builds QA/Gate/Candidate; writes seal LAST.
validate_renewal_receipt(root, receipt_path, state_path) -> receipt
validate_prepared_renewal_set(root, state_path, set_path) -> validated_set   # no permission token
activate_renewal(root, state_path, set_path, reason{REVIEWED_MECHANICAL_RENEWAL}, executor, recorded_at) -> result
resume_renewal_activation(root, state_path, record_path) -> result
verify_renewal_history(root, record_path) -> historical_result
resolve_renewal_selection(root, cfg, state) -> identity_selection  # active projection only after historical+active checks
```

All path arguments repo-contained except declared build-tooling absolutes. Writer claims new `P/renewals/<id>/` outputs exclusively; refuses pre-existing conflicting or same-byte takeover; preserves incomplete dirs; never deletes foreign/unknown files. `manuscript_spec` contains only coverage/requirement assertions + author/time inputs, no caller source/profile overrides. Deterministic-check inputs use existing `quality.validate_checks` contract with actual evidence results; no automatic family PASS by schema.

### 2.2 Activation / State / anchor (shared)

- New strict branch in `publication-surface-revalidation.schema.json`: preserve branch1 `REVIEWED_CORE_CHANGE` verbatim and branch2 `REVIEWED_EDITORIAL_CORRECTION` verbatim; add branch3 exact keys per d880 §4.3 shape with `reason_class=REVIEWED_MECHANICAL_RENEWAL`, `kind=RENEWAL_ACTIVATION_V1` (name is contract choice for Astra; no `active_set`/verified-dict/pending boolean). `supersedes`, `prior_checkpoint`, `canonical_anchor={kind,ref}`, `before_state_ref`, `before_active_digest` (canonical SHA of sorted effective seven publication rows + exact observed Candidate ref/null), `before_candidate_ref`, `set_ref`, `core`, `establishment`, `recorded_at` — all mandatory, `additionalProperties:false`, duplicate-key refusal, exact lowercase SHA/commit formats.
- `before_state_ref` must equal both the bound proposal's basis State ref and the P2R retained COPY of those exact bytes; `supersedes`/before-Candidate/digest must agree with retained-before derivation and freshly observed current-before. Historical validation reads the retained State copy, never expects the old hash at the now-updated live State path. Equality remains mandatory on explicit orphan-record resume.
- Canonical anchor rule unchanged (d880 §5): cumulative legacy rows against original validation checkpoint; anchor = original checkpoint if no legacy revalidation before first activation, else latest legacy record immediately preceding first activation; repeated activations retain that same anchor; mixed chain with later legacy successor is unsupported/fail-closed. Renewal does not recompute or migrate the anchor.
- **Candidate/seal COMPLETE BEFORE switch.** Only write = new exclusive activation record, then known-byte State temp+replace updating **only** `publication_revalidation_provenance`. No canonical Candidate/source/QA rewrite. New State validates selected renewal set + normal stage/Preview path before success. No canonical Candidate install, no second pointer, no latest-scan. `verify_renewal_history(record_path)` is historical-only (no State arg); `validate_prepared_renewal_set` needs no active record for that set.
- Failure table inherits d880 §7 with renewal `old` = currently active versioned set (not canonical): seal complete but record absent → explicit `activate_renewal` retry with full current-before + full leaf revalidation (seal is not permission); record created but State still exact old → record inert, `resume_renewal_activation` revalidates full current-before/set/intent and may install that exact record, ordinary activate refuses collision; State already exact new → strict validate + readonly `ALREADY_ACTIVE`; State neither old nor expected new / unreadable / unsafe → `INDETERMINATE`, preserve all bytes, no overwrite/rollback/adoption; close/post-replace validation failure → primary + secondary errors + observed old/new/unknown disposition, never delete referenced/possibly-referenced record. No multi-file atomicity/globalCAS/crash-atomicity claim; single-writer/held/no-follow assumption explicit and fault-tested.
- Normal consumers resolve via the **one role-aware path resolver with State argument** (d880 §8: `resolve_stage_artifact_path` single resolver; orchestrator/handoff/human-gate recompute + SHA-compare in loaders, not only producers). Direct stage/Human-Gate route is the default (`config/survey-production-v2.json` all `handoff_required:false`; `survey_handoff_v2.py:101-102` basis preemption is not stage coverage — `build_handoff` success remains unproved/out-of-scope unless a stage requires handoff). Freeze `build_profiled_freeze`, `approve_publication_preview`, `_validate_stage_artifacts`, VALIDATED/RELEASE_CANDIDATE checks, export workflow predicate, `_prior_artifacts` active projection — all must be renewal-aware or explicitly refuse revised mode in the same implementation unit (Explore inventory; Worker A bridge for code refs).
- Scope: **pre-Preview only** unless Astra justifies a root choice otherwise. Preview-approved / Freeze/Release-decided / exception-active / invalid/foreign authority → refuse renewal. No State rewind, no Profile rebind, no canonical-copy fallback, no new Human Gate, no generic supersession engine. Post-decided/migration is a separate operation.
- Liveness: renewal must either reach healthy active renewal Candidate (then normal Preview→Freeze→Release) **or** terminate in an explicit loss plan (old set stays active + recorded refusal reason + operator next action). Silently stuck state (seal inert forever with no disposition, or old set active but renewal presumed) is refused. After successful renewal, a further reader correction uses the ordinary editorial operation with `prior version KEEP_IMMUTABLE / mutable State COPY`; renewal→editorial-correction chaining is supported. Old legacy R1 / canonical revalidation stays strictly separate and continues to refuse in revised mode.

## 3. Case U — same reader AND exact same source trio / manuscript / PDF

U is pure mechanical renewal: Core/tool/contract epoch changed, but every reviewed target byte is identical. The only new bytes are mechanical wrappers that must reference the new epoch (receipt/Gate/QA/Candidate/seal/activation + build provenance). If any reviewed-target byte differs, U is inapplicable — use C.

### 3.1 Which exact paths/bytes must stay (reuse condition)

ALL of these must verify byte-identical at their **original paths** (no copies):

- Reader: `P/reader-surface-input-v2.json` (canonical FILE bytes).
- Authoring: `P/authoring-input.json` (proposed authoring; accepted Draft archive role unchanged).
- P2R retained files at recorded refs (retained COPY vs KEEP per P1 policy).
- P3S staged trio at recorded refs: `P/staged-source/main.tex`, `P/staged-source/references.bib`, `P/staged-source/jgaisurvey.sty` + closed `P/staged-source/staged-source-manifest.json` (same `scope_review_ref`).
- Manuscript: old `P/publication/reader-manuscript-v2.json` bytes.
- PDF trio: old `P/publication/build/main.pdf` + `build/main.log` + `build/main.pdf.sha256` — see §3.3 for log nuance.
- Reviews' REVIEWED TARGETS: the `{reader_manuscript,source,pdf}` target refs recorded inside the old semantic/visual review records must equal the above paths+SHAs exactly (not merely equal SHAs at other paths).
- QA inputs that are content hashes of the above (not wall-clock/tool versions).

Independent detection (not caller flag): `prepare_renewal` re-hashes all of the above from file bytes, compares against old seal selection table (15 roles) + old receipt `outputs` (exact three staged refs) + review TARGET refs. Any mismatch → U refused before writes (exit 2, no partial seal). Caller `mode=U` never grants reuse.

### 3.2 RECORD location vs REVIEWED TARGET identity (the central U rule)

- REVIEWED TARGET identity = `{path,sha256[,byte_count,page_count]}` of the artifact the reviewer actually inspected (reader file, manuscript file, staged source files, PDF file). Stored **inside** the review record as its target refs.
- RECORD file location = where the review record itself lives (e.g. `P/publication/reviews/semantic-<id>.json`, or outside `P/publication/` when externally supplied — permitted when consistent per R6 Weekly `P/external-reviews/` control). Stored as the seal's `semantic-review` / `visual-review` role ref.
- Reuse in U means: the old review RECORD files stay at their original immutable paths and their TARGET refs still equal the current (unchanged) target bytes. The new renewal seal's `semantic-review` / `visual-review` roles point at **those same original RECORD paths+SHAs**. Do NOT copy identical targets to new paths and call approval reused — same-SHA different-location is refused by the Candidate↔seal path+SHA + review-TARGET checks (R6 `r6-seal-only-L-new`, `r6-target-rebind-L-new` negatives).
- New renewal does not create new semantic/visual RECORDs in U. It creates new receipt / QA bundle / Gate / Candidate / seal / activation RECORDs (new paths under `P/renewals/<id>/`) whose internal TARGET refs point back at the unchanged original artifacts.

### 3.3 What is new in U and why

| New artifact (under `P/renewals/<id>/`) | Why new refs are needed | Binds to |
|---|---|---|
| `renewal-source-manifest` (new strict receipt kind, e.g. `RENEWAL_SOURCE_V1`; not a relaxed old canonical receipt) | Old receipt pins `current_tools` / contract closure / `receipt_sha256` of the old epoch; mechanical evidence needs new-epoch refs. Exact keys mirror d880 §4.1 (`proposal_ref`, `retention_manifest_ref`, `staged_manifest_ref`, `scope_review_ref`, `reviewed_reader_input`, `authored_refs`, `accepted_refs`, `current_tools`, `outputs`, `receipt_sha256`) + `renewal_of {set_ref, seal_ref}` + old/new tool digests via Worker A bridge. | Same `proposal_ref`/`staged_manifest_ref`/`scope_review_ref`/reader bytes as old; new `current_tools`; same `outputs` trio. |
| `reader-manuscript-renewal` vs reuse old manuscript | If manuscript builder is deterministic and inputs unchanged, bytes should equal old manuscript. Either (a) reuse old manuscript path in seal roles (preferred — no duplicate) and let renewal receipt/Gate reference it, or (b) emit a byte-identical copy only if the inventory rule requires renewal-namespace containment — **not selected**: duplicates violate "no duplicate copies of proposed-reader/staged trio" (§10 removed-work). Reuse original `P/publication/reader-manuscript-v2.json` path. | Old manuscript path+SHA. |
| `quality-regression-bundle-renewal-v2.json` | Deterministic checks must be **freshly executed** under current rules (`quality.validate_checks` with actual evidence results); cached PASS is not reused. If the check family changed and old results cannot be justified under current rules, U cannot proceed — require new external review or refuse unsupported contract migration (see §3.4). Bundle refs are new even when underlying evidence bytes are unchanged, because the bundle itself hashes its inputs + rule versions. | Same evidence bytes where stable; new bundle SHA. |
| `reader-surface-gate-renewal-v2.json` | Gate derivation branch (editorial branch bound to receipt + proposed-reader + scope + trio/manuscript) must be revalidated under current Gate schema/loader/CLI. Gate does not bind receipt hash directly, but Gate **requires receipt before itself** in the DAG and checks shared path/SHA/pages consistently. New Gate role path is required because the seal selection table pins exact Gate path+SHA. | Old scope review + old trio/manuscript + new receipt. |
| `publication-candidate-renewal-v2.json` | Candidate is a seal role outside the original seven-row union; normal VALIDATED_DRAFT checkpoint accepts only the selected Candidate path/hash. Even though Candidate does not bind Gate/receipt hashes, its own path+SHA must be pinned in the new seal, and QA changes (new bundle SHA) may necessitate a new Candidate. Old Candidate stays byte-identical and pinned historical, not adopted. | New Gate + new bundle + old manuscript/PDF where reused. |
| `publication-set-renewal-v2.json` (seal, `SEALED_INERT`) | New 15-role selection table with U-specific mixture: `reader-input`/`authoring-input`/`source-receipt`(new renewal receipt)/`reader-manuscript`(old path)/`validated-source`(old trio path)/`bibliography`/`style`(old trio)/`publication-pdf`/`build-log`/`pdf-digest`(old build3 paths — see log nuance)/`quality-regression-bundle`(new)/`semantic-review`/`visual-review`(old RECORD paths)/`reader-surface-gate`(new)/`publication-candidate`(new). Seal `set_sha256` canonical-without-itself. Written LAST. | Mixed old/new as above; no `external_reviews` duplicate map; no activation hash. |
| `build-record-renewal.json` | **Historical build provenance retained truthfully.** Old PDF reused → old `build-record.json` retained; renewal does NOT claim a rebuild under new TeX. Renewal build-record (if any) records `reused_build {record_ref, pdf_ref, log_ref, digest_ref}` + `renewal_tools {old,new}` + `no_rebuild` assertion, verified by `prepare_renewal` (no build executed in U). If any party rebuilt, that is C, not U. | Old build record + old build3. |
| Activation record (canonical chain, branch3) | Moves sole `publication_revalidation_provenance` pointer from old seal to renewal seal. | `set_ref` = new seal; `supersedes` = prior activation/editorial record; anchor unchanged. |

Log nuance: `build/main.log` embeds toolchain versions/paths/timestamps. If U reuses the old PDF, it reuses the old log + old digest as a unit (all three build3 refs = old paths). A fresh log from a no-op or version-probe run is NOT substituted into the seal's `build-log` role, because then log↔PDF provenance would lie. The new-epoch tool evidence lives in the renewal receipt (`current_tools`) + renewal build-record (`renewal_tools`), not in a forged log.

### 3.4 Fresh checks and contract-migration refusal

- Fresh deterministic checks: re-execute the exact check family pinned by the new QA bundle under current code; compare evidence bytes where stable, but the PASS is new. No cached PASS, no `pending`/verified-dict bypass.
- Current rules compat: receipt validation independently reloads the exact scope review, re-derives the proposed reader from new proposed authoring + unchanged accepted Draft, compares canonical reader FILE bytes + all rendered output bytes, verifies current contract/tool closure + actual current accepted research via strict current State + route loaders. It never requires current State to equal the old before-State hash. P2V `SCOPE_BOUND` is re-observed before eligibility (before-only; `P2V_AFTER_ACTIVATION_REFUSED`, no `receipt_kind` caller token). P3S historical replay via `verify_staged_source` (historical P2R/scope/replay, not P2V/seal).
- If the current review contract or check family changed such that old semantic/visual results cannot be justified as still valid (e.g. new required check family, changed scope-review semantics, changed Gate derivation), **U is refused**: either supply new external reviews (which converts the attempt to C with new Gate/Candidate/seal) or refuse unsupported contract migration with an explicit loss plan (old set stays active). No silent reblessing of old-epoch P3S manifests, no implicit old-epoch acceptance.

## 4. Case C — same reader but source / PDF / manuscript / output changes

C is a genuine re-render: reader IR byte-identical, but at least one of staged trio / manuscript / PDF / build outputs differs (including layout-only or metadata-only differences). All changed rendered targets get **new immutable paths** under the renewal root; old targets stay immutable.

### 4.1 New immutable targets

- New staged derivation (trio + manifest) under `P/renewals/<id>/staged-source/{main.tex,references.bib,jgaisurvey.sty,staged-source-manifest.json}` OR re-render from same trio with new toolchain — either way the **effective staged inputs** for this renewal are pinned by a new staged manifest with its own `scope_review_ref` handling (see §4.2). Old `P/staged-source/` closed4 untouched. New manifest's `scope_review_ref` either reuses the exact old scope-review path (if scope still valid under current contract) or records a new scope review — but the old scope RECORD is never mutated, and reuse is only as HISTORICAL input (§4.2).
- New `build/main.pdf` + `main.log` + `main.pdf.sha256` under `P/renewals/<id>/build/` via real disposable-root build with explicitly selected executable + fixed recipe (no caller shell string). Record real exit/log/tool versions/digests. Failed build → no admissible set. Build auxiliaries stay outside the publication inventory; external files outside the namespace are pinned dependencies, not writer-owned files.
- New manuscript `P/renewals/<id>/reader-manuscript-renewal-v2.json` (new `editorial_source`-style proof entry bound to the new staged manifest + new trio, same `proposal_ref` namespace, same reader bytes).
- New receipt / QA bundle / Gate / Candidate / seal all under `P/renewals/<id>/`, all with new path+SHA pins. Old `P/publication/` inventory untouched.

### 4.2 Reviews in C (mandatory postrender; limited early reuse)

- **Ordinary external postrender semantic + visual review is mandatory** against the NEW manuscript + NEW PDF (exact new paths+SHAs as TARGETs). Supplied records arrive at final repo-contained immutable paths (recommended `P/renewals/<id>/reviews/`, but any repo-contained path is permitted when the seal binds exact refs — R6 external-outside control). Result dependencies explicitly enumerated from validated schemas, not generic path scan. No symlinks/latest/mtime authority. Separately labelled supplied fixtures; no self-generated PASS (the operation authors no semantic/visual PASS).
- **Same-input early semantic / correction-scope review may be reused ONLY if**: (a) exact reviewed reader path+SHA unchanged (byte-identical `P/reader-surface-input-v2.json`), (b) current contract still validates that scope review (fresh `P2V SCOPE_BOUND` + current scope-review loader, not cached), and (c) the old scope block is recognized as HISTORICAL input to the new Gate/manuscript derivation — **not as approval of the new Core change**. Gate's early-scope binding uses the old scope RECORD bytes, but the new Gate/Candidate/seal additionally require the new postrender reviews. If (a)–(c) fail, a new scope review is required; scope reuse never waives postrender review.
- New source-proof variant (renewal receipt/manuscript `editorial_source`-style entry): must verify new staged proof (same issue/Profile/Architecture/approval, exact proposal namespace, actual new staged manifest + exact new trio refs) + rederive proposed reader from same proposed authoring + unchanged accepted Draft + compare canonical reader bytes. It **must not require a changed-reader P1 proposal** (P1 stays identical-reader; no new proposal ID) **and must not require a future seal** (all leafs constructible pre-activation: receipt/manuscript/build/QA/reviews/Gate/Candidate/seal are all complete before activation; Gate requires receipt before itself; seal stores no activation hash; no leaf depends on seal/activation).

### 4.3 Independent change detection (no caller-mode trust)

`prepare_renewal` / `finalize_renewal` independently hash: old trio vs new trio, old manuscript vs new manuscript, old PDF vs new PDF (bytes + `pdf-digest` + `page_count`), old log vs new log. Classification is derived, not taken from a caller `mode` flag:

| Observed | Classification | Consequence |
|---|---|---|
| Trio + manuscript + PDF bytes all identical | U candidate (if reader also identical) | Follow §3; any postrender-review reuse permitted only under §3.2. |
| Trio identical but PDF bytes differ (toolchain/layout/metadata) | **C** (render-output-changed) | New build3 paths; exact-PDF review invalidation applies even if the trio is unchanged — old visual/semantic TARGET refs no longer match the new PDF bytes, so old postrender reviews cannot be rebound by equal trio SHA. New postrender reviews mandatory. |
| Trio differs, PDF identical (e.g. comment-only TeX change that normalises away, or metadata-only source change) | **C** (source-changed) | New staged manifest + new build proof required; old trio-bound receipt/Gate/Candidate invalidated even though the PDF matched. Do not silently treat as U. If the new build reproduces the old PDF byte-identically, the new seal still pins new trio/build-record/manuscript paths; postrender reviews are still required because the TARGET trio changed (review TARGET includes `source` sized refs, not just PDF). |
| Reader IR differs (any canonical byte change) | **Neither U nor C** | Refuse renewal; route to editorial correction (changed-reader path). Do not proceed as renewal. |
| All trio bytes unchanged but PDF rebuild differs in metadata only (e.g. `CreationDate`/`Producer`/`ID`) | **C** | Exact-PDF review invalidation still applies: visual TARGET includes PDF `{path,sha256,byte_count,page_count}`; digest mismatch invalidates old visual approval even though the rendered pages look identical. New visual review (or an explicit metadata-only re-review policy selected by Astra — not this design) is required. This design defaults to mandatory new postrender review. |

## 5. Reuse / invalidation matrix (per artifact and check family)

`REUSE` = old immutable path+SHA pinned in new seal; `NEW` = new path+SHA under renewal root; `RE-EXEC` = freshly executed under current code; `INVALID` = old value cannot be carried.

### 5.1 Artifacts

| Artifact / role | U | C | Notes |
|---|---|---|---|
| `P/proposal.json`, `P/authoring-input.json`, `P/reader-surface-input-v2.json` | REUSE (byte-equal, same path) | REUSE (byte-equal, same path; reader must be identical or refuse) | Never copied to new paths. |
| P2R retained files (recorded refs) | REUSE | REUSE (revalidated historical; retention manifest ref unchanged) | No invented retention-manifest location. |
| P3S `staged-source/` closed4 + `staged-source-manifest.json` | REUSE (same manifest + trio paths) | NEW derivation under renewal root; old closed4 untouched | C manifest has its own `scope_review_ref`. |
| Early scope review RECORD | REUSE path+SHA (TARGET = same reader) | REUSE as HISTORICAL only if §4.2(a)–(c); else new scope review | Never relocated; fileLocation ≠ TARGET. |
| `reader-manuscript` | REUSE old `P/publication/reader-manuscript-v2.json` | NEW under renewal root | C manuscript binds new trio. |
| `validated-source` / `bibliography` / `style` (trio) | REUSE old trio paths | NEW trio paths | Source-proof entry differs accordingly. |
| `publication-pdf` / `build-log` / `pdf-digest` | REUSE old build3 paths (unit) | NEW build3 paths (real rebuild) | U: no rebuild claim; C: real exit/log/versions/digests. |
| `build-record` | REUSE old + new `no_rebuild` wrapper | NEW (actual build inputs/outputs/toolchain) | U wrapper truthfully records reuse. |
| `source-receipt` (`validated-source-manifest` family) | NEW renewal receipt (new epoch refs, same outputs) | NEW renewal receipt (new outputs + new epoch) | Old receipt never rebound. |
| `quality-regression-bundle` | NEW bundle, RE-EXEC checks | NEW bundle, RE-EXEC checks | No cached PASS. |
| `semantic-review` / `visual-review` RECORDs | REUSE old RECORD paths (TARGETs unchanged) | NEW postrender RECORDs (TARGETs = new manuscript+PDF) | U creates no new semantic/visual RECORDs; C mandates them. |
| `reader-surface-gate` | NEW (re-derived under current Gate, old scope+trio) | NEW (new scope-history + new trio/manuscript + new reviews) | Gate requires receipt before itself; early-scope bound, not postrender-record bound. |
| `publication-candidate` | NEW (new bundle/Gate pins) | NEW | Old Candidate stays byte-identical, pinned historical. |
| `publication-set` (seal, 15 roles) | NEW seal, mixed old/new roles, `SEALED_INERT`, written LAST | NEW seal, all-renewal roles (except reader/authoring/retention/scope-history) | No activation hash; no `external_reviews` duplicate map. |
| Activation record (canonical chain) | NEW branch3 record, `supersedes` prior | NEW branch3 record, `supersedes` prior | Anchor unchanged; sole pointer update. |
| `publication_revalidation_provenance` State file | Known-byte temp+replace, only this key | Same | Old/new/unknown semantics per §2.2. |

### 5.2 Check families

| Check family | U | C | Refusal trigger |
|---|---|---|---|
| Canonical reader FILE bytes + rederived proposed reader (new authoring + unchanged Draft) | Must match exactly | Must match exactly | Any IR delta → refuse renewal → editorial path. |
| Staged proof `verify_staged_source` (historical P2R/scope/replay) | Old manifest replay must VERIFY | New manifest proof must VERIFY (same namespace/issues) | Proof failure → no set. |
| Current contract/tool closure + accepted research via strict current State + route loaders | Must hold under new epoch (Worker A bridge) | Same | Closure mismatch → refuse; no old-epoch reblessing. |
| P2V `SCOPE_BOUND` before eligibility | Fresh SCOPE_BOUND on old scope | Fresh SCOPE_BOUND (old scope as history or new scope) | `P2V_AFTER_ACTIVATION_REFUSED`; no caller `receipt_kind` token. |
| Deterministic QA (`quality.validate_checks` + evidence) | RE-EXEC, new bundle | RE-EXEC, new bundle | Missing/nonPASS/stale-family → no Gate/Candidate; unsupported family migration → refuse U. |
| Gate derivation (receipt-before-Gate, early-scope bound) | New Gate must validate | New Gate must validate (new trio/manuscript) | Gate drift/wrong-manuscript/Candidate mismatch → refuse. |
| Candidate validation + seal cross-binding (Candidate-6 ↔ seal-15 path+SHA+sizes/pages; review TARGET ↔ role; manuscript trio/bundle/build) | New Candidate/seal must validate; old TARGETs must still match | Same with new TARGETs | Equal-SHA different-path, seal-only review swap, tamper drift → refuse (R6 negatives). |
| Chain/anchor/depth/sequence (≤32 incl. active, 33 refuses-before-write; supersedes/no-cycle/chronology) | Must validate; anchor = preserved canonical | Same | Malformed/duplicate/depth/State-predecessor drift → refuse. |
| Current-before + retained-before agreement (State bytes, before-Candidate, digest) | Must agree; historical reads retained copy | Same | Drift → refuse; orphan → explicit resume only. |
| Close/write/fsync/replace/readback/ownership/foreign-inode | Classified per-FD seam; partials preserved | Same | Swallowed IO, delete-referenced-record, takeover → refuse. |

## 6. Actual schema / function refs demonstrating constraints

These are the concrete enforcement points the implementation must wire (Worker A bridge owns the historical/current code bodies; Explore owns the full consumer list). No code is changed in this unit; refs are requirements, not proof of new behavior.

- **Strict objects**: new receipt `editorial-publication-source-manifest-v2.schema.json` family + renewal variant; seal `editorial-publication-set-v2.schema.json` (`EDITORIAL_PUBLICATION_SET_V1`, `SEALED_INERT`, exact 15 keys `reader-input, authoring-input, source-receipt, reader-manuscript, validated-source, bibliography, style, publication-pdf, build-log, pdf-digest, quality-regression-bundle, semantic-review, visual-review, reader-surface-gate, publication-candidate`, `set_sha256` canonical-without-itself); activation `publication-surface-revalidation.schema.json` branch1 `REVIEWED_CORE_CHANGE` verbatim + branch2 `REVIEWED_EDITORIAL_CORRECTION` verbatim + new branch3 `REVIEWED_MECHANICAL_RENEWAL` / `RENEWAL_ACTIVATION_V1` (exact §4.3-shaped keys, `additionalProperties:false`, duplicate-key refusal, `supersedes` common edge, depth32). `ref={path,sha256}`, `file_ref={path,sha256,byte_count}`; dates are validated instants; repeated identity fields must agree, never establish competing authority.
- **Reader/manuscript**: Reader schema + `_validate_manifest_semantics:207–219`, `build_manuscript_manifest`; `editorial_source` proof branch (absence retains canonical primary-root rule; presence requires verified P3S proof: same issue/Profile/Architecture/approval, exact proposal namespace, actual staged manifest + exact trio refs; full staged verification calls `verify_staged_source(root,proposal_path,staged_manifest_path)`, not P2V/seal).
- **Low/high split**: `survey_publication_set_v2.py` (low: seal/roles/record/anchor/active selection; `load_json_strict`; live SHA+size; must not call agent/Stage/Gate/receipt/Reader/P1/P2R/P3S validators; Core State calls via local import) + `survey_editorial_publication_v2.py` (high: prepare/build/finalize/full-set/activation/CLI; calls P2R/P3S proof, Reader/QA/Gate/Candidate, P2V before-eligibility; source-proof entry never calls seal/current activation; Gate requires receipt before itself). Mandatory pre-code return: actual import graph with no top-level cycle + explicit call-graph boundaries.
- **Canonical State + strict JSON + cross-binding** (per independent final authority/operation resolutions, adopted as constraints): `_require_canonical_current_state:328–377` (expected path from Profile `source_root` + config `authoritative_filename`, exact `state_rel` equality/no-alias, rejects `retained/history/copy/deep`); `_strict_json_from_bytes/_strict_json_from_text` → `DUPLICATE_KEY` before digest (50+ sites); low `:512–526` external-review placement (repo-contained OUTSIDE `<P>/publication` permitted when Candidate↔seal exact); high `_seal_roles:2413–2419` (review paths FROM Candidate binding, no forced basename/relocation); high `:2791–2840` (Candidate-6 ↔ seal-15 + review-TARGET + manuscript-trio/bundle/build bindings); cache `_get_compiled_validator:172–209` (compiled validators only, external `$ref` never cached; schema bytes + instance+format validated every call `:212–263`).
- **Chain/anchor**: `_check_revalidation_chain` (inclusive `range(REVALIDATION_CHAIN_LIMIT)` / `_build_anchor_chain` 33-iteration shape; 32 valid, 33 refuses-before-write), `_check_immutable_revalidation_rows`, `_validate_checkpoint_record`, `_resolve_checkpoint_artifact`, `_validate_agent_state`, `_prior_artifacts` active projection (seven publication roles only; no research/Architecture/Draft rebind; old-byte + new-set drift both refuse), `resolve_stage_artifact_path` single resolver.
- **Consumers** (same implementation unit must make each renewal-aware or explicitly refuse revised mode; d880 §8 table + R6/R7 evidence): `survey_stage_validation_v2._prior_artifacts` + VALIDATED/RELEASE_CANDIDATE checks; `survey_production_v2.validate_state_semantics:784–809`; agent `approve_publication_preview:1479`; `survey_profiled_freeze_v2.build_profiled_freeze:58`; `config/survey-production-v2.json:278–382` + orchestrator `_configured_expected_artifacts/_configured_gate_inputs:154–233` + handoff `_expand_gate_path/_reviewed_artifacts` + `survey_handoff_v2.py:101–143` + `survey_human_gate_v2.py:249–281` (all recompute + SHA-compare in loaders); stage `survey_stage_validation_v2.py:73–100`; preview export trigger/discovery/manual input (State-bound Candidate choice; inert-set file change never auto-adopts); release workflow/checkpoint/generic Candidate/QA/Freeze builders (verify via actual integration); P1 `_active_effective` + full pipeline/receipt recheck + before-graph/retention/Candidate observation (repeat correction; no current-before call after activation); P2R/P3S historical namespace/source-proof semantics + exact import/schema closure deltas (no silent `unchanged37`); canonical revalidation/R1 refresh + interactive revision wrapper + semantic-quality canonical writer + canonical Weekly/Special build workflows (revised-mode refusal before destructive action/output/guard unless routed through renewal); config contract-files + receipt CURRENT_CLOSUREs + P3S fixed37 deps + CLI registration/docs.
- **Current refusals reused verbatim**: `R1 … refused in VERSIONED_ACTIVE`, canonical-revalidation-refused in revised mode, fake-reason refused; `P2V_AFTER_ACTIVATION_REFUSED`; `STATE_NOT_CANONICAL` vs history-valid; `RECORD_COLLISION`/`INTENT_COLLISION` → explicit resume; `INDETERMINATE`; `ALREADY_ACTIVE` readonly; `RECORD_*`/`STATE_REPLACE`/`POSTREAD_FAIL`/`POSTREPLACE_FAIL`/`RECORD_OWNERSHIP` close-seam taxonomy.

## 7. Worker A bridge — explicit assumptions (not an unconsumed helper)

Worker B does not implement historical/current code bodies. The renewal contract is constructible only if Worker A returns and Astra confirms all of:

1. Historical P1/P2R/P3S entry points and their retained-vs-current pin shapes on actual57: exact `proposal.json` / `authoring-input.json` / `reader-surface-input-v2.json` loaders, retention-manifest ref shape, `verify_staged_source` historical-only behavior, P2V `SCOPE_BOUND` before-only entry, P1 `KEEP_IMMUTABLE` vs State `COPY` policy hook for a second retained generation (renewal KEEP set).
2. Current tool/contract closure enumerator: `current_tools` (executable digests, fixed recipe/argv/env, TeXLive/toolchain versions where available, contract-file + CURRENT_CLOSURE union) for old epoch and new epoch, with byte-level comparison semantics. Renewal receipt must bind both (`renewal_of` old + `current_tools` new); Worker A defines how old tool digests are represented when the old toolchain is no longer installed (recorded evidence vs re-probed).
3. Reader rederivation function: new proposed authoring + unchanged accepted Draft → canonical reader bytes, used by both U and C to prove same-reader (not headline compare).
4. Trio/manuscript/PDF comparator: independent byte + digest + `page_count` comparison used for U-vs-C classification (§4.3); no caller-mode input.
5. Scope-review loader + P2V caller shape for renewal (before-only, no after-activation call, no `receipt_kind` token).
6. QA/Gate/Candidate builder entry points reusable for renewal receipt/Gate/Candidate without forking authority (existing `quality.validate_checks`, Gate `_derivation_for_manuscript`/builder/CLI, Candidate builder).
7. State/chain helpers: canonical-State resolver, before-digest computer, anchor-chain walker (inclusive-32), `supersedes` sequencer.

If any assumption is unconfirmed, the renewal operation is not constructible and must stop before code (Astra scope choice), not proceed with a detached helper.

## 8. Operator cost — removed / added / unknown (honest)

Removed (qualitative, unmeasured): in-place publication overwrite/rollback across a Core/tool wait; stale canonical Candidate replacement; duplicate copies of proposed-reader/staged trio; same-issue wrong-seal/manuscript/Candidate confusion (strict cross-binding catches it).

Added: second retained generation (`P/renewals/<id>/` persistent versioned files); typed selection/resolver consumer changes for renewal-aware readback; strict new receipt/seal/branch3 closure maintenance; preflight + full historical/current replay per renewal; operator-facing explicit `activate_renewal` / `resume_renewal_activation`; separate postrender review procurement in C (real author-independent inspection, not synthetic); explicit loss-plan bookkeeping.

Unknowns (not hidden): whether TeX/toolchain differences keep PDF byte-identical often enough for U to be common (if not, most renewals are C and U machinery is rarely exercised); actual review latency/cost for C postrender semantic+visual; measured verification time for full replay on representative (non-placeholder) sources; whether the current check family will accept old evidence bytes in U or force C; storage growth from retained renewals. No numeric savings, no finish date.

## 9. Public fixture recipes (success + negatives; code commit before authority)

All fixtures: fresh independent Git with **actual complete new renewal source committed first** (meaningful source commit), then actual accepted research/Architecture/Draft + initial publication authority → P1 proposal/retention/early scope/P3S → old versioned set (sealed+activated) → Core/tool change → renewal prepare/review/finalize/seal/activation. "Current epoch" = tool/contract/receipt/basis consistency. Weekly + LONGFORM_SPECIAL routes where applicable; real PDF/log/digest transfer; strict receipt/Gate/QA/Candidate/State lifecycle to RELEASED for positives (synthetic Preview/Freeze/Release only; no genuine Human approval; placeholder content stays production-semantic NO-GO).

### 9.1 Success recipes

- **U-PASS**: old set healthy + active; Core/tool epoch bumped (Worker A bridge records old/new digests); trio/manuscript/PDF/reader all byte-identical (§3.1 independent check); fresh QA RE-EXEC PASS under current rules; new Gate/Candidate/seal validate; branch3 activation `ACTIVATED`; strict readback shows active renewal set, historical readback shows old set; normal direct stage→Preview→Freeze→RELEASED on renewal; old canonical files + old Candidate + old seal byte-identical; second renewal idempotent → `ALREADY_ACTIVE` readonly.
- **C-PASS**: same reader IR identical; new trio (or same trio + new toolchain) → real rebuild → new PDF/manuscript paths; new postrender semantic + visual RECORDs against new manuscript+PDF PASS; early scope reused as HISTORICAL only with fresh `SCOPE_BOUND`; new receipt/QA/Gate/Candidate/seal validate; branch3 activation `ACTIVATED`; lifecycle RELEASED; old set preserved byte-identical.

### 9.2 Negative / control recipes (each: exact entry, seam, write-window, observed old/new/unknown disposition, explicit resume/healthy control)

- **Comment-only control** (source trio comment/whitespace-only change, reader IR same, PDF bytes identical after rebuild): must classify as **C**, not U. Old trio-bound receipt/Gate/Candidate invalidated by trio-byte mismatch even though PDF matched. Requires new staged manifest + new build proof + new postrender reviews (TARGET trio changed). Proves caller-mode flag is not trusted.
- **Render-output-changed control** (same trio bytes, new toolchain changes PDF bytes/layout or metadata): must classify as **C**. Exact-PDF review invalidation applies; old visual/semantic TARGET refs no longer match new PDF `{path,sha256,byte_count,page_count}`. New postrender reviews mandatory. Proves trio-SHA equality does not carry PDF approval.
- **Semantic-IR-changed refusal** (any canonical reader byte change, however small): must refuse renewal pre-write (exit 2, no renewal dir seal, old State healthy). Operator next action = editorial correction path, not renewal. Proves headline-equality is not reader identity.
- **Metadata-only PDF rebuild** (trio + manuscript unchanged, PDF differs only in `CreationDate`/`Producer`/`ID`): treated as C per §4.3 (exact-PDF invalidation). New visual review required in this design (no metadata-exemption policy selected).
- Standard renewal negatives (mirror d880 §9 with renewal bindings): same-issue wrong seal/manuscript/Candidate; old canonical Candidate supplied after renewal activation; inert renewal set not adopted; unconsumed/unknown branch3 record; research ref change; old authored/new reader inconsistency; equal-SHA different reviewed path (seal-only swap + target-rebind); stale/failed/missing postrender reviews (C) or missing fresh QA (U/C); build failure / extra input/output / hash drift; seal missing role / unknown ref / duplicated role; legacy-anchor error / cycle / depth / sequence; State/predecessor drift; approved/foreign Candidate; canonical writer after renewal; every record/State write/close/fsync/replace/late-readback failure with immediate observed delta + explicit resume/healthy control. Test public callers, not standalone validators or earlier unintended refusals.
- **Contract-migration refusal**: current check family changed so old evidence cannot be justified → U refused with explicit loss plan (old set stays active + recorded reason). Proves no unsupported reblessing.

Closure/regressions: exact staged/receipt/current-contract dependency changes; Reader/Gate/State/stage/Preview/Freeze/export path handlers; affected initial-mode R1 guard; P1/P2R/P2V/P3S repeat behavior; renewal→editorial-correction chaining. Correct failures and rebind exact source.

## 10. Open items and stop

DM022 accepted-upstream correction, DM016/017 Profile readiness, representative-data semantic/visual/layout/bibliography acceptance, Retrospective/manual/direct-primary applicability, fixed candidate/seven-point audit, Human migration/adoption, net-work measurement remain OPEN. This design does not close allR3 or DM021, does not migrate old-epoch P3S manifests, does not prove `build_handoff` success, does not claim globalCAS/crash-atomicity/continuous-no-drift/creator-identity/certified-rerunner.

**Stop. No code/test/build/fixture/source changes in this unit. Ordinary Commit/Push Human-owned. This file is the ONLY write in this Worker B unit; `notes/rephase-1-editor` left intact per AGENTS.md.**
