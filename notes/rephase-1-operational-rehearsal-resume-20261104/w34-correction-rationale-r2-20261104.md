# W34 r2 chronology correction — concise rationale (proposal, not review)

2026-11-04. Author r2 (NOT reviewer/root). Preserves r1 (`w34-corrected-input-20261104.json` 5e53a179...) untouched. Bounds: Root §3 (astra-resume-resolution.md §§1-3 FULL), final addendum + final-map, prior delta review + delta-map, r3 observation (`current-observation-r3-20261104.json` 3f350e3a... authority; old `current-observation.json` malformed pins rejected). Active e84 instance only. No active changes/Raw staging/execution/imports/tests/network/Production/reconstruct Git. Packet DATA only.

## Criterion applied

`VERIFIED+MAIN_EVENT+MATERIAL` asserts a week-eligible event. Boundary Aug14/Aug21 date-only or Sep8 capture+context asserted as W34 placement with unresolved 22Z side → overall `PARTIAL` (content-VERIFIED / timing-UNRESOLVED). Internal Aug15-20 date-only needs no clock. `AUTHOR_CLAIM` supported (`evidence-v2-card.schema.json:148`); splits use `VERIFIED/UNRESOLVED` targets only (schema `_validate_card_core` structure-only). Claims unchanged except r1 scope fixes already done.

## r2 input

`w34-corrected-input-r2-20261104.json` 1580317B `1ea562977534b55d3bbf2f89492411e89e22be09bc5667a450da6bf5ede2fbed` (programmatic sha256, 64-hex valid), 409/409 records. Delta vs original: 16 DIDs; vs r1: 12 DIDs. Supplement unchanged `ce6f977a...5b14b...` 389414B (corrected r3 pin; old 61-char rejected). 401→393 identical otherwise; no blanket downgrade. Materiality/window unchanged (c024 CONTEXT kept). c004 VERIFIED internal stays; c055/c065/c006/c096 r1 fixes stand; c001 PARTIAL with new sub-split.

PARTIAL set: c002/c020/c022/c024/c039/c045/c066/c099/c100/c101/c102 + c001 (split). Each carries content-VERIFIED + timing/entry-dating UNRESOLVED with no-upgrade clause. Full hashes/counts/target keys in `w34-corrected-delta-r2-20261104.json`. No new fetch indispensable.

Preserved: original/supplement/accepted/Ledger/Completeness/States/r1 files. No install/disposition. Ready for independent review; re-run + re-review required before `EVIDENCE_REVIEWED`. No semantic self-approval.
