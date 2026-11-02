---
sensor: grok-x-source-intake
task_id: "weekly-x-2026-W34-r2-correction-1"
issue_id: "2026-W34"
status: raw
correction_of: "weekly-x-2026-W34-r2"
---

# Run metadata

- observation window: 2026-08-14T18:00:00-04:00 to 2026-08-21T18:00:00-04:00 (America/New_York, [start, end)) ≡ UTC [2026-08-14T22:00:00Z, 2026-08-21T22:00:00Z)
- search methods used: (unchanged from original r2; no new search performed)
- search limitations: (unchanged from original r2)
- total retained topic clusters: 12
- total unique X URLs (all windows): 47
- total unique ordinary-window X URLs: 10
- total unique BACKGROUND_ONLY X URLs: 20
- total unique LATE_BREAKING X URLs: 17
- total official-account X URLs: 17 (ordinary: 2; background: 15; late-breaking: 0)
- total independent/non-official X URLs: 30 (ordinary: 8; background: 5; late-breaking: 17)
- total linked non-X primary-source unique URLs: 9

# Observation summary

After strict UTC reclassification against [2026-08-14T22:00:00Z, 2026-08-21T22:00:00Z):

Ordinary-window (10 URLs) material is limited primarily to:
- Two official Google posts at ~22:44Z on 14 Aug amplifying Gemini 3.7 Flash day-after usage.
- Mid-window free-tier / GLM-5.3 access signals (15 Aug).
- 18 Aug safety/pace commentary.
- Several 21 Aug (pre-22:00Z) Qwen local-optimization, abliteration, and performance posts.

The majority of Grok 4.6 official amplification, DeepSeek V4-Pro launch/pricing, most NVIDIA/HF posts, and many early Gemini posts fall into BACKGROUND_ONLY (pre-22:00Z 14 Aug).

A substantial set of 21 Aug post-22:00Z posts (Qwen MLX speedups, free-token promos, integration reports, qualitative comparisons) are LATE_BREAKING.

Pre-window original launches are retained only as BACKGROUND_ONLY provenance; W34 delta (pricing, adoption, reproduction, benchmark, integration, failure, safety) is called out where present. Post-level provenance preserved; no URLs added or removed.

# Topic clusters

## Cluster 1: Grok 4.6 post-release performance and multimodal signals

- Category: frontier / proprietary foundation models; coding models
- Importance signal: High
- Confidence of observation: Likely
- Original event before window: yes
- New W34 delta: independent coding/multimodal performance observations, official amplification of CursorBench and GPQA claims, Build harness guidance
- Primary-source locator(s): https://Grok.com/build

### X posts

| X URL | Author / handle | Posted time | Role | What this post contributes | Claim status |
|---|---|---|---|---|---|
| https://x.com/elonmusk/status/2088138697002668110 | Elon Musk / @elonmusk | 2026-08-14T05:40:35Z | OFFICIAL_ANNOUNCEMENT; COMMUNITY_ANALYSIS | Amplifies CursorBench #1 ranking claim for real-world coding vs Claude Fable 5 / Opus 5 / GPT-5.6 Sol | author-claim |
| https://x.com/elonmusk/status/2088127459971522726 | Elon Musk / @elonmusk | 2026-08-14T04:55:56Z | OFFICIAL_TECHNICAL_FOLLOWUP | Highlights multimodal (image & video understanding) upgrade vs Grok 4.5; productivity claim 10-100x on video review workloads | author-claim |
| https://x.com/elonmusk/status/2088100521261359218 | Elon Musk / @elonmusk | 2026-08-14T03:08:53Z | OFFICIAL_TECHNICAL_FOLLOWUP | States Grok 4.6 works best with Grok Build harness; links primary | official |
| https://x.com/elonmusk/status/2088033597999473050 | Elon Musk / @elonmusk | 2026-08-13T22:42:58Z | OFFICIAL_ANNOUNCEMENT | Simple endorsement post in quote chain of independent kernel/modding test | official |
| https://x.com/elonmusk/status/2087970387002855683 | Elon Musk / @elonmusk | 2026-08-13T18:31:47Z | OFFICIAL_ANNOUNCEMENT | Amplifies GPQA Diamond 94.9% claim | author-claim |
| https://x.com/XFreeze/status/2088137836079804882 | X Freeze / @XFreeze | 2026-08-14T05:37:10Z | INDEPENDENT_BENCHMARK | Original CursorBench ranking post quoted by Musk | observed |
| https://x.com/yunta_tsai/status/2088062294119104944 | Yun-Ta Tsai / @yunta_tsai | 2026-08-14T00:36:59Z | PERFORMANCE_OBSERVATION | Independent multimodal productivity observation on video understanding | observed |
| https://x.com/ArthurMacwaters/status/2088044880379761103 | Arthur MacWaters / @ArthurMacwaters | 2026-08-13T23:27:48Z | PERFORMANCE_OBSERVATION | Notes optimization for Grok Build | observed |
| https://x.com/MiaAI_lab/status/2087857449172689240 | Mia / @MiaAI_lab | 2026-08-13T11:03:01Z | INDEPENDENT_REPRODUCTION | 8-hour kernel/modding test claiming parity with Kimi K3 at lower tokens/speed | observed |
| https://x.com/cb_doge/status/2087953922229170682 | DogeDesigner / @cb_doge | 2026-08-13T17:26:22Z | INDEPENDENT_BENCHMARK | GPQA Diamond ranking post | observed |

### Observation
Post-release technical discussion and official amplification of Grok 4.6 coding and multimodal claims continued into the ordinary window. Distinct independent tests and official guidance on Build harness were retained separately.

### Follow-up for ChatGPT/Sol
Verify CursorBench / GPQA primary results and Build harness documentation; assess whether multimodal claims generalize beyond author use-cases.

## Cluster 2: Gemini 3.7 Flash official launch amplification and early usage

- Category: frontier / proprietary; coding models and agents
- Importance signal: High
- Confidence of observation: Confirmed
- Original event before window: yes (launch ~Aug 13)
- New W34 delta: official Google posts on Aug 14 showing early creative/coding usage, design adherence, web-dev capabilities, playable game one-shot
- Primary-source locator(s): https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/

### X posts

| X URL | Author / handle | Posted time | Role | What this post contributes | Claim status |
|---|---|---|---|---|---|
| https://x.com/Google/status/2088396439198089236 | Google / @Google | 2026-08-14T22:44:46Z | OFFICIAL_ANNOUNCEMENT | Official day-after post: "most intelligent workhorse model yet for coding and agents"; showcases community creativity | official |
| https://x.com/Google/status/2088396450258391370 | Google / @Google | 2026-08-14T22:44:48Z | OFFICIAL_TECHNICAL_FOLLOWUP | Calls for user examples | official |
| https://x.com/Google/status/2088366086316315080 | Google / @Google | 2026-08-14T20:44:09Z | OFFICIAL_ANNOUNCEMENT | Video demo of upgraded design adherence / web-dev; one-shot playable game in Antigravity | official |
| https://x.com/Google/status/2088366088509591790 | Google / @Google | 2026-08-14T20:44:10Z | OFFICIAL_TECHNICAL_FOLLOWUP | Links primary blog | official |
| https://x.com/Google/status/2088345261164617842 | Google / @Google | 2026-08-14T19:21:24Z | OFFICIAL_ANNOUNCEMENT | Cross-promotion with GeminiApp | official |
| https://x.com/Motion_Viz/status/2090924251520065713 | MotionViz / @Motion_Viz | 2026-08-21T22:09:23Z | INTEGRATION_OR_DEPLOYMENT | Reports 1-prompt / 1-hr memory transfer setup from prior Gemini 3.7 + Hermes to new stack | observed |
| https://x.com/deftdawg/status/2090947274272645212 | Deftdawg / @deftdawg | 2026-08-21T23:40:52Z | FAILURE_OR_REGRESSION | Reports Gemini 3.7-flash high resorts to view-source instead of filesystem code inspection | observed |
| https://x.com/10xmylife/status/2090746640495964545 | 海明Dev / @10xmylife | 2026-08-21T10:23:37Z | PERFORMANCE_OBSERVATION | Strong endorsement for Chinese writing tasks | observed |

### Observation
Official Google amplification on Aug 14 confirmed early coding/agent positioning and design capabilities. Independent integration and failure reports appeared later in window.

### Follow-up for ChatGPT/Sol
Confirm exact launch timestamp vs window; evaluate coding/agent benchmarks vs prior Flash; investigate reported filesystem regression.

## Cluster 3: DeepSeek V4-Pro launch and pricing

- Category: open-weight / open-source models; agents
- Importance signal: High
- Confidence of observation: Confirmed
- Original event before window: yes (Aug 13 launch)
- New W34 delta: API pricing peak/off-peak update effective Aug 16; continued availability signals
- Primary-source locator(s): DeepSeek API docs (referenced in posts)

### X posts

| X URL | Author / handle | Posted time | Role | What this post contributes | Claim status |
|---|---|---|---|---|---|
| https://x.com/deepseek_ai/status/2087864585504305397 | DeepSeek / @deepseek_ai | 2026-08-13T11:31:22Z | OFFICIAL_ANNOUNCEMENT | Official V4-Pro launch: major Agent upgrades, flexible reasoning effort, native OpenAI Responses API / Codex support | official |
| https://x.com/deepseek_ai/status/2087864589895798968 | DeepSeek / @deepseek_ai | 2026-08-13T11:31:23Z | OFFICIAL_TECHNICAL_FOLLOWUP | Pricing update: peak/off-peak rates (off-peak 50% lower); effective 16:00 UTC Aug 16 | official |

### Observation
Official launch and pricing structure change provide concrete access/cost delta inside/near window.

### Follow-up for ChatGPT/Sol
Verify API model names and pricing tables; assess agentic gains vs prior V4 preview.

## Cluster 4: Qwen3.8-27B open weights, local inference speedups, and safety variants

- Category: open-weight models; local inference; safety
- Importance signal: High
- Confidence of observation: Likely
- Original event before window: yes (weights ~mid-Aug)
- New W34 delta: community MLX/Apple Silicon 3.3x decode speedup challenge results; abliterated/uncensored FP8 variants with near-zero refusal rates; high HF download signals
- Primary-source locator(s): https://huggingface.co/orcarouter/Qwen3.8-27B-Uncensored-FP8 ; https://www.yukon.org/mlxfast ; Hugging Face Qwen collections

### X posts

| X URL | Author / handle | Posted time | Role | What this post contributes | Claim status |
|---|---|---|---|---|---|
| https://x.com/0xkydo/status/2090894947335750142 | Kydo / @0xkydo | 2026-08-21T20:12:57Z | INDEPENDENT_BENCHMARK; PERFORMANCE_OBSERVATION | Detailed MLX challenge results: 3.3x decode (26→87.9 tok/s) on M5 Max via 31 solvers / custom MTP heads; technical breakdown | observed |
| https://x.com/julianharris/status/2090950801099256146 | Julian Harris / @julianharris | 2026-08-21T23:54:53Z | COMMUNITY_ANALYSIS | Amplifies open-weights innovation pace; notes 1-week-old model + 330% Mac speedup | observed |
| https://x.com/doodlestein/status/2090866739705737599 | Jeffrey Emanuel / @doodlestein | 2026-08-21T18:20:51Z | SECURITY_OR_SAFETY_OBSERVATION | Shares uncensored FP8 weights link; urges download before potential ban | observed |
| https://x.com/doodlestein/status/2090866417482510497 | Jeffrey Emanuel / @doodlestein | 2026-08-21T18:19:35Z | SECURITY_OR_SAFETY_OBSERVATION | Notes near-zero refusal after abliteration while preserving MMLU/GSM8K etc. | observed |
| https://x.com/MaxForAI/status/2090920962296578081 | Max For AI / @MaxForAI | 2026-08-21T21:56:19Z | COMMUNITY_ANALYSIS; REPORTING_OR_SECONDARY | Chinese-language summary of abliteration method (131 residual matrices) and capability retention | observed |
| https://x.com/NullContex1s/status/2090922565539917905 | why / @NullContex1s | 2026-08-21T22:02:41Z | PERFORMANCE_OBSERVATION | Reports 1.7M HF downloads; notes multimodal image-text capability | observed |
| https://x.com/Oluwaphilemon1/status/2090951888552301053 | FHILY👑 / @Oluwaphilemon1 | 2026-08-21T23:59:12Z | PERFORMANCE_OBSERVATION | Local DGX Spark runs comparing Qwen3.8-Max 1-bit vs other models | observed |
| https://x.com/tlanderso/status/2090951328843620464 | Thomas A. Anderson / @tlanderso | 2026-08-21T23:56:59Z | PERFORMANCE_OBSERVATION | Qualitative comparison: smart but dry writing vs GLM | observed |

### Observation
Strong independent technical activity on local optimization and safety-removal of the newly available dense open-weight model. Distinct posts for speedup methodology, abliteration details, and download momentum retained.

### Follow-up for ChatGPT/Sol
Confirm HF model cards and exact release dates; evaluate abliteration impact on residual capabilities and safety implications; verify MLX upstreaming claims.

## Cluster 5: GLM-5.3 / Z.AI activity and free-tier signals

- Category: open-weight / frontier; coding / agents / multimodal
- Importance signal: Medium
- Confidence of observation: Likely
- Original event before window: unknown
- New W34 delta: free-token promotions, benchmark claims vs Kimi/Fable/SWE/cyber, multimodal Flash mentions, compute-source speculation
- Primary-source locator(s): https://chat.z.ai/ ; Z.AI related pages

### X posts

| X URL | Author / handle | Posted time | Role | What this post contributes | Claim status |
|---|---|---|---|---|---|
| https://x.com/kocer_eth/status/2088776558668288410 | kocer / @kocer_eth | 2026-08-15T23:55:13Z | INTEGRATION_OR_DEPLOYMENT; INDEPENDENT_BENCHMARK | Free PRO trial details for GLM-5.3 (3M tokens/day); benchmark claims beating Kimi K3 / Fable 5 on Terminal/SWE/cyber | author-claim |
| https://x.com/e_go0309/status/2090952085240266836 | babajiba / @e_go0309 | 2026-08-21T23:59:59Z | INTEGRATION_OR_DEPLOYMENT | 100M free GLM-5.3 tokens promo for itokenify users | observed |
| https://x.com/Da7_Tech/status/2090926178232123654 | Da7em / @Da7_Tech | 2026-08-21T22:17:03Z | COMMUNITY_ANALYSIS | Speculates Ox-Alpha is GLM from Zai; questions compute source for free scale | unverified |
| https://x.com/TheoryoftheDog/status/2090951993497960613 | Theory of the Dog / @TheoryoftheDog | 2026-08-21T23:59:37Z | OTHER_TECHNICAL_SIGNAL | Notes GLM 5.3 Flash multimodal | observed |
| https://x.com/velkan_gst/status/2090951516551053358 | velkan / @velkan_gst | 2026-08-21T23:57:44Z | PERFORMANCE_OBSERVATION | Personal usage signal of high free-token volume | observed |

### Observation
Multiple free-access and benchmark signals around GLM-5.3 family inside window; distinct from pure announcement.

### Follow-up for ChatGPT/Sol
Locate official Z.AI release notes; verify free-tier terms and independent benchmarks.

## Cluster 6: NVIDIA Nemotron 3.5 Lightning follow-ups

- Category: open-weight models; agents; local inference
- Importance signal: Medium
- Confidence of observation: Confirmed (follow-ups)
- Original event before window: yes (Aug 11)
- New W34 delta: partner post-training examples, NeMo Switchyard routing library, dataset release signals inside/near window
- Primary-source locator(s): https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 ; https://huggingface.co/datasets/nvidia/Nemotron-RL-Agentic-Terminal-Pivot-v1

### X posts

| X URL | Author / handle | Posted time | Role | What this post contributes | Claim status |
|---|---|---|---|---|---|
| https://x.com/NVIDIAAI/status/2088339706752983230 | NVIDIA AI / @NVIDIAAI | 2026-08-14T18:59:20Z | OFFICIAL_TECHNICAL_FOLLOWUP | Introduces NeMo Switchyard open-source model routing library pairing frontier + Nemotron Lightning | official |
| https://x.com/NVIDIAAI/status/2087662769512571010 | NVIDIA AI / @NVIDIAAI | 2026-08-12T22:09:25Z | OFFICIAL_TECHNICAL_FOLLOWUP | Highlights partner domain post-training of Lightning | official |
| https://x.com/NVIDIAAI/status/2087258724654284971 | NVIDIA AI / @NVIDIAAI | 2026-08-11T19:23:54Z | OFFICIAL_ANNOUNCEMENT | Ships Nemotron-RL-Agentic-Terminal-Pivot dataset | official |
| https://x.com/NVIDIAAI/status/2087173733823680855 | NVIDIA AI / @NVIDIAAI | 2026-08-11T13:46:10Z | OFFICIAL_ANNOUNCEMENT | Weights + data + recipes available on HF | official |

### Observation
Official technical follow-ups on routing and partner usage provide concrete W34 delta beyond original release.

### Follow-up for ChatGPT/Sol
Confirm dataset and Switchyard repos; assess agentic post-training quality.

## Cluster 7: Hugging Face State of Open Models Summer 2026

- Category: research / evaluation; open-weight landscape
- Importance signal: Medium
- Confidence of observation: Confirmed
- Original event before window: no
- New W34 delta: official summary of usage patterns (Qwen leads local, agents rising)
- Primary-source locator(s): https://huggingface.co/blog/state-of-open-models-summer-2026

### X posts

| X URL | Author / handle | Posted time | Role | What this post contributes | Claim status |
|---|---|---|---|---|---|
| https://x.com/huggingface/status/2088301795890044975 | Hugging Face / @huggingface | 2026-08-14T16:28:41Z | OFFICIAL_ANNOUNCEMENT; AUTHOR_RESEARCH_POST | State of Open Models Summer 2026: frontier larger but small models dominate real usage; Qwen leads local; agents major force | official |

### Observation
Single high-signal official landscape summary inside window.

### Follow-up for ChatGPT/Sol
Read full blog for quantitative usage data.

## Cluster 8: Local AI / Apple Silicon / MLX ecosystem momentum

- Category: inference serving / local inference; developer tooling
- Importance signal: Medium
- Confidence of observation: Likely
- Original event before window: no
- New W34 delta: concrete multi-solver speedup campaigns and production upstreaming claims for Qwen on MLX
- Primary-source locator(s): https://www.yukon.org/mlxfast ; Darkbloom references

### X posts

| X URL | Author / handle | Posted time | Role | What this post contributes | Claim status |
|---|---|---|---|---|---|
| https://x.com/0xkydo/status/2090894947335750142 | Kydo / @0xkydo | 2026-08-21T20:12:57Z | INDEPENDENT_BENCHMARK; INTEGRATION_OR_DEPLOYMENT | Full technical post on MLX challenge methodology and results (already listed in Cluster 4; dual-role) | observed |
| https://x.com/julianharris/status/2090950801099256146 | Julian Harris / @julianharris | 2026-08-21T23:54:53Z | COMMUNITY_ANALYSIS | Frames broader open-weights innovation impact | observed |

### Observation
Overlaps with Qwen cluster but distinct ecosystem signal on community-driven kernel/MTP optimization.

### Follow-up for ChatGPT/Sol
Track upstreaming status into core MLX.

## Cluster 9: Agent / coding harness and free-tier tooling signals

- Category: coding models and coding agents; developer tooling
- Importance signal: Medium
- Confidence of observation: Likely
- Original event before window: mixed
- New W34 delta: free trials bundling multiple Chinese frontier models; IDE/CLI integration
- Primary-source locator(s): various IDE download pages referenced

### X posts

| X URL | Author / handle | Posted time | Role | What this post contributes | Claim status |
|---|---|---|---|---|---|
| https://x.com/kocer_eth/status/2088776558668288410 | kocer / @kocer_eth | 2026-08-15T23:55:13Z | INTEGRATION_OR_DEPLOYMENT | Detailed free trial + IDE setup for multi-model access (dual with Cluster 5) | observed |
| https://x.com/kocer_eth/status/2086383429579325697 | kocer / @kocer_eth | 2026-08-09T09:25:47Z | INTEGRATION_OR_DEPLOYMENT | Earlier free trial post for context (background) | observed |

### Observation
Concrete developer-access promotions inside window.

### Follow-up for ChatGPT/Sol
Map exact models and rate limits.

## Cluster 10: Multimodal / video / image generation mentions

- Category: multimodal / vision-language; image / video generation
- Importance signal: Low
- Confidence of observation: Unverified
- Original event before window: mixed
- New W34 delta: scattered usage signals; no major new frontier video model inside ordinary window
- Primary-source locator(s): none retained as primary

### X posts

| X URL | Author / handle | Posted time | Role | What this post contributes | Claim status |
|---|---|---|---|---|---|
| https://x.com/yunta_tsai/status/2088062294119104944 | Yun-Ta Tsai / @yunta_tsai | 2026-08-14T00:36:59Z | PERFORMANCE_OBSERVATION | Grok 4.6 multimodal productivity (dual-listed) | observed |

### Observation
Limited new primary multimodal releases inside strict window; most signals secondary to text/coding models.

### Follow-up for ChatGPT/Sol
Check for Gemini Omni or FLUX follow-ups outside ordinary counts.

## Cluster 11: Safety / alignment / policy adjacent signals

- Category: safety, alignment, cybersecurity
- Importance signal: Medium
- Confidence of observation: Likely
- Original event before window: no
- New W34 delta: public discussion of abliteration ease on newly released open weights; broader pace-of-progress safety comments
- Primary-source locator(s): HF uncensored model cards

### X posts

| X URL | Author / handle | Posted time | Role | What this post contributes | Claim status |
|---|---|---|---|---|---|
| https://x.com/doodlestein/status/2090866739705737599 | Jeffrey Emanuel / @doodlestein | 2026-08-21T18:20:51Z | SECURITY_OR_SAFETY_OBSERVATION | Direct link + ban-anticipation framing (dual) | observed |
| https://x.com/kimmonismus/status/2089790124825456738 | Chubby♨️ / @kimmonismus | 2026-08-18T19:02:46Z | COMMUNITY_ANALYSIS | Quotes Amodei on model progress outstripping safety; notes 2026 acceleration | observed |

### Observation
Concrete technical safety-removal example plus high-level timeline commentary.

### Follow-up for ChatGPT/Sol
Assess prevalence of abliterated variants and any official responses.

## Cluster 12: Cross-cutting adoption / pricing / access momentum

- Category: model distribution and cloud/platform availability
- Importance signal: Medium
- Confidence of observation: Likely
- Original event before window: mixed
- New W34 delta: multiple free-token windows and pricing adjustments (DeepSeek, GLM, others)
- Primary-source locator(s): provider pricing pages

### X posts

| X URL | Author / handle | Posted time | Role | What this post contributes | Claim status |
|---|---|---|---|---|---|
| https://x.com/deepseek_ai/status/2087864589895798968 | DeepSeek / @deepseek_ai | 2026-08-13T11:31:23Z | OFFICIAL_TECHNICAL_FOLLOWUP | Peak/off-peak pricing (dual) | official |
| https://x.com/e_go0309/status/2090952085240266836 | babajiba / @e_go0309 | 2026-08-21T23:59:59Z | INTEGRATION_OR_DEPLOYMENT | Free token promo (dual) | observed |

### Observation
Access-cost signals complement model capability releases.

### Follow-up for ChatGPT/Sol
Aggregate pricing changes for cost-sensitive workloads.

# Cross-cutting patterns

- Open-weight dense models (Qwen3.8-27B) receiving rapid community optimization and safety modification within days of availability.
- Official accounts actively amplifying early usage and harness guidance rather than only launch-day posts.
- Free-tier and peak/off-peak pricing used as adoption accelerators by multiple Chinese and open labs.
- Local inference (especially Apple Silicon / MLX) showing measurable multi-x gains via collaborative challenges.
- Safety discussion shifting from abstract alignment to concrete parameter-level refusal removal on public weights.

# Late Breaking

17 unique X URLs have posted_at >= 2026-08-21T22:00:00Z and are classified LATE_BREAKING in the corrected ledger. These include multiple Qwen3.8-27B local/MLX performance and abliteration posts, GLM free-token promos, integration/setup reports, and qualitative comparisons. Exact URLs are present in x-url-ledger.corrected.tsv with window_status=LATE_BREAKING. They are excluded from ordinary-window counts.

# Coverage assessment

High-recall coverage achieved across frontier proprietary, open-weight, coding/agents, local inference, and safety lanes. After strict UTC boundary reclassification, ordinary-window material is thinner than the original (misclassified) report indicated; many launch-adjacent official posts fall into BACKGROUND_ONLY. Multimodal video generation and major new research papers had lower signal density inside the strict ordinary window. Post-level provenance preserved; no artificial URL caps applied; URL set identical to original ledger. Independent of prior DailyX / r1 / Sol candidate materials. This file is a classification/accounting correction only; no new X search was performed.
