# Independent packaging report — Profile/support COMPLETE DIRECT409 delivery (packaging only)

Date: 2026-10-31 UTC. NEW packaging owner, not source author. Source QUIESCENT throughout; concurrent final verification worker reads/runs separate snapshot, does not modify source. No source/tests edits, no candidate Git/index/config edits, no ordinary commit, no reconstruct git status/HEAD/log/readback/network/restore-from-remote/Production/intake/cleanup/reset. Existing 55 Gitlinks/child dirt untouched.

## 1. Delivery artifacts (NEW unique packet, no overwrite)

`notes/rephase-1-profile-support-implementation/source-packaging/final-20261031T200637Z/`:

- `complete-profile-support-409.patch` — SHA256 `e0ca796f6091f0ab2c824e616dc43705d6234ba9b15c827a132010249985a938` / 5240998B. ONE complete DIRECT actual409-relative full-index binary patch (`git diff --cached --full-index --binary HEAD` with temp index): 138 files, 81801 insertions, 855 deletions. Covers ALL current deltas INCLUDING inherited 133 (verified: old133 − new-delta = 0; no incremental on old patch, no old overlay layering).
- `complete-profile-support-manifest.json` — SHA256 `5a34afe827d1a2fa15e4325a20fded8de54339dd624c4c3d5447bd8646d215fa` / 186595B. All 770 intended paths `{SHA256, bytes, git_mode, physical_mode, kind}` + delta inventory (`diff_M` 57, `new_A` 81) + pins.
- Raw GEN/proof logs: `cp-git-*`, `tar-*`, `gen-count-*`, `gen-pyc-*`, `gen-head-*`, `gen-revparse-*`, `gen-remote-*`, `gen-noalternates-*`, `inode-check-*`, `gen-verify770-*`, `gen-read-tree-*`, `gen-verify689-*`, `gen-lstree-*`, `gen-lsfiles-stage-*`, `gen-add-*`, `gen-status-*`, `gen-diff-names-*`, `gen-diff-namestatus-*`, `gen-diff-stat-*`, `gen-diff-numstat-*`, `gen-diff-check-*`, `gen-diff-*`, `manifest-gen-*`, `patch-sha256.txt`, `patch-bytes.txt`, `manifest-sha256.txt`, `manifest-bytes.txt`, plus proof `indep-*`, `workcopy-before/after-*`, `candidate-head-after-*`. No Git DB in packet (`find packet -name .git` empty). Old packets preserved untouched.

## 2. Freeze root + isolation (ignored runtime)

- GEN: `.rephase-1-editorial-runtime/profile-support-packaging-20261031T200637Z/gen-copy/candidate-partial-b40de60/` (worktree 770 intended files, no `.git` in worktree count; `.git` byte-copied `cp -a` no `--link`) + `gen-index` (TEMP `GIT_INDEX_FILE`, outside packet; candidate/root indexes never touched). GEN DB: 83 files at copy time (later 221 after staging 138 new blobs, expected), 0 inode overlap vs candidate at copy time, no alternates/commondir, inert `example.invalid` origin, HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`/tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`. GEN worktree == candidate intended bytes (770/770, 0 mismatch).
- PROOF: `.rephase-1-editorial-runtime/profile-support-packaging-20261031T200637Z/proof-copy/candidate-partial-b40de60/` (+ `.git` byte-copied `cp -a` separate, 83 files, 0 overlap vs CAND/GEN, inert origin, HEAD/tree same). No proof-copy restore from old runners; NEW helper `restore689-new.py` (ignored runtime, not packet) via `git show HEAD:<path>` per-file, no fake-root/no ordinary commit/network/lazy fetch/old runner. Worktree before = clean 689 base only (see §4); after = 770.
- No blind-copy author residue: GEN/PROOF/CAND worktrees 0 `*.pyc`/0 `__pycache__` (excluded by policy, preserved on disk? Actually 0 present, no cleanup needed). Candidate has 0 pyc (verified).
- No `GIT_*` env at checks; `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_TERMINAL_PROMPT=0`, `GIT_NO_LAZY_FETCH=1` for all Git read/mutation in GEN/PROOF only. No `git config` executed. No empty commit, no Gitconfig changes. No meaningful fixture commits needed packaging.

## 3. Measured actuals (derived, not assumed)

- Intended: **770** = **689** tracked-at-HEAD + **81** untracked new (801? No, 770 on-disk excl `.git`; 0 pyc excluded).
- Actual delta vs actual409: **57M + 81A = 138 files** (measured via `git diff --cached --name-status HEAD`: 81 A, 57 M, 0 D/R, exit 0; `gen-diff-names` 138 lines). Premise `54M/79A/133` superseded by current: +3 tracked modifications beyond final133 +2 new test files.
- New intent (81A): original 79A (14 further new schemas incl DM022 5, 12 further new scripts incl LOW/HIGH, 38 further new tests etc per final133 disposition, full bytes in manifest `new_A`) + 2 legitimate new tests inspected before inclusion (no unknown worktree residues blind-copied, no deletion unknown data, no pyc/cache/rawlogs/runtime fixture included):
  - `tests/test_profile_support_upstream_repair_v2.py` 115763B `926e2e0a0ee2f7104ed5c92d7bbdd50ef3610b2d7f6fd542c51a5bcb597632d6` (ordinary + DERIVED operation oracles, frozen pin §8.4/§8.5)
  - `tests/test_dm022_c_direct_operation_v2.py` 35636B `ac44154fa0ba7e4b3d83bbbdda8e242e03fd50b048b92a293820da805b56b97a` (DM022 C direct/DERIVED/binding/consumer oracles, frozen pin §10)
- Modified tracked (57M): 54 inherited M (workflows, config, 6 schemas, 35 scripts, sty, 7 tests per final133 `diff_M`) with current bytes (12 among them further modified in this unit, still M) + 3 newly modified beyond final133 (were unchanged in final133, now M):
  - `scripts/run_evidence_v2_agent_first.py` 3684B `f73f2ab91fc88a794d4f734d0952e80edff438259d3ad2315001df60b8d61910` (thin delegation, B)
  - `tests/test_run_evidence_v2_interactive.py` 7721B `9d668bae9aca7437dc05a21c17724f50407b8e2c338bbc5fdf123909f50eb0e3` (migrated caller)
  - `tests/test_survey_evidence_v2.py` 43662B `ed0155cdf97c1baa8381113e775f232c4641c2f52a3c1f815970f5dbf4c03adc` (shared-helper real-HEAD migration, ready hash for DM022)
- Other 12 modified among original 768 vs manifest (full list §3.1): screening 82277 `f0f28954…`, evidence 130152 `36b7b583…`, runner interactive 45084 `5a6280ac…`, research_authority 212084 `546bbad1…`, prearch_acceptance 92741 `388c8994…`, plus 7 fixture/test helpers (c1 4782 `059fdf24…`, g71 5918 `43d4d414…`, lifecycle 4717 `f8c8f822…`, prearch fixtures 3873 `769f1820…`, full_lifecycle 280038 `b736baa7…`, b-consumers 47594 `cad603cc…`, A2 acceptance 87215 `bdf10930…`). All within exclusive ownership (A/B/C/D/ordinary), no unowned edits.
- Unchanged inherited vs actual409: 632 tracked files byte-identical to HEAD and manifest final; all 133 original delta paths present in new 138 (old133 − new138 = 0; extra-in-new = 5 listed above). Inherited 93 from renewal included via final133 (old93 − new-delta = 0 per final133 review; not re-layered).
- Base-689 availability: `git ls-tree HEAD -- <689>` 689 lines, `cat-file --batch-check` 689 lines missing 0 (`BASE689-AVAILABLE`, exit 0). Bulk outside intended scope (missing-26309-reachable / bulk31466 / runtime+TeX) NOT bundled — qualified below, not claimed.
- Modified tracked all within intended set (57/57). No `.tmp`/`*~` files. All intended paths under known top dirs with expected extensions. Excluded `pyc/__pycache__` 0/0.
- Git modes: 769× `100644`→`0o664` + 1× `100755`→`0o775` (bridge), 0 exec mismatch, 0 physical mismatch across CAND/GEN/PROOF.

### 3.1 Full modified list vs original manifest (15 among 768)

`run_evidence_v2_agent_first`, `run_evidence_v2_interactive`, `survey_evidence_v2`, `survey_prearchitecture_acceptance_v2`, `survey_research_authority_v2`, `survey_screening_v2`, `dm022_c1_fixture_helpers_v2`, `dm022_g71_g76_fixture_v2`, `dm022_lifecycle_fixture_v2`, `dm022_prearchitecture_fixtures_v2`, `test_dm022_full_lifecycle_v2`, `test_dm022_prearch_b_ordinary_consumers_v2`, `test_dm022_prearchitecture_acceptance_v2`, `test_run_evidence_v2_interactive`, `test_survey_evidence_v2` (15). Extras 2 new tests above. Total worktree 770, missing 0, extra 2 (legitimate), pyc 0.

## 4. Pins verified (read-only, candidate-only allowed + fresh DBs)

- CAND HEAD `409b292756dd1277b9dfae87679934c0d2ce251c` (via `cat .git/HEAD`), shallow `774dd39a951c9ac3818e83dfffd4c7666efb0a20`, origin inert, no `GIT_*` env. After generation HEAD/shallow unchanged (stable).
- GEN HEAD/tree/origin/noalternates/inode-separation all exit 0 (except noalternates exit 2 = absent, expected). GEN worktree 770, pyc 0.
- Frozen source pins for final verification reviewer (workcopy delivery, also GEN/PROOF identical):
  - Screening 82277 `f0f289540302753b2e7cad5f4fded1df0387ca1403309aa032a733199c42d5a1`
  - Evidence 130152 `36b7b5832845ea8a984697f980b0148fdf454736`
  - Runner 45084 `5a6280ac19986a05e363a673dd57294ed6d4257355fdb888d9cdd9466fe5d812`
  - Agent-first 3684 `f73f2ab91fc88a794d4f734d0952e80edff438259d3ad2315001df60b8d61910`
  - LOW 212084 `546bbad1cfc84cd28e984b3652df08b52a07e5015dcf2836717fb64238212737`
  - HIGH 92741 `388c89941cef393868c9a2cef5ad7276889ffa01aeda294e756c0d76b6f9efd4`
  - Shared helper 43662 `ed0155cdf97c1baa8381113e775f232c4641c2f52a3c1f815970f5dbf4c03adc`
  - Ordinary tests 115763 `926e2e0a0ee2f7104ed5c92d7bbdd50ef3610b2d7f6fd542c51a5bcb597632d6`
  - C-direct tests 35636 `ac44154fa0ba7e4b3d83bbbdda8e242e03fd50b048b92a293820da805b56b97a`
  - A2 87215 `bdf109300aed18dec4d517dcf8d527f80cef0e15cde7649d035eb02eac7c629a`, etc. Full 770 in manifest.

## 5. GEN zero/non-zero results (numeric exits)

`cp-git` 0, `tar` 0/0, `gen-count` 0 (770), `gen-pyc` 0 (0), `gen-head` 0, `gen-revparse` 0, `gen-remote` 0, `gen-read-tree` 0, `gen-verify689` 0 (`BASE689-AVAILABLE`), `gen-lstree` 0 (32155 HEAD entries; staged 32236 = 32155+81), `gen-lsfiles-stage` 0, `gen-add` 0, `gen-status` 0 (31604 lines incl bulk D, correctly EXCLUDED from `--cached` patch), `gen-diff-names` 0 (138), `gen-diff-namestatus` 0 (81A/57M), `gen-diff-stat` 0 (138 files, 81801+/855-), `gen-diff-numstat` 0 (138), `gen-diff` 0 (5240998B patch).

`gen-diff-check` exit **2 with 5 whitespace lines PRESERVED** (not suppressed): trailing + 4 blank-EOF + summary (392B stdout, 0B stderr). See `gen-diff-check-stdout.txt`. This is known staged-diff whitespace, NOT check/apply failure (check 0 + apply 0 prove success despite warnings).

## 6. Independent proof (NEW separate DB, clean 409 base, no old overlay)

- Proof root: `.rephase-1-editorial-runtime/profile-support-packaging-20261031T200637Z/proof-copy/candidate-partial-b40de60` (+ `.git` 83 files), outside packet, ignored runtime, NEW unique location.
- Source: candidate `.git` independent byte-copy `cp -a` no `--link` (`indep-cp-git-exit 0`). HEAD `409b292…`, tree `8ce36998…`, inert origin, no alternates (exit 2 expected).
- Baseline: AVAILABLE BASE 689 actual Git blobs to NEW worktree tracked689 only via read-only `git show HEAD:<path>` per-file (NEW helper, no fake-root/no ordinary commit/network/lazy fetch/old runner; `restore689-new.py` outside packet). Absent 26309/bulk31466 qualification retained.
- Do NOT apply on top old93/old133: worktree before = clean 689 base only (verified: `git diff --name-only -- <689>` exit 0 0B; new81 absent 81/81 `ALL-ABSENT-OK`; 689 modes/SHA: unchanged 632 equal manifest final, mod-same-as-final 57 = exactly `diff_M`, mode mismatch 0/689 `BEFORE-689-OK`). No Git DBs/new gitlinks in packet.
- Numeric apply/check RAW + whitespace — preserved, not normalized:
  - First `git apply --check` with `--git-dir/--work-tree` from wrong cwd: exit **1**, 0B stdout, 6592B stderr (59 `No such file` errors) — tool/cwd deviation, preserved as `indep-apply-check-stdout/stderr/exit.txt` (initial failure log, not overwritten).
  - Corrected `git apply --check` with `workdir=PROOF`: exit **0**, 0B/0B (`indep-apply-check-stdout2/stderr2/exit2.txt`) — no `--whitespace=fix`, no `--reject`, no partial.
  - Actual `git apply` ONCE with `workdir=PROOF`: exit **0**, stdout 0B, stderr **1115B** with 5 whitespace warnings (preserved, not suppressed; see `indep-apply-stderr.txt`). No `no warnings` claimed.
- Full 770 + 138 equality — all files, three trees, exact (not sample-only) via `hashlib.sha256` (no project import):
  - Proof worktree 770, manifest 770, missing 0, unexpected 0; content mismatch 0/770 vs manifest; physical 0/770 (`0o664`/`0o775` exact); gitmode exec mismatch 0.
  - GEN worktree 770, set diff 0/0, content mismatch 0/770 vs proof.
  - CAND 770, missing 0, unexpected 0; content mismatch 0/770 vs proof. Zero unexpected source paths; all intended paths under known top dirs.
  - Delta: `M 57 A 81 total 138`; `M-in-HEAD` verified via base689 (57 differ, 632 unchanged); `A-in-HEAD` verified via new81 absent before + present after (81/81).
  - After apply worktree 770 (689+81), no pyc created in proof (no test run).
- Lineage: old133 (`complete-dm022-manifest.json`, 54M/79A/768) `missing-in-new 0`, `INHERITED133-INCLUDED`; extra-in-new 5 (listed §3). Final patch is DIRECT against `409` (single direct apply on clean 689 PROOF, `check0/apply0`, no `--unsafe-paths`, no layered patches) — therefore direct-includes-inherited133 holds. First92 obsolete + inherited57 + delivery-correction chain preserved in prior packets (not re-verified beyond 133 inclusion here).
- DB origin/inode separation — metadata only, no Human HEAD:
  - `cand 853 (770+83)`, `gen 991 (770+221 after staging 138 new blobs, expected)`, `proof 853 (770+83)`, all distinct inodes.
  - `OVERLAP cand vs GEN 0`, `vs PROOF 0`, `GEN vs PROOF 0` (`INODE-SEPARATION-OK`). No hardlinks (nlink 1/1), no symlinks (0), no alternates/commondir, inert origin. GEN growth 83→221 is from `git add` creating 138 new blob objects (expected staging, not sharing; still distinct inodes). No `git config` executed. Packet has no `.git`.
  - No HumanHEAD/status/log/readback: no git commands in workspace reconstruct root; reconstruct objects not inspected (scoped CAND/GEN/PROOF only per task). GEN/CAND/SRC HEADs read only inside their own `.git` (all `409b292…`), never workspace HEAD.

## 7. Exclusions and non-claims (retained)

PartialDB `26309` missing reachable / `bulk31466` outside / runtime+TeX unbundled retained; scoped `689+81` only, not full hydrated/tree-clean (staged `32236` vs materialized `770` proves scoping). `Git100644 vs physical 0o664` separate (single `100755`→`0o775` noted). No tests/build/import/runtime, no adoption/semantic/production quality, no migration/audit, no certified rerunner/globalCAS/crash-atomicity, no suite-count decoration. No packet driver scripts shipped; `/tmp/.../*.py` one-shot NEW helpers live outside packet (`restore689-new.py` in WORKROOT, `intended770b.txt` in `/tmp`) and are NOT shipping source. No reapply performed beyond single required apply. No ordinary candidate/reconstruct commit/new HEAD. No unread historical objects required.

## 8. Failures / warnings / deviations (honest, no old PASS transfer)

- `gen-diff-check` exit 2 (5 whitespace lines, 392B) — preserved diagnostics, not suppressed with `--ignore` (see `gen-diff-check-stdout.txt`).
- Proof `apply` stderr 1115B (5 whitespace warnings + summary) — preserved, not normalized.
- First proof `apply --check` exit 1 (59 `No such file` errors) due to invoking `git --git-dir/--work-tree apply --check` from wrong cwd (tool deviation: `git apply` ignores `--work-tree` and uses cwd). Preserved as initial failure log; corrected with `workdir=PROOF` exit 0. No transcript reconstruction, no overwritten files.
- `apply_patch` CLI absent in this environment (consistent with A/B/C/D reports); all packet file creations via `Write` for new exclusive files + `bash` for command-generated artifacts (shell-output allowed). Specialized edit not needed (no source edits). Disclosed here, not recast as `apply_patch` execution.
- Old packaging scripts read as historical DATA only (`source-disposition.md`, `independent-final-packaging-review.md`, `gen-*`/`indep-*` logs); saved runners in `/tmp/opencode/jgas-dm022-indep-*.py` never executed.
- No old run PASS transferred; no behavioral tests/build run in this packaging unit; independent final review separate. Source stable during generation (`workcopy-before/after` 770/770 0 mismatch `SOURCE-STABLE`; HEAD/tree/shallow unchanged).
- Available proof for final verification reviewer: `proof-copy/candidate-partial-b40de60` (770 files, HEAD `409b292…`, applied patch, exit 0/0/1115B). Executable/full-source binding IDs: frozen pins §4 + manifest `complete-profile-support-manifest.json` (all 770 SHA/bytes/modes) + patch `complete-profile-support-409.patch` (138 files). GEN location above; PACKET location `notes/rephase-1-profile-support-implementation/source-packaging/final-20261031T200637Z/`.

## 9. Scope statement

Checked: actual intended inventory (770 = 768+2 legit new, 0 missing/extra beyond 2, 0 pyc, 15 modified among 768 detailed, modes compared, provenance inspected); saved patch/manifest FULL hash+bytes; before HEAD/tree/689/new81/clean; numeric `check0/apply0 + 0/1115B` RAW + `5` whitespace preserved; all 138 delta + all 770 intended files byte-exact across CAND/GEN/PROOF (not sample-only); inherited133 inclusion; DB/inode/alternates/origin/index/packet guards metadata-only.

Not checked / not claimed: runtime behavior, test execution, semantic approval, production quality, full-history/tree-clean certification, migration/adoption, audit, whole readiness. No code/adoption PASS. Source baseline fixed774, partialDB missing26309/bulk31466 preserved. No fake root, no empty commit, no Gitconfig changes. Stop at packaging; independent final review separate. WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN; quality/adoption/savings OPEN.

ProofDB: `.rephase-1-editorial-runtime/profile-support-packaging-20261031T200637Z/proof-copy/candidate-partial-b40de60` (83-file `.git` + 770 worktree). RAW: `indep-*.txt` + `gen-*.txt` + `workcopy-*.txt` + hash/bytes files in same packet. Patch `e0ca796f…985a938/5240998B`, manifest `5a34afe8…d215fa/186595B`.

(End — independent packaging owner, not source author, fail-closed: any mismatch would have reported precise file, no repair, no PASS.)
