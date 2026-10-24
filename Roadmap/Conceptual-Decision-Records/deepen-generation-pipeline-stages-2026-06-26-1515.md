---
title: Conceptual decision record — Generation pipeline stages (2.1)
created: 2026-06-26
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, phase-2]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]"
decision_kind: deepen
queue_entry_id: godo-followup-20260626T151300Z-phase2-1
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research:
  - "[[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]]"
---

# Conceptual decision record

## Summary

Minted Phase **2.1** secondary naming **GenerationPipeline** stage executors from SeedParser through sim_bootstrap, with **CollaborativeRefinementLoop** pause points and **DryRunValidator** + **SeedSnapshot** gates at pipeline entry and pre-compile — materializing Phase 1 DAG contracts for the collaborative world-forge phase.

## PMG alignment

PMG Phase 2 mandates generation pipeline `seed parsing → terrain → biomes → POIs → entities → simulation bootstrap` and collaborative dialogue (system proposes scaffolds, users refine). This choice maps PMG stages to named executors and explicit refinement loops without hardcoded narratives.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Flatten all stages into Phase 2 primary | Fewer notes | Oversized primary; poor breadth-first exit | Phase 2 primary checklist already defines three secondaries |
| Merge 2.1 + 2.2 in one deepen | Faster breadth | Violates single-artifact deepen; blurs canon registry boundary | Queue contract: one secondary per run; 2.2 owns IntentResolver detail |
| Skip CollaborativeRefinementLoop | Simpler pipeline | Loses PMG collaborative forge identity | PMG explicitly requires choice loops between intents and machine |

**Chosen path:** Dedicated **2.1** secondary with stage executors + collaborative gates; canon registry deferred to **2.2**.

## Validation evidence

- Phase 1.2 / 1.2.1 stage DAG and manifest I/O — [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]
- Phase 1.3 SeedSnapshot + DryRunValidator — [[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]
- Influence research pattern: WorldGen Director→Validator→Compiler — [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]]
- PMG Phase 2 bullet list — [[genesis-mythos-master-goal]]
- Hostile first-pass validator — [[.technical/Validator/roadmap-auto-validation-20260626T173600Z-godo-followup-20260626T151300Z-phase2-1-l1postlv.md]]

## Links

- Parent roadmap note: [[Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]
- Workflow log row: 2026-06-26 15:15 | deepen | Phase-2-1-Generation-Pipeline-Stages | 2.1
