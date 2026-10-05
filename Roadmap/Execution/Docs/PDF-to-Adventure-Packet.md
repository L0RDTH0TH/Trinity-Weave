---
title: PDF → Adventure Packet (Execution pointer) — genesis-mythos-master
created: 2026-09-30
updated: 2026-10-01
tags: [execution, cartridge, half-b, genesis-mythos-master]
para-type: Project
project-id: genesis-mythos-master
roadmap_track: execution
status: active
factory_greenlit: false
---

# PDF → Adventure Packet

**Law:** [[Half-B-Alpha-Mode]] — gate `pdf_to_adventure_packet` when cartridge work is in scope. **Not** live Success via archived `horizon_demo_investor` (see `4-Archives/Projects/genesis-mythos-master/horizon-demo-investor-ask-retired-20261001T072552Z/`). `factory_greenlit: false`. This note is a **touch pointer**, not a converter harness.

## Path

1. **Source PDF (exemplar):** `Ingest/PZO9500-9E_WeBeGoblinsFree.pdf`
2. **Derive** structured adventure packet under operator IP rules (no Paizo prose dump into game tree).
3. **Land** under `5-Attachments/Code-Repos/genesis-mythos-alpha/genesis-mythos/content/packs/<id>/`

## Pack schema (current shape)

| File | Role |
|------|------|
| `pack.json` | Stable id, honesty banner, `release_stage` |
| `beats.json` | Session beats |
| `sites.json` | Sites / places |
| `pregens.json` | Pregen PCs |

Placeholder `example_goblin_oneshot` = empty-shape feedstock until PDF-derived packet exists — **not** Success ceiling.

## Related

- Trinity `implementation_gate_catalog` — `pdf_to_adventure_packet` (leaf when in scope)
- [[Half-B-Alpha-0-Implementation-Receipt]] — staging receipt honesty
- Archived investor ask — not active Success
