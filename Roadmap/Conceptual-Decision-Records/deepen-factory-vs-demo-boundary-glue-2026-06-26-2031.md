---
title: "CDR — Factory vs demo track boundary glue (Phase 6.3)"
created: 2026-06-26
tags: [conceptual-decision-record, genesis-mythos-master, phase-6, dual-track]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-6-3-Factory-vs-Demo-Track-Boundary-Glue-Roadmap-2026-06-26-2031]]"
decision_kind: deepen
queue_entry_id: godo-followup-20260626T203100Z-phase6-deepen-6-3
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: reconciled
related_research: []
---

## Summary

Chose an explicit **glue secondary (6.3)** with **DualTrackBoundaryManifest**, independent **AttestationSeparationPolicy**, and **MountContractGlue** so factory Phase 0 catalog law (6.1) and horizon demo v1 loop proof (6.2) cannot substitute for each other's sign-off. Default integrated build profile is `horizon_demo_in_shell` — demo runs inside factory **PlayRegionHost** sockets, not a parallel tree.

## PMG alignment

PMG requires factory kinesthetic honesty and a playable vertical slice without conflating catalog attestation with demo feel. Separating attestations preserves Half A factory spine authority while still allowing an integrated player build that mounts demo into the presentation shell.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---|---|---|---|
| Merge boundary into 6.1 only | Fewer notes | Demo track authority blurred; 6.2 exports orphaned at seam | Breadth-first needs dedicated glue after both secondaries exist |
| Merge boundary into 6.2 only | Demo-centric narrative | Factory catalog gates appear demo-owned | Violates dual-track factory spine law |
| Defer glue to execution track only | Faster conceptual pass | No conceptual contract for CI / operator review | Phase 6 primary explicitly lists glue task; PMG dual-track language |

## Validation evidence

- Pattern: dual-track boundary tables in **6.1** and **6.2** already state non-conflation — **6.3** consolidates into **DualTrackBoundaryManifest**
- Validator: [[.technical/Validator/roadmap-auto-validation-20260626T203100Z-godo-followup-20260626T203100Z-phase6-deepen-6-3]]
- Parent notes: [[Phase-6-1-Factory-Phase-0-Presentation-Shell-Roadmap-2026-06-26-1912]], [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]
- Workflow anchor: deepen 6.3 @ 2026-06-26 20:31

## Links

- Parent: [[Phase-6-3-Factory-vs-Demo-Track-Boundary-Glue-Roadmap-2026-06-26-2031]]
- Phase primary: [[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-06-26-0914]]
- Master goal: [[genesis-mythos-master-goal]]
