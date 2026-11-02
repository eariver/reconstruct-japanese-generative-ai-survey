> This page is for version dev.
> For other versions, use one of these documentation indexes:
> - Latest (v1.6.1) (default): https://docs.nvidia.com/dynamo/latest/llms.txt
> - dev: https://docs.nvidia.com/dynamo/dev/llms.txt
> - v1.6.1: https://docs.nvidia.com/dynamo/v1.6.1/llms.txt
> - v1.6.0: https://docs.nvidia.com/dynamo/v1.6.0/llms.txt
> - v1.5.1: https://docs.nvidia.com/dynamo/v1.5.1/llms.txt
> - v1.5.0: https://docs.nvidia.com/dynamo/v1.5.0/llms.txt
> - v1.4.2: https://docs.nvidia.com/dynamo/v1.4.2/llms.txt
> - v1.4.1: https://docs.nvidia.com/dynamo/v1.4.1/llms.txt
> - v1.4.0: https://docs.nvidia.com/dynamo/v1.4.0/llms.txt
> - v1.3.0: https://docs.nvidia.com/dynamo/v1.3.0/llms.txt
> - v1.2.1: https://docs.nvidia.com/dynamo/v1.2.1/llms.txt
> - v1.2.0: https://docs.nvidia.com/dynamo/v1.2.0/llms.txt
> - v1.1.1: https://docs.nvidia.com/dynamo/v1.1.1/llms.txt
> - v1.1.0: https://docs.nvidia.com/dynamo/v1.1.0/llms.txt
> - v1.0.2: https://docs.nvidia.com/dynamo/v1.0.2/llms.txt
> - v1.0.1: https://docs.nvidia.com/dynamo/v1.0.1/llms.txt
> - v1.0.0: https://docs.nvidia.com/dynamo/v1.0.0/llms.txt
> - v0.9.1: https://docs.nvidia.com/dynamo/v-0-9-1/llms.txt
> - v0.9.0: https://docs.nvidia.com/dynamo/v-0-9-0/llms.txt
> - v0.8.1: https://docs.nvidia.com/dynamo/v-0-8-1/llms.txt
> - v0.8.0: https://docs.nvidia.com/dynamo/v-0-8-0/llms.txt
> - v0.7.1: https://docs.nvidia.com/dynamo/v-0-7-1/llms.txt
> - v0.7.0: https://docs.nvidia.com/dynamo/v-0-7-0/llms.txt

> For clean Markdown content of this page, append .md to this URL. For the complete documentation index, see https://docs.nvidia.com/dynamo/llms.txt. For full content including API reference and SDK examples, see https://docs.nvidia.com/dynamo/llms-full.txt.

# DeepSeek-V4.1-Flash

Deploy DeepSeek-V4.1-Flash with NVIDIA Dynamo. The vLLM B200 and GB200 recipes use eight GPUs, sparse-indexer logits, and DSpark speculative decoding. H200 uses 16 GPUs for aggregated serving or eight for disaggregated serving, with CUTLASS MoE, EPLB, and DSpark-3. SGLang recipes are also available for GB200.

Choose your deployment target

Framework

vLLM

<input type="radio" id="recipe-framework-sglang" name="recipe-framework" value="sglang" />

SGLang

GPU

GB200

<input type="radio" id="recipe-sku-b200" name="recipe-sku" value="b200" />

B200

<input type="radio" id="recipe-sku-h200" name="recipe-sku" value="h200" />

H200

Topology

Aggregated

<input type="radio" id="recipe-variant-disagg" name="recipe-variant" value="disagg" />

Disaggregated

**Model** deepseek-ai/DeepSeek-V4.1-Flash **GPUs** 8x GB200 **Layout** Two TP4 workers **Configuration** MXFP4 sparse-indexer KV and sparse-indexer logits

**Model** deepseek-ai/DeepSeek-V4.1-Flash **GPUs** 8x GB200 **Layout** One TP4 prefill worker and one TP4 decode worker **Configuration** MXFP4 sparse-indexer KV and sparse-indexer logits

**Model** deepseek-ai/DeepSeek-V4.1-Flash **GPUs** 8x B200 **Layout** Two TP4 workers **Configuration** MXFP4 sparse-indexer KV and sparse-indexer logits

**Model** deepseek-ai/DeepSeek-V4.1-Flash **GPUs** 8x B200 **Layout** One TP4 prefill worker and one TP4 decode worker **Configuration** MXFP4 sparse-indexer KV and sparse-indexer logits

**Model** deepseek-ai/DeepSeek-V4.1-Flash **GPUs** 16x H200 **Layout** Four TP4 workers **Configuration** CUTLASS MoE, EPLB, DSpark-3

**Model** deepseek-ai/DeepSeek-V4.1-Flash **GPUs** 8x H200 **Layout** One TP4 prefill worker and one TP4 decode worker **Configuration** CUTLASS MoE, EPLB, DSpark-3

**Status** No SGLang recipe for H200. Select vLLM or GB200.

**Model** deepseek-ai/DeepSeek-V4.1-Flash **GPUs** 8x GB200 **Layout** Two TP4 workers **Configuration** TP4 + EP4

**Model** deepseek-ai/DeepSeek-V4.1-Flash **GPUs** 8x GB200 **Layout** One TP4 prefill worker and one TP4 decode worker **Configuration** TP4 + EP4

**Status** No SGLang recipe for B200. Select vLLM or GB200.

## Prerequisites

* A Kubernetes cluster with a compatible Dynamo operator and eight B200/GB200 GPUs, 16 H200 GPUs for aggregated serving, or eight H200 GPUs for disaggregated serving.
* Per frontend: 16 CPU cores and 128 GiB of host memory on B200/GB200, or 4 CPU cores and 8 GiB on H200.
* Per worker: four GPUs, 16 CPU cores, 512 GiB of host memory, 64 GiB of ephemeral storage, and capacity for a 200 GiB shared-memory volume.
* A populated ReadWriteMany model-cache PVC, referenced as `shared-model-cache` by the recipes.

The worker memory and shared-memory requests match the tested configuration.

* Kustomize v5.8.1 and a filled [cluster Kustomization](https://github.com/ai-dynamo/dynamo/blob/main/recipes/templates/kustomize/README.md) for placement, cache binding, registry credentials, and networking.
* ARM64 worker nodes for GB200 or AMD64 worker nodes for B200/H200.

- The recipe Kustomization supplies UCX transport settings. For B200 and GB200,
  add the cluster's RDMA device and interface settings.

* Place the prefill and decode workers on separate RDMA-capable H200 nodes, with
  four GPUs per worker. The recipe requests four `rdma/ib` devices per worker
  and selects their assigned NICs at startup. Configure the SR-IOV network
  device plugin to provide `rdma/ib`, `PCIDEVICE_RDMA_IB`, and
  `PCIDEVICE_RDMA_IB_INFO`. Do not set a static `UCX_NET_DEVICES` value.

- NVIDIA DRA and ComputeDomain support, with the workers placed in one NVLink clique.

## Deploy

Set the namespace and populate the cache using the [model-cache manifests](https://github.com/ai-dynamo/dynamo/tree/main/recipes/deepseek-v4.1-flash/model-cache). The download Job pins snapshot `dba1be0a40aa45a94ad051997016db3960a90277`.

```bash
export NAMESPACE=your-namespace
export CLUSTER_CONFIG=/path/to/your/filled-cluster-kustomization
```

Render the selected configuration to a local file:

```bash
kustomize build recipes/deepseek-v4.1-flash/vllm/agg-gb200-agentic > "${CLUSTER_CONFIG}/recipe.yaml"
```

[Source Kustomization](https://github.com/ai-dynamo/dynamo/blob/main/recipes/deepseek-v4.1-flash/vllm/agg-gb200-agentic/kustomization.yaml)

```bash
kustomize build recipes/deepseek-v4.1-flash/vllm/disagg-gb200-agentic > "${CLUSTER_CONFIG}/recipe.yaml"
```

[Source Kustomization](https://github.com/ai-dynamo/dynamo/blob/main/recipes/deepseek-v4.1-flash/vllm/disagg-gb200-agentic/kustomization.yaml)

```bash
kustomize build recipes/deepseek-v4.1-flash/vllm/agg-b200-agentic > "${CLUSTER_CONFIG}/recipe.yaml"
```

[Source Kustomization](https://github.com/ai-dynamo/dynamo/blob/main/recipes/deepseek-v4.1-flash/vllm/agg-b200-agentic/kustomization.yaml)

```bash
kustomize build recipes/deepseek-v4.1-flash/vllm/agg-h200-agentic > "${CLUSTER_CONFIG}/recipe.yaml"
```

[Source Kustomization](https://github.com/ai-dynamo/dynamo/blob/main/recipes/deepseek-v4.1-flash/vllm/agg-h200-agentic/kustomization.yaml)

```bash
kustomize build recipes/deepseek-v4.1-flash/vllm/disagg-h200-agentic > "${CLUSTER_CONFIG}/recipe.yaml"
```

[Source Kustomization](https://github.com/ai-dynamo/dynamo/blob/main/recipes/deepseek-v4.1-flash/vllm/disagg-h200-agentic/kustomization.yaml)

```bash
kustomize build recipes/deepseek-v4.1-flash/vllm/disagg-b200-agentic > "${CLUSTER_CONFIG}/recipe.yaml"
```

[Source Kustomization](https://github.com/ai-dynamo/dynamo/blob/main/recipes/deepseek-v4.1-flash/vllm/disagg-b200-agentic/kustomization.yaml)

Use the [cluster Kustomization guide](https://github.com/ai-dynamo/dynamo/blob/main/recipes/templates/kustomize/README.md) to configure node placement, registry access, model storage, and networking. Set its single `resources` entry to `recipe.yaml`, then apply:

```bash
set -o pipefail
kustomize build --load-restrictor LoadRestrictionsNone "${CLUSTER_CONFIG}" | \
  kubectl apply --dry-run=server -f - -n "${NAMESPACE}"
kustomize build --load-restrictor LoadRestrictionsNone "${CLUSTER_CONFIG}" | \
  kubectl apply -f - -n "${NAMESPACE}"
```

```bash
kubectl apply -f recipes/deepseek-v4.1-flash/sglang/agg-gb200/deploy.yaml -n "${NAMESPACE}"
```

```bash
kubectl apply -f recipes/deepseek-v4.1-flash/sglang/disagg-gb200/deploy-generic.yaml -n "${NAMESPACE}"
```

The [GKE variant](https://github.com/ai-dynamo/dynamo/blob/main/recipes/deepseek-v4.1-flash/sglang/disagg-gb200/deploy-gke-rdma.yaml) supplies provider RDMA settings.

## Smoke Test

Forward the selected deployment's frontend Service:

```bash
kubectl port-forward svc/dsv41-flash-vllm-gb200-agg-agentic-frontend 8000:8000 -n "${NAMESPACE}"
```

```bash
kubectl port-forward svc/dsv41-flash-vllm-gb200-disagg-agentic-frontend 8000:8000 -n "${NAMESPACE}"
```

```bash
kubectl port-forward svc/dsv41-flash-vllm-b200-agg-agentic-frontend 8000:8000 -n "${NAMESPACE}"
```

```bash
kubectl port-forward svc/dsv41-flash-vllm-h200-agg-agentic-frontend 8000:8000 -n "${NAMESPACE}"
```

```bash
kubectl port-forward svc/dsv41-flash-vllm-h200-disagg-agentic-frontend 8000:8000 -n "${NAMESPACE}"
```

```bash
kubectl port-forward svc/dsv41-flash-vllm-b200-disagg-agentic-frontend 8000:8000 -n "${NAMESPACE}"
```

```bash
kubectl port-forward svc/deepseek-v41-flash-sglang-gb200-agg-frontend 8000:8000 -n "${NAMESPACE}"
```

```bash
kubectl port-forward svc/deepseek-v41-flash-sglang-gb200-disagg-frontend 8000:8000 -n "${NAMESPACE}"
```

Send a request in a separate terminal:

```bash
curl -sS http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"deepseek-ai/DeepSeek-V4.1-Flash","messages":[{"role":"user","content":"Reply with exactly: READY"}],"temperature":0,"max_tokens":512}'
```

Check that the response contains an answer.

For disaggregated SGLang, HTTP 200 can still contain `content: null` and zero completion tokens when KV transfer fails. Require a nonempty answer. The generic manifest forces Mooncake TCP with `MC_FORCE_TCP=1`; the GKE variant uses RDMA. If you select the NVLink fabric path, place both workers in one NVLink clique. A split can log `cuMemImportFromShareableHandle failed: 400` and return an empty answer.

## Measured Performance

Results for the agentic workload (64K input tokens, 400 output tokens), using
eight B200/GB200 GPUs, 16 H200 GPUs for aggregated serving, or eight H200 GPUs for disaggregated serving. Output throughput includes reasoning tokens.

| Workload                        | Recipe                                        | Framework | SKU   | Concurrency | System output tok/s/GPU | User output tok/s (P50) | TTFT P50 (ms) | TTFT P90 (ms) |
| ------------------------------- | --------------------------------------------- | --------- | ----- | ----------: | ----------------------: | ----------------------: | ------------: | ------------: |
| Agentic (64K input, 400 output) | Aggregated (2 × TP4)                          | vLLM      | B200  |         168 |                  990.57 |                   54.69 |        178.66 |      3,068.28 |
| Agentic (64K input, 400 output) | Disaggregated (1 prefill, 1 decode; TP4 each) | vLLM      | B200  |         184 |                1,087.71 |                   82.12 |        135.12 |     90,076.83 |
| Agentic (64K input, 400 output) | Aggregated (2 × TP4)                          | vLLM      | GB200 |         168 |                  953.08 |                   51.83 |        286.75 |      3,524.82 |
| Agentic (64K input, 400 output) | Disaggregated (1 prefill, 1 decode; TP4 each) | vLLM      | GB200 |         168 |                1,154.87 |                   80.85 |        169.02 |     57,116.54 |
| Agentic (64K input, 400 output) | Aggregated (4 × TP4)                          | vLLM      | H200  |          80 |                  209.18 |                   51.32 |        171.29 |      6,368.76 |
| Agentic (64K input, 400 output) | Disaggregated (1 prefill, 1 decode; TP4 each) | vLLM      | H200  |          64 |                  359.41 |                   50.63 |        177.59 |     35,043.23 |

The catalog recommends GB200 disaggregated for maximum measured system output
throughput per GPU at these operating points.

For GB200 at the selected concurrency, disaggregated serving delivers 21%
more output tok/s/GPU and 56% more p50 user tok/s. TTFT p90 rises from
3.52 s to 57.12 s.

[Benchmark instructions and full TTFT/ITL distributions](https://github.com/ai-dynamo/dynamo/blob/main/recipes/deepseek-v4.1-flash/perf/README.md).

No published benchmark results.

## Configurations

All vLLM targets use expert parallelism, expert load balancing (EPLB), KV-aware
routing, and DSpark with three draft tokens and block verification. Adaptive
verification is disabled. They serve text using the `deepseek_v41` reasoning
and tool-call parsers. In the table below, P/D means prefill/decode.

| Setting                         | B200 / GB200 aggregated    | B200 disaggregated           | GB200 disaggregated               | H200 aggregated           | H200 disaggregated        |
| ------------------------------- | -------------------------- | ---------------------------- | --------------------------------- | ------------------------- | ------------------------- |
| MoE backend                     | `deep_gemm_mega_moe`       | `deep_gemm_mega_moe`         | `deep_gemm_mega_moe`              | `flashinfer_cutlass`      | `flashinfer_cutlass`      |
| KV cache dtype                  | `fp8_ds_mla`               | Auto (`nvfp4_ds_mla`)        | `fp8_ds_mla`                      | `fp8_ds_mla`              | `fp8_ds_mla`              |
| Attention backend               | `FLASHMLA_MEGA_ATTN_DSV41` | `FLASHMLA_MEGA_ATTN_DSV41`   | `FLASHMLA_MEGA_ATTN_DSV41`        | Runtime default           | Runtime default           |
| Sparse indexer                  | MXFP4 KV, sparse logits    | MXFP4 KV, sparse logits      | MXFP4 KV, sparse logits           | Runtime default           | Runtime default           |
| EPLB communicator               | `torch_gloo`               | `torch_gloo`                 | `torch_gloo`                      | Runtime default           | Runtime default           |
| Max context tokens              | 1,048,576                  | Runtime default              | 1,048,576                         | Model default (1,048,576) | Model default (1,048,576) |
| Max sequences                   | 1,024                      | Runtime default              | 1,024                             | 1,024                     | 1,024                     |
| Max batched tokens              | 16,384                     | 32,768 P / runtime default D | 16,384                            | 8,192                     | 8,192                     |
| GPU memory utilization          | 0.92                       | Runtime default              | 0.92                              | 0.92                      | 0.92                      |
| KV block size                   | 128                        | Runtime default              | 128                               | Runtime default           | Runtime default           |
| Max CUDA graph capture size     | 512                        | 512 P / 1,024 D              | 512 P / 1,024 D                   | 512                       | 512                       |
| Long-prefill threshold          | Unset                      | 4,096 P                      | 4,096 P                           | Unset                     | Unset                     |
| Prefix-cache retention interval | 1,024                      | 1,024                        | 1,024                             | 1,024                     | 1,024                     |
| Conditional disaggregation      | N/A                        | `isl_bounding`               | Enabled, default policy           | N/A                       | `isl_bounding`            |
| KV transfer                     | N/A                        | NIXL/UCX over InfiniBand     | NIXL/UCX within one NVLink clique | N/A                       | NIXL/UCX over InfiniBand  |

Aggregated targets and H200 disaggregated set the decode-active-request weight
to 50. B200 and H200 disaggregated use `isl_bounding` with effective-input
threshold 2,048, input-ratio threshold 0.70, and decode-busy threshold 0.50.
With the measured image, both B200 disaggregated workers logged
`Using DeepSeek's nvfp4_ds_mla KV cache format` when `kv_cache_dtype=auto`.
See the linked Kustomize sources for the complete flags and container images.

The SGLang GB200 targets use the `dev.1` runtime. Aggregated serving enables
DSpark; disaggregated serving uses Mooncake without speculative decoding.

## Source

[Recipe sources](https://github.com/ai-dynamo/dynamo/tree/main/recipes/deepseek-v4.1-flash)