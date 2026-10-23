# Group L correction R1 — changed hash/diff report (owned paths only)

DST: `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60`
HEAD (detached, unchanged): `409b292756dd1277b9dfae87679934c0d2ce251c`
R1 initial bytes archived in `correction-r1/initial-bytes/` (hashes equal the
R1 pins). This report covers the correction-R1 working tree. No H/C paths
touched; no commit/push/reset/clean/raw-delete/network. Other DST
modifications/untracked files from parallel H/C workers are NOT included.

Owned paths:
- `scripts/survey_publication_set_v2.py` (NEW, rewritten)
- `schemas/publication-surface-revalidation.schema.json` (branch edit, unchanged this round)
- `schemas/editorial-publication-set-v2.schema.json` (NEW, unchanged this round)
- `scripts/survey_agent_control_v2.py` (branch/resolver/raw wiring)
- `tests/test_survey_publication_set_v2.py` (NEW, expanded behavioral)

## SHA256 (correction-R1)

- schemas/editorial-publication-set-v2.schema.json: `7beebcef48d7777144f7df7ce3fddc27c0d39df685fdc49cbfdd7d798c7e61e9` (unchanged)
- schemas/publication-surface-revalidation.schema.json: `2d0a9499af0456c071f88b5deb2971b7abbee838ed73cf5a5595ae418f41e9ed` (unchanged)
- scripts/survey_publication_set_v2.py: `2ef92fed6f1a43b18f55f6da9b522ba672f58dda2a34c29f127aebb58e49eff2` (was `6e753dc3…`)
- scripts/survey_agent_control_v2.py: `12995a8415f8b2ee28fab783b1688f2b3012aadb045f03ad95cf7e5be3d8f78d` (was `9ef94dfb…`)
- tests/test_survey_publication_set_v2.py: `0cef7a6b648a60b93bd403bef7115ff8417db3c8fd3bff925d5728bd899eeda7` (was `f7cf2662…`)

Line counts: seal schema 92, revalidation schema 246, set module 1687,
agent 2692, tests 919.

## What changed vs R1 (by review item)

- `resolve_stage_artifact_path(root,cfg,state,profile,name,template)` ADDED
  (frozen mandatory; candidate is State-aware with canonical-token check,
  other names retain exact template behavior + raw alias refusal). Agent
  `_validate_stage_artifacts` now routes ALL roles through it.
- Raw-first I/O layer ADDED in low module (lexical traversal refusal,
  ancestor lstat no-follow walk, FIFO/socket/device/dir refusal, O_NOFOLLOW
  reads, strict duplicate-key JSON before actual jsonschema validation).
  All pubset file reads use it; agent trust-boundary loads (records,
  checkpoints, prior, approvals, reviews, State, freeze/manifest, profile,
  results) switched to it. Global schema module untouched.
- `canonical7` is now refs-only (no live expectation); legacy selection fully
  validates live effective refs (SHA plus byte_count for superseded),
  original-union equality, contract-path agreement, no missing-seven fill.
  Effective7/canonical7 rows are exactly `{path,sha256,origin}` (matches P1).
- `before_active_digest` enforces exactly seven roles, unique identities and
  paths, valid refs, extras/missing refused.
- Activation verifies proposal/staged/retention schemas; `state:authority`
  unique COPY row with `<P>/retained/before/<path>` dest mapping; retained
  State COPY bytes; retained-State profile ref to unique KEEP Profile row;
  Profile/retained-State labels vs proposal; proposal dir bound to KEEP
  Profile source_root plus proposal_id; before-Candidate nullable only when
  the canonical Candidate is absent (first activation) and equal to the
  predecessor seal Candidate (repeated); candidate PDF binds before-effective
  PDF; digest recomputed (no fill for non-cumulative).
- Seal enforces exact P namespace (fixed filenames), staged
  `outputs.{main,bibliography,style}` mapping to
  `validated-source/bibliography/style` (`primary`/`staged_refs` refused),
  pdf-digest opens with the PDF SHA, receipt/manuscript/bundle/reviews/Gate/
  Candidate/build-record cross-refs and result identity (no high-module
  calls), page_count agreement, build-record §6 keys with recipe/declared
  I/O binding.
- Agent chain validates EVERY linked editorial activation fully
  (`validate_activation_record` on link files; low stays readonly, no
  recursion), (path,sha256) cycle keys, total depth 32, later-legacy refusal.
  `_resolve_checkpoint_artifact` validates the checkpoint with the proper
  active revalidation (legacy mapping restored post-R1) and only then
  projects the seven roles via the fully-validating selection.
- Mode probe `resolve_publication_mode` (pointer branch only, no live
  enforcement) drives `assert_canonical_publication_mode` writer refusal;
  `require_active_or_canonical` keeps full live enforcement for read paths.
- No `14/17` summary counts in code; no P3S-closure-count assumption anywhere.
- H-owned receipt/build schemas are NOT imported and their files are NOT
  schema-pinned by L; L enforces contract-frozen structural keys only.
