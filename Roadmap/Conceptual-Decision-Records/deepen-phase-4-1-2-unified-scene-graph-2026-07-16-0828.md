---
title: Conceptual decision record — Phase 4.1.2 UnifiedSceneGraph tertiary
created: 2026-07-16
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, phase-4, tertiary-tree]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roadmap-2026-07-16-0828]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase412-tertiary-20260716T122709Z
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
---

# Conceptual decision record

## Summary

Minted Phase **4.1.2** tertiary under live `phase_4_tertiary_tree` for **UnifiedSceneGraph** + **CameraInterpolatorRegistry** + **PlayerFPRig** — composition nouns for scene attachment, blend selection, and default FP agency. Advances DFS after 4.1.1 without factory/L5 or pseudo-code.

## PMG alignment

Deepens Phase 4 perspective/control by naming how presentation composes a single scene authority and swaps camera blends while keeping Camera3D/SubViewport and per-rig FOV on sibling tertiaries / execution track.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Fold into parent 4.1 only | Fewer notes | No tertiary-tree progress; harness noop | Forbidden while feed gate RED |
| Mint FOV rigs first (4.1.3) | Earlier DM rig detail | Breaks declared next DFS after 4.1.1 | Continuity + queue target 4.1.2 |
| Bundle all 4.1 nouns in one tertiary | One note | Body >1400; mixes control vs composition | Cap + sibling DFS |

**Chosen:** mint `4.1.2` UnifiedSceneGraph / CameraInterpolatorRegistry / PlayerFPRig; queue `4.1.3` WorldCam / MapCam / SensoriumAttach FOV next.

## Validation evidence

- Queue: `followup-deepen-phase412-tertiary-20260716T122709Z`
- Gate: `factory_feed_gate` / `phase_4_tertiary_tree`
- Persona: `half_a.conceptual_architect`
- Artifact: `Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roadmap-2026-07-16-0828.md`
- Pattern: parent 4.1 rollup actor rows + ModeTransitionGraph ordering step 3 (interpolator)
- Validator first pass: `needs_work` / `state_hygiene_failure` — [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-followup-deepen-phase412-tertiary-20260716T122709Z-20260716T123331Z]]
- MCP backup unavailable; `run_mode: full_run_inline`

## Links

- Parent: [[Phase-4-1-Player-FP-and-Perspective-Envelope-Roadmap-2026-06-26-1705]]
- Prior DFS: [[Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roadmap-2026-07-16-0812]]
- New tertiary: [[Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roadmap-2026-07-16-0828]]
- PMG: [[genesis-mythos-master-goal]]
