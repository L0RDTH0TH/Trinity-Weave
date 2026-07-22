---
title: Grok — Trinity-Weave context
created: 2026-06-09
updated: 2026-07-17
tags: [grok, trinity-weave, weave]
---

# Grok — Trinity-Weave context

Attach **[L0RDTH0TH/Trinity-Weave](https://github.com/L0RDTH0TH/Trinity-Weave)** for weave architecture questions.

## Start here

1. **`GROK-START-HERE.md`** (repo root) — includes **STOP** box for catalog mint / GMM
2. **`OBSERVABILITY.json`** — card ids, paths, `last_publish_utc`, question routing
3. **`weave/CARD-INDEX.md`** — **weave card** catalog (`locked` \| `provisional`) — **not** product mint
4. **`Docs/GROK-OBSERVABILITY.md`** — what you can/cannot observe
5. **`Docs/GROK-PROJECT-BRIDGE.md`** — three-tier bridge (`main` / `project/<id>` / fulfill)

## Question routing

| Question type | Branch / surface |
|---------------|------------------|
| **Mint the catalog / product deliverable rows** | **`main`** → `weave/component-proposals/catalog_mint.yaml` + `Docs/catalog-mint/<project_id>/` |
| Weave design, maintenance grammar, meta cards, host-weld, gate cards | **`main`** |
| Other project instances (Roadmap, catalog, observability) | **`project/<id>`** (Cursor/export — not Grok mint feedstock) |
| Tertiary bodies (`tert_*`) | Mediated fulfill pack |
| Live runtime (queues, Watcher) | **None** — paste only |

## Hard boundary

Grok has **no live workspace access**. Ground answers in **committed** Trinity-Weave files. Cite `OBSERVABILITY.json` → `last_publish_utc` when staleness matters.

## Key paths

| Path | Contents |
|------|----------|
| `OBSERVABILITY.json` | Machine index |
| `weave/components/<id>.yaml` | Locked cards |
| `weave/component-proposals/<id>.yaml` | Provisional cards |
| `weave/host-weld/live/safety.md` | Execution safety digest |
| `Docs/ARCHITECTURE-OVERVIEW.md` | System map |
| `meat-suit-entry/` | Bone pilot entry |
