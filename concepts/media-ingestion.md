---
title: Media Ingestion
created: 2026-05-25
updated: 2026-05-25
type: concept
tags: [podcast, audio-processing, video, wiki-pattern]
sources: []
confidence: high
contested: false
contradictions: []
---

# Media Ingestion

**Media Ingestion** is the workflow of taking non-textual source materials—such as **audio files, podcasts, music, and video recordings**—and processing them into searchable, structured markdown pages that can compound within the [[llm-wiki-pattern]].

By enabling media ingestion, the wiki bridges the gap between spoken-word context, sonic features, visual references, and compiled textual knowledge.

## Media Ingestion Pipeline

The process consists of three major stages:

```
[Media Source] ──► [Extraction (ffmpeg)] ──► [Transcription (Whisper)] ──► [Wiki Integration]
(File or URL)       (Lightweight Audio)       (Timestamps & Text)          (Concepts & Links)
```

1. **Stage & Fetch (Layer 1):**
   - Raw media files are stored in `raw/audio/` or `raw/video/` and kept as immutable binary sources.
   - For streaming media (such as YouTube videos, podcasts, and shorts), URLs are resolved and matched against unique video IDs.

2. **Extract & Isolate:**
   - For video files (`.mp4`, `.mkv`), `ffmpeg` extracts the audio track into a single-channel, 16kHz `.mp3` file under `raw/audio/` to minimize transcription file size and overhead.
   - SHA256 hashes are calculated on both the raw media and the resulting transcripts to guarantee file integrity and prevent duplicate processing.

3. **Transcription & Feature Isolation (Speech-to-Text):**
   - **Speech (Podcasts/Videos):** YouTube transcripts are fetched programmatically using `youtube-transcript-api`. Local audio is sent to an external API (like OpenAI/Groq Whisper) or run through a local lightweight model to extract timestamped JSON segments.
   - **Music/Songs:** Transcribed lyrics are matched with structural metadata (intro, verse, chorus). Optional acoustic extractors (such as Librosa or Essentia) can be used to capture bpm, musical key, and sonic mood.

4. **Integration (Layer 2):**
   - The resulting text/transcript is written as a markdown file under `raw/transcripts/`.
   - The LLM parses the transcript, extract key quotes, matches mentioned entities, updates corresponding pages, and logs the activity in `log.md`.

## Active Ingest Tools

- **`fetch_transcript.py`:** Extracts full timestamped transcripts from YouTube URLs.
- **`ingest_media.py`:** A unified orchestration script that routes URLs and local files, extracts video audio via `ffmpeg`, computes SHA256 file-integrity checks, and places metadata stubs.
- **`ffmpeg`:** Handles local media splitting, codec conversion, and sound compression.
- [[rag]]**: Standard Retrieval-Augmented Generation which this pipeline can optionally seed with raw segments.
- [[pkm]]**: Personal Knowledge Management systems which are enriched by multimedia contexts.

## Ingestion Examples
- **Ingested Audio Track:** [Ntrafx Podcast Clip (Feb 13, 2006)](raw/transcripts/ntrafx_pod_feb13_2006_5min_clip.md) — A 5-minute raw audio clip programmatically transcribed using **Gemini 2.5 Flash** and compiled into the [[ntrafx-podcast]] entity page.
- **Ingested Official Music Track:** [MakeUFamo.us Audio (Theme Song)](raw/transcripts/makeufamous-audio.md) — The official R&B/Hip-Hop brand track, programmatically transcribed using the Gemini Files API and mapped to the [[makeufamous-theme-song]] entity page.
- **Ingested Platform Concept:** The **[[makeufamous]]** talent platform illustrates the scaling of media ingestion, where hundreds of thousands of 60-second video submissions are processed, transcribed, and audited autonomously by AI models.


