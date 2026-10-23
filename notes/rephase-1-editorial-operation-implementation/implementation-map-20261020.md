# R3 editorial operation — pre-code interface/copy return (implementation LEAD)

2026-10-20. Human continued after `df63555`; root observed `main...origin/main` clean and
governing contract `d880f53ec3215a151768b5b7987787571456914ffb1990cfcdaf63e88e9e3e4d` unchanged.
This invocation is **PRE-CODE interface/copy return only**. No new design resubmission,
no unattached helper, no source code edits, no fixture/test/build, no network,
no candidate/reconstruct commits. Root handles delegation; no subagents spawned here.

Governing (all read): `outputs/rephase-1-editorial-operation-contract-decision.md` (191 lines),
packet `notes/rephase-1-editorial-operation-contract/README.md`,
`astra-review-resolution.md` §3, mandatory technical Overriding qualification
(item1 legacy cumulative not incremental, item2 versioned KEEP selected not observed),
operation review §9 final-binding addendum (§4.3 line 85 + §5 line 100).

## 0. Copies, packet, verification scope

- Available source (read-only, preserved): `/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60`
  actual detached `409b292756dd1277b9dfae87679934c0d2ce251c` / tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  full status 4M+18A=22, cached empty, diff 4 names, index present.
- NEW independent implementation copy (this invocation):
  `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60`
  same HEAD/tree/detached/status/cached/diff, inert origin `https://example.invalid/rephase-candidate-recovery.git`,
  no active hooks (only `*.sample`), no `objects/info/alternates`, no `info/alternates`,
  shallow `774dd39a...`, sparse-worktree config preserved, `cp -a` independent inodes
  (`SHARED_COUNT=0` on 4-sample: `.git/index`, `survey_agent_control_v2.py`,
  `jgaisurvey.sty`, `publication-surface-revalidation.schema.json`).
- Original + R2 fixtures preserved: no restore/reapply of old scripts, no `git clean/reset/raw deletion`,
  no source edits. Source mutation recheck: still 22 rows after copy.
- Expected22 verified from corrected `notes/rephase-1-initial-build-integration/source-packaging/complete22-manifest.json`:
  `OK=22 TOTAL=22 MISMATCHES=0` both SRC and DST; `complete22-409-clean.patch`
  SHA `7c82ec47eb82dc56210b82063fe04c583d29cd36df5ce19f48297ebd4f000334` 1233999B;
  static21 `notes/rephase-1-dm021-p3s/draft-history-r11/static21.json`
  SHA `1c0e339ceb31ddb8d565580f4e0d0b2140085cc414bb766b46872fdc8a2ef1a5`;
  style `templates/survey/jgaisurvey.sty` SHA `035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec` 6569B.
- Sanitized env: `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0` +
  `git --no-optional-locks`; `GIT_DIR/WORK_TREE/INDEX_FILE/OBJECT_DIRECTORY/ALTERNATE_OBJECT_DIRECTORIES/COMMON_DIR/PREFIX`
  all unset (recorded in prep stdout). No lazyfetch: no `promisor/partial` in `config --list`,
  inert remote only. Workspace HEAD `df635550c4683a43da731f33c90f88703e303034` read-only;
  new packet files are untracked `??` (expected, not a Human Commit Point).
- Snapshot scope (not generic certification): HEAD/tree/detached/full-status/index/config/hooks/remote/
  alternates/pins recorded; cache probe is `root __pycache__ absent + maxdepth2 find empty` only;
  inode walk is exact 4-sample `stat dev:ino` comparison, not whole-tree census; tool-observed
  hashes only. Old checker scripts NOT rerun; python hashlib comparison is new read-only observation.
- NEW prep script BEFORE execution: `notes/rephase-1-editorial-operation-implementation/prepare_implementation_copy_20261020T131500Z.sh`
  Raw: `prep-stdout-20261020T131500Z.txt`, `prep-stderr-20261020T131500Z.txt` (empty),
  `prep-exit-20261020T131500Z.txt` (`0`). Unique DST stamp `20261020T131527Z`.
- TL2026 probe availability only (no installer/test/build):
  `/tmp/opencode/jgas-texlive-20261019T133205Z/texlive/bin/x86_64-linux/lualatex` exists;
  `latexmk` exists; R2 `weekly-build/special-build` dirs available with real `main.pdf/log/sha`.
  Reuse actual available path/runtime; no new toolchain install in pre-code.
- This file: `notes/rephase-1-editorial-operation-implementation/implementation-map-20261020.md`
  (this return). Stop for ROOT map approval, not Human Commit Point.

## 1. Exact files + function edits / ownership groups

All paths relative to implementation copy root. Line refs are current-source anchors; edits keep
same files (no renames) except 2 new modules + 5 new schemas.

**Group L — low-level identity (owns `survey_publication_set_v2.py` + seal/activation schema + anchor/digest):**
- `schemas/publication-surface-revalidation.schema.json` (161 lines): refactor to two fully strict
  branches. Preserve branch1 verbatim legacy object/required 14 keys/`additionalProperties:false`
  with `reason_class=REVIEWED_CORE_CHANGE`. Add branch2 `EDITORIAL_PUBLICATION_ACTIVATION_V1`
  exact keys (§4.3): `schema_version,kind,issue_id,reason_class,reason,lifecycle,prior_checkpoint,supersedes,canonical_anchor,before_state_ref,before_active_digest,before_candidate_ref,set_ref,core,executor,recorded_at,establishment`.
  `canonical_anchor={kind,ref}` kind `VALIDATION_CHECKPOINT|LEGACY_REVALIDATION`.
  `supersedes` common chain edge both branches. No top-level required leaking across branches.
- `scripts/survey_agent_control_v2.py`:
  `_resolve_publication_revalidation:1090` / `resolve_active:1084` — add branch dispatch
  (validate each record under its own branch; legacy writer cannot emit editorial authority;
  mixed later-legacy-after-activation unsupported fail-closed, not canonical fallback).
  `_check_immutable_revalidation_rows:847` — add editorial branch: check 15-role seal table binding,
  `before_state_ref/supersedes/before-Candidate/digest` agreement, no second active-role table,
  no fake legacy rows. `_check_revalidation_chain:952` — enforce same issue/`prior_checkpoint`,
  strictly increasing numeric sequence, nondecreasing valid instants, no cycles/duplicate links,
  bounded depth 32, missing/unknown branch refuses; historical validation reads retained State copy.
  `_validate_checkpoint_record:264` (`:291-295` superseded-mapping condition only when
  `authority.path==prior_checkpoint.path`) — must NOT apply to editorial active projection;
  active roles come from seal table. `_resolve_checkpoint_artifact:512`, `_validate_agent_state:353`
  (`:391-425` active revalidation), `_validate_stage_artifacts:1204`,
  `revalidate_publication_surface` writer (~:784+) — legacy writer refuses editorial reason;
  new activation writer lives in high-level module, not here.
  `approve_publication_preview:1465` (`:1480-1483` canonical `publication/v2/publication-candidate-v2.json`) —
  revised-mode exact active Candidate (via resolver §8), canonical approval output path stable.
  `validate-state` CLI `main:2263` — unchanged containment, calls branched validator.
- `scripts/survey_publication_set_v2.py` (NEW, §2): pure identity/selection, anchor/digest,
  active projection. Owned by Group L, reviewed boundary with Group H.

**Group H — high-level operation (owns `survey_editorial_publication_v2.py` + 4 new schemas + receipt/Gate/Reader branches + CLI):**
- `schemas/editorial-publication-source-manifest-v2.schema.json` (NEW): strict
  `schema_version,kind=EDITORIAL_PUBLICATION_SOURCE_V1,issue_id,research_profile,publication_profile,generator_route,proposal_ref,retention_manifest_ref,staged_manifest_ref,scope_review_ref,reviewed_reader_input,authored_refs,accepted_refs,current_tools,outputs,receipt_sha256`.
  `outputs` exactly 3 staged refs. `receipt_sha256` hashes canonical object without itself.
- `schemas/editorial-publication-set-v2.schema.json` (NEW): strict
  `schema_version,kind=EDITORIAL_PUBLICATION_SET_V1,status=SEALED_INERT,issue_id,research_profile,publication_profile,proposal_ref,staged_manifest_ref,build_record_ref,roles,set_sha256`.
  `roles` exactly 15 keys `file_ref` values (see §4). No activation hash, no `external_reviews` duplicate map.
- `schemas/editorial-publication-build-record-v2.schema.json` (NEW, §5).
- `schemas/editorial-manuscript-spec-v2.schema.json` (NEW, §5).
- `schemas/editorial-toolchain-spec-v2.schema.json` (NEW, §5).
- `schemas/reader-manuscript-v2.schema.json` (124 lines): add optional
  `editorial_source={proposal_ref,staged_manifest_ref}`; absence retains canonical
  `survey_root/main.tex` rule verbatim; presence requires verified P3S proof.
- `scripts/survey_reader_publication_v2.py`: `_validate_manifest_semantics:171` (`:218-219`
  `source_path.resolve()==survey_root/main.tex`) — add editorial_source branch (proof calls
  existing `verify_staged_source`, never P2V/seal). `build_manuscript_manifest:297` — same branch.
- `schemas/reader-surface-gate-v2.schema.json` + `scripts/survey_reader_surface_gate_v2.py`:
  `_derivation_for_manuscript:1145` (`:1160-1231` DIRECT_PRIMARY / Longform / Weekly) —
  add strict editorial derivation branch bound to new receipt + original proposed-reader ref +
  exact early scope review + exact staged trio/manuscript; existing old receipt branches strict retained.
  `evaluate_reader_surface_gate:1234`, Gate builder/validator/CLI `:1962+` changed together; CLI refuses
  unknown branch. Postrender semantic record NEVER substitutes for early scope.
- `scripts/survey_weekly_derivation_v2.py` / `survey_longform_derivation_v2.py` /
  `survey_longform_generated_v2.py` / `survey_weekly_semantic_publication_v2.py` /
  `survey_longform_semantic_publication_v2.py`: receipt dispatch — add editorial receipt validator
  `validate_editorial_receipt`; existing Weekly/Longform `validate_receipt` dispatch extended,
  old canonical receipt constraints retained.
- `scripts/survey_editorial_publication_v2.py` (NEW, §2): prepare/build/finalize/full-set
  verification/activation + CLI. Calls P2R/P3S proof + Reader/QA/Gate/Candidate + P2V before-eligibility.
  Source-proof entry for Reader/receipt must NOT call seal/activation. Explicit call-graph boundaries.
- `scripts/survey_quality_v2.py`: `validate_checks:132` / `build_bundle:193` — deterministic-check inputs
  use existing contract with actual evidence results; no automatic family PASS by schema.

**Group C — consumers/resolver/workflows (owns resolver + all §8 callers + R1 refusal + export):**
- Resolver (NEW in low-level, used by all): `resolve_publication_selection` + single role-aware
  `resolve_publication_artifact_path(root,cfg,state,role)` with State argument (see §8).
- `scripts/survey_stage_validation_v2.py`: `_prior_artifacts:159` + `_publication_approval_artifacts:130`
  — active publication roles/Candidate via resolver + historical+active identity checks;
  canonical original checkpoint templates historical only, never rewritten.
  `VALIDATED_DRAFT:523` / `RELEASE_CANDIDATE:575` semantic checks — active Candidate binding.
- `scripts/survey_production_v2.py`: `validate_state_semantics:658` (`:784-809` canonical
  Candidate/PDF binding) — revised-mode exact active Candidate; canonical approval/Freeze/Manifest
  outputs stable with refs pointing to active set.
- `scripts/survey_profiled_freeze_v2.py`: `build_profiled_freeze:50` (`:58` canonical
  `publication-candidate-v2.json`) — revised-mode exact active Candidate via resolver.
- `config/survey-production-v2.json`: `gate_inputs.PUBLICATION_PREVIEW:224-226`
  (`:225` publication-candidate template), `stage_plan.VALIDATED_DRAFT:347` (`:356` candidate template) —
  introduce `publication-candidate` token deriving active candidate or canonical default; DRAFT templates fixed.
- `scripts/survey_orchestrator_v2.py`: `_configured_expected_artifacts:125`,
  `_configured_gate_inputs:142` — State-aware recompute+compare in loaders, not only producers.
- `scripts/survey_handoff_v2.py`: `expected_output_contract:48` (`_expand:41` only `{source_root}`) —
  role-aware resolver with State.
- `scripts/survey_human_gate_v2.py`: `_expand_gate_path:205`, `_reviewed_artifacts:230`
  (`:247-274` canonical candidate+PDF) — State-aware; recompute+compare.
- `.github/workflows/survey-production-v2-export-publication-preview.yml` — watch State activation +
  versioned Candidate paths; choose exact State-bound Candidate; fail on ambiguous/mismatched input;
  never export inert set merely because its file changed. Manual `candidate_path` input validated same way.
  Release workflow/checkpoint/generic Candidate/QA/Freeze builders: explicit refs largely work; verify
  via actual integration (no automatic generic-code edit). Stable canonical Manifest path + Freeze
  Candidate ref stay.
- `scripts/survey_editorial_correction_proposal_v2.py`: `_active_effective:380`,
  `_build_graph:563` (`mutable` COPY set `:570-596`, `_pol:597-599`, live State COPY `:613-614`),
  pipeline/receipt recheck, before-graph/retention/Candidate observation — support canonical +
  active-set before-graphs, repeat correction; no current-before call after activation (P2V caller updated).
- `scripts/survey_editorial_current_authority_v2.py`: `observe_current_authority:101` — extend to
  active-set basis (live-vs-retained compare + scope reload); fresh `SCOPE_BOUND` is before-eligibility
  for prepare/activation only, never a receipt replay dependency after activation.
- `scripts/survey_editorial_retention_v2.py` + `scripts/survey_editorial_staged_source_v2.py`:
  keep historical namespace/source-proof semantics + public P1 destination conflict; update exact
  import/schema closure for new deps (never silent `unchanged37`).
- `scripts/survey_weekly_mechanical_refresh_v2.py:890` + interactive revision wrapper +
  semantic-quality canonical writer + canonical Weekly/Special build workflows — revised-mode refusal
  BEFORE destructive action/output/guard creation unless explicitly routed through new operation.
  Initial publishers already `DRAFT_COMPLETE`-only: preserve that guard + verify revised refusal.
- `config` contract-files + receipt `CURRENT_CLOSURE`s + P3S fixed deps + CLI registration/docs —
  register every new authority-bearing module/schema + affected transitive consumer (see §10).

## 2. Two new modules (exact boundaries)

- `scripts/survey_publication_set_v2.py` — LOW-LEVEL identity only.
  MAY use: `survey_production_v2` core safe path/hash/schema primitives
  (`repo_local_path`, `sha256_file/bytes/object`, `load_json`, `parse_instant`, `aggregate_file_hash`),
  `survey_schema_v2` loader, stdlib `json/hashlib/pathlib/datetime`.
  MUST NOT call (import or runtime): `survey_agent_control_v2`, `survey_stage_validation_v2`,
  `survey_reader_surface_gate_v2`, `survey_reader_publication_v2`, receipt validators,
  `survey_editorial_correction_proposal_v2` (P1), `survey_editorial_retention_v2` (P2R),
  `survey_editorial_staged_source_v2` (P3S), `survey_editorial_current_authority_v2` (P2V),
  QA/Gate/Candidate builders. Core State calls it via local import; no top-level cycle.
  Exposes: `validate_seal(root,set_path)`, `validate_activation_record(root,record_path)`,
  `derive_canonical_anchor(root,cfg,state,chain)`, `before_active_digest(rows,candidate_ref)`,
  `resolve_publication_selection(root,cfg,state)->identity_selection`,
  `resolve_publication_artifact_path(root,cfg,state,role)->Path`.
  Validates all selected file refs, allowed role/path structure, seal/record binding, historical anchor.
  Claims no semantic replay.

- `scripts/survey_editorial_publication_v2.py` — HIGH-LEVEL operation + source proof + CLI.
  MAY call: existing P2R `verify_retention`, P3S `verify_staged_source`, Reader/QA/Gate/Candidate APIs,
  P2V `observe_current_authority` for before-eligibility, low-level set module above,
  Weekly/Longform derivation + receipt validators.
  Source-proof entry used by Reader/receipt MUST NOT call seal or current activation.
  Keep explicit call-graph boundaries despite shared file; no import-time execution.
  Exposes contract §6 signatures (all path args repo-contained unless build tooling):
  `prepare_publication(root,state_path,proposal_path,staged_manifest_path,manuscript_spec_path,toolchain_spec_path,recorded_at)->prepared_paths`
  `finalize_publication(root,state_path,proposal_path,staged_manifest_path,deterministic_checks_path,semantic_review_path,visual_review_path,recorded_at)->set_ref`
  `validate_editorial_receipt(root,receipt_path,state_path)->receipt`
  `validate_prepared_set(root,state_path,set_path)->validated_set` (no active record needed, returns no permission token)
  `activate_publication(root,state_path,set_path,reason,executor,recorded_at)->result`
  `resume_activation(root,state_path,record_path)->result`
  `verify_activation_history(root,record_path)->historical_result`
  `resolve_publication_selection(root,cfg,state)->identity_selection` (re-export low-level).
  Prepare consumes existing valid P3S set + referenced scope/retention; derives final paths; invokes real
  build + public source-proof/manuscript construction; never regenerates P1 after retention, never invents review.

## 3. Actual import graph (mandatory pre-code return)

Top-level (static, must be verified by implementation via AST + runtime import probe):
- `survey_publication_set_v2` top-level imports ONLY: `survey_production_v2 as core`,
  `survey_schema_v2 as schema_gate`, stdlib. No function-local imports to forbidden modules.
- `survey_editorial_publication_v2` top-level imports: `core`, `schema_gate`,
  `survey_publication_set_v2 as setmod`, `survey_editorial_retention_v2 as retention`,
  `survey_editorial_staged_source_v2 as staged`, `survey_reader_publication_v2 as reader`,
  `survey_quality_v2 as quality`, `survey_publication_v2 as publication`,
  `survey_reader_surface_gate_v2 as gate` (for Gate builder only, not for identity),
  `survey_weekly_derivation_v2/survey_longform_derivation_v2` + generated receipt modules.
  Function-local imports: `survey_editorial_current_authority_v2` inside prepare/activation
  (before-eligibility only); `survey_agent_control_v2` inside activation for State replace
  (no Gate→receipt→State recursion: full receipt calls strict State + route loaders which terminate
  in identity resolution via `load_derivation` → `validate_agent_state` + `resolve_checkpoint_artifact`,
  never full Gate/receipt).
- P3S historical scope uses narrow Session adapter + review loader
  (`staged.verify_staged_source:1699-1889` → P2R `verify_retention` on manifest-declared retention path
  `:1811-1837`, retained State COPY `:1861-1871`, KEEP Profile `:1876-1884`; explicitly NO P2V/current-State/HEAD
  `:1699-1705`). P1 review loader: `proposal_v2._Collector` raw-first safe/reverify + `session.safe_read`,
  `HASH_CONFLICT/POLICY_CONFLICT` refusal; staged manifest `scope_review_ref` exact path, no forced rename.
- Proof/replay: receipt validation independently reloads exact early scope review; verifies P2R/P3S
  historical replay; rederives proposed reader from NEW proposed authoring + unchanged accepted Draft;
  compares canonical reader FILE bytes + all rendered output bytes; verifies current contract/tool closure
  + actual current accepted research via strict State + ordinary route loaders.
- Writer/reader separation: low-level never calls high-level; high-level never called by low-level.
  `validate_agent_state` uses low-level + existing checkpoint/report/Human agreement.
  Implementation must emit actual `python -c` import graph + `git grep ^import/^from` enumeration as
  reviewed test boundary before code (mechanical return, not authority-policy choice).

## 4. Strict schemas

- Revalidation schema refactor (see §1): branch1 verbatim legacy; branch2 exact keys above.
  `supersedes` common edge both branches. `before_state_ref` = proposal basis State ref + P2R retained
  COPY exact bytes; `supersedes`/before-Candidate/digest agree with retained-before + fresh current-before.
  Historical validation reads retained copy, never expects old hash at updated live State path.
  Equality mandatory on explicit orphan-resume.
- Seal `editorial-publication-set-v2.schema.json`: top-level
  `schema_version,kind=EDITORIAL_PUBLICATION_SET_V1,status=SEALED_INERT,issue_id,research_profile,publication_profile,proposal_ref,staged_manifest_ref,build_record_ref,roles,set_sha256`.
  `roles` exactly 15 `file_ref={path,sha256,byte_count}`:
  `reader-input, authoring-input, source-receipt, reader-manuscript, validated-source,
  bibliography, style, publication-pdf, build-log, pdf-digest,
  quality-regression-bundle, semantic-review, visual-review, reader-surface-gate, publication-candidate`.
  Each path checked against §2 (proposal/staged refs or supplied immutable review ref).
  Source/manuscript/bundle/reviews/Gate/Candidate/build record agree on shared paths/SHA/bytes/page-counts.
  QA result refs validated/pinned through bundle. No activation hash, no duplicated `external_reviews` map.
- Receipt `editorial-publication-source-manifest-v2.schema.json` (§1 keys).
  Generator route existing Weekly or Longform. Authored refs keep distinct proposed
  publication-authoring vs accepted Draft archive roles. Outputs exactly 3 staged refs.
- Reader `reader-manuscript-v2.schema.json`: optional `editorial_source` branch (§1);
  absence retains canonical rule; presence requires verified P3S proof (same issue/Profile/Architecture/
  approval, exact original proposal namespace, actual staged manifest + exact primary/Bib/style refs).
  Existing coverage/fidelity/leakage rules retained.
- Gate schema/loader/CLI changed together; old canonical receipt branches retained strict.

## 5. Build-record / manuscript-spec / toolchain-spec (exact names + keys)

- `schemas/editorial-publication-build-record-v2.schema.json` — file
  `P/publication/build-record.json`. Exact keys:
  `schema_version,kind=EDITORIAL_PUBLICATION_BUILD_V1,issue_id,proposal_ref,staged_manifest_ref,
  declared_inputs{primary,bibliography,style},recipe{fixed_steps},toolchain{executable,versions,argv,env},
  outputs{publication-pdf,build-log,pdf-digest},exit_code,recorded_at,build_sha256`.
  Excludes itself from digest inputs. `declared fixed recipe/options/env`, required argv, versions,
  actual outputs recorded. Failed build yields no admissible set.
- `schemas/editorial-manuscript-spec-v2.schema.json` — input file supplied to prepare
  (e.g. `P/publication/manuscript-spec.json`, caller-chosen name but validated). Exact keys:
  `schema_version,kind=EDITORIAL_MANUSCRIPT_SPEC_V1,issue_id,proposal_ref,
  architecture_coverage[],reader_requirements[],authored_by,recorded_at`.
  Contains ONLY existing coverage/requirement assertions/author/time inputs, no caller source/profile overrides.
- `schemas/editorial-toolchain-spec-v2.schema.json` — input file supplied to prepare
  (e.g. `P/publication/toolchain-spec.json`). Exact keys:
  `schema_version,kind=EDITORIAL_TOOLCHAIN_SPEC_V1,executor,absolute_executable,recipe,argv,env,recorded_at`.
  Executor configuration, NOT approval; absolute executable + declared fixed recipe/options/env.
- Manuscript output: `P/publication/reader-manuscript-v2.json` (existing Reader schema + editorial_source).
- New receipt: `P/publication/validated-source-manifest.json` (editorial receipt schema).
  QA bundle `quality-regression-bundle-v2.json`, Gate `reader-surface-gate-v2.json`,
  Candidate `publication-candidate-v2.json`, seal `publication-set.json` — all under `P/publication/`
  except primary trio stays `P/staged-source/{main.tex,references.bib,jgaisurvey.sty}`.
  External reviews at final repo-contained immutable refs (recommended `P/publication/reviews/`,
  exact supplied refs retained without relocation); result deps explicitly enumerated from validated schemas,
  no generic path scan. No symlinks/latest/mtime authority.

## 6. CLI signatures / parse path roots / refusal

Extend `survey_agent_control_v2.py main:2223` subparsers OR new
`survey_editorial_publication_v2.py main` (selected: new module CLI, same `--repo-root/--config`
conventions; no fixture-only driver; publicly exposed command must not depend on fixture driver).
All `--repo-root` resolved, all other paths parsed via `core.repo_local_path` /
`_revalidation_row_path` containment (raw-first, no-follow, alias refusal); absolute or `..` escapes refuse.
- `prepare-publication --state <State> --proposal <P/proposal.json> --staged-manifest <P/staged-source/staged-source-manifest.json> --manuscript-spec <spec> --toolchain-spec <spec> [--recorded-at <instant>]`
  → prints `prepared_paths` JSON. Refuses: invalid P1/retention/scope/P3S, pre-existing conflicting/same-byte
  target, incomplete dir takeover, unknown toolchain executable, build failure.
- `finalize-publication --state <State> --proposal <P> --staged-manifest <...> --deterministic-checks <QA results> --semantic-review <supplied> --visual-review <supplied> [--recorded-at]`
  → prints `set_ref`. Rechecks current-before scope + all input pins before writes; constructs deterministic
  wrapper + Candidate from validated inputs; validates Gate with early proposed-reader scope; writes seal last.
- `validate-editorial-receipt --receipt <validated-source-manifest> --state <State>` → receipt JSON.
- `validate-prepared-set --state <State> --set <publication-set.json>` → validated set (no permission token).
- `activate-publication --state <State> --set <publication-set.json> --reason <text> --executor <id> [--recorded-at]`
  → `result {status: ACTIVATED|ALREADY_ACTIVE|INDETERMINATE, record_path, state_path, observed_old/new/unknown}`.
  Requires fresh in-invocation P2V SCOPE_BOUND, complete set validation, exact current State bytes,
  same predecessor/current contract/tool scope, valid original/active-before Candidate, predecision eligibility.
  Repeats stable pin checks immediately before first record write AND immediately before State replace.
- `resume-activation --state <State> --record <activation-record>` → installs exact record after full revalidation
  or returns read-only status; ordinary activate refuses collision when record exists but State still exact old.
- `verify-activation-history --record <activation-record>` → historical result (inert/historical/current-active distinct).
- Existing `revalidate-publication-surface` (`--reason-class/--reason`) — legacy writer path; refuses
  `REVIEWED_EDITORIAL_CORRECTION` (must use new activation). `refresh-mechanical-evidence`,
  `advance-stage/approve-*`, `validate-state` unchanged except branched validation.
- All failures exit `2` with `code: [phase/disposition] detail` typed message; stdout is JSON result only,
  stderr is human detail. No caller shell string for build (fixed recipe, no `shell=True`).

## 7. Complete write / ownership / failure / resume / close taxonomy

Single writer/operator assumption explicit; no multi-file atomicity/globalCAS/power-loss guarantee.
Writers use exclusive create (`O_EXCL`), held/no-follow ownership where implemented; remaining window
disclosed + fault-tested.

- ONLY writes: new exclusive activation record (existing sequence naming under
  `canonical publication/v2`, e.g. `publication-surface-revalidation-rN.json`), then known-byte
  State temp+replace updating ONLY `publication_revalidation_provenance`. No canonical Candidate/source/QA rewrite.
  New State validates selected set + normal stage/Preview path before success.
- New exclusive outputs (prepare/finalize): `build/{main.pdf,main.log,main.pdf.sha256}`,
  `build-record.json`, `reader-manuscript-v2.json`, `validated-source-manifest.json`,
  `quality-regression-bundle-v2.json`, `reader-surface-gate-v2.json`, `publication-candidate-v2.json`,
  `publication-set.json` (last). Writers claim new output paths exclusively; refuse pre-existing
  conflicting OR same-byte target; preserve incomplete outputs; never delete foreign/unknown files.
  Staged4 vs build3 inventories separate; build auxiliaries outside publication inventory;
  external files are pinned dependencies, not writer-owned.
- Failure table (contract §7, must be fault-tested with immediate observed delta):
  prepare/build/review/finalize incomplete → old State healthy, inert dir preserved, new proposal ID for
  new attempt, no same-byte takeover/auto-cleanup.
  seal complete before activation → explicit retry with full current-before recheck; seal is NOT permission.
  record created but State still exact old → `resume_activation` revalidates full current-before/set/record
  intent and may install exact record; ordinary activate refuses collision.
  State already exact new pointer → validate strict active State + full set, return `ALREADY_ACTIVE`
  read-only, no ownership takeover/fresh approval.
  State neither known old nor expected new / unreadable / unsafe → preserve all bytes, `INDETERMINATE`,
  no automated overwrite/rollback/adoption.
  close/postreplace validation failure → report primary + secondary errors + observed old/new/unknown
  disposition; never delete referenced/possibly-referenced record; explicit recovery, not file-presence success.
- Close taxonomy: every record/State write/close/late-readback failure classified with
  `phase/disposition/observed-delta` + explicit resume/healthy control test. Resume proves current
  consistency/eligibility, not creator identity; does NOT authorize post-Preview correction or manual State rollback.

## 8. Active path resolver + all callers

- Resolver (in `survey_publication_set_v2.py`):
  `resolve_publication_selection(root: Path, cfg: dict, state: dict) -> dict`
  returns `identity_selection {mode: CANONICAL|VERSIONED_ACTIVE, active_set_ref|None, effective_roles{7}, candidate_ref}`.
  `resolve_publication_artifact_path(root,cfg,state,role: str) -> Path`
  single role-aware path resolver with State argument. Fixed DRAFT templates unchanged;
  `publication-candidate` token derives active candidate or canonical default. Recompute + compare in
  loaders, not only producers. `resolve_checkpoint_artifact(validation,role)` + stage `_prior_artifacts`
  return active projection ONLY after historical + active identity checks; raw historical inspection separate.
- All callers (must all be active-aware or explicitly refuse revised mode before code-complete):
  `survey_agent_control_v2._resolve_* / _check_immutable_revalidation_rows / _check_revalidation_chain /
  _validate_checkpoint_record / _resolve_checkpoint_artifact / _validate_agent_state /
  _validate_stage_artifacts / approve_publication_preview:1479 / _revalidation_record_path /
  _revalidation_existing_sequences / _publication_revalidation_roles:685 / _pending_conditions`;
  `survey_reader_publication_v2._validate_manifest_semantics:207-219 / build_manuscript_manifest`;
  receipt dispatch (Weekly/Longform) + Gate `_derivation_for_manuscript` + builder/CLI;
  `survey_stage_validation_v2._prior_artifacts:159 / _publication_approval_artifacts:130 /
  VALIDATED:523 / RELEASE_CANDIDATE:575 semantic checks`;
  `survey_production_v2.validate_state_semantics:784-809`;
  `survey_profiled_freeze_v2.build_profiled_freeze:58`;
  `config gate_inputs:225 / stage_plan:356`;
  `survey_orchestrator_v2._configured_expected_artifacts:125 / _configured_gate_inputs:142`;
  `survey_handoff_v2.expected_output_contract:48 / _expand:41`;
  `survey_human_gate_v2._expand_gate_path:205 / _reviewed_artifacts:230`;
  preview-export workflow trigger/discovery/manual input; release workflow/checkpoint/generic
  Candidate/QA/Freeze builders (verify via integration); P1 `_active_effective:380` + pipeline/receipt
  recheck + before-graph/retention/Candidate observation + P2V caller; P2R/P3S closure updates;
  canonical revalidation/R1 refresh/interactive wrapper/semantic-quality writer/canonical Weekly/Special
  build workflows (refuse revised mode pre-write).

## 9. Canonical R1 / revalidation / wrapper / build pre-write refusal

- Existing canonical mechanical refresh (`survey_weekly_mechanical_refresh_v2.refresh_mechanical_evidence:890+`,
  active-predecessor `:899`, Gate-role `:920-938`) + canonical revalidation writer +
  interactive revision wrapper + semantic-quality canonical writer + canonical Weekly/Special build workflows:
  in revised mode (State selects versioned set) REFUSE BEFORE destructive action/output/guard creation
  unless explicitly routed through new operation. R1→correction supported (freshly derived before basis,
  including 2 refresh records with correct cumulative anchor). R1 AFTER versioned activation explicitly
  REFUSES before writes (not supported by threading active refs). Versioned mechanical renewal is
  unselected capability loss / whole-readiness obligation (§10); no false editorial-reason bypass,
  no silent old-canonical-bytes refresh. Initial publishers already `DRAFT_COMPLETE`-only: preserve guard
  + verify revised refusal in integration tests.

## 10. Exact affected CURRENT_CLOSURE + P3S fixed deps + contract-files (not `37+unknown`)

- `survey_weekly_derivation_v2.CURRENT_CLOSURE` (8): `survey_weekly_derivation_v2.py`,
  `survey_weekly_semantic_publication_v2.py`, `survey_drafting_citation_refs_v2.py`,
  `survey_bibliography_access_provenance_v2.py`, `render_article_draft_tex.py`,
  `reader-surface-input-v2.schema.json`, `weekly-publication-source-manifest-v2.schema.json`,
  `jgaisurvey.sty`. Must add: `survey_publication_set_v2.py`, `survey_editorial_publication_v2.py`,
  `editorial-publication-source-manifest-v2.schema.json`, `editorial-publication-set-v2.schema.json`,
  `editorial-publication-build-record-v2.schema.json`, `editorial-manuscript-spec-v2.schema.json`,
  `editorial-toolchain-spec-v2.schema.json`, `reader-manuscript-v2.schema.json` (amended),
  `reader-surface-gate-v2.schema.json` (amended) + every touched consumer module/schema in §8.
- `survey_longform_generated_v2.CURRENT_CLOSURE` (14): `survey_longform_generated_v2.py`,
  `survey_longform_semantic_publication_v2.py`, `survey_longform_derivation_v2.py`,
  `survey_drafting_citation_refs_v2.py`, `survey_bibliography_access_provenance_v2.py`,
  `render_article_draft_tex.py`, `longform-reader-input-v2.schema.json`,
  `longform-publication-source-manifest-v2.schema.json`, `reader-surface-semantic-review-v2.schema.json`,
  `reader-surface-gate-v2.schema.json`, `survey_reader_surface_gate_v2.py`,
  `survey_production_v2.py`, `survey_schema_v2.py`, `jgaisurvey.sty`. Same additions as above
  (Weekly+Longform both extended; exact post-change tuples enumerated in implementation, never `+unknown`).
- P3S `_SHARED_PY` (27) + `_SHARED_SCHEMAS` (5) + route extra (3) + staged module (1) + style (1) = 37
  asserted at `survey_editorial_staged_source_v2:140-142`. Must extend `_SHARED_PY` with
  `survey_publication_set_v2.py` + `survey_editorial_publication_v2.py` (+ any new consumer imported
  by staged proof path) and `_SHARED_SCHEMAS` with the 5 new schemas above; size assertion updated
  from `27+5+3+1+1` to exact new counts (e.g. `29+10+3+1+1` if only those; actual counts fixed in code,
  verified by `TOOL_DRIFT` refusal). Never claim silent `unchanged37`.
- `config/survey-production-v2.json contract_files`: `pipeline` 60+ entries (`:6-70`,
  docs/prompts/schemas incl. `reader-manuscript/quality-bundle/candidate/preview-approval/visual/freeze/release/checkpoint`
  schemas) + `quality` 3 entries (`:71-75`). Must append every new schema + touched consumer script/config
  path actually loaded via `control_paths` (`weekly:594`, `longform:547`, `retention:602`) and
  `implementation_control_roots:87` (`config/schemas/scripts/.github/workflows`).
  `verify_tool_basis` ancestry/dirty/untracked + `contract_identity` equality enforce it; omission fails closed.
- CLI registration/docs: `survey_agent_control_v2 main:2223` subparsers + new module `main` + workflow docs;
  every new authority-bearing module/schema + affected transitive consumer registered in same unit.

## 11. Historical anchor (last legacy before first activation, cumulative original)

Legacy rows are CUMULATIVE against original validation checkpoint (Overriding qualification corrects
old `per-link incremental` wording; actual `_check_revalidation_chain:1010-1012` passes SAME original
`prior_record` into `_check_immutable...` for every link). Root contract preserves that semantics and
derives NEW editorial canonical anchor:
- No legacy revalidation before first activation → anchor = original validation checkpoint.
- Otherwise anchor = LATEST legacy record immediately preceding first activation. Validate each legacy
  link's original-checkpoint union under its own legacy semantics. Recorded `canonical_anchor` must equal
  chain-derived identity. Repeated activations retain same anchor. Legacy writer after activation refused;
  mixed chain with later legacy successor unsupported fail-closed, not canonical fallback.
- `before_active_digest` = canonical SHA of sorted effective 7 publication checkpoint rows +
  exact observed Candidate ref/null at activation entry. `canonical_anchor={kind,ref}` kind
  `VALIDATION_CHECKPOINT|LEGACY_REVALIDATION`. Historical checkpoint/report/implementation/contract +
  unchanged research still verified; materialized canonical files checked against anchor effective rows;
  new set refs checked separately. Exactly 7 publication roles project to active seal roles; no
  research/Architecture/Draft rebinding. `prior_checkpoint` = original validation ref; `supersedes` =
  exact prior revalidation/activation ref or null.

## 12. Repeated correction retention

P1 classification changes explicitly (REQUIRED new behavior, not current-P1 proof):
prior immutable versioned publication/staged/proposal/seal/Candidate bytes = `KEEP_IMMUTABLE`;
mutable live State = `COPY`; mutable non-versioned control inputs retain actual policy.
First canonical before-graph keeps existing P1/P2R conservative capture. All KEEP refs byte-checked;
immutability is operating rule + detection, not filesystem magic. Second pre-Preview correction resolves
active-set before-graph (effective rows, not original canonical bytes); P1/P2V must support canonical +
active-set graphs; no current-before P2V call after activation.

## 13. Draft contradictions explicitly avoided

No canonical Candidate install before/after activation (State sole selection mutation; all active
Candidate consumers explicitly changed). No `publication/outputs` duplicate or staged-trio copy;
primary trio stays P3S staged4. No duplicate reader/authoring copy; no forced assumed
retention-manifest basename (use staged manifest `scope_review_ref` exact path). No receipt/manuscript
needs future seal to validate; no leaf self-reference; seal stores no activation hash / no `external_reviews`
map. No `active_set`/verified-dict/pending boolean from caller as permission. No postrender semantic record
as early scope (Gate binds early proposed-reader scope). No P2V after activation as receipt replay.
No old-authored/new-reader mix (rederive proposed reader from NEW proposed authoring + unchanged accepted Draft;
compare canonical bytes). No self-referential fixture (no F0 receipt containing F0's yet-unknown SHA;
meaningful SOURCE commit before authority). No incremental `prior_sha256` rollforward. No synthetic
detector/signature or runtime-generated genuine PASS; no fake F0 authority. Current epoch = tool/contract/
receipt/basis consistency, not recency.

## 14. Fixture / verification plan (no decorative full-suite rerun)

Order: meaningful independent SOURCE commit (actual complete new source/contract) BEFORE authority fixtures.
Then: actual accepted research/Architecture/Draft + initial publication authority → P1/retention/early-scope/P3S
→ new preparation/build → separately labelled supplied review fixtures → seal/activation.
- Changed-reader correction reaches healthy active Candidate + normal synthetic Preview/Freeze/Release
  using REAL PDF (both initial routes unchanged; Weekly `WEEKLY_GENERATED_V2` + Longform `LONGFORM_GENERATED_V1`
  via TL2026 `lualatex` + fixed recipe, real exit/log/versions/digests, exclusive transfer to `build3`).
  Old canonical files + old Candidate byte-identical; exact proposed early-review path retained.
- Second pre-Preview correction works; legacy R1×2→correction uses correct cumulative canonical anchor;
  active vs historical readback distinct; artifact-only commits only under actual closure predicates.
  Meaningful new source build when source/tool inputs change.
- Required positives: both routes unchanged; changed-reader→active Candidate→synthetic lifecycle;
  R1×2→correction; repeat correction; inert-valid vs historical vs current-active readback; `ALREADY_ACTIVE`;
  resume orphan exact record; close/postreplace secondary-error reporting.
- Required negatives (on PUBLIC callers, not standalone validators): same-issue wrong seal/manuscript/Candidate;
  old canonical Candidate supplied after activation; inert valid set not adopted; unconsumed/unknown record branch;
  research ref change; old-authored/new-reader mismatch; equal-SHA different reviewed path; stale/failed/missing
  external reviews; build failure/extra input/output/hash drift; seal missing role/unknown ref/duplicated role;
  legacy-anchor error/cycle/depth/sequence; State/predecessor drift; approved/foreign Candidate;
  canonical writer after activation; EVERY record/State write/close/late-readback failure with immediate
  observed delta + explicit resume/healthy control. Test public callers / loaders (recompute+compare),
  not merely standalone validation or earlier unintended refusal.
- Regressions (needed only): exact staged/receipt/current contract dependency changes,
  Reader/Gate/State/stage/Preview/Freeze/export path handlers, affected R1 initial-mode guard,
  P1/P2R/P2V/P3S repeat behavior. No full old-suite decoration; no milestone-count-as-test-count.
- Synthetic vs genuine: typed fixtures visibly separate; author-independent semantic/visual inspection
  of real PDF separately from synthetic type/authority fixtures; no agent-generated genuine Human approval;
  production semantic NO-GO retained.

## 15. Workable parallel split (shared interfaces fixed, lead integrates)

Shared frozen before code: §4 branch keys + 15-role table + receipt/build-record/spec keys + §6 signatures
+ resolver signatures + write/ownership/failure taxonomy + closure enumeration rule.
Lead (this invocation) integrates; no detached helper-only completion.

- Worker A (Group L): `survey_publication_set_v2.py` + revalidation schema branch + anchor/digest +
  `survey_agent_control_v2` branch dispatch + `_validate_checkpoint_record/_resolve_checkpoint_artifact`.
  Disjoint paths: new low-level module + revalidation schema + agent control edits only.
- Worker B (Group H): `survey_editorial_publication_v2.py` + 4 new schemas (receipt/set/build-record/specs) +
  Reader/Gate/receipt dispatch + `survey_quality_v2` + Gate/Reader builders + new CLI.
  Disjoint paths: new high-level module + 5 new schemas + Reader/Gate/quality/receipt files only.
- Worker C (Group C): resolver wiring + `survey_stage_validation_v2`, `survey_production_v2`,
  `survey_profiled_freeze_v2`, `config`, `survey_orchestrator_v2`, `survey_handoff_v2`,
  `survey_human_gate_v2`, export workflow, P1/P2V repeat, P2R/P3S closure bumps, R1/wrapper/build refusal,
  `CURRENT_CLOSURE`/`contract_files`/CLI docs. Disjoint paths: consumer/config/workflow files only.
- Integration: lead owns cross-file import-graph probe + closure enumeration + fixture SOURCE commit order +
  full §9 positive/negative matrix + independent review/audit handoff. Unexpected unrelated defect returns
  for scope choice; partial helper-only is NOT acceptance.

## 16. Packet paths + blockers

- Packet: `notes/rephase-1-editorial-operation-implementation/`
  `prepare_implementation_copy_20261020T131500Z.sh` + `prep-stdout/stderr/exit-20261020T131500Z.txt` +
  this `implementation-map-20261020.md`.
- Source copy: `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60`
  (NEW unique root; SRC preserved; R2 `/tmp/opencode/jgas-final22-*`, `jgas-initial-*`,
  `jgas-texlive-*` untouched).
- Essential blockers: NONE for map approval. Implementation blockers to be enforced, not waived:
  (a) actual import-graph extraction + `CURRENT_CLOSURE`/P3S-S2/`contract_files` exact enumeration
  before code; (b) TL2026 executable/toolchain pin selection recorded in toolchain-spec (absolute path +
  versions, no caller shell string); (c) fixture SOURCE commit before authority (no F0 self-reference).
  No runtime/code/test/build/fixture/source changes in THIS unit.

**Return complete. Awaiting ROOT map approval before whole selected two-route
prepare→review-input→finalize→activate→normal consumer implementation.**
