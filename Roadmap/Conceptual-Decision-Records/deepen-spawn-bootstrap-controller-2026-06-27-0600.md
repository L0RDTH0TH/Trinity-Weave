---
title: CDR — SpawnBootstrapController Session Bootstrap (6.2.1)
created: 2026-06-27
tags: [roadmap, cdr, genesis-mythos-master, phase-6, horizon-demo, spawn-bootstrap]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roadmap-2026-06-27-0600]]"
decision_kind: deepen
queue_entry_id: godo-1168c1400f2f
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
persona_id: half_a.conceptual_architect
---

## Summary

Mint tertiary **6.2.1** for **SpawnBootstrapController** — beat 1 (Spawn) of the eight-beat horizon demo loop. Decomposes the spawn stage from parent **6.2** secondary: session-handle consumption, stub world facet initialization, **PlayerFPRig** socket attachment, and `demo.spawn_complete` emission gate. Depth-first backfill of the 6.2 branch; 6.1 triad already closed (6.1.1–6.1.3).

## PMG alignment

PMG requires horizon demo v1 to prove perspective split, living sim seam, and DM overwrite in a single playable loop. Decomposing beat 1 isolates the session-bootstrap contract from locomotion (beat 2), intent (beat 3), sim (beat 4), and downstream beats — enabling Half A catalog to sign off spawn gate independently. Canonical bus string `presentation.play_region_ready` (not bare `PlayRegionReady`) enforced per 6.1.2/6.1.3 law.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---|---|---|---|
| Refine 6.2 secondary in-place | No new file | 6.2 secondary already at breadth-complete; beat granularity lost | Depth-first backfill warranted per `child_before_sibling_exit` and eight-beat loop contract |
| Mint all eight beats in one note | Compact | Oversize violation; beats have independent precondition gates | Tertiary scope should map one beat per note (or closely coupled beat pair) |
| Start with beat 2 FPExploreRigHost | FP locomotion is richer | Beat 1 is dependency for beat 2; spawn must precede FP explore | Depth-first: beat 1 first per DemoLoopOrchestrator stage ordering |

## Validation evidence

- Parent 6.2 secondary HorizonDemoManifest beat table: beat 1 `SpawnBootstrapController` with `presentation.play_region_ready` prerequisite.
- 6.1.2 socket catalog: `fp_baseline_rig` socket confirmed as FPRig mount target.
- 6.1.3 canonical bus string: `presentation.play_region_ready` (not `PlayRegionReady`).
- OQ resolutions: OQ-6.2.1-001 single-attempt per session; OQ-6.2.1-002 one POI sufficient; OQ-6.2.1-003 beat 2 owns mode activation.

## Links

- Parent: [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]
- Tertiary note: [[Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roadmap-2026-06-27-0600]]
- Workflow log target: Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap (2026-06-27 06:00)
- Queue: `godo-1168c1400f2f`
