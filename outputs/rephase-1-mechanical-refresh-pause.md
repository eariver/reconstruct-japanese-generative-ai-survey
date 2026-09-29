# R1 — Human-requested safe pause before root review

**Later status:** Human resumed; the unreviewed return below received CHANGES_REQUIRED, then bounded corrections and independent resolution completed at b74db67. Read [current assessment](rephase-1-mechanical-refresh-assessment.md). This document preserves the actual earlier pause; no current pause or redispatch instruction is inferred from it.

Recorded **2026-09-28T23:30:46+09:00** (root clock). Human requested a stop at a safe point after General returned implementation/test evidence. **Stopped before Astra implementation/oracle review and before independent review.** This is a pause inventory, not candidate acceptance or a test-evidence verdict. No further Worker, tests, repairs or independent review were launched for closeout.

## Saved state

- Reconstruct HEAD remains Human commit `d17560028bd5db459636ca957888b7369b5d5cda`; no agent Commit/Push. New contract/analysis/implementation packet and pause-entry updates are uncommitted.
- Last reviewed shipping candidate remains **e4c82692abee6acedbba07815b0d74ccefb80a7e**. Root rechecked its HEAD and tracked-clean status (pre-existing Python caches only). R1 is a separate, **unreviewed** candidate.
- R1 fixture: `/tmp/jgas-rephase-mechanical-r1-20260928T000710Z`, branch `codex/rephase-1-mechanical-r1`.
- R1 candidate **`afd925d4f2413533e62c3ed211c732dd4a4d1539`**, tree `2ee9cf2a284aca8497e99fb833102b03f2fcf0a2`, parent `e79967ac4a8d5da4b78e1a6ba8902c0ab2e2ced8`. Root read these Git identities and tracked-clean status; `scripts/__pycache__/` and `tests/__pycache__/` remain untracked.
- Intermediate runtime: `65ee720358a534bcd2c93ee02c80682971d6844c`; corrections: `e79967ac4a8d5da4b78e1a6ba8902c0ab2e2ced8`.
- **Different Git basis:** `a1a4242adaddc42427b68c18ae367c04d6cd63b4`, tree `4b0fcadc172ffc999b318dc6e39a6f0a0f218b27`, is a fresh root commit of copied worktree bytes, **not e4c8269 and not its Git descendant**. General reports 683/724 copied blobs verified against e4c8269, with 41 promisor-missing historical `sources/...` data files unverified. Source-boundary equivalence/isolation needs review before any inherited PASS or acceptance.

## Durable entries

1. [Astra selected contract/task](rephase-1-mechanical-refresh-contract-decision.md).
2. [General source analysis, including section 11 corrections](../notes/rephase-1-mechanical-refresh/operational-contract-analysis.md).
3. [Implementation isolation/path inventory](../notes/rephase-1-mechanical-refresh/implementation/00-isolation-inventory.md).
4. [Worker test report](../notes/rephase-1-mechanical-refresh/implementation/02-test-evidence.md) and [manifest](../notes/rephase-1-mechanical-refresh/implementation/manifest.json).
5. [Candidate patch](../notes/rephase-1-mechanical-refresh/implementation/logs/r1-candidate.patch) — Worker reports basis `a1a4242..afd925d`, seven files, SHA-256 `eccb85fd1eba8a61cae0839414040fe42ffea1c716eae216be5be747edb0574d`. Root has not verified that hash/diff or reviewed candidate source yet. `logs/` contains 19 saved files including development failures and final/affected test logs.

The manifest's `candidate_head`/`candidate_branch` describe the **source e4c8269**; `successor_head` and `fixture_branch` describe R1. Do not mistake those fields for a single tested head. Standalone database recovery/complete changed-file-copy packaging has not been established by this pause inventory; keep the fixture and patch.

## Worker-reported outcomes — not yet root-accepted

General reports 14 dedicated methods (742.117 s), 25 revalidation methods (47.570 s), and affected groups 35 + 5 + 8 + 12, all final runs successful/no skips. Earlier implementation/fixture failures are listed in the report. Root has only read the report/manifest at this stop, **not** audited raw log identity binding, exact exits, coverage, failure oracles or the complete diff. Do not promote the manifest's broad `all_runs: 0` summary into a clean development history or an exact-head/full-CI claim.

Candidate work reportedly implements the selected four runtime paths, two test paths and runbook. The accepted contract, not the Worker summary, determines what must be checked: strict public Gate/receipt replay, prior effective authority, same-byte/criteria guards, complete old receipt+Gate retention, exclusive guard, revalidation ownership, conflict-safe restoration, and no post-commit rollback.

## Procedure/evidence questions already visible

- Worker inventory line 13 explicitly records **`--no-verify`** for its basis commit despite the no-hook-bypass instruction; the Worker return summary said no hook bypass. Treat this as a disclosed instruction deviation/contradiction requiring clarification, not as approved or silently clean. Do not amend or recreate history to hide it.
- The source archive attempt hit known promisor-missing objects and was replaced by worktree-copy/new-DB preparation. Raw failure and 41-file inventory are partly described as shell-history-only. Scope, available durable evidence and any recovery limitations must be assessed explicitly.
- One shell-Python edit is disclosed by the Worker despite the dedicated-editing requirement. Preserve attribution and facts; it does not itself prove runtime correctness or incorrectness.
- New basis, tests' exact-head binding, packet byte/hash completeness and requested failure cases remain unreviewed. Stop is not a judgment that all selected contract tests are covered.

## First action after Human resumes

1. Read this pause record and the selected contract. Recheck reconstruct/fixture status without resetting, cleaning, checking out, or rerunning saved scripts. Preserve new Human edits.
2. Astra reviews actual seven-path diff and raw test evidence, starting with basis/content identity and the procedure contradictions above. Request bounded evidence completion or source/test corrections from General as needed. Root remains reviewer, not implementer/test runner.
3. Only after source/oracle/evidence correction and exact candidate fixation, commission a fresh author-independent scoped implementation review. No prior CLI/B/witness PASS automatically transfers to this new Git basis/head. Do not redo successful tests solely because a chat paused.

Whole candidate remains **NOT_READY**, step 4/B3 OPEN, canonical seven-point audit unstarted. Bootstrap limitation (R1-installed receipt baselines), noncooperating-writer/global-CAS/crash limits and all separate Profile/build/DM/findings dispositions remain. Ordinary reconstruct Commit/Push is Human-owned.
