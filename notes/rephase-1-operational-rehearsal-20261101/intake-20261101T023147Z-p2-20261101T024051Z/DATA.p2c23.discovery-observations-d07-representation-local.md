# Discovery observations — D07 Model representation and local inference
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r1 | observed: 2026-09-21
# Standing question: why can a huge-total / low-active MoE still be undeployable locally?
# (size vs active compute vs memory CAPACITY vs memory BANDWIDTH.)

## S50 — llama.cpp repository (GGML history, GGUF runtime, quantization families, CPU/GPU split)
- locator: https://github.com/ggerganov/llama.cpp
- class: PRIMARY_REPO | published: 2023-03 (ongoing; captured 2026-09-21) | retrieval: LOCATOR_CAPTURED (tree/config pending Evidence)
- summary: Reference implementation for the whole D07 lane: GGML tensor engine history, GGUF loader + mmap,
  k-quant/imatrix families, CPU/GPU layer split, Apple/consumer hardware paths. Adoption authority for
  "open weights actually run locally" claims across all MoE capstones.

## S51 — KTransformers repository (heterogeneous CPU/GPU MoE execution)
- locator: https://github.com/kvcache-ai/ktransformers
- class: PRIMARY_REPO | published: 2024 (ongoing; captured 2026-09-21) | retrieval: LOCATOR_CAPTURED
- summary: Expert-offload / heterogeneous execution for large MoE (DeepSeek-class) on limited VRAM:
  the practical answer to the standing question — active compute is small but ALL experts must be
  RESIDENT-or-prefetchable, so weight CAPACITY (and PCIe/NVLink bandwidth for expert movement) dominates.
  Needs version-specific verification at Evidence (fast-moving repo).

## S52 — vLLM Ascend GLM-5.3-Flash tutorial (single/multi-node deployment + accuracy/perf evaluation)
- locator: https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.3-Flash.html
- class: PRIMARY_DOC | published: 2026-08 | retrieval: SUMMARY_CAPTURED
- summary: 320B/18B served quantized (mxfp8/w8a8) on Atlas 800 nodes; DeepSeek-style MTP speculative config;
  tool-call/reasoning parsers; benchmark hooks. Deployment evidence tying D07 (serving/local) to D05 (MTP)
  and D06 (quant) for one capstone. Ascend-hardware framing is vendor-conditional.
