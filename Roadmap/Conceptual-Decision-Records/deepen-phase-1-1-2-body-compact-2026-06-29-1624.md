---
title: CDR — Phase 1.1.2 body compact
created: 2026-06-29
project-id: genesis-mythos-master
roadmap_track: conceptual
para-type: Project
tags: [cdr, conceptual-decision, phase-1, layer-decoupling, factory-feed-gate]
status: validated
validation_status: validated
validator_second_pass: "[[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-architect-rr-gmm-remi-df6901a9-next-20260629T163000Z-second-pass]]"
validator_report: "[[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-architect-rr-gmm-remi-df6901a9-next-20260629T162500Z]]"
validator_report: "[[.technical/parallel/godot/Validator/validator-roadmap_handoff_auto-architect-rr-gmm-remi-df6901a9-next-20260629T162500Z]]"
ira_report: "[[.technical/Internal-Repair-Agent/roadmap/2026-06/genesis-mythos-master-ira-call-1-architect-rr-gmm-remi-df6901a9-next.md]]"
parent_roadmap_note: "[[Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roadmap-2026-06-29-0932]]"
decision_kind: deepen
queue_entry_id: architect-rr-gmm-remi-df6901a9-next
product_factory_run_id: 1373c0c3408d
persona_id: half_a.conceptual_architect
---

## Decision

Compact **Phase 1.1.2** tertiary body (7616→≤1200 chars) per `factory_feed_gate` oversize blocker; dense tables moved to rollup child [[Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roll-up-2026-06-29]] following 1.3.x body compact pattern.

## Rationale

Harness authority `factory_feed_gate` required material body compaction before `pmg_phases` mint batch; `harness_forbid_deepen_noop` and `harness_material_change_required` mandate rollup split — not deepen_noop.

## Evidence

- Tertiary: [[Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roadmap-2026-06-29-0932]]
- Rollup: [[Phase-1-1-2-Bus-Category-Registry-and-CanonCommitBoundary-Roll-up-2026-06-29]]
- Prior pattern: [[Phase-1-3-2-SeedSnapshotAuthority-Contract-Roll-up-2026-06-29]], [[Phase-1-2-1-Stage-DAG-Node-Contracts-Roll-up-2026-06-29]]

## Out of scope

Factory/L5 mint, User-Story scopes, bus serialization schemas, Godot wiring.
