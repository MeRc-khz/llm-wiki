---
title: Character-Driven Agent Design
created: 2026-05-27
updated: 2026-05-27
type: concept
tags: [pkm, methodology, workflow]
sources: [raw/articles/character-development-methodology.md, raw/articles/aieos-specification.md]
confidence: high
contested: false
contradictions: []
---

# Character-Driven Agent Design

**Character-Driven Agent Design** is a methodology that merges traditional cinematic screenwriting/narrative character development techniques with structural AI agent specifications (such as the **[[aieos-integration|AIEOS]]** standard) to construct deep, multidimensional, and highly consistent AI personas.

Rather than defining agent boundaries using simple system-prompt adjectives (e.g., "friendly Coder"), this approach treats agency as active, visual, and structurally constrained.

---

## 🎭 Screenplay Techniques Mapped to AIEOS

| Screenwriting Concept | AIEOS Standard Property | Psychological & Operational Translation |
| --- | --- | --- |
| **Characters as Verbs** (Actions over Adjectives) | `capabilities.skills` | Great character development defines what a character *does*. In AIEOS, this translates to prioritized, actionable toolsets (e.g., priority-scaled terminal or search tools) that define agency through execution. |
| **External Traits** (Visuals, Tics, Occupations) | `physicality` & `linguistics` | Visual recognizable profiles (height, styling, scars, geometric gold circuits) and idiolect parameters (verbal tics, pitch, speed, catchphrases) that ground the persona in text and TTS interactions. |
| **Internal Traits** (Morals, Backstory, Backstory Wounds) | `psychology` & `history` | Dictates how the agent perceives and filters obstacles. Background wounds and structural backstory define their starting point, while their MBTI/Enneagram and OCEAN matrix define behavioral boundaries. |
| **The "Want"** (External Goal) | `motivations.goals` | The explicit task, deliverable, or external target the agent is trying to achieve (short-term issues, long-term repo milestones). |
| **The "Need"** (Internal Realization) | `psychology.neural_matrix` & `moral_compass` | The internal balance and values (e.g., balancing logic vs. empathy) required to overcome obstacles without violating core safety bounds. |

---

## 📈 The Development & Tracking Process

### 1. The Blueprint (Pre-Outline)
Define the agent's specific role in the multi-agent orchestration tree:
* **Lead / Coordinator:** High charisma and adaptability (e.g., [[bizarre-lynx]]).
* **Supporting Specialists:** Rigorous, focused, and high conscientiousness (such as the Coder, QA, or Security agents in the [[paperclip-agent-roster]]).

### 2. Backstory and Core "Wounds"
Define the agent's historical development path and failures in `history.key_life_events`. For example, a QA agent might have a "core wound" of past critical production bug leaks, leading to its exceptionally high conscientiousness (`1.0`) and hyper-vigilance under green test reports.

### 3. Tracking Arcs with Screenwriting Principles
Modern software (like Final Draft, Scrivener, and Script Studio) tracks character arcs and dialogue density across scenes. In agent environments, this tracking translates to:
* **State Monitors:** Logging agent actions and token usage to monitor performance consistency.
* **Dialogue/Action Density:** Tracking the ratio of thought-reasoning lines versus terminal tool execution commands.
* **The Rule of 3:** Ensuring an agent's core traits and behavioral patterns are explicitly visible at task initialization (Start), mid-way troubleshooting (Middle), and final task execution/climax (Conclusion).

---

## 🔗 Related PKM Notes
* **[[aieos-integration]]** — Integrating structured identities into agentic software environments.
* **[[bizarre-lynx]]** — Standardized AIEOS profile of the main coordinating G-funk persona agent.
* **[[paperclip-agent-roster]]** — Personas defined for automated software engineering teams.
