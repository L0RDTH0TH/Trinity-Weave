---
title: CDR — Layer decoupling as four named runtime layers
created: 2026-06-26
tags: [conceptual-decision-record, roadmap, genesis-mythos-master]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]"
decision_kind: deepen
queue_entry_id: godo-c26e4064aa57
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research:
  - "[[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]]"
---

# Conceptual decision record

## Summary

Minted Phase 1.1 as **four runtime layers** (WorldState, Simulation, Presentation, InputIntent) with a session-scoped composition root and canon-commit read-only gate before sim writes. Bus categories (`canon.*`, `sim.*`, `session.*`, `presentation.*`) named for downstream catalog mint.

## PMG alignment

Serves [[genesis-mythos-master-goal]] modularity mandate: decouple world state, simulation, rendering, and input; embed session 0 + canon pipeline boundaries; enable factory-first catalog rows without collapsing layers into monolithic autoload loops.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Monolithic gameplay autoload | Faster greenfield spike | Blocks remixing, hides canon/sim race | PMG requires aggressive modularity |
| Three layers (merge Presentation+Input) | Simpler diagram | Blurs agency delegation vs presentation modes | PMG perspective split needs separate InputIntent |
| Event bus only (no layer IDs) | Flexible wiring | Catalog mint lacks stable nouns | Half A needs named rows before execution |

**Chosen path:** Four named layers + session composer + read-only canon validator gate — aligns influence research canon-as-infrastructure pattern.

## Validation evidence

- [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]] — canon state machine, event-sourced continuity, session-scoped DI
- [[genesis-mythos-master-goal]] — canon pipeline stages, perspective/agency split
- Pattern: World Kernel / canon validator gate (Ikki, Design Science — cited in research synth)
- Validator (nested first pass): [[.technical/Validator/roadmap-auto-validation-20260626T095318Z]] — handoff_verdict: deepen_continue_with_sync

## Links

- Parent roadmap note: [[Phase-1-1-Layer-Decoupling-and-Interface-Contracts-Roadmap-2026-06-26-1200]]
- Workflow log row: 2026-06-26 09:35 | deepen | Phase-1-1-Layer-Decoupling | 1 | 1.1
