# DM021-P2R implementation — bounded complete

2026-10-14. [Assessment / exact identity / next design-only task](../../outputs/rephase-1-dm021-p2r-assessment.md) is the current entry. Fixed [retention contract194fd7de](../../outputs/rephase-1-dm021-retention-contract-decision.md) unchanged. One-shot retained-root capture + standalone exact retained-set verification, **not current eligibility or full DM021 repair**. Whole NOT_READY, step4/B3 OPEN, canonical audit unstarted, DM021 OPEN. Stop at Human Commit Point.

## Read final evidence together

1. [Final correction2 packet](evidence-20261014T000000Z-correction2/) and `correction2-final-report.md`.
2. **[Astra closeout resolution / mandatory errata](evidence-20261014T000000Z-correction2/astra-closeout-resolution.md)** + [fresh author-independent final resolution, including §10](evidence-20261014T000000Z-correction2/independent-final-resolution.md). BOUNDED_PASS for this component only.
3. `expected16-correction2c.json`, `inherited13-static-freeze.json`, `cache-inventory-static.json`; `run_p2r_correction_v9.{pre,post,meta,stage-running,stage-done}.json`, `.stdout.txt`, `.stderr.txt`, `.exit` and executed `.py.READY`. Final25/7936.817s/no skips/child0+wrapper0. Affected2 is included again in25, not added coverage; optimized1 is separately scoped.
4. `complete-p2r-16path-v3.patch` + `.sha256`: **830622B**, SHA256 **5b79218e3c90fc8bcb11e39571e2ab1e8dfc52e04f5e98843937e4e876515208**. Final saved-patch `proof_apply16_v7.py.READY`/raw/exit and `proof-freeze-{clean,applied}-v7.json` prove the bounded clean409 application.

## Source and recovery

Active `/tmp/opencode/jgas-dm021p2r-impl-20261013T123807Z/candidate-partial-b40de60`; final apply copy `/tmp/opencode/jgas-dm021p2r-verify-20261014T000007Z/candidate-partial-b40de60`. Both actual detached409b292756dd1277b9dfae87679934c0d2ce251c/tree8ce3699861505f32d1d60bdc185d4d4f635aedb2 **plus16 uncommitted paths3M13A**. Active additionally preserves84 pinned cache files; final run checked exact100 raw rows and avoided in-tree cache execution using a fresh absent prefix + disabled bytecode writes. Apply-copy-only84 cache removal is recorded. No candidate commit/branch.

P2R module3833b14a/schema347e5499/test4155baab; all3 physical0664. P1 inherited13 unchanged. Final test1818 lines corrects report1802. P1 original active/apply copies remain preserved, with their own qualifications. If current copies disappear, use [four parent409 inputs](../rephase-1-dm021-contract/availability-at-closeout.md) with new fail-closed restoration, then **full16patch directly to clean409** (contains P1/LF2I/LF1; do not layer those first). Partial DB/missing26309blobs/runtime-unbundled limits persist. Do not rerun saved scripts or infer continuous availability from recorded snapshots.

## Work, interruption and corrections

- Human starting reconstruct **a45e1bfea675b496b44b01f50460d1458675c840**. General actual code/tests; Astra architecture/source/oracle/evidence review; separate independent reviewers. No Production/network/intake/adoption/commit.
- [Task](task.md), [initial concrete interface](interface-proposal.md), [root feedback](astra-interface-feedback.md), [correction](interface-correction.md), [implementation selection](astra-implementation-selection.md). PhaseA `raw-*` files are transcribed tool observations, not direct shell logs; task was Astra-authored.
- Initial `evidence-20261013T123807Z-impl/`: initial3,10 successes plus setup failures and initial independent CHANGES_REQUIRED. Root [R1](astra-review-r1.md) found additional real behavior/guard gaps.
- `evidence-20261013T173500Z-correction/`: initial3 preservation, correction attempts, failed v4 (17/18), interrupted v5 (pre/meta only), v6 earlier19 plus optimized1/patchf42. [Resumption record](resume-after-interruption.md) preserves Human request and observed process/result bounds. Earlier independent blanket R1–R6 PASS was overstated; root [R2](astra-review-r2.md) supersedes it.
- `evidence-20261014T000000Z-correction2/`: drafts, READY revisions, static pins/cache inventory, preedit v6 actual byte copies, [execution selection](correction2-execution-selection.md), failed v8 (23/25), affected2 and final v9 (25/25), final optimized1 and v7 apply proof. Every result retains its own source/version scope.
- Proof failures were a clean-freeze bug in the Worker's own script; external-deletion/sparse/timer/process hypotheses are retracted. An UNEXECUTED proof draft was deleted/restored without byte certification. Diagnostic scratch, strace, tool substitutions and cache residue remain disclosed. No generic rerunner certification.

## Important scope qualifications

COPY+KEEP is a dependency-bearing set, not self-contained backup, semantic approval or current authority. Capture is one-shot, existing root refuses, no partial resume/takeover/cleanup. P1 post-capture refusal is preserved. Historical verifier uses retained State→exact Profile KEEP relation, no current-State/basename substitution. Late-plant test proves refusal + post-removal equality rather than immediate injected-path no-write; final proof logger has unproved fault propagation. See mandatory root/independent supplements rather than broad initial PASS language. Synthetic fixtures and identity checks are not genuine Human/semantic/visual acceptance; no global CAS/atomicity/replica guarantee.

Next after Human continuation: assessment§4 retained-aware current-authority **contract analysis before code**, not automatic live promotion. No reason/State/Candidate/Human Gate changes selected. Stop at this Commit Point.
