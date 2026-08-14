---
title: Conceptual decision record — Phase 3.1.3 body compact under factory feed cap
created: 2026-07-15
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, phase-3, body-compact]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-3-1-3-NPC-Agendas-Subsystem-Roadmap-2026-06-29-2330]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase313-20260715T213743Z
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
validator_first: needs_work
primary_code: state_hygiene_failure
ira_applied: true
validation_hygiene: reconciled
related_research: []
---

# Conceptual decision record

## Summary

Compacted Phase **3.1.3** tertiary body **5644→1163** chars (≤1200 harness / ≤1400 feed cap) and preserved full NL tables in rollup [[Phase-3-1-3-NPC-Agendas-Subsystem-Roll-up-2026-06-29]]. Clears `conceptual_note_oversized` for this path under `factory_feed_gate` mint_batch `pmg_phases`.

## PMG alignment

Keeps NPC agenda + lore-hook feedstock factory-feedable without truncating design nouns — rollup retains actors, lifecycle, per-tick sketch, imports/exports, and edge cases that serve Phase 3 living simulation.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Leave oversized body | No rewrite risk | Blocks factory feed readiness | Gate RED; forbidden deepen_noop |
| Delete detail permanently | Fastest shrink | Loses handoff evidence | Violates NL preservation |
| Atomize new quarternaries this run | Smaller tertiary | Scope creep vs single compact | Deferred; this run = compact only |

**Chosen path:** Body compact + existing rollup child (same pattern as Phase 3.1.2 / 3.1.1).

## Validation evidence

- Pattern: prior body-compact deepen runs (Phase 3.1, 3.1.2, 3.2, 3.3) under feed cap
- Parent path: `Phase-3-1-3-NPC-Agendas-Subsystem-Roadmap-2026-06-29-2330.md`
- Harness: `factory_feed_gate` reason `body_over_cap:5641>1400` → cleared for this slice; next cursor Phase-3-1-4 (`6052>1400`)
- Measured body raw **1163** / strip **1160** ≤1200 harness / ≤1400 feed (pre **5644**)

## Validator trace

- **validator_first:** `needs_work` — `primary_code: state_hygiene_failure` — `reason_codes: state_hygiene_failure,contradictions_detected,safety_unknown_gap,missing_roll_up_gates`
- **report:** [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-followup-deepen-phase313-20260715T213743Z-20260715T214952Z]]
- **ira_call_index:** 1 — **ira_applied:** true — **validation_hygiene:** reconciled
- **ira_report:** [[.technical/Internal-Repair-Agent/roadmap/2026-07/genesis-mythos-master-ira-call-1-followup-deepen-phase313-20260715T213743Z]]
- **execution_gaps_advisory:** true — `missing_roll_up_gates` / forward `safety_unknown_gap` remain conceptual-track advisory (no HR pins invented)
- **compare_verdict:** pending_second_pass
- **validation_status:** pattern_only (until second pass)

## Links

- Parent roadmap note: [[Phase-3-1-3-NPC-Agendas-Subsystem-Roadmap-2026-06-29-2330]]
- Rollup: [[Phase-3-1-3-NPC-Agendas-Subsystem-Roll-up-2026-06-29]]
- Queue: `followup-deepen-phase313-20260715T213743Z`
