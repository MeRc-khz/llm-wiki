---
title: RunPod Flash
created: 2026-08-24
updated: 2026-08-24
type: entity
tags: [infrastructure, inference, automation, model]
sources:
  - raw/articles/runpod-flash-overview.md
  - raw/articles/runpod-flash-quickstart.md
  - raw/articles/runpod-flash-create-endpoints.md
  - raw/articles/runpod-flash-parameters.md
  - raw/articles/runpod-flash-gpu-types.md
  - raw/articles/runpod-flash-pricing.md
  - raw/articles/runpod-flash-apps-overview.md
  - raw/articles/runpod-flash-apps-deploy.md
  - raw/articles/runpod-flash-apps-requests.md
  - raw/articles/runpod-flash-custom-docker.md
  - raw/articles/runpod-flash-execution-model.md
  - raw/articles/runpod-flash-storage.md
  - raw/articles/runpod-flash-best-practices.md
  - raw/articles/runpod-flash-tutorial-sdxl.md
  - raw/articles/runpod-flash-tutorial-text-gen.md
  - raw/articles/runpod-flash-tutorial-rest-api.md
confidence: high
contested: false
---

# RunPod Flash

RunPod Flash is a Python SDK for developing cloud-native AI/ML applications where you define everything — hardware, remote functions, and dependencies — using local code. You write `@Endpoint`-decorated Python functions on your local machine, and Flash automatically handles GPU/CPU provisioning and worker scaling on [RunPod Serverless](https://docs.runpod.io/serverless/overview).

## Why It Matters

For bzr-dial and Paperclip, Flash lets us write our own GPU generation endpoints (image generation, music generation, text-to-speech, etc.) without managing servers. We can deploy custom Python functions that run on NVIDIA GPUs, scale automatically, and bill per-second with no charges when idle. This is the infrastructure layer for any [[comfyui]] or [[makeufamous]] AI generation pipeline that needs to scale beyond the CPU-only server.

## Quick Start

```bash
pip install runpod-flash
flash login  # authenticates with RunPod API key
```

```python
import asyncio
from runpod_flash import Endpoint, GpuType

@Endpoint(name="hello-gpu", gpu=GpuType.NVIDIA_GEFORCE_RTX_4090, dependencies=["torch"])
async def hello():
    import torch
    gpu_name = torch.cuda.get_device_name(0)
    return {"gpu": gpu_name}

asyncio.run(hello())
```

## Endpoint Types

Flash supports four endpoint patterns:

### 1. Queue-Based Endpoints

Use `@Endpoint(...)` as a decorator for batch processing and async workloads. Each function gets its own endpoint with dedicated workers.

```python
@Endpoint(
    name="image-processor",
    gpu=GpuType.NVIDIA_GEFORCE_RTX_4090,
    workers=(0, 5),
    dependencies=["torch", "pillow"]
)
async def process_image(image_data: dict) -> dict:
    import torch
    from PIL import Image
    return {"processed": True}
```

**API routes**: `/run` (async, returns job ID), `/runsync` (sync, waits for result), `/status/{id}` (check job).

**Request format**: `{"input": {...}}` — input is wrapped in an `input` key.

### 2. Load-Balanced Endpoints

Use `Endpoint(...)` as an instance with route decorators for HTTP APIs. Multiple routes share the same workers.

```python
api = Endpoint(
    name="inference-api",
    gpu=GpuType.NVIDIA_GEFORCE_RTX_4090,
    workers=(1, 5),
    dependencies=["torch"]
)

@api.post("/predict")
async def predict(data: dict) -> dict:
    import torch
    return {"prediction": "result"}

@api.get("/health")
async def health():
    return {"status": "ok"}
```

**API routes**: Custom paths (e.g., `/predict`, `/health`). Direct JSON payload (no `{"input": {...}}` wrapper).

**URL pattern**: `https://{endpoint_id}.api.runpod.ai/{path}`

### 3. Custom Docker Images

Deploy pre-built Docker images (vLLM, ComfyUI, Automatic1111, or your own) and interact as a client.

```python
vllm = Endpoint(
    name="vllm-server",
    image="runpod/worker-vllm:stable-cuda12.1.0",
    gpu=GpuType.NVIDIA_A100_80GB_PCIe,
    env={"MODEL_NAME": "meta-llama/Llama-3.2-3B-Instruct"}
)

result = await vllm.post("/v1/completions", {"prompt": "Hello"})
```

Official RunPod worker images: `runpod/worker-vllm`, `runpod/worker-a1111:stable`, `runpod/worker-comfy`.

### 4. Existing Endpoints

Connect to an already-deployed RunPod endpoint by ID:

```python
ep = Endpoint(id="abc123")
job = await ep.run({"prompt": "hello"})
await job.wait()
print(job.output)
```

## Key Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | required | Endpoint name (identifies it on RunPod) |
| `gpu` | `GpuGroup`/`GpuType`/list | `GpuGroup.ANY` | GPU hardware selection |
| `cpu` | `str`/`CpuInstanceType` | `None` | CPU instance (mutually exclusive with `gpu`) |
| `workers` | `int` or `(min, max)` | `(0, 1)` | Worker scaling config |
| `idle_timeout` | `int` | `60` | Seconds before scaling down idle workers |
| `dependencies` | `list[str]` | `None` | Python packages to install on worker |
| `system_dependencies` | `list[str]` | `None` | System packages (apt) |
| `env` | `dict[str, str]` | `None` | Environment variables for workers |
| `volume` | `NetworkVolume`/list | `None` | Persistent network storage at `/runpod-volume/` |
| `datacenter` | `DataCenter`/list | `None` (all DCs) | Datacenter selection |
| `gpu_count` | `int` | `1` | GPUs per worker |
| `execution_timeout_ms` | `int` | `0` (no limit) | Max execution time per job |
| `flashboot` | `bool` | `True` | Fast cold-start via pre-loaded images |
| `image` | `str` | `None` | Custom Docker image |
| `scaler_type` | `ServerlessScalerType` | auto | Scaling strategy |
| `min_cuda_version` | `str`/`CudaVersion` | `"12.8"` | Min CUDA for GPU selection |
| `python_version` | `str` | local Python | Worker Python version |

## Available GPUs

### GPU Pools (`GpuGroup`)

| GpuGroup | GPUs Included | VRAM |
|----------|---------------|------|
| `ANY` | Any available | Varies |
| `AMPERE_16` | RTX A4000, RTX 4000 Ada, RTX 2000 Ada | 16GB |
| `AMPERE_24` | RTX A4500, RTX A5000, RTX 3090 | 20-24GB |
| `ADA_24` | L4, RTX 4090 | 24GB |
| `ADA_32_PRO` | RTX 5090 | 32GB |
| `AMPERE_48` | A40, RTX A6000 | 48GB |
| `ADA_48_PRO` | L40S, L40, RTX 6000 Ada | 48GB |
| `AMPERE_80` | A100 80GB PCIe, A100-SXM4-80GB | 80GB |
| `ADA_80_PRO` | H100 80GB HBM3 | 80GB |
| `BLACKWELL_96` | RTX PRO 6000 Blackwell | 96GB |
| `HOPPER_141` | H200 | 141GB |
| `BLACKWELL_180` | B200 | 180GB |

### Specific GPU Types (`GpuType`)

Key types: `NVIDIA_GEFORCE_RTX_4090` (24GB, Ada), `NVIDIA_GEFORCE_RTX_5090` (32GB, Blackwell), `NVIDIA_A100_80GB_PCIe` (80GB, Ampere), `NVIDIA_H100_80GB_HBM3` (80GB, Hopper), `NVIDIA_H200` (141GB, Hopper), `NVIDIA_B200` (180GB, Blackwell).

See raw/articles/runpod-flash-gpu-types.md for the full list.

### Fallback Strategy

Mix `GpuType` and `GpuGroup` for robust availability:

```python
@Endpoint(
    name="flexible",
    gpu=[
        GpuType.NVIDIA_A100_80GB_PCIe,  # Try first
        GpuGroup.AMPERE_48,             # Pool fallback
        GpuGroup.ANY                    # Ultimate fallback
    ]
)
async def infer(data: dict) -> dict: ...
```

## Datacenters

15 datacenters available. GPU endpoints can deploy to all; CPU endpoints restricted to `EU_RO_1`.

| Location | DataCenter |
|----------|------------|
| US - California | `US_CA_2` |
| US - Georgia | `US_GA_2` |
| US - Illinois | `US_IL_1` |
| US - Kansas | `US_KS_2` |
| US - Maryland | `US_MD_1` |
| US - Missouri | `US_MO_1` / `US_MO_2` |
| US - North Carolina | `US_NC_1` / `US_NC_2` |
| US - Nebraska | `US_NE_1` |
| US - Washington | `US_WA_1` |
| Europe - Czech Republic | `EU_CZ_1` |
| Europe - Romania | `EU_RO_1` |
| Europe - Iceland | `EUR_IS_1` |
| Europe - Norway | `EUR_NO_1` |

## Pricing

Per-second billing. You pay for: (1) worker start time (container init + dependency load), (2) execution time (running your function), (3) idle timeout duration (worker stays active after request, configurable via `idle_timeout`).

**No charges when code isn't running.** Workers that are scaled down (idle) don't incur costs.

**Cost optimization**:
- Choose smallest GPU that fits your workload (24GB VRAM → RTX 4090 or L4, not A100)
- Use `workers=(0, N)` to scale to zero when idle
- Use CPU workers for non-GPU tasks (`cpu="cpu5c-2-4"`)
- Set lower `idle_timeout` for infrequent traffic
- Limit `workers` to prevent runaway scaling

## Execution Model

**What runs where**: `@Endpoint`-decorated function bodies run on RunPod workers. Everything else (control flow, local code) runs on your machine.

**Worker lifecycle**: Initializing → Running → (idle for `idle_timeout` seconds) → Idle (scaled down). Workers auto-scale based on demand between `workers=(min, max)`.

**Cold start** (10-60s): Provision new worker, start container, execute function. Happens on first call or after all workers scale down.

**Warm start** (~1s + function time): Route to already-running idle worker. Configured via `workers=(1, N)` to keep at least one worker warm.

**Endpoint naming**: Same name + same config = reuse. Same name + different config = auto-update. New name = new endpoint.

**Import rule**: pip-installed packages must be imported **inside** the function body, not at the top of the file. Local project modules can be imported at the top — Flash ships their source to the worker.

## Flash Apps (Production Deployments)

### Development Workflow

1. `flash init PROJECT_NAME` — create project with example workers
2. Write `@Endpoint` functions
3. `flash dev` — local dev server; endpoint functions run on Runpod workers
4. `flash deploy` — build artifact, upload, provision Serverless endpoints
5. `flash deploy --env staging` / `--env production` — deploy to specific environments

### Build & Deploy

`flash deploy` packages code + dependencies + manifest into `.flash/artifact.tar.gz` (max 1.5GB), uploads to RunPod, provisions independent Serverless endpoints.

**Deployment architecture**: One `Endpoint` class = one Serverless endpoint. Queue-based endpoints create one per function. Load-balanced endpoints serve multiple routes from one endpoint.

**Cross-endpoint communication**: Endpoints can call each other. Import the target function inside your function body; Flash generates dispatch stubs and uses the RunPod GraphQL API for service discovery.

**Calling deployed endpoints**: After deploy, call from scripts directly — Flash resolves app context from project directory. Override with `FLASH_APP` and `FLASH_ENV` env vars.

### Post-Deployment URLs

- **Queue-based**: `https://api.runpod.ai/v2/{endpoint_id}/run` or `/runsync`
- **Load-balanced**: `https://{endpoint_id}.api.runpod.ai/{route_path}`

Authentication: Bearer token with RunPod API key.

## Storage

**Network volumes** mount at `/runpod-volume/`. One volume per datacenter. Used for sharing large models across workers, persisting data between runs, caching.

```python
vol = NetworkVolume(name="model-cache", size=100, datacenter=DataCenter.US_GA_2)

@Endpoint(
    name="model-server",
    gpu=GpuGroup.ANY,
    datacenter=DataCenter.US_GA_2,
    volume=vol
)
async def serve(data: dict) -> dict:
    model = load_model("/runpod-volume/models/bert")
    ...
```

**Container disk**: Ephemeral, erased when worker stops. Use network volumes for persistence.

## Tutorials (Raw Reference)

Three official tutorials with complete code:

1. **Image generation with SDXL** — Stable Diffusion XL on 24GB GPUs, base64 output. See `raw/articles/runpod-flash-tutorial-sdxl.md`
2. **Text generation with transformers** — HuggingFace transformers pipeline. See `raw/articles/runpod-flash-tutorial-text-gen.md`
3. **REST API with load balancer** — Production HTTP API with custom routes. See `raw/articles/runpod-flash-tutorial-rest-api.md`

## Limitations

- Runs natively on macOS and Linux. Windows requires WSL2.
- CPU endpoints restricted to `EU_RO_1` datacenter.
- Rapid scaling can hit account worker thresholds — contact RunPod support to increase capacity.
- 1.5GB deployment artifact limit.
- Live execution local module payload capped at 8 MiB (use `flash deploy` for larger).
- `.env` values are local-only; must use `env` parameter for deployed workers.

## Related Wiki Pages

- [[comfyui]] — Currently CPU-only on our server; Flash could provide GPU-backed ComfyUI endpoints
- [[makeufamous]] — AI audition judges could run as Flash GPU endpoints
- [[gpu-generation-endpoints]] — Patterns for writing our own GPU generation endpoints with Flash
- [[lawnczar]] — Potential GPU endpoints for map rendering or geospatial processing
