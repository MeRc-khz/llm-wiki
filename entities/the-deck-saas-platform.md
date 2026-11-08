---
title: The Deck — Social Music SaaS Platform
created: 2026-11-08
updated: 2026-11-08
type: entity
tags: [music, monetization, video, solana, agentic]
sources: []
confidence: high
contested: false
contradictions: []
---

# The Deck — Social Music SaaS Platform

**The Deck** is a social music SaaS product line from **bzrlxnzzz** (the [[bizarre-lynx]] brand) built on the
[[ballademix-reassembly-deck]] engine. A musician uploads a **deck** — the same shape as the 92-bar package:
a tempo, a melody track, a drum track, a master track, and the stems — and the platform chops the melody
and drums into sample pads and positions the clips on a shared timeline. The artist/owner then runs a
**campaign** and ties in their social platforms for the **NFT video releases**.

Live admin: `https://ballademicz.com/daw/admin/`
Live deck: `https://ballademicz.com/daw/`
Source: `/var/www/ballademicz/html/daw/` (git repo `MeRc-khz/ballademix`, branch `main`).

## The upload unit: a deck

| Part | Role in the deck |
|---|---|
| **tempo** | BPM that defines bar length. The current deck runs **90 BPM**, so a bar = 2.6667 s, a beat = 0.6667 s, a tick = 0.1667 s. |
| **master track** | Locked, muted timeline reference. Everything aligns against it. Currently **92 bars / 245.33 s**. |
| **melody track** | The melodic bed; also chopped into pads. |
| **drum track** | The rhythm bed; also chopped into pads. |
| **stems** | The released pieces the listener reassembles. |

## What the platform does to an upload

1. **Chops melody and drums into sample pads.** The current deck ships **49 contiguous 2-bar tiles**
   (`A01`…`A49`) cut sample-exact from the source bed, each encoded with delay compensation so audio
   starts at sample zero. Seam dead air went from 54.9 ms to ≤2 ms.
2. **Positions clips on the timeline.** Every clip carries an `at` in seconds; dragging slides it and
   both trim edges land on the grid.
3. **Snaps to bar:beat:tick.** A `SNAP` control cycles **BAR / BEAT / TICK**, default **TICK**. The drag
   readout speaks **bar:beat:tick**, 1-indexed to match the sequencer.
4. **Trims leading silence.** Each stem is trimmed to its first audible sample on load and its clip
   moves to that sample's real timeline position; `TRIM SILENCE` re-runs the pass over every lane and
   every duplicate clip. It is idempotent.

## Campaign layer (admin dashboard)

The admin page is a **single-file** dashboard at its own route (`/daw/admin/`). Persistence is browser
**IndexedDB**, database `thedeck-admin`, object stores `campaign` and `stems`.

### Campaign
Name, **start date**, **frequency** (daily / weekly / every 2 weeks / monthly), release count, social
handles (X, Instagram, TikTok, YouTube), and a **post template** with placeholders
`{{title}} {{n}} {{count}} {{date}} {{link}} {{stem}}`. The release schedule is generated from start
date + frequency; each row is one stem release and shows photo/lyrics readiness pills.

### Stems
Per stem: title, **photo uploaded as a data URL**, **lyrics text**, and an optional **video URL**.
Stats count stems / photos / lyrics so the owner can see what is still missing.

### Video NFT manifest
`buildManifest()` emits JSON: platform, version, generatedAt, the campaign block (including the dated
schedule), and a per-stem block with `id, label, title, kind, bars, audio, photo, lyrics, video` plus an
`nft` object (`name, description, image, animation_url, attributes[]`). Download as
`the-deck-manifest-YYYY-MM-DD.json`, or copy to clipboard.

### Verified live (2026-11-08, headless Chrome against the live URL)

| Check | Result |
|---|---|
| Campaign save | stored `{name, startDate, frequency, count}` in IndexedDB |
| Schedule | weekly 4 → 11-15/11-22/11-29/12-06; biweekly → 11-15/11-29/12-13/12-27; monthly → 11-15/12-15/2027-01-14/2027-02-13 |
| Photo upload | PNG accepted as `data:image/png;base64,…` (8 014 chars), thumbnail rendered |
| Lyrics + video | saved and returned in the stems store |
| Manifest | 35 740 chars, parses, stem 03 carries photo + lyrics + `animation_url` |
| Download | `the-deck-manifest-2026-11-08.json`, 35 892 bytes, `application/json` |
| Reload persistence | campaign and stems both restored |
| Console errors | 0 |

### Bug found and fixed during bring-up
The IndexedDB `tx()` helper resolved `out.result` only when it was not `undefined`. A `get` on an empty
store resolves `undefined`, so the helper returned the **`IDBRequest` object** itself, which then got
written back as the stems payload and threw `DataCloneError: IDBRequest object could not be cloned`.
Fixed by testing `"result" in out` instead of comparing to `undefined`, plus a guard in `loadAll()` so a
request object can never be adopted as state.

## Open product decisions

1. **Master vs pad source.** Pads are cut from `segment_17`, the master lane plays `segment_01`, and the
   declared master `segment_17a` was a silent export (since rebuilt from 17's first 92 bars). Default:
   re-cut pads from `segment_01`.
2. **98 pad bars vs 92-bar map.** Last 6 bars run past the master. Default: cap at 92.
3. **Five stems overrun bar 92** — `03, 04, 05, 06, 15`. Default: re-cut.
4. **Gamified layer not built** — combo/streak, 24 levels, stars, leaderboard.

## Related
* [[ballademix-reassembly-deck]] — the single-file fake DAW this product line runs on.
* [[ballademix]] — the parent record and Solana NFT mechanics.
* [[bzrlnx-paperchasers-campaign]] — the social serial whose clips are the same stems.
* [[bizarre-lynx]] — the brand and agent identity behind bzrlxnzzz.
