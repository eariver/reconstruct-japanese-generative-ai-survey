# Supplement-carry initial implementation (first return, no packaging/CURRENT proof yet)

Workcopy: `.rephase-1-editorial-runtime/supplement-carry-implementation-20261106T131722Z/candidate-work`
Base: isolated epoch `5eef790bd8d492c557cc4db9c29425e3e410d47d` / tree `a851584ffbb59222e105583ec2af8fba20a87692`, 771 files verified ok vs final139 manifest (patch `de0af9cbd5`, manifest `c5a6b230`, test7b `7b862305`), extras 0, no alternates, inert origin `https://invalid.invalid/inert.git`, process-scoped identity, no HOME/gitconfig change, no empty commits. Saved e84/proof untouched; 139 patch NOT re-applied (already-applied source copied, .git excluded then new independent DB).

Changed (intended, uncommitted diff preserved):
- `scripts/survey_research_authority_v2.py` base-staged `e6c56ba3978f8323ab54b55e3986393f0ae9a077` -> worktree `30ac6432fc0c5423f7d406ba6167e2006614d606014e76e5b980a8454f6f7aca`
- `scripts/survey_prearchitecture_acceptance_v2.py` base-staged `37f22ab4c94ec5a75ea8f842ca8bb5efc5a82357` -> worktree `69032c5b16cda28f090ad8c386479f8a950f1a4ab392d68f85da720d2c267651`
- `tests/test_dm022_supplement_carry_v2.py` NEW (untracked) worktree `abf1c9e0c82e5657b423da4c74371de3812bbc2928148b19224e1b4362ea2db2`

Diff: `implementation-20261106T131722Z/initial-implementation.diff` (22357B, `git diff -- scripts/...` from workcopy, no `git -C .`, no reconstruct status/HEAD/log/readback).
Scope: LOW `_bind_selected_supplement_for_revision` (new narrow private helper, existing LOW module only) + package carry (OLD prompt/non-supplement contracts verbatim, supplement contract/rule from stable bytes, deterministic task/meta IDs, exact non-DROP/affected + OLD/NEW matrix + supplement recheck no reseal) + prove cross-check (request<->package + manifest==request per r2-review §2.8, null enforces no authority) + HIGH prepare seams (SizedRef verify before writes, package==request recheck, manifest==request recheck). No new schema/module/cache/verified-dict/CLI flags; signatures unchanged; Contract8 unchanged (scripts absent from identity); tool SHAs will change (2 modules).

Tests (PYTHONDONTWRITEBYTECODE=1, real HIGH both routes, isolated fixture DBs, meaningful commits only in fixtures):
- argv: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_dm022_supplement_carry_v2 -v`
- workdir: workcopy above; env: PYTHONDONTWRITEBYTECODE=1, process-scoped fixture Git identity (no gitconfig/HOME change)
- exit: 0; raw: `implementation-20261106T131722Z/focused-test-raw.txt` (1325B)
- 4 tests OK (11.225s): WEEKLY DERIVED novel+unchanged (3 tasks: affected supp + unaffected supp + Discovery-only, R!=E, adopt/readback/resume, repeat anchor), THEMATIC direct novel+unchanged (same 3-task pattern), red control null+bindings refuses at actual card build (`source_bindings must explicitly select...`, not token), decoy/OLD+null + unknown-DID refuses.
- Initial failed fixture runs preserved in tool history (X target-source hardcode, implementation_sha HEAD mismatch, non_drop dict-vs-string bug fixed, overwrite refusal, completeness O-ROOT-1 missing) — fixed with minimal fixture corrections, no extra implementation changes beyond the non_drop predicate fix above.

Scope/unresolved (for root review before next verification):
- Focused batch only; no whole old suites, no CURRENT proof (`verify_renewal_source_proof` not run), no packaging/DIRECT diff, no real W34/SP 409/160 correction (needs separate independent semantic review, not test count).
- Replaced-supplement version (SP 27+3) not yet exercised; novel+unchanged covered for both routes. Late/readback oracles (807/888/950/1124/1327/1603/1662), retention/guard/resume failure seams beyond ALREADY_ACTIVE, and full affected/unaffected ledger `rows_checked` coverage beyond byte-identical cards remain for next verification.
- No contract contradiction found; mechanical projections unchanged (actual proof exclusions control); no source silencing (unaffected facts/source_bindings preserved).
- Code remains uncommitted in workcopy; no ordinary candidate/reconstruct commit/push.
