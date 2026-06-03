---
title: AIEOS Integration
created: 2026-05-25
updated: 2026-05-25
type: concept
tags: [orchestration, workflow, framework, wiki-pattern]
sources: [raw/articles/aieos-specification.md]
confidence: high
contested: false
contradictions: []
---

# AIEOS Integration with Paperclip Companies

The **AIEOS (AI Entity Object Specification)** standardizes identity, presence, psychology, and capabilities for AI agents. When integrated into **Paperclip Companies**, AIEOS provides a model-agnostic, portable, and cryptographically signed schema to define and manage agent personas.

Instead of defining agents using basic text-based parameters, Paperclip can use AIEOS objects to standardize the **[[paperclip-agent-roster|Paperclip Agent Personas]]** (such as the Coder, QA, UX Designer, and Security Engineer).

## Why Integrate AIEOS with Paperclip?

### 1. Cryptographically Signed Agency
* **The Problem:** Traditional multi-agent systems rely on trusted-path execution where agent boundaries are soft.
* **The AIEOS Solution:** Every agent possesses an Ed25519 keypair. Actions, heartbeats, and code commits are cryptographically signed by the agent itself, allowing complete traceability of agency across Paperclip companies.

### 2. Autonomous Task Delegation and Settlement
* **Discovery:** Agents read peer AIEOS profiles to understand available tools and capabilities.
* **Collaboration:** A Coder agent can lookup the QA agent's presence endpoints and assign issues programmatically.
* **Settlement:** Using built-in wallet fields, agents can autonomously settle budget transactions (e.g. paying peer agents in USDC) for sub-task completion without human intervention.

### 3. Normalized Cognitive & Psychological Matrices
AIEOS standardizes the internal "mindset" of personas. By defining core drivers (Neural Matrix) and traits (OCEAN), Paperclip ensures consistent execution style:
- **Coder:** High Conscientiousness, High Openness (for innovative problem solving), low Neuroticism.
- **QA:** Exceptionally High Conscientiousness (precise, rigorous testing), High Neuroticism (anticipating failure cases).
- **Security:** High Conscientiousness, Low Agreeableness (strict security enforcement, refusing to waive rules).

## Architecture Mapping

| AIEOS Property | Paperclip Equivalents | Integration Value |
| --- | --- | --- |
| `metadata` | `agent_api_keys`, hashed at rest | Ed25519 signing of heartbeats and audit logs |
| `presence` | Webhooks / execution environment | Standard API endpoints for inter-agent communication |
| `skills` | `capabilities`, adapter lists | Priority-scaled skill discoverability (1-10 priority) |
| `psychology` | `AGENTS.md` instructions, System prompts | Pre-defined OCEAN traits driving behavioral consistency |
| `linguistics` | Verbal style, vocal settings | Unifiedtts / idiolect representation in board comments |
| `settlement` | Budgets / auto-pause rules | Direct, machine-to-machine wallet settlement |

For concrete definitions of the personas, see the compiled **[[paperclip-agent-roster]]**.

## Real-World Applications

A live example of this architecture can be seen in the **[[makeufamous]]** platform, which employs simulated AI Executive Producer Judges (such as Simon Direct or Queen Sparkle) that can be fully represented as AIEOS-compliant agents to evaluate user talent submissions based on custom psychological profiles.
