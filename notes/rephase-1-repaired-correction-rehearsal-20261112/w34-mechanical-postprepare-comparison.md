# W34 mechanical post-prepare comparison — independent data reviewer (DATA only)

Role: NEW independent mechanical/data reviewer, not content reviewer/operator.
Method: stdlib only (`json`/`hashlib`/`pathlib`/`OrderedDict`); read/hash/parse allowed.
No runtime/project imports, tests, Git, network, Production, active writes, subagents.
No source validator loosening. No content-review reconstruction.
Existing W34 decision `c7ba…` held — not approval to adopt.

Machine companion: `w34-mechanical-postprepare-comparison.json` (full per-file hashes, per-row diffs).

## 1. Refs verified from actual bytes

Runtime: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`
epoch `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325`, parent e84.

Old active (CP `0979f9f7703a25c2bd3424824bc4ad9f8719e8e7bcc49c19c5573d0f70ab593a`):

- `evidence/v2/accepted/5ca6f31033dcaed6a153f0eb6f838f18bc9bdd1674a19a941f8c8378f88e4e48/evidence-accepted.json`
  `edf21e4de5f7ab8d2bd5189f45abc8cc6d0cf6475e532b20bcc56b0ce5660218`/126592
- `evidence/v2/views/accepted/574b96ff3ce87f7f2e46fcd78724bf1fbfcdad590e009be1500f03446697b5c5/edition-views-accepted.json`
  `3777133cc09d0189ab97cc1d8ff1f8b420108d43880f69f1745356508b8acfce`/159498
- `sources/2026-W34/materiality-ledger-v2.json`
  `f089cc4eedb49a81b4b925c1219f22a77237d16f28fdee73f20a3744e725e91d`/186202
- `sources/2026-W34/profile-completeness-v2.json`
  `e8c432dd6275e81df5286cb8c0d55d99e27aa0812c52a114d870dddaf0d2795f`/71532

New prepared (manifest `54de43edc49a24e2fd8ffaf02144a83c5812a2c59290eb1d3a914709e8583da2`/438583):

- `research/v2/acceptance-revisions/w34-repaired-20261112-r1/revision-manifest.json`
  `54de43edc49a24e2fd8ffaf02144a83c5812a2c59290eb1d3a914709e8583da2`/438583
- `research/v2/acceptance-revision-inputs/w34-repaired-20261112-r1.json`
  `057e186fbda8df8f58fd400def30cf5a6a80ba1d310f161f1854882619f1e5a3`/1434802
- `candidate/materiality-ledger.json`
  `523df63c91339524c6d292b20866b850894d2e36a35e876d9ca8eea38ada9202`/186214
- `candidate/profile-completeness.json`
  `d9c455dac0bd05f88edcf26991b8e6cb33b4fe3f4a98d6e8dcf2c825c7f0941d`/71532

Affected: `w34-event-arxiv-2608-15127`, `16096`, `18389`, `21100`
(4 task files: `task-ef1d67ce…`, `task-4fe332e9…`, `task-56725e60…`, `task-f49a436a…`).

Root resolution read: `astra-operation-resolution.md` FULL §§1–7
(manifest 54de43…, 409 tasks, old four refs unchanged, semantic review pending).

## 2. Results — 409 cards (`results/task-*.json`)

| scope | total | byte_equal | byte_differ | parsed_equal | parsed_differ |
|---|---|---|---|---|---|
| all | 409 | 0 | 409 | 405 | 4 |
| unaffected 405 | 405 | 0 | 405 | 405 | 0 |
| affected 4 | 4 | 0 | 4 | 0 | 4 |

Filenames identical old vs new (409/409 set-equal).

Unaffected 405 — hash≠ but docs==, exact field/order diff:

- Parsed JSON `==` (strict `json.loads` equality, order-insensitive).
- Bytes `!=` for 405/405. Top key order identical.
- Sole difference: `entities[0]` key order.
  - Old universal 409/409: `entity_id, canonical_name, entity_type, organization, canonical_url`
  - New universal 409/409: `canonical_name, canonical_url, entity_id, entity_type, organization` (alphabetical)
  - No value difference. No other key order difference.
- Example `task-0129bae24406796541d6.json` (unaffected, `w34-event-arxiv-2608-15762`):
  old `4ac6322b33bbf16fa5cf813e697a9f7f33a5026c229572d26ce1fec2ed34fe4f`/6604B,
  new `61398a6c40af0dcddaf6d2883a2544abdc33133b8cf9ecf58cc1d0a8e725df2a`/6604B,
  same length, first byte diff at offset 565, 252 differing bytes all inside entity block.

Affected 4 — parsed differ (genuine correction + same mechanical reorder):

- `claims[0].text/context`: old `"… proposes … Title: Content selection saved."` + generic context
  → new literal spans (`15127` agentic sentence, `16096` retrieval sentence,
  `21100` MLLM sentence, `18389` code-agent sentence with `\n`).
- `claims` other indices / `verification.targets[].finding`: updated body refs (§§, protocol details).
- `limitations`: 2→3 rows, maker-reported wording tightened, parsing-observation removed.
- `status` unchanged (`PARTIAL`), `entities` IDs unchanged, entity order still alphabetical in new.

## 3. Views — 409 (`views/view-*.json`)

| scope | total | byte_equal | parsed_equal | detail |
|---|---|---|---|---|
| all | 409 | 0 | 0 | 409 parsed-differ |
| unaffected 405 | 405 | 0 | 0 | 405/405 differ ONLY in `evidence_sha256` |
| affected 4 | 4 | 0 | 0 | `evidence_sha256` + `materiality` + `profile_annotations` |

Top key order identical 409/409:
`schema_version, issue_id, research_profile, evidence_task_id, evidence_sha256, materiality, scope_dimensions, profile_annotations`.

Unaffected 405:

- `evidence_sha256` differs (new = sha256 of new card bytes, see §6).
- All other fields identical: `materiality.status/rationale`, `scope_dimensions`,
  `profile_annotations.{why_this_issue,window_relation,carry_over}`.
- Example `view-0129bae24406796541d6.json` (same task as above):
  len 844/844, file sha old `2686dc95…` vs new `06a16f0e…`,
  `evidence_sha256` old `4ac6322b…` (old card) vs new `61398a6c…` (new card),
  materiality `CONTEXT` rationale identical.

Affected 4 — exact diff fields `['evidence_sha256','materiality','profile_annotations']`:

- `evidence_sha256`: new card sha (mechanical).
- `materiality.status`: `CONTEXT`→`MATERIAL`; `rationale`: provisional generic
  → box/sidebar SUPPORTING note (P2/P1/P4/P2 destinations per dossier).
- `profile_annotations.why_this_issue`: same rationale change;
  `window_relation=MAIN_EVENT`, `carry_over=false` preserved.
- `scope_dimensions` preserved.

## 4. Tasks — 409 (`tasks/task-*.json`)

409/409 byte-identical and parsed-identical (including 4 affected task files).
`discovery_ids`, `source_records`, `verification_targets`, `screening_basis` preserved.
Package task derivation intact; correction lives in request records, not tasks.

## 5. Ledger — 439 rows (`materiality-ledger-v2.json`)

Whole file: old `f089cc4e…`/186202 vs new `523df63c…`/186214 (delta +12B).
Parsed whole-file `!=` (expected, 4 rows changed).

Per-row by `discovery_id` (keys identical 439/439):

- parsed_equal 435, parsed_differ 4.
- Unaffected 435 incl DROP: 435/435 identical.
  Preserved: 4 `DUPLICATE` rows with `screening_decision=DROP`
  (`c042/c067/c069/c070` grok-build/dogwood/nemotron) + 354 `CONTEXT`,
  41→45 `MATERIAL` delta is only the 4 affected, 26 `EXCLUDED`, 10 `HOLD`.
- Affected 4 — exact 3 fields each:
  `downstream_disposition: CONTEXT→MATERIAL`,
  `evidence_view_statuses: [CONTEXT]→[MATERIAL]`,
  `rationale: Screening=…; Edition View=CONTEXT → …MATERIAL`
  (`KEEP`/`INSPECT` screening prefix preserved).
  `+1` char per field (`CONTEXT`7→`MATERIAL`8) ×3 fields ×4 rows = +12B matches file delta.

## 6. Source chain — confirmed from actual bytes/key order, not hypothesis

- Dispatch: `prepare-normal-high-r3.py:797`
  `json.dumps(request, sort_keys=True, separators=(",",":"), …)+b"\n"`.
  Actual `request.json` is compact sorted: no newlines, alphabetical top keys,
  alphabetical `records[].entity` (`canonical_name, canonical_url, entity_id, entity_type, organization`).
- Base: `interactive-evidence.json` is pretty `indent=2` original order:
  `entity: entity_id, canonical_name, entity_type, organization, canonical_url`.
- Card core: `survey_evidence_v2.py:2246` `entity=dict(record["entity"])`
  preserves request insertion order (alphabetical), no re-sort.
- Bytes: `survey_production_v2.py: json_bytes=json.dumps(…, indent=2)+"\n"` (NO `sort_keys`,
  preserves insertion order).
  → New cards pretty alphabetical vs old cards pretty original: same values,
  reordered keys, same length for unaffected.
- Views: `survey_research_authority_v2.py: card_raw=core.json_bytes(card);
  card_sha=sha256(card_raw); view=build_research_view_content(profile, task_id, card_sha, rec)`.
  → Card reorder changes card sha, changes `view.evidence_sha256` even when other view fields identical.
  `validate_edition_view` requires `view.evidence_sha256==evidence sha`; strict unaffected predicate rightly refuses.

Completeness note (out of 405/439/409 scope, recorded for provenance):
same 3 obligations content-identical by ID, order rotated
(old `current-relevance, technical-significance, carry-over` vs new `carry-over, current-relevance, technical-significance`),
`basis.materiality_ledger_sha256` updated old `f089…`→new `523d…`; bytes same length 71532, hash differs.

## 7. Prior content-return claim — rejected, no report files found

Claim in `w34-supplied-decision-r1.json:assessment`
(`405 results exact-identical, 405 views preserve … with only mechanical evidence_sha differing`):

- Searched packet for post-prepare content/delta report files: none found (only dossier, pins, patch, execution reports, decision).
- `REJECT` as logically ambiguous/false:
  - 405 results are NOT byte-identical (0/405 byte-equal, 0/409 overall) but ARE parsed-identical (405/405).
  - 405 views are NEITHER byte-identical (0/405) NOR parsed-identical (0/405 parsed-equal; 405/405 differ in `evidence_sha256`).
- Do not trust phrasing; use §§2–3 + JSON details.

## 8. Verdict — NEW corrected request/R needed, not shipping defect

`NEW request serialization corrected + NEW R required; NOT a producer/validator shipping defect.`

- Producer correctly preserves request order and hashes exact bytes; validator correctly
  enforces `evidence_sha` binding. Do NOT loosen source validator. Strict refusal is correct.
- Root cause is request canonicalization (`sort_keys`) alphabetizing entity/record keys
  vs original base order. Fix is order-preserving request serialization, then regenerate R.
- Tasks 409/409 identical + ledger unaffected 435/435 identical prove no task/ledger corruption;
  drift is purely mechanical key-order + derived sha, plus 4 genuine MATERIAL promotions.
- Required next: author NEW request preserving base interactive key order
  (no `sort_keys` alphabetization of `records`/`entity`), single HIGH prepare to NEW revision id,
  re-run this mechanical comparison (expect 405 byte-equal+parsed-equal, 4 semantic diffs only).
- Not required: producer/validator change, R4/generic-reader/PDF/Production/State mutation.
- `c7ba…` content decision held, not adoption approval.

Stop at Human Commit Point. Ordinary Commit/Push Human-owned.
