# SP correction final addendum r6 — independent content reviewer (preserves prior reviews, explicit correction)

Reviewer: NEW independent content reviewer (same as `reviews/sp-correction-proposal-review.md` + `...-addendum-r5.md`, both preserved byte-identical). This r6 addendum corrects prior-review misses explicitly; it does not edit prior files.
Scope: r6 DATA only. No source/state write, no HIGH prepare/adopt/resume/readback, no Selection/Architecture, no R4/Draft/PDF/Human Gate, no synthetic decision/approval.
Method: Read + stdlib hash/compare only (Read, sha256sum, python stdlib json/hashlib). Runner `scripts/run_evidence_v2_interactive.py` read as DATA (never imported/executed). No project runtime/tests/Git binary/network/Production/subagents. No reconstruct readback. New cc1c runtime read as DATA only. Setup cc1c exact773 current per root README; old producer gap not current blocker.

## 1. Prior-review correction (explicit)

Prior r4 review + r5 addendum MISSED two contract errors that root caught (§4):
- (a) `source_bindings: null` explicit is invalid. Contract `run_evidence_v2_interactive.py:133,192-193`: allowed = required15 + optional `{source_bindings}`; if present must be unique non-empty string array — null fails. Original D142 in base 697a OMITS the key (15 keys total). r3-r5 wrote explicit null (r5: all4 missing `lineage_role`, D142 16th key null). Prior reviews checked obligations/FULLDID/literals but did NOT audit actual interactive record keys vs `_validate_record`.
- (b) `lineage_role` REQUIRED THEMATIC field (`_validate_record:132-133`, `124-133`, `206-208`; COMMON10 + THEMATIC5 =15; `LINEAGE_ROLES` includes CORE). Base 697a has `lineage_role=CORE` for all4 (D070/D071/D141 16 keys incl bindings, D142 15 keys omit bindings). r3-r5 dropped it. Prior reviews missed it.
- (c) D142 claim2/materiality/caveat overstatement missed in depth: OLD claim2 `No benchmark or calibration-measurement protocol is published on the reference` is unestablished for unfetched body; OLD materiality `contract + confidence derivation specified` + caveat `contract facts … corroboration` overstated specified contract for summary-only note. Prior reviews passed claim2 as narrow INFERENCE but did not require summary-scope/HOLD narrowing. Corrected in r6 below.

## 2. r6 files (hashes verified)

- `sp-repaired-records-4-r6.json` 17947B `cca74577729ee22bbab088a6fdc30f909c2a79bd5e6781c1f4d80fac36a4d7c2` (schema `sp-repaired-records-4-r6-1`, 4 new, counts 4/156/160).
- `sp-repaired-input-assembly-r6.json` 3164B `7e3724868f743be435add00cd220606584224637070844ac9c91d6c660505d74` (explicit jq filter, full30 r4 + completeness r5 reused).
- `sp-repaired-delta-r5-r6.json` 4921B `ea24fbc20b349ec2a1a4a65d58a6a35aac1801ef66aa85bf405dd05c50d23b1b` (exact old/new field map, no silent change).
- `sp-repaired-schema-read-check-r6.json` 3203B `3e7446dbb4349e5fd33282ceda642868450dfa36dd1eaa8ab3ee7936cdd6f59f` (actual contract read, honest not runtime PASS, validator not executed).
- `sp-repaired-content-review-dossier-r6.md` 8847B `53854acedca7a7d18c0b06995c24e3a07600f67172dbc21140f8228156c3d5e0` (§4 old/new maps, §5 contract read).
- Reused unchanged: completeness-request r5 36487B `cc4ce34dc3463df5d352a5d6449c577a77555e5a5006ab7e2b13fb4d42714d0d` (O10 archive-aware LIMITATION, 15×7 + residual5 + closure request-shape), supplement-full30 r4 31522B `e2bfb30ae738b1328b1b3c5eceab1b9313d6d017cc864bce0b68c1997ca128fb` (30 real), staging r4, routing r4. Base 697a 355643B, r6 ffcd 30922B, Evidence/Views/Ledger/Completeness, S142 3751B f7ee, u1/u2/u3 wire/decoded/CDX/served as in original review (unchanged).

## 3. Actual full-record + THEMATIC schema verification (not summary)

Contract read (`run_evidence_v2_interactive.py:120-215` as DATA): required = COMMON10 (`discovery_id/status/entity/artifact_type/claims/limitations/verification/materiality/materiality_rationale/scope_dimensions`) + THEMATIC5 (`lineage_role/branch_ids/transition_ids/inheritance_note/historical_attribution_caveat`) =15; allowed = required + `{source_bindings}` optional; `source_bindings` if present must be unique non-empty string array (null fails :192-193); claims exactly `{text,evidence_class,context}` context string/null; verification exactly `{target,status,finding}`; entity exactly 5 keys org/url string/null; THEMATIC `lineage_role` in `LINEAGE_ROLES {CORE,BRIDGE,CONTEXT,PARALLEL,COMPETING,COUNTEREXAMPLE}`, `branch_ids/transition_ids` string arrays, `inheritance_note/caveat` string/null.

Base 697a actual (read): D070/D071/D141 16 keys (15 required incl `lineage_role=CORE` + `source_bindings` non-empty hex16 bound task sources `6a5ae38a…/0d550497…/95365faf…`), D142 15 keys (15 required incl `lineage_role=CORE`, `source_bindings` key absent). Target strings exact vs 697a preserved in r6 (D070 2/D071 1/D141 2/D142 2, no new split).

r6 actual: D070/D071/D141 16 keys (15 required incl `lineage_role=CORE` + `source_bindings` non-empty hex16 `ea9b086e…/793903f4…/228b8166…` bound to full30 task sources, no duplicates); D142 15 keys (15 required incl `lineage_role=CORE`, `source_bindings` key absent exactly as base, not null). Only permitted nullable keys null (`entity.canonical_url`, `inheritance_note`); all claim contexts/caveats non-null strings; no unknown fields; `evidence_class` INFERENCE (D142×2) / VENDOR_CLAIM (D070/D071/D141×3); status PARTIAL all4; `MATERIAL` kept for D142 as potential relevance + explicit HOLD ceiling in rationale (PARTIAL+MATERIAL allowed; REJECTED→NON_MATERIAL / NEEDS_MORE→HOLD only constraints :188-191, not violated). PASS — lineage restored, null removed, key counts match base.

r5 actual (for correction record): all4 missing `lineage_role`, D142 explicit null — confirms prior miss.

## 4. D142 all claims + context/rationale (not just first-token literal)

- claim0 `INDEPENDENT_EVIDENCE_NOT_FOUND_AS_OF_2026-09-21` INFERENCE, context agent-summary S142 3751B f7ee line44 verbatim, observed 2026-09-21, no body/supplement, `source_bindings key absent — omitted per optional-array contract (not null)`, no schema/math/version/date/body inferred, UNRESOLVED. Genuine token + honest absence (not null). PASS.
- claim1 NEW `Captured research summary reports no benchmark or calibration-measurement protocol located in that summary scope; API body uninspected, not a global absence proof; independent peer-reviewed evidence NOT FOUND as of that captured pass.` INFERENCE, context same S142 pass + `API body outstanding at https://docs.typesafe.ai/api, no supplement entry, key absent; records what the captured summary reports as not located in that scope, with body uninspected and no global nonexistence claim.` OLD global `published on the reference` was unestablished for unfetched body; NEW is summary-scope + uninspected + not-global-proof. Both verifications UNRESOLVED (full-body outstanding; calibration gap as captured-pass finding). PASS as narrowed negative, no global proof.
- materiality_rationale NEW `TypeSafe API reference as relevant but unverified contract lead: primary body outstanding (https://docs.typesafe.ai/api unfetched), summary-only captured note; no verified schema/confidence/version/date/body claim; MATERIAL as potential relevance only with explicit HOLD editorial ceiling (not verified, not selected).` OLD `contract + confidence derivation specified` overstated specified contract; NEW is relevant-but-unverified lead + HOLD ceiling, MATERIAL as potential relevance only. PASS.
- caveat NEW `API page not fetched this pass; summary-level contract lead only with launch/docs scope notes; primary-body inspection outstanding; no verified contract/confidence facts; HOLD ceiling.` Removes `contract facts … corroboration` implication. PASS.
- limitations `Reference page not fetched; schema/confidence-derivation details outstanding.` retained. No fetch/schema fix. If contract cannot support even this narrowed INFERENCE + absent-key + HOLD form, exact gap is `D142 body outstanding, no supplement, summary-only S142 token + summary-scope negative only, no schema/math/version/date/body verification possible` — return gap, no fetch.

## 5. Reused files still valid

- Completeness r5 `cc4ce34d`: 15×7-field per result schema, O10 archive-aware BOUND LIMITATION (served-3 Sept20/21 CDX MATCH + D142 unfetched + RLCD + indep gap + vLLM/Dynamo current-only true + 1.14 drift note, no auto SAT), residual5 == profile == interactive (no false currentONLY), closure 3-field == interactive request (not 8-field result), top extras packet-local. Stale pins only in `rationale_map old`. PASS (as reviewed in r5 addendum).
- Full30 r4 `e2bfb30a`: 30 real, 13 keys, hex16 stable, FULLDID, canonical PRIMARY_ANNOUNCEMENT/DOC + PRIMARY_OFFICIAL, `published_at null`, 27 byte-identical. Unchanged, no new source. PASS.
- 156 preserved (assembly cites `d455f7221a0addd93dd2a3c07c874fe4dfb815d3e795933882eb839e868a1ef9`, counts 160=156+4) + D165 `16f046f59e171a80c22bb0df2a159af9eafaa1ad3cfb0f9a2269ab90871e6fe2` VERIFIED 0 changes. r6 `d165_preserved` carries same; `changed_ids`/`counts.preserved` rename is packet-local (new_records keys are the contract surface, verified §3). PASS.
- D070/D071/D141 claims/verification/limitations/bindings/materiality (r5 archived-bound + relevance/ledger + VERIFIED-conditional + D141 `PLATFORM RATE LIMIT caps not measured throughput`) byte-identical from r5 (delta proves). No premature `accepted revision completed` (`until accepted revision + independent re-review` conditional). PASS.

## 6. Verdict

Prior blocking gaps (O10 false current-only, D141 rate qualifier) already closed in r5; root §4 blockers (null, lineage, D142 global/overstated contract) CLOSED in r6 with explicit old/new mapping (dossier §4 + delta), no silent change, no new fetch/schema fix.

**Final PROPOSAL_READY for normal HIGH prepare** on cc1c exact773 using r6 records `cca74577` + assembly `7e37248` + reused completeness `cc4ce34d` + full30 `e2bfb30a` + staging/routing r4 FULLDID. Actual external Decision still requires after graph: HIGH prepare with HEAD/tree/tool pins → proof/adopt/resume/readback → independent re-review → root dispatch → Selection/Architecture. No synthetic decision/approval, no semantic PASS, no acceptance. DATA only. Whole NOT_READY/DM021+022OPEN/audit unstarted/quality-adoption-savings OPEN. Stop at Human Commit Point.

## 7. Read scope

r6 records/assembly/delta/dossier/schema-check; reused r5 completeness + r4 full30/staging/routing; base 697a full records (key counts/lineage/bindings/targets) + tasks + S142 + profile/interactive completeness + `profile-completeness-result.schema.json` + runner `_validate_record:120-215` + `COMMON/THEMATIC/LINEAGE` defs (all as DATA); archive u1/u2/u3 + intake metas (hash/bytes/CDX/served re-verified via prior reviews + substring checks). No validator execution, no imports, no runtime/tests/Git/network/Production.
