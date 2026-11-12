# Actual DM022 supplement operation map (source-grounded)

Read-only source inspection of the active e84 candidate-work tree. No execution,
imports, tests, network, Git, Production checkout, or active writes. This map
supersedes the earlier applicability note's §4.2 “LOW direct + HIGH
coordination” normal-path claim; that note remains preserved as historical
synthesis and is not copied. No B2/B4 precode cycle, generic reader, new module,
or source edit is proposed here.

`CW` = `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work`.

## 1. Verdict

**NO actual supported normal `prepare_revision → adopt_revision` route currently
carries an Evidence Authority Supplement.**

- HIGH `prepare_revision` has no package/supplement override and always calls
  the LOW package builder.
- LOW `build_revision_package_from_paths` builds tasks from Discovery/Screening
  and copies only the OLD package `prompt`/`contracts`; it does **not** copy
  `authority_supplement` or task `authority_supplement_source_ids`, and ignores
  `request.supplement_manifest`.
- LOW `build_revision_cards_views_from_paths` resolves supplement context from
  the **package** `authority_supplement`; with the HIGH-generated package that
  context is empty, so cards are Discovery-only or fail if request
  `source_bindings` names a supplement ID.
- HIGH `adopt_revision` consumes the prepared manifest/candidate outputs; it
  has no package override and no supplement path.
- The manifest/proof/retention schemas do not compose a supplemented HIGH
  candidate: manifest has a nullable `candidate_outputs.supplement_manifest`,
  but proof `proposed` has no supplement field and retention covers only the
  seven canonical slots, not supplement Raw.

**YES only for the lower direct LOW unit path**: a manually supplemented
package + request with schema-valid `source_bindings` can drive
`build_revision_cards_views_from_paths` / `accept_revision_evidence_views_from_paths`.
That path is tested, but it is not HIGH prepare/adopt and is not an operational
State-adoption composition.

## 2. Actual call graph and signatures

HIGH (`survey_prearchitecture_acceptance_v2.py`):

| item | line |
|---|---|
| `prepare_revision(repo_root, state_path, request_path, revision_id)` | 456 |
| calls `low.build_revision_package_from_paths(repo_root, request_abs, state_copy, rev_root / "candidate")` | 636 |
| writes candidate package | 638 |
| writes tasks | 639-641 |
| calls `low.build_revision_cards_views_from_paths(repo_root, rev_root / "candidate/package.json", request_abs, results_dir, views_dir, before_copy_path=state_copy)` | 651 |
| writes cards/views | 658-664 |
| manifest `candidate_outputs.supplement_manifest = request.get("supplement_manifest")` | 786 |
| `adopt_revision(repo_root, state_path, revision_path, decision_path)` | 1100 |
| adopts manifest candidate outputs / proof / report / checkpoint | 1128-1296 |

CLI (`main`, lines 1483-1521) exposes only:

```text
prepare --repo-root --state-path --request-path --revision-id
adopt   --repo-root --state-path --revision-path --decision-path
resume  --repo-root --state-path --revision-path
readback --repo-root --state-path [--revision-path]
```

There is **no `--package`, `--supplement`, `--supplement-manifest`, or package
override** on prepare/adopt.

LOW (`survey_research_authority_v2.py`):

| item | line |
|---|---|
| `build_revision_package_from_paths(repo_root, request_path, before_copy_path, output_dir)` | 2128 |
| loads request; COPY SHA bind | 2150-2155 |
| loads OLD previous checkpoint and OLD package | 2159-2177 |
| derives tasks from effective Discovery + Screening | 2183-2228 |
| validates tasks | 2231-2242 |
| package `prompt` / `contracts` taken from OLD package only | 2257-2258 |
| package/task fields + return | 2243-2274 |
| `build_revision_cards_views_from_paths(repo_root, package_path, request_path, results_dir, views_dir, *, before_copy_path)` | 2277 |
| loads package / validates basis | 2314-2348 |
| `_resolve_phase_supplement_context(repo_root, package, implementation_sha=None, screening_acceptance=None, discoveries=None)` | 2350-2355 |
| per-task source merge + `_build_card_core` | 2399-2403 |
| request `source_bindings` must select a source authority | evidence `_build_card_core` 2243-2247 |

Critical source facts:

- `build_revision_package_from_paths` reads OLD package only at `2172-2177`
  and copies only `old_pkg_pkg.get("prompt")` / `old_pkg_pkg.get("contracts")`
  at `2257-2258`. It does **not** read `old_pkg_pkg.get("authority_supplement")`.
- Task construction at `2211-2228` sets `source_records`, `verification_targets`,
  and `screening_basis`, but no `authority_supplement_source_ids`.
- Its package dict at `2243-2265` has no `authority_supplement` and no
  supplement contract extension.
- `request.supplement_manifest` is not referenced by this function; only the
  HIGH manifest records `request.get("supplement_manifest")` at `786`.
- `_resolve_phase_supplement_context` returns a legitimate empty context when
  `package.get("authority_supplement")` is absent
  (`survey_evidence_v2.py:322-330`). With the HIGH package, it is empty.
- `_build_card_core` requires `record.source_bindings` to name task-bound
  sources (`survey_evidence_v2.py:2243-2247`). A request binding to
  `supplement-src-*` therefore fails when the package has no supplement
  authority; without `source_bindings`, the card defaults to `src-1`
  (Discovery only).

## 3. Actual schemas

- Request: `schemas/dm022-revision-request-v2.schema.json`
  - `supplement_manifest` is required and may be `null` or `SizedRef`
    (lines 7, 37).
  - No package body / `authority_supplement` override field.
- Manifest: `schemas/dm022-revision-manifest-v2.schema.json`
  - `candidate_outputs` requires `package`, `tasks`, `cards`, `views`,
    acceptances, ledger, completeness, and `supplement_manifest`
    (line 37).
  - `supplement_manifest` may be null or `SizedRef` (line 47).
  - Retention snapshots are exactly seven canonical slots (line 28).
- Proof: `schemas/dm022-revision-proof-v2.schema.json`
  - `proposed` requires package/tasks/cards/views/acceptances/ledger/
    completeness and digests (line 16); it has **no** `supplement_manifest`
    field.
  - Proof validation therefore carries supplement authority only if the NEW
    package itself carries `authority_supplement`; there is no separate proof
    row.
- Retention: seven-slot `retention_snapshots` only. Supplement Raw files are
  not retained by the HIGH prepare inventory; direct LOW supplement validation
  reads the manifest-declared `raw_path` at its existing path.
- Package/task schemas: `evidence-v2-run-package.schema.json:12,99` and
  `evidence-v2-task.schema.json:15` define the supplement authority/task IDs
  that the HIGH package builder never sets.

## 4. Test-proven scope

The direct LOW supplemented case is tested, but explicitly not as HIGH
threading:

`tests/test_evidence_scaling_v2.py:1266-1475`:

- docstring `1266-1277`: HIGH prepare threads the **unsupplemented** revision
  package; LOW card supplement binding is covered via the shared core/unit
  probe, “not claimed as HIGH-threaded here.”
- `1374-1384`: explicit “Pre-existing HIGH producer limitation”: HIGH
  `build_revision_package_from_paths` never carries `authority_supplement`;
  `_build_request_and_decision` sets `supplement_manifest: None` and no
  `source_bindings`; HIGH prepare/adopt threads the unsupplemented package.
- `1385-1423`: test manually copies the HIGH package and adds
  `authority_supplement`, supplement contract/rule, task
  `authority_supplement_source_ids`, and request `source_bindings`.
- `1428-1454`: direct LOW `build_revision_cards_views_from_paths` +
  `accept_revision_evidence_views_from_paths` on that manually supplemented
  package.
- `1467-1475`: `high.adopt_revision` is called on the **original unsupplemented
  revision** (not the supplemented `supp-candidate`), then readback/check.

Full HIGH prepare/adopt tests use unsupplemented requests:

- `tests/test_dm022_prearchitecture_acceptance_v2.py:615` —
  `"supplement_manifest": None`.
- `tests/test_dm022_full_lifecycle_v2.py:486` —
  `"supplement_manifest": None`.

Thus:

- **LOW direct supplemented package + direct LOW card/view/acceptance**: yes,
  unit-tested.
- **HIGH prepare + HIGH adopt with supplements**: no test and no producer
  wiring; the existing test deliberately says so.
- The test's later HIGH adopt does not adopt the supplemented products.

## 5. Current W34: affected bodies are supplement-only, not Discovery-bound

Current W34 accepted package:

`CW/sources/2026-W34/evidence/v2/accepted/5ca6f31033dcaed6a153f0eb6f838f18bc9bdd1674a19a941f8c8378f88e4e48/`
package 157429B SHA `0ec312b4b66435ee09c34f982b39bf126710edb2c853d6b2915733a7fe25652c`;
Evidence `edf21e4d…` 126592B.

Current package has:

- `authority_supplement` =
  `sources/2026-W34/external/evidence-supplement/evidence-authority-supplement-r2-fresh-basis.json`
  389414B SHA `ce6f977a3e690e779c380b7b035d9247207e262b5c50a5b14b6b6b8f0fbc704e`;
- **401** task records with `authority_supplement_source_ids` of 409;
- **8** task records without supplement IDs;
- supplement manifest 428 sources.

The 4 affected arxiv-body IDs:

| DID | task | supplement source ID | current card sources | body already in supplement |
|---|---|---|---|---|
| `w34-event-arxiv-2608-15127` | `evidence:2026-W34:8fab99aa7093acb9` | `supplement-src-6f78fb828e6ec113` | supplement only | `.../evidence-bodies/arxiv/2608_15127.html` 314048B `85c70376…` |
| `w34-event-arxiv-2608-16096` | `evidence:2026-W34:5841bec7775ece26` | `supplement-src-c980beaaa7c4448a` | supplement only | `.../2608_16096.html` 414077B `a4c2aafe…` |
| `w34-event-arxiv-2608-21100` | `evidence:2026-W34:b6357aec74216e97` | `supplement-src-70c044a81cc5695d` | supplement only | `.../2608_21100.html` 711224B `da737a85…` |
| `w34-event-arxiv-2608-18389` | `evidence:2026-W34:0dd05128103b336c` | `supplement-src-c54d707262dc6b1b` | supplement only | `.../2608_18389.html` 388712B `56b48291…` |

Optional `2608-21095` is also supplement-only (`supplement-src-061d52789b50ef36`;
197521B `a48cacf8…`). The Discovery locator exists in task
`source_records`, but the card `sources` and record `source_bindings` select
only the supplement source. They are **not Discovery-bound**.

Consequence for full409:

- 401/409 cards require supplement refs.
- The 4 affected are within those 401; 397 unaffected supplement-bound cards
  plus 8 Discovery-only unaffected cards remain.
- HIGH prepare builds a package with **zero** supplement refs; cards become
  Discovery-only (or prepare fails if request `source_bindings` still names
  supplement IDs).
- `prove_revision_from_paths` compares every unaffected old/new card and refuses
  semantic drift (`survey_research_authority_v2.py:3354-3388`). The 397
  unaffected supplement-bound cards would differ from Discovery-only new cards.
- Therefore HIGH prepare/adopt cannot produce a valid full409 revision with the
  current package/card authority, even though the 4 bodies already exist in the
  W34 supplement manifest (no new archive needed for those bodies).

## 6. Current SP: D141 supplement-bound, D142 Discovery-only

Current SP accepted package:

`CW/sources/SP-efficient-llm-2026/evidence/v2/accepted/73f4bc1ec69c70925a7119a0327ff5e6f024812b56cf8edd7c49eae9f672a297/`
package 50279B SHA `4f6b9bdad089d88e12cbe96b1a80020d1dedb82da9afc33c752f6713c02789b5`.

- `authority_supplement` =
  `sources/SP-efficient-llm-2026/external/evidence-supplement/evidence-authority-supplement-r6-sp17-20261104T162747Z.json`
  30922B SHA `ffcd0a7eefdcf81700bd81982031ccbf7e8895835f55609eac772c40946fc4b3`.
- **28** supplement-bound tasks of 160; 30 manifest sources.
- `EFF-D141`: task supplement ID `supplement-src-95365faf9fae84f7`; card
  source only that supplement; body
  `sp17-models-current.html` 219035B `59b6c17b…`.
- `EFF-D142`: **no** task supplement ID; card source `src-1` from Discovery;
  no body.

Thus a new D141 archive would need replacement in the existing supplement
manifest; a new D142 archive would need a **new** supplement source (D142 is not
currently supplement-bound). Either requires the HIGH producer to carry
`authority_supplement` and task `authority_supplement_source_ids`, which it does
not. Full160 adoption would also lose the other unaffected supplement-bound
cards (27 or 28 depending on affected set), and proof would refuse their
semantic drift. `EFF-D142` with a new archive cannot be carried by the existing
normal route; it is blocked unless the source/producer capability is extended.

## 7. Answer to the operation question

### YES — existing lower direct calls only

On a **manually supplemented package** (the test's `supp-candidate` pattern):

- `low.build_revision_cards_views_from_paths(repo_root, supp_pkg_path, supp_request_path, results_dir, views_dir, before_copy_path=copy_path)`
- `low.accept_revision_evidence_views_from_paths(repo_root, supp_pkg_path, results_dir, views_dir, profile_path, evidence_accepted_root, views_accepted_root, request_path=supp_request_path, before_copy_path=copy_path)`

with `supp_package["authority_supplement"]`, supplement contract/rule, task
`authority_supplement_source_ids`, and request `source_bindings` already set.
This is unit-supported (`test_evidence_scaling_v2.py:1385-1465`), but it does
not include HIGH prepare/manifest/proof/adopt.

### NO — normal HIGH prepare/adopt composition

- No existing caller/CLI package override for `prepare_revision`.
- No copy of OLD `authority_supplement` or task supplement IDs.
- No use of `request.supplement_manifest` by the package builder.
- No package authority for card supplement context.
- No `supplement_manifest` in proof `proposed`; retention has only seven slots.
- HIGH adopt consumes the unsupplemented manifest/candidate outputs.
- Current W34/SP full revision sets contain 401/28 supplement-bound cards;
  unaffected proof comparison would fail.

**Missing capability:** HIGH revision-package supplement carry + task IDs +
package/authority contract + manifest/proof/retention integration. This is a
producer/contract gap, not a generic-reader/B2/B4 issue and not a new module
proposal. No source edit or implementation is selected here.

## 8. Explicit known unknowns

- Whether an authorized future change could extend HIGH package carry without a
  new contract: unknown/not present; no such source exists now.
- Whether a manually constructed supplemented HIGH revision could pass
  `prove_revision_from_paths` and adopt: not tested; current public calls do not
  construct it, and manifest/proof/retention do not bind its supplement
  authority/raw retention.
- Whether the W34 4 affected bodies would pass a fresh independent semantic
  review: not assessed here; they are already retained in the W34 supplement
  manifest.
- Whether D142 has any acceptable historical/current body outside the
  authorized captures: unknown; not fetched/claimed.

No execution, test, fixture, network, Git, Production, or approval was
performed.
