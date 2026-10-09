# LF-2 design correction (supersedes V1 boundary; no code)

2026-10-09. Preserves `design-proposal.md` + preparation packet unchanged.
Source = DST `/tmp/opencode/jgas-lf2-design-20261009T113013Z` bytes (409 +
LF-1 overlay). OBSERVED = read from DST; PROPOSE = new behavior. No
implementation, tests, fixtures, commits, or network in this call.

## 1. Directive disposition (narrows proposal §1 blocker A)

Retain legacy check (`run_..._base.py:133-135`) and LF-1 lexists refusal
(`derivation:988-993`); never import or execute the legacy writer. A NEW
explicit directive-absent initial entry that refuses that input needs NO
blanket Human bind-file/migrate/defer decision: it preserves the
already-selected format obligation (base `:114-116`, render `:101-103`, LF-1
schema `final_summary` + `build:655-666`) and existing
approved-Architecture/Human reading duties without claiming the sidecar
accepted. Absence of the file still proves no universal instruction-freedom;
substantive conflict stays with existing owners. Blocker A now applies ONLY to
adopting an existing directive-bearing edition. No D1/D2/D3, no new role, no
free-text `review_reference` authority. No contradictory bound obligation
observed; none fabricated.

## 2. Caller (narrows proposal §2 blocker B)

The missing `stage:reader-publication-validation` registry entry
(`survey_handlers_v2.py:452-479`) is NOT an LF-2 blocker and gets no repair.
The actual selected route is the agent-first bridge, OBSERVED:
`survey_stage_validation_v2.validate_stage:601-647` (direct validation, CLI
`:662-684`), `survey_agent_control_v2.build_stage_checkpoint:1267-1329` /
`advance_with_checkpoint:1332-1390`, called directly by
`survey_core_execution_bridge_v2._advance_stage:365-407` (validate → reviews →
checkpoint → advance). Registry `execute_action:521`/`load_handler_module:889`
is the legacy orchestrator route; nothing here claims an executed route from
static reading. PROPOSE public
`scripts/survey_longform_semantic_publication_v2.py`, flags
`--repo-root/--state/--input/--semantic-review/--materialize-surface-only`
(mirror `survey_weekly_semantic_publication_v2.py:54-61`). It refuses
non-DRAFT_COMPLETE, non-THEMATIC/LONGFORM_SPECIAL, present-directive, or
malformed route BEFORE any mkdir/unlink/write, never imports
`run_semantic_publication_v2_interactive._prepare_revision` (8-file delete
`:46-55`). Reader-file create-only window is separate from the source-output
window (§6). DIRECT_PRIMARY stays PRIMARY_ONLY (`surface_gate:1082-1085`).

## 3. One INITIAL route (rejects proposal V1)

V1 (main/bib/style+receipt at DRAFT_COMPLETE, Gate/admission/readback
deferred) is rejected: `_derivation_for_manuscript:1080-1118` refuses
structured Longform and Gate schema `derivation.oneOf` allows only
DIRECT_PRIMARY + WEEKLY (`reader-surface-gate-v2.schema.json:160-185`); a
checksum-only receipt is not the contract boundary. PROPOSE one bounded
INITIAL route: derive reader-only → persisted SEMANTIC_EDITORIAL review →
reviewed-only serialization → narrow receipt → generated Gate (new route/scope)
→ exact-manuscript admission at DRAFT_COMPLETE (`stage_validation:511-518`)
AND VALIDATED_DRAFT (`:563-570`) → healthy later readback (§8). If too large,
the fallback is a demonstrably complete READ-ONLY serializer/replay
preparatory component — never an admitted writer without Gate called vertical.

## 4. Canonical paths, receipt fields, Gate route/scope

| Artifact | Canonical path | Schema / route disposition |
|---|---|---|
| Reader input | `publication/v2/reader-surface-input-v2.json` | KEEP name; validate with LF-1 `longform-reader-input-v2` (route+format distinguish, not filename) |
| Semantic review | `publication/v2/reader-surface-semantic-review-v2.json` (default) | KEEP; schema already allows LONGFORM_SPECIAL (`reader-surface-semantic-review-v2:23`) |
| Receipt | `publication/v2/validated-source-manifest.json` | KEEP filename; NEW schema file (Weekly schema consts `WEEKLY_GENERATED_V2`); strict route rejection of legacy `post_architecture_directive` shape, no fallback |
| Outputs | `<survey_root>/main.tex|references.bib|jgaisurvey.sty` | canonical survey-root names (weekly `validate_receipt:744-751` pattern) |
| Gate | new `derivation.oneOf` branch | `{route:LONGFORM_GENERATED_V1, scope:LONGFORM_MAIN_BIB_STYLE, receipt:{path,sha256}}`; existing two branches untouched |

Receipt keys (mirror `weekly.build_receipt:634-666`): `schema_version`,
`issue_id`, `route=LONGFORM_GENERATED_V1`, `status`, `production_state_basis`
(path/historical_sha256/lifecycle), `accepted_refs`, `authored_refs`
(`publication-semantic-input` + `drafting-authored-archive`),
`reviewed_reader_input{path,sha256}`, `semantic_review{path,sha256}`,
`current_tools{repository_commit_sha,contract,closure}`, `outputs
{primary,bibliography,style}`, `receipt_sha256`.

## 5. Reviewed-only serialization + Gate scanner gap

PROPOSE new pure `render_main(surface)` / `render_bibliography(surface)` that
consume ONLY the reviewed surface, reusing as pure helpers base
`_render_tex:81-104`, `longform.render_package:43-119`,
`render_cross_family:122-147`, `_bib_text:35-53`, `_kicker:55-56`,
`tex_escape`, `preflight_tex:150-162`. Every emitted value enumerated in
proposal §4 (metadata/visible_text incl `toc_title=目次`/cover/frontmatter per
package pid/order/headline/deck/kicker/glance/sections/timeline/synthesis/
boundary/notes/cross rows/final_summary/bib did/key/title/author/url/urldate +
anchor order); raw Draft/body/sidecar dicts never re-read post-review. Gap
OBSERVED: `scan_structured_reader_surface:754-863` is Weekly-specialized
(`:762-786`); its fallback scans only headline/deck/blocks (`:787-863`) and
misses LF-1 nested glance/sections/timeline/synthesis/boundary/notes/bib
fields. BOTH runtime (new Longform branch) and Gate schema (§4) need the new
structured route; LF-1 reader validation is not Gate support. DIDs/keys are
mechanical, not reader prose: scan all display strings, not identifiers.

## 6. Receipt replay (five distinct digests) + write-failure rules

Distinct values: (a) authored/archive file SHAs, (b) accepted-ref file SHAs,
(c) recomputed reader FILE bytes (`canonical_reader_bytes`/`core.json_bytes`),
(d) deterministic output bytes, (e) receipt self-digest, (f) review object
digest. Replay OBSERVED pattern (`weekly.validate_receipt:726-773`): envelope +
self-digest (`_inspect:679-696`), current-tool head/contract/closure pinning
(`_verify_head_bytes` pattern), `load_derivation` at recorded State file,
accepted/authored equality, canonical output paths, reviewed-bytes equality,
deterministic main/bib/style replay vs `outputs`. Correction: Weekly
`validate_receipt` does NOT itself reload the review; review authority is
revalidated in Gate inspection (`_inspect_gate_record:1635-1650` via
`load_and_validate_semantic_review:884-1045`) and matched to the receipt
(`:1643-1650`, `_derivation_for_manuscript:1098-1101`). Longform preserves
that split. Snapshot rules: pre-validate all predictable errors before any
write; refuse-existing on every output (weekly `:135-137`, base `:188-189`);
same-byte first-pass retry only on exact bytes+authority (weekly `:77-82`);
mid-write failure reports and retains ownership, no CAS/generic atomicity;
existing partial refuses; recovery is a separate explicit operation.

## 7. Fidelity/accountability (no exact blocker found)

Manuscript schema OBSERVED: per-must-cover `reader_locations` as
`Section N — title` / `Subsection N.M — title`
(`reader-manuscript-v2:49,63,88`); `validate_reader_fidelity` resolves each to
an exact extant non-empty TeX block (`survey_reader_fidelity_v2.py:187-225`,
`:245-266`); starred headings are NOT authorities (`:105-118`); renderer emits
numbered `\section` per package (`base:54`→`longform:54`), cross (`:126`),
summary (`base:101`) but `\section*`/`\subsection*` elsewhere. Fixture
strategy: synthetic Architecture with small `must_cover_requirements`, each
mapped to its package numbered section `Section N — <headline>` with exact
title match in `(drafting_order, package_id)` emission order; non-empty bodies
required. Substantive adequacy stays ChatGPT `ARCHITECTURE_CONTENT_FIDELITY`
review (`:459-463`), never synthetic approval or skipped checks, no universal
parser. Feasibility holds at type/identity level; real-PDF/visual acceptance
stays separate. If a precise fidelity obligation later blocks rendering, it
will be returned source-grounded — none is claimed now.

## 8. Readback split + lifecycle refusals

Writer guard stays exact-DRAFT_COMPLETE (LF-1 `:969-978`); LF-1
`load_derivation(root, state_path, authored_path)` has NO `pending_basis`
param, unlike weekly `:475-500` (VALIDATED_DRAFT auto-basis `:481-486`).
PROPOSE separate read-only readback (Gate expected-manuscript + receipt
replay) at VALIDATED_DRAFT (candidate binding `:523-572`) and revalidation
(`agent_control:~1900-1979`); explicitly refuse `_PendingPublicationBasis`,
changed-Core/superseded-artifact, and stale-State-equality contexts. No
lifecycle relaxation, no pending Preview regeneration, no Weekly R1 ownership,
no stale PDF/approval reuse, no automatic historical revalidation.

## 9. Budget, call graph, oracle

| Path | Label | Role |
|---|---|---|
| `scripts/survey_longform_semantic_publication_v2.py` | A | two-pass entry (flags §2) |
| `schemas/longform-publication-source-manifest-v2.schema.json` | A | narrow receipt (§4) |
| `scripts/survey_longform_derivation_v2.py` | R | `load_derivation/build/validate/canonical_reader_bytes` |
| `scripts/survey_longform_publication_v2.py`(+base) | R | pure render helpers (§5) |
| `scripts/survey_reader_surface_gate_v2.py` | M | review loader + Longform scan branch + `_derivation_for_manuscript` Longform arm + Gate schema arm |
| `scripts/survey_reader_publication_v2.py` | M | manuscript manifest/fidelity binding for Longform primary |
| `scripts/survey_stage_validation_v2.py`+config | R | two admission sites (no logic change expected) |

Closure: LF-1 module, new publisher, `citation_refs`, provenance,
`tex_escape` renderer, reader+receipt schemas, style, config control
roots/contracts. Call graph:
publisher(pass1 derive→write reader)→review(PASS)→publisher(pass2
review-gate→serialize→receipt)→manuscript→Gate→`validate_stage`→checkpoint
(`build_stage_checkpoint`)→advance (`advance_with_checkpoint` via bridge
`_advance_stage`)→later readback replay. Oracle: synthetic-PDF + persisted
synthetic reviews prove type/identity only; negatives per task Q7 (no-write,
stale review, wrong target, tamper, malformed route, advancement/readback,
nonreader stability, Weekly/direct-primary affected checks); no old-suite
reruns. Verdict: correctable proposal, no absolute source blocker. Next:
Astra selects INITIAL scope (or READ-ONLY fallback), then scoped independent
design review. STOP before code.
