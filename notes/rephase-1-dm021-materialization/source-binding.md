# DM021 materialization unit — source binding (NEW, read-only observations)

2026-10-16 JST. Companion to `analysis.md` (General proposal, design-only).
Every entry below was observed by read-only means in this unit: `git
rev-parse` / `git status --porcelain=v1 --untracked-files=all` /
`git diff --stat` with `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0
GIT_ALLOW_PROTOCOL=file` (all rc 0), `sha256`+`stat` recomputation of the 18
pinned paths vs static v5 (18/18 MATCH), and `grep`/`read` of candidate
source. No imports, tests, copies, restores, network, or file changes beyond
these two NEW analysis documents. Line numbers are byte observations at the
verified pins, not standing references.

## 1. Identity binding

| Item | Observed value |
|---|---|
| Active worktree | `/tmp/opencode/jgas-dm021p2v-impl-20261014T224000Z/candidate-partial-b40de60` |
| HEAD (detached actual) | `409b292756dd1277b9dfae87679934c0d2ce251c` |
| Tree | `8ce3699861505f32d1d60bdc185d4d4f635aedb2` |
| Full status | 3 modified tracked + 15 new source + 84 `__pycache__/*.pyc` |
| Modified tracked (3M) | `schemas/reader-surface-gate-v2.schema.json`, `schemas/reader-surface-semantic-review-v2.schema.json`, `scripts/survey_reader_surface_gate_v2.py` |
| Static pins | `notes/rephase-1-dm021-p2v/source-correction/expected18-source-correction-v5.json` — 18/18 sha256+bytes+mode(`0o664`) MATCH |
| Key pins | P1 `cdd69fe7c24de6d…` 113535 B; observer `79a3396cf07d8…` 37896 B; test `c567715dfb4ff…` 74061 B |
| Complete-18 patch (P2V evidence, not rehashed) | `dc5ae07b4acb19da…` 948373 B, applies DIRECTLY to clean 409 |
| Cache census | 84 paths, all `.pyc` under `scripts/__pycache__/` + `tests/__pycache__/`; content bytes NOT re-verified here (P2V TB1 proof remains cache-byte authority); none executed/imported |
| Preceding reconstruct commit (boundary context) | `5595d214375f77c93fc3376799fb29b145bc5e32` — Human-authorized P2V closeout push; NOT candidate/production/adoption authority |

## 2. Exact callsite index (all verified by read in this unit)

Producers / serializers:
- `scripts/survey_longform_derivation_v2.py:1101` `load_derivation`
  (DRAFT_COMPLETE-only `:1122`, action `:1127`); `:1142`
  `load_derivation_for_readback` (allowlist `:1166`, no pending bypass);
  `:627` surface schema keys; `:685–719` `longform_revision` envelope.
- `scripts/survey_weekly_derivation_v2.py:475` `load_derivation`;
  `:481–487` checked pending fallback (NOT editorial authority);
  `:22` reader input schema; `:400`/`:445` renderers.
- `scripts/survey_longform_generated_v2.py:293` `render_main`; `:468`
  `render_bibliography`.
- Staged-ordering precedent:
  `scripts/survey_longform_semantic_publication_v2.py:60`
  (`--materialize-surface-only`); `:370–460` pass1/pass2; `:372–390`
  pass2 refuses silent pass1; `:410–414` partial-output preflight;
  `:423` exclusive surface write; `:430` install readback;
  `:436–455` same-byte reuse rules; `:474–487` review-on-disk gate;
  `:481`/`:486` materialization-prohibited-until-PASS.

Receipt / tools:
- Longform `verify_tool_basis` `:519–582` (uncommitted overlay refuses —
  docstring `:519–528`); `verify_closure_at_commit` `:585`;
  `validate_receipt` `:660–758` (review binding `:694–697`, canonical
  siblings `:720–730`, FILE-byte replay `:741–742`, output replay
  `:753–757`).
- Weekly `_verify_head_bytes` `:577–631`; `build_receipt` `:634–666`;
  `_inspect_receipt_envelope` `:669–696`; `verify_closure_at_commit`
  `:699–724`; `validate_receipt` `:726–773`.

Gate / manuscript / reviews / bundle:
- `scripts/survey_reader_surface_gate_v2.py:1145`
  `_derivation_for_manuscript` (3 routes; canonical suffix `:1162–1169`,
  `:1201–1203`; receipt-next-to-surface `:1173`/`:1206`; triple equality
  `:1178–1181`/`:1211–1214`; output↔manuscript equality `:1183–1198`,
  `:1215–1231`); `:1234` `evaluate_reader_surface_gate`; `:1842`
  `validate_manuscript_surface`.
- `scripts/survey_reader_publication_v2.py:297`
  `build_manuscript_manifest` (no overwrite `:352–354`); `:358`
  `validate_manuscript_manifest`; `:544` `validate_review_record`
  (digest `:579`).
- `scripts/survey_quality_v2.py:232` `validate_bundle`; `:60`
  `bind_pdf_authority`.

Candidate / stage chain (unchanged by this proposal):
- `scripts/survey_publication_v2.py:668` `build_candidate` (immutable
  `:745`); `:749` `validate_candidate`; `:817`
  `build_preview_approval`; `:855` `validate_preview_approval`.
- `scripts/survey_handlers_v2.py:150` `stage_handoff_handler`; `:378`
  `validate_publication_candidate`; `:394` `validate_freeze` (exact match
  `:409–430`); `:434` `validate_release`.
- `scripts/survey_stage_validation_v2.py:66–74` DRAFT_COMPLETE 7 roles;
  `:75` VALIDATED_DRAFT→`publication-candidate`; `:126–156`
  approval-artifact binding.

Controller / State / revalidation:
- `scripts/survey_agent_control_v2.py:45`
  `REVALIDATION_REASON_CLASSES={"REVIEWED_CORE_CHANGE"}`; `:348`
  `validate_agent_state`; `:685` `_publication_revalidation_roles`;
  `:696` `_pending_conditions`; `:711` `_collect_pending_rows`
  (canonical-role-only `:737–740`); `:746` `_verify_pending_binding`;
  `:784` `built_checked_pending_publication_basis`; `:1773`
  `revalidate_publication_surface` (reason gate `:1789`, row rebind
  `:1844–1886`, QA `:1900–1944`, Gate `:1931`, sequence `:1954–1957`,
  pre-mutation recheck + exclusive writes `:1996–2032`).
- `scripts/survey_weekly_mechanical_refresh_v2.py:36` R1
  `REASON_CLASS`; `:690–718` canonical asserts; `:920` roles.

P1 / P2R / P2V (fixed composition surface):
- `scripts/survey_editorial_correction_proposal_v2.py:47`
  `PROPOSAL_FILES`; `:327` `_eligibility`; `:380` `_active_effective`;
  `:828–862` Candidate observed/unadopted; `:1302` `_retention_plan`;
  `:1309` `_pipeline_data`; `:1514` `_pipeline`; `:1576`
  `_validated_state_profile_for_tree`; `:1741` `prepare_proposal`;
  `:1775` `_validate_scope` (after-binding `:1786–1793`, authority
  `:1811–1835`); `:1838` `validate_proposal` (compare `:1865–1867`,
  post-scope receipt recheck `:1880`, stability `:1882–1887`).
- `scripts/survey_editorial_retention_v2.py:44–48` schema/filename;
  `:851` `capture_retention` (HEAD pin `:880`); `:1731`
  `verify_retention`.
- `scripts/survey_editorial_current_authority_v2.py:101`
  `observe_current_authority` (observation only).

Negative finding (verified by grep): no correction materializer, writer,
installer, promoter, or adoption routine exists anywhere under `scripts/`
(`materializ|install_correction|promote_correction|apply_correction|write_live|adopt_correction`
hits are Longform pass1/pass2, unrelated helpers, and review prose only).

## 3. Fixed prior contracts (unchanged authority)

- P1: `outputs/rephase-1-dm021-contract-decision.md` (SHA07e89990…);
  P1 assessment + `notes/rephase-1-dm021-p1/`.
- P2R: `outputs/rephase-1-dm021-retention-contract-decision.md`
  (SHA194fd7de…); P2R assessment + `notes/rephase-1-dm021-p2r/`.
- P2V: `outputs/rephase-1-dm021-current-authority-contract-decision.md`
  (SHA2ea1d98f…); assessment §4 + `notes/rephase-1-dm021-p2v/`
  `astra-closeout-resolution.md` +
  `source-correction/independent-final-resolution.md` (scoped 13+1,
  B1 State-COPY oracle, close/failure qualifications — all in force).
- Production baseline `774dd39a` fixed; intake `afdb3df3` secondary
  evidence only (not re-fetched).

## 4. Proposed new/changed surface (General proposal — Astra selects)

P3 (next implementation, §6 of analysis): **2A / 0M / 0 schema** —
A `scripts/survey_editorial_correction_builder_v2.py`
(`build_staged_reader`, in-memory result, structured errors,
exclusive single-staged-file ownership) +
A `tests/test_survey_editorial_correction_builder_v2.py`
(10–14 methods, synthetic accepted-chain Longform/Weekly/R1 oracles).
P4 touch list (designed, not implemented): receipt validators ×2, Gate
4th route, manuscript binding rule, bundle staged-output rule,
revalidation reason class + corrected role(s), writer, State adoption —
exact diffs belong to the P4 implementation unit after Astra selects
Alternatives V (§2.3) and E (§5.2).

## 5. Raw-vs-summary labeling

- §§1–2 path/hash/mode/count values are MEASURED values from the
  commands listed in the header (not persisted raw logs — no new raw
  evidence was produced or needed in a design unit).
- §2 line numbers are direct read observations at the pinned bytes.
- `analysis.md` §§2–7 are PROPOSAL (General judgment on fixed sources),
  explicitly labeled as such; they assert no runtime behavior and adopt
  no authority.
