# Discovery observations r2 — G15 Efficiency measurement frameworks / harness authority
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r2 | observed: 2026-09-21
# Purpose: standardize WHAT each framework binds (workload, lengths, concurrency, TTFT/TPOT/throughput,
# HW, energy, accuracy, identity) so the issue can explain why two tokens/s numbers rarely compare.

## S118 — MLPerf Inference (MLCommons; incl. LLM interactive methodology)
- locator: https://mlcommons.org/benchmarks/inference/
- class: PRIMARY_SPEC (benchmark authority) | published: null (versioned rounds; paper 1911.02549 for v0.5 base)
- retrieval: SUMMARY_CAPTURED (round rules pending Evidence)
- paper: https://arxiv.org/abs/1911.02549 (Reddi et al., 2019-11)
- summary: Scenario-based harness (SingleStream/Multistream/Server/Offline) binding query arrival, latency
  bounds (e.g. TTFT/TPOT percentiles for interactive LLM), throughput under SLO, system + precision identity,
  and audited submission rules. The existence proof that comparable serving numbers REQUIRE a shared scenario;
  vendor tokens/s without scenario are non-comparable by construction.

## S119 — GenAI-Perf (NVIDIA perf_analyzer generative-AI benchmarking)
- locator: https://github.com/triton-inference-server/perf_analyzer
- class: PRIMARY_REPO (measurement tool) | published: null (ongoing) | retrieval: LOCATOR_CAPTURED
- summary: Request-rate-controlled load generation with TTFT/ITL/throughput decomposition for LLM serving
  endpoints. Binds concurrency/request-rate — the missing condition in most provider throughput figures
  (cf. S75/S80). AIPerf as a distinct NVIDIA product was NOT located in this pass (see ledger G15 note).

## S120 — LLMPerf (Ray project; token-throughput benchmark with published caveats)
- locator: https://github.com/ray-project/llmperf
- class: PRIMARY_REPO (measurement tool) | published: null (ongoing) | retrieval: LOCATOR_CAPTURED
- summary: Widely cited but caveated throughput harness (fixed synthetic workloads, client-side limits);
  include precisely BECAUSE its caveats teach the incomparability lesson. Do not present as ground truth.

## S121 — EleutherAI lm-evaluation-harness
- locator: https://github.com/EleutherAI/lm-evaluation-harness
- class: PRIMARY_REPO (evaluation harness) | published: null (ongoing) | retrieval: LOCATOR_CAPTURED
- summary: De-facto harness standard pinning prompt formatting, few-shot, sampling, and metric computation
  for accuracy benchmarks. Accuracy-side counterpart to serving harnesses: same benchmark name + different
  harness = different number (cf. S100 DeepSWE footnote).

## S122 — HELM (Stanford CRFM holistic evaluation)
- locator: https://github.com/stanford-crfm/helm
- class: PRIMARY_REPO + PRIMARY_PAPER | published: 2022-11 | retrieval: SUMMARY_CAPTURED
- paper: https://arxiv.org/abs/2211.09110 (Liang et al.)
- summary: Multi-metric/multi-scenario accuracy+efficiency+fairness harness with transparency-first reporting
  (exact prompts, adaptation, contamination notes). Reproducibility-framework anchor for the validity lane.
