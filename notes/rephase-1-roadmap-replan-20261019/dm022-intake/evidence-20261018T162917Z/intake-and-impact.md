# DM-022 intake and roadmap-replan impact

Packet: `notes/rephase-1-roadmap-replan-20261019/dm022-intake/evidence-20261018T162917Z/`
Pins: observed `main` **`c8d0ecc1c9566a2303ad3b4c42635d4b672650e4`**
(`Merge pull request #567 from eariver/release-record/2026-W41-38651145434`,
parents `686fc02a…` / `e49939c4…`);
doc blob SHA **`0a0fe3eb0a8f538a9c8c29455be5cef8f6999d57`**
(`git hash-object` == Contents API `sha`), SHA-256
`fa90ce8792440849df765c4fd54485acaa63cf442df979640174678275e668d7`,
72,465 bytes, 918 lines. Two `gh` API calls (main metadata + single pinned
contents fetch) plus one supplementary Issue #562 metadata/body call; all exit 0,
stderr 0 bytes. Raw responses, decode logs, exit files preserved in packet.
Fixed baseline `774dd39a…` unchanged; prior `afdb3df3…` capture untouched.

## Exact reported problem

**CV2-DM-022 — No lawful pre-Architecture same-State supersession of accepted
Evidence / Edition Views / Materiality** (captured doc lines 738–786).

- Status: **`OPEN_CORE`** (edition-local editorial compatibility planned;
  formal Core bypass NOT yet validated).
- Category: Accepted upstream authority / SHA provenance / pre-Architecture lifecycle.
- Tracking: Issue #562 and umbrella Issue #515.
- First reproduction: `2026-W40` at `EVIDENCE_REVIEWED` (2026-10-10 JST).
  Latest reproduction: `2026-W40` Selection r11 independent review (2026-10-10 JST).

W40 reached canonical `EVIDENCE_REVIEWED` after accepting 37 Discovery records,
37 Screening decisions, 35 Evidence Cards, 35 Edition Views, the 37-row
Materiality Ledger and LIMITED Completeness. Two already-known candidates retained
as `HOLD / TIME_UNRESOLVED` were later found by independent primary-source checks
to have original **issuer-authored, Hugging Face organization-hosted articles**
inside the W40 half-open window `[2026-09-25T22:00:00Z, 2026-10-02T22:00:00Z)`:

- Ai2 AstaBrief 8B official organization article:
  host JSON-LD `datePublished = 2026-10-02T15:19:50.340Z`;
- ServiceNow AutoSynthData official organization article:
  host JSON-LD `datePublished = 2026-10-02T04:01:31.290Z`.

These timestamp values establish the **hosted article event**, not model-weight
upload, code/dataset creation, independent reproducibility, or a first-ever
product-availability instant. The original HTML bytes are not archived in the r11
commit, so re-consumption/retrieval proof is necessary if accepting new official
Evidence.

Sol r11 approved **Plan B as a provisional editorial/materiality direction for
both events**, NOT as canonical Core Selection or a Human Gate decision. The
frozen pipeline cannot replace earlier accepted Evidence/Views/Materiality at the
same lifecycle State:

- `scripts/survey_production_v2.py::transition_state` permits exactly one forward
  step and rejects backward / same-State transitions;
- `scripts/survey_human_gate_v2.py::invalidate_pending_gate` applies to an
  already-reached pending Human Gate and, for Architecture, requires a passed
  Architecture checkpoint — neither condition is met at `EVIDENCE_REVIEWED`;
- frozen Candidate Selection validation rejects `SELECTED` for a matrix row with
  `materiality = HOLD`;
- existing State checkpoint provenance requires SHA-bound canonical attestation
  paths; lifecycle history has a fixed transition shape — appending an event or
  overwriting accepted files is NOT authorized supersession.

The Summary names this `CORE_REENTRY_CONTRACT_GAP`: a **generic shared-Core
governance/authority limitation**, explicitly distinct from CV2-DM-016 (Evidence
source-type mapping) and CV2-DM-021 (post-validated publication correction reason).

Observed W40 impact (unchanged authority):

- Authoritative views remain `29 MATERIAL / 4 HOLD / 2 CONTEXT`; r10
  reviewer-only Selection is `28 SELECTED = 20 PRIMARY + 8 SUPPORTING`,
  plus 1 INSPECT, 4 HOLD, 2 REJECT.
- Proposed Plan B is `31 MATERIAL / 2 HOLD / 2 CONTEXT`; a potential
  `30 SELECTED = 22 PRIMARY + 8 SUPPORTING` is **proposed only**, exact roles
  not finally approved.
- Core Acceptance, checkpoint bytes, `production-state.json`,
  Selection/Architecture State and both Human Gates unchanged. No formal 30-item
  Selection acceptance is authorized.

Edition-local continuity (planned, **not** a Core fix): W40 Muse r12 instruction
retains the **Core-valid existing 28 selected candidates**, corrects
reviewer-preview HOLD rationales without claiming accepted upstream revisions, and
stages two non-canonical, evidence-sourced technical supplements for Sol review.
The supplements are **NOT Core SELECTED, NOT formal Architecture packages, and NOT
approved publication appendices**. The user requires Core changes to be maintained
**only in a separate Core task**; Weekly/Special must not patch shared Core,
weaken frozen validators, spoof Gate records, or silently edit accepted authority.
`EDITION_WORKAROUND` is to be marked only after a lawful edition-local execution
path is verified. The gap remains `OPEN_CORE` regardless of editorial progress.

Required future Core direction (handled separately, **not during edition
production**): a reviewed, tightly gated **append-only same-State upstream
authority supersession** at `EVIDENCE_REVIEWED`, before Selection and all Human
Gates, bound to exact work HEAD/Tree, reviewed main/Core identity, old accepted
SHA graph, affected-ID allowlist and explicit Sol decision; preserve immutable old
authority bytes, record old-to-new SHA lineage, deterministically revalidate
Evidence/Card/View/Materiality/Completeness and force new Matrix/Selection preview
generation; preserve original Discovery/Screening `INSPECT` when actually
compatible with frozen validators, expanding scope only with proof; explicitly
reconcile canonical checkpoint path binding, history schema constraints and frozen
implementation-SHA binding; no direct checkpoint overwrite, manual State rollback
or forged Human `REQUEST_CHANGES`; fail closed on stale HEAD, unsupported source
clock/role, mismatched candidate IDs, non-idempotent replay, unapproved Human
reviews or any post-Architecture edit; test Weekly and non-Weekly profiles.

## Authoritative status vs secondary claims

Authoritative (directly read in this intake):

- The captured Summary text at pinned commit `c8d0ecc1…` / blob `0a0fe3eb…`
  (byte-verified: `git hash-object` == API `sha`).
- Issue #562 metadata + body, fetched read-only in this intake: **state `open`**,
  no labels, 0 comments, created = updated = 2026-10-10T09:37:43Z, never closed.
  Its 7-point bounded Core-enhancement/acceptance contract (reviewed same-State
  supersession op with HEAD/Tree/SHA guards, versioned new accepts + append-only
  supersession record, full revalidation, negative tests on Weekly + another
  profile, implementation in a separately authorized Core maintenance branch —
  no W40 hotfix) corroborates the Summary entry point-for-point, including the
  W40 branch `weekly/2026-W40-v2-work` r11 HEAD `5b63d0c9…` and reviewed main
  `afdb3df3…` (the DM-021 capture commit).

Secondary (reported, deliberately not independently read — no authority adopted):

- The seven `sources/2026-W40/execution/…` defect/ledger/feasibility/
  counterfactual/decision/instruction records listed as direct evidence
  (doc lines 772–778); Sol r11 scope decision contents beyond what Issue #562
  quotes; W40 r12 edition-local execution outcome (Summary records it as
  *instructed, not yet validated*).
- Umbrella Issue #515, prior W41 Suggestion r1.0/r1.1 rows (DM-002 recurrence,
  no new ID), and the `83f581eb…` self-reported last-reviewed main, whose delta
  from pinned `c8d0ecc1…` was not diffed (outside authorization).

## Roadmap-replan implications (read-only assessment, no fix implemented)

1. **DM-022 is a Core-governance gap, not edition content.** It constrains any
   replan that touches accepted upstream authority (Evidence/Cards/Views/
   Materiality/Completeness) at `EVIDENCE_REVIEWED` pre-Architecture: there is
   currently no lawful same-State supersession operation. Replan must treat
   accepted W40 authority (29 MATERIAL / 4 HOLD / 2 CONTEXT, 28 SELECTED) as
   frozen and Plan B / 30-SELECTED as provisional-only until a separately
   authorized Core repair lands.
2. **No reconstruct impact by default.** Reconstruct's frozen baseline `774dd39a…`
   predates the frozen Production Line contract in the same way; DM-022 concerns
   live Production `survey_production_v2.py` / `survey_human_gate_v2.py` lifecycle
   transitions, which reconstruct does not execute. No reconstruct source/fixture
   change follows from this intake.
3. **DM-021 stays independent.** The Summary and Issue #562 both distinguish
   DM-022 (`CORE_REENTRY_CONTRACT_GAP`, pre-Architecture) from DM-021
   (post-`VALIDATED_DRAFT` reason class) and DM-016 (source-type taxonomy).
   Do not batch them into one repair without the Summary §8 restart-contract
   deduplication, which belongs to a Human-resumed Core maintenance cycle —
   explicitly out of scope here.
4. **Next replan input, if Human continues:** the unresolved primary evidence is
   the W40 r12 edition-local execution outcome and the `sources/2026-W40/…`
   records — fetchable only under a new explicit authorization, not presumed.
   The W40 guarded-stop State (Selection/Human Gates pending) means the item may
   still evolve on the Production Line; this capture is pinned at `c8d0ecc1…`
   and must not be treated as a standing refresh.

## Scope and limits of this intake

- Exactly three `gh api` read-only calls (main metadata, one pinned document,
  one issue metadata/body); transcripts in `api-calls.md`. No code/tree/refs/
  comments/corpora fetch; no writes of any kind.
- Prior captures (`d6381568…`, `afdb3df3…`) untouched; baseline `774dd39a…`
  unchanged; no rebaseline or adoption inference.
- No historical runner was executed; no fixtures/tests were read or run.
- This adds a scoped DM-022 disposition. Earlier DM-021 (21st) and prior-20
  dispositions keep their recorded scopes; no all-item re-audit was performed.

## Astra-requested correction (overrides as noted, 2026-10-19 JST; no network used; raw captures intact)

The original analysis above is preserved for audit; the following corrections
override it where they conflict.

1. **Implication 2 ("No reconstruct impact by default … which reconstruct does
   not execute") is FALSE and superseded.** Isolated candidate tests do execute
   lifecycle transitions, and reconstruct targets system architecture including
   accepted upstream corrections. **DM-022 is material architectural/acceptance
   input**: it affects practical operability and cost of any replan touching
   accepted upstream authority (Evidence/Cards/Views/Materiality/Completeness),
   and it requires explicit source-grounded applicability/disposition before
   integrated readiness. This is not an automatic fix, not an all-22 batch, and
   not a live-Production write permission.
2. **Implication 3 is partially superseded.** DM-021 and DM-022 have distinct
   state/review predicates (post-`VALIDATED_DRAFT` reason class vs
   pre-Architecture same-State supersession) but **may share design principles**
   (SHA-bound authority, append-only lineage, fail-closed refusal); shared
   principles may inform replan analysis without batching the repairs. Summary
   §8 is **production's reported restart process, NOT a higher-priority
   prohibition** on Human-authorized reconstruction planning.
3. **"Authoritative" is qualified.** The three GETs prove capture fidelity only:
   exact Summary bytes pinned at `c8d0ecc1…` and Issue #562 state/text as
   captured. They **cannot prove the underlying technical/edition reproduction**.
   "Authoritative" above means *primary captured issue status/text*; the W40
   technical facts (host timestamps, authority counts, Sol decision substance,
   r12 outcome) remain unreproduced secondary evidence.
4. **Scope bullet corrected:** "no writes of any kind" is wrong. Correct scope
   is **no Production writes**; local packet files were written as the
   authorized durable record (this packet itself is the write).
5. **Continuation is delegated, not gated.** The user explicitly delegates
   replan/next-task selection and continuation. This packet **invents no new
   Human approval gate for every analysis step**; the README stop-line records
   intake completion, not a gate requirement.
