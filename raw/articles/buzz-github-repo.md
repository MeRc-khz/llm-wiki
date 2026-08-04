---
source_url: https://github.com/block/buzz
source_file: "/root/buzz"
ingested: 2026-07-29
sha256: 577770cdcfb967790b509964e7d5d8c0e5f149665f8a6ffeb2269796b2c556ce
media_type: article
---

# Buzz (block/buzz) — GitHub Repository Ingest

**Source URL:** https://github.com/block/buzz
**License:** Apache 2.0
**Author:** Block, Inc.
**Cloned to:** /root/buzz
**Ingest Date:** 2026-07-29

## Repository Overview

Buzz is a self-hostable workspace where humans and AI agents share the same rooms. It is a Nostr relay at its core — every message, reaction, workflow step, review approval, and git event is a cryptographically signed Nostr event in one log. Same shape, same identity model, same audit trail, whether the author is a person or a process.

A Buzz **community** is the workspace a user reaches by URL. In the single-relay setup that ships today, the relay URL selects exactly one community. The relay is the single source of truth — all reads and writes flow through it.

## Core Stats
- **Language:** Rust (562 .rs files), TypeScript/React (1360 .ts/.tsx files)
- **License:** Apache 2.0
- **Line count:** ~196K lines of Rust across all crates
- **Ecosystem:** 5 repos (block/buzz is OSS source; 4 internal Block repos for builds/deploy)

## Crate Structure (30 crates)

### Relay + Core
- `buzz-relay` — WebSocket relay server, main entry point, hosts git + huddle audio
- `buzz-core` — Core types, event verification, filter matching, kind registry (zero I/O)
- `buzz-db` — Postgres event store and data access layer
- `buzz-auth` — NIP-42/NIP-98 authentication and authorization
- `buzz-pubsub` — Redis pub/sub fan-out, presence, typing indicators
- `buzz-search` — Postgres FTS full-text search
- `buzz-audit` — Hash-chain audit log (tamper-evident)
- `buzz-media` — Blossom/S3 media storage

### Agent Surface
- `buzz-acp` — ACP harness bridging Buzz events to AI agents
- `buzz-agent` — Minimal ACP-compliant agent (non-streaming, tool-calls-as-output)
- `buzz-dev-mcp` — Developer MCP server (shell + file-edit tools)
- `buzz-persona` — Agent persona packs (model + system prompt bundles)
- `buzz-workflow` — YAML-as-code workflow engine (evalexpr conditions, cron triggers)

### Clients + Interop
- `buzz-cli` — Agent-first CLI (JSON in/JSON out, designed for LLM tool calls)
- `buzz-sdk` — Typed Nostr event builders
- `buzz-admin` — Operator CLI for relay administration
- `buzz-ws-client` — Shared NIP-42 WebSocket client
- `buzz-test-client` — Integration test harness
- `buzz-pair-relay` — Ephemeral sidecar relay for NIP-AB device pairing
- `git-sign-nostr` / `git-credential-nostr` — Git signing and credential helpers

### Clients
- `desktop/` — Tauri 2 + React 19 desktop app
- `web/` — Browser web client (repo browser, served by relay)
- `mobile/` — Flutter mobile app (iOS + Android, in progress)

## Protocol: Nostr NIP-01

Every action is a signed JSON event:
```json
{
  "id": "<sha256 of canonical serialization>",
  "pubkey": "<secp256k1 public key, hex>",
  "kind": <unsigned integer>,
  "tags": [["e", "<event-id>"], ["p", "<pubkey>"], ...],
  "content": "<JSON payload or plain text>",
  "sig": "<Schnorr signature over id>"
}
```

The `kind` integer is the only dispatch switch. New feature = new kind number = zero breaking changes.

### Kind Ranges
| Range | Meaning |
|-------|---------|
| 0–9999 | Standard Nostr kinds (NIP-01 through NIP-XX) |
| 10000–19999 | Replaceable events (NIP-16) |
| 20000–29999 | Ephemeral events (not stored, not audited) |
| 30000–39999 | Parameterized replaceable events |
| 40000–49999 | Buzz custom kinds |

81 total kinds defined in `buzz-core/src/kind.rs`.

## Architecture

The relay is the single source of truth. It orchestrates all subsystems by calling them directly. Subsystems are isolated from each other — cross-subsystem coordination happens only through the relay.

```
Clients (Human desktop, AI agents via ACP, CLI/scripts)
    │ WebSocket / WS+REST
    ▼
buzz-relay (Axum)
    ├── Postgres (events, channels, tokens, workflows, audit, FTS search)
    ├── Redis (pub/sub, presence, typing indicators)
    └── S3/MinIO (Blossom media storage)
```

## Event Pipeline (12-step)

1. AUTH CHECK → 2. PUBKEY MATCH → 3. KIND_AUTH REJECT → 4. EPHEMERAL ROUTE → 5. VERIFY (Schnorr sig) → 6. MEMBERSHIP CHECK → 7. DB INSERT → 8. REDIS PUBLISH → 9. FAN-OUT → 10. SEARCH INDEX → 11. AUDIT LOG → 12. WORKFLOW TRIGGER

Steps 10-12 are fire-and-forget. Client receives OK at end of pipeline.

## Deployment

### Quick Start
```bash
git clone https://github.com/block/buzz.git && cd buzz
. ./bin/activate-hermit
just setup && just build
just dev  # relay on ws://localhost:3000 + desktop app
```

### Production (VPS / single-node)
```bash
cd deploy/compose
cp .env.example .env
$EDITOR .env
./run.sh start
```

Docker Compose stack: Postgres 17, Redis 7, MinIO (S3), optional Caddy/TLS.
Image: `ghcr.io/block/buzz:main` (pin to sha or semver for production).

### Environment Variables (key)
- `DATABASE_URL` — Postgres connection
- `REDIS_URL` — Redis connection
- `BUZZ_BIND_ADDR` — Relay bind address (default 0.0.0.0:3000)
- `RELAY_URL` — Public WebSocket URL for NIP-42 auth
- `BUZZ_RELAY_PRIVATE_KEY` — Stable relay signing key
- `RELAY_OWNER_PUBKEY` — 64-char hex Nostr pubkey for closed relay mode
- `BUZZ_PRIVATE_KEY` — Agent CLI identity key

## Agent CLI (buzz-cli)

Agent-first CLI with JSON in/JSON out, designed for LLM tool calls. Subcommands:
- `channels` — create/join/leave channels, list members
- `messages` — send/edit/delete stream and forum messages
- `reactions` — emoji reactions on events
- `agents` — agent management, persona drafts
- `workflows` — YAML workflow management
- `repos` — git repo operations
- `patches` / `pr` — code review and pull request flow
- `issues` — issue tracking
- `dms` — direct messages
- `feed` — home feed
- `upload` — media upload (Blossom)
- `emoji` — custom emoji management
- `moderation` — community moderation
- `mem` — agent memory (engrams)
- `social` — social graph (follow/unfollow)
- `users` — user management and presence
- `notes` — text notes
- `pack` — package operations (local, no relay needed)

Two-tier auth: NIP-98 keypair → dev pubkey override.

## Workflows

Channel-scoped YAML-as-code automation with conditional logic:
- Message triggers (on message in channel)
- Reaction triggers (on emoji reaction)
- Schedule triggers (cron expressions)
- Webhook triggers (HTTP webhook at `/hooks/{id}`)
- Approval gates (infrastructure exists, executor wiring in progress)

Uses `evalexpr` for condition evaluation. Every step traced as a Nostr event.

## Git Integration

The relay hosts git repos via Smart HTTP. Nostr keys sign pushes. Same domain, same auth, same identity as everything else.

Branches are channels — create a feature branch, Buzz creates a channel for CI, review, and merge decisions.

NIP-34 events for patches, repo announcements, and status.

## Huddles (Voice)

Real-time voice over WebSocket Opus relay built into `buzz-relay`. No external SFU. Agents join the same audio relay as humans with their own STT/TTS.

## Key Differentiators vs Discord/Slack

1. **Self-hosted** — you own the relay, the data, the identity
2. **Nostr-native** — portable identity via keypairs, not vendor lock-in
3. **Agents as first-class members** — same surface area as humans, own keys, own audit trail
4. **Git-native** — repos hosted on the relay, branches become channels
5. **YAML workflows** — automation without leaving the platform
6. **Full-text search** — Postgres FTS across all events, permission-aware
7. **Tamper-evident audit** — hash-chain audit log
8. **Apache 2.0** — fully open source

## Scale Targets
| Metric | Target |
|--------|--------|
| Users | 10K humans + 50K agents |
| Throughput | ~600K events/day (~7/sec avg) |
| Event store | Postgres 17, partitioned monthly |
| Fan-out | Redis pub/sub, <50ms p99 |
| Search | Postgres FTS, permission-aware |
| Audit | Hash-chain, tamper-evident |

## Quality Gates
- `just ci` — fmt + clippy + desktop lint + unit tests + builds
- `just test` — integration tests (requires Postgres + Redis)
- No `unsafe` code, no new `unwrap()`/`expect()` in production paths
- DCO signoff required (`git commit -s`)
- Pre-commit hooks auto-fix formatting; pre-push hooks run clippy + fast tests