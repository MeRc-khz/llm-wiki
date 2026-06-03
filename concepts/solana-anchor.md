---
title: Solana Development with Anchor
created: 2026-05-26
updated: 2026-05-26
type: concept
tags: [architecture, framework, workflow]
sources:
  - raw/articles/anchor-basics-program-structure.md
  - raw/articles/anchor-basics-pda.md
  - raw/articles/anchor-basics-cpi.md
  - raw/articles/anchor-references-account-constraints.md
  - raw/articles/anchor-references-space.md
  - raw/articles/anchor-references-security-exploits.md
confidence: high
contested: false
contradictions: []
---

# Solana Smart Contract Development with Anchor

The **Anchor Framework** is the industry-standard developer suite for building secure, efficient, and structured smart contracts (known as **Programs**) on the **Solana** blockchain. Written in **Rust**, Anchor handles boilerplate serialization/deserialization, automates account validation, auto-generates Interface Definition Languages (IDLs), and enforces strict security constraints.

---

## ⚙️ Core Solana & Anchor Mechanics

Unlike Ethereum's EVM, where smart contracts are stateful and self-contained, Solana segregates **Code** from **State**:
* **State-less Programs:** Programs contain only executable logic (read-only instruction files).
* **State-full Accounts:** All persistent data (balances, NFT metadata, system configurations) is stored in separate, external **Accounts**.
* **Rent Exemption:** To store data on-chain, accounts must maintain a minimum balance of SOL (lamports) called the "rent-exempt reserve," proportional to the account's allocated `space` (bytes). Optimizing space is the primary way to lower "gas fees" (rent deployment costs) on Solana.

---

## 🛠️ Anchor Program Structure

A standard Anchor program consists of three core components:
1. **`declare_id!` Macro:** Defines the program's public key (on-chain address).
2. **`#[program]` Module:** Contains the execution endpoints (instruction handlers).
3. **`#[derive(Accounts)]` Structs:** Declaratively defines and validates the list of accounts required by each instruction.

```rust
use anchor_lang::prelude::*;

declare_id!("MyProgramAddress11111111111111111111111111");

#[program]
pub mod nft_dividends {
    use super::*;

    // 1. Instruction Handler
    pub fn initialize_vault(ctx: Context<InitializeVault>, total_nfts: u16) -> Result<()> {
        let vault_state = &mut ctx.accounts.vault_state;
        vault_state.total_nfts = total_nfts;
        vault_state.accumulated_dividends = 0;
        vault_state.bump = ctx.bumps.vault_state;
        Ok(())
    }
}

// 2. Account Validation Struct
#[derive(Accounts)]
pub struct InitializeVault<'info> {
    #[account(
        init,
        payer = authority,
        space = 8 + 2 + 8 + 1, // Anchor Discriminator + u16 + u64 + u8
        seeds = [b"vault-state"],
        bump
    )]
    pub vault_state: Account<'info, VaultState>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
}

// 3. On-chain State Account
#[account]
pub struct VaultState {
    pub total_nfts: u16,               // 2 bytes
    pub accumulated_dividends: u64,    // 8 bytes
    pub bump: u8,                      // 1 byte
}
```

---

## 🗝️ PDAs (Program Derived Addresses) & Seeds

**Program Derived Addresses (PDAs)** are a core cryptographic feature of Solana. They are public keys that **do not have a corresponding private key**. Instead, they are deterministically derived using a combination of optional seed strings and the program's ID, finding a key that falls off the Ed25519 elliptic curve.

### Primary Uses:
* **Decentralized Storage Key:** Acting as a database key to store user-specific states (e.g., deriving a claim-status account using the seeds: `[b"claim-state", user_wallet.key().as_ref()]`).
* **On-Chain Vaults:** Allowing a program to sign transactions programmatically (e.g. transferring SOL/USDC out of a vault PDA using seeds and its bump).

---

## 💰 Gas Optimization & Space Allocation (LAMPORT Savings)

In Solana, storage cost is paid upfront upon account initialization. If your program allocates more space than needed, you freeze valuable SOL. 

### Size of Core Types in Rust/Anchor:
* `u8`, `bool`: `1 byte`
* `u16`: `2 bytes`
* `u32`, `f32`: `4 bytes`
* `u64`, `f64`: `8 bytes` (standard for balances / lamports)
* `Pubkey`: `32 bytes`
* `Option<T>`: `1 byte` + size of `T`
* **Anchor Discriminator:** Every `#[account]`-marked struct includes an automatic, prepended **8-byte header** (discriminator) used to verify that the read account matches the expected type.

### Rent-Saving Best Practices:
1. **Fixed arrays over Vectors:** Use fixed arrays like `[u8; 16]` instead of `Vec<u8>` or `String` which require padding and overhead.
2. **Strict Sizing:** Never guess space. Calculate explicitly: `space = 8 (discriminator) + size_of_fields`.
3. **Reuse Accounts:** Close unused accounts using the `close` constraint to reclaim the locked SOL rent balance back to your wallet!

---

## 🏆 Decentralized NFT Dividend Pattern (Pull vs. Push)

For the **[[ballademix|Ballademix]]** and **[[makeufamous|MakeUFamo.us]]** ecosystems, distributing royalties/dividends to thousands of NFT holders on-chain requires a scalable, gas-efficient architecture.

### The "Push" Anti-Pattern (Inefficient & Will Fail)
* **The Flow:** The platform iterates through all NFT holders and pushes SOL/USDC directly to their wallets.
* **Why it fails:** Exceeds transaction size limits (max 1232 bytes), computation budget, and incurs massive transaction fee overhead.

### The "Pull" Pattern (Scalable & Hyper-Efficient)
* **The Flow:** Platform revenues are collected in a centralized program vault PDA. The program maintains a global counter of `total_accumulated_dividends_per_share`. Each NFT holder owns a tiny PDA (`ClaimState`) tracking what share they have *already* pulled.
* **The Claim:** When an NFT holder wants their dividends, they initiate a single transaction:
  1. The program validates that the user actually holds the required NFT in their wallet (by reading their Associated Token Account / Metaplex Metadata).
  2. Calculates the claimable amount: `claimable = (global_accumulated_per_share - user_claimed_per_share) * nft_balance`.
  3. Executes a **CPI (Cross-Program Invocation)** to transfer that amount from the program's vault PDA directly to the user's wallet.
  4. Updates the user's `claim_state` PDA to match the global counter.

### Pull Pattern Accounts Validation:
```rust
#[derive(Accounts)]
pub struct ClaimDividends<'info> {
    #[account(
        mut,
        seeds = [b"global-vault-state"],
        bump = global_vault.bump
    )]
    pub global_vault: Account<'info, GlobalVault>,
    
    /// CHECK: Safe. Checked via seeds and bump
    #[account(
        mut,
        seeds = [b"vault-token-account"],
        bump
    )]
    pub vault_pda_signer: AccountInfo<'info>,

    #[account(
        init_if_needed,
        payer = user,
        space = 8 + 8 + 1, // Discriminator + u64 (already_claimed) + u8 (bump)
        seeds = [b"claim-state", user.key().as_ref(), nft_mint.key().as_ref()],
        bump
    )]
    pub user_claim_state: Account<'info, UserClaimState>,

    // Verification that user owns the token account representing the NFT
    #[account(
        constraint = nft_token_account.owner == user.key(),
        constraint = nft_token_account.mint == nft_mint.key(),
        constraint = nft_token_account.amount == 1 // Must own 1 NFT
    )]
    pub nft_token_account: Account<'info, TokenAccount>,
    pub nft_mint: Account<'info, Mint>,

    #[account(mut)]
    pub user: Signer<'info>,
    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
}
```

This "Pull" pattern ensures that **gas/rent costs are entirely paid by the claiming user** upon executing their withdrawal, scaling effortlessly to 10,000+ NFT holders without cost or congestion overhead on the platform creators.
