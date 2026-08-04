---
title: LawnCzar QR Referral Network
created: 2026-08-02
updated: 2026-08-02
type: concept
tags: [lawnczar, referral, crypto, solana, qr, affiliate, monetization]
sources: [js/referral-system.js, signup.html, server.js]
confidence: high
contested: false
contradictions: []
status: mvp-complete
---

# LawnCzar QR Referral Network

**QR-powered crypto affiliate network** for [[lawnczar]] — sellers and users sign up, get a Solana wallet + QR code, place it around their neighborhood, and earn commission on every purchase made by people who scan their code.

---

## 🔄 How It Works

```
1. SIGN UP                 2. DISTRIBUTE              3. SCAN                   4. EARN
┌────────────┐            ┌──────────────┐           ┌──────────────┐          ┌──────────────┐
│ User enters │            │ Print QR on  │           │ New user     │          │ 5% commission│
│ name + zip  │──→ wallet │ signs, post  │──→ QR    │ scans QR     │──→ app │ credited to   │
│ → Solana    │  + QR    │ around       │  scanned │ → opens with │  opens │ referrer's    │
│ wallet      │  created │ neighborhood │          │ referrer link│        │ Solana wallet │
└────────────┘            └──────────────┘           └──────────────┘          └──────────────┘
```

---

## 🏗️ Architecture

### Backend (`js/referral-system.js`)
- **Wallet creation**: `@solana/web3.js` Keypair.generate() → new Solana keypair per user
- **QR generation**: `qrcode` npm package → data URL PNG with referral link embedded
- **Referral tracking**: session-based — each QR scan creates a session linked to the referrer
- **Commission model**: 5% of purchase amount credited to referrer's ledger (configurable via `COMMISSION_RATE` env)
- **Payout threshold**: Auto-trigger on-chain SOL transfer when earnings exceed 0.1 SOL (configurable via `PAYOUT_THRESHOLD`)
- **On-chain balance**: Live Solana RPC query for wallet balance (devnet by default)

### API Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/referral/signup` | POST | Create wallet + QR code (`{name, zip}` → `{referralId, walletPubkey, qrCode, referralUrl}`) |
| `/api/referral/scan/:id` | GET | Resolve QR scan → create session |
| `/r/:referralId` | GET | QR landing page → 302 redirect to app with session token |
| `/api/referral/purchase` | POST | Record purchase → calculate + credit commission (`{sessionId, amount, txHash}`) |
| `/api/referral/dashboard/:id` | GET | Full dashboard: stats, events, QR code, wallet |
| `/api/referral/balance/:id` | GET | On-chain Solana wallet balance |
| `/api/referral/list` | GET | All referrers (admin) |

### Frontend (`signup.html`)
- Sign-up form: name + zip → wallet creation → QR code display + download
- Earnings dashboard: referral count, total earnings, on-chain balance, recent activity feed
- QR code downloadable as PNG for printing

---

## 💰 Commission Flow

```
New user buys $49 Single license (0.05 SOL)
  → 5% commission = 0.0025 SOL → credited to referrer ledger
  → Referrer total: 0.0025 SOL (< 0.1 threshold, no payout yet)

New user buys $149 Team license (0.15 SOL)
  → 5% commission = 0.0075 SOL → credited to referrer ledger
  → Referrer total: 0.01 SOL (< 0.1 threshold, no payout yet)

...accumulates until threshold reached...
  → processPayout() triggers on-chain SOL transfer to referrer wallet
  → Ledger resets, payout event recorded
```

### Config (`.env`)
```
COMMISSION_RATE=0.05      # 5%
PAYOUT_THRESHOLD=0.1      # 0.1 SOL
SOLANA_RPC=https://api.devnet.solana.com
APP_BASE_URL=http://localhost:3000
```

---

## 🧪 Tested End-to-End (2026-08-02)
1. ✅ Sign up "Maria from National City" (91950) → wallet `DE4LUR...`, QR generated (4390 chars)
2. ✅ QR scan → session created, referrer identified
3. ✅ Purchase 0.05 SOL → 0.0025 SOL commission credited
4. ✅ Purchase 0.15 SOL → 0.0075 SOL commission, total 0.01 SOL
5. ✅ Dashboard shows 1 referral, 0.01 SOL earned, 2 events
6. ✅ On-chain balance query (0 SOL — new devnet wallet)
7. ✅ QR redirect `/r/ref_xxx` → 302 to app with session token
8. ✅ Invalid referral → 404

---

## 🚀 Production Roadmap

### Current (MVP)
- In-memory stores (Map) — fine for dev/demo
- Solana devnet
- 5% flat commission

### Next Steps
- [ ] **MongoDB persistence** — move `users` and `sessions` to `db.collection('referral_users')` and `db.collection('referral_events')`
- [ ] **Wallet encryption** — encrypt secret keys at rest with AES-256
- [ ] **Stripe integration** — when user pays with Stripe, convert to SOL at current rate for commission
- [ ] **On-chain payouts** — implement actual SOL transfer from platform treasury to referrer wallet
- [ ] **Multi-tier commissions** — higher rate for sellers who refer other sellers (build both sides of marketplace)
- [ ] **QR analytics** — track scan locations, conversion rates, top-performing neighborhoods
- [ ] **Physical QR signage** — integrate with existing LawnCzar QR sign generation for yard sale postings
- [ ] **Mainnet deployment** — switch `SOLANA_RPC` to mainnet, fund treasury wallet

### Security Considerations
- Wallet secret keys stored in-memory only for MVP — **must encrypt before production**
- Session tokens should be JWT-signed with expiration
- Rate-limit signup endpoint to prevent wallet spam
- Commission calculation should be atomic (MongoDB transactions in production)

---

## 🔗 Cross-References
- [[lawnczar]] — main platform, markers, map, routing
- [[lawnczar-agentic-route-planning]] — route proxy and itinerary system
- [[solana-anchor]] — Solana smart contract patterns for on-chain commission distribution
- [[tokenized-equity]] — fractionalized ownership models that could apply to top referrers
- [[czarui]] — Stripe integration for payment processing that triggers commissions
