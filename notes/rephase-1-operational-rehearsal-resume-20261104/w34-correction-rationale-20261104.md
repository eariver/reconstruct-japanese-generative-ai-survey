# W34 corrected input DATA — author rationale (proposal, not review)

2026-11-04. W34 DATA proposal author (NOT reviewer/root). Human continued active rehearsal; no reconstruct Commit readback. Bounds: `notes/rephase-1-operational-rehearsal-resume-20261104/README.md`, `astra-resume-resolution.md` FULL, `current-observation.md/json`, reviews `w34-evidence-authority-consumption-review-20261104.md` + `correction-addendum-20261104.md` + `decision-map-20261104.json`. Active instance `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work` (e84 over 48082356). No active writes/staging/disposition, no execution/import/tests/network/Production checkout/reconstruct Git/readback; no `git -C .`; no source/State/CP/gate changes; no subagents. New packet DATA only; original inputs/products preserved.

## 1. What this proposes

- NEW complete 409-record input: `w34-corrected-input-20261104.json` 1575840B `5e53a179ea49ac0f3ea190cf2e9fc7e77f69aa1d3c1f504d84971a5a9ac2bfe2` (base `3ffc6e31...` 1573186B, +2654B). 409/409 records, 409 unique IDs. Exactly 8 DIDs altered; 401 byte-identical (JSON compare). No all-49 downgrade.
- Exact delta: `w34-corrected-delta-20261104.json` (full hashes, altered DID/target/key map, before/after).
- Supplement unchanged: `evidence-authority-supplement-r2-fresh-basis.json` 389414B `ce6f977a...` (428 bindings / 425 distinct, 428/428 verified). No new supplement; input scope excludes uncaptured shells by removing those `supplement-src` IDs from `source_bindings` only. No IDs invented, no fetch.
- Schema: `AUTHOR_CLAIM` is supported (`evidence-v2-card.schema.json:148`, `evidence-card.schema.json:85/103/117`, `dm022-revision-request:120` enum includes `AUTHOR_CLAIM`). c055 `PRIMARY_FACT -> AUTHOR_CLAIM` needs no schema change.

## 2. Per-DID corrections (reviewer/root-justified only)

- **c002** — remove `ordinary-window X discussion corroborates timing`. Keep content VERIFIED (Anthropic 190678B `ab2187dc...` date-only). Chronology residual explicit (Aug 14 vs 22:00Z); X is lead only. No upgrade.
- **c006** — feed-only binding. Remove shell `supplement-src-6f7270b995d12409` (281297B `208418d8...` JS shell, captured-but-unconsumed, not failed fetch) from `source_bindings`; keep feed `4d2cb3db49666f68` (1696769B `f92f4cef...` `dateAdded 2026-08-17` internal). Claims already feed-worded; limitation reworded to captured-but-unconsumed. VERIFIED feed-only stands.
- **c020** — add missing boundary limitation (Aug 14 date-only `article:published_time` + byline vs 22:00Z). Content VERIFIED stands (737786B `18ecbb55...`); residual explicit for Selection; no clock upgrade.
- **c039** — remove unbound `observable via separately captured community artifacts` (single binding only). Keep content VERIFIED (347654B `af949d0053...` date-only). Hold Aug 14 vs 22:00Z residual; no community timing claim.
- **c055** — researcher-only `AUTHOR_CLAIM`; exclude MSRC shell corroboration; vendor scope UNRESOLVED. `source_bindings` → Varonis only `d0c044832ca72006` (265189B `ea8c922e...`); remove MSRC `1ed7511b4105f0bd` (2717B `3bd2718a...` shell). Claim-3 `PRIMARY_FACT -> AUTHOR_CLAIM` researcher-only; contexts state no MSRC citation. Verification split: researcher chain VERIFIED / vendor corroboration UNRESOLVED (remove `with CVE-ID vendor corroboration`). Overall stays PARTIAL (correct). Existing Varonis capture suffices; MSRC/NVD listed only as optional if vendor wording later load-bearing.
- **c065** — unsupported preview verification `VERIFIED -> UNRESOLVED`; overall stays PARTIAL HOLD (correct). Discussion-existence as `SOCIAL_OBSERVATION` preserved; preview/traffic specs UNRESOLVED without first-party artifact; Aug 26 attribution excluded. `src-1` suffices for HOLD.
- **c096** — verified-entry vs unproven scope split. Verification 1→2: entry (read/search/prepare/send + approval-by-default in Aug 20 notes, 719962B shared) VERIFIED / Apple-silicon/Work-Codex scope UNRESOLVED. Record stays VERIFIED with scope residual; no scope upgrade.
- **c066** — wording must not imply X proves primary timing. Claim-2 `official X` → `X`; context `exact authority` → `lead only, not primary authority`. Limitations/verification split: plan-list content VERIFIED vs Aug 21 timing UNRESOLVED (X lead + secondary only, page re-dated Aug 26 never cited as Aug 21 authority). Materiality rationale `corroborated by X` removed. No week-eligibility upgrade from X. Existing capture suffices; no new primary-date fetch authorized.

Split chronology clauses are explicit (`VERIFIED content + UNRESOLVED timing/scope residual`) without upgrading week eligibility in any DID.

## 3. What is deliberately unchanged

- Legitimate VERIFIED preserved; 401 records identical. No blanket downgrade.
- `weekly:carry-over` SATISFIED stays (1 rechecked MiniMax, DROP C076/C077 recorded, 0 Evidence tasks required; future Selection exclusion explanation does not retroactively unsatisfy).
- Counts clarified only: 369 accepted-root / 439 effective = 434 event + 5 accounting / 409 non-DROP (439−30). Never sum root+effective. No file correction for counts.
- Supplement bindings unchanged except the two scope exclusions above; supplement Raws preserved.

## 4. Missing material

None indispensable for this proposal. Optional only if load-bearing (root decides, no fetch here): MSRC/NVD for c055/c006 vendor wording; Help Center scoped URL for c096; OpenRouter rankings versioned for c065.

## 5. Preservation and next

Original active input/supplement/accepted Evidence `450b508c...`/Views `5ad0a6ac...`/Ledger `76ac53f9...`/Completeness `93dbefae...`/States/profiles/checkpoints/old480/bd80/reviews preserved untouched. No State/Profile/CP/source/test/config writes; no disposition executed. Ready for independent review. After approval: NEW proposed-input version via normal strict facades (never overwrite `bf208f96.../f744e46b...`), normal Evidence/Views/Ledger/Completeness re-run with fail-closed guards, preserve old runs + State, then independent re-review before `EVIDENCE_REVIEWED`. No Selection/Architecture/Draft/PDF/R4 now. WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN. Human Commit Point — stop.
