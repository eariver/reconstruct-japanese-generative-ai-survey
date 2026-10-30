# DM016 source-class applicability — bounded repair proposal (DESIGN ONLY)

2026-10-30. Author-side proposal, NOT independent approval. DESIGN/SOURCE-READ ONLY:
no source edits/import/runtime/tests/build/fixtures/network/Git mutation/Production
refresh. Source read from final133 proof
`/tmp/opencode/jgas-dm022-indep-20261029T235900Z/proof-candidate`
(content-equal to final delivery per independent packaging review
check0/apply0, 133/768; fallback GEN/candidate-work NOT used).
Baseline `774dd39a` fixed. Captures reused from
`notes/rephase-1-deferred-intake-20261003/deferred-maintenance-summary.md:463-517`
and DM022 narrow; no refetch.

## 1. Exact source-class path (final133, file:line)

1. **Discovery (open).** `schemas/survey-discovery-record.schema.json:51`
   `source_type: {type:string,minLength:1}` — open vocabulary.
   `scripts/survey_discovery_v2.py:84-153` `_normalize_record` preserves
   locator/collector/raw_refs, no allowlist; source_type passes through.
2. **Screening (Weekly-narrow gate).**
   `schemas/screening-record.schema.json:12` enum 4
   (`paper,github-release,official-feed-item,official-index-snapshot`).
   `scripts/build_screening_index.py:135,186,265,303,319` emits only those 4.
   `scripts/survey_screening_v2.py:49-60` `SOURCE_KEYS` carries source_type;
   no open-Thematic collector exists here.
3. **Task generation (passthrough).**
   `scripts/build_evidence_tasks.py:90` `source_types=unique_strings(record.source_type)`;
   `:115` `INSPECT_INDEX` special-case on `official-index-snapshot`; no mapping.
   `schemas/evidence-task.schema.json:25` same 4-enum.
4. **Evidence builder (TWO inconsistent maps).**
   - Runner-local `scripts/run_evidence_v2_interactive.py:49-56` 6 entries
     (`PRIMARY_OFFICIAL/PAPER/REPOSITORY,SOCIAL,SECONDARY_INVESTOR_ACCOUNT→SECONDARY,SECONDARY`);
     leaf `:_source_class:110-114`.
   - Canonical `scripts/survey_evidence_v2.py:44-109` ~40 values (Weekly +
     W34 gap-fill `:80-108`); leaf `_source_class:177-184`.
   Neither contains the 10 Thematic literals (§2). Third URL-sniff map
   `scripts/run_special_interactive_evidence.py:41-47` (arxiv→PAPER,
   github→REPOSITORY, else OFFICIAL) is locator-guess, not provenance.
5. **Validator / supplement / binding.**
   `survey_evidence_v2.py:304-305` supplement `source_class==_source_class(source_type)`;
   `:413-446` `task_authority_sources` (Discovery `_source_class` + exact supplement);
   `:1016-1055` `validate_evidence_card` binds card→authority, refuses class drift.
   Public `validate_evidence_card:965` / `validate_edition_view:1437` /
   `validate_materiality_ledger:2102` vs leaf `_source_class:177`,
   `_validate_*_content:2056,2084`. Runner calls same canonical validators
   (`run_evidence_v2_interactive.py:684,717,737,782`).
   Schema gap: `schemas/evidence-authority-supplement-v2.schema.json:61` enum 4
   (no `SOCIAL`) vs `schemas/evidence-v2-card.schema.json:85` enum 5 (with `SOCIAL`).
6. **Views / Ledger (passthrough).** `scripts/build_candidate_matrix.py:171-172`
   `source_class_counts` counts only; `survey_evidence_v2.py:1663-1685` ledger rows
   carry `task_authority_sources` classes; no re-mapping.
7. **Reader (Weekly/Thematic/Retrospective).**
   `scripts/run_weekly_interactive_evidence.py:122,152,187` branches on Weekly
   `source_types`; `scripts/survey_reader_publication_v2.py:37-46` PREARCH-kind
   gate, no class mapping. Thematic/Retrospective readers consume
   Evidence/Views/Ledger via unchanged validators; unsupported type fails closed
   at step 5, never at reader.
8. **DM022 correction (no third map).** `survey_research_authority_v2.py`
   (`:1514,1536,1597,1639,2176,2182,2189`) and
   `survey_prearchitecture_acceptance_v2.py:682` call canonical
   `validate_*` / `_validate_*_content`; grep finds zero `SOURCE_CLASS_MAP` /
   `_source_class` definitions in either HIGH module. Both routes reuse the same
   canonical mapper — DM022 union did NOT repair the runner/canonical split.

## 2. Type matrix (EXACT literals; see JSON sidecar for machine form)

| # | EXACT source_type literal | runner 6 | canonical ~40 | Weekly need | Thematic need |
|---|---|---|---|---|---|
| W1-4 | `paper,github-release,official-feed-item,official-index-snapshot` | mapped | mapped | genuine supported | usable only if provenance fits |
| T1 | `PRIMARY_DOC` | MISSING | MISSING | n/a | REQUIRED per edition audit, unmapped |
| T2 | `PRIMARY_REPO` | MISSING | MISSING | n/a | same |
| T3 | `PRIMARY_ANNOUNCEMENT` | MISSING | MISSING | n/a | same |
| T4 | `PRIMARY_MODEL_CARD` | MISSING | MISSING | n/a | same |
| T5 | `PRIMARY_SPEC` | MISSING | MISSING | n/a | same |
| T6 | `SECONDARY_REFERENCE` | MISSING | MISSING | n/a | same |
| T7 | `SECONDARY_TECHNICAL` | MISSING | MISSING | n/a | same |
| T8 | `RUNTIME_RECIPE` | MISSING | MISSING | n/a | same |
| T9 | `PACKAGING_DOCS` | MISSING | MISSING | n/a | same |
| T10 | `RUNTIME_PR` | MISSING | MISSING | n/a | same |

Source-confirmed gap (not secondary-report-only): `rg` over proof `scripts/`
returns zero hits for all 10 literals; both maps read in full above. Secondary
production report (`deferred-maintenance-summary.md:479-490`, `TS-001` blocked at
first `PRIMARY_DOC`, 67/160 tasks) is consistent with, but not substituted for,
that source read. Retrospective/manual/direct-primary vocabularies are
UNDETERMINED — no literal list in captures; must not be assumed covered.

Alias relabelling (e.g. `PRIMARY_DOC→PRIMARY_PAPER` to satisfy the validator)
is prohibited: `survey_evidence_v2.py:304-305,1053-1055` enforce exact
`source_type→source_class` equality and supplement exactness; relabelling would
falsify provenance while passing shape. The pre-code rule (witnesses use only
genuinely supported types, report 10 as OPEN non-closure) stands.

## 3. Bounded contract choices (smallest coherent; no batch maintenance)

**Option A — Centralized canonical map + shared pure helper (RECOMMENDED).**
Single `SOURCE_CLASS_MAP` owned by `survey_evidence_v2` (or extracted pure
module with identical semantics); runner `run_evidence_v2_interactive` and any
HIGH helper import it, no local copy. Each newly admitted literal gets explicit
provenance + full source-specific predicates (collector, raw shape, timestamp /
`datePublished`-as-event meaning, access-provenance, card/claim binding).
Pros: one divergence-proof authority; preserves genuine semantics; closures stay
in validators. Cons: touches frozen validator-adjacent file; needs independent
re-review + fingerprint update. Compatibility: current Weekly rows unchanged
(same 6→5 values); historical bytes preserved (no rewrite). Roles: schema owner
(map + 3 schema enums), Profile owner (per-witness allowlists).

**Option B — Normalize at task stage.** `build_evidence_tasks.py` projects
Thematic literals to existing classes before Evidence. Pros: no validator-file
touch. Cons: destroys original `source_type` at the earliest derived artifact;
downstream `source_class==_source_class` checks then verify the projection, not
the original — exactly the alias-workaround failure; ledger loses auditability.
REJECT unless projection ledger + original preservation (which collapses to C).

**Option C — Maintained explicit translations + projection ledger (FALLBACK).**
Keep both maps frozen; add versioned translation table + per-task
original/projected ledger (as SP-efficient-llm-2026 compat did edition-locally),
fail closed on unmapped. Pros: zero frozen-validator diff; byte-preserving;
auditable. Cons: permanent second table to maintain; every new literal needs
table + ledger + validator pass; cost grows per Profile. Acceptable ONLY as
bounded Thematic bridge with explicit sunset into A.

No full-Profile acceptance, no `SOCIAL`-for-all default, no silent Special
narrowing, no `fab1ee`-style unsupported claim.

## 4. Schema / fingerprint / byte-preservation deltas

- Schemas: extend `evidence-task.schema.json:25`, `screening-record.schema.json:12`
  ONLY for literals the Profile owner declares supported with collectors;
  fix supplement `:61` to include `SOCIAL` (currently stricter than card);
  `survey-discovery-record.schema.json:51` stays open.
- Reader/source-control: fingerprint new map module + 3 schemas + collector/
  task-builder predicates in the delivery manifest (same pattern as final133
  `complete-dm022-manifest.json`); historical Evidence/Views/Ledger bytes and
  `b650`-era pins untouched — new acceptance creates new versioned rows, never
  rewrites old records.
- Predicate extraction is part of THIS contract (per-literal collector, raw,
  timestamp/event, access, claim-binding predicates), not deferred to code.

## 5. Desired tests / oracles / cost unknowns (no runtime proof now)

- MULTI-source/MULTI-DID: one package with Weekly 4 + ≥3 newly admitted Thematic
  literals across ≥2 DIDs; supplement + Discovery-bounded mix; ledger row per DID.
- Failure oracles: unknown literal → `unsupported source_type` refuse pre-write;
  class-drifted card → refuse at `:1053`; supplement `SOCIAL` row → currently
  schema-refuse (documents §1.5 gap); alias-labelled input → refuse, no pass;
  missing named-obligation rows → completeness refuse (DM017, separate).
- Unknowns: collector build cost per literal; full cross-profile regression
  size; manifest/fingerprint review time; translation-table maintenance if C
  chosen. No numeric saving/date claimed.

## 6. Root questions / blockers (explicit)

1. Which of the 10 Thematic literals are necessary genuine types for the
   supported product (vs out-of-scope)? Profile owner must decide; author cannot.
2. Is Retrospective/manual/direct-primary vocabulary in scope for this repair,
   or explicitly disposed as unsupported? Need literal lists or non-coverage writ.
3. A (centralize now) vs C (bounded bridge then A)? Author recommends A.
4. Who owns the canonical map file and per-literal predicates, and what
   independent re-review + fingerprint update closes it?
5. Supplement `SOCIAL` omission — defect to fix in this unit or separate?
