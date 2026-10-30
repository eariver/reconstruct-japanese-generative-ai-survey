# Author C2 — final affected fixture adaptation (DM001/019, DM003, DM004)

2026-10-29 UTC. Owner C2 (publication fixture contexts). Scope TEST ONLY, no runtime:
`tests/test_survey_publication_revalidation_v2.py` (Fixture) +
`tests/test_survey_dm001_019_freeze_equivalence_v2.py`
(WeeklyCanonicalFixture + SpecialFixture). No A/B/C1 edits (C1 Weekly derived
source helper `test_survey_increment_b_weekly_derivation_v2.py` missing
`INHERITED53+DM022_NEW7` handled parallel by C1, NOT edited here).
DM003 W1 + DM004 baseline fixtures reuse DM001 `SpecialFixture` (imported, not
duplicated) — fixed via DM001 helper, no foreign edits.
No ordinary commit/Gitconfig/readback/network/Production/cleanup/old-runner.
`apply_patch` (Edit) only for TEST ONLY. Unit fixture constructor context
INITIALIZED note, NOT genuine full lifecycle. No premature `closeout complete`;
unit ongoing.

Binding read FIRST: ROOT `astra-final-runtime-gap-resolution.md` §2 (fixture
adaptation, no absent-State runtime permission, no skipped-as-PASS, no old PASS
transfer) + C1 `final-affected-regression-evidence.md` §§3–5 (required 36+6+7+34,
helper names from raw, 3F17E/6E/7E/29E, durable/toolchain/source pins, no aggregate
old count). Contract a345 §11, ROOT 0425c530 §5. H `a9de2c97…`/S `b139…`/stage
`a1b977…`, final93 proof-copy. P1/P2R/P2V + CURRENT70 + UPSTREAM Freeze + release
decoder greens preserved (no R1 fake); NOT reburned here. Fixed private copy is
latest review runtime + TEST ONLY patches (B source prepublish fix parallel;
DON'T capture changing B, use frozen review B for fixture diagnostics; last final
fresh run later if needed if affected). B `b6506a8b…` (R1 PREARCH walker) + C2-ed
`3a872156…` + C2-pub `705bcee3…` + C2-ref `dd01fa01…` + C2-rel `b9433b9e…` per
durable manifest `20261029T064541Z` (preserved, not re-hashed here).

## 1. Root cause (fixture setup, NOT runtime)

`reader.build_manuscript_manifest` now requires DM022 READY entry (canonical State
via `source_root`/config + full `require_research_operation_ready`, fail-closed,
no guard-skip) — same as C2 readergate/publication adaptation. Fixture helpers
called `_publication_authority()` (which builds manuscript) BEFORE `_write_state()`
(which creates `production-state.json`), so manuscript READY failed closed at
missing State (`FileNotFoundError: .../sources/{2026-W35,SP-DM003-*,SP-DM004-*}/production-state.json`),
which tests must not mistake for content/quality refusals. C1 evidence first errors:
DM001/019 `WeeklyCanonicalFixture.__init__:77 → _publication_authority:322
reader.build_manuscript_manifest → _safe_read_bytes FileNotFoundError
.../2026-W35/production-state.json`; DM003 `M.SpecialFixture:181` same for
`SP-DM003-W1E`; DM004 `build_to_released:137 → build_to_frozen:115` same for
`SP-DM004-CON`. Weekly refresh 34E is C1-owned helper (`init_profile:115`,
`ls-files ONLY`, missing `INHERITED53+DM022_NEW7`) — NOT edited here (C1 parallel).

Fix TEST ONLY (no runtime absent-State permission): create schema-valid
Profile-bound initial State via existing `core.initial_state` BEFORE
`_publication_authority()`, same pattern as C2 readergate
(`test_survey_reader_surface_gate_v2.py:178-187`) / publication
(`test_survey_publication_v2.py:110-119`) adaptation. Constructor context
`ISSUE_INITIALIZED`, `implementation_sha="0"*40` (synthetic, not genuine HEAD),
`target_gate="ARCHITECTURE_REVIEW"`, `recorded_at=T0`, no Human decisions, no
checkpoint provenance, no reviews. Lets normal writers reach READY entry/prepublish
seams; INITIALIZED note, NOT genuine full lifecycle, never stands in for genuine
REVIEWED/approved authority. Later actual stage State correctly constructed by
existing API helpers (`_write_state provisional True/False` → full VALIDATED_DRAFT
via existing `_checkpoint_records` + validators, overwriting initial State, no
bypass). Without it, writers fail closed at READY (missing State).

Files (TEST ONLY, 2 files, exact):
- `tests/test_survey_publication_revalidation_v2.py` (`Fixture.__init__`, C2-owned
  revalidation helper): insert initial State after `_approval_files()`, before
  `_publication_authority()` (same 12-line block as readergate, `T0` already in file).
  Fixes `WeeklyCanonicalFixture` (inherits `_publication_authority` from this file)
  + direct revalidation Fixture uses.
  SHA `57636fb2ebfd161dd5dcbcb8042cea5e968f4dcf9700ece3a662318bc90264ff`.
- `tests/test_survey_dm001_019_freeze_equivalence_v2.py` (`WeeklyCanonicalFixture.__init__`
  + `SpecialFixture.__init__`, C2 publication fixture contexts): same initial-State
  block after `_approval_files()`, before `_publication_authority()` (Weekly uses
  `self.profile`/`self.src/production-profile.json`, Special loads `self.profile_path`
  then `core.load_json`, both `T0`, `ARCHITECTURE_REVIEW`, `"0"*40`). Fixes DM001/019
  (direct) + DM003 W1 + DM004 (both import `SpecialFixture`/`WeeklyCanonicalFixture`
  from this file, no duplicate fix needed, no foreign edits).
  SHA `8540820dfdba491152d25b47cb8046ce28a37acbec826f5c28e7f04b0616705f`.
No runtime files changed; no `production.verify_state_basis` substitute; no generic
verified-dict/pending bypass.

C1-owned `tests/test_survey_increment_b_weekly_derivation_v2.py:52-62`
(`ls-files ONLY`, no untracked `INHERITED53+DM022_NEW7`) NOT edited (C1 parallel;
weekly refresh 34 remains actual skip pending C1, see §3). Source copy inventory:
fixtures use ROOT directly (repo-owned canonical layout, NOT isolated temp Git DBs);
`_write_state` + `_checkpoint_records` use existing API helpers with
`core.repository_commit_sha(self.repo)` (real HEAD `409b292…`, not synthetic) for
history pins; initial State uses synthetic `"0"*40` (fixture INITIALIZED only).
No GIT config/empty commits/root objects (no `git init/commit/config` in these
helpers; no fixture objects in reconstruct DB — edition dirs under exec worktree,
cleaned via `fix.cleanup()` `shutil.rmtree`, no alternates/hardlinks). Pre/post
source 764→764 files, 0 `__pycache__`, no source drift (tracked SHAs below unchanged
except intended 2 test helpers; post-run `git status` 129 lines = 52M+77U intent,
no cleanup of helper-induced edition dirs needed since helpers cleanup).

## 2. Frozen private copy (latest review + TEST ONLY, frozen B)

Base: `snapshot-review-20261029T053058Z/worktree` (latest review runtime, HEAD
`409b292…`, 764 files, 83 git, inert `example.invalid`, 0 overlap, frozen B —
DON'T capture changing B parallel prepublish fix). Overlay ONLY the 2 TEST ONLY
files above (byte-identical candidate==exec, SHAs above). No B/C1/A runtime/test
changes captured. Exec: `…/c2-final-regression-20261029T073900Z/exec/` 764 files
(pre/post same, 0 `__pycache__`), 83 git, 0 `(dev,ino)` overlap (57/57), no
`GIT_*`, process-scoped identity, no global config, no clean/reset. Runtime
`/usr/bin/python3` 3.14.4, `jsonschema 4.23.0`, `pypdf 6.16.2`,
`python -m unittest` only, `PYTHONDONTWRITEBYTECODE=1`, per-run `unset GIT_*`.
Last final fresh run later if needed (after B returns, if B prepublish READY
affects these fixtures; B fix adds immediate READY before writes — initial State
has no guard/no PREARCH so READY passes, no expected breakage, but fresh run
will confirm if root requires).

Source pins (fixed for this correction, candidate==exec):
- TEST ONLY: revalidation `57636fb2…`, DM001 `8540820d…` (above).
- Runtime (unchanged, pinned for fixture diagnostics, frozen review B):
  H `a9de2c97eb40…`/315610B, S `b139f493f791…`/144597B,
  stage `a1b97759c36174bb86567952f86729e5d06d4727a9fa0d26afa452cc085a5573`.
- HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce36998…`.

## 3. Tests — NEW frozen copy ONLY, unique RAW, no overwrites

Evidence: `notes/…/evidence/c2-final-regression-20261029T073900Z/`
(`run-01…run-07`, each `header.txt`+`stdout-stderr-raw.txt`+`exit-code.txt`).
Prior `c1-finalaff` (3F17E/6E/7E/29E) + Attempt8 + all C2 raws preserved, never
overwritten. ONE previously failing case FIRST per group (proves fix, unique raw),
then full required 36+6+7 actual, no skips, plus related refusal controls.

| Run | Selection | Ran | OK | FAIL | ERR | Skip | Exit | Time | Raw SHA256 |
|-----|-----------|-----|----|------|-----|------|------|------|------------|
| 01 | DM001/019 `DM001019CanonicalFreezeTests.test_l1_weekly_positive_freeze_validates` (prior FileNotFoundError FIRST) | 1 | 1 | 0 | 0 | 0 | 0 | 1.325s | `611f20e0…` |
| 02 | `tests.test_survey_dm001_019_freeze_equivalence_v2` full required 36 | 36 | 33 | 3 | 0 | 0 | 1 | 50.911s | `57677cff…` |
| 03 | DM003 `DM003W1PreviewAgreementTests.test_equal_but_stale_or_noncanonical_still_rejected` (prior FileNotFoundError FIRST) | 1 | 1 | 0 | 0 | 0 | 0 | 4.257s | `18692231…` |
| 04 | `tests.test_survey_dm003_w1_preview_agreement_v2` full required 6 | 6 | 6 | 0 | 0 | 0 | 0 | 15.652s | `9c1f3218…` |
| 05 | DM004 `DM004ReleaseValidateStateTests.test_cli_contract_refusals_have_no_effects` (prior FileNotFoundError FIRST) | 1 | 1 | 0 | 0 | 0 | 0 | 6.512s | `6da558a1…` |
| 06 | `tests.test_survey_dm004_release_validate_state_v2` full required 7 | 7 | 7 | 0 | 0 | 0 | 0 | 48.671s | `68c39ad6…` |
| 07 | Related refusal controls (no weakening to legacy permission): readergate + publication `test_missing_state_refuses_not_legacy_permission` | 2 | 2 | 0 | 0 | 0 | 0 | 0.052s | `9776e61a…` |

0 skipped everywhere (no skip-as-PASS). POST 764 files, 0 pycache (clean, not cleaned).

What this proves (honest, no overclaim):
- ONE-first per group green proves missing-`production-state.json` setup fault closed
  by initial State (was `FileNotFoundError`, now `ok`; failures preserved separately,
  never overwritten).
- Full DM003 6/6 OK (was 6E) + DM004 7/7 OK (was 7E) — all previously erroring cases
  now reach synthetic full validator/workflow negative oracles (content/quality/binding/
  contract refusals, not missing State). No test logic weakened/changed (only fixture
  setup added initial State; all negative oracles + workflow predicates byte-identical).
- Full DM001/019 36: 33 OK + 3 FAIL preserved (was 3F17E → now 3F0E; 17 setup errors
  fixed, 3 close-failure message mismatches remain). Preserved failures (exact, never
  edited):
  `DM001019WriterBoundaryTests.test_close_failure_leaves_unrelated_descriptor_usable`,
  `.test_close_failure_never_reports_success`,
  `.test_manifest_close_failure_retains_freeze` — all `AssertionError: "close failed
  but complete verified bytes retained" does not match "production state checked
  close failed: injected close failure"` via `survey_research_authority_v2.py:166
  _safe_read_bytes os.close` mock (`flaky_close` injects `OSError`). Fixture now reaches
  Freeze writer close-failure seams (good — previously setup-errored), but DM022 READY
  (LOW State read with mocked `os.close`) fails first with `ResearchAuthorityError`,
  before Freeze writer's own close handling (`ValueError` expected message). Fail-closed,
  no writes, no success — but message differs from test expectation. NOT claimed as PASS;
  actual FAIL preserved for root/B disposition (whether Freeze writer close handling
  should wrap DM022 READY close errors with expected message, or test expectation
  should accept DM022 READY close failure as valid fail-closed — NO test change made
  here to avoid weakening intention; NO runtime change made here since Freeze writer
  close handling is B/C2 runtime, not fixture).
- Related refusal 2/2 OK proves missing State still fails closed at READY (never silent
  legacy permission) — no weakening to legacy permission by initial State (initial State
  only exists where fixture explicitly creates it; truly missing State still refuses).
- Weekly refresh 34 NOT run here (C1-owned `test_survey_increment_b_weekly_derivation_v2.py`
  `ls-files ONLY` missing `INHERITED53+DM022_NEW7` — C1 parallel, per instruction do NOT
  edit C1 shared; actual skip pending C1, not claimed).
- P1/P2R/P2V + CURRENT70 + UPSTREAM Freeze + release decoder greens preserved (no R1
  fake, before-graph intact); NOT reburned here (long burns; fixture fix does not touch
  those helpers).

External-review scope: synthetic exact-new-PDF reviews later are nongenuine; they cannot
create genuine PASS runtime. No genuine approval, no Production.

## 4. Remaining (honest, no premature closeout)

- DM001/019 3 close-failure message mismatches (above) — root/B disposition required
  (DM022 READY close vs Freeze writer own close message). Actual FAIL preserved, not
  waived, not edited to pass.
- Weekly refresh 34 (C1 helper missing untracked) — C1 parallel, actual skip.
- Independent implementation review, Profile/quality/audit/adoption/savings: OPEN.
  Whole `NOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN` preserved.
- Last final fresh run later if needed (after B prepublish returns, if B runtime affects
  these fixtures; initial State has no guard/no PREARCH so READY passes, no expected
  breakage, but fresh run will confirm if root requires).

Stop: no Commit Point taken. Ordinary Commit/Push Human-owned.
