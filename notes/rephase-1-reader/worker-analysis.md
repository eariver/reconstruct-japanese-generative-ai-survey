# B3 reader coverage/derivation — bounded Worker analysis

Date: 2026-09-21 JST  
Role: Worker, not independent Auditor  
Fixed candidate inspected read-only: `bf32edf98ba8f605169d7188bbc764de74ee4f6e` (`/tmp/jgas-rephase-freeze-b1b2`)  
Fixed production ancestor: `774dd39a951c9ac3818e83dfffd4c7666efb0a20`

This analysis maps the smallest credible reader contract and regression boundary. It does not change the candidate, production, schemas, or tests, and it does not establish publication quality or all-profile viability.

## Findings

### 1. Current hashes authenticate two separate things, not their relationship

The persisted semantic review authenticates exactly its `reviewed_surface.path` and bytes (`scripts/survey_reader_surface_gate_v2.py:895-1056`). Gate evaluation separately scans the Reader Manuscript primary source (`:1160-1174`) and optionally scans the reviewed structured surface (`:1253-1279`). The semantic authority check only compares the review hash to the current reviewed file (`:1281-1304`). The independent gate validator rechecks all recorded files and the semantic review (`:1499-1560`), but it never proves that the primary source was produced from the reviewed JSON.

The downstream stage validator supplies only expected issue/profile when validating the Gate (`scripts/survey_stage_validation_v2.py:463-517`, `:520-567`). It does not supply the stage-selected Reader Manuscript path/hash. A same-issue/profile Gate can therefore be internally hash-consistent without being tied to the exact manuscript selected by the current stage. The saved Phase-5 counterexample demonstrates this exact separation: changing the TeX and refreshing the manifest while leaving the reviewed JSON unchanged still produced and revalidated a passing Gate (`notes/phase-5-upstream-reconciliation/probe.py:90-131`; `probe-results.json:reader_binding`).

A new field containing a caller-asserted primary-source hash would only move this assertion into another signed object. The repair needs an independently recomputed derivation or exact identity with the reviewed primary source.

### 2. Weekly's reviewed JSON is not the renderer's complete reader input

`_render_tex` consumes issue/date/window metadata, cover, frontmatter, summary, Architecture plan, Draft spec/result blocks, section labels, and citation mapping (`scripts/survey_weekly_semantic_publication_v2.py:286-361`). The current projection supplies only cover headline/deck, closing synthesis, final-summary paragraphs, and spec package headline/deck/blocks (`:499-526`; builder at `scripts/survey_reader_surface_gate_v2.py:841-892`). It omits reader-visible or output-affecting inputs:

| Emitted/output-affecting input | Renderer | Current reviewed projection |
|---|---|---|
| cover anchors | `survey_weekly_semantic_publication_v2.py:303-305` | absent |
| frontmatter heading, lede, scope notes | `:309-316` | absent |
| final-summary heading | `:345-353` | absent |
| Architecture section label | `:321-326` | absent |
| result-only `CLAIM_BOUNDARY` text | `:329-343` | absent; projection uses spec blocks at `:503-514` |
| display date and window boundary | `:303` | absent |
| citation keys / placement inputs | `:327-343`, `:352-353` | absent |

The non-boundary result prose is checked against the spec before projection (`:450-475`), so that subset has a useful correspondence. Result-only claim-boundary blocks have no such projected representation. The separate pre-TeX lexical list also omits cover anchors and all frontmatter fields (`:528-544`).

The input schema reflects the incomplete shape (`schemas/reader-surface-input-v2.schema.json:7-51`). Gate evaluation does not validate a selected structured surface against that schema: it loads any JSON object with `packages`, scans known fields, and silently ignores every exception (`scripts/survey_reader_surface_gate_v2.py:1264-1279`). One upstream revalidation fixture writes `final_summary` instead of schema-required `final_summary_paragraphs` and still builds the Gate (`tests/test_survey_publication_revalidation_v2.py:367-415`). A repaired derived-IR route must schema-validate the exact reviewed object and fail closed; the current best-effort scan is not a derivation validator.

The concurrent bounded root probe independently expands the mutation set to ten output-affecting omissions and shows a full render-input prototype rejecting stale output (`notes/rephase-1-reader/probe-results.json`). It also shows why that prototype should not be shipped: an internal result annotation changes a provenance comment and review digest even though reader prose is unchanged. Reader judgment should bind a reader-oriented IR, while build/provenance identity is checked separately.

### 3. Caller/profile topology is not one uniform path

**Weekly.** The Weekly CLI already has the right two-step control shape: `--materialize-surface-only` writes the JSON and stops (`scripts/survey_weekly_semantic_publication_v2.py:378-389`, `:560-567`); a normal run requires a persisted PASS review of that exact JSON before writing TeX (`:569-618`). This is the narrowest place to replace the partial projection with a complete reader IR and make rendering consume that IR.

**THEMATIC / LONGFORM_SPECIAL.** `run_semantic_publication_v2_interactive_base.py` renders TeX directly from publication input, Draft inputs, and normalized longform revision (`:81-104`, `:118-206`). It has no surface-only mode, no `--semantic-review`, and no structured-surface builder. The output includes cover/frontmatter/summary plus extensive longform revision prose rendered by `survey_longform_publication_v2.py:43-147`. Weekly's schema/builder cannot establish coverage for this path.

**RETROSPECTIVE_PERIOD.** Core permits `RETROSPECTIVE_PERIOD/LONGFORM_SPECIAL` (`scripts/survey_production_v2.py:295`; config at `config/survey-production-v2.json:131-153`). The longform publisher checks only `publication_profile == LONGFORM_SPECIAL` (`run_semantic_publication_v2_interactive_base.py:129-131`), while its labels and revision shape are explicitly thematic (`:55-79`; `survey_longform_publication_v2_base.py:75-218`). I found no explicit Retrospective semantic-publication caller or profile-specific renderer regression. Treating a Thematic positive as Retrospective coverage would be unsupported.

**Manual/direct-source route.** The semantic-review schema permits any repository-local reviewed surface, and its loader can validate the primary TeX itself by exact path/hash (`scripts/survey_reader_surface_gate_v2.py:1003-1022`). This can be a legitimate compatibility mode only if the Gate requires `reviewed_surface == manuscript.primary_source`. Current Gate code does not require that equality. `survey_reader_publication_v2.build_reader_surface_gate` is a library function rather than a CLI and currently forwards the review without selecting a derivation mode (`:638-703`).

This direct-primary capability is evident from the generic file resolver/hash checks, but I found no dedicated test that reviews `main.tex` through the new Reader-Surface review schema. Existing helpers overwhelmingly review `reader-surface-input-v2.json` (`tests/test_survey_reader_surface_gate_v2.py:237-290`). A direct-route positive and wrong-file negative are therefore required before treating it as supported behavior.

Direct primary identity also does not cover every supporting reader surface. The Gate lexically scans bibliography and supporting TeX and records their hashes (`scripts/survey_reader_surface_gate_v2.py:1176-1209`), while the semantic review schema names exactly one `reviewed_surface` (`schemas/reader-surface-semantic-review-v2.schema.json:25-33`). Reviewing `main.tex` directly would establish semantic correspondence for the primary only; bibliography/source-note semantic coverage remains a separate, currently unspecified boundary. This does not invalidate a primary-only B3 repair, but it prevents claiming whole reader-surface semantic closure.

There is also an existing exact-source/PDF `SEMANTIC_EDITORIAL` Publication Review (`survey_reader_publication_v2.py:458-540`, validation at `:544-635`). Requiring another direct-TeX Reader-Surface review would duplicate judgment unless the review responsibilities are deliberately consolidated. The new Reader-Surface loader explicitly rejects the older review record (`survey_reader_surface_gate_v2.py:928-935`), so reuse is an authority/schema decision, not a safe incidental adapter change.

### 4. Audit prose is adjacent scope, not part of reader derivation

Both Gate evaluation and manifest validation lexically scan `architecture_coverage[].detail` (`scripts/survey_reader_surface_gate_v2.py:1210-1232`, `:1615-1627`). That field is an accountability explanation in the Reader Manuscript schema, not emitted by either renderer (`schemas/reader-manuscript-v2.schema.json:48-73`). It should remain structurally and substantively validated by the existing manuscript/fidelity/review contracts, but it should not be treated as reader-facing text. Removing it from reader lexical scope is the R3 companion change; it does not help prove JSON-to-primary derivation.

## Minimum credible contract boundary

The smallest sound design has two explicit routes selected from verified artifacts, not a caller-provided boolean.

1. **Direct primary-source route.** Accept when the persisted semantic review's exact `reviewed_surface.path/sha256` equals the exact Reader Manuscript `primary_source`. This route needs no JSON derivation claim. It is suitable for bounded manual compatibility, but should not be imposed as a second review where a profile already performs equivalent exact-source semantic review without first deciding authority consolidation.
2. **Derived reader-IR route.** Accept only a schema-valid, profile-specific canonical reader IR. A trusted adapter recomputes that IR from the current authoritative renderer inputs, compares object equality with the reviewed IR, renders with the production renderer, and compares the resulting exact primary bytes with the Reader Manuscript primary source. The Gate must not trust an IR-supplied output hash as proof.

The reader IR should contain reader-visible semantic values and stable locators, not full upstream result objects or internal annotations. For Weekly, the minimum shape covers:

- identity and visible issue metadata (issue/profile, display date, window label);
- complete cover and frontmatter;
- ordered package heading/deck/section label and every emitted prose/claim-boundary block with stable block kind/id;
- complete final-summary heading and paragraphs;
- the reader-visible citation/source-note representation or an explicit separately validated supporting-surface boundary.

Mechanical build inputs belong in a separate derivation/provenance binding: renderer/contract identity, upstream authority refs, citation map, and exact primary path/hash. The validator must recompute this binding and the output. This separation lets a non-reader annotation change invalidate/rebuild the derivation evidence without forcing a fresh semantic judgment when the reader IR is unchanged.

The Gate-to-stage connection should also become explicit. `validate_reader_surface_gate` should receive the exact `manuscript_path` selected by stage validation (or validate an equivalent schema-bound Reader Manuscript artifact reference), require one exact MANUSCRIPT_MANIFEST surface, load it, and require the Gate's PRIMARY_SOURCE to equal that manifest's primary source. Issue/profile matching alone is insufficient.

For Weekly, the existing two-pass CLI can produce/review the IR and then render from that same validated object. For LONGFORM_SPECIAL, a caller decision is still required:

- add a matching surface-only/IR consumer path to the longform publisher for both THEMATIC and RETROSPECTIVE_PERIOD; or
- explicitly use the direct-primary route and decide whether/how its judgment can reuse the existing exact-source semantic Publication Review.

The first route is structurally consistent and avoids a second semantic judgment, but is a larger cross-profile change. The second is a smaller correspondence repair but can preserve or add duplicated review work. Because the Retrospective caller/render contract is not established in the fixed candidate, a bounded contract/design prototype should precede candidate implementation. A Weekly-only implementation must not be described as closing B3 for the whole candidate.

## Options and tradeoffs

### Option A — reader-oriented IR plus trusted profile adapters (recommended design direction)

- Strongest early-review correspondence without reviewing TeX twice.
- Preserves persisted semantic-review authority and its current drift checks.
- Separates reader judgment from build/provenance churn.
- Requires a Weekly adapter/refactor and a real choice/implementation for LONGFORM_SPECIAL; Retrospective needs its own positive evidence.

### Option B — require direct primary-source review for every profile

- Very small and mechanically strong correspondence check.
- Loses Weekly's intended pre-TeX semantic boundary and duplicates the existing exact-source semantic Publication Review unless those authorities are consolidated.
- Consolidation would change review check families and reverse the current explicit legacy-review rejection; that is broader than a local B3 hash fix.

### Option C — full renderer-input envelope plus renderer hash

- Easy to re-render and compare exactly.
- Overbinds semantic review to internal metadata and provenance comments; root's probe demonstrates needless digest churn with unchanged reader prose.
- Useful only as a design witness, not a production contract.

### Option D — add primary/manuscript hashes to the current Gate

- Smallest diff.
- Unsound by itself: the producer can assert mutually consistent reviewed/input/output hashes without proving transformation. It does not close the preserved counterexample.

## Smallest meaningful regression scope after the contract decision

1. **Weekly IR coverage:** mutate each omitted field above and prove both IR and emitted primary change; retain covered controls. Include result-only claim-boundary text and section labels.
2. **Trusted derivation:** matching reviewed IR/current primary passes; changing primary and refreshing manifest/Gate digests fails; changing/dropping an IR field with fresh object hashes fails; changing renderer/build inputs requires recomputed derivation evidence. Do not use a caller-supplied expected hash as the oracle.
3. **Reader/build separation:** a non-reader internal annotation leaves the reader IR unchanged but changes/rebuilds provenance binding as applicable; semantic review remains reusable only if reader bytes/IR are unchanged.
4. **Exact manuscript admission:** a Gate for another same-issue/profile manuscript fails at both DRAFT_COMPLETE and inherited VALIDATED_DRAFT validation. The reviewed-surface direct route passes only for exact primary path/hash.
5. **Schema fail-close:** malformed or wrong-profile structured JSON, including the current `final_summary` fixture shape, is rejected rather than silently skipped.
6. **R3 scope:** internal wording in `architecture_coverage.detail` no longer blocks reader lint; the same wording in actual IR/primary prose still blocks.
7. **Caller positives:** one real Weekly two-pass function/CLI chain; one THEMATIC LONGFORM_SPECIAL route; one RETROSPECTIVE_PERIOD route or an explicit unsupported/fail-closed result; one manual direct-primary route if retained.
8. **Targeted existing regressions:** the relevant cases in `tests/test_survey_reader_surface_gate_v2.py`, `tests/test_survey_semantic_publication_v2.py`, `tests/test_survey_publication_revalidation_v2.py`, and `tests/test_survey_human_gate_revalidation_revision_v2.py`, plus stage-boundary tests that consume `reader-surface-gate`. There is no basis to rerun full CI before this contract is chosen.

## Missing facts before implementation

- The canonical Retrospective semantic-publication caller and actual reader-source construction path are not identified in the fixed tree.
- It is undecided whether bibliography/source-note prose belongs inside semantic reader IR or remains a separately exact, lexically scanned supporting surface.
- It is undecided whether the existing exact-source Publication Review can carry `READER_PIPELINE_INDEPENDENCE` and replace a separate direct-source Reader-Surface judgment. That requires explicit authority/check-family review, not inference from overlapping names.
- No actual edition, semantic reviewer, Human Gate, full stage chain, Windows path, or Special/Retrospective end-to-end run was exercised here.

Accordingly, the next concrete unit should be a bounded B3 contract decision and profile-caller prototype, followed by a candidate only after Weekly and LONGFORM_SPECIAL routes are both specified. This Worker analysis is not a fresh seven-point audit or adoption recommendation.
