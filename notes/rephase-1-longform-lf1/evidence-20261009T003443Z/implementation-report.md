# LF-1 implementation/test report (source-only, no commit)

2026-10-09. Implements Astra `astra-implementation-selection.md` (overrides
proposal/correction on conflict). Independent copy
`/tmp/opencode/jgas-lf1-design-20261009T001653Z` at fixed409
(`409b292756dd1277b9dfae87679934c0d2ce251c`, tree
`8ce3699861505f32d1d60bdc185d4d4f635aedb2`); HEAD/tree unchanged, no
candidate commit/branch. Exactly 3 new working-overlay paths; every run
guard asserts status shows ONLY these + zero tracked modifications.
No reconstruct/source/restore writes except this new packet dir.
No network/subagents/old-script reruns. Fixture Git DBs are independent
temp dirs. STOP for Astra, then author-independent review. NOT shipping PASS.

## 1. Overlay (hashes stable across all authoritative runs)

- `scripts/survey_longform_derivation_v2.py` (909 lines)
  `c35eed84b5fe05fdd218581a919fd8aae732ccd4c2bbc9a0c159d8a43e17ba26`
- `schemas/longform-reader-input-v2.schema.json` (209 lines)
  `71156a53b776a82928519b0a3f821cf40bd4279550e0bc4973c7ed27394e588b`
- `tests/test_survey_longform_derivation_v2.py` (880 lines)
  `bd0893a030b86098aa56698004988177bc9a5c1fa368222432b0bd4d050cb7e7`
- Patch: `overlay.patch` (vs /dev/null); bytes: `overlay-sha256.txt`.
- No shared-helper/schema/config/Weekly-closure edits; no CLI; no renderer
  import/invocation; no reader-file/Gate/receipt writes; no CURRENT_CLOSURE.

## 2. Behavior (selected deltas from proposal)

- `load_derivation(root,state_path,authored_path)` read-only; exact
  DRAFT_COMPLETE + `next_action==stage:reader-publication-validation`
  (config-bound); THEMATIC/LONGFORM_SPECIAL; no later-state route.
  Legacy `editorial/post-architecture-directives-v2.json` lexists (file OR
  symlink, incl. dangling) refuses BEFORE projection, never read as authority.
- Pure `build_longform_reader_input(...)` (fixed construction order);
  `validate_longform_reader_input`; `canonical_reader_bytes` =
  `core.json_bytes` with digest = SHA256 of those bytes (never sha256_object).
  Reader object has NO provenance/audit fields (mechanical refs + authored
  refs returned side-channel in memory only).
- `toc_title=目次`; single `edition_descriptor`; all note labels
  (`Chronology:`/`Technical points:`/`Limitation / attribution:`/`Primary URL:`),
  kickers, box/table/reference/cover/build/strapline/date-prefix constants
  explicit (style defaults recorded as observed overrides, no Weekly reuse).
- URL subset exactly as module docstring: HTTP(S)+host, ASCII, reject
  whitespace/controls/`{} \%#^~"<>|` + backslash; `%`/fragments/non-ASCII IRI
  refused undisclosed-transform (exclusions disclosed, exact issue returned).
- Card-only access with `explicit_source_id=None` always; differing-timestamp
  ambiguity refuses; single-DID rows; unique primary-subject entity;
  same-entity title/URL/org (`Unknown` only null/empty); Matrix/Materiality/
  Discovery/Draft exact-one `refs` eligibility; VERIFIED/PARTIAL only.
- Stage-advanced Evidence revalidation uses the production
  historical-basis override (same mechanism as the Weekly accepted-source
  loader), not a mock.

## 3. First accepted fixture feasibility: PROVED (not blocked)

Synthetic THEMATIC/SP001 chain (compliant `*-D###` DIDs) reaches State AT
DRAFT_COMPLETE via current producers + real stage checks/checkpoints + typed
Architecture approval (evidence→views→ledger→completeness→matrix→selection→
architecture→approval→packages/results→synthesis→archive/authored→X→discovery
acceptance→6 stage advancements). Positive + order + stability green.
Genuine authority edges hit during setup (recorded, not bypassed):
canonical accepted-Evidence tree materialization; result rebind after approval;
NEEDS_MORE blocked at real readiness (test asserts BLOCKED there — held-back
evidence never reaches projection); task-bound sources forbid unbound URLs.

## 4. Test report (raw logs in this dir; pre/post guards per run)

New suite 20/20 on final code: `run-final-A.log` 6 OK (positive, reorder
normalization, 2-package order, Unknown fallback, mechanical stability,
no-writer inventory); `run-final-B.log` 5 OK (unknown DID, dup note, URL
mismatch, tamper hash, access ambiguity); `run-batch-B3.log` 2 OK
(held-back early-block, unsafe URL end-to-end + policy set);
`run-batch-C.log` 7 OK (missing row, directive file/symlink, earlier
lifecycle, runner, escape, symlinked ancestor). In-test guards: temp-tree
byte inventory equal across derivation; no `main/bib/sty`/gate/manifest
under edition roots; legacy writer absent from `sys.modules`.
Regression: `run-regression.log` 5/5 OK
(`BibliographyAccessProvenanceUnitTests`, shared resolver contract).
Superseded development runs preserved untouched:
`smoke-01..04.log`, `run-batch-A.log`, `run-batch-B.log`, `run-batch-B2.log`
(canonical-tree copy, result rebind, historical-basis override, loop-indent,
stability-scope, fixture-scope fixes — each cause+fix above).
`test_longform_publication_v2.py` bare-function tests not run (no pytest in
environment); the new module does not import that code.

## 5. Limits / LF-2 blocks unchanged

Whole candidate NOT_READY, step4/B3 OPEN, canonical audit unstarted.
LF-2 still blocked: legacy publisher file authority/producer, real
DRAFT_COMPLETE artifact producer/handler, receipt/Gate replay, serializer
escaping/closure (incl. IRI/`%`), later-state readback. No new authority
created here. Runner: `run-focused.sh` (asserting guards, raw log per run,
`PYTHONDONTWRITEBYTECODE=1`, fixtures outside source). Debug helper
`/tmp/opencode/lf1-debug.py` removed after use; no stray state.
