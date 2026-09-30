# R1 mechanical refresh — current evidence entry

**Bounded implementation complete at b74db67.** Read [Astra assessment](../../outputs/rephase-1-mechanical-refresh-assessment.md) and [selected contract](../../outputs/rephase-1-mechanical-refresh-contract-decision.md). This reviewed R1 is in a fresh-root isolated DB, not e4 ancestry; its later e4-lineage assembly is recorded separately below. Whole candidate NOT_READY.

**Later assembly completion:** the exact seven-path increment is now assembled as e4's direct child **481dec0**, with separate scoped checks/review. Read [assembly assessment](../../outputs/rephase-1-r1-assembly-assessment.md) and [assembly packet](../rephase-1-r1-assembly/README.md) for current identity/next task. This packet retains b74's own implementation evidence and limitations; historical assembly-pending text below is not a rerun instruction.

## Current exact evidence

- [Final manifest](correction/final-b74db679f03908048db91420a8f262d412b8f58c/manifest-final.json): HEAD `b74db679f03908048db91420a8f262d412b8f58c`, tree `515b5e93a29ba82d87f6fa81c7ecbaf2c3701bb0`, parent `57853cb76d3189b862f1edabe46b83cfc0c7bd29`. Seven exact changed-file copies and full **a1a4242→b74** patch (not baseline→b74) in that directory.
- Final raw logs: `weekly-refresh.log` 34, `revalidation.log` 31, `gate.log` 27, `cli.log` 5 — **97 methods, no skips, all exit 0**, with actual source pins. Earlier matrices have their own identities; subtests are not extra methods.
- [Independent first review](correction/independent-review-8a544f9.md): CHANGES_REQUIRED at 8a; [independent final resolution](correction/independent-resolution-b74db67.md): BOUNDED_PASS at b74. No tests/candidate writes by reviewer; neither is the seven-point audit or Human approval.

## Historical records and mandatory limits

- `operational-contract-analysis.md` retains original proposals and explicit correction section; the root contract controls implementation.
- `implementation/` contains original afd925d return, failed/development logs and [clarification](implementation/03-return-evidence-clarification.md): four hook bypasses contrary to instruction, fresh copied-content root, 41 unverified historical blobs, missing run-time pins. `returned-afd925d/` preserves that source separately.
- `correction/round2/` is the 8a matrix and copies. **`correction/round3/` was overwritten/re-anchored**, despite the preservation rule: initial 985/20177 raw logs are lost/unverified. `returned-57853cb/` archives the later state as found. [Author limitation note](correction/evidence-preservation-limitations.md) plus Astra's assessment give the corrected scope; neither listing nor recreated source recovers old raw execution output.
- `correction/witness-afd.py` is heuristic source-string inspection, not a regression oracle or 23 real defect reproductions. Do not treat its generic exit 0 as a test PASS.
- **Do not auto-run saved scripts, runners or previous witness harnesses.** They may target fixed fixtures/log paths, and their labels are historical. Future justified runs require a fresh output target and explicit identity checks.

Synthetic accepted chains/reviews/PDFs retain that label. Cooperative serialization, byte/identity-checked writes and guarded ordinary-failure recovery are bounded guarantees, not crash recovery/global CAS/full publication acceptance. The next task is seven-path integration onto an independent e4-lineage database with fresh exact identity and scoped review, not a new feature or a repeat of completed tests.
