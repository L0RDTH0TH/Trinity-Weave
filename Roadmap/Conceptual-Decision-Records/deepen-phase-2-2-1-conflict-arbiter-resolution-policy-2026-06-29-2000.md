---
title: "Deepen — Phase 2.2.1 ConflictArbiter resolution policy"
created: 2026-06-29
tags: [roadmap, cdr, genesis-mythos-master, phase-2, conflict-arbiter]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-2-2-1-ConflictArbiter-Resolution-Policy-Roadmap-2026-06-29-2000]]"
decision_kind: deepen
queue_entry_id: architect-rr-gmm-remi-phase2-tertiary-next-20260629
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: pending_validator_second_pass
related_research: []
persona_id: half_a.conceptual_architect
---

# Deepen — Phase 2.2.1 ConflictArbiter resolution policy

## Summary

Minted **2.2.1 — ConflictArbiter Resolution Policy** as second Phase 2 tertiary under factory feed gate cursor `phase_2_tertiary_tree`. Materializes resolution modes (`reject_new`, `prefer_incumbent`, `table_merge`, `defer_to_dm`, `split_thread`), **MergeTablePolicy** (explicit table quorum — no silent merge), and conflict-class bindings deferred in parent 2.2 § Responsibilities.

## PMG alignment

PMG requires collaborative canon: player intents become facts only after table visibility. Parent 2.2 named **ConflictArbiter** and forbade silent merge; this tertiary makes resolution authority explicit for factory feedstock and later DM workbench UX.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|-------------|--------|----------|----------------|
| 2.1.1 body compact first | Clears oversize blocker on 2.1.1 (7736 chars vs cap 1200) | Delays new tertiary mint while gate RED for tree incomplete | **Superseded 2026-06-29:** both 2.1.1 + 2.2.1 body compacts GREEN; depth-first advance to 2.2.1 mint chosen per user guidance |
| RegistrySnapshot schema tertiary | Completes 2.2 task backlog item | Lower factory-feed priority vs ConflictArbiter named in user guidance | User guidance explicitly cites 2.2.1 ConflictArbiter |
| Inline expand parent 2.2 only | No new file | Violates tertiary tree harness; gate stays RED | Factory feed gate requires tertiary mints under phase_2_tertiary_tree |

**Chosen path:** 2.2.1 ConflictArbiter resolution policy as second Phase 2 tertiary.

## Validation evidence

- Pattern: parent 2.2 § Behavior ConflictArbiter actor + § Edge cases conflicting canon
- Pattern: Phase 1.2.2 intent collision boundaries
- Parent deferral: 2.2 § Responsibilities optional tertiary ConflictArbiter — now minted

## Links

- Minted tertiary: [[Phase-2-2-1-ConflictArbiter-Resolution-Policy-Roadmap-2026-06-29-2000]]
- Workflow anchor: 2026-06-29 20:00 | Phase-2-2-1-ConflictArbiter-Resolution-Policy | architect-rr-gmm-remi-phase2-tertiary-next-20260629
- Persona: half_a.conceptual_architect | product_factory_run_id: 1373c0c3408d

## Validator trace

- `validator_first: needs_work` | `primary_code: state_hygiene_failure` | `reason_codes: state_hygiene_failure,contradictions_detected,safety_unknown_gap`
- `report: [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-architect-rr-gmm-remi-phase2-tertiary-next-20260629-20260629T201500Z]]`
- `ira_applied: true` | `ira_report: [[.technical/Internal-Repair-Agent/roadmap/2026-06/genesis-mythos-master-ira-call-1-architect-rr-gmm-remi-phase2-tertiary-next-20260629.md]]`
- `body_compact: complete` (2.1.1 + 2.2.1 GREEN 2026-06-29) | compact CDR: [[Conceptual-Decision-Records/deepen-phase-2-2-1-body-compact-2026-06-29-2030]] | next: validator second pass on compact slice
