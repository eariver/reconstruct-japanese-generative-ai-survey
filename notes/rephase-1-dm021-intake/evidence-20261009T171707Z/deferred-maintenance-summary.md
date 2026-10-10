# Core v2 Deferred Maintenance Summary

Status: `CORE_CHANGE_PAUSED / LIVING_DEFERRED_MAINTENANCE_INVENTORY`  
Established: 2026-09-20 JST  
Last reviewed edition: `SP-vision-multimodal-2026`  
Last reviewed `main`: `7c8e4b1ee913007e4d1e0dc627e2c0a7c2f5ff4f`  
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
Latest reproduction: `2026-W39`

The profile-aware Freeze helper expects the legacy post-approval `visual-review-record-v2` shape while current Publication Candidate authority binds the pre-preview `publication-review-record-v2` VISUAL record.

The two contracts are incompatible. W35-W38 therefore used the canonical lower-level `survey_publication_v2.build_freeze` compatibility path instead of repairing shared Core. TS-001 reissue recurred identically (candidate-bound pre-preview VISUAL `fae79e67...` vs legacy `pdf_path` schema) and used the same lower-level path plus the CV2-DM-019 identity correction below. TS-002 (`SP-beyond-text-2026`) recurred identically (candidate-bound pre-preview VISUAL `56db5134...` vs legacy `pdf_path` schema) via edition-local `execution/ts002-freeze-compat-20260928.py`; no new ID. W39 reproduced the same schema mismatch during `RELEASE_CANDIDATE -> FROZEN`; the lower-level canonical publication freeze path was again required with no shared-Core change.

Evidence:

- `sources/2026-W35/execution/defects/w35-profiled-freeze-visual-authority-core-defect-20260915.md`
- `sources/2026-W36/execution/defects/w36-freeze-core-defects-20260918.md`
- `sources/2026-W37/execution/defects/w37-freeze-core-defects-20260919.md`
- `sources/2026-W38/execution/defects/w38-freeze-core-defects-20260919.md`
- `sources/SP-efficient-llm-2026/execution/defects/ts001-reissue-freeze-core-defects-20260923.md`
- `sources/SP-beyond-text-2026/execution/defects/ts002-freeze-core-defects-20260928.md`
- `sources/2026-W39/execution/defects/w39-freeze-compat-note-20260929.md`

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
Latest reproduction: `2026-W39`

`survey_stage_validation_v2._prior_artifacts()` iterates non-null `checkpoint_provenance` entries and assumes they are Stage Checkpoints. After canonical Publication Preview approval, `checkpoint_provenance.publication_preview` is a Human Gate approval record, not a Stage Checkpoint.

Observed failure:

`prior Stage Checkpoint fails ... stage-checkpoint-v2.schema.json: 'artifacts' is a required property`

W35-W38 used an in-memory admission correction that excludes Human Gate provenance from Stage Checkpoint admission while still validating it through the dedicated Human Gate path. TS-001 reissue recurred identically (`gates/publication-preview-approval.json` `15b88fb2...`) and used the same bounded correction. TS-002 recurred identically (`gates/publication-preview-approval.json` `5e121516...`) via the same bounded correction. W39 reproduced the same Human-gate-as-checkpoint misclassification after canonical r6 approval and used the same bounded runtime admission; no new ID.

Evidence:

- `sources/2026-W39/execution/defects/w39-freeze-compat-note-20260929.md`

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
Latest reproduction: `2026-W39`

W38 Freeze compatibility additionally had to admit the true `VALIDATED_DRAFT -> RELEASE_CANDIDATE` checkpoint record explicitly because the checkpoint file existed and matched the stage record, but the current stage configuration exposed no corresponding `checkpoint_provenance` pointer (`checkpoints: []`).

TS-001 reissue recurred identically: `orchestration/v2/checkpoints/VALIDATED_DRAFT.json` carries the exact r2 `publication-candidate` artifact (`adf22516...`) but is unreferenced by `checkpoint_provenance`; the same bounded admission was applied. TS-002 recurred identically: `orchestration/v2/checkpoints/VALIDATED_DRAFT.json` carries the exact r12 `publication-candidate` artifact (`4d2c01ab...`) but is unreferenced; the same bounded admission was applied. W39 again required explicit admission of the canonical sibling `VALIDATED_DRAFT` checkpoint during Freeze compatibility validation; no new ID.

Evidence:

- `sources/2026-W38/execution/defects/w38-freeze-core-defects-20260919.md`
- `sources/SP-efficient-llm-2026/execution/defects/ts001-reissue-freeze-core-defects-20260923.md`
- `sources/SP-beyond-text-2026/execution/defects/ts002-freeze-core-defects-20260928.md`
- `sources/2026-W39/execution/defects/w39-freeze-compat-note-20260929.md`

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
Latest reproduction: `2026-W39`

The canonical release workflow successfully creates/reconciles the public Release and exact PDF bytes, then fails in the post-release provenance step because it invokes a non-existent `validate-state` CLI subcommand.

Confirmed recurrences:

- W36 workflow run `35345335385` -> recovery PR #504;
- W37 workflow run `35418054523` -> recovery PR #510;
- W38 workflow run `35438708696` -> recovery PR #514;
- `SP-efficient-llm-2026` workflow run `35863535480` -> recovery PR #524
  (`special/efficient-llm-2026` Release created and exact-byte reconciled before
  the sole `validate-state` failure; provenance recovered edition-locally via
  `survey_release_checkpoint_v2.py` + Python API `validate_agent_state`);
- `SP-beyond-text-2026` workflow runs `36333979769` (created) / `36333984167` (reconciled)
  (`special/beyond-text-2026` Release created and exact-byte reconciled before
  the sole `validate-state` failure in both runs; provenance recovered edition-locally via
  `survey_release_checkpoint_v2.py` + Python API `validate_agent_state` -> recovery PR #549);
- `2026-W39` workflow run `36581201216` -> recovery PR #557
  (public `weekly/2026-W39` Release and exact approved PDF bytes were created/reconciled successfully; the workflow then failed in post-release provenance closure and the W38-style bounded recovery recorded the missing Release Record/checkpoint/state through a normal PR without recreating the public Release).

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
Tracking: [Issue #501](https://github.com/eariver/japanese-generative-ai-survey/issues/501) + [Issue #534](https://github.com/eariver/japanese-generative-ai-survey/issues/534)  
First reproduction: `2026-W36`  
Latest known reproduction: `SP-vision-multimodal-2026`

W36 exposed mechanically or over-literally normalized Japanese that became semantically opaque to a technically literate reader.

TS-002 (`SP-beyond-text-2026`) reproduced the same generic failure at larger scale across three bounded edition-local passes plus seed-independent Sol audits:

- TS-002 evidence: [Issue #533](https://github.com/eariver/japanese-generative-ai-survey/issues/533) (first-pass: `零射影`/`声器`/`符号言語`/`無撞着`/`抽出推論`/Transformer literalization), [Issue #539](https://github.com/eariver/japanese-generative-ai-survey/issues/539) (second-pass: `模型`/`U 網`/`波形網`/frame/GPU/attention families), [Issue #543](https://github.com/eariver/japanese-generative-ai-survey/issues/543) + Sol authoritative maps r2–r10 and Muse candidate returns under `sources/SP-beyond-text-2026/execution/terminology-issue543/` plus `sol-terminology-readback-issue543-*.md` (final broad normalization + seed-independent residuals incl. VBench dimension identity loss).
- The edition was repaired edition-locally (276-row terminology ledger at closure; exact 78pp PDF `4e225067...` released), but the generic pre-publication language/semantic fidelity guard remains deferred.
- TS-002 demonstrates that a simple forbidden-word list is insufficient: seed-list zero counts did not imply closure (Sol r1/r3/r7/r10 each found seed-external residuals after worker zero), context-dependent terms require source-bound adjudication, and canonical model/metric/benchmark/dataset identities require entity-preservation scanning beyond lexical matching.

W39 then reproduced CV2-DM-006 again in a Weekly profile. Publication Preview r1-r4 required repeated edition-local terminology repair under Issue #501, including forced/literal forms such as `模型`, `符号`, `番付`, `腕前の物差し`, `値札`, `手ほどき`, `真としない`, and other seed-external residuals. Three W39-specific additive seed supplements plus a final seed-independent Sol reread were needed before the r6 reader bytes were accepted. This confirms that the defect is not confined to Longform Specials and that zero-hit completion against a fixed seed is not sufficient closure evidence.

TS-003 (`SP-vision-multimodal-2026`) reproduced this failure after `VALIDATED_DRAFT`: independent reader review corrected forced/untranslated editorial terms (`exhibits`, `cap`, `残差 reformulation`) and an ambiguous double-negative in the OpenPose description, while paper review still found `模型` (8), `基線` (2), and `hardware` (1) as nonblocking residuals under Issue #534. The nine bounded reader repairs were accepted before exact-byte Human approval. Edition-local closure does not fix the generic language QA gap.

Generic reusable seed corpus (authority seed for future read-only lint, no auto-rewrite):

- `docs/editorial/ja-technical-terminology-overtranslation-seed.md` (100 H4 entries across 10 families + canonical-identity section + context-dependent section + snapshot-only counts; every entry `auto-rewrite allowed: false`; de-duplicates #533/#539/#543 + post-seed Sol/Muse findings);
- W39 additive review corpora:
  - `docs/editorial/ja-technical-terminology-overtranslation-seed-w39-additions.md`;
  - `docs/editorial/ja-technical-terminology-overtranslation-seed-w39-r2-residual-additions.md`;
  - `docs/editorial/ja-technical-terminology-overtranslation-seed-w39-r3-residual-additions.md`.

Required invariant:

> technically established Japanese wording is allowed; the defect is forced, non-standard, or identity-destroying translation that makes a technically literate Japanese reader reconstruct the English source term.

The scope of CV2-DM-006 is not “avoid kanji”. Established Japanese (`符号器`/`復号器`/`潜在`/`写像`/etc.) stays allowed; the defect is forced overtranslation.

Required future Core direction:

- add a bounded semantic/editorial QA contract before TeX/PDF publication;
- do not solve this solely with forbidden-word substitution;
- preserve conventional English/katakana terms when they are clearer than forced Japanese;
- regression-test representative W36 and W39 failures;
- add known prohibited/review-required scan from the seed corpus;
- add same-concept consistency scan (e.g. `zero-shot`/`ゼロショット`/`零射影` variants in one edition);
- add canonical-name/entity preservation scan (model/architecture/method/metric/benchmark/dataset);
- add benchmark/metric identity scan (incl. VBench/VBench-2.0 dimension identities);
- add seed-independent suspicious-translation scan (broad scan must not stop at seed-list zero);
- provide a reviewed exception mechanism (`REPLACE`/`RETAIN` with source/context reason);
- prohibit auto-rewrite (detection + human/Sol review only).

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

### CV2-DM-013 — Distinct source/version/event dates can be silently conflated or diverge across reader surfaces

Status: `EDITION_FIXED_CORE_DEFERRED`  
Category: Temporal source authority  
Tracking: closed edition Issue #511 + closed W39 Issue #551  
First reproduction: `2026-W38`  
Latest reproduction: `2026-W39`

W38 TypeSafe/Jev showed a first-party blog displayed date different from a later founder launch announcement timestamp. The edition initially collapsed the dates into one interpretation.

W39 exposed the same generic temporal-authority weakness in two additional forms during Issue #551 review:

- DolphinBench arXiv v1 (Sep.21) and v2 (Sep.22) were compressed into reader wording equivalent to `9月21日（改め22日）`, obscuring the distinct version events;
- Claude Code source-note prose retained Sep.23 while the reader body, bibliography and accepted official `@ClaudeDevs` ledger authority all bound the behavior announcement to Sep.25.

Both W39 instances were repaired edition-locally before r6 approval, but no generic cross-surface temporal consistency guard exists in shared Core.

Required future Core direction:

`source displayed/version/event date -> collector provenance -> Evidence temporal authority -> reader-facing date(s)`

- model distinct source publication, source revision/version, announcement and collector timestamps explicitly rather than collapsing them;
- prevent a later/secondary timestamp from replacing a first-party displayed date without an explicit distinct-event model;
- check repeated reader/source-note/bibliography surfaces for contradictory dates bound to the same event identity;
- regression-test W38 TypeSafe/Jev plus W39 DolphinBench and Claude Code date cases.

---

### CV2-DM-014 — Human-readable execution index can remain stale after successful release recovery

Status: `OPEN_CORE`  
Category: Execution-record closure / navigation consistency  
Tracking: no dedicated GitHub Issue yet  
First observed in final released state: `2026-W37`  
Latest observed: `2026-W39`

The bounded release-provenance recovery intentionally changes only the minimum five Wxx provenance files. As a result, `sources/<edition>/execution/index.md` can still describe the pre-release `RELEASE_CANDIDATE / Publication Preview pending` state after canonical `production-state.json` is already `RELEASED / COMPLETE`.

W39 reproduces this exactly after recovery PR #557: canonical `sources/2026-W39/production-state.json` is `RELEASED / COMPLETE`, while `sources/2026-W39/execution/index.md` still says `RELEASE_CANDIDATE`, Publication Preview r6 pending and `next action: PUBLICATION_PREVIEW`, and even retains the stale statement `Shared Core defects: None discovered in this run` despite the later Freeze/Release recurrences.

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
Post-freeze relevance: W36 and TS-003 reader-surface/authority leakage demonstrate remaining boundary gaps

The frozen Production Line includes the pre-publication reader-surface gate merged by PR #496, but Issue #434 remains open because the broader contract is larger than lexical leakage detection.

Outstanding generic concerns include:

- internal editorial/review rationale must not become reader prose;
- reader-facing publication payload must not fall back to internal Architecture/Profile fields;
- must-cover fulfillment must point to actual reader content, not prose describing Architecture;
- source-class-specific Claim Boundary rendering;
- bibliography publication transform;
- cross-profile semantic regression coverage.

TS-003 independently caught and removed `IDは受入時に修正済みである。` from P07B/Detic reader prose after earlier publication-layer validation. This is a concrete recurrence of internal editorial/process metadata leaking into the reader surface; its bounded R04 repair is accepted and the general publication-boundary weakness remains open.

This item is included as a pre-freeze carry-over because several post-freeze defects depend on or expose remaining gaps in the same boundary.

---
 
### CV2-DM-016 — Evidence source-class map rejects canonical Thematic source types

Status: `OPEN_CORE / EDITION_WORKAROUND`  
Category: Evidence / authority source classification  
Tracking: [Issue #515](https://github.com/eariver/japanese-generative-ai-survey/issues/515)  
First reproduction: `SP-efficient-llm-2026`  
Latest reproduction: `SP-efficient-llm-2026`

The frozen Production Line accepts an open Discovery `source_type` vocabulary through canonical Discovery and Screening, but the Evidence path later fail-closes against a narrower hard-coded `SOURCE_CLASS_MAP`.

In `SP-efficient-llm-2026`, canonical Screening completed over 165 Discovery records, but the Evidence runner failed at the first `PRIMARY_DOC` task with:

```text
unsupported source_type for Evidence authority: 'PRIMARY_DOC'
```

The edition audit found **67 of 160 non-DROP Evidence tasks** bound to 10 canonical Thematic source types that are accepted upstream but missing from the frozen Evidence source-class map:

- `PRIMARY_DOC`
- `PRIMARY_REPO`
- `PRIMARY_ANNOUNCEMENT`
- `PRIMARY_MODEL_CARD`
- `PRIMARY_SPEC`
- `SECONDARY_REFERENCE`
- `SECONDARY_TECHNICAL`
- `RUNTIME_RECIPE`
- `PACKAGING_DOCS`
- `RUNTIME_PR`

Direct evidence:

- `sources/SP-efficient-llm-2026/execution/defects/shared-core-evidence-source-map-gap-20260922.md`
- blocked Evidence session `sources/SP-efficient-llm-2026/execution/sessions/ts001-reissue-evidence-20260922.md`

The defect is structurally similar to the pre-freeze W34 source-map gap repaired by PR #486, but shared Core modification is currently paused. The edition therefore must not rewrite accepted Discovery identities or patch Core in place.

Authorized edition-local compatibility direction:

- preserve canonical Discovery and Screening bytes;
- use a deterministic, explicit source-type projection only in derived Evidence Task copies;
- allow only the reviewed mapping from the 10 Thematic source types to existing frozen Core authority classes;
- record original/projected task hashes and per-task mapping in an edition-local compatibility ledger;
- fail closed on any unmapped source type;
- run the resulting package, Evidence Cards, Edition Views, Materiality and Completeness through the **unmodified frozen Core validators**;
- use the canonical Evidence Authority Supplement path for corrected/additional post-Screening source bodies rather than rewriting Discovery provenance.

An edition-local compatibility success does **not** close this generic Core defect.

Required future Core direction when maintenance resumes:

- make Discovery/Screening/Evidence source-type admission internally consistent;
- classify the 10 reviewed Thematic source types explicitly by provenance;
- remove the duplicate/narrow Evidence-runner source-class map or prove it cannot diverge from the canonical mapping;
- preserve unknown-source fail-closed behavior;
- add cross-profile regression coverage proving every source type accepted into canonical Discovery/Screening is either Evidence-classifiable or rejected before Screening.

---

### CV2-DM-017 — Completeness builder omits Discovery-added obligations required by its validator

Status: `OPEN_CORE / EDITION_WORKAROUND`  
Category: Completeness / obligation materialization  
Tracking: [Issue #515](https://github.com/eariver/japanese-generative-ai-survey/issues/515)  
First reproduction: `SP-efficient-llm-2026`  
Latest reproduction: `SP-efficient-llm-2026`

During the frozen-Core Evidence compatibility execution for `SP-efficient-llm-2026`, the current interactive Completeness builder and validator exposed a second generic contract mismatch.

The edition's canonical Discovery gap-fill introduced edition-local obligations `EFF-O13`, `EFF-O14`, and `EFF-O15` in Discovery provenance. The frozen interactive builder `run_evidence_v2_interactive._build_completeness` materializes the Production Profile's initial obligations only, while the frozen Completeness validator additionally requires every obligation ID named by Discovery provenance to appear in the Completeness result.

Consequently, a builder-produced payload is incomplete relative to its own downstream validator whenever a valid Discovery expansion introduces new obligation IDs after Profile initialization.

Direct reproduction/evidence:

- `sources/SP-efficient-llm-2026/execution/compat/evidence-source-class-projection/run_frozen_evidence_chain.py`
- `sources/SP-efficient-llm-2026/execution/compat/evidence-source-class-projection/validation-report.md`
- `sources/SP-efficient-llm-2026/profile-completeness-v2.json`

The edition-local compatibility path appends the three exact Discovery-declared rows with mechanically derived Discovery/Evidence bindings and then submits the full payload to the **unchanged frozen Completeness schema and validator**. Shared Core remains unchanged.

This workaround does not close the generic defect.

Required future Core direction when maintenance resumes:

- make the canonical Completeness builder enumerate the same obligation authority set that the validator requires;
- define the supported lifecycle for obligations introduced by post-initialization Discovery/gap-fill;
- either materialize Discovery-added obligations deterministically or reject unsupported obligation introduction before downstream Evidence;
- preserve exact Profile dimension membership and Discovery/Evidence binding checks;
- add regression coverage for Thematic Discovery expansion that adds valid new obligation IDs after initialization;
- ensure builder output validates without edition-authored structural completion rows.

---

### CV2-DM-018 — Longform Publication QA can PASS gross Overfull hbox / rendered clipping

Status: `OPEN_CORE / EDITION_FIXED_CORE_DEFERRED`  
Category: Publication QA / visual-layout regression  
Tracking: [Issue #520](https://github.com/eariver/japanese-generative-ai-survey/issues/520)  
First reproduction: `SP-efficient-llm-2026`  
Latest reproduction: `SP-efficient-llm-2026`

TS-001 reissue Publication Preview r1 exact PDF (`bc6e280c668a4a17ff98dae58fc574cdce701cce9dd8926eb8b1138e82a46e0b`, 66 pages) contained a visible clipping defect on p.56: the first glossary `tabular` was pushed right by paragraph/table context and overflowed ~70pt beyond text width, cropping definition text.

The r1 build log recorded the corresponding `Overfull \hbox (~70pt)` but Publication Preview prep did not treat it as blocking, and the r1 VISUAL review recorded PASS over the exact clipped bytes. The defect was therefore Human-reported via Issue #520, not machine-blocked.

Source cause (edition-local, layout-only):

```tex
\subsection*{用語集}
本巻で使う技術用語の定義を集めたものである。節をまたいで同じ言葉が同じ意味で使われていることを確かめるために置いた。
\begin{tabular}{@{}p{0.18\textwidth}p{0.75\textwidth}@{}}
```

Paragraph termination was not explicit between the lead sentence and the first `tabular`, so the table was treated in a bad paragraph/layout context and pushed right. Later p.57/p.58 glossary tables with identical column widths rendered correctly, confirming layout context (not column width) as the cause.

Edition repair (r2, `EDITION_FIXED`):

- minimum layout-only fix: `...置いた。\par` + `\noindent` before the first `tabular`; no glossary content rewrite; no unrelated page redesign;
- r2 CI build (run `35801995228`, PDF `8a9a721ac35b2e5baa2e20162b5a6ba4ae63945d512d985484aeae56073a23c1`, 66 pages) has max Overfull `10.0pt` (0 BLOCK, 12 REVIEW_REQUIRED at 10.0pt in full-width tables with explicit rendered disposition, 6 RECORD at 8.99pt);
- p.56 first table fully within bounds with 0 clipping; p.57/p.58 unchanged and correct; full 66pp render with no overlap/cropped/orphan/blank/hole/bibliography regression;
- edition-local guard `sources/SP-efficient-llm-2026/execution/validation/overfull_hbox_guard.py` (≥20pt BLOCK, 10–20pt REVIEW_REQUIRED, <10pt RECORD) enforced for r2; exact generic threshold remains a deferred Core decision.

Direct evidence:

- [Issue #520](https://github.com/eariver/japanese-generative-ai-survey/issues/520) (r1 commit `1266a5f02…`, PDF `bc6e280c…`, ~70pt log finding, acceptance criteria)
- r2 repair: `special/efficient-llm-2026-work` Publication Preview r2 (PDF `8a9a721a…`, overfull guard `overfull-guard-r2.json`, visual review full-66pp PASS, prep `publication-preview-prep-r2.md`)
- Related prior layout series (not duplicates, cited in #520): #79, #106, #400

Issue #521 (`DeepSeek V4.1 Flash 8B input / 16B output` reader wording) was evaluated alongside and is explicitly **not** added as a Core item: it is `EDITION_LOCAL / PUBLICATION_CORRECTNESS` (bounded wording repair, no generic transformation rule found). No Core defect is invented for #521.

Required future Core direction when maintenance resumes:

- make gross TeX overflow detectable before Human Publication Preview;
- define reviewed blocking/review-required threshold policy;
- bind build-log overflow findings to rendered-page review;
- ensure LONGFORM_SPECIAL appendix/glossary pages are included in mandatory rendered review coverage;
- add a regression fixture reproducing the p.56 glossary paragraph/table context;
- prohibit VISUAL PASS when a materially clipped page exists.

---

### CV2-DM-019 — Canonical Freeze builder derives release identity from internal issue_id instead of the profile public slug

Status: `OPEN_CORE / EDITION_WORKAROUND`  
Category: Freeze / public release identity  
Tracking: [Issue #515](https://github.com/eariver/japanese-generative-ai-survey/issues/515)  
First reproduction: `SP-efficient-llm-2026`  
Latest reproduction: `SP-beyond-text-2026`

`scripts/survey_publication_v2.py::build_freeze` derives the Release Manifest identity via `release_identity(publication_profile, issue_id)`. For `SP-efficient-llm-2026` (internal issue `SP-efficient-llm-2026`, public survey slug `efficient-llm-2026`) the reference canonical build yields `special/SP-efficient-llm-2026`.

The frozen release workflow (`.github/workflows/survey-production-v2-release.yml`, authority step) mandates:

```text
tag = manifest['release_identity']
expected_tag = profiled.release_identity(profile)  # paths.survey_root slug
if tag != expected_tag: raise SystemExit('Release Manifest public identity mismatch')
```

i.e. `special/efficient-llm-2026`. A bare-`build_freeze` manifest would therefore hard-fail the frozen release for every divergent-slug edition. SP001 never exposed this (slug `SP001` == issue_id `SP001`, convergent); divergent-slug retrospectives froze under the pre-v2 flow. TS-001 reissue is the first divergent-slug LONGFORM_SPECIAL freeze under Core v2.

Edition-local compatibility (TS-001, runtime-only, no Core change):

- Freeze Record written byte-identical to the canonical `build_freeze` reference (same `frozen_at`);
- Release Manifest byte-identical to the reference EXCEPT `release_identity` (`special/efficient-llm-2026`, the exact value the frozen workflow enforces) and the Freeze path rebound from the reference scratch path to the canonical Freeze path (same SHA); re-validated via `validate_release_manifest`;
- the resulting public Release (`special/efficient-llm-2026`, canonical run `35863535480`) passed the workflow's identity check, confirming the diagnosis.

Direct evidence:

- `sources/SP-efficient-llm-2026/execution/ts001-freeze-compat-20260923.py`
- `sources/SP-efficient-llm-2026/execution/defects/ts001-reissue-freeze-core-defects-20260923.md`
- workflow run `35863535480` (identity check passed; later failed only on CV2-DM-004)
- TS-002 recurrence: `sources/SP-beyond-text-2026/execution/ts002-freeze-compat-20260928.py`
- `sources/SP-beyond-text-2026/execution/defects/ts002-freeze-core-defects-20260928.md`
- workflow runs `36333979769` / `36333984167` (identity check passed for `special/beyond-text-2026`; later failed only on CV2-DM-004; no new ID)

Required future Core direction when maintenance resumes:

- derive the Freeze/Manifest release identity from the Production Profile public slug (single authority with the release workflow), not the internal issue_id;
- prove profile-aware Freeze and canonical `build_freeze` produce identical Freeze authority and identical Manifest bytes for both convergent and divergent slugs (extends the CV2-DM-001 equivalence requirement);
- add divergent-slug LONGFORM_SPECIAL regression coverage through the release identity check.

---

### CV2-DM-020 — Citation resolution does not guarantee claim-to-source semantic fidelity

Status: `OPEN_CORE / EDITION_FIXED_CORE_DEFERRED`  
Category: Publication QA / claim-source semantic binding  
Tracking: closed W39 [Issue #551](https://github.com/eariver/japanese-generative-ai-survey/issues/551) + [Issue #515](https://github.com/eariver/japanese-generative-ai-survey/issues/515)  
First reproduction: `2026-W39`  
Latest reproduction: `SP-vision-multimodal-2026`

W39 Publication Preview demonstrated a generic gap between deterministic citation/key resolution and **semantic correctness of the claim actually bound to that source**. All citation keys could resolve while reader prose still misrepresented novelty, strengthened a source beyond its stated conclusion, flattened conditional/attributed numbers, or bound the wrong source role.

Issue #551 exposed several independent manifestations in one edition:

- **ART novelty:** reader prose initially made the reverse transcriptase itself appear newly discovered, while primary-source read-back showed the RT was already known and the novelty was the system-level combination of RT + partner/accessory gene + long repeat array;
- **Cursor proxy strength:** reader prose strengthened a source saying evals can be a fast/useful proxy with distributional limitations into an effectively categorical `当てにならず` conclusion;
- **Claude Code source role:** a Sep.25 behavior-change claim was initially bound only to secondary material even though the accepted public ledger already contained the official `@ClaudeDevs` first-party announcement; behavior and plan-tier conditions required separate source bindings;
- **Opus 5.5 conditions:** `typical workload` cost estimation and `up to 2.5x faster` were flattened into less-qualified reader wording until source read-back restored attribution/conditionality;
- **source-boundary contradiction:** after binding the official X post as first-party evidence, `99-source-notes.tex` still categorically said public-post ledger material could not establish publication facts, requiring an explicit role-based exception limited to separately cited official first-party posts.

W39 was repaired publication-locally and released exact Human-approved r6 bytes. TS-003 subsequently reproduced the same general gap even though all 178 citations resolved across 124 unique Evidence/Bib keys: independent Human paper review found the DETR 300-epoch / 16 V100 / ~3-day training setting incorrectly conflated with its 500-epoch comparison setting, POPE `polling` mistranslated as voting, and MMBench EN/ZH misidentified as Japanese/English. All three were corrected under PR-01/02/03 and independently checked against primary papers before exact-byte Human approval; the accepted Evidence was preserved with an edition-local correction ledger. The generic Core gap remains: citation existence/key resolution and source admission do not prove that the drafted claim preserves the source's subject, novelty, scope, strength, conditions, attribution, or authority role.

This is related to but distinct from:

- CV2-DM-006, which targets forced/identity-destroying Japanese terminology;
- CV2-DM-013, which targets temporal authority/date identity;
- CV2-DM-015, which targets the broader internal/public Publication Boundary.

Required future Core direction when maintenance resumes:

- add an explicit claim-to-source semantic-fidelity review contract before Publication Preview;
- require claim decomposition where one sentence mixes behavior, plan/tier conditions, prices, benchmark results, or other claims supported by different source roles;
- preserve source epistemic strength (`can`, `may`, `up to`, `typical`, estimated/attributed) through synthesis and reader serialization;
- prefer/require admitted first-party authority for the exact first-party fact when available, while allowing separately bounded secondary support for details not present in the primary source;
- validate source-role consistency between reader citations, bibliography/source notes and public/community ledgers;
- distinguish `citation key resolved` from `claim semantically supported` in QA results;
- add regression fixtures from W39 ART, Cursor, Claude Code and Opus 5.5;
- fail closed or require explicit reviewed disposition when a semantic/source-role mismatch is found.

---

### CV2-DM-021 — Post-VALIDATED_DRAFT reader/editorial corrections have no truthful revalidation reason class

Status: `OPEN_CORE / EDITION_WORKAROUND`  
Category: Publication-surface revalidation / lifecycle provenance / exact-PDF Freeze and Release  
Tracking: [Issue #560](https://github.com/eariver/japanese-generative-ai-survey/issues/560) and umbrella [Issue #515](https://github.com/eariver/japanese-generative-ai-survey/issues/515)  
First reproduction: `SP-vision-multimodal-2026` (TS-003)  
Latest reproduction: `SP-vision-multimodal-2026` (2026-10-10 JST)

The shared Core v2 already supports an immutable, State-bound post-validation publication-surface revalidation record, but both `scripts/survey_agent_control_v2.py` and `schemas/publication-surface-revalidation.schema.json` allow only the `REVIEWED_CORE_CHANGE` reason class. Legitimate independent/editorial/Human PDF review corrections occurring **after** `VALIDATED_DRAFT` are not a reviewed shared-Core change. Using that reason would misstate review authority; silently rewriting immutable `DRAFT_COMPLETE.json` or publishing its old PDF would violate exact-byte provenance.

TS-003 reproduced this gap:

- Immutable `DRAFT_COMPLETE.json` bound the old canonical `main.pdf` SHA-256 `0916bb5e6222a48de002773eaa1963da9decee90b73b5fc5d292fc08caff3148` and `main.tex` `edcf8ef982a63ac9dc65881aae1963a7daf64fa7fc16de67fbf97825cba090cb`.
- Human-approved, independently QA-closed corrected PDF was `b2de84493f2215e26d16e569498c5f4b6476ebc314230cbb4e01540a72742093` (708782 bytes, 39 pages) under `execution/reader-paper-fidelity-repair-20261009/`.
- `production-state.json` remained `VALIDATED_DRAFT`, `publication_preview = pending`, and the stale normal Publication Candidate could not legitimately stand for this approved PDF.
- The Human Owner explicitly authorized a **one-off Core v2 publication-path bypass conditional on logging the shared-Core defect**. Issue #560 was opened; approved exact bytes plus TeX/Bib/style and research/QA/approval evidence were Freeze-pinned with an explicit `EXCEPTION_FROZEN` manifest and merged via PR #561.
- Public GitHub Release `special/vision-multimodal-2026` was created and its downloaded PDF reverified at exact approved SHA by successful workflow run `37955511006`. The distinct `EXCEPTION_RELEASED` record was committed on `main`. Normal Core v2 `FROZEN/RELEASED` lifecycle and formal Publication Preview approval are **not** claimed.
- This bypass solved the TS-003 publication operationally, **not** the generic Core defect, which remains OPEN.

Direct evidence:

- `sources/SP-vision-multimodal-2026/execution/defects/ts003-post-validation-editorial-revalidation-gap-20261010.md`;
- [Issue #560](https://github.com/eariver/japanese-generative-ai-survey/issues/560);
- `sources/SP-vision-multimodal-2026/publication/exception-20261010/freeze-manifest.json`;
- `sources/SP-vision-multimodal-2026/publication/exception-20261010/release-record.json`;
- [PR #561](https://github.com/eariver/japanese-generative-ai-survey/pull/561);
- [Release `special/vision-multimodal-2026`](https://github.com/eariver/japanese-generative-ai-survey/releases/tag/special/vision-multimodal-2026);
- [successful exact-byte publication workflow](https://github.com/eariver/japanese-generative-ai-survey/actions/runs/37955511006).

Required future Core direction:

- define a genuine, narrowly scoped `REVIEWED_EDITORIAL_CORRECTION` or equivalent reason for post-validation reader/source-fidelity corrections, distinct from `REVIEWED_CORE_CHANGE`;
- preserve the historical validation checkpoint and frozen upstream Architecture/Evidence/Selection/Draft/Human Architecture approvals while requiring new editorial decision/evidence provenance;
- rebuild and validate exact corrected manuscript, TeX/PDF, quality bundle, semantic/visual review and the State-bound append-only supersession record; reject stale candidate or SHA drift;
- continue the normal candidate → formally reviewed Human Publication Preview → Freeze → Release chain using the exact new PDF SHA;
- cover Weekly and Special, legitimate and illegitimate reasons, absence of Human review, forged/invalid provenance, repeated corrections, races/idempotency, and non-regression of the original post-Core-change path.

This item is specifically about **the missing lifecycle/legal reason and authority rebind**, not about the technical content defects already categorized under DM-006/015/020. Do not merge the TS-003 exception itself into Core v2 or mark this item `CORE_FIXED`.

---

## 6. Items intentionally not treated as current shared-Core defects

The following edition issues are closed because their edition-level acceptance criteria are satisfied:

- #500 — W36 temporal-boundary wording;
- #502 — W36 community citation target;
- #511 — W38 TypeSafe/Jev temporal authority;
- #512 — W38 full community-ledger auditability.

Issue #551 is closed at the edition level after W39 r6 approval/release, but its newly identified **generic** claim-to-source semantic-fidelity gap is retained above as CV2-DM-020.

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
| `SP-efficient-llm-2026` | Evidence-review update in r0.3 | DM-016, DM-017 | Source-class projection workaround validated; Completeness builder/validator obligation mismatch also exposed and handled edition-locally; shared Core remains frozen. |
| `SP-efficient-llm-2026` | Publication Preview r2 repair update in r0.4 | DM-018 | Issue #520 gross Overfull/clipping PASS defect recorded as generic QA debt (edition fixed locally with overfull guard + full render); Issue #521 evaluated as EDITION_LOCAL, not added; shared Core implementation unchanged. |
| `SP-efficient-llm-2026` | Final release closure review in r0.5 | DM-019; DM-001/002/003/004 recurred | New divergent-slug release-identity defect (build_freeze vs profile public slug) recorded with edition-local identity correction; Freeze/Release recurrences documented; DM-016/017/018 unchanged; edition RELEASED/COMPLETE with exact Human-approved PDF; shared Core implementation unchanged. |
| `SP-beyond-text-2026` | Final release closure review in r0.6 | No new CV2-DM ID; DM-001/002/003/004/019 recurred; DM-006 materially updated | TS-002 Freeze/Release recurrences with edition-local compat (`ts002-freeze-compat-20260928.py`, recovery PR #549, runs 36333979769/36333984167); CV2-DM-006 latest reproduction + generic seed corpus `docs/editorial/ja-technical-terminology-overtranslation-seed.md` (#533/#539/#543 incorporated); edition RELEASED/COMPLETE with exact Human-approved 78pp PDF; shared Core implementation unchanged. |
| `2026-W39` | Final release closure review in r0.7 | **DM-020 new**; DM-001/002/003/004/006/013/014 recurred or materially updated | Issue #551 exposed generic claim-to-source semantic-fidelity/source-role weakness (new DM-020); Issue #501 terminology defect recurred across multiple preview rounds (DM-006); DolphinBench/Claude Code temporal identity issues extend DM-013; Freeze compat repeated DM-001/002/003; release run `36581201216` repeated DM-004 and recovery PR #557; final `execution/index.md` remains stale after recovery (DM-014). Edition RELEASED/COMPLETE with exact Human-approved 12pp PDF; shared Core implementation unchanged. |
| `SP-vision-multimodal-2026` | Exceptional release closure review in r0.8 | **DM-021 new**; DM-006/015/020 recurred | TS-003 post-`VALIDATED_DRAFT` editorial and source-fidelity repairs exposed an unsupported publication revalidation reason (`REVIEWED_CORE_CHANGE` only; #560). Human authorized one-off exception: exact approved 39pp PDF SHA `b2de8449…` Freeze-pinned and released with PR #561 and run `37955511006`; distinct exception records preserved, normal Production State remains `VALIDATED_DRAFT`. Prior reader Japanese, editorial process leak and citation semantic-fidelity failures documented in DM-006/015/020; shared Core unchanged. |

Next required update: the next Weekly/Special guarded stop or closure if it occurs first.

## 10. Revision History

| Revision | Date (JST) | Reviewed through | Change |
| --- | --- | --- | --- |
| `r0.1` | 2026-09-20 | `2026-W38` | Initial consolidated deferred-maintenance inventory. Backfilled W35-W38 defect records, post-freeze Issues, release recovery evidence, and relevant pre-freeze Publication Boundary carry-over. Established Core pause policy, stable CV2-DM IDs, per-edition update contract, restart contract, and tracker Issue #515. |
| `r0.2` | 2026-09-22 | `SP-efficient-llm-2026` guarded stop | Added CV2-DM-016 for the Evidence source-class map mismatch exposed by the Efficient LLM Thematic. Recorded deterministic edition-local compatibility as the production workaround while shared Core remains frozen. |
| `r0.3` | 2026-09-22 | `SP-efficient-llm-2026` Evidence review | Added CV2-DM-017 for the Completeness builder/validator obligation-materialization mismatch exposed when Discovery-added EFF-O13/O14/O15 reached the frozen Completeness stage. |
| `r0.4` | 2026-09-23 | `SP-efficient-llm-2026` Publication Preview r2 repair | Added CV2-DM-018 for Longform Publication QA passing gross Overfull hbox / rendered clipping (Issue #520, r1 ~70pt p.56 glossary overflow with VISUAL PASS). Recorded edition-local layout fix + overfull guard + full-66pp visual disposition; Issue #521 explicitly EDITION_LOCAL, not added. |
| `r0.5` | 2026-09-23 | `SP-efficient-llm-2026` final release closure | Added CV2-DM-019 for canonical Freeze builder deriving release identity from internal issue_id instead of the profile public slug (first divergent-slug LONGFORM_SPECIAL freeze; edition-local identity correction, workflow identity check passed). Recorded CV2-DM-001/002/003 Freeze recurrences and CV2-DM-004 Release recurrence (run 35863535480, recovery PR #524); DM-016/017/018 unchanged; edition RELEASED/COMPLETE. |
| `r0.6` | 2026-09-28 | `SP-beyond-text-2026` final release closure | No new CV2-DM ID. Refreshed DM-001/002/003/004/019 latest reproductions to `SP-beyond-text-2026` with TS-002 evidence (`ts002-freeze-core-defects-20260928.md`, `ts002-release-recovery-20260928.md`, runs 36333979769/36333984167, PRs #548/#549). Materially updated DM-006 (tracking #501+#534, TS-002 #533/#539/#543 evidence, new generic seed corpus path, forbidden-list insufficiency, expanded future scan directions, established-Japanese invariant). Edition RELEASED/COMPLETE; shared Core implementation unchanged. |
| `r0.7` | 2026-09-30 | `2026-W39` final release closure | Added CV2-DM-020 for claim-to-source semantic fidelity / source-role binding after Issue #551 (ART novelty, Cursor claim strength, Claude Code first-party binding, Opus conditionality, source-note role consistency). Refreshed DM-001/002/003 Freeze recurrences from `w39-freeze-compat-note-20260929.md`, DM-004 release recurrence (run `36581201216`, PR #557), DM-006 Weekly terminology recurrence (#501 + W39 supplements), DM-013 temporal/version/date recurrence (#551), and DM-014 stale execution index after recovery. W39 RELEASED/COMPLETE; shared Core implementation unchanged. |
| `r0.8` | 2026-10-10 | `SP-vision-multimodal-2026` exceptional final release | Added CV2-DM-021 for missing post-validated reader/editorial publication revalidation authority (Issue #560), documenting explicit Human-approved one-off exception Freeze + verified GitHub Release (PR #561; run `37955511006`) without changing formal Core v2 lifecycle. Refreshed DM-006 Japanese terminology, DM-015 internal editorial leakage, DM-020 claim-to-source source-fidelity recurrences. New edition-local defect note linked; existing statuses remain OPEN until consolidated Core maintenance. |

## 11. Reference authority

Primary evidence for the current inventory includes:

- frozen Production Line: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`;
- W39 closure-reviewed main: `239ef2703a93fa802f232978c7166d04d6cc3d49`;
- TS-003 exceptional-release-closure-reviewed main: `7c8e4b1ee913007e4d1e0dc627e2c0a7c2f5ff4f`;
- [Issue #560](https://github.com/eariver/japanese-generative-ai-survey/issues/560), exception manifest/Release record, PR #561, and workflow run `37955511006` for CV2-DM-021;
- [Issue #497](https://github.com/eariver/japanese-generative-ai-survey/issues/497);
- [Issue #501](https://github.com/eariver/japanese-generative-ai-survey/issues/501);
- [Issue #505](https://github.com/eariver/japanese-generative-ai-survey/issues/505);
- [Issue #506](https://github.com/eariver/japanese-generative-ai-survey/issues/506);
- [Issue #507](https://github.com/eariver/japanese-generative-ai-survey/issues/507);
- [Issue #508](https://github.com/eariver/japanese-generative-ai-survey/issues/508);
- [Issue #515](https://github.com/eariver/japanese-generative-ai-survey/issues/515);
- closed W39 [Issue #551](https://github.com/eariver/japanese-generative-ai-survey/issues/551) for CV2-DM-020 and DM-013 W39 evidence;
- closed edition Issues #500, #502, #511, #512 for deferred generic hardening;
- [Issue #434](https://github.com/eariver/japanese-generative-ai-survey/issues/434) as a pre-freeze carry-over;
- W35-W38 edition-local defect records under `sources/<edition>/execution/defects/`;
- release recovery PRs #504, #510, #514, #524, #549 and #557;
- TS-001 reissue edition-local defect records (`ts001-reissue-freeze-core-defects-20260923.md`, `ts001-reissue-release-recovery-20260923.md`) and compat helper (`execution/ts001-freeze-compat-20260923.py`);
- TS-002 edition-local defect records (`sources/SP-beyond-text-2026/execution/defects/ts002-freeze-core-defects-20260928.md`, `sources/SP-beyond-text-2026/execution/defects/ts002-release-recovery-20260928.md`) and compat helper (`sources/SP-beyond-text-2026/execution/ts002-freeze-compat-20260928.py`);
- W39 Freeze compatibility: `sources/2026-W39/execution/defects/w39-freeze-compat-note-20260929.md`;
- W39 Release workflow run `36581201216`, recovery PR #557, final `RELEASED / COMPLETE` state, and public tag `weekly/2026-W39`;
- W39 stale navigation reproduction: `sources/2026-W39/execution/index.md` versus canonical `sources/2026-W39/production-state.json`;
- generic terminology seed: `docs/editorial/ja-technical-terminology-overtranslation-seed.md` plus W39 additive supplements (CV2-DM-006 authority seeds; no auto-rewrite);
- historical feedback authority: `docs/survey-production-core-v2-production-feedback-backlog.md`.

When a later revision updates an item, cite the newest direct reproduction evidence while retaining the earlier history above.
