---
title: Conceptual decision record — Phase 4.1.2 body recompact ≤1200
created: 2026-07-16
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, phase-4, body-compact]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roadmap-2026-07-16-0828]]"
decision_kind: deepen
queue_entry_id: followup-deepen-gmm-4-1-2-20260716T213643Z
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
roadmap_track: conceptual
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
validator_report: "[[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-followup-deepen-gmm-4-1-2-20260716T213643Z-20260716T215312Z.md]]"
ira_report: "[[.technical/Internal-Repair-Agent/roadmap/2026-07/genesis-mythos-master-ira-call-1-followup-deepen-gmm-4-1-2-20260716T213643Z.md]]"
---

# Conceptual decision record

## Summary

Recompacted Phase **4.1.2** tertiary feedstock body **1407→≤1200** under `factory_feed_gate` / Config `max_note_body_chars.tertiary: 1200`. Preserved composition nouns + rollup pointer; tightened Interfaces/Handoff. No factory/L5. Sibling 4.1.1 live measure **1029≤1200** (historical trail 1400→1014 retained).

## PMG alignment

Keeps UnifiedSceneGraph / CameraInterpolatorRegistry / PlayerFPRig mintable for Half A `pmg_phases` without inventing Camera3D ownership or dropping PerspectiveAnchor exclusivity.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Leave body at 1407 | No churn | Feed gate RED `body_over_cap` | Forbidden (`harness_forbid_deepen_noop`) |
| Split into quaternary notes | Smaller slices | Tree already closed; overkill for ~220 chars | Cap reachable via compact |
| Deepen factory/L5 | Unrelated | Out of deepen scope | Explicit forbid |

**Chosen:** in-place body compact + roll-up retention; next DFS **4.1.3** `body_over_cap`.

## Validation evidence

- Queue: `followup-deepen-gmm-4-1-2-20260716T213643Z`
- Gate: `factory_feed_gate` / `conceptual_note_oversized` / tertiary cap 1200
- Body measured: **1188≤1200** (before 1407)
- Sibling consistency: 4.1.1 live **1029≤1200** (historical 1014 trail)
- Pattern: Phase-4.1.1 body-recompact-1200 trail
- Artifact: `Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roadmap-2026-07-16-0828.md`
- Validator first: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-followup-deepen-gmm-4-1-2-20260716T213643Z-20260716T215312Z.md]] — `needs_work` / `state_hygiene_failure`
- IRA: [[.technical/Internal-Repair-Agent/roadmap/2026-07/genesis-mythos-master-ira-call-1-followup-deepen-gmm-4-1-2-20260716T213643Z.md]]

## Links

- Parent: [[Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roadmap-2026-07-16-0828]]
- Roll-up: [[Phase-4-1-2-UnifiedSceneGraph-CameraInterpolatorRegistry-and-PlayerFPRig-Roll-up-2026-07-16]]
- Prior CDR: [[Conceptual-Decision-Records/deepen-phase-4-1-2-unified-scene-graph-2026-07-16-0828]]
- Sibling recompact: [[Conceptual-Decision-Records/deepen-phase-4-1-1-body-recompact-1200-2026-07-16-1722]]
