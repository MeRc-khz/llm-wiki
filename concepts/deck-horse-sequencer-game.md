---
title: The Deck — H.O.R.S.E. on the Drum Sequencer
created: 2026-11-14
updated: 2026-11-14
type: concept
tags: [music, game-dev, workflow, community]
sources: []
confidence: high
contested: false
contradictions: []
---

# The Deck — H.O.R.S.E. on the Drum Sequencer

## 1. What it is

Basketball H.O.R.S.E. as call-and-response memory on the drum sequencer: one player **sets** a pattern
("takes a shot"), the other **matches** it from memory ("attempts the same shot"). The setter draws; the
matcher reproduces. Builds on the two-user drum session in [[the-deck-arrangements-lane-locks]] §6 (one
host, one clock, edits as events) and runs on the engine documented in [[ballademix-reassembly-deck]].

**This is a design for an unbuilt feature.** No game code exists; everything below is specified against
the shipped sequencer and transport it will reuse.

The matcher never plays audio of their own — they enter steps into the grid and submit; the host replays
both. One transport (`lib/drumseq.js:1-22`), one owner (`index.html:2677-2700`).

## 2. Match structure

Two players. Round 1 = **1 bar (16 steps)**. Each **round adds a bar**. The setter's pattern is the shot;
the matcher's submission is the attempt. A correct submission **swaps the roles** — the successful matcher
becomes the next setter and chooses: a new pattern, or **build on the existing one** (one bar longer).

Either player may set the opening round; host picks first by default.

| Event | Effect |
|---|---|
| Matcher reproduces the pattern exactly | Roles swap; new setter chooses *new* or *extend* |
| Matcher misses | +1 strike; same setter keeps the shot |
| Strikes reach the limit | Match over; other player wins |

**Strikes = 3 by default.** Note plainly: the basketball game is spelled H-O-R-S-E (five letters / five
misses). The owner chose **three**. Make the count a single knob `MATCH_STRIKES`, default `3`.

## 3. The two phases per round

Each round has exactly two phases on the shared transport.

| Phase | Who acts | What happens |
|---|---|---|
| **LISTEN** | matcher | Pattern plays on the shared clock; the grid renders it; a visible countdown runs |
| **REPRODUCE** | matcher | Grid clears; matcher places steps from memory; SUBMIT |

**LISTEN duration N. Default: `N = bars × 4 s`.** More bars means more steps to hold, so more time; the
linear rule is the simplest that scales. Mark it as a default to tune, not a derived constant. It is one
knob, `LISTEN_SECONDS_PER_BAR`, default `4`.

During LISTEN the grid shows the setter's pattern read-only (cells `on`, unclickable). During REPRODUCE
the grid shows only the matcher's entries. The countdown is on screen for both players.

## 4. Judging

The **host judges, authoritatively** — a single verdict, broadcast, no dispute protocol (§6).

Judging is a **DIFF, not pass/fail**. The verdict reports, per item:

| Diff class | Meaning |
|---|---|
| **missing** | step in the target that the submission lacks |
| **extra** | step in the submission that the target lacks |
| **wrong voice** | a step at the right index but a different pitch |
| **wrong velocity band** | pitch+step match, velocity lands in a different band |

**Exact-match rule per step: on `(pitch, step index)`.** A step is correct iff some submitted hit shares
the target hit's pitch and step. Velocity is **advisory** — reported, banded, not a failing condition by
default (see §8). Sub-step offsets are ignored: the grid is step-space (`STEPS_PER_BAR = 16`,
`lib/drumseq.js:24`), and drawn hits land dead on the step (`lib/drumseq.js:8-9`).

Why a diff: the player must see *what* they got wrong to learn the instrument, and the diff is exactly
what the "reveal a voice" power-up shows (§5). A binary pass/fail teaches nothing and cannot power the
reveal.

## 5. Power-ups

Three, one of each available at match start.

| Power-up | Effect | Timing |
|---|---|---|
| **pass** | decline to set; the other player sets; **no strike** | before setting |
| **2× time** | double the **remaining** LISTEN window | during LISTEN |
| **reveal a voice** | reveal one voice's steps (one pitch row) during REPRODUCE | during REPRODUCE |

**2× time** doubles what is left, not the whole N — adopting it late gets less.

**reveal a voice** exposes one voice's row from the diff/target — a `DS_NAMES` pitch
(`index.html:2592-2594`) whose cells light up for the matcher.

**Economy (a knob):** one of each at match start; **earn one more per successful match** (the winner
chooses which), **cap 3**. `POWERUP_EARN_PER_WIN = 1`, `POWERUP_CAP = 3`.

## 6. Network model

Rides the shared-clock rule already written in the parent page, [[the-deck-arrangements-lane-locks]] §6 —
**do not stream clock ticks; send the clock's parameters and the edits.**

* **One host, single writer.** The host owns the **transport origin** and is the sole authority. It
  broadcasts `{tempo, bar, originTime, state}`; no negotiation, no split clock.
* **Round state in, submission out.** The host broadcasts round state (`phase`, `bars`, `N`, `strikes`,
  whose turn). The matcher sends **one submission snapshot**; the host diffs it (§4) and broadcasts the
  verdict.
* **The setter's pattern travels as a snapshot, in one message, on round start.** Never as a stream of
  `noteAdd`/`noteRemove` edits — the game needs the target whole, not its edit history.
* **Audio never crosses the wire** each peer plays its own local soundfont
  (`index.html:2605-2617`). The wire carries `[pitch, start, dur, vel]` tuples, not samples.
* **Transport** a WebRTC data channel, signalling over the Buzz Nostr relay or copy-paste SDP (parent §6).
* **Target drop.** When REPRODUCE begins, the matcher's client **drops the target pattern** from the live
  edit path — the grid no longer holds it. **Be honest: this is client-side.** A determined player can
  still read the pattern from their own memory or dev tools. This is a game for fun, not for stakes; the
  drop protects the honest player's experience, not the state.
* **Disconnect** default: the match is **abandoned, no strike** (§8).

## 7. What already exists to build on

| Piece | Where | Real detail |
|---|---|---|
| Sequencer API | `lib/drumseq.js:23` | `createDrumSeq(host)` → `open`, `setNotes`, `notes`, `export`, `load`, `setTempo` |
| Note tuple | `lib/drumseq.js:65-71` | `exportNotes()` → `[[pitch, startSec, durSec, vel], …]`, sorted by start |
| 16 steps / bar | `lib/drumseq.js:24` | `STEPS_PER_BAR = 16`; grid is step-space |
| One clock | `lib/drumseq.js:1-22`, `193-229` | `pump()` fires what the host playhead passes; reads the host, never schedules its own |
| Transactional swap | `lib/drumseq.js:306-319` | `load(notes, tempo)` rebuilds + `setNotes`; `setNotes` reloads from an array |
| Preset record | `lib/store.js:8` | `drums` payload = `{ tempo, notes:[[pitch,startSec,durSec,vel],…] }` |
| Preset I/O | `index.html:3386-3395`, `3436-3448` | `saveDrumPreset` / `loadDrumPreset` (bound to the `drums` store) |
| Live drum payload | `index.html:3165-3171` | `drumPayload()` → `{ tempo, notes }` from `drumSeq.export()` |
| Transport the seq reads | `index.html:2677-2700` | the `host` object: `play/stop/position/seek`, `audio.now()`, `noteOn` |
| Synth (local audio) | `index.html:2605-2617` | `WorkletSynthesizer` + `GeneralUserGS.sf3` on channel 9 |
| Voice names | `index.html:2592-2594` | `DS_NAMES` maps pitch → name (the "reveal a voice" row label) |
| Store singleton | `index.html:3150-3160` | `presetStore` = `createStore()`; IndexedDB, localStorage fallback |
| Shared-clock design | parent §6 | host-authoritative, local derivation, edits as events |

## 8. Open decisions

1. **Time rule per round** — `N = bars × 4 s` proposed; tune the constant, or make it per-voice-count.
2. **Is velocity judged?** — default: advisory only (banded, reported, non-failing). Decide whether a
   wrong band counts as a miss.
3. **Extend or replace?** — a successful matcher *may* extend the existing pattern (one bar longer) or
   replace it. Decide whether extend is mandatory past some round.
4. **Earned or drafted?** — power-ups earned per win (default) vs drafted at match start.
5. **Disconnect mid-round** — default: match abandoned, no strike. Decide whether the standing player
   wins.

## Related

* [[the-deck-arrangements-lane-locks]] — the parent design; §6 is the P2P clock this game rides.
* [[ballademix-reassembly-deck]] — the engine: one transport, drum sequencer, SpessaSynth.
* [[the-deck-saas-platform]] — the shipped deck and admin this game would live in.
* [[buzz]] — the Nostr relay that can carry the game's signalling.
