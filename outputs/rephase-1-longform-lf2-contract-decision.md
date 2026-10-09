# LF-2 — initial generated Longform integration contract

2026-10-09. Astra design selection after Human continuation at reconstruct **b11c2d0b28d49c0df560273a7f49f7e6739aee85**. This is a **design unit**, not implementation acceptance. Source is unchanged409 + exact LF-1 three-file overlay (runtime233e8655/schema7bae9d2a/testce687447). No candidate code/schema/test edits or fixture/test/build execution in this unit. Whole candidate NOT_READY, step4/B3 OPEN, canonical audit unstarted.

Read [LF-1 assessment](rephase-1-longform-lf1-assessment.md), [General first proposal](../notes/rephase-1-longform-lf2/design-proposal.md), its [mandatory correction](../notes/rephase-1-longform-lf2/design-correction.md), and [Astra feedback](../notes/rephase-1-longform-lf2/astra-design-feedback.md). The choices below govern conflicting proposal wording. First-proposal blockers and writer-only completion are not selected.

## 1. Selected boundary / authority

Select **one initial THEMATIC/LONGFORM_SPECIAL, THEMATIC_FOUR_FAMILY_LINEAGE_V1 generated route**, from reader-only first pass through independently replayable source receipt and generated Gate, both existing exact-manuscript admission sites, and healthy later readback. Call the implementation unit **LF-2I** (task label, not a new Profile enum). Receipt-only/source-writer V1 with Gate/admission deferred is rejected as an incomplete integration boundary. No line/path ceiling replaces the required guarantees; net lifecycle savings remain unmeasured.

The new explicit entry retains LF-1's **legacy directive presence refusal**, including dangling symlinks. It never executes or replaces `run_semantic_publication_v2_interactive.py` or its base writer. Their existing directive check and pending-delete behavior are not migrated or certified. Therefore absence of a bound legacy directive producer does not block this restricted new initial route; it still blocks **adopting a directive-bearing edition through it**. Required final summary is a selected format obligation, not a fabricated Human approval. Applicable approved-Architecture/Human instructions and substantive conflict decisions remain with their existing owners; file absence is not proof of instruction-freedom.

The missing reader-handler entry in legacy `survey_handlers_v2.py` is not a prerequisite repair. Source shows the direct agent-first route: `survey_stage_validation_v2.validate_stage`/CLI → `survey_agent_control_v2.build_stage_checkpoint` → `advance_with_checkpoint`; `survey_core_execution_bridge_v2._advance_stage:365–407` invokes that sequence. No executed witness is claimed here. New publisher generates inputs for that route; it does not dispatch the old `survey_orchestrator_v2` registry or transition State itself.

DIRECT_PRIMARY/PRIMARY_ONLY remains an explicit limited capability. A malformed generated target/receipt may not fall back to it. Preserved Weekly behavior/current closure is not silently generalized. Existing pre-TeX semantic, later semantic/editorial, visual, Architecture and Human Preview responsibilities remain distinct; no new reviewer or automatic semantic PASS.

## 2. Entry, artifacts and operation ordering

Proposed public CLI: `scripts/survey_longform_semantic_publication_v2.py` with `--repo-root`, `--state`, `--input`, optional `--semantic-review`, and `--materialize-surface-only`. No default call into the legacy writer. These are prospective interfaces, not commands available in the current candidate.

| Artifact | Selected path / responsibility |
|---|---|
| Complete reader input | `<source_root>/publication/v2/reader-surface-input-v2.json`; LF-1 schema/route/format; exact canonical FILE bytes |
| Pre-TeX review | default sibling `reader-surface-semantic-review-v2.json`, or explicit contained path; existing Reader-Surface semantic-review schema/loader |
| Immutable authoring archive | sibling `interactive-semantic-publication-input.json`; exact validated input-byte snapshot, separate from reader identity |
| Source outputs | `<survey_root>/main.tex`, `references.bib`, copied trusted `jgaisurvey.sty` |
| Source receipt | sibling `validated-source-manifest.json`; new strict `longform-publication-source-manifest-v2.schema.json`, route `LONGFORM_GENERATED_V1`; no legacy/Weekly shape fallback |
| Generated Gate | existing Gate artifact/producer, derivation `{route: LONGFORM_GENERATED_V1, scope: LONGFORM_MAIN_BIB_STYLE, receipt:{path,sha256}}` |

**Before any mkdir/output write**, contain/check inputs, validate exact DRAFT_COMPLETE/configured action, THEMATIC/LONGFORM_SPECIAL and directive refusal, load real accepted authority, derive/validate/scan the complete reader object and validate output ownership/path/inventory. No writer support for later lifecycle, pending Preview, changed-output regeneration or arbitrary/manual TeX/includes.

Pass1 writes only the canonical reader input. Existing same-byte input may be reused only after fresh successful derivation and **byte equality**, not merely parsed-object equality. Wrong bytes/alias/unsupported format refuses without overwrite. No review/receipt/Gate is generated by pass1.

Pass2 requires an already materialized exact reader input; absence refuses rather than silently doing pass1. Call `load_and_validate_reader_surface_semantic_review` with expected issue/Profile/path/SHA and `require_pass=True`. Invalid/missing/stale/non-PASS/VISUAL/legacy review refuses before all source/archive/receipt writes. Its on-disk record/digest/checks are necessary type/identity checks, not machine proof of real reviewer independence or semantic sufficiency.

Then derive all output bytes in memory, validate finite serializer closure/preflight, committed current-tool/contract identity, closed build-directory inventory and prospective receipt schema/digests. Refuse existing main/bib/style/archive/receipt and any aliases/undeclared inputs. Check exact accepted/authored/review/tool snapshots immediately before writes. Use exclusive owned-file creation, preserve original unrelated bytes, and verify output/snapshot consistency before installing a receipt as the final source-set record. Predictable failure must leave the source window untouched. Mid-write/close/drift failure must return failure and clearly retain/report owned partial output; retries refuse partial sets, no silent deletion/repair. No global CAS or crash-atomicity claim.

## 3. Same-object rendering and fidelity

Introduce pure `render_main(surface)` / `render_bibliography(surface)` in a narrow generated-source helper. Every semantic value must come from the reviewed object: title/display dates/prefixes, all cover/frontmatter/revision text, labels/kickers/table headers, note URLs, final summary, bibliography and citation placement/order. No post-review raw Draft/body/sidecar reread. No arbitrary TeX escape hatch. The current renderer is a **reference inventory**, not a drop-in pure serializer: its writer `_render_tex` imports/inputs and hardcoded labels cannot simply be reused unchanged.

Use the actual trusted style setters for displayed repository/build/labels/strapline/edition descriptor and explicitly set `contentsname` from reviewed `toc_title=目次`; preserve the existing layout contract. Serialize inert structural commands and finite safe tokens; escape prose/Bib fields by context and retain LF-1's explicit narrow URL subset. Code closure binds the literal style and actual helper bytes. Unsupported headings/characters that cannot be traced by the existing fidelity parser must refuse before writes or receive a separately justified local serializer solution — no general parser expansion.

Keep numbered package/cross-family/final-summary sections and current balanced narrative/full-width surfaces. Existing manuscript producer/fidelity validator remain the authority for accountability maps; do not autogenerate an editorial adequacy claim from section presence. A proposed synthetic fixture maps every exact `(package_id,must_cover_requirement)` to its extant numbered package section, plus exactly one `FINAL_SYNTHESIS` requirement to the final-summary section. Starred headings are not numbered authorities.

Later review records must still satisfy `ARCHITECTURE_CONTENT_FIDELITY`, `LONGFORM_TECHNICAL_DEPTH`, `FINAL_SYNTHESIS_QUALITY` (including actual highest-drafting-order package, exact final location and `reader-role:final-synthesis`), below-target density disposition when applicable, and `LONGFORM_MIXED_LAYOUT` evidence. This design identifies a type/identity fixture route, **not demonstrated constructibility or genuine fidelity**. If the real validators cannot accept it without bypass/invented authority, stop with the exact blocker.

## 4. Receipt, replay and Gate integration

New receipt has strict keys: `schema_version`, `issue_id`, `route`, `status=ESTABLISHED`, `production_state_basis{path,historical_sha256,lifecycle_state}`, `accepted_refs`, exactly two named `authored_refs` (`publication-semantic-input`, `drafting-authored-archive`), `reviewed_reader_input{path,sha256}`, `semantic_review{path,sha256}`, `current_tools{repository_commit_sha,contract,closure}`, `outputs{primary,bibliography,style}` and `receipt_sha256`. Bind the approved format through exact reader bytes/schema (no extra implicit selector). Self-digest uses canonical object hash excluding itself; artifact refs always hash exact FILE bytes. Review object digest is distinct from its file SHA; reader bytes and output bytes are independently compared.

Proposed source-helper APIs: `render_main(surface)`, `render_bibliography(surface)`, `validate_survey_build_directory(root,relative_path)`, `current_closure(root)`, `verify_tool_basis(root,receipt_tools)`, `build_receipt(root,context,planned_or_written_refs)` and `validate_receipt(root,receipt_path,state_path=None)`. Final signature details may be refined in the implementation task without changing these guarantees.

**Public Longform receipt replay itself reloads and validates the persisted semantic review**, exact expected surface/path/Profile, in addition to envelope/self-digest, live accepted/authored refs, tool/contract/ancestry, independent context derivation, exact reader FILE bytes, canonical output paths/build inventory and deterministic main/bib/style bytes. General correction's suggestion to preserve Weekly's split (review loaded only by outer Gate) is not selected. Gate also reloads the review independently and binds the same file SHA; this preserves existing admission guarantees without treating a bare receipt as sufficient review authority.

`_derivation_for_manuscript` receives a Longform branch for the structured target; existing direct-primary branch remains PRIMARY_ONLY. Require canonical reader/receipt paths, matching issue/Profile/route, exact three output bindings to the selected manuscript, and exactly BIBLIOGRAPHY+STYLE support. Validate new Gate schema route/scope. Unexpected/malformed structured target rejects explicitly, never a legacy fallback.

Add a Longform branch to `scan_structured_reader_surface`; the existing Weekly/fallback branches miss nested LF-1 fields. Walk the defined reader schema's actual display strings/citation representations (including bibliography and all visible constants); do not scan internal identifiers as prose or dump whole authority objects. Gate create/validate/CLI must use the same strict route and persisted-review loader. Both stage sites already forward exact expected manuscript + current State, as does publication revalidation; change those callers only if an actual threading gap is demonstrated, not by default.

## 5. Loader/readback and tool closure

LF-1 loader cannot remain read-only-in-the-diff if later readback is added. Refactor its authority loading behind two explicit operations: default `load_derivation(...)` retains exact initial DRAFT_COMPLETE write eligibility; new `load_derivation_for_readback(...)` is read-only and permits an explicit tested allowlist of healthy current states **DRAFT_COMPLETE, VALIDATED_DRAFT, RELEASE_CANDIDATE, FROZEN, RELEASED**. Both retain validated Profile/accepted checkpoints/Architecture/Draft/source attribution/directive refusal. Readback never writes or calls a publisher. Reject unrecognized/terminal-invalid states, mismatched live authority and unsupported pending/revalidation context; do not manufacture a former-State dictionary.

Generation-State SHA remains historical provenance; legitimate advancement does not require equality with that old file hash. Current State validation is still mandatory. An existing valid revalidation pointer must not be rejected merely for existing; the source/review/authority actually selected by current validation rules governs. **Changed-Core pending establishment and mechanical renewal are not implemented by this unit.** When the normal State validator or current-tool/receipt checks reject such a context, preserve that failure instead of adding a Weekly pending-basis bypass. Inspect actual `_PendingPublicationBasis` call paths during implementation and document the precise unsupported operation; no broad claim of all publication revalidation.

Proposed explicit Longform closure: LF-1 derivation, new generated-source helper and public entry, actually used pure-render/preflight helpers, `survey_drafting_citation_refs_v2.py`, `survey_bibliography_access_provenance_v2.py`, `render_article_draft_tex.py`, reader-input and new receipt schemas, shared Gate/runtime/schema, semantic-review schema and trusted `templates/survey/jgaisurvey.sty`. Also enforce existing repository implementation-control roots and configured contract-file equality/ancestry so unlisted shared helper changes are not exempt. Declare/register new receipt/reader contracts where current `contract_identity` requires; no copied Weekly closing-synthesis/metadata semantics or silent `CURRENT_CLOSURE` edit. Exact closure/path list is fixed before the first verification run and reviewed against actual imports/call graph.

The working composite is uncommitted: actual publisher/receipt tool guards must refuse it as a committed implementation basis. Testing may materialize the exact selected bytes in fresh independent **synthetic committed Git fixtures**, under the existing isolated-test authorization. Do not weaken production dirty/untracked/current-tool checks, label fixture commits shipping candidates, or infer candidate-commit permission from this task. Any later candidate commit needs explicit authorization and fresh identity-bound acceptance.

## 6. Concrete path budget / verification boundary

| Path | Expected action |
|---|---|
| `scripts/survey_longform_semantic_publication_v2.py` | A — thin public two-pass writer/CLI |
| `scripts/survey_longform_generated_v2.py` | A — pure serialization, closed inventory, receipt and independent replay |
| `schemas/longform-publication-source-manifest-v2.schema.json` | A — strict receipt |
| `scripts/survey_longform_derivation_v2.py` | M — authority-load/readback split; retain default LF-1 boundary |
| `scripts/survey_reader_surface_gate_v2.py` | M — complete Longform scan + receipt route/admission |
| `schemas/reader-surface-gate-v2.schema.json` | M — explicit generated Longform arm |
| `config/survey-production-v2.json` | M only for necessary contract-file registration; no dispatcher/lifecycle policy repair |
| `tests/test_survey_longform_publication_integration_v2.py` | A — real accepted-chain two-pass/replay/CLI/admission/lifecycle/no-write/tamper proof |
| Existing LF-1 / Gate / CLI / revalidation tests | M only for demonstrated contract changes; run affected selected controls |
| Active legacy renderer/base writer, fidelity/manuscript schemas, reader-publication builder, stage/controller/bridge | Read/reuse existing APIs; any source change needs a concrete gap and Astra decision |

This table corrects General's read-only label on LF-1 and omission of a separate Gate-schema path. Reusing an unchanged renderer with unreviewed hardcodes is not permitted; if actual reuse needs local helper parameterization, revise the budget before editing it. A new generated helper is the one serializer/replay owner for the explicit new route, not a second uncoordinated writer for the same operation. Output existence/route/directive rules prevent silent legacy takeover.

Minimum future evidence on the exact final composite:

1. Real accepted Thematic chain → pass1 reader-only → real persisted review loader → pass2 exact source/archive/receipt. Synthetic review/PDF/Human rows are explicitly type/identity fixtures.
2. Missing/stale/wrong-path/wrong-same-issue/non-PASS/legacy review and invalid directive/lifecycle/aliases: immediate before/after owned-tree no-write around the appropriate pass, including no deletion by legacy wrapper. Pre-existing partial outputs refuse unchanged.
3. Independent receipt replay and generated Gate creation/revalidation; altered reader/main/bib/style/closure/accepted source rejected even with fresh self-hashes. Actual strict committed-tool guard refuses the uncommitted source basis.
4. Current manuscript/quality/later reviews/Candidate via existing validators and real DRAFT_COMPLETE→VALIDATED_DRAFT→RELEASE_CANDIDATE admissions, exact wrong-same-issue manuscript negatives at both sites. Healthy FROZEN/RELEASED readback through valid synthetic authorities, no live Release/Actions. If a later-state fixture is unavailable, return the precise unsupported scope before claiming completion.
5. Same reader bytes under allowed nonreader authoring changes with renewed mechanical bindings, without stale PDF/visual/Human waiver or a claimed operational regeneration owner. Finite heading/token/URL escaping, complete nested scanner coverage and existing fidelity/depth/layout obligations.
6. Affected Weekly/direct-primary positives and schema/receipt route negatives, plus relevant LF-1 default-loader checks because that code changes. No automatic full old suite; tests chosen from actual changed dependency paths.

Persist exact source/base/overlay hashes, actual runtime/argv/cwd/env, all failures/exits and asserting pre/post guards with exclusive logs. Never overwrite earlier evidence or report a print-only/post-nonasserting runner as fail-closed. Artifact/source-only fixtures do not prove TeX/PDF build transfer, actual semantic/visual review, all-profile viability or lifecycle cost savings.

## 7. Commit Point / next action

Obtain scoped author-independent **design** review of this selected contract and resolve concrete findings. On completion, stop at the design Human Commit Point. Next General task is LF-2I implementation on the preserved409+LF1 independent copy, after checking exact identity and incorporating the design-review conditions; no candidate commit, LF-1 rerun or code execution is implied by the design verdict. Existing directive-bearing editions and pending-regeneration/Core-change renewal remain separately unresolved.
