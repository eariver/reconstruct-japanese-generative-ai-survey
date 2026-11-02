# Discovery observations r2 — G13 KV-cache management as a separate lineage
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r2 | observed: 2026-09-21
# Five-way separation: (1) architectural KV reduction [r1 D04] / (2) KV quantization [r1 D06] /
# (3) eviction-compression [here] / (4) prefix reuse [here] / (5) offload-disaggregation [here + S61].

## S109 — H2O / Heavy-Hitter Oracle (Zhang et al.)
- locator: https://arxiv.org/abs/2306.14048
- class: PRIMARY_PAPER | published: 2023-06 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: Eviction policy keeping heavy-hitter + recent tokens; near-full-attention quality at 20% budget
  (vendor-reported curve; verify at Evidence). Category (3) eviction. Distinguish from attention-sink
  mechanics (S110): H2O is score-driven, StreamingLLM is positional.

## S110 — StreamingLLM / attention sinks (Xiao et al.)
- locator: https://arxiv.org/abs/2309.17453
- class: PRIMARY_PAPER | published: 2023-09 | retrieval: SUMMARY_CAPTURED
- summary: Keeps initial sink tokens + sliding window; enables infinite-length streaming decode without
  fine-tuning. Category (3) with positional policy; the sink phenomenon constrains ALL eviction claims.

## S111 — SnapKV (Li et al.)
- locator: https://arxiv.org/abs/2404.14469
- class: PRIMARY_PAPER | published: 2024-04 | retrieval: SUMMARY_CAPTURED
- summary: Prompt-phase observation-window voting for important KV positions, then compressed decode.
  Category (3); prompt-aware vs decode-eviction distinction matters for prefill-heavy agent workloads.

## S112 — PyramidKV (Cai et al.)
- locator: https://arxiv.org/abs/2406.02032
- class: PRIMARY_PAPER | published: 2024-06 | retrieval: SUMMARY_CAPTURED
- summary: Layer-wise pyramidal budget allocation (lower layers keep more); stacking with S109–S111 class
  methods. Category (3); layer-heterogeneity evidence relevant to CSA2 cross-layer sharing (S30).

## S113 — vLLM Automatic Prefix Caching
- locator: https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/
- class: PRIMARY_DOC | published: null (living docs) | retrieval: LOCATOR_CAPTURED (doc body pending Evidence)
- summary: Block-hash prefix reuse in vLLM; category (4). Granularity contrast with SGLang radix tree
  (S54 doctrinal note): block (default 32) vs token/page granularity is the one material difference.

## S114 — LMCache (external KV-cache layer: reuse, offload, disaggregation transport)
- locator: https://github.com/LMCache/LMCache
- class: PRIMARY_REPO | published: 2024-05 (created; ongoing) | retrieval: SUMMARY_CAPTURED (code pending Evidence)
- summary: Engine-independent daemon; persistent tiered offload (CPU/SSD/Redis/Mooncake/S3/NIXL);
  NON-prefix reuse via CacheBlend recompute; PD disaggregation over NIXL; Mooncake as storage backend;
  NVIDIA Dynamo integration. Categories (4)+(5) in one artifact; Mooncake relationship: backend, not rival.
- r1 parent: external:SP-efficient-llm-2026:EFF-D061 (Mooncake paper).
