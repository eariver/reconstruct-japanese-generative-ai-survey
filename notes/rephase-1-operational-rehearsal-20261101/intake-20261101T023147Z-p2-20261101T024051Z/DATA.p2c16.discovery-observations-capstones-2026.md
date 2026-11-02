# Discovery observations — 2026 capstone model case studies (cross-lane fact bundles)
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r1 | observed: 2026-09-21
# Each capstone needs: spec/attention/precision/decoding/serving/economics/methodology/independent evidence.
# "Secondary modern cases" are materiality watches, not selections.

## S75 — DeepSeek-V4-Flash provider page (284B/13B, mHC, Muon 32T, FP4+FP8, throughput)
- locator: https://lambda.ai/inference-models/deepseek-ai/deepseek-v4-flash
- class: SECONDARY_REFERENCE (provider page relaying vendor specs) | published: 2026-04-27 | retrieval: SUMMARY_CAPTURED
- summary: 284B/13B; hybrid CSA+HCA; mHC; Muon on 32T tokens; FP4 experts + FP8 body; SGLang/vLLM deploy
  (TP4 + expert-parallel over 8xB200; FP8-quant path for Hopper); 1222 tok/s output / 11000 total (SGLang)
  and 1469/13217 (vLLM) provider-measured; reasoning modes Non-think/Think High/Think Max.
- limitation: Provider-measured throughput (hardware/batch undisclosed in capture); rebind at Evidence.

## S76 — DeepInfra DeepSeek-V4-Flash API pricing ($0.09/$0.18/$0.018 per 1M)
- locator: https://deepinfra.com/deepseek-ai/DeepSeek-V4-Flash/api
- class: SECONDARY_REFERENCE (price snapshot, NOT official DeepSeek price) | published: 2026-09-20 | retrieval: SUMMARY_CAPTURED
- summary: Standard tier input/output/cached-input economics sample for API-economics lane. Distinguish
  provider list price from DeepSeek official API pricing (S31 peak/off-peak) at Evidence.

## S77 — Infra-oriented DeepSeek-V4.1-Flash architecture study (parameter accounting)
- locator: https://deepseek-v3.ezyang.com/studies/dsv41-flash.html
- class: SECONDARY_TECHNICAL (independent accounting from checkpoint tensors) | published: 2026-09 (draft, unlisted)
- retrieval: SUMMARY_CAPTURED
- summary: Backbone exactly 551,566,180,464 params (552B) + 196,928,504,320 Engram (196B) from 48-shard headers
  cross-checked vs config.json/model.py; 890 B/token global-KV derivation (2.5 entries x (288+68));
  SWA caches bounded/non-persisted; 14.2B DSpark drafter (mtp.*); vision tower 485M excluded from backbone count.
- limitation (load-bearing): Prose/diagram AI-drafted (Fable/Claude), NO human edit pass yet; author states
  not part of published series. Use ONLY as a gap-fill lead (tensor-shape claims re-verify from checkpoint
  at Evidence), never as mechanism authority.

## S78 — vLLM deepseek_v41 model code docs (FlashMLA sparse backend, FP8 dispatch, DSpark class)
- locator: https://docs.vllm.ai/en/latest/api/vllm/models/deepseek_v41/
- class: PRIMARY_DOC (runtime implementation) | published: 2026-09 (living docs) | retrieval: SUMMARY_CAPTURED (code body pending Evidence)
- summary: Multimodal entry point; FlashMLA sparse backend + metadata builders; expert_dtype-aware FP8 config
  (fp4 MXFP4 ue8m0 vs fp8 block); DSparkDeepseekV4ForCausalLM with mtp.* name-remap; draft layers reuse
  engine attention backend. Strongest current-deployment evidence for V4.1 serving support.

## S79 — Qwen3.8-Flash-Next launch analysis (llm-stats: open weights, self-reported scores, product split)
- locator: https://llm-stats.com/blog/research/qwen3.8-flash-next-launch
- class: SECONDARY_TECHNICAL | published: 2026-08-26 | retrieval: SUMMARY_CAPTURED
- summary: Open-weight Qwen4-architecture preview (NOT the Cloud Flash API SKU); 125B/6B + 51B n-gram + 4B MTP;
  262K native (1M on API SKU); self-reported DeepSWE 58.7 (+4.3 vs V4-Flash-0731), SWE-Pro 62.5 (+6.5),
  Toolathlon 73.5, LCB-v6 91.9, GPQA-D 91.7, OSWorld-2.0 binary 19.4 (coin-flip caveat), MathVision 90.6/95.7 w/CI.
- limitation: Explicitly self-reported/HF-README-derived, NOT independently verified; product-split warning
  (weights vs hosted API) is itself valuable scope hygiene for the issue.

## S80 — NVIDIA technical blog: Qwen3.8-Flash-Next on GB300 NVL72 (QSA speedups, Day-0 runtimes)
- locator: https://developer.nvidia.com/blog/experiment-with-qwen3-8-flash-next-on-nvidia-gb300-nvl72-for-agentic-coding
- class: SECONDARY_TECHNICAL (vendor benchmark + enablement) | published: 2026-08-26 | retrieval: SUMMARY_CAPTURED
- summary: QSA: up to 7.6x prefill / 4.9x decode vs full attention; 8.6x prefill throughput vs Qwen3.7-Plus
  @1M ctx + 90% prefix-cache hit; Day-0 SGLang/vLLM/TRT-LLM + NeMo recipes. Hardware/batch/cache-conditioned
  numbers — exemplary of why efficiency claims must carry conditions.

## S81 — Qwen3.8-Flash-Next official blog (GDN+QSA, Gated Residual, n-gram, Muon, refit)
- locator: https://qwen.ai/blog?id=qwen3.8-flash-next
- class: PRIMARY_ANNOUNCEMENT | published: 2026-08 (exact day unverified) | retrieval: SUMMARY_CAPTURED
- summary: Four-aspect upgrade (attention/residual/embedding/optimization); micro-block QSA with compressed
  lightweight indexer; per-layer independent compression (vs cross-layer index sharing); Muon assignment +
  fused-param splitting; scaling-law refit; HF + ModelScope weights. Pairs with S08 (report) and S29 (card).

## S82 — GLM-5.3-Flash launch analysis (320B/18B, pricing, stealth test, comparisons)
- locator: https://llm-stats.com/blog/research/glm-5.3-flash-launch
- class: SECONDARY_TECHNICAL | published: 2026-08-26 | retrieval: SUMMARY_CAPTURED
- summary: First natively multimodal GLM-5 (text/image/video); 320B/18B, 45 layers, 1M ctx, MIT weights;
  stealth-tested as ox-alpha; list $0.15/$0.03/$0.50 per 1M (50% promo to 2026-09-09 — clock, not rate);
  thinking always-on; self-reported DeepSWE 63.4 (+17.2 vs 5.2), AutomationBench 48.8 (+22.6); vs Opus 4.8
  near on agents, loses NL2Repo 56.3 vs 69.7; distinct from text-only glm-5.3 ($1.40/$4.40).
- limitation: All comparisons vendor numbers; promo/time-bound pricing must not be quoted as steady-state.

## S83 — HF transformers GLM5-next doc (hybrid sparse+linear, mHC, 30T corpus, no-MTP-layer impl note)
- locator: https://raw.githubusercontent.com/huggingface/transformers/main/docs/source/en/model_doc/glm5_next.md
- class: PRIMARY_DOC | published: 2026-08-26 | retrieval: SUMMARY_CAPTURED
- summary: 320B/18B at 1/10th price claim; ~3.0x less attention compute, ~4.4x smaller KV vs GLM-5.3 (vendor);
  IndexPool + mHC; 30T multimodal pretrain; transformers impl EXCLUDES MTP layer (deployment-relevant
  asymmetry vs vLLM MTP path S52). reasoning_effort (low/high/max) control.

## S84 — GLM-5.3-Flash LM Studio page (IndexPool mechanism gloss, forced thinking, benchmark table)
- locator: https://lmstudio.ai/models/glm-5.3-flash
- class: SECONDARY_REFERENCE | published: 2026-08 | retrieval: SUMMARY_CAPTURED
- summary: IndexPool = indexer-key compression for long-context serving cost; linear-local + sparse-retrieval
  division of labor; benchmark table (Terminal-Bench 2.1 84.3, DeepSWE 63.4, Toolathlon 78.4, AutomationBench
  48.8, Agents' Last Exam 26.3, OfficeQA Pro 62.4, BabyVision 53.4) explicitly vendor-reported with
  harness-variance warning. Local-deployment framing (LM Studio Cloud/Bionic, 1M ctx config).

## S85 — NVIDIA NIM GLM-5.3-Flash card (hybrid KDA + sparse MLA, FP8, release 2026-08-25)
- locator: https://build.nvidia.com/z-ai/glm-5-3-flash
- class: SECONDARY_REFERENCE | published: 2026-09-15 | retrieval: SUMMARY_CAPTURED
- summary: Describes hybrid "KDA and sparse MLA" attention + native FP8 + reasoning/tool-calling; HF release
  2026-08-25. NOTE: "KDA" label here collides with Kimi Delta Attention (S27) — terminology collision to
  resolve at Evidence (vendor shorthand vs shared mechanism; NO ancestry claim).

## S86 — MiniMax-M2.x materiality watch (secondary modern case)
- locator: https://huggingface.co/MiniMaxAI
- class: SECONDARY_REFERENCE (org page; model-level mechanism unconfirmed this pass) | published: null
- retrieval: LOCATOR_ONLY
- summary: Investigated for materiality per scope; no materially distinct efficiency mechanism confirmed in
  this Discovery pass. Sol-directed gap-fill decides pursue vs park. Nationality is not a criterion.

## S87 — gpt-oss open-weight models (secondary modern case)
- locator: https://openai.com/index/introducing-gpt-oss/
- class: PRIMARY_ANNOUNCEMENT | published: 2025-08-05 | retrieval: LOCATOR_ONLY (body pending gap-fill)
- summary: OpenAI open-weight release (gpt-oss-120b/20b, MoE, Apache 2.0 per launch coverage; verify license
  at Evidence). Materiality question for the issue: what distinct efficiency mechanism, if any, does it
  contribute vs the MoE/quantization/serving lanes above. Sol-directed gap-fill.
