# Attempt 12 analysis (exit=1: 1 failure of 32, 0 errors; source freeze identical pre/post)

Single defect in candidate test: the fixture-code subprocess imports the P1
test helpers from the fixture's committed `tests` package, but fixture roots
never contained `tests/` (copied dir set was config/schemas/scripts/
templates/prompts/docs/data only). Fix: `_make_source_root` now also copies
tracked `tests/` files; the new P1 test file itself remains covered by the
explicit untracked-inclusion list with hash pinning.

Rerun as attempt-13 with exclusive outputs; attempts 01–12 preserved unmodified.
