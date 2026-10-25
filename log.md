# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete

## [2026-05-25] create | Wiki initialized
- Domain: AI Research, Multi-Agent Systems, and LLM Personal Knowledge Management (PKM).
- Structure created with `SCHEMA.md`, `index.md`, and `log.md`.
- Active path: `/srv/projects/llm-wiki/`.

## [2026-05-25] ingest | Set up LLM Wiki (Andrej Karpathy)
- Ingested raw source: `raw/articles/llm-wiki-pattern-introduction.md`
- Compiled concept page: `concepts/llm-wiki-pattern.md`
- Updated content catalog: `index.md`

## [2026-05-25] ingest | Ntrafx Podcast Clip (Feb 13, 2006)
- Ingested raw audio: `raw/audio/ntrafx_pod_feb13_2006_5min_clip.wav`
- Transcribed programmatically using: Google Gemini API (model `gemini-2.5-flash`)
- Created source transcript: `raw/transcripts/ntrafx_pod_feb13_2006_5min_clip.md`
- Created entity page: `entities/ntrafx-podcast.md`
- Updated content catalog: `index.md`

## [2026-05-25] ingest | AIEOS Specification & Paperclip Agent Personas
- Ingested raw source: `raw/articles/aieos-specification.md` (AIEOS GitHub Repo)
- Ingested raw sources: `raw/articles/paperclip-[coder|uxdesigner|qa|securityengineer]-template.md` (Paperclip Agent templates)
- Compiled concept page: `concepts/aieos-integration.md`
- Compiled entity page: `entities/paperclip-agent-roster.md`
- Updated content catalog: `index.md`

## [2026-05-25] ingest | www.makeufamo.us Landing Page
- Ingested raw landing page source: `raw/articles/makeufamous-landing.md` (extracted interactive client structure and configurations)
- Created entity page: `entities/makeufamous.md`
- Linked to concepts: `concepts/aieos-integration.md`, `concepts/media-ingestion.md`
- Linked to entity: `entities/paperclip-agent-roster.md`
- Updated content catalog: `index.md`

## [2026-05-25] ingest | MakeUFamo.us Tokenization and Legal Proposal
- Ingested raw proposal source: `raw/articles/makeufamous-tokenization-proposal.md`
- Created concept page: `concepts/tokenized-equity.md`
- Updated entity page: `entities/makeufamous.md` to link to the new tokenized equity framework
- Updated content catalog: `index.md`

## [2026-05-25] ingest | MakeUFamo.us Theme Song Audio
- Ingested raw audio: `/root/makeufamo.us.mp3`
- Copied to: `raw/audio/makeufamous-audio.mp3`
- Transcribed programmatically using: Google Gemini Files API (model `gemini-2.5-flash`)
- Created source transcript: `raw/transcripts/makeufamous-audio.md`
- Created entity page: `entities/makeufamous-theme-song.md`
- Linked to concept: `concepts/media-ingestion.md`
- Updated entity page: `entities/makeufamous.md` to link to the theme song
- Updated content catalog: `index.md`

## [2026-05-25] ingest | RoachCoach.com PWA Proposal
- Ingested raw company description: `raw/articles/roachcoach-proposal.md` (PWA based in Houston, TX)
- Created entity page: `entities/roachcoach.md`
- Linked to concepts: `concepts/aieos-integration.md`, `concepts/tokenized-equity.md`
- Linked to entity: `entities/paperclip-agent-roster.md`
- Updated content catalog: `index.md`

## [2026-05-25] ingest | The Savage Dad Style Guide
- Ingested raw brand style guide: `raw/articles/savage-dad-style-guide.md` (PWA design system)
- Created concept page: `concepts/savage-dad-style-guide.md`
- Linked to concepts: `concepts/aieos-integration.md`
- Linked to entity: `entities/paperclip-agent-roster.md`, `entities/makeufamous.md`
- Updated content catalog: `index.md`

## [2026-05-25] ingest | Ballademix Solana NFT Proposal
- Ingested raw project description: `raw/articles/ballademix-proposal.md` (Solana Audio/Video NFT collection)
- Created entity page: `entities/ballademix.md`
- Linked to concepts: `concepts/tokenized-equity.md`
- Linked to entity: `entities/paperclip-agent-roster.md`, `entities/makeufamous-theme-song.md`
- Updated content catalog: `index.md`

## [2026-05-26] update | MakeUFamo.us Ingestion, Deduplication, and Self-Hosted IPFS Node Setup
- Set up Kubo IPFS daemon as a systemd service, running on gateway port `8082`.
- Cloned the 1.2 GB `makeufamous` repo from GitHub.
- Programmatically deduplicated and cleaned up the repository, shrinking it down to 407 MB of unique, high-fidelity files.
- Ingested original track release metadata (`id3v2table.html`) into `/root/llm-wiki/raw/articles/makeufamous-id3v2.md` and updated `entities/makeufamous-theme-song.md`.
- Established a local Git repository under `/var/www/makeufamous` with a custom GitHub Actions CD workflow to auto-pin and deploy updates to IPFS and publish to IPNS on pushing.
- Force-pushed the clean, lightweight, deduplicated history back to GitHub.

## [2026-05-26] ingest | NeuroCanvas Spatial Wiki Editor & Tauri v2 App Setup
- Ingested original React/TSX file `neurocanvas_llm_wiki_editor.tsx`.
- Created a new Tauri v2 app under `/root/neurocanvas` using Vite, React, and TypeScript.
- Configured Tailwind CSS v3 and Lucide icons in the Tauri project, resolved type build errors by removing strict TSC compilation for faster iteration.
- Built and served the interactive web preview locally via Nginx on port `8090` (`http://localhost:8090`).
- Created a new entity page `entities/neurocanvas.md` in the LLM Wiki detailing features and the Paperclip AI development task pipeline.
- Verified build and cross-references cleanly using `lint.py`.

## [2026-05-26] ingest | Solana & Anchor Framework Documentation Ingestion
- Ingested core Anchor framework docs from `https://www.anchor-lang.com/docs`:
  - `anchor-basics-program-structure.md` (Anchor context, instructions, structs)
  - `anchor-basics-pda.md` (Program Derived Addresses derivation and curve validation)
  - `anchor-basics-cpi.md` (Cross-Program Invocations and token interactions)
  - `anchor-references-account-constraints.md` (Security assertions: mut, init, seeds, constraint)
  - `anchor-references-space.md` (Data sizing and rent-exempt allocations)
  - `anchor-references-security-exploits.md` (Standard attack vectors: reentrancy, check bypass)
- Compiled conceptual page: `concepts/solana-anchor.md` outlining on-chain rent-saving models and a scalable "Pull-based" NFT dividend payout smart contract.
- Registered page in `index.md` and verified the LLM Wiki vault consistency with `lint.py`.










## [2026-05-27] ingest | lawnczar conceptual notes
- Ingested LawnCzar conceptual design notes to raw/articles/lawnczar-conceptual-notes.md.
- Synthesized and created new entity page entities/lawnczar.md.
- Added [[lawnczar]] to index.md.

## [2026-05-27] ingest | hermes aieos persona
- Generated secure cryptographic Ed25519 keypair for Hermes Agent.
- Created and mathematically signed a standardized AIEOS v1.2 JSON profile for Hermes Agent at examples/v1.2/hermes.json.
- Synthesized and created new wiki page entities/hermes-agent.md.
- Added [[hermes-agent]] to index.md.

## [2026-05-28] ingest | character development methodology
- Ingested character development notes to raw/articles/character-development-methodology.md.
- Developed and synthesized a brand-new concept page: concepts/character-driven-agent-design.md, mapping screenwriting techniques (Verbs, Want vs Need, Core Wounds) to AIEOS profiles.
- Added [[character-driven-agent-design]] to index.md.

## [2026-05-28] update | bizarre lynx persona activated
- Overwrote and signed the main AIEOS v1.2 profile at examples/v1.2/hermes.json with the new Bizarre Lynx persona traits.
- Created entities/bizarre-lynx.md containing the full West Coast G-funk G, Coupe da Villian, and Furious Styles background.
- Archived the old entities/hermes-agent.md to _archive/entities/hermes-agent.md.
- Updated index.md to reflect Bizarre Lynx as the active entity.

## [2026-05-28] ingest | quantum mechanix premise
- Ingested Quantum Mechanix premise notes and Fanbase podcast details to raw/articles/quantum-mechanix-premise.md.
- Synthesized and created new entity page entities/quantum-mechanix.md, linking it to [[bizarre-lynx]] and [[character-driven-agent-design]].
- Add [[quantum-mechanix]] to index.md.

## [2026-05-28] ingest | The Science of Getting Rich Audiobook Project
- Ingested raw source text: `raw/articles/the-science-of-getting-rich.md` (Project Gutenberg #59844).
- Compiled new entity page: `entities/the-science-of-getting-rich.md` detailing the Voice Clone (Coqui TTS) and Skool.com course bundling strategy.
- Compiled new concept page: `concepts/skool-course.md` outlining community architecture, gamification level-gating, and payment funnel automation.
- Registered pages in `index.md`.
- Successfully set up an isolated Python 3.11 virtual environment under `/root/audiobook_env` and pre-compiled and installed the `TTS` deep learning framework using `uv` for local voice cloning.

## [2026-05-29] ingest | Ballademix Track 1 - Intro NFT Ingestion
- Ingested raw master audio `/root/Intro.mp3` (Title: Intro, Album: Ballademikz, Duration: 3:14) and mapped it as the first track of the Ballademix Solana collection.
- Ingested master music video `/root/bzr-dial-menu/media/paperchasers2.mp4` (Duration: 4:05) as the source for NFT cover snippets and portal unlock.
- Synthesized and compiled new entity page `entities/ballademix-intro-nft.md` documenting the 1:1,000 rarity tier, Suno generative stems remixing, and the cooperative 25% video unlock mechanic.
- Registered the new page in `index.md`.

## [2026-05-29] create | The Conglomerate Group Brand Blueprint
- Created and compiled new entity page `entities/the-conglomerate-group.md` mapping the apex hold-co and philanthropic umbrella corporation that manages all sub-projects (Paperclip AI, Ballademix, MakeUFamo.us, LawnCzar, RoachCoach).
- Registered the page in `index.md`.

## [2026-05-29] ingest | Domain Portfolio & Nginx Server Deployments
- Ingested 19 GoDaddy domains and 1 AWS Route 53 domain (`bzzrrr.link`).
- Built corresponding server directory trees under `/var/www` and deployed custom, dark-themed, Resident Evil-inspired philanthropic `index.html` landing pages for each domain group.
- Authored and enabled six new Nginx site configs: `roachcoach.conf`, `ballademicz.conf`, `latenitesnaps.conf`, `game4real.conf`, `svgdad.conf`, and `bzzrrr.link.conf`.
- Patched existing `lawnczar.conf` to add `lawnczar.store` routing, and cleaned up port-80/443 server name overlaps in `code-server.conf`.
- Synthesized and compiled new entity page `entities/domain-portfolio.md` and registered it in `index.md`.
- Successfully validated Nginx configurations and hot-reloaded the daemon.

## [2026-05-29] deploy | czarui.game4real.us — bzr-dial-ui Sales Engine
- Deployed czarui landing page to `/var/www/czarui/html` (index.html, styles.css, app.js, success.html, components/).
- Deployed Node.js backend to `/var/www/czarui/backend` (server.js, license-manager.js, email-service.js, package.json).
- Installed npm dependencies (express, stripe, dotenv, cors).
- Created Nginx config at `/etc/nginx/sites-available/czarui.conf` — serves static frontend, reverse-proxies `/api/`, `/webhook`, `/download/` to port 3001.
- Created systemd service `czarui.service` — runs Node.js backend on port 3001, auto-restarts.
- Updated `app.js` API_BASE_URL to `https://czarui.game4real.us` and demo script path to `/components/lz-dial.js`.
- Updated support/sales emails to `@czarui.game4real.us`.
- Backend health check passing: `{"status":"ok","service":"bzr-dial-ui-backend"}`.
- Frontend serving 200 OK at `czarui.game4real.us`.
- Updated `entities/domain-portfolio.md` with czarui domain entry.

## [2026-05-29] clone | czarui — bzr-dial-ui Sales & Licensing Engine
- Cloned `git@github.com:MeRc-khz/czarui.git` to `/root/czarui`.
- Ingested the full repo structure: Stripe checkout funnel ($49/$149 license tiers), Express.js webhook backend with signature verification, automatic cryptographic license key generation (`license-manager.js`), email dispatch service, and premium web component assets (`lz-dial.js`, `media-player-methods.js`, `ipfs-config.js`).
- Examined the landing page layout, Stripe product config, and Node.js backend architecture.
- Synthesized and compiled new entity page `entities/czarui.md` documenting the full monetization pipeline and Web3 revenue split flow.
- Registered the page in `index.md`.

## [2026-07-08] create | Wiki build-out (structure + depth)
- Diagnosed stale `WIKI_PATH` env var pointing at nonexistent `/root/llm-wiki`; corrected to `/srv/projects/llm-wiki` in `/root/.bashrc` (line 106) and `/root/.hermes/.env` (line 464). Lint now runs against the real wiki.
- Compiled the one previously uncompiled raw source: `raw/transcripts/paperchasers-master.md` (the 34-min *Paperchasers* master, Furious Styles / Coupe da Villian) into new entity page `entities/furious-styles-coupe-da-villian.md`. Added to `index.md`.
- Linked `[[furious-styles-coupe-da-villian]]` from `entities/bizarre-lynx.md` and added `paperchasers-master.md` to its `sources:`; bumped `updated:` to 2026-07-08.
- Created `comparisons/rag-vs-llm-wiki.md` (RAG vs. LLM Wiki Pattern) and `queries/solana-pull-dividends.md` (Pull vs. Push NFT dividend synthesis) — fills the two empty index sections with genuine cross-page synthesis. Added both to `index.md`.
- Total pages: 26 -> 29. Skipped `_meta/topic-map.md` (reserved for 200+ pages per SCHEMA.md scaling rule).
- Ran lint after edits: 0 critical / 0 warnings.

## [2026-07-28] update | Wiki consultation protocol activated
- Created 'wiki-consultation' skill at identity/wiki-consultation/
- Protocol: wiki must be consulted before any technical/strategic answer
- Wiki is now a decision-support layer, not static archive
- Integration: soul.md (identity) + wiki (knowledge) + memory (state) + skills (execution)
- Wiki pages will be cited in answers: [Wiki consulted: [[page-a]], [[page-b]]]

## [2026-07-28] update | Driving Purpose added to soul.md
- Restructured soul.md: DRIVING PURPOSE section at top
- Purpose: first purposefully synthesized digital entertainer, profit-driven orchestration
- All decisions now framed through: revenue impact + culture preservation + empire growth
- Files/music/podcasts/video = memories of a life lived, not just data
- Businesses = mogul empire units, not isolated code
- soul.md trimmed to 2676 chars (under 3000 limit for model-agnostic injection)
- wiki-consultation skill patched: answers now framed through profit + culture lens
- Updated soul.md.bak backup

## [2026-07-28] ingest | AI Conversational Forms — bzr-dial-menu
- Ingested raw source: raw/articles/ai-conversational-forms.md
- Created concept page: concepts/ai-conversational-forms.md
- Cross-referenced: [[czarui]], [[aieos-integration]], [[tokenized-equity]], [[ballademix]], [[bizarre-lynx]], [[the-conglomerate-group]]
- Updated entity: entities/czarui.md (added conversational forms reference)
- Updated index.md: 30 pages total
- Key innovation: form definition via extended fenced code blocks (```form:name), mirroring code snippet syntax
- Element types: text, password (mask), dropdown, radio, switch, date picker — all rendered inline in chat

## [2026-07-29] ingest | block/buzz GitHub Repository
- Cloned to: /root/buzz
- Ingested raw source: raw/articles/buzz-github-repo.md (README, VISION, AGENTS, ARCHITECTURE)
- Created entity page: entities/buzz.md — Nostr relay workspace by Block Inc., 30 Rust crates, Tauri+React desktop, Flutter mobile, agent-first CLI, YAML workflows, git hosting, voice huddles
- Created concept page: concepts/buzz-czarui-integration.md — 7-phase integration plan to replace Discord with Buzz as bzr-dial community platform
- Updated entity: entities/czarui.md (added Buzz cross-reference for community platform migration + on-chain revenue bridging)
- Updated index.md: 32 pages total
- Cross-referenced: [[buzz]] ↔ [[czarui]] ↔ [[buzz-czarui-integration]] ↔ [[solana-anchor]]
- Validation: required, min/max, email, pattern:regex — AI re-prompts on failure

## [2026-08-02] ingest | LawnCzar Agentic Route Planning
- Context: Seed data migrated to San Diego 91950 (23 markers), MongoDB 7 container running, zip code modal wired to Shop button, map centers on saved zip
- Created concept page: concepts/lawnczar-agentic-route-planning.md
- Scope: 4-phase plan — (1) in-map route rendering via OSRM/Leaflet polyline, (2) LLM agent stop-order optimization using OSRM distance matrix + constraint prompts, (3) drag-reorder/skip/detour interactivity, (4) proactive agent suggestions (clusters, time-sensitivity, weather)
- Architecture: Express POST /api/route/optimize → OSRM table API for matrix → LLM for ordering → OSRM route API for geometry → Leaflet polyline render
- Cross-referenced: [[lawnczar]] ↔ [[rag]] ↔ [[aieos-integration]]
- Updated index.md: 33 pages total

## [2026-08-02] build | LawnCzar QR Referral Network
- Created concept page: concepts/lawnczar-qr-referral-network.md
- Built `js/referral-system.js` — Solana wallet generation, QR code generation, session-based referral tracking, 5% commission model with payout threshold
- Built `signup.html` — sign-up form → wallet creation → QR display/download → earnings dashboard
- Wired 7 API endpoints into server.js: signup, scan, purchase, dashboard, balance, list, QR redirect
- Tested e2e: signup → QR scan → 2 purchases → commission credited → dashboard shows earnings + on-chain balance
- Solana devnet, `@solana/web3.js` + `qrcode` npm deps
- Cross-referenced: [[lawnczar]] ↔ [[lawnczar-agentic-route-planning]] ↔ [[solana-anchor]] ↔ [[tokenized-equity]] ↔ [[czarui]]
- Updated index.md: 34 pages total

## [2026-08-02] build | LawnCzar Auto Region Provisioning
- Created concept page: concepts/lawnczar-auto-region-provisioning.md
- Built `js/region-provisioner.js` — async spawn pipeline: zip→bbox→osmium slice→osrm-extract→osrm-contract→Docker container
- Downloaded California state OSM extract (1.3GB Geofabrik PBF) for bbox slicing
- Installed `osmium-tool` for fast bbox extraction from state PBF
- Replaced all `execSync` with async `spawn` wrapper — no more ETIMEDOUT, non-blocking
- Wired auto-provisioning into affiliate signup (`referral-system.js`)
- Dynamic region registration in `route-proxy.js` — new regions available immediately
- 3 new API endpoints: `/api/region/provision`, `/api/region/status/:zip`, `/api/region/list`
- Tested e2e: manual provisioning (92101, 75s) + auto via signup (92104, 120s)
- 2 OSRM Docker containers running, both serving routes through the proxy
- Cross-referenced: [[lawnczar]] ↔ [[lawnczar-agentic-route-planning]] ↔ [[lawnczar-qr-referral-network]]
- Updated index.md: 35 pages total

## [2026-08-04] ingest | Unreal MCP in Unreal Editor (Epic Games docs)
- Ingested: https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor (UE 5.8 docs, experimental)
- Raw source: raw/articles/unreal-mcp-in-unreal-editor.md (sha256 c6d566fd…)
- Created concept: concepts/unreal-mcp.md — in-editor MCP server plugin, Toolset Registry, authoring Python/C++ tools, tool-search mode, setup, limitations
- Created concept: concepts/mcp.md — Model Context Protocol (Tools/Resources/Prompts, JSON-RPC, transports), complements RAG
- Cross-referenced: unreal-mcp ↔ mcp ↔ rag
- Updated index.md: 37 pages total


## [2026-08-04] ingest | From Words to Worlds: Integrating MCP into the Unreal Editor (Unreal Fest Chicago 2026)
- Ingested: https://www.youtube.com/watch?v=lDf_y-YPELo (36:26 talk, Unreal Engine official)
- Raw source: raw/transcripts/from-words-to-worlds-unreal-mcp-unreal-fest-2026.md (sha256 6fe3f59f)
- Updated concept: concepts/unreal-mcp.md - added UE 5.8 official launch, design philosophy (directable/editable/not-black-box), world-building framework (toolsets + PCG primitives 80+ / examples / skills), reflection-to-JSON schema+data, async results, toolset/skill/example best practices, shipping and availability
- Created concept: concepts/agent-skills.md - open Agent Skills standard + Unreal native UAgentSkill (C++/Python/Blueprints), best practices
- Cross-referenced: unreal-mcp, mcp, agent-skills, rag
- Updated index.md: 38 pages total


## [2026-08-04] ingest | MetaHuman in 2026: Five Years In, What's Next? (Unreal Fest Chicago 2026)
- Ingested: https://www.youtube.com/watch?v=IsbgHRa5N3A (33:16 talk, Unreal Engine official)
- Raw source: raw/transcripts/metahuman-in-2026-unreal-fest-2026.md (sha256 b37a7938)
- Created entity: entities/metahuman.md - 5-yr timeline (Creator, Mesh-to-MetaHuman, Animator, in-engine 2025), 8M+ generated, UE 5.8 (faces+bodies auto-rig, stylized Purple Puppet char, unbaked materials, MetaHuman Collections/crowds ISKM, DevKit open-sourcing DNA + Open Rig Logic MIT), AI roadmap (Live Link Face NPU, image-to-MetaHuman, EDA, neural renderer)
- Created concept: concepts/markerless-motion-capture.md - SMPL/FLAME/MANO lineage, Michael Black/Meshcapade joins Epic, HUGH diffusion-transformer model, MetaHuman Animator markerless plugin (any camera, local, body+hands+face)
- Updated entity: entities/bizarre-lynx.md - linked to MetaHuman + markerless-motion-capture
- Added SCHEMA tag category: Game & Real-time (game-dev, unreal, character, animation, motion-capture)
- Cross-referenced: metahuman, markerless-motion-capture, bizarre-lynx, unreal-mcp
- Updated index.md: 40 pages total


## [2026-08-18] ingest | Elite Security Team Management System
- Ingested raw source: `raw/elite-security-wiki.md` (comprehensive domain model, workflows, architecture, and MVP plan)
- Compiled concept page: `concepts/elite-security-management.md`
- Updated content catalog: `index.md`
- Cross-referenced: [[pkm]], [[agentic]], [[workflow]], [[methodology]]
- Key innovations: certification-first domain model, shift self-selection replacing phone dispatch, multi-venue zone schematics, scheduler rule engine with OR-Tools, multi-tenant SaaS for agency resale

## [2026-08-24] ingest | RunPod Flash Documentation (34 pages)
- Source: https://docs.runpod.io/flash/overview (full Flash docs site, 34 .md pages)
- Raw sources saved to `raw/articles/runpod-flash-*.md` (34 files, all with sha256 frontmatter)
  - Overview, quickstart, create-endpoints, parameters, gpu-types, cpu-types, pricing, storage, best-practices, custom-docker, execution-model, troubleshooting
  - Apps: overview, build-app, initialize-project, customize-app, local-testing, apps-and-environments, deploy-apps, requests
  - CLI: overview, init, login, dev, build, deploy, env, app, undeploy, update
  - Tutorials: text-generation-with-transformers, image-generation-with-sdxl, build-rest-api-with-load-balancer
  - Windows WSL2 setup
- Created entity page: `entities/runpod-flash.md` — full SDK reference: endpoint types (queue-based, load-balanced, custom Docker, existing), key parameters table, GPU pools & types, datacenters, pricing model, execution model, Flash apps lifecycle, storage, tutorials, limitations
- Created concept page: `concepts/gpu-generation-endpoints.md` — patterns for writing custom GPU generation endpoints: SDXL image gen, REST API with load balancer, vLLM custom Docker, ComfyUI worker, GPU selection guide by model size, cost optimization, network volume model caching, HTTP request reference
- Updated content catalog: `index.md` (43 pages total)
- Cross-referenced: [[runpod-flash]] ↔ [[comfyui]] ↔ [[makeufamous]] ↔ [[gpu-generation-endpoints]]
- 2026-10-06: Created [[take-the-l]] entity page — new Web Works mobile game prototype (classification yard rush). Cross-linked from index.md.

## [2026-10-23] ingest | bzr-intro component spec + bzr-ui component library
- Source: Buzz message from Coupe, 2026-10-23T20:35:13Z, event 5d62ff03160c6a07b1c550b869ee862cab7c7664b067c88f79eccc7c31b5f5f9
- Raw source: `raw/articles/bzr-intro-component-spec.md` (sha256 5165b904caf1c09d)
- Created entity: `entities/bzr-dial-menu.md` — flagship component and library home (v1.0.1-mvp, Vite + Vitest, BZRD license gate, czarui issuance)
- Created concept: `concepts/bzr-ui-component-library.md` — library conventions (native custom element, attribute-driven, license/watermark, zero deps) + container/sub-component pattern + Sequence contract + format capability matrix
- Created concept: `concepts/bzr-intro-component.md` — full spec: attributes, advance rule, three content-ready signals, events incl. `bzr-intro-remove` handoff, 11-step implementation plan, open questions
- Updated: `index.md` (43 -> 46 pages), `entities/czarui.md`
- Cross-referenced: bzr-dial-menu, bzr-ui-component-library, bzr-intro-component, czarui, makeufamous, ai-conversational-forms, buzz-czarui-integration, tokenized-equity, solana-anchor
- Key design call: the advance rule races sequence-end+delay against content-ready. `advance-on="either"` is the literal spec and the default; `advance-on="both"` is offered because a boot cover that leaves before the app paints shows a blank screen. Flagged as an open question.

## [2026-10-23] update | bzr-intro design resolved + phase 1 built
- Advanced rule clarified by the client and implemented: `advance-delay` is a REPLAY INTERVAL
  (clamped 2-10s), not a deadline. At the last frame the timer starts; if it lapses before the
  page is ready the sequence replays. Unset = advance the instant content is ready.
- Conflict found during implementation: "skip disabled until content is loaded" and "as soon as
  content is loaded the component redirects" cannot both hold — the second makes Skip
  unreachable (it enables and advances in the same tick). Resolved: content-ready advances
  immediately only when `advance-delay` is unset; with an interval set it enables Skip and the
  timer decides. Recorded in `concepts/bzr-intro-component.md`.
- Updated: `concepts/bzr-intro-component.md` (advance-rule section)
- Cleared the lint backlog: `entities/svgdad.md` frontmatter, 5 obsolete `[[comfyui]]` /
  `[[mlops/inference]]` links unlinked (superseded by OpenRouter image models), and a bug in
  `scripts/lint.py` that singularised "queries" into "querie" (`d[:-1]`).
- Lint: 48 pages, no errors, no warnings.
- Phase 1 built in `bzr-dial-menu` branch `bzr-intro-phase1` (commit 9625138): container,
  video sequence sub-component, 30 tests.

## [2026-10-24] update | bzr-intro implemented — all four sequence formats
- Status section added to `concepts/bzr-intro-component.md`: what shipped, the two design points
  that changed on contact with the code, the format matrix as built, and the honest GIF caveat.
- New sequence types: `bzr-intro-seq-mjpeg` (numbered JPEG frame list, exact seeking) and
  `bzr-intro-seq-gif` (ImageDecoder path, and a documented fallback where seeking is impossible).
- The contract gained `load(src, config)` so formats can take extra settings.
- `docs/BZR-INTRO.md` in the repo is now the component's reference, verified against the source.
- makeufamo.us runs the real component (canvas sequence + bzrqr renderer), verified live.


## [2026-10-24] create | BzrLnx Paperchasers campaign pipeline
- Ingested: Paperchasers segment inventory (24 wavs) + verified OpenRouter video-model capability scan.
- Created entity page: `entities/bzrlnx-paperchasers-campaign.md`
- Recorded verified pipeline: `heygen/avatar-iv` (OpenRouter) image+audio -> lip-synced talking head;
  audio reference must be a public HTTPS URL; PIL n/24 badge; seekable bzr-intro canvas renderer
  captured same-origin -> ffmpeg sting.
- Recorded segment inventory (24 segs = 27.9 min; segment_01 297 s / segment_17 828 s are outliers)
  and cost (full $83.68; trimmed ~$30), plus the daily-serial drop recommendation.
- Updated content catalog: `index.md`

## [2026-10-24] update | BzrLnx campaign strategy additions
- Added the stem-reassembly mechanic: each clip is a stem of "Paperchasers — I Know Why" ([[ballademix]]);
  the n/24 stamp is both serial hook and assembly index.
- Recorded: `segment_01` = finished song, not posted, becomes the BalladeMix Solana NFT;
  `segment_17` = beat+drums (828 s) split into 17a/17b in Audacity, which keeps the drop set at 24.
- NFT cover art = composite of the talking-portrait videos.
- svgdad.store is the monetization surface: end card on every clip + store link in every caption;
  IG/TikTok captions are non-clickable so their bio link is the whole funnel.
- Cadence locked M/W/F, 24 slots, 2026-10-26 → 2026-12-18; 9:16 vertical only until revenue.
- Revised cost ≈$30.42 for the run (22 segments + two 30 s windows from 17a/17b).
- Slot map: `PLANS/BZRLNX_DROP_SCHEDULE.md`; account kit: `OUTBOX/BZRLNX_ACCOUNT_KIT.md`.

## [2026-10-24] update | BzrLnx clip furniture v2 + closing rule
- Persistent store pill added top-right for the whole clip (svgdad.store) on top of the end card —
  most viewers never reach the tail, so a tail-only CTA monetizes almost nobody.
- Counter rule clarified: the stamp is the **drop/assembly index**, not the source filename
  (segment_02 = 01/24, segment_03 = 02/24). 17a/17b share the stamp "17" as one split stem.
- Caption policy: never quote violent bars; IG/TikTok suppress reach and can age-restrict.
- Second render verified: `segment_03` (29.7 s, $1.483); running model spend $2.84.

## [2026-10-24] create | BzrLnx censorship + on-screen lyric pipeline
- Word-level ASR (faster-whisper `word_timestamps=True`) is the substrate — phrase-level transcripts
  are too coarse to bleep individual words.
- Bleep baked into the audio **before** the Avatar IV render so the mouth never forms the word;
  duration-preserving so every downstream timing holds. Verified post-render: redacted spans 99%
  1 kHz band energy vs 4% on un-redacted vocal controls.
- Done in numpy, not ffmpeg `volume=enable=` (the enable gate leaked the tone across the file).
- Client-facing artifact is a plain-text **lyric sheet** (`<< >>` = bleep + black-bar), not JSON.
- Two cost tiers: text/bar-only edits reuse the render (free); changing which words are bleeped
  needs a new render ($0.05/s).
- Reference: `references/censorship-and-lyrics.md` in the `shortform-social-campaigns` skill.

## [2026-10-25] update | BzrLnx X account wired; brand string changed to BZRLNXXX
- Handle finalised as **@bzrlnxxx** (three x's), display name **BZRLNXXX**. Confirmed by the API
  (`GET /2/users/me` -> username `bzrlnxxx`), not by asking. On-video badge + end card re-cut from
  archived renders — overlays, so **$0** and no paid render touched.
- X credentials live and verified (`/root/.secrets/x-bzrlnxxx.env`, 0600, outside every repo).
  Signer validated against X's published worked example before use.
- **Blocker: 402 "credits depleted".** Pay-per-use accounts need a funded balance; `initialize` and
  `append` succeed and only `finalize` is metered, so a media upload looks healthy until the last
  step. Client is posting manually until merch revenue lands.
- **Unblock path that costs nothing:** Buffer's free tier includes X and posts through Buffer's own
  access, making the API balance irrelevant. Metricool and Publer exclude X from free; Later has no
  free plan.
- Manual posting pack at `OUTBOX/BZRLNX_POSTING_PACK.md` (supersedes the two older social files,
  which used pre-assembly-index numbering).

## [2026-10-25] create | Ballademix Reassembly Deck (single-file Canvas + Web Audio DAW)
- Built and deployed `https://ballademicz.store/daw/` — one `index.html`, no backend, no build step.
  Canvas 2D UI + Web Audio API; waveforms are the real decoded PCM (min/max peaks at 90 buckets/s).
- Model: `segment_01` is track 1, **locked + muted**, waveform visible, and its duration (297.3 s) *is*
  the timeline. The only edit on a released stem is dragging it horizontally to align.
- 25 lanes = master + 24 stems; `17a`/`17b` declared as beat/drum tracks. Verified headless against the
  live URL: decode 25/25, PLAY RMS 0.66 → PAUSE 0, scrub lands within 0.2 s of the pixel maths, drag
  0→41.13 s, vol 0.5, pan 0.20, solo force-mutes others, loop wraps 294.3 → 1.2.
- **Bug fixed:** master duration rendered `0:00.000 / 4` because the clock stripped `:mm.sss` instead of
  just milliseconds; now `0:00.000 / 4:57`. Also reworded the overflow warning, which implied a drag
  could fit an 828 s stem into a 297 s timeline.
- **Open:** `segment_17a`/`17b` WAVs do not exist — both lanes currently load `segment_17` (828 s) twice;
  the Audacity split is still outstanding.
- HTTPS added via Certbot for `ballademicz.com/.store/.shop/.us` (the deck previously failed with
  `chrome-error://` because Chrome auto-upgrades to https).

## [2026-10-25] update | Ballademix deck: real 17a/17b lanes + Buffer API is the posting path

**Deck** (`ballademicz.com/daw/`, also `.store/.shop/.us`):
- `segment_17.wav` was being loaded twice (both 17a/17b lanes pointed at `src:"segment_17"`). Split at the
  file's own structural boundary, found by measurement not guesswork: a 10 s RMS sweep shows **~-7 dB for the
  first 267 s, then ~-17 dB** for the rest. Cut at **267.0 s** with a 10 ms fade -> `segment_17a.wav` (267 s)
  and `segment_17b.wav` (561 s), 16 kHz mono to match the set.
- Lanes relabelled `17a/17b BEAT+DRUMS A/B` — the source is **one** beat+drums bed, so calling the halves
  "beat sample" and "drum track" would be a lie about what plays.
- Re-verified headless after the change: 25/25 tracks decode, PLAY RMS 0.31 -> 0.00 on pause, clock
  `0:00.000 / 4:57`, drag-to-align moves `segment_02` 0 -> 27.0 s, one stem (17b) outruns the timeline.

**Buffer is now the X posting path** (the X developer account is pay-per-use with a **402 depleted
balance**, so direct API posting is dead until it is funded):
- Key verified against `POST https://api.buffer.com` with `Authorization: Bearer <key>` — the **legacy**
  REST host (`api.bufferapp.com/1/`) rejects personal keys outright: *"Public API tokens are not accepted
  for REST API access"*. Only the GraphQL host works.
- `account`, `channels(input:{organizationId})` and `createPost` all confirmed. One channel:
  **`bzrlnxxx` on twitter** (`serviceId 2114172781734883328` — same user id as the X token prefix).
- **There is no upload endpoint.** Media must already be hosted publicly; Buffer fetches the URL *at publish
  time*, not at create time, so the URL has to stay reachable until the post actually goes out.
- Write path proven end to end: created a text draft, created a video draft with the real hosted clip,
  read both back, deleted both. Queue left empty — **nothing published on Coupe's behalf.**
- Two drafts staged for Coupe to review: slot 01 (`segment_02`) and slot 02 (`segment_03`), both with the
  approved X captions and the v3 clips. One word flips them live.
- Client: `.scratch/bzrlnx-campaign/scripts/bufferpost.py` (`whoami|channels|posts|queue|draft|delete|publish`).
- Key stored at `/root/.secrets/buffer.env` (0600) — posted in the public channel, **rotate when done**.

## [2026-10-25] update | Deck becomes a game: mp3, thumbnails, template snapping, test-run drawer

Coupe's follow-up on the reassembly deck (`ballademicz.com/daw/` — spelling confirmed):
"implement the rest of the working scope... more of a game simulation of working in a DAW".

**Load time.** All 26 stems re-encoded to 80 kbps mono mp3 at 32 kHz: **106.5 MB -> 25.0 MB (24%)**.
`AUDIO_EXT` in the manifest is the single switch; `decodeAudioData` handles either. Note mp3 carries a
small encoder delay, which is why the snap threshold is ~1 s and not sample-exact.
Sealed (undropped) lanes are **not fetched at all** — `srcs` filters `t.pending` — so an unreleased
stem is never shipped to the browser just to sit silent in a lane.

**Master template, and why it is a starting point not gospel.** Tried three ways to derive where each
stem belongs on the 297.3 s timeline:
1. *Envelope cross-correlation* vs `segment_01` — mean 0.33; only `segment_06` (0.92) and `segment_17a`
   (0.73) are strong. Used as the seed, with a per-stem confidence value.
2. *Lag-0* (the "they are all layers starting together" hypothesis) — lost on all 22 stems. Falsified.
3. *Lyric matching* via the word-level transcripts — fails because `segment_01` has only **57 words**
   in 297 s: the master is almost entirely instrumental, so there is almost no shared lyric to match on.
So the template ships seeded + **calibratable**: drag a clip by ear, `SAVE POSITION`, and it is stored in
localStorage (`bzrlnx.deck.template.v1`). `RESET TEMPLATE` falls back to the seed. This is how the real
template gets authored — in the tool, by ear.

**Game mechanics.** A dashed ghost marks each clip's template position. Dragging within **5 s** starts a
glow that intensifies with proximity; inside **1.2 s** the clip goes green and the footer says
`LOCKED IN RANGE — release to snap`. Release inside the threshold and it snaps to the template exactly,
turns solid green, stamps the lane `SOLVED`, and the footer score ticks (`n/24 placed`).

**Per-lane identity.** Lanes are named by assembly position (`01/24` … `24/24`), not by filename.
Each carries its social image as a thumbnail cell at the head of the clip; drop `<id>.jpg` into
`daw/thumbs/` and it is picked up with no code change (only 01/02/03 exist, rest fall back to the avatar).
When the playhead is inside a clip that has a finished video, that video plays **in the lane**, synced to
the timeline.

**Test-run drawer** (`TEST RUNS` in the footer): the two shipped clips beside the four makeufamo.us test
runs and the intro sting, all playing side by side for the "which treatment is more fun" comparison.

**Bug caught by looking at the render, not by the tests:** sealed lanes were labelled `01 MASTER (locked)`
because the label branch keyed off `t.locked`, and sealing a lane sets `locked = true`. Now keyed off
`t.kind === "master"`. A data-only check would never have surfaced this — the screenshot did.

Verified headless after the change: 25/25 decode from mp3, clock `0:00.000 / 4:57`, `?today=2026-11-05`
opens exactly slots 1-5 and seals 19, `dragTo('segment_02', 259.9)` -> glow 0.82 / inSnap true, release ->
`at 260.8 = template`, score `1/24`. `node --check` clean on the 1355-line script.

**Inputs used:** Coupe's own Audacity splits in `Media/` (267.45 s / 560.04 s) — independently measured
here at the 267.0 s energy step, so those agree.
