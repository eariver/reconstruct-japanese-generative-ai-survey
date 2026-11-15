# Repaired correction rehearsal — independent runtime setup (FIRSTOPERATION)

Date (actual UTC): 2026-11-12T12:57:10Z start, setup dir `setup-20261112T125743Z`, new runtime `repaired-correction-rehearsal-20261112T125743Z`.
Authorizing packet: `notes/rephase-1-repaired-correction-rehearsal-20261112/README.md` FIRSTOPERATION, prior assessment §5 + root closeout FULL + independent §8 FINAL-BINDING read.

## New independent copy

- NEW_WORK: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`
- HEAD: `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325`
- Parent (copied actual e84 ancestry): `e84a82aca000c990597ea8cf60f548e2ff187bd1`
- Parent of e84: `480823560c0c26ed2e5baa18e0e79a22b2839a27`
- Tree (new): `ed2dc4ddd4a9486ccc9d0944bbd48653199b2485`
- Old tree (e84): `fb8e536ed2860acef8feb2eac7992a69e4b03ae9`
- Old HEAD verified: `e84a82aca000c990597ea8cf60f548e2ff187bd1`, parent `480823560c0c26ed2e5baa18e0e79a22b2839a27`, shallow `774dd39a951c9ac3818e83dfffd4c7666efb0a20`
- No network clone: `cp -a` from saved e84, exit 0. Inert origin `https://example.invalid/rephase-candidate-recovery.git` retained.
- Independence: `.git` is dir (no gitdir file/link), no `commondir`, no `worktrees`, no `objects/info/alternates` (no shared objects), 0 symlinks in bound roots, 0 hardlinks (`find -links +1` 0), inodes differ old vs new (index 24645184 vs 22452497, HEAD 24645197 vs 22452498, sample source 24645163 vs 21404139), object count 213 preserved pre-copy, 223 post-commit (+10). No reconstruct Git/status/HEAD/log/readback, no `git -C .`.

## Baseline preserved

- Copied all materials/history/State/CP bytes without cleanup. `git status --porcelain` identical old vs new pre-install (23 lines: 10 M materials + 13 ?? groups). Logs `HEAD` identical.
- Old source pins: LOW `0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b`/218692, HIGH `388c89941cef393868c9a2cef5ad7276889ffa01aeda294e756c9f76b6f9efd4`/92741, C `6ffde575a21b3748147fda3f662d7934a78c5082a062a4f174519d4902aee585`/42156, scaling `d486809c4ae88c0e78784ade8e456cd9227b25a29c12cde9700664a1eec3edad`/91561, supplement 2 absent expected.
- Expected partial-DB qualification: `git diff --stat` fails `fatal: unable to read 99c34b75b9e5f52d3c19897c24939ce3d14a1f62` (indexed `sources/2026-W34/discovery/discovery-accepted-v2.json` blob missing, `cat-file` not valid object). `status`/`ls-tree`/`rev-list --count 15` succeed. Preserved, not a setup failure; file-level hashes used.

## Exact773 install (no patch overlay)

- Manifest verified actual: `a7e40c4711a66b4d1d2541e6af1a97fd0e531d217e233f45ce43b40e19cef40c`/202833B, patch `171812f686c05d8494de8bd32a6c00e043dc5ff1aa7452204a8e35f16848600d`/5532921B, head `409b292756dd1277b9dfae87679934c0d2ce251c`, 773 files.
- Installed all 773 proof-copy files into new copy via `shutil.copy2` + `chmod` to manifest `physical_mode`, verifying src hash/bytes/mode before and dst after: ok 773 fail 0.
- Precise delta old e84 -> new (computed actual):
  - `scripts/survey_research_authority_v2.py` 0974c709... -> 7f5fc9e0d79729d98345f0b0352d5070c76e93f92f2c14148e22c9f38a8f4c0f/240969
  - `scripts/survey_prearchitecture_acceptance_v2.py` 388c8994... -> f312f02e2dc5c1aa5a1d6432bca134cd83f0a1edea2d127721d0206d05514a90/97844
  - `tests/test_dm022_c_direct_operation_v2.py` 6ffde575... -> 1fa905bf7e184cb63905b05d87018e27b7b55387f450352bbd02d4ddfe888e31/43626
  - `tests/test_evidence_scaling_v2.py` d486809c.../91561 -> 7b862305db39afde93c44ca0f1ce2d4b5faf512729e6956a8166b16f09c0e12e/106616
  - `tests/test_dm022_supplement_carry_v2.py` absent -> a8aaafe35f8b602fec36491a3fd116376c426e46d3724bda546d471637693d16/65884
  - `tests/test_dm022_supplement_carry_scale_v2.py` absent -> 7118092f80b1a7a23f198b887926ec1631c7adf9f3503c7016cc693254644668/27736
  - Other 767 manifest files identical. Materials (State/Profile/Ledger/Completeness/Checkpoints) unchanged (e.g. W34 State d7acd29b..., SP State 180db8c..., checkpoints 3c64e...,4d322...,0979f...,5b991...,481d96...,1233b1... all UNCHANGED-OK).

## Isolated execution-source commit

- Staged only 6 above (`diff --cached --name-only` 6, `stat` 6 files 2073+/40-). Materials remain unstaged M + untracked ?? preserved post-add and post-commit.
- Commit: `[detached HEAD cc1c7fd]` with process-scoped `-c user.name=repaired-correction-setup-20261112T125743Z -c user.email=repaired-setup-20261112T125743Z@example.invalid`, message isolated execution source, no `--allow-empty`/`--no-verify`, no Gitconfig/HOME change (global eariver unchanged, local inert, HOME /home/eariver, hooks samples present). Exit 0.
- Index 32237 -> 32239 (+2 new), objects 213 -> 223. Committed blobs match working (`hash-object` == `ls-tree` for all 6: 7b7a5fd...,b664e42...,deacba8...,c91a2d3...,511dafb...,35019b9... OK).
- Status post-commit: 10 M materials + untracked preserved, 6 source now committed (absent from status).

## Verification from new copy

- All773 hash/size/mode OK 773/0 (LOW 7f5..., HIGH f312...).
- Committed/live/loaded module path: `sys.path[0]=new`, `low.__file__` and `high.__file__` under new, SHA 7f5.../f312... OK. `PYTHONDONTWRITEBYTECODE=1`, no `GIT_*`/`GIT_ROOT` overrides.
- Strict read-only `agent.validate_agent_state(root,cfg,state)` both PASS `[]`:
  - W34 EVIDENCE_REVIEWED, impl 48082356..., checkpoints ISSUE 3c64e..., DISCOVERY 4d322..., CANDIDATES 0979f... (evidence/materiality/completeness same file), file hashes match provenance, CP/contract/profile == old e84.
  - SP EVIDENCE_REVIEWED, impl 48082356..., checkpoints 5b991...,481d96...,1233b1..., same checks, CP/contract/profile == old.
  - Contract8 unchanged (4 SHAs per issue: pipeline 3adfbda..., quality b5b955d..., research 666f8a0.../0f575e6..., publication 99adff9.../a685955...).
- No HIGH prepare/adopt/guard/State write/Raw staging/Selection. State hashes unchanged post-setup (d7acd...,180db...).

## Successor four refs (unchanged, eligible for next)

- W34: ISSUE_INITIALIZED 3c64e40bde778b6b6ecdcf73e2403079373a79cc47bee764ed8eb5cea0de92cf, DISCOVERY_COLLECTED 4d3221d347d15a6b041703ce2cf3133546636e3066e37a02cf67f5fcbc7d4611, CANDIDATES_NORMALIZED 0979f9f7703a25c2bd3424824bc4ad9f8719e8e7bcc49c19c5573d0f70ab593a (evidence/materiality/completeness).
- SP: 5b9910c97bcbfaa4ef14ee72e59b7db0ae2e26086d2043ff470b871ba8042770, 481d965f689c2dd9fde2c7e115df2d34ba2e21adc95c7d20f4bdc099728c725c, 1233b1f6ca3301d6430d4d157788d0a45a613c9ce1e1563e7c06fe11d73993f0.
- Next blockers: none for setup; further work requires independent semantic review/adopt/resume/readback per packet, no hand-repin/rollback, no invented Raw, D142 still unfetched, no standing network.

Raw/argv/env/PID/start/end/exits/object/index in `raw/` + `data/` here. Tool deviation: none (no subagents, no network, no reconstruct readback, no source edits beyond install).
