# Operation correction — HIGH/Freeze parallel disjoint ownership
# HumanHEAD f84fcf5. Selected contract 478f / root 7d7d5a45 §6.
# OWN ONLY: survey_versioned_renewal_v2.py + survey_publication_v2.py + new tests.
# Others own source proof and Reader, no overlap.

2026-10-25. Author correction for independent-operation-review B1-B3.

## Scope
- B1: typed renewal authority (proof/basis/COPY/trio/current tools) into Freeze
  snapshot + preflight lexical/inode overlap. No generic walker. ROOT correction:
  _existing_compatible_bytes REFUSES divergent bytes; missing overlap guard is
  contract gap, not confirmed overwrite.
- B2: HIGH FD-safe reads, canonical lexical spelling, cfg/Profile/State rechecks.
- B3: exact path+SHA+inode; alias REFUSE BEFORE writes, NOT ALREADY_ACTIVE.
- Style: U CURRENT template vs retained trio.style; C allowed on mismatch.
- prepare-targets documented as declared C half.

## Files changed (writable candidate, owned only)
- scripts/survey_versioned_renewal_v2.py
- scripts/survey_publication_v2.py
- tests/test_versioned_renewal_operation_correction_b1b2b3.py (new)

## Test strategy
- NEW independent frozen baseline (copy of snapshot-work 731) + only patch
  snapshot (2 scripts + new test). NOT shared candidate.
- Real old R3/C/U input preserved (high24 U3d proof/basis/Candidate/approval
  copied read-only; high24 originals never modified).
- New SOURCE commit before authorities in isolated fixtures where new files
  could become authorities (see make_operation_correction_20261025T060000Z.sh).
- No stale SELF, no bound companions sidecar.
- No cleanup/reset/deletion/old-runner/network/candidate/reconstruct commit.
