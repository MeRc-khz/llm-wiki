---
source_url: https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor
ingested: 2026-08-04
sha256: c6d566fdd6fb341d89f416bc252c41b656bdc001b8cb5a3d3099fe6dfb5c1383
media_type: article
---

Unreal MCP embeds an MCP server inside the Unreal Editor process so that any MCP-compatible AI agent, such as Claude Code, Cursor, or the MCP Inspector, can drive the editor over a local HTTP connection. The plugin exposes engine functionality, such as spawning actors, configuring lighting, creating material instances, inspecting Slate widgets, and running automation tests, as Tools that an AI agent can invoke on the user's behalf and is also easy to extend with your own custom tools.

> **NOTE**
Keep in mind that many features are incomplete or missing. APIs and data formats are subject to change at any time as it matures.

The plugin's identifier in the engine source tree, .uplugin files, C++ symbols, and console commands is ModelContextProtocol. The friendly name Unreal MCP is what surfaces in the Plugin Browser and in this documentation.

Toolsets and tools are not implemented by Unreal MCP itself; instead, the AllToolsets plugin must be used to enable them.

## What is the Model Context Protocol?

The Model Context Protocol (MCP) is an open specification published at modelcontextprotocol.io. It defines how an AI client talks to an MCP server using a small set of JSON-RPC message types: initialize, tools/list, tools/call, and similar. A server advertises three kinds of primitives:

- Tools are named functions the client can call, with typed parameters and return values.
- Resources are read-only data the client can fetch by a Uniform Resource Identifier (URI).
- Prompts are reusable prompt templates.

Unreal MCP is an MCP server: it advertises Tools backed by Unreal Engine functionality and accepts connections from any client that speaks the protocol.

The plugin runs inside the editor process. By default, the server only accepts connections from the same machine, has no authentication layer, and is not designed for remote use. The exact binding behavior is documented under Limitations and Known Issues.

A key function of the MCP server is to synchronize external requests with the Unreal Engine game thread by executing Tool invocations on the game thread serially, meaning clients should not issue overlapping Tool calls.

## Setup

Setup follows these primary steps:

- Enable the Unreal MCP and All Toolsets plugins.
- Configure auto-start.
- Generate a client configuration file.
- Start the AI agent from the project root.
- [Optional] Use the integrated Terminal plugin to run the AI agent, keeping the entire workflow inside the editor.

### Enable the plugins

Open Edit > Plugins, search for Unreal MCP, and check the Enabled box. Search for All Toolsets plugin and check the Enabled box. These plugins depend on the Toolset Registry plugin, which is enabled automatically. Restart the editor when prompted.

> **NOTE**
The All Toolsets plugin is a convenient way to load all of the default toolsets for Unreal Engine. However, if you only want certain toolsets to be available, you can find and enable them individually.

*[Image: Enable the Unreal MCP Plugin in the Plugins browser.]*

### Configure auto-start

Open Edit > Editor Preferences, scroll to the General group, and select Model Context Protocol. The panel exposes the Auto Start Server setting. When enabled, the MCP server starts automatically every time the editor launches and binds to http://127.0.0.1:8000/mcp.

The same panel also exposes the listening port (default 8000) and the URL path (default /mcp) for environments where those defaults conflict with another local service. The server name advertised in serverInfo.name is always unreal-mcp.

*[Image: In Editor Preferences, enable Auto Start Server under Model Context Protocol.]*

To start the server on demand instead, leave Auto Start Server off and enter ModelContextProtocol.StartServer in the editor console. The command also accepts an optional port: ModelContextProtocol.StartServer 8000.

### Generate a client config

Each AI agent expects its server list in a specific file format and at a specific location in the project tree. The plugin writes that file directly. From the editor console (open with the backtick key by default), enter:

```
ModelContextProtocol.GenerateClientConfig ClaudeCode
```

The command writes .mcp.json to the project root with the correct entry pointing at the running server. The supported client names are ClaudeCode, Cursor, VSCode, Gemini, Codex, and All. Use All when configuring multiple agents at once:

```
ModelContextProtocol.GenerateClientConfig All
```

The generated .mcp.json for Claude Code looks like this:

```
{
  "mcpServers": {
    "unreal-mcp": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

JSON-format configs (Claude Code, Cursor, VS Code, Gemini) are merged with any existing entries, so running the command repeatedly is safe. The TOML config used by the Codex CLI is write-once: the command refuses to overwrite an existing file, and a stale config must be removed by hand.

### Connect from your AI agent of Choice

To connect, launch your preferred AI agent CLI or application from the project or workspace root where the configuration files were generated. For specific connection steps and advanced settings, please refer to the documentation for your chosen AI client.

If you’re having trouble connecting You can try the following:

If your AI agent CLI or application does not find Unreal MCP, please verify that it was launched from the project or workspace root where the configuration files were generated.

Try launching your AI agent of choice after the editor launches, or you might need to reconnect the MCP. You can do it by:

1. Launch the Unreal Editor, making sure the MCP started.
1. Launch an AI agent (one that listens to the MCP from the editor) in the workspace root.

### Optional: One-shot Using the Terminal Plugin

The Terminal plugin embeds a fully functional terminal panel inside the editor and supports running shell commands automatically when the panel opens. Combined with Unreal MCP, this allows the entire workflow to stay inside a single editor window.

To set up the Terminal Plugin:

1. Open Edit > Plugins, search for Terminal. Restart the editor for changes to take effect.
1. Open Editor Preferences > General > Terminal.

Within the Terminal editor preferences, add entries to the Startup Commands list with the following in this order:

1. Set the terminal type so the AI agent CLI detects a capable terminal.  Warning: Without this, claude and similar CLIs fall back to a degraded mode and may emit raw escape sequences instead of formatted output.
1. Change to the directory where GenerateClientConfig wrote .mcp.json (the project root in installed builds, the workspace root in source builds).
1. Set an AI agent CLI to use. In this example, set claude

The explicit cd is what makes the recipe portable: the Terminal panel starts new sessions in FPaths::RootDir(), which is the workspace root in source builds and the engine installation directory in installed builds, so the working directory does not always match where .mcp.json lives.

*[Image: Enter the command ModelContextProtocol.GenerateClientConfig]*

*[Image: Look at the log to see the output has been written.]*

## Quick Start

With the server running and an AI agent connected, you can begin interacting with Unreal Engine.

To start, try a simple question to confirm your AI agent is connected and receiving context from the editor, such as:

- "What actors do I have selected?"
- "What are a few things you can do in Unreal?"

The rest is up to you! Results may vary depending on the AI agent you use.

### Toolsets and the Toolset Registry

The plugin discovers Tools by querying the Toolset Registry, an Unreal Engine subsystem provided by a sibling plugin of the same name.

A Toolset is a class that derives from UToolsetDefinition (or unreal.ToolsetDefinition in Python) and exposes one or more functions marked as Tool calls.

The Toolset Registry collects every such class at startup, Unreal MCP wraps each Tool call as an MCP Tool, and the wrapped Tool becomes available to every connected MCP client. The registry is consumed by other AI surfaces in the engine, so a toolset authored for MCP works without modification for those.

## Authoring MCP Tools

There are two ways to add a Tool to the running server. The first is the recommended path and should fit nearly every case. The second is for advanced cases where reflection-driven discovery does not fit.

## Recommended Path Using the Toolset Registry

A toolset is a class that derives from unreal.ToolsetDefinition (Python) or UToolsetDefinition (C++) and groups related Tools. Both languages are first-class; pick whichever fits the work. Most of the toolsets shipped with the Toolset Registry plugin, including SceneTools, ActorTools, MaterialInstanceTools, and ObjectTools, are authored in Python.

Users working in Claude Code can scaffold a new toolset of either language with the create-toolset skill from the unreal-mcp Claude Code plugin. The conventions described below still apply once the scaffold lands; the skill simply removes the boilerplate.

#### Authoring in Python

Python toolsets live as .py modules under any plugin's Content/Python/ directory. The registry discovers them at startup. The shipped ActorTools (currently in Engine/Plugins/Experimental/ToolsetRegistry/Content/Python/toolset_registry/toolsets/core/actor.py) is short enough to walk through:

```
import unreal
import toolset_registry
from toolset_registry.toolsets.core.utils import require_editable

@unreal.uclass()
class ActorTools(unreal.ToolsetDefinition):
    """Provides tools for inspecting and modifying actors, including
    their transforms, labels, parent-child relationships, and components."""
```

The following conventions apply:

- The @unreal.uclass() decorator exposes the class to Unreal Engine reflection. The class inherits from unreal.ToolsetDefinition.
- The class docstring describes the toolset itself and surfaces as the toolset's grouping description.
- Each Tool function carries the @toolset_registry.tool_call decorator and is declared @staticmethod. Functions without @toolset_registry.tool_call are not advertised.
- Parameter and return type hints (unreal.Actor, str, bool, list[str], dataclasses, etc.) drive the JSON Schema the Tool advertises.
- The function docstring uses Google style with Args: and Returns: blocks. The description text and per-argument descriptions are reflected into the Tool's schema and should be written with the same care as the public surface of any other API.

#### Authoring in C++

C++ toolsets follow the same pattern under different syntax. Derive from UToolsetDefinition, mark the class UCLASS(BlueprintType, Hidden), and expose static UFUNCTION(meta = (AICallable)) methods. Doc comments on the function and on each parameter are reflected into the schema in the same way as Python docstrings.

A complete shipped example is UAttributeSetToolset in the GASToolsets plugin (Engine/Plugins/Experimental/Toolsets/GASToolsets/Source/GASToolsets/Private/AttributeSetToolset.h). It exposes two AICallable functions with plain USTRUCT return types and no asynchronous behavior. Note that GASToolsets is an experimental engine plugin that ships disabled by default; enabling it surfaces an experimental-feature warning prompt the first time.

Reach for C++ when:

- A Tool needs engine functionality not exposed to Python.
- A Tool's signature uses USTRUCT or other reflected types not cleanly expressible through Python type hints.
- A Tool is hot enough that the Python-to-engine boundary cost matters.

#### After authoring

Run ModelContextProtocol.RefreshTools from the editor console to force the plugin to re-poll the registry. For C++ Tools, Live Coding picks up changes to existing function bodies; adding a new UFUNCTION requires a full editor restart.

The following guidelines produce Tools that AI clients consume reliably, regardless of language:

- Keep functions small and focused. One Tool, one responsibility.
- Prefer descriptive function names and structured return types over free-form strings. Structured types serialize to JSON Schema with field-level types and descriptions; free-form strings carry no schema and force the client to parse them itself.
- To exclude a function that lives inside a toolset from being advertised, omit @toolset_registry.tool_call (Python) or add meta = (AIIgnore) (C++).

### Direct registration

For cases where reflection-driven discovery is not enough (Tools whose schemas are determined at runtime, Tools that come and go dynamically, or Tools backed by data outside the type system), implement IModelContextProtocolTool directly and register the implementation:

```
TSharedRef<IModelContextProtocolTool> Tool = MakeShared<FMyDynamicTool>();
IModelContextProtocolModule::GetChecked().AddTool(Tool);
```

The caller takes responsibility for deregistration when the Tool's lifetime ends. The interface methods are invoked on the game thread (the HTTP server is ticked from the core ticker), the same as for Toolset Registry-discovered Tools.

## Configuration Reference

### Editor Preferences: Model Context Protocol)

| Property | Default | Description |
| --- | --- | --- |
| Auto Start Server | false | Start the MCP server automatically on editor startup. |
| Server Port Number | 8000 | Port the server binds to on 127.0.0.1. |
| Server URL Path | /mcp | URL path the server serves under. |
| Enable Tool Search | true | When enabled, tools/list returns the three meta-tools (list_toolsets, describe_toolset, call_tool) instead of every Tool schema. See the Tool Search concept. |

### Console commands

|  |  |
| --- | --- |
| ModelContextProtocol.StartServer [port] | Start the server, optionally overriding the port. |
| ModelContextProtocol.StopServer | Stop the server and close all sessions. |
| ModelContextProtocol.RefreshTools | Re-poll registered tool providers. Use after authoring or hot-reloading toolsets. |
| ModelContextProtocol.GenerateClientConfig <Client|All> | Generate a config file for the named MCP client in the project root. |

### Command-line Flags

| Flag | Description |
| --- | --- |
| -ModelContextProtocolStartServer | Start the server during editor or commandlet startup, regardless of the Auto Start Server setting. |
| -ModelContextProtocolPort=N | Override the listening port (1..65535). Falls back to the Server Port Number setting if invalid. |

### Console Variables

| Console Variable | Type | Default |  |
| --- | --- | --- | --- |
| ModelContextProtocol.WrapPODToolResultsInObject | bool | true | Wrap primitive Tool results in {"result": ...} for clients that expect object-shaped responses. |
| ModelContextProtocol.AudioResultOggFormat | bool | false | Encode audio Tool results as OGG instead of WAV. |
| ModelContextProtocol.ProgressIntervalSeconds | float | 1.0 | Minimum interval between MCP progress notifications. |
| ModelContextProtocol.PaginationPageSize | int32 | 0 | Maximum items per paginated response. 0 disables pagination and returns all items. |
| ModelContextProtocol.EnableAnalytics | bool | true | Gate telemetry emission. |

## Debugging

Output Log on startup. When auto-start is enabled, the server logs its bind address, port, and URL path to the Output Log during editor initialization. A failure to bind (port already in use, missing dependent plugin, etc.) surfaces there. This is the first place to look if the server does not appear to be running.

LogModelContextProtocol log category. All plugin output flows through LogModelContextProtocol. Raise the verbosity with Log LogModelContextProtocol Verbose in the editor console.

MCP Inspector. The MCP Inspector is the official debugging client for any MCP server, published as a npx command. When a Tool fails to appear, returns the wrong shape, or reports a protocol-level error, point the Inspector at the running server: it lists every advertised Tool with its declared schema and provides a form-style invocation surface that bypasses any AI agent's interpretation of the request.

You can launch the Inspector with npx @modelcontextprotocol/inspector.

When the Inspector window opens, point it at http://127.0.0.1:8000/mcp over the Streamable HTTP transport.

ModelContextProtocol.RefreshTools. The plugin caches the toolset list at startup. After authoring a new toolset, hot reloading a changed function body, or activating a Game Feature Plugin that contributes toolsets, run this command to force a re-poll. After Live Coding a toolset method, a connected client may still hold the old Tool schema; run RefreshTools and reconnect the client.

## Editor and runtime availability

The plugin is split across three modules. ModelContextProtocol and ModelContextProtocolEngine are runtime modules: they own the server, the protocol implementation, the settings, and the StartServer, StopServer, RefreshTools, and GenerateClientConfig console commands. ModelContextProtocolEditor is editor-only and is responsible only for the auto-start hook and for adapting Toolset Registry-discovered toolsets into MCP Tools.

The server is therefore not strictly tied to the editor. Cooked and shipping game builds can host an MCP server by calling IModelContextProtocolModule::StartServer() at startup.

## Tool Search

By default, the plugin runs in tool-search mode (bEnableToolSearch = true). In this mode, tools/list returns three discovery meta-tools rather than every advertised Tool:

| Tool-Search Mode | Description |
| --- | --- |
| list_toolsets | Returns the available toolset names and descriptions. |
| describe_toolset | Returns the schemas for a named toolset. |
| call_tool | Dispatches a named toolset’s Tool with the supplied arguments and returns the result on the same turn. |

The agent walks this discovery path on demand, which keeps tools/list responses small even when the registry exposes hundreds of Tools. Setting this to false reverts to advertising every Tool eagerly, at the cost of a much larger initial schema payload. Tool authors should not rely on Tools being advertised eagerly; the tool-search path is the default a connecting agent will see.

The tool-search meta-tools themselves are part of the editor-only adapter. Cooked-build hosts that register Tools through IModelContextProtocolModule::AddTool() directly advertise them eagerly regardless of the bEnableToolSearch setting.

## Limitations and Known Issues

- Supports HTTP and Server-Sent Events only. The stdio and WebSocket transports are not supported.
- Loopback only by default. The HTTP listener binds per [HTTPServer.Listeners] DefaultBindAddress (default localhost), and the server rejects non-loopback Origin headers. There is no authentication layer; the plugin is not safe to expose beyond the local machine.
- MCP Resources and Prompts are not advertised by any shipping toolset.
- The Toolset Registry adapter is editor-only. Cooked and shipping builds can host an MCP server (see Editor and runtime availability) but Tools shipped through the registry are not auto-discovered there; they must be registered explicitly through IModelContextProtocolModule::AddTool().
- Live Coding does not propagate new UFUNCTION declarations. Adding a Tool requires an editor restart.

## See also

- Model Context Protocol specification
- MCP Inspector
