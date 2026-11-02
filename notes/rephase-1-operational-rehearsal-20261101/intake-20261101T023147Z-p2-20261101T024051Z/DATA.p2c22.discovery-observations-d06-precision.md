# Discovery observations — D06 Precision, quantization and compression
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r1 | observed: 2026-09-21
# Separation rule: PTQ vs QAT/native-low-bit; weight-only vs weight+activation; KV quant; optimizer precision;
# file/storage encoding. GGUF is a FORMAT, never a quantization algorithm.

## S41 — LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale (Dettmers et al.)
- locator: https://arxiv.org/abs/2208.07339
- class: PRIMARY_PAPER | published: 2022-08-15 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: Outlier-aware mixed-precision decomposition enabling 8-bit inference of 100B+ models on
  consumer-class memory. Origin of the outlier problem framing that SmoothQuant/AWQ later attack differently.

## S42 — GPTQ (Frantar et al.)
- locator: https://arxiv.org/abs/2210.17323
- class: PRIMARY_PAPER | published: 2022-10-04 | retrieval: SUMMARY_CAPTURED
- summary: One-shot weight-only PTQ via approximate second-order (OBQ lineage); 3–4 bit weights with small
  perplexity cost. Weight-only => memory-capacity win, limited bandwidth/compute win without kernel support.

## S43 — SmoothQuant (Xiao et al.)
- locator: https://arxiv.org/abs/2211.10438
- class: PRIMARY_PAPER | published: 2022-11-08 | retrieval: SUMMARY_CAPTURED
- summary: Migrates activation difficulty to weights (per-channel scaling) enabling W8A8. Weight+activation
  claim class; distinct failure mode from weight-only methods.

## S44 — AWQ: Activation-aware Weight Quantization (Lin et al.)
- locator: https://arxiv.org/abs/2306.00978
- class: PRIMARY_PAPER | published: 2023-06-01 | retrieval: SUMMARY_CAPTURED
- summary: Protects ~1% salient weights (activation-magnitude guided); strong 4-bit weight-only results with
  tiny calibration sets. Salient-weight framing connects to importance-matrix/mixed-quant practice in
  llama.cpp families (S50).

## S45 — QLoRA (Dettmers et al.)
- locator: https://arxiv.org/abs/2305.14314
- class: PRIMARY_PAPER | published: 2023-05-23 | retrieval: SUMMARY_CAPTURED
- summary: 4-bit frozen base + LoRA adapters; fine-tuning efficiency anchor shared with D09. Quantization +
  adaptation interaction in one artifact.

## S46 — SparseGPT (Frantar & Alistarh)
- locator: https://arxiv.org/abs/2301.00774
- class: PRIMARY_PAPER | published: 2023-01-03 | retrieval: SUMMARY_CAPTURED
- summary: One-shot pruning to 50–60% sparsity via the same OBS solver family as GPTQ; pruning+retraining
  examples for D09 must show the retraining half, which this paper bounds.

## S47 — BitNet: Scaling 1-bit Transformers (Wang et al.)
- locator: https://arxiv.org/abs/2310.11453
- class: PRIMARY_PAPER | published: 2023-10-17 | retrieval: SUMMARY_CAPTURED
- summary: Native 1-bit (BitLinear) training direction; energy/latency argument for native low-bit vs PTQ.
  Industrial-adoption evidence beyond Microsoft research line is a Sol gap-fill item (do not over-claim).

## S48 — GGUF specification (ggml project)
- locator: https://github.com/ggerganov/ggml/blob/master/docs/gguf.md
- class: PRIMARY_SPEC | published: 2023-08 (spec versioned in-repo; captured 2026-09-21) | retrieval: LOCATOR_CAPTURED (spec body pending Evidence)
- summary: File format + tensor layout + metadata + mmap alignment contract. Anti-thinness binding: GGUF
  names a CONTAINER; the quantization ALGORITHMS are the llama.cpp families (k-quants, imatrix) layered on it.

## S49 — MXFP4 / FP4-expert deployment evidence (V4 line + vLLM dispatch)
- locator: https://docs.vllm.ai/en/latest/api/vllm/models/deepseek_v41/
- class: PRIMARY_DOC | published: 2026-09 | retrieval: SUMMARY_CAPTURED
- cross: S17 (V4-Flash FP4 experts/FP8 body), S30 (V4.1 FP4 main KV E2M1), S63 (Dynamo FP8-dense/FP4-expert/FP8-KV)
- summary: vLLM dispatches MoE linear scales by expert_dtype (fp4 MXFP4 ue8m0 vs fp8 block, float32 scales);
  missing dtype defaults fp4. Evidence that FP4/MXFP4 moved from paper to serving-critical path in 2026,
  conditioned on B200-class hardware (S17) — the hardware-conditionality question answered for one instance.
