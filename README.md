# LLM Wiki — Knowledge Base

The structured knowledge base powering the Hermes Agent and AgentHTTP.
Contains entities, concepts, and raw source material across all Conglomerate Group projects.

## Structure
- `entities/` — People, projects, companies, creative works
- `concepts/` — Synthesized frameworks and architectures
- `raw/articles/` — Ingested source documents
- `raw/audio/` — Transcribed audio files
- `scripts/` — Ingestion and linting tools

## Usage
```bash
python3 scripts/lint.py        # Validate all pages
python3 scripts/transcribe_audio.py <file>  # Transcribe audio
```
