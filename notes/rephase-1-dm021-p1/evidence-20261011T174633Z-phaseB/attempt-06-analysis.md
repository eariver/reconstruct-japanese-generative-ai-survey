# Attempt 06 analysis (exit=1: 5 errors of 32, 0 failures; source freeze identical pre/post)

Single defect: graph nodes carried short policy names (`KEEP`/`COPY`) while the
proposal schema (and selection) require `KEEP_IMMUTABLE`/`COPY_BEFORE_REPLACEMENT`.
Fix: `_pol()` emits the full enum values; `_retention_plan` branches on
`KEEP_IMMUTABLE`. Candidate test oracle already expected the full names.

Rerun as attempt-07 with exclusive outputs; attempts 01–06 preserved unmodified.
