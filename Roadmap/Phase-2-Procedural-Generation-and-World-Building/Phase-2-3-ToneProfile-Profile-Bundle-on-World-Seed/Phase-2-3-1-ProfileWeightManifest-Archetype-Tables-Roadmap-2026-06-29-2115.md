---
title: Phase 2.3.1 — ProfileWeightManifest Archetype Tables
roadmap-level: tertiary
phase-number: 2
subphase-index: 2.3.1
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feedstock_slice: phase_2_tertiary_tree
body_compact_status: complete
factory_feed_gate_status: green
branch_open: false
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-2
- tone-profile
- profile-weight-manifest
- archetype-registry
para-type: Project
roadmap_track: conceptual
rollup-detail: '[[Phase-2-3-1-ProfileWeightManifest-Archetype-Tables-Roll-up-2026-06-29]]'
links:
- '[[Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]'
- '[[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-06-26-0914]]'
- '[[Phase-2-1-Generation-Pipeline-Stages-Roadmap-2026-06-26-1515]]'
- '[[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]'
- '[[Phase-1-2-1-Stage-DAG-Node-Contracts-Roadmap-2026-06-26-1105]]'
- '[[genesis-mythos-master-goal]]'
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 2.3.1 — ProfileWeightManifest Archetype Tables

Canonical **ProfileWeightManifest** namespace tables for four PMG built-in archetypes. Parent [[Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]; nouns + table contracts only.

## Scope

**In:** **ArchetypeRegistry**, **ProfileWeightManifest** namespaces (`terrain`–`quest`), **PaletteVetoKey**, **NamespaceDefaultResolver**, **ReceptiveNodeBinding**. **Out:** Session0 UI, `data/archetypes/`, Godot loaders, factory/L5.

## Behavior

Registry lookup → manifest namespaces → veto application → **ToneProfileInjector** at 2.1 receptive nodes per **ReceptiveNodeBinding** index. Four archetype ids; six namespaces.

## Interfaces

Imports: 1.2.1 stage DAG, 2.1 pipeline, 2.2 ToneCompatibilityGate, `session.*`. Exports: registry index, manifest tables, veto schema → factory mint / execution mirror.

## Roll-up

Tables, edge cases, handoff → [[Phase-2-3-1-ProfileWeightManifest-Archetype-Tables-Roll-up-2026-06-29]].

## Handoff

**80%** — NL complete; detail in rollup. Execution-deferred: Godot loaders, REGISTRY-CI, HR rollup gates.
