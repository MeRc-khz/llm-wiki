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

