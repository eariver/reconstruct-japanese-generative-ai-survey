# Attempt 05 analysis (exit=1: 6 errors of 32, 0 failures; source freeze identical pre/post)

Two defects, both in candidate inputs (fixtures/gate green):

1. Proposal schema required `renderer_commit` to match 64-hex, but the actual
   recorded tool commit is a 40-hex Git SHA (matches the receipt schema's own
   `repository_commit_sha` pattern `^[0-9a-f]{40}$`). Fix: schema now requires
   the 40-hex commit pattern for `renderer_commit` only; digests stay 64-hex.
2. Matrix `noncanonical-before` hit the receipt callee first (`Weekly reviewed
   reader input drift`): full receipt validation byte-compares the reviewed
   file before P1's own canonical check. Fix: reorder `_pipeline` — parse the
   gate file for receipt routing and the receipt envelope for authored/reader
   routing (routing only, never acceptance), derive before/proposed with P1
   canonical checks first, THEN full receipt validation (plus a
   `RECEIPT_BINDING_CHANGED` guard that routing reads match the validated
   receipt), then full Gate validation. All bindings still verified.

Rerun as attempt-06 with exclusive outputs; attempts 01–05 preserved unmodified.
