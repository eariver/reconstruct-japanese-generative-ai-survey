# R1 correction round 3 — final results at successor 57853cb

All runs executed ONCE at committed HEAD `57853cb` (tree `b5f07b6…`) via the
durable runner (pins HEAD/tree/parent, source hashes, argv, cwd, python/deps in
each log). No tool-only results claimed. Weekly collects 33 tests (32
antecedent + validation-report new); counts disclosed per file, not collapsed.

| Suite (log) | Tests | Result |
|---|---|---|
| Weekly mechanical refresh (`weekly-refresh.log`) | 33 ran | OK, exit 0, 0 skipped (1535s) |
| Publication revalidation (`revalidation.log`) | 31 ran | OK, exit 0, 0 skipped (55s) |
| Reader-surface Gate (`gate.log`) | 27 ran | OK, exit 0, 0 skipped (1.2s) |
| Gate CLI persisted review (`cli.log`) | 5 ran | OK, exit 0, 0 skipped (39s) |
| **Total** | **96 ran** | **0 failed, 0 errors, 0 skipped** |

Round-3 regressions in the matrix: validation-report drift before/after receipt
(true CORE_STAGE_CONTRACT refs), canonical-names unit, inventory-unreadable
unit, writer+controller temp-ownership fault tests, bundle-result drift,
metadata-revalidation effective-rows success, alias entry tests, staged-control
refusal, same-byte swap (API + wrapper), post-preflight drift cases. Post-rename
no-dangling-pointer, true-overlap, foreign-guard, head/state, partial-API and
postcommit oracles retained and green here.

For ROOT review then independent resolution. The independent reviewer has not
seen 985dcd6+ and does not approve; nothing claimed otherwise. No adoption or
PASS claimed. Candidate fixtures use process-local synthetic Git envs; root does
not run tests.
