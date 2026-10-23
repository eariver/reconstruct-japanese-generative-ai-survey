# R3 corrective CODE return (Worker, internal — NOT Human Commit Point)

## Pre-start verification
- `ps` at 2026-10-21T09:25Z: no active project Python/build/test child (only
  system networkd-dispatcher, unattended-upgrades, opencode web infra). No live
  job duplicated.
- DST `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60`
  HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, status as found (24 tracked M +
  untracked new editorial modules/schemas/tests + `__pycache__` + `tmpvr07sdme/`
  residue preserved, never cleaned). Prior failed-provider worker left NO fix:
  low docstring already claimed 4-key but constructors still emitted 3-key.
  Pre-edit bytes archived in this dir (`*.pre-r3` + SHAs in `README.md`).

## Code changes (DST only, via dedicated Edit; no shell source write)
1. `scripts/survey_publication_set_v2.py` (`d2909bbaead935d6fba548fb9b0c9d1178a6027685db2d8c8691b6ee8f02f2c1`,
   was `60f9f1141ccaa961003598d0692465f2a43ed310c8b780e8b1b7e9002fffc446`):
   - `before_active_digest` now accepts verified 4-key rows
     `{path,sha256,byte_count,origin}` as well as internal 2-key recompute maps;
     digest still covers `{name,path,sha256}` (stable); `byte_count`/`origin`
     validated when present.
   - New `_verified_row_4key`: reads live bytes raw-first, verifies SHA FIRST,
     cross-checks an expected stored size when supplied, then derives
     `byte_count = len(live)` (never blesses stored size without SHA check).
   - New `_anchored_canonical7`: VALIDATION_CHECKPOINT anchor -> original seven
     verified live; LEGACY_REVALIDATION anchor -> latest legacy cumulative
     effective (each link cumulative vs ORIGINAL, `prior_sha256 == original`,
     never incremental), verified live, origin ORIGINAL.
   - New `_verified_active7_from_seal`: seal seven verified live with seal
     `byte_count` cross-check, origin ACTIVE.
   - `resolve_publication_selection`: CANONICAL no-pointer returns anchored
     verified 4-key (both tables); legacy mode returns anchored for BOTH
     canonical7 and effective7 (they agree; cross-checked vs head record) with
     per-row stored-size validation incl. preserved rows; editorial
     VERSIONED_ACTIVE returns anchored canonical7 + verified active7.
     Genuine no-pointer candidate fastpath untouched.
2. `scripts/survey_agent_control_v2.py` (`05f1ee03a91b647d88bd66877e702c7044a34c6f5d44bdbeb46710375a104103`,
   was `12995a8415f8b2ee28fab783b1688f2b3012aadb045f03ad95cf7e5be3d8f78d`):
   - `_validate_checkpoint_record` editorial branch: for `validation`
     checkpoint only, expected SHAs come from low `resolve_publication_selection`
     `canonical7` (anchored cumulative, verified 4-key) instead of `superseded={}`
     + original SHA. Other checkpoints keep `superseded={}`. Pending override
     preserved. Explicit fail-closed when selection is not VERSIONED_ACTIVE.
     No research rebind, no drift bypass; low active15/effective7 still
     independently checked via selection/seal.
3. `scripts/survey_editorial_correction_proposal_v2.py` UNCHANGED
   (`79bf910d79c93768824050e92cc770ce163d235b6746f82859723b59353dd292`):
   its `VERSIONED_ROW_SHAPE` 4-key check was already correct; the bug was low's
   3-key export. No P1 edit needed.

## Focused tests (new, DST `tests/test_survey_publication_r3_anchor_shape_v2.py`, 6/6 PASS)
- R3RowShape: no-pointer 4-key verified; R1x2 anchor == latest (r2), anchored
  canonical Gate == new live bytes != original, canonical7 == effective7 in
  legacy mode, all rows exact 4 keys with live-derived sizes; low output
  satisfies P1 `VERSIONED_ROW_SHAPE`.
- R3Refusal: stored `byte_count` mismatch refused; live drift refused; digest
  rejects bad origin, accepts 4-key (stable value vs 2-key).
- R3AgentAnchor: live Gate == anchored canonical7, != original (the exact old
  POSTREPLACE_FAIL premise); agent now checks anchored.
- Raw: `r3-focused-stdout/stderr/exit.txt` (exit 0). Pinned source at test time:
  low `d2909bba...`, agent `05f1ee03...`, P1 `79bf910d...` (unchanged).
- Existing: low18 17/18 + agent control5 5/5 (`r3-existing-low-agent-*`, exit 1).
  Single failure is `test_r1_anchor_and_live_effective`, which encodes the OLD
  buggy expectation ("canonical7 keeps original refs") — now correctly anchored
  (`5c02...` live vs `17e6...` original). NOT edited; left for root disposition
  with failure evidence preserved.
- P1 suite `test_survey_editorial_correction_proposal_v2` (9 tests) errors in
  SETUP (`init_profile` -> `contract_identity`: `contract file does not exist:
  schemas/editorial-manuscript-spec-v2.schema.json`), pre-existing DST
  config-vs-old-helper mismatch, unrelated to this fix (P1 module unedited,
  config untouched by this worker). Raw in `r3-p1-*`.
- No claim of real second correction / R1 repeat from pure tests. New
  `__pycache__` growth during runs is untracked residue, preserved (runs used
  `-B`; no clean per instruction).

## New frozen SOURCE snapshot (untouched, tests never run inside)
- Root: `/tmp/opencode/jgas-editorial-r3-20261021T093525Z/candidate-partial-b40de60`
- HEAD `757cbfe4d085462e4edb1ce8a9f19dc34e7e148a`, tree
  `45b66ea881f864ba338a21286a6e0bd0e9ef30fa`, status clean (0), 718 files
  (689 materialized tracked + 29 new: R2 28 + R3 focused test).
- Excludes `__pycache__`/`tmpvr07sdme` residue (0/0/0). Valid JSON manifest
  `source-manifest-r3.json` in this dir (718 entries, path/sha256/bytes/mode;
  manifest SHA `cb656bcd878e9f0442a1cbc8f477867ccb8eba868a5f3b158906bf974a6a0eda`).
- Key pins: low `d2909bbaead935d6fba548fb9b0c9d1178a6027685db2d8c8691b6ee8f02f2c1`;
  agent `05f1ee03a91b647d88bd66877e702c7044a34c6f5d44bdbeb46710375a104103`;
  P1 `79bf910d79c93768824050e92cc770ce163d235b6746f82859723b59353dd292`;
  new test `ab6c9ca422f32c12398482d0edd2d0dc591f97e7e96fa476164a8baecab4400b`.
- Commit `worker-r3-fix <worker-r3-fix@example.invalid>`, inert origin
  `https://example.invalid/workerR3-r3snapshot.git` (never fetched). No
  alternates; inodes distinct vs DST (`45:553197` vs `45:780412`, links 1);
  zero files with links>1; DST HEAD still `409b292...`.
- Future work only in clones of this snapshot. STOP at internal return.
