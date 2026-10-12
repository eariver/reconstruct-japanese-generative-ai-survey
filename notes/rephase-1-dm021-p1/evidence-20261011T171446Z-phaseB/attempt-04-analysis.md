# Attempt 04 analysis (exit=1: 1 failure + 5 errors of 32; source freeze identical pre/post)

Single new layer reached (graph build runs). One design defect, not a fixture
problem: `POLICY_CONFLICT` for `references.bib`, which is both a receipt
generated output (mutable → COPY) and a manuscript BIBLIOGRAPHY support
(formerly KEEP). Per-role policy assignment is order-dependent first-wins in
disguise. Fix: single deterministic policy function of the path — COPY iff the
path is an effective non-review checkpoint row, a receipt output, the receipt
or reader-input file, or a bundle QA result file; KEEP otherwise (upstream,
checkpoint/predecessor records, digest-pinned reviews, tool closures,
candidate). Genuine HASH_CONFLICT / residual POLICY_CONFLICT guards retained.
Also added the before-reader file as an explicit `reader:before-input` node via
a `RECEIPT_CLOSURE reviewed-input` edge (it was basis-only before).

Rerun as attempt-05 with exclusive outputs; attempts 01–04 preserved unmodified.
