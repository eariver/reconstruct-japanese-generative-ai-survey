# CURRENT proof — supplement-carry new runtime (independent runner, weekly LayerB)

Packet: `notes/rephase-1-supplement-carry-repair-20261106/current-proof-20261107T035000Z/`
Role: independent CURRENT-proof runner (not author, not reviewer, no subagents). Read repair README + `astra-implementation-resolution.md` FULL, frozen workcopy bounds, final tests; hashed full 773 before/after. Author/proof/e84 unchanged. Reused existing fixtures + prior evidence-scaling CURRENT supplement as DATA reference only; did NOT rerun old saved harness.

## Source bounds (verified pre/post identical)

- Workcopy: `.rephase-1-editorial-runtime/supplement-carry-implementation-20261106T131722Z/candidate-work`, HEAD `5eef790bd8d492c557cc4db9c29425e3e410d47d` (new root, NOT 409 ancestry), inert origin, no alternates.
- Intended 773 = 771 tracked (`git ls-files --cached` 771) + 2 untracked new tests; `pins-workcopy-773-before.txt` == `pins-workcopy-773-after.txt` YES (773 rows).
- Worktree SHA256 pre/post identical: LOW `d50282bf0812a4d07e3da13cf3574961add0466cd27a3ef3c648b89fe40330dd` (239978B), HIGH `f312f02e2dc5c1aa5a1d6432bca134cd83f0a1edea2d127721d0206d05514a90` (97844B), NEWTEST `5d5d3aadec70bc5d5c22fdec3e3c65d4f38d73aa995d326d8927fb8f73e26f00` (60569B, 14 tests), NEWSCALE `7118092f80b1a7a23f198b887926ec1631c7adf9f3503c7016cc693254644668` (27736B), CTEST `1fa905bf7e184cb63905b05d87018e27b7b55387f450352bbd02d4ddfe888e31`.
- Porcelain post same 5 lines (3M + 2??), `diff --stat` 3 files 487+/39-, HEAD unchanged, no author commit.
- Proof-copy LOW `0974c709…` mtime same, e84 `e84a82aca000…` HEAD same — untouched, no writes.

## Fixture (new independent DB, process-scoped identity only)

- Fixture: `.rephase-1-editorial-runtime/supplement-carry-current-proof-20261107T035000Z/fixture-20261107T034735Z/work`, HEAD `bd69c5563c4525f5b78a4a1f9ade978b6257530c` (new commit on bootstrap-weekly ancestry `721a04d…`, no reconstruct DB objects, no alternates, `nlink==1`, inert origin `example.invalid`, no `git config`/HOME rewrite, no `--allow-empty`, no hooks bypass, no remote push).
- Copy: bootstrap-weekly + workcopy source via `shutil.copyfile` (no hardlinks, no `.git`/`__pycache__`/`*.pyc`/`.rephase-1-editorial-runtime`), `git add` source paths, `git commit` with `GIT_AUTHOR_*`/`GIT_COMMITTER_*` + `GIT_CONFIG_NOSYSTEM=1` + `GIT_CONFIG_GLOBAL/SYSTEM=/dev/null` + `GIT_OPTIONAL_LOCKS=0`.
- Loader: `sys.path.insert(0, work)`, pop `scripts.*`, import `src`/`hist`/`high`/`core` + test helpers from fixture work, assert `__file__.startswith(work)` before authority; fixture `git show HEAD:<rel>` SHA == live == workcopy for `source/history/high/LOW/Evidence` (committed tool bytes, not manual fake proof/stub/role hash).
- Helper: `tests/test_versioned_renewal_source_phase_s.py` `b52692c34488…` from fixture work (existing API/test helper, DATA reuse).

## Actual API outcome (real `verify_renewal_source_proof`, weekly LayerB, no PDF)

- Issue `2026-W37`, prop `wk-boot-1`, route `WEEKLY_GENERATED_V2`, renewal `supplement-carry-current-w1`.
- `_basis_for` (real HIST verdict, real contract, real observed bindings) + `_full_valid_proof` (real trio/old refs, Layer-A digests, CURRENT G76 closure 70/contract/HIST) → `src.verify_renewal_source_proof(work, basis_rel, proof_rel)` returns `CURRENT_PROOF_VALID is True`.
- `basis_file_sha256 db7b1abc5b76…` == live basis bytes, `basis_self_sha256 e8487c2be112…` == basis field, `proof_sha256 42d8ab1cce99…`, `closure_len 70` with `d50282…`/`f312…` (new runtime, not final139 `0974c709…`/`388c899…`). Live State unchanged.
- SAME stored proof negative: mutate disposable fixture `scripts/survey_research_authority_v2.py` (+1 comment line, orig preserved), invoke SAME `basis_rel`/`proof_rel` bytes → `RenewalSourceError: BASIS_CURRENT_TOOL_DRIFT: proof closure drift: scripts/survey_research_authority_v2.py` (SAME proof/basis bytes unchanged during refusal). Restore orig → `CURRENT_PROOF_VALID True` (`verify-repair.json`). No code coercion, not active State rollback/cleanup.
- Raw: `raw/argv.txt, env.txt, cwd.txt, pid.txt, wall-start/end.txt (20261107T034735Z–034744Z, 9s), exit.txt 0, stdout.txt, stderr.txt (empty), helper-hash.txt 07c29183… (22141B), workcopy-post.txt, fixture-check.txt, pins-same.txt YES, proof-e84-post.txt, meta.txt`; `data/` has `renewal-basis.json (e8487c2b…)`, `renewal-source-proof.json (42d8ab1c…)`, `current-code-closure.json (70)`, `manifest.json`, `verify-positive.json`, `verify-repair.json`, `drift-refusal.txt`, `repair-positive.txt`, `pins-workcopy-773-before/after.txt (773 same)`, `pins-fixture-source.txt`, `helper-sha.txt`.

## Qualified scope, helper failures distinct

- Weekly only via LayerB `full_valid_proof` (no HIGH finalize toolchain, no PDF build, no stub); longform via existing 7/8/3 consumers + family 6/graph 8 labelled not re-proven here. No closure-assertion-only `CURRENT`; genuine approvals vs synthetic fixture labels preserved (`phase-S-test (synthetic, non-genuine)`, `SYNTHETIC_FIXTURE_*`, `example.invalid`, no Human approval, no RELEASED claim).
- Helper failures distinct: none in this run (exit 0, stderr empty); HIGH U finalize toolchain not attempted per scope (prior TeX block preserved as history, not re-run).
- No author source commit, no reconstruct `git -C .`/status/log/HEAD/readback, no network/Production, no extra PDF/full high pub suite; stopped on no unexpected setup/contract failure (none, no widening/local rerun).
- Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Ordinary Commit/Push Human-owned.
