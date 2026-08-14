---
title: Conceptual decision record — Phase 4.2.3 body recompact ≤1200
created: 2026-07-16
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, phase-4, body-compact]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-4-2-3-DM-Rail-Chrome-and-DMRailUXContract-Roadmap-2026-07-16-0653]]"
decision_kind: deepen
queue_entry_id: followup-deepen-gmm-4-2-3-20260716T232339Z
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
roadmap_track: conceptual
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
---

# Conceptual decision record

## Summary

Recompacted Phase **4.2.3** tertiary feedstock body **1267→1060≤1200** under `factory_feed_gate` / Config `max_note_body_chars.tertiary: 1200`. Preserved DMRailUXContract nouns + rollup pointer; dropped duplicate ## Roll-up; tightened Scope/Behavior/Handoff. No factory/L5. Prior siblings 4.1.1=**1061** / 4.1.2=**1176** / 4.1.3=**1153** / 4.2.1=**1138** / 4.2.2=**1031** ≤1200 preserved.

## PMG alignment

Keeps operator rail-chrome + blocked-reason messaging nouns mintable for Half A `pmg_phases` without inventing Godot Camera3D wiring or collapsing chrome into sim mutation.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Leave body at 1267 | No churn | Feed gate RED `body_over_cap` | Forbidden (`harness_forbid_deepen_noop`) |
| Split into quaternary notes | Smaller slices | Tree already closed; overkill for ~200 chars | Cap reachable via compact |
| Deepen factory/L5 | Unrelated | Out of deepen scope | Explicit forbid |

**Chosen:** in-place body compact + roll-up retention; next DFS **4.3.1** `body_over_cap:1296>1200`.

## Validation evidence

- Queue: `followup-deepen-gmm-4-2-3-20260716T232339Z`
- Snapshot: `Versions/Phase-4-2-3-…pre-recompact-1200-20260716-233709.md`
- Live body measure: **1060≤1200**
- Pattern: prior 4.2.2 recompact `followup-deepen-gmm-4-2-2-20260716T230307Z`
- Validator first pass: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-followup-deepen-gmm-4-2-3-20260716T232339Z-20260716T234032Z.md]] — `severity: medium`; `recommended_action: needs_work`; `primary_code: state_hygiene_failure`
- IRA call 1: [[.technical/Internal-Repair-Agent/roadmap/2026-07/genesis-mythos-master-ira-call-1-followup-deepen-gmm-4-2-3-20260716T232339Z.md]]

## Links

- Parent: [[Phase-4-2-3-DM-Rail-Chrome-and-DMRailUXContract-Roadmap-2026-07-16-0653]]
- Roll-up: [[Phase-4-2-3-DM-Rail-Chrome-and-DMRailUXContract-Roll-up-2026-07-16]]
- Master goal: [[genesis-mythos-master-goal]]
- Workflow anchor: deepen 2026-07-16 19:37 Target Phase-4-2-3
- Validator: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-followup-deepen-gmm-4-2-3-20260716T232339Z-20260716T234032Z.md]]