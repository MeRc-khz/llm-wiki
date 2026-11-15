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

**Shipped and playable** at `ballademicz.com/daw/horse/` — hot-seat since 2026-11-14 (commit
`2310d1a`), **two browsers since 2026-11-15** (commit `7054b71`). The whole match loop — SET → LISTEN →
REPRODUCE → diff → role swap → three-strike ending — runs on the shared clock in the browser, with the
power-ups and the verdict panel live, and a networked match signals over the Buzz relay and then plays
peer to peer over a WebRTC data channel (§6). Local two-player hot seat is still there and is the
default; nothing touches the network unless somebody presses HOST or JOIN.

It is a **separate route, not a mode inside the deck**, because the deck currently ships no MIDI drum
lane (`TRACKS` has no `midiDrum` entry) — a drum-sequencer song is still the unbuilt half of §3 of
[[the-deck-arrangements-lane-locks]]. The page drives `lib/drumseq.js` headless instead: it never calls
`open()`, so the sequencer's editor UI is never mounted, and `toggle` / `export` / `load` / `pump` are
the API. One transport, owned by the page and read by the sequencer, exactly as the deck runs it.

The matcher never plays audio of their own — they enter steps into the grid and submit; the host replays
both. One transport (`lib/drumseq.js:1-22`), one owner (`index.html` `initDrums()` (`createDrumSeq` host)).

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
(`index.html` `DS_NAMES`) whose cells light up for the matcher.

**Economy (a knob):** one of each at match start; **earn one more per successful match** (the winner
chooses which), **cap 3**. `POWERUP_EARN_PER_WIN = 1`, `POWERUP_CAP = 3`.

## 6. Network model

Rides the shared-clock rule already written in the parent page, [[the-deck-arrangements-lane-locks]] §6 —
**do not stream clock ticks; send the clock's parameters and the edits.** Built 2026-11-15
(`horse/net.js`, commit `7054b71`).

### The split of authority

| Role | Owns | Sends |
|---|---|---|
| **Host** | the clock, the round, the strikes, the verdict | one `sync` carrying the whole public state, after every change |
| **Guest** | its own grid and its own submission — nothing else | intents: `lock`, `submit`, `power`, `earn`, `choose`, `continue` |

One writer for the match state, so the two peers cannot disagree about whose turn it is. The state that
travels is the whole public record — `phase, round, bars, setter, matcher, strikes, stock, target,
revealed, verdict, listenMs` — because a snapshot cannot partially apply and a stream of deltas can.
The target travels as **one snapshot**, never as `noteAdd`/`noteRemove` edits: the game needs the shot
whole, not its history.

The **host ends the listen**, not each client. A guest that ran its own phase machine would drift from
the host's clock and could clear its grid at a different moment than the verdict arrives.

### Signalling: the Buzz relay

* **Kind `24900`** — inside the ephemeral range (20000–29999), so the relay routes it through Redis
  fan-out and **never stores it**. Verified after a full match: `select count(*) from events where
  kind = 24900` → `0`.
* **Channel `horse-signal`** (open visibility). The relay's channel fan-out is keyed on the **`h` tag**;
  a `#t`-only selector matches nothing, and `#t` alongside `#h` is not enforced. So `h` is the selector
  and the `t` tag (`horse-<code>`) is carried for the clients to read.
* **A fresh keypair per page load.** `pubkey_allowlist_enabled` and `require_relay_membership` both
  default to `false` in this deployment, so any key can NIP-42 authenticate, and an **open-visibility**
  channel admits any authenticated pubkey even though the channel-membership check is real
  ("member OR open-visibility channel").
* **Subscribe only after the NIP-42 handshake settles.** A `REQ` sent before auth is refused with
  `CLOSED`, and an unhandled `CLOSED` looks exactly like "the peer never answered" — this cost a full
  debugging round; the client now surfaces `CLOSED` and re-subscribes.
* **One offer, one answer, non-trickle ICE.** Both sides wait for `iceGatheringState === "complete"`
  (bounded at 4 s) and put the whole SDP in one event each. The host re-publishes its offer every 2.5 s
  until an answer lands, because an ephemeral event that arrives before the guest subscribes is gone.
* **The payload is AES-GCM encrypted with the match code** (PBKDF2-SHA256, 150k iterations, fixed salt).
  The channel is open, so anyone on the relay can *read* these events, and an SDP carries the peers' IP
  addresses. The code is therefore the capability: private code, private match.
  **Honest limit:** a 6-character code is ~31 bits, so this keeps eavesdroppers out, not attackers. It is
  a game, not a secret. Anyone who guesses the code can also inject a competing answer.
* **No signalling library.** `@noble/secp256k1` is vendored (MIT) for BIP-340 schnorr; event ids use
  `crypto.subtle`; the relay client is ~90 lines of `["EVENT"/"REQ"/"AUTH"]` over a WebSocket.

### Still true from the design

* **Audio never crosses the wire** — each peer plays its own local soundfont (`index.html` `armDrums()`).
  The wire carries `[pitch, start, dur, vel]` tuples.
* **Target drop.** When REPRODUCE begins the matcher's client drops the target from the live edit path.
  **Client-side, stated plainly:** a player with dev tools on their own machine can still find it. The
  drop protects the honest player's experience, not the state.
* **A timer ends the listen, not the frame loop.** `requestAnimationFrame` stops in a backgrounded tab,
  so a network host whose window was hidden would never fire its own phase change and would stall both
  players. The listen now ends on a `setTimeout`.
* **Disconnect** — the match is abandoned, no strike. Verified: the surviving peer stays in phase with
  `strikes: [0, 0]`.

## 7. What already exists to build on

| Piece | Where | Real detail |
|---|---|---|
| **The game** | `horse/index.html` | SET / LISTEN / REPRODUCE / verdict / choose / over, the grid, the diff, the power-ups, the strikes |
| Sequencer API | `lib/drumseq.js:23` | `createDrumSeq(host)` → `open`, `setNotes`, `notes`, `export`, `load`, `setTempo` |
| Note tuple | `lib/drumseq.js:65-71` | `exportNotes()` → `[[pitch, startSec, durSec, vel], …]`, sorted by start |
| 16 steps / bar | `lib/drumseq.js:24` | `STEPS_PER_BAR = 16`; grid is step-space |
| One clock | `lib/drumseq.js:1-22`, `193-229` | `pump()` fires what the host playhead passes; reads the host, never schedules its own |
| Transactional swap | `lib/drumseq.js:306-319` | `load(notes, tempo)` rebuilds + `setNotes`; `setNotes` reloads from an array |
| Preset record | `lib/store.js:8` | `drums` payload = `{ tempo, notes:[[pitch,startSec,durSec,vel],…] }` |
| Preset I/O | `index.html` `saveDrumPreset()` / `loadDrumPreset()` | `saveDrumPreset` / `loadDrumPreset` (bound to the `drums` store) |
| Live drum payload | `index.html` `drumPayload()` | `drumPayload()` → `{ tempo, notes }` from `drumSeq.export()` |
| Transport the seq reads | `index.html` `initDrums()` (`createDrumSeq` host) | the `host` object: `play/stop/position/seek`, `audio.now()`, `noteOn` |
| Synth (local audio) | `index.html` `armDrums()` | `WorkletSynthesizer` + `GeneralUserGS.sf3` on channel 9 |
| Voice names | `index.html` `DS_NAMES` | `DS_NAMES` maps pitch → name (the "reveal a voice" row label) |
| Store singleton | `index.html` `initPresets()` | `presetStore` = `createStore()`; IndexedDB, localStorage fallback |
| Shared-clock design | parent §6 | host-authoritative, local derivation, edits as events |

`index.html` is edited constantly, so it is cited by **symbol**, not by line — a line number there
goes stale within a day. `lib/drumseq.js` and `lib/store.js` change rarely and keep their line
numbers.

## 8. Decisions and what is still open

Settled 2026-11-14:

| Question | Decision |
|---|---|
| Time per round | `bars × 4 s` — default kept. KNOB `LISTEN_SECONDS_PER_BAR` |
| Is velocity judged? | No. Advisory only; exact match is `(pitch, step)` |
| Extend or replace? | **The winner's choice, every round** — `NEW PATTERN` or `BUILD ON IT (+1 BAR)` |
| Disconnect mid-round | Match abandoned, no strike — verified over the wire |
| Strikes | 3. KNOB `MATCH_STRIKES` |

Still open:

1. **The kit is fixed at four voices** (kick / snare / hat / open hat) so the board stays legible. A
   16-row kit + a scrolling board would need a different reveal affordance.
2. **Power-up economy** — one of each at start, one earned per win, cap 3. Unexercised in a real match
   against a human; tune it when matches have been played.
3. **Two players only.** The protocol has no room list, no spectators and no reconnection — if a peer
   drops the match is over. Three-way H.O.R.S.E. would need the host to address more than one guest.
4. **Music-aligned timing across the wire.** Each side still starts its own transport when the phase
   message lands, so the two peers can be up to one network RTT apart in *pattern playback*. The judging
   is unaffected (it is step-based, not audio-based), but two musicians playing together would want the
   host to publish a start time and each side to schedule against its own clock offset.

## 9. Verified live

### The two-browser match (2026-11-15, commit `7054b71`)

Two headless Chrome tabs, a real host and a real guest, every control clicked with dispatched pointer
events; 0 console errors on both. Signalling went through the live relay and the play went over the data
channel:

```
A hosts           code BNL8RU  · status "signalling"
B joins           types the code, status "waiting for the host's offer"
connect           A "connected — peer to peer"   B "connected — peer to peer"
                  distinct signalling keypairs: true
relay log (A)     signal in: answer · ice: connected · match on — player 1 sets
relay log (B)     signal in: offer  · ice: checking · ice: connected
both in           set / set · A is player 1 · B is player 2
A draws 4 hits    B receives the shot: phase listen · 4 target notes · 4 painted cells · 3.58 s left
host clock ends   B phase reproduce · target cells painted: 0 (hidden) · entry 0
B reproduces      4 of 4 · submit
verdict           both sides "MADE IT" · correct true · missing 0 · extra 0 · equal on both
B calls EXTEND    A setter 1 · bars 2 · A and B agree, 4 cells carried
guest sets        B draws and locks in -> the HOST applies it: A phase listen, 4 target notes
turn gating       A is now the matcher; A's grid is not editable (false)
guest power-up    A uses REVEAL -> the host arbitrates, reveals SNARE, 2 hint cells
B leaves          A stays: strikes [0, 0] — a disconnect is not a miss
relay footprint   select count(*) from events where kind = 24900  ->  0
```

### The single-machine match (2026-11-14)



Played end to end in headless Chrome against `https://ballademicz.com/daw/horse/`, every control clicked
with dispatched pointer events (not `element.click()`), 0 console errors:

```
boot            kit [36,38,42,46]  step 0.1667 s  tempo 90  phase idle
start match     synth armed (General User GS, channel 9)  phase set  setter 0
draw 4 hits     sequencer holds 4 hits / 3 voices / 16 steps / 90 BPM
lock in         phase listen  countdown 3.58 -> 2.38 (counting down)
listen ends     phase reproduce  entry 0  target cells painted: 0 (hidden)
reveal a voice  revealed [HAT]  2 hint cells  entry still 0 (it does not play it for you)
submit wrong    phase verdict  missing 4  extra 1  grid markers miss 4 / extra 1
continue        phase set  pattern back in the grid  panel hidden
submit exact    phase choose  correct true  missing 0  extra 0  "MADE IT"
earn + build    power-up taken  bars 1 -> 2  pattern carried over  listen window 7.58 s
2x time         7.58 s -> 14.61 s (doubles the REMAINDER)
pass            setter 0 -> 1  matcher 0  strikes unchanged  stock pass 1 -> 0
empty lock in   refused: "draw at least one hit first"
listen          grid read-only, a click during the listen changed nothing
3 misses        strikes [0,0] -> [3,0]  phase over  "player 2 wins the match"
start from over full reset: strikes, stock, bars, cells
notes to synth  60 + 32 fired across the two runs (audio is really scheduled)
```

One behaviour the build added to the spec: **a miss holds on the verdict.** The first cut dropped
straight back into SET, which meant the diff was computed, printed in the panel — and never painted on
the grid. The whole point of judging by diff is that the player sees what they got wrong, so a miss now
sits in a `verdict` phase with the missing (▲) and extra (▼) cells marked and a
`CONTINUE — PLAYER n SHOOTS AGAIN` button before the shot goes back.

## Related

* [[the-deck-arrangements-lane-locks]] — the parent design; §6 is the P2P clock this game rides.
* [[ballademix-reassembly-deck]] — the engine: one transport, drum sequencer, SpessaSynth.
* [[the-deck-saas-platform]] — the shipped deck and admin this game would live in.
* [[buzz]] — the Nostr relay that can carry the game's signalling.
