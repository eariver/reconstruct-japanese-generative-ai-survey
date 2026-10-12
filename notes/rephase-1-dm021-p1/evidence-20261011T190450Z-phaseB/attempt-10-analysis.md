# Attempt 10 analysis (exit=1: 1 error of 32, 0 failures; source freeze identical pre/post)

Single remaining defect in candidate test: the gate rebuild unlinked the old
gate file first, but the gate builder's internal receipt replay resolves
pending rows including the gate itself. Fix: rebuild manuscript/bundle/reviews
with immediate unlink-before-own-rebuild, but rebuild the gate over the
existing file (its builder evaluates before writing, no pre-refusal observed).

Rerun as attempt-11 with exclusive outputs; attempts 01–10 preserved unmodified.
