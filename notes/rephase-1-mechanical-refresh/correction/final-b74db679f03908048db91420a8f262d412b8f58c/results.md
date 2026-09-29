# R1 correction final — results at successor b74db67

All runs executed ONCE at committed HEAD `b74db67` (tree `515b5e9…`) via the
durable runner (pins HEAD/tree/parent, source hashes, argv, cwd, python/deps in
each log). No tool-only results claimed. Weekly collects 34 tests (33
antecedent + null-review new); counts disclosed per file, not collapsed.

| Suite (log) | Tests | Result |
|---|---|---|
| Weekly mechanical refresh (`weekly-refresh.log`) | 34 ran | OK, exit 0, 0 skipped (1677s) |
| Publication revalidation (`revalidation.log`) | 31 ran | OK, exit 0, 0 skipped (56s) |
| Reader-surface Gate (`gate.log`) | 27 ran | OK, exit 0, 0 skipped (1.2s) |
| Gate CLI persisted review (`cli.log`) | 5 ran | OK, exit 0, 0 skipped (40s) |
| **Total** | **97 ran** | **0 failed, 0 errors, 0 skipped** |

Round-4 regressions in the matrix: K1 null-review refresh success plus retained
validation-report mutation negatives; canonical-names unit; inventory-unreadable
unit; writer+controller temp-ownership fault tests; bundle-result drift;
metadata-revalidation effective-rows success; alias entry tests; staged-control
refusal; same-byte swap (API + wrapper); post-preflight drift cases. Post-rename
no-dangling-pointer, true-overlap, foreign-guard, head/state, partial-API and
postcommit oracles retained and green here.

For ROOT review then independent resolution. The independent reviewer has not
seen 985dcd6+ and does not approve; nothing claimed otherwise. No adoption or
PASS claimed. Candidate fixtures use process-local synthetic Git envs; root does
not run tests.
