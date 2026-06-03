---
title: Savage Dad Style Guide
created: 2026-05-25
updated: 2026-05-25
type: concept
tags: [knowledge-base, wiki-pattern, methodology]
sources: [raw/articles/savage-dad-style-guide.md]
confidence: high
contested: false
contradictions: []
---

# Savage Dad Style Guide

The **Savage Dad Style Guide** defines the visual, verbal, and component-level guidelines for the "Savage Dad" Progressive Web Application (PWA). Rejecting standard corporate design systems, the guide outlines a highly unique **Material Design 3 (M3)** override system optimized for an urban, high-contrast, black-theme aesthetic representing Generation X hip-hop culture, family protection, and tech prepping.

---

## 🎙️ Brand Persona & Verbal Identity

Savage Dad’s communication relies on three core pillars that direct all written copy, marketing, and transactional templates:

1. **Street Authenticity:** Rooted in the inner-city streets of Hip Hop America. Tone is direct, unapologetic, and firm—strictly avoiding corporate jargon.
2. **Renaissance Man:** Gen X survivor, sneakerhead, and tech prepper. Speaks with a witty, ahead-of-the-curve authority.
3. **Protective Patriarch:** Rooted in family values and faith. Tone is mentoring, trustworthy, and protective, ensuring users feel respected and secure.

### Messaging Application Examples
* **CTA Buttons:** commanding and urgent (*"SECURE THE DROP," "MAKE IT YOURS"*).
* **Validation Errors:** relatable and correcting (*"Whoa, check that email again, pops."*).
* **Success Prompts:** confident acknowledgment (*"Secured. That's going straight to the cart."*).

---

## 🎨 Visual Identity & Material 3 Overrides

The design system overrides standard Material 3 color and typography defaults to construct a cohesive "Street Wear Black" environment.

```
       ┌────────────────────────────────────────────────────────┐
       │             Savage Dad M3 Dark Theme                   │
       └───────────────────────────┬────────────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ Background       │     │ Primary          │     │ Action/CTA       │
│ Street Wear Black│     │ Sunburn Orange   │     │ Reflective Silver│
│ (#1F1B16)        │     │ (#FFB683)        │     │ (#FFFFFF)        │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

### 1. Typography Pairings
To maximize impact, Savage Dad pairs an aggressive, display-heavy heading font with a modern, clean reading font:
* **Headings (H1, H2, H3):** *Bangers* (or Graffiti/BMX styles)—aggressive, raw, and high-energy. Used sparingly for headers, prices, and high-priority action banners.
* **Body & UI Elements:** *Roboto*—clean, highly legible, and modern. Used for functional body copy, inputs, forms, and product specs.

### 2. Mood & Imagery Guidelines
* **Photography Vibe:** High-contrast, desaturated, and moody street photography featuring deep shadows and strong directional light. Models should look confident and determined inside authentic inner-city environments.
* **Product Shoots:** Set on clean charcoal or deep-black backdrops to keep product apparel as the focal point while maintaining the dark theme.

---

## 🛠️ PWA Component Blueprint (Material 3)

Material 3 components are customized using the brand's unique color tokens to ensure responsive, accessible (WCAG compliant) layouts:

* **Primary Action Buttons:** Uses M3 Filled buttons with a bold, all-caps Roboto font in **Reflective Silver (`#FFFFFF`)** on a **Sunburn Orange (`#FFB683`)** active background.
* **Secondary Actions / Add-to-Cart:** Uses M3 Outlined buttons utilizing a Sunburn Orange stroke and text.
* **Product Cards:** M3 elevated surface containers styled on a **Surface Background (`#2B2723`)** where product headings use the *Bangers* typeface.
* **Input Text Fields:** Uses M3 Filled Text Field styling. When focused, the input line changes to the **Earthy Tan (`#DBC0A3`)** secondary color.
* **Toasts & Alerts:** Uses the M3 Snackbar component. Successful actions render with a **Muted Olive (`#A8D773`)** background, while failures render on **Crimson Red (`#FFB4AB`)**.

---

## 🔗 Ecosystem & Agent Coordination

The Savage Dad Style Guide coordinates directly with other major elements of your agentic enterprise:

### 1. Linguistic Personas in AIEOS
Savage Dad’s verbal guidelines can be coded as a specific **[[aieos-integration|AIEOS-compliant linguistic profile]]**. Defining parameters like the speaker's idiolect (Gen X, urban slang, prepper keywords) allows customer service agents or voice-assistant bots to communicate with users using the consistent brand voice across SMS, Telegram, or phone platforms.

### 2. Development via Paperclip AI
Building the Savage Dad e-commerce PWA is a collaborative task for **[[paperclip-agent-roster|Paperclip Agent Teams]]**:
* **`UX Designer`:** Translates the desaturated high-contrast style rules into standard Figma/Tailwind design tokens.
* **`Coder`:** Packages the Material 3 React/Tailwind elements and ensures the service workers are set up for offline PWA installation.
* **`QA`:** Runs accessibility color checks to ensure that Sunburn Orange text passes contrast minimums against Street Wear Black.
* **`Security Engineer`:** Hardens payment form integrations and prepper email pre-registration sheets.

### 3. Contrast to Peer Visual Designs
Savage Dad’s heavy, aggressive style contrasts beautifully against **[[makeufamous|MakeUFamo.us]]**, which uses a neon purple-and-pink aesthetic. This highlights the flexibility of the Material 3 override model across diverse business concepts in your registry.
