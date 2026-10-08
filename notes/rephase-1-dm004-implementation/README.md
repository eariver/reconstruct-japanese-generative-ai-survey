# DM-004 — bounded CLI/Release closure repair complete

[Astra assessment/current next unit](../../outputs/rephase-1-dm004-assessment.md) controls scope. **Final409b292: local DM-004 bounded repaired; stop at Human Commit Point.** Whole candidate NOT_READY, step4/B3 OPEN, canonical seven-point audit unstarted; no upstream CORE_FIXED or Production adoption.

## Current identity and result

- HEAD **409b292756dd1277b9dfae87679934c0d2ce251c**, tree **8ce3699861505f32d1d60bdc185d4d4f635aedb2**, direct parent34f934e; seven unit commits on fixed parent e1705b7.
- Implementation `/tmp/opencode/jgas-dm004-impl-20261004T234416Z`, branch `codex/dm004-release-validate-state`; independent restore `/tmp/opencode/jgas-dm004final-restore-20261007T131353Z/candidate-partial-b40de60`, branch `dm004final`, actual finalHEAD and clean.
- Two paths only: agent-controller CLI +23 lines and new514-line behavioral test module. Workflow YAML unchanged. `validate-state` is read-only, invokes shared agent-State validation, returns0/JSON for valid State and2/stderr for controlled invalid inputs, resolves repo-local path before load. No RELEASED-only CLI policy.
- **Final7 behavioral +14 existing =21 successful methods**, no skips;18 internal new subcase executions are not extra methods. New acceptance uses real validators and actual extracted local closure block; existing checkpoint tests retain mock-based unit scope. No live Release/Actions/PR/network.

## Decisions, attempts and reviews

1. [General analysis](contract-analysis.md) → mandatory [Astra implementation task](implementation-task.md) (corrects generic-State/legacy CLI/mocked fixture assumptions).
2. `evidence-20261004T234535Z/`: original parent invalid-choice witness, implementation attempts,6ffed32 evidence and first failures. [Initial independent CHANGES_REQUIRED](independent-implementation-review.md).
3. [Astra correction task](correction-task.md) → `evidence-20261007T125126Z/`: containment, real full-block/no-write/discriminative oracles and strict saved v2 runner; [correction resolution](independent-correction-resolution.md) qualifies earlier reviewer no-write/whole-block overclaims.
4. **Final packet `evidence-20261007T131353Z/`:** [machine manifest](evidence-20261007T131353Z/final-manifest.json), [test-only closeout supplement](evidence-20261007T131353Z/closeout-supplement.md), [qualification](evidence-20261007T131353Z/evidence-qualification.md), `run-01-final-newmod/` and `run-02-final-affected/` with persisted pre/post guards/raw streams/exits, source copies/patch/pack/restore records. Removed source-grep rationale test; fail-fast uses unmodified extracted line with actual STATE environment expansion.
5. [Independent final resolution](independent-final-resolution.md): final source/evidence BOUNDED_PASS; earlier6+14/8+14 remain their own results, not automatically transferred.

## Portable inputs

Existing b40 archive (5,152,199B, SHA256 `faf6792faf37ad30af2dbd7203b8896ca00964a91d00623a4f01278f2ade9f3c`) + DM001/01920pack (46,164B, `2c2a8e6f2ab5fbd71b6cddfe5d875e4a821d09ef54ba9714eaab12e438e81a99`) + W1sevenpack (57,856B, `97d384fe8f7216f110cd401d1279129da83fab2000f28c24a73abe0b177b0fd9`) + [DM004 final pack](evidence-20261007T131353Z/dm004final-e1705b7-to-409b292.pack) (**48,240B**, SHA256 **`e3d941653eadf2459a13f1b85b9fbbffd819f0a0ad6bb77eb121b2cba02279bf`**;32 objects,7 commits/16 trees/9 blobs).

All4 hash-gated offline restoration verified actual finalHEAD/tree/clean available chain to shallow774, both paths' modes/blobs/bytes and zero shared object inodes. Saved script/logs are exact-run evidence, not a general certified rerun API. Use new absent targets and fresh checks if needed; never patch-rebuild a falsely labelled commit. Missing26,309 inherited blobs and unbundled runtime remain. Older guard/restore evidence gaps are not retroactively repaired.

Next after Human continuation: **LONGFORM_SPECIAL direct-source/supporting-surface contract/acceptance proposal at409**, analysis before code. No generic maintenance batch, new review-role consolidation, Summary refresh or real publication. Human owns ordinary reconstruct Commit/Push.
