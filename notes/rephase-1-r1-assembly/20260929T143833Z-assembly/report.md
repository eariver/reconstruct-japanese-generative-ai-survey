# R1 assembly milestone 1 report — e4-lineage byte-copy plus exact seven-path increment

Date: 2026-09-29. Worker: FRESH General Co-Worker (bounded assembly, not independent reviewer). Root handles final docs/review; this unit handles Git-aware assembly only. No test suites run.

## 1. Fixed identities

- Reconstruct HEAD: `a22d69308e9bbfb84cee9d8530c258a2a911d059`, branch `main`, tracking `main...origin/main`, Windows git `2.39.0.windows.2` shows clean (`## main...origin/main` only). No reconstruct commit/push by worker.
- e4 source: `e4c82692abee6acedbba07815b0d74ccefb80a7e`, tree `bc377b6b7eb1e47dacd719e0f76b5a86703f3f3e`, parent `6d87edd28a1be8893ca2ab67fed6e32e54b0de6c`, branch `codex/rephase-1-gate-cli`, fixture `/tmp/jgas-rephase-gate-cli`, inert origin `https://example.invalid/rephase-increment-b.git`. Tracked-clean except `scripts/__pycache__/` and `tests/__pycache__/`.
- R1 source: `b74db679f03908048db91420a8f262d412b8f58c`, tree `515b5e93a29ba82d87f6fa81c7ecbaf2c3701bb0`, parent `57853cb76d3189b862f1edabe46b83cfc0c7bd29`, branch `codex/rephase-1-mechanical-r1-correction`, fixture `/tmp/jgas-rephase-mechanical-r1-20260928T000710Z`, inert origin `https://example.invalid/mechanical-r1.git`. Root basis `a1a4242adaddc42427b68c18ae367c04d6cd63b4` (tree `4b0fcadc172ffc999b318dc6e39a6f0a0f218b27`) is NOT e4 ancestry. 41 historical data blobs remain unverified.
- Production baseline `774dd39a951c9ac3818e83dfffd4c7666efb0a20` unchanged.
- Patch: `notes/rephase-1-mechanical-refresh/correction/final-b74db679f03908048db91420a8f262d412b8f58c/patch-final-a1-b74db67.patch`, SHA-256 `7817fa4fc027ae0bac9bbd7e7bbd18c588ba3373b52e17730eafebe2b92aab01`, verified locally. Range `a1a4242..b74db67` (not baseline patch).
- New assembly candidate: `481dec0c0233d7871df79a07a88aa5fe2291daa3`, tree `657032438c6ed8b1c055d5a120b67b4b261a5092`, parent MUST and IS exact `e4c82692abee6acedbba07815b0d74ccefb80a7e`, branch `codex/rephase-1-r1-assembly`, fixture `/tmp/jgas-rephase-r1-assembly-20260929T143833Z`, date `2026-09-29 23:43:13 +0900`.

B and all witnesses preserved unmutated. No broad history reload, no model/provider investigation, no delegation.

## 2. Byte-copy (independent, no sharing)

Parent `/tmp` verified `drwxrwxrwt` before copy. Destination `/tmp/jgas-rephase-r1-assembly-20260929T143833Z` verified absent before copy (no-overwrite guard pass). Source HEAD/tree/tracked-clean and refs/remotes plus `no GIT_* overrides` checked before copy. Preserved source DBs not mutated at all.

Method: `cp -a /tmp/jgas-rephase-gate-cli /tmp/jgas-rephase-r1-assembly-20260929T143833Z`, exit recorded as success. Reason documented: dedicated file tools cannot recursively copy binary `.git` exactly; native copy procedure explicitly allowed for this mechanical assembly. No `git clone`/`archive`/`init`/`fresh-root`/`worktree`/`alternates`/`hardlink`/object sharing. File modes and sparse/shallow/promisor metadata preserved. No silent source filtering; pycache copied with worktree (destination status matches source: pycache-only untracked), explicitly recorded here.

Isolation verification (exhaustive, not samples):

- Destination `gitdir=.git`, `commondir=.git`, `absolute-gitdir=/tmp/jgas-rephase-r1-assembly-20260929T143833Z/.git` (own, not source). Source absolute is `/tmp/jgas-rephase-gate-cli/.git`.
- Refs identical before branch change (6 lines, including e4 plus increment-a/b, r2, freeze-b1b2, r2-original).
- `.git` is real directory, no symlinks in source or destination `.git`; no `objects/info/alternates`; no `.git/commondir` file (standalone).
- Object files: 6235 source, 6235 destination, list identical; all inodes different (0 same); all `nlink==1` (0 hardlink violations); sizes identical; SHA-256 of every object file identical (0 hash mismatches).
- `config`, `shallow` (`774dd39a...`), `info/sparse-checkout`, `HEAD` byte-identical.
- Destination HEAD/tree/branch/status after copy match source exactly. Sources still fixed at e4/b74 after copy.

No `git fsck`/retry full history (known missing blobs). No hydration/fetch/network/production/current-main/Actions. No inherited `GIT_DIR`/`WORK_TREE`/`INDEX_FILE`/`OBJECT_DIRECTORY`/`ALTERNATE_OBJECT_DIRECTORIES`/`COMMON_DIR` overrides.

## 3. Preimage and patch application

Four existing preimages verified mode/blob against BOTH e4 and a1 (index/tree-local reads, no fetch):

- `scripts/survey_agent_control_v2.py`: `100644 2940abe3cd4049769983d53ca0be269087b15977`
- `scripts/survey_reader_surface_gate_v2.py`: `100644 ea1eb652ab49eb479e17318712d84c318bfaf475`
- `scripts/survey_weekly_derivation_v2.py`: `100644 477de21e9565e7a15044bd0e5d1ae6e555394524`
- `tests/test_survey_publication_revalidation_v2.py`: `100644 01f9ce6b7561e59ac25fbb801dd27162667d30e7`

Three added paths verified absent in e4 (`ls-tree` empty, `ls-files` empty) and absent in destination pre-patch:

- `scripts/survey_weekly_mechanical_refresh_v2.py`
- `tests/test_survey_weekly_mechanical_refresh_v2.py`
- `docs/weekly-mechanical-refresh.md`

Seven paths are 4 scripts, 2 tests, 1 doc per final manifest. Patch `numstat` lists exactly those 7 (counts in manifest). `numstat` was inspected but NOT used as substitute.

Actual `git apply --check` on destination BEFORE application (fixture git `2.34.1`):

- Command: `git -C /tmp/jgas-rephase-r1-assembly-20260929T143833Z apply --check /mnt/d/Git/reconstruct-japanese-generative-ai-survey/notes/rephase-1-mechanical-refresh/correction/final-b74db679f03908048db91420a8f262d412b8f58c/patch-final-a1-b74db67.patch`
- CWD: `/tmp` via worker Python (no shell variables).
- stdout: empty. stderr: empty. Numeric exit: 0.
- At check time HEAD `e4c8269`, tree `bc377b6`, parent `6d87edd`, branch `codex/rephase-1-gate-cli`, status pycache-only untracked.
- Raw record preserved in `commands/apply-check.txt` and manifest.

Materialization via Git-aware patch application (no new code edits):

- Command: `git -C <DST> apply <same patch>`. stdout empty, stderr empty, exit 0.
- Result: 4 tracked modifications unstaged + 3 added files untracked + pycache untracked; index still e4 blobs; `diff --cached` empty. No extra changed/untracked authored paths.
- Every resulting file mode/blob/SHA256 equals b74 final copies AND actual b74 objects (worktree SHA256 vs manifest, `hash-object` vs b74 blob, `ls-tree b74` contains blob, `changed-files` copy SHA matches worktree; all 7 true; modes `644` match `100644`).
- Unrelated tree entries remain e4 mode/blob exactly, including inaccessible promisor references compared as Git tree identity metadata without hydration (example `sources/2026-W32/freeze-v0.2.md` `100644 blob c03ae4320f748f0832574af054c25778d8b39eb1` identical e4 vs DST HEAD). Inherited missing objects recorded as limitation, not full baseline application proof.

## 4. Review commit (own DB only)

New branch in own copy only: `git -C <DST> checkout -b codex/rephase-1-r1-assembly` from e4 (not imported b74 history). stdout empty, stderr `Switched to a new branch 'codex/rephase-1-r1-assembly'`, exit 0. HEAD still e4/tree bc377/parent 6d87edd at branch point.

Before commit inspected `git status`/`git diff`/`git log --oneline -10` (outputs in manifest; log shows e4 ancestry: e4c8269, 6d87edd, c04f32a, cb96ab9, e0d72c7, daa1dd3, b5d3e71, fe50c2b, 1a96491, bf32edf).

Staging: `git -C <DST> add -- <seven paths>` (exactly 7, no pycache). stdout/stderr empty, exit 0. Cached numstat/name-status show exactly A3+M4 matching patch counts.

Commit (process-local identity, actual clock, NO bypass):

- Env: `GIT_AUTHOR_NAME='R1 Assembly General Co-Worker'`, `GIT_AUTHOR_EMAIL='r1-assembly@example.invalid'`, `GIT_COMMITTER_NAME='R1 Assembly General Co-Worker'`, `GIT_COMMITTER_EMAIL='r1-assembly@example.invalid'`. No `git config` update, no `--no-verify`/`-n`, no `amend`/`reset`/`clean`, no `core.hooksPath` override.
- stdout: `[codex/rephase-1-r1-assembly 481dec0] R1 assembly: apply reviewed seven-path mechanical-refresh increment onto e4 lineage 7 files changed, 4287 insertions(+), 43 deletions(-) create mode 100644 docs/weekly-mechanical-refresh.md create mode 100644 scripts/survey_weekly_mechanical_refresh_v2.py create mode 100644 tests/test_survey_weekly_mechanical_refresh_v2.py`. stderr empty, exit 0. Hooks ran normally (no bypass flag).
- Result HEAD `481dec0c0233d7871df79a07a88aa5fe2291daa3`, tree `657032438c6ed8b1c055d5a120b67b4b261a5092`, parent exact e4, branch `codex/rephase-1-r1-assembly`, date `2026-09-29 23:43:13 +0900`. Status after clean except pycache.

Post-commit verification:

- `ls-tree 481dec0` for seven paths matches b74 blobs/modes exactly (all 7 true).
- `diff e4c8269 481dec0 --name-status` is ONLY the seven (A3+M4, sorted match).
- Full tree compare: e4 32149 entries, new 32152 entries (+3 added), 0 unrelated mode/blob mismatches.
- Log `-2` shows `481dec0 (parent e4)` then `e4c8269 (parent 6d87edd)`; e4 lineage, not b74/a1 history.
- No fixture objects created in reconstruct DB; no reconstruct commit/push; no source re-checkout.

If copy/apply/normal hook/commit had failed, raw failure would be saved as blocker; none occurred (all first-attempt exits 0, recorded in manifest `attempts`; no invented base, no disabled hooks).

## 5. Limitations (not retroactively clean)

- R1 fresh-root deviations remain: original four prohibited hook-bypass flags and round3 evidence overwrite are historical deviations, preserved in `implementation/03-return-evidence-clarification.md` and `correction/evidence-preservation-limitations.md`. Later normal commits do not undo them. This assembly uses normal hooks (no bypass) in its OWN DB only.
- 41 historical data blobs under `sources/...` remain unverified from R1 basis; e4 sparse/promisor/shallow limits explicit. No hydration. Full baseline application NOT claimed.
- Old 97-method success on b74 remains old scope; exact-code equivalence guides minimal fresh check but no automatic PASS transfer. Whole candidate NOT_READY; step 4/B3 open; canonical seven-point audit unstarted.
- Saved runners/harnesses are evidence, not safe rerun instructions. No test suites run in this unit.

## 6. Proposed minimum next checks (for root approval, not automatic)

After root review, run ONLY these four Git-aware R1 methods first (in assembly DB, no real edition State/Gate mutation), plus one read-only head-bytes diagnostic. Do NOT rerun full 97 or old suites by default.

Exact method inventory source: `tests/test_survey_weekly_mechanical_refresh_v2.py` (34 methods), `tests/test_survey_publication_revalidation_v2.py` (31), `tests/test_survey_reader_surface_gate_v2.py` (27), `tests/test_survey_gate_cli_persisted_review_v2.py` (5). Names verified in assembly worktree.

Proposed argv (example, subject to root selection):

- `python -m unittest tests.test_survey_weekly_mechanical_refresh_v2.test_first_and_repeat_success -v` — real accepted first/repeat on e4 lineage.
- `python -m unittest tests.test_survey_weekly_mechanical_refresh_v2.test_metadata_revalidation_effective_rows_then_refresh -v` — healthy prior metadata to refresh (Gate-only delta).
- `python -m unittest tests.test_survey_weekly_mechanical_refresh_v2.test_active_predecessor_not_noop_and_artifact_only_noop -v` — artifact-only/no-op refusal.
- `python -m unittest tests.test_survey_weekly_mechanical_refresh_v2.test_pre_install_control_change_unsupported -v` — unsupported pre-install control change.

Plus read-only diagnostic via worker Python in assembly DB: assembled-DB `_verify_head_bytes` at own HEAD `481dec0`/current closure vs stale e4 original control snapshot, to bind the real inherited history rather than only synthetic test roots. No real edition State/Gate mutation in assembly checkout.

If different tests are justified (e.g. Gate/CLI drift found), state why; otherwise these four plus the diagnostic are the minimum justified scope. Original 97 on b74 guides selection but does not transfer.

## 7. Files changed in reconstruct (this unit only)

- `notes/rephase-1-r1-assembly/README.md` (new)
- `notes/rephase-1-r1-assembly/20260929T143833Z-assembly/manifest.json` (new, noncompact)
- `notes/rephase-1-r1-assembly/20260929T143833Z-assembly/report.md` (this file, new)
- `notes/rephase-1-r1-assembly/20260929T143833Z-assembly/commands/apply-check.txt` (new)
- `notes/rephase-1-r1-assembly/20260929T143833Z-assembly/commands/apply.txt` (new)
- `notes/rephase-1-r1-assembly/20260929T143833Z-assembly/commands/add.txt` (new)
- `notes/rephase-1-r1-assembly/20260929T143833Z-assembly/commands/commit.txt` (new)
- `notes/rephase-1-r1-assembly/20260929T143833Z-assembly/commands/branch.txt` (new)

No other reconstruct paths touched. No reconstruct commit/push. STOP milestone 1 after packaging; root then selects tests/review.
