# DM-003 witness/disposition — omitted checkpoint and split Preview authority

**Successor update 2026-10-05:** localDM003-W1 is now bounded repaired at e1705b7 by the [shared-State agreement unit](rephase-1-dm003-w1-assessment.md),24 selected methods and separate qualified implementation/evidence review. Original222 witness and initial OPEN disposition below remain historical; no generic omitted-checkpoint repair or upstream CORE_FIXED follows. Current next unit is DM-004 command/validation contract after the new Human Commit Point, not a repeat witness.

Recorded **2026-10-04T05:35:00+09:00** (Astra clock). Started at clean Human reconstruct commit **1bb42dd01774bf30bc6f4a09cff43b9a321d531b** after Push/continuation, no fetch. **Witness/disposition unit complete; no shipping code change. Stop at this Human Commit Point.** Candidate remains **222a37e9ee2aa96724a491f2c04c2583a86b9650**, tree **dbabeed5e70d79b51abb09b64666ca9e1d0fd5dd**. Whole candidate **NOT_READY**, step4/B3 OPEN, canonical seven-point audit unstarted.

## Decision in brief

1. **The omitted named pointer is not a blocker for the tested current Freeze route.** At222, typed Preview approval supplies the exact Candidate. A consumed `VALIDATED_DRAFT→RELEASE_CANDIDATE` checkpoint need not be rediscovered after the transition. Do not introduce generic filesystem scanning, an extra checkpoint name or automatic map expansion to solve this selected route.
2. **A separate narrow consistency gap is demonstrated before Freeze writes.** With canonical checkpoint-side approval A1 and a different standalone-valid Human-side approval A2 for the same Candidate, `validate_agent_state` returns no errors and `build_profiled_freeze` writes a Freeze/Manifest bound to A2. Stage admission then rejects the disagreement. This is a real pre-write validation gap, not a successful FROZEN/publication bypass.
3. **Next bounded unit:** repair approved Preview reference agreement in the shared State validation boundary, with actual wrapper no-write regression. This is selected from measured behavior, not a generic DM-003 resolver or a twenty-item backlog batch. No repair has begun in this unit.

## 1. Source contract and phase distinction

[Task](../notes/rephase-1-dm003-witness/task.md), [General proposal](../notes/rephase-1-dm003-witness/source-and-cases.md), [Astra execution selection](../notes/rephase-1-dm003-witness/execution-decision.md). The later Summary at saved d6381568 is secondary evidence only; no new production/main/Issue/primary-record intake was performed. Baseline remains **774dd39a951c9ac3818e83dfffd4c7666efb0a20**.

Root inspected the actual222 controller/stage code:

- Config `VALIDATED_DRAFT` has `checkpoints: []`. `build_stage_checkpoint` writes the canonical `orchestration/v2/checkpoints/VALIDATED_DRAFT.json`; `advance_with_checkpoint` validates it and advances the lifecycle but its empty checkpoint loop adds no named provenance pointer.
- The existing named **`validation`** pointer refers to **`DRAFT_COMPLETE.json`**, a different producer/role. It is not missing and was not deleted in the positive witness.
- The unmapped checkpoint **does have authority when the transition consumes it**. Later `_prior_artifacts` iterates State-bound named pointers; the typed Preview approval supplies the Candidate through `_publication_approval_artifacts`. This is a phase distinction, not “files have no authority at any time”.
- The State-updating `approve_publication_preview` reads the canonical Candidate and normally writes matching Human/checkpoint Preview refs. The lower-level `publication.build_preview_approval` can also create a typed record; calling the controller the sole producer would be inaccurate.
- `validate_stage` validates State, then current-artifact cardinality, then prior artifacts and their merge. A surplus current `publication-candidate` at RELEASE_CANDIDATE is rejected as an **extra key**, before the merge helper; a merge-conflict message is not the public-entry oracle for that case.

This preserves typed authority and avoids inferring active authority from directory membership. Broad historical/provenance completeness is not established by this witness and is not declared upstream CORE_FIXED.

## 2. Execution and evidence binding

General authored and ran external harnesses in an independent byte-copy at `/tmp/opencode/jgas-dm003-witness-20261003T200937Z`, same exact222 HEAD/tree/parent, inherited inert origin, no alternates/hardlinked object store. Original implementation/restored DBs were read-only inputs and remain clean. Root independently re-read witness and source identities/status; no fixture objects were created in reconstruct's DB.

The new harnesses use pinned Python3.12.14, offline Git settings, real publication/State/stage validators and the existing **single Thematic LONGFORM_SPECIAL** fixture. Upstream records, reviews, PDF and Human decisions are explicitly synthetic. No authority/Git-success mocks, shipping source edits, candidate/ref commits, live Actions/Release or recovery rerun.

Fresh asserted HEAD/tree/parent/tracked-clean and five source hashes bracket each scenario. These checks bind source identity, not untracked fixture mutations; the corrected scenarios separately inventory regular files under their two fixture roots. Inventories record hashes and exact added/modified/removed sets; selected authority/artifact bytes are saved as `.bin` plus metadata. This is not a complete standalone backup of every fixture input or a whole-filesystem/continuous attestation. Witness-owned fixtures were cleaned only after evidence capture. Original shipping222/portable recovery materials are unchanged.

## 3. Initial evidence, review and targeted corrections

The [initial report](../notes/rephase-1-dm003-witness/dm003-witness-20261003T200937Z/REPORT.md) maps seven scenarios and **86 recorded harness operations**, not86 test methods. It demonstrates normal omitted-map admission, absent/corrupt unreferenced sibling tolerance, stale Candidate rejection, split-ref stage rejection and distinct-path rival behavior. Its stronger claims were rejected by Astra and the [independent initial review](../notes/rephase-1-dm003-witness/independent-witness-review.md):

- “Byte-distinct same-PDF rival is structurally impossible” generalized from a failed fixture attempt. A new valid bundle/review/Candidate can use the same canonical source/manuscript/PDF without changing active C1 pins.
- C1/C6 immediate self-comparisons did not prove before/after stability; C2/C3 did not have the claimed full write-window snapshots. Their successful operations remain narrower observations.
- Original C7's hash-only winner check could not distinguish two same-byte Candidate paths.
- Original C5 built Freeze **before** splitting refs, then tested stage only. It could not establish wrapper rejection before writes or justify “not a defect”.

The [Astra correction decision](../notes/rephase-1-dm003-witness/correction-decision.md) selected only three meaningful follow-ups. [Supplement report](../notes/rephase-1-dm003-witness/dm003-supplement-20261003T202828Z/REPORT.md) and [manifest](../notes/rephase-1-dm003-witness/dm003-supplement-20261003T202828Z/evidence/supplement-manifest.json) record **46 operations across S1/S2/S3**, not46 methods and not an extra whole-suite PASS.

| Scenario | Corrected actual result |
|---|---|
| **S1 genuine rival + orphan** | C2 independently validates, has distinct path **and bytes/hash**, same PDF as C1; exactly four new bundle/review/Candidate files, active named pins untouched. Direct Freeze(C2,A1) refuses exact binding; stage surplus key refuses before merge. Unmapped checkpoint retargeted to C2 is schema-valid but transition/report-inconsistent; real wrapper/stage still select **C1 path+hash**. `_prior_artifacts` selection, Freeze record and exact operation write windows corroborate it. |
| **S2 missing sibling** | Canonical transition consumes the checkpoint, then the witness deletes only that unmapped sibling before approval. Exact windows: removal `{−sibling}`; approval `{+approval, ~State}`; wrapper `{+Freeze,+Manifest}`; stage `{+report}`. Other inventoried bytes unchanged; sibling not recreated. This is the central snapshot-backed no-selected-path-blocker result. |
| **S3 split refs** | Fresh outputs absent; A1/A2 individually valid and distinct, both approve the same C1. Human ref changed to alternate A2, checkpoint ref remains canonical A1. State validator returns `[]`; actual wrapper **BUILT** exactly two files bound to A2, State unchanged. Stage then raises `Human Preview and checkpoint approval authorities disagree`, no stage report. This is a characterized **defect finding**, not a successful fail-closed test. |

S1's attempted setup first failed because its reference snapshot was captured before approval, which legitimately modifies State; first traceback is preserved and corrected S1-R2 is explicit. Initial v1 failures/guard refusals, one unintended C1–C5 rerun and removed witness bytecode cache are disclosed; old evidence/harness and narrower claims remain. Do not describe the session as clean-first-run or treat the unintended rerun as extra coverage.

## 4. Local finding DM003-W1 — Preview reference agreement before Freeze

This is a **local Re:Phase finding identifier**, not a new Production CV2-DM ID, Issue, upstream status transition or claim that the recorded production editions have this defect.

**Source:** `survey_agent_control_v2._validate_agent_state` lines403–416 validates the canonical `checkpoint_provenance.publication_preview` approval and hash but does not compare the Human-side Preview ref. The profiled wrapper `_safe_state_profile` trusts that State validation and later loads the **Human-side** ref (`survey_profiled_freeze_v2.py:59–62`). The stage resolver alone compares the two (`survey_stage_validation_v2.py:138–139`).

**Measured effects:** [S3 wrapper outcome](../notes/rephase-1-dm003-witness/dm003-supplement-20261003T202828Z/evidence/S3/s3-wrapper-outcome.json) records alternate approval path `sources/SP-DM003-S3/gates/publication-preview-approval-rival.json`, SHA256 `2567643b62dde94f74d5600e7589dab2dace9e6e1727c83a79acf3ec9375e935`. It freezes the original C1 (`7bf983b2e3830a74d55b45a4c6bc17b74b3fdcda739342fbc36103e2dc8e92af`). [File diff](../notes/rephase-1-dm003-witness/dm003-supplement-20261003T202828Z/evidence/S3/s3-wrapper-window.diff.json) contains only the two added output files; saved State hashes/bytes are stable across the wrapper. [Stage traceback](../notes/rephase-1-dm003-witness/dm003-supplement-20261003T202828Z/evidence/S3/s3-stage.traceback.txt) shows the real equality guard rejecting the split.

**Impact boundary:** approval identity/provenance divergence at the writer; same-Candidate bytes in this witness. No candidate-divergent split admission, no successful FROZEN transition, no bypass of the stage backstop, no real Human/publication impact demonstrated. Normal `approve_publication_preview` writes both refs together; the split was deliberately introduced to test fail-close behavior. Nonetheless the writer can leave artifacts that the required next stage refuses, contradicting a clean pre-write consistency boundary and creating avoidable repair work.

The prior DM-001/019 bounded result at222 remains historical evidence for its tested contract, **qualified by this newly demonstrated related gap**. Do not transfer that PASS into a claim that arbitrary State/provenance corruption is already rejected before Freeze. No changes or re-tests of the former implementation were made to hide this finding.

## 5. Review disposition and next unit

The [independent resolution](../notes/rephase-1-dm003-witness/independent-witness-resolution.md) read the corrected harness/source, guards, inventories, saved artifacts and precise errors; it returned **BOUNDED_PASS for witness/disposition only**. It was file-based independent review, not a second execution/live-DB audit. Astra read the actual controller/stage/wrapper, corrected harness/write-window raw and S3 output/traceback, and checked shipping/witness identities. The initial CHANGES_REQUIRED and all corrections remain preserved.

**Astra disposition:** DM-003 omitted-pointer behavior does not justify a generic checkpoint discovery repair for the selected typed-approval route. **DM003-W1 is OPEN and warrants a narrow next implementation unit.** Stage rejection must remain; the new guard should reject the inconsistent State before the wrapper writes anything.

### Next General task after Human continuation

Start at fixed222 in a new independent copy, preserve shipping/restored/portable evidence. Before code, return the smallest shared-State condition/callsite/test plan (short internal milestone, not another broad inventory): for **approved** Publication Preview, Human and checkpoint refs must agree on the exact canonical typed approval path/hash, with existing machine status and approval validation intact. Prefer the existing `_validate_agent_state` boundary so `_safe_state_profile` and other State consumers inherit one invariant; avoid parallel competing wrapper-only authority or a generic provenance subsystem. Keep the stage equality backstop. Pending/inert authority behavior and downstream FROZEN compatibility must be explicitly preserved or source-groundedly scoped.

Initial runtime allowance: `scripts/survey_agent_control_v2.py` plus a focused regression test module/necessary existing fixture use. No schema/config/new checkpoint names or filesystem scanning; expand paths only for a demonstrated caller need reviewed by Astra. Reuse S3 as parent defect, then prove strict State and actual wrapper rejection **before outputs** with unchanged pre-call State/authority bytes, healthy approved control, stale/missing/disagreeing refs, and relevant pending/Freeze-stage regressions. Do not merely assert an error in the later stage or reword a builder success into PASS. General implements/tests, Astra reviews diff/raw, fresh independent implementation reviewer follows. Fresh exact-head evidence and portable successor binding required; old56 is not automatically transferred.

No repair is implemented now. **Stop at this Human Commit Point**; ordinary reconstruct Commit/Pull/Push remains Human-owned. DM-004, Special/support/DM-016/017, build transfer, semantic/rendered acceptance, application readiness and final audit retain separate dispositions. No Summary refetch, old-suite decoration or automatic next-unit execution.
