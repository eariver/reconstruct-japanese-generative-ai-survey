# Selection scaling repair — R2 corrected integration map (MAP-ONLY, no code)

Status: R2 corrects R1 per `astra-repair-resolution.md` FULL + `independent-map-review.md` F1–F11.
R1 `integration-map.md` preserved; this R2 is the implementation-ready unified design.
No source edits/imports/runtime/tests/fixtures/network/Git/reconstruct readback/subagents in this unit.
Source: active `.../repaired-correction-rehearsal-20261112T125743Z/candidate-work`
HEAD `ae0dd1ee5b0e7a85c44bdab0e6cd024bf12f0c56` parent `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325`
tree `ec11cf6c49b3cdf54c7aa98703f6d3e74806dc58`; final773 manifest `a7e40c47…`/202833B BASE `409b292`,
final141 patch `171812f6…`/5532921B unchanged. Active + shadow preserved; no install/retry over them.
R1 pins reused as expected pins (not rebaselined); line numbers are active-worktree observations.

Root decisions applied: (a) no obligation to optimise every initial 3/6AG if bounded full initial + real 7-run proves practical;
(b) remove multiplicative 45AG first-EU / 90AG summary; (c) may retain LOW `low:1073` second AG unchanged —
R2 retains it unchanged and accounts initial cost; (d) private cross-module helpers allowed with owner/lifetime/B1;
(e) `_load_upstream_content` is NOT LIVE equivalence — predicate-diff + sibling-acceptance binding required;
(f) State-hash/triplet alone insufficient; historical package-SHA needs sibling acceptance + rerun;
(g) immutable commit text / `cat-file -e` alone insufficient — retain full own-epoch batch;
(h) new HEAD does NOT auto-conflict — facade `verify_current_stage_basis` handles old-State init;
(i) pins captured BEFORE validation bytes consumed, with inventory/containment/lineage.

## 1. Unified mechanism (one design, no generic aspirations)

Bounded full initial (unchanged code, full cost) → pre-capture full closure → single content-EU + single upstream →
cheap freshness for all later writes/returns. No new module/schema/family/global/epoch/ContextVar/public-flag/
caller-verified-dict/third-validator. Public signatures unchanged (see §8). No architecture moved to LOW.
Shared predicate cores refactored in existing modules only (no mirrored validators).

- KEEP full: `run:249` 3AG + `run:260` first READY 2AG (including `low:1018` + `low:1073` second AG RETAINED
  unchanged) + `run:264` first resolve 1AG = 6 AG bounded initial. Full 6E/3V nesting + full own-epoch batch
  retained there (F2 explicitly NOT optimised in initial; three-/six-pass is not a defect per root §2).
  Cost is one-time and honestly recorded; real W34/SP 7-run oracle proves practicality (no speedup claim,
  no extrapolation from READY probes: W34 READY 85.01s partial-8E / SP READY 27.98s-12E are observations only).
- REMOVE multiplicative: first `_load_upstream` 45AG at `run:310` replaced by single content load
  (`_load_upstream_content` + `_derive_matrix_rows_content` P, 0 AG, §4); summary double 45AG at
  `base:866`+`:880/:373` replaced by single held `upstream` + private against-upstream validators (§5).
  Net full-run 162AG → 6AG initial + 0AG EU + cheap freshness (FILE/pin/lstat + full own-epoch batch, §6).
- Runner holder optimises ONLY post-population gates (`:271`, `:316`, `:362`, `:427`, `:440`, `:444`,
  `:451`, `:456`, screening second half, matrix/summary second EU). It never retrofits `low:1073`
  (F3 ownership fixed). LOW completion file unchanged.

## 2. Epoch / tool-family / facade (actual semantics, no contradiction)

- Continuation: NEW independent byte-copy of `ae0dd1e` (hardlinks 0, inodes differ, objects 231/231,
  inert origin, no commondir/alternates/worktrees, no new commit, no State/Profile repin). Verify source773,
  spot runner/LOW/HIGH SHAs, both States `EVIDENCE_REVIEWED` init480 history4 Human-pending, PREARCH CPs
  (`W34 73ab28ea…`/6054, `SP 2a528ed5…`/6300), completions, 8 four-ref FILE hashes, active 7-absent vs
  shadow 0/3 partials, guard absent, `GIT_OPTIONAL_LOCKS=0`/`PYTHONDONTWRITEBYTECODE=1`. Work on copy only.
- State file facts (read, not imported): both States `implementation.repository_commit_sha=480823560c0c26ed…`
  (isolated rehearsal identity), history last `e84a82ac…`; W34 record impl `cc1c7fd1…`, SP record impl `ae0dd1ee…`.
  HEAD `ae0dd1e` ≠ State impl `48082…` ≠ W34 recorded `cc1c…` already today — normal operation already
  handles this split. Historical own-epoch uses RECORDED commit (`low:610-617` never demands HEAD==recorded),
  so new repair HEAD does not break history. CURRENT `core.verify_state_basis` (`production:959-995`)
  DOES demand `state.implementation==implementation_sha` (`:983-984`) + contract from LIVE files (`:980-982`),
  but runner EU runs UNDER `agent_tool.current_stage_basis_override` (`agent_tool:121-143`, `finally` restore)
  where `core.verify_state_basis` is replaced by `verify_current_stage_basis` (`agent_tool:42-50`:
  requested `implementation_sha==current HEAD` then `agent.validate_agent_state`, no State-impl equality).
  Runner passes `implementation_sha=repository_commit_sha(repo_root)` (`run:265`; `production:189-207`
  HEAD-only, ignores dirty) so new HEAD passes under override. Outside override, `agent.validate_agent_state`
  (`agent:919-1070`) never checks HEAD, and LOW `require_research_operation_ready`/`resolve`/`check_supersession`
  never check HEAD (recorded-commit + COPY/pins only). LIVE `validate_package_basis` /
  `validate_evidence_package_basis` outside override WOULD fail with new HEAD (State 48082≠new HEAD) —
  R2 avoids them for EU by using State-free content cores (which skip `verify_state_basis`, §4 table).
  No old-implementation override passed, no State/Profile repin, no fresh-init fixture standing in for
  saved-State continuation (F9 resolved).
- Tool-family: strict pinned-record family only. Runner `_dm022_pinned_family` (`run:50-67`) +
  agent `_dm022_pinned_family` (`agent:110-128`) via `low.load_typed_checkpoint_record` (`low:329`);
  `_dm022_state_kind` (`agent:131-149`) test-only, never routing. Override used ONLY at `run:309-313`
  (`derive_candidate_matrix`) and `run:432-436` (`build_architecture_review_summary`); screening inner
  `validate_acceptance` runs under screening-internal override (`screening:1102-1103`).
  `survey_prearchitecture_acceptance_v2.py` pinned in codeset but NOT imported by this writer (call-map §0).
- Commit/test ordering (F9): (i) repair on copy dirty; (ii) dirty oracles + affected tests labelled
  dirty-working-tree (old HEAD string, dirty bytes — not committed-tool proof); (iii) commit new HEAD
  (record new SHA/tree); (iv) CLEAN re-run at least full initial + 7-slot success + return binding with
  no dirty (binds committed bytes, `implementation_sha`=new HEAD under override); (v) DIRECT409
  BASE`409b292`→new-HEAD patch + manifest + proof-copy + fresh CURRENT source proof + independent
  implementation review. Dirty label prevents fake-old-implementation; clean re-run prevents
  new-HEAD-always-fails misreading.

## 3. Family codeset / digest / closure membership (exact paths)

- LOW historical 7 mapped (`low:587-599`, `frozenset`): `scripts/survey_research_authority_v2.py`,
  `scripts/survey_prearchitecture_acceptance_v2.py`,
  `schemas/dm022-revision-request-v2.schema.json`, `schemas/dm022-revision-manifest-v2.schema.json`,
  `schemas/dm022-revision-proof-v2.schema.json`, `schemas/dm022-preadoption-report-v2.schema.json`,
  `schemas/dm022-supersession-checkpoint-v2.schema.json`; `$id`s in `_DM022_SCHEMA_IDS` (`low:601-607`).
  `tool_pins.tool_shas` must equal EXACTLY this set (`low:664-667`); no caller-arbitrary list.
- Own-epoch needed set per AG (`low:685-695`): contract inputs from COMMIT's own
  `config/survey-production-v2.json:contract_files` (pipeline 76 + quality 3, counted live) +
  `config/survey-production-v2.json` + `schemas/survey-production-profile.schema.json` +
  `schemas/survey-production-state.schema.json` + sorted pinned 7 + `request.profile_ref` path.
  Proved via `ls-tree -r` (`low:696`) + `cat-file --batch` (`low:716-726`) + `$id` + Contract8 recompute
  (`low:754-798`, mirrors `core.contract_identity` `production:210-228` + `core.sha256_object`).
  Contract8 unchanged after repair means historical epoch still valid, NOT repaired-code proof (F7);
  repaired-code proof is oracles + affected tests + fresh CURRENT proof + independent review only.
- CURRENT pipeline closure (not own-epoch): 76 pipeline files (docs/redesign/authority/operator/contract/
  schemas/prompts/candidate/draft/publication/freeze/release + `dm022-*` schemas) + 3 quality docs
  + `implementation_control_roots=[config,schemas,scripts,.github/workflows]`. Replay63/66 union is
  precode map membership, not Selection-writer closure — not claimed here. No digest claimed for repaired
  runner/LOW/base until implementation (record new SHA256/bytes then; Contract8/STATE/PROFILE/DM022
  schemas verified unchanged via `sha256_file` before/after, any change returns to root).

## 4. First-EU replacement (F1-b + F8 pre-capture, 45AG removed)

Retain initial 6AG full; first EU at `run:310` MUST NOT be LIVE `_load_upstream` (45AG unobserved for W34-409,
W34 0/7 timeout). Use content cores with pre-captured pins:

- After `:264` (first resolve full), call NEW LOW private
  `low._get_selection_authority_bundle(repo_root: Path, state_path: Path) -> dict`
  (owner LOW, lifetime single call, function-local `evidence/completeness/screening` imports only).
  It re-reads via PUBLIC reloads only (no caller dicts): State FILE → `_resolve_research_from_state_bytes`
  → `_load_typed_four_refs` (classification + 4 FILE/shape + digest + ledger/completeness shape, `low:437-565`)
  → request/manifest/report/proof/decision/retention/COPY/completion reloads (same as `resolve:1181-1201`
  + `_verify_adopted_graph_full:836-925`) → `derive_ordinary_root_effective_context(repo_root, request_abs,
  before_copy_abs)` (`low:1861-1909`, COPY-bound, never LIVE path) for `root_records/root_path/
  effective_records/effective_path/screening_acceptance/profile/canonical_state_path`.
  Then ENUMERATES full closure (exact, no `schemas/*` vagueness) and `_capture_phase_pins` BEFORE any
  content validation (no post-validation baseline):
  State FILE; checkpoint FILE; 4 artifact FILEs; profile FILE (`request.profile_ref`); request/manifest/
  report/proof/decision/retention-inventory/COPY/completion FILEs (SizedRef path+sha+byte_count via
  `_verify_sized_ref_bytes` `low:297-306` + `_safe_read_bytes` `low:147-187` with `O_NOFOLLOW`/dev-ino match);
  DCP `discovery-acceptance` + SCP `screening-acceptance` + accepted Discovery JSONL (root) + effective
  Discovery JSONL (via kernel `low:1510-1684`); screening package/batch/result FILEs (via
  `_check_screening_batches_and_digest` shared helper); evidence acceptance+package + `tasks/*.json` +
  `results/*.json` via `_exact_regular_files(run_dir/tasks|results, expected_names)` (`evidence:1635-1636`,
  names from `package.tasks[].path` basename, `meta_by_id` bind `evidence:1634-1661`); views acceptance+
  `views/*.json` via `_exact_regular_files(views_dir, {view_filename(task_id)})` (`evidence:1819-1826`);
  supplement manifest + EVERY `validated.sources[]` Raw via `_resolve_phase_supplement_context` all-entry
  loop (`evidence:369-376`, `_supplement_source_file` `evidence:497-520` containment/no-follow) +
  `basis_refs` (Discovery+Screening acceptance pins `evidence:359-368`); ledger/completeness FILEs (already
  in 4); retention `inventory.json` 7 rows vs manifest `retention_snapshots` 7 slots exact bind
  (`low:901-917`); completion `seven_plan` 7 rows. Directory inventory: `_exact_regular_files` demands
  exact regular-file set (no missing/extra, no symlink); ancestor containment via
  `_assert_pin_repo_ancestors` (`evidence:280-297`, `_repo_file` policy) + LOW `_repo_rel` (`low:127-135`).
  Returns bundle `{state_path,state_sha,checkpoint_path,checkpoint_sha,four_paths_shas_bytes,
  request/manifest/report/proof/decision/retention/COPY/completion_pins_bytes,
  profile_bytes,root_records,root_path,effective_records,effective_path,screening_acceptance,
  expectations={issue_id,research_profile,canonical_state_path},supplement{manifest_ref,entries:MappingProxyType,raw_refs:tuple,basis_refs,source_root},own_epoch{commit,blobs,contract},guard_lstat,seven_lstat,implementation_sha}`.
  All `entries` as `MappingProxyType`, `raw_refs` as tuple — never mutable caller dict (no `verified_dict`).
- First EU then calls EXISTING `base._load_upstream_content(repo_root,profile_path,discovery_path,
  screening_path,evidence_path,views_path,ledger_path,completeness_path,expectations,root_records,root_path)`
  (`base:85-152`, signature has NO `effective_*`/NO `implementation_sha` — R1 corrected) with bundle
  `expectations/root_records/root_path`, then `base._derive_matrix_rows_content(...)` (`base:183-276`,
  P retained: `sha256_file+load_json` per card/view at `:213-218`). Content cores used:
  `screening._validate_screening_acceptance_content` (`screening:1486-1521`) +
  `_resolve_effective_discovery_basis_content` (`screening:1436-1483`);
  `evidence._validate_evidence_acceptance_content` (`evidence:1738-1793`, pins BEFORE parse `:1747-1751`,
  basis-content `:1768`, ctx DATA-mode `impl=None` `:1779-1785`, `_check_..._with_context` `:1786`,
  freshness BEFORE RETURN `:1789-1792`); `evidence._validate_edition_views_acceptance_content`
  (`evidence:1856-1893`, nested Evidence at `:1876`, views pin+row checks `:1867-1892`);
  `evidence._validate_materiality_ledger_content` (`evidence:2724-2767`, derives effective via content
  `:2758-2762`, shared `_check_ledger_rows_content`); `completeness._validate_profile_completeness_content`
  (`completeness:241-262`, shared `_check_completeness_result_content` + `_validate_obligation_shape`).
  LIVE vs content predicate-diff (F5 table, actual lines):
  State-SHA equality (`screening:1333-1334` LIVE `sha256_file(state)==basis.state_sha256` +
  `core.verify_state_basis` `:1336`; `evidence:1219-1223` same) vs path-identity
  (`screening:1304-1305`/`evidence:1168-1169` `basis.state_path==canonical_state_path`, never SHA/LIVE);
  `_canonical_root_acceptance` State-bound (LIVE `screening:1001-1046`) vs session root
  (content `screening:1444-1483`, no `_canonical_root_acceptance`/`resolve_checkpoint_artifact`/override);
  supplement `implementation_sha`+provided acceptance/discoveries (LIVE `evidence:2000-2006,1241-1248`)
  vs `None`+session (content `evidence:1779-1785,1925-1933,1192-1198`); Discovery SHA
  (LIVE `discovery.resolve()==effective.resolve()` + SHA equality `evidence:810-814,1934-1941` noted)
  vs session-pinned Discovery (`evidence:1934-1941` resolve-compare + `effective.records` coverage).
  Gap coverage: State-SHA → `require_same_triplet` + State FILE rehash + triplet equality at every gate;
  Discovery SHA → FILE rehash vs expected pins; supplement Raw → `_recheck_supplement_context` over ALL
  entries (`evidence:389-424`, never task-subset); package SHA → sibling acceptance exact archived hash
  (`_historical_state_basis_wrapper` semantics preserved: acceptance sibling + archived package hash checked,
  then original predicates rerun with adjusted SHA — content path enforces sibling bind at
  `screening:1513-1514`/`evidence:1765/1925`, NOT triplet-only, per root §2). No predicate duplicated/relaxed;
  private factoring with internally constructed context only.

## 5. Summary single-upstream (90AG removed, no LOW move)

`build_architecture_review_summary` today does `_load_upstream` at `base:866` (45AG) +
`validate_candidate_matrix(matrix,*args)` at `base:880` → `derive_candidate_matrix(*args)` at `base:390` →
`_load_upstream` at `base:373` (45AG, no new input). R2 adds two NEW privates in BASE only
(public `derive/_load/validate/build` signatures unchanged, wrapper `survey_architecture_v2.py:98-136`
  delegation + `_base.validate_architecture=` patch `:141` preserved):
- `base._validate_candidate_matrix_against_upstream(matrix: dict, upstream: dict, profile_path: Path, completeness_path: Path, ledger_path: Path, evidence_path: Path, views_path: Path) -> list[str]`
  (re-derives rows via `_derive_matrix_rows_content` P only, compares `matrix != expected` same as
  `base:388-397`, NO second `_load_upstream`; row P retained, 45AG removed).
- `base._build_architecture_review_summary_with_upstream(repo_root: Path, profile_path: Path, discovery_path: Path, screening_path: Path, evidence_path: Path, views_path: Path, ledger_path: Path, completeness_path: Path, matrix_path: Path, selection_path: Path, architecture_path: Path, implementation_sha: str, upstream: dict) -> dict`
  (takes held `upstream` from first EU, loads `matrix/selection/architecture` JSONs, calls
  `_validate_candidate_matrix_against_upstream` + `validate_selection` (`base:407-564`, small basis/hash/shape)
  + `validate_architecture` (`base:567-...` + wrapper empty-placement contract, small) + summary projection
  (`base:914-1044`), NO `_load_upstream` at `:866`, NO re-derive at `:880/:373`).
Runner holds single `upstream` (invocation-local, `MappingProxyType`/tuple, never in public `run()` return
  which keeps 7 rels + counts + readiness) from first content-EU and passes to both
  `derive` (already done) and summary private overload. Lifetime single `run()`, discarded on any freshness
  failure; cross-invocation nonreuse by construction (local, never module-global/ContextVar).

## 6. Later gates + screening + own-epoch (cheap, with full batch)

- LOW `low:1073` second AG RETAINED unchanged (no LOW completion change; first READY stays 2AG full).
  Later READYs (`:316,:362,:427,:440,:444,:451,:456`) do NOT call `_dm022_require_ready`/
  `require_research_operation_ready`; runner calls NEW LOW-owned private
  `low._assert_selection_authority_fresh(repo_root: Path, state_path: Path, bundle: dict) -> None`
  (owner LOW, calls existing `require_no_active_guard` `low:4024`, `lstat_slot` `low:3984`,
  `_verify_sized_ref_bytes`, `_safe_read_bytes`, `require_same_triplet` `low:387-400`,
  `evidence._recheck_phase_pins/_recheck_supplement_context/_assert_pin_repo_ancestors` function-locally,
  `expected_after` recompute `low:568-584`, seven-plan vs inventory vs `lstat_slot` tolerance `low:1102-1124`,
  PLUS full `low._verify_own_epoch_commit` batch `low:639-799` — retained per root/F6, not SHA-only skip;
  git batch (`cat-file -e` `:671`, `show` `:673`, `ls-tree -r` `:696`, `batch` `:716-726`, `$id`+Contract8
  `:754-798`) is small vs 6E/3V and covers missing/corrupt objects from partial DB
  (`155b78cf…` restored, `b797…`/26309 missing remain). Any non-zero → fail-closed
  `ResearchAuthorityError`/`DM022_TRANSITION_ACTIVE`, never `expected=observed`. Cheap = no 6E/3V walks,
  not zero git reads.
- Runner double resolve: KEEP `:264` full (1AG + lineage `:1214-1228`); REPLACE `:271` with
  `low._assert_selection_authority_fresh` + reuse of `:264` `four` dict (same State/checkpoint, no
  intervening write). `_dm022_pinned_family` (`:270`) stays (typed load only).
- Screening `:283` 6AG: KEEP `resolve_checkpoint_artifact` path full (includes 3AG via `agent:1210`);
  REPLACE inner `validate_acceptance` second 3AG with
  `screening._validate_screening_acceptance_content` + `_resolve_effective_discovery_basis_content`
  using bundle `expectations/root_records/root_path` + cheap freshness (sibling acceptance + archived
  package hash + rerun predicates per `_historical_state_basis_wrapper` `agent_tool:53-118`, not triplet-only).
  `resolve_effective_discovery_basis` (`:286`) unchanged (no AG).
- Within-AG (F2): NO sharing in initial 6AG (retain nesting `low:945-972` + `evidence:1876/2752/2934` as
  correctness). Later cheap gates never re-enter nesting. Fallback ONLY if oracle shows initial still
  impractical: per-AG invocation-local pin/supplement cache (function-local dict, discarded on any drift,
  `_capture_before_validate` + `_recheck_before_return` + ancestor checks preserved, no reseal) — not pre-built.
  If a context class cannot be safely pinned (e.g. newly discovered byte not in §4 enumeration), retain full
  check for that class and articulate cost (per prompt).

## 7. Write + return + slots + LEGACY/standalone/no-supp

Every write keeps gate + no-overwrite + return binding (sites unchanged, only gate cost changes):
`matrix :316→:319`, `selection :362→:365`, `architecture :427→:430`, `review :440→:443`,
`attention :444→:447-448` (`build_attention`/`validate_attention` small),
`archive(shutil.copy2) :451→:454`, `audit(write_json) :456→:459-471` (audit binds input + 5 outputs).
Each preceded by `low._assert_selection_authority_fresh` + `_dm022_preflight_seven` (`:304`, lstat) +
per-file `exists()/is_symlink()` refuse + `lstat_slot` legitimate-regeneration tolerance
(old-absent + new-content/same-byte-new-inode allowed, same-inode stale/nonregular/unreadable refuse,
`low:1102-1124`). Outer `run()` return (`:472-481`) re-binds 7 rels + SHAs AFTER final freshness; any drift
between last write and return refuses (no partial PASS). Seven self-writes need owned progression (not auto-trust,
not immutable-slot block). Partial-failure preserved, no cleanup/retry over partials, unknown/guard refuses,
no auto-rollback. LEGACY: healthy same-triplet LEGACY keeps canonical `materiality-ledger-v2.json`/
`profile-completeness-v2.json`, guard-only READY, no AG/content-cache (family dispatch unchanged).
Standalone/public semantics + `schema_gate.validate_instance` + `_derive_matrix_rows_content` projection
unchanged, no public bypass. No-supplement: `authority_supplement None` + `None+None` refusal preserved
(`evidence:300-330,1194-1198`); supplemented→null refuses.

## 8. Changed paths / imports (no arbitrary budget, no new public)

- `scripts/run_selection_architecture_v2_interactive.py`: add private `_CheckedSelectionAuthority` holder
  (frozen, `MappingProxyType`/tuple fields from §4 bundle) + runner-private `_assert_..._fresh` thin wrapper
  calling `low._assert_selection_authority_fresh` (single existing runner→low edge, no new runner→evidence/
  base/completeness/screening direct private imports); call-site swaps at `:271,:316,:362,:427,:440,:444,:
  451,:456` + screening-second-half + summary-with-upstream. Public `run/_dm022_*` unchanged.
- `scripts/survey_research_authority_v2.py`: add privates `_get_selection_authority_bundle` +
  `_assert_selection_authority_fresh` (function-local `evidence/completeness/screening` imports as today
  `low:459-460,820-821`; top-level B1 leaf rule preserved: only `core`+`schema_gate`+stdlib at top).
  Existing `_verify_completion_full/_verify_adopted_graph_full/resolve/check_supersession/require_*`
  signatures unchanged; `low:1073` retained.
- `scripts/survey_architecture_v2_base.py`: add privates `_validate_candidate_matrix_against_upstream` +
  `_build_..._with_upstream` (reuse `_load_upstream_content/_derive_matrix_rows_content` shared cores).
  Public `derive/_load/validate/build` unchanged; wrapper `survey_architecture_v2.py` delegation intact.
  No new module/schema/family/config/Contract8 input; no global/ContextVar/caller-dict/public-flag.
  If shared cores need refactor across modules, do it in these existing files with exact import delta listed
  at implementation (no 3-file cap imposed).

## 9. Oracles + helper bindings (precise, no vague counts)

- Full initial + 7-run: unmutated W34-409/SP-160 on new clean HEAD via normal `run()` must emit 7/7 exact
  schemas + basis SHA binds + `readiness READY_FOR_ARCHITECTURE_REVIEW` + audit input/output binds;
  `validate_selection/validate_architecture/validate_attention` 0 errors. Helpers:
  `tests/test_run_selection_architecture_v2_interactive.py` (runner contract/no-overwrite),
  `tests/test_dm022_prearch_b_ordinary_consumers_v2.py` (B-side), `tests/test_survey_architecture_v2.py` +
  `tests/test_survey_architecture_review_expansion_v2.py` (matrix/summary).
- First-write: mutate one referenced byte before `:319` (Raw/task/result/View/supplement/COPY/State/
  checkpoint/four-ref/guard/slot) → must refuse at cheap gate with `ResearchAuthorityError`/
  `DM022_TRANSITION_ACTIVE`/provenance-drift, no write. Missing-object (unlink one Raw/task) → pin-recheck
  refuse. Helpers: `test_dm022_b_late_prepublish_v2` + `test_dm022_normal_writer_late_guard_v2`
  (late/prepublish/guard), `test_survey_evidence_v2/test_survey_completeness_v2/test_survey_active_*`
  (Evidence/Views/Ledger/Completeness content).
- Late/outer-return: mutate State/checkpoint/artifact between last write and `:472-481` return → return
  refused (no 7-rel PASS). Helper: same runner test + `test_dm022_c_*`/`test_dm022_c_direct_operation_v2`/
  `test_dm022_full_lifecycle_v2` (completion/resolve/proof).
- Source-epoch/missing-blob: run on copy missing one recorded blob (e.g. simulate absent `b797…` path) →
  full `_verify_own_epoch_commit` batch refuses (proves SHA-only insufficient). Helper:
  `test_dm022_prearchitecture_acceptance_v2` + `test_dm022_prearch_b_ordinary_consumers_v2`.
- Separate invocations/issues: second `run()` must NOT reuse holder (holder is `run()` local — prove by code:
  no module-global/ContextVar, bundle passed explicitly); W34 bundle must not validate SP
  (`issue_id/triplet` mismatch refuses in `_validate_*_content` identity + `require_same_triplet`).
  Helpers: `test_survey_agent_control_v2` + `test_survey_agent_tool_v2` (state/override/facade).
- All-seven archive/audit stable: `archive(shutil.copy2)` byte-equal + `audit` input/output SHA binds stable
  across clean re-run (same bytes, new inode allowed per `lstat_slot` tolerance). Helper: runner test +
  `test_evidence_scaling_v2` (scaling shape, no old expensive rerun).
- LEGACY/no-supp/history-current: LEGACY same-triplet fixture → legacy branch (no AG);
  no-supplement fixture → empty-ctx + `None+None` refusal where needed; COPY-bound
  `derive_ordinary_root_effective_context` refuses LIVE path as COPY and vice versa
  (`low:1890-1896,1937-1945`). Fixtures: `dm022_prearchitecture_fixtures_v2` + `dm022_lifecycle_fixture_v2` +
  `dm022_g71_g76_fixture_v2`. Affected vs unaffected split + genuine changed-tool epochs in isolated
  synthetic fixtures; no old timeout rerun for decoration.
- Record wall/CPU/`rchar` honestly (no uninstrumented ranking/speedup claim); do not extrapolate full-run
  from READY probes.

## 10. Proof + delivery + stop

After repair on new copy: actual W34-409/SP-160 all-seven normal-writer completion, independent actual
output/content binding, fresh CURRENT source proof (`verify_renewal_source_proof` CURRENT_PROOF_VALID +
SAME-proof drift refusal/restore), exact delivery binding, independent implementation review → Commit Point.
Delivery: complete DIRECT409 `409b292`→new-HEAD patch (inherited overlays included, never layer old patches)
+ manifest (per-path SHA/bytes/modes) + proof-copy `candidate-partial-b40de60` check0/apply0 all-paths×3,
scoped689+new, missing26309/bulk31466/runtimeTeX nonbundled + whitespace diagnostics retained.
Prior final141 `171812f…`/5532921B + manifest `a7e40c47…` unchanged until new delivery binds.
Genuine gaps (un-pinnable class, new schema/module/family/global-flag need, supplement shape change,
Profile P1–P4, DM022-HIGH/LOW residual, Thematic/Retrospective scope per 2026-10-31) return to root before
broadening. No generic B2/B4 cycle, reader unit, or timeout-only enlargement.

## 11. Confirmation checklist (root + fresh independent scoped BEFORE code)

Initial-6AG retained + EU/summary multiplicative removed; LOW `1073` retained + later-cheap ownership split;
holder fields→calls/pins/rechecks (§4 bundle); `_load_upstream_content` params + predicate-diff + sibling
bind; new private signatures + call sites + lifetime; full own-epoch batch everywhere; exact import delta +
Contract8≠repair-proof sentence; pre-capture enumeration + no-rebaseline; write/return/slot/LEGACY/no-supp;
epoch commit/test ordering + `implementation_sha` per phase; oracles→helpers→consumers/facade bindings;
proof + DIRECT409 plan; gap/stop conditions. No code until both confirmations.

(End of R2 map — MAP-ONLY, no code.)
