# Attempt 08 analysis (exit=1: 1 failure + 1 error of 32; source freeze identical pre/post)

Two defects, both in candidate test (module green underneath):

1. Weekly tamper negatives now surface `STATE_INVALID`, not `DERIVATION_REFUSED`:
   checkpoint-bound tampers fail strict State validation (first gate) before
   any derivation runs — the layered behavior is correct, the oracle was stale.
   Fix: expect `STATE_INVALID` for checkpoint tampers; added a
   non-checkpoint authoring-archive tamper to keep loader-level
   `DERIVATION_REFUSED` covered.
2. Predecessor QA rebuild hit the producers' own no-overwrite guards
   (`refusing to overwrite Reader Manuscript Manifest`). Fix: the fixture
   explicitly unlinks the five stale QA files (manuscript/gate/bundle/two
   later reviews) before honest rebuild with real builders — fixture evolution,
   snapshotted only around P1 calls.

Rerun as attempt-09 with exclusive outputs; attempts 01–08 preserved unmodified.
