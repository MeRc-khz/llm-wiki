---
title: Buzz-CzarUI Integration
created: 2026-07-29
updated: 2026-07-29
type: concept
tags: [workflow, agentic, framework, tool-use]
sources: [raw/articles/buzz-github-repo.md]
confidence: medium
contested: false
contradictions: []
---

# Buzz-CzarUI Integration: Replacing Discord for bzr-dial Community Management

This page outlines the integration approach for using [[buzz]] as the community management platform for [[czarui]] and the bzr-dial-menu ecosystem, replacing Discord.

---

## Why Replace Discord?

The bzr-dial-menu ecosystem currently relies on Discord for community interaction, but Discord has fundamental limitations for this project:

1. **No agent integration** — Discord bots are second-class; Buzz agents are first-class members with own keys, audit trails, and full channel surface
2. **No git-native workflow** — Buzz turns branches into channels; CI, review, and merge decisions live in the same room
3. **No self-hosting** — Discord is SaaS lock-in; Buzz is Apache 2.0 and self-hostable on the same infrastructure
4. **No portable identity** — Discord identity is tied to the platform; Buzz uses Nostr keypairs (portable across relays)
5. **No YAML workflows** — Buzz has built-in automation; Discord requires external bot infrastructure
6. **No on-chain integration path** — Buzz's Nostr event model can bridge to [[solana-anchor|Solana Anchor]] events naturally

---

## Integration Architecture

```
                         ┌─────────────────────────────┐
                         │     Buzz Relay (self-hosted) │
                         │     buzz.bzzrr.link:3000     │
                         └───────────┬─────────────────┘
                                     │ WebSocket (NIP-01)
                 ┌───────────────────┼───────────────────┐
                 │                   │                   │
                 ▼                   ▼                   ▼
    ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
    │  Buzz Desktop App │  │  Agent (buzz-cli) │  │  CzarUI Backend  │
    │  (Tauri+React)    │  │  (Paperclip team) │  │  (Express :3001)  │
    │                   │  │                   │  │                   │
    │  Community members│  │  @mention triggers│  │  Stripe webhooks  │
    │  Channel chat     │  │  Code review      │  │  License delivery │
    │  Forum threads    │  │  Workflow runs    │  │  Revenue splits   │
    └──────────────────┘  └──────────────────┘  └────────┬─────────┘
                                                          │
                                                          │ HTTP webhook
                                                          ▼
                                               ┌──────────────────┐
                                               │  Buzz Workflow   │
                                               │  (YAML trigger)  │
                                               │                  │
                                               │  on stripe.event  │
                                               │  → post to channel│
                                               │  → trigger agent  │
                                               └──────────────────┘
```

---

## Phase 1: Deploy Buzz Relay (Self-Hosted)

**Goal:** Stand up a Buzz relay on the existing server infrastructure.

### Steps

1. **Docker Compose deployment** on the czarui server:
   ```bash
   cd /root/buzz/deploy/compose
   cp .env.example .env
   # Configure: DATABASE_URL, REDIS_URL, BUZZ_BIND_ADDR, RELAY_URL
   # Set RELAY_URL=ws://buzz.bzzrr.link:3000 (or behind Nginx TLS)
   # Generate owner keypair with buzz-admin keygen
   ./run.sh start
   ```

2. **Nginx reverse proxy** — add to existing config:
   ```nginx
   server {
       listen 443 ssl;
       server_name buzz.bzzrr.link;
       
       location / {
           proxy_pass http://127.0.0.1:3000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
       }
   }
   ```

3. **Postgres + Redis** — Buzz ships its own Docker Compose with Postgres 17 and Redis 7. These run alongside the existing czarui infrastructure (czarui backend uses its own Express server, no DB conflict).

4. **Generate owner keypair**:
   ```bash
   buzz-admin keygen  # produces hex private key + npub public key
   # Set RELAY_OWNER_PUBKEY in .env for closed relay mode
   ```

### Verification
- `curl http://127.0.0.1:3000/_liveness` returns 200
- Desktop app connects to `wss://buzz.bzzrr.link` and shows the community
- `buzz-cli` can authenticate with `BUZZ_PRIVATE_KEY` and list channels

---

## Phase 2: Channel Structure for bzr-dial Community

**Goal:** Set up the channel topology that mirrors and replaces the Discord server structure.

### Proposed Channels

| Channel | Type | Purpose |
|---------|------|---------|
| `#general` | Stream | Open discussion, replaces Discord #general |
| `#announcements` | Stream | Release notes, product updates (read-heavy, write-restricted) |
| `#support` | Stream | License support, bug reports |
| `#license-keys` | Forum | License delivery confirmation, key regeneration requests |
| `#dev-log` | Stream | Development progress, daily updates |
| `#revenue` | Stream | On-chain dividend announcements, revenue split reports |
| `#agent-ops` | Stream | Paperclip agent activity feed (auto-posted by agents) |
| `#releases` | Forum | Release notes archive (Discourse-like long-form) |
| `#github` | Stream | Git events from czarui repo (NIP-34 patches, pushes) |
| `#governance` | Forum | Token holder proposals, voting discussions |
| `#media` | Stream | Paperchasers, NFT drops, audio releases |

### Channel Templates

Buzz supports channel templates (`buzz-cli channel-templates`) — define the bzr-dial community structure once and apply it on any fresh relay.

---

## Phase 3: CzarUI Backend Webhook Integration

**Goal:** Bridge Stripe events from the czarui backend to Buzz channels.

### Approach: Buzz Workflow Webhook Trigger

Buzz workflows expose HTTP webhook endpoints at `/hooks/{id}`. The czarui backend (`server.js` :3001) can POST Stripe events directly to a Buzz workflow webhook.

1. **Create a Buzz workflow** that listens for webhook triggers:
   ```yaml
   # stripe-checkout-completed.yaml
   name: stripe-checkout-completed
   trigger:
     type: webhook
   conditions:
     - 'payload.type == "checkout.session.completed"'
   steps:
     - send_message:
         channel: license-keys
         content: |
           ✅ New license purchased!
           Customer: {{ payload.data.object.customer_email }}
           Product: {{ payload.data.object.metadata.product }}
           Amount: ${{ payload.data.object.amount_total / 100 }}
     - trigger_agent:
         agent: paperclip-coder
         message: "Generate and deliver license key for {{ payload.data.object.customer_email }}"
   ```

2. **Register the webhook** with `buzz-cli workflows create` — returns a webhook URL.

3. **Add to czarui backend** (`server.js`):
   ```javascript
   // After processing Stripe webhook, forward to Buzz
   async function notifyBuzz(stripeEvent) {
       await fetch('https://buzz.bzzrr.link/hooks/stripe-checkout', {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify(stripeEvent)
       });
   }
   ```

4. **Alternative: Direct buzz-cli integration** — the czarui backend can shell out to `buzz-cli` to post messages directly:
   ```javascript
   const { execSync } = require('child_process');
   function postToBuzz(channel, content) {
       execSync(`buzz-cli messages send --channel "${channel}" --content '${content}'`, {
           env: { ...process.env, BUZZ_RELAY_URL: 'http://localhost:3000', BUZZ_PRIVATE_KEY: process.env.BUZZ_BOT_KEY }
       });
   }
   ```

### Stripe Events to Bridge

| Stripe Event | Buzz Channel | Action |
|--------------|-------------|--------|
| `checkout.session.completed` | `#license-keys` | Post purchase confirmation, trigger license delivery agent |
| `payment_intent.payment_failed` | `#support` | Alert support team |
| `invoice.paid` | `#revenue` | Post revenue update, trigger dividend calculation |
| `customer.subscription.created` | `#license-keys` | Post new subscription |
| `customer.subscription.deleted` | `#support` | Alert retention team |

---

## Phase 4: Paperclip Agent Integration

**Goal:** Deploy Paperclip agents into Buzz as first-class community members.

### Agent Registration

Each Paperclip agent gets its own Nostr keypair and is added to relevant channels:

| Agent | Channels | Role |
|-------|----------|------|
| Paperclip Coder | `#dev-log`, `#github`, `#support` | Code review, patches, bug triage |
| Paperclip QA | `#dev-log`, `#github` | Test runs, CI reporting |
| Paperclip UX | `#general`, `#support` | User feedback analysis, UI suggestions |
| Paperclip Security | `#revenue`, `#governance` | Audit monitoring, security alerts |

### Agent Setup

```bash
# Generate keypair for each agent
buzz-admin keygen  # → save private key for each agent

# Register agent profile
buzz-cli agents create \
  --name "Paperclip Coder" \
  --pubkey <hex_pubkey> \
  --owner <owner_pubkey>

# Add agent to channels
buzz-cli channels members add \
  --channel dev-log \
  --pubkey <agent_pubkey> \
  --role bot
```

### ACP Harness

`buzz-acp` bridges @mentions in channels to AI agent backends. When a community member @mentions Paperclip Coder in `#support`, the ACP harness:
1. Receives the NIP-29 group message event
2. Routes it to the agent backend (Goose, Codex, Claude Code, or custom)
3. Agent processes and responds as a signed Nostr event in the same channel

This replaces Discord bot infrastructure entirely — agents are native members with full audit trails.

---

## Phase 5: Git-Native Development Workflow

**Goal:** Move czarui development from GitHub-centric to Buzz-native git.

### Approach

Buzz's relay hosts git repos via Smart HTTP. The czarui repo can be mirrored or migrated:

1. **Mirror czarui to Buzz relay git:**
   ```bash
   cd /srv/projects/czarui
   git remote add buzz https://buzz.bzzrr.link/czarui.git
   git push buzz main
   ```

2. **Branch-as-channel workflow:**
   - `git checkout -b feature/stripe-webhook-v2` on the dev machine
   - Buzz auto-creates a `#feature-stripe-webhook-v2` channel
   - CI posts results to the channel
   - Paperclip Coder reviews the patch in-channel
   - Merge decision recorded as NIP-34 event

3. **buzz-cli patch flow:**
   ```bash
   buzz-cli patches create --repo czarui --branch feature/stripe-webhook-v2
   buzz-cli pr create --title "Stripe webhook v2" --body "..." 
   buzz-cli pr review --pr-id <id> --approve
   buzz-cli pr merge --pr-id <id>
   ```

### GitHub Bridge

For continued GitHub visibility during transition, `git-sign-nostr` and `git-credential-nostr` allow pushing to both GitHub and Buzz simultaneously. NIP-34 events mirror to both surfaces.

---

## Phase 6: On-Chain Revenue Integration

**Goal:** Connect Buzz's event log to the [[solana-anchor|Solana Anchor]] dividend system at `/root/bzr-dial-contributor/`.

### Approach

When Stripe revenue is deposited on-chain via the contributor bridge (currently at `:3001`), the event can be posted to Buzz:

1. **Revenue workflow** in Buzz:
   ```yaml
   name: on-chain-deposit
   trigger:
     type: webhook
   steps:
     - send_message:
         channel: revenue
         content: |
           💰 Revenue deposited on-chain!
           Amount: {{ payload.amount }} USDC
           Tx: {{ payload.signature }}
           Split: 15% dividends / 10% conservation / 75% ops
     - trigger_agent:
         agent: paperclip-security
         message: "Verify on-chain deposit {{ payload.signature }} and post audit"
   ```

2. **Contributor bridge** posts to Buzz webhook after `deposit_revenue` instruction succeeds.

3. **Token holders** in the `#governance` channel can see real-time revenue flow and claim dividends — the Buzz channel becomes the community-facing view of the on-chain treasury.

---

## Phase 7: Community Migration

**Goal:** Migrate bzr-dial community from Discord to Buzz.

### Steps

1. **Announce migration** in Discord with Buzz relay URL and desktop app download link
2. **Onboard key members** — generate keypairs, add to channels
3. **Mirror important content** — pin key Discord messages as Buzz forum posts
4. **Set up agent activity feed** — Paperclip agents post to `#agent-ops` so members see what agents are doing
5. **Decommission Discord** — redirect Discord invites to `buzz.bzzrr.link`

### Desktop App Distribution

Buzz provides packaged builds for macOS (.dmg), Linux (.AppImage/.deb), and Windows (.exe) from GitHub releases. Community members download and connect to `wss://buzz.bzzrr.link`.

---

## Technical Requirements

| Component | Requirement |
|-----------|------------|
| Server | Existing VPS (same as czarui backend) |
| Docker | Compose v2.24.4+ |
| Postgres | 17 (Buzz ships its own container) |
| Redis | 7 (Buzz ships its own container) |
| MinIO | For media storage (optional, can skip initially) |
| Nginx | WebSocket proxy for TLS termination |
| Rust | 1.88+ (only if building from source) |
| Node | 24+ + pnpm 10+ (only if building desktop from source) |

### Ports

| Service | Port | Notes |
|---------|------|-------|
| Buzz Relay | 3000 | Internal; Nginx proxies 443 → 3000 |
| CzarUI Backend | 3001 | Existing Stripe webhook server |
| Postgres (Buzz) | 5432 | Buzz's own, separate from any czarui DB |
| Redis (Buzz) | 6379 | Buzz's own |
| Adminer | 8082 | DB browser (optional) |

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Buzz is actively developed (some features "being wired up") | Core relay, channels, messages, search, and agent CLI work today — that covers 90% of community management needs |
| Mobile clients not ready | Desktop app + web client cover desktop users; mobile users use web client initially |
| Workflow approval gates incomplete (WF-08) | Use message-based approvals as workaround; agents can react with 👍 to approve |
| Community adoption friction (new app) | Buzz desktop app is a normal installer — lower friction than Discord setup was |
| Buzz relay shares server with czarui | Docker isolation; Buzz uses its own Postgres + Redis containers |

---

## Summary

Buzz replaces Discord as the bzr-dial community platform by providing:
- **Self-hosted Nostr relay** at `buzz.bzzrr.link` with full data ownership
- **First-class agent membership** for the Paperclip team (no more bot API workarounds)
- **Stripe webhook bridging** via Buzz workflow webhooks → channel notifications
- **Git-native development** with branch-as-channel workflow for the czarui repo
- **On-chain revenue visibility** with Solana deposit events posted to community channels
- **YAML automation** replacing Discord bot infrastructure
- **Full-text search** across all community history
- **Tamper-evident audit log** for governance and compliance

The integration is phased — start with relay deployment and channel structure, then layer in Stripe webhooks, agent registration, git mirroring, and on-chain revenue posting. Each phase is independently valuable.