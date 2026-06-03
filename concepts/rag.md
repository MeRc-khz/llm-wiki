---
title: Retrieval-Augmented Generation
created: 2026-05-25
updated: 2026-05-25
type: concept
tags: [rag, database]
sources: [raw/articles/llm-wiki-pattern-introduction.md]
confidence: high
contested: false
contradictions: []
---

# Retrieval-Augmented Generation (RAG)

**Retrieval-Augmented Generation (RAG)** is an AI architectural pattern where an LLM retrieves relevant document chunks from an external database (such as a vector database) at query time to ground its final generated answer. This pattern is commonly used in traditional [[pkm|knowledge management]] tools.

## Key Attributes & Trade-offs
- **Pros:** Excellent for querying large corpora of raw/unstructured text without fine-tuning models.
- **Cons (RAG-Only):** The model is "stateless" relative to the knowledge—it does not synthesize or compile relationships over time. It has to rediscover knowledge and piece together fragments on every single query.

Patterns like the [[llm-wiki-pattern]] address these limits by incrementally compiling knowledge once and maintaining a persistent, structured, interlinked graph.
