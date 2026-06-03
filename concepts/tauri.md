---
title: Tauri Framework
created: 2026-05-26
updated: 2026-05-26
type: concept
tags: [workflow, framework]
sources: [neurocanvas_llm_wiki_editor.tsx]
confidence: high
contested: false
contradictions: []
---

# Tauri Framework

**Tauri** is a modern, lightweight, security-first open-source framework for building multi-platform desktop and mobile applications using web frontends (like React, Svelte, or Vue) backed by a high-performance **Rust** system layer.

---

## 🏗️ Architecture & Philosophy

Tauri differs fundamentally from heavier runtime containers (such as Electron) by discarding embedded chromium runtimes and using native webviews:

```
┌─────────────────────────────────────────┐
│              Web Frontend               │
│        (React, Vite, HTML/CSS)          │
└───────────────────┬─────────────────────┘
                    │ (Inter-Process Communication / IPC)
                    ▼
┌─────────────────────────────────────────┐
│              Rust Core                  │
│       (System APIs, File OS, DB)        │
└─────────────────────────────────────────┘
```

1. **Native Webviews:** Instead of packaging a heavy browser engine, Tauri leverages the OS's native web view (Webkit2GTK on Linux, WKWebView on macOS/iOS, and WebView2 on Windows/Android). This shrinks bundle sizes down from ~100MB to less than 10MB.
2. **Rust Backend:** System operations, secure encryption, database bindings, and heavy computations are handled safely in Rust.
3. **Security Sandboxing:** IPC (Inter-Process Communication) and file system access are locked down by default. Access to OS resources must be explicitly configured using fine-grained capability scopes.

---

## 📱 Tauri v2 (Mobile & Plugins)

**Tauri v2** expands platform support to mobile environments (Android and iOS) using a standardized **plugin architecture**:
- **Unified Plugins:** Plugins (such as file system, store, secure-storage, and notification) share a single API boundary that spans both desktop and mobile runtimes.
- **Client-Server Synergy:** Enables local client apps (like [[neurocanvas|NeuroCanvas]]) to operate completely offline while securely bridging browser-based React components to the local storage, device sensors, and native file systems. This provides an offline-first foundation for custom [[pkm|Personal Knowledge Management (PKM)]] nodes and interactive [[llm-wiki-pattern|LLM Wikis]].
