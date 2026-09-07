---
source_url: https://docs.runpod.io/flash/apps/overview
ingested: 2026-08-24
sha256: 8ac9638c260cec2ee75eccccae76ff019d16497b65c02590b36164c5dfaa09dc
media_type: article
---

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.runpod.io/llms.txt
> Use this file to discover all available pages before exploring further.

# Overview

> Understand the Flash app development lifecycle. Review setup, configuration, deployment, and usage guidance for Runpod Flash.

export const ServerlessTooltip = () => {
  return <Tooltip headline="Serverless" tip="A cloud computing platform that allows you to deploy AI/ML applications without provisioning or managing servers." cta="Learn more about Serverless" href="/serverless/overview">Serverless</Tooltip>;
};

A Flash app is a collection of <ServerlessTooltip /> endpoints deployed to Runpod.

<CardGroup cols={2}>
  <Card title="Build your first app" href="/flash/apps/build-app" icon="code" horizontal>
    Create a Flash app, test it locally, and deploy it to production.
  </Card>

  <Card title="Initialize a project" href="/flash/apps/initialize-project" icon="folder-plus" horizontal>
    Create boilerplate code for a new Flash project with `flash init`.
  </Card>
</CardGroup>

## App development workflow

Building a Flash application follows a clear progression from initialization to production deployment:

<Steps>
  <Step title="Initialize">
    Use `flash init` to create a new project with example workers:

    ```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
    flash init PROJECT_NAME
    cd PROJECT_NAME
    pip install -r requirements.txt
    ```

    This gives you a working project structure with GPU and CPU worker examples. [Learn more about project initialization](/flash/apps/initialize-project).
  </Step>

  <Step title="Develop">
    Write your application code by defining `Endpoint` functions that execute on Runpod workers:

    ```python theme={"theme":{"light":"github-light","dark":"github-dark"}}
    from runpod_flash import Endpoint, GpuType

    @Endpoint(
        name="inference-worker",
        gpu=GpuType.NVIDIA_GEFORCE_RTX_4090,
        workers=3,
        dependencies=["torch"]
    )
    def run_inference(prompt: str) -> dict:
        import torch
        # Your inference logic here
        return {"result": "..."}
    ```

    [Learn more about customizing your app](/flash/apps/customize-app).
  </Step>

  <Step title="Test locally">
    Start a local development server to test your application:

    ```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
    flash dev
    ```

    Your app runs locally and updates automatically. When you call an `@Endpoint` function, Flash sends the latest code to Runpod workers. [Learn more about local testing](/flash/apps/local-testing).
  </Step>

  <Step title="Deploy">
    When ready for production, deploy your application to Runpod Serverless:

    ```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
    flash deploy
    ```

    When you deploy an app, Runpod:

    1. Packages your code, dependencies, and deployment manifest into a tarball (max 1.5 GB).
    2. Uploads the tarball to Runpod.
    3. Provisions independent Serverless endpoints based on your [endpoint configurations](/flash/create-endpoints).

    Your entire application—including all worker functions—runs on Runpod infrastructure. [Learn more about deployment](/flash/apps/deploy-apps).
  </Step>

  <Step title="Manage">
    Use apps and environments to organize and manage your deployments across different stages (dev, staging, production). [Learn more about apps and environments](/flash/apps/apps-and-environments).
  </Step>
</Steps>

## Apps and environments

Flash uses a two-level organizational structure: **apps** (project containers) and **environments** (deployment stages like dev, staging, production). See [Apps and environments](/flash/apps/apps-and-environments) for complete details.

## Next steps

<CardGroup cols={2}>
  <Card title="Build your first app" href="/flash/apps/build-app" icon="code" horizontal>
    Create a Flash app, test it locally, and deploy it to production.
  </Card>

  <Card title="Initialize a project" href="/flash/apps/initialize-project" icon="folder-plus" horizontal>
    Create boilerplate code for a new Flash project with `flash init`.
  </Card>

  <Card title="Test locally" href="/flash/apps/local-testing" icon="flask" horizontal>
    Use `flash dev` for local development and testing.
  </Card>

  <Card title="Deploy to Runpod" href="/flash/apps/deploy-apps" icon="rocket" horizontal>
    Deploy your application to production with `flash deploy`.
  </Card>
</CardGroup>