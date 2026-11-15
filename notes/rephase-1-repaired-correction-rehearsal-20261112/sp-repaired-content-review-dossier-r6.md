# SP repaired correction — content review dossier r6 (DATA only, no active write)

Role: DATA author, offline read-only. No source/state/runtime/import/test/network/Git/Production/subagents. No python imports (Read + sha256sum + jq + grep only; runner .py read as DATA, never imported/executed). Epoch correct `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325` parent e84 (not truncated). R4/r5 preserved as history; this r6 supersedes only the root §4 blockers. No shared README/ROOT edits.

## 1. Basis (READONLY)

- New runtime cc1c: `.rephase-1-editorial-runtime/repaired-correction-rehearsal-20261112T125743Z/candidate-work`, epoch `cc1c7fd1cf979e71fda4ae2164828b37bc1b2325`, parent `e84a82aca000c990597ea8cf60f548e2ff187bd1`. Both States EVIDENCE_REVIEWED, init480, Profile/Contract8/checkpoints preserved. Setup complete; no prepare/adopt/guard/Selection.
- Accepted interactive 697a 355643B `697a4ed088b76f18b3859568a735491a3a8b2295c480be3e1e678c4d8b31f104` (160). Supplement r6 ffcd 30922B `ffcd0a7eefdcf81700bd81982031ccbf7e8895835f55609eac772c40946fc4b3` (30). Four refs: Evidence 65784e 49237B, Views 1557fef7 64222B, Ledger b7c85b 66850B, Completeness d67f7f 33683B (15 obs, 2 SAT/13 LIM).
- Archive intake (completed, not standing): manifest 4289B, decoded-manifest, claim-version-map, independent-content-review. u1 wire 42836B 10bf6607/decoded 253542B 14ae3118/index 2697B 495c93a8 served 2026-09-21T03:30:22Z; u2 wire 49007B 62bf012c/decoded 307198B 35770834/index 1093B 487d4aec served 2026-09-21T04:13:55Z; u3 plain 350662B 97a5dd74/index 1104B 41dfc593 served 2026-09-20T20:50:53Z via requested 20260921091419 (E2BRC NO-MATCH unserved never cited). S142 file 3751B f7eeec68 (line 44 token), d10 file 4453B 0b8bd0ab.
- r6 files (NEW; r4/r5 preserved): records-4-r6 17947B cca74577, assembly-r6 (this packet), delta-r5-r6, schema-check-r6, this dossier. Reused unchanged: completeness-request r5 36487B cc4ce34 (O10 archive-aware, 15×7 + residual + closure), supplement-full30 r4 31522B e2bfb30a (30 real), staging-map r4, routing-map r4 (FULL DID clean, D142 summary routing).

## 2. Full hashes 64 derived from actual files (sha256sum, no invention)

- Base: 697a, ffcd, 65784e, 1557fef7, b7c85b, d67f7f, f7ee, 0b8b, wire/decoded/index above (all verified §1).
- r6 new: records-4 cca74577729ee22bbab088a6fdc30f909c2a79bd5e6781c1f4d80fac36a4d7c2 17947B; assembly/delta/schema/dossier hashes reported in final return (computed after write, no self-reference inside files).
- Reused: completeness r5 cc4ce34d…, full30 r4 e2bfb30a…, 156 preserved d455f722…, D165 16f046f5….

## 3. Literal + key checks (exact, visible, no hidden instructions)

Unchanged from r5 review PASS (re-verified): D070 Q1/Q2/Q3 contiguous visible (line 207 div, `<strong>`, paragraph; quarantine retained); D071 Q1 visible content-area, Q2 line 646 span, Q3 callout, 255 absent (only CSS/JSON/SVG false positives); D141 Q1 line 652 span, Q2 `<td>` rate row, Q3 customizing section, 1.13-only era, served Sept20 via Sept21 truthfully; `Content selection saved` 0 hits; script 8/11/11 unrelated bundles; quotes in visible elements, not script JSON/response labels.
- D142 first claim unchanged INFERENCE token `INDEPENDENT_EVIDENCE_NOT_FOUND_AS_OF_2026-09-21` (S142 line 44, grep verified), agent-summary provenance, null bindings replaced by key absence (see §4), UNRESOLVED.
- D141 Q2 context carries explicit `PLATFORM RATE LIMIT row … caps (not measured throughput)` (r5, preserved in r6); VENDOR_CLAIM numerical row, units tokens/sec + req/min correct.

## 4. Rationale maps old→new (not silent)

### D142 claims[1] (unestablished global → narrow summary-scope)
- OLD (base/r5): `No benchmark or calibration-measurement protocol is published on the reference; independent peer-reviewed evidence remains NOT FOUND as of this pass.`
- NEW (r6): `Captured research summary reports no benchmark or calibration-measurement protocol located in that summary scope; API body uninspected, not a global absence proof; independent peer-reviewed evidence NOT FOUND as of that captured pass.`
- Class INFERENCE retained; verification both UNRESOLVED retained; no body/fetch.

### D142 materiality_rationale (unsupported specified-contract → relevant-but-unverified lead)
- OLD: `TypeSafe API reference: contract + confidence derivation specified; no benchmark/calibration protocol; independent evidence absent.`
- NEW: `TypeSafe API reference as relevant but unverified contract lead: primary body outstanding (https://docs.typesafe.ai/api unfetched), summary-only captured note; no verified schema/confidence/version/date/body claim; MATERIAL as potential relevance only with explicit HOLD editorial ceiling (not verified, not selected).`
- materiality MATERIAL kept as potential relevance + explicit HOLD ceiling, no verified claim.

### D142 historical_attribution_caveat
- OLD: `Reference page not fetched this pass; contract facts at summary level with launch/docs corroboration.`
- NEW: `API page not fetched this pass; summary-level contract lead only with launch/docs scope notes; primary-body inspection outstanding; no verified contract/confidence facts; HOLD ceiling.`
- Removes `contract facts … corroboration` implication; explicit unverified + HOLD.

### D142 source_bindings (invalid null → omitted) + lineage_role (restored)
- OLD (r5): `"source_bindings": null` (invalid: optional array not nullable per run_evidence_v2_interactive.py:133,192-193).
- NEW (r6): key omitted exactly as base 697a (15 keys for D142: required 15 THEMATIC incl lineage_role=CORE, no source_bindings). Contexts say `key absent - omitted per optional-array contract (not null)`, no runtime bypass.
- lineage_role=CORE restored for all 4 (r3-r5 dropped it; required THEMATIC field per _validate_record:132-133 + COMMON/THEMATIC sets). D070/D071/D141 source_bindings arrays preserved (non-empty, hex16, bound task sources).

### D070/D071/D141 materiality + D141 Q2 (r5 → r6: preserved)
- r5 narrow archived-bound rationales + relevance/ledger sentences + VERIFIED-conditional + D141 rate qualifier already correct; r6 preserves byte-identical from r5 (rebuilt from base + r5 fixes, keys verified). No silent change; see delta file for byte proof.

### O10 / closure / residual (r5 → r6: preserved)
- O10 archive-aware rationale, residual 5 + closure request-shape unchanged from r5 cc4ce34 (reviewed valid; vLLM/Dynamo current-only true kept; no auto SAT). Mapped in r5 dossier §4; r6 reuses file unchanged.

## 5. Source-schema check (read-only, NOT runtime PASS)

Read `scripts/run_evidence_v2_interactive.py` `_validate_record` (lines 120-215) as DATA (never imported/executed): required = COMMON (10) + THEMATIC (5) = 15 keys; allowed = required + {source_bindings} optional; source_bindings if present must be unique non-empty string array (null fails); claims exactly {text,evidence_class,context} (context string/null only); verification exactly {target,status,finding}; entity exactly 5 keys (organization/canonical_url string/null only); lineage_route/branch/transition/inheritance_note/historical_caveat validated; THEMATIC lineage_role/branch/transition required. Full key audit in `sp-repaired-schema-read-check-r6.json`: D070/D071/D141 16 keys (15 required incl lineage_role=CORE + source_bindings non-empty hex16, bound task sources, no duplicates); D142 15 keys (15 required incl lineage_role=CORE, source_bindings omitted); only permitted nullable keys are null (entity.canonical_url, inheritance_note; claims context all non-null strings; historical_caveat strings); no unknown new fields; targets exact (D070 2, D071 1, D141 2, D142 2); evidence_class INFERENCE/VENDOR_CLAIM per reviewed scope; status PARTIAL preserved; MATERIAL kept for D142 as potential relevance + HOLD ceiling only. No validator executed, no imports, no runtime PASS claimed.

## 6. Limits + remaining gaps (READY FOR REVIEW, no acceptance)

- DATA only. No State/source write, no HIGH prepare/adopt/resume/readback, no Selection/Architecture, no R4/Draft/PDF/Human Gate. O10 + materiality + rate qualifier + D142 narrow fixes are proposal DATA; actual external Decision requires HIGH prepare on cc1c with HEAD/tree/tool pins → proof/adopt/resume/readback → independent re-review → root dispatch.
- Independent review must judge: D142 narrow INFERENCE token + summary-scope negative + HOLD-ceiling MATERIAL + absent (not null) bindings meets contract with null supplement authority (or return gap); 3 publisher literals support historical rebinding with quarantine (literal ≠ rest-of-card proof); O10 archive-aware + closure/residual unchanged adequate; keys exact per §5.
- No claim acceptance, no independent decision, no semantic PASS here.
- Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Human Commit Point.
