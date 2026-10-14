# Correction to retained-aware current-authority proposal (F1–F6)

2026-10-14. Design Co-Worker (General). Preserves `analysis.md` (initial,
445 lines, NOT selected) and `source-binding.md`; this file corrects per
`astra-feedback.md` F1–F6. No code/schema/test/fixture/copy/network/old-script
actions. Read-only file citations below (`proposal_v2.py` = P1 module
`5d2fde45`, 1830 lines; `retention_v2.py` = P2R module `3833b14a`, 2080 lines).
STOP for root selection; no new Human Gate/role.

## F1 — three comparisons, no invented history

Withdrawn: `analysis.md` §1 “proposal-time whole-tree + retained delta”.
Proposal stores basis/plan/digests, not a complete tree inventory: proposal
schema strict keys (`proposal` schema, no tree map); `_pipeline` proposal
object `:1454-1485` carries refs/digests/plan only. Manifest stores
rows/`capture_inputs`, not an immutable dir map (manifest schema, 149 lines).
P1 `_tree_map:267-318` is an intra-call snapshot (root-anchored, alias/FIFO
refusal, `.git` excluded), passed as `tree_entry` and compared intra-call
(`_pipeline:1440-1442`; `prepare:1629-1631`; `validate:1819-1821`).

Corrected P2V comparisons:

- (a) **Current rederived vs supplied proposal.** Rederive authority/before
  graph/plan from live bytes via factored data helpers, then exact field
  equality per `validate:1778-1801` (header `:1778-1781`, basis `:1782`,
  authoring `:1785-1786`, reader ref `:1787-1788`, canonical digest
  `:1789-1791`, description nonempty/by-construction `:1793-1794`, ref-digest
  `:1795-1797`, retention `:1798-1799`, staged bytes `:1800-1801`). No
  proposal-time tree equality required.
- (b) **Persistence vs retained rows.** Same-invocation retained validation
  per `verify:1926-2056` (inventory, COPY rehash `:1953-1959`, KEEP repin
  `:1960-1963`, staged `:1964-1988`, final re-inventory `:2043-2056`).
- (c) **Intra-call zero-delta.** From THIS invocation entry (retention already
  present) to final observation: `col.reverify` (`proposal_v2.py:191-233`:
  ancestor-alias + bytes + HEAD + config) and `_Session` reverify/close
  (`retention_v2.py:243-278,501-519,2056-2066`) plus entry-vs-final
  control/edition/retained inventories. Read-only observer permits **zero**
  invocation-caused additions — no retained-delta allowance. Preexisting
  unrelated files outside the retained closed inventory are not automatic
  staleness unless authority predicates (rederived graph, receipt/Gate/bundle,
  control/edition pins) make them so. `capture_inputs` extras are historical
  observations (`verify:2009-2019` scope comment `:2010-2016`), not a complete
  provenance map.

## F2 — data-only factoring, no enum/verified_set

Withdrawn: `_retention_plan_with_policy(..., verified_set=...)` and
`_pipeline_common(..., dest_policy, verified_set)`. An enum is still a
bypass-shaped interface when a caller supplies the acceptance set.

Corrected shape:

- **DATA-ONLY helpers** (pure, no acceptance): extract graph construction
  (`_build_graph` callers `:1431-1436`), plan-row construction from
  graph+proposal_dir (rows/roles/policy/dest strings, no filesystem existence
  verdict), canonical-bytes derivation (`_derive`/`_canonical:431-451`), and
  field-equality comparators (mirror `:1778-1801`). A data helper never
  returns readiness.
- **FIXED completions** (acceptance, per entry, no mode/skip/token):
  existing P1 wrappers always perform absence checks (`_retention_plan:
  :1269-1284`: `dest in inputs` `:1269-1270`, namespace overlap `:1271-1274`,
  absent-required `:1278-1284`); new P2V observer always performs full
  same-invocation retained validation + equality (§F3 order). No public
  mode flag, no caller `verified_set`, no trusted `VERIFIED`/`input_hashes`.
  Each success path is fixed at its call site and reviewable as such.
- **Live/retained separation** (concrete): `_retention_plan:1238`
  `inputs=set(col.files)` feeds `:1269-1274` overlap. Pinning retained
  destinations into that same collector before plan generation would
  self-overlap (`dest in inputs` false-positive, or namespace false-positive).
  Therefore P2V keeps **live collector** (P1 `_Collector`: live authority
  inputs only — State/config/Profile/receipt/Gate/staged; retained dests
  never pinned there before plan step) separate from **retained reader**
  (P2R `_Session`-style: retained dests/manifest/KEEP refs pinned with full
  no-follow/alias/regular checks). Cross-binding compares hashes across the
  two stores without merging; untrusted retained files are fully checked, not
  excluded wholesale.

## F3 — exact responsibilities and order

`_pipeline:1291-1492` returns `{proposal, proposed_canonical,
before_canonical, graph, frozen, effective, ...}` (`:1486-1492`) — not
`input_hashes`, not scope, not final receipt. Public `validate:1698-1830`
owns the rest:

1. Pins: config `:1710-1714`, proposal `:1715-1723`, strict State/Profile
   authority **before** canonical dir/tree (`_validated_state_profile_for_tree`
   `:1728`, C4 `:1536-1569`), canonical dir compare `:1729-1741`, layout
   `:1743-1751`, staged `:1752-1753`, description/path prechecks `:1756-1769`.
2. Broad walk only after (1): `tree_entry=_tree_map` `:1770-1771`.
3. `_pipeline` rederivation `:1774-1775`, then ALL-field comparisons
   `:1778-1801` (see F1a).
4. State/Profile reload from pinned bytes `:1802-1808`, optional scope
   `:1809-1812` (`_validate_scope:1635-1695`), then **final FULL receipt
   AFTER scope** (`_final_full_receipt_recheck:1813-1814`, full validator per
   `:1572-1598`, not contract-only), then `col.reverify` + final tree
   `:1816-1821`.
5. Return supplied UNCHANGED + `input_hashes` built here (`:1823-1824` from
   `col.files`) + `measured` (`:1826-1830`).

`prepare:1601-1632` mirrors this (authority `:1616`, tree `:1617-1618`,
pipeline `:1619-1620`, schema `:1621-1622`, final receipt `:1624`,
reverify+tree `:1626-1631`).

P2V orchestration (fixed, read-only):

1. Strict current State/Profile authority before any broad current walk
   (call actual `_validated_state_profile_for_tree`; historical retained
   Profile validity is not current-State validity).
2. Retained same-invocation validation on pinned proposal/manifest bytes
   (provisional dest `:1844-1860` before retained-State read; canonical dir
   `:1901-1925`; inventory/rehash/staged/`capture_inputs`/canonical-bytes/
   final re-inventory).
3. Fresh rederivation via factored DATA-ONLY helpers on live snapshots.
4. Field equality (F1a) + optional scope (existing semantics, F5) **before**
   final FULL receipt recheck.
5. Final pins: re-read every consumed live/retained byte against recorded
   same-byte refs, re-inventory control/edition/retained, HEAD stability,
   close-all. Later helpers may reread live objects, so final checks close
   those windows by comparing to recorded refs — never re-snapshotting
   changed bytes into truth. No global CAS claimed.

## F4 — equality and provenance limits

- Live State byte equality to `basis.state_ref` (via rederived basis equality
  `:1782`) is the bounded choice; no metadata relaxation. Original checkpoint
  (`:355-377`) and active-before (`:380-411`, `ACTIVE_PATH_REBIND :401-402`,
  no filename choice) exact.
- Artifact-only HEAD evolution permitted **only** under the full existing
  predicates — receipt contract equality (`_pipeline:1400-1403`), full receipt
  replay (`_final_full_receipt_recheck`), control/edition pins, `_Collector`
  HEAD stability (`:218-219`), controller pending-basis/head (`control:1838-
  1840`, implementation_sha) — not `git cat-file -e` existence alone (Weekly
  `_verify_head_bytes` proves renderer-commit validity only).
- Same-epoch vs historical fingerprints: P2R-dep entries (`P2R_MODULE`,
  `MANIFEST_SCHEMA :2017-2019`) are historical observations (`:2010-2016`);
  exact hashes enforced only where independently required (plan `:2020-2027`,
  staged/proposal `:2028-2039`, COPY `:1953-1959`, KEEP `:1960-1963`). No
  blanket extra-file equality. Old pins do not transfer to the refactor.
- No whole-history/origin claims: without external monotonic/authenticated
  authority, a coherently restored historical byte set or same-path same-byte
  foreign set cannot be distinguished. Implementation is **forbidden** from
  forging State/deleting retention/rollback-to-pass; that rule is distinct
  from unproved universal anti-rollback detection. P2R refuses
  deleted/incomplete retention (`INVALID_RETENTION`); capture refuses
  preexisting roots (`RETAINED_ROOT_EXISTS`, `:934-945`), but standalone
  readback does not attest creator. Same-byte foreign canonical bytes cannot
  prove creator. No new ledger/role/Gate.

## F5 — result, coverage, budget

- Scope (existing, unchanged): no scope arg, or valid ordinary review with no
  correction block (`_validate_scope:1668-1670` returns `RESULT_REQUIRED`),
  yields NEEDS_SCOPE; invalid supplied review refuses
  (`SCOPE_ORDINARY_INVALID` etc.); WITHIN + exact before
  (`basis.active_reader_input_ref`)/after (reader ref + canonical sha)/
  upstream (`preserved_upstream_digest`) + substantive
  `EDITORIAL_CORRECTION_SCOPE` PASS (`:1673-1695`) binds scope, not promotion.
- P2V return (in-memory observation, strict keys): proposal path+SHA,
  manifest path+SHA, actual live State path+SHA, current observed HEAD,
  optional scope path+SHA, measured digests
  (`before_graph_digest`/`preserved_upstream_digest`/proposed-reader
  sha/graph nodes/edges), consumed `input_hashes`. Names use
  `CURRENT_READINESS_NEEDS_SCOPE` / `CURRENT_READINESS_SCOPE_BOUND`
  (observation-only). Non-durable: never a bearer permission; future writers
  need fresh checks (labels alone cannot prevent misuse — documented).
- Budget: 2A1M/0-schema plausible **only** after this factoring map (helpers
  = data-only derivation/plan/equality; completions fixed; no 600-line
  duplication). New module + new test + changed P1 ⇒ future composite
  **18 paths 3M15A vs 409** (current 16 = 3M13A + 2A), not “18–19”.
  Existing schemas + P2R behavior unchanged.
- Fixture/oracle corrections: real R1-owner fixture (valid predecessor
  pointer via `resolve_active_publication_revalidation`, never “R1-like”
  pointer prose). Persistence-positive/freshness-negative **only** when the
  mutated path is not required KEEP (required-KEEP mutation fails both
  verifier and P2V; mutable COPY-original mutation passes verifier, fails P2V
  freshness). No post-all-checks injection oracle: each late-drift case
  targets a seam **before** a declared later check (e.g., plant between
  retained validation and fresh rederivation, caught by re-pinning + final
  re-inventory), preserving the no-global-CAS limit. Same-byte foreign origin
  is not a compulsory verifier-refusal oracle (F4 indistinguishability;
  takeover forbidden at capture via existence refusal, not readback origin
  proof).

## F6 — factual/attribution corrections

- Withdrawn: `analysis.md` §7 “revalidation rows bind OLD bytes only.”
  Controller `revalidate_publication_surface:1844-1886` supports changed
  surface rows: current-SHA comparison per row (`:1852-1870`: preserved vs
  superseded with `prior/new_sha256`), requires ≥1 regenerated artifact
  (`:1875-1876`), binds rows to checked pending basis (`:1877-1886`), under
  restricted `REVIEWED_CORE_CHANGE` (`:45`, `:1789-1790`). That restricted
  reason is not editorial authority (P1 adds no reason by design `:1-23`).
- `source-binding.md` §§1/8 wording corrected: tool observations and
  transient captures not persisted as raw are **summarized observations**,
  not durable direct raw proof — this includes HEAD/tree/status counts and
  the 16-hash/84-path-set comparisons in §§1–3 (directly observed, honestly
  labeled summary since no raw packet persisted). No new raw packet is
  created solely to repair wording. 84-cache path-set observation stays
  distinct from byte rehash; no cache execution occurred.
- Task is Astra-authored.

## Corrected comparison / call graph / snapshots / cost

| Comparison | Inputs | Predicate source |
|---|---|---|
| Rederived vs supplied | live State/Profile/receipt/Gate/upstream/staged vs proposal fields | `validate:1778-1801` |
| Persistence vs rows | retained State/Profile/COPY/KEEP/staged/manifest vs manifest rows | `verify:1926-2056` |
| Intra-call stability | entry pins vs final re-reads + inventories + HEAD/close | `col.reverify :191-233`; `_Session :243-278,2056-2066` |

Call graph: strict authority → narrow pins → retained validation →
tree snapshot → data-only rederivation → field equality → optional scope →
final FULL receipt → final pins/inventories/HEAD/close → observation.
Control snapshot = config + all consumed live paths (`input_hashes` scope);
edition snapshot = `_tree_map` entry vs final (zero invocation delta);
retained snapshot = expected-sets closure + rehash (entry vs final).

Cost: 2A1M/0-schema (one small module + one focused test + private P1
factoring with fixed completions; affected regressions only, no suite
transfer). No blocker found for this bounded observer; full
staged-review/materialization/receipt/Gate/QA/reason/State promotion stays
unselected and is not required for P2V. Whole NOT_READY, step4/B3 OPEN,
canonical audit unstarted, DM021 OPEN.
