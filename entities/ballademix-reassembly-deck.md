---
title: Ballademix Reassembly Deck
created: 2026-10-25
updated: 2026-10-25
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

## Fixed during bring-up

- **The clock reported the wrong master length** — `0:00.000 / 4` instead of `/ 4:57`. The formatter
  stripped `:mm.sss` instead of only the milliseconds.
- **The overflow notice was misleading** — "drag them in or split" implied a drag could fit an 828 s stem
  onto a 297 s timeline. Now: *"stem(s) run longer than the master — slide to align a section"*.
- **HTTPS was missing**, so Chrome auto-upgraded and the deck died on `chrome-error://`. Certbot now
  covers `ballademicz.com/.store/.shop/.us`. Never test a browser page over plain HTTP and trust the result.

## Related

* [[ballademix]] — the parent project and its Solana NFT mechanics.
* [[bzrlnx-paperchasers-campaign]] — the social serial whose 24 clips are the same stems.
* [[bzr-intro-component]] — the canvas intro used as the brand sting on the campaign clips.
