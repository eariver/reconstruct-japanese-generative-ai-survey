# Final affected — duplicate DID fix §8 (independent runner, read-only)

Packet: `notes/rephase-1-supplement-carry-repair-20261106/final-affected-20261107T040550Z/`
Workcopy: `.rephase-1-editorial-runtime/supplement-carry-implementation-20261106T131722Z/candidate-work` (no source/test changes)
Previous raw preserved incl old failed C batch `affected-verification-20261107T031826Z/batch-05-c-direct-raw.txt`; not summed. Scale heavy 2 NOT rerun (old valid unique 409/160 shape unchanged; qualified composite).

## Binding stable 773 pre==post

- 771 tracked +2 new (focused a8aa, scale 7118) =773; 3M (LOW/HIGH/Ctest) +2?? unchanged
- LOW 7f5fc9e0d79729d98345f0b0352d5070c76e93f92f2c14148e22c9f38a8f4c0f, HIGH f312f02e..., focused a8aaafe3... (17), scale 7118092f..., Ctest 1fa905bf...
- Load roots: proof workcopy scripts/... (see pre-loaded-module-paths.txt)
- Clean Git env process identity, PYTHONDONTWRITEBYTECODE=1, no HOME/config/ordinary commit/network/Production/reconstruct readback; fixtures own temp-DB lifecycle only, no external cleanup

## Batches (separate PIDs, unmasked exits)

- Batch 01 FULL focused 17: `tests.test_dm022_supplement_carry_v2` 17 run / 17 pass / 0 fail / 0 skip, 33.735s, exit 0 (PID 805817, 040559Z-040634Z). Covers valid HIGH all routes + novel/unchanged/replaced/late + duplicate 3 (860/890/912).
- Batch 02 FULL C-direct 7: `tests.test_dm022_c_direct_operation_v2` 7/7/0, 18.326s, exit 0 (PID 807581).
- Batch 03 selected A2 3 no-supp: weekly + thematic + repeat anchor: 3/3/0, 10.355s, exit 0 (PID 808943).

No unexpected failure (no fix/rerun). No full-suite/semantic claim.
