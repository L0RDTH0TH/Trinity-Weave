---
title: Grok — start here (Trinity-Weave)
created: 2026-06-09
audience: grok_github_integration
---

# Grok — start here

**Repo:** [L0RDTH0TH/Trinity-Weave](https://github.com/L0RDTH0TH/Trinity-Weave)  
**Branch:** `main`  
**Purpose:** Committed **weave maintenance grammar** for this operator's Second Brain — not live runtime, not game code, not project Roadmaps.

## What problem this repo solves (plain language)

The operator runs a large Obsidian vault with automated **prompt queues**, **maintenance harnesses**, and **LLM agent pipelines**. Trinity-Weave is the **public design manual + code slice** for how that maintenance layer works: YAML "cards" describe components, Python harness scripts enforce alignment, and a schedule tick keeps exports synced.

You cannot see the private vault. You **can** reason about weave design from files here.

## Read order (5 minutes)

1. **`OBSERVABILITY.json`** (repo root) — machine index: card ids, paths, routing, last publish
2. **`Docs/ARCHITECTURE-OVERVIEW.md`** — system map without vault lore
3. **`weave/CARD-INDEX.md`** — every shipped card id + one-line role
4. **`Docs/GLOSSARY-FOR-EXTERNAL-READERS.md`** — jargon → plain English
5. **`weave/components/trinity_prompt_context.yaml`** — how cards compose for prompts

## Question routing

| If the user asks about… | Read here first | Elsewhere |
|-------------------------|-----------------|-----------|
| Weave design, meta cards, self-wrap, schedule planes | **This repo** | — |
| Queue dispatch, `.cursor/` agents, EAT-QUEUE rules | `genesis-mythos-master-roadmap` / `iteration-2-roadmap-rules` | Not in Trinity-Weave |
| GMM game / phase roadmap narrative | `genesis-mythos-master-roadmap` engine branches | Not in Trinity-Weave |
| Live queue depth, Watcher, current lane state | **Unavailable** — say so; ask user to paste | Private vault only |

## Hard limits (say these out loud)

- No live vault, MCP, or Watcher access
- `[[wiki-links]]` in YAML/docs are Obsidian paths — map `weave/components/<id>.yaml` for card `id`
- Factory output (`1-Projects/`, `Roadmap/`) is **intentionally excluded**

## Key paths

| Path | Contents |
|------|----------|
| `weave/components/*.yaml` | Locked Trinity cards (conceptual + touch + rules + contract) |
| `weave/trinity-partition-registry.yaml` | Maintenance core id registry |
| `weave/host-weld/live/safety.md` | Execution safety digest |
| `scripts/eat_queue_core/weave/` | Maintenance Python |
| `scripts/eat_queue_core/harness.py` | CLI entry (many subcommands) |
| `Docs/Maintenance-Trinity-Constitution.md` | Dual-lock / corps charter |

## Test engagement

Ask the user for a **card id** (e.g. `schedule_event_planes`), a **harness command** (e.g. `trinity_weave_self_wrap`), or a **scenario** (e.g. "provisional card went red on conduct"). Ground answers in the matching YAML + constitution sections.
