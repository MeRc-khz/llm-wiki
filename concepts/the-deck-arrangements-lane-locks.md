---
title: The Deck — Arrangements, Lane Locks, and Realtime Collaboration
created: 2026-11-13
updated: 2026-11-13
type: concept
tags: [music, monetization, workflow, game-dev, community]
sources: []
confidence: high
contested: false
contradictions: []
---

# The Deck — Arrangements, Lane Locks, and Realtime Collaboration

This page defines how a **song** in [[the-deck-catalog-saas-structure]] becomes plural: many saved
arrangements, creator-owned lane locks, layering by the listener, and a shared drum clock between two
browsers. It extends the catalog hierarchy (User → Catalog → Album → Song) with the unit the platform
actually sells and shares — the **arrangement**.

## 1. An arrangement is the shareable asset

A **song** is a deck (tempo + master + melody + drums + stems). An **arrangement** is one saved
placement of that deck: every lane's `at` / `dur` / `offset`, its mute/solo/mix state, and any MIDI note
data. The deck already persists exactly this shape (`lib/store.js` — the `deck` preset payload; the
`__last__` autosave slot is a single unnamed arrangement). The catalog layer moves the record out of one
browser's IndexedDB and into the song, where it can be named, forked, and shared.

Every song is born with one arrangement:

**The master arrangement**

* it is the **first** arrangement of the song, created with the song itself
* all clips are **unlocked and in place**, laid out from the admin's calibrated `TEMPLATE` bar map
* it is named `master`
* buying the master track unlocks **the master track, the master arrangement, and every clip**
* the master track and the master arrangement are the same object — the track is the audio, the
  arrangement is its placement. See §2.

**What a listener without the master gets**

* the `alwaysOn` reference lanes — the drum bed and the SAMPLE pad. `nft/stems.json` marks these
  `alwaysOn` and `nft/gate.js:137` excludes them from stem gating, so they are never sealed
* plus any stems the listener already holds (purchased, campaign drop, or bundle)
* and the right to save **their own named arrangements** over that base

So an unpaid user is not blocked from the platform — they are blocked from the master's specific
placement and from the clips they don't own. They still compose, still save, still share.

A user keeps **N named arrangements per song**, each forkable from any arrangement they can play.

## 2. Placing an arrangement — RESET and SOLVE

The **master track and the master arrangement are the same object seen twice**: the track is the audio,
the arrangement is its placement. Both come from the creator's calibrated `TEMPLATE` map, so the master
arrangement is also the **answer key** for every fork. Two actions read it:

| Action | What it does |
|---|---|
| **RESET** | Every unlocked lane *and every placed duplicate* goes back to `0:00`, so the user can drag the pieces into position by hand. |
| **SOLVE** | Places **every unlocked clip on its master-arrangement position** in one action — one drag per clip replaced by one press. |

They are complements: reset then solve, or reset then place by hand. Neither is a guess — a lane with no
master position (the `alwaysOn` SAMPLE and MELODY lanes carry no `TEMPLATE` entry) is left exactly where
the user put it and reported as such, and a lock holds through both. A clip parked off its target loses
its placed tick, so the count on screen never claims a placement the timeline does not have.

Shipped on the live deck (2026-11-13, commit `ffd38bc`): `RESET` and `SOLVE` sit together in the header,
visible in simple mode. `SOLVE` landed 18 of 18 lanes with master positions exactly on target and left
the 2 without one alone; `RESET` returned 18 clips (lanes + duplicates) to `0:00` while a locked lane
held at `41.5 s`; a reload restored all 18 placements with the score derived, not remembered.


## 3. Creating a song from the user admin

`user admin → album → add song`. Two entry shapes:

| Entry | Shape | Status |
|---|---|---|
| **Full deck upload** | master audio + melody + drums + stems, chopped into pads — the Paperchasers package | current pipeline |
| **Drum-sequencer song** | a deck with **one MIDI drum sequence track and no audio at all** | the minimal publishable unit |

The drum-sequencer song is the important one: it is the smallest thing a creator can ship, and its
**first arrangement is the pattern drawn in the sequencer**. Nothing else is required to publish.

It is also nearly free to build, because the engine already supports a lane with no audio:

* a MIDI lane has no `AudioBuffer` and never will (`index.html:1195`)
* it drives SpessaSynth on channel 9, sharing the deck's one transport (`index.html:2484`)
* `drumseq.exportNotes()` yields `[[pitch, startSec, durSec, vel], …]` (`lib/drumseq.js:65`) — the exact
  payload `store.js` already persists as a `drums` preset (`{tempo, notes}`)

A song with `lanes = [midiDrum]` and no `assets` is therefore a legal song. It is also the cheapest thing
to mint: one pattern, one asset.

## 4. Lane locks

The creator **locks what must survive** downstream arrangement. Three scopes:

| Scope | Granularity | Example |
|---|---|---|
| **lane** | whole track | the master track; a reference drum bed |
| **voice** | one drum pitch | hi-hat `42`, snare `38`, kick `35`/`36` |
| **clip** | one placed clip | a placed sample loop |

A lock is a **write permission**, not a mute and not a gate. A locked lane is still audible, still
visible, still inspectable — it just refuses drag, trim, delete, and note edits from anyone but the
owner. Unlocked lanes stay fully editable, and new lanes can always be added on top.

**Voice-level locking is the point.** "The creator makes a drum pattern and locks the hi-hat, the snare,
and the bass drum to preserve the essence" — the essence lives at the voice level. Locking the whole drum
lane would also freeze the listener's own additions, which is the opposite of the intent. The drum
sequencer already addresses voices by pitch (`DS_NAMES` in `index.html:2488`), so a voice lock is a
`Set` of pitches filtered out of the edit path.

Locks live at two levels, and the difference is who they protect:

* **Song locks** — set by the creator, they apply to the song and every fork of it. This is the essence
  the creator is protecting.
* **Fork locks** — a contributor can lock **their own contribution inside their own fork** (the lane they
  added, the sample they uploaded, the vocal they recorded). Their fork is theirs; the lock keeps a
  collaborator or a remix of that fork from rewriting it.

The engine already has the lane-level primitive: the master is `locked:true, muted:true` by definition
(`index.html:344`), and a not-yet-dropped stem self-locks (`index.html:2122`). Locks generalize that
flag to voice and clip scope.

## 5. The listener's layering surface

Over the locked base, a favoriter (or any player of the song) can add:

| Add | Mechanism already in the engine | New work |
|---|---|---|
| **to the drums** | `drumSeq.setNotes()`; unlocked voices only | voice-lock filter in the editor |
| **a sample** | `lib/sampler.js` pads + `store.js` `samples` store | an upload path into the pads |
| **vocals from the device** | — | `getUserMedia` + `MediaRecorder` → a `vocal` asset |
| **a piano roll track + instrument** | SpessaSynth `WorkletSynthesizer` + `GeneralUserGS.sf3`, `programChange` per channel | a piano roll UI |

The instrument track is the cheapest of the four. The synth is already armed with a full General MIDI
soundfont (`index.html:2502`), so an instrument lane only needs `{channel, program}` plus notes — and
those notes use the same `[pitch, start, dur, vel]` tuple the drum lane already stores. The drum grid
generalizes to a piano roll by swapping the percussion pitch axis for a chromatic one; the transport,
scheduling, and persistence layers are unchanged.

## 6. Realtime: two users, one drum clock

**P2P drum sequencer collaboration** — both users hold the sequencer open, one shared clock, edits land
on both.

The design constraint is the whole design: **do not send clock ticks.** Send the clock's parameters and
the edits.

* **Authority** — one peer is host. The host broadcasts `{tempo, bar, originTime, state}`. There is no
  negotiation and no consensus; a single writer cannot produce a split clock.
* **Local derivation** — each peer derives the playhead from its own `AudioContext.currentTime` against
  the shared origin. This is the pattern the deck already runs: *one clock*, `drumseq` reads the host's
  playhead and schedules hits against it (`lib/drumseq.js` header).
* **Edits as events** — `noteAdd` / `noteRemove` / `tempo` / `voiceLock` are sent as events with a version
  counter; the host applies, echoes, and the guest replays. State sync is a snapshot on join, not a stream.
* **Audio never crosses the wire** — each peer plays its own local soundfont. The wire carries note
  numbers and timing, not samples.
* **Transport** — a WebRTC data channel. Signalling over the Buzz Nostr relay (which we operate), or
  copy-paste SDP for zero infrastructure.

The payoff: latency shows up as a few milliseconds of grid offset on one hit, never as drift, because
there is one origin and each side's read of it is local.

The first game built on this clock is specified in [[deck-horse-sequencer-game]] — basketball H.O.R.S.E.
as call-and-response memory: the setter draws a drum pattern, the matcher reproduces it from memory, and
each round adds a bar.

## 7. Data model additions

```
arrangements        id, song_id, user_id, name, is_master, forked_from,
                    visibility, tempo, created_at, updated_at
arrangement_lanes   id, arrangement_id, lane_id, kind (audio|midi|sampler|vocal),
                    at, dur, offset, muted, solo, vol, pan, channel, program
arrangement_notes   id, arrangement_lane_id, pitch, start, dur, vel
lane_locks          id, song_id, scope (lane|voice|clip), target, locked_by, created_at
collab_sessions     id, song_id, host_id, guest_id, signaling, started_at, ended_at
```

`arrangements` replaces the browser-local `deck` preset record; `master` is the row with
`is_master = true`. `arrangement_notes` is the drum pattern or piano roll payload, keyed per lane so one
song can carry a drum lane and a piano lane independently.

## 8. Ownership rules, restated

| Actor | Can play | Can arrange | Can lock |
|---|---|---|---|
| **Owner** | everything | everything | yes |
| **Bought the master** | master track + master arrangement + all clips | fork into own named arrangements | no |
| **Favorited only** | `alwaysOn` lanes + owned stems | yes, on those lanes | no |
| **Collab guest** | host's unlocked lanes | live edits, host-scoped | no |

Revenue paths are unchanged: master track (which now carries the master arrangement and every clip),
per-stem unlock, album bundle, campaign drop. The master arrangement is what makes the master purchase
worth more than the audio — a buyer gets the authored placement, not a pile of clips.

## 9. Build order

1. **`arrangements` table** + name / fork / save in the deck — replaces the single `__last__` slot.
2. **Master arrangement generated at song creation** from the calibrated `TEMPLATE` map.
   *Shipped in the deck ahead of the table:* `RESET` + `SOLVE` (commit `ffd38bc`) already place a fork
   from the master arrangement on the deck's single autosave slot. The table only changes where the
   record lives.
3. **Lane + voice locks** — stored on the song, enforced in the drag/trim handles and in `drumseq`.
4. **Drum-sequencer-only song** — album → song → pattern, no audio assets required.
5. **Sample upload + device recording** — feed the pads and a new `vocal` lane.
6. **Piano roll track** — instrument lane on SpessaSynth, chromatic grid.
7. **WebRTC drum clock** — host-authoritative, relay signalling, edit events.

## 10. Open decisions

Decided 2026-11-13:

1. **Master immutability** — resolved: the master track *is* the master arrangement, and it is the answer
   key for forks. It is not edited after release; a change is a new arrangement. (§2)
2. **Lock escape** — resolved: no request flow. The creator unlocks at will, and **a contributor can lock
   their own contribution inside their own fork**. Forks keep the lock state they were created under. (§4)
3. **Collab persistence** — resolved: **two forks, one per peer**; each peer saves their own. (§6)
4. **Arrangement resale** — default: share link only, no resale until licensing settles.
5. **Vocal storage** — default: uploaded as a private asset, never surfaced in the public manifest.

## Related

* [[the-deck-catalog-saas-structure]] — the catalog → album → song → deck hierarchy this page extends.
* [[the-deck-saas-platform]] — the shipped deck, admin dashboard, and Deck Builder.
* [[ballademix-reassembly-deck]] — the engine: one transport, drum sequencer, sampler pads, SpessaSynth.
* [[buzz]] — the Nostr relay that can carry the collaboration signalling.
* [[tokenized-equity]] — ownership model if master/stem mints become fractional.