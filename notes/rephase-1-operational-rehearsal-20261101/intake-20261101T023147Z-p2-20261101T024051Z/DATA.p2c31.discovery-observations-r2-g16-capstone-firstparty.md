# Discovery observations r2 — G16 Capstone first-party authority completion
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r2 | observed: 2026-09-21
# Closes r1 G01 (V4.1 paper), G02 (DSpark mechanism), G03 (DSA primary), G04/G05 (GLM terminology ground).

## S123 — DeepSeek-V4.1-Flash technical report (official; closes G01)
- locator: https://arxiv.org/abs/2609.19969
- class: PRIMARY_PAPER (official technical report) | published: 2026-09-18 | retrieval: SUMMARY_CAPTURED (full-body + HF PDF pending Evidence)
- mirror: https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/DeepSeek_V41_Tech_Report.pdf
- summary: CED (8B prefill / 16B decode active); pure CSA2 (Full/Reindex/Reuse, Hierarchical Sparse Indexer);
  FP4 global KV in TRAINING with marginal degradation; 890 B/token HBM (~1/4 V4-Flash); SWA Bounded Replay
  (persistent ~1/8; bounds decoder forward to n_win, nearly halves prefill compute); persistent-KV management
  section; Engram section; 45T multimodal pretrain; SFT->RL->OPD (40+ teachers, async rollout); controllable
  effort 1-100 with exponential token penalty; eval appendix with scaffold configs (N=8 DeepSWE / N=3 T-Bench,
  temp 1.0, containers, no-net T-Bench 2.1). Benchmark table incl. HLE†/Codeforces/MathArena/Terminal-Bench
  2.1-4.0/DeepSWE/NL2Repo/CyberGym with †-marked conditions to bind at Evidence.
- r1 parents: external:SP-efficient-llm-2026:EFF-D030, external:SP-efficient-llm-2026:EFF-D031.

## S124 — DeepSeek-V4 technical report (V4-Flash first-party anchor)
- locator: https://arxiv.org/abs/2606.19348
- class: PRIMARY_PAPER (official report, preview) | published: 2026-04-26 | retrieval: SUMMARY_CAPTURED
- summary: V4-Pro 1.6T/49B + V4-Flash 284B/13B; hybrid CSA+HCA; FP4 routed experts; Muon training;
  32T/33T tokens; 1M native; vs V3.2: 10% single-token FLOPs / 7% KV (Flash @1M). Upgrades S17 provider
  facts to first-party authority; V4-Pro phase-out context (S31 launch page: V4-Pro routes to V4.1-Flash).
- r1 parent: external:SP-efficient-llm-2026:EFF-D017.

## S125 — DeepSeek-V3.2 report (DSA primary; closes G03)
- locator: https://arxiv.org/abs/2512.02556
- class: PRIMARY_PAPER (official report) | published: 2025-12 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: DSA = lightning indexer + fine-grained token selection under MLA; O(Lk) vs O(L^2); continued
  training from V3.1-Terminus (ONLY architectural delta vs Terminus); parity with Terminus + Fiction.liveBench
  independent long-context signal; scaled RL post-training; Speciale variant; independent-eval citations.
  Disambiguation: DSA (V3.2 continued-training, MLA-instantiated) vs CSA/CSA2 (V4/V4.1 static modes) vs
  NSA (S26) vs QSA (S29).
- r1 parent: external:SP-efficient-llm-2026:EFF-D032.

## S126 — DeepSeek-V3.2-Exp launch + API docs (DSA debut, price-cut evidence)
- locator: https://deepseek.com/en/news/v3-2-exp
- class: PRIMARY_ANNOUNCEMENT | published: 2025-09-29 | retrieval: SUMMARY_CAPTURED
- mirror: https://api-docs.deepseek.com/news/news250929 (Tech report: https://github.com/deepseek-ai/DeepSeek-V3.2-Exp/blob/main/DeepSeek_V3_2.pdf; kernels in TileLang+CUDA; HF: deepseek-ai/DeepSeek-V3.2-Exp)
- summary: DSA debut on V3.1-Terminus; API prices cut 50%+ immediately; open weights + kernels. G07-relevant:
  rare vendor-claimed efficiency->price transmission with a dated price event (verify price table at Evidence).
- r1 parent: external:SP-efficient-llm-2026:EFF-D032.

## S127 — QwenLM/Qwen3.8-Flash-Next GitHub repository (report + README source of truth)
- locator: https://github.com/QwenLM/Qwen3.8-Flash-Next
- class: PRIMARY_REPO (official; README.md + tech_report.pdf) | published: 2026-08 | retrieval: SUMMARY_CAPTURED (PDF body pending Evidence)
- summary: Distinction BOUND (HF card + ModelScope + README converge): Qwen3.8-Flash-Next = experimental
  open-weight preview (262144 native, YaRN->1M); Qwen3.8-Flash = production API version (1M default,
  built-in tools). N-gram async-prefetch overlap; refit scaling laws kill batch warmup; 1/9 training-cost
  claim (vendor). Serving: SGLang cookbook, vLLM recipe, TokenSpeed recipe, KTransformers recommended
  (D07 link). SWE-bench Pro methodology footnote: all-but-Opus on Claude Code harness; problematic tasks
  corrected; baselines re-run on refined set (binds S93/S100 normalization at Evidence).
- r1 parent: external:SP-efficient-llm-2026:EFF-D029.

## S128 — GLM-5 technical report (Z.ai first-party; closes GLM lineage ground)
- locator: https://arxiv.org/abs/2602.15763
- class: PRIMARY_PAPER (official report) | published: 2026-02-17 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: GLM-5 744B/40B (256 experts, 80 layers), 28.5T tokens; ADOPTS DSA (DeepSeek Sparse Attention,
  cited) for continued pretraining; MLA; SWA/GDN ablations + SimpleGDN continual-training linearization;
  RULER ablations; Chinese-GPU full-stack adaptation; MLA-vs-GQA memory claim. Establishes DSA as
  cross-lab adopted mechanism (no ancestry beyond citation) and grounds G04/G05 term checks.
- r1 parents: external:SP-efficient-llm-2026:EFF-D082, external:SP-efficient-llm-2026:EFF-D083.

## S129 — zai-org/GLM-5 GitHub repository (IndexShare, MTP, deployment matrix)
- locator: https://github.com/zai-org/GLM-5
- class: PRIMARY_REPO (official) | published: 2026-02 (created; ongoing) | retrieval: SUMMARY_CAPTURED
- summary: IndexShare (2603.12201): shared indexer every 4 sparse layers, 2.9x per-token FLOPs @1M;
  MTP acceptance +20% (GLM-5.2); deployment matrix SGLang/vLLM/Transformers/KTransformers/Unsloth + Ascend
  (vLLM-Ascend/xLLM/SGLang). IndexShare-vs-IndexPool naming: IndexShare is the published mechanism;
  IndexPool (S84 secondary gloss) unresolved — G04 partial; Evidence must confirm or drop IndexPool.
- r1 parent: external:SP-efficient-llm-2026:EFF-D084.

## S130 — zai-org/GLM-5.3-Flash model card (first-party checkpoint identity)
- locator: https://huggingface.co/zai-org/GLM-5.3-Flash
- class: PRIMARY_MODEL_CARD | published: 2026-08 (release 08-25/26) | retrieval: SUMMARY_CAPTURED (config tensors pending Evidence)
- summary: arxiv tag 2602.15763 (GLM-5 report lineage); MIT; fp8; glm5_next; eval-results; vLLM+SGLang+Docker
  serving blocks; BF16 sibling variant exists (precision-variant discipline for Evidence). Upgrades S82/S84
  secondary facts toward first-party checkpoint identity.
- r1 parent: external:SP-efficient-llm-2026:EFF-D082.

## S131 — Z.ai developer docs: GLM-5.3-Flash overview (3.01x / 4.44x first-party numbers)
- locator: https://docs.z.ai/guides/vlm/glm-5.3-flash
- class: PRIMARY_DOC | published: null (living docs) | retrieval: SUMMARY_CAPTURED
- summary: First open-source frontier model combining sparse+linear attention (vendor framing);
  attention compute -3.01x, KV -4.44x vs GLM-5.3. Precise ratios to prior GLM-5.3 (not absolute); vendor-claimed,
  G07 quarantine applies.

## S132 — KDA kernel implementation (FLA) + vLLM path (Kimi impl evidence; G16-Kimi)
- locator: https://github.com/fla-org/flash-linear-attention/tree/main/fla/ops/kda
- class: PRIMARY_REPO (implementation) | published: null (ongoing) | retrieval: LOCATOR_CAPTURED (kernel body pending Evidence)
- cross: https://github.com/MoonshotAI/Kimi-Linear (vLLM impl + checkpoints, r1 S28)
- summary: Open KDA kernel + vLLM implementation = implementation evidence beyond the paper (S27);
  materially adds deployability proof for the KDA lane. Kernel numerics/perf to be read at Evidence, not here.
- r1 parent: external:SP-efficient-llm-2026:EFF-D028.
