---
title: bzr-ui Component Library
created: 2026-10-23
updated: 2026-10-23
type: concept
tags: [framework, architecture, workflow, monetization]
sources: [raw/articles/bzr-intro-component-spec.md]
confidence: high
contested: false
contradictions: []
---

# bzr-ui — Component Library

**bzr-ui** is the [[the-conglomerate-group|Conglomerate's]] library of dependency-free native
Web Components, commercially licensed through [[czarui]]. It is the product behind the
[[bzr-dial-menu]] Kickstarter campaign and the thing the "$100K: Full 5-component Web Works
library" stretch goal refers to.

## Members

| Component | Status | Purpose |
|---|---|---|
| [[bzr-dial-menu]] | shipped (v1.0.1-mvp) | Viewport-edge radial dial replacing dropdowns |
| [[bzr-intro-component]] | designed (this cycle) | Sequence-file intro/bumper overlay with transport |
| Edge-drawer panel | stretch goal ($50K) | Slide-out panel |
| — | stretch goal ($100K) | Full five-component library |

## Shared conventions

Every component in the library follows the same shape, and new ones must match it:

- **Native custom element.** `class BzrX extends HTMLElement`, `attachShadow({mode: 'open'})`,
  `static get observedAttributes()`, `connectedCallback` / `disconnectedCallback`. No React,
  no framework, no runtime dependencies.
- **Attribute-driven configuration** read via `getAttribute()` in the constructor and
  `attributeChangedCallback` — no required JS to instantiate.
- **License gate.** A `license` attribute validated against `BZRD-XXXX-XXXX-XXXX-XXXX`;
  unlicensed instances render a watermark. See [[czarui]] for the Stripe issuance side.
- **Build/test.** Vite for bundling, Vitest with `environment: 'jsdom'` for tests, source at
  `src/bzr-<name>.js` with a sibling `src/bzr-<name>.test.js`.
- **Demo pages.** The repo root `index.html` is the primary demo; `pages/*.html` hold
  focused demos (media, inline content, edge-dial).
- **Events out, attributes in.** Components communicate state changes by dispatching
  `CustomEvent`s rather than calling into host code.

## The sub-component pattern (introduced by bzr-intro)

The library's first real *extensibility* problem arrives with [[bzr-intro-component]]:
the component must play a sequence that could be an mp4, webm, animated gif, mjpeg stream, or
a procedural canvas animation. Those have wildly different capabilities — an mp4 can be
seeked, a gif traditionally cannot.

Rather than a forest of `if (type === 'video')` branches inside one class, the container is
split from the renderer:

```
<bzr-intro>                     ← container: owns transport, chrome, advance logic
  └── <bzr-intro-seq-video>     ← sub-component: loads, plays, seeks ONE format
  └── <bzr-intro-seq-gif>
  └── <bzr-intro-seq-canvas>
  └── <bzr-intro-seq-mjpeg>
```

Each sequence sub-component implements the same **Sequence contract**, and the container
talks only to that contract. A new format is a new file, never an edit to the container.

### The Sequence contract

| Member | Kind | Meaning |
|---|---|---|
| `load(src)` | method → Promise | Fetch/prepare; resolve when first frame is paintable |
| `play()` / `pause()` | method | Transport |
| `seek(progress)` | method | Jump to 0..1 — **may be a no-op** |
| `duration` | getter | Seconds; `0`/`null` if not time-based |
| `progress` | getter | 0..1 current position |
| `seekable` | getter | Whether the scrubber should be interactive |
| `ready` | getter | First frame decoded |
| `destroy()` | method | Release object URLs, decoders, listeners |

The container degrades gracefully: if `seekable` is false, the scrubber renders disabled
rather than being hidden, so the control layout never shifts between formats.

### Format capability matrix

| Format | Sub-component | Time-based | Seekable | Notes |
|---|---|---|---|---|
| mp4 / webm | `seq-video` | yes | yes | `<video>`, `muted` + `playsinline` required for autoplay; needs HTTP Range on the server or mobile Safari refuses to play at all |
| animated gif | `seq-gif` | no | via `ImageDecoder` | `ImageDecoder` (Chromium) allows frame-accurate scrub by decoding frame-by-frame; without it, play/pause only |
| mjpeg / jpeg sequence | `seq-mjpeg` | yes | yes | A frame list — the most scrubbable format, plus a `<img>` fallback for live MJPEG streams |
| still image / poster | `seq-image` | no | no | Single frame, holds |
| procedural | `seq-canvas` | yes | yes | The makeufamo.us intro. `draw(p)` pure in progress |
| audio only | — | yes | yes | Pair a static sequence with the `sound` attribute instead |

**Design consequence:** `scrub` is a first-class capability that not every format supports.
That is a property of the *format*, surfaced through the sub-component — not a defect in the
container.

## Why this matters commercially

The library is sold as licensed components (see [[czarui]]). A container/sub-component split
means a buyer can extend the library without forking it, which is what makes an
"Edge-drawer panel" or a fifth component cheap to add later — each new component reuses the
licensing, watermark, event and build conventions established here.
