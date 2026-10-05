---
title: Conceptual decision record — Phase 3.2 body compact under factory feed cap
created: 2026-07-15
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, phase-3, body-compact]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]"
decision_kind: deepen
queue_entry_id: architect-rr-gmm-remi-cc648715
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
---

# Conceptual decision record

## Summary

Compacted Phase **3.2** secondary body **10336→1131** chars (secondary feed cap **1400**) and preserved full NL tables in rollup [[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roll-up-2026-07-15]]. Clears harness `conceptual_note_oversized` for this path under `factory_feed_gate` mint_batch `pmg_phases`.

## PMG alignment

Keeps off-screen faction/tribe narrative packaging feedstock factory-feedable without truncating design nouns — rollup retains absence→delta→narrative contracts that serve living-simulation Phase 3 of the master goal.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Leave oversized body | No rewrite risk | Blocks `conceptual_factory_feed_ready` | Gate RED; forbidden deepen_noop |
| Delete detail permanently | Fastest shrink | Loses handoff evidence | Violates NL preservation |
| Split into tertiaries this run | Smaller secondaries | Scope creep vs single compact | Deferred breadth-first; this run = compact only |

**Chosen path:** Body compact + rollup child (same pattern as Phase 3.1.2 / Phase 3 primary).

## Validation evidence

- Pattern: prior body-compact deepen runs (Phase 3.1.2, Phase 3 primary) under feed cap
- Parent path: `Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615.md`
- Harness: `factory_feed_gate` reason `body_over_cap:10336>1400` → cleared for this slice

## Validator trace

- `validator_first: needs_work` — `primary_code: state_hygiene_failure` — report: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-architect-rr-gmm-remi-cc648715-20260715T210000Z]]
- `ira_applied: true` — ira_report: [[.technical/Internal-Repair-Agent/roadmap/2026-07/genesis-mythos-master-ira-call-1-architect-rr-gmm-remi-cc648715]]
- `validator_second: log_only` — `compare_verdict: improved_vs_first_pass_ira_hygiene_repaired_core_eligible_log_only` — second_pass: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-architect-rr-gmm-remi-cc648715-20260715T211500Z-second-pass]]
- `validation_status: validated`; Body under cap re-verified: 1131 ≤ 1400; feed cursor advanced to Phase-3-3

## Links

- Parent roadmap note: [[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]
- Rollup: [[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roll-up-2026-07-15]]
- Queue: `architect-rr-gmm-remi-cc648715`
