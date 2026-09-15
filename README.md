# reconstruct-japanese-generative-ai-survey

External architecture review and reconstruction workspace for `eariver/japanese-generative-ai-survey`. Production remains read-only until the Human explicitly authorizes a change.

## Re:Phase 1 — start here

**The r2 proposal, bounded independent review and bounded Git-aware integration are complete.** Continue in this repository and treat prior Phases as historical evidence. The old Phase 5 work order is superseded.

1. [Re:Phase 1 handoff](handoff/rephase-1-continuation.md)
2. [Current integration assessment](outputs/rephase-1-integration-assessment.md); prior assessments retain their original scope
3. [Integration evidence](notes/rephase-1-integration/README.md) and [r2 candidate/review evidence](notes/rephase-1-connection/README.md), only as needed; [prior design](outputs/rephase-1-operating-contract-assessment.md) remains historical context

Baselines:

- historical reconstruct starting point: `ec6a502e9ae37e956d677f96f29af6c4e4591fc4`
- Human-fixed production baseline: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`

Do not follow newer production main or rebaseline without explicit Human instruction. **Necessary Git operations and Git-aware tests are now authorized.** Use independent fixture repositories; production changes/adoption remain separately unauthorized.

The [broader direction](outputs/rephase-1-direction-assessment.md) remains partial redesign that removes identifiable work while preserving quality, authority and history. The [five-file r2 candidate](notes/rephase-1-connection/candidate.patch) removes copied live status and its maintenance obligation while retaining substantive reading/review. Its bytes remain unchanged after one bounded independent review and integration.

The latest evidence covers 27 distinct upstream bridge/Human Gate tests (18 initial Linux passes + 9 after test-guard repairs), real-loader CLI scenarios for Weekly/Thematic/Retrospective, and an unchanged-navigation revision/approval chain. The isolated Git commits and research/Human records are synthetic fixtures. Full CI/Actions/publication, final audit, adoption and net savings are not established.

The bounded candidate work is complete. Next is Human's decision whether to advance it toward production application review under existing Core/CI/fixed-head/contract rules. Do not rerun successes or add another independent review without a new concern/required authorization. Known Freeze/reader defects remain maintenance evidence, not an automatic roadmap.

## Purpose

Produce high-quality Weekly and Special editions with substantially less total lifecycle work: production, research, supervisory reasoning and independent review, repair, CI/runtime, LLM usage, maintenance/migration and Human effort. Moving work between roles is not saving. Current Core and role assignments may be reconsidered; their existing guarantees must be accounted for.

No architecture adoption, full current-production quality certification or net saving has been established. W33/W34/SP001 saved States are RELEASED; this is not a new full-chain or PDF quality validation.

## Historical archive

Prior `outputs/`, `notes/`, `handoff/`, `instructions/` and `brief/` remain at their original paths for provenance and reproducibility. Archive is logical: no historical files were moved or rewritten. Their old current/next/Phase instructions are historical and do not govern new work.

The [last Phase 5 assessment](outputs/astra-phase-5-upstream-reconciliation-assessment.md) and [old handoff](handoff/astra-phase-5-continuation.md) retain the prior disposition and limits. Consult a historical result only when it has information value for the current decision. The pre-reset repository, including its old entry documents, remains available at `ec6a502e`.

The Human handles ordinary Git Pull/Push and final commit. Necessary Git operations and independent Git-aware fixtures are authorized. Production posting, application and adoption require separate explicit authorization.
