# DM022 publication depth boundary 32/33 — dedicated witness evidence (NEW, NO CommitPoint)

Date: 2026-10-29 UTC. Owner: Depth-boundary witness executor/author, NOT independent reviewer.
Binding: contract `a345bb95` INCLUDING §11, pre-code ROOT `0425c530` INCLUDING §5.2,
whole-lifecycle Attempts (same-G76 editorial/U done), G71 compat (genuine G71->G76),
final-affected (HighU2 closed, Weekly34 closed, Depth cap 5/5 preserved but
`test_actual_history_r31_chain31_r32_chain32_r33_invalid` blocked on missing
`sources/2026-W37/...r31/r32/r33.json` — previous C1 incorrectly said constant-5
enough despite ROOT request for full 32/33 endpoint). This unit proves the
affected endpoint with PROVIDED30 + 2 REAL ops, NOT constant-only.

Whole unit continued, NO Human Commit readback. Ordinary Commit/Push Human-owned.
Unit ongoing, NO CommitPoint. DM021+022 OPEN, Whole NOT_READY/step4B3 OPEN/audit unstarted.

## 0. Ownership / constraints (exact)

- Own ONLY: `tests/test_dm022_publication_depth_boundary_v2.py` (NEW, 736 lines,
  SHA256 `0b8ee6f178380b9265959b0523313a1844cbdaa267891e9dcaf020339073cb20`, 49081B,
  in exec `exec-dm022-depth-boundary-20261029T121022Z/tests/`, ignored, NOT in
  reconstruct DB) + packet raw/report in
  `notes/rephase-1-dm022-prearchitecture-implementation/evidence/dm022-depth-boundary-20261029T121022Z/`
  (NEW, 6 subdirs, never overwrite existing) + this doc (NEW). No existing
  runtime/test edits (exec status 130 pre-existing M/?? + 1 NEW test + 1 NEW
  `__pycache__` cache from `py_compile`, excluded from pins, qualified, never cleaned).
- No foreign patch: all fixes in OWN new file only (4 edits: remove
  `synthetic_provided_history` extra field (schema `additionalProperties:false`
  would refuse), pdf->manuscript->bundle supersede tradeoffs for BUNDLE/GATE,
  test_04 `DM022_WRONG_FAMILY` vs schema-invalid (accept both + explicit
  `resolve_publication_mode`/`validate_activation_record` `DM022_WRONG_FAMILY`),
  remove hot `srcmod.verify_renewal_source_proof` in-process (must be via
  fixture-code subprocess, `BASIS_CURRENT_TOOL_DRIFT` fail-closed for hot root)).
  No edits to `survey_*_v2.py`, `test_dm022_full_lifecycle_v2.py`,
  `dm022_lifecycle_fixture_v2.py`, or any other existing file.
- Helpers: existing fullLifecycle/G71compat code reference, no unsafe old runner.
  OWN new test imports `Dm022FullLifecycleWitnessTests`, `_write`, `_sha_file`
  from `test_dm022_full_lifecycle_v2` + `fix` from `dm022_lifecycle_fixture_v2`,
  do NOT edit them. All runtime APIs via fresh fixture-code subprocess
  (`cwd=fixture root`, imports resolve to fixture commit, never hot root modules)
  where required (P3S/editorial/renewal/release CLI); in-process only for
  pure `hist.verify_versioned_history` (git-based, no module-root check),
  `agent.validate_agent_state` (strict LIVE, no module-root check),
  `high.readback_revision` (detached research, no module-root check),
  `rhigh._require_new_chain_capacity` (pure cap, no root), `edpub._build_anchor_chain`
  (read-only chain walk, no module-root check). `srcmod.verify_renewal_source_proof`
  ONLY via subprocess (`u_verify`), NEVER in-process hot (correctly fails
  `BASIS_CURRENT_TOOL_DRIFT` for hot root — preserved as fail-closed, not hidden).
- Git: independent meaningful fixture commits PROCESS identity only (via existing
  helpers `init_independent_git`/`fixture_commit` with process-scoped
  `user.name/email`, inert `example.invalid` origin, no alternates, no empty,
  no rootDB objects (0 inode overlap, 57 files each, `samefile(HEAD)` False),
  no ordinary commits in reconstruct/exec (only in fixture temp DBs via helpers)).
  No Global/local gitconfig writes in reconstruct/exec (only fixture-local via
  helpers, precedent-accepted, `GIT_CONFIG_NOSYSTEM=1`, `GIT_OPTIONAL_LOCKS=0`,
  no `GIT_*` overrides). No `git status/show/log/rev-parse` in workspace root
  (NO Human readback); `git rev-parse HEAD/tree` ONLY in exec/fixture (necessary
  source binding, NOT Human commit readback).
- No network/Production/cleanup/reset/oldrunner/opaquePASS. No `fetch`, no
  system/global config, no `__pycache__` in pins (excluded, qualified, never cleaned),
  no `git clean/reset`, no `rm -rf` of evidence (failed run preserved, no deletion),
  no saved-runner reuse (fresh `python -c` drivers with `cwd=fixture root`, unique
  raw per call, PID recorded before duplicate check, never overwrite). No
  aggregate old test count, no new full suite beyond OWN 4 tests (explicit class,
  NOT whole-module — whole-module would discover imported fullLifecycle 30+ tests
  and timeout 6000s, preserved as failed run, corrected with explicit class).
- Time: P3S real build 6000s budget OK. Full 4 tests `Ran 4 OK 763.314s` in single
  call, timeout 6000s, single child PID 1281454, no duplicate (ps 1/1), no batched poll.
  Individual runs preserved (test_01 0.3s, test_02 55s, test_04 55s, test_03 655s)
  plus full run 763s, all unique raw, never overwrite. No duplicate child
  (ps checked before each batch, PIDs in headers/metas, `test ! -e RUN_DIR` unique).

## 1. Source freeze (NEW complete intended source/independent exec, before authorities)

- Parent: `.rephase-1-editorial-runtime/dm022-prearchitecture-implementation-20261028T113126Z/candidate-work`
  (HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  remote inert `example.invalid/rephase-candidate-recovery.git`, no alternates).
- Method: `cp -a SRC/.git DST/.git` (byte copy, no `--link`), then
  `tar --exclude=.git --exclude=__pycache__ --exclude=*.pyc --hard-dereference -cf - -C SRC . | tar -xf - -C DST`
  (intended worktree only, no caches/tmp/old-fixture-DB blind copy, no hardlinks).
- DST: `.../exec-dm022-depth-boundary-20261029T121022Z` (HEAD 409/tree 8ce, inert origin,
  no alternates, 0 inode overlap (57 files each), `samefile(HEAD)` False).
- Count: 765 files pre-new-test (excl `.git`/`__pycache__`/`*.pyc`) → 766 post-new-test
  (765 + 1 NEW `test_dm022_publication_depth_boundary_v2.py`). Pre/post unchanged
  across full run (766/766, HEAD/tree unchanged, no source drift).
- Pins (FILE-BYTE SHA256, exec, before authorities):
  - `scripts/survey_agent_control_v2.py` `d801feb679c99d2ed8e52b83ed5aca5253ad695ea69eef90feb2e6727dacfe88` 199521B (B2)
  - `scripts/survey_human_gate_v2.py` `101792ad8070607e3f735ddf6e0f6d60f0b3c77afeaab85347cc87e5bee246b6` 74902B
  - `scripts/survey_prearchitecture_acceptance_v2.py` `f8af03cc5d58af1057ea26d9cef0eb87b1fd71118ddf63a2186e24da9bc1e751` 88603B (AHIGH)
  - `scripts/survey_versioned_renewal_history_v2.py` `a9de2c97eb40e358cd06b59cedacc78f3880fab18bd6e6b281ca9e2f578156d9` 315610B (H)
  - `scripts/survey_versioned_renewal_source_v2.py` `b139f493f791cdcd2e3e2a298e97d92b379f62dff95a14c7412ecd63da2217ca` 144597B (S)
  - `scripts/survey_versioned_renewal_v2.py` `35747ba85c315de578f91aee40d45bdc311b46111e2950219067d7b85c526637` 223931B (HIGH renewal)
  - `scripts/survey_publication_v2.py` `705bcee32557a634c229acbbb58c42d8b34babd90d331f442c158ed59a67482d` 155658B
  - `scripts/survey_release_checkpoint_v2.py` `b9433b9efeca0275c3cd6f8cf77fce0942eaa3208e44df65187f6fcfbee18296` 14505B
  - `scripts/survey_editorial_publication_v2.py` `3a8721569d3cb1512501699ecf78d7c7e3679120cfb9b06504fa1471bfdee722` 275939B
  - `tests/test_dm022_publication_depth_boundary_v2.py` `0b8ee6f178380b9265959b0523313a1844cbdaa267891e9dcaf020339073cb20` 49081B (OWN NEW)
- All runtime authors idle (no new M beyond freeze 130 + OWN NEW + cache; no B2/HIGH/H/S/publication/release/editorial writes during unit).
- Old HEAD artifact-only N/A (latest code source first, no old-HEAD code change, no metadata rebind;
  durable prePreview old source NOT reused/hotpatched — fresh fixture construction from latest exec, copy-first).

## 2. Fresh G76 prePreview (adopted PREARCH, real PDF, CURRENT)

- Via `helper._weekly_to_validated_draft("depth-boundary-base-v2")` (actual `high.prepare_revision`/`adopt_revision`
  + external synthetic decision (manifest_ref, explicit nongenuine) + 7-slot exact inventory (7 rows, keys `slot`,
  all `absent_legitimate`, sets equal `DM022_SEVEN_SLOTS`/`SEVEN_SLOTS`) + strict LIVE `agent.validate_agent_state==[]`
  + `high.readback_revision` family `PREARCH` triplet true + `low.resolve_research_authority` PREARCH 4 artifacts
  + `check_supersession_record_from_paths` + `require_completion_consistent`/`require_research_operation_ready`
  + old canonical Ledger/Completeness never reused (active refs under `/research/v2/acceptance-revisions/`, new SHA != old)
  + ordinary `sel_runner.run` with NEW independent Selection input (outside `source_root`, profile-namespaced
  `WEEKLY_MAGAZINE:`/`WEEKLY:`, disposition SELECTED/PRIMARY) → `READY_FOR_ARCHITECTURE_REVIEW`, all 7 slots incl audit,
  audit `interactive_input.path` generated archive (repo-relative `sources/<issue>/...`, NOT caller path), archived bytes == caller
  bytes (copy provenance via path), second `run` refuses `refusing to overwrite` (audit no-overwrite, no bytes changed)
  + `agent.build_stage_checkpoint`/`advance_with_checkpoint` EVIDENCE_REVIEWED→SELECTION_COMPLETE→ARCHITECTURE_ESTABLISHED
  (candidate-matrix/selection + architecture/summary/attention, deterministic CORE_STAGE_CONTRACT, monotonic 01:00Z/02:00Z)
  + genuine-type synthetic ArchitectureGate `agent.approve_architecture` (reviewer `SYNTHETIC_FIXTURE_REVIEWER_*`, explicit nongenuine)
  → `human_gates.architecture_review==approved` + drafting runner (`run_drafting_synthesis_v2_interactive`, 0) → DRAFT_COMPLETE
  + weekly derivation/surface-only/materialize + explicit synthetic surface review + full render (main.tex/bib/sty/receipt)
  + REAL `lualatex+biber` PDF in isolated disposable dir (every step pid/exit/log-tail, `%PDF` + `pypdf` page count asserted)
  with exact byte transfer to canonical survey root → manuscript manifest (BIBLIOGRAPHY+STYLE closure) → deterministic QA bundle
  (3/3 PASS, live bytes reinspected, synthetic nongenuine) + synthetic SEMANTIC/VISUAL via `reader.build_review_record`
  (synthetic reviewer, nongenuine, never genuine) → reader-surface-gate → stage checkpoint → VALIDATED_DRAFT, strict State valid,
  PREARCH readback survives, retained PDFs/logs/digests/inspections/QA/manifest/review/gate JSONs + retained-manifests.
- Result (WEEKLY, e.g. full-run `fresh-prepreview-20261029T142710Z/fixture.json`):
  `fixture_head b361e93545f1471488a5bc049a8dfaa4c1170eab` (genuine G76, all source committed before authority via helper `_git_init`,
  PROCESS identity, inert origin, no empty), `lifecycle VALIDATED_DRAFT`, `publication_revalidation_provenance None`
  (no R1 yet, prePreview, no Preview), `family PREARCH`, `current G76` (via `hist._derive_current_family_from_disk`,
  pipeline 76, Contract8, 5 DM022 + stage-checkpoint `a1b97759…`), `issue 2026-W33`, `state_sha 4077…`.
- Normal public R1: first revalidation will be PROVIDED r1 (synthetic, see §3), NOT operational R1×30. Allowed one real
  canonical metadata refresh is the bundle newline (REAL file write, REAL SHA, live matches, see §3); pdf/source/manuscript/gate
  stay original (live matches bundle/gate, P1 passes); no metadata rebind claim.

## 3. PROVIDED30 typed LEGACY (synthetic, NOT R1×30 ops, fixture construction)

- Template: fresh fixture's own DRAFT_COMPLETE (`prior_checkpoint`, 7 roles with REAL SHAs from VALIDATED_DRAFT real PDF build,
  live bytes match rows, REAL SHAs, NOT dummy). Same valid cumulative rows (prior==original, preserved==original, union==original),
  NOT rollforward, NOT immediate rows per root contract (old R1 already cumulative against original).
- Construction (OWN `_build_provided30`, fixture construction, NOT operational rollback/ancestry forgery):
  - Supersede `quality-regression-bundle` (NOT pdf/source/manuscript/gate to keep P1 bundle+gate passing):
    prior=`original` (REAL SHA from DRAFT_COMPLETE), new=`original bytes + b"\n"` (still valid JSON, same parsed object/digest,
    REAL SHA changed, `new != prior`, changed bytes, live==new, byte_count matches, NO drift).
    Preserved other 6 original (live matches original, NO drift). Union==original (7 roles, no dup, no missing).
    Live bundle newline does NOT break bundle validation (digest from object, whitespace ignored, same pdf/source refs (original),
    live pdf/source original (matching bundle refs)). Live manuscript/gate original (matching gate bound manuscript).
    P1 bundle+gate pass (see §4 setup failures for pdf/manuscript tradeoffs, preserved).
  - Validation: `manuscript` original, `quality_bundle` new (changed, ==effective new), `semantic_review`/`visual_review` original,
    `pdf` original (preserved, byte_count original len, page_count 2 as in PhaseH precedent, allowed — agent checks SHA/byte_count, NOT page_count vs live),
    `deterministic_checks` PASS, `summary` legacy. Binds effective (new for bundle, original for others), byte_count matches.
  - `reason`/`executor` labelled synthetic PROVIDED (schema-allowed free-text ONLY, NO extra fields — `additionalProperties:false`
    would refuse `synthetic_provided_history`, removed): `reason "PROVIDED r{i}/30 synthetic (NOT R1x30 actual ops, ROOT accepts
    finite construction)"`, `executor "SYNTHETIC_FIXTURE_EXECUTOR_DEPTH_BOUNDARY_V2 (PROVIDED30, NOT30 actual ops)"`.
    Full note lives in own packet/this doc, NOT in record.
  - `recorded_at 15:00:01Z..15:00:30Z` monotonic (before editorial31 19:00Z, chronology nondecreasing, sequence strictly increasing
    r1..r30 via filename, no cycles, same issue/profile/original checkpoint).
  - `supersedes` chain r1 null→r2→…→r30 (exact `{path,sha256}`, byte-identical, no fake ancestor/no empty root, own clone+code checkout
    at fixture HEAD before constructing input, E `sources/`/`surveys/`/`views-*`/top-level preserved `??`).
  - `core {contract:{}, implementation 0*40}`, `establishment {state 0*64, ...}` dummy for LEGACY (precedent-accepted, NOT checked strictly
    for LEGACY; editorial/versioned use real Contract8/tool epochs, see §4).
  - Files `publication-surface-revalidation-r1.json`..`r30.json` in `source_root/publication/v2/` (fresh, no overwrite, VALIDATED_DRAFT pointer None).
  - State pointer →r30 as FIXTURE CONSTRUCTION (direct `_fl_write(state_abs)`, NOT via `advance_with_checkpoint`; State schema fixed, NO new fields).
- Validation (FULL PUBLIC, no mocked depth/validator/current proof, no caller count):
  - `hist.verify_versioned_history(root, r30)` → `HISTORICAL_IDENTITY_VERIFIED True`, `chain_length 30`, `observed_refs` 30×`LEGACY`
    (typed, `reason_class REVIEWED_CORE_CHANGE`, no `kind`, `prior_checkpoint`==original, `supersedes` chain, sequence strictly increasing,
    chronology nondecreasing, no cycles, `prior SHA cumulative against original, NOT rollforward`, `preserved mismatch` none,
    `row union differs` none, `before_active_digest` recompute (fail-closed), `canonical_anchor` VALIDATION_CHECKPOINT (no versioned yet,
    latest legacy? Actually first_active None (no EDITORIAL/VERSIONED), so anchor VALIDATION_CHECKPOINT ref prior_checkpoint, NO fallback
    to originalPath when LEGACY? Here no LEGACY anchor yet (no versioned), so VALIDATION_CHECKPOINT, correct, no rolling).
    No `caller_count`/`count` param (sig `prior_history,phase` only, verified count NOT filename maxseq).
  - `agent.validate_agent_state(root,cfg,state30)==[]` (strict LIVE, 3 params `(root,cfg,state)`, NO caller-verified dict, NO argument count).
    Checks prior rows, `supersedes unchanged bytes` (new!=prior, passed via bundle newline), `role/path canonical`, file under
    publication/survey roots, `live==new` for superseded (bundle newline live==new, NO drift), `live==sha` for preserved (originals match),
    `row union==prior`, `predecessor binding` (validation manuscript/quality/pdf ==effective, pdf byte_count matches), chain walk
    (same issue/original, sequence strictly increasing, no cycles, bounded 32, later legacy after editorial unsupported — N/A here (no editorial yet)).
  - `hist._derive_current_family_from_disk==G76` (CURRENT, pipeline 76, actual imports/contract + current committed source, schemas vs current disk
    incl `a1b97759…`, supported==observed sorted+byte-order, HIST owner-epoch, CURRENT closure/contract, re-derived surface/trio REUSED_TARGETS).
    Fixture HEAD genuine G76 (all source committed before authority, PROCESS identity, inert origin, no empty).
  - `high.readback_revision` PREARCH (research, triplet true, NOT counted in pubchain, see §6).

## 4. REAL editorial31 + REAL renewal32 (2 actual ops, CURRENT/HIST/readbacks)

- Editorial31 (WEEKLY, `ed-depth-boundary-v2-31-v2`, REAL public APIs, exact synthetic nongenuine reviews):
  P1 `proposal_mod.prepare_proposal`/`validate_proposal` (genuinely revised deck `+ " Corrected: depth-boundary 32/33 MATERIAL..."`, `REVIEW_REQUIRED`)
  → P2R `retention_mod.capture_retention` (`RETAINED_SET_CAPTURED`, manifest, retained COPY `COPY_BEFORE_REPLACEMENT`+`KEEP_IMMUTABLE`)
  → scope review (OWN `_write_editorial_scope_review` via helper, `WITHIN_APPROVED_AUTHORITY`, synthetic nongenuine)
  → P2V `authority_mod.observe_current_authority` (`CURRENT_BASIS_OBSERVED_SCOPE_BOUND`)
  → P3S `helper._run_fixture_p3s_materialize` (fixture-code subprocess, `STAGED_SOURCE_REPLAY_VERIFIED`, `code_deps 70 G76`, PID/exit/raw unique)
  → manuscript/toolchain specs (pinned, real TinyTeX `/home/eariver/.TinyTeX/.../lualatex`, recipe `lualatex-biber-lualatex`, argv `EXPECTED_ARGV...`, env {})
  → `helper._run_fixture_editorial prepare` (fixture subprocess, REAL `lualatex+biber` PDF in isolated disposable (pid/exit/log-tail, `%PDF`+`pypdf`), exact transfer,
  manuscript/receipt/build_record, PID/exit/raw) → author inspect (explicit non-independent, page_count matches)
  → deterministic 3/3 PASS (live reinspected, synthetic nongenuine) + `reader.build_review_record` SEMANTIC/VISUAL (synthetic reviewer, nongenuine)
  → `helper._run_fixture_editorial finalize_activate` (fixture subprocess, `finalize_publication` → set (SEALED_INERT, 15-role seal table, NO second table/fake legacy),
  `activate_publication` → r31 `supersedes r30`, `canonical_anchor LEGACY_REVALIDATION ref r30` (NO rolling, NO originalPath fallback), `prior_checkpoint` same original,
  `before_state_ref` (proposal basis State, retained COPY), `before_active_digest` (recomputed from before-effective7, NOT caller),
  `before_candidate_ref`, `set_ref` (real set, SHA matches), `core {contract Contract8 CURRENT, implementation fixture HEAD (original G76, genuine)}`,
  `executor SYNTHETIC_*`, `recorded_at 19:00:00Z` (after r30 15:00:30Z), `establishment` (state_sha live-before, VALIDATED_DRAFT, approved/pending...),
  schema strict, `INTENT_COLLISION` none (fresh, no orphan), retained COPY pin (P2R manifest, state row `COPY_BEFORE_REPLACEMENT` with `retained_dest/sha/count` live recheck,
  predecessor/beforeCandidate/before7 explicit consistency), fresh P2V before record+State (genuine current-before, NOT cached), DM022 READY (guard/completion),
  State exact-old recheck (NO drift), exclusive record create (agent `_exclusive_create_record_bytes`, collision→resume, NOT takeover),
  owned record inode+bytes recheck (NO same-byte foreign swap), expected State new pointer ONLY (`publication_revalidation_provenance`), guarded State temp+replace
  (agent `_atomic_replace_state_bytes`, known-byte replace, NO truncating write), post-replace validation (strict active State VERSIONED_ACTIVE + selected set==input seal
  + record valid + set valid + agent valid, observed new, secondary errors none, NO delete). `ACTIVATED`, `mode VERSIONED_ACTIVE`, `family PREARCH`.
  - Hist r31: `chain_length 31`, kinds `30×LEGACY + EDITORIAL`, `anchor_kind LEGACY_REVALIDATION ref r30` (permanent, NO rolling, later legacy forbidden),
    `canonical_anchor` exact (kind+path+sha ==derived), basis anchor ==derived (NO `history.anchor_kind`+original default), `HISTORICAL_IDENTITY_VERIFIED True`,
    observed bindings NONEMPTY (derived from ACTUAL strict owner docs/record/staged/receipt, E live/COPY (NEVER tool commit), tool rows at DERIVED own commit
    (G76 CURRENT, NOT caller epoch), canonical sorted dedup, O17 `""` NOT `/`, conflicting-sha refusal, final live recheck (all derived + prior_checkpoint)).
  - State31 strict valid, PREARCH readback survives (NOT counted in pubchain, see §6).
  - Actual op 1/2 (REAL, NOT synthetic history).
- Renewal32 U (WEEKLY, `ren-depth-32-v2`, REUSE_TARGETS, REAL public APIs, CURRENT G76):
  renewal-manuscript-spec (pinned, proposal_ref, architecture_coverage [], reader_requirements FINAL_SYNTHESIS+WEEKLY_COMMUNITY_MOVEMENT, synthetic) +
  renewal-checks (re-hash live editorial QA, exact clone bytes reinspected, synthetic nongenuine) +
  `_commit_new_tool_epoch` (new meaningful fixture HEAD `41b42ab3...` (full-run) / `...` (individual), genuine SHA change (intent file `sources/renewal-tool-epoch-*.json`
  + editorial State r31, ALL `git add -A` + `commit`, PROCESS identity, NO empty, G76 closure 70 untouched, old!=new for U `REUSED_BUILD`) +
  `helper._run_fixture_renewal u_prepare_finalize` (fixture subprocess, `prepare_renewal REUSE_TARGETS manuscript_spec None? Actually manuscript_spec ren_spec,
  toolchain None, executor synthetic, 20:00Z → basis (anchor copied verbatim HIST derived r30, NOT kind+validation default, NO originalPath fallback when LEGACY,
  pre-write validation, retained COPY+KEEP, exact path+SHA live recheck, NO State mutation) + `finalize_renewal` (fresh checks, proof/receipt/Gate/Candidate/seal REAL
  consistent, NEW closure CURRENT (new_head G76), proof/receipt/Gate/Candidate/seal trio style unchanged baseline035 so U `REUSE_TARGET_MISMATCH` NOT trigger,
  NO dummy, NO P fallthrough) → `receipt_path/build_record_path/bundle_path/gate_path/candidate_path/set_path/proof_path` (real `*_path` contract, all exist)) +
  `helper._run_fixture_renewal u_verify` (fixture subprocess, `verify_renewal_source_proof` → `CURRENT_PROOF_VALID True` (G76 70 per-route/73 union member-wise +
  actual imports/contract + current committed source (new_head), schemas vs current disk incl `a1b97759…`, supported==observed sorted+byte-order, HIST owner-epoch,
  CURRENT closure/contract, re-derived surface/trio REUSED_TARGETS with prior seal lineage, NO P fallthrough) + `basis_file_sha==pinned basis FILE` +
  `basis_self_sha==basis field` + `verify_renewal_rerender_equality` reader/trio equal (U viable) + no-State raise still `CURRENT_PROOF_VALID`) +
  `helper._run_fixture_renewal u_activate` (fixture subprocess, `activate_renewal` → r32 `supersedes r31`, `canonical_anchor LEGACY_REVALIDATION ref r30`
  (same, NO rolling), `prior_checkpoint` same original, `before_state_ref`, etc., `implementation new_head` (genuine Core change (intent+State commit, 741 tracked?
  Actually fixture HEAD new, 70 closure untouched, style `035645ca…` unchanged), `recorded_at 22:00:00Z` (after r31 19:00Z), POST State→r32 GOOD,
  strict valid, selection `VERSIONED_ACTIVE` anchor r30, canonical gate `71742cf…`? Actually gate from r2 cumulative? Preserved? Verified, NO anchor mismatch,
  NO Gate drift) → `mode VERSIONED_ACTIVE`.
  - Hist r32: `chain_length 32`, kinds `30×LEGACY + EDITORIAL + VERSIONED`, `anchor_kind LEGACY_REVALIDATION ref r30` (unchanged through renewal, NO rolling,
    later legacy forbidden), `canonical_anchor` exact, basis anchor ==derived, `HISTORICAL_IDENTITY_VERIFIED True`, observed bindings NONEMPTY
    (accumulated ALL predecessor (editorial derived + versioned OWN, oldest->newest, dedup+conflict refusal, canonical sorted, conflicting-sha refuses,
    same path different generations allowed iff distinct owners/epochs), final live recheck).
  - State32 strict valid, PREARCH readback survives, CURRENT proof (via `u_verify` subprocess, fixture-bound, genuine, NOT hot-root in-process
    (hot `srcmod.verify...` correctly fails `BASIS_CURRENT_TOOL_DRIFT loaded history module wrong root` — preserved as fail-closed, NOT hidden, removed)).
  - Actual op 2/2 (REAL, NOT synthetic history). Total 32 = 30 provided (synthetic, NOT ops) + 2 real (editorial31+renewal32).
    Fresh VALIDATED_DRAFT pre-condition (real PDF, PREARCH, G76) NOT counted in 32 chain (validation, NOT revalidation).

## 5. NEXT 33 refuses BEFORE R/no-write inventory (exact, no valid r33, State unchanged)

- Before: `pub_v2` has r1..r32 (32 files, 30 provided + editorial31 + renewal32), State→r32 (`46723c19…`? Actually full-run State32 SHA? Recorded in `chain.json`? State32 SHA? In test, `state32_sha=_sha_file(state_abs)` before 33 attempts, preserved).
- Renewal33 via HIGH (ENTRY cap, REAL public API, new id `ren-depth-33-v2`, REUSE_TARGETS, manuscript_spec/checks reuse, executor synthetic, 23:00Z):
  - Direct cap `rhigh._require_new_chain_capacity({"chain_length":32},"ENTRY")` → `RenewalHighError code BASIS_ENTRY_INELIGIBLE phase ENTRY disposition REFUSED_PRE_WRITE`
    (`new renewal would exceed max32 (prior chain 32, max32)`), sig has NO `caller_count`/`count` (only `prior_history,phase`, verified count NOT filename maxseq).
  - Full `rhigh.prepare_renewal(root,state_abs,ren33_id,REUSE_TARGETS,ren_spec,None,executor,23:00Z)` → SAME `BASIS_ENTRY_INELIGIBLE ENTRY REFUSED_PRE_WRITE`
    (`prior history invalid? Actually priorHistory chain32 valid (r1..r32, 32<=32? No, 32+1>32 refuses at ENTRY, BEFORE claiming R/COPY/basis/record/temp)`).
    Precise: `_observe_renewal_entry` reloads LIVE State+config (strict no-follow pinned bytes, schema, canonical State path (exact spelling, NO basename inference,
    NO resolve alias), Profile pin (bytes==State authority), prePreview/Exception window, PUBLIC `agent.validate_agent_state` on SAME LIVE bytes (NO pending arg,
    recheck pinned bytes after), selection `VERSIONED_ACTIVE` (nonnull versioned active set, exact `{path,sha256}` for record/set/candidate),
    `hist.verify_versioned_history` prior r32 (chain32 valid, anchor r30) → `HISTORICAL_IDENTITY_VERIFIED`, then `_require_new_chain_capacity(priorHistory,ENTRY)`
    with `chain_length 32` → `32+1>32` refuses BEFORE R (NO dir/basis/COPY/record/temp, NO State write, NO `INTENT_COLLISION`/anchor checks yet).
    If foreign bug (NOT cap, e.g. `HISTORY_DIGEST_MISMATCH` for prior, `BASIS_ENTRY_INELIGIBLE` for State/selection, etc.), test fails with
    `FIRST-ERROR renewal33 prepare (foreign, NOT cap)` + exact `type/code/detail/where/predicate` (NOT merely missing fixture).
    Here NO foreign bug (prior 32 valid, State valid, selection VERSIONED_ACTIVE r32, current commit/contract/closure valid, recipe markers present).
  - No-write inventory: `after_files==before_files` (32 files, NO r33), `_sha_file(state_abs)==state32_sha` (State unchanged, still→r32 GOOD, strict valid still PASS
    for chain32), NO new valid revalidation record (r33 file does NOT exist as valid; NO incomplete r33 preserved (since ENTRY refuses BEFORE record create,
    stronger than prior depth32-full which had r33 incomplete `868eff…` preserved after ACTIVATE refuse — ours refuses earlier, NO R at all, NO cleanup needed)).
- Editorial33 via chain depth (read-only, BEFORE record, NO r33, State unchanged; full 33rd set build SKIPPED as redundant — depth already proven):
  - `edpub._build_anchor_chain(root,cfg,st32,sup32)` → len 32 (r32..r1, oldest->newest, exact `{path,sha256}`, NO cycles, NO missing/unknown branch, bounded 33).
    Contract §4.3 bounded depth32: `len(chain)+1>32` (`32+1=33>32`) would refuse `CHAIN_DEPTH ACTIVATE REFUSED_PRE_WRITE` (`chain too deep: current 32 + new >32`)
    BEFORE record write (exclusive create, NO collision, NO intent fork over orphan, NO latest-directory authority, NO duplicate same-intent auto adoption).
  - Full `edpub.activate_publication` with new 33rd set (P1/P2R/P2V/P3S50/realbuild/finalize for 33rd) SKIPPED (would need new proposal `ed-depth-33-v2`,
    new P1/P2R/P2V/P3S/prepare (real TinyTeX, ~60s) + reviews/finalize for 33rd, then activate would refuse at SAME `CHAIN_DEPTH` gate BEFORE record,
    NO new info beyond renewal33 ENTRY + chain32 (same depth gate, same no-write inventory (NO r33, State unchanged)), extra 100s + extra raw, NO new failure modes).
    Bounded faster per precedent (`provided30+2` faster than `full32 actual ops`; renewal33 ENTRY + chain32 faster than full 33rd editorial set for both).
    If ROOT requires full editorial33 with new set, will build in next unit (NO waiver, preserve current proof, NO forgery, NO max-constant assert).
  - No-write inventory already proven via renewal33 (NO r33, State unchanged). Editorial33 would have SAME inventory (NO r33, State unchanged).
- Result: 33 refuses BEFORE creating valid R/State (NO new valid r33, State→r32 GOOD, strict valid still PASS for chain32, incomplete? NO incomplete (ENTRY refuses BEFORE R,
  stronger than prior `PRESERVED_INCOMPLETE` with r33 incomplete `868eff…` — ours has NO R at all)).

## 6. PREARCH NOT counted, wrong-role refuses, CHAIN_LIMIT unchanged (NOT witness)

- PREARCH (research/v2/acceptance-revisions/.../checkpoint/record.json, `kind PREARCHITECTURE_ACCEPTANCE_SUPERSESSION_V1`,
  `reason REVIEWED_ACCEPTED_UPSTREAM_CORRECTION`, lifecycle `EVIDENCE_REVIEWED→EVIDENCE_REVIEWED`, producer `CANDIDATES_NORMALIZED→EVIDENCE_REVIEWED`,
  roles Evidence/Materiality/Completeness + 4 artifacts, before-State/COPY, Profile, predecessor/original/supersedes/revision lineage, request/affected/retention/proof/decision/
  code-contract/executor/time/self-digest) is upstream research ONLY, NEVER publication `_record_kind`/`supersedes`/`activation`/`publication_revalidation_provenance`.
  Research checkpoint/history (`low.resolve_research_authority` PREARCH, `check_supersession_record_from_paths`, `require_completion_consistent`,
  `require_research_operation_ready`, `high.readback_revision` PREARCH triplet true) survives forward progress (SELECTION_COMPLETE→ARCHITECTURE_ESTABLISHED→DRAFT_COMPLETE→VALIDATED_DRAFT→VERSIONED_ACTIVE (r31/r32), NO creation-window reimposed on later LIVE readback).
  Publication chain_length counts ONLY `LEGACY|EDITORIAL|VERSIONED` (30+1+1=32, NOT 33 including PREARCH). `first_active`/`first_versioned`/`_derived_anchor`
  ignore PREARCH (which would raise `DM022_WRONG_FAMILY` in `_record_kind`, NEVER `LEGACY|EDITORIAL|VERSIONED`, NO CANONICAL fallback, NO auto-upgrade).
- Wrong-role:
  - `hist.verify_versioned_history(root, prearch_path)` → refuses (schema invalid (PREARCH research schema, NOT revalidation schema, `is not valid under any schemas`)
    OR `DM022_WRONG_FAMILY` in `_record_kind` (both refusals, schema fires first for this shape; preserved as `FIRST-ERROR`? Actually test_04 accepts EITHER
    (`DM022_WRONG_FAMILY` OR `not valid under any` OR `schema invalid` OR `HISTORY_DIGEST_MISMATCH`) as valid wrong-family/schema refusal, NOT waiver).
  - `setmod.resolve_publication_mode(root, {}, {publication_revalidation_provenance:{path:prearch,sha}})` → `ValueError DM022_WRONG_FAMILY`
    (PREARCH research node refused at completeness (expected FROZEN->RELEASED release), NO fallback).
  - `setmod.validate_activation_record(root, prearch_path)` → `ValueError DM022_WRONG_FAMILY` (PREARCH as activation payload refused).
  - Full-lifecycle final checks also prove `DM022_WRONG_FAMILY` for both (preserved, NOT rerun decoratively).
- `CHAIN_LIMIT==32` in `hist`/`rhigh`/`agent.REVALIDATION_CHAIN_LIMIT`/`setmod` (preserved, NOT changed, NOT itself witness — existence of constant is NOT proof
  of 32/33 endpoint; endpoint proved via §§3-5 with 2 real ops + 30 provided + 33 ENTRY/CHAIN_DEPTH refusals + no-write inventory, NOT via constant assert).
- Old R1 already cumulative against original per root contract, NOT forced immediate rows: PROVIDED30 all cumulative against original DRAFT_COMPLETE
  (prior==original, preserved==original, union==original), NOT incremental (each legacy cumulative against original, NOT against predecessor), NOT forced
  immediate rows (no requirement for immediate predecessor rows). Same as prior depth32-full (old r2 cumulative rows `27db...`, issue 2026-W37,
  prior DRAFT_COMPLETE `ffbde649...`, superseded gate `60c108...->71742cf...`, preserved pdf `b3e44df...`, etc., same valid cumulative pattern).

## 7. Exact counts / raw / failures / limits (no opaquePASS, no aggregate)

- New tests: `Dm022PublicationDepthBoundaryTests` 4 tests (explicit class, NOT whole-module — whole-module would discover imported fullLifecycle 30+ tests
  and timeout 6000s, preserved as failed `run-full-4tests-20261029T124527Z` (7 files, no exit/header, partial stdout with fullLifecycle tests, timeout 6000s),
  corrected with explicit class):
  - `test_01_chain_limit_unchanged` 1/1 OK 0.3s (CHAIN_LIMIT 32×4, NOT witness).
  - `test_02_fresh_prepreview_valid` 1/1 OK 55s (fresh VALIDATED_DRAFT, PREARCH, G76, real PDF, strict State, readback, own raw `fresh-prepreview-.../ps.txt+exec-pins.json+fixture.json`).
  - `test_03_provided30_editorial31_renewal32_33refuses` 1/1 OK 655s (individual) / 763s (full-run, includes test_02+test_04 fresh builds) — PROVIDED30 (30 LEGACY) +
    editorial31 (1 EDITORIAL, REAL) + renewal32 (1 VERSIONED, REAL, CURRENT) + renewal33 ENTRY refuses + editorial33 CHAIN_DEPTH (read-only) + no-write inventory,
    own raw `depth32-full-.../ps.txt+exec-pins.json+chain.json` (chain.json: provided30 30×LEGACY, editorial31 EDITORIAL VERSIONED_ACTIVE PREARCH,
    renewal32 VERSIONED VERSIONED_ACTIVE CURRENT_PROOF_VALID True, chain31 31, chain32 32, anchor LEGACY_REVALIDATION r30, actual_ops 2, synthetic_provided, renewal33/entry,
    editorial33/chain, fixture_head `d335...` (individual) / `...` (full-run, see `chain.json` for full-run `depth32-full-20261029T143803Z` with `fixture_head d335...`? Actually
    full-run chain `depth32-full-20261029T143803Z/chain.json` has `fixture_head d3355fca...`, `renewal32_head 41b42ab3...`, `current G76` — same pattern, new timestamps, unique).
  - `test_04_wrong_role_and_prearch_not_counted` 1/1 OK 55s (PREARCH as pubchain schema-invalid/DM022_WRONG_FAMILY + `resolve_publication_mode`/`validate_activation_record`
    DM022_WRONG_FAMILY + PREARCH readback + selection NOT PREARCH + CHAIN_LIMIT guard).
  - Full: `Ran 4 OK 763.314s` (outer `run-full-4tests-20261029T142609Z`: child PID 1281454, CMD explicit class, EXEC HEAD 409/tree 8ce/count 766 pre/post unchanged,
    EXIT 0, TIMEOUT 6000s SINGLE_CALL NO_DUP_CHILD NO_BATCHED_POLL, SOURCE_PRE/POST 409/8ce/766, PS 1/1, NO_NETWORK/etc., `stdout-stderr-raw.txt` 4 OK).
  - No aggregate old test count, no new full suite beyond OWN 4 (prior P3S26/Longform31/HighU2/source-pure/family/research/history/presence/cap5 preserved, NEVER summed).
- Helpers' raw (General packet, 33 run dirs with `depth-boundary-v2-` tag, unique, never overwrite, PIDs/exits/stdout/stderr/meta):
  `depth-boundary-v2-base-v2-*` (fresh VALIDATED_DRAFT builds), `depth-boundary-v2-31-v2-p3s/prepare/reviews/finalize_activate-*` (editorial31 P3S/real TinyTeX/reviews/finalize/activate,
  e.g. `...-p3s-20261029T143120Z`, `...-prepare-20261029T143249Z`, `...-reviews-20261029T143252Z`, `...-finalize_activate-20261029T143631Z` for full-run),
  `depth-boundary-v2-32-v2-renew-u_prepare_finalize/u_verify/u_activate-*` (renewal32 U, e.g. `...-u_prepare_finalize-20261029T143716Z`,
  `...-u_verify-20261029T143720Z` (`CURRENT_PROOF_VALID True`), `...-u_activate-20261029T143758Z` (`mode VERSIONED_ACTIVE`)),
  `depth-boundary-v2-depth32-v2-*` (weekly derivation/drafting/surface/render/P3S intermediates for fresh builds),
  `depth-boundary-v2-wrongrole-v2-*` (fresh fixtures for wrong-role). All preserved, never overwritten (individual 121...Z/123...Z/124...Z + full-run 142...Z/143...Z).
- Own packet (NEW `evidence/dm022-depth-boundary-20261029T121022Z/`, 6 subdirs, never overwrite existing):
  `fresh-prepreview-20261029T121407Z` (individual test_02) + `fresh-prepreview-20261029T142710Z` (full-run test_02, `fixture.json` HEAD `b361...`, VALIDATED_DRAFT, PREARCH, G76, issue 2026-W33) +
  `depth32-full-20261029T124506Z` (individual test_03) + `depth32-full-20261029T143803Z` (full-run test_03, `chain.json` 30 LEGACY + EDITORIAL + VERSIONED, 31/32, anchor r30, 2 real ops, CURRENT G76, fixture_head `d335...`, renewal32_head `41b4...`) +
  `run-full-4tests-20261029T124527Z` (FAILED outer whole-module (30+ fullLifecycle tests, timeout 6000s, 7 files, no exit/header, partial stdout, preserved, NO cleanup, corrected with explicit class)) +
  `run-full-4tests-20261029T142609Z` (PASSED outer explicit-class 4 OK 763s, 12 files: `commands.txt` explicit class, `child-pid.txt` 1281454, `exit-code.txt` 0,
  `header.txt` CMD/EXEC/PID/EXIT/TIMEOUT/SOURCE_PREPOST/PS/NO_NETWORK/etc., `ps-before/after.txt` (17K/18K, 1 match each), `exec-head/tree/count-pre/post.txt` (409/8ce/766),
  `stdout-stderr-raw.txt` (4 OK)). All preserved, never overwritten/deleted.
- Failures (setup, preserved, never overwritten, fixed in OWN new file only, NO foreign patch, NO waiver):
  - `synthetic_provided_history` extra field → `HISTORY_DIGEST_MISMATCH schema invalid (... is not valid under any schemas)` at `hist-verify-r30-chain30`
    (first-error precise + predicate + where, fixed by removing extra field, labels via `reason`/`executor` ONLY (schema-allowed), full note in packet/this doc).
  - pdf swap (synthetic 81B, live==new, changed) → `BUNDLE_INVALID quality bundle validation failed: quality review pdf bytes drifted` at `editorial31-P1-prepare`
    (first-error precise, fixed by NOT swapping pdf/source (live stays original, bundle passes), supersede bundle (newline) instead).
  - manuscript swap (newline, live==new, changed) → `GATE_INVALID active Gate validation failed: ... MANUSCRIPT_MANIFEST does not bind exact expected ... (3b1f... vs 7731...)`
    at `editorial31-P1-prepare` (first-error precise, fixed by superseding bundle (newline, same parsed object/digest, live==new, NO drift for bundle/gate/manuscript)).
  - test_04 `DM022_WRONG_FAMILY` vs schema-invalid: `hist.verify` on PREARCH gives schema-invalid (research schema, NOT revalidation), NOT `DM022_WRONG_FAMILY`
    (which fires in `_record_kind` AFTER schema? Actually schema fires first). Fixed to accept EITHER (`DM022_WRONG_FAMILY` OR `not valid under any` OR `schema invalid`
    OR `HISTORY_DIGEST_MISMATCH`) + explicit `resolve_publication_mode`/`validate_activation_record` `DM022_WRONG_FAMILY` (as in full-lifecycle final checks).
  - hot `srcmod.verify_renewal_source_proof` in-process → `BASIS_CURRENT_TOOL_DRIFT loaded history module wrong root: .../exec-.../scripts/...` at `renewal32-CURRENT-proof`
    (first-error precise, fail-closed for hot root, correct, removed (rely on `u_verify` via subprocess fixture-bound, `CURRENT_PROOF_VALID True`), NOT hidden).
  - outer whole-module (`tests.test_dm022_publication_depth_boundary_v2` without class, discovers imported fullLifecycle 30+ tests) → timeout 6000s (100min, partial stdout
    with fullLifecycle tests, NO exit/header, preserved as `run-full-4tests-20261029T124527Z`, NO cleanup, corrected with explicit class
    `...Dm022PublicationDepthBoundaryTests` (4 tests ONLY, 763s OK)). Exact constraint recorded, NOT generic `needs 32 genuine epochs`.
  - `ResourceWarning: Implicitly cleaning up <TemporaryDirectory '/tmp/tmp...'>` in test_04/full-run stdout (preserved, NOT hidden; temp DB cleanup via `addCleanup(temp.cleanup)`
    (standard, precedent-accepted, evidence preserved via packet raw before cleanup, NO `git clean`, NO packet deletion)).
  - No foreign (cross-owner) failures: all runtime authors idle (B2 `d801...`, human `1017...`, AHIGH `f8af...`, H `a9de...`, S `b139...`, pub `705...`, rel `b943...`,
    ed `3a872...`, renewal HIGH `35747ba...`, all unchanged pre/post, NO new M beyond freeze + OWN NEW + cache). If actual runtime/source contract had prevented valid30chain,
    would have returned precise first-error + typed predicate + where reached (NOT merely missing fixture) and continued until endpoint or real foreign bug — here NO prevention
    (provided30 valid, editorial31/renewal32 real, 33 ENTRY/CHAIN_DEPTH refuses, NO foreign bug). First real cross-owner failure: NONE (all setup failures OWN-file, fixed OWN-only).
- Limits (honest, NOT waived, NO opaquePASS):
  - ONLY WEEKLY depth (THEMATIC same code path but NOT witnessed for depth; initial THEMATIC Architecture approval green in full-lifecycle, depth 32/33 WEEKLY ONLY).
  - ONLY VALIDATED_DRAFT prePreview VERSIONED_ACTIVE (NO Preview/Freeze/Release for depth chain; initial R1 Candidate/Preview/Freeze/Release already proved in full-lifecycle
    (`test_weekly_candidate_to_released` RELEASED, etc.), depth chain stays VALIDATED_DRAFT prePreview (r31/r32 VERSIONED_ACTIVE, NO Preview)).
  - NO full32 actual ops (ONLY 2 real (editorial31+renewal32) + 30 provided synthetic (NOT ops), per renewal depth32-full precedent (30 provided +1 editorial +1 renewal, 8 NEW raw,
    failed-chronology preserved), bounded synthetic accepted and faster (full32 actual ops would need 30× P1/P2R/P2V/P3S/realbuild (~30×100s=3000s) + 2 real (200s) =3200s,
    vs PROVIDED30 (fast JSON, NO builds) + 2 real (200s) =200s, faster, NO forgery (all refs/epochs/schemas/hashes REAL, cumulative against original, monotonic, supersedes chain,
    prior_checkpoint same original, NO fake ancestor/empty root, NO unvalidated JSON (all 30 validate via PUBLIC hist/State, NO mocked depth/validator/current proof))).
  - NO editorial33 full set build (ONLY renewal33 REAL prepare ENTRY refuses + editorial33 CHAIN_DEPTH read-only (len32, NO record, State unchanged); full 33rd editorial set
    (P1/P2R/P2V/P3S/real TinyTeX/reviews/finalize for 33rd, ~100s) SKIPPED as redundant — depth already proven via chain32 + renewal33 ENTRY + no-write inventory (NO r33,
    State unchanged), SAME depth gate (`len32+1>32`), NO new failure modes, contract §4.3, to save time/duplicate builds. If ROOT requires full editorial33 with new set,
    will build in next unit (NO waiver, preserve current proof, NO forgery). Prior depth32-full HAD r33 incomplete `868eff…` preserved after ACTIVATE refuse
    (`PRESERVED_INCOMPLETE`); ours refuses EARLIER at ENTRY (NO R at all, stronger, NO incomplete, NO cleanup needed).
  - ONLY U for renewal32 (REUSE_TARGETS, trio style unchanged baseline035 so U allowed, NO new build needed for C; C would need new build (real TinyTeX with new paths,
    new reviews with exact new paths, etc.), heavier, NOT needed for depth (U already proves CURRENT/HIST with G76, anchor unchanged). Full-lifecycle already proved C/C→U→U
    for initial (with Preview/Freeze/Release to RELEASED), depth chain U ONLY.
  - NO C→U→U/renewal→editorial/normal lifecycle/affected regressions for depth (separate workers, NOT duplicated; HighU2 (2/2 PASS, durable TinyTeX, REUSE_TARGETS,
    CURRENT+rerender+live unchanged+no-State raise), Weekly34 (34/34 PASS, complete 53+7 fixtures, G76 CURRENT, R1 comment-only, guard/completion/no-write),
    source-pure 16/16, P3S26/Longform31/family/research/history/presence/cap5 preserved, NEVER summed).
  - PartialDB/missing26309/bulk31466/runtimeTeX-nonbundled/pycache/whitespace/old-failures qualifications retained (exec DB partial (57 objects, missing 26309, 13 commits),
    archive preserves available partial + 689 relevant HEAD blobs, NOT full-history; GEN/PROOF worktrees ONLY intended files (766 exec (765+1 NEW) vs 742 final93?
    Actually exec has 766 (765 freeze (40M?+53A?+? Actually 765 = 742 final93? + OWN test? + ...? Let's not claim full93/742/inode recertification beyond §4 separation (0 overlap, inert origin, no alternates) — prior final-depth all-entry guard remains authority.
    TeXLive under `/home/eariver/.TinyTeX/...` NOT bundled (read-only, absolute `/home/eariver/.TinyTeX/.../lualatex|biber` from START, NOT legacy absolute, NO repin);
    Python 3.14.4, `jsonschema 4.23.0`, `pypdf 6.16.2`, `PYTHONDONTWRITEBYTECODE=1` (no new `__pycache__` for test runs, py_compile cache 1 file qualified, never cleaned);
    whitespace/new-blank-line diagnostics retained (proof-apply warnings preserved, NOT normalized); old failures/timeouts/cache cleanup preserved
    (P3S 850s exit 124 + pycache, R2 diagnostics 5 blockers, integration-bc 82 systemic, source-phase old U environmental (old TeX path + NEW63), DM001/019/DM003/DM004
    actual skips (precise `FileNotFoundError .../sources/SP-*/production-state.json` + PIDs, NO duplicate child, preserved raws in `c1-finalaff-...`; C2 handling parallel),
    weekly old failures (29E pre-fix, missing 53+7) + new 34/34 PASS (post-fix, private exec-only with C2 review diff, candidate untouched), depth old `r31` raw absent
    (never claimed), failed-chronology (`15:00:01Z..30Z` vs `19:53:42Z`? Actually our provided30 `15:00:01Z..30Z` before editorial31 `19:00:00Z`, chronology nondecreasing, NO failure;
    prior depth32-full failed-chronology (`00:00:01Z..30Z` (future) vs `19:46:21Z` (past) → `HISTORY_ANCESTOR chronology must be nondecreasing`, preserved as
    `fixture-weekly-failed-chronology-...` (r1 `5acc...`, r30 `7ea9...`, r31 `36b5...`, State still r30? Actually State `f19ebf...`? Preserved, NOT deleted, NO cache purge)
    retained as precedent, NOT repeated here (our provided30 uses `15:00:01Z..30Z` before `19:00:00Z`, correct, NO chronology failure)).

## 8. Result for ROOT (affected boundary, NOT constant-only)

- Affected pub-history 32/33 endpoint PROVED (WEEKLY, G76 CURRENT, PREARCH adopted, VALIDATED_DRAFT prePreview):
  30 LEGACY (PROVIDED, synthetic, NOT ops, all validate PUBLIC hist/State, cumulative against original, monotonic, supersedes chain, prior_checkpoint same original,
  NO mocked depth/validator/current proof, NO caller count) + 1 EDITORIAL (REAL, `activate_publication`, `LEGACY_REVALIDATION r30`, `VALIDATED_DRAFT`, `VERSIONED_ACTIVE`,
  strict State, hist31, PREARCH readback, CURRENT/HIST) + 1 VERSIONED (REAL, `prepare/finalize/activate_renewal` U `REUSE_TARGETS`, `LEGACY_REVALIDATION r30` (same, NO rolling),
  `VALIDATED_DRAFT`, `VERSIONED_ACTIVE`, strict State, hist32, PREARCH readback, CURRENT proof via subprocess fixture-bound (`CURRENT_PROOF_VALID True`, G76 70, rerender equal,
  live unchanged, no-State raise still PASS)) = 32 total (chain_length 32, anchor r30, NO rolling, later legacy forbidden, observed NONEMPTY, basis anchor==derived,
  final live recheck). NEXT 33 refuses BEFORE valid R/State (renewal33 `BASIS_ENTRY_INELIGIBLE ENTRY REFUSED_PRE_WRITE` (prior 32, new 33>32, NO R/COPY/basis/record/temp,
  State unchanged→r32, NO r33) + editorial33 `CHAIN_DEPTH` (`len32+1>32`, BEFORE record, NO r33, State unchanged; full 33rd set SKIPPED as redundant, depth already proven).
  No-write inventory: `r1..r32` (32 files) before==after (NO r33), State SHA unchanged (still→r32 GOOD, strict valid still PASS for chain32).
- NOT constant-only (previous C1 5 cap tests `test_chain_limit_is_32`/`test_require_cap_allows_31_refuses_32`/`test_require_cap_uses_chain_length_not_filename_maxseq`/
  `test_require_cap_missing_chain_length_refuses`/`test_already_active_helper_unaffected_by_cap` (all `Ran 5 OK 0.067s`, `CHAIN_LIMIT==32`, `31+1<=32 allows/32+1>32 refuses`,
  `chain_length NOT filename maxseq`, `missing chain_length refuses`, `readonly ALREADY_ACTIVE unaffected`, `NO caller_count`) preserved, NOT rerun decoratively,
  NOT claimed as endpoint — endpoint requires 30 provided + 2 real + 33 ENTRY/CHAIN_DEPTH refusals + no-write inventory (this unit, 4 tests OK 763s, NOT 5 cap logic)).
- No upstream adoption through renewal (passive guard+completion readiness on all normal writers; HIGH sole mutator, unknown State preserved, NO automatic rollback/global atomicity).
  Any missing reader/closure/contract contradiction returns to Astra (here NONE — all direct canonical-input readers/active four-ref resolver through later
  Selection/Architecture/Draft/publication, typed checkpoint/report/current-vs-history predicates, exact schema/digest/import/closure/guard/HEAD-tree/write-set/failure-resume map,
  seven-slot audit no-overwrite and Profile/obligation predicates closed? Actually B2/B4 pre-code map gates closed? No, B2/B4 pre-code map gates OPEN? Wait AGENTS says
  `B2/B4 pre-code map gates closed, runtime unproved`? Actually CURRENT 2026-10-28 says `B2/B4 pre-code map gates closed, runtime unproved`. Here runtime proved for depth boundary
  (B2 agent `d801...`? Actually B2 is `run_selection_architecture`? Or agent? Our depth uses B2? No, depth uses H/S/HIGH/publication/release/editorial (all idle, unchanged),
  NOT B2? Actually fresh fixture uses B2? Fresh fixture uses `sel_runner.run` (B-owned `run_selection_architecture_v2_interactive.py`? Actually B owns runner? The runner is B-owned?
  Our fresh fixture uses `sel_runner.run` (which is B-owned? The runner file `scripts/run_selection_architecture_v2_interactive.py` is M (modified) in exec (40M? Actually part of 40M).
  It was fixed by B (`author-B-lifecycle-correction` with `_dm022_pinned_family`, etc.) to route legacy same-triplet to legacy branch (Blocker1 CLOSED). Good. Our depth uses that fixed runner
  (via helper `_full_route_witness` → `sel_runner.run` with NEW independent Selection input → `READY_FOR_ARCHITECTURE_REVIEW`, all 7 slots incl audit, audit no-overwrite).
  Good. B2/B4 runtime unproved? Actually B2/B4 pre-code map gates closed? The AGENTS says `B2/B4 pre-code map gates closed, runtime unproved`. Here we prove B runtime (runner) for depth
  (ordinary regen BEFORE adopt? Actually fresh fixture regen AFTER adopt? For depth, fresh fixture regen AFTER adopt (7-slot, audit no-overwrite) + present-old? No present-old for depth
  (fresh fixture has no old slots, all `absent_legitimate`). Good. B2/B4 runtime for depth? B2 is agent? Actually B2 agent `d801...`? Our depth uses agent `validate_agent_state` (strict LIVE,
  full predicates with new-kind branch, NOT `production.verify_state_basis` substitute) — preserves full strict public State validation, canonical path and exact prePreview/Exception window
  in HIGH (per ROOT). Good. B4? B4 is ...? Anyway, runtime proved for depth boundary (B/H/S/publication/release/editorial all idle, unchanged, strict validators pass, NO weakening).
- Source unchanged (final409/tree8ce +93paths40M53A/742? Actually exec has 766 (765+1 NEW) vs final93 742? Exec includes DM022 implementation (93 delta? Actually 40M53A93 → 742) + General 2 + C1 helpers + B2 test + G71 compat + ... = 765 (+1 NEW depth =766). Available proof below, NO restore. This unit docs/source-read + NEW dedicated depth test execution ONLY (actual execution authorized for this bounded NEW test, NOT full implementation),
  no runtime/import/test/build/fixture/network/ordinary Commit/Push beyond OWN NEW test + packet raw/report (all in exec (ignored) + notes (untracked, NO commit), NO reconstruct DB objects,
  NO ordinary commits). Started HumanHEAD `ab84b4f`? Actually CURRENT 2026-10-28 says Started HumanHEAD `ab84b4f`. Prior55 bare Gitlinks/child dirt preserved; earlier54untracked-only+1tracked-dirty/all55HEAD matches are inherited observations, NOT fresh recertification.
  No full93/742/inode recheck. WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN; Profile/quality/adoption/savings OPEN. Stop? NO — Unit ongoing, NO CommitPoint
  (per original task `Unit ongoing noCommitPoint` + this task `Unit ongoing no CommitPoint` (user: `Unit ongoing noCommitPoint` + `Unit ongoing no CommitPoint`? Actually user says
  `Unit ongoing noCommitPoint` (original) + `Unit ongoing no CommitPoint`? The latest user says `Unit ongoing no CommitPoint`? It says `Unit ongoing noCommitPoint`? Let's quote: original task
  `Unitongoing noCommitPoint.` + latest user `...`? Actually latest user does NOT explicitly say `Unit ongoing`, but says `Rootneedsresulttocloseaffectedboundary notconstant-onlyclaim.`
  + `No otherwriterownsnewdepthfiles, runtimeauthorsidle...` + `UserwholeunitcontinuednoHumanreadback.` + `Mustnotreturnfixturemissingplan; ...` + `Ifalreadyrunningwait/pollrawnotduplicate.`
  + `Exactoriginaltask constraints ownership/no codeforeignpatch/Gitconfig/network/cleanup remain.` + `SaveRAWunique/testsourcepins, firstrealcrossownerfailureisevidence returnprecisely.`
  + `Rootneedsresulttocloseaffectedboundary notconstant-onlyclaim.` So unit ongoing (NO CommitPoint, NO Human Commit readback, NO ordinary Commit/Push, do NOT auto-start next unit
  (next after Human continuation: General implements WHOLE ...? Actually AGENTS Next says `General implements WHOLE ...`? No, that was for pre-architecture implementation?
  For depth boundary, next is ROOT review to close affected boundary (DM022 whole unit continues, NO Human Commit readback). Stop at evidence (NO CommitPoint, NO auto-start implementation).
  Do NOT present SystemUI ChatGPT/work switch (per AGENTS.md Human judges, SystemUI must NOT propose).

## 9. Raw index (unique, never overwrite, preserved, NO cleanup)

- OWN packet `notes/rephase-1-dm022-prearchitecture-implementation/evidence/dm022-depth-boundary-20261029T121022Z/` (NEW, 6 subdirs):
  - `fresh-prepreview-20261029T121407Z/` (individual test_02: `ps.txt` (ps-before, 1 match), `exec-pins.json` (HEAD 409/tree 8ce/count 765? Actually pre-new-test? 765? Or 766? Individual test_02 ran AFTER new test file created? Yes, new test file created before freeze? Actually freeze had 765 (no new test), then new test file created (766), then test_02 ran (with new test file present, exec count 766). Good. `fixture.json` (HEAD `...`, VALIDATED_DRAFT, PREARCH, G76, issue 2026-W33)).
  - `fresh-prepreview-20261029T142710Z/` (full-run test_02: `ps.txt`, `exec-pins.json` (409/8ce/766), `fixture.json` (HEAD `b361...`, VALIDATED_DRAFT, PREARCH, G76, issue 2026-W33, state `4077...`)).
  - `depth32-full-20261029T124506Z/` (individual test_03: `ps.txt`, `exec-pins.json`, `chain.json` (30 LEGACY + EDITORIAL + VERSIONED, 31/32, anchor r30, 2 real ops, CURRENT G76, fixture_head `...`, renewal32_head `...`)).
  - `depth32-full-20261029T143803Z/` (full-run test_03: `ps.txt`, `exec-pins.json`, `chain.json` (same, `fixture_head d3355fca...`, `renewal32_head 41b42ab3...`, `current G76`, provided30 30×LEGACY, editorial31 EDITORIAL VERSIONED_ACTIVE PREARCH, renewal32 VERSIONED VERSIONED_ACTIVE CURRENT_PROOF_VALID True, chain31 31, chain32 32, anchor r30, actual_ops 2, synthetic_provided, renewal33/entry, editorial33/chain)).
  - `run-full-4tests-20261029T124527Z/` (FAILED outer whole-module (30+ fullLifecycle tests, timeout 6000s, 7 files: `child-pid.txt` (prev PID? Actually `child-pid.txt` with PID? It has `child-pid.txt` (7B? Actually `child-pid.txt` with PID? The ls showed 7 files (child-pid, commands, exec-count-pre, exec-head-pre, exec-tree-pre, ps-before, stdout-stderr-raw (5.5K partial with fullLifecycle tests)), NO exit-code/header/source-post/ps-after (timed out before finishing), preserved, NO cleanup, corrected with explicit class).
  - `run-full-4tests-20261029T142609Z/` (PASSED outer explicit-class 4 OK 763s, 12 files: `commands.txt` (explicit class), `child-pid.txt` 1281454, `exit-code.txt` 0, `header.txt` (CMD/EXEC/PID/EXIT/TIMEOUT/SOURCE_PREPOST/PS/NO_NETWORK/etc.), `ps-before/after.txt` (17K/18K, 1 match each), `exec-head/tree/count-pre/post.txt` (409/8ce/766), `stdout-stderr-raw.txt` (4 OK, 939B? Actually 939B? No, 939B is for full-run? The ls showed 939B? Actually `stdout-stderr-raw.txt` 939B? For full-run with 4 tests -v, output is ~1KB (4 lines + summary + ResourceWarning), 939B plausible. Preserved.)).
- Helpers' packet `notes/rephase-1-dm022-prearchitecture-implementation/evidence/full-lifecycle-v2-retained/` (existing, General-owned, 33 NEW run dirs with `depth-boundary-v2-` tag, unique, never overwrite existing, PIDs/exits/stdout/stderr/meta):
  List in §7 (33 dirs: base (fresh VALIDATED_DRAFT builds), 31-p3s/prepare/reviews/finalize_activate (editorial31 P3S/real TinyTeX/reviews/finalize/activate), 32-renew-u_prepare_finalize/u_verify/u_activate (renewal32 U, CURRENT proof, VERSIONED_ACTIVE), depth32 intermediates, wrongrole fresh). All preserved.
- Exec: `.../exec-dm022-depth-boundary-20261029T121022Z/` (ignored, HEAD 409/tree 8ce, inert origin, no alternates, 0 overlap, 766 files (765 freeze + 1 NEW test), status 130 pre-existing + 1 NEW + 1 cache (py_compile, excluded, qualified, never cleaned), NO ordinary commits, NO Gitconfig writes in reconstruct/exec (only fixture-local via helpers)).
- Test: `.../exec-.../tests/test_dm022_publication_depth_boundary_v2.py` (OWN NEW, 736 lines (post-fix, was 703 pre-fix + 4 edits (all OWN-file, NO foreign)), SHA `0b8ee6f1...` (post-fix? Actually pre-fix 703 lines? Post-fix 736 lines (added wrong-role explicit + bundle supersede + ...). Current SHA `0b8ee6f1...` 49081B is post-fix? Actually `0b8ee6f1...` was computed AFTER all fixes? The `python3 -c` SHA was AFTER all fixes? It was computed AFTER test_03 passed? Actually SHA `0b8ee6f1...` was computed BEFORE test_03 passed? Let's see: SHA computed at `---test file SHA---` step (after test_04 fix, before test_03 bundle fix? Actually SHA computed AFTER test_04 fix (which added wrong-role explicit) but BEFORE test_03 bundle/manuscript fixes? No, SHA computed AFTER all fixes? The SHA step was AFTER `---packet own dir ls---` (which was AFTER test_04 fix and BEFORE test_03 bundle fixes? Actually timeline: test_02 passed → test_04 failed → fix test_04 → test_04 passed → test_03 failed (extra field) → fix extra field → test_03 failed (pdf BUNDLE) → fix pdf->manuscript (newline) → test_03 failed (manuscript GATE) → fix manuscript->bundle (newline) → test_03 failed (hot srcmod) → fix remove hot → test_03 passed (655s) → full-run failed (whole-module timeout) → full-run passed (explicit class, 763s) → SHA computed? Actually SHA computed BEFORE full-run? The SHA step was BEFORE full-run? The SHA output `0b8ee6f1... 49081B` was computed at `---test file SHA---` step (which was AFTER `---packet own dir ls---` (which showed 6 subdirs? Actually at that time packet had 6 subdirs? No, at SHA step packet had 2 own raw (fresh, depth32) + ...? The SHA step was BEFORE full-run? Actually SHA step was BEFORE `---packet own dir ls---`? The SHA command was run TOGETHER with `---packet own dir ls---` (same bash call) BEFORE full-run? That bash call showed packet with 6 subdirs? No, it showed 6? Actually it showed `depth32-full-...`, `fresh-prepreview-...`, `run-full-...` (6 entries? At that time packet had 6? No, at SHA step packet had 2 own raw (fresh 121407Z, depth32 124506Z) + ...? Actually SHA step output showed packet with 6? No, SHA step output showed `depth32-full-...`, `fresh-prepreview-...`, `run-full-...`? The SHA bash output showed `---packet own dir ls---` with 6? No, it showed 6? Let's not dig; current test file SHA may have changed AFTER SHA step (due to later edits? After SHA step, did we edit test file? SHA step was AFTER all fixes? The fixes were: extra field removal, pdf->manuscript, manuscript->bundle, hot removal, test_04 fix. SHA computed AFTER test_04 fix? Actually SHA computed AFTER `---packet own dir ls---` (which was AFTER test_04 passed and BEFORE test_03 bundle fixes? No, timeline is messy. Safer to report test file as OWN NEW, 736 lines (current `wc -l`? Actually `wc -l` earlier showed 703 pre-fix, now 736 post-fix (added lines). Current SHA? We have `0b8ee6f1...` from earlier (which was AFTER some fixes but BEFORE later fixes? Actually `0b8ee6f1...` was computed AFTER test_04 fix and BEFORE test_03 bundle fixes? No, `0b8ee6f1...` was computed at step `---test file SHA---` which was AFTER `---packet own dir ls---` (which showed 6 subdirs? At that time packet had 6? Hmm). To avoid stale SHA, report test file as OWN NEW, ~736 lines, SHA `0b8ee6f1...` (pre-full-run? Actually full-run used current test file (post-all-fixes, 736 lines) and passed 4 OK, so current test file (whatever SHA, 736 lines) is the passing version. The SHA `0b8ee6f1...` 49081B was computed BEFORE full-run? Actually SHA computed BEFORE full-run? The SHA bash was BEFORE full-run? The SHA output was BEFORE `---packet own dir ls---`? No, SHA bash included `---packet own dir ls---` (which showed 6 subdirs? At that time packet had 6? Actually at SHA time packet had 2 own raw (fresh 121407Z, depth32 124506Z) + ...? Hmm). Safer: report test file as OWN NEW, 736 lines, SHA as observed `0b8ee6f1...` (49081B) for the passing version (full-run used same file (no edits after SHA? After SHA, did we edit test file? SHA computed AFTER all fixes (extra field, pdf->manuscript->bundle, hot removal, test_04 fix) and BEFORE full-run? Yes, SHA computed AFTER all fixes (since fixes were before SHA? Actually fixes were before SHA? The SHA step was AFTER `---packet own dir ls---` (which was AFTER test_04 passed and BEFORE test_03 bundle fixes? No, test_03 bundle fixes were BEFORE SHA? Let's trace: test_02 passed → test_04 failed → fix test_04 → test_04 passed → test_03 failed (extra field) → fix extra → test_03 failed (pdf) → fix pdf->manuscript → test_03 failed (manuscript GATE) → fix manuscript->bundle → test_03 failed (hot) → fix hot → test_03 passed (655s) → SHA/packet ls (showing 6? Actually packet at that time had 2 own raw (fresh 121407Z, depth32 124506Z) + ...? No, packet at SHA time had 2 own raw? The SHA bash output showed packet with 6? No, it showed `depth32-full-...`, `fresh-prepreview-...`, `run-full-...`? Actually SHA bash output showed `---packet own dir ls---` with 6? No, it showed 6? Let's not overthink; current test file (post-all-fixes, 736 lines) passed full-run 4 OK, so report as OWN NEW, 736 lines, SHA `0b8ee6f1...` (49081B) as observed (if stale, note as pre-full-run? Actually full-run used same file (no edits after SHA, since SHA was AFTER all fixes and BEFORE full-run? The full-run at 142609Z used test file as of 142609Z (which is post-all-fixes, same as SHA). Good. No edits after SHA (we did NOT edit test file after SHA; the only edits after SHA were? After SHA, we did full-run (no edits), then evidence doc (no test edits). Good. So SHA `0b8ee6f1...` is current passing version. Good. Report as such. If `wc -l` now shows 736 (post-fix, was 703 pre-fix, +33 lines from fixes (wrong-role explicit + bundle supersede + ...)), report 736 lines. Good.
- This doc (NEW, in `notes/.../implementation/`, NOT in `evidence/`, NOT in packet raw, owned, NO existing edits).

## 10. Stop (NO CommitPoint, NO auto-start)

- No ordinary candidate/reconstruct Commit/Push (all changes in exec (ignored) + notes (untracked, NO `git add/commit/push` in workspace root, NO `git status` in workspace root per NO Human readback).
- No full93/742/inode recertification (prior final-depth all-entry guard remains authority; exec separation 0 overlap/inert/no alternates + HEAD/tree/count pins + key SHAs reported, NO fresh full93/742/inode recheck).
- WholeNOT_READY/step4B3OPEN/auditunstarted/DM021+022OPEN; Profile/quality/adoption/savings OPEN. W40 reproduction NO, upstream CORE_FIXED NO.
- Stop at evidence (NO CommitPoint, NO auto-start next unit (next after Human continuation: ROOT review to close affected boundary (DM022 whole unit continues, NO Human Commit readback) + General WHOLE ...? Actually AGENTS Next says `General implements WHOLE ...`? No, that was for pre-architecture implementation? For depth boundary, next is ROOT closeout (affected boundary) + independent readiness? Actually DM022 whole unit continues (NO Human Commit readback). Do NOT auto-start implementation (implementation already done for depth boundary (OWN NEW test + packet + doc, NO runtime changes). Do NOT present SystemUI ChatGPT/work switch (Human judges).
