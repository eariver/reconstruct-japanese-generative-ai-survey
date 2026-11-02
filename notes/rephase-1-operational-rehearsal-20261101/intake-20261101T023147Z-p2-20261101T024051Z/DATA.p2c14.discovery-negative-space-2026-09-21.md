# Discovery negative-space / suspected gaps / terminology watches
# Edition: SP-efficient-llm-2026 | collector_run: efficient-llm-discovery-r1 | observed: 2026-09-21
# For Sol Discovery completeness review. NOT silently ignored; each needs pursue/park decision.

## G01 — DeepSeek-V4.1-Flash "Read Paper" target URL unlocated
- The launch page (S31) links a paper; no arXiv/HF-paper URL was isolated in this pass. Without it the
  edition lacks the capstone's mechanism authority (CED/CSA2/Engram/DSpark derivations). Priority gap-fill.

## G02 — DSpark primary mechanism authority missing
- Only checkpoint-config + vLLM code + card prose (S40). Losslessness, acceptance model, draft-training
  recipe, and DSpark-vs-MTP-head relationship unverified. Do not assert DSpark == MTP-head + tree.

## G03 — DSA (DeepSeek Sparse Attention, V3.2-Exp) primary URL unisolated
- Needed to separate DSA vs CSA/CSA2 vs NSA vs QSA (S32). Terminology collision risk is high in this family.

## G04 — "KDA" label collision (Kimi Delta Attention S27 vs NVIDIA NIM "hybrid KDA" for GLM-5.3-Flash S85)
- Resolve whether GLM's "KDA" denotes the same kernel ancestry or vendor shorthand. No ancestry claim allowed.

## G05 — "mHC" cross-lab recurrence (DeepSeek V4-Flash S17, Mega-mHC kernel in ezyang S77, GLM-5.3-Flash S83/S84)
- Shared term across three labs' 2026 materials. Mechanism-equivalence check required; treat as terminology
  watch, not evidence of transfer.

## G06 — Jev independent reproduction: community-grade only (S73)
- No peer-reviewed or vendor-independent benchmark of typed-decision vs generate-then-parse located.
- RLCD algorithm transparency: no public pseudo-code/paper located; parallel-sampler architecture details
  vendor-only. Evaluation-methodology exactness (S70 race) unbound.

## G07 — Training-cost ratios are vendor-claimed across capstones
- Qwen 1/3-tokens ~1/9-FLOPs (S08), GLM 1/10th-price + 3.0x/4.4x (S83/S84), DeepSeek 1/4-HBM 1/8-SSD (S31).
  None independently reproduced in this pass. Cost-per-completed-task (the D01-correct metric) measured nowhere.

## G08 — Expert-choice routing, Ring Attention, ThunderMLA and other plausible absentees
- Specialist sweep question: expert-choice routing (Zhou et al. 2022) industrial adoption; Ring Attention
  long-context training; ThunderMLA/TileLang kernel line; Hydra/Sequoia draft-head variants beyond EAGLE-2;
  BitNet industrial deployment (S47); FP4 TRAINING evidence (FP4 appears here as inference/serving only).
  Each is a pursue/park candidate, not a silent omission.

## G09 — Alias map (same mechanism, different vendor names) — draft for Sol audit
- sparse-attention family: DSA (DeepSeek V3.2) / CSA+HCA (V4-Flash) / CSA2 (V4.1) / NSA (S26) / QSA (Qwen) /
  IndexPool+sparse (GLM) — pairwise deltas unverified.
- linear-recurrent family: Mamba(2) / GDN (S24) / KDA-Kimi (S27) / "KDA"-GLM (S85).
- residual plumbing: Gated Residual-Qwen (S08) / Single-Pass mHC-V4.1 (S30) / mHC-GLM (S83) / Mega-mHC (S77).
- decoding: MTP-head (S38/S39) / DSpark (S40) / EAGLE-tree (S36/S37).

## G10 — Benchmark methodology primaries outstanding
- DeepSWE-1.1 standalone methodology (S100 relies on a model-card footnote); BrowseComp methodology (S97);
  SWE-bench-Pro body + which-"Pro" normalization (S93); BFCL paper counterpart (S95); HLE numbers absent
  for all capstones (S90). Efficiency-metric harness conditions (batch/concurrency/HW) absent for most
  provider throughput figures (S75/S80).

## G11 — Retrieval-status honesty ledger
- SUMMARY_CAPTURED (web-search grounded, full body pending Evidence): S01–S03, S05–S09(except S09 partial),
  S10–S17, S18–S27, S29–S31, S33–S40, S41–S47, S49, S53, S55, S57, S59–S63, S67–S69, S70–S74, S75–S76, S79–S85, S88–S94, S96, S98, S100.
- LOCATOR_CAPTURED (existence/location verified, body not yet read): S07(repo), S28, S48, S50–S52(partial S52 summary), S54, S56, S58, S64–S66, S93, S95.
- LOCATOR_ONLY (location plausible, body untouched): S32, S86, S87, S97, S99.
- No record claims AUTHORITY_CONSUMED — that judgment belongs to Sol at Evidence authority-consumption review.
