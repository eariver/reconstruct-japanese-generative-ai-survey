# W34 corrected-input delta review — narrow PROPOSAL check (no execution)

**Role:** General independent supervisory reviewer (NOT author/root/operator, NOT Sol/Luna/Human). Source/data-read only.
**Preserves:** original `w34-evidence-authority-consumption-review-20261104.md` + machine, `correction-addendum-20261104.md` + `decision-map-20261104.json` (history; this is a new delta review, not an edit).
**Read:** `../w34-corrected-input-20261104.json` (1575840B `5e53a179ea49ac0f3ea190cf2e9fc7e77f69aa1d3c1f504d84971a5a9ac2bfe2`), `../w34-corrected-delta-20261104.json` (`c55395774e075f4ce2db1d14e10fe39dcee6f0281c3938a5c3b6dde80c34d46e` 19856B), `../w34-correction-rationale-20261104.md` (`92d02d34ec8aacc82e742efd4714ffc4492fb5e7c76f6cd2ce64b061604432b9` 6212B), `../w34-owned-output-disposition-candidate-20261104.json` (`8955707950c71f6b7165b315151850a1e6639aa06af8256559607e5de9d90080` 10204B, ownership mapping only), base e84 `sources/2026-W34/evidence/proposed-input/interactive-evidence.json` (1573186B `3ffc6e310e389bf03275b7ac7df0b029e43acec5f6140cc3a5bd56f8a4794f27`), supplement `ce6f977a…` 389414B, schemas + `survey_evidence_v2.py` / `run_evidence_v2_interactive.py` (binding/card semantics, source-read only), captured Raws as needed. No network/Production checkout/reconstruct Git/readback (`git -C .` never run), no imports/runtime/tests/build/fixtures, no State/source/product writes, no subagents, no revised-input authoring, no new fetches.
**Machine:** `w34-corrected-proposal-delta-decision-map-20261104.json` (generated full hashes; authority for bytes).
**Verdict: narrow `CHANGES_REQUIRED` before any execution** (smallest blockers §4; no blanket rejection, no new fetch, no execution approved).

## 1. Delta exactly as claimed (8/409, 401 identical)

JSON compare original vs corrected: 409/409 records, 409 unique IDs, exactly 8 DIDs differ (`c002,c006,c020,c039,c055,c065,c066,c096`); other 401 byte-identical. Bytes +2654B (1573186→1575840), SHA `3ffc6e31…` → `5e53a179ea49ac0f3ea190cf2e9fc7e77f69aa1d3c1f504d84971a5a9ac2bfe2` verified by re-hash. Carry-over SATISFIED unchanged, counts wording fixed (369 root / 439=434+5 / 409, never summed). No all-49 downgrade.

## 2. Schema/enum/target-ID/card semantics for splits

- `AUTHOR_CLAIM` supported: `evidence-v2-card.schema.json:148`, `evidence-card.schema.json:85/103/117` enum includes `AUTHOR_CLAIM`; c055 `PRIMARY_FACT→AUTHOR_CLAIM` needs no schema change — confirmed from e84 schema bytes.
- Verification arrays: schema allows `targets[]` with `status ∈ {VERIFIED,UNRESOLVED,CONTRADICTED,NOT_APPLICABLE}`; 1→2 splits for c055/c066/c096 are schema-valid (no uniqueness bar on target text). Interactive input verification has no `subject_ids/source_ids` (output-card-only); splits carry `target/status/finding` only — valid.
- **Semantics not assumed:** code validates structure only (`_validate_card_core` checks refs/enums, no overall-vs-targets linkage). Overall `VERIFIED` with an `UNRESOLVED` component is schema-valid but **semantically sound only if the unresolved component is not load-bearing for the MATERIAL/W34 claim**. c055 PARTIAL with researcher-VERIFIED + vendor-UNRESOLVED is sound (overall PARTIAL reflects unresolved). c096 VERIFIED with entry-VERIFIED + scope-UNRESOLVED is sound **only** because scope is not in claims (entry-only MATERIAL). c066 VERIFIED with plan-VERIFIED + timing-UNRESOLVED is **unsound** for MATERIAL W34 (timing is week eligibility) — overall must be PARTIAL (see §4).

## 3. Supplement/task binding — retained full supplement is legal, no new supplement needed

Author removed `supplement-src-6f7270b995d12409` (c006 shell 281297B) + `supplement-src-1ed7511b4105f0bd` (c055 MSRC 2717B) from input `source_bindings` only; supplement file retains all 428/425 Raws unchanged (`ce6f977a…`, 428/428 verified).

Source-read (e84): interactive input requires `set(bindings).issubset(allowed)` where `allowed` = task-bound Discovery + supplement IDs — subset allowed, so input binding 426/428 is valid. Package requires `set(bound)==set(supplement_entries)` **for tasks** (`authority_supplement_source_ids` in package tasks, still 428/428 since tasks unchanged) — still exact. Cards require card sources ⊆ task-bound allowed sources — citing subset (feed/Varonis only) is valid. Shells remain captured-but-unconsumed in supplement/tasks, uncited by cards — legally retained, no per-task exactness fail, no pruned supplement required. Existing capture suffices; no indispensable new material on binding.

## 4. Chronology vs content — smallest blockers (no VERIFIED event-in-week with unresolved timing)

Window UTC `[2026-08-14T22:00Z,2026-08-21T22:00Z)`. Content VERIFIED stands where body supports it; timing residual must be explicit and must not be relabelled as week-established. `window_relation MAIN_EVENT` + `MATERIAL` + overall `VERIFIED` together imply W34 event — with unresolved boundary timing this is unsound.

**Author splits done right:** c055 (PARTIAL, vendor UNRESOLVED), c065 (PARTIAL HOLD, preview UNRESOLVED), c096 (entry VERIFIED / scope UNRESOLVED — scope not in claims, overall VERIFIED sound for entry).

**Blockers (narrow, exact wording fix, no new fetch):**

1. **c066 overall VERIFIED → PARTIAL.** Plan-list VERIFIED / timing UNRESOLVED split is correct, but MATERIAL W34 requires Aug21 timing. Timing rests only on DailyX X `2026-08-21T17:29:36Z` lead + secondary (page re-dated Aug26 never cited — correct). X is lead only, not primary date. With timing UNRESOLVED, `VERIFIED MATERIAL MAIN_EVENT` relabels unresolved timing as event-in-week. Fix: keep targets split, change overall `VERIFIED→PARTIAL` (materiality stays MATERIAL, window stays MAIN_EVENT as asserted-but-residual). Existing 184728B `793b387e874aa6240b829bc2a686490e719f7c1ceb9a5e8a938915366b70b8c8` suffices; no new primary-date fetch authorized here.
2. **c002/c020/c039 single VERIFIED with residual note → split + overall PARTIAL.** Each holds Aug14 date-only vs 22Z start as residual note but keeps single `VERIFIED` target + overall `VERIFIED MATERIAL MAIN_EVENT`. Date-only boundary cannot prove 22Z side; single VERIFIED relabels it. Fix: split into (content VERIFIED / timing UNRESOLVED) like c066, overall →PARTIAL, preserve limits (c002 190678B `ab2187dc…`, c020 737786B `18ecbb55…`, c039 347654B `af949d0053d384603e928f85f2523fc3b84715c788281e03a72d85dcf4243654`). Existing captures suffice.
3. **c022/c045 not in proposal but same boundary defect → must be included.** c022 `Date: 2026-08-21` (48149B `9f0e83b2…`) + c045 `Aug 21` badge (488098B `c790515d…`) remain single VERIFIED MATERIAL MAIN_EVENT with no timing split/residual. Fix: same split (content VERIFIED / Aug21 vs 22Z UNRESOLVED) + overall PARTIAL. No new fetch.
- c006 feed-only VERIFIED (Aug17 internal `dateAdded 2026-08-17`, no clock needed), c096 entry-VERIFIED/scope-residual, c001 PARTIAL, c024 CONTEXT, and unaffected 31 DIDs are PROPOSAL_READY as worded (content vs residual separated, no week upgrade).

Carry-over SATISFIED stands (1 rechecked MiniMax, C076/C077 DROP recorded, 0 Evidence tasks required; future Selection explanation does not retroactively unsatisfy).

## 5. W34 exact2 disposition candidate — ownership only, no execution approval

Mapping (`89557079…` 10204B) correctly scopes exact2 unaccepted CAND-owned files: `materiality-ledger-v2.json` 186202B `76ac53f90f3c731c5819ab73ae3fcfd4451f7d5030795232e80e02ebac2aca4b` + `profile-completeness-v2.json` 71532B `93dbefae96ee0acddf5a13125dac6d28a25c3ef3e1d4decaf61d766356c57bfb`, State CAND/pending/null, 2 checkpoints, no Gates, Contract8/Profile/DCP/SCP pins recorded, accepted dirs preserved, retention packet-local, guarded unlink + readiness + no-restore/no-force/no-weakening, SP plan not authorizing W34. Ownership/gap-check useful; **do not approve** unreviewed execution harness/retention-namespace liveness, and infer no SP authorization. Disposition requires its own bounded Astra authorization after corrected-input approval + fresh re-review; no REQUEST_CHANGES/rollback/reinit.

## 6. Verdict + smallest path

**`CHANGES_REQUIRED` (narrow):** apply §4 overall→PARTIAL + split fixes for c002/c020/c039/c066 (+ include c022/c045 same pattern) as a new DATA revision of the corrected input (never overwrite accepted `bf208f96…/f744e46b…`); keep supplement identical (legal retention §3); keep carry-over/counts/unaffected scopes. Then normal strict-facade re-run (new proposed-input file, new Evidence/Views/Ledger/Completeness via public APIs, fail-closed guards, preserve old runs/State) + fresh independent re-review before `EVIDENCE_REVIEWED`. No Selection/Architecture/Draft/PDF/R4 now. Historical 41/7/12pp reference only.

Attribution: General independent supervisory reviewer. No Sol/Astra/Human. May be cited by existing `AGENT_RESEARCH` only. No new Gate/schema/State advance, no fake PASS/R4/savings. WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN.

(End — 2026-11-04.)
