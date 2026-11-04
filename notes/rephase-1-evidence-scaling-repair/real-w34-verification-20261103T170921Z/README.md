# Real W34 409 verification — MATERIAL FAILURE return to Root (no PASS)

Packet: `notes/rephase-1-evidence-scaling-repair/real-w34-verification-20261103T170921Z/`
Runtime: `.rephase-1-editorial-runtime/evidence-scaling-w34-verification-20261103T170921Z/candidate-work`
Status: **ACTUAL normal run attempted once via strict facade; FAILED before first copy with durable raw. No 409 completion. Returned to Root, no weakening/restart, no code change.**

## 1. Authority / scope

- Root authorized actual W34 409 continuation NOW on corrected runtime SOURCE-review-ready + fresh F5+full16+DM022 green.
- Read FULL: `astra-implementation-resolution.md` §§4/6/7, `astra-source-review.md`, `independent-implementation-review.md` latest F5 (§§ READY_FOR_REAL409 + F5 qualification), `implementation-return.md` §10, test-F5 packet `notes/rephase-1-evidence-scaling-test-F5-20261103T170019Z/README.md`.
- NO subagents. Human no Commit readback. No network/Production/current checkout/ordinary candidate/reconstruct commit/push/source old-workcopy edits. Meaningful source commit only NEW independent rehearsal/test DB authorized (done: `bd80d60`, see §3).

## 2. SOURCE pins + inventory (derived, no guesses)

Author workcopy `.rephase-1-editorial-runtime/evidence-scaling-implementation-20261103T114312Z/candidate-work` (HEAD `409b292…` ordinary, edits uncommitted):

- `scripts/survey_evidence_v2.py` 158943B `487425385052fa181b0a24954815c6fbb6882a0af1fc7256ef7352b309359c2a` OK
- `scripts/run_evidence_v2_interactive.py` 45501B `c9b7c70bd58055b105c6dce8b9e75072fa83e8396acd929d13b676185b4c225b` OK
- `scripts/survey_research_authority_v2.py` 218692B `0974c709b55365ef93cded5e97707e705b8a59aae01734e52c40e3b40c1a008b` OK
- `tests/test_evidence_scaling_v2.py` 79860B `1c95f6756f3b0fdd2d2bcebfc48a64fe25fc3e21150dc5796ba36c11d0a67e75` (current, may gain Views TEST-ONLY separately; runtime frozen)

Baseline final138 manifest `634d41f9807e8cd60ca3d839245358fa5e5da312f6d1b58ae84c1619481a03dc`/186847B, 770 intended, HEAD `409b292…`. Old pins in manifest for 3 runtime: `36b7b58…`/130152B, `5a6280ac…`/45084B, `546bbad1…`/212084B. Full inventory for NEW epoch = baseline 770 with 3 updated + new test = **771 intended** (verified `before_full_count=771/after=771`, `source_mutated_during_run=false`). No guessed counts/cache blind copy. Physical modes `0o664`, git `100644` throughout.

## 3. NEW isolated clone + script-only epoch (legitimate REAL change)

- Preserved source: `.rephase-1-editorial-runtime/rehearsal-20261101T025600Z/candidate-work`, HEAD `480823560c0c26ed2e5baa18e0e79a22b2839a27` (both CANDIDATES). `origin https://example.invalid/rephase-candidate-recovery.git` inert, no `objects/info/alternates`, no `GIT_*` env, 0 symlinks, owner `eariver`, hooks samples only. Parent verified, capacity 326G avail >> 249M needed.
- Byte-copy whole rehearsal via `cp -a` (no hardlinks) to NEW `evidence-scaling-w34-verification-20261103T170921Z/candidate-work`; removed only `scripts/__pycache__` (25 pyc, 1.8M) in NEW clone to avoid cache blind copy. Original `__pycache__` preserved. All 231 `.git` files: file-list match, 0 shared inodes, 0 content mismatches, all `nlink=1` (full compare, not sample).
- Old source expected pins verified in NEW before install (all 3 OLD_OK, test absent). Installed ONLY reviewed 3 runtime + new test via `cp` (bytes/modes verified NEW_OK above); no config/docs/schema/Profile/State/checkpoint edits. `git status` diff vs original = only 3M + 1A (+ `__pycache__` removal); 7 pre-existing `M sources/…` + 7 `??` real-DATA preserved identical.
- Staged ONLY 4 intended paths (`git add` 4 files, never `add -A`). Committed with process-scoped identity (`-c user.name=w34-verify-isolated -c user.email=w34-verify@example.invalid`, no `allow-empty`, no `git config` change; config still `eariver`):
  - `bd80d6030d91a82c9b922be2087010b8254de72c` parent `480823560c0c26ed2e5baa18e0e79a22b2839a27`, tree `460109878c1d32f38f8cb7f72f3feb04618e964e`
  - Blobs `6a1b6886…/1cf49059…/e6c56ba3…/2addfb07…` match working `hash-object`, modes `100644`.
  - Contract8 unchanged (pipeline `3adfbda2…`, quality `b5b955d5…`, research `666f8a06…`, publication `99adff93…` identical orig vs new). State `implementation.repository_commit_sha` still `48082356` (old init retained, no hand-repin/reinit/fresh start), lifecycle `CANDIDATES_NORMALIZED`. Old DCP/SCP-equivalent State/Profile/checkpoint bytes identical (see machine `before_state==after_state` for run; orig vs new SP match).
- CAND dirty-runtime note: CAND path checks supplied/current SHA but does NOT prove clean tree; external committed/loaded binding done here (blobs + `__file__` hashes below). New clone code commit is legitimate REAL runtime change (3 runtime cores), not artifact/test-only (test file separate).

## 4. W34 inputs (exact, verified in NEW clone)

- `production-state.json` 3386B `7e6a50c2b84cdc7e526f1560f02efd95184685770edb95ab35bb9a40c633ea58` OK, lifecycle `CANDIDATES_NORMALIZED`, impl `48082356`
- `production-profile.json` 2371B `2a8c3089cec29eb64e121cdf0429eed38670df704ebe955079751198557cfeb1` OK
- `discovery-v2.jsonl` 963155B `e176326f853ed42b69bad8a1998513d8dba8d3838af7cdea0ca9bc8261df46b0` (369 lines = R369)
- `screening/input/event-discovery-v2.jsonl` 1335444B `0a23be47dad8ddaf4f0a9c3261d97cc0006ac942bfd2321be2487289a34da31e` (E439 basis)
- `screening/v2/accepted/e193ad05…/screening-accepted.json` 543880B `b9d963d83b712ba3fb7e93358f051c4e902f31d0e262c44eea6f76dcdf155841` (dir `e193ad05…` distinct)
- `evidence/proposed-input/interactive-evidence.json` 1573186B `3ffc6e310e389bf03275b7ac7df0b029e43acec5f6140cc3a5bd56f8a4794f27` (409 records: 352 PARTIAL / 49 VERIFIED / 8 NEEDS_MORE — kept as structural DATA pending semantic review, no publisher-truth claim)
- `external/evidence-supplement/evidence-authority-supplement-r2-fresh-basis.json` 389414B `ce6f977a3e690e779c380b7b035d9247207e262b5c50a5b14b6b6b8f0fbc704e` (428 entries / 425 distinct Raw, canonical paths from P6, hash verified). No old61 r1 present/used.
- Canonical `sources/2026-W34/evidence/v2` absent before invoke (confirmed); `materiality-ledger-v2.json`/`profile-completeness-v2.json` absent (required, runner refuses overwrite). SP `production-state 4865998b…`/3454B + `production-profile aff05fd5…`/13748B untouched/read-only (orig vs new byte-equal).

## 5. Actual run (strict facade, fresh harness, exclusive raw)

Harness `run_w34_verify.py` (stored packet, not old runners): same-process `run_mod.run(repo_root, state_path, input_path, supp_path)` via existing strict facades, no bypass/monkeypatch/preloaded `current_stage_basis_override`/subset/source projection. Public API unchanged (3 changed files). `PYTHONDONTWRITEBYTECODE=1`, one run until material failure.

- Outer: cwd `/home/eariver/git/reconstruct-japanese-generative-ai-survey`, PID `3485376` (recorded, polled same PID, never relaunched while alive; no duplicate jobs), outer start `2026-11-03T17:11:40Z`, outer end `2026-11-03T17:12:50Z`.
- Inner (machine.json): PID 3485376, start `2026-11-03T17:11:40.419560+00:00`, end `2026-11-03T17:11:57.980296+00:00`, wall 17.5607s, mono 17.5607s, exit 2.
- Modules (same-process `__file__` + hash match committed source): Evidence `…/candidate-work/scripts/survey_evidence_v2.py` `48742538…`/158943B, runner `c9b7c70b…`/45501B, LOW `0974c709…`/218692B. Committed `HEAD bd80d60/parent 48082356` recorded in machine `committed`.
- Before/after pins: 4 runtime + 6 State/Profile/SP + 5 W34 inputs + full 771 inventory — all runtime/State/inputs identical before/after except expected run failure left no canonical writes; `source_mutated_during_run=false`. Source bytes no mutate during run confirmed.
- `/proc/self/io` (same-process, raw dumps in machine.json): before `rchar:1625377 wchar:0 syscr:185 read_bytes:24576`, after `rchar:4837797528 wchar:4447015 syscr:18247 syscw:828 read_bytes:24576` (delta rchar 4836172151 ≈4.8GB logical, read_bytes physical unchanged 24KB). `rusage` utime 0.0468→16.2708 (delta 16.22s), stime delta 1.03s. No transcribed metrics; raw preserved.
- Raw pointers: `raw/stdout.txt` (149B, `{"exit":2,…}`), `raw/stderr.txt` (2.3K traceback), `raw/machine.json` (21K full record), `raw/pid.txt`, `raw/outer_*.txt`, `raw/repo_root.txt`, `run_w34_verify.py`.

## 6. Material failure — traced predicate, returned to Root

```
ValueError: implementation commit differs from authoritative state; explicit rebase/reinitialization is required
  at survey_production_v2.verify_state_basis:984
  via survey_evidence_v2.validate_evidence_package_basis:1223
  via run_evidence_v2_interactive._revalidate_run_owner:710
  via survey_evidence_v2._finish_authority_phase:446
  via run_evidence_v2_interactive.run:712
```

Predicate (`survey_production_v2.py:959-984`): `if state["implementation"]["repository_commit_sha"] != implementation_sha: raise`. State holds `480823560c…` (preserved init identity); `implementation_sha = core.repository_commit_sha(repo_root)` is new epoch `bd80d6030d…`. Strict equality required; script-only epoch does NOT retain LIVE-State equality despite Contract8 having no script members. This contradicts Explore's read-only trace that normal agent-first path permits committed script-only continuation with retained init identity. Per instruction, **do NOT weaken validator or silently restart/reinit/hand-repin**; no code changes on failure. Returned exact source/raw to Root/Astra for disposition (rebase/reinit decision needs guarded owned-output authority, not automatic).

Post-failure verification:

- Zero canonical outputs: `sources/2026-W34/evidence/` still only `proposed-input/`; ledger/completeness still absent; State still `CANDIDATES_NORMALIZED` (no `EVIDENCE_REVIEWED` advance, no semantic review/Gate). Accepted/public readback not applicable (no new outputs).
- Structural counts (409 cards/409 views/439 ledger/3 oblig, 352/49/8) remain input-side only; no validator-defect fix attempted.
- R≠E preserved (no run completed to check, no hand-append). Task IDs/bindings 428/425 remain supplement-side only.
- SP State+products unchanged (byte-equal). Old rehearsal unchanged end-compare (all 5 spot pins UNCHANGED_OK, HEAD `48082356`, status 15 lines). NEW runtime still new pins (no mutate).
- Failures unique/raw/no overwrite/lost stdio; no invented PASS. Raw preserved in ignored NEW clone (no canonical outputs to retain) + packet raw (not TempDB auto-clean-only proof).
- Current source epoch `bd80d60` distinct from ordinary shipping author HEAD `409b292…`; new tree `46010987…`.

## 7. Metrics scope (bounded, no overclaim)

- New measured: rchar delta ≈4.84GB, wall 17.56s, utime 16.22s to early `_finish` failure (before first copy). Old transcribed failed bounds: rchar `228011353736` (~228GB) ~14min to 143-task termination (operator-transcribed at 14:38, no raw `/proc` dump). Compare ONLY these logical-read/time numbers; **no disk/deadlock/all-cost claim, no old-full-runtime extrapolation, no physical-disk proof**.
- No all-profile/adoption/savings/whole PASS. No semantic publisher truth (49 VERIFIED kept structural). Goal actual 409 completion NOT met — this packet is failure evidence for Astra disposition, not delivery.

## 8. Pointers for independent review

- Harness: `run_w34_verify.py`
- Machine: `raw/machine.json` (argv/env/cwd/PID/exit/start-end UTC, modules/committed, before/after pins, rusage, io_before/after, result/error/traceback)
- Raw: `raw/stdout.txt`, `raw/stderr.txt`, `raw/pid.txt`, `raw/outer_start_utc.txt`, `raw/outer_end_utc.txt`, `raw/outer_exit.txt`, `raw/outer_cwd.txt`, `raw/outer_env.txt`, `raw/repo_root.txt`
- Manifest: `artifact-manifest.json` (full hash/modes + metrics)
- Runtime: `.rephase-1-editorial-runtime/evidence-scaling-w34-verification-20261103T170921Z/candidate-work` (HEAD `bd80d60`, parent `48082356`)
- Source epoch distinct from `409b292…`; old rehearsal `48082356` preserved.

**Human Commit Point — stop; do not auto-start repair. Awaiting Astra disposition on implementation-SHA vs State-identity continuation.**
