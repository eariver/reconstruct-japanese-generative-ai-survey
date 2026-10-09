# LF-2 initial integration proposal (design only, no code)

2026-10-09. Base 409 + exact LF-1 3-file overlay in independent
`/tmp/opencode/jgas-lf2-design-20261009T113013Z` (evidence
`notes/rephase-1-longform-lf2/evidence-20261009T113013Z/`). Observed source
below = DST bytes; proposed behavior is marked PROPOSE. No code/test/build ran.

## 0. Copy identity (observed)

HEAD 409b292/tree 8ce3699/parent 34f934e; status exactly 3 untracked; overlay
hashes 233e8655/7bae9d2a/ce687447; origin inert, shallow true, no alternates/
partialClone; 689 tracked bytes identical, 31466 both-absent (sparse
`.github/config/docs/schemas/scripts/specials/templates/tests`); 109 objects
each side, zero shared (dev,ino), no multilink; SRC pre/post identical.

## 1. Directive/control gate

Observed sole consumer `run_semantic_publication_v2_interactive_base.py:133-135`
loads `editorial/post-architecture-directives-v2.json`, requires exactly one
`FINAL_ISSUE_SUMMARY required=true placement=END...`; manifest `:202` binds its
path/sha/directive_id. No producer/schema/validator/checkpoint (grep
`post-architecture-directives` in scripts = only `:133`; `schemas/*directive*`
none; Human-gate inputs `survey-production-v2.json:218-226` lack it).
Substantive obligation already exists independent of that file: base
`:114-116` heading `この号の総括` + ≥3 paras, render `:101-103`, LF-1 schema
`final_summary` const + `build_longform_reader_input:655-666`. PROPOSE: keep
LF-1 `load_derivation:988-993` lexists refusal for any present entry (file or
dangling symlink) in the initial route; clean synthetic chain without the entry
proves the publisher. Filename/hash/absence creates or erases no authority.
BLOCKER A: satisfying the legacy publisher needs either a bound directive
producer or a Human-authorized publisher migration. Minimum decision: Human
selects bind-file vs migrate-publisher vs defer-LF-2; no D1/D2/D3 essay, no new
role, no free-text `review_reference` authority (base `:158` normalizes it;
LF-1 keeps it mechanical-only).

## 2. Actual caller

Observed public `run_semantic_publication_v2_interactive.py:66-68` runs
`_prepare_revision()` then `_base.main()`. `_prepare_revision:23-64` acts only
at `RELEASE_CANDIDATE+PUBLICATION_PREVIEW pending+no-provenance`, deleting 8
owned outputs `:46-55` before base validates. Base `:122-124` admits
`DRAFT_COMPLETE+stage:semantic-publication-validation` or revision path; LF-1
requires `DRAFT_COMPLETE+stage:reader-publication-validation`
(`derivation:969-978`, config `:330-333`). Config DRAFT_COMPLETE handler token
is `stage:reader-publication-validation`, but `survey_handlers_v2.py:452-479`
registers only `stage:semantic-publication-validation` (+others) — no
`stage:reader-publication-validation` entry and no `validate:reader-publication`
validator there. So the token is today a descriptive config string, not a
proved dispatched CLI integration; registry absence alone is not proof of total
unsupportedness (orchestrator `execute_action:521`/`load_handler_module:889`
resolves modules dynamically). PROPOSE: new explicit initial entry (not a
duplicate publisher, not a Weekly dispatch repair) that validates
lifecycle/Profile/route/directive/input BEFORE any delete; default refuses
non-DRAFT_COMPLETE, non-THEMATIC/LONGFORM_SPECIAL, present-directive,
malformed route with no DIRECT_PRIMARY fallback (`surface_gate:1082-1085`
stays PRIMARY_ONLY).

## 3. Two-pass producer (persisted review before writes)

Model observed: `survey_weekly_semantic_publication_v2.py:70-153` (surface
materialize `:70-82`, scan `:84-91`, `--materialize_surface_only :92-97`,
persisted review require `:99-114`, head-verify `:118`, refuse-existing `:135-137`).
PROPOSE Longform pass-1: `load_derivation` (LF-1 `:949-1117`) returns in-memory
`surface/accepted_refs/authored_refs`; `validate_longform_reader_input:922-941`
+ `canonical_reader_bytes:944-946` (`core.json_bytes`) written once to edition
`publication/v2/` reader-input path (new name TBD, not Weekly's
`reader-surface-input-v2.json`). Pass-2 must call existing
`surface_gate.load_and_validate_reader_surface_semantic_review:884-1045` with
`expected_issue_id/profile/surface_path/surface_sha256, require_pass=True`,
enforcing SEMANTIC_EDITORIAL (VISUAL rejected), `reader-surface-semantic-
review-v2` schema, digest, `READER_PIPELINE_INDEPENDENCE` + all checks
detail/locs, PASS→all-PASS + 0 unresolved blocking, reviewed_by/recorded_at,
disk-byte drift `:992-1000`. `build_semantic_authority:1051-1068` already
forbids synthetic PASS. Mismatch/non-PASS/missing → fail closed before any
main/bib/sty/receipt writes. Later SEMANTIC/VISUAL/Architecture/Human Preview
(`stage_validation:501-502`, `reader_publication.build_review_record:458-541`)
stay distinct; no generated PASS, no free-text authority.

## 4. Same-input serialization

Observed emitters: base `_render_tex:81-104`, `longform.render_package:43-119`,
`render_cross_family:122-147`, `_bib_text:35-53`, `_kicker:55-56`,
`tex_escape`, `preflight_tex:150-162`. PROPOSE every emitted value comes from
the reviewed object only: issue_metadata title/display_as_of; visible_text all
consts incl `toc_title=目次`, edition_descriptor; cover/headline/deck/anchors;
frontmatter heading/lede/scope_notes; per-package pid/order/headline/deck/
kicker/glance/sections/timeline/synthesis/boundary/notes
(title/chronology/points/limitation/primary_url); cross heading/paras/rows
(観点/GLM/Qwen/DeepSeek/Kimi); final_summary heading/paras/placement; bib
did/key/title/author/url/urldate + anchor order. Raw Draft/body/sidecar dicts
never re-read after review (wrapper docstring preserves this). Finite policy:
reuse LF-1 token/URL grammar + `tex_escape`; `\url{}` unescaped `:116`;
preflight layout/leakage; `_safe:24-29` containment; owned outputs only
`main.tex/references.bib/jgaisurvey.sty` (+optional pdf/log/sha not all
mandatory); refuse-existing + exact no-write windows. LF-1 source-only change:
none expected beyond exposing constants accessor; any change needs fresh
31-method proof under Astra decision.

## 5. Receipt/Gate and closure

PROPOSE new narrow `schemas/longform-publication-source-manifest-v2.schema.json`
(do not reuse Weekly receipt schema; Weekly `ROUTE=WEEKLY_GENERATED_V2`,
`RECEIPT_SCHEMA`, `CURRENT_CLOSURE:28-37`). Filename
`publication/v2/validated-source-manifest.json` may be retained only with
explicit route/schema rejection of the legacy shape (base `:202` legacy binds
`post_architecture_directive+semantic_input`). Fields (mirror
`weekly.build_receipt:634-666`): issue/route `LONGFORM_GENERATED_V1`/status,
state basis {path,historical_sha,lifecycle}, accepted/authored refs,
reviewed_reader_input {path,sha}, semantic_review {path,sha}, current_tools
{commit,contract,closure}, outputs {primary,bibliography,style},
receipt_sha256. Independent rederivation: `load_derivation` + validate +
canonical bytes + new `validate_receipt` + extend
`surface_gate._derivation_for_manuscript:1071-1118` (today Weekly-only
`:1086-1118`; DIRECT_PRIMARY `:1082-1085` preserved; malformed Longform gets no
fallback). Gate: `validate_reader_surface_gate:1670-` with mandatory
`expected_manuscript_path` at both `stage_validation` DRAFT_COMPLETE
`:511-518` and VALIDATED_DRAFT `:563-570` + publication revalidation;
generation-State hash is provenance, not later equality. Closure: LF-1 module,
new publisher, citation_refs, provenance, tex_escape, reader+receipt schemas,
style, config control roots/contracts. No Weekly closure import, no silent
`CURRENT_CLOSURE` change, no opaque bundle. Overlay testing: independent
synthetic committed fixtures carry the test; receipt `_verify_head_bytes`
pattern (`weekly:577-631`: ancestor/control-diff/dirty/untracked/closure-byte
checks) stays strict — do not claim the uncommitted composite HEAD is
committed; no candidate commit authorized here.

## 6. Lifecycle

Write-entry only at DRAFT_COMPLETE + `stage:reader-publication-validation`
(config `:330-333`). Later read-only revalidation at VALIDATED_DRAFT
(candidate binds manuscript/source/bundle/reviews `:523-572`),
RELEASE_CANDIDATE/FROZEN via existing gate paths (`agent_control:1931`);
current authority = validated current accepted artifacts + Gate
expected-manuscript, never stale generation-State equality. Refuse: any
non-DRAFT_COMPLETE write, pending-Preview regeneration via interactive delete
path, Weekly R1 ownership reuse, changed-output repair, stale PDF/Human
approval reuse after bound changes, automatic historical revalidation.

## 7. Path/API/fixture/acceptance budget

| Minimal path | Callsite / role |
|---|---|
| `scripts/survey_longform_publisher_v2.py` (new) | two-pass entry: derive→review-gate→serialize→receipt |
| `schemas/longform-publication-source-manifest-v2.schema.json` (new) | narrow receipt |
| `scripts/survey_longform_derivation_v2.py` (LF-1, read) | `load_derivation/build/validate/canonical_reader_bytes` |
| `scripts/survey_longform_publication_v2.py` + base entry (read/adapt) | `render_package/render_cross_family/preflight_tex` |
| `scripts/survey_reader_surface_gate_v2.py` (reuse) | review loader + Gate `expected_manuscript_path` |
| `scripts/survey_stage_validation_v2.py`, config (read) | DRAFT_COMPLETE/VALIDATED_DRAFT admission |

Fixture: extend LF-1 real synthetic accepted Thematic chain (not schema-only).
Future proof cases: two-pass no-write when review missing/stale/non-PASS;
wrong same-issue target; deterministic independent replay; fresh-rehash tamper
of reader/main/bib/style/control; malformed route with no DIRECT_PRIMARY
fallback; supported advancement + readback; same-byte nonreader stability;
affected Weekly/direct-primary regressions. No rerun of passed-31/old suites
for decoration. Source type/identity tests ≠ rendered/semantic review.

## 8. Boundary/cost and blockers

Full LF-2 (publisher+review+serialize+receipt+Gate both sites+readback) is too
broad for one review. PROPOSE first complete vertical V1: pass-1 reader
materialize + persisted review gate + same-object main/bib/sty + narrow receipt
at DRAFT_COMPLETE only, deferring VALIDATED_DRAFT readback + stage-admission
wiring to V2. V1 is independently verifiable (no knowingly unverifiable
writer); V2 reuses its bytes. Cost not zero: serializer escaping/closure,
receipt replay, fixture chain, independent review. Real blockers: (A) §1
Human publisher-authority decision; (B) DRAFT_COMPLETE dispatch proof for the
`stage:reader-publication-validation` token (config vs actual dispatch). Next
decision for Astra: approve V1 boundary + receipt filename/route disposition +
review filename, or return blocker resolution. Then STOP at Human Commit Point.
