# §8 duplicate-DID exact-coverage correction (TEST-ONLY + focused tests, runtime frozen except LOW predicates)

Workcopy: `.rephase-1-editorial-runtime/supplement-carry-implementation-20261106T131722Z/candidate-work`
Base: `5eef790…` (new isolated root, NOT 409 ancestry).
Runtime (frozen except §8 LOW predicates): LOW `7f5fc9e0…` (was `d50282…`), HIGH `f312f02e…` unchanged.
Tests: focused `a8aaafe3…` (17 methods: 14 preserved + 3 duplicate new), C `1fa905bf…` (N7 updated), scale `7118092f…` (2 methods preserved, not rerun).

Source diff (`corrected-implementation-v3.diff`, 46940B, tracked only):
- `derive_before_context`: cardinality+set (`len==len(non_drop)` + `set==non_drop`), same message (no oracle break).
- `build_revision_package_from_paths`: same cardinality+set (same message as C N7 expects).
- `prove_revision_from_paths`: same guard for proof admission (message includes duplicate word for new path; no existing oracle asserts it).
- Views comparison (§6) unchanged; empty_ctx canonical factory unchanged.
- No schema/helper framework/general cleanup; no HIGH/runtime changes beyond predicates.

C N7 (§7 authorized, preserved failure raw `affected-verification/.../batch-05-c-direct-raw.txt`):
- Updated expected to new preflight exact message + timing (State COPY may exist, candidate package/tasks/cards NOT yet constructed) + inventory (State unchanged, no checkpoint/proof/guard, no candidate package/tasks/results). `changed-c-n7-v2-raw.txt` exit 0 (4.553s) with new source.

Duplicate guards (new, 3 tests, `duplicate-guard-raw.txt` exit 0, 3.223s):
- Identical-body duplicate, conflicting-body duplicate (HIGH prepare refuses before candidate publication, State/guard preserved, inert COPY allowed precise, no normalization/drop).
- Direct prove admission with duplicate-bound request (tampered request+manifest+decision bindings hold, duplicate predicate refuses; no decoy).

Scale witnesses (preserved, not rerun in §8 per scope; prior raws `scale-w34-raw.txt` exit 0 313.961s, `scale-sp-raw.txt` exit 0 96.578s):
- W34: 409 tasks, 401 supp-bound, 428 entries (374×1 + 27×2), 428 unique Raw (documented selected shape, not real 428/425 duplicate shape), affected 4 + unaffected 405, unchanged+replaced via HIGH prepare/adopt/readback.
- SP: 160 tasks, 28 supp-bound, 30 entries (26×1 + 2×2), affected 4 + unaffected 156.
- Multi-source, full views/cards/ledger/task-identity/rows_checked/mechanical, prior-records preserved, synthetic explicit.

Pending: targeted regressions beyond C N7, no-supp compat, fresh CURRENT proof (`verify_renewal_source_proof` via API) + new DIRECT409 delivery after review; no real 409/160 semantic adoption. Old CURRENT/packaging (`final-20261107T034506Z`) preserved pre-fix, superseded, not overwritten. No full PASS claimed.
