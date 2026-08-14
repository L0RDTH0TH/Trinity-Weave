---
title: Conceptual decision record — Phase 4.1.1 body recompact ≤1200
created: 2026-07-16
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, phase-4, body-compact]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roadmap-2026-07-16-0812]]"
decision_kind: deepen
queue_entry_id: architect-rr-gmm-remi-fd0e8a04
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
roadmap_track: conceptual
persona_id: half_a.conceptual_architect
product_factory_run_id: 1373c0c3408d
validator_report: "[[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-architect-rr-gmm-remi-fd0e8a04-20260716T212548Z.md]]"
ira_report: "[[.technical/Internal-Repair-Agent/roadmap/2026-07/genesis-mythos-master-ira-call-1-architect-rr-gmm-remi-fd0e8a04.md]]"
---

# Conceptual decision record

## Summary

Recompacted Phase **4.1.1** tertiary feedstock body **1400→≤1200** under `factory_feed_gate` / Config `max_note_body_chars.tertiary: 1200`. Preserved nouns + rollup pointer; moved verbose import/export prose into existing roll-up. No factory/L5.

## PMG alignment

Keeps PerspectiveEnvelope / ModeTransitionGraph / PilotGraph mintable for Half A `pmg_phases` without dropping control-noun fidelity or inventing Godot Camera3D ownership.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Leave body at 1400 | No churn | Feed gate RED `body_over_cap` | Forbidden (`harness_forbid_deepen_noop`) |
| Split into quaternary notes | Smaller slices | Tree already closed; overkill for ~200 chars | Cap reachable via compact |
| Deepen factory/L5 | Unrelated | Out of deepen scope | Explicit forbid |

**Chosen:** in-place body compact + roll-up retention; next DFS **4.1.2** `body_over_cap`.

## Validation evidence

- Queue: `architect-rr-gmm-remi-fd0e8a04`
- Gate: `factory_feed_gate` / `conceptual_note_oversized` / tertiary cap 1200
- Body measured: **1014≤1200**
- Pattern: prior Phase-4/6 body-compact + roll-up trail
- Artifact: `Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roadmap-2026-07-16-0812.md`
- Validator first: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-architect-rr-gmm-remi-fd0e8a04-20260716T212548Z.md]] — `needs_work` / `state_hygiene_failure`
- IRA: [[.technical/Internal-Repair-Agent/roadmap/2026-07/genesis-mythos-master-ira-call-1-architect-rr-gmm-remi-fd0e8a04.md]]

## Links

- Parent: [[Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roadmap-2026-07-16-0812]]
- Roll-up: [[Phase-4-1-1-PerspectiveEnvelope-ModeTransitionGraph-and-PilotGraph-Roll-up-2026-07-16]]
- Prior CDR: [[Conceptual-Decision-Records/deepen-phase-4-1-1-perspective-envelope-2026-07-16-0812]]
