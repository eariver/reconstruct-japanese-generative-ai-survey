# Discovery observations — Benchmark methodology lane (taxonomy, seeds, efficiency metrics, validity)
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r1 | observed: 2026-09-21
# Rule: taxonomy/methodology/failure-modes only. NO leaderboard. Every number binds conditions at Evidence.

## S88 — MMLU-Pro (broad knowledge/reasoning, harder MMLU successor)
- locator: https://arxiv.org/abs/2406.01574
- class: PRIMARY_PAPER | published: 2024-06-13 | retrieval: SUMMARY_CAPTURED (methodology body pending Evidence)
- summary: 10-option, reasoning-focused mass-multitask set; the "broad knowledge" column for capstone tables
  (V4-Flash MMLU-Pro numbers in S75/NVIDIA card; Kimi MMLU-Pro-4k in S28). Version: pin exact revision at Evidence.

## S89 — GPQA Diamond (expert science, contamination-resistant)
- locator: https://arxiv.org/abs/2311.12022
- class: PRIMARY_PAPER | published: 2023-11-29 | retrieval: SUMMARY_CAPTURED
- summary: Google-proof expert science QA; Diamond = hardest verified split. Capstone citations (GPQA-D 91.7
  S79) must specify split/harness at Evidence.

## S90 — Humanity's Last Exam (frontier saturation-response benchmark)
- locator: https://arxiv.org/abs/2501.14249
- class: PRIMARY_PAPER | published: 2025-01-24 | retrieval: SUMMARY_CAPTURED
- summary: Expert-crafted hardest-questions set with public/private split design; validity-lane anchor for
  saturation/contamination discussion. No capstone HLE number captured this pass (negative-space note).

## S91 — LiveCodeBench (contamination-resistant code generation)
- locator: https://arxiv.org/abs/2403.07974
- class: PRIMARY_PAPER | published: 2024-03-15 | retrieval: SUMMARY_CAPTURED
- summary: Time-windowed problem collection vs contamination; version pinning (v6 in S79) mandatory at Evidence.

## S92 — SWE-bench (repository-level software engineering)
- locator: https://arxiv.org/abs/2310.06770
- class: PRIMARY_PAPER | published: 2023-10-10 | retrieval: SUMMARY_CAPTURED
- summary: Real-GitHub-issue task construction; base for the Verified/Pro validity-mandate thread (S93).
  Broken-task and harness-drift critiques belong to the validity lane, not the score column.

## S93 — SWE-bench-Pro (long-horizon SWE, validity-evolution example)
- locator: https://arxiv.org/abs/2503.01324
- class: PRIMARY_PAPER | published: 2025-03-04 | retrieval: LOCATOR_CAPTURED (body + version drift pending Evidence)
- summary: Mandatory evolution example with SWE-bench Verified: version drift, broken tasks, private subsets,
  self-reported vs reproduced scores. Qwen README cites "SWE-bench Pro 62.5" and "SWE-Pro" variants —
  Evidence must normalize WHICH Pro artifact/harness each capstone number used.

## S94 — Terminal-Bench (terminal/environment interaction)
- locator: https://arxiv.org/abs/2406.06750
- class: PRIMARY_PAPER | published: 2024-06-14 | retrieval: SUMMARY_CAPTURED
- summary: Containerized terminal tasks; GLM-5.3-Flash cites Terminal-Bench 2.1 84.3 (S84) — version suffix
  shows why benchmark NAME alone is not a measurement contract.

## S95 — BFCL / Berkeley Function-Calling Leaderboard (tool/function calling)
- locator: https://github.com/ShishirPatil/gorilla
- class: PRIMARY_REPO (official benchmark repo) | published: 2024 (ongoing) | retrieval: LOCATOR_CAPTURED
- summary: Multi-turn/function-call evaluation harness; paper counterpart to bind at Evidence. Tool-parser
  dependence (cf. S52 glm47 parser flags) is a hidden-scaffold risk for agent scores.

## S96 — τ-bench (interactive tool agents)
- locator: https://arxiv.org/abs/2406.12045
- class: PRIMARY_PAPER | published: 2024-06-20 | retrieval: SUMMARY_CAPTURED
- summary: Airline/retail tool-interaction tasks with pass^k consistency semantics; pass@k vs pass^k
  distinction is a mandatory condition-binding item at Evidence.

## S97 — BrowseComp (web browsing/research agents)
- locator: https://openai.com/index/browsecomp/
- class: PRIMARY_ANNOUNCEMENT | published: 2025-04 | retrieval: LOCATOR_ONLY (methodology pending gap-fill)
- summary: Hard web-research benchmark for browsing agents; relevant to agent-capability columns of 2026
  capstones. Exact version/harness outstanding.

## S98 — RULER (long-context retrieval/reasoning)
- locator: https://arxiv.org/abs/2404.18532
- class: PRIMARY_PAPER | published: 2024-04-26 | retrieval: SUMMARY_CAPTURED
- summary: Graded long-context suite (NIAH variants, multihop, aggregation); Kimi reports RULER-128k 84.3
  with 3.98x speedup (S28) — the rare joint capability+efficiency datapoint the lane wants more of.

## S99 — AIME / MAA competition authority (math benchmark generation)
- locator: https://maa.org/math-competitions
- class: PRIMARY_SPEC (competition owner) | published: null (annual) | retrieval: LOCATOR_ONLY
- summary: AIME2025 cited in Kimi RL results (S27); generation/year/cutoff and CI-tool conditions must be
  bound at Evidence (cf. MathVision-with-CI split in S79).

## S100 — DeepSWE-1.1 methodology note (harness-dependent agent benchmark)
- locator: https://huggingface.co/Qwen/Qwen3.8-Flash-Next
- class: PRIMARY_MODEL_CARD (methodology footnote) | published: 2026-08-26 | retrieval: SUMMARY_CAPTURED
- summary: Evaluated under Claude Code AND mini-SWE-agent harnesses (temp 1.0, top_p 0.95, 256K ctx),
  BEST-of-two reported; Flash-Next best on mini-SWE-agent. Exemplifies hidden-scaffold/vendor-harness risk:
  the "same benchmark" yields different numbers per harness, and best-of reporting inflates. Mandatory
  cautionary exhibit for the validity lane; independent DeepSWE methodology primary outstanding (gap-fill).
