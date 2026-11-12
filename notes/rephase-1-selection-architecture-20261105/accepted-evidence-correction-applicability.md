# Accepted-Evidence correction applicability — Selection dependency (read-only, no code)

**Role:** applicability analyst — NOT implementer, NOT author, NOT independent reviewer of Selection substance, NOT Human.
**Date:** 2026-11-05.
**Method:** read-only packet DATA + prior root/contract/implementation notes as DATA. No implementation, no active State/source writes, no imports/tests/build/fixtures, no network/new fetch, no Git/HEAD/status/log/commit readback, no ordinary Commit/Push, no Production mutation, no subagents.
**Instance only (selected):** `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work`, epoch `e84a82aca000c990597ea8cf60f548e2ff187bd1` over `48082356`. Shipping final139/771 DIRECT409 (`de0af9cb…`/`c5a6b230…`) unchanged; test-only `d486` vs `7b86` delta preserved as history. No other instance, no Production checkout, no current-main following, no reconstruct readback used as authority.

**Read scope (explicit):**

- Packet `README.md`, `astra-working-resolution.md` (§§1–3), `route-map.md` FULL, `route-supplement.md` FULL, `route-map-data.json` FULL, `w34-read-scope-and-pins.json`, `sp-read-scope-and-pins.json`.
- `reviews/w34-r2-selection-proposal-independent-review-20261105.md` FULL + machine, `reviews/sp-selection-proposal-independent-review-20261105.md` FULL, `w34-r2-selection-proposal.md`, `w34-r2-counts.json`, `w34-r2-arxiv-triage.json` (header/cluster counts), `w34-r2-body-read-ledger.md` + `w34-r2-body-read-raw.json` (existence/sections/SHA, not re-consumed here), `sp-essential-gap-map.json` FULL, `sp-jev-authority-inventory.md` (existence only).
- Design authority: `outputs/rephase-1-dm022-prearchitecture-contract-decision.md` INCLUDING §11 FULL (+ §§1–10 as binding), `outputs/rephase-1-dm022-prearchitecture-precode-assessment.md` (B2/B4 OPEN), `outputs/rephase-1-dm022-prearchitecture-implementation-assessment.md` + mandatory `astra-closeout-resolution.md` excerpts via authorized notes DATA (`notes/rephase-1-evidence-scaling-repair/astra-closeout-resolution.md` §76, `test-preparation.md` §§15–16, `interface-map-r2.md`, `caller-map.json`), `outputs/rephase-1-evidence-correction-rehearsal-assessment.md`.
- NOT done: no source-file re-read in workspace root, no project import, no runtime/test execution, no network, no Git, no State advance, no Draft/PDF, no Human Gate request, no full-319/160 semantic re-read. Counts/pins below are joins of already-recorded DATA, not new verification.

## 1. Current selected authority (both EVIDENCE_REVIEWED, LEGACY, no Human review, 7 slots absent)

Both editions are `EVIDENCE_REVIEWED`, `next_action = stage:selection`, `terminal_reason = null`. Research checkpoints are LEGACY `CORE_STAGE_CONTRACT` (`kind` absent, `from_state/to_state` present), NOT DM022 PREARCH records. No `candidate-matrix-v2.json`, `candidate-selection-v2.json`, `architecture-v2.json`, review summary/attention, `gates/`, `handoffs/`, or `orchestration/v2/interactive/` exists for either edition — writer has not run in this instance. Guard absent in both.

| edition | State (bytes/SHA) | checkpoint CANDIDATES_NORMALIZED | four refs (live SHA-checked in route-map-data) |
|---|---|---|---|
| 2026-W34 | `d7acd29b1518399ffc2376eb07e102491a6ec9782b3fdd79815c5f230e1886b0` 4087B, `EVIDENCE_REVIEWED` | `0979f9f7703a25c2bd3424824bc4ad9f8719e8e7bcc49c19c5573d0f70ab593a` 4549B, `CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED`, impl `e84` | Evidence `edf21e4d…` 409, Views `3777133c…` 409, Ledger `f089cc4e…` 439, Completeness `e8c432dd…` 3 LIMITED (1 SATISFIED/2 LIMITATION) |
| SP-efficient-llm-2026 | `180db8c30721825d40461cd5e1b92edb704f3630f518bfd693b4732211538220` 4194B, `EVIDENCE_REVIEWED` | `1233b1f6ca3301d6430d4d157788d0a45a613c9ce1e1563e7c06fe11d73993f0` 4745B, same transition, impl `e84` | Evidence `65784e69…` 160 (8 VERIFIED/152 PARTIAL), Views `1557fef7…` 160 (132 MATERIAL/28 CONTEXT), Ledger `b7c85b4e…` 165 (132M/28C/5E), Completeness `d67f7f83…` 15 LIMITED (2 SATISFIED O01/O07, 13 LIMITATION) |

- State `implementation` remains init `48082356`; latest checkpoint/implementation is `e84`. Normal agent Stage Checkpoint path uses **current executing HEAD** for new checkpoints, not State init pin (route-supplement §1).
- LEGACY four-ref rule active here: Evidence/Views via same passed checkpoint (exact artifact name/path/live SHA, View binds Evidence SHA); Ledger/Completeness via canonical `source_root` paths (here identical to checkpoint rows, so four coincide). Historical accepted dirs are storage only. PREARCH resolver (`low.resolve_research_authority`) and `require_research_operation_ready` guard/completion checks are future-branch, not active (route-map §§4–5).
- Matrix = Evidence results (one Discovery per result, verified 409/409 W34, 160/160 SP). Ledger non-Matrix rows (W34 26 EXCLUDED+4 DUPLICATE, SP 5 EXCLUDED) have no Evidence task, never become Matrix candidates, never Selection assignments (route-map §6).
- Validator eligibility before roles (route-map §6): W34 399 eligible, 10 ineligible (`8 NEEDS_MORE/HOLD + 2 PARTIAL/HOLD`; `REJECTED/NEEDS_MORE` and `NON_MATERIAL/HOLD` cannot be SELECTED); SP 160 eligible (PARTIAL eligible, no NEEDS_MORE/HOLD in Matrix). Eligibility is mechanical, NOT editorial sufficiency (§4.2).
- Human Gates both pending; no `gates/architecture-approval.json`, no `gates/review-index.json`, no reviewed commit, no presented immutable request to supersede, no Exception, null publication revalidation pointer (route-map §§1/9, route-supplement §1). No prior Human review/REQUEST_CHANGES history to exclude (DM022 §3 exclusion does not trigger).

This satisfies the DM022 **lifecycle part** of the operating window (§3) for both editions. Content/authority part is decided per-§2 below.

## 2. Real upstream gaps found by the new Selection unit (why correction is a dependency, not a feature)

### 2.1 W34 — 4 (+1 optional) promising papers, bodies captured, accepted cards abstract-triage only

Independent r2 review verdict: `CHANGES_REQUIRED` — r2 NOT ready as actual substance with fixed-41 outcome. Universal maker-reported/no-reproduction/no-deployment exclusion collapses KEEP17/in-window/full-section and INSPECT9/out-of-window to the same HOLD string; fixed-41 is preserved post-hoc, not derived.

Accepted claim scope for papers is abstract-triage only (review §5, machine `B3-claim-scope`):

- Sampled task cards carry `technical_claims_accepted:false`, `discovery_only:true`, `DISCOVERY_SOURCE_ONLY` (100+ grep hits, zero counterexamples observed in review). Body-read ledger/raw (26 bodies, §§/text_len 30–152KB/SHA) is packet DATA, NOT checkpoint-bound authority. Selection/Architecture must be built from checkpoint refs — packet DATA cannot be cited as claim basis.

Counterfactual inclusions warranted (all `SUPPORTING_EVIDENCE`, `AUTHOR_CLAIM` maker-reported, no deployment/reproduction claim, with limits; one Research-Notes box, +0.5–1pp):

| DID | body pin (r2 ledger/raw, captured, maker-reported) | claim (bounded method/eval-as-reported + limits) | proposed role |
|---|---|---|---|
| `w34-event-arxiv-2608-15127` agentic workloads | 314048B `85c70376…`, 08-15T09:02Z KEEP14, full §§3–5 | long-running tool/state/I-O, non-LLM bottlenecks, pay-go breakdown (HKUST/Alibaba/ByteDance) | P2 SUPPORTING (serving-mechanism background) |
| `w34-event-arxiv-2608-16096` commercial-tax | 414077B `a4c2aafe…`, 08-17T04:37Z INSPECT9, full §§ incl Limitations | MuSiQue/HippoRAG-2 license audit + 13 embedders floor + indexing/embedding/answering cost model + buyer checklist | P1 SUPPORTING (buyer-caution sidebar qualifying pricing/SOTA numbers) |
| `w34-event-arxiv-2608-21100` ReFrame | 711224B `da737a85…`, 08-21T13:47Z KEEP17, Limitations present | evidence-guided test-time safety alignment for MLLMs (cross-modal jailbreak/safety-awareness/over-refusal) | P4 SUPPORTING |
| `w34-event-arxiv-2608-18389` jagged frontier | 388712B `56b48291…`, 08-18T23:46Z KEEP17, full Abstract→Conclusion | code-agent robustness is scaffold/codebase-dependent under semantics-preserving transforms (first such evaluation, as reported) | P2/P3 SUPPORTING single destination (recommend P2 robustness counterweight) |
| (optional) `w34-event-arxiv-2608-21095` Trustworthy RAG | 197521B, 08-21T13:42Z KEEP16 | Security-Reliability Gap/poisoning evaluation agent | P4 SUPPORTING only if box has room; else considered-and-held alternate |
| named alternates | 14927 routing (caution note, negative result), 14967 WAN (analytical pre-measurement + vendor, weaker than 15127) | explicitly considered, not overlooked | contextual/background |

Exact minimal next per review §5 (no new fetch; captured bodies only): **new proposed-input Evidence version for ONLY the 4 (+1) DIDs** — one bounded claim set per DID (title/method/eval-as-reported/limits/no-code/no-deployment), each citing exact `raw_path` + body SHA + section location already in r2 ledger/raw; re-run Evidence/Views/Ledger/Completeness via strict facades with fresh fail-closed guards (preserve `5ca6f310` outputs + State/Profile/CP); independent re-review of corrected 4–5 cards only; then Selection delta (4–5 HOLD→SUPPORTING + one box, page arithmetic fix 14–16pp). No 319 re-run, no broad crawl, no status upgrade beyond bounded `AUTHOR_CLAIM` PARTIAL.

Additional r2 blockers preserved: page total `P1 3–4 + P2 4 + P3 2–3 + P4 3 + P5 2 = 14–16pp`, not claimed 14–15pp (correct total or tighten P3 2–3→2pp); 39 non-arxiv CONTEXT now per-DID meaningful, no promotion beyond §5 warranted; dossier correctly scopes Paper Watch as absent-after-reading, must amend to “4–5 box pending Evidence update; without update, fixed-41 is no-paper scoped.”

**Necessity for W34:** any paper inclusion in a load-bearing role REQUIRES upstream correction. Existing Evidence cannot support it. Validator eligibility (`PARTIAL`+`CONTEXT` selectable) does not satisfy governance §§4.2/4.4/8 (captured-readable bodies that could affect materiality must be inspected for additional claims; same-generic-reason collapsed clusters must be broken by actual relevance/novelty/redundancy).

### 2.2 SP — D141 stale alias, D142 unfetched verification overclaim, O10 archive pending

From `sp-essential-gap-map.json` + SP independent review (`CHANGES_REQUIRED`, author map NOT ready):

- **D141** `PARTIAL CONTEXT`, verification UNRESOLVED historical, HOLD Appendix-A. Accepted card `task-4700b268375ef45d48a6.json` 6321B `aad7cc3f…` claims aliases both →1.13.0. Current body `DATA.sp13-models.html` 219035B `59b6c17b…` dateModified 2026-11-01T02:39:33Z, aliases `jev-latest/jev-preview →1.14.0`, table 1.13.0+1.14.0. Contradiction: card vs current body. Historical summary is 2026-09-21 `SUMMARY_CAPTURED` 3751B `f7eeec68…` (jev-1.13.0) only. Correction scope to Root: note 1.14.0 present + aliases→1.14.0 in current body; historical 1.13.0 summary-only vs new body distinct; retain UNRESOLVED (09-21 revision needed; do NOT elevate current 1.13 presence to historical pin).
- **D142** `PARTIAL MATERIAL`, verification MIXED (`VERIFIED` contract-role recorded + `UNRESOLVED` calibration NOT FOUND + limitation page-not-fetched internally inconsistent), HOLD summary-only. Accepted card `task-21ce0892d8846adffd6b.json` 3681B `7d7d26d4…`. NO body (`NONE`, no sp17-api raw, no supplement entry). Historical summary only: answer schema + distribution-derived confidence summary-only, `INDEPENDENT_EVIDENCE_NOT_FOUND_AS_OF_2026-09-21`. Cannot support schema fields/confidence math/version/date/body consumption/current-or-historical primary-body status/independent calibration validity. Correction scope: retain PARTIAL/UNRESOLVED; do NOT treat target label as body verification; contract details require D142 body (current-only even if fetched, historical requires ≤09-21 snapshot).
- **O10 Jev historical authority BLOCKED:** no full-body pre-09-21 TypeSafe capture in authorized captures. Historical material is 2026-09-21 summaries only (4453B `0b8bd…` + 3751B `f7eeec68…`). Full bodies 2026-11-01 current-only (D070 270966B, D071 165512B, D141 219035B; D142 none). O10 remains LIMITATION; cannot be waived by empty P8 + Appendix HOLD. Upgrade requires archive snapshots for 3 locators (launch/concepts/models; api only if contract load-bearing) via Root limited archive access; no Human Q1Q2Q3; no active upstream edit here. Status `BLOCKING for O10 as-of VERIFIED; HOLD+LIMITATION is honest ceiling`.
- **Deployment inheritance BLOCKING for as-of claims:** G1 vLLM historical (current 2705796B `fa61427e` Vercel HIT no version header; 0/13 commits ≤cutoff; supplement `s14-commits-file-correct` 61054B) OPTIONAL for architecture (DSpark already via V41 §2.4.3 + README `dba1be0`) but BLOCKING for as-of deployment-config claims (D040/D049/D063/D153 moved HOLD); G2 Dynamo matrix (current 16535B `5b9ddeb7`, FP8 exact absent) OPTIONAL current-role-only, STOP no new repo guess. P5 must cite V41+README for architecture, quarantine vLLM/Dynamo current-only.
- **Tiering/budget BLOCKING:** SELECTED 132 = 131 MATERIAL + 1 CONTEXT is ledger carry-over, not measured-effect filter; 7 zero-PRIMARY obligations (O01/O03/O08/O09/O12/O13/O10 variant); 22pp+ lineage-only P1–P3/P7 unjustified; mis-tiered SUPPORTING `D143 Engram` (body-consumed VERIFIED deltas) is O13 measured core → PRIMARY. Exact corrections: (1) O10/D142 blocking (fetch D142 body + G3 09-21 revisions, or restrict P8 to contract-existence + NOT FOUND), (2) move D040/D049/D063/D153 to HOLD/Appendix-A or fetch G1/G2 pins, (3) promote D143 + re-map/justify 70+6=76pp per package, (4) state deterministic `candidate:<issue>:sha256(task)[:16]` runner mapping + downstream `section_label`/closing-summary debt.

**Necessity for SP:** any D141/D142 as-of fact use or O10 as-of VERIFIED REQUIRES upstream correction + historical pins. HOLD+LIMITATION is the honest ceiling from existing captures. D142 body absence + 09-21 snapshot absence cannot be cured from existing copied+new inputs/supplement alone — archive fetch is a new-material dependency returning to Root.

## 3. Existing DM022 accepted-upstream correction contract (selected, implementation exists, pre-code gate OPEN)

Contract `a345bb95…` + precode ROOT `0425c530…` + implementation final133 (`25b48878…`/manifest `31fa4a72…`) remain design/implementation authority. This unit reuses that contract; it does NOT repin contracts, add a new module/schema/family, or invent a new engine. Implementation is already BOUNDED COMPLETE (final133 actual409/tree8ce + 133paths54M79A/768); what is OPEN is the **next-use pre-code readiness + independent readiness + Astra confirmation BEFORE code** (§10), including B2/B4.

### 3.1 Operating window (§3) — fits W34 4-IDs; SP needs archive decision

Initial support is agent-first Core-v2 at **exactly `EVIDENCE_REVIEWED`**, before any accepted Selection/Architecture or Human Gate presentation/review:

- Strict canonical LIVE State/Profile validation, exact path/hash/issue/profile/init provenance; public agent validation, NOT caller-verified dict.
- Passed Discovery/Screening + Evidence/Materiality/Completeness with valid checkpoint provenance (latter three = same current producer checkpoint + four accepted artifacts).
- Selection/Architecture/Draft/validation/publication-preview/Freeze/Release checkpoints pending with no accepted downstream provenance; Architecture/Preview gates pending with no Human approval/provenance, no recorded Human review/index entry, no presented immutable request to supersede, no Exception, null publication revalidation pointer.
- Existing author-side Selection/Architecture drafts/previews may exist; NOT accepted authority; handled by downstream plan; no broad tree cleanup.
- Same issue, Profile bytes/paths, Discovery record universe + accepted Screening decisions; **affected-ID allowlist nonempty/unique/subset of already-known non-DROP IDs; new Discovery IDs or changed Screening decisions refused** (earlier-regeneration contract).
- State returned after genuine Human REQUEST_CHANGES, pending/reviewed Architecture Gate, approved Architecture, or later stage is OUTSIDE this window (legitimate Gate revision remains under its own conditions; do NOT manufacture a Gate or fake Human feedback).

Witnesses required: Weekly+Thematic (same research revision operation; no publication rendering in revision itself). DM016/DM017/Profile bounds per §8 apply (see §6).

Assessment: W34 4 (+1) DIDs are already-known non-DROP Matrix IDs (KEEP/INSPECT, PARTIAL/CONTEXT/MATERIAL), same Discovery/Screening universe, no Screening change — window-eligible on ID grounds. SP D141/D142 are known non-DROP Matrix IDs on ID grounds, but lack required newly retained Raw/history (D142 no body; O10 no ≤09-21 snapshots) — window-eligible only AFTER the archive-access dependency is decided and satisfied; otherwise HOLD ceiling applies.

### 3.2 Preserve / produce / review / validate (§4)

- **Before graph + retained inputs:** reload canonical State→passed checkpoint→typed artifact graph (package/task/card/result, Discovery/Screening/X/raw/supplement provenance, Ledger/Completeness + criteria/prompt/schema bindings). Keep all content-addressed accepts + original checkpoint bytes at original paths. Copy mutable before-State + every present targeted unaccepted canonical output into new owned retention root; record exact present/absent inventory + source refs. Old reviewed targets NOT rebound by equal bytes.
- Evidence need not exist in tool-source commit; record actual source/tool contract separately (committed/loaded/live controls + exact HEAD/tree observations). No current-main refresh or arbitrary schema/contract migration.
- **Candidate accepted graph:** new immutable namespace `R=<source_root>/research/v2/acceptance-revisions/<revision_id>` (safe single-segment, exact Profile-derived root, no latest-scan). Truthful new package/task/result inputs bound to actual pre-revision State + existing Discovery/Screening. Same-State production must NOT pretend issue was `CANDIDATES_NORMALIZED`.
- New Evidence/View accepts = content-addressed new runs under owned R; unchanged complete runs reused ONLY at exact validated immutable refs. Changed cards/Views ALWAYS newly validated complete acceptance, NOT partial overlay. Ledger/Completeness newly generated versioned files under R. Old canonical Ledger/Completeness remain byte-identical, become inactive ONLY after adoption; no canonical overwrite/rebind-by-hash.
- Per affected ID bind old/new full content + reason, newly retained Raw + source/event/clock semantics. New official article must have actual preserved bytes/provenance, NOT Summary quotation. Preserve `INSPECT` ONLY where current task/card/view/ledger validators actually allow non-DROP valid task association; do NOT promote to KEEP/MATERIAL by label. No automatic HOLD→MATERIAL/SELECTED promotion.
- **Review + deterministic proof:** externally supplied author-independent research/authority-consumption decision binds exact before/after graphs, affected IDs, Raw, claimed interpretation (existing reasoning responsibility, NOT new Human Gate, NOT new “Sol” role; historical Sol r11/Plan B is NOT this decision). Do NOT generate genuine PASS inside writer.
- Revalidate COMPLETE proposed graph under current supported contract: package/task/result exact sets/digests; card source/entity/claim/time/access constraints; Views coverage + Evidence binding; Ledger coverage/dispositions/rationales; Completeness obligations + provenance-derived closure; unchanged Discovery/Screening/X/raw + Profile relations; affected allowlist + all unaffected semantic content. Mechanical acceptance-directory/file SHA changes may propagate to unaffected rows, but propositions/status/rationale/content cannot silently change — every such projection explicitly mapped in pre-code, NOT excluded by directory prefix.
- New deterministic proof bound to proposed bytes BEFORE adoption; must NOT call current State acceptance recursively; LIVE eligibility checked by high op separately. Pure final93 validators reusable/extractable; `verify_renewal_source_proof` + publication history/reasons are NOT DM022 admission APIs. Full fresh checks replace no semantic reasoning.

### 3.3 Typed checkpoint + lifecycle truth (§5)

One typed superseding checkpoint: `kind=PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`, truthful reason `REVIEWED_ACCEPTED_UPSTREAM_CORRECTION`. Carries: actual operation lifecycle `EVIDENCE_REVIEWED→EVIDENCE_REVIEWED`, separately named producer boundary `CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED` (re-attested family, NOT fabricated executed transition); exactly checkpoint roles Evidence/Materiality/Completeness + all four named artifacts with full exact refs; before-State source/COPY refs, current Profile, exact predecessor + original anchor, `supersedes`/revision lineage; request/affected-ID/retention-plan refs, proposed-graph proof, supplied research decision, current code/contract/work-ref observations, executor/time/self-digest. Exact field names/schema/digest expressions are pre-code deliverables. Strict new checkpoint-schema branch + truthful supersession proof/report REQUIRED; do NOT forge old `CORE_STAGE_CONTRACT` lifecycle fields.

Record complete BEFORE adoption. **Sole active selection update** = known-byte guarded replacement of canonical State changing `checkpoint_provenance.evidence/.materiality/.completeness` together to SAME new record ref. No second live selector. Lifecycle/passed flags/original forward `history`, Profile/init contract, other checkpoints, Human gates unchanged. Append-only supersession lineage in records; same-state row NOT appended to fixed forward history array.

Agent/checkpoint validation + active resolvers must recognize this kind ONLY in typed research family, verify lineage + same-record triplet, refuse split/mixed authority. Ordinary forward advancement stays forward-only. Standalone/history validation proves retained-basis; high adoption/resume additionally verifies current canonical State vs recorded before/expected-after bytes. Record path/valid proposal is NOT permission token.

Normal consumers must obtain new Ledger/Completeness + Evidence/Views via active State-bound research checkpoint interface. Original canonical files are historical, NOT fallback after supersession. Implementation map mandatory: agent State/checkpoint/build/advance/readback; active Evidence/Views + new active Ledger/Completeness resolution; interactive Evidence candidate-production helpers; Selection/Matrix/Architecture generators + stage validators; downstream Draft/Synthesis/Reader derivation + publication proposal/retention consumers tracing accepted research; operator/handoff/Human Gate preparation; checkpoint/history inspection. Each affected caller resolves new refs or explicitly refuses this mode. No unattached helper or evidence-pointer-only update.

### 3.4 Canonical downstream regeneration — A1 seven slots, guard, order (§§6/11)

Selected **A1: retain/clear exact unaccepted canonical output slots** (NOT versioning every downstream role — A2 rejected). Existing Selection runner produces **seven** outputs (original six-file inventory corrected by §11.1 to include audit). Exact Profile/config/producer-derived paths + any actual conditional outputs enumerated BEFORE code. No fabricated `sources/<issue>` path, broad glob, or arbitrary notes/review deletion.

| # | role | relative slot (validated `source_root`) |
|---|---|---|
| 1 | Matrix | `candidate-matrix-v2.json` |
| 2 | Selection | `candidate-selection-v2.json` |
| 3 | Architecture | `architecture-v2.json` |
| 4 | Architecture summary | `architecture-review-summary-v2.json` |
| 5 | Architecture attention | `architecture-review-attention-v2.json` |
| 6 | Interactive input archive | `orchestration/v2/interactive/selection-architecture-input.json` |
| 7 | Interactive audit | `orchestration/v2/interactive/selection-architecture-audit.json` |

Preparation records which slots present, copies exact bytes to retained storage. Before clearing, prove each is unaccepted, NOT Human-reviewed/request-bound, unchanged since capture, in fixed invalidation plan. Unknown/foreign/changed files refuse; absent entries do NOT become deletion permissions. Normal regeneration must produce fresh Matrix/Selection/Architecture package vs new accepted graph, fresh independent reasoning, ordinary Architecture Human Gate later.

Here all seven are **absent** (route-map-data `outputs_absent` for both editions) — retention inventory is currently trivially absent, but MUST still be recorded as exact absent inventory before adoption. Successor normal runner no-overwrite/preflight MUST cover all seven INCLUDING audit (runner `101–114,304–307` + per-write preflights; audit slot previously unchecked, now required).

**Missing files do NOT block normal generator** — its usual precondition. “Clear while State-old, consumers block because files missing” proposal is rejected. Use scoped exclusive transition guard, checked by affected operational producers/advance/Gate prep at entry + before publishing outputs. Coordination, NOT second authority pointer. Unknown/unreadable/mismatched guards fail closed. Strict read-only State/history diagnosis remains possible; NOT permission to proceed while transition incomplete.

Selected order (§6): `pin current basis → generate/review/prove immutable candidate → retain COPYs/inventory → claim + revalidate guard → complete supersession checkpoint → prevalidate exact expected State → atomic State triplet switch → checked clearing of old unaccepted slots → postread/inventory verification → release owned guard → ordinary regeneration`.

Writer may validate internally constructed expected State as plan, but MUST still validate actual pinned LIVE State BEFORE mutation + actual after bytes AFTERWARD. Must NOT pass synthetic old-lifecycle State to content producers or treat hypothetical State as current authority. No multi-file atomicity/automatic rollback claimed; guarded transition covers pointer adoption + cleanup; incomplete op (new State + old stale drafts) leaves normal producers blocked by guard. Source derivation + role validation also reject stale inputs independently. All coordination-requiring operation consumers concretely inventoried; code cannot begin if unguarded normal writer can regenerate stale outputs in window.

### 3.5 Failure / resume / work-ref rules (§7)

| boundary/observation | required behavior |
|---|---|
| invalid basis, changed ID/Raw/Profile, failed review/content proof, unsupported stage/mode | refuse BEFORE adoption/cleanup; preserve owned inert preparation if already created |
| incomplete candidate/retention | preserve; no same-byte takeover; new attempt uses new id unless specific immutable completed phase has explicit validated continuation |
| complete record, State still exactly before | ordinary adoption refuses existing same-intent; explicit resume reloads record/graph/review/COPY/guard, may switch |
| State exactly expected after, cleanup incomplete | explicit resume verifies active triplet, removes ONLY remaining exact old planned slots; missing already-cleared allowed, foreign/replaced bytes preserved + refused |
| State after, cleanup complete | full readback + readonly ALREADY_ACTIVE/complete result; no new acceptance/approval |
| State neither before nor expected after, or unreadable ownership | INDETERMINATE: preserve records/bytes/guard; no automatic restoration/deletion/adoption |
| write/short-write/fsync/close/replace/postread/guard failure | retain primary/secondary errors + actual old/new/unknown observations; never delete referenced/possibly-referenced records |

Request/preparation binds exact observed HEAD/tree + committed current tool/schema/contract files + full live evidence pins. High finalization/adoption takes expected work HEAD/tree check + rereads them; NO future self-containing commit SHA required. Artifact-only descendant commit during review admissible ONLY if ancestry + exact changed-path set explained by declared attempt input/output/review records, every prior pin unchanged, current controls/contract identical. Otherwise refuse, new bounded attempt; no standing main-follow/generic dirty allowance. Pre-code map MUST supply this predicate + complete path set.

Capture atomicity/rollback wishes are requirements to evaluate, NOT proof files can be changed atomically. Retention + explicit resume preserve authority; they do NOT certify crash atomicity, global CAS, creator authenticity. Review/QA validators check supplied evidence; they do NOT manufacture genuine assessment.

## 4. HIGH vs LOW supplement path — the decisive operability point

### 4.1 Recorded limitation (from authorized repair DATA, not new source read)

- `notes/rephase-1-evidence-scaling-repair/astra-closeout-resolution.md` §76: **“HIGH's existing revision-package producer does not carry authority supplements. This repair does not add that capability. The supplemented lower package-path API is tested; do not label a no-supplement HIGH fixture as proof of supplemented HIGH production.”**
- `test-preparation.md` §§15–16: `HIGH build_revision_package_from_paths never carries authority_supplement and HIGH request builder sets supplement_manifest: None with no source_bindings, so HIGH prepare/adopt cannot thread supplement cards; the direct LOW package-path case above verifies the selected lower API without pretending HIGH creates it (per §22 disposition).`
- `caller-map.json`: `hot_path run() 678–918`, `explicit_out_unless_root_includes: LOW build_revision_cards_views_from_paths:2325/2345/2348 + LOW accept_revision_evidence_views_from_paths:2454/2459`, `private_add: _supplement_entries_once … _supplement_entries_for_package … _build_card_with_entries … _validate_card_with_entries … _supplement_entries_once`, `threading: re-derive package-linearly at each public boundary with already-resolved acceptance/discoveries; no public context kwarg, no global/epoch cache, no caller dict`.
- `interface-map-r2.md` + `affected-verification` Layer-B: supplemented LOW bulk path proven on bounded revision subset + readback freshness; no-supplement HIGH fixture + private slice does NOT prove supplemented LOW bulk path; actual HIGH package builder appears NOT to carry supp — record pre-existing producer limit rather than adding capability.

Consequence: **normal HIGH prepare path CANNOT be used to author supplemented cards.** Any attempt to thread new body Raw/supplement through `build_revision_package_from_paths` would require a new capability (new producer wiring) — NOT selected, returns to Root, no code until new contract + readiness. The T15 precedent (`test_low_derived_copy_build_accept_readback_with_supplement_raw_succeeds`) is explicit: REAL C-helper 1-child DERIVED chain + REAL A2 state/prepare/decide + HIGH prepare/adopt/readback **(unsupplemented HIGH flow)** + direct LOW `derive_ordinary_root_effective_context` (R≠E oracle) + COPY pin + `check_supersession_record_from_paths []`, PLUS direct LOW public `build_revision_cards_views_from_paths` / `accept_revision_evidence_views_from_paths` on ACTUAL supplemented revision-package copy (real HIGH package + real supplement manifest via real validator; meta SHAs recomputed; schema-valid `source_bindings` in request copy) with genuine retained COPY/request/DCP/SCP: bulk cards cite exact supp authority, FULL PUBLIC card validator `== []`.

### 4.2 Selected normal path that DOES support existing copied + new inputs/supplement

The supported path is **LOW direct package-path for card/view production + HIGH coordination for adoption/guard/resume** — all EXISTING final133 APIs, no caller verified-dict, no private bypass, no new module/source feature:

**LOW bulk builder/acceptance (supplement-capable, existing):**

- `build_revision_cards_views_from_paths(repo_root, rev_root/candidate/package.json, request_abs, results_dir, views_dir, before_copy_path=state_copy)` + `accept_revision_evidence_views_from_paths(...)` + wrappers (`prove_revision_from_paths`, `check_supersession_record_from_paths`, `build_versioned_ledger/completeness_from_paths`) — required keyword-only `request_path` + `before_copy_path` (None refused); `ds_context` true R/E; package/tasks adjacent (from `interface-map-r2.md` §3).
- `LOW never imports runner, no LIVE` (`interface-map-r2.md` §3); same `_build/_validate_card_core`; LOW per-LOW-phase `C` via `_validate_evidence_package_basis_content` with true root; same logical-unit rule; `COPY bytes == request SHA`, `COPY ≠ LIVE path`.
- Private phase supplement context (NOT a caller permission token, NOT a public kwarg/bypass):
  - `_resolve_phase_supplement_context(repo_root: Path, package: dict, *, implementation_sha: str|None, screening_acceptance: dict, discoveries: list[dict], expected_issue_id: str, phase: str) -> PhaseSupplementContext` (validating constructor, phase-local only; checks `package.authority_supplement{path,sha256}` shape → manifest SHA → `validate_evidence_authority_supplement(...,implementation_sha,screening_acceptance,discoveries)` → pins `entries` + `manifest_sha256` + `source_root`; discarded on return/exception; never threaded across publics, no ContextVar/global).
  - `_task_source_dict_for_task(task, ctx)`, `_lazy_phase_source_provider(ctx_factory)` (defers entries until first source-need; CARD_KEYS/identity/basis/entities run BEFORE provider, preserving error/IO order), `_build_card_core(task, meta, package, record, runner, source_authorities)`, `_validate_card_core(card, task, task_sha, package, get_sources)` (early errors before source IO; legacy single-Discovery `source-1` fallback preserved), `_recheck_publication_unit_pins(repo_root, ctx, *, package_path, task_paths, profile_path, state_path, acceptance_paths)` (logical-unit re-hash, package-linear full Raw re-hash under same `implementation_sha`; raises on drift, discards ctx).
  - Publics unchanged (no caller verified-dict/context kwarg/bypass): `task_authority_sources(repo_root,task,package)`, `validate_evidence_card(card,task,task_sha,package,*,repo_root=None)` (supplement+`None` → `requires repository validation context`; non-supplement → Discovery structural, no IO).
  - `_supplement_entries_for_package(impl=None, screening_acceptance, discoveries)` skips ONLY `validate_screening_acceptance` LIVE revalidation, substituting `core.load_json` + `screening.read_jsonl` DATA; historical `_content` cores supply DATA from State-free content validation with true root (`root_records/root_path`), never `verify_state_basis`/`repository_commit_sha`. Owner MUST therefore pass validated `screening_acceptance{issue_id,package_sha256,batches,decisions}`, `discoveries` (effective records, non-DROP coverage exact), `expected_issue_id`, plus `package{authority_supplement,basis{discovery/screening paths+SHAs},prompt/contracts}`; R/E already bound by owner via `resolve_effective_discovery_basis` / LOW `derive_ordinary_root_effective_context` (COPY-only, refuses LIVE path).

**HIGH coordination (unsupplemented flow, still required for adoption):**

- Existing HIGH prepare/adopt/readback wiring for State triplet switch, guard claim/revalidation/release, retention COPY/inventory, supersession record completion, expected-State prevalidation, postread/inventory verification, explicit resume — WITHOUT threading supplement cards through HIGH package producer.
- Guard: `source_root/orchestration/v2/acceptance-revision.guard.json`, checked at mutating entries/prepublish points (`require_research_operation_ready`); unknown/unreadable/mismatched fail closed.
- No public context/bypass flag, no global/epoch/lifetime authority cache, no caller verified-dict, no third mirrored validator, no new runtime module/schema/family, no source-class policy or ordinary3/5/DM0227 semantic change (repair ROOT §5). `implementation_sha=None` in supplement leaf remains DATA loading, NOT LIVE State validation.

This composition uses **existing copied inputs** (original checkpoint bytes, original content-addressed accepts, existing Discovery/Screening/X/raw/supplement provenance, `5ca6f310` W34 outputs + State/Profile/CP preserved) **+ new inputs** (truthful new package/task/result inputs bound to pre-revision State + existing Discovery/Screening; captured bodies as newly retained Raw with actual preserved bytes/provenance; supplement manifest entries for the 4–5 W34 DIDs citing exact `raw_path` + body SHA + section location) **+ supplement** (real supplement manifest via real validator; meta SHAs recomputed; schema-valid `source_bindings` in request copy) — WITHOUT inventing a new engine or adding HIGH supplement carry.

### 4.3 What remains OPEN (B4 + §10) before author code

DM022 §11.3 + precode B4 stay **pre-code OPEN** until the next map binds:

- Actual producer output arguments, filenames, schema fields, current content-validator entrypoints for the LOW supplemented path in THIS selected source (e84/final133, not historical final93 numbers alone).
- Demonstration that old canonical Ledger/Completeness are neither overwritten nor accidentally consumed (exact versioned R paths vs canonical paths; resolver returns new refs or explicitly refuses mode).
- Complete direct canonical-input reader + active four-ref resolver enumeration through later Selection/Architecture/Draft/publication (B2 mandatory completeness gate), exact unaccepted-slot inventory (currently 7 absent — record as absent), phase HEAD/tree predicate + complete path set, owned IO/resume oracles, Profile-specific acceptance predicates (DM016 taxonomy refusal, DM017 union preservation with exact provenance, no fabricated fulfilment, unchanged full validator use).
- Every guard-requiring writer + every post-acceptance consumer through Selection→Architecture→Draft/Reader inventoried; proof no unguarded normal writer can regenerate stale outputs in window.
- Mechanical SHA-propagation mapping for unaffected rows (directory-prefix exclusion forbidden).

Until Astra + author-independent readiness confirm that map, **implementation is BLOCKED** — even for the window-eligible W34 4-IDs. B2/B4 are NOT closed by this applicability note.

## 5. Concrete required artifacts / report / request / reviews / COPY-vs-LIVE / epoch / resume

### 5.1 Required artifacts (owned R + retention + State)

- `R=<source_root>/research/v2/acceptance-revisions/<revision_id>` (safe single-segment, exact Profile-derived root): new immutable package/task/result inputs; content-addressed Evidence/View accepts under R; versioned Ledger/Completeness under R; new Raw with actual preserved bytes/provenance (W34: captured HTML 112KB–1.5MB stdlib-strip bodies, bytes/SHA/`raw_path`/sections already in r2 ledger/raw).
- Retained root: mutable before-State COPY + every present targeted unaccepted canonical output (here: 7 absent — record exact absent inventory with source refs; old reviewed targets never rebound by equal bytes).
- Typed checkpoint record `PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1` (complete BEFORE adoption): lifecycle `EVIDENCE_REVIEWED→EVIDENCE_REVIEWED`, producer boundary `CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED`, roles Evidence/Materiality/Completeness + four exact refs, before-State source/COPY refs, current Profile, exact predecessor + original anchor, `supersedes`/lineage, request/affected-ID/retention refs, proposed-graph proof, supplied research decision, code/contract/work-ref observations, executor/time/self-digest. New checkpoint-schema branch REQUIRED.
- Guard `orchestration/v2/acceptance-revision.guard.json` (claimed + revalidated; coordination, NOT second authority pointer).
- Expected-State prevalidation bytes + postread/inventory verification bytes.

### 5.2 Report

- Truthful supersession proof/report (new-schema branch; do NOT forge old `CORE_STAGE_CONTRACT` lifecycle fields to trick unchanged validators).
- Complete proposed-graph revalidation (package/task/result sets/digests; card source/entity/claim/time/access; Views coverage + Evidence binding; Ledger dispositions/rationales; Completeness obligations + provenance closure; unchanged Discovery/Screening/X/raw/Profile; affected allowlist + unaffected semantic content; mechanical projection map).
- Deterministic proof bound to proposed bytes BEFORE adoption (NOT current-State-recursive; LIVE eligibility high-side only).
- Later normal-stage reports are SEPARATE (post-correction regeneration): `stage-validation/EVIDENCE_REVIEWED-report.json` (`candidate-matrix`+`candidate-selection`) + `EVIDENCE_REVIEWED-reviews.json` (≥1 deterministic `CORE_STAGE_CONTRACT` with `result_path`→report) → `advance-stage` → `SELECTION_COMPLETE`; then `SELECTION_COMPLETE-report.json` (`issue-architecture`+summary+attention) + reviews → `ARCHITECTURE_ESTABLISHED` (pending `ARCHITECTURE_REVIEW`, terminal `HUMAN_GATE_REACHED`). Writer alone never advances State, never records Human approval.

### 5.3 Request

- Exact observed HEAD/tree (`e84` + committed tool/schema/contract SHAs) + full live evidence pins (State/Profile/checkpoint/four refs with bytes/SHAs) + `implementation_sha` handling (supplement leaf `None` = DATA, NOT LIVE).
- Affected-ID allowlist: W34 proposal `15127/16096/21100/18389 (+21095 optional)` — nonempty/unique/subset of known non-DROP Matrix IDs, NO new Discovery IDs, NO Screening change. SP proposal MUST list exact DIDs + distinguish as-of vs current-only roles (D141/D142 correction scope per gap-map G6; D040/D049/D063/D153 HOLD vs fetch; O10 archive scope).
- Retention-plan refs + `request_path` + `before_copy_path` (both required keyword-only, None refused) + `ds_context` true R/E + package/tasks adjacency + `COPY bytes == request SHA` + `COPY ≠ LIVE path`.
- `source_bindings` schema-valid in request copy; meta SHAs recomputed; supplement manifest via real validator.

### 5.4 Reviews

- Externally supplied author-independent research/authority-consumption decision (existing reasoning responsibility) binding exact before/after graphs, affected IDs, Raw, claimed interpretation. Historical r2/SP reviews are history, NOT this decision. Do NOT generate PASS inside writer.
- Independent re-review of corrected cards ONLY (W34: 4–5 cards; SP: D141/D142 scope + O10/archive scope) + complete-graph revalidation. No 319/160 full semantic PASS claimed as part of correction.
- No Human REQUEST_CHANGES fabricated; no Human Gate decision inferred from missing records; no synthetic approval promoted to real approval.

### 5.5 COPY vs LIVE vs history vs current epoch

- **COPY:** mutable before-State COPY + present targeted outputs in owned retention root; LOW `before_copy_path` REQUIRED; `COPY bytes == request SHA`; `COPY ≠ LIVE path`; LOW `derive_ordinary_root_effective_context` COPY-only, refuses LIVE path; historical `_content` cores use true root `root_records/root_path`, never LIVE.
- **LIVE:** strict canonical LIVE State/Profile validation via public `agent.validate_agent_state` (exact path/hash/issue/profile/init provenance); HIGH finalization/adoption validates actual pinned LIVE BEFORE mutation + actual after bytes AFTERWARD; hypothetical/synthetic old-lifecycle State NEVER passed to content producers; expected work HEAD/tree check + reread (no future self-containing SHA required; artifact-only descendant admissible ONLY with explained ancestry/changed-path set + unchanged prior pins + identical controls/contract).
- **History:** all content-addressed accepts + original checkpoint bytes at original paths KEPT; old canonical Ledger/Completeness byte-identical → inactive ONLY after adoption; no overwrite/rebind-by-hash; historical/detached proof State-nonrecursive; prior accepted history validation retains basis, NOT current eligibility.
- **Current epoch:** e84 (`e84a82aca000c990597ea8cf60f548e2ff187bd1` over `48082356`) is the ONLY selected runtime; State init `480` + Profile/Contract8/DCP/SCP unchanged; script-only changes do NOT change Contract8; checkpoint impl `e84`; normal Stage Checkpoint path uses current executing HEAD for new checkpoints. No fresh restart proves normal retry; never hand-repin State/Profile or claim fresh restart as retry proof.

### 5.6 Failure / resume (DM022 §7 binding)

See §3.5 table. Key for supplemental case: pre-first-write fault → zero canonical writes, temp discarded; late fault after earlier accepted output → earlier present/later absent, fail-closed; `State==before` + complete record → explicit resume may switch (ordinary adoption refuses same-intent); `State==expected-after` + cleanup incomplete → resume removes ONLY remaining exact old planned slots; INDETERMINATE → preserve, no auto-restore/delete/adopt; all write/fsync/close/replace/postread/guard faults retain primary/secondary errors + old/new/unknown observations.

## 6. Bounded alternatives (no renewal reuse, no overwrite, no reset, no fake Gate, no repin, no new engine)

### A. Truthful same-State PREARCH correction (DM022 A1) — SELECTED design, implementation-gated

- **What:** §3–§5 full path for W34 4 (+1) DIDs (and SP ONLY after archive decision + pins). LOW supplemented card/view production + versioned Ledger/Completeness under R + typed supersession + guarded triplet switch + checked 7-slot clearing (currently absent-inventory) + ordinary regeneration (fresh Matrix/Selection/Architecture + independent reasoning + ordinary Human Gate later).
- **Preserves:** accepted research/history, original checkpoint bytes, old canonical bytes until adoption, lifecycle/forward-history truth, normal lifecycle conventions, existing validator strictness, no generic verified-dict/bypass/new module.
- **Costs (UNKNOWN, not zero):** typed checkpoint/report/lineage, retained storage, guard/resume coordination, affected-consumer integration, new independent research review, implementation + Weekly+Thematic representative witness (both routes, repeated correction, strict State/CURRENT proof, real PDF/editorial/C→U→U/RELEASED/COMPLETE narrow control, known stale-draft/interruption/malformed/split/wrong-stage/unsupported/stale/metadata/ownership/close/replace/explicit-resume tests), measured cost. Synthetic reviews explicitly nongenuine.
- **Needs before code:** §10 pre-code map + B2/B4 closure + Astra + independent readiness confirmation (see §7 blockers). Partially guarded A1 FORBIDDEN — if guard/consumer map cannot preserve invariants, return A1-vs-A2 comparison before code, do NOT implement partial A1.

### B. Keep Evidence / limit Selection (no State mutation) — honest ceiling if correction rejected

- **W34:** fixed-41 vendor-news architecture EXPLICITLY scoped as **no-paper** (NOT “papers judged irrelevant”); correct page arithmetic to 14–16pp (or tighten P3); keep 4–5 papers as HOLD CONTEXT with per-DID method/redundancy reasons; dossier amends “昇格なし” to “4–5 box pending Evidence update (§5); without update, fixed-41 is no-paper scoped”; 39 non-arxiv per-DID reasons preserved; no promotion, no body citation as claim basis.
- **SP:** HOLD+LIMITATION ceiling: O10 LIMITATION retained, P8 restricted to contract-existence + NOT FOUND (no as-of mechanism narrative); move D040/D049/D063/D153 to HOLD/Appendix-A current-only (or fetch G1/G2 pins); promote D143 Engram to PRIMARY (O13 measured core); re-map V41/Qwen/Kimi numbers to O03/O08 or scope lineage chapters background-only with cut budgets; justify 70+6=76pp per package in technical-utility terms; preserve D119/D162 exceptions, V41 §2.4.3+README DSpark architecture scope, Jev current-only quarantine + no-scope-change honesty.
- **Costs:** no State mutation, no guard, no new checkpoint, no implementation. Limits: cannot cite body snippets, cannot use SUPPORTING paper box, cannot claim D141 historical VERIFIED or D142 contract details, O10 as-of VERIFIED impossible. No renewal reuse, no overwrite, no reset.

### C. Stop for selected capability decision (return to Root) — REQUIRED when operability missing

Triggers (any one blocks code):

- SP G3 archive fetch (3 TypeSafe URLs; api only if load-bearing) needs Root limited archive-access decision; no Human Q1Q2Q3; no active upstream edit here; no broad crawl/Production checkout/code adoption/standing main-follow.
- HIGH supplement-carry enhancement would be a NEW capability — NOT selected; if LOW direct package-path deemed insufficient, return A1-vs-A2 + producer decision before code, do NOT smuggle HIGH wiring change.
- Any missing reader/closure/contract contradiction, unsupported source type (DM016 alias relabel forbidden), incomplete builder silent claim (DM017 union + unchanged full validator required, no fabricated fulfilment), stale HEAD/controls/Raw, missing named obligations, metadata-only “promotion,” ownership/close/replace faults, unguarded normal writer in window, or B2/B4 incompleteness.
- No silent Special narrowing, no alias relabel/obligation drop, no batch deferred-maintenance, no Production refresh/rebaseline, no unselected implementation. No all-maintenance batch or unselected Profile changes.

Rejected as completion in all cases: frozen-HOLD + noncanonical technical supplements as changed active acceptance; accepted-file overwrite/re-pin; hash-only or reason-only admission; fake Human revision; legacy temporary-State acceptance; **post-VALIDATED renewal reuse** (wrong authority/lifecycle for DM022 — renewal requires approved Architecture + `VALIDATED_DRAFT`, preserves upstream research; DM022 is pre-Selection EVIDENCE_REVIEWED same-State research revision). Existing conditional Gate reentry + genuinely new issue remain legitimate alternatives under own conditions, NOT universal same-State solutions. Fully versioning all downstream roles (A2) NOT selected (expands Architecture/Human/Draft/publication resolution + migration).

## 7. Necessity + bounded-operability blockers to Root BEFORE author code

**Necessity (this is a task dependency, NOT an automatic new-feature unit; do NOT implement yet):**

1. W34 paper box (if Human wants it) NECESSITATES upstream correction. Existing Evidence (`technical_claims_accepted:false`, abstract-triage) + packet-DATA bodies cannot support SUPPORTING inclusion. Mechanical eligibility ≠ editorial sufficiency.
2. SP as-of D141/D142/O10 use NECESSITATES correction + historical pins. Current-only bodies + missing D142 body + missing ≤09-21 snapshots cannot support as-of VERIFIED. HOLD+LIMITATION is ceiling otherwise.
3. Page/budget/tiering corrections (W34 arithmetic, SP D143 PRIMARY + lineage justification) are Selection deltas AFTER (W34) or WITH (SP) the Evidence decision — do NOT hide upstream dependency in prose or invent Human REQUEST_CHANGES.

**Bounded operability (W34 4-IDs window-eligible; SP blocked on archive; both blocked on pre-code map):**

1. **W34 window:** EVIDENCE_REVIEWED + no Human review/index/gate + 7 absent + guard absent + same issue/Profile/Discovery/Screening + affected IDs subset of known non-DROP + no new Discovery/Screening change + captured bodies/SHAs/sections already in ledger/raw — SATISFIED on ID/provenance grounds for `15127/16096/21100/18389 (+21095)`. Content sufficiency (bounded AUTHOR_CLAIM PARTIAL claim sets citing exact raw_path+SHA+section) + independent research decision + complete-graph revalidation remain to be authored/reviewed, NOT assumed.
2. **SP window:** ID grounds satisfied for D141/D142 correction scope, but CONTENT blocked — D142 no body, O10 no ≤09-21 snapshots, G1/G2 as-of pins missing. Requires Root limited archive-access decision (G3; G1/G2 ONLY if as-of deployment claimed). No active upstream edit, no Human Q1Q2Q3, no broad fetch selected here.
3. **Supplement path:** HIGH revision-package producer CANNOT thread supplement (recorded limitation). Selected normal path for supplemented cards is LOW direct package-path (`build_revision_cards_views_from_paths` / `accept_revision_evidence_views_from_paths` + `prove/check/build_versioned` wrappers) with private phase supplement context, true-root R/E, COPY-only, no caller dict/bypass/new module — ALREADY implemented in final133/selected source. Using existing copied + new inputs/supplement via LOW + HIGH adoption/guard coordination is operable IN PRINCIPLE, but B4 + §10 map must still bind actual producer args/filenames/schema fields/validator entrypoints + old-canonical non-overwrite proof for THIS e84 source. Until then BLOCKED.
4. **Pre-code completeness (§10 + B2/B4):** exact new module/import/closure/API/CLI/schema/digest/guard/write-set map; actual checkpoint/report branch fields; same-record triplet validation; historical/current proof boundaries; ALL active research + downstream callers (Selection→Architecture→Draft/Reader, NOT just four artifact builders); exact unaccepted-slot inventory (currently 7 absent); phase HEAD/tree predicate + complete path set; owned IO/resume oracles; Profile-specific predicates (DM016 unsupported-type refusal, no alias relabel; DM017 union + unchanged validator, no silent incomplete-builder claim); mechanical-projection map (no directory-prefix exclusion). Astra + independent readiness confirmation REQUIRED before code. New caller flags/verified dicts, skipped predicates, path budgets, unselected schema migrations FORBIDDEN.
5. **Guard/consumer coordination:** every guard-requiring writer + every post-acceptance consumer through Selection→Architecture→Draft/Reader must be inventoried; proof no unguarded normal writer can regenerate stale outputs in window; unknown/unreadable/mismatched guards fail closed. Partially guarded A1 FORBIDDEN.
6. **No forbidden substitutes:** no post-VALIDATED renewal reuse, no accepted overwrite/re-pin, no State reset, no fake REQUEST_CHANGES, no contract repin, no new engine, no generic new reader, no old-script rerun, no generic reader/R4/approval/PDF/Production. Existing source has no generic new reader — do NOT invent one.

**Return to Root:** W34 4-ID correction MAY proceed to pre-code mapping (no new fetch needed; captured bodies only) IF Root confirms the Research-Notes box is wanted and authorizes the bounded §10 map task. SP correction MUST await Root archive-access decision + scope ruling (as-of vs current-only ceiling) BEFORE any pre-code map. Neither proceeds to author code in this unit.

## 8. Bounds + stop

- Using current selected `e84` ONLY + authorized notes DATA (fixed774/c8 + 17 SP URLs/version metadata + P1–P6/publisher intake/supplement captures reused as DATA, never refetched). No new standing crawl, no current-main following, no local Production checkout, no code/weights adoption, no Production mutation.
- No reconstruct Git/status/log/HEAD/Commit readback; any necessary later project Git calls explicitly confined to isolated runtime ONLY (none performed here).
- No ordinary candidate/reconstruct Commit/Push; no Human readback; no network/Production action this unit.
- Whole NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN; quality/adoption/savings OPEN.
- **Human Commit Point — stop; do NOT auto-start pre-code, implementation, rehearsal, R4, or new feature unit.** Ordinary Commit/Push Human-owned.

## Attribution

Applicability analyst DATA synthesis from packet + DM022 contract/implementation/root notes listed in scope. Prior BOUNDED_CLOSEOUT/CANDIDATES_NORMALIZED reviews, r2/SP independent reviews, route-map/supplement observations cited as history, NOT reused as approval. No new Human Gate/Draft/PDF/Selection write claimed. No confirmation of §7 FINAL-BINDING beyond cited reviews.
