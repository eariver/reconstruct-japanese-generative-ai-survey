# Reader F4 correction — source pins (20261025)

Ownership: scripts/survey_reader_publication_v2.py + tests/test_versioned_renewal_reader_f4_20261025.py ONLY.
Schema schemas/reader-manuscript-v2.schema.json UNCHANGED (no XOR global; canonical neither allowed).
Other authors HIGH+publication/source-proof untouched.

## Fixed snapshot (READONLY)
- .rephase-1-editorial-runtime/versioned-renewal-freeze-20261024T174422Z/snapshot-work
- HEAD 409b292756dd1277b9dfae87679934c0d2ce251c (actual409)
- scripts/survey_reader_publication_v2.py 91de5cb69ba37c356f2dbd29d25bd1b4352d21ac30e1afdc985d86d4049e650d (pre-fix)
- schemas/reader-manuscript-v2.schema.json 426f5a3689e2bc2829138893a8a28f0fc1fc6e696d373419a49f5cf16e8bb4f3 (unchanged)

## Writable candidate (dirty, NO ordinary commit)
- .rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work
- HEAD 409b292756dd1277b9dfae87679934c0d2ce251c
- scripts/survey_reader_publication_v2.py 098a2c8222f15f693c524139f2678be008a7ec9fafca275fc831ede9aa13bf1c (F4 fix, unchanged since v1)
- tests/test_versioned_renewal_reader_f4_20261025.py (new, v5 CURRENT):
  58e33ccacb77e8e077ebc642b1d293e8990c810d98ff0c20651a326dee7cca6f
- Status: 39M (tracked, incl. fixed reader) + 43U (42 frozen + 1 new F4 test) = 82 lines; only diff vs snapshot is OWN 2 files.

## NEW isolated snapshot (independent DB, TEST-ONLY SOURCE commits)
- .rephase-1-editorial-runtime/versioned-renewal-readerf4-20261025T060000Z/snapshot-work
- Base HEAD 409b292756dd1277b9dfae87679934c0d2ce251c
- a21b2637dbd564c8ffc50239ba65105767ec4fa1 (v1 fix + v1 test, 82 files)
- df1b3c545aadc84468656414e4a542e49c499e52 (test v2)
- 12c082db607b41d1800e7ed0bb2a2edbce2cce88 (test v3)
- 8e4f9f454320ce7ba7712badbe7283d90e90af5e (test v4)
- de95c6b6ad0719f5894b7c09d82608962fce0ea2 (test v5 CURRENT, 5 PASS + 2 PENDING)
- Worktree 732 files (731 frozen + 1 new F4 test; fixed reader overwrites 1 of 731).
- .git 83 files, no alternates, inert example.invalid, dev:ino disjoint, nlink==1 (see make_iso-stdout.txt).

## Weekly fixture (high24, READONLY except unique f4- tmp, restored)
- .rephase-1-editorial-runtime/versioned-renewal-high24-20261025T040000Z/renewal-weekly
- HEAD 50b03a64627a8bbcc725c7fcbebc3d30dce84c9b (G6 CURRENT)
- G1 commit 3d456e50b64723e67113db5fdfffc74bd57e9a0d (old-epoch pending)
- C1 manuscript 035fdc1c1d407c2379b53d00cf17b730b515096e9f5c732ee58cfee2560497a9
- C1 proof 043b0fc15c31366b66562023fc299f4a8caea0421a5346f537b1a573b26c3423
- U1 proof 551985955b0ca97e361fcb5f50b3569993c4f09ad94120f419380eb8a0143cfb
- U3d proof ecd4a5cd555ccaf1ebd0dace297187d95f6f3df9b4d6fc46b4be8a7984b3f5cc
- Editorial manuscript cff7253d0dedd3d22e69ec98ef7b7f27a30763d88065b32f7d44f8fe94f19a17
- Canonical manuscript 345c589b5c03838a35567e88eb5b3056a2c6f5cc4747a95eab7f0ee166f3e1df

## Test result (isolated de95c6b, PYTHONDONTWRITEBYTECODE=1)
- Command: python3 -m unittest tests.test_versioned_renewal_reader_f4_20261025 -v (cwd=isolated DST, READER_F4_WEEKLY_ROOT=high24 weekly)
- Exit 0, 7 tests: 5 PASS + 2 SKIP (explicit PENDING, no stub).
- PASS: neither+proof REFUSE, sibling+current REFUSE, canonical PASS, canonical+proof REFUSE, U-after-C (C1+U3d CURRENT) PASS.
- PENDING: correct-C-own + U-editorial-own at G1 (scratch quota/history limits; see test docstrings + v3/v4 attempt logs).
- Mutation restore: PRE_CLEAN_OK, POST_CLEAN_OK, original SHAs unchanged (see test-stdout.txt).
- Raw: test-exit.txt (0), test-stdout.txt, test-stderr.txt; v4 attempt logs preserved as -v4-attempt.

## Scope failures / limits
- Old-epoch PASS (C-own, U-editorial-own) PENDING, not proven here (needs G1-epoch isolated repo with .git history; full-archive hit Errno 122, minimal lacks .git).
- No HIGH/publication/source-proof edits; no schema change; no whole-unit PASS; no CommitPoint.
- No network/old-runner/cleanup/reset/ordinary candidate/reconstruct commit (writable candidate dirty, isolated commits are TEST-ONLY in independent DB).
