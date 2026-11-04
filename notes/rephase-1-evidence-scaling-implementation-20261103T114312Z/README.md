# Evidence scaling implementation — packet (no approval)

Workdir (ignored runtime, NEW, independent DB):
`.rephase-1-editorial-runtime/evidence-scaling-implementation-20261103T114312Z/candidate-work/`
from final138 proof `.rephase-1-editorial-runtime/profile-support-packaging-20261031T202327Z/proof-copy/candidate-partial-b40de60`
(actual409/tree8ce +138 delta/770 intended).
Manifest `634d41f9807e8cd60ca3d839245358fa5e5da312f6d1b58ae84c1619481a03dc`/186847B,
patch `efb505e4c1ccb3c83121db2fbaa9fec05ed900c252184765ca3b50f7b28254e`/5247647B.

Preserved: old rehearsal `48082356` + real DATA untouched (no mutation here);
author copy HEAD409 preserved, no ordinary commit/push; no root Git status/log/HEAD,
no Human readback/network/Production/current checkout.
All old maps/reviews preserved (R1/R2, Astra §§1-7, independent FINAL).

Changed runtime owners (3, no new module/schema/family):
- `scripts/survey_evidence_v2.py`
- `scripts/run_evidence_v2_interactive.py`
- `scripts/survey_research_authority_v2.py`
Test-only: `tests/test_evidence_scaling_v2.py` (new, allowed).

See `implementation-return.md` for helper mechanics, caller closure/modes,
test runs with raw stdout/stderr/PID/argv/env/exit/pins, limits, blockers.
`test-runs/` holds UNIQUE exclusive raw files per batch.

Whole NOT_READY (implementation complete, no independent review/whole READY).
Do NOT run real409 yet — root reviews diff first. Human Commit Point.
