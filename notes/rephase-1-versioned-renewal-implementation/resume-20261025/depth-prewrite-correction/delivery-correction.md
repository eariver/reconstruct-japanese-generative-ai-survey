# Depth pre-write cap — DELIVERY correction (writable candidate was stale)

2026-10-25. DELIVERY fix ONLY. No new runtime changes beyond already-tested
+27-line HIGH guard + new depth test.

## Prior overclaim acknowledged

Prior work reported “candidate fixed” after testing in
`versioned-renewal-depth-rewrite-…/fixture-weekly` (HEAD `280319c`, HIGH `3db…`,
new test present, public32 chain32 / prepare33 pre-write refusal verified).
PACKAGING + both reviewers found the writable delivery candidate still carried
the old bytes. First packaging `92` files / `741` source is therefore an
OBSOLETE delivery, not the selected final. This file corrects delivery by
transporting the EXACT already-tested 2 files to the writable candidate.
No new logic, no new test content, no schema change.

## Pre-transport verification (writable candidate was stale)

- Writable candidate:
  `.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work/scripts/survey_versioned_renewal_v2.py`
  FILE SHA256 `1dad1ad12ba509c477ea97fb3a22e5156ae1627182f3286f373f32eae7ba2fbb` exactly.
- Writable candidate test absent:
  `.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work/tests/test_survey_versioned_renewal_depth_prewrite_v2.py`
  did NOT exist before transport.

## Tested source location (recorded fixture/snapshot)

- EXACT tested HIGH:
  `.rephase-1-editorial-runtime/versioned-renewal-depth-rewrite-20261025T200000Z/fixture-weekly/scripts/survey_versioned_renewal_v2.py`
  SHA256 `3dbdedb8b44b366b129cc351b25a8bb898a62ad23e424d27e46c3df85a6a6d0b`.
- EXACT tested new test:
  `.rephase-1-editorial-runtime/versioned-renewal-depth-rewrite-20261025T200000Z/fixture-weekly/tests/test_survey_versioned_renewal_depth_prewrite_v2.py`
  SHA256 `ea2646381a41139a950deb1b6f60e6e27649beedee5ac3c4b5169c46fc63fdb8`.
- Snapshot copy (same HIGH bytes):
  `.rephase-1-editorial-runtime/versioned-renewal-depth-rewrite-20261025T200000Z/snapshot-fixed/scripts/survey_versioned_renewal_v2.py`
  SHA256 `3dbdedb8b44b366b129cc351b25a8bb898a62ad23e424d27e46c3df85a6a6d0b`.
- Fixture HEAD `280319c` has only derivation comment vs fix `d39fb89`:
  `d39fb89:scripts/survey_versioned_renewal_v2.py` SHA `3dbded…`,
  `280319c:scripts/survey_versioned_renewal_v2.py` SHA `3dbded…` (HIGH same),
  `d39fb89..280319c --stat` = `scripts/survey_weekly_derivation_v2.py | 2 ++` only.

## Full SHA + diff (27+/0- guard only)

- Before: HIGH `1dad1ad…` (candidate-work).
- After: HIGH `3dbded…` (tested fixture/snapshot).
- `diff -u` = 27 insertions, 0 deletions:
  `+def _require_new_chain_capacity…` (26-line helper, ENTRY check
  `chain_length+1<=32`, verified count not filename maxseq, ALREADY preserved,
  no cap change/loosening/synthetic/caller permit) +
  `+    _require_new_chain_capacity(prior_history, "ENTRY")` (1-line ENTRY call).
- Orphan matching-intent (`_refuse_matching_intent_orphan`) + anchor pre-write
  checks (`_copy_hist_anchor`, pre-write anchor/hypothetical-State validation)
  unchanged (diff shows additions only, no modifications/deletions).
- H `74275d22a342014009d5d090fbe9c552981941e90259c298065d2ba6929d1f3d`
  unchanged. S `2290ddd0dc8397f86451aff70d50fd4da0c6184fcf1bef3ed96259642af2d1eb`
  unchanged.

## Exact transport (2 files, no other files)

Applied via dedicated editor (not blind whole-fixture copy, not old code/test data):

1. `…/candidate-work/scripts/survey_versioned_renewal_v2.py`
   := tested `3dbded…` byte-for-byte (helper + ENTRY call only).
2. `…/candidate-work/tests/test_survey_versioned_renewal_depth_prewrite_v2.py`
   := tested `ea2646…` byte-for-byte (new, 106 lines, 6 tests).

No other candidate-work files touched. No ordinary commit. No reconstruct DB
writes (`.rephase-1-editorial-runtime/` is gitignored). No schema changes.
First packaging `92` / source proof / material source preserved as history;
packet `notes/rephase-1-versioned-renewal-implementation/source-packaging/`
(`complete-versioned-renewal-409.patch`, `complete-versioned-renewal-manifest.json`
delta `92`) NOT overwritten.

## Post-transport verification

- Candidate HIGH == tested `3dbded…` byte-for-byte (`diff -q` SAME).
- Candidate new test == tested `ea2646…` byte-for-byte (`diff -q` SAME).
- Other intended runtime unchanged: H `74275d…`, S `2290ddd…` same in
  candidate-work before/after.
- Root HEAD `f84fcf5` unchanged, `git diff --stat` empty,
  `git diff --cached --stat` empty (only `?? notes/…/resume-20261025/` +
  `?? notes/…/source-packaging/`, no staged, no reconstruct commit).
- No new runtime rerun needed: exact bytes already public32
  (`high-u32-rewrite2` ACTIVATED r34 chain32 State→r34 strict PASS) /
  prepare33 pre-write refusal (`BASIS_ENTRY_INELIGIBLE ENTRY REFUSED_PRE_WRITE`
  prior 32+1>32, no new R/record/temp, inventory exact same) /
  ALREADY32 readonly tested in fixture with identical bytes.

## Expected repackaging

Root packager recompute: FINAL `93` files (`92` + new depth test) /
`742` source (`741` + new test). This delivery file does NOT overwrite the
prior `92` packet; it records transport for the new FINAL.

No CommitPoint. No whole PASS claimed.
