---
title: Grok — start here (Trinity-Weave)
created: 2026-06-09
updated: 2026-07-17
audience: grok_github_integration
---

# Grok — start here

**Repo:** [L0RDTH0TH/Trinity-Weave](https://github.com/L0RDTH0TH/Trinity-Weave)  
**Branch:** `main` (weave law) · `project/<id>` (project instances)  
**Purpose:** Committed **weave maintenance architecture** — YAML cards, harness, host-weld law.

## What this repo is

Trinity-Weave is the **public design manual + code slice** for an agentic Second Brain maintenance layer:

- YAML **cards** describe components (intent, code touchpoints, rules, proofs)
- Python **harness** aligns and operates that grammar
- **Schedule tick** keeps published indexes fresh

You see **committed git only**. You do not see live local workspaces unless the bone pilot pastes a fulfill pack.

## Read order (5 minutes)

1. **`OBSERVABILITY.json`** — machine index: card ids, paths, routing, last publish
2. **`Docs/ARCHITECTURE-OVERVIEW.md`** — system map
3. **`weave/CARD-INDEX.md`** — every shipped card id + tier + one-line role
4. **`Docs/GLOSSARY-FOR-EXTERNAL-READERS.md`** — jargon → plain English
5. **`weave/components/trinity_prompt_context.yaml`** — how cards compose for prompts

## Question routing

| If the question is about… | Read |
|---------------------------|------|
| Weave design, meta cards, self-wrap, schedule, host-weld, gate cards | **`main`** — `weave/components/`, `weave/component-proposals/` |
| Project instances, catalog rows, execution Roadmap | **`project/<id>`** branch root (`GROK-PROJECT-START.md`) |
| Tertiary note bodies (`tert_*`) | Mediated **fulfill pack** — request; do not invent |
| Live queue / Watcher / unpublished edits | **Unavailable** — say so; ask for paste |

## Hard limits

- No live vault, MCP, or Watcher access
- Provisional cards are **active law** but may evolve — cite tier (`locked` \| `provisional`)
- `[[wiki-links]]` in YAML are Obsidian paths — map to `weave/components/<id>.yaml` or `weave/component-proposals/<id>.yaml`

## Key paths

| Path | Contents |
|------|----------|
| `weave/components/*.yaml` | Locked Trinity cards |
| `weave/component-proposals/*.yaml` | Provisional cards (active; may evolve) |
| `weave/trinity-partition-registry.yaml` | Maintenance core id registry |
| `weave/host-weld/live/safety.md` | Execution safety digest |
| `scripts/eat_queue_core/harness.py` | CLI entry |
| `Docs/Maintenance-Trinity-Constitution.md` | Dual-lock / corps charter |
| `Docs/GROK-PROJECT-BRIDGE.md` | Three-tier bridge contract |
| `meat-suit-entry/` | Bone pilot orientation |

## Test engagement

Ask for a **card id**, a **harness command**, or a **scenario**. Ground answers in matching YAML + constitution.
