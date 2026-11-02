# Discovery observations r4 — accepted X r3 corpus + bounded primary/runtime follow-up (F1–F4)

Source-local claims only until Evidence verification. Retrieval: SUMMARY_CAPTURED; full-body consumption at Evidence stage.

## X0 — Accepted X r3 corpus (basis for EFF-D162)

- Imported Raw: `sources/SP-efficient-llm-2026/external/x/efficient-llm-reception-pass-01/raw/x-reception-result-r3.md` (30213 bytes; Sol PASS / IMPORT_AUTHORIZED).
- 27 direct X observations; 24 unique accounts; 20 independent; 1 vendor/project; 2 runtime/packaging-maintainer; 1 unclear.
- FIRST_HAND 17 YES / 3 NO / 7 UNCLEAR. Reception 20 positive / 3 mixed / 0 negative / 4 neutral.
- Coverage buckets: DeepSeek V4.1 Flash 7; Qwen3.8-Flash-Next 6; Kimi Linear 2; GLM-5.3-Flash 5; Jev 3; local stack/mechanisms 4.
- Strong practical signal: local deployment feasibility, runtime maturity gaps, quantization choices, host-memory/offload constraints.
- Jev: one independent classification-oriented evaluation (OBS-R2-021) + OpenCode permission-routing integration (OBS-R2-022) + hosting availability (OBS-R2-023); systematic production-failure evidence LOW_SIGNAL.
- High-value editorial flags (not separate records): OBS-R2-002, 003, 005, 008, 009, 011, 014, 015, 017, 021, 022.
- X remains reception/deployment observation authority only, not technical-spec authority.

## F1 — DeepSeek V4.1 Flash vLLM recipe authority (EFF-D163)

- Locator: `https://recipes.vllm.ai/deepseek-ai/DeepSeek-V4.1-Flash` (vLLM Recipes, maintainer authority; observed 2026-09-22).
- New beyond EFF-D040/D078/D153 (DSpark mechanism, model code docs, HF card): recipe-level deployment authority — vLLM 0.30.0+ floor; single-node TEP/H200/B200 strategies; DSpark is the ONLY speculative method for this checkpoint because V4.1 dropped the MTP module trained alongside V3/V4 (serving-relevant architecture delta); on AMD/ROCm vLLM currently refuses adaptive verification (two named failing checks: indexer helper `supports_device_cpu_query_lens_mismatch()` False; `DeepseekV41ROCMAiterSparseSWABackend` reports `UNIFORM_BATCH` not `ALWAYS`); Engram tables alone ~196.6B params (~183–189 GiB) dominate capacity planning.
- Purpose served: separates architecture efficiency (8–16B active, compressed KV) from runtime support existence (day-0) from hardware/runtime immaturity (AMD verification refusal, MTP-module drop).
- GitHub self-report caveat: no field/performance issue promoted; recipe claims only.

## F2 — GLM-5.3-Flash Unsloth local quantization authority (EFF-D164)

- Locator: `https://unsloth.ai/docs/models/glm-5.3-flash` (Unsloth documentation, packaging authority; observed 2026-09-22). Unsloth previously absent from Discovery.
- New: authoritative GGUF availability table for GLM-5.3-Flash (1-bit UD-IQ1_S 93.1 GB through BF16 642 GB; UD-Q4_K_XL 200 GB; UD-IQ3_XXS 120 GB); memory-fit guidance (1-bit ~100 GB RAM; 3-bit 128–150 GB incl. Mac/DGX Spark; 8-bit 350 GB); llama.cpp + Unsloth Desktop paths; day-zero llama.cpp PR `ggml-org/llama.cpp#27754`; faster-decoding/MTP support claim (up to 3.3x at long context) recorded as vendor-packaging claim requiring independent confirmation — the X `1.6–3.4x` speed claim is NOT accepted.
- Corresponds to accepted X packaging observation OBS-R2-015/016.

## F3 — Qwen3.8-Flash-Next llama.cpp implementation authority (EFF-D165)

- Locator: `https://github.com/ggml-org/llama.cpp/pull/27742` (merged 2026-08-27; Unsloth-authored `qwen4exp` port; observed 2026-09-22).
- New beyond EFF-D050 (generic llama.cpp repo): exact implementation authority behind OBS-R2-009 — converter + text graph + QSA sparse attention + PLE n-gram hash embeddings (host-side hashing, 97.7 GiB table); correctness validated against vLLM reference (PPL 4.0068 vs 4.0126; QSA bit-identical below budget; jaccard 0.975 above); known gaps honestly documented (conv state across ubatches fixed in-PR; chunked-prefill/decode caveats).
- Materially explains Flash-Next support, MoE/CPU-offload-adjacent host-memory handling (PLE host-side row gather), and long-context implementation status.

## F4 — Jev independent-evaluation lead: INDEPENDENT_WRITEUP_NOT_RESOLVED

- OBS-R2-021's outbound full write-up link could not be resolved to an exact public source from outside X (two bounded searches; no `vesko_st` write-up recovered; nearby independent secondary material such as jev-agent benchmarks pages are NOT the linked source and are not substituted).
- The X observation (independent RC/commonsense + hand-authored Wikipedia + customer-service eval, Sonnet/Opus-level on several, contamination caveats) is retained as X observation only. No Discovery record created for F4.
