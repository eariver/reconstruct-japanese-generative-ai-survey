# SP repaired correction — content review dossier r4 (DATA only, no active write)

Role: DATA author, offline read-only. No source/state/runtime/import/test/network/Git/Production/subagents.
Offline DATA parse only. Runtime owner separately handles new copy HEAD/tool pins (setup cc1c complete, producer gap repaired; old NOTYET/BLOCKED HIGH statements stale — corrected here only in new sp-*-r4 draft addenda, not root).

R3 files preserved as history. This r4 supersedes r3 only for the fixes below; no root/shared entry edited.

## 1. Basis (READONLY, new runtime cc1c)

- Selected new instance: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`, epoch `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325`, parent e84. Both States EVIDENCE_REVIEWED, init480, Profile/Contract8/checkpoints preserved. Setup complete; no prepare/adopt/guard/Selection by setup.
- Latest accepted interactive: `697a4ed088b76f18b3859568a735491a3a8b2295c480be3e1e678c4d8b31f104` 355643B. CP four refs: Evidence `65784e69559f9379412935fa5e7671beddee59b46b8fdb28a848d450e2b68ce0` 49237B, Views `1557fef75b4b737379a0e84eea983d9151b7148077f65da018206a2fae2b0341` 64222B, Ledger `b7c85b4eb009249b355445f94a4041d4374990fccb07c38595b61c1e770c8c60` 66850B, Completeness `d67f7f8363407b30d58dbe2dbe562b3666ea9483f9f16303859cfe459ab5e805` 33683B (15 obs, 2 SAT/13 LIM, O10 LIMITATION). D165 2-field fix preserved.
- Archive packet: `notes/rephase-1-selection-architecture-20261105/intake-20261106T001808Z-jev-archive/` (manifest 4289B, intake_helper, decoded-manifest, independent-content-review, claim-version-map). 3-index + 3-body logical (7 HTTP hops with archive 302). D142 API unfetched, no standing permission.
- New r4 files in this packet (r3 preserved): `sp-repaired-records-4-r4.json` (16726B e9bcc646…), `sp-repaired-supplement-full30-r4.json` (31522B e2bfb30a…), `sp-repaired-input-assembly-r4.json`, `sp-repaired-obligations-15-r4.json` (31838B 1d80d994…), `sp-repaired-staging-map-r4.json`, `sp-repaired-raw-routing-map-r4.json`, this dossier, `sp-repaired-schema-read-check-r4.json`.

## 2. Full hashes 64 derived from actual files (no invention)

- interactive 697a… 355643B, supplement r6 ffcd… 30922B, evidence-accepted 65784e… 49237B, views 1557fef7… 64222B, ledger b7c85b… 66850B, completeness d67f7f… 33683B (all in cc1c runtime, sha256sum verified).
- SUMMARY_CAPTURED: `discovery-observations-r2-g19-g20-data-jev.md` 3751B f7eeec68…, `discovery-observations-d10-specialization-jev.md` 4453B 0b8bd0ab… (cc1c raw, sha256sum verified).
- u1 wire 42836B 10bf6607…, decoded 253542B 14ae3118…, index 2697B 495c93a8…; u2 wire 49007B 62bf012c…, decoded 307198B 35770834…, index 1093B 487d4aec…; u3 wire/plain 350662B 97a5dd74…, index 1104B 41dfc593… (intake packet, sha256sum verified).
- r4 artefacts: records-4 e9bcc646… 16726B, full30 e2bfb30a… 31522B (30 entries), obligations 1d80d994… 31838B (15 obs). Computed via sha256sum after write (no self-reference inside files).

## 3. Literal checks (exact UTF8 in supplied decision Raw)

Basename contains FULL DID in all future Raws (EFF-D070/EFF-D071/EFF-D141/EFF-D142). R3 partial `sp17-D070` fixed.

### D070 — u1.snapshot.decoded.html
- Q1: `We built a new stack entirely focused on automation: with a new model architecture, parallel sampler for maximum efficiency, and training method we call Reinforcement Learning for Calibrated Decisions (RLCD).` — grep -o contiguous, line 207 visible Framer `<div><p>` body (not `<script>` JSON). Adjacent title/og:url/Sep15/byline/ssr 09-18/optimized 09-20 retained in proof, not publication pin.
- Q2: `End-to-end response time is 70ms-500ms` — visible `<strong>` in same paragraph; 40x-200x/$0.042 in adjacent text (vendor quarantine, not claimed literal).
- Q3: `This is where the claims of 193.6x faster, 444.6x cheaper on our home page comes from, and we expect that these are on the higher end of real world gains.` — visible paragraph; nuance admissions retained.
- No hidden instructions: `Content selection saved` count 0 in u1/u2/u3. `<script>` counts 8/11/11 are Framer/Mintlify bundles; quotes occur in visible `<p>/<div>`, not in `application/json` script blobs or response labels (verified via grep -n line contexts 207/646/652).

### D071 — u2.snapshot.decoded.html
- Q1: `System One models are a class of AI models built to make fast, structured decisions that software can use directly.` — grep -o contiguous, visible content-area (line 641 region), followed by `A System One model evaluates a <a>state</a>…` (tag-split, NOT used as literal — correctly avoided).
- Q2: `Calibration is measured across groups of predictions; it does not guarantee that an individual answer is correct.` — line 646 `<span data-as="p">` visible, not script.
- Q3: `Jev currently accepts text input only.` — visible callout; 255-cardinality absent (verified absence, stays current-only).
- Same hidden-instruction check: 0 hits.

### D141 — u3.snapshot.body.bin (plain)
- Q1: `An alias is a model name that resolves to a versioned model ID.` — line 652 `<span data-as="p">` visible table intro, not script.
- Q2: `250,000 tokens per second / 1,200 requests per minute` — visible `<td>` rate-limits row; $42/$0.042/64k/text-only in same table.
- Q3: `Jev is not fine-tuned or LoRA-adapted with customer data.` — visible customizing section; RLCD shared-weights in next sentence.
- Served truthfully `2026-09-20T20:50:53Z` via requested `20260921091419` 302; requested-row E2BRC NO-MATCH never cited. dateModified 09-20. Nov 1.14 drift noted separately, no back-projection.

### D142 — no API body (real gap, narrow summary-note claim only)
- First claim text (exact, INFERENCE): `INDEPENDENT_EVIDENCE_NOT_FOUND_AS_OF_2026-09-21`
  - Location: existing immutable `discovery-observations-r2-g19-g20-data-jev.md` line 44: `- independent-evidence verdict: INDEPENDENT_EVIDENCE_NOT_FOUND_AS_OF_2026-09-21 for peer-reviewed or` (token contiguous, grep verified).
  - Provenance (context, not text): agent-summary record, NOT publisher fact. Source file 3751B f7ee…, SUMMARY_CAPTURED observed 2026-09-21 by collector efficient-llm-discovery-r2, S142, retrieval SUMMARY_CAPTURED, locator https://docs.typesafe.ai/api, published null. No body fetched, no supplement entry, source_bindings null retained, no schema fields/confidence math/version/date/body consumption inferred. Body verification UNRESOLVED.
  - Future Raw copy: `sp17-EFF-D142-summary-captured-20260921.md` = exact copy of existing 3751B file, no new content, no appended claims. First-claim literal + full-DID Raw copy both derive from existing immutable bytes.
  - Field contract: with `source_bindings: null`, record cannot cite supplement authority; claims read as agent-summary/negative findings (INFERENCE) with explicit raw provenance, not supplement-bound publisher facts. No new supplement source invented. If source class/metadata-only cannot legally support even this narrow claim, return gap — documented here; independent review must judge. No validator change, no fetch.
- Second claim (preserved INFERENCE): `No benchmark or calibration-measurement protocol is published on the reference; independent peer-reviewed evidence remains NOT FOUND as of this pass.` — agent negative finding from same summary pass, not publisher fact. Verification both UNRESOLVED (overclaimed VERIFIED corrected in r3, retained).

## 4. Source class / provenance (no promotion, no independent bench)

- Supplement `source_type` canonical as in base r6 (schema allows any string minLength 1; canonical values observed: PRIMARY_ANNOUNCEMENT, PRIMARY_DOC, PRIMARY_PAPER, RUNTIME_PR, RUNTIME_RECIPE, PRIMARY_MODEL_CARD, first_party_announcement, first_party_product_docs, etc.). R4 uses PRIMARY_ANNOUNCEMENT (D070) / PRIMARY_DOC (D071/D141) — identical to replaced old entries, not bare ANNOUNCEMENT/DOC. `source_class` PRIMARY_OFFICIAL (same as predecessors). `published_at null` (memento served in relation/routing, not publication). No current→asof promotion, no independent bench. RLCD name-only.
- 156 unaffected + D165 preserved byte-identical (hashes d455…, 16f046…); Views/Ledger/Completeness rationales preserved; O10 LIMITATION. No View/Materiality promotion.

## 5. Obligations — 15 explicit, 7 fields each

Basis `profile-completeness-v2.json` 33683B d67f7f…, overall LIMITED. Each row: obligation_id/dimension/description/status/discovery_ids/evidence_task_ids/rationale. Full 15 in `sp-repaired-obligations-15-r4.json` (31838B 1d80d994…): O01 SATISFIED, O07 SATISFIED, rest LIMITATION including O10. O10: pending independent mechanisms/eval; vendor-historical scope (u1/u2/u3 served) + independent-measurement gap explicit; vLLM/Dynamo quarantined Appendix-A; V41 §2.4.3 + README dba1be0. No auto SAT.

## 6. Supplementary Raw27 + 4 future Raws

- Preserved 27 byte-identical to r6 (including D165 pr.json, D062x2/D093x2 extras). Full30 real array in r4 (30 entries, 13 keys each, hex16, stable task IDs, sourceRoot future paths with FULL DID, no traversal). No merge needed.
- Future Raws (proposed only, no active write): 3 publisher exact copies of decoded bytes with FULL DID + 1 D142 exact copy of SUMMARY_CAPTURED with FULL DID. Wire gzip retained only in packet/routing.

## 7. Stale r3 fixed (r3 preserved)

- `sp17-D070` → `sp17-EFF-D070-…`, similarly D071/D141; D142 `sp17-EFF-D142-summary-captured-20260921.md` added per proof.
- `sourceManifestPointers` + `future_raw_path` suffix `(= copy of…)` removed; clean paths only, copy semantics in separate `copy_note`/`note` fields.
- Descriptor 27-hash+3 replaced by real full30 array (31522B e2bfb30a…).
- Patch4 + obligations descriptor replaced by records-4 (e9bcc646…) + input-assembly (explicit jq filter, no custom merge contract) + obligations-15 (1d80d994…).
- D142 synthesized SUMMARY_ONLY replaced by exact token + agent-summary provenance (INFERENCE, null bindings, no publisher claim).
- source_type bare-form avoided; canonical PRIMARY_* retained; schema keys verified (13 required, hex16, sha256, no invented fields).
- Targets exact, no new split (D070 2, D071 1, D141 2, D142 2).

## 8. Limits + remaining gaps (READY FOR REVIEW, no acceptance)

- DATA only. No State/source write, no HIGH prepare/adopt/resume/readback, no Selection/Architecture, no R4/Draft/PDF/Human Gate. Producer gap repaired in cc1c source, but DATA-shape/content still requires independent review + root dispatch with new HEAD/tree/tool pins.
- Independent review must judge: (a) D142 narrow summary-note claim meets contract with null bindings/metadata-only (or return gap); (b) 3 publisher literals support historical rebinding with vendor quarantine (literal presence ≠ verification of rest of card); (c) 255-cardinality exclusion, 1.14 drift note, O10 LIMITATION adequate; (d) full30/assembly/obligations hashes and counts.
- No claim acceptance, no independent decision, no semantic PASS claimed here.
- Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Human Commit Point.
