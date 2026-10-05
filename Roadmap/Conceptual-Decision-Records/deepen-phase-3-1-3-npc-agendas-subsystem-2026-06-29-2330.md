---
title: "Deepen — Phase 3.1.3 NPC Agendas subsystem"
created: 2026-06-29
tags: [roadmap, genesis-mythos-master, conceptual-decision-record, factory-feed-gate, tertiary-mint]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-3-1-3-NPC-Agendas-Subsystem-Roadmap-2026-06-29-2330]]"
decision_kind: deepen
queue_entry_id: godo-23ac6568adb3-next-phase3-tertiary-313
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: pending_validator_second_pass
persona_id: half_a.conceptual_architect
handoff_readiness_tertiary: 80
factory_feed_gate_reason: conceptual_tertiary_tree_incomplete:phase_3
product_factory_run_id: 1373c0c3408d
---

## Summary

Minted third Phase 3 tertiary **3.1.3 — NPC Agendas Subsystem** under factory feed gate cursor `phase_3_tertiary_tree`. Materializes the **NPCAgendaSubsystem** actor deferred in parent 3.1 § Behavior — naming **AgendaSlotRegistry**, **LoreHookBindingIndex**, **AvailabilityWindowPolicy**, and **NPCAgendaTickDelta** as the second **SimTickPipeline** slot after weather, without Godot AI paths.

## PMG alignment

PMG requires NPCs with agendas driven by collaborative canon and living simulation time. Parent 3.1 named **NPCAgendaSubsystem** and bound it to **LoreHookRegistry** sim-active hooks; this slice makes agenda slots, availability windows, and ConsequenceResolver merge precedence explicit for factory feedstock under `pmg_phases`.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---|---|---|---|
| 3.1.1 body compact first | Clears oldest `body_compact_pending` | No new tertiary tree node; weaker feed gate progress | User guidance prefers 3.1.3 mint; `depth_first` advances pipeline ordering |
| Mint 3.1.4 faction graph first | Advances graph math | Violates parent § Behavior ordering (`weather → npc → faction`) | Pipeline ordering is PMG-faithful spine per CDR 3.1.2 |
| Refine 3.1 secondary only | No new file | Fails `harness_forbid_deepen_noop` | Harness requires material structural change |
| Touch factory/l5 | Could advance Loop 2 | Explicitly forbidden in queue scope | `factory_l5_excluded` |

**Chosen path:** 3.1.3 NPC agendas as third warranted Phase 3 tertiary under 3.1.

## Validation evidence

- [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]] § Behavior **NPCAgendaSubsystem** + ordering step 3
- [[Phase-3-1-2-Weather-Environmental-State-Subsystem-Roadmap-2026-06-29-2230]] — weather slot precedes NPC pass
- [[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]] — **LoreHookRegistry** sim-active lifecycle
- [[Conceptual-Decision-Records/deepen-phase-3-1-2-weather-environmental-state-subsystem-2026-06-29-2230]] — prior tertiary opened tree

## Links

- Parent secondary: [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]
- Minted tertiary: [[Phase-3-1-3-NPC-Agendas-Subsystem-Roadmap-2026-06-29-2330]]
- Roll-up: [[Phase-3-1-3-NPC-Agendas-Subsystem-Roll-up-2026-06-29]]
- Prior sibling: [[Phase-3-1-2-Weather-Environmental-State-Subsystem-Roadmap-2026-06-29-2230]]
- Workflow anchor: 2026-06-29 23:30 | Phase-3-1-3-NPC-Agendas-Subsystem | godo-23ac6568adb3-next-phase3-tertiary-313
