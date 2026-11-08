---
title: Ballademix Reassembly Deck
created: 2026-10-25
updated: 2026-11-08
type: entity
tags: [music, agentic, video]
sources: []
confidence: high
contested: false
contradictions: []
---

# Ballademix Reassembly Deck

A **single-file, browser-based "fake DAW"** for the [[ballademix]] project: it lets a listener play the
released stems of the record *"I Know Why"* and **slide each waveform along a shared timeline** to
reassemble the song by ear. There is no backend and no build step — one `index.html`, HTML Canvas for
the UI, and the **Web Audio API** for playback, so the waveforms drawn are the real decoded PCM, not
a generated image.

Live: `https://ballademicz.store/daw/` (also `ballademicz.com` / `.shop` / `.us`) — served from
`/var/www/ballademicz/html/daw/`, `ballademicz.conf`.

## Why the Web Audio API is load-bearing

The point is *precision alignment*, so the waveform has to come from the same samples that play. Each
stem is fetched, `decodeAudioData()`'d, and reduced to min/max peak buckets (`PEAKS_PER_SEC = 90`);
the canvas renders those buckets. The playhead and the audio clock read from the same
`AudioContext.currentTime`, so what you see is what you hear.

## Design decisions

- **The master defines the timeline.** `segment_01` is track 1, **locked and muted**, with its waveform
  still visible. It is the reference marker every other stem is aligned against — the timeline length
  is always `segment_01`'s duration (297.3 s).
- **Sliding is the only edit.** For a released stem the sole user action is dragging its clip
  horizontally (`at`, in seconds). Solo / mute / lock / volume / pan sit alongside, but nothing else
  about the audio is mutable.
- **Locking is enforced in three places** — the clip body refuses to drag, the M/S buttons refuse, and
  the master cannot be unmuted. A locked track is forced to `effMuted`.
- **Solo re-computes mute globally**: any soloed (unlocked) track silences every other unlocked track.
- **Stems that outrun the master are surfaced, not hidden.** `segment_17a`/`17b` are ~828 s against a
  297 s timeline; the footer warns rather than silently clipping.

## Playback model

Each clip is an `AudioBufferSourceNode` scheduled at an absolute `AudioContext` time when PLAY is
pressed, with a per-track `GainNode` → `StereoPannerNode` chain. PAUSE stops every source and freezes
`pos`; LOOP re-arms the schedule when the playhead reaches the master end; SCRUB on the ruler stops
sources, sets `pos`, and resumes on release.

## Verified behaviour (2026-10-25, headless Chrome against the live URL)

| Feature | Result |
|---|---|
| Decode + render | 25 tracks, all buffers decoded, peaks drawn |
| PLAY / PAUSE | `AudioContext` running, RMS ≈ 0.66 while playing, 0 after pause, sources drained to 0 |
| SCRUB | click at 300 px past the control strip → `pos ≈ 88.1 s` (px/s and offset check out) |
| Drag to align | `segment_02` `at` 0 → 41.13 s |
| Volume / pan | volume bar sets `vol` 0.5; pan lane sets `pan` 0.20 |
| Mute / solo | toggles flip `muted`, and solo force-mutes all other unlocked tracks |
| LOOP | from `pos 294.3` wraps to `1.2` and keeps playing |

## Bugs fixed during bring-up

- **Master-duration display.** `fmt(masterDur).replace(/:\d{2}\.\d{3}$/,'')` stripped the minutes too,
  so the clock read `0:00.000 / 4`. The intent was to drop milliseconds only — corrected to
  `.replace(/\.\d{3}$/,'')`, giving `0:00.000 / 4:57`.
- **Misleading overflow copy.** "drag them in or split" implied a drag could make an 828 s stem fit a
  297 s timeline. Reworded to "stem(s) run longer than the master — slide to align a section".

## The 17a / 17b lanes

`segment_17.wav` is **one** 828 s beat+drums bed, not two separated stems. A 10 s RMS sweep shows a hard
energy step — the first ~267 s sit around **-7 dB** and everything after drops to **-17 dB** — so the
file is cut there rather than at a blind midpoint:

| lane | file | span | length |
|---|---|---|---|
| 17a | `daw/audio/segment_17a.wav` | 0 – 267.0 s (loud section) | 267.0 s |
| 17b | `daw/audio/segment_17b.wav` | 267.0 – 828.0 s (quieter section) | 561.0 s |

Both are 16 kHz mono PCM with a 10 ms fade at the cut, matching the rest of the stem set. **The labels
are deliberately `17a BEAT+DRUMS A` / `17b BEAT+DRUMS B`, not "beat sample" / "drum track"** — calling
two halves of one bed by two instrument names would misdescribe what plays. Swap in real separated stems
and relabel once they exist.

## Game layer (2026-10-25)

- **Format:** 26 stems as 80 kbps mono mp3 — **106.5 MB -> 25.0 MB**. Sealed lanes are not fetched at all.
- **Master template:** where each stem belongs on the timeline. Seeded from envelope cross-correlation
  (mean 0.33 — honesty required), per-stem confidence stored, and **calibratable in-deck**: drag by ear,
  `SAVE POSITION`, persisted in localStorage. Lag-0 and lyric-matching were both tried and falsified —
  `segment_01` has only 57 words in 297 s, so the master is nearly all instrumental.
- **Mechanics:** ghost marker at the target; glow within 5 s; green inside 1.2 s; release snaps exactly
  and stamps the lane SOLVED; footer keeps score (`n/24 placed`).
- **Identity:** lanes named by assembly position (`01/24`), each with its social image as a thumbnail
  cell; an in-lane video plays when the playhead crosses a clip that has a finished cut.
- **Test-run drawer:** shipped clips beside the makeufamo.us test runs, side by side.

## Fixed during bring-up

- **The clock reported the wrong master length** — `0:00.000 / 4` instead of `/ 4:57`. The formatter
  stripped `:mm.sss` instead of only the milliseconds.
- **The overflow notice was misleading** — "drag them in or split" implied a drag could fit an 828 s stem
  onto a 297 s timeline. Now: *"stem(s) run longer than the master — slide to align a section"*.
- **HTTPS was missing**, so Chrome auto-upgraded and the deck died on `chrome-error://`. Certbot now
  covers `ballademicz.com/.store/.shop/.us`. Never test a browser page over plain HTTP and trust the result.

## Current state (2026-11-08)

The deck has moved on from the original 25-lane / 297 s release. It is now a **21-lane, 92-bar / 245.33 s**
deck at **90 BPM**, and it is the engine behind [[the-deck-saas-platform]].

| Change | State |
|---|---|
| Lane count | **21** — master + 17A SAMPLE + 17B MELODY + 18 chopped stems. The four lanes with no 92-bar chop (`segment_02, _20, _21, _24`) were **removed**. |
| Master row height | **3× the other lanes** — 186 px vs 62 px. Row layout, hit-testing, clip drawing, trim handles, drag overlay, scrollbar and wheel scrolling all use per-row height. |
| Loop region | The ruler carries a loop with drag handles. Dragging a grip moves a boundary, dragging the band slides the whole loop, `LOOP` wraps playback at the loop end. The pad sequencer takes its length from the loop (4-bar loop → 4 bars / 64 steps). |
| Numbering | Ruler labels, master clock, seq playhead and loop label are **1-indexed**, matching the sequencer. The old split convention made A04 read "bar 6" on the timeline and "BAR 7" in the seq. |
| SAMPLE lane switch | `PADS` / `ORIG` in three places (header, lane pill, drawer header), one state (`PADSEQ.on`). Persists in the deck payload. |
| Leading silence | Every stem trimmed to its first audible sample on load; `TRIM SILENCE` re-runs it. Idempotent. 19 stems carried heads totalling 1259.894 s. |
| Snap | `SNAP` cycles BAR / BEAT / TICK (default TICK). Sliding a clip and both trim handles land on the grid; readout speaks bar:beat:tick. |
| Audio fix | `audio/segment_17a.mp3` was a **dead export** (245.33 s, peak 0.0000). Rebuilt from `segment_17.mp3`'s first 92 bars — corr 1.0000 with both 17A and pad A01. Silent original backed up at `/root/.hermes/cache/scratch/segment_17a_silent.bak.mp3`. |
| Admin dashboard | `/daw/admin/`, single file, IndexedDB `thedeck-admin`. Campaign, stem photos as data URLs, stem lyrics, video NFT manifest. See [[the-deck-saas-platform]]. |

**Still open:** pads run to 98 bars against a 92-bar master (default cap); five stems overrun bar 92
(`03, 04, 05, 06, 15`, default re-cut); master lane plays `segment_01` while pads tile `segment_17`
(default re-cut pads); gamified layer (combo/streak, 24 levels, stars, leaderboard) not built.

## Related

* [[the-deck-saas-platform]] — the social music SaaS product line built on this engine.
* [[ballademix]] — the parent project and its Solana NFT mechanics.
* [[bzrlnx-paperchasers-campaign]] — the social serial whose 24 clips are the same stems.
* [[bzr-intro-component]] — the canvas intro used as the brand sting on the campaign clips.
