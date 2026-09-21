# Diagnostic disposition

Closed by root on 2026-09-21 JST, following work begun 2026-09-16.

Candidate: `d38f023ce200619f7f49ce17a348755f05e0e021` (a1), direct parent fixed production `774dd39a951c9ac3818e83dfffd4c7666efb0a20`. Its six files are the unchanged five r2 production files plus the existing WU-011 contract-test adjustment.

## What completed

- The Worker's initial Python 3.10 diagnostic established a real document-test incompatibility with five-file r2. The preserved one-test failure required copied `PRE-AUDIT CANDIDATE` status. Worker proposed the test-only correction; root reviewed and applied it in the independent Git fixture. The corrected test is visibly `ok` in the subsequent Python 3.12 broad log. No Gate/schema/runtime authority check was relaxed.
- A separate initial import error was fixed-Core syntax requiring Python 3.12. Root provisioned isolated 3.12.14 and the fixed direct dependencies; see `runtime-setup.md`.
- `workflow-checks.json`: 405 Python files compile; 79 config/schema JSON files and 16 exact fixed-tree release manifests parse. The source manifests were parsed from a hash-verified cache. This is local workflow-equivalent checking, not hosted CI or full edition validation.
- `targeted-results.json` and `targeted-unittest.txt`: after materializing 41 exact fixed-tree assets (92,553 bytes, 25 raw downloads and 16 cache hits), both release-manifest tests and the SP001 access-provenance fixture test passed: **3 tests, no skips/failures/errors**. Their preceding broad-run failure/error/skip arose from sparse missing assets. No test or production artifact content was rewritten to make them pass. `test-assets.json` records every input hash.

## What did not complete

The Worker's Python 3.10 broad log is incomplete and was superseded by the corrected candidate/runtime. The Worker then hit its model usage limit after delivering the patch; root took over execution. Its separate 78-test subset log is preserved as auxiliary diagnostic evidence, not a complete CI result or a unique-test aggregate.

Root started `python -B -m unittest discover -s tests -p test_*.py -v` on a1 with Python 3.12.14. On resumption there was no running process and no `full-results.json` completion record. `full-unittest.txt` ends during a test, without unittest's final summary. The cause of termination is not established. **The full run is incomplete; do not reconstruct a complete PASS from its visible successful lines.** Preserve this log unchanged.

Its visible release-manifest failure/error and SP001 missing-file skip were resolved only by the three targeted reruns above. A W34 historical-commit fixture remains skipped because that older commit is unavailable in the shallow fixed-parent repository. Six legacy handoff skips are explicitly declared by upstream tests. Later undispatched/incomplete tests remain unverified in this run. No full all-tests or exact Core-pattern suite success is claimed on a1; no live Actions run was performed.

## Stop decision

The independent preparatory Auditor has established connected baseline blockers and `NOT_READY`. Root accepts that disposition. Completing or repeating the remaining broad suite cannot remove those contradictions; it is not necessary to establish the present negative readiness decision. Stop diagnostic expansion here and preserve the candidate/evidence for the next separately scoped maintenance decision. This does not waive remaining diagnostics before any later final audit/adoption.

The independent report predates this root diagnostic closeout. Root binds its unchanged candidate/source evidence to the final packet, but does not claim that the Auditor independently ran or signed these later tests. Canonical final seven-point audit was not started. No PASS was invalidated or carried across a mutation because none was issued.
