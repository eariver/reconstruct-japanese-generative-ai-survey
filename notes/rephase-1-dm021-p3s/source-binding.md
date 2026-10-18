# DM021-P3S PhaseA — read-only source binding (NEW, no code/copy/tests)

2026-10-17 JST. Co-Worker General PhaseA proposal companion to
`interface-proposal.md`. Read-only only: `git rev-parse` / `git status` /
`sha256sum`+`stat` recomputation, `grep`/`read` of candidate source. No
`import`, no cache execution, no test/runtime, no copy/restoration, no
network. Sanitized env `GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0
GIT_ALLOW_PROTOCOL=file` for all Git-aware reads.

## 1. Identity — MEASURED (direct commands this unit)

| Item | Measured value |
|---|---|
| Reconstruct HEAD (boundary context, Human-authorized continuation) | `6dcbb89bb08fcb711a790030821a3c8e83e4a722`, tree `a375c66a03d290611a11c9374c39729ede78658f`, status clean except `?? notes/rephase-1-dm021-p3s/task.md` |
| Fixed contract (reviewed decision, rehashed by root before) | `outputs/rephase-1-dm021-staged-source-contract-decision.md` SHA256 `42eb8dbbb1eeda362b264847c80bdbf478b433ab1fe9777e7fe49c8ed9df3472` |
| Candidate source worktree | `/tmp/opencode/jgas-dm021p2v-impl-20261014T224000Z/candidate-partial-b40de60` |
| Candidate HEAD (detached actual) | `409b292756dd1277b9dfae87679934c0d2ce251c` |
| Candidate tree | `8ce3699861505f32d1d60bdc185d4d4f635aedb2` |
| Candidate full status (sanitized `git status --porcelain=v1 --untracked-files=all \| sort`) | 102 rows: **3 modified tracked + 15 new source + 84 `__pycache__/*.pyc`** |
| Modified tracked (3M) | `schemas/reader-surface-gate-v2.schema.json`, `schemas/reader-surface-semantic-review-v2.schema.json`, `scripts/survey_reader_surface_gate_v2.py` |
| New source (15) | 4 schemas (`editorial-correction-proposal`, `editorial-retention-manifest`, `longform-publication-source-manifest`, `longform-reader-input`) + 6 scripts (`survey_editorial_correction_proposal_v2`, `survey_editorial_current_authority_v2`, `survey_editorial_retention_v2`, `survey_longform_derivation_v2`, `survey_longform_generated_v2`, `survey_longform_semantic_publication_v2`) + 5 tests (`test_survey_editorial_correction_proposal_v2`, `test_survey_editorial_current_authority_v2`, `test_survey_editorial_retention_v2`, `test_survey_longform_derivation_v2`, `test_survey_longform_publication_integration_v2`) |
| Contract asks for P2V final apply copy | relocated per task; not separately re-verified here (see §4) |

Full sorted status output was read directly (102 lines, head `M schemas/...`
through `?? tests/...`); only the census above is persisted, not the raw log.

## 2. Static 18 — MEASURED byte proof (sha256sum + stat, no imports)

All 18 recomputed `sha256 + bytes + mode` **MATCH**
`notes/rephase-1-dm021-p2v/source-correction/expected18-source-correction-v5.json`
(18/18). Modes all `664` (= `0o664`). Full table (path | bytes mode | sha256):

- `schemas/editorial-correction-proposal-v2.schema.json` | 3945 664 | `5623c0d9…333a4607`
- `schemas/editorial-retention-manifest-v2.schema.json` | 5618 664 | `347e5499…549855c`
- `schemas/longform-publication-source-manifest-v2.schema.json` | 2720 664 | `4dadf873…601cf26043e8ca`
- `schemas/longform-reader-input-v2.schema.json` | 10624 664 | `7bae9d2a…b88fbd0643`
- `schemas/reader-surface-gate-v2.schema.json` | 6894 664 | `fe4a96f4…8133a22c`
- `schemas/reader-surface-semantic-review-v2.schema.json` | 4219 664 | `e8598239…38e73d6699b`
- `scripts/survey_editorial_correction_proposal_v2.py` | 113535 664 | `cdd69fe7…1c27eab` (P1)
- `scripts/survey_editorial_current_authority_v2.py` | 37896 664 | `79a3396c…b580d3f4` (observer)
- `scripts/survey_editorial_retention_v2.py` | 122231 664 | `3833b14a…480b73f5b2`
- `scripts/survey_longform_derivation_v2.py` | 62260 664 | `c09c5558…8ac84ea41149`
- `scripts/survey_longform_generated_v2.py` | 39992 664 | `d480e11d…beb97dfde376a163a58b0ebed97d3c2`
- `scripts/survey_longform_semantic_publication_v2.py` | 36224 664 | `4d235a38…11f68cec6a229195`
- `scripts/survey_reader_surface_gate_v2.py` | 94511 664 | `e7305884…bf0131d1f06bbe` (3M member, matches v5 final pin)
- `tests/test_survey_editorial_correction_proposal_v2.py` | 112708 664 | `f581fad0…7c1242dbac`
- `tests/test_survey_editorial_current_authority_v2.py` | 74061 664 | `c567715d…62009aa62009` (test)
- `tests/test_survey_editorial_retention_v2.py` | 93733 664 | `4155baab…f083d614e`
- `tests/test_survey_longform_derivation_v2.py` | 91161 664 | `ce687447…6699fcc12fbf913`
- `tests/test_survey_longform_publication_integration_v2.py` | 107757 664 | `4a03b564…39f637d2bca11a4`

Complete-18 patch `dc5ae07b4ac19da…` (948373 B, applies DIRECTLY to clean 409)
is inherited P2V evidence, not rehashed here.

## 3. Cache 84 — path CENSUS only (bytes NOT proven, nothing executed)

`find scripts/__pycache__ tests/__pycache__ -name '*.pyc' | sort | wc -l` =
**84** (68 under `scripts/__pycache__/`, 16 under `tests/__pycache__/`; every
entry `*.cpython-314.pyc` or `*.cpython-314.opt-1.pyc`). Content bytes were
**not** re-verified; P2V TB1 proof remains the cache-byte authority. No `.pyc`
was imported, executed, or cleaned (prefix-effect and cleanup rules stay in
force for implementation). Census vs byte-proof separation is deliberate:
§2 is MEASURED proof; this section is census only.

## 4. SUMMARIZED / INHERITED (not re-proven here)

- P2V scoped 13+1 behavioral/basis results, B1 State-COPY oracle, whitespace
  live-State drift finding, close/failure qualifications: per P2V
  assessment/closeout + `source-correction/independent-final-resolution.md`.
- P2R 25-method bounded completion, root R1/R2 + independent §10: per P2R
  packet. P1 36-method completion + R1–R4: per P1 packet.
- Contract/S1–S5/§7 design judgments: per `outputs/…contract-decision.md`,
  `notes/rephase-1-dm021-materialization/astra-review-resolution.md`,
  `independent-design-review.md` §§0–7 (read fully for this proposal).
- Relocated final-apply copy (`TB1proof-clean409-copy`, applied-18): named in
  task; availability/identity check is implementation-time work, not claimed
  here. If absent at implementation, the fail-closed four-parent-input
  actual409 restoration + full18patch path from the P2V packet applies; no
  layered old patches, fake root, or network refresh.
- Style bytes below (§5) WERE measured this unit (sha/stat, no import); they
  are MEASURED, not inherited.

## 5. Exact helper/signature index — MEASURED reads at pinned bytes

`file:line` below are read observations at HEAD `409b292`, not standing refs.

**P1** `scripts/survey_editorial_correction_proposal_v2.py`:
`_Collector.__init__(root)` `:95` (pins HEAD via
`core.repository_commit_sha`, routes config through `safe`);
`.safe(value,label)->Path` `:126` (raw-first alias/traversal/nonregular
refusal, pins bytes); `.pinned(ref,label)` `:181`; `.reverify()` `:191`;
`prepare_proposal(root,state_path,authoring_path,proposal_id,change_description=None)` `:1741`;
`_validate_scope(col,root,scope_review_value,proposal,state,profile)->str` `:1775`
(sole `col` surface used: one `col.safe(scope_review_value)` at `:1778`;
State/Profile are passed data, never admission);
`validate_proposal(root,state_path,proposal_path,scope_review_path=None)` `:1838`;
`PROPOSAL_FILES=("authoring-input.json","reader-surface-input-v2.json","proposal.json")` `:47`;
`RESULT_REQUIRED="REVIEW_REQUIRED"` `:50`, `RESULT_BOUND="REVIEW_BOUND_PROPOSAL"` `:51`;
`SCOPE_VERSION="EDITORIAL_CORRECTION_SCOPE_V1"` `:48`,
`SCOPE_CHECK_ID="EDITORIAL_CORRECTION_SCOPE"` `:49`;
`_canonical(route,surface)->bytes` `:448` (Longform→
`longform_derivation.canonical_reader_bytes`, else `core.json_bytes`).

**P2R** `scripts/survey_editorial_retention_v2.py`:
`_Session.__init__(root)` `:187` (dirfd no-follow, root symlink refusal,
entry-vs-fd binding); `.safe_read(value,label,phase,disp)->(rel,bytes)` `:369`;
`.repinned(ref,label,phase,disp,expected_size=None)->rel` `:463`;
`.reverify(phase,disp)` `:477`; `._sanitized_git_env_ctx()` `:632`;
`capture_retention(root,state_path,proposal_path)` `:851`;
`verify_retention(root,proposal_path,manifest_path)` `:1731` (I1 chain
COPY→retained State→State.profile→KEEP at `:1827–1896`;
provisional-dest mapping before retained read `:1844–1859`; KEEP rehash
`:1961–1963`); `RESULT_CAPTURED/RESULT_VERIFIED` `:46–47`;
`RetentionError(code,phase,disposition,detail,owned,cause)` `:68`.

**P2V** `scripts/survey_editorial_current_authority_v2.py`:
`observe_current_authority(root,state_path,proposal_path,manifest_path,scope_review_path=None)` `:101`;
`RESULT_NEEDS_SCOPE="CURRENT_BASIS_OBSERVED_NEEDS_SCOPE"` `:36`,
`RESULT_SCOPE_BOUND="CURRENT_BASIS_OBSERVED_SCOPE_BOUND"` `:37`;
Session-FIRST then live `_Collector`, sanitized Git scope, narrow early pins
`:115–168`; stable-fact return with `state_ref/proposal_ref/retention_manifest_ref/scope_review_ref/observed_head/measured/input_hashes` `:575+`
(full P2R re-verify + pin/final boundaries, merged live+retained hashes —
writer-internal only, never persisted as staged truth).

**Renderers/canonicalizers**:
Longform `render_main(surface)->str` `:293`, `render_bibliography(surface)->str`
`:468`, `validate_generated_closure(main_text,style_text)` `:489`,
`validate_heading_syntax` `:256`, `verify_tool_basis` `:519`,
`verify_closure_at_commit` `:585`, `validate_receipt` `:665` (FILE-byte replay
`:741–757`, style `(root/STYLE_PATH).read_bytes()`), `CURRENT_CLOSURE` 14
entries `:52–66`, `STYLE_PATH=templates/survey/jgaisurvey.sty` `:43`,
`ROUTE="LONGFORM_GENERATED_V1"`; derivation `canonical_reader_bytes` `:949`,
`validate_longform_reader_input` `:927`, `load_derivation` `:1101`,
`load_derivation_for_readback` `:1142`.
Weekly `render_main` `:400`, `render_bibliography` `:445`,
`validate_generated_closure` `:464`, `load_derivation` `:475`,
`validate_receipt` `:726`, `verify_closure_at_commit` `:699`,
`CURRENT_CLOSURE` 8 entries, `STYLE_PATH` identical, `ROUTE="WEEKLY_GENERATED_V2"`.
Shared `render_article_draft_tex.tex_escape` `:32` (only reuse per Longform
docstring); citation `survey_drafting_citation_refs_v2.refs` `:40`,
provenance `resolve_source_access_provenance` `:45`.
Gate `load_and_validate_reader_surface_semantic_review(repo_root,review_path,*,expected_issue_id,expected_publication_profile,expected_surface_path,expected_surface_sha256,require_pass=True)` `:958`
(strict schema/digest/surface/checks `:983–1069`); fidelity via `fidelity._mask_tex_comments` `:507`.

**Style input** (MEASURED stat+sha, no import):
`templates/survey/jgaisurvey.sty` 6547 B mode 664
SHA256 `3b6d15627439b35a352d692c8c5f9c2ac25dd02968e75beb30a69b8f53e5cc`.

**S2 broader file pins** (MEASURED sha/stat this unit for proposal concreteness;
runtime-import edges from `grep ^from/^import`, no imports):
agent_control `278dc404…` 124636 B; agent_tool `0ff3bd9a…` 8207 B; drafting
`ac7d6942…` 20457 B; citation_refs `57b62c5f…` 3805 B; provenance `b51bcab8…`
9212 B; render_tex `9c64ebce…` 11304 B; validate_article_draft `bef91a53…`
17213 B; weekly_pipeline `f6ceaf80…` 21699 B; evidence `f7478d86…` 84889 B;
production `ba91a8ad…` 55342 B; schema_gate `0406f327…` 3261 B;
surface_gate `e7305884…` 94511 B; fidelity `0d29b304…` 20004 B;
weekly_derivation `1cb1f705…` 43603 B; weekly_semantic_publication `53315030…`
8233 B; publication `f3b73d85…` 51835 B; quality `f8a3ef6a…` 13322 B;
reader_publication `d2145042…` 27385 B; reader-surface-input schema `8db11d4e…`
5676 B; weekly receipt schema `c11ad525…` 2714 B; production config
`30042258…` 18253 B (config NOT in S2; listed only to record exclusion —
verifier uses retained KEEP Profile, never live config).

**Actual fixture helpers** (names verified by grep; `_build_validated` does
NOT exist and is never proposed):
P1 test: `_run_git`, `_make_source_root`, `_snapshot`, `_assert_no_write`,
`_new_weekly_helper`, `_build_weekly_validated`, `_new_longform_helper`,
`_commit_derivation_only_change`, `_rebuild_weekly_qa_after_regeneration`,
`_regenerate_weekly_outputs`, `_run_fixture_code`, `_stage_proposal`
(legacy compat), `_stage_authoring_before_prepare` (required new flow),
`_stage_reader_and_proposal`, `_scope_review_for`,
`_assert_transitives_expected_set`; issues `W_ISSUE=incb.ISSUE`,
`L_ISSUE=lf2i_tests.ISSUE`. P2R test: `_make_p2r_source_root`, `_copy_base`,
`_prepare_proposal_for`, `_allowed_delta_only`, `_assert_owned_delta_only`.
P2V test: `_make_p2v_source_root`, `_run_fixture_code`, `_observe_with_timeout`,
`_P2V_OBSERVE_CASCADE`, `_R1_REFRESH_SCRIPT` (genuine owner
`refresh_mechanical_evidence(repo_root,cfg,state_path,reason,executor,recorded_at)`
non-emitted comment refresh), `_R1_SAMEBYTE_SCRIPT`, `_R1_PREPARE_CASCADE`;
`UNTRACKED_P2V_SOURCES` 15 entries, `P2R_EXTRA` 3 entries.
Real recipes: Longform via `lf2i_tests.LongformPublicationIntegrationV2Tests`
two-pass reviewer gating + `lf1_tests.LongformDerivationV2Tests` authored chain;
Weekly via `incb.IncrementBWeeklyDerivationV2Tests` accepted-chain probe +
`_build_weekly_validated` straight-line healthy VALIDATED_DRAFT with real
`build_manuscript_manifest/build_review_record/build_bundle/build_reader_surface_gate`
+ `validate_*` cascade; R1 via committed-fixture `refresh_mechanical_evidence`
(non-emitted TeX-comment-preserving) + `_commit_derivation_only_change`
(single comment literal → `main.tex` only) — never a generic TeX cascade.

Negative finding (grep, no execution): no `materializ|install_correction|
promote_correction|apply_correction|write_live|adopt_correction` writer exists
under `scripts/`; hits are pass1/pass2, unrelated helpers, review prose only.
