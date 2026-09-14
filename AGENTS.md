# AGENTS.md

ChatGPT chat / workの切り替えは適宜Humanが判断するので、SystemUIで提案しないでください。

This repository is the writable workspace for an external architecture/design review of `eariver/japanese-generative-ai-survey`.

## Current task: Re:Phase 1

Human explicitly reset the reconstruction direction on 2026-09-15. Prior Phase structure, decisions and next steps are historical evidence, not architecture authority. Re:Phase 1 direction reassessment is complete; reconstruction overall remains open. No production adoption or net lifecycle saving is established.

Read first:

1. `handoff/rephase-1-continuation.md`
2. `outputs/rephase-1-direction-assessment.md` — sections 1 and 6–7; sections 2–5 for evidence and disposition when needed.
3. Necessary evidence only from `notes/rephase-1/README.md`.

Reconstruct baseline: `ec6a502e9ae37e956d677f96f29af6c4e4591fc4`.
Production baseline: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`.
Both remote main refs were GET-confirmed. These are fixed observations, not a promise of future currentness.

Selected direction: retain this workspace, logically archive prior work, and rebaseline against current production. Evaluate partial redesign by naming work that can actually be removed while retaining required guarantees. Current Core, canonical schemas, role assignments and audit implementation are comparison starting points, not permanently fixed architecture.

If asked to continue, the selected next bounded unit is a reconstruct-only proposal separating current operational rules from live status, with an explicit retirement mapping for duplicate current statements and reading/update obligations. Use the concrete scope and stop conditions in assessment section 7.1. A new summary added on top of all existing obligations is not success. This unit is not implemented yet. Do not automatically start a full manual rewrite, wrapper framework, telemetry system, source-to-PDF shadow execution or cost trial.

The old default sequence of Freeze repair followed by reader repair is superseded as reconstruction's work order. Their fixed-ref counterexamples remain maintenance evidence; fix a defect when it is a prerequisite for the particular route being evaluated. Do not make every maintenance item a prerequisite to architecture work. Do not transplant the whole old runtime patch over current #495/#496.

## Objective and evidence discipline

Minimize total lifecycle work across production, source research, all-role reasoning/review, repair/regeneration, CI/runtime, LLM usage, operational complexity, migration/dual maintenance, and Human handoff, while preserving publication quality, research sufficiency, provenance, fail-close for crisp invariants, Human authority, Weekly/Special viability and historical traceability. Moving work is not saving. Justified long-term investment is allowed.

Distinguish source inspection, function/schema witnesses, synthetic chains, actual production records, independent review and measured work. Full publication quality, current cold-start/general execution and net savings remain unproven. Do not infer cognitive work from artifact count or missing logs, or count necessary independent review as duplication. Unknown costs are not zero.

Current W33/W34/SP001 saved States say RELEASED; this reassessment did not repeat full dependency/publication validation. #492/#495/#496 are upstream achievements. Their merged implementation does not establish reconstruct adoption or ordinary-path viability. Preserve actual Human approval and historical authority.

Prior outputs, notes, handoffs, instructions, brief and patches stay in place as historical records. Their old current/next/phase wording does not override this entry or the current Human request. Do not overwrite historical decisions. Reuse relevant evidence with its scope and limitations rather than re-running successful tests or reloading all chats by default. Old 5-B non-support is not universal disproof; old lab failures are not successful publication. Read the original evidence when reusing a specific result.

## Repository and execution boundaries

- `eariver/japanese-generative-ai-survey` is READ ONLY unless Human explicitly authorizes a production mutation. No production branches, PRs, Issues/comments, State, decisions, Gates, Freeze/Release, adoption or migration changes.
- `eariver/reconstruct-japanese-generative-ai-survey` is writable for analysis, proposals and bounded isolated probes/candidates within the current request.
- Ordinary Git Pull/Push and final commit are Human-owned. Do not perform them.
- New independent-agent work requires fresh explicit permission for the concrete scope. Prior Phase 4-C/5-B permissions are exhausted. No delegation was performed in Re:Phase 1.
- Do not fix or update a stale/dirty production checkout for investigation. Read fixed source through read-only APIs when needed.
- Git-aware fixtures must use an independent isolated Git root and inert origin. Never let fixture object/ref creation inherit reconstruct's Git database. Preserve the historical distinction between the old first run's 52 passes/6 Git-root errors and its isolated follow-up.

Choose targeted, cost-aware reads and stop when additional evidence is unlikely to change the decision. External tools/OSS are options when a concrete replacement boundary warrants comparison; do not conduct broad research merely for coverage. Production's current operating constraints remain effective until explicitly changed, even when reconstruct proposes alternatives.

For closeout-only requests, update the current handoff and stop. Do not infer authorization for a new phase or trial from a commit title.
