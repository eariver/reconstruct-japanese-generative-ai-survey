# W34 Selection proposal + Architecture structure DATA (author v1)

**Role:** W34 research/editorial proposal AUTHOR (not independent reviewer, not Sol/Astra/Human). **Date:** 2026-11-05. **Unit:** new Selection/Architecture preparation after Evidence-correction BOUNDED CLOSEOUT (read packet README + preceding assessment §5 + root closeout FULL + independent §9 FINAL-BINDING before use).

**Instance (only):** `.rephase-1-editorial-runtime/evidence-scaling-w34-retry-20261103T172327Z/candidate-work`, epoch `e84a82aca000c990597ea8cf60f548e2ff187bd1` parent `48082356`. **State:** `EVIDENCE_REVIEWED` `d7acd29b…` 4087B. **Checkpoint:** `CANDIDATES_NORMALIZED.json` `0979f9f7…` 4549B binding 4 refs (Evidence `edf21e4d…`126592B 409, Views `3777133c…`159498B 409, Ledger `f089cc4e…`186202B 439, Completeness `e8c432dd…`71532B 3 LIMITED). **Counts:** 409 Evidence (38 VERIFIED / 363 PARTIAL / 8 NEEDS_MORE), 439 Ledger (358 CONTEXT / 41 MATERIAL / 10 HOLD / 26 EXCLUDED / 4 DUPLICATE), window `2026-08-14T18:00-04:00–2026-08-21T18:00-04:00 = UTC [2026-08-14T22:00Z, 2026-08-21T22:00Z)`. Full pins + exact read scope in `w34-read-scope-and-pins.json`; per-DID machine in `w34-per-did-disposition-machine.json`. Japanese dossier in `w34-human-dossier-draft-ja.md`.

**No active writes:** this packet is NEW author DATA only (`w34-*`). Active State/products unchanged, no Selection/Architecture API JSON, no Draft/PDF, no Human Gate request, no independent approval claimed. Existing old reviews/accepted immutable.

## 1. Principles (governance-bound)

- **Source-bound:** all assignments resolve via checkpoint-bound 4 refs + ledger task linkage, not arbitrary accepted-dir scan or historical baseline products. Shipping final139/771 DIRECT409 unchanged; runtime test-only `d486` vs delivered `7b86` preserved.
- **Chronology honesty:** 11 PARTIAL MATERIAL with boundary-date load-bearing timing (Aug14 vs 22Z start, Aug21 vs 22Z end, Sep8 capture Entry-dating) are content-VERIFIED but timing-UNRESOLVED. They appear ONLY with restricted role/context (`SUPPORTING_EVIDENCE` + explicit `date-level only, no clock-time proof`), never as confirmed-W34 `FEATURE_CORE` events. No PARTIAL chronology asserted as confirmed W34 event.
- **No status upgrade:** `VERIFIED/PARTIAL/NEEDS_MORE` and `MATERIAL/CONTEXT/HOLD` are original canonical labels, not new semantic PASS. Vendor numbers stay `VENDOR_CLAIM` with `no independent reproduction`; researcher claims stay `AUTHOR_CLAIM`; SOCIAL stays `SOCIAL_OBSERVATION`. `PRIMARY_OFFICIAL` binding alone never treated as consumed.
- **Coherent coverage, not budget:** no arbitrary top-N, year-group, or page-count cutoff. Selection follows meaning/duplicate/sufficiency: clean W34 deltas as core, docs/how-to merged as boxes, boundary items qualified, duplicates collapsed, 180-bucket (319 arxiv) omitted for hash-only/maker-reported reasons after distinct-body check, not shallow exclusion.
- **Not copying historical 41/7:** baseline `41 selected / 7 packages / 12pp` is comparison only. This proposal coincidentally also touches 41 MATERIAL rows but with different thesis (5 packages, FEATURE 12 / SECTION 12 / SUPPORTING 17 with 11 qualified), different page target (16–18pp), and explicit chronology/carry-over/duplication handling. No historical package allocation reused.
- **Compression audit:** governance §4.4 triggers if `SELECTED<=1` while `non-DROP>=20` or `VERIFIED>=10`. Here `non-DROP=409`, `VERIFIED=38`, `SELECTED positive=41` → trigger condition NOT met (41>1). Counterfactual still tested in §7: full arxiv consumption could support an additional technical package but would not displace VERIFIED core; sparse 1-package alternative rejected.
- **Taskless DROP lawful:** 30 non-evidenced rows (26 EXCLUDED + 4 DUPLICATE, 0 tasks/0 views) are screening `DROP` with O_EXCL-style history preserved in ledger; no evidence tasks existed to dispose. Lawful without normal Evidence run. Carry-over C076/C077 included here with explicit disposal (§5).

## 2. Proposed Architecture (5 packages, 16–18pp target)

**Reader purpose:** Weekly magazine reader asks “what materially changed in generative AI for Aug14–21, and why now?” Thesis: **W34 is a distribution-and-governance week — frontier capabilities reach users through Bedrock/Enterprise/IDE/chat surfaces with new pricing, while agent platforms GA the pay-and-collaborate layer and safety/governance sets the terms.** Technical vs business mix kept: ~60% technical mechanisms/controls, ~40% pricing/distribution/infra/economics; vendor framing quarantined.

| Pkg | Title (draft) | Role mix | pp | Takeaway |
|---|---|---|---|---|
| P1 | Frontier availability, pricing & distribution | FEATURE 4 + SECTION 4 + SUPPORTING 4 (qualified) | 4 | Where models run and what they cost changed: Sol promo, Bedrock expansions, DeepSeek repricing, Alibaba tables; boundary releases date-qualified |
| P2 | Agent platform GA wave — build, pay, collaborate | FEATURE 4 + SECTION 3 + SUPPORTING 4 (merged box) | 5 | Agents can now transact and co-work: Payments, Computer Use/Skills/Files, Slack Code, Agentic Search; Alipay/Dogwood/Runway as parallels; AgentCore patterns as one box |
| P3 | Enterprise developer surfaces & controls | SECTION 2 + SUPPORTING 6 (all qualified) | 3 | IT/admin view: Computer History expansion, Apple Messages (scope-qualified), Copilot trio snapshots (Sep8-qualified), Antigravity bundle/addition split, CLI/free-mode context |
| P4 | Safety, security & frontier governance | FEATURE 2 + SECTION 2 + SUPPORTING 3 (1 researcher-only + 2 qualified) | 3 | Terms of deployment: Astra pacing, ZDR/Private Safety, Teens (observation-dated), KEV catalog; CoSnitch researcher-only; watermark date-qualified; Defenders essay as framing |
| P5 | Infrastructure, economics & creative distribution | FEATURE 2 + SECTION 1 + SUPPORTING 2 (qualified) | 2 | Money/metal/media: PORTS-Pike 8GW, Stripe/OpenRouter, Firefly GA; Pika family date-qualified |

Total positive 41 rows (12 FEATURE_CORE / 12 SECTION_CORE / 17 SUPPORTING_EVIDENCE with 11 timing/researcher-qualified). HOLD 10 → HOLD_OUT, CONTEXT 358 → non-selected context, DROP 30 → EXCLUDE. Page allocation respects `editorial_constraints` (16 target, 24 max, late-breaking post-cutoff stays out, HOLD/excluded not drafted).

### P1 — Frontier availability, pricing & distribution (4pp)
- **Primary (FEATURE_CORE, clean):** c017 Sol promo ($4/0.40/20, Nov21 window, Terra/Luna separated, Sep3 mirror excluded); c023 Grok Bedrock GA (500K, cross-region, Aug12 base preserved); c030 Bedrock GPT-5.6 cross-region (25+ regions, Responses/Converse/Chat); c040 DeepSeek V4-Pro repricing (Aug16 switch, Aug13 GA background, tariff figures secondary-only).
- **Section (SECTION_CORE, clean date-level):** c018 Imagen shutdown/migration (Gemini-API Aug17, Vertex Jun30 unresolved); kimi-k3 Aug19 + wan-prime Aug20 tables (provider availability, kept separate from Runway Wan); Memory JSON Aug20 (capability, no quality claim).
- **Supporting qualified (SUPPORTING_EVIDENCE, date-level only):** c039 Qwen3.8, c022 Vision-Exp, c045 regional processing, c066 Grok Bot expansion — each content-VERIFIED, timing UNRESOLVED vs 22Z, presented as “date-level placement, clock-time proof absent” sidebars, not main-event headlines.
- **Supported takeaway:** distribution/pricing moved more than base-model novelty in W34.
- **Open/negative:** exact Aug14/21 clock times unresolved; post-promo pricing, region-exhaustive availability, benchmark parity all vendor-stated.

### P2 — Agent platform GA wave (5pp)
- **Primary:** c010 Payments (402/stablecoin/MPP, budgets/TTLs, Identity/Observability); c011 Computer Use/Skills/Files GA (screenshots vs structural browser-use, 1TB/org, Foundry also); c012 Slack Code (diffs/Block Kit/HTML/canvas, Claude/Devin/Copilot/Vercel live, ChatGPT soon); c007 Alipay commerce (Skills/MCP/AHA, Ah Bao) as commerce parallel.
- **Section:** c019 Agentic Search (find/open/navigate/read/grep, FinanceBench/OfficePro maker-reported); c031 Dogwood authoring (NL→Cedar, gateway enforcement, Aug6 background separated); c047 Runway MCP (list/open/tweak/run, Wan separated).
- **Merged box (SUPPORTING, not separate cores):** c087 + c104 + c105 + Memory JSON as one “AgentCore control-plane patterns” box (gateway-intercepted evaluation, user-auth propagation, async task-token/durable, JSON extraction). Rationale: steady-state docs/how-to, not dated launches; merging avoids inflating core count and preserves sufficiency without implying launches.
- **Takeaway:** pay-and-collaborate layer GA’d together; mechanisms described, outcomes not measured.
- **Open:** regional/fiat coverage, latency/quality, validation completeness all vendor-described.

### P3 — Enterprise developer surfaces (3pp)
- **Section clean:** c052 Computer History expansion (Aug20 EEA/CH/UK Pro, optional/off-by-default, screenshot-vs-audio boundary); c096 Apple Messages plugin (read/search/prepare/send with approval-by-default; Apple-silicon/Work-Codex scope UNRESOLVED qualifier, no Apple endorsement).
- **Qualified trio (SUPPORTING, Sep8-capture qualifier):** c099 JetBrains, c100 Slack, c101 Teams — feature content VERIFIED in Sep8 snapshots, entry-dating UNRESOLVED (changelog context + Discovery, not primary date). Presented as “observed snapshots suggesting W34, not confirmed W34 events” with rollout specifics absent.
- **Split:** c102 Antigravity — Aug20 bundle (Standard/Plus + admin) VERIFIED internal as section-level; Aug21 Cloud-blog addition (pooled quotas/caps/audit/MCP/browser) UNRESOLVED no-clock as qualified supporting.
- **Context (SUPPORTING):** Kimi CLI v0.37/0.38, Replit Luna free-mode (vendor rationale only).
- **Takeaway:** admin/IDE/chat integration is where W34 lands for enterprises; dating precision is the limit.
- **Open:** plan eligibility, quality/limits, console verification needed.

### P4 — Safety, security & governance (3pp)
- **Primary:** c005 Astra pacing (2-week pause, largest run on hold, sandboxing/isolation/30-min alert/deeper alignment; Critical preliminary, 20% overhead estimate); c008 ZDR + Private Safety preview (eligible frontier, cross-interaction signals without content, Sep white paper pending, CSAM carve-out policy-level).
- **Section:** c004 Teens (auto-routing, safeguards, Study Mode/Model Spec/Blueprint; effectiveness vendor-described; timing via Aug18 first-observation, not dateline); c006 Ray KEV (Aug17 feed catalog fact only; shell uncaptured, exploitation/vendor-fix scope needs advisory/NVD).
- **Researcher-only supporting:** c055 CoSnitch (Varonis 265KB body supports 3-flaw chain, Aug18 server patches, Copilot Personal scope, no exploitation observed; MSRC 2717B shell uncaptured, CVE/severity researcher-attributed, no vendor corroboration). Presented as researcher finding, not vendor-confirmed CVE.
- **Qualified supporting:** c002 watermark (token-choice for EU AI Act, no practical impact vendor-described; Aug14 date-only vs 22Z unresolved; no detector); Defenders essay as framing sidebar (watershed thesis, not release).
- **Takeaway:** deployment terms tightened while capabilities spread; all strong claims remain vendor/researcher-attributed.
- **Open:** detector availability, age-estimation effectiveness, KEV exploitation scope, MSRC bytes.

### P5 — Infrastructure, economics & creative distribution (2pp)
- **Primary:** c026 PORTS-Pike (8GW-IT, SB/NVIDIA/DOE, pay-as-completed, 800MW 2028 plan vs completed fact); c003 Stripe/OpenRouter (Aug19 agreement, mission/name/product continuity; $7–8B press-excluded, scale figures company-reported).
- **Section:** c091 Firefly audio (Music/Speech/SFX GA, commercially-safe vendor-framed, license terms not captured).
- **Qualified supporting:** c020 Pika Audio family (Soundtrack/SFX/Speech/Music + prices VERIFIED; Aug14 date-only vs 22Z unresolved; 9x/20x multiples vendor-framed; Aug18 posts are follow-ups, not 4 launches).
- **Takeaway:** capital/compute/creative-tooling moved with distribution, not just models.
- **Business/technical balance:** this package carries business weight so P1–P4 can stay technical; vendor economics never presented as measured facts.

**Paper Watch:** explicitly omitted as package. 319 arxiv CONTEXT (180-bucket `cs-ai.atom` concentration noted in Screening) are distinct per-DID bodies (112–556KB HTML, e.g., 14927/14967/14927 lanes/methods verified distinct) but hash-only PARTIAL, maker-reported, no reproduction, ~314 not fully read. Shallow top-N/year-group exclusion NOT used; omission reason is authority-consumption insufficiency, not count. If fully consumed, a 6th technical package (retrieval/agents/eval) could emerge — tested as counterfactual in §7 — but would supplement, not displace, VERIFIED core.

## 3. All-439 dispositions (summary; full machine is authority)

- **FEATURE_CORE 12 + SECTION_CORE 12 + SUPPORTING_EVIDENCE 17 = 41 positive** as above (11 PARTIAL qualified, 6 docs/how-to merged, 0 HOLD promoted, 0 DROP promoted).
- **HOLD_OUT 10:** c033 (Benchmarks absent), c035 (Vera Rubin X-only), c038 (SenseNova timestamp), c051 (romance-bait event nature), c053 (Seedance Jul31 background, no W34 delta), c054 (MediaTek X-only), c057 (MOU 401, no text), c065 (Ox Alpha SOCIAL_OBSERVATION only, Aug26 attribution excluded), c097 (Kling 51–79char shells), c103 (delegation Feb background). Each UNRESOLVED/HOLD honestly held; no promotion without upstream Evidence revision per gate `HOLD_ALLOWED`.
- **EXCLUDE 30 taskless DROP lawful:** 5 coverage (ComfyUI, llama.cpp, TensorRT-LLM, SGLang, vLLM — Releases API routine noise, outside W34 scope); 4 DUPLICATE (c042 grok-distribution→c023/c024, c067 grok-build→c025/c066, c069 dogwood→c031, c070 nemotron→c029; no separate evidence, no loss); 2 carry-over C076/C077 (Music3.0 Aug13, H3 Aug03 pre-window per carryover ledger `9cf2233e…`, RECHECKED_UNRESOLVED → explicit disposal here: no promotion/backfill/current action); 19 other screening DROPs (FlashInfer nightly, Anthropic revenue/hire, Preparedness-team report, GitHub outage, pricing-discussion meta, frontier-comparison meta, DynamoDB Vector, Agent Lightning, Wan3.0/Runway availability post-cutoff, Gemini Omni/Transcribe, ScienceFlow/CoRun/Renormalising papers, OpenRouter tutorial, HF Summer report, Amodei amplification, Palmyra X6 — each outside ordinary W34 scope/duplicate/routine noise per ledger rationale, 0 tasks/0 views).
- **EXCLUDE 358 CONTEXT (non-selected, retained):** 319 arxiv (distinct bodies, hash-only, maker-reported; 5 sampled confirm sections beyond abstract but still unreproduced) + 39 non-arxiv (c001 GLM-5.3 Flash post-cutoff split, c009 Mythos binders, c013 DSpark, c015 UI-Mate repo-first, c016 X Ads cutoff-boundary, c021 Stable Audio workflow-only, c024 Grok listing observed-not-captured, c025 Build cadence vs availability gap, c027 Gemma downloads vendor-counted, c028 Micron planned-investment, c029 Nemotron background, c032 dashboard beta-drift, c034 Web Search filters, c036 Fenris agenda-not-results, c037 MiniMax Design undated, c041 Gemini 3.7 pre-window, c043 Unsloth quants, c044 MLX community, c046 vector guidance, c048 Transformers patch, c050 AutoDesign paper, c056 Meta Mac secondary-only, c058 social-only, c073/c080–c083/c085/c088/c092–c093/c095/c098 Apple/Cohere/paper signals, 4 Apple/Cohere refresh). Each with card-level limitation (undated/secondary/pre-window/post-cutoff/workflow-only/vendor-only) — not selected, no upgrade, preserved for negative-space audit.
- **Ledger 439 = 434 expansion (incl. 2 carry-over) + 5 coverage** distinct from R369/E439 bases (`e176326f…`/`0a23be47…`/`b9d963d8…`); R369 vs E439 never summed. Completeness `weekly:current-relevance` count-language stale (`434 vs 439`) noted but not blocking; `carry-over` SATISFIED now explicitly disposed here (no silent DROP).

## 4. Rejected alternatives (why not)

- **Historical 41/7/12pp copy:** rejected as approval — reference only, package allocation unknown in this runtime, chronology/duplication not re-evaluated there. Our 5-package thesis + qualified supporting + 16–18pp differs.
- **Sparse 1-package (e.g., AgentCore-only):** rejected — would ignore VERIFIED frontier distribution/pricing/safety deltas (c017/c023/c030/c040/c005/c008) that are independently supported; compression audit counterfactual fails (different multi-item architecture IS supportable).
- **Arxiv-led Paper Watch package:** rejected now — hash-only, maker-reported, no reproduction; 5 sampled show beyond-abstract content but still vendor-claimed; full consumption is future investment, not current sufficiency.
- **Business-only or safety-only issue:** rejected — would break technical/business mix and Weekly completeness (current-relevance + technical-significance + carry-over all LIMITED).
- **Shallow top-N / year-group / citation-count filter:** never used — would violate governance §8 (unselected bodies richer than claims, VERIFIED+CONTEXT/HOLD sampling, cluster collapse). Our omission is per-DID authority-based.
- **Promoting PARTIAL boundary to FEATURE:** rejected — would assert confirmed W34 events without clock-time proof. Restricted supporting with explicit qualifier is the honest ceiling.
- **Promoting HOLD/NEEDS_MORE to positive:** rejected per gate `HOLD_ALLOWED`/`REJECT_ALLOWED` — requires upstream Evidence revision + re-review, not editorial wish.

## 5. Compression audit (governance §4.4)

- **Trigger:** `SELECTED positive 41 >1`, so formal `SELECTED<=1` scrutiny NOT triggered. Documented anyway.
- **Counterfactual:** *If captured primaries were fully consumed, could a materially different multi-item Architecture be supported?* Yes, partially: full arxiv consumption (319 distinct HTML bodies, 112–556KB) could support an additional methods/eval package (retrieval benchmarks, agentic workloads, safety evals) beyond current 5. It would **supplement**, not displace, P1–P5 VERIFIED core (distribution/pricing/GA/safety/infra deltas are independently first-party supported). No evidence that full consumption would collapse current core to 1 package. Sparse alternative therefore rejected with reason.
- **Negative-space sweep:** major lanes covered (Anthropic/OpenAI/Google/AWS/xAI/DeepSeek/Qwen/Alibaba/Mistral/Slack/Runway/Adobe/Pika/Stripe/NVIDIA). Gaps are HOLDs above (Vera Rubin, SenseNova, MediaTek, MPA MOU, Kling, Benchmarks, Ox preview specs) — each with targeted-search history, residual explicitly listed. No fresh sweep performed (no network); reuse of prior sweep + ledger duplicate/concentration analysis is stated limit.

## 6. Limits (no approval claimed)

- Author DATA only; **no independent research/selection review yet, no Architecture approval, no Human Gate, no R4 audit, no Draft/PDF**. WholeNOT_READY/step4B3OPEN/audit unstarted/DM021+022OPEN; quality/adoption/savings OPEN.
- Statuses are historical labels; chronology residuals (11 PARTIAL + c001/c024 CONTEXT) remain UNRESOLVED; vendor/researcher/SOCIAL classes quarantined.
- 180-bucket counts (319 arxiv) are not sufficiency; duplicate collapse (4 groups) is ledger-recorded, not re-proven by new bytes.
- Carry-over disposal here satisfies Selection explicit-disposal obligation; `profile-completeness` file itself unchanged (active write requires root dispatch).

## 7. Packages → Architecture structure (for later API JSON, not yet built)

Proposed `candidate-selection-v2.json` assignments = machine `proposal_role` per DID (every row exactly one role; HOLD/REJECT never positive; POST_CUTOFF only LATE_BREAKING/WATCHLIST/HOLD_OUT/EXCLUDE — none proposed as main-window positive). Proposed `architecture-v2.json` packages = P1–P5 above with `primary_candidate_ids` = FEATURE+SECTION in package, `supporting_candidate_ids` = SUPPORTING in package, `drafting_order` P1→P5, empty-placement synthesis NOT used. `build_architecture_input` roles respected (`HOLD_OUT`/`EXCLUDE` never drafted). Exact `evidence_task_id` lists derivable from machine `evidence_task_ids` + ledger; API JSON deferred until source interface map reviewed.

## 8. Necessary missing authority (only if selected claim needed it)

**None indispensable for qualified presentation above.** Optional upgrades ONLY if Human/root later demands confirmed-W34 headlines for PARTIAL items:

- c002/c020/c039: `Last-Modified`/sitemap/archived Aug14 version + clock time vs 22Z (locators: Anthropic watermark page, Pika family page, Qwen3.8 repo news).
- c022/c045/c066/c102-addition: Aug21 clock-time header/sitemap/archived version (DeepSeek changelog, OpenAI changelog badge, xAI Grok Bot versioned Aug21 page — DailyX X never authority, Cloud Antigravity Aug21 blog version).
- c099–c101: entry-level dated bytes (not Sep8 capture) for JetBrains/Slack/Teams governance.
- c055/c006: MSRC advisory `https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-24301` + NVD record (vendor severity/scope; researcher-only now).
- c024: captured Aug21 listing bytes (Cloud partner-models/grok versioned + xAI release-notes) if listing-date precision needed.
- HOLDs: first-party durable pages per original review §8 (OpenRouter Benchmarks section, NVIDIA/press Vera Rubin, SenseNova model card, MediaTek artifact, MPA MOU text, Kling Turbo/MCP/CLI launch, Ox preview listing).

No new standing crawl, current-main following, Production checkout, or code adoption authorized; any gap-fill returns to root with specific scope.

## 9. Attribution

Author: W34 research/editorial proposal author (isolated-runtime DATA reads only). Prior BOUNDED_PROCEED reviews cited as history, not reused as approval. Independent research/selection review still required before Architecture dossier + Human ARCHITECTURE_REVIEW.
