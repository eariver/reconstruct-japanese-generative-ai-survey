# R1×2→editorial→renewal anchor — NEW attempt (no overwrite old blocker)

2026-10-25. Anchor DB `versioned-renewal-r1-anchor-20261025T150000Z/anchor-weekly`. Reconstruct `f84fcf5` clean. No candidate/reconstruct commits, no network/old-runner exec/cleanup. All reviews/Preview synthetic, no genuine approval.

## 1. Old 721 clone (complete, no E)

- SRC R7b `jgas-editorial-r7b…/candidate-partial-b40de60` HEAD `721a04d`, tree `ac7cb0bd`, manifest 721 incl `.latexmkrc 18199fd8…`.
- DST `anchor-weekly` HEAD `721a04d`, 721 files, status clean, `.git` isolation (no alternates, inert `example.invalid`, `dev:ino` disjoint, `nlink==1`), no `GIT_*`.
- Evidence: `make_721_clone…sh` DONE OK, `dst-head/tree/count/status/isolation/noalternates/config/env-check` all exit 0.

## 2. Canonical Weekly VALIDATED (old 721 test library, fresh child)

- Used SOURCE `tests.test_survey_editorial_correction_proposal_v2._new_weekly_helper/_build_weekly_validated` (old 721 code, PYTHONPATH=fix, cwd=fix, no 740 caching).
- HEAD stays `721a04d`, status `??` 93 E (new edition, no tracked mods). Artifacts: `production-state.json ad2d207c…`, `validated-source-manifest 8971e7d7…`, `reader-manuscript 345c589b…`, `reader-surface-gate 60c10876…`, `main.pdf b3e44df8…` (blank pypdf initial, allowed for initial canonical; real TL required only for editorial R3 once).
- Monotonic dt 12.1s, synthetic reviews, PID/heartbeat recorded. No commit (E untracked, correct).

## 3. R1×2 PUBLIC (weekly_derivation only, no --allow-empty)

- R1a commit `fc9a543…` + CLI `refresh-mechanical-evidence --reason "R1 anchor refresh 1" --recorded-at 2026-10-25T15:10:00Z` exit 0 → `r1.json`.
- R1b commit `36c679cc…` + CLI `--reason "R1 anchor refresh 2" --recorded-at 2026-10-25T15:20:00Z` exit 0 → `r2.json`.
- Verified `r1+r2` exactly, `r2.supersedes` → r1, `prior_checkpoint` DRAFT_COMPLETE, no fake shape. HEAD `36c679cc`, tree recorded, E preserved (retention `.mechanical-refresh-retention/…`). PUBLIC, not fabricated. Fresh subprocess per R1 (PYTHONPATH=fix), `.latexmkrc` present (old 721 fix, no new helper patch needed — used exact source clone).

## 4. Editorial R3 (old 721, P3S50, real TL once)

- Proposal `wk-anchor-ed3` (previous ed1/ed2 partials preserved, new id no takeover): headline `Weekly tested method, revised anchor edition`, deck synthetic, 3 paras incl exact `The accepted source authors describe the tested method.` Changed reader, Weekly envelope.
- P1 `prepare_proposal` + `validate REVIEW_REQUIRED` exit 0. P2R capture/verify `CAPTURED/VERIFIED`. Scope synthetic `WITHIN_APPROVED_AUTHORITY`. P2V `CURRENT_BASIS_OBSERVED_SCOPE_BOUND`. P3S50 materialize/verify `STAGED_SOURCE_REPLAY_VERIFIED`, `code_deps 50` (old code preserved, new P3S fix NOT applied to old epoch).
- Real TL2026 `lualatex+biber` at `/tmp/opencode/jgas-texlive…` (existing local tools, read-only): `prepare_publication` dt recorded, `main.pdf` 5 pages 62865B SHA `17132182…`, `main.log` 92972B, not fake blank (>5000B). QA deterministic (3 checks) + synthetic semantic/visual via actual `reader_pub.build_review_record` (synthetic reviewer, no genuine approval).
- Finalize + `validate_prepared_set` + `activate_publication` exit 0 → `r3.json`. Verified `r3.supersedes r2.json SHA 27db45ce…`, `canonical_anchor LEGACY_REVALIDATION ref r2.json` (anchor r2, no rollover). State `VALIDATED_DRAFT`, Preview pending, strict `validate_agent_state` healthy (recorded in helper, not reproduced here). No source commit for editorial (tool epoch unchanged since R1b).

## 5. Overlay 740 (OWN source commit, preserve E)

- SRC740 archive `versioned-renewal-archive-input-…/snapshot-work` HEAD `409b292`, 740 files `4e2783fb…`.
- Copied 740 files (no `rsync` blind, SHA verified), `git add -- <740 paths>` only (E stays `??` 213 lines), commit `5950e0f…` message `TEST-ONLY: overlay 740 SOURCE before renewal U, E preserved` (parent `36c679c`). Verified `ls-files` subset 740/740 missing 0 (total 740, R7b DB has no 32155 bulk), E preserved untracked. Old P3S50 record (50 deps) untouched; new current controls full 740 tracked except E.

## 6. Renewal U same-reader (new 740 tools, fresh child) — PRECISE FAILURE (not proven)

- Prepare `high-u1-anchor-weekly` REUSE_TARGETS (mspec ed3, toolchain None) exit 0 → `basis_path …/renewals/high-u1-anchor-weekly/renewal-basis.json`.
- Fresh checks from ed3 deterministic-checks (re-inspected live bytes) → `renewal-u-fresh-checks.json`.
- Finalize exit 0 → keys `build_record_path/bundle_path/candidate_path/disposition/gate_path/proof_path/receipt_path/set_path` (new code uses `_path` suffix, not bare `receipt` — matches source_phase_s shape, not a block).
- Activate exit 2 INDETERMINATE: `post-activation State invalid (preserved, no rollback): active publication selection invalid for revalidation agreement: selection recorded anchor must equal chain-derived identity; Stage Checkpoint artifact drift: reader-surface-gate`.
- Preserved incomplete `r4.json` SHA `9b69edd8…`, `supersedes r3.json SHA 7dce79ac…` (good, supersedes editorial), `canonical_anchor LEGACY_REVALIDATION ref DRAFT_COMPLETE.json SHA ffbde649…` (original checkpoint, NOT r2 — needs root triage vs expected r2). State now points to `r4.json` (INDETERMINATE preserved, no rollback/adoption/deletion). No duplicate failure writer (first failure preserved).
- Renewal basis/proof/history/current-State: basis/proof exist under `…/renewals/high-u1-anchor-weekly/`, history NOT verified (activate failed before history). Current State strict check NOT passed (INDETERMINATE). Fresh Python per new epoch (PYTHONPATH=fix at 5950e0f), no old caching. Clock monotonic recorded, synthetic `recorded_at` separate.

## 7. R1-after-versioned refusal — PASS (no writes)

- Public `refresh-mechanical-evidence` after versioned (State points to incomplete r4) exit 2: `R1 mechanical refresh refused in VERSIONED_ACTIVE/invalid mode before any write: canonical operation refused in revised mode (use versioned editorial operation) (versioned renewal unselected §10; no editorial-reason bypass)`.
- Verified no new `r5`, records still `r1+r2+r3+r4`, HEAD stays `5950e0f`. No writes. Required oracle proven.

## 8. Anchor fields / code ids / temp status

- `old_source 721a04d85532d7855f3e54cc411f5847c787726e`, `old_tree ac7cb0bd…`, `R1a fc9a543…`, `R1b 36c679cc…`, `r2 SHA 27db45ce…`, `r3 SHA 7dce79ac…` (supersedes r2, anchor r2), `real PDF 5p 62865B 17132182…`, `overlay 5950e0f…` (parent 36c679c, 740 tracked, E 213 untracked), `renewal basis/proof high-u1-anchor-weekly/`, `r4 SHA 9b69edd8…` (supersedes r3, anchor DRAFT_COMPLETE ffbde649… — triage vs r2), `State → r4 INDETERMINATE preserved`.
- Code ids: R1 `survey_agent_control_v2.refresh-mechanical-evidence`, editorial `proposal_mod.prepare_proposal/validate`, `retention.capture/verify`, `observer.observe_current_authority SCOPE_BOUND`, `staged.materialize/verify 50`, `edpub.prepare (real TL lualatex+biber)/finalize/validate_prepared_set/activate`, renewal `high.prepare REUSE_TARGETS/finalize/activate/verify_history`, `agent.validate_agent_state` (strict, prePreview/Exception window per precode §6).
- Temp: workspace `…/r1-anchor-…/tmp`, fresh child per step, PID/heartbeat files (`validated.pid/heartbeat`, `r1x2.pid/heartbeat`, `editorial.pid/heartbeat`, `renewal-u.pid/heartbeat`), terminal guards 600–1500s, no duplicate failure writes, no `/tmp` writes except read-only TL binaries, no GIT sharing, no candidate/reconstruct mutation.

**Conclusion:** R1×2 PUBLIC + editorial R3 with real PDF + anchor r2 + overlay 740 + R1-refusal PROVEN. Renewal U NOT proven — precise INDETERMINATE (gate drift + anchor identity). Do NOT declare full anchor proven. Root to triage renewal gate/anchor (reader-surface-gate drift under new schema? anchor DRAFT_COMPLETE vs r2?) before retry. No whole-unit/independent PASS, no CommitPoint.
