---
source_url: https://docs.runpod.io/flash/cli/overview
ingested: 2026-08-24
sha256: 05340b5182e7006463c88d1583c1b4ec553fcc864fa5e54ea66d936714b4ee4c
media_type: article
---

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.runpod.io/llms.txt
> Use this file to discover all available pages before exploring further.

# CLI overview

> Learn how to use the Flash CLI for local development and deployment. Review setup, configuration, deployment, and usage guidance for Runpod Flash.

The Flash CLI provides commands for initializing projects, running local development servers, building deployment artifacts, and managing your applications on Runpod Serverless.

Before using the CLI, make sure you've [installed Flash](/flash/overview#install-flash).

## Available commands

| Command                                 | Description                                               |
| --------------------------------------- | --------------------------------------------------------- |
| [`flash init`](/flash/cli/init)         | Create a new Flash project with a template structure      |
| [`flash login`](/flash/cli/login)       | Authenticate with Runpod using your API key               |
| [`flash dev`](/flash/cli/dev)           | Start the local development server with automatic updates |
| [`flash build`](/flash/cli/build)       | Build a deployment artifact without deploying             |
| [`flash deploy`](/flash/cli/deploy)     | Build and deploy your application to Runpod               |
| [`flash env`](/flash/cli/env)           | Manage deployment environments                            |
| [`flash app`](/flash/cli/app)           | Manage Flash applications                                 |
| [`flash undeploy`](/flash/cli/undeploy) | Remove deployed endpoints                                 |
| [`flash update`](/flash/cli/update)     | Update Flash to the latest or a specific version          |

## Getting help

View help for any command by adding `--help`:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash --help
flash deploy --help
flash env --help
```

## Authentication

Authenticate with Runpod:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash login
```

This command opens your browser to authenticate with Runpod. After you approve the request, your API key is saved locally for future CLI operations. See [`flash login`](/flash/cli/login) for details.

Alternatively, set the `RUNPOD_API_KEY` environment variable:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
export RUNPOD_API_KEY=your_api_key_here
```

## Using uv

If you installed Flash with [uv](https://docs.astral.sh/uv/), prefix all Flash commands with `uv run`:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
uv run flash login
uv run flash dev
uv run flash deploy
```

## Common workflows

### Local development

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
# Create a new project
flash init PROJECT_NAME
cd PROJECT_NAME

# Install dependencies
pip install -r requirements.txt

# Add your API key to .env
# Start the development server
flash dev
```

### Deploy to production

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
# Build and deploy
flash deploy

# Deploy to a specific environment
flash deploy --env ENVIRONMENT_NAME
```

### Manage deployments

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
# List environments
flash env list

# Check environment status
flash env get ENVIRONMENT_NAME

# Remove an environment
flash env delete ENVIRONMENT_NAME
```

### Clean up endpoints

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
# List deployed endpoints
flash undeploy list

# Remove specific endpoint
flash undeploy ENDPOINT_NAME

# Remove all endpoints
flash undeploy --all
```