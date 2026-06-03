---
source_url: "https://www.anchor-lang.com/docs/basics/pda"
ingested: 2026-05-26
media_type: article
---

Anchor Docs
[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}GithubDiscordStack ExchangeGetting Started
InstallationQuickstart
Solana PlaygroundLocal DevelopmentCore Concepts
The Basics
Program StructureProgram IDL FileProgram Derived AddressCross Program InvocationClient LibrariesTypeScriptRustTesting LibrariesLiteSVMMolluskAdditional FeaturesDependency Free ComposabilityCustom ErrorsEmit EventsZero CopyFootgunsSPL Tokens
Interacting with Tokens
BasicsExtensionsReferences
Program Development
Account TypesAccount ConstraintsAnchor.toml ConfigurationAnchor CLIAnchor Version ManagerAccount SpaceRust to JS Type ConversionVerifiable BuildsSealevel AttacksExample ProgramsAnchor Project UpdatesRelease NotesChangelogContribution GuideSearch⌘KAnchor DocsGithubDiscordStack Exchange
* On this pageThe Basics
# Program Derived Address
Learn how to use Program Derived Addresses (PDAs) in Anchor programs to create deterministic account addresses.

Program Derived Addresses (PDA) refer to a feature of Solana development that
allows you to create a unique address derived deterministically from pre-defined
inputs (seeds) and a program ID.

This section will cover basic examples of how to use PDAs in an Anchor program.

## Anchor PDA Constraints

When using PDAs in an Anchor program, you generally use Anchor's account
constraints to define the seeds to derive the PDA. These constraints serve as
security checks to ensure that the correct address is derived.

The constraints used to define the PDA seeds include:

`seeds`: An array of optional seeds used to derive the PDA. Seeds can be
static values or dynamic references to account data.

* `bump`: The bump seed used to derive the PDA. Used to ensure the address falls
off the Ed25519 curve and is a valid PDA.

* `seeds::program` - (Optional) The program ID used to derive the PDA address.
This constraint is only used to derive a PDA where the program ID is not the
current program.

The `seeds` and `bump` constraints are required to be used together.

### Usage Examples

Below are examples demonstrating how to use PDA constraints in an Anchor
program.

seedsbumpseeds::programinit
The `seeds` constraint specifies the optional values used to derive the PDA.
No Optional Seeds

* Use an empty array `[]` to define a PDA without optional seeds.
[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[derive(Accounts)]
pub struct InstructionAccounts<'info> {
    #[account(

        seeds = [],
        bump,
    )]
    pub pda_account: SystemAccount<'info>,
}`
```
Single Static Seed

* Specify optional seeds in the `seeds` constraint.
[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[derive(Accounts)]
pub struct InstructionAccounts<'info> {
    #[account(

        seeds = [b"hello_world"],
        bump,
    )]
    pub pda_account: SystemAccount<'info>,
}`
```
Multiple Seeds and Account References

* Multiple seeds can be specified in the `seeds` constraint. The `seeds`
constraint can also reference other account addresses or account data.
[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[derive(Accounts)]
pub struct InstructionAccounts<'info> {
    pub signer: Signer<'info>,
    #[account(

        seeds = [b"hello_world", signer.key().as_ref()],
        bump,
    )]
    pub pda_account: SystemAccount<'info>,
}`
```
The example above uses both a static seed (`b"hello_world"`) and a dynamic seed
(the signer's public key).

## PDA seeds in the IDL

Program Derived Address (PDA) seeds defined in the `seeds` constraint are
included in the program's IDL file. This allows the Anchor client to
automatically resolve account addresses using these seeds when constructing
instructions.

This example below shows the relationship between the program, IDL, and client.

ProgramIDLClient
The program below defines a `pda_account` using a static seed (`b"hello_world"`)
and the signer's public key as a dynamic seed.

[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`use anchor_lang::prelude::*;

declare_id!("BZLiJ62bzRryYp9mRobz47uA66WDgtfTXhhgM25tJyx5");

#[program]
mod hello_anchor {
    use super::*;
    pub fn test_instruction(ctx: Context<InstructionAccounts>) -> Result<()> {
        msg!("PDA: {}", ctx.accounts.pda_account.key());
        Ok(())
    }
}

#[derive(Accounts)]
pub struct InstructionAccounts<'info> {

    pub signer: Signer<'info>,
    #[account(

        seeds = [b"hello_world", signer.key().as_ref()],
        bump,
    )]
    pub pda_account: SystemAccount<'info>,
}`
```
Previous

Program IDL File

Next

Cross Program Invocation

### On this page
[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}Anchor PDA ConstraintsUsage ExamplesPDA seeds in the IDLEdit on GitHub