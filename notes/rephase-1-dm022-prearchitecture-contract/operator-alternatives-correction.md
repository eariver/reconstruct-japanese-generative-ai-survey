# DM022 operator/alternatives CORRECTION (AUTHOR-side, DESIGN-only)

2026-10-26. Root CHANGES_REQUIRED disposition on the initial
`operator-alternatives-analysis.md` (Analysis-B). This file is the ONLY NEW
file: `notes/rephase-1-dm022-prearchitecture-contract/operator-alternatives-correction.md`.
Analysis-B is PRESERVED unchanged; where this correction conflicts, this
correction governs. No runtime/tests/source writes/Git/network. No new source
reads this unit; all citations below reuse the read-only final93 proof-copy
observations already recorded in Analysis-B §§2/10. No implementation
authorization. Root author selection review remains separate. No independent
PASS/adoption.

## C0. What is corrected

- C1: Initial Option-S "evidence pointer only" is WITHDRAWN as underspecified.
  The upstream authority at `EVIDENCE_REVIEWED` is not one pointer. The
  operative unit is the versioned UPSTREAM accepted bundle
  (Screening-basis-bound Evidence acceptance + bound Edition-Views acceptance +
  derived Materiality-Ledger + Completeness) with typed checkpoint lineage
  (`evidence` / `materiality` / `completeness` checkpoint records), swapped as
  a triplet of refs in the SAME existing State record. Lifecycle, per-checkpoint
  pass marks, and actual forward history are unchanged. No second live pointer
  is created. The original canonical checkpoint record bytes are KEPT
  historically. Any new record kind must truthfully declare a same-State
  correction, never a fake old-stage report.
- C2: "No Selection until Sol approves" as phrased in Analysis-B is WITHDRAWN
  as a prescribed new Sol gate. No new Sol role and no new Human Gate is
  proposed. The ingress rule is the EXISTING author-independent
  research/authority-consumption review (current General/Astra governance
  versus captured Sol historically — see C4), with an explicitly provided
  decision binding the before/after graph plus affected IDs, new Raw, and time-
  claim scope. That review is a refuse/approve ingress check on the operator
  bundle, not a genuine-PASS generator and not an automatic approval of W40
  Plan-B.
- C3: "Blast radius 3 files" is WITHDRAWN as ungrounded. Root fixed stage
  universe/ref/role correctness applies: at the same `EVIDENCE_REVIEWED` State
  (Selection checkpoint still pending) the interactive selection/architecture
  writer may ALREADY have produced UNACCEPTED canonical preview assets at
  canonical paths even though no accepted Selection exists. The affected set is
  the exact KNOWN SIX unaccepted canonical output slots (C1 below), not three.
  All affected unaccepted outputs must be preserved (retained copy + manifest)
  and invalidated (guarded clear of exactly the pinned known files) BEFORE
  ordinary regeneration, so the future Human Architecture Review sees ONLY
  current derived inputs. Broad globs, unknown cleanup, and accepted/gate-bound
  removal are forbidden.

## C1. Root-fixed stage universe: the six known unaccepted slots

Observed in final93 proof-copy
`scripts/run_selection_architecture_v2_interactive.py:199-201` (first-time
writer, `EVIDENCE_REVIEWED` entry at `:167-168`, active Evidence/Views
resolution at `:176-191`, no-overwrite guard at `:199-201`, archive copy at
`:328-329`):

Relative to the edition `source_root` (Profile `paths.source_root`):

1. `candidate-matrix-v2.json`
2. `candidate-selection-v2.json`
3. `architecture-v2.json`
4. `architecture-review-summary-v2.json`
5. `architecture-review-attention-v2.json`
6. `orchestration/v2/interactive/selection-architecture-input.json` (archive
   copy of the interactive input)

Role correctness:

- Slots 1–2 are owned by `EVIDENCE_REVIEWED` (`config/survey-production-v2.json:266-271
  canonical_regeneration_artifacts`: matrix + selection owner `EVIDENCE_REVIEWED`;
  selection-architecture-input likewise `EVIDENCE_REVIEWED`). They are the
  Selection-stage outputs the normal writer regenerates at canonical paths.
- Slots 3–5 are owned by `SELECTION_COMPLETE` (same config block). At a pure
  `EVIDENCE_REVIEWED` State they must not exist as accepted authority; but the
  interactive runner writes 1–5 together in one invocation BEFORE any State
  advance (runner never advances State, never records approval). Hence a State
  that never left `EVIDENCE_REVIEWED` may still hold UNACCEPTED bytes in slots
  3–5. They are preview artifacts, not accepted Architecture, not a Human Gate
  surface.
- Slot 6 is the per-run input archive. It is run-scoped provenance, not active
  authority, but a stale archive alongside a new supersession would mislead
  review; it is in the invalidation set for exactly the superseded run.

Consequences applied in C5–C6:

- Existence of any of slots 1–6 does NOT imply an accepted Selection,
  an advanced lifecycle, a passed `selection`/`architecture` checkpoint, or any
  Human review. `machine_checkpoints.selection/architecture` remain `pending`
  with null provenance; `human_gates` remain pending/null; review index empty.
- Before ordinary regeneration after a supersession, ALL SIX slots (whichever
  exist) must be retained then cleared under the A1 rule. Regeneration then
  proceeds through the EXISTING normal writer at the SAME canonical paths.
  The future Human Architecture Review therefore resolves only current derived
  inputs via the normal `_reviewed_artifacts` / `_validate_pending_gate_surface`
  path (`survey_human_gate_v2.py:1002-1048`), never retained copies.

## C2. Concrete A: versioned upstream bundle + triplet ref-swap (SAME record)

Selected shape for root decision (design only, not authorized to build):

- A-input (versioned upstream accepted bundle, all content-addressed,
  append-only, old bytes preserved):
  new Evidence acceptance + new Edition-Views acceptance bound to that exact
  Evidence SHA (`survey_evidence_v2.py:1159-1213`, `:1498-1552`, same-checkpoint
  rule `survey_agent_control_v2.py:902-938`), new Materiality-Ledger derived
  from the new bound pair (`survey_evidence_v2.py:1579-1655`), new Completeness
  bound to the new Ledger/Views/Evidence set
  (`survey_handlers_v2.py:204-238 _evidence_basis`), each with package/task/
  result/view/ledger/completeness SHA lineage back to Screening/Discovery/
  Profile.
- A-mutation (ONE existing State record, no lifecycle motion):
  atomically swap the THREE existing refs — `checkpoint_provenance.evidence`,
  `.materiality`, `.completeness` (each `{path, sha256}` to its canonical
  attestation/checkpoint record) — from old attestation SHAs to new attestation
  SHAs in the SAME `production-state.json` record. `lifecycle_state` stays
  `EVIDENCE_REVIEWED`; per-checkpoint `passed` marks stay `passed`; `history`
  array is byte-identical (length still `LIFECYCLE.index+1`,
  `survey_agent_control_v2.py:678-700`); `next_action`/`terminal_reason`
  re-derived unchanged (`stage:selection`/null). No second live pointer: at any
  instant exactly one triplet is the State-bound active authority; the old
  triplet is inert history, the new triplet is active only after the swap
  commits.
- A-lineage: original canonical checkpoint record bytes KEEP on disk and in the
  supersession manifest (old `{path,sha256}` per checkpoint + old accept SHAs).
  The new checkpoint records are NEW kinds/bytes that truthfully declare a
  same-State correction (new attestation content, new accept SHAs, supersession
  reference, no rewritten `recorded_at` history, no backdated stage report).
  They must NOT mimic an original `CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED`
  stage report (different `from_state`/producer context, different lineage).
- A-scope bound: Discovery/Screening checkpoints stay PASSED on the same
  authority UNLESS the req.-4 finding explicitly requires a canonical Screening
  change (see C7). New Discovery/Screening IDs or decision changes are OUTSIDE
  this narrow operation and need boundary reentry, not the triplet swap.

## C3. Downstream options: A1 (selected) vs A2 (rejected)

- A1 (SELECTED for root decision): archive + guarded clear of the exact KNOWN
  six unaccepted canonical slots, then existing normal selection/architecture
  writer regenerates at canonical paths.
  Procedure: (i) COPY each existing slot byte into an owned retained root
  (outside canonical paths, e.g. edition `execution/…` retained area) with a
  manifest row `{canonical_path, old_sha256, retained_path, retained_sha256}`;
  (ii) VERIFY each slot is not accepted/gate-bound (not named by any
  `checkpoint_provenance`, not named by `human_gate_provenance`, not a Human
  review input of a presented gate — true by entry predicates in C5);
  (iii) REMOVE only the exact pinned known files that were copied and verified;
  no broad glob, no unknown cleanup; changed/foreign files (slot SHA differs
  from the pinned pre-copy SHA at remove time) REFUSE and leave state
  `unknown` for explicit handling; (iv) proceed to the §C6 operator flow.
- A2 (REJECTED): version every downstream output (new versioned paths/roles for
  matrix/selection/architecture/summary/attention/input-archive) plus a new
  role resolver threaded through Human Gate, Draft, and publication consumers.
  Impact: every downstream consumer (`_selection_basis`, `_validate_pending_gate_surface`,
  orchestrator `stage_plan`, publication derivation, renewal source refs) would
  need a version-aware resolver; Human Gate inputs, approval snapshots, and
  publication provenance would fork; audit must cover both old and new role
  shapes. Huge invariant surface for a pre-Architecture correction whose
  downstream authority does not yet exist as accepted state.

A1-vs-A2 reason (source-ground):

- Invariants: A1 preserves the single-canonical-path invariant every consumer
  already enforces (`resolve_checkpoint_artifact` exactly-one-artifact rule,
  `resolve_active_evidence_views` same-authority rule, `_reviewed_artifacts`
  canonical Gate paths, writer no-overwrite guards
  `survey_architecture_v2_base.py:396`, `:1176`,
  `run_selection_architecture_v2_interactive.py:199-201`). A2 breaks it and
  pays the resolver cost everywhere.
- Cost: A1 cost is bounded file-copy + manifest + six-path clear + normal
  regeneration (qualitative only; unknown, never numerically doubled — see C5).
  A2 cost is unbounded across Gate/Draft/publication plus dual-shape audit.
- Failure: A1 failure modes are local and checkable (copy mismatch, slot
  changed mid-flight, accepted-bound slot encountered, State-write failure —
  table C6). A2 failure modes are semantic (wrong role resolved at Gate,
  stale version bound in approval snapshot, publication lineage fork) and
  harder to detect.

## C4. Review ingress rule (existing roles only)

No new Sol role. No new Human Gate. No Sol PASS generator. No automatic W40
Plan-B approval.

- Historically captured Sol (r11 Plan-B provisional direction, host-timestamp
  ledger, counterfactual) is SECONDARY evidence (intake correction: captured
  status/text fidelity only, technical facts unreproduced). It informs but does
  not authorize.
- Currently, the author-independent research/authority-consumption review is
  the General/Astra governance chain (AGENTS.md role contract: Astra/root
  reviewer, General/Explore workers, independent auditor separate from
  candidate authors). That existing chain performs the ingress check.
- Ingress requires an explicitly PROVIDED decision artifact binding:
  before-graph (old Evidence/View/Ledger/Completeness SHAs + old
  `checkpoint_provenance.evidence/materiality/completeness` + old matrix/
  selection preview SHAs where slots exist), after-graph (new bundle SHAs +
  new attestation SHAs), affected IDs (exactly the changed candidate/task IDs —
  the two HOLD DIDs for W40; all other IDs byte-identical), new Raw scope
  (archived original hosted HTML bytes + retrieval provenance + SHA/bytes),
  and time-claim scope (claimed `datePublished` values + event-meaning
  statement: hosted-article publication event, NOT weight/code/dataset
  availability, NOT first product-availability instant; AstaBrief artifact-
  predates and AutoSynthData no-standalone-implementation caveats preserved
  from Issue #562).
- The review verdict is refuse-or-admit the OPERATOR BUNDLE. Admit does not
  constitute Selection approval, Architecture approval, materiality PASS, or
  Human `APPROVED`. The edition still must run normal Selection derivation +
  full Sol dossier + Human Architecture Review before any approval exists.

## C5. Entry predicates (ROOT tentative) and corrected legal alternatives

ROOT-tentative entry (ALL must hold; any failure REFUSES before any copy/clear):

1. `lifecycle_state == EVIDENCE_REVIEWED` exact.
2. `machine_checkpoints`: `evidence/materiality/completeness == passed` with
   healthy same-authority provenance (each `{path,sha256}` resolves to an
   existing canonical attestation record, SHA matches, checkpoint-record
   validation clean); `selection/architecture/draft/validation == pending`
   with null provenance.
3. Downstream gates/provenance: `human_gates.architecture_review == pending`
   AND `human_gates.publication_preview == pending`;
   `human_gate_provenance.* == null`; no Human review index rows, no approval
   snapshots, no presented Gate request (`reviewed_repository_commit_sha`
   absent); `publication_revalidation_provenance == null`.
4. `exception_gate.status == inactive`.
5. Same Profile/source roots (`profile.path` resolves to current Profile,
   `source_root` stable), current contract/implementation identity valid,
   `validate_agent_state` clean, `derive_control_fields ==
   (stage:selection, null)`.
6. Unsupported unless separately selected: a State already returned by Human
   `REQUEST_CHANGES` (prior review scope exists in `gates/reviews/*-rN.json` /
   index). Captured Sol r11 is NOT a Human Gate and does not trigger this
   clause — but a genuine prior Human rN WOULD, and this narrow operation does
   not cover that shape. Do NOT fake a Human `REQUEST_CHANGES` or a forward
   advance merely to manufacture an invalidatable surface for the wrong
   content (`request_changes:1350-1425` requires a real pending gate + real
   `reviewed_by/at/reference` + allowed boundary; fabrication is forbidden).
7. Provided decision artifact present (C4 scope) with exact SHAs.

Corrected legal alternatives (conditional, not universal):

- Gated reentry via EXISTING paths is lawful IF AND ONLY IF the edition
  naturally reaches a pending Gate later (e.g., after advancing with OLD
  authority to `ARCHITECTURE_ESTABLISHED` with a passed architecture checkpoint
  and `HUMAN_GATE_REACHED`, `invalidate_pending_gate` with an allowed boundary
  becomes available; or a real Human `REQUEST_CHANGES` with an allowed
  pre-Architecture boundary rewinds to the chosen boundary). That is a
  conditional future path, not a current `EVIDENCE_REVIEWED` operator. It must
  neither be misread as "no legitimate fallback exists" nor invoked by
  fabricating gate state.
- New edition (`initialize`: `survey_production_v2.py:1051-1071`, refuses when
  profile/state exists so it needs a new issue id or archival) REMAINS an
  available fallback with its own provenance chain. Its cost is QUALITATIVE
  ONLY (new X-intake/Screening/Evidence run, history discontinuity, review
  re-execution; necessary independent review is not duplication). No automatic
  "numerically double" claim is made — unknown stays unknown.

## C6. Bounded operator flow + failure table (A1 shape, design only)

Flow (each step fail-closed, in order; no step invents Human authority):

1. Pin entry predicates (C5) on live bytes; record pins (State SHA, config SHA,
   HEAD/Tree, reviewed-main SHA, base provenance SHAs, slot SHAs where slots
   exist, decision artifact SHA).
2. Generate the new upstream bundle to content-addressed staging (NOT canonical
   paths): new Evidence/View accepts, Ledger, Completeness, Matrix/Selection
   PREVIEW (not approval). Validate every deterministic binding (C4/C7) while
   still unbound.
3. Independent ingress review of the bundle against the provided decision
   (C4). REFUSE stops here with zero mutation.
4. Retain: COPY each existing slot 1–6 byte into the owned retained root +
   manifest row. VERIFY retained SHA equals pre-copy canonical SHA.
5. Guard: confirm no slot is accepted/gate-bound (C3 procedure step ii).
   Any bound slot REFUSES (unknown/unsupported shape, explicit handling).
6. Clear: remove ONLY the copied+verified exact pinned files. Re-verify SHA
   immediately before unlink; on mismatch REFUSE (changed/foreign).
7. Swap: write the SAME State record with the new triplet refs (C2),
   re-derive control fields, run full `validate_agent_state`. On any error
   restore: retained copies stay retained (history), canonical slots stay
   cleared, State bytes restored from the step-1 snapshot — then STOP in an
   explicitly degraded but fully described posture (see transition CHECK below),
   never silently half-active.
8. Regenerate normally: existing selection/architecture writer recreates slots
   1–6 at canonical paths from the NEW active triplet. No manual authoring of
   downstream bytes.

Failure table (bounded; crash-recovery NOT promised — see disclaimer):

| Step | Failure | Detection | Posture / resume |
|---|---|---|---|
| 1 pin | Any predicate false; HEAD moved; SHA drift | Pin comparison vs live bytes | REFUSED_PRE_WRITE; no mutation; safe retry after re-pin |
| 2 generate | Package basis drift; Card/View/Ledger/Completeness/Matrix invalid; timestamp/source-role invalid | Existing validators (`validate_evidence_package_basis`, `validate_evidence_card`, `validate_edition_view`, `validate_materiality_ledger`, `validate_profile_completeness`, `validate_candidate_matrix/selection`) | Inert staging only; discard staging; old active authority untouched; fix inputs, re-generate |
| 3 review | Ingress refuses (graph/ID/Raw/time scope insufficient) | Explicit review verdict | No mutation; bundle stays unbound staging; decision must be repaired |
| 4 retain | Copy SHA mismatch; retained write fails | SHA recheck after copy | REFUSE; canonical untouched; retry copy; unknown on repeated failure |
| 5 guard | Slot is accepted/gate-bound; slot is not one of the six known paths | Provenance membership check; path allowlist | REFUSE / unsupported-shape; no clear; explicit handling |
| 6 clear | Pre-unlink SHA changed (changed/foreign file appeared) | Re-verify before unlink | REFUSE that path; already-cleared paths stay cleared+retained; posture = degraded-transition (below); never glob-retry |
| 7 swap | New triplet validation fails; State write fails | `validate_agent_state` errors; write error | Restore State bytes from step-1 snapshot; canonical slots remain cleared+retained; posture = degraded-transition; explicit resume only |
| 8 regen | Writer fails on new triplet | Writer errors | State references new triplet but canonical slots absent/partial; posture = degraded-transition; explicit resume (re-run writer, never hand-author slots) |

Transition CHECK (both intermediate postures must block stale reuse):

- Post-clear, pre-swap (State still old, slots cleared): State itself may still
  validate (preview slots are not checkpoint provenance), but NORMAL consumers
  that expect canonical preview bytes MUST block/fail-closed on missing slots
  rather than fall back to retained copies or to an absent-matrix default.
  Retained history is readable as history ONLY (manifest path), never resolved
  as active authority (`resolve_checkpoint_artifact` exact-single-artifact rule;
  Gate surface requires canonical paths). Operators must CHECK this blocking
  behavior for the concrete writer/consumer set; if any consumer silently
  treats missing slots as empty-selection or reuses a cached matrix, the flow
  is UNSAFE and stops.
- Post-swap, pre-regen (State new, slots absent/stale-cleared): the OLD Ledger
  (still on disk at its old canonical path only if that path is itself a
  versioned accept dir — it is NOT reactivated) must NOT resolve as active.
  New active role resolution MUST go through the NEW `evidence/materiality/
  completeness` provenance (exact `{path,sha256}`), never through a bare
  canonical filename. Until regeneration completes, Selection derivation MUST
  refuse (missing inputs) rather than reuse any retained old Matrix/Selection.
  Both postures therefore satisfy: no stale Selection reuse in either State.

Global atomicity disclaimer (explicit): steps 4–7 touch multiple files plus one
State record. The flow provides per-step fail-closed refusal and State-byte
restore, but it CANNOT promise full atomic rollback or crash recovery across
the multi-file mutation from the Issue phrase "never force push or reset"
(which constrains Git mechanics, not storage atomicity). A crash between clear
and swap, or between swap and regen, leaves the degraded-transition posture
above; recovery is EXPLICIT resume (re-verify pins, re-check table, continue
from the recorded progress of old/new/unknown), never automatic replay, never
assumed idempotent success.

Whole-stage return / new edition as the alternative to A1: neither is a
CURRENTLY available operator at a pure `EVIDENCE_REVIEWED` State (no backward
transition API, no pending gate to invalidate, `initialize` refuses over an
existing tree). They are FUTURE operation selections (advance-then-invalidate
if a gate is naturally reached; or fresh initialize with a new chain), so they
qualify as conditional fallbacks, not as current universals.

## C7. Profile / DM016 / DM017 / finish-line bounds

- DM016 is TWO inconsistent maps, not one vague gap: (map-1) open Discovery/
  Screening `source_type` vocabulary that accepts the 10 Thematic types, versus
  (map-2) the frozen Evidence runner `SOURCE_CLASS_MAP` that fail-closes with
  `unsupported source_type for Evidence authority` (DM016 entry lines 482–490,
  types `PRIMARY_DOC/REPO/ANNOUNCEMENT/MODEL_CARD/SPEC`,
  `SECONDARY_REFERENCE/TECHNICAL`, `RUNTIME_RECIPE/PACKAGING_DOCS/RUNTIME_PR`).
  No automatic 10-type batch is selected. The initial operation MAY be bounded
  to Weekly + Thematic ONLY with genuinely supported types (Weekly W40 pair +
  Thematic tasks whose source types already validate under the UNCHANGED frozen
  Evidence map/validators) plus complete explicit obligation rows (DM017 below).
  Every unsupported type encountered MUST be rejected fail-closed; alias
  relabelling merely "to get a PASS" is forbidden. The analysis must explicitly
  name the broader representativeness as NOT closed (untested types/profiles
  remain OPEN_CORE) and must carry the full project finish line (all required
  profiles incl. Retrospective/manual/direct-primary applicability — see below)
  rather than silently dropping it.
- DM017 is the Discovery-named obligation builder gap (DM017 entry lines 540–544:
  builder materializes Profile initial obligations only; validator additionally
  requires every Discovery-provenance obligation ID; `EFF-O13/14/15` precedent).
  Material for ANY profile whose supersession introduces post-initialization
  obligation IDs. The new Completeness MUST supply complete explicit rows with
  mechanical Discovery/Evidence bindings through the UNCHANGED frozen schema
  and validator; no builder bypass, no structural-completion invention.
- Source Evidence for the two hosted articles: supplemental HTML is exact Raw
  (byte-preserved original article bytes + retrieval provenance: URL,
  fetched_at, SHA256, byte count), and the time-event meaning is preserved as
  fields, not collapsed: `datePublished` hosted-article event vs. artifact
  availability (`weight/code/dataset` first-downloadable instant) vs. product
  availability vs. reproducibility — with the Issue #562 caveats kept
  (AstaBrief artifact predates the October article; AutoSynthData has no
  verified standalone public implementation). The supplement path
  (`survey_evidence_v2.py:188-360`, authority §8 ¶265) carries corrected/
  additional post-Screening bodies WITHOUT rewriting Discovery provenance or
  accepted Screening history.
- New Discovery/Screening IDs or decision changes (e.g., a HOLD→MATERIAL flip
  that actually requires a Screening disposition change, or a brand-new
  Discovery record) need BOUNDARY reentry (a wider operation than this narrow
  triplet swap) and are NOT selected here. Optional `INSPECT` retention is
  allowed ONLY where the actual task-binding predicates permit it (Issue #562
  req. 4 — FIRST determine from the precise `survey_screening_v2` /
  `survey_evidence_v2` task-binding rules whether the accepted `INSPECT`
  Screening decision covers the new Evidence task; if the contract requires a
  canonical Screening change, document + SHA-guard it explicitly as an
  extended branch, not as silent reuse).
- Finish line (not dropped): Weekly (`WEEKLY + WEEKLY_MAGAZINE`,
  `ROLLING_WINDOW`, X/Grok REQUIRED) is the W40 shape; Thematic
  (`THEMATIC + LONGFORM_SPECIAL`, `OPEN_HISTORY_AS_OF`/`CURRENT_STATE_AS_OF`,
  lineage semantics) is the bounded second profile for the integrated proof;
  Retrospective (`RETROSPECTIVE_PERIOD + LONGFORM_SPECIAL`, `BOUNDED_PERIOD`,
  period-end gate), manual transport (operational Grok relay only, never a
  Gate), and direct-primary publication route (`DIRECT_PRIMARY/PRIMARY_ONLY`,
  `survey_reader_surface_gate_v2.py:1325-1326` — a surface route with
  reviewed-primary drift check, not an upstream resourcing path) keep their
  existing applicability and remain part of the required full-project audit
  matrix. This correction selects the BOUNDED initial operation only; it does
  not close the broader profiles.

## C8. Return: bounded answers

- Operator flow: C6 table (pin → stage-generate → ingress-review → retain →
  guard → clear → swap → regenerate), with transition CHECK and no atomicity
  promise.
- A1 vs A2: A1 selected (single-canonical-path invariants, bounded cost,
  local checkable failures); A2 rejected (versioned-role resolver fork through
  Gate/Draft/publication, unbounded audit, semantic failure modes). Cost in
  both cases is QUALITATIVE ONLY — unknown, never a numeric double/halving
  claim.
- Current legal alternatives at pure `EVIDENCE_REVIEWED`: forward Selection
  with OLD authority (lawful, non-fixing); conditional gated reentry IF a
  pending Gate is naturally reached later (existing `request_changes` /
  `invalidate_pending_gate` with allowed boundaries + real Human/operator
  provenance); fresh edition `initialize` (lawful fallback, new chain, no
  continuity). No same-State supersession, no backward transition, no pending-
  gate invalidation, no Human decision, and no post-`VALIDATED_DRAFT`
  renewal/revalidation is lawful TODAY at this State.
- Review ingress rule: C4 (existing General/Astra author-independent review of
  the provided before/after graph + affected IDs + new Raw + time-claim scope;
  refuse-or-admit the bundle; admit ≠ Selection/Architecture/Human approval).
- Atomic-rollback promise: EXPLICITLY NOT MADE (C6 disclaimer). Issue #562
  "never force push or reset" is a Git-mechanics guard, not a storage-
  atomicity guarantee.
- New Sol gate: EXPLICITLY NOT PRESCRIBED (C4).

---

*End of correction. Analysis-B preserved; this file governs on conflict.
No code/tests/build/fixtures/source/runtime/Git/network performed or
authorized. Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN
preserved. Stop at Human Commit Point.*
