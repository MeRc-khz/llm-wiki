---
source_url: https://docs.runpod.io/flash/windows-wsl2
ingested: 2026-08-24
sha256: e111fccb5cacb1f1f480fc1d1ecf5420ff57171aa62eea6ff33767a205c2fb08
media_type: article
---

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.runpod.io/llms.txt
> Use this file to discover all available pages before exploring further.

# Use Flash on Windows

> Set up WSL2 with Ubuntu to run Flash on Windows. Review setup, configuration, deployment, and usage guidance for Runpod Flash.

Flash runs natively on macOS and Linux. On Windows, you can run Flash through Windows Subsystem for Linux (WSL2), which provides a full Linux environment on your machine.

## Requirements

* Windows 10 version 2004 or later, or Windows 11.
* Administrator access to your Windows machine.
* [Runpod account](/accounts-billing/manage-accounts) with a verified email address.
* [An API key](/get-started/api-keys) with **All** access permissions.

## Step 1: Enable WSL2

Open PowerShell or Command Prompt as Administrator (right-click and select "Run as administrator"), then run:

```powershell theme={"theme":{"light":"github-light","dark":"github-dark"}}
wsl --install
```

This command enables WSL, installs the latest Linux kernel, sets WSL2 as the default version, and installs Ubuntu as your Linux distribution.

<Tip>
  If WSL is already installed on your system, you can install Ubuntu specifically with:

  ```powershell theme={"theme":{"light":"github-light","dark":"github-dark"}}
  wsl --install -d Ubuntu
  ```
</Tip>

After the installation completes, restart your computer when prompted.

## Step 2: Set up Ubuntu

After restarting, Ubuntu launches automatically and prompts you to create a Linux username and password. These credentials are separate from your Windows account and are used only within the Linux environment.

If Ubuntu doesn't launch automatically, open it from the Start menu by searching for "Ubuntu".

Once setup is complete, you'll see the Ubuntu terminal prompt:

```text theme={"theme":{"light":"github-light","dark":"github-dark"}}
username@hostname:~$
```

Update your package lists to ensure you have access to the latest software:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
sudo apt update && sudo apt upgrade -y
```

## Step 3: Install Python and uv

Flash requires Python 3.10 or later. Ubuntu typically includes Python, but you should verify the version:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
python3 --version
```

If you need a newer version, install it:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
sudo apt install python3.12 python3.12-venv -y
```

Install [uv](https://docs.astral.sh/uv/), a fast Python package manager:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, restart your terminal or run the following to add uv to your path:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
source $HOME/.local/bin/env
```

## Step 4: Install and authenticate Flash

Create a project directory and set up a virtual environment:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
mkdir my-flash-project && cd my-flash-project
uv venv
source .venv/bin/activate
```

Install Flash:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
uv pip install runpod-flash
```

Authenticate with your Runpod account:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash login
```

This opens your browser to authorize Flash. After you approve, your credentials are saved.

<Tip>
  Alternatively, you can set your API key directly:

  ```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
  export RUNPOD_API_KEY="your_key"
  ```
</Tip>

## Step 5: Verify your installation

Test that Flash is working correctly:

```bash theme={"theme":{"light":"github-light","dark":"github-dark"}}
flash --version
```

You're now ready to use Flash. Continue with the [quickstart](/flash/quickstart) to run your first GPU workload.

## Tips for working with WSL2

**Accessing Windows files**: Your Windows drives are mounted under `/mnt/`. For example, `C:\Users\YourName\Documents` is accessible at `/mnt/c/Users/YourName/Documents`.

**Opening WSL from any folder**: In Windows Explorer, type `wsl` in the address bar to open Ubuntu in that directory.

**VS Code integration**: Install the [WSL extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) for VS Code to edit files in WSL with full IDE support. Run `code .` from your WSL terminal to open VS Code in the current directory.

**Default terminal**: You can set Ubuntu as your default terminal in Windows Terminal for quicker access.