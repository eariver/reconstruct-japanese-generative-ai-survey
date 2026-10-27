# DM022 pre-Architecture contract — independent authority design review

2026-10-26. **Fresh independent design reviewer, not author. READ-ONLY source/code/capture inspection only.**

Method: `Read`/`Grep`/`Glob` on decision, packet, capture and final93 proof-copy only.
No runtime/import/tests/build/fixtures/Git mutation/network/Production refresh/restore.
No source edits, no candidate/reconstruct Commit/Push.

## 0. Inputs and authority

Reviewed:

- `outputs/rephase-1-dm022-prearchitecture-contract-decision.md` (§§1–10).
- Mandatory packet `notes/rephase-1-dm022-prearchitecture-contract/astra-review-resolution.md` (R1–R7, §3).
- Packet `README.md`, `source-and-carryover-observation.md/.json`.
- Existing narrow DM022 capture `notes/rephase-1-roadmap-replan-20261019/dm022-intake/`
  including `evidence-20261018T162917Z/intake-and-impact.md` §§1–201 **including
  Astra correction §§168–201**, `issue562-api.json`, `dm022-source.json`.
- Author Task-A `accepted-authority-source-analysis.md` and Task-B
  `operator-alternatives-analysis.md` plus their corrections
  `accepted-authority-source-correction.md` / `operator-alternatives-correction.md`.

Author A/B initial + corrections are **REJECTED where Root overrides**.
This review tests the **Root-selected contract** (decision + R1–R7), not author
“constructible/selected” prose. No precode/runtime approval, no adoption,
no Production semantic READY.

Source pinned (read-only observation, not recertified here):

- Proof-copy `.rephase-1-editorial-runtime/versioned-renewal-packaging-final-depth-20261025T205432Z/proof-copy/candidate-partial-b40de60`
  = actual `409b292` / tree `8ce36998` + 93 paths 40M53A / 742 files.
  Patch `f898d33b…` / manifest `d488c6ee…` pins match AGENTS.md as observed in
  carryover note §8; 5/5 spot file hashes match; full-93/742 recertification
  **not** performed this unit (see §10 carryover).
- Capture pins: Summary commit `c8d0ecc1…`, blob `0a0fe3eb…`,
  Issue562 open/0-comments/2026-10-10T09:37:43Z. W40 technical facts
  (29/4/2, Plan B substance, r11 HEAD, HTML bytes) remain **unreproduced
  secondary evidence** per intake correction; this review treats them as
  reported intake, not code facts.

## 1. Verdict

**DESIGN_BOUNDED_PASS ONLY, with mandatory precode gate OPEN.**

The selected bounded same-State upstream acceptance revision is source-grounded
and internally coherent at contract-selection level: exact `EVIDENCE_REVIEWED`
window, one truthful typed supersession record with separate producer boundary,
same-record e/m/c triplet swap with no extra LIVE pointer, four-artifact
completeness, forward history unchanged with lineage outside history, immutable
old bytes vs new typed acceptance, guard switch-then-clear with strict
unknown-not-rollback resume, no fake Sol/Human Gate, no hash-only/raw rebind/
pending-flag permission, bounded Weekly/Thematic witnesses with DM016/017 left
open.

This is **not** constructible-runtime proof, not implementation acceptance,
not adoption. Concrete module/import/closure/API/CLI/schema/digest/guard/
write-set map per decision §10 remains mandatory; Astra + author-independent
readiness reviewer must confirm it before code. Blocking precode-closure
findings B1–B4 below must be closed in that gate; they do not require a new
contract selection. If precode cannot prove the stated completeness conditions,
return to §9 A1-vs-A2 comparison before code rather than implement a partially
guarded A1.

Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN;
Profile/quality/fixed-candidate/adoption/savings remain open.

## 2. Applicability — defect exists, no lawful path on final93

Confirmed source-grounded:

- `survey_production_v2.py:75-87 LIFECYCLE`, `:89-102 CHECKPOINTS`,
  `config/survey-production-v2.json:218-225 gate_at_state`
  (only `ARCHITECTURE_ESTABLISHED→ARCHITECTURE_REVIEW`,
  `RELEASE_CANDIDATE→PUBLICATION_PREVIEW`), `:256-265`
  operator boundaries, `:266-275 canonical_regeneration_artifacts`,
  `:276-315 stage_plan` (`CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED`
  checkpoints `[evidence,materiality,completeness]`;
  `EVIDENCE_REVIEWED→SELECTION_COMPLETE` checkpoints `[selection]`).
- `survey_production_v2.py:998-1048 transition_state:1014-1015`
  refuses same/backward (`exactly one forward step`); `:1020-1030` requires
  exact passed/provenance updates with canonical attestation revalidation.
- `survey_human_gate_v2.py:440-485 _current_pending_gate` requires mapping hit +
  pending + null provenance + `HUMAN_GATE_REACHED`; at `EVIDENCE_REVIEWED` no
  mapping entry → `has no configured pending Human Gate` (`:463-465`).
  `invalidate_pending_gate:1179-1348` additionally requires passed
  `architecture` checkpoint for `ARCHITECTURE_REVIEW` (`:1208-1209`), zero
  review-index rows, HEAD/branch/surface guards. Unreachable at bare
  `EVIDENCE_REVIEWED` though `EVIDENCE_REVIEWED` appears in the allowed-boundary
  vocabulary — vocabulary, not gate-presence grant. Root R1 correctly scoped.
- `survey_versioned_renewal_v2.py:560-590 _require_renewal_entry_window`
  requires `VALIDATED_DRAFT` + approved Architecture + pending Preview +
  pending downstream + inactive Exception. Ineligible six lifecycle steps early.
  `survey_agent_control_v2.py:2323+ revalidate_publication_surface` is
  `VALIDATED_DRAFT` publication-surface only. No post-VALIDATED reuse by
  default — decision §2/§9 correctly rejects conflation with
  `REVIEWED_VERSIONED_CORE_RENEWAL`.
- Legacy `revise_weekly_interactive_evidence.py:40-57/85-219` operates
  `sources/<issue>/pipeline-state.json` with state-bytes restore, not Core-v2
  `production-state.json` provenance/history. Category error to cite as Core-v2
  precedent — decision §2 correctly excludes it.
- Forward Selection with old HOLDs is lawful but non-fixing:
  `run_selection_architecture_v2_interactive.py:167-168` requires
  `EVIDENCE_REVIEWED`; `survey_architecture_v2_base.py:526-527` refuses
  HOLD→SELECTED; handlers `_evidence_basis/_selection_basis`
  (`survey_handlers_v2.py:204-280`) re-derive from checkpoint-bound bytes.
  New immutable accepts alone are inert without checkpoint re-pin.

Decision §1 correctly states this as source-grounded applicability, **not** a
local W40 reproduction, with original HTML / full decision corpus not acquired
and 29/4/2 vs 31/2/2 not accepted authority here.

## 3. State-checkpoint semantics

### 3.1 Agent Stage Checkpoint vs Core attestation — correctly distinguished

- Agent: `survey_agent_control_v2.py:481-594 _validate_checkpoint_record`
  validates `{path,sha256}` shape, live SHA, schema
  (`stage-checkpoint-v2.schema.json`), producer `from/to`
  (`_producer_for_checkpoint:348-352`), issue/membership, artifact/review drift,
  plus `_validate_core_stage_report:365-443`. It does **not** require a
  canonical checkpoint pathname; canonical-path enforcement lives only in
  `advance_with_checkpoint:1768-1826:1772-1773` and
  `_validate_stage_artifacts:1622-1655`. Root R2 correctly bars inferring
  agent-path restrictions from `core.validate_state_semantics` /
  `verify_state_basis`.
- Core: `survey_production_v2.py:718-890 validate_state_semantics`
  (`:722-733` exact checkpoint/provenance sets, `:734-758` passed/pending
  attestation rules, `:760-780` fixed forward history shape, `:782-795` Human
  gate provenance) and `survey_production_v2.py:959-996 verify_state_basis`
  (global current-contract + implementation + legacy + semantics). Distinct from
  agent `validate_agent_state:597-748` + `verify_agent_state_basis:941-944`
  (resumable State without globally pinning edition tool commit; per-checkpoint
  implementation/contract via Stage Checkpoint records).
- Decision §2 + R2 correctly select the agent-first surface as the DM022
  authority path; `production.verify_state_basis` is a different globally
  current-pinned API, not a substitute. No design reliance on a missing enum
  alone; gap is lawful producer/adoption semantics + coordinated consumers.

### 3.2 One strict supersession record, truthful same-State operation

Selected `kind=PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`,
reason `REVIEWED_ACCEPTED_UPSTREAM_CORRECTION` (decision §5) with:

- actual operation `EVIDENCE_REVIEWED→EVIDENCE_REVIEWED`;
- separately named producer boundary `CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED`
  (artifact family re-attested, not fabricated execution).

Source necessity confirmed:

- `_producer_for_checkpoint` derives all of evidence/materiality/completeness
  from `CANDIDATES_NORMALIZED` stage; `advance_with_checkpoint:1778-1781`
  requires `record.from==current` and `record.to==stage.next_state` and exact
  checkpoint-set match; `_validate_core_stage_report:400-408` requires
  `report.from==lifecycle` and `report.to==next_state`; schema
  `stage-checkpoint-v2.schema.json:200-208 evidenceArtifacts` requires all four
  named artifacts only when `from_state==CANDIDATES_NORMALIZED`, while
  `:209-215 selectionArtifacts` keys on `EVIDENCE_REVIEWED`. A same-State
  `EVIDENCE→EVIDENCE` record therefore has no producer/schema branch today —
  required new strict branch + same-State report path, exactly as decision §5
  mandates (“do not forge old `CORE_STAGE_CONTRACT` lifecycle fields”).
  Exact field names/schema/digest expressions legitimately deferred to precode;
  kind/reason/operation-vs-producer distinction is the design invariant and is
  present. Author correction’s alternate kind strings (`EVIDENCE_SUPERSESSION_V1`)
  are superseded by the selected kind.

### 3.3 Triplet same-record atomic update, no extra LIVE pointer

- Config `CANDIDATES_NORMALIZED.checkpoints=[evidence,materiality,completeness]`;
  `advance_with_checkpoint:1810-1812` writes the **same** authority to every
  checkpoint in the stage; `resolve_active_evidence_views:914-923` requires
  `evidence.checkpoint_authority==views.checkpoint_authority` plus View→Evidence
  SHA binding (`:928-932`); `_resolve_checkpoint_artifact:839-847` enforces
  exactly-one-artifact per name with live SHA re-hash (`:854-860`).
- Decision §5 sole active update — guarded co-replacement of
  `checkpoint_provenance.{evidence,materiality,completeness}` to the **same**
  new record ref, lifecycle/passed/history/Profile/gates unchanged — matches
  this granularity. Guard is transient coordination checked at entry/before
  publishing, not active authority (decision §6, R5). No second live selector
  introduced. Coherent; exact guard file/schema/write-set legitimately precode
  (see §8).

### 3.4 Four artifacts complete

Schema `evidenceArtifacts` requires `evidence-acceptance`,
`edition-views-acceptance`, `materiality-ledger`, `profile-completeness`.
Decision §5 requires exactly roles Evidence/Materiality/Completeness with all
four named refs + before-State/COPY, Profile, predecessor/anchor,
`supersedes`/revision lineage, request/affected-ID, retention-plan, proof,
decision, tool/contract/work-ref, executor/time, self-digest. Old canonical
checkpoint bytes KEEP historically; new records truthfully declare same-State
correction, never fake old-stage report. Coherent; exact schema branch
precode.

### 3.5 Forward history unchanged, lineage outside history

`validate_state_semantics:760-780` and `validate_agent_state:678-700` both
require `len(history)==index+1` with fixed `from/to` path and monotonic
`recorded_at`. Decision §5 keeps lifecycle/passed/history/Profile/gates
unchanged; same-state row **not** appended to forward history; append-only
supersession lineage lives in records. Correct — history stays the
forward-transition transcript. Exact lineage placement/fields precode.

## 4. Preserve / produce / review / validate

- **Before graph + retained inputs:** decision §4 reloads canonical
  State→passed checkpoint→typed artifact graph (package/task/card/result/View,
  Discovery/Screening/X/raw/supplement, Ledger/Completeness, criteria/prompt/
  schema bindings); keeps content-addressed accepts + original checkpoint bytes;
  copies mutable before-State + every present targeted unaccepted canonical
  output to owned retention root with present/absent inventory; old reviewed
  targets not rebound by equal-byte copy. Matches append-only accept dirs
  (`survey_evidence_v2.py:1159-1213`, `:1498-1552`, `:1797-1801` refuse
  overwrite) and exclusive `mkdir+copy2`. Exact retention-root path/manifest
  schema precode (see B-findings).
- **Candidate graph:** new immutable namespace
  `R=<source_root>/research/v2/acceptance-revisions/<revision_id>`
  (safe single segment, Profile-derived root, no latest-scan selection);
  truthful new package/task/result inputs bound to pre-revision State +
  existing Discovery/Screening; no fake `CANDIDATES_NORMALIZED` execution.
  New Evidence/View accepts content-addressed under R; unchanged complete runs
  reused only at exact validated immutable refs; changed cards/Views always new
  complete acceptance, not partial overlay; Ledger/Completeness newly generated
  versioned files under R; old canonical Ledger/Completeness byte-identical
  until State adoption; no canonical overwrite/rebind-by-hash. Coherent with
  accept exclusivity; versioned-vs-canonical reader cutover is precode-closure
  (B2/B4).
- **Review:** externally supplied author-independent research/authority-
  consumption decision binding before/after graphs, affected IDs, Raw, claimed
  interpretation; existing reasoning responsibility, not new Human Gate or new
  “Sol” role; historical Sol r11/Plan B not this acceptance; no genuine PASS
  generated inside writer. Matches R6/C4 and intake correction (captured Sol
  secondary, current General/Astra chain performs ingress). No fake
  Sol/HumanGate.
- **Deterministic proof leaf:** bound to proposed bytes before adoption; must
  **not** call current State acceptance recursively; LIVE eligibility by high
  op separately; pure final93 content validators reusable/extractable;
  `verify_renewal_source_proof` and publication history/reasons **not** DM022
  admission APIs; full fresh checks replace no semantic reasoning. Correctly
  preserves renewal closeout discipline (History/source NEVER call current
  State validation). Complete proposed-graph revalidation list (package/task/
  result sets+digests, card source/entity/claim/time/access, Views coverage+
  binding, Ledger coverage/dispositions/rationales, Completeness obligations+
  closure, unchanged Discovery/Screening/X/raw/Profile, affected allowlist +
  all unaffected semantic content) with mechanical SHA-propagation explicitly
  mapped precode (not directory-prefix excluded). Design invariant present;
  exact predicate/closure map precode.
- **INSPECT:** decision §4 preserves INSPECT only where validators allow
  (non-DROP, valid task association + evidence status); no KEEP/MATERIAL
  promotion by label; no automatic HOLD→MATERIAL/SELECTED. Source-grounded:
  `build_evidence_tasks.py:19 PROMOTED={KEEP,MAYBE,INSPECT}`;
  `survey_evidence_v2.py:1602-1635` disposition = View materiality irrespective
  of KEEP/MAYBE/INSPECT; `validate_edition_view:1437-1491`
  (`REJECTED→NON_MATERIAL:1456`, `NEEDS_MORE→HOLD:1458`,
  `VERIFIED/PARTIAL` may be MATERIAL). Retaining INSPECT while promoting
  HOLD→MATERIAL structurally permitted iff new Evidence `VERIFIED/PARTIAL`
  with re-consumption proof. Exact task-binding rule citation precode, but
  invariant correctly stated.
- **New Raw/clock/affected-DID/unaffected comparison:** decision §4 binds
  old/new full content+reason per affected ID, newly retained Raw with
  source/event/clock semantics; new official article requires preserved
  bytes/provenance, not Summary quotation; revalidates time/access constraints
  and unaffected propositions/status/rationale/content. Coherent.
- **Missing old article HTML:** decision §1 + R6 explicitly state original HTML
  + full decision corpus not acquired here; 29/4/2 vs 31/2/2 not new authority;
  publication time ≠ model/code/dataset availability or reproducibility. Not
  proven proof — correctly bounded. Precode witnesses must archive original
  bytes + retrieval provenance (URL/fetched_at/SHA/bytes) with
  `datePublished` event-meaning preserved (hosted-article event vs artifact/
  product availability vs reproducibility, AstaBrief-predates +
  AutoSynthData-no-standalone caveats).

## 5. Downstream / Architecture / Draft / publication selectors + guard order

- **A1 selected vs A2 rejected:** A1 retain/clear exact unaccepted canonical
  slots then normal regeneration at canonical paths; A2 version every
  downstream role (rejected: resolver fork through Gate/Draft/publication,
  unbounded audit, semantic failure modes). Decision §6 + R4 + correction
  C3 reasoning (single-canonical-path invariants:
  `_resolve_checkpoint_artifact` exact-one rule, same-authority rule,
  `_reviewed_artifacts`/Gate canonical paths, writer no-overwrite guards
  `survey_architecture_v2_base.py:396,1176`,
  `run_selection_architecture_v2_interactive.py:199-201`) is source-grounded.
  If concrete guard/consumer map cannot preserve invariants, return to
  comparison before code — correct fallback.
- **Six-slot inventory — BLOCKING erratum B1:** decision §6 + correction C1
  claim “six outputs” (`candidate-matrix/selection`, `architecture`,
  `review-summary/attention`, `selection-architecture-input`). Actual runner
  `run_selection_architecture_v2_interactive.py:193-201` guards those six,
  but `:328-343` additionally writes
  `orchestration/v2/interactive/selection-architecture-audit.json`
  (unguarded `core.write_json`, contains input/output SHAs + runner) without
  inventory. Stale audit beside a supersession would mislead review like slot 6.
  Decision’s “exact paths/conditional outputs must be enumerated before code”
  already anticipates conditionals, but the fixed “six” count is factually
  short. **Minimal repair:** amend inventory to include the audit file under
  the same retain + provenance-check + pinned-clear rule (or explicitly scope
  it as retained provenance with manifest retention and justify non-canonical
  status); precode must enumerate all seven + any Profile/config/conditional
  outputs. No fake `sources/<issue>` path, broad glob, or notes/review deletion
  — retained as stated.
- **Ledger/Completeness/Matrix/Selection direct readers — BLOCKING precode
  closure B2:** today `run_selection_architecture:176-177` reads canonical
  `materiality-ledger/profile-completeness`; `run_drafting_synthesis:65-89`
  mixes checkpoint Evidence/Views (`:67-69`) with canonical
  ledger/completeness/matrix/selection (`:86-89`) and only checks matrix↔Evidence
  binding (`:70-73`); `survey_drafting_v2.py:130`,
  `run_evidence_v2_interactive.py:715-732` (canonical Ledger/Completeness with
  refuse-overwrite) likewise assume canonical paths. Decision §5 correctly
  requires new active Ledger/Completeness resolution via State-bound checkpoint
  and “each affected caller must resolve new refs or explicitly refuse,” with
  §10 tracing every post-acceptance consumer Selection→Architecture→Draft/
  Reader. Exact function inventory legitimately precode, **but** precode must
  prove closure: list every canonical ledger/completeness/matrix/selection
  reader (including Draft/Synthesis/Reader/publication proposal/retention,
  stage validators, operator/handoff/Gate preparation, checkpoint/history
  inspection) and show each either resolves via new provenance or refuses
  superseded mode; no canonical-filename fallback after adoption; no fake
  canonical old stage Report. Failure to close blocks code.
- **No fake canonical old stage Report:** decision §5 requires strict new
  checkpoint-schema branch + truthful supersession proof/report; forbids
  forging old `CORE_STAGE_CONTRACT` fields to trick unchanged validators.
  Matches `_validate_core_stage_report:400-408,441` + `_validate_stage_artifacts`
  canonical-path checks. Coherent.
- **Guard + order R5 switch-THEN-clear:** selected order
  `pin→generate/review/prove→retain COPYs→claim+revalidate guard→complete
  record→prevalidate expected State→triplet switch→checked clearing→postread→
  release guard→regeneration` (decision §6, R5) supersedes correction C6
  clear-then-swap. “Missing outputs do not block generator; they enable it”
  correctly rejects Worker “clear while State-old, consumers block” joint with
  `run_selection:199-201` no-overwrite semantics. Post-swap-with-stale-files
  posture remains blocked by guard + independent source-derivation/role
  validation; post-clear/pre-swap and post-swap/pre-regen both must refuse
  stale reuse. Completeness condition present: “code cannot begin if an
  unguarded normal writer can regenerate stale outputs in this window.”
  Exact guard path/schema/checked-caller list precode (see §8). Read-only
  State/history diagnosis remains permitted without proceeding while
  incomplete — correctly scoped.

## 6. Failure / resume / work-ref — strict unknown, no rollback

Decision §7 table reviewed against correction C6 + `invalidate_pending_gate`
precedent:

- Invalid basis/changed ID-Raw-Profile/failed review/proof/unsupported
  stage-mode → refuse before adoption/cleanup; preserve owned inert prep.
- Incomplete candidate/retention → preserve; no same-byte takeover; new id
  unless explicit validated continuation of an immutable completed phase.
- Complete record + State still before → ordinary adoption refuses same intent;
  explicit resume reloads record/graph/review/COPY/guard and may switch.
- State exactly expected-after + cleanup incomplete → explicit resume verifies
  triplet, removes only remaining exact planned slots; missing cleared slots
  allowed, foreign/replaced bytes preserved+refused.
- State after + cleanup complete → full readback + readonly ALREADY_ACTIVE/
  complete; no new acceptance/approval.
- State neither before nor expected-after, or unreadable ownership →
  INDETERMINATE, preserve records/bytes/guard; **no automatic State
  restoration, deletion or adoption**.
- Write/short-write/fsync/close/replace/postread/guard failure → retain
  primary/secondary errors + old/new/unknown observations; never delete
  referenced/possibly-referenced records.

This supersedes Worker-B “restore State bytes on swap failure” per R5, as
tasked (“strict resume unknown old/new not rollback”). Coherent fail-closed
posture with explicit resume only; no multi-file atomicity / crash-atomicity /
global-CAS / creator-authenticity claimed (decision §7 + C6 disclaimer
preserved). Work HEAD/tree predicate (§7: bind exact HEAD/tree + committed
tool/schema/contract files + live evidence pins; adoption rereads + expected
HEAD/tree check; no future self-containing SHA; artifact-only descendant
admissible only with explained ancestry/changed-path set, unchanged pins,
identical controls/contract; otherwise refuse; no standing main-follow/dirty
allowance; complete path set precode) correctly mirrors renewal CURRENT-proof
discipline without transplanting renewal entry. “Atomic State triplet switch”
must be read as single-record co-update with postread verification, not
storage atomicity — **minimal wording repair B3**: qualify “atomic” this way
in precode; retain no-atomic-rollback disclaimer.

## 7. Profile bounds — Weekly/Thematic witnesses, DM016/017 not closed

- **DM016:** decision §8 states two inconsistent source-class maps + 10 absent
  canonical Thematic types; refuses unsupported types; no alias relabelling;
  Weekly+Thematic witnesses use genuinely supported types and report taxonomy
  non-closure. Source-grounded: `run_evidence_v2_interactive.py:38-45`
  (6-entry map) vs `survey_evidence_v2.py:44-109` (Weekly-extended map) differ;
  neither contains the 10 Thematic types. Correctly bounded; broader taxonomy
  unification separate prerequisite. Precode must name the exact supported
  type allowlist per witness; untested types/profiles stay OPEN_CORE.
- **DM017:** decision §8 states builder omits Discovery-named obligations while
  validator requires them; operation preserves/validates union of
  Profile-initial + existing Discovery-named obligations with provenance, no
  fabricated fulfilment; may consume explicitly provided complete rows with
  unchanged full validator; must not silently call incomplete builder.
  Source-grounded: `_build_completeness:471-507` iterates only
  `profile.initial_obligations`, while
  `survey_completeness_v2.py:213-236` requires every Discovery-named ID
  (`silently dropped named Discovery obligations`, trace-back checks).
  Correct; generic builder alignment remains separate decision.
- **Witness scope:** Weekly + Thematic/Longform via same research revision op;
  no publication rendering inside revision; Retrospective/manual/direct-primary/
  Foundation remain whole-readiness dependencies (Weekly `ROLLING_WINDOW`+X/Grok,
  Thematic `OPEN_HISTORY_AS_OF/CURRENT_STATE_AS_OF`+lineage, Retrospective
  `BOUNDED_PERIOD`, manual Grok relay as transport not Gate, `DIRECT_PRIMARY`
  as surface route `survey_reader_surface_gate_v2.py:1325-1326` not upstream
  resourcing). No all-maintenance batch or unselected Profile changes. No fake
  Sol/HumanGate: ingress is existing General/Astra author-independent review of
  provided bundle (refuse-or-admit, admit ≠ Selection/Architecture/Human
  approval). No hash-only / raw-checkpoint rebind / caller-verified dict /
  pending-flag permission: rejected in §9 (accepted overwrite, hash-only,
  reason-only, fake Human revision, legacy temporary-State, post-VALIDATED
  renewal reuse); §5 “record path or valid proposal is not permission token.”
  Coherent.

## 8. Legitimately deferred precode vs design-invariant-missing

**Legitimately deferred (must appear in §10 gate, code blocked until closed):**

- Exact new module/import/closure/API/CLI/schema/digest/guard/write-set map;
  checkpoint/report branch field names, digest expressions, supersession
  proof/report shape; same-record triplet validation predicate;
  historical/current proof boundaries; full active-research + downstream caller
  list (agent State/checkpoint/build/advance/readback, Evidence/Views +
  Ledger/Completeness resolution, Evidence candidate-production helpers,
  Selection/Matrix/Architecture generators + stage validators, Draft/Synthesis/
  Reader + publication proposal/retention, operator/handoff/Gate prep,
  checkpoint/history inspection); exact unaccepted-slot inventory (now seven
  incl. audit, B1); phase HEAD/tree predicate + complete path set; owned
  IO/resume oracles; Profile-specific acceptance predicates; mechanical
  SHA-propagation mapping for unaffected rows; guard consumer inventory with
  “no unguarded writer” proof; postread/inventory verification oracles.
- Exact supported source-type allowlists per witness; exact Discovery-named
  obligation rows; exact archived-HTML + retrieval-provenance shape;
  timestamp-parser + event-meaning fields.

**Not missing — design invariants already fixed (precode must implement, not
re-decide):**

- Same-State window predicates (§3/C5); one-record same-triplet swap with no
  second pointer; four-artifact completeness; history unchanged + lineage
  outside history; immutable old bytes; content-addressed new accepts with no
  overwrite/rebind-by-hash; proof leaf without State recursion + separate LIVE
  HIGH checks + HEAD/tree/contract bootstrap; INSPECT/RAW/clock/DID/unaffected
  rules; missing-HTML non-proof; A1 vs A2 selection with single-canonical-path
  preservation; switch-then-clear with guard blocking + completeness bar;
  INDETERMINATE/no-rollback resume; existing-review ingress with no new
  Sol/Human Gate; hash-only/raw-rebind/pending-flag prohibitions; DM016/017
  non-closure with fail-closed refusal.

No new caller flags/verified dicts, skipped predicates, path budgets, or
unselected schema migrations allowed in precode.

## 9. Blocking findings (actual fns/lines + minimal repair)

- **B1 — audit-file omission (factual inventory short).**
  `scripts/run_selection_architecture_v2_interactive.py:199-201` guards six
  paths; `:328-343` writes seventh
  `orchestration/v2/interactive/selection-architecture-audit.json` unguarded.
  Decision §6 / correction C1 “six outputs” omits it.
  **Repair:** amend inventory to seven (or explicitly scope audit as retained
  provenance under identical retain/check/clear); precode must enumerate audit
  + all conditional outputs; never leave stale audit beside new supersession.

- **B2 — canonical Ledger/Completeness/Matrix readers need checkpoint cutover
  proof (precode-closure, not re-selection).**
  `run_selection_architecture_v2_interactive.py:176-177,193-198`,
  `run_drafting_synthesis_v2_interactive.py:65-89` (`:67-73` partial binding
  check only), `survey_drafting_v2.py:130`,
  `run_evidence_v2_interactive.py:715-732`,
  `survey_handlers_v2.py:204-314 _evidence_basis/_selection_basis`,
  `survey_stage_validation_v2.py:402-543`, plus Weekly/Longform derivation
  (`survey_weekly_derivation_v2.py:609-610`,
  `survey_longform_derivation_v2.py:1033`,
  `survey_editorial_correction_proposal_v2.py:1469,1508`,
  `run_semantic_publication_v2_interactive_base.py:131`,
  `run_drafting_synthesis_v2_interactive.py:67`).
  **Repair:** precode lists every canonical-file reader and shows each either
  resolves via new `evidence/materiality/completeness` provenance (exact
  `{path,sha256}` + live re-hash, no caller dict) or explicitly refuses
  superseded mode; original canonical files historical, never fallback after
  adoption; no fake old `CORE_STAGE_CONTRACT` report.

- **B3 — “atomic” State-switch wording (clarification).**
  Decision §6 `atomic State triplet switch` alongside “no multi-file atomicity
  or automatic rollback.” **Repair:** read “atomic” as single-State-record
  co-update of the three refs with postread/inventory verification only;
  retain C6/§7 no-crash-atomicity/global-CAS disclaimer; precode defines
  postread oracle. No storage-atomicity claim.

- **B4 — versioned R Ledger/Completeness vs canonical overwrite refusal
  (precode path proof).**
  `survey_evidence_v2.py:1797-1801 write_materiality_ledger` +
  `run_evidence_v2_interactive.py:715-717,730-732` refuse canonical overwrite;
  decision §4 creates versioned Ledger/Completeness under `R`.
  **Repair:** precode defines versioned write paths + checkpoint artifact refs,
  shows canonical files stay byte-identical and inactive via provenance switch
  (not overwrite), with exact present/absent inventory and source refs.

Author “restore State bytes,” “clear-while-State-old blocks,” “evidence-pointer
only,” “three-file blast radius,” “new Sol gate,” numeric double-cost, and
unconditional history/attestation-mutation claims remain **rejected** per
R1–R7/decision; this review does not revive them.

## 10. Known carryover constraint (documented, not rectified)

Per packet observation (this review performed no Git mutation/cleanup):

- HumanHEAD `d9fffb2` (parent `f84fcf5`), `main`/`origin/main` same at
  observation time. 55 bare gitlink entries mode `160000` without `.gitmodules`,
  all added by `d9fffb2`; all 55 recorded SHAs match worktree child HEADs;
  54 children untracked-dirt only, 1 child
  (`failure-resume-verification/.../fork-drift-tool`) with tracked
  `scripts/survey_quality_v2.py` modification + untracked classes;
  `--ignore-submodules=all/dirty` clean, default `diff --raw` shows 1.
  Child `.git` dirs are path-local directories with inert `example.invalid`
  remotes (representatives checked); `alternates`/`commondir` absent (all-55 +
  root + proof-copy sweep); no full inode/hardlink audit — no global
  no-sharing certification. Portable clone carries gitlink SHAs + regular
  files only, not child DB bytes/untracked files/tracked worktree edit.
  Prior “no Git DB in packet” covers only
  `source-packaging/final-depth-20261025T205432Z/`, not PACKROOT proof/gen
  copies or 55 fork children.
- Final93 proof-copy available in place; 5/5 spot hashes + patch/manifest
  SHA/bytes match; full-93/742 + source-isolation **not** recertified here;
  missing26309/bulk31466/runtimeTeX nonbundled + 5 apply whitespace diagnostics
  retained as previously qualified. This carryover does not affect the verified
  final93 code patch but bounds portability/fixture claims. No remediation
  authorized or performed; preexisting dirt preserved.

## 11. Precode gate restatement + stop

General’s §10 return must trace every guard-requiring writer and every
post-acceptance consumer Selection→Architecture→Draft/Reader (now including
audit + canonical-ledger readers per B1/B2), with exact schemas/digests/guard/
write-sets, phase HEAD/tree predicate + complete path set, owned IO/resume
oracles, and Profile-specific predicates. Astra + author-independent readiness
reviewer must confirm; no implementation until then.

**Stop. Root chooses next after this review. Ordinary Commit/Push Human-owned.**
Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN preserved.

---

## FINAL-BINDING addendum (2026-10-27, independent authority reviewer)

**Scope of this addendum only:** bind the corrected decision wording including
§11 and root resolution §4; verify the binding selected contract is coherent
after correction and that remaining precode unknowns are finite/checkable
rather than a residual design contradiction. **Preserves §§0–11 above
unchanged.** No runtime proof, no unconditional code authorization, no
source/code/tests/build/Git writes/network. Read-only `Read` of decision,
root §4, and proof-copy runner plus read-only `sha256sum` of the decision file.

**Bound wording:**

- `outputs/rephase-1-dm022-prearchitecture-contract-decision.md` including §11,
  header **BOUNDED CONTRACT SELECTION / mandatory pre-code gate OPEN /
  implementation blocked**, §11 as binding design-review resolution.
- Read-only SHA256: **`a345bb9524b4dfc5b5f32600d0d708687e2b6131d91a43965c97b6418388f223`**,
  31351 bytes via read-only `sha256sum` in workspace root. Binds this addendum’s
  verdict to that exact wording; any wording change invalidates this binding.
- `notes/rephase-1-dm022-prearchitecture-contract/astra-review-resolution.md`
  including §4 (independent-review disposition, seven-slot confirmation,
  B2/B4 precode-OPEN, no implementation authorization).
- Prior 55 bare-gitlink / nested-dirt carryover (§10 above, packet observation)
  remains unchanged carryover, left intact; it is **not** a new approval gate
  and does not alter the final93 code-patch pins.

**Actual source recheck (audit row + role-input coupling):**

- `run_selection_architecture_v2_interactive.run:158–353` directly re-read:
  `:193–201` no-overwrite preflight covers six paths only
  (matrix/selection/architecture/summary/attention/archive);
  `:328–343` additionally writes
  `orchestration/v2/interactive/selection-architecture-audit.json` via
  unguarded `core.write_json`, binding `interactive_input={archive path,SHA}`,
  `runner`, and five `outputs` refs (matrix/selection/architecture/summary/
  attention) — not itself. `:328–329` `shutil.copy2(input_path, archive_path)`
  couples the caller’s new Selection input file to the generated archive.
  §11.1’s seven-row table (validated Profile `source_root`-relative), retain-
  present/record-absent rule, audit `interactive_input`+`outputs` binding rule,
  partial-run non-fabrication rule, no-generic-cleanup rule, successor
  seven-path preflight/guard rule, and caller-input vs generated-archive
  provenance distinction together **dispose B1 as a design rule**. Exact
  writer/ownership/fault oracles remain precode per §11.1 — finite, checkable.
- `:176–181` combines canonical Ledger/Completeness with State-resolved
  Evidence/Views, confirming the direct-reader surface cited in B2. §11.2 makes
  that surface explicitly mandatory (new four-ref resolver from the same typed
  checkpoint; inputs change via verified graph while A1 output paths stay
  canonical; creation restricted to §3 `EVIDENCE_REVIEWED`, adopted-checkpoint
  readback valid through later forward transitions with original context from
  retained lineage; detached proof State-nonrecursive, eligibility/guard
  high-side; full strict State predicates with precise new-kind branch, not a
  `production.verify_state_basis` substitute; later R1/editorial/renewal walkers
  must recognize the new kind). B2 stays **mandatory precode completeness
  gate** — finite enumeration + resolver/refusal + post-acceptance tests, not a
  residual permission to leave readers unchanged. Design PASS here is not
  evidence those callers are already repaired.
- §11.3 narrows “atomic” to one complete known-byte State file replacement
  with all three refs + full after-readback under single-writer/held-descriptor
  discipline; explicitly not cross-directory/guard/record/slot/durability/crash
  atomicity; failed after-readback with new/unknown does not authorize
  before-bytes restoration (§7 INDETERMINATE preserved). This disposes B3’s
  wording without weakening same-record co-update. Versioned R producer
  paths/real stage context with actual output arguments, filenames, schema
  fields, and current content-validator entrypoints, plus no-overwrite/no-
  accidental-consumption proof and no fabricated `CANDIDATES_NORMALIZED` State,
  stay **precode OPEN** per §11.3 (B4) — finite call/path map, not an open
  authority choice.
- §11.4 + root §4 retain the A1-vs-A2 fallback (return exact blocker and revise
  rather than implement partially guarded A1), confirm no runtime/code/test/
  fixture/acceptance/Production action in this unit, and set the next Human
  continuation to the §10 precode readiness return, not implementation or
  repository cleanup.

**Coherence after correction vs contradiction:**

- Six→seven: resolved by binding seven-slot budget; earlier six-slot author/root
  wording preserved as history only, not the write/clear budget (root §4).
- Clear-then-swap (correction C6) vs switch-then-clear (decision §6/R5): resolved
  by binding switch-then-clear with guard blocking + completeness bar
  (“code cannot begin if an unguarded normal writer can regenerate stale
  outputs”).
- Restore-on-swap-failure (Worker-B/C6) vs no-automatic-restoration (§7/R5):
  resolved by binding INDETERMINATE/no-rollback with explicit resume only.
- “Atomic” vs no-multi-file-atomicity: resolved by §11.3 single-record
  co-update reading.
- Canonical-overwrite vs versioned-R: resolved by versioned-R + provenance
  switch with no overwrite and no canonical-filename fallback after adoption;
  concrete paths pending precode proof, authority choice closed.
- No new contradiction introduced by §11: no second live pointer, no forged
  old-stage report, no history-schema mutation, no new Sol/Human Gate, no
  hash-only/raw-rebind/pending-flag permission, no `CANDIDATES_NORMALIZED`
  runner reuse with fabricated State. Remaining unknowns (§8 above + §11.1–11.3
  enumerations) are finite precode artifacts checkable by the §10 readiness
  reviewer without runtime execution.

**Definitive verdict (selection only):**

**DESIGN_BOUNDED_PASS (contract selection only), mandatory precode gate OPEN,
implementation blocked.** Covers the corrected decision including §11 as bound
by the hash above. Not a runtime/constructibility proof, not implementation
authorization, not adoption, not Production acceptance. Whole NOT_READY /
step4B3 OPEN / audit unstarted / DM021+022 OPEN preserved. Root closeout
follows both final reviews; ordinary Commit/Push remains Human-owned.
