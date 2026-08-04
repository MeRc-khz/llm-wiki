---
title: MetaHuman
created: 2026-08-04
updated: 2026-08-04
type: entity
tags: [game-dev, unreal, character]
sources: [raw/transcripts/metahuman-in-2026-unreal-fest-2026.md]
confidence: high
contested: false
contradictions: []
---

# MetaHuman

**MetaHuman** is Epic Games' digital-human technology for creating photorealistic (or stylized), fully rigged characters, announced at Unreal Fest Chicago 2026 as **5 years old**. Product director Tony positions it not as "building statues" but as bringing characters to life. Creators have generated **8+ million MetaHumans** — adoption, not demo. ^[raw/transcripts/metahuman-in-2026-unreal-fest-2026.md]

## Milestones

- **MetaHuman Creator** (early access) — accessible interface guided by real-world acquisition data, letting anyone create photoreal, rigged humans fast.
- **Mesh to MetaHuman** (a year later) — auto-rig/convert from a head mesh.
- **MetaHuman Animator (2023)** — facial performance capture from an iPhone on a tripod; no head-mounted camera, markers, studio, or week-long pipeline. Later made to work with just a microphone and in real time.
- **2025** — Creator moved in-engine (browser + export step gone); parametric bodies with sculpt/blend, fitted clothing, expanded data.
- **Maya & Houdini** tools for DCC workflows.

## Notable use (2026)

- **Clair Obscur: Expedition 33** (Sandfall) — Game of the Year at The Game Awards, the most decorated game ever; Jennifer English's BAFTA-winning performance as Mel was captured with MetaHuman Animator.
- **Sinners** — Oscar-nominated film, virtual production + rapid real-time iteration.
- **Coachella** — Anyma visuals live events. Also deployed across all of Epic's own characters, from Fortnite to stylized projects like *Yuki's Revenge*.

## UE 5.8 headline features

- **Mesh to MetaHuman → faces AND bodies** — auto-rigging to Epic's character standards (skeleton/rig, compatible with grooms, clothing, customization, templates). Works from sculpts, scans (e.g. 3D Scan Store), or AI-generated meshes (Tripo/Meshy). Demo: non-artist Zara turned her sketch → Meshy 3D → alive in-engine character.
- **Stylized characters** — a production-quality stylized character built on MetaHuman core tech (with Purple Puppet), shipped with step-by-step docs covering auto-rigging to expression-editor sculpting.
- **Unbaked materials & textures** — author/migrate materials and textures in or out of engine, view in real time, edit geometry while seeing material changes. Plus custom lighting scenes and render-settings matching inside MetaHuman Creator ("work in context").
- **MetaHuman Collections / crowds** — a new asset class for building huge crowds: 1000+ fully clothed MetaHumans in real time on base PS5, rendered as Nanite **instance skinned meshes (ISKMs)** at ~1/10 the memory, seamlessly blending to full-fidelity near camera; scales from high-end PC to 500 on a mobile device. Experimental in-engine (MetaHuman menu). Speaker Henry's favorite question: how Collections relate to **Mutable**.
- **MetaHuman DevKit** — **open-sourcing** two core technologies, **DNA** and **Open Rig Logic**, under an **MIT** license (live as of the talk), so MetaHuman tech can run in any engine/platform ("if it's going to be a standard, the whole industry must build on it").

## Research / AI roadmap

- **Live Link Face** — real-time facial solving running directly on dedicated AI hardware / NPUs (highlighted by Google as next-gen on-device AI).
- **Image → MetaHuman** — a rigged, textured character generated from a single input image in minutes (models recover facial shape/appearance/material detail).
- **EDA (Epic Developer Assistant)** — conversational character creation/edit ("make him younger/older… and it tells you why"), and generating an entire diverse cast/crowd from a high-level request.
- **Neural renderer for digital humans** — "image uplift" that preserves a character's likeness and respects scene lighting across changing environments.
- **Michael Black + Meshcapade joined Epic** — bringing the [[markerless-motion-capture]] tech and SMPL lineage.

## See also

- [[markerless-motion-capture]] — Michael Black/Meshcapade's tech now integrated into MetaHuman Animator (model: HUGH).
- [[bizarre-lynx]] — the user's own UE5/6 MetaHuman-based digital twin avatar.
- [[unreal-mcp]] — MCP support in the same Unreal 5.8 release for agent-driven editing.
