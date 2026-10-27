# DM022 pre-Architecture operator / alternatives analysis (AUTHOR-side, DESIGN-only)

2026-10-26. AUTHOR-side design analysis, independent work from the accepted Graph.
No implementation, no tests/build/fixtures/source/runtime/Git writes/Production
refresh. Read-only source inspection only.

## 0. Inputs and method

- Instruction: assessment §5 (`outputs/rephase-1-versioned-renewal-implementation-assessment.md`
  §§1–5, esp. §5), root closeout
  (`notes/rephase-1-versioned-renewal-implementation/astra-closeout-resolution.md`
  §§1–7, esp. §6).
- Narrow DM022 capture only (no network, no re-fetch):
  `notes/rephase-1-roadmap-replan-20261019/dm022-intake/README.md`,
  `notes/rephase-1-roadmap-replan-20261019/dm022-intake/evidence-20261018T162917Z/intake-and-impact.md`
  (including Astra-requested correction §§168–201),
  `dm022-source.json`, `issue562-api.json` body (LEN 5180, extracted read-only),
  `deferred-maintenance-summary.md` (918 lines, SHA256
  `fa90ce8792440849df765c4fd54485acaa62cf442df97964017467825e668d7`,
  blob `0a0fe3eb…`, pinned commit `c8d0ecc1…`).
- Source READONLY: final93 proof-copy
  `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`
  (actual409/tree8ce + 93 paths 40M53A, DIRECT409 patch
  `f898d33bfe6904fd29063c4f08a6176e7bd02b234d2c6a3a2d505614941da2a`).
  Prior Worker-B failure mode (source-unread) was explicitly avoided: every
  API claim below was read in that tree. No imports/tests/build/fixture/source/
  runtime/Git writes.
- This file is the ONLY new file:
  `notes/rephase-1-dm022-prearchitecture-contract/operator-alternatives-analysis.md`.
  Root author selection review is separate. No independent PASS/adoption,
  no implementation until root decision.

## 1. Accepted-Graph starting point (DM022, W40)

Authoritative (captured bytes, not reproduced technical facts; per intake
correction, "authoritative" = primary captured issue status/text):

- `CV2-DM-022 — No lawful pre-Architecture same-State supersession of accepted
  Evidence / Edition Views / Materiality`, status `OPEN_CORE`, Issue #562
  (open, 0 comments, created=updated `2026-10-10T09:37:43Z`) + umbrella #515.
- First/latest reproduction `2026-W40` at `EVIDENCE_REVIEWED` / Selection r11
  (2026-10-10 JST). W40 branch `weekly/2026-W40-v2-work`, r11 HEAD
  `5b63d0c9…`, reviewed main `afdb3df3…` (DM021 capture commit).
- Accepted authority frozen: `29 MATERIAL / 4 HOLD / 2 CONTEXT`; r10
  reviewer-only Selection `28 SELECTED = 20 PRIMARY + 8 SUPPORTING` (+1 INSPECT,
  4 HOLD, 2 REJECT). Sol r11 Plan B provisional `31 MATERIAL / 2 HOLD /
  2 CONTEXT`, potential `30 SELECTED = 22 PRIMARY + 8 SUPPORTING` **proposed
  only**, exact roles not approved. No formal 30-item Selection acceptance.
  Core Acceptance, checkpoint bytes, `production-state.json`,
  Selection/Architecture State, both Human Gates unchanged.
- Two already-known `HOLD / TIME_UNRESOLVED` candidates later found to have
  issuer-authored, Hugging-Face-organization-hosted articles inside W40
  half-open window `[2026-09-25T22:00:00Z, 2026-10-02T22:00:00Z)`:
  Ai2 AstaBrief `datePublished=2026-10-02T15:19:50.340Z`;
  ServiceNow AutoSynthData `datePublished=2026-10-02T04:01:31.290Z`.
  Timestamps establish hosted-article event, not weight/code/dataset upload,
  independent reproducibility, or first product-availability instant. Original
  HTML bytes not archived in r11 commit; re-consumption/retrieval proof
  necessary if accepting new Evidence.
- Sol r11 approved Plan B as provisional editorial/materiality direction for
  both events, NOT canonical Core Selection or Human Gate decision.
- Issue #562 7-point bounded Core-enhancement/acceptance contract (body §§
  "Requested bounded Core enhancement"): (1) only at `EVIDENCE_REVIEWED` with
  Selection/Architecture pending, both Human Gates pending + null provenance,
  explicit Sol scope decision; (2) fail-closed HEAD/Tree/main-SHA guards, exact
  base `checkpoint_provenance`, old acceptance SHA, changed-ID allowlist, no
  force-push/reset; (3) preserve old bytes + SHA traceability, versioned new
  accepts + append-only supersession record old→new + reviewer decision;
  (4) new Evidence/Card authority must include original hosted issuer articles,
  preserve Discovery/Screening provenance, FIRST determine whether accepted
  `INSPECT` Screening permits new Evidence/Views/Materiality without 37/37
  regeneration (`derive_candidate_matrix` derives from Evidence/View/
  Materiality, `validate_selection` rejects HOLD materiality, neither directly
  tests KEEP Screening); (5) revalidate 35 Evidence/Card↔View, 37-row Ledger,
  Completeness, Matrix/Selection preview, timestamps/roles, State stays
  `EVIDENCE_REVIEWED`, no Selection advance until Sol approves; (6) negative
  tests (stale HEAD/SHA, unauthorized ID, human review present, beyond-evidence
  stage, bad timestamp, missing source/hash, failed validators, incongruent
  Evidence/View, forced backward transition, idempotent replay), Weekly +
  another profile, no unrelated edition mutation; (7) separately authorized
  existing Core maintenance branch, normal PR merge, no W40 hotfix.
- Distinct from DM016 (source-type map) and DM021 (post-`VALIDATED_DRAFT`
  reason class). Intake correction: DM021/DM022 share design principles
  (SHA-bound authority, append-only lineage, fail-closed refusal) but must not
  be batched; Summary §8 is production restart process, not a prohibition on
  Human-authorized reconstruction planning.

## 2. What is CURRENTLY legal at `EVIDENCE_REVIEWED` (exact triggers)

All paths below cite final93 proof-copy bytes. `EVIDENCE_REVIEWED` means
(`config/survey-production-v2.json:307-315,218-225`):
`lifecycle_state=EVIDENCE_REVIEWED`, `next_action=stage:selection`,
`terminal_reason=null` (no `gate_at_state` entry), checkpoints
`evidence/materiality/completeness=passed`, `selection=pending`, both Human
Gates `pending` with null provenance. At W40, additionally, review-index empty
(no Human review yet), architecture checkpoint not passed.

### 2.1 Legal today: run the normal forward Selection stage ONCE

- `scripts/survey_production_v2.py:998-1048 transition_state()`:
  exactly one forward step (`target_index != current_index+1` refused),
  requires exact passed checkpoint updates + provenance updates matching
  `stage_plan[current].checkpoints`. At `EVIDENCE_REVIEWED` the only legal
  target is `SELECTION_COMPLETE` with `selection=passed`.
- `scripts/survey_agent_control_v2.py:1768-1826 advance_with_checkpoint()`:
  same forward-only shape (`from_state==current`, `to_state==stage[next_state]`,
  checkpoint set must match, contract + implementation identity must match
  current tool, resumable State via `validate_agent_state`).
- `scripts/run_selection_architecture_v2_interactive.py:158-201 run()`:
  requires `lifecycle_state==EVIDENCE_REVIEWED`, resolves active Evidence/Views
  via `agent.resolve_active_evidence_views` (checkpoint-bound, §2.4), derives
  Matrix via `architecture.derive_candidate_matrix`, validates, then
  **refuses to overwrite** any of `candidate-matrix-v2.json`,
  `candidate-selection-v2.json`, `architecture-v2.json`,
  `architecture-review-summary-v2.json`, `architecture-review-attention-v2.json`,
  `orchestration/v2/interactive/selection-architecture-input.json`.
  This runner never advances State, never records Human approval.
- `scripts/survey_handlers_v2.py:250-280 _selection_basis/validate_selection`:
  Matrix/Selection validated against the CURRENT checkpoint-bound
  Evidence/Views/Ledger/Completeness (`_evidence_basis`), with
  `_same_authority` input→output binding. With old HOLDs retained, frozen
  Selection validation rejects `SELECTED` for HOLD rows (legacy
  `candidate_selection_gate.py:169-176` documents the same rule for the old
  Weekly gate; Core v2 `survey_architecture_v2.validate_selection` enforces
  HOLD-materiality rejection per DM022 intake §48/§55).
- Consequence: the forward Selection path is legal but preserves the DM022
  defect — Plan B 30-SELECTED cannot pass while the two HOLDs remain HOLD.
  Running it does not correct Evidence/Views/Materiality.

### 2.2 NOT legal at `EVIDENCE_REVIEWED`: any Human APPROVED / REQUEST_CHANGES

- `scripts/survey_human_gate_v2.py:681-… record_architecture_approval()`
  (and `agent.approve_architecture:1829-1903`): requires
  `lifecycle_state==ARCHITECTURE_ESTABLISHED` + `human_gates.architecture_review==pending`
  + passed `architecture` checkpoint + immutable `PROPOSED` Architecture +
  `READY_FOR_ARCHITECTURE_REVIEW` summary binding exact Architecture SHA.
  None holds at `EVIDENCE_REVIEWED`. Cannot invent an approval.
- `scripts/survey_human_gate_v2.py:1350-1425 request_changes()` (+
  `request_architecture_revision`, `request_publication_preview_revision`):
  requires `_validate_gate_pending` (pending gate at `GATE_STATES[gate]`),
  exact reviewed State/artifacts/commit, non-empty `requested_changes`,
  `reviewed_by/reviewed_at/review_reference`, allowed
  `human_gate_revision_boundaries[gate]` preceding the gate state, then
  `_revised_state` (history truncation to `target_index+1`, checkpoint
  clearing, `publication_revalidation_provenance=None` if validation
  invalidated) + superseded-path removal + `agent.validate_agent_state`.
  At `EVIDENCE_REVIEWED` there is no pending gate (`_current_pending_gate`
  raises "no configured pending Human Gate"), so neither `APPROVED` nor
  `REQUEST_CHANGES` can be recorded. A fabricated `REQUEST_CHANGES` or fake
  approval to "force the existing path" is explicitly forbidden by Issue #562
  ("Do not … spoof Human Gate input") and by authority
  (`docs/survey-production-core-v2-authority.md:265-266` — no Human record
  without a real decision).
- Publication cross-gate `REQUEST_CHANGES` to a pre-`ARCHITECTURE_ESTABLISHED`
  boundary additionally requires active approved Architecture
  (`_superseded_gate_authority_paths:924-941`, `_revised_state:986-993`);
  not present at `EVIDENCE_REVIEWED`.

### 2.3 NOT legal at `EVIDENCE_REVIEWED`: operator pending-gate invalidation

- `scripts/survey_human_gate_v2.py:1179-1347 invalidate_pending_gate()`:
  exact triggers (all must hold): `gate in GATE_KEYS`; non-empty
  `reason/operator_reference/expected_work_branch_head`;
  `_current_pending_gate` == requested gate (lifecycle must be
  `GATE_STATES[gate]`, gate `pending`, provenance null,
  `terminal_reason==HUMAN_GATE_REACHED`); for `ARCHITECTURE_REVIEW`,
  `machine_checkpoints.architecture==passed`; never cross active Architecture
  approval for `PUBLICATION_PREVIEW`; `regeneration_boundary in
  operator_pending_gate_invalidation_boundaries[gate]`; review index has NO
  reviews; invalidated commit == current HEAD == committed review surface;
  expected work-branch head matches `refs/remotes/origin/<work_branch>` (or
  local); Gate surface validates (`_validate_pending_gate_surface`: for
  Architecture, `PROPOSED` + `READY_FOR_ARCHITECTURE_REVIEW` + summary binds
  exact Architecture SHA); then `_revised_state` with allowed boundaries,
  checkpoint/canonical cleanup, immutable operator record
  (`human_decision=false`, prior State/inputs/commit, invalidated checkpoint
  authority, superseded canonical paths), resumable State via
  `agent.validate_agent_state`, with full rollback on failure.
- Config (`config/survey-production-v2.json:256-265`):
  `ARCHITECTURE_REVIEW: [ISSUE_INITIALIZED … SELECTION_COMPLETE]`,
  `PUBLICATION_PREVIEW: []`. Gate→state: only `ARCHITECTURE_ESTABLISHED →
  ARCHITECTURE_REVIEW`, `RELEASE_CANDIDATE → PUBLICATION_PREVIEW`.
- At `EVIDENCE_REVIEWED`: no `gate_at_state` entry, terminal is null not
  `HUMAN_GATE_REACHED`, architecture checkpoint not passed, Gate surface not
  presented. `_current_pending_gate` fails closed. There is no generic
  pending-override: a `PUBLICATION_PREVIEW` invalidation is configured with
  zero allowed boundaries, and `ARCHITECTURE_REVIEW` invalidation cannot run
  before `ARCHITECTURE_ESTABLISHED`. Cannot repurpose it for upstream
  Evidence correction (Issue #562: "never … repurpose pending-Gate
  invalidation").

### 2.4 Active authority is checkpoint-bound; new files alone change nothing

- `scripts/survey_agent_control_v2.py:902-938 resolve_active_evidence_views()`:
  active Evidence + Views come from ONE State-bound `evidence` checkpoint
  (`resolve_checkpoint_artifact` for `evidence-acceptance` +
  `edition-views-acceptance`), same `checkpoint_authority`, View must bind
  exact Evidence SHA. Historical accepted dirs are inert storage; directory
  order/mtime/latest heuristics are never authority
  (`docs/survey-production-core-v2-authority.md:258-261`).
- `scripts/survey_evidence_v2.py:1159-1213 accept_evidence_results()` and
  `1498-1552 accept_edition_views()`: append-only content-addressed
  (`accepted_root/<result_set_sha>/evidence-accepted.json`,
  `accepted_root/<view_set_sha>/edition-views-accepted.json`), idempotent only
  on identical bytes, refuse overwrite with different manifest, validate
  package basis + card/view bindings. Generating a NEW immutable accept is
  allowed as file creation, but it does NOT become active authority without a
  checkpoint update — and no current API updates the `evidence` checkpoint
  while staying at `EVIDENCE_REVIEWED` (forward `transition_state`/`advance`
  leaves `EVIDENCE_REVIEWED`; `_revised_state` requires a Human gate).
  In-place overwrite of an accepted file breaks `sha256_file` provenance
  checks (`validate_state_semantics`, `_validate_checkpoint_record`,
  `_check_evidence_acceptance_results_content`) and is fail-closed drift, not a
  lawful correction.
- `scripts/survey_evidence_v2.py:1579-1655 build_materiality_ledger()` +
  completeness (`survey_handlers_v2._evidence_basis:204-238`): Ledger and
  Completeness are derived from the SAME bound Screening/Evidence/Views set
  (exact SHA bases, no silent DROP, non-DROP exactly one Evidence task in
  WU-007, HOLD mapping enforced). They cannot be regenerated against a
  different Evidence set while the checkpoint still names the old one.

### 2.5 Post-Screening supplement ≠ supersession

- `scripts/survey_evidence_v2.py:188-360` Evidence Authority Supplement:
  edition-local manifest binding Raw bytes + SHA + issue/task/Screening basis,
  validated, output refuses overwrite. Per authority
  (`docs/survey-production-core-v2-authority.md:265`), post-Screening primary
  authority may enter Evidence ONLY through an exact supplement; Screening
  decisions and accepted Screening history remain unchanged. A supplement can
  carry the two hosted issuer articles as additional source bodies for named
  tasks, but it does not replace the accepted Evidence/Views/Materiality or
  rebind the active checkpoint. It is a necessary input shape for a future
  supersession, not the supersession itself.

### 2.6 Legacy Weekly revise path is NOT a Core v2 lawful path

- `scripts/revise_weekly_interactive_evidence.py:1-248`:
  append-only pre-selection revision for the LEGACY coarse pipeline
  (`sources/<issue>/pipeline-state.json`, gates
  `candidate_inventory/evidence_normalized/candidate_selection/issue_architecture`).
  Reuses exact prior package bytes + `CANDIDATES_NORMALIZED` basis, expands
  review, stores new result-set SHA + `supersession.json`
  (`PRE_SELECTION_EVIDENCE_REVISION`, `pipeline_state_unchanged=true`),
  restores coarse state bytes after `accept_evidence_results.accept`.
  This is legacy Weekly machinery, not `production-state.json` / Core v2
  checkpoint provenance. It cannot update a Core v2 `evidence` checkpoint and
  must not be cited as a Core v2 precedent. Counterexample: running it on a
  Core v2 edition would create legacy files beside — not inside — the active
  authority chain.

### 2.7 Post-VALIDATED mechanisms are NOT reusable by default

- `scripts/survey_versioned_renewal_v2.py:560-590 _require_renewal_entry_window`
  + `619+ _observe_renewal_entry`: requires healthy `VALIDATED_DRAFT` +
  approved Architecture + pending Preview (no Preview provenance) + pending
  `publication_preview/freeze/release` + inactive Exception. At
  `EVIDENCE_REVIEWED` entry is `BASIS_ENTRY_INELIGIBLE / REFUSED_PRE_WRITE`.
- `scripts/survey_agent_control_v2.py:2323+ revalidate_publication_surface`
  (authority `docs/survey-production-core-v2-authority.md:270`): only at
  `VALIDATED_DRAFT` with approved Architecture, preview/freeze/release pending,
  no Exception; covers ONLY bounded publication-surface roles
  (reader-manuscript/PDF/quality/semantic/visual/Reader Gate), verifies every
  other checkpoint-bound byte unchanged. Upstream Evidence/Views/Materiality
  are explicitly out of scope.
- Assessment §5 and closeout §6 forbid treating post-`VALIDATED_DRAFT`
  renewal as a pre-Architecture correction ("no post-VALIDATED renewal reuse
  by default", "no accepted-input overwrite, hash-only admission"). Renewal
  preserves old accepted lineage for publication regeneration; DM022 needs new
  accepted upstream authority BEFORE Selection/Architecture. Conflating them
  would bypass Sol review, Human Gates, and downstream invalidation.

## 3. Alternatives comparison (before Architecture)

| # | Alternative | What it does | Lawful today at `EVIDENCE_REVIEWED`? | Why / exact block |
|---|---|---|---|---|
| A | Normal forward Selection → Architecture → Gates (existing agent/controller + orchestrator) | Derive Matrix/Selection/Architecture from CURRENT checkpoint-bound accepts, advance `EVIDENCE_REVIEWED→SELECTION_COMPLETE→…` | Legal but DOES NOT FIX DM022 | Binds old HOLDs; Selection validator rejects HOLD→SELECTED. Produces the frozen 28-SELECTED or a refused 30-SELECTED, not Plan B. |
| B | Same-State upstream supersession (Issue #562 7-point contract) | Keep old bytes, generate versioned new Evidence/Views/Materiality/Completeness + append-only supersession record, rebind active `evidence` checkpoint WITHOUT lifecycle advance, State stays `EVIDENCE_REVIEWED`, no Selection until Sol approves | NOT YET lawful — the missing operation | No current API updates `evidence` checkpoint provenance while staying at same lifecycle with history-length preservation. Requires new reviewed Core op (see §6). |
| C1 | Whole-stage replay (re-run evidence/materiality/completeness stage from `CANDIDATES_NORMALIZED`) | Re-execute full handler chain, new accepts for all 37/35/37 rows | No lawful trigger | Would require backward transition (`EVIDENCE_REVIEWED→CANDIDATES_NORMALIZED`); `transition_state` is forward-only; `_revised_state` requires a Human gate; `initialize` refuses when profile/state exists (destructive re-init). Replay outputs would be inert files, not active authority. |
| C2 | Dependency-cut regeneration (only changed 2 HOLD chains + Ledger/Completeness/Matrix preview) | Regenerate only affected task/card/view rows + derived Ledger/Completeness deltas | No lawful trigger (same as C1 for activation) | Generation is cheap; ACTIVATION is the gap. Dependency-cut also needs the §6 checkpoint-rebind rule + proof that untouched rows are byte-identical and still bound. Otherwise risks partial-join (Evidence from run N, Views from run M) which `resolve_active_evidence_views` explicitly forbids (same-checkpoint-authority check). |
| D1 | Immutable new accepts + active checkpoint selection (proposed) | Old accepts preserved content-addressed; new run dirs + supersession record; explicit checkpoint-rebind op selects new `evidence` checkpoint authority | Proposed lawful shape (see §6) | Matches accept-file idempotence + `resolve_active_evidence_views` same-authority invariant. Needs new op; no overwrite. |
| D2 | Accepted-file overwrite / hash-only admission | Mutate accepted JSON/JSONL in place, or admit new set by SHA match alone | FORBIDDEN | Breaks `sha256_file` provenance, checkpoint-record artifact SHA, `_check_*_content` digest identity; Issue #562 and assessment §5 forbid "accepted input overwrite" and "hash-only admission". |
| E | Operator pending-gate invalidation at `EVIDENCE_REVIEWED` | Use `invalidate_pending_gate` with a configured boundary to rewind to `CANDIDATES_NORMALIZED` or `EVIDENCE_REVIEWED` | NOT APPLICABLE | §2.3: no pending gate at `EVIDENCE_REVIEWED`, terminal null, architecture not passed, review-index rule. `PUBLICATION_PREVIEW` has zero allowed boundaries. Cannot invent a generic pending override. |
| F | Human `REQUEST_CHANGES` / fake approval at `EVIDENCE_REVIEWED` | Record rN revision or approval to rewind/advance | FORBIDDEN | §2.2: no pending gate, no `PROPOSED` Architecture, no `READY` summary. Fabricating either violates Human-decision semantics (AGENTS.md session-bootstrap: Human owns `APPROVED` vs `REQUEST_CHANGES`, boundary, requested changes; ChatGPT/Core never infer). |
| G | Edition restart / new issue (`init-weekly`/`init-thematic`) | Fresh `production-state.json` history length 1, new `source_root`, re-run intake with corrected retrieval | LAWFUL but LOSSY | `survey_production_v2.initialize:1051-1071` refuses if profile/state exists — requires a NEW issue id or archival of the old tree (new provenance chain, not same-State continuity). Preserves nothing automatically; old→new lineage must be recorded manually. Breaks W40 continuity, doubles X-intake/Screening/Evidence cost, invalidates r10/r11 review history as active authority (preserved only as historical evidence). Legitimate fallback if §6 is rejected, but it is NOT same-State supersession and must not be mislabeled as such. |
| H | Legacy `revise_weekly_interactive_evidence` on Core v2 | Append-only legacy revision + `supersession.json`, state unchanged | NOT APPLICABLE to Core v2 | §2.6: legacy `pipeline-state.json` only. Would create sidecar files outside Core v2 checkpoint provenance. |
| I | Post-`VALIDATED_DRAFT` renewal or `revalidate_publication_surface` | Reuse renewal `REVIEWED_VERSIONED_CORE_RENEWAL` / revalidation pointer | FORBIDDEN by default | §2.7: entry window is `VALIDATED_DRAFT` + approved Architecture + pending Preview. At `EVIDENCE_REVIEWED` ineligible. Different reason class (DM021 vs DM022), different lifecycle, different downstream scope. |

## 4. What must KEEP / new obligations / invalidated downstream

### 4.1 KEEP (immutable, never overwritten)

- Raw/imported evidence: immutable accepted Raw bytes incl. Grok result bytes,
  X manifest/instruction/prompt/result provenance where used
  (authority §8: "Retain immutable accepted Raw bytes … exact active Evidence/
  View authority reviewed by Sol").
- Old accepted runs: all prior Screening/Evidence/View acceptance dirs
  (content-addressed `result_set_sha` / `view_set_sha`), prior packages
  (`package.json`), task/result copies, validation reports.
- Previous checkpoints: every passed Stage Checkpoint record
  (`orchestration/v2/attestations/<checkpoint>.json` + `agent_checkpoint_dir`
  records) with exact `{path,sha256}` provenance; `checkpoint_provenance`
  entries for `discovery/screening/evidence/materiality/completeness`.
- Review history: `history` array (length must exactly match lifecycle index,
  `validate_agent_state:678-700`), `gates/reviews/*-rN.json`,
  `gates/reviews/approvals/*-rN.json`, `gates/review-index.json` (must stay
  empty until a real Human gate), operator invalidation dir
  (`execution/operator-invalidations/`, must stay empty until a real pending-
  gate invalidation), prior `host-timestamp-ledger-r11`,
  `selection-counterfactual-r11`, feasibility report (secondary evidence, Issue
  #562 links).
- Old Matrix/Selection preview (r10 reviewer-only 28-SELECTED) as historical
  evidence, not active authority.

### 4.2 New acceptance obligations

Deterministic (machine-checkable, necessary but NOT sufficient):

- New Evidence package basis revalidation (exact Discovery/Screening/Profile/
  prompt/contract SHA, archived files), per-task Card validation, result-set
  digest identity, View→Evidence SHA binding + materiality/status coherence
  (`REJECTED→NON_MATERIAL`, `NEEDS_MORE→HOLD`), scope-dimension membership in
  Profile, Ledger derivation (no silent DROP, non-DROP exactly one task,
  HOLD mapping), Completeness obligations incl. Discovery-added IDs (DM017
  interaction, §7), Matrix derivation from new Evidence/Views/Ledger/
  Completeness, Selection validation (HOLD rejection now satisfied by
  MATERIAL), Architecture + Review Summary + Attention derivation, Stage
  Checkpoint `CORE_STAGE_CONTRACT` + implementation/contract identity,
  `validate_agent_state` clean, `transition_state`/`advance` preconditions for
  the NEXT forward step only.
- Proof of original hosted issuer articles: archived original HTML bytes (not
  just JSON-LD timestamp claims), retrieval provenance (URL, fetched_at,
  SHA256, byte count), timestamp parsing (`datePublished` values above) with
  explicit semantics (article-publication event, not weight/code/dataset
  availability), source-role mapping (DM016 interaction for Thematic; Weekly
  roles for W40), per-task Evidence/View revalidation.

Semantic (Sol/ChatGPT research adequacy, cannot be reduced to deterministic
PASS; authority §§5–6, session-bootstrap §§7–8):

- Sol authority-consumption review: were substantive primary bodies actually
  read and converted into bounded Evidence claims (capture/binding ≠
  consumption)?
- Sol materiality/Selection review: are both newly MATERIAL announcements
  truly in-window, technically material methods announcements (not conflated
  with artifact-creation predates / unverified standalone implementation per
  Issue #562 editorial decision)?
- Sol completeness/negative-space/compression review: with `31 MATERIAL`,
  is sparse-selection risk handled; `SELECTED<=1 while non-DROP>=20 or
  VERIFIED>=10` compression audit if triggered; strong unselected candidates
  + omissions reviewed.
- Sol Architecture dossier readiness: coverage, authority consumption,
  disposition map, alternatives, limitations, blocking/non-blocking findings —
  BEFORE any `READY_FOR_ARCHITECTURE_REVIEW` claim. `READY`, deterministic
  PASS, or Luna/Work completion never substitutes for this judgment.

### 4.3 Invalidated downstream (precise, with branch bounds)

If the §6 supersession is adopted, the following downstream artifacts derived
from the OLD `evidence` checkpoint MUST be treated as superseded (regenerated,
not patched in place); nothing else is implicitly invalidated:

- `candidate-matrix-v2.json` (owner `EVIDENCE_REVIEWED`,
  `canonical_regeneration_artifacts:269`) — MUST regenerate (new Evidence/
  Views/Ledger/Completeness → new Matrix). Old Matrix bytes preserved
  historically.
- `candidate-selection-v2.json` (owner `EVIDENCE_REVIEWED`) — MUST regenerate
  as preview only; NO Selection approval until Sol approves supersession
  (Issue #562 req. 5). Old r10 reviewer-only Selection preserved.
- `selection-architecture-input.json` (owner `EVIDENCE_REVIEWED`) — MUST
  regenerate (archive of interactive input is per-run; old archive preserved).
- `architecture-v2.json` + `architecture-review-summary-v2.json` +
  `architecture-review-attention-v2.json` (owner `SELECTION_COMPLETE`) —
  NOT YET EXISTENT at `EVIDENCE_REVIEWED`; must NOT be created from stale
  Matrix. After supersession + forward Selection, they are generated fresh.
  No active Architecture approval exists to supersede (unlike Publication
  cross-gate case).
- Draft/publication/Freeze/Release (`DRAFT_COMPLETE→RELEASED`) — NOT YET
  EXISTENT; no invalidation needed. Branch bound: invalidation stops at the
  `evidence` checkpoint + its three derived previews above. `discovery`/
  `screening` checkpoints stay PASSED unless the §6 contract explicitly finds
  a canonical Screening change required (Issue #562 req. 4: FIRST determine
  whether accepted `INSPECT` permits promotion; if Screening change required,
  document + SHA-guard explicitly — that would extend invalidation to the
  `screening` checkpoint and is a larger branch).
- `publication_revalidation_provenance` stays null (validation checkpoint not
  yet passed); history length unchanged (same-State, no new lifecycle row).

## 5. Failure / resume / operator files / normal Gate return

- Failure atomicity precedent: `invalidate_pending_gate:1316-1347` snapshots
  `state_bytes` + cleanup-path bytes, unlinks + writes record + writes state +
  validates resumable, rolls back ALL on exception (record removed, state
  restored, snapshots restored). Any §6 supersession op MUST provide the same
  all-or-nothing guarantee: no partial checkpoint rebind, no half-written new
  accepts referenced as active, no orphaned supersession record.
- Resume: explicit resume only (cf. renewal `resume_renewal_activation`,
  editorial `resume_activation`). `ALREADY_ACTIVE`/idempotent replay must be
  readonly (Issue #562 req. 6: idempotent replay test). Stale HEAD/SHA,
  unsupported candidate ID, Human review present, beyond-evidence stage, bad
  timestamp, missing source/hash, failed validator, incongruent Evidence/View,
  forced backward transition must all fail closed with preserved prior State.
- Operator files: new immutable record type (NOT `operator-pending-gate-
  invalidation-v2`, NOT Human review record): `human_decision=false`,
  prior State/inputs/commit, old→new authority hashes (Evidence/View/Ledger/
  Completeness/Matrix preview), Sol scope decision reference, changed-ID
  allowlist, `recorded_at`, schema-validated, never overwrites existing
  record path, never inside a cleanup target (same discipline as
  `invalidate_pending_gate:1249-1261`).
- Normal Gate return: after supersession, the edition returns to the NORMAL
  forward path — `stage:selection` → `SELECTION_COMPLETE` →
  `stage:architecture` → `ARCHITECTURE_ESTABLISHED` → pending
  `ARCHITECTURE_REVIEW` → Human `APPROVED`/`REQUEST_CHANGES` with full dossier.
  The supersession itself creates NO Human revision, NO `reviewed_by/at`, NO
  approval snapshot. The next Human decision is the ordinary Architecture
  Review r1 (or rN+1 if a prior pending gate existed — not the W40 case).

## 6. Bounded integrated option(s) + counterexamples / capability loss

### Option S (RECOMMENDED for root selection): versioned same-State evidence
supersession with checkpoint rebind, State stays `EVIDENCE_REVIEWED`

1. Gate: only when `lifecycle==EVIDENCE_REVIEWED`, Selection/Architecture
   pending, both Human Gates pending + null provenance, review index empty,
   architecture checkpoint not passed, exact Sol scope decision (changed IDs =
   the 2 HOLD candidates, old accept SHAs, basis SHAs) provided.
2. Guards: fail-closed work-branch HEAD/Tree + reviewed main/Core SHA (no
   force-push/reset), exact base `checkpoint_provenance[evidence]` match, old
   acceptance SHA match, changed-ID allowlist (others byte-identical).
3. Preserve: all §4.1 bytes. Generate: new immutable Evidence/View accepts
   (content-addressed), new Ledger/Completeness, new Matrix/Selection PREVIEW
   (not approval), ONE append-only supersession record old→new + Sol decision.
   New Evidence authority includes archived original hosted articles + preserved
   Discovery/Screening provenance; FIRST resolve Issue #562 req. 4 (INSPECT
   retention vs canonical Screening change — explicit finding, SHA-guarded if
   Screening changes).
4. Rebind: single atomic checkpoint update — `checkpoint_provenance[evidence]`
   (+ derived `materiality`/`completeness` attestations if they are separate
   checkpoint records in this tree) → new attestation `{path,sha256}`;
   `history` UNCHANGED (same-State); `lifecycle_state` stays
   `EVIDENCE_REVIEWED`; `validate_agent_state` must pass; rollback on any
   failure. No Selection advance until Sol approves supersession.
5. Regression: full deterministic revalidation (§4.2) + negative tests (Issue
   #562 req. 6) on Weekly AND another profile (Thematic or Retrospective —
   see §7 for DM016/DM017 interactions); no unrelated edition mutation; no
   post-`VALIDATED_DRAFT` machinery; no new Human Gate.

### Option R (FALLBACK, lossy): edition restart / new issue

Fresh `initialize` (new issue id or archived old tree), re-run intake with
corrected retrieval. Lawful but loses same-State continuity, doubles cost,
orphans r10/r11 history as active authority. Accept ONLY if root rejects S
(e.g., Screening semantics force a full 37/37 regeneration incompatible with
same-State rebind, or Sol finds new retrieval undermines Discovery closure).
Must be labeled restart, not supersession.

### Counterexamples (explicitly NOT proposed)

- C-overwrite / hash-only admission (§3 D2): breaks provenance, forbidden.
- Fake `REQUEST_CHANGES` / fake `APPROVED` / generic pending override (§3 E/F):
  fabricates Human authority, forbidden.
- Post-`VALIDATED_DRAFT` renewal reuse (§3 I): wrong lifecycle/reason class,
  forbidden by default.
- Legacy Weekly revise as Core v2 fix (§3 H): wrong State authority, not a
  precedent.
- Dashboard/logging framework / new Human Gate: NOT proposed (unasked; task
  forbids).

### Capability loss if S is rejected (no supersession at all)

- W40 stays frozen at 29/4/2 with 28-SELECTED ceiling; two issuer-authored
  in-window methods announcements remain HOLD despite verified hosted-article
  events; Plan B 30-SELECTED can never be lawfully selected; edition cannot
  advance to Architecture without either (a) mis-selecting HOLDs (validator
  refusal) or (b) silently dropping material candidates (research inadequacy).
- No same-State path means every future pre-Architecture upstream correction
  (host timestamp fix, retrieval gap, View/materiality error found before
  Selection) forces either edition restart or indefinite HOLD — the exact
  `CORE_REENTRY_CONTRACT_GAP` cost.

## 7. DM016 / DM017 / Profile dependencies (separate from mandatory DM022 scope)

Source-cited, no all-22 batch (intake correction §2, AGENTS.md deferred
boundaries):

- DM016 (`deferred-maintenance-summary.md:474-529`, `OPEN_CORE /
  EDITION_WORKAROUND`, Tracking #515): Evidence source-class map rejects 10
  canonical Thematic source types (`PRIMARY_DOC/REPO/ANNOUNCEMENT/MODEL_CARD/
  SPEC`, `SECONDARY_REFERENCE/TECHNICAL`, `RUNTIME_RECIPE`, `PACKAGING_DOCS`,
  `RUNTIME_PR`). Required future Core: consistent Discovery/Screening/Evidence
  admission + regression proving every accepted Discovery type is
  Evidence-classifiable or rejected before Screening. **Dependency for DM022:**
  NONE for W40 Weekly (`WEEKLY` profile, `WEEKLY_MAGAZINE` publication) — the
  two new articles are `PRIMARY_ANNOUNCEMENT`-like hosted articles entering
  through Weekly Evidence roles, not the 10 Thematic types. MANDATORY for
  integrated-contract validation on a second profile IF that profile is
  Thematic (`THEMATIC + LONGFORM_SPECIAL`): the §6 negative-test second
  profile run must either avoid DM016 types or carry the authorized
  edition-local projection ledger (preserve Discovery/Screening, deterministic
  projection in derived Task copies, per-task mapping, fail closed on
  unmapped, unmodified frozen validators, Supplement for corrected bodies).
  Do not batch-fix DM016 inside DM022; record interaction only.
- DM017 (`deferred-maintenance-summary.md:532-563`, `OPEN_CORE /
  EDITION_WORKAROUND`, Tracking #515): Completeness builder
  (`run_evidence_v2_interactive._build_completeness`) materializes Profile
  initial obligations only; validator additionally requires every Discovery-
  provenance obligation ID. SP-efficient-llm-2026 exposed via `EFF-O13/14/15`.
  **Dependency for DM022:** CONDITIONAL for any profile (incl. W40) — IF the
  supersession's Discovery gap-fill or re-retrieval introduces new obligation
  IDs after initialization, the new Completeness MUST enumerate them
  (edition-local append with mechanical Derivation/binding, unchanged frozen
  schema/validator, cf. DM017 workaround) or the supersession fails its own
  Completeness validation. If no new obligations are introduced, DM017 adds no
  work. Document the finding either way; do not batch-fix the generic builder.
- Profile applicability (separate axis, `config/survey-production-v2.json:
  133-164`, authority §§6–7, session-bootstrap §6):
  `WEEKLY + WEEKLY_MAGAZINE` (W40: `ROLLING_WINDOW`, X/Grok REQUIRED, carry-over
  + `why_this_week`/Watchlist/Late-Breaking semantics);
  `THEMATIC + LONGFORM_SPECIAL` (`OPEN_HISTORY_AS_OF`/`CURRENT_STATE_AS_OF`,
  lineage/branch/transition semantics, X `CHATGPT_DECIDES`);
  `RETROSPECTIVE_PERIOD + LONGFORM_SPECIAL` (`BOUNDED_PERIOD`, chronology/
  synthesis, period-end gate, internal `SP-…` vs public slug identity).
  Manual transport is operational transport only (Grok Drive result relay), not
  a Human Gate and not a regeneration alternative. `DIRECT_PRIMARY`
  (`survey_reader_surface_gate_v2.py:1325-1326`) is a publication-surface
  route (`PRIMARY_ONLY`, reviewed-primary drift check), NOT an upstream
  Evidence resourcing path — it does not supply missing issuer articles.
  Integrated-contract proof needs Weekly (W40 shape) + ONE other profile
  (Thematic preferred for DM016 coverage, or Retrospective for period-closure
  coverage); the choice determines which of DM016/DM017 interactions are
  exercised, but neither DM is thereby closed.

## 8. All-role work comparison (qualitative only, unknown ≠ zero)

Per authority §§5–6 (Sol owns research sufficiency/consumption/materiality/
Selection/Architecture/dossier; Luna/Work owns bounded execution/capture/
normalization/delegation; ChatGPT is operator; deterministic tools own
hashes/schemas/paths/validators; Human owns `APPROVED`/`REQUEST_CHANGES` +
  boundary + requested changes):

- Option S costs: ChatGPT re-retrieval + archive + package/task rebuild +
  Card/View/Ledger/Completeness/Matrix derivation + checkpoint-rebind op +
  negative-matrix execution (×2 profiles); Sol re-review (consumption +
  materiality + completeness + Selection preview + dossier readiness); Human
  unchanged (no new gate, normal Architecture Review later); deterministic
  revalidation compute (per-invocation batching, no global cache — renewal
  closeout §2 precedent). Option R adds full X-intake/Screening/Evidence
  repetition + new-issue provenance + history loss.
- No numeric work-saving, cost, or finish-date claim is made (no measurement;
  moving work is not saving; necessary independent review is not duplication).
  Representative Production semantic quality remains NO-GO; synthetic
  approvals are not genuine (renewal closeout §3 precedent applies unchanged).

## 9. Exact choices for root / findings / unknowns

Choices for root (no implementation until selection):

1. Adopt Option S as the integrated DM022 contract and commission concrete
   interface/schema/digest/closure/accepted-authority predicate map + Sol
   dossier + independent author-side design review; OR
2. Adopt Option R (restart) with explicit continuity-loss acceptance; OR
3. Declare W40 Plan B out of scope (keep 29/4/2 frozen, document HOLD
   retention rationale, accept capability loss in §6).

Findings (design-level, source-read):

- F1: No current public API lawfully supersedes accepted Evidence/Views/
  Materiality at `EVIDENCE_REVIEWED` while staying at same State. Forward
  Selection is lawful but preserves HOLDs; Human/operator gate paths are
  inapplicable (`ARCHITECTURE_ESTABLISHED`/`RELEASE_CANDIDATE` only).
- F2: Active authority is checkpoint-bound (`resolve_active_evidence_views`
  same-checkpoint rule); new immutable accepts alone are inert. Overwrite or
  hash-only admission is fail-closed drift.
- F3: Supplement carries new source bodies without replacing accepts; legacy
  Weekly revise is wrong-State machinery; post-`VALIDATED_DRAFT` renewal/
  revalidation is wrong-lifecycle machinery.
- F4: Downstream blast radius is bounded (§4.3): Matrix + Selection preview +
  selection-architecture-input; Architecture/Draft/publication not yet
  existent; Discovery/Screening stay unless req.-4 forces explicit Screening
  change.
- F5: DM016 is Thematic-only interaction (second-profile test concern), DM017
  is conditional (new-obligation concern); neither is batched into DM022.

Unknowns (require root/Sol disposition, not assumed):

- U1: Do accepted `INSPECT` Screening decisions semantically permit new
  Evidence/Views/Materiality promotion for the 2 HOLD DIDs (Issue #562 req. 4),
  or does the precise governance contract require canonical Screening change?
  (Source read confirms Matrix derives from Evidence/Views/Materiality and
  Selection rejects HOLD, but the Screening→Evidence permission edge needs the
  exact `survey_screening_v2`/`survey_evidence_v2` task-binding rule cited in
  the concrete map.)
- U2: Exact archived-byte retrieval provenance for the 2 hosted articles
  (bytes not in r11 commit) — re-consumption proof shape, timestamp parser,
  source-role assignment.
- U3: Second-profile choice for integrated proof (Thematic vs Retrospective)
  and consequent DM016/DM017 exercise scope.
- U4: Supersession record schema name/location + checkpoint-rebind function
  signature + history-preservation proof (concrete map must show
  `history.length == LIFECYCLE.index(EVIDENCE_REVIEWED)+1` unchanged and
  `validate_agent_state` clean).

## 10. Source API index (final93 proof-copy unless noted)

- Lifecycle/config: `scripts/survey_production_v2.py:75-87 LIFECYCLE`,
  `89-102 CHECKPOINTS`, `550-576 derive_control_fields/refresh_state_control`,
  `998-1048 transition_state`, `1051-1071 initialize`;
  `config/survey-production-v2.json:203-264 orchestration/gate_at_state/
  gate_inputs/revision_boundaries/operator_pending_gate_invalidation_boundaries/
  canonical_regeneration_artifacts/stage_plan`, `276-396 stage_plan`.
- Gates: `scripts/survey_human_gate_v2.py:440-485 _current_pending_gate`,
  `681+ record_architecture_approval`, `902-921 _superseded_paths_for_regeneration`,
  `924-941 _superseded_gate_authority_paths`, `944-999 _revised_state`,
  `1002-1048 _validate_pending_gate_surface`, `1179-1347 invalidate_pending_gate`,
  `1350-1425 request_changes`, `1428-1481 revision wrappers`.
- Agent/controller: `scripts/survey_agent_control_v2.py:597-748
  validate_agent_state/_validate_agent_state`, `902-938
  resolve_active_evidence_views`, `1768-1826 advance_with_checkpoint`,
  `1829-1944 approve_architecture/approve_publication_preview`;
  `scripts/survey_agent_tool_v2.py:42-180 stage-basis override + allowlisted
  helpers`; `scripts/survey_orchestrator_v2.py:977-1001 advance_to_gate`.
- Evidence/Views/Ledger/Completeness/Selection/Architecture:
  `scripts/survey_evidence_v2.py:1159-1213 accept_evidence_results`,
  `1498-1552 accept_edition_views`, `1579-1655 build_materiality_ledger`,
  `188-360 supplement`; `scripts/survey_screening_v2.py:919-979 accept_results`;
  `scripts/survey_handlers_v2.py:204-309 evidence/selection/architecture
  validators`; `scripts/run_selection_architecture_v2_interactive.py:158-201
  run` (EVIDENCE_REVIEWED + no-overwrite);
  `scripts/candidate_selection_gate.py:169-176 HOLD rule (legacy statement)`;
  `scripts/survey_architecture_v2_base.py:396 refuse-overwrite`.
- Renewal/revalidation (counter-precedents):
  `scripts/survey_versioned_renewal_v2.py:560-590 entry window,
  619+ entry observation` (VALIDATED_DRAFT only);
  `scripts/survey_agent_control_v2.py:2323+ revalidate_publication_surface`
  (authority §8 ¶270: VALIDATED_DRAFT, publication-surface roles only).
- Legacy (counter-precedent): `scripts/revise_weekly_interactive_evidence.py`
  (legacy `pipeline-state.json`, not Core v2); `scripts/accept_evidence_results.py`
  (legacy `CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED` coarse gate);
  `scripts/apply_special_selection_and_propose_architecture.py:197-198`
  (legacy EVIDENCE_REVIEWED gate).
- Authority/governance: `docs/survey-production-core-v2-authority.md`
  (esp. §§5–8, ¶270 revalidation), `docs/survey-production-core-v2-session-bootstrap.md:146-211`
  (pending-gate invalidation vs REQUEST_CHANGES, Architecture APPROVED/REQUEST_CHANGES),
  `docs/survey-production-core-v2-execution-record-policy.md`,
  `docs/survey-production-core-v2-operator-execution-bridge.md`,
  `docs/survey-production-core-v2-sol-luna-review-governance.md`;
  `AGENTS.md` (proof-copy session bootstrap + Human boundaries).
- DM022 capture: intake `README.md`, `intake-and-impact.md` (+ correction),
  `dm022-source.json`, `issue562-api.json` body, `deferred-maintenance-summary.md:738-786`
  (DM022 entry), `:474-563` (DM016/DM017), `:740-760` gap statement.
- Prior delivery bounds: `outputs/rephase-1-versioned-renewal-implementation-assessment.md:§5`,
  `notes/rephase-1-versioned-renewal-implementation/astra-closeout-resolution.md:§§1,6-7`.

---

*End of AUTHOR-side DESIGN-only analysis. No code/tests/build/fixtures/source/
runtime/Git writes performed. Awaiting root selection review; no independent
PASS/adoption claimed. Whole NOT_READY / step4B3 OPEN / audit unstarted /
DM021+022 OPEN preserved. Stop at Human Commit Point.*
