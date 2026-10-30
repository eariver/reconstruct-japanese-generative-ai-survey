# Source disposition — FINAL DM022 pre-Architecture delivery (packaging only)

Date: 2026-10-29 UTC. FINAL source delivery packaging. No tests executed, no
source edits, no ordinary commits, no Human commit readback (no git commands in
workspace reconstruct root; all Git read-only INSIDE candidate-work or the fresh
GEN copy). No network, no fetches, no cleanup. No semantic PASS claimed; final
independent proof is a SEPARATE agent next (NOT self-labeled here).

## 1. Delivery artifacts (new unique packet, no overwrite)

`notes/rephase-1-dm022-prearchitecture-implementation/source-packaging/final-20261029T152913Z/`:

- `complete-dm022-prearchitecture-409.patch` — SHA256
  `25b488784d02a156db693459dce6c1d369e7144f1f3c49461c9b3a846b1b7260` /
  4931836B. ONE complete DIRECT actual409-relative full-index binary patch
  (`git diff --cached --full-index --binary HEAD`): 133 files, 77161
  insertions, 689 deletions. Covers ALL final deltas INCLUDING inherited 93
  (verified: old93 − new-delta = 0; no first-partial, no old-overlay layering).
- `complete-dm022-manifest.json` — SHA256
  `31fa4a728cabc145232ef930b91c9c5e6f773692299a25a9177c994393d469fa` /
  185422B. All 768 intended paths `{SHA256, bytes, git_mode, physical_mode,
  kind}` + delta inventory (`diff_M` 54, `new_A` 79) + pins.
- Raw GEN logs: `cp-git-*`, `tar-pipeline-exit`, `gen-count-*`, `gen-head-*`,
  `inode-check-*`, `gen-noalternates-*`, `gen-remote-*`, `gen-revparse-*`,
  `gen-read-tree-*`, `gen-verify689-*`, `gen-add-*`, `gen-status-*`,
  `gen-diff-names-count`, `gen-diff-stderr`, `gen-diff-stat-*`,
  `gen-diff-numstat-*`, `gen-diff-check-*` (stdout/stderr/numeric exits).
- This file. No Git DB in packet (`find -name .git` empty). Old packets
  preserved untouched.

## 2. Freeze root + isolation (ignored runtime)

`.../.rephase-1-editorial-runtime/dm022-packaging-final-20261029T152913Z/`:
`gen-copy/candidate-partial-b40de60/` (worktree 768 intended files, no `.git`;
`.git` byte-copied `cp -a` no `--link`) + `gen-index` (TEMP `GIT_INDEX_FILE`,
outside packet; candidate/root indexes never touched — candidate cached still
0, status still 54M/81??, HEAD still `409b292…`). GEN DB: 83/83 files, 0 inode
overlap vs candidate, no alternates/commondir, inert `example.invalid` origin,
HEAD `409b292…`/tree `8ce36998…`. GEN worktree == candidate intended bytes
(768/768, 0 mismatch). No proof-copy restore, no old runners.

## 3. Measured actuals (derived, not assumed)

- Intended: **768** = **689** tracked-at-HEAD + **79** untracked new
  (801 on-disk excl `.git` minus 33 `*.pyc` in 2 `__pycache__` dirs — excluded
  by declared policy, PRESERVED on disk, no cleanup).
- Actual delta vs actual409: **54M + 79A = 133 files** (measured; the
  `52M79A131` premise is superseded — M is 54: +2 C2 release/editorial
  modifications since review freeze; +4 new files: Normal 2, depth 1, B2 1).
- Base-689 availability: `git ls-tree HEAD` over exactly the 689 paths +
  `git cat-file --batch-check` on all 689 blobs → 689 lines, **0 missing**
  (fail-closed, no lazy fetch). Bulk outside intended scope
  (missing-26309-reachable / bulk31466 / runtime+TeX) NOT bundled — qualified
  below, not claimed.
- Modified tracked all within intended set (54/54). No `.tmp`/`*~` files.
  No file/symbol named `BaseModule` anywhere in candidate (read-only grep).
  All intended paths under known top dirs with expected extensions.

## 4. Pins verified (read-only)

HIGH `f8af03cc`/88603, LOW `2aef837f`/155892; agent `d801feb6`/199521, human
`101792ad`/74902, orch `491888fe`/61147, bridge `2fd8a6a2`/25617; C2 release
`b9433b9e`/14505, publication `705bcee3`/155658, refresh `dd01fa01`/96623,
editorial `3a872156`/275939; history `a9de2c97`/315610, source
`b139f493`/144597. A `_norm_path` 106× LOW / 27× HIGH.

## 5. GEN zero results (numeric exits)

`cp-git` 0, `tar` 0/0, `gen-count` 0 (768), `gen-head` 0, `inode-check` 0
(83/83 overlap 0), `gen-noalternates` 2 (= absent, expected),
`gen-remote`/`gen-revparse`/`gen-read-tree`/`gen-verify689`/`gen-add`/
`gen-status`/`gen-diff`/`gen-diff-stat`/`gen-diff-numstat` 0.
`gen-diff-check` exit **2 with 6 whitespace lines — PRESERVED diagnostics, not
suppressed with `--ignore`** (see `gen-diff-check-stdout.txt`).

## 6. Bounds / old failures (honest, no full-tree-clean claim)

- Partial DB inherited: 26309 missing reachable blobs / bulk31466 paths /
  runtime+TeX unbundled — retained qualification, unchanged by this unit.
- `git status` in GEN shows 31466 worktree-vs-index deletions (bulk not
  materialized in the scoped copy) — correctly EXCLUDED from the `--cached`
  patch (cached diff == exactly the 133 intended paths, verified
  `CACHED-EQUALS-INTENDED-DELTA`).
- No `git apply --check` against clean409 (no clean tree restored; no
  fake-root). No independent proof (separate agent next).
- No packet driver scripts shipped as source: the `/tmp/dm022-gen-*.py`
  one-shot generators live outside the packet and are NOT shipping test
  source. Shipped tests are candidate-owned known files only (list §7).
  External TeX (TinyTeX path per coordination) and system runtime paths are
  environment notes, not bundled inputs.

## 7. Intended delta file list (133 = 54M + 79A; full 768 in manifest)

New intent (79A) — 5 DM022 schemas, 2 A modules, 4 A5/B/C witness helpers, 68
further source/test additions since final93 (full bytes in manifest `new_A`):

- schemas: `dm022-preadoption-report-v2`, `dm022-revision-manifest-v2`,
  `dm022-revision-proof-v2`, `dm022-revision-request-v2`,
  `dm022-supersession-checkpoint-v2` (+ 14 further new schemas incl.
  staged-source/toolchain/versioned-renewal/publication/reader/weekly sets)
- scripts: `survey_research_authority_v2.py`,
  `survey_prearchitecture_acceptance_v2.py` (+ 12 further new scripts)
- tests: `dm022_prearchitecture_fixtures_v2.py`,
  `test_dm022_prearchitecture_acceptance_v2.py`,
  `dm022_c1_fixture_helpers_v2.py`, `test_dm022_c1_family_closure_v2.py`,
  `test_dm022_c1_h_presence_controls_v2.py`,
  `test_dm022_c1_research_graph_v2.py`, `dm022_g71_g76_fixture_v2.py`,
  `dm022_lifecycle_fixture_v2.py`, `test_dm022_full_lifecycle_v2.py`,
  `test_dm022_g71_g76_compatibility_v2.py`,
  `test_dm022_prearch_b_ordinary_consumers_v2.py`,
  `test_survey_dm022_c2_consumers_v2.py`,
  `test_survey_dm022_c2_editorial_closure_v2.py`,
  `test_survey_dm022_c2_release_decoder_v2.py`,
  `test_survey_dm022_c2_renewal_freeze_v2.py` (+ 38 further new tests incl.
  group-C, P1/P2R/P2V copy-list, renewal, longitudinal and activation-fault
  suites; Normal-24 exported 2 files, depth 1, B2-late 1 among them)
- Modified tracked (54M): 3 workflows, `config/survey-production-v2.json`, 6
  schemas (candidate/publication/quality/reader/semantic/surface sets), 35
  scripts (agent/handlers/stage/orchestrator/bridge/human-gate/drafting/
  evidence/discovery/completeness/production/profile/quality/publication/
  reader/refresh/intake/citation/handoff/execution), `templates/survey/
  jgaisurvey.sty`, 7 tests (dm004-release, execution-record, increment-b,
  publication, reader-gate, refresh suites) — exact list in manifest `diff_M`.

## 8. Freeze discipline after this pack

Runtime authors idle (explicit idle assumption: all writers STOPPED per task
premise; candidate verified untouched post-pack). Witness tests run FROM the
frozen copy; only new test files may grow later, not runtime. Any source change
after this pack requires a NEW corrected package — never overwrite these
artifacts. Stop — packaging scope only.
