---
title: CDR — Phase 5.1 Rule Engine Primitives and Plugin Hooks
cdr-type: deepen
phase-number: 5
subphase-index: "5.1"
project-id: genesis-mythos-master
queue_entry_id: godo-followup-20260626T204500Z-phase5-deepen-5-1
roadmap_track: conceptual
created: 2026-06-26
tags: [cdr, genesis-mythos-master, phase-5, rule-engine]
---

## Decision Summary

Minted Phase 5.1 secondary: **Rule Engine Primitives and Plugin Hooks** — establishes the base rule engine seam for the GMM rule system integration phase.

## Key architectural decisions locked

1. **RulePrimitive library** is the atomic building block set; plugins extend via PluginHookManifest, not by subclassing core atoms. Extensibility is additive.
2. **RuleConflictArbiter** uses priority-chain + veto semantics; session-level plugin load order deterministic (priority ASC, lexicographic tie-break). No runtime priority override by DM in 5.1 scope (OQ-5.1-003 flagged for 5.3).
3. **Session-boundary hot-swap policy** locked conceptually: new plugins take effect at session boundary; mid-session install routes through ReGenerationIntentQueue (3.3) as structural_re_gen. No live mid-session swap without operator intent.
4. **Rule DSL format** is behaviour-first / execution-deferred (OQ-5.1-001): conceptual contract specifies condition/effect/trigger triple schema; format is an execution-track choice.
5. **RuleEffectBus** channels all effect routing asynchronously to subsystem queues; DMPauseGate (3.1) holds world_delta effects during DM pause — rule effects are not immune to sim pause semantics.

## Phase 5 breadth status

- 5.1: rule engine primitives + plugin hooks — **minted this run** ✓
- 5.2: spell agency/perspective metadata — pending next deepen
- 5.3: quest pressure from canon graph — pending

## Validation status

- Post-mint validator: pending nested cycle (this CDR created pre-validator in same run)
- primary_code: TBD (balance cycle running)
- execution_gaps_advisory: true (conceptual_v1)

## Source note

[[Phase-5-1-Rule-Engine-Primitives-and-Plugin-Hooks-Roadmap-2026-06-26-2045]]
