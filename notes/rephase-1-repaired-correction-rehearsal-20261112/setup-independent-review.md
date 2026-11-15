# Independent setup review — repaired-correction-rehearsal 20261112T125743Z

Reviewer: independent setup reviewer (not operator/authors).
Scope: setup only. No operational authority to prepare/adopt, stage Raw, write guard, change State, or start Selection.
Method: Read tool + stdlib hashing/stat (sha256sum/python `hashlib/os/stat/zlib`), file/inode inspection, `.git` file reads + zlib decode. No project imports, no run/tests, no network, no reconstruct Git/status/HEAD/readback, no source writes, no subagents, no Git binary.

## 1. Source epoch and ancestry (via saved raw + `.git` files, no exec)

- NEW work: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`
- `.git/HEAD` (Read): `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325`
- `.git/logs/HEAD` (Read, 6 lines): `... 48082356 -> e84a82aca000c990597ea8cf60f548e2ff187bd1 -> cc1c7fd1cf979e71fda4ae2164828b37bc1b2325`, with isolated-execution message, process-scoped identity, timestamp `1794488479 +0900`.
- zlib-decoded commit objects (no git binary):
  - `cc1c7fd`: `tree ed2dc4ddd4a9486ccc9d0944bbd48653199b2485`, `parent e84a82aca000c990597ea8cf60f548e2ff187bd1`
  - `e84a82ac`: `tree fb8e536ed2860acef8feb2eac7992a69e4b03ae9`, `parent 480823560c0c26ed2e5baa18e0e79a22b2839a27`
- Saved raw agreement: `data/new-HEAD.txt`, `data/final-HEAD.txt` = `cc1c7fd...`; `data/new-commit-cat.txt` tree/parent/message match decode; `data/new-show-stat.txt` 6 files `2073+/40-`; `data/new-parent-post.txt`/`final-parent.txt` = `e84...`; `data/old-parent.txt` = `4808...`; `data/new-tree-post.txt`/`final-tree.txt` = `ed2dc4...`; `data/old-tree.txt` = `fb8e53...`.
- Label note (non-blocker): `data/new-parent.txt` holds `4808...` (old's parent) and `data/new-tree.txt` holds `fb8e...` (old tree); correct new values are in `new-parent-post.txt`/`final-tree.txt` and decoded commit. Do not cite the two misnamed files as new identity.
- Claimed source epoch `cc1c7fd...`, parent copied `e84...`, tree `ed2dc4...`: CONFIRMED.

## 2. Final source manifest and 773 verification (independent)

- Manifest file: `notes/rephase-1-supplement-carry-repair-20261106/source-packaging/final-20261107T040903Z/complete-supplement-carry-manifest.json`
- Independent: bytes `202833`, sha256 `a7e40c4711a66b4d1d2541e6af1a97fd0e531d217e233f45ce43b40e19cef40c`, `files_len 773`, head `409b292756dd1277b9dfae87679934c0d2ce251c`. Matches `data/manifest-sha.txt`, `manifest-parse.txt`, `manifest-bytes.txt`.
- Independent recomputation over NEW work for all manifest entries (sha256 + bytes + `physical_mode`): `ok 773 fail 0`.
- Six installed delta (old e84 -> new), independently recomputed old and new, matches manifest and `data/postinstall-delta.txt`:
  - `scripts/survey_research_authority_v2.py`: `0974c709...` 218692 -> `7f5fc9e0d79729d98345f0b0352d5070c76e93f92f2c14148e22c9f38a8f4c0f` 240969
  - `scripts/survey_prearchitecture_acceptance_v2.py`: `388c8994...` 92741 -> `f312f02e2dc5c1aa5a1d6432bca134cd83f0a1edea2d127721d0206d05514a90` 97844
  - `tests/test_dm022_c_direct_operation_v2.py`: `6ffde575...` 42156 -> `1fa905bf7e184cb63905b05d87018e27b7b55387f450352bbd02d4ddfe888e31` 43626
  - `tests/test_evidence_scaling_v2.py`: `d486809c...` 91561 -> `7b862305db39afde93c44ca0f1ce2d4b5faf512729e6956a8166b16f09c0e12e` 106616
  - `tests/test_dm022_supplement_carry_v2.py`: ABSENT -> `a8aaafe35f8b602fec36491a3fd116376c426e46d3724bda546d471637693d16` 65884
  - `tests/test_dm022_supplement_carry_scale_v2.py`: ABSENT -> `7118092f80b1a7a23f198b887926ec1631c7adf9f3503c7016cc693254644668` 27736
  - All modes `0o664`. Other 767 manifest files identical (773 total - 6).
- Setup `install-summary.json` `ok 773 fail 0` and `verify-773-new.txt` 6 hashes: independently CONFIRMED.

## 3. Object-DB independence (file/inode, no Git binary)

- NEW `.git` is dir (not file/link/gitdir). `commondir` absent, `worktrees` absent, `objects/info/alternates` absent (NEW and OLD both `No such file or directory` in saved raw, re-confirmed via `test -e`).
- No `GIT_*` overrides in setup env (per `strict-validation.txt` `GIT_DIR=None` etc., `live-loaded-modules.txt` sys.path[0]=new).
- Inodes differ OLD vs NEW (independent `ls -i`):
  - HEAD: OLD `24645197` vs NEW `22452568` (saved `data/inode-head-compare.txt` showed NEW `22452498` pre/post-commit transient; current still distinct from OLD, independence holds)
  - index: OLD `24645184` vs NEW `22452497` (matches saved)
  - sample source `survey_research_authority_v2.py`: OLD `24645163` vs NEW `21404139`
- Symlinks: 0 in OLD and NEW bound roots (full walk). Hardlinks (`st_nlink>1`): 0 in NEW.
- Object counts via filesystem (`find objects -type f`): OLD `213`, NEW `223` (+10). Matches `data/old-object-count.txt`/`new-object-count.txt`, `precommit/postcommit` counts, `index 32237->32239` (+2 new).
- Remote (Read `.git/config`): `https://example.invalid/rephase-candidate-recovery.git`, inert. No `reconstruct` remote, no alternates, no worktree link.
- No reconstruct Git readback performed by reviewer. Independence: PASS.

## 4. Checkpoint vs artifact correction (setup owner mislabel)

Setup `README.md` §54 lists under “Successor four refs” three checkpoint file hashes (ISSUE `3c64e...`/`5b991...`, DISCOVERY `4d322...`/`481d96...`, CANDIDATES `0979f9...`/`1233b1...`). Those are Discovery/Screening/Evidence checkpoint refs, not the four research-artifact refs.

Actual four research-artifact refs are in the Evidence checkpoint `CANDIDATES_NORMALIZED.json` `artifacts[]` (Read both issues in NEW work, file hashes re-verified, OLD vs NEW identical):

W34 (`sources/2026-W34/...`, checkpoint `0979f9f7703a25c2bd3424824bc4ad9f8719e8e7bcc49c19c5573d0f70ab593a`):
- `edition-views-acceptance`: `sources/2026-W34/evidence/v2/views/accepted/574b96ff3ce87f7f2e46fcd78724bf1fbfcdad590e009be1500f03446697b5c5/edition-views-accepted.json`, `3777133cc09d0189ab97cc1d8ff1f8b420108d43880f69f1745356508b8acfce`, 159498B
- `evidence-acceptance`: `sources/2026-W34/evidence/v2/accepted/5ca6f31033dcaed6a153f0eb6f838f18bc9bdd1674a19a941f8c8378f88e4e48/evidence-accepted.json`, `edf21e4de5f7ab8db2d5189f45abc8cc6d0cf6475e532b20bcc56b0ce5660218`, 126592B
- `materiality-ledger`: `sources/2026-W34/materiality-ledger-v2.json`, `f089cc4eedb49a81b4b925c1219f22a77237d16f28fdee73f20a3744e725e91d`, 186202B
- `profile-completeness`: `sources/2026-W34/profile-completeness-v2.json`, `e8c432dd6275e81df5286cb8c0d55d99e27aa0812c52a114d870dddaf0d2795f`, 71532B

SP (`sources/SP-efficient-llm-2026/...`, checkpoint `1233b1f6ca3301d6430d4d157788d0a45a613c9ce1e1563e7c06fe11d73993f0`):
- `edition-views-acceptance`: `sources/SP-efficient-llm-2026/evidence/v2/views/accepted/5e722402c7e8df6077f87f0da33b2b53355f22ae3f306482dedbd27350b7145f/edition-views-accepted.json`, `1557fef75b4b737379a0e84eea983d9151b7148077f65da018206a2fae2b0341`, 64222B
- `evidence-acceptance`: `sources/SP-efficient-llm-2026/evidence/v2/accepted/73f4bc1ec69c70925a7119a0327ff5e6f024812b56cf8edd7c49eae9f672a297/evidence-accepted.json`, `65784e69559f9379412935fa5e7671beddee59b46b8fdb28a848d450e2b68ce0`, 49237B
- `materiality-ledger`: `sources/SP-efficient-llm-2026/materiality-ledger-v2.json`, `b7c85b4eb009249b355445f94a4041d4374990fccb07c38595b61c1e770c8c60`, 66850B
- `profile-completeness`: `sources/SP-efficient-llm-2026/profile-completeness-v2.json`, `d67f7f8363407b30d58dbe2dbe562b3666ea9483f9f16303859cfe459ab5e805`, 33683B

Source-root paths same OLD vs NEW (relative paths identical); new absolute root is NEW work above. All eight artifact files exist at stated paths with matching bytes. Checkpoint files themselves byte-identical OLD vs NEW.

## 5. State / Profile / Contract8 / CP (old accepted sets unchanged)

- Production-State (Read NEW): both `EVIDENCE_REVIEWED`, `implementation.repository_commit_sha 480823560c0c26ed2e5baa18e0e79a22b2839a27`, `human_gates pending/pending`, `human_gate_provenance null/null`, `machine_checkpoints` discovery/screening/evidence/materiality/completeness `passed`, selection/architecture/draft/validation/preview/freeze/release `pending` (seven absent), `exception_gate inactive`, `target_gate ARCHITECTURE_REVIEW`, `next_action stage:selection`, `history` last `CANDIDATES_NORMALIZED->EVIDENCE_REVIEWED` at `e84...` (2026-11-05). No new research transition, no repin/rollback.
- State file hashes identical OLD vs NEW: W34 `d7acd29b1518399ffc2376eb07e102491a6ec9782b3fdd79815c5f230e1886b0`, SP `180db8c30721825d40461cd5e1b92edb704f3630f518bfd693b4732211538220`.
- Profile/Contract8: state-embedded + checkpoint-embedded contracts match setup claim and are unchanged (state files identical). W34 research `666f8a064b190...`, publication `99adff93ff44...`; SP research `0f575e6d97ca...`, publication `a6859559dd1b...`; pipeline `3adfbda22131...`, quality `b5b955d524fb...` both issues. Profiles: W34 `2a8c3089cec2...`, SP `aff05fd573ce...`.
- Copied materials (14 paths: State/Profile/Ledger/Completeness + 3 checkpoints x2 issues) independently re-hashed OLD vs NEW: all UNCHANGED (prefixes `d7acd29b1518`, `2a8c3089cec2`, `f089cc4eedb4`, `e8c432dd6275`, `3c64e40bde77`, `4d3221d347d1`, `0979f9f7703a`, `180db8c30721`, `aff05fd573ce`, `b7c85b4eb009`, `d67f7f836340`, `5b9910c97bcb`, `481d965f689c`, `1233b1f6ca33`).
- `final-status.txt` 10M + 13?? preserved; materials remain M/untracked post-add/post-commit per `postadd-status.txt`/`postcommit-status.txt`; six source now committed (absent from status). No State/Profile/CP write.

## 6. Code validation, loaded paths, guard absence

- `data/strict-validation.txt` (setup operator run, read-only): `validate_agent_state errs []` both issues, `ALL STRICT READ-ONLY VALIDATION PASS`, `exit 0`.
- Loaded paths (Read): `agent .../new/.../survey_agent_control_v2.py`, `core .../new/.../survey_production_v2.py`, `sys.path[0]=new`, `low.__file__`/`high.__file__` under NEW with `low 7f5fc9e0...` / `high f312f02e...` matching manifest. `LIVE LOADED OK from new copy`.
- Bound source: six committed blobs match working (`data/blob-match.txt` 6 OK, `committed-blobs.txt` `7b7a5fd.../b664e42.../deacba86.../c91a2d35.../511dafbc.../35019b95...`).
- Guard: no guard written; exception inactive; no HIGH prepare/adopt/Raw staging/Selection (setup README §52 + strict validation + state hashes unchanged post-setup per `final-state-hashes.txt`).

## 7. Partial-DB diff failure (known qualification, not clean claim)

- `data/old-diff-exit.txt` `exit:128`, `old-diff-stat.txt`/`old-diff-nameonly.txt` `fatal: unable to read 99c34b75b9e5f52d3c19897c24939ce3d14a1f62`, `old-missing-cat.txt` `fatal: Not a valid object name ...`, `old-missing-obj-ls.txt` pins indexed blob `99c34...` for `discovery-accepted-v2.json` and `canonical-discovery-accepted-v3.json` (stage 0).
- Setup README §22 correctly calls this “Expected partial-DB qualification … Preserved, not a setup failure; file-level hashes used.” `status`/`ls-tree`/`rev-list --count 15` succeeded per README. Reviewer makes no all-history/tree-clean claim; scope is 773 intended files + materials, not full hydrated/tree-clean or all-history proof. No unqualified clean-diff claim found.

## 8. Verdict

**SETUP_READY** — bounded setup scope only.

- Exact773 installed and committed on copied e84 ancestry with only six intended changes; materials/State/Profile/Contract8/CP old accepted sets preserved; DB independent; ancestry/tree/commit verified without Git binary; correct four artifact refs established; both EVIDENCE_REVIEWED with init480/human pending/seven absent/guard absent; validation `[]` with new loaded paths; partial-DB failure properly qualified.
- Blockers: none for setup.
- Non-blocker notes: (a) `new-parent.txt`/`new-tree.txt` misnamed (old values; use `new-parent-post.txt`/`new-tree-post.txt`/decode); (b) HEAD inode transient vs saved (still independent); (c) setup “four refs” wording corrected in §4 above — next operations must bind the eight artifact SHAs/paths in §4, not checkpoint file hashes.
- No authority granted by this review to prepare/adopt, stage archive Raw, write guard/Selection, fetch D142, or use standing network. Next requires root dispatch + independent content decision/review per `astra-operation-resolution.md`.
