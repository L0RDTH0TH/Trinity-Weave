---
title: CDR — PlayRegionHost Mount Lifecycle Decomposition (6.1.2)
created: 2026-06-27
tags: [roadmap, conceptual-decision-record, genesis-mythos-master, phase-6]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-6-1-2-PlayRegionHost-Mount-Lifecycle-Roadmap-2026-06-27-0431]]"
decision_kind: deepen
queue_entry_id: godo-509363bc2f08
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research:
  - "Ingest/Agent-Research/2026-06-27-influence-conceptual-deepen-gmm-040652Z.md"
product_factory_run_id: c1dc1d565ea2
---

## Summary

Split parent **6.1** at the **PlayRegion** stage: mint tertiary **6.1.2** naming **PlayRegionHost** mount lifecycle, prerequisite gate on **PresentationSessionHandle**, rig socket catalog, `presentation.play_region_ready` bus contract, and single-active-PlayRegion invariant — deferring HUD layers to **6.1.3**.

## PMG alignment

Factory Phase 0 presentation shell proves **launch → PlayRegion → HUD** ordering before horizon demo wiring. Isolating **PlayRegionHost** enables Half A catalog attestation of viewport mount + socket registry without conflating launch bootstrap (**6.1.1**) or HUD chrome (**6.1.3**).

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---|---|---|---|
| Keep PlayRegion in parent 6.1 only | Fewer notes | Parent already oversized; branch_split at 6.1.1 | Depth-first backfill requires sibling tertiaries |
| Merge PlayRegion + HUD in one tertiary | Shorter branch | Violates three-stage funnel boundaries; weakens **KH-6.1-003** audit | HUD is distinct factory scope (**6.1.3**) |
| Allow multi-PlayRegion at conceptual depth | Flexible demos | Conflicts with parent OQ-6.1-002 factory Phase 0 contract | Single active PlayRegion locked |

## Validation evidence

- Parent **6.1** Launch → PlayRegion → HUD table and **PlayRegionHost** responsibilities — [[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]
- **6.1.1** handoff fields and `launch_complete` boundary — [[Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]]
- **MountContractGlue** socket naming for 6.2 consumers — [[Phase-6-3-Factory-vs-Demo-Track-Boundary-Glue-Roadmap-2026-06-26-2031]]
- Research: launch handoff + dual-track socket discipline — [[Ingest/Agent-Research/2026-06-27-influence-conceptual-deepen-gmm-040652Z]]
- Validator first pass (IRA reconciled): [[.technical/Validator/roadmap-auto-validation-20260627T045512Z-godo-509363bc2f08]]

## Links

- Workflow log target: Phase-6-1-2-PlayRegionHost-Mount-Lifecycle (6.1.2)
- Queue: `godo-509363bc2f08`
- Prior slice: [[Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]]
