# Operational rehearsal — operation readiness (working author analysis)

2026-11-01. General rehearsal execution owner, bounded READ-ONLY planning.
This is WORKING author analysis, not root approval, not independent review,
not audit/adoption. No execution was performed for this doc.

## 1. Scope and method

Source read-only, no execution:

- Final implemented source: `.rephase-1-editorial-runtime/profile-support-packaging-20261031T202327Z/proof-copy/candidate-partial-b40de60`
- Complete patch `efb505e44c1ccb3c83121db2fbaa9fec05ed900c252184765ca3b50f7b28254e` /5247647B
- Manifest `634d41f9807e8cd60ca3d839245358fa5e5da312f6d1b58ae84c1619481a03dc` /186847B (manifest file governs; prose hash typos elsewhere are DATA errors per ROOT §2, not alternative identities)
- Read as DATA: `outputs/rephase-1-profile-support-implementation-assessment.md` FULL, `notes/rephase-1-profile-support-implementation/astra-closeout-resolution.md` FULL, independent final review FINAL-BINDING+CLOSEOUT, packet README CURRENT, `outputs/rephase-1-scope-reassessment-20261031.md` INCLUDING §8, `brief/00-mission-and-success-criteria.md`
- Targeted caller/predicate reads only in proof-copy `scripts/` + `config/survey-production-v2.json` (paths below). No import/runtime/tests/build/fixtures/network/Git/Commit-readback/Production actions. No subagents. Materials/explicit-target inventory is owned by separate Explore; no target invented here.

## 2. Research Profile vs publication Profile vs generation route (do not conflate)

From `scripts/survey_production_v2.py:349-356`:

- Research Profile: `WEEKLY`, `THEMATIC`, `RETROSPECTIVE_PERIOD`
- Publication Profile: `WEEKLY_MAGAZINE`, `LONGFORM_SPECIAL`
- Legal pairs: `WEEKLY→WEEKLY_MAGAZINE`; `THEMATIC|RETROSPECTIVE_PERIOD→LONGFORM_SPECIAL`. No other pair is valid.

Generation/review route is a third axis, from `scripts/survey_reader_surface_gate_v2.py:1351-1409`, `scripts/survey_weekly_derivation_v2.py:32`, `scripts/survey_longform_generated_v2.py:44-45`:

- `WEEKLY_GENERATED_V2` / `WEEKLY_MAIN_BIB_STYLE`: canonical `publication/v2/reader-surface-input-v2.json` + sibling `validated-source-manifest.json`, exact trio `main.tex/references.bib/jgaisurvey.sty`
- `LONGFORM_GENERATED_V1` / `LONGFORM_MAIN_BIB_STYLE`: same shape for Thematic four-family, route `THEMATIC_FOUR_FAMILY_LINEAGE_V1` (`scripts/survey_longform_derivation_v2.py:109`), receipt re-derives reader object and reloads persisted semantic review independently of outer Gate
- `DIRECT_PRIMARY` / `PRIMARY_ONLY` (`surface_gate:1353-1356`): `reviewed_surface_path == primary[path]` byte-identical, no generated transform
- `EDITORIAL_PUBLICATION_V1` / `EDITORIAL_MAIN_BIB_STYLE` (`surface_gate:1330-1351`): staged trio/manuscript binding path

Research Profile answers "what evidence rules apply"; publication Profile answers "what renderer/contract applies"; generation route answers "what review receipt proves the bytes". A Thematic edition can legally be `THEMATIC/LONGFORM_SPECIAL` research/publication pair but take either `LONGFORM_GENERATED_V1` or `DIRECT_PRIMARY` review route. Do not treat "manual can do it" as covering the generated route, and do not treat a `DIRECT_PRIMARY` pass as complete-reader proof.

## 3. Route table (shortest rehearsal; no invented target)

`{W}` = concrete Weekly issue_id after material inventory. `{S}` = genuinely needed Special (Thematic topic or Retrospective period) after material inventory. Do not substitute fixture IDs.

| Route | Existing capability (normal public API) | Normal correction that actually applies | What can rehearse without Human authority | What needs Human authority / gap |
|---|---|---|---|---|
| Weekly generated `{W}` | `INITIALIZE_WEEKLY` → Screening/Evidence/completeness → Selection → Architecture → Draft synthesis (`run_drafting_synthesis_v2_interactive.py:68-71` requires `ARCHITECTURE_ESTABLISHED` + approved Architecture) → `WEEKLY_GENERATED_V2` receipt → Candidate/staged/Preview/Freeze/Release. X intake required per edition (`AGENTS.md` bridge doc) | P1 editorial correction `prepare_proposal/validate_proposal` (`survey_editorial_correction_proposal_v2.py:548-573`): ONLY `WEEKLY/WEEKLY_MAGAZINE` + `THEMATIC/LONGFORM_SPECIAL`, requires `VALIDATED_DRAFT` + approved Architecture + `publication_preview:pending` + no downstream checkpoints. Versioned renewal (`survey_versioned_renewal_v2.py:11-22` HIGH ops). Accepted-upstream correction via DM022 HIGH/LOW (new-ID repeat, not same-ID). Genuine `REQUEST_CHANGES` re-entry per §4 | Full disposable run to `VALIDATED_DRAFT`: real intake bytes, real Screening/Evidence runs, real completeness/Selection, real authored Architecture + Draft, real reader input + receipt replay, real `main.tex` build + log, real deterministic/semantic/visual QA reads | Presenting `ARCHITECTURE_REVIEW` or exact-byte `PUBLICATION_PREVIEW` (needs Human APPROVED/REQUEST_CHANGES on exact committed bytes + Profile-bound work-branch head). Cannot rehearse approval itself. Missing cutoff/issue window or X `observed_at`/Raw permission → stop, ask (§8) |
| Four-family Thematic generated `{S-thematic}` | `INITIALIZE_THEMATIC` (temporal mode + `as_of` from request `recorded_at`, same `core.thematic_profile()` path; no SP-specific adapters) → same stage spine → `LONGFORM_GENERATED_V1` serializer/replay only (`survey_longform_generated_v2.py:4-22`); legacy publication writer never imported/invoked there | Same P1 as Weekly (Thematic side supported). Same renewal + DM022 accepted-upstream paths. Same `REQUEST_CHANGES` re-entry | Same disposable scope as Weekly, plus: four-family reader object validation (`validate_longform_reader_input`), receipt `validate_receipt` independent semantic-review reload, exact trio path check (`surface_gate:1379-1394`) | Same two Human Gates. Four-family coverage does NOT prove arbitrary-Thematic or Retrospective. Missing `topic_scope`/planning authority or `thematic-scope-spec-v2` bytes → stop, ask. Do not invent topic |
| Arbitrary Thematic manual `DIRECT_PRIMARY` | Same `INITIALIZE_THEMATIC` + stages, but review target is canonical primary bytes directly (`surface_gate:1353-1356` + drift check). No reader transform, no generated receipt | P1 still available (same route pair), but receipt type differs (`PRIMARY_ONLY`, no generated trio proof). Post-`VALIDATED_DRAFT` change without `REQUEST_CHANGES` or new edition is unsupported — see §4. Renewal/DM022 only where their stage/State predicates hold; do not force generated-route ops onto a `PRIMARY_ONLY` manuscript | Disposable authoring + exact primary bytes + deterministic QA + semantic/visual reads on those bytes. Can prove "this primary is internally consistent and readable" | Cannot claim generated-reader completeness from a `PRIMARY_ONLY` pass. Cannot convert `PRIMARY_ONLY` to generated coverage by re-labeling. Needs explicit Human agreement that `PRIMARY_ONLY` is the accepted review scope for this `{S}` (question §8) |
| Retrospective manual / period CLI `{S-retro}` | `INITIALIZE_RETROSPECTIVE` → generic `survey_period_v2.period_profile` (monthly/half-year/annual/custom bounded spec). Constraints (`special_pipeline.py:80-97`): `topic_scope` must be null, `community.mode != ENABLED` (OPTIONAL only), coverage `start<end<=retrospective_as_of`, `work_branch==special/<slug>-work`, `source_root==sources/<SP->` | P1 does NOT support `RETROSPECTIVE_PERIOD` (`_route_of` raises `UNSUPPORTED_ROUTE`, `proposal:566-573`). Normal correction is ONLY genuine Human `REQUEST_CHANGES` re-entry (§4) or new edition/renewal where predicates hold; no P1 shortcut. DM022 accepted-upstream still research-only, never publication activation | Disposable run through same spine to `VALIDATED_DRAFT` with period-CLI inputs, real chronology/materialization (`materialize_annual_chronology`, `special_period_consistency*`, `finalize_special_retrospective_compat`), real reader/primary bytes + QA reads | Any claim "P1-corrected Retrospective" is false on current source — record as gap, do not rehearse P1 there. Missing period window/manifest `coverage`/`retrospective_as_of` or Raw permission → stop, ask. Do not invent period |

Mechanical update and accepted-upstream correction are operations, not separate edition rows: use versioned renewal HIGH (`prepare_renewal/finalize_renewal/validate_renewal_receipt/activate_renewal/resume_renewal_activation`) only where State selects a versioned record and prePreview/Exception window holds; use DM022 `prepare_revision/resume_revision/resume_bound_attempt` only as upstream-research correction with pinned COPY + LEGACY DCP/SCP chain, never as publication activation (`DM022_WRONG_FAMILY` at original validation site, `proposal:67-73`). Failure/resume rehearses only the seam actually exercised (guard/no-overwrite/owned-partial per closeout), not a generic crash-recovery proof.

## 4. Current normal-stage predicates and truthful revision choices

- P1 eligibility is narrow (`survey_editorial_correction_proposal_v2.py:548-563`): `lifecycle_state==VALIDATED_DRAFT`, `architecture_review==approved`, `publication_preview==pending` with no provenance, `publication_preview/freeze/release` checkpoints pending, `exception_gate.status==inactive`. Violate any → `INELIGIBLE_STATE`, pre-write refusal. Post-`VALIDATED_DRAFT` "normal correction" without meeting this is not normal.
- P1 route gate (`proposal:566-573`): only `THEMATIC/LONGFORM_SPECIAL` and `WEEKLY/WEEKLY_MAGAZINE`. Retrospective P1 attempt must refuse `UNSUPPORTED_ROUTE`. Record the refusal; do not work around it.
- Draft synthesis entry (`run_drafting_synthesis_v2_interactive.py:68-71`): `ARCHITECTURE_ESTABLISHED` + approved Architecture + strict `validate_agent_state` + DM022 READY entry. No Architecture approval → no Draft.
- Human Gates are exactly `ARCHITECTURE_REVIEW` → `ARCHITECTURE_ESTABLISHED` and exact-byte `PUBLICATION_PREVIEW` → `RELEASE_CANDIDATE` (`AGENTS.md` + `config/survey-production-v2.json:242-260`). Allowed re-entry boundaries: Architecture `ISSUE_INITIALIZED..SELECTION_COMPLETE`; Publication `ISSUE_INITIALIZED..VALIDATED_DRAFT` (including `ARCHITECTURE_ESTABLISHED/DRAFT_COMPLETE`). Boundary must precede the Gate state; unknown boundary → `HumanGateError`. Only genuine Human `APPROVED` or `REQUEST_CHANGES` with explicit `regeneration_boundary` moves State (`survey_human_gate_v2.py:1446-1566`). Silence is never a decision; synthetic fixture Gate/review is never genuine approval; no new Human Gate is created for rehearsal.
- `REQUEST_CHANGES` semantics: records immutable review provenance, selectively invalidates downstream checkpoints/authority, clears only superseded canonical authority blocking regeneration, returns to the chosen allowed boundary as `rN+1`. Publication Preview feedback on `ARCHITECTURE_ESTABLISHED`-or-earlier boundary preserves prior `rN` record + approval snapshot, verifies/supersedes active canonical approval, clears active Architecture provenance, marks Architecture pending, invalidates downstream from boundary (`AGENTS.md` Human-decision section + `survey_human_gate_v2.py:990-1045`). "Manual edit then continue" without this path is not a truthful revision choice.
- Unsupported post-`VALIDATED_DRAFT` paths: any edit/activation after `VALIDATED_DRAFT` that is not (a) pre-acceptance authoring, (b) genuine `REQUEST_CHANGES` re-entry above, or (c) separately lawful operation/new edition with its own predicates (renewal/DM022-accepted where bound) must be refused and logged as blocker. Never pass with a fabricated `REQUEST_CHANGES`, accepted-overwrite, or hash-only admission.

## 5. What disposable rehearsal may / may not do

May (all in disposable copy, autonomous toward Gate per Core `AGENTS.md`):

- Real research/editing: Source Intake (Weekly X required; Special explicit REQUIRED/NOT_REQUIRED rationale), search expansion, Screening, Evidence, completeness/materiality, Selection, Architecture preparation, reader-facing authorship, synthesis, edition-local repair.
- Real deterministic QA + ChatGPT semantic/editorial QA + exact-PDF visual QA reads on real bytes; real `main.tex→main.pdf` build + `main.log`; real receipt replays (`weekly.validate_receipt`, `longform_generated.validate_receipt`).
- Real reader-draft reads to support Human review preparation (e.g. draft packages, reader-surface-input, staged trio) WITHOUT publication activation: building/reading bytes is allowed; `Candidate` atomic binding + `RELEASE_CANDIDATE/FROZEN/RELEASED` transitions are not rehearsed as releases.
- Real failure/resume seams where actually exercised (exclusive COPY claim, guard/no-overwrite, owned-partial windows per closeout).

Must remain pending (never rehearsed as complete):

- Either Human Gate decision itself; `READY_FOR_ARCHITECTURE_REVIEW`, validator PASS, or synthetic review/PDF as genuine approval; any Production push/retain on Profile-bound canonical work branch as reviewed SHA; any `RECORD_*_APPROVAL` without genuine Human bytes.
- Publication activation/supersession via PREARCH (research-only by contract); post-`VALIDATED_DRAFT` overwrite without §4 path; Retrospective P1 (unsupported route).
- No fabricated State: every stage requires exact committed Production State + every Gate input + `agent.validate_agent_state` on canonical `source_root/state` path. Disposable fixture State never substitutes for the reviewed commit.

## 6. Smallest execution sequence (parameterized; target chosen after Explore inventory)

For each of `{W}` + one genuinely needed `{S}` (Thematic-four-family, arbitrary-manual, or Retrospective — chosen on real need, not coverage):

1. Fix target + authority: issue_id / `special_id`+`special_slug`+`edition_kind`+coverage window + work_branch + source_root from permitted material. If any of topic/period/Raw permission missing → §8 question, stop.
2. Disposable init: fresh isolated copy (never reconstruct DB objects); `INITIALIZE_WEEKLY|THEMATIC|RETROSPECTIVE` with recorded request bytes. Record init wall-clock + tool SHAs.
3. Normal spine to `VALIDATED_DRAFT`: intake → Screening → Evidence → completeness/materiality → Selection → Architecture prep → supervised review checkpoint (internal Sol review per governance, NOT Human Gate) → Draft synthesis → reader/generated receipt → deterministic + semantic + visual QA. Log each stage pass/fail + rework loop count.
4. Where applicable and predicates hold: one truthful correction loop — either P1 `prepare_proposal/validate_proposal` (Weekly/Thematic only, §4 eligibility) or genuine simulated `REQUEST_CHANGES` handling WITHOUT forging Human decision (record boundary that *would* apply, do not execute `record_*_approval`/`request_changes` as Human). For Retrospective, record P1-unsupported explicitly instead.
5. Where needed: one mechanical-update or accepted-upstream seam ONLY if its entry predicates actually hold on the rehearsal State; otherwise record "not exercised, predicate X unmet" rather than forcing it.
6. Stop before Human Gate presentation. Package: exact bytes read/built, QA findings, correction disposition, cost rows (§7), blockers/gaps. No Candidate install, no Freeze/Release, no adoption/migration/audit.

Do not invent `{W}`/`{S}`, dates, Raw URLs, or review decisions to fill this sequence.

## 7. Cost comparison without fabrication

Compare against WORKING quality-equivalent existing operation via existing logs only; no full telemetry, no all-old replay, no fake baseline/dates/tokens:

- Use: weekly-regeneration supplement (`notes/rephase-1-weekly-regeneration/logs/20260927T160625Z/` + evidence closeout; S0/S1/S2 are separate synthetic commits, not a full rerun), initial-build-integration real TL2026 PDFs + Gate/QA/Candidate lifecycle (synthetic-authority, semantic NO-GO preserved), profile-support bounded batches (ordinary 28/26, A2 25, affected 37, Selection/7slot/draft 1 each + FINAL applied 7; separate batches, never summed), renewal/editorial qualified composites.
- Distinguish: (a) one-time setup/investment (restore/packaging/tool pinning, fixture authoring, missing-dependency discovery) vs (b) recurring per-edition research/edit/review/build/repair/Human time (intake reads, re-reads, LLM usage, handoffs, regeneration loops, QA/visual reads, Human discovery latency). Existing logs supply (b) only fragmentarily; mark every absent cell `UNKNOWN` rather than reconstructing tokens/time.
- Minimal reusable worklog columns (one row per stage-attempt, append-only):

`date_utc | edition_target | stage_or_op | input_bytes_ref (path+sha) | role (research/edit/review/build/repair/Human) | wall_clock_s (measured or UNKNOWN) | llm_usage (measured or UNKNOWN) | outcome (pass/refusal/rework_loop_N) | rework_reason | blocker_or_gap_ref`

- Report as: `periodic repeat saving − (implementation/verification/audit/migration/parallel-ops/exception handling)` per scope §5; break-even count/rate stays `UNKNOWN` until frequency/horizon/unit-cost are observed. Moving work (e.g. supervisory→operations) is not saving; necessary independent review is not duplication.

## 8. Stopping / escalation and minimal Human questions

Stop and escalate to Astra (not silent Special exclusion, not auto-broaden) when:

- Actual missing topic/period/Raw permission: target/period/coverage/Raw bytes not in authorized material → ask Human, do not synthesize fixture as real need.
- New capability/contract gap: stage/route refuses with a predicate no existing API satisfies (e.g. Retrospective P1, unsupported generation transform, missing reader contract) → return exact caller/predicate/minimal alternative/cost to Astra before broadening.
- Quality/provenance blocker: claim/source/date/comparison or visual defect that normal correction (§4) cannot legally repair → record as adoption blocker for R4 scoping.

Ask Human ONLY when needed, one question at a time, with exact options:

1. `Target/period choice`: `{W} issue_id` + `{S} special_id/kind/coverage` — which concrete Weekly + which ONE genuinely needed Special justifies rehearsal cost? (No rehearsal starts without this.)
2. `Missing bytes permission`: for that target, which Raw/topic/period bytes may be used, or explicitly "none — stop"? (No new intake authority assumed; prior 4-GET/DM021 captures are not standing refresh.)
3. `Review-scope agreement (if manual)`: is `DIRECT_PRIMARY/PRIMARY_ONLY` accepted as the review scope for this `{S}`, or is generated-reader proof required (which may be a gap)?

## 9. Actionable findings and boundaries

- Shortest honest rehearsal is disposable `{W}` generated + ONE needed `{S}` through `VALIDATED_DRAFT` with real QA reads, plus exactly the correction seam whose predicates hold (P1 for Weekly/Thematic; `REQUEST_CHANGES`-shaped re-entry recorded but not forged; P1-refusal recorded for Retrospective). No generic reader unit, no precode/audit, no all-Special replay.
- `DIRECT_PRIMARY` is a legal existing route but a bounded scope (`PRIMARY_ONLY`), not reader-complete proof; four-family success never transfers to arbitrary-Thematic/Retrospective.
- Real semantic/visual work CAN proceed on real disposable bytes to prepare Human review; the Human decision, exact-byte Gate binding, and any activation/release MUST remain pending with no synthetic substitution and no new Gate.
- Cost verdict stays open: setup vs recurring separated, unknowns explicit, no summed suite counts, no fake savings. If rehearsal shows normal correction legally impossible for the needed `{S}`, that is a blocker returned to Astra — not closed with "manual can do it."

(End of working analysis — no code, tests, shipping modules, migration/adoption/audit in this unit.)

---

## Appendix CORR-20261101 — Root corrections (append-only; original §§1–9 preserved, not rewritten)

Read packet `README.md` Root corrections alongside this appendix. This appendix corrects three points in the original; where it conflicts with §§3–8, this appendix governs.

### C1. Correct stage sequence — no init→VALIDATED_DRAFT before Architecture approval

Original §§3–6 stated a disposable run could proceed from initialization through `VALIDATED_DRAFT` while stopping before all Human Gates. That is incorrect as a normal-stage claim: interactive Drafting requires `ARCHITECTURE_ESTABLISHED` plus approved Architecture Review (`run_drafting_synthesis_v2_interactive.py:68-71`), with strict State validation and DM022 READY entry. Drafting/build/quality-to-preview cannot legally precede the Architecture Gate.

Correct bounded sequence (isolated rehearsal copy only; no Production writes/adoption):

- Phase A (before genuine Architecture approval): intake/research (Screening/Evidence/completeness/materiality), Selection, Architecture preparation, and the Human-facing Architecture dossier only. Stop at Architecture Review presentation preparation. No Draft synthesis, no reader/generated receipt build, no Candidate, no Preview preparation.
- Genuine Human Gate 1: `ARCHITECTURE_REVIEW` → `ARCHITECTURE_ESTABLISHED`. Requires genuine Human `APPROVED` on exact committed bytes (Profile-bound work-branch head). Target/material authorization is not approval. No synthetic approval may be fabricated, carried from historical/synthetic fixtures, or inferred from target selection.
- Phase B (only after genuine approval, within its real conditions): permitted drafting synthesis, reader/generated receipt (`WEEKLY_GENERATED_V2` / `LONGFORM_GENERATED_V1`) or exact `DIRECT_PRIMARY` bytes as applicable, deterministic/semantic/visual QA, Preview preparation. Stop before presenting Publication Preview.
- Genuine Human Gate 2 (actual Human Preview, later): exact-byte `PUBLICATION_PREVIEW` → `RELEASE_CANDIDATE`. Likewise genuine decision only; never rehearsed as complete.

Any correction/P1/renewal/DM022 seam in Phase A or B applies only where its own entry predicates actually hold (§4 predicates unchanged). Unmet predicate = record "not exercised," never force or simulate the Gate.

### C2. No new PRIMARY_ONLY-agreement gate

Original §3 (arbitrary-Thematic row) and §8 Q3 framed explicit Human agreement on `DIRECT_PRIMARY/PRIMARY_ONLY` scope as a rehearsal gate question. That extra gate is withdrawn: route scope and limits are normal target-selection material only. Explain and verify the applicable review receipt (`PRIMARY_ONLY` vs generated trio proof) against the actual needed operations when the target is chosen; do not add a separate agreement gate or block Phase A preparation on it.

### C3. Cost baseline — synthetic timings are mechanical investment only

Original §7 listed synthetic fixture logs (weekly-regeneration S0/S1/S2, TL2026 synthetic-authority builds, profile-support bounded batches) alongside production comparison. Correction: those synthetic timings describe mechanical investment/runtime only and must not be equated to a quality-equivalent recurring production baseline. Usable baseline is actual permitted historical production worklogs only within their comparable scope; all missing research/edit/review/build/repair/Human/token/time cells stay `UNKNOWN`. No reconstructed or carried-forward timings.

### Standing boundaries for this correction

- No production-checkout/material inspection was performed for this appendix; Explore's checkout reads exceeded its boundary and that return is quarantined per packet README (not used here, not re-validated, not adopted as corpus/baseline/approval/completeness proof).
- No runtime/Git/network/source edits; this unit remains input-blocked preparation, isolated rehearsal only.
- Remaining inputs (unchanged): target still unchosen; root asks Human for one Weekly + one genuinely needed Special and bounded prospective material access. No automatic execution after this correction.
