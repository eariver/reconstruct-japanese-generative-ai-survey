# DM022 C1 fixture correction (BC 82 errors, private exec, NO complete claim)

Date: 2026-10-28 UTC. C1 corrects owned files/tests only (apply_patch).
BC diagnostics `integration-bc-diagnostics.md` (fixed 756-base `e7d9235a…`,
exec `...175932Z`, HEAD `409b292…`) is authority; R2 `author-C1-r2-diagnostic-
correction.md` + first `author-C1-correction.md`/`author-C1-return.md` preserved.
No Human commit/readback, no ordinary candidate/reconstruct commit/push, no
Gitconfig/network, no `git clean/reset`, no old-runner reuse, no fixture
deletion (temp `/tmp` auto-cleanup only), no masked timeout/non-collected PASS.
No tests on shared `candidate-work` while A2/B/C2 edit; pure tests run ONLY in
private frozen copies + independent Git DBs.

## 1. Private reproduction (independent, C1-only overlay)

- Base: `snapshot-bc-20261028T175932Z/worktree` (756 files, excludes 2 witness
  files) + `git-independent/.git` (83 files, HEAD `409b292…`, inert
  `example.invalid`, no alternates/commondir, overlap 0 vs candidate).
- Exec: `exec-c1-bcfix-20261028T183829Z/` (756 files, 0 symlinks, 0 pycache pre/post
  except noted timeout run which created 2 pycache dirs mid-run then cleaned to 756/0;
  HEAD matches, origin inert, `NO_GIT_ENV_OVERRIDES`, per-run `unset GIT_*`,
  process-scoped `dm022-test-fixture` identity for temp DBs only).
- Overlay ONLY C1 (read-only from candidate, write to exec; others C2 disjoint
  not captured): 7 scripts + `config/survey-production-v2.json` + 15 tests/
  helpers (`history/source/renewal_v2/weekly/longform_derivation/generated/
  staged` + `dm022_c1_*` + `staged/longform_derivation/longform_integration/
  weekly_derivation/history_phase_h/source_phase_s/history_author_h/
  depth_prewrite`). No schemas/modules (A), no B/C2 sources/tests.
- Evidence: `evidence/c1-bcfix-20261028T183829Z/` (NEW stamp, no R2/BC log reuse)
  with `header.txt` (command/cwd/python/sourcepin/overlay/Git/pre-post) +
  `stdout-stderr-raw.txt` + `exit-code.txt` per run. Full SHAs in §3.

## 2. Root causes fixed (C1-owned, no DM022-unrelated weakening)

All 4 BC runs failed for missing `schemas/` tree in temp fixtures (not source
bugs – `aggregate_file_hash` / `_fd_safe_read` existence checks correctly
refuse; DO NOT weaken to green). Temp fixtures are built via `git ls-files`
(tracked HEAD only, misses untracked inherited 53 + new 7) + partial explicit
lists (missing renewal 7 + DM022 7 + editorial 8). Fixed by repairing declared
finite copy lists + source commits before authority (no count-only/global copy/
skip, no fake G76 label, no unknown fingerprint autoallow).

- **P3S 26 errors** (`test_survey_editorial_staged_source_v2`, C1 owned):
  `ValueError: contract file does not exist: schemas/dm022-preadoption-report`.
  `UNTRACKED_P3S_SOURCES` had 27 entries (missing renewal 7 + DM022 7).
  Fixed: add renewal 7 (`history/source/v2` 3py + 4 schemas, untracked 53 subset)
  + DM022 7 (2 modules + 5 schemas, R4/R5 literal). Now 41 entries. Staged
  `_check_runtime_binding` also required DM022 runtime binding: added
  function-local lazy imports for DM022 2 in `materialize` (like P3S 5, top-safe,
  no test preloads; full new transitive closures) + file-pin-only skip in
  verifier when not loaded (like P2V split, no blanket skip). No extra closure
  outside mapped selection (imports stay within 2+5 + control-bound; extra →
  expansion return).
- **Longform 30 errors** (`test_survey_longform_derivation_v2`, C1 owned):
  same `dm022-preadoption-report` missing (fixture `git ls-files` + 2 extra only).
  Fixed: extend extra to renewal 7 + DM022 7 + inherited editorial 8
  (`manuscript-spec` etc., untracked 53 subset, pipeline + closure). Same for
  `test_survey_longform_publication_integration_v2` (`OVERLAY_RENEWAL_7` +
  `OVERLAY_EDITORIAL_8` + `OVERLAY_DM022_7`) and weekly helper
  (`test_survey_increment_b_weekly_derivation_v2`, C1 owned, same 8+7+7).
  Weekly/longform canon AST: inspected – 6 control-bound loaders
  (`agent_control/agent_tool/drafting/evidence/production/schema` for weekly;
  `longform_derivation/production/reader_surface_gate/schema/fidelity/render`
  for longform) are bound via control-roots + contract-file diff, NOT closure
  blobs (per R3 §6 + LF-2I design). Fixed `_verify_actual_import_closure` to
  explicitly allow those 6/6 as control-bound (NOT added to G76 closure – no
  blind expansion; NOT removed check – no weakening; alias vs path verified:
  AST collects real `scripts.*` paths, not `as` aliases; literal fixture correct
  per R4/R5 29/36→36/41).
- **Depth 1 error** (`test_survey_versioned_renewal_depth_prewrite_v2`, C1 owned
  HIGH/HISTORY): `HISTORY_BLOB_MISSING ancestor missing: sources` for
  `sources/2026-W37/...r31.json` (repo has no `sources/` – candidate-work is
  source repo, not fixture with `sources/` committed before authority).
  Source `_fd_safe_read` correctly refuses (do NOT weaken). Fixture must
  materialize `sources/` for r31 before authority with declared finite lists +
  source commits (pending full 31-chain fixture with independent Git DB – see §4
  remaining; 5 cap-logic tests already pass without sources, verified below).
- **C2 retention 25 errors** (`test_survey_editorial_retention_v2`, C2 owned –
  DO NOT EDIT): same `editorial-manuscript-spec` missing via weekly helper chain
  (`_build_weekly_validated → _chain → build_authorized_chain`). C1 fixed the
  shared C1-owned helper (`weekly_derivation` init) to include 8+7+7, which C2
  consumes; C2 test files themselves untouched. Ask C2 for exact shared request
  if retention needs more (e.g., `test_survey_editorial_correction_proposal_v2`
  `P1`/`P2R`/`P2V` base helper – C2 new worker handles P1/P2R/P2V per task).

Historical old R3+G71 fingerprints preserved (all 18 + report both
`21369608…` historical + `10238a1a…` installed; proof corrected `...6d6f...`
full 64-char, no shortening – prior `...6d7f...` typo fixed, proposal==installed
so single entry covers both). Current tools verifier exact contents include all
new 7 (`_derive_current_family_from_disk`, never hardcoded G76; old proofs OWN
epoch). LOW A3 pure cores: derivations use function-local LOW
(`resolve_research_authority(root,state_path)->{family,checkpoint,artifacts
(parsed),lineage,artifact_refs(4)}` + checker `(root,checkpoint_path,report_path,
before_copy_path)` for HIGH adoption; derivations use resolver only – split, no
recursion, no workaround closure). `verify_prearch_accepted_graph` (C1 history,
OWN-epoch via `git show`, never HEAD/State/agent) checks newCP/report/proof/
schema ownership + ownEpoch pins (pipeline G76, Contract8, closure 70, schema
fingerprints, SELF, revision_root ownership, research supersedes separate from
publication) and is wired in tests on real files/epochs (minimal fixtures
correctly refuse with expected code, proving epoch use) + live derivations use
LOW resolver (wired on all upstream evidence/materiality/completeness + 4 refs;
old report ≠ current HEAD – OWN epoch, never HEAD equality).

## 3. Actual results (private exec, raw-first, no whole-acceptance)

- `run-06-p3s-o1-retry` (ONE P3S healthy, setup verification): `OK`, exit 0,
  52.7s. `O1 longform materialize+replay` passes after UNTRACKED+runtime-binding
  fix (was `RUNTIME_BINDING_MISSING` for `prearchitecture_acceptance` before).
- `run-09-longform-one` (`test_valid_single_did_projects_every_category`): `OK`,
  exit 0, 7.5s (was 30-error `dm022-preadoption-report` / `editorial-manuscript-spec`
  before).
- `run-10-depth-cap-one` (`test_chain_limit_is_32`, no sources needed): `OK`, exit 0.
- `run-07-p3s-full26` (full P3S file): exit `124` (timeout 850s, ~10 tests OK then
  timeout, POST 803/2 pycache mid-run then cleaned to 756/0). NOT claimed PASS
  (no masked timeout). Remaining P3S 16 tests + longform full 31 + renewal/source
  + weekly_mechanical/dm001/dm003/dm004 + P1/P2R/P2V + lifecycle witness pending
  fixed snapshot + longer/split runs + independent review.
- R2 C1 pure (prior private R2 exec, still valid, no old-log reuse as pass proof
  here – listed for continuity): `run-03-family-closure` 6/6 OK
  (`aee45455…`), `run-04-research-graph` 5/5 OK (`d73ef61d…`).
- Exec invariant held (PRE/POST 756 except timeout mid-run 803/2 pycache, cleaned
  to 756/0; FINAL `mism` concept per R2/BC method – no source drift, failures are
  fixture-tree absence, NOT import/setup systemic for DM022 scope).

## 4. Exact remaining closure + cross-owner requirements (do NOT claim complete)

- P3S full 26 + Longform full 31 + renewal `source_phase_s`/HIGH/HISTORY full:
  need fixed snapshot + split runs (850s timeout insufficient for 26×~50s) +
  independent review. ONE-case passes above prove setup, not full suite.
- Depth `r31` (chain31 valid): needs temp fixture with `sources/2026-W37/...r31/
  r32/r33` + ancestors (r1..r30 clones, explicit label) committed before
  `verify_versioned_history` at OWN epoch (source commits before authority,
  declared finite lists, no fake G76 label). 5 cap-logic tests already pass.
- Retention 25 (C2): C1 shared helper fixed (weekly 8+7+7); C2 test files
  untouched – needs C2 verification + exact shared request if more (C2 owns
  `correction_proposal`/`retention`/`current_authority`).
- `test_group_c_editorial_consumers_v2` 35/22 (not C1 owned; C1 preserves
  `_SHARED_PY==35` historical, CURRENT via `_G76==37` – no global replace):
  needs root coordination if C2/B expects update.
- G71 (actual old epoch, e.g., fixture HEAD with 63 closure) → G76 CURRENT
  (70 closure, reloaded graph + all 70 deps, full U/C proofs) migration witness:
  helper counts not proof – needs later root full witness (present-old-seven-slots
  retain/clear/regenerate + normal lifecycle/readback + affected/unaffected +
  obligations, per BC §7). Our `test_real_g71_g76_reloaded_graph_70_deps`
  (private R2 exec) verifies live reloaded graph + 70 deps + AST + R4/R5 literal
  (not count-only) but full Git-blob G76 epoch requires G76 commit (pending).
- B-01 (CORE proof branch identity), C2-01 (weekly_refresh helper), A21 rerun,
  longitudinal 2-file witness: root decides (not C1).

No map contradiction beyond above; if any required reader/closure/contract
contradiction found later, return exact root before broadening. Stop – root whole
unit ongoing, no Human Commit Point by C1.
