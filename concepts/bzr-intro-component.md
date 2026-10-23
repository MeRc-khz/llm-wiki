---
title: bzr-intro Component
created: 2026-10-23
updated: 2026-10-23
type: concept
tags: [framework, video, animation, workflow, monetization]
sources: [raw/articles/bzr-intro-component-spec.md]
confidence: high
contested: false
contradictions: []
---

# bzr-intro Component

**bzr-intro** is the second component in [[bzr-ui-component-library|the bzr-ui library]] and the
first that plays a **user-supplied sequence file**. It is a full-bleed overlay that covers a
page while the app boots, plays a sequence with transport controls, and then takes itself away.

It generalises the intro already running on [[makeufamous]], which proved the interaction
design but hardcoded its sequence as procedural canvas drawing.

## Answering the question directly: is the sequence a video file?

**Not today — and that is the gap this component closes.** The shipped makeufamo.us intro is a
canvas animation whose frame is a pure function of progress; there is no video file anywhere.
The requirement is the opposite: the user brings a **file** (mp4, webm, gif, mjpeg) and the
component plays it. That is the right call, because a file is what a customer can actually
supply.

The two are not alternatives — they are two implementations of one interface:

- a `<video>`-backed sub-component satisfies the common case (mp4/webm),
- a canvas sub-component lets the procedural intro from makeufamo.us live inside the same
  component without special-casing.

That interface is the **Sequence contract**, defined in [[bzr-ui-component-library]] (see *The
Sequence contract*) — and because the sequence types differ so much in capability (an mp4 seeks;
a plain gif does not), the contract exposes `seekable` so the transport can degrade honestly
instead of breaking.

## Usage

```html
<!-- video sequence, replay every 4s while the app boots, sound, then redirect -->
<bzr-intro
    src="/media/intro.mp4"
    background="#0b0914"
    advance-delay="4"
    wait-for="#app-ready"
    sound="/media/intro.mp3"
    redirect="https://bzzrr.link"
    license="BZRD-XXXX-XXXX-XXXX-XXXX">
</bzr-intro>
```

```html
<!-- no advance-delay: leaves the moment the page content is ready -->
<bzr-intro src="/media/bumper.gif" wait-for="#app-ready"></bzr-intro>
```

The element is written as the **first child of `<body>`**. It is not removed by its own JS;
removal is an explicit, observable transition, so the host page can react to it.

## Attributes

| Attribute | Type | Default | Description |
|---|---|---|---|
| `src` | URL | — | The sequence file |
| `type` | `video`, `gif`, `mjpeg`, `canvas`, `image` | inferred from `src` extension | Which sequence sub-component to mount |
| `background` | CSS colour | `#000` | Field behind the sequence; `transparent` lets the page show through |
| `fit` | `contain`, `cover` | `contain` | Sequence is auto-centred; `cover` fills the viewport |
| `advance-delay` | seconds | *unset* | **Replay interval** while waiting for content, **clamped 2–10**. Unset = advance as soon as content is ready |
| `max-hold` | seconds | *unset* | Optional escape hatch: advance regardless after N seconds |
| `wait-for` | CSS selector | — | Content is ready when this element exists |
| `redirect` | URL | — | Navigate on advance instead of revealing the host page |
| `sound` | URL | — | `.mp3` played with the sequence; an unmute control sits in the chrome |
| `sound-volume` | 0–1 | `0.6` | — |
| `once` | `session`, `local`, `never` | `session` | Repeat suppression, same semantics as the current intro |
| `storage-key` | string | `bzr.intro.seen` | — |
| `label` | string | `Skip` | Skip button text |
| `z-index` | number | `2147483000` | — |
| `license` | `BZRD-…` | — | Same gate as [[bzr-dial-menu]]; unlicensed renders a watermark |

## The advance rule

The intro is a **cover that holds until the app is ready**. It has no fixed duration.

```
play the sequence
  └─ on reaching the LAST frame
       ├─ advance-delay IS set → start timer (2–10s)
       │     ├─ content ready first → advance
       │     └─ timer lapses and content is NOT ready → REPLAY the sequence from frame 0
       │                                                (on reaching the last frame, restart the timer)
       └─ advance-delay NOT set → sit on the last frame; advance the instant content is ready

content ready, advance-delay NOT set → advance immediately
content ready, advance-delay SET     → enables Skip; the timer at the last frame decides
                                       (content ready then → advance, otherwise → replay)
```

The asymmetry is deliberate: **it is what gives Skip a purpose.** If content-ready advanced
instantly in both cases, the Skip button would enable and become irrelevant in the same tick —
it could never be pressed. With a replay interval set, content arriving mid-sequence enables
Skip and the visitor can leave early without waiting for the sequence and the timer.

So `advance-delay` is a **replay interval while waiting**, not a deadline. Omitting it means
"wait silently on the final frame"; setting it means "keep the show running until the app can
take over". Values outside 2–10s are **coerced, not rejected**, so a bad attribute cannot make
the component unusable.

**Advance** means: if `redirect` is set, navigate there; otherwise remove the overlay and reveal
the host page. Redirect fires on **both** natural completion and skip.

### Skip is gated on the content being ready

**The Skip button is disabled until the page content has loaded**, then enables. The intent is
that a visitor cannot skip past an app that hasn't rendered and land on a blank screen.

The consequence worth knowing: if the backend never reports ready, the sequence replays forever
and Skip stays disabled — the visitor is held behind the overlay with no way out. An optional
`max-hold` escape hatch (advance regardless after N seconds) is the mitigation; it is **off by
default** so behaviour matches the specification exactly.

## Content-ready signals

Three ways, first one wins, so it works whatever the host architecture is:

1. `wait-for="#app-ready"` — a MutationObserver resolves when the selector matches.
2. `window.dispatchEvent(new CustomEvent('bzr:content-ready'))` — for SPAs that know when their
   fetches landed.
3. `document.querySelector('bzr-intro').contentReady()` — imperative, for tight control.

If none is supplied, content never reports ready and the sequence replays indefinitely (or
waits on the last frame when `advance-delay` is unset).

## Behaviour inherited from the shipped intro

Play, pause, loop, scrub, skip — already proven on makeufamo.us and carried over:

- **Scrub** works because the container only ever asks the sequence for `seek(progress)`.
  Formats that cannot seek render the scrubber **disabled, in place** — the layout never
  shifts between formats.
- **Skip** on: button, `Escape`, scroll, click on the sequence. Controls `stopPropagation` so
  pressing play cannot also trigger skip.
- **Sound**: browsers block autoplay with audio, so `sound` cannot start on load. The chrome
  carries an **unmute button**; the sequence autoplays muted and the audio joins on a gesture.
- **`prefers-reduced-motion: reduce`** → the component never mounts.
- **Once per session** via `sessionStorage`, same as today.
- **Transport is a real player**: clicking the sequence toggles play/pause; Space toggles;
  loop lights up when engaged.

### Hard-won implementation constraints

Two bugs from the shipped intro that the library must not reintroduce:

- **A per-frame UI sync must never recreate DOM.** Rewriting a control's `innerHTML` at 60fps
  destroys the element under the pointer between `mousedown` and `mouseup`, so `click` never
  fires — the button is dead to real users while a programmatic `.click()` still passes. Diff
  every DOM write.
- **Serve media with HTTP Range support.** Mobile Safari refuses to play a video response
  without `Accept-Ranges`/`206`, and nothing can seek.

## Events

| Event | `detail` | Fires when |
|---|---|---|
| `bzr-intro-ready` | `{duration, seekable}` | First frame paintable |
| `bzr-intro-play` / `bzr-intro-pause` | `{progress}` | Transport |
| `bzr-intro-seek` | `{progress}` | Scrubbed |
| `bzr-intro-replay` | `{attempt}` | Replayed because content was not ready in time |
| `bzr-intro-content-ready` | `{}` | The host reported content ready |
| `bzr-intro-skip` | `{progress}` | Skipped (only possible once content is ready) |
| `bzr-intro-end` | `{reason}` — `content`, `skip` or `max-hold` | Advancing |
| `bzr-intro-remove` | `{reason}` | The overlay is leaving the DOM — host pages hook this to start animations |

`bzr-intro-remove` is the handoff contract: the page gets told the intro is going away rather
than having to poll for its absence.

## Implementation plan

Files land in `/srv/projects/REPOS/bzr-dial-menu` alongside `src/bzr-dial-menu.js`, following
the library's conventions (native custom element, shadow DOM, attribute-driven, Vite + Vitest).

| # | Deliverable | Path | Phase |
|---|---|---|---|
| 1 | Container: attrs, shadow chrome, transport, advance controller, once-per-session, events, license/watermark | `src/bzr-intro.js` | 1 |
| 2 | Sequence contract + registry (`bzrIntro.sequence(name, Class)`) | `src/bzr-intro.js` | 1 |
| 3 | Video sub-component (`<video>`, muted/playsinline autoplay, seek) | `src/bzr-intro-seq-video.js` | 1 |
| 4 | Container + contract tests (advance/replay, clamping, content-ready, transport, DOM-diff regression) | `src/bzr-intro.test.js` | 1 |
| 5 | GIF sub-component — `ImageDecoder` frame-accurate scrub, `<img>` fallback with `seekable:false` | `src/bzr-intro-seq-gif.js` | 2 |
| 6 | MJPEG / jpeg-sequence sub-component (frame list, live-stream fallback) | `src/bzr-intro-seq-mjpeg.js` | 2 |
| 7 | Canvas sub-component — wraps a `draw(p)` renderer | `src/bzr-intro-seq-canvas.js` | 2 |
| 8 | Demo page | `pages/intro-demo.html` | 3 |
| 9 | README section | `README.md` | 3 |
| 10 | First consumer: port makeufamo.us to `<bzr-intro … type="canvas">` | `/var/www/makeufamous/html/index.html` | 3 |

All open questions are resolved: `advance-delay` is a replay interval (unset = advance on
content-ready), redirect fires on skip as well as completion, and sound gets an unmute control.

## Related

- [[bzr-ui-component-library]] — the library this belongs to, and the Sequence contract
- [[bzr-dial-menu]] — the first component; shares licensing and conventions
- [[czarui]] — license issuance and the commercial funnel
- [[makeufamous]] — the site running the prototype of this component
