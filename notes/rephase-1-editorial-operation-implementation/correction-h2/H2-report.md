# H2 corrective return — full implementation (H-owned only, no L/C edits)

DST ONLY: `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60`
Governing: d880 contract + `astra-implementation-selection.md` frozen interfaces/ownership/closure (§§2–3).
R1 defects: `astra-draft-review-r1.md` ALL (7 H items). L/C authors paused; separate reviewer inspects L/C read-only.
H owns: `survey_editorial_publication_v2.py` + 4 schemas + Reader/Gate runtime/schema + Weeklydrv/Longformdrv/generated/initial-publishers if needed.
Never: L low/agent/set/reval schemas or C/P1/P2R/P2V/P3S/config/consumers/workflows.

## 0. Archive (byte-identical, before H2 edits)

- NEW packet `correction-h2/history/` (not rewrite/delete of prior packets).
- `README.md` (Write, dedicated editor) + byte-identical copies via `cp -a` (preservation, not implementation edit):
  `survey_editorial_publication_v2.py.H1` 40887b70…, `editorial-*.H1` (4 schemas, hashes match H1 report),
  `survey_reader_publication_v2.py.H1` e817…, `survey_reader_surface_gate_v2.py.H1` fade…,
  `survey_weekly_derivation_v2.py.H1` 2d3b…, `reader-manifest/gate.H1` 0d8f…/f10d….
- All H2 implementation edits used dedicated editor (Read/Edit/Write) only; no shell file write/clean/reset/commit/network to DST.
  Archiving `cp -a` was to workspace packet only (byte-identical preservation); no DST shell writes.
- No code import to original src; all focused checks used `PYTHONDONTWRITEBYTECODE=1` + `TMPDIR=/tmp/opencode` (external cache, no source `__pycache__`).
- No long real fixtures/build until root code review; meaningful focused unit tests only (real predicates, not mirror text).

## 1. H-owned writes (disjoint, L/C preserved)

- EDITED (H, 2862 lines, was 1020): `scripts/survey_editorial_publication_v2.py` H2 `b86983cb…` (was H1 `40887b70…`).
- EDITED (H, narrow slices only): `scripts/survey_reader_publication_v2.py` H2 `5febb50c…` (was H1 `e817…`),
  `scripts/survey_reader_surface_gate_v2.py` H2 `0e586d28…` (was H1 `fade…`).
- UNCHANGED (H, already 22 per selection, preserved): `scripts/survey_weekly_derivation_v2.py` (22-closure), 4 schemas (receipt/build-record/mspec/toolspec, no schema shape change needed),
  `schemas/reader-manuscript/gate` (H1 editorial branches preserved underneath H2 trio/verifier fixes in runtime only).
- NOT touched (L/C concurrent, preserved): `survey_publication_set_v2.py`, `survey_agent_control_v2.py`, revalidation/set schemas,
  stage/production/freeze/config/orchestrator/handoff/human-gate/workflows, P1/P2V/P2R/P3S, R1, wrappers, docs.
  Tracked L/C diffs in `git diff --name-only` pre-existed H2 (parallel workers); H2 did not edit those paths (all H2 Edits targeted H files only).

## 2. R1 fixes (all 7, real code, not scaffolding)

1. **Activation/resume (was stubs)**: Deleted `setmod.activate_selection` + `_activate_via_lowlevel` + `hasattr` fictional `write_activation_record`/`resume_activation_record`/`verify_activation_history`.
   H now constructs exact record + uses EXISTING `agent._exclusive_create_record_bytes` + `_atomic_replace_state_bytes` (function-local import, no top-level cycle).
   Derives exact original checkpoint/supersedes/latest legacy anchor (via `_build_anchor_chain` + `setmod.derive_canonical_anchor`),
   before_active7+Candidate (via `resolve_publication_selection` effective7/candidate_ref + `before_active_digest`),
   proposal retained State equality (basis state_ref == current State bytes + retained COPY via L validation),
   canonical record seq (`_next_record_seq` via profile source_root + `publication-surface-revalidation-rN.json` + lstat, no leading zeros),
   expected State new pointer only (`publication_revalidation_provenance` sole mutation, no canonical rewrite).
   Read-only `ALREADY_ACTIVE` does full strict State (`agent.validate_agent_state`) + full set; orphan resume revalidates current-before + record bytes;
   primary+secondary errors with observed old/new/unknown, never deletes referenced/unknown. Genuine P2V `SCOPE_BOUND` fresh at both prewrite boundaries
   (before record, before State). L readonly (no fictional methods, no silent fallback; missing helper reports exact need to root).

2. **Receipt (was file-hash + comments)**: Full public contract independently (no caller delegation).
   Strict State (`agent.validate_agent_state`, no Gate/receipt recursion) + route derive NEW authoring (`proposal proposed.authoring_input_ref`)
   + unchanged accepted Draft (initial receipt `drafting-authored-archive` via `basis.generated_receipt_ref`, exact path/sha) + current_tools exact set
   (22/27 sorted-unique, path==name, SHA==current bytes, contract==`contract_identity`, commit ancestor via `git cat-file/merge-base`, no recency claim)
   + actual P3S historical proof (`verify_staged_source` typed `{result,proposal_ref,staged_manifest_ref,observed_refs,measured}`, `RETAINED_SET_VERIFIED`, no P2V/seal)
   + early scope binding (scope `reviewed_surface` == receipt `reviewed_reader_input` == proposal `proposed_reader_ref`, `editorial_correction_scope WITHIN_APPROVED_AUTHORITY`,
   `before_reader` == basis `active_reader_input_ref`, never postrender-as-preTeX) + exact canonical reader bytes/staged3 replay
   (staged `outputs={main,bibliography,style}` NOT primary, no `staged_refs` alias, main→primary mapping, file bytes + byte_count at final boundary).
   No beforeState hash equality after activation. Verifier dict shape is actual source (observed_refs/measured, not guessed `issue_id/outputs`).

3. **Prepared set (was hash + receipt, _build_only bypass, missing-schema fallback)**:
   Removed public `_build_only` param (no bypass). Requires strict schema (no fallback, L set schema must exist).
   Fully validates all 15 roles (exact `file_ref`, SHA/bytes at final boundary, closed inventory, staged4 vs build3 separate, no dup paths),
   strict schema, no deps bypass, receipt (full above), actual manuscript (`validate_manuscript_manifest`), bundle (`validate_bundle` + external deterministic result refs pinned),
   external supplied reviews (`validate_review_record` + PASS, never synthesized), Gate (`validate_reader_surface_gate` + editorial derivation),
   Candidate (`validate_candidate` + cross-binding), build record (schema + digest including inputs/outputs), PDF/log/digest (bytes + page-count via bundle/Candidate),
   current research (seal issue/Profile == strict State), exact cross-refs (proposal/staged/build/manuscript/bundle/reviews/Gate/Candidate/build agreement),
   closed inventory + external check results. Valid inert set needs no active pointer, but all current proofs still apply. Returns no permission token.

4. **Safe paths (was resolve-before-check)**: Raw-first lexical containment (`_lexical_rel` rejects absolute/`..`/`.`/empty/backslash before resolve),
   then `core.repo_local_path`, then held-ancestor checks via `os.lstat` (no follow, refuses symlink/FIFO/socket ancestors + non-dir),
   leaf `lstat` refuses symlink/FIFO/socket (no laundering, no FIFO blocking). Bounded regular-file reads (`_read_bytes_bounded` via `O_RDONLY|O_NOFOLLOW`,
   size bound 20MB, short-read loop). Source/ancestor identity + expected bytes at final boundaries (not only before op).

5. **Exclusive writers (was check-then-write/rename, unlink unknown tmp)**:
   True `O_CREAT|O_EXCL|O_NOFOLLOW` (now `O_RDWR` for fd readback), no prior exists-check trusted, no tmp+rename (which can overwrite race winner),
   short-write loop/fsync/fstat identity/seek+readback through same fd (never stat-after-close claim), final pin (re-read via safe + SHA).
   Preserves owned partial/unknown (never unlinks unknown), primary+secondary errors. Existing `write_json` builders (non-exclusive) adapted at owned entry:
   H-owned Reader/Gate builders still use `write_json` internally, so H uses guarded intermediary staging (system temp outside publication inventory,
   repo-relative refs so no review-target rebinding) + validate temp via actual validators + exclusive transfer to final + own-temp cleanup only if identity+bytes match.
   Quality/Candidate (generic, not owned) same temp+validate+exclusive pattern (exact serialization via actual validated inputs + schema, no hash blessing, no autogenerated PASS).
   Build3 transfer uses pinned known bytes + exclusive + final readback (no false glob CAS).

6. **Build (was trio guess, ignored exe, ambient env, rmtree, blacklist, truncation, glob CAS)**:
   Fixed exact trio (`outputs.main/bibliography/style`, NOT primary, no `staged_refs`), absolute exe + companion (`biber`/`latexmk` in same bin dir, regular-file, no PATH/shell),
   fixed exact argv (allowlisted tokens only, no `-e`/`-shell-escape`/`-output-directory`, no shell metachars), allowlisted env only
   (`TEXMFHOME/TEXMFVAR/TEXMFCONFIG/SOURCE_DATE_EPOCH/TZ/LANG/LC_ALL`, no `GIT_*`/root overrides, no ambient `os.environ` merge),
   recipe `.latexmkrc` hash copy pinned before/after (input-copy checks), source inputs unchanged pre/post (bounded pins),
   real executable+companion resolution, required log predicates + PDF pages (`pypdf strict`, >=1, no 1-fallback), digest.
   Preserves failed build root + full raw (no `rmtree`, no `[-4000:]` truncation; full stdout/stderr up to 1MB + `full_raw` list, tmpdir path in error for manual recovery).
   Exclusive build3 transfer (pinned known bytes + fd readback + final SHA/size, no glob CAS).

7. **Finish/prepare (was invented arch names, guessed trio, synthetic PASS comments)**:
   Uses actual typed P3S (`verify_staged_source` typed return) + P2V (`SCOPE_BOUND` fresh at prewrite, not cached) + new schemas consistently.
   Pre-review manuscript final bytes first (exclusive temp+transfer, validated via `validate_manuscript_manifest`); supplied reviews never synthesized
   (persisted files only, `validate_review_record` + PASS, Gate early-scope binding, Candidate via actual `build_candidate`/`validate_candidate`, never publisher/canonical install).
   Full lifecycle possible with existing generic API outputs (no comments claiming it). New functions work with ACTUAL existing schema/types
   (staged `main` vs receipt `primary`, bundle `source/pdf`, candidate `reader_manuscript/source/pdf/quality_bundle/semantic_review/visual_review`, etc.; no guessed field names).

## 3. Reader/Gate narrow fixes (H-owned slices, no old-branch relaxation)

- Reader `_validate_manifest_semantics` editorial branch: fixed verifier shape (proof has no `issue_id/outputs/staged_refs`; checks `result==VERIFIED` + `proposal_ref/staged_manifest_ref` + manifest issue),
  fixed trio to `outputs.main/bibliography/style` (NOT primary, no `staged_refs` alias, main→primary mapping). Existing DIRECT/WEEKLY/LONGFORM branches untouched.
- Gate `_derivation_for_manuscript` editorial branch: fixed staged proof shape + trio mapping (main→primary) + early scope reload via actual scope JSON
  (`reviewed_surface` == receipt `reviewed_reader_input`, `editorial_correction_scope WITHIN_APPROVED_AUTHORITY`, never postrender), plus receipt-vs-staged trio check.
  Existing DIRECT/WEEKLY/LONGFORM branches untouched.

## 4. Closure/registry (frozen per selection, no +unknown)

- Weekly 22, Longform 27 (common14 exact, sorted-unique, no overlap), verified `len==22/27` in `_editorial_closure_rows` + focused checks.
  P3S 50 is C-owned (H did not edit; H union assumption = P3S50 + initial tuple, exact count checked in receipt).
  H added NO scripts/config to `contract_files` (C owns registration; 5 new semantic schemas to be registered by C per selection §3).
  R1 comment-only Weekly change leaves contract identity unchanged (scripts not in `contract_files`) — preserved.

## 5. Focused tests (bytecode-external, no source pollution, no long fixtures/build)

- `PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/opencode` (external cache), no `__pycache__` in source (verified 0 after).
- `py_compile` 3/3 OK (`survey_editorial_publication_v2.py` H2 2862 lines, Reader, Gate).
- Focused real-predicate checks (not mirror text):
  - `_lexical_rel` refuses absolute (`/etc/passwd` → `EditorialError`) PASS, refuses `../outside` PASS.
  - `_exclusive_write_bytes` creates + refuses second (collision, no takeover) PASS, fd readback matches PASS (fixed `O_WRONLY`→`O_RDWR` bug found + fixed in H2).
  - `_editorial_closure_rows` Weekly 22 PASS, Longform 27 PASS (exact, sorted-unique).
  - `ALLOWED_ARGV_TOKENS` excludes `-e` (allowlist, not blacklist-only) PASS, includes `main.tex` PASS; `SEAL_ROLES` 15 PASS.
  - AST/code audit: no `setmod.activate_selection`/`write_activation_record`/`resume_activation_record`/`verify_activation_history` calls PASS,
    no `core.write_json`/`target.write_bytes`/`shutil.rmtree` in H module PASS, no `_build_only` param PASS (only docstring mention of removal),
    `staged_refs` only in comments (NOT primary alias) PASS.
- Failures retained: H1 initial bugs (stubs, trio `primary` guess, `proof.get(issue_id)`, `_build_only`, `hasattr` fictional, `resolve→launder`, `check-then-rename`, `rmtree/truncation`, `hasattr(..._exact_pdf_page_count) else 1`) are preserved in `correction-h2/history/*.H1` + H1 report; H2 does not overwrite history.
- No long real fixtures/build until root code review (per instruction); no authority execution claimed.

## 6. Diff/API (exact)

- NEW (untracked, H2): `scripts/survey_editorial_publication_v2.py` 2862 lines `b86983cb…` (was H1 1020 lines `40887b70…` in history).
- EDITED (H): `survey_reader_publication_v2.py` H2 `5febb50c…` (+trio/verifier fix), `survey_reader_surface_gate_v2.py` H2 `0e586d28…` (+trio/verifier/scope fix).
- UNCHANGED (H, preserved): Weekly 22-closure, 4 schemas (no shape change), Reader/Gate schemas (H1 branches preserved).
- Public API (contract §6, no caller-verified dicts, path args repo-contained):
  `prepare_publication(root,state_path,proposal_path,staged_manifest_path,manuscript_spec_path,toolchain_spec_path,recorded_at)->prepared_paths`
  `finalize_publication(root,state_path,proposal_path,staged_manifest_path,deterministic_checks_path,semantic_review_path,visual_review_path,recorded_at)->set_ref`
  `validate_editorial_receipt(root,receipt_path,state_path)->receipt`
  `validate_prepared_set(root,state_path,set_path)->validated_set` (NO `_build_only`)
  `activate_publication(root,state_path,set_path,reason,executor,recorded_at)->{ACTIVATED|ALREADY_ACTIVE,record_path,state_path,observed}`
  `resume_activation(root,state_path,record_path)->{RESUMED|ALREADY_ACTIVE,record_path,state_path,observed}`
  `verify_activation_history(root,record_path)->historical_result` (inert/historical/current-active distinct, no eligibility claim)
  `resolve_publication_selection(root,cfg,state)` (re-export L).
- CLI: `prepare/finalize/validate-receipt/validate-set/activate/resume/verify-history` with `--repo-root/--state/--proposal/--staged-manifest/.../--reason/--executor/--recorded-at`, path roots via containment, refusal exit 2, stdout JSON only.

## 7. Cross-group needs (no detached helper-only completion)

- L: No missing helper for H2 (all frozen `validate_seal/validate_activation_record/derive_canonical_anchor/before_active_digest/resolve_publication_selection` present; H reports exact need if missing, no silent fallback).
  H did NOT edit L files; L concurrent drafts preserved. No `resolve_stage_artifact_path` needed by H (H uses `resolve_publication_artifact_path` + `resolve_publication_selection` only).
- C: Needs C to provide P3S exact50 assertion + `contract_files` 5-schema registration (`pipeline` 62→67) + consumer wiring (already in C report, H did not edit C files).
  H used guarded temp+exclusive for quality/Candidate (generic, not owned) without editing C builders; if root prefers concrete safe-builder extension (exclusive `write_json` in quality/publication),
  H requests it (exact extension: `O_EXCL|O_NOFOLLOW` + fd readback in `build_bundle`/`build_candidate`, no semantic change) — H did not edit those paths.
  C P2V `receipt_kind` caller-policy removal (per R1 integration) is C-owned; H passes `None` (prepare/activate before-eligibility only), no `receipt_kind` invention.
  Initial publishers `DRAFT_COMPLETE`-only + revised refusal are H-owned if needed (untouched in H2; H requests root confirm if initial-publisher edits required, no unrelated renderer edits).
- Lead/root: Awaiting root code review before authority execution (no long fixtures/build). H2 is complete real code (not scaffolding); integration hold: combined source freeze + independent implementation review + eventual whole-candidate audit remain OPEN.

**H2 code return complete. Awaiting root review (no H-side authority execution).**
