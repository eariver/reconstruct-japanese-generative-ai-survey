# Material binding — actual DATA refs (hashes after saving, transport ≠ proof)

Code: final138 `efb505e4`/5247647B, manifest `634d41f9`/186847B. Workdir HEAD `48082356` (isolated rehearsal base). Refs: W34 `774dd39a`, SP `c8d0ecc1`.

## Profiles / States (fresh, source-bound, CURRENT)

- W34 fresh Profile from `core.weekly_profile` (now 2026-08-25T00:00:00Z, issue 2026-W34): question/window (ROLLING_WINDOW 2026-08-14T18:00–2026-08-21T18:00-04:00 America/New_York)/dims (3)/obligs (weekly:current-relevance/technical-significance/carry-over)/paths match authorized `.rephase-1-inputs/774…/production-profile.json`. Contract fresh (`2.0-rc1`). State `ISSUE_INITIALIZED`, impl `48082356`, agent-valid.
- SP fresh Profile from `core.thematic_profile` (spec = authorized `DATA.production-profile.json` question/dims/asof/inclusion/exclusion/O01–O12/paths verbatim): temporal OPEN_HISTORY_AS_OF 2026-09-21T16:10:00Z, 12 dims, paths `sources/SP-efficient-llm-2026` preserved; contract fresh. State `ISSUE_INITIALIZED`, impl `48082356`, agent-valid.

## Intake DATA used (all in `intake-20261101T023147Z-p2-20261101T024051Z/`, plus P1)

- W34 Discovery root: `DATA.p2b01.discovery-v2.jsonl` 963155B `e176326f853e…` (369 rec) → active `sources/2026-W34/discovery/discovery-v2.jsonl` (copied, exact bytes).
- W34 effective (reference only, not installed): `DATA.p2b19.p2b19` 1335444B `0a23be47…` (439 event rec, REFERENCE_EXPANSION).
- W34 interactive Evidence: `DATA.p2b18.p2b18` 1573186B `3ffc6e31…` (409 rec, 3 obligs 3-field, runner muse-spark-1.3 EXPERIMENTAL_LUNA).
- W34 acceptance reference (not installed): `DATA.p2b02` 377589B, `DATA.p2b05` 543880B (439), `DATA.p2b06` 126603B (409), `DATA.p2b08` 159498B (409 views), `DATA.p2b09` 186202B (439-row ledger), `DATA.p2b10` 71532B (3 obligs LIMITED), `DATA.p2b11` 676213B (409-row matrix), `DATA.p2b12` 289677B (SELECTED41), `DATA.p2b13` 27528B `7f30d273…`, summaries/attention, supplement `DATA.p2d01` 50490B, checkpoints p2a01–p2a10.
- SP Discovery root: `DATA.p2b20.discovery-v2.jsonl` 173299B `7074cef2…` (165 rec) → active `sources/SP-efficient-llm-2026/discovery/discovery-v2.jsonl`.
- SP Raw obs (24/25, copied to active `sources/SP-efficient-llm-2026/raw/`): `DATA.p2c15`–`DATA.p2c38` (methodology/capstones/d01–d10/r2-g12–g20/r3-d09–g23/r4-x; negative-space `DATA.p2c14` reference only). Missing: x-reception `…/raw/x-reception-result-r3.md` (needed, §3).
- SP Screening: `DATA.p2b22` 69226B `65330476…` (165, 135 KEEP) + `DATA.p2g14` 68226B (decisions, 165/165 valid, cover accepted exactly).
- SP Evidence original (fresh-run basis): `DATA.p2c01` 313083B `6cac92b1…` (160 rec, 155 PARTIAL/5 VERIFIED — ts001-substantive) + `DATA.p2c02` 12011B task-targets; r2 `DATA.p2c03` 311908B reference only (148/12 matches projected counts, not used as basis). Accepted projected (`DATA.p2b23` 49241B, `DATA.p2b24` 64227B, package `DATA.p2g15` 48659B, interactive `DATA.p2g16` 311908B) comparison-only.
- SP adapted completeness input (packet only): `input-archive/SP/interactive-evidence-adapted-O13-15.json` 346320B (p2c01 + O13/O14/O15 5-field from `DATA.p2b26`; 12×3 + 3×5 verified, no upgrade).
- SP acceptance reference: `DATA.p2b25` 66865B, `DATA.p2b26` 32511B (15 obs: 3 SATISFIED/12 LIMITATION), `DATA.p2b27` 236220B, `DATA.p2b28` 83877B (SELECTED112), `DATA.p2b29` 32767B + summaries/attention (9-pkg), research-scope `DATA.p2b32` 12302B, reader trio (`DATA.p2a28` 293777B `87bcb707…`, `DATA.p2a29` 39266B, `DATA.p2a30` 850785B `8a9a721a…`), manuscript `9657B cf7aca20…`, candidate `adf22516…`, revalidation `380cedca…`, checkpoints p2a11–p2a19, supplement `DATA.p2f02` 12859B + 13 Raw 1,275,978B, sessions/Sol pass, compat ledger `DATA.p2e02` 87223B (comparison only).
- W34 PDF/manuscript + SP PDF/tex/bib SHAs as in ready-sufficiency (reused by exact SHA, not re-fetched; transport ≠ completeness).

Old approvals/checkpoints never rebound; compat never adopted; synthetic fixtures never baseline. Missing X manifests + Raw in §3 with expected SHAs are the only blockers to Discovery acceptance.
