---
title: LawnCzar
created: 2026-05-27
updated: 2026-05-27
type: entity
tags: [database, workflow]
sources: [raw/articles/lawnczar-conceptual-notes.md]
confidence: high
contested: false
contradictions: []
---

# LawnCzar

**LawnCzar** (also referenced as **LawnMap**) is a location-based Progressive Web App (PWA) marketplace platform designed to streamline community-based commerce, connecting buyers and sellers for local events such as yard sales, estate sales, moving sales, and food trucks.

* **Production URLs:**
  * 🌐 **React-Based Implementation:** [https://lawnczar.com](https://lawnczar.com)
  * 🎨 **Native Web Components Implementation:** [https://lawnczar.shop](https://lawnczar.shop)
  * Diagnostic Ports:
    * React App Static: `http://<IP_ADDRESS>:8086`
    * Express Backend / Native App: `http://<IP_ADDRESS>:8085`

---

## 🏗️ Core Architecture & Features
LawnCzar represents an integration of decentralized architecture and modern interactive map workflows.

### 1. Interactive Navigation & Shop Mode
* **Circle-to-Select (Lasso Tool):** Shoppers can draw freehand lasso shapes on the map to selectively target active sales in a neighborhood.
* **Tinder-Style Swiping UI:** Once an area is lassoed, matching sales load into a `<swipe-deck>` component. Swiping right keeps a sale in the active itinerary, while swiping left discards it.
* **Optimized Routing:** Renders custom routing paths to generate the most efficient travel plan between selected sales using Leaflet Routing Machine.

### 2. Seller Onboarding & Monetization
* **Onboarding Stepper:** A streamlined, 4-step wizard guides sellers through submitting sale details, uploading item photos, and scheduling dates.
* **Stripe Payments:** Integration for purchasing active markers on the map.
* **QR Signage:** Generation of dynamic QR codes linked to the PWA for physical lawn signage.
* **Live Video Streaming:** Built-in video widgets (e.g., Agora or Daily.co) allow sellers to broadcast live directly within the interactive map marker.

---

## 🔗 Related Initiatives & Evolution
During the conceptual phase, several adjacent technologies and business models were brainstormed:
* **Blockchain & Tokenization:** Explored integration with blockchain technology for transparent data ownership and decentralized hosting.
* **Musician Networks:** Explored secondary ideas such as social networks for musicians (related to [[ballademix]] and [[makeufamous]]).

---

## 💾 Implementation Details
The actual implementation located in `/root/lawnmap` utilizes:
* **Frontend:** Native Web Components (Vanilla HTML5 / Shadow DOM) and CSS Grid.
* **Map Engine:** Leaflet.js for interactive rendering and GPS tracking.
* **Service Worker:** Standalone PWA offline caching.
* **Backend:** Node.js, Express, and MongoDB (`lawnczar` database).
* **Testing Suite:** Vitest with JSDOM runner.
