# Attempt 03 analysis (exit=1: 1 failure + 5 errors of 32; source freeze identical pre/post)

All 27 gate-control tests passed. Two P1 defects, both in candidate module:

1. `REF_DRIFT: gate-bound pre-TeX review` (4 hits incl. matrix cascade): the
   review node was pinned against `review_sha256` (a sha256_object digest over
   the review JSON value) instead of the review FILE's bytes. Fix: pin via the
   validated receipt's `semantic_review{path,sha256}` file ref, require the
   gate's review binding to equal the receipt's, and bind the pinned file's
   parsed `review_sha256` to the loader authority (`REVIEW_DIGEST_UNBOUND`
   otherwise). Review edge now carries file bytes sha.
2. Matrix `noncanonical-before` hit the callee first: Gate byte-scan refuses a
   noncanonical surface before P1's own check. Fix: reorder `_pipeline` —
   parse gate file for receipt routing (unvalidated), full receipt validation,
   before/proposed derivation with P1 canonical checks, THEN full Gate
   validation. Every binding is still verified; byte-level P1 checks precede
   byte-sensitive callee checks.

Rerun as attempt-04 with exclusive outputs; attempts 01–03 preserved unmodified.
