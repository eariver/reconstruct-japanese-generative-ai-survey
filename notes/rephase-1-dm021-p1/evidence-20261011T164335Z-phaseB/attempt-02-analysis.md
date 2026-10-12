# Attempt 02 analysis (exit=1: 6 errors of 32, 0 failures; source freeze identical pre/post)

All 27 affected gate-control tests passed again. All P1 errors were ONE arity
bug: `_pipeline` still passed the removed `before_context` argument to the
rewritten `_build_graph` (`takes 12 positional arguments but 13 were given`,
4 occurrences in stderr across the 5 P1 tests + matrix summaries). No fixture,
graph, scope, or predecessor logic was exercised yet.

Fix (candidate source, uncommitted): drop `before_context` at the call site.
Rerun as attempt-03 with exclusive outputs; attempts 01–02 preserved unmodified.
