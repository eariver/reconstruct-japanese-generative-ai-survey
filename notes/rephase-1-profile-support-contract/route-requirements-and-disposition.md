# Route requirements and necessity disposition — Author C documentation-only

Status: **DOCUMENTATION-ONLY, NOT a contract decision, NOT a PASS, NOT adoption.**
No source edits/import/runtime/tests/build/fixtures/network/Git/Human-commit
readback. Source-read only from final133 proof
`/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate`
(patch `25b48878…`, manifest `31fa4a72…` per independent packaging review).
Baseline fixed `774dd39a`. Task authority: assessment §5
(`outputs/rephase-1-dm022-prearchitecture-implementation-assessment.md:52-60`)
+ roadmap §1/§4
(`outputs/rephase-1-completion-roadmap-20261019.md:27-36,66-78`).
Prior scope: `notes/rephase-1-special-support-contract/astra-scope-selection.md` FULL.
Companions: `source-class-applicability.md` (DM016), `named-obligation-applicability.md`
(DM017) in this directory. ROOT provisional policy presumed; ROOT selects next unit
order. Unknown edition priorities reported, not invented; no date/savings claim.

## 1. Provisional policy restated (no silent narrowing)

Weekly and required Special — including non-four-family Thematic and Retrospective —
MUST remain completion requirements per roadmap §1 (`...-20261019.md:36`:
"Thematic/Longformだけで暗黙に縮めない…必要経路がunsupportedなら全体完了は保留").
FIRST bounded repair is DM016 canonical new genuine source types + DM017 ordinary
full named union (shared upstream dependency, NOT all-Profile acceptance).
No automatic retirement/rebaseline/historical migration, no publication Semantic PASS.
Whole `NOT_READY`/step4B3 OPEN/audit unstarted/DM021+022 OPEN unchanged.

## 2. Route inventory (actual pair rules, not labels)

- Research profiles: `WEEKLY`, `RETROSPECTIVE_PERIOD`, `THEMATIC`
  (`config/survey-production-v2.json:138-157`; `survey_production_v2.py:349-356`;
  `survey_research_authority_v2.py:486`).
- Publication profiles: `WEEKLY_MAGAZINE`, `LONGFORM_SPECIAL`
  (`config/survey-production-v2.json:158-169`).
- Pair rule: `WEEKLY→WEEKLY_MAGAZINE`; `RETROSPECTIVE_PERIOD|THEMATIC→LONGFORM_SPECIAL`
  (`survey_production_v2.py:353-356`; `survey_period_v2.py:108-109`;
  `thematic_profile:527-528` at `survey_production_v2.py:524-543`).
- Generated routes are narrower than pairs: `WEEKLY_GENERATED_V2`
  (`survey_weekly_derivation_v2.py:627-628`) and `LONGFORM_GENERATED_V1`
  (`survey_longform_derivation_v2.py:690-691,1280-1281,1323-1324`).

## 3. Generated Longform is four-family only, not generic Thematic

`FORMAT="THEMATIC_FOUR_FAMILY_LINEAGE_V1"` (`survey_longform_derivation_v2.py:109`).
Fixed visible constants block generic reuse:
`FIXED_TITLE/EDITION/FINAL_HEADING/TOC_TITLE` (`:118-122`),
`cross_table_header=["観点","GLM","Qwen","DeepSeek","Kimi"]` (`:124-136`).
Any claim of generic-IR readiness must first diff these constants and the
serializer inventory before renaming headers. Per scope-selection §3 and contract
decision §§4-6, initial scope is the existing four-family shape; other topics need
their own mapping, not header relabelling.

## 4. DIRECT_PRIMARY / manual: preserved with honest PRIMARY_ONLY limits

Gate returns `{"route":"DIRECT_PRIMARY","scope":"PRIMARY_ONLY"}` on exact primary
path+bytes (`survey_reader_surface_gate_v2.py:1352-1356`); generated branches
require canonical `reader-surface-input-v2.json` + receipt + exact trio closure
(`:1357-1428`). Supporting `BIBLIOGRAPHY`/`STYLE` path+sha binding in a manual
manuscript is a byte hash, not a complete-reader semantic projection (contrast
`survey_reader_surface_gate_v2.py:1335-1349` editorial trio binding vs `:1356`
early return). Scope-selection decision 2 governs: keep existing manifest/support
hashes and later reviews; do NOT silently upgrade to complete supporting-surface
semantics; special decision §2: STYLE already byte-bound but pre-TeX semantic
coverage is not established.
Manual is NOT declared sufficient by code-path presence. `PRIMARY_ONLY` still
receives real post-render reviews (core `PDF_PREFLIGHT`, publication-profile
`AGENT_VISUAL` checks per `config/survey-production-v2.json:170-206`, plus
semantic-editorial/visual/Human Preview at lifecycle), which is distinct from
complete-input semantic reuse (pre-TeX Reader-Surface judgment over every emitted
value/order/citation placement). No blanket "manual unsupported publication":
manual publishes through those post-render gates; what it lacks is the
mechanical/semantic split and invalidation economy, not all review.

## 5. Retrospective and Foundations (no silent drop, no extra engine)

- Retro Profile/helper is generic upstream: `survey_period_v2.py:5-9,75-134`
  builds any `RETROSPECTIVE_PERIOD/LONGFORM_SPECIAL` from configured periods or
  bounded custom `--spec`/`--special-slug` (`:193-201`); `period_profile`
  validates pair + `BOUNDED_PERIOD` (`:105-133`). No Generated Retro exists.
  Editorial P1 refuses Retro/manual (`survey_editorial_correction_proposal_v2.py:566-573`);
  renewal admits only WEEKLY+THEMATIC (`survey_versioned_renewal_source_v2.py:637-639`);
  mechanical refresh requires WEEKLY (`survey_weekly_mechanical_refresh_v2.py:1232-1233`);
  PREARCH refuses wrong family at validation site (`...proposal_v2.py:587-589`;
  `...refresh_v2.py:46`). Editorial/renewal/PREARCH rejection preserved.
- Custom Retro bridge `--spec` gap: NOT a missing engine. The helper already
  exposes direct `--spec` CLI (`survey_period_v2.py:204-216`); if direct CLI is
  authorized per existing Human direct-execution preference, no extra
  manager/engine is needed. Record authorization, not new code.
- Foundations (`GENERATIVE_AI_FOUNDATIONS`) is a planning overlay, not a new
  profile: `survey_x_intake_v2.py:86,152-154` requires THEMATIC profile and maps
  to a Drive `series_category`, with `profile_policy THEMATIC:CHATGPT_DECIDES`
  (`config/survey-production-v2.json:129-133`). Planning-only, not product
  acceptance — but generic Thematic is still required, so Foundations demand
  cannot be used to silently drop non-four-family Thematic.

## 6. FIRST repair (shared upstream, already proposed)

DM016: centralize canonical `SOURCE_CLASS_MAP` + per-literal predicates (Option A),
no alias relabelling, no `fab1ee`-style claim (`source-class-applicability.md:§§1-3`).
DM017: ordinary explicit 7-field request union reusing unchanged validators
(O1, DM022-LOW pattern), OLD same-ID fallback only, no autofill
(`named-obligation-applicability.md:§§3-5`). Both are Profile-neutral upstream
repairs needed by Weekly/Thematic/Period alike; neither is all-Profile acceptance.

## 7. Route × stage × correction coverage (final133)

| Route | Initial → VALIDATED | P1 editorial correction | Renewal U/C | PREARCH upstream | Manual legality |
|---|---|---|---|---|---|
| WEEKLY gen `WEEKLY_GENERATED_V2` | supported (weekly derivation + Gate) | supported (`_route_of` WEEKLY; `_eligibility` VALIDATED + Arch approved) | supported (U exact-target / C new build) | supported (same-State, both routes) | n/a (generated) |
| THEMATIC four-family gen `LONGFORM_GENERATED_V1` | supported within FORMAT only | supported (same P1 path) | supported | supported | n/a |
| THEMATIC non-four-family | Discovery/Profile allowed; Evidence blocked on 10 literals (DM016 §2); reader IR blocked on §3 constants | P1 route shape passes pair check but no complete reader to correct → OPEN | route check passes but no receipt/IR → OPEN | same-State machinery exists but no accepted reader → OPEN | DIRECT_PRIMARY PRIMARY_ONLY only (§4) |
| RETROSPECTIVE_PERIOD | Profile/helper + Discovery allowed; Evidence/reader blocked (no generated IR; DM016/017 literals undetermined) | UNSUPPORTED_ROUTE (explicit refuse) | BASIS mismatch refuse | wrong-family refuse | DIRECT_PRIMARY PRIMARY_ONLY only |
| DIRECT_PRIMARY any manual | allowed as authored source (pre-acceptance authoring) | only via §8 gates, never direct changed-reader P1 | no renewal receipt | no PREARCH reader | PRIMARY_ONLY, post-render reviews only |

Citations: P1 `_eligibility`/`_route_of` (`...proposal_v2.py:548-573`);
renewal route tuple (`...renewal_source_v2.py:637-639`); Gate branches
(`...gate_v2.py:1352-1428`); DM016 10-literal gap (`source-class-...:§2`);
Thematic closure re-derived (`named-obligation-...:§4`).

## 8. When legit manual repair can actually proceed (vs blanket republication)

- Before any accepted source (pre-acceptance stages up to EVIDENCE_REVIEWED):
  authoring new source is legitimate — new manuscript/support bytes with no
  accepted authority to violate. No Gate faking needed; create a new edition
  Profile/State via the normal initialize path (`survey_period_v2.py:181,228-229`
  pattern; Weekly/Thematic equivalents).
- After VALIDATED with changed reader: direct P1 on Retro/manual is UNSUPPORTED
  (`...proposal_v2.py:573`); changed-reader republication without a proper gate
  is arbitrary correction, not legal. Legitimate paths only: (a) genuine Human
  `REQUEST_CHANGES` reopening to an allowed regeneration boundary
  (`survey_human_gate_v2.py:5-15,180,344`; never agent-synthesized PASS), or
  (b) a new edition / other proper gate (new Profile/State, new DRAFT_COMPLETE,
  or a future selected correction contract). Never fake Gate bytes, never reuse
  old-State hash as current authority (`run_drafting_synthesis_v2_interactive.py:214`;
  `survey_drafting_v2_base.py:564`; P1 `INELIGIBLE_STATE` at `:548-563`).
- Stage rule of thumb: EVIDENCE_REVIEWED bare presentation manufactures no Gate
  (`survey_human_gate_v2.py:55-60` DM022 note); VALIDATED + approved Architecture
  + pending Preview is the only P1 entry; downstream-resolved checkpoints forbid
  entry. Manual edits outside these windows are just files, not corrections.

## 9. Subsequent REQUIRED gate: complete-reader + normal correction for OPEN routes

Still explicit and unselected; compare three (cost/closure/invalidation):

1. **Generalize existing Longform structured IR** — reuse finite serializer +
   same-object rendering + exact replay; must first lift §3 constants to
   parameterized display/columns or admit new formats explicitly. Pros: keeps one
   semantic/mechanical split. Cons: touches frozen IR; each new topic pays
   schema/authority/replay proof. No generic-IR claim until constants diff closes.
2. **Separate Profile writer** (Retro-specific and/or non-four-family-specific
   reader object) — Pros: no four-family overfit; Cons: second receipt/Gate/
   producer/readback + duplicate invalidation policy; migration cost.
3. **Conservative full-review manual** (exact declared-source-set binding, raw
   bundle hash + full re-review on any byte change) — Pros: no IR invention,
   honest about closure; Cons: raw hash is NOT complete Reader (layout/deps via
   `\def`/catcodes/Lua unreadable by declaration list per scope-selection §1);
   highest re-review cost; does not deliver the semantic/mechanical split.
   Select only with explicit re-review budget, never as silent default.

## 10. Evidence bounds and unknowns

Bounds: this file is source-citation only; no runtime, no test counts, no
full-final-suite, no loader-path log claim, no publication Semantic PASS.
DM016/DM017 proposals are DESIGN ONLY (their §§5-6 list oracles/costs as
unknowns). Scope-selection + contract decision remain authority for the
generated-direction choice; this disposition adds Retro/manual/Foundations
necessity without altering them.
Unknowns (do not invent): which non-four-family Thematic topics are product-
required vs out-of-scope; which Retro periods/slugs are required and their
priority order; per-literal collector cost (DM016 §5); ordinary-path operator
burden (DM017 §5). No numeric saving/date claimed.

## 11. Root questions (selection only, no code)

1. Confirm Weekly + required Special (incl. non-four-family + Retro) remain
   completion requirements; designate required vs explicitly-disposed topics.
2. Select DM016-A (+ supplement `SOCIAL` fix scope) and DM017-O1 vs O2 as FIRST
   unit; confirm no Profile rebinding/new framework/DM016 batching beyond literals.
3. Authorize direct `--spec` Retro CLI vs declaring a bridge gap; confirm no extra
   engine.
4. Select §9 direction for the subsequent complete-reader/normal-correction gate
   as its own contracted unit after FIRST repair.
