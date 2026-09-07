---
source_url: https://docs.runpod.io/flash/cli/update
ingested: 2026-08-24
sha256: 03ddc672d0f543287394a82560010ae1f71ad2192bac27261353af2a2935ab0b
media_type: article
---

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.runpod.io/llms.txt
> Use this file to discover all available pages before exploring further.

# update

Update the Flash CLI to the latest version or a specific version. The command fetches version information from PyPI and installs using uv (when available) or pip.

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash update [OPTIONS]
```

## Examples

Update to the latest version:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash update
```

Update to a specific version:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash update --version 1.4.0
```

## Flags

<ResponseField name="--version, -V" type="string">
  Target version to install. If not specified, updates to the latest version available on PyPI.
</ResponseField>

## Automatic update checks

Flash checks for newer versions in the background when you run most commands. If an update is available, a notice appears after the command completes:

```
A new version of runpod-flash is available: 2.0.0
  Run 'flash update' to upgrade.
```

This check runs at most once every 24 hours and is cached locally to `~/.config/runpod/update_check.json`.

### Excluded commands

The background check does not run for:

* `flash dev` - Long-running development server where the notice would appear at an unpredictable time.
* `flash update` - Already managing versions directly.

### Disabling update checks

Set the `FLASH_NO_UPDATE_CHECK` environment variable to skip automatic update checks:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
export FLASH_NO_UPDATE_CHECK=1
```

Update checks are also skipped automatically in CI environments (when the `CI` environment variable is set) and in non-interactive sessions (when neither stdout nor stderr is a TTY).

## Related commands

* [`flash --version`](/flash/cli/overview#getting-help) - Check your current Flash version