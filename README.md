# reconstruct-japanese-generative-ai-survey

External architecture review and reconstruction workspace for `eariver/japanese-generative-ai-survey`. Production remains read-only until the Human explicitly authorizes a change.

## Re:Phase 1 — start here

**Direction reassessment is complete.** Continue in this repository, treat prior Phases as historical evidence, and use current production as the new comparison baseline. The old Phase 5 work order is superseded.

1. [Re:Phase 1 handoff](handoff/rephase-1-continuation.md)
2. [Direction assessment](outputs/rephase-1-direction-assessment.md), especially sections 1 and 6–7
3. [Evidence and verification scope](notes/rephase-1/README.md), only as needed

Fixed baselines, confirmed through read-only GitHub APIs on 2026-09-15 JST:

- reconstruct: `ec6a502e9ae37e956d677f96f29af6c4e4591fc4`
- production main: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`

Selected direction: partial redesign around current production, removing identifiable operational work while preserving quality, authority and history. The next bounded proposal separates effective operating rules from live status and names the duplicate current statements and reading/update obligations it would retire. It is not yet implemented. Known Freeze/reader defects remain maintenance evidence, not an automatic reconstruction roadmap.

## Purpose

Produce high-quality Weekly and Special editions with substantially less total lifecycle work: production, research, supervisory reasoning and independent review, repair, CI/runtime, LLM usage, maintenance/migration and Human effort. Moving work between roles is not saving. Current Core and role assignments may be reconsidered; their existing guarantees must be accounted for.

No architecture adoption, full current-production quality certification or net saving has been established. W33/W34/SP001 saved States are RELEASED; this is not a new full-chain or PDF quality validation.

## Historical archive

Prior `outputs/`, `notes/`, `handoff/`, `instructions/` and `brief/` remain at their original paths for provenance and reproducibility. Archive is logical: no historical files were moved or rewritten. Their old current/next/Phase instructions are historical and do not govern new work.

The [last Phase 5 assessment](outputs/astra-phase-5-upstream-reconciliation-assessment.md) and [old handoff](handoff/astra-phase-5-continuation.md) retain the prior disposition and limits. Consult a historical result only when it has information value for the current decision. The pre-reset repository, including its old entry documents, remains available at `ec6a502e`.

The Human handles ordinary Git Pull/Push and final commit. Production posting, application and adoption require separate explicit authorization.
