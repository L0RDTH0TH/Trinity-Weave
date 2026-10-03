---
title: Deepen — Phase 1.2.1 body compact (factory feed gate)
created: 2026-06-29
project-id: genesis-mythos-master
roadmap_track: conceptual
parent_roadmap_note: "[[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]"
decision_kind: deepen
queue_entry_id: resume-deepen-gmm-121-compact-20260629T131500Z
master_goal: "[[genesis-mythos-master-goal]]"
validation_status: validated
validator_second_pass: "[[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-resume-deepen-gmm-121-compact-20260629T131500Z-20260629T141500Z-second-pass]]"
validator_report: "[[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-resume-deepen-gmm-121-compact-20260629T131500Z-20260629T141500Z]]"
ira_report: "[[.technical/Internal-Repair-Agent/roadmap/2026-06/genesis-mythos-master-ira-call-1-resume-deepen-gmm-121-compact-20260629T131500Z.md]]"
product_factory_run_id: "1373c0c3408d"
tags: [roadmap, cdr, genesis-mythos-master, phase-1]
para-type: Project
---

## Summary

Compact Phase 1.2.1 tertiary body from ~11370 → ≤1200 chars by moving per-stage contract tables, StageDAG edge registry, ToneProfile injection registry, invariants, pseudo-code, and handoff table to rollup child [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roll-up-2026-06-29]]. Preserved frontmatter, sibling wikilinks, scope/behavior/handoff essentials inline.

## PMG alignment

Factory feed gate blocks PRODUCT_FACTORY_CONTINUE while tertiary feedstock exceeds harness `body_over_cap` (1200). Compact pattern matches Phase 1 primary oversize reconcile — keeps proc-gen DAG contract authority in vault without losing table detail.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
|---|---|---|---|
| Split into multiple tertiaries | Smaller files | Breaks 1.2.1 slice identity | Harness targets this path |
| Truncate tables in-place | Faster | Loses contract detail | Rollup preserves tables |
| Defer compact to execution track | No conceptual edit | Factory gate stays RED | Harness requires conceptual fix |

## Validation evidence

- Tertiary: [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]
- Rollup child: [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roll-up-2026-06-29]]
- Pattern: [[Conceptual-Decision-Records/deepen-phase1-primary-body-compact-2026-06-29-1215]]
- Snapshot: Backups/Per-Change/Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105--a1b2c3d4--20260629-140000.md.bak

## Links

- Workflow log: 2026-06-29 14:00 compact deepen row appended
- Persona: half_a.conceptual_architect
- `gate_signature: conceptual_note_oversized:body_over_cap`
