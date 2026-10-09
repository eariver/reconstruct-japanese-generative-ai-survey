# LONGFORM_SPECIAL contract — independent scoped DESIGN review (not implementation approval)

2026-10-09. Fresh author-independent scoped DESIGN reviewer. Root (Astra) authored
`outputs/rephase-1-special-support-contract-decision.md`; General authored prior
`analysis.md` / `correction-and-contract.md` / `generated-contract-feasibility.md`.
This reviewer is separate from both authors. This is a contract-direction design
check only: no implementation approval, no canonical audit, no code/test/fixture/
build/network, no Human authority claim. Whole candidate stays NOT_READY, step4/B3
OPEN, canonical audit unstarted.

## 1. Reviewed documents (exact hashes)

- `outputs/rephase-1-special-support-contract-decision.md`
  sha256 `796c65fca59f5a2461aca82065d0448e12410d1d3c341c2d2ab8ac2e7942e9b9`
- `notes/rephase-1-special-support-contract/task.md`
  sha256 `2268f50afeca560e42abec37aed5b8347b086118dbe0c3e63d1505f53f9d8922`
- `notes/rephase-1-special-support-contract/analysis.md`
  sha256 `8d80c406829f192492ecf77854a2ac53f9d671325bdff2cb688b78bff2b8bbd9`
- `notes/rephase-1-special-support-contract/correction-and-contract.md`
  sha256 `b6f19249178f4f14092fc457082c49fe5f6460cd114e8c553052dd466a46bc13`
- `notes/rephase-1-special-support-contract/astra-scope-selection.md`
  sha256 `38a05896eccbeb484d19ac4b7658b6c19331f3d236e977ffbd27811049de4b32`
- `notes/rephase-1-special-support-contract/generated-contract-feasibility.md`
  sha256 `9899ded3d7519050948f9f2c8f03405df5d2dba56c2dc830c0c71412bbd49047`

Decisions/qualifications in the decision supersede conflicting options below them;
prior packet files remain preserved source analyses/proposals, not authority.

## 2. Source identity and method

Fixed source `/tmp/opencode/jgas-dm004-impl-20261004T234416Z`, verified read-only with
`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`, inherited root
overrides unset, no checkout/ref/object writes, no lazy fetch:

- HEAD `409b292756dd1277b9dfae87679934c0d2ce251c`
- tree `8ce3699861505f32d1d60bdc185d4d4f635aedb2`
- parent `34f934e9783f06d5ad5c0eb3a5cb38dadecfe5c4` (short `34f934e`)
- `status --porcelain` empty before and after (tracked clean)
- origin `https://example.invalid/rephase-candidate-recovery.git` inert (fetch/push)
- `--is-shallow-repository true` (inherited shallow at 774 only)

No production/main/Summary refetch, no linked primary-record intake, no fixture
objects/refs, no source edits. `sha256sum` used for document hashes only. No
subagents. Source reads only; the two `python3 -c` JSON/sha probes in this session
were read-only inspection aids, not test/fixture/build execution.

## 3. Design examination (source file/line evidence)

- **Caller/stage mismatch + delete window.** Decision §2 correctly states base
  initial guard `stage:semantic-publication-validation` at
  `run_semantic_publication_v2_interactive_base.py:122` vs configured
  `DRAFT_COMPLETE` handler `stage:reader-publication-validation` at
  `config/survey-production-v2.json:330-333`. Public
  `run_semantic_publication_v2_interactive.py:32-39` gates deletion on exact
  RELEASE_CANDIDATE + PUBLICATION_PREVIEW + pending + no-provenance, then unlinks
  eight owned artifacts at `:46-63` before `_base.main()` at `:67-68`; base
  validates State/input only at base `:126-127` and writes TeX/bib/style with
  preflight only at `:187-205` with no persisted pre-TeX review call. Decision
  marks this read-not-executed, refuses to certify pending behavior, and notes
  resolve-then-`is_symlink` checks are not raw-alias refusal proof. §6.1 selects
  the configured handler with reader-input-only materialization then a real
  persisted Reader-Surface PASS before TeX/bib/style writes; §6.5 requires any
  new-operation call at an unsupported lifecycle to refuse before the old wrapper
  could delete, with legacy deletion uncertified and no default Weekly-R1-owner
  reuse. This preserves the delete-before-validation hazard as an explicit stop,
  not a reused path.
- **Reader-field completeness vs active wrapper/base/style.** Decision §4 uses the
  active wrapper `survey_longform_publication_v2.py:43-147` as inventory, not
  `_base.render_package`. Verified: wrapper docstring `:50` and code render only
  `supplement` (cover/headline/deck/anchors, frontmatter, glance/narrative/
  timeline/synthesis/claim-boundary/notes, cross-family) with no `result.blocks`
  loop, while base `survey_longform_publication_v2_base.py:245-255` replays Draft
  blocks with `source_spec.discovery_ids` cites. Decision correctly rejects the
  feasibility raw-Draft-block row: raw Draft bodies are validation/provenance
  inputs, not an alternative render truth. Fixed title literal at base `:87`
  (`Japanese Generative AI Technical Survey Special`), fixed edition descriptor
  at `:88`, cover at `:89`, frontmatter at `:91-95`, per-package loop at `:96-99`,
  cross-family at `:100`, final summary at `:101-103` are all covered; derived
  kicker at base `:56` is correctly kept as visible semantic input. Cross-family
  shape correctly names the wrapper normal full-width table at wrapper `:135-138`
  (`観点 & GLM & Qwen & DeepSeek & Kimi`) as canonical, not the base
  `:289-306` sidewaysfigure. Fixed/helper strings (box/kicker/note/reference
  labels, repository/build labels+values, edition descriptor, strapline) are
  required as explicit IR members with future explicit setter passing through the
  existing style interface (`jgaisurvey.sty:75-100`, cover/table emission
  `:110-138`); Weekly `survey_weekly_derivation_v2.py:400-414` already passes
  repository/build/coverlabels/strapline/edition explicitly, while Longform base
  currently relies on style defaults — the gap is correctly identified, not
  assumed covered. Implicit class labels (e.g. TOC title from `\tableofcontents`)
  are correctly left as an explicit reviewed value or disclosed build dependency,
  not a guessed field. Layout internals (pagination, `\Needspace`/`\clearpage`/
  `multicols`/`wideflow`/`tabularx` measure) remain trusted build/visual
  responsibility. No contradictory opaque-bundle projection is selected.
- **Accepted authority, card/DID/primary-entity/access.** Decision §5 requires
  validated State/checkpoint references and existing validators, refuses
  canonical-path presence or manifest-hash adjacency as acceptance, and treats
  publication-authored cover/revision/summary as constrained choices, not
  checkpoint-accepted research or verbatim Draft copy. Verified: base `:156`
  reads adjacent `interactive-evidence.json` rows with `:170-178`
  sources/`source_bindings` fallback and only HOLD/NEEDS_MORE/canonical-URL
  presence checks — not accepted-card replay. Single-DID/single-card,
  `entity_id == card.artifact.primary_subject_id`, nonempty `canonical_name`,
  non-null/nonempty `canonical_url`, same-entity organization with explicit
  literal `Unknown` fallback, and URL-matched `resolve_source_access_provenance`
  (`survey_bibliography_access_provenance_v2.py:45-126`: equal-timestamp first
  capture, different-timestamp fail-closed unless explicit `source_id` resolves
  uniquely, no min/max/latest heuristic per `:59-60`) are all grounded in
  `evidence-v2-card.schema.json:24-50` (`entities[]`, `artifact.primary_subject_id`)
  and `survey_evidence_v2.py:899-900` (`primary_subject_id` must reference a
  registered entity). B helpers correctly bounded: `_strict_evidence_sources`
  (`survey_weekly_derivation_v2.py:182-203`: card path+sha, single-card DID
  uniqueness) is a pattern, while `_records_from_authorities` (`:206-258`: Matrix
  title, `Unknown`, Discovery `source_locator`, access resolution at `:252`) is
  explicitly not a drop-in because Longform intends entity metadata. Package
  authorization via Draft Package `evidence_inputs`/candidate rows with exact-one
  `survey_drafting_citation_refs_v2.refs:40-72` semantics is grounded; base
  `_assigned_ids(spec)` from the authored archive is correctly denied as itself
  Architecture acceptance. `review_reference` free text (base `:85` `_nonempty`)
  is denied as review authority. Directive file at base `:133-135` is denied as
  Human authority by path/hash; LF-1 must identify its control role and stop on
  unresolved conflict rather than drop the requirement or invent a gate. DM-016/
  017 remain separate upstream prerequisites; shared helper extraction only after
  profile-neutral caller/closure analysis, with no silent Weekly helper move,
  CURRENT_CLOSURE change, or closing-summary import (`_closing_summary:271-283`
  forces `profile_synthesis.current_interpretation`, inapplicable here).
- **Citations/format restrictions.** `sp001`-prefixed keys at base `:192`,
  `_cite` at base `:221-222`, cited order at base `:159-161`, per-placement cites
  throughout wrapper/base renderers, and `technical_notes[].primary_url ==
  canonical_url` at base `:165-167` support the §4 bibliography/citation row
  (key/title/author/URL/urldate plus anchors/ordering, no implicit source switch).
  Four-family lineage v1 (`THEMATIC LINEAGE` kicker `:56`, four columns
  `:138-144`/wrapper `:138`, `sp001` keys `:192`, `len(comparison)>=3` at
  base `:194-195`) is retained as an explicit restriction; THEMATIC +
  LONGFORM_SPECIAL only, Retrospective generated route unproved, no Weekly-field
  coercion, no legacy-JSON fallback, no header-only relabelling. `LONGFORM_INITIAL`
  is correctly labelled an operation shorthand, not a new profile enum (no such
  enum in 409); proposed `LONGFORM_GENERATED_V1` /
  `THEMATIC_FOUR_FAMILY_LINEAGE_V1` and `reader-surface-input-v2.json` /
  `longform-reader-input-v2.schema.json` are correctly marked as proposed names,
  not fields present in 409.
- **Review-role preservation.** DIRECT_PRIMARY/PRIMARY_ONLY limits preserved with
  no silent upgrade; Gate `derivation.oneOf` verified as DIRECT_PRIMARY-only or
  WEEKLY_GENERATED_V2 receipt
  (`reader-surface-gate-v2.schema.json:159-186`, `_derivation_for_manuscript`
  `:1071-1118`: exact primary bytes else Weekly research/publication profile,
  canonical input, receipt, two-support closure). STYLE byte-binding vs scan gap
  correctly scoped: sized manuscript refs (`survey_reader_publication_v2.py:
  221-236`) plus Gate `scanned_surfaces` (`survey_reader_surface_gate_v2.py:
  1217-1232`) bind bytes, while `SUPPORTING_SOURCE and suffix == .tex` at `:1241`
  and `:1752` lets `.sty` fall through with no `scan_tex`; leakage lint masks
  only listed constructs (`mask_tex_comments_and_structural_macros:496-537`),
  not `\def`/`\csname`/catcodes/Lua/computed reads. Fidelity correctly scoped to
  raw canonical `main.tex` numbered blocks (`parse_longform_blocks:105`,
  `validate_reader_fidelity:245-322`, substantive adequacy left to semantic
  review); technical-note `set(note_ids) != allowed` at base `:181-183` is
  correctly noted as not enforcing exactly-once cardinality despite its message.
  Later SEMANTIC_EDITORIAL/VISUAL/Architecture/Human Preview obligations remain
  with current owners; no new reviewer role, no late-PASS reuse, no universal TeX
  parser, no migration/revalidation of historical editions.
- **LF-1 vs LF-2 boundary, lifecycle/readback, cost.** LF-1 is source-only
  schema + projector with real accepted-authority loaders (no success mocks or
  renamed sidecars), single-DID/primary-subject proof covering every emitted
  category plus ambiguity/duplicate/citation/order/mechanical-only controls, with
  no `main`/bib/style writes and no Gate/PASS or readiness implication; LF-2 must
  separately prove two-pass no-write failure, real loader/receipt/Gate replay at
  both admission sites, tamper negatives, supported advancement, and
  Weekly/direct-primary regressions with no old PASS transfer. Receipt correctly
  defined as narrow Longform schema with explicit legacy-shape rejection,
  independent re-derivation of input and all outputs, and generating-State hash
  as historical provenance rather than a later-State equality requirement.
  Readback at applicable later stages with validated current authority (write
  entry restrictions not blindly imposed) and malformed-Longform no-fallback to
  DIRECT_PRIMARY are coherent. Cost correctly stated as substantial and
  unestimated (not zero/cheaper), net savings unknown, path budget provisional
  (new derivation module, two schemas, existing entrypoints/wrapper/Gate/stage/
  CLI threading as forwarding requires; fidelity/manuscript schema unchanged
  unless a demonstrated gap is separately selected).

## 4. Findings (severity + precise resolution; none blocks the contract direction)

- **F1 [Info] Pending-deletion antecedent.** Decision §2 “Its pending-Preview
  path” is factually the public `run_semantic_publication_v2_interactive.py:
  23-63` deletion before `_base.main()`, not base `:123` alone. Resolution: read
  “Its” as the public entry; no contract change. LF-1/2 ordering in §6.1/6.5
  already enforces refuse-before-delete.
- **F2 [Low] Package-ID/label token safety needs an LF-1 rule.** Decision §4
  treats raw package IDs used only for anchors/provenance as mechanical safe
  tokens, with displayed kicker effects in the reader input. Resolution: LF-1
  internal design must state the allowed `package_id` charset (Architecture-bound)
  plus `\label{pkg:…}` / `% package:…` / kicker-suffix construction and
  `tex_escape`/URL/token handling, refusing arbitrary executable text; do not
  assume mechanical-safe. This is deferred detail, not a current contradiction.
- **F3 [Low] “Proven nonreader change” needs its LF-2 proof reading.** Decision
  §4 permits reuse of pre-TeX judgment only for proven nonreader changes with
  unchanged reader content/citation identity and intact authority. Resolution:
  interpret “proven” strictly as LF-2 independent re-derivation of the reviewed
  input and all outputs with renewed mechanical receipt/Gate (per §6.3:
  refreshed hashes alone are not proof), while exact source/PDF/visual/Human
  byte rules still lapse. No prose waiver; variable provenance comments stay out
  of TeX (mechanical evidence), consistent with correction C4-A.
- **F4 [Info] Base-line citation scope.** Decision §4 cites base `:84-89`/`:191`
  wholesale for the descriptor row. Resolution: the `% Generated…` comment in
  `:85` stays mechanical evidence; only exact display values (including fixed
  title/date-prefix/cutoff words, with access/event/publication dates kept
  distinct) enter the IR. No omission or contradiction found.
- **F5 [Info] `meta.title` wording superseded.** Feasibility §1 loosely lists
  “meta title (authored)”; decision §4 explicitly requires no invented
  `meta.title` source and exact fixed-title display values. Resolution: decision
  wording governs; LF-1 must source the title as a fixed format label, not a
  profile field.

No concrete contradictory or unsafe contract found. No universal parser, no
opaque-bundle equivalence claim, no invented authority, no review-role fusion, no
retrospective/generic-Thematic overclaim, no Weekly coercion, no lifecycle
deletion reuse.

## 5. Limitations

- Source-only design review; no runtime, fixture, build, PDF, or corpus behavior
  observed. Deterministic-test and semantic/rendered acceptance claims in §§6-7
  are proposals for LF-1/LF-2, not executed evidence.
- Available fixed 409 DB only; unmaterialized historical blobs/data beyond it are
  explicit limits, not hydrated or substituted.
- `survey_drafting_citation_refs_v2.refs`, Evidence/Card/Matrix/Discovery, and
  provenance-resolver readings are interface/contract reads, not a constructed
  Thematic accepted fixture. An actually invalid/unconstructible fixture remains
  a concrete LF-1 BLOCKED stop per §§5/7.
- Genuine semantic/rendered acceptance (DM-006/013/018/020 dimensions, claim
  conditions, JA meaning, log→page/clipping/appendix coverage) stays distinct
  and open; saved Summary capture only, no unread-corpus adoption.

## 6. Bounded verdict

**DESIGN_BOUNDED_PASS** — the selected generated-Longform reader-input/
derivation direction, THEMATIC + LONGFORM_SPECIAL four-family-lineage-v1 scope,
reader-content table, accepted-source mapping limits, closure/operation order,
and LF-1 source-only gate with LF-2 integration boundary form a coherent,
fail-closed, review-preserving contract direction. Implementation details
intentionally deferred to the LF-1 internal source/schema/fixture proposal
(package-ID token rule, exact IR keys, date-kind enumeration, directive-authority
identification, receipt/closure threading) do not need to be fixed here. No code
acceptance, no canonical audit, no Human authority claim. Stop at Human Commit
Point; LF-1 proceeds only under its stated design-first, real-loader, blocker-
first terms.
