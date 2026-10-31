---
title: "CDR — Canon Registry + Intent Resolver (Phase 2.2 deepen)"
created: 2026-06-26
tags: [roadmap, conceptual-decision-record, genesis-mythos-master, phase-2]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]"
decision_kind: deepen
queue_entry_id: godo-followup-20260626T153000Z-phase2-2
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research:
  - "[[Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]]"
  - "[[Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]"
---

## Summary

Minted Phase **2.2** secondary defining **CanonRegistry**, **IntentResolver**, **LoreHookRegistry**, and **CanonFact** lifecycle (`proposed → accepted → hooked → sim-active`) with resolver cross-cuts at **2.1** POI/entity/sim_bootstrap stages. Chose explicit **ConflictArbiter** (no silent merge) and **RegistrySnapshot** alignment with Phase 1.3 dry-run gates.

## PMG alignment

Directly implements PMG **collaborative canon & session bootstrap** — intents become facts, then systemic hooks, then visible ripples. Supports **player-lite** intent inbox and **DM workbench** accept/revise without hardcoded narrative. Registry feeds the collaborative world-forge pipeline in Phase 2.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| Merge registry into **2.1** pipeline note | Fewer files | Oversized secondary; blurs stage vs canon ownership | Breadth-first Phase 2 structure requires separate 2.2 slice per primary task list |
| Auto-accept all session 0 intents | Faster bootstrap | Violates table-agency; risks canon contradictions | PMG requires table accept/revise; ConflictArbiter + validator gates preferred |
| Skip LoreHookRegistry (facts → stages direct) | Simpler graph | Loses hook projection layer from Phase 1.2.2 | Phase 1 intent decomposition already names hook materialization boundary |

## Validation evidence

- PMG canon pipeline states — [[genesis-mythos-master-goal]] § Collaborative canon & session bootstrap
- Phase 1.2.2 intent lifecycle boundaries — [[Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]]
- **2.1** stage handoff points for resolver cross-cut — [[Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]] § Behavior step 6
- Execution rollup / REGISTRY-CI explicitly **execution-deferred** on conceptual track per operator guidance
- Validator report — [[.technical/Validator/roadmap-auto-validation-20260626T183000Z-godo-followup-20260626T153000Z-phase2-2]]
- Second-pass validator — [[.technical/Validator/roadmap-auto-validation-20260626T192000Z-godo-followup-20260626T153000Z-phase2-2-second-pass]]

## Links

- Workflow log: 2026-06-26 15:30 | Phase-2-2-Canon-Registry-and-Intent-Resolver | iter 2.2
- Factory run: `product_factory_run_id: f35ff65cfb4f`
- Persona: `half_a.conceptual_architect`
