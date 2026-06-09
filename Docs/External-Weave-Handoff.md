---
title: External Weave Handoff (draft — light slice)
created: 2026-06-09
tags: [weave, phase-18, trinity-weave]
status: draft
---

# External Weave Handoff (draft)

**Status:** Draft light slice shipped to [Trinity-Weave](https://github.com/L0RDTH0TH/Trinity-Weave). Full Phase 18 adopter handoff remains gated on paces run (see maintenance trinity plan § Phase 18).

## Weave Core (light)

This export is **filled meta + weave harness**, not an empty skeleton:

| Layer | Adopter receives | Adopter mutates |
|-------|------------------|-----------------|
| Harness + weave Python | `scripts/eat_queue_core/weave/`, schedule plane | Config knobs; host adapter |
| Locked maintenance_core meta | `weave/components/*.yaml` | `--operator-mutation` + re-lock |
| Host law | `weave/host-weld/live/` | Extend via host-weld pattern |
| Their factories | — | Adopter-authored (not in this repo) |

## Mutation tiers

1. **maintenance_core** — read-only for automation; operator ack + `--operator-mutation` to edit
2. **conceptual_spine** — consumable locked doctrine
3. **provisional** — not shipped in Trinity-Weave public slice

## First wrap (deferred)

Full first-wrap runbook for non–Second-Brain adopters ships after Phase 18 paces gate. This repo is sufficient for **reading** the maintenance grammar.

## Reference deployment

Second Brain (private vault) is the reference deployment — Curator, institute lane, Obsidian MCP, GMM factories. None of that runtime ships here.
