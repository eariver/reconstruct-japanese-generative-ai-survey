# Discovery observations — D05 Decoding acceleration
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r1 | observed: 2026-09-21
# Per-method record rule: distribution preservation, retraining need, acceptance, gain, hw/batch constraints.

## S33 — Fast Inference from Transformers via Speculative Decoding (Leviathan et al.)
- locator: https://arxiv.org/abs/2211.17192
- class: PRIMARY_PAPER | published: 2022-11-28 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: Origin authority (with S34): small draft model proposes tokens, target verifies in parallel;
  LOSSLESS (output distribution preserved), no retraining of target. Draft-acceptance rate governs speedup;
  memory-bandwidth-bound decode is the regime where it wins.

## S34 — Accelerating Large Language Model Decoding with Speculative Sampling (Chen et al.)
- locator: https://arxiv.org/abs/2302.01318
- class: PRIMARY_PAPER | published: 2023-02-02 | retrieval: SUMMARY_CAPTURED
- summary: Independent co-origin of the draft/verify framework with the acceptance-criterion formalism.
  Pair with S33 as joint origin; do not single-source the invention claim.

## S35 — Medusa (Cai et al.)
- locator: https://arxiv.org/abs/2401.10774
- class: PRIMARY_PAPER | published: 2024-01-13 | retrieval: SUMMARY_CAPTURED
- summary: Multiple decoding heads on frozen backbone; tree attention verification. Historically/materially
  useful baseline; non-greedy acceptance relaxation does NOT guarantee losslessness (EAGLE-2 paper's
  explicit contrast) — record the qualification, not just the speedup.

## S36 — EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty (Li et al., ICML'24)
- locator: https://arxiv.org/abs/2401.15077
- class: PRIMARY_PAPER | published: 2024-01-26 | retrieval: SUMMARY_CAPTURED
- summary: Drafts autoregressively at second-to-top feature level (+1-step-ahead tokens); tree-structured
  draft via tree attention; lossless; no target fine-tuning; draft trains on 2–4B tokens (vs 3000B for a
  fresh small draft model); LLaMA2-Chat 70B: 2.7–3.5x latency, ~2x throughput. EAGLE-3 later reports this
  line inspired DeepSeek-V3's MTP pretraining (reverse influence: decoding -> training).

## S37 — EAGLE-2: Faster Inference with Dynamic Draft Trees
- locator: https://arxiv.org/abs/2406.16858
- class: PRIMARY_PAPER | published: 2024-06-13 | retrieval: SUMMARY_CAPTURED
- summary: Context-dependent (not position-only) acceptance -> confidence-driven dynamic trees; 2.5–5x;
  no extra training beyond EAGLE. Documents the acceptance-rate science needed for honest D05 reporting.

## S38 — Better & Faster Large Language Models via Multi-token Prediction (Gloeckle et al.)
- locator: https://arxiv.org/abs/2404.19737
- class: PRIMARY_PAPER | published: 2024-04-18 | retrieval: SUMMARY_CAPTURED
- summary: MTP as TRAINING objective (auxiliary heads, denser signal) distinct from MTP-as-decoding; the
  mechanism DeepSeek-V3/Qwen3.8-Flash-Next/GLM-5.3-Flash reuse at inference. Keep training-benefit and
  decoding-benefit claims separate per instance.

## S39 — vLLM MTP documentation (native multi-token prediction speculative decoding)
- locator: https://docs.vllm.ai/en/latest/features/speculative_decoding/mtp
- class: PRIMARY_DOC | published: 2026 (living doc; captured 2026-09-21) | retrieval: SUMMARY_CAPTURED
- summary: Deployment authority: target-native MTP needs NO separate draft model; GLM-5.3-Flash served with
  DeepSeek-style MTP draft head (num_speculative_tokens 3–5, enforce_eager) per vLLM Ascend tutorial (S52).
  Current-deployment evidence for MTP adoption.

## S40 — DSpark evidence bundle (DeepSeek-V4.1 speculative mechanism)
- locator: https://docs.vllm.ai/en/latest/api/vllm/models/deepseek_v41/
- class: PRIMARY_DOC (code-adjacent) | published: 2026-09 | retrieval: SUMMARY_CAPTURED (code body pending Evidence)
- cross: https://docs.nvidia.com/dynamo/dev/recipes/deepseek-v4-1-flash.md (DSpark block-5 aggregated; refused under disaggregation)
- summary: DSpark = semi-autoregressive draft generation with confidence-scheduled verification (per HF card
  S30); draft weights ship IN the target checkpoint (mtp.*: 3 extra MoE blocks, 14.2B drafter per ezyang
  accounting S77); vLLM carries DSparkDeepseekV4ForCausalLM + name-remap. NO standalone DSpark paper located
  in this pass.
- limitation: Mechanism authority is currently checkpoint-config + runtime-code + card prose. Sol gap-fill:
  confirm DSpark vs MTP-head relationship and acceptance/losslessness status; do NOT assert equivalence.
