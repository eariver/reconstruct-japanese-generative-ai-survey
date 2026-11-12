# Supplement-carry corrected return (C1/C2 + HIGH late recheck + new tests, no full PASS)

Workcopy: `.rephase-1-editorial-runtime/supplement-carry-implementation-20261106T131722Z/candidate-work`
Base: isolated epoch `5eef790bd8d492c557cc4db9c29425e3e410d47d` (new root, NOT 409 ancestry; base blob IDs `e6c56ba3`/`37f22ab` are 40-char Git blobs vs 64-char SHA256, same files as final139 `0974c709`/`388c899`). Baseline untouched (no amend/replace); changes uncommitted.

Corrected source (post C1/C2/HIGH):
- `scripts/survey_research_authority_v2.py` worktree `57d06c7c4cf23d2502dc9f399a871f6abfca0975cb295bf7bfff18b7cc19fc9f` (base-staged `e6c56ba3…`)
- `scripts/survey_prearchitecture_acceptance_v2.py` worktree `f312f02e2dc5c1aa5a1d6432bca134cd83f0a1edea2d127721d0206d05514a90` (base-staged `37f22ab4…`)
- `tests/test_dm022_supplement_carry_v2.py` NEW `e3041b0250a7a013e7b2537f782b8f8c11f9dde5ab629335c21d5fd4c8a97bcc` (10 tests)
- Diff: `corrected-implementation.diff` (36062B, `git diff --` 2 files, 417+/23-); initial diff preserved as `initial-implementation.diff` (historical).

C1 (package pin discipline): request+COPY pinned before load via `_capture` + `_load_pinned_json` + schema + ancestors + recheck; OLD checkpoint/package via pinned loads; profile/discovery/screening + prompt/contracts (+ supplement schema) pinned before DS derivation; DS via original owner proper `derive_ordinary_root_effective_context` (COPY, never LOW LIVE); supplement via helper `_resolve` (effective DS, COPY-bound source_root); before return `_finish_authority_phase` (recheck supp + recheck pins + owner revalidate fields/files + recheck, no reseal). No future-path pins; private `MappingProxyType` discarded; explicit inert R partials vs no zero-write claim.

C2 (dead code): removed `expected_disc_abs/scp/manifest_abs` + `pass` + `_ = ...`; discovery/screening path binding relies on documented kernel (1630-1651) + `_resolve` manifest basis enforcement; no fabricated fallback.

HIGH (request late drift): preserve `original_request_raw/sha/len` + `original_supp_ref` (deepcopy) at entry; before manifest write re-read request bytes and compare to original, re-verify request refs + supplement SizedRef bytes, enforce `manifest.supplement_manifest == original_supp_ref` (not tautological in-memory compare); write `original_request_raw` to `request.json`. Proof triangle (request<->package + manifest==request, null enforces) already covers persisted triangle.

Tests (10, `PYTHONDONTWRITEBYTECODE=1`, real HIGH both routes, isolated fixture DBs, process-scoped identity):
- Preserved initial 4 (novel→unchanged Weekly DERIVED + Thematic, red null+bindings actual card failure, null+unknown).
- New: Weekly DERIVED replaced + Thematic replaced (same + replaced Raw, unaffected cards byte-identical, full task identity/Discovery binding, ledger rows identical for unaffected, `rows_checked` + mechanical allowlist), real decoy (a) request unrelated SizedRef refuses prepare, (b) manifest field swapped to decoy refuses prove (not null-control mislabel), late request drift before manifest (seam mutates request after LOW, HIGH late recheck refuses, State/guard preserved), late Raw drift before LOW return (seam mutates Raw during builder, pin recheck refuses).
- New batch raw: `corrected-batch-raw.txt` (argv/env/PID/start/exit/end + unittest stdout/stderr, exit 0, 23.634s, 10 tests OK). Pre/post source hashes identical (57d06/f312/e304), no mutation during tests.
- Parent baseline control (original final139, no monkeypatch, 1 test, no full suite): `baseline-control-raw.txt` (exit 1) — thematic novel positive fails on original producer with actual `source_bindings must explicitly select task-bound sources` (card build, not token). Fresh saved raw (not tool-history only). Demonstrates new test discriminates (fails before, passes after).

Gaps (not full PASS, for root/next verification):
- Replaced coverage is 1 replaced + 1 same supplement-bound + 1 Discovery-only per route; full SP 27+3 scale + W34 401 scale not exercised (needs real-material rehearsal, separate semantic review).
- Late mutations cover request (HIGH manifest boundary) + Raw (LOW return); COPY/OLDpkg/basis/manifest-file late drifts covered via pin recheck in code but not all exercised as separate failing tests (remaining: OLD checkpoint/package, profile/discovery/screening, prompt/contracts, supplement manifest file late drifts). No State/guard writes in all negatives (asserted State bytes + guard absent where applicable); inert R/retention partials explicitly allowed (state_copy + slot COPYs + candidate files may remain on late refusal, no cleanup).
- Targeted regressions (`test-oracle-inventory.md` §9), no-supp compat (`:615`/`:486` + C), fresh CURRENT proof (`verify_renewal_source_proof` via API with new pins/`expected_head/tree`), exact delivery still open. No PDF/R4/general suite. No real 409/160 correction.
- Initial fixture failures fixed locally; only fresh saved raws claimed (`corrected-batch-raw.txt`, `baseline-control-raw.txt`); initial `focused-test-raw.txt` preserved as historical.
