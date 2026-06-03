---
title: czarui
created: 2026-05-29
updated: 2026-05-29
type: entity
tags: [workflow, framework, database, agentic]
sources: [raw/articles/aieos-specification.md]
confidence: high
contested: false
contradictions: []
---

# czarui (bzr-dial-ui Sales System)

The **czarui** system (synced with the production repository `git@github.com:MeRc-khz/czarui.git` and cloned at `/root/czarui`) is the commercial licensing engine, Stripe transaction funnel, automatic license generator, and distribution hub for our interactive **[[ballademix|bzr-dial-menu]]** widgets and G-Funk interfaces. 

This platform serves as **[[the-conglomerate-group|The Conglomerate Group's]]** primary web component monetization gateway, packaging our premium Web Audio/Video widgets into commercial license classes.

---

## 🛠️ System & Codebase Architecture

The project contains the complete codebase to run a secure, automated digital-product storefront:

```
                  ┌────────────────────────────────────────────────────────┐
                  │                 Landing Storefront                     │
                  │              (Tailwind / index.html)                   │
                  └───────────────────────────┬────────────────────────────┘
                                              │
                                              │ Click "Buy Now"
                                              ▼
                  ┌────────────────────────────────────────────────────────┐
                  │                Stripe Checkout Flow                    │
                  │             (Stripe-Hosted Payment Page)               │
                  └───────────────────────────┬────────────────────────────┘
                                              │
                                              │ Payment Captured
                                              ▼
                  ┌────────────────────────────────────────────────────────┐
                  │                 NodeJS Backend Core                    │
                  │             (Express / server.js Webhook)              │
                  └─────────┬───────────────────────────┬──────────────────┘
                            │                           │
                            ▼                           ▼
                  ┌──────────────────┐        ┌──────────────────┐
                  │  License Manager │        │  Email Service   │
                  │ (Gen Cryptokey)  │        │ (SMTP / Receipt) │
                  └──────────────────┘        └──────────────────┘
```

### 1. The Storefront Landing Page (`/root/czarui/landing`)
- **File Assets:** `landing/index.html`, `landing/styles.css`, `landing/app.js`
- **Branding & Vibe:** Retro-futuristic, dark-themed, sleek layout showcasing interactive dials and video components in live preview blocks.
- **Conversion Flow:** Embeds direct Stripe Checkout pricing table buttons ($49 for Standard Developer license, $149 for Commercial/Studio license).

### 2. The NodeJS Backend Daemon (`/root/czarui/backend`)
- **File Assets:** `backend/server.js`, `backend/license-manager.js`, `backend/email-service.js`, `backend/package.json`
- **Webhook Endpoint:** Receives secure, signed `checkout.session.completed` webhooks from Stripe, cryptographically validating that the caller is indeed Stripe.
- **License Engine (`license-manager.js`):** Automatically generates secure, unique, and non-forgeable cryptographic license keys bound to the customer's email and session token.
- **Email Dispatcher (`email-service.js`):** Integrates SMTP connections (SendGrid, AWS SES, or custom Gmail API) to instantly mail the buyer their license keys and dedicated product download links.

### 3. The Premium Component Assets (`/root/czarui/components`)
Contains the premium web elements bundled and distributed to licensed buyers:
- **`lz-dial.js`:** The core interactive SVG/canvas-based dial selector widget. It features drag-and-spin coordinates, customizable friction, elastic rebounds, and custom keyboard controls.
- **`media-player-methods.js`:** Sophisticated, hardware-accelerated video/audio playback and state controller scripts (built to manage the loop slices for the *Paperchase* video walls).
- **`ipfs-config.js`:** Built-in Kubo IPFS gateway configurations to allow buyers to serve dial widgets over decentralised protocols.

---

## 🪙 Stripe Business & Revenue Strategy

The system is configured to support the monetization goals of **The Conglomerate Group** and its founders, mapping physical cash flows back into the digital ecosystem:

### 1. Packaging Classes
Under `PACKAGING_GUIDE.md`, the visual widgets are partitioned into distinct tiers:
*   **Developer Class ($49):** Single-domain license, compiled JS access, Standard updates.
*   **Studio/Mogul Class ($149):** Unlimited domains, raw source code access, premium IPFS hooks, and priority support from our Paperclip Agent Team.

### 2. Automated Web3 Revenue Splits
To support our **[[tokenized-equity|Tokenized Equity Framework]]**:
1. Stripe captures fiat credit card and Apple Pay payments.
2. Revenues flow up to the corporate Stripe account.
3. Our automated backend scripts (under development) periodically convert the Stripe fiat balance to digital USDC.
4. The USDC is pushed directly to our on-chain Gnosis multi-sig treasury at `0x7890123456789012345678901234567890123456` or the Solana settlement address `B1Z4rr3LyNxSeLfArChItEcT7777777777777777` where holders can programmatically "pull" their dividend share.
