---
title: Unreal MCP
created: 2026-08-04
updated: 2026-08-04
type: concept
tags: [mcp, agentic, tool-use, framework]
sources: [raw/articles/unreal-mcp-in-unreal-editor.md, raw/transcripts/from-words-to-worlds-unreal-mcp-unreal-fest-2026.md]
confidence: high
contested: false
contradictions: []
---

# Unreal MCP

**Unreal MCP** (engine identifier `ModelContextProtocol`) is an experimental Unreal Engine 5.8 plugin that embeds an [[mcp]] server inside the Unreal Editor process. Any MCP-compatible AI agent — Claude Code, Cursor, the MCP Inspector — can drive the editor over a local HTTP connection by invoking engine functionality as Tools: spawning actors, configuring lighting, creating material instances, inspecting Slate widgets, running automation tests. Readiness: **experimental**; many features are incomplete and APIs/data formats are subject to change.

> The friendly name *Unreal MCP* surfaces in the Plugin Browser; the actual identifier in the engine source tree, `.uplugin` files, C++ symbols, and console commands is `ModelContextProtocol`.

## Official launch (Unreal Fest Chicago 2026)

Unreal MCP was officially launched with the **Unreal Engine 5.8** release, announced at Unreal Fest Chicago 2026 in the talk *"From Words to Worlds"* (Nathan, Jess, Quentin). It's **open and free**, shipping not just the server but out-of-box support for ~2 dozen engine and editor systems — just shy of ~1,000 ready-to-go APIs (materials, blueprints, PCG, and more). ^[raw/transcripts/from-words-to-worlds-unreal-mcp-unreal-fest-2026.md]

### Design philosophy

Epic frames the LLM as an **assistant, not a magic bullet**, guided by three principles:

- **Directable** — the model amplifies creative intent rather than replacing it.
- **Everything editable** — no special access/permissions/formats; every LLM action is inspectable as it happens and the results are indistinguishable from human-made assets, so you can edit/review after the fact.
- **Not a closed black box** — a clear, open path to customization, consistent with Unreal's extensibility ethos.

### World-building framework: toolsets + primitives + examples + skills

To make LLM reasoning work for spatial/world building (which LLMs inherently struggle with), Epic built a four-part data-driven framework — PCG was chosen as the "spatial language" because it excels at procedural content generation:

- **Toolsets** — APIs for LLMs (the [[unreal-mcp]] authoring surface).
- **PCG primitives** — a library of **80+ plug-and-play, fully parameterized spatial operations** built as PCG subgraphs (create shapes, compose, transforms, sample/filter/spawn). These are the LLM's "vocabulary"; they work with or without an LLM.
- **Examples** — complete PCG graphs built from primitives ("sample sentences to whole books"); the LLM consults them to reproduce or generalize.
- **Skills** — distilled, non-inherent knowledge ([[agent-skills]]); e.g. a lighting skill encodes "set the sun before the sky," and enabling screenshots lets the LLM iterate visually toward a look.

This produced a fully parametric city generated entirely via PCG + prompts in ~a day (vs. weeks for the Matrix Awakens city), plus an "instant" fire-and-forget `Instance` function that runs a pre-made PCG graph without leaving a trace in the level.

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

### Extension via reflection & async (5.8)

- **Reflection-driven JSON:** Unreal's reflection system (UStruct/FProperty, plus Python) auto-generates both **JSON Schema** (type definitions) and **JSON data** (values) for your toolset. Your function signature *is* the schema — tooltips, min/max metadata, enums, nested structs/arrays all bundle automatically. TAs, TDs, and test engineers can author tools without engine-programmer boilerplate. ^[raw/transcripts/from-words-to-worlds-unreal-mcp-unreal-fest-2026.md]
- **Async results:** toolsets are internally asynchronous, but UFunctions are fire-and-forget. Return `UToolCallAsyncResult` (subclasses for string/image/custom) to return results over the wire without blocking the editor.

### Toolset / skill / example best practices

- **Toolsets:** design clean APIs (name args well, write tooltips, pick good types) as if for a smart junior programmer ≈ an LLM. Be *complete* (CRUD: setters need getters and list-ers), *composable* (modular, not monolithic/on-rails), and *communicative* (return informative error paths — in Python/C++ — so the LLM can self-correct rather than silently failing). **Skills:** keep them novel, collegial, durable, and parsimonious (see [[agent-skills]]). **Examples:** use *static* templates (e.g. effects) or *dynamic* discovery (toolsets inspect/read assets; the skill tells the LLM to find and read examples) for fungible domains like gameplay.

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

## Shipping & availability

Announced with UE 5.8: the **MCP server**, the tool sets and skills, and an example **semantic-search** implementation; the **PCG primitives plugin** (spatial operations, examples, `Instance` fire-and-forget calls); and **Unreal Engine skills for the Claude Code plugin**. Planned: the **City Sample PCG plugin** as a later release (targeted end of summer 2026). Epic expects the work to be self-contained so projects can integrate or cherry-pick, and stresses that features useful to users generally prove useful to LLMs (and vice versa). ^[raw/transcripts/from-words-to-worlds-unreal-mcp-unreal-fest-2026.md]

## See also

- [[mcp]] — the open protocol Unreal MCP implements.
- [[agent-skills]] — the distilled-knowledge layer (skills) of the MCP workflow.
- [[rag]] — adjacent LLM-grounding mechanism (retrieval vs. live tool access).
