# Discovery observations r3 — G21 Conditional Memory / Lookup Sparsity (mandatory new lane)
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r3 | observed: 2026-09-21
# Four-way distinction (mandatory): MoE expert weights / neural attention-KV memory /
# external retrieval-RAG / STATIC LEARNED LOOKUP (Engram). Do NOT call Engram RAG.

## S143 — Conditional Memory via Scalable Lookup (Engram paper; Cheng et al., DeepSeek-AI + PKU)
- locator: https://arxiv.org/abs/2601.07372
- class: PRIMARY_PAPER | published: 2026-01-12 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: Conditional MEMORY as complement to conditional COMPUTE (MoE): modernized N-gram embeddings
  with O(1) lookup; deterministic addressing -> host-memory prefetch with negligible inference overhead;
  Sparsity Allocation U-shaped law (neural MoE vs static memory); Engram-27B beats iso-param/iso-FLOP MoE
  baselines across knowledge/reasoning/code/math; early layers relieved of static-pattern reconstruction
  (depth preserved for reasoning); long-context training + results sections present.
- required questions: computation-vs-memory tradeoff answered via allocation law; iso-methodology explicit;
  model/runtime tradeoffs (table size vs overhead) to be read at Evidence.

## S144 — deepseek-ai/Engram official implementation
- locator: https://github.com/deepseek-ai/Engram
- class: PRIMARY_REPO (official; README + Engram_paper.pdf + engram_demo_v1.py) | published: 2026-01 (created)
- retrieval: SUMMARY_CAPTURED (demo code body pending Evidence)
- summary: Demo (mocked Attention/MoE/mHC, data-flow focus) + paper PDF + eval figures (scaling law,
  pretraining, long-context, case study). Implementation evidence for deterministic addressing/offload
  claims; production-grade kernel path still to verify at Evidence. Apache-2.0 (repo).

## S145 — Qwen N-gram embedding vs Engram lineage assessment
- locator: https://github.com/QwenLM/Qwen3.8-Flash-Next
- class: PRIMARY_REPO (assessment anchored to official Qwen + Engram authorities) | published: 2026-08
- retrieval: SUMMARY_CAPTURED
- summary: Qwen materials describe their 20M-entry bigram/trigram table + async host-prefetch as an
  internal design (four-aspect upgrade; loss-vs-downstream saturation noted). NO citation of Engram and
  NO derivation statement located in Qwen report/card/blog/README. Temporal order (Engram 2026-01 before
  Qwen3.8-Flash-Next 2026-08) does NOT establish derivation.
- verdict: PARALLEL_OR_UNRESOLVED_LINEAGE. Shared lookup-memory design pressure confirmed; technical
  derivation unestablished. Do not infer ancestry from similarity.

## S146 — kNN-LM (Khandelwal et al.; retrieval-interpolation precedent)
- locator: https://arxiv.org/abs/1911.00172
- class: PRIMARY_PAPER | published: 2019-11 | retrieval: SUMMARY_CAPTURED
- summary: Bounded precedent: nearest-neighbor datastore interpolated with LM at INFERENCE (retrieval over
  explicit corpus, Approximate search, per-token cost). Contrast object: explicit-corpus retrieval with
  query-time search vs Engram's static learned table with O(1) deterministic address. Included ONLY to
  sharpen the lookup-vs-retrieval boundary, not as RAG history.

## S147 — RETRO (Borgeaud et al.; retrieval-architecture precedent)
- locator: https://arxiv.org/abs/2112.04426
- class: PRIMARY_PAPER | published: 2021-12 | retrieval: SUMMARY_CAPTURED
- summary: Chunked cross-attention retrieval architecture (frozen retriever + trained reader).
  Contrast object: retrieval CONDITIONING inside the forward pass vs static lookup memory fused with hidden
  states. Closes the precedent sweep; no further retrieval history (no generic RAG survey).
