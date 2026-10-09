# LF-1 design proposal — source-only longform reader-input projector (preimplementation)

2026-10-09. Preimplementation only. No candidate source edits, no tests run,
no fixture executed, no commits/branches, no network, no Summary/main intake,
no old scripts, no reconstruct writes beyond this packet.
Whole candidate NOT_READY, step4/B3 OPEN, canonical audit unstarted.

## 0. Identities, packet, method

- Fixed source: `409b292756dd1277b9dfae87679934c0d2ce251c`,
  tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`,
  parent `34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4`.
- Source read: `/tmp/opencode/jgas-dm004-impl-20261004T234416Z`
  (HEAD/tree/parent/clean/inert-origin/shallow/no-alternates verified pre-copy).
- Independent byte-copy (this proposal's read basis):
  `/tmp/opencode/jgas-lf1-design-20261009T001653Z`
  - HEAD/tree/parent identical to fixed409; `status --porcelain` empty;
    origin `https://example.invalid/rephase-candidate-recovery.git` inert;
    `--is-shallow-repository true`; no `.git/objects/info/alternates`;
    zero symlinks; zero objects with nlink>1; zero shared object inodes
    vs source (comm of inode lists = 0); refs identical to source
    (4 heads, no new refs); `GIT_DIR/WORK_TREE/CEILING/COMMON` unset;
    no partialClone/promisor.
- Reconstruct: `1610777e7948a94a725dd4836d23337256a49f53` (Human continuation),
  read-only; no branch/ref writes.
- Packet: `notes/rephase-1-longform-lf1/evidence-20261009T001653Z/`
  (`commands.txt`, `source-identity.log`, `dst-identity.log`,
  `isolation.log`, this `design-proposal.md`).
- Governing inputs (unchanged):
  decision `outputs/rephase-1-special-support-contract-decision.md`
  (sha256 `796c65fca59f5a2461aca82065d0448e12410d1d3c341c2d2ab8ac2e7942e9b9`),
  `notes/rephase-1-special-support-contract/independent-design-review.md`
  (DESIGN_BOUNDED_PASS), `notes/rephase-1-special-support-contract/astra-review-resolution.md`
  (F1–F5 dispositions). Prior General proposal errors superseded; no options redo.
- Method: source-only `Read`/`Glob`/`Grep` + `git rev-parse/status/remote/for-each-ref`,
  `stat`, `find`, `cp -a`, `du`. No `python` execution of candidate code
  (not even `-c` probes), no test/fixture/build, no legacy writer invocation.
  All `file:line` below are observed in the independent copy
  (byte-identical to fixed409).

Scope: THEMATIC + LONGFORM_SPECIAL, first format
`THEMATIC_FOUR_FAMILY_LINEAGE_V1` only. No Retrospective/manual-TeX,
no Weekly closure change, no universal parser, no new reviewer role,
no DIRECT_PRIMARY upgrade, no migration/revalidation of history.

---

## 1. Full emitted-value mapping (no raw Draft replay, no meta.title)

Inventory basis is the active wrapper
`scripts/survey_longform_publication_v2.py:43-147`, not
`_base.render_package`. Base raw-Draft-block replay
(`scripts/survey_longform_publication_v2_base.py:245-255`,
`spec_blocks` + `result.blocks` loop) is REJECTED as render truth;
raw Draft bodies are validation/provenance inputs only, per decision §4.
Base fixed title is a literal, not a profile field (see F5).

### 1.1 Proposed reader-input top-level keys (order as listed; JSON object
order not semantically significant, canonical bytes per §5)

| # | Key | Type | Source / ordering | Emitted use (fixed409 citation) |
|---|---|---|---|---|
| 1 | `schema_version` | const `"2.0-rc1"` | format constant | cf. base `_validate_input:108` envelope |
| 2 | `route` | const `"LONGFORM_GENERATED_V1"` | proposed route (not present in 409) | cf. Weekly `ROUTE="WEEKLY_GENERATED_V2"` (`survey_weekly_derivation_v2.py:25`); Gate `derivation.oneOf` currently DIRECT_PRIMARY-only or WEEKLY_GENERATED_V2 (`reader-surface-gate-v2.schema.json:159-186`) — LF-2 Gate change separate, LF-1 must not claim Gate support |
| 3 | `format` | const `"THEMATIC_FOUR_FAMILY_LINEAGE_V1"` | proposed format (not present in 409); explicit four-family restriction | wrapper `:138` header `観点 & GLM & Qwen & DeepSeek & Kimi`; base `:56` kicker; base `:192` `sp001` keys; base `:194-195` `len(comparison)>=3` |
| 4 | `issue_id` | nonempty string, `^[A-Za-z0-9][A-Za-z0-9._-]*$` | State-bound Profile `issue_id` (`survey-production-profile.schema.json:18`, `survey-production-state.schema.json:15`) | base `_validate_input:108` envelope check |
| 5 | `research_profile` | const `"THEMATIC"` | State/Profile | base `main:130` requires LONGFORM_SPECIAL publication profile; research THEMATIC per decision |
| 6 | `publication_profile` | const `"LONGFORM_SPECIAL"` | State/Profile | same |
| 7 | `issue_metadata` | object §1.2 | validated Profile + fixed labels | base `:87-88,191` |
| 8 | `visible_text` | object §1.3 | style contract constants, explicit IR members | `jgaisurvey.sty:75-100`, wrapper/base fixed strings |
| 9 | `cover` | `{headline,deck,anchors}` authored, list order retained | publication-authored input (constrained choice, not checkpoint-accepted research) | base `_validate_input:109-111`, `_render_tex:89` |
| 10 | `frontmatter` | `{heading,lede,scope_notes}` authored, order retained | same | base `:112-113`, `_render_tex:91-94` |
| 11 | `packages` | array, `(drafting_order,package_id)` order from accepted Architecture | accepted Draft Result headline/deck + normalized revision supplement + derived kicker | base `:141` sort, `:96-99` loop, wrapper `render_package:43-119` |
| 12 | `cross_family_synthesis` | `{heading,paragraphs,comparison_rows}` authored, order retained | normalized revision | base `:190-208`, wrapper `render_cross_family:122-147` |
| 13 | `final_summary` | `{heading,const; paragraphs,>=3,order}` authored | authored `final_summary.heading/paragraphs` | base `:114-116`, `_render_tex:101-103` — MANDATORY, end-of-publication order |
| 14 | `bibliography` | array, first-seen cited order §1.6 | strict accepted-data mapping §2 | base `:159-168,192-193`, `_bib_text:35-53` |
| 15 | `provenance` (MECHANICAL ONLY, excluded from reader hash) | object §5 | State/Profile/Architecture/approval/Draft/Evidence/Card/Matrix/Materiality/Discovery refs + tool closure + `review_reference` free text + runner/recorded-at | cf. Weekly `accepted_refs`/`current_tools` pattern (`survey_weekly_derivation_v2.py:519-559,573-632`); base `:85` `% Generated…` comment + `:98` variable package/result-hash comment stay mechanical evidence per F4 |

`review_reference` (`base:85` `_nonempty`, `validate_revision:82-85`) is
mechanical-only free text, never reader authority, never rendered.
`runner`/`recorded-at`/receipt/tool/source hashes similarly excluded.
No whole Profile/State/Draft/manifest dump as reader target.

### 1.2 `issue_metadata` (exact display values, date kinds distinct)

- `title`: const `"Japanese Generative AI Technical Survey Special"`
  (base `_render_tex:87` literal). NO `meta.title` source (F5); do not add
  a purported authored/profile `meta.title` field.
- `edition_descriptor`: const `"Thematic Longform Special"`
  (base `:88` `\surveyeditiondescriptor`).
- `display_as_of`: exact display string derived from validated Profile
  `research_scope.temporal_policy.as_of` for THEMATIC
  (`OPEN_HISTORY_AS_OF` or `CURRENT_STATE_AS_OF`,
  `survey-production-profile.schema.json:75-93`) via the existing
  transformation `as_of.replace("T"," ").replace("Z"," UTC")`
  (base `:191`). Preserve the fixed prefixes:
  `Thematic history / as of {display}` and `As-of boundary: {display}`
  (base `:87`) as explicit IR strings, not recomputed by the renderer.
- `as_of_source`: the raw Profile `as_of` ISO-8601 (for audit, not display).
- Date-kind separation (mandatory): `display_as_of` (research boundary)
  ≠ event dates (inside authored chronology prose, not separate date
  fields) ≠ access dates (`urldate` per bibliography entry, from
  `resolve_source_access_provenance`, §2) ≠ publication dates
  (future LF-2 receipt/Gate timestamps, mechanical only).
  Never substitute edition cutoff/window end/retrospective as-of
  for `urldate` (cf. `survey_bibliography_access_provenance_v2.py:1-7`
  module docstring).

### 1.3 `visible_text` (every fixed/helper/style-visible string as explicit IR)

All emitted constants must come from this object; the future renderer
must pass them explicitly through the existing style interface
(`jgaisurvey.sty:75-100` setters, cover/table emission `:110-138`).
Longform base currently relies on style defaults — gap to be closed
in LF-2 serializer, not assumed covered. Proposed keys (all nonempty strings):

- `cover_cutoff_label`, `cover_repository_label`, `cover_build_label`,
  `repository_value`, `build_value`, `strapline`
  (cf. Weekly `VISIBLE_TEXT:38-50` which already passes
  `eariver/japanese-generative-ai-survey`, `LuaLaTeX / jlreq / LuaTeX-ja`,
  cutoff/repository/build labels, edition descriptor, strapline explicitly
  at `survey_weekly_derivation_v2.py:400-414`; Longform must match this
  explicitness; style defaults at `jgaisurvey.sty:70-73` are NOT authority).
- `edition_descriptor`: `"Thematic Longform Special"` (displayed via
  `\surveyeditiondescriptor` + cover strapline line `:136`).
- `frontmatter_boundary`: `"Scope / attribution boundary"`
  (base `:92` `\begin{claimboundary}[Scope / attribution boundary]`).
- `claim_boundary`: `"Claim boundary"` (wrapper `:95`).
- `theme_overview_title`: `"Theme at a glance"` (wrapper `:59,68`).
- `timeline_heading`: `"Transition timeline"` (wrapper `:80`).
- `technical_notes_heading`: `"Source-backed Technical Notes"` (wrapper `:101`).
- `cross_family_kicker`: `"CROSS-FAMILY SYNTHESIS"` (wrapper `:127`).
- `cross_comparison_title`: `"Cross-family comparison"` (wrapper `:135`).
- `cross_table_header`: exact ordered tuple
  `["観点","GLM","Qwen","DeepSeek","Kimi"]` (wrapper `:138` normal
  full-width; base `:289-306` sidewaysfigure is NOT canonical).
- `issue_summary_kicker`: `"ISSUE SYNTHESIS"` (base `:101`).
- `issue_summary_label`: `"sec:issue-summary"` anchor name (base `:102`
  `\label{sec:issue-summary}`) — mechanical-safe token, display-neutral.
- `references_title`: `"References / Source Notes"`
  (base `:103` `\printbibliography[title={...}]`).
- `toc_title`: explicit reviewed value OR disclosed build dependency.
  `\tableofcontents` (base `:95`) emits an implicit class label with no
  reviewed IR source in 409. LF-1 must NOT guess it. Options for Astra:
  (a) add `toc_title` to `visible_text` as a fixed constant to be
  reviewed, or (b) record as disclosed trusted-build dependency
  (pagination/layout internals remain trusted build/visual per decision §4).
  No silent "already covered".
- Fixed `% Generated…` comment (base `:85`) and variable
  `% package:{pid} draft-result-sha256:…` comment (base `:98`) are
  EXCLUDED from reader content (F4); variable hashes/provenance go to
  mechanical evidence; any retained constant comment must be inert and
  part of the trusted serializer (F2 resolution).

Kicker rule: per-package kicker is VISIBLE derived semantic input, not
mechanical (decision §4). Construction enumerated in §4; every displayed
effect (suffix words, ordinal) is in IR (`packages[].kicker`).

### 1.4 Per-package object (exact keys, types, normalization)

```text
packages[]:
  package_id: string (Architecture-bound token, §4 charset)
  drafting_order: integer >=1 (from Architecture `packages[].drafting_order`,
    `issue-architecture-v2.schema.json:53`)
  headline: nonempty string (accepted Draft Result `headline`, exact match
    to semantic archive `spec.headline`, base:146)
  deck: nonempty string (accepted Draft Result `deck`, exact match, base:146)
  deck_discovery_ids: nonempty list of DID, each `_DISCOVERY_ID`
    (`^[A-Za-z0-9._-]+-D\d{3,}$`, base:26), subset of assigned set,
    first-seen order (base `_ids:47-58`)
  kicker: nonempty string, derived per §4 (visible)
  theme_at_a_glance: list>=2 of {label,text,discovery_ids} (base:112-123)
  narrative_sections: list>=2 of {heading, paragraphs[{text,discovery_ids}]}
    (base:124-134)
  timeline: list>=2 of {label,text,discovery_ids} (base:135-146)
  synthesis: {heading, paragraphs[{text,discovery_ids}]} (base:147-153)
  reader_claim_boundary: nonempty list of {text,discovery_ids} (base:154)
  technical_notes: nonempty list of {title,discovery_id,chronology,
    technical_points(list>=2),limitation,primary_url} (base:155-183),
    with EXACTLY one note per assigned DID + explicit duplicate rejection
    (§2, §4, §7) — base `:181-183` set-equality alone is insufficient
```

Normalization (reuse exact base semantics, no invention):
- `_nonempty`: strip, reject empty (base:29-32).
- `_reader_text`: `_nonempty` + FORBIDDEN_READER_PATTERNS
  (base:16-24 plus wrapper `:18-22` additions `"Evidence pass"`,
  `"本Evidence"`) + `\bVerify\b` + DID-exposure regex (base:35-44,
  wrapper `_strengthened_reader_text:27-36` adds `scan_reader_text_lines`
  BLOCKING/UNRESOLVED refusal). All reader strings pass this.
- `_ids`: DID syntax + membership in assigned set + first-seen dedup
  (base:47-58). LF-1 preserves this; global bibliography order is
  first-seen across `(drafting_order,package_id)`-ordered packages
  then revision IDs (base:159-161), then cross-family (base:63-79
  `_revision_ids`).
- Envelopes exact: `longform_revision` must equal
  `{review_reference,new_external_evidence,packages,cross_family_synthesis}`
  (base:82-84); per-row envelopes exact (base:98-99,160-161,191,198);
  `new_external_evidence` must be `False` (base:86-87).
- HOLD/NEEDS_MORE promotion refused (base:110-111,166); missing Evidence
  refused (base:107-109).

### 1.5 Cross-family + final summary (mandatory categories)

- `cross_family_synthesis.heading`: nonempty reader text.
- `cross_family_synthesis.paragraphs`: nonempty list of
  `{text,discovery_ids}` (discovery_ids ⊆ selected_union, base:207).
- `cross_family_synthesis.comparison_rows`: list>=3 of
  `{dimension,glm,qwen,deepseek,kimi,discovery_ids}` (base:193-208).
  `dimension/glm/qwen/deepseek/kimi` are reader text (no header-only
  relabelling into unrelated topics; four-family shape explicit).
- `final_summary.heading`: const `"この号の総括"` (base:115 exact match;
  Weekly equivalent uses Architecture-bound heading at
  `survey_weekly_derivation_v2.py:174-175`, but Longform 409 hardcodes —
  LF-1 preserves the hardcoded constant as format rule, see §3).
- `final_summary.paragraphs`: list>=3 nonempty strings in order
  (base:116). Rendered at END_OF_PUBLICATION_BEFORE_REFERENCES_OR_END_MATTER
  (base:101-103, manifest `:202` placement field). Mandatory in IR and
  end-of-publication order; existing final-synthesis substantive obligation kept.

### 1.6 Bibliography / citation identity / order / placement

- Per-DID entry: `{discovery_id, key, title, author, url, urldate}`.
  - `title` = entity `canonical_name` (nonempty, §2).
  - `author` = same-entity `organization`, or literal `"Unknown"` when
    null/empty (base `_bib_text:38` fallback preserved, not guessed
    from another entity/host).
  - `url` = entity `canonical_url` (non-null/nonempty, §2); technical-note
    `primary_url` must equal it (base:165-167); conflict with old
    authoring data is explicit refusal, not silent rewrite.
  - `urldate` = `YYYY-MM-DD` from `resolve_source_access_provenance`
    (provenance module `:45-141`); missing/invalid access timestamp fails
    closed (`_bib_text:40-45` raises when no urldate).
  - `key`: `sp001` + `did.lower().replace("-","")` (base:192).
    COLLISION CAVEAT (new, for Astra): lowercasing + dash-stripping can
    collide for DIDs differing only by case/dash (e.g. `A-B-D001` vs
    `ab-D001`). LF-1 must refuse colliding DID sets explicitly rather
    than silently merging citations. Propose: build map, if
    `len(keys) != len(dids)` refuse with collision diagnostic.
- Citation anchors/ordering: `_cite` (base:221-222, wrapper:39-40)
  `\cite{key,...}` per placement; cited order = first-seen (base:159-161);
  all emitted placements (deck/glance/narrative/timeline/synthesis/boundary/
  notes/cross) included with exact discovery_ids.
- No implicit source switch or self-rehashed unrelated input; placements
  constrained to authorized package inputs via exact-one `refs` semantics (§2).

---

## 2. Real accepted chain, loaders, constructible fixture

### 2.1 Authority principle (no invented authority, no sidecar fallback)

- Validate acceptance + each named card path/hash through existing Evidence API.
  B `_strict_evidence_sources` (`survey_weekly_derivation_v2.py:182-203`:
  card path+sha, single-card DID uniqueness) is a PATTERN to adapt, not
  automatic Longform support. B `_records_from_authorities` (`:206-258`:
  Matrix title, `Unknown`, Discovery `source_locator`) is NOT a drop-in:
  Longform intends entity metadata (canonical_name/canonical_url/organization
  from the primary-subject entity).
- Publication-authored cover/revision/summary are authoring choices
  constrained by accepted sources, not checkpoint-accepted research or
  verbatim Draft copy.
- Adjacent `interactive-evidence.json` rows + `sources`/`source_bindings`
  fallback (base:156,170-178) are NOT accepted-card authority.
  Location beside validated acceptance or a manifest hash does not confer
  acceptance. LF-1 must use only the validated acceptance tree.
- No unbound sidecar `sources`/`source_bindings`, min/max/latest/date-of-window
  fallback, success mocks, or silent authority repair.

### 2.2 Exact loader set (all exist in 409; precise citations)

| Step | Existing API | Refusal if |
|---|---|---|
| State/Profile | `survey_agent_control_v2.validate_agent_state` (`:348-350` → `_validate_agent_state:353-499`); `_profile_and_source:105-120`; `survey_production_v2.validate_profile`, `repo_local_path`, `sha256_file`, `parse_instant`, `derive_control_fields`; `survey_schema_v2.validate_instance/load_and_validate_json` (`survey_schema_v2.py:55-71`) | State invalid, Profile drift, issue/Profile/contract mismatch, lifecycle/history/gate/checkpoint errors; `GIT_*` root overrides present (test guard pattern `test_survey_increment_b_weekly_derivation_v2.py:43-47`) |
| Checkpoints | `agent.resolve_checkpoint_artifact` (`:502-612`) + `resolve_active_evidence_views` (`:615-648`, same-checkpoint Evidence+Views binding + View→Evidence SHA binding) | wrong checkpoint, missing/duplicate artifact, SHA drift, symlink/unsafe, checkpoint-set mismatch |
| Evidence acceptance | `survey_evidence_v2.validate_evidence_acceptance` (`:1116-1167`: package copy, task/result exact sets, per-card `validate_evidence_card` + status/discovery_ids agreement, content-addressed `result_set_sha256` == run-dir name) + `validate_evidence_card` (`:880-...`, incl. `artifact.primary_subject_id ∈ entities` at `:898-901`) | any divergence, HOLD/NEEDS_MORE promotion downstream |
| Cards | per-result card file `sha256` vs acceptance row (`validate_evidence_acceptance:1152-1153`); single-DID/single-card uniqueness (new Longform check modelled on `_strict_evidence_sources:199-202`) | DID in multiple cards; card missing `sources`; multi-DID card in first-subset proof |
| Entity | card `entities[]` (`evidence-v2-card.schema.json:24-38`) + `artifact.primary_subject_id` (`:40-50`) | no entities; `primary_subject_id` not in registered set; `canonical_name` empty; `canonical_url` null/empty; multiple entities with unique primary-subject match still OK (not auto-ambiguous), else stop |
| Access | `survey_bibliography_access_provenance_v2.resolve_source_access_provenance` (`:45-141`: single-source URL-match-or-refuse `:79-88`; multi-source URL-match `:89-97`; equal-timestamp first-capture `:109-111`; different-timestamp fail-closed unless unique `explicit_source_id` `:112-126`; no min/max/latest per `:59-60`; missing-date fail-closed `:128-141`) + `load_evidence_sources` (`:144-207`) for `sources`/`explicit_source_id` from acceptance tree (NOT adjacent interactive fallback as authority) | no sources; URL mismatch; zero URL matches; ambiguous captures with different timestamps and no unique authority; missing `accessed_at` |
| Matrix/Materiality/Discovery | `candidate-matrix-v2.schema.json`, `materiality-ledger.schema.json`, `discovery-acceptance-v2.schema.json` + `agent.resolve_checkpoint_artifact` for `candidate-matrix`/`materiality-ledger`/`discovery-acceptance`; status/disposition bindings as in `_records_from_authorities:239-248` | Matrix↔acceptance SHA drift, Matrix↔ledger drift, accepted_status mismatch, materiality mismatch, Discovery row missing, `source_locator` missing (Discovery locator NOT used as bibliography URL for Longform — entity URL is) |
| Draft authorization | `survey_drafting_citation_refs_v2.refs` (`:40-87`: exact-one `did` in authorized `evidence_inputs` candidate rows via `candidate_matrix.rows`, duplicate `candidate_id` refused, first-seen ordered dedup, empty refused) | `evidence_inputs` missing/empty; `did` resolves ≠1; no refs |
| Draft validity | `survey_drafting_v2.validate_draft_result` (called at base:143) + `survey_draft_profile_v2.validate_extension_propagation` (`:22-43`: Profile/Publication extensions must exactly preserve Draft Package directives) + `validate_architecture_approval` (`survey_drafting_v2_base.py:105-134`: exact bytes binding of architecture/summary/attention + `reviewed_by/at/reference` + timezone-aware) | Draft drift, extension mutation, approval mismatch |
| Synthesis | `survey_drafting_v2.validate_synthesis_result` (called at base:137) | upstream synthesis invalid |
| Package order | Architecture `packages` sorted by `(drafting_order,package_id)` (base:141) | coverage differs from Architecture (base:188-189) |
| Reader-text hygiene | `survey_longform_publication_v2_base._reader_text/_nonempty/_ids/_validate_paragraph_rows` (`:29-72`) + wrapper `_strengthened_reader_text` (`survey_longform_publication_v2.py:27-36`, `scan_reader_text_lines` BLOCKING/UNRESOLVED refusal) | leakage patterns, `Verify`, DID exposure, invalid/out-of-package DID |

Eligibility subset for first proof (decision §5, unchanged):
single DID resolves exactly once inside authorized Draft Package evidence
inputs AND to one accepted card; that card carries a single DID in its
acceptance row; unique `entity_id == card.artifact.primary_subject_id`;
nonempty `canonical_name`; non-null/nonempty `canonical_url`;
organization from same entity or literal `Unknown`; access resolved ONLY
from that card's URL-matched sources; equal-timestamp duplicates follow
resolver rule, different-timestamp ambiguity stops; only VERIFIED/PARTIAL
with downstream eligibility (never HOLD/NEEDS_MORE/REJECTED promotion);
package authorization via Draft Package `evidence_inputs`/candidate rows
with exact-one `refs` semantics; revision placements may differ from raw
Draft prose but remain within authorized choices and are captured in the
reviewed object.

### 2.3 Constructible synthetic fixture path (through real loaders, not schema-only dicts)

YES — constructible with one adaptation (DID syntax). Path reuses existing
test factories; schema-only dictionaries do NOT count as accepted data.

1. `evidence_tests.SurveyEvidenceV2Tests.sandbox` (`test_survey_evidence_v2.py:31-46`:
   copies `config/schemas/scripts/templates/prompts/docs/data` contract files
   into temp root) + `init_profile(root,cfg,"THEMATIC")` (`:78-90`:
   `core.thematic_profile` with `OPEN_HISTORY_AS_OF`, `SP001`,
   `scope_dimensions ["lineage","competition"]`) — gives State/Profile/contract.
2. `make_screening` with ONE discovery whose `discovery_id` is COMPLIANT,
   e.g. `fixture-paper-D001` (NOT `"target-source"` as in
   `test_survey_architecture_v2.py:31`: `target-source` fails
   `_DISCOVERY_ID` (`base:26`). All downstream validators accept arbitrary
   IDs; only Longform enforces `-D\d{3,}`. Use compliant ID throughout
   (Discovery locator `https://example.invalid/fixture-paper-D001`).
3. `make_evidence` → `card_for_task` (`test_survey_evidence_v2.py:158-233`)
   already yields the required entity shape: `entities[target{Target Model,
   Example, locator}, comparator{...}]`, `artifact.primary_subject_id=target`,
   `sources[source-1{url=locator, PRIMARY_PAPER, accessed_at
   2026-08-22T02:10:00+09:00}]`, `claims[claim-1/AUTHOR_CLAIM]`,
   `status VERIFIED`. Single-DID card: one discovery → one task → one
   acceptance row (verify `discovery_ids==[DID]` in acceptance).
4. `make_views` (`:268-315`) with THEMATIC annotations
   (`lineage_role CORE`, `branch_ids [main]`, etc.) + `build_materiality_ledger`
   + completeness (`SATISFIED`, THEMATIC closure) + `derive_candidate_matrix`
   — all via `architecture_tests.chain` (`test_survey_architecture_v2.py:18-128`).
5. `selection_for` + `architecture_for` (`:131-223`): single package
   `pkg-001`, `drafting_order 1`, `primary_candidate_ids [cid]`.
   Extend with THEMATIC `profile_extensions{lineage_package_role CORE}` and
   `publication_extensions{longform_chapter_kind lineage}` as built.
   Approval via `drafting_tests.build_authorized_chain("THEMATIC")`
   (`test_survey_drafting_v2.py:19-90`: summary/attention/approval with
   `reviewed_by human-reviewer`, exact SHA binding) + `derive_package`
   (`:92-110`) + `valid_result` (`:112+`: CLAIM ref from card claims).
6. Semantic archive
   `draft/v2/interactive-drafting-synthesis-input.json` (`spec_by_id`,
   base:139): fixture must provide `deck_discovery_ids=[DID]` + minimal
   `blocks` carrying `[DID]` so `_assigned_ids(spec)` (`base:58-61`)
   = `{DID}` and `validation_plans=[{pkg-001,{DID}}]`.
7. Authored longform revision (publication-authored, constrained):
   one package row `pkg-001` with every emitted category —
   `theme_at_a_glance>=2`, `narrative_sections>=2`,
   `timeline>=2`, `synthesis`, `reader_claim_boundary>=1`,
   `technical_notes=[{title,discovery_id=DID,chronology,points>=2,
   limitation,primary_url=canonical_url}]` (exactly one note for the one DID),
   plus `cross_family_synthesis{heading,paragraphs>=1,
   comparison_rows>=3}` all citing `[DID]` (allowed: cross cites
   `selected_union={DID}`), `cover{headline,deck,anchors>=1}`,
   `frontmatter{heading,lede,scope_notes>=1}`,
   `final_summary{heading この号の総括, paragraphs>=3}`,
   `review_reference` nonempty free text (mechanical only),
   `new_external_evidence False`.
8. Load through the NEW projector's `load_derivation` (§5), which calls
   the real loaders in §2.2 in order; then `build_longform_reader_input`
   (pure); then `validate_longform_reader_input` (schema gate).
   At no point are schema-only dicts asserted as accepted; every DID/
   card/hash/URL/access claim passes through the validators above.

Known fixture caveats (disclosed, not blockers):
- DID must be `-D\d{3,}`-compliant; existing `"target-source"` fixtures
  are NOT reusable verbatim for Longform revision fields.
- Single-package fixture proves the mapping, NOT generic Thematic
  completeness or multi-DID/card attribution (explicitly out of first subset).
- THEMATIC synthesis payload shape differs from Weekly
  `current_interpretation` (`survey_weekly_derivation_v2.py:300-307`
  inapplicable here); fixture must use the THEMATIC synthesis contract,
  not import Weekly closing-summary policy (`_closing_summary:271-283`
  forces `profile_synthesis.current_interpretation` — must NOT be reused).

---

## 3. Directive authority — BLOCKED (evidence + minimum decision needed)

### 3.1 What the consumer does

`scripts/run_semantic_publication_v2_interactive_base.py:133-135`:

```python
directive_path=source_root/"editorial/post-architecture-directives-v2.json"; directive=_load(directive_path)
final_rows=[r for r in directive.get("requirements",[]) if r.get("kind")=="FINAL_ISSUE_SUMMARY" and r.get("required") is True]
if len(final_rows)!=1 or final_rows[0].get("placement")!="END_OF_PUBLICATION_BEFORE_REFERENCES_OR_END_MATTER": raise SystemExit(...)
```

Manifest binds `post_architecture_directive{path,sha256,directive_id}`
(`:202`). `_load` is `core.load_json` — no schema, no validator.

### 3.2 Exhaustive authority search (source-only, 409)

- `grep -rn "editorial"`: only the consumer above + unrelated
  "editorial" prose in tests/docs. No producer, no schema, no validator,
  no checkpoint artifact named `post-architecture-directives`,
  no `schemas/*directive*.json`, no `find -name "*directive*"` hits.
- `grep -rni "directive"`: consumer + `survey_draft_profile_v2.py:5,41`
  ("extension directives approved in Architecture and copied into the
  Draft Package" — a DIFFERENT mechanism: Architecture→Package extension
  propagation, validated by `validate_extension_propagation:22-43`, NOT
  the editorial JSON file).
- `grep -rn "FINAL_ISSUE"`: only the consumer line. No docs, no tests,
  no Architecture/Synthesis/Draft validator references it.
- Human contracts: `docs/special-human-gates.md` defines exactly two Human
  Gates (Architecture Review, Publication Preview); gate inputs in
  `config/survey-production-v2.json:218-226` are
  architecture/summary/attention and publication-candidate respectively.
  The directive file is in NEITHER gate input list.
- Architecture approval: `validate_architecture_approval`
  (`survey_drafting_v2_base.py:105-134`) binds ONLY architecture/summary/
  attention bytes + `approval_id/reviewed_by/reviewed_at/review_reference`.
  It does NOT bind the directive file.
- Architecture schema (`issue-architecture-v2.schema.json`) has NO
  directive/final-summary-placement field; `publication_extensions` is free
  object with no placement validator for Longform.
- Stage validation `DRAFT_COMPLETE` (`survey_stage_validation_v2.py:464-521`)
  requires manuscript/source/pdf/bundle/semantic/visual/gate — no directive file.
- `review_reference` (base:85) is `_nonempty` free text, explicitly denied
  as review authority (decision §5).

### 3.3 Interpretation

- NONBINDING authoring input: `cover`, `frontmatter`, `final_summary`
  text, revision prose, `review_reference` string. These are choices
  constrained by accepted sources, reviewed pre-TeX, never authority by
  themselves.
- CLAIMED binding directive: exactly-one `FINAL_ISSUE_SUMMARY required`
  row with `placement END_OF_PUBLICATION_BEFORE_REFERENCES_OR_END_MATTER`.
  The substantive placement (summary at end before references) is real and
  preserved by serializer order (base:101-103), but its ONLY 409 control
  is the unvalidated adjacent JSON file. A path/hash or `review_reference`
  string does not make it Human/Architecture authority (decision §5).

### 3.4 Verdict: BLOCKED — do not implement around it

LF-1 cannot BOTH (a) require the file (grants authority to an unvalidated
adjacent file with no producer/schema/checkpoint/Human binding) AND
(b) drop it (drops the only 409 encoding of the substantive placement
obligation) without one of:

**Minimum decision needed (Astra to select exactly one; no other change authorized):**

- **D1 (bind it):** Human/Architecture authority explicitly adopts the
  directive file — e.g. Architecture approval or a Human gate input binds
  its path+hash AND a new schema/validator governs its
  `{requirements[].kind/required/placement/directive_id}` envelope —
  with producer/checkpoint named. Then LF-1 `load_derivation` validates it
  via that authority.
- **D2 (harden as format constant, drop file dependency):** Human declares
  the placement a fixed four-family-lineage-v1 format rule
  (`END_OF_PUBLICATION_BEFORE_REFERENCES_OR_END_MATTER`, heading
  `この号の総括`, `paragraphs>=3`) requiring NO directive file; LF-1
  validates the constant and never reads
  `editorial/post-architecture-directives-v2.json`. The legacy consumer's
  file check is then a publisher-side (LF-2) migration item, not LF-1 input.
- **D3 (defer):** Human defers placement authority to LF-2
  publisher/receipt/Gate integration; LF-1 emits `final_summary` position
  as authored order only, with an explicit `placement_asserted` flag marked
  UNPROVED, and no publisher claim.

Until Astra selects D1/D2/D3, LF-1 is NOT implementation-ready.
This proposal provides the complete schema/API/fixture design so Astra CAN
decide, but no code/fixture/run may proceed on an invented authority.

---

## 4. Safety policy (F2 mandatory item; LF-1 proves, LF-2 serializer proves)

### 4.1 Package-ID / label / key / comment / URL / prose rules

- **Allowed `package_id` charset (Architecture-bound):**
  `^[A-Za-z0-9][A-Za-z0-9._-]*$` (same as Profile `issue_id`,
  `survey-production-profile.schema.json:18`; Architecture
  `package_id` is currently `minLength 1` only —
  LF-1 MUST enforce the stricter charset and refuse others).
  Rationale: IDs flow into `\label{pkg:…}` (wrapper:55, base:236),
  `% package:…` comments, and kicker suffixes. `tex_escape` on arbitrary
  text is NOT proof of safe label/URL/comment contexts (F2).
- **Label construction (exact):** `\label{pkg:{tex_escape(pid)}}` only;
  no other label prefixes; refuse `pid` containing `%{}[]#,` whitespace,
  or non-ASCII even after escaping. Labels are display-neutral mechanical
  tokens; any displayed effect of the ID goes through the kicker (below).
- **Kicker construction (exact, visible):**
  `f"THEMATIC LINEAGE {ordinal}/{total} — {package_id.rsplit('-',1)[-1].replace('_',' ')}"`
  (base:55-56). Enumerate: split on LAST `-`, take suffix, `_`→space,
  prefix `THEMATIC LINEAGE {ordinal}/{total} — `. Every displayed effect
  (suffix words, ordinal/total) is in IR `packages[].kicker`; raw IDs used
  only for anchors/provenance otherwise are mechanical. Refuse empty suffix;
  refuse IDs that make the kicker collide across packages in one issue.
- **Citation keys:** `sp001` + `did.lower().replace("-","")` (base:192).
  DID charset is `_DISCOVERY_ID` (base:26), so keys match
  `^sp001[a-z0-9._]+$`. LF-1 MUST detect key collisions across the DID set
  and refuse (do not silently merge `\cite` targets). Keys are mechanical
  tokens derived from accepted DIDs, never authored free text.
- **Comments:** Fixed `% Generated…` (base:85) excluded from IR (F4).
  Variable `% package:{pid} draft-result-sha256:…` (base:98) excluded from
  IR; hashes live in `provenance`, never in TeX comments. Any retained
  constant comment in LF-2 serializer must be inert (no `%` escapes that
  could re-enable parsing tricks) and part of the trusted serializer.
  Variable provenance/hash text must NEVER enter TeX.
- **URLs:** `primary_url` and bibliography `url` are ONLY the validated
  entity `canonical_url` (§2); technical-note URL MUST equal it or refuse
  (base:165-167). Emit as `\url{<url>}` WITHOUT `tex_escape`
  (wrapper:116) — therefore LF-1 MUST validate URL safety:
  nonempty, no whitespace, no `{}$%#^~\\`, ASCII printable, and
  `url.strip() == url`. Authoring URLs that disagree are refused, not rewritten.
- **Prose:** every reader string through `_reader_text` (+ wrapper
  strengthening) AND `tex_escape` (`render_article_draft_tex.py:32-45`:
  `\\ & % $ # _ { } ~ ^`) at render time. No raw-TeX escape hatch; no
  `\def/\csname`/catcode/Lua/computed reads; no `\input/\include`
  (cf. Weekly `validate_generated_closure:464-472` — LF-2 must adopt an
  equivalent Longform closure check; LF-1 schema refuses strings containing
  `\input`/`\include` patterns as defense-in-depth, but real refusal proof
  belongs to LF-2 serializer test).
- **Order:** cover anchors, frontmatter scope_notes, all paragraph/row
  lists, glances, timelines, syntheses, boundaries, notes, comparison_rows,
  bibliography — list order retained end-to-end; transformations preserve
  first-seen order (`_ids:56-57`, `_revision_ids:63-79`,
  `cited:159-161`).

### 4.2 What LF-1 proves now vs LF-2 serializer proofs

- LF-1 (source-only projector + schema): input validations — envelope,
  charset, DID syntax/membership, entity/URL/access/Materiality/status,
  exact-one refs, duplicate-note/collision refusals, order/canonical bytes,
  no-write (projector writes no `main.tex`/`references.bib`/`jgaisurvey.sty`,
  creates no Gate/PASS). LF-1 proves PROJECTION STABILITY (same accepted +
  same authored ⇒ same reader bytes; runner/provenance-only mutation ⇒
  same reader bytes, changed mechanical bindings), NOT operational review reuse.
- LF-2 (separate unit): real serializer refusal/escaping —
  `tex_escape`/`\url`/label/kicker rendering, `validate_generated_closure`
  equivalent, narrow receipt + independent re-derivation, Gate replay at both
  admission sites, two-pass no-write failure, tamper negatives, supported
  advancement, Weekly/direct-primary regressions. F3 "proven" means LF-2
  independent re-derivation + renewed receipt/Gate + output comparison;
  refreshed hashes or equal `main.tex` alone are insufficient.

---

## 5. API, canonical bytes, dependencies (source-only; no writer/Gate/CLI)

### 5.1 Proposed module (paths in §6)

`scripts/survey_longform_derivation_v2.py` — NEW, pure + read-only loaders.
Prefer NO CLI. If a CLI is later warranted (e.g. deterministic CI probe),
it requires separate Astra selection; LF-1 exposes importable functions only.

```python
def load_derivation(root: Path, state_path: Path, authored_path: Path) -> dict
    """Read-only: validate State/Profile/checkpoints/acceptance/cards/matrix/
    materiality/discovery/architecture/approval/packages/results/synthesis/
    archive via §2.2 loaders; return {surface_inputs, accepted_refs, records,
    provenance}. Refuses per §5.3. Writes nothing. Invokes no legacy writer."""

def build_longform_reader_input(
    issue_id: str,
    profile: dict, architecture: dict,
    authored: dict, synthesis_result: dict,
    ordered: list[dict], records: dict,
) -> dict
    """Pure projector: validated values → complete reader object (§1).
    No I/O, no State, no hashes, no Gate. Deterministic; order-preserving."""

def validate_longform_reader_input(root: Path, value_or_path: dict | Path) -> dict
    """Schema-gate + route/format/Profile-identity check via
    survey_schema_v2.validate_instance/load_and_validate_json against
    schemas/longform-reader-input-v2.schema.json. Returns normalized value."""

def canonical_reader_bytes(value: dict) -> bytes
    """core.json_bytes (indent 2, ensure_ascii False, +\\n) — file bytes.
    Digest = core.sha256_file / core.sha256_object (sort_keys compact)
    for receipt binding (LF-2)."""
```

Caller (LF-2, NOT LF-1): configured `DRAFT_COMPLETE`
`stage:reader-publication-validation` handler
(`config/survey-production-v2.json:330-333`) calls `load_derivation` →
`build_longform_reader_input` → materializes **reader input only** →
requires real persisted independent Reader-Surface PASS for those exact
bytes before ANY `main.tex`/`references.bib`/`jgaisurvey.sty` write.
Any new-operation call at an unsupported lifecycle refuses BEFORE the
legacy public wrapper could delete
(`run_semantic_publication_v2_interactive.py:23-63` eight owned unlinks
before `_base.main():67-68`; F1). LF-1 MUST NOT import or invoke
`run_semantic_publication_v2_interactive{,_base}` at all.

### 5.2 Canonical bytes + mechanical separation

- File bytes: `core.write_json` (`survey_production_v2.py:90-92` →
  `json_bytes:86-87`) — `(json.dumps(ensure_ascii=False, indent=2)+"\n")`.
- Digest: `core.sha256_file` (file bytes) for artifact refs;
  `core.sha256_object` (`:103-105`, sort_keys compact) for in-memory equality.
- Reader hash covers §§1.1 keys 1–14 ONLY. `provenance` (§1.1 key 15:
  state/profile/architecture/approval/package/result/acceptance/card/matrix/
  ledger/discovery/synthesis/archive/authored refs + tool closure +
  `review_reference`/runner/recorded-at) is EXCLUDED. Stability test mutates
  ONLY mechanical fields (e.g. `review_reference` string, runner name) and
  asserts identical reader file bytes + changed provenance bindings.
- Separate mechanical deps: `CURRENT_CLOSURE`-analog for Longform
  (provisional: new derivation module + new reader-input schema +
  `survey_longform_publication_v2{,_base}.py` + `survey_drafting_citation_refs_v2.py`
  + `survey_bibliography_access_provenance_v2.py` +
  `render_article_draft_tex.py` + `STYLE_PATH` + narrow receipt schema (LF-2));
  exact list requires Astra path decision + profile-neutral caller/closure
  analysis before ANY shared-helper extraction. No Weekly helper move,
  no `CURRENT_CLOSURE` change, no closing-summary import
  (`survey_weekly_derivation_v2.py:28-37` closure;
  `_closing_summary:271-283` inapplicable).

### 5.3 Refusal conditions (fail-closed, non-exhaustive but binding)

State/Profile/contract/checkpoint/acceptance/card/entity/access/matrix/
materiality/discovery/package/result/synthesis/archive mismatches per §2.2;
`research_profile != THEMATIC` or `publication_profile != LONGFORM_SPECIAL`;
`route/format` mismatch; `issue_id` mismatch; lifecycle < `DRAFT_COMPLETE`;
multi-DID/card ambiguity; missing/ambiguous entity/URL/access; HOLD/NEEDS_MORE;
exact-one `refs` failure; `primary_url != canonical_url`; duplicate technical-note
DID or missing coverage; empty/short lists (glance/narrative/timeline/notes/
comparison/final_summary); forbidden reader patterns/`Verify`/DID exposure;
package-ID charset violation; kicker/citation-key collision; unsafe URL;
unsupported TeX control in authored text; directive-file state per §3 decision
(D1: validate bound file; D2: never read file, enforce constant; D3: emit
UNPROVED flag, no publisher claim). No sidecar fallback, no silent repair,
no Weekly-field coercion, no malformed legacy-JSON fallback.

Reader-input-only output policy: LF-1 emits ONLY the validated reader-input
object (+ in-memory provenance for tests). It MUST NOT write
`main.tex`/`references.bib`/`jgaisurvey.sty`, MUST NOT create Gate/PASS,
MUST NOT modify shared lifecycle/admission, MUST NOT delete files.

---

## 6. Minimal changed-path budget (necessity; Astra-selected)

| Path | Change | Necessity |
|---|---|---|
| NEW `scripts/survey_longform_derivation_v2.py` | pure projector + read-only `load_derivation` + `validate_*` + `canonical_reader_bytes` (§5) | required: the component itself; no legacy-writer reuse |
| NEW `schemas/longform-reader-input-v2.schema.json` | reader-input schema (§1) with `route LONGFORM_GENERATED_V1`, `format THEMATIC_FOUR_FAMILY_LINEAGE_V1`, `visible_text` constants, per-package/cross/summary/bib shapes, `toc_title` handling, `provenance` excluded from reader hash | required: validation gate for the projector |
| NEW `tests/test_survey_longform_derivation_v2.py` | focused proof (§7), synthetic Thematic fixture via real loaders, no full old suites | required: feasibility evidence |
| (LF-2, NOT LF-1) narrow Longform receipt schema; existing public/base entrypoints + active wrapper serializer; Gate/runtime/schema + reader wrapper forwarding; contract registration | provisional per decision §6 | deferred; every threading change needs demonstrated gap + separate selection |

Any shared-helper extraction (e.g. generalizing `_strict_evidence_sources`
or `resolve_source_access_provenance` callers), config/contract change,
or Weekly closure modification requires EXPLICIT Astra selection with
profile-neutral caller/closure analysis. `survey_reader_fidelity_v2.py`
and manuscript schema stay unchanged unless a demonstrated necessary
interface gap is separately selected. No CLI unless a concrete necessary
interface warrants it (none identified — functions suffice).

---

## 7. Focused verification (real loaders; no coverage decoration)

Harness pattern: isolated temp-root Git DB (inert origin, no alternates,
no `GIT_*` overrides — cf. `test_survey_increment_b_weekly_derivation_v2.py:43-76`
`git ls-files` copy + `git init/commit`), THEMATIC chain via
`evidence_tests`/`architecture_tests`/`drafting_tests` helpers (§2.3),
strict pre/post `HEAD`/`tree`/source-vs-HEAD guards + no-write oracles
before fixture cleanup (LF-1 implementation phase, not this proposal).
Exact methods (names provisional, semantics binding):

1. `test_valid_single_did_primary_subject_projects_every_category`
   — fixture §2.3 (1 pkg, 1 DID, 1 note, cross>=3 rows, final summary,
   all kickers/style labels incl. `toc_title` disposition); assert
   `validate_longform_reader_input` PASS + every §1 category present +
   `bibliography[0]=={DID,key,title,author,url,urldate}` with entity values.
2. `test_source_selection_ambiguity_refuses` — DID in two cards → refuse;
   DID resolving 0 or 2× in package `evidence_inputs`/matrix → refuse
   (exact-one `refs`); card with 2 DIDs in first-subset mode → refuse.
3. `test_card_hash_membership_access_url_refuses` — tampered card bytes
   (SHA drift), DID-missing acceptance, `canonical_name` empty,
   `canonical_url` null/empty, `primary_url != canonical_url`,
   sources URL-mismatch, zero URL matches, different-timestamp ambiguous
   captures without unique `explicit_source_id`, missing `accessed_at` →
   each refuses with distinct diagnostic (no min/max/latest fallback).
4. `test_duplicate_note_and_citation_order_refuses_or_preserves`
   — duplicate technical-note DID (`[DID,DID]` over `{DID}`) refuses
   (extra beyond set-equality); `comparison_rows<3`, `theme_at_a_glance<2`,
   `narrative<2`, `timeline<2`, `final_summary.paragraphs<3` refuse;
   per-field duplicate citation dedups first-seen (base `_ids`);
   global bibliography order == first-seen across
   `(drafting_order,package_id)` + revision IDs; kicker/citation-key
   collisions refuse.
5. `test_every_emitted_category_mutation_breaks_bytes`
   — one mutation per §1 category (title/descriptor/date-prefix/cutoff
   words, cover/headline/deck/anchors, frontmatter, per-package kicker/
   glance/narrative/timeline/synthesis/boundary/notes, cross heading/rows/
   `観点/GLM/Qwen/DeepSeek/Kimi`, final summary, bib key/title/author/URL/
   urldate, each `visible_text` label) changes canonical reader bytes;
   raw Draft-body-only mutation does NOT change reader bytes (proves no
   raw replay); `meta.title`-invention has no source (proves F5).
6. `test_nonreader_projection_stability_with_distinct_binding`
   — mutate ONLY `review_reference`/runner/recorded-at (mechanical) →
   identical `canonical_reader_bytes` + changed `provenance` bindings;
   independent re-derivation yields identical bytes (F3 scope: stability
   only, NOT review reuse).
7. `test_unsupported_format_lifecycle_and_no_write_inventory`
   — `WEEKLY`/wrong route-format/profile, lifecycle < `DRAFT_COMPLETE`,
   malformed legacy JSON → refuse; pre/post `git status --porcelain` empty,
   `main.tex`/`references.bib`/`jgaisurvey.sty` absent, no Gate/PASS created;
   legacy writer (`_prepare_revision` deletion path, `_base.main`) never
   imported/called (assert via `sys.modules` + filesystem inventory).

Affected regressions (justified by actual deps, NOT full suites):
`test_longform_publication_v2.py` (3 preflight/hygiene tests),
`test_survey_bibliography_access_provenance_v2.py` (resolver semantics),
`test_survey_drafting_v2.py` THEMATIC paths + `test_survey_evidence_v2.py`
acceptance paths touched by fixture reuse. No old 405-compile/79-JSON/
16-manifest reruns, no Windows/Actions/all-profile runs for decoration.
Director-authority tests blocked until §3 D1/D2/D3 selected.

---

## 8. Risks, non-goals, STOP

- **Authority BLOCKED (§3):** no implementation/fixture-run until Astra
  selects D1/D2/D3. Do not invent authority, drop the placement obligation,
  or add a producer/role/Gate.
- Net lifecycle savings unmeasured; generated direction justified by
  sufficiency/provenance/invalidation goals, not zero-cost claim.
- Semantic/rendered acceptance (DM-006/013/018/020: JA meaning, date-role
  fidelity, claim/attribution sufficiency, log→page/clipping/appendix)
  remains distinct and open; no semantic PASS generator imported.
- No old PASS transfer; changed head/merge/base invalidates PASS.
- Token/URL/label proof split: LF-1 schema refusal now, LF-2 real
  serializer refusal/escaping later (F2).

**STOP for Astra.** Awaiting path decision (especially §3 D1/D2/D3 +
`toc_title` disposition + closure list) before ANY implementation,
fixture execution, or LF-2 work. Next unit on selection: implement ONLY
the selected source-only component in
`/tmp/opencode/jgas-lf1-design-20261009T001653Z` with exact
commands/runtime/argv/cwd/env, raw stdout/stderr/exits, strict fail-closed
guards, no-write oracles, and explicit successor-portability proposal;
reconstruct commits/Push remain Human-owned.
