# COMPLETE22 source packaging — bounded Worker (no independent review) — 2026-10-19

Role: bounded packaging Worker, NOT independent reviewer, NOT root/Astra.
Another Worker corrects witness evidence; SOURCE remains immutable.
No source code edits/tests/imports/network/production/candidate commit, no historical runners.

## 1. Source + task inputs read

- AGENTS.md isolation/packaging boundary (independent DB, inert origin, no alternates/hardlinks/object sharing, no fixture objects in reconstruct DB, ordinary commit/push Human-owned, stop at Commit Point).
- `notes/rephase-1-initial-build-integration/style-correction/README.md` + `style-coltitle-fix.patch` (one-line `+  coltitle=SurveyInk,`).
- `notes/rephase-1-initial-build-integration/style-correction/final22-manifest.json` (22-path list reference only; contains 73-char typo for staged-source-manifest, see §6).
- Root decisions: `astra-postbuild-disposition.md` §5 item 1 (SELECT FIX one-line style; items 2–4 deferred/retained), `astra-integration-review-return.md` §§1–6 (required stage negatives, transfer exclusivity, tautologies, evidence correction, deviations, QA scope — NOT executed here), `independent-final-integration-review.md` BOUNDED_PASS with mandatory §7 qualifications (NOT re-run here).
- Pinned21 reference: `notes/rephase-1-dm021-p3s/draft-history-r11/static21.json` SHA256 `1c0e339ceb31ddb8d565580f4e0d0b2140085cc414bb766b46872fdc8a2ef1a5` (3670 B), verified hash-before-trust.

## 2. Frozen candidate (read-only, unmodified)

- Location: `/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60`
- HEAD `409b292756dd1277b9dfae87679934c0d2ce251c` (detached, `symbolic-ref` rc=1), tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, shallow true, git-dir/common-dir `.git`.
- Status exact `4M18A22` (verified `status --porcelain=v1 --untracked-files=all` sorted equality):
  - M (4): `schemas/reader-surface-gate-v2.schema.json`, `schemas/reader-surface-semantic-review-v2.schema.json`, `scripts/survey_reader_surface_gate_v2.py`, `templates/survey/jgaisurvey.sty`
  - ?? (18): 5 schemas + 5 scripts + 1 longform-generated + 1 semantic-publication + 6 tests (exact list in `complete22-manifest.json`; matches final22-manifest keys).
  - `diff HEAD --name-only` = 4 tracked above; `diff --cached --name-only` empty.
- Pins verified 22/22 BEFORE trusting (script `src-before-pins-stdout.txt` exit 0):
  - 21 inherited match static21 SHA/bytes/mode (all `0o664`).
  - Style after: SHA256 `035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec`, 6569 B, `0o664`.
  - Style HEAD bytes: SHA256 `3b6d15627439b35a352d692c8c5f9c2ac25dd02968e75beb30a69b8c8f53e5cc`, 6547 B (matches manifest `before_*`; restored in proof clean step).
  - HEAD blobs for all 4 tracked available via `git show HEAD:path` (missing-historical-blob diagnostics would have fail-closed; none missing).
- Source before vs after identical (status sorted diff empty, pins re-verified; `src-after-ok.txt`). Original/source index never mutated (`src-mid-diff-cached` empty; temp index used for GEN only).

## 3. Method (new scripts saved BEFORE execution, sanitized env, durable raws)

Scripts (dedicated `Write`/`Edit`, no `apply_patch`, no shell rewrites):
- `package_complete22_20261019T141500Z.sh` (v1 faulty: `cp` double-leaf nesting; failure preserved in `attempt1-cp-nesting-fail/` 59 files).
- `package_complete22_20261019T141600Z.sh` (v2: cp fixed but GEN/PROOF leaf paths double-appended `.../candidate-partial-b40de60/candidate-partial-b40de60`; separation fail preserved in `attempt2-separation-path-fail/` 82 files).
- `package_complete22_20261019T141700Z.sh` (v3 SUCCESS, exit 0; `GEN_COPY/PROOF_COPY` are parents, leaf appended once at use sites; new PACKROOT).

Sanitization every invocation: inherited `GIT_*` unset, `GIT_NO_LAZY_FETCH=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0`, `git --no-optional-locks`, `PYTHONDONTWRITEBYTECODE=1`. No fetch, no system/global config, no network, no `__pycache__` in source/dest.

Packaging roots (new unique `/tmp/opencode`, no hardlinks):
- Failed: `/tmp/opencode/jgas-style22-packaging-20261019T141500Z/` (empty gen/proof dirs).
- Failed: `/tmp/opencode/jgas-style22-packaging-20261019T141600Z/` (gen/proof byte copies present but double-path logic failed separation).
- SUCCESS: `/tmp/opencode/jgas-style22-packaging-20261019T141700Z/` with `gen-copy/candidate-partial-b40de60`, `proof-copy/candidate-partial-b40de60`, absolute `gen-index` (outside notes packet).
- Independence: `cp -a` (no hardlinks); full `.git` `dev:ino` walk src(83) vs gen(83) vs proof(83) vs reconstruct(2567) collisions 0 cross-domain 0; worktree 22 hardlink-shared 0; `.git/objects/info/alternates` absent; remote `https://example.invalid/...` inert; config `--show-origin` only `.git/config` + `.git/config.worktree`; `gen-index` outside packet verified (`gen-index-outside-ok.txt`); no `index`/`.git` leaked into notes (`packet-list.txt`).

GEN (independent DB + absolute temp index outside packet):
- `rm -f GEN_INDEX` (absent check), `read-tree HEAD` into `GIT_INDEX_FILE=$PACKROOT/gen-index` (exit 0), `add -- <ONLY known22>` (exit 0), `diff --cached --name-only` verified exactly 22 sorted equality (`gen-names-ok.txt`), `diff --cached --binary HEAD > complete22-409-clean.patch` (exit 0, `gen-diff-exit.txt`).
- No original/source index mutation; no unrequested commit; missing historical blob would have fail-closed (none missing).

PROOF (independent disposable copy, single direct clean409 apply):
- Verified 22 pins in proof copy BEFORE mutation (exit 0).
- Restored ONLY tracked4 exact HEAD bytes via `git show HEAD:path` (4 separate raw stdout/stderr/exit + `cp` exits), removed ONLY known new18 after pin verification (18 separate `rm` exits).
- Verified clean409: HEAD still `409b292…`, `status` empty, `diff HEAD` empty, absent18 OK, HEAD bytes match `264fdd64…/6300`, `1594933f…/3160`, `818b1735…/86029`, `3b6d1562…/6547` (`proof-clean-headbytes-stdout.txt` exit 0).
- Applied SAVED full22: `apply --check --verbose` (stdout 0 B, stderr 1449 B listing 22 Checking lines, exit 0) then `apply --verbose` (stdout 0 B, stderr 3409 B, exit 0) — separate raw files, single direct clean409 invocation, NOT layered copies.
- Validated 22 SHA/bytes/modes + full status: `proof-after-status` sorted-equal to source before `4M18A22` (`proof-status-ok.txt`), pins 22/22 OK, HEAD unchanged (no commit), inherited21 unchanged.

Raw capture: every git/cp/rm/python invocation has unique `*-stdout.txt`/`*-stderr.txt`/`*-exit.txt` (numeric, `printf "%s"`), appended to `commands.log`; no overwritten failures (attempt1/attempt2 preserved in subdirs); no shell masked exits (`set -u` only, explicit `rc` checks).

No embedded Git DB/index/toolchain in notes: packet contains only `.sh`, `.patch`, `.json`, `.txt`, `.bin` (show outputs), `.log`; `find -maxdepth 2 -name .git` empty.

## 4. Outputs (this packet)

- Patch: `complete22-409-clean.patch` — 1,233,999 B, SHA256 `7c82ec47eb82dc56210b82063fe04c583d29cd36df5ce19f48297ebd4f000334`. `git apply --stat`: 22 files, 21117 insertions, 10 deletions. `git apply --numstat` matches 18 new files (0 deletions) + 4 modified (`reader-surface-gate` 16, `semantic-review` 32, `reader_surface_gate` 134/10, `jgaisurvey.sty` 1/0). Directly applicable to clean409 (proof `--check`+`apply` both 0).
- Manifest: `complete22-manifest.json` — patch SHA/bytes/path, candidate/HEAD/tree/status, static21 file SHA, style expected, 22 files SHA/bytes/mode/git_status (+ style before_*), proof copy/gen_copy/gen_index + check/apply exits. Corrects final22-manifest typo (see §6).
- Script: `package_complete22_20261019T141700Z.sh` (v3 success) + preserved faulty v1/v2 + `attempt1/`/`attempt2/` raws.
- Raw proof/source guards: `src-before-*`, `src-after-*`, `src-mid-*`, `separation-*`, `gen-*`, `proof-*`, `commands.log`, `script-stdout.txt` (1827 B) / `script-stderr.txt` (0 B) / `script-exit.txt` (`0`), `packet-list.txt`.
- No tests executed (per instruction; one-line style already real-built two-route in `final22-integration-20261019T135318Z`, NOT re-run here).

## 5. Exact pins / path / source identity

- Candidate: `/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60`, detached `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, `4M18A22`.
- Patch: `notes/rephase-1-initial-build-integration/source-packaging/complete22-409-clean.patch`, 1233999 B, `7c82ec47eb82dc56210b82063fe04c583d29cd36df5ce19f48297ebd4f000334`, 22 paths (list in §2 + manifest).
- Style: after `035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec`/6569, before `3b6d15627439b35a352d692c8c5f9c2ac25dd02968e75beb30a69b8c8f53e5cc`/6547, single `+  coltitle=SurveyInk,` (matches `style-coltitle-fix.patch`).
- Static21: `1c0e339ceb31ddb8d565580f4e0d0b2140085cc414bb766b46872fdc8a2ef1a5`, 21/21 verified.
- GEN: `/tmp/opencode/jgas-style22-packaging-20261019T141700Z/gen-copy/candidate-partial-b40de60` + absolute `/tmp/opencode/jgas-style22-packaging-20261019T141700Z/gen-index` (outside packet).
- PROOF: `/tmp/opencode/jgas-style22-packaging-20261019T141700Z/proof-copy/candidate-partial-b40de60` (cleaned to 409 then single applied), `--check` exit 0, `apply` exit 0.

## 6. Limitations / disclosures

- Typo correction: `style-correction/final22-manifest.json` lists `schemas/editorial-staged-source-manifest-v2.schema.json` SHA as 73-char `4fa6172338072258f1f3c204b27331ac79a35b2ac79a35b2af9d42ac6a2e8be7a34e32e46` (duplicated `2ac79a35b2`); actual file + static21 + this manifest use correct 64-char `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46` (5627 B). Script fail-closed against static21, not typo manifest; this packet corrects it.
- Partial DB: `rev-list --missing=print` census retained (present 2376 / missing 26309, 13 commits) — archive preserves available partial content, NOT full history; `HEAD:` blobs for tracked4 present, but missing-blob diagnostics would have stopped GEN (none triggered). Not a full-history/backup certification.
- Runtime unbundled: TeXLive/toolchain under `/tmp/opencode/jgas-texlive-...` NOT bundled here; Python 3.14.4 local runtime, no source imports, no builds/tests in this unit.
- Current check, NOT global certification: HEAD/tree/status/pins/inert/no-alternates/inode separation are current observations for GEN/PROOF isolation only; NOT continuous no-drift, NOT generic tool rerunner certification, NOT execution-fixture isolation (future fixtures need fresh isolated DB + separation at execution time).
- No new authority: HEAD still 409 (no candidate commit), no Gate/Candidate/State/Preview/Freeze/Release, no Human approval, no production adoption; independent review + root correction of witness evidence remain separate (another Worker).
- Failed attempts preserved: `attempt1-cp-nesting-fail/` (v1 `cp` double-leaf, 59 files) + `attempt2-separation-path-fail/` (v2 leaf double-append, 82 files); v1/v2 scripts preserved, NOT deleted/overwritten.
- No old-test rerun: `test_survey_*` NOT executed here; one-line style change already real-built two-route (`final22-integration-20261019T135318Z`) per root disposition; this unit is packaging only.

## 7. STOP — awaiting root/next Worker

COMPLETE22 patch + single direct clean409 proof complete. No commit/push. Next is witness-evidence correction (separate Worker) + root review; do NOT start next implementation unit. Ordinary Commit/Push Human-owned.
