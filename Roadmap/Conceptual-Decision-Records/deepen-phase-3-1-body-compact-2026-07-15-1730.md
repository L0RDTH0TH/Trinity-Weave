---
title: Conceptual decision record — Phase 3.1 body compact under factory feed cap
created: 2026-07-15
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, phase-3, body-compact]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase31-20260715T212746Z
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
---

# Conceptual decision record

## Summary

Compacted Phase **3.1** secondary body **11906→≤1400** chars (secondary feed cap **1400**) and preserved full NL tables in rollup [[Phase-3-1-Tick-Based-Simulation-Core-Roll-up-2026-07-15]]. Clears harness `conceptual_note_oversized` for this path under `factory_feed_gate` mint_batch `pmg_phases`.

## PMG alignment

Keeps tick-based simulation core feedstock factory-feedable without truncating design nouns — rollup retains actor registry, seven-step ordering, Phase 2/1 imports, and 3.2/3.3 seams that serve living-simulation Phase 3 of the master goal.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Leave oversized body | No rewrite risk | Blocks `conceptual_factory_feed_ready` | Gate RED; forbidden deepen_noop |
| Delete detail permanently | Fastest shrink | Loses handoff evidence | Violates NL preservation |
| Split into tertiaries this run | Smaller secondaries | Scope creep vs single compact | Deferred; this run = compact only |

**Chosen path:** Body compact + rollup child (same pattern as Phase 3.2 / 3.3 / Phase 3 primary).

## Validation evidence

- Pattern: prior body-compact deepen runs (Phase 3.3, Phase 3.2, Phase 3.1.2) under feed cap
- Parent path: `Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600.md`
- Harness: `factory_feed_gate` reason `body_over_cap:11906>1400` → cleared for this slice

## Validator trace

- `validator_first: needs_work` — `primary_code: state_hygiene_failure` — report: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-followup-deepen-phase31-20260715T212746Z-20260715T213159Z]]
- `ira_applied: true` — ira_report: [[.technical/Internal-Repair-Agent/roadmap/2026-07/genesis-mythos-master-ira-call-1-followup-deepen-phase31-20260715T212746Z]]
- `validator_second: log_only` — `compare_verdict: improved_vs_first_pass_ira_hygiene_repaired_core_eligible_log_only` — second_pass: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-followup-deepen-phase31-20260715T212746Z-20260715T213532Z-second-pass]]
- `validation_status: validated`; Body under cap re-verified: 1189 ≤ 1400; feed cursor advanced to Phase-3-1-3

## Links

- Parent roadmap note: [[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]
- Rollup: [[Phase-3-1-Tick-Based-Simulation-Core-Roll-up-2026-07-15]]
- Queue: `followup-deepen-phase31-20260715T212746Z`
