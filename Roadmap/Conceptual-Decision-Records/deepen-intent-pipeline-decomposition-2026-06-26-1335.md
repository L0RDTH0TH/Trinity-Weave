---
title: Conceptual decision record — intent pipeline decomposition 1.2.2
created: 2026-06-26
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, intent-pipeline]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]]"
decision_kind: deepen
queue_entry_id: godo-8314515a9b29
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research:
  - "[[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]]"
---

# Conceptual decision record

## Summary

Minted tertiary **1.2.2** to decompose parent **IntentResolver** intent population flow (`proposed → accepted → hooked → sim-active`) after **1.2.1** stage DAG contracts, honoring depth-first `child_before_sibling_exit` before sibling **1.3**.

## PMG alignment

PMG mandates canon pipeline and LoreHookRegistry population before sim bootstrap. This slice names actors, bus events, and stage cross-cut timing so Half A catalog mint can attach nouns without guessing IntentResolver ownership.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Fold intent flow into 1.2.1 stage table | Single tertiary | Blurs DAG spine vs intent cross-cut | Parent 1.2 explicitly defers intent decomposition to 1.2.2 |
| Mint DeterministicCompiler tertiary before intent | Surfaces compile gate earlier | Intent outputs are compile inputs — order inverted | DAG + intent population precede compile per parent ordering |
| Refine 1.2.1 in place | No new file | Does not satisfy user_guidance mint 1.2.2 | Queue explicitly requested tertiary mint |

**Chosen path:** Tertiary **1.2.2** intent-pipeline decomposition — aligns with parent IntentResolver actor table and PMG canon lifecycle.

## Validation evidence

- Parent [[Phase-1-2-Procedural-Generation-Graph-and-Intent-Population-Pipeline-Roadmap-2026-06-26-1022]] IntentResolver ordering and edge cases (pattern continuity)
- Prior CDR [[deepen-stage-dag-node-contracts-2026-06-26-1105]] branch-split warrant
- Influence research [[Ingest/Agent-Research/2026-06-26-influence-conceptual-deepen-gmm-093504Z]] — `proposed → accepted → hooked → sim-active` mapping (indirect pattern)
- Validator first pass: [[.technical/Validator/roadmap-auto-validation-20260626T133500Z-godo-8314515a9b29]]

## Links

- Parent roadmap note: [[Phase-1-2-2-Intent-Pipeline-Decomposition-Roadmap-2026-06-26-1335]]
- Workflow log row: 2026-06-26 13:35 | deepen | Phase-1-2-2-Intent-Pipeline-Decomposition | 1.2.2
