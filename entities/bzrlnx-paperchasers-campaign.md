---
title: BzrLnx Paperchasers Campaign
created: 2026-10-24
updated: 2026-10-24
type: entity
tags: [agentic, workflow, media]
sources: [raw/transcripts/paperchasers-master.md]
confidence: high
contested: false
contradictions: []
---

# BzrLnx Paperchasers Campaign

The **BzrLnx Paperchasers campaign** is the audience-building / advertising outreach run for
the [[bizarre-lynx|Bizarre Lynx]] persona. It turns the 24 segments of the
[[furious-styles-coupe-da-villian|Paperchasers]] master recording into a serialized set of
short-form vertical videos, each pairing one audio segment with a photo of Coupe's younger
self, animated into a lip-synced talking head. The serial framing is the `n/24` counter on
every clip; the tail of every clip carries the [[makeufamous|MakeUFamo.us]] BZR Lnx intro
sequence as a brand sting.

## Pipeline (verified end-to-end 2026-10-24)

1. **Talking head.** Photo + audio segment → **`heygen/avatar-iv`** on [[openrouter-video-generation|OpenRouter]].
   Avatar IV is the only OpenRouter video model with modality `text+image+audio->video`: it
   lip-syncs a supplied audio track to a single photo rather than synthesizing its own speech.
   Every other model (Veo 3.1, Kling v3, Wan 3.0, Seedance 2.5, Hailuo 3) generates audio from
   a text script and cannot rap a real vocal.
   * Request shape — `POST /api/v1/videos`, `input_references: [{type:"image_url",...},{type:"audio_url",...}]`.
   * **The audio reference must be a public HTTPS URL** (`Only HTTPS URLs are allowed`); an image
     *can* be a `data:` URL. Serve audio from an nginx web root.
   * 1080p, 9:16, 25 fps out. Figure ~$0.05/video-second (measured: 27.2 s → $1.3576).
2. **`n/24` badge.** PIL-generated 1080×1920 RGBA overlay (`@BZRLNX` + `NN/24`, amber `#f5b800`),
   composited with `ffmpeg overlay`.
3. **Intro sting.** The [[bzr-intro-component|bzr-intro]] canvas renderer
   (`bzrqr-renderer.js`) is seekable — `draw(ctx, p, env)` is pure in `p` — so the 4.4 s sting is
   produced by stepping `p` 0→1 and capturing `canvas.toDataURL()` from a same-origin harness page,
   then encoding with ffmpeg. Capturing must happen **same-origin** with the assets or the canvas
   taints and `toDataURL()` throws.

## Segment inventory and cost

The 24 segments total **1673.7 s (27.9 min)**. Two are outliers — `segment_01` (297 s) and
`segment_17` (828 s) — long pieces, not ~25 s verses like the rest. Full-run model cost at
$0.05/s is **$83.68**; with 01 and 17 trimmed to ~30 s each it is **≈$30**. Budget accordingly.

## Scheduling

The `n/24` counter is a countdown device: a **serial drop converts far better than a bulk dump**,
because every clip ends with a reason to follow the next. (First recommendation was daily; the
agreed cadence is M/W/F — see below.)

## Strategy — the stem-reassembly mechanic

Every posted clip is a **stem of the record "Paperchasers — I Know Why"** in the
[[ballademix]] project, not a standalone video. The premise: a viewer who collects all 24 clips —
pulls the audio into a DAW, or sequences the video — can **reassemble the original song**. The
`n/24` counter is therefore doing double duty: it is the serial hook *and* the assembly index. Drop
order is song order, so the numbering must stay faithful to the stems.

Consequences that constrain production:

- `segment_01` is the **finished full song** and is never posted. It becomes the BalladeMix Solana
  NFT.
- `segment_17` is the beat + drums (828 s), split by Coupe into `17a` / `17b` in Audacity. One slot
  becomes two, which is what keeps the drop set at exactly 24 after `01` is removed.
- The **NFT cover art is a composite of the talking-portrait videos** — the campaign's visual output
  is also the NFT's artwork source, so clip framing is NFT art, not just social content.
- **svgdad.store is the monetization surface.** Every clip ends on an `svgdad.store` end card and
  every caption carries the store. IG and TikTok captions are not clickable, so the bio link is the
  entire funnel on those two platforms.

## Scheduling

M/W/F, one clip per drop day — **24 slots = 8 weeks**, 2026-10-26 → 2026-12-18, slot
**18:00 PT / 21:00 ET**, X at 09:00–12:00 PT. Photos are curated per-drop-day rather than
pre-paired, and all output is **9:16 vertical only** until svgdad.store revenue funds other formats.
Slot map and calendar live in `PLANS/BZRLNX_DROP_SCHEDULE.md`; account kit in
`OUTBOX/BZRLNX_ACCOUNT_KIT.md`.

Cost, revised: 22 segments (548.4 s) + two 30 s windows from 17a/17b = **≈$30.42** for the run.

## Related

* [[bizarre-lynx]] — the persona and its social handles.
* [[makeufamous]] — source of the intro sting.
* [[media-ingestion]] — the transcription/splitting pipeline that produced the segments.
