---
title: RAG vs. the LLM Wiki Pattern
created: 2026-07-08
updated: 2026-07-08
type: comparison
tags: [comparison, rag, wiki-pattern]
sources: [raw/articles/llm-wiki-pattern-introduction.md]
confidence: high
contested: false
contradictions: []
---

# RAG vs. the LLM Wiki Pattern

Both approaches ground LLMs in external knowledge. They differ on *when* the synthesis happens and *who* pays the compute.

## Dimensions

| Dimension | [[rag|RAG]] | [[llm-wiki-pattern|LLM Wiki Pattern]] |
|-----------|-------------|----------------------------------------|
| Synthesis timing | Every query, from scratch | Once, at ingest time |
| State across queries | Stateless (forgets) | Persistent, compounding |
| Source of truth | Vector chunks at query time | Pre-compiled interlinked pages |
| Contradiction handling | Resolved live, per query | Flagged *before* you ask |
| Best for | Huge raw corpora, no curation budget | High-value, curated, evolving knowledge |
| Human role | Asks questions | Sources + directs curation |
| Agent role | Retrieves chunks | Curator, librarian, linker |

## Verdict
RAG excels when you must query a massive, unstructured corpus without investing in curation — but it re-derives relationships on every call and leaves contradictions for the model to resolve under time pressure. The LLM Wiki Pattern shifts that cost forward: the agent compiles, links, and flags once, so queries hit a clean, navigable graph (a native [[pkm|Obsidian]] vault). They are not mutually exclusive — RAG can front the raw layer while the wiki sits on top as the curated layer.

This wiki is the artifact: 24 sources compiled into 29 pages, maintained by the ingest / query / lint cycle documented in [[llm-wiki-pattern]]. For the inverse comparison from the RAG side, see [[rag-vs-llm-wiki|RAG vs. the LLM Wiki Pattern]].
