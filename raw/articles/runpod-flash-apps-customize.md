---
source_url: https://docs.runpod.io/flash/apps/customize-app
ingested: 2026-08-24
sha256: 9b253d8e87a6734e85311c005f5e78277b7c92ceb6fa76a01d3e67a4f3d2c638
media_type: article
---

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.runpod.io/llms.txt
> Use this file to discover all available pages before exploring further.

# Customize your Flash app

> Modify the Flash project template to build your application. Review setup, configuration, deployment, and usage guidance for Runpod Flash.

export const QueueBasedEndpointsTooltip = () => {
  return <Tooltip headline="Queue-based endpoint" tip="A Serverless endpoint that processes requests sequentially through a managed queue, providing guaranteed execution and automatic retries. Uses handler functions and standard operations like /run and /runsync." cta="Learn more about queue-based endpoints" href="/serverless/endpoints/overview#queue-based-endpoints">queue-based endpoints</Tooltip>;
};

export const LoadBalancingEndpointsTooltip = () => {
  return <Tooltip headline="Load balancing endpoints" tip="Serverless endpoints that route requests directly to worker HTTP servers without queuing, ideal for real-time applications and streaming. Support custom HTTP frameworks like FastAPI or Flask." cta="Learn more about load balancing endpoints" href="/serverless/load-balancing/overview">load balancing endpoints</Tooltip>;
};

After running `flash init`, you have a working project template with example <LoadBalancingEndpointsTooltip /> and <QueueBasedEndpointsTooltip />. This guide shows you how to customize the template to build your application.

## Endpoint types

Flash supports two endpoint types, each suited for different use cases:

| Type              | Best for               | Functions per endpoint |
| ----------------- | ---------------------- | ---------------------- |
| **Queue-based**   | Long-running GPU tasks | One                    |
| **Load-balanced** | Fast HTTP APIs         | Multiple (via routes)  |

<Tabs>
  <Tab title="Queue-based">
    Each `@Endpoint` function creates a separate Serverless endpoint:

    ```python theme={"theme":{"light":"github-light","dark":"github-dark"}}
    @Endpoint(name="preprocess", gpu=GpuType.NVIDIA_A100_80GB_PCIe)
    def preprocess(data): ...

    @Endpoint(name="inference", gpu=GpuType.NVIDIA_A100_80GB_PCIe)
    def run_model(input): ...
    ```

    Call via `/run` or `/runsync`: `https://api.runpod.ai/v2/{endpoint_id}/runsync`
  </Tab>

  <Tab title="Load-balanced">
    Multiple routes share one endpoint:

    ```python theme={"theme":{"light":"github-light","dark":"github-dark"}}
    api = Endpoint(name="api-server", cpu="cpu5c-4-8", workers=(1, 5))

    @api.post("/generate")
    def generate_text(prompt: str): ...

    @api.get("/health")
    def health_check(): ...
    ```

    Call via HTTP routes: `https://{endpoint_id}.api.runpod.ai/generate`
  </Tab>
</Tabs>

## Add load balancing routes

To add routes to an existing load balancing endpoint, use the route decorator pattern:

```python title="lb_worker.py" theme={"theme":{"light":"github-light","dark":"github-dark"}}
from runpod_flash import Endpoint

api = Endpoint(name="lb_worker", cpu="cpu5c-4-8", workers=(1, 5))

# Existing routes
@api.post("/process")
async def process(input_data: dict) -> dict:
    # ... existing code ...
    pass

# Add a new route
@api.get("/status")
async def get_status() -> dict:
    return {"status": "healthy", "version": "1.0"}
```

All routes share the same `lb_worker` Serverless endpoint. Each route is accessible at its defined path.

**Key points:**

* Multiple routes can share one endpoint configuration
* Each route has its own HTTP method and path
* All routes on the same endpoint deploy to one Serverless endpoint

## Add queue-based endpoints

To add a new queue-based endpoint, create a new endpoint with a unique name:

```python title="gpu_worker.py" theme={"theme":{"light":"github-light","dark":"github-dark"}}
from runpod_flash import Endpoint, GpuType

# Existing endpoint
@Endpoint(
    name="gpu-inference",
    gpu=GpuType.NVIDIA_A100_80GB_PCIe,
    workers=3,
    dependencies=["torch"]
)
async def run_inference(input: dict) -> dict:
    import torch
    # Inference logic
    return {"result": "processed"}

# New endpoint for a different workload
@Endpoint(
    name="gpu-training",
    gpu=GpuType.NVIDIA_A100_80GB_PCIe,
    workers=1,
    dependencies=["torch", "transformers"]
)
async def train_model(config: dict) -> dict:
    import torch
    from transformers import Trainer
    # Training logic
    return {"model_path": "/models/trained"}
```

This creates two separate Serverless endpoints, each with its own URL and scaling configuration.

<Warning>
  **Do not reuse the same endpoint name for multiple queue-based functions when deploying Flash apps.** Each queue-based `@Endpoint` must have its own unique `name` parameter.
</Warning>

## Modify endpoint configurations

Customize endpoint configurations for each worker function in your app. Each `@Endpoint` function can have its own GPU type, scaling parameters, and timeouts optimized for its specific workload.

```python theme={"theme":{"light":"github-light","dark":"github-dark"}}
# Example: Different configs for different workloads
@Endpoint(
    name="preprocess",
    gpu=GpuType.NVIDIA_GEFORCE_RTX_4090,  # Cost-effective for preprocessing
    workers=(0, 5)
)
async def preprocess(data): ...

@Endpoint(
    name="inference",
    gpu=GpuType.NVIDIA_A100_80GB_PCIe,  # High VRAM for large models
    workers=(1, 10)  # Keep one worker ready
)
async def inference(data): ...
```

For details, see:

* [Configuration parameters](/flash/configuration/parameters) for all available options.
* [GPU types](/flash/configuration/gpu-types) for selecting hardware.
* [Best practices](/flash/configuration/best-practices) for optimization guidance.

## Test your customizations

After customizing your app, test locally with `flash dev`:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash dev

# If using uv:
uv run flash dev
```

This starts a development server at [http://localhost:8888](http://localhost:8888) with:

* Interactive API documentation at `/docs`
* Auto-reload on code changes
* Real remote execution on Runpod workers

Make sure to test:

* All HTTP routes work as expected
* Endpoint functions execute correctly
* Dependencies install properly
* Error handling works

## Next steps

<CardGroup cols={2}>
  <Card title="Test locally" href="/flash/apps/local-testing" icon="flask" horizontal>
    Use `flash dev` for local development and testing.
  </Card>

  <Card title="Deploy to Runpod" href="/flash/apps/deploy-apps" icon="rocket" horizontal>
    Deploy your application to production with `flash deploy`.
  </Card>

  <Card title="Configure hardware resources" href="/flash/configuration/parameters" icon="sliders" horizontal>
    Complete reference for configuration options.
  </Card>

  <Card title="Create endpoint functions" href="/flash/create-endpoints" icon="code" horizontal>
    Learn more about writing and optimizing endpoint functions.
  </Card>
</CardGroup>