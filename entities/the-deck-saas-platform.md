---
title: The Deck — Social Music SaaS Platform
created: 2026-11-08
updated: 2026-11-13
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
5. **Bounded trim handles.** Dragging a clip's head cannot pass its first audible sample (the `lead`),
   and the tail cannot pass the source end. Both schedulers also hard-clamp `offset`/`dur` to the
   buffer window, so an out-of-range read can no longer wrap and replay the opposite end of the sample
   (the "drag the begin, hear the end" bug).

## Deck builder (admin dashboard)

The admin's **Deck Builder** tab is a form over the deck's autosave slot
(`ballademix-daw` / store `deck` / record name `__last__`). It reads the saved payload, renders one
control group per lane, and writes the edited payload back. The deck applies it on the next reload.

Per lane:

* **Start — bar:beat:tick** (bar 1-indexed, beat 1–4, tick 1–16) writes `at`.
* **Length — bar:beat:tick** (bar 0-indexed, beat 0–3, tick 0–15) writes `dur`.
* **Trim head (s)** writes `offset`, clamped to `[lead, buffer − 1 tick]`.
* **+ front / + back** reveal *n* ticks of audio before the head or after the tail, clamped to the real
  source window. A no-op reports why ("head sits at the lead" / "tail sits at the source end").
* **Apply** commits the form to the lane; **Reset** restores the saved values; **Revert edits** reloads
  the whole saved payload.

**Save deck** writes the payload with `adjusted: true`, which tells the deck to skip its legacy
trim-repair heuristics so hand-set `at`/`dur`/`offset` survive a reload. The optional **Also update
template targets** checkbox also rewrites the calibrated `template` map so the game layer's targets
follow the new alignment. The payload also now carries per-lane `lead` and `buf` so the builder can
bound its controls to the real audio.

## Product structure — catalog, albums, songs

The full project structure is defined in [[the-deck-catalog-saas-structure]]. In short:

```
User → Catalog (public profile) → Album → Song (a deck: tempo + master + melody + drums + stems)
```

* **Catalog** — the user's site profile at `/{handle}`; albums, songs, bio, followers.
* **Album** — a collection of songs with cover, release date, description.
* **Song** — one deck. The master track is the full song (buy); the stems are the clips (unlock / buy).
* **Feed** — newly published songs across catalogs, each card carrying play / favorite / load-into-deck.
* **Favorites** — the listener's library and the bridge from discovery to arrangement.
* **Deck** — the listener's saved arrangement of a song's unlocked clips, on the bar:beat:tick grid.
* **Ownership** — master NFT + per-stem NFTs (the existing `nft/gate.js` gate), with album bundles and
  campaign drops as additional revenue paths.

## Arrangements, locks, and live collaboration

The next layer up from the catalog is defined in [[the-deck-arrangements-lane-locks]]:

* **Arrangements are the sharable asset.** Each song has a **master arrangement** (first, all clips
  unlocked, placed from the admin `TEMPLATE`) and any number of named user arrangements forked from it.
  Buying the master track unlocks the master track, the master arrangement, and every clip.
* **Unpaid players are not blocked.** They get the `alwaysOn` reference lanes (drum bed + sample) and any
  stems they hold, and can save their own arrangements over that base.
* **Lane locks preserve the essence.** Creator locks a lane, a drum voice (hi-hat / snare / kick), or a
  single clip; the lock blocks edits by others but never mutes or hides the lane. Everything unlocked
  stays free for the listener to add drums, upload samples, record device vocals, and add piano-roll
  instrument tracks.
* **A song can be one drum pattern.** The minimal publishable song is a deck with a single MIDI drum
  sequence lane and no audio — its first arrangement is the pattern from the drum sequencer.
* **P2P drum collaboration.** Two users open the same sequencer over a WebRTC data channel with one
  host-authoritative clock; edits travel as events, audio never crosses the wire.

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
schedule), and a per-stem block with `id, label, title, kind, bars, audio, photo, lyrics, video`, a
`timeline` block (`start`, `end`, `lengthSeconds`, `lengthBars`, `startBBT`, `endBBT`, `snapped`), plus
an `nft` object (`name, description, image, animation_url, attributes[]`). Download as
`the-deck-manifest-YYYY-MM-DD.json`, or copy to clipboard. The timeline is read from the deck's live
autosave payload, so admin alignment edits flow straight into the NFT manifest.

### Deck builder verified live (2026-11-11, headless Chrome against the live URL)

| Check | Result |
|---|---|
| Form render | 2 synthetic lanes rendered with correct start/length readouts (`1:1:01`, `92:0:00`) |
| Start edit | `segment_03` moved to bar 51:1:1 = 133.333 s; readout and end updated |
| Length edit | 10 bars 2 beats = 28.000 s; end 161.333 s |
| + back (4 ticks) | length 28.000 → 28.667 s |
| + front (4 ticks) | start 133.333 → 132.667 s, offset 140 → 139.333 |
| Save deck | payload written with `adjusted: true`, `at 130`, `dur 29.3333`, `offset 139.3333` |
| Template checkbox | `template.segment_03` rewritten to 130 |
| Revert edits | form returned to the saved 130 after a 106 edit |
| Deck reload | live deck applied `at 130 / dur 29.3333 / offset 139.3333`; `fmtBBT(159.3333)` = `60:4:01` |
| Manifest | stem 03 `start 130`, `startBBT 49:4:01`, `endBBT 60:4:01` |

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
* [[the-deck-catalog-saas-structure]] — the catalog → album → song → deck hierarchy, feed, favorites, and ownership/monetization model.
* [[the-deck-arrangements-lane-locks]] — named arrangements, the master arrangement, lane/voice locks, listener layering, and P2P drum collaboration.
* [[ballademix-reassembly-deck]] — the single-file fake DAW this product line runs on.
* [[ballademix]] — the parent record and Solana NFT mechanics.
* [[bzrlnx-paperchasers-campaign]] — the social serial whose clips are the same stems.
* [[bizarre-lynx]] — the brand and agent identity behind bzrlxnzzz.
