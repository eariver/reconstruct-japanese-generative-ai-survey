# Discovery observations — D03 Conditional computation / Mixture of Experts
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r1 | observed: 2026-09-21
# Lineage rule: trace routing/load/memory/communication mechanisms, not model names alone.

## S10 — Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer (Shazeer et al.)
- locator: https://arxiv.org/abs/1701.06538
- class: PRIMARY_PAPER | published: 2017-01-23 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: Origin authority for learned sparse gating with top-k routing, load-balancing auxiliary loss,
  and the total-vs-compute separation (capacity without proportional FLOPs). All later MoE work branches here.
- tradeoff surface: routing imbalance, communication (all-to-all dispatch/combine), expert memory residency.

## S11 — GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding (Lepikhin et al.)
- locator: https://arxiv.org/abs/2006.16668
- class: PRIMARY_PAPER | published: 2020-06-30 | retrieval: SUMMARY_CAPTURED
- summary: Production-scale MoE with expert parallelism, sharded dispatch, and capacity-factor mechanics;
  establishes the communication/memory-residency problem class for giant sparse models.

## S12 — Switch Transformers (Fedus et al.)
- locator: https://arxiv.org/abs/2101.03961
- class: PRIMARY_PAPER | published: 2021-01-11 | retrieval: SUMMARY_CAPTURED
- summary: Top-1 routing simplification; shows routing-strategy choice (top-1 vs top-k) trades quality
  against communication/compute. Mandatory seed per scope.

## S13 — Mixtral of Experts (Jiang et al.)
- locator: https://arxiv.org/abs/2401.04088
- class: PRIMARY_PAPER (official report) | published: 2024-01-08 | retrieval: SUMMARY_CAPTURED
- summary: 8x7B (46.7B total / ~13B active) open-weight MoE that carried sparse activation into the
  Western open ecosystem; 32K context. Adoption evidence for MoE outside Chinese labs.

## S14 — DeepSeekMoE: Towards the Ultimate Specialist Lexicon (Dai et al.)
- locator: https://arxiv.org/abs/2401.06066
- class: PRIMARY_PAPER | published: 2024-01-11 | retrieval: SUMMARY_CAPTURED
- summary: Fine-grained experts + shared experts + device-limited routing; the routing/shared-expert design
  that DeepSeek-V2/V3 industrialize. Mechanism authority for the DeepSeek MoE branch.

## S15 — DeepSeek-V2: A Strong, Economical, and Efficient MoE Language Model
- locator: https://arxiv.org/abs/2405.04434
- class: PRIMARY_PAPER (official report) | published: 2024-05-07 | retrieval: SUMMARY_CAPTURED
- summary: 236B total / 21B active; MLA + DeepSeekMoE; 128K context. First report to make efficiency a
  first-class architectural claim (also D04 MLA origin for DeepSeek line). Training and serving implications
  in one artifact.

## S16 — Qwen3 Technical Report (Qwen dense/MoE breadth anchor)
- locator: https://arxiv.org/abs/2505.09388
- class: PRIMARY_PAPER (official report) | published: 2025-05-14 | retrieval: SUMMARY_CAPTURED
- summary: Documents the Qwen family breadth strategy (dense + MoE sizes, multilingual/coding/reasoning)
  preceding Qwen3.5–3.8 efficiency generations. Used here for family-lineage adoption evidence, not for
  efficiency numbers.

## S17 — DeepSeek-V4-Flash (284B total / 13B active; hybrid CSA+HCA; mHC; FP4+FP8)
- locator: https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash
- class: PRIMARY_MODEL_CARD | published: 2026-04-23 | retrieval: SUMMARY_CAPTURED (config tensors pending Evidence)
- cross-check: https://lambda.ai/inference-models/deepseek-ai/deepseek-v4-flash (provider mirror, secondary)
- summary: MoE with hybrid Compressed Sparse Attention + Heavily Compressed Attention; Manifold-Constrained
  Hyper-Connections (mHC); Muon pretraining on 32T tokens (per provider page); FP4 experts + FP8 body
  (~146GB native; FP8-only quant ~284GB for H100). 1M native context; MIT license (per provider page).
- efficiency/capability/tradeoff: FP4 halves weight footprint but requires B200-class hardware; sparse
  attention shifts cost to indexer. License/hardware facts need artifact-level verification at Evidence.
- terminology watch: mHC also appears in Qwen (Mega-mHC kernel, ezyang study) and GLM-5.3-Flash materials.
  No cross-lab ancestry claim without authority.
