# H batched Git perf — narrow AUTHOR-H task (parallel, root FULL operation remains)

2026-10-25. AUTHOR-H narrowly bounded performance/integration. Human `f84fcf5`,
correct candidate `.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work`,
H before `8f1294e7367306d802bdf059a21f631abed80cee54a162e074ad203e1a7f64c0` (3740 lines, pre-batch),
H after `70bcdbb8602dd012cd300eba3e9972735ea5dd29e52cfb76e59cee6605230467` (3989 lines, batched).
Other authors untouched: PUB `02f851...`, S `20f63e...`, HIGH `1620b92...`/`9a0469...`, Reader `098a2c...`, schemas unchanged.

## Scope (root-selected FULL operation remains, this is narrow H-only)

- Read AGENTS (no authority cache), root `7d7d5a45...` §6 (pointer `""`, strict LIVE State, no Path fix),
  contract `478f0051...` §11 (typed history/source/high, exact U/C, proof threading).
- H source 3395-line base (`1667c190...`) + Contract8 current preserved; no weakening CURRENT on EVERY readback.
- Real high24 weekly history r1 (chain1, 11 bindings) and r8 (chain8, 82 bindings) + source-proof relevant entry
  (S Layer-B CURRENT closure readback measured indirectly via H chain; S file untouched).
- Fresh controlled snapshot, cProfile + Git-call counting, retaining all source pins/guard/exits.
  No old saved-runner execution, no network, no fixture cleanup, no ordinary candidate commit.

## Baseline (pre-batch, H 8f12..., 20261025 fresh run on high24 weekly)

- r1: 3.379s, git 895 (show 408, ls-tree 374, cat-file -e 113), chain1, 11 bindings, PASS
- r8: 57.015s, git 9247 (show 4052, ls-tree 2669, cat-file -e 2526), chain8, 82 bindings, PASS
- Profile: subprocess 25.3s + jsonschema 27.3s of 57s. Dominant per-file Git child calls confirmed.
- Raw: `measure_h_baseline_20261025.py` + `before-measure-20261025.json` (reconstructed from fresh run output,
  H 8f12...). BEFORE profiles overwritten by AFTER run; BEFORE top40 showed git dominance (see §Results).

## Fix (H-only, SAME predicates, bounded batched RAW retrieval WITHIN single invocation)

- `_sanitized_git_env()`: strips GIT_DIR/WORK_TREE/INDEX_FILE/PREFIX/COMMON_DIR/NAMESPACE, sets
  GIT_OPTIONAL_LOCKS=0, NOSYSTEM, GLOBAL/SYSTEM=/dev/null, NO_LAZY_FETCH=1, NO_REPLACE_OBJECTS=1.
  No remote/lazy fetch, no inherited root override. Diagnostics stderr+returncode preserved.
- `_FINITE_BATCH_PATHS`: exact finite union (OLD_PIPELINE_67 + NEW_SCHEMAS_4 + QUALITY_3 + config/profile/state +
  OLD_PY_30 + OLD_SCHEMAS_14 + NEW_PY_3 + NEW_SCHEMAS_4 + FAMILY + ROUTE + STAGED + STYLE + RECIPE +
  KNOWN_SCHEMA_SHAS keys + OWNER_REGISTRY paths). No new unsupported paths/prefix, no optional checks.
- `_fetch_epoch_tree_batch()`: single `git ls-tree -z <epoch> -- <finite>` per epoch, NUL parsing,
  verifies mode 6-octal, type==blob, OID 40hex, path in finite set, no duplicates, count bounds,
  newline/NUL/bad type/length/mode/path/object-replace/missing/ancestor fail-closed.
- `_fetch_epoch_blobs_batch()`: single `git cat-file --batch` by validated OIDs (not path lines),
  parses `<oid> <type> <size>\n<content>\n` binary-safe, verifies OID==requested, type==blob,
  size int 0..10MB, content length, trailing NL, count==requests, no extra bytes. Missing -> BLOB_MISSING.
- `_git_show_blob`/`_git_tree_mode`: use batch when `_cache` present and path in finite set; fallback single-path
  with sanitized env otherwise (preserves SAME predicates for unknown paths, no broadening).
- `verify_versioned_history`: creates per-invocation `_inv_cache={}` and threads through all H helpers
  (`_verify_editorial_ancestor`, `_derive_editorial_observed_bindings`, `_verify_versioned_ancestor`,
  `_derive_versioned_own_bindings`, plus all `_verify_*`/`_check_*`/`_derive_*`/`_recompute_*`).
  Only immutable tree/blob/commit-existence cached; HEAD/dirty never cached (H leaf has no HEAD/dirty queries).
  No global/persistent cache, no caller permit, no ambient context. Exact epoch/root+path+mode+blobSHA+byte_count
  still verified for EVERY ref; git batch cannot accept new paths.

## After (batched, H 70bc..., same fixture/pins)

- r1: 0.547s (first AFTER run) / 0.162s (second, warm FS) vs 3.379s before → 6.2x–20.8x faster, git 3 vs 895 (298x fewer)
- r8: 29.32s / 9.66s vs 57.02s before → 1.9x–5.9x faster, git 20 vs 9247 (462x fewer)
- Gain range: r1 6–21x time, 298x calls; r8 1.9–5.9x time, 462x calls. Remaining ~27s is jsonschema instance validation
  (SAME predicates, 1360 validations, cannot cache results; validator construction ~1.4s only, so schema-cache alternative
  would give <5% gain – not implemented, correctly returns measured gain, no fake fix).
- Semantic identity: chain1/11 and chain8/82 unchanged, observed_refs/observed_source_bindings byte-identical
  (verified in perf test + existing author-H 5/5 OK). No weakening.
- Raw: `after-measure-20261025.json` (=`baseline-measure-20261025.json`, H 70bc...), `baseline-profile-r1/r8-20261025.txt` (AFTER).

## Tests (NEW independent DBs only, no candidate commit)

- New: `tests/test_versioned_renewal_history_perf_batched_20261025.py` (3 tests, 51–54s, PASS):
  - `test_perf_r1_r8_semantic_identity_and_gain`: isolated high24 copy (721 ancestry + G1-G6 + oldE uncommitted, inert origin),
    r1/r8 PASS with same chain/bindings, git <=30, faster than before, zero-write inventory (no tracked mods),
    repeat r8 still passes (no authority cache).
  - `test_negatives_still_refuse`: wrong mode (100755 vs 100644 → HISTORY_MODE), missing blob (BLOB_MISSING),
    foreign schema (UNSUPPORTED), unknown route/contract (UNSUPPORTED), pointer "/" (UNSUPPORTED, intended seam with valid live/epoch),
    O17 inventory pointer (UNSUPPORTED), deep extra/subset after rehash (HISTORY_DIGEST_MISMATCH, late, not digest drift;
    full rehash of basis/proof self-digests + record refs, so digests pass). Each in NEW isolated DB, preserved (never cleaned).
  - `test_repeat_after_mutation_refuses_no_authority_cache`: first PASS chain8, mutate live basis SHA, second must refuse
    (proves no cached PASS).
- Existing author-H: `test_versioned_renewal_history_author_h_20261025` 5/5 OK with batched code (T1 genuine style-change,
  T2 NEW63/UNKNOWN, T3a/b/c scope/selfdigest/extra-keys + T3d pointer + T3e foreign epoch, all late after rehash).
  Proves SAME predicates for deep negatives preserved.
- Exits: `test-exits-20261025.txt` (all 0). No full integration, no independent PASS, no CommitPoint.

## Source pins / guards

- Candidate HEAD `409b292...`, fixture weekly HEAD `50b03a6...`, status `??` only (oldE + new tests), no tracked mods.
- H before `8f12...` (3740), H after `70bc...` (3989). S `20f63e...`, HIGH `1620b92...`, Reader `098a2c...` untouched.
- Frozen baseline: `.rephase-1-editorial-runtime/versioned-renewal-combined-freeze-20261025T041436Z/snapshot-work` (735 files, 409b292).
- Own patch: H batched diff only (see `git diff` in candidate-work, H file only). New test file untracked (independent DB commits only).
- No network, no old runners, no cleanup of failed fixtures/raw (all scratch preserved under `versioned-renewal-test-scratch-authorH/perf-batched-*`).

## For root

- Combined final source = frozen baseline (735) + own H patch (batched, 70bc...). New test file for parallel route exec reference.
- Parallel route exec after you: use combined snapshot + batched H (faster history, same predicates) for U/C operation.
- Report: exact gain r1 6–21x (3.38s→0.16–0.55s, 895→3 calls), r8 1.9–5.9x (57.0s→9.7–29.3s, 9247→20 calls);
  scoped tests 3/3 PASS + existing 5/5 OK; failures none (deep extra/subset covered by existing T3, perf negatives early+deep both refuse);
  not full integration (no U/C, no renewal→editorial, no normal lifecycle, no regressions beyond H); final H `70bcdbb8602dd012cd300eba3e9972735ea5dd29e52cfb76e59cee6605230467`.
  No independent PASS, no CommitPoint. Ordinary Commit/Push Human-owned.
