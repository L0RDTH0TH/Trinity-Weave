---
title: "Deepen — Phase 3.1.4 Faction Graph subsystem"
created: 2026-06-30
tags: [roadmap, genesis-mythos-master, conceptual-decision-record, factory-feed-gate, tertiary-mint]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-3-1-4-FactionGraph-Subsystem-Roadmap-2026-06-30-0015]]"
decision_kind: deepen
queue_entry_id: godo-c5dfb6c9c49d-next-phase3-tertiary-314
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validator_second_pass_needs_work
persona_id: half_a.conceptual_architect
handoff_readiness_tertiary: 80
factory_feed_gate_reason: conceptual_tertiary_tree_incomplete:phase_3
product_factory_run_id: 1373c0c3408d
---

## Summary

Minted fourth Phase 3 tertiary **3.1.4 — Faction Graph Subsystem** under factory feed gate cursor `phase_3_tertiary_tree`. Completes the **SimTickPipeline** subsystem trio (weather → NPC agendas → faction graph) deferred in parent 3.1 § Behavior — naming **FactionGraphRegistry**, **ThresholdRuleIndex**, **FactionGraphTickDelta**, and **OffScreenEventScheduler** (math-only) without Godot graph UI or **3.2** narrative surfacing.

## PMG alignment

PMG requires living simulation with factions and tribes that evolve while the player is away. Parent 3.1 named **FactionGraphSubsystem** and bound graph math to **ConsequenceResolver** precedence; **3.2** owns **FactionGraphDeltaExtractor** packaging. This slice makes edge weights, threshold rules, and tick-delta envelopes explicit for factory feedstock under `pmg_phases`.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---|---|---|---|
| 3.1.1 body compact first | Clears oldest `body_compact_pending` | No new tertiary; weaker pipeline completion signal | User guidance prefers 3.1.4 mint; completes SimTickPipeline ordering |
| Merge into 3.1.3 NPC slice | Fewer files | Blurs NPC vs faction ownership; violates parent actor table | Parent 3.1 separates **NPCAgendaSubsystem** and **FactionGraphSubsystem** |
| Refine 3.1 secondary only | No new file | Fails `harness_forbid_deepen_noop` | Harness requires material structural change |
| Touch factory/l5 | Could advance Loop 2 | Explicitly forbidden in queue scope | `factory_l5_excluded` |

**Chosen path:** 3.1.4 faction graph as fourth warranted Phase 3 tertiary under 3.1 — closes 3.1 pipeline tertiary set.

## Validation evidence

- [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]] § Behavior **FactionGraphSubsystem** + ordering step 3 (`faction_graph`)
- [[Phase-3-1-3-NPC-Agendas-Subsystem-Roadmap-2026-06-29-2330]] — NPC slot precedes faction pass
- [[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]] — **FactionGraphDeltaExtractor** boundary (packaging vs tick math)
- [[Conceptual-Decision-Records/deepen-phase-3-1-3-npc-agendas-subsystem-2026-06-29-2330]] — prior tertiary opened tree; 3.1.4 was named forward target

## Links

- Parent secondary: [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]
- Minted tertiary: [[Phase-3-1-4-FactionGraph-Subsystem-Roadmap-2026-06-30-0015]]
- Roll-up: [[Phase-3-1-4-FactionGraph-Subsystem-Roll-up-2026-06-30]]
- Prior sibling: [[Phase-3-1-3-NPC-Agendas-Subsystem-Roadmap-2026-06-29-2330]]
- Workflow anchor: 2026-06-30 00:15 | Phase-3-1-4-FactionGraph-Subsystem | godo-c5dfb6c9c49d-next-phase3-tertiary-314
