---
title: NeuroCanvas Wiki Editor
created: 2026-05-26
updated: 2026-05-26
type: entity
tags: [agentic, workflow, pkm, knowledge-base]
sources: [neurocanvas_llm_wiki_editor.tsx]
confidence: high
contested: false
contradictions: []
---

# NeuroCanvas Wiki Editor

**NeuroCanvas Wiki Editor** is an interactive, canvas-based wiki editor and multi-dimensional page layout system that serves as a client-server local app. Built with **React, TypeScript, Tailwind CSS**, and packaged using **[[tauri|Tauri v2]]**, the tool combines visual element positioning, multi-media asset linking, and a fully interactive **3D Force-Directed Node Graph** to create a spatial editing experience.

---

## 🏗️ Core Features & Architecture

NeuroCanvas is structured as a client-side single-page spatial canvas backed by local native OS system bridges:

```
┌──────────────────────────────────────────────────────────────┐
│                  NeuroCanvas React Frontend                  │
│   ┌────────────────────┐            ┌────────────────────┐   │
│   │  Spatial Canvas    │            │ 3D Force-Directed  │   │
│   │  (Drag & Position) │            │ Graph Canvas       │   │
│   └─────────┬──────────┘            └─────────┬──────────┘   │
└─────────────┼─────────────────────────────────┼──────────────┘
              ▼                                 ▼
┌──────────────────────────────────────────────────────────────┐
│                       Tauri v2 Bridge                        │
│   ┌────────────────────┐            ┌────────────────────┐   │
│   │ Native File System │            │ Local Persist      │   │
│   │ (Save/Load CIDs)   │            │ (Sqlite/KV Store)  │   │
│   └────────────────────┘            └────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

### 1. 3D Force-Directed Node Graph (`Graph3D`)
- **Physics Engine:** Custom 3D gravity and link-spring simulation executing in real-time on an HTML5 canvas.
- **Interactions:** Supports rotation via dragging, hover states for nodes, and clicking nodes to trigger instant viewport navigation.
- **Dynamic Link Resolution:** Inspects the active elements of all pages and dynamically renders linking lines between pages when text elements contain internal wiki links.

### 2. Spatial Element Sandbox
Users drag, drop, position, and resize multiple element types on an open spatial sandbox:
- **Text Blocks:** Supports customizable typography, sizing, colors, weights, and inter-page hyperlinking.
- **Media (Images & Video):** Supports image/video uploading and absolute positioning with dynamic CSS filters (Saturate, Brightness, Contrast, Sepia, Hue Rotate) editable on canvas.
- **Folders:** Group-able visual files.
- **HTML Compilation:** Features an automated compiler (`exportHTML`) that serializes the canvas elements into a single-page interactive static build.

---

## 🚀 Local Deployment and Serving

NeuroCanvas is fully configured and compiled as a web service and a local desktop/mobile package:
* **Frontend Web Service:** Built using Vite + React and served locally via Nginx at **`http://localhost:8090`**.
* **Tauri v2 Desktop App:** Located under `/root/neurocanvas`, compiling directly to desktop executables.
* **Tauri v2 Mobile Target:** Android and iOS setups are initialized and ready for deployment.

---

## 📎 Paperclip AI Task Pipeline (Collaborative Development)

To run a development cycle through the **[[paperclip-agent-roster|Paperclip AI Agent Team]]**, the following task roadmap has been established:

### Task 1: Native Local Save Bridge (Coder & Security Engineer)
- **Goal:** Connect the browser-based `exportHTML` trigger to write compiled wiki outputs directly to the local disk using Tauri v2's native File System plugin (`@tauri-apps/plugin-fs`).
- **Security Check:** Security Engineer audits the tauri capability scopes inside `src-tauri/capabilities/default.json` to ensure directory write access is restricted only to safe user paths.

### Task 2: Spatial Layout Mobile Optimization (UX Designer)
- **Goal:** Audit Tailwind styles in `App.tsx` to handle pinch-to-zoom gestures and canvas navigation on mobile targets (Tauri Android/iOS).
- **Design Rule:** Visual elements must use percentage-based boundaries or auto-scaling viewports on small screens.

### Task 3: State Persistence & E2E Validation (QA)
- **Goal:** Set up local state persistence using the browser's IndexedDB or `@tauri-apps/plugin-store` to prevent data loss on app restarts. Write a test suite to mock node dragging and save triggers.
