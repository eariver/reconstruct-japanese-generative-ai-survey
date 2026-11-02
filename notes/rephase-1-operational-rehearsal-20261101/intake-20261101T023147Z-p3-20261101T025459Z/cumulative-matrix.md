# Cumulative inventory matrix — P1/P2/P3 + prior captures (no recopy)

Reuse rule: P3 reuses P1/P2/archived bytes by reference (hashes in their manifests); only new REQUIRED Raw bytes fetched here. No file recopied across intakes.

| Intake | GETs | DATA files | Bytes | Contents | Manifest |
|---|---|---|---|---|---|
| P1 `intake-20261101T023147Z` | 6 | 4 | 23382 | W34 candidate/release (774), SP listings/profile/state (c8) | `manifest.json` |
| P2 `...p2-20261101T024051Z` | 179 | 145 | 12194416 | checkpoints (20) + aggregated dossier (W34 369/439/409/409, SP 165/160/160) + Raw 25 obs + supplement 13 raw + reader/PDF + validations/worklogs | `manifest.json` (179 results, multiline) |
| P3 `...p3-20261101T025459Z` (this) | 63 (59 contents +4 blob) | 59 | 13492448 | W34 55 discovery Raw + bib audit + official-provenance + working-set + sol decision + sty + SP x-reception (4 large via blob) | `manifest.json` (63 results, multiline) |
| Prior archived (reused, not refetched) | 0 new | — | — | `tree.json` 3351 W34 blobs; 15-file W34 snapshot; 774 manuscript; 3e3e PDF (338722B `e93db71a...`); 4-doc c8 intake (`.py` DATA) | their packets |

Total new bytes this program: P1 ~25KB + P2 12,194,416B + P3 13,492,448B = ~25.7MB (plus 15MB transport overhead in `*.stdout.raw`). No recopy across intakes.

## Path coverage (not handcounts)

### W34 discovery `raw_paths` (55 unique in `DATA.p2b01.discovery-v2.jsonl`, all under `sources/2026-W34/`)
- Total refs: 55; fetched in P3 (+1 already in P2): 55 (carryover ledger already in P2 `DATA.p2e07...`, 54 new here). No W33/other-edition ref → no broad read.
  - `sources/2026-W34/carryover/carryover-ledger-v0.1.json` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2e07.carryover-ledger-v0.1.json
  - `sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/comfy-org__comfyui.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a01.comfy-org__comfyui.json
  - `sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/flashinfer-ai__flashinfer.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a02.flashinfer-ai__flashinfer.json
  - `sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/ggml-org__llama.cpp.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a03.ggml-org__llama.cpp.json
  - `sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/huggingface__transformers.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a04.huggingface__transformers.json
  - `sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/nvidia__tensorrt-llm.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a05.nvidia__tensorrt-llm.json
  - `sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/sgl-project__sglang.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a06.sgl-project__sglang.json
  - `sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/vllm-project__vllm.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a07.vllm-project__vllm.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/arxiv-agent-inheritance.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a08.arxiv-agent-inheritance.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/arxiv-corun.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a09.arxiv-corun.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/arxiv-egogazelite.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a10.arxiv-egogazelite.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/arxiv-embodied-security.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a11.arxiv-embodied-security.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/arxiv-lapf.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a12.arxiv-lapf.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/arxiv-scienceflow.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a13.arxiv-scienceflow.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/aws-vector-solutions.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a14.aws-vector-solutions.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/deepseek-v4-flash-vision-exp.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a15.deepseek-v4-flash-vision-exp.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/google-gemini-3-7-flash.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a16.google-gemini-3-7-flash.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/google-omni-1-1-flash.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a17.google-omni-1-1-flash.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/google-transcribe.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a18.google-transcribe.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/minimax-h3.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a19.minimax-h3.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/minimax-music-3.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a20.minimax-music-3.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/mistral-agentic-search.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a21.mistral-agentic-search.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/nvidia-ai-ecosystem.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a22.nvidia-ai-ecosystem.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/openai-api-regional-processing.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a23.openai-api-regional-processing.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/openai-chatgpt-release-notes.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a24.openai-chatgpt-release-notes.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/qwen3-8-27b.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a25.qwen3-8-27b.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/runway-changelog.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a26.runway-changelog.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/sol-baseline-locator-observations.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a27.sol-baseline-locator-observations.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/stability-stable-audio.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a28.stability-stable-audio.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/xai-api-changelog.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a29.xai-api-changelog.json
  - `sources/2026-W34/collectors/sol-approved-primary-gapfill/runs/w34-discovery-materialization-r1/raw/zai-glm-5-3.json` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a30.zai-glm-5-3.json
  - `sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/arxiv/runs/20260907T161121Z/raw/cs-ai.atom` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a31.cs-ai.atom
  - `sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/arxiv/runs/20260907T161121Z/raw/cs-cl.atom` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a32.cs-cl.atom
  - `sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/arxiv/runs/20260907T161121Z/raw/cs-cr.atom` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a33.cs-cr.atom
  - `sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/arxiv/runs/20260907T161121Z/raw/cs-cv.atom` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a34.cs-cv.atom
  - `sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/arxiv/runs/20260907T161121Z/raw/cs-dc.atom` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a35.cs-dc.atom
  - `sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/arxiv/runs/20260907T161121Z/raw/cs-lg.atom` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a36.cs-lg.atom
  - `sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/official-pages/runs/20260907T161655Z/raw/apple-ml-research.html` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a37.apple-ml-research.html
  - `sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/official-pages/runs/20260907T161655Z/raw/cohere-blog.html` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a38.cohere-blog.html
  - `sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/official-pages/runs/20260907T161655Z/raw/kimi-code-whats-new.html` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a39.kimi-code-whats-new.html
  - `sources/2026-W34/execution/luna/w34-architecture-r2-research-sufficiency-revision-r1/source-intake/sources/2026-W34/collectors/official-pages/runs/20260907T161655Z/raw/openai-news-rss.html` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a40.openai-news-rss.html
  - `sources/2026-W34/execution/luna/w34-discovery-gapfill-after-sol-review-r1/source-observations/alibaba-model-lifecycle-official-web.md` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a41.alibaba-model-lifecycle-official-web.md
  - `sources/2026-W34/execution/luna/w34-discovery-gapfill-after-sol-review-r1/source-observations/official-fallback-web-observations.md` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a42.official-fallback-web-observations.md
  - `sources/2026-W34/external/x/dailyx/raw/2026-08-16_0700.md` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a43.2026-08-16_0700.md
  - `sources/2026-W34/external/x/dailyx/raw/2026-08-17_0700.md` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a44.2026-08-17_0700.md
  - `sources/2026-W34/external/x/dailyx/raw/2026-08-18_0700.md` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a45.2026-08-18_0700.md
  - `sources/2026-W34/external/x/dailyx/raw/2026-08-19_0700.md` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a46.2026-08-19_0700.md
  - `sources/2026-W34/external/x/dailyx/raw/2026-08-20_0700.md` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a47.2026-08-20_0700.md
  - `sources/2026-W34/external/x/dailyx/raw/2026-08-21_0700.md` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a48.2026-08-21_0700.md
  - `sources/2026-W34/external/x/dailyx/raw/2026-08-22_0700.md` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a49.2026-08-22_0700.md
  - `sources/2026-W34/external/x/weekly-x-2026-W34-r2/raw/correction-report.md` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a50.correction-report.md
  - `sources/2026-W34/external/x/weekly-x-2026-W34-r2/raw/grok-x-result.corrected.md` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a51.grok-x-result.corrected.md
  - `sources/2026-W34/external/x/weekly-x-2026-W34-r2/raw/search-accounting.corrected.md` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a52.search-accounting.corrected.md
  - `sources/2026-W34/external/x/weekly-x-2026-W34-r2/raw/x-url-ledger.corrected.tsv` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a53.x-url-ledger.corrected.tsv
  - `sources/2026-W34/intake/working-set/sol-discovery-event-inventory-v0.2.md` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a54.sol-discovery-event-inventory-v0.2.md

### SP discovery `raw_paths` (25 unique in `DATA.p2b20.discovery-v2.jsonl`)
- Total refs: 25 (24 `raw/` +1 `external/x/.../x-reception-result-r3.md`); 25 `raw/` files already in P2 (`DATA.p2c14-38`), x-reception fetched in P3 (`DATA.p3a59...`). Negative-space file in `raw/` but not referenced in discovery → still fetched in P2 as Raw closure (extra, not missing).
  - `sources/SP-efficient-llm-2026/external/x/efficient-llm-reception-pass-01/raw/x-reception-result-r3.md` → intake-20261101T023147Z-p3-20261101T025459Z/DATA.p3a59.x-reception-result-r3.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-benchmarks-methodology.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c15.discovery-observations-benchmarks-methodology.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-capstones-2026.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c16.discovery-observations-capstones-2026.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-d01-fundamentals.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c17.discovery-observations-d01-fundamentals.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-d02-scaling-training.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c18.discovery-observations-d02-scaling-training.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-d03-moe.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c19.discovery-observations-d03-moe.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-d04-attention-kvcache.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c20.discovery-observations-d04-attention-kvcache.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-d05-decoding.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c21.discovery-observations-d05-decoding.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-d06-precision.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c22.discovery-observations-d06-precision.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-d07-representation-local.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c23.discovery-observations-d07-representation-local.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-d08-serving.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c24.discovery-observations-d08-serving.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-d09-distillation.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c25.discovery-observations-d09-distillation.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-d10-specialization-jev.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c26.discovery-observations-d10-specialization-jev.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g12-distributed-training.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c27.discovery-observations-r2-g12-distributed-training.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g13-kv-management.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c28.discovery-observations-r2-g13-kv-management.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g14-conditional-depth.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c29.discovery-observations-r2-g14-conditional-depth.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g15-harness.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c30.discovery-observations-r2-g15-harness.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g16-capstone-firstparty.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c31.discovery-observations-r2-g16-capstone-firstparty.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g17-g18-routing-lowbit.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c32.discovery-observations-r2-g17-g18-routing-lowbit.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-r2-g19-g20-data-jev.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c33.discovery-observations-r2-g19-g20-data-jev.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-r3-d09-depth-check.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c34.discovery-observations-r3-d09-depth-check.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-r3-g21-conditional-memory.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c35.discovery-observations-r3-g21-conditional-memory.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-r3-g22-test-time-compute.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c36.discovery-observations-r3-g22-test-time-compute.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-r3-g23-model-routing.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c37.discovery-observations-r3-g23-model-routing.md
  - `sources/SP-efficient-llm-2026/raw/discovery-observations-r4-x-followup.md` → intake-20261101T023147Z-p2-20261101T024051Z/DATA.p2c38.discovery-observations-r4-x-followup.md

### W34 article identities (manuscript `supporting_files` + primary, 12 files)
- All 12 verified exact SHA+bytes vs fetched bytes + tree blobs (see P3 README §2): `main.tex` +8 sections +`references.bib`+`jgaisurvey.sty` (P2 `DATA.p2c39-49` + P3 `DATA.p3a58...`). No stale index paths.
