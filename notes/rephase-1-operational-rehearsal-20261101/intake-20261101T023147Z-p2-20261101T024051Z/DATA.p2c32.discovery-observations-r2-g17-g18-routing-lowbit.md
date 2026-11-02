# Discovery observations r2 — G17 MoE routing completeness (bounded) + G18 low-bit completeness
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r2 | observed: 2026-09-21
# Rule: only mechanisms clarifying present-day MoE design; no router catalogue. G18: Discovery expansion,
# not inclusion commitment. Native-low-bit-training vs PTQ separation maintained.

## S133 — Expert Choice Routing (Zhou et al.)
- locator: https://arxiv.org/abs/2202.09368
- class: PRIMARY_PAPER | published: 2022-02 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: Inverted assignment (experts choose tokens) with capacity guarantees and inherent balance;
  contrasts token-choice top-k (S10–S12) and frames aux-loss-free designs (V3 S06) as the third point.
  Closes r1 G08 absentee item at Discovery level; adoption-in-2026-models unverified (Sol materiality).

## S134 — MegaBlocks (Gale et al.; MoE compute substrate)
- locator: https://arxiv.org/abs/2211.15841
- class: PRIMARY_PAPER | published: 2022-11 | retrieval: SUMMARY_CAPTURED
- summary: Block-sparse MoE GEMMs turning routing sparsity into wall-clock wins; the compute twin to
  DeepEP's communication twin (S64). Present-day relevance: FP8/blocked MoE kernels in 2026 serving stacks.
- r1 parent: external:SP-efficient-llm-2026:EFF-D064.

## S135 — BitNet b1.58 (Wang et al.; native ternary lineage)
- locator: https://arxiv.org/abs/2402.17764
- class: PRIMARY_PAPER | published: 2024-02 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: 1.58-bit (ternary {-1,0,1}) matched-full-precision claim at 3B scale; BitNet (S47) lineage step.
  Industrial deployment beyond research line still open (extends r1 G08 item, still unresolved).

## S136 — OCP Microscaling (MX) Specification v1.0 (MXFP8/6/4, MXINT8)
- locator: https://www.opencompute.org/documents/ocp-microscaling-formats-mx-v1-0-spec-final-pdf
- class: PRIMARY_SPEC | published: 2023-09 | retrieval: SUMMARY_CAPTURED (spec body pending Evidence)
- summary: Block-32 + E8M0 shared-scale chassis; MXFP4 = E2M1/4.25 effective bits. THE format authority
  behind S49's MXFP4-ue8m0 vLLM dispatch and V4-line FP4 claims. Training-vs-inference applicability and
  accumulation-precision caveats live here; Evidence must read them before repeating vendor FP4 claims.

## S137 — Microscaling Data Formats for Deep Learning (Rouhani et al.)
- locator: https://arxiv.org/abs/2310.10537
- class: PRIMARY_PAPER | published: 2023-10 | retrieval: SUMMARY_CAPTURED
- summary: MX paper counterpart: conversion recipes, dot-product semantics, training/inference coverage.
  Native-low-bit-training evidence class (vs PTQ S42–S44): conversion is defined, not fitted post-hoc.
