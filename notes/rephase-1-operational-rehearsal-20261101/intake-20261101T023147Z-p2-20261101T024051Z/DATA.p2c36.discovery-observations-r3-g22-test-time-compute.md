# Discovery observations r3 — G22 Test-Time Compute / Reasoning Efficiency (major lane)
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r3 | observed: 2026-09-21
# Thesis: tokens/SEC (D05) and tokens/TASK (here) are different levers. Distinct from speculative decoding.
# Six-way distinction: (1) faster generation / (2) fewer reasoning tokens / (3) parallel samples-search /
# (4) difficulty-adaptive compute / (5) learned stopping / (6) explicit user-runtime budget.

## S148 — Scaling LLM Test-Time Compute Optimally (Snell et al.)
- locator: https://arxiv.org/abs/2408.03314
- class: PRIMARY_PAPER | published: 2024-08 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: Origin for the lane: test-time scaling can beat parameter scaling for reasoning; verifier +
  search strategy (best-of-N/beam/majority); difficulty dependence (hard prompts benefit most);
  compute-optimal allocation; FLOPs-matched comparisons. Sequential-vs-parallel framing reused by s1.

## S149 — s1: Simple test-time scaling (Muennighoff et al.)
- locator: https://arxiv.org/abs/2501.19393
- class: PRIMARY_PAPER | published: 2025-01-31 | retrieval: SUMMARY_CAPTURED
- summary: s1K (1000 Q, difficulty/diversity/quality) SFT on Qwen2.5-32B (26 min/16 H100) + BUDGET FORCING
  (truncate with end-of-thinking delimiter OR extend with "Wait"); exceeds o1-preview up to +27% MATH/AIME24;
  50->57% AIME24 extrapolation, flattens ~6x. Training-data-selection x inference-budget relationship explicit;
  claims benchmark-specific (competition math). Sequential (long trace) vs Parallel (majority vote) taxonomy.

## S150 — ThinkPrune (RL pruning of long CoT)
- locator: https://arxiv.org/abs/2504.01296
- class: PRIMARY_PAPER | published: 2025-04 | retrieval: LOCATOR_CAPTURED (body pending Evidence/gap-fill)
- summary: Reasoning-token pruning via RL (class (2)+(5): fewer tokens + learned brevity). Representative of
  shorter-chain-preference mechanisms; body unread — Sol to confirm it carries the mechanism-class weight
  or substitute at Evidence.

## S151 — When More Thinking Hurts: Overthinking in Test-Time Scaling
- locator: https://arxiv.org/abs/2604.10739
- class: PRIMARY_PAPER | published: 2026-08-24 | retrieval: SUMMARY_CAPTURED
- summary: R1-32B vs s1-32B on GPQA Diamond, budgets 500–16000: both peak ~10K then DECLINE (negative flips
  dominate); 8000 tokens = 16x cost of 500. Overthinking mechanism (abandoning correct answers) +
  adaptive-stopping implication: stopping can cut cost AND raise accuracy. Cost-quantified diminishing
  returns — the lane's cautionary anchor.

## S152 — Reasoning on a Budget (survey of adaptive/efficient TTC)
- locator: https://arxiv.org/abs/2507.02076
- class: PRIMARY_PAPER (survey) | published: 2025-07 | retrieval: LOCATOR_CAPTURED
- summary: Secondary-by-design: taxonomy of adaptive test-time allocation (class (4)) incl. 2025–2026 work.
  Use as candidate-finder + taxonomy cross-check, never as mechanism authority.

## S153 — Current-model effort-control binding (V4.1 + Qwen first-party)
- locator: https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash
- class: PRIMARY_MODEL_CARD (binding record; mechanism in S123/S127) | published: 2026-09
- retrieval: SUMMARY_CAPTURED
- summary: V4.1: continuously controllable reasoning effort 1–100 with exponential token penalty + per-effort
  result tables (class (6) explicit budget). Qwen (via S127 card): enable_thinking / preserve_thinking /
  reasoning_effort + thinking/non-thinking modes. Lane-to-capstone binding; effort-vs-accuracy curves to be
  read at Evidence, not asserted here.
