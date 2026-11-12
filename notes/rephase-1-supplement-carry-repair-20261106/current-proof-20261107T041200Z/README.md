# CURRENT proof v3 — §8 new runtime (independent runner, weekly LayerB only)

Packet: `notes/rephase-1-supplement-carry-repair-20261106/current-proof-20261107T041200Z/`
Role: independent CURRENT-proof runner (not author, no subagents). Reviewed/adapted `current-proof-20261107T035000Z` harness into new namespace with fresh actual hashes; did NOT blind-exec old runner or reuse static old pins. Old `035000Z` (LOW `d50282`) preserved pre-§8, superseded not overwritten.

## Source bounds (verified pre/post identical)

- Workcopy: `.rephase-1-editorial-runtime/supplement-carry-implementation-20261106T131722Z/candidate-work`, HEAD `5eef790bd8d492c557cc4db9c29425e3e410d47d` (new root, NOT 409 ancestry), inert origin, no alternates.
- Intended 773 = 771 tracked + 2 untracked; `pins-workcopy-773-before.txt` == `pins-workcopy-773-after.txt` YES.
- Worktree SHA256: LOW `7f5fc9e0d79729d98345f0b0352d5070c76e93f92f2c14148e22c9f38a8f4c0f` (240969B), HIGH `f312f02e2dc5c1aa5a1d6432bca134cd83f0a1edea2d127721d0206d05514a90` (97844B), focused `a8aaafe35f8b602fec36491a3fd116376c426e46d3724bda546d471637693d16` (65884B, 17), scale `7118092f80b1a7a23f198b887926ec1631c7adf9f3503c7016cc693254644668` (27736B), Ctest `1fa905bf7e184cb63905b05d87018e27b7b55387f450352bbd02d4ddfe888e31`.
- Porcelain post same 5 lines, `diff --stat` 3 files 497+/40-, HEAD unchanged, no author commit. Proof-copy/e84 untouched.

## Fixture (new independent DB, process identity only)

- Fixture: `.rephase-1-editorial-runtime/supplement-carry-current-proof-20261107T041200Z/fixture-20261107T040957Z/work` HEAD `b4ca2d91e508a9a33651f2e0455cf2037744623a` (new commit `supplement-carry CURRENT proof v3: exact 7f5fc9 §8 new-runtime 773 snapshot`, bootstrap-weekly ancestry, no reconstruct objects, no alternates, `nlink==1`, inert `example.invalid` origin, no `git config`/HOME/`--allow-empty`/hooks bypass).
- Loader: `sys.path.insert(0, work)`, import `source/history/high/core` + test helpers from fixture work, `__file__.startswith(work)`; `git show HEAD:<rel>` == live == workcopy for `source/history/high/LOW/Evidence`. Helper `b52692c34488…`.

## Actual API outcome (real `verify_renewal_source_proof`, weekly LayerB, no PDF)

- Issue `2026-W37`, prop `wk-boot-1`, route `WEEKLY_GENERATED_V2`, renewal `supplement-carry-current-v3-w1`.
- `_basis_for` + `_full_valid_proof` → `CURRENT_PROOF_VALID is True`. `basis_file 18ba69a19885…`, `basis_self 9eafae9a8e1f…`, `proof fd705a9678aa…`, `closure_len 70` with `7f5fc9/f312`. Live State unchanged.
- SAME stored proof negative: disposable fixture LOW +1 line → `BASIS_CURRENT_TOOL_DRIFT: proof closure drift: scripts/survey_research_authority_v2.py` (SAME bytes unchanged). Restore → `CURRENT_PROOF_VALID True`.
- Raw: `argv/env/cwd/pid/wall 040956Z-041005Z/exit 0/stdout/stderr/helper 064eb9a3…` in `raw/`; `data/` has basis/proof/closure/manifest/`verify-positive.json`/`verify-repair.json`/`drift-refusal.txt`/pins-773/helper-sha.

## Qualified scope

Weekly LayerB only. No new Longform/family counts, no semantic/Human/R4/adoption claim. Helper failures distinct: none (exit 0, stderr empty). No source/e84/proof mutation, no ordinary commit/reconstruct readback/Production/network. Whole NOT_READY/DM021+022OPEN/audit unstarted. Ordinary Commit/Push Human-owned.
