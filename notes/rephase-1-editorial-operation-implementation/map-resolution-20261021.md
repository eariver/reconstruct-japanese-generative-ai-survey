# R3 map resolution — disjoint ownership + exact registry (adds to, preserves original map)

Root review: architecture matches contract; pre-code return not yet exact. This file
FIXES §10 `e.g.29+10`/`actualcountsincode` contradiction, ownership overlap, and 4-sample
isolation insufficiency. It PRESERVES `implementation-map-20261020.md` (no edits) and adds
exact frozen ownership, L APIs, registry, legacy-shape, spec/toolchain, and full all-entry
isolation. No source code edits, no copy recreation/checkout/reset, no network/imports/tests.
Short prerequisite return within ongoing task, not next unit/Commit Point.

Governing unchanged: `d880f53e...e3e4d`, SRC `/tmp/opencode/jgas-style-correction-20261019T135318Z/candidate-partial-b40de60`
(`409b292`/tree `8ce36998`, 4M18A22), DST `/tmp/opencode/jgas-editorial-op-impl-20261020T131527Z/candidate-partial-b40de60`,
workspace `df63555`, packet `notes/rephase-1-editorial-operation-implementation/`.

## 1. Frozen disjoint ownership (NEVER cross-edit)

- **L owns (only L edits):** `scripts/survey_publication_set_v2.py` (NEW),
  `schemas/publication-surface-revalidation.schema.json` (branch2 edit, branch1 verbatim),
  `schemas/editorial-publication-set-v2.schema.json` (NEW),
  `scripts/survey_agent_control_v2.py` (branch dispatch + resolver wiring only).
  L owns NOTHING else. L does not edit H/C files. L reviews H/C call-site use of L helpers.
- **H (lead) owns (only H edits):** NEW `scripts/survey_editorial_publication_v2.py`,
  4 NEW schemas `schemas/editorial-publication-source-manifest-v2.schema.json`,
  `schemas/editorial-publication-build-record-v2.schema.json`,
  `schemas/editorial-manuscript-spec-v2.schema.json`,
  `schemas/editorial-toolchain-spec-v2.schema.json`,
  existing `schemas/reader-manuscript-v2.schema.json` (editorial_source branch only) +
  `schemas/reader-surface-gate-v2.schema.json` + `schemas/reader-surface-semantic-review-v2.schema.json`
  (editorial Gate branch only, no old-branch relaxation),
  `scripts/survey_reader_publication_v2.py` (`_validate_manifest_semantics:171` + `build_manuscript_manifest` only),
  `scripts/survey_reader_surface_gate_v2.py` (`_derivation_for_manuscript:1145` + Gate builder/validator/CLI only),
  `scripts/survey_weekly_derivation_v2.py` + `scripts/survey_longform_derivation_v2.py` +
  `scripts/survey_longform_generated_v2.py` + `scripts/survey_weekly_semantic_publication_v2.py` +
  `scripts/survey_longform_semantic_publication_v2.py` (only needed editorial receipt-dispatch changes;
  no unrelated renderer edits), direct publisher initial guards if needed (DRAFT_COMPLETE-only preserved).
  H owns Weekly/Longform `CURRENT_CLOSURE` definitions (verify/extend exactly per §4).
  H NEVER edits L/C files.
- **C owns (only C edits):** `scripts/survey_stage_validation_v2.py`, `scripts/survey_production_v2.py`,
  `scripts/survey_profiled_freeze_v2.py`, `config/survey-production-v2.json`,
  `scripts/survey_orchestrator_v2.py`, `scripts/survey_handoff_v2.py`, `scripts/survey_human_gate_v2.py`,
  `.github/workflows/survey-production-v2-export-publication-preview.yml` (+ release workflow/docs),
  canonical build workflows + interactive revision wrapper + semantic-quality canonical writer,
  `scripts/survey_editorial_correction_proposal_v2.py` (P1 active-set/repeat),
  `scripts/survey_editorial_current_authority_v2.py` (P2V active-set caller),
  `scripts/survey_editorial_retention_v2.py` + `scripts/survey_editorial_staged_source_v2.py`
  (keep historical semantics, closure bumps only), `scripts/survey_weekly_mechanical_refresh_v2.py` (R1 refusal),
  docs. C owns P3S fixed closure (`_SHARED_PY/_SHARED_SCHEMAS/_route_code_deps`) and config registry
  (`contract_files` + `implementation_control_roots` + CLI registration/docs).
  C NEVER edits L/H files. Shared interfaces frozen in §2–§6; lead integrates; unexpected defect returns
  for scope choice; partial helper-only is not acceptance.

Supersedes original map §1 ownership groups and §15 split where they overlapped L/H set-schema and
H/C receipt-closure ownership and implied `e.g.` counts. All other original map sections preserved
unless explicitly corrected below.

## 2. L helper APIs frozen (H/C call, never reimplement, no caller verified-dict)

All paths repo-contained `Path`; no caller-supplied `{path,sha256}` dict is trusted — L re-hashes
from disk under containment (`core.repo_local_path`, raw-first no-follow, alias refusal) and refuses
on drift. `defaultpath never permission`: returning a default canonical path when no active set does
NOT grant authority; callers must still validate the returned bytes via strict State + receipt/Gate.

```python
# L (survey_publication_set_v2.py)
def resolve_publication_selection(root: Path, cfg: dict, state: dict) -> dict:
    """Return identity_selection (no permission token, no verified-dict input)."""
    # mode: "CANONICAL" | "VERSIONED_ACTIVE"
    # {
    #   "mode": ...,
    #   "active_set_ref": {"path","sha256"} | None,   # seal ref when VERSIONED_ACTIVE
    #   "activation_record_ref": {"path","sha256"} | None,
    #   "canonical_anchor": {"kind": "VALIDATION_CHECKPOINT"|"LEGACY_REVALIDATION", "ref": {"path","sha256"}},
    #   "effective7": {role: {"path","sha256","origin": "ORIGINAL"|"ACTIVE"}}  # exactly 7 publication roles
    #              # from original validation checkpoint, with active projection applied when VERSIONED_ACTIVE
    #   "candidate_ref": {"path","sha256"} | None,    # versioned Candidate when VERSIONED_ACTIVE else None
    #   "candidate_path": str,                        # exact State-bound Candidate path to read:
    #              # versioned Candidate path when VERSIONED_ACTIVE, else default canonical
    #              # "sources/{id}/publication/v2/publication-candidate-v2.json" (defaultpath, never permission)
    #   "record_ref": {"path","sha256"} | None,       # active revalidation/activation record ref or None
    #   "set_ref": {"path","sha256"} | None,          # seal ref or None
    # }
def resolve_publication_artifact_path(root: Path, cfg: dict, state: dict, role: str) -> Path:
    """Single role-aware path resolver with State argument. role in 7 publication roles + 'publication-candidate'."""
    # Recomputes from resolve_publication_selection; compares resolved bytes to selection pins;
    # refuses on unknown role, ambiguous/mismatched input, symlink/alias escape. Loaders recompute+compare,
    # not only producers. Fixed DRAFT templates unchanged.

# L record/identity helpers H/C must call (exact names frozen):
def validate_seal(root: Path, set_path: Path) -> dict: ...
def validate_activation_record(root: Path, record_path: Path) -> dict: ...
def derive_canonical_anchor(root: Path, cfg: dict, state: dict, chain: list[dict]) -> dict: ...
def before_active_digest(effective7: dict, candidate_ref: dict | None) -> str: ...
  # canonical SHA256 of sorted effective seven publication checkpoint rows + exact observed Candidate ref/null
def active_candidate_ref(root: Path, cfg: dict, state: dict) -> dict | None: ...
def require_active_or_canonical(root: Path, cfg: dict, state: dict, want_versioned: bool) -> dict: ...
  # fail-closed branch guard for revised-mode refusal (R1/wrapper/build call before destructive action)
```

H calls: `validate_seal`, `derive_canonical_anchor`, `before_active_digest`, `resolve_publication_selection`
(prepare/finalize/activate/resume/verify). C calls: `resolve_publication_selection`,
`resolve_publication_artifact_path`, `active_candidate_ref`, `require_active_or_canonical`
(stage/Preview/Freeze/config/orchestrator/handoff/human-gate/export/R1/wrapper).
External callers (CLI/workflows) NEVER supply `active_set`/verified-dict/pending boolean; L re-derives
everything from `(root,cfg,state)` + on-disk bytes.

## 3. CRITICAL registry — contract hash vs implementation closure (do NOT blindly add)

Existing distinction preserved (mechanical proof: R1 comment-only `survey_weekly_derivation_v2.py`
change leaves contract hash unchanged because scripts are NOT in `contract_files`):

- `config/survey-production-v2.json contract_files`: semantic authority hash inputs only.
  Current exact: `pipeline` 62 files (docs/prompts/requirements + 24 schemas incl. `reader-manuscript`,
  `quality-bundle`, `candidate`, `preview-approval`, `visual`, `freeze`, `release-manifest/record`,
  `stage-checkpoint`, etc.; NOT including `weekly/longform-publication-source-manifest`,
  `reader-surface-input/longform-reader-input`, `reader-surface-gate/semantic-review`,
  `publication-surface-revalidation`, scripts, or `config` itself) + `quality` 3 docs.
  `implementation_control_roots` = `["config","schemas","scripts",".github/workflows"]` (4).
  `control_paths = [DEFAULT_CONFIG] + implementation_control_roots + STYLE + contract_files.values()`
  is used for `git diff --quiet commit HEAD` + dirty/untracked fail-closed checks
  (`weekly_derivation:591-618`, `longform_generated:544-569`); `CURRENT_CLOSURE` bytes are pinned
  INTO the receipt (`expected_names` + per-row `sha256` + `git show commit:path` equality).
- Rule (frozen): ADD new *semantic* schemas (and justified contract docs) to `contract_files.pipeline`;
  ADD new *implementations* to exact source closure + rely on existing `implementation_control_roots`
  (already covers `scripts/`/`schemas/`). NEVER add `scripts/*.py` or `config` itself or every touched
  consumer to `contract_files.pipeline/quality`. If script inclusion made R1×2 fail State/Profile
  contract (`pipeline_contract_sha256` drift on comment-only change), the map is wrong — this map avoids it.
- Selected registry change (exact): `pipeline` 62 → 67 (+5 NEW semantic schemas below; `quality` 3 unchanged;
  `implementation_control_roots` 4 unchanged because `scripts/`+`schemas/` already cover new files):
  `schemas/editorial-publication-source-manifest-v2.schema.json`,
  `schemas/editorial-publication-set-v2.schema.json`,
  `schemas/editorial-publication-build-record-v2.schema.json`,
  `schemas/editorial-manuscript-spec-v2.schema.json`,
  `schemas/editorial-toolchain-spec-v2.schema.json`.
  Amended `reader-manuscript-v2.schema.json` already in pipeline (bytes change, size 62→67 counts only new files).
  Amended `reader-surface-gate/semantic-review` + `publication-surface-revalidation` NOT added to pipeline
  (preserve existing distinction: they live in implementation closure + control_roots, like today;
  revalidation schema currently NOT in pipeline — keep it there, do not newly add).
  No `scripts/*.py`, no `config/survey-production-v2.json` itself added (it is `DEFAULT_CONFIG`, already
  in control_paths separately). Justified contract docs: none added in this increment (no new authority doc).
- Dynamic final-code check must match this map: implementation will run AST/read-only import enumeration
  (no source import) + `git grep` closure vs `contract_files` audit; if actual top-level imports require
  a different set, return to root (do not silently execute with `+unknown`).

## 4. Exact postchange sets per Weekly/Longform/P3S (named paths, cardinalities, no +unknown)

Method: read `_SHARED_PY` (27), `_SHARED_SCHEMAS` (5), `CURRENT_CLOSURE` tuples, and AST top-level
imports (inspect stdout, no source import). Closure = bytes pinned in receipt; control_paths = diff guard.
New files enter closure ONLY where receipt bytes actually depend on them; otherwise control_paths already
covers them via `scripts/`/`schemas/` roots.

- **Weekly `CURRENT_CLOSURE` 8 → 8 UNCHANGED** (H owns, verifies unchanged):
  `scripts/survey_weekly_derivation_v2.py`, `scripts/survey_weekly_semantic_publication_v2.py`,
  `scripts/survey_drafting_citation_refs_v2.py`, `scripts/survey_bibliography_access_provenance_v2.py`,
  `scripts/render_article_draft_tex.py`, `schemas/reader-surface-input-v2.schema.json`,
  `schemas/weekly-publication-source-manifest-v2.schema.json`, `templates/survey/jgaisurvey.sty`.
  Why no addition: Weekly `validate_receipt`/`load_derivation` top-level imports (`agent_control`,
  `agent_tool`, `drafting_v2`, `evidence_v2`, `production`, `schema_gate` — see AST) are already
  covered by control_paths, not closure, by existing design; editorial receipt is a SEPARATE schema/validator
  (`validate_editorial_receipt` in H module) with its OWN closure (below), not an extension of Weekly closure.
  Adding editorial files to Weekly closure would wrongly force all old Weekly receipts to fail
  (`expected_names` mismatch) and break R1×2 initial-mode guard — map refuses that.
- **Longform `CURRENT_CLOSURE` 14 → 14 UNCHANGED** (H owns, verifies unchanged):
  `scripts/survey_longform_generated_v2.py`, `scripts/survey_longform_semantic_publication_v2.py`,
  `scripts/survey_longform_derivation_v2.py`, `scripts/survey_drafting_citation_refs_v2.py`,
  `scripts/survey_bibliography_access_provenance_v2.py`, `scripts/render_article_draft_tex.py`,
  `schemas/longform-reader-input-v2.schema.json`, `schemas/longform-publication-source-manifest-v2.schema.json`,
  `schemas/reader-surface-semantic-review-v2.schema.json`, `schemas/reader-surface-gate-v2.schema.json`,
  `scripts/survey_reader_surface_gate_v2.py`, `scripts/survey_production_v2.py`,
  `scripts/survey_schema_v2.py`, `templates/survey/jgaisurvey.sty`.
  Same justification as Weekly: editorial path reuses Longform loaders but pins its own closure.
- **P3S `_route_code_deps` 37 → 37 UNCHANGED** (C owns, verifies unchanged):
  `_SHARED_PY` 27 (exact list in inspect stdout: `render_article_draft_tex`, `survey_agent_control_v2`,
  `survey_agent_tool_v2`, `survey_architecture_v2`, `survey_architecture_v2_base`,
  `survey_bibliography_access_provenance_v2`, `survey_completeness_v2`, `survey_drafting_citation_refs_v2`,
  `survey_drafting_v2`, `survey_drafting_v2_base`, `survey_editorial_correction_proposal_v2`,
  `survey_editorial_retention_v2`, `survey_evidence_v2`, `survey_longform_derivation_v2`,
  `survey_longform_generated_v2`, `survey_production_v2`, `survey_publication_v2`, `survey_quality_v2`,
  `survey_reader_fidelity_v2`, `survey_reader_publication_v2`, `survey_reader_surface_gate_v2`,
  `survey_review_attention_v2`, `survey_schema_v2`, `survey_screening_v2`, `survey_weekly_derivation_v2`,
  `validate_article_draft`, `weekly_pipeline`) + `_SHARED_SCHEMAS` 5
  (`editorial-correction-proposal`, `editorial-retention-manifest`, `editorial-staged-source-manifest`,
  `reader-surface-gate`, `reader-surface-semantic-review`) + route extra 3
  (Weekly: `reader-surface-input` + `weekly-publication-source-manifest` + `weekly_semantic_publication`;
  Longform: `longform-reader-input` + `longform-publication-source-manifest` + `longform_semantic_publication`)
  + staged module 1 + style 1 = 37 (assert `27+5+3+1+1` stays).
  Why no addition: P3S `verify_staged_source` explicitly never calls P2V/current-State/HEAD and never
  imports set/editorial modules (AST top-level imports of `survey_editorial_staged_source_v2.py`: proposal,
  retention, longform_derivation/generated, production, reader_surface_gate, schema_gate, weekly_derivation —
  all already in 27; no set/editorial import). Changed bytes in already-listed files (e.g. P1 active-set,
  agent_control branch) are covered without size change. Adding new files would trip `CODE_DEPS_SHAPE`
  and falsely claim staged proof depends on activation — map refuses that.
- **NEW editorial operation closure (H defines, C reviews, exact size 12):**
  `scripts/survey_publication_set_v2.py`, `scripts/survey_editorial_publication_v2.py`,
  `schemas/editorial-publication-source-manifest-v2.schema.json`,
  `schemas/editorial-publication-set-v2.schema.json`,
  `schemas/editorial-publication-build-record-v2.schema.json`,
  `schemas/editorial-manuscript-spec-v2.schema.json`,
  `schemas/editorial-toolchain-spec-v2.schema.json`,
  `schemas/reader-manuscript-v2.schema.json` (amended), `schemas/reader-surface-gate-v2.schema.json` (amended),
  `schemas/quality-regression-bundle-v2.schema.json`, `schemas/publication-candidate-v2.schema.json`,
  `templates/survey/jgaisurvey.sty` — pinned by `validate_editorial_receipt`/`validate_prepared_set`
  (new `verify_editorial_closure_at_commit` mirroring Weekly/Longform `verify_closure_at_commit` shape,
  but separate function, no old-closure size change). AST justification: H module top-level imports are
  exactly setmod + retention + staged + reader + quality + publication + gate-builder + weekly/longform
  derivation/generated + core/schema_gate (no Stage/orchestrator/handoff/human-gate/R1 imports at top-level;
  P2V/agent State only function-local), so no transient import missing beyond these 12 + already-covered
  control_paths. Final-code AST check must reproduce this 12-set; any deviation returns to root.

No `ALL scripts`, no `+unknown`, no `e.g.29+10`. All cardinalities are code-asserted (`len==8`, `len==14`,
`len==27+5+3+1+1`, new `len==12`).

## 5. Legacy schema fix (no hardcoded 14)

Current `publication-surface-revalidation.schema.json` (161 lines): `required` has 14 keys
(`schema_version,issue_id,reason_class,reason,lifecycle,prior_checkpoint,superseded_artifacts,preserved_artifacts,validation,core,executor,recorded_at,supersedes,establishment`),
`additionalProperties:false`, `$defs/authority/superseded_artifact/preserved_artifact/validation/core/sha256/gitsha`.
L refactor: wrap in `oneOf: [{$ref: "#/$defs/legacy_revalidation"}, {"$ref": "#/$defs/editorial_activation"}]`
(or equivalent `anyOf` with discriminator on `reason_class`+`kind`), where `legacy_revalidation`
is VERBATIM copy of current object (same required/`additionalProperties`/`$defs` refs, no hardcoded
count in code — code validates via `schema_gate.load_and_validate_json`, never `len(required)==14`).
Branch2 `editorial_activation` exact keys per contract §4.3 (no top-level required leaking across branches;
`supersedes` common chain edge both branches; `canonical_anchor/before_state_ref/before_active_digest/before_candidate_ref/set_ref`
new). Chain helpers dispatch per validated branch; legacy writer cannot emit editorial authority.

## 6. Spec / toolchain / build-record fixes

- Input specs live OUTSIDE yet-unclaimed `P/publication/` root: `P/manuscript-spec.json`
  (validated by `editorial-manuscript-spec-v2.schema.json`) and `P/toolchain-spec.json`
  (validated by `editorial-toolchain-spec-v2.schema.json`). `prepare_publication` claims `P/publication/`
  absent (refuses pre-existing conflicting/same-byte target, preserves incomplete, never deletes
  foreign/unknown); inputs are pinned dependencies, not writer-owned outputs. Original map §2/§5 paths
  inside `P/publication/` corrected here (specs are siblings, not children).
- `manuscript-spec` keys (frozen): `schema_version,kind=EDITORIAL_MANUSCRIPT_SPEC_V1,issue_id,proposal_ref,architecture_coverage[],reader_requirements[],authored_by,recorded_at`.
  Only existing coverage/requirement assertions/author/time, no caller source/profile overrides.
- `toolchain-spec` keys (frozen): `schema_version,kind=EDITORIAL_TOOLCHAIN_SPEC_V1,executor,absolute_executable,recipe,argv[],env{},recorded_at`.
  Executor configuration, NOT approval. `argv` allowlisted fixed-recipe arguments only
  (e.g. `lualatex --interaction=nonstopmode --halt-on-error --synctex=1 --file-line-error %O %S`,
  `biber %O %B`, `latexmk -pdf -lualatex -interaction=nonstopmode`); NO `latexmk -e`/shell string/`-shell-escape`
  passthrough; unknown flag refuses. `env` allowlist (e.g. `TEXMFHOME`, `SOURCE_DATE_EPOCH`) only;
  NO `GIT_*`/root overrides/`TEXINPUTS` escape/`PATH` rewrite; absolute executable must exist under
  probed TL2026 `texlive/bin/x86_64-linux/` and versions recorded.
- `build-record` keys (frozen, file `P/publication/build-record.json`):
  `schema_version,kind=EDITORIAL_PUBLICATION_BUILD_V1,issue_id,proposal_ref,staged_manifest_ref,
  recipe_ref{path,sha256},declared_inputs{primary,bibliography,style},recipe{fixed_steps[]},
  toolchain{executable,versions,argv,env},outputs{publication-pdf,build-log,pdf-digest},exit_code,recorded_at,build_sha256`.
  `recipe_ref` is the versioned recipe source ref/hash (`.latexmkrc` path `".latexmkrc"` SHA pinned from
  implementation commit, 5 lines, `$pdf_mode=4` etc.), NOT only `fixed_steps`. `build_sha256` hashes
  canonical object WITHOUT `outputs` self-refs to avoid output-self-hash cycle (same pattern as
  `receipt_sha256`/`set_sha256` excluding self); outputs are transferred exclusively to `build3` after
  successful exit, then hashed. Failed build yields no admissible set.

## 7. Full isolation appendices (all-entry scope, not 4-sample)

NEW script BEFORE execution: `notes/rephase-1-editorial-operation-implementation/inspect_full_isolation_20261021T000000Z.sh`.
Raw: `inspect-stdout-20261021T000000Z.txt`, `inspect-stderr-20261021T000000Z.txt` (empty),
`inspect-exit-20261021T000000Z.txt` (`0`). No copy recreation/checkout/reset, no network/imports/tests.

- `.git` census (all entries, `os.walk` + `lstat`, type-aware):
  SRC `.git`: regular 83, dirs 48, symlinks 0, other 0, intra-repo duplicate-inode keys 0.
  DST `.git`: regular 83, dirs 48, symlinks 0, other 0, intra-repo duplicate 0.
  RECON `.git`: regular 3062, dirs 271, symlinks 0, other 0, intra-repo duplicate 0.
  Shared regular inodes: DST vs SRC 0, DST vs RECON 0, SRC vs RECON 0 (all 0 expected independent).
  Worktree regular files (excluding `.git`): SRC 707, DST 707, shared 0.
- Alternates/configs fail-closed: `objects/info/` absent (exit 2) SRC/DST; `objects/info/alternates` absent (exit 1)
  SRC/DST; `info/alternates` absent (exit 1) SRC/DST; RECON same absent pattern (recorded).
  Config inert (`example.invalid` SRC/DST, `github.com/eariver/...` RECON, no `promisor/partial/lazyfetch`);
  `core.sparsecheckout=true/cone=true` preserved SRC/DST; hooks only `*.sample` SRC/DST (no active hooks);
  `shallow` `774dd39a...` SRC/DST; `HEAD` detached `409b292` SRC/DST vs attached `refs/heads/main` RECON.
  Any present alternates / active hook / shared inode would have been explicit blocker — none found.
- Source22 pre/post + cache scope: `src_pin_pre OK=22/22 MISMATCHES=0`, `src_pin_post OK=22/22` (no mutation);
  DST pins `OK=22/22` (prior prep stdout). Cache probe depth-limited (`__pycache__` absent at root SRC/DST,
  `maxdepth2 find` empty) — NOT whole-tree guard/execution-fixture certification (explicit limit).
  Inode walk scope is full `.git` (83+83+3062 regular) + full worktree regular (707+707) via `lstat` dev:ino,
  not prior 4-sample. Snapshot identity only, not generic guard certification.
- AST/registry scope: `_SHARED_PY` 27 + `_SHARED_SCHEMAS` 5 + Weekly 8 + Longform 14 exact names in inspect
  stdout; top-level imports for 15 modules enumerated read-only (no `import survey_*` executed).
  `contract_files.pipeline` 62 + `quality` 3 + `implementation_control_roots` 4 recorded.
  Dynamic final-code actual-import check later must reproduce §4 sets; any required change returns to root.

## 8. Blockers / return

Essential blockers: NONE for 3-worker authorization. Enforcement gates (not waived):
(a) final-code AST + `git grep` closure vs `contract_files` audit must reproduce §3–§4 sets exactly;
(b) toolchain absolute path + allowlisted argv/env + `.latexmkrc` recipe hash recorded, no shell string;
(c) fixture SOURCE commit before authority (no F0 self-reference); (d) L API return keys exactly per §2,
no caller verified-dict. Original `implementation-map-20261020.md` preserved; this resolution overrides
only ownership overlap, `e.g.` counts, spec paths, recipe/self-hash, and 4-sample scope as above.

**Return complete. Awaiting root authorization of 3 workers under frozen ownership/interfaces.**
