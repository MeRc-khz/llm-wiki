---
title: bzr-dial-menu
created: 2026-10-23
updated: 2026-10-23
type: entity
tags: [framework, monetization, workflow, animation]
sources: [raw/articles/bzr-intro-component-spec.md]
confidence: high
contested: false
contradictions: []
---

# bzr-dial-menu

**bzr-dial-menu** is the flagship native Web Component of [[bzr-ui-component-library|the bzr-ui
library]]: a viewport-edge radial dial that replaces dropdown menus. Physics-based inertial
scrolling, snapping, hybrid Canvas/DOM rendering at 60 FPS, zero framework dependencies.

It is the product behind the Kickstarter campaign taglined *"Built Different. Prove It."* and
the first of the library's components to ship.

## Facts

- **Repo:** `/srv/projects/REPOS/bzr-dial-menu` — `src/bzr-dial-menu.js` plus
  `src/bzr-dial-menu.test.js`.
- **Version:** `v1.0.1-mvp` (close-button fix, trigger z-index above overlay, backdrop click
  handler).
- **Build:** Vite; tests via Vitest with `environment: 'jsdom'`. No runtime dependencies.
- **Licensing:** validated from a `license` attribute against `BZRD-XXXX-XXXX-XXXX-XXXX`;
  unlicensed instances render a watermark. Keys are issued and sold through [[czarui]].
- **Marketplace listing:** https://github.com/MeRc-khz/bzr-dial-menu
- **Live demo:** https://czarui.game4real.us

## Structure

The repo is the home of the library, not just this component:

```
src/bzr-dial-menu.js        the dial
src/bzr-dial-menu.test.js
pages/*.html                focused demos (media, inline content, edge-dial)
index.html                  primary demo
```

## Related components and modals

- [[ai-conversational-forms]] — chat-style modal used by this dial to collect form input.
- [[bzr-intro-component|bzr-intro]] — the second library component: a sequence-file intro
  overlay with transport controls, designed 2026-10-23.
- [[buzz-czarui-integration]] — replacing Discord with [[buzz]] for community management
  around the product.
- [[tokenized-equity]], [[solana-anchor]] — the Dev Edition NFT share-certificate and dividend
  mechanics sold alongside the licence tiers.
