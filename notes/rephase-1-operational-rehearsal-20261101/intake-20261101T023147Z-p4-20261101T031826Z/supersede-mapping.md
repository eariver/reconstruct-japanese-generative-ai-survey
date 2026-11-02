# Supersede mapping — P3 failed zero DATA → P4 verified payload (full hex, no truncation)

Old P3 DATA preserved (0 bytes, `sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`) as fault evidence; **SUPERSEDED UNAVAILABLE — do NOT consume**. New P4 DATA is authoritative for these 6 repo paths.

| P3 failed gid | Repo path @774 | Blob SHA (fixed metadata) | Size | Old DATA (0B, superseded) | P4 new gid | P4 NEW verified DATA | SHA256 (full) |
| P3 failed gid | Repo path @774 | Blob SHA (fixed metadata) | Size | Old DATA (0B, superseded) | P4 new gid | P4 NEW verified DATA | SHA256 (full) |
| `p3a02` | `sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/flashinfer-ai__flashinfer.json` | `90462213d9825c9224a0b169d753f023dcf18537` | 1805968 | `intake-...p3.../DATA.p3a02.*` (0B `e3b0...`, UNAVAILABLE) | `p4a02` | `intake-...p4-.../DATA.p4a02.flashinfer-ai__flashinfer.json` | `f75febae2316477e9cd12c4e0a654e83f6d4f90e2def3a47a8a4ad1922946507` |
| `p3a03` | `sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/ggml-org__llama.cpp.json` | `62edff35562c0eaa4d175546364b1c2838a11a3a` | 5257525 | `intake-...p3.../DATA.p3a03.*` (0B `e3b0...`, UNAVAILABLE) | `p4a03` | `intake-...p4-.../DATA.p4a03.ggml-org__llama.cpp.json` | `80345df9de1fc27f8401efe9bd26cba04297ac9f755eeb41b4f7e231339175d2` |
| `p3a04` | `sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/huggingface__transformers.json` | `daa04d862800fc51c3066a2b3e2f53ff96394992` | 1323799 | `intake-...p3.../DATA.p3a04.*` (0B `e3b0...`, UNAVAILABLE) | `p4a04` | `intake-...p4-.../DATA.p4a04.huggingface__transformers.json` | `2a843332a5f95495ac372fa9e947c73a90e5dc93320f6461718c0d65cea8b6f9` |
| `p3a05` | `sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/nvidia__tensorrt-llm.json` | `6b093886cc5cf29de0c3ebe55bb907de9c64bad3` | 1854867 | `intake-...p3.../DATA.p3a05.*` (0B `e3b0...`, UNAVAILABLE) | `p4a05` | `intake-...p4-.../DATA.p4a05.nvidia__tensorrt-llm.json` | `d711b2ebb37cba888013ce125315c90b446721c0f194159fbb9622ca09598f9a` |
| `p3a06` | `sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/sgl-project__sglang.json` | `f16c5ec6b2a24a09e7f76dd5fd7ca8e555d30587` | 1839084 | `intake-...p3.../DATA.p3a06.*` (0B `e3b0...`, UNAVAILABLE) | `p4a06` | `intake-...p4-.../DATA.p4a06.sgl-project__sglang.json` | `acab64f7e4eb53f3d5bc1dd0cdc12e38af3fe7685d9a9d630c2365cb9ad0c9d2` |
| `p3a07` | `sources/2026-W34/collectors/github-releases/runs/20260902T121634Z/raw/vllm-project__vllm.json` | `94aaa50674ab67014d4b0a0030c00af752df7c87` | 3340585 | `intake-...p3.../DATA.p3a07.*` (0B `e3b0...`, UNAVAILABLE) | `p4a07` | `intake-...p4-.../DATA.p4a07.vllm-project__vllm.json` | `75f34b036929d41ad2cabb290b8eb647b9776ed0942a7d4d2399edf967a763be` |

P3 large-file pattern already blob-fixed in P3 (preserved, verified, NOT superseded here):
- `p3a31 cs-ai.atom` 2479649B `2fd387fe...` → `p3b31` blob `2fd387fe...` verified (`DATA.p3a31.cs-ai.atom` now 2479649B `31243b8b...`). Contents-API `encoding:none` metadata-only, supplemented by exact blob.
- `p3a34 cs-cv.atom` 1612070B `4e19a711...` → `p3b34` verified.
- `p3a36 cs-lg.atom` 1996383B `d3b5ea7e...` → `p3b36` verified.
- `p3a37 apple-ml-research.html` 2532040B `0f83d2c2...` → `p3b37` verified.

X-manifests/tasks (NEW, no prior failure):
- W34 `x-source-intake-v2.json` 3913B `113d62e7...` (`DATA.p4x01...` `702881aa...`) + task `grok-task.md` 11686B `2d6c607b...` (`DATA.p4x03...` `e97bbd06...` == manifest) + result `grok-x-result.corrected.md` 23612B (P3 `DATA.p3a51...` `43b0923b...` == manifest).
- SP `x-source-intake-v2.json` 5359B `638ea4af...` (`DATA.p4x02...` `3465dc4f...`) + task `grok-task.md` 20555B `c9a04eb6...` (`DATA.p4x04...` `c1150730...` == manifest) + result `x-reception-result-r3.md` 30213B (P3 `DATA.p3a59...` `b3a8a040...` == manifest).
