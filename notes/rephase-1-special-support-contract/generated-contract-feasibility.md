# Generated-Longform IR feasibility — THEMATIC + LONGFORM_INITIAL only (no code/tests)

Fixed 409 at `/tmp/opencode/jgas-dm004-impl-20261004T234416Z` (HEAD/tree clean/inert/shallow verified).
One coherent generated IR, not bundle-then-adapter. DIRECT_PRIMARY stays primary-only.
Retrospective generated route NOT proven; Retrospective keeps direct-primary only. No entry/old-file/Git/runtime/network/agents work. Prior reports preserved.

## 1. Emitted field -> authority -> IR member (actual 409)

Producer today: `run_semantic_publication_v2_interactive_base.py` (blob 4aa20a4b) `_validate_input:106-116`
+ `_render_tex:81-104` + `_bib_text:35-53`; revision contract
`survey_longform_publication_v2_base.py` (blob d4f53f63) `validate_revision:75-218`;
base-renderer `render_package:225-286` / `render_cross_family:289-306` / `preflight_tex:309-335`.
Style interface `templates/survey/jgaisurvey.sty:60-100` (`\surveysetup/\surveycoverstory/
\surveyeditiondescriptor/\surveyrepository/\surveybuildvalue/\surveycoverlabels/\surveystrapline`,
cover/table emission :110-138). Weekly analog for setter-passing: `survey_weekly_derivation_v2.py:400-442`
(`\surveyrepository/\surveybuildvalue/\surveycoverlabels/\surveystrapline/\surveyeditiondescriptor` from IR).

| Emitted (order fixed :84-104) | Current field/helper | Authority | IR member / mechanical-only |
|---|---|---|---|
| `\surveysetup{issue,title,date,cutoff}` | `issue_id`, `meta title`(authored), `as_of` from `profile.research_scope.temporal_policy.as_of` (:191) + window | profile-accepted as_of; title/authored-context | IR: `issue_id/title/display_date/window_boundary`; raw profile JSON out |
| cover headline/deck/anchors `\surveycoverstory` | `data.cover{headline,deck,anchors}` (:108-111) | publication-authored (new prose) | IR members verbatim + order |
| frontmatter heading/lede/scope_notes | `data.frontmatter` (:112-113), rendered :91-95 | publication-authored | IR members verbatim |
| edition descriptor `Thematic Longform Special` | hardcoded :88 | fixed format constant | IR: fixed label (see FourFamily decision) |
| per-package headline/deck/kicker `THEMATIC LINEAGE o/n` | `result.headline/deck` checked vs semantic archive (:145-149); `_kicker` (:56) | accepted Draft result text; kicker template mechanical | IR: `headline/deck/section_label` from accepted result; kicker derived, not authored |
| Draft body blocks replayed | `result.blocks` vs `spec.blocks` text equality (:147-149); rendered :245-255 with `source_spec.discovery_ids` cites | accepted Draft/Synthesis archive | IR: block refs `{block_id,text,attribution,citations}` OR explicit "not in IR, replayed from accepted refs" — Astra must pick; do not silently duplicate |
| theme_at_a_glance/narrative/timeline/synthesis/claim_boundary | `longform_revision.packages.*` validated vs per-package allowlist (:92-187) | publication-authored, Evidence-constrained | IR members verbatim + per-row `discovery_ids` |
| technical notes + chronology/points/limitation/primary_url | `technical_notes[]{title,discovery_id,chronology,technical_points,limitation,primary_url}`; `primary_url==canonical_url` (:165-167); exact-once coverage (:181-183) | publication-authored, accepted-entity-bound | IR members verbatim; `primary_url` must equal accepted canonical URL |
| cross-family heading/paras + comparison rows | `cross{heading,paragraphs,comparison_rows}` (:190-208) | publication-authored, `selected_union`-constrained | IR members verbatim |
| `\cite` placement/order | `_cite` (:221-222) + `bib_key_by_did sp001+did` (:192) | placement authored; membership accepted-bound | IR: per-block ordered `citations[]`; bib order = `cited[]` order (:159-161) |
| bib title/author/url/urldate | `_bib_text` (:35-53) from `records[did]` entity + `urldate` | accepted Evidence (see §2) | IR `bibliography[]:{discovery_id,key,title,author,url,urldate}` |
| style-visible labels/values | setters above; Weekly passes `visible_text` (:410-414) | fixed defaults + issue values | IR `visible_text`-analog (fixed labels + repository/build/edition/strapline values) |
| output order main/bib/style | `survey_root/main.tex + references.bib + jgaisurvey.sty` (:187-194) | derivation outputs | IR order fixed; tool/style/control hashes + receipt provenance mechanical-only |
| EXCLUDED from semantic identity | `review_reference` free text (:85), runner/recorded-at, `% package:...draft-result-sha` (:98), preflight counts, manifest/receipt SHAs, tool closure | provenance/mechanical | Out of IR; variable provenance comments move to mechanical evidence |

## 2. FourFamily bounded format decision

Hardcodes define one topic shape: kicker `THEMATIC LINEAGE` (:56), base `render_cross_family` 4 columns
(`glm/qwen/deepseek/kimi`, `required_row` :198; header :299; wrapper header :138), `sp001` key prefix (:192).
(Note: base-module `render_cross_family:289-306` uses sidewaysfigure; wrapper override
`survey_longform_publication_v2.py:122-147` uses normal full-width — selected shape must name which serializer
is canonical.) Decision for Astra: either (F1) retain explicit narrow format v1 (fixed 4 lineage columns +
fixed kicker/key scheme; other Thematic topics unsupported until mapped), or (F2) small parameterization of
display labels/column headers only within the fixed 4-column/row-minimum shape (column keys stay
`glm/qwen/deepseek/kimi`, count fixed, `len(comparison)>=3` :194-195). No generic column/topic framework.
Do not claim all-Thematic support while F1/F2 hardcodes stand.

## 3. Accepted-card mapping (blocker-first; no new authority)

- Current longform reads sidecar `acceptance.parent/interactive-evidence.json` rows (:156) with
  `entity{canonical_name,organization,canonical_url}`, `materiality/status/sources/source_accessed_at/urldate`,
  `source_bindings` fallback (:170-178). A sidecar beside acceptance is not authority.
- Replace with: matrix `candidate-matrix-v2.schema.json:12-22` (`evidence_acceptance_sha256` binding) + rows
  (`evidence_task_id/discovery_ids/evidence_sha256/title/evidence_status/materiality` :29-40); card
  `evidence-v2-card.schema.json` (`entities[]{canonical_name/organization/canonical_url}` :24-38,
  `artifact{canonical_name/canonical_url}` :40-50, `status` :23, `sources[]{source_id/url/source_class/title/
  published_at/accessed_at/role}` :75-92); B helpers `_strict_evidence_sources:182-203` (card path+sha,
  single-card DID uniqueness) + `_records_from_authorities:206-258` (matrix↔acceptance↔ledger↔discovery agreement,
  `resolve_source_access_provenance` fail-closed on ambiguity/missing date).
- Shareable iff profile-neutral: `parse_access_date:17-43`, `resolve_source_access_provenance:45-86`,
  `load_evidence_sources:144` only. Do NOT import Weekly closing/synthesis/authored gates
  (`_closing_summary:271-283`, `build_reader_input:286-307` force `profile_synthesis.current_interpretation`).
- Concrete constraints to encode (fail-closed): DID single-card membership (B :200-201/:224-227);
  `evidence_status/materiality` matrix↔acceptance↔ledger agreement (B :239-242); canonical URL non-null and
  URL-matched source with valid `accessed_at` else refuse (card allows `canonical_url:null`; provenance
  :66-86 refuses heuristics); `organization:null` needs explicit `Unknown`-fallback policy (do not silently copy
  B's Weekly fallback without Astra approval); multi-entity cards need explicit DID→entity selection rule;
  citation membership = Architecture-assigned package allowlist (base :95-111) — outside IDs refuse.
- Concrete blocker stop: if Thematic Evidence needs source classes outside the accepted map (DM-016) or
  obligations outside builder/validator agreement (DM-017), the IR has no feasible accepted source — return
  BLOCKED with the missing class/field, do not invent a compat authority here.

## 4. Path/API budget (surface-only -> review -> same-IR generation -> replay)

- Source fix required (not optional): base initial guard `next_action stage:semantic-publication-validation`
  (:122) contradicts configured DRAFT_COMPLETE handler `stage:reader-publication-validation`
  (`config/survey-production-v2.json:330-333`). Fix the literal/source before any LONGFORM_INITIAL claim;
  persisted pre-TeX review must precede TeX/Bib/style writes (base :187-205 currently writes with preflight only).
- New (real cost): `schemas/longform-reader-input-v2` (IR) + `schemas/longform-source-manifest-v2` (receipt:
  mirror `build_receipt:634-666` + closure check pattern :600-631 with longform CURRENT_CLOSURE);
  narrow derivation module (surface-only builder + `render_main/render_bibliography/validate_closure` analogs
  reusing `tex_escape`, B setter pattern, restricted `\usepackage/\addbibresource` + no `\input/\include`);
  persisted review via existing `reader-surface-semantic-review` + `build_reader_surface_gate:638-705`;
  same-IR materializer by refactoring base `_render_tex/_bib_text`/style-copy to consume the IR (adapt, do not
  add a second writer); manuscript via existing `build_manuscript_manifest:297-355`; Gate new `route/scope` +
  `validate_reader_surface_gate:1670-1715` readback + CLI `validate-gate/scan-manuscript` + stage threading
  (`survey_stage_validation_v2.py:470-573`). Fidelity untouched unless included-file blocks selected.
  Preserve wrapper pending-deletion path untouched (no execution/certification); no auto Special-R1 extension.

## 5. Acceptance + first milestone

- Deterministic: surface-only valid/invalid; persisted PASS required before writes; same-IR regeneration
  byte-equal main/bib/style; manuscript/Gate admit exact IR route; mutations (changed support value, fresh
  rehash w/o review, wrong-manifest, bib/urldate drift, content-style vs layout-only, dynamic/undeclared input
  refusal, mechanical-only control) behave per matrix. Semantic/rendered (reviewer + rendered proof, never
  hash-only): claim-to-source fidelity, date/role/strength preservation, JA meaning, Overfull/clipping QA.
- Milestone 1: IR schema + surface-only builder + accepted-mapping proof on synthetic fixtures only (no PDF /
  production claim). If §3 mapping infeasible, scope the contract BLOCKED here, not another projection.
