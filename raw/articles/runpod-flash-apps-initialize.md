---
source_url: https://docs.runpod.io/flash/apps/initialize-project
ingested: 2026-08-24
sha256: eacc9f170209b1e3062d58afc364189a8dc3a5132e3a8f385444bea883a53738
media_type: article
---

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.runpod.io/llms.txt
> Use this file to discover all available pages before exploring further.

# Initialize a Flash app project

> Use flash init to create a new Flash project with a ready-to-use structure. Review configuration and usage details for Runpod Flash.

export const QueueBasedEndpointsTooltip = () => {
  return <Tooltip headline="Queue-based endpoint" tip="A Serverless endpoint that processes requests sequentially through a managed queue, providing guaranteed execution and automatic retries. Uses handler functions and standard operations like /run and /runsync." cta="Learn more about queue-based endpoints" href="/serverless/endpoints/overview#queue-based-endpoints">queue-based endpoints</Tooltip>;
};

export const LoadBalancingEndpointsTooltip = () => {
  return <Tooltip headline="Load balancing endpoints" tip="Serverless endpoints that route requests directly to worker HTTP servers without queuing, ideal for real-time applications and streaming. Support custom HTTP frameworks like FastAPI or Flask." cta="Learn more about load balancing endpoints" href="/serverless/load-balancing/overview">load balancing endpoints</Tooltip>;
};

The `flash init` command creates a new Flash project with a complete project structure, including example <LoadBalancingEndpointsTooltip /> and <QueueBasedEndpointsTooltip />, and configuration files. This gives you a working starting point for building Flash applications.

Use `flash init` whenever you want to start a new Flash project, fully configured for you to run `flash dev` and `flash deploy`.

## Create a new project

Create a new project in a new directory:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash init PROJECT_NAME
cd PROJECT_NAME

# If using uv:
uv run flash init PROJECT_NAME
```

Or initialize in your current directory:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash init .

# If using uv:
uv run flash init .
```

## Project structure

`flash init` creates the following structure:

<Tree>
  <Tree.Folder name="PROJECT_NAME" defaultOpen>
    <Tree.File name="lb_worker.py" />

    <Tree.File name="gpu_worker.py" />

    <Tree.File name="cpu_worker.py" />

    <Tree.File name=".env.example" />

    <Tree.File name=".gitignore" />

    <Tree.File name="pyproject.toml" />

    <Tree.File name="requirements.txt" />

    <Tree.File name="README.md" />
  </Tree.Folder>
</Tree>

### Key files

**lb\_worker.py**: An example load-balanced worker with HTTP routes. Contains `@Endpoint` functions with custom HTTP methods and paths (e.g., `POST /process`, `GET /health`). Creates one endpoint when deployed.

**gpu\_worker.py**: An example GPU queue-based worker. Contains `@Endpoint` functions that run on GPU hardware. Provides `/runsync` route for job submission. Creates one endpoint when deployed.

**cpu\_worker.py**: An example CPU queue-based worker. Contains `@Endpoint` functions that run on CPU-only instances. Provides `/runsync` route for job submission. Creates one endpoint when deployed.

Each worker file defines a resource configuration and its associated functions. When you deploy, Flash creates one Serverless endpoint per unique resource configuration.

## Set up the project

After initialization, complete the setup:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Add your API key to .env
# RUNPOD_API_KEY=your_api_key_here
```

## Handle existing files

If you run `flash init` in a directory with existing files, Flash detects conflicts and prompts for confirmation:

```text theme={"theme":{"light":"github-light","dark":"github-dark"}}
File Conflicts Detected

Warning: The following files will be overwritten:
  • requirements.txt
  • gpu_worker.py
  • README.md
  • lb_worker.py
  • cpu_worker.py

Continue and overwrite these files? [y/N]:
```

Use `--force` to skip the prompt and overwrite files:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash init . --force

# If using uv:
uv run flash init . --force
```

## Start developing

Once your project is set up:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
# Start the development server
flash dev

# Open the API explorer
# http://localhost:8888/docs

# If using uv:
uv run flash dev
```

Make changes to your worker files, and the server reloads automatically. When you're ready, deploy with:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash deploy

# If using uv:
uv run flash deploy
```

## Next steps

* [Customize your app](/flash/apps/customize-app) to add endpoints and modify configurations.
* [Test locally](/flash/apps/local-testing) with `flash dev`.
* [Deploy to production](/flash/apps/deploy-apps) with `flash deploy`.
* [View the flash init reference](/flash/cli/init) for all options.