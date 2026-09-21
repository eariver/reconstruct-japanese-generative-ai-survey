# Core v2 Deferred Maintenance Summary

Status: `CORE_CHANGE_PAUSED / LIVING_DEFERRED_MAINTENANCE_INVENTORY`  
Established: 2026-09-20 JST  
Last reviewed edition: `2026-W38`  
Last reviewed `main`: `0a0b0747ec6e21b120eb3bf4684d82e241f9d042`  
Frozen Production Line: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`  
Frozen Production Line tree: `cd46a6f7a6dcc4031e76220cea4c52c7dd1fc481`  
Update tracker: [Issue #515](https://github.com/eariver/japanese-generative-ai-survey/issues/515)

## 1. Purpose

This document is the durable human-readable Summary of **known Core v2 problems and generic hardening items that remain unfixed in shared Core while Core modification is intentionally paused**.

It exists so that production can continue with edition-local repairs and bounded compatibility where authorized, without losing the accumulated shared-Core debt needed for a later consolidated maintenance cycle.

This document is **not**:

- Production State authority;
- a Human Gate;
- a replacement for GitHub Issues;
- a replacement for edition-local `execution/defects/*.md`;
- permission to modify shared Core during edition production.

The exact reproduction evidence remains in the linked Issues, edition-local defect records, workflow runs, PRs and frozen releases.

## 2. Core pause policy

Shared Core implementation remains frozen until the Human Owner explicitly resumes Core v2 maintenance.

During this pause:

- do not modify shared Core merely because an edition encounters a defect;
- prefer an edition-local repair when the problem is content/publication-local;
- use a narrowly bounded edition-local runtime compatibility only when separately authorized and already justified by precedent;
- record any new shared-Core defect under the edition execution tree;
- add or update the corresponding item in this Summary at edition closure;
- do not mark an item `CORE_FIXED` because one edition was repaired successfully.

When Core maintenance resumes, this Summary is the primary intake list for deciding the repair batch, dependencies, regression matrix and final fixed-head audit scope.

## 3. Scope

The initial inventory covers:

1. defects first reproduced after the current Production Line was frozen at `774dd39a...`;
2. generic Core hardening explicitly carried forward from W36-W38 edition repairs;
3. one important pre-freeze publication-boundary item that remains open and materially overlaps the post-freeze findings.

Historical items that were fully repaired in shared Core before the frozen Production Line are not included.

## 4. Status vocabulary

| Status | Meaning |
| --- | --- |
| `OPEN_CORE` | Shared-Core defect/hardening is still unresolved. |
| `EDITION_WORKAROUND` | Production can proceed only through an edition-local workaround/compatibility; shared Core remains defective. |
| `EDITION_FIXED_CORE_DEFERRED` | The observed edition was repaired, but a generic Core invariant/regression remains unimplemented. |
| `PARTIALLY_IMPLEMENTED` | Shared Core contains some protection, but the generic issue remains open or has known gaps. |
| `CORE_FIXED_PENDING_REVALIDATION` | A future Core patch exists but has not yet passed required fixed-head regression/production revalidation. |
| `CORE_FIXED` | Reviewed shared Core and required regressions/production validation have closed the item. |

A closed edition-specific GitHub Issue does **not** automatically imply `CORE_FIXED`.

## 5. Current deferred inventory

### CV2-DM-001 — Profile-aware Freeze validates the wrong visual-review schema

Status: `OPEN_CORE / EDITION_WORKAROUND`  
Category: Freeze / authority binding  
Tracking: [Issue #497](https://github.com/eariver/japanese-generative-ai-survey/issues/497)  
First post-freeze reproduction: `2026-W35`  
Latest reproduction: `2026-W38`

The profile-aware Freeze helper expects the legacy post-approval `visual-review-record-v2` shape while current Publication Candidate authority binds the pre-preview `publication-review-record-v2` VISUAL record.

The two contracts are incompatible. W35-W38 therefore used the canonical lower-level `survey_publication_v2.build_freeze` compatibility path instead of repairing shared Core.

Evidence:

- `sources/2026-W35/execution/defects/w35-profiled-freeze-visual-authority-core-defect-20260915.md`
- `sources/2026-W36/execution/defects/w36-freeze-core-defects-20260918.md`
- `sources/2026-W37/execution/defects/w37-freeze-core-defects-20260919.md`
- `sources/2026-W38/execution/defects/w38-freeze-core-defects-20260919.md`

Required future Core direction:

- make profile-aware Freeze validate the Candidate-bound pre-preview VISUAL authority;
- prove profile-aware Freeze and canonical `build_freeze` produce semantically equivalent authority where release identity is the same;
- add Weekly and Special regression coverage.

---

### CV2-DM-002 — Freeze prior-artifact validator treats Human Gate approval as a Stage Checkpoint

Status: `OPEN_CORE / EDITION_WORKAROUND`  
Category: Freeze / provenance typing  
Tracking: [Issue #497](https://github.com/eariver/japanese-generative-ai-survey/issues/497)  
First post-freeze reproduction: `2026-W35`  
Latest reproduction: `2026-W38`

`survey_stage_validation_v2._prior_artifacts()` iterates non-null `checkpoint_provenance` entries and assumes they are Stage Checkpoints. After canonical Publication Preview approval, `checkpoint_provenance.publication_preview` is a Human Gate approval record, not a Stage Checkpoint.

Observed failure:

`prior Stage Checkpoint fails ... stage-checkpoint-v2.schema.json: 'artifacts' is a required property`

W35-W38 used an in-memory admission correction that excludes Human Gate provenance from Stage Checkpoint admission while still validating it through the dedicated Human Gate path.

Required future Core direction:

- type prior provenance by producer/semantic role rather than by non-null pointer;
- preserve validation of true prior checkpoints;
- validate Human Gate authority through the Human Gate contract;
- add RELEASE_CANDIDATE -> FROZEN regression coverage.

---

### CV2-DM-003 — VALIDATED_DRAFT checkpoint authority can exist but be absent from checkpoint_provenance admission

Status: `OPEN_CORE / EDITION_WORKAROUND`  
Category: Stage validation / checkpoint provenance completeness  
Tracking: no dedicated GitHub Issue yet  
First reproduction: `2026-W38`  
Latest reproduction: `2026-W38`

W38 Freeze compatibility additionally had to admit the true `VALIDATED_DRAFT -> RELEASE_CANDIDATE` checkpoint record explicitly because the checkpoint file existed and matched the stage record, but the current stage configuration exposed no corresponding `checkpoint_provenance` pointer (`checkpoints: []`).

Evidence:

- `sources/2026-W38/execution/defects/w38-freeze-core-defects-20260919.md`

Required future Core direction:

- ensure prior-artifact discovery has a complete canonical source for all required prior checkpoint artifacts;
- avoid requiring runtime-only discovery of an otherwise valid checkpoint;
- add a regression for Freeze with a Candidate checkpoint that is valid on disk but omitted by the current provenance map.

---

### CV2-DM-004 — Release workflow invokes non-existent `survey_agent_control_v2.py validate-state`

Status: `OPEN_CORE / EDITION_WORKAROUND`  
Category: Release / post-release provenance closure  
Tracking: no dedicated GitHub Issue yet  
First confirmed reproduction: `2026-W36`  
Latest reproduction: `2026-W38`

The canonical release workflow successfully creates/reconciles the public Release and exact PDF bytes, then fails in the post-release provenance step because it invokes a non-existent `validate-state` CLI subcommand.

Confirmed recurrences:

- W36 workflow run `35345335385` -> recovery PR #504;
- W37 workflow run `35418054523` -> recovery PR #510;
- W38 workflow run `35438708696` -> recovery PR #514.

The bounded recovery does **not** recreate or re-upload the public Release. It writes the missing edition-local release provenance using existing canonical helpers and Python API validation.

Required future Core direction:

- remove/replace the invalid CLI invocation;
- ensure normal release workflow completes the Release Record, Stage Checkpoint and provenance PR without recovery;
- regression test an exact FROZEN -> RELEASED workflow run.

---

### CV2-DM-005 — Reader-surface suppression plumbing is internally inconsistent

Status: `OPEN_CORE / EDITION_FIXED_CORE_DEFERRED`  
Category: Reader-surface validation / suppression transport  
Tracking context: [Issue #434](https://github.com/eariver/japanese-generative-ai-survey/issues/434), closed W36 edition issue #502  
First post-freeze reproduction: `2026-W36`  
Latest reproduction: `2026-W36`

W36 required a public commit-pinned GitHub URL for community-observation auditability. The frozen reader-surface gate treated the public `.../blob/<sha>/surveys/...` URL as internal-path leakage.

The documented file-based suppression mechanism was also unusable through the canonical path:

- loader/documentation disagree on array vs object shape;
- object form is converted to dict keys rather than suppression entries;
- canonical review/stage builders do not thread a working suppression list through;
- direct Python API suppression works but canonical stage validation re-scans and fails.

Evidence:

- `sources/2026-W36/execution/defects/w36-r2-reader-surface-suppression-plumbing-blocker-20260917.md`

W36/W38 avoided changing Core by using a different reader-public citation surface.

Required future Core direction:

- make the documented suppression file shape actually load and apply;
- distinguish public repository permalinks from accidental internal-path leakage;
- ensure canonical builders/validators use the same suppression authority;
- add public-permalink and narrow-suppression regressions.

---

### CV2-DM-006 — Reader-facing Japanese can preserve words while losing technical meaning

Status: `OPEN_CORE`  
Category: Semantic/editorial publication QA  
Tracking: [Issue #501](https://github.com/eariver/japanese-generative-ai-survey/issues/501)  
First reproduction: `2026-W36`  
Latest known reproduction: `2026-W36`

W36 exposed mechanically or over-literally normalized Japanese that became semantically opaque to a technically literate reader.

The edition was repaired, but the generic pre-publication language/semantic fidelity guard remains deferred.

Required future Core direction:

- add a bounded semantic/editorial QA contract before TeX/PDF publication;
- do not solve this solely with forbidden-word substitution;
- preserve conventional English/katakana terms when they are clearer than forced Japanese;
- regression-test representative W36 failures.

---

### CV2-DM-007 — Weekly X Source Intake lacks formal pre-Grok review and low-yield/open-world guarantees

Status: `OPEN_CORE`  
Category: Weekly Source Intake / X observation  
Tracking: [Issue #505](https://github.com/eariver/japanese-generative-ai-survey/issues/505)  
First formalized: `2026-W37`  
Latest edition exercising edition-local hardening: `2026-W38`

Open hardening includes:

- formal pre-Grok Sol task review before Drive handoff;
- candidate-level URL provenance/cardinality;
- low-yield detection and mandatory expansion;
- independent-account accounting;
- open-world / unknown-unknown discovery;
- preservation of URL provenance downstream.

W38 used edition-local task hardening and independent Sol correction, but shared Core remains unchanged.

---

### CV2-DM-008 — Worker output can falsely claim Sol/Human reviewer authority

Status: `OPEN_CORE`  
Category: Reviewer authority / provenance  
Tracking: [Issue #506](https://github.com/eariver/japanese-generative-ai-survey/issues/506)  
First formalized: `2026-W37`  
Latest known relevant edition: `2026-W37`

A worker must not self-author artifacts or rationale labeled as Sol/Human review unless the named authority actually supplied that content.

Required future Core direction:

- separate worker analysis, deterministic validation, independent Sol review and Human decision;
- validate runner/provider vs claimed reviewer identity;
- reject worker-created `sol-*.md` authority artifacts without bound external authority;
- add regression fixtures for false `Sol:`/Human attribution.

---

### CV2-DM-009 — Execution/Human Gate timestamps can be future-dated or timezone-mislabeled

Status: `OPEN_CORE / EDITION_WORKAROUND`  
Category: Provenance chronology  
Tracking: [Issue #507](https://github.com/eariver/japanese-generative-ai-survey/issues/507)  
First formalized: `2026-W37`  
Latest reproduction/handling: `2026-W38`

W37 exposed future-dated and likely local-time-as-`Z` metadata that contradicted commit chronology and Human Gate causal ordering. W38 required edition-local correction ledgers and careful wall-clock handling.

Required future Core direction:

- timezone-aware actual wall clock at write time;
- reject materially future-dated review/state timestamps;
- where commit authority is available, validate `reviewed_at/recorded_at <= containing commit time`;
- validate causal lifecycle ordering;
- preserve historical bad bytes and use append-only correction ledgers rather than rewriting history.

---

### CV2-DM-010 — Weekly trailing boxed block can produce a near-empty page before one-column Sources

Status: `OPEN_CORE / EDITION_FIXED_CORE_DEFERRED`  
Category: Weekly layout / pagination  
Tracking: [Issue #508](https://github.com/eariver/japanese-generative-ai-survey/issues/508)  
First reproduction: `2026-W37`  
Latest edition checked against workaround pattern: `2026-W38`

W37 exposed a two-column body -> trailing Claim Boundary -> `balance` -> `clearpage/onecolumn` failure mode that orphaned the box on an otherwise mostly empty page.

W37 was repaired edition-locally, and W38 retained the accepted closing-page pattern. Generic Weekly regression/layout hardening is still deferred.

Required future Core direction:

- add a Weekly layout fixture for the trailing boxed block transition;
- detect structural page holes/orphan boxes without forcing a fixed page count;
- preserve two-column body and one-column Sources/References identity.

---

### CV2-DM-011 — Temporal confidence can be strengthened downstream beyond source authority

Status: `EDITION_FIXED_CORE_DEFERRED`  
Category: Temporal semantics / synthesis  
Tracking: closed edition Issue #500  
First reproduction: `2026-W36`  
Latest known recurrence: no later blocking recurrence after edition-local discipline

W36 initially turned an unresolved/medium-confidence event-window placement into definite “same week” synthesis prose.

W36 was repaired, but the generic invariant remains deferred:

`source/event temporal confidence -> package -> synthesis`

Required future Core direction:

- prevent weaker or unresolved temporal authority from being serialized as stronger definite chronology;
- regression-test weekly synthesis against unresolved boundary placement.

---

### CV2-DM-012 — Exact community-ledger counts need a reader-auditable public target

Status: `EDITION_FIXED_CORE_DEFERRED`  
Category: Publication provenance / auditability  
Tracking: closed edition Issues #502 and #512  
First reproduction: `2026-W36`  
Latest reproduction: `2026-W38`

W36 lacked a reader-followable target for its community observation. W38 later published an exact `25 / 23 / 2` ledger count while exposing only representative direct X URLs.

Both editions were repaired without shared-Core change.

Required future Core direction:

- if reader-facing prose publishes an exact community-ledger count, require a reader-auditable public target or require the wording to be weakened/qualified;
- preserve context-only status for community/X observations;
- prevent internal candidate/Screening/Selection/Evidence metadata from leaking through the audit surface.

---

### CV2-DM-013 — Source displayed date, collector date and later announcement date can be silently conflated

Status: `EDITION_FIXED_CORE_DEFERRED`  
Category: Temporal source authority  
Tracking: closed edition Issue #511  
First reproduction: `2026-W38`  
Latest reproduction: `2026-W38`

W38 TypeSafe/Jev showed a first-party blog displayed date different from a later founder launch announcement timestamp. The edition initially collapsed the dates into one interpretation.

The edition now carries an append-only two-date correction authority, but the generic invariant is not in shared Core.

Required future Core direction:

`source displayed date -> collector provenance -> Evidence temporal authority -> reader-facing date`

A collector must not replace a first-party displayed date with an X/secondary date without explicitly modeling the distinct event/announcement authority.

---

### CV2-DM-014 — Human-readable execution index can remain stale after successful release recovery

Status: `OPEN_CORE`  
Category: Execution-record closure / navigation consistency  
Tracking: no dedicated GitHub Issue yet  
First observed in final released state: `2026-W37`  
Latest observed: `2026-W38`

The bounded release-provenance recovery intentionally changes only the minimum five Wxx provenance files. As a result, `sources/<edition>/execution/index.md` can still describe the pre-release `RELEASE_CANDIDATE / Publication Preview pending` state after canonical `production-state.json` is already `RELEASED / COMPLETE`.

Machine authority is correct, so this is not a release-integrity defect, but it violates the execution-record policy expectation that `index.md` remain concise and current.

Required future Core/operations direction:

- define whether post-release recovery must also refresh `execution/index.md`;
- if minimal provenance recovery intentionally excludes it, provide a deterministic final navigation refresh step;
- add a closure consistency check between human-readable index and machine lifecycle authority.

---

### CV2-DM-015 — Publication Boundary remains only partially hardened

Status: `PARTIALLY_IMPLEMENTED / OPEN_CORE`  
Category: Publication semantic boundary  
Tracking: [Issue #434](https://github.com/eariver/japanese-generative-ai-survey/issues/434)  
Origin: pre-freeze W33/SP001  
Post-freeze relevance: W36 reader-surface and language/auditability failures demonstrate remaining boundary gaps

The frozen Production Line includes the pre-publication reader-surface gate merged by PR #496, but Issue #434 remains open because the broader contract is larger than lexical leakage detection.

Outstanding generic concerns include:

- internal editorial/review rationale must not become reader prose;
- reader-facing publication payload must not fall back to internal Architecture/Profile fields;
- must-cover fulfillment must point to actual reader content, not prose describing Architecture;
- source-class-specific Claim Boundary rendering;
- bibliography publication transform;
- cross-profile semantic regression coverage.

This item is included as a pre-freeze carry-over because several post-freeze defects depend on or expose remaining gaps in the same boundary.

## 6. Items intentionally not treated as current shared-Core defects

The following edition issues are closed because their edition-level acceptance criteria are satisfied:

- #500 — W36 temporal-boundary wording;
- #502 — W36 community citation target;
- #511 — W38 TypeSafe/Jev temporal authority;
- #512 — W38 full community-ledger auditability.

They remain referenced above only where their **generic Core hardening** has not been implemented.

Issue #448 is not a defect backlog item. It is the persistent operator transport queue.

## 7. Per-edition update contract

This Summary must be reviewed **after every Weekly or Special edition**.

Normal update point:

`edition final verification -> Summary review/update -> edition session close`

If a shared-Core defect prevents normal release, update this Summary at the guarded stop instead.

At each update, review at minimum:

1. new `{source_root}/execution/defects/*.md`;
2. new or changed GitHub Issues created during the edition;
3. Human Architecture/Publication `REQUEST_CHANGES` that imply generic pipeline hardening;
4. Freeze compatibility notes;
5. Release workflow failures and release-provenance recovery PRs;
6. independent Sol review findings that identify a cross-edition failure mode.

Then:

- add a new `CV2-DM-xxx` item for a genuinely new generic problem;
- update `Latest reproduction` / status / evidence on recurring items;
- keep edition-specific repair and generic Core status separate;
- append one row to both the Revision History and Edition Update Ledger;
- if no new item exists, explicitly record `inventory reviewed; no change`.

Do not delete historical Summary items. Transition their status.

## 8. Core maintenance restart contract

When the Human Owner explicitly resumes Core v2 maintenance:

1. freeze a reviewed `main` / Production Line baseline for maintenance intake;
2. read this Summary and all referenced primary defect records/Issues;
3. deduplicate related items without discarding historical IDs;
4. identify dependency groups;
5. define repair batches and regression matrix;
6. implement outside edition production;
7. run exact-head diagnostic CI and the required fixed-head audit;
8. run representative real-production revalidation;
9. mark each item `CORE_FIXED` only after its required regression/production evidence passes;
10. keep the Revision History intact.

A batch repair may close multiple `CV2-DM` items, but each item must receive its own disposition/evidence.

## 9. Edition Update Ledger

| Edition | Summary review | New / materially changed deferred items | Notes |
| --- | --- | --- | --- |
| `2026-W35` | backfilled in r0.1 | DM-001, DM-002 | Freeze defects first formally recorded after Core pause. |
| `2026-W36` | backfilled in r0.1 | DM-004, DM-005, DM-006, DM-011, DM-012 | Release workflow defect first confirmed; reader-surface suppression blocker; W36 publication issues repaired edition-locally. |
| `2026-W37` | backfilled in r0.1 | DM-007, DM-008, DM-009, DM-010, DM-014 | X intake/reviewer authority/timestamp/layout findings; release defect recurred. |
| `2026-W38` | reviewed in r0.1 | DM-003, DM-013; DM-004/009/012/014 recurred | TypeSafe temporal authority and 25-row ledger repaired edition-locally; Freeze/release compatibility still required. |

Next required update: the next Weekly or Special edition closure after `2026-W38`.

## 10. Revision History

| Revision | Date (JST) | Reviewed through | Change |
| --- | --- | --- | --- |
| `r0.1` | 2026-09-20 | `2026-W38` | Initial consolidated deferred-maintenance inventory. Backfilled W35-W38 defect records, post-freeze Issues, release recovery evidence, and relevant pre-freeze Publication Boundary carry-over. Established Core pause policy, stable CV2-DM IDs, per-edition update contract, restart contract, and tracker Issue #515. |

## 11. Reference authority

Primary evidence for the current r0.1 inventory:

- frozen Production Line: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`;
- current reviewed main at establishment: `0a0b0747ec6e21b120eb3bf4684d82e241f9d042`;
- [Issue #497](https://github.com/eariver/japanese-generative-ai-survey/issues/497);
- [Issue #501](https://github.com/eariver/japanese-generative-ai-survey/issues/501);
- [Issue #505](https://github.com/eariver/japanese-generative-ai-survey/issues/505);
- [Issue #506](https://github.com/eariver/japanese-generative-ai-survey/issues/506);
- [Issue #507](https://github.com/eariver/japanese-generative-ai-survey/issues/507);
- [Issue #508](https://github.com/eariver/japanese-generative-ai-survey/issues/508);
- closed edition Issues #500, #502, #511, #512 for deferred generic hardening;
- [Issue #434](https://github.com/eariver/japanese-generative-ai-survey/issues/434) as a pre-freeze carry-over;
- W35-W38 edition-local defect records under `sources/<edition>/execution/defects/`;
- release recovery PRs #504, #510 and #514;
- historical feedback authority: `docs/survey-production-core-v2-production-feedback-backlog.md`.

When a later revision updates an item, cite the newest direct reproduction evidence while retaining the earlier history above.
