---
title: Grok — Trinity-Weave context
created: 2026-06-09
tags: [grok, trinity-weave, weave]
---

# Grok — Trinity-Weave context

Attach **[L0RDTH0TH/Trinity-Weave](https://github.com/L0RDTH0TH/Trinity-Weave)** branch **`main`** for weave architecture questions.

## Start here (in repo)

1. **`GROK-START-HERE.md`** (repo root)
2. **`OBSERVABILITY.json`** — card ids, paths, `last_publish_utc`, question routing
3. **`weave/CARD-INDEX.md`** — human-readable card catalog
4. **`Docs/GROK-OBSERVABILITY.md`** — what you can/cannot observe

## Question routing

| Question type | Primary repo | Branch |
|---------------|--------------|--------|
| Weave design, maintenance grammar, meta cards, host-weld | **Trinity-Weave** | `main` |
| Queue behavior, `.cursor/` agents, EAT-QUEUE ops | `genesis-mythos-master-roadmap` | `iteration-2-roadmap-rules` |
| GMM roadmap / game execution narrative | `genesis-mythos-master-roadmap` | `godot-genesis-mythos-master` (etc.) |
| Live runtime (Watcher, queue depth) | **None** — paste or committed telemetry only |

## Hard boundary

Grok has **no live vault access**. Ground answers in **committed** Trinity-Weave files only. Cite `OBSERVABILITY.json` → `last_publish_utc` when staleness matters.

## Key paths

| Path | Contents |
|------|----------|
| `OBSERVABILITY.json` | Machine index for Grok |
| `weave/components/<id>.yaml` | Locked Trinity cards |
| `weave/host-weld/live/safety.md` | Execution safety digest |
| `Docs/ARCHITECTURE-OVERVIEW.md` | Plain-language system map |
| `Docs/GLOSSARY-FOR-EXTERNAL-READERS.md` | Jargon decoder |

## Not in Trinity-Weave

Project files (`1-Projects/`, `Roadmap/` from factories) are **intentionally excluded**. Switch to engine branch on `genesis-mythos-master-roadmap` for GMM phase notes.
