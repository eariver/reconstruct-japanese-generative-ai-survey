# SP correction final addendum r7 — pin-only correction (preserves prior reviews, discloses prior error)

Reviewer: NEW independent content reviewer (same as r4/r5/r6 reviews, all preserved byte-identical, NOT rewritten).
Scope: r7 pin-only DATA vs r6/r4. No source/state write, no HIGH prepare/adopt/resume/readback, no Selection/Architecture, no R4/Draft/PDF/Human Gate, no synthetic decision/approval.
Method: Read + stdlib hash/compare only (Read, sha256sum, python stdlib json/hashlib). No project imports/runtime/tests/Git binary/network/Production/subagents. No reconstruct readback. New cc1c + old e84 + P2 DATA read as DATA only. Setup cc1c exact773 current per root README; old producer gap not current blocker.

## 1. Prior-review error disclosed (no rewriting)

Prior r4 review (§2) + r5 addendum + r6 addendum claimed S142 full-pin match but carried wrong full SHA `f7eeec6872fa7dd9ad8f8fb08beadfb9e2ff2bab571ffff807c2d34718662662` (`…18662662`) in:
- `reviews/sp-correction-proposal-review.md:27` + `-machine.json` (S142 pin),
- `reviews/sp-correction-proposal-review-addendum-r5-machine.json` (`base_pins.s142`),
- r4-r6 DATA (`sp-repaired-raw-routing-map-r4.json` `existing_sha256`, `sp-repaired-records-4-r4/r5/r6.json` D142 `claims[0].context` provenance string, `sp-repaired-staging-map-r4.json` `summary_proof_copy.sha256`, `sp-repaired-patch4.json` superseded context).
Cause per `d142-pin-discrepancy-review.md`: prefix `f7eeec68` identical hid single-char typo at index 59 (0-based `7` vs `6`); outer `execution-report.md:11` (`matching routing pin`) + machine `precise_exception` (`match f7eeec68/3751`) were prefix-only and incorrect — full 64-char comparison fails. This addendum discloses the error and proves the correction; prior reports are preserved as history, NOT rewritten.

## 2. Independent pin proof (actual, not prefix-only)

Actual recomputed (stdlib `hashlib.sha256(read_bytes()).hexdigest()` + `st_size`, mode `0o664`):
- NEW cc1c: `…/repaired-correction-rehearsal-20261112T125743Z/candidate-work/sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g19-g20-data-jev.md` 3751B `f7eeec6872fa7dd9ad8f8fb08beadfb9e2ff2bab571ffff807c2d34718672662`
- OLD e84: `…/evidence-scaling-w34-retry-20261103T172327Z/candidate-work/…/discovery-observations-r2-g19-g20-data-jev.md` 3751B same `…18672662`
- P2 captured DATA: `notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c33.discovery-observations-r2-g19-g20-data-jev.md` 3751B same `…18672662`
- Provenance: P2 `manifest.json` gid `p2c33` `repo_path sources/…/discovery-observations-r2-g19-g20-data-jev.md` `reported_blob_sha 0c1d507b…` `reported_size 3751` `data_files[0]` 3751B `…18672662` (computed match); P5 `did-bodies.md` same path `@c8 blob 0c1d507b… 3751B …18672662`; inventory `sp-jev-authority-inventory.md:97` same; expected manifests r5/r6/r7-D165fix + P2 DATA manifest all `…18672662`. Old == new == P2 == entry-inventory == provenance. No drift/mutation.
- Wrong routed `…18662662` differs by ONE byte (index 59 `6` vs actual `7`). Initial SP zero-write refusal (`prepare-normal-high-r3.py:648` `REFUSE: SP D142 pinned drift`, exit 2, zero SP writes) was CORRECT full-hash enforcement, not a bug to bypass.

## 3. r7 bounded pin-only diff vs r6/r4 (ONE byte each, no semantic diff)

r7 files (sha256sum verified): records-4-r7 17947B `0a54004eefe12b5412ebca733826f4401c5dfcb8ac644f32111e2d547785cb06`, routing-r7 4061B `af4e043c1120ded74e6ad2c284c372c34ea6bd39b4e030663412ce9eb01e8dcf`, staging-r7 2644B `b7fac76093bad619b8796c71c1e3c03225edd59b68cda76647e1d3dcb7785f70`, assembly-r7 3382B `3f291e6fb1eb5d6078f032efb6fb443bd0496c3f1f6285af35a66455d92cef95`, dossier-r7 8046B `51a316a141b889c77f8e24ba9fa303daad412bed6efa3c2e593e435fa2dd876f`.
- records: r6 `cca74577` → r7 `0a54004e`, same 17947B, `cmp -l` count 1 at 13959 (`…18662662` → `…18672662` in D142 `claims[0].context` SourceSHA substring). Claims text, INFERENCE×2, contexts (absent-key + summary-scope + uninspected + not-global-proof), materiality HOLD ceiling, caveat no-verified-facts, verification 2×UNRESOLVED, lineage CORE all4, D142 key omitted, D070/D071/D141 bindings/rate qualifier/materiality all byte-identical to r6. No semantic diff besides correct SourceSHA.
- routing: r4 `d8e10ea0` → r7 `af4e043c`, same 4061B, 1 byte at 314 (`existing_sha256` typo → actual). Future FULLDID paths unchanged.
- staging: r4 `f9780f6a` → r7 `b7fac760`, same 2644B, 1 byte at 2636 (`summary_proof_copy.sha256` typo → actual). Future FULLDID paths unchanged.
- r7 wrong-count 0 / correct-count 1 per file; no other SP new DATA carries either variant (dossier-r7 §5 historical scan preserved, 11 typo spots + 62-char malformed `…80adfb…` len62 in old candidate-maps reported, NOT rewritten).
- Reused unchanged: completeness r5 36487B `cc4ce34dc3463df5d352a5d6449c577a77555e5a5006ab7e2b13fb4d42714d0d` (O10 archive-aware LIMITATION, 15×7 + residual5 + closure request-shape, verified in r5/r6), full30 r4 31522B `e2bfb30ae738b1328b1b3c5eceab1b9313d6d017cc864bce0b68c1997ca128fb` (30 real). Assembly r7 cites same hashes. 156 `d455f722…` + D165 `16f046f5…` preserved (counts 160=156+4). Targets exact 2/1/2/2.

## 4. Verdict

Pin typo CLOSED with tied immutable bytes (no blind repin, no drift). All r6-approved content (O10, narrow D142 + HOLD, keys/targets, literals/quarantine, 156/D165, completeness/full30, FullDID) preserved.

**Final PROPOSAL_READY on r7** for normal HIGH prepare (cc1c exact773): records `0a54004e` + routing `af4e043c` + staging `b7fac760` + assembly `3f291e6f` + reused completeness `cc4ce34d` + full30 `e2bfb30a`. Actual external Decision requires after graph: HIGH prepare with HEAD/tree/tool pins → proof/adopt/resume/readback → independent re-review → root dispatch → Selection/Architecture. No synthetic approval, no semantic PASS, no acceptance. DATA only. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Human Commit Point.

## 5. Read scope

r7 records/routing/staging/assembly/dossier + discrepancy review + machine; reused r5 completeness + r4 full30; base 697a/tasks/S142/profile/interactive completeness + runner contract (prior r6 verification); old e84/new cc1c/P2 DATA bytes + P2 manifest/P5 did-bodies/inventory/expected manifests (hash/size/provenance). No validator, no imports, no Git/network/Production.
