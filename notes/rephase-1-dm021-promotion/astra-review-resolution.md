# Astra P2R design resolution / mandatory implementation conditions

2026-10-13 JST. Author-side architecture/source synthesis, distinct from [fresh independent design review](independent-design-review.md). **Accept DESIGN_BOUNDED_PASS** for [selected P2R contract](../../outputs/rephase-1-dm021-retention-contract-decision.md), SHA256 **194fd7dea0bfef7e9605fc7ed34a2e90a7f0ab63428333c1dec48b605949370e**. No implementation/runtime/publication acceptance is inferred.

## 1. Selection and rejected interpretations

P2R is one-shot retention capture plus separate read-only verification, expected3A module/schema/test. No existing P1 behavior changes. Existing retained root refuses even if all bytes match; partial outputs remain and require separate disposition. A complete retained set may be read again, but there is no convergent writer retry or equality-based takeover.

The initial General analysis and correction remain intact. Their old-byte-only revalidation claim, mislabeled Gate delta, too-small full-writer budget, candidate-as-publisher statement, mandatory production-owned fixture, schema-version shorthand, convergent partial retry and “fresh P1 after retention” promise are superseded by selected contract §§1–6. Existing revalidation supports changed publication bytes under a restricted reason; the editorial authority/integration problem is different. No second State pointer/reason or second-live-review default is selected.

P1 remains strict: after capture its destination-absence check refuses. Full promotion therefore still needs a new retained-aware current-authority contract. We are selecting a useful missing persistence component, not certifying automatic composition with P1/adoption. Both lifecycle benefit and storage/verification/manual recovery cost must be assessed later; no measured net-savings claim.

## 2. Mandatory pre-code return, interpreting independent review conditions

The fresh reviewer found no design blocker, and required concrete interface details before code. General's next return must resolve these within the selected contract:

### I1 — Profile binding after live State replacement

Do not choose an arbitrary KEEP row labelled Profile, rely on a basename, or read mutable current State to locate retained history. A concrete feasible chain to specify is: exact supplied proposal SHA → manifest and basis equality → unique `state:authority` COPY row whose original path/hash equals `basis.state_ref` → verified retained State bytes → exact State `profile` path/hash → unique matching KEEP row and verified Profile bytes → validated source_root/proposal_id → exact canonical proposal/retained/manifest paths. Actual P1 graph has State at `survey_editorial_correction_proposal_v2.py:608–614`, State-bound Profile validation at `:415–427`, and exact bundle/manuscript Profile relations at `:493–514,679,768–776`. X intake may contribute another Profile role (`:1159–1165`); it is not interchangeable authority. Reject missing/ambiguous/disagreeing rows. Before reading each typed hop, enforce raw containment/regular-file checks; before broad inventory or writes, establish canonical roots. No current eligibility is inferred from parsing retained State.

### I2 — Concrete raw-read / snapshot / ownership protocol

Importing P1 `_Collector` wholesale may initialize current config/HEAD and pull in assumptions unsuitable for historical retained-set verification. Specify actual helper reuse or a minimal local safe-read primitive; do not silently expand P1 or introduce a generic filesystem framework. Pin known wrapper bytes before their rereading validators, use P1's returned `input_hashes` to bind all consumed dynamic dependencies, and verify source-copy bytes against those hashes. Define mode/type/ancestor checks and the exact control/edition inventory, including new P2R module/schema. P1 guards are not proof of a later writer's safety. All I/O/Git checks must fail explicitly, retain raw failures, and not depend on optimized-away assertions.

Define exclusive root claim and the identities tracked for root/ancestors/files during the invocation. Same bytes alone do not establish ownership. Unexpected mutation stops without foreign cleanup. Manifest-last means exclusive-create/write/close/readback plus verification, not mere path presence or a global atomic transaction. Any temp requirement must fit the closed inventory protocol and be reviewed before code.

### I3 — Exact schema/results and proof scopes

Use `2.0-rc1` plus `EDITORIAL_RETENTION_V1`, fixed exact paths, one-to-one sorted rows, strict unknown-field/type/ref checks and explicit canonical JSON. Capture input fingerprints are observations, not signatures or persisted independent approval. `RETAINED_SET_CAPTURED` means this invocation finished its checks; `RETAINED_SET_VERIFIED` means the observed bound set is complete now. Neither means current authority/semantic approval or historical successful invocation. Specify typed incomplete/invalid/indeterminate errors and preserve close-failure outputs accurately. KEEP drift refuses successful retained-set verification; live mutable COPY-original drift is not a persistence failure after capture.

### I4 — Verification budget and stop

Use actual accepted-chain synthetic Longform/Weekly plus an R1-predecessor case and the contract's behavior/fault/write-window oracles. Choose affected regressions after the diff; no P1-36 transfer or decorative full-suite rerun. If three added files cannot meet the contract, if bound Profile/history cannot be resolved safely, or if a future-consumption identity is missing, return the exact blocker before scope expansion. Concrete interface approval is Astra's existing engineering decision, not a new Human publication Gate.

## 3. Evidence bounds and next action

General's source identity/all13 hash/mode checks and fresh reviewer's HEAD/status/key-module hash/source reads are summarized tool observations; raw command transcripts were not persisted. Independent review is actual-source design review, not document-only acceptance, but it did not independently rehash all13. Prior P1 durable freezes/patch/qualifications remain the exact content basis. No new guards/rerunners/runtime proof were created in this unit.

Source remains actual409/tree8ce +13files3M10A, P1 fullpatch85e9d9ab, original selected contract07e89990 unchanged. No restoration/network/intake/fixture/code/schema/test/build/ref/commit change in this unit. Current copy availability is an observation, not a guarantee of future `/tmp` survival.

Next after Human continuation: General P2R interface/fixture proposal resolving I1–I4, then only selected retention implementation after Astra return. Full adoption/reason/State promotion stays design-open; Whole NOT_READY, step4/B3 OPEN, canonical audit unstarted, DM021 OPEN. Stop at Human Commit Point now; Commit/Push remains Human-owned.
