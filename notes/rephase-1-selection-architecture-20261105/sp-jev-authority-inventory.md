# SP Jev / System One captured-authority inventory

Read-only DATA inventory, independent of the SP proposal reviewer. No new
fetch, network, Git, current-main, Production checkout, runtime tests/imports,
or project execution. Scope is the active e84 source and the cited packet
captures only; this is **not** a whole-Production-corpus absence proof.

`CW` = `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work`.

## 1. Bottom line

- EFF-O10 is mandatory, and the SP temporal policy is
  `OPEN_HISTORY_AS_OF = 2026-09-21T16:10:00Z`
  (`CW/sources/SP-efficient-llm-2026/production-profile.json`, 13748B,
  SHA256 `aff05fd573ce873afa24c0ede26c2b4591ee28b7048c9ed528e8fc389ed8ee45`).
- Within the authorized captures, **there is no full-body, pre-2026-09-21
  TypeSafe/System One capture**. The available historical material is a
  2026-09-21 **agent summary** (`SUMMARY_CAPTURED`), not a publisher body or a
  version-pinned revision.
- The full TypeSafe bodies that do exist are **2026-11-01 current observations**
  (`sp17-launch-current.html`, `sp17-concepts-current.html`,
  `sp17-models-current.html`) and are explicitly classified current-only /
  historical UNCONFIRMED.
- **D142 has no captured body at all.** Its only existing record is a
  summary-level card; it cannot establish API schema fields, confidence
  derivation, version/date, or historical state.
- The five living-document current-only rows in the proposal are
  D004, D070, D071, D141, D163. Jev-specific current-only rows are
  **D070, D071, D141**; **D142 is separate summary-only support**, not a
  current-only full body.
- The proposal's own dossier says O10 remains LIMITATION and no 09-21 VERIFIED
  claim is made (`sp-human-dossier-draft-ja.md:35,48`). That is the honest
  ceiling from existing captures. If O10 must become as-of historical
  VERIFIED, new historical access is required.

## 2. Current accepted Evidence cards

Latest CP: `sources/SP-efficient-llm-2026/orchestration/v2/checkpoints/CANDIDATES_NORMALIZED.json`
SHA256 `1233b1f6ca3301d6430d4d157788d0a45a613c9ce1e1563e7c06fe11d73993f0`
(4745B). The accepted Evidence package is:

`CW/sources/SP-efficient-llm-2026/evidence/v2/accepted/73f4bc1ec69c70925a7119a0327ff5e6f024812b56cf8edd7c49eae9f672a297/`

Pins:

| file | bytes | SHA256 |
|---|---:|---|
| `evidence-accepted.json` | 49237 | `65784e69559f9379412935fa5e7671beddee59b46b8fdb28a848d450e2b68ce0` |
| `package.json` | 50279 | `4f6b9bdad089d88e12cbe96b1a80020d1dedb82da9afc33c752f6713c02789b5` |
| `interactive-evidence.json` | 355643 | `697a4ed088b76f18b3859568a735491a3a8b2295c480be3e1e678c4d8b31f104` |

Cards (all current accepted status):

| DID | card path (under `results/`) | bytes | SHA256 | status |
|---|---|---:|---|---|
| EFF-D070 | `task-b8b9f70aa257d5359768.json` | 7468 | `6090eee4c3b2ffd2ac9f2c81f726c06a946d11869f35d2b18cbe5aed6a532579` | PARTIAL |
| EFF-D071 | `task-cc12f66d1bfb44ff872d.json` | 5972 | `bc7dedb1d85cb77ae67449cbcab3d9258b2f914eefae06fed7bc3284394f8c5b` | PARTIAL |
| EFF-D141 | `task-4700b268375ef45d48a6.json` | 6321 | `aad7cc3f311d22f91e6e8252290c5d27ef88770c610b2766a223901d727612e4` | PARTIAL |
| EFF-D142 | `task-21ce0892d8846adffd6b.json` | 3681 | `7d7d26d454bf9f982696bb3a622f6c13b3116135eba9f1403639b9b998f9ca8b` | PARTIAL |

Current cards explicitly say previous VERIFIED-without-body was corrected to
PARTIAL/UNRESOLVED historical (D070/D071/D141) per
`reviews/evidence-efficient-llm-review-20261101T113240Z.md` §§3-3–3-5.

## 3. Historical summary capture (2026-09-21)

The only captured "historical" Jev material is the discovery observation file:

`CW/sources/SP-efficient-llm-2026/raw/discovery-observations-d10-specialization-jev.md`
4453B, SHA256 `0b8bd0ab6804ba0fd31f9e5a6a647a738d101be33ef69b9d80bcaaabc00e87ce`.
Header: `collector_run: efficient-llm-discovery-r1 | observed: 2026-09-21`.

Relevant rows:

- **S70 / EFF-D070** — launch; locator
  `https://typesafe.ai/blog/introducing-system-one-models-and-jev`;
  `published: 2026-09-15` is a Discovery claim; retrieval
  `SUMMARY_CAPTURED`. Records new architecture, parallel sampler, RLCD, typed
  outputs, 70–500 ms, $0.042/MTok, 193.6x/444.6x vendor claims, vendor
  quarantine.
- **S71 / EFF-D071** — docs; `published: 2026-09` living docs; captured
  2026-09-21; `SUMMARY_CAPTURED`. Records Choice/Score/Noul, parallel,
  group-level calibration caveat, text-only/atomic-question limits, early
  access/waitlist.
- **S72 / EFF-D072** — Jev wiki; `published: 2026-09-19`; secondary; 1.13
  model-card facts; not specification authority.
- **S73 / EFF-D073** — awesome-jev community hub; `published: 2026-09-17`;
  community reproduction leads only; **no peer-reviewed reproduction located**
  in that pass.
- **S74 / EFF-D074** — DataCamp explainer; `published: 2026-09-19`; secondary
  corroboration of early access/waitlist and $0.042/M input; technical facts
  must rebind to TypeSafe.

Second historical summary file:

`CW/sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g19-g20-data-jev.md`
3751B, SHA256 `f7eeec6872fa7dd9ad8f8fb08beadfb9e2ff2bab571ffff807c2d34718672662`.
Header observed 2026-09-21; contains:

- **S141 / EFF-D141** — `Jev 1.13 official Models page`; `published: null`
  (living docs; captured 2026-09-21); `SUMMARY_CAPTURED`. Records `jev-1.13.0`
  current, aliases to 1.13, 64k/32k, 250k tok/s, 1200 req/min, input-only
  billing, no per-account tuning, RLCD remains a name.
- **S142 / EFF-D142** — `TypeSafe API reference`; `published: null`; captured
  2026-09-21; `SUMMARY_CAPTURED`. Records answer schema + distribution-derived
  confidence, **no benchmark/calibration protocol**, and
  `INDEPENDENT_EVIDENCE_NOT_FOUND_AS_OF_2026-09-21`.

These are historical **observations/summaries**, not full publisher bodies.
They support "as recorded on 2026-09-21" but not "this was the publisher's
2026-09-21 body/revision."

Initial P2 accepted/input captures are also historical but superseded:

- `notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2b23.evidence-accepted.json`
  49241B, SHA256 `72ba3407b63161c58d7f4c6a9c0c1db65f9fc26c498b781322e3f88b376a3047`;
  D070/D071/D141 = **VERIFIED**, D142 = PARTIAL.
- P2 proposed inputs:
  `DATA.p2c01.interactive-evidence.json` 313083B,
  SHA256 `6cac92b1a51e109a9596752d60263e7341506025211cca8dc619fa80f4229c85`;
  `DATA.p2c03.interactive-evidence-r2.json` 311908B,
  SHA256 `8cff1a0e39f881c1d8d6c0ec3c4501268f90e81011493463b82d0d5489849091`.
- P1/P2 input archives:
  `execution-20261101T025600Z/input-archive/SP/interactive-evidence-adapted-O13-15.json`
  346320B, SHA256 `00ab6bbb7ae423df6ab45cb934c13fdeaed61cda52a2503da94f5c283207d6e0`;
  r2 archive 345202B,
  SHA256 `f46dcf2f43ebed472d309d40a70ddba8f402193eeca99787791636442ba29958`.

Those initial VERIFIED statuses were **not backed by durable bodies** and were
corrected by review `evidence-efficient-llm-review-20261101T113240Z.md`
(34848B, SHA256 `8d67b704aee79b54e33f90ab0a094f3c1a7f7bbec1be048abf606e0eb06f9fc7`),
§3 rows 3–5: `CHANGES_REQUIRED`, repair to PARTIAL + `NEEDS_MORE` /
`AUTHORITY_NOT_FOUND`. Do not resurrect those initial VERIFIED labels.

## 4. Current full bodies (2026-11-01) — current-only

Publisher intake:
`notes/rephase-1-operational-rehearsal-20261101/publisher-intake-20261101T163426Z/`
manifest 69160B,
SHA256 `5432a05ee8a2447fc5e63e44422a84718bde04502b3aaac6d102633e55e2de50`.

| DID | body | bytes | SHA256 | HTTP date / Last-Modified | classification |
|---|---|---:|---|---|---|
| D070 | `DATA.sp11-launch.html` | 270966 | `278478f09f3df3c2987dba4c7620ef7b842fed1c1e13f362e3a11d3713c21de9` | 2026-11-01T16:35:40Z / 2026-10-28T06:35:51Z | current-only / mixed internal date |
| D071 | `DATA.sp12-concepts.html` | 165512 | `b58d91ae23784860dd4083c04ca51b1a382b9c045c54af053085c0e0bfe3540d` | 2026-11-01T16:35:41Z / 2026-11-01T03:12:59Z | current-only |
| D141 | `DATA.sp13-models.html` | 219035 | `59b6c17b12d3cb8ac781abdf5f9b52888ce336d840d35c49cc9c1f9ec9286e60` | 2026-11-01T16:35:41Z / 2026-11-01T02:48:04Z | current-only / 1.14 drift |
| D142 | — | — | — | — | no body captured |

Identical current-body copies also exist at
`CW/sources/SP-efficient-llm-2026/external/evidence-supplement/raw/sp17-launch-current.html`
and `sp17-concepts-current.html`, `sp17-models-current.html` (same
bytes/SHA). The supplement that binds them:
`CW/sources/SP-efficient-llm-2026/external/evidence-supplement/evidence-authority-supplement-r6-sp17-20261104T162747Z.json`
30922B,
SHA256 `ffcd0a7eefdcf81700bd81982031ccbf7e8895835f55609eac772c40946fc4b3`.

Date precision/body-vs-metadata:

- **D070 launch**: current body contains **both**
  `date`,`2026-09-15T00:00:00.000Z` (CMS field) and a visible
  `<!-- Published Oct 28, 2026, 6:35 AM UTC -->`; also Framer
  `ssr-released-at 2026-10-27T16:00:13.417Z` /
  `page-optimized-at 2026-10-28T06:35:50.853Z`; HTTP Last-Modified
  2026-10-28. The 09-15 field is not a version pin. It does not prove a
  2026-09-15 or 2026-09-21 revision;   the current page is a mixed/current
  observation. The Oct Last-Modified is not disproof of an earlier
  publication, but it is also not proof of the 2026-09-21 body.
- **D071 concepts**: body `dateModified:"2026-10-14T21:07:12.427Z"`; no
  `datePublished`; HTTP Last-Modified 2026-11-01. Current-only.
- **D141 models**: body `dateModified:"2026-11-01T02:39:33.379Z"`; HTTP
  Last-Modified 2026-11-01; table now shows **both** `jev-1.14.0` and
  `jev-1.13.0`; aliases `jev-latest`/`jev-preview` point to **1.14.0**.
  Current-only. This directly conflicts with the D141 card claim that both
  aliases resolve to 1.13.0; treat that claim as stale/current-scope
  inconsistency, not historical authority.
- **D142 API**: no body, no headers, no version/date. Only card metadata.

P5 body-location record:
`notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p5-20261101T114236Z/did-bodies.md`
32514B, SHA256 `326a073b029d32c3c4be73c2fbdf6ab86d8e0d586fa2576bc6e6256b9492e575`.
D070/D071/D141 rows are explicit "UNCONFIRMED historical - current
observation only"; D142 is not one of the 17 body rows.

## 5. D142 — real title/locator and what it can justify

Current card:

`CW/sources/SP-efficient-llm-2026/evidence/v2/accepted/73f4bc1ec69c70925a7119a0327ff5e6f024812b56cf8edd7c49eae9f672a297/results/task-21ce0892d8846adffd6b.json`
3681B, SHA256 `7d7d26d454bf9f982696bb3a622f6c13b3116135eba9f1403639b9b998f9ca8b`,
status PARTIAL.

Exact identity:

- artifact `canonical_name`: `TypeSafe API reference (docs.typesafe.ai/api)`
- source `title`: `TypeSafe API reference (contract + confidence derivation)`
- `url`/locator: `https://docs.typesafe.ai/api`
- `published_at`: null
- card source `accessed_at`: `2026-09-22T15:00:00Z`
- `source_bindings`: `[]` in `sp-candidate-map.json`
- body: **not present**; no `sp17-api` raw file, no supplement source entry
- limitation: `Reference page not fetched; schema/confidence-derivation details outstanding.`

It **can** justify only a bounded summary-level record:

- the API-reference role was described as specifying an answer schema and
  distribution-derived confidence;
- a bounded negative finding: no benchmark or calibration-measurement
  protocol was located on the reference in the pass.

It **cannot** justify:

- actual request/response schema fields;
- the confidence derivation math or guarantees;
- API version/date/availability;
- that the page body was consumed;
- current or historical primary-body status;
- independent evaluation or calibration validity.

The card's `verification` target text `VERIFIED — Contract-role recorded with
corroboration; page body outstanding.` is internally inconsistent with its
status/limitation; the accepted Evidence status remains PARTIAL. Do not treat
that target label as body verification.

## 6. Historical mechanism/evaluation/availability classification

| item | historical capture | current body | defensible boundary |
|---|---|---|---|
| Choice/Score/Noul, parallel, calibration group caveat, text-only/atomic questions | S71/S141 summaries, 2026-09-21 | D071 current 2026-11-01 | historically **summarized**, current body observed; no historical body pin |
| RLCD / parallel sampler / new architecture | S70 summary 2026-09-21 | D070 current 2026-11-01 | vendor/project claim; RLCD internals not disclosed; no historical body |
| 70–500 ms, 40–200x, $0.042/MTok, 193.6x/444.6x, laptop/adapters/OpenRouter bias | S70/S141 summaries 2026-09-21 | D070 current 2026-11-01 | vendor claims historically summarized; current body contains vendor claims; no independent reproduction |
| Early access/waitlist/availability | S71/S74 summaries 2026-09-21 | D070 current 2026-11-01 | historical summary + current body; no historical body pin |
| `jev-1.13.0`, 64k/32k, 250k tok/s, 1200 req/min, alias drift | S141 summary 2026-09-21 | D141 current 2026-11-01 (now 1.13 + 1.14; aliases ->1.14) | version/alias is current-only; historical 1.13 is summary-only; no historical body |
| API contract/confidence derivation | S142 summary 2026-09-21 | none | summary-only; no schema/body; cannot justify details |
| independent reproduction/peer review | S73 summary 2026-09-21 | D073 current PARTIAL | no peer-reviewed reproduction located; community leads only; absence is a limitation, not proof |

Thus: historical **summary-level** mechanism/claims exist; historical
**body/version-confirmed** evidence does not. Current full bodies are
current-only. Do not promote the 2026-09-21 summaries to VERIFIED body
authority, and do not treat current 1.13/1.14 strings as proof of the
2026-09-21 revision.

## 7. Missing version boundaries

Within the authorized captures, missing:

- D070: any pre-cutoff body/revision at 2026-09-15 or 2026-09-21; current body
  is post-cutoff and mixed-date.
- D071: any 2026-09-21 body/revision; current body modified 2026-10-14 (after
  cutoff) and served 2026-11-01.
- D141: any 2026-09-21 body/revision; current body now has 1.14 and aliases
  point to 1.14, not 1.13.
- D142: any body (current or historical); only a summary-level card.
- D072/D073/D074: only discovery summaries; no full bodies; secondary/community
  and no independent reproduction.
- No captured independent benchmark/reproduction of Jev latency/price/accuracy
  or RLCD/calibration behavior.

This is a bounded capture-scope statement, not a claim that no snapshot exists
anywhere.

## 8. If as-of historical VERIFIED is genuinely required

Existing captures are sufficient only for an explicit O10 LIMITATION /
current-context treatment. If the root/Human requires as-of 2026-09-21
historical body verification, the minimal exact access would be one archived
snapshot per exact locator at or before 2026-09-21:

- `https://typesafe.ai/blog/introducing-system-one-models-and-jev`
- `https://docs.typesafe.ai/concepts/system-one`
- `https://docs.typesafe.ai/models`
- `https://docs.typesafe.ai/api` (only if API contract details are load-bearing;
  otherwise keep D142 summary-only/limitation)

Minimal method, if separately authorized: one archive index query per locator
limited to 2026-09-01..2026-09-21 for a 200 `text/html` snapshot, then the
single exact snapshot body+headers. For example:

```text
https://web.archive.org/cdx/search/cdx?url=<exact-locator>&from=2026-09-01&to=2026-09-21&filter=statuscode:200&filter=mimetype:text/html&output=json
# then one snapshot only:
https://web.archive.org/web/<snapshot-timestamp>id_/<exact-locator>
```

No live publisher crawl, no multiple revisions, no auto-Human question. This
was **not** fetched or executed here.

For D142 specifically: a current body capture would still be current-only;
historical API contract authority requires a <=2026-09-21 snapshot. If only the
negative calibration-protocol finding and summary-level contract role are used,
the existing summary card is enough for a limitation, not for schema details.

For independent reproduction, no URL access substitutes for independent
evaluation; the missing peer-reviewed/independent measurement remains a
research limitation.

## 9. Proposal-status implication

- The proposal's five current-only rows are D004/D070/D071/D141/D163; the Jev
  current-only rows are D070/D071/D141. D142 is summary-only supporting
  contract material.
- Keeping O10 as LIMITATION, retaining vendor quarantine, and making no
  09-21 VERIFIED claim is consistent with the captured evidence.
- P8 must not use D142 to assert actual schema/confidence fields, and must not
  use D070/D071/D141 to assert a 2026-09-21 historical version.
- Any upgrade of O10 to as-of VERIFIED requires the missing historical access in
  §8; any D142 contract-detail claim requires a D142 body.

No semantic PASS, quality adoption, or new Evidence review is claimed by this
inventory.
