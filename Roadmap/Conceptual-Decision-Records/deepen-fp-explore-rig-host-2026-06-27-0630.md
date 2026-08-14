---
title: CDR — FPExploreRigHost First-Person Explore (6.2.2)
created: 2026-06-27
tags: [roadmap, cdr, genesis-mythos-master, phase-6, horizon-demo, fp-explore]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roadmap-2026-06-27-0630]]"
decision_kind: deepen
queue_entry_id: godo-followup-20260627T060000Z-6-2-2
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
persona_id: half_a.conceptual_architect
---

## Summary

Mint tertiary **6.2.2** for **FPExploreRigHost** — beat 2 (FP explore) of the eight-beat horizon demo loop. Decomposes FP mode activation, locomotion/look input consumption, and `demo.fp_active` exit gate from parent **6.2** secondary. Depth-first continuation of 6.2 branch after **6.2.1** spawn bootstrap.

## PMG alignment

PMG requires horizon demo v1 to let players **feel** first-person agency before intent/sim/rule beats. Isolating beat 2 proves **PerspectiveEnvelope** `player_fp` activation and input path without conflating spawn (beat 1) or intent labeling (beat 3) — supporting perspective-split pillar validation in the playable loop.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---|---|---|---|
| Merge beats 1–2 in one tertiary | Fewer files | Violates eight-beat decomposition; spawn and explore have distinct gates | Depth-first one-beat-per-tertiary per 6.2.1 precedent |
| Activate FP mode in beat 1 spawn | Shorter path to movement | OQ-6.2.1-003 assigns mode activation to beat 2; conflates attach vs activate | Beat 2 owns **PerspectiveEnvelope** activation |
| Auto-advance beat 2 on timer | Kiosk-friendly | Skips interact teaching moment for beat 3 | Interact-only default; timer is execution debug only |

## Validation evidence

- Parent 6.2 beat table: beat 2 **FPExploreRigHost** with `demo.spawn_complete` input and `demo.fp_active` output.
- 6.2.1 export: FPRig attached-and-inactive; `demo.spawn_complete` on `session.*`.
- 4.1 **PerspectiveEnvelope**: `player_fp` legal mode and self-agency intent routing.
- OQ resolutions: OQ-6.2.2-001 interact-only exit; OQ-6.2.2-002 sensitivity exec-deferred; OQ-6.2.2-003 fp_active after first input frame.

## Links

- Parent: [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]
- Prior beat: [[Phase-6-2-1-SpawnBootstrapController-Session-Bootstrap-Roadmap-2026-06-27-0600]]
- Tertiary note: [[Phase-6-2-2-FPExploreRigHost-First-Person-Explore-Roadmap-2026-06-27-0630]]
- Workflow log target: Phase-6-2-2-FPExploreRigHost-First-Person-Explore (2026-06-27 06:30)
- Queue: `godo-followup-20260627T060000Z-6-2-2`
