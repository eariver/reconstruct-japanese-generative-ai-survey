# Group H return — high-level operation implementation (H-owned only)

Root selection `astra-implementation-selection.md` read. Contract `d880f53e` stable.
DST `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60` ONLY.
Original22 + R2 fixtures read-only. No candidate/reconstruct commit, no network/clean/reset/raw deletion.
H (author + later lead) implements ONLY root §1 H paths. L/C concurrent drafts preserved; H did NOT edit L/C files.
No agents spawned. No long fixtures/builds/tests until integration freeze/root review.

## 1. H-owned writes (disjoint)

NEW (H):
- `scripts/survey_editorial_publication_v2.py` (1019 lines, full functions, CLI)
- `schemas/editorial-publication-source-manifest-v2.schema.json` (EDITORIAL_PUBLICATION_SOURCE_V1)
- `schemas/editorial-publication-build-record-v2.schema.json` (EDITORIAL_PUBLICATION_BUILD_V1, digest includes input/output refs excludes only self)
- `schemas/editorial-manuscript-spec-v2.schema.json` (EDITORIAL_MANUSCRIPT_SPEC_V1, FULFILLED assertions only)
- `schemas/editorial-toolchain-spec-v2.schema.json` (EDITORIAL_TOOLCHAIN_SPEC_V1, absolute exe, allowlisted argv/env)

EDITED (H, existing R2 overlay preserved):
- `schemas/reader-manuscript-v2.schema.json`: optional `editorial_source={proposal_ref,staged_manifest_ref}` ($defs.editorialSource), required list unchanged (no new required).
- `schemas/reader-surface-gate-v2.schema.json`: `derivation.oneOf` 3→4 (+ `EDITORIAL_PUBLICATION_V1/EDITORIAL_MAIN_BIB_STYLE` with receipt ref). Existing 3 branches verbatim.
- `scripts/survey_reader_publication_v2.py`: `_validate_manifest_semantics` editorial branch (canonical verbatim when absent; P3S `verify_staged_source` proof + same issue/Profile + exact staged trio when present; never seal/activation) + `build_manuscript_manifest(..., editorial_source=None)` (strict shape, added to base before digest).
- `scripts/survey_reader_surface_gate_v2.py`: `_derivation_for_manuscript` editorial branch first (staged proof via P3S verifier, editorial receipt at `P/publication/validated-source-manifest.json`, early scope ref must equal reviewed_surface_path, P1 `_validate_scope` reload shape-checked never postrender-as-preTeX, staged trio/manuscript binding, returns `EDITORIAL_PUBLICATION_V1/EDITORIAL_MAIN_BIB_STYLE`). Existing DIRECT/WEEKLY/LONGFORM branches untouched.
- `scripts/survey_weekly_derivation_v2.py`: `CURRENT_CLOSURE` 8→22 (+ common14 exact, sorted-unique, no overlap).
- `scripts/survey_longform_generated_v2.py`: `CURRENT_CLOSURE` 14→27 (+ common14 minus Gate overlap =13 new).

NOT touched by H (L/C concurrent, preserved):
- L: `survey_publication_set_v2.py` (absent, L drafts), `publication-surface-revalidation.schema.json` (M by L), `editorial-publication-set-v2.schema.json` (?? by L), `survey_agent_control_v2.py` (clean, L drafts).
- C: `survey_stage_validation_v2.py`, `survey_production_v2.py`, `survey_profiled_freeze_v2.py`, `config/survey-production-v2.json`, `survey_orchestrator_v2.py`, `survey_handoff_v2.py`, `survey_human_gate_v2.py`, workflows, P1/P2V/P2R/P3S, R1, wrappers, docs (M/?? by C preserved).
- `quality` generic untouched (only referenced via `QUALITY_SCHEMA=quality-regression-bundle-v2.schema.json` confirmed actual).
- R2 baseline Ms (`reader-surface-semantic-review.schema.json`, `reader_surface_gate runtime scan`, `jgaisurvey.sty`) preserved underneath H edits.

## 2. Full functions (not stubs) + key behaviors

`survey_editorial_publication_v2.py` top-level imports ONLY stdlib + `core` + `schema_gate` (no import-time execution, no top-level cycle). All other deps function-local.

- `validate_editorial_receipt(root,receipt,state)`: inert-before-seal needs no active record; strict State + unchanged accepted research + exact source replay (staged trio bytes + rendered outputs) after activation with NO beforeState hash equality. Calls P2R/P3S historical replay only (no P2V future seal, no current activation). Digest excludes only self.
- `prepare_publication(...)`: P2V `SCOPE_BOUND` current-before → disposable build (real TL2026 toolchain, fixed recipe `lualatex-biber-lualatex`/`latexmk-lualatex`, allowlisted argv no `-e`/shell/output-override, allowlisted env no `GIT_*`/root, `.latexmkrc` recorded) → exclusive `build3` transfer → build-record (recipe_ref hash + input/output refs, `build_sha256` includes all refs excludes only self) → receipt (exact trio, `proposed-publication-authoring` + `accepted-draft-archive`, current_tools closure 22/27) → Reader manuscript (spec coverage `FULFILLED` actual fields, `editorial_source` staged proof). Input specs `P/manuscript-spec.json`, `P/toolchain-spec.json` outside unclaimed `P/publication` (prepare claims absent, refuses same-byte takeover). No semantic/visual PASS producer.
- `finalize_publication(...)`: current-before recheck + all immutable inputs, `quality.validate_checks` (DETERMINISTIC actual evidence, no family PASS) + `build_bundle` (exact source/PDF), supplied QA/schema refs + postrender reviews final exact paths, Gate with early scope (editorial branch), Candidate via actual `publication.build_candidate` (never publisher, no canonical install), seal last (exclusive, 15 roles).
- `validate_prepared_set(...)`: every 15 role existence/SHA/bytes, source/receipt/manifest/bundle/reviews/gate/candidate/build shared refs + external deps + inventory; current research/tool healthy; returns no permission token.
- `activate_publication(...)`: rederives all on paths, P2V fresh before, L `resolve_publication_selection` + retained/current matching via L, new immutable sequence record then State pointer guarded replace (L writer). old/new/unknown classification, primary+secondary errors, no delete unknown, explicit orphan resume, read-only `ALREADY_ACTIVE`, no silent takeover/rollback/synthetic detection. Calls actual candidate APIs only.
- `resume_activation`, `verify_activation_history`, `resolve_publication_selection` (re-export L), CLI `prepare/finalize/validate-receipt/validate-set/activate/resume/verify-history` with `--repo-root/--state/--proposal/--staged-manifest/.../--reason/--executor/--recorded-at`, path roots via containment, refusal exit 2.
- No caller-verified dict; default candidate path never permission (L-owned resolver authoritative).

## 3. Closure / registry (selected 50, no extra edge)

- Weekly 22 (8 old + common14, verified `closure_len=22`), Longform 27 (14 old +13 new, Gate overlap excluded, verified `27`).
- Common14 exact per root §3 (set, editorial_pub, current_authority, 5 new schemas incl. L set, reader-manuscript, reader-surface-gate, revalidation, quality-bundle, candidate, `.latexmkrc`).
- P3S 50 is C-owned (H did not edit); H union assumption = P3S50 + initial tuple, exact count checked in `_editorial_closure_rows` (22/27). AST top-level imports (prior inspect) show H function-local deps (P1/proposal, P2R/retention, P3S/staged, P2V/observer, Reader, Quality, Publication, Gate, Weekly/Longform, L set) are all covered by Weekly/Longform closures + P3S50 + control-roots; NO extra actual edge beyond selected 50 required. If final-code import check finds a new edge, H will return concrete required extension instead of omitting (none found now).
- Registry: H added NO scripts/config to `contract_files` (C owns registration; 5 new semantic schemas to be registered by C per root §3: source-manifest/set/build-record/manuscript-spec/toolchain-spec; implementations stay in closures + `implementation_control_roots`). R1 comment-only Weekly change leaves contract identity unchanged (scripts not in contract_files) — preserved.

## 4. Pure checks (unique namespace, no pollution)

- Script BEFORE: `notes/rephase-1-editorial-operation-implementation/h-pure-checks-20261021T000000Z.sh`
- Raw: `h-pure-stdout-20261021T000000Z.txt`, `h-pure-stderr-20261021T000000Z.txt` (empty), `h-pure-exit-20261021T000000Z.txt` (`0`)
- `py_compile` 5/5 OK (`PYTHONDONTWRITEBYTECODE=1`, `__pycache__` removed after, 0 remain), schema JSON 6/6 OK, closures 22/27 OK, SRC pins `OK 22/22` (original22 untouched), DST `HEAD 409b292/tree 8ce.../detached/4M18A` + L/C concurrent drafts preserved.
- Hashes: `survey_editorial_publication_v2.py 40887b70...`, `source-manifest 494a1d15...`, `build-record b7c82476...`, `manuscript-spec 043ce8a5...`, `toolchain-spec 50b5dc3e...` (full `sha256sum` in check stdout).
- API: 22 defs (`EditorialError` … `main`, exact list in check appendix via `grep ^def/^class`).
- Failures: none in H pure scope. Concurrent L/C diffs + R2 overlay diffs are not H failures and are preserved (see DST status in check stdout). `__pycache__` pollution removed; no derived mirrors, no long fixtures/builds/tests.

## 5. Blockers / integration hold

NONE for L/C continue + lead integrate. Integration needs (not waived): L `survey_publication_set_v2.py` + revalidation branch + set schema + agent wiring; C P3S50 assertion + `contract_files` 5-schema registration + consumer wiring; then lead whole-operation fixtures. H did NOT commit, did NOT edit L/C files, did NOT create source commit, original22 untouched.

**H code return complete. Awaiting root integrate with L/C (H will not independently edit their files).**
