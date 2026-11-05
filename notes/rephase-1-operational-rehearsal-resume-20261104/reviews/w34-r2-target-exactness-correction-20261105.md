# W34 r2 target-exactness correction — runtime exactness over schema possibility (no execution)

**Role:** General independent supervisory reviewer (NOT author/root/operator, NOT Sol/Luna/Human). Data/source-read only.
**Preserves:** prior `w34-r2-proposal-final-review-20261104.md` + map as **original wrong PASS** (history; this corrects it, does not edit it). Prior called 1→2 splits valid because schema allows arrays — **wrong**: `_build_card_core` enforces exact task-target coverage, and r3 run actually rejected c001 on that exact check. Acknowledged here.
**Read (source/data only):** r3 failure `../w34-dispose-run-execution-report-20261105T003915Z.md` FULL + `../w34-dispose-run-stderr-20261105T003915Z.txt` (c001 exact-target error + FAILURE.json path bug), retained package source `survey_evidence_v2.py` `_build_card_core` exact-match block (source-read, no import/run), e84 tasks (409 `verification_targets`), base input `3ffc6e31…`, r2 input `1ea56297…`, supplement `ce6f977a…`, retention/live State (data-only). No active writes/runtime imports/network/Production/reconstruct Git/readback, no subagents, no input authoring, no new fetches.
**Machine:** `w34-r2-target-exactness-correction-map-20261105.json` (generated; all 409 target names vs r2 + required single-target fixes).
**State/gates/products:** live State `7e6a50c2…` CANDIDATES_NORMALIZED pending/null unchanged; exact2 both absent live, backups safe (`76ac53f9…` 186202B + `93dbefae…` 71532B, manifest `c9cf925b…` readback-verified, data-only). **No accepted new products exist** (run stopped before any Evidence accept); no claim otherwise.

## 1. Schema-vs-runtime gap (acknowledged)

Schema (`evidence-v2-card.schema.json`, `evidence-card.schema.json`) allows `verification.targets[]` with `VERIFIED|UNRESOLVED|...` — splits are schema-valid. **Runtime is stricter:** `_build_card_core` builds `verification_map={row[target]:row}` from the record and requires `set(verification_map)==set(expected_targets)` where `expected_targets=list(task.verification_targets)` (screening-task bound), else `ValueError: verification input must cover exact task targets`. Pre-disposal `validate_interactive_input` checks only ids/bindings, so the mismatch surfaced mid-run at c001 (first failure, STOP). Prior review missed this layer. Criterion going forward is **runtime exactness**, not schema possibility.

## 2. Necessary criterion (Root: no new source/schema/Screening rewrites)

Keep **original single target strings exactly** as in tasks/base input (listed in map). Do NOT invent split targets. Express proven subclaims + chronology/scope/vendor limitations in `finding` + `limitations` + `materiality_rationale` text. Set single-target `status=UNRESOLVED` when the original **compound** target (content + W34 placement/vendor/scope as written) is not fully established; keep `VERIFIED` only when the single target as written is fully established. Overall `status`: `PARTIAL` (or HOLD/NEEDS_MORE as before) when any load-bearing element of the single target is UNRESOLVED; `VERIFIED` only when the single target + MATERIAL + MAIN_EVENT week claim is fully established. Proven content stays **described** in findings (not erased) but must not be labelled full-VERIFIED target when the compound is unresolved. No new fetch, no Screening re-targeting.

## 3. Required fixes (14 mismatched DIDs; other 395 match, no change)

- **c001/c002/c020/c022/c024/c039/c045/c066/c099/c100/c101/c102:** revert 1→2 splits to the single original task target string (exact text in map), `status=UNRESOLVED` (timing/entry-dating load-bearing unresolved: Aug14/Aug21 date-only vs 22Z side, Sep8 capture+context, Aug21 listing observed-not-captured, Aug21 Cloud addition), finding = proven content description (body-supported, with byte sizes where already established) + explicit UNRESOLVED timing clause + no-upgrade clause, limitations preserved + timing residual, overall `PARTIAL` (c024 PARTIAL CONTEXT, c001 PARTIAL CONTEXT stays). Claims/binding/limitations wording from r2 otherwise preserved (no new fetch).
- **c055:** revert 1→2 split to single original target `One-click chain ... Distinguish Copilot Personal from Microsoft 365 Copilot.` `status=VERIFIED` (researcher chain proven via Varonis 265189B; vendor corroboration was never in the target string — it lives in findings/limitations). Keep r2 claims (`AUTHOR_CLAIM` researcher-only, MSRC uncited), single-source binding (Varonis only; shell retained uncited in supplement, legally retained per prior binding analysis), limitations (shell captured-but-unconsumed, no corroboration), overall `PARTIAL` (as original/r2). No new vendor target invented.
- **c096:** revert 1→2 split to single original target `Apple-silicon macOS plugin ... approval by default.` `status=VERIFIED` (entry content proven in Aug20 notes 719962B; scope restriction was never in the target string — it lives in limitations). Keep single binding, limitations (scope UNRESOLVED residual), overall `VERIFIED` (entry load-bearing; scope not in target). No new scope target invented.
- **c006/c065 + other 395:** no target change (already exact). c006 VERIFIED feed-only stands (Aug17 internal); c065 single UNRESOLVED HOLD stands.

Full 409 target-name comparison + exact original strings + r2 strings + required single-target status/overall in machine map. New author r3 pending; don't author input here.

## 4. Disposition / run status

Exact2 absent live with safe backups verified data-only (hashes above); old State/gates unchanged CAND/pending; no new accepted products (run stopped pre-accept). Next requires: (a) new r3 input implementing §3 single-target fixes (never overwrite accepted dirs), (b) fix FAILURE.json relative→absolute path bug noted in report, (c) new bounded observation/decision for already-removed exact2 (backups preserved, no auto-restore), (d) independent re-review before any new dispose/run auth. No State advance, no Selection, no SP inference.

Attribution: General independent supervisory reviewer. WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN.

(End — 2026-11-05.)
