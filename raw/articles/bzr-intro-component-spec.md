---
source_url: (Buzz message, coupe-hermes channel #79255874-0fc4-4cea-8c84-6dae728fd122)
source_file:
ingested: 2026-10-23
sha256: 5165b904caf1c09d
media_type: article
---

# bzr-intro — Component Spec (raw)

Source: Buzz message from Coupe, 2026-10-23T20:35:13+00:00, event `5d62ff03160c6a07b1c550b869ee862cab7c7664b067c88f79eccc7c31b5f5f9`.

Verbatim request:

> cool, this is going to be the second javascript component in the bzr ui library. bzr-intro component. Add this component to the index.html file of your project and it will not remove it self until index page and fetched data render. Is the sequence a video file? user should be able to use a sequence file like a gif, mjpg, mp4, etc. sequence should auto center. same functionality that we have with our intro sequence play, loop, pause, scrub and skip. 2 - 10 seconds after the last frame, if the index page content has loaded which ever comes first component is removed, advanced to the index.html content. Different sequence type should be handled by sub components. background color, time before advance (2 - 10 seconds), redirect url, sound .mp3, ingest this idea into the wiki and come up with a plan on how to implement this with bzr-dial as a component library

## Context at the time of the request

The intro that prompted this already exists on makeufamo.us (see [[makeufamous]]) and was
built as a single-purpose canvas animation, not a reusable component:

- Source lives in `/srv/projects/Media/makeufamous/intro/intro.js`, deployed to
  `/var/www/makeufamous/html/assets/intro.js` and injected as the last script tag in the
  landing `index.html` (which is **not** tracked in a repo).
- It renders the BZRQR mark from a layered `.ora` export — five colour groups
  (head, qr grid, goatee, shades, cap) each animating on its own clock, over a light field
  that dissolves to dark.
- It already implements play / pause / loop / scrub / skip, once-per-session, skip on
  Esc and scroll, and `prefers-reduced-motion` opt-out.
- `draw(p)` is a pure function of progress, which is what makes the scrubber trivial — no
  video element and no seeking.

That implementation is the proof of the interaction design. The request is to generalise it
into a library component where the sequence is a **supplied file** rather than hardcoded
procedural drawing.

## Explicit requirements extracted

1. Second JS component in the bzr UI library; name `bzr-intro`.
2. Drops into any `index.html`; it must **not remove itself** until the host page's content
   *and* its fetched data have rendered.
3. The sequence is a **file the user supplies** — gif, mjpg, mp4, etc.
4. Sequence should **auto-centre**.
5. Same transport as the existing intro: **play, loop, pause, scrub, skip**.
6. Removal trigger: **2–10 seconds after the last frame**, OR when the index page content
   has loaded — **whichever comes first** — then advance to the index content.
7. **Different sequence types handled by sub-components.**
8. Configurable: **background colour**, **time before advance (2–10s)**, **redirect URL**,
   **sound (.mp3)**.
9. Ingest into the wiki; produce an implementation plan for bzr-dial as a component library.
