---
title: LLM Wiki Pattern
created: 2026-05-25
updated: 2026-05-25
type: concept
tags: [wiki-pattern, pkm, knowledge-base]
sources: [raw/articles/llm-wiki-pattern-introduction.md]
confidence: high
contested: false
contradictions: []
---

# The LLM Wiki Pattern

The **LLM Wiki Pattern** is a novel methodology for building and maintaining personal or team [[pkm|knowledge bases]] using LLMs. Developed as a compounding, persistent alternative to standard [[rag]], it shifts the effort from "retrieving and synthesizing on every query" to "compiling knowledge once and keeping it current." (For a side-by-side breakdown of the trade-offs, see [[rag-vs-llm-wiki|RAG vs. the LLM Wiki Pattern]].)

## Core Idea: Compounding vs. Rediscovering

In traditional RAG or doc-chat interfaces (e.g., NotebookLM, ChatGPT uploads), the LLM starts from scratch for every question. It must find relevant fragments, resolve contradictions, and build a synthesis in real time, forgetting everything once the session ends.

The **LLM Wiki Pattern** introduces a persistent, interlinked wiki (using markdown files) that sits between the raw sources and the user. The LLM acts as the **curator, librarian, and programmer** of this wiki:
- **Incremental Integration:** When a new source is added, the LLM reads it, updates relevant entity/concept pages, notes contradictions, and links information together.
- **Compounding Artifact:** The knowledge is pre-compiled. Cross-references are resolved, and contradictions are flagged *before* you ask a question.
- **Obsidian Integration:** The markdown-based repository functions natively as an Obsidian vault, allowing the human to browse pages, click links, and view the graph network in real time.

## Division of Labor
- **The Human:** Sourcing raw materials, exploring the network, directing analysis, and guiding the synthesis.
- **The LLM Agent:** Heavy lifting, summarizing, bookkeeping, link validation, formatting, and file indexing.

## Architecture: The Three Layers

1. **Raw Sources (Layer 1):** Immutable files (articles, transcripts, PDFs, images) that serve as the ground truth. The LLM reads these but never edits them.
2. **The Wiki (Layer 2):** Directory of LLM-generated markdown files, categorised into `entities/`, `concepts/`, `comparisons/`, and `queries/`.
3. **The Schema (Layer 3):** Standard rules, file-naming conventions, and metadata structures (e.g., `SCHEMA.md`) that make the LLM a disciplined wiki maintainer.

## Core Operations

- **Ingest:** Reading a raw source (including audio/video sources through [[media-ingestion]]), updating affected entity/concept pages (often touching 10-15 files), and logging the changes.
- **Query:** Answering questions based on the pre-compiled wiki rather than searching raw chunks, and filing high-value syntheses back into the wiki.
- **Lint:** Auditing the wiki to find orphan pages, dead links, missing tags, stale claims, and unresolved contradictions.

## Navigation & Tracking
- **`index.md`:** Content-oriented, alphabetical list of all pages and one-line summaries.
- **`log.md`:** Chronological record of all actions (e.g., `## [2026-05-25] ingest | Article Title`).
