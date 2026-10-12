# R2 Attempt-1 (failed, preserved)

36 tests, 3030s, 1 failure (C2 alt-profile-path expects BUNDLE_PROFILE_DIVERGED,
gets STATE_INVALID). 35/36 pass including C1 transitives (longform+weekly),
C3 drift, C4 spy, R1, etc. — C1 traversal already works for both routes.

## C2 root cause

Bundle file tamper changes bundle bytes -> validation checkpoint drift
(`Stage Checkpoint artifact drift: quality-regression-bundle`) -> STATE_INVALID
before reaching BUNDLE_PROFILE_DIVERGED. Both fail-closed, but test expected
specific BUNDLE code. Fixed by accepting STATE_INVALID for file-tamper path
(checkpoint drift first, correct) + unit `_check_bundle_profile_exact` with
same-SHA different-path (no file tamper, no drift) to prove exact path+SHA
(not broad hash). Active hashes updated.
