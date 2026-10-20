# R3 canonical live replacement + durable checked context — author-side analysis (Worker A)

> Role: author-side architecture Worker A. NOT independent reviewer, NOT root/Astra,
> NOT Human Gate. No runtime implementation, tests, builds, fixtures, Git mutation,
> network, or commit in this unit. All source claims are read-only observations of the
> actual available candidate below; line numbers refer to that tree, not the workspace.
> Companion source-availability record: `current-source-observation.md` / `.json`
> (same packet). Immutable-versioned-set design is owned by another Worker; DM022/R1
> edge mapping is owned by Explore. This file designs ONLY the canonical side and the
> comparison inputs root needs. It does not select between the two options.

- Actual source (read-only): `/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60`
- Detached HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`, tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`, status `4M18A22` (verified this unit, see companion observation; 22/22 SHA/bytes/mode match `complete22-manifest.json`, patch `7c82ec47…` 1233999 B).
- Governing assessment: `outputs/rephase-1-initial-build-integration-assessment.md` §5 (R3).
  Mandatory bounds: `notes/rephase-1-initial-build-integration/astra-closeout-resolution.md`,
  `independent-final-resolution.md` §§2–6, `independent-postfix-visual-resolution.md`.
- Rejected predecessors (read to avoid repetition, NOT resubmitted):
  `notes/rephase-1-roadmap-replan-20261019/admission/integrated-admission-contract-analysis.md`
  (parallel pointer + O_EXCL-on-live + P2V×2-same-before + recipe-only fixture + "call validators" cycle gap —
  8 Astra blockers, NO-GO) and `integrated-admission-correction.md` (existing-chain E1 +
  prepare/install/finish + temp+replace — the R1 corrected baseline this design builds on
  and explicitly deltas from, see §1).

## 0. Decision

**SELECT (candidate): canonical live replacement of the edition publication surface,
admitted through the EXISTING `publication-surface-revalidation` reason chain extended
with a truthful editorial reason, driven by a DURABLE disk-persisted checked context
across three operator phases, with EXTERNAL genuine semantic/visual review inputs at
both the pre-TeX and postrender boundaries.**

This is a coherent candidate design, NOT a proof of feasibility and NOT an implementation
PASS. It becomes implementation-selectable only after (a) fresh author-independent design
review, (b) Astra comparison against the immutable-versioned-set option (§16), and
(c) R2-style real-build oracle evidence on actual accepted fixtures. §17 lists the exact
conditions under which this candidate must instead return source-grounded NO-GO.

Deliberate deltas from the R1 correction baseline (why this is not a resubmission):

1. **New receipt/Gate/loader entries are REQUIRED, not zero-change reuse.** The correction's
   "0 receipt/Gate logic changes" claim does not survive the authored→reader derivation
   facts in §2: a changed proposed reader cannot replay from old authored bytes through
   the current strict loaders, and versioned-first QA cannot be pre-validated through
   canonical-path-only public validators. §4 specifies the exact new entry points.
2. **Versioned NEW authored input is mandatory.** Copying a changed reader over the live
   reviewed input while reusing old authored bytes is refused by construction (§2).
3. **After-install readback uses a newly designed no-cycle after-context**, not a second
   P2V-before and not any caller enum/`verified_set`/generic pending bypass (§5).
4. **Operation intent is durable on disk**, because genuine reviews arrive over a long,
   unquantified window during which live is acknowledged invalid (§6). Memory-only
   transaction context is insufficient and is rejected here.
5. No path-count budget is offered (no "3A/0M"); §12 gives the exact impact table with a
   caller reason per touched path. Existing consumers are changed where the contract
   requires it, never by silent assumption.

## 1. Actual-source facts grounding this design (candidate tree)

All paths relative to the candidate root. Verified by read-only inspection this unit
(grep + targeted reads; no import, no execution).

**Lifecycle/State hardness.**
- `scripts/survey_production_v2.py:32-44` — 11-state `LIFECYCLE`; `transition_state` allows
  only `current+1`. Same-State supersession does not exist. (Shared DM021/DM022 hardness;
  stages differ — Explore's mapping, not decided here.)
- `schemas/survey-production-state.schema.json` — `publication_revalidation_provenance` is
  an optional existing pointer; no editorial pointer field exists.
- `schemas/publication-surface-revalidation.schema.json:26` — `reason_class` is currently
  `{"const": "REVIEWED_CORE_CHANGE"}` (single). `required` includes `reason_class` (line 10).

**Pending/checked-row machinery (the existing checked context for the commit step).**
- `scripts/survey_agent_control_v2.py:45` — `REVALIDATION_REASON_CLASSES={"REVIEWED_CORE_CHANGE"}`.
- `:685-693` `_publication_revalidation_roles` — 6 DRAFT_COMPLETE artifacts + canonical
  `reader-surface-gate` = the only 7 rows `_collect_pending_rows:711-743` can mark changed;
  any other changed path → `changed noncanonical or upstream role/path` refusal;
  `require_change=True` demands ≥1 changed publication byte.
- `:746-781` `_verify_pending_binding` + `:784-808` `built_checked_pending_publication_basis` —
  fresh context built from actual State/checkpoint/files and rechecked (State path
  canonical, State/config bytes, HEAD, validation ref, row snapshot, predecessor pointer).
- `:696-708` `_pending_conditions` — VALIDATED_DRAFT + architecture approved + preview
  pending + freeze/release/preview checkpoints pending + exception inactive.

**Exact (name,path) union + active-before binding (inspected, not assumed).**
- `:847-949` `_check_immutable_revalidation_rows` — every `superseded_artifacts[]` row must
  match a prior-checkpoint `(name,path)` key with equal `prior_sha256`, changed bytes,
  canonical role/path, containment under `publication_dir|survey_root`, and (live) exact
  `new_sha256`/byte-count; every `preserved_artifacts[]` row must equal its prior SHA;
  then `seen != set(prior_rows)` → `artifact row union differs from prior checkpoint` (line 916-917).
  `validation.{manuscript,quality_bundle,semantic_review,visual_review,pdf}` refs must bind
  to the effective row SHAs at `:926-948`. This is the preferable consumer set: any new
  authority MUST satisfy this union/binding check, which is why a parallel unconsumed
  pointer was correctly rejected — it has zero such consumers.
- `:952-…` `_check_revalidation_chain` — walks `supersedes` links with byte-identity,
  cycle detection, issue/prior-checkpoint match. Mixed-reason history is structurally
  supported (membership is the only reason check at `:994-995,:1115-1116`).
- `:1084-1187` `resolve_active_publication_revalidation` — live + historical resolution;
  `:1115-1116` reason membership.
- `:1604-1642` `_exclusive_create_record_bytes` — O_EXCL lawful ONLY for never-existing
  sequence files (fd dev/ino identity + same-fd readback). `:1666-1770`
  `_atomic_replace_state_bytes` — temp+`os.replace` with double expected-old recheck.
  These two are the ownership precedents: O_EXCL for new files, temp+replace for existing.
- `:1898-1944` — revalidation QA block calls `reader.validate_manuscript_manifest`,
  `quality.validate_bundle`, `reader.validate_review_record` ×2
  (`SEMANTIC_EDITORIAL`/`VISUAL`), `surface_gate.validate_reader_surface_gate` with
  mandatory `expected_manuscript_path` + `state_path` (`:1931-1938`), then requires all
  bundle checks PASS (`:1941-1944`). Final commit path already exists; only reason
  membership + bindings enforcement are missing.

**Receipt strictness (cycle source + authored boundary).**
- `scripts/survey_longform_generated_v2.py:665-758` `validate_receipt` — reloads persisted
  semantic review itself (`:686-697`), re-derives the reader via
  `longform.load_derivation_for_readback` from the authored `publication-semantic-input`
  (`:698-706`), pins canonical `survey_root/{main.tex,references.bib,jgaisurvey.sty}`
  outputs (`:707-714`), pins canonical edition siblings
  `publication/v2/{reader-surface-input-v2.json, interactive-semantic-publication-input.json,
  validated-source-manifest.json}` (`:720-730`), demands reviewed-reader FILE bytes ==
  `canonical_reader_bytes(rederived)` (`:741-742`), then deterministic TeX replay
  (`:744-757`). Consequence (§2): with UNCHANGED authored bytes, a CHANGED proposed reader
  fails at `:735-742` — correctly. Copying the new reader over live input without new
  authored bytes breaks derivation authority; the design must carry new authored bytes
  with old→new lineage and teach the loaders to accept them in the admission scope.
- Weekly `survey_weekly_derivation_v2.load_derivation/build_receipt/validate_receipt` —
  same shape with route-local canonical outputs + pending_basis branch (verified by grep;
  full line map is root's hotspot list, §18).

**Gate derivation binds receipt (one direction; no receipt→Gate edge).**
- `scripts/survey_reader_surface_gate_v2.py:1145-1225` `_derivation_for_manuscript` —
  generated routes demand canonical `reader-surface-input-v2.json` name + `publication/v2`
  suffix, sibling `validated-source-manifest.json` revalidation, reviewed-target and
  semantic-review binding, and `receipt.outputs == manuscript.primary+bib+style` with exact
  `survey_dir/{main.tex,references.bib,jgaisurvey.sty}` paths (`:1190-1197`). DIRECT_PRIMARY
  is primary-only (`:1156-1159`) and is REFUSED for generated corrections.
- `:1598-…` `_inspect_gate_record` (never admission alone) + `:1794-…`
  `validate_reader_surface_gate(..., expected_manuscript_path, state_path)` — always
  inspect + derivation replay. Call graph is controller → Gate → receipt → review-loader +
  derivation: a DAG, not a cycle — PROVIDED the admission scope passes explicit contexts
  instead of letting each layer re-resolve strict current State (which is stale mid-window).
  The "cycle" failure mode is re-resolution against stale State, fixed by §5.

**Proposal/P2R/P2V/P3S boundaries (composed, not patched).**
- `survey_editorial_correction_proposal_v2.py:822-862` — Publication Candidate observed via
  canonical Profile `source_root` path, alias refusal, `publication.validate_candidate` +
  exact 6-field active-before equality (`CANDIDATE_DIVERGED` on any field mismatch),
  `CANDIDATE_OBSERVED unadopted`, COPY classification, no ownership. (Evidence Selection
  `candidate_selection_gate.py` is a different authority — never cited for admission.)
- Same module: `publication-semantic-input`/`publication-authored-input` rederivation,
  `canonical_reader_bytes`, nonempty `change_description` (descriptive, not approval),
  supplied-vs-rederived mismatch refusals (~`:1690-1733`), `_validate_scope:1775-…`
  binding the persisted `proposed_reader_ref` (path+SHA).
- `survey_editorial_current_authority_v2.py:101-…` `observe_current_authority(...)` —
  read-only, `RESULT_SCOPE_BOUND` / `RESULT_NEEDS_SCOPE`; valid ONLY pre-install.
- `survey_editorial_staged_source_v2.py:126` `_route_code_deps`, `:209` `_manifest_digest`,
  `:944` `STAGED_ONLY`, `:544,1801` `TOOL_DRIFT`, writer-internal P2V stable-facts-only.
- `config/survey-production-v2.json:339-344` — DRAFT_COMPLETE artifacts
  (`reader-manuscript`, `validated-source→{survey_root}/main.tex`, `publication-pdf`,
  `quality-regression-bundle`, `semantic/visual-review`); `:389-390` `state_authority`.

**Stable Profile/public identity and source paths (confirming the task's identity basis).**
- Profile binds `paths.source_root` / `paths.survey_root`; all canonical admission paths
  derive from them (never hardcoded edition names): State
  `<source_root>/production-state.json` (`state_authority.authoritative_filename`), live TeX
  `<survey_root>/{main.tex,references.bib,jgaisurvey.sty}`, live QA
  `<source_root>/publication/v2/{reader-manuscript-v2.json, quality-regression-bundle-v2.json,
  semantic-editorial-review-v2.json, visual-review-v2.json, reader-surface-gate-v2.json,
  validated-source-manifest.json, reader-surface-input-v2.json,
  interactive-semantic-publication-input.json}`, Candidate
  `<source_root>/publication/v2/publication-candidate-v2.json`. Public identity =
  Profile-bound `(issue_id, research_profile, publication_profile, route)` + survey_root
  basename slug; tag derivation stays internal to validated Candidate-bound Profile
  (DM001/019 precedent, AGENTS.md) — no new identity invention here.

## 2. Authored→reader boundary: new authored input is mandatory

**Rule.** A changed proposed reader MUST arrive with versioned NEW authored bytes plus
explicit old→new authored lineage. Reusing old authored bytes while copying a changed
reader over the live reviewed input is refused (`AUTHORING_LINEAGE_MISSING` /
`READER_DERIVATION_MISMATCH`), because current receipt replay (`§1`, longform `:735-742`)
re-derives the reader from authored + accepted Draft and demands FILE-byte equality.

- New authored input lives versioned under the proposal dir:
  `<proposal_dir>/authored-input.json` (exact filename fixed at implementation; content =
  the route's `publication-semantic-input` shape for the correction, carrying
  `change_description`, `proposal_id`, and unchanged accepted refs).
- Lineage record inside the proposal: `authored_lineage: {old_authored_ref:{path,sha256},
  new_authored_ref:{path,sha256}, accepted_refs_equal: true, draft_untouched: true}`.
- Accepted Draft bytes are NEVER overwritten (P1 `PROPOSED_ARCHIVE_DRIFT/PROFILE_DRIFT`
  precedent; `initialize` destructive refusal). If the correction's accepted refs differ
  from current checkpoint chain → `UPSTREAM_DRIFT` refuse, no silent rebase.
- If P1 proves a prose-only TeX delta with an identical reader object (canonical SHA equal),
  the authored write is identity (`RESUMED_IDENTICAL`, no-op) — the only exception, and it
  must be proved by `canonical_reader_bytes` equality, not asserted.
- Loader/receipt acceptance of the new authored ref is an explicit admission-scoped entry
  (§4), never a standing bypass: old epochs and normal paths resolve authored exactly as
  today.

## 3. Early review target: immutable proposed-reader path

- The review target is the versioned immutable path
  `<proposal_dir>/proposed-reader.json` (P1 `proposed_reader_ref` {path,sha256},
  `proposed_reader_canonical_sha256`), NOT the live `reader-surface-input-v2.json`.
- Early (pre-TeX) scope review = real P1 `_validate_scope` via the P3S narrow Session
  adapter on retained bytes (no live Collector, no dummy HEAD/config). It gates
  prepare→install. `ordinary-without-block` scope is refused in admission.
- Same-SHA different-path rebinding is refused (`PATH_IDENTITY_MISMATCH`; Human Gate
  canonical-bytes precedent). The scope review binds `{path,sha256}` exactly.
- Pre-TeX genuine semantic assessment of the proposed reader / staged trio may additionally
  arrive as an EXTERNAL input (reviewer-owned bytes pinned in the durable intent, §6);
  it never substitutes for `_validate_scope`, and runtime never mints it.

## 4. REQUIRED receipt/Gate/loader changes (exact new entries)

Rationale: (i) versioned-first QA cannot pre-validate through canonical-path-only public
validators; (ii) new authored bytes need an admission-scoped derivation path; (iii) final
commit reuses the EXISTING strict path (§1 `:1898-1944` + `revalidate_publication_surface`)
unchanged in logic. New entries are additive and admission-scoped; normal/old-epoch
behavior is byte-identical.

1. `survey_longform_derivation_v2.load_derivation_for_admission(root, state_file,
   new_authored_path, *, expected_accepted_refs) -> context`
   — same strictness as `load_derivation_for_readback` except the authored input is the
   explicit versioned new-authored file; accepted refs must equal the pinned before-context
   refs or raise `UPSTREAM_DRIFT`. No State-mutation, no pending bypass.
2. `survey_weekly_derivation_v2.load_derivation_for_admission(...)` — Weekly analogue
   (route-local canonical outputs; pending_basis constructed internally at finish, never
   caller-supplied).
3. `survey_longform_generated_v2.validate_receipt_for_admission(root, receipt_candidate_path,
   *, after_ctx: _AfterContext) -> receipt_doc`
   — validates a versioned-first receipt's envelope/self-digest/reviewed-target/semantic binding,
   canonical output PATHS (against after-context survey_root), and deterministic TeX replay of
   after-TeX bytes, WITHOUT requiring the receipt to already live at the canonical receipt path
   and WITHOUT re-resolving strict current State (uses after_ctx pins). Same refusal taxonomy
   as `validate_receipt` plus `AFTER_CTX_MISMATCH`.
4. `survey_weekly_derivation_v2.validate_receipt_for_admission(...)` — Weekly analogue.
5. `survey_reader_surface_gate_v2.validate_gate_for_admission(repo_root, gate_candidate_path, *,
   expected_manuscript: dict, after_ctx) -> gate_doc`
   — inspect + `_derivation_for_manuscript` with an explicit admission derivation resolver
   that calls (3)/(4) instead of the canonical-path receipt validators. DIRECT_PRIMARY refused.
6. Reader/quality/review builders+validators (`build/validate_manuscript_manifest`,
   `build/validate_bundle`, `build/validate_review_record`) — NO logic change; admission calls
   them with explicit paths/identities (authored_by = editorial-correction identity, never
   synthetic Human; full check families; `fidelity.validate_review_depth`; exact PDF page count).

Recursion-freedom: admission call graph is strictly layered —
`admit_finish` → (5) → (3)/(4) → (1)/(2) + review loaders. No layer re-resolves strict
current State or calls back into the admission module. The existing public validators keep
their internal call shape; the `_for_admission` entries are the only new edges, and they
terminate at pinned bytes. No public bearer enum, no caller `verified_set`, no generic
`ignore/pending` flags anywhere in the new module.

## 5. Checked contexts: before (P2V) vs after (new, no-cycle)

- **Before-context** = existing `observe_current_authority` (`SCOPE_BOUND` required,
  `NEEDS_SCOPE` → refuse) run ONCE in `prepare`, plus P1 rederivation, `verify_retention`,
  `verify_staged_source`, early scope, candidate observation, TOOL_DRIFT pinning. Frozen
  into the durable intent (§6). Never re-run after any live write; a post-install
  P2V-before-shaped call is FORBIDDEN to be required (it must correctly report drift).
- **After-context** (`_AfterContext`, internal frozen dataclass, never serialized as
  authority, never consulted by other modules): built in `finish` SOLELY by re-deriving
  from disk — live after-TeX SHAs, built-PDF SHA/page-count, versioned QA SHAs, intent
  digests, State ref (still old until commit), predecessor record — and compared field by
  field against the intent's expected deltas. Fields: `root_resolved, state_ref,
  config_sha256, head, profile_ref, proposal_ref, retention_manifest_ref,
  staged_manifest_ref (+manifest_digest), scope_review_ref, validation_checkpoint_ref,
  predecessor_revalidation_ref?, new_authored_ref + authored_lineage, before_live_refs×3,
  before_qa_refs×8, before_candidate?+verdict, expected_new_tex×3, expected_reader_delta,
  after_live_refs (measured), after_pdf (measured), versioned_qa_refs (measured)`.
  Construction uses retention `_Session.safe_read` narrow pins + `core.sha256_*` over pinned
  bytes (never `Path.read_bytes` on caller strings); HEAD via sanitized `git rev-parse`
  (P2V precedent). Any deviation except the explicitly expected deltas →
  `WINDOW_DRIFT`/`AFTER_CTX_MISMATCH`, fail closed.
- **Current authority after commit** is proved by the EXISTING strict validators, not by the
  after-context: strict `validate_agent_state` PASS + `resolve_active(live=True)` returning
  the new record + `_check_revalidation_agreement`. The after-context is scaffolding for
  safe pre-validation; current authority is the existing chain's verdict.

## 6. Three phases across external review, durable intent, long invalid-live window

**Phase A — `admit_prepare` (read-only + versioned writes outside live).**
- Re-derive/verify P1 (PROPOSED), P2R (CAPTURED), P3S (STAGED_ONLY), P2V-before
  (SCOPE_BOUND), early scope, candidate observation (§9), `_pending_conditions`,
  TOOL_DRIFT. Freeze before-refs + expected-new bytes into durable intent file
  `<proposal_dir>/admit-intent.json` with `phase: PREPARED` (temp+replace, owned; schema:
  exact key list = §5 after-context minus measured fields + `created_by/at/head`).
- No live mutation. Output: intent v1.

**Phase B — `admit_install` (owned live TeX replace only).**
- Re-derive intent pins from disk (State/retention/staged/scope/HEAD/contract/QA/PDF/
  candidate unchanged since PREPARED) or `WINDOW_DRIFT` refuse.
- Replace live `<survey_root>/{main.tex,references.bib,jgaisurvey.sty}` from staged bytes
  via temp+replace per §7 (sibling temp `.<basename>.tmp-admit-<newsha16>` O_EXCL +
  write-loop + fsync + fd identity + same-fd readback + expected-old recheck + `os.replace` +
  post-replace readback). Equal-payload retry → `RESUMED_IDENTICAL`; divergent live →
  `DIVERGENT_LIVE` refuse, preserve for manual recovery.
- Mark intent `phase: TRANSITION_INVALID_LIVE` (TeX new, QA/PDF/State old — explicitly
  acknowledged, bounded by intent, not previewable/freezable/releasable; strict
  `validate_agent_state` MUST fail here, which is the correct fail-closed posture).
- Failure → per-file `*_REPLACE_INCOMPLETE` / `INDETERMINATE`, owned-temp rule (§7),
  live preserved as found, manual recovery required. Never success on partial.

**Phase C — `admit_finish` (build → EXTERNAL reviews → validate → commit → rebind).**
1. Build PDF from live after-TeX under owned-write discipline (existing targets →
   temp+replace; `main.log` diagnostic retained, `main.pdf.sha256` transfer check; same
   deterministic toolchain/pinning as normal publication for the route;
   `validate_survey_build_directory` precheck). Toolchain-infeasible → NO-GO per §17,
   never invented PDF bytes.
2. **External genuine review capture (the long window).** Postrender semantic + visual
   assessments OF the built PDF arrive as EXTERNAL reviewer-owned inputs (files received
   outside the repo or under `<proposal_dir>/received-reviews/`, SHA-pinned into intent
   v2 with reviewer identity + timestamp). Operator materializes them via
   `build_review_record` ×2 with exact page count + full check families
   (`reviewed_by` = actual external identity; `recorded_at` = actual capture time).
   Pre-TeX external semantic assessment (of proposed reader/staged trio) is captured the
   same way at Phase A→B if supplied. RUNTIME NEVER GENERATES A PASS: any review record
   whose bytes were produced by fixture/synthetic/type helpers is refused as authority
   (`SYNTHETIC_REVIEW_REFUSED`); synthetic type-fixtures stay in their separate lane
   (assessment §2 / postfix resolution). Human Preview stays the normal
   `approve_publication_preview` on the fresh Candidate AFTER admission — no new Human
   gate is created, and admission never calls `approve_*` itself.
3. Generate remaining QA versioned-first (`finish-tmp/`), pre-validate versioned vs live
   after-bytes with §4 entries, owned-install QA+PDF+receipt (+reader_input iff
   `expected_reader_delta.changed`, with `validate_longform_reader_input`/`validate_reader_input`
   + `canonical_reader_bytes` FILE equality), then call EXISTING
   `revalidate_publication_surface(reason_class="REVIEWED_EDITORIAL_CORRECTION", reason=<nonempty
   truthful editorial reason binding proposal_id/change_description>, ...)` with
   `editorial_bindings`, then `build_fresh_candidate_after_rebind` + owned install (§9).
4. Intent `phase: ADMITTED_AWAITING_PREVIEW`. Normal Preview/Freeze/Release path resumes
   under existing operators/gates.

**External input ownership.**
| Input | Owner | Form | Pinned where |
|---|---|---|---|
| Correction prose change (authoring) | Correction author | versioned `authored-input.json` + `change_description` | proposal refs |
| Pre-TeX semantic assessment (optional) | External reviewer | reviewer-signed bytes + identity/time | intent v1/v2 `received_reviews[]` |
| Postrender semantic + visual assessments | External reviewers | reviewer-owned files, exact PDF page-count bound | intent v2, then `build_review_record` |
| Human Preview decision | Human (normal gate) | `approve_publication_preview` on fresh Candidate | State/approval paths (existing) |
| Install/commit execution | Operator (Human-delegated) | three phase calls + manual-recovery triage | intent phase markers |

**Long invalid-live window.** Reviews arrive over reviewer time (days possible), NOT build
time. The ONLY evidence-backed durations in this program are the two final selected builds
(~21.0 s / ~23.9 s, assessment §4 — explicitly not total cost) and ~1 GB one-time TeX
setup. No "minutes" claim is made (R1 correction of the prior "minutes" assertion stands).
During the window: (a) live serves old PDF/QA (TeX new but unvalidated — readers see the
old rendered PDF; no claim about serving behavior beyond file bytes is made); (b) strict
validators fail closed (pending rows changed, predecessor stale); (c) intent on disk is the
sole resume basis: `admit_resume` re-reads intent + disk and either continues the phase or
fails closed — never re-baselines silently. Crash/power-loss mid-window → manual recovery
from retained COPY + staged bytes + intent digests; no auto-rollback deleting unknown
bytes; no CAS/crash-atomicity claim (mandatory non-certification, inherited).

## 7. Exact write set, ownership, failure, recovery, resume

One editorial admission (Longform route; Weekly differs only in route/profile/renderers).

| # | Target (Profile-derived canonical rel) | Before (intent) | After (expected) | Ownership | Failure code → disposition |
|---|---|---|---|---|---|
| 1–3 | `<survey_root>/{main.tex,references.bib,jgaisurvey.sty}` | `before_live_refs` {path,sha256,byte_count} | staged bytes {sha256,byte_count} (+style-input equality vs `templates/survey/jgaisurvey.sty`) | temp+replace §6B | `TEX/BIB/STYLE_REPLACE_INCOMPLETE` → INCOMPLETE/INDETERMINATE, owned-temp rule, live preserved as found |
| 4 | `<survey_root>/main.pdf` | `before_pdf` {sha256,bytes,pages} | freshly built PDF bytes | temp+replace | `PDF_BUILD_FAILED` (no QA built; TRANSITION held; rebuild or restore TeX from retained COPY) / `PDF_REPLACE_INCOMPLETE` |
| 5 | `<survey_root>/main.log` (+`main.pdf.sha256` if route present) | before log (diagnostic) | fresh build log | temp+replace (or O_EXCL create if absent) | `LOG_RETAINED` (diagnostic only, never blocks authority) |
| 6–11 | `<source_root>/publication/v2/{reader-manuscript-v2.json, quality-regression-bundle-v2.json, semantic-editorial-review-v2.json, visual-review-v2.json, reader-surface-gate-v2.json, validated-source-manifest.json}` | `before_qa_refs` | generated QA binding after-bytes (manuscript/bundle digests, review SHAs, `PASSED` Gate, receipt SHA) | generate versioned (`build_*` refuse overwrite) then temp+replace + pre-install public validation | `MANUSCRIPT/BUNDLE/SEMANTIC/VISUAL/GATE/RECEIPT_INSTALL_INCOMPLETE`; pre-install validation failure → `QA_VALIDATION_FAILED` / REFUSED_POST_INSTALL (record/State/Candidate unwritten) |
| 12 | `.../interactive-semantic-publication-input.json` (archive) | before archive (KEEP) | UNCHANGED | no write; drift → `ARCHIVE_DRIFT` refuse | — |
| 13 | `.../reader-surface-input-v2.json` (live reviewed input) | before reader SHA | proposed canonical SHA iff `expected_reader_delta.changed`, else identity no-op | temp+replace iff changed (+reader validators + FILE equality) | `READER_INPUT_INSTALL_INCOMPLETE` |
| 14 | `.../publication-surface-revalidation-r{next}.json` (new sequence) | absent (exists/symlink → `REVALIDATION_RECORD_COLLISION` refuse) | new record (editorial reason + bindings + superseded/preserved + validation.* + supersedes) | O_EXCL create (`_exclusive_create_record_bytes` precedent) | record/State per controller rollback taxonomy (`:2047-2200` analogue); unknown bytes never deleted |
| 15 | `<source_root>/production-state.json` | `state_sha` (expected-old) | State + `publication_revalidation_provenance={path,sha256}` (no lifecycle/history/checkpoint mutation) | temp+replace (`_atomic_replace_state_bytes` precedent) | `STATE_REPLACE_UNKNOWN` → preserve record+State, manual recovery |
| 16 | `.../publication-candidate-v2.json` | `before_candidate` + verdict (§9) | fresh Candidate (`READY_FOR_PUBLICATION_PREVIEW`, after-refs, `candidate_sha256`) | versioned `build_candidate` temp then temp+replace (replacement writer, §9) | `CANDIDATE_REPLACE_REFUSED` / `CANDIDATE_INSTALL_INCOMPLETE` |
| — | `<proposal_dir>/{admit-intent.json, finish-tmp/*, received-reviews/*}` | — | intent v1→v2→v3 | owned O_EXCL/temp+replace (non-authority scratch) | retained on failure for inspection |

Ancestor/identity discipline for EVERY live target (controller precedents
`_check_output_ancestors`, `_reject_symlink_ancestors_reval`, `_install_owned_json:490-558`):
lexical `repo_local_path` + `..`/backslash refuse + leaf symlink/FIFO/dir refuse + ancestor
`lstat` walk (no symlinked/non-dir ancestor) + fd `(st_dev,st_ino)` capture + same-fd
readback + pre/post expected-old/new rechecks. Same-byte different-inode swap after create
= foreign evidence: retained, never unlinked. Post-replace readback mismatch →
`POST_REPLACE_MISMATCH`, manual recovery.

## 8. New APIs (exact shapes, no ellipses in implementation)

New module `scripts/survey_editorial_admission_v2.py` (filename fixed at implementation start;
no code in this analysis unit). Error type `EditorialAdmissionError(ValueError)` with
`(code, phase, disposition, detail, owned?, cause?)`; `owned` carries
`{owned_temp?, live_preserved_as, expected_old_sha256, expected_new_sha256, identity?}`
plus per-file primary+secondary close-error chains. No CLI, no State adoption outside
finish record+State, no Gate/Candidate approval, no PDF invention.

- `admit_prepare(root, state_path, proposal_path, retention_manifest_path, staged_manifest_path,
  scope_review_path, new_authored_path) -> PREPARED`
  returns `{result: EDITORIAL_ADMIT_PREPARED, proposal_id, issue_id, research_profile,
  publication_profile, route, state_ref, proposal_ref, retention_manifest_ref,
  staged_manifest_ref{+manifest_digest}, scope_review_ref, new_authored_ref, authored_lineage,
  validation_checkpoint_ref, predecessor_revalidation_ref?, before_live_refs{main,
  bibliography, style}, before_qa_refs{manuscript, quality_bundle, semantic_review,
  visual_review, gate, receipt, pdf{+byte_count,page_count}, reader_input}, before_candidate?
  {path,sha256,verdict}, expected_new_tex×3, expected_reader_delta{changed,new_sha256?},
  head, contract_identity, renderer_commit, intent_ref}` + writes intent v1.
  Refusals: `GIT_ENV_REFUSED, STATE_UNREADABLE, PROFILE_DRIFT, P1_BASIS_MISMATCH,
  RETENTION_INVALID, STAGED_INVALID, P2V_NOT_SCOPE_BOUND, SCOPE_INVALID,
  AUTHORING_LINEAGE_MISSING, READER_DERIVATION_MISMATCH, UPSTREAM_DRIFT,
  CANDIDATE_{FOREIGN,DIVERGED,INVALID,ALIAS,ADOPTED,RETENTION_MISSING},
  PENDING_CONDITIONS_UNMET, TOOL_DRIFT` — all `REFUSED_PRE_WRITE`, nothing live created.
- `admit_install(root, prepared_or_intent_ref) -> INSTALLED`
  re-derives all pins; owned temp+replace main→bib→style; returns
  `{result: EDITORIAL_TEX_INSTALLED_TRANSITION_INVALID_LIVE, installed_tex×3{+identity},
  live_invalid_ack, window_id}` + intent v2. Refusals: `WINDOW_DRIFT/PRESERVED_LIVE,
  LIVE_BEFORE_DRIFT/REFUSED_PRE_WRITE, *_REPLACE_INCOMPLETE/INCOMPLETE|INDETERMINATE`.
- `admit_finish(root, intent_ref, *, reason, executor, recorded_at, page_count?=None)
  -> ADMITTED`
  PDF_BUILD → QA_GENERATE_VERSIONED → QA_VALIDATE_LIVE (§4 entries) → QA_INSTALL_OWNED →
  REVALIDATION_COMMIT (existing controller call with editorial reason+bindings) →
  CANDIDATE_REBIND. Returns `{result: EDITORIAL_ADMITTED_AWAITING_PREVIEW, pdf_ref,
  qa_refs×6{+receipt_sha256}, revalidation_record_ref{+sequence}, state_ref, candidate_ref,
  predecessor_ref?}` + intent v3. Refusals: `PDF_BUILD_FAILED, QA_VALIDATION_FAILED/
  REFUSED_POST_INSTALL, *_INSTALL_INCOMPLETE, REVALIDATION_FAILED/PRESERVED_LIVE,
  REASON_EMPTY/REASON_CLASS_MISMATCH, CANDIDATE_REPLACE_REFUSED, SYNTHETIC_REVIEW_REFUSED,
  POST_REPLACE_MISMATCH`.
- `admit_resume(root, intent_ref) -> phase-appropriate continuation or fail-closed refusal`
  (disk-only; never re-baselines: compares disk to intent, continues or reports).
- `verify_editorial_admission(root, proposal_path, retention_manifest_path, staged_manifest_path,
  revalidation_record_path) -> {result: EDITORIAL_ADMISSION_REPLAY_VERIFIED, chain_length,
  reason_class}` — read-only historical replay (retention + staged + row/chain/agreement in
  `live=False` + bindings exact-match + TeX FILE-byte replay + authored-lineage check). Never
  checks current State/P2V/HEAD.

## 9. Schema: one edit (exact)

`schemas/publication-surface-revalidation.schema.json`:
- `properties.reason_class`: `{"const":"REVIEWED_CORE_CHANGE"}` →
  `{"enum":["REVIEWED_CORE_CHANGE","REVIEWED_EDITORIAL_CORRECTION"]}`.
- Add `properties.editorial_bindings`: `{type:object, additionalProperties:false,
  required:[proposal_ref, retention_manifest_ref, staged_manifest_ref, scope_review_ref,
  new_authored_ref, authored_lineage_digest, before_live_digest, after_live_digest],
  properties:{*_ref: authority{path,sha256} ×5, *_digest: sha256-hex}}`.
- `allOf: [{if:{properties:{reason_class:{const:REVIEWED_EDITORIAL_CORRECTION}}},
  then:{required:[...existing..., editorial_bindings]}}]` — old CORE_CHANGE records
  validate unchanged (field absent → old path). No State schema change. No other schema
  changes (receipt/Gate/manuscript/quality/review/Candidate keep canonical shapes).

## 10. Operation sequence (users + commands, three phases)

| Step | Actor | Operation (module call / external handoff) | Persists | Gate to next |
|---|---|---|---|---|
| 0 | Correction author | supplies authoring change + `change_description` | versioned `authored-input.json`, `proposed-reader.json` | P1 PROPOSED |
| 1 | Operator | P1 propose → P2R capture → scope record → P2V-before → P3S staged (existing modules, unchanged) | proposal/retention/scope/staged | all green |
| 2 | External reviewer (opt pre-TeX) | semantic assessment of proposed reader/staged trio | `received-reviews/` + intent pin | — |
| 3 | Operator | `admit_prepare(...)` | intent v1 (PREPARED) | SCOPE_BOUND + all pins |
| 4 | Operator | `admit_install(...)` | live TeX new + intent v2 (TRANSITION_INVALID_LIVE) | window recheck |
| 5 | Operator | build PDF (inside `admit_finish` phase PDF_BUILD) | live PDF/log new (unvalidated) | build success |
| 6 | External reviewers | postrender semantic + visual assessments OF the built PDF | `received-reviews/` + intent v2 pins | reviewer bytes received |
| 7 | Operator | `admit_finish(...)` remainder (QA gen → §4 pre-validation → owned install → revalidation commit → Candidate rebind) | live QA/receipt/State/Candidate new + intent v3 | all validators PASS |
| 8 | Human | normal `approve_publication_preview` on fresh Candidate → Freeze/Release (existing, unchanged) | approval/freeze/release (existing paths) | Human decision |

`admit_resume` may be invoked by the operator after any interruption/failure instead of
repeating a phase; repeated correction on the same issue follows §11.

## 11. Repeated correction + same-reader R1 interleaving (concrete)

- Second correction allowed iff after first finish: State still VALIDATED_DRAFT +
  `_pending_conditions` green + `resolve_active(live=True)` returns first correction's
  record error-free. Second `prepare` uses updated predecessor (= first record), updated
  before-sets (first correction's after), UNCHANGED validation checkpoint (never rewritten),
  NEW `proposal_id` (retention-root + sequence collision prevent reuse).
- Interleaving with Weekly mechanical refresh or a `REVIEWED_CORE_CHANGE` revalidation
  between corrections: allowed iff each operation's own pending-basis/predecessor checks
  pass in order; overlapping concurrent admits on one issue are refused by sequence
  collision + expected-old drift (no queue, no merge).
- Foreign mutation between corrections (second `before_graph` ≠ first `after`) →
  `BASIS_MISMATCH` refuse + manual triage. One fail-closed refusal with preserved evidence
  stops the attempt; no retry-until-green loop.
- Same-reader R1 (mechanical refresh) interleaving: if Evidence accepted refs change between
  prepare and finish → `UPSTREAM_DRIFT` refuse (no silent rebase); fixture State must be
  post-refresh where the route requires it, else `MECHANICAL_STALE` refuse at prepare.

## 12. Impacted file:function list (no budget; every row has a caller reason)

| Path | Change | Functions / entries | Reason |
|---|---|---|---|
| `scripts/survey_editorial_admission_v2.py` | ADD | `admit_prepare/admit_install/admit_finish/admit_resume/verify_editorial_admission`, `EditorialAdmissionError`, internal `_AfterContext/_EditorialInstallBasis` | Owns ONLY the previously unowned window (intent + TeX/QA/PDF/Candidate temp+replace + versioned QA + bounded contexts). All authority checks delegate to existing/new-scoped validators with explicit contexts. |
| `schemas/publication-surface-revalidation.schema.json` | MODIFY | `reason_class` const→enum + `editorial_bindings` | Minimal hook carrying proposal/retention/staged/scope/authored + before/after digests inside the existing chain (which already enforces rows/chain/agreement/pending/State). |
| `scripts/survey_agent_control_v2.py` | MODIFY (narrow) | `REVALIDATION_REASON_CLASSES` (`:45`); `_check_revalidation_chain` + `_resolve_publication_revalidation` membership (`:994-995,:1115-1116`); new bindings exact-match enforcement; reuse `revalidate_publication_surface`, `resolve_active_*`, `_check_immutable_revalidation_rows`, `_check_revalidation_chain`, `_check_revalidation_agreement`, `built_checked_pending_publication_basis`, `_collect_pending_rows`, `_verify_pending_binding`, `_validate_agent_state/validate_agent_state`, `_exclusive_create_record_bytes`, `_atomic_replace_state_bytes` | Existing chain enforces everything except membership + bindings. No lifecycle/transition/human-gate logic change. |
| `scripts/survey_longform_derivation_v2.py` | ADD entry | `load_derivation_for_admission` (1) | New authored acceptance without touching readback path. |
| `scripts/survey_weekly_derivation_v2.py` | ADD entry | `load_derivation_for_admission` + `validate_receipt_for_admission` (2) | Same, Weekly route. |
| `scripts/survey_longform_generated_v2.py` | ADD entry | `validate_receipt_for_admission` (3) | Versioned-first pre-validation; `validate_receipt:665-758` logic untouched. |
| `scripts/survey_reader_surface_gate_v2.py` | ADD entry | `validate_gate_for_admission` (5) | Explicit-ctx derivation; `validate_reader_surface_gate:1794-…` untouched. |
| `scripts/survey_reader_publication_v2.py`, `survey_quality_v2.py`, `survey_stage_validation_v2.py`, `survey_publication_v2.py`, `survey_production_v2.py`, `survey_human_gate_v2.py`, `candidate_selection_gate.py` | NO CHANGE | called with explicit args only | Canonical paths/strict State/check families already correct for live after-bytes; Selection gate never called (different authority). |
| `scripts/survey_editorial_correction_proposal_v2.py`, `survey_editorial_retention_v2.py`, `survey_editorial_current_authority_v2.py`, `survey_editorial_staged_source_v2.py` | NO CHANGE (one fixture-side expectation) | composed as-is | P1 retention plan SHOULD include a candidate COPY row when a candidate exists, else `prepare` refuses `CANDIDATE_RETENTION_MISSING` (proposal/fixture fix, not a P1 code change). |
| `tests/` | ADD new behavioral files only | `admit_prepare→install→finish→verify` per §15 + negatives §13 + regressions (DM001/019 Freeze pair, W1 equality, DM004 containment, LF-1/LF-2I scoped no-write, P1/P2R/P2V pins) | Proves new authority without rewriting old proofs; no old-suite transfer, no decorative counts. |

## 13. Failure table (exact codes; owned/preserved per row)

| Trigger | Phase | Code / disposition | Owned / preserved |
|---|---|---|---|
| Empty reason / CORE_CHANGE for editorial bytes | finish/commit | `REASON_EMPTY` / `REASON_CLASS_MISMATCH` / REFUSED_POST_INSTALL | record/State/Candidate untouched |
| `change_description` ≠ proposal / id/issue/profile/route mismatch | prepare/finish | `PROPOSAL_MISMATCH` / REFUSED_PRE/POST | live preserved |
| Old authored reused with changed reader / lineage absent | prepare | `AUTHORING_LINEAGE_MISSING` / `READER_DERIVATION_MISMATCH` / REFUSED_PRE_WRITE | live untouched |
| Scope ordinary-no-block / tampered proposed/retention/staged/scope/authored bytes | prepare | `SCOPE/RETENTION/STAGED/AUTHORING_INVALID` / REFUSED_PRE_WRITE | live untouched |
| TOOL_DRIFT (HEAD/contract/closure ≠ pinned renderer/receipt tools) | any pre-write | `TOOL_DRIFT` / REFUSED_* | live preserved |
| Live TeX ≠ expected-old at install entry / pre-replace | install | `LIVE_BEFORE_DRIFT` / REFUSED_PRE_WRITE | live preserved as found |
| Short/zero/fsync/close/replace/readback fault, any live target | install/finish | `*_REPLACE_INCOMPLETE` / INCOMPLETE, or INDETERMINATE (complete-valid bytes retained, close failed) | owned-temp rule; live preserved as found (old or new-complete); never success |
| Same-byte foreign swap (different inode) | any install | identity mismatch → retain, manual recovery | foreign bytes never unlinked |
| Symlink leaf/ancestor, non-reg target, `..`/backslash escape | preflight | `*_ALIAS` / `*_ANCESTOR` / REFUSED_* | nothing written |
| `before_candidate` foreign/diverged/invalid/alias | prepare | `CANDIDATE_FOREIGN/DIVERGED/INVALID/ALIAS` / REFUSED_PRE_WRITE | live untouched; owner triage |
| `before_candidate` adopted (Preview approval / Freeze / Release binds it) | prepare/finish | `CANDIDATE_ADOPTED_REFUSAL` / REFUSED_* | live preserved; decided-history contract required (out of scope) |
| Healthy same-before unadopted candidate (exact 6-field equality, §9) | prepare | `OBSERVED_HEALTHY_SAME_BEFORE` → PROCEED (not reject); becomes `STALE_AFTER`, superseded + retained | provenance preserved; usability gap closed |
| Versioned QA fails any §4 validator vs live after-bytes | finish/validate | `QA_VALIDATION_FAILED` / REFUSED_POST_INSTALL | TeX new held (TRANSITION_INVALID_LIVE); record/State/Candidate unwritten; fix QA or restore TeX |
| Synthetic/type-fixture review offered as authority | finish | `SYNTHETIC_REVIEW_REFUSED` | nothing committed |
| DIRECT_PRIMARY derivation for generated correction | finish | `DIRECT_PRIMARY_REFUSED` | no admission |
| Sequence collision / State ≠ expected-old / HEAD changed | finish/commit | `REVALIDATION_RECORD_COLLISION` / `STATE_DRIFT` / `HEAD_CHANGED` | controller rollback taxonomy; unknown bytes never deleted |
| Post-replace readback mismatch | finish | `POST_REPLACE_MISMATCH` / manual recovery | record+State preserved as found |
| Crash/power-loss mid-window | any | TRANSITION_INVALID_LIVE held; recover from retained COPY + staged + intent | no CAS/crash-atomicity claim |

## 14. Candidate supersession predicates (healthy unadopted ≠ blanket reject)

At `prepare` (before-install), exactly three verdicts for the observed Publication Candidate
(P1 `:822-862` observation reused):
- `OBSERVED_HEALTHY_SAME_BEFORE` → PROCEED: file exists, `validate_candidate` passes,
  exact 6-field active-before equality holds, `candidate_sha256` recomputed, Human Preview
  still pending with NO approval/provenance binding these bytes, no Freeze/Release binding
  them. Recorded in intent. After `finish` it is `STALE_AFTER` (superseded; retained via P2R
  COPY row when in retention plan, else via revalidation `prior_sha256` lineage — missing
  COPY row → `CANDIDATE_RETENTION_MISSING` refuse rather than silent history drop).
- `CANDIDATE_{FOREIGN,DIVERGED,INVALID,ALIAS}` → refuse pre-write; explicit operator triage,
  never auto-overwrite/merge.
- `CANDIDATE_ADOPTED` → refuse pre-write (`CANDIDATE_ADOPTED_REFUSAL`); decided history needs
  a separate (unselected) contract.
- Absent → `NO_CANDIDATE_BEFORE`, proceed; `finish` still builds the fresh Candidate the
  normal Preview path needs.
- Replacement writer (after rebind, never publisher): versioned-temp `build_candidate`
  (after-refs + exact page count + `candidate_sha256`) → `validate_candidate` → owned
  temp+replace (expected-old = before SHA; absent → O_EXCL create). Candidate never publishes
  TeX/PDF/QA; Freeze consumes Candidate+approval+visual+bundle+profile with snapshot rechecks.

## 15. Real-build / negative oracle recipe (implementation entry, not executed here)

- **Fixture recipe (meaningful independent SOURCE commits BEFORE authority; recipe-only
  commit never a renderer basis):** per route, independent DB (inert origin, no alternates,
  process-scoped identity): `F0` = minimal fixed-baseline tree (config with route profiles,
  State DRAFT_COMPLETE→VALIDATED_DRAFT, validation checkpoint passed, architecture approved,
  preview/freeze/release pending, canonical inputs + QA PASS binding F0 bytes, predecessor
  record iff testing second correction); `F1` = authoring change ONLY (new authored input +
  proposed reader + truthful `change_description`; NO authority files). Authority order:
  P1 → P2R → scope → P2V-before → P3S → prepare → install → finish(PDF → external reviews →
  QA → commit → Candidate) → `verify_editorial_admission` → normal Preview/Freeze/Release.
  `currentEpoch` = fixture temporal/as_of window covers the issue window (not stale clock);
  post-refresh State where the route requires it.
- **Positive oracles:** prepare freezes intent (SCOPE_BOUND + verdict recorded); install
  3-file temp+replace + TRANSITION ack; finish PDF+6 QA+receipt live-validated (§4 entries)
  + revalidation `rN(REVIEWED_EDITORIAL_CORRECTION + editorial_bindings)` + strict
  `validate_agent_state` PASS + `resolve_active(live=True)` PASS + fresh `validate_candidate`
  PASS + historical replay PASS. No low-level exit-0/file-exists/single-Gate-PASS counts.
- **Negative oracles:** every row of §13 with exact code + owned/preserved evidence (file-map
  before/after + HEAD/status equality on refusals, per NEG-S1/NEG-G precedent: seam
  identified, only-intended delta, no report on refusal, repaired healthy control).
  Transfer controls reuse the evidence-only `transfer_exclusive` helper scope
  (VALIDATED_DRAFT-stop; NOT a RELEASED rerun claim — mandatory bound, inherited).
- **Regressions (mandatory):** DM001/019 Freeze pair (exact Candidate path/hash, exclusive
  writer, snapshot), W1 approved-only equality (healthy pending valid, stage backstop),
  DM004 `validate-state` containment (workflow call unchanged), LF-1/LF-2I scoped no-write +
  pure/schema/helper separation, P1/P2R/P2V pins (no transfer). New admission must not break
  existing healthy revalidation rows.

## 16. Cost: operators, review, setup, maintenance (evidence-backed; unknowns unknown)

- **Operator cost (new, per correction):** three phase invocations + window monitoring +
  fail-closed triage with exact `owned/live_preserved_as/expected_old/new` diagnostics.
  Removed operator work: manual TeX copy + manual QA re-invocation + manual Candidate JSON
  edit + unconnected helper round-trips (qualitative; MEASURED savings require timed R3
  comparison — explicitly NOT claimed here; assessment §4: total work unmeasured).
- **Review cost (dominant, external):** genuine pre-TeX assessment (optional) + postrender
  semantic + visual assessments per correction, plus normal Human Preview (existing gate,
  unchanged). Synthetic fixtures never substitute. Latency unknown — the invalid-live window
  lasts as long as reviewers take; the design bounds it by intent-on-disk + fail-closed
  serving posture, not by a time promise.
- **Setup cost (evidence-backed):** ~1 GB one-time TeXLive provision per build env
  (assessment §4); toolchain unbundled from source packets (missing26309/unbundled retained).
  Per-route selected-build seconds (~21.0/~23.9 s for the two final builds) are build-only
  observations, NOT operation totals — cited here only to prevent re-inflation.
- **Maintenance (ongoing):** `editorial_bindings` enforcement + mixed-reason chain
  compatibility + retained COPY storage per correction (bounded proposal dir) + `_for_admission`
  entry upkeep alongside public validators.
- **Unknowns (explicit):** external review latency; live PDF determinism in the R2 env;
  representative-length layout quality (postfix resolution leaves it OPEN); DM022
  applicability (Explore); versioned-set comparative cost (other Worker); net lifecycle
  savings (unmeasured until Human adoption + old-path retirement). Necessary independent
  review is not counted as duplication (objective work order, AGENTS.md).

## 17. NO-GO triggers (decisive source-grounded rejection conditions)

This candidate MUST return NO-GO (with exact interface difference + lost usability + scoped
alternative, never a punt to another helper analysis) if implementation discovery shows:
- (a) live LuaLaTeX PDF build cannot satisfy `validate_survey_build_directory` +
  `validate_generated_closure` deterministically in the fixed env → no manuscript/bundle/
  review/Candidate authority exists; alternative (versioned-PDF transfer) would require
  `pdfAuthority`/`bind_pdf_authority`/Candidate-pdf/Freeze-snapshot path changes (exact
  functions listed in §12) — whole completion stays OPEN.
- (b) the new-authored derivation entry cannot satisfy Longform `:720-742` + Gate
  `:1190-1197` without forking canonical consumers beyond the §4 entries (i.e. canonical
  sibling rules must accept versioned paths standing) → canonical replacement infeasible;
  versioned-set alternative becomes the remaining option for root.
- (c) only-decided-history corrections remain (all targets `CANDIDATE_ADOPTED`) → R1 scope
  stays pending-preview corrections; decided history needs its own contract.
- Any NO-GO preserves all evidence and names file:line + expected-vs-actual.

## 18. Concrete source hotspots for root (+ fresh author-independent design review)

Candidate tree (`/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60`):
- `scripts/survey_agent_control_v2.py:45` (reason set), `:685-743` (roles/pending rows),
  `:746-808` (pending binding/basis), `:847-949` (immutable rows + union + validation binding),
  `:952-1017` (chain), `:1020-1081` (agreement), `:1084-1187` (resolve live/historical),
  `:1500-1556` (preserved provenance), `:1604-1642` (O_EXCL record), `:1666-1770` (State
  temp+replace), `:1773-2201` incl. `:1898-1944` (QA block) + commit/rollback taxonomy.
- `scripts/survey_production_v2.py:32-44` (lifecycle hardness); `core.repo_local_path/
  sha256_*/contract_identity/repository_commit_sha` (authority primitives).
- `schemas/survey-production-state.schema.json` (existing provenance pointer, no editorial
  field); `schemas/publication-surface-revalidation.schema.json:10,26` (reason const edit point).
- `scripts/survey_longform_generated_v2.py:606-758` (build/inspect/validate receipt;
  `:707-730` canonical, `:698-706` readback, `:741-742` FILE replay, `:744-757` TeX replay).
- `scripts/survey_weekly_derivation_v2.py` (`load_derivation/build_receipt/validate_receipt`,
  pending_basis branch — root to pin exact lines at review).
- `scripts/survey_reader_surface_gate_v2.py:1145-1225` (`_derivation_for_manuscript`),
  `:1598-…` (inspect≠admission), `:1794-…` (validate, mandatory expected_manuscript+state).
- `scripts/survey_reader_publication_v2.py` (`build/validate_manuscript_manifest`,
  `build/validate_review_record` refuse-overwrite), `scripts/survey_quality_v2.py`
  (`build/validate_bundle` refuse-overwrite, DETERMINISTIC, `bind_pdf_authority`).
- `scripts/survey_publication_v2.py:668-869` (candidate build/validate/preview approval),
  `:171-245,:323-430,:490-558,:561-657` (Freeze preflight/owned install/return).
- `scripts/survey_editorial_correction_proposal_v2.py:822-862` (observed Candidate),
  `~1690-1733` (supplied-vs-rederived), `:1775-…` (`_validate_scope`).
- `scripts/survey_editorial_current_authority_v2.py:101-…` (before-only observer).
- `scripts/survey_editorial_staged_source_v2.py:126,209,544,944,1801` (deps/digest/drift/status).
- `config/survey-production-v2.json:339-344` (DRAFT_COMPLETE artifacts), `:389-390`
  (state_authority).
- `schemas/publication-candidate-v2.schema.json` + live QA schemas (reused unchanged).

Design review should verify especially: editorial `reason` truthfulness binding,
`editorial_bindings` required-field completeness (incl. `new_authored_ref`),
`_for_admission` entries' refusal parity with public validators, before/after context
comparison exactness, long-window resume safety, `before_candidate` COPY-row requirement,
Weekly/Longform route-delta leakage, Freeze-pair coexistence, second-correction predecessor
handling, and cost/authority scope. Any design PASS is not implementation, application,
audit, or adoption approval. Stop at Human Commit Point; ordinary Commit/Push Human-owned.

## 19. Limits (no PASS claim)

Author-side analysis only. No code/tests run, no PDF built, no genuine review or Human
decision produced or simulated, no Freeze/Release/migration/adoption, no full-suite
inference, no savings measurement, no CAS/crash-atomicity/continuous no-drift claim,
no all-profile claim. Missing26309/unbundled-runtime inherited. `STAGED_ONLY`/
`ADMITTED_AWAITING_PREVIEW` (if ever reached) are byte-consistency + replay only.
Production semantic quality of placeholder editions remains NO-GO (assessment §2).
Whole NOT_READY / step4・B3 OPEN / audit unstarted / DM021+DM022 OPEN.

*End of Worker A canonical analysis.*
