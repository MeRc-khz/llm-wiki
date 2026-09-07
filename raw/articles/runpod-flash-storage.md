---
source_url: https://docs.runpod.io/flash/configuration/storage
ingested: 2026-08-24
sha256: 4d6e0baf54a7a510d9528096bb6caeef05eaf6caa5935f76b18577be01cd7e2b
media_type: article
---

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.runpod.io/llms.txt
> Use this file to discover all available pages before exploring further.

# Storage

> Understand container disk and network volume storage for Flash workloads. Review configuration and usage details for Runpod Flash.

export const WorkerContainerDiskTooltip = () => {
  return <Tooltip headline="Container disk" tip="Temporary storage that exists only while a worker is running, and is completely lost when the worker is stopped or deleted." cta="Learn more about container disks" href="/serverless/storage/overview#container-disk">container disk</Tooltip>;
};

export const NetworkVolumesTooltip = () => {
  return <Tooltip headline="Network volume" tip="Persistent storage that exists independently of your other compute resources. Can be attached to multiple Pods or Serverless endpoints to share data between machines." cta="Learn more about network volumes" href="/storage/network-volumes">network volumes</Tooltip>;
};

Flash workers have access to two types of storage: <WorkerContainerDiskTooltip /> for temporary data and <NetworkVolumesTooltip /> for persistent, sharable data.

## Container disk

A container disk provides temporary storage that exists only while a worker is running. Each worker gets its own isolated container disk, with a default size of 64GB for GPU endpoints.

You can read and write temporary files to the container disk using standard filesystem operations from within `@Endpoint` functions.

Any file that is *not* written to a network volume (at `/runpod-volume/`) is written to the container disk, and will be erased when the worker stops.

### Configuring container disk size (GPU-only)

Configure container disk size for GPU endpoints using the `template` parameter (default: 64GB).

```python theme={"theme":{"light":"github-light","dark":"github-dark"}}
from runpod_flash import Endpoint, GpuType, PodTemplate

@Endpoint(
    name="large-temp-storage",
    gpu=GpuType.NVIDIA_A100_80GB_PCIe,
    template=PodTemplate(containerDiskInGb=100)
)
async def process(data: dict) -> dict:
    # 100GB container disk available
    ...
```

### CPU auto-sizing

CPU endpoints automatically adjust container disk size based on instance limits:

* `CPU3G` and `CPU3C` instances: vCPU count × 10GB (e.g., 2 vCPU = 20GB)
* `CPU5C` instances: vCPU count × 15GB (e.g., 4 vCPU = 60GB)

If you specify a custom size that exceeds the instance limit, deployment will fail with a validation error.

## Network volumes

Network volumes provide persistent storage that survives worker restarts. Each volume is tied to a specific datacenter. Use volumes to share data between endpoint functions or to persist data between runs.

### Attaching network volumes

Attach a network volume using the `volume` parameter. Flash uses the volume `name` to find an existing volume or create a new one. Specify the `datacenter` parameter to control where the volume is created:

```python theme={"theme":{"light":"github-light","dark":"github-dark"}}
from runpod_flash import Endpoint, GpuType, DataCenter, NetworkVolume

vol = NetworkVolume(name="model-cache", size=100, datacenter=DataCenter.US_GA_2)

@Endpoint(
    name="persistent-storage",
    gpu=GpuType.NVIDIA_A100_80GB_PCIe,
    datacenter=DataCenter.US_GA_2,
    volume=vol
)
async def process(data: dict) -> dict:
    # Access files at /runpod-volume/
    ...
```

The `size` parameter specifies the volume size in GB. Valid values range from 10 to 4096 GB (4 TB). If not specified, `size` defaults to 100 GB.

You can also reference an existing volume by ID:

```python theme={"theme":{"light":"github-light","dark":"github-dark"}}
vol = NetworkVolume(id="vol_abc123")
```

### Multi-datacenter volumes

For endpoints deployed across multiple datacenters, pass a list of volumes (one per datacenter):

```python theme={"theme":{"light":"github-light","dark":"github-dark"}}
from runpod_flash import Endpoint, GpuType, DataCenter, NetworkVolume

volumes = [
    NetworkVolume(name="models-us", size=100, datacenter=DataCenter.US_GA_2),
    NetworkVolume(name="models-eu", size=100, datacenter=DataCenter.EU_RO_1),
]

@Endpoint(
    name="global-inference",
    gpu=GpuType.NVIDIA_A100_80GB_PCIe,
    datacenter=[DataCenter.US_GA_2, DataCenter.EU_RO_1],
    volume=volumes
)
async def process(data: dict) -> dict:
    # Workers in each region access their local volume at /runpod-volume/
    ...
```

<Warning>
  Only one network volume is allowed per datacenter. If you specify multiple volumes in the same datacenter, deployment will fail.
</Warning>

### Accessing network volume files

Network volumes mount at `/runpod-volume/` and can be accessed like a regular filesystem:

```python theme={"theme":{"light":"github-light","dark":"github-dark"}}
from runpod_flash import Endpoint, GpuType, NetworkVolume

vol = NetworkVolume(name="model-storage")

@Endpoint(
    name="model-server",
    gpu=GpuType.NVIDIA_A100_80GB_PCIe,
    volume=vol,
    dependencies=["torch", "transformers"]
)
async def run_inference(prompt: str) -> dict:
    from transformers import AutoModelForCausalLM, AutoTokenizer

    # Load model from network volume
    # Persists across worker restarts and shared between workers
    model_path = "/runpod-volume/models/llama-7b"
    model = AutoModelForCausalLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # Run inference
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_length=100)
    text = tokenizer.decode(outputs[0])

    return {"generated_text": text}
```

### Load-balanced endpoints with storage

```python theme={"theme":{"light":"github-light","dark":"github-dark"}}
from runpod_flash import Endpoint, GpuType, NetworkVolume

vol = NetworkVolume(name="model-storage")

api = Endpoint(
    name="inference-api",
    gpu=GpuType.NVIDIA_GEFORCE_RTX_4090,
    volume=vol,
    workers=(1, 5)
)

@api.post("/generate")
async def generate(prompt: str) -> dict:
    from transformers import AutoModelForCausalLM

    model = AutoModelForCausalLM.from_pretrained("/runpod-volume/models/gpt2")
    # Generate text
    return {"text": "generated"}

@api.get("/models")
async def list_models() -> dict:
    import os
    models = os.listdir("/runpod-volume/models")
    return {"models": models}
```

### Creating and managing network volumes

Network volumes must be created before attaching them to an Endpoint. See [Network volumes](/storage/network-volumes) for detailed instructions.