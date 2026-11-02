# 2026-W34 Sol Discovery semantic completeness decision — r1

Status: **SOL SEMANTIC DECISION / PRE-DISCOVERY-MATERIALIZATION**  
Date: `2026-09-03` JST  
Issue: `2026-W34`  
Canonical work branch: `weekly/2026-W34-v2-work`  
Reviewed main authority: `c7a898889463b049dea4ee7337ee16ad5fbf3191`  
Observed pre-decision work-branch HEAD: `c98b54a84e5625ac243aa47b830545c972cd3a51`

Decision ID: `SOL-W34-DISCOVERY-COMPLETENESS-20260903-R1`

## 1. Decision

Sol accepts the **semantic Discovery completeness** of the current W34 pre-Screening working set as sufficient to proceed to Raw-backed Discovery materialization.

The accepted semantic baseline is the edition-local working set already materialized at the pre-decision branch HEAD:

- Sol event-level inventory: **105/105** (`W34-C001` through `W34-C105`);
- DailyX topic crosswalk: **76/76** accounted;
- corrected Weekly Grok r2 URL ledger/crosswalk: **47/47** accounted;
- corrected Grok r2 window classification: **10 `ORDINARY_WINDOW` / 20 `BACKGROUND_ONLY` / 17 `LATE_BREAKING`**;
- Weekly carry-over obligation: **1/1 represented**, currently `RECHECKED_UNRESOLVED` with no forced promotion;
- configured GitHub Releases Raw: seven immutable repository-response objects, with five in-window release matches;
- lane-level reverse search and gap review across the Weekly technical surface has been completed by Sol, including explicit boundary/context records and additional events missed by the original X/non-X sensors.

This is a semantic completeness decision only. It is **not** Core `DISCOVERY_COLLECTED` acceptance and is not Screening, Evidence, Materiality, Selection, Architecture, or Human approval.

## 2. Why the blocked collectors do not invalidate the semantic completeness decision

The canonical arXiv and configured official-page collectors remain `RETRY_REQUIRED` with zero response Raw because the available Luna execution surface was blocked before HTTP by the outbound network gate.

Those failures are retained as real capture gaps. They must not be rewritten as collector success or quiet-lane findings.

However, Sol independently expanded and rechecked the W34 Discovery surface using DailyX, corrected Grok r2, existing canonical GitHub Releases Raw, first-party/project locators, primary-source review, and lane-by-lane reverse search. The resulting 105-event working set preserves positive events, negative/boundary findings, context, chronology uncertainties, and authority gaps without silently dropping low-materiality items.

Accordingly, the collector failures remain **capture/provenance gaps**, not a reason to restart broad Discovery from zero or hold semantic completeness indefinitely.

## 3. Core materialization requirement that still blocks formal Discovery acceptance

Current Core v2 schemas require accepted Discovery records to be Raw-backed:

- `schemas/survey-discovery-record.schema.json` requires `source.raw_paths` with at least one item;
- `schemas/discovery-acceptance-v2.schema.json` requires each accepted record to carry at least one `raw_ref` with `path`, `sha256`, and `byte_count`.

The current 105-event working set is a pre-Screening semantic/traceability inventory, not yet a schema-valid Raw-backed Discovery graph.

Therefore the next bounded task is **Discovery Raw materialization**, not additional broad candidate search.

## 4. Frozen scope for the next materialization task

The 105 event identities are the completeness baseline. Luna must not delete an event because it appears low-materiality, duplicative, background-only, post-cutoff, commercially focused, or unlikely to survive Screening.

Event identities may map many-to-one or one-to-many onto source-centric Discovery records when justified by source identity, but every `W34-C001` through `W34-C105` must remain traceable through an explicit event-to-Discovery crosswalk.

The final Discovery record count is **not required to equal 105**. The graph is source/provenance-centric; the 105-event set is the semantic coverage baseline.

If Luna finds that two event identities are genuinely the same event, it may map both to one Discovery record but must retain both event IDs in the crosswalk and record the merge rationale. It must not erase one from traceability.

## 5. Raw/source authority policy for materialization

For Discovery only, Raw is an observation/provenance requirement, not technical Evidence acceptance.

Allowed Raw foundations, in descending preference:

1. existing immutable canonical collector Raw already in the edition;
2. exact imported source bytes already returned by a connected source/Drive artifact where those bytes are available;
3. exact DailyX/Grok observation bytes imported from their known Drive files;
4. bounded source-local capture from a first-party source, following the established Core-v2/W33 Discovery reconstruction pattern;
5. where no first-party artifact is accessible, a bounded observation capture from the best available discovery source, explicitly retaining an `AUTHORITY_GAP` or equivalent boundary for later Evidence review.

A bounded source-local capture must identify the source URL, source title, retrieval/observation time, supported event date when available, and concise source-local observations. It must not fabricate exact HTTP bytes or present tool-extracted/reformatted text as an exact page mirror.

X/secondary observation Raw may establish that a Discovery signal existed. It does **not** establish benchmark values, technical specifications, license terms, model weights, release chronology, security severity, or other publication-grade technical facts. Those remain for Evidence verification.

## 6. X authority boundary

The current required Weekly Grok/X manifest is complete and dispositioned. Preserve:

- canonical run: `weekly-x-2026-W34-r2`;
- post-level authority: `x-url-ledger.corrected.tsv`;
- window counts: `10 / 20 / 17`;
- corrected narrative prose is not count authority;
- X-to-X agreement is discovery confidence only, never technical verification.

DailyX is a separate high-recall X observation corpus and must remain independently attributable from the Weekly Grok r2 run.

## 7. Lifecycle authority

Current Production State remains:

- lifecycle: `ISSUE_INITIALIZED`;
- next action: `stage:discovery`;
- target Human gate: `ARCHITECTURE_REVIEW`.

The next Luna task is authorized to materialize and validate a candidate Discovery graph **without advancing lifecycle**.

After Luna returns a candidate commit, Sol will independently verify:

- Raw integrity and existence;
- 105/105 event traceability;
- DailyX and Grok provenance;
- chronology/boundary preservation;
- Core schema/validator compatibility;
- no scope deletion or unauthorized semantic promotion.

Only after that Sol review may deterministic `stage:discovery` advancement be authorized.

## 8. Explicitly not decided here

This decision does not decide:

- Screening KEEP/DROP decisions;
- technical Evidence acceptance;
- Materiality scoring;
- profile completeness after Evidence;
- final Candidate Selection;
- Architecture roles/order;
- Architecture Review Human Gate outcome;
- reader-facing prose;
- Publication Preview;
- Freeze or Release.

Those remain downstream responsibilities under current Core authority.
