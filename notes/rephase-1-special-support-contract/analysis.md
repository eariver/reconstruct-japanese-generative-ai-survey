# LONGFORM_SPECIAL direct-source/support contract — analysis before code

Fixed source: 409b292756dd1277b9dfae87679934c0d2ce251c, tree 8ce3699861505f32d1d60bdc185d4d4f635aedb2,
parent 34f934e, at `/tmp/opencode/jgas-dm004-impl-20261004T234416Z`, branch
`codex/dm004-release-validate-state`. Read-only verify with
`GIT_NO_LAZY_FETCH=1 GIT_OPTIONAL_LOCKS=0 GIT_ALLOW_PROTOCOL=file`: HEAD/tree/parent match,
`status --porcelain` empty (tracked clean), origin `https://example.invalid/...` inert,
`--is-shallow-repository true` (inherited shallow at 774 only). No root override, no writes,
no network/agents/tests/fixtures/objects/refs. Production 774 unchanged; no Summary refetch,
linked records, old suites, main, or recovery. `apply_patch` is not available in this tool
environment; this new packet file uses Write only. No entry/gitattributes/old-file edits.

## 1. Actual producer/caller path (409 worktree = HEAD, clean)

- No LONGFORM generated reader-input adapter exists. `schemas/reader-surface-input-v2.schema.json`
  (blob 5594f1e9) `route: const WEEKLY_GENERATED_V2` only; `schemas/reader-surface-gate-v2.schema.json`
  (blob 90ec8fe2) `derivation.oneOf` allows only `DIRECT_PRIMARY/PRIMARY_ONLY` or
  `WEEKLY_GENERATED_V2/WEEKLY_MAIN_BIB_STYLE` with receipt. Gate
  `scripts/survey_reader_surface_gate_v2.py` (blob 89b5b859) `_derivation_for_manuscript:1082-1118`
  returns PRIMARY_ONLY on exact primary path+bytes, else requires WEEKLY/WEEKLY_MAGAZINE:1086,
  canonical `reader-surface-input-v2.json:1088-1092` plus `validated-source-manifest.json` receipt:1093-1101
  and exact 2-support main/bib/style closure:1102-1118. A LONGFORM structured target is explicitly
  rejected at :1086-1087. Do not assume Weekly fields apply to Special.
- Actual LONGFORM_SPECIAL direct/manual producer is
  `scripts/run_semantic_publication_v2_interactive_base.py` (blob 4aa20a4b): requires
  LONGFORM_SPECIAL profile :130, DRAFT_COMPLETE or pending RELEASE_CANDIDATE Preview State :122-124,
  shared `validate_agent_state` :126-127, accepted Draft packages/results vs semantic archive :141-153,
  Evidence acceptance + `longform.validate_revision` :154-158, per-DID canonical name/URL/source-provenance
  and HOLD/NEEDS_MORE refusal :163-186, then writes `survey_root/main.tex`, `references.bib`, copied
  `jgaisurvey.sty`, longform `validated-source-manifest.json`, preflight and quality bindings :187-205.
  Rendering is split: `survey_longform_publication_v2.py` (blob 540245ca) `render_package:43-119` /
  `render_cross_family:122-147` / `preflight_tex:150-162` over reviewed `longform_revision` validated by
  `survey_longform_publication_v2_base.py` (blob d4f53f63) `validate_revision:75-189` (exact package-set
  match, per-DID Evidence allowlist, HOLD refusal, Technical-Notes cover-every-source-once :181-183).
- THEMATIC vs RETROSPECTIVE_PERIOD reach the same renderer today but are not the same authority.
  `scripts/survey_production_v2.py:295-296` (profile validation) requires LONGFORM_SPECIAL for both
  research profiles; THEMATIC init at :467/479/482 uses `surveys/special/<id>` survey_root, while
  `scripts/survey_period_v2.py:2-69/104-177` is the Retrospective bounded-period bootstrap/validator.
  `schemas/special-edition-manifest.schema.json` distinguishes `edition_kind` with THEMATIC requiring
  `topic_scope` string vs RETROSPECTIVE null :62-70. Config `survey-production-v2.json` (blob cffe16fe)
  gives distinct temporal policies, synthesis payloads, and quality checks (THEMATIC open-history vs
  PERIOD bounded-period; THEMATIC_HISTORICAL_ATTRIBUTION vs PERIOD_SCOPE_LABEL_IDENTITY :131-180).
  X-intake categories are likewise distinct (`Retrospective_Special` vs `Thematic_Special`).
  Supported caller today is the direct renderer above; any "Longform adapter" is a future option, not
  a present schema-allowed path. A schema permitting LONGFORM_SPECIAL in manuscript/Gate profile enums
  is not proof of a generated route.
- Manuscript/Gate/review authority: `schemas/reader-manuscript-v2.schema.json` (blob a751a4bc) allows
  research `WEEKLY|RETROSPECTIVE_PERIOD|THEMATIC` x publication `WEEKLY_MAGAZINE|LONGFORM_SPECIAL`,
  with `primary_source` + `supporting_files[]` roles `BIBLIOGRAPHY|STYLE|SUPPORTING_SOURCE` :34-46,
  plus `architecture_coverage`/`reader_requirements`. `scripts/survey_reader_publication_v2.py`
  (blob a1ba8670) pins primary to canonical `survey_root/main.tex` :213-219, dedupes support :221-236,
  requires exact Architecture/requirement-set match :238-258, then LONGFORM deterministic fidelity
  :267-273 and lexical Gate :275ff. `scripts/survey_reader_fidelity_v2.py` (blob b5b8953b)
  `validate_reader_fidelity:252-319` proves only that claimed locations resolve to exact extant
  non-empty numbered TeX blocks (`Section N — title`); substantive adequacy is explicitly left to
  `ARCHITECTURE_CONTENT_FIDELITY` semantic/editorial review (schema :49/63/88). Gate
  `evaluate_reader_surface_gate:1136-1265` scans PRIMARY_SOURCE tex :1200-1214, BIBLIOGRAPHY via
  `scan_bib` :1233-1240, SUPPORTING_SOURCE `.tex` via `scan_tex` :1241-1248, manifest/coverage text,
  synthesis payload, and structured surface (Weekly full-field scan :762-786; non-Weekly narrow scan
  :787ff). Semantic authority comes only from a persisted validated review
  (`build_semantic_authority:1051-1068` refuses synthesis; `load_and_validate_...:1023-1048` requires
  PASS/identity/timestamps). Later `BIBLIOGRAPHY_METADATA` (AGENT_SEMANTIC), VISUAL
  (`TOC_HIERARCHY/LONGFORM_PAGE_BALANCE/...`), PDF preflight, and Human ARCHITECTURE/PUBLICATION_PREVIEW
  gates (config :156-195/214-226) remain separate; reusing them as pre-TeX PASS is rejected.

## 2. Field/surface responsibility (selected B split vs 409 actual)

| Surface | Existing manifest/schema field | Producer/input authority | Actual scan/review target + replay check | Missing guarantee / proposed owner |
|---|---|---|---|---|
| Primary TeX | manuscript `primary_source` path/sha/bytes | direct renderer output; Profile `survey_root/main.tex` authority | Gate PRIMARY_SOURCE lexical scan; DIRECT_PRIMARY exact path+bytes (:1082-1085); fidelity block resolution | Supports primary identity only; owner: Reader-Surface semantic review (existing role) |
| Declared support TeX/includes | `supporting_files[]` role SUPPORTING_SOURCE | manual author (no generated adapter) | Gate scans only `.tex` SUPPORTING_SOURCE; dynamic `\input/\include`, extra `.bib`, paths outside closure have no allowlist check for Special (Weekly has `validate_generated_closure` + build-dir inventory; Special has neither) | Missing: declared-closure allowlist + alias/dynamic refusal. Owner: same Reader-Surface review + deterministic replay (new narrow check, no new role) |
| Bibliography `.bib` + citation placement/order | `supporting_files[]` role BIBLIOGRAPHY; longform bib from accepted Evidence (`_bib_text:35-53`, `bib_key_by_did:192-193`) | accepted Evidence cards + `longform_revision` allowlists; `technical_notes[].primary_url == canonical_url` (:165-167) | Gate `scan_bib` lexical only; placement/order bound only via renderer `_cite` + manifest `cited_discovery_ids`; no Special equivalent of B's exact `_refs` placement replay | Missing: independent placement/order replay against accepted Draft/Result. Owner: Reader-Surface review judges values; deterministic check proves placement |
| Source notes/URLs/access dates | bib `url/urldate`; `technical_notes.primary_url/chronology/limitation`; `provenance_resolver` dates | accepted Evidence entity `canonical_name/canonical_url` + source access provenance | Deterministic URL/date presence checks; semantic truth/role/strength NOT proved (DM-013/020) | Owner: semantic/editorial + provenance review (existing); deterministic check only binds bytes |
| Content-emitting style/helper | `supporting_files[]` role STYLE; `templates/survey/jgaisurvey.sty` (blob 16c68ba2) `\surveysetup/\surveycoverstory/\surveyeditiondescriptor/\surveyrepository/\surveybuildvalue/\surveycoverlabels/\surveystrapline` (:75-100) + `surveycover/sectionkicker/wideflow/claimboundary/themeoverview/technicalnote` (:110-188) | renderer passes reviewed strings into style macros; trusted style bytes copied (`shutil.copyfile` :190) | **Gap:** Gate records STYLE as SUPPORTING_SOURCE kind but applies no `scan_tex` (suffix `.sty` fails :1241 condition); style lexical/provenance scan absent. Weekly binds style via receipt outputs + CURRENT_CLOSURE; Special binds only via longform manifest `style.source/copied_sha` | Missing: STYLE byte binding + content-vs-layout separation in Gate replay. Owner: exact source closure + visual review; content-emitting changes are semantic inputs |
| Layout-only/external TeX | same STYLE bytes; `\RequirePackage` list (:4-27), geometry/column/indent (:46-58) | upstream style + installed TeX | visual/preflight responsibility; `preflight_tex` layout/leakage checks | Owner: visual/publication review; not pre-TeX semantic identity |
| Provenance/comments | longform `% package:...draft-result-sha256` (:98); receipt-style hashes in longform manifest | mechanical derivation evidence | Must be fixed literals/hex/safe tokens; arbitrary TeX/comments unreviewed | Owner: mechanical authority; reader input unchanged => no semantic re-review, but bound bytes change still invalidates exact approvals |

Distinguish: declared hash binding (manifest/Gate `scanned_surfaces`) ≠ lexical scan (prohibited-pattern lint)
≠ substantive semantic review (intelligibility/sufficiency) ≠ source fidelity (claim-to-accepted-source)
≠ rendered proof (PDF/visual). Hash equality never proves support semantics.

## 3. Two bounded options (real paths/cost; unknowns not zero)

(a) Declared-source/bundle review target for the actual manual route. Touch: manifest validator
(`survey_reader_publication_v2.py`), Gate (`survey_reader_surface_gate_v2.py`), fidelity
(`survey_reader_fidelity_v2.py`), no new renderer/adapter. Review target = finite declared set
(primary + named bib + named style + enumerated supporting TeX), each path+sha+bytes bound, alias/symlink/
dynamic-include/undeclared-entry refusal, STYLE included in lexical scan-or-explicit-trust list.
Invalidation: any declared byte change => new semantic review + new Gate; nonreader mechanical-only change
(e.g. provenance comment literal rotation with identical reader values) => mechanical re-evidence, no
semantic re-judgment, but stale PDF/visual/Human approvals still lapse on byte change. Cost: small new
validation + fixtures; duplicate work minimal; caller-compatible (renderer unchanged); leaves accepted-source
derivation unproved (accepted by construction, not replayed). Fails closed on undeclared/dynamic content.
(b) Justified Longform profile adapter with accepted source + deterministic replay. Touch: (a) plus a new
narrow Longform derivation module + receipt schema + reader-input or bundle schema + publisher threading
(analogous to `survey_weekly_derivation_v2.py` blob 6d14009c: `validate_reader_input:383-393`,
`render_main:400-442`, `render_bibliography:445-461`, `validate_generated_closure:464-472`,
build-dir inventory :100-123, CURRENT_CLOSURE :28-37). Invalidation: same as Weekly — accepted-input or
closure/output drift forces regeneration + re-review; unrelated JSON/hash refresh is not an oracle.
Cost unknown (new schema/renderer/receipt/pending-context threading, Thematic vs Retrospective divergence,
citation-placement replay); duplicate work with (a) if both built; migration risk (forcing Weekly fields onto
Special or silent legacy-JSON fallback — both rejected). Reject: all-internal-metadata copies into review
target, undocumented late-review reuse, universal TeX parser. Do not select (b) merely for fewer apparent
lines; (a) is the minimal honest closure, (b) is justified only if Astra wants replayable accepted-source
proof for Special.

## 4. Proposed minimal contract (for Astra selection; recommend (a) now, (b) later if needed)

- Semantic-review identity: the persisted `reader-surface-semantic-review` PASS over the exact declared
  bundle (primary + enumerated supports + manifest coverage text + rendered bib values + style-emitted
  strings). Mechanical/source authority: manifest path/sha/byte bindings + Gate `scanned_surfaces` +
  longform manifest `rendered_source/bibliography/style` shas. Neither substitutes for the other.
- Membership/order/hash: closed membership list in manifest; order-sensitive bib/citation binding
  (`cited_discovery_ids` order + per-placement `\cite` replay); sha256 + byte_count on every member;
  canonical `survey_root` paths only; no same-issue/Profile inference, no directory scan.
- Reader-visible support values judged: all bib title/author/url/urldate, technical-note title/chronology/
  points/limitation/primary_url, cover/frontmatter/summary strings passed into style macros, section/head/deck/
  kicker text, claim-boundary text. Reviewer judges meaning; deterministic check judges exact bytes/placement.
- Style trust boundary: `jgaisurvey.sty` bytes pinned; layout internals trusted under exact closure + visual
  review; any macro that emits variable reader-visible text (`\survey*` setters, `surveycover`,
  `sectionkicker`, box titles) is a semantic input — changing its call arguments requires re-review,
  changing its definition requires re-review + visual re-proof. Never label content-emitting change "layout-only".
- Safe nonreader changes: provenance-only comment/hex-literal rotations that leave every reader value and
  rendered byte except the comment itself unchanged may update mechanical evidence without semantic
  re-judgment; all exact-output approvals still lapse per existing byte rules.
- Path/alias/undeclared/dynamic: repo-local canonical paths only; refuse symlinks/ancestors/escapes
  (follow `_safe`/`repo_local_path` precedent); refuse `\input/\include` beyond declared set, extra
  `\addbibresource`, undeclared files in `survey_root`, and `.aux/.bbl` re-read as inputs; decoy same-byte
  directory does not satisfy binding (bind receipt/manifest paths to canonical Profile dir).
- Stop policy: unsupported input (ambiguous Evidence needing unaccepted sidecar, dynamic includes,
  unknown style dependency, divergent Thematic/Retrospective source-class gap) => bounded fail-closed stop,
  not silent acceptance, generic resolver, new authority, or new reviewer role. All existing
  Reader-Surface/Architecture/Publication/visual/Human obligations stay with their current owners.

## 5. Acceptance matrix (proposed only, not executed)

Deterministic type/identity (real loader/validator positives + targeted mutation negatives):
same-main with changed bib/style/support bytes rejected; fresh rehash without semantic review rejected;
wrong same-issue manifest (swapped primary, missing/duplicate primary, stale bytes) rejected per B/A boundary;
undeclared `.sty/.cls/.tex` or `\input` dynamic route refused; mechanical-only annotation control passes
semantically but rebuilds mechanical evidence. Genuine semantic/rendered (require reviewer + rendered proof,
never hash-only): bibliography role/date-qualifier drift (DM-013: version vs announcement vs collector dates
across body/bib/notes); source-role/strength drift (DM-020: novelty/strength/conditions/role misrepresentation
despite resolved keys); content-emitting style vs layout-only (changed cover/kicker/box text vs pure geometry);
Japanese technical-meaning preservation (DM-006 seed-corpus lint as review aid, `auto-rewrite allowed: false`);
rendered QA (DM-018: Overfull/clipping log→page binding, mandatory appendix/glossary coverage, no VISUAL PASS
over material clipping). Do not redeclare whole B3 closed; reuse B/A oracles for Weekly/DIRECT_PRIMARY only.
No claim that a mock/synthetic fixture, hash match, or schema-valid review proves a production route works.

## 6. Path budget / stop

Actual paths with reasons: `scripts/survey_reader_publication_v2.py` (manifest closure/canonical primary);
`scripts/survey_reader_surface_gate_v2.py` (STYLE/support scan + Special closed inventory + derivation branch);
`schemas/reader-manuscript-v2.schema.json` + Gate schema (only if membership fields must change — prefer
no schema change for (a)); `scripts/survey_reader_fidelity_v2.py` (support-block resolution if SUPPORTING_SOURCE
claims locations); `templates/survey/jgaisurvey.sty` read-only reference (trust boundary list, no redesign);
tests/fixtures proposed only (real caller/loader/validator + mutation oracles above). Fixture feasibility:
synthetic LONGFORM_SPECIAL fixtures can exercise deterministic refusal/identity; they cannot prove publisher
validity, visual truth, or Human approval. Upstream prerequisites distinct from support semantics: DM-016
(Evidence source-class admission for Thematic types) and DM-017 (completeness builder vs validator obligation
lifecycle) must be resolved before any adapter claims accepted-source completeness; they are not the same
defect as supporting-TeX semantics. DM-006/013/018/020 inform acceptance using only the saved Summary capture
(`notes/rephase-1-deferred-intake-20261003/`); no unread corpora/Issues/edition repairs adopted, no auto-rewrite
or numeric-threshold engines. Build transfer/real PDF compilation stays separately dispositioned. Missing fixed
materialized inputs (no live `/tmp` DBs beyond the named 409 DB; no hydrated historical blobs): disclosed,
not fetched. Whole candidate NOT_READY, step4/B3 OPEN, canonical audit unstarted. Stop here for Astra
architecture selection; no code until the contract choice is recorded + scoped independent review.
