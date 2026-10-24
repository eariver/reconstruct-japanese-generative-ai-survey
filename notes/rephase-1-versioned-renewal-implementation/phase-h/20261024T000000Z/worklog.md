# Phase-H worklog — versioned renewal historian + low structural plumbing (NEW, append-only)

2026-10-24. AUTHOR implementation, bounded phase H of WHOLE renewal (not completion).
Workdir authoritative: `.rephase-1-editorial-runtime/versioned-renewal-env-20261023T185000Z/candidate-work/`
(actual409 HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
intended57 25M32A preserved; phase-H adds NEW files only, no M1 transplant).

## 1. Authority read (no code yet)

- Contract `outputs/rephase-1-versioned-renewal-contract-decision.md` SHA `478f0051...`, including §11.
- Root gate `notes/rephase-1-versioned-renewal-precode/astra-precode-gate-resolution.md` SHA `7d7d5a45...`, including §6
  (LIVE `agent.validate_agent_state` preserved, `production.verify_state_basis` distinct, O17 `""` not `"/"`,
  `schema_pointer` allows `""`, no Screening `Path(".")` repair).
- Precode assessment `outputs/rephase-1-versioned-renewal-precode-assessment.md`, packet README, independent
  readiness review final-binding ROOT resolution + pointer-erratum, integrated R3 (822 lines, `d080c182...`,
  JSON `1f758b0a...`) with R4/R5/R6 deltas AS OVERRIDDEN BY ROOT.
- Environment correction `notes/rephase-1-versioned-renewal-implementation/environment-correction.md`
  (NEW correct source `.../versioned-renewal-env-20261023T185000Z/candidate-work/`, 721 files, 25M32A,
  83-file independent DB, no hardlinks/alternates/inherited GIT env). Rejected M1
  `.../versioned-renewal-impl-20261023T181352Z/candidate-work/` (fake root `a8890d4`, 3 commits, 729 files)
  preserved read-only, never transplanted. Started from actual57, not M1.

## 2. Ownership (this phase only)

- NEW `scripts/survey_versioned_renewal_history_v2.py` (HIST leaf, `verify_versioned_history` +
  `verify_renewal_retention`, typed E/T readers, no agent/Reader/Gate/Candidate/high/P1/P2R/P3S calls).
- FOUR new schemas `schemas/versioned-renewal-*.schema.json` (strict, local `#/$defs/*` only,
  `schema_pointer` type string allows `""`, buildRecord embedded `$defs` with exact
  `REUSED_BUILD`/`EXECUTED_BUILD` variants).
- ONLY low structural plumbing: `scripts/survey_publication_set_v2.py` +
  `scripts/survey_agent_control_v2.py` + `schemas/publication-surface-revalidation.schema.json`
  needed history/typed renewal record (`_is_versioned_record` for 2 pairs, bind new record/seal,
  legacy/editorial otherwise intact). Other workers own source proof/high/content/other consumers.
- Root will integrate; coordinate by exact interfaces, no unmapped fields.

## 3. Historian design (meaningful, no placeholders)

- Raw-first layer (lexical parts, ancestor lstat no-follow, O_NOFOLLOW regular-file reads,
  FD close errors, strict duplicate-JSON refusal, repo containment). Proven safe-reader logic
  extracted locally (no pubset/core import, acyclic; schema_gate only, standalone).
- Owner registry O1..O17 fixed (epoch DERIVED, never caller): O17 scope
  `schemas/reader-surface-semantic-review-v2.schema.json` pointer `""` (whole-doc root, never `"/"`).
  Other inventory pointers (`/properties/renewal_source`, `/properties/renewal_source_proof_ref`,
  `/properties/derivation/oneOf/4`, `/$defs/buildRecord`, `/oneOf/2`) preserved as registered.
- E live original/COPY (never required at tool commit) vs T own recorded commit+path+hash/mode
  (`git cat-file -e <epoch>^{commit}` + `git show <epoch>:<path>` SHA + `git ls-tree` mode `100644`,
  never live-path equality; old T live bytes after Core change never enforced).
  P2R KEEP vs T classification via typed receipt edges + fixed closure membership (no KEEP-prefix,
  no directory-prefix, no `*.py` blanket; unknown closure row → `UNSUPPORTED_MIGRATION`).
  Each schema/closure source owner bound to linked staged producer / current receipt /
  prior renewal basis CURRENT epoch; unknown registry → `UNSUPPORTED_MIGRATION`.
- No evidence at tool commit, no old-code exec, no history calls to State/P1/P2R/P3S/full proof/
  Reader/Gate/Candidate. No caller verified dict or caller epoch authority; returns descriptive
  `HISTORICAL_IDENTITY_VERIFIED` + observed pins only.
- Every ancestor incl renewals: own current tools, namespace/inventory/self-digests/exact cross-bindings
  (early scope/history/build/review targets), bounded chain 32/no cycles/latest legacy anchor never
  rollforward, legacy cumulative original-checkpoint checks. Reused materialization proof/build terminal
  may be older ancestor than immediate predecessor but reachable typed selection lineage; foreign
  sibling (different issue/supersedes branch, equal SHA different path/lineage) refuses.
- New renewal schemas have no untyped objects (`additionalProperties:false` everywhere, every
  `type:object` typed) and no unregistered refs (all `$ref` local `#/$defs/*`).
- Existing current State validation remains full public in HIGH; low calls historian structurally only.
  Dangling high/source calls fail closed (`PublicationSetError` until modules arrive).
- Gate after current normal admission separate (agreement via selection, not historian).

## 4. Low plumbing (exact 2 pairs)

- `survey_publication_set_v2.py`: added `VERSIONED_KIND/REASON/SET_KIND/STATUS` + schema paths,
  `_is_versioned_record` (kind `VERSIONED_RENEWAL_ACTIVATION_V1` + reason `REVIEWED_VERSIONED_CORE_RENEWAL`)
  + `_is_versioned_seal` (kind `VERSIONED_RENEWAL_SET_V1` + status `SEALED_INERT`),
  `_validate_versioned_seal` (new schema, self-digest, 15 roles live, renewal refs live, no full proof recursion),
  `validate_seal` versioned dispatch BEFORE editorial (editorial verbatim), `_validate_versioned_activation`
  (required non-null supersedes/before_candidate/set/basis/proof, retained COPY live, HIST leaf delegation),
  `validate_activation_record` versioned dispatch, `derive_canonical_anchor` versioned branch
  (first-active editorial/versioned, later legacy refused), `_recompute_before_digest` versioned predecessor
  (prior seal seven, before-Candidate equals prior seal Candidate).
- `survey_agent_control_v2.py`: added `VERSIONED_*` consts, `_is_versioned_record` + `_is_versioned_seal`,
  `_check_versioned_rows` (HIST leaf, no legacy row tables, required renewal links, retained COPY live),
  `_check_immutable_revalidation_rows` versioned dispatch, `_check_revalidation_chain` versioned kinds
  (head/link, reason classes, linked activation proof via pubset+HIST), `_check_revalidation_agreement`
  versioned same as editorial (selection effective7), `_resolve_publication_revalidation` versioned branch
  (pubset versioned + chain + agreement), `_validate_checkpoint_record` versioned same as editorial
  (anchored selection). Full public `validate_agent_state` preserved; low calls historian structurally.
- `publication-surface-revalidation.schema.json`: `oneOf` 2→3, added `$defs/versioned_activation`
  (all REQUIRED, `supersedes` REQUIRED non-null authority, `before_candidate_ref` REQUIRED non-null,
  `retained_copy_ref` sized, `before_active_digest` SHA, `renewal_basis/proof_ref` authority,
  `core` typed `versioned_core` with Contract8 (8 keys) + `implementation_commit_sha`, establishment
  pre-decision) + `$defs/versioned_core`. Legacy/editorial branches verbatim.

## 5. Tests (strict unit scope, fresh NEW procedures, isolated DBs)

- NEW `tests/test_versioned_renewal_history_phase_h.py` (5 tests, disjoint temp Git DBs, inert origin,
  genuine tool-before-authority commits, no reconstruct-DB fixtures, no empty root, no saved runners):
  - `test_legacy_oldformat_history_passes`: typed oldformat legacy r1→r2 with real ancestry,
    `HISTORICAL_IDENTITY_VERIFIED`, chain 2, anchor `VALIDATION_CHECKPOINT` (legacy-only).
  - `test_e_uncommitted_at_tool_commit_positive`: tool epoch first, E added later, `git show <epoch>:E`
    fails (positive control per decision §3), historian still passes (no E-at-epoch demand).
  - `test_tool_epoch_change_positive_and_tamper_negative`: observed bindings at own epoch pass;
    tamper (wrong source SHA) → `HISTORY_DIGEST_MISMATCH`; missing blob → `HISTORY_BLOB_MISSING`;
    unregistered schema_path → `UNSUPPORTED_MIGRATION`; O17 `"/"` → `HISTORY_DIGEST_MISMATCH`,
    repair `""` passes. Uses real `tool_a.py`/`tool_schema.json` + O17 schema blobs at epoch.
  - `test_copy_mismatch_foreign_duplicate_raw_symlink`: retained COPY tamper → mismatch, repair passes;
    foreign issue (proof `2026-W02` vs record `2026-W01`) → `HISTORY_ANCESTOR`; duplicate JSON →
    duplicate refusal; absolute/traversal → `HISTORY_MODE`; symlink → `HISTORY_MODE` refusal.
  - `test_chain_depth_and_anchor`: 33-deep fake legacy chain → depth refuse (max32).
- No introspection/AST string-presence as proof; all behavioral (exact HIST codes + repair).
- Raw results (candidate-work, `PYTHONDONTWRITEBYTECODE=1`):
  - `python3 -m unittest tests.test_versioned_renewal_history_phase_h -v` → 5/5 OK (0.795s).
  - `python3 -m unittest tests.test_survey_publication_set_v2 -v` → 18/18 OK (existing low intact).
  - `python3 -m unittest tests.test_survey_publication_set_v2 tests.test_versioned_renewal_history_phase_h -v` → 23/23 OK.
  - `python3 -m unittest tests.test_repository_contract_syntax -v` → 2/2 OK (schemas parse, scripts compile).
  - `python3 -m unittest tests.test_survey_publication_revalidation_v2 -v` → 31/31 OK.
  - `tests.test_survey_editorial_retention_v2` → 25 errors (pre-existing: `git ls-files` misses 32 untracked
    intended files incl `schemas/editorial-manuscript-spec-v2.schema.json`; contract_identity fails in temp
    fixture; same failure before phase-H, not a phase-H regression; no full-suite inference claimed).
- Actual fixture DBs disjoint with genuine old source committed before old authorities; no empty root/
  no objects reconstruct. Existing test helpers used for shape reference; new procedures built minimal
  typed fixtures with real Git ancestry (not invented shapes). End-to-end initial fixture (full editorial
  + C→U→U + renewal→editorial + normal lifecycle) pending lead fixtures worker; this return is strict unit
  scope, not whole PASS.

## 6. Source pins / evidence (this run)

- Run ID: `20261024T000000Z` (phase-h dir `notes/rephase-1-versioned-renewal-implementation/phase-h/20261024T000000Z/`).
- Candidate-work HEAD still `409b292` (no ordinary commits), tree `8ce36998` (base) + worktree changes:
  - M (25, unchanged from actual57): agent_control, revalidation, etc. (see `git diff --name-only HEAD`).
  - NEW phase-H (5, untracked, not in 57): 4 schemas + `scripts/survey_versioned_renewal_history_v2.py`
    (55530 B, SHA `7868122647ff952eec5ffd81eee2a5bce83cc48c63624e32e7058f161ff436f3`) +
    `tests/test_versioned_renewal_history_phase_h.py`.
  - Plumbing edits (tracked M + untracked): `schemas/publication-surface-revalidation.schema.json` (M),
    `scripts/survey_agent_control_v2.py` (M), `scripts/survey_publication_set_v2.py` (untracked part of 57,
    now extended with versioned branches).
  - `__pycache__` residue from test runs (untracked, not source; never blind-copy).
- Rejected M1 + env `184000Z` FAIL preserved untouched (no reset/clean/deletion).
- No network, no old-runner exec, no shell source edits (`Write`/`Edit` only), no `git clean/reset`,
  no ordinary commits in candidate/reconstruct, fixture commits only in separate temp DBs (isolated,
  meaningful source-before-authority, inert origin).
- Remaining: source proof (`survey_versioned_renewal_source_v2.py`) + high (`survey_versioned_renewal_v2.py`)
  + other consumers (publication, quality, gate, staged, weekly/longform, editorial_publication, config,
  test_group_c) + bootstrap/U/C + repeat/C→U→U + renewal→editorial + normal lifecycle + failure/resume +
  affected regressions + independent final review. Whole unit uncompleted; no Human Commit Point from
  partial worker return.

## 7. Interfaces for Root integration (exact, no unmapped fields)

- `survey_versioned_renewal_history_v2.verify_versioned_history(root: Path|str, record_path: Path|str) -> dict`
  returns `{"HISTORICAL_IDENTITY_VERIFIED": True, "observed_refs": [...], "chain_length": int, "anchor_kind": str}`.
  Raises `RenewalHistoryError(code, detail)` with `code` in `HISTORY_*` (`HISTORICAL_IDENTITY_VERIFIED` vs
  `HISTORY_COMMIT_MISSING/HISTORY_BLOB_MISSING/HISTORY_SCHEMA_MISSING/HISTORY_DIGEST_MISMATCH/
  HISTORY_ANCESTOR/HISTORY_MODE/HISTORY_TOOL_EPOCH_DRIFT/HISTORY_PACKAGE_MUTATED`), `BASIS_*`
  (`RETAINED_COPY_MISSING` etc. via retention), `UNSUPPORTED_MIGRATION`, `REVIEW_TARGET_MISMATCH` (via
  versioned ancestor issue/lineage), `INDETERMINATE` (not used here). No permit, no caller dict/epoch.
- `survey_versioned_renewal_history_v2.verify_renewal_retention(root, basis_path) -> dict`
  returns `{"HISTORICAL_IDENTITY_VERIFIED": True, "retained_copy": {"path","sha256"}}`.
- Owner registry: `OWNER_REGISTRY` tuple + `_OWNER_BY_TYPE`, `_ALLOWED_SCHEMA_PATHS` (fixed, no caller).
  O17 entry `("scope","schemas/reader-surface-semantic-review-v2.schema.json","")`.
- Low: `survey_publication_set_v2._is_versioned_record(record) -> bool` (exact pair),
  `._is_versioned_seal(seal) -> bool` (exact pair), `validate_seal` dispatches to
  `_validate_versioned_seal`, `validate_activation_record` dispatches to `_validate_versioned_activation`
  (HIST leaf). `survey_agent_control_v2._is_versioned_record/_is_versioned_seal`,
  `_check_versioned_rows`, versioned branches in `_check_immutable_revalidation_rows`,
  `_check_revalidation_chain`, `_check_revalidation_agreement`, `_resolve_publication_revalidation`,
  `_validate_checkpoint_record`. All legacy/editorial predicates intact.
- Schemas: `versioned-renewal-basis-v2` (`VERSIONED_RENEWAL_BASIS_V1`, `observed_source_bindings` with
  `schema_pointer` type string allows `""`), `versioned-renewal-source-proof-v2`
  (`VERSIONED_RENEWAL_SOURCE_PROOF_V1`, `supported_source_bindings` same shape, `comparison`
  `REUSED_TARGETS` requires `old_manuscript_ref`+`old_build_unit_refs`), `versioned-renewal-source-manifest-v2`
  (`VERSIONED_RENEWAL_SOURCE_V1` + `$defs.buildRecord` with `kind` `VERSIONED_RENEWAL_BUILD_V1`,
  `variant` `REUSED_BUILD` (requires `original_*`+`renewal_tools`+`no_rebuild`, forbids executed keys) /
  `EXECUTED_BUILD` (requires `declared_inputs`+`recipe`+`toolchain`+`outputs`+`exit_code:0`, forbids reused keys)),
  `versioned-renewal-publication-set-v2` (`VERSIONED_RENEWAL_SET_V1`/`SEALED_INERT`, exact 15 roles),
  `publication-surface-revalidation` new `$defs/versioned_activation` + `$defs/versioned_core`
  (Contract8 + impl SHA). All `$ref` local `#/$defs/*`, all objects `additionalProperties:false`.
- On contract contradiction: return precise `file:line` issue before broadening (none asserted as faithful
  until tested exact preds above; only strict unit scope proven).

Stop here. Whole NOT_READY/step4B3 OPEN/audit unstarted/DM021+022 OPEN. Ordinary Commit/Push Human-owned.
