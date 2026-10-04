# DM-003 supplement report — S1/S2/S3 at fixed 222

Packet `notes/rephase-1-dm003-witness/dm003-supplement-20261003T202828Z/`
(`run_dm003_supplement.py`, `evidence/`, `evidence/supplement-manifest.json`).
Original seven-scenario data/report/harness preserved untouched. 46 recorded
operations across 3 scenarios (operations, not test methods). No shipping
changes, commits, network, or runtime repair.

## S1 — genuine byte-distinct rival + orphan selection (21 ops, PASS)

C2 built through actual builders over the same canonical source/manuscript/PDF
via existing `_build_special_second_chain` (distinct bundle/reviews/candidate;
only 4 files added, named State pins and C1 bytes untouched). Both Candidates
independently `validate_candidate`-valid: C2 sha `c09183a1…` ≠ C1 sha
`619ff4cf…`, equal pdf-sha, distinct paths. Direct `Freeze(C2,A1)` rejects exact
binding with no outputs and identical State. Orphan retargeted to C2 is
schema-valid yet path-AND-sha divergent from the consumed CORE report. Wrapper
freezes exact C1 **path+sha**; direct `_prior_artifacts` call resolves the C1
path with matching hash; surplus stage key hits the extra-key guard (not
merge); correct admission PASSes with a report-only write window. This replaces
the withdrawn infeasibility claim with the feasible boundary; old C6/C7 stay as
narrower distinct-path-only evidence.

## S2 — missing-sibling positive with write windows (13 ops, PASS)

Removal window is exactly `{-VALIDATED_DRAFT.json}`; approval window exactly
`{+approval, ~State}`; Freeze window exactly `{+freeze,+manifest}`; stage
window exactly `{+report}` — every other fixture byte identical (full
inventories + saved bytes pre/post). Sibling never recreated. This is the
central DM-003 positive with real snapshots; old C1/C3 keep their narrower
operation-success scope, no retrospective proof claimed.

## S3 — split refs at the wrapper boundary (12 ops, CHARACTERIZED finding)

Fresh approved State, outputs initially absent, A1/A2 each standalone valid
(distinct ids, both bind C1), human→A2 with checkpoint A1. `validate_agent_state`
returns `[]`. **The post-split wrapper BUILT**: added exactly Freeze+Manifest,
State unmodified, and byte proof shows the pair is bound to the **human-side
rival approval** (frozen approval sha == A2, ≠ A1; frozen candidate == C1).
Stage admission then rejects the disagree guard with no report. Original C5's
stage-only evidence could not claim pre-write behavior; S3 shows the writer
silently admits split authority.

## Bounded disposition proposal (for root + independent review)

1. File a **narrow defect**: missing human==checkpoint equality gate in
   `build_profiled_freeze`'s `_safe_state_profile` and in `validate_agent_state`
   (checkpoint-side only). Impact is bounded — same-C1 freeze here, stage
   backstop blocked FROZEN advance — but the writer must not mint outputs from
   split authority.
2. No runtime repair in this unit (not authorized); root selects scope only
   after independent resolution. No generic provenance scanner/resolver, no
   DM-004, no adoption inference.
3. Withdrawn overclaims (infeasibility, C1/C6 tautologies, C7 sha-only winner,
   C5 "not a defect") are corrected by S1/S2/S3 above; old observations keep
   their narrowed scope. Stop at the Human Commit Point after review.
