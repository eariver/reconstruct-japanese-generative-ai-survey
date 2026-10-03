# Fixed-baseline candidate recovery — completed bounded unit

Read [Astra assessment/current next task](../../outputs/rephase-1-candidate-recovery-assessment.md). **Recovery complete at b40de60; stop at Human Commit Point before Freeze implementation.** Whole candidate NOT_READY, step 4/B3 OPEN, seven-point audit unstarted.

## Current exact inputs

- Candidate `b40de600e9ed1f80cb278213ccf17aa5f3cd9de3`, tree `657032438c6ed8b1c055d5a120b67b4b261a5092`, direct parent fixed Production `774dd39a951c9ac3818e83dfffd4c7666efb0a20`. Tree equals historical 481; original history/old PASS is not restored.
- Live original `/tmp/opencode/jgas-rephase-candidate-recovery-20261003T0435Z`; independently restored `/tmp/opencode/jgas-recovery-restore-20261003T0445Z`; branch `codex/rephase-candidate-recovery`, inert origin.
- [Final recovery manifest](m3-20261003T0445Z/corrections-20261003T0456Z/recovery-manifest.json) **plus** [final machine-generated 32+9 identity binding](m3-20261003T0445Z/corrections2-identity-20261003T0944Z/final-identity-binding.json). The older m2/m3-pretty findings-test blob has a disclosed single-hex typo; do not use it as final identity authority.
- [Portable archive](m3-20261003T0445Z/candidate-partial-b40de60.tar.gz): 5,152,199 bytes, SHA256 `faf6792faf37ad30af2dbd7203b8896ca00964a91d00623a4f01278f2ade9f3c`; actual partial DB + 686 materialized files, not all-history/all-assets/venv backup. Offline restored identity/inventories + current-source positive verified.

## Evidence navigation

1. [Task](task.md), [General preflight](preflight.md), [Astra method](method-decision.md), [verification selection](verification-decision.md).
2. `m2-20261003T0435Z/`: exact fixed-SHA acquisition, four patch applications, new commit/full tree equality, runtime/imports; initial bad import probe preserved.
3. `m3-20261003T0445Z/`: five fresh methods all successful (stage/CLI each has three subcases in one method), actual recovered-DB current closure positive/exact-drift negative, archive/census/offline restoration. Tests are suite-bound, not per-method HEAD-header proof. Stage fixtures use recovered Git; direct-primary CLI does not exercise the unselected Weekly Git helper.
4. **Mandatory corrections:** [scope/guards/unsafe-harness/evidence-loss supplement](m3-20261003T0445Z/corrections-20261003T0456Z/corrections.md), then [identity-table correction](m3-20261003T0445Z/corrections2-identity-20261003T0944Z/correction.md). Original claims and initial failures are not silently rewritten.
5. [Initial independent CHANGES_REQUIRED](independent-recovery-review.md), [documentary resolution](independent-recovery-resolution.md), [all-41 identity resolution](independent-identity-resolution.md). The latter qualifies the reviewer's initial full-blob-check overclaim. Final recovery-only BOUNDED_PASS, not Freeze implementation/full application approval.

## Recovery and next action

Saved `restore.sh`, `run_five.py`, `run_closure.py` and other harnesses are **historical evidence: DO NOT RERUN**. Some overwrite output paths; restore wrapper masks failures. The valid archive was established by final-content checks after manual recovery, not wrapper exit. If needed later, use a newly reviewed no-overwrite extraction with archive hash/member checks and exact identity/object/byte verification. Do not hydrate missing blobs or change source just to make recovery look complete.

Next unit after Human continuation: General DM-001/019 joint implementation, beginning with concrete shared-helper/writer-preflight/test-fixture design for Astra review; preserve b40de60 in an independent DB. Source/runtime recovery is complete and need not be repeated. Reuse the Summary capture; no current-main/Production mutation or Summary refresh. Human owns reconstruct Commit/Push.
