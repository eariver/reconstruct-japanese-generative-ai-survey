# SP repaired correction — content review dossier r5 (DATA only, no active write)

Role: DATA author, offline read-only. No source/state/runtime/import/test/network/Git/Production/subagents. No python imports (jq + sha256sum + Read/Write/Grep only). Runtime epoch correct `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325` parent e84 (not handwritten truncated). R4 preserved as history; this r5 supersedes only the review-required fixes below. No shared README/ROOT edits.

## 1. Basis (READONLY)

- New runtime cc1c: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`, epoch `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325`, parent `e84a82aca000c990597ea8cf60f548e2ff187bd1`. Both States EVIDENCE_REVIEWED, init480, Profile/Contract8/checkpoints preserved. Setup complete; no prepare/adopt/guard/Selection by setup.
- Accepted interactive 697a 355643B `697a4ed088b76f18b3859568a735491a3a8b2295c480be3e1e678c4d8b31f104` (160 records). Supplement r6 ffcd 30922B `ffcd0a7eefdcf81700bd81982031ccbf7e8895835f55609eac772c40946fc4b3` (30 sources). Four refs: Evidence 65784e 49237B, Views 1557fef7 64222B, Ledger b7c85b 66850B, Completeness d67f7f 33683B (15 obs, 2 SAT/13 LIM).
- Archive intake (completed, not standing): manifest 4289B, decoded-manifest, claim-version-map, independent-content-review. u1 wire 42836B 10bf6607/decoded 253542B 14ae3118/index 2697B 495c93a8 served 2026-09-21T03:30:22Z; u2 wire 49007B 62bf012c/decoded 307198B 35770834/index 1093B 487d4aec served 2026-09-21T04:13:55Z; u3 plain 350662B 97a5dd74/index 1104B 41dfc593 served 2026-09-20T20:50:53Z via requested 20260921091419 (E2BRC NO-MATCH unserved never cited). S142 file 3751B f7eeec68, d10 file 4453B 0b8bd0ab.
- r5 files (NEW; r4 preserved): records-4-r5 17824B c8cd4278, completeness-request-r5 36487B cc4ce34d, input-assembly-r5 (this packet), full30 r4 reused 31522B e2bfb30a (no new source), staging-map r4, routing-map r4, schema-check r5, this dossier. Old patch4 (14291B, synthesized SUMMARY_ONLY) stays superseded history.

## 2. Full hashes 64 derived from actual files

All via sha256sum on actual files (listed §1 + r5/r4 packet files). No invented hashes. New r5: records-4 c8cd4278c857ac14cbd94ffce7740314bc4068f11fdf30b37e129f0e55877871 17824B; completeness-request cc4ce34dc3463df5d352a5d6449c577a77555e5a5006ab7e2b13fb4d42714d0d 36487B. Reused r4 full30 e2bfb30a (30 entries), r4 staging f9780f6a, r4 routing d8e10ea0 (clean FULL DID, no suffix — still valid, referenced not rewritten).

## 3. Literal checks (exact UTF8, visible body, no hidden instructions)

Unchanged from r4 review PASS (re-verified by grep -o/-n, 0 hidden `Content selection saved` in u1/u2/u3; `<script>` 8/11/11 are bundles; quotes in visible `<p>/<div>/<span>/<td>`, not script JSON):
- D070 Q1/Q2/Q3 contiguous visible (line 207 region div; Q2 `<strong>`; Q3 paragraph). Vendor quarantine retained; Q2/Q3 do not claim speed truth (race/accuracy UNRESOLVED).
- D071 Q1 visible content-area, Q2 line 646 span, Q3 callout; 255/cardinality/score-then-choose absent verified (only CSS `255 255 255` + JSON blob/SVG false positives).
- D141 Q1 line 652 span, Q2 `<td>` rate row, Q3 customizing section; 1.13-only era (1.13.0 ×8, both aliases →1.13.0; `1.14` hits SVG false positives). Served truthfully Sept20 via requested Sept21.
- D142 first claim exact token `INDEPENDENT_EVIDENCE_NOT_FOUND_AS_OF_2026-09-21` (S142 line 44, grep verified), INFERENCE, agent-summary provenance (3751B f7ee file, observed 2026-09-21, null bindings, no body/schema/math, UNRESOLVED). Future Raw `sp17-EFF-D142-summary-captured-20260921.md` = exact copy, no new content. No fetch/validator fix.

## 4. Rationale changes mapped old/new (not silent)

### O10 (status LIMITATION retained, no auto SAT)
- OLD (false current-only, base interactive + profile `d67f7f83…`): `Jev first-party core current-only (launch 270966B 278478f0 + concepts 165512B b58d91ae + models 219035B 59b6c17 current, all UNCONFIRMED historical, Last-Modified after cutoff) with vendor quarantine; independent reproduction/evaluation thin (community leads, F4 unresolved, no calibration protocol).`
- NEW (r5 completeness-request): `Jev first-party core vendor-historical BOUND (u1 launch served 2026-09-21T03:30:22Z 253542B 14ae3118 CDX MATCH, u2 concepts served 2026-09-21T04:13:55Z 307198B 35770834 CDX MATCH, u3 models served 2026-09-20T20:50:53Z 350662B 97a5dd74 served-row CDX MATCH via requested 20260921091419, vendor quarantine, RLCD name-only, no independent bench) with D142 body unfetched, RLCD internals undisclosed, independent calibration/reproduction outstanding (community leads, F4 unresolved, no calibration protocol, no independent bench); vLLM recipe + Dynamo dev current-only quarantined Appendix-A; current 1.14 model drift post-cutoff noted, no back-projection; architecture via V41 S2.4.3 + README dba1be0.`
- Keeps vLLM/Dynamo current-only true; adds served-3 historical vendor body Sept20/21 + D142 unfetched + RLCD + indep calibration/repro; removes false all-UNCONFIRMED + 6 stale pins as O10 ground (pins retained only as history of replaced current-only rows, not as rationale).

### Closure / residual_limitations (request shape, unchanged, explicitly reviewed)
- Base request `closure={targeted_gap_fill_completed:true, limitations:[5 same as residual], status:LIMITED}`, `residual_limitations=[5 clauses: wrong-identity locators; abstract-scope; thin eval; AIPerf open; per-figure pins]`. Reviewed: no false currentONLY text (do not claim Jev historical/current; thin-eval clause is about independent reproduction, still true). Preserved byte-identical in r5 completeness-request. vLLM/Dynamo current-only appears only where true (per-record/O?? rationales, not here). No change, mapped here not silent.

### Affected record materiality_rationale (narrow, preserved sentences restored)
- D070 OLD: `Jev launch current-only (270966B current, vendor quarantine); historical UNCONFIRMED, reproduction thin. Inclusion eligibility CONTEXT (current-only context with LIMITATION; historical VERIFIED requires 09-21/pinned revision per 174126Z §5). Relevance to O10/O04/O08/O11 preserved in rationale text; MATERIAL status alone is not relevance proof. Ledger downstream CONTEXT (not MATERIAL proof) until historical version bound. Verification UNRESOLVED historical preserved.`
- D070 NEW (r5): `Jev launch vendor-historical BOUND (archived 2026-09-21T03:30:22Z 253542B 14ae3118 CDX MATCH, vendor quarantine, RLCD name-only); independent reproduction thin. Inclusion eligibility CONTEXT (archived context with LIMITATION; O10 LIMITATION retained, no independent bench). Relevance to O10/O04/O08/O11 preserved in rationale text; MATERIAL status alone is not relevance proof. Ledger downstream CONTEXT (not MATERIAL proof) until accepted revision + independent re-review. Verification VERIFIED historical presence (vendor scope, conditional; race/accuracy quarantine UNRESOLVED retained).`
- D071 OLD/NEW: same pattern (concepts 2026-09-21T04:13:55Z 307198B 35770834; 255 absent stays current-only noted in claims/limitations; verification VERIFIED conditional). Relevance/ledger sentences restored.
- D141 OLD: `Jev models current-only (219035B, 1.13.0 + drift current); historical UNCONFIRMED. ...` NEW: `Jev models vendor-historical BOUND (archived 2026-09-20T20:50:53Z raw plain 350662B 97a5dd74 served-row CDX MATCH via requested 20260921091419, 1.13-only era, vendor quarantine, RLCD name-only). Nov 1.13+1.14 table with aliases->1.14.0 is post-cutoff drift, noted not conflicting, no back-projection. ... Verification VERIFIED historical presence + version/alias binding (vendor scope, conditional).` Relevance/ledger restored.
- D142 materiality unchanged (no currentONLY; API summary-only MATERIAL). D165 + 156 unaffected byte-identical (d455…, 16f046…).

### D141 Q2 context (rate-limit qualifier)
- OLD (r4): `Same archived revision; $42/BTok input outputs free, 64k ctx (32k state + longest question), text only, 250k tok/s + 1200 req/min in same table. Historical 1.13.0-only, no 1.14. Literal verified in same Raw.`
- NEW (r5): `Same archived revision; $42/BTok input outputs free, 64k ctx (32k state + longest question), text only, PLATFORM RATE LIMIT row 250k tok/s + 1200 req/min caps (not measured throughput) in same table. Historical 1.13.0-only, no 1.14. Literal verified in same Raw.`
- Claim text unchanged literal `250,000 tokens per second / 1,200 requests per minute`; class VENDOR_CLAIM (numerical vendor row, not independent measurement); units correct (tokens/sec + requests/min caps).

## 5. Source/task/filename/contract checks

- Original task targets preserved (no new split): D070 2, D071 1, D141 2, D142 2 (identical to 697a). Supplement task IDs stable (5491…/e1f751…/deaa55…); D142 no supplement entry.
- D142 first quote INFERENCE genuine S142 (token + provenance §3); Full DID Raws (EFF-D070/D071/D141/D142) in staging/routing/full30 r4 (reused, still valid; r5 adds no new Raw).
- `source_type` canonical PRIMARY_ANNOUNCEMENT/DOC (same as replaced old rows; schema allows string, observed base set includes these + PRIMARY_PAPER/RUNTIME_PR/etc.; no bare ANNOUNCEMENT/DOC invented). `source_class` PRIMARY_OFFICIAL. 13 keys, hex16, sha256, no traversal, `published_at null`.
- `sourceManifestPointers` clean paths only (r4); no literal `(= copy…)` suffix. Full30 real 30-entry array (no merge); 156 preserved + D165 intact; full30 no other new source/material/intake.
- Completeness object = request shape (obligations 15×7 + residual 5 + closure 3-field) from accepted request, NOT result wrapper (no overall_status/basis wrapper). 7-field shape per `profile-completeness-result.schema.json` (obligation_id/dimension/description/status/discovery_ids/evidence_task_ids/rationale); residual string array; closure request-shape (targeted_gap_fill_completed/limitations/status) as observed in base interactive (NOT result closure with expansion_passes). Validated by sourceread (schemas + base files read above).

## 6. Limits + remaining gaps (READY FOR REVIEW, no acceptance)

- DATA only. No State/source write, no HIGH prepare/adopt/resume/readback, no Selection/Architecture, no R4/Draft/PDF/Human Gate. O10 fix + materiality + rate qualifier are proposal DATA; actual external Decision requires HIGH prepare on cc1c with HEAD/tree/tool pins → proof/adopt/resume/readback → independent re-review → root dispatch → Selection/Architecture.
- Independent review must judge: O10 archive-aware rationale sufficient (no auto SAT); D070/D071/D141 narrow materiality adequate; D141 rate-limit qualifier adequate; D142 narrow INFERENCE token-quote meets contract with null bindings (or return gap); literals support historical rebinding with quarantine (literal ≠ rest-of-card proof).
- No claim acceptance, no independent decision, no semantic PASS here.
- Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Human Commit Point.
