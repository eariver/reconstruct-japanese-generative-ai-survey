# SP repaired correction — content review dossier r7 (DATA only, no active write)

Role: DATA author, offline read-only. No source/state/runtime/import/test/network/Git/Production/subagents. No python imports (Read + sha256sum + jq + grep only; runner .py read as DATA in r6, never imported/executed). Epoch correct `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325` parent e84. R3–R6 + all raw preserved as history (r4/r5/r6 typos retained in place, not rewritten); this r7 corrects ONLY the erroneous full-SHA references below. No shared README/ROOT edits.

## 1. Basis (READONLY)

- New runtime cc1c: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`, epoch above. Both States EVIDENCE_REVIEWED, init480, Profile/Contract8/checkpoints preserved. Setup complete; no prepare/adopt/guard/Selection.
- Accepted interactive 697a 355643B `697a4ed088b76f18b3859568a735491a3a8b2295c480be3e1e678c4d8b31f104` (160). Supplement r6 ffcd 30922B `ffcd0a7eefdcf81700bd81982031ccbf7e8895835f55609eac772c40946fc4b3` (30). Four refs: Evidence 65784e 49237B, Views 1557fef7 64222B, Ledger b7c85b 66850B, Completeness d67f7f 33683B.
- Archive intake (completed, not standing): u1 wire 42836B 10bf6607/decoded 253542B 14ae3118/index 2697B 495c93a8 served 2026-09-21T03:30:22Z; u2 wire 49007B 62bf012c/decoded 307198B 35770834/index 1093B 487d4aec served 2026-09-21T04:13:55Z; u3 plain 350662B 97a5dd74/index 1104B 41dfc593 served 2026-09-20T20:50:53Z via requested 20260921091419 (E2BRC NO-MATCH unserved never cited). No u1/u2/u3 change in r7.
- r7 files (NEW): records-4-r7 17947B 0a54004e, routing-r7 4061B af4e043c, staging-r7 2644B b7fac760, assembly-r7 (this packet), this dossier. Reused unchanged: completeness-request r5 cc4ce34d (O10 archive-aware, 15×7 + residual + closure), full30 r4 e2bfb30a (30 real, FULL DID).

## 2. Provenance proof pointer + exact 1-digit delta (no blind repin, no drift)

Actual recomputed bytes (sha256sum, all 3751B mode 0o664):
- OLD e84: `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work/sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g19-g20-data-jev.md` → `f7eeec6872fa7dd9ad8f8fb08beadfb9e2ff2bab571ffff807c2d34718672662`
- NEW cc1c: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work/sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g19-g20-data-jev.md` → same `…18672662` / 3751
- P2 captured DATA: `notes/rephase-1-operational-rehearsal-20261101/intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c33.discovery-observations-r2-g19-g20-data-jev.md` → same `…18672662` / 3751
Provenance (no fetch, captured scope only): P2 `manifest.json` gid `p2c33` label `SP-raw-obs-r2-g19`, ref `c8d0ecc1c9566a2303ad3b4c42635d4b672650e4`, `repo_path sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g19-g20-data-jev.md`, `reported_blob_sha 0c1d507be945b1cf38d8afbee0be8aaf8b0a623b`, `reported_size 3751`, `data_files[0]` bytes 3751 sha256 `f7eeec68…18672662` (computed P2 DATA bytes match manifest); P5 `did-bodies.md` same path `@c8 blob 0c1d507b… 3751B sha256 f7ee…18672662 (P2 DATA.p2c33 reused no recopy)`; authority inventory `sp-jev-authority-inventory.md:97` same `…18672662`; expected manifests r5/r6/r7-D165fix + P2 DATA manifest all `…18672662`. Old e84 == new cc1c == P2 DATA == entry-inventory == provenance. No drift/mutation.
Routed typo (r4–r6): `f7eeec6872fa7dd9ad8f8fb08beadfb9e2ff2bab571ffff807c2d34718662662` (`…18662662`). Exact delta: full-string compare, single-char diff at index 59 (0-based): actual `7` vs routed `6`; prefix `f7eeec68` identical (why prefix-only execution-report claims hid it). Wrapper correctly refused on full-hash mismatch (`prepare-normal-high-r3.py:648` D142 pinned drift, exit 2, zero SP writes). Verdict per independent review: TYPO_DATA_CORRECTION, not UNKNOWN_DRIFT. This r7 applies the tied correction, not a blind repin.

## 3. Sole field diffs r6→r7 (1 byte per file, paths unchanged)

- records-4: r6 `cca74577…` 17947B → r7 `0a54004e…` 17947B. Sole change: D142 `claims[0].context` SHA substring `…18662662` → `…18672662`. `cmp -l` count = 1. Keys/texts otherwise identical (D142 key omitted, lineage CORE all 4, INFERENCE token, narrow summary-scope, UNRESOLVED×2, MATERIAL HOLD ceiling; D070/D071/D141 r5 fixes incl D141 rate qualifier preserved).
- routing: r4 `d8e10ea0…` 4061B → r7 `af4e043c…` 4061B. Sole change: `d142_summary_routing.existing_sha256` typo → actual. `future_raw_path` FullDID unchanged (`sp17-EFF-D142-summary-captured-20260921.md` etc.). `cmp -l` = 1.
- staging: r4 `f9780f6a…` 2644B → r7 `b7fac760…` 2644B. Sole change: `summary_proof_copy.sha256` typo → actual. Future paths unchanged FullDID (EFF-D070/D071/D141/D142). `cmp -l` = 1.
- No other new source/material/intake. Byte counts unchanged (17947/4061/2644).

## 4. Literal / schema / targets (unchanged from r6 approval, re-verified)

- D142 first claim INFERENCE exact token `INDEPENDENT_EVIDENCE_NOT_FOUND_AS_OF_2026-09-21` (S142 line 44), agent-summary provenance, null bindings absent (key omitted), UNRESOLVED×2, no body/fetch. D070/D071/D141 literals visible body vs script JSON re-verified in r6 review (line 207 div, 646 span, 652 span; hidden `Content selection saved` 0). D141 Q2 PLATFORM RATE LIMIT qualifier preserved.
- Record keys per `run_evidence_v2_interactive.py:120-215` (read-only): D070/D071/D141 16 keys (15 THEMATIC incl lineage_role=CORE + source_bindings non-empty hex16), D142 15 keys (required incl lineage_role=CORE, source_bindings omitted — not null, no unknown fields, only permitted nullable: entity.canonical_url, inheritance_note). Targets exact (2/1/2/2). 156 + D165 preserved (`d455f722…`, `16f046f5…`). Completeness r5 (O10 archive-aware LIMITATION, 15×7 + residual + closure request-shape, no wrapper) reused. Full30 r4 reused. No validator executed, no imports.

## 5. Bad-hex scan (report historical, rewrite nothing)

- 64-char typo `…18662662` found in 11 historical spots (preserved, NOT rewritten): `sp-repaired-patch4.json` (superseded synthesized context), `sp-repaired-records-4-r4/r5/r6.json` (D142 context), `sp-repaired-raw-routing-map-r4.json` (existing_sha256 — root cause of SP dispatch refusal), `sp-repaired-staging-map-r4.json` (summary_proof_copy.sha256), `reviews/sp-correction-proposal-review.md:27` + `-machine.json` (S142 pin), `reviews/sp-correction-proposal-review-addendum-r5-machine.json` (base_pins s142), `d142-pin-discrepancy-review.md:37` + `-machine.json` (intentional quotes as typo evidence + typo-path list — keep as investigation record).
- 62-char malformed `f7eeec6872fa7dd9ad8f8fb80adfb9e2ff2bab571ffff807c2d34718662662` (len 62, invalid SHA256) in `notes/rephase-1-selection-architecture-20261105/sp-candidate-map-r2.json:9408`, `sp-candidate-map-r3.json:10339`, `sp-essential-gap-map.json:10,66` (Explore transcription, not authority — report only, no rewrite per task).
- r7 files contain 0 typo / 1 correct each (verified). No other SP new DATA carries either variant (dossier/schema/assembly reference correct full hash or 8-char prefix only where explicitly prefix).

## 6. Limits + remaining gaps (READY FOR REVIEW, no acceptance)

- DATA only. No State/source write, no HIGH prepare/adopt/resume/readback, no Selection/Architecture, no R4/Draft/PDF/Human Gate. R7 corrects only the SHA typo; all r6-approved content (O10, materiality, rate qualifier, D142 narrow INFERENCE + HOLD, keys, targets, 156/D165, completeness, full30, FullDID paths) preserved.
- Independent review must judge: corrected pins route to tied immutable bytes (old e84 == new cc1c == P2 DATA == manifests); narrow D142 claim + HOLD ceiling meets contract with absent bindings; literals support historical rebinding with quarantine.
- No claim acceptance, no independent decision, no semantic PASS here.
- Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Human Commit Point.
