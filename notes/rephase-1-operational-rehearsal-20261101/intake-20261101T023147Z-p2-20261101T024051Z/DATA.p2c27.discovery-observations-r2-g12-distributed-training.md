# Discovery observations r2 — G12 Distributed training and training-memory systems
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r2 | observed: 2026-09-21
# Required question: which techniques reduce ARITHMETIC vs merely make an impossible job FIT/SCALe?
# Do not call all of these model-efficiency improvements without that distinction.

## S101 — Megatron-LM (tensor model parallelism origin)
- locator: https://arxiv.org/abs/1909.08053
- class: PRIMARY_PAPER | published: 2019-08 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: Intra-layer tensor splitting (column/row-parallel GEMMs, f/g operators); the fit-and-scale
  mechanism for multi-billion dense training. Category: SCALE/PLACE, not arithmetic reduction.
- r1 parent: external:SP-efficient-llm-2026:EFF-D002 (Chinchilla-era training context).

## S102 — GPipe (pipeline parallelism)
- locator: https://arxiv.org/abs/1811.06965
- class: PRIMARY_PAPER | published: 2018-11 | retrieval: SUMMARY_CAPTURED
- summary: Micro-batch pipeline with recomputation; bubble-vs-memory tradeoff origin. SCALE/PLACE.
  Include only as historical necessity for the pipeline-parallelism thread.

## S103 — ZeRO: Memory Optimizations Toward Training Trillion-Parameter Models
- locator: https://arxiv.org/abs/1910.02054
- class: PRIMARY_PAPER | published: 2019-10 | retrieval: SUMMARY_CAPTURED
- summary: Shards optimizer states/gradients/parameters across data-parallel ranks (ZeRO-1/2/3);
  removes memory redundancy without changing arithmetic. Category: FIT (memory), not FLOPs.

## S104 — ZeRO-Offload / ZeRO-Infinity (heterogeneous memory)
- locator: https://arxiv.org/abs/2101.06840
- class: PRIMARY_PAPER | published: 2021-01 | retrieval: SUMMARY_CAPTURED (Infinity: 2104.07857, same entry)
- summary: Offloads optimizer states (Offload) then full model states to CPU/NVMe (Infinity) with
  bandwidth-aware scheduling. Direct ancestor of host-memory offload thinking reused at inference
  (Qwen 51B n-gram tables, S29). Category: FIT via heterogeneous memory; movement cost is the tradeoff.

## S105 — Activation checkpointing / sublinear memory (Chen et al.)
- locator: https://arxiv.org/abs/1604.06174
- class: PRIMARY_PAPER | published: 2016-04 | retrieval: SUMMARY_CAPTURED
- summary: Recompute-vs-store tradeoff origin (sqrt-N segments). Category: memory-for-compute EXCHANGE —
  reduces footprint by SPENDING arithmetic. The one entry that moves the wrong way on FLOPs; record explicitly.

## S106 — FSDP (Fully Sharded Data Parallel)
- locator: https://arxiv.org/abs/2304.11277
- class: PRIMARY_PAPER | published: 2023-04 | retrieval: SUMMARY_CAPTURED
- summary: ZeRO-3-class sharding in PyTorch-native form; the sharded-data-parallel lineage most current
  training stacks actually use. Category: FIT/SCALE.

## S107 — DeepSpeed-Ulysses (sequence/context parallelism)
- locator: https://arxiv.org/abs/2309.14509
- class: PRIMARY_PAPER | published: 2023-09 | retrieval: SUMMARY_CAPTURED
- summary: All-to-all attention-head partitioning across ranks for long sequences; the training-side
  counterpart to inference context-parallel serving. Category: SCALE for long context.

## S108 — Ring Attention (Liu et al.)
- locator: https://arxiv.org/abs/2310.01889
- class: PRIMARY_PAPER | published: 2023-10 | retrieval: SUMMARY_CAPTURED
- summary: Blockwise attention with ring KV exchange; near-unbounded context training. Closes r1 G08
  absentee item. Category: SCALE; per-device memory bounded, total arithmetic unchanged.
