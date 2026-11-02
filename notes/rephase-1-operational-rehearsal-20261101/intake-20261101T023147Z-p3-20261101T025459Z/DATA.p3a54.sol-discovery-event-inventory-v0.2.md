# 2026-W34 Sol Discovery Candidate Inventory v0.2


Status: **TEMPORARY / NON-CANONICAL / DISCOVERY COMPLETENESS WORKING RECORD**


This record is deliberately pre-Screening. It preserves discovered events before materiality or Selection decisions. It must not be treated as Evidence, Candidate Selection, Architecture, or lifecycle authority.


## Basis


- DailyX: 7 daily files, 76 topic records; all topic records mapped into this event-level inventory.
- DailyX exact X URLs: 99 unique observed; W34 ordinary-window recheck previously found 98 ordinary / 1 pre-window.
- Weekly Grok r2 corrected ledger: 47 unique X URLs; 10 ordinary / 20 background / 17 late-breaking. Exact URL overlap with DailyX is only 1, so the two X sensors are treated as largely independent.
- Luna non-X readiness: 22 manual primary locators plus canonical GitHub Releases Raw from 7 configured repositories; arXiv/official-page exact-byte collectors still require retry.
- Sol primary-source/web expansion: first-party pages and model/research artifacts used only for discovery verification at this stage.


## Status vocabulary


- `KEEP_CANDIDATE`: retain for Screening; not a Selection decision.
- `KEEP_CONTEXT`: retain as context but do not silently promote to technical event.
- `BOUNDARY_PRE_WINDOW`: event predates W34; may support background or a distinct W34 delta.
- `BOUNDARY_POST_CUTOFF`: post-cutoff; retain as boundary/Late Breaking context.
- `CHRONOLOGY_VERIFY`: real event/artifact, but exact W34 timing remains unresolved.
- `AUTHORITY_VERIFY`: observed claim/event still needs stronger first-party authority.
- Qualifiers such as `DATE_ONLY_BOUNDARY`, `PRIMARY_AUTHORITY_GAP`, `RESEARCH_SCREEN`, etc. narrow what must be checked before Evidence.


## Inventory summary


- KEEP_CANDIDATE: 82
- KEEP_CONTEXT: 7
- BOUNDARY_PRE_WINDOW: 11
- BOUNDARY_POST_CUTOFF: 4
- CHRONOLOGY_VERIFY: 0
- AUTHORITY_VERIFY: 1
- Total event-level records: 105


## Event-level inventory


| ID | Event | Lane | Current Discovery status | Source layers | Notes / next verification |
|---|---|---|---|---|---|
| W34-C001 | GLM-5.3 flagship release | Foundation Models / Agents | KEEP_CANDIDATE / DATE_ONLY_BOUNDARY | Official ZCode changelog v3.7.7 (Aug 14); official model artifact; DailyX+r2 | Release confirmed; exact Aug 14 time vs 22:00Z boundary still unresolved. Keep W34 adoption/free-access/coding-agent delta regardless. |
| W34-C002 | Claude text watermark | Safety / Provenance / Policy | KEEP_CANDIDATE / DATE_ONLY_BOUNDARY | Anthropic official Aug 14 article; DailyX | Future Claude models use token-choice watermarking for EU AI Act compliance. Exact page time vs W34 start unresolved; ordinary-window X discussion exists. |
| W34-C003 | OpenRouter joins Stripe | Inference / Routing / Business | KEEP_CANDIDATE | OpenRouter official Aug 19 announcement; DailyX | Confirmed transaction/integration event; model gateway scale and routing economics are technically relevant. |
| W34-C004 | ChatGPT for Teens | Product / Safety | KEEP_CANDIDATE | OpenAI official Aug 18; DailyX | Distinct teen experience with automatic age routing and stronger safety controls. |
| W34-C005 | OpenAI cyber-critical capability pacing | Safety / Security / Frontier governance | KEEP_CANDIDATE | OpenAI official Aug 18; DailyX | Astra preliminary Critical cyber threshold evidence plus stronger containment/monitoring/alignment and development pacing. |
| W34-C006 | Ray CVE-2025-62593 added to CISA KEV | Safety / Security / Systems | KEEP_CANDIDATE | DailyX; CISA-KEV attestation via security sources; Ray/GitHub advisory | W34 exploitation/KEV delta is distinct from 2025 vulnerability disclosure. |
| W34-C007 | Alipay full-stack agentic commerce platform | Agents / MCP / Commerce | KEEP_CANDIDATE / PRIMARY_AUTHORITY_GAP | Alipay statement relayed by multiple publications; DailyX | Agent-ready Skills/MCP conversion, AHA interoperability, payments/identity/risk/fulfillment. Seek direct Ant/Alipay release for Evidence. |
| W34-C008 | OpenAI Zero Data Retention + Private Safety Processing | Safety / Privacy / Serving | KEEP_CANDIDATE | OpenAI official Aug 19; DailyX | Cross-interaction safety pattern detection designed to remain compatible with ZDR. |
| W34-C009 | Claude protein design / analytical chemistry results | Research / Science | KEEP_CANDIDATE | Anthropic research Aug 18; DailyX | Primary research result; maker-reported experimental claims require careful framing. |
| W34-C010 | Amazon Bedrock AgentCore Payments GA | Agents / MCP / Payments | KEEP_CANDIDATE | AWS official Aug 18; DailyX | Autonomous paid API/MCP/content transactions with guardrails and observability. |
| W34-C011 | Claude Platform Computer Use + Skills API + Files API GA | Agents / Computer Use | KEEP_CANDIDATE | Claude official Aug 20; DailyX | Computer use, Skills API, Files API generally available; browser use tool added. |
| W34-C012 | Slack Code channels for coding agents | Coding Agents / Collaboration | KEEP_CANDIDATE | Slack official Aug 20; DailyX | Moves agent coding work from private sessions into collaborative code channels. |
| W34-C013 | LFM2.5-DSpark speculative decoding checkpoints | Inference / Local AI | KEEP_CANDIDATE | Liquid AI official Aug 20; DailyX | Public draft checkpoints for three LFM2.5 models; vendor-reported throughput gains. |
| W34-C014 | GPT-Image-2 transparent background preview | Image Generation / API | KEEP_CANDIDATE | OpenAI Developers post Aug 20; developer community mirror; Sol discovery | Clear API capability delta; community reports include edge-quality caveats. |
| W34-C015 | Tencent UI-Mate-27B open-weight GUI agent | Agents / Multimodal / Open Weight | KEEP_CANDIDATE | arXiv Aug 16; Tencent HF model card; Sol discovery | 27B GUI agent for long-horizon desktop tasks; benchmark numbers maker-reported. |
| W34-C016 | X Ads MCP launch | Agents / MCP / Advertising | KEEP_CANDIDATE / PRIMARY_DOC_VERIFY | DailyX official X observation | Agent-driven ad management via MCP; preserve exact launch post and locate canonical X Business docs. |
| W34-C017 | GPT-5.6 Sol API price reduction | Pricing / Access | KEEP_CANDIDATE | OpenAI official X post 2026-08-21T19:34:10Z; current official model page; DailyX | W34 timing is fixed by OpenAI's official post. Current model page confirms $4/M input and $20/M output with stated 20%/33% reductions and promotional pricing window. |
| W34-C018 | Imagen shutdown and migration to Gemini Image | Image Ecosystem / Deprecation | KEEP_CANDIDATE | Google Firebase official migration docs; Sol discovery | All Imagen models shut down Aug 17; migration to Gemini 3.x Image. |
| W34-C019 | Mistral Agentic Search | Agents / Retrieval | KEEP_CANDIDATE | Mistral official Aug 20; Luna non-X lead | Multi-step retrieval/navigation/verification layer; vendor benchmarks remain maker-reported. |
| W34-C020 | Pika Audio family: Speech / SFX / Music / Soundtrack | Speech / Audio / Music | KEEP_CANDIDATE | Pika official Aug 18 model pages; DailyX Speech | Four distinct audio-generation releases; family-level Aug 14 page is boundary, individual launches Aug 18. |
| W34-C021 | Stable Audio 3.0 workflow expansion | Audio / Creative Workflow | KEEP_CANDIDATE | Stability AI official Aug 18; Luna non-X lead | DAW plugin and advanced web workflow; not a new Stable Audio 3.0 model release. |
| W34-C022 | DeepSeek-V4-Flash-Vision-Exp | Multimodal / API | KEEP_CANDIDATE | DeepSeek official Aug 21; DailyX; Luna non-X lead | Experimental vision/multimodal API release; maker benchmarks need methodology-aware treatment. |
| W34-C023 | Grok 4.6 on Amazon Bedrock | Model Distribution / Cloud | KEEP_CANDIDATE | xAI official Aug 19; DailyX | Underlying Grok 4.6 is pre-window; Bedrock GA is a clean W34 distribution delta. |
| W34-C024 | Grok 4.6 on Gemini Enterprise Agent Platform | Model Distribution / Cloud | KEEP_CANDIDATE | xAI official Aug 21; DailyX | Clean W34 distribution delta distinct from base model launch. |
| W34-C025 | Grok Build available on web/mobile/every plan | Coding / App-Building Agents | KEEP_CANDIDATE | xAI official Aug 19; DailyX-related Grok updates | July beta becomes broadly available with publishing/sharing and model access. |
| W34-C026 | OpenAI joins PORTS-Pike / NVIDIA-SB Energy infrastructure deal | Infrastructure / Hardware | KEEP_CANDIDATE | OpenAI + NVIDIA official Aug 17; DailyX | Large long-term AI compute infrastructure commitment; keep infrastructure facts separate from speculative economics. |
| W34-C027 | Gemma surpasses 1B downloads | Open Weight / Adoption | KEEP_CANDIDATE | Google official Aug 20; DailyX | Adoption/ecosystem milestone; not a model release. |
| W34-C028 | Micron Research Labs launch | Hardware / Research Infrastructure | KEEP_CANDIDATE | Micron official Aug 20; DailyX | Long-horizon memory/compute research hub; hardware relevance to AI. |
| W34-C029 | NVIDIA Nemotron 3.5 Lightning on SageMaker JumpStart | Open Weight / Cloud Distribution | KEEP_CANDIDATE | AWS official Aug 17; related DailyX Nemotron/Switchyard | Underlying model pre-window; JumpStart availability is W34. |
| W34-C030 | OpenAI GPT-5.6 cross-Region inference on Amazon Bedrock | Serving / Distribution | KEEP_CANDIDATE | AWS official Aug 17/20; Sol expansion | Cross-Region inference and expanded API support for Sol/Terra/Luna across 25+ regions. |
| W34-C031 | Dogwood natural-language policy authoring in AgentCore | Agent Governance / Safety | KEEP_CANDIDATE | AWS official Aug 20; DailyX Dogwood | Original Dogwood release pre-window; W34 follow-up adds policy authoring and temporal controls in production context. |
| W34-C032 | OpenRouter Activity dashboard + Analytics API | Agents / Observability / Cost | KEEP_CANDIDATE | OpenRouter official Aug 17; Sol expansion | Per-agent/model/request spend and usage observability; relevant to production-agent operations. |
| W34-C033 | OpenRouter Visual Image Benchmarks | Evaluation / Image | KEEP_CANDIDATE | OpenRouter official Aug 21; Sol expansion | 39 image models over challenging prompts with price/time display; evaluation methodology must be framed as OpenRouter's benchmark. |
| W34-C034 | AgentCore Web Search domain/date filters | Agents / Retrieval / Control | KEEP_CANDIDATE | AWS official Aug 19; Sol expansion | Per-request source-domain and freshness filtering enforced server-side. |
| W34-C035 | OpenAI Vera Rubin racks running training stack | Infrastructure | KEEP_CANDIDATE / X_PRIMARY_ONLY | DailyX official/employee X observation | Treat as operational infrastructure observation until an equivalent first-party durable page is captured. |
| W34-C036 | DeepMind games research partnership / long-horizon agent research | Research / Agents | KEEP_CANDIDATE | Google DeepMind official Aug 21 article; DailyX | Official Aug 21 research article confirms game-developer partnerships aimed at long-horizon planning, continual learning and multi-agent research. |
| W34-C037 | MiniMax Design agentic creative platform | Agents / Multimodal Creative | KEEP_CANDIDATE / FIRST_PARTY_DATE_VERIFY | DailyX; official MiniMax Design product site; multiple independent Aug 20 launch reports | Product identity is confirmed and external dated sources converge on Aug 20 launch; retain only the first-party-date qualifier until a dated MiniMax launch artifact is captured. |
| W34-C038 | SenseNova-U1.5 open multimodal generation/editing model | Image / Multimodal / Open Weight | KEEP_CANDIDATE / CHRONOLOGY_VERIFY | DailyX; official SenseNova HF collection/model | Artifact exists; precise public release timestamp vs W34 needs history/model-card verification. |
| W34-C039 | Qwen3.8-27B availability and W34 local-inference wave | Foundation Models / Open Weight / Local | KEEP_CANDIDATE / DATE_ONLY_BOUNDARY | Qwen official repo Aug 14; DailyX+r2; Luna lead | Base availability date confirmed but exact release time unresolved; W34 local optimization/adoption is independently observable. |
| W34-C040 | DeepSeek V4-Pro W34 pricing/access delta | Foundation Models / Agents / Pricing | KEEP_CANDIDATE | DeepSeek official Aug 13 launch + pricing effective Aug 16; DailyX+r2 | Do not redraft Aug 13 GA as W34; retain the in-window pricing/access change. |
| W34-C041 | Gemini 3.7 Flash W34 adoption/usage delta | Foundation Models / Coding / Agents | KEEP_CANDIDATE / PRE_WINDOW_BASE | Google Aug 13 launch; DailyX+r2 ordinary follow-up | Base launch is pre-window; ordinary-window official/community follow-ups can support adoption/usage delta only. |
| W34-C042 | Grok 4.6 W34 adoption/integration delta | Foundation Models / Coding / Agents | KEEP_CANDIDATE / PRE_WINDOW_BASE | xAI Aug 12 base launch; DailyX; cloud/Copilot/Build follow-ups | Base launch pre-window; keep W34 integrations/distribution/usage as deltas. |
| W34-C043 | Qwen3.8 Unsloth/GGUF optimization | Local AI / Quantization | KEEP_CANDIDATE / COMMUNITY_PROJECT | DailyX | Third-party packaging/optimization; verify artifact timestamp and technical deltas before Evidence. |
| W34-C044 | Qwen3.8 MLX speedup / abliteration wave | Local AI / Safety / Community | KEEP_CANDIDATE / COMMUNITY_SIGNAL | corrected Grok r2 ordinary posts; DailyX related Qwen | Important W34 open-weight momentum; technical claims need artifact/benchmark verification. |
| W34-C045 | OpenAI API regional processing / changelog delta | Serving / Data Residency | KEEP_CANDIDATE / PRIMARY_CAPTURE_REQUIRED | Luna official-page lead Aug 21 | Candidate-specific official changelog capture still needed. |
| W34-C046 | AWS vector solutions for agentic AI where data lives | Retrieval / Systems | KEEP_CANDIDATE | Luna official AWS Aug 20 lead | Implementation/system architecture item; not a model release. |
| W34-C047 | Runway MCP workflow update | Creative Tools / MCP | KEEP_CANDIDATE | Runway official changelog Aug 20 | Workflow Support in Runway MCP lets agents list, open, tweak, and run workflows; separate from post-cutoff Wan 3.0 availability. |
| W34-C048 | Transformers v5.15.1 release | Developer Tooling | KEEP_CANDIDATE / SCREENING_REQUIRED | Canonical GitHub Releases Raw | In-window configured collector match; significance to be screened from release notes. |
| W34-C049 | FlashInfer W34 nightly releases | Inference / Serving | KEEP_CANDIDATE / SCREENING_REQUIRED | Canonical GitHub Releases Raw (4 matches) | Preserve as collector-discovered release activity; screen for substantive technical delta. |
| W34-C050 | AutoDesign meta-harness optimization | Research / Agent Harness | KEEP_CANDIDATE / SPLIT_DELTA | Official GitHub README: Aug 14 initial public release; Aug 15 DeepSeek Harness support; DailyX | Base release is date-only against the W34 start boundary, while Aug 15 DeepSeek Harness support is a clean in-window technical delta. |
| W34-C051 | LLM romance-baiting / pig-butchering scam experiment | Research / Safety | KEEP_CANDIDATE / CONFERENCE_OR_DISCUSSION_DELTA | DailyX; USENIX Security paper locator | Underlying research circulated before W34; retain the technical findings but verify whether the W34 event is conference presentation/public discussion rather than new-paper publication. |
| W34-C052 | ChatGPT Computer History rollout/privacy discussion | Product / Privacy | KEEP_CANDIDATE / DATE_ONLY_BOUNDARY | OpenAI official ChatGPT release notes Aug 14 + Aug 20 regional expansion; DailyX | Feature is confirmed: optional macOS activity history, off by default, recording interaction events rather than screenshots/audio; Aug 20 added EEA/Switzerland/UK for Pro. Base Aug 14 entry is date-only vs W34 start, but Aug 20 expansion is a clean W34 delta. |
| W34-C053 | Seedance 2.5 US availability claim | Video | KEEP_CANDIDATE / AUTHORITY_VERIFY / PRE_WINDOW_BASE | DailyX; ByteDance Seed official Jul 31 base launch | Seedance 2.5 itself launched Jul 31. No clean first-party W34-specific US-availability delta has yet been found; retain the observation but do not redraft the base launch as W34. |
| W34-C054 | MediaTek / automotive-edge Qwen3.8 deployment | Edge AI / Hardware | KEEP_CANDIDATE / AUTHORITY_VERIFY | DailyX | Potential deployment/adoption event; verify first-party MediaTek/partner artifact. |
| W34-C055 | Microsoft Copilot Personal CoSnitch (CVE-2026-24301) disclosure/patch | Safety / Agent Security | KEEP_CANDIDATE | Varonis Threat Labs primary research Aug 18; coordinated Microsoft patch statement; DailyX | One-click chain involved automatic prompt execution, connected-app data exfiltration and persistent-memory poisoning; Varonis says patches shipped Aug 18 and no exploitation was observed. Distinguish Copilot Personal from Microsoft 365 Copilot. |
| W34-C056 | Meta AI Mac app with Muse Spark system-wide dictation | Product / Multimodal / Desktop | KEEP_CANDIDATE / PRIMARY_VERIFY | DailyX; secondary TechCrunch Aug 20 | Product event appears real; seek Meta first-party announcement before Evidence. |
| W34-C057 | ByteDance–MPA AI copyright agreement covering Seedance/Seedream | Governance / Generative Media | KEEP_CANDIDATE | TikTok/ByteDance official newsroom Aug 17; Reuters; DailyX | Official MOU establishes a shared framework for IP guardrails on Seedance and Seedream across ByteDance/TikTok products. |
| W34-C058 | US pressure on allies over China-led AI framework | Policy / Geopolitics | KEEP_CANDIDATE / HIGH_AUTHORITY_REPORTING | DailyX; Reuters reporting based on US officials/internal draft | Retain neutrally as geopolitical AI-policy candidate. No public primary government document has yet been captured, so do not overstate beyond the reported draft/official sourcing. |
| W34-C059 | Anthropic business/revenue/IPO reports | Business Context | KEEP_CONTEXT | DailyX | May inform market context but not a core technical event absent technical implications. |
| W34-C060 | Anthropic hire of Amir Salek | Company / Hardware Talent | KEEP_CONTEXT | DailyX | Personnel move; retain only if it materially connects to infrastructure strategy. |
| W34-C061 | OpenAI Preparedness-team disbanding report | Safety / Company Context | KEEP_CONTEXT / CONTESTED | DailyX reporting; OpenAI denial/counter-reporting | Do not state as fact; contextualize only if needed around the official cyber-pacing announcement. |
| W34-C062 | GitHub worldwide outage affecting AI coding workflows | Developer Infrastructure | KEEP_CONTEXT | DailyX | Operational dependency/failure context; not necessarily a generative-AI product event. |
| W34-C063 | Model pricing / Chinese-vs-Western economics discussion | Market Context | KEEP_CONTEXT | DailyX | Trend/context cluster, not a single authoritative event. |
| W34-C064 | Frontier model comparison / release-density discussion | Market Context | KEEP_CONTEXT | DailyX | Use only as community-signal context, not evidence. |
| W34-C065 | Ox Alpha stealth preview, later revealed as GLM-5.3-Flash | Foundation Models / Evaluation / Deployment | KEEP_CANDIDATE / EX_POST_IDENTITY_RESOLVED | DailyX ordinary-window preview observations; OpenRouter stealth listing; later Z.ai official GLM-5.3-Flash disclosure | W34 event is the anonymous real-world preview/traffic evaluation. Identity was intentionally hidden during W34 and resolved post-cutoff; do not retroactively treat the Aug 26 official GLM-5.3-Flash release as an ordinary-window release. |
| W34-C066 | Grok Bot access expansion to more plans | Agents | KEEP_CANDIDATE | xAI official news index Aug 21; DailyX | Base Grok Bot launch is Aug 11 (pre-window). The W34 event is the Aug 21 expansion to SuperGrok Plus, Cursor Pro+ and all Cursor Teams plans. |
| W34-C067 | Grok Build / Voice miscellaneous updates | Agents / Audio | KEEP_CANDIDATE / MERGE_REVIEW | DailyX | Split into specific first-party W34 deltas (Build availability, possibly voice/playground) rather than one vague cluster. |
| W34-C068 | AWS DynamoDB Vector Search | Retrieval / Database | BOUNDARY_PRE_WINDOW | DailyX | Underlying GA was Aug 5; keep as background only unless a new W34 delta emerges. |
| W34-C069 | Original Dogwood open-source release | Agent Governance | BOUNDARY_PRE_WINDOW | DailyX | Original release pre-window; W34-C031 captures the in-window follow-up. |
| W34-C070 | Original Nemotron 3.5 Lightning / NeMo Switchyard | Open Weight / Routing | BOUNDARY_PRE_WINDOW | DailyX | Base release Aug 11; W34-C029 captures clean in-window JumpStart availability. |
| W34-C071 | Agent Lightning v1.0 | Agent Training | BOUNDARY_PRE_WINDOW | Sol prior map | Release/news appears Aug 11; preserve background unless new W34 delta verified. |
| W34-C072 | Wan 3.0 video prime / Runway Wan 3.0 availability | Video | BOUNDARY_POST_CUTOFF | Luna/previous Sol review | Observed Aug 24/26; not ordinary W34. |
| W34-C073 | InferenceX AgentX v3 | Evaluation / Inference | BOUNDARY_POST_CUTOFF / SPLIT_W34_METHOD | Sol prior map | AgentX v3 is Aug 24, but Aug 19 agentic benchmark methodology may remain an ordinary research candidate. |
| W34-C074 | Google Gemini Omni 1.1 Flash | Multimodal | BOUNDARY_POST_CUTOFF | Luna lead | Aug 27. |
| W34-C075 | Google Gemini 3.5 Transcribe | Speech | BOUNDARY_POST_CUTOFF | Luna lead | Aug 26. |
| W34-C076 | MiniMax Music 3.0 | Audio / Open Weight | BOUNDARY_PRE_WINDOW | Luna carry-over check | Aug 13; not W34 unless new adoption delta. |
| W34-C077 | MiniMax H3 | Foundation Models | BOUNDARY_PRE_WINDOW | Luna carry-over check | Aug 3. |
| W34-C078 | ScienceFlow v1 paper | Research / Agents / Retrieval | BOUNDARY_PRE_WINDOW | Luna arXiv lead | Submitted Aug 14 14:54Z before W34 start. |
| W34-C079 | CoRun paper | Research / Evaluation | BOUNDARY_PRE_WINDOW | Luna arXiv lead | Submitted Aug 14 15:17Z before W34 start. |
| W34-C080 | LAPF paper | Research / Agents / Multimodal | KEEP_CANDIDATE / RESEARCH_SCREEN | Luna arXiv lead | Submitted Aug 15 11:28Z; abstract-level locator pending canonical arXiv capture. |
| W34-C081 | Agent inheritance / creative-agent governance paper | Research / Safety | KEEP_CANDIDATE / RESEARCH_SCREEN | Luna arXiv lead | Submitted Aug 15 20:17Z; speculative research must remain research, not operational fact. |
| W34-C082 | EgoGazeLite paper | Research / Multimodal / Edge | KEEP_CANDIDATE / RESEARCH_SCREEN | Luna arXiv lead | Submitted Aug 16; on-device gaze predictor for token-efficient multimodal video. |
| W34-C083 | Embodied-agent security paper | Research / Safety / Multimodal | KEEP_CANDIDATE / RESEARCH_SCREEN | Luna arXiv lead | Submitted Aug 17; foundation-model embodied-agent attack/defense research. |
| W34-C084 | Renormalising Generative Models for Active Inference paper | Research | BOUNDARY_PRE_WINDOW | DailyX; arXiv 2608.09512 | arXiv v1 was submitted Aug 10 12:14Z, before W34. Retain only as research context unless a distinct W34 update/event is identified. |
| W34-C085 | Agent-harness / DarwinX-style evolution research mentions | Research / Agents | KEEP_CANDIDATE / RESEARCH_SCREEN | DailyX | Keep as research lead; split concrete papers/repos from vague community discussion before Evidence. |
| W34-C086 | OpenRouter Image Generation API tutorial/product workflow | Image / API | KEEP_CANDIDATE / SCREENING_REQUIRED | OpenRouter official Aug 17 | New code-first workflow around unified image API; screen against more material image events


## Verification pass 1 — resolved gaps


- `W34-C036`: RESOLVED — Google DeepMind official article is dated 2026-08-21.
- `W34-C052`: RESOLVED AS SPLIT DELTA — Computer History appears in OpenAI release notes on 2026-08-14; a clean W34 expansion to EEA/Switzerland/UK appears on 2026-08-20.
- `W34-C055`: RESOLVED — Varonis primary disclosure dated 2026-08-18 identifies CoSnitch / CVE-2026-24301 and states patches shipped that day; no observed exploitation.
- `W34-C057`: RESOLVED — TikTok/ByteDance official newsroom dated 2026-08-17 confirms the MPA–ByteDance MOU covering IP guardrails for Seedance/Seedream.
- `W34-C066`: RESOLVED AS ACCESS DELTA — xAI's base Grok Bot page is Aug 11, while the xAI news index records an Aug 21 expansion to additional plans.
- `W34-C084`: RECLASSIFIED PRE-WINDOW — arXiv 2608.09512 v1 is Aug 10 12:14Z.
- `W34-C037`: product identity confirmed on official MiniMax Design site; multiple independent dated sources converge on Aug 20 launch, but a first-party dated launch page has not yet been captured. Keep chronology qualifier for now.
- `W34-C038`: official SenseNova-U1.5 model/collection is confirmed, but current Hugging Face activity indicates the full model repository was populated/updated around or after the W34 boundary while a Preview artifact existed earlier. Preserve chronology verification rather than assuming the DailyX discussion equals the full-model release.


Verification pass 1 changes only Discovery classification/provenance notes; it does not perform Screening or Selection.
. |
| W34-C087 | AWS AgentCore governed tool-access patterns | Agent Governance / Tooling | KEEP_CANDIDATE / SCREENING_REQUIRED | AWS official Aug 21 | Governed/auditable enterprise tool gateway patterns; may merge into AgentCore control-plane feature. |
| W34-C088 | Amazon Nova Forge multi-turn custom reward functions | Training / RL | KEEP_CANDIDATE / DATE_ONLY_BOUNDARY | AWS technical post Aug 14 | Potential training-systems candidate; exact post time vs W34 start needs resolution. |
| W34-C089 | Hugging Face State of Open Models: Summer 2026 | Open Weight / Ecosystem Analysis | BOUNDARY_PRE_WINDOW | Hugging Face official Aug 14 article; official X post at 2026-08-14T16:28:41Z; corrected Grok r2 | Valuable ecosystem/adoption analysis, but the official X publication signal is before the W34 22:00Z start. Retain as background/context, not a W34 release. |
| W34-C090 | Amodei pace-of-progress safety commentary amplification | Safety / Community Context | KEEP_CONTEXT / COMMUNITY_SIGNAL | corrected Grok r2 ordinary post at 2026-08-18T19:02:46Z | Preserve the ordinary-window community observation, but it is not by itself a new technical release or policy event and has no linked primary artifact in r2. |
| W34-C091 | Adobe Firefly Audio generally available | Audio / Music / Speech / Creative Workflow | KEEP_CANDIDATE | Adobe official Aug 20 | Generate Music, Generate Speech, and Generate Sound Effects broadly available in Firefly; commercially safe workflow claims are vendor-framed. |
| W34-C092 | MOSS-VL W34 technical-report and ms-swift integration delta | Multimodal / Open Weight / Tooling | KEEP_CANDIDATE | OpenMOSS official repo; Aug 15 technical report and Aug 21 ms-swift support | Base MOSS-VL models predate W34; retain the in-window technical-report and first-class inference/fine-tuning integration deltas. |
| W34-C093 | 4DAnyone 4D human reconstruction paper | Research / Video / 4D Generation | KEEP_CANDIDATE / RESEARCH_SCREEN | arXiv Aug 20 | Reconstructs 4D humans from casual monocular video using multiview-consistent generation and 4D Gaussian Splatting; research claims require paper-level screening. |
| W34-C094 | Writer Palmyra X6 flagship model / harness launch | Foundation Models / Agents / Enterprise | BOUNDARY_PRE_WINDOW | Writer official Aug 13 launch; Aug 14 press-release page | Underlying launch is Aug 13 and must not be redated into W34; retain as context for in-window enterprise-agent economics discussion only. |
| W34-C095 | ChatGPT Aug 21 product-experience updates | Product / Plugins / UX | KEEP_CANDIDATE / SCREENING_REQUIRED | OpenAI official release notes Aug 21 | Improved plugin discovery, more time-aware answers, faster long web conversations, and earlier interactive-content rendering; screen as a grouped product delta. |
| W34-C096 | Apple Messages plugin for ChatGPT Work and Codex | Agents / Plugins / Messaging | KEEP_CANDIDATE | OpenAI official release notes Aug 20 | Apple-silicon macOS plugin can read/search iMessage, SMS, and RCS and prepare/send messages through Messages with approval by default. |
| W34-C097 | Kling AI 3.0 Turbo plus Kling MCP / CLI disclosure | Video / Agents / MCP / CLI | KEEP_CANDIDATE | Kuaishou official Q2 results Aug 19 | Official filing states Kling 3.0 Turbo release and official launch of Kling MCP and CLI for agent-orchestrated batch content creation; distinguish from February Kling 3.0 base launch. |
| W34-C098 | LFM2.5 Q4_0 quantization-aware distillation checkpoints | Local AI / Quantization / Inference | KEEP_CANDIDATE | Liquid AI official Aug 19 | Updated 4-bit checkpoints for four LFM2.5 models trained with QAD; vendor reports roughly 97% BF16 average retention. |
| W34-C099 | GitHub Copilot for JetBrains enterprise-managed settings | Coding Agents / Governance / MCP | KEEP_CANDIDATE | GitHub official changelog Aug 18 | Adds enterprise plugin governance, MCP allow/deny lists, managed OpenTelemetry, and permission-mode controls in JetBrains. |
| W34-C100 | GitHub Copilot agentic experience in Slack | Coding Agents / Collaboration | KEEP_CANDIDATE | GitHub official changelog Aug 21; Slack Code related | Public preview brings Copilot cloud-agent sessions into Slack conversations and code channels with shared steering and PR workflows. |
| W34-C101 | GitHub Copilot shared agentic work in Microsoft Teams | Coding Agents / Collaboration | KEEP_CANDIDATE | GitHub official changelog Aug 21 | Public preview starts shared Copilot cloud-agent sessions from Teams discussions, with human-in-loop approval controls for agent-authored PRs. |
| W34-C102 | Google Antigravity enterprise subscription expansion | Coding Agents / Enterprise / Governance | KEEP_CANDIDATE | Google Cloud official Aug 20 | Antigravity becomes available in eligible Gemini Enterprise subscriptions with administrative, security, and pooled-spend controls. |
| W34-C103 | Google/DeepMind intelligent delegation for multi-agent systems | Research / Multi-Agent Systems | KEEP_CANDIDATE / RESEARCH_SCREEN | Google Cloud official Aug 21 referencing DeepMind delegation research | Enterprise-facing synthesis of adaptive delegation, contracts, negotiation, and security guardrails; screen the underlying research separately. |
| W34-C104 | AgentCore user-authorization-context propagation patterns | Agent Security / Identity / Tooling | KEEP_CANDIDATE / SCREENING_REQUIRED | AWS Security Blog Aug 19 | Infrastructure-enforced user authorization propagation across agent data/tool calls; important control-plane pattern, but a technical-how-to rather than a new model/product release. |
| W34-C105 | Asynchronous AgentCore invocation patterns in serverless pipelines | Agent Systems / Serving | KEEP_CANDIDATE / SCREENING_REQUIRED | AWS official Aug 19 | Task-token callback, direct service integration, and durable-function patterns for long-running agents without idle compute; implementation architecture item. |




## Process guard


No item in this file is rejected solely because Sol considers it low materiality. Items may be merged by event identity, but the source observations that led to them must remain traceable. Screening and later materiality/Selection are separate stages.