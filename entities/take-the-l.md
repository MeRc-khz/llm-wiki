---
title: Take the 'L'
created: 2026-10-06
updated: 2026-10-06
type: entity
tags: [game-dev, monetization]
sources: [raw/articles/take-the-l-concept.md]
confidence: high
contested: false
contradictions: []
---

# Take the 'L'

**Take the 'L'** is a mobile puzzle-arcade game prototype by Web Works Systems / [[bizarre-lynx]]: a train **classification yard** rush game. Player works the control tower of a rail yard, frantically classifying incoming rail cars onto the correct outbound tracks before the clock expires. Designed as a single-file HTML5 prototype (vanilla JS + CSS) intended for conversion to a packaged mobile title for app-store sale — monetization track pairs with the [[makeufamous]] / [[lawnczar]] ecosystem playbook.

## Core Loop
- **Intake queue:** rail cars roll into the yard — cargo types are color-coded: Tanker (LIQUID), Autorack (AUTOS), Grain, Hopper (COAL), Boxcar (FREIGHT), Reefer (COLD).
- **Tracks:** each outbound track declares a destination (Chicago, Dallas, Seattle, Miami) + required cargo type. Car count scales with day/level.
- **Train integrity rule:** a departing train needs an **ENGINE first** and a **CABOOSE last**, with ≥2 cargo cars between. Misplaced cars are rejected (engine-first, caboose-last, cargo-match).
- **Departure:** complete track = points (cargo count × bonus), +time on departure; difficulty scales by day (more tracks, faster queue pressure).

## Production Plan
1. **Prototype (this repo):** `/srv/projects/REPOS/take-the-l/index.html` — single file, mobile-first, touch controls.
2. **Hardening:** level curve tuning, sound, offline PWA shell, score persistence (localStorage → optional [[czarui]]-style leaderboard).
3. **Store conversion:** wrap with Capacitor/TWA for Play Store/App Store; monetization via ad interstitials between shifts + one-time "Yardmaster" upgrade.

## Related
- [[lawnczar]] — mobile/web release pipeline precedent
- [[makeufamous]] — Conglomerate entertainment IP portfolio

