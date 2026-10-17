---
title: CDR — Launch Flow and DevLeakageGuard Decomposition (6.1.1)
created: 2026-06-27
tags: [roadmap, cdr, genesis-mythos-master, phase-6, factory]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap-Roadmap-2026-06-27-0406]]"
decision_kind: deepen
queue_entry_id: godo-4b200d9dc28e
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
persona_id: half_a.conceptual_architect
---

## Summary

Split parent **6.1** factory presentation shell at the **Launch** stage: mint tertiary **6.1.1** naming **LaunchFlowController** lifecycle, bootstrap checklist, **DevLeakageGuard** policy, and **PresentationSessionHandle** handoff — deferring PlayRegion and HUD to sibling tertiaries. Depth-first backfill after Phase 6 breadth complete at **6.3**.

## PMG alignment

PMG requires factory Phase 0 to prove player-facing presentation law (kinesthetic honesty, no dev leakage) before horizon demo gameplay. Decomposing launch/bootstrap isolates attestation-critical gates from mount/HUD slices so Half A catalog rows can sign off incrementally without conflating factory spine with demo loop (6.2).

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---|---|---|---|
| Refine 6.1 in place | No new files | Parent already exceeds secondary body cap; checklist dilution | Branch split warranted per `max_note_body_chars.secondary` |
| Jump to advance-phase | Faster phase closure | Leaves 6.x without tertiaries; violates `child_before_sibling_exit` | Depth-first params require child backfill first |
| Mint 6.3.1 glue tertiary first | Boundary doc is fresh | Skips 6.1 branch closure — sibling exit blocked | 6.1 is earliest open branch |

## Validation evidence

- Pattern: Phase **1.2.1** / **1.2.2** branch split precedent for oversized secondaries on conceptual track.
- Parent note [[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]] — launch stage table and DevLeakageGuard section.
- Config `roadmap.max_note_body_chars.secondary: 1400` — parent body exceeds cap.
- Validator: [[.technical/Validator/roadmap-auto-validation-20260627T040653Z-godo-4b200d9dc28e]]

## Links

- Parent: [[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]]
- Workflow log target: Phase-6-1-1-Launch-Flow-and-DevLeakageGuard-Session-Bootstrap (2026-06-27 04:06)
- Queue: `godo-4b200d9dc28e`
