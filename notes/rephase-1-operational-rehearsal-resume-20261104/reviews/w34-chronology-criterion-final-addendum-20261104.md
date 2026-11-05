# W34 final chronology criterion — short addendum (Root §3)

**Role:** General independent supervisory reviewer (NOT author/root/operator, NOT Sol/Luna/Human). Source/data-read only.
**Preserves:** original review + correction addendum + decision map + delta review + delta map as history (reversals preserved; this does not edit them).
**Read:** `../astra-resume-resolution.md` §3 FULL, Profile window, all flagged record fields below from e84 + corrected proposal (source-read only, no new fetch). No network/Production/reconstruct Git/readback, no imports/runtime/tests/build, no State/source writes, no subagents, no input authoring.
**Machine:** `w34-chronology-criterion-final-map-20261104.json` (generated full hashes).
**Clarification:** prior `PROCEED_WITH_RESIDUALS_TO_SELECTION_PREP` / `CONTENT_VERIFIED_WITH_RESIDUALS` wording was reviewer shorthand, **not** stage authorization. Status remains `CHANGES_REQUIRED` until corrected acceptance is re-run and independently re-reviewed. No advance to `EVIDENCE_REVIEWED`/Selection approved here.

## Uniform criterion (Profile/window + record fields, no invented linkage)

Profile `ROLLING_WINDOW 2026-08-14T18:00-04:00` to `2026-08-21T18:00-04:00` = UTC `[2026-08-14T22:00Z, 2026-08-21T22:00Z)`. No schema rule links overall `status` to verification `targets[]` status in code (checked `survey_evidence_v2.py` `_validate_card_core`); criterion is semantic, not schema-enforced:

- `window_relation MAIN_EVENT` + `materiality MATERIAL/CONTEXT` + overall `VERIFIED` together assert a week-eligible event. If the record's own claims/verification-target/materiality-rationale explicitly assert a **boundary date** (Aug14/Aug21 date-only without clock, or Sep8 capture-date + context) **as the W34 placement**, and that precision cannot decide the 22Z side, timing is load-bearing → overall must be `PARTIAL` (split content-VERIFIED / timing-UNRESOLVED). Date-only on unambiguously internal dates (Aug15–20, e.g., Aug17 feed `dateAdded`, Aug18 entry/first-observation, Aug20 bundle) needs no clock; Last-Modified/capture/sitemap/observed_at are never publication time and are not demanded.
- `MATERIAL` alone does not prove timing; content-VERIFIED alone does not prove week eligibility. Do not downgrade content that is body-supported; do not keep overall VERIFIED where timing is load-bearing and unresolved.

## Final table (all already-flagged chronology DIDs)

| DID | Record asserts week date? | Required aggregate | Target split | Exact unresolved aspect | Claim unchanged vs narrow |
|---|---|---|---|---|---|
| c002 VERIFIED MATERIAL MAIN_EVENT | Yes: claims Aug14 article + target “Exact Aug14 vs 22Z remains residual” VERIFIED | **PARTIAL** (reverses addendum keep-VERIFIED) | content VERIFIED / timing UNRESOLVED | Aug14 date-only vs 22:00Z start side | claims unchanged; target must split, remove single-VERIFIED-with-residual |
| c004 VERIFIED MATERIAL MAIN_EVENT | No: claims no date; target content-only; timing Aug18 first-observation internal | **VERIFIED remains** | single content VERIFIED (no split needed) | Aug18 internal vs 22Z not at edge; residual note suffices | unchanged; reason VERIFIED: no boundary assertion, internal date sufficient |
| c020 VERIFIED MATERIAL MAIN_EVENT | Yes: “Pika’s Aug14 page…” + target “family-level Aug14 page is boundary” VERIFIED | **PARTIAL** | content VERIFIED / timing UNRESOLVED | Aug14 date-only vs 22Z start side | claims unchanged; add split (already has limitation) |
| c022 VERIFIED MATERIAL MAIN_EVENT | Yes: “entry dated 2026-08-21 releases…” + target confirms release (no timing split) | **PARTIAL** (not in 8-proposal; must include) | content VERIFIED / timing UNRESOLVED | Aug21 date-only vs 22Z end side | claims unchanged; add timing target UNRESOLVED |
| c024 VERIFIED CONTEXT MAIN_EVENT | Yes: “Clean W34 distribution delta…” VERIFIED with Aug21 corroboration observed-not-captured | **PARTIAL CONTEXT** | content VERIFIED / listing-date UNRESOLVED | Aug21 listing version date precision (observed, not captured) | claims unchanged; split required |
| c039 VERIFIED MATERIAL MAIN_EVENT | Yes: “News 2026-08-14…” + target date-confirmed VERIFIED | **PARTIAL** | content VERIFIED / timing UNRESOLVED | Aug14 date-only vs 22Z start side | claims unchanged; already removed unbound clause, add split |
| c045 VERIFIED MATERIAL MAIN_EVENT | Yes: “Aug21 feature…” + target confirms Aug21 delta VERIFIED | **PARTIAL** (not in 8-proposal; must include) | content VERIFIED / timing UNRESOLVED | Aug21 badge date-only vs 22Z end side | claims unchanged; add timing target UNRESOLVED |
| c066 VERIFIED MATERIAL MAIN_EVENT | Split already: plan VERIFIED / timing UNRESOLVED | **PARTIAL** (reverses addendum keep-VERIFIED) | keep split | Aug21 vs 22Z via X lead + secondary only; page re-dated Aug26 never authority | claims already narrowed (X lead only); overall fix only |
| c099 VERIFIED MATERIAL MAIN_EVENT | Yes by implication: snapshot content + MAIN_EVENT with entry-dating via Sep8 capture + context | **PARTIAL** | content VERIFIED / entry-dating UNRESOLVED | Sep8 capture ≠ publication; entry vs W34 via context, not primary date | claims unchanged; add split |
| c100 VERIFIED MATERIAL MAIN_EVENT | Same as c099 | **PARTIAL** | content VERIFIED / entry-dating UNRESOLVED | same | claims unchanged; add split |
| c101 VERIFIED MATERIAL MAIN_EVENT | Same as c099 | **PARTIAL** | content VERIFIED / entry-dating UNRESOLVED | same | claims unchanged; add split |
| c102 VERIFIED MATERIAL MAIN_EVENT | Yes: Aug20 bundle + Aug21 addition in one VERIFIED target | **PARTIAL** | Aug20 bundle VERIFIED / Aug21 addition UNRESOLVED | Aug21 no-clock vs 22Z end; Aug20 internal sufficient | narrow claim or split; existing Aug20 capture suffices for bundle part |
| c001 PARTIAL CONTEXT MAIN_EVENT | Yes: “Release confirmed; exact Aug14 vs 22Z still unresolved” VERIFIED sub-target | **PARTIAL stays** | split sub-target content VERIFIED / timing UNRESOLVED | Aug14 vs 22Z side (Discovery Aug14 vs captured Aug18) | overall unchanged; fix sub-target split only |

c065 HOLD already PARTIAL/UNRESOLVED (correct, no change). c006 feed-only VERIFIED (Aug17 internal) remains VERIFIED — internal date needs no clock. Unaffected 31 DIDs remain as in decision map.

Existing captured DATA suffices for all content parts; **no new fetch indispensable**. Optional MSRC/Help/rankings only if vendor/scope/specs later load-bearing (root decides).

## Verdict

`CHANGES_REQUIRED` narrow: author must revise overall + splits per table (c002/c020/c039/c066 PARTIAL, include c022/c045/c024/c099-102/c001-split) as new DATA revision via strict facades, then re-run + independent re-review before `EVIDENCE_REVIEWED`. Prior keep-VERIFIED reversals for six are superseded by this uniform load-bearing rule; history preserved.

Attribution: General independent supervisory reviewer. No Sol/Astra/Human. WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN.

(End — 2026-11-04.)
