# Discovery observations r3 — G23 Multi-Model Routing / Cascades (bounded system lane)
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r3 | observed: 2026-09-21
# Core question: why serve every request with the same expensive model?
# Mandatory taxonomy: MoE routing (experts) / MoD (token-layer) / speculative decoding (draft-verify) /
# MODEL ROUTING-CASCADE (whole model) / Jev specialization (task-specialized class). NOT an agent survey.

## S154 — FrugalGPT (Chen et al.; LLM cascade)
- locator: https://arxiv.org/abs/2305.05176
- class: PRIMARY_PAPER | published: 2023-05-10 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: Cascade origin: sequential cheap->expensive APIs with generation-scoring function + router +
  stop/cost judge; up to 98% cost saving at matched quality (or +4–5% accuracy at matched cost);
  HEADLINES case -80%/+1.5% vs GPT-4; sometimes WEAKER models correct where GPT-4 errs. Assumptions:
  reliable quality estimation; API-era cost table (stale prices — do not quote as current); added latency
  from sequential escalation is the limitation.

## S155 — RouteLLM (Ong et al.; learned preference-data router)
- locator: https://arxiv.org/abs/2406.18665
- class: PRIMARY_PAPER | published: 2024-06-26 | retrieval: SUMMARY_CAPTURED
- summary: Single-query routing (weak vs strong) trained on 80k Chatbot-Arena preferences + judge/golden
  augmentation; win-probability threshold alpha; PGR/CPT metrics; 2x+ savings (3.66x MT-Bench CPT50);
  generalizes to unseen model pairs without retraining. Contrast vs FrugalGPT: one call (latency-safe)
  vs sequential cascade (quality-estimation-gated). Router-training data staleness is the limitation.

## S156 — Dynamic Model Routing and Cascading survey (2026)
- locator: https://arxiv.org/abs/2603.04445
- class: PRIMARY_PAPER (survey) | published: 2026-04-21 | retrieval: SUMMARY_CAPTURED
- summary: Secondary-by-design: unifies routing vs cascading vs cascade-routing (AutoMix, Self-REF,
  LM-Blender, cascade routing with skip/reorder); quality estimation as the critical factor. Candidate
  pool for bounded follow-ups (Routoo/speculative cascades NOT separately collected — survey pointers
  suffice at Discovery; Sol may promote).

## S157 — Router-LLM fragility analysis (EACL 2026 Findings)
- locator: https://aclanthology.org/2026.findings-acl.1199.pdf
- class: PRIMARY_PAPER (limitation evidence) | published: 2026-03 | retrieval: SUMMARY_CAPTURED
- summary: Preference-data routers (incl. RouteLLM family) are fragile under distribution shift/paired-model
  change; "simple"-query definition sensitivity. Mandatory counterweight: routing gains are conditional on
  router-task alignment, paralleling the harness-dependence lesson (S100).

## S158 — Mixture-of-Agents (Wang et al.; model-pool collaboration)
- locator: https://arxiv.org/abs/2406.04692
- class: PRIMARY_PAPER | published: 2024-06 | retrieval: LOCATOR_CAPTURED (body pending Evidence/gap-fill)
- summary: Layered multi-model proposal/aggregation; included ONLY for the pool-vs-router boundary question
  (collaboration, not selection). Park-leaning: Sol to confirm materiality or park (agent-survey risk).
