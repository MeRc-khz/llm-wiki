# LLM Wiki Schema

## Domain
This wiki covers **AI Research, Multi-Agent Systems, and Personal Knowledge Management (PKM) with LLMs**. It compiles knowledge on AI models, agentic workflows, software development, and the tools/infrastructure supporting autonomous intelligence.

## Conventions
- **Filenames:** Lowercase, hyphens, no spaces, ending in `.md` (e.g., `agentic-workflows.md`).
- **Frontmatter:** Every wiki page must begin with a YAML frontmatter block (defined below).
- **Links:** Use `[[wikilinks]]` for internal navigation. Every new page must have at least 2 outbound links, and relevant existing pages must be updated to link to the new page.
- **Update Policy:** When updating a page, always update the `updated` field in the frontmatter. If a new source introduces contradictory claims:
  1. Record both perspectives with dates/sources.
  2. Mark in frontmatter: `contradictions: [other-page-slug]`.
  3. Set `contested: true` and flag in the log/lint.
- **Provenance Markers:** On pages that synthesize 3+ sources, append `^[raw/articles/source-file.md]` to key paragraphs to track source claims back to the exact immutable raw files.

## YAML Frontmatter Template

### Wiki Pages (entities, concepts, comparisons, queries)
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query
tags: [from taxonomy below]
sources: [raw/articles/source-name.md]
confidence: high | medium | low
contested: false | true
contradictions: []
---
```

### Raw Sources (raw/articles, raw/papers, raw/transcripts, raw/audio, raw/video)
```yaml
---
source_url: https://example.com/source # (for web/youtube clips)
source_file: "raw/audio/file.mp3"     # (for local audio/video files)
ingested: YYYY-MM-DD
sha256: <hex digest of raw file or transcript body>
media_type: article | paper | audio | video
duration: "HH:MM:SS"                 # (for audio/video sources)
---
```

## Tag Taxonomy
All tags used must belong to this predefined taxonomy. To add a tag, document it here first.

### Categories:
- **Models:** `model`, `architecture`, `benchmark`, `fine-tuning`, `inference`
- **Agents:** `agentic`, `orchestration`, `workflow`, `framework`, `tool-use`
- **PKM & Design:** `pkm`, `knowledge-base`, `wiki-pattern`, `methodology`
- **Infrastructure:** `database`, `rag`, `vector-search`, `mcp`
- **Media Ingest:** `podcast`, `audio-processing`, `video`, `music`, `lyrics`, `transcript`
- **Meta:** `comparison`, `historical-timeline`, `controversy`

## Page Thresholds
- **Create a Page:** When an entity/concept is central to one source, or is mentioned across 2+ separate sources.
- **Merge/Update:** Add information to an existing page rather than making a near-duplicate.
- **Split:** When any page exceeds 200 lines, extract sub-topics into separate pages and link them.
- **Archive:** If a page is entirely deprecated or superseded, move it to `_archive/` and remove from the index.
