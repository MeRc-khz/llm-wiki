---
title: Agent Skills
created: 2026-08-04
updated: 2026-08-04
type: concept
tags: [agentic, tool-use, workflow, framework]
sources: [raw/transcripts/from-words-to-worlds-unreal-mcp-unreal-fest-2026.md]
confidence: medium
contested: false
contradictions: []
---

# Agent Skills

**Agent Skills** is an open standard for giving an AI agent distilled, task-specific knowledge it needs but doesn't inherently have. In the context of Unreal Engine 5.8, Epic added a native class for it — `UAgentSkill` — taking the same semantics and spirit as the skills used by tools like Claude Code and making it Unreal-native. Confidence is **medium** — single-source, fast-moving standard.

## Unreal's native implementation

- `UAgentSkill` is a new UClass. Deriving from it creates a skill in **C++**, **Python**, or **Blueprints**.
- Blueprint skills become **U assets**, so they can be checked into the project and shared like any other asset.
- Skills are essentially a "big bucket of text," but because they're UObjects they support **programmatic skill-text construction**: override a function invoked whenever the skill text is read, letting the skill inject/append project context dynamically before the agent sees it.
- Used heavily by the [[unreal-mcp]] world-building workflow (e.g. a "lighting skill" encoding that you set the sun before the sky) to make the LLM perform tasks reliably.

## Writing good skills (best practices)

- **Novel:** add information the LLM can't get elsewhere. If a tool already returns it, or it's all over the internet, don't put it in a skill. Focus on proprietary, surprising, domain-specific knowledge.
- **Collegial:** write like you'd talk to a colleague, not didactically script it. LLMs are smart and tokens are precious — short conversational notes ("set the sun before the sky, then check the clouds") outperform long instructional text.
- **Durable:** avoid hard-coding property/function names that can change — skills are pure text and can't be programmatically verified against renames, so they go stale silently.
- **Parsimonious:** every token counts; keep it to the information needed and no more.

## See also

- [[unreal-mcp]] — the MCP stack in which skills are authored and consumed.
- [[mcp]] — the protocol layer underneath.
