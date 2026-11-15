# SP repaired correction — content review dossier (DATA only, no active write)

Role: DATA author, offline read-only. No project imports/runtime/tests/Git/network/Production/subagents.
Offline DATA/PDF/HTML parse only (stdlib). Runtime owner separately does new copy HEAD/tool pins later.

## 1. Basis (READONLY)

- Saved real instance: `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work`, old e84 `e84a82aca000c990597ea8cf60f548e2ff187bd1` parent `48082356`. Both States EVIDENCE_REVIEWED. Preserved, not cleaned/edited.
- Latest accepted interactive: `697a4ed088b76f18b3859568a735491a3a8b2295c480be3e1e678c4d8b31f104` 355643B (== `sp-corrected-input-r5-D165fix-20261105.json`). CP four refs unchanged: Evidence `65784e69…` 160 (8V/152P), Views `1557fef7…` 160, Ledger `b7c85b4e…` 165, Completeness `d67f7f83…` 15 (2 SAT/13 LIM). D165 2-field final fix preserved (hash `16f046f5…`).
- Proposals read: `sp-four-record-correction-proposal-r2.json` + `sp-archive-source-id-preimage-map.json` (preimage `DID|served_url|decoded_sha256` → hex16). Preserved as history; stale fields fixed as NEW DATA below, original r2 retained.
- Archive packet: `intake-20261106T001808Z-jev-archive/` (manifest `671bfab8…`, intake_helper `30f050fd…`). Wire/decoded/manifests + `independent-content-review.md` + `claim-version-map.md` read as DATA. 3-index + 3-body logical (7 HTTP hops with archive 302). No standing permission, no new fetch.
- Unaffected 156 hash `d455f7221a0addd93dd2a3c07c874fe4dfb815d3e795933882eb839e868a1ef9` (canonical sorted JSON). Preserved supplement 27 hash `c75389e89c00760231a1e1621efe0c6fdcea8b76aec624397adda896f5a1f995`. Expected full30 hash with DID filenames `445d2265432320569487c5da3e97e41843e30e93bc35a1e1925100e230e409f8`.

## 2. Genuine quoted spans (literal UTF8 verified present in supplied decision Raw)

All spans below verified via offline substring search in packet Raw files. Basename contains DID in future Raw (see staging map). No appended translation, no artificial claim-bearing Raw.

### D070 — u1.snapshot.decoded.html (253542B `14ae3118…`, wire 42836B `10bf6607…`, CDX `6XH5…MATCH`)

- Q1 (claims[0]): `We built a new stack entirely focused on automation: with a new model architecture, parallel sampler for maximum efficiency, and training method we call Reinforcement Learning for Calibrated Decisions (RLCD).`
- Q2 (claims[1]): `End-to-end response time is 70ms-500ms`
  - Adjacent same-body context (not claimed literal): `for TypeSafe. This can range from 40x-200x faster…`, `$0.042 / MTok`, outputs free.
- Q3 (claims[2]): `This is where the claims of 193.6x faster, 444.6x cheaper on our home page comes from`

Vendor scope, RLCD name-only, no independent validation. Title `Introducing System One Models & Jev - TypeSafe AI Blog`, `og:url` exact locator, Sep 15 byline + embedded `2026-09-15T00:00:00.000Z` + Sep 20 publish comment + ssr `2026-09-18T08:31:26.653Z` / optimized `2026-09-20T23:50:00.411Z` retained in proof, not as publication pin.

### D071 — u2.snapshot.decoded.html (307198B `35770834…`, wire 49007B `62bf012c…`, CDX `TUION…MATCH`)

- Q1 (claims[0]): `System One models are a class of AI models built to make fast, structured decisions that software can use directly.`
- Q2 (claims[1]): `Calibration is measured across groups of predictions; it does not guarantee that an individual answer is correct.`
- Q3 (claims[2]): `Jev currently accepts text input only.`
  - Accompanied same-body: `It evaluates strings, JSON objects, and arrays of text.`, `Images, audio, and video are not supported (yet).`
  - Explicitly ABSENT in archived visible text: 255-cardinality / score-then-choose two-stage handling (Nov-current scope, stays current-only, removed from as-of).

### D141 — u3.snapshot.body.bin (350662B `97a5dd74…` plain decoded identity, served-row CDX `ABQRK5…MATCH`)

Truthful citation: served `2026-09-20T20:50:53Z` via requested `20260921091419` 302. Requested-row `E2BRC…NO-MATCH` unserved, never cited as served. `dateModified 2026-09-20T02:53:36.007Z`.

- Q1 (claims[0], alias binding): `An alias is a model name that resolves to a versioned model ID.`
  - Same-revision table: `jev-latest → jev-1.13.0`, `jev-preview → jev-1.13.0` (`No preview build available right now`), single `jev-1.13.0` only, no `1.14` (1.14 hits are SVG false positives).
- Q2 (claims[1]): `250,000 tokens per second / 1,200 requests per minute`
  - Same table: `Price (per Btok / per Mtok)` `$42 / $0.042`, `Context length 64k…32k…`, `Input Text only…`, outputs free.
- Q3 (claims[2]): `Jev is not fine-tuned or LoRA-adapted with customer data.`
  - Same section: `It is trained with RLCD to return calibrated decisions, and the same weights serve every account.`

Nov drift noted separately: current body `219035B 59b6c17…` dateModified `2026-11-01` shows `1.13 + 1.14` table, aliases `→1.14.0`. Post-cutoff, not conflicting, no back-projection.

### D142 — no API body (real gap)

- No `sp17-api` raw, no supplement entry, `source_bindings: null` unchanged. u1/u2/u3 contain no API schema (u2 links API ref for full request shape only).
- New claims[0] explicitly `SUMMARY_ONLY … Body outstanding…` + refusal, binding genuine old text:
  - Genuine S142 SUMMARY_CAPTURED (`discovery-observations-r2-g19-g20-data-jev.md` 3751B `f7eeec68…`, observed 2026-09-21): `POST /v1/systemone; per-question Choice/Score/Noul answers with probabilities; confidence DERIVED from distribution (Choice/Score)` + `NO benchmark methodology, NO calibration measurement protocol, NO independent audit` + `INDEPENDENT_EVIDENCE_NOT_FOUND_AS_OF_2026-09-21`.
- New claims[1] preserves baseline negative finding (INFERENCE retained). Verification `Evidence-stage full-body verification` CORRECTED `VERIFIED → UNRESOLVED` (overclaim fix). `calibration protocol gap` UNRESOLVED retained. No schema/confidence math/version/date/body consumption inferred. If literal-in-Raw proof required, RETURN real gap — done here, no fetch, no validator fix.

## 3. Source class / provenance (no promotion, no independent bench)

- All 3 new supplement `source_class PRIMARY_OFFICIAL` (same as current-only predecessors), `source_type ANNOUNCEMENT/DOC` preserved. `published_at null` (memento served time is not publication; served in `relation` + routing map). `accessed_at` intake instants preserved.
- `relation` states archived revision served timestamp + wire/decoded/CDX + vendor scope + `no independent validation`. No `current → as-of` promotion, no `independent bench` claim. RLCD internals undisclosed name-only.
- Views/Ledger/Completeness: 156 unaffected record fields + View rationales preserved (hash above). No View/Materiality promotion. O10 stays LIMITATION (see §4).

## 4. Obligations — all 15 explicit, O10 LIMITATION (DM022 7 fields each)

Basis `profile-completeness-v2.json` 33683B `d67f7f83…`, overall LIMITED. Each obligation has 7 fields: `obligation_id/dimension/description/status/discovery_ids/evidence_task_ids/rationale`. No auto SAT.

- O01 SATISFIED, O07 SATISFIED, all others LIMITATION including O10. O10 text: pending independent mechanisms/eval; improved boundary vendor-historical scope (u1/u2/u3 served timestamps) + independent-measurement gap explicit; vLLM/Dynamo quarantined Appendix-A; architecture via V41 §2.4.3 + README `dba1be0`. Do not auto SAT. Historical-body gap closes for D070/D071/D141 at stated timestamps; independent-measurement gap does not.

## 5. Supplementary Raw27 + 3Raw future-only

- Supplementary Raw27 preserve old all unaffected cards: 27 preserved entries byte-identical to r6 (hash `c75389e8…`), including D165 `1ae83672998fa5fe` (pr.json 26122B `3728e08d…`) and D062x2/D093x2 extras. No old overwrite.
- Proposal 3Raw future stage only copy of decoded bytes with DID filenames (staging map + `sourceManifestPointers` var declared). No active `source_root/external` write now. Wire gzip retained only in packet + routing map.

## 6. Stale fields fixed as NEW DATA (original r2 preserved)

- Future raw paths lacked DID → now `sp17-D070-…`, `sp17-D071-…`, `sp17-D141-…` + `sourceManifestPointers` declared.
- Firstclaims were summaries → now literal UTF8 verified spans above.
- D071 255-cardinality vague → now explicitly absent archived visible text, removed from as-of, stays current-only.
- D141 served-via-requested already truthful in r2 → preserved + requested-row NO-MATCH explicitly not cited.
- D142 `unchanged` vague → now explicit `SUMMARY_ONLY`/refusal + genuine S142 binding + `VERIFIED→UNRESOLVED` downgrade.
- Claim classes: D071/D141 vendor mechanism → `VENDOR_CLAIM` (vendor scope, no independent validation); D142 summary `PROJECT_CLAIM` + negative `INFERENCE` retained.
- Supplement shape: 13 keys, hex16, stable task IDs, sourceRoot future paths, `published_at null` all re-checked (schema-read-check file, honest not runtime pass).

## 7. Limits + next

- This packet is DATA only. No active State/source write, no producer run, no Selection/Architecture, no R4/Draft/PDF/Human Gate. Operation remains BLOCKED on HIGH supplement-carry gap (see selection-architecture + supplement-carry closeouts); LOW manual workaround not selected.
- Next after Human continuation (runtime owner): new independent byte-copy of saved e84, install exact773 proof, isolated execution-source commit, strict read APIs, then revalidate this DATA against actual records/tasks/schema + genuine HIGH prepare/adopt/resume/readback with independent reviews. Return unexpected failure with raw commands/env/cwd/PID/time/exits, no auto retry/cleanup.
- Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Human Commit Point.
