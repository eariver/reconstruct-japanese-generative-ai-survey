# R1 mechanical refresh — Astra bounded completion assessment

Recorded 2026-09-29; root clock observed `2026-09-29T23:14:20+09:00`. **The selected seven-path R1 implementation is bounded complete at b74db67**, following source/oracle corrections, a pinned 97-method matrix and a separate independent resolution. This is root's author-side judgment. **Whole candidate remains NOT_READY; step 4/B3 and baseline application remain open.** No production adoption or canonical seven-point audit occurred.

## Exact identities — do not merge the two Git histories

- Reviewed R1 implementation: **`b74db679f03908048db91420a8f262d412b8f58c`**, tree `515b5e93a29ba82d87f6fa81c7ecbaf2c3701bb0`, parent `57853cb76d3189b862f1edabe46b83cfc0c7bd29`.
- Fixture `/tmp/jgas-rephase-mechanical-r1-20260928T000710Z`, branch `codex/rephase-1-mechanical-r1-correction`, independent database/inert origin. Root rechecked HEAD/tree/parent and tracked-clean status; Python caches remain untracked.
- Its basis **`a1a4242adaddc42427b68c18ae367c04d6cd63b4` is a fresh copied-content root**, not an e4c8269 descendant. Four existing changed-path mode/blob identities were verified against e4c8269; three paths were new. The broader copy has 683 verified blobs and 41 unverified historical data blobs. R1 tests use constructed synthetic editions from the verified code/config/schema subset. Full-tree equivalence or application is not claimed.
- Preserved integration/shipping-line candidate **e4c82692abee6acedbba07815b0d74ccefb80a7e** and B **c04f32ad46109403e8a63faaa8394a90ee6b869c** remain unchanged. Root ran read-only tracked-diff/HEAD checks on both. The next assembly must not silently turn a fresh-root R1 PASS into an e4-lineage or fixed-baseline application PASS.
- Production baseline `774dd39a951c9ac3818e83dfffd4c7666efb0a20` remains fixed. Ordinary reconstruct Commit/Push remains Human-owned; reconstruct HEAD was `d17560028bd5db459636ca957888b7369b5d5cda` throughout this continuation.

## What R1 now implements

`survey_agent_control_v2.py refresh-mechanical-evidence` is a bounded operational writer for **same-edition, same-reader-input, same-output Weekly** evidence renewal after an allowed committed change to `survey_weekly_derivation_v2.py`. It requires an R1-installed baseline receipt, strict pre-decision VALIDATED_DRAFT State, unchanged review criteria/config/schema/other controls, clean committed tool bytes and identical accepted/authored/source/PDF/manuscript/review/QA bindings. Other changed control paths, pre-install migration, changed output/content/criteria and unresolved existing pending State are unsupported.

The writer anchors the old Gate to current checkpoint/effective active authority and its old receipt to that Gate. Private structural/semantic inspection is shared with ordinary validators; **public Gate/receipt validation still always performs full current replay**. Historical closure is checked against actual generating-commit blobs, not an assumed original-head identity.

Before replacement it captures/rechecks bound input, checkpoint/deterministic-result, predecessor-chain, reviewer/QA/PDF and control-file/membership dependencies. Both superseded receipt and Gate bytes (plus State and inert metadata) are retained and verified. An exclusive guard has per-operation nonce and fd identity. Receipt/Gate use checked same-directory replacement; the existing revalidation owner exclusively creates its record and replaces State from known serialized bytes. Record/guard/temp deletion requires known bytes and ownership identity. Conflicting or ambiguous failure retains evidence and fails closed; post-commit reporting cannot roll back established authority.

For repeat refresh after prior metadata renewal, **Gate is the only new change relative to the healthy active starting authority**. The pending row list is relative to the original checkpoint, so already-active non-Gate superseded rows may remain only with exactly the same name/path/prior/new hashes. Root adopts this as the precise interpretation of the original Gate-only contract, not permission to introduce new non-Gate changes.

## Source and oracle review history

Root's [initial afd925d findings](rephase-1-mechanical-refresh-review-findings.md) were CHANGES_REQUIRED: guard removal on failed restoration, non-exclusive record creation/truncating State writes, incomplete snapshots, alias/canonical-path gaps, incomplete prior binding and insufficient failure oracles. A fresh correction General worked within the same seven paths, preserving the original candidate history.

Further root review rejected comments/summary as proof: directory roots were not actually snapshotted; validation checkpoint review-result refs were still skipped; alias checks followed resolution; temp identity did not protect changed same-inode bytes; API post-rename failure could delete a still-referenced record; metadata comparison was weakened to pass a fixture. These were corrected with actual recorded-ref snapshots, raw-first path checks, complete semantic-authority forwarding, phase-aware ownership checks and targeted fault tests.

The final small correction preserves valid non-DETERMINISTIC checkpoint review rows with `result: null`; only deterministic result references require and pin `{path,sha256}`, while the entire checkpoint file remains hash-bound. Its real validator-positive refresh test and true validation-report drift tests are included in the final matrix. No malformed legacy-result fallback was accepted.

The independent reviewer first issued [CHANGES_REQUIRED at fixed 8a544f9](../notes/rephase-1-mechanical-refresh/correction/independent-review-8a544f9.md), including record-inode ownership, nonce/retry separation and two low-priority checks. It then inspected the complete successor delta and issued its own **[BOUNDED_PASS at b74db67](../notes/rephase-1-mechanical-refresh/correction/independent-resolution-b74db67.md)**, resolving K1–K5/N1–N4 with no remaining blocker within the selected scope. Root read both reports and the relevant final code/deltas. The reviewer neither changed candidate bytes nor executed tests. Its judgment is separate from author execution and root review; it is not canonical seven-point acceptance.

Nonce qualification: earlier deterministic timestamp collisions already failed closed; predictable names alone were not an acceptance exploit. Unique operation identity improves retry separation. Identity/byte checks detect specified interleavings but do not make the final check-plus-filesystem syscall globally atomic against arbitrary noncooperators.

## Final evidence

[Final manifest and seven copies](../notes/rephase-1-mechanical-refresh/correction/final-b74db679f03908048db91420a8f262d412b8f58c/manifest-final.json) / [full R1 patch from a1 basis](../notes/rephase-1-mechanical-refresh/correction/final-b74db679f03908048db91420a8f262d412b8f58c/patch-final-a1-b74db67.patch), recorded SHA-256 **`7817fa4fc027ae0bac9bbd7e7bbd18c588ba3373b52e17730eafebe2b92aab01`**. This includes initial R1 plus corrections; it is **not a full production-baseline patch**. Root independently compared the seven copied files' Git object hashes to actual b74 committed blobs; all match, and the a1→b74 diff contains exactly the selected seven paths.

| Final module | Methods | Raw outcome at b74 |
|---|---:|---|
| Weekly mechanical refresh | 34 | OK; exit 0; 1677.448 s |
| Publication revalidation | 31 | OK; exit 0; 56.284 s |
| Reader-Surface Gate | 27 | OK; exit 0; 1.204 s |
| Gate CLI persisted review | 5 | OK; exit 0; 40.137 s |
| **Total** | **97** | **0 failures/errors/skips** |

The final directory's four raw logs pin HEAD/tree/parent, source hashes, command/cwd, Python 3.12.14 and dependency versions, and explicit numeric exits. Root inspected those pins and completion results. Subtests are within methods, not additional method counts. The earlier eight-method Weekly derivation result is antecedent evidence, not a b74 exact-head run. Root/reviewer did not rerun tests.

Meaningful cases include real accepted first/repeat paths, healthy prior metadata revalidation, both old-byte retention, non-op/artifact-only refusal, input/output/criteria/staged/dirty/alias/canonical failures, actual overlapping cooperating calls, foreign same-byte record/guard replacements, validation-report/QA dependency drift, temp ownership, post-rename no-dangling-pointer and post-commit no-rollback. Fault injections are labelled; no successful authority or Git checks are fabricated. Synthetic research/reviews/blank PDF exercise actual publisher/CLI/validators but are not real editorial/visual/Human acceptance.

## Procedure and preservation qualifications — not retroactively clean

- [Original return clarification](../notes/rephase-1-mechanical-refresh/implementation/03-return-evidence-clarification.md) records four prohibited `--no-verify` uses, the contradictory initial summary, changed Git basis, 41 unverified data blobs and missing original runtime identity pins. These facts remain. Later normal correction commits do not undo the violations, and absence of a bypass flag does not independently prove that any particular hook executed.
- Earlier `all_runs: 0`, “23 failing witnesses,” and source-string tests are not accepted as broad runtime evidence: failed batches remain failures, and `witness-afd.py` is heuristic source inventory, not 23 executed defect reproductions.
- **Evidence overwrite deviation:** root directly observed `correction/round3/manifest-round3.json` initially bound to 985dcd6 and later to 57853cb; corresponding older suite outputs were replaced in place. The author's [limitation note](../notes/rephase-1-mechanical-refresh/correction/evidence-preservation-limitations.md) describes 20177a1→578, but is incomplete about the earlier 985 state. Treat both older raw-run sets as **lost/unverified** unless actually preserved. Source is recoverable from immutable commits; logs cannot be reconstructed from source or summaries. Directory listing alone is not byte-identity verification.
- `returned-57853cb/` preserves the later packet as found. The final b74 directory is separate and the current acceptance relies on its pinned logs/copies and review, not lost execution records. Old source revisions/failed attempts are not silently promoted to final PASS.
- The author repeated a broader four-module matrix after the final tiny fix than root requested. Record the actual successful scope without presenting the extra execution as necessary or as measured lifecycle savings. Do not repeat the now-passing checks for decoration.
- Saved runners/old harnesses are evidence, not safe rerun instructions. Any later justified run must refuse existing output paths and pin its own source identity. Ordinary final reconstruction commit has not been performed by agents.

## Remaining limits and next task

Continuation update 2026-09-30: the e4-lineage assembly described below is now bounded complete at **481dec0**, with direct e4 parent, seven b74-identical paths, selected fresh checks and a separate assembly review. Read [assembly assessment/next task](rephase-1-r1-assembly-assessment.md). b74 retains its original implementation scope; no full baseline application or old-97 transfer follows. The task below remains the prior authorization record, not a repeat-work instruction.

R1 does not provide full multi-file atomicity, automated crash/power-loss recovery, global CAS/noncooperating-editor safety, changed-output regeneration, pre-install migration, real build/PDF-preflight/transfer, all-profile support, Windows/Actions proof or net lifecycle savings. Existing Special/support, DM-001/003/004 and optional findings transport dispositions remain. Full baseline application and the canonical audit are still open.

**Next bounded unit: restore an e4-lineage integration candidate, not another feature.** General should prepare an independent **byte-copied Git database** from preserved e4c8269 (not `git archive`, full clone, worktree or object sharing), keep its sparse/promisor limits explicit, and inspect/apply only the verified seven-path R1 increment. Verify each preimage, resulting code/mode/blob equality to b74 and unchanged unrelated entries; no hydration/current-main access or auto-migration of edition States. Preserve both original databases. If copying or normal hooks prevent this, return the exact blocker; do not make another undisclosed fresh-root substitute or bypass hooks.

On a new local review commit record actual parent/tree/changed hashes. A new head/history requires affected Git-aware/current-tool diagnostics and scoped assembly review; do not transfer b74 PASS automatically. Choose those checks by the demonstrated assembly delta rather than rerunning every suite by default. No live publication/rebaseline/reconstruct Commit/Push is authorized. This closeout is a Human commit/Push checkpoint.
