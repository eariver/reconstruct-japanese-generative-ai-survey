# R1 integrated admission CORRECTION — checked editorial admission / full-promotion coherent contract decision + implementation task

> Author-side architecture Co-Worker correction. NOT independent review. NOT independent PASS.
> Preserves original `integrated-admission-contract-analysis.md` (do not edit original; this file corrects §§2/3/7 per `astra-first-review.md` 8 blockers).
> Tool disclosure: task asked for `apply_patch`; environment has no `apply_patch`. Used dedicated `Write` for this new file + `bash`/`Read` for source tracing only. No code/tests/git writes/network/production mutation.
> Source read-only: `/tmp/opencode/jgas-roadmap-r1-20261018T163842Z/candidate-partial-b40de60` = real detached `409b292756dd1277b9dfae87679934c0d2ce251c` / tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2` + final21 (3M18A, static21 `1c0e339c`). No source mutation, no test execution, no restore duplication (restore/current-source verification owned by separate evidence worker: `restoration-procedure.md`, `restoration-manifest.json`, `current-source-verification-20261019T000525Z/`; numbers below are re-reads for design, not new restore proof).

## 0. Corrected decision (single coherent selection, no punt)

**SELECT: `REVIEWED_EDITORIAL_CORRECTION` as second `reason_class` inside the EXISTING `publication-surface-revalidation` chain + bounded 3-operation owned transaction (`prepare` / `install` / `finish`) with explicitly acknowledged temporary-invalid-live window. REJECT: parallel `editorial_admission_provenance` pointer + separate `editorial-admission-record` schema (prior §§2.5/7.1), all-versioned-generation-then-pointer-switch, status-quo gap, broad authority replacement, helper-only slice.**

Why this is the only coherent closure (detail in §§2–5,9):

- Existing chain already has consumers for every predicate R1 must close: `resolve_active_publication_revalidation` / `_resolve_publication_revalidation` (`survey_agent_control_v2.py:1084-1187`), `_check_immutable_revalidation_rows` (`:847-949`), `_check_revalidation_chain` (`:952-1017`), `_check_revalidation_agreement` (`:1020-1081`), `_validate_agent_state` / `validate_agent_state` (`:~strict public validation`), `built_checked_pending_publication_basis` + `_collect_pending_rows` + `_verify_pending_binding` (`:784-808,:711-743,:746-781`), Weekly `load_derivation` pending_basis branch (`survey_weekly_derivation_v2.py:load_derivation`), stage `validate:reader-publication` DRAFT_COMPLETE semantics (`survey_stage_validation_v2.py:_validate_stage_semantics` DRAFT_COMPLETE branch), publication `validate_candidate` / `build_candidate` / Freeze preflight (`survey_publication_v2.py:749-814,:668-746,:171-245`). A parallel pointer has zero of these consumers; prior §§2.1/7.1 left it unconsumed (Astra blocker 1,5). Fixing that would require new State field + ≥8 validator/call-site edits with no coverage gain.
- Live 3-file `O_EXCL` is impossible (healthy before bytes exist). Prior §2.5 claimed exclusive 3-file ownership. Correction uses owned `temp+replace` from known expected-old bytes (controller precedent `_atomic_replace_state_bytes:1666-1770`), never `O_EXCL` on existing, never truncate/overwrite/rollback/cleanup (Astra blocker 2).
- `P2V-before` cannot be re-run after the before-set changes and still demand same-before equality. Prior §2.5/§7 demanded `P2V×2 stable-fact` across install with second-map full equality excluded only loosely. Correction splits: `P2V-before` once in `prepare` (before-context), public live validators + `verify_retention`/`verify_staged_source` re-reads in `finish` (after-context), no second same-before claim (Astra blocker 2).
- Receipt/Gate/manuscript cycle cannot be closed by “call existing validators” alone. Longform `validate_receipt:665-758` pins canonical `survey_root/{main.tex,references.bib,jgaisurvey.sty}` (`:707-714`), canonical `source_root/publication/v2/{reader-surface-input-v2.json,interactive-semantic-publication-input.json,validated-source-manifest.json}` (`:720-730`), strict `load_derivation_for_readback` (`:698-706`), deterministic FILE-byte replay (`:734-757`). Gate `_derivation_for_manuscript` (`survey_reader_surface_gate_v2.py:_derivation_for_manuscript`) re-runs that receipt and demands `receipt.outputs == manuscript.primary+supports`. `validate_reader_surface_gate` (`:validate_reader_surface_gate`) always runs full derivation replay after `_inspect_gate_record` (inspection alone is never admission). `build_manuscript_manifest` / `build_review_record` / `build_bundle` all refuse overwrite (`survey_reader_publication_v2.py:build_manuscript_manifest: if output_path.exists: refuse`; `build_review_record: if output_path.exists: refuse`; `survey_quality_v2.py:build_bundle: if output_path.exists: refuse`; `survey_publication_v2.py:_write_immutable: divergent overwrite refuse`; `_install_owned_json:502-518 divergent refuse`). Correction therefore defines versioned-QA-generation-then-owned-install + live revalidation, with exact context restrictions and no generic ignore/pending bearer (Astra blocker 4).
- `3A/0M` with “existing changes are blockers” is incoherent: the design cannot pass without consuming schema+controller. Correction gives exact impact table (§5) with no path-count budget; every touched path has a caller reason (§2.3).
- Candidate confusion corrected (§2.11): `candidate_selection_gate.py` (Evidence Selection, HOLD/REJECT roles, `validate(selection,matrix)`) is NOT `schemas/publication-candidate-v2.schema.json` + `survey_publication_v2.validate_candidate/build_candidate` (Publication Candidate, `READY_FOR_PUBLICATION_PREVIEW`, manuscript/source/pdf/bundle/semantic/visual binding). P1 `:822-862` observes the latter. Healthy same-before observed candidate must be recorded as `OBSERVED_HEALTHY_SAME_BEFORE`, not blanket-rejected; supersession has exact pending/no-approval/adoption predicates; replacement is normal `build_candidate` after rebind; Candidate is never publisher.

If any essential contradiction below proves infeasible during R2 implementation, R2 must return explicit `NO-GO` with exact interface difference + scoped alternative (e.g. “live PDF build infeasible in this env → no admission; alternative X loses Y, therefore whole completion stays OPEN”), never “defer predicate to next helper analysis”.

## 1. Actual-source facts re-read for this correction (hotspots)

All paths relative to restored DB root. Line numbers are this source; workspace files are different overlay.

**Lifecycle/State hardness.**
- `scripts/survey_production_v2.py:32-44` `LIFECYCLE` 11 states; `transition_state` (cf. `survey_production_v2.py:transition_state`, Astra note 935–985 in workspace numbering) allows only `current+1`, same-State/backward refused. Same-State supersession does not exist. This is shared DM021 (post-`VALIDATED_DRAFT`) / DM022 (pre-Architecture `EVIDENCE_REVIEWED`) hardness, stages differ.
- `schemas/survey-production-state.schema.json:1-160` — `additionalProperties:false`, `publication_revalidation_provenance` is optional `nullableAuthority` (`:77`), no editorial pointer field exists. Adding a parallel pointer would require State schema edit + every `_validate_agent_state` / `_verify_pending_binding` / `_resolve_publication_revalidation` consumer edit with zero current coverage.
- `scripts/survey_agent_control_v2.py:45` `REVALIDATION_REASON_CLASSES={"REVIEWED_CORE_CHANGE"}` single. `schemas/publication-surface-revalidation.schema.json: reason_class const REVIEWED_CORE_CHANGE`, `lifecycle const VALIDATED_DRAFT`, `establishment` pre-decision sanctions (`:lifecycle VALIDATED_DRAFT, architecture_review approved, publication_preview pending, freeze pending, release pending`).

**Pending/allowed rows.**
- `survey_agent_control_v2.py:685-693` `_publication_revalidation_roles`: stage `DRAFT_COMPLETE` 6 artifacts (`reader-manuscript`, `validated-source`, `publication-pdf`, `quality-regression-bundle`, `semantic-review`, `visual-review`) + `reader-surface-gate` canonical `source_root/publication/v2/reader-surface-gate-v2.json`. These 7 are the ONLY rows `_collect_pending_rows:711-743` can mark changed; any other changed path → `changed noncanonical or upstream role/path` refusal. `require_change=True` default demands ≥1 changed publication byte.
- `survey_agent_control_v2.py:696-708` `_pending_conditions`: `VALIDATED_DRAFT` + architecture approved + publication_preview pending + no preview provenance + freeze/release/publication_preview checkpoints pending + exception inactive. `built_checked_pending_publication_basis:784-808` builds fresh checked context from actual State/checkpoint/current files; `_verify_pending_binding:746-781` rechecks State path canonical (`source_root/production-state.json` via `state_authority.authoritative_filename`), State bytes, config bytes, HEAD, validation ref, row snapshot, predecessor pointer. `revalidate_publication_surface:1773-2201` snapshots `pending_basis` at entry, derives `superseded` (changed under `publication_dir|survey_root`) vs `preserved`, requires equality with `pending_basis.replacements/preserved` (`:1877-1886`), verifies preserved provenance (`_verify_preserved_provenance:1500-1556`), validates fresh QA (`:1898-1944`: `reader.validate_manuscript_manifest`, `quality.validate_bundle`, `reader.validate_review_record ×2` with `SEMANTIC_EDITORIAL`/`VISUAL` kinds, `surface_gate.validate_reader_surface_gate` with `expected_manuscript_path`, bundle checks all PASS), then exclusively creates `publication-surface-revalidation-r{seq}.json` (`_revalidation_record_path`, `_revalidation_existing_sequences`, `_exclusive_create_record_bytes:1604-1642` with fd dev/ino identity + same-fd readback) and atomically replaces State (`_atomic_replace_state_bytes:1666-1770` temp+`os.replace` with double expected-old recheck + temp identity/bytes pre-publish recheck), with owner-aware rollback that never deletes unknown bytes (`:2047-2200`). This is the authoritative completion to reuse, not duplicate.

**Longform receipt strictness (cycle source).**
- `scripts/survey_longform_generated_v2.py:606-638` `build_receipt`, `:641-663` `_inspect_receipt_envelope` (no tool pinning, never proof alone), `:665-758` `validate_receipt` (public: tool pin `verify_tool_basis`, contract equality `THEMATIC/LONGFORM_SPECIAL`, persisted semantic review reload `surface_gate.load_and_validate_reader_surface_semantic_review require_pass`, review→receipt binding, `longform.load_derivation_for_readback`, accepted-refs equality, canonical outputs `:707-714`, `validate_survey_build_directory`, canonical FILE-byte/path authority `:716-730` exactly `reader-surface-input-v2.json` / `interactive-semantic-publication-input.json` / `validated-source-manifest.json` under `source_root/publication/v2`, drift checks, `validate_longform_reader_input` + `canonical_reader_bytes` FILE-byte equality `:734-742`, heading syntax, `render_main/render_bibliography` + `validate_generated_closure` + deterministic replay `:744-757`).
- `scripts/survey_longform_derivation_v2.py: load_derivation / load_derivation_for_readback / validate_longform_reader_input / canonical_reader_bytes` — strict State/Profile/contract/HEAD authority; readback is the only live derivation entry.

**Weekly receipt (slightly looser paths, same canonical outputs).**
- `scripts/survey_weekly_derivation_v2.py: load_derivation` (strict State via `agent.validate_agent_state` or pending_basis branch, `DRAFT_COMPLETE+`, `WEEKLY/WEEKLY_MAGAZINE`, checkpoint-resolved architecture/synthesis/draft/evidence/matrix/ledger/discovery + card refs), `build_receipt`, `_inspect_receipt_envelope`, `validate_receipt` (tool closure `_verify_head_bytes`, contract `WEEKLY/WEEKLY_MAGAZINE`, derivation reload, accepted-refs equality, canonical `survey_root/{main.tex,references.bib,jgaisurvey.sty}` outputs, `validate_survey_build_directory`, reviewed-input drift + `validate_reader_input` object equality + `render_main/render_bibliography` + `validate_generated_closure` + deterministic replay). Weekly does NOT pin canonical reader/archive/receipt sibling paths the way Longform `:720-730` does, but Gate still demands `reader-surface-input-v2.json` name + sibling `validated-source-manifest.json` receipt.

**Gate/manuscript/quality/review (cycle closers).**
- `scripts/survey_reader_surface_gate_v2.py: _inspect_gate_record` (structural/semantic minus derivation replay; never admission alone) + `validate_reader_surface_gate(repo_root,path,*,issue_id,publication_profile,expected_manuscript_path,state_path)` (always `_inspect` + `_derivation_for_manuscript` receipt/current-tool replay; `expected_manuscript_path` mandatory for stage admission callers) + `_derivation_for_manuscript` (DIRECT_PRIMARY primary-only vs generated LONGFORM/WEEKLY routes; generated routes demand `reader-surface-input-v2.json` name + `publication/v2` suffix + sibling receipt `validate_receipt` + `receipt.reviewed_reader_input/semantic_review` binding + `receipt.outputs == manuscript.primary+bib+style` with `survey_dir/main.tex|references.bib|jgaisurvey.sty` exact paths) + `evaluate_reader_surface_gate` (lexical lint + mandatory semantic authority, scanned_surfaces with `MANUSCRIPT_MANIFEST×1 + PRIMARY_SOURCE×1`, gate_sha recomputation, byte-count checks) + `load_and_validate_reader_surface_semantic_review` / `load_and_validate_semantic_review`.
- `scripts/survey_reader_publication_v2.py: build_manuscript_manifest` (exact `MANUSCRIPT_SCHEMA`, `manifest_sha256`, `_validate_manifest_semantics`, `if output_path.exists: refuse`), `validate_manuscript_manifest`, `build_review_record(repo_root,manuscript_path,pdf_path,page_count,review_kind,checks,reviewed_by,recorded_at,output_path)` (`review_kind ∈ {SEMANTIC_EDITORIAL,VISUAL}`, exact PDF page count via `_exact_pdf_page_count`, expected check family via `_expected_review_checks` + `fidelity.validate_review_depth`, `if output_path.exists: raise`), `validate_review_record` (digest + manuscript/profile/source/pdf binding + page-count + check family + fidelity), `build_reader_surface_gate`.
- `scripts/survey_quality_v2.py: build_bundle(repo_root,issue_id,source_path,pdf_path,checks,output_path,pdf_authority,*,production_profile_path)` (`if output_path.exists: refuse`, `bind_pdf_authority`, `validate_checks` DETERMINISTIC, `bundle_sha256`), `validate_bundle`, `bind_pdf_authority`, `expected_checks/validate_checks`.
- `scripts/survey_stage_validation_v2.py: _validate_stage_semantics` DRAFT_COMPLETE branch: binds manuscript→source, bundle→source+PDF (`REPOSITORY_FILE` required), semantic/visual→manuscript+source+PDF, then `surface_gate.validate_reader_surface_gate`. This is the normal-path public validator reused after admission; no new Gate needed.

**Publication Candidate / Freeze (postinstall return).**
- `schemas/publication-candidate-v2.schema.json:1-72` (`2.0-rc1`, `READY_FOR_PUBLICATION_PREVIEW`, `reader_manuscript/source/pdf/quality_bundle/semantic_review/visual_review` + `candidate_sha256`, `pdfAuthority` with `REPOSITORY_FILE|GITHUB_ACTIONS_ARTIFACT`).
- `scripts/survey_publication_v2.py:668-746` `build_candidate` (exact manuscript/bundle/semantic/visual/PDF binding, `candidate_sha256`, `_write_immutable`), `:749-814` `validate_candidate` (digest + 5 authority drifts + manuscript/profile/source/pdf/review cross-binding), `:817-869` preview approval (`publication_candidate_path+sha` + `pdf_path+sha+page_count` binding), `:171-245` `_prepare_freeze_inputs` (joint Freeze authority + snapshot), `:323-430` `_preflight_freeze_pair` (schema + ancestor + authority-overlap/hardlink + equal-payload resume + manifest-without-freeze refuse + snapshot recheck), `:490-558` `_install_owned_json` (`O_CREAT|O_EXCL|O_NOFOLLOW`, FileExists→lstat/symlink/reg/ancestor/exact-bytes resume else divergent refuse, fd identity, short-write loop, fsync/close handling with owned-partial rule), `:561-657` `_install_freeze_pair` (Freeze first, Manifest second with inter-half Freeze re-verification, completed-Freeze-retained-on-Manifest-failure), `:919-963` `build_freeze`, plus `validate_release_manifest`, merge/release builders. Candidate is SHA-bound selection decision for Human Preview, never publisher: Freeze consumes Candidate+approval+visual+bundle+profile, it does not publish Candidate bytes as source.
- `scripts/candidate_selection_gate.py:1-251` (`suggested_role/validate/initialize`, Evidence `REJECT→EXCLUDE`, `HOLD/INSPECT_MORE→HOLD_OUT`, `POST_CUTOFF→LATE_BREAKING`, `HOLD→positive` refuse) — Evidence Selection only. Unrelated to Publication Candidate except name similarity. Must never be cited as candidate authority.

**P1/P2R/P2V/P3S boundaries reused, not re-argued.**
- `scripts/survey_editorial_correction_proposal_v2.py:1-15` read-only, no approval/reason/State; `_compare_supplied_to_rederived:1710-1737` BASIS/PROPOSED mismatch; `:822-862` observed `publication-candidate-v2.json` via `publication.validate_candidate` + exact 6-field active-before equality (`CANDIDATE_DIVERGED` if any field differs), classified `COPY (old mutable)` + `CANDIDATE_OBSERVED unadopted` edge, no ownership. P1 basis/proposed/retention_plan already carry versioned reviewed target front half (`basis.state_ref/validation_checkpoint_ref/active_revalidation_ref/active_reader_input_ref/before_graph_digest/generated_receipt_ref/renderer_commit/contract_identity` + `proposed.authoring_input_ref/proposed_reader_ref/canonical_sha/change_description`).
- `scripts/survey_editorial_retention_v2.py: capture_retention / verify_retention`, `_Session.safe_read` dirfd/no-follow pins, retained-root `.../editorial-corrections/<proposal_id>/retained` one-shot (`RETAINED_ROOT_EXISTS` refuse), `KEEP_IMMUTABLE` vs `COPY_BEFORE_REPLACEMENT` policies, manifest `CAPTURED`.
- `scripts/survey_editorial_current_authority_v2.py: observe_current_authority(root,state_path,proposal_path,manifest_path,scope_review_path=None)` read-only, `RESULT_SCOPE_BOUND/NEEDS_SCOPE`, P1 header/basis/proposed/plan + retained-set consistency + entry-to-final stability (ORIGINAL pins + control/edition/retained inventories + HEAD, no resnapshot laundering).
- `scripts/survey_editorial_staged_source_v2.py: materialize_staged_source / verify_staged_source`, `STAGED_DIRNAME/MANIFEST_FILENAME/MAIN|BIBLIOGRAPHY|STYLE_FILENAME`, `EDITORIAL_STAGED_SOURCE_V1/STAGED_ONLY`, fixed 37 replay deps (`_route_code_deps`), manifest-last, owned 4-file, `TOOL_DRIFT`, narrow `_SessionScopeReader` reusing real P1 `_validate_scope` on retained bytes, `P2V×2 stable-facts-only` (no second-map full equality).
- `config/survey-production-v2.json`: `state_authority.{authoritative_filename:production-state.json, agent_checkpoint_dir, architecture_approval_path, publication_preview_approval_path, profile_filename}`, `orchestration.stage_plan.DRAFT_COMPLETE.{artifacts[6], checkpoints:[validation], handler:stage:reader-publication-validation, validator:validate:reader-publication}`, `contract_files.pipeline/quality`.

**Human Gates.**
- `scripts/survey_human_gate_v2.py: record_architecture_approval / record_publication_preview_approval`, `invalidate_pending_gate` (pending-only + Architecture passed-checkpoint conditions). `survey_agent_control_v2.py:1393-1497` `approve_architecture / approve_publication_preview` (exact-byte approvals, canonical paths, State `human_gates/human_gate_provenance/machine_checkpoints` updates). No new Human Gate is created by admission; Human Preview stays normal `approve_publication_preview` on fresh Candidate.

## 2. Blocker-by-blocker corrections (real solutions, no punt)

### 2.1 Existing 3 TeX outputs cannot `O_EXCL` — owned `temp+replace`, not exclusive create

Prior §§2.5/7.1 applied P3S staged `O_EXCL` to live `survey_root/{main.tex,references.bib,jgaisurvey.sty}`. Those 3 exist healthy-before by definition (`_collect_pending_rows` kept-set; receipt outputs canonical). `os.open(O_CREAT|O_EXCL)` must fail (`FileExistsError`) or, worse, a FileExists→overwrite branch would be divergent-overwrite violation.

**Correction:** live replaces use the controller’s proven `temp+replace` pattern (`_atomic_replace_state_bytes:1666-1770` + `_install_owned_json:490-558` FileExists branch logic, adapted for non-JSON bytes):

- Preflight per target: lexical `repo_local_path` + `..`/backslash refuse + `is_symlink` leaf refuse + ancestor `lstat` walk (no symlinked/non-dir ancestor, cf. `_check_output_ancestors:125-142`, `_reject_symlink_ancestors_reval:1559-1601`), target must be regular file (not symlink/FIFO/dir), current bytes SHA == expected-old SHA from bounded context (§2.8) else `LIVE_BEFORE_DRIFT` refuse with live preserved.
- Write to sibling temp `.<basename>.tmp-admit-<newsha16>` with `O_CREAT|O_EXCL` (temp is new, so `O_EXCL` is lawful), `write loop + fsync + fd dev/ino capture + same-fd readback == expected-new bytes` (staged bytes for TeX; generated bytes for QA/PDF per §2.6), temp readback recheck, live `expected-old` recheck immediately before `os.replace`, temp identity+bytes pre-publish recheck, `os.replace`, post-replace readback `== expected-new`. Any short/zero/fsync/close/replace/readback fault → `INCOMPLETE/INDETERMINATE` per-file classification (§2.7), owned temp removed only if still own identity+expected bytes, live preserved, manual recovery required. No truncating `write_json`, no `unlink` of unknown bytes, no rollback that deletes foreign evidence (same rules as `:2047-2200`).
- Equal-payload resume: if live already equals expected-new (identical retry after `INDETERMINATE` with complete bytes retained), treat as `RESUMED_IDENTICAL`, do not rewrite. Divergent live (neither expected-old nor expected-new) → `DIVERGENT_LIVE` refuse, preserve for manual recovery.
- This applies to EVERY existing live target in §2.7, not only 3 TeX. New sequence files (revalidation `rN`, never-existing versioned QA temps) may use `O_EXCL` create (`_exclusive_create_record_bytes` precedent).

### 2.2 `P2V-before` cannot run after the before-set changes — split before/after, no second same-before

Prior demanded writer-internal `P2V×2` with stable-fact comparison across live install. After TeX install, `before_graph_digest` / `before_live_refs` necessarily change; a second `observe_current_authority` in before-context must fail (correctly). Demanding it to pass is incoherent.

**Correction — three operation boundaries, two different observation kinds:**

- `prepare` (before-context, read-only + versioned writes only outside live): run `observe_current_authority(root,state_path,proposal_path,retention_manifest_path,scope_review_path)` fresh (P2V-before, `SCOPE_BOUND` required; `NEEDS_SCOPE` → refuse). Pin `bounded context` (§2.8) including `before_live_refs`, `before_qa_refs`, `before_candidate`, `predecessor revalidation ref`, HEAD, contract, renderer commit. No live mutation yet, so P2V-before is valid.
- `install` (owned live TeX replace per §2.1, still no QA/State/Candidate writes): do NOT re-run P2V-before. Instead re-verify only that (a) State bytes == context `state_sha`, (b) retention manifest + staged manifest + proposal + scope review bytes unchanged (re-`safe_read` + SHA), (c) live TeX after == expected-new, (d) non-target live files (QA/PDF/Candidate/State) unchanged vs context (proves window ownership). Any violation → `WINDOW_DRIFT` fail with owned partials preserved.
- `finish` (after-context, public validators): run `verify_retention` + `verify_staged_source` (historical consistency, no current-State claim) + FRESH live QA validators against after-bytes with explicit after-context (`reader.validate_manuscript_manifest`, `quality.validate_bundle`, `reader.validate_review_record` ×2, `surface_gate.validate_reader_surface_gate` with `expected_manuscript_path` + `state_path`, `longform.validate_receipt` or `weekly.validate_receipt` with `state_path`/`pending_basis` per route). These are after-readbacks, not second P2V-before. A second `observe_current_authority` in before-context after install is FORBIDDEN to be required; if run for diagnostics it must be expected to report `BEFORE_DRIFT` (proves install happened), not `SCOPE_BOUND`.
- Stable-facts comparison across install is limited to control/retained inventories (contract files, retention bytes, staged bytes, HEAD lineage) that must NOT change; before-live bytes must change (exactly the 3 TeX + later QA/PDF per expected deltas). Prior “stable-facts-only” is retained for the former, explicitly excluded for the latter.

### 2.3 Arbitrary `3A/0M` forbidden — exact impact table instead of budget (§5)

Prior §7.1 declared `1 module + 1 schema + 1 test` with “existing changes are blockers”. That is backwards: the design needs existing-chain consumption, so the schema+controller MUST change minimally. Correction replaces the budget with §5 caller/path table: 1 new admission module (owned transaction + versioned QA generation + candidate replacement writer), 1 schema edit (revalidation `reason_class` enum + optional `editorial_bindings`), 2 small controller edits (`REVALIDATION_REASON_CLASSES` + chain/reason checks + editorial-bindings enforcement when present), 0 receipt/Gate/manuscript/quality/stage/publication logic changes (reuse as callers with explicit context args), plus behavioral tests (new files only, no old-test transfer). No path-count ceiling; deferral only on unresolved predicates per P3S contract §2 precedent, not on count.

### 2.4 Unconsumed State pointer/schema invalid — reuse existing chain, extend reason, compare on coverage/cost

**Options compared (consumer coverage = which existing validators enforce the new authority without new wiring):**

| Option | State/schema change | Consumers that already enforce it | New wiring / retained cost | Verdict |
|---|---|---|---|---|
| **E1: `REVIEWED_EDITORIAL_CORRECTION` inside existing `publication_revalidation_provenance` chain (SELECT)** | `publication-surface-revalidation.schema.json`: `reason_class` `const→enum {REVIEWED_CORE_CHANGE, REVIEWED_EDITORIAL_CORRECTION}` + optional `editorial_bindings {proposal_ref,retention_manifest_ref,staged_manifest_ref,scope_review_ref,before_live_digest,after_live_digest}` (`additionalProperties:false` preserved; `required` unchanged; when `reason_class==REVIEWED_EDITORIAL_CORRECTION` then `editorial_bindings` required + 4 refs exact `{path,sha256}` + digests 64-hex). No State schema change (`publication_revalidation_provenance` already `nullableAuthority`). Controller: `REVALIDATION_REASON_CLASSES += {REVIEWED_EDITORIAL_CORRECTION}` + `_check_revalidation_chain:994-995` + `_resolve_publication_revalidation:1115-1116` accept both + `_check_immutable_revalidation_rows` + `_check_revalidation_agreement` unchanged (they already bind rows/chain/PDF agreement for any reason) + new `editorial_bindings` exact-match check (proposal/retention/staged/scope SHAs + before/after digests vs bounded context + live). | All: `resolve_active`/`_resolve` (live+historical), `_check_immutable_rows`, `_check_chain`, `_check_agreement`, `_validate_agent_state` (strict + pending), `built_checked_pending_basis`/`_collect_pending_rows` (7-role allowlist), Weekly `load_derivation` pending branch, stage `validate:reader-publication`, `validate_candidate`/Freeze (via `validation.*` refs), human-gate agreement. History preserved via `supersedes` chain mixing both reasons (chain chronology + prior-checkpoint-match checks already reason-agnostic except reason-membership). | Small: 1 schema edit + 3 controller hunks + new admission caller. Old `REVIEWED_CORE_CHANGE` rows untouched; mixed chain explicitly allowed; old bytes immutable (superseded_artifacts `prior_sha256` + retained copies). | **SELECT** |
| E2: parallel `editorial_admission_provenance` + `editorial-admission-record` schema (prior §§2.1/7.1, REJECT) | New State field + new schema + new resolvers. | None: receipt/Gate/manuscript/quality/stage/Candidate/publication/derivation never read it; `validate_agent_state` would need new branch; `resolve_active` would need second pointer with precedence rules; historical predecessor semantics undefined; `pending_basis` rows ignore it. | Large: State schema + ≥5 validators + receipt/Gate derivation + stage + publication + new verifier, plus precedence/migration for mixed history, plus double-chain agreement. Advertised “no existing changes” is false economy — it leaves authority unenforced. | REJECT |

No `equalSHA review rebinding`: `producer_head` stays provenance-only (P3S S5 inheritance); review path identity stays exact `{path,sha256}` with `PATH_IDENTITY_MISMATCH` on same-SHA different-path (Human Gate `:864` canonical-bytes precedent, P1 `PROPOSED_ARCHIVE_DRIFT/PROFILE_DRIFT :1559-1565`).

### 2.5 Receipt/Gate/manuscript cycle — separate three review kinds, fix contexts, no generic bypass

Three review kinds are distinct authorities, never substituted:

- **Early scope review (pre-TeX, immutable proposed-reader path):** real P1 `_validate_scope` via P3S narrow `_SessionScopeReader` on retained bytes (no live Collector, no dummy HEAD/config). Input is `proposed_reader_ref` (versioned `.../editorial-corrections/<proposal_id>/proposed-reader.json`, immutable once P1 `PROPOSED`), not live `reader-surface-input-v2.json`. This gates `prepare→install` (prose/derivation boundary, no PDF needed). `ordinary-without-block` scope is refuse in admission (P3S O7 allowlist does not transfer).
- **Postrender QA (live TeX+PDF+manuscript/bundle/semantic/visual/Gate/receipt, §2.6):** built AFTER `install` against live after-bytes, validated with exact public APIs and explicit contexts (see §3): `validate_manuscript_manifest(repo,manuscript_path,issue_id)`, `validate_bundle(repo,bundle_path,issue_id)`, `validate_review_record(repo,path,issue_id,expected_kind)` ×2, `validate_reader_surface_gate(repo,gate_path,issue_id,publication_profile,expected_manuscript_path,state_path)` (mandatory `expected_manuscript_path` + `state_path` for admission; standalone inspection without them is never admission), `validate_receipt(root,receipt_path,state_path[,pending_basis])` per route (Longform strict canonical + `load_derivation_for_readback`; Weekly canonical outputs + `load_derivation`). No `DIRECT_PRIMARY` fallback for generated correction (would evade receipt contract). No `pending_basis` as bearer: `pending_basis` is only the controller-internal checked row snapshot passed explicitly to Weekly `load_derivation`/`validate_receipt` when `VALIDATED_DRAFT` strict State would otherwise see changed rows; it is constructed by `built_checked_pending_publication_basis` from actual State/checkpoint/files, rechecked by `_verify_pending_binding`, never a caller-supplied enum/flag to skip validation. Generic `ignore/pending` bearer flags are forbidden.
- **Human Preview (normal Gate, after authoritative completion):** `publication.validate_candidate` on fresh Candidate + `agent_control.approve_publication_preview` (exact Candidate+PDF binding, canonical `source_root/publication/v2/publication-candidate-v2.json` + `gates/publication-preview-approval.json`). Admission never invents `APPROVED`, never forges `REQUEST_CHANGES`, never calls `approve_*` itself; it only produces `READY_FOR_PUBLICATION_PREVIEW` Candidate for normal Human decision. Synthetic fixture reviews are never genuine approvals (inherited limit).

### 2.6 Fresh PDF/log/QA/postrender semantic+visual arrival — `prepare/install/finish` with live build, versioned alternative costed

**Authoritative completion requires live-bound fresh QA.** Staged replay alone is not public readback (P3S limit). Therefore:

- `prepare`: versioned inputs only — P1 proposal (`PROPOSED`), P2R retention (`CAPTURED`), P2V-before (`SCOPE_BOUND`), P3S staged (`STAGED_ONLY`, 4-file owned `staged-source/` + `staged-source-manifest.json` with `manifest_digest`), early scope review PASS. No live writes. Output: bounded context (§2.8) + `expected_new_tex` bytes (staged `main/references/style` bytes, already deterministically replayed by `verify_staged_source`).
- `install`: owned live TeX replace (3 files, §2.1) from `expected_new_tex`. Live is now `TRANSITION_INVALID_LIVE` (TeX new, QA/PDF old, State old) — explicitly acknowledged, bounded by context, not authoritative, not previewable. Failure here → §2.7 partial classification + manual recovery, never silent success.
- `finish`: (a) build PDF from live TeX. R1 contract fixes the build boundary without claiming R3 build proof: use the SAME deterministic toolchain/pinning as normal publication for the route (LuaLaTeX per `WEEKLY_BUILD_OUTPUTS`/`LONGFORM_BUILD_OUTPUTS` `main.pdf/main.log/main.pdf.sha256` inventory; `validate_survey_build_directory` precheck; `validate_generated_closure` for TeX/style closure). Build is executed in the live `survey_root` under owned-write discipline (PDF/log are existing live targets → `temp+replace` per §2.1; `main.log` retained as diagnostic, `main.pdf.sha256` as transfer check). If the execution environment cannot run LuaLaTeX deterministically, `finish` must `NO-GO` here (see §11), not invent PDF bytes or bless unbuilt QA. (b) Generate QA bytes versioned-first (in-memory + temp files under `.../editorial-corrections/<proposal_id>/finish-tmp/`, never live yet): manuscript (`build_manuscript_manifest` with live `primary_source` + `BIBLIOGRAPHY`+`STYLE` supports + architecture/coverage/requirements carried from before-context, `authored_by` = editorial correction identity, NOT synthetic Human), quality bundle (`build_bundle` with live source+PDF + DETERMINISTIC checks + `production_profile_path`), semantic+visual reviews (`build_review_record` ×2 with exact PDF page count + full check families + `fidelity.validate_review_depth`), Gate (`evaluate_reader_surface_gate` with manuscript + semantic authority), receipt (`longform.build_receipt` or `weekly.build_receipt` with live `surface/review/primary/bib/style` + `current_tools` HEAD/contract/closure). (c) Validate versioned QA against live after-bytes with public validators (same functions as §2.5, explicit contexts). (d) Owned-install QA+PDF+receipt to live canonical paths (`temp+replace`, §2.1/§2.7). (e) Call existing `revalidate_publication_surface(repo,cfg,state_path,reason_class="REVIEWED_EDITORIAL_CORRECTION",reason="<non-empty truthful editorial reason binding proposal_id/change_description>",executor,recorded_at)` which creates `publication-surface-revalidation-r{next}.json` with `editorial_bindings` + updates `publication_revalidation_provenance` (record-last, State `temp+replace`). Reason reuses no `REVIEWED_CORE_CHANGE`; empty reason or old-enum pass-through → `REASON_CLASS_MISMATCH` refuse. (f) Build fresh Candidate (`publication.build_candidate` → canonical `publication-candidate-v2.json` via replacement writer §2.11) + `validate_candidate`.

**Versioned-bundle alternative (all-versioned generation then pointer switch) — REJECT as infeasible for R2:** would require adding file indirection (live `survey_root/main.tex` → versioned target pointer) + changing Longform `:707-730` canonical checks + Weekly canonical outputs + Gate `_derivation_for_manuscript` sibling-receipt rule + manuscript `primary_source`/`supporting_files` path rules + stage DRAFT_COMPLETE artifact paths + `validate_survey_build_directory` + Candidate `source/pdf` path rules + Freeze snapshot paths to accept versioned paths. That is ≥8 logic files + 4 schemas + contract-file hash changes (contract identity covers schemas/config) + migration for old epochs. No pointer exists today; inventing one creates a second authority with double-readback cost and migration burden. The bounded invalid-live window (minutes, single-issue, fail-closed, manual-recovery documented) is cheaper and preserves all current canonical consumers unchanged. Hence SELECT live-build + bounded window, REJECT pointer-switch.

### 2.7 Full write set (not 3 files) + ancestor identities + failure classification + invalid-live acknowledgement

Full owned write set for one editorial admission (Longform route; Weekly differs only in `route`/`research_profile` per §7):

| # | Target (canonical rel) | Before (context) | After (expected) | Ownership | Ancestor/identity checks | Failure disposition |
|---|---|---|---|---|---|---|
| 1 | `<survey_root>/main.tex` | `before_live_refs.main {path,sha256,byte_count}` (healthy before) | staged `main` bytes `{sha256,byte_count}` | `temp+replace` §2.1 | lexical + ancestor lstat + leaf symlink refuse + fd dev/ino + same-fd readback + pre/post `expected-old/new` rechecks | `TEX_REPLACE_INCOMPLETE` (short/write/fsync/close/replace/readback) → owned temp rule (§2.1), live preserved as found (old or new-complete), `INDETERMINATE` if complete-valid-bytes retained but close failed; never success |
| 2 | `<survey_root>/references.bib` | same pattern | staged `bibliography` bytes | `temp+replace` | same | `BIB_REPLACE_INCOMPLETE` ditto |
| 3 | `<survey_root>/jgaisurvey.sty` | same pattern | staged `style` bytes (must equal `templates/survey/jgaisurvey.sty` bytes per staged `style_input_ref`; style source itself untouched) | `temp+replace` | same + style-input equality | `STYLE_REPLACE_INCOMPLETE` ditto |
| 4 | `<survey_root>/main.pdf` | `before_pdf {path,sha256,byte_count,page_count}` | freshly built PDF bytes from after-TeX (page_count via `_exact_pdf_page_count`) | `temp+replace` (existing) | same + PDF page-count binding | `PDF_REPLACE_INCOMPLETE` / `PDF_BUILD_FAILED` (no QA built, live TeX new + PDF old → `TRANSITION_INVALID_LIVE` held, manual recovery: rebuild or restore TeX from retained COPY per context) |
| 5 | `<survey_root>/main.log` (+ `main.pdf.sha256` if present per `*_BUILD_OUTPUTS`) | before log (diagnostic, not authority) | fresh build log | `temp+replace` or exclusive-create if absent | same (log failure never blocks authority but is retained) | `LOG_RETAINED` (diagnostic only) |
| 6 | `<source_root>/publication/v2/reader-manuscript-v2.json` | `before_qa.manuscript {path,sha256}` | generated manuscript binding after-TeX/PDF (`manifest_sha256`) | `temp+replace` (build_* refuse overwrite, so generate versioned then owned-install) | same + `validate_manuscript_manifest` pre-install | `MANUSCRIPT_INSTALL_INCOMPLETE` |
| 7 | `<source_root>/publication/v2/quality-regression-bundle-v2.json` | `before_qa.bundle` | generated bundle (`bundle_sha256`, DETERMINISTIC PASS) | `temp+replace` | same + `validate_bundle` | `BUNDLE_INSTALL_INCOMPLETE` |
| 8 | `<source_root>/publication/v2/semantic-editorial-review-v2.json` | `before_qa.semantic` | generated `SEMANTIC_EDITORIAL` review (`review_sha256`, full check family) | `temp+replace` | same + `validate_review_record(kind)` | `SEMANTIC_INSTALL_INCOMPLETE` |
| 9 | `<source_root>/publication/v2/visual-review-v2.json` | `before_qa.visual` | generated `VISUAL` review | `temp+replace` | same | `VISUAL_INSTALL_INCOMPLETE` |
| 10 | `<source_root>/publication/v2/reader-surface-gate-v2.json` | `before_qa.gate` | evaluated Gate (`PASSED`, `gate_sha256`, derivation receipt-bound) | `temp+replace` | same + `validate_reader_surface_gate(expected_manuscript_path,state_path)` | `GATE_INSTALL_INCOMPLETE` |
| 11 | `<source_root>/publication/v2/validated-source-manifest.json` | `before_qa.receipt` | built receipt (`receipt_sha256`, canonical outputs, FILE-byte replay) | `temp+replace` | same + `validate_receipt(state_path)` | `RECEIPT_INSTALL_INCOMPLETE` |
| 12 | `<source_root>/publication/v2/interactive-semantic-publication-input.json` (Longform archive; Weekly equivalent `interactive-semantic-publication-input` sibling per route) | before archive (preserved, KEEP) | unchanged (editorial correction does not rewrite authored archive; `authored_refs` equality required) | no write (drift → refuse) | `ARCHIVE_DRIFT` refuse | — |
| 13 | `<source_root>/publication/v2/reader-surface-input-v2.json` (reviewed reader input) | before reader input (preserved upstream; NOT overwritten by proposed-reader) | unchanged (proposed-reader lives versioned under `editorial-corrections/<id>/proposed-reader.json`; live reviewed input stays old until revalidation re-derives? Clarified: for generated routes the live reviewed input IS the pre-TeX surface that rendered the TeX; editorial correction’s proposed-reader must equal the rederived surface from new live? Actually P1 `proposed_reader_canonical_sha256` + staged replay already prove proposed==rendered; live reviewed input after admission is still the old canonical file unless the correction also updates it. DECISION: live reviewed input is part of publication surface only insofar as receipt binds it; if proposed-reader differs from live reviewed input, receipt `reviewed_reader_input` must be updated to new live reviewed input bytes via owned `temp+replace` from proposed canonical bytes (expected-old = before reader SHA, expected-new = proposed canonical SHA + `canonical_reader_bytes` equality). This is the 14th write; see §3 `expected_reader_delta`. If P1 proves prose-only TeX delta with identical reader object, this write is identity (no-op, `RESUMED_IDENTICAL`).) | `temp+replace` iff changed | same + `validate_longform_reader_input` / `validate_reader_input` + `canonical_reader_bytes` FILE equality | `READER_INPUT_INSTALL_INCOMPLETE` |
| 14 | `<source_root>/publication/v2/publication-surface-revalidation-r{next}.json` (new sequence) | absent (sequence collision → refuse) | new record (`reason_class=REVIEWED_EDITORIAL_CORRECTION` + `editorial_bindings` + `superseded/preserved` + `validation.*` + `supersedes` predecessor or null) | `O_EXCL` create (`_exclusive_create_record_bytes` precedent) | ancestor + fd identity + same-fd readback | `REVALIDATION_RECORD_COLLISION` (exists/symlink) / `REVALIDATION_RECORD_INCOMPLETE` (owner-aware preserve per `:2047-2200`) |
| 15 | `<source_root>/production-state.json` (canonical via `state_authority.authoritative_filename`) | `state_sha` (expected-old) | State with `publication_revalidation_provenance={path,sha256=expected_record_sha}` (no lifecycle/history/checkpoint mutation; `history` append only via normal Freeze/Release later, not here) | `temp+replace` (`_atomic_replace_state_bytes` precedent) | ancestor + double expected-old recheck + temp identity/bytes pre-publish + post-replace readback | `STATE_REPLACE_UNKNOWN` (preserve record+State, manual recovery; same taxonomy as `:2064-2200`) |
| 16 | `<source_root>/publication/v2/publication-candidate-v2.json` | `before_candidate` (observed unadopted, §2.11) | fresh Candidate (`candidate_sha256`, `READY_FOR_PUBLICATION_PREVIEW`, binds after-manuscript/source/pdf/bundle/reviews) | `temp+replace` via replacement writer (§2.11; `build_candidate` to versioned temp then owned-install, never `Candidate-as-publisher`) | same + `validate_candidate` + supersession predicates | `CANDIDATE_REPLACE_REFUSED` (foreign/approved/drift) / `CANDIDATE_INSTALL_INCOMPLETE` |

Staged `staged-source/` 4-file + retention `retained/` + proposal/scope/versioned QA temps are NOT live; they use their existing one-shot `O_EXCL` disciplines (P2R/P3S preserved). Ancestor identities for every live target are `(st_dev,st_ino)` fd-captured at creation/temp plus `lstat` ancestor walks; same-byte replacement (identical content, different inode) is foreign evidence and must be retained, never unlinked (precedents `:1645-1663`, `:441-480`).

Temporary-invalid-live acknowledgement: between `install` TeX success and `finish` revalidation-State success, `validate_agent_state` (strict, no pending) MUST fail (pending rows changed, revalidation predecessor stale, QA/PDF drift). This is expected `TRANSITION_INVALID_LIVE`, bounded by the in-memory context (§2.8) and the owned-window checks (§2.2 install re-verify). It is not previewable, not freezable, not releasable; `_pending_conditions` + `resolve_active` will report `row snapshot changed / predecessor invalid` until `finish` completes. Crash/power-loss in window → manual recovery from retained COPY + staged bytes + context digests (no auto-rollback that deletes unknown bytes, no global CAS/crash-atomicity claim — inherited limit).

### 2.8 Bounded transaction context — internally rederived, exact deltas, no public enum/bypass

New module holds NO public bearer enum, NO caller `verified_set`, NO `CALLER_VERIFIED` bypass. Instead an internal frozen dataclass (example name `_EditorialInstallBasis`, never serialized as authority, never consulted by other modules):

```
_EditorialInstallBasis(
  root_resolved: str,
  state_path_rel: str, state_sha256: str,
  config_sha256: str, head: str,
  profile_path: str, profile_sha256: str,
  source_root_rel: str, survey_root_rel: str,
  proposal_path: str, proposal_sha256: str, proposal_id: str, issue_id: str,
  research_profile: str, publication_profile: str, route: str,
  retention_manifest_path: str, retention_manifest_sha256: str,
  staged_manifest_path: str, staged_manifest_sha256: str, staged_digest: str,
  scope_review_path: str, scope_review_sha256: str,
  validation_checkpoint_path: str, validation_checkpoint_sha256: str,
  predecessor_revalidation_path: str | None, predecessor_revalidation_sha256: str | None,
  before_live_refs: tuple[(name,path,sha256,byte_count) ×3 TeX],
  before_qa_refs: tuple[(name,path,sha256[,byte_count,page_count]) ×(manuscript,bundle,semantic,visual,gate,receipt,pdf,reader_input)],
  before_candidate_path: str | None, before_candidate_sha256: str | None, before_candidate_verdict: str,
  expected_new_tex: tuple[(name,path,sha256,byte_count) ×3],
  expected_reader_delta: (changed: bool, new_sha256: str | None),
  pending_snapshot: _PendingPublicationBasis | None  # built at finish-entry, not caller-supplied
)
```

Construction (`prepare`): every SHA rederived via `retention._Session.safe_read` narrow pins + `core.sha256_bytes` over pinned bytes (not `Path.read_bytes` on caller strings), `contract_identity` recomputed, HEAD via sanitized `git rev-parse` (P2V precedent), validation checkpoint + predecessor via `_resolve_publication_revalidation(live=False)` + `resolve_active`, candidate via `publication.validate_candidate` + 6-field before-equality (§2.11). Any drift/shape/policy failure → `REFUSED_PRE_WRITE`, creates nothing live.

Rechecks: `install`-entry and `finish`-entry and pre-`os.replace` each re-derive the same fields from disk and require equality except the explicitly expected deltas (`before_live→expected_new_tex`, later `before_qa→generated_qa`, `before_candidate→fresh_candidate`, `predecessor→new record`). Second observation map is never adopted as new baseline; it is compared to context.

### 2.9 Public current validators after completion + historical predecessor semantics

After `finish` State success:

- Strict `validate_agent_state(root,cfg,state)` (no pending) must PASS with new `publication_revalidation_provenance` (proves current authority, not just historical replay). `resolve_active_publication_revalidation(live=True)` must return new record with `live` row/SHA/size checks + `_check_revalidation_agreement` (Human Preview/Freeze/Release agreement when those later exist).
- Historical `verify_editorial_admission`-style readback (standalone, no current-State claim, P3S `verify_staged_source` precedent): revalidates retained/staged/admission consistency + deterministic TeX replay + `supersedes` chain walk (`_check_revalidation_chain` precedent, mixed reasons allowed) + old-bytes immutability (retained COPY bytes == `superseded_artifacts[].prior_sha256`, `preserved_artifacts[]` equality, validation checkpoint bytes unchanged). Old live bytes are never mutated in place history; they survive as retained copies + `prior_sha256` pins + prior checkpoint artifacts.
- No migration of old epochs: prior `REVIEWED_CORE_CHANGE` records keep their bytes/shape; new `editorial_bindings` is optional for old records (absent → old validation path unchanged). `supersedes` links new→predecessor (or null if first). Chain chronology (`linked_at ≤ current_at`, same `prior_checkpoint`, same `issue_id`) enforced for mixed chain.

### 2.10 Repeated correction / R1 interleaving

Second editorial correction on same issue is allowed iff after first `finish`: State is still `VALIDATED_DRAFT` + architecture approved + preview pending + freeze/release pending + exception inactive (`_pending_conditions`), and `resolve_active(live=True)` returns first correction’s record with no errors. Second `prepare` uses updated `predecessor = first record`, updated `before_live/qa/candidate` (first correction’s after), same `validation_checkpoint` (unchanged; validation checkpoint never rewritten), new `proposal_id` (different; `RETAINED_ROOT_EXISTS` + sequence collision prevent reuse). Interleaving with Weekly mechanical refresh (`refresh-mechanical-evidence`) or new `REVIEWED_CORE_CHANGE` revalidation between corrections is allowed iff each operation’s own `pending_basis`/predecessor checks pass in order; concurrent/overlapping admits on same issue are refused by sequence collision + `expected-old` drift (no queue, no merge). If second correction’s `before_graph` no longer matches first correction’s `after` (foreign mutation in between) → `BASIS_MISMATCH` refuse, manual triage. No “keep retrying until green” loop; precise stop after one fail-closed refusal with preserved evidence.

R1 (roadmap R1, this contract) interleaving: this contract IS R1’s output; R2 vertical implementation must not start a second R1-style contract analysis. If R2 discovers an essential interface contradiction (e.g. live PDF build provably impossible under fixed toolchain), it returns `NO-GO` per §11, not a new helper-only analysis.

### 2.11 Candidate — observed unadopted Publication Candidate, supersession predicates, replacement writer

Facts: P1 `:822-862` observes `publication-candidate-v2.json` at `(source_root)/publication/v2/publication-candidate-v2.json` (from Profile `source_root`, not parent traversal), symlink→`CANDIDATE_ALIAS` refuse, `publication.validate_candidate` + 6-field exact active-before equality (`reader_manuscript/source/pdf/quality_bundle/semantic_review/visual_review` path+SHA vs `effective[reader-manuscript|validated-source|publication-pdf|quality-regression-bundle|semantic-review|visual-review]`), `CANDIDATE_DIVERGED` on any field mismatch, graph `CANDIDATE_OBSERVED unadopted`, mutable-COPY classification, no ownership. This is Publication Candidate, never `candidate_selection_gate` Selection (Evidence roles). Prior §2.6 conflated install collision with HOLD rejection; Astra blocker 3 requires distinction.

**Correction — three verdicts at `prepare` (before-install), one writer after `finish`:**

- `OBSERVED_HEALTHY_SAME_BEFORE` (proceed): candidate file exists, `validate_candidate` passes, 6-field equality with before-effective holds, `candidate_sha256` recomputed, Human Preview still `pending` with NO `publication_preview` provenance/approval binding this candidate bytes (`state.human_gate_provenance.publication_preview is None` + approval file absent or `validate_preview_approval` fails to bind this candidate — i.e. unadopted), no Freeze/Release binding it (`machine_checkpoints.freeze/release pending` + no `freeze-record`/`release-manifest` referencing its SHA). Record `before_candidate_{path,sha256,verdict}` in context. Install may proceed; after `finish` this candidate is `STALE_AFTER` (its 6 fields no longer equal after-effective; retained via P2R COPY if in retention plan, else preserved as superseded bytes via revalidation `prior_sha256` lineage — exact retention row for candidate SHOULD be `COPY_BEFORE_REPLACEMENT` in P1 `retention_plan` when candidate exists; if P1 omitted it, `prepare` refuses with `CANDIDATE_RETENTION_MISSING` rather than silently dropping history).
- `CANDIDATE_FOREIGN / CANDIDATE_DIVERGED / CANDIDATE_INVALID / CANDIDATE_ALIAS` (refuse pre-write): `validate_candidate` fails, or 6-field mismatch vs before-effective (foreign bytes), or symlink/unsafe, or issue/Profile mismatch. `CANDIDATE_COLLISION`-family refuse, live untouched. Owner decision required (explicit operator triage, not auto-overwrite/merge).
- `CANDIDATE_ADOPTED` (refuse pre-write): candidate bytes ARE bound by existing Preview approval (`validate_preview_approval` binds this candidate SHA) or Freeze/Release (`freeze-record`/`release-manifest` reference it) or `human_gate_provenance.publication_preview` equals its approval. Supersession would fork decided history → refuse with `CANDIDATE_ADOPTED_REFUSAL`. Editorial correction on decided history needs a different (currently unselected) decided-history contract, not this R1.
- Absent candidate (`NO_CANDIDATE_BEFORE`): proceed (no supersession needed); `finish` still builds fresh Candidate (normal path needs one for Preview).

**Replacement writer (after rebind, never publisher):** `build_fresh_candidate_after_rebind(root, state, after_qa_refs, output_tmp) -> candidate_tmp_path` = thin owned wrapper around `publication.build_candidate(repo,issue_id,publication_profile,reader_manuscript_path,source_path,pdf_path,page_count,quality_bundle_path,semantic_review_path,visual_review_path,output_tmp)` with versioned temp output (new file, `O_EXCL` lawful), then `validate_candidate`, then owned `temp+replace` to canonical `publication-candidate-v2.json` with `expected-old = before_candidate_sha` (or absent→`O_EXCL` create) + ancestor/identity checks per §2.1. Candidate never publishes TeX/PDF/QA; Freeze (`_prepare_freeze_inputs/_preflight/_install`) consumes Candidate+approval+visual+bundle+profile with snapshot rechecks. `build_preview_approval` / `approve_publication_preview` remain normal Human steps after admission; admission stops at `READY_FOR_PUBLICATION_PREVIEW`.

## 3. Concrete API shapes (no ellipses — full signatures, returns, refusals)

New module (proposed path `scripts/survey_editorial_admission_v2.py`; exact filename fixed at R2 start, no code in R1): three public operations + one read-only verifier. All take/return `pathlib.Path`, raise `EditorialAdmissionError(ValueError)` with `code/phase/disposition/detail/owned/cause` (P3S `StagedSourceError` precedent). No CLI, no State adoption outside `finish` record+State, no Gate/Candidate approval, no PDF invention.

```
class EditorialAdmissionError(ValueError):
  def __init__(self, code: str, phase: str, disposition: str, detail: str,
               owned: dict[str, object] | None = None,
               cause: BaseException | None = None) -> None

def admit_prepare(
  root: str | Path,
  state_path: str | Path,
  proposal_path: str | Path,
  retention_manifest_path: str | Path,
  staged_manifest_path: str | Path,
  scope_review_path: str | Path
) -> dict[str, object]:
  # Phases PIN → P1_REDERIVE → RETENTION_VERIFY → STAGED_VERIFY → P2V_BEFORE → SCOPE_EARLY → CANDIDATE_OBSERVE → CONTEXT_FREEZE.
  # Returns {
  #   "result": "EDITORIAL_ADMIT_PREPARED",
  #   "proposal_id": str, "issue_id": str, "research_profile": str, "publication_profile": str, "route": str,
  #   "state_ref": {"path": str, "sha256": str},
  #   "proposal_ref": {"path": str, "sha256": str},
  #   "retention_manifest_ref": {"path": str, "sha256": str},
  #   "staged_manifest_ref": {"path": str, "sha256": str, "manifest_digest": str},
  #   "scope_review_ref": {"path": str, "sha256": str},
  #   "validation_checkpoint_ref": {"path": str, "sha256": str},
  #   "predecessor_revalidation_ref": {"path": str, "sha256": str} | None,
  #   "before_live_refs": {"main": {"path": str, "sha256": str, "byte_count": int},
  #                        "bibliography": {"path": str, "sha256": str, "byte_count": int},
  #                        "style": {"path": str, "sha256": str, "byte_count": int}},
  #   "before_qa_refs": {"manuscript": {"path": str, "sha256": str},
  #                      "quality_bundle": {"path": str, "sha256": str},
  #                      "semantic_review": {"path": str, "sha256": str},
  #                      "visual_review": {"path": str, "sha256": str},
  #                      "gate": {"path": str, "sha256": str},
  #                      "receipt": {"path": str, "sha256": str},
  #                      "pdf": {"path": str, "sha256": str, "byte_count": int, "page_count": int},
  #                      "reader_input": {"path": str, "sha256": str}},
  #   "before_candidate": {"path": str, "sha256": str, "verdict": str} | None,
  #   "expected_new_tex": {"main": {"path": str, "sha256": str, "byte_count": int},
  #                        "bibliography": {"path": str, "sha256": str, "byte_count": int},
  #                        "style": {"path": str, "sha256": str, "byte_count": int}},
  #   "expected_reader_delta": {"changed": bool, "new_sha256": str | None},
  #   "head": str, "contract_identity": {"pipeline_contract_version": str, "pipeline_contract_sha256": str,
  #     "quality_contract_version": str, "quality_contract_sha256": str,
  #     "research_profile_version": str, "research_profile_sha256": str,
  #     "publication_profile_version": str, "publication_profile_sha256": str},
  #   "renderer_commit": str
  # }
  # Refusals (phase/disposition): GIT_ENV_REFUSED/PIN/REFUSED_PRE_WRITE,
  #   STATE_UNREADABLE/PIN/REFUSED_PRE_WRITE, PROFILE_DRIFT/PIN/REFUSED_PRE_WRITE,
  #   P1_BASIS_MISMATCH/P1_REDERIVE/REFUSED_PRE_WRITE, RETENTION_INVALID/RETENTION_VERIFY/REFUSED_PRE_WRITE,
  #   STAGED_INVALID/STAGED_VERIFY/REFUSED_PRE_WRITE, P2V_NOT_SCOPE_BOUND/P2V_BEFORE/REFUSED_PRE_WRITE,
  #   SCOPE_INVALID/SCOPE_EARLY/REFUSED_PRE_WRITE, CANDIDATE_FOREIGN|DIVERGED|INVALID|ALIAS|ADOPTED|RETENTION_MISSING/CANDIDATE_OBSERVE/REFUSED_PRE_WRITE,
  #   PENDING_CONDITIONS_UNMET/PIN/REFUSED_PRE_WRITE, TOOL_DRIFT/PIN/REFUSED_PRE_WRITE.

def admit_install(
  root: str | Path,
  prepared: dict[str, object]
) -> dict[str, object]:
  # Phases WINDOW_RECHECK → TEX_REPLACE_MAIN → TEX_REPLACE_BIB → TEX_REPLACE_STYLE → INSTALL_READBACK.
  # Re-derives every prepared SHA from disk (retention Session safe_read + core.sha256_bytes);
  # requires equality except no live change yet; then owned temp+replace per §2.1 for 3 TeX in order main→bib→style.
  # Returns {
  #   "result": "EDITORIAL_TEX_INSTALLED_TRANSITION_INVALID_LIVE",
  #   "installed_tex": {"main": {"path": str, "sha256": str, "byte_count": int, "identity": [int, int]},
  #                    "bibliography": {"path": str, "sha256": str, "byte_count": int, "identity": [int, int]},
  #                    "style": {"path": str, "sha256": str, "byte_count": int, "identity": [int, int]}},
  #   "live_invalid_ack": "TRANSITION_INVALID_LIVE: TeX new, QA/PDF/State old; not previewable/freezable/releasable until finish",
  #   "window_id": str
  # }
  # Refusals: WINDOW_DRIFT/WINDOW_RECHECK/PRESERVED_LIVE (State/retention/staged/scope/HEAD/contract/QA/PDF/Candidate changed before install),
  #   LIVE_BEFORE_DRIFT/TEX_REPLACE_*/REFUSED_PRE_WRITE (live != expected-old),
  #   TEX_REPLACE_INCOMPLETE/TEX_REPLACE_*/INCOMPLETE|INDETERMINATE (per-file §2.7, owned temp rule, live preserved as found).

def admit_finish(
  root: str | Path,
  installed: dict[str, object],
  prepared: dict[str, object],
  *,
  reason: str,
  executor: str,
  recorded_at: str,
  page_count: int | None = None
) -> dict[str, object]:
  # Phases PDF_BUILD → QA_GENERATE_VERSIONED → QA_VALIDATE_LIVE → QA_INSTALL_OWNED → REVALIDATION_COMMIT → CANDIDATE_REBIND.
  # Builds PDF from live after-TeX (owned temp+replace per §2.1/§2.6; NO-GO if toolchain infeasible),
  # generates QA versioned-first under .../editorial-corrections/<proposal_id>/finish-tmp/,
  # validates with public validators (explicit issue_id/publication_profile/expected_manuscript_path/state_path, no bypass),
  # owned-installs QA+PDF+receipt (+reader_input iff expected_reader_delta.changed),
  # calls revalidate_publication_surface(reason_class="REVIEWED_EDITORIAL_CORRECTION", reason, executor, recorded_at)
  #   with editorial_bindings, then build_fresh_candidate_after_rebind + owned candidate install.
  # Returns {
  #   "result": "EDITORIAL_ADMITTED_AWAITING_PREVIEW",
  #   "pdf_ref": {"path": str, "sha256": str, "byte_count": int, "page_count": int},
  #   "qa_refs": {"manuscript": {"path": str, "sha256": str},
  #               "quality_bundle": {"path": str, "sha256": str},
  #               "semantic_review": {"path": str, "sha256": str},
  #               "visual_review": {"path": str, "sha256": str},
  #               "gate": {"path": str, "sha256": str},
  #               "receipt": {"path": str, "sha256": str, "receipt_sha256": str}},
  #   "revalidation_record_ref": {"path": str, "sha256": str, "sequence": int},
  #   "state_ref": {"path": str, "sha256": str},
  #   "candidate_ref": {"path": str, "sha256": str, "candidate_sha256": str},
  #   "predecessor_ref": {"path": str, "sha256": str} | None
  # }
  # Refusals: PDF_BUILD_FAILED/PDF_BUILD/INCOMPLETE (live TeX new held, manual recovery),
  #   QA_VALIDATION_FAILED/QA_VALIDATE_LIVE/REFUSED_POST_INSTALL (versioned QA does not validate live; live preserved, no record/State/Candidate written),
  #   QA_INSTALL_INCOMPLETE/QA_INSTALL_OWNED/INCOMPLETE|INDETERMINATE (per-file §2.7),
  #   REVALIDATION_FAILED/REVALIDATION_COMMIT/PRESERVED_LIVE (controller error text chained; owned QA/PDF retained as found, record/State per controller rollback taxonomy),
  #   CANDIDATE_REPLACE_REFUSED/CANDIDATE_REBIND/REFUSED_POST_INSTALL (adopted/foreign/drift at rebind time),
  #   REASON_CLASS_MISMATCH|REASON_EMPTY/REVALIDATION_COMMIT/REFUSED_POST_INSTALL.

def verify_editorial_admission(
  root: str | Path,
  proposal_path: str | Path,
  retention_manifest_path: str | Path,
  staged_manifest_path: str | Path,
  revalidation_record_path: str | Path
) -> dict[str, object]:
  # Read-only historical consistency + deterministic replay. Never checks current State/P2V/HEAD.
  # Re-runs verify_retention + verify_staged_source + revalidation row/chain/agreement checks in historical (live=False) mode
  # + editorial_bindings exact-match + TeX FILE-byte replay (staged bytes == revalidation superseded new_sha bytes).
  # Returns {"result": "EDITORIAL_ADMISSION_REPLAY_VERIFIED", "revalidation_record_ref": {"path": str, "sha256": str},
  #          "chain_length": int, "reason_class": "REVIEWED_EDITORIAL_CORRECTION"}.
  # Refusals: RETENTION_MISMATCH / STAGED_MISMATCH / REVALIDATION_HISTORICAL_MISMATCH / EDITORIAL_BINDINGS_MISMATCH / TOOL_DRIFT.
```

Internal `_EditorialInstallBasis` per §2.8 (never public, never serialized). No `...` in R2 implementation: every `dict` above has exact keys; `owned` in errors carries `{"owned_temp": str|None, "live_preserved_as": str, "expected_old_sha256": str, "expected_new_sha256": str, "identity": [int,int]|None}` plus per-file `primary+secondary` close-error chains (P3S precedent).

## 4. Record / schema fields and canonical paths (exact)

**Changed schema (1 file):** `schemas/publication-surface-revalidation.schema.json`

- `properties.reason_class`: `{"const":"REVIEWED_CORE_CHANGE"}` → `{"enum":["REVIEWED_CORE_CHANGE","REVIEWED_EDITORIAL_CORRECTION"]}`.
- Add `properties.editorial_bindings`: `{"type":"object","additionalProperties":false,"required":["proposal_ref","retention_manifest_ref","staged_manifest_ref","scope_review_ref","before_live_digest","after_live_digest"],"properties":{"proposal_ref":{"$ref":"#/$defs/authority"},"retention_manifest_ref":{"$ref":"#/$defs/authority"},"staged_manifest_ref":{"$ref":"#/$defs/authority"},"scope_review_ref":{"$ref":"#/$defs/authority"},"before_live_digest":{"$ref":"#/$defs/sha256"},"after_live_digest":{"$ref":"#/$defs/sha256"}}}`. Top-level `required` unchanged; add `allOf: [{"if":{"properties":{"reason_class":{"const":"REVIEWED_EDITORIAL_CORRECTION"}}},"then":{"required":[...existing...,"editorial_bindings"]}}]` (existing 14 + editorial_bindings when editorial; old records without the field still validate when reason is CORE_CHANGE).
- No other schema changes in R2. Receipt/Gate/manuscript/quality/review/Candidate/State schemas UNCHANGED (canonical paths preserved, no versioned-path allowance, no equalSHA rebinding).

**No new State field.** `publication_revalidation_provenance` (`nullableAuthority`) already carries `{path,sha256}` of `publication-surface-revalidation-r{seq}.json`. Editorial authority is that record (with `editorial_bindings`), consumed by all existing resolvers.

**Canonical paths (computed from Profile `paths.source_root` / `paths.survey_root`, never hardcoded edition names):**

- State: `<source_root>/production-state.json` (`state_authority.authoritative_filename`).
- Profile: `state.profile.path` (exact `{path,sha256}`).
- Config: `config/survey-production-v2.json` (`core.DEFAULT_CONFIG`).
- Validation checkpoint: `state.checkpoint_provenance.validation.{path,sha256}`.
- Predecessor/active revalidation: `state.publication_revalidation_provenance.{path,sha256}` or null (first correction).
- Proposal: `<source_root>/publication/v2/editorial-corrections/<proposal_id>/proposal.json` (`PROPOSAL_FILENAME`).
- Retention manifest: `<same proposal_dir>/retention-manifest.json` (P2R `MANIFEST_SCHEMA` `CAPTURED`); retained root `<proposal_dir>/retained/`.
- Staged manifest: `<proposal_dir>/staged-source/staged-source-manifest.json` (`STAGED_ONLY` + `manifest_digest`); staged TeX `<proposal_dir>/staged-source/{main.tex,references.bib,jgaisurvey.sty}`.
- Scope review: `<proposal_dir>/scope-review.json` (P1 scope output pinned via Session; exact filename fixed at R2, immutable after `prepare`).
- Live TeX: `<survey_root>/{main.tex,references.bib,jgaisurvey.sty}`.
- Live PDF/log: `<survey_root>/{main.pdf,main.log[,main.pdf.sha256]}`.
- Live QA: `<source_root>/publication/v2/{reader-manuscript-v2.json,quality-regression-bundle-v2.json,semantic-editorial-review-v2.json,visual-review-v2.json,reader-surface-gate-v2.json,validated-source-manifest.json,reader-surface-input-v2.json,interactive-semantic-publication-input.json}` (last archive KEEP, not rewritten).
- Revalidation record: `<source_root>/publication/v2/publication-surface-revalidation-r{seq}.json` (`seq = max(existing)+1`, `O_EXCL`).
- Candidate: `<source_root>/publication/v2/publication-candidate-v2.json` (canonical for `approve_publication_preview`).
- Versioned QA temps: `<proposal_dir>/finish-tmp/{reader-manuscript.json,quality-bundle.json,semantic-review.json,visual-review.json,gate.json,receipt.json,candidate.json}` (never canonical, never consumed as authority, removed only if own identity+bytes per temp rule; retained on failure for inspection).

## 5. Caller / path impact table (actual functions, reason for change vs reuse)

| Path | Change | Actual functions touched / called | Reason (why change or why reuse untouched) |
|---|---|---|---|
| `schemas/publication-surface-revalidation.schema.json` | MODIFY: `reason_class` const→enum + optional `editorial_bindings` object | — (schema only) | Minimal hook to carry proposal/retention/staged/scope + before/after digests inside existing chain; preserves `additionalProperties:false` + old records. Parallel pointer would need State schema + new resolvers with zero consumers. |
| `scripts/survey_agent_control_v2.py` | MODIFY (3 hunks): `REVALIDATION_REASON_CLASSES += {"REVIEWED_EDITORIAL_CORRECTION"}` (`:45`); `_check_revalidation_chain` + `_resolve_publication_revalidation` reason-membership (`:994-995,:1115-1116`); new `editorial_bindings` exact-match enforcement (proposal/retention/staged/scope SHAs + before/after digests vs live + context) when reason is editorial | `revalidate_publication_surface`, `resolve_active_publication_revalidation`, `_resolve_publication_revalidation`, `_check_immutable_revalidation_rows`, `_check_revalidation_chain`, `_check_revalidation_agreement`, `built_checked_pending_publication_basis`, `_collect_pending_rows`, `_verify_pending_binding`, `_validate_agent_state/validate_agent_state`, `resolve_checkpoint_artifact/_resolve_checkpoint_artifact` (all reused, not rewritten) | Existing chain already enforces rows/chain/agreement/pending/State for any reason; only membership + bindings check missing. No lifecycle/transition/human-gate logic change. |
| `scripts/survey_editorial_admission_v2.py` | ADD (1 module): `admit_prepare/admit_install/admit_finish/verify_editorial_admission` + `EditorialAdmissionError` + internal `_EditorialInstallBasis` | Calls (never patches): `p1mod._Collector` (via P2R Session, not direct), `retention.capture_retention/verify_retention` + `_Session.safe_read`, `staged.materialize_staged_source/verify_staged_source`, `current_authority.observe_current_authority` (prepare only), `longform.validate_longform_reader_input/canonical_reader_bytes/load_derivation_for_readback` OR `weekly.validate_reader_input/load_derivation`, `longform_generated.build_receipt/validate_receipt` OR `weekly.build_receipt/validate_receipt`, `reader.build_manuscript_manifest/validate_manuscript_manifest/build_review_record/validate_review_record`, `quality.build_bundle/validate_bundle/bind_pdf_authority`, `surface_gate.evaluate_reader_surface_gate/validate_reader_surface_gate/load_and_validate_*`, `publication.build_candidate/validate_candidate`, `agent_control.revalidate_publication_surface/resolve_active_publication_revalidation/validate_agent_state/built_checked_pending_publication_basis`, `core.repo_local_path/sha256_*/contract_identity/repository_commit_sha`, `stage.validate_stage` (post-finish regression only) | Owns ONLY the previously unowned window (live TeX/QA/PDF/Candidate temp+replace + versioned QA generation + bounded context). All authority checks delegate to existing public validators with explicit contexts; no validator logic duplicated, no bypass flags. |
| `scripts/survey_longform_generated_v2.py`, `scripts/survey_weekly_derivation_v2.py`, `scripts/survey_reader_surface_gate_v2.py`, `scripts/survey_reader_publication_v2.py`, `scripts/survey_quality_v2.py`, `scripts/survey_stage_validation_v2.py`, `scripts/survey_publication_v2.py`, `scripts/survey_production_v2.py`, `scripts/survey_human_gate_v2.py`, `scripts/candidate_selection_gate.py` | NO CHANGE (reuse as callers with explicit args) | `validate_receipt` (both routes, with `state_path` + optional `pending_basis`), `load_derivation[_for_readback]`, `validate_reader_surface_gate(...,expected_manuscript_path,state_path)`, `validate_manuscript_manifest`, `validate_review_record`, `validate_bundle`, `validate_stage`, `validate_candidate/build_candidate`, `repo_local_path/contract_identity`, Human Gate `record/approve` (not called by admission) | Canonical paths + strict State + FILE-byte replay + check families already correct for live after-bytes; versioned-path allowance would fork every consumer (§2.6 rejected). `candidate_selection_gate` never called (Evidence Selection ≠ Publication Candidate). |
| `scripts/survey_editorial_correction_proposal_v2.py`, `scripts/survey_editorial_retention_v2.py`, `scripts/survey_editorial_current_authority_v2.py`, `scripts/survey_editorial_staged_source_v2.py` | NO CHANGE | `capture_retention/verify_retention`, `observe_current_authority`, `materialize/verify_staged_source`, P1 rederivation + `_validate_scope` via narrow Session | P1/P2R/P2V/P3S boundaries preserved; admission composes them, does not patch them. P1 retention plan SHOULD include candidate COPY row when candidate exists (else `prepare` refuses `CANDIDATE_RETENTION_MISSING` — a fixture/proposal fix, not a P1 code change). |
| `tests/` | ADD new behavioral tests only (new files, e.g. `tests/test_editorial_admission_v2_*.py`); NO edits to `old13+1/25/26` suites, no full-suite transfer | Exercise `admit_prepare→install→finish→verify` on real synthetic fixtures (§§6–7) + negatives/oracles (§8) + regressions (DM001/019 Freeze pair, W1 4-line equality, DM004 `validate-state` containment, LF-1/LF-2I scoped no-write, P1/P2R/P2V pins) | Proves new authority without rewriting old proofs; decorative count inflation forbidden. |

## 6. Exact fixture recipe (meaningful independent SOURCE commit before authority, not recipe-only)

Prior §7.2 allowed “fixture recipe commit” (JSON recipe) before authority. Astra blocker 6: implementation SOURCE + contract must be committed in a meaningful independent Git BEFORE authority creation; uncommitted worktree or recipe-only commit must never be renderer basis.

**Recipe (per route; Longform + Weekly envelope each need one):**

1. Independent fixture Git DB (new `git init`, inert origin `https://example.invalid/...`, no alternates/hardlinks, process-scoped `user.name=editorial-fixture` / `user.email`): commit `F0` = minimal fixed-baseline source tree sufficient to run derivation+receipt+Gates (config `survey-production-v2.json` with `WEEKLY`+`WEEKLY_MAGAZINE` or `THEMATIC`+`LONGFORM_SPECIAL` profiles, `survey-production-profile.json`, `production-state.json` at `DRAFT_COMPLETE→VALIDATED_DRAFT` with `validation` checkpoint `passed` + architecture approved + preview pending + freeze/release pending, full checkpoint chain bytes referenced by State, `reader-surface-input-v2.json` + `interactive-semantic-publication-input.json` + drafting archive + evidence/screening/discovery/materiality/selection/architecture/draft packages, canonical `survey_root/{main.tex,references.bib}` + `templates/survey/jgaisurvey.sty`, `validated-source-manifest.json` receipt `ESTABLISHED` with `current_tools{repository_commit_sha=F0, contract, closure}`, QA set `reader-manuscript/quality-bundle/semantic/visual/gate` all `PASSED/PASS` binding F0 bytes, `publication-surface-revalidation` absent or prior `REVIEWED_CORE_CHANGE` record if testing second-correction, NO `publication-candidate-v2.json` yet OR one healthy same-before candidate per §2.11). `F0` message: `fixture(<route>,<epoch>): independent implementation source before authority`. Record `F0 SHA` (40-hex).
2. Commit `F1` = authoring change only (the editorial prose fix): modified authoring input (`publication-semantic-input` JSON or equivalent per route) + `proposed-reader.json` (canonical bytes via route `canonical_reader_bytes`/`validate_reader_input`) + `change_description` (non-empty truthful editorial reason, e.g. `correct vendor model name + citation year in Weekly envelope currentEpoch table; no architecture change`). No authority files in `F1` (no receipt/QA/Candidate/State/revalidation). `F1` is the renderer basis; `verify_tool_basis` / `_verify_head_bytes` / `current_closure` pin `F1` as `renderer_commit`.
3. Authority creation order AFTER `F1` committed: `P1 proposal (PROPOSED, basis=F1 State/validation/receipt/commit/contract + proposed=F1 authoring/proposed-reader)` → `P2R capture (CAPTURED, retained COPY of before TeX + KEEP of upstream + candidate COPY if present)` → `scope review (immutable proposed-reader path)` → `P2V-before (SCOPE_BOUND, HEAD=F1)` → `P3S staged (STAGED_ONLY, render proposed via route renderers)` → `admit_prepare (context freeze, HEAD=F1)` → `admit_install (live TeX F1-staged bytes)` → `admit_finish (PDF+QA live, revalidation rN with editorial_bindings{proposal=F1 proposal SHA, retention, staged, scope}, State update, fresh Candidate)` → normal `approve_publication_preview` (Human, NOT fixture) → `build_freeze` etc. No step uses uncommitted bytes as basis; `producer_head` provenance cites `F1`, HEAD equality never required after `F1` (artifact-only HEAD compat, P3S S5).
4. Fixtureepoch: `currentEpoch` means the fixture State’s `temporal policy` / `as_of` window covers the issue’s current edition window (Weekly envelope `ROLLING_WINDOW` or Longform `BOUNDED_PERIOD` per Profile), not a stale window. R1 interactions: fixture State must be post-`refresh-mechanical-evidence` if the route needs it (mechanical rows current), otherwise `prepare` must refuse `MECHANICAL_STALE` rather than silently using stale Evidence.

## 7. End-to-end sequences (Longform + Weekly envelope, currentEpoch, R1 interactions)

Common prelude (both routes): independent DB `F0→F1` per §6 → `P1→P2R→scope→P2V-before→P3S→admit_prepare` (all `REFUSED_PRE_WRITE` on any drift; `TOOL_DRIFT` before any live write).

**Longform (`THEMATIC/LONGFORM_SPECIAL`, `LONGFORM_GENERATED_V1`):**
`admit_prepare` pins `before_live{main,bib,sty}` + `before_qa{manuscript,bundle,semantic(PASS),visual(PASS),gate(PASSED),receipt(ESTABLISHED),pdf(REPOSITORY_FILE),reader_input}` + `before_candidate` verdict + `predecessor` (null or prior record) → `admit_install` replaces 3 TeX from staged (`render_main/render_bibliography` Longform + style copy already verified) → `admit_finish`: PDF build live → versioned manuscript (Longform `architecture_coverage` with numbered `Section N/Subsection N.M` traceability + `reader_requirements`, `authored_by=editorial-correction:<proposal_id>`) → versioned bundle (DETERMINISTIC checks + `bind_pdf_authority` REPOSITORY_FILE) → versioned semantic (`SEMANTIC_EDITORIAL` full family + `fidelity.validate_review_depth`) + visual (`VISUAL` full family) → versioned Gate (`evaluate_reader_surface_gate` + lexical lint 0 blocking) → versioned receipt (`longform.build_receipt` with `load_derivation_for_readback` context + canonical `:720-730` paths + FILE-byte replay) → validate all versioned vs live → owned-install QA+PDF+receipt (+reader_input iff changed with `validate_longform_reader_input` + `canonical_reader_bytes` equality) → `revalidate_publication_surface(REVIEWED_EDITORIAL_CORRECTION, reason="editorial correction <proposal_id>: <change_description>", executor, recorded_at)` → `resolve_active(live=True)` PASS → `build_fresh_candidate_after_rebind` (`build_candidate` with after-refs + `_exact_pdf_page_count` + `candidate_sha256`) → `validate_candidate` PASS → normal Preview/Freeze/Release path (`approve_publication_preview` Human → `build_freeze` preflight+owned pair → `validate_release_manifest`).

**Weekly envelope (`WEEKLY/WEEKLY_MAGAZINE`, `WEEKLY_GENERATED_V2`, currentEpoch envelope):**
Same with Weekly renderers (`weekly.render_main/render_bibliography`, `validate_generated_closure`, `validate_reader_input`), Weekly receipt (`weekly.build/validate_receipt` with `pending_basis` when `VALIDATED_DRAFT` strict State sees changed rows — constructed inside `finish` via `built_checked_pending_publication_basis`, never caller-supplied), Weekly Gate derivation (`WEEKLY_MAIN_BIB_STYLE` scope), envelope `reader-surface-input` + `quality` + `subject-entity-property-binding` sibling handling per `survey_weekly_semantic_publication_v2` (no envelope metadata overbind; `supporting_files` exactly `BIBLIOGRAPHY+STYLE` + `primary`).

**R1 interactions:** if Weekly mechanical Evidence refreshed (`refresh-mechanical-evidence`) between `prepare` and `finish`, `finish`-entry re-derivation must see same `accepted_refs` as `prepare` context; changed Evidence → `UPSTREAM_DRIFT` refuse (no silent rebase). Repeated correction (§2.10) uses updated predecessor/before sets.

## 8. Negatives / failure-recovery oracles (must all be tested, exact codes)

| Trigger | Phase | Expected `code` / `disposition` | Owned / preserved |
|---|---|---|---|
| Empty `reason` or `reason_class=REVIEWED_CORE_CHANGE` for editorial bytes | `finish/REVALIDATION_COMMIT` | `REASON_EMPTY` / `REASON_CLASS_MISMATCH` / `REFUSED_POST_INSTALL` | Nothing written (record/State/Candidate untouched) |
| `change_description` ≠ proposal `proposed.change_description` or `proposal_id/issue/profile/route` mismatch | `prepare`/`finish` | `PROPOSAL_MISMATCH` / `REFUSED_PRE|POST` | Live preserved |
| Scope `ordinary-without-block` or tampered `proposed_reader`/`scope_review`/`retention`/`staged` bytes | `prepare` | `SCOPE_INVALID` / `RETENTION_INVALID` / `STAGED_INVALID` / `REFUSED_PRE_WRITE` | Live untouched |
| `TOOL_DRIFT` (HEAD/contract/closure differs from pinned `renderer_commit`/receipt `current_tools`) | any pre-write | `TOOL_DRIFT` / `REFUSED_*` | Live preserved |
| Live TeX `!= expected-old` at install-entry or pre-replace | `install` | `LIVE_BEFORE_DRIFT` / `REFUSED_PRE_WRITE` | Live preserved as found |
| Short/zero/fsync/close/replace/readback fault on any live target | `install`/`finish` | `*_REPLACE_INCOMPLETE` / `INCOMPLETE`, or `INDETERMINATE` when complete-valid bytes retained but close failed | Owned temp rule (§2.1); live preserved as found (old or new-complete); never success |
| Same-byte replacement swapped after create (different inode, same bytes) | any install | Identity mismatch → retain, `FOREIGN_EVIDENCE_PRESERVED` / manual recovery | Never unlink foreign bytes |
| Symlink leaf/ancestor or non-reg target or `..`/backslash escape | preflight | `*_ALIAS` / `*_ANCESTOR` / `REFUSED_*` | Nothing written |
| `before_candidate` foreign/diverged/invalid/alias | `prepare` | `CANDIDATE_FOREIGN|DIVERGED|INVALID|ALIAS` / `REFUSED_PRE_WRITE` | Live untouched |
| `before_candidate` adopted (bound by Preview approval/Freeze/Release) | `prepare`/`finish` | `CANDIDATE_ADOPTED_REFUSAL` / `REFUSED_*` | Live preserved; needs decided-history contract (out of R1) |
| Healthy same-before candidate present (exact 6-field equality, unadopted) | `prepare` | `OBSERVED_HEALTHY_SAME_BEFORE` (proceed, NOT reject) → after `finish` becomes `STALE_AFTER` (superseded, retained) | Provenance preserved; usability gap closed |
| Versioned QA fails any public validator vs live after-bytes (manuscript/bundle/semantic/visual/Gate/receipt, wrong kind/check family/page-count/digest/derivation) | `finish/QA_VALIDATE_LIVE` | `QA_VALIDATION_FAILED` / `REFUSED_POST_INSTALL` | Live TeX new held (`TRANSITION_INVALID_LIVE`), QA/record/State/Candidate unwritten; manual recovery (fix QA or restore TeX from retained COPY) |
| `DIRECT_PRIMARY` gate derivation for generated correction | `finish` | `DIRECT_PRIMARY_REFUSED` | No admission |
| Sequence collision (`rN` exists/symlink) or State `!= expected-old` pre-replace or HEAD changed | `finish` | `REVALIDATION_RECORD_COLLISION` / `STATE_DRIFT` / `HEAD_CHANGED` | Per controller rollback taxonomy (`:2047-2200`); unknown bytes never deleted |
| Post-replace readback mismatch | `finish` | `POST_REPLACE_MISMATCH` / manual recovery | Record+State preserved as found |
| Crash/power-loss mid-window | any | `TRANSITION_INVALID_LIVE` held; recovery from retained COPY + staged bytes + context digests; no auto-rollback deleting unknown bytes | No CAS/crash-atomicity claim |

Success oracles (positive): `prepare` context freeze with `SCOPE_BOUND` + `OBSERVED_HEALTHY_SAME_BEFORE|NO_CANDIDATE_BEFORE`; `install` 3 TeX `temp+replace` + `TRANSITION_INVALID_LIVE` ack; `finish` PDF+6 QA+receipt live-validated + `revalidation rN (REVIEWED_EDITORIAL_CORRECTION + editorial_bindings)` + strict `validate_agent_state` PASS + `resolve_active(live=True)` PASS + fresh `validate_candidate` PASS + `verify_editorial_admission` historical replay PASS. No low-level `exit0`/file-exists/Gate-PASS alone counts as admission.

## 9. Cost / removed work / alternatives (qualitative genuine large, no strawman)

**R2 cost is genuinely large (not “P3S-scale”):** dominant costs are (a) owned `temp+replace` for 12–16 live targets with ancestor/fd/readback discipline + per-file failure taxonomy, (b) versioned QA generation (manuscript with architecture coverage + bundle DETERMINISTIC + 2 full review families + Gate lint + receipt FILE-byte replay) with genuine ChatGPT semantic/visual effort (not synthetic PASS), (c) live PDF build + log retention + page-count binding, (d) bounded-context plumbing + re-derivation at 3 boundaries, (e) fresh Candidate + Preview/Freeze/Release return path, (f) fixture `F0→F1` independent source commits per route + full negative/recovery matrix + regressions. Prior “P3S 3A/0M same-scale” estimate is WITHDRAWN.

**Removed operator work / new setup / maintenance / manual recovery (must be shown in R2/R3 tables, not asserted here):**
Removed: hand-written status/helper往復 for corrections (unconnected P1/P2R/P2V/P3S invocations + manual TeX copy + manual QA re-invocation + manual Candidate JSON edit), divergent-overwrite triage from unowned writes, second manual Preview/Freeze due to stale Candidate. New setup: 1 admission module + 1 schema enum/field + 3 controller hunks + fixture DBs (independent, inert). Ongoing maintenance: editorial_bindings enforcement + mixed-chain compatibility + retained COPY storage per correction (bounded, per-proposal dir). Manual recovery: ONLY on fail-closed refusals/`INCOMPLETE`/`INDETERMINATE` with preserved bytes + exact `owned/live_preserved_as/expected_old/new` diagnostics (no silent repair, no generic rerunner certification).

**Coherent alternatives compared (not unsafe strawmen):**

- **Alt-V (versioned QA + pointer switch, REJECT §2.6):** coherent but infeasible-cheap only if indirection existed. Real cost: ≥8 logic + 4 schema + contract-hash + migration + double-readback. Loses canonical-consumer reuse. Rejected with explicit caller list, not “unsafe generic”.
- **Alt-R (parallel editorial pointer + separate record, REJECT §2.4):** coherent as greenfield authority but zero consumer coverage; real cost is new resolvers + precedence + migration. Rejected on coverage/cost, not on “generic bypass” caricature.
- **Alt-S (status quo: staged only, no admission, REJECT):** leaves R1 exit unmet (roadmap §6: admission target undecided → build/writer without operation). Cost is continued dual maintenance (old manual correction + unconnected helpers) with no lifecycle return. Rejected per roadmap mission (moving work is not saving).
- **Alt-B (broad same-State rewrite / generic Gate invalidation / Candidate-as-publisher, REJECT):** would close DM021+DM022 in one permission change but spoils frozen authority (pre-Architecture vs post-VALIDATED stage confusion, SHA-bound checkpoint + review-index + history shape rework). Rejected per Summary tightly-gated append-only requirement, not per path-count.

## 10. DM022 material, distinct stages (no new permission gate for analysis)

DM022 (`EVIDENCE_REVIEWED` pre-Architecture, accepted Evidence/Views/Materiality update problem, `OPEN_CORE`) is material input per roadmap §3 + intake correction (Worker “no impact” withdrawn). Common principles reused: SHA-bound authority, append-only lineage (old bytes + old→new SHA), fail-closed refusal, deterministic revalidation, original Discovery/Screening `INSPECT` retention, canonical checkpoint/history binding, no direct overwrite/manual rollback/forged `REQUEST_CHANGES`. Stage/review/acceptance differences kept distinct: DM022 target is Evidence/Cards/Views/Materiality/Completeness with affected-ID allowlist + Sol decision + HEAD/Tree/work guards; DM021 target is reader→staged TeX→live `survey_root` with scope+semantic/visual+Gate+Human Preview + TeX ownership + Candidate collision + Freeze/Release return. No repair batching across stages. No new Human permission gate is added for analysis: continued work stays under existing Human delegation (replan README R1 contract); ordinary candidate commit/Production mutation/adoption remain Human-owned per AGENTS.md. R3 will judge DM022 applicability + needed repair/existing-alternative effectiveness on fixed source (`c8d0ecc/blob0a0fe3eb/Issue562`), without refetching `r12`/`sources/2026-W40/*`/`#515`/`W41`/`83f581eb` absent new explicit authorization.

## 11. No-go handling (no punt to helper-only analysis)

If R2 implementation hits an essential contradiction, it must stop with reasoned `NO-GO`, not another analysis slice:

- Example: live LuaLaTeX PDF build cannot be made deterministic/owned in R2 env (missing toolchain/fonts, non-reproducible bytes, `validate_survey_build_directory` + `validate_generated_closure` unsatisfiable). Then: `NO-GO: finish PDF_BUILD infeasible under fixed toolchain; alternative versioned-PDF-transfer would require receipt `pdfAuthority` + `bind_pdf_authority` + Candidate `pdf` + Freeze snapshot path changes (list exact functions); without PDF there is no manuscript/bundle/review/Candidate authority, therefore no admission; whole completion stays OPEN; staged-only + manual build remains unadopted helper, not operation.`
- Example: `before_candidate` adopted-history case. Then: `NO-GO for decided history under R1; needs separate decided-history contract (not R2); R1 stays bounded to pending-preview corrections.`
- Any `NO-GO` preserves all evidence, names the exact interface difference (file:line + expected vs actual), states what usability is lost (e.g. Weekly viability, Special coverage), and proposes a scoped alternative with cost. Key predicates are never punted to “more helper analysis”.

## 12. Root key decisions + line hotspots (for Astra + fresh author-independent design review)

**Key decisions for root (adopt / reject / amend):**
1. `REVIEWED_EDITORIAL_CORRECTION` inside existing chain (E1) vs parallel pointer (E2) — §2.4 table. Recommend E1.
2. Live `temp+replace` for all 12–16 targets (§§2.1/2.7) vs `O_EXCL` 3-file — must adopt temp+replace; O_EXCL on existing is infeasible.
3. `P2V-before` once + after-validators (§2.2) vs writer-internal `P2V×2` same-before — must adopt split; same-before after install is correctly failing.
4. `prepare/install/finish` with bounded `TRANSITION_INVALID_LIVE` (§§2.6–2.8) vs pointer-switch versioned (Alt-V) — recommend bounded window; Alt-V costed at ≥12 files + migration.
5. Early-scope vs postrender-QA vs Human-Preview separation + explicit contexts + no bypass (§2.5) — must adopt; “call validators” alone is insufficient.
6. Candidate `OBSERVED_HEALTHY_SAME_BEFORE` proceed + `COPY_BEFORE_REPLACEMENT` retention + `build_candidate` replacement writer (§2.11) vs blanket reject / Candidate-as-publisher — must adopt supersession predicates.
7. Exact impact table (§5) with no path budget vs `3A/0M` — must adopt table.
8. Fixture `F0→F1` SOURCE commits before authority (§6) vs recipe-only — must adopt SOURCE commits.
9. `NO-GO` with exact interface difference (§11) vs predicate punt — must adopt no-punt rule.

**Hotspots to re-read (restored DB, not workspace):**
- `scripts/survey_agent_control_v2.py:45` (reason set), `:685-743` (roles/pending rows), `:746-808` (pending binding/basis), `:847-949` (immutable rows), `:952-1017` (chain), `:1020-1081` (agreement), `:1084-1187` (resolve active/historical), `:1500-1556` (preserved provenance), `:1604-1642` (exclusive record), `:1666-1770` (State temp+replace), `:1773-2201` (revalidate incl. `:1898-1944` QA + `:1995-2046` record/State commit + `:2047-2200` rollback taxonomy).
- `scripts/survey_production_v2.py:32-44` (lifecycle), `repo_local_path/sha256_*/contract_identity/repository_commit_sha` (authority primitives).
- `schemas/survey-production-state.schema.json:77` (existing `publication_revalidation_provenance`, no editorial pointer), `schemas/publication-surface-revalidation.schema.json` (`reason_class` const → enum + `editorial_bindings` addition point).
- `scripts/survey_longform_generated_v2.py:606-638,641-663,665-758` (build/inspect/validate receipt; `:707-730` canonical, `:698-706` readback, `:734-757` FILE replay).
- `scripts/survey_weekly_derivation_v2.py: load_derivation/build_receipt/_inspect/validate_receipt` (canonical outputs, pending_basis branch).
- `scripts/survey_reader_surface_gate_v2.py: _inspect_gate_record / validate_reader_surface_gate / _derivation_for_manuscript / evaluate_reader_surface_gate` (inspection≠admission, `expected_manuscript_path+state_path` mandatory, receipt rebinding).
- `scripts/survey_reader_publication_v2.py: build_manuscript_manifest / validate_manuscript_manifest / build_review_record / validate_review_record / build_reader_surface_gate` (refuse-overwrite, digest, check family, fidelity).
- `scripts/survey_quality_v2.py: build_bundle / validate_bundle / bind_pdf_authority` (refuse-overwrite, DETERMINISTIC, REPOSITORY_FILE).
- `scripts/survey_publication_v2.py:668-746,749-814,817-869,171-245,323-430,490-558,561-657,919-963` (candidate build/validate, preview approval, Freeze preflight/owned install/return).
- `scripts/candidate_selection_gate.py:57-66,123-216` (Evidence Selection, NOT Publication Candidate — do not cite for admission).
- `scripts/survey_editorial_correction_proposal_v2.py:822-862` (observed Publication Candidate, 6-field equality, COPY/unadopted, no ownership), `:1710-1737` (BASIS/PROPOSED mismatch), P1 `_validate_scope` (early scope via narrow Session).
- `scripts/survey_editorial_retention_v2.py: capture_retention/verify_retention/_Session` + `scripts/survey_editorial_current_authority_v2.py: observe_current_authority` (prepare-only) + `scripts/survey_editorial_staged_source_v2.py: materialize/verify_staged_source` (staged 4-file, manifest-last, 37 deps, `TOOL_DRIFT`, `_SessionScopeReader`).
- `scripts/survey_stage_validation_v2.py: _validate_stage_semantics` DRAFT_COMPLETE branch + `config/survey-production-v2.json` (`state_authority`, `stage_plan.DRAFT_COMPLETE` 6 artifacts + Gate).
- `schemas/publication-candidate-v2.schema.json` + `schemas/reader-manuscript-v2/quality-regression-bundle-v2/publication-review-record-v2/reader-surface-gate-v2` (live QA shapes reused unchanged).

Fresh author-independent design review should verify §§2–5/7–8 gaps, especially: editorial `reason` truthfulness binding, `editorial_bindings` required-field completeness, live PDF build feasibility, `before_candidate` COPY-row requirement, Weekly/Longform route delta漏れ, Freeze-pair coexistence, second-correction predecessor handling, and cost/authority scope. Design PASS (if granted) is not implementation/application acceptance; R2 selection stays with Astra return; stop at Human Commit Point.

## 13. Limits (no PASS claim)

No code/tests run, no PDF built, no genuine review/Human decision, no Freeze/Release/migration/adoption, no full-suite inference, no net-savings measurement, no global CAS/crash-atomicity/continuous no-drift, no all-profile claim. Missing `26309` blobs / unbundled runtime / `__pycache__` absence inherited. Synthetic fixture reviews are never genuine approvals; `STAGED_ONLY`/`ADMITTED_AWAITING_PREVIEW` are byte-consistency + replay only. This correction is author-side architecture input for Astra decision + fresh design review, not independent audit, not implementation PASS, not adoption approval. Stop at Human Commit Point; ordinary Commit/Push Human-owned unless explicitly authorized.

*End of correction.*
