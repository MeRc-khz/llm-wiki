---
title: Solana NFT Dividend Pattern (Pull vs. Push)
created: 2026-07-08
updated: 2026-07-08
type: query
tags: [architecture, workflow, framework]
sources: [raw/articles/anchor-basics-cpi.md, raw/articles/makeufamous-tokenization-proposal.md]
confidence: high
contested: false
contradictions: []
---

# Solana NFT Dividend Pattern (Pull vs. Push)

**Question:** How do you distribute royalties / dividends to thousands of NFT holders on Solana without blowing the transaction budget?

**Answer (filed synthesis):** Use the **Pull** (claim-based) pattern, not Push.

## Why Push fails
Pushing SOL / USDC to every holder in a loop exceeds Solana's 1232-byte transaction size limit and incurs massive cumulative fee overhead. It does not scale past a handful of wallets.^[raw/articles/anchor-basics-cpi.md]

## How Pull works
1. Revenues (fiat via Stripe, or on-chain) accumulate in a program **vault PDA**.
2. The program tracks `total_accumulated_dividends_per_share` globally.
3. Each holder has a tiny **`ClaimState` PDA** (`seeds = [b"claim-state", user, nft_mint]`) recording what they have already pulled.
4. On claim, the program CPIs USDC from the vault PDA to the holder, then updates their `claim_state`.
5. **Gas is paid by the claimer**, so cost scales to 10,000+ holders with zero platform overhead.^[raw/articles/anchor-basics-cpi.md]

## Where this is deployed
- **[[ballademix|Ballademix]]** — generative-beat NFTs with dividend-bearing tiers.
- **[[makeufamous|MakeUFamo.us]]** — ERC-1155 song shares wrapped in a **[[tokenized-equity|Wyoming DAO LLC]]**, with a Gnosis Safe treasury feeding the same pull contract.^[raw/articles/makeufamous-tokenization-proposal.md]
- **[[czarui|czarui]]** — Stripe fiat → USDC conversion feeds the on-chain treasury.

## See also
- [[solana-anchor]] — full Anchor program structure, PDA mechanics, and the `ClaimDividends` account-validation code.
- [[tokenized-equity]] — the legal wrapper + smart-contract architecture that sits above this pattern.
