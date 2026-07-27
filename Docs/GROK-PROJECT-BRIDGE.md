---
title: Grok Project Bridge
created: 2026-07-17
audience: grok_github_integration
---

# Grok Project Bridge

Three-tier Cursor ↔ Grok bridge on **Trinity-Weave**.

## Tiers

| Tier | Surface | Contents |
|------|---------|----------|
| A | `main` | Weave law: locked + **provisional** cards, harness, indexes |
| B | `project/<id>` | Project instances: Roadmap, catalog, observability |
| C | Mediated fulfill | Tertiary pointers → security gate → bone-pilot ack → pack paste |

## Routing

- **Weave / gates / cards** → `main` (`weave/components/`, `weave/component-proposals/`)
- **Project mint / execution** → `project/genesis-mythos-master` (branch root)
- **Tertiary bodies** → never on GitHub; request by `tert_*` id via fulfill broker

## Hard boundary (Grok)

*I have no direct local vault access — all content comes via published branches or mediated fulfill packs.*

## Provisional cards

1. *Provisional cards are active system law but may evolve — cite tier when advising.*
2. *When a provisional card is referenced, note its tier and cross-check against locked equivalents or operator intent if advising on implementation.*

## Catalog mint (what Grok actually uses)

GitHub connector ≈ **`main` only** (no branch picker).

1. **Instruction law:** `weave/component-proposals/catalog_mint.yaml` (Trinity card)
2. **Per-project pack:** `Docs/catalog-mint/<project_id>/`  
   (`PACK-MANIFEST.yaml`, conceptual + pins + tech stack excerpts, `slice-catalog.yaml`, **`Actual-Play-Feedstock/`** moment cards)
3. **Active pointer:** `Docs/catalog-mint/ACTIVE.md`

**Actual-play moment cards** must live under the pack on **`main`** (`Docs/catalog-mint/<id>/Actual-Play-Feedstock/`).  
Vault path `1-Projects/.../Actual-Play-Feedstock/` and Trinity `project/<id>` are **not** visible to the Grok connector.

Emit / refresh packs (Cursor/operator):

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness catalog_mint_pack_emit --vault-root . --project-id <id>
```

Bone pilot **names `project_id` in the mint cue** — Grok does not discover it from branches or ACTIVE.md.

Project branch `project/<id>` remains Cursor/export instance — not something the bone pilot configures inside Grok.

## Example fulfill request

```yaml
grok_fulfill_request:
  request_id: "20260717-gmm-001"
  project_id: genesis-mythos-master
  project_branch: project/genesis-mythos-master
  purpose: "Clarify a conceptual_pin Roadmap note for the current single-row mint candidate"
  node_ids: ["tert_a1b2c3"]
  need: summary
  max_chars: 2000
```

## Push economy

- Remote for Grok = this repo only (`main` first, then `project/*`)
- Local sync may succeed while remote push waits on budget — cite `Docs/Grok-Bridge-Status.json` → `recommendation`

## Harness (operator workspace)

```bash
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness project_bridge_sync --vault-root . --project-id genesis-mythos-master
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness project_bridge_push --vault-root . --branch project/genesis-mythos-master
PYTHONPATH=scripts python3 -m scripts.eat_queue_core.harness grok_bridge_status --vault-root .
```
