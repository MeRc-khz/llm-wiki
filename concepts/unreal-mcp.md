---
title: Unreal MCP
created: 2026-08-04
updated: 2026-08-04
type: concept
tags: [mcp, agentic, tool-use, framework]
sources: [raw/articles/unreal-mcp-in-unreal-editor.md]
confidence: high
contested: false
contradictions: []
---

# Unreal MCP

**Unreal MCP** (engine identifier `ModelContextProtocol`) is an experimental Unreal Engine 5.8 plugin that embeds an [[mcp]] server inside the Unreal Editor process. Any MCP-compatible AI agent — Claude Code, Cursor, the MCP Inspector — can drive the editor over a local HTTP connection by invoking engine functionality as Tools: spawning actors, configuring lighting, creating material instances, inspecting Slate widgets, running automation tests. Readiness: **experimental**; many features are incomplete and APIs/data formats are subject to change.

> The friendly name *Unreal MCP* surfaces in the Plugin Browser; the actual identifier in the engine source tree, `.uplugin` files, C++ symbols, and console commands is `ModelContextProtocol`.

## Architecture

- **Server in-editor:** `ModelContextProtocol` and `ModelContextProtocolEngine` are runtime modules owning the server, protocol, settings, and the console commands. `ModelContextProtocolEditor` is editor-only: it handles the auto-start hook and adapts Toolset Registry toolsets into MCP Tools.
- **Game-thread sync:** Tool invocations execute on the Unreal game thread serially; clients must not issue overlapping Tool calls.
- **Local only:** binds to loopback by default (default `http://127.0.0.1:8000/mcp`), no auth; not safe to expose beyond the local machine.

## Toolsets & the Toolset Registry

Unreal MCP does *not* implement the Tools itself. It discovers them by querying the **Toolset Registry**, a sibling subsystem. A *Toolset* is a class deriving from `UToolsetDefinition` (C++) or `unreal.ToolsetDefinition` (Python) with functions marked as Tool calls. The registry collects these at startup; Unreal MCP wraps each as an MCP Tool available to every connected client. Enable the **All Toolsets** plugin to load the default toolsets (SceneTools, ActorTools, MaterialInstanceTools, ObjectTools …), or enable them individually.

## Setup quick reference

1. Enable **Unreal MCP** + **All Toolsets** plugins (Edit > Plugins), restart.
2. Editor Preferences > General > **Model Context Protocol**: enable **Auto Start Server** (binds `127.0.0.1:8000/mcp`); or run `ModelContextProtocol.StartServer [port]` in the console.
3. Generate a client config from the console, e.g. `ModelContextProtocol.GenerateClientConfig ClaudeCode` (supported: `ClaudeCode`, `Cursor`, `VSCode`, `Gemini`, `Codex`, `All`). Writes `.mcp.json` to the project root.
4. Launch the agent from the project/workspace root. Optional: use the **Terminal** plugin to keep everything in-editor.

## Authoring custom Tools

- **Recommended — Toolset Registry:** derive from `unreal.ToolsetDefinition` (Python, under any plugin's `Content/Python/`) or `UToolsetDefinition` (C++, `UCLASS(BlueprintType, Hidden)` with static `UFUNCTION(meta=(AICallable))`). Function docstrings + type hints drive the JSON Schema. Refresh with `ModelContextProtocol.RefreshTools`; new C++ `UFUNCTION`s require a full editor restart (Live Coding doesn't propagate new declarations).
- **Advanced — direct registration:** implement `IModelContextProtocolTool` and call `IModelContextProtocolModule::GetChecked().AddTool(...)`; caller owns deregistration. Used for runtime-schema or dynamic Tools.

## Tool Search mode

Default (`bEnableToolSearch=true`): `tools/list` returns three discovery meta-tools — `list_toolsets`, `describe_toolset`, `call_tool` — instead of every schema, keeping responses small. Agents walk this path on demand. Cooked/shpping builds that register Tools directly advertise them eagerly.

## Key limitations

- HTTP + Server-Sent Events only; **no stdio or WebSocket** transports.
- Loopback-only; rejects non-loopback Origin headers. No authentication layer.
- No shipping toolset advertises MCP Resources or Prompts.
- Runtime availability: cooked and shipping game builds *can* host a server via `IModelContextProtocolModule::StartServer()`, but registry toolsets are editor-only; Tools must be registered explicitly via `AddTool()` there.

## Debugging

- Output Log: auto-start logs bind address/port/path; failures (port in use, missing plugin) surface there.
- `LogModelContextProtocol` log category; raise verbosity with `Log LogModelContextProtocol Verbose`.
- **MCP Inspector** (`npx @modelcontextprotocol/inspector`) is the official debugging client — point it at `http://127.0.0.1:8000/mcp` (Streamable HTTP) to inspect schemas and invoke Tools directly.

## See also

- [[mcp]] — the open protocol Unreal MCP implements.
- [[rag]] — adjacent LLM-grounding mechanism (retrieval vs. live tool access).
