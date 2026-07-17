---
title: Weave Core Manifest (public slice)
created: 2026-06-09
updated: 2026-07-17
tags: [weave, trinity-weave, grok]
---

# Weave Core Manifest

**Public repo:** [L0RDTH0TH/Trinity-Weave](https://github.com/L0RDTH0TH/Trinity-Weave)  
**Authority:** locked meta `trinity_weave_public_export` + `public_surface_topology`  
**Purpose:** Weave maintenance architecture — filled meta, provisional gates, harness, host-weld.

## Grok observability (auto-generated each sync)

| Artifact | Path | Purpose |
|----------|------|---------|
| Start here | `GROK-START-HERE.md` | Read order + routing |
| Machine index | `OBSERVABILITY.json` | Card ids, paths, last publish, routing |
| Card catalog | `weave/CARD-INDEX.md` | Tiered table of shipped cards |
| Architecture | `Docs/ARCHITECTURE-OVERVIEW.md` | System map |
| Glossary | `Docs/GLOSSARY-FOR-EXTERNAL-READERS.md` | Jargon decoder |
| Meat suit entry | `meat-suit-entry/README.md` | Bone pilot hub |

## Shipped layers

| Layer | Export path | Notes |
|-------|-------------|-------|
| Weave Python | `scripts/eat_queue_core/weave/` | Maintenance spine |
| Schedule plane | `scripts/eat_queue_core/schedule_*.py`, `pseudo_clock.py` | Background rhythm |
| Locked meta YAML | `weave/components/*.yaml` | Doctrine cards |
| Provisional YAML | `weave/component-proposals/*.yaml` | Active law; may evolve |
| Registry | `weave/trinity-partition-registry.yaml` | Maintenance partition ids |
| Host weld law | `weave/host-weld/live/`, `manifest.yaml` | Compiled execution gates |
| Bridge socket | `Docs/Rules/host-weld-bridge.mdc` | Host adapter reference |
| Design docs | `Docs/*` | Architecture + bridge contracts |

## Locked meta ids (illustrative)

See `OBSERVABILITY.json` → `meta_card_ids` for the live list. Includes (among others):

- `trinity_prompt_context`
- `harness_runtime_contract`
- `schedule_event_planes`
- `cursor_host_adapter`
- `host_execution_safety_contract`
- `public_surface_topology`
- `trinity_weave_public_export`

## Forbidden on `main`

Project **instances** (`Roadmap/` trees, factory output paths), live queues, resolve maps. Gate **cards** that define mint/execution grammar ship on `main` (locked or provisional).

## Publish harness

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness weave_public_sync --vault-root .
```

Schedule tick may run change-gated sync when allowlisted fingerprints move.
