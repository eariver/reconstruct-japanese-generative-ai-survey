# Discovery observations — D08 Inference kernels and serving systems
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r1 | observed: 2026-09-21
# Thesis: architecture alone does not determine cost or throughput; the serving stack is mandatory.

## S53 — Efficient Memory Management for LLM Serving with PagedAttention / vLLM (Kwon et al., SOSP'23)
- locator: https://arxiv.org/abs/2309.06180
- class: PRIMARY_PAPER | published: 2023-09-12 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: Non-contiguous paged KV blocks kill fragmentation waste; continuous batching (Orca lineage S03);
  prefix sharing hooks. The serving-system origin for the KV-cache-aware era. Chunked-prefill refinements
  arrive via SARATHI (S62).

## S54 — SGLang + RadixAttention (fast serving framework; radix-tree prefix reuse)
- locator: https://github.com/sgl-project/sglang
- class: PRIMARY_REPO | published: 2024 (ongoing; captured 2026-09-21) | retrieval: LOCATOR_CAPTURED
- doctrinal note: RadixAttention = radix TREE deciding WHICH blocks share + ordinary paged attention reading
  shared blocks; token-granular (page_size=1) vs vLLM block-hash granularity is the one material difference
  (per third-party parity analysis captured in pass; verify at Evidence, do not cite as primary).
- summary: Qwen3.8-Flash-Next Day-0 support (S80) and V4.1-Flash Dynamo recipes (S63) both route through
  SGLang — current-deployment evidence for radix prefix reuse on 2026 capstones.

## S55 — SGLang paper: Efficient Execution of Structured Language Model Programs
- locator: https://arxiv.org/abs/2312.07104
- class: PRIMARY_PAPER | published: 2023-12-18 | retrieval: SUMMARY_CAPTURED
- summary: RadixAttention + compressed FSM execution for multi-call programs; the "serving waste" beyond
  single-request batching (shared prefixes across agentic rollouts) — directly relevant to agent-cost
  arguments in V4.1 materials (cache-hit share of agent cost).

## S56 — FlashMLA repository (DeepSeek)
- locator: https://github.com/deepseek-ai/FlashMLA
- class: PRIMARY_REPO | published: 2025-02 (captured 2026-09-21) | retrieval: LOCATOR_CAPTURED
- summary: MLA-optimized decode kernel (paged, low-rank-aware); the kernel half of the MLA efficiency story
  (architecture S15 + kernel here + ETAP S57). vLLM V4.1 carries a FlashMLA sparse backend (S78).

## S57 — FlashMLA-ETAP (MLA inference on mid-tier H20)
- locator: https://arxiv.org/abs/2506.01969
- class: PRIMARY_PAPER | published: 2025-06-19 | retrieval: SUMMARY_CAPTURED
- summary: 2.78x over FlashMLA @64K/bs16; 5.24x/4.94x over FA3/FlashInfer; 15.2x lower RMSE than FA3.
  Independent-systems evidence class: efficiency claims with numerical-stability accounting — the reporting
  standard D08 items should be held to.

## S58 — TensorRT-LLM repository (NVIDIA)
- locator: https://github.com/NVIDIA/TensorRT-LLM
- class: PRIMARY_REPO | published: 2023 (ongoing; captured 2026-09-21) | retrieval: LOCATOR_CAPTURED
- summary: Production kernel/compiler stack with Day-0 Qwen3.8-Flash-Next support (S80). Material-where-adopted
  per scope; Evidence to bind exact version/precision paths per capstone.

## S59 — Splitwise (Patel et al.)
- locator: https://arxiv.org/abs/2311.18677
- class: PRIMARY_PAPER | published: 2023-11-29 | retrieval: SUMMARY_CAPTURED
- summary: Prefill/decode disaggregation origin: split phases onto heterogeneous pools, trade KV transfer for
  specialization. Direct ancestor of the S63 disaggregated topology (4+4 GB200, Mooncake KV path).

## S60 — DistServe (Zhong et al., OSDI'24)
- locator: https://arxiv.org/abs/2401.09670
- class: PRIMARY_PAPER | published: 2024-01-18 | retrieval: SUMMARY_CAPTURED
- summary: Disaggregated prefill/decode with SLO-aware placement; the scheduler/SLO-tradeoff authority for D08.

## S61 — Mooncake (Qin et al.)
- locator: https://arxiv.org/abs/2411.01181
- class: PRIMARY_PAPER | published: 2024-11-05 | retrieval: SUMMARY_CAPTURED
- summary: Disaggregated KV-cache-centric store (CPU/DRAM/SSD pooling, RDMA); the mechanism behind S63's
  Mooncake TCP/RDMA pin and V4.1's SSD-cache economics (1/8 SSD claim S31 needs this context to be readable).

## S62 — SARATHI (Agrawal et al.; chunked prefill)
- locator: https://arxiv.org/abs/2308.16315
- class: PRIMARY_PAPER | published: 2023-08-30 | retrieval: SUMMARY_CAPTURED
- summary: Decode-creep-free chunked prefill by piggybacking decode with prefill chunks; the scheduler
  refinement between Orca (S03) and disaggregation (S59/S60). Open-world addition from the serving sweep.

## S63 — NVIDIA Dynamo DeepSeek-V4.1-Flash recipe (already captured as S04; D08 reading)
- locator: https://docs.nvidia.com/dynamo/dev/recipes/deepseek-v4-1-flash.md
- class: PRIMARY_DOC | published: 2026-09 | retrieval: SUMMARY_CAPTURED
- summary (serving lens): Aggregated (speculation ON) vs disaggregated (speculation OFF) is a clean
  scheduler/SLO experiment on one model; KV-aware routing, TP4/EP4, Mooncake transport pins. Binds D04
  (CED/CSA2), D05 (DSpark), D06 (FP8/FP4), D08 (topology) on a single 2026 artifact.

## S64 — DeepEP repository (DeepSeek expert-parallel communication library)
- locator: https://github.com/deepseek-ai/DeepEP
- class: PRIMARY_REPO | published: 2025-02 (captured 2026-09-21) | retrieval: LOCATOR_CAPTURED
- summary: MoE dispatch/combine at scale (NVLink/RDMA, FP8-aware); the communication half of D03's
  expert-memory-residency story. Open-world addition: efficiency requires the comm library, not just routing math.

## S65 — DeepGEMM repository (DeepSeek FP8 GEMM library)
- locator: https://github.com/deepseek-ai/DeepGEMM
- class: PRIMARY_REPO | published: 2025-02 (captured 2026-09-21) | retrieval: LOCATOR_CAPTURED
- summary: Fine-grained FP8 matmul supporting V3-class training/inference; the kernel half of D02's FP8 story.
  Open-world addition from the kernel sweep.

## S66 — FlashInfer repository (AI kernels for LLM serving)
- locator: https://github.com/flashinfer-ai/FlashInfer
- class: PRIMARY_REPO | published: 2024 (ongoing; captured 2026-09-21) | retrieval: LOCATOR_CAPTURED
- summary: Shared kernel substrate (paged/MLA/sparse/speculative paths) underneath vLLM/SGLang-class servers;
  needed so "kernel support" claims for capstones (QSA kernels, KDA kernel, FlashMLA sparse) resolve to
  concrete artifacts at Evidence.
