---
title: Decision Record — Stage DAG Node Contracts (1.2.1)
created: 2026-06-26
tags: [roadmap, decision-record, genesis-mythos-master, phase-1]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]"
decision_kind: deepen
queue_entry_id: godo-25015de8ba91
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research:
  - "[[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]]"
---

## Summary

Minted tertiary **1.2.1** to decompose oversized secondary **1.2** (body > secondary cap). Chose **stage DAG node contracts** first (manifest I/O table + replaceability seams) over intent-pipeline decomposition, preserving depth-first `child_before_sibling_exit` before advancing to sibling **1.3**.

## PMG alignment

PMG mandates a procedural generation graph with deterministic compile and modularity for remixing. Naming stage nodes with typed manifests early gives Half A catalog and Phase 2 executors stable nouns without premature implementation.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| Mint 1.2.1 as intent-pipeline decomposition | Surfaces CanonFact → LoreHook flow sooner | Splits DAG spine from intent cross-cut | DAG contracts are structural prerequisite per parent 1.2 ordering |
| Skip tertiary; advance to 1.3 | Faster breadth | Violates `reject_oversized_without_children` and depth-first branch closure | Body 11k+ chars requires child warrant |
| Refine 1.2 in place | No new file | Exceeds `max_note_body_chars.secondary` | Branch split warrant fires |

## Validation evidence

- Parent 1.2 research integration cites stage DAG + DeterministicCompiler patterns — [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]]
- Config `roadmap.max_note_body_chars.secondary: 1400`; measured parent body ~11429 chars
- `params.deepen_traversal: depth_first` + `child_before_sibling_exit: true` from queue hand-off

## Links

- Parent: [[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]]
- Workflow log target: Phase-1-2-1-Stage-DAG-Node-Contracts (2026-06-26 11:05)
- Queue: `godo-25015de8ba91`
