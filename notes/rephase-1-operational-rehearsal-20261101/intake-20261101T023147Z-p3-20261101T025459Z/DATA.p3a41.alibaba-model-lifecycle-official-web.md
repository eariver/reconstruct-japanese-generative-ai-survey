# Alibaba Model Studio official lifecycle observation

Status: bounded Discovery-stage source observation; not an Evidence decision.

- Source: [Alibaba Cloud Model Studio — Model lifecycle and updates](https://www.alibabacloud.com/help/en/model-studio/newly-released-models)
- Retrieval route: the repository-owned official-page collector returned HTTP 502 for this page during the fallback run. A direct public Web retrieval of the same first-party page succeeded on 2026-09-08 UTC. The page reported `Last Updated: Sep 02, 2026`.
- Scope: the page is a model-lifecycle table. Its date is the provider/model-service lifecycle date shown by Alibaba; it is not, by itself, a claim about the base model's original upstream release or a later third-party integration.

## W34 rows observed

| Provider/model row | Alibaba lifecycle date | Discovery interpretation |
| --- | --- | --- |
| `wan3.0-video-prime` | 2026-08-20 | in-window Model Studio availability/lifecycle event |
| `kimi-k3` | 2026-08-19 | in-window Model Studio availability/lifecycle event |
| `qwen3.8-27b` | 2026-08-17 | in-window Model Studio availability/lifecycle event |
| `ZHIPU/GLM-5.3` | 2026-08-17 | in-window Model Studio availability/lifecycle event |

## Chronology boundary

These rows are retained as separate provider-distribution/service-availability observations. They must not be collapsed with a base-model release date, a later Runway or other integration, or a later provider announcement. In particular, the in-window `wan3.0-video-prime` Model Studio row is distinct from the later Runway integration represented in the prior inventory.

The page exposes date-level chronology rather than a precise publication timestamp. Downstream Evidence may bind stronger timestamped first-party material if it becomes available; this Discovery observation does not manufacture that precision.
