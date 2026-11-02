# SP primary-consumption NARROW UPDATE — version supplement (no overwrite of prior)

**Role:** General independent supervisory reviewer — NOT author, NOT Stage writer, NOT input editor. Read-only, data-only (stdlib hash/parse + text search), no project runtime/network/Git readback/State write/source edit/new Gate. No subagents. SP ONLY.

**Files:**
- This update: `notes/rephase-1-operational-rehearsal-20261101/reviews/primary-consumption-efficient-llm-20261101T174126Z.md`
- Machine findings (new version, separate): `…/primary-consumption-efficient-llm-20261101T174126Z.json` (hashes generated via `hashlib`, not manual truncation)
- Prior consumption (preserved, NOT overwritten): `…/primary-consumption-efficient-llm-20261101T172752Z.md` + `.json` (17-body SUPPORTS/PARTIAL table)
- Prior decision (retained, NOT closed): `reviews/evidence-efficient-llm-review-20261101T113240Z.md` §§3–5/§7 CHANGES_REQUIRED (11/12 VERIFIED unsupported + loadbearing PARTIAL overclaims + O05/O04/O11 rationale)
- Supplement read FULL: `publisher-intake-supplement-20261101T172535Z/README.md` + `manifest.json` (12 new DATA, 1124966B; original 40 untouched)
- Original intake referenced: `publisher-intake-20261101T163426Z/` 40 DATA (bodies + API/abs, retrieval 2026-11-01T16:35:36–16:36:42Z)

**Cutoff:** `as_of 2026-09-21T16:10:00Z`. Retrieval vs revision dates kept distinct (published / updated / observed / commit / Last-Modified are separate). Later LastModified does NOT by itself disprove earlier publication — the initial “contradicts date” framing for living docs is WITHDRAWN except where API/abs version history positively contradicts (E151 below, handled as lineage correction, not silent root fix).

**Read scope (narrow — NOT another all-66 baseline review):** supplement 12 DATA + HF README full read (§4) + PR/commits/comments metadata pointers (§3) + vLLM file-history (§5) + TypeSafe date strings (§5) + original API/abs histories for 10 arXiv (§2). No re-read of whole 66pp reader, no all-160 recount (prior coverage stands).

---

## 1. New supplement pins (12 DATA, exact)

| gid | file | bytes | SHA256 | result |
|---|---|---|---|---|
| s15-commits-all100 | DATA.s15-commits-all100.json | 256128 | `4143b4ad4569ca8e44473613deef9dd3c8e6aa2b94e6f8ddbe4d9a1f3fbacb0e` | 65/65 commits, 2026-08-25–08-27 |
| s15-comments-p1-100 | DATA.s15-comments-p1-100.json | 271317 | `c1b1f7d5e6d92c9b3a518b5e665a67beaec48142274ffe4ec540309e8e325b51` | 100/144 comments |
| s15-comments-p2-100 | DATA.s15-comments-p2-100.json | 134958 | `541bd239ff4a9209d75d97f810a412178b79611fbf87df102eb0d07d428e4750` | 44/144 comments |
| s14-commits-file-correct | DATA.s14-commits-file-correct.json | 61054 | `747e5df2c2ab5861027e981b73a212072aec5ef9dafecae7e3f9bf8880b66eed` | vllm repo file history 13 commits 2026-10-17–10-31, 0/13 ≤ cutoff |
| s14-file-main-correct | DATA.s14-file-main-correct.json | 112399 | `b2ff92429c4fc7f2619847a4a79246bef7ab24d930ceaf750d890a8a7ccd4754` | file @main sha `29a4c64…`, size 80832, current |
| s14-commit-e0d-correct | DATA.s14-commit-e0d-correct.json | 8284 | `1d93055ac1833e20778792c54ed9dff29ff9ce7241b68c0f2bd085a03980cdd2` | blob commit `e0d00e4…` author 2026-11-01 (> cutoff, current) |
| s14-commits-file | DATA.s14-commits-file.json | 2 | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | `[]` wrong repo (preserved) |
| s14-file-main | DATA.s14-file-main.json | 127 | `e45906ce02e79f16fb87a838d86bb4e497e37a9591f97608fa013bbcd8b9cbc2` | 404 wrong repo (preserved) |
| s14-commit-e0d00e4 | DATA.s14-commit-e0d00e4.json | 174 | `a5fb0d59c0428c96cfc544a347b8942849e95a1f717d8d3904af8016034248cd` | 422 wrong repo (preserved) |
| s16-commits-main-html | DATA.s16-commits-main.html | 267351 | `b32414f94dc49dbfe91a5953fa67964f00d5bc3a17d74bb6678ecb6d5f97f406` | 17 commits (11 Sep 10 ≤ cutoff + 6 Oct) |
| s16-commits | DATA.s16-commits.json | 62 | `4f1d517745cabbba311752b8d9f602fe20433024713238869e5bd7ee092a2292` | 404 API endpoint (preserved failure) |
| s16-README-dba1be0 | DATA.s16-README-dba1be0.md | 13110 | `347c9db4e5506acb531cbc3b724407ab88e9af8781679152f0823d7bac16d251` | README @`dba1be0` 2026-09-10T08:18:10Z, historical body |

Transport: supplement 12 requests (10 exit-0 + 2 exit-1 gh-notfound preserved as 404/422 proof), 9 HTTP200 + 3 HTTP404/422 preserved. No overwrite of original 40; new gids `s14-*/s15-*/s16-*` distinct.

---

## 2. 10 arXiv precutoff KEEP — no new body (API + abs history governs)

All 10 selected versions are latest≤cutoff per locally verified API/abs histories (supplement did_decisions, no new fetch by reviewer):

- EAGLE v3 2025-03-04, Snell v1 2024-08-06, s1 v3 2025-03-01, ThinkPrune v1 2025-04-02, FrugalGPT v1 (API 2023-05-09 vs P5 05-10: 1-day record-vs-publication diff, UNVERIFIED not false), Kimi v2 2025-11-01 (history v1 10-30 / v2 11-01; P5 10-29 1-day diff), Qwen v1 2026-08-31, V4.1 v1 2026-09-17 (P5 09-18 1-day diff), V3.2 v1 2025-12-02.
- **Overthinking E151: KEEP v1 2026-04-12, NO v2 exists.** API `id …/abs/2604.10739v1 pub 2026-04-12 upd 2026-04-12` + abs `[v1 2026-04-12 only, no v2]` as of 2026-11-01 retrieval. P5 `published_at 2026-08-24` has NO corresponding v2 in history — treated as UNVERIFIED record date (may refer to revision/record date, not first publication), NOT marked false, NOT coerced. **No August v2 to capture; v1 `c4254e53…` remains the cutoff-available body.** Prior consumption §2A row 5 SUPPORTS-metrics stands with corrected date (see §6).

No unconditional “all 17 historical VERIFIED”: these 10 are CONFIRMED as cutoff-available bodies with SUPPORTS/PARTIAL per prior table; semantic VERIFIED still requires NEW bound run (§8).

---

## 3. PR27742 now COMPLETE — dated merge/validation confirmable within PROJECT_CLAIM scope

- PR: number 27742, title `model: add Qwen3.8-Flash-Next (qwen4exp)` (P5 descriptive title differs — flagged as description, not mismatch), state closed, **merged True `2026-08-27T19:32:31Z`**, head `eaf93765572e794b8e3754fe45adbe12d381e997`, base `732707dff265be513347b02911e1ddf7e1f386`, 65 commits / 28 files / +2881/-38, updated `2026-09-05T20:34:42Z` (ORIG `DATA.sp15-pr.json`).
- Commits: SUPP `s15-commits-all100.json` 65/65, earliest `2026-08-25T14:00:29Z` → latest `2026-08-27T19:28:11Z` (ALL ≤ cutoff). Retrieval 2026-11-01 does NOT change historical commit dates. Example validation-relevant: `6e5b8b7e 2026-08-25 GGUF arch+converter` (converter/QSA/PLE plumbing).
- Comments: SUPP p1-100 + p2-100 = **144/144**, earliest `2026-08-26T13:48:19Z` → latest `2026-09-05T20:34:41Z` (ALL ≤ cutoff). Sample: `2026-08-26T16:34:51Z coder543` mmap-offload report (DGX Spark 22s vs 224s) — implementation-experience scope, not correctness proof.
- **Finding:** historical merge + dated validation-relevant facts (merged status, 65 commits, QSA/PLE support, wikitext ppl 4.0068/4.0126, 98.0% prose, QSA bit-identical, PLE indices, UD-IQ1 2.84e-03, AI-use disclosure per prior card) are **CONFIRMED as dated PROJECT_CLAIM within `merged 08-27 / discussion ≤ 09-05` scope** — NOT independent correctness/rebuild. Category discipline retained: merged PR = existence authority only. Suggested input: D165 **PARTIAL → VERIFIED-able for `merged existence + dated validation-report scope` ONLY after NEW bound run citing `4143b4ad…(65) + c1b1f7d5…(100) + 541bd239…(44)` with `full-conversation consumed 144/144 ≤ cutoff; correctness NOT independently verified, no rebuild claimed`. No further PR fetch needed.

---

## 4. HF historical README @dba1be0 — inspect actual content for D030 (NOT current Oct16 body)

- Commits HTML `b32414f9…` (same-document `commits/main`, 267KB): 17 commits, **11 Sep 10 ≤ cutoff + 6 Oct > cutoff**, latest≤cutoff `dba1be0 2026-09-10T08:18:10Z` (matches P5 09-10 — now corroborated as commit date, previously UNVERIFIED). API `/commits` 404 + wrong-repo attempts preserved as failures (not gaps).
- README `347c9db4…` 13110B @`dba1be0` (NO weights): full read. Contains for D030: `DeepSeek-V4.1-Flash … 552B backbone … 1M context` (§Introduction) ; `CED … 8B prefill / 16B decode` ; `CSA2 Full/Reindex/Reuse … Hierarchical Sparse Indexer … FP4 main KV (E2M1, E4M3/16ch) … 890 bytes/token ~1/4 … SWA Bounded Replay ~1/8 persistent` ; `Single-Pass mHC … Engram 196B … DSpark (semi-autoregressive, confidence-scheduled)` ; `1 shared + 384 routed experts, 6/token` ; `45T tokens … 64K … 1M @34T` ; `reasoning_effort 1–100 … temp 1.0 top_p 0.95` ; Base table `# Backbone 552B / Activated 8B/16B` + instruct tables with harness/scaffold conditions (Terminal-Bench 2.1/3.0/4.0, DeepSWE v1.1, harness names, `temperature/top_p`, 1M context, max_steps=500, no-network) ; license MIT ; `deepseek-recipe` Rust link ; NO MXFP4/MXFP8/B200-conditionality strings in this README (FP4 only; MXFP absent — searched).
- **Finding:** exact README **CONFIRMED ≤ cutoff** and **closes D030 spec scope for CED/CSA/Engram/DSpark/552B/8B/16B/890B/1/4/1/8/45T/effort/harness-conditional eval** independently of vLLM recipe. It does **NOT** close MXFP4/MXFP8/B200-conditionality (absent here) — that remains with V41 report (section-scope, per-figure outstanding) + vLLM current-only. Suggested input: D030 **PARTIAL → VERIFIED-able for `spec-identity scope` ONLY** citing `347c9db4… @dba1be0 2026-09-10` + sections above with `MXFP/B200 outstanding, current Oct16 card NOT cited`.
- **Do NOT pretend D163 historical doc available:** this README does NOT substitute for vLLM recipe history (see §5). D030 closure is independent-card scope, not cross-doc proof.

---

## 5. Residual doc5 — still UNCONFIRMED, materiality vs capture need (no blanket VERIFIED)

Residual 5 = D070/D071/D141 (TypeSafe 3) + D163 (vLLM) + D004 (Dynamo). All 5 are **material to current question** (Jev mandatory O10; vLLM/Dynamo deployment O04/O08/O11 capstone) and therefore currently **HOLD/CONTEXT with explicit LIMITATION** is the honest bound status — NOT exclusion, NOT VERIFIED. Required new historical capture differs per doc:

- **TypeSafe 3 — UNCONFIRMED current-only, use-with-quarantine (no new fetch by supplement; local parse suffices):**
  - Launch: `date 2026-09-15T00:00:00.000Z` field PRESENT in current bytes + `Published Oct 28, 2026` + SSR `2026-10-27` + Last-Modified Oct 28 — BOTH true (MIXED). 09-15 field supports P5 as UNVERIFIED (not false); Oct 27–28 modification does NOT disprove Sep publication, but current bytes do NOT prove 09-21 revision.
  - Concepts `dateModified 2026-10-14`, no `datePublished`; Models `dateModified 2026-11-01`, table now 1.13 + 1.14 (1.13 string present ≠ 09-21 proof; 1.14 drift noted).
  - **Disposition:** keep current-only Raw for archival comparison with vendor quarantine; do NOT elevate asof status. For O10 (mandatory Jev, reproduction thin by design): **HOLD as MATERIAL with explicit LIMITATION** (`launch/concepts/models vendor-quarantined, independent reproduction outstanding, 09-21 revision UNCONFIRMED`) is sufficient for Selection/Architecture discussion — historical VERIFIED requires 09-21 revision or narrower PARTIAL scope (e.g., `launch-announcement scope as current lead only`), NOT a new broad crawl.
- **vLLM recipe — CURRENT ONLY + gap PROVEN (highest drift risk retained):**
  - Correct repo `vllm-project/vllm` (Edit/blob hrefs in current HTML); file `@main` sha `29a4c64…` size 80832 (current Nov 01); blob commit `e0d00e4…` author 2026-11-01 (> cutoff); file history 13 commits **2026-10-17–10-31, 0/13 ≤ cutoff** (`Host model recipes` created Oct 17 + `Sync … recipes#1136,#1137`); wrong-repo `recipes` path empty/404/422 preserved.
  - Historical source likely in `vllm-project/recipes#1136,#1137` per Oct 17 sync message — **exact path unknown, STOP exact need, no broad clone**.
  - **Disposition:** current bytes usable ONLY with topology-conditional quarantine (`pinned-09-20 UNVERIFIED, Oct17–31 history proves current path did not exist ≤ cutoff in vllm repo`). For O04/O11/D163: **HOLD/CONTEXT with LIMITATION** (`floor/CED/layout/AMD per-SKU from current observation, NOT historical proof`); historical VERIFIED requires exact recipes-repo path (Human exact need) — do NOT infer. Pinned-09-20 claim stays UNVERIFIED.
- **Dynamo — UNCONFIRMED (dev current only):** MD 16535B dev header + version index + kustomization links (recipe infra, NOT doc source); no direct Edit link for MD itself; FP4/DSpark/disaggregation present, FP8 exact-string absent (downstream check, not fetch fault). **Disposition:** **HOLD/CONTEXT with LIMITATION** (`locator-bound role + disaggregation wording only; per-topology precision matrix UNCONSUMED`); NO new repo guess. **Old D004 corroboration must NOT cite unsupported historical vLLM** — sibling chain stays PENDING on both legs.

No blanket need: all-17 VERIFIED is NOT required. Appropriately bounded PARTIAL/CONTEXT/HOLD with explicit LIMITATION is the correct task status where primary supports attributed/bounded claims (papers §2 + D030 README + PR merge + D032/supplement positives).

---

## 6. Corrected paper date E151 — upstream lineage, no Discovery rewrite

- Current input (proposed `interactive-evidence`, r2-adapted) carries `published_at 2026-08-24` / `event_date 2026-08-24` for `overthinking-2026` (EFF-D151). Supplement proves via API (`pub 2026-04-12 upd 2026-04-12`) + abs (`[v1 2026-04-12 only, no v2]`) + PDF `arXiv:2604.10739v1 [cs.AI] 12 Apr 2026` (p1) that **only v1 2026-04-12 exists** as of 2026-11-01.
- **Temporal finding to record in NEW proposed input (NOT a Discovery rewrite):** `evidence record event_date 2026-04-12 (API/abs/PDF v1, only version) EXPLICITLY CONTRADICTS Discovery published_at 2026-08-24 note; Discovery bytes preserved unchanged per defect lineage (wrong-locator/supplement pattern deferred to Sol); evidence cites v1 body `c4254e53…` with corrected date + P5 08-24 preserved as UNVERIFIED record-date claim.`
- **Do NOT silently fix root:** accepted `discovery-accepted-v2.json` (`2413dbe2…`) stays byte-identical; NO `local:` rewrite, NO accepted-Discovery edit. Upstream data lineage = API → abs → version-pinned PDF → supplement decision → NEW evidence record (with contradiction note), NOT Discovery mutation.
- Safe claim wording for E151: `Overthinking (v1 2026-04-12, only version ≤ cutoff): flip/CI/cost-utility claims per §§3.3/5 + Table 3/Fig.3 at body scope; P5 08-24 date NOT cited; effort-control binding corroborated via consumed recipe where applicable; causal-mechanism at section scope.`

---

## 7. D030 vs D163 vs D004 discipline (final)

- **D030 MAY close spec-identity scope on historical README alone** (`347c9db4… @dba1be0`, §§ CED/CSA/Engram/DSpark/552B/8B/16B/890B/45T/effort/harness tables + MIT license) — independent of vLLM recipe. MXFP4/MXFP8/B200-conditionality stays OUT (absent here; with V41 report section-scope + vLLM current-only).
- **Do NOT pretend D163 historical doc available:** vLLM history gap proven (§5); D163 stays PARTIAL-current with highest-drift LIMITATION.
- **Old D004 corroboration (`sibling D163 fully consumed`) is WITHDRAWN as stated:** both legs PENDING (Dynamo dev-current + vLLM current-only). D004 stays PARTIAL with `topology/precision UNCONSUMED`, citing dev-current role only.

---

## 8. Minimal correct input plan per DID (verified-target scopes + safe wording)

Operator (NOT reviewer) applies to NEW `interactive-evidence` re-proposal + NEW supplement binding + NEW accept; NO file-edit downgrade of current cards; NO State advance by reviewer:

| DID | verified-target scope for NEW input | safe claim wording (version/license/benchmark conditions) |
|---|---|---|
| D036/D148/D149/D150/D154 | `full-body verification: VERIFIED-able` at cited vN scope (EAGLE §5/Fig.1; Snell §7; s1 §§2–3; ThinkPrune §§3.3/5+Table1/2; FrugalGPT §4/Table3) with `ablations/appendices/formulation outstanding` kept | `… (vN < cutoff, body `sha…` §§ cited; benchmark/harness-bound where stated; no cross-condition ranking)` |
| D151 | `full-body verification: VERIFIED-able with corrected date 2026-04-12` | `… (v1 2026-04-12 only version; P5 08-24 UNVERIFIED record date, Discovery note explicitly contradicted, NOT rewritten)` |
| D027/D008/D123/D125 | `section-level verification: VERIFIED-able` (KDA/identical-recipe/75%/6× + license flag; Qwen Tab.11 + 1/3–1/9 vendor-scope; V41 arch/map + Appx UNCONSUMED; V3.2 DSA/prototype) with per-figure/ablation/license outstanding | `… (vN …; vendor self-comparison / identical-recipe / benchmark-bound scope preserved; per-figure NOT cited)` |
| D032 + 9 wrong-locator + D119/D128 | unchanged (already bounded) | keep supplement/abstract scope wording |
| D165 | `merged existence: VERIFIED-able` + `validation/gaps: PARTIAL (144/144 discussion consumed)` | `PR27742 merged 2026-08-27 head eaf93765 (65 commits 08-25–08-27) + discussion 08-26–09-05 (144) support existence/validation-report scope; correctness NOT independently verified, no rebuild` — cite `4143b4ad… + c1b1f7d5… + 541bd239…` + commit/comment pointers (§3) |
| D030 | `spec-identity: VERIFIED-able` on README scope; `MXFP/B200: PARTIAL` | `… (README @dba1be0 2026-09-10 `347c9db4…` §§ CED/CSA/Engram/DSpark/552B/8B/16B/890B/45T/effort/harness; MXFP/B200 with V41 section-scope + vLLM current-only, quarantined)` |
| D070/D071/D141 | `launch/concepts/models consumption: PARTIAL-current` | `… (current 2026-11-01 bytes, vendor-quarantined; 09-21 revision UNCONFIRMED; 1.13 observed with 1.14 drift; NO asof VERIFIED)` |
| D163 | `recipe/version conditions: PARTIAL-current` | `… (current 2026-11-01 bytes, topology-conditional + DSpark-only wording; pinned-09-20 UNVERIFIED; Oct17–31 history proves current-path gap)` |
| D004 | `locator-bound role: PARTIAL-current` | `… (dev-current MD only; per-topology matrix UNCONSUMED; NO historical-vLLM corroboration cited)` |

Completeness O05/O04/O11: replace blanket `body-consumed` with per-body vN + scope + outstanding list above; keep LIMITED overall; no auto-complete.

---

## 9. Remaining authority gaps (exact) + allowed next (retain CHANGES)

- **Gaps:** vLLM historical YAML ≤ cutoff (exact recipes-repo path unknown per §5 — Human exact need, no broad clone); Dynamo doc source link (STOP, no new repo guess); TypeSafe 09-21 revisions (or accept PARTIAL-current per §5); PR pages complete (CLOSED); HF README closed (CLOSED); 10 arXiv closed as bodies (semantic re-review still needed for VERIFIED).
- **Allowed next:** operator stages NEW supplement (17 + README `347c9db4…` + PR complete) → re-proposes input per §8 (with E151 contradiction note + O05/O04/O11 rewrites) → re-runs normal Evidence accept → requests fresh independent Evidence review of NEW bound artifacts. **Retain root CHANGES_REQUIRED** (`113240Z`) until that NEW review passes. NO whole-Evidence PASS before fresh products bound; NO State advance/checkpoint by reviewer; NO new Gate; NO source-code fix; NO asof elevation of current-only Raw (retained for archival comparison only).

**Attribution:** General independent supervisory reviewer. Binds §1 hashes + HF README/PR/commit pointers + retrieval-vs-revision dates above. No semantic publication PASS, no adoption, no savings, no full-corpus claim.

(End of narrow supplement update — 2026-11-01.)
