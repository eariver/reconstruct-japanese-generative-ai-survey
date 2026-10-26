# Reader F4 final — actual result table (nonempty, no whole PASS/CommitPoint)

- Run: 2026-10-25T19:22:41Z → 19:23:06Z (25.220s), PID 141033, heartbeat 1 line, exit 0.
- Command: `python3 -m unittest tests.test_versioned_renewal_reader_f4_20261025 -v`
  cwd candidate-work, PYTHONDONTWRITEBYTECODE=1, timeout 1200s, no network/old-runner/cleanup/commit.
- Raw: test-exit.txt (0), test-stderr.txt (7 ok), test-stdout.txt (empty, unittest -v to stderr), run-pid.txt, run-heartbeat.txt.

| # | method | fixture/epoch | manuscript | proof | expected | actual |
|---|--------|---------------|------------|-------|----------|--------|
| 1 | test_f4_canonical_neither_without_proof_passes | weekly U1 G1 85eac6f | canonical no-field | none | PASS | ok PASS, no drift |
| 2 | test_f4_canonical_neither_with_proof_refuses | weekly U1 G1 85eac6f | canonical no-field | U1 current | REFUSE REVIEW_TARGET_MISMATCH | ok REFUSE REVIEW_TARGET_MISMATCH, no drift |
| 3 | test_f4_correct_c_passes_at_own_epoch | weekly C1 G2 cec67e5 | C1 embedded own | C1 own (same path+SHA) | PASS | ok PASS, no drift |
| 4 | test_f4_neither_with_outer_proof_refuses | weekly C1 G2 cec67e5 | C1-delete-embedded tmp rehashed (owned) | C1 own | REFUSE REVIEW_TARGET_MISMATCH | ok REFUSE REVIEW_TARGET_MISMATCH, no drift, orig unchanged |
| 5 | test_f4_wrong_embedded_sibling_refuses_even_equal_sha | weekly U3 G4 296c460 | C1-sibling-embedded tmp (equal bytes, new path, owned) | U3 current (trio matches C) | REFUSE lineage-reachable, not drift | ok REFUSE lineage-reachable, no drift, equal SHA verified |
| 6 | test_f4_u_editorial_unchanged_passes_at_own_epoch | weekly U1 G1 85eac6f | editorial stored old source | U1 current external | PASS | ok PASS, no drift |
| 7 | test_f4_u_after_c_ancestor_passes_current | weekly U3 G4 296c460 | C1 stored ancestor | U3 current (trio matches) | PASS | ok PASS, no drift, embedded preserved |

- Summary: Ran 7 tests in 25.220s, OK (0 failures, 0 skips). 4 PASS + 3 REFUSE as specified, all in isolated child fresh roots.
- No skips unless external genuine blocker (none occurred). No PASS from earlier tool drift (child __file__ guard + no BASIS_CURRENT_TOOL_DRIFT in outputs).
- Test-only: candidate dirty (M/U) preserved, no runtime edits, no ordinary candidate/reconstruct commit, scratch cleaned (0 left).
