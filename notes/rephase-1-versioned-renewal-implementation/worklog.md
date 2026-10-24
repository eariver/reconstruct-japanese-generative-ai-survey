# Versioned renewal implementation — worklog (M1 partial milestone)

2026-10-24. Lead IMPLEMENTATION/TEST Co-Worker, Human continued after commit c5b0d7c
(main...origin/main CLEAN at start per root observation).

## Inputs verified (read-only, no restore/network/old runners)

- Proof input unchanged: `.rephase-1-editorial-runtime/final-source-packaging/proof-copy/candidate-partial-b40de60`
  HEAD 409b292756dd1277b9dfae87679934c0d2ce251c, `git status` shows intended57 M (not modified by this unit).
- Selected contract SHA478f00510791b76af24aa7d61f398f0608f7ad8ae7808008c660f2bea6fbfdcf verified.
- Root gate SHA7d7d5a4552eb7a1abcbafa79d8f358ff10ec96e885b55f09f271766b136cab57 verified.
- Corrected R3 JSON pin 1f758b0a2e65081838b60b12473b7593522ecf068773bb059315b6a245df581f used; R4 header typo preserved.
- Python 3.14.4, jsonschema 4.23.0, unittest available; pytest/pip absent (used stdlib + unittest).
- No GIT_* env inherited. Isolated DB has no alternates, no hardlink sharing (different inodes, same device), inert origin `https://example.invalid/versioned-renewal-fixture.git`.

## Isolated workspace

- `.rephase-1-editorial-runtime/versioned-renewal-impl-20261023T181352Z/candidate-work/`
- Copied via `rsync -a --exclude=.git --exclude=__pycache__ --exclude=*.pyc` (no blanket untracked/cache/tmp).
- `git init -b main`, fixture identity `rephase-fixture/fixture@example.invalid`, inert origin, no alternates.
- Commits (meaningful, before authorities, no --allow-empty, no reconstruct commit):
  - 72d6830 milestone 1 code (761 files: base 409+57 plus renewal changes)
  - f360b67 M1 scoped verification test (tests/test_versioned_renewal_m1.py)
  - a8890d4 remove tracked pycache (residue, not source)
- Current isolated HEAD a8890d4ff612563e71b7dcf5db76287acfe4ea35. `git status` clean after M1 (pycache removed).

## Map implemented (faithful to contract §11 + root §§2-4, R3+R4/R5/R6 as overridden)

- 4 new schemas (strict, additionalProperties false, whole-doc "" allowed, no "/" substitution):
  schemas/versioned-renewal-basis-v2, -source-proof-v2, -source-manifest-v2 (+$defs/buildRecord REUSED/EXECUTED), -publication-set-v2.
  `observedSourceBinding.schema_pointer` is `{"type":"string"}` (allows ""), exact registry enforced.
- 5 existing amended (branches only, legacy verbatim):
  reader-manuscript-v2 (+renewal_source XOR editorial_source), publication-candidate-v2 (+optional proof ref),
  quality-regression-bundle-v2 (+optional proof ref), reader-surface-gate-v2 (+5th VERSIONED_RENEWAL_V1),
  publication-surface-revalidation (+3rd VERSIONED_RENEWAL_ACTIVATION_V1/REVIEWED_VERSIONED_CORE_RENEWAL, supersedes+before_candidate nonnull).
- 3 new modules (fixed names, DAG preserved, no forbidden calls in code):
  survey_versioned_renewal_history_v2 (HIST leaf, no agent/Reader/Gate/Candidate/seal/receipt/P1/P2R/P3S),
  survey_versioned_renewal_source_v2 (Layer-A/B, no State validation/seal/P1/P2V, function-local imports, retained-only),
  survey_versioned_renewal_v2 (HIGH, prepares/finalize/receipt/set/activate/resume/history/CLI, preserves public agent.validate_agent_state on LIVE bytes + canonical path + prePreview/Exception window, no verify_state_basis, no Path(".") repair).
- Consumers/closures:
  publication_set (_is_versioned_record, validate_activation_record renewal branch, anchor/versioned chain, mode probe),
  reader_publication (renewal_source branch + renewal_source_proof_ref keyword threading, U no serialized change / C serialized),
  publication candidate (proof threading + digest base 10→11), quality bundle (9→10), gate derivation (VERSIONED_RENEWAL_V1, no inferred receipt),
  staged _SHARED 30→35/14→22 len 50→63, weekly CURRENT_CLOSURE 22→29, longform 27→34, editorial closure 50→63,
  config pipeline 67→71 (4 new schemas only, no .py), test_group_c updated 30/14→35/22.
- Rejected R6 ban NOT implemented: HIGH calls public validate_agent_state (root §2). No substitution by Profile-only/_profile_and_source alone or production.verify_state_basis. Whole-doc pointer "" preserved. No Screening fix.

## Scoped verification (new procedures only, no saved historical runners)

- tests/test_versioned_renewal_m1.py (unittest, 7 tests): new schemas parse + pointer empty allowed, 5 amended branches, closure 63/66 union, pipeline 71, HIGH LIVE validation preserved + no verify_state_basis/Path fix, Layer no-forbidden imports (AST), stale-refusal signature.
  Result: 7/7 OK (0.275s) in isolated workspace. Raw: `python3 -m unittest tests.test_versioned_renewal_m1 -v`.
- P3S closure gate: `_route_code_deps` WEEKLY 63, LONGFORM 63, union 66, new files present. `test_p3s50_and_recipe_binding` PASS after update (35/22).
- Proof-copy input unchanged (M list identical pre/post). No fixture objects in reconstruct DB. No network.

## NOT done (required successor scope, explicit)

- Real R3-format bootstrap under older tool source, Weekly+Longform U and C with genuine changed-tool epochs in isolated synthetic fixtures, repeat including C→U→U, renewal→editorial, normal direct Candidate/Preview/Freeze/Release with real PDF where C, explicit failure/resume and affected regressions (original routes/R1/DM004) with full oracle coverage (P-U1/U2, P-C1/C2, P-S1, P-N1/N2/N3, N-H1..H15, Freeze nested/alias, IO/close/fsync/replace/postread/foreign-inode, 32/33/cycle/anchor, ALREADY_ACTIVE readonly).
- Full accepted-authority predicate extraction equivalence oracles per family, per-file SHA pinning, tripwire grep table delivery as runtime evidence, freeze snapshot file enumeration, build-record variant end-to-end with real disposable build/transfer.
- Independent final implementation review. No independent PASS or adoption claimed. Production semantic NO-GO preserved. Synthetic reviews/fixtures are not genuine approvals.

## Next after root continuation

- General continues in same isolated workspace (HEAD a8890d4): build synthetic fixture State/graphs with genuine changed Core commits, implement proof/source/closure completions (current contract pinning, trio render equality, REUSED/EXECUTED build paths, receipt-after-build, fresh QA/Gate/Candidate/seal, activation/resume), then full oracle matrix + regressions + evidence. Return exact files/raw evidence/next tasks. Do NOT label helper-only complete.
- If source/map contradiction changes authority semantics, return exact file/predicate to Astra before broadening; no stubs/fail-open/unproved PASS.

Stop at partial milestone; root will continue. No ordinary candidate/reconstruct commit/push.
