# DM022 pre-Architecture accepted-upstream correction — contract selection

2026-10-26 author-side selection; 2026-10-27 review resolution. **BOUNDED CONTRACT SELECTION / mandatory pre-code gate OPEN / implementation blocked.** Input is final93 applied source and the existing narrow DM022 capture. No Production refresh, reproduction, source edits or tests in this unit. [Packet](../notes/rephase-1-dm022-prearchitecture-contract/README.md) and [mandatory root resolution](../notes/rephase-1-dm022-prearchitecture-contract/astra-review-resolution.md) govern alongside this decision. §11 is the binding design-review resolution; final review confirmations cover this wording.

## 1. Applicability and choice

The reported need is material: accepted Evidence/Edition Views/Materiality can remain obsolete while a healthy issue is at `EVIDENCE_REVIEWED`, before Selection and Architecture acceptance. Final93 contains no public Core-v2 operation that both replaces that active authority at this boundary and resumes ordinary downstream production with preservation/recovery.

This is a source-grounded applicability finding, **not a local reproduction of W40 Selection r11**. The capture at Summary commit `c8d0ecc1c9566a2303ad3b4c42635d4b672650e4`, blob `0a0fe3eb0a8f538a9c8c29455be5cef8f6999d57`, and Issue562 reports two organization-hosted article timestamps and a provisional materiality direction. Original article HTML and the complete edition decision corpus were not independently acquired here. Reported29 MATERIAL/4 HOLD/2 CONTEXT and proposed31/2/2 are not accepted new authority in this workspace. Article publication time does not establish model/code/dataset first availability or reproducibility.

**Select a bounded same-State upstream acceptance revision:** immutable new accepted Evidence/Views plus versioned Ledger/Completeness, a typed superseding checkpoint record, atomic replacement of the existing Evidence/Materiality/Completeness State-ref triplet, and guarded retention/clearing of unaccepted downstream canonical outputs. Keep the ordinary forward lifecycle/history and canonical Selection/Architecture path conventions. The selection covers the whole path back to normal Architecture preparation; a standalone supersession manifest that ordinary consumers ignore is not completion.

This selects architecture and authority rules, not code-ready interfaces. A concrete pre-code map and independent readiness review remain mandatory (§10).

## 2. What currently works, and what does not

| Existing path | Actual applicability |
|---|---|
| `transition_state` / `advance_with_checkpoint` | Forward stage advance; same/backward transition is not a correction permit. Forward Selection still consumes the old accepted graph |
| `accept_evidence_results` / `accept_edition_views` | Can create content-addressed, validated candidate runs, with strict existing-run checks. Their existence does not select them as active State authority |
| `resolve_active_evidence_views` | State→Evidence checkpoint→exact Evidence and Views from the same checkpoint, with View→Evidence binding. No latest-directory fallback |
| `run_evidence_v2_interactive` | Requires `CANDIDATES_NORMALIZED`; canonical Ledger/Completeness overwrite refusal remains. Cannot simply rerun at `EVIDENCE_REVIEWED` |
| `run_selection_architecture_v2_interactive` | Requires `EVIDENCE_REVIEWED`, reads active evidence/views and refuses existing canonical outputs. Existing Matrix/HOLD rules must not be weakened to select an obsolete HOLD row |
| Pending Architecture operator invalidation | A legitimate existing alternative **when a pending Architecture Gate was naturally reached** with its required checkpoint/head/review conditions. Not available at bare `EVIDENCE_REVIEWED`; do not manufacture a Gate merely to use it |
| Human `REQUEST_CHANGES` | Legitimate only with the actual Human Gate decision and allowed boundary. `EVIDENCE_REVIEWED` reentry keeps accepted Evidence; `CANDIDATES_NORMALIZED` is the earlier boundary for its regeneration. Do not fabricate Human feedback |
| Legacy `revise_*_interactive_evidence` | Operates `pipeline-state.json` and legacy accepts, including temporary legacy State replacement. Does not rebind Core-v2 State/Views/Ledger/Completeness |
| New issue / edition restart | Possible distinct operation, but not same-issue continuity. Repeated research/review work and loss of continuity are costs, not assumed numeric multiples or free savings |
| Post-VALIDATED editorial / renewal | Requires approved Architecture and `VALIDATED_DRAFT`; preserves upstream research. Wrong authority/lifecycle for DM022; no automatic reuse |

The agent-first validator is distinct from core attestation/global-current-commit validation. In actual `survey_agent_control_v2._validate_checkpoint_record:481–594`, schema/producer/membership/artifacts/reviews are validated, but that function does **not** universally require a canonical checkpoint pathname. New versioned paths therefore are not intrinsically impossible. The gap is lawful producer/adoption semantics and coordinated consumers, not a missing enum alone. Raw direct State-ref replacement is not selected merely because a handcrafted record could pass a reader.

## 3. Exact initial operating window

Initial support is for agent-first Core-v2 issues at **exactly `EVIDENCE_REVIEWED`**, before any accepted Selection/Architecture or Human Gate presentation/review:

* Strict canonical LIVE State and Profile validation, exact path/hash/issue/profile/initialization provenance; use public agent validation, not a synthetic prior lifecycle or a caller-verified dict.
* Passed Discovery/Screening and Evidence/Materiality/Completeness with valid checkpoint provenance. The latter three refer to the same current producer checkpoint and its four accepted artifacts: Evidence acceptance, Edition Views acceptance, Ledger, Completeness.
* Selection, Architecture, Draft, validation, publication-preview, Freeze and Release checkpoints pending with no accepted downstream provenance. Architecture/Preview gates pending with no Human approval/provenance, no recorded Human review/index entry or presented immutable request to supersede, no active Exception, and null publication revalidation pointer.
* Existing author-side Selection/Architecture drafts/previews may exist; they are not accepted authority and are handled by the exact downstream plan below. Existing execution/reviewer notes are retained; no broad edition-tree cleanup.
* Same issue, Profile bytes/paths, Discovery record universe and accepted Screening decisions. Affected-ID allowlist is nonempty, unique and a subset of already-known non-DROP IDs. New Discovery IDs or changed Screening decisions require an earlier regeneration contract; they are refused by this bounded operation.

A State returned after genuine Human `REQUEST_CHANGES`, a pending/reviewed Architecture Gate, approved Architecture, or any later stage is outside this first window. Existing legitimate Gate revision remains available under its own conditions. Do not silently erase its review history to obtain eligibility.

Initial required operational witnesses are Weekly and Thematic/Longform. They use the same research revision operation; no publication rendering is part of this revision itself. Broader Profile acceptance is separately bounded in §8.

## 4. Preserve, produce, review and validate

### Before graph and retained inputs

Reload the canonical State→passed checkpoint→typed artifact graph, including package/task/card/result/View files, Discovery/Screening/X/raw/supplement provenance, Ledger/Completeness and their criteria/prompt/schema bindings. Keep all existing content-addressed accepts and original checkpoint bytes at their original paths. Copy mutable before-State and every present targeted unaccepted canonical output into a new owned retention root; record exact present/absent inventory and source refs. Old reviewed targets are not rebound by copying equal bytes.

Evidence is not required to exist in a tool-source commit. Record the actual source/tool contract separately, with committed/loaded/live controls and exact work HEAD/tree observations. No current-main refresh or arbitrary schema/contract migration is authorized by this content correction.

### Candidate accepted graph

Use a new immutable namespace `R=<source_root>/research/v2/acceptance-revisions/<revision_id>` (safe single-segment id, exact Profile-derived root, no latest-scan selection). Prepare truthful new package/task/result inputs bound to the actual pre-revision State and existing Discovery/Screening. Same-State production must not pretend the issue temporarily was `CANDIDATES_NORMALIZED`.

New Evidence and View accepts use content-addressed new runs under the owned revision namespace; unchanged complete runs may be reused only at their exact validated immutable refs. Changed cards/Views always produce a newly validated complete acceptance, not a partial overlay interpreted as already accepted. Ledger and Completeness are newly generated versioned files under R. The old canonical Ledger/Completeness remain byte-identical and become inactive only after State adoption; no canonical overwrite/rebind-by-hash.

For every affected ID, bind old/new full content and reason, newly retained Raw and source/event/clock semantics. The new official article must have actual preserved bytes/provenance, not a Summary quotation used as evidence. Preserve Screening `INSPECT` only where current task/card/view/ledger validators actually allow it (non-DROP, valid task association and evidence status); do not promote it to KEEP or MATERIAL by label alone. No automatic HOLD→MATERIAL/SELECTED promotion.

### Review and deterministic proof

An externally supplied, author-independent research/authority-consumption decision binds the exact before/after graphs, affected IDs, Raw evidence and claimed interpretation. It is the existing reasoning responsibility, not a new Human Gate or a new “Sol” role. Historical Sol r11/Plan B is not this new acceptance decision. Do not generate a genuine PASS record inside the writer.

Revalidate the **complete** proposed graph under the current supported contract: package/task/result exact sets and digests; every card's source/entity/claim/time/access constraints; complete Views coverage and Evidence binding; Ledger coverage/dispositions/rationales; Completeness obligations and provenance-derived closure; unchanged Discovery/Screening/X/raw and Profile relations; the affected allowlist and all unaffected semantic content. Mechanical acceptance-directory/file SHA changes may propagate to unaffected rows, but their propositions/status/rationale/content cannot silently change. Every such mechanical projection must be explicitly mapped in pre-code, not excluded by directory prefix.

New deterministic proof is bound to proposed bytes before adoption, and must not call current State acceptance recursively. LIVE eligibility is checked by the high operation separately. Pure final93 content validators may be reused/extracted; `verify_renewal_source_proof` and publication history/reasons are not DM022 admission APIs. Full fresh checks replace no semantic reasoning.

## 5. Typed checkpoint selection; lifecycle history remains truthful

Use **one typed superseding checkpoint record** for the new Evidence/Views/Ledger/Completeness set. Select `kind=PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`, truthful reason class `REVIEWED_ACCEPTED_UPSTREAM_CORRECTION`. It carries:

* actual operation lifecycle `EVIDENCE_REVIEWED→EVIDENCE_REVIEWED`, separately named producer boundary `CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED` (the artifact family being re-attested, not a fabricated executed transition);
* exactly the checkpoint roles Evidence/Materiality/Completeness and all four named artifacts, with full exact refs;
* before-State source/COPY refs, current Profile, exact predecessor checkpoint and original checkpoint anchor, `supersedes`/revision lineage;
* request/affected-ID and retention-plan refs, proposed-graph proof, supplied research decision, current code/contract/work-ref observations, executor/time and self-digest.

The exact field names/schema/digest expressions are pre-code deliverables. A strict new checkpoint-schema branch and a truthful supersession proof/report are required; do not forge the old `CORE_STAGE_CONTRACT` report's lifecycle fields to trick unchanged validators.

The record is complete before adoption. The **sole active selection update** is a known-byte, guarded replacement of canonical State, changing `checkpoint_provenance.evidence`, `.materiality`, `.completeness` together to the **same new record ref**. No second live selector is introduced. Lifecycle, passed flags, original forward `history`, Profile/initialization contract, other checkpoints and Human gates remain unchanged. Append-only supersession lineage lives in the records; a same-state row is not appended to the fixed forward history array.

Agent/checkpoint validation and active resolvers must recognize this kind only within this typed research family, verify lineage and same-record triplet, and refuse split/mixed authority. Ordinary forward advancement remains forward-only. Standalone/history validation proves the record's retained basis; high adoption/resume additionally verifies current canonical State against the recorded before/expected-after bytes. A record path or valid proposal is not a permission token.

Normal consumers must obtain new Ledger/Completeness and Evidence/Views through the active State-bound research checkpoint interface. Original canonical files are historical, not fallback authority after supersession. The following implementation map is mandatory: agent State/checkpoint/build/advance/readback; active Evidence/Views and new active Ledger/Completeness resolution; interactive Evidence candidate-production helpers; Selection/Matrix/Architecture generators and stage validators; downstream Draft/Synthesis/Reader derivation and publication proposal/retention consumers that trace accepted research; operator/handoff/Human Gate preparation; checkpoint/history inspection. Each affected caller must resolve the new refs or explicitly refuse this mode. No unattached helper or evidence-pointer-only update.

## 6. Canonical downstream regeneration and transition safety

Select **A1: retain/clear exact unaccepted canonical output slots**, rather than versioning every downstream Architecture/Draft/Human Gate/publication output in this unit. The current Selection runner produces **seven** outputs: Matrix, Selection, Architecture, review summary, attention, input archive and audit JSON. The original six-file inventory omitted the audit and is corrected by §11.1. Exact Profile/config/producer-derived paths and any actual conditional outputs must be enumerated before code. No fabricated `sources/<issue>` path, broad glob or deletion of arbitrary notes/reviews.

Preparation records which slots are present and copies those exact bytes to retained storage. Before clearing, prove each is unaccepted, not a Human-reviewed/request-bound input, unchanged since capture and in the fixed invalidation plan. Unknown/foreign/changed files refuse; absent entries do not become deletion permissions. Normal regeneration must produce a fresh Matrix/Selection/Architecture package against the new accepted graph, with fresh independent reasoning and the ordinary Architecture Human Gate later.

**Missing output files do not themselves block the normal generator**: they are its usual precondition. Therefore the Worker proposal “clear while State-old, consumers block because files are missing” is rejected. Use a scoped exclusive transition guard, checked by affected operational producers/advance/Gate preparation at entry and before publishing outputs. It is coordination, not a second active-authority pointer. Unknown/unreadable/mismatched guards fail closed. Strict read-only State/history diagnosis remains possible; it must not be confused with permission to proceed while a transition is incomplete.

Selected order:

`pin current basis → generate/review/prove immutable candidate → retain COPYs/inventory → claim and revalidate guard → complete supersession checkpoint → prevalidate exact expected State → atomic State triplet switch → checked clearing of old unaccepted slots → postread/inventory verification → release owned guard → ordinary regeneration`

The writer may validate its internally constructed expected State as a plan, but must still validate actual pinned LIVE State before mutation and actual after bytes afterward. It must not pass synthetic old lifecycle State to content producers or treat a hypothetical State as current authority.

No multi-file atomicity or automatic rollback is claimed. The guarded transition covers pointer adoption and cleanup; an incomplete operation can have new State plus old stale draft files, in which case normal producers remain blocked by the guard. Source derivation and role validation also reject stale inputs independently. All operation consumers requiring coordination must be concretely inventoried; code cannot begin if an unguarded normal writer can regenerate stale outputs in this window.

## 7. Failure / resume / work-ref rules

| Boundary/observation | Required behavior |
|---|---|
| Invalid basis, changed ID/Raw/Profile, failed review/content proof, unsupported stage/mode | Refuse before adoption/cleanup; preserve owned inert preparation if already created |
| Incomplete candidate/retention | Preserve; no same-byte takeover. New attempt uses a new id unless a specific immutable completed phase has an explicit validated continuation |
| Complete record, State still exactly before | Ordinary adoption refuses existing same intent; explicit resume reloads record/graph/review/COPY/guard and may switch |
| State exactly expected after, cleanup incomplete | Explicit resume verifies active triplet and removes only remaining exact old planned slots; missing already-cleared slots allowed, foreign/replaced bytes preserved and refused |
| State after, cleanup complete | Full readback + readonly ALREADY_ACTIVE/complete result; no new acceptance or approval |
| State neither before nor expected after, or unreadable ownership | INDETERMINATE, preserve records/bytes/guard; no automatic State restoration, deletion or adoption |
| Write/short-write/fsync/close/replace/postread or guard failure | Retain primary/secondary errors and actual old/new/unknown observations; never delete referenced or possibly referenced records |

Request/preparation binds exact observed HEAD/tree and committed current tool/schema/contract files, plus full live evidence pins. High finalization/adoption takes an expected work HEAD/tree check and rereads them; no future self-containing commit SHA is required. An artifact-only descendant commit during review is admissible only if its ancestry and exact changed-path set are explained by the declared attempt's input/output/review records, every prior pin remains unchanged and current controls/contract are identical. Otherwise refuse and require a new bounded attempt; no standing main-follow or generic dirty allowance. The pre-code map must supply this predicate and its complete path set.

The capture's atomicity/rollback wishes are requirements to evaluate, not proof existing files can be changed atomically. Retention and explicit resume preserve authority; they do not certify crash atomicity, global CAS or creator authenticity. Review and QA validators check supplied evidence; they do not manufacture genuine assessment.

## 8. Profile dependencies and capability bounds

* **DM016:** final93 has two inconsistent source-class maps, and the10 captured canonical Thematic types are absent. This remains an initial-production/Profile compatibility problem. This bounded correction refuses unsupported source types; no alias relabelling to make a validator pass. Weekly+Thematic witnesses must use genuinely supported source types and explicitly report that this does not close canonical Thematic taxonomy support. Necessary taxonomy unification is a separate selected prerequisite if representative usage needs it.
* **DM017:** the interactive builder omits Discovery-named obligations while the validator requires them. This operation must preserve/validate the union of Profile-initial and existing Discovery-named obligations, with exact provenance and no fabricated fulfilment. It may consume explicitly provided complete obligation results and use the unchanged full validator; it must not silently call the incomplete builder and claim completeness. General builder alignment remains a necessary separate decision for ordinary initial production if that path is required.
* Screening `INSPECT` is not by itself a MATERIAL prohibition: actual Evidence/View/Ledger predicates permit an appropriate non-DROP validated path. Specific evidence status, event/clock, Profile scope and materiality reasoning still must hold. Changed Screening decisions/new Discovery obligations arising from a changed Discovery graph are outside this first same-State correction.
* Retrospective/manual/direct-primary/Foundation use remains a whole-readiness dependency. A research-side revision is not tied to a publication renderer, but these profiles are not declared proven by the two initial witnesses. No all-maintenance batch or unselected Profile changes.

## 9. Alternatives and qualitative cost

Selected A1 removes needless new-issue recreation and preserves old accepted authority while enabling a truthful same-issue revision. Added work is typed checkpoint/report/lineage support, retained storage, guard/resume coordination, affected consumer integration and new independent research review. These costs must be measured in implementation and representative use; unknown is not zero.

Rejected as completion: frozen-HOLD plus noncanonical technical supplements (useful editorial continuity, not changed active acceptance); accepted-file overwrite/re-pin; hash-only or reason-only admission; fake Human revision; legacy temporary-State acceptance; post-VALIDATED renewal reuse. Existing conditional Gate reentry and a genuinely new issue remain legitimate alternatives under their own conditions, not universal same-State solutions.

Fully versioning all downstream output roles (A2) could avoid canonical cleanup but expands Architecture/Human review/Draft/publication resolution and migration significantly. It is not selected here. If A1's concrete guard/consumer map cannot preserve the required invariants, return to this comparison before code rather than implement a partially guarded A1.

## 10. Mandatory pre-code gate, required witness and stop

Before implementation, General must return the exact new module/import/closure/API/CLI/schema/digest/guard/write-set map, actual checkpoint/report branch fields, same-record triplet validation, historical/current proof boundaries, all active research and downstream callers, exact unaccepted-slot inventory, phase HEAD/tree predicate, owned IO/resume oracles and Profile-specific acceptance predicates. Trace every guard-requiring writer and every post-acceptance consumer through Selection→Architecture→Draft/Reader, not just the four artifact builders. Astra and an author-independent readiness reviewer must confirm it. New caller flags/verified dictionaries, skipped predicates, path budgets or unselected schema migrations are not allowed.

Implementation witnesses must include Weekly+Thematic: valid current `EVIDENCE_REVIEWED`; preservation of Discovery/Screening/Profile and old accepts; actual newly captured input proof with correct article-event interpretation; complete new Evidence/Views/Ledger/Completeness acceptance; exact affected/unaffected comparison and externally supplied independent decision; adoption through one same-record triplet; fresh canonical Matrix/Selection/Architecture regeneration; normal stage advances and genuine-type synthetic Architecture Gate flow; repeated correction; strict old/current readback; downstream publication consumers retain correct accepted lineage. Synthetic reviews remain explicitly nongenuine. Test known stale canonical drafts, guard interruption on both sides of State switch, malformed/split refs, wrong stage/prior Human review, unsupported types, stale HEAD/controls/Raw, missing named obligations, metadata-only “promotion,” ownership/close/replace faults and exact explicit resume. Earlier refusals are not proof of later seams.

This unit is design/source inspection only. No new operation, no W40 reproduction or upstream CORE_FIXED, no deployment/Production acceptance. **Stop at Human Commit Point after independent design review and closeout.** Whole NOT_READY / step4B3 OPEN / audit unstarted / DM021+022 OPEN; necessary Profile/quality/fixed-candidate/adoption/savings remain open.

## 11. Binding design-review resolution (2026-10-27)

The [independent authority review](../notes/rephase-1-dm022-prearchitecture-contract/independent-authority-design-review.md) and [independent operation review](../notes/rephase-1-dm022-prearchitecture-contract/independent-operation-design-review.md) cover **contract selection only**, not implementation readiness or a W40 reproduction. Authority B1–B4 receive these dispositions; all concrete pre-code closure remains required by §10.

### 11.1 Exact seven-slot boundary, not deletion of research history

Root directly read `run_selection_architecture_v2_interactive.run:158–353`. Existing no-overwrite preflight covers only six paths (`193–201`); the function additionally writes the audit (`328–343`). The selected invalidation/retention set is the following seven paths, each relative to the **validated Profile `source_root`**:

| Role | Relative slot |
|---|---|
| Matrix | `candidate-matrix-v2.json` |
| Selection | `candidate-selection-v2.json` |
| Architecture | `architecture-v2.json` |
| Architecture summary | `architecture-review-summary-v2.json` |
| Architecture attention | `architecture-review-attention-v2.json` |
| Interactive input archive | `orchestration/v2/interactive/selection-architecture-input.json` |
| Interactive audit | `orchestration/v2/interactive/selection-architecture-audit.json` |

Retain every present old slot and record absent slots. The audit's `interactive_input` and five `outputs` refs must bind the captured old files if it is claimed as a complete old producer result. Partial failed-run outputs are not fabricated into a complete reviewed result; they still require exact retained inventory and no active/Human binding before removal. Arbitrary reviewer notes, raw captures, accepted directories and other execution history remain untouched. No path is cleared merely because its basename resembles one of these slots.

The successor normal runner's no-overwrite/guard preflight must cover **all seven**, including the currently unchecked audit slot; no divergent audit overwrite after adoption. The pre-code map must also distinguish the caller's new Selection input file from this generated archive, preserving both provenance and the independent new reasoning. This resolves B1 as a design rule; exact writer/ownership code and fault oracles remain pre-code deliverables.

### 11.2 Active research resolution throughout the later lifecycle

Direct canonical readers are a required implementation surface, not an unchanged-consumer claim: `run_selection_architecture_v2_interactive:176–181` currently combines canonical Ledger/Completeness with State-resolved Evidence/Views. Drafting and other consumers also contain canonical path assumptions. The new active research resolver must return all four consistent refs from the same selected typed checkpoint, and callers must not re-open old canonical Ledger/Completeness afterward. Selection/Architecture output paths remain canonical under A1; their **inputs** change through the verified State-selected graph.

Creation/adoption is restricted to §3's `EVIDENCE_REVIEWED` window. **Readback of the adopted checkpoint is not restricted to that current lifecycle.** Normal forward transitions to Selection, Architecture, Draft and publication must continue to validate and consume it while its original operation context is verified from retained before-State/lineage. Do not demand live State still equal the revision's before-State or pretend the correction happened at a later stage. Historical/detached proof remains State-nonrecursive; current operational eligibility and guard checks remain high-side. The agent's normal public strict State validator must retain its full existing predicates with a precise new-kind branch, not a current-pinned `production.verify_state_basis` substitute.

Before code, enumerate every direct read/write site, its replacement resolver or explicit mode refusal, and its post-acceptance tests. Also verify that later R1/editorial/renewal accepted-source/retention walkers recognize the new research checkpoint kind. B2 stays a **mandatory pre-code completeness gate**; design PASS is not evidence those callers are already repaired.

### 11.3 Co-update and candidate path contract

“Atomic State triplet switch” means one complete known-byte State file replacement containing all three refs and full after-readback, under the declared single-writer/held-descriptor discipline. It is not a claim of atomicity across the revision directory, guard, checkpoint record, seven canonical slots, filesystem durability or crashes. Failed after-readback with new/unknown State does not authorize restoration of before bytes. Preserve referenced artifacts and guard; explicit resume follows §7. This disposes B3's wording issue without weakening same-record co-update.

Evidence/View accepts are immutable content-addressed runs; Ledger/Completeness live at declared versioned R paths. The pre-code proposal must bind actual producer output arguments, filenames, schema fields and current content-validator entrypoints, and demonstrate that old canonical Ledger/Completeness are neither overwritten nor accidentally consumed. It must not invoke the normal `CANDIDATES_NORMALIZED` interactive runner with a fabricated State. Existing pure helpers or lawful inert-candidate acceptance APIs can be used only with the new operation's actual high-side eligibility and full proposed-graph checks. B4 stays **pre-code OPEN** until that path/call map is concrete.

### 11.4 Gate outcome and remaining work

The selected authority/retention/review/adoption/guard/regeneration design is bounded. Implementation is still blocked on the concrete schema/report/checkpoint/consumer/guard/HEAD-tree/IO map in §10, including B2/B4 and the audit-slot writer obligations. If any required predicate or normal writer cannot be included without weakening it, return the exact blocker and revise A1 versus A2; do not implement a partially guarded operation.

No runtime code, test, fixture, acceptance replacement or Production action has occurred in this unit. The next Human continuation begins with the **pre-code readiness return**, not immediate implementation or repository cleanup. The55 inherited Gitlinks and nested dirt are separately recorded carryover, left intact.
