---
title: Conceptual decision record — Phase 4.3.3 AgencyPersistenceLedger tertiary
created: 2026-07-16
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, phase-4, tertiary-tree]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-4-3-3-AgencyPersistenceLedger-AbsentProxy-and-RailStatePersistence-Roadmap-2026-07-16-0749]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase433-tertiary-20260716T114316Z
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
---

# Conceptual decision record

## Summary

Minted Phase **4.3.3** tertiary under live `phase_4_tertiary_tree` for **AgencyPersistenceLedger** + **AbsentProxyPolicyTable** + **RailStatePersistence** — persistence contracts for dominate / absent-proxy / DM rail cursor across transitions. Closes the 4.3 tertiary branch after 4.3.2 without factory/L5 or pseudo-code.

## PMG alignment

Deepens Phase 4 perspective/control by naming how agency and rail state survive mode switches and loads, preserving layer-decoupling while serializers and Camera3D stay execution-deferred.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Fold ledger into 4.3.2 Glue | Fewer notes | Mixes choreography with persistence; bloated body | Parent rollup separates glue vs ledger nouns |
| Skip 4.3.3 / only update parent | Cheap | No tertiary-tree progress; harness noop | Forbidden while feed gate RED |
| Mint 4.1 tertiaries first | Earlier 4.1 DFS | Breaks declared next DFS after 4.3.2 | Continuity + queue target 4.3.3 |

**Chosen:** mint `4.3.3` AgencyPersistenceLedger / AbsentProxy / RailStatePersistence; queue `4.1` tertiaries next under `phase_4_tertiary_tree`.

## Validation evidence

- Queue: `followup-deepen-phase433-tertiary-20260716T114316Z`
- Gate: `factory_feed_gate` / `phase_4_tertiary_tree`
- Persona: `half_a.conceptual_architect`
- Artifact: `Phase-4-3-3-AgencyPersistenceLedger-AbsentProxy-and-RailStatePersistence-Roadmap-2026-07-16-0749.md`
- Pattern: parent 4.3 rollup ledger/proxy/rail actor rows + D-4.3-001/002/003
- MCP backup unavailable; `run_mode: full_run_inline`
- validator_first: needs_work; primary_code: state_hygiene_failure
- report: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-followup-deepen-phase433-tertiary-20260716T114316Z-20260716T115417Z.md]]
- ira_report: [[.technical/Internal-Repair-Agent/roadmap/2026-07/genesis-mythos-master-ira-call-1-followup-deepen-phase433-tertiary-20260716T114316Z.md]]

## Links

- Parent: [[Phase-4-3-Agency-Envelope-and-Pilot-Machinery-Glue-Roadmap-2026-06-26-1945]]
- Prior tertiary: [[Phase-4-3-2-PilotMachineryGlue-and-PilotHandoffCoordinator-Roadmap-2026-07-16-0729]]
- New tertiary: [[Phase-4-3-3-AgencyPersistenceLedger-AbsentProxy-and-RailStatePersistence-Roadmap-2026-07-16-0749]]
- PMG: [[genesis-mythos-master-goal]]
