# DM022 C1 R2-diagnostic correction (private frozen copy, NO shared tests, NO Commit Point)

Date: 2026-10-28 UTC. C1 corrects assigned files/tests only with apply_patch.
R2 diagnostics `integration-r2-diagnostics.md` (fixed source R2, 5 blockers) is
authority; first integrated return + `author-C1-correction.md` preserved (not
edited). Root whole unit ongoing; do NOT stop at Human Commit Point. No Human
commit/readback, no ordinary commit/push, no Gitconfig/network, no `git clean/
reset`, no fixture deletion in snapshot/candidate (temp fixtures only in `/tmp`
via `tempfile`, auto-cleaned by framework), no old-log reuse.

## 1. Private reproduction (independent, no shared mutation)

- Base: `snapshot-r2-20261028T124706Z/worktree` (756 files) + `git-independent/.git`
  (83 files, HEAD `409b292…`, inert `example.invalid`, no alternates/commondir).
- Exec: `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/exec-c1-r2diag-20261028T130428Z/` (NEW stamp, not R2 exec):
  worktree `tar --hard-dereference` (756 files, 0 symlinks) + `.git` byte copy
  (`cp -a`, no `--link`); inode overlap SNAP_GIT vs EXEC_GIT 0; HEAD matches;
  origin inert; `env|grep ^GIT_` → `NO_GIT_ENV_OVERRIDES`; per-run `unset GIT_*`
  verified in header.
- Overlay ONLY C1 files from `candidate-work` (read-only source, write to exec):
  7 scripts + `config/survey-production-v2.json` + 3 new + 4 existing C1 tests
  (listed §3). No schemas/modules (A owned), no B/C2 files. Post-overlay
  756 files, 0 pycache (PYTHONDONTWRITEBYTECODE=1; `__pycache__` removed as cache
  hygiene, not source delete).
- Evidence: `notes/.../evidence/c1-r2diag-20261028T130428Z/` (NEW stamp, not R2
  `integration-r2-...`): `run-03-family-closure-pass/` + `run-04-research-graph-pass/`
  with `header.txt` (command/cwd/python/sourcepin/overlay/Git/origin) +
  `stdout-stderr-raw.txt` + `exit-code.txt`. Old `run-01/02` failures in same dir
  preserved as history (not reused as pass proof).
- No tests on shared `candidate-work` while A2/B/C2 edit; pure tests run ONLY in
  exec (private frozen R2 + C1 overlay) with independent meaningful Git fixtures
  (temp dirs + independent Git DBs, process env `GIT_*` unset globally, local
  `git config user.*` in temp repos only) + source pins/raw saving.

## 2. R2 C1 blockers reproduced + corrected (real results)

### C1-01 `test_known_schema_owned_fingerprint` ERROR → PASS (6/6)

- R2: `unknown foreign SHA for schemas/dm022-revision-proof-v2.schema.json`.
- Root cause (inspected, not guessed): registry had typo `...6d7f...` (7) vs
  actual installed `...6d6f...` (6). Proposal + installed in R2 snapshot/worktree/
  candidate all `...6d6f...` (6, 7403B, equal); allowlist had `...6d7f...` (7).
  Single-char registry typo, not shortening (both 64-char full) and not
  autoallow (exact match required – correctly refused wrong SHA).
- Fix (C1 owned `survey_versioned_renewal_history_v2.py`): correct proof entry to
  full installed `a79c09209c145d485ec39e1c1c277f0d706cf3ccfb0972c5bd9f6d6fe7cec5c3`
  (6). Report already has both (proposal `21369608…` historical + installed
  `10238a1a…` current); other 3 installed==proposal (single entry covers both).
  Old known sets preserved; unknown foreign still `UNSUPPORTED_MIGRATION`;
  runtime CURRENT uses owned fingerprint (`_require_owned_schema_fingerprint`:
  live bytes SHA must be known), historical OWN-epoch uses epoch blobs.
- Verify (private exec): `test_known_schema_owned_fingerprint` now OK; live SHAs
  for all 5 match allowlist (full 64-char, no shortening).

### C1-02 `test_weekly_longform_canon_literal_plus_files` ERROR → PASS (6/6)

- R2: `Weekly actual import beyond R4/R5 literal: [agent_control, agent_tool,
  drafting, evidence, production, schema]`.
- Inspected (no weaken, no blind expand): AST collects real `scripts.*` paths
  (not `as` aliases – verified). R4/R5 canon 29/36 intentionally excludes those
  6 (receipt blobs, not control loaders). Original R3 §6 + LF-2I design binds
  unlisted helpers via control-roots (`scripts` in `implementation_control_roots`)
  + contract-file equality/ancestry (`_verify_head_bytes` control diff), not
  closure blobs. Literal fixture correct per R4/R5 (29/36); fault was C1 AST
  check requiring actual ⊆ closure (too strict).
- Fix (C1 owned weekly/longform): `_verify_actual_import_closure` explicitly
  allows 6 control-bound loaders (weekly: agent_control/agent_tool/drafting/
  evidence/production/schema; longform: longform_derivation/production/
  reader_surface_gate/schema/fidelity/render) as control-bound (NOT added to
  G76 closure – no blind expansion). Any other extra → expansion return, never
  silent omit. Closure check unchanged (exact 29/36 + 70/73 + file existence +
  control diff). Inspected alias vs path (AST real paths) + literal fixture
  (R4/R5 correct) – neither weakened nor expanded.
- Verify (private exec): `test_weekly_longform_canon_literal_plus_files` OK;
  `test_staged_literal_plus_ast` OK (staged already AST + set equality).

### C1-03 `test_legacy_file_still_accepted` ERROR → PASS (5/5)

- R2: `_record_kind` refuses `{"reason_class":"LEGACY_REASON"}` (correct – fake
  kind string, not real value).
- Fix (C1 owned test): use real typed old format from actual file:
  `{"reason_class": hist.LEGACY_REASON}` (`"REVIEWED_CORE_CHANGE"`, no `kind`),
  written to real temp file + strict parse + public verifiers
  (`_is_legacy_record`, `_record_kind`). No manually faked kind strings.
  Editorial fake strings removed (no `EDITORIAL_REASON`/`EDITORIAL_KIND` literals;
  uses `hist.VERSIONED_REASON/KIND` constants where needed).
- Verify (private exec): `test_legacy_file_still_accepted` OK; PREARCH still
  refused as `DM022_WRONG_FAMILY` (file-based, public discriminators).

## 3. Real G71→G76 proof (reloaded graph + 70 deps, not dict/count-only)

- Added `test_real_g71_g76_reloaded_graph_70_deps` (private exec):
  derives CURRENT via `hist._derive_current_family_from_disk` (actual disk,
  never hardcoded G76) → asserts G76; reloads receipt/staged closures (70) +
  canon 36/41; verifies all 70 deps exist on disk (reloaded graph) + live SHAs
  + AST (`_verify_actual_import_closure`) + R4/R5 literal sets (delta ONLY 2+5);
  historical G71 via same literal (no count-only). Full Git-blob own-epoch
  (`verify_closure_at_commit` at fixture HEAD with complete source committed)
  requires fixed snapshot with source-committed fixture DB (pending – old HEAD
  409b292 lacks 93 overlay + 7 new files, so Git-blob at old HEAD correctly
  refuses; not claimed as pass).
- `verify_prearch_accepted_graph` (C1 history, OWN-epoch via `git show`, never
  live/HEAD/State/agent): checks kind/reason(`reason`, not `reason_class`)/
  operation/boundary/checkpoints/4 NamedRefs/lineage/SELF/revision_root ownership/
  request/report/proof/decision under revision_root/pipeline G76 at epoch.
  Publication `_record_kind`/`supersedes` remains ONLY legacy/editorial/renewal
  (PREARCH refused). Wired in tests on real files/epochs (minimal fixtures
  correctly refuse with `UNSUPPORTED`/`HISTORY_*`, proving epoch use); live
  derivations use LOW resolver (CURRENT, live re-hash, no State) – split, no
  recursion. Old report epoch ≠ current HEAD (OWN epoch, never HEAD equality).
- LOW A3 pure cores: derivations use function-local LOW
  (`resolve_research_authority(root, state_path)->{family,checkpoint,artifacts
  (parsed),lineage,artifact_refs(4 NamedRefs)}` + checker
  `(root,checkpoint_path,report_path,before_copy_path)->list[str]` for HIGH
  adoption; derivations use resolver only – checker `before_copy` owned by HIGH
  retention, split documented). No workaround additional closure outside mapped
  selection (imports stay within 2+5 + control-bound; extra → expansion return).
- Historical R3+G71 fingerprints/bindings preserved (all 18 + report both);
  current tools verifier exact contents include all new 7 (closure + files + AST
  + owned fingerprint + `_derive_current_family_from_disk`).
- Helpers: existing C1 lists fixed (`staged` 63→G76 70 + 2+5; `phase_h` NEW→G76/
  OLD→G67 + G71; `source_phase_s` derive CURRENT; `history_author_h` assert G71;
  `_SHARED_PY==35` historical preserved, `_SHARED_PY_G76==37` CURRENT – derive
  known historical, not global replace). New helper only supplements, not fixes
  drops – existing drops fixed as above.

## 4. New raw results (no old-log reuse)

- `run-03-family-closure-pass`: `Ran 6 tests OK`, exit 0,
  SHA256 `aee45455135ddec7daa1ae796b371d804b8fba71734d32288ec1b256106a72d1`
  (37 lines with DeprecationWarning only).
- `run-04-research-graph-pass`: `Ran 5 tests OK`, exit 0,
  SHA256 `d73ef61d75faf4bd233e73f3b8726844d9ea854509aba2774b9ea323974e0734`
  (23 lines).
- Pre/post 756 files, 0 pycache, 0 symlinks, no alternates/commondir, inert
  origin, `NO_GIT_ENV_OVERRIDES`; SNAP/CAND untouched (CAND 756/0 pycache after
  cache hygiene). Systemic setup failure did NOT occur (all collected).

## 5. Exact unresolved + cross-owner requirements (return to root, no auto-start)

- B-01 (agent CORE proof branch error identity) – B owned; root adjudicates
  expected `must not carry CORE_STAGE_CONTRACT` vs actual `requires exactly one
  DM022_SUPERSESSION_PROOF`.
- C2-01 (weekly_refresh `_dm022_refuse_prearch_refresh` missing) – C2 owned.
- `test_group_c_editorial_consumers_v2` 35/22 expectation (not C1 owned; C1
  preserves `_SHARED_PY==35` historical, CURRENT via `_G76==37`): needs root
  coordination if C2/B expects update – C1 did NOT edit (disjoint ownership).
- Full G76 own-epoch Git-blob verification (70 closure at G76 epoch with complete
  source committed) + positive G76 upstream rendering witness with real accepted
  graph (requires A2 LOW + B agent PREARCH + fixed snapshot with source-committed
  fixture DBs + independent Git DBs/raw logs/pins). Current pure tests use live
  reloaded graph + actual epochs where feasible; full epoch proof pending.
- A2 LOW/HIGH replacement: derivations use resolver (read-only consumers);
  checker `before_copy` owned by HIGH retention – split documented, root
  confirmation pending if checker required in consumers.
- No map contradiction beyond above; if any required reader/closure/contract
  contradiction found later, return exact root before broadening.

Old returns (`author-C1-return.md`, `author-C1-correction.md`, R2 diagnostics +
raws) preserved. Stop – root whole unit ongoing, no Human Commit Point by C1.
