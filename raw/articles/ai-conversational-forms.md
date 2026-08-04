---
source_url: ""
ingested: 2026-07-28
sha256: pending
media_type: article
---

# AI Conversational Forms Modal — bzr-dial-menu

## Concept

An AI-driven modal system for bzr-dial-menu that captures form data through conversational chat instead of traditional HTML form fields. The AI talks the user through each form step sequentially, validating as it goes.

## How It Works

1. User triggers form (e.g., login, registration, checkout)
2. AI modal opens in chat window
3. AI asks for first field (e.g., "What's your username?")
4. User responds in chat
5. AI validates the input — if invalid, asks again with feedback
6. AI moves to next field (e.g., "Now your password")
7. Process repeats until form complete

## Supported Element Types

Not just text inputs — the system renders actual form elements in the chat window:

- **Text input** — AI asks for username, password, email, etc.
- **Dropdowns** — rendered as selectable list in chat
- **Radio buttons** — rendered as choice cards
- **Switches/toggles** — rendered as chat-native toggles
- **Date picker** — rendered as calendar widget in chat

Each element appears in the chat in the order defined by the form steps.

## Form Definition Syntax

Forms are described in `.md` files using extended fenced code block syntax — similar to how code snippets use triple backticks + language name:

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

  - type: dropdown
    name: role
    label: "Account Type"
    options: [Artist, Producer, Executive, Fan]
    default: Fan
    prompt: "What best describes you?"
```
````

````markdown
```form:registration
steps:
  - type: text
    name: email
    label: "Email"
    validate: required,email
    prompt: "What's your email?"

  - type: radio
    name: tier
    label: "Subscription Tier"
    options:
      - value: single
        label: "Developer — $49"
      - value: team
        label: "Studio — $149"
      - value: dev
        label: "Dev Edition — $500"
    prompt: "Pick your tier"

  - type: switch
    name: newsletter
    label: "Send me updates"
    default: true
    prompt: "Want our newsletter?"

  - type: date
    name: launch_date
    label: "Project Launch Date"
    prompt: "When does your project drop?"
```
````

## Element Types Reference

| Syntax | Element | Chat Rendering |
|--------|---------|----------------|
| `type: text` | Text input | AI asks, user types response |
| `type: text` + `mask: true` | Password | AI asks, input is masked |
| `type: dropdown` | Select dropdown | Rendered as tappable list in chat |
| `type: radio` | Radio buttons | Rendered as choice cards |
| `type: switch` | Toggle switch | Rendered as chat-native toggle |
| `type: date` | Date picker | Rendered as calendar widget |

## Validation

Validation rules follow a comma-separated syntax in the `validate` field:
- `required` — field cannot be empty
- `min:N` — minimum length/value
- `max:N` — maximum length/value
- `email` — must be valid email format
- `pattern:regex` — custom regex validation

When validation fails, AI re-prompts with specific feedback ("That email doesn't look right, try again").

## Use Cases

- **Login flows** — username → password, validated step by step
- **Registration** — email, tier selection, preferences
- **Checkout** — Stripe payment details, billing address
- **Onboarding** — role selection, project setup wizard
- **NFT minting** — metadata fields for BalladeMix drops
- **Solana wallet** — deposit revenue flow, contributor registration
