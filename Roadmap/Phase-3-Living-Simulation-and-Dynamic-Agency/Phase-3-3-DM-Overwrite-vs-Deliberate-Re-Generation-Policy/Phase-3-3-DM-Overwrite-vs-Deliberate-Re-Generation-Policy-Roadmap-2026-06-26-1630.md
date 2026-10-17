---
title: Phase 3.3 — DM Overwrite vs Deliberate Re-Generation Policy
roadmap-level: secondary
phase-number: 3
subphase-index: '3.3'
project-id: genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 80
factory_feedstock_slice: phase_3_secondary_tree
body_compact_status: complete
factory_feed_gate_status: green
created: 2026-06-26
tags:
- roadmap
- genesis-mythos-master
- phase-3
- dm-authority
- overwrite
- re-generation
- narrative-policy
para-type: Project
roadmap_track: conceptual
rollup-detail: '[[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roll-up-2026-07-15]]'
links:
- '[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-06-26-0914]]'
- '[[Phase-3-1-Tick-Based-Simulation-Core-Roadmap-2026-06-26-1600]]'
- '[[Phase-3-2-Off-Screen-Faction-Tribe-Activity-Roadmap-2026-06-26-1615]]'
- '[[Phase-2-2-Canon-Registry-and-Intent-Resolver-Roadmap-2026-06-26-1530]]'
- '[[Phase-2-3-ToneProfile-Profile-Bundle-on-World-Seed-Roadmap-2026-06-26-1535]]'
- '[[Phase-1-3-Modularity-Seams-and-Safety-Invariants-Roadmap-2026-06-26-1437]]'
- '[[genesis-mythos-master-goal]]'
product_factory_run_id: 1373c0c3408d
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Phase 3.3 — DM Overwrite vs Deliberate Re-Generation Policy

When DM may **live-patch** simulation vs when change must **queue deliberate re-generation**. Owns classification, patch-layer semantics, re-gen queue, and reconciliation with **3.1** commit gates / **3.2** dm_queue — nouns + policy only.

## Scope

**In:** **DMOverwriteClass**, **LiveOverwriteRegistry**, **StructuralChangeDetector**, **ReGenerationIntentQueue**, **OverwritePatchLayer**, **DMPauseGate** coord, **SpeculativeDeltaReconciler**, **NarrativeDeltaVetoPolicy**, **CanonConflictArbiter**, **ProvenanceEnvelope**, **RollbackWindow**. **Out:** **3.1** tick math; **3.2** narrative compile; Phase 2.1 DAG exec; Godot tooling; factory/L5.

## Behavior

Classify → registry / structural escalate → pause gate → patch stack **or** re-gen job → speculative reconcile → optional **3.2** veto → `dm.overwrite_applied` / `dm.re_gen_queued`.

## Interfaces

Imports: **3.1** pause/commit/speculative queue; **3.2** dm_queue deltas; **2.2** IntentResolver; **2.3** tone; **1.3** provenance. Exports: patch layer + **ReGenerationIntent** → Phase 4 / Phase 2.1 exec.

## Roll-up

Policy matrix, flows, edge cases → [[Phase-3-3-DM-Overwrite-vs-Deliberate-Re-Generation-Policy-Roll-up-2026-07-15]].

## Handoff

**80%** — NL complete; detail in rollup. Exec-deferred: typed serializers, HR gates.
