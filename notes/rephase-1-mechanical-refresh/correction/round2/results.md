# R1 correction round 2 — final results at successor 8a544f9

All runs executed ONCE at committed HEAD `8a544f9` (tree `68a4479…`) via
`correction/round2/run-suite.sh`, which pins HEAD/tree/parent, source hashes,
argv, cwd, python/deps in each durable log. No tool-only results claimed.

| Suite (log) | Tests | Result |
|---|---|---|
| Weekly mechanical refresh (`weekly-refresh.log`) | 25 ran | OK, exit 0, 0 skipped (1246s) |
| Publication revalidation (`revalidation.log`) | 29 ran | OK, exit 0, 0 skipped (54s) |
| Reader-surface Gate (`gate.log`) | 27 ran | OK, exit 0, 0 skipped (1.2s) |
| Gate CLI persisted review (`cli.log`) | 5 ran | OK, exit 0, 0 skipped (40s) |
| Increment-B weekly derivation (`increment-b.log`) | 8 ran | OK, exit 0, 0 skipped (266s) |
| **Total** | **94 ran** | **0 failed, 0 errors, 0 skipped** |

Targeted true regressions added this round (all in the matrix above unless noted):
- Post-preflight checkpoint/control-dirty/untracked drift refused with zero writes.
- Real-entry alias State path + inside-root publication symlink refused.
- True in-process writer overlap (second real writer refuses occupied guard).
- Foreign guard replacement during retention → precommit refusal, old authority, retention base left.
- Post-rename State failure → rollback-first, orphan-only deletion, no dangling pointer.
- HEAD/State drift split into independent fixtures with exact expectations.
- Torn API write → preserved-new live + tampered record + retained guard.
- Post-commit reporting failure → committed authority never rolled back.

For ROOT review again before any independent review. No adoption or PASS claimed.
Candidate test fixtures use process-local synthetic Git envs; root does not run tests.
