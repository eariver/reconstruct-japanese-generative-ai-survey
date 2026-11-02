---
sensor: grok-x-source-intake
task_id: "efficient-llm-reception-pass-01-r3"
parent_task_id: "efficient-llm-reception-pass-01-r2"
issue_id: "SP-efficient-llm-2026"
observed_at: "2026-09-21T17:16:12+00:00"
status: raw-correction
---

# X Reception Result r3 — efficient-llm-reception-pass-01

## 1. Executive signal summary

r3 is a reconciliation-only correction of r2. The 27 explicit Observation Records (OBS-R2-001 … OBS-R2-027) and the 24 account-ledger rows are preserved unchanged. No new X research was performed; no observations were added or deleted. The sole purpose is to correct internal numerical inconsistencies (FIRST_HAND totals, reception totals, coverage-bucket sums) so that every reported metric derives exactly from the explicit records, and to emit a verifiable FINAL_LEDGER_RECONCILIATION with LEDGER_COUNT_CONSISTENCY.

Qualified independent and runtime-maintainer signal exists for all five capstones, densest for DeepSeek V4.1 Flash (vLLM day-0 + hostile local full-precision attempt + API tok/s claims) and Qwen3.8-Flash-Next (multiple config-rich local llama.cpp / consumer-GPU measurements). GLM-5.3-Flash has strong packaging enablement (Unsloth GGUF) plus local container and Mac throughput anecdotes. Kimi Linear has at least one detailed llama.cpp configuration with measured numbers. Jev has one substantive independent evaluation plus early integration/adoption posts.

Local MoE deployment repeatedly surfaces host-RAM / offload / VRAM-headroom as practical constraints. Counter-signals on aggressive quant quality and long-context/agentic brittleness appear but are not dense. All technical claims remain subject to primary-source verification.

## 2. Exact coverage ledger (reconciled)

Primary coverage-bucket assignment (mutually exclusive; each of the 27 records assigned to exactly one primary bucket):

| Primary coverage bucket | Count | OBS-R2 IDs (primary) |
|-------------------------|-------|----------------------|
| DeepSeek V4.1 Flash | 7 | 001,002,003,004,005,006,007 |
| Qwen3.8-Flash-Next | 6 | 008,009,010,011,012,027 |
| Kimi Linear | 2 | 013,014 |
| GLM-5.3-Flash | 5 | 015,016,017,019,020 |
| Jev | 3 | 021,022,023 |
| Local stack / mechanisms (cross-cutting) | 4 | 018,024,025,026 |
| **Total** | **27** | |

Note: OBS-R2-003 is dual-target (DeepSeek vs Qwen) but counted once under DeepSeek as primary; OBS-R2-018 reports both Qwen and GLM numbers but is counted under local-stack cross-cutting; OBS-R2-019 is comparative commentary counted under GLM; OBS-R2-024–026 are brief preference signals counted under local-stack / mechanisms for reconciliation simplicity. All 27 records remain present and unchanged.

LOW_SIGNAL lanes: dense SGLang/LMCache first-hand configs; systematic Jev production failure logs; matched multi-model head-to-head on identical hardware.

## 3. Capstone model findings

**DeepSeek V4.1 Flash** — Early runtime readiness (vLLM day-0), independent local full-precision feasibility on single 4090 at low tok/s, API throughput claims (~325 tok/s cited), cost-positive reception versus higher-tier models, and agentic workflow use.

**Qwen3.8-Flash-Next** — Multiple first-hand local measurements on 3090/4090-class and Mac M5 Ultra hardware; MoE offload and quant choices decisive; used as OpenCode / agent endpoints.

**Kimi Linear** — Concrete llama.cpp server flags and measured 160/30–40 tok/s on modest GPU; characterized by one practitioner as personality-oriented rather than coding-first.

**GLM-5.3-Flash** — Unsloth GGUF packaging enabling 3-bit on 128 GB RAM and claimed speed-ups; local air-gapped vLLM container reports; Mac throughput comparisons.

**Jev** — Independent classification-oriented evaluation (calibrated positive); OpenCode permission and gateway/SDK adoption signals; still thin on independent production failure modes.

## 4. Local inference / deployment findings

GGUF + llama.cpp is the dominant consumer path. MoE offload to host RAM (`--n-cpu-moe`, `--cpu-moe`, streaming) is repeatedly required. VRAM headroom, KV quant, batch size and NUMA appear as practical levers. vLLM has day-0 support for DeepSeek V4.1 Flash. Heterogeneous and long-context setups surface bandwidth and capacity limits.

## 5. Mechanism-level findings

- MoE + host/Engram-style memory: large parameter fractions can live off-HBM; host RAM/bandwidth become new bottlenecks.
- Sparse/linear attention (KDA, QSA hybrids): architecture claims of KV reduction appear; practical X measurements still limited.
- Quantization: aggressive low-bit GGUF in active use; quality mixed by task.
- MTP / speculative: mentioned in packaging speed-ups; limited independent acceptance-rate data.
- Test-time budgets / overthinking: sparse explicit signal in accepted set.

## 6. Independent benchmark / reproduction leads

- DeepSeek V4.1 Flash official-API ~325 tok/s claim (OBS-R2-007).
- Single-4090 hostile full-precision 1–10 tok/s @ ~1M ctx (OBS-R2-002).
- Qwen3.8-Flash-Next 30 t/s on i9+4090 specific quant (OBS-R2-008).
- Kimi Linear 48B Q4_K_M llama.cpp numbers + flags (OBS-R2-014).
- Unsloth GLM-5.3-Flash GGUF + speed claims (OBS-R2-016, OBS-R2-017).
- Jev independent classification write-up (OBS-R2-022).
- Mac M5 Ultra PP/TG numbers for Qwen and GLM (OBS-R2-012, OBS-R2-020).

All require controlled re-measurement or primary confirmation.

## 7. Failure / counter-signal ledger

- MoE host-RAM / offload cliffs: present (e.g., one-step-too-far slowdowns noted in related local stacks).
- Quant quality loss: anecdotal for aggressive low-bit builds (mainly Qwen-related).
- Long-context / agentic brittleness: some failure-shape similarity noted in cert-trap comparison (OBS-R2-003).
- Jev: independent evaluator flagged possible contamination risk on public sets and limited real B2B data; production failure cases still thin → LOW_SIGNAL for systematic failure modes.
- Speculative/MTP acceptance, sparse-attention kernel maturity, test-time overthinking: NO_COUNTER_SIGNAL_FOUND_AFTER_TARGETED_SEARCH (searched model+fail/OOM/quant/quality/bug within window; no dense independent negative corpus recovered).

## 8. Complete account diversity ledger

| Handle | Apparent role / affiliation evidence | Affiliation class | Accepted OBS IDs | Count | Technologies |
|--------|--------------------------------------|-------------------|------------------|-------|--------------|
| @vllm_project | vLLM project account | RUNTIME_OR_PACKAGING_MAINTAINER | OBS-R2-001 | 1 | DeepSeek V4.1 Flash, vLLM |
| @_xjdr | Independent practitioner (self-described hostile implementation) | INDEPENDENT | OBS-R2-002 | 1 | DeepSeek V4.1 Flash |
| @Whimsicali | Independent tester (cert-trap run) | INDEPENDENT | OBS-R2-003 | 1 | DeepSeek V4.1 Flash, Qwen3.8-Flash-Next |
| @bookwormengr | Independent technical analysis (Engram/HBM commentary) | INDEPENDENT | OBS-R2-004 | 1 | DeepSeek V4.1 Flash, Engram |
| @odas0r | Independent developer (provider tok/s testing) | INDEPENDENT | OBS-R2-005 | 1 | DeepSeek V4.1 Flash |
| @mikawuf | Independent (quotes API speed/cost) | INDEPENDENT | OBS-R2-006, OBS-R2-007 | 2 | DeepSeek V4.1 Flash |
| @aagosh | Independent local benchmaxxer | INDEPENDENT | OBS-R2-008 | 1 | Qwen3.8-Flash-Next |
| @ItsmeAjayKV | Independent llama.cpp experimenter | INDEPENDENT | OBS-R2-009 | 1 | Qwen3.8-Flash-Next |
| @Oluwaphilemon1 | Independent systems note on MoE offload | INDEPENDENT | OBS-R2-010 | 1 | Qwen3.8-Flash-Next, MoE |
| @coffeecup2020 | Independent local LLM (GX10 / DGX-class) | INDEPENDENT | OBS-R2-011 | 1 | Qwen3.8-Flash-Next |
| @wei_wang | Independent (M5 Ultra Qwen numbers) | INDEPENDENT | OBS-R2-012 | 1 | Qwen3.8-Flash-Next |
| @JDBtracker | Independent llama.cpp user | INDEPENDENT | OBS-R2-013, OBS-R2-014 | 2 | Kimi Linear |
| @UnslothAI | Unsloth packaging project | RUNTIME_OR_PACKAGING_MAINTAINER | OBS-R2-015, OBS-R2-016 | 2 | GLM-5.3-Flash |
| @Soveryn_AI | Independent local container operator | INDEPENDENT | OBS-R2-017 | 1 | GLM-5.3-Flash |
| @djdextune | Independent benchmark poster (Mac numbers) | INDEPENDENT | OBS-R2-018 | 1 | Qwen3.8-Flash-Next, GLM-5.3-Flash |
| @liuliu | Independent (throughput commentary) | INDEPENDENT | OBS-R2-019 | 1 | GLM-5.3-Flash, Qwen |
| @jnardiello | Independent local user | INDEPENDENT | OBS-R2-020 | 1 | GLM-5.3-Flash |
| @vesko_st | Independent evaluator (classification write-up) | INDEPENDENT | OBS-R2-021 | 1 | Jev |
| @OpeOginni | Independent integrator (OpenCode permissions) | INDEPENDENT | OBS-R2-022 | 1 | Jev |
| @inference_sh | Service announcing Jev availability | UNCLEAR | OBS-R2-023 | 1 | Jev |
| @loktar00 | Independent local-LLM user | INDEPENDENT | OBS-R2-024 | 1 | DeepSeek Flash-class |
| @gajjar81 | Independent user (cost/quality anecdote) | INDEPENDENT | OBS-R2-025 | 1 | DeepSeek V4.1 Flash |
| @policeoser | Independent (coding preference) | INDEPENDENT | OBS-R2-026 | 1 | GLM-5.3-Flash |
| @victormustar | Hugging Face Head of Product (quoted context) | VENDOR_OR_PROJECT | OBS-R2-027 | 1 | Qwen3.8-Flash-Next (context) |

**Exact metrics from ledger (reconciled against the 27 explicit records)**  
- Accepted observation count: 27  
- Unique direct status URL count: 27  
- Unique account count: 24  
- Unique independent account count: 20  
- Vendor/project-affiliated account count: 1  
- Runtime/packaging-maintainer account count: 2  
- Unclear-affiliation account count: 1  
- FIRST_HAND YES: 17  
- FIRST_HAND NO: 3  
- FIRST_HAND UNCLEAR: 7  

## 9. Primary-source follow-up leads

- DeepSeek V4.1 Flash technical report / HF card / API docs (CED, Engram, KV footprint).  
- Qwen3.8-Flash-Next GitHub/HF (GDN+QSA, N-gram memory).  
- Kimi Linear arXiv 2510.26692 + KDA kernel + vLLM implementations.  
- GLM-5.3-Flash HF / Z.ai report (hybrid attention, mHC).  
- TypeSafe Jev docs + any published System One eval methodology.  
- vLLM / llama.cpp / Unsloth PRs and release notes cited by practitioners.  
- Controlled re-runs of all cited tok/s and classification numbers.

## 10. LOW_SIGNAL / unresolved targets

- Dense independent production failure modes for Jev.  
- First-hand SGLang / LMCache / KTransformers configs for the five named models.  
- Config-matched multi-model throughput tables on identical hardware.  
- Long-running agentic harness failure rates with exact reasoning-budget settings.  
- Conditional Memory / Engram practical quality impact beyond vendor claims.

UNRESOLVED_NOT_COUNTED (r1 prose references that could not be bound to a recovered exact status URL in this pass): generic “multiple posts” cost anecdotes and some secondary reaction threads without recoverable primary status IDs.

## 11. Method and limitations

r2 reused r1 leads and performed additional targeted keyword/semantic recovery solely to obtain exact status URLs and fill weak lanes. Only posts with direct `https://x.com/<handle>/status/<id>` are accepted. Approximate counts eliminated. Affiliation never inferred without explicit evidence. Time scope 2025-01-01–2026-09-21, priority 2026. Limitations: X ranking bias, possible under-sampling of non-English signal, single-configuration measurements not comparable across hardware.

## 12. Complete Observation Records

**OBS-R2-001**  
URL: https://x.com/vllm_project/status/2097940813242405272  
Status ID: 2097940813242405272  
Handle: @vllm_project  
Date: 2026-09-10  
Target: DeepSeek V4.1 Flash / vLLM  
Category: RUNTIME_MAINTAINER  
FIRST_HAND: YES  
Concise: Day-0 vLLM serving support on NVIDIA and AMD; notes Engram n-gram memory and reduced layers writing compressed KV.  
Hardware/config: N/A (serving announcement)  
Runtime: vLLM  
Measurement: N/A  
Comparability caveat: Announcement, not independent throughput.  
Reception: positive  
Primary-source lead: vLLM release notes / DeepSeek HF  
Why matters: Establishes early runtime readiness.  
Confidence: high  
Boundary: Serving claim only.

**OBS-R2-002**  
URL: https://x.com/_xjdr/status/2100712931906494595  
Status ID: 2100712931906494595  
Handle: @_xjdr  
Date: 2026-09-17  
Target: DeepSeek V4.1 Flash  
Category: FIRST_HAND_DEPLOYMENT / INDEPENDENT_TECHNICAL_ANALYSIS  
FIRST_HAND: YES  
Concise: Hostile from-scratch implementation achieved 1–10 tok/s bs=1 ctx=1M+ full-precision mix (bf16/fp8/mxfp4) on single 4090 + 64 GB CPU RAM + 1 TB NVMe; architecture praised.  
Hardware: 1×4090, 64 GB RAM, 1 TB NVMe  
Measurement: 1–10 tok/s (expert-cache dependent)  
Comparability caveat: Full precision, single config, non-optimized.  
Reception: positive technical  
Primary-source lead: Architecture paper / HF weights  
Why matters: Concrete local feasibility under constrained hardware.  
Confidence: medium-high  
Boundary: Self-reported single run.

**OBS-R2-003**  
URL: https://x.com/Whimsicali/status/2100288205425955012  
Status ID: 2100288205425955012  
Handle: @Whimsicali  
Date: 2026-09-16  
Target: DeepSeek V4.1 Flash vs Qwen3.8-Flash-Next  
Category: FIRST_HAND_BENCHMARK  
FIRST_HAND: YES  
Concise: Cert-trap comparison (xhigh, n=40); DeepSeek escaped 26/40; Qwen Flash-Next 33/41; similar failure shapes; DeepSeek ~4.5 min/cell, ~$1.50 total.  
Hardware: API (DeepSeek) vs local 4×7900 XTX (Qwen)  
Measurement: escape rates, latency, cost  
Comparability caveat: Different backends.  
Reception: mixed  
Primary-source lead: Rubric / method details  
Why matters: Independent side-by-side failure-mode signal.  
Confidence: medium  
Boundary: One harness, one rubric.

**OBS-R2-004**  
URL: https://x.com/bookwormengr/status/2097975577886257184  
Status ID: 2097975577886257184  
Handle: @bookwormengr  
Date: 2026-09-10  
Target: DeepSeek V4.1 Flash / Engram  
Category: INDEPENDENT_TECHNICAL_ANALYSIS  
FIRST_HAND: NO  
Concise: Highlights that large Engram embeddings can reside on host LPDDR rather than HBM, reducing HBM and prefill FLOPs; links to prior DeepSeek paper direction.  
Reception: neutral-positive technical  
Primary-source lead: DeepSeek Engram paper / V4.1 report  
Why matters: Mechanism-level reception of host-memory scaling.  
Confidence: medium  
Boundary: Analysis, not measurement.

**OBS-R2-005**  
URL: https://x.com/odas0r/status/2102056149721780554  
Status ID: 2102056149721780554  
Handle: @odas0r  
Date: 2026-09-21  
Target: DeepSeek V4.1 Flash  
Category: FIRST_HAND_BENCHMARK  
FIRST_HAND: YES  
Concise: Provider tok/s testing; DeepSeek V4.1 starts 100–200 tok/s then drops to 30–80 tok/s at ~20% context; few providers reach +200 tok/s sustained.  
Measurement: 100–200 → 30–80 tok/s  
Comparability caveat: Provider-side, context-dependent.  
Reception: mixed  
Why matters: Real-world sustained throughput observation.  
Confidence: medium  
Boundary: Provider opaque.

**OBS-R2-006**  
URL: https://x.com/mikawuf/status/2101994419213705557  
Status ID: 2101994419213705557  
Handle: @mikawuf  
Date: 2026-09-21  
Target: DeepSeek V4.1 Flash  
Category: SECONDARY_REACTION / cost signal  
FIRST_HAND: UNCLEAR  
Concise: Notes cache economics (1/4 HBM, 1/8 SSD) and off-peak rates; cites developer report of under $1 for 100M+ tokens.  
Reception: positive cost  
Primary-source lead: Official pricing / cache docs  
Why matters: Cost-reception lead.  
Confidence: low-medium  
Boundary: Secondary citation.

**OBS-R2-007**  
URL: https://x.com/mikawuf/status/2101994416688804266  
Status ID: 2101994416688804266  
Handle: @mikawuf  
Date: 2026-09-21  
Target: DeepSeek V4.1 Flash  
Category: SECONDARY_REACTION  
FIRST_HAND: UNCLEAR  
Concise: Cites measured 325 tok/s via official API; restates 552B MoE with 8B/16B active.  
Measurement: 325 tok/s (cited)  
Comparability caveat: Secondary; hardware/context not fully specified in post.  
Reception: positive  
Primary-source lead: Official API benchmarks  
Why matters: Throughput claim requiring verification.  
Confidence: low-medium  
Boundary: Citation only.

**OBS-R2-008**  
URL: https://x.com/aagosh/status/2102074687085850707  
Status ID: 2102074687085850707  
Handle: @aagosh  
Date: 2026-09-21  
Target: Qwen3.8-Flash-Next  
Category: FIRST_HAND_BENCHMARK  
FIRST_HAND: YES  
Concise: 30 t/s on 2-year-old i9 64 GB + RTX 4090; quant AD-3.84bpw-IQ4_XS-M64; used as OpenCode API endpoint from MacBook.  
Hardware: i9, 64 GB, RTX 4090  
Measurement: 30 t/s  
Reception: positive  
Why matters: Practical local agentic workflow with disclosed quant.  
Confidence: medium-high  
Boundary: Single quant/hardware.

**OBS-R2-009**  
URL: https://x.com/ItsmeAjayKV/status/2093010496324829542  
Status ID: 2093010496324829542  
Handle: @ItsmeAjayKV  
Date: 2026-08-27  
Target: Qwen3.8-Flash-Next / llama.cpp  
Category: FIRST_HAND_BENCHMARK  
FIRST_HAND: YES  
Concise: After llama.cpp PR, UD-IQ3_XXS (~82 GB) on 3090 24 GB + 64 GB RAM reached 252K context, ~21 t/s decode, peak prefill 245 t/s @ 16K with q8_0 and -ncmoe 36.  
Hardware: 3090 24 GB + 64 GB RAM  
Runtime: llama.cpp (post-PR)  
Measurement: 21 t/s decode, 245 t/s prefill peak  
Reception: positive  
Why matters: Quantified local long-context improvement.  
Confidence: medium-high  
Boundary: Specific PR and quant.

**OBS-R2-010**  
URL: https://x.com/Oluwaphilemon1/status/2100204861979574381  
Status ID: 2100204861979574381  
Handle: @Oluwaphilemon1  
Date: 2026-09-16  
Target: Qwen3.8-Flash-Next / MoE local  
Category: INDEPENDENT_TECHNICAL_ANALYSIS  
FIRST_HAND: UNCLEAR  
Concise: Systems note: 2×3090 + 128 GB RAM setups can reach 300–600 tok/s prefill / 40–50 tok/s decode when quant, KV, --n-cpu-moe, batch, NUMA and VRAM headroom are tuned.  
Hardware: 2×3090 + 128 GB (reported class)  
Measurement: 300–600 / 40–50 tok/s (reported)  
Reception: positive systems  
Why matters: Emphasizes MoE offload and systems variables.  
Confidence: medium  
Boundary: Aggregated report style.

**OBS-R2-011**  
URL: https://x.com/coffeecup2020/status/2102074679699603657  
Status ID: 2102074679699603657  
Handle: @coffeecup2020  
Date: 2026-09-21  
Target: Qwen3.8-Flash-Next  
Category: FIRST_HAND_DEPLOYMENT  
FIRST_HAND: YES  
Concise: Qwen3.8-Flash-Next on single ASUS GX10 (DGX Spark-class): 2 parallel sessions, 512K context, fully local; multi-hour Hermes agent run with few interventions.  
Hardware: GX10  
Reception: positive  
Why matters: Local long-horizon agent success signal.  
Confidence: medium  
Boundary: Qualitative + partial config.

**OBS-R2-012**  
URL: https://x.com/wei_wang/status/2102054751261131075  
Status ID: 2102054751261131075  
Handle: @wei_wang  
Date: 2026-09-21  
Target: Qwen3.8-Flash-Next  
Category: FIRST_HAND_BENCHMARK (secondary numbers)  
FIRST_HAND: UNCLEAR  
Concise: Reports M5 Ultra 256 GB running Qwen3.8-Flash-Next multi-turn agent/tool workloads at 60–85 tok/s generation; prompt processing ~2.5× vs M3 Ultra.  
Hardware: M5 Ultra 256 GB  
Measurement: 60–85 tok/s gen  
Reception: positive  
Primary-source lead: MacStories M5 Ultra review  
Why matters: High-end Apple Silicon practical numbers.  
Confidence: medium  
Boundary: Numbers attributed to review.

**OBS-R2-013**  
URL: https://x.com/JDBtracker/status/2099412688560361952  
Status ID: 2099412688560361952  
Handle: @JDBtracker  
Date: 2026-09-14  
Target: Kimi Linear 48B  
Category: FIRST_HAND_DEPLOYMENT  
FIRST_HAND: YES  
Concise: Good results with Kimi-Linear 48B on 32 GB system RAM + 5060 8 GB; 160 tokens/second with llama.cpp.  
Hardware: 32 GB RAM, RTX 5060 8 GB  
Runtime: llama.cpp  
Measurement: 160 tok/s  
Reception: positive  
Why matters: Early concrete local throughput for Kimi Linear.  
Confidence: medium  
Boundary: Brief report.

**OBS-R2-014**  
URL: https://x.com/JDBtracker/status/2100038317429383437  
Status ID: 2100038317429383437  
Handle: @JDBtracker  
Date: 2026-09-16  
Target: Kimi Linear 48B  
Category: FIRST_HAND_DEPLOYMENT  
FIRST_HAND: YES  
Concise: Full llama-server flags for Q4_K_M; 160 tok/s read & 30–40 tok/s generate on 7900X 12c/24t + RTX 5060 8 GB; model described as willful/personality-oriented, not for programming.  
Hardware + flags: fully posted  
Measurement: 160 read / 30–40 gen tok/s  
Reception: mixed (fun positive, coding limited)  
Why matters: Rarest detailed config + measured numbers for the model.  
Confidence: medium-high  
Boundary: One machine, one use-case characterization.

**OBS-R2-015**  
URL: https://x.com/UnslothAI/status/2092986464196002094  
Status ID: 2092986464196002094  
Handle: @UnslothAI  
Date: 2026-08-27  
Target: GLM-5.3-Flash  
Category: RUNTIME_MAINTAINER / ADOPTION_SIGNAL  
FIRST_HAND: YES  
Concise: GLM-5.3-Flash GGUF released; 3-bit runnable on 128 GB RAM via Unsloth.  
Runtime: Unsloth GGUF / llama.cpp path  
Reception: positive enablement  
Primary-source lead: Unsloth docs / HF GGUF repo  
Why matters: Lowers local barrier for 320B-class MoE.  
Confidence: high (packaging existence)  
Boundary: Packaging claim.

**OBS-R2-016**  
URL: https://x.com/UnslothAI/status/2095852388888522890  
Status ID: 2095852388888522890  
Handle: @UnslothAI  
Date: 2026-09-04  
Target: GLM-5.3-Flash  
Category: RUNTIME_MAINTAINER  
FIRST_HAND: YES  
Concise: Claimed 1.6–3.4× faster local GGUF inference with optimized decoding + MTP support.  
Measurement: 1.6–3.4× (claimed)  
Reception: positive  
Primary-source lead: Unsloth speed guide  
Why matters: MTP / decoding optimization lead.  
Confidence: medium (multiplier needs independent check)  
Boundary: Vendor-packaging claim.

**OBS-R2-017**  
URL: https://x.com/Soveryn_AI/status/2100960374669410616  
Status ID: 2100960374669410616  
Handle: @Soveryn_AI  
Date: 2026-09-18  
Target: GLM-5.3-Flash  
Category: FIRST_HAND_DEPLOYMENT  
FIRST_HAND: YES  
Concise: Local vLLM container (exl3-instanttensor) on Spark; zero public internet sockets; offline env flags; weights on disk.  
Runtime: vLLM container  
Reception: positive (security/local)  
Why matters: Air-gapped local deployment signal.  
Confidence: medium-high  
Boundary: One operator’s setup.

**OBS-R2-018**  
URL: https://x.com/djdextune/status/2102046634909790635  
Status ID: 2102046634909790635  
Handle: @djdextune  
Date: 2026-09-21  
Target: Qwen3.8-Flash-Next & GLM-5.3-Flash  
Category: FIRST_HAND_BENCHMARK (reported numbers)  
FIRST_HAND: UNCLEAR  
Concise: MacStories M5 Ultra 256 GB numbers: Qwen3.8 Flash Next PP 2887 / TG 108 tps; GLM 5.3 Flash PP 1107 / TG 41 tps (vs M3 Ultra baselines).  
Hardware: M5 Ultra 256 GB  
Measurement: as above  
Reception: neutral (reporting)  
Primary-source lead: MacStories review  
Why matters: High-end Apple Silicon comparative throughput.  
Confidence: medium  
Boundary: Secondary to review.

**OBS-R2-019**  
URL: https://x.com/liuliu/status/2102077521852502101  
Status ID: 2102077521852502101  
Handle: @liuliu  
Date: 2026-09-21  
Target: GLM-5.3-Flash / Qwen3.8-Flash-Next  
Category: INDEPENDENT_TECHNICAL_ANALYSIS  
FIRST_HAND: UNCLEAR  
Concise: Speculates ~2000 tok/s possible for GLM 5.3 Flash on M5 Ultra; questions whether peak number or other factors matter more.  
Reception: neutral  
Why matters: Practitioner prioritization discussion.  
Confidence: low  
Boundary: Speculation.

**OBS-R2-020**  
URL: https://x.com/jnardiello/status/2102072642832396792  
Status ID: 2102072642832396792  
Handle: @jnardiello  
Date: 2026-09-21  
Target: GLM-5.3-Flash  
Category: FIRST_HAND_DEPLOYMENT  
FIRST_HAND: YES  
Concise: Continues to use local GLM 5.3 Flash as “beast” paired with frontier models for planning/reviews.  
Reception: positive  
Why matters: Sustained local adoption signal.  
Confidence: medium  
Boundary: Qualitative.

**OBS-R2-021**  
URL: https://x.com/vesko_st/status/2102078925644108051  
Status ID: 2102078925644108051  
Handle: @vesko_st  
Date: 2026-09-21  
Target: Jev  
Category: FIRST_HAND_BENCHMARK / INDEPENDENT_TECHNICAL_ANALYSIS  
FIRST_HAND: YES  
Concise: Independent eval on RC/commonsense + hand-authored Wikipedia set + older customer-service sets; roughly Sonnet/Opus level on several; large cost/speed advantage; caveats on contamination and non-B2B data.  
Reception: positive calibrated  
Primary-source lead: Author’s full write-up link  
Why matters: Rarest independent non-vendor technical look at Jev.  
Confidence: medium-high  
Boundary: Classification-focused; not full agent production.

**OBS-R2-022**  
URL: https://x.com/OpeOginni/status/2102076840844087318  
Status ID: 2102076840844087318  
Handle: @OpeOginni  
Date: 2026-09-21  
Target: Jev  
Category: FIRST_HAND_DEPLOYMENT / ADOPTION_SIGNAL  
FIRST_HAND: YES  
Concise: OpenCode permissions plugin uses Jev for intent-based allow/deny; now supports multiple providers (Zen, OpenRouter, Vercel, TypeSafe).  
Reception: positive integration  
Why matters: Concrete agent-tool integration.  
Confidence: medium-high  
Boundary: One plugin, demo context.

**OBS-R2-023**  
URL: https://x.com/inference_sh/status/2102078304157159740  
Status ID: 2102078304157159740  
Handle: @inference_sh  
Date: 2026-09-21  
Target: Jev  
Category: ADOPTION_SIGNAL  
FIRST_HAND: NO  
Concise: typesafe/jev announced live on inference.sh.  
Reception: neutral-positive availability  
Why matters: Hosting/gateway adoption.  
Confidence: high (announcement)  
Boundary: Service announcement.

**OBS-R2-024**  
URL: https://x.com/loktar00/status/2102077810743386578  
Status ID: 2102077810743386578  
Handle: @loktar00  
Date: 2026-09-21  
Target: DeepSeek Flash-class local  
Category: FIRST_HAND_DEPLOYMENT  
FIRST_HAND: YES  
Concise: “Best local model I run” style comparison to a good DeepSeek Flash lite.  
Reception: positive  
Why matters: Local user preference signal.  
Confidence: low-medium  
Boundary: Qualitative, model variant unclear.

**OBS-R2-025**  
URL: https://x.com/gajjar81/status/2102079506139983877  
Status ID: 2102079506139983877  
Handle: @gajjar81  
Date: 2026-09-21  
Target: DeepSeek V4.1 Flash  
Category: FIRST_HAND_DEPLOYMENT  
FIRST_HAND: YES  
Concise: Tried DeepSeek V4.1 Flash; did almost equal job to Codex at much lower budget/tokens.  
Reception: positive cost/quality  
Why matters: Cost-sensitive practitioner reception.  
Confidence: medium  
Boundary: Single-user anecdote.

**OBS-R2-026**  
URL: https://x.com/policeoser/status/2102078891237978144  
Status ID: 2102078891237978144  
Handle: @policeoser  
Date: 2026-09-21  
Target: GLM-5.3-Flash  
Category: SECONDARY_REACTION  
FIRST_HAND: UNCLEAR  
Concise: GLM 5.3 Flash still better at coding (comparative remark).  
Reception: positive coding  
Why matters: Coding-preference signal.  
Confidence: low  
Boundary: Brief comparative claim.

**OBS-R2-027**  
URL: https://x.com/victormustar/status/2102073792390447486  
Status ID: 2102073792390447486  
Handle: @victormustar  
Date: 2026-09-21  
Target: Qwen3.8-Flash-Next (context)  
Category: SECONDARY_REACTION  
FIRST_HAND: NO  
Concise: Notes a new open-weight terminal model is a Qwen3.8 Flash Next finetune; calls Qwen3.8 Flash Next “my <3 local model”.  
Reception: positive  
Why matters: HF-adjacent local preference signal.  
Confidence: medium  
Boundary: Contextual remark.

## 13. FINAL_LEDGER_RECONCILIATION

OBSERVATION_RECORD_COUNT: 27  
UNIQUE_STATUS_URL_COUNT: 27  
UNIQUE_ACCOUNT_COUNT: 24  
INDEPENDENT_ACCOUNT_COUNT: 20  
VENDOR_PROJECT_ACCOUNT_COUNT: 1  
RUNTIME_MAINTAINER_ACCOUNT_COUNT: 2  
UNCLEAR_AFFILIATION_ACCOUNT_COUNT: 1  

FIRST_HAND_YES_COUNT: 17  
FIRST_HAND_NO_COUNT: 3  
FIRST_HAND_UNCLEAR_COUNT: 7  
(17 + 3 + 7 = 27)

Reception (normalized to four mutually exclusive buckets from the explicit “Reception:” lines):

- POSITIVE_RECEPTION_COUNT: 20  
  (includes “positive”, “positive technical”, “positive cost”, “positive systems”, “positive enablement”, “positive (security/local)”, “positive calibrated”, “positive integration”, “positive cost/quality”, “positive coding”)
- MIXED_RECEPTION_COUNT: 3  
  (OBS-R2-003, OBS-R2-005, OBS-R2-014)
- NEGATIVE_RECEPTION_COUNT: 0  
- NEUTRAL_RECEPTION_COUNT: 4  
  (OBS-R2-004 “neutral-positive technical” normalized to neutral; OBS-R2-018 “neutral (reporting)”; OBS-R2-019 “neutral”; OBS-R2-023 “neutral-positive availability” normalized to neutral)

(20 + 3 + 0 + 4 = 27)

Non-exclusive category label occurrences (a record may carry more than one label; totals therefore exceed 27):

- RUNTIME_MAINTAINER: 3 (001, 015, 016)  
- FIRST_HAND_DEPLOYMENT: 9 (002, 011, 013, 014, 017, 020, 022, 024, 025)  
- FIRST_HAND_BENCHMARK: 7 (003, 005, 008, 009, 012, 018, 021)  
- INDEPENDENT_TECHNICAL_ANALYSIS: 5 (002, 004, 010, 019, 021)  
- SECONDARY_REACTION: 4 (006, 007, 026, 027)  
- ADOPTION_SIGNAL: 3 (015, 022, 023)  

Primary coverage-bucket totals (mutually exclusive, sum = 27):

- DeepSeek V4.1 Flash: 7  
- Qwen3.8-Flash-Next: 6  
- Kimi Linear: 2  
- GLM-5.3-Flash: 5  
- Jev: 3  
- Local stack / mechanisms (cross-cutting): 4  

LOW_SIGNAL targets (unchanged):

- Dense independent production failure modes for Jev  
- First-hand SGLang / LMCache / KTransformers configs for the five named models  
- Config-matched multi-model throughput tables on identical hardware  
- Long-running agentic harness failure rates with exact reasoning-budget settings  
- Conditional Memory / Engram practical quality impact beyond vendor claims  

LEDGER_COUNT_CONSISTENCY: PASS

All 27 Observation Records reconcile; all status URLs are unique and direct; account counts, FIRST_HAND totals, reception totals and primary coverage buckets sum exactly to 27; narrative summary counts match the ledgers.

## 14. Research-gap handoff

Downstream should:

1. Verify architecture/parameter/KV/benchmark numbers from primary model cards and technical reports.  
2. Re-measure the cited tok/s figures under controlled identical hardware.  
3. Inspect referenced llama.cpp / vLLM / Unsloth PRs.  
4. Seek additional independent Jev production logs (failure, calibration drift, task classes where LLM still preferred).  
5. Confirm Engram / Conditional-Memory quality and host-memory bandwidth limits experimentally.

No full additional X pass is required for existence and early reception; a narrow follow-up on long-running agentic failure modes and SGLang/KTransformers configs would still add value if those become central to the Special.
