# Attempt 11 analysis (exit=1: 1 failure of 32, 0 errors; source freeze identical pre/post)

Single remaining defect, and it is a real honesty finding, not a typo: after
the derivation-only fixture commit, regeneration executed AMBIENT candidate
code, so `main.tex` never changed while the revalidation record claimed a
reviewed rendering change. Epoch guards bind replay execution to committed
bytes; ambient code cannot honestly replay a committed derivation revision.

Fix (test only): the post-commit cascade (regenerate with real producers,
honest QA rebuild, real revalidation, P1 prepare + staged REVIEW_REQUIRED
validate, no-write asserts) executes inside a fixture-code subprocess
(cwd=fixture root, sanitized env, no network/PYTHONPATH). The subprocess
imports the test helpers from the FIXTURE's committed `tests` package, so
every replay executes the committed basis. In-process asserts verify the JSON
summary (ACTIVE origin, changed sha, record/pointer/checkpoint integrity,
graph size, REVIEW_REQUIRED) plus file existence.

Rerun as attempt-12 with exclusive outputs; attempts 01–11 preserved unmodified.
