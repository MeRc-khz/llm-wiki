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

## [2026-10-25] update | Owner-edited lyric sheets: 2/3 of redactions were about to ship un-bleeped

Coupe finished editing all 24 sheets (`OUTBOX/bzrlnx-lyrics`, 20:50-22:13). Diffed every one
against the pristine emit in `Media/bzrlnx-campaign/lyrics/`.

**His edit:** armed redactions **28 -> 38**. Added `hoes`+`fucked` (10, 11, 17), `fuckin'` (14),
`tec 9,` (15), `bitch'` (19). Un-barred `tag`, `9,`, `suppressin' fire` in segment_03 — so that
line now reads "you staring at the muzzle of a tech 9" fully legible on screen, while segment_15
bars `tec 9,`. Same class of content, opposite treatment; flagged to him as his call, plus the
consequence that slot 02 is already rendered *with* those bars, so the sheet and the live clip now
disagree. Text corrected by ear throughout ("Gaurd your grill", "I'm bout my cabbage", "street
militia") — his fixes over the ASR, and now the on-screen copy.

**The defect.** 24 of the 38 requested redactions were **unmatchable in the word stream** — the ASR
never wrote `hoes`, `tec 9,`, `bitch'` at all. `find_span` returned None and `build_lines` dropped
them silently: the word would have played in the clear while the clip still looked censored. That is
the same failure class that nearly shipped a live gun reference, and the only one where the video
lies to the client.

**Fix** — `scripts/sheetbleep.py`: exact ASR match first (sample-accurate when the transcript
agrees), else fall back to the barred word's position inside the owner's own line window,
proportional by word index (`line_start + i/N*(line_end-line_start)`), floored at 0.12 s so a
zero-width bleep can never be emitted. Measured rather than assumed on segment_10:
`<<hoes>>` 13.70-13.88 s [sheet timing] 1 kHz band 0.4% -> **100%**; `<<fucked>>` 20.78-21.12 s
[asr] 13.3% -> **100%**; controls ~10-15%.

Also validated: no malformed lines, no backwards timings. One zero-length line fixed
(`segment_21` `15.88|15.88` -> `15.88|16.20`).

**Lesson recorded** in the skill (`references/censorship-and-lyrics.md`): the owner's sheet is the
authority, not the transcript; resolve both ways and count requested vs resolved; verify a bleep by
1 kHz band energy, never by the absence of an error.

## [2026-10-25] build | HyperFrames motion-graphics overlays for the lyric cards

Coupe: keep segment_03 as rendered (no re-render — decision recorded), and find tooling that
"jazzes up the cards" the way TikTok creators use transitions and effects; look into hyperframes.

**What HyperFrames is:** HeyGen's open-source framework (`github.com/heygen-com/hyperframes`) that
turns HTML+CSS+GSAP into frame-accurate video by seeking each frame in headless Chrome and encoding
with ffmpeg. Same vendor as `heygen/avatar-iv`, the model behind our talking-head renders. Ships
agent skills (`/hyperframes`, `/motion-graphics`), not just a CLI. Verified runnable here: Node
v24.22.0, chromium and ffmpeg present; CLI 0.8.200.

**The cost insight that makes it the right choice:** the talking-head render is the paid step and the
cards are not. HyperFrames renders **transparent** overlays (ProRes 4444), so card work is an ffmpeg
composite over already-paid footage — free, and retroactive to clips already shipped.

**Built:** `scripts/make_overlay.py <sheet> <project>` — generates a HyperFrames composition from any
lyric sheet (raw lines, so the `<< >>` positions survive). 13 cards from the real segment_03 sheet,
kinetic type on a `0.028s` stagger, bars wiping `scaleX 0->1`, cards whipping off on line change.
Composited onto `sample_02_raw.mp4` and uploaded for review.

**Three defects the linter did NOT catch (check passed 0 errors while the output was wrong):**
1. `--format webm` returned `pix_fmt=yuv420p` — **no alpha**. It would have composited as an opaque
   black sheet over the footage. **MOV is the alpha-preserving path** (`prores / yuva444p12le`);
   verify with ffprobe before every composite.
2. `data-fps` on `<html>` is ignored — it belongs on the root composition div, else the render
   silently uses 30 fps and fights our 25 fps clips.
3. Type at 68px read as a footnote and the card sat inside the bottom UI-rail zone; now 96px and
   431px clear of the bottom edge. Bars were fixed-width squares (read as checkboxes) — now sized to
   the word, and confirmed black by sampling pixels (interior RGB [4,3,2]) rather than by eye.

**Coupe's decision:** overlay applies going forward; 01/02 can be re-cut retroactively for $0 on his
word. Open: whether to add the beat-sync pass (`hyperframes beats` / `audio` onset detection) to lock
card hits to each stem's drums rather than only the lyric timings.

Lesson recorded as skill `hyperframes-motion-graphics`.

## [2026-10-25] fix | Wrong footage in the overlay demo (my error), and drum sync built

**The error.** The first motion demo composited segment_03's lyric cards onto `sample_02_raw.mp4`.
That file is **segment_02's** take. The footage was chosen by filename in a folder that has been
through several naming passes, and the audio was never checked. Correlating it afterwards:
`sample_02_raw.mp4 vs segment_02 = +1.00`, `vs segment_03 = +0.16`. Every card was stamped on a
different performance. Coupe caught it as "the card and the generation are out of sync wrong card".

**The guard.** `scripts/build_drop.py` now fingerprints the footage against the segment's own audio
and **aborts** below r=0.90, and it verifies the rendered overlay carries alpha (`yuva`) before
compositing. Negative control run deliberately: the wrong pairing returned `r=-0.001` and the build
refused. A correct pairing reads +0.94..+1.00.

**Drum sync — measured, not assumed.** `hyperframes beats` reports "no beats detected" on these
stems and that is correct: autocorrelation of the onset flux peaks at only **0.04-0.32** across
segments 02/03/04/06, so there is **no locked tempo**. The drum bed (`segment_17a`) is a separate
file and is not under slots 01-03. Implemented sync against the **transients actually present**
(77 in seg03, 76 in seg02) via `scripts/onsets.py` (per-band energy flux: kick/body/air, each
normalised so a loud low end cannot dominate):
- entrance snaps onto an onset only within **0.10 s** — beyond that the lyric timing wins, since a
  card arriving 400 ms early is worse than no sync;
- **accent pulse on every onset** inside a card window (scale 1->1.022->1 over 150 ms); 157 accents
  in slot 02.

Independent validation of the detector: ASR line starts landed **+0.017 s, -0.007 s, +0.051 s** from
a detected onset on three separate lines — two unrelated methods agreeing to within a frame.

**Delivered:** `out/slot01_motion.mp4` (segment_02, 26.6 MB) and `out/slot02_motion.mp4`
(segment_03, 59.7 MB), both composited on verified-correct footage, check passed, alpha confirmed,
card measured 650 px from the bottom (clear of the rail zone; overlay-only render put it at 649 px,
so the composite is 1:1).

**Blocked:** drop 3 (Fri 10-30, slot 03 = `segment_04`) has no avatar render, and there is still only
**one portrait for all 24 drops** — two were supplied. Needs a per-drop portrait from Coupe; render
is ~$1.27. Also still outstanding: badge/sting/end-card assembly on top of these two (free), before
Monday.

## [2026-10-26] ship | Slots 01 and 02 finished: motion cards + brand furniture

Both drops assembled end to end and delivered: footage + animated lyric cards + counter badge +
store pill + brand sting + CTA end card. **34.60 s** and **37.36 s** — the same slot structure as the
previously shipped clips, so nothing downstream changes.

**Second bug, this one in the overlay itself.** The card markup was
`<div class="panel"></div><p class="line">…</p>` — the panel was an EMPTY sibling, so it rendered as a
bare 86 px padding strip with the lyric type hanging below it and outside its amber border. Every card
in every clip looked broken. Fixed by nesting the line inside the panel; panel is now 194 px and the
type sits inside it, confirmed on a full-resolution frame. **Lint passed the whole time** — caught only
by looking at one full-res frame rather than a downscaled grid.

**Counter relocated bottom-left -> top-left.** The old position was measured at y=1478 while the new
card's bottom edge is y=1490 — a **12 px collision**. Caught by measuring before shipping, not by
eye. Counter top-left, store pill top-right, lyrics in the lower third: three zones, no contact.
Flagged to Coupe as a layout change since he had said "no changes".

**Verified:** audio-fingerprint guard passed (r>=0.90) on both; overlay alpha `yuva444p12le` at 25 fps;
card bottom edge 427-432 px from the frame bottom; no counter/pill/card overlap; durations exact.

New scripts: `furnish.py` (badge + pill + sting + endcard over an already-composited clip — needed
because `assemble.py` expects separate card PNGs and the cards are now baked in). `make_overlay.py`
also gained `--onsets` with a 0.10 s snap guard plus accent pulses on every transient.

**Still blocked:** drop 3 (Fri 10-30, slot 03 = `segment_04`) needs a per-drop portrait; only one exists
for all 24 drops. Render ~$1.27 once supplied.

**Repeated lesson:** a downscaled contact sheet misled the eye four times in this session (type size,
a logo on a shirt read as the card, and an 86 px strip read as a panel). Pixel measurement was right
every time. Look at full resolution before concluding, and measure before shipping.

## [2026-10-26] build | MuScriptor on the 17a/17b splits + web MIDI/soundfont research

Coupe asked for 17a/17b through MuScriptor, and for research on playing multi-track MIDI and
soundfonts in the browser.

**Transcription.** Ungated mirror (`hf://cocktailpeanut/muscriptor-small/model.safetensors`), CPU,
25 fps-agnostic: 17a 307 s / 17b 323 s wall for 267 s / 560 s of audio. Smoke-tested a 20 s slice
first (valid `MThd`, format 1, 4 tracks, 480 ppq) before committing the long runs. Outputs in
`/srv/projects/muscriptor-out/`: `17a.mid/.json`, `17b.mid/.json`.

**The two halves are not the same kind of thing, and the working labels were backwards.**

| | 17a | 17b |
|---|---|---|
| notes | 1503 | 1606 |
| parts | 6, all musically distinct (5-33 pitches each) | 4, but **91% drums** |
| character | a real 6-part arrangement (voice/lead/kit/2 guitars/bass) | a **drum transcription** |

17b's drum part is legitimate — 831 closed hats, 293 bass drum, 194 snare, 67 open hats; median
inter-onset 0.17 s = eighth-note hats at ~180 BPM, which **independently matches the tempo MuScriptor
detected in 17a** (~180 BPM). But two of 17b's tracks are **degenerate artifacts**: 105 "acoustic
piano" notes all on C5, 6 "flutes" all on C6. Those must be discarded.

So: 17a had been called "beat" and 17b "drums". **It is the reverse.** Deck lanes labelled from the old
assumption would be wrong. Consistent with the earlier energy measurement (17a loud -7 dB, 17b quiet
-17 dB split at 267 s).

**Correction to a prior prediction:** the reference warned of a 120 BPM placeholder fallback when no
tempo locks. On this material the model **did** detect a tempo (~180 BPM, tempo events at 179.9 and
181.5) — the bar grid is real.

**Parser bug, mine.** A first throwaway SMF reader ignored running status and reported mismatched
note-on/note-off counts (78 on / 106 off), which looks exactly like a corrupt file. Fixed; every track
then balanced exactly, giving the 1503. Recorded in the skill as "believe the parser first, the file
second".

**Research (new skill reference `audio-processing/references/web-midi-and-soundfonts.md`).** Three
viable paths — **SpessaSynth** (SF2/SF3 in an AudioWorklet, separate thread so canvas work cannot
glitch it, offline render, and soundfont *smart-trim* down to the samples actually used); **js-synthesizer**
(FluidSynth compiled to WASM — the reference desktop sound); **Tone.js + @tonejs/midi** with the
CORS-open `gleitz/midi-js-soundfonts` sample sets for per-track processing. `MIDI.js`/`MIDIjs` can
only play one file at a time and are unmaintained. Non-negotiables: audio needs a user gesture; the
Web MIDI API needs HTTPS; schedule against the audio time passed into the callback.

## [2026-10-26] build | MIDI bench: soundfont playback of the 17a/17b transcriptions

Coupe: add 17a/17b as MIDI to the deck with browser soundfonts — separate instrument lanes, a piano
roll and a drum-machine lane, no editing, solo/mute/volume/pan, notes glowing on playback, and
**2-3 switchable instruments per track** as the interactive hook.

**Built:** `ballademicz.com/daw/midi/` — one page. SpessaSynth (AudioWorklet, off the main thread) +
**GeneralUser GS** (8 MB SF3, self-hosted). Track -> MIDI channel -> `programChange` for live
instrument swaps. Per lane: solo/mute/volume/pan; melodic tracks as piano rolls, drums as a
drum-machine grid (one row per kit piece). Notes glow amber at the playhead.

Pipeline: `muscriptor-out/prepare_midi.py` converts the MuScriptor MIDI to compact per-track JSON —
tick->seconds **through the tempo map** (these files carry 280 tempo events), zero-length notes
floored, degenerate tracks dropped, per-track channel recorded from the note events (mode, not the
last event seen).

**Three bugs, all mine, all caught by measuring rather than by reading code:**

1. **The page died silently.** `spessasynth_lib/dist/index.js` imports the bare specifier
   `spessasynth_core`; browsers cannot resolve bare specifiers, so the module never *executed* — my
   own try/catch never ran and the page sat on "loading…" with an empty error field. I had believed
   the file was clean because a grep pattern of mine omitted the space in `from "..."` and matched
   nothing. Fixed by bundling to self-contained ESM with esbuild.
2. **No note-offs were ever sent.** Notes had on-events but no off-events, so nothing released: voice
   count climbed **59 -> 103** and muting every track still left **97 voices ringing**. Releases are
   now scheduled at `start+duration`, run for *every* track including muted ones, and silencing a
   track releases what it already holds. Verified: bounded voice count, mute -> 0.
3. **PLAY did nothing** — the guard tested a `piece` variable that was never assigned.

Also fixed in the prep pass: a minimum-duration filter of 0.02 s **deleted the entire 17a drum track**
(all 201 hits are 0.01 s clicks). Drum hits are now floored to 0.06 s instead of dropped, which is why
17a shows 6 parts not 5.

**Verification method, and its limit.** Headless Chrome keeps the AudioContext `suspended` when the
click is synthesised by JS, so the first run showed 0 voices and looked like a dead synth. Driving
PLAY with a **trusted CDP input event** put `ctx` into `running`: 76 notes fired, 17-20 voices, solo
mute behaving by voice count, no errors. A diagnostics hook now exposes the context state so a
suspended context can never again be mistaken for a bug. **Not verified: the audible difference
between instruments** — only that `programChange` is accepted and the program state changes.

**Found in the data, and worth knowing before anyone plays it:** both transcriptions have real holes.
**17a is silent from 70 s to 140 s — a 70-second gap, 26% of the piece;** 17b is silent from 20 s to
50 s. The player is faithful; the transcription detected nothing there.

Lessons recorded in `audio-processing/references/web-midi-and-soundfonts.md`.

## [2026-10-27] build | Per-stem NFT gate on the reassembly deck

Coupe: mint an NFT per stem; once a stem is released it is available as an NFT, and **holding the NFT
activates that stem in the DAW**.

**Built and live:** `ballademicz.com/daw/?gate=nft`.
- `daw/nft/stems.json` — the 24-stem mint manifest (slot, stemId, drop date, `mint: null`), **generated
  from the deck's own track config** so ids and dates cannot drift from what the page renders.
- `daw/nft/gate.js` — reads the connected wallet's token accounts (both token programs), no signature,
  no transaction. `?wallet=<address>` reads any address read-only, which is how the gate is tested
  without a browser extension.
- `?gate=nft` enforces. **Without that parameter the deck is byte-for-byte the old behaviour** —
  verified first, since this was a live page.
- The gate runs **before** the audio loader, so a stem the visitor does not own is never fetched.

**Verified end-to-end against a live mainnet mint**, not simulated: `error: none`, `mints seen: 970`,
`ownedStems: [segment_02]`; that one lane unlocked and decoded (waveform + thumbnail visible) while the
other 23 stayed `SEALED / NFT REQUIRED`. The master lane is never gated.

**Four infrastructure problems, each found by testing and each of which looked like our bug:**

1. `api.mainnet-beta.solana.com` returns **403 "Access forbidden" to a browser** while the identical
   call works from curl — Origin-based.
2. `solana-rpc.publicnode.com` serves `getVersion` but refuses `getTokenAccountsByOwner` as an
   *indexed* request; Ankr and Helius need keys. **No free RPC works from a browser.**
3. **Fix: same-origin nginx proxy `/solrpc`** — which needed (a) a trailing slash on `proxy_pass`
   because Solana only accepts POST at `/` (otherwise 405 "Bad method"), and (b) **blanking the
   forwarded `Origin`/`Referer` headers**, which is exactly what Solana's 403 keys off and nginx
   forwards by default. Also the right production shape: a keyed provider's key then stays server-side.
4. **nginx served `.js` with `Cache-Control: max-age=2592000` (30 days)** — a fix of mine sat on disk and
   never reached the browser, so a cycle was spent debugging code that was already correct. Added a
   `no-cache` rule for `/daw/nft/` and a `?v=` cache-buster.

**Bug of my own:** the master lane (segment_01) was gated — it is the alignment reference and has no
NFT — which also broke its labels (`drops undefined`, `assembly undefined/24`). Now only ids present in
the manifest can be gated.

**Limits stated to Coupe:** client-side gating controls *access*, not *possession* — the mp3s are still
fetchable by direct URL, and fixing that means server-side auth on the audio. The free public RPC will
rate-limit under traffic.

**Open decisions before any minting:** confirm Solana + Metaplex Core; mint on release day or all 24 up
front; free claim vs sale price; who holds supply. Mint addresses drop straight into `stems.json` — the
gate already reads that field, so no code changes when they exist.


## [2026-10-27] fix | "sounds not playing in browser" — could not reproduce, hardened anyway

Coupe reported no sound. **I could not reproduce it on either page**, so I measured real output rather
than trusting the transport UI, using an AnalyserNode tap wired in front of the destination:

```
deck  ballademicz.com/daw/       ctx running   output RMS 0.36-0.41
midi  ballademicz.com/daw/midi/  ctx running   15 voices sounding
```

Both play from a cold load with the PLAY click as the first interaction. Reported honestly as
unreproduced and asked for browser/device plus the new banner text.

Fixes shipped anyway, because these are the real causes of the class:

1. **The MIDI page created its AudioContext at page load.** A context created before any gesture starts
   suspended and on iOS/macOS Safari can stay unresumable — the page looks alive and plays nothing. It
   is now created *inside* the first gesture, with the 8 MB soundfont streamed behind a visible
   percentage.
2. **PLAY before the soundfont finished was silently discarded** (`if (!ready) return;`) — exactly "I
   pressed play and nothing happened". The click now arms the audio and the intent is remembered.
3. **Deck: `play()` called `resume()` without awaiting it** and then scheduled sources against
   `ctx.currentTime`, which is frozen at 0 while suspended — every source lands in the past and never
   sounds while the clock runs. `play()` is now async, waits for `running`, and refuses with a message
   if the browser will not grant it. **Chrome won this race in every attempt, so this is a latent
   fragility fix, not a proven cause.**
4. **`.html` had no `Cache-Control` in nginx**, so browsers cached it heuristically and could keep
   running a stale page. **I was caught by this mid-investigation** — my own browser served an older
   copy and I chased a phantom. HTML is now `no-cache`.

The MIDI page now states why it is silent (banner: *press play* / *loading N%* / *browser is blocking
audio*), and both pages expose output-level taps so silence is measurable.

Lessons recorded in `audio-processing/references/web-midi-and-soundfonts.md` and
`nginx-production-deployments` ("A Cached Page Hides Your Fix").


## [2026-10-28] fix | MIDI bench silent: the synth was never connected to the output

Coupe: *"soundfont loads and piano roll starts but no sound /daw/midi/"*. That three-way split was the
diagnosis — soundfont loading ruled out the network, the roll starting ruled out the scheduler, and
what remained was the output path.

**Root cause: `WorkletSynthesizer` was never connected to `ctx.destination`.** `BasicSynthesizer` is an
`AudioNode` and does not connect itself. One missing call:

```js
synth.connect(meter);          // <- did not exist
meter.connect(ctx.destination);
```

Everything else genuinely worked: the worklet ran, the 8 MB soundfont parsed, notes were scheduled,
voices were allocated. The synth was producing audio into nothing.

**Why it shipped, and the real error:** the previous report claimed the page was making sound on the
evidence of `voices: 15` — but `voiceCount` only proves the synth is *allocating* voices, not that they
reach the speakers. The deck had been verified with a real AnalyserNode RMS (0.36-0.41); the MIDI page
was signed off on an internal counter. **That inconsistency between two pages in the same project is
what let it through** — and it was written into the skill an hour before the bug was reported.

**Verified after the fix, by reading samples:** `ctx running / playing / voices 5 / rms 0.0314`. Added a
live level meter to the header so a silent output chain is visible on the page rather than invisible.

The earlier hardening (arm the context inside the gesture, don't drop an early PLAY, `no-cache` on HTML)
stays: none of it was the cause, all of it is correct, and the cache fix is why a stale page could not
keep masking the result.

Lessons in `audio-processing/references/web-midi-and-soundfonts.md` — "A synth/plugin node does NOT
connect itself — and an internal counter is not evidence of sound".


## [2026-10-29] release | 01/24 LIVE on X — and the staged draft was pointing at the wrong cut

Coupe: *"release 01/24 on x through buffer"*. Published and verified.

**Live:** https://x.com/bzrlnxxx/status/2115597744513372520 — author **BZRLNXXX** (@bzrlnxxx),
created 2026-10-29T00:13:02Z, media **video 34.600 s**, caption verbatim with the `t.co` store link.

**Caught before it shipped: the staged draft was pointing at a superseded file.** Its asset URL was
`7a5c1699...` = **`clip_01_v3_buzz.mp4`** — the cut from *before* the motion cards, badge, store pill,
sting and end card. Publishing it would have opened the campaign with **no store link on the video at
all**, i.e. no funnel, silently and in public. Found by hashing: the relay's media filenames *are*
sha256 content hashes, so the URL decodes to an exact local file. Swapped the asset to
`final_slot01_buzz.mp4` (still a draft), read it back, then published.

**The duration is the receipt:** superseded cut 34.68 s, final 34.60 s, X reports **34.600 s** — the
correct furnished clip is definitively what went out.

**Slot 02's draft had the identical defect** — pointing at `clip_02_v3_buzz.mp4` (37.20 s) instead of
`final_slot02_buzz.mp4` (37.36 s). Swapped and left as a draft.

**Buffer publish mechanics learned the hard way (both silent no-ops):**
- `editPost` is a **full replacement, not a patch** — send only an id and a mode and it wipes the post
  (`Invalid post: Post must have either text or media`). Text and assets must be resent every time.
- **`mode: shareNow` alone does not publish.** It returns `PostActionSuccess` and the post stays
  `draft`/`addToQueue`. The actual switch is `saveToDraft: false` **plus** `mode: shareNow` →
  `scheduled` → `sent`.
- `externalLink` carries the live post URL.

**Verification without the platform API:** X reads return **402 credits depleted** and x.com **403s the
headless browser**, so the post was confirmed through X's own public oEmbed and syndication endpoints
(author, timestamp, media type, duration, caption). The display name now reads **BZRLNXXX** on the
live post — it had still been "Merc kHz" through the API.

Recorded in `shortform-social-campaigns/references/buffer-api-posting.md`.


## [2026-10-30] build | Drum sequencer overlay on the MIDI bench

Coupe wanted to repair MuScriptor's drum transcription by ear: an EDIT pen beside solo/mute on the
drum lane opening a step sequencer — 4/8/16 measures at a time, playing the track, editable **live
while it runs**, with a measure-jump box, total measure count, editable tempo, a PLACE button to push
the sequence into the DAW track, and RESET back to the transcription.

**Built and verified** at `ballademicz.com/daw/midi/` (EDIT on the 17b drums lane): 221 measures,
1467 transcribed hits across 7 voices; view 16 = 1792 cells; click toggles; playback live-editable
(added a hit ahead of the playhead: `fired 0 -> 11`); tempo 140 and back leaves edits intact; PLACE
writes 1469 hits and the main transport then sounds them (**rms 0.0665**); RESET returns the exact 1467.

**The finding that shaped the design — measure the grid fit before snapping.** The transcription is
**not** on a 16th grid: at the detected 93.9 BPM the median distance from the nearest 16th is **40.8 ms**
(p90 72.3, worst 79.7) and only **30.9%** of hits land within 25 ms. Snapping every hit on open would
have audibly re-timed two thirds of the performance the tool exists to repair. So each transcribed hit
**keeps its sub-step offset** (drawn as a shade inside the cell) and only hand-drawn hits land dead on
the grid.

**Two bugs of mine, both caught by measuring rather than reading:**

1. **The overlay was covering the page permanently and swallowing clicks.** `[hidden]` is only
   `display:none` from the UA stylesheet, and my CSS said `display:flex` — an author rule beats it. The
   modal looked "open but empty" because the click meant for the EDIT pen hit the overlay instead.
2. **Changing tempo silently deleted the user's edits**, because the handler rebuilt the grid from the
   original MIDI. Caught only because PLACE reported 1467 hits instead of the 1469 drawn. The grid is
   **step space**, which is tempo-independent — tempo now changes only the seconds-per-step.

Also fixed the scheduler's fired-step guard (an equality test let steps in a sliding lookahead window
fire twice; it is now a monotonic `lastFired` reset on every play/seek).

**Open question put to Coupe:** PLACE is in-memory only — the track reverts on reload. He needs to say
whether an edit is a scratchpad or the new source of truth for that stem.

Lessons recorded in `audio-processing/references/web-midi-and-soundfonts.md`.


## [2026-10-31] change | Deck: drum bed and sample pinned under the master, always active

Coupe: *"put 17a and 17b right under segment_01 17a named Sample and 17b named drum sequence both
should be activated."*

Lane order is now `01 MASTER · SAMPLE (267.4s) · DRUM SEQUENCE (560.0s) · 01/24 ... 24/24`, with both
reference lanes carrying working M/S/L, volume and pan.

**The trap this exposed: the deck derived public numbering from array position.** `buildTracks()` kept a
running `slot` counter over the non-master tracks and derived `pos` (`01/24...24/24`) and `dropDate` from
it. Moving two lanes to the top would therefore have **renumbered the entire campaign** - segment_02,
already live on X as 01/24, would have become 03/24, and every drop date would have shifted two slots.

**Fix: slot comes from the track's own config, never from list order.** `{ id:"segment_17a", ..., slot:16 }`.
Verified after the move: `segment_02 -> 01/24`, `segment_03 -> 02/24`, ... `segment_24 -> 24/24`, and the
NFT manifest's slot->stem mapping is **identical** to before (checked against the file, not assumed).

**Activation** is a new `alwaysOn` flag, honoured in both gates:
- date gate: `pending = !UNLOCK_ALL && !alwaysOn && TODAY_ISO < dropDate`
- NFT gate: `isStem` ignores `alwaysOn` manifest entries, so the two lanes are never gated

Verified: default load and `?today=2026-11-05` both leave SAMPLE + DRUM SEQUENCE open alongside the
released drops; under `?gate=nft` with no wallet they report `gated:false` while `segment_02` still
reports `gated:true`.

**Latent bug fixed in passing:** the master lane was located with `tracks.find(t => t.locked)`, but
**sealed lanes are also `locked`** - so the "master" was whichever locked lane came first in the list.
It was correct only by accident of the master sitting at index 0. Now keyed off `t.kind === "master"`.
Third bug of the same shape in this deck (sealed-lane label, roll track kind, now the master lookup):
**anything keyed off `locked` is suspect, because sealing sets it.**

Open question put to Coupe: the two lanes keep their internal slot numbers (16, 17) because they are the
two halves of segment_17 and the mint manifest depends on it. Treating them as outside the numbered 24
would renumber the campaign and the mint.
