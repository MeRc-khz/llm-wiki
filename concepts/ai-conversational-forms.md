---
title: AI Conversational Forms
created: 2026-07-28
updated: 2026-07-28
type: concept
tags: [workflow, framework, agentic]
sources: [raw/articles/ai-conversational-forms.md]
confidence: high
contested: false
contradictions: []
---

# AI Conversational Forms — bzr-dial-menu Modal

**AI Conversational Forms** is a modal system for [[czarui|bzr-dial-menu]] that replaces traditional HTML forms with a conversational chat interface. Instead of rendering a static form with all fields at once, the AI walks the user through each field sequentially — asking, validating, and advancing one step at a time.

## Core Idea

Traditional forms dump all fields on the user at once. Conversational forms turn form completion into a dialogue — the AI asks one question at a time, validates the answer, then moves to the next field. This creates a guided, higher-conversion experience.

## How It Works

1. User triggers form (login, registration, checkout, etc.)
2. AI modal opens in the chat window
3. AI asks for the first field value
4. User responds in chat
5. AI validates — if invalid, re-prompts with specific feedback
6. AI advances to next field
7. Elements appear in chat in the order defined by form steps

## Element Types in Chat

The system renders actual form elements inline in the chat — not just text:

| Element | Type Syntax | Chat Rendering |
|---------|------------|----------------|
| Text input | `type: text` | AI asks, user types |
| Password | `type: text` + `mask: true` | Masked input |
| Dropdown | `type: dropdown` | Tappable list in chat |
| Radio buttons | `type: radio` | Choice cards |
| Toggle switch | `type: switch` | Chat-native toggle |
| Date picker | `type: date` | Calendar widget |

## Form Definition Syntax

Forms are described in `.md` files using extended fenced code blocks — the same pattern as code snippets use triple backticks + language name:

````markdown
```form:login
steps:
  - type: text
    name: username
    label: "Username"
    validate: required,min:3,max:20
    prompt: "What's your username?"

  - type: text
    name: password
    label: "Password"
    validate: required,min:8
    prompt: "Enter your password"
    mask: true
```
````

The `form:<name>` fence identifier mirrors the `language` slot in standard code blocks — a parser-friendly convention that fits naturally in markdown.

## Validation

Comma-separated rules in the `validate` field:
- `required` — cannot be empty
- `min:N` / `max:N` — length or value bounds
- `email` — email format check
- `pattern:regex` — custom regex

Failed validation triggers an AI re-prompt with specific feedback.

## Strategic Value

For the [[the-conglomerate-group|Conglomerate Group]] portfolio:

- **Higher conversion** — guided flows outperform static forms
- **Cross-project** — same form engine powers [[czarui]] checkout, [[makeufamous]] onboarding, [[ballademix]] NFT minting
- **Revenue impact** — less friction = more license sales, more mints, more signups
- **Brand-aligned** — conversational AI fits the [[bizarre-lynx|Bizarre Lynx]] entertainment persona

## Use Cases

| Flow | Fields | Project |
|------|--------|---------|
| Login | username → password | All platforms |
| Registration | email → tier → preferences | [[czarui]] |
| Checkout | billing → payment → license key | [[czarui]] Stripe |
| NFT minting | metadata → royalty split → mint | [[ballademix]] |
| Contributor onboarding | wallet → role → deposit | [[tokenized-equity]] |

## Related

- [[czarui]] — bzr-dial-menu licensing engine
- [[aieos-integration]] — AIEOS agent forms and profiles
- [[tokenized-equity]] — contributor onboarding flows
- [[ballademix]] — NFT minting metadata forms
