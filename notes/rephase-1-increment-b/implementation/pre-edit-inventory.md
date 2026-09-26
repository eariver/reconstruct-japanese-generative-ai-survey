# Increment B pre-edit inventory and isolation

Recorded 2026-09-22 JST before code edits. Astra approved this bounded inventory. This is implementation evidence, not adoption or audit authority.

## Isolated candidate

- Fixture: `/tmp/jgas-rephase-increment-b-sol-implementation`
- Branch: `codex/rephase-1-increment-b`
- Starting HEAD: `1a9649129d1745fed0b98db46ef15f014407e6fc`
- Starting tree: `5e933aa54034ed227216252a2c8707a59f293acf`
- Parent: `bf32edf98ba8f605169d7188bbc764de74ee4f6e`
- Origin: `https://example.invalid/rephase-increment-b.git`
- Git common directory: local `.git`
- Alternates: absent/empty
- Inherited overrides checked and absent: `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`, `GIT_COMMON_DIR`
- Object files: source 5,134; destination 5,134; destination non-unit hardlink counts 0; shared source/destination device+inode pairs 0; object symlinks 0.
- Tracked index/worktree started clean. Only inherited untracked `scripts/__pycache__/` and `tests/__pycache__/` were present.

## Approved production paths

- New `scripts/survey_weekly_derivation_v2.py`: pure canonical projection/render functions separated from State/checkpoint authority loading and replay validation.
- New `schemas/weekly-publication-source-manifest-v2.schema.json`: strict schema for the existing sole `validated-source-manifest.json` receipt.
- New `scripts/survey_drafting_citation_refs_v2.py`: exact shared extraction of `_ref_rows`/`_refs` semantics.
- `scripts/run_drafting_synthesis_v2_interactive.py`: delegate its existing private citation helpers without changing exact-one resolution or ordered de-duplication.
- `scripts/survey_weekly_semantic_publication_v2.py`: complete canonical input, two-pass review stop, one-object main/bibliography/style rendering and one validated receipt.
- `schemas/reader-surface-input-v2.schema.json`: complete strict `WEEKLY_GENERATED_V2` object.
- `scripts/survey_reader_surface_gate_v2.py`: explicit generated/direct-primary route handling and independent replay.
- `schemas/reader-surface-gate-v2.schema.json`: required narrow derivation block and explicit direct-primary limitation.
- `scripts/survey_reader_publication_v2.py`: forward route/receipt/current State inputs to Gate creation.
- `scripts/survey_agent_control_v2.py`: current-State/checkpoint replay before writing revalidation authority.
- `scripts/survey_stage_validation_v2.py`: current-State/checkpoint replay at both stage admissions while retaining Increment A exact-manuscript checks.
- `templates/survey/jgaisurvey.sty`: default-compatible setters for the small Weekly-visible style text surface; no layout change.

## Approved test paths

- New `tests/test_survey_increment_b_weekly_derivation_v2.py` for the publisher-valid Weekly fixture and dense B contract matrix.
- `tests/test_survey_semantic_publication_v2.py`
- `tests/test_survey_reader_surface_gate_v2.py`
- `tests/test_survey_publication_revalidation_v2.py`
- `tests/test_survey_exact_manuscript_admission_v2.py` only where its narrow A fixtures construct Gate/revalidation records.
- Existing Freeze-stage and Human-Gate revision tests are affected callers through the publication-revalidation fixture; edit only if direct construction requires it.
- Existing cross-package citation-ref tests are required regression coverage for the shared extraction.

Existing A/revalidation fixtures may use explicit `DIRECT_PRIMARY` with exact primary target and an explicit primary-only support limitation. They are not publisher-valid Weekly evidence. Separate tests retain malformed-generated-input rejection and exercise a real schema-valid two-pass Weekly path.

## Intentional non-edits and boundaries

- Keep `schemas/reader-surface-semantic-review-v2.schema.json` unchanged.
- Keep `scripts/survey_bibliography_access_provenance_v2.py` and `scripts/render_article_draft_tex.py` unchanged as exact closure dependencies unless a concrete bounded blocker is found.
- Do not edit global contract-file lists, generic authority/resolver machinery, Release, Freeze, LONGFORM or deferred-maintenance scope.
- Keep accepted upstream implementation basis separate from current renderer/helper/schema/style/current contract identity.
- Freshly self-rehashed receipts cannot authorize changed or uncommitted helper/schema/style bytes or mismatched current-tool identity.
- A checkpoint-bound Draft Result mutation remains an immutable-provenance failure. Semantic annotation separation is demonstrated with separately valid newly bound variants or pure projection.
