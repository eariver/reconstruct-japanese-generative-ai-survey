# Discovery observations — D01 Efficiency fundamentals / bottleneck model
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r1 | observed: 2026-09-21
# Purpose: establish the bottleneck vocabulary (training vs inference, prefill vs decode,
# compute vs memory-bandwidth vs communication, latency vs throughput, total vs active params,
# KV-cache/weight footprints, energy/utilization, token cost vs task cost). No vendor claim is
# treated as independent evidence. Full-body semantic consumption happens at Evidence stage.

## S01 — Scaling Laws for Neural Language Models (Kaplan et al.)
- locator: https://arxiv.org/abs/2001.08361
- class: PRIMARY_PAPER | published: 2020-01-23 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: Power-law scaling of loss in parameters/data/compute; found larger models more sample-efficient.
  Historic anchor for the dense-scaling era this Special contrasts against; later refits (Chinchilla,
  Qwen3.8-Next) revise its allocation conclusions.
- efficiency/capability/tradeoff: Defines the compute-optimal frontier language; does not itself give
  inference-cost guidance. Evidence boundary: source-local claims only.

## S02 — Training Compute-Optimal Large Language Models / Chinchilla (Hoffmann et al.)
- locator: https://arxiv.org/abs/2203.15556
- class: PRIMARY_PAPER | published: 2022-03-29 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: Equal scaling of model size and training tokens (~20 tokens/param); many dense models were
  under-trained. Directly motivates the D02 training-token-reduction thread and later
  architecture-specific refits (e.g. Qwen3.8-Next reports 1/3 tokens, ~1/9 FLOPs vs its 397B-A17B predecessor).
- efficiency/capability/tradeoff: Training-FLOP reduction with capability parity; inference cost untouched
  by itself. Vendor refit claims (Qwen) are vendor claims until reproduced.

## S03 — Orca: A Distributed Serving System for Transformer-Based Generative Models (Yu et al., OSDI'22)
- locator: https://www.usenix.org/conference/osdi22/presentation/yu
- class: PRIMARY_PAPER | published: 2022-07 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: Origin authority for iteration-level (continuous) scheduling: distinguishes the parallel prefill
  phase from incremental decode, batches at iteration granularity instead of request granularity.
  Mandatory conceptual anchor for D01 prefill/decode split and all of D08 serving.
- efficiency/capability/tradeoff: Throughput via reduced idle time; latency/SLO interaction is the tradeoff
  surface carried into Splitwise/DistServe/disaggregation work.

## S04 — NVIDIA Dynamo DeepSeek-V4.1-Flash deployment recipe (aggregated vs disaggregated topologies)
- locator: https://docs.nvidia.com/dynamo/dev/recipes/deepseek-v4-1-flash.md
- class: PRIMARY_DOC (vendor runtime doc) | published: 2026-09 | retrieval: SUMMARY_CAPTURED
- summary: Concrete 2026 instance of D01 distinctions: FP8 dense + FP4 MoE experts + FP8 KV cache;
  8xGB200 aggregated (TP4/EP4, DSpark block-5 speculation) vs 4+4 GB200 disaggregated prefill/decode
  (no speculation; SGLang refuses DSpark under disaggregation); Mooncake KV transfer over TCP vs RDMA;
  KV-aware routing; 1M context. Shows decoding-acceleration gains are topology-conditional.
- efficiency/capability/tradeoff: Prefill/decode disaggregation trades KV-transfer cost for role
  specialization; speculation disabled in one topology. Vendor doc: deployment evidence, not capability proof.
- limitation: NVIDIA hardware/software framing; independent reproduction pending Sol gap-fill.
