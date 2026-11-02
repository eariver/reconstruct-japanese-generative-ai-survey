# Discovery observations r3 — D09 bounded depth check (final negative-space closure)
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r3 | observed: 2026-09-21
# Question: does a reader-facing LLM-efficiency technical history materially need more than
# Hinton-distill + LoRA/QLoRA + R1-distills + SparseGPT (r1 S67/S68/S69/S45/S46)?

## S159 — DistilBERT (Sanh et al.; historical LM-distillation bridge)
- locator: https://arxiv.org/abs/1910.01108
- class: PRIMARY_PAPER | published: 2019-10 | retrieval: SUMMARY_CAPTURED
- summary: 40%-smaller 97%-capability encoder distillation; the historical bridge showing distillation
  predates the LLM era. Verdict: PARK_WITH_REASON — encoder-era classification transfer is not on the
  present thesis path (decoder reasoning-distillation is, covered by S69).

## S160 — MiniLM (Wang et al.; deep self-attention distillation)
- locator: https://arxiv.org/abs/2002.10957
- class: PRIMARY_PAPER | published: 2020-02 | retrieval: SUMMARY_CAPTURED
- summary: Attention-map + value-relation distillation; last materially distinct pre-LLM technique.
  Verdict: PARK_WITH_REASON (same reason as S159). TinyBERT deliberately not separately collected
  (same bridge class; Sol may substitute).

## S161 — Wanda (Sun et al.; pruning by weights × activations)
- locator: https://arxiv.org/abs/2306.11695
- class: PRIMARY_PAPER | published: 2023-06 | retrieval: SUMMARY_CAPTURED
- summary: Training-free magnitude×activation pruning metric; no weight update, no retraining.
  Structured-pruning-beyond-SparseGPT question: Wanda is a METRIC, not a full pruning+retraining pipeline;
  modern LLM structured-pruning-with-recovery evidence beyond S46 still thin. Verdict: record metric,
  PARK_WITH_REASON for pipeline claims (no deployment-grade structured-pruning recovery located this pass).
- Modern reasoning distillation beyond R1: no separate record — R1-distills (S69) + V4.1 OPD-40-teachers
  (S123) + s1K-distill-from-Gemini (S149) already triangulate the modern practice. Sol may expand at Evidence.
