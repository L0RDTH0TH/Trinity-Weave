---
title: Phase 3.1.3 — Roll-up & Agenda Slot Tables
roadmap-level: rollup
phase-number: 3
subphase-index: 3.1.3
project-id: genesis-mythos-master
status: complete
roadmap_track: conceptual
parent-tertiary: '[[Phase-3-1-3-NPC-Agendas-Subsystem-Roadmap-2026-06-29-2330]]'
created: 2026-06-29
tags:
- roadmap
- genesis-mythos-master
- phase-3
- rollup
- npc-agendas
- lore-hooks
para-type: Project
frozen: true
conceptual_frozen_at: '2026-07-17T05:59:24Z'
---

## Compact provenance (2026-07-15)

Body compact of parent tertiary (`followup-deepen-phase313-20260715T213743Z`): **5644→≤1200** body chars; tables below remain authoritative NL detail. Slice `factory_feed_gate_status: green`; project harness advances to **3.1.4** if still oversized.

## Actors

| Actor | Role |
|-------|------|
| **NPCAgendaSubsystem** | Second **SimTickPipeline** slot after `weather` |
| **AgendaSlotRegistry** | npc_id → ordered list of { slot_id, hook_binding_id, priority, cooldown_ticks } |
| **AvailabilityWindowPolicy** | region presence + DM pause + mood_scalar gates |
| **LoreHookBindingIndex** | hook_id → { slot_id, trigger_kind, canon_fact_ref } |
| **AgendaProgressState** | slot_id → { progress, cooldown_remaining, completed } |
| **NPCAgendaTickDelta** | Proposed NPC-scoped patches only — never faction-edge keys |
| **AgendaConflictPolicy** | One committing slot transition per NPC per tick (v1) |
| **OffScreenAgendaDegradePolicy** | background NPC batch every N ticks |

## Agenda slot lifecycle (conceptual v1)

| state | Meaning | Transition |
|-------|---------|------------|
| `dormant` | Slot registered but inactive | hook binding + availability pass |
| `armed` | Eligible this tick | **AvailabilityWindowPolicy** |
| `firing` | Hook trigger consumed | **LoreHookBindingIndex** |
| `cooldown` | Post-fire wait | **AgendaProgressState** |
| `completed` | Terminal for one-shot slots | DM or canon may reset |

## Per-tick pass (algorithm sketch)

```
mood_ctx = RegionWeatherRegistry.read_only(snapshot)
for npc in AgendaSlotRegistry.active_npcs(region_scope):
  if OffScreenAgendaDegradePolicy.skip_this_tick(npc): continue
  armed = AvailabilityWindowPolicy.filter(npc.slots, mood_ctx, DMPauseGate)
  chosen = AgendaConflictPolicy.pick_one(armed)  // v1: highest priority wins
  if chosen and LoreHookBindingIndex.fire_eligible(chosen):
    delta = AgendaProgressState.advance(chosen)
    emit NPCAgendaTickDelta(npc_id, delta)
```

## Interface tables

### Imports

| Source | Consumption |
|--------|-------------|
| **3.1.2** **RegionWeatherRegistry** | mood_scalar for availability gates |
| **2.2** **LoreHookRegistry** | sim-active hook triggers |
| **2.1** **SimGraphSeed** | Initial NPC list + seed agenda templates |
| Parent 3.1 **ConsequenceResolver** | Merge precedence: NPC agendas above weather |

### Exports

| Export | Consumer |
|--------|----------|
| **AgendaSlotRegistry** | **3.2** off-screen activity summaries |
| **NPCAgendaTickDelta** schema | **ConsequenceResolver** |
| Hook-fired events | **WorldEventLog** via parent commit |

## Edge cases

- **Dangling lore hook:** **2.2** `dangling: true` — slot stays dormant; emit `sim.agenda_skipped_dangling_hook` on bus; no WorldState patch.
- **DM pause mid-agenda pass:** Proposals stay speculative until **WorldStateCommitter** — same atomicity as parent 3.1.
- **Conflicting NPC + canon hook:** **ConsequenceResolver** canon precedence wins; NPC delta dropped with audit event — not silent merge.
- **Zero NPC seed:** Valid degenerate — subsystem emits no deltas; weather + faction passes may still run.
- **Mood gate failure:** Slot remains `armed` but does not fire; retry next tick when **mood_scalar** crosses threshold — no catch-up burst.

## Open questions

- **Multi-slot fire per tick:** v1 caps at one — operator attestation if PMG demands parallel slot transitions.
- **Agenda template authoring:** Static tables in v1 vs **SeamRegistry** sim ports — lean SeamRegistry per parent 3.1 open question.
- **Background N for degrade:** Default N=4 conceptual placeholder; **3.2** may tighten for narrative surfacing fidelity.

## Handoff summary

| Field | Value |
|-------|-------|
| **handoff_readiness** | 80% |
| **factory_feedstock_slice** | phase_3_tertiary_tree |
| **pipeline_slot** | `npc_agendas` (second after weather) |
| **sibling_pending** | none — 3.1.4 minted [[Phase-3-1-4-FactionGraph-Subsystem-Roadmap-2026-06-30-0015]] |
| **body_compact_pending** | none for 3.1.3 — compact complete 2026-07-15; next harness cursor **3.1.4** oversize |
