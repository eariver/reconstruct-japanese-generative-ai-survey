# LF-1 — source-only Longform reader-input component

2026-10-09 bounded completion, **Human Commit Point**. Start reconstruct1610777; whole candidate NOT_READY, step4/B3 OPEN, canonical audit unstarted. Read [Astra assessment / exact identity / next task](../../outputs/rephase-1-longform-lf1-assessment.md) first.

## Current evidence (mandatory)

Final directory: **`evidence-20261009T022000Z-correction-R2/`**.

- [Implementation report](evidence-20261009T022000Z-correction-R2/implementation-report.md), [final source hashes](evidence-20261009T022000Z-correction-R2/overlay-sha256.txt), [portable overlay patch](evidence-20261009T022000Z-correction-R2/overlay.patch).
- [31-method raw run](evidence-20261009T022000Z-correction-R2/run-full-module.log), [exact-run Python runner](evidence-20261009T022000Z-correction-R2/run_evidence.py), [fresh apply verification](evidence-20261009T022000Z-correction-R2/verify-apply.log).
- [Independent final resolution](evidence-20261009T022000Z-correction-R2/independent-final-resolution.md), **mandatory [evidence qualification](evidence-20261009T022000Z-correction-R2/evidence-qualification.md)** and [independent evidence supplement](evidence-20261009T022000Z-correction-R2/independent-evidence-supplement.md).
- [v2 post-drift direct capture](evidence-20261009T022000Z-correction-R2/proof-postdrift-v2/capture.log) supersedes the first numeric-exit narrative. First proof transcript was overwritten/lost, not restored by the new proof.

## Composite identity — not a new commit

Base HEAD409b292756dd1277b9dfae87679934c0d2ce251c/tree8ce3699861505f32d1d60bdc185d4d4f635aedb2 PLUS exactly three untracked files:

| Path | SHA256 |
|---|---|
| `scripts/survey_longform_derivation_v2.py` | `233e86557f1627203a4f1e4129c953bf34e1319bd8949b1d58b7d417b0744cf7` |
| `schemas/longform-reader-input-v2.schema.json` | `7bae9d2ac753c83521165c76c9e461ce40ac4e704d9b44d3518ae7b88fbd0643` |
| `tests/test_survey_longform_derivation_v2.py` | `ce687447539a99eb92532bc34246a271fb489b259e63b31ed6699fcc12fbf913` |

Patch SHA256 `253e284b08a209f855d06fd2154a3f34c49315f4014118d98fc54b49c3eae881`.
Live copy `/tmp/opencode/jgas-lf1-design-20261009T001653Z`; fresh apply copy `/tmp/opencode/jgas-lf1-verify-20261009T023000Z`. Original409 remains clean; HEAD alone does not include LF-1. Recover exact409 via its existing four verified inputs if necessary, then independently apply this patch with fresh absent-path/hash/identity/object-separation checks. PartialDB/history/runtime limitations persist; no completed recovery rerun now.

## Preserved history / attribution

1. [Task](task.md), General `evidence-20261009T001653Z/design-proposal.md`, [Astra feedback](astra-design-feedback.md), correction/qualification in that directory.
2. [Independent design gate](independent-design-gate-review.md), [Astra implementation selection](astra-implementation-selection.md): source-only route with legacy directive presence refusal; no invented authority or LF-2 integration.
3. `evidence-20261009T003443Z/`: original implementation20 + regression5 claims, initial failures and print-only runner; preserved, not final evidence.
4. [Astra R1 review](astra-implementation-review-r1.md), different General `evidence-20261009T014500Z-correction-R1R6/`, its [independent CHANGES_REQUIRED](evidence-20261009T014500Z-correction-R1R6/independent-implementation-review.md). Nine final-hash methods there were insufficient; runner postguard PASS overclaim later retracted.
5. [Astra R2 review](astra-implementation-review-r2.md), final directory above:31 successes once on CPython3.14.4, corrected archive/source/schema/guard/oracle boundaries and independent bounded resolutions.

Astra is author-side architecture/source/evidence reviewer; two General implementation workers authored code/tests; a separate reviewer supplied independent scoped judgments. Synthetic stage/Human records are type/identity evidence only. No canonical audit/adoption/whole-profile PASS. No committed-head acceptance or old-runtime/test-count transfer.

Next LF-2 is design-first initial publisher/review/receipt/Gate integration proposal over this exact composite identity; directive authority remains unresolved beyond LF-1's explicit refusal subset. Preserve reader/nonreader separation and existing review roles. Stop here; no automatic LF-2, commit, Push, Summary refresh or old-script execution.
