# Astra DM-021 applicability disposition

2026-10-10. Human explicitly authorized checking the new DM-021 during current work. Read [captured Summary DM-021, lines690–727](evidence-20261009T171707Z/deferred-maintenance-summary.md) and [General intake](evidence-20261009T171707Z/intake-and-impact.md). New capture commit **afdb3df3faa20af3bb5798be429bba8dbd2100b1**, blob **62ee6a6b9792cc96e42f378c5cff67faebaeef43**, SHA256 **7c84b6d8e805cfadf5f10ac0ba587d278fd808461d305231906dcbf79f0c9a51**. This is later evidence, not baseline/code adoption or standing refresh permission. Previous d6381568 capture remains intact; fixed baseline774 remains.

## Decision

**Proceed with the selected LF-2I initial-publication contract4795a586 + F1–F3.** Incorporate DM-021 as an explicit unsupported post-validation editorial-correction operation and a separate future lifecycle/authority disposition. Do not implement a new reason taxonomy/supersession engine in this unit.

Rationale is the selected scope and actual authority boundary, not Production's maintenance scheduling: LF-2I implements initial reviewed source creation and read-only replay of healthy later authorities. It does not authorize post-VALIDATED_DRAFT changed-reader/editorial regeneration or falsely label such corrections `REVIEWED_CORE_CHANGE`. A future reconstruction decision may select DM-021 repair on its merits; the Summary's consolidated-batch policy is not architecture authority over this workspace.

Root source check at fixed409+LF1 confirms the narrow code condition independently of the new Production report: `survey_agent_control_v2.py:45,1789–1790` accepts only `REVIEWED_CORE_CHANGE`, and `publication-surface-revalidation.schema.json:26` has that const. This is static source corroboration, not a new runtime reproduction of TS-003.

## Binding LF-2I consequences

1. Do not add `REVIEWED_EDITORIAL_CORRECTION`, reinterpret the existing reason, rewrite immutable validation checkpoints, bypass current authority or waive changed PDF/source/review hashes. Contract change/tamper negatives must continue to fail closed.
2. Healthy FROZEN/RELEASED fixtures must use the existing **normal** typed approval/checkpoint/Freeze/Release chain. The reported edition-specific `EXCEPTION_FROZEN`/`EXCEPTION_RELEASED` records are not fixture shortcuts or reusable Core authority; no such records are being imported or read.
3. Existing valid revalidation pointers remain subject to current validators; their mere existence does not authorize editorial-correction renewal. If a required LF-2I operation actually intersects the missing-reason gap, General returns its exact raw/source blocker before changing scope. The no-later-state-fixture stop remains mandatory.
4. Record the limitation in LF-2I acceptance/closeout and the next lifecycle/regeneration planning entry. No new production semantic/visual PASS or `CORE_FIXED` claim follows from this intake.

## Acquisition / claim limits

Exactly two reported `gh` API calls resolved main and fetched the named document at that commit; full API responses are saved. The first shell script's decoder was a no-op and its run failed when decoded output was absent; v2 decoded the existing response without another network call. Both scripts/results are preserved as exact-run evidence, not certified rerun tools. The commit-API response is saved in full (the endpoint can include file patch metadata); it is not a new code baseline or authorization to follow linked records.

Issue560, PR561, workflow37955511006 and edition defect/exception artifacts are referenced only by the captured Summary; primary evidence was not separately acquired. `OPEN_CORE / EDITION_WORKAROUND`, exact TS-003 PDF/exception history and production outcome remain **reported secondary evidence**. This adds a scoped21st disposition, not a new all21-item maintenance/intake batch.
