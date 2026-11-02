# Discovery observations r2 — G14 Conditional compute beyond MoE
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r2 | observed: 2026-09-21
# Key distinction: WHICH expert executes (MoE, r1 D03) != WHETHER this token executes this layer (here).

## S115 — Mixture-of-Depths (Raposo et al.)
- locator: https://arxiv.org/abs/2404.02258
- class: PRIMARY_PAPER | published: 2024-04 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: Learned per-token depth routing with fixed compute budget; router decides layer participation,
  not expert choice. Do NOT merge into MoE: routing object differs (depth vs expert). Real-LLM adoption
  status is a Sol materiality question (record, don't over-claim).

## S116 — LayerSkip (Elhoushi et al.; self-speculative early exit)
- locator: https://arxiv.org/abs/2404.16710
- class: PRIMARY_PAPER | published: 2024-04 | retrieval: SUMMARY_CAPTURED
- summary: Layer-dropout training + early-exit inference where the SAME model drafts (self-speculative)
  and verifies remaining layers. Bridges G14 (depth) and D05 (decoding): no separate draft model needed.
- r1 parent: external:SP-efficient-llm-2026:EFF-D036 (EAGLE family context).

## S117 — DeeBERT (Xin et al.; early-exit lineage anchor)
- locator: https://arxiv.org/abs/2004.12918
- class: PRIMARY_PAPER | published: 2020-04 | retrieval: SUMMARY_CAPTURED
- summary: Minimal early-exit precedent (off-ramps on BERT); included ONLY to bound the adaptive-computation
  history so MoD/LayerSkip are not presented as ex-nihilo. No LLM-scale claim attached.
