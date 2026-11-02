# Discovery observations — D04 Attention, sequence and KV-cache efficiency (major lane)
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r1 | observed: 2026-09-21
# Categorical rule: IO-efficient exact attention (FlashAttention family) vs compute/storage-changing
# architectures (sparse / linear / recurrent / hybrid). Never collapse.

## S18 — Multi-Query Attention (Shazeer, "Fast Transformer Decoding: One Write-Head is All You Need")
- locator: https://arxiv.org/abs/1911.02150
- class: PRIMARY_PAPER | published: 2019-11-12 | retrieval: SUMMARY_CAPTURED (full body pending Evidence)
- summary: Single shared KV head; origin of the KV-footprint reduction thread (memory-bandwidth-bound decode).
  Quality cost vs MHA is the documented tradeoff; GQA later interpolates.

## S19 — GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints (Ainslie et al.)
- locator: https://arxiv.org/abs/2305.13245
- class: PRIMARY_PAPER | published: 2023-05-31 | retrieval: SUMMARY_CAPTURED
- summary: Grouped KV heads with checkpoint uptraining; the industry-default KV saver before MLA/sparse era.
  Adoption evidence: near-universal in open models 2023–2025.

## S20 — FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness (Dao et al.)
- locator: https://arxiv.org/abs/2205.14135
- class: PRIMARY_PAPER | published: 2022-05-27 | retrieval: SUMMARY_CAPTURED
- summary: Tiling + online softmax + recomputation = EXACT attention with O(N) HBM traffic instead of O(N^2).
  Mechanism authority for the IO model; must be taught as implementation efficiency, not approximation.

## S21 — FlashAttention-2 (Dao)
- locator: https://arxiv.org/abs/2307.08691
- class: PRIMARY_PAPER | published: 2023-07-17 | retrieval: SUMMARY_CAPTURED
- summary: Better parallelism/partitioning, ~2x over FA1. Boundary: still exact attention; does not change KV asymptotics.

## S22 — FlashAttention-3 (Shah et al.)
- locator: https://arxiv.org/abs/2407.08608
- class: PRIMARY_PAPER | published: 2024-07-10 | retrieval: SUMMARY_CAPTURED
- summary: Asynchrony/warp-specialization for Hopper (FP8, WGMMA). Hardware-conditional gains — D01
  GPU-architecture-dependence question instantiated.

## S23 — Mamba: Linear-Time Sequence Modeling with Selective State Spaces (Gu & Dao)
- locator: https://arxiv.org/abs/2312.00752
- class: PRIMARY_PAPER | published: 2023-12-01 | retrieval: SUMMARY_CAPTURED
- summary: Selective SSM with hardware-aware scan; linear-time, constant-state alternative to attention.
  Lineage anchor for the selective-state branch (Mamba2, GDN, KDA all respond to it).

## S24 — Gated DeltaNet (Yang et al.)
- locator: https://arxiv.org/abs/2412.06464
- class: PRIMARY_PAPER | published: 2024-12-12 | retrieval: SUMMARY_CAPTURED
- summary: Scalar forget gate on the delta rule (weight-decay reading); the direct parent of KDA and the
  recurrent half of Qwen/QSA and Kimi hybrids. Gated DeltaNet vs Mamba2 comparisons recur in Qwen materials.

## S25 — Mistral 7B (sliding-window attention anchor)
- locator: https://arxiv.org/abs/2310.06825
- class: PRIMARY_PAPER (official report) | published: 2023-10-10 | retrieval: SUMMARY_CAPTURED
- summary: SWA with rolling buffer + GQA; effective-span argument (layers x window). Local-attention baseline
  against which sparse/learned retrieval methods must be compared.

## S26 — Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention (Yuan et al.)
- locator: https://arxiv.org/abs/2502.11089
- class: PRIMARY_PAPER | published: 2025-02-17 | retrieval: SUMMARY_CAPTURED
- summary: Open-world addition: hierarchical compression-selection-sliding strategy trained end-to-end;
  adopted/discussed in the DeepSeek-adjacent sparse line (DSA vs NSA naming must be disambiguated at
  Evidence — different labs reuse "sparse attention" labels).

## S27 — Kimi Linear: An Expressive, Efficient Attention Architecture (Kimi Team)
- locator: https://arxiv.org/abs/2510.26692
- class: PRIMARY_PAPER (official technical report) | published: 2025-10-29 | retrieval: SUMMARY_CAPTURED
- summary: KDA = GDN + channel-wise diagonalized gate; 3:1 KDA:MLA hybrid with NoPE on MLA layers;
  48B total / 3B active; claims first fair-comparison win over full attention (short/long/RL regimes);
  KV -75%, up to 6x decode throughput at 1M; 1.16x compute-optimal efficiency; open KDA kernel + vLLM impl
  + 5.7T-token checkpoints. Mandatory D04 anchor.
- limitation: Fair-comparison methodology must be audited at Evidence (identical recipe claim); vendor-authored.

## S28 — MoonshotAI/Kimi-Linear repository (kernel + vLLM + checkpoints)
- locator: https://github.com/MoonshotAI/Kimi-Linear
- class: PRIMARY_REPO | published: 2025-10-29 | retrieval: LOCATOR_CAPTURED (tree/config pending Evidence)
- summary: Deployment authority for KDA: FLA kernel path, vLLM support, Base/Instruct 48B-A3B 1M checkpoints.
  Independent-implementation signal for D04 current-deployment evidence.

## S29 — Qwen/Qwen3.8-Flash-Next README (QSA config, GDN layout, n-gram, MTP, self-reported scores)
- locator: https://huggingface.co/Qwen/Qwen3.8-Flash-Next
- class: PRIMARY_MODEL_CARD | published: 2026-08-26 | retrieval: SUMMARY_CAPTURED (config tensors pending Evidence)
- summary: 125B/6B + 51B n-gram (20M bigrams/trigrams, layer 2, host-offloaded); 48 layers in
  12x(3x(GDN->MoE)->1x(QSA->MoE)); MoE 512 experts (10 routed + 1 shared); QSA = MQA indexer (4Q/1K, d128),
  budget 512 blocks/2048 tokens; MTP 1 layer; 262144 native context (1M via YaRN on API SKU).
  Self-reported: DeepSWE 58.7, SWE-Pro 62.5, Toolathlon 73.5, LCB-v6 91.9, GPQA-D 91.7 (harness/condition-bound).
- limitation: All scores vendor self-reports with harness dependence (Claude Code vs mini-SWE-agent, best-of-two
  reporting). Training-cost ratios (1/3 tokens, ~1/9 FLOPs) likewise vendor-claimed.

## S30 — deepseek-ai/DeepSeek-V4.1-Flash model card (CED, CSA2, SWA replay, Engram, DSpark)
- locator: https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash
- class: PRIMARY_MODEL_CARD | published: 2026-09-10 | retrieval: SUMMARY_CAPTURED (config/model.py pending Evidence)
- summary: 552B backbone + 196B Engram tables; 20-layer causal encoder + 20-layer decoder with decoder global
  KV projected from encoder states (8B active prefill / 16B decode); CSA2 static Full/Reindex/Reuse modes +
  Hierarchical Sparse Indexer; FP4 main KV (E2M1) -> 890 bytes/token (~1/4 of V4-Flash); SWA Bounded Replay
  (persist ~1/8 of V4-Flash); Single-Pass mHC; 1 shared + 384 routed experts (6 active); DSpark speculative
  decoding; native multimodal (DeepSeek-ViT); 45T-token pretrain; controllable reasoning effort 1–100.
- limitation: Card omits license field in captured excerpt (verify at Evidence); Engram/DSpark need
  mechanism-depth gap-fill (config.json, model.py, vLLM code S40/S78).

## S31 — Introducing DeepSeek-V4.1-Flash (official launch)
- locator: https://www.deepseek.com/en/news/deepseek-v4-1-flash
- class: PRIMARY_ANNOUNCEMENT | published: 2026-09-10 | retrieval: SUMMARY_CAPTURED
- summary: 552B MoE; 8B-input/16B-output active; KV 1/4 HBM + 1/8 SSD vs previous generation; API live
  (model id deepseek-flash) with native multimodal; peak/off-peak pricing (off-peak 50%); open-source
  inference collaboration promised. Links "Read Paper" (paper locator NOT yet captured — Sol gap-fill candidate).
- limitation: Announcement-level; benchmark chart conditions and paper URL outstanding.

## S32 — DeepSeek-V3.2-Exp / DeepSeek Sparse Attention (DSA) announcement trace
- locator: https://www.deepseek.com/
- class: PRIMARY_ANNOUNCEMENT (indirect trace via V4.1 launch page + provider pages) | published: 2026 (exact date unverified)
- retrieval: LOCATOR_ONLY — dedicated DSA announcement/report URL not yet isolated in this pass.
- summary: DSA = faster, more efficient long-context training & inference with 50%+ API price cut (per launch
  page). Needed to separate DSA (V3.2-Exp) from CSA/CSA2 (V4 line), NSA (S26), QSA (S29).
- gap: Sol-directed gap-fill: isolate DSA primary URL + mechanism delta vs NSA/CSA.
