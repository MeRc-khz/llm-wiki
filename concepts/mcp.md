---
title: Model Context Protocol (MCP)
created: 2026-08-04
updated: 2026-08-04
type: concept
tags: [mcp, tool-use, framework, infrastructure]
sources: [raw/articles/unreal-mcp-in-unreal-editor.md]
confidence: high
contested: false
contradictions: []
---

# Model Context Protocol (MCP)

**MCP** (Model Context Protocol) is an open specification for how an AI client (an agent, CLI, or IDE like Claude Code, Cursor, Gemini, Codex, VS Code) talks to an *MCP server* that exposes capabilities of a host application or service. Published at modelcontextprotocol.io.

## Core primitives

A server advertises three kinds of primitives over a small set of JSON-RPC message types (`initialize`, `tools/list`, `tools/call`, and similar):

- **Tools** — named functions the client can call, with typed parameters and return values (schema-driven).
- **Resources** — read-only data the client can fetch by a URI.
- **Prompts** — reusable prompt templates.

## Transport

The protocol is transport-agnostic; implementations support different transports (Streamable HTTP, SSE, stdio, WebSocket). A given server typically supports a subset (e.g. an editor-hosted server may expose only HTTP + Server-Sent Events).

## Role in agentic workflows

MCP standardizes how agents reach out of the model context and into external systems (editors, files, databases, tools). It is complementary to, not a replacement for, [[rag]]: RAG retrieves grounding content into context, while MCP gives the agent live access to callable tools/resources. This makes it a foundational layer for [[agent-skills]] and editor/tool orchestration.

## See also

- [[unreal-mcp]] — an MCP server embedded inside Unreal Editor exposing engine functionality as Tools.
- [[rag]] — retrieval-augmented generation, an adjacent mechanism for grounding agents.
