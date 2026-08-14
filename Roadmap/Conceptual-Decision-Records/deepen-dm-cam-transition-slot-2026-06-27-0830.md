---
title: CDR — DMCamTransitionSlot DM Cam (6.2.6)
created: 2026-06-27
tags: [roadmap, cdr, genesis-mythos-master, phase-6, horizon-demo, dm-cam]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roadmap-2026-06-27-0830]]"
decision_kind: deepen
queue_entry_id: godo-followup-20260627T083000Z-6-2-6
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
persona_id: half_a.conceptual_architect
---

## Summary

Mint tertiary **6.2.6** for **DMCamTransitionSlot** — beat 6 (DM cam) of the eight-beat horizon demo loop. Decomposes operator-triggered FP→WorldCam transition via **ModeTransitionGraph** edge `fp_to_worldcam_demo`, **TransitionGuardRegistry** guard stack, **DMPauseGate** read-only interaction, and `demo.dm_cam_active` / `presentation.mode_badge_dm` bus split from parent **6.2** secondary. Depth-first continuation after **6.2.5** rule check.

## PMG alignment

PMG requires the horizon demo to prove **perspective split** — player FP explore followed by DM observation rail before overwrite. Isolating beat 6 validates the rule-complete → operator DM cam seam without conflating rule evaluation (beat 5) or live patch overwrite (beat 7).

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---|---|---|---|
| Auto-trigger DM cam on `rule.demo_pass` | Smoother kiosk flow | Violates OQ-6.2-003 operator authority default | Operator hotkey primary; scripted cue execution-only |
| Include MapCam + SensoriumAttach in beat 6 | Fuller 4.2 matrix coverage | Scope creep; parent 6.2 specifies WorldCam rail only for demo v1 | WorldCam-only per OQ-6.2.6-001 |
| Merge beats 5–6 in one tertiary | Fewer files | Breaks eight-beat decomposition precedent | One-beat-per-tertiary (6.2.1–6.2.5) |
| Skip guard stack (trust hotkey) | Simpler stub | Misses play_region / FP / rule outcome guards from parent | Full guard table documented |

## Validation evidence

- Parent 6.2 beat table: beat 6 **DMCamTransitionSlot** with operator hotkey input and **ModeTransitionGraph** + **HUDLayerStack** mode badge output.
- 6.2.5 export: `demo.rule_check_complete` on `session.*` + **RuleEffectBus** outcome for `rule_outcome_allows_dm`.
- 4.2 **ModeTransitionGraph**, **TransitionGuardRegistry**, **WorldCamPolicy**, **DMRailUXContract** (conceptual authority — demo edge subset).
- 3.1 **DMPauseGate** read-only interaction per 4.2 `not_dmpause_frozen` guard.
- OQ resolutions: OQ-6.2.6-001 WorldCam only; OQ-6.2.6-002 mode badge on presentation.*; OQ-6.2.6-003 scripted cue execution-only.
- First-pass validator (IRA-reconciled): [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-godo-followup-20260627T083000Z-6-2-6-20260627T084500Z]]

## Links

- Parent: [[Phase-6-2-Horizon-Demo-V1-Gameplay-Loop-Roadmap-2026-06-26-1951]]
- Prior beat: [[Phase-6-2-5-RuleCheckProbe-Rule-Check-Roadmap-2026-06-27-0800]]
- Tertiary note: [[Phase-6-2-6-DMCamTransitionSlot-DM-Cam-Roadmap-2026-06-27-0830]]
- Workflow log target: Phase-6-2-6-DMCamTransitionSlot-DM-Cam (2026-06-27 08:30)
- Queue: `godo-followup-20260627T083000Z-6-2-6`
