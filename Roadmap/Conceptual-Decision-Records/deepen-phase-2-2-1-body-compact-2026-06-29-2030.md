---
title: Deepen — Phase 2.2.1 body compact (factory feed gate)
created: 2026-06-29
project-id: genesis-mythos-master
roadmap_track: conceptual
parent_roadmap_note: "[[Phase-2-2-1-ConflictArbiter-Resolution-Policy-Roadmap-2026-06-29-2000]]"
decision_kind: deepen
queue_entry_id: architect-rr-gmm-remi-phase2-221-compact-20260629
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
validator_second_pass: "[[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-architect-rr-gmm-remi-phase2-221-compact-20260629-20260629T210500Z-second-pass]]"
product_factory_run_id: "1373c0c3408d"
tags: [roadmap, cdr, genesis-mythos-master, phase-2]
para-type: Project
---

## Summary

Compact Phase 2.2.1 tertiary body from ~8049 → 1188 chars by moving actor tables, conflict-class catalog, interface tables, edge cases, open questions, handoff readiness matrix, pseudo-code trace, research integration, and tasks to rollup child [[Phase-2-2-1-ConflictArbiter-Resolution-Policy-Roll-up-2026-06-29]]. Preserved frontmatter, sibling wikilinks, scope/behavior/handoff essentials inline.

## PMG alignment

Factory feed gate blocks while tertiary feedstock exceeds harness `body_over_cap` (1200). Compact clears oversize pending 2.2.1 after 2.1.1 GREEN without touching factory/L5 scopes.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---|---|---|---|
| Mint 2.2.2 LoreHook tertiary | New tertiary progress | Leaves 2.2.1 oversize RED | User guidance: 2.2.1 pending compact |
| Truncate tables in-place | Faster | Loses conflict policy detail | Rollup preserves tables |
| Defer to execution track | No conceptual edit | Harness material change required | factory_feed_gate red |

## Validation evidence

- Tertiary: [[Phase-2-2-1-ConflictArbiter-Resolution-Policy-Roadmap-2026-06-29-2000]]
- Rollup child: [[Phase-2-2-1-ConflictArbiter-Resolution-Policy-Roll-up-2026-06-29]]
- Pattern: [[Conceptual-Decision-Records/deepen-phase-2-1-1-body-compact-2026-06-29-2022]]

## Validator trace

- **First pass:** `needs_work` — `primary_code: state_hygiene_failure` — [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-architect-rr-gmm-remi-phase2-221-compact-20260629-20260629T205000Z]]
- **IRA call 1:** [[.technical/Internal-Repair-Agent/roadmap/2026-06/genesis-mythos-master-ira-call-1-architect-rr-gmm-remi-phase2-221-compact-20260629.md]]
- **Workflow log:** deepen L376; deepen_complete + ira_hygiene appended post-IRA
- **Second pass:** `log_only` — `primary_code: safety_unknown_gap` — [[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-architect-rr-gmm-remi-phase2-221-compact-20260629-20260629T210500Z-second-pass]] — `compare_verdict: improved_vs_first_pass_ira_hygiene_repaired_core_eligible_log_only`
