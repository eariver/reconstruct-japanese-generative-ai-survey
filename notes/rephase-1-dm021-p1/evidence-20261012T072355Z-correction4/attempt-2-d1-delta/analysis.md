# R4 Attempt-2 (failed, preserved, NEW runner E1 PASS)

36 tests, 3289.954s, 1 failure (D1 delta assertion logic, code correctly refuses).
NEW runner E1 facts PASS (exclusive O_EXCL, sanitized parent+child Git3 rc-checked,
routing/optimize rejected pre-Git, named-status pre/post identical, caches {} with
PYTHONDONTWRITEBYTECODE=1, no cleanup before post, timeout preserved).

## D1 delta logic (test-only, not code)

Outside `raw/source.json` mutated BEFORE validate-with-scope → P1 refuses
(DERIVATION_REFUSED early, correct fail-closed for outside-tree drift).
Test took `_snap_d1` AFTER mutation (mutated raw in both pre/post P1 snapshots),
so post-P1 diff correctly EMPTY (no P1 writes), but asserted diff=={_orel}
(injected raw) — wrong (injected already in pre). Fixed to two-phase proof:
clean vs mutated diff=={_orel} (explicit injected-only delta, only raw differs),
mutated vs post-P1 diff==set() (no P1 writes beyond injected, HEAD/status unchanged).
