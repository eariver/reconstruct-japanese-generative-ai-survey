# reconstruct-japanese-generative-ai-survey

External architecture review and reconstruction workspace for `eariver/japanese-generative-ai-survey`. Production remains read-only until the Human explicitly authorizes a change.

## Re:Phase 1 — start here

**The r2 proposal, bounded independent review and Git-free helper unit regression are complete.** Continue in this repository and treat prior Phases as historical evidence. The old Phase 5 work order is superseded.

1. [Re:Phase 1 handoff](handoff/rephase-1-continuation.md)
2. [Current unit-runtime assessment](outputs/rephase-1-runtime-assessment.md); [independent-review disposition](outputs/rephase-1-review-disposition.md)
3. [Runtime evidence](notes/rephase-1-runtime/README.md) and [r2 candidate/review evidence](notes/rephase-1-connection/README.md), only as needed; [prior design](outputs/rephase-1-operating-contract-assessment.md) remains historical context

Baselines:

- historical reconstruct starting point: `ec6a502e9ae37e956d677f96f29af6c4e4591fc4`
- Human-fixed production baseline: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`

Do not follow newer production main or rebaseline without explicit Human instruction. **Git operations are currently prohibited**, including read-only inspection and Git-aware tests.

The [broader direction](outputs/rephase-1-direction-assessment.md) remains partial redesign that removes identifiable work while preserving quality, authority and history. The [five-file r2 candidate](notes/rephase-1-connection/candidate.patch) removes copied live status and its maintenance obligation, with caller/test and edited-rule review completed at root. It repairs navigation and scope wording while retaining mandatory reading and review. Five grouped r2 checks include four executed document-only upstream tests; one authorized independent review found no actionable issues in scope and r2 was retained unchanged. The five existing execution-record unit tests now pass against r2 in an isolated copy with their original Profile/State loader mocks. Full Core/CLI/bridge integration remains unperformed.

The separation proposal is complete through bounded independent review and the existing helper unit regression. Remaining adoption conditions are integration checks in a permitted environment and a separate production decision. This review is not final audit or adoption approval; its one-agent authorization is completed. Do not repeat completed work without new evidence. Known Freeze/reader defects remain maintenance evidence, not an automatic roadmap.

## Purpose

Produce high-quality Weekly and Special editions with substantially less total lifecycle work: production, research, supervisory reasoning and independent review, repair, CI/runtime, LLM usage, maintenance/migration and Human effort. Moving work between roles is not saving. Current Core and role assignments may be reconsidered; their existing guarantees must be accounted for.

No architecture adoption, full current-production quality certification or net saving has been established. W33/W34/SP001 saved States are RELEASED; this is not a new full-chain or PDF quality validation.

## Historical archive

Prior `outputs/`, `notes/`, `handoff/`, `instructions/` and `brief/` remain at their original paths for provenance and reproducibility. Archive is logical: no historical files were moved or rewritten. Their old current/next/Phase instructions are historical and do not govern new work.

The [last Phase 5 assessment](outputs/astra-phase-5-upstream-reconciliation-assessment.md) and [old handoff](handoff/astra-phase-5-continuation.md) retain the prior disposition and limits. Consult a historical result only when it has information value for the current decision. The pre-reset repository, including its old entry documents, remains available at `ec6a502e`.

The Human handles ordinary Git Pull/Push and final commit. No Git operations are authorized in the current continuation. Production posting, application and adoption require separate explicit authorization.
