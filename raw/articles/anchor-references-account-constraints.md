---
source_url: "https://www.anchor-lang.com/docs/references/account-constraints"
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
Account TypesAccount ConstraintsAnchor.toml ConfigurationAnchor CLIAnchor Version ManagerAccount SpaceRust to JS Type ConversionVerifiable BuildsSealevel AttacksExample ProgramsAnchor Project UpdatesRelease NotesChangelogContribution GuideSearch⌘KAnchor DocsGithubDiscordStack ExchangeOn this pageProgram Development
# Account Constraints
Anchor Account Constraints Examples

Minimal reference examples for Anchor account
constraints.

See the account constraints
source code
for implementation details.

## Normal Constraints

### `#[account(signer)]`

Description: Checks the given account signed the transaction. Consider using the
Signer type if you would only have this constraint on the account.
Examples: Github
|
Solpg

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(signer)]
#[account(signer @ <custom_error>)]`
```

### `#[account(mut)]`

Description: Checks the given account is mutable. Makes anchor persist any state
changes.
Examples: Github
|
Solpg

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(mut)]
#[account(mut @ <custom_error>)]`
```

### `#[account(dup)]`

Description: By default, Anchor prevents duplicate mutable accounts to avoid
potential security issues and unintended behavior. The `dup` constraint
explicitly allows this for cases where it's intentional and safe.

**Note**: This constraint only applies to mutable account (`mut`) types that
serialize on exit. Other types like `UncheckedAccount`, `Signer`,
`SystemAccount`, `AccountLoader`, `Program`, and `Interface` naturally allow
duplicates as they don't serialize data on exit.

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(mut, dup)]
#[account(mut, dup @ <custom_error>)]`
```

snippet[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[derive(Accounts)]
pub struct AllowsDuplicateMutable<'info> {
    #[account(mut)]
    pub account1: Account<'info, Counter>,
    // This account can be the same as account1
    #[account(mut, dup)]
    pub account2: Account<'info, Counter>,
}

pub fn allows_duplicate_mutable(ctx: Context<AllowsDuplicateMutable>) -> Result<()> {
    Ok(())
}`
```

### `#[account(init)]`

Description: Creates the account via a CPI to the system program and initializes
it (sets its account discriminator).
Examples: Github
|
Solpg

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(
    init,
    payer = <target_account>,
    space = <num_bytes>
)]`
```

### `#[account(init_if_needed)]`

Description: Same as init but only runs if the account does not exist yet.
Requires init-if-needed cargo feature.
Examples: Github
|
Solpg

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(
    init_if_needed,
    payer = <target_account>
)]

#[account(
    init_if_needed,
    payer = <target_account>,
    space = <num_bytes>
)]`
```

### `#[account(seeds, bump)]`

Description: Checks that given account is a PDA derived from the currently
executing program, the seeds, and if provided, the bump.
Examples: Github
|
Solpg

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(
    seeds = <seeds>,
    bump
)]

#[account(
    seeds = <seeds>,
    bump,
    seeds::program = <expr>
)]

#[account(
    seeds = <seeds>,
    bump = <expr>
)]

#[account(
    seeds = <seeds>,
    bump = <expr>,
    seeds::program = <expr>
)]`
```

### `#[account(has_one = target)]`

Description: Checks the target field on the account matches the key of the
target field in the Accounts struct.
Examples: Github
|
Solpg

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(
    has_one = <target_account>
)]

#[account(
    has_one = <target_account> @ <custom_error>
)]`
```

### `#[account(address = expr)]`

Description: Checks the account key matches the pubkey.
Examples: Github
|
Solpg

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(address = <expr>)]
#[account(address = <expr> @ <custom_error>)]`
```

### `#[account(owner = expr)]`

Description: Checks the account owner matches expr.
Examples: Github
|
Solpg

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(owner = <expr>)]
#[account(owner = <expr> @ <custom_error>)]`
```

### `#[account(executable)]`

Description: Checks the account is executable (i.e. the account is a program).
Examples: Github
|
Solpg

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(executable)]`
```

### `#[account(zero)]`

Description: Checks the account discriminator is zero. Use for accounts larger
than 10 Kibibyte.
Examples: Github
|
Solpg

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(zero)]`
```

### `#[account(close = target)]`

Description: Closes the account by sending lamports to target and resetting
data.
Examples: Github
|
Solpg

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(close = <target_account>)]`
```

### `#[account(constraint = expr)]`

Description: Custom constraint that checks whether the given expression
evaluates to true.
Examples: Github
|
Solpg

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(constraint = <expr>)]
#[account(
    constraint = <expr> @ <custom_error>
)]`
```

### `#[account(realloc)]`

Description: Used to realloc program account space at the beginning of an
instruction.
Examples: Github
|
Solpg

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(
    realloc = <space>,
    realloc::payer = <target>,
    realloc::zero = <bool>
)]`
```

### `#[account(discriminator = discrim)]`

Description: Used to override the discriminator for an account. All constant expressions are supported,
but all-zero discriminators are not.

In versions of Anchor before 1.0, program-owned accounts with zeroed discriminators (for example, by manually
initializing an `AccountInfo`, or as preparation for `#[zero]` initialization) can be taken over via IDL instructions.

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(discriminator = 12)]
#[account(discriminator = [1, 2, 3, 4])]
#[account(discriminator = MY_CONST_DISCRIMINATOR)]`
```

## SPL Constraints

### `#[account(token::*)]`

Description: Create or validate token accounts with specified mint and
authority.
Examples: Github
|
Solpg

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(
    token::mint = <target_account>,
    token::authority = <target_account>
)]

#[account(
    token::mint = <target_account>,
    token::authority = <target_account>,
    token::token_program = <target_account>
)]`
```

### `#[account(mint::*)]`

Description: Create or validate mint accounts with specified parameters.
Examples: Github
|
Solpg

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(
    mint::authority = <target_account>,
    mint::decimals = <expr>
)]

#[account(
    mint::authority = <target_account>,
    mint::decimals = <expr>,
    mint::freeze_authority = <target_account>
)]`
```

### `#[account(associated_token::*)]`

Description: Create or validate associated token accounts.
Examples: Github
|
Solpg

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(
    associated_token::mint = <target_account>,
    associated_token::authority = <target_account>
)]

#[account(
    associated_token::mint = <target_account>,
    associated_token::authority = <target_account>,
    associated_token::token_program = <target_account>
)]`
```

### `#[account(*::token_program = expr)]`

Description: The token_program can optionally be overridden.
Examples: Github
|
Solpg

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(*::token_program = <target_account>)]`
```

## Token Extensions Constraints

### `#[account(extensions::close_authority::*)]`

Description: Create or validate close authority extension on the mint account.

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(
    extensions::close_authority::authority = <target_account>
)]`
```

### `#[account(extensions::permanent_delegate::*)]`

Description: Create or validate permanent delegate extension on the mint
account.

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(
    extensions::permanent_delegate::delegate = <target_account>
)]`
```

### `#[account(extensions::transfer_hook::*)]`

Description: Create or validate transfer hook extension on the mint account.

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(
    extensions::transfer_hook::authority = <target_account>,
    extensions::transfer_hook::program_id = <target_account>
)]`
```

### `#[account(extensions::group_pointer::*)]`

Description: Create or validate group pointer extension on the mint account.

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(
    extensions::group_pointer::authority = <target_account>,
    extensions::group_pointer::group_address = <target_account>
)]`
```

### `#[account(extensions::group_member_pointer::*)]`

Description: Create or validate group member pointer extension on the mint
account.

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(
    extensions::group_member_pointer::authority = <target_account>,
    extensions::group_member_pointer::member_address = <target_account>
)]`
```

### `#[account(extensions::metadata_pointer::*)]`

Description: Create or validate metadata pointer extension on the mint account.

attribute[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`#[account(
    extensions::metadata_pointer::authority = <target_account>,
    extensions::metadata_pointer::metadata_address = <target_account>
)]`
```

## Instruction Attribute

### `#[instruction(...)]`

Description: You can access the instruction's arguments with the
`#[instruction(..)]` attribute. You must list them in the same order as in the
instruction handler but you can omit all arguments after the last one you need.
Skipping arguments will result in an error.

Examples:
Github
|
Solpg

snippet[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`
#[program]
pub mod example {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>, input: String) -> Result<()> {
        // --snip--
    }
}

#[derive(Accounts)]

#[instruction(input: String)]
pub struct Initialize<'info> {
    #[account(
        init,
        payer = signer,
        space = 8 + 4 + input.len(),
    )]
    pub new_account: Account<'info, DataAccount>,
    // --snip--
}`
```

Valid Usage:

snippet[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`

#[program]
pub mod example {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>, input_one: String, input_two: String) -> Result<()> {
        // --snip--
    }
}

#[derive(Accounts)]

#[instruction(input_one: String, input_two: String)]
pub struct Initialize<'info> {
    // --snip--
}`
```

snippet[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`
#[program]
pub mod example {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>, input_one: String, input_two: String) -> Result<()> {
        // --snip--
    }
}

#[derive(Accounts)]

#[instruction(input_one: String)]
pub struct Initialize<'info> {
    // --snip--
}`
```

Invalid Usage, will result in an error:

snippet[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}
```rust
`
#[program]
pub mod example {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>, input_one: String, input_two: String) -> Result<()> {
        // --snip--
    }
}

#[derive(Accounts)]

#[instruction(input_two: String)]
pub struct Initialize<'info> {
    // --snip--
}`
```
Previous

Account Types

Next

Anchor.toml Configuration

### On this page
[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}Normal Constraints`#[account(signer)]``#[account(mut)]``#[account(dup)]``#[account(init)]``#[account(init_if_needed)]``#[account(seeds, bump)]``#[account(has_one = target)]``#[account(address = expr)]``#[account(owner = expr)]``#[account(executable)]``#[account(zero)]``#[account(close = target)]``#[account(constraint = expr)]``#[account(realloc)]``#[account(discriminator = discrim)]`SPL Constraints`#[account(token::*)]``#[account(mint::*)]``#[account(associated_token::*)]``#[account(*::token_program = expr)]`Token Extensions Constraints`#[account(extensions::close_authority::*)]``#[account(extensions::permanent_delegate::*)]``#[account(extensions::transfer_hook::*)]``#[account(extensions::group_pointer::*)]``#[account(extensions::group_member_pointer::*)]``#[account(extensions::metadata_pointer::*)]`Instruction Attribute`#[instruction(...)]`Edit on GitHub