# Failed-batch archive — DM022 verification 20261031T155554Z

All dependent-suite runs failed at the common fixture setup gate (A prepackage
`verify_state_basis`: fake-SHA State vs real HEAD). No HIGH/LOW operation proof.
Per root: exact counts, honest classification, no approximations.

## Raw log inventory (all preserved, no overwrites)

Under `notes/rephase-1-profile-support-implementation/dm022-verify-20261031T155554Z/logs/`:

| Log stem | Exact raw tail | Classification |
|---|---|---|
| `a2-baseline-*` | `Ran 25 tests / FAILED (errors=26)` | Early setup failure (26 errors incl. 3 subtests of one tamper test; every error same State-basis `ValueError`) |
| `a2-weekly1-*` | `Ran 1 test / FAILED (errors=1)` | Same setup failure, focused single |
| `b-consumers-*` | `Ran 23 tests / FAILED (errors=10)` | Same setup failure (10 chain-building tests; 13 non-chain tests unaffected) |
| `presence-*` | `Ran 3 tests / FAILED (errors=3)` | Same setup failure |
| `depth-presence-*` | `Ran 31 tests / FAILED (failures=2, errors=28)` | 28 same setup errors + 2 failures incl. one harness preemption: depth duplicate-guard self-tripped on the `timeout`-wrapper process tree (3 cmdline matches: shell+timeout+python). Rerun without wrapper avoids it; not a product defect |
| c1 trio | `Ran 14 tests / FAILED (errors=3)` | Terminal-observed ONLY, no raw file saved (honest gap; not rerun — doomed while setup fails) |
| 8-file batch | no log | **INCOMPLETE/TIMEOUT** (600s tool timeout, process killed; lifecycle/guard suites heavy). Not "not-run" |

## Corrections to prior return

- `test_profile_support_upstream_repair_v2.py:723` is NOT a missing shipping caller: the
  keyword-less invocation was a deliberate `TypeError` oracle in the rejected D draft,
  already replaced by proper negative tests. Missing mandated keywords in a negative
  oracle is not a migration defect. Prior claim withdrawn.
- The timed-out batch is INCOMPLETE/TIMEOUT per root, not "not-run".
- Depth guard trip is harness preemption (wrapper self-match), classified separately
  from the 28 setup errors.

## Common gate traceback (all setup errors)

`survey_screening_v2.py:751 resolve_prepackage_root_effective →
core.verify_state_basis → ValueError: implementation commit differs from authoritative
state`. Helper builds State with `IMPLEMENTATION_SHA="4"*40`; new resolver observes
actual HEAD. Disposition per root: NO fake-SHA threading; fixtures migrate to real
committed source BEFORE initialize (ordinary owner fixing shared helper; C does not
race-edit it).
