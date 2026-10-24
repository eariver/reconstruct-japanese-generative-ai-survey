# Bootstrap fixtures — source/guard record (read-only copy handoff)

2026-10-23. Test/fixture Co-Worker ONLY. No writable candidate runtime edits.
Whole operation ongoing, not closeout.

## Baseline inputs (READONLY, preserved)

- Proof-copy (actual409 + intended57, DIRECT409 patch 659063dc/2018112B):
  `.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`
  HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aeda2b`
  `git status` 57 modified (25M32A pattern per editorial packet), unchanged by this unit.
  Worktree 721 files (scoped689+32, missing26309/bulk31466/runtime/TeX retained).

- Baseline SOURCE synthetic (preferred retained meaningful old source commit):
  `.rephase-1-editorial-runtime/jgas-editorial-r7b-20261023T034500Z/candidate-partial-b40de60`
  HEAD `721a04d85532d7855f3e54cc411f5847c787726e`
  tree `ac7cb0bd2e977b46e957450816eddd779799e144`, `git ls-files` 721.
  Matches `notes/rephase-1-editorial-operation-implementation/correction-r7/source-manifest-r7b.json`
  (count 721, same HEAD/tree). Worktree excl `.git` = 725 (721 + 4 `__pycache__/*.pyc`), excluded.
  Commit message: `SOURCE R7b TEST-ONLY: DM004 python-launcher PATH + missing-record oracle + workspace scratch`.
  This is synthetic source identity, NOT actual candidate409 ancestry.

- M1 corrected candidate (writable runtime, NOT edited here):
  `.rephase-1-editorial-runtime/versioned-renewal-impl-20261023T181352Z/candidate-work/`
  HEAD `a8890d4ff612563e71b7dcf5db76287acfe4ea35` (3 fixture commits, code before authorities),
  `git status` clean (0 lines with correct `--work-tree`), preserved.

- Reconstruct HEAD at start: `c5b0d7cff9f978a2823f9a9e00ae1e0f9d5b3e1f` (Human commit, clean except untracked `notes/rephase-1-versioned-renewal-implementation/`).
  No ordinary candidate/reconstruct commit/push in this unit.

## Fresh isolated DB workspaces (new, under `.rephase-1-editorial-runtime/`)

Parent: `.rephase-1-editorial-runtime/versioned-renewal-bootstrap-20261023T194449Z/`
- `bootstrap-weekly/` — independent Git DB, cloned `--no-hardlinks` from 721 fixture.
  HEAD `721a04d85532d7855f3e54cc411f5847c787726e`, tree `ac7cb0…`, ls-files 721, worktree excl `.git` 721, no `__pycache__`.
- `bootstrap-longform/` — same pins, independent DB.
- `scratch-tmp/weekly/`, `scratch-tmp/longform/` — external TMPDIRs (PYTHONDONTWRITEBYTECODE=1).
- `notes-tmp/` — unused placeholder (evidence lives in notes packet, DBs not in notes).

Isolation verified BEFORE commands (no GIT_* env):
- `.../objects/info/alternates` absent in both (no alternates).
- Inert origins: `https://example.invalid/versioned-renewal-bootstrap-weekly.git`,
  `https://example.invalid/versioned-renewal-bootstrap-longform.git` (no file:// after set-url).
- Inodes disjoint: HEAD blobs `21527371` (orig) vs `21628545` (weekly) vs `21629344` (longform), same device 2050, distinct inodes, no hardlink sharing.
- `git status` clean (0) before authorities in both; HEAD unchanged after activation (authorities are uncommitted worktree files, commit-before-authorities satisfied by retained 721a04d commit).
- No fixture objects in reconstruct DB. No `git clean/reset`, no old runner exec, no network, no log truncation.
- Saved packet runners are READ REFERENCE ONLY (R4e weekly/longform scripts read, not executed).
- Source library function reuse permitted: `p1t._new_weekly_helper/_build_weekly_validated/_stage_*`,
  `p3st._weekly_prepare_from`, `p1t._new_longform_helper`, `core/edpub/reader_pub/reader_gate/pubmod/setmod/retention/observer/staged/agent` imported FROM fixture `FIX_ROOT` via `sys.path.insert(0, FIX_ROOT)`.
- Existing `_make_*_source_root` helpers NOT used unchanged (they yield 674/684/686/696, not 721). Used exact 721 via `git clone --no-hardlinks` of 721a04d DB (721 files, no pycache).
- Runtime source imports FROM fixture module paths; current committed control roots (`config/survey-production-v2.json` inside fixture) used. NewH source from M1 candidate-work NOT used (baseline old57 only).
- Code helpers write fixture-only paths; no original source cache mutation (PYTHONDONTWRITEBYTECODE=1, TMPDIR under workspace scratch, workspace=FIX_ROOT for longform helper).

## Toolchain (local only)

- `/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/lualatex` — LuaHBTeX 1.24.0 (TeX Live 2026).
- `.../biber` — version 2.22.
- `/usr/bin/python3` — 3.14.4, jsonschema 4.23.0, pypdf 6.16.2.
- Fixed recipe `lualatex-biber-lualatex`, `argv == edpub.EXPECTED_ARGV_LUALATEX_BIBER` (4 steps), `mspec` actual architecture coverage.
- Initial longform helper blankPDF is type fixture only; editorial new PDFs are REAL TL2026 (5 pages each, see evidence).

## Harness

NEW file (dedicated editor, not bash heredoc):
`notes/rephase-1-versioned-renewal-implementation/bootstrap-fixtures/run_bootstrap_fixture.py`
- Args: FIX_ROOT NOTES_DIR EXPECT_HEAD EXPECT_TREE EXPECT_COUNT KIND PROPOSAL_ID.
- Guarded: GIT env check, TMPDIR-under-scratch check, HEAD/tree/count, no alternates, inert origin, clean status, toolchain exists.
- Sequence: bootstrap VALIDATED_DRAFT → P1 → P2R (+after-capture refusal) → scope → P2V → P3S50 → specs → prepare REAL → QA + synthetic reviews (actual builders) → finalize → validate_prepared_set → activate → strict State prePreview & history (no Preview).
- Failed partials preserved (no TemporaryDirectory autodelete, failure marker `bootstrap-<kind>-FAILURE.txt`, FIX_ROOT retained).
- Both runs child exit 0. Raw logs: weekly `evidence-weekly-.../run-combined-...txt` (transcribed tool-observed), longform `evidence-longform-.../run-combined-...txt` (tee-preserved).

## Limits

- Single correction per fixture (first activation, supersedes None). No C→U→U, no renewal→editorial, no normal direct Candidate/Preview/Freeze/Release with real PDF where C (beyond bootstrap), no explicit failure/resume oracles, no affected regressions — required successor scope, not claimed.
- Synthetic semantic/visual reviews are clearly synthetic (reviewer `bootstrap synthetic ...`, no genuine Human approval). No freeze/adoption. Production semantic NO-GO preserved.
- No model manual JSON acceptance as genuine public positive.
