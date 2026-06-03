---
source_url: "https://www.anchor-lang.com/docs/references/space"
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
* On this pageProgram Development
# Account Space
Reference guide for calculating account data size (bytes) requirements by Rust type

This reference tells you how much space you should allocate for an account.

This only applies to accounts that don't use `zero-copy`. `zero-copy` uses
`repr(C)` with a pointer cast, so there the `C` layout applies.

In addition to the space for the account data, you have to add `8` to the
`space` constraint for Anchor's internal discriminator (see the example).

## Type chart

TypesSpace in bytesDetails/Examplebool1would only require 1 bit but still uses 1 byteu8/i81u16/i162u32/i324u64/i648u128/i12816[T;amount]space(T) * amounte.g. space([u16;32]) = 2 * 32 = 64Pubkey32Vec<T>4 + (space(T) * amount)String4 + length of string in bytesOption<T>1 + (space(T))Enum1 + Largest Variant Sizee.g. Enum { A, B { val: u8 }, C { val: u16 } } -> 1 + space(u16) = 3f324serialization will fail for NaNf648serialization will fail for NaN

## Example

[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account]
pub struct MyData {
    pub val: u16,
    pub state: GameState,
    pub players: Vec<Pubkey> // we want to support up to 10 players
}

impl MyData {

    pub const MAX_SIZE: usize = 2 + (1 + 32) + (4 + 10 * 32);
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, PartialEq, Eq)]
pub enum GameState {
    Active,
    Tie,
    Won { winner: Pubkey },
}

#[derive(Accounts)]
pub struct InitializeMyData<'info> {
    // Note that we have to add 8 to the space for the internal anchor

    #[account(init, payer = signer, space = 8 + MyData::MAX_SIZE)]
    pub acc: Account<'info, MyData>,
    pub signer: Signer<'info>,
    pub system_program: Program<'info, System>
}`
```

## The InitSpace macro

Sometimes it can be difficult to calculate the initial space of an account. This
macro will add an `INIT_SPACE` constant to the structure. It is not necessary
for the structure to contain the `#[account]` macro to generate the constant.
Here's an example:

[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account]

#[derive(InitSpace)]
pub struct ExampleAccount {
    pub data: u64,
    #[max_len(50)]
    pub string_one: String,
    #[max_len(10, 5)]
    pub nested: Vec<Vec<u8>>,
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(mut)]
    pub payer: Signer<'info>,
    pub system_program: Program<'info, System>,

    #[account(init, payer = payer, space = 8 + ExampleAccount::INIT_SPACE)]
    pub data: Account<'info, ExampleAccount>,
}`
```

A few important things to know:

Don't forget the discriminator when defining `space`

* The `max_len` attribute specifies the maximum number of elements in a Vec, not the total size in bytes.
For example, if you specify `#[max_len(10)]` for a `Vec<u32>`, it means:

Maximum 10 elements

* Each element (u32) takes 4 bytes

* The Vec itself has a 4-byte length prefix

* Total space = 4 + (10 * 4) = 44 bytes

Previous

Anchor Version Manager

Next

Rust to JS Type Conversion

### On this page
[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}Type chartExampleThe InitSpace macroEdit on GitHub