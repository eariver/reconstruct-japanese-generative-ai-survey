# Freeze-transitive correction closeout — PUB shared-wrapper + M1-M6 (owned only, no whole PASS)

HumanHEAD f84fcf5321be3798c862c0156278afbba01f89f6 (clean except untracked resume packets, verified).
Contract 478f0051 incl §11 unchanged, ROOT 7d7d5a45 §6 binding. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN.
No CommitPoint. Ordinary candidate/reconstruct Commit/Push Human-owned. Production semantic NO-GO, synthetic reviews never genuine.

## Source pins (actual, no invention)

- Reconstruct HEAD f84fcf5, status untracked-only freeze-transitive-correction packet (preserved).
- Writable candidate `.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work` HEAD 409b292 (actual409/tree8ce), M=39+? (PUB owned change + inherited57).
  - PUB `scripts/survey_publication_v2.py` `3f4039fd7699baa212020dddfb02b3918bd63e02c475d638d99cbb2a1150d8d6` 125977B 2062 lines
    (was FIXED736 `90d90738dc2fc0c57a22f9656659a6e3665d262919b17f259811d035dac3d8c6` 92396B/1616 lines;
    intermediate grouping `be5c29f256ef463168e9229bff96fdf319260007eb2008b1a7b9116f988db2dd` 125817B preserved in G1).
    Change: shared-wrapper grouping by EXACT(path,sha) FIRST + union + expected from/to/checkpoints/required-set exactly;
    M1-M6 typed visitor (exact field names + implicit relativa, FD-safe, dedup, no generic walker).
  - New test `tests/test_versioned_renewal_freeze_transitive_correction_20261025.py`
    `7b6c68b87091a138cf83f1f3aec7d5a1890d93563b092118e2796d5dd99f6800` (6 behavioral tests, no string PASS).
  - NOT touched: P1/H/HIGH/Reader/source/schemas/stage/other tests (other authors).
- FIXED736 INPUT READONLY `.rephase-1-editorial-runtime/versioned-renewal-final-input-20261025T051343Z/snapshot-work`
  HEAD 409b292, 736 files, dst-hash `d7d7f6df0bbde842c0270d00f493b01e5be2d19fd48ccae56086f5cf4ca3a129` (736 lines).
- Fresh fixture `.rephase-1-editorial-runtime/versioned-renewal-freeze-transitive-20261025T120000Z/renewal-weekly`
  - Bootstrap old R3 `721a04d85532d7855f3e54cc411f5847c787726e` (721 files, E 127+2 ignored, real 5-page PDF).
    Clone --no-hardlinks, inert `example.invalid`, own gitdir, no alternates, nlink==1, dev:ino disjoint, no inherited GIT_*.
  - G1 `4a366bd` (parent 721a04d, 47 files SOURCE-only, E untracked preserved, overlap 0) fixed736 + PUB be5c29f (grouping+M1-M6 v1).
  - G2 `9cd1178` (parent 4a366bd, 1 file SOURCE-only) PUB 3f4039fd (draft M6 {name,path,sha256} extract fix) before new U authority.
  - Current HEAD 9cd1178, tree differs per genuine Core epoch (G1->G2 PUB change).
- Failed root V1 preserved (not deleted):
  - `operation-correction/` initial synthetic _preflight with real U3d _prepare_freeze_inputs hung in H/S (faulthandler Timeout in history:450) + 2 static string mismatches + copy baseline stderr 14k.
  - `run-u1-freeze-20261025T120000Z/` V1 harness-bug (finalize missing --basis/--checks, exit 2) + high-u1-weekly RECORD_COLLISION incomplete preserved.
  - `run-u1-freeze-20261025T121000Z/` V2 RECORD_COLLISION (fresh ID required) + `run-u1-freeze-20261025T122000Z/` V3 Freeze draft-bug (`ValueError draft-package ref fields invalid`) preserved.

## Actual test coverage (exit-proved raw, 1200s bound, PID logs, no helper fake PASS)

- FULL Freeze V4 (G2 PUB 3f4039fd, new RID high-u1c-weekly, REUSE_TARGETS, recorded_at monotonic wallclock):
  - u1-prepare 0 (6.96s), u1-qa 0 (0.32s), u1-finalize 0 (36.63s, REUSED_TARGETS; old U finalize 65s, new H batch faster — 36s here, lifecycle Freeze 74s ~ predicted 70s for S 62 reads+HIST 3-record+150 FD reads),
    u1-validate-set 0 (13.57s), u1-validate-receipt 0 (3.18s), u1-activate 0 (33.76s, ACTIVATED r3 `publication-surface-revalidation-r3.json`, observed new),
    u1-history 0 (1.55s, HISTORICAL_IDENTITY_VERIFIED 3 refs EDITORIAL+U1b? Actually U1c r3 chain, schema_pointer ""),
    u1-lifecycle-freeze 0 (74.56s, stage+synthetic Preview+Freeze+validate_manifest, State pinned True, no mutation).
  - Previously failed at `materiality-ledger not allowed` (weekly step5 + longform direct); now SUCCESS with union.
  - See `run-u1-freeze-20261025T123000Z/` (all *-exit.txt 0, *-stdout.txt/*-stderr.txt/*-dur.txt, commands.log DONE OK).
- Late-swap 7/7 at prep→install must refuse with zero new Freeze/Manifest, exact byte repair healthy control (real file swaps, not string tests):
  - card/task/raw/view/retentionCOPY/config/scope each: prep OK → swap AFTER prep BEFORE install → _preflight/_recheck refuses
    (`Freeze authority input changed` / `bytes changed`), frz_exists=False man_exists=False (lstat FileNotFound), restore exact bytes → healthy _preflight OK (no writes).
  - Each ~17-18s (Freeze prep H/S + snapshot), total 14 runs (7 refuse + 7 healthy) all exit 0.
  - See `late-swap-20261025T124000Z/` (late-swap-*/healthy-* *-exit.txt 0, *-stdout.txt PASS_REFUSE/HEALTHY_PREFLIGHT_OK).
- Unit partial controls (behavioral, FD-safe, not string PASS):
  - shared grouping (real JSON, union equals required, ledger in union), task/view/screening conventions (hash20, batch-001),
    preflight overlap (symlink alias refuses), FD ancestor refuse, no generic walker (exact field handlers present, no urljoin/requests).
  - 4 groups exit 0 in `unit-20261025T124500Z/` (unit-transitive/task-conv/preflight/nowalker *-exit.txt 0).
  - Note: `test_no_generic_walker_in_pub` includes structural `key in src` checks for exact field presence (not prose-location authority); main coverage is FULL Freeze + late-swap real files.

## Precise remaining (OPEN, not claimed)

- C route (new trio, real TL2026 disposable build + transfer + digest, EXECUTED_BUILD vs REUSED_BUILD) with new PUB 3f4039fd not yet verified (only U REUSE done).
- Repeat including C→U→U (only U1c single U done; need C1→U2→U3 with genuine second epoch, nonsquashed git log + HEAD^{tree} + tool-blob SHA).
- Renewal→editorial (P1 `RECEIPT_KIND_UNKNOWN: VERSIONED_RENEWAL_SOURCE_V1` dispatcher renewal branch, pre-G5/G6 gap; owned by P1 team, not this PUB patch).
- Normal direct Candidate/Preview/Freeze/Release to RELEASED (only synthetic Preview+Freeze+manifest done; merge verification + release record + R1×2 anchor + overwrite-guard oracles OPEN for separate worker).
- Explicit failure/resume (RENDER refusal, REFUSED_TARGET_EXISTS, RECORD_COLLISION/PRESERVED_INCOMPLETE no-rollback, ALREADY_ACTIVE/resume, IO/close/fsync/replace/postread/foreign-inode/32/33/cycle/anchor) + affected regressions (original routes/R1-slow/DM004 7/7 + publication/quality/gate/stage/pubset/revalidation/freeze/staged-EDQUOT, whole-pipeline 63/66/67→71 measured) + independent final implementation review (assessment §5).
- H/S timeout path (run54/59/61 Timeout 0:03:00 in history _git_run via source:1241 via reader:208/389, same class as V3 lifecycle 38s? Actually V4 lifecycle 74s succeeded, no timeout; but H batch perf + P1 routing + longform C→U→U + renewal→editorial timeouts remain H/S/P1 joint, not F1-F4/B1-B3 alone).
- New test file is partial unit controls only (6 tests), not full 97-method/25/13/43+2 suites; no certified rerunner/continuous isolation/globalCAS/crash-atomicity/genuine approval.
- No whole PASS, no CommitPoint, no adoption/migration/savings. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN. Production semantic NO-GO retained.

## Files (new unique, no overwrite of failures)

- `freeze-transitive-correction/README.md` (this file basis, pins updated after run)
- `setup-20261025T120000Z.sh` + `setup-.../` (G1 fixture, E-hash, overlay, staged 47, overlap 0)
- `g1-commit-20261025T120000Z.sh` + `g1-commit-.../` (G1 4a366bd, 47 files)
- `g2-commit-20261025T122000Z.sh` + `g2-commit-.../` (G2 9cd1178, 1 file PUB fix)
- `run-u1-freeze-20261025T120000Z.py` + `run-u1-freeze-.../` (V1 harness-bug preserved)
- `run-u1-freeze-20261025T121000Z.py` + `run-u1-freeze-.../` (V2 collision preserved)
- `run-u1-freeze-20261025T122000Z.py` + `run-u1-freeze-.../` (V3 U1b r2 + Freeze draft-bug preserved)
- `run-u1-freeze-20261025T123000Z.py` + `run-u1-freeze-.../` (V4 FULL Freeze SUCCESS)
- `late-swap-20261025T124000Z.py` + `late-swap-.../` (7 refuse + 7 healthy SUCCESS)
- `unit-20261025T124500Z.sh` + `unit-.../` (4 groups SUCCESS)
- Candidate patch: `scripts/survey_publication_v2.py` 3f4039fd + `tests/test_..._20261025.py` 7b6c68b (uncommitted in candidate-work, no reconstruct commit).

Return: PUB 3f4039fd7699baa212020dddfb02b3918bd63e02c475d638d99cbb2a1150d8d6 (2062 lines, 125977B),
tests 7b6c68b (6 tests), FULL Freeze V4 exit 0 (74.56s) + late-swap 14/14 exit 0 + unit 4/4 exit 0.
Remaining as above, no whole PASS/CommitPoint.
