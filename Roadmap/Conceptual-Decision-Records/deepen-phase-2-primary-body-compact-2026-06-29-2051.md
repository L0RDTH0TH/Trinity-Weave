---
title: "Deepen — Phase 2 primary body compact"
created: 2026-06-29
tags: [roadmap, genesis-mythos-master, conceptual-decision-record]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]"
decision_kind: deepen
queue_entry_id: architect-rr-gmm-remi-phase2-primary-compact-20260629T205100Z
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
---

## Summary

Compacted Phase 2 primary roadmap note body from oversize (7023 chars) to ≤2000 chars by moving handoff table, roll-up gates, open questions, subphase index, dataview, and consistency reports into rollup child [[Phase-2-Procedural-Generation-and-World-Building-Roll-up-2026-06-29]]. Preserved wikilinks to secondaries 2.1/2.2/2.3 and NL sections (Scope, Behavior, Interfaces, Edge cases) on primary.

## PMG alignment

Factory feed gate requires PMG phase primaries stay within harness body cap so Half A catalog / L5 conductor can consume phase feedstock without context blow-up. Phase 2 proc-gen + world-building scope remains visible on compact primary; detail preserved in rollup per Phase 1 primary compact pattern.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---|---|---|---|
| Split into multiple tertiaries | Finer granularity | Scope creep; secondaries already exist | Secondaries 2.1–2.3 already minted |
| Truncate NL sections only | Faster | Loses handoff evidence | Rollup preserves full tables |
| Leave oversize | No edit risk | Blocks factory feed gate RED | Harness `harness_forbid_deepen_noop` requires material compact |

## Validation evidence

- Workflow factory feed gate: `conceptual_note_oversized` on Phase 2 primary (`7023>2000`)
- Pattern: Phase 1 primary compact (`architect-rr-gmm-remi-phase1-primary-oversize`) — rollup child + `rollup-detail` frontmatter
- Queue: `architect-rr-gmm-remi-phase2-primary-compact-20260629T205100Z`

## Links

- Parent: [[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]
- Rollup: [[Phase-2-Procedural-Generation-and-World-Building-Roll-up-2026-06-29]]
- Master goal: [[genesis-mythos-master-goal]]
