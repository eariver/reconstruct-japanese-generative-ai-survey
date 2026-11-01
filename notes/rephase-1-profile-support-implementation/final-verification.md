# Final meaningful affected verification — quiescent source, genuine durable raw

2026-10-31. NEW General verification-execution owner (not independent semantic reviewer). Actual source implementation QUIESCENT and code/tests authored by others. No code/test modifications, no PASS invented. No ordinary commits. No reconstruct git status/HEAD/log, no Human readback, no network/installs/Production/intake/rebaseline.

Authority read in full: `notes/rephase-1-profile-support-implementation/astra-implementation-review.md`, `ordinary-verification.md` latest §8 (incl §8.1 raw-insufficiency qualification + §8.5 frozen pins), `independent-early-source-review.md` §9 (raw gap + DERIVED gap + census), `dm022-integration-verification.md` latest §§9–10 (exact test IDs + raw command names), `independent-final-implementation-review.md` (provisional SOURCE/ORACLE, §3.1 C-breadth + §5 prerequisites), actual source tests (real IDs below).

## 1. Quiescent source + inventory (770 intended, no caches)

Workcopy (read-only for this run, preserved): `.rephase-1-editorial-runtime/profile-support-implementation-20261031T153148Z/candidate-work`
Final133 manifest: `notes/rephase-1-dm022-prearchitecture-implementation/source-packaging/final-20261029T152913Z/complete-dm022-manifest.json` (intended 768, delta 54M/79A, head `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`).

Full comparison workcopy vs manifest (excl `.git`, excl `*.pyc`/`__pycache__`):
- work 770, manifest 768, missing 0, extra 2: `tests/test_profile_support_upstream_repair_v2.py`, `tests/test_dm022_c_direct_operation_v2.py`. No other extra/missing. `*.pyc` 0, `__pycache__` 0.

Frozen pins re-observed in NEW snapshot (full SHA256, not abbreviations):
- `scripts/survey_screening_v2.py` 82277B `f0f289540302753b2e7cad5f4fded1df0387ca1403309aa032a733199c42d5a1`
- `scripts/survey_evidence_v2.py` 130152B `36b7b5832845ea8a984c69a3097f9846976805c556679ed980b0148fdf454736`
- `scripts/run_evidence_v2_interactive.py` 45084B `5a6280ac19986a05e363a673dd57294ed6d4257355fdb888d9cdd9466fe5d812`
- `scripts/run_evidence_v2_agent_first.py` 3684B `f73f2ab91fc88a794d4f734d0952e80edff438259d3ad2315001df60b8d61910`
- `scripts/survey_research_authority_v2.py` 212084B `546bbad1cfc84cd28e984b3652df08b52a07e5015dcf2836717fb64238212737`
- `scripts/survey_prearchitecture_acceptance_v2.py` 92741B `388c89941cef393868c9a2cef5ad7276889ffa01aeda294e756c9f76b6f9efd4`
- `tests/test_profile_support_upstream_repair_v2.py` 115763B `926e2e0a0ee2f7104ed5c92d7bbdd50ef3610b2d7f6fd542c51a5bcb597632d6`
- `tests/test_survey_evidence_v2.py` 43662B `ed0155cdf97c1baa8381113e775f232c4641c2f52a3c1f815970f5dbf4c03adc`
- `tests/test_dm022_c_direct_operation_v2.py` 35636B `ac44154fa0ba7e4b3d83bbbdda8e242e03fd50b048b92a293820da805b56b97a`
- `tests/test_dm022_prearchitecture_acceptance_v2.py` 87215B `bdf109300aed18dec4d517dcf8d527f80cef0e15cde7649d035eb02eac7c629a`
- `tests/test_dm022_c1_family_closure_v2.py` `b564e723d827fa6b6b04aca963496bc1e60894dad515b449e1d3e53f79569c66`
- `tests/test_dm022_c1_h_presence_controls_v2.py` `a8ce879478a6532657bf6eeb96bc28219dd634e8f7b2ce8920aa2f6c9243bd2d`
- `tests/test_dm022_c1_research_graph_v2.py` `9ef62e519bf360052524cd6380109aee7d79c882d83188b30a87ebdf15c7d3d3`
- `tests/test_dm022_prearch_b_ordinary_consumers_v2.py` `cad603ccec78cbda88841ce56c62605260762241fbe079d0d60356ef3485a48e`
- `tests/test_dm022_full_lifecycle_v2.py` 280038B `b736baa7d38f33a8a41c01a61060ec01df8ffc19780cb47443e0a81a72b9c334`
- `tests/test_run_evidence_v2_interactive.py` 7721B `9d668bae9aca7437dc05a21c17724f50407b8e2c338bbc5fdf123909f50eb0e3`
- `tests/test_run_evidence_v2_agent_first.py` 4452B `e50a14b135af6e8bf35f4193a8310600f1b9943864a8e9238efbc2ee58fa462a`
- `tests/test_survey_evidence_source_class_regression.py` `ba015ea3cbbb5861a7f450f27b1787c13051191089ec8921bb3af8a2950ffcc3`

Workcopy still quiescent after runs (re-checked `f0f28954…`, `926e2e0a…`, `ac44154f…` unchanged). No workcopy edits. Another packaging worker reads quiescent source; no changes expected/observed from this owner.

## 2. NEW ignored runtime fixed snapshot + independent Git DB

- Snapshot: `.rephase-1-editorial-runtime/profile-support-final-verify-20261031T200617Z/snapshot-fixed` (770 files excl `.git`, 0 `*.pyc`, 0 `__pycache__`).
- Method: `mkdir -p` (parents verified), `tar --exclude=.git -cf - -C candidate-work . | tar -xf - -C snapshot-fixed` exit 0, `cp -a candidate-work/.git snapshot-fixed/.git` exit 0. No blind-copy author residue. Preserved original workcopy/old snapshots; no old saved runners, no cleanup/reset/raw overwrites.
- Git: `HEAD` `409b292756dd1277b9dfae87679934c0d2ce251c`, `shallow` `774dd39a951c9ac3818e83dfffd4c7666efb0a20`, origin `https://example.invalid/rephase-candidate-recovery.git` (inert), `objects/info/alternates` absent (no alternates file), no `GIT_*` env (`env | grep ^GIT` exit 1), distinct inodes/dev vs workcopy (spot-checked), nlink 1/1, single file. No ordinary commits. Fixture commits only in independent temp DBs with process-scoped identity (`git -c user.*` + `GIT_*` env, never `--allow-empty`, never `git config`, no root DB) per test bodies; no fixture objects in reconstruct DB.
- Packet logs: `notes/rephase-1-profile-support-implementation/final-verification-20261031T200617Z/logs/` (NEW unique, exclusive opens only).
- Evidence runner (packet, not shipping runtime): `.../final-verification-20261031T200617Z/run_final_verification.py` (fail-closed Popen wrapper), `loader_probe.py`, `run_loader_fixed.py`, `run_loader_fixed2.py` (all via specialized Write, never `echo`/heredoc; `apply_patch` binary absent, disclosed).

Runtime: `/usr/bin/python3` 3.14.4, `PYTHONDONTWRITEBYTECODE=1`, jsonschema 4.23.0, pypdf 6.16.2, no installs. TeX `pdflatex/xelatex/lualatex/latexmk` absent (`which` empty) — explicit probe, not default PATH assumption; no PDF builds required (no PDF-dependent finding; Selection/draft runners verify generation on current bytes without TeX per C §10). No network/Production/intake/rebaseline/Human readback/reconstruct git ops.

## 3. Selected batches (exact IDs, no count sums, sequential)

Wrapper executes sequentially (separate fixtures, no parallel; no `timeout`-shell wrapper so guards cannot self-match commandlines). Common-positive-setup STOP armed: wrapper stops further batches on first non-zero/timeout/pins-change. No failure occurred, so all 8 ran. Each batch is its own exact run; no cross-batch count sum. Old summary-only 21/24 +14/14 and 26/26 +26/26 stay unverified historical (per `ordinary-verification.md` §8.1); this run provides NEW verbose raw only.

All test `stdout.txt` are 0B by framework design (`unittest -v` writes to stderr); all `stderr.txt` hold REAL verbose outputs (`Ran … OK`). Not evidence loss. No hand summaries as stdout. Numeric exits saved even on timeout/wrapper failure (no timeouts occurred). Missing-raw: none for tests (each stderr has `Ran` + `OK`); loader v1 failures disclosed below, fixed by v2.

### 3.1 ordinary-newmodule-28 (full new ordinary module, incl 16c + 23/24)

Selector: `tests.test_profile_support_upstream_repair_v2 -v` (28 tests: 01,02,03,04,05,06,07,08,09,10,11,12,13,14,14b,15,16,16b,16c,17,18,19,20,20b,21,23,24,22 — classes DM016/DM017/Parity/History/Prepackage/Derived/Guard).
- Command: `/usr/bin/python3 -m unittest tests.test_profile_support_upstream_repair_v2 -v`, cwd snapshot-fixed, env `PYTHONDONTWRITEBYTECODE=1`.
- PID 2555496, start 2026-10-31T20:08:19.922234+00:00, end 2026-10-31T20:08:26.705034+00:00, duration 6.783s, timeout 600s, timed_out False, returncode 0, exit file `0`.
- Raw: `.../logs/ordinary-newmodule-28-stdout.txt` (0B, framework), `...-stderr.txt` (7617B, verbose per-test `... ok`, `Ran 28 tests in 6.068s`, `OK`), `...-command.txt`, `...-env.txt`, `...-pid.txt` (`2555496`), `...-exit.txt` (`0`), `...-meta.txt` (PID/argv/cwd/env/time/returncode), `...-pins-before.txt`/`...-pins-after.txt` (770 lines each, identical).
- Covers real public pair 16c (direct `runner.run` vs agent-first `adapter.main` CLI on cloned fixtures, exact outputs + closure-first + 7-field + Selection refs) and real DERIVED 23 (healthy many-to-many R!=E + Selection `derive_candidate_matrix`/`write_candidate_matrix`/`validate_selection==[]`) /24 (lossy `(R-2,O-SHARED)` refuses `DECLARATION_LOSS` before first write with full inventory).

### 3.2 ordinary-affected-26 (exact 26 from ordinary report)

Selectors: `tests.test_survey_evidence_v2` (12) + `tests.test_run_evidence_v2_interactive` (8) + `tests.test_run_evidence_v2_agent_first` (4) + `tests.test_survey_evidence_source_class_regression` (2).
- Command: `/usr/bin/python3 -m unittest tests.test_survey_evidence_v2 tests.test_run_evidence_v2_interactive tests.test_run_evidence_v2_agent_first tests.test_survey_evidence_source_class_regression -v`
- PID 2556382, 2026-10-31T20:08:27.076348+00:00 → 2026-10-31T20:08:29.697152+00:00, 2.621s, timeout 600s, rc 0.
- Raw: `ordinary-affected-26-stderr.txt` (5331B, `Ran 26 tests in 1.979s`, `OK`), stdout 0B (framework), plus command/env/pid/exit/meta/pins-before/after (770 each, identical).

### 3.3 dm022-c-6 (new C module)

Selector: `tests.test_dm022_c_direct_operation_v2 -v` (6: `test_c_direct_weekly_prepare_adopt_readback`, `test_c_thematic_direct_prepare_adopt_readback`, `test_c_derived_weekly_true_r_not_equal_e`, `test_c_negatives_profile_copy_retention_refuse_no_write`, `test_c_binding_negatives_beyond_file_sha`, `test_c_report_positive_control_extra_rows_pass`).
- PID 2556587, 2026-10-31T20:08:30.006552+00:00 → 2026-10-31T20:08:43.617361+00:00, 13.611s, rc 0.
- Raw: `dm022-c-6-stderr.txt` (1946B, `Ran 6 tests in 13.435s`, `OK`), plus per-batch raw set as above (pins 770 identical).

### 3.4 dm022-a2-25 (full A2)

Selector: `tests.test_dm022_prearchitecture_acceptance_v2 -v` (25 `Dm022A2OperationTests` methods incl Weekly/THEMATIC prepare/adopt/resume/readback, high CLI, guard/slots, tamper/resume, loader dispatch, repeat-preserves-anchor).
- PID 2557596, 2026-10-31T20:08:43.923279+00:00 → 2026-10-31T20:09:21.867836+00:00, 37.945s, rc 0.
- Raw: `dm022-a2-25-stderr.txt` (5357B, `Ran 25 tests in 37.511s`, `OK`).

### 3.5 dm022-affected-37 (c1-family/presence/research/b-ordinary)

Selectors: `tests.test_dm022_c1_family_closure_v2` (6) + `tests.test_dm022_c1_h_presence_controls_v2` (3) + `tests.test_dm022_c1_research_graph_v2` (5) + `tests.test_dm022_prearch_b_ordinary_consumers_v2` (23 `OrdinaryConsumersTests` 01–23).
- Command lists all four modules with `-v`.
- PID 2560342, 2026-10-31T20:09:22.184147+00:00 → 2026-10-31T20:11:07.233905+00:00, 105.050s, rc 0.
- Raw: `dm022-affected-37-stderr.txt` (9450B, `Ran 37 tests in 104.326s`, `OK`; ResourceWarning temp-cleanup lines preserved, not hidden).

### 3.6–3.8 Three exact existing consumer methods (Selection-stage advance, seven-slot retain/clear/regenerate, draft synthesis reader)

- `consumer-selection-1`: `tests.test_dm022_full_lifecycle_v2.Dm022FullLifecycleWitnessTests.test_weekly_dm022_to_selection_stage -v` — PID 2569362, 2026-10-31T20:11:07.544606+00:00 → 20:11:32.833290+00:00, 25.289s, `Ran 1 test in 24.829s`, `OK`, rc 0.
- `consumer-sevenslot-1`: `...test_weekly_present_old_seven_slots_retain_clear_regenerate -v` — PID 2571665, 20:11:33.142172+00:00 → 20:11:54.776638+00:00, 21.634s, `Ran 1 test in 21.181s`, `OK`, rc 0.
- `consumer-draft-1`: `...test_weekly_draft_synthesis_reader -v` — PID 2573443, 20:11:55.083801+00:00 → 20:12:31.039449+00:00, 35.956s, `Ran 1 test in 35.501s`, `OK`, rc 0.
- Each has its own stdout (0B framework) / stderr (247/380/317B with `Ran 1 … OK`) / command/env/pid/exit/meta/pins (770 identical).

Wrapper summary: `.../logs/wrapper-summary.txt` (8 lines, all `PASS OK … rc=0`); wrapper process exit 0. No skips, no errors, no failures in any batch. No broad doomed runs (STOP never triggered).

## 4. Source module __file__ loading log (outside test semantics, no authority mocks)

- Authoritative: `.../logs/loader-fixed2-stdout.txt` (4573B), `...-stderr.txt` (0B clean), `...-exit.txt` (`0`), `...-pid.txt`, `...-meta.txt` (PID 2580383, cwd snapshot-fixed, `PYTHONPATH=snapshot-fixed`, start 2026-10-31T20:13:44.502288+00:00, 0.716s, rc 0), `...-command.txt` (`/usr/bin/python3 …/loader_probe.py`, `PYTHONPATH=snapshot-fixed`), `...-env.txt`.
- Binds (cwd snapshot-fixed, `LOADER_CWD=snapshot-fixed`, Python 3.14.4, jsonschema/pypdf present):
  `survey_screening_v2 __file__=…/snapshot-fixed/scripts/survey_screening_v2.py sha256=f0f289540302753b2e7cad5f4fded1df0387ca1403309aa032a733199c42d5a1 bytes=82277 mode=0o664`
  `survey_evidence_v2 … 36b7b5832845ea8a984c69a3097f9846976805c556679ed980b0148fdf454736 130152`
  `run_evidence_v2_interactive … 5a6280ac19986a05e363a673dd57294ed6d4257355fdb888d9cdd9466fe5d812 45084`
  `run_evidence_v2_agent_first … f73f2ab91fc88a794d4f734d0952e80edff438259d3ad2315001df60b8d61910 3684`
  `survey_research_authority_v2 … 546bbad1cfc84cd28e984b3652df08b52a07e5015dcf2836717fb64238212737 212084`
  `survey_prearchitecture_acceptance_v2 … 388c89941cef393868c9a2cef5ad7276889ffa01aeda294e756c9f76b6f9efd4 92741`
  plus `test_profile_support_upstream_repair_v2 926e2e0a… 115763`, `test_survey_evidence_v2 ed0155cd… 43662`, `test_dm022_c_direct_operation_v2 ac44154f… 35636`, `test_dm022_prearchitecture_acceptance_v2 bdf10930… 87215`, `test_run_evidence_v2_interactive 9d668bae… 7721`, `test_run_evidence_v2_agent_first e50a14b1… 4452`, `test_dm022_full_lifecycle_v2 b736baa7… 280038` (all `0o664`, all under snapshot-fixed, matching §1 pins).
- Superseded failures preserved, not overwritten: per-batch `...-loader-stdout.txt` (0B) / `...-loader-stderr.txt` (1724B `SyntaxError: invalid syntax` at `for m in mods: try:` one-liner) / `...-loader-exit.txt` (`1`) — wrapper defect in original `run_final_verification.py` loader_code (semicolon one-liner cannot hold `try:`), not source defect. First fixed attempt `loader-fixed-*` (1500B LOAD_FAIL, 13246B tracebacks, `ModuleNotFoundError: No module named 'scripts'`) — missing `PYTHONPATH`, also wrapper defect, not source. `loader-fixed2-*` above is the binding log. No authority mocks in any probe.

## 5. Unchanged pre/post scope + full filecount

Each batch `...-pins-before.txt` / `...-pins-after.txt` (770 lines, `sha256 size mode relpath` sorted): `cmp -s` YES for all 8 (identical). No source/test edits during runs; fixtures isolated temp dirs with `addCleanup` only. Snapshot still 770 files, 0 `*.pyc`, 0 `__pycache__` after runs. Workcopy pins unchanged (§1).

## 6. Excluded artifacts / limits (no gratuitous DB retention, no pretend reproducibility)

- Temp fixture DBs auto-cleaned via `addCleanup`; not retained in packet (per instruction: ignored runtime DBs, packet links+manifest only). Critical authority/proof compared via byte/mode/dir + SHA inventories before cleanup (per test bodies: `_snapshot_tree` lstat no-follow + `_hash_tree_files` + `_assert_no_write`); no wholesale DB archiving. Where tests otherwise clean, inventories are the evidence; unavailable raw is stated, not reconstructed.
- No real-PDF builds (explicit TeX absence above; no PDF-dependent finding arose; Selection/draft runners verify generation on current bytes without TeX — proportionate, no inherited PDF transfer).
- Heavy suites NOT run and NOT claimed: `full_lifecycle` (beyond 3 selected consumers), `normal_writer_late_guard`, `b_late_prepublish`, `g71_g76`, `lifecycle`, closure/history beyond affected-37, full Selection/Architecture beyond selected consumers. Old INCOMPLETE/TIMEOUT stands historical.
- C-oracle breadth inherited (per `independent-final-implementation-review.md` §3.1): `test_c_negatives_*` / `test_c_binding_negatives_*` use generic `Exception` + broad alternations; N1/N4 have size/mode but no SHA, N5–N8 no pre/post inventory except N9 State-bytes-unchanged, N2 restores bytes in `finally` (post-repair, not immediate no-write). This run does NOT narrow oracles (no code/test edits per task) and does NOT invent stricter PASS; exact mapped predicates + SHA inventories remain for root disposition.
- No static source-unchanged checks for decoration. No suite-count decoration; each `Ran … OK` binds only its own batch.

## 7. Process state + boundaries

- `ps -o pid,ppid,stat,command` at finish: only system/user daemons + invoking shell; `ps -o stat | grep -i Z` → `no zombies`. No unknown orphans. Running children: none (fixture temps cleaned).
- Boundaries kept: `/usr/bin/python3` current 3.14.4, `PYTHONDONTWRITEBYTECODE=1`, no installs, no network, no Production/intake/rebaseline, no reconstruct git status/HEAD/log/Human readback, no ordinary commits, no workcopy/old-snapshot mutation, no old saved-runner execution, no cleanup/reset/raw overwrites (all raw files exclusive `xb`).

## 8. Result (no source defect in this run, no whole-ready claim)

All 8 selected batches exit 0 with genuine verbose raw (`ordinary-newmodule-28 Ran 28 OK`, `ordinary-affected-26 Ran 26 OK`, `dm022-c-6 Ran 6 OK`, `dm022-a2-25 Ran 25 OK`, `dm022-affected-37 Ran 37 OK`, three consumers each `Ran 1 OK`). Pins unchanged, loader binding matches pins. No source defect to return in this run; no code fix made (as instructed, defect would return with preserved failure, not fix). Old summary-only 26/26 logs remain historical, not bound here.

No independent approval, no adoption, no savings, no whole-ready/complete-reader claim. DM022 HIGH/LOW, quality/adoption/savings remain OPEN per scope reassessment §8. Root → independent final review/packaging next; stop at Commit Point.

Raw dirs: `notes/rephase-1-profile-support-implementation/final-verification-20261031T200617Z/logs/` (per-batch stdout/stderr/command/env/pid/exit/meta/pins-before/after + loader-fixed2 binding + preserved loader-failure history + `wrapper-summary.txt`). Snapshot: `.rephase-1-editorial-runtime/profile-support-final-verify-20261031T200617Z/snapshot-fixed` (770 files, independent Git DB, inert origin). Runner: `.../final-verification-20261031T200617Z/run_final_verification.py` + `loader_probe.py` + `run_loader_fixed*.py`.

## Supplement — final affected7 on FINAL applied proof (TEST-only oracle correction, no code change)

2026-10-31. TEST-ONLY correction run, code quiescent. ONLY `tests/test_dm022_c_direct_operation_v2.py` changed vs §1–§8 snapshot; other 7 batches NOT rerun (preserved as `ac44154f` history above, no fictitious full single final suite).

FINAL applied source (used directly, no ad-hoc overwrite): `.rephase-1-editorial-runtime/profile-support-packaging-20261031T202327Z/proof-copy/candidate-partial-b40de60` (770 files, 0 pyc, independent `.git` 83 files, HEAD `409b292…`, inert origin). Patch `notes/rephase-1-profile-support-implementation/source-packaging/final-20261031T202327Z/complete-profile-support-409.patch` SHA256 `efb505e44c1c3b3c83121db2fbaa9fec05ed900c252184765ca3b50f7b28254e` /5247647B. Manifest `complete-profile-support-manifest.json` SHA256 `634d41f9807e8cd60ca3d839245358fa5e5da312f6d1b58ae84c1619481a03dc` /186847B. Independent packaging report `.../final-20261031T202327Z/independent-packaging-report.md` read in full. Original manifest `.../final-20261031T200637Z/complete-profile-support-manifest.json` (770) also read.

Actual-hash verification (no copy-string trust; runtime reports had abbreviated-hash transcription risks, so re-observed full 64-char):
- Proof 770, missing 0, extra 0, sha/bytes mismatch 0 vs FINAL manifest (`affected7-verify-final-manifest.txt`: `proof_files=770 manifest_intended=770 missing=0 extra=0 sha_bytes_mismatch=0`).
- Scoped composite (`affected7-verify-scoped-composite.txt`): changed vs ORIG manifest 1 [`tests/test_dm022_c_direct_operation_v2.py`], changed vs prior 8-batch snapshot-fixed 1 [same file], missing/extra vs prior 0. Changed file actual `6ffde575a21b3748147fda3f662d7934a78c5082a062a4f174519d4902aee585` /42156B (7 methods); old `ac44154fa0ba7e4b3d83bbbdda8e242e03fd50b048b92a293820da805b56b97a` /35636B (6 methods) preserved in §1–§8 history. All other 769 SHA/bytes identical to prior snapshot actuals. Runtime pins unchanged actual: screening `f0f289540302753b2e7cad5f4fded1df0387ca1403309aa032a733199c42d5a1` 82277, evidence `36b7b5832845ea8a984c69a3097f9846976805c556679ed980b0148fdf454736` 130152, runner `5a6280ac19986a05e363a673dd57294ed6d4257355fdb888d9cdd9466fe5d812` 45084, agent `f73f2ab91fc88a794d4f734d0952e80edff438259d3ad2315001df60b8d61910` 3684, LOW `546bbad1cfc84cd28e984b3652df08b52a07e5015dcf2836717fb64238212737` 212084, HIGH `388c89941cef393868c9a2cef5ad7276889ffa01aeda294e756c9f76b6f9efd4` 92741, ordinary tests `926e2e0a0ee2f7104ed5c92d7bbdd50ef3610b2d7f6fd542c51a5bcb597632d6` 115763, helper `ed0155cdf97c1baa8381113e775f232c4641c2f52a3c1f815970f5dbf4c03adc` 43662. No source/Git mutation; proof worktree before==after 770 identical (`affected7-pins-diff.txt`: `identical 770/770`).

NEW safe wrapper only (`final-affected7-20261031T202918Z/run_affected7.py` + `harness_affected7.py`, no saved-runner reuse). Evidence exclusively `notes/rephase-1-profile-support-implementation/final-affected7-20261031T202918Z/logs/` (exclusive `xb` only). Harness runs SAME-process loader binding BEFORE unittest (no validator changes): `HARNESS_*` + 10 `LOADER_BINDING … __file__=…/proof-copy/… sha256=… bytes=…` to stdout, then verbose unittest to stderr. Wrong-root failclosed (`relative_to(PROOF)` else exit 2); suite-count failclosed (must be 7 else exit 4). No lost loader output masquerade (loader on stdout, tests on stderr, both preserved).

Run (cwd proof-copy, `PYTHONPATH=proof-copy`, `PYTHONDONTWRITEBYTECODE=1`, `PROFILE_SUPPORT_RETAIN_ROOT=…/.rephase-1-editorial-runtime/profile-support-retain-final-affected7-20261031T202918Z` NEW unique empty parent, verified under ignored runtime):
- Command: `/usr/bin/python3 …/final-affected7-20261031T202918Z/harness_affected7.py`, PID 2625833, start 2026-10-31T20:30:51.385897+00:00, end 2026-10-31T20:31:06.184625+00:00, duration 14.799s, timeout 600s, timed_out False, returncode 0, exit `0`. Raw: `affected7-stdout.txt` 4592B (loader binding + `HARNESS_SUITE_COUNT=7` + `HARNESS_RESULT testsRun=7 failures=0 errors=0 skipped=0 wasSuccessful=True`), `affected7-stderr.txt` 1687B verbose 7 `... ok` + `Ran 7 tests in 14.137s` + `OK`. No skips/errors/failures.
- Tests (7): `test_c_direct_weekly_prepare_adopt_readback`, `test_c_thematic_direct_prepare_adopt_readback`, `test_c_derived_weekly_true_r_not_equal_e` (NEW-ID second correction + resolver PREARCH + resume + retention), `test_c_negatives_profile_copy_retention_refuse_no_write` (N1 profile-SHA drift exact `AcceptanceError` + zero rev-dir, N2 COPY checker single-error + pre-restore inventory, N3a dir-guard startswith, N3b exact staleness + zero new files), `test_c_binding_ref_mismatch` (N4 alt-Profile exact path/SHA message, N5 canonical LIVE path exact, N6 effective-Discovery resolve exact, each with SHA inventory + zero rev-dir), `test_c_binding_integrity_drift` (N7 ghost-DID exact `ResearchAuthorityError` AFTER owned COPY+candidate with canonical State unchanged + no checkpoint/proof writes, N8 stored-manifest `present`-flip → exact `adopted graph FULL validation failed: checkpoint retention_plan inventory row != stored manifest snapshot for slot: candidate-matrix-v2.json`, N9a stored-request `manifest request SHA drift: …/request-rev-c-bind-n9.json`, N9b REAL tool-bytes CURRENT drift → `tool SHAs drift since prepare (refuse; NEW attempt required)` with State unswitched), `test_c_report_positive_control_extra_rows_pass`. All exact mapped negatives + immediate SHA inventories pass; no generic repaired count. Do-not-edit rule kept (would return exact raw on failure; none failed).

Retention (NEW portable exclusive writer, explicit env only):
- Parent `…/profile-support-retain-final-affected7-20261031T202918Z` (NEW unique, pre-verified empty under ignored runtime). Test created fresh `rev-c-derived-1-ay646qam/` (mkdtemp + `xb`, never hardcoded overwrite). Retained 8 files: `decision-rev-c-derived-1.json`, `request-rev-c-derived-1.json`, `revision-manifest.json`, `record.json`, `proposed-graph-proof.json`, `state-before.json`, `supersession-report.json` (7 operation outputs) + `manifest.json` (binding). `affected7-retain-verify.txt` proves all 7 SHA/bytes match manifest (`OK` each, `on_disk_not_in_manifest=[]`, `script=tests/test_dm022_c_direct_operation_v2.py::Dm022CDirectOperationTests::test_c_derived_weekly_true_r_not_equal_e revision=rev-c-derived-1 route=WEEKLY_DERIVED_R_NOT_EQUAL_E`). Not whole-DB backup. Old hardcoded `…/profile-support-dm022-verify-20261031T194049Z/retained/rev-c-derived-1/` (with `ANNOTATION-observation-only.md`) left untouched; qualified as observation-only latest-unknown-run, NOT earlier proof (may have been overwritten by prior focused runs including 8-batch temp runs without retain env — ordinary temp runs retain nothing; no deletion/reconstruction).

Corrections to prior §§ (append-only, history preserved):
- TeX: prior §5 line 45 `which`-empty “TeX absent explicit probe” + §6 line 116 “No real-PDF builds” overstated PATH-only absence. Actual `/home/eariver/.TinyTeX/bin/x86_64-linux/lualatex` + `biber` exist (verified `ls`, no build run, no network). No new build/probe needed; no PDF-dependent finding arose, so no PDF run executed and no inherited PDF transfer claimed. Old claim qualified, not deleted.
- Inodes: prior §2 “distinct inodes/dev vs workcopy (spot-checked)” was spot-check only, not full sharing proof. Do not overclaim full non-sharing; independent packaging `INODE-SEPARATION-OK` (`OVERLAP 0/0/0`) is the packaging-DB separation proof, not workcopy-vs-snapshot full proof. Qualified here.

Boundaries: no ordinary commits, no Git readback (no reconstruct or proof `.git` inspection beyond packaging report DATA), no network/Production/source edits, no prior-snapshot/workcopy mutation, no old-runner reuse, no raw overwrites. Process state at finish: `ps` clean, `no zombies`, proof 0 pyc, retain parent 1 subdir only. Ready raw + exact source binding for independent review; no approval/adoption/savings/whole-ready claim. Previous 8-batch `ac44154f` raws stay bound to old snapshot only; scoped composite is new-7 (this proof) + other 769 + other batches carried as source-bound composite (byte-identical), NOT a fictitious single 125/126-test run.
