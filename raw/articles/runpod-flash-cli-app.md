---
source_url: https://docs.runpod.io/flash/cli/app
ingested: 2026-08-24
sha256: c215565923c0dd1671cc133b6c2b59f7ba324c0bc0bea22f7f2123b926ddc0c5
media_type: article
---

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.runpod.io/llms.txt
> Use this file to discover all available pages before exploring further.

# app

Manage Flash applications. An app is the top-level container that groups your deployment environments, build artifacts, and configuration.

```bash Command theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash app <subcommand> [OPTIONS]
```

## Subcommands

| Subcommand | Description                         |
| ---------- | ----------------------------------- |
| `list`     | Show all apps in your account       |
| `create`   | Create a new app                    |
| `get`      | Show details of an app              |
| `delete`   | Delete an app and all its resources |

***

## app list

Show all Flash apps under your account.

```bash Command theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash app list
```

### Output

```text theme={"theme":{"light":"github-light","dark":"github-dark"}}
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Name           ┃ ID                   ┃ Environments            ┃ Builds           ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ my-project     │ app_abc123           │ dev, staging, prod      │ build_1, build_2 │
│ demo-api       │ app_def456           │ production              │ build_3          │
│ ml-inference   │ app_ghi789           │ dev, production         │ build_4, build_5 │
└────────────────┴──────────────────────┴─────────────────────────┴──────────────────┘
```

***

## app create

Register a new Flash app on Runpod's backend.

```bash Command theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash app create <NAME>
```

### Arguments

<ResponseField name="NAME" type="string" required>
  Name for the new Flash app. Must be unique within your account.
</ResponseField>

### What it creates

This command registers a Flash app in Runpod's backend—essentially creating a namespace for your environments and builds. It does not:

* Create local files (use `flash init` for that).
* Provision cloud resources (endpoints, volumes, etc.).
* Deploy any code.

The app is just a container that groups environments and builds together.

### When to use

<Note>
  Most users don't need to run `flash app create` explicitly. Apps are created automatically when you first run `flash deploy`. This command is primarily for CI/CD pipelines that need to pre-register apps before deployment.
</Note>

***

## app get

Get detailed information about a Flash app.

```bash Command theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash app get <NAME>
```

### Arguments

<ResponseField name="NAME" type="string" required>
  Name of the Flash app to inspect.
</ResponseField>

### Output

```text theme={"theme":{"light":"github-light","dark":"github-dark"}}
╭─────────────────────────────────╮
│ Flash App: my-project           │
├─────────────────────────────────┤
│ Name: my-project                │
│ ID: app_abc123                  │
│ Environments: 3                 │
│ Builds: 5                       │
╰─────────────────────────────────╯

              Environments
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Name       ┃ ID                 ┃ State   ┃ Active Build     ┃ Created          ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ dev        │ env_dev123         │ DEPLOYED│ build_xyz789     │ 2024-01-15 10:30 │
│ staging    │ env_stg456         │ DEPLOYED│ build_xyz789     │ 2024-01-16 14:20 │
│ production │ env_prd789         │ DEPLOYED│ build_abc123     │ 2024-01-20 09:15 │
└────────────┴────────────────────┴─────────┴──────────────────┴──────────────────┘

                     Builds
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ ID                 ┃ Status                   ┃ Created          ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ build_abc123       │ COMPLETED                │ 2024-01-20 09:00 │
│ build_xyz789       │ COMPLETED                │ 2024-01-18 15:45 │
│ build_def456       │ COMPLETED                │ 2024-01-15 11:20 │
└────────────────────┴──────────────────────────┴──────────────────┘
```

***

## app delete

Delete a Flash app and all its associated resources.

```bash Command theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash app delete <NAME>
```

### Arguments

<ResponseField name="NAME" type="string" required>
  Name of the Flash app to delete.
</ResponseField>

### Process

1. Shows app details and resources to be deleted.
2. Prompts for confirmation (required).
3. Deletes all environments and their resources.
4. Deletes all builds.
5. Deletes the app.

<Warning>
  This operation is irreversible. All environments, builds, endpoints, volumes, and configuration will be permanently deleted.
</Warning>

***

## App hierarchy

See [Apps and environments](/flash/apps/apps-and-environments#app-hierarchy) for the complete app organization structure.

## Auto-detection

Flash CLI automatically detects the app name from your current directory:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
cd /path/to/APP_NAME
flash deploy          # Deploys to 'APP_NAME' app
flash env list        # Lists 'APP_NAME' environments
```

Override with the `--app` flag:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash deploy --app other-project
flash env list --app other-project
```

## Related commands

* [`flash env`](/flash/cli/env) - Manage environments within an app
* [`flash deploy`](/flash/cli/deploy) - Deploy to an app's environment
* [`flash init`](/flash/cli/init) - Create a new project