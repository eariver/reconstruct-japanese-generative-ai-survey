# Discovery observations — D02 Scaling and training efficiency
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r1 | observed: 2026-09-21

## S05 — FP8 Formats for Deep Learning (Micikevicius et al.)
- locator: https://arxiv.org/abs/2206.06277
- class: PRIMARY_PAPER | published: 2022-06-15 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: FP8 format/algorithm origin for deep-learning training and inference; establishes the
  mixed-precision lineage (FP8 training) that DeepSeek-V3 later industrializes and V4.x extends to FP4 experts.
- efficiency/capability/tradeoff: Memory/throughput vs numerical-stability control; optimizer-state and
  scaling-bias handling are the documented costs.

## S06 — DeepSeek-V3 Technical Report (FP8 training at scale; MTP pretraining objective)
- locator: https://arxiv.org/abs/2412.19437
- class: PRIMARY_PAPER (official technical report) | published: 2024-12-27 | retrieval: SUMMARY_CAPTURED
- summary: 671B MoE trained with FP8 mixed precision at scale; introduces Multi-Token Prediction as a
  pretraining objective (densifies training signal) whose by-product MTP modules later serve speculative
  decoding (EAGLE-3 lineage explicitly cites this). MLA + DeepSeekMoE + auxiliary-loss-free load balancing.
- efficiency/capability/tradeoff: Reported training-cost reduction with frontier capability; training recipe
  details are vendor-reported. MTP blurs training-efficiency vs decoding-acceleration — track both lanes.

## S07 — Muon optimizer (Keller Jordan et al., reference implementation)
- locator: https://github.com/KellerJordan/Muon
- class: PRIMARY_REPO | published: 2024 (ongoing) | retrieval: LOCATOR_CAPTURED (code body pending Evidence)
- summary: Orthogonalized-gradient optimizer (Newton-Schulz) adopted in Qwen3.8-Flash-Next (2-D linear-map
  weights on Muon; embeddings/head/router/low-rank GR projections stay on AdamW) and reported for
  DeepSeek-V4-Flash pretraining (32T tokens per provider page). Qwen reports upward-shifted optimal LR/batch,
  no batch-size warmup, improved stress-test stability.
- efficiency/capability/tradeoff: Convergence speed/stability vs per-step orthogonalization cost and the
  Muon/AdamW partition design problem. Optimizer-efficiency claims need controlled ablations (Qwen report
  provides some; verify at Evidence).

## S08 — On the Design of Qwen3.8-Next Architecture (Qwen3.8-Flash-Next technical report)
- locator: https://arxiv.org/abs/2608.30320
- class: PRIMARY_PAPER (official technical report) | published: 2026-08-31 | retrieval: SUMMARY_CAPTURED
- summary: 125B total / 6B active + 51B host-offloaded n-gram tables; GDN/QSA hybrid; Gated Residual;
  Muon+AdamW recipe with scaling-law refit. Reports: 8/14 pretraining benchmarks lead the 397B-A17B
  predecessor (rest within 2.6 pts) at 1/3 active params, 1/3 tokens, ~1/9 FLOPs; n-gram vocab lowers loss
  monotonically while downstream saturates (loss != capability warning).
- efficiency/capability/tradeoff: All headline ratios are vendor self-reports (as-of 2026-08-31); needs
  independent reproduction and harness-normalized comparison at Evidence. Mandatory D02 anchor.

## S09 — Qwen3-Next: Towards Ultimate Training & Inference Efficiency (Qwen blog)
- locator: https://qwen.ai/blog?from=research.latest-advancements-list&id=4074cca80393150c248e508aa62983f9cb7d27cd
- class: PRIMARY_ANNOUNCEMENT | published: 2026 (exact date unverified; record as 2026) | retrieval: SUMMARY_CAPTURED
- summary: Claims GDN stronger in-context learning than SWA/Mamba2; 3:1 GDN:attention hybrid beats monolithic
  architectures on both quality and cost. Ancestor statement for the Qwen3.5→3.8 hybrid lineage that
  Qwen3.8-Flash-Next reworks into GDN+QSA.
- efficiency/capability/tradeoff: Vendor claim; ablation details live in the technical report (S08).
