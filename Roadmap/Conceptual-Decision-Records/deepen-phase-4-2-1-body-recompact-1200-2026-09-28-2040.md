---
title: Conceptual decision record — Phase 4.2.1 body recompact ≤1200 (overnight)
created: 2026-09-28
tags: [conceptual-decision-record, roadmap, genesis-mythos-master, phase-4, body-compact]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]"
decision_kind: deepen
queue_entry_id: architect-rr-gmm-exec-68db4b29
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
related_research: []
roadmap_track: conceptual
persona_id: half_a.conceptual_architect
goal_authority_run_id: gmm-exec-deepen-overnight-20260928T235200Z
validator_report: "[[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-architect-rr-gmm-exec-68db4b29-20260929T004438Z.md]]"
ira_report: "[[.technical/Internal-Repair-Agent/roadmap/2026-09/genesis-mythos-master-ira-call-1-architect-rr-gmm-exec-68db4b29.md]]"
architect_orchestration_run_id: gmm-exec-deepen-overnight-20260928T235200Z
---

# Conceptual decision record

## Summary

Recompacted Phase **4.2.1** tertiary feedstock body **1211→1193≤1200** under `factory_feed_gate` / tertiary cap 1200. Preserved TransitionGuardRegistry / DM session authority nouns + rollup pointer; scrubbed stale Handoff Next DFS. No factory/L5. Frozen stamp retained (feed-gate feedstock write).

## PMG alignment

Keeps DM rail transition guard nouns mintable for Half A `pmg_phases` without inventing Godot signal wiring.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| ------------- | ------ | -------- | -------------- |
| Leave body at 1211 | No churn | Feed gate RED `body_over_cap` | Forbidden (`harness_forbid_deepen_noop`) |
| Split into quaternary notes | Smaller slices | Tree closed; overkill for ~18 chars | Cap reachable via compact |
| Deepen factory/L5 | Unrelated | Out of deepen scope | Explicit forbid |

**Chosen:** in-place body recompact; next DFS Phase-6 primary `body_over_cap:2900>2000` (post-clear feed cursor).

## Validation evidence

- Validator first: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-architect-rr-gmm-exec-68db4b29-20260929T004438Z.md]] — needs_work / state_hygiene_failure
- IRA: [[.technical/Internal-Repair-Agent/roadmap/2026-09/genesis-mythos-master-ira-call-1-architect-rr-gmm-exec-68db4b29.md]]

- Queue: `architect-rr-gmm-exec-68db4b29`
- Gate: `factory_feed_gate` / `conceptual_note_oversized` / tertiary cap 1200
- Body measured: **1193≤1200** (before 1211)
- Snapshot: `Versions/Phase-4-2-1-…pre-recompact-1200-20260929-004045.md`
- Pattern: Phase-4 tertiary body-recompact-1200 trail
- Artifact: `Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456.md`

## Links

- Parent: [[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roadmap-2026-07-16-0456]]
- Roll-up: [[Phase-4-2-1-TransitionGuardRegistry-and-DM-Session-Authority-Roll-up-2026-07-16]]
- Prior CDR: [[Conceptual-Decision-Records/deepen-phase-4-2-1-body-recompact-1200-2026-07-16-1850]]
