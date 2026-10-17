---
title: Phase 3.1.4 — Roll-up & Edge Weight Tables
roadmap-level: rollup
phase-number: 3
subphase-index: 3.1.4
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-tertiary: '[[Phase-3-1-4-FactionGraph-Subsystem-Roadmap-2026-06-30-0015]]'
created: 2026-06-30
tags:
- roadmap
- genesis-mythos-master
- phase-3
- rollup
- faction-graph
- reputation
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Actors

| Actor | Role |
|-------|------|
| **FactionGraphSubsystem** | Third **SimTickPipeline** slot after `npc_agendas` |
| **FactionGraphRegistry** | Nodes { faction_id, tribe_id } + edges { src, dst, edge_kind, weight } |
| **EdgeWeightPolicy** | decay_rate, min_weight, max_weight per edge_kind |
| **ThresholdRuleIndex** | rule_id → { predicate, edge_mutation, cooldown_ticks } |
| **OffScreenEventScheduler** | background-region event arms — math only |
| **FactionGraphTickDelta** | Graph-scoped patches only — never NPC agenda keys |
| **GraphConflictPolicy** | One committing mutation per (src, dst, edge_kind) per tick (v1) |
| **TribeMembershipIndex** | tribe_id → parent_faction_id |

## Edge kinds (conceptual v1)

| edge_kind | Meaning | Typical weight range |
|-----------|---------|-------------------|
| `reputation` | Directed favor/hostility | -100 .. +100 |
| `tension` | Escalation pressure (raids, feuds) | 0 .. 100 |
| `treaty` | Formal pact strength | 0 .. 100 |
| `trade` | Economic coupling | 0 .. 100 |

## Per-tick pass (algorithm sketch)

```
for region in RegionScopeResolver.active(snapshot):
  decay = EdgeWeightPolicy.passive_decay(FactionGraphRegistry.edges_in(region))
  candidates = ThresholdRuleIndex.evaluate(decay, npc_agenda_side_effects_readonly)
  offscreen = OffScreenEventScheduler.advance(region) if region.is_background
  chosen = GraphConflictPolicy.pick_one_per_edge_key(candidates + offscreen)
  emit FactionGraphTickDelta(chosen)
```

## Interface tables

### Imports

| Source | Consumption |
|--------|-------------|
| **3.1.3** agenda side-effects | Threshold predicates only — read-only |
| **2.1** **SimGraphSeed** | Initial topology + seed weights |
| **2.2** **LoreHookRegistry** | Canon-triggered faction events |
| Parent 3.1 **ConsequenceResolver** | Merge precedence: faction rules above NPC/weather |

### Exports

| Export | Consumer |
|--------|----------|
| **FactionGraphRegistry** | **3.2** **FactionGraphDeltaExtractor** |
| **FactionGraphTickDelta** schema | **ConsequenceResolver** |
| Armed off-screen events | **3.2** **TribeActivityScheduler** |

## Edge cases

- **Circular reputation loops:** **GraphConflictPolicy** breaks ties by rule priority — no oscillation within single tick.
- **Tribe split mid-tick:** **TribeMembershipIndex** stale read — block commit, emit `sim.faction_graph_stale_membership` — DM reconcile.
- **Zero-edge seed:** Valid degenerate — subsystem emits no deltas; weather/NPC passes may still run.
- **Conflicting canon + threshold:** **ConsequenceResolver** canon precedence wins; faction delta dropped with audit event.
- **Background batch lag:** **OffScreenEventScheduler** may defer N ticks — **3.2** **AbsenceCatchupBridge** packages without re-running tick math.

## Open questions

- **Multi-edge mutation per pair:** v1 caps at one — operator attestation if PMG demands parallel reputation + tension shifts.
- **Dynamic node creation:** Static seed topology in v1 vs runtime faction spawn — lean static + DM-triggered promotions per **3.3**.
- **Decay baseline per ToneProfile:** Neutral point may vary by profile — deferred to **2.3** execution deepen.

## Handoff summary

| Field | Value |
|-------|-------|
| **handoff_readiness** | 80% |
| **factory_feedstock_slice** | phase_3_tertiary_tree |
| **pipeline_slot** | `faction_graph` (third after weather, npc_agendas) |
| **3.1 branch** | pipeline tertiaries complete (3.1.1–3.1.4) |
| **body_compact_pending** | none (3.1.1–3.1.4 tertiaries cleared 2026-07-15) |
