# reconstruct-japanese-generative-ai-survey

External architecture review and reconstruction workspace for `eariver/japanese-generative-ai-survey`. Production remains read-only until the Human explicitly authorizes a change.

## Re:Phase 1 — start here

**B3 boundary design and function experiment are complete; B3 implementation remains open; whole-candidate readiness is NOT_READY.** Candidate f1 and production remain unchanged. The experiment rejects a full-render-input review format because it binds reader judgment to internal metadata changes. Canonical final seven-point audit has not started. Prior Phases remain historical evidence.

1. [Re:Phase 1 handoff](handoff/rephase-1-continuation.md)
2. [Current reader boundary assessment](outputs/rephase-1-reader-boundary-assessment.md)
3. [B3 implementation contract](notes/rephase-1-reader/contract-decision.md) and [design evidence/reviews](notes/rephase-1-reader/README.md), only as needed; [Freeze repair](outputs/rephase-1-freeze-assessment.md) and [prior application assessment](outputs/rephase-1-application-assessment.md) retain their original scope

Baselines:

- historical reconstruct starting point: `ec6a502e9ae37e956d677f96f29af6c4e4591fc4`
- Human-fixed production baseline: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`

Do not follow newer production main or rebaseline without explicit Human instruction. **Necessary Git operations and Git-aware tests are now authorized.** Use independent fixture repositories; production changes/adoption remain separately unauthorized.

The [broader direction](outputs/rephase-1-direction-assessment.md) remains partial redesign that removes identifiable work while preserving quality, authority and history. The [five-file r2 candidate](notes/rephase-1-connection/candidate.patch) removes copied live status and its maintenance obligation while retaining substantive reading/review. Its bytes remain unchanged after one bounded independent review and integration.

Application candidate a1 is `d38f023ce200619f7f49ce17a348755f05e0e021`, with the authentic fixed production parent in an independent sparse Git repository. Local Python 3.12 compile/JSON checks passed; three sparse-asset-blocked tests passed after exact input hydration. The broad unittest diagnostic is incomplete and is not full CI PASS. See the evidence for initial failures, skips and scope. Earlier synthetic integration results are retained separately.

The B1/B2 successor f1 is `bf32edf98ba8f605169d7188bbc764de74ee4f6e`, parent a1. Its 24 targeted tests passed; separate before witnesses failed at the identified baseline defects. The independent review is scoped to this repair. The next adoption prerequisite is B3 reader coverage/derivation, not another run of successful Freeze tests. Do not transplant old repairs. Full CI/Actions/publication, final seven-point audit, adoption and net savings remain unestablished.

## Purpose

Produce high-quality Weekly and Special editions with substantially less total lifecycle work: production, research, supervisory reasoning and independent review, repair, CI/runtime, LLM usage, maintenance/migration and Human effort. Moving work between roles is not saving. Current Core and role assignments may be reconsidered; their existing guarantees must be accounted for.

No architecture adoption, full current-production quality certification or net saving has been established. W33/W34/SP001 saved States are RELEASED; this is not a new full-chain or PDF quality validation.

## Historical archive

Prior `outputs/`, `notes/`, `handoff/`, `instructions/` and `brief/` remain at their original paths for provenance and reproducibility. Archive is logical: no historical files were moved or rewritten. Their old current/next/Phase instructions are historical and do not govern new work.

The [last Phase 5 assessment](outputs/astra-phase-5-upstream-reconciliation-assessment.md) and [old handoff](handoff/astra-phase-5-continuation.md) retain the prior disposition and limits. Consult a historical result only when it has information value for the current decision. The pre-reset repository, including its old entry documents, remains available at `ec6a502e`.

The Human handles ordinary Git Pull/Push and final commit. Necessary Git operations and independent Git-aware fixtures are authorized. Production posting, application and adoption require separate explicit authorization.
