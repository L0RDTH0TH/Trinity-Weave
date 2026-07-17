---
title: Grok Project Bridge
created: 2026-07-17
audience: grok_github_integration
---

# Grok Project Bridge

Three-tier Cursor ↔ Grok bridge on **Trinity-Weave** only.

## Tiers

| Tier | Surface | Contents |
|------|---------|----------|
| A | `main` | Weave law: locked + **provisional** cards, harness, indexes |
| B | `project/<id>` | Project instances: Roadmap, catalog, observability |
| C | Mediated fulfill | Tertiary vault pointers → Cursor gate → pack paste |

## Routing

- **Weave / gates / cards** → `main` (`weave/components/`, `weave/component-proposals/`)
- **Project mint / execution** → `project/godot-genesis-mythos-master` (branch root)
- **Tertiary bodies** → never on GitHub; request by `tert_*` id via fulfill broker

## Harness

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness project_bridge_sync --vault-root . --project-id godot-genesis-mythos-master
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness project_bridge_push --vault-root . --branch project/godot-genesis-mythos-master
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness grok_bridge_status --vault-root .
```

## Hard boundary (Grok)

*I have no direct local vault access — all content comes via published branches or mediated fulfill packs.*

## Provisional cards

1. *Provisional cards are active system law but may evolve — cite tier when advising.*
2. *When a provisional card is referenced, note its tier and cross-check against locked equivalents or operator intent if advising on implementation.*

## Example fulfill request

```yaml
grok_fulfill_request:
  request_id: "20260717-godot-001"
  project_id: godot-genesis-mythos-master
  project_branch: project/godot-genesis-mythos-master
  purpose: "Clarify catalog row ui_presentation_shell L5 scope for mint review"
  node_ids: ["tert_a1b2c3", "catalog:ui_presentation_shell"]
  need: summary
  max_chars: 2000
```

## Push economy

- Grok remote = Trinity-Weave only (`main` first, then `project/*`)
- Curator = private backup (separate cadence)
- gmmr = vestigial for this bridge

Status: [[3-Resources/Second-Brain/Docs/Grok-Bridge-Status|Grok-Bridge-Status]]
