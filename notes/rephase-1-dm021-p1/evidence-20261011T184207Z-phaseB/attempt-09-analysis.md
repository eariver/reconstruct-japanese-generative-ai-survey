# Attempt 09 analysis (exit=1: 1 failure + 1 error of 32; source freeze identical pre/post)

Two defects, both in candidate test (module green underneath):

1. Weekly negatives trailing no-write assert still used the pre-staging
   snapshot. Fix: assert against the post-staging snapshot (P1-call windows
   only); tamper files are restored in `finally` and covered.
2. Predecessor QA rebuild unlinked all five QA files up front, so the gate
   rebuild's internal receipt replay hit pending-path row resolution with gaps
   (`quality-regression-bundle missing`). Fix: dependency order with immediate
   unlink-before-own-rebuild — manuscript, then bundle, then the two later
   reviews, then the gate last — so every row file exists whenever a producer
   replays pending rows.

Rerun as attempt-10 with exclusive outputs; attempts 01–09 preserved unmodified.
