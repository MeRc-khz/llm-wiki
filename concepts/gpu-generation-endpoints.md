---
title: GPU Generation Endpoints with Flash
created: 2026-08-24
updated: 2026-08-24
type: concept
tags: [inference, infrastructure, model, automation]
sources:
  - raw/articles/runpod-flash-create-endpoints.md
  - raw/articles/runpod-flash-parameters.md
  - raw/articles/runpod-flash-gpu-types.md
  - raw/articles/runpod-flash-custom-docker.md
  - raw/articles/runpod-flash-tutorial-sdxl.md
  - raw/articles/runpod-flash-tutorial-text-gen.md
  - raw/articles/runpod-flash-tutorial-rest-api.md
  - raw/articles/runpod-flash-apps-requests.md
  - raw/articles/runpod-flash-pricing.md
confidence: high
contested: false
---

# GPU Generation Endpoints with Flash

Patterns and recipes for writing our own GPU generation endpoints using [[runpod-flash]]. This page covers the architectural decisions, code patterns, and deployment strategies for running AI generation workloads (images, text, audio, video) on RunPod's GPU infrastructure.

## Endpoint Pattern Selection

| Use Case | Pattern | Why |
|----------|---------|-----|
| Image/music generation API | Load-balanced | HTTP routes, direct JSON, low-latency |
| Batch processing (many prompts) | Queue-based | Async, job status polling, scales to zero |
| Pre-built model server (vLLM, ComfyUI) | Custom Docker image | Deploy the official image, call as client |
| Script-based one-off generation | `@Endpoint` decorator | Simplest, runs from local script |

## Pattern 1: Image Generation Endpoint (SDXL)

Queue-based endpoint for generating images with Stable Diffusion XL. Returns base64-encoded PNG.

```python
from runpod_flash import Endpoint, GpuGroup

@Endpoint(
    name="image-gen-sdxl",
    gpu=[GpuGroup.ADA_24, GpuGroup.AMPERE_24],  # 24GB GPUs (4090, L4, A5000)
    workers=(0, 3),
    idle_timeout=900,  # 15 min — keep models warm for batch jobs
    dependencies=["diffusers", "torch", "transformers", "accelerate"]
)
def generate_image(prompt, negative_prompt="", num_steps=30, guidance_scale=7.5):
    import torch
    from diffusers import StableDiffusionXLPipeline
    from io import BytesIO
    import base64

    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant="fp16"
    ).to("cuda")

    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=num_steps,
        guidance_scale=guidance_scale,
        height=1024,
        width=1024
    ).images[0]

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return {"image_base64": base64.b64encode(buffered.getvalue()).decode()}
```

**Call it** (after `flash deploy`):
```bash
curl -X POST https://api.runpod.ai/v2/{endpoint_id}/runsync \
    -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"input": {"prompt": "a cool cat in sunglasses, 1024x1024"}}'
```

## Pattern 2: REST API with Load Balancer

Multiple routes sharing one endpoint. Good for a generation service with health check, text-to-image, and image-to-image.

```python
from runpod_flash import Endpoint, GpuType

api = Endpoint(
    name="gen-api",
    gpu=GpuType.NVIDIA_GEFORCE_RTX_4090,
    workers=(1, 5),  # always keep 1 warm
    idle_timeout=300,
    dependencies=["diffusers", "torch", "transformers"]
)

@api.post("/generate")
async def generate(prompt: str, negative: str = ""):
    import torch
    from diffusers import StableDiffusionXLPipeline
    from io import BytesIO
    import base64

    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16
    ).to("cuda")

    image = pipe(prompt=prompt, negative_prompt=negative).images[0]
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return {"image": base64.b64encode(buffered.getvalue()).decode()}

@api.get("/health")
async def health():
    return {"status": "ok", "gpu": "available"}
```

**Call it**:
```bash
# Direct JSON payload — no {"input": {...}} wrapper
curl -X POST https://{endpoint_id}.api.runpod.ai/generate \
    -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "cyberpunk city at night"}'
```

## Pattern 3: Custom Docker Image (vLLM)

Deploy a pre-built inference server and call it as a client. No Python function code needed.

```python
from runpod_flash import Endpoint, GpuType

vllm = Endpoint(
    name="vllm-llama",
    image="runpod/worker-vllm:stable-cuda12.1.0",
    gpu=GpuType.NVIDIA_A100_80GB_PCIe,
    workers=(0, 3),
    env={
        "MODEL_NAME": "meta-llama/Llama-3.2-3B-Instruct",
        "MAX_MODEL_LEN": "4096",
        "GPU_MEMORY_UTILIZATION": "0.9",
        "MAX_CONCURRENCY": "30",
    }
)

# Call it
result = await vllm.post("/v1/completions", {"prompt": "Hello world", "max_tokens": 100})
models = await vllm.get("/v1/models")
```

## Pattern 4: ComfyUI Worker

Deploy the official RunPod ComfyUI worker image for GPU-backed ComfyUI generation:

```python
from runpod_flash import Endpoint, GpuType

comfyui = Endpoint(
    name="comfyui-gpu",
    image="runpod/worker-comfy",
    gpu=GpuType.NVIDIA_GEFORCE_RTX_4090,
    workers=(0, 2),
    idle_timeout=600,
    env={
        "HF_TOKEN": "your_token",
    }
)

# Submit a workflow
job = await comfyui.run({
    "input": {
        "workflow": {...},  # ComfyUI API format workflow JSON
    }
})
await job.wait()
print(job.output)
```

This gives us GPU-backed ComfyUI as a scalable endpoint, complementing our existing CPU-only [[comfyui]] setup on the server.

## GPU Selection Guide

| Model/Workload | Min VRAM | Recommended GPU | GpuGroup |
|----------------|----------|-----------------|----------|
| SDXL (1024x1024) | 16GB | RTX 4090, L4 | `ADA_24` |
| SD 1.5 (512x512) | 8GB | RTX 4090, A5000 | `ADA_24` or `AMPERE_24` |
| 7B text model (inference) | 16GB | RTX 4090, L4 | `ADA_24` |
| 13B text model | 40GB | A40, RTX A6000 | `AMPERE_48` |
| 70B text model (4-bit) | 48GB | A100 80GB | `AMPERE_80` |
| MusicGen audio | 16GB | RTX 4090, L4 | `ADA_24` |
| Multi-GPU training | 4×80GB | A100 80GB ×4 | `AMPERE_80` + `gpu_count=4` |

## Cost Optimization

1. **Scale to zero**: `workers=(0, N)` — no charges when idle
2. **Match VRAM to model**: Don't use A100 for a 7B model that fits on a 4090
3. **Use GPU pools**: `GpuGroup.ADA_24` gives flexibility across 4090/L4
4. **Keep warm during bursts**: `workers=(1, N)` with `idle_timeout=300` for production
5. **Network volume for models**: Avoid re-downloading 7GB models on every cold start

## Network Volume for Model Caching

```python
from runpod_flash import Endpoint, GpuGroup, DataCenter, NetworkVolume

vol = NetworkVolume(name="model-cache", size=200, datacenter=DataCenter.US_GA_2)

@Endpoint(
    name="cached-image-gen",
    gpu=GpuGroup.ADA_24,
    datacenter=DataCenter.US_GA_2,
    volume=vol,
    workers=(0, 3),
    idle_timeout=900,
    dependencies=["diffusers", "torch", "transformers", "accelerate"]
)
def generate(prompt: str):
    import torch
    from diffusers import StableDiffusionXLPipeline

    # Load from network volume instead of downloading
    pipe = StableDiffusionXLPipeline.from_pretrained(
        "/runpod-volume/models/sdxl-base",
        torch_dtype=torch.float16
    ).to("cuda")
    ...
```

## HTTP Request Reference

### Queue-Based (async)

```bash
# Submit job
curl -X POST https://api.runpod.ai/v2/{endpoint_id}/run \
    -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"input": {"prompt": "hello"}}'
# → {"id": "job-abc-123", "status": "IN_QUEUE"}

# Check status
curl https://api.runpod.ai/v2/{endpoint_id}/status/job-abc-123 \
    -H "Authorization: Bearer $RUNPOD_API_KEY"
# → {"id": "job-abc-123", "status": "COMPLETED", "output": {...}}
```

### Queue-Based (sync, 60s default timeout)

```bash
curl -X POST https://api.runpod.ai/v2/{endpoint_id}/runsync \
    -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"input": {"prompt": "hello"}}'
# → {"id": "job-abc-123", "status": "COMPLETED", "output": {...}}
```

### Load-Balanced (direct)

```bash
curl -X POST https://{endpoint_id}.api.runpod.ai/generate \
    -H "Authorization: Bearer $RUNPOD_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "hello"}'
# → {"image": "base64..."}
```

## Job Status States

| Status | Description |
|--------|-------------|
| `IN_QUEUE` | Waiting for available worker |
| `IN_PROGRESS` | Worker executing your function |
| `COMPLETED` | Finished successfully |
| `FAILED` | Error occurred |

## Related Wiki Pages

- [[runpod-flash]] — Full entity page with complete parameter reference, datacenters, and CLI
- [[comfyui]] — Current CPU-only ComfyUI setup that could be GPU-accelerated via Flash
- [[makeufamous]] — AI audition judges as Flash GPU endpoints
- [[mlops/inference]] — vLLM serving and quantization patterns
