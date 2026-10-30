# Author C2 — final fault-oracle resolution (close-fault targeting + weekly 53+7)

2026-10-29 UTC. Owner C2. Scope TEST ONLY, no runtime (runtime C2 unchanged;
actual new bug → ROOT before fix, none here): `tests/test_survey_dm001_019_freeze_equivalence_v2.py`
(3 close-fault targeting), `tests/test_survey_weekly_mechanical_refresh_v2.py`
(53+7 finite list + tightened pointer oracle, C2-owned), plus prior
`tests/test_survey_publication_revalidation_v2.py` (initial State, from prior unit,
preserved). No A/B/C1 source edits (C1 IncrementB `c87da3e7…` pin used as-is, no
cross-edit; C1 WeeklyRefresh private `07efef1e…` inspected, permanent C2 fix with
same 53+7 literal + unittest SHA checks, not bare assert). No ordinary commit/
Gitconfig/readback/network/Production/cleanup/old-runner. `apply_patch` only.
Unit fixture INITIALIZED note, NOT genuine lifecycle. No premature closeout;
unit ongoing.

Binding read FIRST: ROOT `astra-final-runtime-gap-resolution.md` §2 (no waiver,
no skipped-as-PASS, no old PASS transfer, no global atomicity) + C1
`final-weekly-depth-regression-evidence.md` (private exec path/diff, 53+7 literal,
tightened pointer oracle, runtime unchanged) + C1 `final-affected-regression-evidence.md`
§§3–5 (36+6+7+34 required, helper names from raw, 3F17E/6E/7E/29E, no aggregate).
Contract a345 §11, ROOT 0425c530 §5. H `a9de2c97…`/S `b139…`/stage `a1b977…`.
P1/P2R/P2V + CURRENT70 + Freeze UPSTREAM + release decoder greens preserved (no R1
fake); NOT reburned here. Fixed private copy is latest review 764 + TEST ONLY +
C1 pin (frozen B, don't capture changing B2); last final fresh run later if
affected (B prepublish parallel).

## 1. DM001 3 FAIL — early LOW vs intended owned pair close (TEST fault targeting, NOT runtime weakening)

Prior `c2-final-regression-20261029T073900Z/run-02-dm001-full` (initial-State fix
only): 36 Ran, 33 OK + 3 FAIL preserved, 0 ERR (was 3F17E → 3F0E; 17 setup
`FileNotFoundError .../production-state.json` fixed). Preserved failures (never
overwritten):
- `DM001019WriterBoundaryTests.test_close_failure_never_reports_success`
- `DM001019WriterBoundaryTests.test_manifest_close_failure_retains_freeze`
- `DM001019WriterBoundaryTests.test_close_failure_leaves_unrelated_descriptor_usable`
All `AssertionError: "close failed but complete verified bytes retained" does not
match "production state checked close failed: injected close failure"` via
`survey_research_authority_v2.py:166 _safe_read_bytes os.close` mock
(`flaky_close` first/second/every close) hitting DM022 LOW State read (READY)
before writer. Fail-closed, no writes, but wrong seam (early READY, not owned
Freeze/manifest pair) + wrong message (LOW `ResearchAuthorityError`, not Freeze
writer `ValueError` expected oracle). Never match new early error or broaden regex.

Fix TEST ONLY (same files, no runtime `survey_publication_v2.py` change):
- Track `os.open` (owned writer exclusive `O_CREAT|O_EXCL|O_WRONLY`, never LOW
  `O_RDONLY`): `opened[fd]=(path,flags)` only for owned creates.
- `flaky_close(fd)`: pop `opened[fd]`; fail ONLY if target path (`freeze-close`,
  `manifest-mclose`, `freeze-sentinel` respectively) + owned flags, else
  `real_close` (LOW State reads, sentinel `O_TRUNC` no-`O_EXCL`, unrelated FDs
  never faulted). Call REAL close appropriately then raise ONLY intended fault
  once (`target_n==1` Freeze, `==2` manifest second target, `failed-once` sentinel
  first target + sentinel `real_open` reuse-proof).
- Prove healthy positive reaches write + target close counter: `target_n` asserted
  (`==1`/`==2`/`failed-once` + `sentinel-ok`), retained bytes + second healthy
  build outside mock (`f2==retained`, `validate_release_manifest` where applicable)
  + immediate outputs + partial/idempotent outcomes original expectations preserved
  (`close failed but complete verified bytes retained` / `completed Freeze record
  retained` verbatim, NOT broadened to LOW message).
- Never match new early error (`production state checked close failed` must NOT
  appear in new passing raws for these 3 tests) or broaden regex (keep original
  `assertRaisesRegex` strings byte-identical).

Source pins (candidate==exec, TEST ONLY):
- `tests/test_survey_dm001_019_freeze_equivalence_v2.py`
  `f82b331892201743bacb4343b3c33fa0b556bea7a594ff06ee42e40683a9e0e3`
  (initial State `57636fb2…` pattern + fault targeting above, no runtime).
- `tests/test_survey_publication_revalidation_v2.py`
  `57636fb2ebfd161dd5dcbcb8042cea5e968f4dcf9700ece3a662318bc90264ff`
  (initial State only, preserved from prior unit).

## 2. Weekly 34 — C2 permanent 53+7 (private verified, not unshipped green)

C1 private exec `exec-c1-weeklydepth-20261029T071500Z` proves Weekly 34/34 PASS
with complete fixtures (IncrementB `c87da3e7…` 53+7 + WeeklyRefresh private
`07efef1ea94c…` 53+7 literal + tightened pointer oracle, runtime H/S unchanged).
Candidate-work `test_survey_weekly_mechanical_refresh_v2.py` untouched (`0c76bb0…`
in review) — C2 owned per coordination, C1 did NOT cross-edit (private exec only
+ exact `diff -u` 98 insertions for C2 review).

C2 permanent fix in candidate-work (this unit, TEST ONLY, no runtime):
- Same 60-file literal as private: recipe `.latexmkrc` (mirrors P1 helper SHA check)
  + INHERITED53 (53 verbatim, final-depth 40M+53A) + DM022_NEW7 (7 REQUIRED 2+5),
  standalone literal (no circular P1 import), explicit (no wildcard/count-only).
- C2 discipline (stricter than private bare `assert`): `self.assertTrue(src.is_file())`
  + `shutil.copyfile` + `self.assertEqual(core.sha256_file(src), core.sha256_file(dst))`
  BEFORE `git init/add -A/commit` (source commit before authority), process-scoped
  `IDENTITY` (`GIT_AUTHOR/COMMITTER_*`), no global Git config, no empty commits,
  no root objects. Declared fixture `before Source Commit` preserved.
- Same tightened pointer oracle as private (ROOT-approved TEST-ONLY): `before =
  _snapshot([state, receipt, gate])`, exact `missing-r9.json` + `selection mode
  probe missing` + `VERSIONED_ACTIVE/invalid` + `versioned renewal unselected`,
  no-write `before==after`, no `.lock`/`.retention` files (proves R1 refuses in
  VERSIONED_ACTIVE before any write, not any-Exception loose OR).
- C1 shared `test_survey_increment_b_weekly_derivation_v2.py` candidate patched
  `c87da3e76c49…` already includes 53+7 (verified, NOT edited here — no cross C1
  source edit).

Source pins (candidate==exec):
- `tests/test_survey_weekly_mechanical_refresh_v2.py`
  `51eeafe3dd71be04323080971784dca29ae433fed2d48e1c65c33381467329ae`
  (53+7 + tightened pointer, C2 permanent; private `07efef1ea94c…` exec-only
  superseded for candidate-work, preserved in C1 evidence, never deleted).
- `tests/test_survey_increment_b_weekly_derivation_v2.py` (C1 owned, used as-is)
  `c87da3e76c49e33f1a033fefc057d7098797b230e6d31b0b485fda3f292937ef`.

Weekly 34 must match private verified intended candidate bytes (same 60-file
intended fixtures + same tightened oracle, not just reported green from unshipped
private test). Permanent file differs in style (unittest SHA checks vs bare assert)
but same intended 60-file set + same tightened pointer assertions — proves same
intended 34/34, not unshipped green.

## 3. Frozen private copy (review 764 + TEST ONLY + C1 pin, frozen B)

Base: `snapshot-review-20261029T053058Z/worktree` (latest review runtime, HEAD
`409b292…`, 764 files, 83 git, inert `example.invalid`, 0 overlap, frozen B —
DON'T capture changing B/B2 parallel prepublish). Overlay ONLY (byte-identical
candidate==exec):
- revalidation `57636fb2…`, DM001 `f82b3318…`, weekly refresh `51eeafe3…`,
  IncrementB C1 pin `c87da3e76…` (4 files).
Exec: `…/c2-final-fault-20261029T085442Z/exec/` 764 files (same count: 4 paths
overwritten, no new paths), 83 git, 0 `(dev,ino)` overlap (57/57), 0 `__pycache__`
PRE/POST, no `GIT_*`, process-scoped identity, no global config, no clean/reset.
Runtime `/usr/bin/python3` 3.14.4, `jsonschema 4.23.0`, `pypdf 6.16.2`,
`python -m unittest` only, `PYTHONDONTWRITEBYTECODE=1`, per-run `unset GIT_*`.
Old `c2-final-regression-…` (3 FAIL preserved) + C1 `c1-finalaff-…`/`c1-weeklydepth-…`
(3F17E/6E/7E/29E + private 34/34) + Attempt8/durables preserved, never overwritten.
Last final fresh run later if needed (after B prepublish returns, if B runtime
affects these fixtures; initial State has no guard/no PREARCH so READY passes,
no expected breakage, but fresh run will confirm if root requires).

## 4. Tests — NEW frozen copy ONLY, unique RAW, numeric exit, pre/post source

Evidence: `notes/…/evidence/c2-final-fault-20261029T085442Z/`
(`run-01…run-06`, each `header.txt`+`stdout-stderr-raw.txt`+`exit-code.txt`).

| Run | Selection | Ran | OK | FAIL | ERR | Skip | Exit | Time | Raw SHA256 |
|-----|-----------|-----|----|------|-----|------|------|------|------------|
| 01 | DM001 3 fault targeted (never/sentinel/manifest, owned FD only) | 3 | 3 | 0 | 0 | 0 | 0 | 1.857s | `b61b2602…` |
| 02 | `tests.test_survey_dm001_019_freeze_equivalence_v2` full required 36 | 36 | 36 | 0 | 0 | 0 | 0 | 45.488s | `a4aba08d…` |
| 03 | DM003 ONE control `test_equal_but_stale_or_noncanonical_still_rejected` (no repeat full 6 unless shared changes; shared IncrementB/weekly do NOT affect SpecialFixture) | 1 | 1 | 0 | 0 | 0 | 0 | 3.873s | `64698ebe…` |
| 04 | DM004 ONE control `test_cli_contract_refusals_have_no_effects` (same reason) | 1 | 1 | 0 | 0 | 0 | 0 | 5.940s | `83c71a2f…` |
| 05 | `tests.test_survey_weekly_mechanical_refresh_v2` full required 34 (must match private 34/34 intended) | 34 | 34 | 0 | 0 | 0 | 0 | 530.120s | `a410124f…` |
| 06 | Related refusal controls (no legacy weakening): readergate + publication `test_missing_state_refuses_not_legacy_permission` | 2 | 2 | 0 | 0 | 0 | 0 | 0.050s | `29b44fb3…` |

0 skipped everywhere (no skip-as-PASS). POST 764 files, 0 pycache (clean, not cleaned).

What this proves (honest, no overclaim):
- Targeted 3 fault green with owned-FD restriction (target close counters `==1`/`==2`/
  `failed-once` + sentinel `sentinel-ok` + `real_close` appropriately + raise once)
  + healthy second builds outside mock (`f2==retained`, `validate_release_manifest`)
  + immediate outputs/partial/idempotent original expectations (`close failed but
  complete verified bytes retained` / `completed Freeze record retained` verbatim).
  Never matched new early LOW error (`production state checked close failed` absent
  in new passing raws; first 3 failed raws preserved in prior `c2-final-regression-…`
  `run-02-dm001-full` with `ResearchAuthorityError`, never overwritten/deleted).
- Full DM001 36/36 OK (was 33/36 + 3F in prior `c2-final-regression-…`; 17 setup
  errors already fixed by initial State, now 3 fault oracles fixed by targeting —
  all synthetic full validator/workflow negative oracles actually reached, not
  weakened/changed intention (same `assertRaisesRegex` strings, same `validate_*`
  + workflow predicates, same `f2==retained` idempotent checks).
- DM003/DM004 ONE controls green (no repeat full 6/7 — already green 6/6 + 7/7 in
  prior unit with same DM001 helpers; shared IncrementB/weekly changes do NOT affect
  SpecialFixture path, one-control proves no regression; full 6/7 NOT re-burned).
- Weekly 34/34 OK with permanent C2 fix (same intended 60-file fixtures + same
  tightened pointer oracle as private `07efef1e…` 34/34 PASS, not unshipped green:
  permanent file `51eeafe3…` differs in style (unittest SHA checks vs bare assert)
  but same intended set + same tightened assertions; C1 IncrementB `c87da3e7…`
  already includes 53+7, no cross-edit).
- Refusal 2/2 OK proves missing State still fails closed at READY (never silent
  legacy permission) — no weakening by initial State (initial State only where
  fixture explicitly creates it; truly missing State still refuses).

External-review scope: synthetic exact-new-PDF reviews later are nongenuine; they
cannot create genuine PASS runtime. No genuine approval, no Production.

P1/P2R/P2V + CURRENT70 + Freeze UPSTREAM + release decoder greens preserved (no R1
fake, before-graph intact); NOT reburned here (fixture fix does not touch those helpers).

Runtime C2 unchanged in this unit (only `tests/` edited: DM001 fault targeting +
WeeklyRefresh 53+7/tightened + prior revalidation/DM001 initial State; no
`scripts/` diff vs review 764 — `diff scripts/` empty except frozen B baseline).
If actual new runtime bug found, return ROOT before fix (none found; 3 FAIL were
test fault targeting, not runtime).

## 5. Remaining (honest, no premature closeout)

- B source prepublish fix parallel (`build_stage_checkpoint`/`advance_with_checkpoint`/
  `approve_architecture`/`approve_publication_preview` final READY) — DON'T capture
  changing B (frozen review B used here); last final fresh run later if needed (if B
  runtime affects these fixtures; initial State READY passes, no expected breakage).
- Depth 32/33 NEW fixture (30 legacy actual commits + C2 editorial helper + frozen64
  durable) — C1 to return precise missing pieces, not forged here (preserved).
- Independent implementation review, Profile/quality/audit/adoption/savings: OPEN.
  Whole `NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN` preserved.

Stop: no Commit Point taken. Ordinary Commit/Push Human-owned.
