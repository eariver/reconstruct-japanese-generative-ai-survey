# AGENTS.md

ChatGPT chat / workの切り替えは適宜Humanが判断するので、SystemUIで提案しないでください。

This repository is the writable workspace for an external architecture/design review of `eariver/japanese-generative-ai-survey`.

## Current task: Re:Phase 1

Human explicitly reset the reconstruction direction on 2026-09-15. Prior Phase structure, decisions and next steps are historical evidence, not architecture authority. Re:Phase 1 direction reassessment and the bounded operating-rule/live-status separation proposal are complete; reconstruction overall remains open. The five-file r2 candidate has completed bounded root caller/test and edited-rule review, with local repairs and document-only checks. One explicitly authorized independent review of r2 is complete with no actionable findings in its bounded scope. Root retained r2 unchanged. No production adoption or net lifecycle saving is established.

Read first:

1. `handoff/rephase-1-continuation.md`
2. `outputs/rephase-1-review-disposition.md` — current independent-review disposition and remaining boundaries. The prior `outputs/rephase-1-connection-assessment.md` retains root connection evidence.
3. Necessary evidence only from `notes/rephase-1-connection/README.md`. Prior design/obligation map: `outputs/rephase-1-operating-contract-assessment.md`; r1 evidence remains historical. The broader direction remains in `outputs/rephase-1-direction-assessment.md`.

Historical reconstruct starting baseline: `ec6a502e9ae37e956d677f96f29af6c4e4591fc4`; this is not a claim about the present HEAD.
Human-fixed production baseline: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`.
Do not change this baseline or follow/inspect newer production main unless Human explicitly requests rebaselining. The previous remote observations are historical. Use the captured fixed-ref inputs and only retrieve missing fixed-ref blobs when necessary.

Current Human instruction: **No Git operations.** Do not run even read-only Git status/diff/log/rev-parse, fetch, worktree/init or Git-aware tests. Do not query remote Git/ref endpoints. Use filesystem reads/hash/difflib and Git-free offline checks. Do not invoke older capture/observe helpers that contain Git or ref lookups.

Selected direction: retain this workspace, logically archive prior work, and rebaseline against current production. Evaluate partial redesign by naming work that can actually be removed while retaining required guarantees. Current Core, canonical schemas, role assignments and audit implementation are comparison starting points, not permanently fixed architecture.

The bounded proposal removes copied live status from authority/index documents and the execution-record initializer, together with the policy requiring those copies to be maintained. It retains substantive mandatory reading/review obligations and session history. Current candidate: `notes/rephase-1-connection/candidate.patch` (r2); r1 is preserved. The r2 follow-up repaired configuration-driven review navigation, objective/mode/transport navigation, pending-review guidance, and overly broad Markdown/Frozen wording. It remains a reconstruct proposal, not a ready-to-adopt production patch.

Root caller/test and edited-rule review is complete. Five grouped r2 checks include four actual upstream document-only tests; 42 normative sections and all helper AST outside two templates are unchanged. Execution-record tests were statically inspected, not executed. The completed independent review supports bounded rule/navigation/static compatibility only. No full initializer/CLI/bridge/Core integration or savings is established. The earlier display experiment is not a new Core validator and must not be installed wholesale.

The authorized r2 independent review is complete. Report: `notes/rephase-1-connection/independent-review.md`; input/closeout records bind it to unchanged candidate hashes. No candidate repair was requested. The operating-rule/live-status separation unit is now complete through bounded independent review. Do not repeat root checks or independent review without new evidence.

The remaining path toward adoption is existing integration verification in an explicitly permitted environment, then a separate production-adoption decision under normal Core review/CI/contract rules. Git remains prohibited, and this review is not seven-point audit PASS or execution compatibility certification. Do not weaken reviewed-commit verification or call stubbed runs full Core validation. This one-agent r2 permission is completed; it is not general delegation permission. Stop at this supported decision surface rather than expanding into a dashboard, manual framework, telemetry or another resolver.

The old default sequence of Freeze repair followed by reader repair is superseded as reconstruction's work order. Their fixed-ref counterexamples remain maintenance evidence; fix a defect when it is a prerequisite for the particular route being evaluated. Do not make every maintenance item a prerequisite to architecture work. Do not transplant the whole old runtime patch over current #495/#496.

## Objective and evidence discipline

Minimize total lifecycle work across production, source research, all-role reasoning/review, repair/regeneration, CI/runtime, LLM usage, operational complexity, migration/dual maintenance, and Human handoff, while preserving publication quality, research sufficiency, provenance, fail-close for crisp invariants, Human authority, Weekly/Special viability and historical traceability. Moving work is not saving. Justified long-term investment is allowed.

Distinguish source inspection, function/schema witnesses, synthetic chains, actual production records, independent review and measured work. Full publication quality, current cold-start/general execution and net savings remain unproven. Do not infer cognitive work from artifact count or missing logs, or count necessary independent review as duplication. Unknown costs are not zero.

Current W33/W34/SP001 saved States say RELEASED; this reassessment did not repeat full dependency/publication validation. #492/#495/#496 are upstream achievements. Their merged implementation does not establish reconstruct adoption or ordinary-path viability. Preserve actual Human approval and historical authority.

Prior outputs, notes, handoffs, instructions, brief and patches stay in place as historical records. Their old current/next/phase wording does not override this entry or the current Human request. Do not overwrite historical decisions. Reuse relevant evidence with its scope and limitations rather than re-running successful tests or reloading all chats by default. Old 5-B non-support is not universal disproof; old lab failures are not successful publication. Read the original evidence when reusing a specific result.

## Repository and execution boundaries

- `eariver/japanese-generative-ai-survey` is READ ONLY unless Human explicitly authorizes a production mutation. No production branches, PRs, Issues/comments, State, decisions, Gates, Freeze/Release, adoption or migration changes.
- `eariver/reconstruct-japanese-generative-ai-survey` is writable for analysis, proposals and bounded isolated probes/candidates within the current request.
- All Git operations are currently prohibited by Human, including read-only inspection. Ordinary Git Pull/Push and final commit remain Human-owned.
- New independent-agent work requires fresh explicit permission for the concrete scope. Prior Phase 4-C/5-B permissions are exhausted. One r2 independent review was explicitly authorized and completed with no actionable findings in scope; this is not general delegation permission.
- Do not fix or update a stale/dirty production checkout for investigation. Read fixed source through read-only APIs when needed.
- Git-aware fixtures are not allowed under the current instruction. If Human later authorizes Git work, they must use an independent isolated Git root and inert origin. Never let fixture object/ref creation inherit reconstruct's Git database. Preserve the historical distinction between the old first run's 52 passes/6 Git-root errors and its isolated follow-up.

Choose targeted, cost-aware reads and stop when additional evidence is unlikely to change the decision. External tools/OSS are options when a concrete replacement boundary warrants comparison; do not conduct broad research merely for coverage. Production's current operating constraints remain effective until explicitly changed, even when reconstruct proposes alternatives.

For closeout-only requests, update the current handoff and stop. Do not infer authorization for a new phase or trial from a commit title.
