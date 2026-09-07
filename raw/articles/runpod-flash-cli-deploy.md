---
source_url: https://docs.runpod.io/flash/cli/deploy
ingested: 2026-08-24
sha256: d7da2090e463e6c17ca1b73631464356384e3036ebf0136de652aba8a656bd8e
media_type: article
---

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.runpod.io/llms.txt
> Use this file to discover all available pages before exploring further.

# deploy

Build and deploy your Flash application to Runpod Serverless endpoints in one step. This is the primary command for getting your application running in the cloud.

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash deploy [OPTIONS]
```

## Examples

Build and deploy a Flash app from the current directory (auto-selects environment if only one exists):

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash deploy
```

Deploy to a specific environment:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash deploy --env production
```

Deploy with additional excluded packages:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash deploy --exclude scipy,pandas
```

Build and test locally before deploying:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash deploy --preview
```

## Flags

<ResponseField name="--env, -e" type="string">
  Target environment name (e.g., `dev`, `staging`, `production`). Auto-selected if only one exists. Creates the environment if it doesn't exist.
</ResponseField>

<ResponseField name="--app, -a" type="string">
  Flash app name. Auto-detected from the current directory if not specified.
</ResponseField>

<ResponseField name="--no-deps">
  Skip transitive dependencies during pip install. Useful when the base image already includes dependencies.
</ResponseField>

<ResponseField name="--exclude" type="string">
  Comma-separated packages to exclude (e.g., `torch,torchvision`). Use this to stay under the 1.5GB deployment limit.
</ResponseField>

<ResponseField name="--output, -o" type="string" default="artifact.tar.gz">
  Custom archive name for the build artifact.
</ResponseField>

<ResponseField name="--preview">
  Build and launch a local Docker-based preview environment instead of deploying to Runpod.
</ResponseField>

<ResponseField name="--python-version" type="string">
  Target Python version for worker images (3.10, 3.11, 3.12, or 3.13). Overrides per-resource `python_version` declarations and local interpreter detection.
</ResponseField>

## What happens during deployment

1. **Build phase**: Creates the deployment artifact (same as `flash build`).
2. **Environment resolution**: Detects or creates the target environment.
3. **Upload**: Sends the artifact to Runpod storage.
4. **Provisioning**: Creates or updates Serverless endpoints.
5. **Configuration**: Sets up environment variables and service discovery.

## Rolling releases for code changes

When you run `flash deploy` on an already-deployed application, Flash compares your current build against the previous deployment to determine what needs updating.

Flash triggers a rolling release when your source code changes, even if your resource configuration stays the same. During the build phase, Flash computes a fingerprint of your source files. If this fingerprint differs from the previous deployment, Flash treats it as a configuration change and initiates a rolling update to your endpoints.

This means you can iterate on your code without modifying resource configurations like GPU types or worker counts. Run `flash deploy` after making code changes, and Flash rolls out the updated code to your endpoints.

## Architecture

After deployment, your Flash app runs as independent Serverless endpoints on Runpod:

<div style={{ marginLeft: '4rem'}}>
  ```mermaid theme={"theme":{"light":"github-light","dark":"github-dark"}}
  %%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#9289FE','primaryTextColor':'#fff','primaryBorderColor':'#9289FE','lineColor':'#5F4CFE','secondaryColor':'#AE6DFF','tertiaryColor':'#FCB1FF','edgeLabelBackground':'#5F4CFE', 'fontSize':'14px','fontFamily':'font-inter'}}}%%

  flowchart TB
      Users(["USERS"])
      StateManager["Runpod GraphQL API<br/>• Service discovery<br/>• Manifest registry"]

      subgraph Runpod ["RUNPOD SERVERLESS"]
          LB["lb_worker ENDPOINT<br/>(load-balanced)<br/>• POST /process<br/>• GET /health"]
          GPU["gpu_worker ENDPOINT<br/>(queue-based)<br/>• POST /runsync"]
          CPU["cpu_worker ENDPOINT<br/>(queue-based)<br/>• POST /runsync"]

          LB <-.->|"inter-endpoint calls"| GPU
          LB <-.->|"inter-endpoint calls"| CPU

          LB -.->|"service discovery"| StateManager
          GPU -.->|"service discovery"| StateManager
          CPU -.->|"service discovery"| StateManager
      end

      Users -->|"call directly"| LB
      Users -->|"call directly"| GPU
      Users -->|"call directly"| CPU

      style Runpod fill:#1a1a2e,stroke:#5F4CFE,stroke-width:2px,color:#fff
      style Users fill:#4D38F5,stroke:#4D38F5,color:#fff
      style LB fill:#5F4CFE,stroke:#5F4CFE,color:#fff
      style GPU fill:#22C55E,stroke:#22C55E,color:#000
      style CPU fill:#22C55E,stroke:#22C55E,color:#000
      style StateManager fill:#AE6DFF,stroke:#AE6DFF,color:#fff
  ```
</div>

Each resource configuration in your code creates an independent endpoint. You can call any endpoint directly based on your needs.

## App and environment management

### Automatic creation

Flash automatically creates apps and environments as needed during deployment:

* If the app doesn't exist, Flash creates it along with the target environment.
* If only the environment doesn't exist, Flash creates it within the existing app.

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
# Creates the app and 'staging' environment if they don't exist
flash deploy --env staging
```

### Auto-selection

When you have only one environment, it's selected automatically:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
# Auto-selects the only available environment
flash deploy
```

When multiple environments exist, you must specify one:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
# Required when multiple environments exist
flash deploy --env staging
```

### Default environment

If no app or environment exists and none is specified, Flash creates the app with a `production` environment by default.

## Post-deployment

After successful deployment, Flash displays all deployed endpoints:

```text theme={"theme":{"light":"github-light","dark":"github-dark"}}
✓ Deployment Complete

Load-balanced endpoints:
  https://abc123xyz.api.runpod.ai  (lb_worker)
    POST   /process
    GET    /health

  Try it:
    curl -X POST https://abc123xyz.api.runpod.ai/process \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ***" \
        -d '{"input_data": {"message": "Hello from Flash"}}'

Queue-based endpoints:
  https://api.runpod.ai/v2/def456xyz  (gpu_worker)
  https://api.runpod.ai/v2/ghi789xyz  (cpu_worker)

  Try it:
    curl -X POST https://api.runpod.ai/v2/def456xyz/runsync \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ***" \
        -d '{"input": {"input_data": {"message": "Hello from the GPU"}}}'
```

Each endpoint is independent with its own URL and can be called directly.

### Authentication

All deployed endpoints require authentication with your Runpod API key:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
export RUNPOD_API_KEY="your_key_here"

curl -X POST https://YOUR_ENDPOINT_URL/path \
    -H "Authorization: Bearer ***" \
    -H "Content-Type: application/json" \
    -d '{"param": "value"}'
```

## Preview mode

Test locally before deploying:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash deploy --preview
```

This builds your project and runs it in Docker containers locally:

* Each endpoint runs in its own container.
* All containers communicate via Docker network.
* Endpoints exposed on local ports for testing.
* Press `Ctrl+C` to stop.

## Managing deployment size

Runpod Serverless has a **1.5GB limit**. Flash automatically excludes packages that are pre-installed in the base image (`torch`, `torchvision`, `torchaudio`, `numpy`, `triton`).

If the deployment is still too large, use `--exclude` to skip additional packages:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash deploy --exclude scipy,pandas
```

See [`flash build` - Managing deployment size](/flash/cli/build#managing-deployment-size) for more details.

## flash dev vs flash deploy

See [`flash dev`](/flash/cli/dev#flash-dev-vs-flash-deploy) for a detailed comparison of local development vs production deployment.

## Troubleshooting

### Multiple environments error

```text theme={"theme":{"light":"github-light","dark":"github-dark"}}
Error: Multiple environments found: dev, staging, production
```

Specify the target environment:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash deploy --env staging
```

### Deployment size limit

Base image packages are auto-excluded. If the deployment is still too large, use `--exclude` to skip additional packages:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash deploy --exclude scipy,pandas
```

### Authentication fails

Ensure your API key is set:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
echo $RUNPOD_API_KEY
export RUNPOD_API_KEY="your_key_here"
```

## Related commands

* [`flash build`](/flash/cli/build) - Build without deploying
* [`flash dev`](/flash/cli/dev) - Local development server
* [`flash env`](/flash/cli/env) - Manage environments
* [`flash app`](/flash/cli/app) - Manage applications
* [`flash undeploy`](/flash/cli/undeploy) - Remove endpoints