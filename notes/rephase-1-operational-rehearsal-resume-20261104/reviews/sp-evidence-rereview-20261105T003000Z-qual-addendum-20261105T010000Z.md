# SP re-review qualification / final-binding addendum (narrow literal + authority corrections, original preserved)

**Role:** SAME NEW independent substantive Evidence reviewer. NOT operator/source/plan author, NOT Astra/root, NOT prior reviewer, NOT Human. No subagents.
**Original review preserved, NOT edited:** `reviews/sp-evidence-rereview-20261105T003000Z.md` 23664B `bbb0c36230c5c577330aea67a5092aea73068fb2f8b91f76fd535677c1c78aca` + machine `sp-evidence-rereview-20261105T003000Z-machine.json` 9361B `ef9699bac401282e2158689c9d36d86b32dfd8e7521a2c280783f8f98f9d25a8`.
**This addendum:** `reviews/sp-evidence-rereview-20261105T003000Z-qual-addendum-20261105T010000Z.md` + machine `sp-evidence-rereview-20261105T003000Z-qual-machine-20261105T010000Z.json` (real rehash primary).
**Bounds:** source-read/data-only stdlib `hashlib/os.lstat/json` only. Only active e84 + permitted packets `notes/rephase-1-operational-rehearsal-20261101` + `notes/rephase-1-operational-rehearsal-resume-20261104`. No project imports/run/tests/network/Production/reconstruct Git/readback. No active e84 writes. Packet-local review writes only (this addendum). SP ONLY. No State advance.

## Q1 — Literal count corrections (do not change substance, do affect recording)

Original §2/§6 phrasing is literally wrong and is corrected here without silent rewrite:

- Wrong: “7 papers + PR now bounded VERIFIED” (implies 7 papers + PR = 8 new, total 9 with D032).
- Correct: **6 papers + PR = 7 new VERIFIED from old-unsupported** (D036 EAGLE, D148 Snell, D149 s1, D150 ThinkPrune, D151 overthinking, D154 FrugalGPT + D165 PR27742) **+ retained D032 = 8 VERIFIED total** (`evidence-accepted.json` 152 PARTIAL / 8 VERIFIED). The 6-paper list is exactly D036/D148/D149/D150/D151/D154. No other paper promoted.
- Wrong: “4 living-doc/docs correctly HELD as PARTIAL/UNRESOLVED/CONTEXT” listing 5 IDs.
- Correct: **5 current-only records HELD as PARTIAL / UNRESOLVED / CONTEXT**: D070 launch, D071 concepts, D141 models, D163 vLLM recipe, D004 Dynamo. **HOLD is informal review shorthand, NOT a ledger enum.** Actual enums: record `status PARTIAL`, `verification.status UNRESOLVED`, ledger `downstream_disposition CONTEXT`, views `CONTEXT`. Do not record HOLD as enum.
- §3 title “10 papers CONFIRMED + PR COMPLETE + HF CONFIRMED + 5 current-only” remains correct as staged-Raw inventory (10 = 6 VERIFIED-new papers + 4 PARTIAL section-scope papers D027/D008/D123/D125; PR = D165; HF = D030 README; 5 = above). The §2 error was only the VERIFIED-new subset count. No body added/removed by this correction.

Effect on verdict: **none** — counts were transcription errors, authority bindings unchanged.

## Q2 — Old-view hash: actual rehash primary (no transcription authority)

Root noted reported old-view SHA differs from earlier real verification. Rehashed NOW from active e84 bytes (stdlib, no transcription):

- Old views `sources/SP-efficient-llm-2026/evidence/v2/views/accepted/50c919b9…/edition-views-accepted.json` 64227B `7a205de1010da647fd8d9af9a8b029da461faae68be4501d0406b3b116ee2a4f` — matches original §1 line 30 verbatim. **This review’s §1 used the real file hash, not the r4-manifest copy.**
- Old evidence `09f487ab…/evidence-accepted.json` 49241B `9c2543191e78a1b8e005e46f0ead9c5a10470a28406f0fd10b58fb8829c46e18` — matches §1 line 29.
- New views `2ad42d4d…` 64222B `e439db857e9e2f2547f98dfc12c9b956f220b83375d3523290f8c9937f90e9db`, new evidence `d64264268eefaf73ae83ba81e175b57badf8ad609c65893636dd4da9ba4115c1` 49237B — match §1.
- The 5 r4-manifest mismatches (61/65/60-char, 2-vs-1 byte) reported in `sp-corrected-delta-r4-20261104.json` §unresolved are **initial-plan manifest copies, REPORT ONLY, never fixed by reseal**. Harness bound real files at operation time (§8). This review binds real-file rehashes; **machine real-hash primary, MD transcription secondary.** No silent correction of old packet; original manifest preserved as deviating evidence.

Effect on verdict: **none** — no hash change, authority already real-file bound.

## Q3 — D165 authority dissection: bound pr.json vs unbound packet (no automatic pass)

Inspected actual accepted card + task-bound sources + bound body (all current bytes):

- Task binding is SINGLE: `source_bindings ["supplement-src-1ae83672998fa5fe"]` → supplement row binds ONE Raw: `raw/sp17-pr27742.json` 26122B `3728e08d0731a5faab852f32d0aee0fdd6011bf0873c7c697cb4280b0a338561` == packet `DATA.sp15-pr.json` same bytes/SHA. **Commits/comments packet files are NOT staged authority and NOT task-bound:** `DATA.s15-commits-all100.json` 256128B `4143b4ad…`, `DATA.s15-comments-p1-100.json` 271317B `c1b1f7d5…`, `DATA.s15-comments-p2-100.json` 134958B `541bd239…` remain packet DATA only.
- Bound `pr.json` body (4836 chars) **DOES contain** the numerical validation claims cited in the card: wikitext-2 `4.0068` vs `4.0126` (1 hit each), `98.0` percent (1), `QSA` (4), `PLE` (2), `97.7` GiB (1), `bit-identical` (2), `jaccard` 0.975 (1), `UD-IQ1` / `2.84` (1 each), `qwen4exp` (5), `converter` (1), AI-use disclosure. Card claims 1–3 (merged arch, validation table, gaps) are therefore **supported by the bound body at PR scope**, with limitations `no independent rebuild` + `implementation-described` + `merged = existence NOT correctness` preserved. This part needs no downgrade.
- Card finding phrase “QSA/PLE/memory/validation/gaps at PR scope **per commit messages** + validation ppl …” + “full conversation 65/65 … 144/144 … CONFIRMED in packet” **conflates bound and unbound.** Qualified holding:
  - `number 27742 / title / state closed / merged True 2026-08-27T19:32:31Z / head eaf93765 / base 732707df / commits 65 / comments 144 / 65 commits-28 files / updated 2026-09-05` are in bound `pr.json` fields — SUPPORTS merged-existence + count chronology from bound authority.
  - Detailed commit messages / comment bodies and per-date 65/65 + 144/144 completeness (`08-25–08-27`, `08-26–09-05 ≤cutoff`) are corroborated ONLY by unbound packet files — **may corroborate chronology in review context, MUST NOT support new numerical validation claims if absent from bound pr.json.** They do not add numerical validation here; all cited numbers above are already bound.
  - Corrected reading: D165 VERIFIED = **merged existence + PR-scope validation-report as stated in bound pr.json body**; packet 65+144 = **chronology corroboration only (review context), not staged authority.** The words “per commit messages” in the finding are struck as authority and retained only as chronology pointer.
- No automatic pass on unbound numbers: confirmed none needed — no card numerical claim relied SOLELY on unbound commits/comments. If a future Selection need requires commit-level detail (e.g., which commit fixed PLE conv state), that subset must be staged as NEW supplement Raw and re-reviewed; current VERIFIED does not cover it.

Effect on verdict: **BOUNDED_PROCEED unaffected with this qualification.** D165 stays VERIFIED at the narrowed scope above; it does not become PARTIAL, but its packet corroboration MUST NOT be cited as staged validation authority downstream.

## Q4 — Coverage clarification: 113240Z relied-on vs this-delta read scope (no full160 inference)

Exact unique counts, no inference:

- This delta substantively read FULL: **17 patched input records** (D036/D148/D149/D150/D154/D027/D008/D123/D125/D070/D071/D141/D163/D165/D030/D004/D151 — verification/claims/limitations/materiality/bindings) + **15 completeness rows full** + ledger 165 counts/5 CONTEXT/5 EXCLUDED spot + views counts + supplement 30 rows + 17 staged Raw SHA/bytes + operation/manifest/READY/DISPOSE_RUN/retention/delta/true-binding/plans.
- Relied-on (NOT re-extracted): **9 wrong-locator supplement cards** (D005/D061/D062/D093/D094/D098/D112/D117/D139, retained PARTIAL abstract-scope, bindings spot-checked) + **D032 launch** (retained SUPPORTS) from `113240Z` §§3–4 + `172752Z/174126Z` DATA. Prior `113240Z` itself substantively read ~12 VERIFIED + ~9 wrong-locator + ~8 loadbearing + 15 obligs — **it was never a full160 semantic PASS either.**
- Unchanged `143 = 160 − 17` = 9 wrong-locator + D032 + 133 others. Of those 133, NEITHER review claims full-body semantic verification; prior PARTIAL/abstract-scope retained ONLY where claims scoped accordingly. **Combined reviews do NOT infer full160 semantic PASS.** The “143 non-patched includes earlier 19” is therefore NOT a verified-19 subset — it is a relied-on/retained subset with explicit abstract-scope limits.
- This addendum does not expand read scope to 160 and does not upgrade any unpatched record.

Effect on verdict: **none** — clarification only; BOUNDED_PROCEED remains delta-scoped per §§2–6, not whole-corpus.

## Final binding (narrow, matters affecting BOUNDED_PROCEED stated)

- Q1 literal errors: **do NOT affect BOUNDED_PROCEED** (transcription, authority unchanged).
- Q2 hash: **does NOT affect BOUNDED_PROCEED** (real-file bound, manifest mismatch already quarantined).
- Q3 D165: **does NOT overturn BOUNDED_PROCEED** with the narrowed holding above (numericals bound; packet = chronology only; “per commit messages” struck as authority). Any downstream citation MUST use the narrowed scope; commit-detail needs require NEW staged supplement + re-review.
- Q4 coverage: **does NOT expand to full160 PASS**; BOUNDED_PROCEED stays delta-scoped to EVIDENCE_REVIEWED on authority-consumption grounds, with Selection residuals per original §9.

Original review + this addendum + corrected machine together form the review record. No State advance by reviewer. Allowed next unchanged: Root may record and advance SP to EVIDENCE_REVIEWED via normal checkpoint path; then Selection/Architecture prep only when gates hold. All other NOT-allowed per original §9 remain.

(End of qualification / final-binding addendum — 2026-11-05, SAME independent reviewer.)
