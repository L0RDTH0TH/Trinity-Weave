---
title: "Deepen — Phase 3.1.1 SimClock and TickScheduler policy"
created: 2026-06-29
tags: [roadmap, genesis-mythos-master, conceptual-decision-record, factory-feed-gate, tertiary-mint]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-3-1-1-SimClock-and-TickScheduler-Policy-Roadmap-2026-06-29-2205]]"
decision_kind: deepen
queue_entry_id: godo-1b2f88b2381e-next-phase3-tertiary
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: pending_validator_second_pass
persona_id: half_a.conceptual_architect
handoff_readiness_tertiary: 79
factory_feed_gate_reason: conceptual_tertiary_tree_incomplete:phase_3
product_factory_run_id: 1373c0c3408d
---

## Summary

Minted first Phase 3 tertiary **3.1.1 — SimClock and TickScheduler Policy** under factory feed gate cursor `phase_3_tertiary_tree`. Materializes the clock + scheduler contracts deferred in parent 3.1 § Tasks — naming **SimClockPolicyRegistry**, **TickBudgetManifest**, **CatchupDeferralPolicy**, and **DMPauseGate** finish-in-flight rule at the clock layer without Godot implementation paths.

## PMG alignment

PMG requires a living simulation that advances independently of rendering. Parent 3.1 named **SimClock** and **TickScheduler** but deferred tertiary detail; this slice makes step-mode and catch-up policy explicit for factory feedstock under `pmg_phases` and for **3.2** **AbsenceCatchupBridge** coordination.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---|---|---|---|
| Breadth-first tertiary exempt only | Faster gate narrative | Fails `harness_forbid_deepen_noop` on RED feed gate | Harness requires material structural change |
| Mint 3.2 tertiary first | Off-screen narrative is player-visible | `depth_first` + `child_before_sibling_exit` requires 3.1 branch first | Queue params + parent § Tasks cite 3.1 tertiaries first |
| Refine 3.1 secondary in-place only | No new file | No tertiary tree progress; noop under harness | `harness_forbid_deepen_noop: true` |
| Touch factory/l5 | Could advance Loop 2 | Explicitly forbidden in queue scope | `factory_l5_excluded` |

**Chosen path:** 3.1.1 SimClock + TickScheduler policy as first warranted Phase 3 tertiary under 3.1.

## Validation evidence

- [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]] § Tasks deferred tertiaries + § Behavior SimClock/TickScheduler
- [[workflow_state]] `factory_feed_gate_reason: conceptual_tertiary_tree_incomplete:phase_3`
- [[Conceptual-Decision-Records/deepen-phase-3-secondary-tree-factory-feed-gate-2026-06-29-2145]] — secondary tree qualified; tertiary tree opened
- Pattern: registry-before-executor (same as 1.2.1 stage DAG before pipeline run)

## Links

- Parent secondary: [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]
- Minted tertiary: [[Phase-3-1-1-SimClock-and-TickScheduler-Policy-Roadmap-2026-06-29-2205]]
- Roll-up: [[Phase-3-1-1-SimClock-and-TickScheduler-Policy-Roll-up-2026-06-29]]
- Workflow anchor: 2026-06-29 22:05 | Phase-3-1-1-SimClock-and-TickScheduler-Policy | godo-1b2f88b2381e-next-phase3-tertiary
