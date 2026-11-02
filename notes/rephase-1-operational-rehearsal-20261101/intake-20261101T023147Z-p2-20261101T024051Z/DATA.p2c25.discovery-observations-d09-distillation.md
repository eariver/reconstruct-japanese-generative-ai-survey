# Discovery observations — D09 Distillation, pruning and adaptation efficiency
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r1 | observed: 2026-09-21
# Boundary: explain current usage; NOT a generic fine-tuning tutorial.

## S67 — Distilling the Knowledge in a Neural Network (Hinton et al.)
- locator: https://arxiv.org/abs/1503.02531
- class: PRIMARY_PAPER | published: 2015-03-09 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: Soft-target distillation origin; sufficient history to explain R1-distill usage (S69) and the
  quality/capacity tradeoff frame (student capacity vs teacher coverage).

## S68 — LoRA: Low-Rank Adaptation (Hu et al.)
- locator: https://arxiv.org/abs/2106.09685
- class: PRIMARY_PAPER | published: 2021-06-17 | retrieval: SUMMARY_CAPTURED
- summary: Frozen-base + low-rank adapter = fine-tuning efficiency anchor; pairs with QLoRA (S45) for the
  quantized-adaptation interaction. Capability note: adapter capacity bounds hard-task transfer.

## S69 — DeepSeek-R1: Incentivizing Reasoning Capability via RL (+ R1 distilled models)
- locator: https://arxiv.org/abs/2501.12948
- class: PRIMARY_PAPER (official report) | published: 2025-01-22 | retrieval: SUMMARY_CAPTURED
- summary: R1-Zero large-scale RL -> cold-start -> RL -> distillation into Qwen/Llama dense students.
  Mandatory reasoning-distillation case: shows post-training (not architecture) as an efficiency lever —
  small models inherit reasoning patterns at a fraction of training cost, with documented degradation vs
  teacher on hardest tasks (verify exact deltas at Evidence; do not generalize beyond reported conditions).
