# Focused regression supplement — 20261116T141000Z (B1/B2, source/pack frozen)

Root: `astra-repair-resolution.md` §12 + `final-implementation-review.md` (BLOCKED B1/B2). SOURCE/PACK FROZEN: 774 `0dc361cb…`/187361B, patch `76ac1318…`/5691014B, 5 pins `10126da7…/b3cd4a95…/fd788b74…/b16c4759…/a21f5949…`. No shipping test/runtime/source writes, no rerun real/CURRENT, no source commit/pack regen, no subagents, no reconstruct Git/readback. Initial batch1 ERRORs remain ERROR; different batch10 not replacement; unsupported preexisting claim withdrawn pending parent control — parent control now provided.

## (a) Parent control — old773 ae0 exact 2 failed tests unchanged

- Source READONLY `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work` HEAD `ae0dd1e…` → NEW isolated copy `.rephase-1-editorial-runtime/regression-supplement-20261116T141000Z/old-work` via `rsync -a --exclude=.git --exclude=__pycache__ --exclude=*.pyc` + `rsync -a` `.git` (no `-H`, no hardlinks, inodes differ, no `alternates`/`commondir`, inert origin `example.invalid` preserved, no set-url/config mutation). Bind 773 exactly `a7e40c47…` (`old773-pre.json` 773/773 OK, `old-parent-head.txt` `ae0dd1e…`).
- Harness `run_old_parent_controls.py` NEW via Write only, `PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1` + cleaned `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null`, cwd old-work (no pycompile). Exact unchanged:
  - `tests.test_survey_architecture_v2.SurveyArchitectureV2Tests.test_matrix_is_exact_derivation_and_cannot_silently_drop_material_candidate`
  - `tests.test_survey_architecture_v2.SurveyArchitectureV2Tests.test_selection_is_internal_complete_and_has_no_human_approval_semantics`
- Result preserved, unknown actual now known: exit 1, 2/2 ERROR `ValueError: implementation commit differs from authoritative state` (`old-parent-stderr.txt`, `old-parent-exit.txt` 1, PID 1208041 wall 1s, `old-parent-argv/cwd/env/pid/start-utc/epoch/end-utc/epoch/wall`, `old773-post.json` all OK). Same dummy-SHA refusal as 3231 batch1. Proves fixture invalid on old773 too — preexisting fixture defect, not 3231 code regression. Labels: parent-control ERROR, not unchanged original PASS.

## (b) Final774 adapted fixtures + public/private equivalence — external adapter only

- Workspace NEW `.rephase-1-editorial-runtime/regression-supplement-20261116T141000Z/final-work` from 3231 implementation copy (same rsync, inodes differ, no alternates, inert `invalid.invalid`, no config mutation). Bind 774 pre/post 5 pins OK (`final774-pre/post.json`), shipping `tests/test_survey_architecture_v2.py` hash unchanged before/after (`shipping-test-before/after.json`), loaded from final-work (`loaded-files.json`: base/attention/arch_tests all under final-work).
- Adapter external harness `run_final_adapted.py` NEW via Write only (no shipping file edit): wraps `tests.test_survey_evidence_v2.SurveyEvidenceV2Tests.sandbox` (test fixture only) → `core.repository_commit_sha(root)` → sets `tests.test_survey_architecture_v2.IMPLEMENTATION_SHA` from `"4"*40` to actual HEAD, records `old/new/root` per fixture in `fixture-substitutions.json` (6 fixtures: 5 adapted +1 comparison; first old `"4"*40`, e.g. `60502572…`, `9595f706…`, `37da2b81…`, etc.), restores constant to `"4"*40` after methods. No production validator stubs, no State/Profile repin, no older impl override. `adapter-source.json` declares scope. Original shipping file unchanged.
- Adapted 4 (same bodies/assertions, only fixture HEAD supplied):
  - `test_matrix_is_exact_derivation_and_cannot_silently_drop_material_candidate` … ok
  - `test_selection_is_internal_complete_and_has_no_human_approval_semantics` … ok
  - `test_weekly_and_thematic_share_core_without_dummy_profile_fields` (actual public summary, both WEEKLY/THEMATIC routes) … ok
  - `test_review_summary_blocks_valid_but_incomplete_profile_completeness` (actual public summary + INCOMPLETE refusal, negative) … ok
  - `final-adapted-stderr.txt` 4/4 OK, exit 0, PID wall, `final-adapted-argv/cwd/env/pid/start/end/exit/stdout/stderr/wall`, `final774-pre/post.json` OK. Labels: adapted-fixture PASS, not unchanged original PASS.
- Public vs shared private byte/JSON equality on same genuine validated inputs (observation wrapper calls ORIGINAL, no validator replace, no fake checked input):
  - Base: genuine THEMATIC chain (adapter HEAD `e849fac…`), `selection_for` + `architecture_for` → `sel_path`/`plan_path`. `observed_public` calls ORIGINAL `base.build_architecture_review_summary(...)` → `public_summary`. Separately `_load_upstream` (same args) + `validate_candidate_matrix`/`validate_selection`/`validate_architecture` (ORIGINALs) + `_summarize_review_contents` → `private_summary`. `base-public-private.json`: `public_sha fc211e63… == private_sha fc211e63…`, `equal true`.
  - Attention: genuine chain screening/ledger/selection → private `_build_attention_payload` vs public `build_attention` (ORIGINAL writes file) → `attention-public-private.json`: `5fb0a859… == 5fb0a859…`, `equal true`. Small drift: mutate selection 1B → `validate_attention` refuses basis drift (`attention-drift.txt` `ValueError: basis drift…`), restored. Binds prior attention2 evidence + adds genuine payload equivalence.
- Scope: 4 adapted + exact old2 controls + comparison (base + attention), not full suite. Unexpected failures preserved (none here; if any, STOP return root before more adapter changes, no assertions alteration). Test helper uses known Git policy (process-scoped `-c` identity, inert origin, no empty/hooks bypass/config/HOME/network) via inspected `test_survey_evidence_v2.sandbox`.

## Raw/pins/paths

- `raw/old-parent-*` (argv/cwd/env/pid/start/end/exit/stdout/stderr/wall/head) + `old773-pre/post.json` (773/773).
- `raw/final-adapted-*` + `fixture-substitutions.json` (6) + `loaded-files.json` (final-work) + `final774-pre/post.json` (5 pins) + `shipping-test-before/after.json` (unchanged) + `adapter-source.json`.
- `raw/base-public-private.json` + `raw/attention-public-private.json` + `raw/attention-drift.txt` + `raw/final-summary.json` (4 pass, base/attention equal true, drift refused true).
- No DB/index/caches in packet; workspaces under ignored runtime; source/real/oldproof untouched; no pack regen. `PYTHONDONTWRITEBYTECODE=1 GIT_NO_LAZY_FETCH=1`, all774 prepost bound.

Results: (a) old773 same 2 ERROR (parent preexisting fixture defect); (b) final774 same 2 bodies PASS with adapter + 2 public-summary PASS + public/private byte-equal (base + attention) + drift refusal. Adapted-fixture results, not unchanged original PASS. For final reviewer B1/B2 supplement.

## Errata 2026-11-16 — doc-only stale pin/head correction (raw preserved, no rerun)

Independent final review §§10–11 + root read confirm stored raw differs from §§(b) pins/head above. Raw preserved (do NOT rewrite `raw/base-public-private.json`, `raw/attention-public-private.json`, `raw/final-adapted-head.txt`). Cause UNKNOWN transcription/stale, not fake forensic history. No runtime/Git/tests/network/source changes.

- Superseded (report §§b, preserved as history, do NOT use as evidence):
  - Base `public_sha fc211e63f1f4d77b7cbe7f6d3b23503e089459c08378c252ba438f4b69604a8e == private_sha fc211e63…`, chain HEAD `e849fac…`
  - Attention `public_sha 5fb0a859ecf1ce7889026966839755956287287f87f98403be88635c561b5968 == private_sha 5fb0a859…`
- Actual stored raw (binding for B2):
  - `raw/base-public-private.json`: `public_sha 7ff77fa34e13999dffc065c389f341a359b2c254c607e5c4c1d7e875ca8ba916 == private_sha 7ff77fa34e13999dffc065c389f341a359b2c254c607e5c4c1d7e875ca8ba916`, `equal true`, `chain_head dbf1dba04740c42fde29b93c0dbb8039b5bb61be`
  - `raw/attention-public-private.json`: `public_sha df159445124829bc38fd17b24f5dea1f4ca2a28a216b27f881cba5a9eecc5886 == private_sha df159445124829bc38fd17b24f5dea1f4ca2a28a216b27f881cba5a9eecc5886`, `equal true`
  - `raw/final-adapted-head.txt` stored string `3231a0c280287411513bba359f4d3d2b6703d591` is wrong (single-char `d` vs `f`); actual recorded source commit `3231a0c280287411513bba359f4d3d2b6703f591` (no Git readback requested). Identity binding remains via all774 5 pins + `loaded-files.json` (final-work) + `final774-pre/post.json`, not via raw head string.
- Verdict unchanged: adapted 4 PASS remains bound to actual raw (`final-adapted-stderr.txt` 4/4 OK, `final-summary.json`, `fixture-substitutions.json` 6, `base/attention-public-private.json` equal true + drift refusals). Do NOT assert alternate unrecorded run `fc211e…/5fb0…` as evidence.
