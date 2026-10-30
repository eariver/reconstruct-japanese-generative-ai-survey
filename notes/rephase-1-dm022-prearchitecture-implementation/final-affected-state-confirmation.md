# Final affected-state confirmation — B2 guard + Human history on FINAL delivery 768 (no source edits)

Date: 2026-10-29 UTC. All authors idle. No source editing, no Human readback, no ordinary commits, no Gitconfig/network/cleanup, no old-runner reuse. Test subprocesses use fresh meaningful independent Git DBs with process identity only. Current code reports are NOT authority — ONLY frozen-exec actuals below count. Do NOT claim overall acceptance; do NOT sum into one CI.

## 1. Fixed delivery source (ONLY tested source)

- Patch: `notes/rephase-1-dm022-prearchitecture-implementation/source-packaging/final-20261029T152913Z/complete-dm022-prearchitecture-409.patch`
  SHA256 `25b488784d02a156db693459dce6c1d369e7144f1f3c49461c9b3a846b1b7260` / 4931836B / 133 files (54M+79A, DIRECT actual409, inherited93 included).
- Manifest: `.../complete-dm022-manifest.json`
  SHA256 `31fa4a728cabc145232ef930b91c9c5e6f773692299a25a9177c994393d469fa` / 185422B / 768 entries `{SHA256,bytes,git_mode,physical_mode,kind}` + delta `diff_M 54 / new_A 79`.
- Intended: 768 = 689 tracked-at-HEAD + 79 untracked new (801 on-disk excl `.git` minus 33 `*.pyc` excluded by policy, preserved, no cleanup).
- Pins (read-only, verified in exec): HIGH `f8af03cc5d58af1057ea26d9cef0eb87b1fd71118ddf63a2186e24da9bc1e751`/88603, LOW `2aef837f`/155892; agent `d801feb679c99d2ed0839e41e6dbf91d5b1adcbeeb2a042af24f62d9c37`/199521, human `101792ad8070607e8237c2e1e5ccfa1ab9f5ff1e731a4a914df91bb3ccaf3b9`/74902, orch `491888fe...`/61147, bridge `2fd8a6a2...`; C2 release `b9433b9e`/14505, publication `705bcee3`/155658, refresh `dd01fa01`/96623, editorial `3a872156`/275939; history `a9de2c97`/315610, source `b139f493`/144597.
- Proof-candidate (independent apply): `/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate` (768 worktree + 83-file `.git`, HEAD `409b292...`/tree `8ce36998...`, no alternates, inert `example.invalid`, 768/768 0 mismatch vs manifest, 0 overlap, `apply --check 0` + `apply 0/1175B` with 6 whitespace lines preserved).

## 2. NEW frozen execution copy (parent ignored, independent DB)

- Exec: `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/exec-finalaff-20261029T164402Z/` (NEW unique stamp)
  - Source: byte-copy from proof-candidate (`tar --exclude=.git --hard-dereference` + `cp -a .git` no `--link`).
  - Worktree 768 files, git 83 files, HEAD `409b292...`, no alternates/commondir, origin inert `example.invalid`.
  - Vs manifest: 768/768 SHA/bytes/physical_mode 0 mismatches. Vs proof-candidate git: 83/83 0 `(dev,ino)` overlap. No hardlinks. No Git DB in packet.
  - No source changes/candidate imports (never imported `candidate-work`; `PYTHONDONTWRITEBYTECODE=1`, `unset GIT_*`, process-scoped `GIT_AUTHOR/COMMITTER=dm022-finalaff-fixture/finalaff@example.invalid`, inert origin, no network, no commits, no cleanup).
  - Pre/post per run: 768 files, 0 `__pycache__`/`*.pyc` in exec (caches qualified as 0, no cleanup of candidate 33 pyc which remain on disk per policy).
  - Python `/usr/bin/python3` 3.14.4, `jsonschema 4.23.0`, `pypdf 6.16.2`; unittest only.

## 3. Actual fresh results (exact module names, collection actuals)

Base: `notes/rephase-1-dm022-prearchitecture-implementation/evidence/finalaff-20261029T164402Z/` — per-run `header.txt` (command/PID/exit/source pre/post/modes/hash count/caches) + `stdout-stderr-raw.txt` + `exit-code.txt`, unique dirs, no logs reuse.

| Run | Exact module | Ran | OK | FAIL | ERR | Skip | Exit | Raw SHA |
|-----|--------------|-----|----|------|-----|------|------|---------|
| 01 | `tests.test_survey_dm003_w1_preview_agreement_v2` (DM003 W1 full6, latest guard) | 6 | 6 | 0 | 0 | 0 | 0 | `aac02dcc...` (11 lines, 13.6s) |
| 02 | `tests.test_survey_dm004_release_validate_state_v2` (DM004 CLI 7, latest guard) | 7 | 7 | 0 | 0 | 0 | 0 | `e1219a56...` (12 lines, 43.0s) |
| 03 | `tests.test_survey_agent_control_v2` (agent 5) | 5 | 5 | 0 | 0 | 0 | 0 | `7dd2e59b...` (10 lines) |
| 04 | `tests.test_survey_active_evidence_views_v2` (views 2) | 2 | 2 | 0 | 0 | 0 | 0 | `77eb8059...` (7 lines, stable bytes) |
| 05 | `tests.test_dm022_b_late_prepublish_v2` (B2 public guard 15, d801/1017/f8af) | 15 | 15 | 0 | 0 | 0 | 0 | `7255ce63...` (30 lines, 162.5s) |
| 06 | `tests.test_dm022_prearch_b_ordinary_consumers_v2` (ordinary 23, B2 prepub direct) | 23 | 23 | 0 | 0 | 0 | 0 | `1aaf2ba9...` (57 lines, 73.5s) |
| 07 | `tests.test_dm022_prearchitecture_acceptance_v2` (A25, HIGH f8af) | 25 | 25 | 0 | 0 | 0 | 0 | `2a4e3321...` (49 lines, 26.3s) |
| 08 | DM001 + weekly representative (1pos+1neg each, NOT full 36+34): `DM001019CanonicalFreezeTests.test_l1_weekly_positive_freeze_validates` + `DM001019WrapperFreezeTests.test_w4_wrapper_negatives_leave_no_outputs` + `WeeklyMechanicalRefreshV2Tests.test_first_and_repeat_success` + `...test_accepted_and_authored_mutation_refused` | 4 | 4 | 0 | 0 | 0 | 0 | `268d7a59...` (49 lines, 56.3s) |

- Fresh total: 87 ran, 87 pass, 0 fail/error/skip.
- Most important DM003 6 + DM004 7 evidence ledger pending on latest guard (d801/1017/f8af): CLOSED fresh on final delivery (no missing-fixture ERROR; fixture helpers STATE+full53+7 patched per task; if missing fixtures had ERRORed, would have reported ROOT first blocker with no code patch — none occurred).
- B2 15 + ordinary 23: fresh on final delivery with pins d801/1017/f8af/b943/705 (match delivery §A5.1, NOT old review b650/3d1). Existing B2 private raws (`bf4ac40b...` 15 late, `233bec90...` 23 ordinary on same d801/1017) are qualified as prior binding only (same B2 source, but older exec); this composite does NOT sum them — fresh 15+23 above are the confirmation on final 768. Source-hash verified same HIGH f8af (`f8af03cc...`/88603 in exec == A5 run `d77d5776...` HIGH), so no separate HIGH-only repeat beyond A25 already run fresh here.
- A25: fresh 25/25 on final HIGH f8af (not relying on A5 private `d77d5776...` which had same f8af but older 765-file base). Justified as required (B2 prepub direct + HIGH history-window affect normal Advance wrappers; A prepare/validState must be re-proved on final 768).
- DM001 36 + weekly 34: full NOT reburned (older B60 fixes + new B2 prepub direct). Representative 1pos+1neg each chosen as appropriate non-decorative scope (positive proves Advance wrapper still builds on final guard; negative proves no-write refusal). Full 36+34 remain available if root requires, no claim made from representatives beyond their seams.

## 4. Unchanged prior results (qualified, NOT summed)

- Prior B2 15 late (`bf4ac40b...`) + 23 ordinary (`233bec90...`) on B2 private (d801/1017, HIGH likely f8af): preserved as history, NOT transferred as final proof (different exec base 765 vs final 768; runtime B2 files byte-identical per SHA, but C2/H/S/delivery delta +4 files since review freeze means fresh confirmation above is required — done).
- Prior A5 25/25 (`d77d5776...` on 765f, HIGH f8af): preserved, NOT summed (different file count 765 vs 768; A files byte-identical `2aef837f/f8af03cc`, but final delivery adds 3 files since A5 — fresh A25 above on 768 is the confirmation).
- Prior DM003/DM004/weekly/DM001 failures in C1-finalaff (missing `production-state.json` on older exec): superseded by STATE+full53+7 fixture patch + final guard; NOT cited as current blockers (fresh 6+7+4 pass above).
- No aggregate full-matrix PASS claimed; no overall acceptance claimed.

## 5. Source binding + proof limits

- Exec 768/768 vs manifest `31fa...`, patch `25b488...` DIRECT actual409 (133 files 54M79A, inherited93 included, no old overlay). GEN `gen-diff-check` 6 whitespace + proof `apply 1175B` warnings preserved, not suppressed. Partial DB 26309 / bulk31466 / runtime+TeX unbundled qualified unchanged. `Git100644 vs 0o664` (single `100755` bridge) noted. No `BaseModule`. No packet Git DB.
- Identity: exec HEAD `409b292...`, inert origin, 0 inode overlap proof-vs-GEN-vs-CAND, no Human HEAD/status, no reconstruct objects. Fixture DBs independent temp dirs, process identity, inert origin, meaningful commits where git init required; no fixture objects in reconstruct; no ordinary commits.
- If missing fixtures had occurred: would have returned ERROR (fail-closed) with exact `FileNotFoundError`/requires-bound-fixture + PID, no runtime waiver, no code patch — none occurred in this scope (all 87 collected, 0 skipped).
- Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN preserved except progress; Profile/quality/adoption/savings OPEN. Later lifecycle + independent implementation review remain separate. Stop at Human Commit Point.
